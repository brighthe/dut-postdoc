---
title: "Matrix-Free 全局算子与迭代求解技术线研究指南"
topic: "Matrix-Free 技术线的已有能力、目标差距、实施路线与阶段完成边界"
tags:
  - technical-line
  - research-guide
  - matrix-free
  - Krylov
  - preconditioning
  - finite-element
  - mpi
  - heterogeneous-computing
status: "in-progress"
date_start: 2026-07-21
date_update: 2026-07-29
related:
  - linear-elasticity
  - matrix-free/assembly-levels
  - matrix-free/distributed-operator-and-shared-dofs
  - piml-matrix-free-gpu-and-model-selection-technical-synthesis
---

# Matrix-Free 全局算子与迭代求解技术线研究指南

> **定位**：本页是 Matrix-Free 技术线的长期第一入口，集中回答“目前已经具备什么能力、距离最终目标还有什么差距、下一步如何推进以及何时可以标记完成”。三维线弹性的连续模型、弱形式和有限元离散见 [[../../concepts/linear-elasticity]]；Matrix-Free 的数学定义、五级装配层次和第三方框架术语见 [[../../concepts/matrix-free/assembly-levels]]；MPI 单元分区、共享自由度、同步归约和加权内积见 [[../../concepts/matrix-free/distributed-operator-and-shared-dofs]]。
>
> **当前主要研究对象**：以三维线弹性方程作为首个统一参考问题，建立 FA/LA/EA/PA/UA、Krylov、预条件以及 CPU/GPU/MPI 的正确性与性能基线；本页维护参考问题、阶段门禁和研究状态，SOPTX 示例维护程序实现、运行方法和验证证据，Maxwell/PML 现阶段仅作为已有 EA/EbE 分布式实现的工程参考。
>
> **当前事实底线**：已经形成积分点 contraction 原型、`mfleo` 的 MFEM PA 工程路径和 `xihe/matrix_free_3` 的 Maxwell EA/EbE 分布式原型；SOPTX 三维线弹性 EA/FA、对等重叠副本 MPI 与无预条件加权 CG 已完成阶段 1 数值门禁，当前优先工作进入分布式接口提取、LA 与预条件基线。

## 一、技术线目标与边界

最终目标是形成统一的有限元算子与迭代求解框架：给定 $\mathbf x$，能够按选定装配层级可靠地计算 $\mathbf y=\mathbf K\mathbf x$，并在可扩展预条件器支持下完成 CPU、GPU 和 MPI 环境中的端到端求解。

当前阶段以三维线弹性方程求解为主线，首先统一线弹性 Matrix-Free 算子、Krylov 和预条件路径；在线弹性正确性、收敛性和性能验证闭环后，再用 Maxwell 等其他 PDE 检验框架的通用性。

| 维度 | 最终目标 |
|---|---|
| 装配与存储 | FA/TA、LA、EA/EbE、PA/QA、UA/NONE 可统一描述、切换和比较 |
| 软件接口 | `setup/update/apply/diagonal`、边界处理、自由度映射和诊断语义统一 |
| 实现路径 | Python 用于参考正确性和快速研究，C++ 用于高性能实现与软件集成 |
| 并行执行 | CPU、GPU、CPU MPI、GPU-aware MPI 使用一致的算子和验证口径 |
| 求解 | CG/MINRES/GMRES、真残差和可组合预条件器形成可靠闭环 |
| 验证 | 正确性、收敛性、内存、通信和完整 solve 使用统一 Benchmark |

“统一支持”不等于所有组合都从零实现，而是以统一契约连接已有框架、外部项目和共享测试。具体 PDE、材料模型、设计变量更新、单一硬件 kernel 优化及项目实时任务，由对应课题页或项目仓库维护。

### Ma2026 接续目标

以 Ma2026 的 PIML 子结构框架作为算法起点，把“多尺度形函数按需预测和释放、粗网格全局缩聚矩阵仍显式组装”的实现逐步推进为子结构算子级 Matrix-Free 求解框架。FA/TA 和 LA 用作显式参考、MPI 调试及预条件基础；EA/EbE、PA-like 与 UA/NONE 构成后续算子级 Matrix-Free 主线。

