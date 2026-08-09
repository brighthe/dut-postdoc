---
title: "GPU/HPC 异构并行与端到端性能技术线研究指南"
topic: "GPU/HPC 技术线的研究目标、性能边界、证据锚点、阶段门禁与当前状态"
tags:
  - technical-line
  - research-guide
  - GPU
  - HPC
  - heterogeneous-computing
  - MPI
  - performance-engineering
status: "in-progress"
date_start: 2026-07-21
date_update: 2026-08-06
related:
  - gpu-hpc/distributed-algebra-and-execution-decoupling
  - gpu-hpc/heterogeneous-execution-modes
  - gpu-hpc/method-lineage
  - ../piml-matrix-free-gpu/_index
  - ../piml-matrix-free-gpu/project-plan
---

# GPU/HPC 异构并行与端到端性能技术线研究指南

> **定位**：本页是 GPU/HPC 技术线的长期第一入口，博士后阶段横向服务 [[../piml-matrix-free-gpu/project-plan#三、工作包与依赖|核心项目 WP1–WP3]]，但长期能力仍可跨项目复用。本页集中回答“目前已经具备什么能力、距离最终目标还有什么差距、下一步如何推进以及何时可以标记完成”。系统解耦框架见 [[../../concepts/gpu-hpc/distributed-algebra-and-execution-decoupling]]；团队公开 HPC 成果的演进与纳入标准见 [[../../concepts/gpu-hpc/method-lineage]]。
>
> **当前主要研究对象**：以三维线弹性 Matrix-Free 求解和 PIML 子结构批处理作为首个统一载体，逐步覆盖 CPU、单 GPU、多 GPU、GPU-aware MPI 与完整拓扑优化流程；其他 PDE、非线性和多物理场仅作为后续扩展方向。
>
> **当前事实底线**：已经有 soptx 单次 GPU MatVec 证据，以及独立 `mfleo` 在单 GPU + 单 CPU 核条件下的端到端 CG 和基础预条件工程经验；Ma2026 提供团队公开的 CPU/MPI 完整优化流程并行基础。三者不是同一套一体化实现，多 GPU、多 CPU 核协同及 GPU-aware MPI 尚未考虑，也尚未完成 PIML 批量推理与子结构 Matrix-Free 的端到端 GPU 管线和桌面端十亿细网格。

## 一、定位、事实所有权与研究目标

最终目标不是只优化一个 GPU kernel，而是形成可解释、可扩展、可集成的异构性能能力：在满足数值正确性和求解收敛门禁的前提下，降低完整 solve 或完整优化迭代的墙钟时间与峰值内存，并能够解释性能瓶颈如何随规模、硬件和算法阶段迁移。

| 维度 | 最终目标 |
|---|---|
| 测量协议 | kernel、MatVec、solve、优化迭代与完整任务边界统一，基线和同步语义明确 |
| 单设备执行 | CPU、单 GPU 使用同一离散、停止准则和正确性门禁，能够完成端到端对照 |
| 数据组织 | batch、布局、缓存—重算、scatter-add、kernel fusion 和工作区策略可组合 |
| 数值精度 | FP64、FP32 与混合精度同时评价误差、迭代数、回退和端到端收益 |
| 分布式执行 | CPU MPI、多 GPU、GPU-aware MPI 的 owned/ghost、通信、归约和粗网格语义统一 |
| 性能诊断 | Roofline、时间分解、内存和通信数据能够定位实际瓶颈 |
| 扩展性 | 单卡、多卡和多节点强弱扩展使用可复现配置与一致问题定义 |
| 软件集成 | 后端选择、设备资源、profiling 和性能回归形成可复用模块 |

本技术线负责批处理、数据布局、设备执行、内存与通信、profiling、扩展性和性能回归；PIML 模型物理正确性、结构保持与回退见 [[piml-research-guide]]，Matrix-Free 算子、Krylov 和预条件的数学正确性见 [[matrix-free-research-guide]]。本页接收两条数值技术线冻结的接口与正确性门禁，不建立第二套算子或模型定义。

### 1.1 核心研究问题

1. PIML 推理、局部算子作用和 scatter-add 应缓存、按需计算还是融合为一个管线？
2. 数据布局怎样兼顾规则子结构 batch、边界子结构、尾 batch 和多种后端？
3. 当前瓶颈是算力、显存带宽、原子回填、数据搬移、launch、归约、预条件还是通信？
4. 单次 MatVec 加速能否转化为完整 solve 和完整优化迭代收益？
5. FP64、FP32 与混合精度如何影响结构性质、Krylov 收敛和最终拓扑？
6. 多 GPU/多节点下如何处理 halo exchange、全局归约、粗网格和负载不均衡？
7. 如何建立跨设备、跨后端和跨提交可复现的性能回归体系？

## 二、GPU/HPC 技术路线与性能边界

### 2.1 执行路线与评价边界

异构执行模式本身的稳定分类（硬件拓扑、执行层级、编程模型、数据/精度策略四个正交维度）见 [[../../concepts/gpu-hpc/heterogeneous-execution-modes]]；本节的五级路线是这些模式在本项目对象上的实施顺序。

当前技术路线按“组装式 CPU/GPU 参考 → 同题 Matrix-Free CPU/单 GPU → PIML 批处理与 Matrix-Free GPU 融合 → 完整拓扑优化与混合精度 → 多 GPU/GPU-aware MPI”逐级推进。每一级都继承上一阶段冻结的离散、边界条件、停止准则与正确性门禁，不允许用单个 kernel、单次 MatVec 或局部吞吐替代完整 solve 与完整优化流程的端到端结论。

性能评价必须同时记录绝对时间、迭代数、峰值内存/显存、数值误差及瓶颈迁移；硬件、装配层级、预条件、数值精度或编程模型发生变化时，应分别标明，不能把联合收益全部归因于 GPU。五级计时、Roofline、强弱扩展与可复现记录协议由 [[../../concepts/gpu-hpc/performance-model]] 统一维护。

### 2.2 当前可用工程基础

| 基础 | 已经做到的内容 | 当前边界 |
|---|---|---|
| soptx GPU 算子原型 | 13.2 万 DOF 下，单次 GPU MatVec 约为 CPU 路径的 $11.9\times$；内存估计从 42.1 MB 降至 4.0 MB；NumPy、PyTorch CPU、CUDA 三后端结果一致 | 只证明单次算子作用的 GPU 趋势和省内存潜力，不是完整 solve 或优化迭代加速；独立 `brighthe/soptx` 主仓库已有三维线弹性、PyTorch/CUDA 与 CG 候选入口，但尚未通过阶段 1 运行门禁 |
| `mfleo` 单 GPU 工程经验 | 已完成 650 万 DOF、单 GPU + 单 CPU 核条件下的端到端 CG；相对同规模 MFEM PA 基线约 $3.72\times$–$12.74\times$；P2 tet 的 Jacobi、Chebyshev 测试在单 GPU 条件下约 $4\times+$ | 属独立 PA/Matrix-Free 工程路径，未接入当前 soptx/PIML 原型；尚未考虑多 GPU、多 CPU 核协同或 GPU-aware MPI |
| Ma2026 团队公开 HPC 基础 | 使用 CPU/MPI、PETSc 多重网格和分布式子结构划分，并行覆盖粗网格求解、恢复、灵敏度、PDE 滤波和 MMA，报告强弱扩展 | 属公开 CPU/MPI 完整优化流程证据，不是 GPU 或异构实现；完整边界见 [[../../concepts/gpu-hpc/method-lineage]] |
| 分布式算子工程参考 | `xihe/matrix_free_3` 已形成 Python、FEALPy backend、MPI CPU 的 EA/EbE 原型，包含 gather、局部作用、scatter-add、共享自由度同步和 Krylov/预条件探索 | 正确性、收敛性和扩展性验证尚未闭环；公司仓库独立维护，本知识库不复制代码、数据、日志或内部文档 |

这四类基础分别覆盖 GPU MatVec 趋势、单 GPU 端到端工程、团队公开 CPU/MPI 完整流程和分布式算子结构，但不能拼接成“PIML × Matrix-Free × GPU/MPI 已经完成”的结论。

## 三、国内外研究现状、研究缺口与选题价值

### 3.1 范围与判定口径

本页所称 GPU/HPC 不只是把现有 CPU kernel 改写为 CUDA，而是研究离散、算子、求解器和完整优化流程怎样适配异构体系结构。证据必须分别说明：改变的是硬件、算法、装配层级还是精度；使用单 GPU、多 GPU、CPU–GPU 协同或 GPU-aware MPI 中的哪一种；性能数字对应 kernel、MatVec、solve、优化迭代还是完整任务。统一的五级计时、Roofline、强弱扩展和正确性口径由 [[../../concepts/gpu-hpc/performance-model]] 维护。

GPU 加速的对象至少包括局部积分或局部算子、gather/scatter、Krylov 向量原语与全局归约、预条件、位移恢复、灵敏度、过滤和优化器。只迁移其中一项不能自动支持完整优化加速；Matrix-Free 减少数据移动、混合精度改变吞吐和多 GPU 增加设备资源也属于算法—硬件联合变化，必须保留绝对时间、迭代数、峰值显存和数值误差，不能把联合收益全部归因于 GPU。

### 3.2 国外研究进展

国外路线沿“GPU 进入完整拓扑优化（Wadbro & Berggren 2009）→ 三维 Matrix-Free GPU（Schmidt & Schulz 2011/2012）→ 数据局部性细化与多 GPU（Martínez-Frutos & Herrero-Pérez 2015/2016）→ 可移植后端抽象与多 GPU 混合精度（Abdelfattah et al. 2021、Herrero-Pérez & Martínez Castejón 2021）→ 高层语言完整流程（Träff et al. 2023）”演进，核心共识是 GPU 可覆盖完整优化流程，但每项证据的硬件、装配层级和边界均不同，不能跨层外推。逐篇贡献与证据边界见 §4 证据锚点表；跨线证据成熟度与耦合机制见 [[../piml-matrix-free-gpu/high-performance-solver-survey]]。

### 3.3 国内与团队路线进展

“国内”只依据论文原始机构、实施平台或资助信息判断，不依据作者姓名推断。当前可核实证据覆盖 Python 高层 GPU 路线（Hou et al. 2025，CuPy 向量化 SpMV，非 Matrix-Free）、CPU–GPU 异构流程（Liu et al. 2026，EMsFEM + MPI + GPU 灵敏度）和团队 CPU/MPI 完整优化流程（[[../../literature/topology-opt/notes/Ma2026-highperformanceparallel|Ma et al. 2026]]，不用 GPU、粗网格仍显式组装）；均未形成与本项目相同的 PIML–Matrix-Free–GPU 链路。逐篇边界见 §4；未建单篇笔记文献的 `to-ingest` 状态见 [[../../literature/_index#当前 ingest 队列]]。

### 3.4 研究缺口与选题价值

1. **算法收益与硬件收益尚未统一分解。** 现有论文常同时改变装配层级、预条件器、精度、编程模型和硬件；缺少同题、同离散、同停止准则下从 CPU 组装式到 GPU Matrix-Free 的逐级消融。
2. **完整拓扑优化的端到端瓶颈会迁移。** MatVec 加速后，预条件、归约、恢复、灵敏度、过滤、优化器和数据搬移可能成为主导；单 kernel 或单 solve 的峰值吞吐不能回答完整任务是否受益。
3. **动态拓扑与复杂离散的 GPU 适配仍不统一。** 规则体素能够避免部分间接访存和数据竞争，但低阶非结构网格、边界子结构、材料分布持续更新和多种局部算子会改变 batch、scatter-add 与负载均衡策略。
4. **多 GPU 与 GPU-aware MPI 证据不足。** 多 GPU 工作已经证明设备容量和任务并行的价值，但 halo exchange、全局归约、粗网格、设备绑定和通信—计算重叠尚未在本项目对象上闭环。
5. **PIML 推理与 Matrix-Free 求解尚未形成统一 GPU 管线。** 现有 GPU 路线使用精确或预计算局部算子，国内 PIML 路线基于 CPU/MPI；尚缺预测、结构检查、精确回退、局部作用、scatter-add、Krylov 和预条件的一体化时间—显存证据。
6. **混合精度缺少力学与优化级门禁。** 吞吐和显存收益必须继续检查对称性、正定性、真实残差、迭代数、位移、柔顺度、灵敏度和最终拓扑，不能只报告低层数值差异。

对 WP1，GPU/HPC 单线用于建立精确算子下可重放的 CPU、单 GPU、Matrix-Free GPU 和必要的多 GPU/MPI 对照，回答“减少数据移动和改变执行平台后，完整 solve 的正确性、收敛、时间和显存怎样变化”。这使后续学习算子的收益具有可信基线，而不是与不一致的 CPU 程序比较。

对 WP2，本技术线用于研究局部材料分布、预测 $N/K_s$、结构检查和精确回退的批量组织，比较缓存、按需推理和推理—局部作用融合，并明确 FP64、FP32 与混合精度的结构门禁。GPU 不是 WP2 的独立训练目标，而是检验结构保持局部算子能否以可部署方式产生的执行环境。

对满足门禁后的 WP3，选题价值在于研究学习近似、全局 Matrix-Free 和异构执行三者的耦合：预测误差会影响 Krylov 与预条件，Matrix-Free 会改变缓存—重算和数据移动，GPU 会改变 batch、scatter-add、归约和通信成本。只有同时报告局部结构性质、真实残差、全局响应、最终拓扑、完整时间和峰值显存，才能判断融合是否真正扩大可解规模。

## 四、证据锚点及结论边界

本表是单线证据边界（每项证据能支持/不能支持什么）；跨线证据成熟度、耦合机制与研究假设见 [[../piml-matrix-free-gpu/high-performance-solver-survey]]。

| 证据 | 计算对象与平台 | 能支持的结论 | 不能支持的结论与证据边界 |
|---|---|---|---|
| Williams et al. 2009 | Roofline；算术强度、带宽与峰值 | 支持数据移动／算力瓶颈的基础判定 | 不解释完整 solve、通信和预条件；`refs.bib` 已登记 |
| Wadbro & Berggren 2009 | 二维 Poisson 型像素拓扑优化；商品级 GPU | GPU 可进入百万级变量完整优化 | 不支持三维结构弹性、Matrix-Free 或多 GPU |
| Schmidt & Schulz 2011/2012 | 三维 SIMP、Matrix-Free CG；CUDA GPU | 早期全 GPU 三维结构拓扑优化路线 | 不支持现代硬件、多 GPU 或学习算子 |
| Martínez-Frutos & Herrero-Pérez 2015 | 固定网格 FEA、DoF-level Matrix-Free；GPU | 数据局部性、片上存储和细粒度映射可降低访存 | 主要是 FEA/solve，不是完整优化 |
| Martínez-Frutos & Herrero-Pérez 2016 | 鲁棒拓扑优化；单机多 GPU | 任务级与数据级并行可覆盖求解、灵敏度和过滤 | 不支持多节点 GPU-aware MPI 或 PIML |
| Abdelfattah et al. 2021 | CEED 高阶 Matrix-Free；NVIDIA/AMD GPU | 支持高阶离散的数据移动优化和后端可移植性 | 不直接支持低阶动态拓扑或 PIML |
| Herrero-Pérez & Martínez Castejón 2021 | 密度法拓扑优化、分布式 CG/AMG、混合精度；多 GPU | 多 GPU 容量、预条件和精度策略需共同评价 | 不等同于全局不组装或学习算子融合 |
| Träff et al. 2023 | 三维线性／非线性拓扑优化；OpenMP/Futhark；单 GPU | 摘要支持单 GPU 千万级单元与完整优化流程 | 具体硬件、Matrix-Free、求解器和外推边界待译文精读 |
| Hou et al. 2025 | CuPy 向量化 SpMV、二维/三维拓扑优化；单 GPU | 支持国内近期 Python GPU 与千万级单元路线 | 全局矩阵已生成，不属于 Matrix-Free |
| Liu et al. 2026 | EMsFEM 层级结构、MPI CPU + RTX 4090；完整并发优化 | 支持国内 CPU–GPU 异构响应/灵敏度路线 | 单服务器、显式宏观算子；不支持 PIML/全局 Matrix-Free |
| Ma et al. 2026 | PIML、CPU/MPI、PETSc MG-GMRES；完整优化 | 支持团队并行流程、按需预测和强弱扩展基础 | 不是 GPU 或全局算子级 Matrix-Free；已入库 |

除 Williams 2009 与 Ma 2026 外，本表目前只采用出版社页面能够直接支持的事实。带链接条目：[[../../literature/topology-opt/notes/Traff2023-GPU-topology-optimisation|Träff et al. 2023]]、[[../../literature/topology-opt/notes/Ma2026-highperformanceparallel|Ma et al. 2026]]。未建单篇笔记文献的 `to-ingest` 状态统一维护在 [[../../literature/_index#当前 ingest 队列]]；当前证据矩阵不替代后续全文 ingest。

## 五、阶段门禁与当前执行状态

### 5.1 已完成的独立基础

- soptx 原型已有 NumPy、PyTorch CPU 与 CUDA 的算子结果一致性，以及受控规模下的单次 GPU MatVec 和内存趋势数据。
- `mfleo` 已形成单 GPU + 单 CPU 核条件下的端到端 CG、基础预条件和 PA kernel 工程经验。
- Ma2026 已公开验证 CPU/MPI、PETSc 多重网格和完整拓扑优化流程的强弱扩展。

### 5.2 部分完成或待核实

- **soptx `examples/gpu_elasticity/minimal_demo.py` 已运行通过**：二维平面应变 FA 组装 + CG 完整 solve，pytorch 后端 CPU/CUDA 逐位一致（真残差 ≤ 1e-10、逐位 ≤ 1e-9），对照设计符合 [[../../concepts/gpu-hpc/performance-model#4. 异构执行与通信口径|CPU/GPU 口径]]。与阶段 1 门禁差异：二维制造解非三维悬臂梁、上游 FEALPy、未绑定性能记录格式；可支撑正确性链路成立，不构成三维悬臂梁或性能数字门禁证据。工程入口：`/home/brighthe/workspace/soptx/examples/gpu_elasticity/`。
- soptx 当前数字尚未绑定统一的预热、同步、重复统计、硬件软件版本和可重放入口。已 clone 的独立 `C:\workspace\soptx`（`brighthe/soptx`，`main`）包含 `soptx/tests/test_cantilever_3d_wsl.py`：该入口已参数化 NumPy/PyTorch/JAX backend、`cpu/cuda` device、三维悬臂梁和 CG；另有当前模型 `soptx/model/cantilever_3d_lfem.py`。本次只做静态核查，尚未运行，不能登记为标准 GPU 算例已经跑通。
- `mfleo` 的结果来自独立工程路径，尚未与三维线弹性共享基准、PIML predictor 或当前科研原型对齐。
- `xihe/matrix_free_3` 可作为 CPU MPI 数据流参考，但相关验证实验尚未运行，不能写成正确性与扩展性已经闭环。
- 当前结果尚未形成跨设备、跨后端和跨提交的统一性能记录与回归格式。

### 5.3 尚未完成

- 尚未建立可重放的 FEALPy/soptx 三维线弹性组装式 CPU/GPU 完整求解算例。
- 尚未在同一三维线弹性问题下建立 Matrix-Free CPU、单 GPU 与 MPI 对照基线。
- 尚未完成 PIML 批量推理、局部 $K_s x_s$、scatter-add、Krylov 与预条件的一体化 GPU 管线。
- 尚未将位移恢复、灵敏度、PDE 滤波和 OC/MMA 纳入完整 GPU 优化迭代。
- 尚未完成多 GPU、GPU-aware MPI、多节点强弱扩展和通信隐藏。
- 尚未形成可复用异构后端、自动性能回归或桌面端十亿细网格验证。

当前只证明若干独立能力可为后续融合提供基础，不能声称已经形成端到端异构拓扑优化系统。

### 5.4 目标与当前差距

| 能力维度 | 当前状态 | 下一道关键门槛 |
|---|---|---|
| 性能协议 | 已有五级计时规范，历史数字仍分散 | 在首个 CPU/GPU 完整 solve 中落实环境、同步、重复统计和正确性字段 |
| 证据入口 | `examples/gpu_elasticity/minimal_demo.py` 二维 CPU/GPU 逐位一致已跑通；三维悬臂梁 CPU/CUDA + CG 候选入口尚未运行并冻结 | 从当前主仓库整理唯一可重放的 CPU/GPU 命令；历史数字无法恢复时降级为历史证据 |
| 参考问题 | 当前 soptx 主仓库已有 `CantileverBeam3d` 和三维悬臂梁测试，各工程基础仍使用不同离散和规模 | 先冻结组装式三维线弹性算例，再由 Matrix-Free 路线继承同题黄金结果 |
| CPU 基线 | 有候选组装式组件和独立 CPU/MPI 工程基础 | 先完成与 GPU 同题、同精度、同停止准则的组装式 CPU 参考 solve |
| 单 GPU | 有历史 MatVec 趋势和独立端到端经验 | 先完成 FEALPy/soptx 组装式 GPU CG，再建立同题 Matrix-Free MatVec、预条件和完整 solve |
| PIML batch | 尚未实现融合 | 冻结 batch 形状、尾 batch、缓存/重算和回退语义 |
| GPU 管线 | 原语分散 | 贯通 gather、推理/局部作用、scatter-add、向量原语、归约和预条件 |
| 完整优化 | 尚未接入 | 覆盖恢复、灵敏度、过滤、优化器及完整 $T_{\mathrm{iter}}$ 分解 |
| 精度策略 | 尚无统一对照 | 比较 FP64、FP32、混合精度的误差、迭代数、回退和收益 |
| 多 GPU/多节点 | 尚未考虑或实现 | 完成设备绑定、GPU-aware MPI、通信/计算重叠和粗网格策略 |
| 性能回归 | 无统一状态账 | 固化基准配置、统计阈值、正确性门禁和新基线规则 |
| 软件集成 | 各路径接口独立 | 将设备、后端、profiling 和诊断封装为可复用模块 |

当前最优先的工作不是追求未经定义的峰值加速，而是先用 FEALPy/soptx 跑通一个可重放的三维线弹性 CPU/GPU 完整求解算例，在实际入口中冻结参考问题、正确性门禁和最小性能记录字段；只有完整 solve 基线稳定后，Matrix-Free kernel 优化才具有可比较意义。

### 5.5 阶段门禁

#### 阶段 1：跑通 FEALPy/soptx 三维线弹性 CPU/GPU 算例

- 基于独立 `C:\workspace\soptx` 主仓库、FEALPy backend、soptx 三维悬臂梁 PDE 和线弹性组件整理唯一可重放入口，冻结网格、材料、边界、载荷、DOF 顺序、FP64 精度、CG 停止准则与结果格式。
- CPU 作为参考路径，GPU 使用 PyTorch/CUDA；两条路径均须完成刚度装配、载荷构造、边界条件处理和 CG 状态方程求解，不能以单个 kernel、局部装配或一次 MatVec 代替完整 solve。
- 对照 CPU/GPU 位移、柔顺度或应变能、真残差、CG 迭代数和边界自由度；先建立正确性与可重放性，再讨论性能。
- 以 [[../../concepts/gpu-hpc/performance-model]] 为规范，记录命令、代码版本、硬件软件环境、预热、同步、完整 solve 计时和峰值内存；同时核查 soptx 与 `mfleo` 历史数字的来源，无法恢复的数字明确标为历史记录。
- **门禁**：存在唯一可重放命令；同一问题的 CPU/GPU 完整 solve 均收敛并通过位移、能量/柔顺度、真残差和边界条件检查；结果包含迭代数、绝对时间、峰值内存和环境记录。历史 $11.9\times$ 仅作为单次 MatVec 证据，不作为本阶段加速比阈值。

#### 阶段 2：建立同题 Matrix-Free GPU solve 与预条件基线

- 继承阶段 1 冻结的三维线弹性离散、边界、载荷、DOF 顺序、FP64 精度、停止准则和组装式 CPU/GPU 黄金结果，不另建一套数值基准。
- 建立同题 Matrix-Free CPU 与单 GPU 算子，验证完整 MatVec、Krylov 和预条件路径；同时测量 setup/update、MatVec、预条件、向量原语、同步、峰值内存和完整 solve。
- 使用 system-level timeline 和 kernel-level 指标判断瓶颈，Roofline 只用于解释适合该模型的计算区间；CPU MPI 与分布式数据流作为后续扩展接口保留。
- **门禁**：Matrix-Free CPU/GPU 结果通过阶段 1 组装式黄金结果以及 [[matrix-free-research-guide]] 的算子正确性与真残差门禁；完整 solve 可重放，并同时报告绝对时间、迭代数、峰值内存和各阶段分解，不以单次 MatVec 代替阶段完成。

#### 阶段 3：打通 PIML 批量推理与 Matrix-Free GPU 管线

- 接收 [[piml-research-guide]] 冻结的 predictor 输入、输出、结构检查和精确回退语义，按规则子结构、边界类型和尾 batch 设计固定形状批处理。
- 比较“预测并缓存 $K_s$”“每次 MatVec 按需推理”和“推理—局部作用融合”三条路径，贯通 gather、局部作用、scatter-add、向量更新、归约、Krylov 和预条件。
- 分析 batch 大小、布局、原子回填、颜色划分、分区缓冲、kernel fusion 和工作区复用。
- **门禁**：三条策略在同一真值、容差和 solve 接口下比较；同时给出局部结构性质、全局响应、迭代数、吞吐、完整 solve 时间和峰值显存的 Pareto 数据。

#### 阶段 4：覆盖完整优化迭代与混合精度

- GPU 化或明确保留在 CPU 的位移恢复、应变能、灵敏度、PDE 滤波、OC/MMA 和设计变量更新，记录完整 $T_{\mathrm{iter}}$ 分解。
- 比较 FP64、FP32 和混合精度，检查结构性质、残差、位移、柔顺度、灵敏度、拓扑、迭代数和精确回退。
- 对长期占主导的环节开展针对性优化，不以将瓶颈转移到其他阶段作为完成。
- **门禁**：至少完成一组可重放的完整优化流程；CPU/GPU 在约定容差内一致，并给出误差—时间—内存 Pareto 前沿及所有主要阶段的时间占比。

#### 阶段 5：多 GPU、GPU-aware MPI 与可复用后端

- 冻结 rank/thread/device 绑定、owned/ghost、halo exchange、设备缓冲区、全局归约、粗网格和负载划分语义，验证所用 MPI 实现的设备缓冲区路径。
- 开展单 GPU、多 GPU 和多节点强弱扩展，分别报告计算、通信、归约、粗网格、数据搬移和负载不均衡。
- 将后端选择、设备资源、profiling、结果记录和性能回归封装为可复用模块；硬件、算法或计时边界变化时建立新基线。
- **门禁**：正确性、完整 solve/优化迭代和强弱扩展均有可重放配置；GPU-aware MPI 结论绑定具体 MPI 实现与版本；性能回归同时包含数值门禁，且不存在用局部 kernel 数据替代多节点端到端结论的情况。

各阶段只有在具备可重放入口、明确事实来源、正确性证据和端到端计时后才能标记为“已完成”。不预设缺乏基准支持的加速比阈值；性能没有提升时也应保留有效的瓶颈分析与失败模式。

回退原则：PIML 推理覆盖 MatVec 收益时缓存 $K_s$、采用压缩表示或融合推理与局部作用；scatter-add 原子冲突严重时使用颜色划分、分区缓冲或分阶段归并；混合精度破坏结构性质或收敛时局部/全局回退 FP64；显存不足时使用流式 batch、重计算和分区执行；多 GPU 效率差时先处理负载、归约和粗网格，不盲目增加节点。

## 六、权威事实来源

- [[../../concepts/gpu-hpc/distributed-algebra-and-execution-decoupling]] — 分布式计算系统的代数/算法层与硬件/执行层解耦框架。
- [[../../concepts/gpu-hpc/heterogeneous-execution-modes]] — 异构执行模式分类（硬件拓扑、执行层级、编程模型、数据/精度）与本页执行路线的坐标。
- [[../../concepts/gpu-hpc/reference-libraries/fealpy-mfem-gpu-backend-comparison]] — FEALPy 4.0 与 MFEM 的 GPU 后端设计对比（阶段 1 与 Matrix-Free 路线的实现层参照）。
- [[../../concepts/gpu-hpc/method-lineage]] — 团队公开 HPC 成果的纳入标准、Ma2026 CPU/MPI 节点与公开空白。
- [[../piml-matrix-free-gpu/_index]] — 博士后核心研究项目统一入口与最低融合边界。
- [[../piml-matrix-free-gpu/project-plan]] — WP1–WP3 的 GPU/HPC 角色、阶段依赖和项目级完成条件。
- [[../piml-matrix-free-gpu/high-performance-solver-survey]] — GPU/异构并行、端到端瓶颈和实验矩阵调研。
- [[../../literature/_index#当前 ingest 队列]] — 本阶段核心论文和唯一 `to-ingest` 状态入口。
- [[../../literature/topology-opt/notes/Ma2026-highperformanceparallel]] — 团队 CPU/MPI 并行 PIML、PETSc 多重网格和强弱扩展的论文事实。
- `C:\workspace\soptx`（个人公开仓库 `brighthe/soptx`，`main`）— 阶段 1 的当前实现来源；已静态定位 `soptx/tests/test_cantilever_3d_wsl.py` 与 `soptx/model/cantilever_3d_lfem.py`，但尚未运行，不作为本知识库运行依赖。
- `C:\workspace\fealpy\app\soptx` — FEALPy 内置的旧版 SOPTX，只作为历史代码参考，不再作为阶段 1 实现基线。
- `C:\workspace\mfleo` — 独立单 GPU PA/Matrix-Free 工程事实源；不作为本知识库运行依赖。
- `C:\workspace\xihe`（`origin/develop`）— `xihe/matrix_free_3` 的独立公司工程事实源；不复制公司代码、数据、日志或内部文档。
- [[piml-research-guide]]、[[matrix-free-research-guide]] — 另外两条长期技术线及其正确性门禁。
- [[../../discussions/guo-xu/first-formal-work-report]] — 第一次线下汇报中的 GPU/HPC 摘要。
- [[_index]] — 长期技术线总入口。
