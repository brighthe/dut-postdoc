---
title: "帧 8：Matrix-Free 无矩阵高性能求解原型指南"
tags:
  - matrix-free
  - Frame-8
  - high-performance-computing
  - GPU
  - MPI
  - preconditioner
  - implementation-guide
status: "in-progress"
date: 2026-07-03
related:
  - frame7_piml_pipeline_guide
  - frame9_piml_matrix_free_pipeline_guide
  - postdoc-research-plan
---

# 帧 8：Matrix-Free 无矩阵高性能求解原型指南

本文档专门用于统筹与解答 PPT **帧 8（方向一 · Matrix-Free 无矩阵高性能求解原型）** 的所有底层逻辑。目标是：对照本 guide，可以解释帧 8 中出现的每一个术语、公式、数值结果、参考文献与答辩边界。

> 维护约定：本文档是帧 8 的主入口。原 `matrix_free_math_principles` 与 `soptx-matrix-free-integration-plan` 已删除，其有效内容并入本文档；后续不要再沿旧入口接续。若未来更新帧 8 数值，必须优先核对权威事实源，不凭记忆改数。

## 1. 帧 8 的答辩任务

帧 8 不是单纯解释 Matrix-Free 概念，而是回答评委可能连续追问的四个问题：

1. **为什么可以不组装全局刚度矩阵？**  
   因为 Krylov 求解只需要算子作用 $y=Kx$，不需要显式访问矩阵条目。
2. **不组装矩阵是否改变有限元离散模型？**  
   不改变。Matrix-Free 改变的是实现方式，不改变弱形式、离散空间、本构关系和边界条件。
3. **已有正确性证据到什么程度？**  
   已有 MatVec 等价、状态方程一致和三后端一致性验证，说明无矩阵链路已打通。
4. **高性能基础是否只停留在口号？**  
   不是。已有 GPU MatVec 趋势、GPU/MPI 端到端求解和 Jacobi/Chebyshev 预条件算子基础，可作为入站前能力证明。

帧 8 的一句话口径：

> Matrix-Free 不改变有限元离散模型，只把“组装并存储全局刚度矩阵”替换为“按需计算算子作用 $y=Kx$”，为大规模 Krylov 求解和 GPU/MPI 并行提供入口；这套快速算法底座后续可同时服务方向一 PIML 全局求解和方向二 MMC/MMV 高效结构分析。

帧 8 的定位：

- **不是**完整博士后方向一系统已完成的结果页。
- **是**入站前 Matrix-Free 能力证明页：正确性链路 + GPU 算子趋势 + GPU/MPI/预条件工程基础。
- **作用**是承接帧 7 的局部 PIML 算子，并为帧 9 的 PIML × Matrix-Free × GPU 融合路线提供全局求解基础；从长期软件架构看，它也是方向二 MMC/MMV 高效结构分析可复用的快速算法底座。

## 2. 当前 PPT 帧面结构与逐元素说明

### 2.1 整体结构

当前帧 8 采用左图右文结构：

- **顶部引导句**：说明 Matrix-Free 的定义和用途。
- **左侧「算子作用管道」**：展示 $x \to y=Kx$ 的无矩阵算子作用流程。
- **右侧「验证结果与并行/预条件基础」**：用四条证据说明正确性、求解闭环、GPU 趋势和并行/预条件基础。
- **底部关键点**：一句话强调“不形成/存储全局 $K$”。
- **底部参考文献**：Kronbichler 2012 + Brown 2010，支撑 Matrix-Free / 高阶算子求值的方法学来源。

### 2.2 帧面术语速查表

