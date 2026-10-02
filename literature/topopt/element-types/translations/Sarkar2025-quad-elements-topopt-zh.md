---
title: "翻译：Topology Optimization With Quadrilateral Elements: A Comparative Study, Codes, and Tutorials"
tags:
  - translation
  - element-types
  - topology-optimization
  - quadrilateral-elements
  - matlab-code
status: "done"
date_created: 2026-09-10
date_updated: 2026-09-11
source: "../sources/Sarkar2025-quad-elements-topopt.pdf"
citekey: "Sarkar2025-quadelements"
language: "zh-CN"
---

# Topology Optimization With Quadrilateral Elements: A Comparative Study, Codes, and Tutorials

---

# 信息

- **中文标题**：四边形单元拓扑优化：对比研究、代码与教程
- **作者**：Swagatam Islam Sarkar；Prabhat Kumar
- **单位**：印度理工学院海得拉巴分校（Indian Institute of Technology Hyderabad, Telangana, India）；两位作者均隶属机械与航空航天工程系，Prabhat Kumar 另隶属计算工程系与工程科学系
- **期刊**：*Computer Applications in Engineering Education*
- **卷 / 期 / 文章号**：33(3): e70031（全文 30 页）
- **年份**：2025
- **DOI**：10.1002/cae.70031
- **收稿 / 修回 / 录用**：2025-01-25 / 2025-03-01 / 2025-03-24
- **资助**：作者声明本研究未获得专项资助。

# 摘要

本文针对四边形族单元，例如四节点（Q4）、八节点（Q8）和九节点（Q9）单元在多种问题中的拓扑优化（TO）开展比较研究。针对涉及不同物理场的三类不同设计问题，本文开发了采用 Q8 和 Q9 单元的 MATLAB 代码，并给出了生成连接矩阵以及根据泊松比确定这些单元的单元刚度矩阵的简明高效方法。为展示相对性能，本文研究了：(i) 承受恒定力的刚度优化结构的柔顺度最小化；(ii) 承受设计相关压力载荷的承载结构的柔顺度最小化；(iii) 以期望输出变形最大化为目标的柔顺机构问题。所有问题均施加体积约束。Q8 和 Q9 有限元得到的优化设计不存在棋盘格模式。为保证优化设计具有最小特征尺寸，本文引入了灵敏度过滤和密度过滤方案；同时还概述了 Heaviside 投影过滤的实现方法，以获得接近二值（0-1）的优化解。本文给出的全面比较研究连同代码和补充材料，既可作为学术界的教学工具，也可为该领域的初学者提供有价值的资源。相关代码收录于附录中。

**关键词：** 柔顺机构；设计相关压力载荷；高阶四边形单元；MATLAB 代码；拓扑优化

# 1 引言

拓扑优化（TO）是一种工程计算设计技术，用于优化给定设计域内的材料分布。它能够针对所关注的问题找到高效、创新且非常规的优化材料分布。该技术求解相应的边值问题，并在给定的物理/几何约束下优化所需目标。通常，前者采用有限元法求解，其中设计域[^original-1]使用有限元（FE）进行参数化，这些单元可以从简单的三角形、四边形有限元 [1]，一直扩展到六边形单元 [2–5]、多边形单元 [6–8] 等高级有限元。每个有限元都被赋予一个设计（密度）变量 $\rho\in[0,1]$。在拓扑优化中，密度变量通常被松弛 [1]；因此，需要通过惩罚和/或投影将中间密度（$0<\rho<1$）推向 0 或 1，以获得接近二值的解。也就是说，在优化结束时，期望优化解主要由 $\rho=1$ 或 $\rho=0$ 构成。$\rho=1$ 表示单元为实体状态，而 $\rho=0$ 表示单元为空洞状态。除基于密度的方法之外，针对不同应用还存在多种其他拓扑优化方法，例如参数化水平集法 [9–11]、渐进结构优化 [12]、基于特征的方法 [2, 7, 13] 等。不过，本研究仅关注基于密度的方法。

由于 Q4 双线性（四节点）四边形有限元具有形式简单和计算成本低的优点，它一直被广泛用于二维设计域的离散。然而，早期研究已经发现，使用 Q4 有限元得到的优化设计可能出现棋盘格模式（空洞单元与实体单元交替分布的区域）或点连接等问题 [14]。众所周知，为处理这些几何奇异性，人们已经发展出多种技术，其中包括灵敏度过滤 [1]、密度过滤 [15]、使用高级二维单元 [2, 5, 6]，以及采用八节点（Q8）[16, 17]、九节点（Q9）[17, 18] 等高阶四边形单元。基于后两类技术的方法仍需使用前述过滤技术，以保证长度尺度控制和网格无关解 [5]。尽管已有大量论文和公开代码讨论在不同应用中结合 Q4 有限元使用前两类技术的方法 [5]，但对于一组涉及不同物理场的不同设计问题，尚无文献同时详细介绍采用 Q8 和 Q9 有限元的拓扑优化、具体代码、教程及比较研究。本文旨在填补这一空白，为学生、研究人员和初学者提供一个使用四边形族单元（Q4、Q8 和 Q9 有限元）亲手实践拓扑优化的工具与平台，而非提出新的高级研究内容。本文求解三类不同的设计问题：涉及设计无关（恒定）载荷和设计相关载荷的结构优化，以及采用设计无关驱动力的柔顺机构（CM）优化。为使优化设计具有最小特征尺寸，本文采用了过滤技术；为获得接近 0-1 解的优化设计，还实现了 Heaviside 投影过滤，并对结果进行比较。

本文开发了采用 Q8 和 Q9 有限元的拓扑优化 MATLAB 代码，分别称为 `topQ8` 和 `topQ9`，用于求解给定体积分数下的柔顺度最小化问题。设计变量按照文献 [1] 使用最优性准则进行更新。这些代码分别列于附录 A 和附录 B。代码最初用于 Messerschmitt–Bölkow–Blohm（MBB）梁设计的优化。此外，为便于比较，还针对具有不同边界条件和外力的多种问题提供了不同扩展。

柔顺机构是一种整体式设计，它利用自身柔性构件的变形，将施加的输入载荷传递到所需输出端。与传统刚体机构相比，这类机构具有多项优势。通常，可采用伪刚体模型和连续体优化方法来综合/优化这类机构。由于这些机构既应提供足够的变形，也应能承受所施加的驱动力，基于连续体的方法通常使用机构的柔性度量（例如输出变形）和刚度度量（输入位移、应变能、输入弹簧）来定义目标。迄今为止，拓扑优化已被用于多种应用中的柔顺机构设计 [19–24]。Ananthasuresh 等 [25] 将输出位移与应变能的加权和最大化。Frecker 等 [26] 提出多准则目标，并报告了收敛性的改善。Sigmund [27] 在约束输入位移的同时，提出最大化机构的机械增益。关于柔顺机构的多种应用及相关设计方法，可参见文献 [28]。本文采用人工输入/输出弹簧表述。在给定体积约束下，最大化机构的输出变形 [29]。在弹簧模型中，输入弹簧的 $k_{\mathrm{in}}$ 表示驱动器刚度，输出弹簧的 $k_{\mathrm{out}}$ 表示工件刚度。本文提出自研 MATLAB 代码 `topQ8CM` 和 `topQ9CM`，采用人工输入/输出弹簧法设计柔顺机构。设计变量使用最优性准则法 [30] 更新。这些代码最初用于优化反向器柔顺机构，随后进一步扩展到柔顺夹持机构的优化。

设计相关压力载荷具有多种应用。此类载荷的位置、方向和大小会随拓扑优化迭代而变化，由此带来若干挑战 [31–33]。这些挑战包括：建立压力场与设计变量之间的关系，识别施加载荷的边界，确定与整体压力场一致的节点力，以及在典型拓扑优化框架中计算载荷灵敏度项 [32, 33]。已有多种方法用于处理这些问题，例如可参见文献 [32, 34, 35]。本文采用文献 [32] 报告的方法，因为该方法为上述挑战提供了可行解法 [33]，并且已被用于求解文献 [24, 35–38] 中的多种问题。本文分别采用 Q8 和 Q9 有限元，按照与采用 Q4 有限元的 `TOPress` [33] 类似的方式开发了 MATLAB 代码 `TOPressQ8` 和 `TOPressQ9`。这些代码最初用于在给定体积约束下，以柔顺度最小化为目标设计受压圆弧。设计变量采用移动渐近线法（MMA；参见文献 [39]）更新。

所提供的代码涵盖了若干关键环节，包括高效生成单元连接矩阵及相应的刚度矩阵、施加边界条件和力条件，以及应用不同的过滤技术和优化工具。教程介绍了如何针对具有设计无关载荷和设计相关载荷的柔顺度最小化问题及柔顺机构设计问题，在改变边界条件和力条件的情况下生成设计。本文对采用 Q4、Q8 和 Q9 得到的优化设计进行了全面比较与讨论。包含代码和教程的这项综合研究有望成为学生、研究人员和初学者的教学资源，并为今后开展采用四边形族单元的拓扑优化研究奠定基础。

本文其余部分安排如下。第 2 章简要介绍 Q4、Q8 和 Q9 单元及相关术语。第 3 章给出问题表述，并介绍过滤方案、优化问题、灵敏度分析和优化更新方案。第 4 章说明用于柔顺度最小化问题的 Q8 和 Q9 有限元 MATLAB 代码实现。第 5 章给出结果与讨论，其中介绍 MBB 设计优化、收敛曲线及相关计算成本；还给出 `topQ8` 和 `topQ9` 面向不同问题的多种扩展、`topQ8CM` 和 `topQ9CM` 代码的开发及两个基准柔顺机构设计的求解、`TOPressQ8` 和 `TOPressQ9` 面向设计相关压力载荷下柔顺度最小化问题的开发，以及两个承受设计相关载荷的承载结构的求解与讨论。最后，第 6 章给出结论。

# 2 Q4、Q8 和 Q9 单元

有限元法（FEM）是一种数值技术，通常用于求解拓扑优化表述所对应的边值问题（BVP）。在二维设计域参数化中，一般采用三角形 [40]、四边形 [15] 和六边形 [3, 5, 8, 41] 有限元。本文采用 Q4、Q8 和 Q9 有限元（图 1）对设计域进行离散并开展有限元分析（FEA），进而执行拓扑优化。为保证内容完整，下面对这些单元作简要说明。

![[Sarkar2025_Fig1.png]]

<center><b>
图 1：四边形族单元：(a) Q4、(b) Q8 和 (c) Q9。数字标注表示局部节点编号方案；$\xi$-$\eta$ 为自然坐标系。
</b></center>

## 2.1 Q4 单元

Q4 单元因其简单、形状规则、节点较少且效率较高而常用于拓扑优化。这类单元易于生成和管理网格，因而能够缩短网格划分与预处理时间 [1]。此外，与高阶单元相比，它们对网格畸变较不敏感，这有利于在优化过程中保持网格质量 [1]。然而，它们可能难以准确表示复杂几何与材料分布 [30]，从而产生近似误差。这一限制会影响优化设计的精度，尤其是在几何形状复杂的问题中 [1]。此外，它们得到的优化设计还可能含有棋盘格模式和点连接 [14]。

图1a 表示自然坐标系 $\xi$-$\eta$ 中的一个 Q4 单元。局部节点位于顶点处，并按 1、2、3、4 编号。上述节点编号方案（图 1a）对应的形函数可写为 [42]：

$$
N_i=\frac{(1+\xi_i\xi)(1+\eta_i\eta)}{4}.
\tag{1}
$$

其中，$N_i$（$i=1,2,3,4$）表示形函数，节点 $i_{1,2,3,4}$ 的 $(\xi_i,\eta_i)$ 分别为：$(\xi_1,\eta_1)=(-1,-1)$、$(\xi_2,\eta_2)=(1,-1)$、$(\xi_3,\eta_3)=(1,1)$、$(\xi_4,\eta_4)=(-1,1)$。这些形函数用于确定所关注问题的边值问题解。

## 2.2 Q8 单元

除角节点外，Q8 有限元在四条边的中点还各有一个节点（图 1b），因而能够更好地捕捉优化设计中的边界效应和局部变化。这一点有利于减小优化结构中的应力集中 [1]。此外，Q8 单元更适用于网格自适应技术，因为它们能够更好地贴合加密后的网格区域，而不会引入过度畸变。这种网格自适应灵活性可使优化结果更加高效、准确 [30]。Q8 有限元具有更多节点且连接关系要求更高，这可能使网格生成更加复杂、耗时。其复杂性还会增加拓扑优化过程的预处理开销 [30]。本文给出一种简便高效的 Q8 网格及相应连接矩阵生成方法，从而为减少计算时间提供一种可行方案。图 1b 所示 Q8 单元的形函数可写为 [43]：

$$
N_i=
\begin{cases}
\dfrac{(1+\xi_i\xi)(1+\eta_i\eta)(-1+\xi_i\xi+\eta_i\eta)}{4}, & i=1,2,3,4,\\[6pt]
\dfrac{(1-\xi^2)(1+\eta_i\eta)}{2}, & i=5,7,\\[6pt]
\dfrac{(1-\eta^2)(1+\xi_i\xi)}{2}, & i=6,8.
\end{cases}
\tag{2}
$$

其中，$N_i$（$i=1,2,\ldots,8$）表示形函数，节点 $i_{1,2,\ldots,8}$ 的 $(\xi_i,\eta_i)$ 为：$(\xi_1,\eta_1)=(-1,-1)$、$(\xi_2,\eta_2)=(1,-1)$、$(\xi_3,\eta_3)=(1,1)$、$(\xi_4,\eta_4)=(-1,1)$、$(\xi_5,\eta_5)=(0,-1)$、$(\xi_6,\eta_6)=(1,0)$、$(\xi_7,\eta_7)=(0,1)$、$(\xi_8,\eta_8)=(-1,0)$（图 1b）。

## 2.3 Q9 单元

Q9 有限元的每个单元包含九个节点，因此在表示不规则或曲线几何时具有更好的建模能力，可实现更真实的模拟。高阶单元的优势见文献 [44, 45]。Q9 有限元具有更多节点和额外自由度（DOF），可能导致计算成本增加，这在大规模拓扑优化问题中会成为限制。这一限制已在文献 [44, 45] 中得到讨论。Q9 单元还可能对网格质量和单元长宽比更敏感，因此需要谨慎划分网格，以避免数值问题 [42]。与 Q8 有限元类似，本文给出一种简便高效的 Q9 网格及相应网格连接矩阵生成方法。图 1c 所示 Q9 单元的形函数可写为 [42]：

