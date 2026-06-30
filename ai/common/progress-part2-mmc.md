---
title: "进度与决策 · 考核 Part 2 / MMC 显式几何与高阶网格切割（分支）"
tags:
  - progress
  - decision-log
  - defense
  - MMC
  - MMV
status: "in-progress"
date: 2026-06-30
related:
  - soptx-mmc-integration-plan
  - mmc_math_principles
  - mmc-mmv-numerical-discretization-survey
  - one-week-defense-sprint-plan
---

# 进度与决策 · 考核 Part 2 / MMC 显式几何与高阶网格切割（分支）

> 本文件是 [[status]]（AI 接续入口 hub）下「考核 Part 2 / MMC 方向二」工作线的**分支**，记录细节与决策。
> 进度推进时更新本文件，并同步 [[status]] 对应行。

## 1. 一句话现状

面向答辩冲刺，**“能力 C”的范围已明确收敛**：不开发完整的优化闭环，仅展示**显式几何对高阶背景网格的精确切割与高阶积分点布设**。目前已完成理论和集成计划的构建，锁定了三篇必读核心文献，正准备进入代码绘图阶段（T1→V1）。

## 2. 答辩 deck（`talks/2026-postdoc-entry-assessment/template-8min.tex`）

| 帧 | 状态 | 下一步 |
|---|---|---|
| 帧 8 · 方向二 MMC | LaTeX 目前仅有占位 TikZ，且编译存在 `\ifthenelse` 报错 | 待 `mmc_baseline.pdf` 出图后填入，并修复报错 |

**内容口径**：
展示高阶拉格朗日网格被 MMC 组件切割时的精确数值积分能力。以此向评委证明：博士期间积累的“高阶离散/混合元”方法与郭旭团队的“MMC/MMV 显式几何”体系在最底层的**技术映射管线已经打通**，具备切实可行的融合基础。

## 3. 文档体系（MMC 架构支撑）

| 层 | MMC/MMV 显式拓扑优化方向 |
|---|---|
| 总体调研 | `mmc-mmv-numerical-discretization-survey` |
| 数学原则 | `mmc_math_principles` |
| 集成计划 | `soptx-mmc-integration-plan` |

## 4. 关键决策记录（本会话，2026-06-30）

1. **目标收敛**：放弃在短期内编写完整的 MMC 优化 Demo，将答辩展示目标明确锁定在“**前向几何映射与精确切割积分图**”的生成。这能用最小的开发成本给出最硬核的基础证明。
2. **文献聚焦**：确立了三篇必读核心文献，覆盖底座与拔高防守：
   - SMO 2016（Zhang et al.）：MMC 基础框架与 TDF 描述（附 188 行代码基准）。
   - CMAME 2017（Zhang et al.）：MMV 孔洞演化框架。
   - CMAME 2016（Zhang et al.）：基于 XFEM 的精确边界积分与尺度控制（指导如何在切割网格上精确布设积分点）。

## 5. 阅读状态

- **待读（最高优）**：Zhang W, et al. SMO 2016 (A new topology optimization approach based on MMC...) —— 作为接下来 Demo 代码编写的直接数学公式参考。
- **待读（防守与拔高）**：Zhang W, et al. CMAME 2016 (XFEM 精确边界积分)；Zhang W, et al. CMAME 2017 (MMV)。

## 6. 下一步待办

- [ ] 研读 SMO 2016 及配套 188 行 MATLAB 代码的 TDF 定义逻辑。
- [ ] 按照 `soptx-mmc-integration-plan` 执行 **T1→T2→V1**，编写 Python 脚本产出 `mmc_baseline.pdf` 矢量图。
- [ ] 修复 LaTeX 帧 8 的 `\ifthenelse` 报错并将矢量图插入。