| PPT 词语 | 含义 | 答辩时怎么说 | 边界 |
|---|---|---|---|
| Matrix-Free | 无矩阵算子作用；不显式形成全局刚度矩阵，只在需要时计算 $y=Kx$ | “Matrix-Free 改变的是求解实现方式，不改变有限元离散模型。” | 不是完全没有刚度算子，也不是不求解线性方程 |
| 无矩阵 | 不组装/不存储全局矩阵 $K$ | “无矩阵指不持久化全局 $K$，但仍保留等价的力学算子作用。” | 局部几何/材料数据仍可能缓存 |
| 刚度矩阵 $K$ | 有限元离散后得到的全局线性算子 | “传统方法显式装配 $K$，Matrix-Free 只提供 $Kx$。” | 本页不改变 $K$ 对应的物理模型 |
| 算子作用 $y=Kx$ | 给定向量 $x$，返回刚度算子作用结果 $y$ | “Krylov 求解器只需要反复调用这个黑盒。” | 只说明单次作用，不等于完整优化闭环 |
| MatVec | Matrix-Vector multiplication，矩阵向量乘 | “MatVec 等价是最基础的正确性验证。” | MatVec 快不必然等于整体 solve 快 |
| Krylov | 一类迭代线性求解方法 | “CG/GMRES 都属于 Krylov 家族，它们只依赖 $Kx$。” | 收敛速度仍依赖条件数和预条件 |
| CG | 共轭梯度法，适合对称正定系统 | “线弹性刚度矩阵通常适合用 CG。” | 若预测算子破坏对称正定，可能需 GMRES/MINRES |
| 预条件 | 改善 Krylov 收敛的算子 | “Matrix-Free 解决存储和算子作用，预条件解决迭代次数。” | AMG/ILU 往往依赖显式矩阵，不一定适合当前口径 |
| GPU | 用于批量局部算子作用和向量操作的异构硬件 | “Matrix-Free 把访存压力转为更多局部计算，适合 GPU。” | 当前 PPT 第 ③ 条是 MatVec 加速，不是端到端 solve 加速 |
| MPI | Message Passing Interface，分布式并行通信接口 | “1-32 进程说明已有多进程并行工程经验。” | 第 ④ 条是前期 PA/Matrix-Free 算子基础，不是当前一体化系统 |
| PA | Partial Assembly，局部组装/部分组装 | “不组装全局矩阵，但可缓存积分点或局部几何量以减少重复计算。” | PA 不是传统全矩阵组装 |
| Jacobi / Chebyshev | Matrix-Free 兼容的基础预条件路线 | “它们不强依赖完整显式矩阵，适合作为入门预条件基础。” | 不是最终最强预条件器 |
| P2 tet | 二阶四面体单元 | “典型三维高阶单元，积分点多，适合展示 Matrix-Free/PA 价值。” | 属于前期工程基础，不是当前 PPT 原型的唯一单元 |
| DOF | Degrees of Freedom，自由度数量 | “自由度越大，显式矩阵存储越容易成为瓶颈。” | 不等同于设计变量数量 |

## 3. 左侧流程图逐节点解释

PPT 左侧展示的是一次 Matrix-Free 算子作用的标准流程：

```text
全局向量 x
  -> 单元自由度提取 x_e = A_e x
  -> 局部算子作用 y_e = K_e x_e
  -> 全局累加回填 y = sum_e A_e^T y_e
  -> Krylov / CG 状态方程 KU = F
```

逐框解释：

1. **全局向量 $\mathbf{x}$**  
   Krylov 迭代中传入的全局向量。它可以理解为当前迭代的搜索向量或试探向量。

2. **单元自由度提取 $\mathbf{x}_e=A_e\mathbf{x}$**  
   用提取算子 $A_e$ 从全局向量中取出单元 $e$ 对应的自由度。这一步也常被称为 **gather**。

3. **局部算子作用 $\mathbf{y}_e=K_e\mathbf{x}_e$**  
   对单元局部向量做刚度作用。PPT 为了简洁写成 $K_e x_e$，但真正高性能 Matrix-Free 中可以不显式形成 $K_e$，而是在积分点直接做 $B^TDBx_e$ 张量收缩。

4. **全局累加回填 $\mathbf{y}=\sum_e A_e^T\mathbf{y}_e$**  
   把每个单元的局部贡献回填到全局向量，这一步也常被称为 **scatter-add**。