$$
N_i=
\begin{cases}
\dfrac{\xi_i\eta_i\xi\eta(1+\xi_i\xi)(1+\eta_i\eta)}{4}, & i=1,2,3,4,\\[6pt]
\dfrac{\eta_i\eta(1-\xi^2)(1+\eta_i\eta)}{2}, & i=5,7,\\[6pt]
\dfrac{\xi_i\xi(1-\eta^2)(1+\xi_i\xi)}{2}, & i=6,8,\\[6pt]
(1-\xi^2)(1-\eta^2), & i=9.
\end{cases}
\tag{3}
$$

其中，$N_i$（$i=1,2,\ldots,9$）为形函数，节点 $i_{1,2,\ldots,9}$ 的 $(\xi_i,\eta_i)$ 为：$(\xi_1,\eta_1)=(-1,-1)$、$(\xi_2,\eta_2)=(1,-1)$、$(\xi_3,\eta_3)=(1,1)$、$(\xi_4,\eta_4)=(-1,1)$、$(\xi_5,\eta_5)=(0,-1)$、$(\xi_6,\eta_6)=(1,0)$、$(\xi_7,\eta_7)=(0,1)$、$(\xi_8,\eta_8)=(-1,0)$、$(\xi_9,\eta_9)=(0,0)$（图 1c）。

# 3 问题表述

本研究采用基于密度的拓扑优化方法 [46]。其中，单元 $e$ 的 Young 模量 $E_e$ 按照修正的 SIMP（Solid Isotropic Material with Penalization，带惩罚的固体各向同性材料）方案 [15] 插值为：

$$
E_e=E_{\min}+\tilde{\rho}_e^{\,p}(E_0-E_{\min}),
\tag{4}
$$

其中，$E_0$ 是 $\tilde{\rho}_e=1$ 时材料的刚度，$E_{\min}$ 表示赋予空洞区域的极小刚度，以防止刚度矩阵变为奇异矩阵；$p$ 为惩罚因子。本文取 $p=3$。$\tilde{\rho}_e$ 是过滤后的设计变量，它随本文采用的不同过滤技术而确定，相关内容将在下文讨论。

## 3.1 过滤

拓扑优化中主要的数值异常包括棋盘格模式的形成（实体单元与空洞单元交替排列成一定模式）、点连接以及网格依赖等 [30]。此外，由不充分的数值建模产生的解，例如拓扑优化中与棋盘格模式相关的解，在实际中并不可行。本文采用过滤技术，即对优化设计中的材料分布进行正则化或平滑的方法，以克服这些几何奇异性。

### 3.1.1 灵敏度过滤

灵敏度过滤由文献 [27] 提出。该技术要求在算法迭代过程中修改所使用的设计灵敏度。一个单元及其邻域内灵敏度的加权平均决定该单元的设计灵敏度。过滤后的灵敏度写为 [15]：

$$
\frac{\overline{\partial f_0}}{\partial\rho_e}
=
\frac{\displaystyle\sum_{i\in N_e}H_{ei}\rho_i\frac{\partial f_0}{\partial\rho_i}}
{\displaystyle\max(\gamma,\rho_e)\sum_{i\in N_e}H_{ei}},
\tag{5}
$$

其中，函数 $f_0$ 表示目标函数，$\rho_e$ 表示单元 $e$ 的密度，$\rho_i$ 表示过滤半径 $r_{\min}$ 内相邻单元 $i$ 的密度。权重因子 $H_{ei}$ 定义为 $H_{ei}=\max(0,r_{\min}-\Delta(e,i))$。$\Delta(e,i)$ 是单元 $e$ 与单元 $i$ 的形心间距。$N_e$ 为满足 $\Delta(e,i)<r_{\min}$ 的单元 $i$ 的集合。为避免除以 0，引入一个很小的正数 $\gamma\;(=10^{-3})$ [15]。注意，由于 $H_{ei}$ 与设计变量无关，因此只需在拓扑优化过程开始前确定一次，随后一直使用。

### 3.1.2 密度过滤

过滤密度通过计算一个单元及其邻域内密度（设计变量）的加权平均得到，与灵敏度过滤方法类似。密度过滤由 Bruns 和 Tortorelli [47] 提出，其定义为：

$$
\tilde{\rho}_e=
\frac{\displaystyle\sum_{i\in N_e}H_{ei}\rho_i}
{\displaystyle\sum_{i\in N_e}H_{ei}},
\tag{6}
$$

其中，$\tilde{\rho}_e$ 是单元 $e$ 对应于设计变量 $\rho_e$ 的过滤密度。由于该过滤方案作用于原始密度（设计变量），在优化过程中，还需要更新目标函数 $f_0$ 和材料体积 $V$ 对设计变量 $\rho_j$ 的灵敏度。通常，所需灵敏度采用链式法则确定：

$$
\frac{\partial\psi}{\partial\rho_j}
=\sum_{e\in N_j}\frac{\partial\psi}{\partial\tilde{\rho}_e}
\frac{\partial\tilde{\rho}_e}{\partial\rho_j}
=\sum_{e\in N_j}
\frac{H_{je}}{\displaystyle\sum_{i\in N_e}H_{ei}}
\frac{\partial\psi}{\partial\tilde{\rho}_e},
\tag{7}
$$

其中，函数 $\psi$ 表示目标函数或约束。此处同样有 $H_{ei}$ 与设计变量无关，因此只需在拓扑优化过程开始前确定一次。

## 3.2 优化问题

为给出研究、教程并与相应开发代码进行比较，本文在给定体积约束下考虑三种不同的优化表述。第一种是最常见的恒定载荷下柔顺度最小化问题，其中所有灵敏度具有相同符号。第二种是采用恒定驱动力设计柔顺机构，其中目标灵敏度可能具有不同符号。第三种是承受设计相关载荷的承载结构设计，其中目标灵敏度还包含载荷灵敏度项 [32, 33]；因此，目标灵敏度具有不同符号。带体积约束的一般优化表述可写为：

$$
\left.
\begin{aligned}
&\underset{\tilde{\boldsymbol{\rho}}}{\min} && f_0,\\
&\text{subjected to:} && \lambda:\ \mathbf{K}\mathbf{U}-\mathbf{F}=\mathbf{0},\\
&&& \mu:\ V-V_f\leq 0,\\
&&& 0\leq\rho_i,\tilde{\rho}_i\leq 1\quad(i=1,2,\ldots,N_e).
\end{aligned}
\right\}
\tag{8}
$$

其中，$f_0$ 为目标函数，$\mathbf{U}$、$\mathbf{F}$ 和 $\mathbf{K}$ 分别为全局位移向量、力向量和刚度矩阵。$V_f$ 和 $V$ 分别为设计的允许体积和当前体积。$\lambda$（向量）和 $\mu$（标量）是分别对应于状态方程和体积约束的 Lagrange 乘子。$\rho_i$ 是第 $i$ 个单元的设计变量，$\tilde{\rho}_i$ 表示与之对应的过滤变量。$N_e$ 是用于离散设计域的有限元总数。$\boldsymbol{\rho}$ 和 $\tilde{\boldsymbol{\rho}}$ 分别表示设计变量向量和过滤设计变量向量。

### 3.2.1 灵敏度分析

本研究采用基于梯度的优化器更新设计变量，因此需要计算目标函数和约束相对于设计变量的导数。本文使用伴随变量法确定这些导数，并注意到约束数（等于 1，即体积约束）小于设计变量数（等于 $N_e$）。对于式 (8) 所表述的优化问题，可将 Lagrangian $\mathcal{L}$ 写为：

$$
\mathcal{L}=f_0+\mu(V-V_f)+\boldsymbol{\lambda}^{\mathrm{T}}(\mathbf{K}\mathbf{U}-\mathbf{F}).
\tag{9}
$$

现在，对 $\mathcal{L}$ 关于物理（过滤）设计变量求导，进而给出优化所需条件，可写为：

$$
\begin{aligned}
\frac{\partial\mathcal{L}}{\partial\tilde{\rho}_e}
={}&\frac{\partial f_0}{\partial\tilde{\rho}_e}
+\frac{\partial f_0}{\partial\mathbf{U}}
\frac{\partial\mathbf{U}}{\partial\tilde{\rho}_e}
+\mu\frac{\partial V}{\partial\tilde{\rho}_e}
+\boldsymbol{\lambda}^{\mathrm{T}}
\left(
\frac{\partial\mathbf{K}}{\partial\tilde{\rho}_e}\mathbf{U}
+\mathbf{K}\frac{\partial\mathbf{U}}{\partial\tilde{\rho}_e}
-\frac{\partial\mathbf{F}}{\partial\tilde{\rho}_e}
\right)\\
={}&\frac{\partial f_0}{\partial\tilde{\rho}_e}
+\left(\frac{\partial f_0}{\partial\mathbf{U}}+\boldsymbol{\lambda}^{\mathrm{T}}\mathbf{K}\right)
\frac{\partial\mathbf{U}}{\partial\tilde{\rho}_e}
+\boldsymbol{\lambda}^{\mathrm{T}}
\frac{\partial\mathbf{K}}{\partial\tilde{\rho}_e}\mathbf{U}
+\mu\frac{\partial V}{\partial\tilde{\rho}_e}
-\boldsymbol{\lambda}^{\mathrm{T}}
\frac{\partial\mathbf{F}}{\partial\tilde{\rho}_e}.
\end{aligned}
\tag{10}
$$

采用伴随变量法时，选取 $\boldsymbol{\lambda}$ 使得 $\left(\frac{\partial f_0}{\partial\mathbf{U}}+\boldsymbol{\lambda}^{\mathrm{T}}\mathbf{K}\right)=0$，从而得到：

$$
\boldsymbol{\lambda}^{\mathrm{T}}
=-\frac{\partial f_0}{\partial\mathbf{U}}\mathbf{K}^{-1}.
\tag{11}
$$

将 $\boldsymbol{\lambda}$ 代入式 (10)，得到：

$$
\frac{\partial\mathcal{L}}{\partial\tilde{\rho}_e}
=\frac{\partial f_0}{\partial\tilde{\rho}_e}
-\frac{\partial f_0}{\partial\mathbf{U}}\mathbf{K}^{-1}
\left(
\frac{\partial\mathbf{K}}{\partial\tilde{\rho}_e}\mathbf{U}
-\frac{\partial\mathbf{F}}{\partial\tilde{\rho}_e}
\right)
+\mu\frac{\partial V}{\partial\tilde{\rho}_e}.
\tag{12}
$$

现在采用最优性准则，即令 $\frac{\partial\mathcal{L}}{\partial\tilde{\rho}_e}=0$，可得：

$$
\frac{
-\dfrac{\partial f_0}{\partial\tilde{\rho}_e}
+\dfrac{\partial f_0}{\partial\mathbf{U}}\mathbf{K}^{-1}
\left(
\dfrac{\partial\mathbf{K}}{\partial\tilde{\rho}_e}\mathbf{U}
-\dfrac{\partial\mathbf{F}}{\partial\tilde{\rho}_e}
\right)
}{
\mu\dfrac{\partial V}{\partial\tilde{\rho}_e}
}=1.
\tag{13}
$$

式 (13) 表示给定优化问题的最优条件。利用该条件，定义量 $\beta_e$ 为：

$$
\beta_e=
\frac{
-\dfrac{\partial f_0}{\partial\tilde{\rho}_e}
+\dfrac{\partial f_0}{\partial\mathbf{U}}\mathbf{K}^{-1}
\left(
\dfrac{\partial\mathbf{K}}{\partial\tilde{\rho}_e}\mathbf{U}
-\dfrac{\partial\mathbf{F}}{\partial\tilde{\rho}_e}
\right)
}{
\mu\dfrac{\partial V}{\partial\tilde{\rho}_e}
}.
\tag{14}
$$

在优化的最终阶段，所得到的设计变量和 $\mu$ 应使每个单元的 $\beta_e$ 都达到 1。因此，只要 $\beta_e$ 达到 1，就会得到优化结果。

## 3.3 优化更新方案

本节介绍用于求解本文所考虑问题的优化方案。

### 3.3.1 受恒定载荷的刚度优化结构

在给定体积约束下，对承受恒定载荷的刚度优化结构进行优化，以最小化设计的柔顺度。因此，$f_0=\mathbf{U}^{\mathrm{T}}\mathbf{K}\mathbf{U}$，且 $\frac{\partial\mathbf{F}}{\partial\tilde{\rho}_e}=0$。由此，式 (14) 化为：

$$
\beta_e=
\frac{
\mathbf{U}^{\mathrm{T}}
\dfrac{\partial\mathbf{K}}{\partial\tilde{\rho}_e}
\mathbf{U}
}{
\mu\dfrac{\partial V}{\partial\tilde{\rho}_e}
}.
\tag{15}
$$

本文按照文献 [15] 的更新方案更新设计变量：

$$
\rho_e^{\mathrm{new}}=
\begin{cases}
\max(0,\rho_e-m),
& \rho_e\beta_e^{\eta}\leq\max(0,\rho_e-m),\\[4pt]
\min(1,\rho_e+m),
& \rho_e\beta_e^{\eta}\geq\min(1,\rho_e+m),\\[4pt]
\rho_e\beta_e^{\eta},
& \text{其他情况}.
\end{cases}
\tag{16}
$$

其中，$\rho_e^{\mathrm{new}}$ 表示单元 $e$ 的更新密度，$m$ 为正的移动限值，$\eta$ 表示数值阻尼系数（$\eta=0.5$）。$\mu$ 采用二分法 [15] 求得。如前所述，目标是使结构的柔顺度最小。材料体积 $V$ 和柔顺度 $f_0$ 关于过滤变量的灵敏度可写为 [15]：

$$
\frac{\partial f_0}{\partial\tilde{\rho}_e}
=-p\tilde{\rho}_e^{\,p-1}(E_0-E_{\min})
\mathbf{u}_e^{\mathrm{T}}\mathbf{k}_0\mathbf{u}_e,
\qquad
\frac{\partial V}{\partial\tilde{\rho}_e}=1.
\tag{17}
$$

