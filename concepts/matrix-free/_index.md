---
title: "Matrix-Free 主题入口"
type: index
tags:
  - matrix-free
  - finite-element
status: draft
date_added: 2026-07-26
date_update: 2026-07-29
---

# Matrix-Free 主题入口

> 本页是 Matrix-Free 的统一语义入口：稳定方法理解与公开成果谱系放在 `concepts/matrix-free/`，单篇论文事实放在 `literature/`，当前能力、任务路线与验收放在 `research/technical-lines/`。

## 稳定知识

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[assembly-levels]] | Matrix-Free 五级装配层次、跨框架术语和判定边界 | in-progress |
| [[distributed-operator-and-shared-dofs]] | MPI 单元分区、共享自由度、同步归约与分布式 MatVec 的统一数学描述 | in-progress |
| [[method-lineage]] | 郭旭老师团队公开 Matrix-Free 相关成果的方法谱系；当前直接节点为 Ma2026 | draft |

## 当前研究

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[../../research/technical-lines/matrix-free-research-guide]] | 当前已有能力、目标差距、实施路线与阶段门禁 | in-progress |

## 关联实现

- `soptx:examples/matrix_free_elasticity_3d/README.md#理论代码对应` — 当前个人研究的可执行线弹性基线；源码、运行方式和验证事实由 SOPTX 维护。

## 核心文献

- [[../../literature/topology-opt/Ma2026-highperformanceparallel]] — 当前唯一经证实、明确使用 `matrix-free` 表述的团队论文。

## 关联主题

- [[../linear-elasticity]] — 当前三维参考问题的连续模型、变分形式和有限元离散基础。
- [[../piml/_index]] — PIML 稳定知识、方法谱系与当前研究入口。
- [[../gpu-hpc/_index]] — GPU/HPC 端到端性能模型、公开成果谱系与当前研究入口。

## 边界

- 不复制单篇论文的完整摘要、实验数字和公式推导；这些由 `literature/` 维护。
- 不记录当前任务状态、实施阶段或预计交付日期；这些由 `research/` 维护。
- 不把 PIML 前序论文直接标为 Matrix-Free 成果，也不把尚未公开的设想写成团队既有路线。
- 新成果只有在论文、预印本、专利或公开软件等来源可核实时，才进入正式时间线。
