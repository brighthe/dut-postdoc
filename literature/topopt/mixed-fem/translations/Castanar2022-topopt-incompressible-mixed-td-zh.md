---
title: "翻译：基于拓扑导数与混合格式的不可压缩结构拓扑优化 (Topological derivative-based topology optimization of incompressible structures using mixed formulations)"
tags:
  - translation
  - mixed-fem
  - topology-optimization
  - topological-derivative
  - incompressible
status: "done"
date_created: 2026-09-11
date_updated: 2026-09-11
source: "../sources/Castanar2022-topopt-incompressible-mixed-td.pdf"
citekey: "castanarTopologicalDerivativebasedTopology2022"
language: "zh-CN"
---

# Topological Derivative-Based Topology Optimization of Incompressible Structures Using Mixed Formulations

---

# 信息

- **中文标题**：基于拓扑导数与混合格式的不可压缩结构拓扑优化
- **英文标题**：Topological derivative-based topology optimization of incompressible structures using mixed formulations
- **作者**：Inocencio Castañar; Joan Baiges; Ramon Codina; Henning Venghaus
- **作者单位**：
  - 加泰罗尼亚理工大学（Universitat Politècnica de Catalunya · BarcelonaTech, UPC, Jordi Girona 1-3, Edifici C1, 08034 Barcelona, Spain）
  - 国际数值工程计算方法中心（Centre Internacional de Mètodes Numèrics en Enginyeria, CIMNE, Edifici C1, Campus Nord UPC, Gran Capitán S/N, 08034 Barcelona, Spain）
