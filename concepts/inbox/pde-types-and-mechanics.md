---
title: "偏微分方程的类型与典型力学问题"
type: concept
tags:
  - partial-differential-equations
  - linear-elasticity
status: done
date_added: 2026-11-09
date_update: 2026-11-09
---

# 偏微分方程的类型与典型力学问题

下表选取三个常见的二阶模型，以固体静力平衡、瞬态导热和一维波动分别说明椭圆型、抛物型和双曲型方程，并对照它们在有限区域上的定解条件。

| 方程类型 | 典型问题 | 代表方程 | 定解条件 |
| --- | --- | --- | --- |
| **椭圆型** | **固体静力边值问题** | 线弹性静力平衡方程（位移形式） $-\mu\Delta\boldsymbol u-(\lambda+\mu)\nabla(\nabla\cdot\boldsymbol u)=\boldsymbol b$ | **边值条件**：给定位移或面力。 |
| **抛物型** | 瞬态导热 | 一维热传导方程 $T_t=\alpha T_{xx}$ | **初边值条件**：初始温度和热边界条件。 |
| **双曲型** | 一维结构振动与波动 | 一维波动方程 $u_{tt}=c^2u_{xx}$ | **初边值条件**：初始位移、初始速度和端部边界条件。 |

第一行采用均匀、各向同性的小变形线弹性模型，$\lambda,\mu$ 为 Lamé 常数。将 Hooke 定律代入静力平衡方程 $-\nabla\cdot\boldsymbol\sigma(\boldsymbol u)=\boldsymbol b$ 即得表中的位移形式，推导所用的应变、本构关系及边界条件见 [[linear-elasticity|线弹性方程、变分形式与有限元离散]]。热传导与波动的标准模型可参见 L. C. Evans《Partial Differential Equations》第 2 章 §§2.3–2.4。