5. **Krylov / CG 状态方程 $KU=F$**  
   外层求解器只需要反复调用 $x \mapsto y=Kx$，即可求解状态方程。Matrix-Free 提供的是这个黑盒算子接口。

浅蓝底框的含义：

- **局部算子作用**是 Matrix-Free 的核心计算步骤。
- **Krylov / CG 状态方程**是该算子进入全局求解器的接口。

## 4. 数学原理与公式符号解释

### 4.1 从组装式矩阵到无矩阵作用

传统有限元组装写作：

$$
K = \sum_e A_e^T K_e A_e,
$$

其中 $A_e$ 是从全局自由度到单元自由度的提取算子，$K_e$ 是单元刚度矩阵。对任意全局向量 $x$，矩阵向量乘法可改写为：

$$
y = Kx
  = \left(\sum_e A_e^T K_e A_e\right)x
  = \sum_e A_e^T\left(K_e(A_e x)\right).
$$

这说明：只要能对每个单元执行局部作用 $K_e x_e$，再把结果 scatter-add 回全局向量，就不必显式形成全局矩阵 $K$。

进一步地，真正高性能的 Matrix-Free 不一定形成局部 $K_e$。对于线弹性问题，可以直接按积分点执行：

$$
y_e = K_e x_e
    = \sum_q w_q \lvert J_q\rvert B_q^T D B_q x_e.
$$

### 4.2 公式符号逐项解释

| 符号 | 含义 | 在帧 8 中的角色 |
|---|---|---|
| $K$ | 全局刚度矩阵 / 全局线性算子 | 传统方法会显式组装；Matrix-Free 中只通过 $Kx$ 体现 |
| $x$ | Krylov 迭代传入的全局向量 | 算子作用的输入 |
| $y$ | $Kx$ 的结果向量 | 算子作用的输出 |
| $e$ | 单元编号 | 对所有单元累加局部贡献 |
| $A_e$ | 全局到单元自由度的提取算子 | gather：$x_e=A_ex$ |
| $A_e^T$ | 单元到全局的回填算子 | scatter-add：把 $y_e$ 回填到 $y$ |
| $K_e$ | 单元刚度矩阵 | PPT 中的简写；高性能实现中可不显式形成 |
| $x_e$ | 单元自由度向量 | 局部算子作用的输入 |
| $y_e$ | 单元局部贡献向量 | 局部算子作用的输出 |
| $B_q$ | 第 $q$ 个积分点的应变-位移矩阵 | 直接积分点作用的核心 |
| $D$ | 材料本构矩阵 | 线弹性材料刚度 |
| $w_q\,\lvert J_q\rvert$ | 积分权重与几何 Jacobian 行列式绝对值的乘积 | 数值积分系数 |
| $MF(x)$ | Matrix-Free 管道对 $x$ 的作用结果 | 用来和显式矩阵乘 $Kx$ 比较 |

答辩时解释公式可以压成一句：

> 传统方法先把所有 $A_e^TK_eA_e$ 装成全局 $K$，再乘 $x$；Matrix-Free 则把“乘 $K$”拆回每个单元局部作用再累加，因此数学等价但避免全局矩阵存储。

## 5. 右侧四条数值结果解释

### 5.1 总览表

| 条目 | PPT 数值 | 证明什么 | 边界 |
|---|---|---|---|
| ① MatVec 等价 | $10^{-15}$--$10^{-13}$ | 单次无矩阵算子作用与显式矩阵乘一致 | 只是单次算子正确性 |
| ② 状态方程一致 | 残差 $10^{-11}$--$10^{-10}$ | 整个求解过程与组装式路径一致 | 小规模闭环，不是大规模完整系统 |
| ③ GPU MatVec 加速 | 13.2 万 DOF，$11.9\times$；内存 $42.1\to4.0$ MB | 单卡 GPU 上算子级加速和省内存趋势 | 不是端到端 solve 加速 |
| ④ GPU/MPI + 预条件基础 | 650 万 DOF，1-32 进程，$3.72\times$--$12.74\times$；P2 tet CPU $1.20\times$--$1.21\times$，GPU 约 $4\times+$ | 已有并行/预条件算子工程基础 | 前期 PA/Matrix-Free 算子基础，可迁移但不等同当前一体化系统 |

