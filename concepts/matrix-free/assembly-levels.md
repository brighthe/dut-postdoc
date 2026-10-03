---
title: "Matrix-Free 装配层次"
type: concept
aliases:
  - Matrix-Free Assembly Levels
  - Operator Assembly Levels
  - FA/LA/EA/PA/UA
tags:
  - matrix-free
  - finite-element
  - assembly
  - partial-assembly
  - operator
status: in-progress
date_added: 2026-07-21
date_update: 2026-10-03
---

# Matrix-Free 装配层次

> Matrix-Free 是由“算子数据保存到哪一层”区分的实现谱系，按 libCEED 与 MFEM 兼容的口径分为 `FA/TA → LA → EA/EbE → PA/QA → UA/NONE` 五级。

## 1. 统一算子表示

### 1.1 单元层：$\mathbf G$、$\mathbf B$、$\mathbf D$

有限元离散算子可写成

$$
\mathbf K
=
\mathbf G^{\mathsf T}
\mathbf B^{\mathsf T}
\mathbf D
\mathbf B
\mathbf G,
$$

- $\mathbf G$：全局 DOF 与单元 DOF 的限制和回填，即 `cell2dof` 的 gather 与 scatter-add；
- $\mathbf B$：单元自由度到积分点的插值或微分，线弹性中即应变位移矩阵；
- $\mathbf D$：积分权重、几何 Jacobian、材料系数和积分点物理核，线弹性中即 $w_q\lvert\det\mathbf J_e\rvert$ 乘本构矩阵。

本页只讨论线弹性，$\mathbf K$ 即全局刚度算子，单元层记 $\mathbf K_e$；求解器页面（[[../linear-solvers/krylov-subspace-methods|Krylov 子空间方法]]、[[../linear-solvers/preconditioning|预条件]]）按通用线性代数记 $\mathbf A\mathbf x=\mathbf b$，其中的 $\mathbf A$ 即此处的 $\mathbf K$。

单元自由度数记为 $m$，各单元不同时写 $m_e$；单元数记为 $N_e$。

两个映射把同一个场依次表示得越来越冗余：

| 记号       | 名称     | 每个自由度出现次数     | 由谁到达        |
| -------- | ------ | ------------- | ----------- |
| T-vector | 全局 DOF | 恰好 1 次        | —           |
| E-vector | 单元 DOF | 每个含有它的单元各 1 份 | $\mathbf G$ |
| Q-vector | 积分点数据  | 每单元每积分点各 1 份  | $\mathbf B$ |

全局 DOF 的个数是线性方程组的维数，Krylov 方法的内积在这一层定义。

### 1.2 进程层：$\mathbf P$

自由度按 rank 分区存储时，每个 rank 只持有自己单元碰到的自由度，界面自由度在每个持有它的 rank 上各有一份副本。在最外层再套一个映射 $\mathbf P$：

$$
\mathbf K
=
\mathbf P^{\mathsf T}
\mathbf G^{\mathsf T}
\mathbf B^{\mathsf T}
\mathbf D
\mathbf B
\mathbf G
\mathbf P,
$$

$\mathbf P$ 与 $\mathbf G$ 是同一种构造在两个层次上的重复，都是布尔限制矩阵的竖向堆叠：$\mathbf P$ 按 rank 堆叠，把全局向量的每个分量复制给持有它的每个 rank；$\mathbf G$ 按单元堆叠，把每个 rank 局部向量的每个分量复制给用到它的每个单元。记 rank 总数为 $R$，

$$
\mathbf P=
\begin{bmatrix}\mathbf P_0\\\vdots\\\mathbf P_{R-1}\end{bmatrix},
\qquad
\mathbf G=
\begin{bmatrix}\mathbf G_1\\\vdots\\\mathbf G_{N_e}\end{bmatrix},
\qquad
\mathbf P_p\in\{0,1\}^{N_p\times N_{\text{true}}},
\quad
\mathbf G_e\in\{0,1\}^{m_e\times N_L}.
$$

$\mathbf P_p$ 取出 rank $p$ 持有的那些 true DOF，$\mathbf G_e$ 取出单元 $e$ 用到的那些进程局部 DOF；$N_p$ 为 rank $p$ 持有的自由度数（含界面副本），$N_L=\sum_p N_p$ 为 L 层维数。$\mathbf G_e$ 只触及拥有单元 $e$ 的那个 rank 的分量，因此 $\mathbf G$ 按 rank 天然块对角，L 层以内没有跨 rank 耦合。单一分区时 $R=1$、$\mathbf P=\mathbf I$。

$\mathbf P^{\mathsf T}$ 把各 rank 的贡献按全局编号相加，是代数意义上的求和归约，结果落在 T 层；halo exchange 是各 rank 把界面自由度上的本地贡献互发并相加，使每份副本都拿到全部贡献，属于“相加后再把结果播回各副本”的通信形态，对应 $\mathbf P\mathbf P^{\mathsf T}$，不是 $\mathbf P^{\mathsf T}$ 本身。向量层次因此多出一层：

| 记号 | 名称 | 每个自由度出现次数 | 由谁到达 |
|---|---|---|---|
| T-vector | true DOF（全局自由度，不含副本） | 恰好 1 次 | — |
| L-vector | 进程局部 DOF | 每个持有它的 rank 各 1 份 | $\mathbf P$ |
| E-vector | 单元 DOF | 每个含有它的单元各 1 份 | $\mathbf G$ |
| Q-vector | 积分点数据 | 每单元每积分点各 1 份 | $\mathbf B$ |

true DOF 就是 1.1 的全局 DOF，不含副本，$N_{\text{true}}$ 才是线性方程组的真实维数。记引用计数 $\boldsymbol r=\mathbf P^{\mathsf T}\mathbf 1$、L 层副本数对角阵 $\mathbf W=\operatorname{diag}(\mathbf P\boldsymbol r)$，则

