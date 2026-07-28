---
title: "分布式 Matrix-Free 算子：网格分区、共享自由度与 MPI 同步"
type: concept
aliases:
  - Distributed Matrix-Free Operator
  - MPI Domain Decomposition and Shared DOFs
  - 分布式无矩阵算子
tags:
  - matrix-free
  - finite-element
  - mpi
  - domain-decomposition
  - shared-dofs
  - krylov
status: in-progress
date_added: 2026-07-27
date_update: 2026-07-27
---

# 分布式 Matrix-Free 算子：网格分区、共享自由度与 MPI 同步

> **一句话**：MPI 有限元通常对单元做非重叠分区、对界面自由度保存共享或 ghost 副本；分布式 Matrix-Free 算子必须用严格一致的输入同步、局部作用、输出归约和加权内积，才能表示与串行全局算子相同的固定线性映射。

## 1. 单元非重叠不等于自由度不重叠

设有限元网格的单元集合为

$$
\mathcal T_h=\{K_1,\ldots,K_{N_c}\}.
$$

将其划分给 $P$ 个 MPI rank：

$$
\mathcal T_h
=
\bigcup_{r=0}^{P-1}\mathcal T_h^{(r)},
\qquad
\mathcal T_h^{(r)}\cap\mathcal T_h^{(s)}
=\varnothing
\quad(r\ne s).
\tag{1}
$$

式 (1) 表示每个单元只由一个 rank 负责。但是，相邻子区域需要共同描述分区界面上的有限元函数，所以界面节点、边或面自由度可能同时出现在多个 rank 的局部编号中。

以最低阶 Nedelec 元为例，自由度位于网格边上：

$$
u_e=\int_e \mathbf E\cdot\mathbf t_e\,\mathrm ds.
\tag{2}
$$

若边 $e$ 位于两个子区域的公共界面上，则两个 rank 都需要保存 $u_e$ 的局部副本。故应区分：

- **单元分区**：通常非重叠；
- **自由度表示**：在接口处可以重叠；
- **物理边界**：原连续问题的边界；
- **人工分区界面**：MPI 划分产生的内部界面，不是新的物理边界。

## 2. 限制算子与全局算子

设全局 true-DOF 向量为

$$
\mathbf u\in\mathbb C^N,
$$

rank $r$ 保存 $n_r$ 个局部自由度。用布尔限制矩阵

$$
\mathbf R_r\in\{0,1\}^{n_r\times N}
\tag{3}
$$

表示从全局 true DOF 到 rank-local DOF 的提取：

$$
\mathbf u_r=\mathbf R_r\mathbf u.
\tag{4}
$$

若 $\mathbf A_r$ 表示 rank $r$ 所负责单元产生的局部算子，则全局有限元算子为

$$
\mathbf A
=
\sum_{r=0}^{P-1}
\mathbf R_r^{\mathrm T}
\mathbf A_r
\mathbf R_r.
\tag{5}
$$

式 (5) 是分布式装配矩阵和分布式 Matrix-Free MatVec 的共同数学目标。区别只在于 $\mathbf A_r$ 以哪一种装配层级保存和执行：

- LA 保存 rank-local 稀疏矩阵；
- EA/EbE 保存单元稠密矩阵并逐单元作用；
- PA/QA 保存积分点或部分装配数据；
- UA/NONE 在 MatVec 中进一步即时生成数据。

装配层级的完整边界见 [[assembly-levels]]。

## 3. 自由度引用次数

定义全局引用次数向量

$$
\mathbf q
=
\sum_{r=0}^{P-1}
\mathbf R_r^{\mathrm T}\mathbf 1_r,
\tag{6}
$$

其中 $q_i$ 表示全局自由度 $i$ 被多少个 rank 保存。通常：

$$
q_i=
\begin{cases}
1,&i\text{ 是子区域内部自由度},\\
2\text{ 或更大},&i\text{ 是共享界面自由度}.
\end{cases}
\tag{7}
$$

记