### 5.2 ① MatVec 等价

PPT 写法：

> $\|{\rm MF}(x)-Kx\|/\|Kx\|:\;10^{-15}$--$10^{-13}$

解释：

- **MatVec** 是 Matrix-Vector multiplication，即矩阵向量乘。
- **MF(x)** 是 Matrix-Free 管道对同一个 $x$ 算出的结果。
- **Kx** 是显式组装全局矩阵后做矩阵向量乘得到的结果。
- 相对误差达到 $10^{-15}$--$10^{-13}$，说明二者在机器精度量级一致。

答辩口径：

> 这说明 Matrix-Free 不是换模型，也不是近似求解；在同一个有限元离散下，它和组装式矩阵乘法是机器精度等价的。

注意：① 只验证**单次算子作用**等价，还不是完整求解过程等价。完整求解过程等价由下一条“状态方程一致”承担。

### 5.3 ② 状态方程一致

PPT 写法：

> 小规模 CG 解 $\equiv$ 组装直解，残差 $10^{-11}$--$10^{-10}$

解释：

- MatVec 等价只验证单次 $Kx$。
- 状态方程一致说明这个 $Kx$ 黑盒已经能接入 CG，跑完整个 $KU=F$ 求解闭环。
- 这就是**整个求解过程等价**的证据：同一个问题用 Matrix-Free CG 求解，与组装式路径/组装直解得到一致位移解，并且残差达到 $10^{-11}$--$10^{-10}$。
- NumPy / PyTorch CPU / PyTorch CUDA 三档一致，说明后端切换没有破坏求解结果。

答辩口径：

> 第一条证明单次算子正确；第二条证明整个状态方程求解过程也能跑通并与组装式结果一致。因此帧 8 不是只有 MatVec 等价，也有小规模求解闭环等价。

### 5.4 ③ GPU MatVec 加速

PPT 写法：

> 13.2 万 DOF：$11.9\times$；内存估计 $42.1 \to 4.0$ MB

解释：

- 这是 **单次 MatVec 算子执行时间** 的加速，不是完整求解器总时间加速。
- 内存估计从 42.1 MB 到 4.0 MB，强调无矩阵路径减少矩阵存储需求。
- 这项结果说明算子作用适合 GPU 张量化/批量化。

答辩口径：

> 这里我只说 GPU MatVec 加速趋势，不把它夸大成端到端 solve 加速。端到端加速还需要预条件器和完整求解器进一步打磨。

### 5.5 ④ GPU/MPI + 预条件基础

PPT 写法：

> 650 万 DOF：1--32 进程，$3.72\times$--$12.74\times$；P2 tet：Jacobi/Cheb., CPU $1.20\times$--$1.21\times$；GPU 约 $4\times+$

本地验收报告中的关键数据：

1. **GPU hex，650 万 DOF**
   - order=2：相对全矩阵组装（FA）基线的端到端 CG 求解总时间约 $3.72\times$--$7.94\times$；
   - order=4：相对全矩阵组装（FA）基线的端到端 CG 求解总时间约 $4.63\times$--$12.74\times$；
   - 覆盖 `mpirun=1,2,4,8,16,32`。
2. **P2 tet，CPU 64 核**
   - Jacobi：约 $1.21\times$；
   - Chebyshev：约 $1.20\times$；
   - none：约 $1.18\times$。
3. **P2 tet，GPU + MPI**
   - Jacobi 多数配置约 $4\times+$，边界点 `mpi_tasks=32` 约 $3.89\times$；
   - Chebyshev 配置约 $4.34\times$--$5.51\times$；
   - none 配置约 $4.00\times$--$5.39\times$。

术语解释：

