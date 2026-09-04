---
title: "子结构载体 EA Matrix-Free 算子"
type: concept
aliases:
  - mf-ea-substructural
  - mf-substructural
  - 子结构 EA Matrix-Free
  - substructure-carrier EA matrix-free operator
tags:
  - matrix-free
  - static-condensation
  - schur-complement
  - finite-element
  - operator
status: in-progress
date_added: 2026-08-26
date_update: 2026-09-03
---

# 子结构载体 EA Matrix-Free 算子

子结构静力缩聚（[[../substructural-condensation]]）得到的全局接口系统可以不经显式装配、直接以算子形式进入迭代求解。本页给出该算子的定义、与显式装配的代数恒等、边界条件的子空间表述和对角闭式。按 [[assembly-levels]] 的五级口径，它属 EA 级存储语义、以子结构为载体。

## 1. 接口空间与限制、延拓

设缩聚后的全局接口自由度集合为 $\{1,\dots,n_\Gamma\}$，全域划分为 $B$ 个子结构。第 $j$ 个子结构保留 $n_b$ 个接口自由度，其局部—全局编号由单射

$$
g_j:\ \{1,\dots,n_b\}\ \hookrightarrow\ \{1,\dots,n_\Gamma\}
$$

给出。定义布尔限制矩阵

$$
\mathbf L_j \in \{0,1\}^{n_b \times n_\Gamma},
\qquad
(\mathbf L_j)_{k\ell} = \delta_{\ell,\, g_j(k)}.
$$

限制 $(\mathbf L_j \mathbf x)_k = x_{g_j(k)}$ 取出子结构 $j$ 的局部分量；转置 $\mathbf L_j^{\mathsf T}$ 是对应的延拓，把局部向量送回全局编号位置。$g_j$ 单射保证 $\mathbf L_j \mathbf L_j^{\mathsf T} = \mathbf I_{n_b}$；相邻子结构共享接口自由度，即各 $g_j$ 的像有重叠，同一全局自由度可被多个子结构选中，延拓求和时这些贡献相加。

## 2. 算子定义与性质

