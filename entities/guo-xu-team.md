---
title: "郭旭院士团队"
type: entity
entity_kind: team
aliases:
  - 郭旭团队
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
date_update: 2026-07-29
---

# 郭旭院士团队

> **一句话**：依托大连理工大学工业装备结构分析国家重点实验室，围绕显式拓扑优化（MMC/MMV）、Problem-Independent PIML、复杂力学与多尺度计算、SiPESC 工业软件以及混合变分数值方法开展研究；本页是该团队在知识库中的唯一稳定档案。

## 基本信息

| 项 | 内容 |
|---|---|
| 类型 | team（学术团队） |
| 所属/单位 | 大连理工大学 · 工业装备结构分析国家重点实验室 |
| 负责人 | 郭旭院士（[个人主页](https://faculty.dlut.edu.cn/2000011087/)） |
| 关键词 | MMC/MMV、PIML、EMsFEM、PVP、SiPESC、双模量 |

## 研究体系

### 1. 显式拓扑优化（MMC/MMV）

Moving Morphable Components（MMC）和 Moving Morphable Voids（MMV）以组件或孔洞的低维连续几何参数描述结构拓扑，使几何边界、优化变量和最终构型保持显式关联。其典型计算链包括拓扑描述函数、固定背景网格上的物理分析、伴随灵敏度和几何参数更新。离散方法与工程取舍见 [[../research/postdoc-plan/long-term/direction-2-mmc-mmv/mmc-mmv-numerical-discretization-survey]]。

### 2. 问题无关机器学习（PIML）

Problem-Independent PIML 不直接学习某个整体边界条件、外载荷或优化目标下的端到端答案，而是学习可复用于有限元分析的局部力学表示，再嵌入全局组装、求解和优化流程。数学对象、方法边界和演化关系分别见 [[../concepts/piml/mathematical-foundations]]、[[../concepts/piml/method-lineage]] 与 [[../research/technical-lines/piml-research-guide]]。

### 3. 复杂力学行为变分原理与多尺度计算

该方向从变分原理和多尺度表征出发，处理大变形、双模量、非光滑本构以及微结构设计等复杂问题，为数值离散和学习型局部表示提供力学基础。通用线弹性基础单独维护在 [[../concepts/linear-elasticity]]。

### 4. 工业软件与高性能计算（SiPESC）

SiPESC（Software Integration Platform for Engineering and Scientific Computation）以插件式、组件化和开放接口组织有限元分析、结构优化、多学科优化、可视化与工程数据等能力，为显式拓扑优化、子结构方法和并行求解的工程化提供平台载体。团队公开 Matrix-Free 与并行成果的事实边界见 [[../concepts/matrix-free/method-lineage]]。

### 5. 混合变分问题与极值型数值方法

该方向关注混合变分问题、参数变分原理（PVP）、杂交元和极值型计算，目标包括处理非光滑本构、降低局部变量以及获得适合全局求解的代数系统。本页只记录研究方向，不替代具体概念页和论文笔记中的条件、推导与结论。

## 代表成果与权威入口

| 方向 | 代表成果或知识入口 |
|---|---|
| MMC/MMV | [[../literature/topology-opt/Zhang2016-MMC-topology]]；[[../literature/topology-opt/Zhang2017-MMV-3D]]；[[../research/postdoc-plan/long-term/direction-2-mmc-mmv/mmc-mmv-numerical-discretization-survey]] |
| PIML | [[../literature/topology-opt/Huang2022-problemindependentmachine]]；[[../literature/topology-opt/Huang2023-PIML-substructure]]；[[../literature/topology-opt/Huang2024-PIML-datafree]]；[[../concepts/piml/mathematical-foundations]] |
| 高性能结构分析 | [[../literature/topology-opt/Ma2026-highperformanceparallel]]；[[../concepts/matrix-free/method-lineage]] |
| 个人研究路线 | [[../research/postdoc-plan/postdoc-research-plan]]；[[../research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-high-performance-solver-survey]] |

## 与博士后研究的关联

团队是博士后课题的学术背景，但个人研究问题、阶段安排和技术切入点不在实体页重复维护，统一以 [[../research/postdoc-plan/postdoc-research-plan]] 为准。当前交叉关注包括 PIML 与高性能结构分析、MMC/MMV 数值离散，以及复杂材料模型下的变分与离散方法。

## 来源与维护边界

- 团队负责人及单位信息以[郭旭院士个人主页](https://faculty.dlut.edu.cn/2000011087/)等官方来源为准。
- `entities/` 维护团队身份、稳定研究方向和权威入口；`concepts/` 维护方法定义与推导；`literature/` 维护论文事实；`research/` 维护个人计划、技术线和执行工作流。
- 旧团队总览已合并到本页，并由 frontmatter alias 保持历史链接可解析。
