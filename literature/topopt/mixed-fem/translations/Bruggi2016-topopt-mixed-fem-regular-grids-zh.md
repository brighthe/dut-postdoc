---
title: "翻译：规则网格上基于混合有限元的拓扑优化 (Topology optimization with mixed finite elements on regular grids)"
tags:
  - translation
  - mixed-fem
  - topology-optimization
  - stress-constrained
  - incompressible
  - complementary-energy
status: "done"
date_created: 2026-09-20
date_updated: 2026-09-20
source: "../sources/Bruggi2016-topopt-mixed-fem-regular-grids.pdf"
citekey: "bruggiTopologyOptimizationMixed2016"
language: "zh-CN"
---

# Topology Optimization with Mixed Finite Elements on Regular Grids

---

# 信息

- **中文标题**：规则网格上基于混合有限元的拓扑优化
- **英文标题**：Topology optimization with mixed finite elements on regular grids
- **作者**：Matteo Bruggi
- **作者单位**：米兰理工大学土木与环境工程系（Department of Civil and Environmental Engineering, Politecnico di Milano, I20133, Milano, Italy）
- **期刊**：*Computer Methods in Applied Mechanics and Engineering* (CMAME)
- **卷 / 期 / 页码**：Vol. 305, pp. 133–153 (2016)
- **DOI**：[10.1016/j.cma.2016.03.010](https://doi.org/10.1016/j.cma.2016.03.010)
- **收稿 / 修回 / 录用**：Received 10 October 2015; Revised 30 December 2015; Accepted 7 March 2016
- **Better BibTeX key**：`bruggiTopologyOptimizationMixed2016`
- **译文状态**：全文翻译完成，并已对照原始 PDF（41 页 Accepted Manuscript）逐页核验（`done`）
- **图件资产**：全部 21 幅插图已提取并保存至 `literature/topopt/assets/Bruggi2016_Fig1.png` ~ `Bruggi2016_Fig21.png`
- **底本说明**：本仓库所存 PDF 为 Elsevier *Accepted Manuscript*（41 页，PII `S0045-7825(16)30092-5`，Reference `CMA 10881`），非最终排版版；图件上可见 "ACCEPTED MANUSCRIPT" 斜向水印，按原样保留未作清除。正文节号、式号、图表号与正式版一致，页码不一致。

---

# 摘要

近年来，人们提出了若干新的混合有限元族，用以在规则网格上分析线弹性体，且每个单元所需的自由度数目有限。本文实现了一种二维混合离散格式，据此构造出一类可替代的拓扑优化问题：其中应力充当主变量，且可压缩与不可压缩材料均可处理。结构柔顺度通过余能（complementary energy）的计算得到，而应力约束的施加则十分直接。数值模拟考察了所提方法的特征：针对可压缩材料，给出了与常规位移格式的对比；并引入了不可压缩介质结构的应力约束解。

**关键词**：拓扑优化 (topology optimization)；混合有限元 (mixed finite elements)；余能 (complementary energy)；不可压缩材料 (incompressible materials)；应力约束 (stress constraints)

---

# 1. 引言 (Introduction)

应力约束拓扑优化是一种有效工具，用于探索相对于材料强度或任何涉及应力场的给定要求而言完全可行的构型，参见文献 [1, 2, 3]。在处理离散的应力约束优化设计问题时，一个关键问题是选择这样一种有限元离散格式：它在应力场的评估中既稳健又精确，同时保持分析的计算代价处于合理水平。文献中给出的多数数值方法都采用基于位移的有限元，参见文献 [4, 5, 6, 7, 8]。当位移作为格式的主变量时，应力场通过后处理技术计算得到，并不属于问题的直接变量。由于众所周知的自锁（locking）现象，这些方法无法用于处理由不可压缩材料构成的结构。

作为替代途径，稳定的混合有限元已被用于克服自锁现象，用于处理不可压缩材料结构的能量类设计（参见文献 [9, 10, 11]），或者用于处理涉及"流体相"的优化过程（参见文献 [12, 13, 14, 15]）。混合有限元还可用于提高应力场评估的精度，这取决于单元中所嵌入的形函数 [16]。混合方法把应力纳入弹性问题的直接变量，从而无需任何后处理手段即可施加强度约束并计算相应灵敏度。这一思路最早在文献 [17] 中实现，其所用的有限元离散仍以位移为主变量，且仅限于可压缩材料。

必须指出，以应力为主变量来求解弹性问题——即构造所谓的"真混合"（truly–mixed）有限元问题 [18]——并非易事。在这一版本中，Hellinger–Reissner 变分原理要求应力具有正则性，而位移则可以是间断的。能够满足众所周知的 Babuška–Brezzi 条件的有限元数量十分有限。经典的稳健离散格式或是基于特制的复合有限元 [19]，或是以弱形式嵌入应力张量的对称性要求（参见文献 [20] 等）。一般而言，这两类方案都涉及每个单元大量自由度的处理，因而分析本身的计算代价不可忽略，进而导致完成任何优化过程都需要很高的 CPU 时间 [21]。出于这一原因，此类单元在拓扑优化中的应用局限于忽略材料强度要求的能量类问题，参见文献 [9, 13]。

最近，一族新的二维与三维"真混合"有限元被提出，它专门为规则网格上的计算而设计 [22]。采用正方形或立方体有限元的离散，可以高效地同时实现应力张量的对称性以及对其作为问题主变量所要求的正则性。与常规"真混合"离散相比，每个单元的自由度数目显著下降，而良好的收敛率与对不可压缩材料的完全稳定性则得以保留。这些特性可以在拓扑优化中加以利用，从而考察在可压缩材料的应力约束设计中采用其他有限元逼近的可能性，同时处理具有给定强度要求的不可压缩材料结构的优化设计。

本文实现了这一新族中最低阶的二维"真混合"有限元，用以构造一种仅以"真混合"弹性问题的主变量（即应力）表述的可替代拓扑优化问题。正如文献 [23] 所考察的那样，该格式以结构重量作为目标函数，包含一个用于控制变形能力的能量类约束，以及在需要时用于控制不期望的应力峰值的一组选定约束。在评估结构柔顺度时，不使用基于位移的应变能，而是采用基于应力的余能。

文中给出了数值考察，以评估所提出的基于应力的框架的特征，并给出与可压缩材料常规位移格式的对比。此外还讨论了不可压缩介质构成的结构的应力约束优化。

本文的结构安排如下。第 2 节介绍 Hellinger–Reissner 变分原理，以及在平面问题模拟中所采用的高效四边形混合有限元。第 3 节给出基于经典 SIMP 模型 [24] 的拓扑优化问题的基本内容（此处针对柔度张量而非刚度张量书写），并处理在所采用的基于应力的离散格式中结构柔顺度与应力约束的计算。第 4 节给出最小重量、带柔顺度与应力约束的格式，并讨论若干相关数值问题，例如约束的施加策略以及针对众所周知的奇异性问题所作的数学松弛。第 5 节致力于数值模拟。首先进行初步数值考察，将所采用的混合有限元与采用位移场双线性逼近的常规四节点单元在收敛特性上作对比。随后，将第 3 节引入的格式用于涉及可压缩与不可压缩材料的优化设计问题。第 6 节对全文作结，就所作考察与所引入的应力驱动框架给出若干评述。

---

# 2. 弹性问题 (The elasticity problem)

## 2.1. 连续格式 (Continuous formulation)

本节给出 Hellinger–Reissner 变分原理的"真混合"版本的基本内容：该变分格式以应力为问题的主变量，而位移则扮演 Lagrange 乘子的角色，参见文献 [18]。

考虑具有正则边界 $\partial\Omega$ 的均质域 $\Omega \in \mathbb{R}^2$，并设 $\partial\Omega = \Gamma_d \cup \Gamma_t$。分量为 $\overline{u}_j$ 的给定位移与分量为 $\overline{f}_j$ 的给定面力分别施加在 $\Gamma_d$ 与 $\Gamma_t$ 上。设 $\boldsymbol{\sigma}$ 为未知应力场，$\mathbf{u}$ 为未知位移场，而 $\overline{g}_j$ 为平方可积体载荷矢量的分量。$S_{ijhk}$ 是线弹性各向同性材料的四阶柔度张量，即本构关系逆形式的线性映射，它按

$$\varepsilon_{ij} = S_{ijhk}\,\sigma_{hk}, \qquad \varepsilon_{ij} = (u_{i,j} + u_{j,i})/2$$

把应力变换为应变。于是，"真混合"弱形式可写为：求 $(\boldsymbol{\sigma}, \mathbf{u}) \in H \times W$，使得 $\sigma_{ij} n_i |_{\Gamma_t} = \overline{f}_j$ 且

$$
\left\{
\begin{aligned}
&\int_{\Omega} S_{ijhk}\,\sigma_{hk}\,\tau_{ij}\,\mathrm{d}x + \int_{\Omega} \tau_{ij,i}\,u_j\,\mathrm{d}x = \int_{\Gamma_d} \overline{u}_j\,\tau_{ij}\,n_i\,\mathrm{d}s, && \forall \boldsymbol{\tau} \in H, \\[2mm]
&\int_{\Omega} \sigma_{ij,i}\,v_j\,\mathrm{d}x = -\int_{\Omega} \overline{g}_j\,v_j\,\mathrm{d}x, && \forall \mathbf{v} \in W,
\end{aligned}
\right.
\tag{1}
$$

其中 $n_j$ 表示 $\partial\Omega$ 上法向矢量的分量。

式 (1)$_1$ 由相容方程与逆形式本构律以虚应力场 $\boldsymbol{\tau}$ 作检验而得。由于随后应用了 Gauss–Green 公式，方程中出现了应力场的散度以及右端的线积分。平衡方程以虚位移场 $\mathbf{v}$ 作检验，给出式 (1)$_2$。

函数空间 $H$ 与 $W$ 可以直接由"使所涉积分有意义"这一要求导出。应力场 $\boldsymbol{\sigma}$ 是该格式的主变量，在如下正则空间中求解：

$$H = H(\mathrm{div};\Omega) = \left\{ \boldsymbol{\sigma} : \sigma_{ij} = \sigma_{ji},\ \sigma_{ij} \in L^2(\Omega),\ \sigma_{ij,i} \in L^2(\Omega) \right\}. \tag{2}$$

位移甚至可以是间断的，因为上述泛函定义中所需的唯一要求就是其平方可积性，即：

$$W = \left\{ \mathbf{u} : u_j \in L^2(\Omega) \right\}. \tag{3}$$

值得指出的是，面力边界条件是先验地施加在应力张量的空间上的，而位移边界条件则由变分原理产生，即它出现在式 (1)$_1$ 的右端。事实上，应力是"真混合"问题的主变量，边界条件的施加相对于常规基于位移的框架而言是对偶的，详见下文。

## 2.2. 有限元离散 (Finite element discretization)

本节讨论上一节所引入的"真混合"变分格式的有限元离散。存在一个严格的稳健性要求，即所谓的 inf–sup 条件或 Babuška–Brezzi (BB) 条件，它支配着任何可用离散格式的实现，参见文献 [18]。对可压缩与不可压缩介质均稳定的离散格式为数极少，且所需自由度远多于常规的基于位移的有限元。文献 [22] 最近提出了一族新单元，用以利用任意空间维数下网格的规则性，从而高效地获得稳健的离散。本文实现其中最低阶的单元来处理二维问题。

![[Bruggi2016_Fig1.png]]

<center><b>
图 1：HMZ 混合有限元的自由度。
</b></center>

所采用的单元对全局间断位移场的每个笛卡尔分量 $u_j$ 采用属于 $P_1(x_j) := \mathrm{span}\{1, x_j\}$ 的函数进行插值，这意味着通过线性多项式逼近二维场需要四个自由度（见图 1 中以三角形标记的自由度）。就位移场而言，属于矩形网格 $\mathcal{T}_h$ 的单元 $K$ 上的有限元空间因此为：

$$V(K) = \mathrm{span} \left\{ \begin{matrix} \{1,\, x_1\} \\ \{1,\, x_2\} \end{matrix} \right\}, \tag{4}$$

相应的自由度为：

$$\frac{1}{|K|}\int_K u_j\, v\,\mathrm{d}x, \qquad \text{对所有 } v \in P_1(x_j),\ j = 1, 2. \tag{5}$$

至于应力场的插值，张量的法向分量与切向分量（分别为 $\sigma_{ii}$ 与 $\sigma_{ij}$）采用不同的逼近。前者通过属于 $P_2(x_i) := \mathrm{span}\{1, x_i, x_i^2\}$ 的函数处理，后者则在 $Q_1(x_i, x_j) := \mathrm{span}\{1, x_i, x_j, x_i x_j\}$ 中求解。事实上，由于对空间 $H = H(\mathrm{div};\Omega)$ 的要求，$\sigma_{ii}$ 必须沿 $x_i$ 连续，而 $\sigma_{ij}$ 必须沿 $x_i$ 与 $x_j$ 两个方向都连续。对法向应力分量 $\sigma_{ii}$ 的导数只出现在 $x_i$ 方向，而对 $\sigma_{ij}$ 的导数则出现在 $x_i$ 与 $x_j$ 方向。这一事实说明了为什么法向应力分量使用二次多项式 $P_2(x_i)$，而剪应力分量使用双线性多项式 $Q_1(x_i, x_j)$。表示应力场需要十个自由度（见图 1 中以圆圈标记的自由度）。就应力场而言，属于矩形网格 $\mathcal{T}_h$ 的单元 $K$ 上的有限元空间因此为：

$$\Sigma(K) = \mathrm{span} \left\{ \begin{matrix} \{1,\, x_1,\, x_1^2\} & \{1,\, x_1,\, x_2,\, x_1 x_2\} \\ \{1,\, x_1,\, x_2,\, x_1 x_2\} & \{1,\, x_2,\, x_2^2\} \end{matrix} \right\}. \tag{6}$$

法向应力分量的相应自由度为：

$$
\begin{aligned}
&\frac{1}{|F_{x_i,K}|}\int_{F_{x_i,K}} \sigma_{ii}\,\mathrm{d}s, \qquad \text{对所有 } F_{x_i,K},\ i = 1, 2, \\[2mm]
&\frac{1}{|K|}\int_K \sigma_{ii}\,\mathrm{d}x, \qquad i = 1, 2,
\end{aligned}
\tag{7}
$$

其中 $F_{x_i,K}$ 是 $K$ 中垂直于 $x_i$ 轴的边。切向分量的相应自由度是在矩形单元 $K$ 各顶点处取值的剪应力。关于所考虑的这一族混合有限元的形函数与自由度的更多细节，可参见文献 [25, 26, 27]。

必须指出，式 (1) 的"真混合"本质在离散层面也有重要后果。应力是该格式的主变量，这意味着 $\Gamma_t$ 上的边界条件必须以强形式施加。给定载荷以指定的应力自由度施加，而位移边界条件则相反地通过式 (1)$_1$ 的线积分以弱形式施加。若在 $\Gamma_d$ 上 $\overline{u}_j = 0$，则对偶的应力自由度不作指定，从而使式 (1)$_1$ 右端的相应线积分归零。在此情形下，且假设不存在体载荷，"真混合"问题的离散形式为：

$$
\begin{bmatrix} \mathbf{A}_{\sigma\sigma} & \mathbf{B}_{\sigma u} \\ \mathbf{B}_{u\sigma} & \mathbf{0} \end{bmatrix}
\begin{Bmatrix} \boldsymbol{\sigma} \\ \mathbf{u} \end{Bmatrix}
= \begin{Bmatrix} \mathbf{0} \\ \mathbf{0} \end{Bmatrix},
\tag{8}
$$

上述矩阵的每个分块都可以由式 (1) 的陈述轻易得到，注意双线性型是按其计算中所涉及的自由度来标记的。混合问题的未知量矢量由应力未知量子矢量 $\boldsymbol{\sigma}$ 与位移未知量子矢量 $\mathbf{u}$ 构成。值得回顾的是，只有 $\mathbf{A}_{\sigma\sigma}$ 这一项与材料的本构律有关。

---

# 3. 拓扑优化问题 (The topology optimization problem)

## 3.1. 余能与应力度量 (Complementary energy and stress measure)

设 $\rho(\chi)$ 为一有界函数，满足在 $\Omega$ 中 $0 < \rho \le 1$，表示所考虑域内的材料密度。第 2.1 节引入的四阶柔度张量 $S_{ijhk}$ 依赖于点 $\chi \in \Omega$ 处的材料密度。按照最初为弹性张量建立的固体各向同性材料惩罚（Solid Isotropic Material with Penalization, SIMP）模型 [28, 29]，线弹性固体本构律逆形式的惩罚可写为：

$$S_{ijhk}(\rho(\chi)) = \rho(\chi)^{-p}\, S^0_{ijhk}, \tag{9}$$

其中 $S^0_{ijhk} = -\dfrac{\nu}{E}\delta_{ij}\delta_{hk} + \dfrac{1+\nu}{E}\left(\delta_{ih}\delta_{jk} + \delta_{ik}\delta_{jh}\right)$ 是给定各向同性介质的柔度张量，其工程常数为 $E$（杨氏模量）与 $\nu$（泊松比）。[^1] $p > 1$ 是惩罚参数，可按文献 [30] 等取为 3。

上式适用于可压缩弹性，但不能用于处理涉及不可压缩介质的平面应变问题。事实上，式 (9) 按密度未知量 $\rho$ 的取值对 $E$ 施加惩罚，却未对 $\nu$ 引入任何惩罚。这会导致出现不期望的最小密度区域，它们表现出非零应力，并向最优设计提供非物理的刚度，参见文献 [12]。

为避免此类数值问题，可以用各向同性材料的体积模量与剪切模量来书写本构方程，即 $K = \dfrac{E}{3(1-2\nu)}$ 与 $G = \dfrac{E}{2(1+\nu)}$，并采用不同的 SIMP 型插值，以便对任意 $\rho < 1$ 实现对四阶柔度张量 $S_{ijhk}$ 的有效惩罚。分别以 $\sigma^I_{ij}$ 与 $\sigma^D_{ij}$ 记应力张量的球量部分与偏量部分，以 $\varepsilon^I_{ij}$ 与 $\varepsilon^D_{ij}$ 记应变张量的球量分量与偏量分量，则有：

$$\varepsilon^I_{ij} = \rho(\chi)^{-p_K}\,\frac{1}{3K}\,\sigma^I_{ij}, \qquad \varepsilon^D_{ij} = \rho(\chi)^{-p_G}\,\frac{1}{2G}\,\sigma^D_{ij}. \tag{10}$$

取指数 $p_K$ 大于 $p_G$（数值模拟中取 $p_K = 6$、$p_G = 3$），即可对任意密度未知量 $\rho$ 取值实现合适的刚度惩罚，从而即使在不可压缩材料与平面应变假设下也能获得有效的最优构型，参见文献 [9]。式 (10) 所得到的构型与平面应力、可压缩材料下的拓扑优化基准结果完全一致。当 $p_K = p_G = p$ 时，即退化为式 (9) 的惩罚。

根据式 (1) 与式 (9)，可以定义所谓平衡状态下的结构柔顺度，它可用余能写为：

$$C = \int_{\Omega} \rho^{-p}\, S^0_{ijhk}\, \sigma_{hk}\, \sigma_{ij}\,\mathrm{d}x = \boldsymbol{\sigma}^T \mathbf{A}_{\sigma\sigma} \boldsymbol{\sigma} = \sum_{e=1}^{N} x_e^{-p}\, \boldsymbol{\sigma}_e^T \mathbf{A}^0_{\sigma\sigma,e}\, \boldsymbol{\sigma}_e, \tag{11}$$

其中 $\boldsymbol{\sigma}_e$ 是应力场的单元未知量矢量，$\mathbf{A}^0_{\sigma\sigma,e}$ 是对应于原始（未惩罚）材料的单元刚度矩阵分块，$x_e$ 是 $N$ 个单元密度所组成矢量 $\mathbf{x}$ 的第 $e$ 个分量。若使用式 (10) 的插值代替式 (9)，只需对式 (11) 作直接的修改即可。

为简洁起见，本文采用 von Mises 应力准则来处理最优设计中的应力峰值。也可以采用其他度量，以处理拉压行为不对称材料的强度或考虑疲劳，参见文献 [23, 2, 31]。在平面应力或平面应变假设下，定义可行性的等效应力度量 $\sigma^{eq}$ 所满足的相应不等式为：

$$\sigma^{eq} = \sqrt{3 J_{2D}} = \sqrt{\alpha_1 \sigma_{11}^2 + \alpha_1 \sigma_{22}^2 - \alpha_2 \sigma_{11}\sigma_{22} + 3\sigma_{12}^2} \le \sigma_L. \tag{12}$$

上式中 $\sigma_L$ 是材料强度，$J_{2D}$ 是第二偏应力不变量。$\alpha_1 = \alpha_2 = 1$ 给出适用于平面应力条件的公式；而 $\alpha_1 = 1 - \nu + \nu^2$ 与 $\alpha_2 = 1 + 2\nu - 2\nu^2$ 则计入了平面应变假设下出现的面外正应力 $\sigma_{33} = \nu(\sigma_{11} + \sigma_{22})$。

在求解式 (8) 之后，整个域内的应力状态都可通过问题的主变量 $\boldsymbol{\sigma}$ 得知。第 $e$ 个有限元中某个相关点（例如形心）处的总体应力可写成矢量形式 $\boldsymbol{\sigma}_e = \mathbf{T}_e \boldsymbol{\sigma}$，其中 $\boldsymbol{\sigma}_e = \{\sigma_{11}\ \ \sigma_{22}\ \ \sigma_{12}\}^T$，而 $\mathbf{T}_e$ 是一个矩阵，它挑选出第 $e$ 个单元的应力自由度，并利用第 2.2 节引入的应力形函数来计算 $\boldsymbol{\sigma}_e$ 的三个分量。借助文献 [32] 中详述的代数运算，式 (12) 中的不变量可以用"von Mises 应力矩阵" $\mathbf{M}_e$ 表示：

$$3 J_{2D,e} = \boldsymbol{\sigma}^T \mathbf{M}_e \boldsymbol{\sigma}, \qquad \mathbf{M}_e = \mathbf{T}_e^T \mathbf{V} \mathbf{T}_e, \qquad \mathbf{V} = \begin{bmatrix} \alpha_1 & -\alpha_2/2 & 0 \\ -\alpha_2/2 & \alpha_1 & 0 \\ 0 & 0 & 3 \end{bmatrix}. \tag{13}$$

因此，第 $e$ 个有限元的等效 von Mises 应力度量为：

$$\sigma^{eq}_e = \sqrt{\boldsymbol{\sigma}^T \mathbf{M}_e \boldsymbol{\sigma}}. \tag{14}$$

式 (12) 应当作用于密度为 $x_e$ 的单元的宏观应力 $\sigma_{ij}$。按照文献 [33]，多孔 SIMP 材料的适当失效准则应定义在表观"局部"应力 $\langle \sigma_{ij} \rangle$ 上，它可由 $\langle \sigma_{ij} \rangle = \sigma_{ij}/x_e^q$（$q > 1$）导出。与 SIMP 模型配合使用、作用于第 $e$ 个有限元的 von Mises 应力准则的合适形式为：

$$\frac{\langle \sigma^{eq}_e \rangle}{\sigma_L} = \frac{\sigma^{eq}_e}{x_e^q\, \sigma_L} \le 1, \tag{15}$$

其中 $\langle \sigma^{eq}_e \rangle$ 是第 $e$ 个有限元的等效 von Mises"局部"应力度量。为保持所采用插值模型在任意密度下的物理一致性，应取 $q = p$。

## 3.2. 问题构造 (Problem formulation)

经典的拓扑优化问题以柔顺度作为目标函数，并施加可用体积分数 $V_f$ 的约束以获得非平凡解 [30]。采用本文所给的"真混合"有限元方法，把结构柔顺度写成余能的两倍，并采用式 (9) 的刚度插值，则 MCW 格式（Minimum Compliance with Weight constraint，带重量约束的最小柔顺度）为：

$$
\left\{
\begin{aligned}
&\min_{x_{\min} \le x_e \le 1} && C = \sum_{e=1}^{N} x_e^{-p}\, \boldsymbol{\sigma}_e^T \mathbf{A}^0_{\sigma\sigma,e}\, \boldsymbol{\sigma}_e \\[2mm]
&\ \text{s.t.} && \begin{bmatrix} \mathbf{A}_{\sigma\sigma}(x_e^{-p}) & \mathbf{B}_{\sigma u} \\ \mathbf{B}_{u\sigma} & \mathbf{0} \end{bmatrix} \begin{Bmatrix} \boldsymbol{\sigma} \\ \mathbf{u} \end{Bmatrix} = \begin{Bmatrix} \mathbf{0} \\ \mathbf{0} \end{Bmatrix}, \\[2mm]
& && W / W_0 \le V_f.
\end{aligned}
\right.
\tag{16}
$$

上式中，目标函数是式 (11) 的结构柔顺度 $C$；式 (16)$_2$ 施加第 2.2 节讨论的离散平衡方程；式 (16)$_3$ 施加体积约束。最优设计的重量 $W$ 由单元密度 $x_e$ 乘以体积 $V_e$ 后对离散中的 $N$ 个单元求和得到，而 $W_0$ 代表整个设计区域的体积。对每个密度未知量 $x_e$ 施加下界 $x_{\min} > 0$，以避免式 (16)$_2$ 出现奇异。必须指出，上述问题是以应力表述的。位移是所采用有限元格式的次级变量，对目标函数没有任何贡献——目标函数完全由应力计算得到。

在给定外力作用下最小化结构的柔顺度 $C$，意味着最小化外载荷所作的功，即寻求刚硬的结构。在单个外力作用下，这等同于最小化加载点沿载荷方向的位移。这一途径就可用性（serviceability）而言对结构进行了优化，但并未计入任何防止其倒塌的强度要求。为处理后一问题，可以直接把式 (15) 的失效约束加入式 (16) 的格式中。为构成适定问题，此时应当谨慎选择体积分数 $V_f$，参见文献 [23]。为避免这一困难，可以构造 MWCS 问题，即带柔顺度与应力约束的最小重量（Minimum Weight formulation with Compliance and Stress constraints）格式：

$$
\left\{
\begin{aligned}
&\min_{x_{\min} \le x_e \le 1} && W = \sum_{N} x_e V_e \\[2mm]
&\ \text{s.t.} && \begin{bmatrix} \mathbf{A}_{\sigma\sigma}(x_e^{-p}) & \mathbf{B}_{\sigma u} \\ \mathbf{B}_{u\sigma} & \mathbf{0} \end{bmatrix} \begin{Bmatrix} \boldsymbol{\sigma} \\ \mathbf{u} \end{Bmatrix} = \begin{Bmatrix} \mathbf{0} \\ \mathbf{0} \end{Bmatrix}, \\[2mm]
& && C / C_L \le 1, \\[2mm]
& && \frac{\sigma^{eq}_e}{x_e^q\, \sigma_L} \le 1, \qquad e = 1, \ldots, N.
\end{aligned}
\right.
\tag{17}
$$

上式中，结构重量 $W$ 是目标函数；式 (17)$_3$ 是对总体刚度的约束，要求结构柔顺度 $C$ 低于给定极限 $C_L$。在单个外力作用下，该极限就是加载点沿载荷方向所允许的最大位移。式 (17)$_4$ 包含了作用于式 (15) 等效 von Mises 应力度量上的 $N$ 个局部应力约束。

式 (17) 的整个问题定义了一个同时嵌入可用性（柔顺度约束）与失效（强度约束）要求的最小重量格式。若略去式 (17)$_4$，便得到较简单的 MWC 问题，即带柔顺度约束的最小重量格式；若去掉式 (17)$_3$，便得到常规的 MWS 问题，即应力约束的最小重量格式，参见文献 [33]。

MWCS 设定可用于处理这样的优化设计问题：既对结构的变形能力给定阈值，又对材料强度设定极限。此外，它还可用于消除由式 (16) 的 MCW 设定所得最优设计中的任何应力集中。在这种情形下，$C_L$ 可取为 MCW 设定收敛时最优设计的柔顺度。

为简洁起见，数值部分将主要处理 MWC 问题以导出能量类构型。对柔顺度的给定极限按 $C_L = \alpha_C C_0$ 构造，其中 $C_0$ 是整个域由原始材料填满时所得的柔顺度，$\alpha_C$ 是给定参数。随后在需要时实施 MWCS 格式，以消除所得能量类构型中出现的任何应力集中。

必须指出，式 (17) 的离散格式中所处理的两类约束都是用有限元离散的主变量（即应力）表述的。特别地，应力度量可以直接从"真混合"设定的主未知量得到。这与常规的基于位移的框架有显著差别——后者为施加强度约束需要对变量作后处理。

把式 (16) 与式 (17) 特化到式 (10) 材料模型所需的修改是直接的，为简洁起见此处从略。

---

# 4. 数值问题 (Numerical issues)

## 4.1. 网格依赖性 (Mesh dependence)

本文采用移动渐近线方法（Method of Moving Asymptotes, MMA）[34]——一种成熟的凸序列规划途径——来迭代求解式 (17) 的离散问题。该算法搜寻密度未知量的最优集合，处理由单元常值密度离散与主场（即应力场）的二次/双线性插值所导出的柔顺度与等效应力度量。

众所周知，把单元常值密度离散与位移场双线性插值耦合起来的常规离散格式会出现不期望的棋盘格（checkerboard）模式。由于对应力场的插值较为精细，所采用的"真混合"离散设定不会出现此类数值不稳定。然而，无论采用何种变分原理，都必须处理网格依赖性，参见文献 [35, 36, 37]。本文按照文献 [1] 采用密度过滤途径，而不是像多数情形那样把过滤器作用于目标函数及其灵敏度。原设计变量 $x_e$ 被变换为一组新的物理未知量 $\tilde{x}_e$，即：

$$\tilde{x}_e = \frac{1}{\sum_N H_{el}} \sum_N H_{el}\, x_l, \qquad H_{el} = \sum_N \max\big(0,\ r_{\min} - \mathrm{dist}(e, l)\big). \tag{18}$$

上式中 $\mathrm{dist}(e, l)$ 是第 $e$ 个与第 $l$ 个单元形心之间的距离，$r_{\min} > d_m$ 是过滤半径，$d_m$ 是网格中有限元的参考尺寸。[^2]参数 $r_{\min}$ 对设计中任何构件的最小厚度提供了一种启发式控制。第 5 节给出的数值模拟中取 $r_{\min} = 2 d_m$。

## 4.2. 约束的活跃集 (Active set of constraints)

MWCS 设定主要由式 (17)$_3$ 的柔顺度约束驱动，而局部约束则把解引导至相对于给定强度准则完全可行的构型。按照文献 [23]，从式 (17)$_4$ 的应力约束中挑选出一个受限子集传给 MMA，其主要目的是减少计算灵敏度信息所需的时间，并在处理多约束离散问题时改善优化器的性能。在接下来给出的数值模拟中，第一步只处理左端项 $\ge 0.65$ 的约束。该阈值线性增大，直到第 15 次迭代，此后固定为 0.95。在每一步中，这一挑选把 $N$ 个应力约束的全集缩减为 $N_a \le N$ 个。

所采用的策略在 $N_a \ll N$ 时给出最佳性能，这意味着以稳健的单元级控制和可接受的计算量来处理少数几个局部应力峰值。如上所述，第 5 节实施 MWCS 格式的主要目的，是消除此前由 MWC 设定所得能量类最优构型中出现的局部应力集中。对于需要在大片区域上控制应力场的 MWCS 问题，或者无法从柔顺度约束获益的 MWS 问题，可以借助文献中提出的其他途径稳健地加以处理，特别可参考涉及增强型全局约束或聚合局部约束集合的有效技术，参见文献 [1, 4, 2]。

## 4.3. 应力约束松弛 (Stress constraints relaxation)

众所周知的奇异性问题可能导致优化收敛不良，使优化器无法找到所期望的纯 0–1 设计。这一问题主要源于式 (15) 所定义的、用于处理中间密度的"局部"应力的渐近行为。正如第 3.1 节已经回顾的，为在多孔 SIMP 材料弹性性质与强度性质的建模中实现完全的物理一致性，应取 $p = q$。遗憾的是，若该假设成立，则当材料密度趋于零时"局部"应力仍保持有限（非零），约束方程的可行集可能包含一些零测度的退化子域。这对基于梯度的优化器而言是关键困难，因为它们无法找到位于这些退化子区域中的任何全局最优解，从而陷入表现为大片灰度区的不期望局部最优。

克服这一问题的经典做法是对施加应力约束的方程采用合适的数学松弛。关于众所周知的 $\varepsilon$–松弛的细节可参见文献 [38]。类似地，取指数 $q < p$，可以在低密度区引入强松弛，而不会在满密度处造成任何显著偏差，参见文献 [23] 等。这可以防止优化器收敛到不期望的局部极小，同时在满材料区域保持对强度约束的稳健施加。式 (17)$_4$ 约束的松弛形式与未松弛形式在解析形式上完全相同。由于在所提出的方法中应力既是优化问题也是有限元问题的主变量，因此无需任何额外处理。接下来给出的数值模拟中取 $q = 2.8$。

## 4.4. 灵敏度计算 (Sensitivity computation)

第 3.2 节所引入的最小化过程在每次迭代中都需要计算基于应力的柔顺度 $C$ 的灵敏度。式 (17) 还迭代地要求所选局部应力约束集合的灵敏度。重量函数 $W$ 关于密度未知量的导数在优化开始前一次性求出。

把基于应力的柔顺度 $C$ 对密度未知量 $x_k$ 求导，得到：

$$\frac{\partial C}{\partial x_k} = \frac{\partial \boldsymbol{\sigma}^T}{\partial x_k} \mathbf{A}_{\sigma\sigma} \boldsymbol{\sigma} + \boldsymbol{\sigma}^T \left( \frac{\partial \mathbf{A}_{\sigma\sigma}}{\partial x_k} \boldsymbol{\sigma} + \mathbf{A}_{\sigma\sigma} \frac{\partial \boldsymbol{\sigma}}{\partial x_k} \right). \tag{19}$$

把式 (8) 中"真混合"弹性平衡的第一行对同一密度未知量求导，可知括号中的项为：

$$\frac{\partial \mathbf{A}_{\sigma\sigma}}{\partial x_k} \boldsymbol{\sigma} + \mathbf{A}_{\sigma\sigma} \frac{\partial \boldsymbol{\sigma}}{\partial x_k} = -\mathbf{B}_{\sigma u} \frac{\partial \mathbf{u}}{\partial x_k}. \tag{20}$$

把上式转置并右乘主未知量矢量 $\boldsymbol{\sigma}$，还可以写出：

$$\frac{\partial \boldsymbol{\sigma}^T}{\partial x_k} \mathbf{A}_{\sigma\sigma} \boldsymbol{\sigma} = -\frac{\partial \mathbf{u}^T}{\partial x_k} \mathbf{B}_{\sigma u}^T \boldsymbol{\sigma} - \boldsymbol{\sigma}^T \frac{\partial \mathbf{A}_{\sigma\sigma}}{\partial x_k} \boldsymbol{\sigma}. \tag{21}$$

把式 (20–21) 代入式 (19)，并注意到式 (8) 中"真混合"弹性平衡的第二行要求 $\mathbf{B}_{u\sigma}\boldsymbol{\sigma} = \mathbf{B}_{\sigma u}^T \boldsymbol{\sigma} = \mathbf{0}$，可以断言 $C$ 关于未知密度 $x_k$ 的导数为：

$$\frac{\partial C}{\partial x_k} = -\boldsymbol{\sigma}^T \frac{\partial \mathbf{A}_{\sigma\sigma}}{\partial x_k} \boldsymbol{\sigma} = p\, x_k^{-p-1}\, \boldsymbol{\sigma}_k^T \mathbf{A}^0_{\sigma\sigma,k}\, \boldsymbol{\sigma}_k. \tag{22}$$

式 (17)$_4$ 中应力约束的灵敏度需要一些额外的计算量。回顾式 (15)，所采用的松弛使得第 $e$ 个有限元的等效 von Mises"局部"应力度量 $\langle \sigma^{eq}_e \rangle$ 关于未知密度 $x_k$ 的导数可以直接写出，即：

$$\frac{\partial \langle \sigma^{eq}_e \rangle}{\partial x_k} = -q\, \delta_{ek}\, x_e^{-q-1}\, \sigma^{eq}_e + \frac{\partial \sigma^{eq}_e}{\partial x_k}\, x_e^{-q}, \tag{23}$$

其中 $\delta_{ek}$ 是 Kronecker 符号，当 $e = k$ 时等于 1，当 $e \ne k$ 时等于 0。

由于活跃应力约束的个数 $N_a$ 一般小于设计变量的个数 $N$，本文在计算 $\sigma^{eq}_e$ 的导数时采用伴随法（adjoint method）而非直接法，另见文献 [32] 与 [23]。第 $e$ 个有限元的等效 von Mises"局部"应力度量 $\langle \sigma^{eq}_e \rangle$ 关于未知密度 $x_k$ 的导数为：

$$\frac{\partial \sigma^{eq}_e}{\partial x_k} = -\widetilde{\boldsymbol{\sigma}}^T \frac{\partial \mathbf{A}_{\sigma\sigma}}{\partial x_k} \boldsymbol{\sigma}, \qquad \begin{bmatrix} \mathbf{A}_{\sigma\sigma} & \mathbf{B}_{\sigma u} \\ \mathbf{B}_{u\sigma} & \mathbf{0} \end{bmatrix} \begin{Bmatrix} \widetilde{\boldsymbol{\sigma}} \\ \widetilde{\mathbf{u}} \end{Bmatrix} = \begin{bmatrix} (\boldsymbol{\sigma}^T \mathbf{M}_e \boldsymbol{\sigma})^{-\frac{1}{2}} \mathbf{M}_e \boldsymbol{\sigma} \\ \mathbf{0} \end{bmatrix}, \tag{24}$$

这意味着每个活跃约束都需要对式 (17)$_2$ 的线性系统额外求解一个载荷工况。

最后必须指出，密度过滤器的使用意味着目标函数与全部约束的灵敏度都需要作链式法则的修正。事实上，需要计算关于物理未知量 $\tilde{x}_e$ 的导数。

---

# 5. 数值模拟 (Numerical simulations)

## 5.1. 初步考察："真混合"单元 vs 位移单元 (A preliminary investigation: "truly–mixed" element vs displacement–based element)

首先进行一项数值考察，以评估所实现"真混合"有限元的收敛特性与稳定性。文中给出了与四节点位移有限元的对比，涵盖可压缩与准不可压缩平面应变弹性两种情形。

![[Bruggi2016_Fig2.png]]

<center><b>
图 2：初步考察。几何与边界条件。
</b></center>

图 2 给出所考虑基准问题的几何与边界条件，以及计算应力的点 $A$ 的位置。在"真混合"设定中，$\Gamma_d$ 与 $\Gamma_t$ 上的施加按第 2.2 节进行。具体而言，置零的应力自由度为：下边界上的 $\sigma_{yy}$、$\sigma_{xy}$，上边界上的 $\sigma_{xy}$，以及竖直边上的 $\sigma_{xx}$。上边界上 $\sigma_{yy}$ 的应力自由度置为外压 $w$，以施加沿试件上边界的载荷。

应力张量各分量的解析表达式可由 Airy 应力函数导出，为：

$$\sigma_{xx} = \frac{w}{2I}(l^2 - x^2)y + \frac{w}{I}\left(\frac{y^3}{3} - \frac{c^2 y}{5}\right), \quad \sigma_{yy} = -\frac{w}{2I}\left(\frac{y^3}{3} - c^2 y + \frac{2}{3}c^3\right), \quad \sigma_{xy} = \frac{w}{2I}x(c^2 - y^2), \tag{25}$$

其中 $w = c = 1$，$l = 3c$，$I = 2/3\,c^3$。

首先考虑 $\nu = 0.3$ 的情形。图 3(a)–(c) 给出 $\sigma_{xx}$、$\sigma_{yy}$、$\sigma_{xy}$ 计算值的收敛曲线，横坐标为沿梁高方向的有限元个数 $n$。所采用网格的单元数为 $48 \le 3n \cdot n \le 49{,}152$。所有曲线都收敛到对应式 (25) 精确解的水平渐近平台。直接对作为"真混合"格式主变量的应力场进行插值的二次与双线性多项式，相对于常规四节点有限元中用来逼近位移场的双线性插值之梯度，提供了更高的精度。这与文献 [22] 所给出的、关于所实现混合有限元收敛性质的理论与数值结果一致。

![[Bruggi2016_Fig3.png]]

<center><b>
图 3：通过"真混合"单元与四节点位移单元在 $A$ 点计算得到的应力张量各分量的收敛性：$\sigma_{xx}$ (a)、$\sigma_{yy}$ (b)、$\sigma_{xy}$ (c)、von Mises 等效应力 $\sigma_{VM}$ (d)。平面应变假设，$E = 1\,\mathrm{N/m^2}$，$\nu = 0.3$。
</b></center>

如第 3.1 节所详述，在处理优化设计时采用 von Mises 等效应力 $\sigma_{VM}$ 来控制局部失效。图 3(d) 给出应力度量 $\sigma_{VM}$ 的收敛曲线，它由计算所得的应力张量各分量按式 (12) 左端组合而成。值得指出的是，"真混合"格式比常规位移有限元更快地逼近最终渐近值。

<center><b>
表 1：图 3 所示模拟的 CPU 时间（秒）。
</b></center>

| $n$ | 位移格式<br>总时间 | 位移格式<br>求解平衡方程时间 | 真混合格式<br>总时间 | 真混合格式<br>求解平衡方程时间 |
|:---:|:---:|:---:|:---:|:---:|
| 4 | 2.505 | 0.001 | 4.538 | 0.003 |
| 8 | 2.526 | 0.002 | 4.543 | 0.010 |
| 16 | 2.574 | 0.005 | 4.625 | 0.044 |
| 32 | 2.770 | 0.026 | 4.882 | 0.274 |
| 64 | 3.106 | 0.114 | 6.135 | 1.087 |
| 128 | 7.804 | 0.561 | 17.431 | 7.271 |

表 1 给出上述模拟的计算代价，列出了每次有限元分析运行完整代码所需的总 CPU 时间，以及求解离散平衡方程组所花费的部分 CPU 时间。此处采用 Matlab 的反斜杠算子，与文献 [22] 测试 HMZ 单元时的实现一致。当然，在"真混合"框架中，形函数的构造与全局矩阵的组装更为耗时。应力场的直接离散显著增加了求解平衡方程所涉及的自由度数目，因而相对于低阶位移途径需要更高的计算代价。然而必须指出，相对于常规的"真混合"离散（参见文献 [19] 等），HMZ 单元可以节省大量未知量；而且在处理式 (8) 的鞍点问题时，可以采用专门的求解器来提高计算效率，特别参见文献 [39]。

![[Bruggi2016_Fig4.png]]

<center><b>
图 4：通过"真混合"单元与四节点位移单元计算得到的柔顺度：收敛性 (a) 与误差 (b)。平面应变假设，$E = 1\,\mathrm{N/m^2}$，$\nu = 0.3$。
</b></center>

关于最优设计变形能力的要求，第 3.1 节也已表明这是通过结构柔顺度 $C$ 来处理的。在常规位移格式中，该量按 $\mathbf{u}^T \mathbf{K} \mathbf{u}$ 计算，其中 $\mathbf{u}$ 是主位移未知量矢量，$\mathbf{K}$ 是总体刚度矩阵。在所引入的"真混合"设定中，$C$ 以余能表述，并按式 (11) 由应力未知量计算。图 4(a) 表明相应的收敛曲线以可比的收敛速率趋于同一最终值。以该值作为参考解，图 4(b) 给出误差曲线，突出了"真混合"有限元略优的表现。

![[Bruggi2016_Fig5.png]]

<center><b>
图 5：通过"真混合"单元与四节点位移单元在 $A$ 点计算得到的应力张量各分量的收敛性：$\sigma_{xx}$ (a)、$\sigma_{yy}$ (b)、$\sigma_{xy}$ (c)、von Mises 等效应力 $\sigma_{VM}$ (d)。平面应变假设，$E = 1\,\mathrm{N/m^2}$，$\nu = 0.49$。
</b></center>

众所周知，基于位移的有限元在处理平面应变条件下的不可压缩或准不可压缩材料时会出现自锁，即收敛性的严重丧失，特别参见文献 [18]。为评估此处所考虑各单元的表现，对 $\nu = 0.49$ 重复上述数值考察。图 5(a)–(d) 给出应力张量各分量以及 von Mises 应力度量的收敛曲线。容易看出，就"真混合"离散的结果而言，与图 3(a)–(d) 相比没有任何差别。相反，位移逼近的收敛率显著变差。

![[Bruggi2016_Fig6.png]]

<center><b>
图 6：通过"真混合"单元与四节点位移单元计算得到的柔顺度：收敛性 (a) 与误差 (b)。平面应变假设，$E = 1\,\mathrm{N/m^2}$，$\nu = 0.49$。
</b></center>

图 6 指出，在总体柔顺度的评估上也可以看到类似的行为。当 $\nu \to 0.5$ 时，位移逼近所表现出的数值不稳定在应力与柔顺度两方面都变得严重，而所考虑的"真混合"离散即使对不可压缩弹性问题也保持完全稳定，细节参见文献 [22]。

## 5.2. 算例 1：基于应力的优化 vs 基于位移的优化 (Example 1: stress–based optimization vs displacement–based optimization)

![[Bruggi2016_Fig7.png]]

<center><b>
图 7：算例 1–3。数值应用的几何与边界条件。尺寸单位为 m，力的单位为 N。
</b></center>

本节给出通过第 3.2 节所引入的基于应力的格式所得结果，应用于 L 形悬臂梁优化设计这一基准算例（见图 7），考虑 MWC 与 MWCS 两类问题。对这两类问题都给出了与常规位移格式的对比。

此处假设材料的杨氏模量 $E = 1\,\mathrm{N/m^2}$、泊松比 $\nu = 0.3$。所采用的规则网格由 4096 个单位厚度的正方形单元构成，处于平面应力条件下。最优设计以所采用过滤格式的物理未知量集合给出，同时给出展示式 (12) 所定义单元等效 von Mises 应力度量 $\sigma^{eq}$ 的云图。

表 2 从无量纲重量 $W/W_0$、无量纲柔顺度 $C/C_0$ 以及最大 von Mises 等效应力 $\sigma^{eq}_{\max}$ 三个方面比较所得的最优构型。下标 0 表示与整个域由原始材料填满时相关的量。收敛时的重量与柔顺度除以优化过程第一次迭代（此时 $x_e = 1,\ \forall e$）所计算的相应值。表中还给出了收敛时所处理的活跃约束个数 $N_a^C$。

![[Bruggi2016_Fig8.png]]

<center><b>
图 8：算例 1。MWC 问题的最优拓扑。
</b></center>

图 8 给出在约束 $\alpha_C = 2.0$ 下、采用常规位移有限元框架通过 MWC 格式所得的最优设计。所得构型中加载点的竖向位移是整个域由原始材料填满时所得挠度的两倍。完全以应力实现的 MWC 过程（即按式 (17) 的格式）找到了同样的最优解。

![[Bruggi2016_Fig9.png]]

<center><b>
图 9：算例 1。求解 MWC 问题所得最优设计的 von Mises 应力云图：位移格式解 (a) 与应力格式解 (b)。
</b></center>

图 9 所示相应的 von Mises 应力云图指出，最大应力如预期出现在拐角区域附近。尽管最优构型相同，但通过位移离散所逼近的峰值应力与通过混合有限元方法所逼近的结果有显著差别。位移优化所读出的最大应力为 $\sigma^{eq}_{\max} = 9.7\,\mathrm{N/m^2}$，而基于应力的框架在附近位置得到 $\sigma^{eq}_{\max} = 10.2\,\mathrm{N/m^2}$。混合格式所提供的更精细逼近预期能够更准确地捕捉应力峰值。就目标函数的收敛而言没有发现显著差别，见图 10。

![[Bruggi2016_Fig10.png]]

<center><b>
图 10：算例 1。MWC 问题的收敛曲线。
</b></center>

上述结果与第 5.1 节所给出的、关于所采用有限元收敛特性的考察完全一致。事实上，所考虑的能量类问题完全由结构柔顺度驱动，而两种有限元途径对它的逼近精度几乎相同，特别参见图 4。这解释了为什么位移途径与混合方法找到了图 8 所示的同一最优设计。

![[Bruggi2016_Fig11.png]]

<center><b>
图 11：算例 1。MWCS 问题的最优拓扑：位移格式解 (a) 与应力格式解 (b)。
</b></center>

为在保持所得最优设计刚度的同时消除不期望的应力集中，实施同时计入柔顺度与应力约束的 MWCS 途径。图 11(a) 给出在 $\alpha_C = 2.0$ 与 $\sigma_L = 5.0\,\mathrm{N/m^2}$ 下、采用常规位移有限元框架所得的最优构型。如预期，拐角区域通过引入一组杆件来处理，它们把受拉应力流从几何奇异处引开，同时所有构件都具有合适的厚度以保持总体柔顺度。图 11(b) 给出以应力实现的 MWCS 过程（即按式 (17) 的格式）所得的最优解。按照对应力场的局部施加，两种构型中所得的最大应力相同，见图 12 的云图。

![[Bruggi2016_Fig12.png]]

<center><b>
图 12：算例 1。求解 MWCS 问题所得最优设计的 von Mises 应力云图：位移格式解 (a) 与应力格式解 (b)。
</b></center>

然而，由于应力场评估精度的不同，最优解中出现了一些差异，参见第 5.1 节。采用混合有限元的优化分布出远离几何奇异处的倾斜构件，而位移优化则在拐角周围布置了更多质量。此外，构成最优构型的杆件数目也不相同。

![[Bruggi2016_Fig13.png]]

<center><b>
图 13：算例 1。MWCS 问题的收敛曲线。
</b></center>

就目标函数的收敛（见图 13）以及收敛时活跃约束的个数（见表 2）而言，没有发现显著差别。

<center><b>
表 2：算例 1。以无量纲重量 $W/W_0$、柔顺度 $C$（$\mathrm{N\,m}$）、无量纲柔顺度 $C/C_0$、最大 von Mises 等效应力 $\sigma^{eq}_{\max}$（$\mathrm{N/m^2}$）以及收敛时活跃约束个数 $N_a^C$ 对最优构型作比较。下标 0 指整个域（原始材料）。
</b></center>

| 图 | 问题 | 格式 | $W/W_0$ | $C$ | $C/C_0$ | $\sigma^{eq}_{\max}$ | $N_a^C$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 8 | MWC | 位移格式 | 0.376 | 238.05 | 2.0 | 9.7 | 1 |
| 8 | MWC | 应力格式 | 0.381 | 241.25 | 2.0 | 10.2 | 1 |
| 11(a) | MWCS | 位移格式 | 0.399 | 238.05 | 2.0 | 5.0 | 55 |
| 11(b) | MWCS | 应力格式 | 0.403 | 241.25 | 2.0 | 5.0 | 54 |

## 5.3. 算例 2：可压缩 vs 不可压缩材料 (Example 2: compressible vs. incompressible material)

第二个算例针对图 7 所示的两端固支梁，通过所提出的基于应力的途径来处理可压缩与不可压缩两类材料。考虑 MWC 格式，取 $\alpha_C = 2.5$。此处假设杨氏模量 $E = 1\,\mathrm{N/m^2}$，泊松比取 $\nu = 0.3$ 或 $\nu = 0.5$。所采用的规则网格由 8192 个正方形单元构成，分别在平面应力与平面应变条件下计算。此处分析完整几何而非其一半，以检查最优构型的对称性。

![[Bruggi2016_Fig14.png]]

<center><b>
图 14：算例 2。MWC 问题的最优拓扑：平面应力 $\nu = 0.3$ (a) 与 $\nu = 0.5$ (b)，对比平面应变 $\nu = 0.3$ (c) 与 $\nu = 0.5$ (d)。
</b></center>

<center><b>
表 3：算例 2。针对不同材料性质假设，以无量纲重量 $W/W_0$、柔顺度 $C$（$\mathrm{N\,m}$）与无量纲柔顺度 $C/C_0$ 对最优构型作比较。下标 0 指整个域（原始材料）。
</b></center>

| 图 | 问题 | 假设 | $\nu$ | $W/W_0$ | $C$ | $C/C_0$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 14(a) | MWC | 平面应力 | 0.3 | 0.326 | 8.41 | 2.5 |
| 14(b) | MWC | 平面应力 | 0.5 | 0.324 | 8.63 | 2.5 |
| 14(c) | MWC | 平面应变 | 0.3 | 0.324 | 7.78 | 2.5 |
| 14(d) | MWC | 平面应变 | 0.5 | 0.323 | 6.86 | 2.5 |

图 14(a) 与 (b) 给出平面应力条件假设下、分别对应 $\nu = 0.3$ 与 $\nu = 0.5$ 的最优构型。图 14(c) 与 (d) 给出平面应变情形下相应的最优构型。

![[Bruggi2016_Fig15.png]]

<center><b>
图 15：算例 2。在平面应变、$\nu = 0.5$ 假设下求解 MWC 问题所得最优设计的 von Mises 应力云图。
</b></center>

图 15 给出图 14(d) 最优设计的 von Mises 应力云图，用以确认在平面应变条件下、域内没有为利用低密度处材料不可压缩性而出现的不可行区域，参见第 3.1 节。按照不可压缩介质优化设计的文献，平面应变设计倾向于采用厚实构件以及利用三轴、近乎各向同性应力状态的构型。的确，图 14(d) 的最优构型与其他构型有显著差别：材料在每个固支区域周围聚集，形成实体块而非采用细杆。

![[Bruggi2016_Fig16.png]]

<center><b>
图 16：算例 2。MWC 问题的收敛曲线。
</b></center>

由于所采用无自锁有限元的稳健性以及式 (10) 的刚度插值模型，所得全部结果都是纯 0–1 构型。对此处所考虑的各次模拟，目标函数的历史曲线没有显著差别，如图 16 所示。无论对可压缩还是不可压缩材料，平面应力设计与平面应变优化的收敛过程大致相同。

面外材料的贡献使得平面应变设计比相应的平面应力构型刚硬得多，见表 3。

## 5.4. 算例 3：不可压缩材料的应力约束拓扑优化 (Example 3: stress–constrained topology optimization of incompressible materials)

最后一个算例涉及图 7 所示的矩形悬臂梁。采用所提出的基于应力的途径处理杨氏模量 $E = 1\,\mathrm{N/m^2}$ 的不可压缩材料。在平面应力或平面应变假设下实施由 4704 个 HMZ 有限元构成的网格。

![[Bruggi2016_Fig17.png]]

<center><b>
图 17：算例 3。$\nu = 0.5$ 时 MWC 问题的最优拓扑：平面应力假设 (a) 与平面应变假设 (b)。
</b></center>

首先研究 MWC 问题，在柔顺度约束 $\alpha_C = 2.0$ 下获得刚硬构型。图 17(a) 给出平面应力假设下所得的最优构型，图 17(b) 则对应平面应变情形。图 17(a) 中出现的四根较细杆件在图 17(b) 中被两根较粗杆件所取代，这与上一算例的结论完全一致。

![[Bruggi2016_Fig18.png]]

<center><b>
图 18：算例 3。$\nu = 0.5$ 时求解 MWC 问题所得最优设计的 von Mises 应力云图：平面应力假设 (a) 与平面应变假设 (b)。
</b></center>

图 18 给出所得最优结果的相应 von Mises 应力云图，指出在两种情形下靠近地面约束处都出现了一些应力集中。如表 4 所示，平面应力下的应力峰值更高。事实上，面外效应在平面应变下缓解了材料的受力状态，这通过式 (12) 中的参数 $\alpha_1$ 与 $\alpha_2$ 加以计入。

![[Bruggi2016_Fig19.png]]

<center><b>
图 19：算例 3。$\nu = 0.5$ 时 MWCS 问题的最优拓扑：平面应力假设 (a) 与平面应变假设 (b)。
</b></center>

为在保持所需刚度的同时消除不期望的应力峰值，实施 MWCS 途径，取 $\alpha_C = 2.0$ 与 $\sigma_L = 12.0\,\mathrm{N/m^2}$。图 19(a) 给出平面应力假设下所得的最优构型，图 19(b) 则对应平面应变情形。

![[Bruggi2016_Fig20.png]]

<center><b>
图 20：算例 3。$\nu = 0.5$ 时求解 MWCS 问题所得最优设计的 von Mises 应力云图：平面应力假设 (a) 与平面应变假设 (b)。
</b></center>

按照图 20(a) 与 (b) 所给出的相应 von Mises 应力云图，最优构型中得到了近乎均匀的应力场。为实现这一结果，倾斜构件被直接连接到地面，而不是与水平构件相交。依据平面问题假设的不同还存在一些差异：在平面应力下倾斜构件与水平构件相邻，而在平面应变下两组杆件之间出现了完全分离。这是为了避免几何干涉对应力状态造成任何扰动。

![[Bruggi2016_Fig21.png]]

<center><b>
图 21：算例 3。MWCS 问题的收敛曲线。
</b></center>

<center><b>
表 4：算例 3。以无量纲重量 $W/W_0$、柔顺度 $C$（$\mathrm{N\,m}$）、无量纲柔顺度 $C/C_0$、最大 von Mises 等效应力 $\sigma^{eq}_{\max}$（$\mathrm{N/m^2}$）以及收敛时活跃约束个数 $N_a^C$ 对最优构型作比较。下标 0 指整个域（原始材料）。
</b></center>

| 图 | 问题 | 假设 | $W/W_0$ | $C$ | $C/C_0$ | $\sigma^{eq}_{\max}$ | $N_a^C$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 17(a) | MWC | 平面应力 | 0.440 | 41.64 | 2.0 | 21.72 | 1 |
| 17(b) | MWC | 平面应变 | 0.421 | 33.57 | 2.0 | 17.53 | 1 |
| 19(a) | MWCS | 平面应力 | 0.467 | 41.64 | 2.0 | 12.00 | 33 |
| 19(b) | MWCS | 平面应变 | 0.447 | 33.57 | 2.0 | 12.00 | 21 |

最后，图 21 给出此处所考虑应力约束问题的收敛曲线。没有出现数值不稳定，从而确认了所提途径不仅能处理能量类问题、也能处理不可压缩材料应力约束问题的稳健性。

---

# 6. 结论与展望 (Conclusions and perspectives)

本文引入了一种可替代的数值方法，用以在规则网格上处理由可压缩或不可压缩材料构成的结构的优化设计。所提出的途径基于采用一种新型"真混合"有限元，它相对于常规单元能够减少自由度数目，同时在应力场评估中保持良好精度并对自锁完全稳健。拓扑优化问题以应力为主变量构造，在重量最小化中同时实施柔顺度约束与应力约束。结构柔顺度通过余能的计算得到，而应力约束的施加十分直接。经典 SIMP 律被改写为对柔度张量施加惩罚。灵敏度计算完全以应力给出导数。

就可压缩介质而言，与常规位移方法的对比表明，最优构型可能受到所采用有限元收敛特性的影响。对于能量类问题，应变能与余能的逼近精度几乎相同，采用常规位移途径与所提出的基于混合有限元的方法之间没有显著差别。相反，应力约束构型则受益于把应力场作为问题主变量的直接离散。

就不可压缩介质而言，所提出的途径能够在不承担其他"真混合"离散所特有计算负担的前提下完成优化。已知能量类平面应变优化设计会利用材料在三轴应力状态下增大的刚度，因而可能给出与平面应力构型不同的拓扑。本文引入了不可压缩介质结构的应力约束解，确认当同时考虑对应力场的施加时可能出现显著差异。

目标函数的历史曲线确认了所提出框架在全部所考虑模拟中的完全稳定性，在处理可压缩与不可压缩材料时表现出几乎相同的性能。

最后必须指出，所采用的这一族混合有限元在任意维数的规则网格上都保持其精度、稳健性与效率。目前正在研究一种"真混合"六面体有限元，以在三维框架下处理由可压缩或不可压缩介质构成的结构的优化设计。

---

# 研究亮点 (Highlights)

> 以下为 Accepted Manuscript 附带的 Highlights 页面内容。

- 构造了一个完全以应力表述的拓扑优化问题。
- 使用一种高效的混合有限元，以在规则网格上提供稳健性与精度。
- 应力约束优化也可用于不可压缩介质的情形。
- 应力约束的最优构型受益于所采用有限元的精度。
- 在不可压缩材料与平面应变情形下得到了独特的最优构型。

---

# 参考文献 (References)

[1] C. Le, J. Norato, T.E. Bruns, C. Ha, D.A. Tortorelli, Stress–based topology optimization for continua, *Struct. Multidiscip. Optim.* 41(2010) 605–620.

[2] H.J. Seung, D.–H. Choi, G.H. Yoon, Fatigue and static failure considerations using topology optimization method, *Appl. Math. Model.* 39(2015) 1137–1162.

[3] S.H. Jeong, S.H. Park, D.–H. Choi, G.H. Yoon, Topology optimization considering static failure theories for ductile and brittle materials, *Comput. Struct.* 110-111(2012) 116-132.

[4] Y. Luo, M.Y. Wang, Z. Kang, An enhanced aggregation method for topology optimization with local stress constraints, *Comput. Methods Appl. Mech. Engrg.* 254(2013) 31–41.

[5] H. Emmendoerfer, E.A. Fancello, A level set approach for topology optimization with local stress constraints, *Internat. J. Numer. Methods Engrg.* 99(2014) 129-156.

[6] X. Guo, W. Zhang, W. Zhong, Stress–related topology optimization of continuum structures involving multi–phase materials, *Comput. Methods Appl. Mech. Engrg.* 268(2014) 632–655.

[7] X. Guo, W.S. Zhang, M.Y. Wang, P. Wei, Stress–related topology optimization via level set approach, *Comput. Methods Appl. Mech. Engrg.* 200(2011), 3439-3452.

[8] E. Holmberg, B. Torstenfelt, A. Klarbring, Stress constrained topology optimization, *Struct. Multidiscip. Optim.* 48(2013) 33-47.

[9] M. Bruggi, P. Venini, Eigenvalue–based optimization of incompressible media using mixed finite elements with application to isolation devices, *Comput. Methods Appl. Mech. Engrg.* 197(2008) 1262-1279.

[10] G.–W. Jang, Y. Y. Kim, Topology optimization with displacement–based nonconforming finite elements for incompressible materials. *Jour. Mech. Science Tech.* 23(2009) 442-451.

[11] G.–W. Jang, H. Panganiban, T.J. Chung, P1-nonconforming quadrilateral finite element for topology optimization, *Internat. J. Numer. Methods Engrg.* 84(2010) 685-707.

[12] O. Sigmund, P.M. Clausen, Topology optimization using a mixed formulation: An alternative way to solve pressure load problems, *Comput. Methods Appl. Mech. Engrg.* 196(2007), 1874-1889.

[13] M. Bruggi, C. Cinquini, An alternative truly–mixed formulation to solve pressure load problems in topology optimization, *Comput. Methods Appl. Mech. Engrg.* 198(2009), 1500-1512.

[14] G. H. Yoon, Topology optimization for stationary fluid–structure interaction problems using a new monolithic formulation, *Internat. J. Numer. Methods Engrg.* 82(2010) 591-616.

[15] E. Lee, J.R.R.A. Martins, Structural topology optimization with design–dependent pressure loads, *Comput. Methods Appl. Mech. Engrg.* 233-236(2012) 40-48.

[16] B. M. Fraeijs de Veubeke, Displacement and equilibrium models, in *Stress Analysis* ed. by O. C. Zienkiewicz and G. Hollister, 145-197, London, Wiley (1965).

[17] M. Bruggi, P. Venini, A mixed FEM approach to stress–constrained topology optimization, *Internat. J. Numer. Methods Engrg.* 73(2008) 1693-1714.

[18] F. Brezzi, M. Fortin, *Mixed and hybrid finite element methods*, New York, Springer (1991).

[19] C. Johnson, B. Mercier, Some equilibrium finite elements methods for two dimensional elasticity problems, *Numer. Math.* 30(1978) 103–116.

[20] D. N. Arnold, R. S. Falk, R. Winther, Mixed finite element methods for linear elasticity with weakly imposed symmetry, *Math. Comp.* 76(2007) 1699-1723.

[21] C. Carstensen, M. Eigel, J. Gedicke, Computational competition of symmetric mixed FEM in linear elasticity, *Comput. Methods Appl. Mech. Engrg.* 200(2011) 2903-2915.

[22] J. Hu, H. Man, S. Zhang, A simple conforming mixed finite element for linear elasticity on rectangular grids in any space dimension, *Jour. Science Comp.* 58(2014) 367–379.

[23] M. Bruggi, P. Duysinx, Topology optimization for minimum weight with compliance and stress constraints, *Struct. Multidiscip. Optim.* 46(2012) 369–384.

[24] M.P. Bendsøe, N. Kikuchi, Generating optimal topologies in structural design using a homogeneization method, *Comput. Methods Appl. Mech. Engrg.* 71(1988) 197–224.

[25] J. Hu, H. Man, S. Zhang, The simplest mixed finite element method for linear elasticity in the symmetric formulation on n–rectangular grids, arXiv:1304.5428 (2013).

[26] J. Hu, S. Zhang, A family of conforming mixed finite elements for linear elasticity on triangle grids, arXiv:1406.7457v2 (2014).

[27] J. Hu, S. Zhang, A family of symmetric mixed finite elements for linear elasticity on tetrahedral grids, *Sci. China Math.* 58(2015), 297–307.

[28] M.P. Bendsøe, Optimal shape design as a material distribution problem, *Struct. Optim.* 1(1989) 193–202.

[29] M. Zhou, G.I.N. Rozvany, The COC algorithm, Part II : topological, geometrical and generalized shape optimization, *Comput. Methods Appl. Mech. Engrg.* 89(1991) 309–336.

[30] M.P. Bendse, O. Sigmund, *Topology optimization theory, methods and applications*, New York, Springer (2003).[^3]

[31] Y. Luo, Z. Kang, Topology optimization of continuum structures with Drucker–Prager yield stress constraints, *Comput. Struct.* 90-91(2012) 65-75.

[32] P. Duysinx, O. Sigmund, New developments in handling stress constraints in optimal material distribution. *7th Symposium on Multidisciplinary Analysis and Optimization* AIAA–98–4906 (1998) 1501–1509.

[33] P. Duysinx, M.P. Bendsøe, Topology optimization of continuum structures with local stress constraints, *Internat. J. Numer. Methods Engrg.* 43(1998) 1453–78.

[34] K. Svanberg, Method of moving asymptotes - A new method for structural optimization, *Internat. J. Numer. Methods Engrg.* 24(1987) 359–373.

[35] B. Bourdin, Filters in topology optimization, *Internat. J. Numer. Methods Engrg.* 50(2001) 2143–2158.

[36] O. Sigmund, J. Petersson, Numerical instabilities in topology optimization: a survey on procedures dealing with checkerboards, mesh-dependencies and local minima, *Struct. Optim.* 16(1998) 68–75.

[37] J.K. Guest, J.H. Prévost, T. Belytschko, Achieving minimum length scale in topology optimization using nodal design variables and projection functions, *Internat. J. Numer. Methods Engrg.* 61(2004) 238–254.

[38] G.D. Cheng, X. Guo, ε–relaxed approach in topology optimization, *Struct. Optim.* 13(1997) 258–266.

[39] O. Schenk, A. Wächter, M. Hagemann, Matching–based preprocessing algorithms to the solution of saddle–point problems in large–scale nonconvex interior–point optimization, *Comput Optim Appl* 36(2007) 321–341.

---

[^1]: 译者注：原文式 (9) 下方把各向同性柔度张量印作 $S^0_{ijhk} = -\frac{\nu}{E}\delta_{ij}\delta_{hk} + \frac{1+\nu}{E}(\delta_{ih}\delta_{jk} + \delta_{ik}\delta_{jh})$。按 $\varepsilon_{ij} = S^0_{ijhk}\sigma_{hk}$ 与各向同性本构 $\varepsilon_{ij} = \frac{1+\nu}{E}\sigma_{ij} - \frac{\nu}{E}\delta_{ij}\sigma_{kk}$ 对照，对称化项的系数应为 $\frac{1+\nu}{2E}$。此处照原文保留。

[^2]: 译者注：原文式 (18) 把过滤权重印作 $H_{el} = \sum_N \max(0,\ r_{\min} - \mathrm{dist}(e, l))$，在 $H_{el}$ 的定义式中多出一个对邻域 $N$ 的求和号；按其所引文献 [1]、[35] 的标准密度过滤，$H_{el}$ 是逐单元对的权重、本身不含求和，求和只出现在式 (18) 第一式的分子与分母中。此处照原文保留。

[^3]: 译者注：原文参考文献 [30] 作者名印作 "M.P. Bendse"，应为 "M.P. Bendsøe"。此处照原文保留。