- **PA（Partial Assembly）**：不组装全局大矩阵，但可在积分点/局部层面缓存必要几何或材料信息，避免纯 Matrix-Free 的重复计算过高。
- **1-32 进程**：使用 MPI 同时调动 1 到 32 个计算进程进行分布式求解。
- **P2 tet**：二阶四面体单元，典型三维高阶单元。
- **Jacobi / Chebyshev**：Matrix-Free 兼容的基础预条件路线。

答辩口径：

> 第 ④ 条不是说当前博士后方向一系统已经完成 GPU/MPI 闭环，而是说明我在 PA / Matrix-Free 并行算子和预条件器方面已有实际工程基础，后续可以迁移到 PIML × Matrix-Free 全局原型中。

补充备注：

- 第 ④ 条和帧 8 的 Matrix-Free 主线是**同一套底层逻辑**：不组装全局大矩阵，以 PA / Matrix-Free 算子作用进入 Krylov/CG 求解，并结合 GPU/MPI 与预条件器提高效率。
- 当前 PPT 中第 ④ 条采用的是本人写的 `mfleo` 包的实测结果，用来证明这套工程能力已经真实跑通过；后续工作是把这套 PA / Matrix-Free / Krylov / 预条件工程能力整合到当前 soptx / PIML × Matrix-Free 全局原型中。

### 5.6 算例参数是否需要补充

帧 8 中第 ④ 条 GPU/MPI 结果的备查参数如下：

| 结果 | 算例 / 单元 | 参数 | 对比基线 | 口径 |
|---|---|---|---|---|
| GPU hex，650 万 DOF | `beam-hex`，六面体 | `order=2, refine=5, ndofs=6502275`；GPU；`mpirun=1/2/4/8/16/32`；CG 求解 | `MFEM PA` | `MFEM PA total_s / hex total_s = 3.72x--7.94x` |
| GPU hex，650 万 DOF | `beam-hex`，六面体 | `order=4, refine=4, ndofs=6502275`；GPU；`mpirun=1/2/4/8/16/32`；CG 求解 | `MFEM PA` | `MFEM PA total_s / hex total_s = 4.63x--12.74x` |
| P2 tet，CPU | `HT`，二阶四面体 | `P2/order=2, refine=0`；固定 `CG iters=300`；`mpi_tasks=64`；预条件 `jacobi/chebyshev/none` | `caststress` | `1.21x / 1.20x / 1.18x` |
| P2 tet，GPU | `HT`，二阶四面体 | `P2/order=2`；CUDA；`mpi_tasks=1/2/4/8/16/32`；预条件 `jacobi/chebyshev/none` | `caststress` | 多数配置 `4x+`；边界点 `jacobi, mpi_tasks=32` 约 `3.89x` |

#### 5.6.1 线弹性方程与材料参数备查

以下内容用于答辩追问时解释“第 ④ 条 GPU/MPI 性能结果到底求的是什么方程”。

`mfleo` 线弹性悬臂梁算例的物理模型可以按下面口径说明：

$$
-\nabla\cdot \boldsymbol{\sigma}(\mathbf{u})=\mathbf{0}\quad \text{in }\Omega,
$$

$$
\boldsymbol{\sigma}(\mathbf{u})
=2\mu\,\boldsymbol{\varepsilon}(\mathbf{u})
+\lambda\,\mathrm{tr}\!\left(\boldsymbol{\varepsilon}(\mathbf{u})\right)\mathbf{I},
\quad
\boldsymbol{\varepsilon}(\mathbf{u})
=\frac12\left(\nabla\mathbf{u}+(\nabla\mathbf{u})^T\right).
$$

弱形式上，对应的刚度算子可理解为

$$
a(\mathbf{u},\mathbf{v})
=\int_{\Omega}
\left[
2\mu\,\boldsymbol{\varepsilon}(\mathbf{u}):\boldsymbol{\varepsilon}(\mathbf{v})
+\lambda\,\mathrm{div}(\mathbf{u})\,\mathrm{div}(\mathbf{v})
\right]\,d\Omega.
$$

