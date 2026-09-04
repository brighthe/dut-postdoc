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
date_update: 2026-08-27
---

# 郭旭

> 大连理工大学教授、中国科学院院士，显式拓扑优化（MMC/MMV）与 Problem-Independent PIML 的提出者与主导者；是本人博士后工作的合作导师，也是本库全部 PIML 与 MMC/MMV 文献的共同作者。

## 基本信息

| 项 | 内容 |
|---|---|
| 类型 | person |
| 所属/单位 | 大连理工大学 · 工业装备结构分析优化与 CAE 软件全国重点实验室 |
| 学术身份 | 中国科学院院士 |
| 关键词 | MMC/MMV、PIML、EMsFEM、PVP、SiPESC、双模量 |
| 公开主页 | <https://faculty.dlut.edu.cn/2000011087/> |
| 指导关系 | [[../liu-chang/liu-chang|刘畅]] 的博士导师 |

## 概况

其研究以显式拓扑优化为主线，向上延伸到复杂力学行为的变分原理与多尺度表征，向下延伸到工业软件与高性能计算实现，近年又通过 Problem-Independent PIML 把机器学习嵌入有限元分析与优化流程。本页是该研究体系与相关汇报在知识库中的统一实体入口。

## 研究体系

### 1. 显式拓扑优化（MMC/MMV）

Moving Morphable Components（MMC）和 Moving Morphable Voids（MMV）以组件或孔洞的低维连续几何参数描述结构拓扑，使几何边界、优化变量和最终构型保持显式关联。其典型计算链包括拓扑描述函数、固定背景网格上的物理分析、伴随灵敏度和几何参数更新。离散方法与工程取舍见 [[../../research/mmc-mmv/mmc-mmv-numerical-discretization-survey]]。

### 2. 问题无关机器学习（PIML）

Problem-Independent PIML 不直接学习某个整体边界条件、外载荷或优化目标下的端到端答案，而是学习可复用于有限元分析的局部力学表示，再嵌入全局组装、求解和优化流程。数学对象、方法边界和演化关系分别见 [[../../concepts/piml/mathematical-foundations]]、[[../../concepts/piml/method-lineage]] 与 [[../../research/piml-matrix-free-gpu/piml-research-guide]]。

### 3. 复杂力学行为变分原理与多尺度计算

该方向从变分原理和多尺度表征出发，处理大变形、双模量、非光滑本构以及微结构设计等复杂问题，为数值离散和学习型局部表示提供力学基础。通用线弹性基础单独维护在 [[../../concepts/linear-elasticity]]。

### 4. 工业软件与高性能计算（SiPESC）

SiPESC（Software Integration Platform for Engineering and Scientific Computation）以插件式、组件化和开放接口组织有限元分析、结构优化、多学科优化、可视化与工程数据等能力，为显式拓扑优化、子结构方法和并行求解的工程化提供平台载体。其公开 Matrix-Free 与并行成果的事实边界见 [[../../concepts/matrix-free/method-lineage]]。

### 5. 混合变分问题与极值型数值方法

该方向关注混合变分问题、参数变分原理（PVP）、杂交元和极值型计算，目标包括处理非光滑本构、降低局部变量以及获得适合全局求解的代数系统。本页只记录研究方向，不替代具体概念页和论文笔记中的条件、推导与结论。

## 已建立文献入口的署名工作

以下条目在本库已有单篇文献入口；作者顺序和页面状态以各页 frontmatter 为准。`draft` 条目当前只使用已核验元数据／摘要，不等同于全文精读。

