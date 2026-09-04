---
title: "Krylov 子空间方法"
type: concept
aliases:
  - Krylov Subspace Methods
  - Krylov 迭代法
  - 预条件 Krylov 求解器
  - Conjugate Gradient
  - 共轭梯度法
  - GMRES
  - MINRES
tags:
  - numerical-algebra
  - linear-solver
  - krylov
  - parallel-reduction
status: draft
date_added: 2026-09-03
date_update: 2026-09-03
---

# Krylov 子空间方法

> Krylov 方法在由初始残差与算子反复作用张成的子空间 $\mathcal K_k(\mathbf A,\mathbf r_0)$ 中按投影或极小残差取近似解，每一步都在更大的子空间里取最优，因而不像定常迭代那样被固定算子的谱半径锁死；运行中只需要算子作用接口 $\mathbf y=\mathbf A\mathbf x$。并行下它唯一必须全局同步的运算是内积。

## 1. 子空间与投影

设初始解为 $\mathbf x_0$，初始残差为 $\mathbf r_0=\mathbf b-\mathbf A\mathbf x_0$。第 $k$ 阶 Krylov 子空间是

$$
\mathcal K_k(\mathbf A,\mathbf r_0)=\operatorname{span}\left\{\mathbf r_0,\ \mathbf A\mathbf r_0,\ \mathbf A^2\mathbf r_0,\ \dots,\ \mathbf A^{k-1}\mathbf r_0\right\}.
$$

Krylov 方法在仿射空间 $\mathbf x_0+\mathcal K_k$ 中取近似解 $\mathbf x_k$，取法有两类：Galerkin 投影要求残差与 $\mathcal K_k$ 正交（CG、FOM），极小残差要求 $\lVert\mathbf b-\mathbf A\mathbf x_k\rVert_2$ 在子空间内最小（MINRES、GMRES）。两类都把 $n$ 维问题化为 $k$ 维子空间上的小规模代数问题，通常 $k\ll n$。子空间的正交基由 Lanczos 过程（对称）或 Arnoldi 过程（一般）逐步生成，前者三项递推，后者需要对全部已有基向量正交化。

## 2. 与定常迭代的区别

[[stationary-iterations|定常迭代]]每步用同一个 $\mathbf G$，$\mathbf e_k=\mathbf G^k\mathbf e_0$，收敛率被 $\rho(\mathbf G)$ 锁死。Krylov 方法的残差可写成 $\mathbf r_k=p_k(\mathbf A)\mathbf r_0$，其中 $p_k$ 是满足 $p_k(0)=1$ 的 $k$ 次多项式，方法在每一步自动选出使 $\mathbf r_k$（或误差的某个范数）最小的 $p_k$，等价于按 $\mathbf A$ 的谱自适应地调整每步的有效算子。

对 SPD 矩阵，CG 的能量范数误差满足

$$
\lVert\mathbf e_k\rVert_{\mathbf A}\le 2\left(\frac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}\right)^{k}\lVert\mathbf e_0\rVert_{\mathbf A},\qquad \kappa=\kappa_2(\mathbf A),
$$

迭代次数随 $\sqrt\kappa$ 而非 $\kappa$ 增长；这一界只用到谱区间，特征值聚集在少数几簇时实际收敛远快于该上界，这也是[[preconditioning|预条件]]的目标。精确算术下 CG 至多 $n$ 步终止，实践中有限精度使正交性丢失，终止性质不可依赖。

## 3. 按矩阵性质分族

| 矩阵性质 | 方法 | 递推与存储 |
|---|---|---|
| 对称正定 | CG，预条件版本 PCG | 基于 Lanczos 过程，短递推，只保留前一步向量，存储与每步计算量最小 |
| 对称不定 | MINRES、SYMMLQ | 基于 Lanczos 过程，短递推，MINRES 保证残差单调 |
| 非对称 / 一般 | GMRES、BiCGSTAB、TFQMR | GMRES 基于 Arnoldi 过程，残差单调极小但长递推须保存全部基向量，实践中定期重启 GMRES(m)；BiCGSTAB 用双正交化换回短递推，代价是残差不再单调 |

