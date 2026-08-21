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
date_update: 2026-08-10
---

# Matrix-Free 装配层次

> **一句话**：Matrix-Free 不是单一实现，而是由“算子数据保存到哪一层”区分的实现谱系；本库统一采用兼容 libCEED 与 MFEM 的 `FA/TA → LA → EA/EbE → PA/QA → UA/NONE` 五级分类。

本页从已经离散的有限元算子出发，回答“程序预先形成和保存什么”。三维线弹性的
平衡方程、弱形式、向量 Lagrange 离散以及 $\mathbf K_e=\int_{\Omega_e}\mathbf B_e^{\mathsf T}\mathbf D\mathbf B_e\,\mathrm dx$ 如何产生，见 [[../linear-elasticity]]。

## 统一算子表示

有限元离散算子可抽象为

$$
\mathbf A
=
\mathbf P^T
\mathbf G^T
\mathbf B^T
\mathbf D
\mathbf B
\mathbf G
\mathbf P,
$$

- $\mathbf P$：并行 true DOF 与进程局部 DOF 的映射；
- $\mathbf G$：进程局部 DOF 与单元 DOF 的限制和回填；
- $\mathbf B$：单元自由度到积分点的插值或微分；
- $\mathbf D$：积分权重、几何 Jacobian、材料系数和积分点物理核。

一次典型算子作用可读作 `true DOF → local/element DOF → quadrature data → element/local DOF → true DOF`。“装配层次”描述上述因子中哪些乘积被提前计算并保存；不同软件的原生命名并不完全相同。

### 四层向量表示

上式的三个映射把同一个场依次表示得越来越冗余。这四层是本页的坐标系，五级分类和下文的“预计算前缘”都建立在它上面：

| 记号 | 名称 | 每个自由度出现次数 | 由谁到达 |
|---|---|---|---|
| T-vector | true DOF（真自由度） | 恰好 1 次 | — |
| L-vector | 进程局部 DOF | 每个持有它的 rank 各 1 份 | $\mathbf P$ |
| E-vector | 单元 DOF | 每个含有它的单元各 1 份 | $\mathbf G$ |
| Q-vector | 积分点数据 | 每单元每积分点各 1 份 | $\mathbf B$ |

**true DOF 的 “true” 是相对于“副本”，不是相对于“假”**：它是全局唯一、不重复计数的那一套未知量，$N_{\text{true}}$ 才是线性方程组的真实维数，而 $\sum_r n_r>N_{\text{true}}$。Krylov 方法的内积必须在 T 层的语义下进行，否则界面自由度会被重复计数。

**这一区分只在并行下有内容**：串行时 L 与 T 是同一个东西，$\mathbf P=\mathbf I$。$\mathbf G$ 与 $\mathbf B$ 则与是否并行无关。

其中 $\mathbf P$ 不只是一个抽象乘号：在 MPI 环境中，它具体涉及单元分区、owned/ghost 或重叠自由度、halo exchange、共享输入一致化、输出归约和全局内积。其数学定义与正确性不变量见 [[../gpu-hpc/distributed-operator-and-shared-dofs]]；本页只使用 T/L 的区分，不重复该页的通信协议与正确性条件。

> **记号对照**：本页的 $\mathbf P$ 就是 [[../gpu-hpc/distributed-operator-and-shared-dofs]] 中的 $\mathbf R_r$（该页按 rank 分别记，$\mathbf u_r=\mathbf R_r\mathbf u$）。注意两点易混：其一，该页的非粗体 $P$ 表示 rank 总数，与本页的映射 $\mathbf P$ 无关；其二，MFEM 惯例把 T→L 称作 prolongation、L→T 才称 restriction，与该页“限制矩阵”的叫法方向相反。以矩阵的实际方向为准。

## 五级分类

| 层级 | 本页规范名称 | 主要保存对象 | MatVec 的主要形式 | Matrix-Free 口径 |
|---|---|---|---|---|
| 1 | Full/True Assembly（FA/TA，全局/真自由度全组装） | 全局稀疏矩阵 $\mathbf A$ | 全局稀疏矩阵向量乘 | 不属于 Matrix-Free |
| 2 | Local Assembly（LA，进程局部组装） | 每个 MPI rank 的局部稀疏矩阵 | halo exchange + 局部稀疏矩阵向量乘 | 通常不属于 Matrix-Free |
| 3 | Element Assembly / Element-by-Element（EA/EbE，单元组装） | 稠密单元矩阵 $\mathbf A_e=\mathbf B_e^T\mathbf D_e\mathbf B_e$ | gather → $\mathbf A_e\mathbf x_e$ → scatter-add | 属于广义全局 Matrix-Free |
| 4 | Partial/Quadrature Assembly（PA/QA，部分/积分点组装） | 积分点数据 $\mathbf D_e$ 或等价 PA 数据 | gather → $\mathbf B_e$ → $\mathbf D_e$ → $\mathbf B_e^T$ → scatter-add | 现代高阶有限元的主流 Matrix-Free 路线 |
| 5 | Unassembled / Matrix-Free（UA/MF/NONE，无组装） | 不保存完整 $\mathbf A_e$，也不预存实质性的 $\mathbf D_e$ | 从几何和系数即时计算算子作用 | 严格意义的 fully Matrix-Free |

三个容易混淆的边界是：EA 保存完整单元矩阵；PA 只保存积分点或等价 PA 数据；UA 在每次 apply 时从几何、系数或状态即时计算这些数据。没有全局稀疏矩阵并不自动等于 PA 或 UA。

