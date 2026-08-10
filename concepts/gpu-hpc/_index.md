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
date_update: 2026-08-10
---

# GPU/HPC 主题入口

> 本页是 GPU/HPC 的统一语义入口：稳定性能口径与公开成果谱系放在 `concepts/gpu-hpc/`，单篇论文事实放在 `literature/`，当前能力、任务路线与阶段门禁放在 `research/technical-lines/`，面向导师/合作者的科研讨论与阶段表达放在 `discussions/`，已完成事件的历史材料放在 `archive/`。

**命名边界**：本主题名为 GPU/HPC，实际覆盖 GPU 卸载、CPU/MPI 对照、多 GPU、GPU-aware MPI 与端到端性能工程，即广义异构高性能计算；不代表全部 HPC 领域（调度、存储、数据中心等不在本主题范围），也不代表团队已有 GPU 成果——公开成果谱系见 [[method-lineage]]。

## 稳定知识

### 核心概念

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[heterogeneous-execution-modes]] | GPU 异构并行实现方式的分类体系：硬件拓扑、执行层级、编程模型与数据/精度策略四个正交维度 | draft |
| [[distributed-algebra-and-execution-decoupling]] | 分布式计算系统的代数/算法层与硬件/执行层解耦框架：三层设计模型、两个层面深度对比与本库核心三柱全景地图 | complete |
| [[distributed-operator-and-shared-dofs]] | 分布式有限元算子的第一原理：单元分区、共享自由度、同步归约、重叠加权内积与全局解收集的正确性不变量 | complete |
| [[performance-model]] | 端到端性能模型与测量口径：五级计时边界、强弱扩展、Roofline、异构与通信口径及最小可复现性能记录 | in-progress |
| [[method-lineage]] | 郭旭老师团队公开 HPC 成果的纳入标准与演进；当前正式节点为 Ma2026 的 CPU/MPI 并行实现 | draft |

### 参考库架构

主要参考库（FEALPy 4.0 与 MFEM）的 GPU/MPI 设计分析，为理解分类体系与实施提供参照。

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[reference-libraries/fealpy-architecture]] | FEALPy 架构：多后端抽象（BackendManager 运行时对象分派）与 GPU 执行路径（PyTorch/Taichi 可用，CuPy 为占位实现），含 EMPI 轻量分布式层（早期实现） | draft |
| [[reference-libraries/mfem-architecture]] | MFEM 架构：Device/forall 编译期宏展开 + 运行时分派、Par* 对象体系与多后端×MPI 混合架构 | draft |
| [[reference-libraries/fealpy-mfem-gpu-backend-comparison]] | 两个主要参考库的 GPU 后端设计对比：同为可移植后端类的两种实现层次 | draft |

## 分布式系统的三层解耦

> 本节只提供主题地图；不复制三层模型的完整对比表、通信协议、正确性证明或程序实测数字。

```text
L1 代数/算法层 (Math & What)        限制/延拓算子、双重向量表示、一致化投影 C 与同步归约 S、重叠加权内积
        |
L2 软件框架接口层 (Software API)    EMPI EntityMPI / PETSc DM / MFEM ParFiniteElementSpace、算子封装
        |
L3 硬件/HPC 执行层 (Hardware & How) Host/Device 内存、GPU-aware MPI 与 GPUDirect、Kernel 打包与多 Stream 重叠
```

数学正确性只由 L1 保证，性能只由 L3 决定，二者必须解耦——L3 的任何优化都不得改变 L1 的结果。三层的完整定义、深度对比与强制解耦原则由 [[distributed-algebra-and-execution-decoupling]] 维护。

### 程序实现必读入口

启动或讨论 SOPTX 中的 GPU/MPI 程序实现前，按下表进入相应的数学、工程与代码事实源；本页只提供阅读顺序和职责路由。

