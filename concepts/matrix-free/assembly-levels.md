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
date_update: 2026-09-04
---

# Matrix-Free 装配层次

> Matrix-Free 是由“算子数据保存到哪一层”区分的实现谱系，按 libCEED 与 MFEM 兼容的口径分为 `FA/TA → LA → EA/EbE → PA/QA → UA/NONE` 五级。

## 1. 统一算子表示

### 1.1 串行

有限元离散算子可写成

$$
\mathbf A
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

两个映射把同一个场依次表示得越来越冗余：

| 记号 | 名称 | 每个自由度出现次数 | 由谁到达 |
|---|---|---|---|
| T-vector | 全局 DOF | 恰好 1 次 | — |
| E-vector | 单元 DOF | 每个含有它的单元各 1 份 | $\mathbf G$ |
| Q-vector | 积分点数据 | 每单元每积分点各 1 份 | $\mathbf B$ |

全局 DOF 的个数是线性方程组的维数，Krylov 方法的内积在这一层定义。

### 1.2 多进程并行

多线程与单卡 GPU 仍在同一地址空间内，每个自由度只有一份，算子保持 1.1 的形式，并行只体现在 $\mathbf G^{\mathsf T}$ 的 scatter-add 要处理写冲突。多进程（MPI）时地址空间被切开，每个 rank 只持有自己单元碰到的自由度，界面自由度在每个持有它的 rank 上各有一份副本。在最外层再套一个映射 $\mathbf P$：

$$
\mathbf A
=
\mathbf P^{\mathsf T}
\mathbf G^{\mathsf T}
\mathbf B^{\mathsf T}
\mathbf D
\mathbf B
\mathbf G
\mathbf P,
$$

$\mathbf P$ 把共享自由度复制给每个持有它的 rank，$\mathbf P^{\mathsf T}$ 把各 rank 的贡献相加，即 halo exchange；串行时 $\mathbf P=\mathbf I$。此时 $\mathbf G$ 作用在本 rank 的局部编号上，向量层次多出一层：

| 记号 | 名称 | 每个自由度出现次数 | 由谁到达 |
|---|---|---|---|
| T-vector | true DOF（全局自由度，不含副本） | 恰好 1 次 | — |
| L-vector | 进程局部 DOF | 每个持有它的 rank 各 1 份 | $\mathbf P$ |
| E-vector | 单元 DOF | 每个含有它的单元各 1 份 | $\mathbf G$ |
| Q-vector | 积分点数据 | 每单元每积分点各 1 份 | $\mathbf B$ |

true DOF 就是 1.1 的全局 DOF，“true”强调不含副本：$N_{\text{true}}$ 才是线性方程组的真实维数，Krylov 方法的内积必须在 T 层语义下进行，在 L 层直接求内积会把界面自由度重复计数。$\mathbf P$ 在 MPI 环境中涉及单元分区、owned/ghost 自由度、halo exchange 与全局内积，其数学定义与正确性不变量见 [[../gpu-hpc/distributed-operator-and-shared-dofs]]；该页按 rank 记作 $\mathbf R_r$，非粗体 $P$ 在该页表示 rank 总数，且 MFEM 惯例把 T→L 称作 prolongation、L→T 称作 restriction，与该页“限制矩阵”的叫法方向相反，以矩阵的实际方向为准。

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
\mathbf A
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

装配层级就是在这条链上选一个预计算前缘：前缘以外的因子在 setup 阶段乘起来并保存，前缘以内的因子留到每次 apply 执行。五级都是 $(\ast)$ 的不同求值方式，没有引入新算子。