### 3.3.2 受恒定驱动力的柔顺机构

为优化柔顺机构，将期望方向上的输出位移 $L_{\mathrm{out}}=\mathbf{L}^{\mathrm{T}}\mathbf{U}$ 作为目标。其中，$\mathbf{L}$ 是一个向量，除输出自由度对应位置取 1 外，其余分量均为 0。根据采用恒定驱动力的已定义目标函数，有 $f_0=-\mathbf{L}^{\mathrm{T}}\mathbf{U}$，且 $\frac{\partial\mathbf{F}}{\partial\tilde{\rho}_e}=0$。此外，驱动力为常量。在这两个条件下，$\beta_e$ 可写为：

$$
\beta_e=
\frac{
-\boldsymbol{\lambda}_1^{\mathrm{T}}
\dfrac{\partial\mathbf{K}}{\partial\tilde{\rho}_e}\mathbf{U}
}{
\mu\dfrac{\partial V}{\partial\tilde{\rho}_e}
},
\tag{18}
$$

其中，$\boldsymbol{\lambda}_1$ 通过求解 $\mathbf{L}=\mathbf{K}\boldsymbol{\lambda}_1$ 确定。本文采用以下设计变量更新方案 [30]：

$$
\rho_e^{\mathrm{new}}=
\begin{cases}
\max(0.001,\rho_e-m),
& \rho_e\beta_e^{\eta}\leq\max(0.001,\rho_e-m),\\[4pt]
\min(1,\rho_e+m),
& \rho_e\beta_e^{\eta}\geq\min(1,\rho_e+m),\\[4pt]
\rho_e\times\max(10^{-10},\beta_e^{\eta}),
& \text{其他情况}.
\end{cases}
\tag{19}
$$

为避免更新设计变量时出现复数，当 $\beta_e$ 小于 $10^{-10}$（接近 0）时，以一个极小正数 $10^{-10}$ 代替 $\beta_e$。此外，优化中还将设计变量的最小值取为 0.001 [30]。优化柔顺机构时，也可以采用 MMA（参见文献 [39]）更新设计变量。

### 3.3.3 承受设计相关压力载荷的承载结构

由于此类载荷的方向、位置和/或大小（即 $\frac{\partial\mathbf{F}}{\partial\tilde{\rho}_e}\neq0$）会随优化迭代演化 [32]，设计相关载荷下的设计优化问题被认为是拓扑优化中的一类挑战性问题。本文采用文献 [32] 首先提出的、带排水项的 Darcy 方法，通过最小化柔顺度（即 $f_0=\mathbf{U}^{\mathrm{T}}\mathbf{K}\mathbf{U}$）设计承载结构。对于这类问题，采用文献 [33] 中的符号和步骤，由式 (14) 确定 $\beta_e$：

$$
\beta_e=
\frac{
-\dfrac{\partial f_0}{\partial\tilde{\rho}_e}
+\dfrac{\partial f_0}{\partial\mathbf{U}}\mathbf{K}^{-1}
\left(
\dfrac{\partial\mathbf{K}}{\partial\tilde{\rho}_e}\mathbf{U}
-\mathbf{T}\mathbf{A}^{-1}
\dfrac{\partial\mathbf{A}}{\partial\tilde{\rho}_e}\mathbf{P}
\right)
}{
\mu\dfrac{\partial V}{\partial\tilde{\rho}_e}
}.
\tag{20}
$$

与采用 Q4 有限元的 `TOPress` MATLAB 代码 [33] 类似，本文使用 MMA [39] 更新设计变量并求解两个基准问题。

至此，本文研究所需的全部组成部分均已说明。下面将介绍针对采用恒定载荷的柔顺度最小化问题，使用 Q8 和 Q9 有限元开发 MATLAB 代码的方法。

# 4 MATLAB 代码说明

本文使用所开发的 MATLAB 代码 `topQ8`、`topQ9`、`topQ8CM`、`topQ9CM`、`TOPressQ8` 和 `TOPressQ9` 开展研究、教程说明和对比。对于材料定义、单元连接关系和过滤部分，采用 Q8 的各程序是相同的，采用 Q9 的各程序也是如此。因此，本节完整说明 MATLAB 程序 `topQ8`（附录 A）和 `topQ9`（附录 B）。这两份程序最初用于 MBB 梁设计。其余程序在补充材料中提供，本文在求解不同问题时说明相应修改。可在 MATLAB 命令窗口中调用：

```matlab
topQ8(nelx,nely,volfrac,penal,rmin,ft)
topQ9(nelx,nely,volfrac,penal,rmin,ft)
```

其中，`nelx` 和 `nely` 分别表示水平与竖直方向的单元数，`volfrac` 为给定体积分数，`penal` 表示惩罚指数 $p$，`rmin` 为过滤半径 $r_{\min}$，`ft` 表示所采用的过滤方式。`ft = 1` 和 `ft = 2` 分别对应灵敏度过滤和密度过滤，`ft = 0` 表示不使用过滤。例如，对图 9 所示半 MBB 梁采用灵敏度过滤和 Q8 单元剖分，可通过以下调用生成优化结构：

```matlab
topQ8(60,20,0.5,3,2.4,1)
```

下面同时介绍两份程序的主要组成部分。

## 4.1 材料定义

材料属性在第 4–6 行定义。`E0` 表示材料的 Young 模量 $E_0$；赋予空单元或空洞区域的人工 Young 模量 `Emin` 对应 $E_{\min}$；`nu` 表示泊松比 $\nu$。下一步计算 $E_0=1$ 时的单元刚度矩阵 $\boldsymbol k_0$，代码中用 `KE` 表示。由于网格规则，每个单元的 `KE` 相同。

## 4.2 有限元分析

本节给出 Q8 和 Q9 有限元的单元连接方案，以 MBB 设计说明相应的单元连接关系。图 2–4 分别展示用 Q4、Q8 和 Q9 有限元对设计域进行参数化的方式。单元与节点按照先从上到下、再从左到右的顺序连续编号。节点 $n$ 的水平和竖直位移分别由自由度编号 $2n-1$ 和 $2n$ 表示。`topQ8` 的第 8–30 行和 `topQ9` 的第 8–38 行分别给出刚度矩阵 `KE` 的构造，提供了确定 Q8 与 Q9 单元刚度矩阵的简单高效方法。

![[Sarkar2025_Fig2.png]]

<center><b>
图 2：Q4 有限元的单元与自由度示意图。各单元中心的蓝色数字为单元编号，角点处的数字为全局自由度编号。
</b></center>

![[Sarkar2025_Fig3.png]]

<center><b>
图 3：Q8 有限元的单元与自由度示意图。各单元中心的蓝色数字为单元编号，角点及边中点处的数字为全局自由度编号。
</b></center>

![[Sarkar2025_Fig4.png]]

<center><b>
图 4：Q9 有限元的单元与自由度示意图。各单元中心的蓝色数字为单元编号，角点、边中点与单元中心处的数字为全局自由度编号。
</b></center>

### 4.2.1 Q8 单元连接矩阵的生成与边界条件定义

本文给出一种简单高效的方法，生成 Q8 有限元网格的连接矩阵。首先构造两个不同矩阵 `nodenrs1`（第 32 行）和 `nodenrs2`（第 32 行），然后将二者组合，获得结构各对应位置的全部节点编号。`nodenrs1` 表示从离散结构第一列开始、隔列排列的节点编号；`nodenrs2` 则表示从第二列开始、隔列排列的节点编号。因此，`nodenrs1` 有 $2\times\texttt{nely}+1$ 行和 $\texttt{nelx}+1$ 列，`nodenrs2` 有 $\texttt{nely}+1$ 行和 $\texttt{nelx}$ 列。当 `nelx = 3`、`nely = 2` 时：

$$
\texttt{nodenrs1}=\begin{bmatrix}
1&9&17&25\\2&10&18&26\\3&11&19&27\\4&12&20&28\\5&13&21&29
\end{bmatrix},\qquad
\texttt{nodenrs2}=\begin{bmatrix}6&14&22\\7&15&23\\8&16&24\end{bmatrix}.
$$

随后，`nodeall`（第 34 行）确定全部节点编号，其排列方式是先依次存放所有单元的第一个节点，再从后续列开始依次存放所有单元的第二个节点，依此类推。当 `nelx = 3`、`nely = 2` 时，`nodeall` 如图 5 所示。`nodeall` 的列数为 $8\times\texttt{nelx}=8\times3=24$，行数为 $\texttt{nely}=2$，即它是一个 $2\times24$ 矩阵。将 `nodeall` 重排为 8 列矩阵，得到 `nodenrs`（第 38 行）。`nodenrs` 的第一列给出所有单元的第一个节点，第二列给出所有单元的第二个节点，以此类推；第 $i$ 行给出第 $i$ 个单元的节点编号。上述网格对应：

$$
\texttt{nodenrs}=\begin{bmatrix}
3&11&9&1&7&10&6&2\\
5&13&11&3&8&12&7&4\\
11&19&17&9&15&18&14&10\\
13&21&19&11&16&20&15&12\\
19&27&25&17&23&26&22&18\\
21&29&27&19&24&28&23&20
\end{bmatrix},
$$

各行依次对应单元 1–6。

![[Sarkar2025_Fig5.png]]

<center><b>
图 5：Q8 单元在 nelx = 3、nely = 2 时的 nodeall 矩阵。
</b></center>

随后，`edofMat`（第 39 行）提供离散结构的全部自由度，其第 $i$ 行对应第 $i$ 个单元的 16 个自由度。`ndof` 为离散结构的自由度总数，满足 `ndof = max(max(edofMat))`。当 `nelx = 3`、`nely = 2` 时，`edofMat` 如图 6 所示。

![[Sarkar2025_Fig6.png]]

<center><b>
图 6：Q8 单元在 nelx = 3、nely = 2 时的 edofMat 矩阵。
</b></center>

接着，`iK`（第 41 行）和 `jK`（第 42 行）分别为行索引向量和列索引向量。分别将 `edofMat` 与大小为 $16\times1$ 和 $1\times16$ 的全 1 向量作 Kronecker 积，再重排得到这两个向量。边界条件在第 44–48 行定义。`F`（第 44 行）和 `U`（第 45 行）分别为全局载荷向量和位移向量。`fixeddofs`（第 46 行）包含位移为零的自由度，`alldofs`（第 47 行）是包含全部自由度的行向量，自由自由度存入 `freedofs`（第 48 行）。停止条件为设计变量变化小于 0.001，或达到 200 次迭代，以先发生者为准。目标函数、单元目标贡献及目标导数分别记为 `f0`（第 84 行）、`f0e`（第 83 行）和 `df0`（第 85 行）。其余符号与函数同 `top88` [15] 或 `HoneyTop90` [5]。

### 4.2.2 Q9 单元连接矩阵的生成与边界条件定义

Q9 连接矩阵的生成与 Q8 类似，但相应矩阵和向量有所修改，以便在每个单元内有效容纳额外的中心节点。`noden`（第 40 行）按照节点在离散结构中的位置排列全部节点编号。当 `nelx = 3`、`nely = 2` 时：

$$
\texttt{noden}=\begin{bmatrix}
1&6&11&16&21&26&31\\
2&7&12&17&22&27&32\\
3&8&13&18&23&28&33\\
4&9&14&19&24&29&34\\
5&10&15&20&25&30&35
\end{bmatrix}.
$$

`nodeall`（第 41 行）按与 Q8 相同的方式包含全部节点编号，共有 $9\times\texttt{nelx}=27$ 列、$\texttt{nely}=2$ 行，如图 7 所示。

![[Sarkar2025_Fig7.png]]

<center><b>
图 7：Q9 单元在 nelx = 3、nely = 2 时的 nodeall 矩阵。
</b></center>

将 `nodeall` 重排为 9 列矩阵，得到 `nodenrs`（第 46 行）。与 Q8 程序相同，`nodenrs` 第 $i$ 行表示第 $i$ 个单元的节点编号：

$$
\texttt{nodenrs}=\begin{bmatrix}
3&13&11&1&8&12&6&2&7\\
5&15&13&3&10&14&8&4&9\\
13&23&21&11&18&22&16&12&17\\
15&25&23&13&20&24&18&14&19\\
23&33&31&21&28&32&26&22&27\\
25&35&33&23&30&34&28&24&29
\end{bmatrix},
$$

各行依次对应单元 1–6。接着，`iK`（第 49 行）和 `jK`（第 50 行）分别由 `edofMat`（第 47 行）与大小为 $18\times1$ 和 $1\times18$ 的全 1 向量作 Kronecker 积后重排得到。后续处理与 Q8 有限元相同。当 `nelx = 3`、`nely = 2` 时，`edofMat` 如图 8 所示。

![[Sarkar2025_Fig8.png]]

<center><b>
图 8：Q9 单元在 nelx = 3、nely = 2 时的 edofMat 矩阵。
</b></center>

## 4.3 过滤

如前所述，`ft = 1` 和 `ft = 2` 分别对应灵敏度过滤与密度过滤，按照文献 [15] 实现。过滤所需参数在 `topQ8` 的第 50–69 行和 `topQ9` 的第 58–77 行准备；灵敏度过滤和密度过滤分别在 `topQ8` 的第 88–93 行和 `topQ9` 的第 96–101 行执行。

## 4.4 优化循环

按照文献 [15]，采用最优性准则法更新设计变量。循环初始化位于 `topQ8` 第 71–74 行和 `topQ9` 第 79–82 行。每次优化迭代首先执行有限元分析，分别对应 `topQ8` 第 79–81 行和 `topQ9` 第 87–89 行；随后在 `topQ8` 第 95–107 行和 `topQ9` 第 103–115 行调用最优性准则法。当相邻两次设计的设计变量之差的 $L_\infty$ 范数小于 0.001，或迭代次数达到 200 时，终止优化循环。

# 5 结果与讨论

本节通过求解多个问题来展示所给 MATLAB 代码的有效性和稳健性，并比较采用 Q4、Q8 和 Q9 有限元所得的结果。首先求解经典的 MBB 优化问题，并给出其收敛历史和计算成本。随后，针对不同问题介绍 `topQ8` 和 `topQ9` 代码的多种扩展。此外，本文开发了 `topQ8CM` 和 `topQ9CM`，用最优性准则法设计柔顺机构（CM）；还给出了 `TOPressQ8` 和 `TOPressQ9`，用于生成承受设计相关载荷的承载结构。为了检验解是否收敛至离散解，还报告了非离散性度量（Measure of Non-Discreteness，$M_{nd}$）[48]，其定义为

