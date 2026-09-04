---
title: "预条件"
type: concept
aliases:
  - Preconditioning
  - Preconditioner
  - 预条件子
  - 预条件器
  - Jacobi 预条件
  - ILU
tags:
  - numerical-algebra
  - linear-solver
  - preconditioning
status: draft
date_added: 2026-09-03
date_update: 2026-09-03
---

# 预条件

> 预条件用易于求逆的 $\mathbf M\approx\mathbf A$ 把方程组换成谱更聚集的等价问题，是决定 Krylov 方法在大规模问题上是否可用的关键。不同预条件子对矩阵信息的需求差异极大：Jacobi 只要对角元，ILU 与 AMG 要显式稀疏矩阵，几何多重网格要网格层次；「主算子不显式组装时预条件子还能怎么构造」由这张需求表回答。

## 1. 形式与目标

条件数 $\kappa(\mathbf A)$ 过大时 Krylov 收敛缓慢。预条件寻找易于求逆的 $\mathbf M\approx\mathbf A$，改为求解等价方程组

$$
\underbrace{\mathbf M^{-1}\mathbf A\mathbf x=\mathbf M^{-1}\mathbf b}_{\text{左预条件}},\qquad
\underbrace{\mathbf A\mathbf M^{-1}\mathbf y=\mathbf b,\ \ \mathbf x=\mathbf M^{-1}\mathbf y}_{\text{右预条件}},\qquad
\underbrace{\mathbf M_1^{-1}\mathbf A\mathbf M_2^{-1}\mathbf y=\mathbf M_1^{-1}\mathbf b}_{\text{分裂预条件}} .
$$

目标不是把 $\kappa$ 压到 1，而是让 $\mathbf M^{-1}\mathbf A$ 的特征值聚集在少数几簇附近，因为 [[krylov-subspace-methods|Krylov]] 的收敛由谱分布而非单一条件数决定。左预条件改变了残差范数（GMRES 极小化的是 $\lVert\mathbf M^{-1}\mathbf r\rVert$），右预条件保持真残差，工程上判停机时须分清。

SPD 情形下 PCG 只需 $\mathbf M$ 对称正定，实现上不必显式对称化：算法在 $\mathbf M$ 内积下运行，每步多一次 $\mathbf z=\mathbf M^{-1}\mathbf r$ 的作用。若 $\mathbf M$ 不对称（如单向 Gauss-Seidel），CG 的理论不再成立，须改用 GMRES 或换对称预条件子；$\mathbf M$ 随迭代变化（内层再套一个迭代求解器）时须用 Flexible GMRES 一类变体。

## 2. 每类预条件子需要什么信息

| 预条件子 | 需要的信息 | 说明 |
|---|---|---|
| Jacobi / 对角缩放 | 对角元 | 最廉价，任何能取到对角的表示都可用；对系数跳跃问题效果有限 |
| 块 Jacobi、Gauss-Seidel、SSOR | 对角块或矩阵行 | [[stationary-iterations|定常迭代]]作预条件子的形式 |
| 不完全分解 ILU(k) / IC(k) / ILUT | 稀疏矩阵元素 | 需要显式稀疏矩阵及其稀疏结构；串行本质强，并行需按分区做块 ILU |
| 多项式预条件 | 谱区间估计 | 只需算子作用，用 Chebyshev 多项式近似 $\mathbf A^{-1}$ |
| 代数多重网格 AMG | 矩阵元素及 strength-of-connection | 粗化完全由矩阵元素驱动 |
| 几何多重网格 GMG | 网格层次与层间转移算子 | 不需要矩阵元素，但需要几何层次；细节见 [[multigrid]] |
| 区域分解 / Schwarz | 子域局部矩阵，可选粗空间 | 与并行分区天然匹配；一层 Schwarz 收敛随子域数退化，加粗空间后可扩展 |
| 低阶 / 代理算子 | 一个更易组装的近似算子 | 高阶算子用低阶组装矩阵作预条件，或用降阶模型近似 |

这张表决定了「当主算子不显式组装时，预条件子还能怎么构造」：装配层级约束的是预条件器而不是求解器，主算子与预条件子可以取不同层级，判据与推导由 [[../matrix-free/assembly-levels#3. 三条跨层级不变量]] 不变量 3 维护。

## 3. 代价核算

预条件的总代价分三部分，性能报告须分别注明：

- **setup**：构造 $\mathbf M$ 的一次性成本，ILU 与 AMG 的 setup 可能与若干次求解相当；
- **apply**：每步 Krylov 迭代作用一次 $\mathbf M^{-1}$ 的成本，需与算子作用同量级比较；
- **update**：矩阵变化后（拓扑优化中每次材料分布更新）$\mathbf M$ 是重建、局部更新还是复用。

一个预条件子值得用，当且仅当减少的迭代次数乘以每步节省，超过 setup 与 apply 增加的总量。矩阵频繁变化的场景中 update 成本往往主导取舍。

## 参考文献

[1] SAAD Y. Iterative Methods for Sparse Linear Systems[M]. 2nd ed. Philadelphia: SIAM, 2003. §9 预条件迭代、§10 预条件技术（ILU、多项式、块预条件）、§14 区域分解。**refs.bib 尚无条目。**
[2] BENZI M. Preconditioning techniques for large linear systems: a survey[J]. Journal of Computational Physics, 2002, 182(2): 418-477. 预条件技术综述。**refs.bib 尚无条目。**
[3] WATHEN A J. Preconditioning[J]. Acta Numerica, 2015, 24: 329-376. 谱聚集而非条件数作为预条件目标的论述。**refs.bib 尚无条目。**
