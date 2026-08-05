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
date_update: 2026-08-04
---

# 长期技术线索引

> 本目录维护可跨项目复用的长期技术能力。博士后阶段三条技术线当前优先服务 [[../piml-matrix-free-gpu/project-plan|核心研究项目]]：Matrix-Free 与 GPU/HPC 支撑 WP1，PIML 与 GPU/HPC 支撑 WP2，三线共同支撑满足门禁后的 WP3。每份 guide 只回答单线能力、阶段和验收边界；项目目标、工作包和总体顺序不在本目录重复维护。

## 三条技术线

| 技术线 | 指导文档 | 当前定位 |
|---|---|---|
| PIML | [[piml-research-guide]] | 当前优先服务 WP2；PIML 指 Problem-Independent Machine Learning，维护局部力学表示、二维／三维结构检查、全局评价、阶段门禁与当前动作 |
| Matrix-Free | [[matrix-free-research-guide]] | 当前优先服务 WP1，并为 WP3 提供全局算子接口；长期路线与当前任务统一由 guide 维护 |
| GPU/HPC | [[gpu-hpc-research-guide]] | 横向服务 WP1–WP3；维护异构执行、计时边界和端到端性能门禁 |

研究执行、训练、记录与验收流程统一见 [[../workflows/_index]]，不在本目录维护具体 workflow 正文。

## 基础概念

- [[../../concepts/piml/_index]] — 项目 PIML 的 Problem-Independent 正式释义及 Physics-Informed 外部方法背景边界。
- [[../../concepts/piml/mathematical-foundations]] — Problem-Independent 路线的问题无关性、局部映射与子结构缩聚学习映射。
- [[../../concepts/piml/method-lineage]] — 郭旭老师团队公开 PIML 成果的演进与事实边界。
- [[../../concepts/matrix-free/assembly-levels]] — Matrix-Free 五级装配层次、MFEM/libCEED 术语映射及跨框架分类准则。
- [[../../concepts/matrix-free/method-lineage]] — 郭旭老师团队公开 Matrix-Free 相关成果的演进、纳入标准和事实边界。
- [[../../concepts/gpu-hpc/performance-model]] — GPU/HPC 五级计时边界、Roofline、强弱扩展与可复现性能记录协议。
- [[../../concepts/gpu-hpc/method-lineage]] — 郭旭老师团队公开 HPC 成果的演进、纳入标准和 GPU/异构事实边界。

## 与其他页面的分工

| 页面类型 | 回答的问题 |
|---|---|
| concepts 概念页 | 技术概念是什么、方法谱系如何演化 |
| 本目录 technical-line guide | 我的长期技术能力如何研究、实施和验收 |
| 课题主题页（`research/piml-matrix-free-gpu/`、`research/mmc-mmv/`） | 当前科研问题如何组合技术线或形成跨论文研究判据 |
| 综合调研与技术 synthesis | 三条线为什么结合、当前总体判断是什么 |
| archive 事件档案 | 已完成报告当时如何解释、使用哪些证据和答辩口径；不再维护当前研究事实 |
| work-reports | 某次面向导师或合作团队实际汇报什么 |

## 维护规则

- 三份 guide 是各技术线的长期第一入口，不从属于固定的“方向一/方向二”编号。
- 每份 guide 可以维护当前能力基线、长期目标、事实边界、阶段模型、验收原则、风险和必要的当前执行状态；不复制软件仓库中的逐项工程 Todo。
- 需要连续跟踪的任务状态、推进顺序和完成记录集中维护在本表指定的 guide 或项目事实源；同一技术线不得建立第二套状态账。
- 项目任务和分工的实时状态仍由对应项目仓库维护；guide 只吸收可复用的方法、指标和结论。
- 跨技术线接口与整体推进顺序由对应课题入口或综合页维护，单线 guide 不建立第二套总体进度账。
- 更新 guide 后检查对应概念页、课题入口、综合页、工作汇报和本索引是否需要同步。

## 跨线综合入口

- [[../piml-matrix-free-gpu/_index]] — 博士后核心研究项目统一入口。
- [[../piml-matrix-free-gpu/project-plan]] — 项目目标、WP1–WP3、两年阶段和总体推进顺序。
- [[../piml-matrix-free-gpu/high-performance-solver-survey]] — PIML、Matrix-Free 与 GPU 三线交叉的证据成熟度、耦合机制、研究假设、统一研究方案与验证协议。
- [[../../work-reports/guo-xu/first-formal-work-report]] — 面向郭旭老师的第一次正式工作汇报。
