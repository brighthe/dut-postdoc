---
title: "长期技术线索引"
topic: "跨研究方向复用的长期技术能力"
tags:
  - technical-line
  - research-guide
  - PIML
  - matrix-free
  - GPU
  - HPC
status: "in-progress"
date_start: 2026-07-21
date_update: 2026-07-21
---

# 长期技术线索引

> 本目录维护不依赖某个阶段性“研究方向编号”的长期技术能力。每份 guide 回答一条技术线“研究对象是什么、当前做到哪里、下一步怎么做、如何验收”；具体科研课题、博士后阶段安排和跨线组合由对应计划与综合页维护。

## 三条技术线

| 技术线 | 指导文档 | 当前定位 |
|---|---|---|
| PIML | [[piml-research-guide]] | 局部力学算子学习、结构保持、误差传播、灵敏度与优化闭环 |
| Matrix-Free | [[matrix-free-research-guide]] | 全局无矩阵算子、Krylov、预条件、Shell Matrix 与规模基线 |
| GPU/HPC | [[gpu-hpc-research-guide]] | GPU 批处理、端到端性能、显存、多后端、MPI 与多节点扩展 |

## 基础概念

- [[../../concepts/matrix-free-assembly-levels]] — Matrix-Free 五级装配层次、MFEM/libCEED 术语映射及项目分类准则。

## 与其他页面的分工

| 页面类型 | 回答的问题 |
|---|---|
| concepts 概念页 | 技术概念是什么、方法谱系如何演化 |
| 本目录 technical-line guide | 我的长期技术能力如何研究、实施和验收 |
| postdoc-plan 与其他课题页 | 当前科研课题如何组合和使用这些技术线 |
| 综合调研与技术 synthesis | 三条线为什么结合、当前总体判断是什么 |
| defense-sprint frame guide | 特定 PPT 帧如何解释、证据和答辩口径是什么 |
| work-reports | 某次面向导师或合作团队实际汇报什么 |

## 维护规则

- 三份 guide 是各技术线的长期第一入口，不从属于固定的“方向一/方向二”编号。
- 每份 guide 同时维护已有基础、事实边界、后续工作、Benchmark、里程碑和风险。
- 项目任务和分工的实时状态仍由对应项目仓库维护；guide 只吸收可复用的方法、指标和结论。
- 跨技术线接口与整体推进顺序由综合页和执行计划维护，单线 guide 不建立第二套总体进度账。
- 更新 guide 后检查对应概念页、综合页、执行计划、工作汇报和本索引是否需要同步。

## 跨线综合入口

- [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-high-performance-solver-survey]] — PIML、Matrix-Free 与高性能求解的综合调研。
- [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-execution-plan]] — 当前博士后计划中的总体工作包与里程碑。
- [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-gpu-and-model-selection-technical-synthesis]] — 当前能力证据、融合路线与模型选型综合。
- [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] — 2026-07 面向郭旭老师的完整工作汇报。
