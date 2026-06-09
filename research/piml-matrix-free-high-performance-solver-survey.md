---
title: "面向大规模结构拓扑优化的 PIML 与 Matrix-Free 高性能求解方法——技术调研"
tags:
  - PIML
  - matrix-free
  - topology-optimization
  - substructuring
  - multigrid
  - PETSc
  - parallel-computing
  - GPU
  - high-performance-computing
status: "in-progress"
date: 2026-06-07
source: "郭旭老师团队在大规模结构拓扑优化中 PIML 与 Matrix-Free 高性能求解的研究报告.pdf"
---

# 面向大规模结构拓扑优化的 PIML 与 Matrix-Free 高性能求解方法

> 本调研对应 [[postdoc-research-plan]] 中第一个研究计划题目。内容以用户提供的研究报告为主线，并结合仓库内已有的 PIML 论文笔记，对方法脉络、现有实现边界与可开展的研究工作作进一步技术化梳理。

---

## 一、问题背景与研究定位

大规模三维结构拓扑优化需要在数百至数千次优化迭代中反复完成结构分析、灵敏度计算、过滤与设计变量更新。随着网格规模进入亿级乃至十亿级，主要瓶颈表现为：

1. 全尺度有限元方程自由度巨大，刚度矩阵组装、存储和求解成本高；
2. 迭代过程中材料分布持续变化，局部刚度与预条件器需要频繁更新；
3. 高分辨率密度场、位移场和中间算子造成显著内存压力；
4. 分布式并行中的通信、负载均衡和粗网格求解逐渐成为扩展性瓶颈；
5. 当 FEA 被显著加速后，过滤、灵敏度分析和 OC/MMA 更新会成为新的主要耗时环节。

郭旭老师团队的 PIML 路线并不直接预测最终拓扑，而是学习可嵌入有限元或子结构分析的局部力学对象，例如多尺度形函数和缩聚刚度。其基本思想可以概括为：

$$
\text{局部材料分布}
\xrightarrow{\text{PIML}}
\text{多尺度形函数/缩聚算子}
\xrightarrow{\text{子结构或粗网格求解}}
\text{全局位移}
\xrightarrow{\text{恢复}}
\text{细网格响应与灵敏度}.
$$

这一思路在算法层面降低全局平衡方程规模，在并行层面利用不同子结构之间局部计算相互独立的特点，并进一步以 Matrix-Free 思想缓解中间算子的存储压力。因此，它适合作为“大规模拓扑优化 + 数值 PDE + 高性能计算”交叉研究的基础框架。

---

## 二、团队研究演化主线

| 时间 | 代表工作 | 方法推进 | 对本课题的意义 |
|---|---|---|---|
| 2022 | Huang et al., EML 56:101887 | 在 EMsFEM 中学习粗单元多尺度形函数，提出问题无关 PIML | 建立“学习局部力学算子而非最终拓扑”的基本范式 |
| 2023 | Huang et al., EML 63:102041 | 推广到三维子结构法，引入边界变形假设和秩保持约束 | 将 PIML 推向十亿级设计变量和三维大规模分析 |
| 2024 | Zhang et al., EML 72:102237 | 以等参单元处理复杂设计域 | 弱化规则矩形/砖体子结构对几何的限制 |
| 2024 | Huang et al., JMPS 193:105893 | 基于力学型代价函数构建 data-free PIML | 降低监督标签生成成本，增强物理一致性 |
| 2026 | Ma et al., Acta Mech. Sin. 42 | PIML + MPI 并行 + 多重网格 + Matrix-Free 存储策略 | 形成面向个人工作站和超算平台的高性能实现 |

从演化逻辑看，团队路线经历了五个连续步骤：

```text
二维 EMsFEM 形函数学习
  → 三维子结构缩聚
  → 复杂设计域
  → data-free 力学训练
  → 分布式并行、多重网格与 Matrix-Free
```

其稳定不变的核心是：把机器学习放在有限元分析的局部算子构造环节，从而使训练模型尽可能独立于具体载荷、边界条件和整体设计域。

---

## 三、PIML 的数值力学基础

### 3.1 从经典子结构法到 PIML

对子结构 $\Omega^j$，将自由度分为边界自由度和内部自由度：