$$
M_{nd}=\frac{\sum_{e=1}^{n}4\tilde{\rho}_e(1-\tilde{\rho}_e)}{n}\times 100\%.
\tag{21}
$$

其中，$n$ 为用于参数化设计域的单元总数。$M_{nd}=0\%$ 表示不存在物理密度处于中间值的单元。若所有单元的物理密度均为 $0.5$，则 $M_{nd}=100\%$，即优化设计完全为灰度设计。

## 5.1 MBB 问题

MBB 梁是拓扑优化中的一个经典优化问题，本文将其作为算例。图9给出了半对称 MBB 梁，在长度中点处施加集中力。在材料总量受限的条件下寻找最优材料分布是该优化问题的目标，其目标函数为最小化柔顺度。$x$ 和 $y$ 方向的尺寸分别记为 $L_x$ 和 $L_y$，且 $L_x:L_y=3:1$。外加集中力 $F$ 取单位值。

![[Sarkar2025_Fig9.png]]

<center><b>
图 9：半对称 MBB 梁设计。
</b></center>

### 5.1.1 MBB 梁结果

考虑三种不同的网格尺寸：$60\times20$、$150\times50$ 和 $300\times100$ 个单元。施加 $50\%$ 的体积约束，材料惩罚指数 $p$ 设为 3。采用灵敏度过滤和密度过滤求解优化问题；对于 $60\times20$、$150\times50$ 和 $300\times100$ 个有限元，过滤半径 $r_{min}$ 分别设为 2.4、6 和 12。

<center><b>
表 1：优化后的 MBB 梁。
</b></center>

![[Sarkar2025_Table1.png]]

表1给出了所得结果。第3、第4和第5列分别表示不采用过滤（`ft=0`）、采用灵敏度过滤（`ft=1`）和采用密度过滤（`ft=2`）时的优化结果。各行分别给出 Q4、Q8 和 Q9 有限元的结果，并采用上述收敛判据。结果表明，对于特定网格尺寸以及特定过滤方式或不采用过滤的情形，Q4 有限元所得柔顺度最低（表1）。不采用过滤时，Q4 有限元得到带有棋盘格模式的优化设计；尽管其柔顺度看似较低，但在实际中不可行。采用高阶单元（Q8 和 Q9）可消除棋盘格模式。然而，优化设计仍具有网格依赖性；采用灵敏度过滤和密度过滤后，这种依赖性得到抑制，结果满足 Q4<Q8<Q9。

### 5.1.2 MBB 收敛历史

对于包含 $300\times100$ 个单元的 MBB 梁，图10-12分别给出了 `ft=0`、`ft=1` 和 `ft=2` 时的收敛历史曲线。

![[Sarkar2025_Fig10.png]]

<center><b>
图 10：不采用过滤时的收敛曲线（$300\times100$）。
</b></center>

![[Sarkar2025_Fig11.png]]

<center><b>
图 11：采用灵敏度过滤时的收敛曲线（$300\times100$ 个有限元）。
</b></center>

图10表明，采用 Q8 和 Q9 的 MBB 优化设计比采用 Q4 时以更少的迭代次数收敛。Q8、Q9 和 Q4 分别需要 56、74 和 200 次迭代。对于所选网格尺寸和优化参数，可以观察到这种收敛行为；但这并非始终成立（表1）。图11表明，采用 Q4、Q8 和 Q9 有限元的 MBB 设计优化均运行至 200 次迭代。然而，迭代次数超过 20 后，曲线斜率几乎为零，即目标函数仅发生很小变化。因此，从实用角度看，可在第40或第50次迭代时停止优化，因为目标函数值已无显著变化。图12表明，40次迭代后，采用 Q4、Q8 和 Q9 有限元的优化总体上均已收敛。因此，可选择在第50或第60次优化迭代后停止；但本文仍将优化继续运行至 200 次迭代。

![[Sarkar2025_Fig12.png]]

<center><b>
图 12：采用密度过滤时的收敛曲线（$300\times100$ 个有限元）。
</b></center>

下面给出采用这些单元完成优化过程所需的计算时间。

<center><b>
表 2：MBB 梁问题采用不同尺寸、网格类型和过滤类型时的计算时间比较（秒）。
</b></center>

| 网格类型 | `ft` | $60\times20$ 时间 (s) | $60\times20$ DOFs | $150\times50$ 时间 (s) | $150\times50$ DOFs | $300\times100$ 时间 (s) | $300\times100$ DOFs | $450\times150$ 时间 (s) | $450\times150$ DOFs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Q4 | 0 | 7.045 | 2,562 | 4.322 | 15,402 | 59.040 | 60,802 | 44.286 | 136,202 |
| Q8 | 0 | 2.934 | 7,522 | 15.941 | 45,802 | 63.719 | 181,602 | 148.410 | 407,402 |
| Q9 | 0 | 4.762 | 9,922 | 19.505 | 60,802 | 103.134 | 241,602 | 287.591 | 542,402 |
| Q4 | 1 | 6.880 | 2,562 | 17.425 | 15,402 | 63.313 | 60,802 | 156.532 | 136,202 |
| Q8 | 1 | 21.093 | 7,522 | 132.473 | 45,802 | 619.240 | 181,602 | 1,498.926 | 407,402 |
| Q9 | 1 | 24.501 | 9,922 | 147.958 | 60,802 | 757.091 | 241,602 | 1,601.953 | 542,402 |
| Q4 | 2 | 13.274 | 2,562 | 22.264 | 15,402 | 162.773 | 60,802 | 668.605 | 136,202 |
| Q8 | 2 | 20.545 | 7,522 | 126.357 | 45,802 | 625.687 | 181,602 | 1,669.776 | 407,402 |
| Q9 | 2 | 24.671 | 9,922 | 153.400 | 60,802 | 863.868 | 241,602 | 2,120.614 | 542,402 |

### 5.1.3 MBB 计算时间

本文使用 AMD EPYC 7282 16核 2.80 GHz 处理器、128 GB RAM 和 64位操作系统，在 MATLAB R2020a 中运行代码。表2给出了不同算例采用不同网格时的计算时间。除 $60\times20$ 且 `ft=0` 的情形外，Q4 比 Q8 和 Q9 更快收敛至最优解，因为采用相同网格尺寸时，Q4 离散的设计域所含 DOFs 更少。对于 $60\times20$ 且 `ft=0` 的情形，在给定条件和所用参数下，Q8 比 Q4 和 Q9 收敛更快。总之，所需计算时间满足 Q4<Q8<Q9；这是一项显然的结论。对于各网格尺寸，总 DOFs 也呈相同趋势，但存在上述例外。

## 5.2 若干扩展

下面介绍 `topQ8` 和 `topQ9` 的多种扩展，用于求解不同问题。此处只说明与 `topQ8` 和 `topQ9` 有关的修改；读者和初学者可按类似方式修改 `top88` 代码。

### 5.2.1 多载荷

本问题求解承受多种载荷工况的悬臂梁（图13）。载荷由四个集中力组成：自由端顶部的一个向上载荷、自由端底部的一个向下载荷、梁中部顶部的一个向上载荷，以及梁中部底部的一个向下载荷。每个载荷的大小均取单位值。输入载荷 $F_i$（$i=1,2,3,4$）表示不同载荷工况（图13）。如图13所示，悬臂梁左边界固定。梁在 $x$ 和 $y$ 方向的尺寸分别记为 $L_x$ 和 $L_y$，且 $L_x:L_y=1:1$。

![[Sarkar2025_Fig13.png]]

<center><b>
图 13：具有多载荷工况的悬臂梁。
</b></center>

由于该问题包含四种载荷工况（图13），为了纳入每种工况，将输入载荷置于四列矩阵中；相应位移也在四列矩阵中计算并记录。列号表示所施加的载荷工况。目标函数写为 $f_0=\sum_{i=1}^{l}w_i\mathbf{U}_i^{T}\mathbf{K}\mathbf{U}_i$，其中，$\mathbf{U}_i$ 表示位移矩阵 $\mathbf{U}$ 第 $i$ 列所存储的第 $i$ 种载荷工况的位移；$l$ 为载荷工况数，$w_i$ 为所考虑载荷的权重。本文取 $w_i=1$；读者也可使用不同的 $w_i$ 运行代码并观察其影响。为适应该问题，代码修改如下。

为施加载荷、初始化位移向量并定义固定 DOFs，将 `topQ8` 的第44-46行修改为

```matlab
F = sparse([ndof-4*nely,ndof,nelx*(3*nely+2)+2,nely*(3*nelx+4)+2*(nelx+1)],...
    [1 2 3 4],[1 -1 1 -1],ndof,4); % nelx 为偶数时
% F = sparse([ndof-4*nely,ndof,nely*(3*nelx+1)+2*(nelx+1),(3*nely+2)*(nelx+1)],...
%     [1 2 3 4],[1 -1 1 -1],ndof,4); % nelx 为奇数时
U = zeros(ndof,4);
fixeddofs = [1:1:4*nely+2];
```

并将 `topQ9` 的第52-54行修改为

```matlab
F = sparse([ndof-4*nely,ndof,2*nelx*(2*nely+1)+2,2*(nelx+1)*(2*nely+1)],...
    [1 2 3 4],[1 -1 1 -1],ndof,4);
U = zeros(ndof,4);
fixeddofs = [1:1:4*nely+2];
```

为确定上述位移向量，将 `topQ8` 第81行和 `topQ9` 第89行替换为

```matlab
U(freedofs,:) = K(freedofs,freedofs)\F(freedofs,:);
```

<center><b>
表 3：多载荷问题的优化结果。
</b></center>

![[Sarkar2025_Table3.png]]

最后，为计算目标函数及其灵敏度，将 `topQ8` 第83-85行和 `topQ9` 第91-93行修改为以下代码：

```matlab
f0=0;
df0=0;
for i = 1:size(F,2)
    Ui = U(:,i);
    f0e = reshape(sum((Ui(edofMat)*KE).*Ui(edofMat),2),nely,nelx);
    f0 = f0 + sum(sum((Emin+xPhys.^penal*(E0-Emin)).*f0e));
    df0 = df0 - penal*(E0-Emin)*xPhys.^(penal-1).*f0e;
end
```

同样，可针对该问题修改 `top88`。

完成上述修改后求解该问题，结果见表3。采用 $100\times100$ 个有限元的网格。体积分数设为 0.5，$r_{min}=6$。收敛判据与 MBB 梁问题（图9）相同。第3、第4和第5列分别表示 `ft=0`、`ft=1` 和 `ft=2` 时的优化结果；第1、第2和第3行分别表示采用 Q4、Q8 和 Q9 有限元所得的优化结果。无论采用过滤与否，Q4 所得柔顺度均最低。与 `ft=0` 的结果相比，`ft=1` 和 `ft=2` 时的 $M_{nd}$ 很高；这是显然的，因为过滤会使密度值扩散。$r_{min}$ 越大，扩散越强，因而 $M_{nd}$ 越高，本文正属于这种情况。

### 5.2.2 含被动区域的设计

为了展示所给代码在含被动区域时的用法（图14），本文采用文献[5]最先求解并说明的问题定义。在结构设计中，有时要求设计域内的特定区域始终保持为实体（填充）或空洞（空），从而对材料的移除或添加施加约束。这些指定区域称为被动区域，对获得所需结构特性起着关键作用。本文采用含实体被动区域和空洞被动区域的设计域[5]。$L_x\times L_y$ 表示设计域尺寸。半径为 $L_y/3$ 的非设计圆形空洞区域，其圆心相对于左下角原点 $(0,0)$ 位于 $(L_x/3,L_y/2)$。此外，一个尺寸为 $0.2L_x\times0.2L_y$ 的非设计矩形实体区域位于顶点 $(0.7L_x,0.1L_y)$、$(0.9L_x,0.1L_y)$、$(0.9L_x,0.3L_y)$ 和 $(0.7L_x,0.3L_y)$ 围成的范围内。悬臂梁左侧固定，外载荷施加在右下角（图14）。

![[Sarkar2025_Fig14.png]]

<center><b>
图 14：含被动区域的设计域。
</b></center>

为适应该问题，对 `topQ8` 和 `topQ9` 作如下修改。为定义载荷、初始化位移向量并定义 `fixeddofs` 向量，将 `topQ8` 第44-46行和 `topQ9` 第52-54行替换为

```matlab
F = sparse(ndof,1,-1,ndof,1);
U = zeros(ndof,2);
fixeddofs = [1:1:4*nely+2];
```

定义一个 `nely`$\times$`nelx` 矩阵以区分主动单元和被动单元。在该矩阵中，数值 0、1 和 2 分别表示主动单元、空洞单元和实体单元。在优化循环开始前（`topQ8` 第74行之后、`topQ9` 第82行之后）加入以下代码：

```matlab
%% 定义被动单元
passive = zeros(nely,nelx);
for i = 1:nelx
    for j = 1:nely
        if sqrt((j-nely/2)^2+(i-nelx/3)^2) < nely/3
            passive(j,i) = 1; % 非设计空洞区域
        elseif (i>0.7*nelx && i<0.9*nelx) && (j>0.7*nely && j<0.9*nely)
            passive(j,i) = 2; % 非设计实体区域
        end
    end
end
```

在 `topQ8` 第103行与第104行之间、`topQ9` 第111行与第112行之间插入以下语句，以更新优化准则：

```matlab
xPhys(passive==1) = 0;
xPhys(passive==2) = 1;
```

采用 $200\times100$ 个有限元参数化设计域。允许体积分数设为 0.5，取 $r_{min}=5$。收敛判据与 MBB 梁设计相同。完成上述修改后，在不同过滤条件下求解问题，结果见表4。第3、第4和第5列分别表示 `ft=0`、`ft=1` 和 `ft=2` 时的优化结果；第1、第2和第3行分别表示采用 Q4、Q8 和 Q9 时的优化结果。无论是否采用过滤，Q4 均给出柔顺度最低的优化结构。`ft=0` 时的 $M_{nd}$ 小得多，说明优化设计接近离散结构。

