---
title: "PIML 术语与主题入口"
type: index
tags:
  - PIML
  - topology-opt
status: in-progress
date_added: 2026-07-21
date_update: 2026-08-09
---

# PIML 术语与主题入口

> 本页连接 PIML 的稳定知识、文献证据和当前研究。核心项目题目及 Huang–Ma 方法谱系中的 PIML 均指 **Problem-Independent Machine Learning（问题无关机器学习）**；Physics-Informed Machine Learning 是可借鉴的外部方法框架，但不是本项目 PIML 的正式展开。项目活跃页面首次出现时应写出相应全称。

## 稳定知识

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[piml-paradigm]] | 问题无关机器学习 (PIML) 通用 5 步范式、数据流全景图与 PINN 侧向对比卡片 | in-progress |
| [[mathematical-foundations]] | Problem-Independent 路线的问题无关性、局部映射、EMsFEM 与子结构缩聚的数学说明与局部—全局契约 | in-progress |
| [[method-lineage]] | Problem-Independent 路线从 EMsFEM 形函数到子结构、data-free 与并行优化的演化主线 | in-progress |
| [[reference-libraries/fealpy-sciml-architecture]] | FEALPy `fealpy.ml` 的自动微分残差算子、配点采样器、网格—网络绑定容器与可视化导出链 | draft |

## PIML 与子结构静力缩聚

> 本节只提供主题地图；不复制 Schur 补推导、程序运行结果或项目阶段状态。

```text
rho^j -> K^j -> (N_exact^j, K_s,exact^j)
      -> (N_hat^j 或 K_s,hat^j)
      -> 全局接口系统 -> 细尺度恢复与下游验证
```

### 程序实现必读入口

启动或讨论 SOPTX 中的 PIML 程序实现前，按下表进入相应的数学、工程与代码事实源；本页只提供阅读顺序和职责路由。

| 入口 | 职责 |
|---|---|
| [[mathematical-foundations]] | 局部 PIML 映射、精确缩聚标签契约、路线 A/B、结构检查与精确回退边界。 |
| [[../substructural-condensation]] | 子结构有限元与精确缩聚的数学事实源。 |
| [[../../research/technical-lines/piml-research-guide]] | 研究目标、学习对象边界、统一比较契约与证据入口。 |

关联实现：SOPTX `examples/substructure_elasticity/`，维护当前精确子结构静力缩聚基线；具体入口与运行方式见该目录 `README.md`。

线弹性密度—刚度前提见 [[../linear-elasticity]]；ML/PINN 的角色边界见 [[../ml-roles-and-boundaries]] 和 [[../pinn-paradigm]]；子结构 PIML 的论文证据见 [[../../literature/topology-opt/notes/Huang2023-PIML-substructure]]。宏观载荷和边界条件只在全局接口系统阶段进入，不是局部学习输入。

## 项目与技术线入口

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[../../research/technical-lines/piml-research-guide]] | 以 Problem-Independent 局部力学表示学习为项目主线，服务 WP2 的证据综合与模型选型 | in-progress |
| [[../../research/piml-matrix-free-gpu/_index]] | 以结构保持 PIML 局部算子为核心内容之一的博士后核心研究项目入口 | in-progress |

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

- 数学事实分别由 [[mathematical-foundations]]（PIML 局部—全局契约）与 [[../substructural-condensation]]（Schur 补缩聚推导）维护，单篇论文事实由 `literature/` 维护，阶段性讨论由 `discussions/` 维护。
- 不在概念页维护当前任务状态、实施阶段或预计交付日期；这些由 [[../../research/technical-lines/piml-research-guide]] 维护。
- PINN 是 Physics-Informed ML 的一类方法，与本项目的 Problem-Independent 路线不是同一正式名称或分类维度，不得混用「PIML」指代二者。
- 新成果只有在论文、预印本、专利或公开软件等来源可核实时，才进入正式时间线。
- 本页不维护容易过期的文件总数，也不登记只因索引、日志、参考文献或顺带讨论而命中关键词的全部文件。
