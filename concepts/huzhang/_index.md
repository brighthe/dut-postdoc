---
title: "Hu–Zhang 混合有限元术语与主题入口"
type: index
tags:
  - Hu-Zhang
  - mixed-fem
  - elasticity
  - topology-opt
status: in-progress
date_added: 2026-08-09
date_update: 2026-08-09
---

# Hu–Zhang 混合有限元术语与主题入口

> 本页连接 Hu–Zhang 混合有限元（Hu–Zhang Mixed Finite Element Method）的理论基础、程序实现、实测收敛证据与拓扑优化论文进展。核心方法指基于对称应力和位移为独立未知量的 $H(\mathrm{div})$ 协调混合有限元方法；在低阶 $k=1,2$ 时配套位移跳量稳定化，在复杂边界角点配套切向顶点松弛。**命名边界**：本主题指上述混合元方法本身及其在拓扑优化中的应用，不代表任意「混合有限元」的通用理论；当前研究产出以论文主线推进，`research/technical-lines/` 下没有独立的 Hu–Zhang 技术线。

## 稳定知识

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[huzhang-mixed-fem]] | Hellinger–Reissner 变分原理、鞍点代数结构、集中载荷的共同离散牵引、跳量稳定化缩放律与角点部分顶点松弛理论 | in-progress |
| [[../linear-elasticity]] | 位移型线弹性基础、强/弱形式与古典位移元对比（本页的出发问题） | in-progress |

## 鞍点结构与稳定化

> 本节只提供主题地图；不复制变分推导、稳定化缩放律证明、收敛阶估计或程序实测数字。

```text
对称应力 σ (H(div) 协调) + 位移 u  ——两个独立未知量
  -> Hellinger–Reissner 变分 -> 离散鞍点系统 [A B^T; B 0]
  -> 低阶 k=1,2：位移跳量稳定化
  -> 复杂边界角点：切向顶点部分松弛
```

应力被提升为主未知量，代价是方程从正定变为鞍点，低阶与角点两处各需一项补救；三者的推导、缩放律与适用边界由 [[huzhang-mixed-fem]] 维护。

### 程序实现必读入口

启动或讨论 SOPTX 代码仓库中的 Hu–Zhang 混合有限元程序实现前，按下表进入相应的架构设计、代数规范与实测事实源。

```text
理论概念 (Theory) -> 软件架构 (Architecture) -> 算例规范 (Math Spec) -> 实测数据 (Results)
```

| 入口 | 路径 | 职责与定位 |
|---|---|---|
| **软件架构 (Architecture)** | `soptx:docs/fem/huzhang-mixed-fem-implementation.md` | `soptx.fem` 底层类图、`A/B/J` 组装器、FEALPy 4.0 接口兼容与测试套件 |
| **算例规范 (Math Spec)** | `soptx:examples/huzhang_elasticity/math_spec.md` | 符号-代码 1 对 1 映射表、离散鞍点方程代数形式、双验收标准 |
| **实测数据 (Results)** | `soptx:examples/huzhang_elasticity/results_analysis.md` | 收敛误差实测数据、观测阶、相对残差与诊断分析报告；实测数值与证据 provenance 的唯一事实源 |

跨仓库路径一律使用 `repo:path` 相对写法，不写机器绝对路径。

## 项目与论文路线入口

> 本主题当前没有独立的 `research/technical-lines/` 技术线，研究产出以下列论文主线推进；这是本页与其他主题入口在该节命名上的唯一差异。

| 视图 | 路径 / 链接 | 职责与定位 |
|---|---|---|
| **投稿大纲 (Outline)** | [[../../papers/arbitrary-order-huzhang-topopt-outline]] | 投稿目标 CICP 规格、7 个 Case 证据矩阵、投稿门禁规划 |
| **中文初稿 (Draft)** | [[../../papers/arbitrary-order-huzhang-topopt-draft-zh]] | 论文中文初稿全文（包含第 4.1 节高低阶前向收敛双表与第 4.2 节拓扑优化算例） |

## 文献证据

- **Hu 2015**: Hu, J. Finite element approximations of symmetric tensors on simplicial grids in $\mathbb{R}^n$: the higher order case. *Journal of Computational Mathematics*, 2015. DOI: `10.4208/jcm.1412-m2014-0071`.（高阶 Hu–Zhang 空间构造与线性弹性收敛）
- **Chen–Hu–Huang 2018**: Chen, L., Hu, J., Huang, X. Fast auxiliary space preconditioners for symmetric tensor field discretization. *Mathematics of Computation*, 87, 2018.（应力 $L^2$ 误差的 $\mathcal{O}(h^{k+1})$ 超收敛估计）
- **Hu–Ma 2021**: Hu, J., Ma, R. Partial relaxation of $C^0$ vertex continuity of stresses of conforming mixed finite elements for the elasticity problem. *Computational Methods in Applied Mathematics*, 2021. DOI: `10.1515/cmam-2020-0003`.（混合边界转折角点处的切向顶点松弛）
- **Chen 2024 (CICP)**: Chen, C., Chen, L., Huang, X., Wei, H. Geometric decomposition and efficient implementation of high order face and edge elements. *Communications in Computational Physics*, 35, 1045–1072, 2024. DOI: `10.4208/cicp.OA-2023-0249`.（高阶元几何分解与高效装配范式）

## 关联入口

- 关联主题：[[../_index]] — 概念页总索引。
- 关联主题：[[../linear-elasticity]] — 位移型线弹性基础。
- 关联主题：[[../piml/_index]] — Problem-Independent 机器学习主线（材料插值与局部算子学习关联）。

## 管理边界

- 变分推导、鞍点代数结构、稳定化缩放律与角点松弛理论由 [[huzhang-mixed-fem]] 维护；程序架构、算例规范与实测数值分别由上表的 SOPTX 三份文档维护，本页不复制其中任何数字。
- 不在概念页维护论文写作进度、投稿门禁状态或预计交付日期；这些由 [[../../papers/arbitrary-order-huzhang-topopt-outline]] 维护。
- 收敛阶结论必须区分理论估计与本项目实测观测阶，不把文献中的估计直接表述为本项目已复现的结果。
- 新成果只有在论文、预印本、专利或公开软件等来源可核实时，才进入正式时间线。
- 本页不维护容易过期的文件总数，也不登记只因索引、日志、参考文献或顺带讨论而命中关键词的全部文件。
