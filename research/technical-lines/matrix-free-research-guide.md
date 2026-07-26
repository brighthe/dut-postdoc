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
date_update: 2026-07-26
related:
  - matrix-free/assembly-levels
  - frame8_matrix_free_pipeline_guide
  - piml-matrix-free-execution-plan
---

# Matrix-Free 全局算子与迭代求解技术线研究指南

> **定位**：本页是 Matrix-Free 技术线的长期第一入口，集中回答“目前已经具备什么能力、距离最终目标还有什么差距、下一步如何推进以及何时可以标记完成”。Matrix-Free 的数学定义、五级装配层次和第三方框架术语见 [[../../concepts/matrix-free/assembly-levels]]。
>
> **当前主要研究对象**：以三维线弹性方程作为首个统一参考问题，建立 FA/LA/EA/PA/UA、Krylov、预条件以及 CPU/GPU/MPI 的正确性与性能基线；Maxwell/PML 现阶段仅作为已有 EA/EbE 分布式实现的工程参考。
>
> **当前事实底线**：已经形成积分点 contraction 原型、`mfleo` 的 MFEM PA 工程路径和 `xihe/matrix_free_3` 的 EA/EbE 分布式原型；三者相互补充，但不是同一套一体化实现，也尚未在统一算例和 Benchmark 下完成横向验证。

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

| 基础 | 已经做到的内容 | 当前边界 |
|---|---|---|
| 当前积分点 contraction 原型 | 直接执行 $\mathbf B^T\mathbf D\mathbf B\mathbf x$，不形成全局 $\mathbf K$ 或完整单元 $\mathbf K_e$；MatVec 与显式矩阵乘相对误差达到 $10^{-15}$–$10^{-13}$；已跑通小规模 CG，最终残差约为 $10^{-11}$–$10^{-10}$；NumPy、PyTorch CPU、CUDA 结果一致 | 是否预存 $\mathbf D_e$ 尚未核实，因此只能确定不是 FA、LA 或 EA，不能在 PA 与 UA 之间强行归类 |
| `mfleo` | 基于 MFEM Partial Assembly，以 C++ CPU/CUDA kernel 实现线弹性算子；已有 tet/hex、不同阶次、单 GPU + 单 CPU 核条件下的端到端 CG、对角线及 Jacobi/Chebyshev 等工程经验 | 属于 PA/QA 工程基础；尚未考虑多 GPU、多 CPU 核协同或 GPU-aware MPI，也不是当前科研原型和完整有限元平台 |
| `xihe/matrix_free_3` | 已形成 Python、FEALPy backend、MPI CPU 的 Maxwell/PML 分布式原型；保存完整单元局部张量并执行 gather、局部作用、scatter-add 和共享自由度同步，因此属于 EA/EbE；已包含 GMRES/MINRES、真残差诊断及 block Jacobi/ILU 探索 | 人工真解、离散误差、多进程一致性、预条件收敛和规模验证尚未闭环，不能表述为“正确性与收敛已全面验证” |
| 第三方能力 | MFEM 提供多级装配与 PA/UA 能力，PETSc 提供 Shell Matrix、Krylov 和预条件接口；其他框架映射见概念页 | 属于可复用基础，不等于本技术线已经完成对应实现 |

公司仓库只作为只读事实源。本知识库仅保留非敏感技术结论，不复制公司代码、运行日志、内部数据或客户算例，也不建立跨仓库运行依赖。

### 郭旭老师团队公开成果与本技术线衔接

截至 2026-07-26，当前公开且可核实的直接 Matrix-Free 相关节点只有 [[../../literature/topology-opt/Ma2026-highperformanceparallel]]。该工作通过 PIML 按需预测并释放多尺度形函数 $\mathbf N^j$ 降低内存，但仍形成子结构缩聚刚度并组装粗网格全局缩聚矩阵；按五级分类，其全局求解属于第 1 级 FA/TA，而不是算子级 EA、PA 或 UA。

这项成果为“以重计算换存储”及 PIML 子结构接入提供了直接基础。本技术线的接续任务是进一步打通不组装全局缩聚矩阵的 $y=\mathbf K_s x$、Krylov、预条件和 GPU/MPI 闭环；这是当前拟推进的研究方向，不能写成团队已经完成的公开成果。团队成果的长期演进和新增证据统一维护在 [[../../concepts/matrix-free/method-lineage]]。