### 以主算子路径判定

若主算子路径缓存每个单元的完整稠密矩阵 $\mathbf A_e$，但不形成全局稀疏矩阵，则该路径属于 EA/EbE；若主路径只保存积分点数据或等价因子，则应判为 PA/QA；若这些数据在每次 MatVec 中即时生成，则应判为 UA/NONE。为调试或黄金对照另行构造的 FA/TA 算子不改变主路径的分类。分类依据是实际保存对象和 MatVec 数据流，而不是某种语言接口是否只暴露隐式算子调用。

## 装配层次的算子形式

### 因子链的块结构

统一算子表示中的四个因子都有块结构，五级分类正是建立在这个结构上：

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

$\mathbf G_e$ 是从进程局部自由度到单元 $e$ 自由度的布尔限制矩阵；$\mathbf B_e$ 和 $\mathbf D_e$ 按单元分块，$\mathbf D_e$ 再按积分点 $q$ 分块——积分点之间没有耦合，这是 PA/UA 能够成立的结构前提。$\mathbf G_e$ 与 MPI 层的 $\mathbf P$ 不同；后者见 [[../gpu-hpc/distributed-operator-and-shared-dofs]]。

代入统一表示并利用块结构，得到**五级共同的出发点**：

$$
\mathbf A
=\sum_{e=1}^{N_e}
\bigl(\mathbf G_e\mathbf P\bigr)^{\mathsf T}
\mathbf B_e^{\mathsf T}\mathbf D_e\mathbf B_e
\bigl(\mathbf G_e\mathbf P\bigr).
\tag{$\ast$}
$$

五级分类没有引入任何新的算子，全部是对 $(\ast)$ 的不同求值方式。

### 预计算前缘

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

装配层级就是在这条链上选一个**预计算前缘**：前缘以外的因子在 setup 阶段乘起来并保存，前缘以内的因子留到每次 apply 时执行。

| 层级 | 前缘位置 | setup 保存 | 每次 apply 执行 |
|---|---|---|---|
| FA/TA | 链的最外层 | $\mathbf P^{\mathsf T}\mathbf G^{\mathsf T}\mathbf B^{\mathsf T}\mathbf D\mathbf B\mathbf G\mathbf P$ | 无（只做一次 SpMV） |
| LA | $\mathbf P$ 之内 | $\mathbf G^{\mathsf T}\mathbf B^{\mathsf T}\mathbf D\mathbf B\mathbf G$ | $\mathbf P,\ \mathbf P^{\mathsf T}$ |
| EA/EbE | $\mathbf G$ 之内 | $\{\mathbf B_e^{\mathsf T}\mathbf D_e\mathbf B_e\}$ | $\mathbf P,\mathbf G,\ \mathbf G^{\mathsf T},\mathbf P^{\mathsf T}$ |
| PA/QA | $\mathbf B$ 之内 | $\{\mathbf D_e\}$ | $\mathbf P,\mathbf G,\mathbf B,\ \mathbf B^{\mathsf T},\mathbf G^{\mathsf T},\mathbf P^{\mathsf T}$ |
| UA/NONE | 链的最内层 | 几何与材料 | 全链，含 $\mathbf D_e$ 的即时构造 |

前缘位置**单调**控制的是两件事：前缘越靠内，setup 与 update 越便宜，每次 apply 需要重算的因子越多。

但**存储不是前缘位置的单调函数**，这一点极易误判。原因是“装配”这个动作同时做了两件性质不同的事：

1. **预计算**——把若干因子相乘并保存，增加存储、减少 apply 工作量；
2. **合并**——scatter-add 把落在同一全局位置的多份贡献相加，**减少**存储。

只有跨越 $\mathbf G$ 和 $\mathbf P$ 时才发生合并（多个单元、多个 rank 贡献同一个自由度）；跨越 $\mathbf B$ 和 $\mathbf D$ 时不发生。因此 FA 同时享有预计算与合并，EA 只保留了单元内的预计算而**放弃了合并**，其存储反而高于 FA（见下文 EA 一节的严格不等式）。真正的存储下降从 PA 才开始——那是往回撤预计算，而不是恢复合并。

换言之，存储—重算权衡在 EA → PA → UA 之间成立，而 FA/LA 属于另一个区间：它们省的是重复条目，不是重算。

以下逐级给出算子形式。为突出装配层级本身，$\mathbf P$ 在 EA 之后的各式中省略（可统一理解为把 $\mathbf G_e$ 替换为 $\mathbf G_e\mathbf P$）。

### FA/TA：全局矩阵作用

FA/TA 在 setup 阶段完成单元贡献的 scatter-add，形成并保存全局稀疏矩阵：

$$
\begin{aligned}
\mathbf A_{\mathrm{FA}}
&=
\sum_e
\mathbf G_e^{\mathsf T}
\mathbf A_e
\mathbf G_e,
\\
\mathbf y_{\mathrm{FA}}
&=
\mathbf A_{\mathrm{FA}}\mathbf x.
\end{aligned}
$$

这里的 $\mathbf G_e$ 已含 $\mathbf P$。全局矩阵在 true DOF 编号下形成，setup 之后 $\mathbf P,\mathbf G,\mathbf B,\mathbf D$ 全部可以释放——这是 FA 与其余四级最本质的区别：**只有 FA 的 apply 完全不需要网格**。

“FA” 与 “TA” 在本页并列使用：FA（Full Assembly）强调形成完整全局矩阵，TA（True Assembly）强调该矩阵建立在 true DOF 编号上。串行下两者无区别；并行下 TA 的措辞更准确，因为矩阵的行列索引必须是全局唯一编号。

