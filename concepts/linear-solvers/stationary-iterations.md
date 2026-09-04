---
title: "定常迭代法"
type: concept
aliases:
  - Stationary Iterative Methods
  - 经典迭代法
  - Jacobi 迭代
  - Gauss-Seidel 迭代
  - SOR
  - Richardson 迭代
  - 矩阵分裂
tags:
  - numerical-algebra
  - linear-solver
  - stationary-iteration
  - smoother
status: draft
date_added: 2026-09-03
date_update: 2026-09-03
---

# 定常迭代法

> 定常迭代把 $\mathbf A$ 分裂为易逆的 $\mathbf M$ 与余项 $\mathbf N$，每步用同一个固定算子 $\mathbf G=\mathbf I-\mathbf M^{-1}\mathbf A$ 更新解，收敛当且仅当 $\rho(\mathbf G)<1$，收敛率完全由谱半径决定。对椭圆型有限元问题它随网格加密而退化，今天不再作独立求解器，而是作为 Krylov 的预条件子和多重网格的光滑子存在。

## 1. 分裂格式与收敛判据

取 $\mathbf A=\mathbf M-\mathbf N$，其中 $\mathbf M$ 易于求逆，则 $\mathbf A\mathbf x=\mathbf b$ 等价于不动点方程 $\mathbf x=\mathbf M^{-1}\mathbf N\mathbf x+\mathbf M^{-1}\mathbf b$，对应迭代

$$
\mathbf x_{k+1}=\mathbf M^{-1}\mathbf N\mathbf x_k+\mathbf M^{-1}\mathbf b
=\mathbf G\mathbf x_k+\mathbf c,\qquad
\mathbf G=\mathbf I-\mathbf M^{-1}\mathbf A .
$$

误差 $\mathbf e_k=\mathbf x_k-\mathbf x$ 满足 $\mathbf e_{k+1}=\mathbf G\mathbf e_k$，故 $\mathbf e_k=\mathbf G^k\mathbf e_0$。对任意初值收敛当且仅当谱半径 $\rho(\mathbf G)<1$，渐近收敛率为 $\rho(\mathbf G)$。整个过程中 $\mathbf G$ 不变，没有任何自适应余地，这是它与 [[krylov-subspace-methods|Krylov 方法]]的本质区别。

等价的残差修正形式为 $\mathbf x_{k+1}=\mathbf x_k+\mathbf M^{-1}(\mathbf b-\mathbf A\mathbf x_k)$：每步用 $\mathbf M^{-1}$ 近似 $\mathbf A^{-1}$ 作用于残差，这正是[[preconditioning|预条件]]的原型。

## 2. 经典格式

取 $\mathbf A=\mathbf D-\mathbf L-\mathbf U$（对角、严格下三角、严格上三角）：

| 方法 | $\mathbf M$ | 特点 |
|---|---|---|
| Richardson | $\omega^{-1}\mathbf I$ | 最简单的一阶格式，$\omega$ 需按谱区间选取；SPD 时最优 $\omega=2/(\lambda_{\min}+\lambda_{\max})$ |
| Jacobi | $\mathbf D$ | 各分量可同时更新，天然并行；阻尼 Jacobi 取 $\mathbf M=\omega^{-1}\mathbf D$ |
| Gauss-Seidel | $\mathbf D-\mathbf L$ | 用已更新分量，串行依赖；对一致排序矩阵收敛率约为 Jacobi 的平方 |
| SOR | $\omega^{-1}\mathbf D-\mathbf L$ | Gauss-Seidel 的超松弛，$\omega$ 取最优时收敛阶显著改善，但最优 $\omega$ 依赖谱信息 |
| 对称 Gauss-Seidel / SSOR | 前向一遍加后向一遍 | 得到对称的 $\mathbf M$，可作 SPD 问题的预条件子 |

Jacobi 与 Gauss-Seidel 对严格对角占优或对称正定矩阵收敛；SOR 对 SPD 矩阵在 $0<\omega<2$ 时收敛。Gauss-Seidel 的串行依赖在并行中通过红黑排序或多色排序解除，代价是收敛率略降。

## 3. 网格依赖与光滑性质

对二阶椭圆问题的有限元离散，网格尺寸 $h$ 减小时 $\rho(\mathbf G)$ 趋近于 1：Jacobi 与 Gauss-Seidel 为 $1-O(h^2)$，最优 SOR 为 $1-O(h)$。迭代次数随自由度数增长，因此它们不再作为独立求解器。

它们保留下来的价值来自光滑性质：对 $\mathbf G$ 的特征分解，对应高频（振荡）特征向量的特征值远小于 1，少数几步迭代就能把误差中的高频分量压掉，剩下的是在当前网格上看起来光滑的低频分量。这一性质在[[multigrid|多重网格]]中被系统利用：细网格上做几步定常迭代作为光滑子，低频分量交给粗网格处理。

## 4. 在求解器体系中的位置

- 作为 [[krylov-subspace-methods|Krylov]] 的预条件子：Jacobi 预条件即对角缩放，SSOR、块 Jacobi 是最常见的一批廉价预条件子，见 [[preconditioning]]。
- 作为[[multigrid|多重网格]]的光滑子：阻尼 Jacobi、Gauss-Seidel、Chebyshev 多项式光滑是标准选择，并行环境下常用 Chebyshev 或多色 Gauss-Seidel。
- 作为独立求解器只在小规模或强对角占优问题中出现。

## 参考文献

[1] SAAD Y. Iterative Methods for Sparse Linear Systems[M]. 2nd ed. Philadelphia: SIAM, 2003. §4 定常迭代、分裂与收敛定理。**refs.bib 尚无条目。**
[2] VARGA R S. Matrix Iterative Analysis[M]. 2nd ed. Berlin: Springer, 2000. 正则分裂、SOR 最优松弛因子理论。**refs.bib 尚无条目。**
[3] BRIGGS W L, HENSON V E, MCCORMICK S F. A Multigrid Tutorial[M]. 2nd ed. Philadelphia: SIAM, 2000. §2 定常迭代的光滑性质。**refs.bib 尚无条目。**