| 层级 | 在接续路线中的实现对象 | 定位 |
|---|---|---|
| FA/TA | 显式形成并组装全局缩聚矩阵 $\mathbf K_s$ | Ma2026 算法参考与黄金对照 |
| LA | 每个 MPI rank 保存进程局部稀疏矩阵，显式处理 owned/ghost DOF 与 halo exchange | 分布式显式基线和预条件基础，不作为核心 Matrix-Free 成果 |
| EA/EbE | 保存各子结构 $\mathbf K_s^j$，MatVec 执行 gather、局部作用和 scatter-add，不组装全局 $\mathbf K_s$ | 第一条子结构算子级 Matrix-Free 路线 |
| PA-like | 保存 $\mathbf N^j$、积分点数据或其他因子，通过 $(\mathbf N^j)^{\mathrm T}\mathbf K^j\mathbf N^j$ 的因子化过程完成作用，不形成完整 $\mathbf K_s^j$ | 只有核实实际保存对象后才能正式归类为 PA/QA |
| UA/NONE | 在 MatVec 中按需生成局部表示，不缓存完整 $\mathbf K_s^j$ 或等价积分点算子数据 | 严格无组装候选路线，需核实重计算边界 |

实施时先以精确 $\mathbf K_s^j$ 建立 FA/LA/EA 和 Krylov/预条件闭环，再研究 PA-like 与 UA/NONE；上述路径稳定后，才将局部算子来源替换为 PIML 预测的 $\widehat{\mathbf K}_s^j$。PIML 决定局部算子如何获得，装配层级决定全局 MatVec 如何保存和执行，两者必须分别判定。

## 二、当前已有基础

| 基础                   | 已经做到的内容                                                                                                                                                                                          | 当前边界                                                               |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| 当前积分点 contraction 原型 | 直接执行 $\mathbf B^T\mathbf D\mathbf B\mathbf x$，不形成全局 $\mathbf K$ 或完整单元 $\mathbf K_e$；MatVec 与显式矩阵乘相对误差达到 $10^{-15}$–$10^{-13}$；已跑通小规模 CG，最终残差约为 $10^{-11}$–$10^{-10}$；NumPy、PyTorch CPU、CUDA 结果一致 | 是否预存 $\mathbf D_e$ 尚未核实，因此只能确定不是 FA、LA 或 EA，不能在 PA 与 UA 之间强行归类     |
| `mfleo`              | 基于 MFEM Partial Assembly，以 C++ CPU/CUDA kernel 实现线弹性算子；已有 tet/hex、不同阶次、单 GPU + 单 CPU 核条件下的端到端 CG、对角线及 Jacobi/Chebyshev 等工程经验                                                                     | 属于 PA/QA 工程基础；尚未考虑多 GPU、多 CPU 核协同或 GPU-aware MPI，也不是当前科研原型和完整有限元平台 |
| `xihe/matrix_free_3` | 已形成 Python、FEALPy backend、MPI CPU 的 Maxwell/PML EA/EbE 原型；当前本地证据支持 FA/EA MatVec、边界与细网格 1/2-rank 结果一致 | 细网格无预条件 GMRES 未达到真残差门禁，仅作为分布式数据流辅助参考，不再承担阶段 1 完成判定 |
| `soptx/matrix_free_elasticity_3d` | 已形成单位立方体三维线弹性制造解、SOPTX 材料与积分器、FA 黄金对照、缓存单元刚度的 EA/EbE、对等重叠副本 MPI、加权 CG 与四组验证驱动 | 2026-07-28 数值门禁通过；当前仅覆盖 `p=1`、`float64`、1/2 ranks、简单二分区和无预条件 CG，不包含性能或扩展性证据 |
| 第三方能力                | MFEM 提供多级装配与 PA/UA 能力，PETSc 提供 Shell Matrix、Krylov 和预条件接口；其他框架映射见概念页                                                                                                                             | 属于可复用基础，不等于本技术线已经完成对应实现                                            |

公司仓库作为独立工程仓库和权威事实源维护。本知识库仅保留非敏感技术结论，不复制公司代码、运行日志、内部数据或客户算例，也不建立跨仓库运行依赖。