#### setup 的两个动作

$\mathbf A_{\mathrm{FA}}=\sum_e\mathbf G_e^{\mathsf T}\mathbf A_e\mathbf G_e$ 这一步同时完成了两件应当分开理解的事：

- **预计算**：$\mathbf B_e^{\mathsf T}\mathbf D_e\mathbf B_e$ 的乘积被求出并保存；
- **合并**：多个单元落在同一个 $(i,j)$ 位置的贡献被加到一起，只保留一份。

第二件事决定了 FA 的稀疏模式：$(i,j)$ 非零当且仅当自由度 $i$ 与 $j$ 至少共享一个单元。因此非零数由自由度邻接图确定，

$$
\operatorname{nnz}(\mathbf A_{\mathrm{FA}})
=d^2\sum_{a=1}^{N_n}\bigl(\nu_a+1\bigr),
$$

其中 $\nu_a$ 为与节点 $a$ 共享单元的邻接节点数，$d$ 为每节点分量数（每个节点对贡献一个 $d\times d$ 块）。三维四面体网格上 $\nu_a$ 典型在 $10\sim15$，故三维向量 $P_1$ 每行约 $33\sim48$ 个非零。

#### apply 的真实瓶颈：算术强度

FA 的 apply 是一次 SpMV，浮点量为 $2\operatorname{nnz}$，看上去是五级中最少的。但 SpMV 的性能不由浮点量决定。以 CSR 为例，每个非零需要读取一个值（8 字节）和一个列索引（4 字节），换来一次乘和一次加：

$$
\text{算术强度}\;\approx\;\frac{2\ \text{flop}}{12\ \text{byte}}\;\approx\;0.17\ \text{flop/byte}.
$$

现代 CPU 与 GPU 的 machine balance（峰值算力／峰值带宽）远高于这个值，因此 **SpMV 是彻底的访存受限内核，只能达到峰值算力的很小比例**，且 $\mathbf x[\mathrm{col}[j]]$ 的间接寻址是随机访存，既不利于向量化也不利于缓存。

这是整条 Matrix-Free 路线的根本动机：**目标不是减少浮点运算，而是提高算术强度**——用重算换掉对大数组的读取。理解这一点之后，才能正确解读后面各级的收益，也才能避免用 flop 计数去论证 Matrix-Free 的优劣。

#### FA 不可替代的能力

FA 被排除在 Matrix-Free 之外，不等于它是落后选项。有些能力只有显式矩阵才提供：

- 稀疏直接法（LU、Cholesky、MUMPS 等），以及由此而来的鲁棒黄金参考解；
- 代数预条件（ILU、AMG）——它们需要矩阵元素本身，而不只是 MatVec；
- 谱与条件数分析、稀疏模式诊断；
- 作为其余四级的正确性对照：任何一级与 FA 的 MatVec 逐点比较都是最直接的实现判据。

因此本页把 FA 定位为**黄金参考**，而不是被淘汰的层级；主路径为 EA/PA/UA 时，另行构造 FA 用于对照不改变主路径的分类。

### LA：进程局部矩阵作用

LA 把求和切在 $\mathbf P$ 这一层：每个 rank $r$ 只对本进程的单元求和，形成局部稀疏矩阵，$\mathbf P$ 留到运行时：

$$
\mathbf A_{\mathrm L}^{(r)}
=\sum_{e\in\Omega_r}\mathbf G_e^{\mathsf T}\mathbf A_e\mathbf G_e,
\qquad
\mathbf y_{\mathrm{LA}}
=\mathbf P^{\mathsf T}\!\left[\mathbf A_{\mathrm L}^{(r)}\left(\mathbf P\mathbf x\right)\right].
$$

单元分区互不相交且完全覆盖时，$\sum_r \mathbf P_r\mathbf A_{\mathrm L}^{(r)}\mathbf P_r^{\mathsf T}=\mathbf A_{\mathrm{FA}}$，即 LA 与 FA 在精确算术下同样等价。

**LA 不是存储优化。** 各 rank 局部矩阵的非零总数不小于全局矩阵——界面自由度所在的行在多个 rank 上重复出现，因此 LA 的总存储略高于 FA。它的意义在别处：避免全局编号与集中存储、把 setup 局部化、并为区域分解型预条件（Schwarz、子结构）提供天然的局部代数对象。这是本页把 LA 列为“通常不属于 Matrix-Free”的原因——省略的是全局**编号**，不是全局**矩阵**。

### EA/EbE：单元矩阵作用

EA/EbE 不形成全局稀疏矩阵，而是保存单元矩阵集合 $\{\mathbf A_e\}$，在每次 MatVec 中直接计算

$$
\mathbf y_{\mathrm{EA}}
=
\sum_e
\mathbf G_e^{\mathsf T}
\left[
\mathbf A_e
\left(\mathbf G_e\mathbf x\right)
\right].
$$

EA 的算子作用可以进一步分解为

$$
\mathbf x_e=\mathbf G_e\mathbf x,
\qquad
\mathbf y_e=\mathbf A_e\mathbf x_e,
\qquad
\mathbf y_{\mathrm{EA}}=\sum_e\mathbf G_e^{\mathsf T}\mathbf y_e.
$$

其中三步依次为 gather、单元矩阵作用和 scatter-add。在精确算术下，EA 与 FA 表示同一个离散算子，即

$$
\mathbf y_{\mathrm{EA}}
=
\mathbf y_{\mathrm{FA}}.
$$