| 层级 | setup 保存 | 每次 apply 执行 | Matrix-Free 口径 |
|---|---|---|---|
| Full/True Assembly（FA/TA） | 全局稀疏矩阵 $\mathbf P^{\mathsf T}\mathbf G^{\mathsf T}\mathbf B^{\mathsf T}\mathbf D\mathbf B\mathbf G\mathbf P$ | 一次 SpMV | 不属于 |
| Local Assembly（LA） | 每个 rank 的局部稀疏矩阵 $\mathbf G^{\mathsf T}\mathbf B^{\mathsf T}\mathbf D\mathbf B\mathbf G$ | $\mathbf P$、局部 SpMV、$\mathbf P^{\mathsf T}$ | 通常不属于 |
| Element Assembly / Element-by-Element（EA/EbE） | 稠密单元矩阵 $\{\mathbf A_e=\mathbf B_e^{\mathsf T}\mathbf D_e\mathbf B_e\}$ | gather、$\mathbf A_e\mathbf x_e$、scatter-add | 广义 Matrix-Free |
| Partial/Quadrature Assembly（PA/QA） | 积分点数据 $\{\mathbf D_e\}$ | gather、$\mathbf B_e$、$\mathbf D_e$、$\mathbf B_e^{\mathsf T}$、scatter-add | 高阶有限元的主流路线 |
| Unassembled（UA/NONE） | 几何与材料 | 全链，含 $\mathbf D_e$ 的即时构造 | 严格 fully Matrix-Free |

判定一份实现属于哪一级，看主算子路径实际保存的对象与 MatVec 数据流：保存全局或 true-DOF 稀疏矩阵为 FA/TA；只在各 rank 保存局部稀疏矩阵为 LA；为每个单元保存完整 $\mathbf A_e$ 为 EA；只保存 $\mathbf D_e$ 或等价数据为 PA；$\mathbf D_e$ 在每次 MatVec 中从几何、系数或状态即时计算为 UA。为调试或黄金对照另行构造的 FA 算子不改变主路径的分类。没有全局稀疏矩阵不自动等于 PA 或 UA，`MATSHELL`、`ImplicitMatrix`、`nonassemble=True` 或自定义 `operator.apply()` 只说明采用了隐式算子接口，不决定层级。

前缘位置单调控制两件事：前缘越靠内，setup 与 update 越便宜，每次 apply 需要重算的因子越多。存储却不是前缘位置的单调函数，因为“装配”同时做了两件不同的事：预计算把若干因子相乘并保存，增加存储、减少 apply 工作量；合并由 scatter-add 把落在同一全局位置的多份贡献相加，减少存储。合并只在跨越 $\mathbf G$ 和 $\mathbf P$ 时发生，跨越 $\mathbf B$ 和 $\mathbf D$ 时不发生。FA 同时享有预计算与合并；EA 保留了单元内的预计算但放弃了合并，存储反而高于 FA；真正的存储下降从 PA 开始，那是往回撤预计算，不是恢复合并。存储与重算的权衡在 EA → PA → UA 之间成立，FA/LA 省的是重复条目，不是重算。

以下逐级给出算子形式。为突出装配层级本身，$\mathbf P$ 在 EA 之后各式中省略，可统一理解为把 $\mathbf G_e$ 替换为 $\mathbf G_e\mathbf P$。

### 2.1 FA/TA：全局矩阵作用

FA/TA 在 setup 阶段完成单元贡献的 scatter-add，形成并保存全局稀疏矩阵：

$$
\mathbf A_{\mathrm{FA}}
=
\sum_e
\mathbf G_e^{\mathsf T}
\mathbf A_e
\mathbf G_e,
\qquad
\mathbf y_{\mathrm{FA}}
=
\mathbf A_{\mathrm{FA}}\mathbf x.
$$

这里的 $\mathbf G_e$ 已含 $\mathbf P$。全局矩阵在 true DOF 编号下形成，setup 之后 $\mathbf P,\mathbf G,\mathbf B,\mathbf D$ 全部可以释放，五级中只有 FA 的 apply 完全不需要网格。FA 强调形成完整全局矩阵，TA 强调该矩阵建立在 true DOF 编号上，串行下两者无区别，并行下 TA 的措辞更准确。

FA 的稀疏模式由合并决定：$(i,j)$ 非零当且仅当自由度 $i$ 与 $j$ 至少共享一个单元，

$$
\operatorname{nnz}(\mathbf A_{\mathrm{FA}})
=d^2\sum_{a=1}^{N_n}\bigl(\nu_a+1\bigr),
$$

其中 $\nu_a$ 为与节点 $a$ 共享单元的邻接节点数，$d$ 为每节点分量数。三维四面体网格上 $\nu_a$ 典型在 $10\sim15$，三维向量 $P_1$ 每行约 $33\sim48$ 个非零。

FA 的 apply 是一次 SpMV，浮点量 $2\operatorname{nnz}$ 是五级中最少的，但 SpMV 的性能不由浮点量决定。以 CSR 为例，每个非零读取一个值（8 字节）和一个列索引（4 字节），换来一次乘和一次加：