### 郭旭老师团队公开成果与本技术线衔接

截至 2026-07-26，当前公开且可核实的直接 Matrix-Free 相关节点只有 [[../../literature/topology-opt/Ma2026-highperformanceparallel]]。该工作通过 PIML 按需预测并释放多尺度形函数 $\mathbf N^j$ 降低内存，但仍形成子结构缩聚刚度并组装粗网格全局缩聚矩阵；按五级分类，其全局求解属于第 1 级 FA/TA，而不是算子级 EA、PA 或 UA。

这项成果为“以重计算换存储”及 PIML 子结构接入提供了直接基础。本技术线的接续任务是进一步打通不组装全局缩聚矩阵的 $y=\mathbf K_s x$、Krylov、预条件和 GPU/MPI 闭环；这是当前拟推进的研究方向，不能写成团队已经完成的公开成果。团队成果的长期演进和新增证据统一维护在 [[../../concepts/matrix-free/method-lineage]]。

## 三、当前成果边界

### 已完成

- 已证明积分点算子作用可以在不形成全局矩阵和完整单元矩阵的前提下达到机器精度一致，并进入小规模 CG 求解。
- 已具备 `mfleo` 的 PA、C++/CUDA、单 GPU + 单 CPU 核端到端 CG、Krylov 和基础预条件工程经验。
- 已具备 `xihe/matrix_free_3` 的 EA/EbE、MPI 分布式算子、Krylov 和预条件探索基础。
- SOPTX 三维线弹性阶段 1 已通过 $4^3/1$-rank、$8^3/1$-rank、$16^3/1$-rank 和 $16^3/2$-ranks 的 EA 主求解、单 rank FA 黄金参考、真残差、Dirichlet、显式解、收敛阶与跨 rank 一致性数值门禁；独立 FA 完整 CG 路径已明确验证 $4^3/1$-rank。

### 部分完成或待核实

- 当前 contraction 原型仍需核实 $\mathbf D_e$ 缓存策略，才能确定属于 PA 还是 UA。
- `xihe/matrix_free_3` 已有 Maxwell 分布式 MatVec 与 1/2-rank 一致性证据，但细网格 GMRES 未收敛；它不再阻塞线弹性主基线。
- 预条件能力分散在不同实现中，尚未形成统一的 operator level 与 preconditioner level 组合规范。
- 各实现的离散问题、自由度顺序、残差和计时边界尚未完全统一。
- `mfleo` 尚未考虑多 GPU、多 CPU 核协同或 GPU-aware MPI，不能将单 GPU + 单 CPU 核结果表述为 GPU/MPI 并行已经完成。
- SOPTX 阶段 1 尚未记录计时、加速比、并行效率、峰值内存或更多 ranks；当前结果只能作为 CPU MPI 正确性基线。

### 尚未完成

- 尚未形成连接 Python/C++、CPU/GPU、single/MPI 的统一 Matrix-Free 框架。
- 尚未完成 FA、LA、EA、PA、UA 在同一参考问题下的横向 Benchmark。
- 尚未形成统一的 GPU-aware MPI、自动验收和唯一状态账。
- 尚未把精确子结构 $K_s$ 和 PIML 预测的 $\widehat K_s$ 依次接入全局 Krylov 求解闭环。

## 四、目标与当前差距

| 能力维度 | 当前状态 | 下一道关键门槛 |
|---|---|---|
| 参考问题 | 三维线弹性制造解的 FA/EA、无预条件 CG、收敛阶和 1/2-rank 数值门禁已通过 | 冻结阶段 1 语义，提取可复用分布式算子接口并建立 LA/预条件基线 |
| 装配层级 | EA 与 PA/UA 分别已有基础 | 在同一问题上统一 FA、LA、EA、PA、UA 的语义和结果 |
| 算子协议 | 各项目接口独立 | 冻结 `setup/update/apply/diagonal`、边界和 owned/ghost DOF 语义 |
| 双语言 | Python 与 C++ 各有局部基础 | 使用共享黄金数据验证两种语言表示同一离散算子 |
| 并行与硬件 | SOPTX 已有 1/2-rank CPU MPI 正确性基线，`mfleo` 有单 GPU + 单 CPU 核经验，两条路径尚未融合 | 补齐 CPU MPI 性能口径，再完成多 GPU 及 GPU-aware MPI 的实现与一致性验证 |
| Krylov 与预条件 | SOPTX 无预条件加权 CG 已通过真残差门禁，其他实现已有 GMRES/MINRES 和若干基础预条件 | 建立分层预条件、真残差门禁、重建与复用策略 |
| Benchmark | 已冻结阶段 1 三维线弹性的正确性问题、门禁和结果；性能字段待实测 | 将同一契约扩展到 LA、预条件、内存、通信、更新、MatVec 和完整 solve |
| PIML 接口 | 尚未接入 | 先接入精确 $K_s$，验证后再替换为 $\widehat K_s$ 并分析误差传播 |

