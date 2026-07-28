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
date_update: 2026-07-26
---

# GPU/HPC 主题入口

> 本页是 GPU/HPC 的统一语义入口：稳定性能口径与公开成果谱系放在 `concepts/gpu-hpc/`，单篇论文事实放在 `literature/`，当前能力、任务路线与阶段门禁放在 `research/technical-lines/`。

## 稳定知识

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[performance-model]] | 从 kernel 到完整任务的计时边界、Roofline、扩展效率与可复现性能记录协议 | in-progress |
| [[method-lineage]] | 郭旭老师团队公开 HPC 成果的纳入标准与演进；当前正式节点为 Ma2026 的 CPU/MPI 并行实现 | draft |

## 当前研究

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[../../research/technical-lines/gpu-hpc-research-guide]] | 当前已有基础、目标差距、实施路线与阶段门禁 | in-progress |

## 核心文献

- [[../../literature/topology-opt/Ma2026-highperformanceparallel]] — 当前可核实的团队 HPC 正式节点：PIML 降维、CPU/MPI 分布式并行、PETSc 多重网格与完整优化流程并行化。
- [Williams, Waterman & Patterson 2009](https://doi.org/10.1145/1498765.1498785) — Roofline 性能模型。

## 关联主题

- [[../piml/_index]] — PIML 局部力学表示、批量推理需求与当前研究入口。
- [[../matrix-free/_index]] — Matrix-Free 装配层次、算子原语与当前研究入口。

## 边界

- 不记录单篇论文完整摘要和实验细节；这些由 `literature/` 维护。
- 不在稳定知识页维护当前任务状态、个人原型进度和预计日期；这些由 `research/` 维护。
- 不把单个 kernel 或 MatVec 加速直接表述为完整 solve 或完整优化流程加速。
- 不把 CPU/MPI 结果写成 GPU 结果，也不把尚未实现的多 GPU、GPU-aware MPI 或多节点路线写成既有能力。
