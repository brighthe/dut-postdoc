---
title: "研究执行工作流索引"
topic: "可跨技术线复用的研究执行、训练、记录与验收流程"
tags:
  - research
  - workflow
  - reproducibility
status: "in-progress"
date_start: 2026-07-29
date_update: 2026-07-29
---

# 研究执行工作流索引

> 本目录回答“研究过程具体如何执行、记录和验收”。长期技术能力的目标、现状、阶段与门禁由 [[../technical-lines/_index]] 维护；稳定理论与数学定义由 `concepts/` 维护。

## 当前工作流

| 层级 | 工作流 | 当前定位 |
|---|---|---|
| 通用父流程 | [[machine-learning-workflow]] | 与具体问题、训练信号和网络解耦的机器学习生命周期、产物和验收契约 |
| 方法实例 | [[pinn-machine-learning-workflow]] | 一维 Poisson PINN 的采样、自动微分、loss、训练与评价全过程；当前实现映射见附录 |
| 方法契约草案 | [[linear-elasticity-pinn-machine-learning-workflow]] | 小变形静力线弹性 PINN：二维平面应力/平面应变与三维共用的训练、评价与复现流程 |

当前关系为：

```text
machine-learning-workflow.md
├─ pinn-machine-learning-workflow.md
│  └─ 一维 Poisson PINN
└─ linear-elasticity-pinn-machine-learning-workflow.md
   └─ 小变形静力线弹性 PINN（二维/三维配置）
```

## 维护边界

- 通用流程只定义跨方法复用的环节、产物和验收职责，不包含具体方程或单次运行数字。
- 方法实例说明如何将通用环节映射到具体数学问题和训练信号；当前软件实现的源码指针作为附录证据，不定义方法流程。
- 线弹性 PINN、PIML 或其他方法工作流进入本目录，不进入 `technical-lines/`。
- 程序、runner、测试和 checkpoint 继续由对应实现仓库维护，本知识库只保存方法、接口和经核实结论。
- 页面迁移使用 frontmatter `aliases` 保持 append-only [[../../log]] 中的历史路径可解析。

## 关联入口

- [[../technical-lines/_index]] — PIML、Matrix-Free、GPU/HPC 三条长期技术线。
- [[../_index]] — Research 总入口。
- [[../../concepts/piml/ml-roles-and-boundaries]] — 计算力学机器学习路线的学习对象与角色边界。