浮点计算中，两条路径可能因组装和求和顺序不同而产生舍入误差量级的数值差异，但这不改变二者的代数等价性。在线弹性问题中，$\mathbf A_e$ 对应单元刚度矩阵 $\mathbf K_e$，$\mathbf A_{\mathrm{FA}}$ 对应全局刚度矩阵 $\mathbf K$。

#### $\mathbf G_e$ 从不被实例化

$\mathbf G_e\in\{0,1\}^{m\times n}$ 写成矩阵只是为了让推导闭合。实现中它就是一个整数索引数组（单元到自由度映射）：$\mathbf G_e\mathbf x$ 是按索引取值（gather），$\mathbf G_e^{\mathsf T}\mathbf y_e$ 是按索引累加（scatter-add）。若真的形成 $\mathbf G_e$，其规模为 $m\times n$，EA 会比 FA 更费存储且毫无意义。这一点对 PA、UA 同样成立。

#### EA 不是存储优化

装配只会把多份贡献**合并**到同一位置，不会产生新位置。因此每个单元条目 $(\alpha,\beta)$ 都映射到某个全局位置 $(i,j)$，而多个单元条目可以映到同一位置，于是严格地有

$$
\operatorname{nnz}(\mathbf A_{\mathrm{FA}})\;\le\;\sum_e m_e^2\;=\;\text{EA 的存储量},
$$

**等号成立当且仅当任意两个单元不共享自由度**，即间断 Galerkin 一类的情形——此时全局矩阵本身就是块对角的，EA 与 FA 完全重合。对连续 Galerkin，不等式严格成立：

> **EA 的存储永远不小于 FA。**

三维线弹性 $P_1$ 四面体可以量化这个差距。设 $N_n$ 个节点、$N_e\approx 6N_n$ 个四面体，$m=12$，两侧一律按满存储计：

| | 每单元 | 存储量（doubles） |
|---|---|---|
| FA，按 $\nu_a\approx14$ 估计 | — | $\operatorname{nnz}=9\sum_a(\nu_a+1)\approx135\,N_n$ |
| EA | $m^2=144$ | $144N_e\approx864\,N_n$ |

即 EA 约为 FA 的 $6$ 倍。利用 $\mathbf A_e$ 与 $\mathbf A_{\mathrm{FA}}$ 的对称性可把两者各减约一半，相对关系不变。**在低阶单元上采用 EA，动机不可能是省存储。**

#### 那 EA 省的是什么

- **省掉全局装配这一步本身**：无需构造稀疏模式、无需排序与去重压缩成 CSR。setup 完全按单元并行，没有全局同步点；
- **update 便宜**：材料或设计变量改变时只重算 $\mathbf A_e$，稀疏结构无须重建（见后文 update 成本一节）；
- **访存模式规则**：$\mathbf A_e\mathbf x_e$ 是小稠密 GEMV，数据连续、可向量化，不含 CSR 的随机间接寻址（间接寻址被推到 gather/scatter 两端）；
- **通往 PA/UA 的阶梯**：EA 已经建立了 gather → 单元作用 → scatter-add 的完整数据流与边界处理语义，PA 只需把中间一步替换为 $\mathbf B_e^{\mathsf T}\mathbf D_e\mathbf B_e$ 的因子化作用。

#### scatter-add 的写竞态

$\mathbf G_e^{\mathsf T}$ 是 EA 唯一的非平凡并行难点：多个单元会写同一个全局自由度。串行下这只是顺序累加，并行下必须处理写冲突，常见三种做法是原子加、单元着色（同色单元互不共享自由度，可无冲突并行）和按自由度归约（转置遍历，每个自由度收集其相邻单元的贡献）。三者在 GPU 上的性能差异很大，且都不改变代数结果。这是 EA 实现的核心工程问题，与装配层级的定义无关。

#### 算术强度：EA 并没有解决 FA 的瓶颈

按 FA 一节的口径估算：EA 的 apply 每单元读取 $m^2$ 个 double（$8m^2$ 字节）并执行 $2m^2$ 次浮点运算，

$$
\text{算术强度}\;\approx\;\frac{2m^2\ \text{flop}}{8m^2\ \text{byte}}\;=\;0.25\ \text{flop/byte},
$$

与 SpMV 的 $0.17$ 同量级。EA 改善的是访存的**规则性**（连续块读取而非随机间接寻址），不是访存的**总量**——每次 apply 仍要把全部 $\{\mathbf A_e\}$ 从内存流过一遍，而这个数组还比 FA 的矩阵更大。

因此，**EA 是精确的 Matrix-Free 基线，但不是性能路线的终点**。真正提高算术强度必须减少每次 apply 所读取的数据量，也就是不再保存 $\mathbf A_e$——这正是 PA/QA 与 UA/NONE 的动机。

### PA/QA：积分点数据作用

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
\right],
$$

五步依次为 gather、$\mathbf B_e$ 插值/求导、积分点上的逐点作用、$\mathbf B_e^{\mathsf T}$ 回代和 scatter-add。中间一步没有任何积分点间的耦合——这正是 $\mathbf D=\operatorname{blkdiag}(\mathbf D_{e,q})$ 的块结构，也是 PA 在 GPU 上天然并行的原因。

PA 成立的前提是 $\mathbf B_e$ **不需要保存**，即它能从参考单元数据与单元几何现算。这依赖两层分解，必须分清：

**第一层（对任意单元类型成立）**：由链式法则 $\nabla_{\boldsymbol x}=\mathbf J_e^{-\mathsf T}\nabla_{\hat{\boldsymbol x}}$，

