---
title: "子结构 Schur 补算子的 PA 结合"
type: concept
aliases:
  - mf-pa-schur-substructural
  - 子结构 Schur 补 PA 算子
  - Partial assembly for Schur complement substructuring
tags:
  - matrix-free
  - partial-assembly
  - substructure
  - static-condensation
  - schur-complement
  - operator
status: draft
date_added: 2026-10-05
date_update: 2026-10-25
---

# 子结构 Schur 补算子的 PA 结合

> [[mf-schur-substructural|子结构 Schur 补算子]] 的单元层采用共享参考 EA。改为 PA 时，局部刚度的算子作用可直接替换，卡点在在线必需的内部求逆 $(\mathbf K_{ii}^j)^{-1}$：PA 不保存显式矩阵，无法直接分解。本页给出三种结合方式与适用判断，为基于 [[assembly-levels]] 层级权衡的推导，未引用专门讨论子结构与 PA 结合的文献。PIML 路线不需要在线内部求逆，见 [[mf-pa-piml-substructural]]。

## 1. 单元层需求

### 1.1 两层装配层级

子结构方法有两层映射：单元到子结构，子结构到全局接口，两层的装配层级可以分别选择。子结构层保存局部缩聚刚度时与 EA 同形：$\mathbf K_{s,\mathrm{corner}}^j$ 对应 $\mathbf K_e$，$\mathbf A_c^j$ 对应 $\mathbf G_e$，
$$
\mathbf K_C\mathbf x=\sum_j(\mathbf A_c^j)^{\mathsf T}\mathbf K_{s,\mathrm{corner}}^j\mathbf A_c^j\mathbf x
\quad\text{与}\quad
\sum_e\mathbf G_e^{\mathsf T}\mathbf K_e\mathbf G_e\mathbf x
$$
形式相同；完整接口路径不保存 $\mathbf K_s^j$、每次现算，对应该层不保存、逐次构造。本页只讨论单元层由[[assembly-levels#2.3.2 共享参考 EA：只保存 $\mathbf K_e^0$ 与 $s_e$|共享参考 EA]] 改为 [[assembly-levels#2.4 PA/QA：积分点数据作用|PA]]，子结构层两条接口路径不变。

### 1.2 两类需求

| 需求 | 在 [[mf-schur-substructural]] 中的位置 | PA 能否提供 |
|---|---|---|
| 算子作用 $\mathbf K_{bb}^j\mathbf x$、$\mathbf K_{ib}^j\mathbf x$ | §2 第 1 条缩聚作用、§3 第 1 条角点刚度形成、载荷修正 | 能，即 gather → $\mathbf B_e$ → $\mathbf D_e$ → $\mathbf B_e^{\mathsf T}$ → scatter-add |
| 内部求逆 $(\mathbf K_{ii}^j)^{-1}\mathbf r$ | §2 第 1 条每次缩聚作用、§3 第 1 条角点 setup、§1 第 2 条位移恢复 | 不能直接提供：稀疏直接分解需要显式矩阵元素，PA 不保存 |

内部求逆在线必需，PA 下只能二选一：由积分点数据现算单元矩阵后组装内部块，或改用以 PA 为算子的迭代求解。

## 2. 三种结合方式

1. **作用用 PA，$\mathbf K_{ii}^j$ 仍组装并分解。** 由积分点数据现算单元矩阵、只组装内部块后做 Cholesky。可行，但子结构的主要存储是 $\mathbf K_{ii}^j$ 的分解因子，PA 只替换了边界耦合块的作用，收益有限。
2. **内部求解改为迭代。** $\mathbf K_{ii}^j\mathbf v_i=\mathbf r$ 以 PA 算子作 PCG，整条链不再需要显式矩阵。
   - 配完整接口：外层接口 CG 每次迭代都要在每个子结构内做一次内层 PCG，形成嵌套迭代；内层近似求解使缩聚算子只在内层容差内对称，外层需用 flexible CG 或收紧内层容差，“精确算术下与显式路径恒等”相应弱化为“在内层容差内一致”。
   - 配角点接口：内部求解只出现在 setup，每个子结构对 $n_c^j$ 个右端各解一次（三维六面体子结构 $n_c^j=24$），之后只保存 $\mathbf K_{s,\mathrm{corner}}^j$ 与可选的 $\mathbf T_{\mathrm{corner}}^j$，作用阶段不再涉及 $\mathbf K_{ii}^j$。多右端可用块 Krylov 或共享预条件分摊。
3. **以高阶单元为子结构（单元级静态凝聚）。** 把每个 $p$ 阶张量积单元视为子结构，凝聚单元内部（气泡）自由度。内部块继承张量积结构，可分离算子可用快速对角化（fast diagonalization）求逆而不显式分解（来源待确认）。[[../../literature/topopt/matrix-free/translations/Fu2023-high-order-structured-diff-topopt-zh#4.3 精度与可扩展性研究|Fu 等 (2023) §4.3]] 对混合 Helmholtz 问题逐单元凝聚 $L^2$ 自由度，属同类做法。

## 3. 适用判断

[[mf-schur-substructural]] 的单元层设定是规则网格、低阶单元、各单元只差标量 $s_e$（SIMP 固定泊松比）。此时共享参考 EA 优于 PA：

- 存储：共享参考 EA 为 $m^2+N_e$，PA 为 $N_e\,n_q\,c$（$c$ 为每积分点数据个数），后者更大；
- 计算：PA 的计算优势依赖张量积单元上的 sum factorization，加速比 $p^{d-1}$（[[assembly-levels#2.4.3 存储与代价|§2.4.3]]），低阶时约为 1。

满足下列任一条件时，单元层改用 PA 才有收益：

- 子结构内采用高阶张量积单元，共享参考单元矩阵 $m^2$ 随 $p^{2d}$ 增长，apply 代价同阶；
- 网格不规则或单元形状各异，共享参考 EA 的前提不成立，标准 EA 存储为 $N_e m^2$；
- 需在 GPU 等设备上避免稀疏直接分解，此时宜取 §2 第 2 种方式配角点接口。

## 参考依据

- [[assembly-levels]]：装配层级定义、共享参考 EA 的前提与存储、PA 的存储与 sum factorization 代价（§2.3.2、§2.4、§2.4.3）；§3 的存储与计算比较据此推导。
- [[mf-schur-substructural]]、[[../substructure/exact-substructural]]：内部求逆在两条接口路径与位移恢复中的出现位置；§2 的三种结合方式及嵌套迭代、精度弱化的分析为本页推导。
- [[../../literature/topopt/matrix-free/translations/Fu2023-high-order-structured-diff-topopt-zh|Fu 等 (2023)]]：逐单元静态凝聚 $L^2$ 自由度的实例（§4.3）。
- 快速对角化求逆内部块、内层近似求解对外层 CG 的影响：本库尚无文献页，待确认。
