---
title: "Matrix-Free 全局算子与迭代求解技术线研究指南"
topic: "全局无矩阵算子、Krylov、预条件和软件求解接口"
tags:
  - technical-line
  - research-guide
  - matrix-free
  - Krylov
  - preconditioning
  - finite-element
status: "in-progress"
date_start: 2026-07-21
date_update: 2026-07-21
related:
  - matrix-free-assembly-levels
  - piml-matrix-free-high-performance-solver-survey
  - piml-matrix-free-execution-plan
  - frame8_matrix_free_pipeline_guide
---

# Matrix-Free 全局算子与迭代求解技术线研究指南

> **定位**：本页是 Matrix-Free 技术线的长期第一入口，负责全局算子作用、Krylov 求解、预条件、算子更新和软件接口。它可服务 PIML、MMC/MMV、常规有限元及其他需要大规模状态方程求解的研究课题。
>
> **当前事实底线**：已经形成三类互补基础：积分点 contraction 的状态方程原型、`mfleo` 的 MFEM PA 工程路径、`xihe/matrix_free_3` 的 EA/EbE 分布式 Maxwell 原型；三者不是同一实现，尚未完成 PIML 子结构算子接入和一体化大规模求解。

## 一、技术线目标与边界

Matrix-Free 的目标是以“给定 $\mathbf x$，计算 $\mathbf y=\mathbf K\mathbf x$”的算子接口替代全局矩阵显式组装和存储，并在可扩展预条件器支持下完成可靠的迭代求解。

本技术线负责：

- 单元级、子结构级和混合层次的无矩阵算子作用；
- Dirichlet 边界、自由度映射、局部提取与 scatter-add；
- CG、MINRES、GMRES 等 Krylov 方法及停止准则；
- Jacobi、块 Jacobi、Schwarz、几何多重网格和低阶代理预条件；
- PETSc Shell Matrix 等软件接口、算子更新和跨优化步复用；
- 正确性、收敛性、内存和求解时间的统一基线。

本技术线不负责：

- PIML 模型的训练与结构保持，见 [[piml-research-guide]]；
- GPU 内核优化、多节点通信和硬件性能工程，见 [[gpu-hpc-research-guide]]；
- 某一应用方向的几何或设计变量更新方法。

## 二、数学对象与最小接口

常规有限元 Matrix-Free 作用可写为：

$$
\mathbf y
=
\sum_e
(\mathbf P_e)^T
\mathbf B_e^T
\mathbf D_e
\mathbf B_e
\mathbf P_e\mathbf x.
$$

子结构缩聚后的全局算子可写为：

$$
\mathbf y
=
\sum_j
(\mathbf A^j)^T
\mathbf K_s^j
\mathbf A^j\mathbf x,
$$

其中 $\mathbf K_s^j$ 可以来自精确缩聚、缓存或 PIML 预测。实现时必须把“局部算子来源”和“全局 Matrix-Free 作用”解耦。

### 2.1 五级装配层次

本技术线统一采用 [[../../concepts/matrix-free-assembly-levels]] 定义的五级存储分类：

| 层级 | 保存对象 | 本技术线口径 |
|---|---|---|
| FA/TA | 全局或 true-DOF 稀疏矩阵 | 显式参考基线，不属于 Matrix-Free |
| LA | MPI rank 局部稀疏矩阵 | 分布式矩阵路径，通常不属于 Matrix-Free |
| EA/EbE | 完整单元矩阵 $\mathbf K_e$ | 广义全局 Matrix-Free，但不是 PA |
| PA/QA | 积分点 $\mathbf D_e$ 或等价 PA 数据 | 现代高阶有限元的主流 Matrix-Free 路线 |
| UA/NONE | $\mathbf D_e$ 也在 apply 时按需计算 | 严格意义的 fully Matrix-Free |

PETSc `MatShell`、MFEM `Operator` 或自定义 `operator.apply()` 只规定算子接口，不自动决定其装配层级；分类必须继续检查内部实际保存的数据。

### 2.2 最小软件接口

最小软件接口：

- operator.apply(x, y)：执行局部提取、局部算子作用和全局回填；
- operator.diagonal()：提供 Jacobi 或诊断所需对角近似；
- operator.update(state)：密度、材料或状态变化后更新局部数据；
- preconditioner.apply(r, z)：与精确算子解耦的预条件接口；
- solver.solve(operator, rhs)：统一残差定义、停止准则和迭代记录；
- diagnostics：记录对称性、能量、残差、迭代数、时间和内存。

