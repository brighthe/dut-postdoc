---
title: A problem-independent machine learning (PIML) enhanced substructure-based approach for large-scale structural analysis and topology optimization of linear elastic structures
authors:
  - Huang, Mengcheng
  - Cui, Tianchen
  - Liu, Chang
  - Du, Zongliang
  - Zhang, Jiameng
  - He, Chuhui
  - Guo, Xu
year: 2023
journal: "Extreme Mechanics Letters"
volume: 63
pages: 102041
doi: "10.1016/j.eml.2023.102041"
zotero_key: 5XMDKI6A
zotero_citation_key: huangProblemindependentMachineLearning2023
tags:
  - PIML
  - substructure
  - topology-opt
  - multiscale-FEM
  - large-scale
status: read
rating: 5
date_added: 2026-05-04
date_read: 2026-07-02
---

# A problem-independent machine learning (PIML) enhanced substructure-based approach for large-scale structural analysis and topology optimization of linear elastic structures

> **引用**：Huang, Mengcheng; Cui, Tianchen; Liu, Chang; Du, Zongliang; Zhang, Jiameng; He, Chuhui; Guo, Xu. *Extreme Mechanics Letters*, 2023, 63:102041. [DOI](https://doi.org/10.1016/j.eml.2023.102041) | [Zotero Link](zotero://select/library/items/5XMDKI6A)
> **完整中文译文**：[[translations/Huang2023-PIML-substructure-zh]]
> **Zotero/Better BibTeX key**：`huangProblemindependentMachineLearning2023`
## 一句话概括

本文把 PIML 从 2022 年的 EMsFEM 粗单元形函数预测推进到**经典子结构静力缩聚框架**：以子结构内部材料分布为输入，离线训练神经网络预测子结构形函数和/或缩聚刚度矩阵，从而把全尺度线弹性分析压缩到边界/粗尺度自由度上，并在十亿级设计变量问题上展示了工作站可解的潜力。

## 研究问题

大规模线弹性结构分析和高分辨率拓扑优化都需要反复求解大规模线性方程组。传统全尺度 FEM 的自由度数量与细网格规模同阶，随着设计分辨率提高，有限元分析成为时间和内存瓶颈。

已有机器学习加速方法的问题在于：

1. 很多端到端模型依赖特定几何、载荷、边界条件或优化问题，泛化性不足；
2. 为训练模型需要预先求解大量边值问题或优化问题，样本生成成本高；
3. 如果只学习全局响应，模型维度会随问题规模变化，难以真正用于超大规模结构。

本文目标是用子结构法把学习对象局部化：模型只学习“局部材料分布 -> 子结构形函数/缩聚刚度矩阵”的映射，因此与整体结构几何、边界条件、外载荷无关。

## 方法

### 子结构静力缩聚

对每个子结构 $j$，将自由度分为边界自由度 $b$ 和内部自由度 $i$。局部刚度矩阵写作

$$
\boldsymbol K_h^j =
\begin{bmatrix}
\boldsymbol K_{bb}^j & \boldsymbol K_{bi}^j \\
\boldsymbol K_{ib}^j & \boldsymbol K_{ii}^j
\end{bmatrix}.
$$

在内部自由度无外载的静力缩聚假设下，

$$
\boldsymbol u_i^j = -(\boldsymbol K_{ii}^j)^{-1}\boldsymbol K_{ib}^j \boldsymbol u_b^j,
$$

因此可定义子结构形函数

$$
\boldsymbol N^j =
\begin{bmatrix}
\boldsymbol I \\
-(\boldsymbol K_{ii}^j)^{-1}\boldsymbol K_{ib}^j
\end{bmatrix}
\quad
\text{或按内部/边界排序写为}
\quad
\begin{bmatrix}
-(\boldsymbol K_{ii}^j)^{-1}\boldsymbol K_{ib}^j\\
\boldsymbol I
\end{bmatrix}.
$$

对应缩聚刚度为

$$
\widetilde{\boldsymbol K}_h^j
=
(\boldsymbol N^j)^T \boldsymbol K_h^j \boldsymbol N^j
=
\boldsymbol K_{bb}^j
-
\boldsymbol K_{bi}^j(\boldsymbol K_{ii}^j)^{-1}\boldsymbol K_{ib}^j.
$$

这一推导说明，PIML 在本文中的作用不是直接学习全局位移解或最终拓扑，而是近似局部静力缩聚中反复出现的 $\boldsymbol N^j$ 或 $\widetilde{\boldsymbol K}_h^j$。

### PIML 学习对象

本文建立局部映射：

```text
子结构内部材料参数 / 密度分布
  -> 子结构形函数 N^j
  -> 缩聚刚度 K_s^j = (N^j)^T K^j N^j
```

与端到端拓扑优化网络不同，这个映射只由子结构离散、单元类型、本构方程和局部材料分布决定，不依赖整体边界条件、载荷和设计域形状。因此训练完成后，可用于同类 PDE 的不同结构分析和拓扑优化问题。

### 力学约束与输出降维

论文强调，平移和转动等刚体运动应由子结构形函数精确再现。通过把这类几何/力学约束显式嵌入输出表达，可以减少网络需要预测的自由参数，并提高鲁棒性。

三维算例中，子结构边界位移由边界节点或进一步降维后的线性边界变形描述。对 $m=5$ 的三维子结构，论文使用多组前馈神经网络分块预测约束后的形函数分量；每个网络 15 个隐层，激活函数交替采用 `tanh` 与 `elu`，并用 400,000 个随机材料分布样本训练。

### 缩聚刚度的两种获得方式

论文中存在两个层级：

1. **预测形函数，再计算缩聚刚度**：先由网络得到 $\boldsymbol N^j$，再用 $(\boldsymbol N^j)^T\boldsymbol K^j\boldsymbol N^j$ 计算 $\widetilde{\boldsymbol K}_h^j$。优点是形函数与位移恢复一致。
2. **直接预测缩聚刚度**：在柔顺机构等算例中，为进一步提高效率，直接预测缩聚刚度矩阵。

从论文方法本身看，这两条路线对应精度与效率的权衡：由形函数计算缩聚刚度更容易保持位移恢复和能量一致性；直接预测缩聚刚度则更强调在线效率。

## 实验 / 数值验证

### 大规模结构分析与拓扑优化

论文报告的核心结论是：相对传统全尺度分析，所提子结构 PIML 方法在测试的大规模算例中可达到 $10^4$ 到 $10^5$ 量级的求解效率提升，同时保持可接受精度。

典型算例包括：

- 三维 MBB 梁；
- 三维柔顺机构设计；
- 十亿级细网格短悬臂梁。

其中，短悬臂梁算例约含 $1.024\times10^9$ 个细分辨率单元、约 $3\times10^9$ 个自由度，论文展示其可在笔记本/工作站环境下完成，不依赖并行计算。

### 精度与效率边界

柔顺机构算例中，论文比较了 EMsFEM 与 PIML 预测缩聚刚度得到的输出位移，两个优化结果的输出位移相对误差约为 7.56% 和 7.65%。这说明本文 2023 子结构 PIML 的展示重点不是“局部算子误差达到 $10^{-3}$”，而是“子结构降维 + 神经网络快速获得缩聚算子”带来的大规模可解性。

需要特别注意的是，直接预测缩聚刚度矩阵时，预测的子结构形函数与预测的缩聚刚度矩阵未必严格满足式 (17) 所要求的能量一致关系；这是论文自己指出的一个精度风险，也是后续方法需要改进的地方。

阅读时要特别注意：不宜把 Huang 2023 直接概括为“局部算子预测误差达到 $10^{-3}$”的证据；本文更直接支撑的是**子结构框架、问题无关性、降维效率和十亿级规模**。

## 主要结论

1. 子结构法提供了天然的局部问题无关学习对象：材料分布决定局部缩聚算子，整体几何、载荷和边界条件只在全局粗尺度方程中出现。
2. PIML 使经典子结构法重新具备在线高效性：原本需要重复求解的局部静力缩聚可由神经网络快速预测。
3. 所提方法可用于线弹性结构分析和拓扑优化，并可扩展到柔顺机构这类非自伴随拓扑优化问题。
4. 大规模算例表明，该方法能显著降低结构分析时间，使十亿级设计变量问题具备工作站求解可能。

## 优点与局限

**优点：**

- 与整体边界条件、载荷和结构形状解耦，问题无关性比端到端 ML 更强。
- 与经典子结构法兼容，数学解释清楚。
- 可以同时支持粗尺度求解、细尺度位移恢复和拓扑优化灵敏度计算。
- 为 Ma 2026 的并行 PIML 与按需预测/释放策略提供了前置方法基础。

**局限：**

- 网络与子结构类型、细分尺度 $m$、单元类型和本构关系绑定，改变这些设置通常需要重新训练。
- 论文中为进一步降维使用了边界变形假设，可能带来系统性刚度误差。
- 2023 版本仍以获得局部缩聚算子并组装/求解全局缩聚系统为主，尚未系统讨论全局矩阵存储与组装成本。
- 极大规模展示重在可解性和效率，局部预测误差的细粒度统计需要结合原图表或后续复现实验进一步量化。

## 对我研究的启发

- **与 Huang 2022 的关系**：Huang 2022 可概括为 PIML 增强 EMsFEM 形函数构造；Huang 2023 则进一步转向 PIML 增强子结构形函数与缩聚刚度矩阵构造。二者都强调局部材料分布到局部力学表示的映射，但学习对象和全局求解框架不同。
- **与多分辨率拓扑优化的关系**：本文和 MTOP 都体现了“高分辨率材料描述不必与全局位移自由度一一绑定”的思想；区别在于 MTOP 依靠设计网格、密度积分网格和位移网格解耦，而 Huang 2023 依靠子结构内部自由度消元和边界缩聚。
- **理论限定**：PIML 的问题无关性应理解为“同类 PDE、相同离散和本构设置下，局部材料分布唯一决定子结构形函数/缩聚刚度矩阵”，不能误解为跨物理、跨单元类型的无条件泛化。
- **后续研究问题**：直接预测缩聚刚度虽然效率更高，但可能破坏形函数与刚度之间的能量一致关系；如何在保持效率的同时嵌入更强的力学一致性约束，是值得继续关注的方向。

## 相关文献

- [[Huang2022-problemindependentmachine]] — PIML 奠基论文，EMsFEM 角节点形函数预测。
- [[Ma2026-highperformanceparallel]] — 进一步把子结构 PIML、并行计算和按需预测/释放结合起来。
