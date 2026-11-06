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
date_update: 2026-10-25
---

# 迭代法

迭代法不分解 $\mathbf A$，而是反复调用算子作用 $\mathbf y=\mathbf A\mathbf x$（加上预条件子所需的少量矩阵信息）逐步改进近似解。它的内存只随向量与算子表示增长，是三维大规模问题与不显式组装全局矩阵的算子表示的必经之路；代价是收敛速度受矩阵性质影响；对 SPD 问题，特征值分布是关键因素，通常借助预条件改善。

本页先按两条轴给迭代法分类：外层迭代格式（定常、Chebyshev、Krylov）决定怎样使用近似逆 $\mathbf B\approx\mathbf A^{-1}$，预条件子的构造（松弛、不完全分解、多项式、多重网格、区域分解）决定 $\mathbf B$ 是什么；具体求解器是二者的组合。

## 1. 迭代法的分类

### 1.1 迭代的一般形式

设 $\mathbf A$ 可逆，精确解为 $\mathbf x^\ast$，第 $k$ 步的数值近似解为 $\mathbf x_k$。该步的误差与残差满足

$$
\mathbf e_k=\mathbf x^\ast-\mathbf x_k,\qquad
\mathbf r_k=\mathbf b-\mathbf A\mathbf x_k=\mathbf A\mathbf e_k .
$$

因此，$\mathbf A^{-1}\mathbf r_k$ 就是使当前近似解变为精确解的修正量。迭代法逐步构造可计算的修正 $\mathbf s_k$，更新 $\mathbf x_{k+1}=\mathbf x_k+\mathbf s_k$。常用做法是以易于作用的近似逆 $\mathbf B$ 处理残差，得到预条件残差 $\mathbf z_k=\mathbf B\mathbf r_k$，再结合具体方法构造修正。

据此，可从两条轴区分迭代求解方案：预条件子决定怎样处理残差，外层迭代格式决定怎样构造修正量。

### 1.2 两条分类轴

**轴一：外层迭代格式**，即怎样构造修正量（§2）

| 外层格式 | 更新特点 | 主要收敛因素 | 是否需要内积 |
|---|---|---|---|
| 定常迭代（§2.1） | 用固定的线性算子处理残差，直接作为修正量 | 迭代矩阵的谱半径决定是否对任意初值收敛 | 更新不需要 |
| Chebyshev 迭代（§2.2） | 按预估谱区间确定递推系数，组合当前残差与已有迭代信息 | 谱区间估计及区间内的条件数（SPD 情形） | 更新不需要 |
| Krylov 方法（§2.3） | 在生成的子空间中按投影或极小化准则选取近似解 | 方法、预条件后的矩阵性质及初始残差；非正规情形不能只看特征值 | 通常需要 |

表中内积指更新过程；残差范数判停仍可能需要内积（§2.4）。

**轴二：预条件子的构造**，即 $\mathbf B$ 是什么（§3）

| 构造类别        | 代表                                                                                               |
| ----------- | ------------------------------------------------------------------------------------------------ |
| 松弛类（§3.1）   | Jacobi、Gauss-Seidel、逐次超松弛（Successive Over-Relaxation, SOR）、对称逐次超松弛（Symmetric SOR, SSOR）、块 Jacobi |
| 不完全分解（§3.2） | 不完全 LU 分解（Incomplete LU, ILU）、不完全 Cholesky 分解（Incomplete Cholesky, IC）                           |
| 多项式（§3.3）   | Chebyshev 多项式预条件                                                                                 |
| 多重网格（§3.4）  | 几何多重网格（Geometric Multigrid, GMG）、代数多重网格（Algebraic Multigrid, AMG）                                |
| 区域分解（§3.5）  | 加性 / 乘性 Schwarz                                                                                  |

不预条件时 $\mathbf B=\mathbf I$（或一个标量缩放），只剩轴一。

### 1.3 具体求解器是两条轴的组合

下表中的组合按"预条件子-外层方法"命名。外层的 Krylov 方法以 CG 与广义极小残差法（Generalized Minimal Residual, GMRES）为代表；Jacobi-PCG 即以 Jacobi 为预条件子的 PCG，多重网格预条件共轭梯度法（Multigrid-Preconditioned Conjugate Gradient, MGCG）即以一次 V-cycle 为预条件子的 PCG。

| 预条件子 \ 外层迭代格式 | 定常迭代                    | Chebyshev 迭代     | Krylov 子空间方法        |
| ------------- | ----------------------- | ---------------- | ------------------- |
| 松弛类           | Jacobi、Gauss-Seidel、SOR | Chebyshev-Jacobi | Jacobi-PCG、SSOR-PCG |
| 不完全分解         | 很少单独使用                  | 很少使用             | IC-PCG、ILU-GMRES    |
| 多重网格          | 多重网格求解器                 | 很少使用             | MGCG、AMG-PCG        |
| 区域分解          | Schwarz                 | 很少使用             | Schwarz-PCG         |

Chebyshev-Jacobi 主要用作多重网格的光滑子（§2.2）。

## 2. 外层迭代格式

### 2.1 定常迭代

“定常” 指求解同一个线性系统时，每步使用同一个更新规则：取固定的线性算子 $\mathbf B$，每步将预条件残差 $\mathbf z_k=\mathbf B\mathbf r_k$ 直接作为修正量，即 $\mathbf s_k=\mathbf z_k$，按 $\mathbf x_{k+1}=\mathbf x_k+\mathbf B\mathbf r_k$ 更新。$\mathbf B$ 固定，但残差与修正量随迭代变化。

记迭代矩阵 $\mathbf G=\mathbf I-\mathbf B\mathbf A$，则 $\mathbf x_{k+1}=\mathbf G\mathbf x_k+\mathbf B\mathbf b$，误差 $\mathbf e_k=\mathbf G^k\mathbf e_0$，其中 $\mathbf e_0=\mathbf x^\ast-\mathbf x_0$ 为初始误差。对任意初值收敛的充要条件是迭代矩阵 $\mathbf G$ 的所有特征值的模都小于 $1$，即 $\max_i|\lambda_i(\mathbf G)|<1$。展开递推得 $\mathbf x_k$ 的显式表达式

$$
\mathbf x_k=\mathbf x_0+\sum_{j=0}^{k-1}\mathbf G^j\,\mathbf B\mathbf r_0 ,
$$

其中 $\mathbf G^j\mathbf B\mathbf r_0=\mathbf B\mathbf r_j=\mathbf s_j$ 是第 $j$ 步的修正量。因此，上式表示第 $k$ 步近似解等于初始值加上前 $k$ 步修正量的累积。

定常迭代也常用矩阵分裂表示：取 $\mathbf A=\mathbf M-\mathbf N$，其中 $\mathbf M$ 可逆且便于求解，则

$$
\mathbf M\mathbf x_{k+1}=\mathbf N\mathbf x_k+\mathbf b,
$$

对应 $\mathbf B=\mathbf M^{-1}$。不同分裂对应的具体方法见 §3.1。

### 2.2 Chebyshev 迭代

设 $\mathbf A$ 与固定线性预条件子 $\mathbf B$ 均为 SPD，且 $\mathbf B\mathbf A$ 的特征值落在已知区间 $0<\lambda_{\min}<\lambda_{\max}$ 内。在精确算术下，Chebyshev 迭代的误差可写为

$$
\mathbf e_k=\varphi_k(\mathbf B\mathbf A)\mathbf e_0,\qquad
\deg\varphi_k\le k,\qquad \varphi_k(0)=1 .
$$

$\varphi_k$ 称为误差多项式，描述初始误差经迭代后的变化；§2.1 的定常迭代对应 $\varphi_k(t)=(1-t)^k$。Chebyshev 迭代则按谱区间选取（[1]、[3]）

$$
\varphi_k(t)=\frac{T_k\!\left(\dfrac{\lambda_{\max}+\lambda_{\min}-2t}{\lambda_{\max}-\lambda_{\min}}\right)}{T_k\!\left(\dfrac{\lambda_{\max}+\lambda_{\min}}{\lambda_{\max}-\lambda_{\min}}\right)},
$$

