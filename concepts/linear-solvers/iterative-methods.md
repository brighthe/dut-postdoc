---
title: "迭代法"
type: concept
aliases:
  - Iterative Methods
  - 迭代求解器
  - Stationary Iterative Methods
  - 定常迭代法
  - 经典迭代法
  - Jacobi 迭代
  - Gauss-Seidel 迭代
  - SOR
  - Richardson 迭代
  - 矩阵分裂
  - Chebyshev 迭代
  - Krylov Subspace Methods
  - Krylov 子空间方法
  - Krylov 迭代法
  - 预条件 Krylov 求解器
  - Conjugate Gradient
  - 共轭梯度法
  - PCG
  - GMRES
  - MINRES
  - Flexible CG
  - Preconditioning
  - Preconditioner
  - 预条件
  - 预条件子
  - 预条件器
  - Jacobi 预条件
  - ILU
  - Multigrid
  - 多重网格
  - Geometric Multigrid
  - Algebraic Multigrid
  - GMG
  - AMG
  - 几何多重网格
  - 代数多重网格
  - MGCG
  - Domain Decomposition
  - 区域分解
tags:
  - numerical-algebra
  - linear-solver
  - iterative-method
  - stationary-iteration
  - smoother
  - krylov
  - preconditioning
  - multigrid
  - parallel-reduction
status: draft
date_added: 2026-10-06
date_update: 2026-10-07
---

# 迭代法

> 迭代法不分解 $\mathbf A$，而是反复调用算子作用 $\mathbf y=\mathbf A\mathbf x$（加上预条件子所需的少量矩阵信息）逐步改进近似解。它的内存只随向量与算子表示增长，是三维大规模问题与不显式组装全局矩阵的算子表示的必经之路；代价是收敛快慢取决于谱分布，需要预条件来保证。本页先按两条轴给迭代法分类：外层迭代格式（定常、Chebyshev、Krylov）决定怎样使用近似逆 $\mathbf B\approx\mathbf A^{-1}$，预条件子的构造（松弛、不完全分解、多项式、多重网格、区域分解）决定 $\mathbf B$ 是什么；具体求解器是二者的组合。

## 1. 迭代法的分类

### 1.1 残差修正形式

几乎所有迭代法都可以从残差修正形式出发：

$$
\mathbf x_{k+1}=\mathbf x_k+\mathbf B(\mathbf b-\mathbf A\mathbf x_k),
$$

其中 $\mathbf B\approx\mathbf A^{-1}$ 是易于作用的近似逆。$\mathbf B$ 每步固定时，误差满足 $\mathbf e_k=(\mathbf I-\mathbf B\mathbf A)^k\mathbf e_0$。Chebyshev 迭代与 Krylov 方法同样只用 $\mathbf B$ 与 $\mathbf A$ 的作用生成迭代值，迭代值都落在仿射空间 $\mathbf x_0+\mathcal K_k(\mathbf B\mathbf A,\mathbf B\mathbf r_0)$ 中，误差可统一写成

$$
\mathbf e_k=p_k(\mathbf B\mathbf A)\,\mathbf e_0,\qquad p_k(0)=1,\ \deg p_k=k .
$$

一个迭代法因此由两件事确定：用什么 $\mathbf B$，以及怎样选多项式 $p_k$。

### 1.2 两条分类轴

**轴一：外层迭代格式**，即怎样选 $p_k$（§2）

| 外层格式 | 误差多项式 $p_k(t)$ | 收敛由什么决定 | 是否需要内积 |
|---|---|---|---|
| 定常迭代（§2.1） | 固定为 $(1-t)^k$ | 谱半径 $\rho(\mathbf I-\mathbf B\mathbf A)$ | 不需要 |
| Chebyshev 迭代（§2.2） | 按预先给定的谱区间取 Chebyshev 多项式，逐步变化但不依赖迭代过程 | 谱区间估计及区间内的条件数 | 不需要 |
| Krylov 方法（§2.3） | 每步在所有候选多项式中按投影或极小化准则取最优 | $\mathbf B\mathbf A$ 的整体谱分布 | 需要，每步若干次 |

**轴二：预条件子的构造**，即 $\mathbf B$ 是什么（§3）

| 构造类别 | 代表 | 需要的信息 |
|---|---|---|
| 松弛类（§3.2） | Jacobi、Gauss-Seidel、逐次超松弛（Successive Over-Relaxation, SOR）、对称逐次超松弛（Symmetric SOR, SSOR）、块 Jacobi | 对角、对角块或矩阵行 |
| 不完全分解、多项式与代理算子（§3.3） | 不完全 LU 分解（Incomplete LU, ILU）/ 不完全 Cholesky 分解（Incomplete Cholesky, IC）、Chebyshev 多项式预条件、低阶代理矩阵 | 稀疏矩阵元素、谱区间或一个更易组装的近似算子 |
| 多重网格（§3.4） | 几何多重网格（Geometric Multigrid, GMG）、代数多重网格（Algebraic Multigrid, AMG） | 网格层次或矩阵元素 |
| 区域分解（§3.5） | 加性 / 乘性 Schwarz | 子域局部矩阵，可选粗空间 |

不预条件时 $\mathbf B=\mathbf I$（或一个标量缩放），只剩轴一。

### 1.3 具体求解器是两条轴的组合

下表中的组合按"预条件子-外层方法"命名。外层的 Krylov 方法以共轭梯度法（Conjugate Gradient, CG）与广义极小残差法（Generalized Minimal Residual, GMRES）为代表，带预条件的 CG 称为预条件共轭梯度法（Preconditioned Conjugate Gradient, PCG）；Jacobi-PCG 即以 Jacobi 为预条件子的 PCG，多重网格预条件共轭梯度法（Multigrid-Preconditioned Conjugate Gradient, MGCG）即以一次 V-cycle 为预条件子的 PCG。

| | 定常迭代 | Krylov 方法 |
|---|---|---|
| 松弛类 | Jacobi 迭代、Gauss-Seidel 迭代、SOR | Jacobi-PCG、SSOR-PCG |
| 不完全分解 | 很少单独使用 | IC-PCG、ILU-GMRES |
| 多重网格 | 多重网格求解器 | MGCG、AMG-PCG |
| 区域分解 | Schwarz 迭代 | Schwarz-PCG |

## 2. 外层迭代格式