$$
\mathbf Q=\operatorname{diag}(\mathbf q).
\tag{8}
$$

引用次数不是有限元方程中的物理系数，而是分布式数据表示产生的计数。它用于共享副本平均、加权内积和全局解收集。

## 4. 两类常见分布式表示

### 4.1 Owned/ghost 表示

每个全局自由度指定唯一 owner；其他 rank 只保存 ghost 副本。典型 MatVec 数据流为：

1. owner 向 ghost 执行 halo exchange；
2. 各 rank 完成本地算子作用；
3. ghost 贡献归约给 owner；
4. 必要时再把结果广播到 ghost。

这种表示明确区分 owned DOF 与 ghost DOF。**代表实现**包括 PETSc `DM/VecGhost`、DOLFINx `IndexMap`、deal.II distributed vector、MFEM `ParFiniteElementSpace` 和 NGSolve `ParallelDofs`；Firedrake 底层主要沿用 PETSc 的 owned/ghost 与 halo 机制。

### 4.2 重叠副本表示

所有相邻 rank 都保存共享自由度的对等副本，不预先指定哪个副本更“真实”。令

$$
\mathbf R=
\begin{bmatrix}
\mathbf R_0\\
\vdots\\
\mathbf R_{P-1}
\end{bmatrix},
\qquad
\mathbf x_{\mathrm{loc}}
=
\begin{bmatrix}
\mathbf x_0\\
\vdots\\
\mathbf x_{P-1}
\end{bmatrix}.
\tag{9}
$$

当共享副本可能不一致时，先恢复唯一的全局输入：

$$
\bar{\mathbf x}
=
\mathbf Q^{-1}
\mathbf R^{\mathrm T}
\mathbf x_{\mathrm{loc}},
\tag{10}
$$

再把它限制回各 rank：

$$
\widetilde{\mathbf x}_{\mathrm{loc}}
=
\mathbf R\bar{\mathbf x}.
\tag{11}
$$

式 (10) 对自由度 $i$ 的逐分量形式就是

$$
\bar x_i
=
\frac{1}{q_i}
\sum_{r:\,i\in\mathcal I_r}
x_i^{(r)}.
\tag{12}
$$

因此，共享输入上的“同步求和再除以引用次数”不是经验修补，而是把重叠副本投影回唯一 true-DOF 向量。

**当前实例**是 `xihe/matrix_free_3` 的分布式算子：输入使用 `sync_add(x) / refs` 恢复一致共享值，局部作用后再以 `sync_add(y)` 累加各 rank 的单元贡献。这里描述的是该算例当前实现，不表示 FEALPy 的全部分布式接口都采用对等重叠副本。

libCEED 未固定归入上述任一类：它把 MPI 的 `P` 层及跨设备通信交给宿主程序管理，最终采用 owned/ghost 还是其他重叠表示取决于调用它的应用。

## 5. 分布式 Matrix-Free MatVec

一次正确的重叠表示 MatVec 包含三个阶段。

### 5.1 输入同步

使用式 (10)-(12) 将所有共享副本同步为同一个输入值。若输入本来就是一致表示

$$
\mathbf x_{\mathrm{loc}}=\mathbf R\mathbf x,
\tag{13}
$$

则同步不会改变它，因为

$$
\mathbf Q^{-1}\mathbf R^{\mathrm T}\mathbf R\mathbf x
=\mathbf x.
\tag{14}
$$

### 5.2 局部作用

每个 rank 独立执行

$$
\mathbf z_r
=
\mathbf A_r\widetilde{\mathbf x}_r.
\tag{15}
$$

EA/EbE 情况下，$\mathbf A_r$ 本身又由该 rank 的单元作用组成：

$$
\mathbf A_r\widetilde{\mathbf x}_r
=
\sum_{K\in\mathcal T_h^{(r)}}
\mathbf G_{rK}^{\mathrm T}
\mathbf A_K
\mathbf G_{rK}
\widetilde{\mathbf x}_r,
\tag{16}
$$