$$
\text{算术强度}\;\approx\;\frac{2\ \text{flop}}{12\ \text{byte}}\;\approx\;0.17\ \text{flop/byte}.
$$

现代 CPU 与 GPU 的 machine balance 远高于这个值，SpMV 是彻底的访存受限内核，且 $\mathbf x[\mathrm{col}[j]]$ 的间接寻址是随机访存。整条 Matrix-Free 路线的目标不是减少浮点运算，而是提高算术强度，用重算换掉对大数组的读取；用 flop 计数论证 Matrix-Free 的优劣是错的。

FA 被排除在 Matrix-Free 之外，不等于它是落后选项。稀疏直接法（LU、Cholesky、MUMPS）及由此而来的鲁棒黄金参考解、代数预条件（ILU、AMG）、谱与条件数分析、稀疏模式诊断都只有显式矩阵才提供；任何一级与 FA 的 MatVec 逐点比较是最直接的实现判据。本页把 FA 定位为黄金参考。

### 2.2 LA：进程局部矩阵作用

LA 把求和切在 $\mathbf P$ 这一层：每个 rank $r$ 只对本进程的单元求和，形成局部稀疏矩阵，$\mathbf P$ 留到运行时：

$$
\mathbf A_{\mathrm L}^{(r)}
=\sum_{e\in\Omega_r}\mathbf G_e^{\mathsf T}\mathbf A_e\mathbf G_e,
\qquad
\mathbf y_{\mathrm{LA}}
=\mathbf P^{\mathsf T}\!\left[\mathbf A_{\mathrm L}^{(r)}\left(\mathbf P\mathbf x\right)\right].
$$

单元分区互不相交且完全覆盖时 $\sum_r \mathbf P_r\mathbf A_{\mathrm L}^{(r)}\mathbf P_r^{\mathsf T}=\mathbf A_{\mathrm{FA}}$，LA 与 FA 在精确算术下等价。

LA 不是存储优化：界面自由度所在的行在多个 rank 上重复出现，局部矩阵非零总数不小于全局矩阵。它的意义是避免全局编号与集中存储、把 setup 局部化，并为 Schwarz、子结构等区域分解型预条件提供天然的局部代数对象。省略的是全局编号，不是全局矩阵，所以 LA 通常不算 Matrix-Free。

### 2.3 EA/EbE：单元矩阵作用

EA/EbE 不形成全局稀疏矩阵，保存单元矩阵集合 $\{\mathbf A_e\}$，每次 MatVec 按 gather、单元矩阵作用、scatter-add 三步计算：

$$
\mathbf x_e=\mathbf G_e\mathbf x,
\qquad
\mathbf y_e=\mathbf A_e\mathbf x_e,
\qquad
\mathbf y_{\mathrm{EA}}=\sum_e\mathbf G_e^{\mathsf T}\mathbf y_e
=\mathbf y_{\mathrm{FA}}.
$$

精确算术下 EA 与 FA 表示同一个离散算子，浮点下的差异来自求和顺序，属舍入误差量级。线弹性中 $\mathbf A_e$ 是单元刚度矩阵 $\mathbf K_e=\int_{\Omega_e}\mathbf B_e^{\mathsf T}\mathbf D\mathbf B_e\,\mathrm dx$，其弱形式与向量 Lagrange 离散见 [[../linear-elasticity]]。载体换成子结构、局部矩阵为缩聚刚度 $\mathbf K_s^j$ 的同构实例见 [[mf-ea-substructural|子结构载体 EA Matrix-Free 算子]]。

$\mathbf G_e\in\{0,1\}^{m\times n}$ 写成矩阵只是为了让推导闭合，实现中它是一个整数索引数组：$\mathbf G_e\mathbf x$ 是按索引取值，$\mathbf G_e^{\mathsf T}\mathbf y_e$ 是按索引累加。这一点对 PA、UA 同样成立。装配只会把多份贡献合并到同一位置，不会产生新位置，因此

$$
\operatorname{nnz}(\mathbf A_{\mathrm{FA}})\;\le\;\sum_e m_e^2\;=\;\text{EA 的存储量},
$$