$$
\begin{bmatrix}
\mathbf K_{\mathrm{bb}}^j & (\mathbf K_{\mathrm{ib}}^j)^T\\
\mathbf K_{\mathrm{ib}}^j & \mathbf K_{\mathrm{ii}}^j
\end{bmatrix}
\begin{bmatrix}
\mathbf u_{\mathrm b}^j\\
\mathbf u_{\mathrm i}^j
\end{bmatrix}
=
\begin{bmatrix}
\mathbf f_{\mathrm b}^j\\
\mathbf 0
\end{bmatrix}.
$$

消去内部自由度后，得到 Schur 补意义下的缩聚刚度：

$$
\mathbf K_{\mathrm s}^j
=
\mathbf K_{\mathrm{bb}}^j
-
(\mathbf K_{\mathrm{ib}}^j)^T
(\mathbf K_{\mathrm{ii}}^j)^{-1}
\mathbf K_{\mathrm{ib}}^j.
$$

内部位移可以由边界位移恢复：

$$
\mathbf u_{\mathrm i}^j
=
-
(\mathbf K_{\mathrm{ii}}^j)^{-1}
\mathbf K_{\mathrm{ib}}^j
\mathbf u_{\mathrm b}^j,
$$

相应离散多尺度形函数可记为：

$$
\mathbf N^j
=
\begin{bmatrix}
-(\mathbf K_{\mathrm{ii}}^j)^{-1}\mathbf K_{\mathrm{ib}}^j\\
\mathbf I
\end{bmatrix},
\qquad
\mathbf K_{\mathrm s}^j=(\mathbf N^j)^T\mathbf K^j\mathbf N^j.
$$

传统子结构法的问题在于：拓扑优化每轮都会改变子结构内部材料分布，因此 $\mathbf N^j$ 和 $\mathbf K_{\mathrm s}^j$ 需要反复计算。PIML 用轻量神经网络近似映射

$$
\mathcal F_\theta:
\boldsymbol{\rho}^j
\longmapsto
\mathbf N^j
\quad\text{或}\quad
\mathbf K_{\mathrm s}^j,
$$

从而用网络推理和局部矩阵运算替代内部自由度消元。

### 3.2 “问题无关”的准确含义

PIML 中的 “Problem-Independent” 不是指模型对任意 PDE、材料本构和离散格式均无条件通用，而是指：

- 在控制方程、材料模型、局部离散模板和子结构类型保持一致时；
- 所学习的局部形函数或缩聚算子不显式依赖整体载荷和边界条件；
- 相同局部模型可以复用于不同的整体设计域和拓扑优化算例。

因此，PIML 的可迁移范围仍受以下因素限制：

1. PDE 类型与本构关系；
2. 单元类型和子结构拓扑；
3. 粗细网格比 $m$；
4. 边界变形假设；
5. 密度取值范围及训练分布；
6. 线性/非线性、小变形/大变形等物理假设。

这一区分对研究设计很重要：应把“问题无关性”表述为特定算子族内的可复用性，而不是无限制泛化。

### 3.3 物理约束与结构保持

PIML 预测对象最终要进入有限元平衡方程，因此仅控制逐分量预测误差并不充分。模型至少应满足或近似满足：

- 刚体模态再现；
- 分区单位性质；
- 缩聚刚度对称性；
- 半正定/正定性；
- 秩保持；
- 能量一致性；
- 对材料密度变化的连续性与稳定性。

2022 年方法使用“形函数误差 + 刚度矩阵误差”联合损失；2023 年方法进一步强调 rank-preserving property；2024 年 data-free 方法采用力学型代价函数。对本课题而言，更自然的研究方向是建立结构保持的参数化，例如直接预测满足对称正定约束的局部算子，或在能量范数下训练：

$$
\mathcal L_{\mathrm{energy}}
=
\sum_j
\left|
(\mathbf u_{\mathrm b}^j)^T
\left(
\widehat{\mathbf K}_{\mathrm s}^j-\mathbf K_{\mathrm s}^j
\right)
\mathbf u_{\mathrm b}^j
\right|^2.
$$

---

## 四、Matrix-Free 的现有实现与概念边界

### 4.1 2026 年工作的实际做法

根据 2026 年并行 PIML 论文的公开正文材料，串行实现会保存所有子结构的多尺度形函数。对于 $800\times400\times400=1.28$ 亿个细观单元的设计域，双精度存储全部多尺度形函数约需 98.1 GB 内存。

并行版本采用的 Matrix-Free 策略是：

1. 每个进程按需调用 PIML 模型预测本地多尺度形函数；
2. 立即计算子结构缩聚刚度；
3. 完成局部计算后释放多尺度形函数，不长期存储；
4. 在恢复细网格位移时再次预测多尺度形函数。

