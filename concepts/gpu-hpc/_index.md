---
title: "GPU/HPC 主题入口"
type: index
tags:
  - GPU
  - HPC
  - heterogeneous-computing
  - performance-engineering
status: in-progress
date_added: 2026-07-26
date_update: 2026-08-31
---

# GPU/HPC 主题入口

> 本页是 GPU/HPC 的统一语义入口：稳定性能口径与公开成果谱系放在 `concepts/gpu-hpc/`，单篇论文事实放在 `literature/`，当前能力、任务路线与阶段门禁放在 `research/piml-matrix-free-gpu/`，面向导师/合作者的科研讨论与阶段表达放在 `entities/`，已完成事件的历史材料放在 `archive/`。

**命名边界**：本主题名为 GPU/HPC，实际覆盖 GPU 卸载、CPU/MPI 对照、多 GPU、GPU-aware MPI 与端到端性能工程，即广义异构高性能计算；不代表全部 HPC 领域（调度、存储、数据中心等不在本主题范围），也不代表团队已有 GPU 成果——团队公开成果的边界见 [[../../research/piml-matrix-free-gpu/gpu-hpc-research-guide#四、证据锚点及结论边界]]。

## 稳定知识

### 核心概念

四页不是对称的四选一，而是**一页对象层 + 三页元层**：前者回答「算得对不对」，后三者回答「怎么切、怎么说、怎么量」。写任何 GPU/HPC 结论前，用前者定正确性，用后三者定表述边界。

**代数事实（对象层）**

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[distributed-operator-and-shared-dofs]] | 分布式有限元算子的第一原理：单元分区、共享自由度、同步归约、重叠加权内积与全局解收集的正确性不变量 | complete |

⚠️ 该页只覆盖**进程级（MPI）**的代数正确性，实为 [[parallel-levels]]「进程层」一格的完整展开，与下面三页不同层级；$\mathbf{K}_{\mathrm{loc}}$ 在其中是黑盒。

**执行与度量规范（元层）**

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[parallel-levels]] | 并行的三个层级：进程（MPI）、线程（节点内共享内存）、设备内（SIMT）各自切什么、撞什么墙；与装配层级正交的第二坐标轴 | in-progress |
| [[heterogeneous-execution-modes]] | 异构实现的四维分类与措辞规范：硬件拓扑、执行层级、编程模型、数据/精度；六种硬件拓扑是三层并行粒度的开关组合，另附各配置的外推边界 | complete |
| [[performance-model]] | 端到端性能模型与测量口径：五级计时边界、强弱扩展、Roofline、异构与通信口径及最小可复现性能记录 | in-progress |

### 参考库架构

主要参考库（FEALPy 4.0 与 MFEM）的 GPU/MPI 设计分析，为理解分类体系与实施提供参照。

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[reference-libraries/fealpy-architecture]] | FEALPy 架构：多后端抽象（BackendManager 运行时对象分派）与 GPU 执行路径（PyTorch/Taichi 可用，CuPy 为占位实现），含 EMPI 轻量分布式层（早期实现） | draft |
| [[reference-libraries/mfem-architecture]] | MFEM 架构：Device/forall 编译期宏展开 + 运行时分派、Par* 对象体系与多后端×MPI 混合架构 | draft |

## 分布式系统的三层解耦

> 本节只提供主题地图；不复制三层模型的完整对比表、通信协议、正确性证明或程序实测数字。

```text
L1 代数/算法层 (Math & What)        限制/延拓算子、双重向量表示、一致化投影 C 与同步归约 S、重叠加权内积
        |
L2 软件框架接口层 (Software API)    EMPI EntityMPI / PETSc DM / MFEM ParFiniteElementSpace、算子封装
        |
L3 硬件/HPC 执行层 (Hardware & How) Host/Device 内存、GPU-aware MPI 与 GPUDirect、Kernel 打包与多 Stream 重叠
```

数学正确性只由 L1 保证，性能只由 L3 决定，二者必须解耦——L3 的任何优化都不得改变 L1 的结果。三条强制原则：

1. **代数层错了，硬件层再快也是错的**：MatVec 遗漏归约 $\mathcal{S}$ 或内积未按引用计数去重时，必须先在单进程下验证代数正确性，再谈性能。
2. **通信透明**：跨进程同步封装在 `op @ x` 与 `dot(u, v)` 内部，上层求解器不接触 Send/Recv 句柄。
3. **可移植**：L1 代码在 NumPy/PyTorch/JAX 与 CPU/GPU 间零修改，L3 动态匹配传输通道。

验证门禁按层分开：L1 看 $P$-rank 与 1-rank 结果是否在浮点精度内一致，L3 看强/弱扩展与通信-计算重叠率。L1 的代数定义由 [[distributed-operator-and-shared-dofs]] 维护，L2 的通信子与三种通信模式见 [[parallel-levels]]，L3 的分类由 [[heterogeneous-execution-modes]] 维护。

⚠️ **本节的三层是职责分层，不是并行粒度分层。** [[parallel-levels]] 的三层（进程/线程/设备内）回答「计算切在哪儿」，本节的 L1/L2/L3 回答「这处改动归谁管」。两者同名不同义，引用时必须写全，不可互相替代。