<center><b>
表 4：含被动区域的优化结构。
</b></center>

![[Sarkar2025_Table4.png]]

### 5.2.3 悬臂梁

优化一个在右边界中点受集中力作用的悬臂梁问题（图15）。取 $L_x:L_y=3:1$，外加集中力 $F$ 取单位值。为求解该问题，作如下修改。为定义载荷向量，将 `topQ8` 第44行和 `topQ9` 第52行替换为

```matlab
F = sparse(ndof-2*nely,1,-1,ndof,1);
```

同样，为定义 `fixeddofs`，将 `topQ8` 第46行和 `topQ9` 第54行替换为

```matlab
fixeddofs = [1:1:4*nely+2];
```

![[Sarkar2025_Fig15.png]]

<center><b>
图 15：自由端中点受集中力作用的悬臂梁。
</b></center>

设计域采用 $150\times50$ 个有限元离散，取 $r_{min}=6$。表5给出了优化结果。第3、第4和第5列分别表示 `ft=0`、`ft=1` 和 `ft=2` 时的优化结果；第1、第2和第3行分别表示采用 Q4、Q8 和 Q9 时的优化结果。无论采用何种过滤，甚至不采用过滤，Q4 均得到柔顺度较低的结构。

<center><b>
表 5：优化后的悬臂梁。
</b></center>

![[Sarkar2025_Table5.png]]

## 5.3 柔顺机构

本文设计两个柔顺机构（反向器和夹持器），目标是在期望方向上最大化输出变形。通过分别适当修改 `topQ8` 和 `topQ9` 代码，开发用于优化柔顺机构的 `topQ8CM` 和 `topQ9CM`。

### 5.3.1 反向器

由于反向器机构的设计域具有对称性，图16仅给出其上半对称区域。左上角节点以及沿水平和竖直方向与其相邻的下一节点均固定。水平驱动力施加于左下角，图示弹簧表示驱动刚度 $k_{in}$（图16）。设计域底边施加位移对称边界条件。右下角为输出节点。期望柔顺机构产生与驱动方向相反的输出变形，如图16所示。输出节点处的弹簧表示工件刚度 $k_{out}$。采用 `nelx=160`、`nely=80` 个有限元参数化设计域，取 $r_{min}=3.6$，允许体积分数设为 0.3。

![[Sarkar2025_Fig16.png]]

<center><b>
图 16：反向器机构的上半对称区域。
</b></center>

对 `topQ8` 和 `topQ9` 代码作如下修改，分别形成 `topQ8CM` 和 `topQ9CM`。这些代码的默认设置用于优化反向器机构。

在 `topQ8` 第42行之后加入

```matlab
[Lnode,Rnode] = deal(nodenrs1(:,1), nodenrs1(:,end));
[Bnode,Tnode] = deal(union(nodenrs1(end,:),nodenrs2(end,:)),union(...
    nodenrs1(1,:),nodenrs2(1,:)));
```

在 `topQ9` 第50行之后加入

```matlab
[Lnode,Rnode] = deal(noden(:,1), noden(:,end));
[Bnode,Tnode] = deal(noden(end,:), noden(1,:));
```

向两个代码中加入以下各行：

```matlab
Tdof=[Tnode*2-1; Tnode*2];
Ldof=[Lnode'*2-1; Lnode'*2];
Bdof=[Bnode*2-1; Bnode*2];
Rdof=[Rnode'*2-1; Rnode'*2];
```

向量 `Lnode`、`Rnode`、`Bnode` 和 `Tnode` 给出构成设计域左、右、下和上边界的节点编号；矩阵 `Ldof`、`Rdof`、`Bdof` 和 `Tdof` 则给出相应 DOFs。这些矩阵的第1行和第2行分别表示 $x$ 和 $y$ 方向的 DOFs。

将 `topQ8` 第44-48行和 `topQ9` 第52-56行替换为

```matlab
U = zeros(ndof,1);
lambda1 = U;
inputdof = Bdof(1,1);
outputdof = Bdof(1,end);
F = sparse(inputdof,1,1,ndof,1);
L = sparse(outputdof,1,1,ndof,1);
fixeddofs = union([Tdof(:,1:2);Ldof(:,1:2)],Bdof(2,:));
alldofs = [1:ndof];
freedofs = setdiff(alldofs,fixeddofs);
[kin,kout] = deal (0.1,0.01);
```

`lambda1` 是与向量 `U` 大小相同的伴随变量向量。`inputdof` 和 `outputdof` 分别表示输入位置和输出位置的 DOF。输入驱动载荷由 `F` 定义，而 `L` 表示用于确定 $U_{out}$ 的向量。为了计入驱动刚度 $k_{in}$ 和工件刚度 $k_{out}$，先修改总体刚度矩阵 `K`，随后进行有限元分析。在 `topQ8` 第80行和 `topQ9` 第88行之后，按下式修改 `K` 并计算 $\lambda_1$：

```matlab
K(inputdof,inputdof) = K(inputdof,inputdof) + kin;
K(outputdof,outputdof) = K(outputdof,outputdof) + kout;
lambda1(freedofs) = K(freedofs,freedofs)\L(freedofs);
```

<center><b>
表 6：优化后的反向器机构。
</b></center>

![[Sarkar2025_Table6.png]]

其中，`kin=0.1` 和 `kout=0.01` 分别表示 $k_{in}$ 和 $k_{out}$。目标函数及其灵敏度由以下代码计算。将 `topQ8` 第83-84行和 `topQ9` 第91-92行替换为

```matlab
f0e = reshape(sum((lambda1(edofMat)*KE).*U(edofMat),2),nely,nelx);
f0 = L'*U;
```

由于本问题的灵敏度可为正也可为负，将 `topQ8` 第95-96行和 `topQ9` 第103-104行修改为

```matlab
l1 = 0; l2 = 100000; move = 0.1;
while (l2-l1)/(l2+l1) > 1e-4 && l2 > 1e-40
```

将 `topQ8` 第98行和 `topQ9` 第106行修改为

```matlab
xnew = max(0.001,max(x-move,min(1,min(x+move,x.*(max(1e-10,-df0./lmid)).^0.3))));
```

其中，$\beta_e$ 的任何负值均被替换为较小的正数 $10^{-10}$，以避免设计变量更新过程中出现复数乘法，因为 $0<\eta<1$。柔顺机构问题取 $\eta=0.3$ [30]。

表6给出了反向器柔顺机构的结果。第3、第4和第5列分别表示 `ft=0`、`ft=1` 和 `ft=2` 时的优化结果；第1、第2和第3行分别表示采用 Q4、Q8 和 Q9 时的优化结果。`ft=0` 时，Q9 给出的位移大于 Q4 和 Q8，期望方向变形量的排序为 Q9>Q8>Q4。采用灵敏度过滤和密度过滤时，Q4 给出的位移大于 Q8 和 Q9；`ft=1` 和 `ft=2` 时输出位移的排序均为 Q4>Q8>Q9。

### 5.3.2 夹持器

下面优化夹持器机构。图17给出了上半对称设计域。在输出位置，空洞区域为物体留出放置空间，实体区域表示夹持器夹持物体的上夹爪（图17）。施加刚度为 $k_{in}$ 的水平驱动力；在其作用下，希望两夹爪相互靠近，以夹持刚度为 $k_{out}$ 的物体。采用 $200\times100$ 个有限元参数化设计域。过滤半径设为 2.4，允许体积分数为 0.3，$k_{in}$ 和 $k_{out}$ 分别设为 0.1 和 0.01。

![[Sarkar2025_Fig17.png]]

<center><b>
图 17：夹持器机构的上半对称区域。
</b></center>

对 `topQ8CM` 和 `topQ9CM` 作如下修改以设计夹持器机构。为确定输出 DOFs 并施加边界条件，将 `topQ8CM` 第53行和 `topQ9CM` 第61行替换为

```matlab
outputdof = Rdof(2,(end-(2*nely/5)));
```

将 `topQ8CM` 第56行和 `topQ9CM` 第64行修改为

```matlab
fixeddofs = union([Tdof(:,1:2); Ldof(:,1:2)], [Bdof(2,1:(2*0.8*nelx+1))]);
```

与 5.2.2 节问题相似，在优化迭代前定义被动区域矩阵：

```matlab
%% 被动单元
passive = zeros(nely,nelx);
for i = 1:nelx
    for j = 1:nely
        if (i>0.8*nelx) && (j>0.8*nely)
            passive(j,i) = 1; % 非设计空洞区域
        elseif (i>0.8*nelx) && (j>0.75*nely && j<=0.8*nely)
            passive(j,i) = 2; % 非设计实体区域
        end
    end
end
```

最后，为计入被动单元，在 `topQ8CM` 第117行与第118行之间、`topQ9CM` 第125行与第126行之间加入以下代码，以修改优化准则：

```matlab
xPhys(passive==1) = 0;
xPhys(passive==2) = 1;
```

<center><b>
表 7：优化后的夹持器机构。
</b></center>

![[Sarkar2025_Table7.png]]

完成上述代码修改后，所得夹持器机构见表7。第3、第4和第5列分别表示 `ft=0`、`ft=1` 和 `ft=2` 时的优化结果；第1、第2和第3行分别表示采用 Q4、Q8 和 Q9 单元时的优化结果。无论是否采用过滤，Q4 给出的位移均大于 Q8 和 Q9。输出位移由大到小的顺序为 Q4>Q8>Q9。

## 5.4 压力载荷结构

当外加载荷随设计演化而变化时，这类载荷被归类为设计相关载荷。例如，当流体压力载荷作用于待优化设计域的边界时，载荷会随优化过程改变。因此，这类载荷带来多项挑战[32]。本文基于采用 Q4 单元参数化设计域的 `TOPress` 代码[^original-2][33]，开发了 `TOPressQ8` 和 `TOPressQ9`。这些代码的默认设置是优化最早见于文献[31]的承载内压拱设计，与 `TOPress` 代码的设置相似。


### 5.4.1 内压拱设计

图18给出了位移和压力载荷边界条件。设计域尺寸为 $L_x:L_y=2:1$。底边左、右两角固定，流体压力施加在底边。采用 `nelx`$\times$`nely`$=100\times50$ 个有限元离散设计域，取 $r_{min}=2$，允许体积分数为 0.5。

![[Sarkar2025_Fig18.png]]

<center><b>
图 18：内压拱问题的设计域。
</b></center>

为开发用于承载拱设计的 `TOPressQ8` 和 `TOPressQ9`，对 `TOPress` 作如下修改。

**`TOPressQ8` 代码开发：**

将 `TOPress` 第9-24行替换为

```matlab
[nodenrs1,nodenrs2]=deal((1:2*nely+1)'+(3*nely+2)*(0:nelx),...
    (2*nely+2:(3*nely+2))'+(3*nely+2)*(0:nelx-1));
nodeall=[nodenrs1(3:2:end,1:nelx) nodenrs1(3:2:end,2:nelx+1) ...
    nodenrs1(1:2:end-1,2:nelx+1) nodenrs1(1:2:end-1,1:nelx) ...
    nodenrs2(2:end,1:nelx) nodenrs1(2:2:end,2:nelx+1) ...
    nodenrs2(1:end-1,1:nelx) nodenrs1(2:2:end,1:nelx)];
nodenrs=reshape(nodeall,[],8); % 8 表示八节点单元
Udofs(1:nelx*nely,[1:2:16,2:2:16]) = [2*nodenrs-1,2*nodenrs];
ndof = max(max(Udofs)); % 总自由度数
[nel,nno] = deal(nelx*nely, ndof/2);
[Lnode,Rnode] = deal(nodenrs1(:,1), nodenrs1(:,end));
[Bnode,Tnode] = deal(union(nodenrs1(end,:),nodenrs2(end,:)),union(...
    nodenrs1(1,:),nodenrs2(1,:)));
[Pdofs,allPdofs,allUdofs]=deal(Udofs(:,2:2:end)/2,1:nno,1:2*nno);
iP = reshape(kron(Pdofs,ones(8,1)),64*nel,1);
jP = reshape(kron(Pdofs,ones(1,8))',64*nel,1);
iT = reshape(kron(Udofs,ones(8,1))',128*nel,1);
jT = reshape(kron(Pdofs,ones(1,16))',128*nel,1);
iK = reshape(kron(Udofs,ones(16,1))',256*nel,1);
jK = reshape(kron(Udofs,ones(1,16))',256*nel,1);
Kp11=[104,45,46,45;45,104,45,46;46,45,104,45;45,46,45,104];
Kp12=(-2)*[37,23,23,37;37,37,23,23;23,37,37,23;23,23,37,37];
Kp22=16*[13,0,2,0;0,13,0,2;2,0,13,0;0,2,0,13];
Kp=[Kp11,Kp12;Kp12',Kp22]/90; % 流动矩阵：Darcy 定律
KDp11=[6,2,3,2;2,6,2,3;3,2,6,2;2,3,2,6];
KDp12=(-2)*[3,4,4,3;3,3,4,4;4,3,3,4;4,4,3,3];
KDp22=4*[8,5,4,5;5,8,5,4;4,5,8,5;5,4,5,8];
KDp=[KDp11,KDp12;KDp12',KDp22]/180; % 排流矩阵
Te11=[-12,-8,-3,3;-12,3,-3,-8;8,12,-3,3;3,-12,-8,-3;...
    3,-3,12,8;3,8,12,-3;3,-3,-8,-12;8,3,-3,12];
Te12=2*[10,-7,0,7;7,0,-7,10;-10,-7,0,7;7,10,-7,0;...
    0,-7,-10,7;7,-10,-7,0;0,-7,10,7;7,0,-7,-10];
Te21=2*[-10,10,0,0;-13,-13,-7,-7;7,13,13,7;0,-10,10,0;0,0,10,-10;...
    7,7,13,13;-13,-7,-7,-13;-10,0,0,10];
Te22=8*[0,5,0,-5;-6,5,6,5;-5,6,-5,-6;-5,0,5,0;...
    0,5,0,-5;-6,-5,6,-5;5,6,5,-6;-5,0,5,0];
Te=[Te11,Te12;Te21,Te22]/180; % 转换矩阵
```

`TOPress` 第25-29行给出单元刚度计算，取自 `topQ8` 第8-30行。将 `TOPress` 第38行修改为