$$
\mathbf P^{\mathsf T}\mathbf P=\operatorname{diag}(\boldsymbol r),
\qquad
\mathbf P^{\mathsf T}\mathbf W^{-1}\mathbf P=\mathbf I .
$$

前式给出界面自由度在 L 层被重复计数的倍数，后式说明 L 层按副本数加权的内积等于 T 层欧氏内积——Krylov 方法的内积必须这样算。

单元分区、owned/ghost 自由度、halo exchange 与全局内积的完整代数见 [[../gpu-hpc/distributed-operator-and-shared-dofs]]，该页采用重叠副本表示，不显式存 T 层向量。两页记号对照：

| 本页 | 被引页 |
|---|---|
| $\mathbf P_p$ | $\mathbf E_p^{\mathsf T}$，该页称「限制算子」，MFEM 称 prolongation |
| $\mathbf D$：积分点算子 | $\mathbf D=\operatorname{diag}(\boldsymbol r)$：引用计数对角阵 |
| $\mathbf P\mathbf P^{\mathsf T}$、$\mathbf P(\mathbf P^{\mathsf T}\mathbf P)^{-1}\mathbf P^{\mathsf T}$ | 归约 $\mathcal S$、一致化投影 $\mathcal C$ |

## 2. 五级分类

四个因子都有块结构：

$$
\mathbf G=
\begin{bmatrix}\mathbf G_1\\\vdots\\\mathbf G_{N_e}\end{bmatrix},
\qquad
\mathbf B=\operatorname{blkdiag}(\mathbf B_e),
\qquad
\mathbf D=\operatorname{blkdiag}(\mathbf D_e),
\qquad
\mathbf D_e=\operatorname{blkdiag}(\mathbf D_{e,q}).
$$

$\mathbf G_e$ 是进程局部自由度到单元 $e$ 自由度的布尔限制矩阵；$\mathbf D_e$ 按积分点 $q$ 分块，积分点之间没有耦合，这是 PA/UA 能够成立的结构前提。代入统一表示得到

$$
\mathbf K
=\sum_{e=1}^{N_e}
\bigl(\mathbf G_e\mathbf P\bigr)^{\mathsf T}
\mathbf B_e^{\mathsf T}\mathbf D_e\mathbf B_e
\bigl(\mathbf G_e\mathbf P\bigr).
\tag{$\ast$}
$$

一次算子作用是沿因子链的一趟往返：

$$
\begin{aligned}
\mathbf x\ (\text{true DOF})
&\xrightarrow{\ \mathbf P\ }\text{local}
\xrightarrow{\ \mathbf G\ }\text{element}
\xrightarrow{\ \mathbf B\ }\text{quadrature}
\xrightarrow{\ \mathbf D\ }\text{quadrature}\\[2pt]
&\xrightarrow{\ \mathbf B^{\mathsf T}\ }\text{element}
\xrightarrow{\ \mathbf G^{\mathsf T}\ }\text{local}
\xrightarrow{\ \mathbf P^{\mathsf T}\ }\mathbf y\ (\text{true DOF})
\end{aligned}
$$

装配层级就是在这条链上选一个预计算前缘。五级都是 $(\ast)$ 的不同求值方式，没有引入新算子。

算子的因子分成四个阶段计算，装配层级决定哪些阶段的产物预先相乘并常驻：

| 阶段 | 何时执行 | 依赖 | 产物 |
|---|---|---|---|
| build | 与网格无关，一次 | 单元类型、阶次、积分规则 | 参考单元积分点上的基函数值与导数值，如 $\hat{\mathbf B}_\varphi$，以及积分权重 $w_q$ |
| setup | 网格确定后，一次 | 网格几何与拓扑 | 积分点上的几何因子 $\mathbf J_e^{-1}$、$\lvert\det\mathbf J_e\rvert$，以及限制算子 $\mathbf G$、$\mathbf P$ |
| update | 每次设计或材料变量改变 | $\rho_e$、本构 | 积分点算子 $\mathbf D_{e,q}$（含 $\rho_e$、本构与积分权重）；已保存的、含 $\mathbf D_e$ 的因子随之重算 |
| apply | 每次 MatVec | 输入向量 | 依次作用 $\mathbf P$、$\mathbf G$、$\mathbf B$、$\mathbf D$、$\mathbf B^{\mathsf T}$、$\mathbf G^{\mathsf T}$、$\mathbf P^{\mathsf T}$，即 gather、梯度、逐点本构、梯度转置、scatter-add |

| 层级 | setup 保存 | 每次 apply 执行 | Matrix-Free 口径 |
|---|---|---|---|
| Full/True Assembly（FA/TA） | 全局稀疏矩阵 $\mathbf P^{\mathsf T}\mathbf G^{\mathsf T}\mathbf B^{\mathsf T}\mathbf D\mathbf B\mathbf G\mathbf P$ | 一次 SpMV | 不属于 |
| Local Assembly（LA） | 每个 rank 的局部稀疏矩阵 $\mathbf G^{\mathsf T}\mathbf B^{\mathsf T}\mathbf D\mathbf B\mathbf G$ | $\mathbf P$、局部 SpMV、$\mathbf P^{\mathsf T}$ | 通常不属于 |
| Element Assembly / Element-by-Element（EA/EbE） | 稠密单元矩阵 $\{\mathbf K_e=\mathbf B_e^{\mathsf T}\mathbf D_e\mathbf B_e\}$ | gather、$\mathbf K_e\mathbf x_e$、scatter-add | 广义 Matrix-Free |
| Partial/Quadrature Assembly（PA/QA） | 积分点数据 $\{\mathbf D_e\}$ | gather、$\mathbf B_e$、$\mathbf D_e$、$\mathbf B_e^{\mathsf T}$、scatter-add | 高阶有限元的主流路线 |
| Unassembled（UA/NONE） | 几何与材料 | 全链，含 $\mathbf D_e$ 的即时构造 | 严格 fully Matrix-Free |

