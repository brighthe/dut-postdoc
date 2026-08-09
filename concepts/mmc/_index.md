---
title: "MMC 主题入口"
type: index
tags:
  - MMC
  - topology-opt
  - explicit-geometry
status: in-progress
date_added: 2026-07-31
date_update: 2026-08-09
---

# MMC 主题入口

> 本页是 Moving Morphable Components（MMC，移动可变形组件）的统一语义入口：稳定数学概念放在 `concepts/mmc/`，单篇论文事实放在 `literature/`，当前数值离散与研究路线放在 `research/`，已完成事件的历史材料放在 `archive/`。**命名边界**：MMC 指以显式组件参数描述结构拓扑的优化框架本身；是否使用机器学习、PIML、Matrix-Free 或 GPU 属于后续方法选择，不属于 MMC 定义。MMV 与 MMC 密切相关但参数化不同，两者差异以对应文献和调研页为准。

## 稳定知识

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[mathematical-foundations]] | 从组件参数、TDF 和多组件并集到 Ersatz 有限元、灵敏度与 MMA 优化闭环 | in-progress |

## 显式几何到优化闭环

> 本节只提供主题地图；不复制 TDF 定义、并集构造、灵敏度推导、验证门禁或算例数字。

```text
组件设计变量 -> 局部坐标与 TDF -> 多组件并集（拓扑变化）
  -> Ersatz 有限元 -> 柔顺度与体积约束 -> MMA 优化闭环
  -> 回到组件设计变量
```

MMC 的特征是设计变量始终是显式几何参数，密度场只是并集经 Ersatz 映射后的中间产物，因此拓扑变化由组件的出现、消失与重叠直接产生。各环节的定义、推导与数值验证门禁由 [[mathematical-foundations]] 维护。

## 项目与技术线入口

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[../../research/mmc-mmv/mmc-mmv-numerical-discretization-survey]] | MMC/MMV 的固定网格、精确边界、高阶离散和高效结构分析路线 | draft |

## 文献证据

- [[../../literature/topology-opt/notes/Zhang2016-MMC-topology]] — 可变厚度 MMC、Ersatz 有限元与 188 行 MATLAB 实现。
- [[../../literature/topology-opt/notes/Zhang2016-minimum-length-scale]] — MMC 最小尺度控制和精确边界处理。
- [[../../literature/topology-opt/notes/Lei2018-machinelearningdriven]] — MMC 设计向量结合 PCA 与 SVR/KNN 的问题相关最终设计预测。
- [[../../literature/topology-opt/notes/Lei2018-machinelearningdriven#模型选型证据卡]] — MMC 低维设计表示在问题相关机器学习代理中的论文证据（同一篇笔记内的证据卡锚点）。
- [[../../literature/topology-opt/notes/Xu2025-PIML-lattice-MMC]] — PIML、MMC、分区坐标映射与三维梯度点阵复合结构优化；当前为元数据／摘要级 `draft` 证据。

## 关联入口

- 关联主题：[[../linear-elasticity]] — MMC 几何进入有限元后的线弹性状态方程。
- 关联主题：[[../piml/_index]] — 学习可复用局部力学表示的 Problem-Independent PIML；MMC 本身不等于 PIML。
- 历史档案：[[../../archive/2026-postdoc-entry-assessment/README]] — 2026 年博士后入站考核答辩的历史材料总览，其中包含当时的 MMC/MMV 计划和表达；档案不再维护当前研究事实。

## 管理边界

- 本主题维护 MMC 的稳定几何、离散和优化概念，不复制单篇论文的样本规模、算例结果或代码逐行说明；这些由 `literature/` 维护。
- 当前研究状态由 `research/` 维护，历史档案只保存事件发生时的材料和表达；当前没有独立 MMC 工作汇报，因此不设该角色条目。
- MMC 是显式拓扑优化框架；是否使用机器学习、PIML、Matrix-Free 或 GPU 是后续方法选择，不属于 MMC 定义本身。
- MMV 与 MMC 密切相关，但两者的孔洞/实体参数化差异仍以对应文献和调研页为准。
- 新成果只有在论文、预印本、专利或公开软件等来源可核实时，才进入正式时间线。
- 本页不维护固定文件数，也不登记只因索引、日志、参考文献或顺带讨论而命中 MMC 的全部文件。
