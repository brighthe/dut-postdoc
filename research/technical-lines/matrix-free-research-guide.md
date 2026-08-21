---
title: "Matrix-Free 全局算子与迭代求解技术线研究指南"
topic: "Matrix-Free 技术线的研究目标、证据边界、阶段门禁与当前状态"
aliases:
  - "research/technical-lines/matrix-free-task-line"
  - "matrix-free-task-line"
  - "线弹性 Matrix-Free：内部研究任务线"
  - "discussions/guo-xu/first-formal-matrix-free-baseline-task"
  - "first-formal-matrix-free-baseline-task"
  - "discussions/guo-xu/first-formal-matrix-free-pa-qa-baseline-task"
  - "first-formal-matrix-free-pa-qa-baseline-task"
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
date_update: 2026-08-10
related:
  - linear-elasticity
  - matrix-free/_index
  - matrix-free/assembly-levels
  - distributed-operator-and-shared-dofs
  - ../piml-matrix-free-gpu/_index
  - ../piml-matrix-free-gpu/project-plan
  - piml-research-guide
---

# Matrix-Free 全局算子与迭代求解技术线研究指南

## 一、定位、事实所有权与研究目标

本页是 Matrix-Free 技术线的统一入口，博士后阶段优先服务 [[../piml-matrix-free-gpu/project-plan#三、工作包与依赖|核心项目 WP1]]（精确算子与基线），并为满足门禁后的 WP3 提供全局算子、Krylov 和预条件接口；长期能力仍可跨项目复用。

本页维护研究目标、路线、文献综合、结论边界、阶段门禁和当前任务状态。装配层级与分布式原理由 `concepts/matrix-free/` 维护；代码、命令、原始结果和正式 evidence 由 `soptx:examples/matrix_free_elasticity` 维护；项目级状态由 [[../piml-matrix-free-gpu/project-plan]] 维护。局部算子构建、结构保持与 PIML 预测见 [[piml-research-guide]]。

Matrix-Free 技术线的本质是提供**全局线性代数算子作用的抽象与迭代求解机制**。它通过自由度限制与回填，实现全局算子作用 $\mathbf{y} = \mathbf{A}\mathbf{x} = \sum_j \mathbf{G}_j^{\mathsf T} \mathbf{A}_j \mathbf{G}_j \mathbf{x}$，且对局部算子的来源保持数学通用性：既支持精确缩聚算子（$\mathbf{A}_j = \mathbf{K}_s^j$），也支持 PIML 预测的结构保持算子（$\mathbf{A}_j = \widehat{\mathbf{A}}_j$）。

| 维度 | 目标 |
|---|---|
| 算子 | 统一 `setup/update/apply/diagonal`、边界处理、自由度映射和诊断语义 |
| 求解 | CG/MINRES/GMRES、真残差和可组合预条件器（代理预条件器/多重网格）可靠闭环 |
| 执行 | Python 参考实现与 C++ 高性能实现对齐，覆盖 CPU、GPU、MPI 和 GPU-aware MPI |
| 评价 | 同时报正确性、收敛性、算子扰动、真残差、完整 solve 时间、峰值内存与通信 |

## 二、Matrix-Free 技术路线与装配边界

Matrix-Free 的判定依据是“省略什么、保存什么、重算什么”，不是论文或接口是否使用 `matrix-free` 字样。完整定义和第三方框架映射见 [[../../concepts/matrix-free/assembly-levels]]。

| 层级 | 保存与省略对象 | 本项目定位 |
|---|---|---|
| FA/TA | 显式形成并组装全局矩阵 | 黄金参考，不作为 Matrix-Free 成果 |
| LA | 每个 rank 保存进程局部稀疏矩阵 | MPI 显式基线和预条件基础 |
| EA/EbE | 保存单元或子结构矩阵，省略全局组装 | 第一条 Matrix-Free 精确基线 |
| PA/QA | 保存形函数、几何和积分点数据，按因子化过程作用 | 不形成完整单元矩阵的核心路线 |
| UA/NONE | MatVec 时按需生成局部表示，进一步减少缓存 | 在 PA/QA 正确性闭环后研究 |

必须明确区分**高阶积分点级 Partial Assembly (PA)** 与 **子结构/大单元级 PIML Matrix-Free**：前者按 Gauss 积分点和和分解（Sum Factorization）作用；后者以子结构或大单元为局部载体，按 $\mathbf{y}_j = \widehat{\mathbf{A}}_j \mathbf{x}_j$ 作用。PIML 学习的本质是局部力学表示，与 Matrix-Free 的局部算子按需累加在计算范式上具有天然契合性，从而避免了“先局部学习、再全局组装”的矛盾路径。

以 [[../../literature/topology-opt/notes/Ma2026-highperformanceparallel|Ma2026]] 为接续点时，先用精确子结构算子 $\mathbf{K}_s^j$ 建立 FA/LA/EA 与 Krylov/预条件闭环（WP1），再推进 PA-like 和 UA/NONE；只有这些路径通过门禁后，才在 WP3 以结构保持 PIML 预测算子 $\widehat{\mathbf{A}}_j$ 替换局部算子来源。PIML 决定局部算子如何获得，装配层级决定全局 MatVec 如何保存和执行，两者必须分别判定。

## 三、国内外研究现状、研究缺口与选题价值

### 3.1 范围与判定口径

以下现状按原文中的省略对象、保存对象和求解路径归类。主算子与预条件器分别判定；Matrix-Free 主算子配合低阶或低精度组装代理并不矛盾。尚未同时完成全文、Zotero 条目和 Citation Key 核验的论文，只采用出版社页面能够支持的事实，不形成全文级结论。

### 3.2 国外研究进展

Hughes、Levit 与 Winget 1983 年的 EBE 方法以省略全局系数矩阵为历史起点。[[../../literature/matrix-free/notes/Kronbichler2012-parallel-cell-operator|Kronbichler 与 Kormann 2012]] 的正式摘要进一步支持以 cell-wise quadrature 和 sum factorization 实现有限元算子，并采用 MPI、节点内线程与显式向量化，覆盖自适应网格及线性／非线性 PDE。该文译文与精读尚未完成，当前不能据此补写具体装配层级、算例、处理器规模或性能数字，也不能外推到 GPU、拓扑优化、PIML 或动态拓扑预条件更新。[Hughes DOI](https://doi.org/10.1016/0045-7825(83)90115-9)

全局矩阵缺失后，预条件成为完整求解的关键。Pazner 2020 年说明 Matrix-Free 主算子可以与低阶细化组装代理、几何多重网格和 Schwarz 预条件结合，但不能据此推断拓扑演化中的更新策略。[[../../literature/topology-opt/notes/Traff2023-GPU-topology-optimisation|Träff et al. 2023]] 的正式摘要报告 OpenMP 4.5 与 Futhark GPU 实现，在单 GPU 上完成 6550 万单元线性拓扑优化约 2 小时，并演示百万单元非线性问题；当前只据此确认 GPU 已进入完整三维拓扑优化流程，Matrix-Free 装配层级、具体硬件和求解器细节待译文与精读完成后核验。[Pazner DOI](https://doi.org/10.1137/19M1282052)

### 3.3 国内研究进展

刘耀儒、周维垣与杨强（Liu et al., 2007）建立了面向三维水工结构的分布式 EBE、Jacobi-PCG 和 MPI 数据交换路线；其方法保存单元刚度矩阵而不生成全局刚度矩阵，属于 EA/EbE。[DOI](https://doi.org/10.1016/j.finel.2006.12.007)

西北工业大学卞翔与方宗德（Bian & Fang, 2017）将 assembly-free deflated CG、OpenMP 和一致体素用于三维屈曲约束拓扑优化，说明省略刚度与 deflation 矩阵可以进入完整优化；规则体素、屈曲专用算法和 CPU 平台限制了结论迁移。[DOI](https://doi.org/10.1177/1687814017715422)

[[../../literature/topology-opt/notes/Zhou2025-efficientaccelerationstrategies|周丙臻、朱子贤与王晓平（Zhou et al., 2025）]]的正式摘要报告了面向三维拓扑优化的有限差分、仅在最粗网格组装矩阵的 fully Matrix-Free 技术、N-cycle MGCG 和渐进策略。当前仅建立笔记与译文骨架，全文技术细节、平台、适用性和性能归因须待逐节翻译与精读后再升级。

郭旭老师团队（Ma et al., 2026）将 PIML 子结构降维、CPU/MPI、多重网格和多尺度形函数按需预测／释放结合到十亿单元级拓扑优化，但全局粗尺度缩聚矩阵仍显式组装。因此该工作是本项目从局部智能计算走向全局算子级 Matrix-Free 的直接接续点，而不是已经完成的融合成果。

“国内研究”的归属仅依据论文公开机构、实施平台或资助信息，不依据姓名或期刊所在地推断。

### 3.4 研究缺口与选题价值

1. 拓扑迭代持续改变材料分布和谱性质，预条件器的复用、局部更新与重建仍缺少统一判据。
2. 高阶规则单元和规则体素上的结论不能直接覆盖低阶非结构网格、复杂边界和动态设计域。
3. 局部 kernel 优势可能被 setup、材料更新、预条件、归约、通信和粗网格成本抵消，需要完整 solve 和优化循环证据。
4. 现有代表工作分别覆盖 MPI EBE、单 GPU 拓扑优化或 CPU/MPI PIML，尚未形成多 GPU、GPU-aware MPI 与学习局部算子的统一闭环。
5. 学习算子会改变对称性、正定性、能量一致性和误差传播，局部误差对 Krylov 收敛、灵敏度及最终拓扑的影响仍待研究。

对 WP1，本技术线用于建立精确算子、Krylov、预条件及 CPU/GPU/MPI 的统一基线，明确性能来源和失败边界。对满足门禁后的 WP3，则先形成精确局部算子的全局求解闭环，再替换为结构保持预测算子，研究预条件耦合、误差传播、缓存—重算、分布外检测和精确回退，并以精度—时间—内存的端到端证据判断是否真正扩展可解规模。

## 四、证据锚点及结论边界

| 来源 | 核心方法与平台 | 可支持的结论 | 证据与外推边界 |
|---|---|---|---|
| Hughes et al. 1983 | EBE，省略全局系数矩阵 | EBE 是 Matrix-Free 历史起点 | 出版社摘要；不补写平台、预条件或性能数字 |
| 刘耀儒等（Liu et al. 2007） | EA/EbE、MPI、Jacobi-PCG、三维水工结构 | 国内已形成 EBE 与分布式 Krylov 路线 | 不支持 PA/UA、GPU 或拓扑优化 |
| [[../../literature/matrix-free/notes/Kronbichler2012-parallel-cell-operator\|Kronbichler & Kormann 2012]] | 摘要级：cell-wise quadrature、sum factorization、MPI、节点内线程与显式向量化 | 现代并行 cell-based Matrix-Free 框架的摘要级锚点 | 译文与精读待完成；不补写装配层级、算例、处理器规模或性能数字，不外推到 GPU、拓扑优化、PIML 或动态拓扑预条件更新 |
| 卞翔、方宗德（Bian & Fang 2017） | assembly-free、OpenMP、deflated CG、屈曲拓扑优化 | Matrix-Free 可进入完整拓扑优化 | 规则体素和专用算法；缓存细节待终审 |
| Pazner 2020 | Matrix-Free 主算子 + 低阶组装代理、GMG/Schwarz | 主算子与预条件器可采用不同装配层级 | 摘要级高阶椭圆问题；不证明拓扑更新策略 |
| [[../../literature/topology-opt/notes/Traff2023-GPU-topology-optimisation\|Träff et al. 2023]] | 三维线性／非线性拓扑优化；OpenMP/Futhark；单 GPU | 摘要支持单 GPU 千万级单元与完整优化流程 | Matrix-Free 装配层级、具体硬件、求解器和外推边界待译文精读 |
| [[../../literature/topology-opt/notes/Zhou2025-efficientaccelerationstrategies\|周丙臻、朱子贤与王晓平（Zhou et al. 2025）]] | 有限差分、最粗层组装、fully Matrix-Free、N-cycle MGCG 与渐进策略 | 国内近期 fully Matrix-Free + MGCG 三维拓扑优化路线 | 正式摘要／元数据级；译文与精读待完成，不补写平台、算例、稳定性或性能归因 |
| [[../../literature/topology-opt/notes/Ma2026-highperformanceparallel\|郭旭老师团队（Ma et al. 2026）]] | PIML、CPU/MPI、PETSc MG-GMRES；全局粗矩阵仍组装 | PIML 局部表示和重计算换存储基础 | 不属于全局算子级 Matrix-Free 或 GPU 融合；已入库 |

未建单篇笔记文献的 `to-ingest` 状态统一维护在 [[../../literature/_index#当前 ingest 队列]]，本表不建立第二套状态账。

结论遵循四条边界：MatVec 一致不替代完整 solve、真残差和解误差；少量 ranks 不支持扩展性结论；单个 kernel 加速不替代端到端时间与内存；外部框架具备某项能力不等于本技术线已经实现或验证。

## 五、权威事实来源

- `soptx:examples/matrix_free_elasticity/README.md` — 二维、三维实现、运行入口和文件职责。
- `soptx:examples/matrix_free_elasticity/results_analysis.md` — 实测数值、证据 provenance 和解释边界的唯一事实源。
- `soptx:examples/matrix_free_elasticity/math_spec.md` — 算子代数、重叠副本表示与门禁阈值的数学定义。
- [[../piml-matrix-free-gpu/project-plan]] — WP1–WP3、依赖关系和项目级状态。
- [[../../concepts/matrix-free/_index]] — Matrix-Free 稳定知识与语义入口。
- [[../../concepts/matrix-free/assembly-levels]] — 五级装配层次和框架术语映射。
- [[../../concepts/gpu-hpc/distributed-operator-and-shared-dofs]] — MPI 共享自由度、同步归约和正确性不变量。
- [[../../literature/_index#当前 ingest 队列]] — 当前待入库证据锚点和储备候选池。
- [[../piml-matrix-free-gpu/high-performance-solver-survey]] — Matrix-Free、PIML 与 GPU/HPC 的跨线问题综合。

`mfleo` 与 `xihe` 只作为独立工程能力来源；本知识库不复制公司代码、数据、日志或内部文档，也不建立跨仓库运行依赖。
