---
title: "博士后核心研究项目入口"
topic: "PIML Matrix-Free 求解与 GPU 协同加速"
aliases:
  - "PIML × Matrix-Free × GPU 融合课题入口"
  - research/piml-matrix-free
  - integration-guide
  - research/piml-matrix-free-gpu/integration-guide
  - piml-matrix-free-gpu-and-model-selection-technical-synthesis
  - research/piml-matrix-free/piml-matrix-free-gpu-and-model-selection-technical-synthesis
  - research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-gpu-and-model-selection-technical-synthesis
tags:
  - research
  - PIML
  - matrix-free
  - GPU
  - topology-optimization
status: "in-progress"
date_start: 2026-07-20
date_update: 2026-08-04
related:
  - long-term-research-lines
  - postdoc-research-output-roadmap
  - project-plan
  - high-performance-solver-survey
  - concepts/matrix-free/_index
---

# 博士后核心研究项目入口

> 本目录维护 [[../long-term-research-lines#主线二：智能高性能计算力学|智能高性能计算力学]] 在博士后阶段的核心研究项目“[[project-plan|面向大规模拓扑优化的 PIML Matrix-Free 求解与 GPU 协同加速方法研究]]”。本页只负责统一导航和事实所有权；项目目标、WP1–WP3、两年阶段和资助映射由项目计划唯一维护。

## 1. 事实所有权

| 内容 | 权威位置 |
|---|---|
| 项目名称、总体目标、WP1–WP3、两年阶段、项目级状态和资助映射 | [[project-plan]] |
| PIML 方法、模型选型、当前状态、历史证据与完成门禁 | [[../technical-lines/piml-research-guide]] |
| Matrix-Free 长期目标、能力边界、阶段模型、验收原则与当前任务状态 | [[../technical-lines/matrix-free-research-guide]] |
| GPU/HPC 当前状态、计时边界与性能门禁 | [[../technical-lines/gpu-hpc-research-guide]] |
| 三线交叉现状、证据成熟度、耦合机制、研究假设、统一研究方案与验证协议 | [[high-performance-solver-survey]] |
| 博士后论文组合、博士延续成果及论文启动条件 | [[../postdoc-research-output-roadmap]] |

## 2. 当前研究

| 页面 | 职责 | 状态 |
|---|---|---|
| [[project-plan]] | 博士后核心项目的科研与执行总计划 | in-progress |
| [[high-performance-solver-survey]] | 三线交叉现状、证据成熟度、耦合机制、研究假设、统一研究方案与验证协议 | in-progress |

## 3. 最低融合边界

1. 各单线的正确性和正式 evidence 闭环后，才启动端到端融合实验。
2. 融合成果必须回答新的耦合机制或端到端科学问题，并形成统一精度、时间和内存证据。
3. 单纯连接已有程序只视为系统集成，不单独构成论文成果。

实际启动融合时，应在对应 technical-line guide 的执行状态和软件仓库中冻结算例、接口、指标、停止条件和失败回退，不另建通用融合规范。

## 4. 当前边界

- 三条技术线尚未形成端到端一体化系统。
- 单线长期边界只从对应 technical-line guide 读取；Matrix-Free 当前结果和下一步任务统一从 [[../technical-lines/matrix-free-research-guide#五、阶段门禁与当前执行状态]] 读取。
- WP1（Matrix-Free/GPU）与 WP2（PIML/GPU）可以分别推进；WP3 的项目级启动条件由 [[project-plan]] 维护，论文 C 的成果边界由 [[../postdoc-research-output-roadmap]] 维护。
- MMC/MMV 是独立合作与应用课题，不在本目录维护。

## 5. 关联入口

- [[../long-term-research-lines]] — 个人长期科研主线。
- [[../postdoc-research-output-roadmap]] — 核心项目论文、博士延续成果与风险控制。
- [[../../concepts/matrix-free/_index]] — Matrix-Free 稳定知识、当前研究、文献证据、工作汇报与历史档案的统一语义入口。
- [[../technical-lines/_index]] — 三条长期技术线。
- [[../technical-lines/piml-research-guide]] — PIML 模型选型原则、WP2 阶段门禁、当前动作和条件性实验。
- [[../../work-reports/guo-xu/_index]] — 郭旭老师工作汇报。
- [[../../work-reports/liu-chang/_index]] — 刘畅老师工作汇报。

## 6. 管理边界

- 本项目是主线二在博士后阶段的主要实施载体，但 PIML、Matrix-Free、GPU/HPC 的稳定概念和长期技术能力仍可跨项目复用。
- 第 80 批及后续基金申请是项目的资助渠道，不是项目本身；基金获批状态不得替代项目完成状态。
- 代码、配置、运行结果和性能日志由相应软件仓库维护；本目录不建立第二套工程事实源。
