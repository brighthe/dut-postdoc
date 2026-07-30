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
tags:
  - topology-opt
  - MMC
  - MMV
  - PIML
  - variational-principles
  - industrial-software
status: in-progress
date_added: 2026-06-18
date_update: 2026-07-30
---

# 郭旭

> **一句话**：大连理工大学教授、中国科学院院士，显式拓扑优化（MMC/MMV）与 Problem-Independent PIML 的提出者与主导者；是本人博士后工作的合作导师，也是本库全部 PIML 与 MMC/MMV 文献的共同作者。

## 基本信息

| 项 | 内容 |
|---|---|
| 类型 | person |
| 所属/单位 | 大连理工大学 · 工业装备结构分析国家重点实验室 |
| 学术身份 | 中国科学院院士 |
| 关键词 | MMC/MMV、PIML、EMsFEM、PVP、SiPESC、双模量 |
| 公开主页 | <https://faculty.dlut.edu.cn/2000011087/> |
| 指导关系 | [[liu-chang]] 的博士导师 |

## 概况

其研究以显式拓扑优化为主线，向上延伸到复杂力学行为的变分原理与多尺度表征，向下延伸到工业软件与高性能计算实现，近年又通过 Problem-Independent PIML 把机器学习嵌入有限元分析与优化流程。本页是该研究体系在知识库中的唯一稳定档案。

## 研究体系

### 1. 显式拓扑优化（MMC/MMV）

Moving Morphable Components（MMC）和 Moving Morphable Voids（MMV）以组件或孔洞的低维连续几何参数描述结构拓扑，使几何边界、优化变量和最终构型保持显式关联。其典型计算链包括拓扑描述函数、固定背景网格上的物理分析、伴随灵敏度和几何参数更新。离散方法与工程取舍见 [[../research/postdoc-plan/long-term/direction-2-mmc-mmv/mmc-mmv-numerical-discretization-survey]]。

### 2. 问题无关机器学习（PIML）

Problem-Independent PIML 不直接学习某个整体边界条件、外载荷或优化目标下的端到端答案，而是学习可复用于有限元分析的局部力学表示，再嵌入全局组装、求解和优化流程。数学对象、方法边界和演化关系分别见 [[../concepts/piml/mathematical-foundations]]、[[../concepts/piml/method-lineage]] 与 [[../research/technical-lines/piml-research-guide]]。

### 3. 复杂力学行为变分原理与多尺度计算

该方向从变分原理和多尺度表征出发，处理大变形、双模量、非光滑本构以及微结构设计等复杂问题，为数值离散和学习型局部表示提供力学基础。通用线弹性基础单独维护在 [[../concepts/linear-elasticity]]。

### 4. 工业软件与高性能计算（SiPESC）

SiPESC（Software Integration Platform for Engineering and Scientific Computation）以插件式、组件化和开放接口组织有限元分析、结构优化、多学科优化、可视化与工程数据等能力，为显式拓扑优化、子结构方法和并行求解的工程化提供平台载体。其公开 Matrix-Free 与并行成果的事实边界见 [[../concepts/matrix-free/method-lineage]]。

### 5. 混合变分问题与极值型数值方法

该方向关注混合变分问题、参数变分原理（PVP）、杂交元和极值型计算，目标包括处理非光滑本构、降低局部变量以及获得适合全局求解的代数系统。本页只记录研究方向，不替代具体概念页和论文笔记中的条件、推导与结论。

## 已入库的署名工作

以下条目在本库已有精读页，其在全部八篇中均为末位作者；作者顺序以各页 frontmatter 为准。

| 论文 | 年份 | 方向 |
|---|---|---|
| [[../literature/topology-opt/Zhang2016-MMC-topology]] | 2016 | MMC 显式拓扑描述的基础工作 |
| [[../literature/topology-opt/Zhang2016-minimum-length-scale]] | 2016 | MMC 框架下的最小长度尺度控制 |
| [[../literature/topology-opt/Zhang2017-MMV-3D]] | 2017 | MMV 三维显式拓扑优化 |
| [[../literature/topology-opt/Lei2018-machinelearningdriven]] | 2019 | MMC + PCA/SVR/KNN，问题相关的最终设计代理 |
| [[../literature/topology-opt/Huang2022-problemindependentmachine]] | 2022 | PIML 起点：EMsFEM 粗单元形函数学习 |
| [[../literature/topology-opt/Huang2023-PIML-substructure]] | 2023 | PIML 推进到子结构静力缩聚 |
| [[../literature/topology-opt/Huang2024-PIML-datafree]] | 2024 | DeepONet + data-free 力学损失 |
| [[../literature/topology-opt/Ma2026-highperformanceparallel]] | 2026 | PIML 子结构路线的并行大规模实现 |

## 知识入口

| 方向 | 权威页面 |
|---|---|
| MMC/MMV 数值离散 | [[../research/postdoc-plan/long-term/direction-2-mmc-mmv/mmc-mmv-numerical-discretization-survey]] |
| PIML 方法基础与谱系 | [[../concepts/piml/mathematical-foundations]]；[[../concepts/piml/method-lineage]]；[[../concepts/piml/ml-roles-and-boundaries]] |
| Matrix-Free 与高性能求解 | [[../concepts/matrix-free/method-lineage]]；[[../research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-high-performance-solver-survey]] |
| 个人研究路线 | [[../research/postdoc-plan/postdoc-research-plan]] |

## 与我的关联

- 是本人博士后工作的合作导师，其研究体系构成课题的学术背景；个人研究问题、阶段安排和技术切入点不在本页重复维护，统一以 [[../research/postdoc-plan/postdoc-research-plan]] 为准。
- 当前交叉关注包括 PIML 与高性能结构分析、MMC/MMV 数值离散，以及复杂材料模型下的变分与离散方法。
- 面向其的周期性工作汇报单独维护在 `work-reports/guo-xu/`，本页不记录汇报内容、行政流程与沟通过程。

## 待确认

- **实验室名称口径不一致**：本页沿用「工业装备结构分析国家重点实验室」，[[liu-chang]] 依据 2026-07-30 公开检索写作「工业装备结构分析优化与 CAE 软件全国重点实验室」。二者应为同一实验室改名前后的名称，需以官方来源核定统一写法后同步两页。
- 其院士当选年份、具体荣誉与在研项目未经官方来源核对，本页不作罗列。

## 来源与维护边界

- 身份与单位信息以[个人主页](https://faculty.dlut.edu.cn/2000011087/)等官方来源为准。
- 本页原为「郭旭院士团队」团队页，2026-07-30 按「一实体一页」原则改为人物页：该团队以其为负责人，团队身份与其个人学术身份在本库中无需分立两页。旧页名、旧团队总览路径及中英文别名均由 frontmatter alias 保持历史链接可解析。
- `entities/` 维护实体身份、稳定研究方向和权威入口；`concepts/` 维护方法定义与推导；`literature/` 维护论文事实；`research/` 维护个人计划、技术线和执行工作流。

## 相关页面

- [[liu-chang]] — 其学生，AI 赋能结构分析优化方向，PIML 主线全部论文共同作者。
- [[../concepts/piml/_index]] — PIML 主题入口及问题无关性的适用边界。
- [[../concepts/matrix-free/_index]] — Matrix-Free 稳定知识与当前研究入口。
- [[../research/technical-lines/piml-research-guide]] — PIML 技术线总入口。