等号成立当且仅当任意两个单元不共享自由度，即间断 Galerkin 的情形；对连续 Galerkin 不等式严格成立，EA 的存储永远不小于 FA。三维线弹性 $P_1$ 四面体上 EA 约为 FA 的 6 倍（数字见 PA 一节的对照表），利用对称性可把两者各减约一半，相对关系不变。在低阶单元上采用 EA，动机不可能是省存储。

$\mathbf G_e^{\mathsf T}$ 是 EA 唯一的非平凡并行难点：多个单元会写同一个全局自由度，串行下只是顺序累加，并行下必须处理写冲突。常见三种做法是原子加、单元着色（同色单元互不共享自由度，可无冲突并行）和按自由度归约（转置遍历，每个自由度收集其相邻单元的贡献）。三者在 GPU 上的性能差异很大，都不改变代数结果。

EA 的 apply 每单元读取 $m^2$ 个 double 并执行 $2m^2$ 次浮点运算，

$$
\text{算术强度}\;\approx\;\frac{2m^2\ \text{flop}}{8m^2\ \text{byte}}\;=\;0.25\ \text{flop/byte},
$$

与 SpMV 同量级。EA 改善的是访存的规则性（$\mathbf A_e\mathbf x_e$ 是连续的小稠密 GEMV，间接寻址被推到 gather/scatter 两端），不是访存的总量。EA 省掉的是全局装配这一步本身（无需构造稀疏模式、排序去重压成 CSR，setup 完全按单元并行）以及 update 的稀疏结构重建，并建立了 PA/UA 共用的 gather → 单元作用 → scatter-add 数据流与边界处理语义。它是精确的 Matrix-Free 基线，不是性能路线的终点；真正提高算术强度必须不再保存 $\mathbf A_e$。

### 2.4 PA/QA：积分点数据作用

PA/QA 连 $\mathbf A_e$ 都不形成，只保存积分点数据 $\mathbf D_e$：

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

中间一步没有任何积分点间的耦合，这是 PA 在 GPU 上天然并行的原因。PA 成立的前提是 $\mathbf B_e$ 不需要保存，能从参考单元数据与单元几何现算，这依赖两层分解。第一层对任意单元类型成立：由链式法则 $\nabla_{\boldsymbol x}=\mathbf J_e^{-\mathsf T}\nabla_{\hat{\boldsymbol x}}$，

$$
\mathbf B_e=\boldsymbol\Gamma(\mathbf J_e)\,\hat{\mathbf B},
$$

$\hat{\mathbf B}$ 是参考单元上的常量矩阵，全网格只存一份，每单元存储只有 $\mathbf D_e$ 与几何因子。第二层只在张量积单元上存在：

$$
\hat{\mathbf B}=\hat{\mathbf B}_{1\mathrm D}\otimes\cdots\otimes\hat{\mathbf B}_{1\mathrm D}
\quad(d\ \text{个因子}),
$$

$\hat{\mathbf B}\mathbf x_e$ 可按维度逐次作用，即 sum factorization。设 $d$ 维张量积单元、阶 $p$、每方向 $q\approx p+1$ 个积分点，单元自由度 $m=(p+1)^d$、积分点数 $n_q=q^d$：

| | 每单元存储 | 每单元 apply 代价 |
|---|---|---|
| EA | $O(m^2)=O(p^{2d})$ | $O(m^2)=O(p^{2d})$ |
| PA，朴素作用 $\hat{\mathbf B}$ | $O(n_q)=O(p^{d})$ | $O(n_q m)=O(p^{2d})$ |
| PA + sum factorization | $O(n_q)=O(p^{d})$ | $O(d\,q\,m)=O(d\,p^{d+1})$ |

PA 的存储优势对任意单元成立，计算优势只在张量积单元加 sum factorization 下成立，加速比 $p^{2d}/p^{d+1}=p^{\,d-1}$，$d=3$ 时 $p=1$ 给出 1，$p=8$ 给出 64。PA 本质上是高阶方法的技术。

三维线弹性 $P_1$ 四面体上，$m=12$，$\mathbf B_e\in\mathbb R^{6\times12}$ 为常量、单点积分即精确。EA 存 $\mathbf A_e$ 共 144 个数；PA 存 $w\lvert\det\mathbf J_e\rvert\,\mathbf D_e$（36 个）加 $\mathbf J_e^{-1}$（9 个）共 45 个数，各向同性时 $\mathbf D_e$ 由 $(\lambda_e,\mu_e)$ 确定，降到 11 个数；浮点代价两者同为 $O(m^2)$。取 $N_e\approx6N_n$、$\nu_a\approx14$，一律按满存储计：