## 三、当前已有基础

### 3.1 当前科研原型

- 已在积分点直接执行 $\mathbf B^T\mathbf D\mathbf B\mathbf x$ contraction。
- 不形成全局 $\mathbf K$，也不预先形成单元 $\mathbf K_e$。
- Matrix-Free MatVec 与显式矩阵乘相对误差达到 $10^{-15}$–$10^{-13}$。
- 已跑通小规模 Matrix-Free CG 求解闭环。
- 最终残差约为 $10^{-11}$–$10^{-10}$。
- NumPy、PyTorch CPU、CUDA 三后端结果一致。

当前代码是否预存 $\mathbf D_e$ 尚未核实，因此只能确定它不属于 FA、LA 或 EA，不能在 PA 与 UA 之间强行归类。

### 3.2 `mfleo`：PA 工程基础

- `mfleo` 的 `develop` 分支基于 MFEM Partial Assembly 接口，以独立 C++ CPU/CUDA kernel 实现线弹性算子作用。
- 已覆盖 tet/hex、不同阶次、CPU/GPU、MPI、对角线以及 Jacobi/Chebyshev 等求解和预条件场景。
- 它是可接入 MFEM 求解流程的算子中间件，不是完整有限元平台，也不负责上层网格划分和全部预条件算法。

### 3.3 `xihe/matrix_free_3`：EA/EbE 应用基础

- `xihe` 的 `develop` 分支在 `examples/matrix_free_3` 中形成了分布式 Maxwell/PML Matrix-Free 原型。
- FEALPy integrator 的 `.const(pspace)` 形成并保留单元局部张量；MatVec 执行单元 gather、局部张量作用、scatter-add 和 MPI 共享自由度同步。
- 因为不组装全局稀疏矩阵但保存完整单元张量，该路径应归为 EA/EbE，而不是 PA。
- 已包含 MINRES/GMRES、真残差诊断和块 Jacobi/ILU 探索；人工真解、多进程一致性和预条件收敛仍有未闭合项，不能将“可运行”写成“全面验证完成”。

### 3.4 当前证据的准确读法

- 当前局部算子仍是常规有限元单元作用，不是 PIML 子结构 $\widehat K_s^j$。
- 当前科研原型证明算子实现和小规模状态方程正确；`mfleo` 提供 PA 工程与性能经验；`xihe` 提供 EA/EbE 电磁应用和分布式 Krylov 经验。三类证据不能互相替代。
- `xihe` 的大规模运行不等于人工真解、离散误差和 Krylov 收敛已经形成完整验证闭环。
- GPU 加速与显存数字属于 GPU/HPC 技术线的性能证据，本页只引用其对接口设计的约束。

## 四、核心研究问题

1. 精确或预测的 $\mathbf K_s^j$ 如何以统一数据布局进入全局算子？
2. 不显式组装矩阵时，怎样获得有效且可扩展的预条件器？
3. PIML 误差破坏对称性或正定性后，应选择 CG、MINRES、GMRES 还是回退精确算子？
4. 拓扑优化中算子每轮变化时，哪些局部数据和预条件层次可以增量更新或跨步复用？
5. FA/LA/EA/PA/UA 五级路线在存储、MatVec、更新和预条件成本上的 Pareto 边界在哪里？
6. 如何让 PETSc Shell Matrix、现有求解流程和后续软件模块共享同一算子协议？

## 五、后续工作包

### WP-M1：精确子结构算子基线

- 先使用精确 $\mathbf K_s^j$ 实现子结构级 Matrix-Free MatVec。
- 与显式缩聚全局矩阵乘逐项对照，固定算子时达到机器精度一致。
- 冻结边界自由度顺序、局部批次布局、边界条件和 scatter-add 语义。

### WP-M2：Krylov 与基础预条件

- 建立 none、Jacobi、block Jacobi 的残差、迭代数、时间和内存基线。
- 根据算子结构测试 CG、MINRES 与 GMRES，记录失效条件。
- 将对称性、最小特征值和残差历史纳入自动诊断。

### WP-M3：可扩展预条件