这一方案本质上是以重复计算换取存储空间，缓解的是**多尺度形函数这一中间量**的内存压力。

### 4.2 与“全局算子 Matrix-Free”的区别

论文并行流程仍包含粗网格全局刚度的组装操作，并使用 PETSc 的 `MatAssemblyBegin` 等接口。因此，当前公开实现不宜笼统表述为“所有层次均不组装矩阵”。更准确的分类是：

| 层次 | 当前公开实现 | 可进一步研究的形式 |
|---|---|---|
| 多尺度形函数 $\mathbf N^j$ | 按需预测、计算后释放 | 已实现 Matrix-Free/无持久存储 |
| 子结构缩聚刚度 $\mathbf K_{\mathrm s}^j$ | 局部计算 | 可按需计算或分层缓存 |
| 全局粗网格刚度 $\mathbf K_{\mathrm s}$ | 仍有显式组装 | 真正的全局 Matrix-Free 算子作用 |
| 多重网格预条件器 | PETSc 并行 MG | 需设计与全局 Matrix-Free 兼容的层次算子 |

真正的全局 Matrix-Free 形式可写为：

$$
\mathbf y
=
\mathbf K_{\mathrm s}\mathbf x
=
\sum_j
(\mathbf A^j)^T
\mathbf K_{\mathrm s}^j
\mathbf A^j\mathbf x,
$$

其中 $\mathbf A^j$ 是从全局粗网格向量提取子结构边界自由度的限制算子。该表达式不要求显式形成 $\mathbf K_{\mathrm s}$，只需对子结构执行局部算子作用。

进一步代入 PIML 多尺度形函数：

$$
\mathbf y
=
\sum_j
(\mathbf A^j)^T
(\widehat{\mathbf N}^j)^T
\mathbf K^j
\widehat{\mathbf N}^j
\mathbf A^j\mathbf x.
$$

这为“PIML 预测局部算子 + 全局 Matrix-Free Krylov 求解”提供了直接数学接口，也是本研究题目相对已有工作的关键增量。

### 4.3 真正 Matrix-Free 化的主要难点

1. **预条件器构造**：不组装全局矩阵后，代数多重网格难以直接建立，需要几何多重网格、p/h 多重网格、低阶组装代理或块对角/Schwarz 预条件。
2. **算子一致性**：PIML 预测误差可能破坏对称性和正定性，影响 CG/MINRES 等 Krylov 方法的收敛。
3. **重复推理成本**：每次 MatVec 若重新预测 $\mathbf N^j$，网络推理可能成为瓶颈，需要比较“缓存 $\mathbf K_{\mathrm s}^j$”“缓存压缩表示”和“完全重算”三种策略。
4. **拓扑迭代中的算子更新**：每轮密度变化后局部算子随之变化，预条件器的复用和增量更新机制需要专门设计。
5. **边界与非均匀子结构**：均匀内部子结构容易复用，复杂边界、载荷附近和非规则区域需要精确处理或混合组装。

---

## 五、并行求解框架与性能瓶颈

### 5.1 已有并行框架

2026 年方法基于 PETSc 3.19，主要组成包括：

- MPI 分布式粗、细网格划分；
- 子结构局部 PIML 推理与缩聚刚度计算；
- PETSc 并行多重网格；
- GMRES 求解粗网格平衡方程；
- PDE 型 Helmholtz 滤波；
- Heaviside 投影；
- 并行 MMA 更新。

以 10.24 亿细观单元为例，设计域分配到 2000 个 CPU 核心；当 $m=10$ 时，每个进程处理 512 个子结构。子结构局部刚度、内部位移、应变能和灵敏度可独立计算，因此局部阶段通信需求较低。

### 5.2 当前瓶颈的层次迁移

PIML 会把计算瓶颈从“全尺度 FEA”逐步转移到其他模块：

```text
全尺度矩阵组装与求解
  → 粗网格全局求解
  → 局部形函数/缩聚算子生成
  → 细网格位移恢复
  → 过滤、灵敏度与设计变量更新
  → 通信和最粗网格瓶颈
```

因此，高性能研究不能只比较一次线性求解的时间，而应记录完整优化迭代的时间分解：

$$
T_{\mathrm{iter}}
=
T_{\mathrm{PIML}}
+T_{\mathrm{local}}
+T_{\mathrm{solve}}
+T_{\mathrm{recover}}
+T_{\mathrm{sens}}
+T_{\mathrm{filter}}
+T_{\mathrm{opt}}
+T_{\mathrm{comm}}.
$$