| | 每单元 | 总量（doubles） |
|---|---|---|
| PA，各向同性 | $11$ | $\approx 66\,N_n$ |
| FA | — | $\operatorname{nnz}=9\sum_a(\nu_a+1)\approx135\,N_n$ |
| PA，一般各向异性 | $45$ | $\approx 270\,N_n$ |
| EA | $144$ | $\approx 864\,N_n$ |

低阶单纯形上只有各向同性 PA 的存储真正低于 FA，PA 相对 EA 是存储优化而非计算优化。在这类网格上推进 PA/QA 的目标是打通 $\mathbf B$–$\mathbf D$ 数据流与接口语义，不是 kernel 加速；把 Matrix-Free 的价值主张建立在低阶问题的存储节省上站不住。

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
\text{EA：重算全部 }\mathbf A_e=\mathbf B_e^{\mathsf T}\mathbf D_e\mathbf B_e\\
\text{PA：只重算 }\mathbf D_e\\
\text{UA：无 update 成本，}\rho_e\ \text{直接进 apply}
\end{cases}
$$

装配层级越低，update 成本越低。单次求解的基准测试看不见这一维，优化循环中它与 apply 成本同量级，性能报告必须分别列出 setup、update、apply 与完整 solve。

## 3. 三条跨层级不变量

精确算术下五级等价。五级都是 $(\ast)$ 的不同求值方式，表示同一个离散算子；浮点下的差异来自求和与组装顺序，属舍入误差量级。任意两级之间的 MatVec 逐点比较可以作为实现正确性判据，容差按舍入量级而非算法精度设定。

对称正定性沿链自动保持。$(\ast)$ 的每一项都是 $\mathbf M_e^{\mathsf T}\mathbf D_e\mathbf M_e$ 的形式（$\mathbf M_e=\mathbf B_e\mathbf G_e\mathbf P$），$\mathbf D_e$ 对称（半）正定时每项及其和亦然。CG 一类要求对称正定的 Krylov 方法的适用性与装配层级无关，逐级要验证的是实现，不是数学。

对角线与子块的可及性随层级下降而递减。预条件器需要的不只是 MatVec：

| 层级 | 持久存储 | apply 代价 | update 成本 | $\operatorname{diag}(\mathbf A)$ | 非对角子块 |
|---|---|---|---|---|---|
| FA/TA | 全局稀疏矩阵非零 | 一次 SpMV | 重新组装 | 直接读取 | 直接读取 |
| LA | 局部稀疏矩阵非零（总量 $\ge$ FA） | SpMV + halo | 重新组装 | 直接读取 | 直接读取 |
| EA/EbE | 每单元 $O(m^2)$ | $O(m^2)$ | 重算 $\mathbf A_e$ | $\sum_e\mathbf G_e^{\mathsf T}\operatorname{diag}(\mathbf A_e)$，一次 scatter-add | 可从 $\mathbf A_e$ 取出 |
| PA/QA | 每单元 $O(n_q s)$ | $O(n_q m)$，张量积单元可降至 $O(d\,q\,m)$ | 重算 $\mathbf D_e$ | $A_{ii}=\sum_e\sum_{\alpha,\beta}(\mathbf M_e)_{\alpha i}(\mathbf D_e)_{\alpha\beta}(\mathbf M_e)_{\beta i}$，需专门 kernel，代价约一次 apply | 不可直接获得 |
| UA/NONE | 几何 + 材料 | PA 代价 + $\mathbf D_e$ 构造 | 无 | 同 PA | 不可直接获得 |

$m$ 为单元自由度数，$n_q$ 为积分点数，$s$ 为每积分点 $\mathbf D$ 的独立分量数；FA/LA 的存储是全局量，EA/PA/UA 是每单元量，同列不可直接比较，换算到同一问题后的排序见 PA 一节的 $P_1$ 对照表；apply 一列是浮点计数，FA 与 EA 都是访存受限，判断性能看算术强度。Jacobi 在所有层级可用，块 Jacobi、ILU 以及依赖 strength-of-connection 的 AMG 在 PA/UA 下无法直接构造：装配层级约束的是预条件器，不是求解器。因此主算子与预条件器可以采用不同层级，主算子取 PA/UA 换存储，预条件器另取一个能提供对角、低阶组装代理或几何多重网格粗空间的层级；性能报告须分别注明 operator level、preconditioner level 以及 setup、update、apply 和完整 solve 成本。