判定一份实现属于哪一级，看主算子路径实际保存的对象与 MatVec 数据流：保存全局或 true-DOF 稀疏矩阵为 FA/TA；只在各 rank 保存局部稀疏矩阵为 LA；为每个单元保存完整 $\mathbf K_e$，或只保存一份参考单元矩阵与逐单元标量（2.3.2），为 EA；只保存 $\mathbf D_e$ 或等价数据为 PA；$\mathbf D_e$ 在每次 MatVec 中从几何、系数或状态即时计算为 UA。为调试或黄金对照另行构造的 FA 算子不改变主路径的分类。没有全局稀疏矩阵不自动等于 PA 或 UA，`MATSHELL`、`ImplicitMatrix`、`nonassemble=True` 或自定义 `operator.apply()` 只说明采用了隐式算子接口，不决定层级。

前缘位置单调控制两件事：前缘越靠内，setup 与 update 越便宜，每次 apply 需要重算的因子越多。存储却不是前缘位置的单调函数，因为“装配”同时做了两件不同的事：预计算把若干因子相乘并保存，增加存储、减少 apply 工作量；合并由 scatter-add 把落在同一全局位置的多份贡献相加，减少存储。合并只在跨越 $\mathbf G$ 和 $\mathbf P$ 时发生，跨越 $\mathbf B$ 和 $\mathbf D$ 时不发生。FA 同时享有预计算与合并；标准 EA 保留了单元内的预计算但放弃了合并，存储反而高于 FA，共享参考单元矩阵的特例除外（2.3.2）；真正的存储下降从 PA 开始，那是往回撤预计算，不是恢复合并。存储与重算的权衡在 EA → PA → UA 之间成立，FA/LA 省的是重复条目，不是重算。

以下逐级给出算子形式。为突出装配层级本身，$\mathbf P$ 在 EA 之后各式中省略，可统一理解为把 $\mathbf G_e$ 替换为 $\mathbf G_e\mathbf P$。

### 2.1 FA/TA：全局矩阵作用

FA/TA 在 setup 阶段完成单元贡献的 scatter-add，形成并保存全局稀疏矩阵：

$$
\mathbf K_{\mathrm{FA}}
=
\sum_e
\mathbf G_e^{\mathsf T}
\mathbf K_e
\mathbf G_e,
\qquad
\mathbf y_{\mathrm{FA}}
=
\mathbf K_{\mathrm{FA}}\mathbf x.
$$

这里的 $\mathbf G_e$ 已含 $\mathbf P$。全局矩阵在 true DOF 编号下形成，setup 之后 $\mathbf P,\mathbf G,\mathbf B,\mathbf D$ 全部可以释放，五级中只有 FA 的 apply 完全不需要网格。FA 强调形成完整全局矩阵，TA 强调该矩阵建立在 true DOF 编号上，单一分区（$\mathbf P=\mathbf I$）下两者无区别，多分区下 TA 的措辞更准确。

FA 的稀疏模式由合并决定：$(i,j)$ 非零当且仅当自由度 $i$ 与 $j$ 至少共享一个单元，

$$
\operatorname{nnz}(\mathbf K_{\mathrm{FA}})
=d^2\sum_{a=1}^{N_n}\bigl(\nu_a+1\bigr),
$$

其中 $\nu_a$ 为与节点 $a$ 共享单元的邻接节点数，$d$ 为每节点分量数。三维四面体网格上 $\nu_a$ 典型在 $10\sim15$，三维向量 $P_1$ 每行约 $33\sim48$ 个非零。

$\operatorname{nnz}$ 只是稳态存储；形成 $\mathbf K_{\mathrm{FA}}$ 的那一刻另有一段瞬时峰值，量级由合并的实现方式决定，而不由 $\operatorname{nnz}$ 决定。把单元贡献先摊平成全长三元组（长度 $N_e m^2$）再排序去重，峰值要同时压住若干份该长度的索引与数值数组，可比 $\operatorname{nnz}$ 高一个量级；先由拓扑建出稀疏模式与单元到槽位的映射、再按单元原地累加，峰值则不超过 $\operatorname{nnz}$ 级。因此 FA 的容量上限由 setup 峰值而非 $\operatorname{nnz}$ 决定，几条实现路线的实测单价由实现仓库持有，本页不给数值。

FA 的 apply 是一次 SpMV，浮点量 $2\operatorname{nnz}$ 是五级中最少的，但 SpMV 的性能不由浮点量决定。以 CSR 为例，每个非零读取一个值（8 字节）和一个列索引（4 字节），换来一次乘和一次加：

$$
\text{算术强度}\;\approx\;\frac{2\ \text{flop}}{12\ \text{byte}}\;\approx\;0.17\ \text{flop/byte}.
$$

现代 CPU 与 GPU 的 machine balance 远高于这个值，SpMV 是彻底的访存受限内核，且 $\mathbf x[\mathrm{col}[j]]$ 的间接寻址是随机访存。整条 Matrix-Free 路线的目标不是减少浮点运算，而是提高算术强度，用重算换掉对大数组的读取；用 flop 计数论证 Matrix-Free 的优劣是错的。

FA 被排除在 Matrix-Free 之外，不等于它是落后选项。稀疏直接法（LU、Cholesky、MUMPS）及由此而来的鲁棒黄金参考解、代数预条件（ILU、AMG）、谱与条件数分析、稀疏模式诊断都只有显式矩阵才提供；任何一级与 FA 的 MatVec 逐点比较是最直接的实现判据。本页把 FA 定位为黄金参考。

### 2.2 LA：进程局部矩阵作用