$$
\mathbf B_e=\boldsymbol\Gamma(\mathbf J_e)\,\hat{\mathbf B},
$$

其中 $\hat{\mathbf B}$ 是参考单元上的常量矩阵，**全网格只存一份**；$\boldsymbol\Gamma(\mathbf J_e)$ 由该单元的 Jacobian 决定。因此 PA 的每单元存储只有 $\mathbf D_e$ 与几何因子。

**第二层（只在张量积单元上存在）**：$\hat{\mathbf B}$ 可再写成一维算子的 Kronecker 积

$$
\hat{\mathbf B}=\hat{\mathbf B}_{1\mathrm D}\otimes\cdots\otimes\hat{\mathbf B}_{1\mathrm D}
\quad(d\ \text{个因子}),
$$

于是 $\hat{\mathbf B}\mathbf x_e$ 可按维度逐次作用，这就是 **sum factorization**。

这两层的区分决定了 PA 的收益边界。设 $d$ 维张量积单元、阶 $p$、每方向 $q\approx p+1$ 个积分点，则单元自由度 $m=(p+1)^d$、积分点数 $n_q=q^d$：

| | 每单元存储 | 每单元 apply 代价 |
|---|---|---|
| EA | $O(m^2)=O(p^{2d})$ | $O(m^2)=O(p^{2d})$ |
| PA，朴素作用 $\hat{\mathbf B}$ | $O(n_q)=O(p^{d})$ | $O(n_q m)=O(p^{2d})$ |
| PA + sum factorization | $O(n_q)=O(p^{d})$ | $O(d\,q\,m)=O(d\,p^{d+1})$ |

即：**PA 的存储优势对任意单元成立，计算优势只在张量积单元加 sum factorization 下成立。** 计算加速比为 $p^{2d}/p^{d+1}=p^{\,d-1}$：$d=3$ 时 $p=1$ 给出 $1$（毫无收益），$p=8$ 给出 $64$。PA 本质上是高阶方法的技术。

低阶单纯形上这一点尤其明显。以三维线弹性 $P_1$ 四面体为例，$m=12$，$\mathbf B_e\in\mathbb R^{6\times12}$ 为常量、单点积分即精确：

- EA 存 $\mathbf A_e$：$m^2=144$ 个数；
- PA 存 $w\lvert\det\mathbf J_e\rvert\,\mathbf D_e$（$6\times6$，即 $36$）加 $\mathbf J_e^{-1}$（$9$）：$45$ 个数；各向同性时 $\mathbf D_e$ 由 $(\lambda_e,\mu_e)$ 两个数确定，降到 $11$ 个数；
- 浮点代价两者同为 $O(m^2)$ 量级。

结论：低阶单纯形上 PA 相对 EA 是**存储优化而非计算优化**。在这类网格上推进 PA/QA，正确的目标是打通 $\mathbf B$–$\mathbf D$ 数据流与接口语义，而不是期待 kernel 加速。

把 FA 一节的基线一并代入（$N_e\approx6N_n$，一律满存储），同一个 $P_1$ 四面体问题的持久存储排序为：

| | 每单元 | 总量（doubles） |
|---|---|---|
| PA，各向同性 | $11$ | $\approx 66\,N_n$ |
| FA | — | $\approx 135\,N_n$ |
| PA，一般各向异性 | $45$ | $\approx 270\,N_n$ |
| EA | $144$ | $\approx 864\,N_n$ |

即在低阶单纯形上，只有各向同性 PA 的存储真正低于 FA，EA 和一般 PA 都更高。**低阶网格上 Matrix-Free 的存储收益本身就很有限**，这与 PA 是高阶技术的结论互为印证；把 Matrix-Free 的价值主张建立在低阶问题的存储节省上是站不住的。

### UA/NONE：即时生成的算子作用

UA/NONE 连 $\mathbf D_e$ 也不保存，在每次 apply 内从单元几何节点 $\mathbf X_e$、材料或设计变量 $\boldsymbol\rho_e$ 及当前状态即时构造：

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
\right],
$$

其中 $\mathbf J_e$、$\det\mathbf J_e$、$\mathbf J_e^{-1}$ 与材料张量全部进入 apply 内部。持久存储降到网格本身加每单元的设计/材料变量。

UA 相对 PA 多出的是 Jacobian 求逆与行列式的重复计算。它在加速器上通常比在 CPU 上更有吸引力：现代加速器的瓶颈多在访存带宽而非浮点吞吐，把 $\mathbf D_e$ 从“读”改为“算”提高了算术强度，在带宽受限区间是净收益。这条推理是定性的、且与具体硬件和问题规模相关，不能替代实测。

### update 成本：静态问题看不见的一维

以上各级只比较了 setup 存储与 apply 代价。在材料分布随迭代变化的问题（如拓扑优化，$\mathbf D_e$ 依赖设计变量 $\rho_e$）中还有第三项：**每次设计更新后重建算子的成本**。

$$
\rho_e\ \text{改变}\;\Longrightarrow\;\mathbf D_e\ \text{改变}\;\Longrightarrow\;
\begin{cases}
\text{FA/LA：重新组装全局或局部稀疏矩阵}\\
\text{EA：重算全部 }\mathbf A_e=\mathbf B_e^{\mathsf T}\mathbf D_e\mathbf B_e\\
\text{PA：只重算 }\mathbf D_e\\
\text{UA：无 update 成本，}\rho_e\ \text{直接进 apply}
\end{cases}
$$