| 项 | guide 中可讲的口径 | 事实边界 |
|---|---|---|
| 求解变量 | 位移场 $\mathbf{u}$ | 三维线弹性问题，不是标量 Poisson 问题 |
| 本构关系 | 各向同性线弹性，Lamé 参数为 $\lambda,\mu$ | 用于解释 PA / Matrix-Free 局部算子如何从位移梯度得到应力 |
| 材料参数 | `mfleo` beam 示例与工具链默认记录为 `lambda=1.25, mu=1.0` | 若严格追问某一次性能表的运行参数，应以生成该结果的运行配置 / JSON 报告为准 |
| 几何参数 | beam 示例默认 `L=1.0, W=0.2` | 650 万 DOF 性能表的关键口径仍以 `order/refine/ndofs` 为主 |
| 固定位移边界 | 悬臂梁固定端为 $x=0$，$\mathbf{u}=0$ | 可解释为 essential / Dirichlet 边界；不同网格文件的边界属性编号以配置为准 |
| 受力边界 | 受力端施加恒定牵引 $\mathbf{t}$，其余边界为自然边界 | 当前 frame8 结果表不需要主动给出牵引数值；未在本页事实源中核实的载荷数值不要编造 |

答辩时如果被问“具体求的方程和材料参数是什么”，可以这样补充：

> 第 ④ 条 GPU/MPI 结果对应的是三维线弹性悬臂梁类算例，未知量是位移场。算子来自各向同性线弹性本构，$\sigma=2\mu\varepsilon+\lambda\mathrm{tr}(\varepsilon)I$，`mfleo` beam 示例默认 Lamé 参数为 `lambda=1.25, mu=1.0`。PPT 主帧没有展开这些参数，是因为这一页的重点不是做算例说明，而是证明 PA / Matrix-Free / Krylov / 预条件 / GPU-MPI 这条工程链路已经跑通。

答辩时若被追问参数，可以这样说：

> 第 ④ 条的详细参数不放在 PPT 主帧，是为了避免页面过密。备查口径是：六面体是 `beam-hex`，650 万自由度，order=2/4，GPU，1 到 32 个 MPI 进程；四面体是 `HT` 的 P2/order=2 算例，CPU 侧固定 64 进程和 300 次 CG 迭代，GPU 侧覆盖 1 到 32 个 MPI 进程，比较 Jacobi、Chebyshev 和无预条件三种配置。它们都服务于同一个结论：我已经有 PA / Matrix-Free / Krylov / 预条件 / GPU-MPI 的工程基础，后续会整合到 soptx 的 PIML × Matrix-Free 原型中。

## 6. 数值结果来源与事实边界

帧 8 的数值分为两类：

| 类型 | 作用 | 当前 PPT 口径 | 事实边界 |
|---|---|---|---|
| 当前无矩阵原型验证 | 证明入站前已经打通 Matrix-Free 状态方程链路 | MatVec 等价、状态方程一致、单卡 GPU MatVec 趋势 | 不等于完整 PIML × Matrix-Free 系统 |
| mfleo PA / Matrix-Free 并行算子原型 | 证明已有 GPU/MPI/预条件工程经验 | 650 万 DOF、1-32 进程、Jacobi/Chebyshev 预条件基础 | 是本人写的 mfleo 包实测结果；但不等同于 PIML × Matrix-Free 一体化系统 |

备查来源：

- `C:\workspace\dut-postdoc\ai\common\status.md`
- `C:\workspace\dut-postdoc\talks\2026-postdoc-entry-assessment\template-8min.tex`
- `C:\workspace\dut-postdoc\talks\2026-postdoc-entry-assessment\outline-8min.md`
- `C:\workspace\mfleo\docs\delivery\finalterm\tet_hex_pa_performance_acceptance_report.md`（第 ④ 条 GPU/MPI + 预条件基础的来源；mfleo 是本人写的 PA / Matrix-Free 并行算子包）
- `C:\workspace\mfleo\docs\delivery\2026_01_27_biweekly\2026_01_27_biweekly.md`（线弹性悬臂梁物理模型、边界条件口径）
- `C:\workspace\mfleo\examples\beam\beam_case_config.hpp` 与 `C:\workspace\mfleo\docs\test\runability_toolchain_user_manual.md`（beam 示例默认 `L/W/lambda/mu` 参数）