```matlab
PF([Tnode,Lnode',Rnode'])=0; PF(Bnode)=Pin; % 施加压力载荷
```

在 MMA 优化循环中，将 `TOPress` 第65、71和75行依次修改为

```matlab
Ae=reshape(Kp(:)*Kc'+KDp(:)*Dc',64*nel,1); % 单元流动矩阵
```

```matlab
Ts=reshape(Te(:)*ones(1,nel),128*nel,1); % 单元转换矩阵
```

```matlab
Ks=reshape(KE(:)*E',256*nel,1); % 单元刚度矩阵
```

将 `TOPress` 第81行中的 `ke` 替换为单元刚度矩阵 `KE`。本文采用 2006 版 MMA 优化器求解压力载荷问题。`ft=0` 时取 $r_{min}=1$。完成上述修改后，通过调用 `TOPressQ8(100,50,0.5,3,2,0.2,8,1,200)` 得到承载拱结构。

**`TOPressQ9` 代码开发：**

将 `TOPress` 第9-24行修改为

```matlab
noden=reshape([1:(2*nelx+1)*(2*nely+1)],(2*nely+1),(2*nelx+1));
nodeall=[noden(3:2:end,1:2:end-2) noden(3:2:end,3:2:end) ...
    noden(1:2:end-2,3:2:end) noden(1:2:end-2,1:2:end-2) ...
    noden(3:2:end,2:2:end-1) noden(2:2:end-1,3:2:end) ...
    noden(1:2:end-2,2:2:end-1) noden(2:2:end-1,1:2:end-2) ...
    noden(2:2:end-1,2:2:end-1)];
nodenrs = reshape(nodeall,[],9);
Udofs(1:nelx*nely,[1:2:18,2:2:18]) = [2*nodenrs-1,2*nodenrs];
ndof = max(max(Udofs)); % 总自由度数
[nel,nno] = deal(nelx*nely, ndof/2);
[Lnode,Rnode] = deal(noden(:,1), noden(:,end));
[Bnode,Tnode] = deal(noden(end,:), noden(1,:));
[Pdofs,allPdofs,allUdofs]=deal(Udofs(:,2:2:end)/2,1:nno,1:2*nno);
iP = reshape(kron(Pdofs,ones(9,1))',81*nel,1);
jP = reshape(kron(Pdofs,ones(1,9))',81*nel,1);
iT = reshape(kron(Udofs,ones(9,1))',162*nel,1);
jT = reshape(kron(Pdofs,ones(1,18))',162*nel,1);
iK = reshape(kron(Udofs,ones(18,1))',324*nel,1);
jK = reshape(kron(Udofs,ones(1,18))',324*nel,1);
Kp11=[56,-3,-2,-3;-3,56,-3,-2;-2,-3,56,-3;-3,-2,-3,56];
Kp12=2*[-9,5,5,-9,-16;-9,-9,5,5,-16;5,-9,-9,5,-16;5,5,-9,-9,-16];
Kp22=-16*[-11,2,0,2,6;2,-11,2,0,6;0,2,-11,2,6;2,0,2,-11,6;...
    6,6,6,6,-32];
Kp=[Kp11,Kp12;Kp12',Kp22]/90; % 流动矩阵：Darcy 定律
KDp11=[16,-4,1,-4;-4,16,-4,1;1,-4,16,-4;-4,1,-4,16];
KDp12=2*[4,-1,-1,4,2;4,4,-1,-1,2;-1,4,4,-1,2;-1,-1,4,4,2];
KDp22=4*[16,1,-4,1,8;1,16,1,-4,8;-4,1,16,1,8;1,-4,1,16,8;...
    8,8,8,8,64];
KDp=[KDp11,KDp12;KDp12',KDp22]/900; % 排流矩阵
Te11=[-12,-4,1,3;-12,3,1,-4;4,12,-3,-1;3,-12,-4,1;...
    -1,-3,12,4;-1,4,12,-3;3,1,-4,-12;4,-1,-3,12];
Te12=2*[8,-1,-2,-3,4;-3,-2,-1,8,4;-8,3,2,1,-4;-3,8,-1,-2,4;...
    2,3,-8,1,-4;1,-8,3,2,-4;-2,-1,8,-3,4;1,2,3,-8,-4];
Te21=2*[-8,8,-2,2;-3,-3,-1,-1;1,3,3,1;2,-8,8,-2;2,-2,8,-8;...
    1,1,3,3;-3,-1,-1,-3;-8,2,-2,8;-4,4,4,-4;-4,-4,4,4];
Te22=8*[0,1,0,-1,0;-6,1,-2,1,8;-1,6,-1,2,-8;-1,0,1,0,0;0,1,0,-1,0;...
    2,-1,6,-1,-8;1,-2,1,-6,8;-1,0,1,0,0;0,8,0,-8,0;-8,0,8,0,0];
Te=[Te11,Te12;Te21,Te22]/180; % 转换矩阵
```

单元刚度矩阵的确定方式与 `topQ9` 相似。将 `TOPress` 第38行修改为

```matlab
PF([Tnode,Lnode',Rnode'])=0; PF(Bnode)=Pin; % 施加压力载荷
```

在 MMA 优化循环中，将 `TOPress` 第65、71和75行依次修改为

```matlab
Ae=reshape(Kp(:)*Kc'+KDp(:)*Dc',81*nel,1); % 单元流动矩阵
```

```matlab
Ts=reshape(Te(:)*ones(1,nel),162*nel,1); % 单元转换矩阵
```

```matlab
Ks=reshape(KE(:)*E',324*nel,1); % 单元刚度矩阵
```

将 `TOPress` 第81行中的 `ke` 替换为单元刚度矩阵 `KE`。本文采用 2006 版 MMA 优化器求解压力载荷问题。`ft=0` 时取 $r_{min}=1$。完成上述修改后，调用 `TOPressQ9(100,50,0.5,3,2,0.2,8,1,200)` 优化承载拱结构。

<center><b>
表 8：优化后的内压拱承载结构。
</b></center>

![[Sarkar2025_Table8.png]]

表8表明，无论是否采用过滤，Q9 给出的柔顺度均低于 Q4 和 Q8。柔顺度排序可写为 Q4>Q8>Q9。第3列和第4列分别表示 `ft=0` 和 `ft=2` 时的优化结果；第1、第2和第3行分别表示采用 Q4、Q8 和 Q9 单元时的优化结果。可以看出，所有情形下优化拱的拓扑均相同；但 `ft=0` 时 $M_{nd}=0$，即得到完全黑白的拱设计。

### 5.4.2 加压腔体设计

下面求解最早见于文献[31]的加压腔体设计。图19给出了设计域以及位移和压力边界条件。空洞区域由施加压力载荷的流体占据，底边也承受流体压力载荷。实体被动区域以棕色表示。$L_x:L_y=3:2$，即采用 `nelx`$\times$`nely`$=120\times80$ 个有限元。取 $r_{min}=2$，体积分数为 0.5。左、右两个底角固定。

![[Sarkar2025_Fig19.png]]

<center><b>
图 19：加压腔体的设计域。
</b></center>

为求解加压腔体问题，对 `TOPressQ8` 和 `TOPressQ9` 作如下修改。

将 `TOPressQ8` 第72-73行和 `TOPressQ9` 第82-83行修改为

```matlab
elNrs = reshape(1:nel,nely,nelx);
sr1 = elNrs(3*nely/8:17*nely/40, 2*nelx/3:nelx);
sr2 = elNrs(23*nely/40:5*nely/8, 2*nelx/3:nelx);
vr1 = elNrs(17*nely/40:end,7*nelx/15:8*nelx/15);
vr2 = elNrs(17*nely/40:23*nely/40,8*nelx/15:nelx);
[NDS, NDV] = deal([sr1(:);sr2(:)], [vr1(:);vr2(:)]);
act = setdiff((1:nel)', union(NDS, NDV));
s1fix = elNrs(3*nely/8:17*nely/40, nelx);
s2fix = elNrs(23*nely/40:25*nely/40, nelx);
fixx = unique(Pdofs([s1fix(:); s2fix(:)],:));
```

加入下列代码行以施加输入流体压力载荷。将 `TOPressQ8` 第76行和 `TOPressQ9` 第86行修改为

```matlab
PF([unique(Pdofs(NDV,:))',Bnode]) = Pin; % 施加压力载荷
```

将 `TOPressQ8` 第80行和 `TOPressQ8` 第90行修改为下式，以计入固定 DOFs[^code-name]：

```matlab
fixedUdofs = [2*Bnode(1)-1 2*Bnode(1) 2*Bnode(end)-1 2*Bnode(end) 2*fixx'-1 2*fixx']; % 固定的位移自由度
```

<center><b>
表 9：加压腔体承载结构的优化结果。
</b></center>

![[Sarkar2025_Table9.png]]

表9表明，不采用过滤时，Q8 给出的柔顺度低于 Q4 和 Q9，柔顺度排序为 Q4>Q9>Q8。采用密度过滤时，Q9 给出的柔顺度低于 Q4 和 Q8，柔顺度排序可写为 Q4>Q9>Q8[^table9-order]。采用 Q4 时，优化设计中含有棋盘格模式。

[^table9-order]: 译者注：此处忠实保留正文说法。`ft=2` 时，表9中 Q4、Q8、Q9 的柔顺度分别为 124.5873、122.3616、122.2238；Q9 确为最小，但按表中数值排序应为 Q4>Q8>Q9，与正文所写 Q4>Q9>Q8 不一致。

通过前述多个采用灵敏度过滤和密度过滤的优化问题，可以看到这些过滤方法能获得不含棋盘格模式的优化设计，但仍包含灰度单元或灰度区域。下面介绍 Heaviside 投影过滤，它可给出接近 0-1 的优化设计。

## 5.5 Heaviside 投影过滤

Heaviside 投影过滤常用于获得近似二元（0-1）的最优解。在拓扑优化中使用 Heaviside 投影过滤时，需要同时采用设计变量、过滤变量和 Heaviside 投影变量。这里，物理变量（即 Heaviside 投影变量）[49,50] 定义为

$$
\bar{\rho}_j=\frac{\tanh(\beta\eta)+\tanh\!\left(\beta(\tilde{\rho}_j-\eta)\right)}{\tanh(\beta\eta)+\tanh\!\left(\beta(1-\eta)\right)}.
$$

其中，$\eta\in[0,1]$ 表示过滤阈值，$\beta\in[0,\infty)$ 控制函数陡峭程度。通常以延拓方式将 $\beta$ 从 $\beta_{in}=1$ 增大到指定最大值 $\beta_u$。本文取 $\beta_u=128$，并在优化中每 60 次迭代将 $\beta$ 加倍。Heaviside 投影变量 $\bar{\rho}_j$ 对过滤变量 $\tilde{\rho}_j$ 的偏导数为

$$
\frac{\partial\bar{\rho}_j}{\partial\tilde{\rho}_j}
=\beta\frac{1-\tanh^2\!\left(\beta(\tilde{\rho}_j-\eta)\right)}
{\tanh(\beta\eta)+\tanh\!\left(\beta(1-\eta)\right)}.
$$

利用链式法则，可以求得 Heaviside 投影变量 $\bar{\rho}_j$ 对设计变量 $\rho_j$ 的偏导数。下标 $j$ 表示第 $j$ 个单元。还可以进一步推导目标函数和约束对设计变量的导数。

代码作如下修改，以加入 Heaviside 投影过滤。以 `ft=3` 表示 Heaviside 投影过滤步骤，并将 `move` 设为 0.1。需要指出，在某些情形下，可能有必要超过移动限值，以控制优化过程的波动。

<center><b>
表 10：采用 Heaviside 投影过滤的半 MBB 梁优化结果。
</b></center>

![[Sarkar2025_Table10.png]]

在优化循环前插入与文献[5]所用代码相似的以下代码。将 `topQ8` 第72行和 `topQ9` 第80行替换为

```matlab
beta = 1;
eta = 0.5;
if (ft == 1 || ft == 2)
    xPhys = x;
elseif (ft == 3)
    xTilde = x; % xTilde 表示过滤变量
    xPhys = (tanh(beta * eta) + tanh(beta * (xTilde - eta))) ./ (...
        tanh(beta * eta) + tanh(beta * (1 - eta)));
end
```

目标函数和约束的灵敏度也将改变。为此，在 `topQ8` 第92行与第93行之间、`topQ9` 第100行与第101行之间插入

```matlab
elseif ft == 3
    dx = beta * (1 - (tanh(beta * (xTilde - eta)).^2)) ./ (...
        tanh(beta * eta) + tanh(beta * (1 - eta)));
    df0(:) = H * (df0(:) .* dx(:) ./ Hs);
    dv(:) = H * (dv(:) .* dx(:) ./ Hs);
```

基于同样的原因，还需在 `topQ8` 第102行与第103行之间、`topQ9` 第110行与第111行之间加入

```matlab
elseif ft == 3
    xTilde(:) = (H * xnew(:)) ./ Hs;
    xPhys = (tanh(beta * eta) + tanh(beta * (xTilde - eta))) ./ (...
        tanh(beta * eta) + tanh(beta * (1 - eta)));
```

最后，在优化循环末尾（即 `topQ8` 第112行之前和 `topQ9` 第120行之前）附加以下代码，执行正则化参数 $\beta$ 的延拓方案：

```matlab
if (ft == 3 && mod(loop, 60) == 0 && beta < 128)
    beta = 2 * beta;
end
```

优化过程中采用延拓策略，以保证可微性并防止陷入局部极小值[14]。每 60 次迭代将 $\beta$ 加倍，使参数 $\beta$ 从 1 逐步增大到 128。

表10给出了采用 Heaviside 投影过滤时半 MBB 梁拓扑优化设计的结果。第1、第2和第3列分别表示尺寸为 $60\times20$、$150\times50$ 和 $300\times100$ 时的优化结果；第1、第2和第3行分别表示采用 Q4、Q8 和 Q9 单元时的优化结果。考察所有结果可以发现，随着采用更高阶单元和更细网格，目标函数值逐渐收敛。因此，对于特定单元类型，粗网格给出的近似较差；在相同网格尺寸下，高阶单元给出的近似更好，从而得到更优的优化解。

# 6 结论

