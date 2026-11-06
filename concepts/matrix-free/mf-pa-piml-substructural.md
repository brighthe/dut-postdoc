---
title: "子结构 PIML 算子的 PA 结合"
type: concept
aliases:
  - mf-pa-piml-substructural
  - 子结构 PIML PA 算子
  - Partial assembly for PIML substructuring
tags:
  - matrix-free
  - partial-assembly
  - piml
  - substructure
  - operator
status: draft
date_added: 2026-10-05
date_update: 2026-10-05
---

# 子结构 PIML 算子的 PA 结合

> [[mf-piml-substructural|子结构 PIML 算子]] 的单元层采用共享参考 EA。PIML 以网络预测替代内部求解，在线阶段不需要 $(\mathbf K_{ii}^j)^{-1}$，路线 A 只需局部刚度的算子作用，单元层可直接改为 PA，其余流程不变。是否值得替换只取决于单元条件。本页为基于 [[assembly-levels]] 层级权衡的推导，未引用专门讨论 PIML 子结构与 PA 结合的文献。精确 Schur 补路线需要在线内部求逆，见 [[mf-pa-schur-substructural]]。

## 1. 单元层需求

单元层由[[assembly-levels#2.3.2 共享参考 EA|共享参考 EA]] 改为 [[assembly-levels#2.4 PA/QA：积分点数据作用|PA]] 时，PA 能提供算子作用 $\mathbf K^j\mathbf v$，不能直接提供内部求逆（稀疏直接分解需要显式矩阵元素，PA 不保存）。两层装配层级的独立性见 [[mf-pa-schur-substructural#1.1 两层装配层级|PA 结合 Schur §1.1]]。按阶段与路线，PIML 的单元层需求为：

| 阶段 / 路线 | 单元层需求 | PA 替换 EA |
|---|---|---|
| 在线，路线 A 完整接口 | 每次接口作用算 $\mathbf K^j[\mathbf x_b;\widehat{\mathbf T}_{\mathrm{full}}^j\mathbf x_b]$（[[mf-piml-substructural#2. 完整接口路径|§2]]） | 直接替换 |
| 在线，路线 A 角点接口 | setup 中对 $\widehat{\mathbf N}_{\mathrm{corner}}^j$ 的 $n_c^j$ 列各作用一次（[[mf-piml-substructural#3. 角点接口路径|§3]]） | 直接替换 |
| 在线，路线 B | 求解阶段不需要 $\mathbf K^j$；内部恢复若改用局部精确求解，需组装并分解 $\mathbf K_{ii}^j$（[[mf-piml-substructural#1. 共同环节|§1]] 第 2 条） | 求解阶段不涉及；精确恢复同 [[mf-pa-schur-substructural#2. 三种结合方式|PA 结合 Schur §2]] 第 1 种方式 |
| 离线，监督训练标签 | 局部精确求解 $\mathbf T^j=-(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j$（[[../piml/piml-substructural#3.2 材料样本与训练目标|PIML §3.2]]） | 需要内部求逆，可离线直接分解，或按 [[mf-pa-schur-substructural#2. 三种结合方式|PA 结合 Schur §2]] 第 2 种方式以 PA 作迭代求解 |
| 离线，无标签能量训练 | 只需 $\mathbf K^j$ 作用于预测形函数（[[../piml/piml-substructural#3.2 材料样本与训练目标|PIML §3.2]]） | 直接替换 |

路线 A 在线阶段与能量训练只涉及算子作用，改用 PA 不改变能量投影的构造，对称半正定性仍由能量投影保证。

## 2. 适用判断

[[mf-piml-substructural]] 的单元层设定是规则网格、低阶单元、各单元只差标量 $s_e$（SIMP 固定泊松比）。此时共享参考 EA 优于 PA：

- 存储：共享参考 EA 为 $m^2+N_e$，PA 为 $N_e\,n_q\,c$（$c$ 为每积分点数据个数），后者更大；
- 计算：PA 的计算优势依赖张量积单元上的 sum factorization，加速比 $p^{d-1}$（[[assembly-levels#2.4.3 存储与代价|§2.4.3]]），低阶时约为 1。

满足下列任一条件时，路线 A 与能量训练改用 PA 才有收益，且可直接替换：

- 子结构内采用高阶张量积单元，共享参考单元矩阵 $m^2$ 随 $p^{2d}$ 增长，apply 代价同阶；
- 网格不规则或单元形状各异，共享参考 EA 的前提不成立，标准 EA 存储为 $N_e m^2$；
- 需在 GPU 等设备上以统一的积分点数据流执行局部作用。

路线 B 求解阶段不涉及单元层，替换与否只影响内部精确恢复与离线标签生成。

## 参考依据

- [[assembly-levels]]：装配层级定义、共享参考 EA 的前提与存储、PA 的存储与 sum factorization 代价（§2.3.2、§2.4、§2.4.3）；§2 的存储与计算比较据此推导。
- [[mf-piml-substructural]]、[[../piml/piml-substructural]]：路线 A/B 的在线作用需求、离线标签生成与能量训练的需求；§1 表格据此整理，替换判断为本页推导。
- [[mf-pa-schur-substructural]]：两层装配层级的独立性、需要内部求逆时的结合方式。