对称性决定能否使用短递推，正定性决定能否使用 CG，这两条是选择方法的第一判据。预条件后的对称性同样要看：SPD 问题用非对称预条件子（如单向 Gauss-Seidel）后不能再用 CG，须改用 GMRES 或换对称预条件子；预条件子随迭代变化时须用 Flexible GMRES（FGMRES）一类允许变预条件的变体。

## 4. 只需算子作用接口

Krylov 方法运行过程中只调用 $\mathbf y=\mathbf A\mathbf x$，不读取 $\mathbf A$ 的元素。这使它成为各种不显式组装全局矩阵的算子表示的自然外层：算子可以是单元级按需作用、子结构缩聚算子或任何线性映射。这一性质对求解器成立，对预条件子不成立，各装配层级还能提供哪些代数信息由 [[../matrix-free/assembly-levels#3. 三条跨层级不变量]] 不变量 3 维护。

## 5. 并行执行中的同步点

Krylov 迭代的每一步由三类运算组成：算子作用 $\mathbf A\mathbf p$、向量更新 AXPY、内积。前两类在分区之间没有依赖（算子作用只在界面上需要交换数据，且可以与内部单元的计算重叠），唯一必须让全部执行实体同步的是内积。

- **每步归约次数**：CG 每次迭代需要 2 次内积（$\mathbf r^{\mathsf T}\mathbf r$ 与 $\mathbf p^{\mathsf T}\mathbf A\mathbf p$），PCG 同样是 2 次（$\mathbf r^{\mathsf T}\mathbf z$ 与 $\mathbf p^{\mathsf T}\mathbf A\mathbf p$）；GMRES 的 Arnoldi 正交化每步归约次数随重启维数 $m$ 增长，代价更高。
- **在各并行层的形态**：进程级是一次 `MPI_Allreduce` 全局同步，设备内是 block reduction 加一次设备级归约，线程级是共享内存归约。进程级是唯一会阻塞全部 rank 的那一种，它必须等所有 rank 到齐才能给出标量，因此强扩展曲线的拐点通常出现在内积而不是算子作用上。三层并行的完整卡点讨论见 [[../gpu-hpc/parallel-levels#3. 两个绕不开的断点]]。
- **共享自由度必须加权**：分区之间有共享自由度时，直接对各 rank 的局部内积求和会重复计数界面分量，必须使用按引用计数加权的内积，它精确等于串行内积，从而保证并行与串行的迭代序列逐点一致；定理与实现约定见 [[../gpu-hpc/distributed-operator-and-shared-dofs#4. 重叠加权内积与 Krylov 求解器收敛理论]]。
- **降低归约代价属于换算法**：s-step / communication-avoiding CG 与 pipelined CG 通过重组递推把多次归约合并或与算子作用重叠，但它们改变了浮点运算次序与数值稳定性，收敛行为需单独验证，不能视为同一算法的不同实现。

## 参考文献

[1] SAAD Y. Iterative Methods for Sparse Linear Systems[M]. 2nd ed. Philadelphia: SIAM, 2003. §6.1 Krylov 子空间与投影；§6.5–6.7 CG 及其收敛界；§6.11 CG 的并行实现与内积归约；§7.1 GMRES 与 Arnoldi 过程；§9.4 Flexible GMRES。**refs.bib 尚无条目。**
[2] TREFETHEN L N, BAU D. Numerical Linear Algebra[M]. Philadelphia: SIAM, 1997. Lecture 32、35、38 关于 Krylov 方法作为多项式逼近的观点与 CG 收敛界。**refs.bib 尚无条目。**
[3] KRONBICHLER M, KORMANN K. A generic interface for parallel cell-based finite element operator application[J]. Computers & Fluids, 2012, 63: 135-147. 只需算子作用接口的 Krylov 求解与单元级算子按需作用的结合路径。cite key `kronbichlerGenericInterfaceParallel2012`。
[4] GHYSELS P, VANROOSE W. Hiding global synchronization latency in the preconditioned Conjugate Gradient algorithm[J]. Parallel Computing, 2014, 40(7): 224-238. pipelined CG 及其与标准 CG 数值行为的差异。**refs.bib 尚无条目。**