**装配层级越低，update 成本越低。** 在单次求解的基准测试里这一维完全不可见，但在优化循环中它与 apply 成本同量级，是判断 Matrix-Free 是否真正划算的必要项——性能报告必须分别列出 setup、update、apply 与完整 solve。

### 三条跨层级不变量

**1. 精确算术下五级等价。** 五级都是 $(\ast)$ 的不同求值方式，因此表示同一个离散算子。浮点下的差异来自求和与组装顺序，属舍入误差量级，不改变代数等价性。这使得任意两级之间的 MatVec 逐点比较可以作为实现正确性判据，其容差应按舍入量级而非算法精度设定。

**2. 对称正定性沿链自动保持。** $(\ast)$ 的每一项都是 $\mathbf M_e^{\mathsf T}\mathbf D_e\mathbf M_e$ 的形式（$\mathbf M_e=\mathbf B_e\mathbf G_e\mathbf P$）。$\mathbf D_e$ 对称（半）正定时每项对称（半）正定，其和亦然。因此 CG 一类要求对称正定的 Krylov 方法的适用性**与装配层级无关**，不需要逐级重新论证；逐级仍要验证的是实现，不是数学。

**3. 对角线与子块的可及性随层级下降而递减。** 预条件器需要的不只是 MatVec：

| 层级 | $\operatorname{diag}(\mathbf A)$ | 非对角子块 |
|---|---|---|
| FA/LA | 直接读取 | 直接读取 |
| EA | $\operatorname{diag}(\mathbf A)=\sum_e\mathbf G_e^{\mathsf T}\operatorname{diag}(\mathbf A_e)$，一次 scatter-add | 可从 $\mathbf A_e$ 取出 |
| PA/UA | 以 $\mathbf M_e=\mathbf B_e\mathbf G_e\mathbf P$ 记，$A_{ii}=\sum_e\sum_{\alpha,\beta}(\mathbf M_e)_{\alpha i}(\mathbf D_e)_{\alpha\beta}(\mathbf M_e)_{\beta i}$，即 $\mathbf M_e$ 各列在 $\mathbf D_e$ 度量下的自内积，需专门 kernel，代价约一次 apply | 不可直接获得 |

这解释了为什么 Jacobi 在所有层级都可用，而块 Jacobi、ILU 以及依赖 strength-of-connection 的 AMG 在 PA/UA 下无法直接构造——**装配层级约束的不是求解器，是预条件器**。这也是下一节“算子与预条件器可以采用不同层级”的根本原因：主算子取 PA/UA 换存储，预条件器另取一个能提供所需代数信息的层级（对角、低阶组装代理、几何多重网格）。

### 存储与代价总表

按每单元计，$m$ 为单元自由度数，$n_q$ 为积分点数，$s$ 为每积分点的 $\mathbf D$ 独立分量数：

| 层级 | 持久存储 | apply 代价 | update 成本 | $\operatorname{diag}$ 可及性 |
|---|---|---|---|---|
| FA/TA | 全局稀疏矩阵非零 | 一次 SpMV | 重新组装 | 直接 |
| LA | 局部稀疏矩阵非零（总量 $\ge$ FA） | SpMV + halo | 重新组装 | 直接 |
| EA/EbE | $O(m^2)$ | $O(m^2)$ | 重算 $\mathbf A_e$ | 一次 scatter-add |
| PA/QA | $O(n_q s)$ | $O(n_q m)$，张量积单元可降至 $O(d\,q\,m)$ | 重算 $\mathbf D_e$ | 专门 kernel |
| UA/NONE | 几何 + 材料 | PA 代价 + $\mathbf D_e$ 构造 | 无 | 专门 kernel |

两点读表须知。其一，FA/LA 的存储是全局量、EA/PA/UA 是每单元量，**同列不可直接比较**；换算到同一问题后的实际排序见 PA 一节末尾的 $P_1$ 四面体对照表。其二，apply 代价一列是浮点计数，而 FA 与 EA 都是访存受限的，浮点少不等于快——判断性能必须看算术强度而非 flop（见 FA 与 EA 各自的算术强度小节）。

## 本质边界条件在各层级下的施加

Dirichlet 条件的施加方式**依赖装配层级**，是五级分类少数几个直接改变实现形态的地方。

记 $\boldsymbol\Pi_D$、$\boldsymbol\Pi_I$ 为 Dirichlet 自由度与内部自由度上的对角投影，$\boldsymbol\Pi_D+\boldsymbol\Pi_I=\mathbf I$；$\bar{\boldsymbol u}$ 为边界取给定值、内部取零的基准向量。**$\boldsymbol\Pi$ 与本页表示 MPI true/local 映射的 $\mathbf P$ 无关**，两者不可混用。

**FA/LA：改写矩阵。** 全局或进程局部稀疏矩阵已经形成，可以直接对 Dirichlet 行列做对称消元。

**EA/PA/UA：改写算子。** 没有可改写的矩阵，只能把原算子包成投影形式：

$$
\tilde{\mathbf A}=\boldsymbol\Pi_I\mathbf A\boldsymbol\Pi_I+\boldsymbol\Pi_D,
\qquad
\tilde{\boldsymbol b}=\boldsymbol\Pi_I\bigl(\boldsymbol b-\mathbf A\bar{\boldsymbol u}\bigr)+\boldsymbol\Pi_D\bar{\boldsymbol u}.
$$

即每次 apply 执行「置零 → 作用 → 还原」：Dirichlet 分量进入 $\mathbf A$ 前被清零，在输出中被恒等替换。