### 2.1 定常迭代

$\mathbf B$ 每步固定，记迭代矩阵 $\mathbf G=\mathbf I-\mathbf B\mathbf A$，则 $\mathbf x_{k+1}=\mathbf G\mathbf x_k+\mathbf B\mathbf b$，误差 $\mathbf e_k=\mathbf G^k\mathbf e_0$。对任意初值收敛当且仅当谱半径 $\rho(\mathbf G)<1$，渐近收敛率为 $\rho(\mathbf G)$。整个过程中 $\mathbf G$ 不变，没有自适应余地，这是它与 Krylov 方法的本质区别。

经典的写法是矩阵分裂：取 $\mathbf A=\mathbf M-\mathbf N$，其中 $\mathbf M$ 易于求逆，$\mathbf A\mathbf x=\mathbf b$ 等价于不动点方程 $\mathbf x=\mathbf M^{-1}\mathbf N\mathbf x+\mathbf M^{-1}\mathbf b$，即 $\mathbf B=\mathbf M^{-1}$、$\mathbf G=\mathbf M^{-1}\mathbf N$。

收敛快慢完全由 $\mathbf B$ 决定：松弛类 $\mathbf B$ 对椭圆问题随网格加密而退化（§3.2），多重网格类 $\mathbf B$ 可使 $\lVert\mathbf G\rVert_{\mathbf A}$ 与网格尺寸 $h$ 无关（§3.4）。

### 2.2 Chebyshev 迭代

设 $\mathbf B\mathbf A$ 的特征值落在已知区间 $[\alpha,\beta]\subset(0,\infty)$ 内（例如 $\mathbf A$、$\mathbf B$ 都为对称正定（Symmetric Positive Definite, SPD）矩阵）。Chebyshev 迭代取

$$
p_k(t)=\frac{T_k\!\left(\dfrac{\beta+\alpha-2t}{\beta-\alpha}\right)}{T_k\!\left(\dfrac{\beta+\alpha}{\beta-\alpha}\right)},
$$

$T_k$ 为 $k$ 次 Chebyshev 多项式。它是在整个区间 $[\alpha,\beta]$ 上最大值最小的满足 $p_k(0)=1$ 的多项式，误差缩减因子约为 $(\sqrt\kappa-1)/(\sqrt\kappa+1)$，$\kappa=\beta/\alpha$，与 CG 收敛界的量级相同。与 CG 的区别是：$p_k$ 由区间端点预先确定，迭代中不需要内积，因而没有全局归约（§2.3.5）；代价是需要谱区间估计，估计偏差会降低收敛速度，且无法像 CG 那样利用谱在区间内部的聚集。

它在实践中主要有两种用途：作多重网格的光滑子，只针对 $[\beta/c,\beta]$ 的高频部分取多项式（$c$ 为预设的比值）；作多项式预条件子（§3.3）。

### 2.3 Krylov 子空间方法

Krylov 子空间方法是一类方法的统称。除 CG、PCG 与 GMRES 外，主要成员还有极小残差法（Minimal Residual, MINRES）、SYMMLQ（Symmetric LQ）、完全正交化方法（Full Orthogonalization Method, FOM）、稳定双共轭梯度法（Biconjugate Gradient Stabilized, BiCGSTAB）与 TFQMR（Transpose-Free Quasi-Minimal Residual），以及变预条件版本灵活共轭梯度法（Flexible Conjugate Gradient, FCG）与灵活 GMRES（Flexible GMRES, FGMRES）：

| 方法             | 适用矩阵 | 递推与存储                                 | 固定预条件子                        | 变预条件子        |
| -------------- | ---- | ------------------------------------- | ----------------------------- | ------------ |
| CG             | SPD  | Lanczos 短递推，只保留前一步向量，存储与每步计算量最小       | PCG（§2.3.2）                     | FCG（§2.4）    |
| MINRES、SYMMLQ  | 对称不定 | Lanczos 短递推，MINRES 保证残差单调             | 预条件 MINRES（要求 SPD 预条件子，§2.3.3） | —            |
| FOM、GMRES      | 一般   | Arnoldi 长递推，须保存全部基向量，实践中定期重启 GMRES(m) | 左 / 右预条件 GMRES                | FGMRES（§2.4） |
| BiCGSTAB、TFQMR | 非对称  | 双正交 Lanczos 短递推，残差不再单调                | 预条件 BiCGSTAB                  | —            |

表中只列外层方法本身。每个 Krylov 方法都可以加预条件，只有 CG 的预条件版本有专门的名称 PCG。PCG 配上不同的预条件子，就得到 Jacobi-PCG、MGCG 等组合（§1.3）；预条件子怎么构造属于 §3。§2.3.1 讲这些方法的共同原理，§2.3.2–§2.3.4 逐个介绍常用方法，§2.3.5 讨论并行执行。