## 三、当前成果边界

### 已完成

- 已证明积分点算子作用可以在不形成全局矩阵和完整单元矩阵的前提下达到机器精度一致，并进入小规模 CG 求解。
- 已具备 `mfleo` 的 PA、C++/CUDA、单 GPU + 单 CPU 核端到端 CG、Krylov 和基础预条件工程经验。
- 已具备 `xihe/matrix_free_3` 的 EA/EbE、MPI 分布式算子、Krylov 和预条件探索基础。

### 部分完成或待核实

- 当前 contraction 原型仍需核实 $\mathbf D_e$ 缓存策略，才能确定属于 PA 还是 UA。
- `xihe/matrix_free_3` 已有分布式原型，但正确性、收敛性和可扩展性验证尚未闭环。
- 预条件能力分散在不同实现中，尚未形成统一的 operator level 与 preconditioner level 组合规范。
- 各实现的离散问题、自由度顺序、残差和计时边界尚未完全统一。
- `mfleo` 尚未考虑多 GPU、多 CPU 核协同或 GPU-aware MPI，不能将单 GPU + 单 CPU 核结果表述为 GPU/MPI 并行已经完成。

### 尚未完成

- 尚未形成连接 Python/C++、CPU/GPU、single/MPI 的统一 Matrix-Free 框架。
- 尚未完成 FA、LA、EA、PA、UA 在同一参考问题下的横向 Benchmark。
- 尚未形成统一的 GPU-aware MPI、自动验收和唯一状态账。
- 尚未把精确子结构 $K_s$ 和 PIML 预测的 $\widehat K_s$ 依次接入全局 Krylov 求解闭环。

## 四、目标与当前差距

| 能力维度 | 当前状态 | 下一道关键门槛 |
|---|---|---|
| 参考问题 | 三类基础使用不同 PDE、离散和实现 | 冻结三维线弹性参考问题及 FA/TA 黄金基线 |
| 装配层级 | EA 与 PA/UA 分别已有基础 | 在同一问题上统一 FA、LA、EA、PA、UA 的语义和结果 |
| 算子协议 | 各项目接口独立 | 冻结 `setup/update/apply/diagonal`、边界和 owned/ghost DOF 语义 |
| 双语言 | Python 与 C++ 各有局部基础 | 使用共享黄金数据验证两种语言表示同一离散算子 |
| 并行与硬件 | `mfleo` 有单 GPU + 单 CPU 核经验，`xihe` 有 CPU MPI 原型，两条路径尚未融合 | 完成多 CPU 核、多 GPU及 GPU-aware MPI 的实现与一致性验证 |
| Krylov 与预条件 | 已有 CG、GMRES/MINRES 和若干基础预条件 | 建立分层预条件、真残差门禁、重建与复用策略 |
| Benchmark | 各项目独立记录 | 统一正确性、内存、通信、更新、MatVec 和完整 solve 报告 |
| PIML 接口 | 尚未接入 | 先接入精确 $K_s$，验证后再替换为 $\widehat K_s$ 并分析误差传播 |

当前最优先的工作不是继续增加孤立 kernel，而是先恢复、跑通并验证 `xihe/matrix_free_3`，以现有 EA/EbE、CPU MPI 和 Krylov 路径建立可复现工程基线；随后再提取通用接口并迁移到三维线弹性。

## 五、下一步实施路线

### 阶段 1：恢复、跑通并验证 `xihe/matrix_free_3`

- 当前起点是：`run.py` 的默认 VTU 网格不在仓库内，`pyproject.toml` 未显式声明 `fealpy`，README 未给出运行命令，已有 GMRES/MINRES 日志也未形成收敛闭环；这些均应视为待处理项，而不是已完成结果。
- 恢复可合法使用的非敏感网格、匹配的 `fealpy` 环境和可重放命令，冻结网格、有限元次数、MPI ranks、求解器、预条件器、停止准则与输出位置。
- 至少完成 1 rank 和 2 ranks 复现，记录真实残差、制造解误差和切向边界误差；仅进程运行到结束不等于算例跑通，现有 `converged: False` 日志不得作为完成证据。
- 以当前 `rtol=1e-8`、`atol=1e-10` 为求解门禁，并保存环境、命令、输入与诊断摘要；若真实残差未满足门禁，则阶段保持未完成并进入问题诊断。