局部数据是各子结构的缩聚刚度 $\mathbf K_s^j \in \mathbb{R}^{n_b \times n_b}$（精确时即 Schur 补，推导见 [[../substructural-condensation#2. Schur 补静力缩聚的严谨数学推导|静力缩聚 §2]]）。全局接口算子定义为

$$
\mathbf A \;:=\; \sum_{j=1}^{B} \mathbf L_j^{\mathsf T}\, \mathbf K_s^{j}\, \mathbf L_j \;\in\; \mathbb{R}^{n_\Gamma \times n_\Gamma},
$$

其矩阵—向量作用按右结合顺序求值：

$$
\mathbf y \;=\; \mathbf A\,\mathbf x \;=\; \sum_{j=1}^{B} \mathbf L_j^{\mathsf T}\Big(\mathbf K_s^{j}\big(\mathbf L_j\,\mathbf x\big)\Big),
$$

任一时刻只出现局部向量与局部矩阵，$n_\Gamma \times n_\Gamma$ 的全局矩阵从不形成。

由二次型

$$
\mathbf x^{\mathsf T} \mathbf A\, \mathbf x \;=\; \sum_{j=1}^{B} (\mathbf L_j \mathbf x)^{\mathsf T}\, \mathbf K_s^{j}\, (\mathbf L_j \mathbf x)
$$

直接得到两条性质：各 $\mathbf K_s^j$ 对称则 $\mathbf A$ 对称；各 $\mathbf K_s^j$ 对称正定且每个全局接口自由度至少被一个子结构覆盖（$\bigcup_j \operatorname{im} g_j = \{1,\dots,n_\Gamma\}$）时，$\mathbf x^{\mathsf T}\mathbf A\mathbf x = 0$ 迫使所有 $\mathbf L_j\mathbf x = \mathbf 0$，进而 $\mathbf x = \mathbf 0$，故 $\mathbf A$ 对称正定。

以上及后续各节的结论只用到这两条代数性质，不依赖 $\mathbf K_s^j$ 的来源：精确 Schur 补、PIML 预测 $\widehat{\mathbf K}_s^j$（[[../piml/piml-substructural]]）或人工构造的对称正定矩阵均可代入。

## 3. 与显式装配的代数恒等

显式路径（[[../substructural-condensation#5. 八步通用算法逻辑与伪代码|8 步缩聚算法]]第 6 步）先累加 $\mathbf K_{\text{global}} = \sum_j \mathbf L_j^{\mathsf T}\mathbf K_s^j\mathbf L_j$ 再乘向量；算子路径逐子结构作用后求和。由矩阵乘法对加法的分配律，

$$
\mathbf K_{\text{global}}\,\mathbf x
\;=\;
\Big(\sum_{j}\mathbf L_j^{\mathsf T}\mathbf K_s^{j}\mathbf L_j\Big)\mathbf x
\;\equiv\;
\sum_{j}\mathbf L_j^{\mathsf T}\Big(\mathbf K_s^{j}\big(\mathbf L_j\mathbf x\big)\Big).
$$

分量层面看得更清楚：两条路径下结果向量的第 $\ell$ 个分量都是

$$
y_\ell \;=\; \sum_{j}\ \sum_{k,\,k'} (\mathbf L_j)_{k\ell}\,\big(\mathbf K_s^j\big)_{kk'}\,x_{g_j(k')},
$$

即两条路径求和的是同一组贡献，只是归并的先后不同——显式路径先按矩阵元位置归并（装配时加），算子路径先按子结构归并（作用时加）。

归并次序进一步带来一处差别：显式路径把落在同一矩阵元 $(\ell,m)$ 的各子结构贡献先加成 $(\mathbf K_{\text{global}})_{\ell m}$，再与 $x_m$ 相乘，即把 $x_m$ 提到了对 $j$ 的求和之外——这正是分配律而非单纯的结合律。因此两条路径连乘法次数都不同：算子路径做 $B\,n_b^2$ 次，显式路径只做 $\operatorname{nnz}(\mathbf K_{\text{global}})$ 次。乘积项集合并不逐项相同，相同的是它们的和。

因此这不是用算子近似矩阵，而是同一个和的两种求值次序，精确算术下恒等。

浮点算术下加法不满足结合律，两条路径的结果不逐位相同，但差异只来自求和次序，相对偏差在机器精度量级（$10^{-16}$）。一致性判据阈值取 $10^{-13}$，其诊断逻辑是反向的：超出该阈值的偏差不可能由舍入产生，唯一解释是两条路径求和的不是同一组项，即编号映射 $g_j$ 或散加逻辑有错。该判据由此区分「精度问题」与「索引错误」：通过即实现与数学定义恒等，不通过即直接指向索引错误。

## 4. 边界条件的子空间表述

设接口自由度分为自由集 $F$ 与约束集 $C$，$\mathbf P_f$ 为向 $F$ 的布尔限制。约束后的求解对象是自由子空间上的算子

$$
\mathbf A_f \;:=\; \mathbf P_f\, \mathbf A\, \mathbf P_f^{\mathsf T},
$$

其矩阵—向量作用同样按右结合顺序求值：

$$
\mathbf y_f \;=\; \mathbf A_f\,\mathbf x_f \;=\; \mathbf P_f\Big(\mathbf A\big(\mathbf P_f^{\mathsf T}\,\mathbf x_f\big)\Big),
$$

即零嵌入（$\mathbf P_f^{\mathsf T}$ 把自由分量放回全接口编号、约束位置补零）、全空间作用（§2 的作用式）、限制回自由集三步。$\mathbf A_f$ 与显式路径中取子块 $\mathbf K_{\text{global}}[F,F]$ 恒等（消元法语义），谱中不含被约束方向的伪零模。

非齐次 Dirichlet 条件下，令 $\mathbf u = \mathbf P_f^{\mathsf T}\mathbf u_f + \mathbf u_c$，其中 $\mathbf u_c$ 只在 $C$ 上取给定值。代入 $\mathbf A\mathbf u = \mathbf g$ 并限制到 $F$：

$$
\mathbf A_f\, \mathbf u_f \;=\; \mathbf P_f\big(\mathbf g - \mathbf A\,\mathbf u_c\big).
$$

右端反力项 $-\mathbf P_f \mathbf A \mathbf u_c$ 需要 $\mathbf A$ 在全接口空间上的作用，无法由 $\mathbf A_f$ 表达；两种作用共享同一批 $\{\mathbf K_s^j\}$。

## 5. 对角的闭式

$g_j$ 单射使 $\mathbf L_j$ 的每一列至多有一个非零元，交叉项全部消失：

$$
(\mathbf A)_{\ell\ell}
= \sum_{j}\sum_{k,k'} (\mathbf L_j)_{k\ell}\,(\mathbf K_s^j)_{kk'}\,(\mathbf L_j)_{k'\ell}
= \sum_{j:\ \ell \in \operatorname{im} g_j} \big(\mathbf K_s^j\big)_{g_j^{-1}(\ell),\, g_j^{-1}(\ell)},
$$

即

$$
\operatorname{diag}(\mathbf A) \;=\; \sum_{j=1}^{B} \mathbf L_j^{\mathsf T}\, \operatorname{diag}\!\big(\mathbf K_s^{j}\big).
$$

对角无需任何算子作用即可获得，Jacobi 类预条件由此直接可得；迭代机制见 [[../linear-solvers/krylov-subspace-methods]]，各类预条件子的信息需求见 [[../linear-solvers/preconditioning]]。

## 来源与相关页面

- [[../substructural-condensation]] — $\mathbf K_s^j$ 的数学来历（§2）与被替换的第 6 步（§5）。
- [[assembly-levels]] — 五级装配层次口径，本页 EA 定位的判据来源。
- [[../linear-solvers/krylov-subspace-methods]] — 算子之上的迭代求解机制；预条件见 [[../linear-solvers/preconditioning]]。
- [[../piml/piml-substructural]] — $\mathbf K_s^j$ 的 PIML 预测来源；该页管局部矩阵怎么学出来，本页管怎么作用。
- [[../../research/piml-matrix-free-gpu/matrix-free-research-guide]] — 研究定位，含与积分点级 PA 的范式区分。
- `soptx:src/soptx/fem/substructure/operator.py` — 实现（主作用、`apply_full`、`diagonal`）。
- `soptx:examples/matrix_free_substructure_elasticity/verify_matrix_free_ea.py` — 统一验证：算子级七项判据（单次作用恒等）+ 求解级四项判据（裸 CG 端到端一致，显式矩阵整个拿掉）；实测数值的唯一事实源是同目录 `results_analysis.md`。