当前最优先的工作已进入阶段 2：以通过验证的 SOPTX 线弹性基线为准，提取 gather、EA/EbE 局部作用、scatter-add、共享 DOF 同步、加权内积、边界和 diagnostics 的可复用接口，并建立同一离散问题下的 LA 与预条件基线。Maxwell `xihe/matrix_free_3` 只保留为跨 PDE 辅助参考。

## 五、下一步实施路线

### 阶段 1：验证三维线弹性 EA/EbE + 重叠副本 MPI 主基线

**状态：2026-07-28 SOPTX 数值门禁已通过。**

- 参考问题取单位立方体、$\lambda=\mu=1$、`p=1` 三维四面体连续 Lagrange 向量元和全边界齐次 Dirichlet 制造解，数值精度为 `float64`；当前实现使用 SOPTX 的 `PolySolPureDirLagrange3d`、`IsotropicLinearElasticMaterial`、`LinearElasticIntegrator` 和 `SourceIntegrator`。
- EA 路径缓存完整单元刚度矩阵但不组装全局 CSR；三个单 rank EA 验证均构造 FA CSR，用于 MatVec、对称性和直接解黄金对照，但独立 `--operator-level fa` 完整 CG 路径当前只明确验证了 $4^3/1$-rank。MPI 单元按 $x=0.5$ 非重叠划分，共享位移 DOF 使用输入 `sync_add/refs`、输出 `sync_add` 的对等重叠副本表示。
- 用户本地依次运行 $4^3$、$8^3$、$16^3$ 的 1-rank 基线和 $16^3$ 的 2-rank 对照；无预条件 CG 固定 `maxit=1000`、`rtol=1e-10`、`atol=1e-12`。
- 完成门禁同时包括：CG 真残差、Dirichlet DOF、FA/EA 原始及边界 MatVec、CG/显式 FA 解、1/2-rank 全局解与 L2 误差一致性，以及网格加密 L2 误差下降和最低观测阶不低于 1.5。
- `stage1-validation.json` 给出 `passed=true`、`failures=[]`：最终观测阶约为 $1.67645$，$16^3$ 的 1/2-rank 解相对差约为 $2.34\times10^{-13}$，单 rank EA/FA 原始 MatVec 相对误差约为 $10^{-16}$。完整运行方法、门禁和精简数值快照见 `soptx:examples/matrix_free_elasticity_3d/README.md#2026-07-28-验证快照`。
- 本阶段完成仅表示当前正确性与收敛门禁闭合，不表示 CPU 并行效率、更多 ranks、预条件器、PA/UA、GPU 或 GPU-aware MPI 已完成。

### 阶段 2：提取 EA/EbE 分布式接口并建立 LA/预条件基线

- 以阶段 1 线弹性实现为主、Maxwell 原型为跨 PDE 对照，提取 gather、单元张量作用、scatter-add、共享自由度同步、边界处理、Krylov 和 diagnostics 的可复用接口语义。
- 在同一线弹性问题上建立 LA 显式 MPI 基线，明确对等重叠副本与后续 owned/ghost 表示的边界，并评估局部显式矩阵作为预条件器的用途。
- 冻结 operator level、preconditioner level、真残差、计时、内存和通信字段；SOPTX 维护个人实现，本知识库只维护理论与研究结论，不复制 `xihe` 公司代码、内部数据或运行依赖。

### 阶段 3：在线弹性基线上推进 PA/UA