**选择判据。** 对称性决定能否在保持最优性的同时使用短递推（BiCGSTAB 等非对称方法以放弃每步最优为代价换回短递推），正定性决定能否使用 CG，这两条是选择方法的第一判据：SPD 用 CG / PCG，对称不定用 MINRES，非对称用 GMRES 或 BiCGSTAB。预条件后的对称性同样要看：SPD 问题用非对称预条件子（如单向 Gauss-Seidel）后不能再用 CG，须改用 GMRES 或换对称预条件子；预条件子随迭代变化时须用 §2.4 的变体。直接法与迭代法之间的选型见 [[linear-solvers-architecture#2. 三条判定线]]。

#### 2.3.1 共同原理

设初始解为 $\mathbf x_0$，初始残差为 $\mathbf r_0=\mathbf b-\mathbf A\mathbf x_0$。第 $k$ 阶 Krylov 子空间是

$$
\mathcal K_k(\mathbf A,\mathbf r_0)=\operatorname{span}\left\{\mathbf r_0,\ \mathbf A\mathbf r_0,\ \mathbf A^2\mathbf r_0,\ \dots,\ \mathbf A^{k-1}\mathbf r_0\right\}.
$$

Krylov 方法在仿射空间 $\mathbf x_0+\mathcal K_k$ 中取近似解 $\mathbf x_k$，把 $n$ 维问题化为 $k$ 维子空间上的小规模代数问题，通常 $k\ll n$。残差可写成 $\mathbf r_k=p_k(\mathbf A)\mathbf r_0$，$p_k(0)=1$；方法每一步按某种准则自动选出最好的 $p_k$，等价于按 $\mathbf A$ 的谱自适应地调整每步的有效算子，定常迭代则固定使用 $(1-t)^k$（§1.1）。一个具体方法由两个选择决定：

- **怎样生成子空间的基**：对称矩阵用 Lanczos 过程，三项短递推；一般矩阵用 Arnoldi 过程，需要对全部已有基向量正交化。
- **按什么准则取解**：Galerkin 投影要求残差与 $\mathcal K_k$ 正交；极小残差要求 $\lVert\mathbf b-\mathbf A\mathbf x_k\rVert_2$ 在子空间内最小。

两两组合得到下表四种方法：

| | Galerkin 投影（$\mathbf r_k\perp\mathcal K_k$） | 极小残差（$\min\lVert\mathbf r_k\rVert_2$） |
|---|---|---|
| Lanczos（对称，短递推） | CG（要求 SPD） | MINRES |
| Arnoldi（一般，长递推） | FOM | GMRES |

CG 可以看作 FOM 在 SPD 情形下的特例：矩阵对称时 Arnoldi 过程退化为 Lanczos 过程，长递推变为短递推。FOM 与 SYMMLQ 实践中很少直接使用，本页不单独介绍。非对称矩阵的 BiCGSTAB 等方法基于双正交 Lanczos 过程，用两组相互双正交的基换回短递推，不在上表之内（§2.3.4）。

预条件时以 $\mathbf B\mathbf A$、$\mathbf B\mathbf r_0$ 代替 $\mathbf A$、$\mathbf r_0$（§3.1）。

Krylov 方法运行过程中只调用 $\mathbf y=\mathbf A\mathbf x$，不读取 $\mathbf A$ 的元素。这使它成为各种不显式组装全局矩阵的算子表示的自然外层：算子可以是单元级按需作用、子结构缩聚算子或任何线性映射。这一性质对求解器成立，对预条件子不成立（§3.6），各装配层级还能提供哪些代数信息由 [[../matrix-free/assembly-levels#3. 三条跨层级性质]] 不变量 3 维护。

#### 2.3.2 CG 与 PCG

**它做什么。** 对 SPD 矩阵，CG 的 Galerkin 条件等价于在子空间中使能量范数误差最小：

$$
\mathbf x_k=\arg\min_{\mathbf x\in\mathbf x_0+\mathcal K_k}\lVert\mathbf x-\mathbf x^\ast\rVert_{\mathbf A}.
$$

每一步的代价固定：1 次算子作用 $\mathbf A\mathbf p$、2 次内积、几次向量更新，只需保存 3–4 个向量。这是所有 Krylov 方法中最省的。

**收敛快慢取决于什么。** CG 的能量范数误差满足

$$
\lVert\mathbf e_k\rVert_{\mathbf A}\le 2\left(\frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}\right)^{k}\lVert\mathbf e_0\rVert_{\mathbf A},\qquad \kappa=\kappa_2(\mathbf A),
$$

迭代次数随 $\sqrt\kappa$ 而非 $\kappa$ 增长。这一界只用到谱区间，与 Chebyshev 迭代（§2.2）相同；特征值聚集在少数几簇时，CG 的实际收敛远快于该上界，这也是预条件的目标（§3.1）。若只有 $m$ 个离群特征值、其余聚集在 $[a,b]$ 内，可令 $p_k$ 在离群值处取零、在 $[a,b]$ 上按 Chebyshev 方式收敛：多花大约 $m$ 步后，收敛速度由有效条件数 $b/a$ 决定（本页推导，§3.4.6 用到）。二阶椭圆问题（如线弹性）的有限元刚度矩阵有 $\kappa=O(h^{-2})$，不加有效的预条件子时，迭代次数按 $O(h^{-1})$ 随网格加密增长。

**PCG。** 加一个固定的 SPD 预条件子 $\mathbf M$，等价于在 $\mathbf M$ 内积下对预条件后的系统做 CG，每步多一次 $\mathbf z=\mathbf M^{-1}\mathbf r$ 的作用，收敛由 $\mathbf M^{-1}\mathbf A$ 的谱决定。$\mathbf M$ 必须对称正定且每步不变（§3.1）；每步变化时改用 FCG（§2.4）。Jacobi-PCG、MGCG 等都是 PCG 配不同预条件子的结果（§1.3）。

**使用要点。**

- **适用条件**：$\mathbf A$ 须为 SPD。约束不足、结构仍有刚体位移时，刚度矩阵只是半正定，CG 可能不收敛；应先补足约束。
- **边界条件**：Dirichlet 条件须用保持对称的方式施加（受约束的行与列同时消去，或置零后对角置 1），只消去行会破坏对称性。
- **停机判据**：常用相对残差 $\lVert\mathbf r_k\rVert_2\le\mathrm{tol}\cdot\lVert\mathbf b\rVert_2$。若改以初始残差 $\lVert\mathbf r_0\rVert_2$ 为参照，用上一步解作初值（热启动）时 $\lVert\mathbf r_0\rVert_2$ 已经很小，同一个 tol 会变得过严，求解代价反而增加。
- **残差曲线**：CG 最小化的是能量范数误差而不是残差，$\lVert\mathbf r_k\rVert_2$ 不一定单调下降，出现波动属正常现象。
- **有限精度**：精确算术下 CG 至多 $n$ 步终止，实践中正交性会逐渐丢失，这一终止性质不可依赖。

#### 2.3.3 MINRES

**它做什么。** 用 Lanczos 短递推，在子空间中使残差 $\lVert\mathbf r_k\rVert_2$ 最小（Paige–Saunders [16]）。它只要求 $\mathbf A$ 对称、不要求正定，残差单调下降；每步代价与 CG 同量级，比 CG 多保存几个向量。同一文献中的 SYMMLQ 也适用于对称不定矩阵，实践中较少使用。

**典型问题。** 鞍点系统，例如 Hu–Zhang 等混合有限元、近不可压缩弹性、Stokes 流动。这类系统同时有正负特征值，CG 可能中断。

**使用要点。**

- 预条件子必须是 **SPD** 的，才能保持短递推；对鞍点系统常用块对角预条件，各块分别近似原块与 Schur 补（Elman–Silvester–Wathen [17]，原书章节未核对）。
- 收敛由预条件后矩阵的正、负两侧特征值区间共同决定，两侧都要被预条件子压缩。

#### 2.3.4 非对称矩阵：GMRES 与 BiCGSTAB

**典型问题。** 非对称矩阵，例如接触摩擦、跟随载荷、非关联塑性的切线刚度，以及对流占优问题。两种方法的取舍在于递推长短：

| | GMRES | BiCGSTAB（及 TFQMR） |
|---|---|---|
| 基的生成 | Arnoldi，长递推：第 $k$ 步要与前面全部 $k$ 个基向量正交化 | 双正交 Lanczos，短递推 |
| 取解准则 | 子空间内残差 $\lVert\mathbf r_k\rVert_2$ 最小 | 不再每步最优 |
| 残差行为 | 单调下降 | 不单调，可能剧烈振荡，个别情况下算法中断（breakdown） |
| 存储与每步计算量 | 随 $k$ 增长，实践中须重启 | 固定，不随迭代步增长 |

**使用要点。**

- **默认先用 GMRES**，它收敛稳健、残差单调。存储过大又不愿频繁重启时，再换 BiCGSTAB；BiCGSTAB 收敛不稳定时，先换回 GMRES 确认问题本身是否可解，再回头调整预条件子。
- **重启 GMRES(m)**：每做 $m$ 步就以当前解为初值重新开始，用来限制存储。$m$ 越小越省内存，但可能停滞甚至不收敛；$m$ 的取值须按问题试验。
- **左、右预条件**：左预条件极小化的是预条件后的残差 $\lVert\mathbf M^{-1}\mathbf r\rVert_2$，右预条件极小化真残差 $\lVert\mathbf r\rVert_2$；用残差判停时须分清是哪一种（§3.1）。
- 预条件子不要求对称；预条件子每步变化时，GMRES 改用 FGMRES（§2.4）。

#### 2.3.5 并行执行中的同步点

Krylov 迭代的每一步由三类运算组成：算子作用 $\mathbf A\mathbf p$、向量更新 $\mathbf y\leftarrow a\mathbf x+\mathbf y$（AXPY）、内积。前两类在分区之间没有依赖（算子作用只在界面上需要交换数据，且可以与内部单元的计算重叠），唯一必须让全部执行实体同步的是内积。

- **每步归约次数**：CG 每次迭代需要 2 次内积（$\mathbf r^{\mathsf T}\mathbf r$ 与 $\mathbf p^{\mathsf T}\mathbf A\mathbf p$），PCG 同样是 2 次（$\mathbf r^{\mathsf T}\mathbf z$ 与 $\mathbf p^{\mathsf T}\mathbf A\mathbf p$）；GMRES 的 Arnoldi 正交化每步归约次数随重启维数 $m$ 增长，代价更高。
- **在各并行层的形态**：进程级是一次 `MPI_Allreduce` 全局同步，设备内是 block reduction 加一次设备级归约，线程级是共享内存归约。进程级是唯一会阻塞全部 rank 的那一种，它必须等所有 rank 到齐才能给出标量，因此强扩展曲线的拐点通常出现在内积而不是算子作用上。三层并行的完整卡点讨论见 [[../gpu-hpc/parallel-levels#3. 两个绕不开的断点]]。
- **共享自由度必须加权**：分区之间有共享自由度时，直接对各 rank 的局部内积求和会重复计数界面分量，必须使用按引用计数加权的内积，它精确等于串行内积，从而保证并行与串行的迭代序列逐点一致；定理与实现约定见 [[../gpu-hpc/distributed-operator-and-shared-dofs#4. 重叠加权内积与 Krylov 求解器收敛理论]]。
- **降低归约代价属于换算法**：s-step / communication-avoiding CG 与 pipelined CG 通过重组递推把多次归约合并或与算子作用重叠，但它们改变了浮点运算次序与数值稳定性，收敛行为需单独验证，不能视为同一算法的不同实现。

### 2.4 变预条件：FCG 与 FGMRES

若 $\mathbf B$ 的作用每步不同，例如内层再套一个按容差停止的迭代求解器，它就不再是固定的线性算子。标准 PCG 的短递推依赖 $\mathbf B$ 固定，此时搜索方向之间的 $\mathbf A$-共轭性会丢失，收敛可能停滞。须改用允许变预条件的变体：

- **SPD 情形，FCG**：把方向更新系数改为 Polak–Ribière 形式 $\beta_j=\mathbf z_{j+1}^{\mathsf T}(\mathbf r_{j+1}-\mathbf r_j)/(\mathbf z_j^{\mathsf T}\mathbf r_j)$（Golub–Ye [14]），或让新方向对最近若干个方向显式做 $\mathbf A$-正交化（Notay [13] 的截断 FCG）。
- **一般情形，FGMRES**：额外保存每步预条件后的向量，以长递推换取对变预条件的容忍。

多重网格作 $\mathbf B$ 时怎样保证固定、对称、正定，见 §3.4.5；保证了这些就不需要上述变体。

## 3. 预条件子的构造

### 3.1 预条件的形式与目标

条件数 $\kappa(\mathbf A)$ 过大时 Krylov 收敛缓慢。预条件寻找易于求逆的 $\mathbf M\approx\mathbf A$（即 $\mathbf B=\mathbf M^{-1}$），改为求解等价方程组

$$
\underbrace{\mathbf M^{-1}\mathbf A\mathbf x=\mathbf M^{-1}\mathbf b}_{\text{左预条件}},\qquad
\underbrace{\mathbf A\mathbf M^{-1}\mathbf y=\mathbf b,\ \ \mathbf x=\mathbf M^{-1}\mathbf y}_{\text{右预条件}},\qquad
\underbrace{\mathbf M_1^{-1}\mathbf A\mathbf M_2^{-1}\mathbf y=\mathbf M_1^{-1}\mathbf b}_{\text{分裂预条件}} .
$$

目标不是把 $\kappa$ 压到 1，而是让 $\mathbf M^{-1}\mathbf A$ 的特征值聚集在少数几簇附近，因为 Krylov 的收敛由谱分布而非单一条件数决定（§2.3.2）。左预条件改变了残差范数（GMRES 极小化的是 $\lVert\mathbf M^{-1}\mathbf r\rVert$），右预条件保持真残差，工程上判停机时须分清。

SPD 情形下 PCG 只需 $\mathbf M$ 为 SPD，实现上不必显式对称化：算法在 $\mathbf M$ 内积下运行，每步多一次 $\mathbf z=\mathbf M^{-1}\mathbf r$ 的作用。若 $\mathbf M$ 不对称（如单向 Gauss-Seidel），CG 的理论不再成立，须改用 GMRES 或换对称预条件子。

### 3.2 松弛类：Jacobi、Gauss-Seidel、SOR、SSOR

取 $\mathbf A=\mathbf D-\mathbf L-\mathbf U$（对角、严格下三角、严格上三角），松弛类预条件子由分裂 $\mathbf A=\mathbf M-\mathbf N$ 的 $\mathbf M$ 给出：

| 方法 | $\mathbf M$ | 特点 |
|---|---|---|
| Richardson | $\omega^{-1}\mathbf I$ | 最简单的一阶格式，$\omega$ 需按谱区间选取；SPD 时最优 $\omega=2/(\lambda_{\min}+\lambda_{\max})$ |
| Jacobi | $\mathbf D$ | 各分量可同时更新，天然并行；阻尼 Jacobi 取 $\mathbf M=\omega^{-1}\mathbf D$ |
| Gauss-Seidel | $\mathbf D-\mathbf L$ | 用已更新分量，串行依赖；对一致排序矩阵收敛率约为 Jacobi 的平方 |
| SOR | $\omega^{-1}\mathbf D-\mathbf L$ | Gauss-Seidel 的超松弛，$\omega$ 取最优时收敛阶显著改善，但最优 $\omega$ 依赖谱信息 |
| 对称 Gauss-Seidel / SSOR | 前向一遍加后向一遍 | 得到对称的 $\mathbf M$，可作 SPD 问题的预条件子 |
| 块 Jacobi | $\mathbf A$ 的对角块 | 块内精确或近似求逆，块间并行 |

作定常迭代时，Jacobi 与 Gauss-Seidel 对严格对角占优或 SPD 矩阵收敛；SOR 对 SPD 矩阵在 $0<\omega<2$ 时收敛。Gauss-Seidel 的串行依赖在并行中通过红黑排序或多色排序解除，代价是收敛率略降。

**网格依赖**：对二阶椭圆问题的有限元离散，网格尺寸 $h$ 减小时 $\rho(\mathbf G)$ 趋近于 1：Jacobi 与 Gauss-Seidel 为 $1-O(h^2)$，最优 SOR 为 $1-O(h)$，相应迭代次数为 $O(h^{-2})$ 与 $O(h^{-1})$，在 $d$ 维中即 $O(n^{2/d})$ 与 $O(n^{1/d})$。迭代次数随自由度数增长，因此它们不再作为独立求解器，只在小规模或强对角占优问题中单独使用。

**光滑性质**：对 $\mathbf G$ 的特征分解，对应高频（振荡）特征向量的特征值远小于 1，少数几步迭代就能把误差中的高频分量压掉，剩下的是在当前网格上光滑的低频分量。今天松弛类主要以两种身份出现：作 Krylov 的廉价预条件子（Jacobi 即对角缩放，另有 SSOR、块 Jacobi）；作多重网格的光滑子（阻尼 Jacobi、Gauss-Seidel，并行环境下常用 Chebyshev 或多色 Gauss-Seidel，见 §3.4）。

### 3.3 不完全分解、多项式与代理算子

- **不完全分解 ILU(k) / IC(k) / 带阈值的 ILU（ILU with Threshold, ILUT）**：在稀疏 LU / Cholesky 分解中按填充层级或数值阈值丢弃部分填充，得到稀疏的近似因子。需要显式稀疏矩阵及其稀疏结构；前代回代串行本质强，并行时须按分区做块 ILU。
- **多项式预条件**：取 $\mathbf B=q(\mathbf A)$ 为 $\mathbf A$ 的低次多项式，常用 Chebyshev 多项式近似 $\mathbf A^{-1}$（§2.2）。只需算子作用与谱区间估计，适合不显式组装矩阵的算子表示与 GPU。
- **低阶 / 代理算子**：用一个更易组装、更易求逆的近似算子作预条件，例如高阶有限元算子用同一网格节点上的低阶组装矩阵作预条件，或用降阶模型近似。

### 3.4 多重网格

多重网格把松弛类只能高效消去高频误差这一缺陷变成分工：细网格上做几步光滑压掉高频，把剩余的低频分量限制到粗网格（在那里它们变成相对高频）求解后再延拓回来校正。对椭圆问题，它是能达到渐近最优复杂度 $O(n)$ 的代表性方法；GMG 从网格层次出发，AMG 只从矩阵元素出发。一次 V-cycle 就是一个 $\mathbf B$：配定常迭代即多重网格求解器，配 Krylov 即 MGCG 等，后者在实践中更常见。

#### 3.4.1 光滑与粗网格校正

松弛类对二阶椭圆问题的 $\rho(\mathbf G)$ 随网格加密趋近于 1，但对应高频特征向量的特征值远小于 1（§3.2）：少数几步就能把误差中的振荡分量压掉，剩下的是在当前网格上光滑的低频分量。光滑的误差可以在更粗的网格上精确表示，而在粗网格上它们的相对频率翻倍，又变成光滑子能高效处理的对象。两个网格层间的转移由限制算子 $\mathbf R$（细到粗）与延拓算子 $\mathbf P$（粗到细）完成，常取 $\mathbf R=\mathbf P^{\mathsf T}$。

#### 3.4.2 V-cycle 骨架

一次两层校正扩展为多层递归即 V-cycle：

1. 细网格前光滑：做 $\nu_1$ 步松弛（阻尼 Jacobi、Gauss-Seidel、Chebyshev 等）；
2. 计算残差并限制到粗网格：$\mathbf r_H=\mathbf R\,(\mathbf b-\mathbf A\mathbf x)$；
3. 粗网格求解 $\mathbf A_H\mathbf e_H=\mathbf r_H$，递归调用本过程，或在最粗层用[[direct-methods|直接法]]求解；
4. 延拓并校正：$\mathbf x\leftarrow\mathbf x+\mathbf P\mathbf e_H$；
5. 细网格后光滑 $\nu_2$ 步。

W-cycle 在每层递归两次，F-cycle 介于二者之间；全多重网格（Full Multigrid, FMG）从最粗层起逐层给出初值，一次扫过即可达到离散精度。对椭圆问题，V-cycle 每次的误差压缩因子与 $h$ 无关，总运算量为 $O(n)$。

#### 3.4.3 GMG 与 AMG

| | GMG | AMG |
|---|---|---|
| 层次来源 | 网格加密序列 | 仅由矩阵元素按连接强度（strength-of-connection）粗化 |
| 粗算子 | Galerkin 方式 $\mathbf A_H=\mathbf R\mathbf A\mathbf P$，或在粗网格上重新离散 | Galerkin 方式 |
| 需要的信息 | 网格层次与层间转移算子，不需要矩阵元素 | 显式稀疏矩阵元素 |
| 适用性 | 结构化或可嵌套加密的网格；高阶元用 p-multigrid 在多项式次数上逐级降阶 | 非结构网格、无几何层次的一般 SPD 问题 |
| 典型实现 | deal.II、MFEM 的 GMG，p-multigrid | HYPRE BoomerAMG、Trilinos ML / MueLu、PETSc GAMG |

弹性问题的 AMG 需要把刚体模态作为近核（near-nullspace）信息提供给粗化，否则粗空间无法表示零能模式，收敛显著退化。

#### 3.4.4 作为求解器与作为预条件子

多重网格作为独立求解器时对光滑子、粗化策略、边界处理与系数跳跃都比较敏感，个别分量收敛慢会拖累整体。作为 Krylov 的预条件子时，一次 V-cycle 就是一次 $\mathbf B$ 作用：SPD 问题配 CG 即 MGCG，一般问题配 GMRES。Krylov 外层能吸收多重网格未能消去的少数分量，鲁棒性与效率通常都优于两者单独使用（§3.4.6）。

#### 3.4.5 V-cycle 作为 PCG 预条件子的条件

PCG 要求预条件子是固定的 SPD 线性算子（§3.1）。把一次 V-cycle 记为映射 $\mathbf r\mapsto\mathbf z=\mathbf B\mathbf r$，记前光滑为 $\mathbf x\leftarrow\mathbf x+\mathbf S(\mathbf b-\mathbf A\mathbf x)$，要满足这一要求需同时做到：

| 要求 | 做法 | 不满足时 |
|---|---|---|
| 线性且固定 | 每次从 $\mathbf z=\mathbf 0$ 出发，做固定次数的循环（通常一次） | 非零初值使映射成为仿射映射；最粗层迭代求解按容差停止、或内层按残差判停，都使映射随 $\mathbf r$ 变化，须用 §2.4 的 FCG |
| 对称 | $\mathbf R=\mathbf P^{\mathsf T}$；后光滑取前光滑的伴随 $\mathbf S^{\mathsf T}$（阻尼 Jacobi 前后步数相同即可，Gauss-Seidel 后光滑须反向扫描）；粗层算子对称，Galerkin 形式 $\mathbf A_H=\mathbf P^{\mathsf T}\mathbf A\mathbf P$ 自动满足 | 改用 GMRES，或换成对称的光滑与转移 |
| 正定 | 每层光滑子在 $\mathbf A$ 范数下收敛，$\lVert\mathbf I-\mathbf S\mathbf A\rVert_{\mathbf A}<1$，阻尼 Jacobi 即 $0<\omega<2/\lambda_{\max}(\mathbf D^{-1}\mathbf A)$；最粗层精确求解，或用满足 $\sigma(\mathbf B_H\mathbf A_H)\subset(0,1]$ 的固定 SPD 近似（如固定步数的内层对称 V-cycle） | $\mathbf B$ 可能不定，PCG 中 $\mathbf r^{\mathsf T}\mathbf z$ 可能非正而中断 |

正定性的来由（本页推导，结论与 Xu–Zikatanov [12] 的 V-cycle 理论一致）：两层情形 Galerkin 粗层精确求解时，误差传播算子为

$$
\mathbf E=\mathbf I-\mathbf B\mathbf A=(\mathbf I-\mathbf S^{\mathsf T}\mathbf A)\,(\mathbf I-\boldsymbol\Pi)\,(\mathbf I-\mathbf S\mathbf A),\qquad \boldsymbol\Pi=\mathbf P\mathbf A_H^{-1}\mathbf P^{\mathsf T}\mathbf A .
$$

$\boldsymbol\Pi$ 是 $\mathbf A$ 内积下到粗空间的正交投影，$\mathbf I-\mathbf S^{\mathsf T}\mathbf A$ 是 $\mathbf I-\mathbf S\mathbf A$ 的 $\mathbf A$-伴随，所以 $\mathbf E$ 是 $\mathbf A$-自伴半正定算子，且 $\lVert\mathbf E\rVert_{\mathbf A}\le\lVert\mathbf I-\mathbf S\mathbf A\rVert_{\mathbf A}^2<1$。于是 $\sigma(\mathbf B\mathbf A)=1-\sigma(\mathbf E)\subset(0,1]$，$\mathbf B$ 为 SPD。粗层换成满足上表条件的近似 $\mathbf B_H$ 后，$\mathbf I-\mathbf P\mathbf B_H\mathbf P^{\mathsf T}\mathbf A$ 的谱仍在 $[0,1]$ 内，结论逐层递归成立。固定做 $k$ 次 V-cycle 对应 $\mathbf E^k$，同样满足。

#### 3.4.6 Krylov 外层为何更稳健

由 §3.4.5，$\sigma(\mathbf B\mathbf A)\subset(0,1]$，作为独立求解器的收敛因子是 $\lVert\mathbf E\rVert_{\mathbf A}=1-\lambda_{\min}(\mathbf B\mathbf A)$，由最难消去的那个误差分量决定。系数高对比度（例如材料与近空区域的刚度相差多个数量级）或几何细节在粗网格上无法表示时，常见的情形是只有少数误差分量被光滑与粗校正同时漏掉。这时 $\mathbf B\mathbf A$ 有少数几个接近 0 的离群特征值，其余特征值聚集在 $[a,1]$ 内。按 §2.3.2 的离群特征值论证，CG 多花大约离群值个数那么多步后，收敛速度只由有效条件数 $1/a$ 决定；独立的 V-cycle 迭代则一直受最差分量拖累（本段为本页推导）。

拓扑优化中 MGCG 自 Amir 等（2014）起被广泛采用；Wang2025 观察到，密度场非均质性更强的多孔填充优化需要明显更多的 MGCG 迭代（[[../../literature/topopt/matrix-free/translations/Wang2025-top3d-xl-matrix-free-matlab-zh#7 结果|Wang2025 第 7 节]]）。

#### 3.4.7 乘性与加性多层预条件子

标准 V-cycle 是**乘性**（multiplicative）的：各层依次处理，每层把前光滑后更新过的残差交给下一层，每层每次循环要作用若干次 $\mathbf A_l$。按子空间校正框架（Xu [10]），另一类是**加性**（additive）的：各层同时作用于同一个残差的限制，

$$
\mathbf B_{\mathrm{add}}=\sum_{l=1}^{L-1}\hat{\mathbf P}_l\,\mathbf S_l\,\hat{\mathbf P}_l^{\mathsf T}+\hat{\mathbf P}_L\,\mathbf A_L^{-1}\hat{\mathbf P}_L^{\mathsf T},
$$

其中 $\hat{\mathbf P}_l$ 是从第 $l$ 层到最细层的复合延拓（$\hat{\mathbf P}_1=\mathbf I$），$\mathbf S_l$ 是第 $l$ 层的 SPD 光滑或缩放算子。Bramble–Pasciak–Xu（BPX）预条件子 [11] 是这一类的代表。

| | 乘性（标准 V-cycle） | 加性 |
|---|---|---|
| SPD 条件 | 需满足 §3.4.5 的光滑子收敛条件 | 各 $\mathbf S_l$ 为 SPD 即可 |
| 每次作用的算子乘法 | 各层都要作用 $\mathbf A_l$（残差更新与后光滑） | 循环内不作用 $\mathbf A_l$，只需各层对角（若 $\mathbf S_l$ 为对角缩放）与最粗层分解 |
| 并行性 | 层间串行 | 各层相互独立，可并行 |
| 收敛 | 预条件后谱更集中，迭代次数少 | 谱较分散，迭代次数通常更多；单独作为迭代法须加阻尼，一般只作预条件子 |

两者的取舍取决于"迭代次数增加的倍数"与"单步代价下降的倍数"之比。Wang2025 的"对角松弛"V-cycle 省去了算法 2 中更新残差的那一行，并把后光滑改为 $\mathbf z^{[l]}\leftarrow\mathbf z^{[l]}+w\,\mathbf r^{[l]}./\mathbf D^{[l]}$，且作用于除最粗层外的每一层（含最细层）。展开递推可得 $\mathbf z^{[l]}=2w(\mathbf D^{[l]})^{-1}\mathbf r^{[l]}+\mathbf P^{[l+1]}\mathbf z^{[l+1]}$、$\mathbf r^{[l+1]}=(\mathbf P^{[l+1]})^{\mathsf T}\mathbf r^{[l]}$，即 $\mathbf S_l=2w\,\mathbf D_l^{-1}$ 的加性形式。原文没有这样命名，这一归类是本页推导。原文把对角松弛与跳过第 2 层的非二进粗化合起来称为"改进非二进 V 循环"，并给出判据：迭代次数增长不超过 2 倍即有净收益（[[../../literature/topopt/matrix-free/translations/Wang2025-top3d-xl-matrix-free-matlab-zh#4.2 多重网格预条件子|Wang2025 4.2 节]]）。原文的算例中，它的迭代次数多于标准 V 循环，但总耗时最短、内存最低（[[../../literature/topopt/matrix-free/translations/Wang2025-top3d-xl-matrix-free-matlab-zh#7 结果|Wang2025 第 7 节]]）。

### 3.5 区域分解

区域分解按子域构造 $\mathbf B$：每个子域上求解（或近似求解）局部问题，再把局部修正组合起来。各子域同时作用于同一残差即加性 Schwarz，依次作用即乘性 Schwarz，二者与 §3.4.7 的加性 / 乘性多层预条件子同属子空间校正框架（Xu [10]）。它与并行分区天然匹配；只用子域局部求解的一层 Schwarz，收敛随子域数增加而退化，加入粗空间后才可扩展。非重叠子结构把问题化为界面上的 Schur 补方程，可直接分解求解（见 [[../exact-substructural]]），也可在界面上用 Krylov 方法迭代求解，本页不展开。

### 3.6 信息需求与代价核算

| 预条件子 | 需要的信息 | 说明 |
|---|---|---|
| Jacobi / 对角缩放 | 对角元 | 最廉价，任何能取到对角的表示都可用；对系数跳跃问题效果有限 |
| 块 Jacobi、Gauss-Seidel、SSOR | 对角块或矩阵行 | 松弛类（§3.2） |
| 不完全分解 ILU(k) / IC(k) / ILUT | 稀疏矩阵元素 | 需要显式稀疏矩阵及其稀疏结构（§3.3） |
| 多项式预条件 | 谱区间估计 | 只需算子作用（§3.3） |
| AMG | 矩阵元素及 strength-of-connection | 粗化完全由矩阵元素驱动（§3.4.3） |
| GMG | 网格层次与层间转移算子 | 不需要矩阵元素，但需要几何层次（§3.4） |
| 区域分解 / Schwarz | 子域局部矩阵，可选粗空间 | 与并行分区天然匹配（§3.5） |
| 低阶 / 代理算子 | 一个更易组装的近似算子 | 高阶算子用低阶组装矩阵作预条件，或用降阶模型近似（§3.3） |

这张表决定了"当主算子不显式组装时，预条件子还能怎么构造"：装配层级约束的是预条件器而不是求解器，主算子与预条件子可以取不同层级，判据与推导由 [[../matrix-free/assembly-levels#3. 三条跨层级性质]] 不变量 3 维护。

预条件的总代价分三部分，性能报告须分别注明：

- **setup**：构造 $\mathbf B$ 的一次性成本，ILU 与 AMG 的 setup 可能与若干次求解相当；
- **apply**：每步 Krylov 迭代作用一次 $\mathbf B$ 的成本，需与算子作用同量级比较；
- **update**：矩阵变化后（例如拓扑优化中每次材料分布更新）$\mathbf B$ 是重建、局部更新还是复用。

一个预条件子值得用，当且仅当减少的迭代次数乘以每步节省，超过 setup 与 apply 增加的总量。矩阵频繁变化的场景中 update 成本往往主导取舍：粗化与 Galerkin 粗算子需要逐次重建的 AMG、高阶 ILU 在这类场景中代价偏高，网格层次固定、只需按新系数重算粗算子的 GMG 更容易摊薄。

## 参考依据

- [1] SAAD Y. Iterative Methods for Sparse Linear Systems[M]. 2nd ed. Philadelphia: SIAM, 2003 — §4 定常迭代、分裂与收敛定理（§2.1、§3.2）；§6.1 Krylov 子空间与投影；§6.5 GMRES 与重启；§6.7 CG 及其收敛界；§6.11 CG 的并行实现与内积归约；§7.1 GMRES 与 Arnoldi 过程；§7.4 BiCGSTAB、TFQMR 等免转置变体（§2.3，章节号未逐一核对原书）；§9 预条件迭代与 §9.4 Flexible GMRES（§2.4、§3.1）；§10 预条件技术（ILU、块预条件，§3.3）；§12.3 多项式预条件与 Chebyshev 加速（§2.2、§3.3）；§13 多重网格方法（§3.4）；§14 区域分解（§3.5）。未入库文献。
- [2] VARGA R S. Matrix Iterative Analysis[M]. 2nd ed. Berlin: Springer, 2000 — 正则分裂、SOR 最优松弛因子理论（§3.2）。未入库文献。
- [3] TREFETHEN L N, BAU D. Numerical Linear Algebra[M]. Philadelphia: SIAM, 1997 — Lecture 32、35、38 关于 Krylov 方法作为多项式逼近的观点与 CG 收敛界（§1.1、§2.3.1、§2.3.2）。未入库文献。
- [4] BRIGGS W L, HENSON V E, MCCORMICK S F. A Multigrid Tutorial[M]. 2nd ed. Philadelphia: SIAM, 2000 — 松弛的光滑性质（§3.2）、粗网格校正、V/W/F-cycle 与 AMG 基础（§3.4.1–§3.4.3）。未入库文献。
- [5] TROTTENBERG U, OOSTERLEE C W, SCHÜLLER A. Multigrid[M]. London: Academic Press, 2001 — 多重网格收敛理论与算法设计（§3.4）。未入库文献。
- [6] BENZI M. Preconditioning techniques for large linear systems: a survey[J]. Journal of Computational Physics, 2002, 182(2): 418-477 — 预条件技术综述（§3）。未入库文献。
- [7] WATHEN A J. Preconditioning[J]. Acta Numerica, 2015, 24: 329-376 — 谱聚集而非条件数作为预条件目标的论述（§3.1）。未入库文献。
- [8] KRONBICHLER M, KORMANN K. A generic interface for parallel cell-based finite element operator application[J]. Computers & Fluids, 2012, 63: 135-147 — 只需算子作用接口的 Krylov 求解与单元级算子按需作用的结合路径（§2.3.1）。cite key `kronbichlerGenericInterfaceParallel2012`。
- [9] GHYSELS P, VANROOSE W. Hiding global synchronization latency in the preconditioned Conjugate Gradient algorithm[J]. Parallel Computing, 2014, 40(7): 224-238 — pipelined CG 及其与标准 CG 数值行为的差异（§2.3.5）。未入库文献。
- [10] XU J. Iterative methods by space decomposition and subspace correction[J]. SIAM Review, 1992, 34(4): 581-613. DOI: 10.1137/1034116 — 乘性与加性子空间校正框架，涵盖多层方法与区域分解（§3.4.7、§3.5）。未入库文献，出版信息经 CrossRef 核对。
- [11] BRAMBLE J H, PASCIAK J E, XU J. Parallel multilevel preconditioners[J]. Mathematics of Computation, 1990, 55(191): 1-22. DOI: 10.1090/S0025-5718-1990-1023042-6 — BPX 加性多层预条件子（§3.4.7）。未入库文献，出版信息经 CrossRef 核对。
- [12] XU J, ZIKATANOV L. Algebraic multigrid methods[J]. Acta Numerica, 2017, 26: 591-721. DOI: 10.1017/S0962492917000083 — 对称 V-cycle 的误差传播算子与作为 SPD 预条件子的条件（§3.4.5）。未入库文献，出版信息经 CrossRef 核对；§3.4.5 的推导为本页按其框架写出，未逐式对照原文。
- [13] NOTAY Y. Flexible conjugate gradients[J]. SIAM Journal on Scientific Computing, 2000, 22(4): 1444-1460. DOI: 10.1137/S1064827599362314 — 变预条件下的截断 FCG（§2.4）。未入库文献，出版信息经 CrossRef 核对。
- [14] GOLUB G H, YE Q. Inexact preconditioned conjugate gradient method with inner-outer iteration[J]. SIAM Journal on Scientific Computing, 1999, 21(4): 1305-1320. DOI: 10.1137/S1064827597323415 — 非精确内层预条件下的 PCG 变体（§2.4）。未入库文献，出版信息经 CrossRef 核对；Polak–Ribière 形式 $\beta_j$ 的归属待对照原文确认。
- [15] [[../../literature/topopt/matrix-free/translations/Wang2025-top3d-xl-matrix-free-matlab-zh|Wang2025 译文]]（citekey `Wang2025-top3d-xl-matrix-free-matlab`）— 拓扑优化中的 MGCG（算法 1、2）、对角松弛的作用范围与非二进 V 循环、非均质性对迭代次数的影响（§3.4.6、§3.4.7）；其中 MGCG 自 Amir 等（2014）起被广泛采用的说法经该文转引，Amir 等（2014）未入库。
- [16] PAIGE C C, SAUNDERS M A. Solution of sparse indefinite systems of linear equations[J]. SIAM Journal on Numerical Analysis, 1975, 12(4): 617-629. DOI: 10.1137/0712047 — MINRES 与 SYMMLQ（§2.3.3）。未入库文献，出版信息经 CrossRef 核对。
- [17] ELMAN H, SILVESTER D, WATHEN A. Finite Elements and Fast Iterative Solvers: with Applications in Incompressible Fluid Dynamics[M]. 2nd ed. Oxford: Oxford University Press, 2014. DOI: 10.1093/acprof:oso/9780199678792.001.0001 — 鞍点系统的 MINRES 与 SPD 块对角预条件（§2.3.3）。未入库文献，出版信息经 CrossRef 核对；所支撑结论的原书章节未核对。