### 5.3 CPU 并行与 GPU 加速的关系

现有 2026 工作主要是 CPU/MPI 分布式并行，并不能直接等同于 GPU 高性能实现。GPU 方向可重点考虑：

- 批量 PIML 推理；
- 子结构局部算子作用；
- 全局 Matrix-Free MatVec；
- 向量更新与归约；
- PDE 滤波；
- 灵敏度计算；
- OC/MMA 中可并行的数据操作。

其中，局部子结构具有固定模板、批量规模大、算术强度较高，是 GPU 友好的计算单元；全局 Krylov 求解中的点积、归约和粗网格通信则可能限制扩展性。

---

## 六、公开算例与量化结果

### 6.1 代表性结果

| 工作 | 规模 | 平台/并行度 | 公开结果 |
|---|---|---|---|
| Huang et al. 2022 | $3200\times1600$ 二维短悬臂梁 | Xeon Gold 6256 | 单步约 3.9--4.1 倍加速 |
| Huang et al. 2022 | 2 亿细单元 MBB 梁 | 单工作站 | 典型迭代 FEA 约 2 分钟 |
| Huang et al. 2023 | 10 亿设计变量、30 亿自由度 | 单工作站 | 摘要报告结构分析效率提升 $10^4$--$10^5$ 量级 |
| Ma et al. 2026 | 3456 万细单元悬臂梁 | 48 CPU 核 | 平均每步约 3.1 s；小规模下柔顺度相对误差约 13.96% |
| Ma et al. 2026 | 1.28 亿细单元悬臂梁 | 40 CPU 核 | 平均每步约 105.9 s；柔顺度相对误差降至约 4.9% |
| Ma et al. 2026 | 150 万细单元 MBB 梁 | 30 CPU 核 | 平均每步约 2.6--2.8 s |

### 6.2 结果解读

这些结果说明：

1. PIML 的优势在大规模问题上更加明显；
2. 子结构边界线性变形假设会带来刚度偏高和柔顺度误差；
3. 增加子结构数量、减小单个子结构对应的物理尺度可改善精度；
4. 性能评价必须同时报告近似误差，不能只报告加速比；
5. PIML 降维、分布式并行和多重网格是三个相互叠加的加速层次；
6. 极限规模下的瓶颈将逐渐转向内存、全局归约、粗网格和优化更新。

---

## 七、现有方法的优势与局限

### 7.1 主要优势

- 学习对象具有明确的数值力学含义，可嵌入标准有限元流程；
- 模型对整体载荷和边界条件具有较好的复用性；
- 子结构局部任务天然适合数据并行；
- PIML 与多重网格、子结构法和 PETSc 软件栈兼容；
- 可通过按需预测多尺度形函数显著降低内存占用；
- 已形成从单机到分布式超算的连续验证路线。

### 7.2 主要局限

- 现有成果主要集中在线弹性、小变形和规则子结构；
- 边界线性变形假设存在可观离散误差；
- “问题无关性”仍依赖 PDE、本构、单元和局部模板保持一致；
- 公开实现的 Matrix-Free 主要针对多尺度形函数存储，并非全局刚度算子的完全无矩阵化；
- 现有并行结果主要基于 CPU/MPI，GPU 内核与异构并行尚未充分公开；
- 预测算子的对称正定性、谱等价性和严格误差传播理论仍不完整；
- 官方开源代码和标准 benchmark 不充分，外部复现成本较高；
- 当 FEA 显著加速后，过滤和优化器更新会成为新的性能瓶颈。

---

## 八、开放科学问题

### 8.1 PIML 误差如何影响优化结果

需要建立从局部算子误差到全局响应、灵敏度和最终拓扑误差的传递链：

$$
\|\widehat{\mathbf K}_{\mathrm s}^j-\mathbf K_{\mathrm s}^j\|
\rightarrow
\|\widehat{\mathbf u}-\mathbf u\|
\rightarrow
\|\widehat{\nabla J}-\nabla J\|
\rightarrow
\text{优化收敛与拓扑偏差}.
$$

尤其应关注近似算子是否会导致灵敏度方向错误、灰度区震荡或优化停滞。

### 8.2 如何保证学习算子的结构性质

可研究：

- Cholesky/谱分解参数化的正定局部刚度；
- 刚体模态硬约束；
- 对称化与特征值截断；
- 能量范数损失；
- 局部谱等价约束；
- 与有限元误差估计器结合的可信度指标。

### 8.3 Matrix-Free 情形下如何构造高效预条件器

