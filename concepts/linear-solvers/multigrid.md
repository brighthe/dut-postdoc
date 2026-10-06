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
date_update: 2026-10-06
---

# 多重网格

> 多重网格把定常迭代只能高效消去高频误差这一缺陷变成分工：细网格上做几步光滑压掉高频，把剩余的低频分量限制到粗网格（在那里它们变成相对高频）求解后再延拓回来校正。在线性代数求解器架构（见 [[linear-solvers-architecture]]）中，它是唯一理论上达到渐近最优复杂度 $O(n)$ 的多尺度算法体系；几何多重网格从网格层次出发，代数多重网格只从矩阵元素出发。实践中它最常作为 Krylov 的预条件子出现。

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

多重网格作为独立求解器时对光滑子、粗化策略、边界处理与系数跳跃都比较敏感，个别分量收敛慢会拖累整体。作为 [[krylov-subspace-methods|Krylov]] 的预条件子时，一次 V-cycle 就是一次 $\mathbf M^{-1}$ 作用：SPD 问题配 CG 即 MGCG（multigrid-preconditioned conjugate gradient），一般问题配 GMRES。Krylov 外层能吸收多重网格未能消去的少数分量，鲁棒性与效率通常都优于两者单独使用。各预条件子的信息需求对照见 [[preconditioning]]。

### 4.1 V-cycle 作为 PCG 预条件子的条件

