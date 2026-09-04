---
title: "多重网格"
type: concept
aliases:
  - Multigrid
  - Geometric Multigrid
  - Algebraic Multigrid
  - GMG
  - AMG
  - 几何多重网格
  - 代数多重网格
  - MGCG
tags:
  - numerical-algebra
  - linear-solver
  - multigrid
  - preconditioning
status: draft
date_added: 2026-09-03
date_update: 2026-09-03
---

# 多重网格

> 多重网格把定常迭代只能高效消去高频误差这一缺陷变成分工：细网格上做几步光滑压掉高频，把剩余的低频分量限制到粗网格（在那里它们变成相对高频）求解后再延拓回来校正。对椭圆问题它的收敛率与网格尺寸无关，是少数达到最优复杂度 $O(n)$ 的方法；几何多重网格从网格层次出发，代数多重网格只从矩阵元素出发。实践中它最常作为 Krylov 的预条件子出现。

## 1. 光滑与粗网格校正

[[stationary-iterations|定常迭代]]对二阶椭圆问题的 $\rho(\mathbf G)$ 随网格加密趋近于 1，但其特征分解中对应高频特征向量的特征值远小于 1：少数几步就能把误差中的振荡分量压掉，剩下的是在当前网格上光滑的低频分量。光滑的误差可以在更粗的网格上精确表示，而在粗网格上它们的相对频率翻倍，又变成光滑子能高效处理的对象。两个网格层间的转移由限制算子 $\mathbf R$（细到粗）与延拓算子 $\mathbf P$（粗到细）完成，常取 $\mathbf R=\mathbf P^{\mathsf T}$。

## 2. V-cycle 骨架

一次两层校正扩展为多层递归即 V-cycle：

1. 细网格前光滑：做 $\nu_1$ 步定常迭代（阻尼 Jacobi、Gauss-Seidel、Chebyshev 等）；
2. 计算残差并限制到粗网格：$\mathbf r_H=\mathbf R\,(\mathbf b-\mathbf A\mathbf x)$；
3. 粗网格求解 $\mathbf A_H\mathbf e_H=\mathbf r_H$，递归调用本过程，或在最粗层用[[direct-methods|直接法]]求解；
4. 延拓并校正：$\mathbf x\leftarrow\mathbf x+\mathbf P\mathbf e_H$；
5. 细网格后光滑 $\nu_2$ 步。

W-cycle 在每层递归两次，F-cycle 介于二者之间；全多重网格（FMG）从最粗层起逐层给出初值，一次扫过即可达到离散精度。对椭圆问题，V-cycle 每次的误差压缩因子与 $h$ 无关，总运算量为 $O(n)$。

## 3. 几何与代数多重网格

| | 几何多重网格 GMG | 代数多重网格 AMG |
|---|---|---|
| 层次来源 | 网格加密序列 | 仅由矩阵元素按连接强度（strength-of-connection）粗化 |
| 粗算子 | Galerkin 方式 $\mathbf A_H=\mathbf R\mathbf A\mathbf P$，或在粗网格上重新离散 | Galerkin 方式 |
| 需要的信息 | 网格层次与层间转移算子，不需要矩阵元素 | 显式稀疏矩阵元素 |
| 适用性 | 结构化或可嵌套加密的网格；高阶元用 p-multigrid 在多项式次数上逐级降阶 | 非结构网格、无几何层次的一般 SPD 问题 |
| 典型实现 | deal.II、MFEM 的 GMG，p-multigrid | HYPRE BoomerAMG、Trilinos ML / MueLu、PETSc GAMG |

弹性问题的 AMG 需要把刚体模态作为近核（near-nullspace）信息提供给粗化，否则粗空间无法表示零能模式，收敛显著退化。

## 4. 作为求解器与作为预条件子

多重网格作为独立求解器时对光滑子、粗化策略、边界处理与系数跳跃都比较敏感，个别分量收敛慢会拖累整体。作为 [[krylov-subspace-methods|Krylov]] 的预条件子（MGCG、GMRES 外套多重网格）时，一次 V-cycle 就是一次 $\mathbf M^{-1}$ 作用，Krylov 外层能吸收多重网格未能消去的少数分量，鲁棒性与效率通常都优于两者单独使用。SPD 问题配 CG 要求 V-cycle 对称，即前后光滑互为转置、$\mathbf R=\mathbf P^{\mathsf T}$。各预条件子的信息需求对照见 [[preconditioning]]。

## 参考文献

[1] BRIGGS W L, HENSON V E, MCCORMICK S F. A Multigrid Tutorial[M]. 2nd ed. Philadelphia: SIAM, 2000. 光滑性质、粗网格校正、V/W/F-cycle 与 AMG 基础。**refs.bib 尚无条目。**
[2] TROTTENBERG U, OOSTERLEE C W, SCHÜLLER A. Multigrid[M]. London: Academic Press, 2001. 多重网格收敛理论与算法设计。**refs.bib 尚无条目。**
[3] SAAD Y. Iterative Methods for Sparse Linear Systems[M]. 2nd ed. Philadelphia: SIAM, 2003. §13 多重网格方法。**refs.bib 尚无条目。**
