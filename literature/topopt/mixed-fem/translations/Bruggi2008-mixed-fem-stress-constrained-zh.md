---
title: "翻译：A mixed FEM approach to stress-constrained topology optimization"
tags:
  - translation
  - mixed-fem
  - topology-optimization
  - stress-constraints
status: "done"
date_created: 2026-09-08
date_updated: 2026-09-14
source: "../sources/Bruggi2008-mixed-fem-stress-constrained.pdf"
citekey: "Bruggi2008-mixedfem"
language: "zh-CN"
---

# A mixed FEM approach to stress-constrained topology optimization

> 原文 PDF：`../sources/Bruggi2008-mixed-fem-stress-constrained.pdf`；DOI：[10.1002/nme.2138](https://doi.org/10.1002/nme.2138)。
> 译文按原文章节、公式编号与图表编号逐段对应；译者说明以脚注标出。图件 `Bruggi2008_Fig1.png` 至 `Bruggi2008_Fig19.png` 与原刊图 1 至图 19 一一对应。

---

# 信息

- **中文标题**：应力约束拓扑优化的混合有限元方法
- **作者**：M. Bruggi；P. Venini（通讯作者，E-mail: paolo.venini@unipv.it）
- **单位**：Department of Structural Mechanics, University of Pavia, via Ferrata, 1, 27100 Pavia, Italy
- **期刊**：*International Journal for Numerical Methods in Engineering*
- **卷 / 期 / 页码**：第 73 卷，第 1693–1714 页；期号 PDF 首页未标注，待确认
- **DOI**：10.1002/nme.2138
- **在线发表 / 正式卷期**：2007-07-10 / 2008
- **收稿 / 修回 / 录用**：2006-09-21 / 2007-05-30 / 2007-06-01
- **基金**：MIUR PRIN-COFIN，2005–2006 年度

---

# 摘要

我们提出一种拓扑优化的替代格式，它能够以直接的方式处理应力约束。主要思想是采用混合有限元离散格式，其中不仅位移（如通常那样），应力也是进入格式的变量。这样一来，任何应力约束都可以在优化过程中处理，而不必借助基于位移方法所特有的后处理操作；若不对应力作光顺，这类后处理还可能造成应力计算精度的损失。文中给出两种 Hellinger–Reissner 型对偶变分原理的连续与离散形式，并将其纳入一个含应力约束的相当一般的拓扑优化问题，该问题用移动渐近线法求解（Int. J. Numer. Meth. Engng. 1984; 24(3):359–373）。进行了大量数值模拟，并概述了正在进行的推广，包括弹塑性介质与不可压缩介质的优化。

**关键词**：拓扑优化；混合有限元；应力约束

---

# 1 引言与研究动机

自开创性论文 [1] 把拓扑优化概念作为一种新颖而强有力的结构设计方法引入以来，该领域已在多个方向上取得进展；如今可以说，拓扑优化已是一门成熟的学科，在各种尺度的结构设计领域带来了概念与实践上的改进。从理论角度看，Bendsøe 与 Sigmund 的研究 [2] 可视为一个里程碑：它为 SIMP 方法（solid isotropic microstructure with penalization）给出了严格的论证；该方法此前虽已在文献中广泛使用，但在该文出现之前一直被认为与连续介质力学理论不一致。至于拓扑优化问题的适定性以及能够收敛到最优解的逼近序列的存在性，文献 [3] 是为数不多的贡献之一。文献中持续报道为成功的数值方法包括序列二次规划（SQP）[4]、凸线性化（CONLIN）[5] 和移动渐近线法（MMA）[6]；这里可以预先说明，本文的实现采用了 MMA，因为它相对于 SQP 表现出显著优势（不过我们迄今尚未测试 CONLIN 格式）。

从应用角度看，新的领域不断被开拓，从最初的线弹性结构设计走向材料设计或多物理场问题等新分支。这个简短的清单远不完整；关于拓扑优化领域的研究现状，请参阅 [7] 的综合论述，关于方法本身的现代而详尽的介绍，请参阅 [8]。

回到本文主题：关于应力约束桁架结构已有大量文献，而涉及二维情形的工作则不多。在优化结构中实施应力限制时遇到的最早问题之一，与满应力设计（Fully Stressed Design）方法密切相关。该方法的目标是得到一个最终设计，使结构的每个离散部分都使材料失效约束达到饱和，例如见 [9]。在最早引入应力约束的研究中，可参阅 [10]，它以内能与整个域上 von Mises 应力场 p-范数泛函的线性组合作为目标函数。Duysinx 与 Bendsøe [11] 在 SIMP 律的框架下处理应力约束的施加，基于微结构建模导出一组逐点的局部约束，并用常规非线性规划技术求解。由此产生的问题是，需要对强度极限采用关于密度变量的指数律插值，且指数与刚度插值所用的相同。作者还表明，把这类约束纳入最小重量拓扑优化格式时，最初在桁架设计中发现的奇异性现象在连续体情形同样出现。在二维情形，设计空间中退化附属区域的存在，表现为标准优化算法难以完全去除某些低密度区域。因此作者借助 ε-松弛技术削弱约束，以帮助最小化算法去除这些区域。

文献 [12] 提出了另一种方法，它借助增广拉格朗日技术把局部约束作为惩罚项纳入目标函数，从而减少逐点约束所需的计算量，同时给出了问题的另一种数值处理。出于同样目的，Duysinx 与 Sigmund [13] 最初提出只施加一个全局 $L^q$ 约束，当 $q$ 很大时它逼近局部约束。在关于该主题的最新贡献中，可参阅 [14] 提出的替代方法。该工作指出，属于非线性 0–1 拓扑优化问题类的应力约束最小重量问题可以改写为线性混合 0–1 问题。在这种建模下，由于应力约束的线性性，需要松弛技术来处理的非凸性消失了，从而可以采用分支定界、分支切割等全局最优化方法。

在这样的背景下，本文自然地立足于 [11] 所采用的方法，即在 SIMP 律框架下施加逐点约束，但本文方法具有明显不同的特征，主要体现在以下三点：

1. 用于逼近问题的空间离散格式。大多数应用采用经典的基于位移的有限元方法。这样做在数值上便于处理，但这种简单格式有两个主要缺点。一方面，应力不是格式的主变量，因此施加应力约束需要计算近似应变场，再通过所采用的本构律转换为应力场。其次，传统位移格式由于闭锁问题，无法模拟不可压缩等极端材料。
2. 众所周知的棋盘格问题，除非采取适当补救措施，否则很可能出现。传统上人们或多或少模仿图像处理领域的做法采用某种滤波 [15]；另一种依赖非协调有限元的方法也已被成功采用 [16]。
3. 奇异性问题，它可能妨碍所采用的最小化算法得到无灰色区域的可行解。应力约束拓扑优化领域的大多数现有工作实施所谓 ε-松弛，它源自 [17] 为桁架问题引入的著名策略。

本文的目的是提出一种基于混合有限元逼近格式的应力约束拓扑优化替代格式。采用 Hellinger–Reissner 变分原理，并提出两种对偶格式。第一种较为简单，可用经典多项式有限元逼近正则的位移场和分片间断的应力场；本文给出的结果来自该格式。第二种对偶格式在文献中常称为"真混合"（truly mixed）格式 [18]，其诱人之处在于即使对不可压缩材料也能通过 inf–sup 条件；相关结果（包括橡胶支座装置的最优设计）将在后续论文中给出。混合有限元离散与 [19] 引入的密度离散相耦合，后者已在基于位移的有限元框架下被证明能给出不含棋盘格的解。在该方法中，每个单元密度取为节点密度的平均值，而节点密度是最小化问题的主变量。至于应力奇异性的处理，本文方法依赖于对应力准则的另一种松弛，并证明它收敛到纯 0–1 设计。

本文结构如下。第 2 节给出混合变分原理的连续与离散形式以及相应的有限元离散格式。第一种离散采用经典多项式有限元，而真混合对偶格式的离散形式采用 Johnson 与 Mercier 的复合单元 [20]。第 3 节导出应力约束拓扑优化问题，并给出处理应力约束施加的一些细节；其中连续与离散最优问题均以（经典的）最优设计目标（如最小柔度与最小体积）表述。第 4 节给出代表性数值模拟的大量结果，涉及当前文献中的经典最优设计问题。特别关注施加越来越严格的应力约束以及改变可用材料上限时最优拓扑发生的变化。此外，通过若干参数化数值研究考察 MMA 方法的收敛速度。第 5 节总结全文，并指出正在进行和有待开展的研究。

---

# 2 有限元格式

## 2.1 引言性说明

用混合有限元逼近结构问题有利有弊，这里简要回顾。多数情况下应力应当被精确计算，因为几乎所有设计准则都基于应力；因此基于位移的有限元（FEM）逼近可能并不完全合适，它需要一种后处理技术来计算应力场（或借助某种应力恢复方法得到其正则化版本），而混合方法把应力作为独立场插值，为分析者提供更好的逼近。此外，某些混合有限元逼近无需任何稳定化技巧即可处理不可压缩介质，这是任何基于位移的方法都不具备的特性。另一方面，基于位移的变分原理只需"简单"的强制性要求，而混合情形还要加上 inf–sup 条件 [18]，它对数值求解可采用的有限元族施加了严格限制。以下各小节给出两种 Hellinger–Reissner 型对偶变分原理的连续与离散形式以及相应的有限元。

## 2.2 各向同性弹性介质的连续混合变分格式

设 $\Omega \in \mathbb{R}^2$ 与 $\partial\Omega$ 分别为系统所占区域及其正则边界。下文中 $\boldsymbol{\sigma}$ 与 $\boldsymbol{\tau}$ 分别表示未知应力场与检验应力场，$\mathbf{u}$ 与 $\mathbf{v}$ 分别表示未知位移场与检验位移场，$\mathbb{C}$ 为满足逐点稳定性的四阶弹性张量，$\mathbf{g}$ 为平方可积的体力向量。首先引入两种 Hellinger–Reissner 原理框架下自然出现的若干函数空间。最常用的格式以正则位移与间断应力为特征，二者分别属于空间

$$
V = [H_0^1(\Omega)]^2
\tag{1}
$$

与

$$
\Sigma = \{\boldsymbol{\tau} : \tau_{ij} \in L^2(\Omega),\ \tau_{ij} = \tau_{ji}\}
\tag{2}
$$

相应的变分格式为：求 $(\boldsymbol{\sigma}, \mathbf{u}) \in \Sigma \times V$，使得

$$
\begin{aligned}
\int_\Omega \mathbb{C}^{-1}\boldsymbol{\sigma} : \boldsymbol{\tau}\,\mathrm{d}x - \int_\Omega \boldsymbol{\varepsilon}(\mathbf{u}) : \boldsymbol{\tau}\,\mathrm{d}x &= 0 \quad \forall \boldsymbol{\tau} \in \Sigma \\
-\int_\Omega \boldsymbol{\varepsilon}(\mathbf{v}) : \boldsymbol{\sigma}\,\mathrm{d}x + \int_\Omega \mathbf{g} \cdot \mathbf{v}\,\mathrm{d}x &= 0 \quad \forall \mathbf{v} \in V
\end{aligned}
\tag{3}
$$

其中"$:$"与"$\cdot$"分别表示二阶张量之间与向量之间的缩并（内积），$\boldsymbol{\varepsilon}(\cdot)$ 照例为对称梯度算子，即

$$
\boldsymbol{\varepsilon}(\mathbf{u}) = \tfrac{1}{2}(\nabla \mathbf{u} + \nabla^{t}\mathbf{u}) \equiv \nabla^{s}\mathbf{u}
\tag{4}
$$

另一种形式可借助 Gauss–Green 公式得到，它把正则性转移到应力场，代价是位移变为间断。引入函数空间

$$
W = [L^2(\Omega)]^2
\tag{5}
$$

与

$$
H = H(\operatorname{div}, \Omega) = \{\boldsymbol{\tau} : \tau_{ij} = \tau_{ji},\ \tau_{ij} \in L^2(\Omega),\ \operatorname{div}\boldsymbol{\tau} \in W\}
\tag{6}
$$

即得第二种 Hellinger–Reissner 格式：求 $(\boldsymbol{\sigma}, \mathbf{u}) \in H \times W$，使得

$$
\begin{aligned}
\int_\Omega \mathbb{C}^{-1}\boldsymbol{\sigma} : \boldsymbol{\tau}\,\mathrm{d}x + \int_\Omega \operatorname{div}\boldsymbol{\tau} \cdot \mathbf{u}\,\mathrm{d}x &= 0 \quad \forall \boldsymbol{\tau} \in H(\operatorname{div}; \Omega) \\
\int_\Omega \operatorname{div}\boldsymbol{\sigma} \cdot \mathbf{v}\,\mathrm{d}x &= -\int_\Omega \mathbf{g} \cdot \mathbf{v}\,\mathrm{d}x \quad \forall \mathbf{v} \in W(\Omega)
\end{aligned}
\tag{7}
$$

格式 (3) 与 (7) 都属于混合方法的经典框架；问题适定性的细节主要涉及 inf–sup 条件以及表示余能的二次型

$$
a(\boldsymbol{\sigma}, \boldsymbol{\tau}) = \int_\Omega \mathbb{C}^{-1}\boldsymbol{\sigma} : \boldsymbol{\tau}\,\mathrm{d}x
$$

在混合双线性型 $b(\cdot,\cdot)$ 的核上的椭圆性，这些均基于 [4]。对所提出的两种变分原理，$b(\cdot,\cdot)$ 分别为

$$
b(\boldsymbol{\tau}, \mathbf{u}) = -\int_\Omega \boldsymbol{\varepsilon}(\mathbf{u}) : \boldsymbol{\tau}\,\mathrm{d}x
$$

$$
b(\boldsymbol{\tau}, \mathbf{u}) = \int_\Omega \operatorname{div}\boldsymbol{\tau} \cdot \mathbf{u}\,\mathrm{d}x
$$

值得注意的是，对于本文所考虑的各向同性介质，余能仅依赖于两个模量，例如 Lamé 常数 $\lambda$ 与 $\mu$，于是可写[^1]

$$
a(\boldsymbol{\sigma}, \boldsymbol{\tau}) = \int_\Omega \mathbb{C}^{-1}\boldsymbol{\sigma} : \boldsymbol{\tau}\,\mathrm{d}x = \int_\Omega \left[\frac{1}{2\mu}\boldsymbol{\sigma}^D : \boldsymbol{\tau}^D + \frac{1}{\lambda+\mu}\operatorname{tr}(\boldsymbol{\sigma})\operatorname{tr}(\boldsymbol{\tau})\right]\mathrm{d}x
$$

## 2.3 各向同性弹性介质的离散混合变分格式

### 2.3.1 连续位移与间断应力

采用第一种变分格式 (3) 时，位移是连续的主变量，而应力充当间断的 Lagrange 乘子。因此引入经典的 $(P_1, P_0)$ 逼近：位移整体连续、单元内线性，应力整体间断、单元内常数。离散变分格式为：求 $(\boldsymbol{\sigma}_h, \mathbf{u}_h) \in \Sigma_h \times V_h$，使得[^2]

$$
\begin{aligned}
\int_\Omega \mathbb{C}^{-1}\boldsymbol{\sigma}_h : \boldsymbol{\tau}_h\,\mathrm{d}x + \int_\Omega \boldsymbol{\varepsilon}(\mathbf{u}_h) \cdot \boldsymbol{\tau}_h\,\mathrm{d}x &= 0 \quad \forall \boldsymbol{\tau}_h \in \Sigma_h \\
-\int_\Omega \boldsymbol{\varepsilon}(\mathbf{v}_h) \cdot \boldsymbol{\sigma}_h\,\mathrm{d}x &= -\int_\Omega \mathbf{g} \cdot \mathbf{v}_h\,\mathrm{d}x \quad \forall \mathbf{v}_h \in V_h
\end{aligned}
\tag{8}
$$

![[Bruggi2008_Fig1.png]]

<center><b>
图 1：剖分为三角形的复合单元。
</b></center>

其中，在协调逼近下，$\Sigma_h \subset \Sigma$ 与 $V_h \subset V$ 分别是区域 $\Omega$ 上零次与一次多项式形函数 $P_0$ 与 $P_1$ 张成的空间。

### 2.3.2 通量连续应力与间断位移

对偶变分格式 (7) 更为微妙，主要困难在于应力张量对称性的处理。在可用的方法 [18] 中，引入 Johnson 与 Mercier 的单元 [20]，它是极少数能在真混合框架下、与单元内线性且整体间断的位移相耦合时通过 inf–sup 条件的单元之一。我们采用如图 1 所示的三角形 JM 复合单元。网格中的每个三角形 $K$ 进一步剖分为三个子三角形 $T_i$，从而定义 Johnson–Mercier 应力空间

$$
JM(K) = \{\boldsymbol{\sigma} \,|\, \boldsymbol{\sigma} \in H(\operatorname{div}; K),\ \boldsymbol{\sigma}|_{T_j} \in [P_1(T_j)]^{2\times 2}_s,\ j = 1, 2, 3\}
\tag{9}
$$

其中 $P_1(T_j)$ 是 $T_j$ 上次数 $\leqslant 1$ 的多项式空间。$JM(K)$ 中的元素 $\boldsymbol{\sigma}$ 由下列 15 个自由度唯一确定 [20]：

$$
\int_{e_i} (\boldsymbol{\sigma} \cdot \mathbf{n}) \cdot \mathbf{w}\,\mathrm{d}s \quad \forall \mathbf{w} \in (P_1(e_i))^2,\ i = 1, 2, 3
\tag{10}
$$

$$
\int_T \boldsymbol{\sigma} : \mathbf{w}\,\mathrm{d}x \quad \forall \mathbf{w} \in (P_0(T))^{2\times 2}_s
\tag{11}
$$

其中 $e_i$ 表示三角形单元的第 $i$ 条边。于是应力在空间

$$
H_h = \{\boldsymbol{\sigma}_h \in H(\operatorname{div}, \Omega),\ \boldsymbol{\sigma}_h|_K \in JM(K)\}
\tag{12}
$$

中逼近。至于位移，采用单元内线性、整体间断的逼近，即位移在空间

$$
W_h = \{\mathbf{v}_h \in W : \mathbf{v}_h|_K \in [P_1(K)]^2\}
\tag{13}
$$

中逼近。离散变分格式因而为：求 $(\boldsymbol{\sigma}_h, \mathbf{u}_h) \in H_h \times W_h$，使得

$$
\begin{aligned}
\int_\Omega \mathbb{C}^{-1}\boldsymbol{\sigma}_h : \boldsymbol{\tau}_h\,\mathrm{d}x + \int_\Omega \operatorname{div}\boldsymbol{\tau}_h \cdot \mathbf{u}_h\,\mathrm{d}x &= 0 \quad \forall \boldsymbol{\tau}_h \in H_h \\
\int_\Omega \operatorname{div}\boldsymbol{\sigma}_h \cdot \mathbf{v}_h\,\mathrm{d}x &= -\int_\Omega \mathbf{g} \cdot \mathbf{v}_h\,\mathrm{d}x \quad \forall \mathbf{v}_h \in W_h(\Omega)
\end{aligned}
\tag{14}
$$

## 2.4 离散矩阵–向量方程

本节稍微滥用记号，用同一符号表示（应力或位移）场及其形函数。这样，两种离散变分格式 (8) 与 (14) 都可写成矩阵形式

$$
\begin{bmatrix}
A_{\sigma\sigma} & B_{\sigma u} \\
B_{u\sigma} & 0
\end{bmatrix}
\begin{Bmatrix}
\sigma \\ u
\end{Bmatrix}
=
\begin{Bmatrix}
0 \\ g
\end{Bmatrix}
\tag{15}
$$

如下一节所示，混合矩阵方程 (15) 作为约束进入最优问题的表述，取代经典的位移方程 $Ku = f$，其中 $K$ 为通常的刚度矩阵，$u$ 与 $f$ 分别为位移向量与载荷向量。再次强调，方程 (15) 对应力张量的逼近远优于位移格式。另一方面，混合矩阵

$$
M = \begin{bmatrix}
A_{\sigma\sigma} & B_{\sigma u} \\
B_{u\sigma} & 0
\end{bmatrix}
$$

不是正定的，其背后是一个鞍点问题。因此线性方程组 (15) 的求解需要专门的数值策略，梯度的解析计算也需要一些额外的代数运算，见下文。

### 2.4.1 混合矩阵–向量方程的求解

对于不定线性方程组 (15) 的数值求解，文献中有若干算法可用。最经典的是 Uzawa 格式及其非精确与预条件变体，它充分利用混合矩阵 $M$ 的块结构以迭代方式求解线性方程组。文献 [21] 引入了一种算法，可用于本文两种混合格式中的第一种，即位移连续而应力间断的情形。此时应力在单元层面被静力凝聚掉，(15) 的求解归结为小型单元矩阵的求逆，计算时间显著节省。在使用现代的大型稀疏线性方程组求解器时，不仅待分解或求逆矩阵的性质重要，代码结构及其与优化代码其余部分的链接能力也至关重要。因此优化模拟采用了专为不定线性方程组求解而设计的 PARDISO 算法 [22, 23]。我们实际使用的是 Fortran 90 版本的 PARDISO，它易于与我们原生 Fortran 实现中最初选定的存储结构链接。下文计算中遇到的典型线性方程组约有一万五千个未知量，来自约四千个单元的网格。就控制矩阵的稀疏性而言，非零元约十万个。所采用的算法分解矩阵约需 0.1 s，求解方程组所需的额外时间可忽略。

---

# 3 应力约束拓扑优化设计

## 3.1 预备说明

本文的主要目标是为应力约束拓扑优化提出一种替代方法，它应足够一般，能处理不同的最优目标。为方便起见，我们选择给出若干关于应力约束最小柔度设计的数值研究，见下一节所述。其他表述，如 [11] 中深入研究的最小体积表述，目前正在研究中，将在不久的将来给出。

## 3.2 柔度格式

下文给出的所有数值研究均可纳入如下应力约束最小柔度框架：

$$
\begin{aligned}
\min_{\rho \in \mathbb{R}^+} \quad & \mathcal{C} = F^{t}U \\
\text{s.t.} \quad & \int_\Omega \rho\,\mathrm{d}\Omega \leqslant \overline{V} \\
& \begin{bmatrix}
A_{\sigma\sigma} & B_{\sigma u} \\
B_{u\sigma} & 0
\end{bmatrix}
\begin{Bmatrix}
\sigma \\ u
\end{Bmatrix}
=
\begin{Bmatrix}
0 \\ g
\end{Bmatrix} \\
& \sigma_{\mathrm{VM}} = \sqrt{\sigma_{xx}^2 + \sigma_{yy}^2 - \sigma_{xx}\sigma_{yy} + 3\sigma_{xy}^2} \leqslant \rho^{p}\sigma_{\mathrm{Y}} \\
& 0 < \rho \leqslant \overline{\rho} = 1
\end{aligned}
\tag{16}
$$

其中 $F$ 为载荷向量，$U \subset u$ 为对偶位移，$\overline{V}$ 为容许体积，即设计域总体积 $V_{\mathrm{tot}}$ 的一个分数，$\sigma_{\mathrm{Y}}$ 为原始全密度材料的屈服应力，$p$ 为 SIMP 指数，数值研究中取 3。关于 (16)$_4$ 右端应力阈值 $\rho^p\sigma_{\mathrm{Y}}$ 的推导，参阅 [11]。注意严格的下界 $0 < \rho$，它是避免刚度矩阵奇异所必需的；为此在数值代码中为质量密度选取一个很小的下界，典型值为 $10^{-3}$。

## 3.3 处理应力约束非正则性的一种替代方法

众所周知，应力约束一般不会导出适定问题。当材料密度趋于零，即设计空间中出现空洞区域时，相应的应力反而可能趋于一个有限值，因此即使在没有材料的地方，数值求解器也可能检测到应力约束的违反 [11]。从理论角度看，由于这种退化，设计空间中的最优区域变得不可达；文献中提出并检验了 ε-松弛方法作为补救，关于桁架拓扑优化情形下的计算与理论考虑分别见 [24, 25]。我们发展了一种不同的方法，其中松弛应力约束的参数 ε 不再出现，取而代之的是我们称之为 qp-松弛的做法，即把应力约束

$$
\sigma_{\mathrm{VM}} = \sqrt{\sigma_{xx}^2 + \sigma_{yy}^2 - \sigma_{xx}\sigma_{yy} + 3\sigma_{xy}^2} \leqslant \rho^{p}\sigma_{\mathrm{Y}}
$$

近似为

$$
\sigma_{\mathrm{VM}} = \sqrt{\sigma_{xx}^2 + \sigma_{yy}^2 - \sigma_{xx}\sigma_{yy} + 3\sigma_{xy}^2} \leqslant \rho^{q}\sigma_{\mathrm{Y}}
$$

其中 $q \to p$ 且从下方逼近。

为说明该方法如何起作用，首先考虑两种方法在形式上的相似性较为方便。考虑上述表达式的平方形式（MMA 算法中实际实现的形式），经典 ε-松弛方法与 qp-松弛分别为

$$
\underbrace{(\sigma_{\mathrm{VM}}^2 - \rho^{2p}\overline{\sigma}^2)\rho \leqslant \varepsilon}_{\varepsilon\text{-relaxation}}, \qquad
\underbrace{(\sigma_{\mathrm{VM}}^2 - \rho^{2q}\overline{\sigma}^2)\rho \leqslant 0}_{qp\text{-approach}}
\tag{17}
$$

经过一些代数运算可以证明，qp-松弛也可写成

$$
(\sigma_{\mathrm{VM}}^2 - \rho^{2p}\overline{\sigma}^2)\rho \leqslant (\rho^{2q} - \rho^{2p})\rho\overline{\sigma}^2
$$

由此可以断言，qp-松弛方法是一种自适应的 ε-松弛格式，其中

$$
\varepsilon = (\rho^{2q} - \rho^{2p})\rho\overline{\sigma}^2
$$

必须注意，这个自适应的 ε 在密度趋于 1 时趋于零，从而保证最终的 0–1 设计不带任何松弛偏差；[11] 所采用形式的经典 ε-松弛不具备这一特性。为分析两种方法在施加应力限制时引入的扰动，考虑 MMA 框架下应力约束的一种合适实现，对 ε-松弛与 qp-方法均如此。

前者为

$$
\frac{\sigma_{\mathrm{VM}}^2}{\rho^{2p}\overline{\sigma}^2} \leqslant 1 + \frac{\varepsilon}{\rho}
\tag{18}
$$

后者为

$$
\frac{\sigma_{\mathrm{VM}}^2}{\rho^{2q}\overline{\sigma}^2} \leqslant 1
\tag{19}
$$

也可改写为

$$
\frac{\sigma_{\mathrm{VM}}^2}{\rho^{2p}\overline{\sigma}^2} \leqslant \frac{\rho^{2q}}{\rho^{2p}}
\tag{20}
$$

将 (18) 与 (20) 的右端与未松弛应力约束

$$
\frac{\sigma_{\mathrm{VM}}^2}{\rho^{2p}\overline{\sigma}^2} \leqslant 1
\tag{21}
$$

的右端比较，可以估计两种方法在整个密度范围内引入的扰动幅度。图 2 绘出了上述扰动后的右端，即

$$
\underbrace{1 + \frac{\varepsilon}{\rho}}_{\varepsilon\text{-relaxation}}, \qquad
\underbrace{\frac{\rho^{2q}}{\rho^{2p}}}_{qp\text{-approach}}
\tag{22}
$$

对两组控制参数 ε 与 $q$，给出了相对于未松弛情形单位线的偏差曲线。

![[Bruggi2008_Fig2.png]]

<center><b>
图 2：应力约束施加中引入的扰动。ε-方法（左）与 qp-方法（右）。
</b></center>

如前所述，qp-方法在密度趋于 1 时不引入任何改动，同时在奇异的低密度区给出合适的偏差。相反，经典 ε-松弛在整个密度范围内引入的容差主要取决于所选松弛参数的大小，特别是在密度为 1 时也不为零。这是需要采用所谓延拓（continuation）方法以更好地逼近约束解的原因之一。此外，两种方法在中间密度区产生不同的改动，这对最小化过程中应力约束的处理有影响，数值部分将进一步考察。

## 3.4 混合格式的特点

### 3.4.1 混合框架下的 SIMP 方法

回顾混合矩阵 $M$ 仅通过余能 $A$ 依赖于设计变量 $\rho$，即

$$
M(\rho) = \begin{bmatrix}
A_{\sigma\sigma}(\rho) & B_{\sigma u} \\
B_{u\sigma} & 0
\end{bmatrix}
$$

而 $B$ 在第一种变分格式中是相容算子，在第二种中是平衡算子，因此与材料无关。解向量 $\{\sigma\ u\}^{t}$ 关于第 $i$ 个单元密度 $\rho_i$ 的灵敏度可按下式计算：

$$
\begin{bmatrix}
\dfrac{\partial A_{\sigma\sigma}}{\partial \rho_i} & 0 \\
0 & 0
\end{bmatrix}
\begin{Bmatrix}
\sigma \\ u
\end{Bmatrix}
+
\begin{bmatrix}
A_{\sigma\sigma} & B_{\sigma u} \\
B_{u\sigma} & 0
\end{bmatrix}
\begin{Bmatrix}
\dfrac{\partial \sigma}{\partial \rho_i} \\[2mm] \dfrac{\partial u}{\partial \rho_i}
\end{Bmatrix}
=
\begin{Bmatrix}
0 \\ 0
\end{Bmatrix}
\tag{23}
$$

或

$$
\begin{bmatrix}
A_{\sigma\sigma} & B_{\sigma u} \\
B_{u\sigma} & 0
\end{bmatrix}
\begin{Bmatrix}
\dfrac{\partial \sigma}{\partial \rho_i} \\[2mm] \dfrac{\partial u}{\partial \rho_i}
\end{Bmatrix}
=
-\begin{bmatrix}
\dfrac{\partial A_{\sigma\sigma}}{\partial \rho_i} & 0 \\
0 & 0
\end{bmatrix}
\begin{Bmatrix}
\sigma \\ u
\end{Bmatrix}
\tag{24}
$$

这意味着计算结构灵敏度需要求解辅助混合问题，其虚拟载荷由 (24) 的右端给出。(24) 中的灵敏度用于计算目标函数的梯度，即柔度目标情形下的

$$
\frac{\partial \mathcal{C}}{\partial \rho_i} = F^{t}\frac{\partial U}{\partial \rho_i}
\tag{25}
$$

以及（von Mises）应力约束的梯度，即

$$
\frac{\partial \sigma_{\mathrm{VM}}}{\partial \rho_i} = \frac{1}{2\sigma_{\mathrm{VM}}}\left[2\sigma_{xx}\frac{\partial \sigma_{xx}}{\partial \rho_i} + 2\sigma_{yy}\frac{\partial \sigma_{yy}}{\partial \rho_i} - \sigma_{xx}\frac{\partial \sigma_{yy}}{\partial \rho_i} - \sigma_{yy}\frac{\partial \sigma_{xx}}{\partial \rho_i} + 6\sigma_{xy}\frac{\partial \sigma_{xy}}{\partial \rho_i}\right]
\tag{26}
$$

### 3.4.2 计算细节

求解最优设计问题 (16) 与鞍点问题 (15) 的算法是下文数值研究所用数值优化方法的核心。对于最小化问题 (16)，采用 MMA [6] 并结合基于 3.4.1 节关系的梯度解析计算。事实上，该问题已针对节点密度作了专门处理，节点密度是下文计算中采用的最小化变量。因此每个单元密度取为其节点值的平均。与以单元密度为最小化变量的经典格式相比，这种做法显著减少了未知量数目。以下文计算中方形域所用的典型网格为例：$32 \times 32$ 个四边形区域，每个再沿对角线剖分为四个三角形，共生成 4096 个单元与 2113 个节点。这种未知量上的节省在最小化过程中被证明特别高效。密度自由度数目的减少事实上降低了出现棋盘格不稳定的可能性，并且在处理多约束最小化过程时计算高效。此外，由于每个节点未知量属于多个单元，这种密度离散还提供了某种长度尺度控制，如 [11, 19] 所述。如下文所示，该方法表现出较快的收敛速度，中间设计与最终最优设计均无棋盘格。SQP 方法（至少在我们的实现中）不具备这些优良特性，它往往停滞在具有多个中间密度区域的中间设计上。不过必须指出问题的非凸性质，并且中间设计虽不理想，仍是优化问题的有效解。

---

# 4 数值研究

## 4.1 总体说明

本节的目标如下：

1. 评估所提方法在存在应力约束时寻找最优拓扑的能力。特别关注为满足应力约束而在最优拓扑中出现的变化。为此，每个问题都在越来越严格的应力和/或体积约束下求解，并对相应的解进行比较与评述。
2. 评估 MMA 算法应用于本文混合最优变分问题时的收敛速度，给出经典 ε-松弛与所提 qp-方法的数值比较。
3. 检验所采用的混合有限元方法与节点密度插值 [19] 相耦合，是否确实能避免出现棋盘格解。

### 4.1.1 数值观察

众所周知，集中载荷附近会出现数值应力奇异性；为平滑这种效应，可以把载荷分布到结构的一小块区域上。在下文的数值算例中未采取此类措施，集中载荷在模拟中按原样施加。因此，集中载荷附近的应力峰值不应解释为约束违反，而应视为数值误差。事实上，在每个载荷作用区周围的若干单元上未施加局部应力约束。

关于 MMA 的收敛问题，必须指出该方法在确定合理的停止准则方面可能遇到困难。为便于对本节给出的各条收敛曲线进行合适的比较，实施了一个统一的停止条件，基于相邻两步密度的最大差值，此处取为 1%。关于所得最优解在约束有效性方面的可行性，参考 MMA 算法在每次迭代给出的、用于在格式 (16) 中施加应力与体积约束的不等式右端值。对本文给出的所有解，MMA 均在所有右端约束 $\leqslant 1$ 的情况下收敛，因此所求解算例的设计均为可行设计。但由于问题的非凸性质，这并不保证这些解是约束最小化问题的全局最优解。

## 4.2 方形固支薄板（两杆桁架）

### 4.2.1 最大材料体积 = 总设计体积的 35%

作为第一个算例，考虑经典的两杆桁架问题，如图 3 与表 I 所示。图 4 与图 5 给出收敛时的最优密度及相应的 von Mises 应力图。首先把最大体积设为设计空间总量的 35%。

![[Bruggi2008_Fig3.png]]

<center><b>
图 3：算例 1。最优设计问题。
</b></center>

<center><b>
表 I：算例 1。物理与几何参数。
</b></center>

| $\overline{V}$ | $E$ | $\nu$ | $L$ | $\sigma_{\mathrm{Y}}$ | $P$ |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.35 | 1 | 0.3 | 400 | 0.028 | 1 |
| 0.25 | 1 | 0.3 | 400 | 0.048 | 1 |

![[Bruggi2008_Fig4.png]]

<center><b>
图 4：算例 1（$\overline{V} = 35\%V_{\mathrm{tot}}$）。最优密度。无应力约束（左）（柔度 28.28）与有应力约束（右）（$q = 2.9$，柔度 30.10）。
</b></center>

![[Bruggi2008_Fig5.png]]

<center><b>
图 5：算例 1。von Mises 应力——无应力约束（左）与有应力约束（右）。
</b></center>

比较无约束设计与应力约束设计，可以观察到的主要变化如下：

1. 左下角的应力峰值通过改变整个设计的拓扑而被消除。事实上可以看到，在应力约束情形下，主要承载机制由斜拉杆和终止于试件左下角的水平受压构件组成，次斜撑杆的汇入只带来可忽略的扰动。相反，在无约束设计中，斜撑杆架在次水平构件之上，在角部附近产生了明显可见的应力集中。
2. 为消除左上角的应力峰值采取了两种不同的措施。一方面，从上角出发的斜杆长度被缩短，这是由于受压斜杆的新几何形状从原点穿过设计域，到达新拉杆的大致中点。其次，左上角的拓扑明显改变，在应力约束设计中该处所用材料似乎更少。

![[Bruggi2008_Fig6.png]]

<center><b>
图 6：算例 1。无应力约束最小柔度设计的收敛曲线。
</b></center>

![[Bruggi2008_Fig7.png]]

<center><b>
图 7：算例 1。收敛曲线。ε-松弛（左）与 qp-方法（右）。
</b></center>

观察图 6 与图 7 的收敛曲线可以看出，约束情形的计算量更大；就最优柔度值而言，为满足应力约束付出的代价是增加 5%。尽管有这一结果，必须指出约束解不一定以无约束设计为下界。由于前已提及的问题非凸性质，无约束解事实上可能是局部极小而非全局极小。图 7 最终涉及 3.3 节为处理奇异性现象而引入的应力约束改动。图中通过与 MMA 算法结合产生的收敛曲线比较了松弛参数 ε 与 $q$ 的不同选择。两种方法都得到纯 0–1 设计，并且在适当选择松弛参数时都能减少迭代次数。至少在本算例中，qp-方法在计算量方面略有优势，这可能源于它在中间密度范围内的不同畸变（见图 2）。主要差别在于最终柔度值：不同 $q$ 取值对应的最终柔度彼此远比不同 ε 取值时接近。这一特点与所谓延拓方法的使用密切相关。在 ε-松弛框架下，通常采用的求解过程是首先用一个适当大的 ε 求解优化问题，其作用是松弛约束以对抗奇异性；然后对递减的松弛参数求解一系列原问题，每一步以上一步的收敛设计作为下一步更严格分析的初始猜测。要消除最优解对 ε 取值的依赖，确实需要这一方法。

相反，采用 qp-方法不一定需要这一过程。事实上可以选择合适的 $q$ 值，既克服奇异性问题，又改善 MMA 的收敛性能，从而得到与未松弛解相当接近的 0–1 最优解（典型地取 $q \geqslant 2.5$）。考虑到多约束问题的高度非线性与复杂性使 MMA 每次迭代耗时较长，这一特点因而能显著减少计算负担。

### 4.2.2 最大材料体积 = 总设计体积的 25%

回到设计问题，为评估可用材料上限的影响，对同一问题取 $\overline{V} = 25\%V_{\mathrm{tot}}$ 进行分析。此外，为补偿材料的不足，应力限值提高到 $\sigma_{\mathrm{Y}} = 0.048$。图 8 给出在 $\overline{V} = 25\%V_{\mathrm{tot}}$ 限制下无约束与应力约束的最优解。无约束解如预期那样是 $\overline{V} = 35\%V_{\mathrm{tot}}$ 时所得解的翻版，应力峰值增加了约 20%。另一方面，应力峰值的增加与（松弛后的）应力约束不相容，因此约束解出现了一种新的拓扑。缩短斜撑以缓解左上节点应力的任务，现在由一根不从原点出发、而是直接固支在左边界上的受压撑杆承担。这一处理还避免了左下节点处出现应力集中（图 9）。

![[Bruggi2008_Fig8.png]]

<center><b>
图 8：算例 1（$\overline{V} = 25\%V_{\mathrm{tot}}$）。最优密度。无应力约束（左）（柔度 40.32）与有应力约束（右）（$q = 2.9$，柔度 41.95）。
</b></center>

![[Bruggi2008_Fig9.png]]

<center><b>
图 9：算例 1（$\overline{V} = 25\%V_{\mathrm{tot}}$）。von Mises 应力——无应力约束（左）与有应力约束（右）。
</b></center>

## 4.3 L 形薄板

第二项研究的对象是经典的 L 形结构，如图 10 与表 II 所示。设计可用的体积分数取为总设计空间的 35%。凹角处众所周知的应力集中现象似乎要求采用专门的变分格式，例如本文提出的第二种格式，它在 $H(\operatorname{div})$ 中逼近应力。采用该方法的数值结果将在后续论文中给出。目前使用第一种 Hellinger–Reissner 原理。图 11 与图 12 给出最优拓扑与 von Mises 应力图。尽管两个设计在拓扑上相似，但出现了明显的差别。在无约束情形，大量材料分布在凹角处，凹角被填充到最大程度，即 270°。角部的应力峰值与应力约束施加的限制不相容。应力约束的最优拓扑事实上有所不同：凹角的角度不再是 270°，而是明显更小。基本上，约束最优拓扑的特征是一根受拉竖杆延伸为两组倾斜构件，它们各自独立地从角部发展到试件的右下与左下部分，从而大幅降低角部应力。此外可以注意到，在无应力约束情形有四根杆从角部发出，而在应力约束情形只需三根主杆， 这进一步证实了为满足应力约束需要在某个角度上削弱结构。图 13 给出 MMA 算法在无约束与应力约束情形下的表现。

![[Bruggi2008_Fig10.png]]

<center><b>
图 10：算例 2。最优设计问题。
</b></center>

<center><b>
表 II：算例 2。物理与几何参数。
</b></center>

| $\overline{V}$ | $E$ | $\nu$ | $L$ | $\sigma_{\mathrm{Y}}$ | $P$ |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.35 | 1 | 0.3 | 75 | 0.5 | 1 |

![[Bruggi2008_Fig11.png]]

<center><b>
图 11：算例 2。最优密度。无应力约束（左）（柔度 268.80）与有应力约束（右）（$q = 2.9$，柔度 286.52）。
</b></center>

![[Bruggi2008_Fig12.png]]

<center><b>
图 12：算例 2。von Mises 应力——无应力约束（左）与有应力约束（右）。
</b></center>

![[Bruggi2008_Fig13.png]]

<center><b>
图 13：算例 2。收敛曲线。无应力约束（左）与有应力约束（右）。
</b></center>

## 4.4 方形固支薄板（四杆桁架）

图 14 与表 III 给出一个简单但拓扑丰富的数值研究，它与算例 1 基本相同，只是载荷施加在右边界的中点。图 15 与图 16 给出收敛时的最优密度及相应的 von Mises 应力图，收敛曲线见图 17 与图 18。

![[Bruggi2008_Fig14.png]]

<center><b>
图 14：算例 3。最优设计问题。
</b></center>

<center><b>
表 III：算例 3。物理与几何参数。
</b></center>

| $\overline{V}$ | $E$ | $\nu$ | $L$ | $\sigma_{\mathrm{Y}}$ | $P$ |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.35 | 1 | 0.3 | 400 | 0.04 | 1 |

![[Bruggi2008_Fig15.png]]

<center><b>
图 15：算例 3。最优密度。无应力约束（左）（柔度 33.42）与有应力约束（右）（$q = 2.9$，柔度 37.97）。
</b></center>

![[Bruggi2008_Fig16.png]]

<center><b>
图 16：算例 3。von Mises 应力——无应力约束（左）与有应力约束（右）。
</b></center>

相当有趣的是，两种情形下加强撑杆的拓扑不同。在无应力约束情形，最优结构呈现高度的超静定性，事实上可以看到三个内部环。这种结构方案提供了相当高的刚度（因而柔度极低），但同时应力值很大。相反，应力约束解可视为无约束解的一个松弛的、稍柔一些的版本，其加强撑杆被约束在左边界上。同样，追求应力约束解时最优柔度值增加了 10%。

![[Bruggi2008_Fig17.png]]

<center><b>
图 17：算例 3。无应力约束最小柔度设计的收敛曲线。
</b></center>

![[Bruggi2008_Fig18.png]]

<center><b>
图 18：算例 3。收敛曲线。ε-松弛（左）与 qp 方法（右）。
</b></center>

图 18 给出该设计问题下 qp-方法与 ε-松弛所得收敛曲线的比较。算例 1 的评述在此同样适用。但必须注意，不同 ε 所画出的曲线要不规则得多，似乎受到不同局部极小的影响。事实上，考虑选取较大松弛（即 ε = 1）所得到的设计（图 19）。它显然呈现出一种仍与无约束设计紧密联系的拓扑，与较小松弛所得到的拓扑相当不同。这一点在延拓框架下相当重要：若选择该设计作为更严格约束最小化的起点，MMA 将被迫尝试从一个局部最优移动到另一个不同的局部最优。相反，qp-方法不存在这一问题，例如图 18 表明，即使在约束改动很大的情况下，不同 $q$ 参数取值下它也收敛到相同的最终柔度值。

![[Bruggi2008_Fig19.png]]

<center><b>
图 19：算例 3。取 ε = 1 时的最优设计。
</b></center>

---

# 5 结论与后续研究需求

本文提出了一种存在局部应力约束时平面弹性结构拓扑优化的替代方法。方法的核心是采用混合有限元离散格式，其中应力（与位移）独立插值，因而能以较高精度直接用于局部应力约束的施加。这一有限元技术与一种密度离散相耦合，后者基于对节点密度作单元平均，节点密度是最小化算法的主变量。奇异性问题通过一种替代技术而非更经典的 ε-松弛来处理。对该过程的特点进行了考察与数值检验，以评估其与经典松弛过程相比的收敛特性。就设计方面而言，结果表明应力约束往往导致与经典最小柔度最优设计完全不同的新拓扑。

当前的发展包括：借助真混合 Hellinger–Reissner 格式进行不可压缩材料的优化；以及借助基于最大耗散原理、且变分框架与本文所用格式同属一族的表述进行弹塑性介质的设计。

---

# 致谢

本文的部分内容是 Matteo Bruggi 在丹麦 Lyngby 的 DTU 由 Martin Bendsøe 教授指导进行为期两个月的研究期间撰写的。感谢 Martin Bendsøe、Ole Sigmund 与 Mathias Stolpe 教授就本文多个主题进行的启发性讨论。同时感谢由 Carlo Cinquini 教授协调的 MIUR PRIN-COFIN 2005–2006 年度资助。

---

# 参考文献

1. Bendsøe M, Kikuchi N. Generating optimal topologies in structural design using a homogeneization method. *Computational Methods in Applied Mechanics and Engineering* 1988; 71(2):197–224.
2. Bendsøe M, Sigmund O. Material interpolation schemes in topology optimization. *Archive of Applied Mechanics* 1999; 69:635–654.
3. Petersson J. Some convergence results in perimeter-controlled topology optimization. *Computational Methods in Applied Mechanical Engineering* 1999; 171:123–140.
4. Luenberger DG. *Linear and Nonlinear Programming*. Addison-Wesley: Reading, MA, 1984.
5. Fleury C. CONLIN: an efficient dual optimizer based on convex approximation concepts. *Structural and Multidisciplinary Optimization* 1989; 1:81–89.
6. Svamberg K. Method of moving asymptotes—a new method for structural optimization. *International Journal for Numerical Methods in Engineering* 1984; 24(3):359–373.[^3]
7. Olhoff N, Eschenauer HA. Topology optimization of continuum structures—a review. *Applied Mechanics Reviews* 2001; 54:331–390.
8. Bendsøe M, Sigmund O. *Topology Optimization—Theory, Methods and Applications*. Springer, EUA: New York, 2003.
9. Querin OM, Steven GP, Xie YM. Evolutionary structural optimization using additive algorithm. *Finite Elements in Analysis and Design* 2000; 34:291–308.
10. Yang RJ, Chen CJ. Stress-based topology optimization. *Structural Optimization* 1996; 12:98–105.
11. Duysinx P, Bendsøe M. Topology optimization of continuum structures with local stress constraints. *International Journal for Numerical Methods in Engineering* 1998; 43:1453–1478.
12. Pereira JT, Fancello EA, Barcellos CS. Topology optimization of continuum structures with material failure constraints. *Structural and Multidisciplinary Optimization* 2004; 26:50–66.
13. Duysinx P, Sigmund O. New developments in handling stress constraints in optimal material distribution. *Seventh Symposium on Multidisciplinary Analysis and Optimization*, AIAA-98-4906, 1998; 1501–1509.
14. Stolpe M, Svanberg K. Modelling topology optimization problems as linear mixed 0–1 programs. *International Journal for Numerical Methods in Engineering* 2003; 57:723–739.
15. Sigmund O, Petersson J. Numerical instabilities in topology optimization: a survey on procedures dealing with checkerboards, mesh-dependencies and local minima. *Structural and Multidisciplinary Optimization* 1998; 16(1):68–75.
16. Jang G-W, Jeong JH, Kim YY, Sheen D, Park C, Kim M-N. Checkerboard-free topology optimization using non-conforming finite elements. *International Journal for Numerical Methods in Engineering* 2003; 57:1717–1735.
17. Cheng GD, Guo X. ε-relaxed approach in topology optimization. *Structural Optimization* 1997; 13:258–266.
18. Brezzi F, Fortin M. *Mixed and Hybrid Finite Element Methods*. Springer: New York, 1991.
19. Hammer VB. Checkmate?—Nodal densities in topology optimization. In *CD-ROM Proceedings of the Second Max Planck Workshop on Engineering Design Optimization*, Department of Mathematics, Technical University of Denmark, Lyngby, Bendsøe MP, Olhoff N, Rasmussen J (eds), 2001.
20. Johnson C, Mercier B. Some equilibrium finite elements methods for two dimensional elasticity problems. *Numerical Mathematics* 1978; 30:103–116.
21. Pian THH. State-of-the-art development of hybrid/mixed finite element method. *Finite Elements in Analysis and Design* 1995; 21:5–20.
22. Schenk O, Gärtner K. Solving unsymmetric sparse systems of linear equations with PARDISO. *Journal of Future Generation Computer Systems* 2004; 20(3):475–487.
23. Schenk O, Gärtner K. On fast factorization pivoting methods for symmetric indefinite systems. *Electronic Transactions in Numerical Analysis* 2006; 23:158–179.
24. Stolpe M, Svanberg K. On the trajectories of the epsilon-relaxation approach for stress-constrained truss topology optimization. *Structural and Multidisciplinary Optimization* 2001; 21:140–151.
25. Petersson J. On continuity of the design-to-state mappings for trusses with variable topology. *International Journal of Engineering Science* 2001; 39:1119–1141.

[^1]: 译者注：原文体积项系数印作 $\frac{1}{\lambda+\mu}$。按二维各向同性柔度张量 $\mathbb{C}^{-1}\boldsymbol{\sigma} = \frac{1}{2\mu}\left[\boldsymbol{\sigma} - \frac{\lambda}{2(\lambda+\mu)}\operatorname{tr}(\boldsymbol{\sigma})\mathbf{I}\right]$ 推导，该系数应为 $\frac{1}{4(\lambda+\mu)}$。此处照原文保留。
[^2]: 译者注：原文式 (8) 第一式的应变项取加号并用"$\cdot$"连接，与连续格式 (3) 的减号与"$:$"不一致，疑为排印差异。此处照原文保留。
[^3]: 译者注：原文作者名印作"Svamberg"，年份印作 1984；该文实际为 Svanberg K.，刊于 *IJNME* 1987; 24:359–373。此处照原文保留。