若未来继续刷新帧 8 数值，应优先核对：

- `C:\workspace\soptx_heliang\docs\frame8_matrix_free_pipeline_results.md`
- `C:\workspace\soptx_heliang\ai\common\progress-frame8_matrix_free.md`

原则：

- 不凭记忆改数。
- 不把 MatVec 加速说成端到端 solve 加速。
- 可以说明第 ④ 条来自本人写的 mfleo PA / Matrix-Free 并行算子原型；但不把它说成 PIML × Matrix-Free 一体化系统已完成。
- 不在 PPT 正文强调具体软件名，避免答辩重心偏移。

## 7. 参考文献口径

帧 8 底部参考文献保留两篇经典 Matrix-Free / 高阶算子求值文献：

> [1] M. Kronbichler, et al. A generic interface for parallel and fast PDE solvers based on high-order tensor product elements. *Computers & Mathematics with Applications*, 63(6):963-982, 2012.  
> [2] J. Brown. Efficient nonlinear solvers for nodal high-order finite elements in 3D. *Journal of Scientific Computing*, 45(1-3):48-63, 2010.

### 7.1 为什么帧 8 放这两篇

| 文献 | 支撑帧 8 的哪一部分 | 答辩口径 |
|---|---|---|
| Kronbichler et al. 2012 | 高阶有限元 Matrix-Free / tensor product / 并行 PDE solver 接口 | “左侧 gather-action-scatter 管道和高性能算子接口对标国际主流 Matrix-Free FEM 思路。” |
| Brown 2010 | 高阶节点有限元中不组装矩阵的高效非线性/迭代求解 | “说明高阶有限元不组装单元矩阵、直接算子求值是成熟的高性能求解路线。” |

### 7.2 为什么不在帧 8 加 Ma 2026

- Ma 2026 是帧 9 的主锚点，用来支撑 PIML × Matrix-Free × 并行的融合路线。
- 帧 8 更聚焦经典 Matrix-Free 算子作用本身，因此放 Kronbichler 2012 + Brown 2010 更干净。
- 若答辩中被问到与 Ma 2026 的关系，应转到帧 9 口径：Ma 2026 主要支撑 PIML 并行化与按需预测/释放策略，帧 8 负责说明我们自身的无矩阵算子基础。

## 8. 与帧 7 / 帧 9 的关系

- **帧 7（PIML）**：回答局部材料分布如何预测多尺度形函数/等效刚度。
- **帧 8（Matrix-Free）**：回答全局状态方程如何不组装矩阵地高效求解。
- **帧 9（融合路线）**：回答 PIML 输出如何直接进入 Matrix-Free / GPU / MPI 管线，并服务长期大规模结构分析目标。

三页合起来的逻辑是：

```text
局部材料分布
  -> PIML 预测多尺度形函数 / 等效刚度
  -> Matrix-Free 全局算子作用
  -> GPU/MPI Krylov 求解
  -> 长期支撑大规模复杂结构拓扑优化
```

## 9. 可直接使用的讲稿

### 9.1 35 秒版本

> 方向一的第二块是 Matrix-Free 高性能求解。Matrix-Free 不是换一个有限元模型，而是把组装和存储全局刚度矩阵，改成每次 Krylov 迭代中按需计算 $y=Kx$。左侧流程图就是这个算子作用管道：先从全局向量提取单元自由度，再做局部算子作用，最后累加回全局向量。右侧是基础验证：MatVec 与组装路径达到机器精度一致，小规模状态方程也能进入 CG 求解闭环；同时，单卡 GPU MatVec 在十万自由度规模有近 12 倍加速和明显内存压缩，前期还具备 GPU/MPI 和 Jacobi/Chebyshev 预条件算子基础。这说明我具备把无矩阵求解迁移到后续 PIML 多尺度全局原型中的基础。

### 9.2 15 秒版本

