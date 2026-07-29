---
title: "PIML 主题入口"
type: index
tags:
  - PIML
  - topology-opt
status: in-progress
date_added: 2026-07-21
date_update: 2026-07-28
---

# PIML 主题入口

> 本页是 Problem-Independent Machine Learning（PIML）的统一语义入口：稳定知识放在 `concepts/piml/`，单篇论文事实放在 `literature/`，当前研究路线与实验进展放在 `research/`。

## 稳定知识

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[ml-roles-and-boundaries]] | 按学习对象、训练信号、物理融合方式和计算角色比较计算力学中的机器学习路线 | draft |
| [[mathematical-foundations]] | PIML 问题无关性、局部映射、EMsFEM 基础路线与子结构缩聚学习映射的数学说明 | in-progress |
| [[method-lineage]] | PIML 从 EMsFEM 形函数学习到子结构、data-free 与并行大规模优化的演化主线 | draft |

## 当前研究

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[../../research/technical-lines/piml-research-guide]] | 当前已有基础、路线选择、目标差距、实施阶段与验收标准 | in-progress |

## 核心文献

- [[../../literature/topology-opt/Lei2018-machinelearningdriven]] — 机器学习 + MMC 实时拓扑优化，作为问题相关直接预测范式的前史。
- [[../../literature/topology-opt/Huang2022-problemindependentmachine]] — Huang 2022，PIML + EMsFEM 形函数。
- [[../../literature/topology-opt/Huang2023-PIML-substructure]] — Huang 2023，PIML + 子结构形函数 / 缩聚刚度矩阵。
- [[../../literature/topology-opt/Huang2024-PIML-datafree]] — Huang 2024，mechanics-based data-free PIML。
- [[../../literature/topology-opt/Ma2026-highperformanceparallel]] — Ma 2026，并行 PIML 与按需预测 / 释放。

## 关联主题

- [[../machine-learning]] — 网络架构、函数／算子学习和 PINN 等训练范式的通用分类框架。
- [[../matrix-free/_index]] — 全局算子、装配层次、Krylov 与预条件。
- [[../gpu-hpc/_index]] — PIML 批量推理、端到端性能与异构并行。

## 边界

- 不记录单篇论文完整摘要和实验细节；这些放在 `literature/`。
- 不在稳定知识页记录答辩话术、阶段原型和任务计划；这些通过“当前研究”入口连接到 `research/`。
- 不把 PIML 泛化为一般 PINN 或 physics-informed ML；本目录的 PIML 指郭旭团队提出的问题无关机器学习路线。
