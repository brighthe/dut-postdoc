---
title: "郭旭老师团队 GPU/HPC 方法谱系"
type: concept
aliases:
  - GPU/HPC method lineage
  - 郭旭团队高性能计算方法演进
tags:
  - GPU
  - HPC
  - method-lineage
  - MPI
  - PIML
  - topology-opt
status: draft
date_added: 2026-07-26
date_update: 2026-08-03
---

# 郭旭老师团队 GPU/HPC 方法谱系

> **一句话**：截至 2026-07-26，当前公开且可核实的正式 HPC 节点为 Ma2026 的 CPU/MPI 并行 PIML 拓扑优化；尚无足够公开证据把 GPU、异构计算、多 GPU 或 GPU-aware MPI 登记为团队既有成果。

## 1. 范围与纳入标准

本页长期记录郭旭老师团队公开 GPU/HPC 成果如何演进。正式时间线只纳入满足以下条件之一、且能核对计算对象和性能边界的成果：

- 正式论文或可公开核实的预印本；
- 已公开专利；
- 具有公开说明、可核实实现边界和性能口径的软件成果。

每个节点必须回答：

1. 并行对象是局部构造、线性求解、灵敏度、过滤、优化器还是完整流程；
2. 使用 CPU、线程、MPI、GPU、多 GPU 或异构节点中的哪些资源；
3. 性能数据对应 kernel、MatVec、solve、优化迭代还是完整任务；
4. 是否同时报告正确性、内存、通信和强弱扩展；
5. 哪些能力仍未实现或未公开。

个人原型、公司内部工程、尚未公开设想和缺少来源的结果不进入正式时间线；它们的当前能力证据由 [[../../research/technical-lines/gpu-hpc-research-guide]] 管理。

## 2. 与 PIML、Matrix-Free 谱系的关系

Huang 2022—2024 建立了 PIML 局部力学表示、子结构缩聚和 data-free 训练基础，完整关系见 [[../piml/method-lineage]]。这些工作降低了局部构造和全局分析成本，是后续高性能实现的算法基础，但不能仅凭大规模算例或潜在并行性重复登记为正式 HPC 节点。

Ma2026 同时属于三种语境：

- 在 PIML 谱系中，它是并行与按需预测的大规模实现节点；
- 在 Matrix-Free 谱系中，它采用多尺度形函数按需预测/释放，但全局粗网格缩聚矩阵仍组装，见 [[../matrix-free/method-lineage]]；
- 在本页中，它是当前正式的 CPU/MPI 高性能并行节点。

三个谱系分别回答学习方法、算子存储层次和并行执行三个正交问题，不相互替代。

## 3. 当前时间线

| 时间 | 代表成果 | 并行与硬件 | HPC 贡献 | 证据状态 |
|---|---|---|---|---|
| 2026 | [[../../literature/topology-opt/notes/Ma2026-highperformanceparallel]] | CPU 集群、MPI、PETSc 多重网格 | PIML 子结构降维、分布式划分、粗网格求解、位移恢复、灵敏度、PDE 滤波和 MMA 的完整流程并行；报告强弱扩展 | 已核实 |

当前只有一个正式节点，不能据此表述为团队已经形成公开的 GPU 或异构并行连续路线。

## 4. Ma2026：CPU/MPI 完整优化流程并行

Ma2026 将 PIML 子结构降维与分布式并行结合：

```text
设计域与子结构分区
  → 局部缩聚 / PIML 形函数预测
  → 粗网格全局矩阵组装
  → PETSc MG 预处理 GMRES
  → 细网格位移恢复与灵敏度
  → PDE 滤波与并行 MMA
```

其 HPC 贡献包括：

- 按子结构分配局部工作，降低每个 MPI rank 的计算与存储负担；
- 并行化粗网格求解之外的恢复、灵敏度、过滤和设计更新，覆盖完整优化流程；
- 使用多尺度形函数按需预测/释放进行时间—空间权衡；
- 报告 CPU 集群上的强扩展、弱扩展和大规模算例。

其边界包括：

- 当前公开实现基于 CPU/MPI，不是 GPU 或 CPU+GPU 异构实现；
- 粗网格全局缩聚矩阵仍形成和组装；
- 尚未公开多 GPU、GPU-aware MPI 或 GPU kernel 的端到端验证；
- 公开扩展结果不能直接迁移为其他 PDE、离散、硬件或计时边界下的结论。

## 5. 个人工程证据不进入公开谱系

soptx 的单次 GPU MatVec 与 `mfleo` 的单 GPU + 单 CPU 核端到端 CG 是本人已有工程基础，可支持后续研究实施，但它们不是郭旭老师团队公开成果，也不是同一套 PIML × Matrix-Free × GPU 系统。

因此本页不登记其性能数字；当前状态、准确读法和后续门禁统一由 [[../../research/technical-lines/gpu-hpc-research-guide]] 维护。

## 6. 长期观察维度

后续出现公开成果时，按以下维度追加：

| 维度 | 需要回答的问题 |
|---|---|
| 执行层级 | 加速的是 kernel、MatVec、solve、优化迭代还是完整任务？ |
| 并行模型 | 使用线程、MPI、GPU、多 GPU、任务并行还是混合模型？ |
| 数值对象 | 覆盖 PIML、Matrix-Free、预条件、恢复、灵敏度、过滤和优化器中的哪些环节？ |
| 数据与通信 | 如何处理 batch、缓存、搬移、halo exchange、归约、粗网格和负载均衡？ |
| 正确性 | 是否同时报告残差、响应误差、灵敏度和最终拓扑？ |
| 性能证据 | 是否给出绝对时间、内存、通信、强弱扩展和可复现配置？ |

## 7. 当前公开空白

截至 2026-07-26，在当前已核实的团队公开成果中，尚未确认以下环节已经闭合：

- PIML 批量推理与局部算子作用的一体化 GPU 管线；
- Matrix-Free 主算子、Krylov 和预条件的端到端 GPU 求解；
- 恢复、灵敏度、过滤和优化器的完整 GPU 化；
- 多 GPU、GPU-aware MPI 和多节点异构扩展；
- 跨设备、跨后端和跨提交的性能回归体系。

这些是公开成果谱系中的空白，不等于团队内部不存在尚未公开的研究。

## 8. 更新规则

- 新成果先建立或更新对应 `literature/` 笔记，再从本页引用。
- 每个节点必须同时记录硬件、并行模型、测量层级、正确性和未覆盖范围。
- 单 kernel、单 MatVec 和端到端结果分开登记，不允许跨层外推。
- 本人的任务、实施顺序、工程原型和阶段门禁只更新 research guide。

## 9. 来源与相关页面

- [[../../literature/topology-opt/notes/Ma2026-highperformanceparallel]] — 论文方法、CPU/MPI 强弱扩展、完整优化流程和边界。
- [Ma et al., 2026, Acta Mechanica Sinica](https://doi.org/10.1007/s10409-025-25942-x) — 出版社 DOI 入口。
- [[../piml/method-lineage]] — PIML 前序方法谱系。
- [[../matrix-free/method-lineage]] — Matrix-Free 存储策略与全局装配边界。
- [[performance-model]] — 计时层级、性能模型和可复现记录口径。
- [[../../research/technical-lines/gpu-hpc-research-guide]] — 当前研究目标、证据边界与阶段门禁。