### 阶段 2：提取 EA/EbE 分布式接口

- 梳理 `xihe/matrix_free_3` 的 gather、单元张量作用、scatter-add、共享自由度同步和边界处理数据流，确认其保存完整单元张量的 EA/EbE 定位。
- 提取 operator、GMRES/MINRES、preconditioner 和 diagnostics 的可复用接口语义，不复制 `xihe` 公司代码、内部数据或运行依赖。
- 冻结 operator level、preconditioner level、owned/ghost DOF、真残差和计时字段，作为后续线弹性路径的接口契约。

### 阶段 3：迁移到三维线弹性

- 建立三维线弹性 FA/TA 显式黄金基线，冻结网格、自由度顺序、边界条件、载荷、停止准则和结果格式。
- 在 FA/TA 基础上建立 LA 显式 MPI 基线，冻结 owned/ghost DOF、halo exchange、局部矩阵与 true-DOF 结果的对应关系，并评估其作为预条件矩阵的用途。
- 将阶段 2 的分布式算子结构迁移到线弹性 EA/EbE，验证 MatVec、能量、真残差以及 1 rank/N rank 一致性。
- 在同一参考问题上继续推进 PA/UA；每完成一个装配层级，同时接入 Krylov 和至少一种可用预条件器，MatVec 可运行不等于阶段完成。

### 阶段 4：对齐 `mfleo` PA 与单 GPU 路径

- 复用 MFEM/PETSc 和 `mfleo` 的工程路径，对齐 EA/PA、Python/C++、边界、残差、计时和输出语义。
- 使用共享黄金算例完成跨语言和 CPU/单 GPU 验证；当前只承认 `mfleo` 单 GPU + 单 CPU 核结果，不写成多 GPU、多核或 GPU-aware MPI 已完成。
- 建立 Jacobi、Chebyshev、Schwarz、多重网格和低阶组装代理等可组合预条件路径，并统一报告 setup、update、operator apply、preconditioner apply、通信、峰值内存和完整 solve。

### 阶段 5：接入子结构与 PIML

- 先用精确 $K_s$ 打通子结构级 Matrix-Free、Krylov 和预条件闭环，再换入 PIML 预测的 $\widehat K_s$，检查结构性质、全局误差、求解收敛和更新成本。
- 开展 GPU 批处理和端到端 profiling，不以单次 MatVec 加速替代完整 solve 结论。
- 在线弹性与单 GPU 路径闭环后，再扩展多 CPU 核、多 GPU 和 GPU-aware MPI。跨技术线时间安排以 [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-execution-plan]] 为准。

若纯 Matrix-Free 预条件不足以稳定收敛，允许使用低阶或低精度组装代理；目标是可靠高效求解，而不是追求预条件器形式上的“完全无矩阵”。

各阶段只有在具备可重放入口、明确事实来源并通过对应阶段门禁后，才能标记为“已完成”；缺少真残差、预条件、峰值内存或完整 solve 的结果只能作为局部证据。

## 六、事实来源与关联页面

- `C:\workspace\xihe`（`origin/develop`）— `xihe/matrix_free_3` 的本地只读事实源；不作为本仓库运行依赖。
- `C:\workspace\mfleo` — `mfleo` 的本地只读事实源；不复制公司代码、数据或内部文档。
- [[../../concepts/matrix-free/assembly-levels]] — Matrix-Free 数学对象、五级装配层次和第三方框架映射。
- [[../../concepts/matrix-free/method-lineage]] — 郭旭老师团队公开 Matrix-Free 相关成果的长期演进和事实边界。
- [[research/postdoc-plan/defense-sprint/direction-1-piml-matrix-free/frame8_matrix_free_pipeline_guide]] — 当前 contraction、CG 和多后端证据。
- [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-high-performance-solver-survey]] — Matrix-Free、预条件和开放问题的综合调研。
- [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-execution-plan]] — PIML、Matrix-Free、GPU 三线融合的总体计划。
- [[../../work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] — 第一次线下汇报中的 Matrix-Free 摘要。
- [[_index]] — 长期技术线总入口。