| 入口 | 职责 |
|---|---|
| [[distributed-algebra-and-execution-decoupling]] | 三层设计模型与强制解耦原则；判断一处改动属于哪一层的依据。 |
| [[distributed-operator-and-shared-dofs]] | L1 的数学事实源：单元分区、共享自由度、同步归约、加权内积与全局解收集的正确性不变量。 |
| [[heterogeneous-execution-modes]] | L3 的分类体系：硬件拓扑、执行层级、编程模型与数据/精度策略四个正交维度。 |
| [[performance-model]] | 跑出任何性能数字前的测量口径：五级计时边界、预热与同步语义、Roofline 判断与最小可复现记录。 |
| [[reference-libraries/fealpy-architecture]]、[[reference-libraries/mfem-architecture]] | 两个参考库分别如何落实 L2/L3；实施前的对照对象。 |
| [[../../research/technical-lines/gpu-hpc-research-guide]] | 研究目标、性能边界、证据锚点与阶段门禁。 |

关联实现：SOPTX `examples/gpu_elasticity/`，维护 GPU 正确性对比与性能 benchmark；具体入口与运行方式见该目录文档，当前已跑通的范围与其证据边界以 [[../../research/technical-lines/gpu-hpc-research-guide#四、证据锚点及结论边界]] 为准。跨仓库路径一律使用 `repo:path` 相对写法，不写机器绝对路径。

## 项目与技术线入口

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[../../research/technical-lines/gpu-hpc-research-guide]] | 研究目标、性能边界、国内外现状、证据锚点与阶段门禁 | in-progress |
| [[../../research/piml-matrix-free-gpu/_index]] | 以 GPU/HPC 横向支撑 WP1–WP3 的博士后核心研究项目入口 | in-progress |
| [[../../research/piml-matrix-free-gpu/high-performance-solver-survey]] | 三条技术线组合后的方法关系、开放问题与研究切入点 | in-progress |

## 文献证据

- [[../../research/technical-lines/gpu-hpc-research-guide#四、证据锚点及结论边界]] — GPU 拓扑优化、Matrix-Free GPU、高阶可移植计算、国内近期异构路线及核心证据矩阵。
- [[../../literature/_index#当前 ingest 队列]] — GPU/HPC 当前阅读对象和唯一 `to-ingest` 状态入口。
- [[../../literature/topology-opt/notes/Ma2026-highperformanceparallel]] — 当前可核实的团队 HPC 正式节点：PIML 降维、CPU/MPI 分布式并行、PETSc 多重网格与完整优化流程并行化。
- [Williams, Waterman & Patterson 2009](https://doi.org/10.1145/1498765.1498785) — Roofline 性能模型。

## 关联入口

- 关联主题：[[../piml/_index]] — PIML 局部力学表示、批量推理需求与当前研究入口。
- 关联主题：[[../matrix-free/_index]] — Matrix-Free 装配层次、算子原语与当前研究入口。
- 工作汇报：[[../../discussions/guo-xu/first-formal-work-report]] — 面向郭旭老师的 PIML–Matrix-Free–GPU 研究衔接与下一步请教；页面明确当前尚无基于统一算例的 GPU 正式结果，不作为 GPU 实现或性能 evidence 的事实源。
- 历史档案：[[../../archive/2026-postdoc-entry-assessment/README]] — 2026 年博士后入站考核答辩的历史材料总览，其中包含当时的 GPU/HPC 计划和表达；档案不再维护当前研究事实。

## 管理边界

- 三层解耦框架与通信正确性由 [[distributed-algebra-and-execution-decoupling]]、[[distributed-operator-and-shared-dofs]] 维护，计时边界、扩展性与可复现记录口径由 [[performance-model]] 维护，单篇论文事实由 `literature/` 维护，实测性能数字由 `research/technical-lines/gpu-hpc-research-guide` 及 SOPTX 对应结果文档维护。
- 不在稳定知识页维护当前任务状态、个人原型进度和预计日期；这些由 `research/` 维护。
- 工作汇报只保存当次实际表达，历史档案只保存事件发生时的材料；二者都不反向覆盖当前实现和性能事实。
- 不把单个 kernel 或 MatVec 加速直接表述为完整 solve 或完整优化流程加速。
- 不把 CPU/MPI 结果写成 GPU 结果，也不把尚未实现的多 GPU、GPU-aware MPI 或多节点路线写成既有能力。
- 新成果只有在论文、预印本、专利或公开软件等来源可核实时，才进入正式时间线。
- 本页不维护固定文件数，也不登记只因索引、日志、参考文献或顺带讨论而命中 GPU/HPC 的全部文件。