候选路线包括：

- 几何多重网格；
- 组装低阶/低精度代理矩阵作为预条件器；
- 子结构块 Jacobi、加性 Schwarz；
- 稀疏近似逆；
- PIML 预测局部平滑器或谱粗空间；
- 混合策略：算子 Matrix-Free，预条件矩阵低频更新。

### 8.4 如何在精度、内存与算力之间自适应切换

不同子结构可采用不同处理方式：

| 子结构类型 | 建议策略 |
|---|---|
| 纯实体/纯弱材料 | 直接查表或解析缩聚 |
| 密度变化平缓 | PIML 预测并缓存压缩算子 |
| 边界/高梯度区域 | 精确局部消元或高精度 PIML |
| 预测不确定度高 | 回退到直接计算并加入在线样本 |

这可形成“学习算子 + 精确算子”的自适应混合求解器。

### 8.5 非线性和多物理场下的可迁移性

当问题进入几何非线性、材料非线性、接触或热-力耦合后，局部算子不再只由静态密度决定，还依赖状态变量、加载路径和切线刚度。需要重新定义“问题无关”的状态空间和训练对象。

---

## 九、面向博士后课题的研究切入点

### 方向 A：可复现基准与误差-性能评估体系

先建立二维/三维 SIMP 基准程序，对比：

1. 全尺度组装式 FEM；
2. 经典子结构缩聚；
3. PIML 子结构；
4. PIML + 多重网格；
5. PIML + 全局 Matrix-Free；
6. CPU 与 GPU 实现。

统一记录柔顺度误差、位移误差、灵敏度误差、迭代次数、峰值内存、通信量、每轮时间分解、强扩展和弱扩展效率。

### 方向 B：真正的 PIML 全局 Matrix-Free 算子

实现全局缩聚算子的按需作用：

```text
提取子结构边界向量
  → PIML/缓存获得局部多尺度算子
  → 局部刚度作用
  → scatter-add 到全局向量
```

重点比较三种内存-算力策略：

- 保存多尺度形函数；
- 只保存缩聚刚度；
- 两者均不保存、按需预测和计算。

### 方向 C：面向 Matrix-Free 的多层预条件

构造“精确算子不组装、低阶预条件器可组装”的混合框架。研究预条件器更新频率与拓扑迭代之间的关系，判断能否跨多个优化步复用粗空间和预条件层次。

### 方向 D：结构保持与误差可控的 PIML

将刚体模态、对称正定性和能量一致性作为硬约束或网络参数化的一部分；建立局部误差指示器，在高风险子结构上自动回退到精确消元。

### 方向 E：GPU/异构并行实现

以子结构批处理为基本计算单元，优先实现：

1. PIML 批量推理；
2. 局部缩聚算子或 MatVec；
3. 细网格位移恢复；
4. 灵敏度与 PDE 滤波；
5. GPU-aware MPI 下的多节点扩展。

### 方向 F：PIML 与 MMC/MMV 的协同

MMC/MMV 的设计变量维度较低，可缓解密度法中设计更新和过滤逐渐成为瓶颈的问题。可以研究：

- PIML 加速 MMC/MMV 固定背景网格上的结构分析；
- 对显式边界切割单元采用精确局部算子，对内部规则子结构采用 PIML；
- Matrix-Free 求解器与 MMC/MMV 几何更新解耦；
- 复杂边界处采用等参单元、XFEM/VEM 或高阶局部修正。

---

## 十、建议的阶段性技术路线

### 阶段 1：基准复现与概念验证

- 复现 2022 EMsFEM-PIML 和 2023 子结构 PIML 的核心流程；
- 建立组装式 FEM、子结构法和 PIML 的统一接口；
- 验证局部刚度、位移、柔顺度与灵敏度误差；
- 建立逐模块性能计时和峰值内存测试。

### 阶段 2：全局 Matrix-Free 与预条件

- 实现子结构级 Matrix-Free MatVec；
- 接入 CG/GMRES 与几何多重网格；
- 比较全组装、部分 Matrix-Free 和完全 Matrix-Free；
- 研究低阶代理预条件与跨优化步复用。

### 阶段 3：GPU 与多节点扩展

- 批量化 PIML 推理和局部算子；
- 实现 GPU 上的过滤、灵敏度和设计变量更新；
- 开展单 GPU、多 GPU 和多节点强/弱扩展测试；
- 分析算力、显存带宽和通信的 Roofline/性能上限。

### 阶段 4：复杂几何与工程平台集成