本文采用 Q4、Q8 和 Q9 四边形单元，对三类涉及不同物理场的拓扑优化问题进行了对比研究，包括恒定载荷和设计相关载荷作用下的柔顺度最小化，以及恒定驱动载荷作用下的柔顺机构优化。所得结果与采用 Q4 单元的公开代码结果进行了比较。首先，针对恒定载荷作用下 MBB 问题的柔顺度最小化，构建了采用 Q8 和 Q9 单元的代码，随后将其扩展到具有不同边界条件和载荷条件的多个问题。进一步修改这些代码，以求解恒定驱动作用下的柔顺机构，以及承受设计相关载荷的承载结构。对于 Q8 和 Q9 单元，这些代码提供了简单、高效的连接关系矩阵和单元刚度矩阵生成方法。采用 Q8 和 Q9 得到的优化设计不含棋盘格模式，但具有网格依赖性。代码中加入了灵敏度过滤和密度过滤，以消除网格依赖解；同时还给出了采用 Heaviside 投影过滤获得接近 0-1 优化解的步骤。

随着采用更高阶单元和更细网格，目标函数值逐渐收敛。粗网格给出的近似较差，而高阶单元可以提高精度和解的质量。采用 Q8 和 Q9 单元时，即使不使用任何过滤方案，也能获得不含棋盘格模式且接近 0-1 的设计。总体而言，对 Q4、Q8 和 Q9 采用相同过滤半径时，各过滤方案所得最终拓扑相同。对于恒定载荷作用下结构柔顺度最小化和恒定驱动作用下柔顺机构优化，代码采用最优性准则法更新设计变量；对于承受设计相关压力载荷的结构设计，则采用 MMA。所开发代码的有效性和稳健性通过上述优化问题进行了数值试验。

尽管 Q8 和 Q9 单元在柔顺度最小化问题中的有效性早已为拓扑优化领域所知，但公开对比研究、代码和教程，有助于初入该领域的人员、研究人员和学者从多个方面理解这些方法。此外，本文还给出了用于柔顺机构和承受设计相关载荷的承载结构的代码，为这些单元的应用开辟了新的方向，也为进一步研究不同高级约束（应力/屈曲）以及涉及不同物理场的问题提供了基础。

[^code-name]: 译者注：原文在此将两个代码名均写为 `TOPressQ8`；结合上下文，后一个疑为 `TOPressQ9`，此处保留原文。

# 作者贡献

Swagatam Islam Sarkar：概念构思、撰写、开发 MATLAB 代码。Prabhat Kumar：概念构思、撰写、审阅与编辑、开发 MATLAB 代码、监督指导。

# 利益冲突

作者声明不存在利益冲突。

# 数据可用性声明

MATLAB 代码在附录 A 和附录 B 中作了详细说明并完整给出。支持本研究结果的数据可在本文的 Supporting Information 中获取。

# 原文尾注

[^original-1]: 本文仅关注二维设计域。

[^original-2]: 访问自 <https://github.com/PrabhatIn/TOPress>。

# 参考文献

参考文献保留原文著录形式。[^ref-original]

[^ref-original]: 译者注：原文第 9 条的年份括号与页码缺失，第 26 条卷号写作 `1192`，第 30、36 条含多余括号，第 38 条题名含 `U3nder`；此处按原文保留，未据推测修改。


1. O. Sigmund, “A 99 Line Topology Optimization Code Written in Matlab,” *Structural and Multidisciplinary Optimization* 21 (2001): 120–127.

2. A. Saxena, “Topology Design With Negative Masks Using Gradient Search,” *Structural and Multidisciplinary Optimization* 44 (2011): 629–649.

3. R. Saxena and A. Saxena, “On Honeycomb Representation and Sigmoid Material Assignment in Optimal Topology Synthesis of Compliant Mechanisms,” *Finite Elements in Analysis and Design* 43, no. 14 (2007): 1082–1098.

4. C. Talischi, G. H. Paulino, and C. H. Le, “Honeycomb Wachspress Finite Elements for Structural Topology Optimization,” *Structural and Multidisciplinary Optimization* 37 (2009): 569–583.

5. P. Kumar, “HoneyTop90: A 90-Line Matlab Code for Topology Optimization Using Honeycomb Tessellation,” *Optimization and Engineering* 24, no. 2 (2023): 1433–1460.

6. C. Talischi, G. H. Paulino, A. Pereira, and I. F. Menezes, “PolyTop: A Matlab Implementation of a General Topology Optimization Framework Using Unstructured Polygonal Finite Element Meshes,” *Structural and Multidisciplinary Optimization* 45 (2012): 329–357.

7. P. Kumar and A. Saxena, “On Topology Optimization With Embedded Boundary Resolution and Smoothing,” *Structural and Multidisciplinary Optimization* 52 (2015): 1135–1159.

8. N. V. Nguyen, H. Nguyen-Xuan, and J. Lee, “Polygonal Composite Elements for Stress-Constrained Topology Optimization of Nearly Incompressible Materials,” *European Journal of Mechanics-A/Solids* 94 (2022): 104548.

9. M. Cui, M. Pan, J. Wang, and P. Li, “A Parameterized Level Set Method for Structural Topology Optimization Based on Reaction Diffusion Equation and Fuzzy Pid Control Algorithm,” *Electronic Research Archive* 30, no. 7 (2022.

10. X. Wang, M. Cui, W. Li, and M. Gao, “A Parameterized Level Set Method for Structural Topology Optimization Using the Approximate Re-Initialization Scheme,” *Mechanics Based Design of Structures and Machines* (2025): 1–32.

11. X. Wang, M. Cui, W. Li, and M. Gao, “Topology Optimization of Structures With Steady-State Heat Conduction Using an Improved Parameterized Level Set Method,” *Mechanics of Advanced Materials and Structures* (2025): 1–18.

12. X. Huang and M. Xie, *Evolutionary Topology Optimization of Continuum Structures: Methods and Applications* (John Wiley & Sons, 2010).

13. F. Wein, P. D. Dunning, and J. A. Norato, “A Review on Feature-Mapping Methods for Structural Optimization,” *Structural and Multidisciplinary Optimization* 62, no. 4 (2020): 1597–1638.

14. O. Sigmund and J. Petersson, “Numerical Instabilities in Topology Optimization: A Survey on Procedures Dealing With Checkerboards, Mesh-Dependencies and Local Minima,” *Structural Optimization* 16 (1998): 68–75.

15. E. Andreassen, A. Clausen, M. Schevenels, B. S. Lazarov, and O. Sigmund, “Efficient Topology Optimization in Matlab Using 88 Lines of Code,” *Structural and Multidisciplinary Optimization* 43 (2011): 1–16.

16. C. S. Jog, R. B. Haber, and M. P. Bendsøe, “Topology Design With Optimized, Self-Adaptive Materials,” *International Journal for Numerical Methods in Engineering* 37, no. 8 (1994): 1323–1350.

17. M. Xiao, S. Mukherjee, B. Raghavan, S. Dutta, P. Breitkopf, and W. Zhang, “Revisiting p-Refinement in Structural Topology Optimization,” *Structures* 34 (2021): 3640–3646.

18. A. Diaz and O. Sigmund, “Checkerboard Patterns in Layout Optimization,” *Structural optimization* 10 (1995): 40–45.

19. P. Kumar, A. Saxena, and R. A. Sauer, “Computational Synthesis of Large Deformation Compliant Mechanisms Undergoing Self and Mutual Contact,” *Journal of Mechanical Design* 141, no. 1 (2019): 012302.

20. N. D. Mankame and G. Ananthasuresh, “Comprehensive Thermal Modelling and Characterization of an Electro-Thermal-Compliant Microactuator,” *Journal of Micromechanics and Microengineering* 11, no. 5 (2001): 452.

21. P. Kumar, C. Schmidleithner, N. Larsen, and O. Sigmund, “Topology Optimization and 3d Printing of Large Deformation Compliant Mechanisms for Straining Biological Tissues,” *Structural and Multidisciplinary Optimization* 63 (2021): 1351–1366.

22. L. Clark, B. Shirinzadeh, J. Pinskier, Y. Tian, and D. Zhang, “Topology Optimisation of Bridge Input Structures With Maximal Amplification for Design of Flexure Mechanisms,” *Mechanism and Machine Theory* 122 (2018): 113–131.

23. T. Smit, S. Koppen, S. J. Ferguson, and B. Helgason, “Conceptual Design of Compliant Bone Scaffolds by Full-Scale Topology Optimization,” *Journal of the Mechanical Behavior of Biomedical Materials* 143 (2023): 105886.

24. J. Pinskier, X. Wang, L. Liow, et al., “Diversity-Based Topology Optimization of Soft Robotic Grippers,” *Advanced Intelligent Systems* 6, no. 4 (2024): 2300505.

25. G. Ananthasuresh, S. Kota, N. Kikuchi, et al., “Strategies for Systematic Synthesis of Compliant Mems,” in *Proceedings of the 1994 ASME Winter Annual Meeting* (1994), 677–686.

26. M. Frecker, G. Ananthasuresh, S. Nishiwaki, N. Kikuchi, and S. Kota, “Topological Synthesis of Compliant Mechanisms Using Multi-Criteria Optimization,” *ASME Journal of Mechanical Design* 1192 (1997): 238–245.

27. O. Sigmund, “On the Design of Compliant Mechanisms Using Topology Optimization,” *Journal of Structural Mechanics* 25, no. 4 (1997): 493–524.

28. B. Zhu, X. Zhang, H. Zhang, et al., “Design of Compliant Mechanisms Using Continuum Topology Optimization: A Review,” *Mechanism and Machine Theory* 143 (2020): 103622.

29. S. Rahmatalla and C. C. Swan, “Sparse Monolithic Compliant Mechanisms Using Continuum Structural Topology Optimization,” *International Journal for Numerical Methods in Engineering* 62, no. 12 (2005): 1579–1605.

30. M. Bendsøe and O. Sigmund, *Topology Optimization—Theory, Methods, and Applications*. Springer Verlag, 2003).

31. V. B. Hammer and N. Olhoff, “Topology Optimization of Continuum Structures Subjected to Pressure Loading,” *Structural and Multidisciplinary Optimization* 19 (2000): 85–92.

32. P. Kumar, J. S. Frouws, and M. Langelaar, “Topology Optimization of Fluidic Pressure-Loaded Structures and Compliant Mechanisms Using the Darcy Method,” *Structural and Multidisciplinary Optimization* 61 (2020): 1637–1655.

33. P. Kumar, “TOPress: A MATLAB Implementation for Topology Optimization of Structures Subjected to Design-Dependent Pressure Loads,” *Structural and Multidisciplinary Optimization* 66, no. 4 (2023): 97.

34. R. Picelli, A. Neofytou, and H. A. Kim, “Topology Optimization for Design-Dependent Hydrostatic Pressure Loading via the Level-Set Method,” *Structural and Multidisciplinary Optimization* 60, no. 4 (2019): 1313–1326.

35. P. Kumar and M. Langelaar, “On Topology Optimization of Design-Dependent Pressure-Loaded Three-Dimensional Structures and Compliant Mechanisms,” *International Journal for Numerical Methods in Engineering* 122, no. 9 (2021): 2205–2220.

36. J. Pinskier, P. Kumar, M. Langelaar, and D. Howard, “Automated Design of Pneumatic Soft Grippers Through Design-Dependent Multi-Material Topology Optimization,” in *2023 IEEE International Conference on Soft Robotics (RoboSoft)*. IEEE, 2023), 1–7.

37. P. Kumar and M. Langelaar, “Topological Synthesis of Fluidic Pressure-Actuated Robust Compliant Mechanisms,” *Mechanism and Machine Theory* 174 (2022): 104871.

38. T. T. Banh, S. Shin, J. Kang, and D. Lee, “Frequency-Constrained Topology Optimization in Incompressible Multi-Material Systems U3nder Design-Dependent Loads,” *Thin-Walled Structures* 196 (2024): 111467.

39. K. Svanberg, “The Method of Moving Asymptotes—A New Method for Structural Optimization,” *International Journal for Numerical Methods in Engineering* 24, no. 2 (1987): 359–373.

40. S. Zheng, W. Tang, and B. Li, “A New Topology Optimization Framework for Stiffness Design of Beam Structures Based on the Transformable Triangular Mesh Algorithm,” *Thin-Walled Structures* 154 (2020): 106831.

41. C. Talischi, G. H. Paulino, and C. H. Le, “Topology Optimization Using Wachspress-Type Interpolation With Hexagonal Elements,” *AIP Conference Proceedings* 973 (2008): 309–314.

42. T. R. Chandrupatla and A. D. Belegundu, *Introduction to Finite Elements in Engineering*, 2012.

43. S. Cen, M.-J. Zhou, Y. Shang, et al., “Shape-Free Finite Element Method: Another Way Between Mesh and Mesh-Free Methods,” *Mathematical Problems in Engineering* 2013 (2013): 491626.

44. K. Bathe, *Finite Element Procedures*, 2006.

45. J. N. Reddy, *An Introduction to the Finite Element Method*, vol. 27, 1993.

46. M. P. Bendsøe, “Optimal Shape Design as a Material Distribution Problem,” *Structural Optimization* 1 (1989): 193–202.

47. T. E. Bruns and D. A. Tortorelli, “Topology Optimization of Non-Linear Elastic Structures and Compliant Mechanisms,” *Computer Methods in Applied Mechanics and Engineering* 190, no. 26–27 (2001): 3443–3459.

48. O. Sigmund, “Morphology-Based Black and White Filters for Topology Optimization,” *Structural and Multidisciplinary Optimization* 33 (2007): 401–424.

49. F. Wang, B. S. Lazarov, and O. Sigmund, “On Projection Methods, Convergence and Robust Formulations in Topology Optimization,” *Structural and Multidisciplinary Optimization* 43 (2011): 767–784.

50. P. Kumar, “Topology Optimization of Stiff Structures Under Self-Weight for Given Volume Using a Smooth Heaviside Function,” *Structural and Multidisciplinary Optimization* 65, no. 4 (2022): 128.

# 附录 A：MATLAB 代码 TopQ8

