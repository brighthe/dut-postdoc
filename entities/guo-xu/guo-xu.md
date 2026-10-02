---
title: "郭旭"
type: entity
entity_kind: person
aliases:
  - Guo Xu
  - Guo, Xu
  - 郭旭院士
  - 郭旭院士团队
  - 郭旭团队
  - guo-xu-team
  - Guo Xu group
  - Guo-Xu team
  - research/teams/guo-xu-team-overview
  - discussions/guo-xu
  - discussions/guo-xu/_index
  - entities/guo-xu
  - entities/guo-xu/guo-xu
tags:
  - topology-opt
  - MMC
  - MMV
  - PIML
  - variational-principles
  - industrial-software
  - work-report
status: in-progress
date_added: 2026-06-18
date_update: 2026-09-09
---

# 郭旭

本页整理郭老师的个人信息、科研方向与本库相关文献，以及与我的关系和重要交流。

## 1. 个人信息

| 项目 | 内容 |
|---|---|
| 姓名 | 郭旭（Xu Guo） |
| 单位 | 大连理工大学 · 工业装备结构分析优化与 CAE 软件全国重点实验室 |
| 学术身份 | 教授、中国科学院院士 |
| 公开主页 | [大连理工大学教师主页](https://faculty.dlut.edu.cn/2000011087/) |

基本资料沿用已有档案，公开主页为核验入口。

## 2. 科研方向与本库相关文献

以下按方向整理本页已收录的 12 篇署名工作，均可在对应文献页作者栏找到 Xu Guo。文献的阅读、核验状态以各页 frontmatter 为准；仅有摘要依据的内容不据此扩展为全文结论。

### 2.1 显式拓扑优化（MMC/MMV）

MMC 与 MMV 分别以可移动、可变形的组件和孔洞描述结构，用几何参数控制拓扑与边界。本库文献涉及替代材料模型、最小长度尺度、三维 MMV，以及机器学习驱动的设计预测。

| 署名文献 | 主要内容 |
|---|---|
| [[../../literature/topopt/mmc-mmv/translations/Zhang2016-MMC-topology-zh\|Zhang et al., 2016]] | MMC 与替代材料模型结合的拓扑优化方法 |
| [[../../literature/topopt/mmc-mmv/translations/Zhang2016-minimum-length-scale-zh\|Zhang et al., 2016：最小长度尺度]] | MMC 框架下的最小长度尺度控制 |
| [[../../literature/topopt/mmc-mmv/translations/Zhang2017-MMV-3D-zh\|Zhang et al., 2017]] | 三维 MMV 显式拓扑优化 |
| [[../../literature/topopt/mmc-mmv/translations/Lei2018-machinelearningdriven-zh\|Lei et al., 2019]] | MMC + PCA/SVR/KNN，面向特定问题的最终设计预测；2018 年在线发表，2019 年正式卷期 |

数值离散与工程取舍见 [[../../research/mmc-mmv/mmc-mmv-numerical-discretization-survey|MMC/MMV 数值离散调研]]。

### 2.2 问题无关机器学习（PIML）

Problem-Independent Machine Learning 学习可复用的局部力学表示或响应映射，再嵌入全局有限元分析与优化。本库收录的路线从 EMsFEM 形函数学习、子结构静力缩聚，扩展到 data-free 训练、复杂设计域、点阵结构和重叠有限元。

| 署名文献 | 主要内容 |
|---|---|
| [[../../literature/topopt/piml/translations/Huang2022-problemindependentmachine-zh\|Huang et al., 2022]] | EMsFEM 粗单元形函数学习 |
| [[../../literature/topopt/piml/translations/Huang2023-PIML-substructure-zh\|Huang et al., 2023]] | 子结构静力缩聚与大规模线弹性分析、拓扑优化 |
| [[../../literature/topopt/piml/translations/Huang2024-PIML-datafree-zh\|Huang et al., 2024]] | DeepONet 与基于力学的 data-free 训练 |
| [[../../literature/topopt/piml/translations/Zhang2024-isoparametric-PIML-zh\|Zhang et al., 2024]] | 基于等参单元的复杂设计域 PIML |
| [[../../literature/topopt/piml/translations/Xu2025-PIML-lattice-MMC-zh\|Xu et al., 2025]] | PIML 与 MMC 结合的三维点阵复合结构优化 |
| [[../../literature/topopt/piml/translations/Guo2026-highgeneralization-bezier-zh\|Guo et al., 2026：Bézier 边界位移]] | 子结构边界位移参数化与内部响应预测 |
| [[../../literature/topopt/piml/translations/Guo2026-PIML-OFEM-zh\|Guo et al., 2026：PIML-OFEM]] | 超采样数值基函数与重叠有限元；文献入口为 arXiv v1 预印本 |

方法演化见 [[../../concepts/piml/piml-paradigm#4. 文献谱系|PIML 方法谱系]]，子结构数学基础见 [[../../concepts/piml/piml-substructural|子结构 PIML]]；与我的研究衔接见 [[../../research/piml-matrix-free-gpu/piml-research-guide|PIML 研究指南]]。

### 2.3 高性能结构分析与工业软件

与 PIML 直接相关的已收录并行工作如下。

| 署名文献 | 主要内容 |
|---|---|
| [[../../literature/topopt/piml/translations/Ma2026-highperformanceparallel-zh\|Ma et al., 2026]] | PIML 子结构路线的大规模并行拓扑优化 |

该文的 `matrix-free` 指多尺度形函数按需预测和释放，仍形成并组装全局粗网格矩阵；与全局算子级 Matrix-Free 的区别见 [[../../concepts/matrix-free/method-lineage|团队 Matrix-Free 方法谱系]]。

原档案还记录了 SiPESC 工业软件方向；其具体平台能力与郭老师个人工作的对应来源待补，不由上述并行论文推定。

## 3. 与我的关系及重要交流

### 3.1 关系与合作背景

工作进展按四个关注点汇总于 [[reports/overview|工作汇报总览]]：Matrix-Free 在 PIML 中的应用、GPU 在 PIML 中的应用、两者联合应用，以及可求解问题规模。

郭老师是我的博士后合作导师。现有研究交集主要是 PIML 与高性能结构分析、MMC/MMV 数值离散，以及变分与离散方法。

- 人物关系及合作背景见 [[../relationships|师门链与人物关系]]；其中师门关系的待核验标记以该页为准。
- 郭老师于 2026 年 8 月介绍了 [[../guo-yilin/guo-yilin|郭一麟]]，作为 PIML 与 GPU 加速方向的合作线索。
- 我的长期研究安排见 [[../../research/long-term-research-lines|个人长期科研主线与博士后成果路线]]，当前项目进展见 [[../../research/piml-matrix-free-gpu/project-plan|博士后核心研究项目]]；入站时的计划保存在 [[../../archive/2026-postdoc-entry-assessment/postdoc-research-plan|入站阶段科研计划]]。

### 3.2 已有来源的重要交流

本节保留有长期价值的交流摘要，逐字聊天与完整事务经过回到来源记录。目前尚未核对与郭老师的完整聊天记录，下表仅整理本库已有记录，不代表全部交流。

| 时间 | 重要内容及后续关联 | 来源与边界 |
|---|---|---|
| 2026-06-17 | 郭老师同意入站科研计划。 | [[../mei-yue/wechat-log\|梅跃沟通档案]]“科研计划把关”中的回顾性记录；尚未核对郭老师原始回复。 |
| 2026-07，入站答辩后 | 郭老师建议先留在大连，去研究院熟悉情况，具体安排联系梅老师。 | [[../mei-yue/wechat-log\|梅跃沟通档案]] 2026-07-06 条目中的线下交流转述；背景标注 7/5，但消息写“今天下午”，具体会面日期待确认。 |
| 2026-08 | 郭老师介绍郭一麟，提供 PIML 与 GPU 加速方向的合作线索。 | [[../guo-yilin/guo-yilin\|郭一麟档案]]、[[../relationships\|人物关系页]]；具体日期与原始表述待补。 |
