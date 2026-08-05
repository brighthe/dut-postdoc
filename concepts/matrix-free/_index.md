---
title: "Matrix-Free 主题入口"
type: index
tags:
  - matrix-free
  - finite-element
status: draft
date_added: 2026-07-26
date_update: 2026-08-04
---

# Matrix-Free 主题入口

> 本页是 Matrix-Free 的统一语义入口：稳定方法理解与公开成果谱系放在 `concepts/matrix-free/`，单篇论文事实放在 `literature/`，当前能力、任务路线与验收放在 `research/technical-lines/`，面向导师的阶段表达放在 `work-reports/`，已完成事件的历史材料放在 `archive/`。

## 稳定知识

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[assembly-levels]] | Matrix-Free 五级装配层次、跨框架术语和判定边界 | in-progress |
| [[distributed-operator-and-shared-dofs]] | MPI 单元分区、共享自由度、同步归约与分布式 MatVec 的统一数学描述 | in-progress |
| [[method-lineage]] | 郭旭老师团队公开 Matrix-Free 相关成果的方法谱系；当前直接节点为 Ma2026 | draft |

## 当前研究

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[../../research/technical-lines/matrix-free-research-guide]] | 长期目标、能力边界、阶段模型、统一验收原则与当前任务状态 | in-progress |
| [[../../research/piml-matrix-free-gpu/_index]] | 以 GPU 加速 Matrix-Free 求解为核心内容之一的博士后核心研究项目入口 | in-progress |
| [[../../research/piml-matrix-free-gpu/high-performance-solver-survey]] | 三条技术线组合后的方法关系、开放问题与研究切入点 | in-progress |

## 工作汇报

- [[../../work-reports/guo-xu/first-formal-work-report]] — 面向郭旭老师的第一次正式工作汇报，保存本次实际要汇报的 Matrix-Free 阶段结果、事实边界和待请教问题；它是阶段表达快照，不是内部任务状态、程序实现或数值 evidence 的事实源。

## 文献证据

- [[../../literature/matrix-free/_index]] — 以 Matrix-Free 方法为主要贡献的实际文献、译文与交叉主题入口。
- [[../../literature/matrix-free/notes/Kronbichler2012-parallel-cell-operator]] — 并行 cell-based 有限元算子应用的 `draft` 骨架；当前仅按正式摘要使用证据，中文译文待完成。
- [[../../literature/_index#当前 ingest 队列]] — 尚未建立单篇笔记的 Matrix-Free 论文和储备候选入口。
- [[../../literature/topology-opt/notes/Ma2026-highperformanceparallel]] — 当前唯一经证实、明确使用 `matrix-free` 表述的团队论文。

## 关联实现

- `soptx:examples/matrix_free_elasticity/README.md` — 当前个人研究的二维、三维可执行线弹性基线；源码、运行方式和验证事实由 SOPTX 维护。

## 历史档案

- [[../../archive/2026-postdoc-entry-assessment/README]] — 2026 年博士后入站考核答辩的历史材料总览，其中包含当时的 Matrix-Free 计划、图件和表达；档案不再维护当前研究事实，不在本页逐一列出内部文件。

## 关联主题

- [[../linear-elasticity]] — 当前三维参考问题的连续模型、变分形式和有限元离散基础。
- [[../piml/_index]] — PIML 稳定知识、方法谱系与当前研究入口。
- [[../gpu-hpc/_index]] — GPU/HPC 端到端性能模型、公开成果谱系与当前研究入口。

## 管理边界

- 不复制单篇论文的完整摘要、实验数字和公式推导；这些由 `literature/` 维护。
- 不在概念页维护当前任务状态、实施阶段或预计交付日期；这些只由 [[../../research/technical-lines/matrix-free-research-guide#五、阶段门禁与当前执行状态]] 维护。
- 不从工作汇报或历史档案反向覆盖概念定义、当前任务状态和工程 evidence；汇报只保存阶段表达，档案只保存历史语境。
- 不把 PIML 前序论文直接标为 Matrix-Free 成果，也不把尚未公开的设想写成团队既有路线。
- 新成果只有在论文、预印本、专利或公开软件等来源可核实时，才进入正式时间线。
- 本页按职责列出 Matrix-Free 的权威入口，不维护容易过期的文件总数，也不登记只因索引、日志、参考文献或顺带讨论而命中关键词的全部文件。