```matlab
%%%% 采用 Q8 单元的拓扑优化代码 %%%%
function topQ8(nelx,nely,volfrac,penal,rmin,ft)
%% 材料参数
E0 = 1;
Emin = 1e-9;
nu = 0.3;
%% 有限元分析准备
A11=[312,85,146,15,138,35,124,-15;85,312,-15,124,35,138,15,146;
146,-15,312,-85,124,15,138,-35;15,124,-85,312,-15,146,-35,138;
138,35,124,-15,312,85,146,15;35,138,15,146,85,312,-15,124;
124,15,138,-35,146,-15,312,-85;-15,146,-35,138,15,124,-85,312];
A12=[77,25,26,5,43,5,34,-5;-5,34,5,43,5,26,-25,77;
77,-25,34,5,43,-5,26,-5;5,34,-25,77,-5,26,-5,43;
43,5,34,-5,77,25,26,5;5,26,25,77,-5,34,5,43;
43,-5,26,-5,77,-25,34,5;-5,26,-5,43,5,34,-25,77]*4;
A22=[-46,0,0,5,-14,0,0,-5;0,-32,5,0,0,2,-5,0;0,5,-32,0,0,-5,2,0;
5,0,0,-46,-5,0,0,-14;-14,0,0,-5,-46,0,0,5;0,2,-5,0,0,-32,5,0;
0,-5,2,0,0,5,-32,0;-5,0,0,-14,5,0,0,-46]*16;
B11=[104,-85,34,45,46,-35,56,-45;-85,104,-45,56,-35,46,45,34;
34,-45,104,85,56,45,46,35;45,56,85,104,-45,34,35,46;
46,-35,56,-45,104,-85,34,45;-35,46,45,34,-85,104,-45,56;
56,45,46,35,34,-45,104,85;-45,34,35,46,45,56,85,104];
B12=[3,-35,-20,5,-3,5,-40,55;55,-40,5,-3,5,-20,-35,3;
3,35,-40,-55,-3,-5,-20,-5;-55,-40,35,3,-5,-20,-5,-3;
-3,5,-40,55,3,-35,-20,5;5,-20,-35,3,55,-40,5,-3;
-3,-5,-20,-5,3,35,-40,-55;-5,-20,-5,-3,-55,-40,35,3]*4;
B22=[6,0,0,5,-6,0,0,-5;0,20,5,0,0,10,-5,0;0,5,20,0,0,-5,10,0;
5,0,0,6,-5,0,0,-6;-6,0,0,-5,6,0,0,5;0,10,-5,0,0,20,5,0;
0,-5,10,0,0,5,20,0;-5,0,0,-6,5,0,0,6]*16;
KE=1/(-1+nu^2)/360*([A11 A12;A12' A22]+nu*[B11 B12;B12' B22]);
%% 生成自由度矩阵
[nodenrs1, nodenrs2]=deal((1:2*nely+1)'+(3*nely+2)*(0:nelx),...
(2*nely+2:(3*nely+2))'+(3*nely+2)*(0:nelx-1));
nodeall=[nodenrs1(3:2:end,1:nelx) nodenrs1(3:2:end,2:nelx+1) ...
nodenrs1(1:2:end-1,2:nelx+1) nodenrs1(1:2:end-1,1:nelx) ...
nodenrs2(2:end,1:nelx) nodenrs1(2:2:end,2:nelx+1) ...
nodenrs2(1:end-1,1:nelx) nodenrs1(2:2:end,1:nelx)];
nodenrs=reshape(nodeall,[],8); % 8 for 8-noded elements
edofMat(1:nelx*nely,[1:2:16,2:2:16]) = [2*nodenrs-1,2*nodenrs];
ndof = max(max(edofMat)); % Total number of DOFs
iK = reshape(kron(edofMat,ones(16,1))',256*nelx*nely,1);
jK = reshape(kron(edofMat,ones(1,16))',256*nelx*nely,1);
% 定义边界条件（半 MBB 梁）
F = sparse(2,1,-1,ndof,1);
U = zeros(ndof,1);
fixeddofs = union([1:2:(4*nely+1)],ndof);
alldofs = [1:ndof];
freedofs = setdiff(alldofs,fixeddofs);
%% 构造过滤器
iH = ones(nelx*nely*(2*(ceil(rmin)-1)+1)^2,1);
jH = ones(size(iH));
sH = zeros(size(iH));
k = 0;
for i1 = 1:nelx
  for j1 = 1:nely
    e1 = (i1-1)*nely+j1;
    for i2 = max(i1-(ceil(rmin)-1),1):min(i1+(ceil(rmin)-1),nelx)
      for j2 = max(j1-(ceil(rmin)-1),1):min(j1+(ceil(rmin)-1),nely)
        e2 = (i2-1)*nely+j2;
        k = k+1;
        iH(k) = e1;
        jH(k) = e2;
        sH(k) = max(0,rmin-sqrt((i1-i2)^2+(j1-j2)^2));
      end
    end
  end
end
H = sparse(iH,jH,sH);
Hs = sum(H,2);
%% 初始化迭代
x = repmat(volfrac,nely,nelx);
xPhys = x;
loop = 0;
change = 1;
%% 开始迭代
while change > 0.001 && loop < 200
  loop = loop + 1;
  %% 有限元分析
  sK = reshape(KE(:)*(Emin+xPhys(:)'.^penal*(E0-Emin)),[],1);
  K = sparse(iK,jK,sK);
  U(freedofs) = K(freedofs,freedofs)\F(freedofs);
  %% 目标函数与灵敏度分析
  f0e = reshape(sum((U(edofMat)*KE).*U(edofMat),2),nely,nelx);
  f0 = sum(sum((Emin+xPhys.^penal*(E0-Emin)).*f0e));
  df0 = -penal*(E0-Emin)*xPhys.^(penal-1).*f0e;
  dv = ones(nely,nelx);
  %% 灵敏度过滤
  if ft == 1
    df0(:) = H*(x(:).*df0(:))./Hs./max(1e-3,x(:));
  elseif ft == 2
    df0(:) = H*(df0(:)./Hs);
    dv(:) = H*(dv(:)./Hs);
  end
  %% 最优性准则
  l1 = 0; l2 = 1e9; move = 0.2;
  while (l2-l1)/(l1+l2) > 1e-3
    lmid = 0.5*(l2+l1);
    xnew=max(0,max(x-move,min(1,min(x+move,x.*sqrt(-df0./dv/lmid)))));
    if ft == 1 || ft==0
      xPhys = xnew;
    elseif ft == 2
      xPhys(:) = (H*xnew(:))./Hs;
    end
    if sum(xPhys(:))>volfrac*nelx*nely, l1=lmid; else l2=lmid; end
  end
  change = max(abs(xnew(:)-x(:)));
  x = xnew;
  %% 输出结果
  fprintf('It.:%4i Obj.:%9.4f Vol.:%5.2f\n',loop,f0,mean(xPhys(:)));
  %% 绘制密度场
  colormap(gray); imagesc(1-xPhys); caxis([0 1]); axis equal; axis off; drawnow;
end
```

# 附录 B：MATLAB 代码 TopQ9

```matlab
%%%% 采用 Q9 单元的拓扑优化代码 %%%%
function topQ9(nelx,nely,volfrac,penal,rmin,ft)
%% 材料参数
E0 = 1;
Emin = 1e-9;
nu = 0.3;
%% 有限元分析准备
A11=[168,45,2,15,-6,-5,-20,-15,-100;45,168,-15,-20,-5,-6,15,2,60;
2,-15,168,-45,-20,15,-6,5,-100;15,-20,-45,168,-15,2,5,-6,-60;
-6,-5,-20,-15,168,45,2,15,36;-5,-6,15,2,45,168,-15,-20,20;
-20,15,-6,5,2,-15,168,-45,36;-15,2,5,-6,15,-20,-45,168,-20;
-100,60,-100,-60,36,20,36,-20,480]*(-1);
A12=[15,-6,-5,-9,-5,2,-15,24,20;2,-5,-9,-5,-6,15,25,20,24;
-15,2,15,-9,5,-6,5,24,-20;2,-15,25,5,-6,5,-9,-20,24;
-5,2,-15,25,15,-6,-5,24,20;-6,15,25,-15,2,-5,-9,20,24;
5,-6,5,25,-15,2,15,24,-20;-6,5,-9,15,2,-15,25,-20,24;
0,24,20,8,0,24,-20,32,0]*4;
A22=[-36,5,6,0,-2,-5,6,0,28;5,-36,0,6,-5,-2,0,28,0;
6,0,-30,-5,6,0,2,0,8;0,6,-5,-30,0,6,5,8,0;
-2,-5,6,0,-36,5,6,0,28;-5,-2,0,6,5,-36,0,28,0;
6,0,2,5,6,0,-30,0,8;0,28,0,8,0,28,0,-96,0;
28,0,8,0,28,0,8,0,-96]*16;
B11=[56,-45,-14,45,-2,5,8,-45,28;-45,56,-45,8,5,-2,45,-14,180;
-14,-45,56,45,8,45,-2,-5,28;45,8,45,56,-45,-14,-5,-2,-180;
-2,5,8,-45,56,-45,-14,45,4;5,-2,45,-14,-45,56,-45,8,-20;
8,45,-2,-5,-14,-45,56,45,4;-45,-14,-5,-2,45,8,45,56,20;
28,180,28,-180,4,-20,4,20,224];
B12=[-45,4,-5,1,-5,-16,45,-8,20;-16,-5,1,-5,4,-45,7,20,-8;
45,-16,-45,1,5,4,5,-8,-20;-16,45,7,5,4,5,1,-20,-8;
-5,-16,45,7,-45,4,-5,-8,20;4,-45,7,45,-16,-5,1,20,-8;
5,4,5,7,45,-16,-45,-8,-20;4,5,1,-45,-16,45,7,-20,-8;
0,-8,20,8,0,-8,-20,-64,0]*4;
B22=[8,5,-2,0,-2,-5,-2,0,4;5,8,0,-2,-5,-2,0,4,0;
-2,0,14,-5,-2,0,2,0,-16;0,-2,-5,14,0,-2,5,-16,0;
-2,-5,-2,0,8,5,-2,0,4;-5,-2,0,-2,5,8,0,4,0;
-2,0,2,5,-2,0,14,0,-16;0,4,0,-16,0,4,0,32,0;
4,0,-16,0,4,0,-16,0,32]*16;
KE = 1/(-1+nu^2)/360*([A11 A12;A12' A22]+nu*[B11 B12;B12' B22]);
%% 生成自由度矩阵
noden=reshape([1:(2*nelx+1)*(2*nely+1)],(2*nely+1),(2*nelx+1));
nodeall=[noden(3:2:end,1:2:end-2) noden(3:2:end,3:2:end) ...
noden(1:2:end-2,3:2:end) noden(1:2:end-2,1:2:end-2) ...
noden(3:2:end,2:2:end-1) noden(2:2:end-1,3:2:end) ...
noden(1:2:end-2,2:2:end-1) noden(2:2:end-1,1:2:end-2) ...
noden(2:2:end-1,2:2:end-1)];
nodenrs = reshape(nodeall,[],9);
edofMat(1:nelx*nely,[1:2:18,2:2:18]) = [2*nodenrs-1,2*nodenrs];
ndof = max(max(edofMat)); % Total number of DOFs
iK = reshape(kron(edofMat,ones(18,1))',324*nelx*nely,1);
jK = reshape(kron(edofMat,ones(1,18))',324*nelx*nely,1);
% 定义边界条件（半 MBB 梁）
F = sparse(2,1,-1,ndof,1);
U = zeros(ndof,1);
fixeddofs = union([1:2:(4*nely+1)],[ndof]);
alldofs = [1:ndof];
freedofs = setdiff(alldofs,fixeddofs);
%% 构造过滤器
iH = ones(nelx*nely*(2*(ceil(rmin)-1)+1)^2,1);
jH = ones(size(iH));
sH = zeros(size(iH));
k = 0;
for i1 = 1:nelx
  for j1 = 1:nely
    e1 = (i1-1)*nely+j1;
    for i2 = max(i1-(ceil(rmin)-1),1):min(i1+(ceil(rmin)-1),nelx)
      for j2 = max(j1-(ceil(rmin)-1),1):min(j1+(ceil(rmin)-1),nely)
        e2 = (i2-1)*nely+j2;
        k = k+1;
        iH(k) = e1;
        jH(k) = e2;
        sH(k) = max(0,rmin-sqrt((i1-i2)^2+(j1-j2)^2));
      end
    end
  end
end
H = sparse(iH,jH,sH);
Hs = sum(H,2);
%% 初始化迭代
x = repmat(volfrac,nely,nelx);
xPhys = x;
loop = 0;
change = 1;
%% 开始迭代
while change > 0.001 && loop < 200
  loop = loop + 1;
  %% 有限元分析
  sK = reshape(KE(:)*(Emin+xPhys(:)'.^penal*(E0-Emin)),[],1);
  K = sparse(iK,jK,sK);
  U(freedofs) = K(freedofs,freedofs)\F(freedofs);
  %% 目标函数与灵敏度分析
  f0e = reshape(sum((U(edofMat)*KE).*U(edofMat),2),nely,nelx);
  f0 = sum(sum((Emin+xPhys.^penal*(E0-Emin)).*f0e));
  df0 = -penal*(E0-Emin)*xPhys.^(penal-1).*f0e;
  dv = ones(nely,nelx);
  %% 灵敏度过滤
  if ft == 1
    df0(:) = H*(x(:).*df0(:))./Hs./max(1e-3,x(:));
  elseif ft == 2
    df0(:) = H*(df0(:)./Hs);
    dv(:) = H*(dv(:)./Hs);
  end
  %% 最优性准则
  l1 = 0; l2 = 1e9; move = 0.2;
  while (l2-l1)/(l1+l2) > 1e-3
    lmid = 0.5*(l2+l1);
    xnew=max(0,max(x-move,min(1,min(x+move,x.*sqrt(-df0./dv/lmid)))));
    if ft == 1 || ft==0
      xPhys = xnew;
    elseif ft == 2
      xPhys(:) = (H*xnew(:))./Hs;
    end
    if sum(xPhys(:))>volfrac*nelx*nely, l1=lmid; else l2=lmid; end
  end
  change = max(abs(xnew(:)-x(:)));
  x = xnew;
  %% 输出结果
  fprintf('It.:%4i Obj.:%9.4f Vol.:%5.2f\n',loop,f0,mean(xPhys(:)));
  %% 绘制密度场
  colormap(gray); imagesc(1-xPhys); caxis([0 1]); axis equal; axis off; drawnow;
end
```