三点性质：

- $\tilde{\mathbf A}$ 对称；$\mathbf A$ 在内部自由度上正定时 $\tilde{\mathbf A}$ 正定，故 CG 仍适用——与[[#三条跨层级不变量|不变量 2]]一致，施加边界不改变 Krylov 方法的适用性。
- 两种做法给出**同一个线性系统**。这是跨层级解一致判据得以成立的前提，而不是一个可有可无的巧合。
- 迭代初值取 $\boldsymbol x_0=\bar{\boldsymbol u}$（已满足边界值），应由调用方显式传入，而非依赖算子内部状态。

### 并行下 FA 的对称消元不成立

在对等重叠副本表示（见 [[../gpu-hpc/distributed-operator-and-shared-dofs]]）下，对称消元发生在矩阵装配**之后**，跨 rank 同步归约 $\mathcal S$ 没有插入点。多 rank 下若沿用 FA 加对称消元，各 rank 会在自己的局部矩阵上求解，**不报错但结果错误**。串行时所有 $\mathcal S$ 退化为恒等，该问题不出现——这是一个只在并行下暴露的静默错误，实现应显式拒绝该组合，而不是留给使用者判断。

## 跨层级正确性判据

[[#三条跨层级不变量|不变量 1]]说五级在精确算术下等价，因此任意两级可以互为参照。本节给出把它落成可执行检查的标准形式。**具体阈值不在本页维护**，由实现仓库的契约持有（如 `soptx:examples/matrix_free_elasticity/utils/contract.py`）；两侧不得各存一份字面量。

设 $\boldsymbol\xi,\boldsymbol\eta$ 为固定随机种子生成的向量，$L_1,L_2$ 为两个装配层级。

| 判据 | 形式 | 检验对象 |
|---|---|---|
| 裸 MatVec 一致 | $\lVert\mathbf A^{(L_1)}\boldsymbol\xi-\mathbf A^{(L_2)}\boldsymbol\xi\rVert/\lVert\mathbf A^{(L_2)}\boldsymbol\xi\rVert$ | 因子链的求值路径 |
| 边界后 MatVec 一致 | 同上，$\mathbf A\to\tilde{\mathbf A}$ | 边界施加两种方式的等价性 |
| 算子对称正定 | $a=\boldsymbol\xi^{\mathsf T}\tilde{\mathbf A}\boldsymbol\eta$、$b=\boldsymbol\eta^{\mathsf T}\tilde{\mathbf A}\boldsymbol\xi$，取 $\lvert a-b\rvert/\max(\lvert a\rvert,\lvert b\rvert)$；另验 $\boldsymbol\xi^{\mathsf T}\tilde{\mathbf A}\boldsymbol\xi>0$ | [[#三条跨层级不变量\|不变量 2]] 的实现侧验证 |
| 解一致 | 迭代解与 FA 上直接法解的相对差 | 完整 solve，而非单次作用 |
| 收敛阶 | $E_k=\lVert\boldsymbol u_h^{(k)}-\boldsymbol u\rVert_{L^2}/\lVert\boldsymbol u\rVert_{L^2}$，相邻网格二等分时 $q_k=\log_2(E_{k-1}/E_k)$ | 离散本身，与装配层级无关 |

两点是 Matrix-Free 特有的，必须点明：

1. **对称性只能用双线性配对检验，不能逐元素比较矩阵**——EA 及以下层级根本不存在可逐元素比较的对象。这是正确性判据在低装配层级下必须改写形式的典型例子，也是[[#三条跨层级不变量|不变量 3]]（代数信息可及性递减）在测试侧的直接后果。
2. **MatVec 一致不替代完整 solve**。逐点比较只覆盖一次算子作用；真残差、边界误差和解误差是彼此独立的门禁，缺一不可。

容差应按舍入误差量级设定而非按算法精度（[[#三条跨层级不变量|不变量 1]]）。参照解只有 FA 能提供，这正是[[#FA 不可替代的能力|FA 作为黄金参考]]的用途所在。

## 框架术语映射

| 框架 | Matrix-Free 入口 | 在五级分类中的理解 |
|---|---|---|
| [libCEED](https://libceed.org/en/latest/libCEEDapi/) | `TA/LA/EA/QA/UA` | 五级分类的主要术语来源 |
| [MFEM](https://mfem.org/howto/assembly_levels/) | `FULL/ELEMENT/PARTIAL/NONE` | 分别对应 FA/EA/PA/UA；LA 没有完全对应的独立 `AssemblyLevel` |
| [deal.II](https://dealii.org/developer/doxygen/deal.II/classFEEvaluation.html) | `MatrixFree`、`FEEvaluation` | 提供高阶 Matrix-Free 算子作用；应按实际缓存对象继续判断 PA 或 UA |
| [PETSc](https://petsc.org/main/manualpages/Mat/MATSHELL/) | `MATSHELL` | 通用 Shell Operator 接口，不代表具体装配层级 |
| [Firedrake](https://www.firedrakeproject.org/matrix-free.html) | `mat_type="matfree"`、`ImplicitMatrix` | 提供隐式算子作用；仍需检查底层保存对象和执行路径 |
| [DOLFINx](https://docs.fenicsproject.org/dolfinx/main/python/demos/demo_matrix-free-petsc.html) | PETSc `SHELL` | 可构造不形成 `MATAIJ` 的算子作用，但 Shell 本身不是装配层级 |
| [NGSolve](https://docu.ngsolve.org/latest/i-tutorials/unit-3.5.1-dgapply/dgapply-scalar.html) | `nonassemble=True` | 支持不组装稀疏矩阵的算子作用；仍需根据实际保存对象分类 |

“五级分类”只作为跨框架比较坐标，具体实现仍应注明框架、原生入口和实际保存对象。`MATSHELL`、`ImplicitMatrix`、`nonassemble=True` 或自定义 `operator.apply()` 只能证明采用了隐式算子接口，不能单独决定其属于 EA、PA 还是 UA。

这里还必须把两个正交维度分开：

- **MPI 分布方式**回答网格如何分区、谁拥有 true DOF、ghost 如何更新以及局部贡献如何归约；
- **装配层级**回答每个 rank 为一次算子作用预先保存了全局矩阵、局部矩阵、单元矩阵、积分点数据还是更少的数据。

因此，MPI 可以分别与 FA、LA、EA、PA 或 UA 组合。PETSc `MATSHELL`、Firedrake `mat_type="matfree"` 和 NGSolve `nonassemble=True` 都不能单独说明采用哪种 MPI 分区与共享 DOF 协议。各框架的 owner/ghost 数据流及其与对等重叠副本代数的关系见 [[../gpu-hpc/distributed-operator-and-shared-dofs#13. 与主流有限元框架的对应|分布式框架对应表]]。

## 快速识别流程

按以下顺序判断一个实现的装配层次：

1. 是否保存全局或 true-DOF 稀疏矩阵？是则为 FA/TA。
2. 是否仅在每个 MPI rank 保存局部稀疏矩阵？是则为 LA。
3. 是否为每个单元保存完整稠密矩阵 $\mathbf A_e$？是则为 EA/EbE。
4. 是否只保存积分点 $\mathbf D_e$ 或等价 PA 数据？是则为 PA/QA。
5. $\mathbf D_e$ 是否在每次 MatVec 中从几何、系数或当前状态即时计算？是则为 UA/NONE。

## 算子与预条件器可以采用不同层级

Matrix-Free 通常只描述主算子路径，预条件器可以使用另一装配层级。例如，主算子使用 PA，预条件器可以使用对角、块对角或低阶组装代理。因此，性能报告必须分别注明 operator level、preconditioner level，以及 setup、update、apply 和完整 solve 成本。

其代数根据是[[#三条跨层级不变量|不变量 3]]：装配层级决定哪些代数信息还能被直接读取，而预条件器需要的往往不止 MatVec。主算子降到 PA/UA 换取存储后，预条件器必须另找一个能提供对角、子块或粗空间的来源，这不是工程妥协而是结构约束。

## 易混淆案例：Ma2026

[[../../literature/topology-opt/notes/Ma2026-highperformanceparallel]] 将多尺度形函数 $\mathbf N^j$ 按需预测、用于形成子结构缩聚刚度后释放，并在粗网格求解后再次预测。这减少了辅助数据的持久存储，但子结构缩聚刚度仍显式形成，粗网格全局缩聚矩阵仍然组装。

因此，Ma2026 的全局缩聚求解按本页五级分类属于第 1 级 FA/TA；论文中的 `matrix-free` 是对辅助数据采用按需重计算的存储优化，不属于第 3—5 级的算子级 Matrix-Free。完整方法边界和后续团队成果更新见 [[method-lineage]]。

## 来源与证据

- [MFEM: Use partial assembly and matrix-free assembly](https://mfem.org/howto/assembly_levels/) — `FULL/ELEMENT/PARTIAL/NONE` 的官方定义。
- [MFEM: Performance and Partial Assembly](https://mfem.org/performance/) — PA 的 $\mathbf B^T\mathbf D\mathbf B$ 分解、积分点存储与 GPU 性能背景。
- [libCEED: Interface Concepts](https://libceed.org/en/latest/libCEEDapi/) — `TA/LA/EA/QA/UA` 的跨层存储分类。
- [PETSc: MATSHELL](https://petsc.org/main/manualpages/Mat/MATSHELL/) — Shell Matrix 是用户自定义数据结构和 MatVec 的接口。

## 相关页面

- [[_index]] — Matrix-Free 稳定方法理解的子知识库入口。
- [[../linear-elasticity]] — 线弹性连续模型、变分形式、有限元离散与单元刚度算子。
- [[../gpu-hpc/distributed-operator-and-shared-dofs]] — MPI 网格分区、共享自由度同步、加权内积与全局解收集。
- [[method-lineage]] — 郭旭老师团队公开 Matrix-Free 相关成果的方法谱系。
- [[../../research/technical-lines/matrix-free-research-guide]] — 长期能力边界、阶段模型与统一验收原则。
- [[../../research/technical-lines/matrix-free-research-guide#五、阶段门禁与当前执行状态]] — 当前任务状态、推进顺序与完成记录。
- [[../../research/technical-lines/gpu-hpc-research-guide]] — GPU/HPC 技术线的性能边界、证据锚点与阶段门禁；本页只给 setup/update/apply 的代价结构，端到端计时口径由该线维护。
- [[../gpu-hpc/reference-libraries/fealpy-mfem-gpu-backend-comparison]] — MFEM/FEALPy 的 GPU 后端设计对比（装配层级与编程模型正交）。
- [[../../research/piml-matrix-free-gpu/high-performance-solver-survey]] — PIML、Matrix-Free 与 GPU 三条技术线组合后的方法关系、开放问题与研究切入点。
- [[../../discussions/guo-xu/first-formal-work-report]] — 面向郭旭老师的阶段表达快照，引用本页的装配层级口径；不反向覆盖本页定义。