$T_k$ 为 $k$ 次 Chebyshev 多项式。它是在整个区间 $[\lambda_{\min},\lambda_{\max}]$ 上最大值最小的满足 $\varphi_k(0)=1$ 的多项式，误差缩减因子约为 $(\sqrt\kappa-1)/(\sqrt\kappa+1)$，$\kappa=\lambda_{\max}/\lambda_{\min}$，与 CG 收敛界的量级相同。与 CG 的区别是：$\varphi_k$ 由区间端点预先确定，迭代中不需要内积，因而没有全局归约（§2.3.4）；代价是需要谱区间估计，估计偏差会降低收敛速度，且无法像 CG 那样利用谱在区间内部的聚集。

它在实践中主要有两种用途：作多重网格的光滑子，只针对 $[\lambda_{\max}/c,\lambda_{\max}]$ 的高频部分取多项式（$c$ 为预设的比值）；作多项式预条件子（§3.3）。

### 2.3 Krylov 子空间方法

先以未预条件的系统为例。由初始残差 $\mathbf r_0=\mathbf b-\mathbf A\mathbf x_0$ 及其经 $\mathbf A$ 反复作用得到的向量，构造 Krylov 子空间

$$
\mathcal K_k(\mathbf A,\mathbf r_0)=\operatorname{span}\{\mathbf r_0,\mathbf A\mathbf r_0,\dots,\mathbf A^{k-1}\mathbf r_0\}.
$$

在该空间维数为 $k$ 时，取一组基 $\mathbf V_k=[\mathbf v_1,\dots,\mathbf v_k]$，近似解写为

$$
\mathbf x_k=\mathbf x_0+\mathbf V_k\mathbf y_k,
$$

其中 $\mathbf y_k\in\mathbb R^k$ 为组合系数，由具体方法的投影或极小化准则确定。


#### 2.3.1 CG

**适用问题。** $\mathbf A$ 为 SPD，即约束充分的位移法线弹性刚度矩阵。把 $\mathbf b$ 看作载荷，解 $\mathbf A\mathbf x=\mathbf b$ 等价于求总势能 $\Pi(\mathbf x)=\tfrac12\mathbf x^{\mathsf T}\mathbf A\mathbf x-\mathbf b^{\mathsf T}\mathbf x$ 的最小值点，残差 $\mathbf r=\mathbf b-\mathbf A\mathbf x$ 就是不平衡力。

**算法。** 最速下降法（反复沿 $\mathbf r$ 下降）会来回折返，收敛慢。CG 把搜索方向 $\mathbf p_k$ 修正为与全部旧方向 $\mathbf A$-共轭（$\mathbf p_i^{\mathsf T}\mathbf A\mathbf p_j=0$），类似于振型互不耦合，于是后面的步骤不会破坏前面已经取得的最小值。$k$ 步后得到的是 Krylov 子空间中势能最小的解（Shewchuk [19]）。初值取 $\mathbf p_0=\mathbf r_0$，每步：

| 步骤 | 计算 | 含义 |
|---|---|---|
| 1 | $\mathbf q=\mathbf A\mathbf p_k$ | 唯一一次刚度矩阵作用 |
| 2 | $\alpha_k=\mathbf r_k^{\mathsf T}\mathbf r_k/\mathbf p_k^{\mathsf T}\mathbf q$ | 沿 $\mathbf p_k$ 走到势能最低处 |
| 3 | $\mathbf x_{k+1}=\mathbf x_k+\alpha_k\mathbf p_k$，$\mathbf r_{k+1}=\mathbf r_k-\alpha_k\mathbf q$ | 更新位移与不平衡力 |
| 4 | $\beta_k=\mathbf r_{k+1}^{\mathsf T}\mathbf r_{k+1}/\mathbf r_k^{\mathsf T}\mathbf r_k$，$\mathbf p_{k+1}=\mathbf r_{k+1}+\beta_k\mathbf p_k$ | 新方向 = 不平衡力 + 一点旧方向 |

只用上一个方向修正一次，新方向就与全部旧方向共轭（这是 $\mathbf A$ 对称带来的），所以 CG 是短递推。

**收敛与代价。**

- 每步 1 次算子作用、2 次内积，只需保存 3–4 个向量。
- 迭代次数随网格加密按 $O(h^{-1})$ 增长：步数约为 $O(\sqrt\kappa)$，而拟一致网格上二阶椭圆问题的刚度矩阵 $\kappa=O(h^{-2})$。
- 每步最小化的是势能而不是残差，$\lVert\mathbf r_k\rVert_2$ 不一定单调下降，出现波动属正常现象。
- 精确算术下至多 $n$ 步终止，实践中正交性会逐渐丢失，这一终止性质不可依赖。

**使用要点。**

- **适用条件**：$\mathbf A$ 须为 SPD。约束不足、结构仍有刚体位移时，刚度矩阵只是半正定，CG 可能不收敛；应先补足约束。
- **边界条件**：Dirichlet 条件须用保持对称的方式施加（受约束的行与列同时消去，或置零后对角置 1），只消去行会破坏对称性。
- **停机判据**：监测哪种残差、用什么范数、相对判据以什么为参照，见 §2.4。

#### 2.3.2 MINRES

**适用问题。** $\mathbf A$ 对称但不定，典型的是鞍点系统，例如 Hu–Zhang 等混合有限元、近不可压缩弹性、Stokes 流动。这类系统同时有正负特征值，CG 第 2 步的分母 $\mathbf p_k^{\mathsf T}\mathbf A\mathbf p_k$ 可能为零或为负，算法中断。

**算法。** MINRES 用 Lanczos 过程生成 Krylov 子空间的正交基 $\mathbf V_k=[\mathbf v_1,\dots,\mathbf v_k]$，满足 $\mathbf A\mathbf V_k=\mathbf V_{k+1}\bar{\mathbf T}_k$，其中 $\bar{\mathbf T}_k$ 是 $(k+1)\times k$ 三对角矩阵。取 $\mathbf x_k=\mathbf x_0+\mathbf V_k\mathbf y_k$，由基的正交性

$$
\lVert\mathbf r_k\rVert_2=\lVert\mathbf r_0-\mathbf A\mathbf V_k\mathbf y_k\rVert_2=\lVert\beta_1\mathbf e_1-\bar{\mathbf T}_k\mathbf y_k\rVert_2,\qquad \beta_1=\lVert\mathbf r_0\rVert_2 ,
$$

于是残差最小化化为一个 $(k+1)\times k$ 的小最小二乘问题，用 Givens 旋转逐列化上三角求解（Paige–Saunders [16]）。初值取 $\mathbf v_1=\mathbf r_0/\beta_1$、$\mathbf v_0=\mathbf 0$，每步：

| 步骤 | 计算 | 含义 |
|---|---|---|
| 1 | $\mathbf q=\mathbf A\mathbf v_k$ | 唯一一次算子作用 |
| 2 | $\alpha_k=\mathbf v_k^{\mathsf T}\mathbf q$，$\mathbf q\leftarrow\mathbf q-\alpha_k\mathbf v_k-\beta_k\mathbf v_{k-1}$，$\beta_{k+1}=\lVert\mathbf q\rVert_2$，$\mathbf v_{k+1}=\mathbf q/\beta_{k+1}$ | Lanczos 三项递推：$\mathbf A$ 对称，新向量只需对前两个基向量正交化 |
| 3 | 用新的 Givens 旋转把 $\bar{\mathbf T}_k$ 第 $k$ 列化为上三角，同时作用在右端 $\beta_1\mathbf e_1$ 上 | 增量求解最小二乘；旋转后右端第 $k+1$ 个分量的绝对值就是 $\lVert\mathbf r_k\rVert_2$ |
| 4 | $\mathbf d_k=(\mathbf v_k-r_{k-1,k}\mathbf d_{k-1}-r_{k-2,k}\mathbf d_{k-2})/r_{kk}$，$\mathbf x_k=\mathbf x_{k-1}+t_k\mathbf d_k$ | 上三角因子带宽为 3，解可逐步更新，不必保存全部 $\mathbf v_j$ |

