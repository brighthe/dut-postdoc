---
title: "PIML 术语与主题入口"
type: index
tags:
  - PIML
  - topology-opt
status: in-progress
date_added: 2026-07-21
date_update: 2026-08-03
---

# PIML 术语与主题入口

> 本页首先解决 PIML 缩写歧义，再连接稳定知识、文献证据和当前研究。核心项目题目及 Huang–Ma 公开方法谱系中的 PIML 均指 **Problem-Independent Machine Learning（问题无关机器学习）**。Physics-Informed Machine Learning 是可借鉴的外部方法框架，但不是本项目 PIML 的正式展开。

## 术语消歧

| 术语 | 本库采用的含义 | 主要学习对象或作用 | 权威入口 |
|---|---|---|---|
| Physics-Informed Machine Learning | 以控制方程、守恒关系、初边值条件、能量原理或代数结构约束数据、loss、模型结构或校正过程的总框架 | 解场、参数、函数／算子或结构化局部表示 | [[../../literature/_index#当前 ingest 队列]]、[[../../research/technical-lines/piml-research-guide#三、国内外研究现状、研究缺口与选题价值]] |
| PINN | Physics-Informed ML 中以神经网络参数化 PDE 解或待识别参数的一类方法 | 坐标／参数到解场，服务正问题或反问题 | [[ml-roles-and-boundaries]] |
| Problem-Independent Machine Learning | Huang–Ma 路线中学习可跨宏观边值问题复用的局部力学表示 | 局部材料分布到多尺度形函数或缩聚刚度 | [[mathematical-foundations]]、[[method-lineage]] |
| neural operator | 学习函数空间之间的映射；能否 physics-informed 取决于训练与结构设计 | 输入函数到输出函数 | [[../machine-learning]]、[[../../literature/_index#当前 ingest 队列]] |

项目活跃页面第一次出现 PIML 时应写出 Problem-Independent Machine Learning 全称；讨论 Physics-Informed Machine Learning 时写出其全称，不再用同一裸缩写指代两种含义。

## 稳定知识

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[ml-roles-and-boundaries]] | 按学习对象、训练信号、物理融合方式和计算角色比较计算力学中的机器学习路线 | draft |
| [[mathematical-foundations]] | Problem-Independent 路线的问题无关性、局部映射、EMsFEM 与子结构缩聚数学说明 | in-progress |
| [[method-lineage]] | Problem-Independent 路线从 EMsFEM 形函数到子结构、data-free 与并行优化的演化主线 | draft |

## 当前研究

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[../../research/technical-lines/piml-research-guide]] | 以 Problem-Independent 局部力学表示学习为项目主线，服务 WP2 的证据、选型、阶段门禁与验证 | in-progress |
| [[../../research/piml-matrix-free-gpu/_index]] | 以结构保持 PIML 局部算子为核心内容之一的博士后核心研究项目入口 | in-progress |

## 工作汇报

- [[../../work-reports/guo-xu/_index]] — 面向郭旭老师的 PIML–Matrix-Free–GPU 阶段汇报入口；具体汇报不是 PIML 任务状态或数值 evidence 的事实源。
- [[../../work-reports/liu-chang/_index]] — 面向刘畅老师的 PIML 模型选型阶段汇报入口；完整研究任务和实验状态由 `research/` 维护。

## 文献证据

- [[../../literature/_index#当前 ingest 队列]] — Physics-Informed ML、PINN、neural operator 与结构保持学习的当前待入库证据。
- [[../../literature/topology-opt/notes/Lei2018-machinelearningdriven]] — 机器学习 + MMC 实时拓扑优化，作为问题相关直接预测范式的前史。
- [[../../literature/topology-opt/notes/Huang2022-problemindependentmachine]] — Huang 2022，PIML + EMsFEM 形函数。
- [[../../literature/topology-opt/notes/Huang2023-PIML-substructure]] — Huang 2023，PIML + 子结构形函数 / 缩聚刚度矩阵。
- [[../../literature/topology-opt/notes/Huang2024-PIML-datafree]] — Huang 2024，mechanics-based data-free PIML。
- [[../../literature/topology-opt/notes/Ma2026-highperformanceparallel]] — Ma 2026，并行 PIML 与按需预测 / 释放。

## 历史档案

- [[../../archive/2026-postdoc-entry-assessment/README]] — 2026 年博士后入站考核答辩的历史材料总览，其中包含当时的 PIML 原型、计划和表达；档案不再维护当前研究事实。

## 关联主题

- [[../machine-learning]] — 经典回归、神经网络架构、函数／算子学习和 PINN 等训练范式的通用分类框架。
- [[../pca-pod]] — 低维特征基、系数和重构；Lei 2018/2019 使用的输出表示工具。
- [[../mmc/_index]] — 显式组件、TDF、Ersatz 与优化闭环；Lei 2018/2019 的设计表示基础。
- [[../matrix-free/_index]] — 全局算子、装配层次、Krylov 与预条件。
- [[../gpu-hpc/_index]] — PIML 批量推理、端到端性能与异构并行。

## 管理边界

- 不记录单篇论文完整摘要和实验细节；这些放在 `literature/`。
- 不在稳定知识页记录答辩话术、阶段原型和任务计划；当前状态由 `research/` 维护，工作汇报和档案只保存相应阶段的表达与历史语境。
- 本入口同时管理缩写消歧；`mathematical-foundations.md` 和 `method-lineage.md` 专门维护项目采用的 Problem-Independent 路线。
- PINN 只是 Physics-Informed ML 的一类方法；Problem-Independent 路线可以采用监督学习或 mechanics-based data-free 训练，但二者仍是不同的分类维度和正式名称。
- 本页不维护固定文件数，也不登记只因索引、日志、参考文献或顺带讨论而命中 PIML 的全部文件。