> 这一页说明 Matrix-Free 能力：不组装全局刚度矩阵，只提供 $y=Kx$ 算子作用。已有 MatVec 等价、状态方程一致、GPU MatVec 加速和 GPU/MPI/预条件工程基础，后续可接入帧 7 的 PIML 局部等效算子，也可作为方向二 MMC/MMV 高效分析的共用求解底座。

## 10. 可能追问与回答

**Q1：Matrix-Free 是不是近似方法？有没有整个求解过程等价？**

A：不是。Matrix-Free 改变的是实现方式，不改变有限元离散模型。MatVec 等价误差达到 $10^{-15}$--$10^{-13}$，说明单次算子作用和显式组装矩阵乘法在机器精度内一致；同时“状态方程一致”说明 Matrix-Free CG 已经跑完整个 $KU=F$ 求解闭环，小规模下与组装式路径/组装直解一致，残差约 $10^{-11}$--$10^{-10}$。

**Q2：为什么只展示 MatVec GPU 加速，不展示完整 solve 加速？**

A：当前原型更适合诚实展示算子级加速趋势。完整 solve 加速还取决于 Krylov 收敛和预条件器效果，因此不能把 MatVec 加速直接等同于端到端求解加速。

**Q3：预条件器为什么重要？**

A：Matrix-Free 解决的是 $Kx$ 怎么算、矩阵怎么不存；预条件器解决的是 Krylov 要迭代多少步。没有合适预条件，大规模问题可能仍然收敛慢。

**Q4：AMG / ILU 能不能直接用？**

A：AMG 和 ILU 往往依赖显式矩阵条目。在 Matrix-Free 框架下，更自然的路线是 Jacobi/Chebyshev、几何多重网格、p/h-multigrid 或结构保持预条件。

**Q5：第 ④ 条 GPU/MPI 数据是不是当前 PPT 原型跑的？**

A：可以强调它和帧 8 的 Matrix-Free 主线是**同一套底层逻辑**：PA / Matrix-Free 算子作用、Krylov/CG 求解、GPU/MPI 并行和预条件器。当前第 ④ 条采用的是我写的 `mfleo` 包的实测结果，用来证明这套工程能力已经跑通过；后续会把这套能力整合进 soptx 的 PIML × Matrix-Free 全局原型。需要区分的是，它和前面 ①-③ 的 soptx/Python 多后端无矩阵链路不是同一套代码路径，也不等同于 PIML × Matrix-Free 一体化系统已经完成。

**Q6：这页和帧 9 的区别是什么？**

A：帧 8 证明 Matrix-Free 本身的能力：如何不组装矩阵地求解状态方程。帧 9 进一步说明如何把帧 7 的 PIML 局部等效刚度喂给帧 8 的 Matrix-Free 全局算子。

## 11. 后续补数方式

帧 8 当前可以作为答辩页使用；后续若要进一步增强证据，可按以下优先级补充：

| 优先级 | 补充项 | 放入帧 8 的方式 |
|---|---|---|
| 高 | 当前原型端到端 CG 求解时间 | 替换“状态方程一致”中的残差占位，增加时间/迭代数 |
| 高 | 当前原型 GPU 端到端 solve 加速 | 替换“GPU MatVec 加速”为“GPU solve 加速” |
| 中 | Jacobi 预条件在当前原型中的迭代下降 | 在第 4 条中补“迭代数下降/残差下降” |
| 中 | 多规模曲线 | 帧 8 若空间不足，转入备份页或讲稿 |
| 低 | 详细 MPI scaling 曲线 | 更适合放入后续工作或备份页，不必压入 8 分钟主线 |

## 12. 关联文档

- [[frame7_piml_pipeline_guide]] — 帧 7：PIML 增强多尺度前向分析原型指南
- [[frame9_piml_matrix_free_pipeline_guide]] — 帧 9：PIML 与 Matrix-Free 融合路线与愿景
- [[piml-matrix-free-execution-plan]] — 方向一长期执行计划
- [[postdoc-research-plan]] — 博士后科研计划总领