## 4. 边界条件与正确性判据

Dirichlet 条件的施加方式依赖装配层级。记 $\boldsymbol\Pi_D$、$\boldsymbol\Pi_I$ 为 Dirichlet 自由度与内部自由度上的对角投影，$\boldsymbol\Pi_D+\boldsymbol\Pi_I=\mathbf I$，$\bar{\boldsymbol u}$ 为边界取给定值、内部取零的基准向量；$\boldsymbol\Pi$ 与 MPI 映射 $\mathbf P$ 无关。FA/LA 已经形成矩阵，可以直接对 Dirichlet 行列做对称消元。EA/PA/UA 没有可改写的矩阵，只能把原算子包成投影形式：

$$
\tilde{\mathbf A}=\boldsymbol\Pi_I\mathbf A\boldsymbol\Pi_I+\boldsymbol\Pi_D,
\qquad
\tilde{\boldsymbol b}=\boldsymbol\Pi_I\bigl(\boldsymbol b-\mathbf A\bar{\boldsymbol u}\bigr)+\boldsymbol\Pi_D\bar{\boldsymbol u},
$$

即每次 apply 执行「置零 → 作用 → 还原」。$\tilde{\mathbf A}$ 对称，$\mathbf A$ 在内部自由度上正定时 $\tilde{\mathbf A}$ 正定，CG 仍适用。两种做法给出同一个线性系统，这是跨层级解一致判据成立的前提。迭代初值取 $\boldsymbol x_0=\bar{\boldsymbol u}$，由调用方显式传入。

并行下 FA 的对称消元不成立。在对等重叠副本表示（见 [[../gpu-hpc/distributed-operator-and-shared-dofs]]）下，对称消元发生在矩阵装配之后，跨 rank 同步归约 $\mathcal S$ 没有插入点，各 rank 会在自己的局部矩阵上求解，不报错但结果错误；串行时所有 $\mathcal S$ 退化为恒等，该问题不出现。实现应显式拒绝该组合。

设 $\boldsymbol\xi,\boldsymbol\eta$ 为固定随机种子生成的向量，$L_1,L_2$ 为两个装配层级。具体阈值由实现仓库的契约持有（如 `soptx:examples/matrix_free_elasticity/utils/contract.py`），两侧不得各存一份字面量。

| 判据 | 形式 | 检验对象 |
|---|---|---|
| 裸 MatVec 一致 | $\lVert\mathbf A^{(L_1)}\boldsymbol\xi-\mathbf A^{(L_2)}\boldsymbol\xi\rVert/\lVert\mathbf A^{(L_2)}\boldsymbol\xi\rVert$ | 因子链的求值路径 |
| 边界后 MatVec 一致 | 同上，$\mathbf A\to\tilde{\mathbf A}$ | 边界施加两种方式的等价性 |
| 算子对称正定 | $a=\boldsymbol\xi^{\mathsf T}\tilde{\mathbf A}\boldsymbol\eta$、$b=\boldsymbol\eta^{\mathsf T}\tilde{\mathbf A}\boldsymbol\xi$，取 $\lvert a-b\rvert/\max(\lvert a\rvert,\lvert b\rvert)$；另验 $\boldsymbol\xi^{\mathsf T}\tilde{\mathbf A}\boldsymbol\xi>0$ | 不变量 2 的实现侧验证 |
| 解一致 | 迭代解与 FA 上直接法解的相对差 | 完整 solve |
| 收敛阶 | $E_k=\lVert\boldsymbol u_h^{(k)}-\boldsymbol u\rVert_{L^2}/\lVert\boldsymbol u\rVert_{L^2}$，相邻网格二等分时 $q_k=\log_2(E_{k-1}/E_k)$ | 离散本身，与装配层级无关 |

对称性只能用双线性配对检验，EA 及以下层级不存在可逐元素比较的矩阵。MatVec 一致不替代完整 solve，真残差、边界误差和解误差是彼此独立的门禁。参照解只有 FA 能提供。

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
