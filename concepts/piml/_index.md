---
title: "Problem-Independent Machine Learning (PIML) 主题入口"
type: index
tags:
  - PIML
  - topology-opt
date_added: 2026-07-21
date_update: 2026-08-13
---

# Problem-Independent Machine Learning (PIML) 主题入口

> 本页为 Problem-Independent Machine Learning (PIML，问题无关机器学习) 的知识地图，连接 PIML 的稳定知识、核心文献证据与研究路线。

## 稳定知识

> “稳定知识”仅涵盖视角长期稳定、通用跨问题的基石范式与基础设施文档。

| 页面 | 一句话概括 |
|---|---|
| [[piml-paradigm]] | 问题无关机器学习 (PIML) 通用 5 步范式、数据流全景图与 PINN 侧向对比卡片 |
| [[method-lineage]] | Problem-Independent 路线从 EMsFEM 形函数到子结构、data-free 与并行优化的演化主线 |
| [[reference-libraries/fealpy-sciml-architecture]] | FEALPy `fealpy.ml` 的自动微分残差算子、配点采样器、网格—网络绑定容器与可视化导出链 |

## PIML 与子结构静力缩聚

> 本节提供 PIML 与子结构静力缩聚结合的核心文档地图；不复制 Schur 补推导、程序运行结果或项目阶段状态。

```text
rho^j -> K^j -> (N_exact^j, K_s,exact^j)
      -> (N_hat^j 或 K_s,hat^j)
      -> 全局接口系统 -> 细尺度恢复与下游验证
```

#### 1. 核心理论与数学事实源 (dut-postdoc 知识库)
| 入口 | 职责与呈现内容 |
|---|---|
| [[../substructural-condensation]] | **子结构有限元与静力缩聚**：子结构划分、Schur 补消元、接口求解与位移恢复的纯力学权威数学事实源。 |
| [[piml-substructural]] | **子结构 PIML 算子与物理正定范式**：局部 PIML 算子映射、路线 A (形函数 N) 与路线 B (Cholesky 刚度 K_s) 对比、物理正定保证与自动回退。 |
| [[../../research/technical-lines/piml-research-guide]] | **PIML 研究指南**：研究目标、学习对象边界、统一比较契约与证据入口。 |

#### 2. 论文证据与文献事实源 (dut-postdoc 知识库)
| 入口 | 职责与呈现内容 |
|---|---|
| [[../../literature/topology-opt/translations/Huang2023-PIML-substructure-zh]] | **Huang 2023 论文中文精译**：子结构缩聚 PIML 原始论文完整中文翻译，含数学公式 1~18、MBB 梁算例（Section 4.1）与拓扑优化流程。 |
| [[../../literature/topology-opt/notes/Huang2023-PIML-substructure]] | **Huang 2023 论文阅读笔记**：论文核心创新点、算法骨架与消融实验结构化笔记。 |

> 配套开源工程代码实现与实测报告见 SOPTX 仓库 `examples/piml_substructure_elasticity/`。

线弹性密度—刚度前提见 [[../linear-elasticity]]；ML/PINN 的角色边界见 [[../ml-roles-and-boundaries]] 和 [[../pinn-paradigm]]。宏观载荷和边界条件只在全局接口系统阶段进入，不是局部学习输入。

## 项目与技术线入口

| 页面 | 一句话概括 |
|---|---|
| [[../../research/technical-lines/piml-research-guide]] | 以 Problem-Independent 局部力学表示学习为项目主线，服务 WP2 的证据综合与模型选型 |
| [[../../research/piml-matrix-free-gpu/_index]] | 以结构保持 PIML 局部算子为核心内容之一的博士后核心研究项目入口 |

## 文献证据

- [[../../literature/_index#当前 ingest 队列]] — Physics-Informed ML、PINN、neural operator 与结构保持学习的当前待入库证据。
- [[../../literature/topology-opt/notes/Lei2018-machinelearningdriven]] — 机器学习 + MMC 实时拓扑优化，作为问题相关直接预测范式的前史。
- [[../../literature/topology-opt/notes/Huang2022-problemindependentmachine]] — Huang 2022，PIML + EMsFEM 形函数。
- [[../../literature/topology-opt/notes/Huang2023-PIML-substructure]] — Huang 2023，PIML + 子结构形函数 / 缩聚刚度矩阵。
- [[../../literature/topology-opt/notes/Huang2024-PIML-datafree]] — Huang 2024，mechanics-based data-free PIML。
- [[../../literature/topology-opt/notes/Ma2026-highperformanceparallel]] — Ma 2026，并行 PIML 与按需预测 / 释放。

## 关联入口

- 关联主题：[[../pinn-paradigm|PINN 通用概念与范式]]
- 关联主题：[[../machine-learning|机器学习分类与归纳偏置主文档]] — 经典回归、神经网络架构、函数／算子学习和 PINN 等训练范式的通用分类框架。
- 关联主题：[[../ml-roles-and-boundaries]] — 计算力学中 PIML、PINN 与其他学习路线的作用位置和边界。
- 关联主题：[[../substructural-condensation]] — 子结构划分、Schur 补消元与接口求解；Huang2023 之后子结构 PIML 路线的经典理论底座。
- 关联主题：[[../mmc/_index]] — 显式组件、TDF、Ersatz 与优化闭环；Lei 2018/2019 的设计表示基础。
- 关联主题：[[../matrix-free/_index]] — 全局算子、装配层次、Krylov 与预条件。
- 关联主题：[[../gpu-hpc/_index]] — PIML 批量推理、端到端性能与异构并行。

## 管理边界

- 数学事实分别由 [[piml-substructural]]（PIML 子结构算子）与 [[../substructural-condensation]]（Schur 补缩聚推导）维护，单篇论文事实由 `literature/` 维护，阶段性讨论由 `discussions/` 维护。
- 不在概念页维护当前任务状态、实施阶段或预计交付日期；这些由 [[../../research/technical-lines/piml-research-guide]] 维护。
- PINN 是 Physics-Informed ML 的一类方法，与本项目的 Problem-Independent 路线不是同一正式名称或分类维度，不得混用「PIML」指代二者。
- 新成果只有在论文、预印本、专利或公开软件等来源可核实时，才进入正式时间线。
- 本页不维护容易过期的文件总数，也不登记只因索引、日志、参考文献或顺带讨论而命中关键词的全部文件。