- 研究几何多重网格、块 Jacobi、加性 Schwarz 和低阶组装代理。
- 采用“精确算子不组装、低阶代理可组装”的混合框架作为稳健兜底。
- 研究预条件器跨优化步复用、低频重建和局部增量更新。

### WP-M4：PIML 算子接入

- 在精确基线稳定后，将局部 $\mathbf K_s^j$ 替换为 $\widehat{\mathbf K}_s^j$。
- 比较局部误差、谱扰动、迭代数、全局响应和回退比例。
- 将结构检查失败的子结构切换到精确消元，不让模型错误污染全局求解器。

### WP-M5：软件集成与规模验证

- 推进 PETSc Shell Matrix 算法层集成和求解器配置统一。
- 在代表性二维、三维和逐级放大算例上建立正确性、收敛和内存基线。
- 形成独立于具体应用方向的 operator/preconditioner/solver 模块。

## 六、Benchmark 与验收指标

| 指标组 | 核心指标 |
|---|---|
| 装配层级 | operator level、preconditioner level、实际保存对象和接口包装方式 |
| 算子正确性 | 与显式矩阵乘的相对误差、能量一致性、对称误差 |
| 求解正确性 | 最终真残差、相对残差、与直接解的位移误差 |
| 收敛性 | 迭代数、残差历史、停滞/发散、预条件后谱聚集 |
| 内存 | bytes/DoF、全局矩阵、单元/积分点数据、预条件器、工作向量和峰值内存 |
| 时间 | operator apply、preconditioner apply、向量运算、通信和完整 solve |
| 更新成本 | 密度变化后的算子更新、预条件重建和跨步复用成本 |
| 可扩展性 | 问题规模增长下的迭代退化、时间复杂度和内存复杂度 |

最低验收门槛：

- 精确局部算子下，Matrix-Free MatVec 与显式路径达到机器精度一致。
- 求解器报告真残差，不只使用递推残差。
- 任一性能结论必须同时报告迭代数、预条件成本和峰值内存。
- PIML 算子接入前后使用同一算例、停止准则和指标记录接口。

## 七、阶段性交付物

| 阶段 | 交付物 |
|---|---|
| 近期 | 精确 $K_s$ 子结构 MatVec、显式对照、基础 Krylov/预条件表 |
| 中期 | PETSc Shell Matrix 算法集成、多层或低阶代理预条件、复用策略 |
| 后期 | PIML 算子接入、误差—收敛报告、大规模可复用求解器模块 |

## 八、主要风险与回退

| 风险 | 回退策略 |
|---|---|
| Matrix-Free 下缺乏有效预条件器 | 组装低阶/低精度代理，采用混合预条件框架 |
| PIML 预测破坏 CG 条件 | 结构修正、精确回退或改用 MINRES/GMRES |
| 迭代数随规模或拓扑变化失控 | 引入多层预条件、粗空间和重建触发准则 |
| 每轮算子和预条件更新过贵 | 局部阈值更新、跨优化步复用和低频重建 |
| Shell Matrix 与现有算法接口不一致 | 先冻结最小 operator 协议，再适配 PETSc 和应用软件 |

## 九、跨技术线接口

- 从 PIML 接收精确或预测局部算子、结构检查结果和回退标记。
- 向 PIML 返回全局误差、残差、迭代数和谱信息。
- 向 GPU/HPC 提供可批处理的局部提取、局部作用、scatter-add 和 Krylov 原语。
- 从 GPU/HPC 接收端到端时间分解，判断保存、缓存或按需重算策略。
- 可为 PIML、MMC/MMV、常规有限元和其他 PDE 方向提供统一求解底座。

## 十、证据与关联文档

- [[../../concepts/matrix-free-assembly-levels]] — 五级装配层次、框架术语和当前项目分类准则。
- [[research/postdoc-plan/defense-sprint/direction-1-piml-matrix-free/frame8_matrix_free_pipeline_guide]] — 当前算子、CG 和多后端证据。
- [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-high-performance-solver-survey]] — Matrix-Free、预条件与开放问题调研。
- [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-execution-plan]] — 当前博士后计划中的工作包与里程碑。
- [[literature/topology-opt/Ma2026-highperformanceparallel]] — PIML、并行多重网格与存储策略参考。
- [[piml-research-guide]]、[[gpu-hpc-research-guide]] — 另外两条长期技术线。
- [[_index]] — 长期技术线总入口。