LA 把求和切在 $\mathbf P$ 这一层：每个 rank $p$ 只对本进程的单元求和，形成局部稀疏矩阵，$\mathbf P$ 留到运行时：

$$
\mathbf K_{\mathrm L}^{(p)}
=\sum_{e\in\Omega_p}\mathbf G_e^{\mathsf T}\mathbf K_e\mathbf G_e,
\qquad
\mathbf y_{\mathrm{LA}}
=\sum_p\mathbf P_p^{\mathsf T}\!\left[\mathbf K_{\mathrm L}^{(p)}\left(\mathbf P_p\mathbf x\right)\right].
$$

单元分区互不相交且完全覆盖时 $\sum_p \mathbf P_p^{\mathsf T}\mathbf K_{\mathrm L}^{(p)}\mathbf P_p=\mathbf K_{\mathrm{FA}}$，LA 与 FA 在精确算术下等价。

LA 不是存储优化：界面自由度所在的行在多个 rank 上重复出现，局部矩阵非零总数不小于全局矩阵。它的意义是避免全局编号与集中存储、把 setup 局部化，并为 Schwarz、子结构等区域分解型预条件提供天然的局部代数对象。省略的是全局编号，不是全局矩阵，所以 LA 通常不算 Matrix-Free。

### 2.3 EA/EbE：单元矩阵作用

EA/EbE 在 setup 中为每个单元形成并保存稠密单元矩阵 $\mathbf K_e=\mathbf B_e^{\mathsf T}\mathbf D_e\mathbf B_e\in\mathbb R^{m\times m}$，但不对单元求和。每次 MatVec 为

$$
\mathbf y_{\mathrm{EA}}=\sum_e\mathbf G_e^{\mathsf T}\bigl(\mathbf K_e\,\mathbf G_e\mathbf x\bigr),
$$

按括号从内到外依次为 gather、单元矩阵–向量乘 $\mathbf K_e\mathbf x_e$、scatter-add：

$$
\mathbf x\ \xrightarrow{\ \mathbf G_e\ (\text{gather})\ }\ \mathbf x_e\ \xrightarrow{\ \mathbf K_e\ }\ \mathbf y_e\ \xrightarrow{\ \sum_e\mathbf G_e^{\mathsf T}\ (\text{scatter-add})\ }\ \mathbf y_{\mathrm{EA}} .
$$

单元矩阵–向量乘只得到各单元的 $\mathbf y_e$，共享节点上来自不同单元的贡献由 scatter-add 累加成全局向量。与 2.1 的 $\mathbf y_{\mathrm{FA}}=\bigl(\sum_e\mathbf G_e^{\mathsf T}\mathbf K_e\mathbf G_e\bigr)\mathbf x$ 相比，EA 只是把单元求和从 setup 移到了每次 apply。

按单元矩阵的保存方式，EA 分为以下两种。

#### 2.3.1 标准 EA：逐单元保存 $\mathbf K_e$

标准 EA 对网格、单元类型和材料没有额外要求，是 EA 的一般形式；单元矩阵彼此不成比例时只能用它。代价是存储：对单元求和只合并落在同一全局位置的元，因此

$$
\operatorname{nnz}(\mathbf K_{\mathrm{FA}})\;\le\;N_e m^2\;=\;\text{标准 EA 的存储量}.
$$

#### 2.3.2 共享参考 EA：只保存 $\mathbf K_e^0$ 与 $s_e$

适用前提有两条。几何上，所有单元的形状、尺寸与朝向都相同，彼此只差平移，如笛卡尔规则网格上的等尺寸六面体；此时各单元的 Jacobian 相同，$\mathbf B_e=\mathbf B$。本构上，各单元只差一个标量，$\mathbf D_e=s_e\mathbf D^0$，如 SIMP 固定泊松比、只插值弹性模量时 $s_e=E(\rho_e)/E_0$。此时

$$
\mathbf K_e=s_e\mathbf K_e^0,
\qquad
\mathbf K_e^0=\mathbf B^{\mathsf T}\mathbf D^0\mathbf B,
$$