其中 $\mathbf G_{rK}$ 是 rank-local DOF 到单元 DOF 的限制。

### 5.3 输出归约

全局输出为

$$
\mathbf y
=
\sum_{r=0}^{P-1}
\mathbf R_r^{\mathrm T}\mathbf z_r.
\tag{17}
$$

若后续算法仍使用重叠表示，则再形成

$$
\mathbf y_{\mathrm{loc}}
=
\mathbf R\mathbf y.
\tag{18}
$$

把三步合并，可将重叠表示上的分布式算子写为

$$
\mathcal A_{\mathrm{dist}}
=
\mathbf R\mathbf A\mathbf Q^{-1}\mathbf R^{\mathrm T}.
\tag{19}
$$

对任意一致输入 $\mathbf x_{\mathrm{loc}}=\mathbf R\mathbf x$，有

$$
\mathcal A_{\mathrm{dist}}\mathbf x_{\mathrm{loc}}
=
\mathbf R\mathbf A\mathbf x.
\tag{20}
$$

式 (20) 是并行 Matrix-Free 正确性的核心不变量：每个 rank 得到的局部结果必须是同一个串行全局结果的限制。

## 6. 为什么输入和输出的同步方式不同

输入代表同一个全局系数，因此共享副本应取唯一一致值，重叠表示中使用平均：

$$
\bar x_i=\frac{1}{q_i}\sum_r x_i^{(r)}.
\tag{21}
$$

输出代表不同子区域对全局方程的贡献，因此应求和：

$$
y_i=\sum_r y_i^{(r)}.
\tag{22}
$$

如果输入也直接求和而不除以 $q_i$，接口自由度会被人为放大；如果输出取平均，跨接口单元的物理贡献又会丢失。只有“输入一致化、局部作用、输出累加”与式 (5) 一致。

## 7. Krylov 内积与真实残差

共享自由度在重叠表示中出现多次，直接计算所有 rank-local 分量的平方和会重复计数。适合一致副本的加权内积为

$$
\langle\mathbf x,\mathbf y\rangle_{\mathrm{ov}}
=
\sum_{r=0}^{P-1}
\sum_{i\in\mathcal I_r}
\frac{\overline{x_i^{(r)}}y_i^{(r)}}{q_i}.
\tag{23}
$$

若 $\mathbf x_{\mathrm{loc}}=\mathbf R\mathbf x$ 且
$\mathbf y_{\mathrm{loc}}=\mathbf R\mathbf y$，则

$$
\langle\mathbf x_{\mathrm{loc}},
\mathbf y_{\mathrm{loc}}\rangle_{\mathrm{ov}}
=
\mathbf x^*\mathbf y.
\tag{24}
$$

因此 Krylov 正交化、停止准则和真实残差

$$
\mathbf r=\mathbf b-\mathbf A\mathbf x
\tag{25}
$$

必须使用与分布式表示一致的全局归约。只看某个 rank 的局部范数，或不除以引用次数，不能代表 true-DOF 残差。

## 8. 全局解收集

从重叠副本恢复 rank 0 上的唯一全局向量，可使用

$$
\mathbf u
=
\mathbf Q^{-1}
\sum_{r=0}^{P-1}
\mathbf R_r^{\mathrm T}\mathbf u_r.
\tag{26}
$$

如果所有副本一致，式 (26) 返回原全局值，而不会把具有 $q_i$ 个副本的接口值放大为 $q_i u_i$。

但应区分两种用途：

- **求解过程中的输出归约**使用求和，因为不同 rank 提供不同单元贡献；
- **求解结束后的解向量收集**使用平均，因为各 rank 保存的是同一个未知量的副本。

## 9. 人工分区界面不是 Dirichlet 边界

设原问题物理边界为 $\partial\Omega$，rank $r$ 的局部网格边界为

$$
\partial\Omega_r
=
(\partial\Omega_r\cap\partial\Omega)
\cup
\Gamma_r,
\tag{27}
$$

其中 $\Gamma_r$ 是人工分区界面。Dirichlet 条件只能施加到