PCG 要求预条件子是固定的 SPD 线性算子（[[preconditioning#1. 形式与目标]]）。把一次 V-cycle 记为映射 $\mathbf r\mapsto\mathbf z=\mathbf B\mathbf r$，记前光滑为 $\mathbf x\leftarrow\mathbf x+\mathbf S(\mathbf b-\mathbf A\mathbf x)$，要满足这一要求需同时做到：

| 要求 | 做法 | 不满足时 |
|---|---|---|
| 线性且固定 | 每次从 $\mathbf z=\mathbf 0$ 出发，做固定次数的循环（通常一次） | 非零初值使映射成为仿射映射；按内层残差判停使循环次数随 $\mathbf r$ 变化，映射非线性，见 4.2 |
| 对称 | $\mathbf R=\mathbf P^{\mathsf T}$；后光滑取前光滑的伴随 $\mathbf S^{\mathsf T}$（阻尼 Jacobi 前后步数相同即可，Gauss-Seidel 后光滑须反向扫描）；粗层算子对称，Galerkin 形式 $\mathbf A_H=\mathbf P^{\mathsf T}\mathbf A\mathbf P$ 自动满足 | 改用 GMRES，或换成对称的光滑与转移 |
| 正定 | 每层光滑子在 $\mathbf A$ 范数下收敛，$\lVert\mathbf I-\mathbf S\mathbf A\rVert_{\mathbf A}<1$，阻尼 Jacobi 即 $0<\omega<2/\lambda_{\max}(\mathbf D^{-1}\mathbf A)$；最粗层精确求解，或用满足 $\sigma(\mathbf B_H\mathbf A_H)\subset(0,1]$ 的固定 SPD 近似（如固定步数的内层对称 V-cycle） | $\mathbf B$ 可能不定，PCG 中 $\mathbf r^{\mathsf T}\mathbf z$ 可能非正而中断 |

正定性的来由（本页推导，结论与 Xu–Zikatanov [6] 的 V-cycle 理论一致）：两层情形 Galerkin 粗层精确求解时，误差传播算子为

$$
\mathbf E=\mathbf I-\mathbf B\mathbf A=(\mathbf I-\mathbf S^{\mathsf T}\mathbf A)\,(\mathbf I-\boldsymbol\Pi)\,(\mathbf I-\mathbf S\mathbf A),\qquad \boldsymbol\Pi=\mathbf P\mathbf A_H^{-1}\mathbf P^{\mathsf T}\mathbf A .
$$

$\boldsymbol\Pi$ 是 $\mathbf A$ 内积下到粗空间的正交投影，$\mathbf I-\mathbf S^{\mathsf T}\mathbf A$ 是 $\mathbf I-\mathbf S\mathbf A$ 的 $\mathbf A$-伴随，所以 $\mathbf E$ 是 $\mathbf A$-自伴半正定算子，且 $\lVert\mathbf E\rVert_{\mathbf A}\le\lVert\mathbf I-\mathbf S\mathbf A\rVert_{\mathbf A}^2<1$。于是 $\sigma(\mathbf B\mathbf A)=1-\sigma(\mathbf E)\subset(0,1]$，$\mathbf B$ 对称正定。粗层换成满足上表条件的近似 $\mathbf B_H$ 后，$\mathbf I-\mathbf P\mathbf B_H\mathbf P^{\mathsf T}\mathbf A$ 的谱仍在 $[0,1]$ 内，结论逐层递归成立。固定做 $k$ 次 V-cycle 对应 $\mathbf E^k$，同样满足。

### 4.2 变预条件与 Flexible CG

若最粗层改用迭代法并按容差停止，或内层 V-cycle 按残差判停，每步作用的 $\mathbf B$ 都不同，甚至不再是线性映射。标准 PCG 的短递推依赖 $\mathbf B$ 固定，此时搜索方向之间的 $\mathbf A$-共轭性会丢失，收敛可能停滞。SPD 情形对应的变体是 Flexible CG（FCG）：把方向更新系数改为 Polak–Ribière 形式 $\beta_j=\mathbf z_{j+1}^{\mathsf T}(\mathbf r_{j+1}-\mathbf r_j)/(\mathbf z_j^{\mathsf T}\mathbf r_j)$（Golub–Ye [8]），或让新方向对最近若干个方向显式做 $\mathbf A$-正交化（Notay [7] 的截断 FCG）；一般情形则用 Flexible GMRES。按 4.1 构造固定 V-cycle，就不需要这些变体。

### 4.3 Krylov 外层为何更稳健

由 4.1，$\sigma(\mathbf B\mathbf A)\subset(0,1]$，作为独立求解器的收敛因子是 $\lVert\mathbf E\rVert_{\mathbf A}=1-\lambda_{\min}(\mathbf B\mathbf A)$，由最难消去的那个误差分量决定。系数高对比度（例如材料与近空区域的刚度相差多个数量级）或几何细节在粗网格上无法表示时，常见的情形是只有少数误差分量被光滑与粗校正同时漏掉。这时 $\mathbf B\mathbf A$ 有少数几个接近 0 的离群特征值，其余特征值聚集在 $[a,1]$ 内。按 [[krylov-subspace-methods#2. 与定常迭代的区别|Krylov 的多项式观点]]，CG 可以让残差多项式在这 $m$ 个离群值处取零，再在 $[a,1]$ 上按 Chebyshev 方式收敛：多花大约 $m$ 步后，收敛速度只由聚集部分的有效条件数 $1/a$ 决定。独立的 V-cycle 迭代则一直受最差分量拖累（本段为本页推导）。

拓扑优化中 MGCG 自 Amir 等（2014）起被广泛采用；Wang2025 观察到，密度场非均质性更强的多孔填充优化需要明显更多的 MGCG 迭代（[[../../literature/topopt/matrix-free/translations/Wang2025-top3d-xl-matrix-free-matlab-zh#7 结果|Wang2025 第 7 节]]）。

### 4.4 乘性与加性多层预条件子

标准 V-cycle 是**乘性**（multiplicative）的：各层依次处理，每层把前光滑后更新过的残差交给下一层，每层每次循环要作用若干次 $\mathbf A_l$。按子空间校正框架（Xu [4]），另一类是**加性**（additive）的：各层同时作用于同一个残差的限制，

$$
\mathbf B_{\mathrm{add}}=\sum_{l=1}^{L-1}\hat{\mathbf P}_l\,\mathbf S_l\,\hat{\mathbf P}_l^{\mathsf T}+\hat{\mathbf P}_L\,\mathbf A_L^{-1}\hat{\mathbf P}_L^{\mathsf T},
$$

其中 $\hat{\mathbf P}_l$ 是从第 $l$ 层到最细层的复合延拓（$\hat{\mathbf P}_1=\mathbf I$），$\mathbf S_l$ 是第 $l$ 层的对称正定光滑或缩放算子。BPX 预条件子（Bramble–Pasciak–Xu [5]）是这一类的代表。

| | 乘性（标准 V-cycle） | 加性 |
|---|---|---|
| 对称正定条件 | 需满足 4.1 的光滑子收敛条件 | 各 $\mathbf S_l$ 对称正定即可 |
| 每次作用的算子乘法 | 各层都要作用 $\mathbf A_l$（残差更新与后光滑） | 循环内不作用 $\mathbf A_l$，只需各层对角（若 $\mathbf S_l$ 为对角缩放）与最粗层分解 |
| 并行性 | 层间串行 | 各层相互独立，可并行 |
| 收敛 | 预条件后谱更集中，迭代次数少 | 谱较分散，迭代次数通常更多；单独作为迭代法须加阻尼，一般只作预条件子 |

两者的取舍取决于"迭代次数增加的倍数"与"单步代价下降的倍数"之比。Wang2025 的"对角松弛"V-cycle 省去了算法 2 中更新残差的那一行，并把后光滑改为 $\mathbf z^{[l]}\leftarrow\mathbf z^{[l]}+w\,\mathbf r^{[l]}./\mathbf D^{[l]}$。展开递推可得 $\mathbf z^{[l]}=2w(\mathbf D^{[l]})^{-1}\mathbf r^{[l]}+\mathbf P^{[l+1]}\mathbf z^{[l+1]}$、$\mathbf r^{[l+1]}=(\mathbf P^{[l+1]})^{\mathsf T}\mathbf r^{[l]}$，即 $\mathbf S_l=2w\,\mathbf D_l^{-1}$ 的加性形式。原文没有这样命名，这一归类是本页推导。原文把对角松弛与跳过第 2 层的非二进粗化合起来称为"改进非二进 V 循环"，并给出判据：迭代次数增长不超过 2 倍即有净收益（[[../../literature/topopt/matrix-free/translations/Wang2025-top3d-xl-matrix-free-matlab-zh#4.2 多重网格预条件子|Wang2025 4.2 节]]）。原文的算例中，它的迭代次数多于标准 V 循环，但总耗时最短、内存最低（[[../../literature/topopt/matrix-free/translations/Wang2025-top3d-xl-matrix-free-matlab-zh#7 结果|Wang2025 第 7 节]]）。

## 参考依据

- [1] BRIGGS W L, HENSON V E, MCCORMICK S F. A Multigrid Tutorial[M]. 2nd ed. Philadelphia: SIAM, 2000 — 光滑性质、粗网格校正、V/W/F-cycle 与 AMG 基础。未入库文献。
- [2] TROTTENBERG U, OOSTERLEE C W, SCHÜLLER A. Multigrid[M]. London: Academic Press, 2001 — 多重网格收敛理论与算法设计。未入库文献。
- [3] SAAD Y. Iterative Methods for Sparse Linear Systems[M]. 2nd ed. Philadelphia: SIAM, 2003 — §13 多重网格方法。未入库文献。
- [4] XU J. Iterative methods by space decomposition and subspace correction[J]. SIAM Review, 1992, 34(4): 581-613. DOI: 10.1137/1034116 — 乘性与加性子空间校正框架（4.4）。未入库文献，出版信息经 CrossRef 核对。
- [5] BRAMBLE J H, PASCIAK J E, XU J. Parallel multilevel preconditioners[J]. Mathematics of Computation, 1990, 55(191): 1-22. DOI: 10.1090/S0025-5718-1990-1023042-6 — BPX 加性多层预条件子（4.4）。未入库文献，出版信息经 CrossRef 核对。
- [6] XU J, ZIKATANOV L. Algebraic multigrid methods[J]. Acta Numerica, 2017, 26: 591-721. DOI: 10.1017/S0962492917000083 — 对称 V-cycle 的误差传播算子与作为 SPD 预条件子的条件（4.1）。未入库文献，出版信息经 CrossRef 核对；4.1 的推导为本页按其框架写出，未逐式对照原文。
- [7] NOTAY Y. Flexible conjugate gradients[J]. SIAM Journal on Scientific Computing, 2000, 22(4): 1444-1460. DOI: 10.1137/S1064827599362314 — 变预条件下的截断 FCG（4.2）。未入库文献，出版信息经 CrossRef 核对。
- [8] GOLUB G H, YE Q. Inexact preconditioned conjugate gradient method with inner-outer iteration[J]. SIAM Journal on Scientific Computing, 1999, 21(4): 1305-1320. DOI: 10.1137/S1064827597323415 — 非精确内层预条件下的 PCG 变体（4.2）。未入库文献，出版信息经 CrossRef 核对；Polak–Ribière 形式 $\beta_j$ 的归属待对照原文确认。
- [9] [[../../literature/topopt/matrix-free/translations/Wang2025-top3d-xl-matrix-free-matlab-zh|Wang2025 译文]]（citekey `Wang2025-top3d-xl-matrix-free-matlab`）— 拓扑优化中的 MGCG（算法 1、2）、对角松弛与非二进 V 循环、非均质性对迭代次数的影响（4.3、4.4）；其中 MGCG 自 Amir 等（2014）起被广泛采用的说法经该文转引，Amir 等（2014）未入库。