第 4 步中 $r_{jk}$ 是 $\bar{\mathbf T}_k$ 经旋转后上三角因子的元素，$t_k$ 是旋转后右端的第 $k$ 个分量；第 3 步旋转只改动右端的第 $k$、$k+1$ 个分量，前 $k-1$ 个分量不再变化，所以解可以按列累加（本页按 [1]、[16] 整理，未逐式对照原文）。

**收敛与代价。**

- 每步 1 次算子作用、2 次内积（$\alpha_k$ 与 $\beta_{k+1}$），与 CG 同量级；须保存 $\mathbf v_{k-1},\mathbf v_k,\mathbf v_{k+1},\mathbf d_{k-1},\mathbf d_k$ 与 $\mathbf x_k$，比 CG 多几个向量。
- $\lVert\mathbf r_k\rVert_2$ 在子空间内最小，因此单调下降；残差范数由第 3 步免费得到，判停不需额外内积。
- 收敛由预条件后矩阵的正、负两侧特征值区间共同决定，两侧都要被预条件子压缩。

**使用要点。**

- 预条件子必须是 **SPD** 的，才能保持短递推，此时极小化的是 $\mathbf M^{-1}$-范数下的残差；对鞍点系统常用块对角预条件，各块分别近似原块与 Schur 补（Elman–Silvester–Wathen [17]，原书章节未核对）。
- 同一文献中的 SYMMLQ 也适用于对称不定矩阵，它极小化的是误差的 2-范数而不是残差，所用仿射空间为 $mathbf x_0+mathbf Amathcal K_k$，实践中较少使用。

#### 2.3.3 GMRES

**适用问题。** $\mathbf A$ 非对称，例如接触摩擦、跟随载荷、非关联塑性的切线刚度，以及对流占优问题。

**算法。** GMRES 用 Arnoldi 过程生成正交基，满足 $\mathbf A\mathbf V_k=\mathbf V_{k+1}\bar{\mathbf H}_k$，其中 $\bar{\mathbf H}_k$ 是 $(k+1)\times k$ 上 Hessenberg 矩阵；残差同样化为 $\lVert\mathbf r_k\rVert_2=\lVert\beta_1\mathbf e_1-\bar{\mathbf H}_k\mathbf y_k\rVert_2$，用 Givens 旋转增量求解（Saad [1]）。与 MINRES 的差别只在基的生成：$\mathbf A$ 不对称，$\bar{\mathbf H}_k$ 不再三对角，新基向量须对全部旧基向量正交化，解也不能按列累加。初值取 $\mathbf v_1=\mathbf r_0/\beta_1$，每步：

| 步骤 | 计算 | 含义 |
|---|---|---|
| 1 | $\mathbf q=\mathbf A\mathbf v_k$ | 唯一一次算子作用 |
| 2 | 对 $j=1,\dots,k$：$h_{jk}=\mathbf v_j^{\mathsf T}\mathbf q$，$\mathbf q\leftarrow\mathbf q-h_{jk}\mathbf v_j$；$h_{k+1,k}=\lVert\mathbf q\rVert_2$，$\mathbf v_{k+1}=\mathbf q/h_{k+1,k}$ | Arnoldi 长递推（修正 Gram–Schmidt），$k+1$ 次内积 |
| 3 | 用新的 Givens 旋转把 $\bar{\mathbf H}_k$ 第 $k$ 列化为上三角，同时作用在右端 | 增量最小二乘；旋转后右端第 $k+1$ 个分量的绝对值就是 $\lVert\mathbf r_k\rVert_2$，用于判停 |
| 4 | 达到容限或 $k=m$ 时：回代上三角方程得 $\mathbf y_k$，$\mathbf x_k=\mathbf x_0+\mathbf V_k\mathbf y_k$ | 一次性组合全部基向量；未收敛则以 $\mathbf x_k$ 为初值重启 |

**收敛与代价。**

- 第 $k$ 步 1 次算子作用、$k+1$ 次内积，须保存 $k+1$ 个基向量与 $\bar{\mathbf H}_k$，存储与每步计算量随 $k$ 线性增长，实践中以 $m$ 步为周期重启，记作 GMRES(m)。
- $\lVert\mathbf r_k\rVert_2$ 在子空间内最小，一个重启周期内单调下降；重启丢弃已建立的子空间，可能停滞。
- 非对称矩阵的收敛不只由特征值决定，还与特征向量矩阵的条件数有关（Saad [1]），没有 CG 那样仅凭 $\kappa$ 的步数估计。

**与 BiCGSTAB 的取舍。** 对非对称矩阵，短递推（省存储）与每步最优（收敛稳）不能同时得到（Faber–Manteuffel [18]），GMRES 与 BiCGSTAB 各取其一：

| | GMRES | BiCGSTAB（及 TFQMR） |
|---|---|---|
| 基的生成 | Arnoldi，长递推：第 $k$ 步要与前面全部 $k$ 个基向量正交化 | 双正交 Lanczos，短递推 |
| 取解准则 | 子空间内残差 $\lVert\mathbf r_k\rVert_2$ 最小 | 不再每步最优 |
| 残差行为 | 单调下降 | 不单调，可能剧烈振荡，个别情况下算法中断（breakdown） |
| 存储与每步计算量 | 随 $k$ 增长，实践中须重启 | 固定，不随迭代步增长 |

**使用要点。**

- **默认先用 GMRES**，它收敛稳健、残差单调。存储过大又不愿频繁重启时，再换 BiCGSTAB；BiCGSTAB 收敛不稳定时，先换回 GMRES 确认问题本身是否可解，再回头调整预条件子。
- **重启 GMRES(m)**：每做 $m$ 步就以当前解为初值重新开始，用来限制存储。$m$ 越小越省内存，但可能停滞甚至不收敛；$m$ 的取值须按问题试验。
- **左、右预条件**：左预条件极小化的是预条件后的残差 $\lVert\mathbf M^{-1}\mathbf r\rVert_2$，右预条件极小化真残差 $\lVert\mathbf r\rVert_2$（§3.7）；判停监测量与之的对应见 §2.4。
- 预条件子不要求对称。预条件子每步变化时改用 FGMRES：它额外保存每步预条件后的向量，以更长的递推换取对变预条件的容忍。

#### 2.3.4 并行执行中的同步点

Krylov 迭代的每一步由三类运算组成：算子作用 $\mathbf A\mathbf p$、向量更新 $\mathbf y\leftarrow a\mathbf x+\mathbf y$（AXPY）、内积。前两类在分区之间没有依赖（算子作用只在界面上需要交换数据，且可以与内部单元的计算重叠），唯一必须让全部执行实体同步的是内积。