$$
\partial\Omega_r\cap\partial\Omega,
\tag{28}
$$

不能把 $\Gamma_r$ 当作新的物理边界。否则原来的全局 PDE 会被错误地切成多个彼此独立的问题。

对 $H(\operatorname{curl})$、$H(\operatorname{div})$ 等协调有限元，还必须按对应的切向迹或法向迹识别边界自由度，而不是把任意边界点值直接写入局部向量。

## 10. 正确性验证不变量

分布式 Matrix-Free 实现至少应检查以下不变量。

| 层次 | 检查 | 数学目标 |
|---|---|---|
| 分区 | 单元非空、无重叠、完整覆盖 | 满足式 (1) |
| 编号 | 每个局部 DOF 可追溯到唯一 true DOF | $\mathbf R_r$ 定义正确 |
| 输入同步 | 一致输入经同步后不变 | 满足式 (14) |
| MatVec | 分布式作用与显式全局作用一致 | 满足式 (20) |
| 边界 | 人工接口不被施加物理 Dirichlet 条件 | 满足式 (27)-(28) |
| 内积 | 1 rank 与多 rank 的全局范数一致 | 满足式 (24) |
| 解收集 | 收集结果不重复计算共享未知量 | 满足式 (26) |
| 求解 | true residual 满足统一停止准则 | 满足式 (25) |
| 跨 rank | 固定问题的 1-rank 与 $P$-rank 解一致 | 分区不改变离散问题 |

需要特别区分：

- **MatVec 一致**证明分布式算子表示正确；
- **1-rank/$P$-rank 迭代向量一致**证明并行数据流和 Krylov 过程一致；
- **真实残差达标**才证明线性系统已经求解到目标精度；
- 两个 rank 数得到同一个未收敛解，不能代替求解收敛门禁。

## 11. 与装配层次和性能的关系

MPI 分区方式与 Matrix-Free 装配层级是两个相互正交的维度：

- 分区回答“哪些 rank 拥有哪些单元和自由度、如何通信”；
- 装配层级回答“每个 rank 为算子作用保存什么数据”。

因此可以存在：

- MPI + FA/TA；
- MPI + LA；
- MPI + EA/EbE；
- MPI + PA/QA；
- MPI + UA/NONE。

同样的式 (5) 可以由不同装配层级实现。通信正确性不自动保证计算核高效，单 rank MatVec 高效也不自动保证多 rank 可扩展。通信量、负载均衡、halo 大小、归约频率和计算/通信重叠属于 [[../gpu-hpc/_index|GPU/HPC]] 的性能研究范围。

## 12. MPI 标准、Python 绑定与有限元框架的职责边界

