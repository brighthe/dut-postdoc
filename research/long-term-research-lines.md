---
title: "个人长期科研主线"
topic: "面向结构拓扑优化的高精度数值离散与智能高性能计算"
aliases:
  - 个人科研主线
  - 长期科研主线
tags:
  - research-agenda
  - topology-optimization
  - numerical-discretization
  - PIML
  - matrix-free
  - GPU
  - high-performance-computing
status: "in-progress"
date_start: 2026-07-31
date_update: 2026-08-04
---

# 个人长期科研主线

> 本页是个人长期科研方向、两条主线及其关系的最高层事实源。具体课题、技术状态、论文证据和软件实现分别由 `research/` 下的课题页与技术线、`literature/`、`papers/` 和对应软件仓库维护，本页不建立并行的任务或进度台账。

## 总体定位

长期研究围绕“**面向结构拓扑优化的高精度数值离散与智能高性能计算**”展开，形成两条来源不同、相互支撑的科研主线：

1. **高精度数值离散与拓扑优化**：起源于数学博士阶段，关注拓扑优化中结构分析的离散精度、数值稳定性与复杂单元适应性。
2. **智能高性能计算力学**：形成于力学博士后阶段，关注 PIML、Matrix-Free 与 GPU 异构并行计算的结合，以及大规模结构分析与拓扑优化中的端到端效率。

## 主线一：高精度数值离散与拓扑优化

### 起源与定位

本主线延续数学博士阶段在计算数学、有限元离散和拓扑优化方面的研究积累，核心目标是发展兼具理论基础、数值稳定性和拓扑优化适用性的高精度离散方法。博士后阶段主要承担既有工作的延续、论文完善和成果转化，不纳入主线二核心项目的 WP1–WP3。

### 核心内容

- **Hu–Zhang 混合有限元拓扑优化**：研究任意次 Hu–Zhang 混合有限元在拓扑优化中的离散、结构响应与优化应用。
- **无稳定化项的虚单元拓扑优化**：研究不依赖额外稳定化项的虚单元离散及其在拓扑优化中的理论与算法问题。

### 当前入口

- [[../papers/arbitrary-order-huzhang-topopt-outline]] — 任意次 Hu–Zhang 混合有限元拓扑优化投稿论文框架。
- [[../papers/arbitrary-order-huzhang-topopt-draft-zh]] — 任意次 Hu–Zhang 混合有限元拓扑优化中文版初稿。
- [[../concepts/huzhang/huzhang-mixed-fem]] — 应力—位移混合变分、$H(\mathrm{div})$ 对称应力空间、低阶跳量稳定化与收敛阶结果的稳定概念页。

无稳定化项虚单元拓扑优化的长期调研和论文入口尚待在形成稳定内容后建立；在此之前不为满足目录形式预建空主题。

## 主线二：智能高性能计算力学

### 起源与定位

本主线面向力学博士后阶段的大规模结构分析与拓扑优化问题，把数据驱动的局部力学表示、无全局矩阵的迭代求解和 GPU 异构执行连接为统一的高性能计算路线。

### 核心内容

- **PIML**：学习可复用的局部力学表示或局部算子，减少多尺度与子结构分析中的重复局部求解。
- **Matrix-Free**：避免显式组装或存储大规模全局矩阵，以算子作用连接 Krylov 迭代与预条件方法。
- **GPU 异构并行计算**：面向局部算子批处理、全局算子作用、迭代求解和端到端流程开展异构并行与性能优化。
- **三者融合**：形成“PIML 局部预测或构造算子 → Matrix-Free 全局算子作用 → Krylov/预条件 → GPU 与 MPI 异构执行”的研究链路。

### 当前入口

- [[piml-matrix-free-gpu/_index]] — 博士后核心研究项目统一入口。
- [[piml-matrix-free-gpu/project-plan]] — 核心项目名称、目标、WP1–WP3、两年阶段和资助映射的唯一事实源。
- [[piml-matrix-free-gpu/high-performance-solver-survey]] — PIML Matrix-Free 求解与 GPU 协同加速的交叉现状、耦合机制、研究假设、统一研究方案与验证协议。
- [[technical-lines/_index]] — PIML、Matrix-Free、GPU/HPC 三条长期技术能力入口。

## 两条主线的关系

| 层面 | 主线一 | 主线二 |
|---|---|---|
| 核心问题 | 如何离散得更准确、更稳定 | 如何计算得更快、规模更大 |
| 主要基础 | 混合有限元、虚单元与拓扑优化离散 | PIML、Matrix-Free、Krylov、GPU/MPI |
| 共同对象 | 结构分析与拓扑优化 | 结构分析与拓扑优化 |
| 衔接方式 | 产生具有数学与力学结构的离散算子 | 对离散算子进行学习、无矩阵作用与异构并行求解 |

两条主线共同服务于大规模、复杂结构拓扑优化中的分析精度、数值稳定性、计算效率和并行可扩展性，但各自主线应保持明确的科学问题与证据体系。

## 博士后阶段成果组织

[[postdoc-research-output-roadmap]] 负责区分博士阶段延续成果与博士后核心项目成果，并把 WP1–WP3 映射为 Matrix-Free/GPU、PIML/GPU、PIML/Matrix-Free/GPU 三层论文及资助申请。行政积分、考核节点和成果认定继续由 `heliangos:career/dlut-postdoc/` 维护，本页不复制阶段性任务和状态。

## 当前课题与边界

- [[piml-matrix-free-gpu/project-plan|面向大规模拓扑优化的 PIML Matrix-Free 求解与 GPU 协同加速方法研究]] 是主线二在博士后阶段的核心牵引项目和主要实施载体；项目状态独立于基金是否获批。
- [[mmc-mmv/mmc-mmv-numerical-discretization-survey|MMC/MMV 显式拓扑优化先进数值分析]] 是具体合作与应用课题，可调用两条主线中的离散和快速求解能力，但不构成第三条个人长期科研主线。
- [[../archive/2026-postdoc-entry-assessment/postdoc-research-plan]] 是博士后入站阶段提交的科研计划，保留当时“两大研究方面、四条主线”的历史交付口径，不作为当前个人长期科研主线的总领。

## 维护边界

- 本页只在长期方向的定义、边界或主线关系发生变化时更新。
- 博士后核心项目的名称、目标、工作包、阶段与资助映射由 [[piml-matrix-free-gpu/project-plan]] 维护；论文组合与风险控制由 [[postdoc-research-output-roadmap]] 维护。
- 单项技术的当前能力、阶段门禁和验收标准由 [[technical-lines/_index]] 维护。
- 具体课题的研究问题、技术综合和证据边界由对应 `research/` 主题页维护。
- 代码、测试、Benchmark 与版本发布由相应软件仓库维护，本页只保存研究结论和仓库指针。
