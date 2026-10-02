---
title: "翻译：PolyTop: a Matlab implementation of a general topology optimization framework using unstructured polygonal finite element meshes"
tags:
  - translation
  - topology-optimization
  - polygonal-fem
  - unstructured-mesh
status: "done"
date_created: 2026-09-11
date_updated: 2026-09-11
source: "../sources/Talischi2012-polytop.pdf"
citekey: "Talischi2012-polytop"
language: "zh-CN"
---

# PolyTop: a Matlab implementation of a general topology optimization framework using unstructured polygonal finite element meshes

---

# 信息

- **中文标题**：PolyTop：采用非结构多边形有限元网格的通用拓扑优化框架的 Matlab 实现
- **作者**：Cameron Talischi；Glaucio H. Paulino；Anderson Pereira；Ivan F. M. Menezes
- **单位**：University of Illinois at Urbana-Champaign，Department of Civil and Environmental Engineering；Pontifical Catholic University of Rio de Janeiro（PUC-Rio），Tecgraf
- **期刊**：*Structural and Multidisciplinary Optimization*
- **卷 / 期 / 页码**：45(3): 329–357，2012
- **DOI**：[10.1007/s00158-011-0696-x](https://doi.org/10.1007/s00158-011-0696-x)
- **投稿 / 修回 / 录用 / 在线发表**：2011-05-24 / 2011-07-12 / 2011-07-19 / 2012-01-08


> 译者说明：本文按原文结构翻译，保留公式、图表、脚注与参考文献；附录代码按原文转录。[^译注代码]

# 摘要

本文给出了一套高效的 Matlab 结构拓扑优化代码，其中包含一个基于等参多边形单元的通用有限元程序；这种单元可以看作线性三角形单元和双线性四边形单元的推广。该代码还采用模块化结构，将分析程序和优化算法与拓扑优化问题的具体列式分离。在这一框架中，有限元分析和灵敏度分析程序不包含与具体列式有关的信息，因而可以独立扩展、开发和修改。本文讨论了拓扑优化中使用非结构网格和任意设计域所涉及的问题，而这些问题在文献中很少受到关注。此外，在考察拓扑优化问题的过程中，本文回顾了将最优形状问题转化为尺寸优化问题所经历的各个步骤。通过这一过程，可以分离有限元分析参数和几何分析参数，并阐明它们与离散优化问题设计变量之间的关系。本文详细说明了 Matlab 代码，并通过数值算例展示代码的功能。

**关键词**：拓扑优化；非结构网格；多边形有限元；Matlab 软件

> **电子补充材料**：本文在线版本（doi:10.1007/s00158-011-0696-x）包含电子补充材料，仅向授权用户开放。

# 1 引言（Introduction）

本文建立了一个求解拓扑优化问题的通用框架，并给出其简洁而高效的 Matlab 实现。该实现包含通用有限元（finite element, FE）分析程序，并涵盖一大类拓扑优化列式。许多拓扑优化工程应用需要使用非结构网格，以精确描述设计域几何、指定载荷和支撑条件，并可靠地分析设计响应。本文讨论任意网格在拓扑优化中的应用，以及文献中很少受到关注的一些实际问题。例如，非结构网格较高的计算成本有时被用作采用均匀网格的理由，并被归因于需要重复计算单元刚度矩阵。然而，正如本文将要说明的，单元刚度矩阵和全局刚度矩阵连通关系等不变量只需计算一次，随后存储起来供后续优化迭代使用。考虑到当前个人计算机的硬件容量，这一做法所需的存储量相对较小，因而是可行的。此外，与可能需要求解数百个线性方程组的整个优化算法相比，计算多个单元刚度矩阵带来的额外开销很小。本文给出的 Matlab 代码既保持了已有教学代码的可读性和效率，又提供了通用的有限元框架。就效率而言，本文的 Matlab 实现与近期发表的 88 行代码（Andreassen et al. 2010）性能相当，并且在大规模网格上更快。

作为任意网格的一个实例，本文实现了基于等参多边形有限元的有限元程序。[^1] 这一选择增强了代码的通用性，因为等参列式能够支持所有线性多边形，包括更常用的线性三角形和双线性四边形。此外，配套论文（Talischi et al. 2011）还给出了一种采用 Matlab 编写、基于 Voronoi 图概念的多边形网格生成器。这两套代码共同构成了一个自包含的 Matlab 离散化与分析软件包。不过，由于有限元代码具有通用性，用户可以直接实现新的单元，例如高阶单元、非协调单元等，也可以使用其他软件生成的网格（Matlab 网格生成器的一个例子是 Persson and Strang 2004 提出的 distMesh）。

本文另一个相关目标是为拓扑优化建立一种模块化代码结构，使求解状态方程并计算灵敏度的分析程序与所选的具体列式相互独立。这意味着分析程序无须了解所采用的具体列式，从而使代码可以容纳不同列式，而不损害其清晰性或实用性。相比之下，以 99 行、88 行代码及类似代码为代表的已有教学软件常常将分析与列式混合在一起，这或许是为了保持代码短小紧凑，但也因此需要多个版本（Andreassen et al. 2010）。在本文框架内，可以开发、修改或扩展分析程序，而不影响优化代码。反过来，如果一个新问题需要不同类型的分析，也可以用合适的分析软件包替换本文给出的分析程序。其他 Matlab 拓扑优化代码同样可以使用本文的通用分析代码。对于寻求将该框架发展到更复杂、更深入的拓扑优化问题，例如多物理场响应、多个几何约束或状态约束，这种解耦方法的形式化处理至关重要；而对于简单的柔顺度基准问题，这种差别可能并不显著。

作为对拓扑优化问题考察的一部分，本文将回顾把最优形状问题转化为尺寸优化问题的各个步骤。在某些地方，我们会偏离通常的叙述方式，以澄清一些常见误解。例如，Ersatz 方法用柔性材料填充空洞区域，它涉及控制状态方程的近似，而不是所采用的某种特定“尺寸”列式。本文还说明，过滤的目的是以隐式方式保证设计场的光滑性。从一些把设计变量正下界（作为实现 Ersatz 方法的手段）与过滤参数关联起来的列式中可以看出，这两个彼此独立的概念有时会被混淆。此外，一些论文在使用过滤时并不一致：过滤只用于计算刚度项，而没有用于体积约束（关于这一问题的讨论见 Sigmund 2007）。本文还将讨论在连续层面采用过滤的依据，并给出导出常用离散运算所需的近似步骤，而这些步骤通常没有被明确说明。通过上述叙述，本文还将部分回答一个重要但经常被忽略的问题：经过各种参数化与限制步骤之后，实际求解的究竟是什么优化问题。

本文其余部分安排如下。第 2 节回顾拓扑优化问题列式与离散化中的基本概念。第 3 节讨论构成 Matlab 软件基础的解耦方法。第 4 节介绍实现细节，第 5 节给出数值算例，第 6 节讨论效率问题。第 7 节以若干评述作为全文总结。

# 2 若干理论问题（Some theoretical considerations）

本节旨在描述经典的连续体结构拓扑优化问题，并以足够一般的形式识别所得离散优化问题的结构。教学代码的框架反映了本节的结论。在此过程中，本文还将回顾拓扑优化问题列式中的一些基本概念，并对从存在若干病态性质的经典问题出发，经过各种步骤，最终得到传递给非线性规划算法的离散“尺寸”问题这一过程作出说明。

## 2.1 经典问题的表述（Statement of the classical problem）

拓扑优化的目标是寻找物理系统最有效的形状 $\omega \subseteq \mathbb{R}^d$，其中 $d=2,3$，而该系统的行为由边值问题的解 $\boldsymbol{u}_\omega$ 表示。更具体地说，需要处理如下形式的问题：

$$
\inf_{\omega\in\mathcal{O}} f(\omega,\boldsymbol{u}_\omega)
\quad \text{满足}\quad
g_i(\omega,\boldsymbol{u}_\omega)\leq 0,
\quad i=1,\ldots,K.
\tag{1}
$$

其中，$\mathcal{O}$ 表示容许形状的集合，$f$ 和 $g_i$ 分别为衡量每个候选形状或设计 $\omega$ 性能的目标函数与约束函数，$K$ 表示约束数量。容许形状的几何限制，例如对其体积或周长的限制，通常通过这些约束函数施加；而对称性、特征尺寸界限等其他设计要求则在 $\mathcal{O}$ 中规定。如图 1 所示，通常需要定义一个扩展设计域或“包容集”$\Omega$，所有形状均位于其中，即对任意 $\omega\in\mathcal{O}$，都有 $\omega\subseteq\Omega$。这一工作域 $\Omega$ 有助于描述控制边值问题。

![[Talischi2012_Fig1.png]]

<center><b>
图 1：扩展设计域与状态方程的边界条件。
</b></center>

众所周知，如果把 $\mathcal{O}$ 定义为 $\Omega$ 的所有可测子集的集合，则该问题一般不能保证最优解存在（例如见 Kohn and Strang 1986a；Allaire 2001）。本文始终假设通过式 (1) 中的约束或直接对 $\mathcal{O}$ 施加了设计或制造约束，使容许形状满足某种统一正则性，从而保证问题适定。这在文献中通常称为限制（restriction）设定[^2]（Sigmund and Petersson 1998；Borrvall 2001）。本文稍后还将回到这一问题。

本文采用连续体结构优化中常见的线性弹性状态方程。其解 $\boldsymbol{u}_\omega\in\mathcal{V}_\omega$ 满足如下变分问题：

$$
\int_\omega \mathbf{C}\nabla\boldsymbol{u}_\omega:\nabla\boldsymbol{v}\,\mathrm{d}\boldsymbol{x}
=\int_{\widetilde{\Gamma}_N}\boldsymbol{t}\cdot\boldsymbol{v}\,\mathrm{d}s,
\qquad \forall\boldsymbol{v}\in\mathcal{V}_\omega,
\tag{2}
$$

其中

$$
\mathcal{V}_\omega=
\left\{\boldsymbol{v}\in H^1(\omega;\mathbb{R}^d):
\left.\boldsymbol{v}\right|_{\partial\omega\cap\Gamma_D}=\boldsymbol{0}\right\}
\tag{3}
$$

是容许位移空间；$\mathbf{C}$ 是构成形状 $\omega$ 的材料的刚度张量；$\Gamma_D$ 与 $\Gamma_N$ 构成 $\partial\Omega$ 的一个划分；$\widetilde{\Gamma}_N\subseteq\Gamma_N$ 是给定非零面力 $\boldsymbol{t}$ 的边界。为了使优化问题 (1) 非平凡，本文假设对每个容许形状 $\omega$，$\partial\omega\cap\Gamma_D$ 具有非零表面测度，且 $\widetilde{\Gamma}_N\subseteq\partial\omega$。这反映了如下要求：容许形状在 $\Gamma_D$ 上受到支撑，并承受定义在 $\widetilde{\Gamma}_N$ 上的设计载荷。注意，在式 (2) 中，$\omega$ 的自由边界，即 $\partial\omega\setminus\partial\Omega$，是无面力边界。由此可见，这里假设载荷与设计无关。关于压力载荷、自重等设计相关载荷问题的列式与分析，可参见 Bourdin and Chambolle (2003) 以及 Bruyneel and Duysinx (2005)。

如果不对容许形状空间作适当参数化，带有式 (2) 所述边值问题约束的最优设计问题 (1) 就不适合采用常规的离散化和优化策略。例如，容许形状空间 $\mathcal{O}$ 中的隐式约束在离散设定下往往不能直接施加。还应注意，内虚功项和容许位移空间 $\mathcal{V}_\omega$ 会随形状 $\omega$ 变化，这进一步增加了离散化的困难。因此，使用与 $\omega$ 对应的特征函数 $\chi_\omega$，把边值问题重新表述在 $\Omega$ 上是有益的。也就是说，用下式替代式 (2)：

$$
\int_\Omega \chi_\omega\mathbf{C}\nabla\boldsymbol{u}_\omega:\nabla\boldsymbol{v}\,\mathrm{d}\boldsymbol{x}
=\int_{\widetilde{\Gamma}_N}\boldsymbol{t}\cdot\boldsymbol{v}\,\mathrm{d}s,
\qquad \forall\boldsymbol{v}\in\mathcal{V},
\tag{4}
$$

此时，容许位移空间为

$$
\mathcal{V}=
\left\{\boldsymbol{v}\in H^1(\Omega;\mathbb{R}^d):
\left.\boldsymbol{v}\right|_{\Gamma_D}=\boldsymbol{0}\right\},
\tag{5}
$$

与式 (3) 不同，它不依赖于 $\omega$。相应地，对最优设计问题 (1)，定义容许空间 $\mathcal{A}_{\mathcal{O}}=\{\chi_\omega:\omega\in\mathcal{O}\}$。这样，形状 $\omega$ 的几何属性可以借助 $\mathcal{A}_{\mathcal{O}}$ 中相应的特征函数来描述。事实上，这种分布式参数化简化了此类约束的定义和施加。例如，形状 $\omega$ 的体积和周长可以写为

$$
V(\omega)=\int_\Omega\chi_\omega\,\mathrm{d}\boldsymbol{x},
\qquad
P(\omega)=\int_\Omega\lvert\nabla\chi_\omega\rvert\,\mathrm{d}\boldsymbol{x},
$$

其中第二个表达式中的积分应理解为函数 $\chi_\omega$ 的全变差。关于用特征函数表示形状以及相关几何测度论概念的更详细讨论，读者可参见 Delfour and Zolésio (2001) 的专著。

通过特征函数对容许形状集合进行参数化虽然是一个非常有用的起点，但它并没有解决全部理论与实际问题。首先，由于能量双线性形式不再强制，扩展边值问题 (4) 的解不一定存在且唯一。在 $\chi_\omega$ 为零的区域，位移对内虚功没有贡献；这种强制性的丧失对应于该变分方程经过有限元离散后刚度矩阵的奇异性。拓扑优化中的常用方法在水平集文献中有时称为 Ersatz 材料模型，其做法是用刚度为 $\varepsilon\mathbf{C}$ 的柔性材料填充这些空洞区域。这相当于在式 (4) 的双线性形式中用 $\varepsilon+(1-\varepsilon)\chi$ 替换 $\chi$。边界 $\partial\omega$ 上的传递条件近似式 (2) 中的无面力状态（关于退化极限下标量椭圆型状态方程的分析，见 Allaire 2001 和 Dambrine and Kateb 2009）。对于最优设计问题 (1)，这一近似是否有效，不仅取决于状态方程解在 $\varepsilon\to 0$ 时的收敛性，还取决于采用修正状态方程所得最优形状的收敛性。显然，最优形状问题的不适定性进一步增加了 Ersatz 方法分析的难度。关于柔顺度最小化退化问题，读者可参见 Allaire and Francfort (1998) 在均匀化框架下给出的部分结果，以及 Bourdin and Chambolle (2003) 在限制框架下给出的结果。

## 2.2 连续参数化（Continuous parametrization）

从实际角度看，用特征函数参数化区域的一个主要缺点是，这种参数化不适合使用常规非线性规划技术。特别地，$\mathcal{A}_{\mathcal{O}}$ 不是向量空间，而特征函数的自然离散化会产生规模过大、实际难以求解的整数规划问题。因此，拓扑优化领域经常采用形状的“连续”参数化。其本质是以一个能够在某个连续区间中取值的函数作为优化问题的控制变量。下文把它称为尺寸函数（sizing function）。为了恢复设计的二元性质，这种重新表述必须伴随状态方程的修改，或向问题中加入新的约束。例如，在密度法中，尺寸函数是一个在 $[0,1]$ 中取值的体积分数或密度函数 $\rho$，它在状态方程、目标函数和约束函数的描述中取代特征函数。此外，通过材料插值函数改变 $\rho$ 在问题中的作用方式，使最优或近似最优密度函数在 $\Omega$ 的大部分区域仅取 0 和 1，从而近似一个特征函数。

例如，在所谓的 SIMP 列式（采用限制设定）中，容许设计空间 $\mathcal{A}$ 是 $L^\infty(\Omega;[0,1])$ 的一个具有充分正则性的子集[^3]，状态方程为

$$
\int_\Omega\left[\varepsilon+(1-\varepsilon)\rho^p\right]
\mathbf{C}\nabla\boldsymbol{u}:\nabla\boldsymbol{v}\,\mathrm{d}\boldsymbol{x}
=\int_{\widetilde{\Gamma}_N}\boldsymbol{t}\cdot\boldsymbol{v}\,\mathrm{d}s,
\qquad \forall\boldsymbol{v}\in\mathcal{V},
$$

其中 $p>1$ 是惩罚指数（Bendsoe 1989；Rozvany et al. 1992；Rozvany 2009）。同时，$\rho$ 以线性方式进入体积、周长等几何约束：

$$
V(\rho)=\int_\Omega\rho\,\mathrm{d}\boldsymbol{x},
\qquad
P(\rho)=\int_\Omega\lvert\nabla\rho\rvert\,\mathrm{d}\boldsymbol{x}.
$$

直观上，中间体积分数受到惩罚，因为与其对体积的贡献相比，分配给它的刚度更小。如果能够证明 SIMP 问题的最优解是一个特征函数，那么由任意 $\rho\in\mathcal{A}\cap L^\infty(\Omega;\{0,1\})$ 均满足 $\rho^p=\rho$ 可知，把设计空间从特征函数扩展为体积分数函数是合理的。遗憾的是，在限制设定下通常并非如此，因为容许密度是光滑的，两个极值之间的变化发生在一个过渡区域内。不过，对于某些 SIMP 离散列式，已有相关结论（Stolpe and Svanberg 2001a；Rietz 2001；Martinez 2005）。

还应注意，密度法（如 SIMP）存在另一种理论依据，它源于最优设计问题 (1) 的松弛（relaxation）（Kohn and Strang 1986a, b, c；Tartar 2000；Cherkaev 2000；Allaire 2001）。这种所谓的材料分布观点内在地涉及均匀化概念。其直观解释是：通过扩展容许设计空间，使之包含相应的广义形状，从而把近似最优解的剧烈振荡，即经典问题不适定性的根本原因，纳入考虑。由于这些振荡发生在细尺度上，它们在广义设计中的影响通过扩展空间内相应复合材料的均匀化性质得到刻画。每一个广义设计都由一个密度函数表征，该函数度量这些振荡在宏观尺度上的体积分数。

本文采用的是另一种观点，即把密度函数看作特征函数的近似。这是因为本文处于限制设定下，而对于大多数含有布局或制造约束的拓扑优化实际应用，这一设定是自然的。松弛思想很难推广到限制框架，因为它相当于允许材料在微观尺度上自由分布，却限制其在宏观尺度上的变化。从某种意义上说，这从数学和物理两个角度削弱了松弛的概念。不过，可以显式构造遵循 SIMP 模型的复合材料（Bendsoe and Sigmund 1999），即刚度与体积分数同 SIMP 一致的材料，因此原则上可以实现这些设计。关于另一种基于虚构制造成本的 SIMP 物理解释，读者可参见 Rozvany (2009) 和 Zhou and Rozvany (1991)。但是，需要注意的是，如果不对容许密度函数施加额外的正则性条件，SIMP 问题仍然是不适定的。

这时会自然产生一个问题：与“连续”且正则化的设计空间 $\mathcal{A}$ 对应的容许形状空间 $\mathcal{O}$ 是什么？例如，考虑到最优密度函数 $\rho^*$ 通常不是特征函数，一般会通过后处理程序解释所得结果，得到经典形状 $\omega^*\subseteq\Omega$。问题在于：$\omega^*$ 在什么意义上是最优的？如果在最优状态下，密度函数的性能能够由相应经典形状的性能很好地近似，那么，当容许形状空间 $\mathcal{O}$ 由与 $\mathcal{A}$ 中近似特征函数对应的形状组成时，就可以说 $\omega^*$ 是“近似”最优的。注意，在这种情况下，容许形状集合 $\mathcal{O}$ 得到了相当明确的定义，也可能反映了正则化方案的意图，从而使连续参数化设定得到合理解释。

为了进一步说明“后处理”的概念和“最优状态”的含义，考虑图 2 所示的三个在 $[0,1]$ 中取值的光滑密度函数 $\rho$。后两个函数近似特征函数；第二行给出了由 $\chi_{\{\rho\geq 0.5\}}$ 定义的相应特征函数。[^4] 显然，只有后两种情况下，$\rho$ 与 $\chi_{\{\rho\geq 0.5\}}$ 才是“接近”的。此外，SIMP 的连续密度列式被设定为：在最优状态下，只会出现这一类设计，即满足 $\rho\approx\chi_{\{\rho\geq0.5\}}$ 的设计。如果目标函数与约束函数的值也能得到良好近似，即 $f(\rho)\approx f\!\left(\chi_{\{\rho\geq0.5\}}\right)$，那么连续参数化就是可接受的。对于采用 SIMP 的柔顺度最小化问题，这些条件显然成立，尽管在连续设定下尚无数学证明。

![[Talischi2012_Fig2.png]]

<center><b>
图 2：(a)、(c)、(e) 为三个在 $[0,1]$ 中取值的“光滑”密度函数 $\rho$ 的灰度图；(b)、(d)、(f) 为由 $\chi_{\{\rho\geq0.5\}}$ 定义的相应解释形状。
</b></center>

到目前为止，尺寸函数的概念似乎与密度同义。[^5] 不过，连续参数化并不限于密度法，水平集列式（Allaire et al. 2004；Wang et al. 2003；Belytschko et al. 2003；de Ruiter and Keulen 2004；Van Dijk et al. 2009）也可以纳入同一框架：水平集函数或隐式函数 $\varphi$ 可以取正值和负值，并且可以要求其属于某个 $\alpha>0$ 所确定的有界区间 $[-\alpha,\alpha]$（Belytschko et al. 2003）。在状态方程和约束函数中代替 $\chi_\omega$ 的是 $H(\varphi)$，其中 $H$ 是近似 Heaviside 函数。需要说明的是，这里并不讨论最终在离散设定下采用何种优化算法；上述部分文献中的水平集方法根据形状灵敏度分析和形状边界运动演化最优形状。与密度列式类似，必须对水平集函数的变化施加某些约束，才能使所得优化问题适定。此外，还必须通过某种机制保证水平集函数在边界附近足够陡峭，使整个区域内的刚度接近二元状态。

## 2.3 尺寸函数的正则性（Regularity of sizing functions）

下面讨论容许尺寸函数空间的正则性。如前所述，从理论角度看，这一问题与问题的适定性有关。需要强调的是，连续参数化，即以尺寸函数替代特征函数，本身并不能解决这一问题。此外，限制设定为论证常用 Ersatz 方法的合理性提供了适当框架。从实际角度看，对尺寸函数的变化加以限制，与所考虑容许几何形状的制造约束有关。

一些列式借助“连续”参数化显式施加局部或全局正则性约束。例如，在周长约束设定中，加入约束函数（Ambrosio and Buttazzo 1993；Haber et al. 1996；Petersson 1999）

$$
g_i(\rho)=\int_\Omega\lvert\nabla\rho\rvert\,\mathrm{d}\boldsymbol{x}-\overline{P}
$$

要求设计的全变差不超过给定周长 $\overline{P}$，从而保证容许密度不会发生过于剧烈的振荡。在斜率约束列式中，$\mathcal{A}\subseteq W^{1,\infty}(\Omega)$，即容许函数是弱可微函数，且其导数本质有界，并且

$$
g_i(\rho)=\mathop{\mathrm{ess\,sup}}_{\boldsymbol{x}\in\Omega}
\lVert\nabla\rho(\boldsymbol{x})\rVert_\infty-\overline{G},
$$

这意味着在整个扩展域 $\Omega$ 上，$\rho\in\mathcal{A}$ 的梯度不能过大，即不能超过给定值 $\overline{G}$。这一局部约束离散后会在优化问题中产生大量线性约束，计算成本可能高得难以承受。关于各种限制方法，感兴趣的读者可参见 Sigmund and Petersson (1998) 及 Borrvall (2001) 的综述论文。

本文重点采用的另一种方法，是借助“正则化”映射 $\mathcal{P}$ 隐式地对 $\mathcal{A}$ 施加正则性。例如，在常用的过滤列式（Bourdin 2001；Borrvall and Petersson 2001）中，$\mathcal{A}$ 由通过光滑过滤函数 $F$ 卷积产生的密度函数构成，即

$$
\mathcal{A}=
\left\{\mathcal{P}_F(\eta):\eta\in L^\infty(\Omega;[0,1])\right\},
\tag{6}
$$

其中，$\mathcal{P}_F$ 是如下积分算子：

$$
\mathcal{P}_F(\eta)(\boldsymbol{x}):=
\int_\Omega F(\boldsymbol{x},\overline{\boldsymbol{x}})
\eta(\overline{\boldsymbol{x}})\,\mathrm{d}\overline{\boldsymbol{x}}.
\tag{7}
$$

式 (6) 表明，对每个 $\rho\in\mathcal{A}$，都存在可测函数 $\eta$，使 $\rho=\mathcal{P}_F(\eta)$。由于映射 $\mathcal{P}_F$ 的性质，尺寸函数 $\rho$ 继承了核函数 $F$ 的光滑性。因此，即使 $\eta$ 不光滑，也能保证 $\rho$ 是光滑的，见图 3(a)、(b)。正如下一节将要讨论的，正是 $\eta$ 的离散化产生了优化问题的设计变量。因此可以看出，利用 $\mathcal{P}_F$ 定义尺寸函数后，无须再对 $\rho$ 显式施加正则性。

![[Talischi2012_Fig3.png]]

<center><b>
图 3：正则化映射及其离散化的作用示意图。(a) 对随机设计变量向量 $\boldsymbol{z}=(z_\ell)_{\ell=1}^N$，$\eta_h=\sum_{\ell=1}^N z_\ell\chi_{\Omega_\ell}$；(b) 对图 (a) 所示设计函数 $\eta_h$ 和线性过滤核 $F$，得到 $\mathcal{P}_F(\eta_h)$。注意，尽管 $\eta_h$ 剧烈振荡，$\mathcal{P}_F(\eta_h)$ 仍具有由 $F$ 决定的光滑变化；(c) $\mathcal{P}_F^h(\eta_h)$，即在定义 $\eta_h$ 的同一有限元剖分上对 $\mathcal{P}_F(\eta_h)$ 作逐单元常数近似。
</b></center>

常用于过滤、半径为 $R$ 的线性“帽状”核为

$$
F(\boldsymbol{x},\overline{\boldsymbol{x}})
=c(\boldsymbol{x})\max\left(1-
\frac{\lvert\boldsymbol{x}-\overline{\boldsymbol{x}}\rvert}{R},0\right),
\tag{8}
$$

其中，$c(\boldsymbol{x})$ 是归一化系数，定义为对任意 $\boldsymbol{x}\in\Omega$ 满足

$$
\int_\Omega F(\boldsymbol{x},\overline{\boldsymbol{x}})
\,\mathrm{d}\overline{\boldsymbol{x}}=1.
\tag{9}
$$

容易看出，该系数的表达式为

$$
c(\boldsymbol{x})=
\left[
\int_{B_R(\boldsymbol{x})\cap\Omega}
\left(1-\frac{\lvert\boldsymbol{x}-\boldsymbol{w}\rvert}{R}\right)
\mathrm{d}\boldsymbol{w}
\right]^{-1},
$$

其中 $B_R(\boldsymbol{x})$ 是以 $\boldsymbol{x}$ 为中心、半径为 $R$ 的球。条件 (9) 保证过滤场 $\mathcal{P}_F(\eta)$ 的上下界与设计函数 $\eta$ 的上下界相同，例如式 (6) 的设计空间中为 0 和 1。不过，结合前面对 $\mathcal{A}$ 定义的讨论，需要强调的是，映射 $\mathcal{P}_F$ 的作用只是对 $\mathcal{A}$ 中的密度函数施加正则性。Sigmund (2007) 已经明确作出这种区分：他把 $\rho\in\mathcal{A}$ 称为“物理”密度函数，以区别于 $\eta\in L^\infty(\Omega;[0,1])$。

还可以用隐式映射规定容许形状的其他布局或制造约束，其方式与过滤方法施加光滑性的方式相同。下面通过施加对称性的例子说明这一思想；挤压、图案重复和渐变等制造约束也可以用类似方式施加（Kosaka and Swan 1999；Almeida et al. 2010；Stromberg et al. 2011）。假设 $\Omega\subseteq\mathbb{R}^2$ 关于 $x_1$ 轴对称，并令 $\Omega^+=\{(x_1,x_2)\in\Omega:x_2\geq0\}$。与其对所有 $\boldsymbol{x}=(x_1,x_2)\in\Omega$ 加入约束

$$
\rho(x_1,x_2)=\rho(x_1,-x_2),
\tag{10}
$$

这在离散设定下是可行的；不如直接把对称性纳入容许尺寸函数空间。为此，定义算子 $\mathcal{P}_s$，它把定义在 $\Omega^+$ 上的函数 $\eta$ 映射为定义在 $\Omega$ 上的函数 $\mathcal{P}_s(\eta)$，并满足

$$
\mathcal{P}_s(\eta)(\boldsymbol{x})=\eta(x_1,\lvert x_2\rvert),
\tag{11}
$$

其中 $\boldsymbol{x}=(x_1,x_2)\in\Omega$，同时令[^6]

$$
\mathcal{A}=\left\{\mathcal{P}_s(\eta):
\eta\in L^\infty(\Omega^+;[0,1])\right\}.
$$

这仍然表示：如果对某个 $\eta\in L^\infty(\Omega^+;[0,1])$ 有 $\rho=\mathcal{P}_s(\eta)$，则 $\rho\in\mathcal{A}$，因而 $\rho$ 自动满足式 (10)。根据上述讨论，通过两个映射的复合 $\mathcal{P}=\mathcal{P}_F\circ\mathcal{P}_s$，即可方便地把对称性与过滤结合起来。



## 2.4 本文的设定（Setting for this paper）

常见适定拓扑优化列式具有两个主要特征：插值模型以及对容许设计施加正则性。许多拓扑优化列式可以写成如下尺寸问题：

$$
\inf_{\rho\in\mathcal{A}} f(\rho,\boldsymbol{u})
\quad \text{满足}\quad
g_i(\rho,\boldsymbol{u})\leq0,
\quad i=1,\ldots,K,
\tag{12}
$$

其中，容许尺寸函数空间为

$$
\mathcal{A}=
\left\{\mathcal{P}(\eta):
\eta\in L^\infty\!\left(\Omega;[\underline{\rho},\overline{\rho}]\right)
\right\},
\tag{13}
$$

而 $\boldsymbol{u}\in\mathcal{V}$ 满足

$$
\int_\Omega m_E(\rho)\mathbf{C}\nabla\boldsymbol{u}:\nabla\boldsymbol{v}
\,\mathrm{d}\boldsymbol{x}
=\int_{\widetilde{\Gamma}_N}\boldsymbol{t}\cdot\boldsymbol{v}\,\mathrm{d}s,
\qquad \forall\boldsymbol{v}\in\mathcal{V}.
\tag{14}
$$

这里，$m_E$ 是材料插值函数，它把某点处 $\rho$ 的值与该点处的刚度联系起来。[^7] 类似地，列式可能还需要为周长界限等其他几何度量定义插值函数。例如，柔顺度最小化问题

$$
f(\rho,\boldsymbol{u})=
\int_{\widetilde{\Gamma}_N}\boldsymbol{t}\cdot\boldsymbol{u}\,\mathrm{d}s,
\qquad
g(\rho)=\frac{1}{\lvert\Omega\rvert}
\int_\Omega m_V(\rho)\,\mathrm{d}\boldsymbol{x}-\overline{v}
$$

还需要为体积约束定义一个插值函数 $m_V$。除 $m_V$ 和 $m_E$ 外，这一框架还需要给出上下界 $\underline{\rho}$、$\overline{\rho}$ 以及映射 $\mathcal{P}$。

## 2.5 离散化（Discretization）

把最优设计问题重新表述为分布式尺寸优化问题 (12)，有利于构造可行的离散化与优化方案。具体而言，设计场 $\mathcal{A}$ 的有限元离散只需剖分扩展域 $\Omega$，在优化过程中设计不断演化时无须重新划分网格。位移场通常也基于同一有限元剖分离散，不过这种选择可能导致棋盘格模式等数值伪影。需要指出的是，在限制设定下，可以证明这种耦合离散策略在网格加密时是收敛的；因此，当网格足够细时，例如网格尺寸小于过滤半径时，上述数值不稳定现象应当消失。

下面讨论基于同一有限元网格实施离散化的各个步骤。其目标是识别离散优化问题的设计变量，并说明这些设计变量与定义状态方程、进而定义代价泛函的参数之间的关系。如下文所示，这一过程涉及对映射 $\mathcal{P}$ 的近似，而拓扑优化文献通常不讨论这种近似。

设 $\mathcal{T}_h=\{\Omega_\ell\}_{\ell=1}^N$ 是 $\Omega$ 的一个剖分，即当 $\ell\neq k$ 时，$\Omega_\ell\cap\Omega_k=\varnothing$，且 $\bigcup_\ell\Omega_\ell=\overline{\Omega}$；$h$ 表示特征网格尺寸。在分析有限元解向问题 (12) 的解收敛时，令 $h$ 趋于零。本文希望基于这一剖分识别式 (12) 的离散对应形式，因此在本节其余部分固定 $\mathcal{T}_h$。式 (13) 中 $\mathcal{A}$ 的逐片常数离散定义为

$$
\mathcal{A}_h=
\left\{\mathcal{P}(\eta_h):
\underline{\rho}\leq\eta_h\leq\overline{\rho},
\left.\eta_h\right|_{\Omega_\ell}=\mathrm{const}\quad\forall\ell
\right\}.
\tag{15}
$$

换言之，每个 $\rho\in\mathcal{A}_h$ 都是映射 $\mathcal{P}$ 作用于设计函数 $\eta_h$ 的像，而 $\eta_h$ 在每个单元 $\Omega_\ell$ 上取常数值。注意，$\eta_h$ 属于如下形式的有限维函数空间：

$$
\eta_h(\boldsymbol{x})=
\sum_{\ell=1}^N z_\ell\chi_{\Omega_\ell}(\boldsymbol{x}),
\tag{16}
$$

其中，$\chi_{\Omega_\ell}(\boldsymbol{x})$ 是与单元 $\Omega_\ell$ 对应的特征函数，$z_\ell$ 是 $\eta_h$ 在 $\Omega_\ell$ 上所取的常数值。此外，式 (15) 的定义保证每个 $\rho_h\in\mathcal{A}_h$ 均可写为 $\rho_h=\mathcal{P}(\eta_h)$，其中某个 $\eta_h$ 具有式 (16) 的形式。因此，$\mathcal{A}_h$ 中的每个候选设计可以由一组设计变量 $\boldsymbol{z}:=(z_\ell)_{\ell=1}^N$ 定义；对于这一剖分，该向量被传递给优化算法。按照上述定义，$\mathcal{A}$ 与 $\mathcal{A}_h$ 之间的唯一区别是对 $\eta$ 加以限制。正是对函数 $\eta$ 的离散化产生了设计变量 $\boldsymbol{z}$：一方面，它们完全刻画离散容许设计空间 $\mathcal{A}_h$；另一方面，它们又成为尺寸优化中传递给优化算法的参数。

如前所述，在同一剖分 $\mathcal{T}_h$ 上离散状态方程，更具体地说离散位移空间 $\mathcal{V}$，是很方便的。设 $\mathcal{V}_h$ 为这一有限维子空间，并假设每个 $\boldsymbol{u}_h\in\mathcal{V}_h$ 具有展开式

$$
\boldsymbol{u}_h(\boldsymbol{x})=
\sum_{i=1}^M U_i\boldsymbol{N}_i(\boldsymbol{x}),
$$

即 $\{\boldsymbol{N}_i\}_{i=1}^M$ 是 $\mathcal{V}_h$ 的一组基，$M$ 是位移自由度数。当 $\rho=\rho_h\in\mathcal{A}_h$ 时，状态方程 (14) 的 Galerkin 近似可以写为

$$
\mathbf{K}\boldsymbol{U}=\boldsymbol{F},
\tag{17}
$$

其中，$\boldsymbol{U}=(U_i)_{i=1}^M$ 是节点位移向量，

$$
F_i=\int_{\widetilde{\Gamma}_N}
\boldsymbol{t}\cdot\boldsymbol{N}_i\,\mathrm{d}s
\tag{18}
$$

是节点载荷，而

$$
\begin{aligned}
K_{ij}
&=\int_\Omega m_E(\rho_h)\mathbf{C}\nabla\boldsymbol{N}_i:
\nabla\boldsymbol{N}_j\,\mathrm{d}\boldsymbol{x}\\
&=\sum_{\ell=1}^N\int_{\Omega_\ell}
m_E(\rho_h)\mathbf{C}\nabla\boldsymbol{N}_i:
\nabla\boldsymbol{N}_j\,\mathrm{d}\boldsymbol{x}
\end{aligned}
\tag{19}
$$

是刚度矩阵。求和符号内的积分是单元 $\Omega_\ell$ 刚度矩阵在全局节点编号下的第 $(i,j)$ 个条目。

注意，$\rho_h=\mathcal{P}(\eta_h)$ 在 $\Omega_\ell$ 上可能不是常数，因此不能移到该积分之外。同样，仅根据有限元剖分，也不能直接计算设计体积等量。这表明，常用拓扑优化算法除了式 (15) 中 $\mathcal{A}_h$ 的定义所明确给出的近似外，还采用了另一个近似步骤。事实上，求解状态方程时采用的这一近似相当于离散算子 $\mathcal{P}$，因而可以在容许设计空间 $\mathcal{A}_h$ 的定义中显式表示。

在实践中，通常用在每个有限元上取常值的函数 $\widetilde{\rho}_h$ 代替尺寸函数 $\rho_h$，即

$$
\widetilde{\rho}_h(\boldsymbol{x})=
\sum_{\ell=1}^N y_\ell\chi_{\Omega_\ell}(\boldsymbol{x}).
\tag{20}
$$

确定单元值 $y_\ell$ 的一种方法是在单元 $\ell$ 的形心处对 $\rho_h$ 采样：

$$
y_\ell=\rho_h(\boldsymbol{x}_\ell^*),
$$

其中 $\boldsymbol{x}_\ell^*$ 表示单元 $\Omega_\ell$ 形心的位置。例如，在过滤情形下，有

$$
\begin{aligned}
y_\ell
&=\rho_h(\boldsymbol{x}_\ell^*)
=\mathcal{P}_F(\eta_h)(\boldsymbol{x}_\ell^*)\\
&=\int_\Omega F(\boldsymbol{x}_\ell^*,\overline{\boldsymbol{x}})
\eta_h(\overline{\boldsymbol{x}})\,\mathrm{d}\overline{\boldsymbol{x}}\\
&=\sum_{k=1}^N z_k
\underbrace{\int_{\Omega_k}F(\boldsymbol{x}_\ell^*,\overline{\boldsymbol{x}})
\,\mathrm{d}\overline{\boldsymbol{x}}}_{:=w_{\ell k}}.
\end{aligned}
\tag{21}
$$

把计算得到的权重收集到矩阵 $\mathbf{P}=(w_{\ell k})$ 中，可将 $\widetilde{\rho}_h$ 的单元值与 $\eta_h$ 的单元值联系为

$$
\boldsymbol{y}=\mathbf{P}\boldsymbol{z}.
\tag{22}
$$

注意，权重 $w_{\ell k}$ 与设计变量 $\boldsymbol{z}$ 无关，可以在算法开始时计算一次。此外，当网格中的 $\Omega_\ell$ 与 $\Omega_k$ 相距较远时，$\boldsymbol{x}_\ell^*$ 不在 $\mathcal{P}_F(\chi_k)$ 的支集内，因此许多权重为零。由此，$\mathbf{P}$ 可以用稀疏矩阵高效存储。附录 A 说明，这些权重与线性帽状函数 (8) 所采用的常见离散过滤公式一致。

矩阵 $\mathbf{P}$ 必须看作映射 $\mathcal{P}_F$ 的离散对应形式。事实上，对 $\mathcal{A}$ 定义中的任意线性映射[^8] $\mathcal{P}$ 进行这种离散化，都会得到常数矩阵。定义“离散化”映射[^9]

$$
\mathcal{P}_h:\eta\longmapsto
\sum_{\ell=1}^N \mathcal{P}(\eta)(\boldsymbol{x}_\ell^*)
\chi_{\Omega_\ell}.
$$

注意，对每个逐片常数设计函数 $\eta_h$ 及线性映射 $\mathcal{P}$，有

$$
\begin{aligned}
\mathcal{P}(\eta_h)(\boldsymbol{x}_\ell^*)
&=\mathcal{P}\!\left(\sum_{k=1}^N z_k\chi_{\Omega_k}\right)
(\boldsymbol{x}_\ell^*)\\
&=\sum_{k=1}^N z_k\mathcal{P}(\chi_{\Omega_k})
(\boldsymbol{x}_\ell^*)
=\mathbf{P}\boldsymbol{z},
\end{aligned}
$$

其中

$$
(\mathbf{P})_{\ell k}=\mathcal{P}(\chi_{\Omega_k})(\boldsymbol{x}_\ell^*).
\tag{23}
$$

这说明了 $\mathcal{P}_h$ 与矩阵 $\mathbf{P}$ 之间的关系。正如向量 $\boldsymbol{z}$ 表示设计函数 $\eta_h$ 的单元值，向量 $\mathbf{P}\boldsymbol{z}$ 给出逐片常数函数 $\mathcal{P}_h(\eta_h)$ 的单元值。

因此，若把这一近似考虑在内，与 $\mathcal{T}_h$ 对应的容许设计空间 $\mathcal{A}_h$ 可以更准确地描述为

$$
\mathcal{A}_h=
\left\{\mathcal{P}_h(\eta_h):
\underline{\rho}\leq\eta_h\leq\overline{\rho},
\left.\eta_h\right|_{\Omega_\ell}=\mathrm{const}\quad\forall\ell
\right\}.
\tag{24}
$$

图 3 说明了采用线性帽状核 $F$ 的正则化映射 $\mathcal{P}_F$ 及其离散化 $\mathcal{P}_F^h$ 的作用。

在式 (19) 中用 $\widetilde{\rho}_h$ 代替 $\rho_h$，也就相当于用 $\mathcal{P}_h(\eta_h)$ 代替 $\mathcal{P}(\eta_h)$，此时刚度矩阵可以简化为

$$
\mathbf{K}=\sum_{\ell=1}^N m_E(y_\ell)\boldsymbol{k}_\ell,
\tag{25}
$$

其中 $(\boldsymbol{k}_\ell)_{ij}=\int_{\Omega_\ell}\mathbf{C}\nabla\boldsymbol{N}_i:\nabla\boldsymbol{N}_j\,\mathrm{d}\boldsymbol{x}$ 是第 $\ell$ 个单元刚度矩阵。如前所述，从 $\mathcal{P}$ 的近似中受益的并不只是刚度矩阵的计算。对包含体积积分和表面积分的目标函数与约束函数，计算也得到了极大简化。例如，

$$
g(\widetilde{\rho}_h)
=\frac{1}{\lvert\Omega\rvert}\int_\Omega
m_V(\widetilde{\rho}_h)\,\mathrm{d}\boldsymbol{x}-\overline{v}
=\frac{\sum_{\ell=1}^N m_V(y_\ell)\lvert\Omega_\ell\rvert}
{\sum_{\ell=1}^N\lvert\Omega_\ell\rvert}-\overline{v}.
$$

应当指出，收敛性证明中有时没有显式考虑这一额外近似，例如 Borrvall and Petersson (2001)，但它是合理的，因为当网格尺寸 $h$ 趋于零时，其影响会消失。不过，精度问题仍然需要考虑。由于只使用一套网格，$\eta_h$ 的变化以及 $\widetilde{\rho}_h$ 和 $\boldsymbol{u}_h$ 的精度都与同一有限元网格绑定。

## 2.6 最小柔顺度问题的离散形式（Discrete form of the minimum compliance problem）

最后，给出定义在 $\mathcal{T}_h$ 上的离散柔顺度最小化问题：

$$
\inf_{\rho_h\in\mathcal{A}_h}
\int_{\widetilde{\Gamma}_N}\boldsymbol{t}\cdot\boldsymbol{u}_h\,\mathrm{d}s
\quad \text{满足}\quad
\frac{1}{\lvert\Omega\rvert}\int_\Omega
m_V(\rho_h)\,\mathrm{d}\boldsymbol{x}-\overline{v}\leq0,
\tag{26}
$$

其中，容许函数空间 $\mathcal{A}_h$ 由式 (24) 给出，$\boldsymbol{u}_h\in\mathcal{V}_h=\operatorname{span}\{\boldsymbol{N}_i\}_{i=1}^M$ 满足离散状态方程

$$
\int_\Omega m_E(\rho_h)\mathbf{C}\nabla\boldsymbol{u}_h:
\nabla\boldsymbol{v}\,\mathrm{d}\boldsymbol{x}
=\int_{\widetilde{\Gamma}_N}\boldsymbol{t}\cdot\boldsymbol{v}\,\mathrm{d}s,
\qquad \forall\boldsymbol{v}\in\mathcal{V}_h.
$$

式 (12) 与连续问题 (26) 之间的唯一区别，是用有限维对应空间 $\mathcal{A}_h$ 和 $\mathcal{V}_h$ 替代了空间 $\mathcal{A}$ 和 $\mathcal{V}$。[^译注编号]

如上一小节所示，该问题与常见的离散形式完全等价：[^10]

$$
\min_{\boldsymbol{z}\in[\underline{\rho},\overline{\rho}]^N}
\boldsymbol{F}^{\mathsf{T}}\boldsymbol{U}
\quad \text{满足}\quad
\frac{\boldsymbol{A}^{\mathsf{T}}m_V(\mathbf{P}\boldsymbol{z})}
{\boldsymbol{A}^{\mathsf{T}}\boldsymbol{1}}-\overline{v}\leq0,
\tag{27}
$$

其中，式 (18) 给出的 $\boldsymbol{F}$ 与设计变量 $\boldsymbol{z}$ 无关；$\boldsymbol{U}$ 满足式 (17)，其中如式 (25) 所示，$\mathbf{K}$ “线性”依赖于 $m_E(\mathbf{P}\boldsymbol{z})$；$\boldsymbol{A}=(\lvert\Omega_\ell\rvert)$ 是单元体积向量；$\mathbf{P}$ 由式 (23) 定义。

[^1]: 多边形离散已经用于计算固体力学，例如见 Ghosh (2010)。在拓扑优化中，多边形离散能够消除棋盘格等数值不稳定性，因而表现优于线性三角形和四边形（Langelaar 2007；Saxena 2008；Talischi et al. 2009, 2010）。

[^2]: 与此相对的是松弛设定。松弛设定首先把 $\mathcal{O}$ 定义为 $\Omega$ 的所有可测子集的集合，然后通过进一步扩大该空间来处理问题的不适定性。

[^3]: 这里，$L^\infty(\Omega;\mathcal{K})$ 表示定义在 $\Omega$ 上、取值于 $\mathcal{K}\subseteq\mathbb{R}$ 的可测函数空间。例如，$L^\infty(\Omega;\{0,1\})$ 和 $L^\infty(\Omega;[0,1])$ 分别表示取值于 $\{0,1\}$ 和区间 $[0,1]$ 的可测函数空间。

[^4]: 对点 $\boldsymbol{x}\in\Omega$，如果 $\rho(\boldsymbol{x})\geq0.5$，该函数取值 1，否则取值 0。这是一种简单的后处理选择。

[^5]: 密度法的各种变体使用不同的材料插值函数，但基本思想相近（Stolpe and Svanberg 2001b；Bruns 2005）。

[^6]: 此处 $\eta$ 与容许函数 $\mathcal{P}_s(\eta)$ 的区别应当更加明显：$\eta$ 定义在半个区域上，而 $\mathcal{P}_s(\eta)$ 定义在整个 $\Omega$ 上。

[^7]: $m_E$ 实质上决定状态方程对设计的依赖关系。

[^8]: 过滤、对称性、图案重复和挤压约束都可以通过这类线性映射实现。

[^9]: 也可以把 $\mathcal{P}_h$ 看作 $\mathcal{P}_h=\mathcal{I}_h\circ\mathcal{P}$，其中 $\mathcal{I}_h$ 把任意 $\rho_h$ 映射为 $\widetilde{\rho}_h$，即 $\mathcal{I}_h(\rho)=\sum_{\ell=1}^N\rho(\boldsymbol{x}_\ell^*)\chi_{\Omega_\ell}$。

[^10]: 在本文其余部分中，把 $m_E(\boldsymbol{y})$ 和 $m_V(\boldsymbol{y})$ 理解为条目分别为 $m_E(y_\ell)$ 和 $m_V(y_\ell)$ 的向量。

# 3 模块化框架、问题列式与优化器（Modular framework, formulation, and optimizer）

离散优化问题 (27) 的结构允许将分析例程与所选择的具体拓扑优化列式分离。这里的分析例程是指代码中用于计算目标函数和约束函数的一组函数，因此它们需要访问网格信息（例如有限元分析，以及计算设计体积或周长的函数）。由最小柔顺度问题可以看出，问题向量 $\mathbf{E}:=m_E(\mathbf{y})$ 和 $\mathbf{V}:=m_V(\mathbf{y})$，即单元刚度与体积分数，是唯一需要提供给分析函数的“设计”相关信息。分析函数不需要知道插值函数的选择；插值函数对应于尺寸参数化的选择，也不需要知道对设计空间施加约束的映射 $P$。因此，本着上述讨论所体现的思想，拓扑优化的通用实现必须具有这样的结构：有限元例程不包含任何与具体拓扑优化列式有关的信息。该方法的一个明显优点是，可以独立地扩展、开发和修改分析函数。

还可以看到，分析函数中使用的某些量，例如单元面积 $A_\ell$、刚度矩阵 $\mathbf{k}_\ell$，以及整体刚度矩阵 $\mathbf{K}$ 的“连接关系”，在优化算法执行期间只需计算一次。因此，为提高实现效率，应当存储这些不变量。需要强调的是，这与有限元剖分 $\mathcal{T}_h$ 是否均匀无关，即与其是否为结构化网格无关。类似地，矩阵 $\mathbf{P}$ 可以在预处理阶段计算一次并加以存储。

为了采用基于梯度的优化算法求解离散问题 (27)——本文的 Matlab 代码采用的正是这种情况——还必须计算代价函数相对于设计变量 $\mathbf{z}$ 的梯度。灵敏度分析也可以沿着相同思路进行“分离”。分析函数计算代价函数相对于其内部参数 $\mathbf{E}$ 和 $\mathbf{V}$ 的灵敏度。根据链式法则，

$$
\frac{\partial g_i}{\partial z_k}
=\sum_{\ell=1}^{N}
\left(
\frac{\partial E_\ell}{\partial z_k}\frac{\partial g_i}{\partial E_\ell}
+\frac{\partial V_\ell}{\partial z_k}\frac{\partial g_i}{\partial V_\ell}
\right),
$$

或写成等价的向量形式：

$$
\frac{\partial g_i}{\partial \mathbf{z}}
=\frac{\partial \mathbf{E}}{\partial \mathbf{z}}\frac{\partial g_i}{\partial \mathbf{E}}
+\frac{\partial \mathbf{V}}{\partial \mathbf{z}}\frac{\partial g_i}{\partial \mathbf{V}}.
\tag{28}
$$

因此，分析函数只需计算 $g_i$ 关于内部参数 $\mathbf{E}$ 和 $\mathbf{V}$ 的灵敏度。对于柔顺度问题，$f=\mathbf{F}^{\mathrm T}\mathbf{U}$，并且有

$$
\frac{\partial f}{\partial E_\ell}
=-\mathbf{U}^{\mathrm T}\frac{\partial \mathbf{K}}{\partial E_\ell}\mathbf{U}
=-\mathbf{U}^{\mathrm T}\mathbf{k}_\ell\mathbf{U},
\qquad
\frac{\partial f}{\partial V_\ell}=0.
\tag{29}
$$

这意味着，计算目标函数的有限元函数还会返回单元应变能的负值，并将其作为灵敏度向量 $\partial f/\partial \mathbf{E}$。式 (28) 中其余各项取决于具体列式，即设计变量 $\mathbf{z}$ 与分析参数之间的关系。例如，$\mathbf{E}=m_E(\mathbf{Pz})$、$\mathbf{V}=m_V(\mathbf{Pz})$ 意味着

$$
\frac{\partial \mathbf{E}}{\partial \mathbf{z}}
=\mathbf{P}^{\mathrm T}\mathbf{J}_{m_E}(\mathbf{Pz}),
\qquad
\frac{\partial \mathbf{V}}{\partial \mathbf{z}}
=\mathbf{P}^{\mathrm T}\mathbf{J}_{m_V}(\mathbf{Pz}),
\tag{30}
$$

其中，$\mathbf{J}_{m_E}(\mathbf{y}):=\operatorname{diag}\big(m_E'(y_1),\ldots,m_E'(y_N)\big)$ 是映射 $m_E$ 的 Jacobian 矩阵。式 (28) 的计算在分析例程之外完成，所得结果 $\partial g_i/\partial \mathbf{z}$ 被传递给优化器，用于更新设计变量的取值。

正如分析例程应与拓扑优化算法的其余部分相分离一样，负责更新设计变量取值的优化器也应当保持独立。拓扑优化领域对此也许更为熟悉，因为 MMA（Svanberg 1987）之类的优化器通常被当作黑箱例程使用。当然，了解并理解优化器内部的工作机制仍然很重要。Groenwold 和 Etman（2008）指出，在顺序优化算法中，当只有一个约束时，对代价泛函采用某些近似会导出一种优化准则（Optimality-Criteria，OC）型更新表达式。若直接修改 OC 表达式，使之能够适应更一般的列式，例如本文提出的列式，做法可能并不显然。为了处理一般的箱约束（即上下界不再是 0 和 1），需要增加一个中间变量。此外，如果希望采用顺序近似的解释，就应当将柔顺度问题中的体积约束线性化。对于 SIMP，这并不是问题，因为体积泛函关于设计变量本来就是线性的。附录 B 对更新格式作了简要讨论。

# 4 Matlab 实现（Matlab implementation）

本节说明离散拓扑优化问题 (27) 的 Matlab 实现。函数 `PolyTop` 是代码的核心，其中包含优化器和分析例程，包括有限元例程以及负责计算代价泛函及其灵敏度的函数。这个原型用于求解柔顺度最小化问题，不过其中指定了专门的函数来计算目标函数和约束函数。所有把设计变量与分析参数联系起来的拓扑优化参数（例如过滤矩阵和材料插值函数），以及有限元模型（例如网格、载荷和状态方程的支承边界条件），均在 `PolyScript` 中从外部定义；`PolyScript` 是调用该核心函数的 Matlab 脚本。这种功能解耦使用户无需修改核心函数，就可以采用不同的列式或离散方式。插值函数和正则化函数也可以方便地修改，例如可以对惩罚参数或过滤半径采用延拓策略。

## 4.1 输入数据与 PolyScript（Input data and PolyScript）

代码的全部输入参数和内部参数被汇集到两个 Matlab 结构体数组中。其中一个结构体称为 `fem`，包含所有与有限元有关的参数；另一个结构体称为 `opt`，包含与拓扑优化列式和优化器有关的变量。表 1 给出了这些结构体数组中的字段。需要注意的是，如果部分 `fem` 字段尚未指定，则会在 `PolyTop` 核心函数内部填充。由于这些结构体位于 Matlab 工作区中，用户也可以访问所有模型参数。

<center><b>表 1：输入结构体中的字段列表。标有上标 † 的字段若为空，则由 PolyTop 内部填充。</b></center>

| 结构体 | 字段 | 含义 |
|---|---|---|
| `fem` | `fem.NNode` | 节点数 |
| `fem` | `fem.NElem` | 单元数 |
| `fem` | `fem.Node` | $[\text{NNode}\times 2]$ 节点数组 |
| `fem` | `fem.Element` | $[\text{NElem}\times \text{Var}]$ 单元元胞数组 |
| `fem` | `fem.Supp` | $[\text{NSupp}\times 3]$ 支承数组 |
| `fem` | `fem.Load` | $[\text{NLoad}\times 3]$ 载荷数组 |
| `fem` | `fem.Nu0` | 实体材料的 Poisson 比 |
| `fem` | `fem.E0` | 实体材料的 Young 模量 |
| `fem` | `fem.Reg` | 规则网格标记 |
| `fem` | `fem.ElemNDof`$^\dagger$ | 表示各单元自由度数的数组 |
| `fem` | `fem.ShapeFnc`$^\dagger$ | 含离散形函数与权重的元胞数组 |
| `fem` | `fem.k`$^\dagger$ | 局部刚度矩阵条目数组 |
| `fem` | `fem.i`$^\dagger$ | 用于稀疏组装 `fem.k` 的索引数组 |
| `fem` | `fem.j`$^\dagger$ | 用于稀疏组装 `fem.k` 的索引数组 |
| `fem` | `fem.e`$^\dagger$ | 与 `fem.k` 对应的单元编号数组 |
| `fem` | `fem.ElemArea`$^\dagger$ | 单元面积数组 |
| `fem` | `fem.F`$^\dagger$ | 整体载荷向量 |
| `fem` | `fem.FreeDofs`$^\dagger$ | 自由自由度数组 |
| `opt` | `opt.zMin` | 设计变量下界 |
| `opt` | `opt.zMax` | 设计变量上界 |
| `opt` | `opt.zIni` | 设计变量初始数组 |
| `opt` | `opt.MatIntFnc` | 材料插值函数句柄 |
| `opt` | `opt.P` | 将设计变量映射为单元变量的矩阵 |
| `opt` | `opt.VolFrac` | 给定的体积分数约束 |
| `opt` | `opt.Tol` | 设计变量的收敛容差 |
| `opt` | `opt.MaxIter` | 最大优化迭代次数 |
| `opt` | `opt.OCMove` | OC 更新格式中的允许移动步长 |
| `opt` | `opt.OCEta` | OC 更新格式中使用的指数 |

在 `PolyScript` 的代表性实现中，调用辅助函数 `PolyMesher` 和 `PolyFilter`，分别初始化有限元网格和利用输入半径 $R$ 构造线性过滤矩阵 $\mathbf{P}$。多边形网格生成器 `PolyMesher` 已在配套论文（Talischi 等，2011）中介绍。[^11] `PolyFilter` 的实现简短而高效，随补充材料一并提供。为了构造过滤矩阵，该函数只需计算网格中各单元形心之间的距离，并根据输入的过滤半径定义过滤权重（参见式 (23) 和附录 A）。如果过滤半径过小，该函数会返回单位矩阵。也可以有意输入负值来得到单位矩阵。在这种情况下，每个设计变量对应一个单元属性——这在文献中有时被称为“基于单元”的方法；如第 2 节所述，它对应于一个不适定的连续列式，因此毫不意外地会受到网格依赖性的影响。不过，只要棋盘格等数值不稳定现象受到抑制，它也可以用于恢复 Michell 型解。

另一个给出的辅助函数是材料插值函数，其函数句柄通过字段 `opt.MatIntFnc` 传递给核心函数。给定输入向量 $\mathbf{y}$ 后，该函数必须返回与之对应、且长度相同的刚度数组和体积分数数组 $\mathbf{E}=m_E(\mathbf{y})$、$\mathbf{V}=m_V(\mathbf{y})$，以及灵敏度向量 $\partial \mathbf{E}/\partial \mathbf{y}:=m_E'(\mathbf{y})$ 和 $\partial \mathbf{V}/\partial \mathbf{y}:=m_V'(\mathbf{y})$。[^12] 例如，对于 SIMP：

```matlab
function [E,dEdy,V,dVdy] = MatIntFnc(y,penal)
eps = 1e-4;
E = eps+(1-eps)*y.^penal;
V = y;
dEdy = (1-eps)*penal*y.^(penal-1);
dVdy = ones(size(y,1),1);
```

需要注意的是，空洞区域的刚度也可以在这里设定。这再次说明，材料插值模型和 Ersatz 近似均独立于正则化格式的选择和设计变量的上下界。材料插值函数可以接受输入参数（例如 SIMP 中的惩罚指数 `penal`），这样用户便可以根据需要在工作区中修改这些参数（例如用于延拓）。

## 4.2 PolyTop 中各函数的说明（Comments on the functions in PolyTop）

核心函数 `PolyTop` 不足 190 行，其中 116 行与有限元分析有关；这 116 行中有 81 行用于计算多边形单元的单元刚度。本节说明核心函数中各个函数的实现。

**主函数（Main function）**　函数首先初始化迭代参数 `Iter`、`Tol` 和 `Change`，并针对初始猜测 `z=opt.zIni` 初始化分析参数（第 8 行）。第 10 行执行的 `InitialPlot` 函数使用 `patch` 函数绘制网格的三角剖分，并输出图形句柄以及向量 `FigData`，后者将用于更新面片颜色。迭代优化算法嵌套在 `while` 循环中；当超过最大迭代次数 `opt.MaxIter`，或者设计变量的变化量 `Change` 小于给定容差时，循环终止。每次迭代中，$\mathbf{E}$ 和 $\mathbf{V}$ 的当前值被传递给分析函数 `ObjectiveFnc` 和 `ConstraintFnc`，顾名思义，它们分别用于计算目标函数和约束函数的数值与灵敏度（第 14、15 行）。设计变量的灵敏度在第 17、18 行按照式 (28) 和 (30) 计算。需要注意的是，逐项乘积 `dEdy.*dfdE` 与矩阵向量乘积 $\mathbf{J}_{m_E}(\mathbf{y})\,\partial f/\partial \mathbf{E}$ 得到相同的向量，因为 Jacobian 矩阵 $\mathbf{J}_{m_E}(\mathbf{y})$ 是对角矩阵，其对角元素为 `dEdy`。随后，设计灵敏度被传递给 `UpdateScheme`，以获得下一组设计变量向量。新设计对应的分析参数在第 21 行计算。最后，将新的目标函数值和当前迭代中的最大变化量输出到屏幕，并更新图中的单元面片颜色，使之反映更新后的设计。

**FEAnalysis**　在说明负责计算目标函数和约束函数的函数之前，先讨论 `FEAnalysis` 函数中有限元分析的实现，以及其中与拓扑优化有关的特定内容。如前所述，整体刚度矩阵的结构具有如下特征：不仅单元刚度矩阵保持不变，网格的连接关系也保持固定。

Matlab 中整体刚度矩阵的高效组装使用内置函数 `sparse`；该函数利用两个等长的索引数组，由输入数值数组生成稀疏矩阵。为了组装整体刚度矩阵，将所有局部刚度矩阵（对应于基准实体材料的刚度）的条目置于单个向量 `fem.k` 中。[^13] 索引向量 `fem.i` 和 `fem.j` 包含 `fem.k` 中每个条目对应的整体自由度。具体而言，这些向量告诉 `sparse` 函数，应将 `fem.k(q)` 放入整体刚度矩阵的第 `fem.i(q)` 行、第 `fem.j(q)` 列。这些向量在第 69–79 行计算并存储。本文约定第 $n$ 个节点的水平和竖直自由度分别为 $2n-1$ 和 $2n$。按照设计，`sparse` 函数会将具有相同索引的 `fem.k` 条目相加。

为了考虑代表当前设计时需要赋给各单元的不同 $E$ 值，代码还会计算并存储另一个索引向量 `fem.e`。该数组记录 `fem.k` 中各局部刚度矩阵条目所属的单元。因此，表达式 `E(fem.e)` 会返回拉长后的单元刚度列表，其尺寸与索引向量相同。逐项乘积 `E(fem.e).*fem.k` 随后对 `fem.k` 中的局部刚度矩阵值进行适当缩放。因此，整体刚度矩阵通过下面一行代码完成组装：

```matlab
K = sparse(fem.i,fem.j,E(fem.e).*fem.k);
```

第 80–89 行仅在第一次迭代时执行，根据给定的 `Supp` 和 `Load` 矩阵计算自由自由度列表 `fem.FreeDofs` 和整体载荷向量 `fem.F`。[^14] 需要注意的是，在第一次迭代完成初始化之后，`FEAnalysis` 函数只需执行四行代码即可得到节点位移（第 91–94 行）。按照 Andreassen 等（2010）的建议，代码中加入了第 92 行，以确保“反斜杠”求解器将刚度矩阵 $\mathbf{K}$ 识别为对称矩阵，从而缩短线性方程组的求解时间。

**ObjectiveFnc**　该函数利用 $\mathbf{E}$ 和 $\mathbf{V}$ 的当前值计算优化问题的目标函数。还需再次指出，该函数不会获得任何与优化列式有关的信息。在原型实现中，柔顺度通过整体力向量与位移向量的内积直接计算；位移向量在调用 `FEAnalysis` 函数时得到。该函数还返回目标函数关于 $\mathbf{E}$ 和 $\mathbf{V}$ 的灵敏度。对于柔顺度，`dfdV` 是零向量，而 `dfdE` 是由单元应变能的负值构成的数组（参见式 (29)）。由于索引向量 `fem.i`、`fem.j` 和 `fem.k` 包含全部相关有限元信息，可以利用它们高效计算应变能。对于单元 $\Omega_\ell$，需要计算 $-\sum_{i,j}U_i(k_\ell)_{ij}U_j$，其中求和遍历单元 $\Omega_\ell$ 的所有自由度 $i$ 和 $j$。因此，需要对 `-U(fem.i).*fem.k.*U(fem.j)` 中与单元 $\ell$ 对应的块求和。第 30–33 行使用 Matlab 的累积和函数 `cumsum` 完成该计算。

**ConstraintFnc**　该函数计算优化问题的约束函数；对于柔顺度问题，该约束为体积分数约束（参见式 (27)）。与 `FEAnalysis` 的初始化步骤类似，面积向量也只计算一次。第 43–45 行计算该函数的数值以及它关于 $\mathbf{E}$ 和 $\mathbf{V}$ 的灵敏度。

**UpdateScheme**　该函数的输入包括目标函数与约束函数的梯度 `dfdz` 和 `dgdz`、当前设计变量集合 `z0`，以及当前约束函数值 `g`。利用这些信息，可以计算近似约束函数：第 56 行的表达式 `g+dgdz'*(zNew-z0)` 给出候选设计变量处线性化约束函数的值 $g_{\mathrm{app}}(\mathbf{z}^{\mathrm{new}})$。更新格式的实现与附录 B 中的内容一致。代码采用二分法（与 88 行和 99 行代码类似）求解对偶问题。第 49 行将移动限值 $M$ 定义为 `opt.OCMove*(zMax-zMin)`。

**LocalK**　该函数计算等参数多边形单元的局部刚度矩阵。由于多边形形函数是仿射协调的，可以利用这些形函数构造从规则 $n$ 边形（即所谓的“参考”单元）到任意凸多边形的等参数映射。此外，当 $n=3$ 和 $n=4$ 时，所得单元分别与熟知的线性三角形单元和双线性四边形单元一致。该等参数列式的实现及所采用的记号遵循大多数有限元教科书中的标准约定[^15]（例如 Hughes 2000）。

虽然多边形形函数可以得到闭式表达式（参见 Tabarraei 和 Sukumar 2006 的附录），为使代码简洁，本文采用下文所述的、计算成本较高的几何构造。不过，所需量只计算一次，从而消除了重复计算形函数所带来的额外开销。对于等参数单元，只需要参考单元各积分点处的形函数值及其梯度。这一点可以从第 100–110 行计算局部刚度矩阵的求积循环中看出。形函数值和求积权重由函数 `TabShapeFnc` 计算并存储在 `fem.ShapeFnc` 中，具体说明见下文。需要注意的是，这种做法只影响初始化过程中计算单元刚度矩阵的额外开销。

**TabShapeFnc**　该函数填充字段 `fem.ShapeFnc`，其中包含参考单元各积分点处的形函数及其梯度的离散值，以及相应的求积权重。`fem.ShapeFnc` 是长度为 $N_{\max}$ 的元胞数组，其中 $N_{\max}$ 是输入网格中一个单元所具有的最大节点数。第 $n$ 个元胞 `fem.ShapeFnc{n}` 本身是一个结构体数组，包含 `N`、`dNdxi` 和 `W` 三个字段，其值由参考 $n$ 边形得到（见第 115–125 行）。在 `PolyTop` 中，这些形函数值只在第 99、101 行的 `LocalK` 函数中使用。

**PolyShapeFnc**　该函数计算参考 $n$ 边形内部一点 $\boldsymbol{\xi}$ 处的一组线性形函数。与节点 $i$ 对应的 Wachspress 形函数（$1\leq i\leq n$）定义为（Sukumar 和 Tabarraei 2004）：

$$
N_i(\boldsymbol{\xi})
=\frac{\alpha_i(\boldsymbol{\xi})}{\displaystyle\sum_{j=1}^{n}\alpha_j(\boldsymbol{\xi})}.
\tag{31}
$$

其中，$\alpha_i$ 是以下形式的插值函数：[^16]

$$
\alpha_i(\boldsymbol{\xi})
=\frac{A(\mathbf{p}_{i-1},\mathbf{p}_i,\mathbf{p}_{i+1})}
{A(\mathbf{p}_{i-1},\mathbf{p}_i,\boldsymbol{\xi})
A(\mathbf{p}_i,\mathbf{p}_{i+1},\boldsymbol{\xi})}.
$$

这里，$A$ 表示由其自变量确定的三角形面积（见图 4a）。由于参考单元是规则多边形，$A(\mathbf{p}_{i-1},\mathbf{p}_i,\mathbf{p}_{i+1})$ 对所有 $i$ 均相同，因此可以从式 (31) 中约去。采用记号 $A_i(\boldsymbol{\xi}):=A(\mathbf{p}_{i-1},\mathbf{p}_i,\boldsymbol{\xi})$，可以得到如下简化的插值函数表达式：

$$
\alpha_i(\boldsymbol{\xi})
=\frac{1}{A_i(\boldsymbol{\xi})A_{i+1}(\boldsymbol{\xi})}.
\tag{32}
$$

![[Talischi2012_Fig4.png]]

<center><b>图 4：(a) 用于定义式 (32) 中 $\alpha_i$ 的三角形面积示意图；(b) 参考规则多边形的三角剖分，以及定义在各三角形上的积分点。</b></center>

在代码第 131–136 行，利用下式计算由 $\boldsymbol{\xi}$ 和各顶点构成的三角形面积及其关于 $\boldsymbol{\xi}$ 的梯度：

$$
A_i(\boldsymbol{\xi})
=\frac{1}{2}
\begin{vmatrix}
\xi_1 & \xi_2 & 1\\
p_{1,i-1} & p_{2,i-1} & 1\\
p_{1,i} & p_{2,i} & 1
\end{vmatrix},
$$

$$
\frac{\partial A_i}{\partial \xi_1}
=\frac{1}{2}(p_{2,i-1}-p_{2,i}),
\qquad
\frac{\partial A_i}{\partial \xi_2}
=\frac{1}{2}(p_{1,i}-p_{1,i-1}).
$$

插值函数的导数可直接写成（在第 140、141 行计算）

$$
\frac{\partial \alpha_i}{\partial \xi_k}
=-\alpha_i
\left(
\frac{1}{A_i}\frac{\partial A_i}{\partial \xi_k}
+\frac{1}{A_{i+1}}\frac{\partial A_{i+1}}{\partial \xi_k}
\right),
\qquad k=1,2.
$$

由式 (31)，可以得到下列形函数梯度表达式（第 147 行）：

$$
\frac{\partial N_i}{\partial \xi_k}
=\frac{1}{\displaystyle\sum_{j=1}^{n}\alpha_j}
\left(
\frac{\partial \alpha_i}{\partial \xi_k}
-N_i\sum_{j=1}^{n}\frac{\partial \alpha_j}{\partial \xi_k}
\right),
\qquad k=1,2.
$$

**PolyTrnglt**　该函数将参考 $n$ 边形的各顶点与位于其内部的输入点 $\boldsymbol{\xi}$ 相连，生成一个有向三角剖分。如图 4b 所示，参考 $n$ 边形的节点位于 $\mathbf{p}_i=(\cos 2\pi i/n,\sin 2\pi i/n)$。该函数同时用于多边形形函数和求积公式的定义。

**PolyQuad**　在参考 $n$ 边形上进行积分的一种方法，是将其划分为 $n$ 个三角形（连接原点与各顶点），并在每个三角形上使用熟知的求积公式。对于下一节的验证问题，本文在每个三角形上采用三个积分点（见图 4b）。需要指出的是，也可以采用最近为多边形区域专门构造的特殊求积公式（例如 Mousavi 等，2009；Natarajan 等，2009）进行数值积分，这些公式具有更高的精度。

**TriQuad、TriShape**　这两个函数由 `PolyQuad` 调用，分别提供参考三角形上的常用求积公式及其线性形函数。

# 5 数值结果（Numerical results）

本节给出若干基准柔顺度最小化问题的数值结果，以展示代码的通用性。所有结果中，Ersatz 参数均取 $\varepsilon=10^{-4}$，实体相的 Young 模量和 Poisson 比分别取 $E_0=1$ 和 $\nu=0.3$。此外，设计变量变化量的最大容差取为 $1\%$。除非另有说明，`opt.P` 均设为式 (33) 给出的线性过滤矩阵 $\mathbf{P}$，并由辅助函数 `PolyFilter` 计算。

第一个算例是 MBB 梁问题（Olhoff 等，1991），其设计域、载荷和支承条件见图 5a。网格由 `PolyMesher`（Talischi 等，2011）生成，包含 5,000 个多边形单元。图 5b 所示最终结果采用半径为 0.04 的线性过滤器（矩形设计域的高度为 1）以及带延拓的 SIMP 模型得到。惩罚参数 $p$ 从 1 增加到 4，增量为 0.5；对于每一个 $p$ 值，最多允许迭代 150 次（通过设置 `opt.MaxIter=150`）。延拓在 `PolyTop` 核心函数之外的 `PolyScript` 中实现如下：

```matlab
for penal = 1:0.5:4
    opt.MatIntFnc = @(y)MatIntFnc(y,'SIMP',penal);
    [opt.zIni,V,fem] = PolyTop(fem,opt);
end
```

这是补充材料所提供 `PolyScript` 中的默认算例。运行该脚本时（例如，直接在命令提示符中输入 `PolyScript`），程序会调用 `PolyMesher` 生成网格[^17]，定义结构体数组 `fem` 和 `opt`，并在该延拓循环内执行 `PolyTop` 核心函数。

![[Talischi2012_Fig5.png]]

<center><b>图 5：MBB 梁问题。(a) 设计域几何、载荷和边界条件；网格由 5,000 个单元（27 个四边形、1,028 个五边形、3,325 个六边形、618 个七边形和 2 个八边形）以及 9,922 个节点组成；分别采用 (b) SIMP、(c) RAMP、(d) 带 Heaviside 过滤的 SIMP 和 (e) 带 Heaviside 过滤的 RAMP 得到的最终拓扑。</b></center>

若要采用另一种材料插值函数，只需在 `PolyTop` 核心函数之外修改 `MatIntFnc`。例如，图 5c 的结果采用 RAMP 函数（Stolpe 和 Svanberg 2001b；Bendsøe 和 Sigmund 2003）：

$$
m_E(\rho)=\varepsilon+(1-\varepsilon)\frac{\rho}{1+q(1-\rho)},
\qquad
m_V(\rho)=\rho.
$$

参数 $q$ 初始取 0，随后通过从 1 开始不断加倍，延拓至 128。由于采用了相同的过滤半径，两个结果之间的差异体现了这两类插值函数性能上的差异。

Heaviside 投影（Guest 等，2004）是材料插值模型的另一个例子。虽然它通常被看作一种非线性过滤方法，但很容易看出，它可以纳入第 2.5 节所述的、正则化映射为线性的框架。更具体地说，若它与 SIMP 联用，材料插值函数为

$$
m_E(\rho)=\varepsilon+(1-\varepsilon)[h(\rho)]^p,
\qquad
m_V(\rho)=h(\rho),
$$

其中

$$
h(x)=1-\exp(-\beta x)+x\exp(-\beta)
$$

是近似 Heaviside 函数，且 $\rho$ 属于式 (6) 定义的容许设计空间，即 $\rho$ 由通常的线性过滤得到。这说明 Heaviside 过滤本质上等价于对材料插值函数进行修改。附加参数 $\beta$ 控制最优解中出现的灰度量。不过需要注意，SIMP 惩罚起着关键作用，因为当 $p=1$ 时，对于任意 $\rho$ 都有 $m_E(\rho)\approx m_V(\rho)$，因此无论 $\beta$ 多大，最优解都将主要由中间密度组成。也可以用类似方式，基于 RAMP 函数定义 Heaviside 格式的材料插值函数。图 5d 和图 5e 分别给出了采用 SIMP 和 RAMP 的 Heaviside 过滤结果，其中惩罚参数和过滤半径与前述结果相同。此外，$p$ 和 $q$ 的延拓与 $\beta$ 的延拓交替进行：$\beta$ 初始取 1，每次 $p$ 或 $q$ 增大时，$\beta$ 加倍。不出所料，所得结果取决于惩罚参数与 $\beta$ 的延拓方式。

下一组结果对应于具有非平凡设计域几何，或者具有非平凡载荷与支承条件的问题。图 6 和图 7 左列给出了设计域及其边界条件。扳手和悬架三角形问题采用 RAMP 函数求解，吊钩和蛇形梁问题采用 SIMP 插值函数求解，二者均使用前述相同的延拓方案。尽管 99 行和 88 行代码可以利用被动单元指定孔洞位置，但显然，在规则网格上描述此处所示的任意几何会十分繁琐，甚至不可行。此外，为了解析设计域的几何、准确指定设计载荷并计算结构响应，必须采用非结构网格。此类问题通常出现在实际应用中；例如，悬架三角形（见图 6c、6d）是 Allaire 和 Jouve（2005）给出的一个拓扑优化工业应用。

![[Talischi2012_Fig6.png]]

<center><b>图 6：具有非平凡设计域几何的柔顺度问题。(a) 扳手问题的设计域，$R=0.03$，$\bar v=0.4$；(b) 采用 RAMP 函数得到的扳手问题最终拓扑；(c) 悬架三角形问题的设计域，$R=0.25$，$\bar v=0.45$，水平载荷的幅值是竖直载荷的 8 倍；(d) 采用 RAMP 函数得到的悬架问题最终拓扑。</b></center>

![[Talischi2012_Fig7.png]]

<center><b>图 7：具有非平凡设计域几何的柔顺度问题。(a) 蛇形梁问题的设计域，$R=0.25$，$\bar v=0.55$；(b) 采用 SIMP 函数得到的蛇形梁问题最终拓扑；(c) 吊钩问题的设计域，$R=2.0$，$\bar v=0.40$；(d) 采用 SIMP 函数得到的吊钩梁问题最终拓扑。</b></center>

下面说明如何在代码中施加对称性及类似的布局约束。考虑扳手问题，并要求设计关于水平轴对称。利用 `PolyMesher` 生成一个非结构但对称的多边形网格（参见 Talischi 等，2011 的第 6.2 节）。对于 $\ell=1,\ldots,N/2$，单元 $\Omega_{\ell+N/2}$ 是单元 $\Omega_\ell$ 关于水平轴的镜像。如第 2.3 节所述，可以通过式 (11) 中给出的映射 $P_s$ 施加对称性。对于该网格，与 $P_s$ 的离散对应的矩阵（参见式 (23)）定义为

$$
(\mathbf{P}_s)_{\ell k}=
\begin{cases}
1, & \ell=k\ \text{或}\ \ell=k+N/2,\\
0, & \text{其他},
\end{cases}
$$

其中，$\ell=1,\ldots,N$，$k=1,\ldots,N/2$。若还要应用过滤，则将 `opt.P` 设置为

$$
\mathbf{P}=\mathbf{P}_F\mathbf{P}_s,
$$

其中 $\mathbf{P}_F$ 是线性过滤矩阵。图 8 给出了沿水平轴施加对称性之后的最优扳手拓扑。该问题的载荷并不对称，因此施加对称性等价于要求最优设计还能承受相同的向上载荷。可以证明，该对称拓扑与包含一对互为镜像、权重相等的载荷工况的多载荷问题之解相同。

![[Talischi2012_Fig8.png]]

<center><b>图 8：扳手问题的对称解。</b></center>

# 6 效率（Efficiency）

最后，本文讨论代码计算成本的构成，并将其效率与 88 行代码（Andreassen 等，2010）进行比较。为了便于比较，MBB 问题采用规则方形网格求解（关于如何使用 `PolyMesher` 生成此类网格，参见 Talischi 等，2011 的第 6.5 节）。过滤半径取为 $R=0.12$。[^18] 对于 88 行代码，将输入标记 `ft` 设为 2，以使用“一致”的密度过滤器。两种代码中，SIMP 惩罚参数均固定为 $p=3$；在一台配备 Intel(R) Core i7 3.33 GHz 处理器和 24.0 GB RAM、运行 Matlab R2009b 的计算机上，均执行 200 次优化迭代。当然，两种代码在每一步迭代中生成了相同的拓扑。

<center><b>表 2：200 次优化迭代的代码运行时间构成。时间单位为秒，括号内为占 PolyScript 总运行时间的百分比。</b></center>

| 网格尺寸 | $90\times30$ | $150\times50$ | $300\times100$ | $600\times200$ |
|---|---:|---:|---:|---:|
| 计算 $\mathbf{P}$ | 0.25 (1.6%) | 0.876 (2.1%) | 9.12 (4.9%) | 93.79 (9.2%) |
| 填充 `fem` | 0.20 (1.3%) | 0.50 (1.2%) | 2.05 (1.1%) | 8.08 (0.8%) |
| 组装 $\mathbf{K}$ | 5.86 (37.8%) | 16.73 (41.1%) | 69.50 (37.2%) | 289.09 (28.5%) |
| 求解 $\mathbf{KU}=\mathbf{F}$ | 3.56 (23.0%) | 11.64 (28.6%) | 60.06 (32.1%) | 302.95 (29.8%) |
| 映射 $\mathbf{z}$ 与 $\mathbf{E},\mathbf{V}$ | 0.17 (1.1%) | 0.86 (2.1%) | 12.86 (6.9%) | 203.82 (20.1%) |
| 柔顺度灵敏度 | 0.94 (6.1%) | 2.76 (6.8%) | 12.94 (6.9%) | 50.82 (5.0%) |
| 绘制解 | 2.53 (16.3%) | 3.15 (7.7%) | 6.20 (3.3%) | 18.76 (1.8%) |
| OC 更新 | 0.96 (6.2%) | 1.99 (4.9%) | 5.17 (2.8%) | 14.39 (1.4%) |
| `PolyScript` 总时间 | 15.50 | 40.74 | 187.02 | 1,015.89 |

`PolyScript` 的运行时间构成见表 2。可以看到，对于所有网格尺寸，包括填充 `fem` 结构体和计算过滤矩阵在内的初始化时间均不大。在 `PolyTop` 随后的迭代过程中，组装刚度矩阵和求解有限元线性方程组占据了代码运行时间的最大部分。将设计变量 $\mathbf{z}$ 映射为分析量 $\mathbf{E}$ 和 $\mathbf{V}$，以及映射相应分析灵敏度（代码第 14、15、21 行）的相对成本随网格尺寸增大而提高。需要注意的是，这两项操作都涉及与过滤矩阵相乘，因而网格越大，对内存的需求也越高。对于 $600\times200$ 网格，这一增长最为显著，这可能是因为过滤矩阵相对于可用内存而言尺寸很大。

<center><b>表 3：PolyScript 与 88 行代码的运行时间比较（200 次优化迭代的时间，单位为秒）。</b></center>

| 网格尺寸 | $90\times30$ | $150\times50$ | $300\times100$ | $600\times200$ |
|---|---:|---:|---:|---:|
| `PolyScript` 总时间 | 15.5 | **40.7** | **187** | **1,016** |
| 88 行代码总时间 | **14.8** | 44.4 | 360 | 4,463 |

表 3 列出了 `PolyScript` 和 88 行代码的运行时间。可以看到，除最小网格外，本文 Matlab 实现均快于 88 行代码。而且，随着网格尺寸增大，两种代码之间的运行时间差距也随之扩大。这说明问题规模越大，`PolyTop` 的效率相对于 88 行代码越高——需要注意，对于 $600\times200$ 网格，加速超过 4 倍。这一现象促使作者进一步研究差异的来源。

作者注意到，在 88 行代码 OC 更新函数的每一次二分迭代中，设计体积都是通过对候选设计变量乘以过滤矩阵所得到的“物理”密度求和计算的。但该体积函数可以改写为

$$
V(\mathbf{z})
=\sum_{\ell=1}^{N}(\mathbf{Pz})_\ell
=\mathbf{1}^{\mathrm T}(\mathbf{Pz})
=(\mathbf{1}^{\mathrm T}\mathbf{P})\mathbf{z}
=(\mathbf{P}^{\mathrm T}\mathbf{1})^{\mathrm T}\mathbf{z},
$$

其中 $\mathbf{1}$ 是由单位分量组成的长度为 $N$ 的向量。注意，向量 $\mathbf{P}^{\mathrm T}\mathbf{1}$ 只需计算一次，此后 $V$ 的计算就可归结为该向量与 $\mathbf{z}$ 的内积，从而尽量避免在每个二分步骤中执行代价较高的 $\mathbf{P}$ 乘法。尽管上述表达式没有在 `PolyTop` 中显式使用，但将 OC 格式与分析例程解耦会自然地导出这一更高效的计算方式。需要注意的是，$\mathbf{P}^{\mathrm T}\mathbf{1}$ 实际上正是提供给 `PolyTop` 中 `UpdateScheme` 函数的灵敏度向量 `dgdz`。[^19] 更新方程基于如下形式的约束函数 $g(\mathbf{z})$ 线性化（见附录 B）：

$$
g(\mathbf{z})=g(\mathbf{z}_0)
+\left(\frac{\partial g}{\partial \mathbf{z}}\right)^{\mathrm T}
(\mathbf{z}-\mathbf{z}_0),
$$

其中 $\mathbf{z}_0$ 是当前迭代的设计变量。由于体积约束是线性的，该式与体积函数的表达式相同（读者可以验证这两个表达式的等价性）。这一观察也许进一步说明了本文所倡导的解耦思想的价值。

本节最后说明计算多个单元刚度矩阵所产生的额外开销。如前所述，为了与 88 行代码进行比较，`fem.k` 的初始化只计算一次单元刚度矩阵（通过设置 `fem.Reg=1`）。不过，即使不使用 `fem.Reg` 标记，重复计算单元刚度矩阵所产生的成本占总成本的比例也很小。例如，对于 $300\times100$ 四边形网格，这一过程耗时 6.12 秒，仅占 200 次优化迭代总成本的 3.3%。类似地，对于包含 10,000 个单元的多边形网格，计算单元矩阵耗时 8.39 秒，占 200 次优化迭代总成本的 5.8%。

# 7 结论与扩展（Conclusions and extensions）

本文提出了一个在任意设计域上采用非结构多边形有限元网格进行拓扑优化的通用框架，并给出了一个名为 `PolyTop` 的模块化 Matlab 代码。在该代码中，分析例程和优化算法与拓扑优化列式的具体选择相分离。事实上，有限元分析和灵敏度分析例程不包含任何与具体列式有关的信息，因此可以被独立地扩展、维护、开发和／或修改。在配套论文中，作者还提供了一个通用多边形单元网格生成器 `PolyMesher`（Talischi 等，2011），同样采用 Matlab 编写。`PolyMesher` 和 `PolyTop` 使用户能够在任意设计域上求解拓扑优化问题，而不再局限于文献中长期占主导地位的 Cartesian 设计域。作者希望借助这些代码，研究群体能够超越 Cartesian 设计域，探索实际工程问题中常见的一般设计域（见图 6–8）。作者也希望 `PolyTop` 的模块化和灵活性能够推动研究群体将该框架用于本文范围之外的其他问题，例如隐式函数列式、流体拓扑优化等。

# 致谢（Acknowledgments）

前两位作者感谢美国能源部科学办公室和国家核安全管理局（National Nuclear Security Administration）能源部计算科学研究生奖学金计划（Department of Energy Computational Science Graduate Fellowship Program）的资助，合同号为 DE-FG02-97ER25308。后两位作者感谢巴西里约热内卢 PUC-Rio 的 Tecgraf（计算机图形技术组，Group of Technology in Computer Graphics）提供经费支持。

[^11]: 需要注意的是，为了成功调用该函数，应将 `PolyMesher` 文件加入 Matlab 路径。当然，也可以用任何其他网格生成器（例如 distMesh；Persson 和 Strang 2004）替代该网格生成器，只要节点列表、单元连接元胞数组、载荷向量和支承向量采用相同格式即可。

[^12]: 这里仍将 $m_E'(\mathbf{y})$ 和 $m_V'(\mathbf{y})$ 理解为元素分别为 $m_E'(y_\ell)$ 和 $m_V'(y_\ell)$ 的向量。本质上，$m_E'(\mathbf{y})$ 和 $m_V'(\mathbf{y})$ 分别是 Jacobian 矩阵 $\mathbf{J}_{m_E}(\mathbf{y})$ 和 $\mathbf{J}_{m_V}(\mathbf{y})$ 的对角元素。

[^13]: 局部刚度矩阵通过第 68 行或第 70 行调用函数 `LocalK` 获得。如果已知网格均匀，则可在初始化 `fem` 结构体时将 `fem.Reg` 标记设为 1，此时只调用一次 `LocalK`（第 68 行），因而不存在重复计算相同单元刚度矩阵的额外开销。

[^14]: 这些矩阵应采用如下格式：`Supp` 必须有三列，第一列为节点编号，第二列和第三列分别给出该节点在 $x$、$y$ 方向的支承条件。数值 0 表示节点自由，数值 1 表示节点固定。节点载荷向量 `Load` 采用类似结构，但第二列和第三列的数值分别表示力在 $x$、$y$ 方向的分量大小。

[^15]: 关于式 (25) 与熟知的单元刚度矩阵表达式 $\int_{\Omega_\ell}\mathbf{B}^{\mathrm T}\mathbf{D}\mathbf{B}\,\mathrm{d}\mathbf{x}$ 之间的联系，可参见 Hughes（2000）第 2.8 节。

[^16]: 在该表达式中，约定 $\mathbf{p}_{n+1}=\mathbf{p}_1$。

[^17]: 由于 `PolyMesher` 中种子点的随机布置，生成的 Voronoi 网格可能与本文结果采用的网格不同。

[^18]: 过滤半径越大，计算过滤矩阵所需的时间越长，占用的内存也越多。

[^19]: 不过，在 `PolyTop` 中，体积函数由整个设计域的体积进行归一化，且各单元可以具有不同面积（因此 `PolyTop` 中以 $\mathbf{A}$ 代替 $\mathbf{1}$）。此外，约束函数定义为归一化体积与给定体积分数 $\bar v$ 之差。

# 附录 A：线性核的过滤矩阵（Filtering matrix for the linear kernel）

通过在单元形心处对式 (21) 的被积函数采样，可以推导出对应于线性帽形过滤器 (8) 的常用离散过滤公式：

$$
\begin{aligned}
w_{\ell k}
&=\int_{\Omega_k}F\left(\boldsymbol{x}_{\ell}^{*},\bar{\boldsymbol{x}}\right)\,\mathrm{d}\bar{\boldsymbol{x}} \\
&=c\left(\boldsymbol{x}_{\ell}^{*}\right)
\int_{\Omega_k}\max\left(1-\frac{\left\lVert\boldsymbol{x}_{\ell}^{*}-\bar{\boldsymbol{x}}\right\rVert}{R},0\right)\,\mathrm{d}\bar{\boldsymbol{x}} \\
&\approx c\left(\boldsymbol{x}_{\ell}^{*}\right)|\Omega_k|
\max\left(1-\frac{\left\lVert\boldsymbol{x}_{\ell}^{*}-\boldsymbol{x}_{k}^{*}\right\rVert}{R},0\right).
\end{aligned}
$$

若采用类似方式近似定义 $c(\boldsymbol{x}_{\ell}^{*})$ 的积分，并用 $S(\ell)$ 表示形心落在单元 $\Omega_\ell$ 形心半径 $R$ 范围内的单元 $\Omega_k$ 的指标集合，即 $\lVert\boldsymbol{x}_{\ell}^{*}-\boldsymbol{x}_{k}^{*}\rVert\leq R$，则过滤后的场可写为

$$
y_\ell=
\frac{
\displaystyle\sum_{k\in S(\ell)}z_k|\Omega_k|
\left(1-\left\lVert\boldsymbol{x}_{\ell}^{*}-\boldsymbol{x}_{k}^{*}\right\rVert/R\right)
}{
\displaystyle\sum_{k\in S(\ell)}|\Omega_k|
\left(1-\left\lVert\boldsymbol{x}_{\ell}^{*}-\boldsymbol{x}_{k}^{*}\right\rVert/R\right)
},
$$

这就是常用表达式。需要指出的是，由于底层网格通常是均匀的，$|\Omega_k|$ 项经常被省略。再次强调，该表达式的向量形式更适合在 Matlab 中实现。因此，过滤矩阵 $\mathbf{P}$ 定义为

$$
(\mathbf{P})_{\ell k}=
\frac{
\max\left(0,|\Omega_k|\left(1-\left\lVert\boldsymbol{x}_{\ell}^{*}-\boldsymbol{x}_{k}^{*}\right\rVert/R\right)\right)
}{
\displaystyle\sum_{k\in S(\ell)}|\Omega_k|
\left(1-\left\lVert\boldsymbol{x}_{\ell}^{*}-\boldsymbol{x}_{k}^{*}\right\rVert/R\right)
}.
\tag{33}
$$

矩阵 $\mathbf{P}$ 以稀疏矩阵形式存储。下面给出本文算例中用于计算该矩阵的 `PolyFilter` 函数：

```matlab
%----------------------------------------------------------------------------%
function [P] = PolyFilter(fem,R)
if R<0, P = speye(fem.NElem); return; end %P is set to identity when R<0
ElemCtrd = zeros(fem.NElem,2);
for el = 1:fem.NElem             %Compute the centroids of all the elements
  vx=fem.Node(fem.Element{el},1); vy=fem.Node(fem.Element{el},2);
  temp = vx.*vy([2:end 1])-vy.*vx([2:end 1]);
  A = 0.5*sum(temp);
  ElemCtrd(el,1) = 1/(6*A)*sum((vx+vx([2:end 1])).*temp);
  ElemCtrd(el,2) = 1/(6*A)*sum((vy+vy([2:end 1])).*temp);
end
[d] = DistPntSets(ElemCtrd,ElemCtrd,R);  %Obtain distance values & indices
P = sparse(d(:,1),d(:,2),1-d(:,3)/R);   %Assemble the filtering matrix
P = spdiags(1./sum(P,2),0,fem.NElem,fem.NElem)*P;
%-------------------------------- COMPUTE DISTANCE BETWEEN TWO POINT SETS
function [d] = DistPntSets(PS1,PS2,R)
d = cell(size(PS1,1),1);
for el = 1:size(PS1,1)       %Compute the distance information
  dist = sqrt((PS1(el,1)-PS2(:,1)).^2 + (PS1(el,2)-PS2(:,2)).^2);
  [I,J] = find(dist<=R);     %Find the indices for distances less that R
  d{el} = [I,J+(el-1),dist(I)];
end
d = cell2mat(d);             %Matrix of indices and distance value
%----------------------------------------------------------------------------%
```

# 附录 B：更新格式（Update scheme）

结构优化中的一种基本迭代方法，是用当前设计点处的近似来替代目标函数和约束函数。也就是说，每次迭代中求解如下近似问题：

$$
\min_{\boldsymbol{z}} f_{\mathrm{app}}(\boldsymbol{z})
\quad\text{subject to}\quad
g_{\mathrm{app}}(\boldsymbol{z})\leq 0,
\qquad
\boldsymbol{z}\in[\underline{\rho},\overline{\rho}]^N.
\tag{34}
$$

其中，$f_{\mathrm{app}}$ 和 $g_{\mathrm{app}}$ 是式 (27) 中目标函数和约束函数在某些适当且具有合理物理意义的中间变量下，由一阶 Taylor 展开得到的近似。为了获得 OC 类型的更新格式，在指数中间变量

$$
\left(\frac{z_\ell-\underline{\rho}}{\overline{\rho}-\underline{\rho}}\right)^a
$$

中，利用设计变量的当前值 $\boldsymbol{z}=\boldsymbol{z}^0$ 对 $f$ 进行线性化，得到

$$
\begin{aligned}
f_{\mathrm{app}}(\boldsymbol{z})
=f(\boldsymbol{z}^0)
&+\sum_{\ell=1}^{N}
\left.\frac{\partial f}{\partial z_\ell}\right|_{\boldsymbol{z}=\boldsymbol{z}^0}
\frac{1}{a}\left(z_\ell^0-\underline{\rho}\right) \\
&\quad\times
\left[
\left(\frac{z_\ell-\underline{\rho}}{z_\ell^0-\underline{\rho}}\right)^a-1
\right].
\end{aligned}
\tag{35}
$$

约束函数在设计变量下采用线性近似：

$$
g_{\mathrm{app}}(\boldsymbol{z})
=g(\boldsymbol{z}^0)
+\sum_{\ell=1}^{N}
\left.\frac{\partial g}{\partial z_\ell}\right|_{\boldsymbol{z}=\boldsymbol{z}^0}
\left(z_\ell-z_\ell^0\right).
\tag{36}
$$

最优性条件给出了 Lagrange 乘子 $\lambda$ 与各设计变量 $z_\ell$ 之间的关系（这里使用了近似的可分离性）：

$$
\frac{\partial f_{\mathrm{app}}}{\partial z_\ell}
+\lambda\frac{\partial g_{\mathrm{app}}}{\partial z_\ell}=0,
\qquad \ell=1,\ldots,N.
$$

Lagrange 乘子的值可通过求解对偶问题获得，例如采用二分法。[^20]

[^20]: 在“倒数”变量中近似响应相关代价函数的重要意义，即 $a=-1$ 时的情形，可参见 Groenwold and Etman (2008) 及其中所列参考文献。当 $a=1$ 时，恢复通常的 Taylor 线性化。

将式 (35) 和式 (36) 代入上式，可化为

$$
\left(\frac{z_\ell-\underline{\rho}}{z_\ell^0-\underline{\rho}}\right)^{1-a}
=-
\frac{
\left.\dfrac{\partial f}{\partial z_\ell}\right|_{\boldsymbol{z}=\boldsymbol{z}^0}
}{
\lambda\left.\dfrac{\partial g}{\partial z_\ell}\right|_{\boldsymbol{z}=\boldsymbol{z}^0}
}
:=B_\ell.
$$

因此，得到最优 $z_\ell$ 关于 $\lambda$ 的显式表达式，记为 $z_\ell^*$，并将其作为下一次迭代的候选值：

$$
z_\ell^*=\underline{\rho}+(B_\ell)^{\frac{1}{1-a}}
\left(z_\ell^0-\underline{\rho}\right).
\tag{37}
$$

量 $\eta=1/(1-a)$ 有时称为阻尼系数。对于倒数近似，$a=-1$，因而 $\eta=1/2$。这也是柔顺度最小化中通常采用的取值。

由于目标函数和约束函数的近似通常仅在当前设计点 $\boldsymbol{z}^0$ 附近准确，只有候选设计变量落在根据移动限值定义的搜索区域内时才会被接受。此外，还需要确保 $z_\ell^{\mathrm{new}}$ 满足箱式约束。基于这些考虑，将下一设计点定义为

$$
z_\ell^{\mathrm{new}}=
\begin{cases}
z_\ell^+, & z_\ell^*\geq z_\ell^+,\\
z_\ell^-, & z_\ell^*\leq z_\ell^-,\\
z_\ell^*, & \text{其他情形},
\end{cases}
$$

其中，$z_\ell^+$ 和 $z_\ell^-$ 是搜索区域的界，定义为

$$
z_\ell^-=\max\left(\underline{\rho},z_\ell^0-M\right),
$$

$$
z_\ell^+=\min\left(\overline{\rho},z_\ell^0+M\right),
$$

这里 $M$ 是移动限值，取为 $\overline{\rho}-\underline{\rho}$ 的某个固定比例。关于这一推导的更多信息，参见 Groenwold and Etman (2008)。

# 附录 C：PolyScript

```matlab
%-------------------------------- PolyScript --------------------------------%
% Ref: C Talischi, GH Paulino, A Pereira, IFM Menezes, "PolyTop: A Matlab %
% implementation of a general topology optimization framework using         %
% unstructured polygonal finite element meshes", Struct Multidisc Optim,     %
% DOI 10.1007/s00158-011-0696-x                                              %
%----------------------------------------------------------------------------%

%% ------------------------------------------ CREATE 'fem' STRUCT
[Node,Element,Supp,Load] = PolyMesher(@MbbDomain,5000,30);
fem = struct(...
  'NNode',size(Node,1),...       % Number of nodes
  'NElem',size(Element,1),...    % Number of elements
  'Node',Node,...                % [NNode x 2] array of nodes
  'Element',{Element},...        % [NElem x 1] var cell array of elements
  'Supp',Supp,...                % Array of supports
  'Load',Load,...                % Array of loads
  'Nu0',0.3,...                  % Poisson's ratio of solid material
  'E0',1.0,...                   % Young's modulus of solid material
  'Reg',0 ...                    % Tag for regular meshes
  );
%% ------------------------------------------ CREATE 'opt' STRUCT
R = 0.04;
VolFrac = 0.5;
m = @(y)MatIntFnc(y,'SIMP',3);
P = PolyFilter(fem,R);
zIni = VolFrac*ones(size(P,2),1);
opt = struct(...
  'zMin',0.0,...                 % Lower bound for design variables
  'zMax',1.0,...                 % Upper bound for design variables
  'zIni',zIni,...                % Initial design variables
  'MatIntFnc',m,...              % Handle to material interpolation fnc.
  'P',P,...                      % Matrix that maps design to element vars.
  'VolFrac',VolFrac,...          % Specified volume fraction constraint
  'Tol',0.01,...                 % Convergence tolerance on design vars.
  'MaxIter',150,...              % Max. number of optimization iterations
  'OCMove',0.2,...               % Allowable move step in OC update scheme
  'OCEta',0.5 ...                % Exponent used in OC update scheme
  );
%% ------------------------------------------------------ RUN 'PolyTop'
figure;
for penal = 1:0.5:4       %Continuation on the penalty parameter
  disp(['current p: ', num2str(penal)]);
  opt.MatIntFnc = @(y)MatIntFnc(y,'SIMP',penal);
  [opt.zIni,V,fem] = PolyTop(fem,opt);
end
%% --------------------------------------------------------------------------
```

# 附录 D：PolyTop

```matlab
%---------------------------------- PolyTop ----------------------------------%
% Ref: C Talischi, GH Paulino, A Pereira, IFM Menezes, "PolyTop: A Matlab %
% implementation of a general topology optimization framework using         %
% unstructured polygonal finite element meshes", Struct Multidisc Optim,     %
% DOI 10.1007/s00158-011-0696-x                                              %
%----------------------------------------------------------------------------%
function [z,V,fem] = PolyTop(fem,opt)
Iter=0; Tol=opt.Tol*(opt.zMax-opt.zMin); Change=2*Tol; z=opt.zIni; P=opt.P;
[E,dEdy,V,dVdy] = opt.MatIntFnc(P*z);
[FigHandle,FigData] = InitialPlot(fem,V);
while (Iter<opt.MaxIter) && (Change>Tol)
  Iter = Iter + 1;
  %Compute cost functionals and analysis sensitivities
  [f,dfdE,dfdV,fem] = ObjectiveFnc(fem,E,V);
  [g,dgdE,dgdV,fem] = ConstraintFnc(fem,E,V,opt.VolFrac);
  %Compute design sensitivities
  dfdz = P'*(dEdy.*dfdE + dVdy.*dfdV);
  dgdz = P'*(dEdy.*dgdE + dVdy.*dgdV);
  %Update design variable and analysis parameters
  [z,Change] = UpdateScheme(dfdz,g,dgdz,z,opt);
  [E,dEdy,V,dVdy] = opt.MatIntFnc(P*z);
  %Output results
  fprintf('It: %i \t Objective: %1.3f\tChange: %1.3f\n',Iter,f,Change);
  set(FigHandle,'FaceColor','flat','CData',1-V(FigData)); drawnow
end
%------------------------------------------------------- OBJECTIVE FUNCTION
function [f,dfdE,dfdV,fem] = ObjectiveFnc(fem,E,V)
[U,fem] = FEAnalysis(fem,E);
f = dot(fem.F,U);
temp = cumsum(-U(fem.i).*fem.k.*U(fem.j));
temp = temp(cumsum(fem.ElemNDof.^2));
dfdE = [temp(1);temp(2:end)-temp(1:end-1)];
dfdV = zeros(size(V));
%------------------------------------------------------ CONSTRAINT FUNCTION
function [g,dgdE,dgdV,fem] = ConstraintFnc(fem,E,V,VolFrac)
if ~isfield(fem,'ElemArea')
  fem.ElemArea = zeros(fem.NElem,1);
  for el=1:fem.NElem
    vx=fem.Node(fem.Element{el},1); vy=fem.Node(fem.Element{el},2);
    fem.ElemArea(el) = 0.5*sum(vx.*vy([2:end 1])-vy.*vx([2:end 1]));
  end
end
g = sum(fem.ElemArea.*V)/sum(fem.ElemArea)-VolFrac;
dgdE = zeros(size(E));
dgdV = fem.ElemArea/sum(fem.ElemArea);
%------------------------------------------------ OPTIMALITY CRITERIA UPDATE
function [zNew,Change] = UpdateScheme(dfdz,g,dgdz,z0,opt)
zMin=opt.zMin; zMax=opt.zMax;
move=opt.OCMove*(zMax-zMin); eta=opt.OCEta;
l1=0; l2=1e6;
while l2-l1 > 1e-4
  lmid = 0.5*(l1+l2);
  B = -(dfdz./dgdz)/lmid;
  zCnd = zMin+(z0-zMin).*B.^eta;
  zNew = max(max(min(min(zCnd,z0+move),zMax),z0-move),zMin);
  if (g+dgdz'*(zNew-z0)>0),   l1=lmid;
  else                        l2=lmid;  end
end
Change = max(abs(zNew-z0))/(zMax-zMin);
%-------------------------------------------------------------- FE-ANALYSIS
function [U,fem] = FEAnalysis(fem,E)
if ~isfield(fem,'k')
  fem.ElemNDof = 2*cellfun(@length,fem.Element); % # of DOFs per element
  fem.i = zeros(sum(fem.ElemNDof.^2),1);
  fem.j=fem.i; fem.k=fem.i; fem.e=fem.i;
  index = 0;
  if ~isfield(fem,'ShapeFnc'), fem=TabShapeFnc(fem); end
  if fem.Reg, Ke=LocalK(fem,fem.Element{1}); end
  for el = 1:fem.NElem
    if ~fem.Reg, Ke=LocalK(fem,fem.Element{el}); end
    NDof = fem.ElemNDof(el);
    eDof = reshape([2*fem.Element{el}-1;2*fem.Element{el}],NDof,1);
    I=repmat(eDof,1,NDof); J=I';
    fem.i(index+1:index+NDof^2) = I(:);
    fem.j(index+1:index+NDof^2) = J(:);
    fem.k(index+1:index+NDof^2) = Ke(:);
    fem.e(index+1:index+NDof^2) = el;
    index = index + NDof^2;
  end
  NLoad = size(fem.Load,1);
  fem.F = zeros(2*fem.NNode,1);    %external load vector
  fem.F(2*fem.Load(1:NLoad,1)-1) = fem.Load(1:NLoad,2);  %x-crdnt
  fem.F(2*fem.Load(1:NLoad,1))   = fem.Load(1:NLoad,3);  %y-crdnt
  NSupp = size(fem.Supp,1);
  FixedDofs = [fem.Supp(1:NSupp,2).*(2*fem.Supp(1:NSupp,1)-1);
               fem.Supp(1:NSupp,3).*(2*fem.Supp(1:NSupp,1))];
  FixedDofs = FixedDofs(FixedDofs>0);
  AllDofs   = [1:2*fem.NNode];
  fem.FreeDofs = setdiff(AllDofs,FixedDofs);
end
K = sparse(fem.i,fem.j,E(fem.e).*fem.k);
K = (K+K')/2;
U = zeros(2*fem.NNode,1);
U(fem.FreeDofs,:) = K(fem.FreeDofs,fem.FreeDofs)\fem.F(fem.FreeDofs,:);
%-------------------------------------------------- ELEMENT STIFFNESS MATRIX
function [Ke] = LocalK(fem,eNode)
D=fem.E0/(1-fem.Nu0^2)*[1 fem.Nu0 0;fem.Nu0 1 0;0 0 (1-fem.Nu0)/2]; %plane stress
nn=length(eNode); Ke=zeros(2*nn,2*nn);
W = fem.ShapeFnc{nn}.W;
for q = 1:length(W)  %quadrature loop
  dNdxi = fem.ShapeFnc{nn}.dNdxi(:,:,q);
  J0 = fem.Node(eNode,:)'*dNdxi;
  dNdx = dNdxi/J0;
  B = zeros(3,2*nn);
  B(1,1:2:2*nn) = dNdx(:,1)';
  B(2,2:2:2*nn) = dNdx(:,2)';
  B(3,1:2:2*nn) = dNdx(:,2)';
  B(3,2:2:2*nn) = dNdx(:,1)';
  Ke = Ke+B'*D*B*W(q)*det(J0);
end
%-------------------------------------------------- TABULATE SHAPE FUNCTIONS
function fem = TabShapeFnc(fem)
ElemNNode = cellfun(@length,fem.Element); % number of nodes per element
fem.ShapeFnc = cell(max(ElemNNode),1);
for nn = min(ElemNNode):max(ElemNNode)
  [W,Q] = PolyQuad(nn);
  fem.ShapeFnc{nn}.W = W;
  fem.ShapeFnc{nn}.N = zeros(nn,1,size(W,1));
  fem.ShapeFnc{nn}.dNdxi = zeros(nn,2,size(W,1));
  for q = 1:size(W,1)
    [N,dNdxi] = PolyShapeFnc(nn,Q(q,:));
    fem.ShapeFnc{nn}.N(:,:,q) = N;
    fem.ShapeFnc{nn}.dNdxi(:,:,q) = dNdxi;
  end
end
%----------------------------------------------- POLYGONAL SHAPE FUNCTIONS
function [N,dNdxi] = PolyShapeFnc(nn,xi)
N=zeros(nn,1); alpha=zeros(nn,1); dNdxi=zeros(nn,2); dalpha=zeros(nn,2);
sum_alpha=0.0; sum_dalpha=zeros(1,2); A=zeros(nn,1); dA=zeros(nn,2);
[p,Tri] = PolyTrnglt(nn,xi);
for i=1:nn
  sctr = Tri(i,:); pT = p(sctr,:);
  A(i) = 1/2*det([pT,ones(3,1)]);
  dA(i,1) = 1/2*(pT(3,2)-pT(2,2));
  dA(i,2) = 1/2*(pT(2,1)-pT(3,1));
end
A=[A(nn,:);A]; dA=[dA(nn,:);dA];
for i=1:nn
  alpha(i) = 1/(A(i)*A(i+1));
  dalpha(i,1) = -alpha(i)*(dA(i,1)/A(i)+dA(i+1,1)/A(i+1));
  dalpha(i,2) = -alpha(i)*(dA(i,2)/A(i)+dA(i+1,2)/A(i+1));
  sum_alpha = sum_alpha + alpha(i);
  sum_dalpha(1:2) = sum_dalpha(1:2)+dalpha(i,1:2);
end
for i=1:nn
  N(i) = alpha(i)/sum_alpha;
  dNdxi(i,1:2) = (dalpha(i,1:2)-N(i)*sum_dalpha(1:2))/sum_alpha;
end
%----------------------------------------------------- POLYGON TRIANGULATION
function [p,Tri] = PolyTrnglt(nn,xi)
p = [cos(2*pi*(1:nn)/nn); sin(2*pi*(1:nn)/nn)]';
p = [p; xi];
Tri = zeros(nn,3); Tri(1:nn,1)=nn+1;
Tri(1:nn,2)=1:nn; Tri(1:nn,3)=2:nn+1; Tri(nn,3)=1;
%------------------------------------------------------ POLYGONAL QUADRATURE
function [weight,point] = PolyQuad(nn)
[W,Q] = TriQuad;                      %integration pnts & wgts for ref. triangle
[p,Tri] = PolyTrnglt(nn,[0 0]);       %triangulate from origin
point=zeros(nn*length(W),2); weight=zeros(nn*length(W),1);
for k=1:nn
  sctr = Tri(k,:);
  for q=1:length(W)
    [N,dNds] = TriShapeFnc(Q(q,:));   %compute shape functions
    J0 = p(sctr,:)'*dNds;
    l = (k-1)*length(W) + q;
    point(l,:) = N'*p(sctr,:);
    weight(l) = det(J0)*W(q);
  end
end
%---------------------------------------------------- TRIANGULAR QUADRATURE
function [weight,point] = TriQuad
point=[1/6,1/6;2/3,1/6;1/6,2/3]; weight=[1/6,1/6,1/6];
%------------------------------------------------ TRIANGULAR SHAPE FUNCTIONS
function [N,dNds] = TriShapeFnc(s)
N=[1-s(1)-s(2);s(1);s(2)]; dNds=[-1,-1;1,0;0,1];
%----------------------------------------------------------- INITIAL PLOT
function [handle,map] = InitialPlot(fem,z0)
Tri = zeros(length([fem.Element{:}])-2*fem.NElem,3);
map = zeros(size(Tri,1),1); index=0;
for el = 1:fem.NElem
  for enode = 1:length(fem.Element{el})-2
    map(index+1) = el;
    Tri(index+1,:) = fem.Element{el}([1,enode+1,enode+2]);
    index = index + 1;
  end
end
handle = patch('Faces',Tri,'Vertices',fem.Node,'FaceVertexCData',...
               1-z0(map),'FaceColor','flat','EdgeColor','none');
axis equal; axis off; axis tight; colormap(gray);
%----------------------------------------------------------------------------%
```

# 参考文献（References）

参考文献按原文保留。[^译注书目]

Allaire G (2001) Shape optimization by the homogenization method. Springer, Berlin

Allaire G, Francfort GA (1998) Existence of minimizers for non-quasiconvex functionals arising in optimal design. Ann Inst Henri Poincare Anal 15(3):301–339

Allaire G, Jouve F (2005) A level-set method for vibration and multiple loads structural optimization. Comput Methods Appl Mech Eng 194(30–33):3269–3290. doi:10.1016/j.cma.2004.12.018

Allaire G, Jouve F, Toader AM (2004) Structural optimization using sensitivity analysis and a level-set method. J Comput Phys 194(1):363–393. doi:10.1016/j.jcp.2003.09.032

Almeida SRM, Paulino GH, Silva ECN (2010) Layout and material gradation in topology optimization of functionally graded structures: a global-local approach. Struct Multidisc Optim 42(6):885–868. doi:10.1007/s00158-010-0514-x

Ambrosio L, Buttazzo G (1993) An optimal design problem with perimeter penalization. Calc Var Partial Differ Equ 1(1):55–69

Andreassen E, Clausen A, Schevenels M, Lazarov B, Sigmund O (2011) Efficient topology optimization in MATLAB using 88 lines of code. Struct Multidisc Optim 43(1):1–16. doi:10.1007/s00158-010-0594-7

Belytschko T, Xiao SP, Parimi C (2003) Topology optimization with implicit functions and regularization. Int J Numer Methods Eng 57(8):1177–1196. doi:10.1002/nme.824

Bendsoe MP (1989) Optimal design as material distribution problem. Struct Optim 1:193–202. doi:10.1007/BF01650949

Bendsoe MP, Sigmund O (1999) Material interpolation schemes in topology optimization. Arch Appl Mech 69(9–10):635–654

Bendsøe MP, Sigmund O (2003) Topology optimization: theory, methods and applications. Springer, Berlin

Borrvall T (2001) Topology optimization of elastic continua using restriction. Arch Comput Methods Eng 8(4):251–285

Borrvall T, Petersson J (2001) Topology optimization using regularized intermediate density control. Comput Methods Appl Mech Eng 190(37–38):4911–4928

Bourdin B (2001) Filters in topology optimization. Int J Numer Methods Eng 50(9):2143–2158

Bourdin B, Chambolle A (2003) Design-dependent loads in topology optimization. ESAIM, Controle Optim Calc Var 9(2):19–48

Bruns TE (2005) A reevaluation of the simp method with filtering and an alternative formulation for solid-void topology optimization. Struct Multidisc Optim 30(6):428–436. doi:10.1007/s00158-005-0537-x

Bruyneel M, Duysinx P (2005) Note on topology optimization of continuum structures including self-weight. Struct Multidisc Optim 29(4):245–256. doi:10.1007/s00158-004-0484-y

Cherkaev A (2000) Variational methods for structural optimization. Springer, New York

Dambrine M, Kateb D (2009) On the Ersatz material approximation in level-set methods. ESAIM, Controle Optim Calc Var 16(3):618–634. doi:10.1051/cocv/2009023

de Ruiter MJ, Van Keulen F (2004) Topology optimization using a topology description function. Struct Multidisc Optim 26(6):406–416. doi:10.1007/s00158-003-0375-7

Delfour MC, Zolésio JP (2001) Shapes and geometries: analysis, differential calculus, and optimization. Society for Industrial and Applied Mathematics, Philadelphia

Ghosh S (2010) Micromechanical analysis and multi-scale modeling using the Voronoi cell finite element method. In: Computational mechanics and applied analysis. CRC Press, Boca Raton

Groenwold AA, Etman LFP (2008) On the equivalence of optimality criterion and sequential approximate optimization methods in the classical topology layout problem. Int J Numer Methods Eng 73(3):297–316. doi:10.1002/nme.2071

Guest JK, Prevost JH, Belytschko T (2004) Achieving minimum length scale in topology optimization using nodal design variables and projection functions. Int J Numer Methods Eng 61(2):238–254. doi:10.1002/nmc.1064

Haber RB, Jog CS, Bendsoe MP (1996) A new approach to variable-topology shape design using a constraint on perimeter. Struct Optim 11(1):1–12

Hughes TJR (2000) The finite element method: linear static and dynamic finite elemnt analysis. Dover, New York

Kohn RV, Strang G (1986a) Optimal design and relaxation of variational problems I. Commun Pure Appl Math 39(1):113–137

Kohn RV, Strang G (1986b) Optimal design and relaxation of variational problems. II. Commun Pure Appl Math 38(1):139–182

Kohn RV, Strang G (1986c) Optimal design and relaxation of variational problems. III. Commun Pure Appl Math 39:353–377

Kosaka I, Swan CC (1999) A symmetry reduction method for continuum structural topology optimization. Comput Struct 70(1):47–61

Langelaar M (2007) The use of convex uniform honeycomb tessellations in structural topology optimization. In: 7th world congress on structural and multidisciplinary optimization, Seoul, South Korea, May 21–25

Martinez JM (2005) A note on the theoretical convergence properties of the SIMP method. Struct Multidisc Optim 29(4):319–323. doi:10.1007/s00158-004-0479-8

Mousavi SE, Xiao H, Sukumar N (2009) Generalized gaussian quadrature rules on arbitrary polygons. Int J Numer Methods Eng. doi:10.1002/nme.2759

Natarajan S, Bordas SPA, Mahapatra DR (2009) Numerical integration over arbitrary polygonal domains based on Schwarz–Christoffel conformal mapping. Int J Numer Methods Eng. doi:10.1002/nme.2589

Olhoff N, Bendsoe MP, Rasmussen J (1991) On cad-integrated structural topology and design optimization. Comput Methods Appl Mech Eng 89(1–3):259–279

Persson P, Strang G (2004) A simple mesh generator in MATLAB. Siam Rev 46(2):329–345. doi:10.1137/S0036144503429121

Petersson J (1999) Some convergence results in perimeter-controlled topology optimization. Comput Methods Appl Mech Eng 171(1–2):123–140

Rietz A (2001) Sufficiency of a finite exponent in SIMP (power law) methods. Struct Multidisc Optim 21:159–163

Rozvany GIN (2009) A critical review of established methods of structural topology optimization. Struct Multidisc Optim 37(3):217–237. doi:10.1007/s00158-007-0217-0

Rozvany GIN, Zhou M, Birker T (1992) Generalized shape optimization without homogenization. Struct Optim 4(3–4):250–252

Saxena A (2008) A material-mask overlay strategy for continuum topology optimization of compliant mechanisms using honeycomb discretization. J Mech Des 130(8):2304-1-9. doi:10.1115/1.2936891

Sigmund O (2007) Morphology-based black and white filters for topology optimization. Struct Multidisc Optim 33(4–5):401–424. doi:10.1007/s00158-006-0087-x

Sigmund O, Petersson J (1998) Numerical instabilities in topology optimization: a survey on procedures dealing with checkerboards, mesh-dependencies and local minima. Struct Optim 16(1):68–75

Stolpe M, Svanberg K (2001a) On the trajectories of penalization methods for topology optimization. Struct Multidisc Optim 21(2):128–139

Stolpe M, Svanberg K (2001b) An alternative interpolation scheme for minimum compliance topology optimization. Struct Multidisc Optim 22(2):116–124

Stromberg LL, Beghini A, Baker WF, Paulino GH (2011) Application of layout and topology optimization using pattern gradation for the conceptual design of buildings. Struct Multidisc Optim 43(2):165–180. doi:10.1007/s00158-010-0563-1

Sukumar N, Tabarraei A (2004) Conforming polygonal finite elements. Int J Numer Methods Eng 61(12):2045–2066. doi:10.1002/nme.1141

Svanberg K (1987) The method of moving asymptotes—a new method for structural optimization. Int J Numer Methods Eng 24(2):359–373

Tabarraei A, Sukumar N (2006) Application of polygonal finite elements in linear elasticity. Int J Comput Methods 3(4):503–520. doi:10.1142/S021987620600117X

Talischi C, Paulino GH, Le CH (2009) Honeycomb wachspress finite elements for structural topology optimization. Struct Multidisc Optim 37(6):569–583. doi:10.1007/s00158-008-0261-4

Talischi C, Paulino GH, Pereira A, Menezes IFM (2010) Polygonal finite elements for topology optimization: a unifying paradigm. Int J Numer Methods Eng 82(6):671–698. doi:10.1002/nme.2763

Talischi C, Paulino GH, Pereira A, Menezes IFM (2011) PolyMesher: a general-purpose mesh generator for polygonal elements written in Matlab. Struct Multidisc Optim. doi:10.1007/s00158-011-0706-z

Tartar L (2000) An introduction to the homogenization method in optimal design. In: Optimal shape design: lecture notes in mathematics, no. 1740. Springer, Berlin, pp 47–156

Van Dijk NP, Langelaar M, Van Keulen F (2009) A discrete formulation of a discrete level-set method treating multiple constraints. In: 8th World Congress on Structural and Multidisciplinary Optimization, June 1-5, 2009, Lisbon, Portugal

Wang MY, Wang XM, Guo DM (2003) A level set method for structural topology optimization. Comput Methods Appl Mech Eng 192(1–2):227–246

Zhou M, Rozvany GIN (1991) The COC algorithm, part II: topological, geometrical and generalized shape optimization. Comput Methods Appl Mech Eng 89(1–3):309–336

[^译注代码]: 附录中的 MATLAB 代码按原文转录，保留英文注释，未执行验证。

[^译注编号]: 原文此处将式 (12) 与式 (26) 的编号倒置；依照前后定义，连续问题为式 (12)，离散问题为式 (26)。此处保留原句，并作说明。

[^译注书目]: 原文书目中存在疑似笔误，包括页码 `42(6):885–868`、DOI `10.1002/nmc.1064` 及拼写 `finite elemnt analysis`；本译文保留原文，未据推测更改。