- 处理非规则设计域和边界子结构；
- 与 MMC/MMV、SiPESC.FEMS、SiPESC.TOPO 或 DLUTopt 流程衔接；
- 建立航空航天和装备结构典型算例；
- 形成可复用求解器模块、benchmark 和论文成果。

---

## 十一、建议的实验矩阵

| 维度 | 建议设置 |
|---|---|
| 问题规模 | $10^6$、$10^7$、$10^8$、$10^9$ 设计变量 |
| 子结构尺度 | $m=4,5,8,10$ |
| 算子模式 | 全组装、缓存局部算子、完全按需 Matrix-Free |
| 求解器 | CG、GMRES、MG-CG、MG-GMRES |
| 预条件器 | Jacobi、块 Jacobi、Schwarz、几何 MG、低阶组装代理 |
| 硬件 | 多核 CPU、单 GPU、多 GPU、CPU+GPU 多节点 |
| 精度指标 | 位移、柔顺度、能量范数、灵敏度、最终拓扑一致性 |
| 性能指标 | 每步时间、总时间、峰值内存、MatVec 吞吐、通信占比、强/弱扩展 |

建议将“与全尺度精确分析的误差”与“相对组装式方法的加速比”绘制成 Pareto 曲线，而不是只报告单一最佳加速结果。

---

## 十二、结论

郭旭老师团队已经形成了从 PIML 局部力学算子学习、三维子结构降维、复杂设计域和 data-free 训练，到分布式并行、多重网格与 Matrix-Free 存储优化的连续研究链条。其最重要的方法论贡献是把机器学习定位为有限元局部算子构造工具，而不是直接替代完整拓扑优化过程。

对本博士后研究而言，最具辨识度的切入点不是重复已有的 PIML 并行框架，而是进一步完成：

> **结构保持的 PIML 局部算子 + 真正的全局 Matrix-Free 作用 + 可扩展多层预条件 + GPU/异构并行 + 完整拓扑优化流程性能协同。**

该方向既能承接团队现有成果，又能发挥计算数学、有限元离散、迭代求解与科学计算软件实现方面的优势，并可自然扩展到 MMC/MMV 显式拓扑优化和国产 CAE 软件平台。

---

## 参考文献与资料

1. Huang M, Du Z, Liu C, et al. *Problem-independent machine learning (PIML)-based topology optimization—A universal approach*. Extreme Mechanics Letters, 2022, 56:101887. [DOI](https://doi.org/10.1016/j.eml.2022.101887). 仓库笔记：[[../literature/topology-opt/Huang2022-PIML-universal]]
2. Huang M, Cui T, Liu C, et al. *A Problem-Independent Machine Learning (PIML) enhanced substructure-based approach for large-scale structural analysis and topology optimization of linear elastic structures*. Extreme Mechanics Letters, 2023, 63:102041. [DOI](https://doi.org/10.1016/j.eml.2023.102041).
3. Zhang L, Huang M, Liu C, et al. *Problem-Independent Machine Learning-enhanced structural topology optimization of complex design domains based on isoparametric elements*. Extreme Mechanics Letters, 2024, 72:102237. [DOI](https://doi.org/10.1016/j.eml.2024.102237).
4. Huang M, Liu C, Guo Y, et al. *A mechanics-based data-free Problem Independent Machine Learning (PIML) model for large-scale structural analysis and design optimization*. Journal of the Mechanics and Physics of Solids, 2024, 193:105893. [DOI](https://doi.org/10.1016/j.jmps.2024.105893).
5. Ma X, Huang M, Du Z, et al. *A high-performance parallel algorithm based on problem independent machine learning (PIML) for large-scale topology optimization*. Acta Mechanica Sinica, 2026, 42. [DOI](https://doi.org/10.1007/s10409-025-25942-x). 仓库笔记：[[../literature/topology-opt/Ma2026-PIML-parallel]]
6. 用户提供：*郭旭老师团队在大规模结构拓扑优化中 PIML 与 Matrix-Free 高性能求解的研究报告*，2026-06。

## 关联文档

- [[postdoc-research-plan]] — 博士后科研计划
- [[guo-xu-team-overview]] — 郭旭院士团队研究体系
- [[mmc-mmv-numerical-discretization-survey]] — 第二个研究计划题目的技术调研
- [[../literature/topology-opt/Huang2022-PIML-universal]] — 2022 PIML 奠基论文笔记
- [[../literature/topology-opt/Ma2026-PIML-parallel]] — 2026 并行 PIML 论文笔记