### 程序实现必读入口

启动或讨论 SOPTX 中的 GPU/MPI 程序实现前，按下表进入相应的数学、工程与代码事实源；本页只提供阅读顺序和职责路由。

| 入口 | 职责 |
|---|---|
| [[distributed-operator-and-shared-dofs]] | L1 的数学事实源：单元分区、共享自由度、同步归约、加权内积与全局解收集的正确性不变量。 |
| [[heterogeneous-execution-modes]] | L3 的分类体系：硬件拓扑、执行层级、编程模型与数据/精度策略四个正交维度。 |
| [[parallel-levels]] | 动手写并行代码前先定坐标：这次要切进程、线程还是设备内，该层的断点与墙分别是什么。 |
| [[performance-model]] | 跑出任何性能数字前的测量口径：五级计时边界、预热与同步语义、Roofline 判断与最小可复现记录。 |
| [[reference-libraries/fealpy-architecture]]、[[reference-libraries/mfem-architecture]] | 两个参考库分别如何落实 L2/L3；实施前的对照对象。 |
| [[../../research/piml-matrix-free-gpu/gpu-hpc-research-guide]] | 研究目标、性能边界、证据锚点与阶段门禁。 |

关联实现：SOPTX `examples/gpu_elasticity/`，维护 GPU 正确性对比与性能 benchmark；具体入口与运行方式见该目录文档，当前已跑通的范围与其证据边界以 [[../../research/piml-matrix-free-gpu/gpu-hpc-research-guide#四、证据锚点及结论边界]] 为准。跨仓库路径一律使用 `repo:path` 相对写法，不写机器绝对路径。

## 项目与分支入口

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[../../research/piml-matrix-free-gpu/gpu-hpc-research-guide]] | 研究目标、性能边界、国内外现状、证据锚点与阶段门禁 | in-progress |
| [[../../research/piml-matrix-free-gpu/_index]] | 以 GPU/HPC 横向支撑三条推进线的博士后核心研究项目入口 | in-progress |
| [[../../research/piml-matrix-free-gpu/project-plan]] | 三个项目分支组合后的方法关系、开放问题与研究切入点 | in-progress |

## 文献证据

- [[../../research/piml-matrix-free-gpu/gpu-hpc-research-guide#四、证据锚点及结论边界]] — GPU 拓扑优化、Matrix-Free GPU、高阶可移植计算、国内近期异构路线及核心证据矩阵。
- [[../../literature/_index#当前 ingest 队列]] — GPU/HPC 当前阅读对象和唯一 `to-ingest` 状态入口。
- [[../../literature/topopt/gpu-hpc/translations/Ma2026-highperformanceparallel-zh]] — 当前可核实的团队 HPC 正式节点：PIML 降维、CPU/MPI 分布式并行、PETSc 多重网格与完整优化流程并行化。
- [Williams, Waterman & Patterson 2009](https://doi.org/10.1145/1498765.1498785) — Roofline 性能模型。

## 关联入口

- 关联主题：[[../piml/_index]] — PIML 局部力学表示、批量推理需求与当前研究入口。
- 关联主题：[[../matrix-free/_index]] — Matrix-Free 装配层次、算子原语与当前研究入口。
- 工作汇报：[[../../entities/guo-xu/first-formal-work-report|郭旭老师第一次工作汇报]] — 面向郭旭老师的 PIML–Matrix-Free–GPU 研究衔接与下一步请教；页面明确当前尚无基于统一算例的 GPU 正式结果，不作为 GPU 实现或性能 evidence 的事实源。
- 历史档案：[[../../archive/2026-postdoc-entry-assessment/README]] — 2026 年博士后入站考核答辩的历史材料总览，其中包含当时的 GPU/HPC 计划和表达；档案不再维护当前研究事实。

## 管理边界

- 三层解耦框架与通信正确性由本页「分布式系统的三层解耦」节与 [[distributed-operator-and-shared-dofs]] 维护，计时边界、扩展性与可复现记录口径由 [[performance-model]] 维护，单篇论文事实由 `literature/` 维护，实测性能数字由 `research/piml-matrix-free-gpu/gpu-hpc-research-guide` 及 SOPTX 对应结果文档维护。
- 不在稳定知识页维护当前任务状态、个人原型进度和预计日期；这些由 `research/` 维护。
- 工作汇报只保存当次实际表达，历史档案只保存事件发生时的材料；二者都不反向覆盖当前实现和性能事实。
- 不把单个 kernel 或 MatVec 加速直接表述为完整 solve 或完整优化流程加速。
- 不把某一并行层级的加速或扩展性结论外推到另一层级；引用「并行」时必须写明是进程、线程还是设备内。
- 不把 CPU/MPI 结果写成 GPU 结果，也不把尚未实现的多 GPU、GPU-aware MPI 或多节点路线写成既有能力。
- 新成果只有在论文、预印本、专利或公开软件等来源可核实时，才进入正式时间线。
- 本页不维护固定文件数，也不登记只因索引、日志、参考文献或顺带讨论而命中 GPU/HPC 的全部文件。