$\mathbf K_e^0$ 即 [[../linear-elasticity#6. Voigt 记号、应变矩阵与单元算子|linear-elasticity §6]] 式 (26) 的实体材料单元刚度，在此前提下各单元相同，$\mathbf K_e=s_e\mathbf K_e^0$ 即该页式 (27)。$\mathbf D^0=\operatorname{blkdiag}_q\bigl(w_q\lvert\det\mathbf J\rvert\,\mathbf D_0\bigr)$ 含积分权重与 Jacobian 行列式，与该页的本构矩阵 $\mathbf D_0$ 不是同一对象。

只需保存一份 $\mathbf K_e^0$ 与 $N_e$ 个标量 $s_e$，因此

$$
\text{共享参考 EA 的存储量}\;=\;m^2+N_e\;<\;\operatorname{nnz}(\mathbf K_{\mathrm{FA}})\;\le\;N_e m^2 .
$$

### 2.4 PA/QA：积分点数据作用

PA/QA 连 $\mathbf K_e$ 都不形成，只保存积分点数据 $\mathbf D_e$：

$$
\mathbf y_{\mathrm{PA}}
=\sum_e
\mathbf G_e^{\mathsf T}
\mathbf B_e^{\mathsf T}
\left[
\mathbf D_e
\left(
\mathbf B_e\left(\mathbf G_e\mathbf x\right)
\right)
\right].
$$

中间一步没有任何积分点间的耦合，这是 PA 在 GPU 上天然并行的原因。

PA 成立的前提是 $\mathbf B_e$ 不需要保存，能从参考单元数据与单元几何现算，这依赖两层分解。

#### 2.4.1 $\mathbf B_e$ 侧：两层分解与现算

第一层对任意单元类型成立。$\mathbf B_e$ 把单元位移自由度变成 Voigt 应变（见 [[../linear-elasticity#6. Voigt 记号、应变矩阵与单元算子|Voigt 记号与应变矩阵]]），可拆成三次含义明确的变换；以下把 $d\times d$ 梯度 $\partial u_i/\partial x_j$ 按 $i$ 为外层、$j$ 为内层拉直成 $d^2$ 维向量，三个因子都作用在拉直后的向量上：

$$
\mathbf x_e
\;\xrightarrow{\ \hat{\mathbf B}\ }\;
\hat\nabla\boldsymbol u
\;\xrightarrow{\ \boldsymbol\Gamma(\mathbf J_e)\ }\;
\nabla\boldsymbol u
\;\xrightarrow{\ \mathbf S\ }\;
\widehat{\boldsymbol\varepsilon},
\qquad
\mathbf B_e=\mathbf S\,\boldsymbol\Gamma(\mathbf J_e)\,\hat{\mathbf B}.
$$

$\hat{\mathbf B}$ 在参考单元上求导，给出参考坐标梯度 $\partial\hat u_i/\partial\hat x_j$；$\boldsymbol\Gamma$ 按链式法则 $\nabla_{\boldsymbol x}u_i=\mathbf J_e^{-\mathsf T}\nabla_{\hat{\boldsymbol x}}u_i$ 拉回物理坐标；$\mathbf S$ 取对称部分并按 Voigt 记号排成 $n_s=d(d+1)/2$ 个分量。记单元上标量基函数个数为 $n_\varphi$，此时 $m=d\,n_\varphi$；记参考单元标量基函数梯度 $\hat{\mathbf B}_\varphi\in\mathbb R^{d\times n_\varphi}$。下表的形状均指单个积分点上的矩阵，存储则为整个单元、单份共享数据的合计：

| 因子                               | 形状              | 依赖           | 逐单元存储                        | 共享存储                           |
| -------------------------------- | --------------- | ------------ | ---------------------------- | ------------------------------ |
| $\hat{\mathbf B}$                | $d^2\times m$   | 单元类型、阶、积分点   | $0$                          | $n_q\,d\,n_\varphi$ 个数，同类型同阶共用 |
| $\boldsymbol\Gamma(\mathbf J_e)$ | $d^2\times d^2$ | 单元几何         | $n_q\,d^2$ 个数，仿射单纯形退化为 $d^2$ | $0$                            |
| $\mathbf S$                      | $n_s\times d^2$ | 方程（与单元、网格无关） | $0$                          | $0$，$0/1$ 常量矩阵                 |

$\hat{\mathbf B}$：在参考单元的积分点上对标量基函数求导得到，与单元几何无关，在 build 阶段算好、不进 setup，同类型同阶的单元共享同一个 $\hat{\mathbf B}_\varphi$，全网格只存一份。$d$ 个位移分量共用同一个 $d\times n_\varphi$ 的 $\hat{\mathbf B}_\varphi$，逐积分点有

$$
\hat{\mathbf B}(q)
=\mathbf I_d\otimes\hat{\mathbf B}_\varphi(q)
=\begin{bmatrix}
\hat{\mathbf B}_\varphi(q) & & \\
 & \ddots & \\
 & & \hat{\mathbf B}_\varphi(q)
\end{bmatrix}
\in\mathbb R^{d^2\times m}.
$$

张量积单元上 $\hat{\mathbf B}_\varphi$ 还有第二层结构。把各积分点上 $\hat{\mathbf B}_\varphi$ 的第 $k$ 行按积分点叠成 $n_q\times n_\varphi$ 的矩阵 $\hat{\mathbf B}_{\varphi,k}$，即对 $\hat x_k$ 求导在全部积分点上的取值，则

$$
\hat{\mathbf B}_{\varphi,k}=\bigotimes_{j=1}^{d}\mathbf M^{(k)}_j,
\qquad
\mathbf M^{(k)}_j=
\begin{cases}
\hat{\mathbf B}_{1\mathrm D}, & j=k,\\
\hat{\mathbf N}_{1\mathrm D}, & j\ne k,
\end{cases}
$$

式中 $\hat{\mathbf N}_{1\mathrm D}$ 与 $\hat{\mathbf B}_{1\mathrm D}$ 分别是一维基函数值与其导数在一维积分点上的取值矩阵：$d$ 个一维算子的张量积里只有求导的那一维取 $\hat{\mathbf B}_{1\mathrm D}$，其余取 $\hat{\mathbf N}_{1\mathrm D}$。有了这个结构，$\hat{\mathbf B}_{\varphi,k}$ 乘单元上某个位移分量的 $n_\varphi$ 个节点值可以拆成 $d$ 次一维作用，矩阵本身不必形成；这一算法称为 sum factorization。

$\boldsymbol\Gamma$：由等参映射 $\boldsymbol x(\hat{\boldsymbol x})=\sum_a\boldsymbol x_a\varphi_a(\hat{\boldsymbol x})$ 算出，用的就是位移的 $\hat{\mathbf B}_\varphi$，几何不另存一份基函数：

$$
\mathbf J_e(q)=\mathbf X_e\,\hat{\mathbf B}_\varphi(q)^{\mathsf T},
\qquad
\boldsymbol\Gamma(\mathbf J_e)=\mathbf I_d\otimes\mathbf J_e^{-\mathsf T},
$$

式中 $\mathbf X_e\in\mathbb R^{d\times n_\varphi}$ 为单元节点坐标。$d$ 个位移分量各自被同一个 $\mathbf J_e^{-\mathsf T}$ 拉回、彼此不混合，故 $\boldsymbol\Gamma$ 为块对角。setup 阶段每单元每积分点求一次逆，只存 $\mathbf J_e^{-1}$ 的 $d^2$ 个数，$\boldsymbol\Gamma$ 本身不形成，$\lvert\det\mathbf J_e\rvert$ 并入 $\mathbf D_e$。三个因子里只有它随网格规模增长，逐积分点一份、按 $N\,n_q\,d^2$ 计，PA 单元存储的 $O(n_q)$ 即由此而来；仿射单纯形上 $\mathbf J_e$ 为常量，降到 $N\,d^2$。

$\mathbf S$：不用算。法向行取 $\partial u_i/\partial x_i$，剪切行把 $\partial u_i/\partial x_j$ 与 $\partial u_j/\partial x_i$ 相加——工程剪应变的因子 2 由这次相加吸收，非零元全为 $1$，张量剪应变约定下则为 $1/2$。对称化跨分量，写不成 $\mathbf I_d\otimes(\cdot)$。它必须作用在 $\boldsymbol\Gamma$ 之后：$\mathbf J_e^{-\mathsf T}$ 非正交时对称化与坐标拉回不交换，在参考坐标下先取对称得到的不是应变。

#### 2.4.2 $\mathbf D_e$ 侧：逐积分点的标量

$\mathbf D_e$ 也不只是本构矩阵，而是逐积分点的一个标量乘一个常量矩阵：

$$
\mathbf D_{e,q}=w_q\,\lvert\det\mathbf J_e\rvert\,s_e\,\mathbf D_0,
$$

$s_e=E(\rho_e)/E_0$ 为 SIMP 等材料插值给出的单元刚度缩放系数，与 2.3.2 相同，无密度场时取 1。设计更新只改这 $n_q$ 个标量（$n_q$ 为单元积分点数），三个 $\mathbf B$ 因子全部不动，也不需重新积分；该性质在第 3 节与 EA、UA 并列讨论。

由结合律 $\mathbf B_e^{\mathsf T}\mathbf D_0\,\mathbf B_e=\hat{\mathbf B}^{\mathsf T}\boldsymbol\Gamma^{\mathsf T}(\mathbf S^{\mathsf T}\mathbf D_0\,\mathbf S)\boldsymbol\Gamma\,\hat{\mathbf B}$，$\mathbf S$ 往左归给 $\mathbf B_e$、往右归给逐点算子都成立。PA 一律往右归：$\mathbf S$ 是方程专有的——热传导没有它，混合元的不一样——而 $\hat{\mathbf B}$ 与 $\boldsymbol\Gamma$ 的依赖里没有方程，$\hat{\mathbf B}_\varphi$ 换个方程仍可共用；且 $\mathbf S$ 跨分量，$\mathbf B_e$ 一旦形成就是 $n_s\times m$ 的稠密对象，$\mathbf I_d\otimes(\cdot)$ 的块对角结构与 sum factorization 都用不上，那恰是 PA 要躲的东西。于是 $\mathbf B$ 一环只做 $\boldsymbol\Gamma\,\hat{\mathbf B}$、交出 $\nabla\boldsymbol u$ 而非 $\widehat{\boldsymbol\varepsilon}$，逐点算子实为 $w_q\lvert\det\mathbf J_e\rvert\,s_e\,\mathbf S^{\mathsf T}\mathbf D_0\,\mathbf S$，形状由 $n_s\times n_s$ 变成 $d^2\times d^2$。libCEED 的 `CeedBasis` 只出 `CEED_EVAL_GRAD`、MFEM 的 `DofToQuad` 只存标量参考基函数的值与梯度、deal.II 的 `FEEvaluation::get_gradient()` 返回张量梯度，对称化一律写在 QFunction 或用户侧，三者同此。

这不改存储的账：三件分开存，$\mathbf S$ 与各向同性下的 $\mathbf D_0$ 都与单元无关、全网格各一份，逐单元的仍只有 $w_q\lvert\det\mathbf J_e\rvert\,s_e$ 这 $n_q$ 个标量。是否把 $\mathbf S^{\mathsf T}\mathbf D_0\,\mathbf S$ 预乘成一个常量矩阵，属于 apply 侧的实现选择，与常驻量无关。

写成 $w_q\lvert\det\mathbf J_e\rvert$ 时默认积分权重按参考单元测度归一。部分实现的单纯形求积采用重心坐标、权重之和为 1 而非参考单元测度（FEALPy 即如此），该因子相应写成 $w_q\lvert T_e\rvert$，二者在 $d$ 维单纯形上相差 $d!$ 倍。

#### 2.4.3 存储与代价

设 $d$ 维张量积单元、阶 $p$、每方向 $q\approx p+1$ 个积分点，标量基函数个数 $n_\varphi=(p+1)^d$（此时 $m=d\,n_\varphi$）、积分点数 $n_q=q^d$。下表的 $O$ 只跟踪 $p$ 的标度，$d$ 视为固定常数：

| | 每单元存储 | 每单元 apply 代价 |
|---|---|---|
| EA | $O(m^2)=O(p^{2d})$ | $O(m^2)=O(p^{2d})$ |
| PA，朴素作用 $\hat{\mathbf B}$ | $O(n_q)=O(p^{d})$ | $O(n_q m)=O(p^{2d})$ |
| PA + sum factorization | $O(n_q)=O(p^{d})$ | $O(d\,q\,m)=O(p^{d+1})$ |

PA 的存储优势对任意单元成立，计算优势只在张量积单元加 sum factorization 下成立，加速比 $p^{2d}/p^{d+1}=p^{\,d-1}$，$d=3$ 时 $p=1$ 给出 1，$p=8$ 给出 64。PA 本质上是高阶方法的技术。

$O(n_q)$ 里的常数在低阶上不可忽略。三维线弹性 $P_1$ 四面体上 $m=d\,n_\varphi=12$，$\mathbf B_e\in\mathbb R^{6\times12}$ 为常量、单点积分即精确：EA 存 $\mathbf K_e$ 共 $m^2=144$ 个数，PA 逐积分点存 $w\lvert\det\mathbf J_e\rvert\,\mathbf D_e$（36 个）加 $\mathbf J_e^{-1}$（9 个）共 45 个数，各向同性时 $\mathbf D_e$ 由 $(\lambda_e,\mu_e)$ 确定、降到 11 个数；浮点代价两者同为 $O(m^2)$。几何因子与加权测度都随 $n_q$ 成比例放大，故一般各向异性下 $n_q\ge4$ 时 PA 的每单元存储即超过 EA，引用 PA 的存储结论时须同时给出 $n_q$ 与是否各向同性。

### 2.5 UA/NONE：即时生成的算子作用

UA/NONE 连 $\mathbf D_e$ 也不保存，每次 apply 从单元几何节点 $\mathbf X_e$、材料或设计变量 $\boldsymbol\rho_e$ 及当前状态即时构造：

$$
\mathbf y_{\mathrm{UA}}
=\sum_e
\mathbf G_e^{\mathsf T}
\mathbf B_e^{\mathsf T}
\left[
\mathbf D_e\!\left(\mathbf X_e,\boldsymbol\rho_e,\dots\right)
\left(
\mathbf B_e\left(\mathbf G_e\mathbf x\right)
\right)
\right].
$$

$\mathbf J_e$、$\det\mathbf J_e$、$\mathbf J_e^{-1}$ 与材料张量全部进入 apply 内部，持久存储降到网格加每单元的设计或材料变量。UA 相对 PA 多出 Jacobian 求逆与行列式的重复计算；加速器的瓶颈多在访存带宽而非浮点吞吐，把 $\mathbf D_e$ 从“读”改为“算”在带宽受限区间是净收益。这条推理是定性的，不能替代实测。

材料分布随迭代变化的问题（拓扑优化中 $\mathbf D_e$ 依赖设计变量 $\rho_e$）在 setup 存储与 apply 代价之外还有第三项，每次设计更新后重建算子的成本：

$$
\rho_e\ \text{改变}\;\Longrightarrow\;\mathbf D_e\ \text{改变}\;\Longrightarrow\;
\begin{cases}
\text{FA/LA：重新组装全局或局部稀疏矩阵}\\
\text{EA：重算全部 }\mathbf K_e=\mathbf B_e^{\mathsf T}\mathbf D_e\mathbf B_e\text{；共享参考单元矩阵时只写 }s_e\\
\text{PA：只重算 }\mathbf D_e\\
\text{UA：无 update 成本，}\rho_e\ \text{直接进 apply}
\end{cases}
$$

装配层级越低，update 成本越低。单次求解的基准测试看不见这一维，优化循环中它与 apply 成本同量级，性能报告必须分别列出 setup、update、apply 与完整 solve。

## 3. 三条跨层级性质

精确算术下五级等价。五级都是 $(\ast)$ 的不同求值方式，表示同一个离散算子；浮点下的差异来自求和与组装顺序，属舍入误差量级。任意两级之间的 MatVec 逐点比较可以作为实现正确性判据，容差按舍入量级而非算法精度设定。

对称正定性沿链自动保持。$(\ast)$ 的每一项都是 $\mathbf M_e^{\mathsf T}\mathbf D_e\mathbf M_e$ 的形式（$\mathbf M_e=\mathbf B_e\mathbf G_e\mathbf P$），$\mathbf D_e$ 对称（半）正定时每项及其和亦然。CG 一类要求对称正定的 Krylov 方法的适用性与装配层级无关，逐级要验证的是实现，不是数学。

对角线与子块的可及性随层级下降而递减。预条件器需要的不只是 MatVec：

| 层级 | update 成本 | $\operatorname{diag}(\mathbf K)$ | 非对角子块 |
|---|---|---|---|
| FA/TA | 重新组装 | 直接读取 | 直接读取 |
| LA | 重新组装 | 直接读取 | 直接读取 |
| EA/EbE | 重算 $\mathbf K_e$；共享参考单元矩阵时只写 $s_e$ | $\sum_e\mathbf G_e^{\mathsf T}\operatorname{diag}(\mathbf K_e)$，一次 scatter-add | 可从 $\mathbf K_e$ 取出 |
| PA/QA | 重算 $\mathbf D_e$ | $K_{ii}=\sum_e\sum_{\alpha,\beta}(\mathbf M_e)_{\alpha i}(\mathbf D_e)_{\alpha\beta}(\mathbf M_e)_{\beta i}$，需专门 kernel，代价约一次 apply | 不可直接获得 |
| UA/NONE | 无 | 同 PA | 不可直接获得 |

Jacobi 在所有层级可用，块 Jacobi、ILU 以及依赖 strength-of-connection 的 AMG 在 PA/UA 下无法直接构造：装配层级约束的是预条件器，不是求解器。因此主算子与预条件器可以采用不同层级，主算子取 PA/UA 换存储，预条件器另取一个能提供对角、低阶组装代理或几何多重网格粗空间的层级；性能报告须分别注明 operator level、preconditioner level 以及 setup、update、apply 和完整 solve 成本。

实现是否真的做到前两条，以三步验收：与 FA 的 MatVec 逐点比较（裸算子与施加 Dirichlet 之后各一次）、双线性配对检验对称性、与 FA 直接法解比较；EA 及以下层级没有可逐元素比较的矩阵，参照解只有 FA 能提供，阈值由实现给出。

## 4. Dirichlet 条件的施加

Neumann 条件进入右端的边界积分，Robin 条件增加一个面上的边界算子，两者与装配层级无关（[[../../literature/fem-libraries/translations/Brown2021-libCEED-fast-algebra-zh|Brown et al. (2021)]]，算子分解一节）；只有 Dirichlet 约束未知量本身。

Dirichlet 条件的施加方式依赖装配层级。记 $\boldsymbol\Pi_D$、$\boldsymbol\Pi_I$ 为 Dirichlet 自由度与内部自由度上的对角投影，$\boldsymbol\Pi_D+\boldsymbol\Pi_I=\mathbf I$，$\bar{\boldsymbol u}$ 为边界取给定值、内部取零的基准向量；$\boldsymbol\Pi$ 与进程层映射 $\mathbf P$ 无关。两种做法：

- 对称消元（FA/LA）：矩阵已经形成，把 Dirichlet 自由度所在的行与列清零、对角置 1，右端减去被清掉的列乘边界值，再把 Dirichlet 位置的右端换成边界值。
- 投影包装（EA/PA/UA）：没有可改写的矩阵，把原算子包一层，每次 apply 执行「置零 → 作用 → 还原」，右端做同样的一次修正。

两者写成同一对公式：

$$
\tilde{\mathbf K}=\boldsymbol\Pi_I\mathbf K\boldsymbol\Pi_I+\boldsymbol\Pi_D,
\qquad
\tilde{\boldsymbol b}=\boldsymbol\Pi_I\bigl(\boldsymbol b-\mathbf K\bar{\boldsymbol u}\bigr)+\boldsymbol\Pi_D\bar{\boldsymbol u}.
$$

对称消元显式存下 $\tilde{\mathbf K}$，投影包装每次算 $\tilde{\mathbf K}\boldsymbol x$，线性系统相同，与 FA 的比较在 $\tilde{\mathbf K}$ 上同样成立。$\tilde{\mathbf K}$ 对称，$\mathbf K$ 在内部自由度上正定时 $\tilde{\mathbf K}$ 正定，CG 仍适用。迭代初值取 $\boldsymbol x_0=\bar{\boldsymbol u}$，由调用方显式传入。

两种做法都有框架实现：对称消元见 [[../../literature/fem-libraries/translations/Anderson2021-MFEM-modular-library-zh|Anderson et al. (2021)]] §5.2、§6，投影包装见 [[../../literature/fem-libraries/translations/Brown2021-libCEED-fast-algebra-zh|Brown et al. (2021)]] 算子分解一节。

并行下对称消元在 true-DOF 系统 $\mathbf P^{\mathsf T}\mathbf K\mathbf P$ 上做；LA 若在各 rank 的局部矩阵上消元，经 $\mathbf P^{\mathsf T}$ 归约后 Dirichlet 行的对角为副本数 $r_i$ 而非 1，右端同乘 $r_i$，解不变。

## 5. 框架术语映射

| 框架 | Matrix-Free 入口 | 在五级分类中的理解 |
|---|---|---|
| [libCEED](https://libceed.org/en/latest/libCEEDapi/) | `TA/LA/EA/QA/UA` | 五级分类的主要术语来源 |
| [MFEM](https://mfem.org/howto/assembly_levels/) | `FULL/ELEMENT/PARTIAL/NONE` | 分别对应 FA/EA/PA/UA；LA 没有独立 `AssemblyLevel` |
| [deal.II](https://dealii.org/developer/doxygen/deal.II/classFEEvaluation.html) | `MatrixFree`、`FEEvaluation` | 高阶 Matrix-Free 算子作用；按实际缓存对象判断 PA 或 UA |
| [PETSc](https://petsc.org/main/manualpages/Mat/MATSHELL/) | `MATSHELL` | 通用 Shell Operator 接口，不代表具体装配层级 |
| [Firedrake](https://www.firedrakeproject.org/matrix-free.html) | `mat_type="matfree"`、`ImplicitMatrix` | 隐式算子作用；仍需检查底层保存对象 |
| [DOLFINx](https://docs.fenicsproject.org/dolfinx/main/python/demos/demo_matrix-free-petsc.html) | PETSc `SHELL` | 可构造不形成 `MATAIJ` 的算子作用，Shell 本身不是装配层级 |
| [NGSolve](https://docu.ngsolve.org/latest/i-tutorials/unit-3.5.1-dgapply/dgapply-scalar.html) | `nonassemble=True` | 不组装稀疏矩阵的算子作用；按实际保存对象分类 |

五级分类只作为跨框架比较坐标，具体实现仍应注明框架、原生入口和实际保存对象。MPI 分布方式（网格分区、true DOF 归属、ghost 更新、局部贡献归约）与装配层级是两个正交维度，MPI 可以分别与五级中任何一级组合，上述接口都不单独说明采用哪种分区与共享 DOF 协议；各框架的 owner/ghost 数据流见 [[../gpu-hpc/distributed-operator-and-shared-dofs]]。

## 参考文献

- [MFEM: Use partial assembly and matrix-free assembly](https://mfem.org/howto/assembly_levels/) — `FULL/ELEMENT/PARTIAL/NONE` 的官方定义。
- [MFEM: Performance and Partial Assembly](https://mfem.org/performance/) — PA 的 $\mathbf B^T\mathbf D\mathbf B$ 分解、积分点存储与 GPU 性能背景。
- [libCEED: Interface Concepts](https://libceed.org/en/latest/libCEEDapi/) — `TA/LA/EA/QA/UA` 的跨层存储分类。
- [PETSc: MATSHELL](https://petsc.org/main/manualpages/Mat/MATSHELL/) — Shell Matrix 是用户自定义数据结构和 MatVec 的接口。
- [[../../literature/fem-libraries/translations/Anderson2021-MFEM-modular-library-zh|Anderson et al. (2021)]]（`andersonMFEMModularFinite2021`）— §5.2 `FormLinearSystem` 与本质边界条件、§6 并行系统上的 Dirichlet 消元。
- [[../../literature/fem-libraries/translations/Brown2021-libCEED-fast-algebra-zh|Brown et al. (2021)]]（`brownLibCEEDFastAlgebra2021`）— 无矩阵算子作用前设置 Dirichlet 目标值。