- **每步归约次数**：CG 每次迭代需要 2 次内积（$\mathbf r^{\mathsf T}\mathbf r$ 与 $\mathbf p^{\mathsf T}\mathbf A\mathbf p$），PCG 同样是 2 次（$\mathbf r^{\mathsf T}\mathbf z$ 与 $\mathbf p^{\mathsf T}\mathbf A\mathbf p$）；GMRES 的 Arnoldi 正交化每步归约次数随重启维数 $m$ 增长，代价更高。
- **在各并行层的形态**：进程级是一次 `MPI_Allreduce` 全局同步，设备内是 block reduction 加一次设备级归约，线程级是共享内存归约。进程级是唯一会阻塞全部 rank 的那一种，它必须等所有 rank 到齐才能给出标量，因此强扩展曲线的拐点通常出现在内积而不是算子作用上。三层并行的完整卡点讨论见 [[../gpu-hpc/parallel-levels#3. 两个绕不开的断点]]。
- **共享自由度必须加权**：分区之间有共享自由度时，直接对各 rank 的局部内积求和会重复计数界面分量，必须使用按引用计数加权的内积，它精确等于串行内积，从而保证并行与串行的迭代序列逐点一致；定理与实现约定见 [[../gpu-hpc/distributed-operator-and-shared-dofs#4. 重叠加权内积与 Krylov 求解器收敛理论]]。
- **降低归约代价属于换算法**：s-step / communication-avoiding CG 与 pipelined CG 通过重组递推把多次归约合并或与算子作用重叠，但它们改变了浮点运算次序与数值稳定性，收敛行为需单独验证，不能视为同一算法的不同实现。

### 2.4 收敛监测：残差向量与范数

迭代中误差 $\mathbf e_k$ 不可计算，只能用残差判停。判停量同时取决于两个选择：监测真残差 $\mathbf r_k$ 还是预条件残差 $\mathbf z_k=\mathbf B\mathbf r_k$，以及用什么范数度量。常用的有三种：

| 监测量 | 定义 | 在 PCG 中的额外代价 | 与误差的关系 |
|---|---|---|---|
| 真残差 | $\lVert\mathbf r_k\rVert_2$ | 多一次内积 $\mathbf r^{\mathsf T}\mathbf r$，可与 $\mathbf r^{\mathsf T}\mathbf z$ 放进同一次归约 | 直接度量原方程的不平衡力；$\lVert\mathbf e_k\rVert_2\le\lVert\mathbf A^{-1}\rVert_2\lVert\mathbf r_k\rVert_2$，数值随 $\mathbf A$ 的尺度变化 |
| 预条件残差 | $\lVert\mathbf B\mathbf r_k\rVert_2$ | 多一次内积 $\mathbf z^{\mathsf T}\mathbf z$，可放进同一次归约 | $\mathbf B\approx\mathbf A^{-1}$ 时近似 $\lVert\mathbf e_k\rVert_2$；数值随 $\mathbf B$ 的缩放变化，$\mathbf B$ 近似较差时它已很小而真残差仍可能较大 |
| 自然范数 | $\sqrt{\mathbf r_k^{\mathsf T}\mathbf B\mathbf r_k}$ | 无，$\mathbf r^{\mathsf T}\mathbf z$ 已在递推中算出 | 与能量范数误差谱等价，见下式；要求 $\mathbf B$ 为 SPD |

不预条件时 $\mathbf B=\mathbf I$，前两种重合，自然范数也退化为 $\lVert\mathbf r_k\rVert_2$。对 SPD 的 $\mathbf A$ 与 $\mathbf B$，由 $\mathbf r_k=\mathbf A\mathbf e_k$，令 $\mathbf y=\mathbf A^{1/2}\mathbf e_k$，则 $\mathbf r_k^{\mathsf T}\mathbf B\mathbf r_k=\mathbf y^{\mathsf T}\mathbf A^{1/2}\mathbf B\mathbf A^{1/2}\mathbf y$，而 $\mathbf A^{1/2}\mathbf B\mathbf A^{1/2}$ 与 $\mathbf B\mathbf A$ 相似，因此

$$
\lambda_{\min}(\mathbf B\mathbf A)\,\lVert\mathbf e_k\rVert_{\mathbf A}^2\;\le\;\mathbf r_k^{\mathsf T}\mathbf B\mathbf r_k\;\le\;\lambda_{\max}(\mathbf B\mathbf A)\,\lVert\mathbf e_k\rVert_{\mathbf A}^2 .
$$

PCG 在 Krylov 子空间中极小化的正是 $\lVert\mathbf e_k\rVert_{\mathbf A}$，自然范数是与它最一致、又不增加计算的可算量。满足 §3.4.4 条件的 MGCG 有 $\sigma(\mathbf B\mathbf A)\subset(0,1]$，自然范数不超过 $\lVert\mathbf e_k\rVert_{\mathbf A}$，二者相差多少取决于 $\lambda_{\min}(\mathbf B\mathbf A)$（上表与本段为本页整理与推导，未对照教材逐条核对）。

**使用要点。**

- **相对判据的参照须用同一度量**：常用 $\lVert\mathbf r_k\rVert\le\mathrm{tol}\cdot\lVert\mathbf b\rVert$，分子与分母取同一种监测量，例如自然范数的参照为 $\sqrt{\mathbf b^{\mathsf T}\mathbf B\mathbf b}$。以 $\lVert\mathbf b\rVert$ 而非初始残差 $\lVert\mathbf r_0\rVert$ 为参照：用上一步解作初值（热启动）时 $\lVert\mathbf r_0\rVert$ 已经很小，同一个 tol 会变得过严，求解代价反而增加。
- **tol 不能跨监测量沿用**：三者之间的倍数取决于 $\mathbf A$、$\mathbf B$ 的谱与缩放，更换监测量或预条件子后，同一个 tol 对应的精度不同。比较不同预条件子时，应统一按真残差容限比较迭代次数与耗时（§3）。
- **单调性**：CG / PCG 中单调下降的是 $\lVert\mathbf e_k\rVert_{\mathbf A}$，上表三个监测量都不保证单调，曲线波动属正常。MINRES 与 GMRES 只保证各自所极小化的那个残差范数单调；GMRES 的左、右预条件分别对应预条件残差与真残差（§3.7）。
- **结束后复核**：监测量达到容限不等于解满足使用要求；求解结束后应计算一次真残差，必要时核对位移、柔顺度等目标量（[[linear-solvers-architecture#3. 选型后的验证]]）。
- **软件参数**：PETSc 的 `KSPSetNormType` 提供 `KSP_NORM_PRECONDITIONED`、`KSP_NORM_UNPRECONDITIONED`、`KSP_NORM_NATURAL` 与 `KSP_NORM_NONE`，分别对应上表三种监测量与不计算范数；各 Krylov 方法支持哪几种、默认取哪种，本页未对照文档核对，待确认。

## 3. 预条件子的构造

预条件子用于在每步迭代中处理残差，帮助外层方法构造更新。记为预条件而选取或构造的辅助矩阵为 $\mathbf M$，其逆作用定义预条件算子 $\mathbf B=\mathbf M^{-1}$；不同预条件方法通常对应不同的 $\mathbf M$。对残差施加预条件，即求解 $\mathbf M\mathbf z_k=\mathbf r_k$，得到预条件残差 $\mathbf z_k=\mathbf M^{-1}\mathbf r_k$，无需显式形成逆矩阵。例如，Jacobi 取 $\mathbf M=\operatorname{diag}(\mathbf A)$，只需逐分量相除。

“近似逆”并不保证 $\mathbf z_k$ 高精度逼近精确误差 $\mathbf e_k$，PCG 也不要求这种逐步精度。预条件的目的是改善 $\mathbf B\mathbf A$ 的特征值分布，使外层迭代用更少的步数达到目标精度。对固定 SPD 预条件子的 PCG，第 $k$ 步的误差由次数不超过 $k$ 的误差多项式作用于初始误差得到；要压低各特征方向的误差分量，就需要该多项式在相应特征值处都足够小。特征值更集中时，通常可用更低次数的多项式达到这一目标，从而减少迭代次数；降低最大与最小特征值之比，也可以改善 PCG 的经典收敛界。最终是否值得使用，还须比较构造和应用预条件子的成本（§3.6）。下表按构造方式分类，左、右及分裂等作用位置见 §3.7。

| 类别 | 代表 | 需要的信息 | 能否配 PCG | 矩阵变化时的更新代价 |
|---|---|---|---|---|
| 松弛类（§3.1） | Jacobi、SSOR、块 Jacobi | 对角、对角块或矩阵行 | Jacobi、SSOR、块 Jacobi 可以；单向 Gauss-Seidel 不对称，不可以 | 低：重取对角或对角块 |
| 不完全分解（§3.2） | ILU、IC、带阈值的 ILU（ILU with Threshold, ILUT） | 显式稀疏矩阵元素及稀疏结构 | IC 可以；ILU 不对称，不可以 | 高：须重新做不完全分解 |
| 多项式（§3.3） | Chebyshev 多项式 | 谱区间估计，只需算子作用 | $q$ 在谱上取正值时可以 | 低：重估谱区间 |
| GMG（§3.4） | 结构化网格上的 V-cycle | 网格层次与层间转移算子，不需要矩阵元素 | 满足 §3.4.4 的条件时可以 | 中：层次固定，按新系数重算粗层算子并重新分解最粗层 |
| AMG（§3.4） | BoomerAMG、GAMG | 矩阵元素及连接强度 | 满足 §3.4.4 的条件时可以 | 较高：粗化由矩阵元素驱动，矩阵变化后通常须重建 |
| 区域分解（§3.5） | 加性 / 乘性 Schwarz | 子域局部矩阵，可选粗空间 | 加性 Schwarz 可以 | 中：重新分解各子域局部矩阵 |


标准 PCG 和预条件 MINRES 要求实际作用于残差的 $\mathbf B$ 是固定的、线性的、对称正定的算子。这些是兼容条件，并不保证加速效果。例如，SPD 矩阵的 Jacobi 预条件满足这些条件，但忽略非对角耦合后是否有效，仍取决于具体问题；实际应比较达到同一真残差容限时的迭代次数与总耗时。GMRES、BiCGSTAB 可以使用非对称预条件子。若预条件作用随迭代变化，应选择适用的灵活方法，例如 FCG 或 FGMRES；其中 FCG 仍有相应的适用条件（§3.7）。

### 3.1 松弛类

取 $\mathbf A=\mathbf D-\mathbf L-\mathbf U$（对角、严格下三角、严格上三角），松弛类预条件子由分裂 $\mathbf A=\mathbf M-\mathbf N$ 的 $\mathbf M$ 给出：

| 方法                     | $\mathbf M$                      | 特点                                                                           |
| ---------------------- | -------------------------------- | ---------------------------------------------------------------------------- |
| Richardson             | $\omega^{-1}\mathbf I$           | 最简单的一阶格式，$\omega$ 需按谱区间选取；SPD 时最优 $\omega=2/(\lambda_{\min}+\lambda_{\max})$ |
| Jacobi                 | $\mathbf D$                      | 各分量可同时更新，天然并行；阻尼 Jacobi 取 $\mathbf M=\omega^{-1}\mathbf D$                   |
| Gauss-Seidel           | $\mathbf D-\mathbf L$            | 用已更新分量，串行依赖；对一致排序矩阵收敛率约为 Jacobi 的平方                                          |
| SOR                    | $\omega^{-1}\mathbf D-\mathbf L$ | Gauss-Seidel 的超松弛，$\omega$ 取最优时收敛阶显著改善，但最优 $\omega$ 依赖谱信息                    |
| 对称 Gauss-Seidel / SSOR | 前向一遍加后向一遍                        | 得到对称的 $\mathbf M$，可作 SPD 问题的预条件子                                             |
| 块 Jacobi               | $\mathbf A$ 的对角块                 | 块内精确或近似求逆，块间并行                                                               |

**效果取决于什么。** 对二阶椭圆问题的有限元离散，网格尺寸 $h$ 减小时 $\rho(\mathbf G)$ 趋近于 1：Jacobi 与 Gauss-Seidel 为 $1-O(h^2)$，最优 SOR 为 $1-O(h)$，相应迭代次数为 $O(h^{-2})$ 与 $O(h^{-1})$，在 $d$ 维中即 $O(n^{2/d})$ 与 $O(n^{1/d})$。但对 $\mathbf G$ 的特征分解，对应高频（振荡）特征向量的特征值远小于 1：少数几步迭代就能把误差中的高频分量压掉，剩下的是在当前网格上光滑的低频分量。这一光滑性质是它们作多重网格光滑子的基础（§3.4.1）。

**使用要点。**

- 迭代次数随自由度数增长，因此不再作独立求解器，只在小规模或强对角占优问题中单独使用；今天主要作 Krylov 的廉价预条件子（Jacobi 即对角缩放，另有 SSOR、块 Jacobi）与多重网格的光滑子（阻尼 Jacobi、Gauss-Seidel，并行环境下常用 Chebyshev 或多色 Gauss-Seidel）。
- 作定常迭代时，Jacobi 与 Gauss-Seidel 对严格对角占优或 SPD 矩阵收敛；SOR 对 SPD 矩阵在 $0<\omega<2$ 时收敛。
- Gauss-Seidel 的串行依赖在并行中通过红黑排序或多色排序解除，代价是收敛率略降。

### 3.2 不完全分解

**它做什么。** 在稀疏 LU / Cholesky 分解中按填充层级（ILU(k)、IC(k)）或数值阈值（ILUT）丢弃部分填充，得到稀疏的近似因子，预条件子的作用即一次前代加一次回代。

**使用要点。 **

- 需要显式稀疏矩阵及其稀疏结构，不适用于不显式组装全局矩阵的算子表示。
- ILU 不对称，只能配 GMRES 等；SPD 问题用 IC 才能配 PCG。
- 前代回代串行本质强，并行时须按分区做块 ILU，收敛随分区数增加而退化。
- 矩阵变化后须重新做不完全分解，在矩阵频繁变化的场景中代价偏高（§3.6）。

### 3.3 多项式预条件

**它做什么。** 取 $\mathbf B=q(\mathbf A)$ 为 $\mathbf A$ 的低次多项式，常用 Chebyshev 多项式在谱区间上近似 $\mathbf A^{-1}$（§2.2）。

**使用要点。** 只需算子作用与谱区间估计，不需要矩阵元素，也没有前代回代那样的串行依赖，适合不显式组装矩阵的算子表示与 GPU。效果取决于谱区间估计的准确程度。对 SPD 矩阵，$q$ 在 $\mathbf A$ 的全部特征值上取正值时 $q(\mathbf A)$ 为 SPD，可以配 PCG；谱区间估计偏差较大时这一点不再有保证。

### 3.4 多重网格

多重网格在由细到粗的一系列层次上分工消去误差：光滑子消去高频分量，粗层校正消去低频分量，对椭圆问题可达 $O(n)$ 的最优复杂度。

多重网格按层次从哪里来分为以下几种：

| 种类                    | 层次从哪里来                           | 需要的信息                  | 适用                           | 典型实现                           |
| --------------------- | -------------------------------- | ---------------------- | ---------------------------- | ------------------------------ |
| GMG（h-多重网格）           | 网格逐级粗化                           | 网格层次与层间转移算子，不需要矩阵元素    | 结构化或可嵌套加密的网格                 | deal.II、MFEM 的 GMG             |
| p-多重网格                | 同一网格上逐级降低多项式次数，最低一层常再接 GMG 或 AMG | 各次数的单元空间               | 高阶有限元                        | deal.II、MFEM                   |
| 经典 AMG（Ruge–Stüben 型） | 按矩阵元素的连接强度挑选粗点                   | 显式稀疏矩阵                 | 非结构网格上的标量椭圆问题；弹性问题需按位移分量分块处理 | HYPRE BoomerAMG                |
| 光滑聚合 AMG              | 把相邻未知量聚合成粗未知量，再对插值做光滑            | 显式稀疏矩阵与近核信息（弹性问题为刚体模态） | 非结构网格上的弹性等向量问题               | Trilinos ML / MueLu、PETSc GAMG |

表中两类 AMG 的区分与实现对应为本页按 Xu–Zikatanov [12] 等整理，未对照原文核对。种类之外，还有两个在任一种多重网格上都可以选择的用法选项：

- **循环方式**：V-cycle 每层递归一次，W-cycle 每层递归两次，F-cycle 介于二者之间；全多重网格（Full Multigrid, FMG）从最粗层起逐层给出初值，一次扫过即可达到离散精度。
- **层间组合**：标准的乘性方式，或 Bramble–Pasciak–Xu（BPX）预条件子一类的加性方式（§3.4.3）。

#### 3.4.1 原理与 V-cycle

松弛类对二阶椭圆问题的 $\rho(\mathbf G)$ 随网格加密趋近于 1，但对应高频特征向量的特征值远小于 1（§3.1）：少数几步就能把误差中的振荡分量压掉，剩下的是在当前网格上光滑的低频分量。光滑的误差可以在更粗的网格上精确表示，而在粗网格上它们的相对频率翻倍，又变成光滑子能高效处理的对象。两个网格层间的转移由限制算子 $\mathbf R$（细到粗）与延拓算子 $\mathbf P$（粗到细）完成，常取 $\mathbf R=\mathbf P^{\mathsf T}$。

一次两层校正扩展为多层递归即 V-cycle：

1. 细网格前光滑：做 $\nu_1$ 步松弛（阻尼 Jacobi、Gauss-Seidel、Chebyshev 等）；
2. 计算残差并限制到粗网格：$\mathbf r_H=\mathbf R\,(\mathbf b-\mathbf A\mathbf x)$；
3. 粗网格求解 $\mathbf A_H\mathbf e_H=\mathbf r_H$，递归调用本过程，或在最粗层用[[direct-methods|直接法]]求解；
4. 延拓并校正：$\mathbf x\leftarrow\mathbf x+\mathbf P\mathbf e_H$；
5. 细网格后光滑 $\nu_2$ 步。

对椭圆问题，V-cycle 每次的误差压缩因子与 $h$ 无关，总运算量为 $O(n)$。

#### 3.4.2 各种类的要点

- **GMG**：粗层算子可用 Galerkin 方式 $\mathbf A_H=\mathbf P^{\mathsf T}\mathbf A\mathbf P$ 得到，也可在粗网格上重新离散。Galerkin 粗算子自动继承细层的系数分布，重新离散则要在粗层上另行处理系数；系数随位置剧烈变化时（如 SIMP 拓扑优化）通常取 Galerkin 方式（本页整理）。
- **p-多重网格**：各层网格相同，只降低多项式次数；最低次一层是低阶问题，再交给 GMG 或 AMG。这正是 §3 所说"构造在代理算子上"的一种做法。
- **AMG**：只需矩阵元素，可作黑盒使用；经典 AMG 按连接强度挑选粗点，光滑聚合 AMG 先聚合再光滑插值。弹性问题须把刚体模态作为近核（near-nullspace）信息提供给粗化，否则粗空间无法表示零能模式，收敛显著退化。粗化与 Galerkin 粗算子的 setup 代价较高，矩阵变化后通常须重建（§3.6）。

#### 3.4.3 乘性与加性多层预条件子

标准 V-cycle 是**乘性**（multiplicative）的：各层依次处理，每层把前光滑后更新过的残差交给下一层，每层每次循环要作用若干次 $\mathbf A_l$。按子空间校正框架（Xu [10]），另一类是**加性**（additive）的：各层同时作用于同一个残差的限制，

$$
\mathbf B_{\mathrm{add}}=\sum_{l=1}^{L-1}\hat{\mathbf P}_l\,\mathbf S_l\,\hat{\mathbf P}_l^{\mathsf T}+\hat{\mathbf P}_L\,\mathbf A_L^{-1}\hat{\mathbf P}_L^{\mathsf T},
$$

其中 $\hat{\mathbf P}_l$ 是从第 $l$ 层到最细层的复合延拓（$\hat{\mathbf P}_1=\mathbf I$），$\mathbf S_l$ 是第 $l$ 层的 SPD 光滑或缩放算子。BPX 预条件子 [11] 是这一类的代表。

| | 乘性（标准 V-cycle） | 加性 |
|---|---|---|
| SPD 条件 | 需满足 §3.4.4 的光滑子收敛条件 | 各 $\mathbf S_l$ 为 SPD 即可 |
| 每次作用的算子乘法 | 各层都要作用 $\mathbf A_l$（残差更新与后光滑） | 循环内不作用 $\mathbf A_l$，只需各层对角（若 $\mathbf S_l$ 为对角缩放）与最粗层分解 |
| 并行性 | 层间串行 | 各层相互独立，可并行 |
| 收敛 | 预条件后谱更集中，迭代次数少 | 谱较分散，迭代次数通常更多；单独作为迭代法须加阻尼，一般只作预条件子 |

两者的取舍取决于"迭代次数增加的倍数"与"单步代价下降的倍数"之比。例如 Wang2025 的"对角松弛"V-cycle 在除最粗层外的每一层只做对角缩放、不更新残差，展开后正是 $\mathbf S_l=2w\,\mathbf D_l^{-1}$ 的加性形式（本页推导，原文未如此命名）；原文报告它的迭代次数多于标准 V-cycle，但总耗时最短、内存最低，并给出"迭代次数增长不超过 2 倍即有净收益"的判据（[[../../literature/topopt/matrix-free/translations/Wang2025-top3d-xl-matrix-free-matlab-zh#4.2 多重网格预条件子|Wang2025 4.2 节]]、[[../../literature/topopt/matrix-free/translations/Wang2025-top3d-xl-matrix-free-matlab-zh#7 结果|第 7 节]]）。

#### 3.4.4 使用

**作为求解器还是作为预条件子。** 多重网格作为独立求解器时对光滑子、粗化策略、边界处理与系数跳跃都比较敏感，个别分量收敛慢会拖累整体。作为 Krylov 的预条件子时，一次 V-cycle 就是一次 $\mathbf B$ 作用：SPD 问题配 CG 即 MGCG，一般问题配 GMRES。Krylov 外层能吸收多重网格未能消去的少数分量，鲁棒性与效率通常都优于两者单独使用。满足相应光滑与粗空间逼近条件时，多重网格预条件可使 $\mathbf B\mathbf A$ 的谱条件数与网格尺寸无关，MGCG 在固定误差容限下的迭代次数不随网格加密持续增长，未预条件 CG 则按 $O(h^{-1})$ 增长（§2.3.1）（Trottenberg 等 [5]）。

**作 PCG 预条件子的条件。** PCG 要求预条件子是固定的 SPD 线性算子（§3）。把一次 V-cycle 记为映射 $\mathbf r\mapsto\mathbf z=\mathbf B\mathbf r$，记前光滑为 $\mathbf x\leftarrow\mathbf x+\mathbf S(\mathbf b-\mathbf A\mathbf x)$，要满足这一要求需同时做到：

| 要求 | 做法 | 不满足时 |
|---|---|---|
| 线性且固定 | 每次从 $\mathbf z=\mathbf 0$ 出发，做固定次数的循环（通常一次） | 非零初值使映射成为仿射映射；最粗层迭代求解按容差停止、或内层按残差判停，都使映射随 $\mathbf r$ 变化，须用 FCG（§3.7） |
| 对称 | $\mathbf R=\mathbf P^{\mathsf T}$；后光滑取前光滑的伴随 $\mathbf S^{\mathsf T}$（阻尼 Jacobi 前后步数相同即可，Gauss-Seidel 后光滑须反向扫描）；粗层算子对称，Galerkin 形式 $\mathbf A_H=\mathbf P^{\mathsf T}\mathbf A\mathbf P$ 自动满足 | 改用 GMRES，或换成对称的光滑与转移 |
| 正定 | 每层光滑子在 $\mathbf A$ 范数下收敛，$\lVert\mathbf I-\mathbf S\mathbf A\rVert_{\mathbf A}<1$，阻尼 Jacobi 即 $0<\omega<2/\lambda_{\max}(\mathbf D^{-1}\mathbf A)$；最粗层精确求解，或用满足 $\sigma(\mathbf B_H\mathbf A_H)\subset(0,1]$ 的固定 SPD 近似（如固定步数的内层对称 V-cycle） | $\mathbf B$ 可能不定，PCG 中 $\mathbf r^{\mathsf T}\mathbf z$ 可能非正而中断 |

满足这三项时，误差传播算子 $\mathbf E=\mathbf I-\mathbf B\mathbf A$ 是 $\mathbf A$-自伴半正定的，且 $\lVert\mathbf E\rVert_{\mathbf A}<1$，因此 $\sigma(\mathbf B\mathbf A)\subset(0,1]$，$\mathbf B$ 为 SPD（Xu–Zikatanov [12]）。

**Krylov 外层为何更稳健。** 由上，作为独立求解器的收敛因子是 $\lVert\mathbf E\rVert_{\mathbf A}=1-\lambda_{\min}(\mathbf B\mathbf A)$，由最难消去的那个误差分量决定。系数高对比度（例如材料与近空区域的刚度相差多个数量级）或几何细节在粗网格上无法表示时，常见的情形是只有少数误差分量被光滑与粗校正同时漏掉。这时 $\mathbf B\mathbf A$ 有少数几个接近 0 的离群特征值，其余特征值聚集在 $[a,1]$ 内。若有 $m$ 个这样的离群特征值，可构造一个在这些点取零的 $m$ 次误差多项式，再用剩余次数压低 $[a,1]$ 内的误差；由此可解释 CG 在付出约 $m$ 步的额外代价后，后续收敛率主要由有效条件数 $1/a$ 控制，而误差界的前因子仍受离群值位置影响。独立的 V-cycle 迭代则一直受最差分量拖累（本段为本页推导）。

拓扑优化中 MGCG 自 Amir 等（2014）起被广泛采用；Wang2025 观察到，密度场非均质性更强的多孔填充优化需要明显更多的 MGCG 迭代（[[../../literature/topopt/matrix-free/translations/Wang2025-top3d-xl-matrix-free-matlab-zh#7 结果|Wang2025 第 7 节]]）。

### 3.5 区域分解

区域分解按子域构造 $\mathbf B$：每个子域上求解（或近似求解）局部问题，再把局部修正组合起来。各子域同时作用于同一残差即加性 Schwarz，依次作用即乘性 Schwarz，二者与 §3.4.3 的加性 / 乘性多层预条件子同属子空间校正框架（Xu [10]）。它与并行分区天然匹配；只用子域局部求解的一层 Schwarz，收敛随子域数增加而退化，加入粗空间后才可扩展。非重叠子结构把问题化为界面上的 Schur 补方程，可直接分解求解（见 [[../substructure/exact-substructural]]），也可在界面上用 Krylov 方法迭代求解，本页不展开。

### 3.6 代价核算

预条件的代价分四部分，性能报告须分别注明：

- **setup**：首次构造 $\mathbf B$ 的成本，ILU 与 AMG 的 setup 可能与若干次求解相当；
- **apply**：每步 Krylov 迭代作用一次 $\mathbf B$ 的成本，需与算子作用同量级比较；
- **update**：矩阵变化后（例如拓扑优化中每次材料分布更新）须重做的那部分 setup，须区分可复用的结构与须重算的数值数据：GMG 的网格层次与转移算子 $\mathbf P$ 不变，只需重算各层对角与 Galerkin 粗算子 $\mathbf P^{\mathsf T}\mathbf A\mathbf P$、重新分解最粗层；AMG 的粗化由矩阵元素驱动，通常须整体重建；
- **内存**：$\mathbf B$ 常驻的存储，例如 GMG 各层粗算子与最粗层分解因子、ILU 的不完全因子，应与算子表示本身的内存一并比较。

依次求解 $N_{\mathrm{sys}}$ 个矩阵各不相同的系统（例如拓扑优化中每个设计迭代一个）时，求解总耗时可写为

$$
T_{\text{总}}=T_{\text{setup}}+(N_{\mathrm{sys}}-1)\,T_{\text{update}}+\sum_{j=1}^{N_{\mathrm{sys}}}N_{\text{iter}}^{(j)}\big(T_{\mathbf A}+T_{\mathbf B}+T_{\text{vec}}\big),
$$

其中 $T_{\mathbf A}$ 为一次算子作用，取决于算子表示（[[../matrix-free/assembly-levels|装配层次]]）；$T_{\mathbf B}$ 为一次 apply；$T_{\text{vec}}$ 为每步的向量运算，PCG 每步 2 次内积与 3 次 AXPY。$T_{\text{vec}}$ 常被忽略，但在不显式组装矩阵的实现中，算子作用每个自由度的访存量已显著降低，向量运算的占比随之上升（本页判断，待实测确认）；并行时内积还带来全局同步（§2.3.4）。$N_{\text{iter}}^{(j)}$ 由 $\mathbf B\mathbf A$ 的特征值分布、初值与判停准则共同决定（§3 开头、§2.4），不只取决于条件数。上式为本页整理。

按上式比较，一个预条件子值得用，当且仅当减少的迭代所省下的 $T_{\mathbf A}+T_{\text{vec}}$，超过它增加的 setup、update 与 $\sum_j N_{\text{iter}}^{(j)}T_{\mathbf B}$；内存不足时还须先满足内存约束。矩阵频繁变化的场景中 update 成本往往主导取舍：粗化与 Galerkin 粗算子需要逐次重建的 AMG、高阶 ILU 在这类场景中代价偏高，网格层次固定、只需按新系数重算粗算子的 GMG 更容易摊薄（各类别的更新代价见 §3 开头的表）。

**拓扑优化中的 update。** 一次优化的设计迭代通常在百次量级，update 要付出同样多次。以上一设计迭代的位移作初值（热启动），且判停以 $\lVert\mathbf b\rVert$ 为参照时（§2.4），优化后期设计变化变小，$N_{\text{iter}}^{(j)}$ 随之下降，而 $T_{\text{update}}$ 不随之减小，它在总耗时中的占比上升。因此 GMG 在拓扑优化中是否划算，除迭代次数外还取决于逐轮 update 的成本（本段为本页推导）。

### 3.7 预条件子与外层方法的结合

**作用位置。** 按作用位置，预条件可分为左、右及分裂三种形式。左预条件求解 $\mathbf M^{-1}\mathbf A\mathbf x=\mathbf M^{-1}\mathbf b$，该系统的残差为 $\mathbf M^{-1}\mathbf r$；右预条件求解 $\mathbf A\mathbf M^{-1}\mathbf y=\mathbf b$，再由 $\mathbf x=\mathbf M^{-1}\mathbf y$ 恢复解，该系统的残差就是原方程的真残差 $\mathbf r=\mathbf b-\mathbf A\mathbf x$。分裂预条件将 $\mathbf M=\mathbf M_1\mathbf M_2$ 的两部分分别作用在左右两侧，求解 $\mathbf M_1^{-1}\mathbf A\mathbf M_2^{-1}\mathbf y=\mathbf M_1^{-1}\mathbf b$，再取 $\mathbf x=\mathbf M_2^{-1}\mathbf y$。左预条件 GMRES 极小化的是预条件后的残差范数，右预条件 GMRES 极小化的是真残差范数；这一极小化性质不能推广到所有迭代方法。判停时监测哪一种残差见 §2.4。

**PCG。** CG 加一个固定的 SPD 预条件子 $\mathbf M$，等价于在 $\mathbf M$ 内积下对预条件后的系统做 CG。每步多一次 $\mathbf z=\mathbf M^{-1}\mathbf r$ 的作用，§2.3.1 第 2、4 步中的 $\mathbf r^{\mathsf T}\mathbf r$ 换成 $\mathbf r^{\mathsf T}\mathbf z$，新方向取 $\mathbf p_{k+1}=\mathbf z_{k+1}+\beta_k\mathbf p_k$，收敛由 $\mathbf M^{-1}\mathbf A$ 的谱决定。判停可用自然范数 $\sqrt{\mathbf r^{\mathsf T}\mathbf z}$，不增加内积（§2.4）。$\mathbf M$ 必须对称正定且每步不变，每步变化时改用 FCG。Jacobi-PCG、MGCG 等都是 PCG 配不同预条件子的结果。

**FCG。** 若预条件子的作用每步不同，例如内层再套一个按容差停止的迭代求解器，它就不再是固定的线性算子。PCG 的短递推依赖预条件子固定，此时搜索方向之间的 $\mathbf A$-共轭性会丢失，收敛可能停滞。FCG 有两种做法：把方向更新系数改为 Polak–Ribière 形式 $\beta_j=\mathbf z_{j+1}^{\mathsf T}(\mathbf r_{j+1}-\mathbf r_j)/(\mathbf z_j^{\mathsf T}\mathbf r_j)$（Golub–Ye [14]），或让新方向对最近若干个方向显式做 $\mathbf A$-正交化（Notay [13] 的截断 FCG）。多重网格作预条件子时怎样保证固定、对称、正定，见 §3.4.4；满足这些条件就只需 PCG，不需要 FCG。

## 参考依据

- [1] SAAD Y. Iterative Methods for Sparse Linear Systems[M]. 2nd ed. Philadelphia: SIAM, 2003 — §4 定常迭代、分裂与收敛定理（§2.1、§3.1）；§5 投影方法的 Galerkin 与 Petrov–Galerkin 条件（§2.3 引言）；§6.1 Krylov 子空间与投影；§6.3 Arnoldi 过程；§6.5 GMRES、Givens 旋转增量求解与重启；§6.6 对称 Lanczos 过程；§6.7 CG 及其收敛界；§6.11 收敛分析（含非对称情形对特征向量矩阵条件数的依赖）、CG 的并行实现与内积归约；§7.4 BiCGSTAB、TFQMR 等免转置变体（§2.3.1–§2.3.4 算法表与收敛说明，章节号未逐一核对原书）；§9 预条件迭代与 §9.4 Flexible GMRES（§2.3.3、§3）；§10 预条件技术（ILU、块预条件，§3.2）；§12.3 多项式预条件与 Chebyshev 加速（§2.2、§3.3）；§13 多重网格方法（§3.4）；§14 区域分解（§3.5）。未入库文献。
- [2] VARGA R S. Matrix Iterative Analysis[M]. 2nd ed. Berlin: Springer, 2000 — 正则分裂、SOR 最优松弛因子理论（§3.1）。未入库文献。
- [3] TREFETHEN L N, BAU D. Numerical Linear Algebra[M]. Philadelphia: SIAM, 1997 — Lecture 32、35、38 关于 Krylov 方法作为多项式逼近的观点与 CG 收敛界（§2.2、§2.3.1）。未入库文献。
- [4] BRIGGS W L, HENSON V E, MCCORMICK S F. A Multigrid Tutorial[M]. 2nd ed. Philadelphia: SIAM, 2000 — 松弛的光滑性质（§3.1）、粗网格校正、V/W/F-cycle 与 AMG 基础（§3.4.1–§3.4.2）。未入库文献。
- [5] TROTTENBERG U, OOSTERLEE C W, SCHÜLLER A. Multigrid[M]. London: Academic Press, 2001 — 多重网格收敛理论与算法设计（§3.4）；多重网格预条件后条件数与网格无关（§3.4.4）。未入库文献。
- [6] BENZI M. Preconditioning techniques for large linear systems: a survey[J]. Journal of Computational Physics, 2002, 182(2): 418-477 — 预条件技术综述（§3）。未入库文献。
- [7] WATHEN A J. Preconditioning[J]. Acta Numerica, 2015, 24: 329-376 — 谱聚集而非条件数作为预条件目标的论述（§3）。未入库文献。
- [8] KRONBICHLER M, KORMANN K. A generic interface for parallel cell-based finite element operator application[J]. Computers & Fluids, 2012, 63: 135-147 — 只需算子作用接口的 Krylov 求解与单元级算子按需作用的结合路径（§2.3）。cite key `kronbichlerGenericInterfaceParallel2012`。
- [9] GHYSELS P, VANROOSE W. Hiding global synchronization latency in the preconditioned Conjugate Gradient algorithm[J]. Parallel Computing, 2014, 40(7): 224-238 — pipelined CG 及其与标准 CG 数值行为的差异（§2.3.4）。未入库文献。
- [10] XU J. Iterative methods by space decomposition and subspace correction[J]. SIAM Review, 1992, 34(4): 581-613. DOI: 10.1137/1034116 — 乘性与加性子空间校正框架，涵盖多层方法与区域分解（§3.4.3、§3.5）。未入库文献，出版信息经 CrossRef 核对。
- [11] BRAMBLE J H, PASCIAK J E, XU J. Parallel multilevel preconditioners[J]. Mathematics of Computation, 1990, 55(191): 1-22. DOI: 10.1090/S0025-5718-1990-1023042-6 — BPX 加性多层预条件子（§3.4.3）。未入库文献，出版信息经 CrossRef 核对。
- [12] XU J, ZIKATANOV L. Algebraic multigrid methods[J]. Acta Numerica, 2017, 26: 591-721. DOI: 10.1017/S0962492917000083 — 对称 V-cycle 的误差传播算子与作为 SPD 预条件子的条件（§3.4.4）；经典 AMG 与光滑聚合 AMG 的区分（§3.4）。未入库文献，出版信息经 CrossRef 核对；§3.4.4 的结论与 §3.4 两类 AMG 的区分及实现对应未逐条对照原文。
- [13] NOTAY Y. Flexible conjugate gradients[J]. SIAM Journal on Scientific Computing, 2000, 22(4): 1444-1460. DOI: 10.1137/S1064827599362314 — 变预条件下的截断 FCG（§3.7）。未入库文献，出版信息经 CrossRef 核对。
- [14] GOLUB G H, YE Q. Inexact preconditioned conjugate gradient method with inner-outer iteration[J]. SIAM Journal on Scientific Computing, 1999, 21(4): 1305-1320. DOI: 10.1137/S1064827597323415 — 非精确内层预条件下的 PCG 变体（§3.7）。未入库文献，出版信息经 CrossRef 核对；Polak–Ribière 形式 $\beta_j$ 的归属待对照原文确认。
- [15] [[../../literature/topopt/matrix-free/translations/Wang2025-top3d-xl-matrix-free-matlab-zh|Wang2025 译文]]（citekey `Wang2025-top3d-xl-matrix-free-matlab`）— 拓扑优化中的 MGCG（算法 1、2）、对角松弛的作用范围与非二进 V 循环、非均质性对迭代次数的影响（§3.4.3、§3.4.4）；其中 MGCG 自 Amir 等（2014）起被广泛采用的说法经该文转引，Amir 等（2014）未入库。
- [16] PAIGE C C, SAUNDERS M A. Solution of sparse indefinite systems of linear equations[J]. SIAM Journal on Numerical Analysis, 1975, 12(4): 617-629. DOI: 10.1137/0712047 — MINRES 的 Lanczos 递推与 Givens 旋转求解、SYMMLQ 极小化误差 2-范数（§2.3.2）。未入库文献，出版信息经 CrossRef 核对。
- [17] ELMAN H, SILVESTER D, WATHEN A. Finite Elements and Fast Iterative Solvers: with Applications in Incompressible Fluid Dynamics[M]. 2nd ed. Oxford: Oxford University Press, 2014. DOI: 10.1093/acprof:oso/9780199678792.001.0001 — 鞍点系统的 MINRES 与 SPD 块对角预条件（§2.3.2）。未入库文献，出版信息经 CrossRef 核对；所支撑结论的原书章节未核对。
- [18] FABER V, MANTEUFFEL T. Necessary and sufficient conditions for the existence of a conjugate gradient method[J]. SIAM Journal on Numerical Analysis, 1984, 21(2): 352-362. DOI: 10.1137/0721026 — 短递推与每步最优不可兼得的条件（§2.3.3）。未入库文献，出版信息经 CrossRef 核对；正文对定理条件的表述为概括，未逐条对照原文。
- [19] SHEWCHUK J R. An Introduction to the Conjugate Gradient Method Without the Agonizing Pain[R]. Pittsburgh: Carnegie Mellon University, 1994. Technical Report CMU-CS-94-125 — 二次型极小化视角下的最速下降之字形与共轭方向（§2.3.1）。未入库文献；技术报告无 DOI，出版信息凭记忆填写，未经核对。