MPI 是进程间通信标准，规范 communicator、rank、点对点通信、集合通信、非阻塞通信和并行 I/O 等基础语义。规范本身不定义有限元网格分区、owned/ghost DOF、共享自由度、halo、Matrix-Free 或装配层级。MPI 的规范性来源是 [MPI Forum 官方标准](https://www.mpi-forum.org/docs/)；Python 程序通常通过 [mpi4py 官方教程](https://mpi4py.readthedocs.io/en/stable/tutorial.html)调用同一套 MPI 语义，而不是采用另一种并行模型。

因此，分布式有限元 Matrix-Free 可以分为三层：

1. **MPI 层**：提供进程、communicator 和消息/集合通信；
2. **分布式有限元层**：定义单元分区、true/local DOF、owner、ghost、限制/延拓和 halo；
3. **算子层**：决定局部算子采用 FA、LA、EA、PA 还是 UA，并实现 MatVec。

后两层由 FEALPy、PETSc、MFEM、deal.II、DOLFINx 等软件在 MPI 之上实现。由此可见，`mpi4py` 导入成功只证明 Python 可以调用 MPI runtime，并不证明网格划分、共享 DOF 通信或 Matrix-Free 算子已经正确。

## 13. 与主流有限元框架的对应

式 (5) 是这些框架共同追求的全局代数结果，但它们通常采用唯一 owner 加 ghost，而不是式 (10) 中对等重叠副本的平均表示。

| 框架 | 分布式表示与通信责任 | 与本页数学描述的关系 |
|---|---|---|
| [libCEED](https://libceed.org/en/latest/libCEEDapi/) | 用 `P` 表示 MPI 分解；全局 T-vector 和跨设备通信由宿主程序管理，libCEED 主要从 L-vector 层开始工作 | 算子因子分解一致，但不能把 libCEED 本身理解为 MPI 网格与 halo 管理器 |
| [MFEM](https://docs.mfem.org/4.8/classmfem_1_1ParFiniteElementSpace.html) | `ParFiniteElementSpace` 区分 local DOF 与 true DOF，并提供 prolongation/restriction 及共享边、面自由度信息 | 与 $\mathbf R_r$、$\mathbf R_r^{\mathrm T}$ 的限制/延拓描述直接对应 |
| [deal.II](https://dealii.org/developer/doxygen/deal.II/classLinearAlgebra_1_1distributed_1_1Vector.html) | 分布式向量区分 locally owned 和 ghost entries；输入用 `update_ghost_values()`，输出贡献用 `compress(add)` | 等价于 owner→ghost 输入同步和 ghost→owner 输出累加；全局内积只计 owned entries，避免重复计数 |
| [PETSc](https://petsc.org/release/manual/vec/) | DM global vector 不保存 ghost，local vector 保存 ghost；典型流程为 forward `INSERT_VALUES` 和 reverse `ADD_VALUES` | 与式 (15)-(17) 等价，但 owner 值是权威输入，不需要再除以 `refs` |
| [Firedrake](https://www.firedrakeproject.org/firedrake/parallelism.html) | 对用户提供较透明的 MPI 分布式执行，底层通过 PETSc 等组件管理分布式网格和 halo | 上层 `mat_type="matfree"` 选择隐式算子，MPI 分布仍由独立的数据结构负责 |
| [DOLFINx](https://docs.fenicsproject.org/dolfinx/main/cpp/doxygen/d2/d30/classdolfinx_1_1common_1_1IndexMap.html) | `IndexMap` 明确区分 owned 与 ghost indices，并记录共享关系；scatter 支持正向和反向通信 | 是 owner/ghost 语义与当前实现最直接的接口类比之一 |
| [NGSolve](https://docu.ngsolve.org/latest/how_to/howto_parallel.html) | MPI 网格分发和 parallel DOF 负责跨 rank 的共享数据表示 | `nonassemble=True` 决定算子是否显式组装，不单独决定 MPI 分区与同步方式 |

对当前对等重叠副本实现，可作如下概念映射：

| 当前数据流 | 主流 owned/ghost 数据流 |
|---|---|
| 输入 `sync_add(x) / refs` | owner→ghost 的 forward scatter / halo update |
| rank-local $\mathbf A_r\mathbf x_r$ | 同样的局部算子作用 |
| 输出 `sync_add(y)` | ghost→owner 的 reverse scatter-add / `compress(add)` |
| 内积按 `refs` 加权 | 只在 owned DOF 上参加全局归约 |
| 解收集后按 `refs` 平均 | 直接收集唯一 owned true DOF |

这张表表示的是代数角色对应，不表示 API 或内存布局相同。只要限制映射和通信正确，两类实现都可以满足式 (20)；不能机械地把 `sync_add/refs` 搬到 owner/ghost 框架中，因为后者已经通过唯一 owner 消除了输入歧义。

## 14. 阶段验证结果应如何解释

2026-07-27 的 `matrix_free_3` 阶段 1 本地输出中，细网格 1 rank 与 2 ranks 的全局解相对差约为 $7\times10^{-15}$。这一结果支持以下有限结论：

- 当前分区、共享 DOF 同步和全局解收集在该算例上保持了串并行代数一致性；
- 该结果不证明 GMRES 已收敛，也不证明预条件器、扩展性或更高 rank 数正确；
- 同次运行中 GMRES 达到 `maxit=1000` 后真实相对残差仍约为 $7.7\times10^{-4}$，所以阶段 1 仍未通过线性求解门禁。

因此，**并行算子一致性**和**线性求解收敛性**必须分别验收。前者主要检查式 (20)、跨 rank 解差和 FA/EA MatVec 对照；后者必须检查式 (25) 的 true residual。两个 rank 数得到同一个未收敛向量，只能说明并行路径一致，不能把阶段标记为完成。

## 来源与证据

- [[assembly-levels]] — 有限元算子的 $\mathbf P^T\mathbf G^T\mathbf B^T\mathbf D\mathbf B\mathbf G\mathbf P$ 分解、五级装配层次和跨框架术语。
- [[../../research/technical-lines/matrix-free-research-guide]] — 当前 Matrix-Free 技术线的 MPI 接口、正确性门禁和实施边界。
- [MPI Forum: MPI Documents](https://www.mpi-forum.org/docs/) — MPI 标准的规范性入口。
- [mpi4py: Tutorial](https://mpi4py.readthedocs.io/en/stable/tutorial.html) — Python 对 MPI 通信语义的官方使用说明。
- [PETSc: Vectors and Parallel Data](https://petsc.org/release/manual/vec/) — global/local ghost vector、forward insert 和 reverse add。
- [DOLFINx: IndexMap](https://docs.fenicsproject.org/dolfinx/main/cpp/doxygen/d2/d30/classdolfinx_1_1common_1_1IndexMap.html) — owned/ghost indices 与共享关系。
- [deal.II: distributed Vector](https://dealii.org/developer/doxygen/deal.II/classLinearAlgebra_1_1distributed_1_1Vector.html) — locally owned/ghost entries、ghost update、compress 和全局内积。
- [MFEM: ParFiniteElementSpace](https://docs.mfem.org/4.8/classmfem_1_1ParFiniteElementSpace.html) — local/true DOF 及并行 prolongation/restriction。
- [libCEED: Interface Concepts](https://libceed.org/en/latest/libCEEDapi/) — 并行 `P` 层与宿主程序通信责任。
- 本页是对有限元限制/延拓、重叠自由度表示和分布式归约关系的数学整理；具体项目代码、私有数据与阶段运行日志仍由各自工程仓库维护。

## 在我研究中的位置

本页为后续三维线弹性 EA/EbE、PA/QA 与 UA/NONE 路线提供统一的 MPI 数学语义。迁移不同 PDE 或不同装配层级时，应保持式 (5)、式 (20)、式 (24) 和式 (26) 不变，再分别替换局部算子 $\mathbf A_r$ 的形成与作用方式。

面向 PIML 子结构方法时，局部算子 $\mathbf A_r$ 还可以由精确缩聚刚度或预测算子提供；无论局部算子来源如何变化，全局共享自由度、Krylov 内积和残差门禁仍必须遵守同一分布式代数。

## 开放问题

1. 在线弹性基线上应选择 owned/ghost 还是重叠副本作为统一参考表示？
2. 如何统一 CPU MPI、GPU-aware MPI 与多 GPU 下的 halo exchange 和归约语义？
3. 主算子 Matrix-Free、预条件器局部组装时，owned/ghost 与 coarse-grid true DOF 应如何衔接？
4. 非匹配网格、约束自由度、周期边界和自适应加密下，$\mathbf R_r$ 与 $\mathbf Q$ 应如何推广？
5. 如何把通信量、同步次数和负载不均衡纳入统一的端到端性能模型？

## 相关页面

- [[_index]] — Matrix-Free 稳定知识与当前研究的主题入口。
- [[assembly-levels]] — FA/LA/EA/PA/UA 装配层次。
- [[method-lineage]] — Matrix-Free 相关公开成果的方法谱系。
- [[../../research/technical-lines/matrix-free-research-guide]] — 当前能力、阶段路线与验证门禁。
- [[../gpu-hpc/_index]] — MPI、GPU-aware MPI、通信和扩展性研究。
