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
date_update: 2026-08-03
---

# GPU/HPC 主题入口

> 本页是 GPU/HPC 的统一语义入口：稳定性能口径与公开成果谱系放在 `concepts/gpu-hpc/`，单篇论文事实放在 `literature/`，当前能力、任务路线与阶段门禁放在 `research/technical-lines/`，面向导师的阶段表达放在 `work-reports/`，已完成事件的历史材料放在 `archive/`。

## 稳定知识

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[performance-model]] | 从 kernel 到完整任务的计时边界、Roofline、扩展效率与可复现性能记录协议 | in-progress |
| [[method-lineage]] | 郭旭老师团队公开 HPC 成果的纳入标准与演进；当前正式节点为 Ma2026 的 CPU/MPI 并行实现 | draft |

## 当前研究

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[../../research/technical-lines/gpu-hpc-research-guide]] | 研究目标、性能边界、国内外现状、证据锚点与阶段门禁 | in-progress |
| [[../../research/piml-matrix-free-gpu/_index]] | 以 GPU/HPC 横向支撑 WP1–WP3 的博士后核心研究项目入口 | in-progress |
| [[../../research/piml-matrix-free-gpu/high-performance-solver-survey]] | 三条技术线组合后的方法关系、开放问题与研究切入点 | in-progress |

## 工作汇报

- [[../../work-reports/guo-xu/first-formal-work-report]] — 面向郭旭老师的 PIML–Matrix-Free–GPU 研究衔接与下一步请教；页面明确当前尚无基于统一算例的 GPU 正式结果，不作为 GPU 实现或性能 evidence 的事实源。

## 文献证据

- [[../../research/technical-lines/gpu-hpc-research-guide#四、证据锚点及结论边界]] — GPU 拓扑优化、Matrix-Free GPU、高阶可移植计算、国内近期异构路线及核心证据矩阵。
- [[../../literature/_index#当前 ingest 队列]] — GPU/HPC 当前阅读对象和唯一 `to-ingest` 状态入口。
- [[../../literature/topology-opt/notes/Ma2026-highperformanceparallel]] — 当前可核实的团队 HPC 正式节点：PIML 降维、CPU/MPI 分布式并行、PETSc 多重网格与完整优化流程并行化。
- [Williams, Waterman & Patterson 2009](https://doi.org/10.1145/1498765.1498785) — Roofline 性能模型。

## 历史档案

- [[../../archive/2026-postdoc-entry-assessment/README]] — 2026 年博士后入站考核答辩的历史材料总览，其中包含当时的 GPU/HPC 计划和表达；档案不再维护当前研究事实。

## 关联主题

- [[../piml/_index]] — PIML 局部力学表示、批量推理需求与当前研究入口。
- [[../matrix-free/_index]] — Matrix-Free 装配层次、算子原语与当前研究入口。

## 管理边界

- 不记录单篇论文完整摘要和实验细节；这些由 `literature/` 维护。
- 不在稳定知识页维护当前任务状态、个人原型进度和预计日期；这些由 `research/` 维护。
- 工作汇报只保存当次实际表达，历史档案只保存事件发生时的材料；二者都不反向覆盖当前实现和性能事实。
- 不把单个 kernel 或 MatVec 加速直接表述为完整 solve 或完整优化流程加速。
- 不把 CPU/MPI 结果写成 GPU 结果，也不把尚未实现的多 GPU、GPU-aware MPI 或多节点路线写成既有能力。
- 本页不维护固定文件数，也不登记只因索引、日志、参考文献或顺带讨论而命中 GPU/HPC 的全部文件。