- 在阶段 1 已冻结的离散问题、自由度顺序、边界、载荷和结果格式上实现 PA/QA，再研究 UA/NONE，避免更换 PDE 导致对照失效。
- 每完成一个装配层级，同时接入 Krylov 和至少一种可用预条件器，并与 FA、LA、EA 的 MatVec、能量、真残差、内存和完整 solve 对照。
- 对等重叠副本用于当前参考实现；面向更大 rank 数和外部框架对接时，再建立 owned/ghost 正式路径及双实现黄金对照。

### 阶段 4：对齐 `mfleo` PA 与单 GPU 路径

- 复用 MFEM/PETSc 和 `mfleo` 的工程路径，对齐 EA/PA、Python/C++、边界、残差、计时和输出语义。
- 使用共享黄金算例完成跨语言和 CPU/单 GPU 验证；当前只承认 `mfleo` 单 GPU + 单 CPU 核结果，不写成多 GPU、多核或 GPU-aware MPI 已完成。
- 建立 Jacobi、Chebyshev、Schwarz、多重网格和低阶组装代理等可组合预条件路径，并统一报告 setup、update、operator apply、preconditioner apply、通信、峰值内存和完整 solve。

### 阶段 5：接入子结构与 PIML

- 先用精确 $K_s$ 打通子结构级 Matrix-Free、Krylov 和预条件闭环，再换入 PIML 预测的 $\widehat K_s$，检查结构性质、全局误差、求解收敛和更新成本。
- 开展 GPU 批处理和端到端 profiling，不以单次 MatVec 加速替代完整 solve 结论。
- 在线弹性与单 GPU 路径闭环后，再扩展多 CPU 核、多 GPU 和 GPU-aware MPI。跨技术线推进顺序以 [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-gpu-and-model-selection-technical-synthesis]] 为准。

若纯 Matrix-Free 预条件不足以稳定收敛，允许使用低阶或低精度组装代理；目标是可靠高效求解，而不是追求预条件器形式上的“完全无矩阵”。

各阶段只有在具备可重放入口、明确事实来源并通过对应阶段门禁后，才能标记为“已完成”；缺少真残差、预条件、峰值内存或完整 solve 的结果只能作为局部证据。

## 六、事实来源与关联页面

- `xtu-phd-thesis:thesis/brightPhD.pdf#第三章` — 线弹性连续模型、变分形式和 Lagrange 有限元离散的原始论文事实源。
- `soptx:examples/matrix_free_elasticity_3d/README.md#理论代码对应` — 阶段 1 三维线弹性主基线的实现、运行入口和精简验证证据。
- `soptx:soptx/model/linear_elasticity_3d.py` — 三维线弹性制造解模型；材料与积分器由 SOPTX 对应软件模块维护。
- `xihe:examples/matrix_free_3` — Maxwell EA/EbE 分布式辅助原型；属于公司工程事实源，不作为本知识库运行依赖。
- `mfleo:README.md` — MFEM PA 与 CPU/CUDA 工程能力的公司仓库入口；不复制公司代码、数据或内部文档。
- [[../../concepts/linear-elasticity]] — 小变形静力线弹性的强形式、弱形式与有限元离散。
- [[../../concepts/matrix-free/assembly-levels]] — Matrix-Free 数学对象、五级装配层次和第三方框架映射。
- [[../../concepts/matrix-free/distributed-operator-and-shared-dofs]] — MPI 单元分区、共享自由度、输入同步、输出归约、加权内积与跨 rank 正确性不变量。
- [[../../concepts/matrix-free/method-lineage]] — 郭旭老师团队公开 Matrix-Free 相关成果的长期演进和事实边界。
- [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-gpu-and-model-selection-technical-synthesis]] — 当前 contraction、CG、多后端证据与跨线融合边界。
- [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-high-performance-solver-survey]] — Matrix-Free、预条件和开放问题的综合调研。
- [[../../work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] — 第一次线下汇报中的 Matrix-Free 摘要。
- [[archive/2026-postdoc-entry-assessment/README]] — 2026 年入站答辩时的历史表达与材料快照，不作为当前事实源。
- [[_index]] — 长期技术线总入口。