- **期刊**：*Computer Methods in Applied Mechanics and Engineering* (CMAME)
- **卷 / 期 / 文章号**：Vol. 390, Article 114438 (2022)
- **DOI**：[10.1016/j.cma.2021.114438](https://doi.org/10.1016/j.cma.2021.114438)
- **在线发表 / 正式卷期**：2022 年 2 月
- **Better BibTeX key**：`castanarTopologicalDerivativebasedTopology2022`
- **译文状态**：全文翻译与核验完成（`done`）
- **图件资产**：全部 20 幅插图已提取并保存至 `literature/topopt/assets/Castanar2022_Fig1.png` ~ `Castanar2022_Fig20.png`

---

# 摘要

在本工作中，提出了一种基于拓扑导数概念的拓扑优化算法，同时适用于近不可压缩与完全不可压缩材料。为了处理此类材料，提出了一种根据偏量与体积（球偏）分量对极化张量（Polarization tensor）进行的新型分解。在线弹性力学背景下应用混合有限元格式，不仅能够处理不可压缩材料行为，还能够在应力计算中获得更高的精度。系统通过变分多尺度（Variational Multiscale, VMS）方法进行稳定化，该方法基于将未知量分解为可解尺度与亚格子尺度以防止数值振荡。文中展示并讨论了若干数值算例，以评估所提格式的稳健性及其在不可压缩弹性实体拓扑优化问题中的适用性。

**关键词**：拓扑优化 (Topology Optimization)；拓扑导数 (Topological Derivative)；不可压缩弹性 (Incompressible Elasticity)；混合插值 (Mixed interpolations)；稳定化方法 (Stabilization methods)

---

# 1 引言 (Introduction)

结构拓扑优化的目标是在给定的边界条件集合下，在设计域内寻找材料的最优布局，使得所产生的材料分布满足一组性能指标 [1]。目前存在若干类拓扑优化方法，例如基于密度的方法（包括广受欢迎的 SIMP 技术）[2]、硬剔除法（hard-kill methods）[3]、边界演化方法（如水平集方法）[4] 等等 [5]。针对此类问题的一种相对较新的方法基于拓扑导数（topological derivative）概念 [6]。该导数量度了给定的形状泛函对于无穷小奇异域摄动的灵敏度，并且由于它可用作优化过程中的最速下降方向，已成为一种非常强大的工具 [7, 8, 9]。

不可压缩材料是指在整个运动过程中保持其体积恒定的材料。在很多情况下，这是连续介质力学和计算力学中经常采用的常见理想化假设。许多高分子聚合物材料在承受有限应变时没有明显的体积改变。此外，许多生物材料和若干类土壤均可建模为近不可压缩或完全不可压缩介质 [10]。

在小应变固体力学问题中，通常优先采用标准的不可压缩低阶有限元 [11]。所谓标准不可约（irreducible）格式，是指仅将位移场作为问题的主未知量，而所有其他场（如应力场和应变场）均通过后处理获得。不幸的是，这种方法在近不可压缩和完全不可压缩工况下表现极差：体积自锁与剪切自锁、压力振荡以及在弯曲主导情况下的劣质表现，都是常观察到的数值病态现象 [12]。

为了克服这些问题，可以借鉴起源于流体力学的一种途径。当考虑固体力学问题的静态、不可压缩、无穷效应变情形时，我们得到一个在数学形式上与流体力学中 Stokes 问题完全相同的椭圆型问题 [13, 14]。因此，将流体力学中使用的速度/压力混合方法引入固体力学问题是极其合理的——在固体力学中它转化为位移/压力混合方法 [15]。该途径促成了流体力学领域不同实现方案向固体力学领域的推广。参见文献 [16, 17, 18, 19]，在这些工作中，不可压缩非线性材料问题通过变分多尺度方法（Variational Multiscale Method, VMS）进行了稳定化处理。值得注意的是，在上述引用文献中采用了正交亚格子尺度方法（Orthogonal Subscales Method, OSS）[34, 20]，它是文献 [22] 中提出的原始稳定化方法的一种变体。这些将应变/位移对以及应力/位移对作为主变量的工作，证明了混合有限元在固体力学中的优越性能。通过使用多个主未知量，每个节点的未知量数目显著增加——特别是当考虑应力或应变时——但它们也显著提高了计算精度。此外，在文献 [23] 中，对文献 [35] 提出的位移/压力/应力或位移/压力/应变三场格式进行了测试，发现当求解既要求不可压缩、又要求应力和应变场具备高精度的算例时非常有效 [36]。

据我们所知，目前面向不可压缩材料拓扑优化问题的研究仍十分有限。在文献 [24, 25] 中，采用针对单元的特定插值方案的混合有限元格式，并对体积模量和剪切模量引入了一类 SIMP 插值 [26]，随后的优化问题通过移动渐近线方法（MMA）[27] 进行求解。进一步地，文献 [28] 提出了比例边界有限元（SBFEM）混合格式以规避位移/压力混合问题的 inf-sup 条件，并应用移动等值面阈值（MIST）方法求解拓扑优化问题。最后，文献 [29] 针对若干种材料插值提出了一种基于密度的拓扑优化方法，并针对近不可压缩材料采用了位移/压力混合格式。

在当前工作中，我们主张将拓扑导数概念与水平集方法相结合来处理拓扑优化问题。然而，在结构拓扑设计的背景下，拓扑导数迄今仅在使用经典的基于位移的格式下被用作下降方向 [30]。因此，该方法局限于可压缩材料。当考虑近不可压缩和完全不可压缩材料行为时，控制方程和拓扑导数表达式均出现奇异性。我们通过引入如文献 [23] 所述的偏量/体积（球偏）分解来克服这一难题，从而获得混合有限元格式。遵循这一思路，本文提出了一种新型的偏量/球偏分解拓扑导数表达式，使得我们能够准确计算不可压缩材料的拓扑导数。结合水平集方法，该方法被用于获取最优拓扑设计。

本文结构安排如下：在第 2 节中，概述了线弹性力学的混合位移/压力（$u/p$）二场与位移/压力/偏应变（$u/p/e$）三场有限元格式，并阐明了亚格子尺度方法；在第 3 节中，通过对极化张量（Polarization tensor）进行体积—偏量分解，定义了一种新型拓扑导数表达式；在第 4 节中，给出了所提出的迭代拓扑优化算法；在第 5 节中，展示并讨论了若干数值算例，以评估该算法并验证其在近不可压缩和完全不可压缩材料中的性能；最后，在第 6 节中得出了关于所提拓扑优化格式的相关结论。

---

# 2 线弹性力学中的混合有限元格式 (Mixed Formulations in Linear Elasticity)

## 2.1 连续介质问题描述 (The continuum problem statement)

在本工作中，运动方程在无穷小应变假设下给出。设 $\Omega$ 为 $\mathbb{R}^d$ 中的开有界多面体域，其中 $d$ 为空间维数。物体内的任意点用位置矢量 $\boldsymbol{x}$ 标记。域的边界记为 $\Gamma := \partial\Omega$，它被划分为给定指定位移的 Dirichlet 边界 $\Gamma_D$ 与施加给定面力的 Neumann 边界 $\Gamma_N$。这两类边界互不相交，即 $\Gamma_D \cap \Gamma_N = \emptyset$，且共同覆盖整个边界，$\Gamma_D \cup \Gamma_N = \Gamma$。

线弹性连续介质力学问题由以下方程组定义：

$$
-\nabla \cdot \boldsymbol{\sigma} = \rho \boldsymbol{b} \quad \text{在 } \Omega \text{ 内},
\tag{1}
$$

$$
\boldsymbol{\sigma} = \mathbb{C} : \boldsymbol{\varepsilon} \quad \text{在 } \Omega \text{ 内},
\tag{2}
$$

$$
\boldsymbol{\varepsilon} = \nabla^s \boldsymbol{u} \quad \text{在 } \Omega \text{ 内},
\tag{3}
$$

其中 $\boldsymbol{u}$ 为位移场，$\boldsymbol{\sigma}$ 为应力张量场，$\boldsymbol{\varepsilon}$ 为应变张量场。式 (1) 为动量平衡方程，其中 $\rho \boldsymbol{b}$ 表示单位体积的外载荷（体力密度），$\nabla \cdot (\cdot)$ 为散度算子。式 (2) 为线弹性本构方程，其中 $\mathbb{C}$ 为各向同性材料的四阶弹性本构张量，定义为：

$$
\mathbb{C} = 2\mu \mathbb{I} + \lambda \boldsymbol{I} \otimes \boldsymbol{I}.
\tag{4}
$$

这里，$\mathbb{I}$ 与 $\boldsymbol{I}$ 分别表示四阶与二阶单位张量，$\lambda$ 和 $\mu$ 为 Lamé 参数。在平面应力（plane stress）假设下，它们表示为：

$$
\lambda = \frac{\nu E}{1 - \nu^2}, \quad \mu = \frac{E}{2(1 + \nu)},
\tag{5}
$$

而在三维（3D）和平面应变（plane strain）假设下，它们定义为：

$$
\lambda = \frac{\nu E}{(1 + \nu)(1 - 2\nu)}, \quad \mu = \frac{E}{2(1 + \nu)}.
\tag{6}
$$

此处 $E$ 为 Young 模量，$\nu$ 为 Poisson 比。最后，式 (3) 为将应变场与位移场联系起来的几何方程（运动学方程），其中 $\nabla^s (\cdot) = \frac{1}{2}\left[\nabla(\cdot) + \nabla^T(\cdot)\right]$ 表示对称梯度算子，$\nabla(\cdot)$ 为常规梯度算子。

将式 (2)–(3) 代入式 (1)，即可获得经典的不可约位移有限元格式。其结果即为著名的 Navier 方程：

$$
-\nabla \cdot \{\mathbb{C} : \nabla^s \boldsymbol{u}\} = \rho \boldsymbol{b} \quad \text{在 } \Omega \text{ 内},
\tag{7}
$$

该方程仅用位移场 $\boldsymbol{u}$ 单独表达。

## 2.2 体积/偏量分解 (The volumetric/deviatoric split)

本小节的目标是将本构方程和几何方程均分解为其体积部分（球偏部分）与偏量部分。体积/偏量分解是发展能够处理不可压缩极限格式的出发点。

### 2.2.1 体积与偏量算子 (Volumetric and deviatoric operators)

首先，定义四阶体积投影张量 $\mathbb{V}$ 与四阶偏量投影张量 $\mathbb{D}$ 为：

$$
\mathbb{V} = \frac{1}{3} \boldsymbol{I} \otimes \boldsymbol{I},
\tag{8}
$$

$$
\mathbb{D} = \mathbb{I} - \frac{1}{3} \boldsymbol{I} \otimes \boldsymbol{I},
\tag{9}
$$

$$
\mathbb{I} = \mathbb{D} + \mathbb{V}.
\tag{10}
$$

利用算子 $\mathbb{V}$ 与 $\mathbb{D}$，可以提取通用二阶和四阶张量的球偏部分与偏量部分。

### 2.2.2 应力与应变张量分解 (Split of stress and strain tensors)

特别地，当作用于对称柯西应力张量 $\boldsymbol{\sigma}$ 时，其结果为：

$$
\mathbb{V} : \boldsymbol{\sigma} = \left(\frac{1}{3} \boldsymbol{I} \otimes \boldsymbol{I}\right) : \boldsymbol{\sigma} = \frac{1}{3} \operatorname{tr}(\boldsymbol{\sigma})\boldsymbol{I} := -p\boldsymbol{I},
\tag{11}
$$

其中 $p$ 为静水压力（在受压状态下取为正值），以及

$$
\mathbb{D} : \boldsymbol{\sigma} = \left(\mathbb{I} - \frac{1}{3} \boldsymbol{I} \otimes \boldsymbol{I}\right) : \boldsymbol{\sigma} = \boldsymbol{\sigma} + p\boldsymbol{I} = \boldsymbol{s},
\tag{12}
$$

其中 $\boldsymbol{s}$ 为偏应力张量。将体积与偏量分量相加，柯西应力张量重构为：

$$
\boldsymbol{\sigma} = \boldsymbol{s} - p\boldsymbol{I}.
\tag{13}
$$

类似地，可以将应变张量 $\boldsymbol{\varepsilon}$ 分解为：

$$
\mathbb{V} : \boldsymbol{\varepsilon} = \left(\frac{1}{3} \boldsymbol{I} \otimes \boldsymbol{I}\right) : \boldsymbol{\varepsilon} = \frac{1}{3}\operatorname{tr}(\boldsymbol{\varepsilon})\boldsymbol{I} := \frac{1}{3} e_{\mathrm{vol}} \boldsymbol{I},
\tag{14}
$$

其中 $e_{\mathrm{vol}}$ 为体积应变，以及

$$
\mathbb{D} : \boldsymbol{\varepsilon} = \left(\mathbb{I} - \frac{1}{3} \boldsymbol{I} \otimes \boldsymbol{I}\right) : \boldsymbol{\varepsilon} = \boldsymbol{\varepsilon} - \frac{1}{3} e_{\mathrm{vol}} \boldsymbol{I} = \boldsymbol{e},
\tag{15}
$$

其中 $\boldsymbol{e}$ 为代表形状畸变（剪切畸变）的偏应变张量。

### 2.2.3 几何方程分解 (Split of the kinematic equation)

应用体积与偏量算子，几何方程 (3) 可分解为：

$$
e_{\mathrm{vol}} = \nabla \cdot \boldsymbol{u},
\tag{16}
$$

$$
\boldsymbol{e} = \mathbb{D} : \nabla^s \boldsymbol{u}.
\tag{17}
$$

将体积与偏量分量相加，几何方程重新表达为：

$$
\boldsymbol{\varepsilon} = \frac{1}{3} e_{\mathrm{vol}} \boldsymbol{I} + \boldsymbol{e} = \frac{1}{3}(\nabla \cdot \boldsymbol{u})\boldsymbol{I} + \mathbb{D} : \nabla^s \boldsymbol{u}.
\tag{18}
$$

### 2.2.4 本构方程分解 (Split of the constitutive equation)

假定应力与应变之间的本构关系可由本构方程 (2) 表达。因此，弹性本构张量 $\mathbb{C}$ 的体积部分 $\mathbb{C}_{\mathrm{vol}}$ 与偏量部分 $\mathbb{C}_{\mathrm{dev}}$ 分别为：

$$
\mathbb{C}_{\mathrm{vol}} = \mathbb{V} : \mathbb{C} = \left(\lambda + \frac{2\mu}{3}\right)\boldsymbol{I} \otimes \boldsymbol{I} := \kappa \boldsymbol{I} \otimes \boldsymbol{I},
\tag{19}
$$

$$
\mathbb{C}_{\mathrm{dev}} = \mathbb{D} : \mathbb{C} = 2\mu\left(\mathbb{I} - \frac{1}{3}\boldsymbol{I} \otimes \boldsymbol{I}\right),
\tag{20}
$$

$$
\mathbb{C} = \mathbb{C}_{\mathrm{vol}} + \mathbb{C}_{\mathrm{dev}},
\tag{21}
$$

其中 $\kappa$ 为材料的体积模量（bulk modulus）。引入应力与应变的分解后，式 (2) 的本构关系可写作：

$$
\{\boldsymbol{s} - p\boldsymbol{I}\} = \left(\mathbb{C}_{\mathrm{vol}} + \mathbb{C}_{\mathrm{dev}}\right) : \left\{\frac{1}{3}(\nabla \cdot \boldsymbol{u})\boldsymbol{I} + \mathbb{D} : \nabla^s \boldsymbol{u}\right\}.
\tag{22}
$$

考虑到体积张量与偏量张量之间的缩并恒等于零，式 (22) 可严格解耦为两个独立的本构方程：

$$
p = -\kappa \nabla \cdot \boldsymbol{u},
\tag{23}
$$

$$
\boldsymbol{s} = \mathbb{C}_{\mathrm{dev}} : \boldsymbol{\varepsilon} = \mathbb{C}_{\mathrm{dev}} : \boldsymbol{e},
\tag{24}
$$

它们分别是原始本构方程的体积对偶与偏量对偶部分。

---

## 2.3 u/p 双场混合格式 (The u/p two-field formulation)

为了处理近不可压缩和完全不可压缩工况，引入著名的混合 $u/p$ 格式。在该格式中，位移场 $\boldsymbol{u}$ 和压力场 $p$ 被选为独立变量。因此，问题的控制方程重写为：

$$
-\nabla \cdot \boldsymbol{s} + \nabla p = \rho \boldsymbol{b} \quad \text{在 } \Omega \text{ 内},
\tag{25}
$$

$$
\boldsymbol{s} = \mathbb{C}_{\mathrm{dev}} : \nabla^s \boldsymbol{u} \quad \text{在 } \Omega \text{ 内},
\tag{26}
$$

$$
\nabla \cdot \boldsymbol{u} + \frac{p}{\kappa} = 0 \quad \text{在 } \Omega \text{ 内}.
\tag{27}
$$

式 (25) 允许我们同时用位移 $\boldsymbol{u}$ 和压力 $p$ 来表述线动量平衡方程，其中应力张量分解式 (13) 已代入动量方程中。此外，联系偏应力与位移的本构律 (26) 允许我们将位移场引入平衡方程 (25)。最后，式 (27) 既充当压力的本构方程，又施加了不可压缩约束。

> **注 2.1**：注意到在完全不可压缩极限下，$\kappa \to \infty$，式 (27) 自动退化为：
> $$
> \nabla \cdot \boldsymbol{u} = 0,
> \tag{28}
> $$
> 这正是无穷小应变理论下的经典不可压缩条件。

### 2.3.1 控制方程 (Governing equations)

将式 (26) 代入式 (25)，混合 $u/p$ 问题转化为寻找位移 $\boldsymbol{u}$ 和压力 $p$ 满足：

$$
-\nabla \cdot \left\{\mathbb{C}_{\mathrm{dev}} : \nabla^s \boldsymbol{u}\right\} + \nabla p = \rho \boldsymbol{b} \quad \text{在 } \Omega \text{ 内},
\tag{29}
$$

$$
\nabla \cdot \boldsymbol{u} + \frac{p}{\kappa} = 0 \quad \text{在 } \Omega \text{ 内}.
\tag{30}
$$

上述控制方程必须附带一组边界条件：

$$
\boldsymbol{u} = \boldsymbol{u}_D \quad \text{在 } \Gamma_D \text{ 上},
\tag{31}
$$

$$
\boldsymbol{\sigma}\boldsymbol{n} = \boldsymbol{s}\boldsymbol{n} - p\boldsymbol{n} = \boldsymbol{t} \quad \text{在 } \Gamma_N \text{ 上},
\tag{32}
$$

其中 $\boldsymbol{n}$ 为边界 $\Gamma$ 上的外法向单位几何矢量。为了简化后续表述，以下均假定齐次 Dirichlet 条件 $\boldsymbol{u}_D = \boldsymbol{0}$。

### 2.3.2 变分形式 (Variational Form of the problem)

我们用符号 $(\cdot, \cdot)_\omega$ 表示在域 $\omega$ 上的 $L^2(\omega)$ 内积，用 $\langle\cdot, \cdot\rangle_\omega$ 表示两个函数在域 $\omega$ 上的乘积积分（不必在 $L^2(\omega)$ 内）。当 $\omega = \Omega$ 时省略下标。

设 $\mathcal{V} = [H^1(\Omega)]^d$ 与 $\mathcal{Q} = L^2(\Omega)$ 分别为位移解与压力解良定的合适函数空间。记 $\mathcal{V}_0$ 为在 Dirichlet 边界 $\Gamma_D$ 上消失的 $\mathcal{V}$ 中的函数子空间。我们关注的乘积空间为 $\mathcal{W} := \mathcal{V} \times \mathcal{Q}$，$\mathcal{W}_0 := \mathcal{V}_0 \times \mathcal{Q}$。

通过针对任意测试函数 $\boldsymbol{V} := [\boldsymbol{v}, q]^T$（$\boldsymbol{v} \in \mathcal{V}_0, q \in \mathcal{Q}$）对式 (29)–(30) 进行加权测试，推导问题的变分形式。弱形式表述为：寻找 $\boldsymbol{U} := [\boldsymbol{u}, p] \in \mathcal{W}_0$，使得满足初始/边界条件且

$$
A(\boldsymbol{U}, \boldsymbol{V}) = F(\boldsymbol{V}) \quad \forall \boldsymbol{V} \in \mathcal{W}_0,
\tag{33}
$$

其中 $A(\boldsymbol{U}, \boldsymbol{V})$ 为定义在 $\mathcal{W}_0 \times \mathcal{W}_0$ 上的双线性型：

$$
A(\boldsymbol{U}, \boldsymbol{V}) := \left(\nabla^s \boldsymbol{v}, \mathbb{C}_{\mathrm{dev}} : \nabla^s \boldsymbol{u}\right) - (\nabla \cdot \boldsymbol{v}, p) + (q, \nabla \cdot \boldsymbol{u}) + \left(q, \frac{1}{\kappa} p\right),
\tag{34}
$$

$F(\boldsymbol{V})$ 为定义在 $\mathcal{W}_0$ 上的线性型：

$$
F(\boldsymbol{V}) := \langle\boldsymbol{v}, \rho\boldsymbol{b}\rangle + \langle\boldsymbol{v}, \boldsymbol{t}\rangle_{\Gamma_N}.
\tag{35}
$$

### 2.3.3 Galerkin 空间离散 (Galerkin Spatial Discretization)

构造协调有限元空间 $\mathcal{V}_h \subset \mathcal{V}$ 与 $\mathcal{Q}_h \subset \mathcal{Q}$，并令 $\mathcal{W}_h = \mathcal{V}_h \times \mathcal{Q}_h$ 及 $\mathcal{W}_{h,0} = \mathcal{V}_{h,0} \times \mathcal{Q}_h$。问题 (33) 的标准 Galerkin 离散版本为：寻找 $\boldsymbol{U}_h \in \mathcal{W}_{h,0}$ 使得

$$
A(\boldsymbol{U}_h, \boldsymbol{V}_h) = F(\boldsymbol{V}_h) \quad \forall \boldsymbol{V}_h \in \mathcal{W}_{h,0}.
\tag{36}
$$

众所周知，该离散问题要求插值空间之间满足离散 inf-sup（Babuška–Brezzi）稳定性条件。对于标准的等阶插值（例如位移和压力均采用连续线性 $P_1$ 单元），该条件不满足，会导致严重的数值压力振荡与自锁。

> **注 2.2**：观察双线性型 $A(\cdot, \cdot)$ 可以发现，涉及 $q$ 与 $p$ 的唯一项是 $\left(q, \frac{1}{\kappa}p\right)$。因此，在近不可压缩和完全不可压缩极限下（$\kappa \to \infty$），该项消失，双线性型呈现典型的鞍点结构。

### 2.3.4 稳定化 u/p 有限元格式 (Stabilized u/p finite element formulation)

为了消除不稳定性并允许使用等阶插值，本文采用基于变分多尺度（Variational Multiscale, VMS）概念的稳定化方法 [22, 32]。令 $\mathcal{W} = \mathcal{W}_h \oplus \widetilde{\mathcal{W}}$，其中 $\widetilde{\mathcal{W}}$ 为在 $\mathcal{W}$ 中补全 $\mathcal{W}_h$ 的无限维空间，在计算中将用有限维空间来近似。该空间的元素记为 $\widetilde{\boldsymbol{U}} \equiv [\tilde{\boldsymbol{u}}, \tilde{p}]^T$，称为**亚格子尺度**（subscales）。类似地，$\mathcal{W}_0 = \mathcal{W}_{h,0} \oplus \widetilde{\mathcal{W}}_0$。

由于 $A(\cdot, \cdot)$ 为双线性型，连续问题 (33) 等价于寻找 $\boldsymbol{U}_h \in \mathcal{W}_{h,0}$ 与 $\widetilde{\boldsymbol{U}} \in \widetilde{\mathcal{W}}_0$ 使得：

$$
A(\boldsymbol{U}_h, \boldsymbol{V}_h) + A(\widetilde{\boldsymbol{U}}, \boldsymbol{V}_h) = F(\boldsymbol{V}_h) \quad \forall \boldsymbol{V}_h \in \mathcal{W}_{h,0},
\tag{37}
$$

$$
A(\boldsymbol{U}_h, \widetilde{\boldsymbol{V}}) + A(\widetilde{\boldsymbol{U}}, \widetilde{\boldsymbol{V}}) = F(\widetilde{\boldsymbol{V}}) \quad \forall \widetilde{\boldsymbol{V}} \in \widetilde{\mathcal{W}}_0,
\tag{38}
$$

其中式 (37) 称为**有限元尺度方程**，式 (38) 称为**亚格子尺度方程**。

从 VMS 导出的稳定化方法的核心思想在于：利用亚格子尺度方程 (38) 求解亚格子尺度的近似表达式，并将其回代到有限元尺度方程 (37) 中，从而补充稳定化项并保持一致性。假定亚格子尺度在单元边界消失（气泡函数性质），亚格子尺度可由投影方程的残差近似表示为：

$$
\tilde{\boldsymbol{u}} \approx \tau_u \widetilde{\Pi}\left(\nabla \cdot \boldsymbol{s}_h - \nabla p_h - \rho\boldsymbol{b}\right),
\tag{39}
$$

$$
\tilde{p} \approx \tau_p \widetilde{\Pi}\left(-\nabla \cdot \boldsymbol{u}_h - \frac{1}{\kappa} p_h\right),
\tag{40}
$$

其中 $\widetilde{\Pi}$ 为向亚格子尺度空间的 $L^2$ 投影算子，$\tau_u$ 与 $\tau_p$ 为稳定化参数，来自对亚格子尺度方程的 Fourier 分析。在线弹性力学中，采用文献 [17] 提出的参数：

$$
\tau_u = c_1 \frac{h^2_K}{2\mu}, \quad \tau_p = 2c_2 \left(\frac{1}{\mu} + \frac{2}{3\kappa}\right)^{-1},
\tag{41}
$$

其中 $h_K$ 为单元特征尺寸，$c_1$ 与 $c_2$ 为待定算法常数。

将近似场 (39)–(40) 代入有限元尺度方程 (37)，获得 $u/p$ 问题的 VMS 稳定化有限元格式：

$$
A(\boldsymbol{U}_h, \boldsymbol{V}_h) + \sum_{K} \tau_u \left\langle -\nabla q_h, \widetilde{\Pi}\left(\nabla \cdot \boldsymbol{s}_h - \nabla p_h - \rho\boldsymbol{b}\right) \right\rangle_K + \sum_{K} \tau_p \left\langle -\nabla \cdot \boldsymbol{v} + \frac{1}{\kappa} q_h, \widetilde{\Pi}\left(-\nabla \cdot \boldsymbol{u}_h - \frac{1}{\kappa} p_h\right) \right\rangle_K = F(\boldsymbol{V}_h) \quad \forall \boldsymbol{V}_h \in \mathcal{W}_{h,0}.
\tag{42}
$$

根据对投影算子 $\widetilde{\Pi}$ 的不同选取，产生不同的稳定化格式：
1. **代数亚格子尺度（ASGS）**：将投影算子直接取为恒等映射 $\widetilde{\Pi} = \mathbb{I}$ [14]；
2. **正交亚格子尺度（OSS）**：将亚格子空间取为与有限元空间正交，即 $\widetilde{\Pi} = \mathbb{I} - \Pi_h$ [34]。

> **注 2.3**：OSS 稳定化的一大关键特性在于，由于正交投影的存在，即使仅包含最少数量的稳定化项，格式在弱意义下依然保持一致性（consistent）。在本格式中，稳定化项可精简为仅保留 $\sum_K \tau_u \langle \nabla q_h, \widetilde{\Pi}(\nabla p_h) \rangle_K$。

---

## 2.4 u/p/e 三场混合格式 (The u/p/e three-field formulation)

为了在求解不可压缩力学问题的同时大幅提高应变场和应力场的计算精度，引入三场混合格式 [23, 35, 36]。位移场 $\boldsymbol{u}$、压力场 $p$ 以及偏应变张量 $\boldsymbol{e}$ 同时作为主未知量。问题的控制方程重写为：

$$
-\nabla \cdot \boldsymbol{s} + \nabla p = \rho \boldsymbol{b} \quad \text{在 } \Omega \text{ 内},
\tag{43}
$$

$$
\boldsymbol{s} = \mathbb{C}_{\mathrm{dev}} : \boldsymbol{e} \quad \text{在 } \Omega \text{ 内},
\tag{44}
$$

$$
\nabla \cdot \boldsymbol{u} + \frac{p}{\kappa} = 0 \quad \text{在 } \Omega \text{ 内},
\tag{45}
$$

$$
\boldsymbol{e} = \mathbb{D} : \nabla^s \boldsymbol{u} \quad \text{在 } \Omega \text{ 内}.
\tag{46}
$$

> **注 2.4**：注意式 (44) 允许直接由偏应变 $\boldsymbol{e}$ 计算偏应力，而无需通过位移梯度的数值微分获得。因此，应力张量 $\boldsymbol{\sigma} = \mathbb{C}_{\mathrm{dev}} : \boldsymbol{e} - p\boldsymbol{I}$ 的计算精度得到了质的飞跃。

### 2.4.1 控制方程 (Governing equations)

将式 (44) 代入动量方程，并将几何方程 (46) 两边与 $\mathbb{C}_{\mathrm{dev}}$ 缩并以使系统对称化，得到三场混合控制方程组：

$$
-\nabla \cdot \left\{\mathbb{C}_{\mathrm{dev}} : \boldsymbol{e}\right\} + \nabla p = \rho \boldsymbol{b} \quad \text{在 } \Omega \text{ 内},
\tag{47}
$$

$$
\nabla \cdot \boldsymbol{u} + \frac{p}{\kappa} = 0 \quad \text{在 } \Omega \text{ 内},
\tag{48}
$$

$$
\mathbb{C}_{\mathrm{dev}} : \boldsymbol{e} - \mathbb{C}_{\mathrm{dev}} : \nabla^s \boldsymbol{u} = \boldsymbol{0} \quad \text{在 } \Omega \text{ 内}.
\tag{49}
$$

伴随边界条件：

$$
\boldsymbol{u} = \boldsymbol{0} \quad \text{在 } \Gamma_D \text{ 上},
\tag{50}
$$

$$
\boldsymbol{\sigma}\boldsymbol{n} = \left(\mathbb{C}_{\mathrm{dev}} : \boldsymbol{e}\right)\boldsymbol{n} - p\boldsymbol{n} = \boldsymbol{t} \quad \text{在 } \Gamma_N \text{ 上}.
\tag{51}
$$

### 2.4.2 变分形式 (Variational Form of the problem)

在数值实现中，采用 Voigt 记号将对称二阶张量转换为矢量（二维下 3 维，三维下 6 维）。设 $\mathcal{E} = [L^2(\Omega)]^v$ 为偏应变分量所在的良定函数空间。定义全空间 $\mathcal{W}_0 := \mathcal{V}_0 \times \mathcal{Q} \times \mathcal{E}$。

针对任意测试函数 $\boldsymbol{V} := [\boldsymbol{v}, q, \boldsymbol{f}]^T \in \mathcal{W}_0$，问题的弱形式为：寻找 $\boldsymbol{U} := [\boldsymbol{u}, p, \boldsymbol{e}]^T \in \mathcal{W}_0$ 使得

$$
A(\boldsymbol{U}, \boldsymbol{V}) = F(\boldsymbol{V}) \quad \forall \boldsymbol{V} \in \mathcal{W}_0,
\tag{52}
$$

其中双线性型为：

$$
A(\boldsymbol{U}, \boldsymbol{V}) := \left(\nabla^s \boldsymbol{v}, \mathbb{C}_{\mathrm{dev}} : \boldsymbol{e}\right) - (\nabla \cdot \boldsymbol{v}, p) + (q, \nabla \cdot \boldsymbol{u}) + \left(q, \frac{1}{\kappa} p\right) - \left(\mathbb{C}_{\mathrm{dev}} : \boldsymbol{f}, \nabla^s \boldsymbol{u}\right) + \left(\boldsymbol{f}, \mathbb{C}_{\mathrm{dev}} : \boldsymbol{e}\right),
\tag{53}
$$

线性型为：

$$
F(\boldsymbol{V}) := \langle\boldsymbol{v}, \rho\boldsymbol{b}\rangle + \langle\boldsymbol{v}, \boldsymbol{t}\rangle_{\Gamma_N}.
\tag{54}
$$

### 2.4.3 Galerkin 空间离散 (Galerkin Spatial Discretization)

引入协调有限元子空间 $\mathcal{E}_h \subset \mathcal{E}$，并定义 $\mathcal{W}_{h,0} = \mathcal{V}_{h,0} \times \mathcal{Q}_h \times \mathcal{E}_h$。离散问题为：寻找 $\boldsymbol{U}_h \in \mathcal{W}_{h,0}$ 使得

$$
A(\boldsymbol{U}_h, \boldsymbol{V}_h) = F(\boldsymbol{V}_h) \quad \forall \boldsymbol{V}_h \in \mathcal{W}_{h,0}.
\tag{55}
$$

同样地，当各场采用同阶多项式（如全 $P_1$ 连续线性单元）时，必须引入稳定化机制。

### 2.4.4 稳定化 u/p/e 有限元格式 (Stabilized u/p/e finite element formulation)

令亚格子尺度为 $\widetilde{\boldsymbol{U}} \equiv [\tilde{\boldsymbol{u}}, \tilde{p}, \tilde{\boldsymbol{e}}]^T$。系统裂解为两组方程：

$$
A(\boldsymbol{U}_h, \boldsymbol{V}_h) + A(\widetilde{\boldsymbol{U}}, \boldsymbol{V}_h) = F(\boldsymbol{V}_h) \quad \forall \boldsymbol{V}_h \in \mathcal{W}_{h,0},
\tag{56}
$$

$$
A(\boldsymbol{U}_h, \widetilde{\boldsymbol{V}}) + A(\widetilde{\boldsymbol{U}}, \widetilde{\boldsymbol{V}}) = F(\widetilde{\boldsymbol{V}}) \quad \forall \widetilde{\boldsymbol{V}} \in \widetilde{\mathcal{W}}_0.
\tag{57}
$$

亚格子尺度近似表示为残差投影：

$$
\tilde{\boldsymbol{u}} \approx \tau_u \widetilde{\Pi}\left(\nabla \cdot (\mathbb{C}_{\mathrm{dev}} : \boldsymbol{e}_h) - \nabla p_h - \rho\boldsymbol{b}\right),
\tag{58}
$$

$$
\tilde{p} \approx \tau_p \widetilde{\Pi}\left(-\nabla \cdot \boldsymbol{u}_h - \frac{1}{\kappa} p_h\right),
\tag{59}
$$

$$
\tilde{\boldsymbol{e}} \approx \tau_e \widetilde{\Pi}\left(\mathbb{D} : \nabla^s \boldsymbol{u}_h - \boldsymbol{e}_h\right),
\tag{60}
$$

其中 $\tau_e$ 参数取自文献 [17]：

$$
\tau_e = c_3,
\tag{61}
$$

$c_3$ 为无量纲算法常数。将上述亚格子场代入式 (56)，得到 $u/p/e$ 的 VMS 稳定化有限元格式：

$$
\begin{aligned}
A(\boldsymbol{U}_h, \boldsymbol{V}_h) &+ \sum_{K} \tau_u \left\langle \nabla \cdot (\mathbb{C}_{\mathrm{dev}} : \boldsymbol{f}) - \nabla q_h, \widetilde{\Pi}\left(\nabla \cdot \boldsymbol{s}_h - \nabla p_h - \rho\boldsymbol{b}\right) \right\rangle_K \\
&+ \sum_{K} \tau_p \left\langle -\nabla \cdot \boldsymbol{v} + \frac{1}{\kappa} q_h, \widetilde{\Pi}\left(-\nabla \cdot \boldsymbol{u}_h - \frac{1}{\kappa} p_h\right) \right\rangle_K \\
&+ \sum_{K} \tau_e \left\langle \mathbb{C}_{\mathrm{dev}} : \nabla^s \boldsymbol{v} + \mathbb{C} : \boldsymbol{f}, \widetilde{\Pi}\left(\mathbb{D} : \nabla^s \boldsymbol{u}_h - \boldsymbol{e}_h\right) \right\rangle_K = F(\boldsymbol{V}_h) \quad \forall \boldsymbol{V}_h \in \mathcal{W}_{h,0}.
\end{aligned}
\tag{62}
$$

> **注 2.5**：在 OSS 变体下，稳定化项可精简为仅在 $q/p$ 分量上保留 $\sum_K \tau_u \langle \nabla q_h, \widetilde{\Pi}(\nabla p_h) \rangle_K$，在 $\boldsymbol{v}/\boldsymbol{u}$ 分量上保留 $\sum_K \tau_e \langle \mathbb{C}_{\mathrm{dev}} : \nabla^s \boldsymbol{v}, \widetilde{\Pi}(\mathbb{D} : \nabla^s \boldsymbol{u}_h) \rangle_K$。

---

# 3 面向不可压缩材料的拓扑导数拓扑优化 (Topological Derivative-Based Topology Optimization for Nearly and Fully Incompressible Materials)

## 3.1 问题设定 (Setting of the problem)

在小应变线弹性力学框架下，结构的几何构型由示性函数（characteristic function）$\chi(\boldsymbol{x})$ 表征：

$$
\chi(\boldsymbol{x}) = \begin{cases}
1, & \boldsymbol{x} \in \Omega_s, \\
0, & \boldsymbol{x} \in \Omega_w,
\end{cases}
\tag{63}
$$

其中设计域被划分为实体强相区 $\Omega_s$ 与弱相区 $\Omega_w$（$\Omega = \Omega_s \cup \Omega_w, \Omega_s \cap \Omega_w = \emptyset$）。$\Omega_w$ 赋予极小的刚度以模拟空洞。强相材料参数记为 $E_s$ 和 $\nu_s$，弱相材料参数记为 $E_w = \gamma E_s$ 与 $\nu_w$，其中 $\gamma > 0$ 为刚度跳跃比（小到足以模拟空洞，大到保证全局刚度矩阵正定可逆）。全域偏量本构张量表示为：

$$
\mathbb{C}_{\mathrm{dev}}(\chi) = \chi \mathbb{C}_{\mathrm{dev}}^s + (1 - \chi) \mathbb{C}_{\mathrm{dev}}^w.
\tag{64}
$$

为了寻求刚度最大的结构，最小化柔顺度泛函（compliance functional）：

$$
J(\chi) = \int_{\Omega} \boldsymbol{\sigma}(\chi, \boldsymbol{x}) : \boldsymbol{\varepsilon}(\chi, \boldsymbol{x}) \,\mathrm{d}\Omega.
\tag{65}
$$

完整的拓扑优化数学模型表示为：

$$
\begin{aligned}
\min_{\chi \in \mathcal{X}_L} \quad & J(\chi) = \int_{\Omega} \boldsymbol{\sigma}(\chi, \boldsymbol{x}) : \boldsymbol{\varepsilon}(\chi, \boldsymbol{x}) \,\mathrm{d}\Omega \\
\text{s.t.} \quad & A(\boldsymbol{U}, \boldsymbol{V}) = F(\boldsymbol{V}) \quad \forall \boldsymbol{V} \in \mathcal{W}_0, \\
& \mathcal{X}_L = \left\{ \chi \in L^\infty(\Omega, \{0, 1\}) \;\middle|\; \int_{\Omega} \chi(\boldsymbol{x}) \,\mathrm{d}\Omega = L|\Omega| \right\},
\end{aligned}
\tag{66}
$$

其中 $L \in (0, 1)$ 为体积上限比例，$A(\cdot, \cdot)$ 与 $F(\cdot)$ 为第 2 节推导的 $u/p$ 或 $u/p/e$ 双线性型与线性型。

## 3.2 材料插值 (Material Interpolation)

在传统的双材料拓扑导数方法中，通常假定两相材料具有相同的泊松比 $\nu = \nu_s = \nu_w$，仅对杨氏模量进行调整。对于可压缩材料，这种做法保证了弱材料对结构刚度没有明显贡献。**然而，当处理不可压缩介质（$\nu_s \to 0.5$）时，若令 $\nu_w = \nu_s = 0.5$，弱材料区域的“气泡”在体积变形下依然呈现无穷大的体积刚度，导致大范围的弱材料能够直接传递静水压力，产生严重的伪构型！**

为避免这种数值伪构型，**弱相材料必须强制设为可压缩介质**，即保证 $\nu_w < 0.5$（算例中通常取 $\nu_w = 0.4$）。

> **注 3.1**：在相交界面单元中，材料性质对应于两相体积比复合材料，必须遵循 Hashin–Shtrikman 物理界限约束 [38]。

## 3.3 基于拓扑导数概念的拓扑优化 (Topology optimization using the topological derivative concept)

拓扑导数度量了在域内某一点引入无穷小夹杂时目标泛函的灵敏度。在点 $\boldsymbol{x}$ 处泛函 $J(\chi)$ 的拓扑导数 $D_T J$ 形式上计算为 [30]：

$$
D_T J(\chi, \boldsymbol{x}) = \boldsymbol{\varepsilon}(\chi, \boldsymbol{x}) : \mathbb{P} : \boldsymbol{\sigma}(\chi, \boldsymbol{x}) + (1 - \gamma)\boldsymbol{b} \cdot \boldsymbol{u}(\chi, \boldsymbol{x}),
\tag{67}
$$

其中 $\mathbb{P}$ 为四阶 Pólya–Szegö 极化张量（Polarization tensor）。根据文献 [39]，极化张量定义为：

$$
\mathbb{P} = \Delta\mathbb{C} : \left[\mathbb{C}_e^{-1} + \Delta\mathbb{C} : \mathbb{T}\right]^{-1},
\tag{68}
$$

其中 $\mathbb{C}_i$ 为夹杂材料张量，$\mathbb{C}_e$ 为基体材料张量，$\Delta\mathbb{C} := \mathbb{C}_i - \mathbb{C}_e$，$\mathbb{T}$ 为四阶 Eshelby 各向同性张量 [40, 41]。

在**平面应变**假设下，极化张量解析展开为：

$$
\mathbb{P} = -\frac{1}{2}(1 + \beta)\left\{ \frac{\tau_1 - \gamma}{\beta\gamma + \tau_1}\mathbb{I} - \frac{1}{4}\left[\frac{\alpha(\gamma - \tau_1\tau_2)}{\alpha\gamma + \tau_1\tau_2} + \frac{2(\tau_1 - \gamma)}{\beta\gamma + \tau_1}\right]\boldsymbol{I}\otimes\boldsymbol{I} \right\},
\tag{69}
$$

其中辅助参数为：

$$
\alpha(\nu_e) = \frac{1}{1 - 2\nu_e}, \quad \beta(\nu_e) = 3 - 4\nu_e, \quad \tau_1 = \frac{1 + \nu_i}{1 + \nu_e}, \quad \tau_2 = \frac{1 - 2\nu_i}{1 - 2\nu_e}.
\tag{70}
$$

在**平面应力**假设下，极化张量解析展开为：

$$
\mathbb{P} = -\frac{1}{2}(1 + \beta)\left\{ \frac{\tau_1 - \gamma}{\beta\gamma + \tau_1}\mathbb{I} - \frac{1}{4}\left[\frac{\gamma(\alpha + \tau_2 - 1) - \alpha\tau_1\tau_2}{\tau_1(\alpha\gamma + \tau_2)} + \frac{2(\tau_1 - \gamma)}{\beta\gamma + \tau_1}\right]\boldsymbol{I}\otimes\boldsymbol{I} \right\},
\tag{71}
$$

其中：

$$
\alpha(\nu_e) = \frac{1 + \nu_e}{1 - \nu_e}, \quad \beta(\nu_e) = \frac{3 - \nu_e}{1 + \nu_e}, \quad \tau_1 = \frac{1 + \nu_i}{1 + \nu_e}, \quad \tau_2 = \frac{1 - \nu_i}{1 - \nu_e}.
\tag{72}
$$

在上述公式中，$\gamma = E_w / E_s$，$\nu_e$ 与 $\nu_i$ 分别表示基体与夹杂材料的泊松比。

> **注 3.2**：若两相泊松比相同（$\nu_e = \nu_i$），则式 (69) 与 (71) 简化为结构拓扑优化中广为人知的经典形式 [42]：
> $$
> \mathbb{P} = -\frac{1}{2}\frac{1 - \gamma}{1 + \beta\gamma}\left[(1 + \beta)\mathbb{I} + \frac{1}{2}(\alpha - \beta)\frac{1 - \gamma}{1 + \alpha\gamma}\boldsymbol{I}\otimes\boldsymbol{I}\right].
> \tag{73}
> $$

在三维空间中，本文采用二维平面应变各向同性极化张量作为良好逼近（对应于柱状无穷小摄动，数值经验表明其表现完全合格 [7]）。

在域内任意点，存在两种可能的相转变：
1. 在实体区开孔引入弱材料夹杂（$\boldsymbol{x} \in \Omega_s$）：$\mathbb{P}_s := \mathbb{P}(\alpha(\nu_s), \beta(\nu_s), \gamma, \tau_1, \tau_2)$；
2. 在弱材料区添加实体夹杂（$\boldsymbol{x} \in \Omega_w$）：$\mathbb{P}_w := \mathbb{P}(\alpha(\nu_w), \beta(\nu_w), \gamma^{-1}, \tau_1^{-1}, \tau_2^{-1})$。

综合定义为：

$$
\mathbb{P} = \begin{cases}
\mathbb{P}_s, & \boldsymbol{x} \in \Omega_s, \\
\mathbb{P}_w, & \boldsymbol{x} \in \Omega_w.
\end{cases}
\tag{74}
$$

极化张量的物理性质确保了：

$$
D_T J(\chi, \boldsymbol{x}) = \begin{cases}
\boldsymbol{\varepsilon} : \mathbb{P}_s : \boldsymbol{\sigma} + (1 - \gamma)\boldsymbol{b}\cdot\boldsymbol{u} \leq 0, & \forall \boldsymbol{x} \in \Omega_s, \\
\boldsymbol{\varepsilon} : \mathbb{P}_w : \boldsymbol{\sigma} + (1 - \gamma)\boldsymbol{b}\cdot\boldsymbol{u} \geq 0, & \forall \boldsymbol{x} \in \Omega_w.
\end{cases}
\tag{75}
$$

由此定义**带符号拓扑导数**（signed topological derivative）为：

$$
D_T^s J(\chi, \boldsymbol{x}) = \begin{cases}
-D_T J(\chi, \boldsymbol{x}), & \boldsymbol{x} \in \Omega_s, \\
D_T J(\chi, \boldsymbol{x}), & \boldsymbol{x} \in \Omega_w.
\end{cases}
\tag{76}
$$

在最优解处，满足如下最优性条件：

$$
D_T^s J(\chi, \boldsymbol{x}) \geq D_T^s J(\chi, \boldsymbol{y}) \quad \forall \boldsymbol{x} \in \Omega_s, \; \forall \boldsymbol{y} \in \Omega_w.
\tag{77}
$$

带符号拓扑导数在两相界面上保持连续。这允许我们构造一个隐式表征两相分布的**水平集函数**（level-set function）$\psi(\chi, \boldsymbol{x})$：

$$
\psi(\chi, \boldsymbol{x}) = D_T^s J(\chi, \boldsymbol{x}) + \lambda,
\tag{78}
$$

$$
\psi(\chi, \boldsymbol{x}) \begin{cases}
> 0, & \boldsymbol{x} \in \Omega_s, \\
< 0, & \boldsymbol{x} \in \Omega_w,
\end{cases}
\tag{79}
$$

标量 $\lambda \in \mathbb{R}$ 通过精确满足体积约束方程来确定：

$$
\int_{\Omega} H(\psi(\chi, \boldsymbol{x})) \,\mathrm{d}\Omega = L|\Omega|,
\tag{80}
$$

$$
H(\psi) = \begin{cases}
1, & \psi \geq 0, \\
0, & \psi < 0.
\end{cases}
\tag{81}
$$

由此显式建立了示性函数与水平集函数的关系：$\chi = H(\psi)$（式 82）。

> **注 3.3**：在有限元离散下，式 (69) 与 (71) 中的拓扑导数直接依赖于不连续的应力和应变场。为了使水平集函数连续可微并能够稳定更新，必须采用基于有限元空间的节点投影（平滑操作）。

## 3.4 不可压缩极限下的拓扑导数 (Topological derivative in the incompressible limit)

当泊松比趋于极限 $\nu_e \to 0.5$ 时，由式 (70) 可见：$\alpha(\nu_e) = \frac{1}{1 - 2\nu_e} \to \infty$，$\tau_2 = \frac{1 - 2\nu_i}{1 - 2\nu_e} \to \infty$。**经典极化张量产生严重的数学奇异性！**

为了克服这一瓶颈，本文提出对极化张量本身进行体积/偏量分解：

$$
\mathbb{P}_{\mathrm{vol}} = \mathbb{V} : \mathbb{P} = \frac{\alpha(1 + \beta)}{8} \frac{\gamma - \tau_1\tau_2}{\alpha\gamma + \tau_1\tau_2} \boldsymbol{I} \otimes \boldsymbol{I},
\tag{83}
$$

$$
\mathbb{P}_{\mathrm{dev}} = \mathbb{D} : \mathbb{P} = -\frac{1}{2}\frac{(1 + \beta)(\tau_1 - \gamma)}{\tau_1 + \beta\gamma} \left(\mathbb{I} - \frac{1}{3}\boldsymbol{I} \otimes \boldsymbol{I}\right),
\tag{84}
$$

$$
\mathbb{P} = \mathbb{P}_{\mathrm{vol}} + \mathbb{P}_{\mathrm{dev}}.
\tag{85}
$$

利用该分解，式 (67) 中的拓扑导数可严格重写为：

$$
\begin{aligned}
D_T J(\chi, \boldsymbol{x}) &= \boldsymbol{\varepsilon} : \mathbb{P} : \boldsymbol{\sigma} + (1 - \gamma)\boldsymbol{b} \cdot \boldsymbol{u} \\
&= \boldsymbol{\varepsilon} : \left(\mathbb{P}_{\mathrm{vol}} + \mathbb{P}_{\mathrm{dev}}\right) : (\boldsymbol{s} - p\boldsymbol{I}) + (1 - \gamma)\boldsymbol{b} \cdot \boldsymbol{u} \\
&= \boldsymbol{\varepsilon} : \mathbb{P}_{\mathrm{dev}} : \boldsymbol{s} - \boldsymbol{\varepsilon} : \mathbb{P}_{\mathrm{vol}} : (p\boldsymbol{I}) + (1 - \gamma)\boldsymbol{b} \cdot \boldsymbol{u}.
\end{aligned}
\tag{86}
$$

第一项对应偏量效应引起的拓扑导数。利用应变偏量分解 $\boldsymbol{\varepsilon} = \frac{1}{3}e_{\mathrm{vol}}\boldsymbol{I} + \boldsymbol{e}$ 及偏量与球偏缩并正交性，化简为：

$$
\boldsymbol{\varepsilon} : \mathbb{P}_{\mathrm{dev}} : \boldsymbol{s} = \boldsymbol{e}(\chi, \boldsymbol{x}) : \mathbb{P}_{\mathrm{dev}} : \boldsymbol{s}(\chi, \boldsymbol{x}).
\tag{87}
$$

由于 $\mathbb{P}_{\mathrm{dev}}$ 在 $\nu_e \to 0.5$ 时保持有界且仅涉及偏量场，该项彻底消除了奇异性！

第二项对应体积效应引起的拓扑导数。引入静水压力方程 $p = -\kappa \nabla \cdot \boldsymbol{u} = -\kappa e_{\mathrm{vol}}$，变形得到：

$$
\begin{aligned}
-\boldsymbol{\varepsilon} : \mathbb{P}_{\mathrm{vol}} : (p\boldsymbol{I}) &= -e_{\mathrm{vol}} p \left(\boldsymbol{I} : \mathbb{P}_{\mathrm{vol}} : \boldsymbol{I}\right) \\
&= \frac{p^2}{\kappa} \left(\boldsymbol{I} : \mathbb{P}_{\mathrm{vol}} : \boldsymbol{I}\right) \\
&:= P_{\mathrm{vol}} p^2(\chi, \boldsymbol{x}),
\end{aligned}
\tag{88}
$$

其中定义标量**体积极化参数** $P_{\mathrm{vol}}$ 为：

$$
P_{\mathrm{vol}} = \frac{1}{\kappa} \left(\boldsymbol{I} : \mathbb{P}_{\mathrm{vol}} : \boldsymbol{I}\right) = \frac{1 + \beta}{E_s}\frac{\gamma - \tau_1\tau_2}{\alpha\gamma + \tau_1\tau_2}.
\tag{89}
$$

通过将体积模量 $\kappa$ 吸收进分子分母的极限抵消中，式 (89) 在不可压缩极限下完全正则化！

> **注 3.4**：在完全不可压缩极限下，当两相材料均不可压缩时，由于体积变形彻底受限，$P_{\mathrm{vol}}$ 必须自然为零。代入 $\nu_e = \nu_i = 0.5$，可以严格验证：
> $$
> \left.P_{\mathrm{vol}}\right|_{\nu=0.5} = \frac{1 + \beta}{E_s}\frac{\gamma - 1}{\alpha\gamma + 1} = \frac{4 - 4\nu}{E_s}\frac{\gamma - 1}{\frac{1}{1 - 2\nu}\gamma + 1} = 0.
> \tag{90}
> $$
> 此时体积效应自然消失，拓扑演化纯粹由偏量应变/应力驱动。

综上所述，**同时适用于近不可压缩与完全不可压缩介质（平面应变与三维）的偏量/球偏分解拓扑导数通用解析式**最终表达为：

$$
D_T J(\chi, \boldsymbol{x}) = \boldsymbol{e}(\chi, \boldsymbol{x}) : \mathbb{P}_{\mathrm{dev}} : \boldsymbol{s}(\chi, \boldsymbol{x}) + P_{\mathrm{vol}} p^2(\chi, \boldsymbol{x}) + (1 - \gamma)\boldsymbol{b} \cdot \boldsymbol{u}(\chi, \boldsymbol{x}).
\tag{91}
$$

> **注 3.5**：在 $u/p$ 格式中，$\boldsymbol{e}$ 和 $\boldsymbol{s}$ 来自位移梯度的数值微分；而在 $u/p/e$ 三场格式中，$\boldsymbol{e}$ 作为主未知量直接求解，$\boldsymbol{s} = \mathbb{C}_{\mathrm{dev}} : \boldsymbol{e}$ 精度大幅提升，从而使式 (91) 拓扑导数的计算精度更为优异。

## 3.5 界面单元处理 (Treatment of the interface elements)

对于被两相材料相割的界面单元 $K^\Gamma$，采用连续正则化示性函数方法：

$$
V_s = \frac{K_s^\Gamma}{K^\Gamma} \in (0, 1), \quad V_w = \frac{K_w^\Gamma}{K^\Gamma} = 1 - V_s \in (0, 1),
\tag{92}
$$

$$
\tilde{\chi}(\boldsymbol{x}) = \frac{K_s^\Gamma}{K^\Gamma}, \quad \boldsymbol{x} \in K^\Gamma.
\tag{93}
$$

界面单元上的极化张量与体积极化参数按体积加权平均插值：

$$
\mathbb{P}_{\mathrm{dev}} = \frac{\Omega_s^\Gamma}{\Omega^\Gamma}\mathbb{P}_{\mathrm{dev}}^s + \left(1 - \frac{\Omega_s^\Gamma}{\Omega^\Gamma}\right)\mathbb{P}_{\mathrm{dev}}^w, \quad P_{\mathrm{vol}} = \frac{\Omega_s^\Gamma}{\Omega^\Gamma}P_{\mathrm{vol}}^s + \left(1 - \frac{\Omega_s^\Gamma}{\Omega^\Gamma}\right)P_{\mathrm{vol}}^w.
\tag{94}
$$

随后统一代入式 (91) 计算界面上的拓扑导数。

---

# 4 拓扑优化算法 (The Topology Optimization Algorithm)

优化求解流程如图 1 所示：

![[Castanar2022_Fig1.png]]
<center><b>
图 1：拓扑优化算法流程图 (Topology Optimization Algorithm Flowchart)
</b></center>

算法初始设定单位水平集函数：

$$
\psi^0(\boldsymbol{x}) = 1 \quad \text{在 } \Omega \text{ 内}.
\tag{95}
$$

在第 $i$ 步迭代中，根据前一步水平集函数计算示性函数：

$$
\chi^i(\boldsymbol{x}) = H\left(\psi^{i-1}(\boldsymbol{x})\right),
\tag{96}
$$

求解混合有限元方程，获得未知量场并计算带符号拓扑导数 $D_T^s J^i(\chi^i, \boldsymbol{x})$。为确保迭代平稳收敛，引入松弛与正则化投影函数：

$$
\phi^i(\chi^i, \boldsymbol{x}) = \kappa^i \frac{\Pi\left(D_T^s J^i(\chi^i, \boldsymbol{x})\right)}{\|\Pi(D_T^s J^i(\chi^i, \boldsymbol{x}))\|} + (1 - \kappa^i)\psi^{i-1}(\chi^{i-1}, \boldsymbol{x}),
\tag{97}
$$

其中 $\Pi$ 为有限元节点投影算子（采用集中质量矩阵以提升计算效率，兼具标准过滤滤波功能）。当前步水平集函数更新为：

$$
\psi^i(\chi^i, \boldsymbol{x}) = \phi^i(\chi^i, \boldsymbol{x}) + \lambda^i,
\tag{98}
$$

拉格朗日乘子 $\lambda^i$ 通过割线法（secant method）高精度求解下式确定：

$$
\int_{\Omega} H\left(\psi^i(\chi^i, \boldsymbol{x})\right) \,\mathrm{d}\Omega = L|\Omega|.
\tag{99}
$$

为了自适应控制松弛因子 $\kappa^i$，定义空间振荡指示子：

$$
\xi^i(\chi^i, \boldsymbol{x}) = \operatorname{sign}\left\{ \left[\frac{\Pi(D_T^s J^i)}{\|\Pi(D_T^s J^i)\|} - \psi^{i-1}\right] \left[\psi^{i-1} - \psi^{i-2}\right] \right\}.
\tag{100}
$$

当 $\xi^i = 1$ 时算法单调推进；当 $\xi^i = -1$ 时局部出现振荡。引入局部微调函数：

$$
\mu^i(\chi^i, \boldsymbol{x}) = \begin{cases}
k_1 \kappa^{i-1}, & \xi^i = 1, \\
k_2 \kappa^{i-1}, & \xi^i = -1,
\end{cases}
\tag{101}
$$

并通过全域加权积分获得标量松弛因子：

$$
\kappa^i = \min\left\{ \left[\frac{\int_\Omega \mu^i(\chi^i, \boldsymbol{x})^{-k_3} \,\mathrm{d}\Omega}{\int_\Omega \psi^i(\chi^i, \boldsymbol{x})\,\mathrm{d}\Omega}\right]^{-k_3}, 1 \right\},
\tag{102}
$$

算例中算法参数取为 $k_1 = 1.1, k_2 = 0.5, k_3 = 0.1$。

> **注 4.1**：该算法在每一次迭代中均严格、精确地满足体积约束，相比罚函数法极大地增强了全局算法稳健性。

---

# 5 数值算例 (Numerical Examples)

所有算例中，算法参数取为 $c_1 = 4, c_2 = 2, c_3 = 0.1$。弱相材料默认设为可压缩，$\nu_w = 0.4$；刚度跳跃比取 $\gamma = 10^{-3}$。所有场变量均采用连续线性插值（$P_1$ 单元）。

## 5.1 单点受载梁 (Single-point load beam)

考查两端固支、底部中点受集中力 $F = 3\,\mathrm{N}$ 的矩形受载梁（图 2）。强材料模量 $E_s = 30\,\mathrm{Pa}$。利用对称性，取左半部分建模，划分为约 51,200 个线性三角形单元，目标体积分数 $L = 40\%$。

![[Castanar2022_Fig2.png]]
<center><b>
图 2：单点受载梁几何模型与边界条件 (Single-point load beam. Geometry)
</b></center>

首先考查**平面应力**工况。由于平面应力下即使泊松比 $\nu_s \to 0.5$，弹性张量也不奇异，因此传统位移法也能获得合理结果（图 3）。可压缩与完全不可压缩极限下的最优构型没有本质差异。

![[Castanar2022_Fig3.png]]
<center><b>
图 3：平面应力工况下单点受载梁最终优化结构（左半域）：(a) $\nu_s = 0.4$；(b) $\nu_s = 0.5$
</b></center>

而在**平面应变**工况下，随着强相材料泊松比逼近不可压缩极限，位移法发生剧烈的体积自锁，导致拓扑演化彻底崩溃（图 4）：当 $\nu_s \geq 0.49$ 时，位移法优化结果呈现严重的伪构型病态。

![[Castanar2022_Fig4.png]]
<center><b>
图 4：平面应变工况下传统位移法随着不可压缩度增加退化的结构构型：(a) $\nu_s = 0.4$；(b) $\nu_s = 0.45$；(c) $\nu_s = 0.49$；(d) $\nu_s = 0.4999$
</b></center>

应用本文提出的稳定化混合有限元与新型拓扑导数，在可压缩情形下与经典解高度吻合（图 5 与图 6）：

![[Castanar2022_Fig5.png]]
<center><b>
图 5：采用 $u/p$ 混合格式的可压缩平面应变梁最终优化结构：(a) $\nu_s = 0.4$ 位移场；(b) $\nu_s = 0.4$ 压力场；(c) $\nu_s = 0.45$ 位移场；(d) $\nu_s = 0.45$ 压力场
</b></center>

![[Castanar2022_Fig6.png]]
<center><b>
图 6：采用 $u/p/e$ 混合格式的可压缩平面应变梁最终优化结构：(a) $\nu_s = 0.4$ 位移场；(b) $\nu_s = 0.4$ 压力场；(c) $\nu_s = 0.45$ 位移场；(d) $\nu_s = 0.45$ 压力场
</b></center>

当材料达到**完全不可压缩极限（$\nu_s = 0.5$）**时，混合法成功求解出清晰的最优构型（图 7）。不可压缩介质的最优拓扑呈现明显不同于可压缩介质的特征：杆件数目变少、单杆厚度明显变粗。

![[Castanar2022_Fig7.png]]
<center><b>
图 7：完全不可压缩平面应变工况（$\nu_s = 0.5$）下两类混合格式的最终优化结构：(a) $u/p$ 位移场；(b) $u/p$ 压力场；(c) $u/p/e$ 位移场；(d) $u/p/e$ 压力场
</b></center>

收敛历程如图 8 所示，两类混合格式均在 100 步以内平稳收敛。

![[Castanar2022_Fig8.png]]
<center><b>
图 8：完全不可压缩平面应变工况（$\nu_s = 0.5$）下单点受载梁柔顺度收敛历程曲线
</b></center>

## 5.2 支承装置 (Bearing device)

第二算例考查橡胶支承装置（图 9）。强材料模量 $E_s = 100\,\mathrm{Pa}, \nu_s = 0.5$，网格含 19,200 个线性三角形单元，目标体积分数 $L = 35\%$。

![[Castanar2022_Fig9.png]]
<center><b>
图 9：支承装置几何模型与载荷条件 (Bearing device. Geometry)
</b></center>

若将弱材料错误地设为不可压缩（$\nu_w = 0.5$），弱材料区被封闭在强材料环内无法变形，呈现极高伪刚度，导致算法退化为不合理的构型（图 10）。而当正确设置可压缩弱材料（$\nu_w = 0.4$）时，获得了物理合理的橡胶支承最优拓扑（图 11）。

![[Castanar2022_Fig10.png]]
<center><b>
图 10：弱相材料设为不可压缩（$\nu_s = 0.5, \nu_w = 0.5$）时的错误优化构型与压力陷阱：(a) 位移场；(b) 压力场
</b></center>

![[Castanar2022_Fig11.png]]
<center><b>
图 11：弱相材料正确设为可压缩（$\nu_s = 0.5, \nu_w = 0.4$）时的合理优化构型：(a) 位移场；(b) 压力场
</b></center>

图 12 给出了对应的收敛历程对比，证实了不可压缩弱材料产生虚假超低柔顺度（人工刚度）的力学机理。

![[Castanar2022_Fig12.png]]
<center><b>
图 12：支承装置在 $\nu_w = 0.4$ 与 $\nu_w = 0.5$ 下的柔顺度迭代历程对比
</b></center>

## 5.3 L 形梁 (L-shaped beam)

第三算例为存在内凹拐角几何应力奇异性的典型 L 形梁（图 13）。$E_s = 1\,\mathrm{MPa}, \nu_s = 0.5$，网格约 22,800 个单元，目标体积比 $L = 50\%$。

![[Castanar2022_Fig13.png]]
<center><b>
图 13：L 形梁几何模型与边界条件 (L-shaped beam. Geometry)
</b></center>

在较细网格下，$u/p$ 与 $u/p/e$ 格式获得的位移场与压力场大致接近（图 14 与图 15）：

![[Castanar2022_Fig14.png]]
<center><b>
图 14：完全不可压缩 L 形梁位移场对比：(a) $u/p$ 格式；(b) $u/p/e$ 格式
</b></center>

![[Castanar2022_Fig15.png]]
<center><b>
图 15：完全不可压缩 L 形梁压力场对比：(a) $u/p$ 格式；(b) $u/p/e$ 格式
</b></center>

**然而，在偏应变场与应力场方面，两类格式展现出截然不同的精度（图 16）**：在 $u/p$ 格式中，应变来自线性单元位移梯度的微分，呈片元常数分布，断口剧烈且严重不平滑；而在 $u/p/e$ 格式中，偏应变作为主变量连续求解，获得了光滑连续、高保真的应变与应力分布，无需任何后处理平滑操作。

![[Castanar2022_Fig16.png]]
<center><b>
图 16：L 形梁各偏应变分量云图对比：左列为 $u/p$ 格式（片元常数，存在间断振荡），右列为 $u/p/e$ 格式（节点连续，高精度光滑）
</b></center>

> **注 5.1**：应力与应变场的高精度对于流固耦合（FSI）和局部应力约束拓扑优化等前沿问题具有重大工程应用价值。

## 5.4 三维算例 (A 3D problem)

第四算例为三维悬臂梁（图 17）。$E_s = 1\,\mathrm{MPa}, \nu_s = 0.5$。取半结构对称建模，采用约 380,000 个线性四面体单元离散，目标体积分数 $L = 10\%$。

![[Castanar2022_Fig17.png]]
<center><b>
图 17：三维悬臂梁几何构型与边界条件 (3D Cantilever beam. Geometry)
</b></center>

图 18 与图 19 展示了 $u/p$ 与 $u/p/e$ 格式下优化结构的三维位移场与压力场，两类格式收敛于一致的清晰三维结构构型。

![[Castanar2022_Fig18.png]]
<center><b>
图 18：完全不可压缩（$\nu_s = 0.5$）三维悬臂梁最终优化构型位移场：(a) $u/p$ 格式；(b) $u/p/e$ 格式
</b></center>

![[Castanar2022_Fig19.png]]
<center><b>
图 19：完全不可压缩（$\nu_s = 0.5$）三维悬臂梁最终优化构型压力场：(a) $u/p$ 格式；(b) $u/p/e$ 格式
</b></center>

图 20 给出了偏应变范数云图，再次印证了 $u/p/e$ 格式在复杂三维几何中捕获高精度应变场的卓越能力。数值结果亦证实采用各向同性平面应变极化张量作为三维问题的近似在工程上完全可行。

![[Castanar2022_Fig20.png]]
<center><b>
图 20：完全不可压缩（$\nu_s = 0.5$）三维悬臂梁偏应变范数分布：(a) $u/p$ 格式；(b) $u/p/e$ 格式
</b></center>

---

# 6 结论 (Conclusions)

本文提出了一种基于拓扑导数概念、面向近不可压缩与完全不可压缩弹性材料的结构拓扑优化新方法。通过将 Pólya–Szegö 极化张量分解为其偏量部分与球偏部分，推导出了一种新型、简洁且无奇异性的不可压缩拓扑导数解析表达式，使得在线弹性范围内处理不可压缩材料拓扑设计成为可能。

成功求解不可压缩力学问题的基石是第 2 节引入的两类变分多尺度稳定化混合有限元格式：
1. **$u/p$ 二场混合格式**：有效规避了离散 inf-sup 条件限制，使简单的全 $P_1$ 单元免于体积自锁；
2. **$u/p/e$ 三场混合格式**：将偏应变作为独立节点未知量，使得在计算偏应力和拓扑导数时获得了更高的精度，生成的应力应变场天然连续光滑，无需后处理人工平滑。

在材料插值模型方面，阐明了在拓扑优化中将弱相材料设为不可压缩会导致弱相“封闭气泡”产生非物理的人工体积刚度，指出弱相材料必须设为可压缩介质（$\nu_w < 0.5$）。

数值算例充分展示了所提算法的稳健性：算例 5.1 证明了该格式能够无缝处理任意泊松比材料；算例 5.2 揭示并消除了弱相材料的体积自锁陷阱；算例 5.3 阐明了三场格式在复杂应力集中处的超高精度优势；算例 5.4 验证了 38 万单元规模复杂三维不可压缩拓扑优化的高效适用性。

---

# 利益冲突声明 (Declaration of competing interest)

作者声明不存在已知可能影响本文报道工作的竞争性经济利益或人际关系。

# 致谢 (Acknowledgements)

I. Castañar 感谢通过预博士 FI 资助（2019-FI-B-00649）获得 Agència de Gestió d'Ajuts Universitaris i de Recerca 的资助支持。J. Baiges 感谢通过 Ramón y Cajal 资助（RYC-2015-17367）获得西班牙政府的支持。R. Codina 感谢通过加泰罗尼亚政府 ICREA Acadèmia 研究计划获得的支持。本工作部分由西班牙政府 TOP-FSI: RTI2018-098276-B-I00 项目资助。CIMNE 获得西班牙经济与竞争力部“Severo Ochoa 研发卓越中心计划”资助（CEX2018-000797-S）。

---

# 参考文献 (References)

[1] M.P.Bendsøe and O.Sigmund. *Topological Optimization: Theory*. Springer, 2013.

[2] M.P.Bendsøe and N.Kikuchi. Generating optimal topologies in structural design using a homogenization method. *Computer Methods in Applied Mechanics and Engineering*, 71(2):197–224, 1988.

[3] X.Huang and Y.Xie. A further review of ESO type methods for topology optimization. *Structural and Multidisciplinary Optimization*, 41:671–683, 2010.

[4] N.P. van Dijk, K.Maute, M.Langelaar, and F. van Keulen. Level-set methods for structural topology optimization: a review. *Structural and Multidisciplinary Optimization*, 48:437–472, 2013.

[5] J.D.Deaton and R.V.Grandhi. A survey of structural and multidisciplinary continuum topology optimization: post 2000. *Structural and Multidisciplinary Optimization*, 49:1–38, 2014.

[6] A.A.Novotny and J.Sokolowski. *Topological Derivatives in Shape Optimization*. Springer, 2013.

[7] J.Baiges, J.Martínez-Frutos, D.Herrero-Pérez, F.Otero, and A.Ferrer. Large-scale stochastic topology optimization using adaptive mesh refinement and coarsening through a two-level parallelization scheme. *Computer Methods in Applied Mechanics and Engineering*, 343:186–206, 2019.

[8] A.A.Novotny, J.Sokolowski, and A.Zochowski. Topological derivatives of shape functionals. Part I: Theory in singularly perturbed geometrical domains. *Journal of Optimization Theory and Applications*, 180:341–373, 2019.

[9] J.Oliver, D.Yago, J.Cante, and O.Lloberas-Valls. Variational approach to relaxed topological optimization: Closed form solutions for structural problems in a sequential pseudo-time framework. *Computer Methods in Applied Mechanics and Engineering*, 355:779–819, 2019.

[10] L.R.G.Treloar. *The Physics of Rubber Elasticity*. Oxford University Press, 1975.

[11] X.Oliver and C.A. de Saracibar. *Continuum Mechanics for Engineers. Theory and Problems*, 2nd edition, 2017.

[12] T.J.R.Hughes. *The Finite Element Method: Linear Static and Dynamic Finite Element Analysis*. Prentice-Hall, Englewood Cliffs, New Jersey, 1987.

[13] T.J.R.Hughes, L.P.Franca, and M.Balestra. A new finite element formulation for computational fluid dynamics: Circumventing the Babuška-Brezzi condition: a stable Petrov-Galerkin formulation of the Stokes problem accommodating equal-order interpolations. *Computer Methods in Applied Mechanics and Engineering*, 59:85–99, 1986.

[14] R.Codina. A stabilized finite element method for generalized stationary incompressible flows. *Computer Methods in Applied Mechanics and Engineering*, 190:2681–2706, 2001.

[15] L.P.Franca, T.J.R.Hughes, A.F.D.Loula, and I.Miranda. A new family of stable elements for nearly incompressible elasticity based on a mixed Petrov-Galerkin finite element formulation. *Numerische Mathematik*, 53(1–2):123–141, 1988.

[16] M.Chiumenti, Q.Valverde, C.A. de Saracibar, and M.Cervera. A stabilized formulation for incompressible elasticity using linear displacement and pressure interpolations. *Computer Methods in Applied Mechanics and Engineering*, 191:1095–1116, 2002.

[17] M.Cervera, M.Chiumenti, and R.Codina. Mixed stabilized finite element methods in nonlinear solid mechanics. Part I: Formulation. *Computer Methods in Applied Mechanics and Engineering*, 199(37–40):2559–2570, 2010.

[18] M.Cervera, M.Chiumenti, and R.Codina. Mixed stabilized finite element methods in nonlinear solid mechanics. Part II: Strain localization. *Computer Methods in Applied Mechanics and Engineering*, 199(37–40):2571–2589, 2010.

[19] I.Castañar, J.Baiges, and R.Codina. A stabilized mixed finite element approximation for incompressible finite strain solid dynamics using a total Lagrangian formulation. *Computer Methods in Applied Mechanics and Engineering*, 368:Article 113164, 2020.

[20] R.Codina. Stabilized finite element approximation of transient incompressible flows using orthogonal subscales. *Computer Methods in Applied Mechanics and Engineering*, 191:4295–4321, 2002.

[21] R.Codina, J.M.González-Ondina, G.Díaz-Hernández, and J.Príncipe. Finite element approximation of the modified Boussinesq equations using a stabilized formulation. *International Journal for Numerical Methods in Engineering*, 57:1249–1268, 2008.

[22] T.J.R.Hughes, G.R.Feijóo, L.Mazzei, and J.Quincy. The variational multiscale method - a paradigm for computational mechanics. *Computer Methods in Applied Mechanics and Engineering*, 166:3–24, 1998.

[23] M.Chiumenti, M.Cervera, and R.Codina. A mixed three-field FE formulation for stress accurate analysis including the incompressible limit. *Computer Methods in Applied Mechanics and Engineering*, 283:1095–1116, 2015.

[24] O.Sigmund and P.M.Clausen. Topology optimization using a mixed formulation: An alternative way to solve pressure load problems. *Computer Methods in Applied Mechanics and Engineering*, 196:1874–1889, 2007.

[25] M.Bruggi and P.Venini. Topology optimization of incompressible media using mixed finite elements. *Computer Methods in Applied Mechanics and Engineering*, 196:3151–3164, 2007.

[26] M.Stolpe and K.Svanberg. An alternative interpolation scheme for minimum compliance optimization. *Structural and Multidisciplinary Optimization*, 22(2):116–124, 2001.

[27] K.Svanberg. The method of moving asymptotes-a new method for minimum compliance optimization. *International Journal for Numerical Methods in Engineering*, 24:359–373, 1987.

[28] C.Li and L.Tong. Topology optimization of incompressible materials based on the mixed SBFEM. *Computers and Structures*, 165:24–33, 2016.

[29] G.Zhang, R.Alberdi, and K.Khandelwal. Topology optimization with incompressible materials under small and finite deformations using mixed u/p elements. *International Journal for Numerical Methods in Engineering*, 115:1015–1052, 2018.

[30] A.A.Novotny, J.Sokolowski, and A.Zochowski. Topological derivatives of shape functionals. Part II: First-order method and applications. *Journal of Optimization Theory and Applications*, 180:683–710, 2019.

[31] I.Babuška. Error-bounds for finite element method. *Numerische Mathematik*, 16(4):322–333, 1971.

[32] R.Codina, S.Badia, J.Baiges, and J.Principe. *Variational Multiscale Methods in Computational Fluid Dynamics*. John Wiley & Sons Ltd., 2017.

[33] S.Badia and R.Codina. Unified stabilized finite element formulations for the Stokes and the Darcy problems. *SIAM Journal on Numerical Analysis*, 47(3):1971–2000, 2009.

[34] R.Codina. Stabilization of incompressibility and convection through orthogonal sub-scales in finite element methods. *Computer Methods in Applied Mechanics and Engineering*, 190:1579–1599, 2000.

[35] R.Codina. Finite element approximation of the three field formulation of the Stokes problem using arbitrary interpolations. *SIAM Journal on Numerical Analysis*, 47:699–718, 2009.

[36] M.Chiumenti, M.Cervera, C.A.Moreira, and G.B.Barbat. Stress, strain and dissipation accurate 3-field formulation for inelastic isochoric deformation. *Finite Elements in Analysis and Design*, 192:103534, 2021.

[37] A.Ferrer. SIMP-ALL: A generalized SIMP method based on the topological derivative concept. *International Journal for Numerical Methods in Engineering*, 120(3):361–381, 2019.

[38] M.P.Bendsøe and O.Sigmund. Material interpolation schemes in topology optimization. *Archive of Applied Mechanics*, 69:635–654, 1999.

[39] S.M.Giusti, A.Ferrer, and J.Oliver. Topological sensitivity analysis in heterogeneous anisotropic elasticity problem. Theoretical and computational aspects. *Computer Methods in Applied Mechanics and Engineering*, 311:134–150, 2016.

[40] J.D.Eshelby. The determination of the elastic field of an ellipsoidal inclusion, and related problems. *Proceedings of the Royal Society: Section A*, 241:376–396, 1957.

[41] J.D.Eshelby. The elastic field outside an ellipsoidal inclusion, and related problems. *Proceedings of the Royal Society: Section A*, 252:561–569, 1959.

[42] C.G.Lopes, R.Batista dos Santos, and A.A.Novotny. Topological derivative-based topology optimization of structures subject to multiple load-cases. *Latin American Journal of Solids and Structures*, 12:834–860, 2015.

[43] S.Amstutz and H.Andrä. A new algorithm for topology optimization using a level-set method. *Journal of Computational Physics*, 216(2):573–588, 2006.

[44] S.Amstutz, S.M.Giusti, A.A.Novotny, and E.A.De Souza Neto. Topological derivative for multi-scale linear elasticity models applied to the synthesis of microstructures. *International Journal for Numerical Methods in Engineering*, 84(6):733–756, 2010.

[45] P.R.Amestoy, I.S.Duff, J.Koster, and J.-Y.L'Excellent. A fully asynchronous multifrontal solver using distributed dynamic scheduling. *SIAM Journal on Matrix Analysis and Applications*, 23(1):15–41, 2001.

[46] P.R.Amestoy, A.Buttari, J.-Y.L'Excellent, and T.Mary. Performance and scalability of the block low-rank multifrontal factorization on multicore architectures. *ACM Transactions on Mathematical Software*, 45(2):Article 2, 2019.

[47] T.Elguedj, Y.Bazilevs, V.M.Calo, and T.J.R.Hughes. $\bar{B}$ and $\bar{F}$ projection methods for nearly incompressible linear and nonlinear elasticity and plasticity using higher-order NURBS elements. *Computer Methods in Applied Mechanics and Engineering*, 197:2732–2762, 2008.

[48] D.S.Malkus and T.J.R.Hughes. Mixed finite element methods - Reduced and selective integration techniques: A unification of concepts. *Computer Methods in Applied Mechanics and Engineering*, 15:63–81, 1978.

[49] J.Baiges and R.Codina. Variational multiscale error estimators for solid mechanics adaptive simulations: an orthogonal subgrid scale approach. *Computer Methods in Applied Mechanics and Engineering*, 325:37–55, 2017.

[50] S.A.Nazarov. Elasticity polarization tensor, surface enthalpy, and Eshelby theorem. *Journal of Mathematical Sciences*, 159:133–167, 2009.

[51] V.A.Eremeyev and V.Konopińska-Zmysłowska. On the correspondence between two- and three-dimensional Eshelby tensors. *Continuum Mechanics and Thermodynamics*, 31:1615–1625, 2019.

[52] A.A.Novotny, J.Sokolowski, and A.Zochowski. Topological derivatives of shape functionals. Part III: Second-order method and applications. *Journal of Optimization Theory and Applications*, 181:1–22, 2019.

[53] A.A.Novotny, R.A.Feijóo, E.Taroco, and C.Padra. Topological sensitivity analysis for three-dimensional linear elasticity problem. *Computer Methods in Applied Mechanics and Engineering*, 196:4354–4364, 2007.

[54] O.Sigmund and P.M.Clausen. Topology optimizations using a mixed formulation: An alternative way to solve pressure load problems. *Computer Methods in Applied Mechanics and Engineering*, 196:1874–1889, 2007.

[55] M.Kachanov, B.Shafiro, and I.Tsukrov. *Handbook of Elasticity Solutions*. Kluwer Academic Publishers, 2003.

[56] E.Boman, K.Devine, L.A.Fisk, R.Heaphy, B.Hendrickson, V.Leung, C.Vaughan, U.Catalyurek, D.Bozdag, and W.Mitchell. Zoltan home page, `http://www.cs.sandia.gov/zoltan`. Sandia National Laboratories, 1999.

[57] H.A.Van der Vorst. Bi-CGSTAB: A fast and smoothly converging variant of Bi-CG for the solution of nonsymmetric linear systems. *SIAM Journal on Scientific and Statistical Computing*, 13(2):631–644, 1992.

[58] S.Balay, S.Abhyankar, M.F.Adams, J.Brown, P.Brune, K.Buschelman, L.Dalcin, V.Eijkhout, W.D.Gropp, D.Kaushik, M.G.Knepley, D.A.May, L.Curfman McInnes, R.T.Mills, T.Munson, K.Rupp, P.Sanan, B.F.Smith, S.Zampini, H.Zhang, and H.Zhang. PETSc Web page, `http://www.mcs.anl.gov/petsc`, 2015.

[59] W.Schroeder, K.Martin, and B.Lorensen. *The Visualization Toolkit* (4th ed.). Kitware, 2006.