| 论文 | 年份 | 方向 | 证据状态 |
|---|---|---|---|
| [[../../literature/topopt/mmc-mmv/translations/Zhang2016-MMC-topology-zh]] | 2016 | MMC 显式拓扑描述的基础工作 | 全文笔记 |
| [[../../literature/topopt/mmc-mmv/translations/Zhang2016-minimum-length-scale-zh]] | 2016 | MMC 框架下的最小长度尺度控制 | 全文笔记 |
| [[../../literature/topopt/mmc-mmv/translations/Zhang2017-MMV-3D-zh]] | 2017 | MMV 三维显式拓扑优化 | 全文笔记 |
| [[../../literature/topopt/mmc-mmv/translations/Lei2018-machinelearningdriven-zh]] | 2019 | MMC + PCA/SVR/KNN，问题相关的最终设计代理 | 全文笔记 |
| [[../../literature/topopt/piml/translations/Huang2022-problemindependentmachine-zh]] | 2022 | PIML 起点：EMsFEM 粗单元形函数学习 | 全文笔记 |
| [[../../literature/topopt/piml/translations/Huang2023-PIML-substructure-zh]] | 2023 | PIML 推进到子结构静力缩聚 | 全文笔记 |
| [[../../literature/topopt/piml/translations/Huang2024-PIML-datafree-zh]] | 2024 | DeepONet + data-free 力学损失 | 全文笔记 |
| [[../../literature/topopt/piml/translations/Zhang2024-isoparametric-PIML-zh]] | 2024 | 等参单元与复杂设计域 PIML | `draft`，摘要级 |
| [[../../literature/topopt/piml/translations/Xu2025-PIML-lattice-MMC-zh]] | 2025 | PIML、MMC 与三维梯度点阵应用 | `draft`，摘要级 |
| [[../../literature/topopt/gpu-hpc/translations/Ma2026-highperformanceparallel-zh]] | 2026 | PIML 子结构路线的并行大规模实现 | 全文笔记 |
| [[../../literature/topopt/piml/translations/Guo2026-highgeneralization-bezier-zh]] | 2026 | Bézier 边界位移参数化与子结构内部响应 | `draft`，摘要级 |
| [[../../literature/topopt/piml/translations/Guo2026-PIML-OFEM-zh]] | 2026 | 超采样数值基函数与重叠有限元 | `draft`，arXiv v1 摘要级 |

## 汇报时间线

| 汇报 | 状态 | 实际日期 | 核心内容 |
|---|---|---|---|
| [[first-formal-work-report]] | preparing | 待确定 | 汇报核心项目精确 Matrix-Free/GPU 基线的当前正式结果、PIML 局部表示与三线融合的研究衔接及下一步设想，请郭老师指导优先科学问题和成果出口 |

## 知识入口与关联

| 方向 | 权威页面 |
|---|---|
| MMC/MMV 数值离散 | [[../../research/mmc-mmv/mmc-mmv-numerical-discretization-survey]] |
| PIML 方法基础与谱系 | [[../../concepts/piml/mathematical-foundations]]；[[../../concepts/piml/method-lineage]]；[[../../concepts/ml-roles-and-boundaries]] |
| Matrix-Free 与高性能求解 | [[../../concepts/matrix-free/method-lineage]]；[[../../research/piml-matrix-free-gpu/project-plan]] |
| 个人长期科研主线与博士后成果路线 | [[../../research/long-term-research-lines]] |
| 入站阶段科研计划 | [[../../archive/2026-postdoc-entry-assessment/postdoc-research-plan]] |
| 师门链与人物关系 | [[../relationships]] |

## 与我的关联及维护规则

- 是本人博士后工作的合作导师，其研究体系构成课题的学术背景；个人长期研究问题与博士后阶段成果安排以 [[../../research/long-term-research-lines]] 为准。
- 当前交叉关注包括 PIML 与高性能结构分析、MMC/MMV 数值离散，以及复杂材料模型下的变分与离散方法。
- 一次汇报只维护一个页面，未实际发生时保持 `preparing`；汇报页只保留当次要讲的工作、结果、事实边界、请教事项、实际结论和行动项。
- 内部任务编号、完整 Todo、程序计划和验收条件统一回到 [[../../research/piml-matrix-free-gpu/matrix-free-research-guide#五、权威事实来源|Matrix-Free guide 的权威事实来源]]；代码、运行命令和原始产物由 SOPTX 维护。
- 真实聊天、约见和关系信息由沟通仓库维护，本页不复制。

## 相关页面

- [[../liu-chang/liu-chang|刘畅]] — 其学生，AI 赋能结构分析优化方向，PIML 主线全部论文共同作者。
- [[../../concepts/piml/_index]] — PIML 主题入口及问题无关性的适用边界。
- [[../../concepts/matrix-free/_index]] — Matrix-Free 稳定知识与当前研究入口。
- [[../../research/piml-matrix-free-gpu/piml-research-guide]] — PIML 技术线总入口。
- [[../../research/piml-matrix-free-gpu/_index|博士后核心研究项目入口]] — 项目导航、事实所有权和最低融合边界。
