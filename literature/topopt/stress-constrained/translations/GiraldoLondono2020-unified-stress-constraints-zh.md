---
title: "翻译：A unified approach for topology optimization with local stress constraints considering various failure criteria: von Mises, Drucker–Prager, Tresca, Mohr–Coulomb, Bresler–Pister and Willam–Warnke"
tags:
  - translation
  - topology-optimization
  - stress-constraints
status: "read"
date_created: 2026-09-18
date_updated: 2026-09-18
source: "../sources/GiraldoLondono2020-unified-stress-constraints.pdf"
citekey: "GiraldoLondono2020-unified-stress-constraints"
language: "zh-CN"
---

# A unified approach for topology optimization with local stress constraints considering various failure criteria: von Mises, Drucker–Prager, Tresca, Mohr–Coulomb, Bresler–Pister and Willam–Warnke

---

# 信息

- **中文标题**：考虑多种失效准则的局部应力约束拓扑优化统一方法：von Mises、Drucker–Prager、Tresca、Mohr–Coulomb、Bresler–Pister 与 Willam–Warnke
- **作者**：Oliver Giraldo-Londoño; Glaucio H. Paulino
- **单位**：佐治亚理工学院土木与环境工程学院（School of Civil and Environmental Engineering, Georgia Institute of Technology, Atlanta, GA 30332, USA）
- **期刊**：*Proceedings of the Royal Society A: Mathematical, Physical and Engineering Sciences* (Proc. R. Soc. A)
- **卷 / 期 / 文章号**：476 / 2238 / 20190861
- **DOI**：10.1098/rspa.2019.0861
- **收稿 / 接收 / 出版**：2019-12-11 / 2020-05-01 / 2020-05-27
- **题献**：谨以此文纪念 Daniel C. Drucker 教授（1918–2001）
- **通讯作者**：Glaucio H. Paulino (paulino@gatech.edu)

# 摘要

拓扑优化中一个引人入胜但极具挑战性的问题在于：在结构不发生局部材料失效的前提下，寻找能够承受一组给定外加荷载的最轻结构。多数研究通过适用于延性材料的 von Mises 准则来考虑材料失效。为了将应用范围拓展至由多种不同材料构成的结构，本文引入了一种能够表示包括 von Mises、Drucker–Prager、Tresca、Mohr–Coulomb、Bresler–Pister 和 Willam–Warnke 在内的多种经典失效准则的统一屈服函数，并将其用于求解具有局部应力约束的拓扑优化问题。该统一屈服函数不仅能够表示这些经典准则，还为 Tresca 和 Mohr–Coulomb 准则提供了光滑化表征——这一性质在使用基于梯度的优化算法时极为关键。本文框架具备良好的可扩展性，可进一步推广至本研究涉及之外的其他失效准则。我们给出了数值算例，以展示在指定外荷载或设计相关荷载（如自重）作用下，如何依据所选取的失效准则，通过统一屈服函数获得截然不同的优化设计构型。

**关键词**：拓扑优化；应力约束；屈服面；材料失效；增广拉格朗日

---

# 1 引言

鉴于其提供的设计自由度，拓扑优化已成为设计高效且兼具仿生有机形态结构系统的强大计算工具。在拓扑优化领域内，局部应力约束拓扑优化公认为一项极具挑战性的难题，至今仍缺乏一种兼具高效性且适用于大规模工程应用的稳健求解方法。

缺乏此类方法的部分原因在于问题本身的物理与数学本质。首先，为了以符合连续介质力学的方式求解该问题，必须将应力视为**局部量**（local quantity），而在拓扑优化的语境下，这意味着必须施加数量极其庞大的局部应力约束以防止局部材料破坏 [1]。其次，已知应力约束优化问题的解往往位于维度小于整个解空间的退化奇异区域内（即所谓的应力奇异性现象）。由于这种退化性，传统的优化算法往往无法深入到这些奇异区域内部，从而导致收敛至次优设计 [2–6]。

文献中已提出多种方法来求解应力约束拓扑优化问题，其中大部分基于**约束聚合技术**（constraint aggregation techniques）[7–19]。在这些方法中，局部应力约束通过全局应力函数（如 Kreisselmeier–Steinhauser 函数 [20] 或 $p$-范数函数 [21]）进行聚合，用以逼近整个设计域或局部子区域内的最大应力。全局应力函数虽然估计了设计域内的最大应力，但其逼近精度严重依赖于被聚合的约束数量以及聚合函数的特定参数。因此，聚合后优化问题的解与原始局部约束问题的解之间存在不可忽视的差异。除了约束聚合之外，也有其他路线被用于求解应力约束拓扑优化，在此不再赘述完整文献综述，读者可参阅 Senhora 等 [22] 及其参考文献以获取关于应力约束文献的全面回顾。

本文用于求解局部应力约束拓扑优化问题的方法基于**增广拉格朗日（Augmented Lagrangian, AL）方法** [23, 24]。该方法是一种数值优化技术，它将含有局部约束的原始优化问题转化为一系列无约束（或仅含简单箱式界限约束）子问题的求解序列。理论与数值上均已证明，即使对于具有退化约束的问题，AL 方法也具备全局收敛性质 [25, 26]。AL 方法在拓扑优化界日益受到重视，自 2000 年代中期以来已被用于求解应力约束拓扑优化问题 [27, 28]。近年来，该方法也被引入到基于水平集（level-set）方法的应力约束拓扑优化中 [29–31]。在基于变密度的拓扑优化背景下，AL 方法同样被用于考虑荷载不确定性 [32] 或制造不确定性 [33, 34] 的应力约束拓扑优化问题。尽管前景广阔，但这些现有方法在使用 AL 方法时均未进行任何形式的归一化以消除网格依赖性，这不利于大规模拓扑优化问题的求解。

为了能够求解超大规模问题，Senhora 等 [22] 提出了一种用于局部应力约束质量最小化拓扑优化的**归一化 AL 方法**。为了使该方法能够有效求解大规模问题，他们对 AL 目标函数进行了修正，使得惩罚项相对于约束总数进行了**归一化**，从而防止了罚项随着局部应力约束数目的增加而发生无界爆炸式增长。AL 函数的归一化使得该算法成功求解了包含超过一百万个局部应力约束的大规模问题。具备如此优异可扩展性的方法能够真正使拓扑优化成为工程实际设计的实用工具，因此我们在本项研究中采纳了这一归一化框架。

与 Senhora 等 [22] 的工作类似，应力约束文献中的绝大多数研究均采用 **von Mises 失效准则** [35] 来表征材料破坏。虽然 von Mises 准则在预测金属等延性材料的失效时非常有效，但基于该准则的应力设计并不适用于采用其他类型材料制造的结构，特别是那些具有拉压异性强度（抗拉强度与抗压强度不同）的材料，如混凝土、岩石、土壤、复合材料、聚合物以及多孔发泡材料等。在少数考虑非 von Mises 应力约束的研究中，绝大多数基于 Drucker–Prager 准则（例如 [36–39]）。除 Drucker–Prager 准则外，Duysinx 等 [40] 考虑了考虑拉压强度差异的 Raghava [41] 与 Ishai [42] 失效准则。其他学者如 Jeong 等 [43] 与 Yoon [44] 则考察了包括 Tresca [45]、von Mises [35]、Drucker–Prager [46] 与 Mohr–Coulomb [47] 在内的多种失效准则，并将其应用于应力约束拓扑优化。

在本项研究中，我们证明了多种经典失效准则——包括 von Mises [35]、Drucker–Prager [46]、Tresca [45]、Mohr–Coulomb [47]、Bresler–Pister [48] 以及 Willam–Warnke [49]——均可以由一个单一的屈服函数来统一表征，我们将其命名为**统一屈服函数（unified yield function）**。我们利用该统一屈服函数定义了一类通用的应力约束，用于预测各种不同材料的破坏，并将其应用于求解具有局部应力约束的质量最小化拓扑优化问题。除局部应力约束外，本构型公式还考虑了**自重（self-weight）效应**；当外加机械荷载的量级与结构自身重量相当或相对较小时，自重效应对优化构型具有决定性的显著影响。为了求解具有庞大局部约束的问题，我们采用了基于归一化 AL 的求解框架。得益于该应力约束的通用性，我们的提法覆盖了从延性金属到岩石、混凝土、土壤及聚合物泡沫等极其宽广的工程材料谱系。

本论文的构思深受 Daniel C. Drucker 教授在应用力学领域的先驱性贡献所启发，特别是他在塑性力学理论方面的开创性奠基工作 [46, 50–57]。他的开创性研究为面向工程实际应用的塑性理论奠定了基石。我们在拓扑优化中的公式构建深受他在该领域基础工作的启发，特别是著名的 Drucker–Prager 屈服准则 [46]。

本文其余部分的结构组织如下：在第 2 节中，我们讨论上述经典屈服函数，为统一屈服函数的推导奠定基础；在第 3 节中，我们详细推导并给出统一屈服函数的显式表达；第 4 节介绍局部应力约束拓扑优化提法；第 5 节给出数值算例结果；第 6 节总结全文结论。此外，附录 A 给出灵敏度分析的完整推导细节，附录 B 给出由统一屈服函数表征的各个经典屈服准则参数汇总。

---

# 2 经典屈服函数

我们讨论工程文献中用于预测各种工程材料失效的最常用屈服准则。这些讨论将为我们推导用于统一表征所有这些失效准则的统一屈服函数奠定基础。

传统上，屈服面（yield surface）通常表示为应力张量不变量的函数：
$$
f(I_1, J_2, J_3) = 0
\tag{2.1}
$$
或者表示为主应力的函数：
$$
f(\sigma_1, \sigma_2, \sigma_3) = 0
\tag{2.2}
$$
其中，Cauchy 应力张量 $\boldsymbol{\sigma}$ 的第一不变量以及偏应力张量 $\boldsymbol{s}$ 的第二、第三不变量分别定义为：
$$
I_1 = \mathrm{tr}(\boldsymbol{\sigma}), \quad J_2 = \frac{1}{2}\boldsymbol{s}:\boldsymbol{s}, \quad J_3 = \det(\boldsymbol{s})
\tag{2.3}
$$
偏应力张量 $\boldsymbol{s}$ 为：
$$
\boldsymbol{s} = \boldsymbol{\sigma} - \frac{I_1}{3}\boldsymbol{I}
\tag{2.4}
$$
其中 $\boldsymbol{I}$ 为二阶单位张量。

不失一般性，由式 (2.1) 或式 (2.2) 描述的屈服面均可写为无量纲的**规范化形式（normalized form）**：
$$
\Lambda = \sigma_{\mathrm{eq}} - 1 = 0
\tag{2.5}
$$
其中 $\sigma_{\mathrm{eq}}$ 是一个（无量纲的）**等效应力测度（equivalent stress measure）**，它既可以由应力不变量定义，也可以由主应力定义。这种屈服函数的书写形式直接引出了我们在拓扑优化中对局部应力约束的泛化。正如后文所讨论的，许多最常用的工程屈服准则的等效应力测度均可以写为如下的通用形式：
$$
\sigma_{\mathrm{eq}} = \alpha(\theta)\sqrt{3J_2} + G(I_1)
\tag{2.6}
$$
其中 $\alpha(\theta)$ 是关于 **Lode 角（Lode angle）** $\theta$ [58] 的函数：
$$
\theta = \frac{1}{3}\arcsin\left( -\frac{3\sqrt{3}}{2}\frac{J_3}{J_2^{3/2}} \right), \quad -\frac{\pi}{6} \leq \theta \leq \frac{\pi}{6}
\tag{2.7}
$$
而 $G(I_1)$ 是关于第一应力不变量 $I_1$ 的函数。函数 $\alpha(\theta)$ 用于定义偏应力平面（deviatoric plane，即八面体平面）上屈服面的截面形状，而 $G(I_1)$ 用于定义三轴应力状态对应于 $\theta = -\pi/6$ 时屈服面的经线截面（meridional section）形状。

## 2.1 (a) von Mises 与 Drucker–Prager 准则

首先讨论直接由应力不变量定义的 von Mises 与 Drucker–Prager 准则。von Mises 准则广泛用于预测金属等延性材料的失效，而 Drucker–Prager 准则通常用于预测土壤、岩石或混凝土等压力相关（pressure-dependent）材料的破坏。

von Mises 屈服准则假设当第二偏应力不变量达到临界值时材料发生塑性屈服，其数学形式为：
$$
f(J_2) = \sqrt{3J_2} - \sigma_{\mathrm{lim}} = 0
\tag{2.8}
$$
其规范化形式为：
$$
\Lambda(J_2) = \alpha\sqrt{3J_2} - 1 = 0
\tag{2.9}
$$
其中：
$$
\alpha = \frac{1}{\sigma_{\mathrm{lim}}}
\tag{2.10}
$$
此处 $\sigma_{\mathrm{lim}}$ 为材料的屈服极限强度。将式 (2.9) 与规范化屈服面定义 (2.5) 对比可知，von Mises 屈服准则的等效应力测度为：
$$
\sigma_{\mathrm{eq}} = \alpha\sqrt{3J_2}
\tag{2.11}
$$

Drucker–Prager 屈服准则 [46] 不仅依赖于第二偏应力不变量，而且依赖于第一应力不变量（即它是一个流体静力压相关的模型）。采用式 (2.5) 的形式，Drucker–Prager 屈服面写为规范化形式：
$$
\Lambda(I_1, J_2) = \alpha\sqrt{3J_2} + \beta I_1 - 1 = 0
\tag{2.12}
$$
其中：
$$
\alpha = \frac{\sigma_c + \sigma_t}{2\sigma_c\sigma_t}, \quad \beta = \frac{\sigma_c - \sigma_t}{2\sigma_c\sigma_t}
\tag{2.13}
$$
式中 $\sigma_c$ 与 $\sigma_t$ 分别为材料的单轴抗压强度与单轴抗拉强度。当 $\sigma_c = \sigma_t = \sigma_{\mathrm{lim}}$ 时，式 (2.13) 中的参数退化为 $\alpha = 1/\sigma_{\mathrm{lim}}$ 且 $\beta = 0$，这意味着当材料的拉伸与压缩强度相同时，Drucker–Prager 模型完全退化为 von Mises 模型。对比式 (2.12) 与式 (2.5) 可知，Drucker–Prager 准则的等效应力测度为：
$$
\sigma_{\mathrm{eq}} = \alpha\sqrt{3J_2} + \beta I_1
\tag{2.14}
$$
注意到 von Mises 准则（式 2.11）与 Drucker–Prager 准则（式 2.14）的等效应力测度均完全满足式 (2.6) 给出的通用形式。

## 2.2 (b) Tresca 与 Mohr–Coulomb 准则

以主应力形式表达的 Tresca 与 Mohr–Coulomb 准则，分别对应于 von Mises 与 Drucker–Prager 准则的非光滑（分段线性六棱柱/六棱锥）版本。假设三个主应力按降序排列，即 $\sigma_1 \geq \sigma_2 \geq \sigma_3$，则 Tresca 准则的规范化屈服面为：
$$
\Lambda(\sigma_1, \sigma_2, \sigma_3) = \alpha(\sigma_1 - \sigma_3) - 1 = 0
\tag{2.15}
$$
Mohr–Coulomb 准则的规范化屈服面为：
$$
\Lambda(\sigma_1, \sigma_2, \sigma_3) = \alpha(\sigma_1 - \sigma_3) + \beta(\sigma_1 + \sigma_3) - 1 = 0
\tag{2.16}
$$
其中式 (2.15) 中的 $\alpha$ 由式 (2.10) 给出，式 (2.16) 中的 $\alpha$ 与 $\beta$ 由式 (2.13) 给出[^1]。

[^1]: 这里选取 $\alpha$ 与 $\beta$ 的取值，使得 Mohr–Coulomb 模型与 Drucker–Prager 模型在单轴拉伸与单轴压缩下预测出完全相同的破坏强度。

从上述主应力表达式来看，它们的等效应力测度并不显见地具有式 (2.6) 的函数形式。为了获得期望的统一函数形式，我们将 Tresca 与 Mohr–Coulomb 准则改用应力不变量表达。为此，借助以下经典主应力与应力不变量之间的转换关系 [59]：
$$
\begin{bmatrix}
\sigma_1 \\
\sigma_2 \\
\sigma_3
\end{bmatrix}
= \frac{2}{\sqrt{3}}\sqrt{J_2}
\begin{bmatrix}
\sin\left(\theta + \frac{2\pi}{3}\right) \\
\sin(\theta) \\
\sin\left(\theta - \frac{2\pi}{3}\right)
\end{bmatrix}
+ \frac{I_1}{3}
\begin{bmatrix}
1 \\
1 \\
1
\end{bmatrix}
\tag{2.17}
$$
鉴于 Tresca 准则是 Mohr–Coulomb 准则在 $\beta = 0$ 时的特例，以下仅给出 Mohr–Coulomb 模型的推导。将式 (2.17) 代入式 (2.16)，可整理出如下等效应力测度：
$$
\sigma_{\mathrm{eq}} = \hat{\alpha}(\theta)\sqrt{3J_2} + \hat{\beta}I_1
\tag{2.18}
$$
其中：
$$
\hat{\alpha}(\theta) = \frac{2}{3}\left(\sqrt{3}\alpha\cos\theta - \beta\sin\theta\right), \quad \hat{\beta} = \frac{2}{3}\beta
\tag{2.19}
$$
基于后续统一表征的需要，我们将 $\hat{\alpha}(\theta)$ 重写为如下形式：
$$
\hat{\alpha}(\theta) = \frac{2\alpha}{3}\sqrt{3 + (\beta/\alpha)^2}\cos(\theta + \tilde{\theta}), \quad \text{其中 } \tan\tilde{\theta} = \frac{\beta}{\alpha\sqrt{3}}
\tag{2.20}
$$
显而易见，Tresca 与 Mohr–Coulomb 模型的等效应力测度同样严格遵循式 (2.6) 的通用结构。

众所周知，这两个失效准则包含非微区域（偏应力平面上的六边形棱角尖点），这在使用基于梯度的优化算法时会导致数值振荡与梯度不连续困难。克服该问题的一种经典方法是对偏应力平面上六边形的顶点进行圆角光滑化。根据 Lagioia & Panteghini [60] 的研究，顶点的圆角化可以通过引入如下修正 Lode 角来实现：
$$
\hat{\theta} = \frac{1}{3}\arcsin(\zeta \sin 3\theta)
\tag{2.21}
$$
其中 $\zeta \leq 1$ 为圆角参数。当 $\zeta = 1$ 时，$\hat{\theta} = \theta$，严格恢复原始的 Tresca 与 Mohr–Coulomb 准则；而当 $\zeta < 1$ 时，即可获得偏应力平面上光滑化后的屈服面。

## 2.3 (c) Bresler–Pister 准则

常用于预测混凝土、聚丙烯及聚合物发泡材料等各向同性材料失效的另一经典准则是 Bresler–Pister 屈服准则 [48]。在规范化形式下，Bresler–Pister 屈服面表示为：
$$
\Lambda(I_1, J_2) = \alpha_{\mathrm{BP}}\sqrt{3J_2} + \beta_{\mathrm{BP}}I_1 + \gamma_{\mathrm{BP}}I_1^2 - 1 = 0
\tag{2.22}
$$
其对应的等效应力测度为：
$$
\sigma_{\mathrm{eq}} = \alpha_{\mathrm{BP}}\sqrt{3J_2} + \beta_{\mathrm{BP}}I_1 + \gamma_{\mathrm{BP}}I_1^2
\tag{2.23}
$$
其中参数为：
$$
\left.
\begin{aligned}
\alpha_{\mathrm{BP}} &= \frac{(\sigma_c + \sigma_t)(2 - \sigma_c/\sigma_b)(2 + \sigma_t/\sigma_b)}{\sigma_c\sigma_t(8 - 3\sigma_c/\sigma_b + \sigma_t/\sigma_b)} \\
\beta_{\mathrm{BP}} &= \frac{(\sigma_c - \sigma_t)\left(4 - \sigma_c/\sigma_b - \sigma_t/\sigma_b + \sigma_c\sigma_t/\sigma_b^2\right)}{\sigma_c\sigma_t(8 - 3\sigma_c/\sigma_b + \sigma_t/\sigma_b)} \\
\gamma_{\mathrm{BP}} &= \frac{\sigma_c - 3\sigma_t + 2\sigma_c\sigma_t/\sigma_b}{\sigma_c\sigma_t\sigma_b(8 - 3\sigma_c/\sigma_b + \sigma_t/\sigma_b)}
\end{aligned}
\right\}
\tag{2.24}
$$
式中参数 $\sigma_c, \sigma_t$ 与 $\sigma_b$ 分别为材料的单轴抗压强度、单轴抗拉强度以及**等双轴抗压强度（equibiaxial compressive strength）**。当 $\sigma_b \to \infty$ 时，Bresler–Pister 准则严格退化为 Drucker–Prager 准则。这是因为当 $\sigma_b \to \infty$ 时，$\alpha_{\mathrm{BP}} \to (\sigma_c + \sigma_t)/(2\sigma_c\sigma_t)$，$\beta_{\mathrm{BP}} \to (\sigma_c - \sigma_t)/(2\sigma_c\sigma_t)$，且 $\gamma_{\mathrm{BP}} \to 0$；将其代入式 (2.23) 即可完全得到式 (2.14) 的 Drucker–Prager 等效应力测度。

## 2.4 (d) Willam–Warnke 准则

除 Bresler–Pister 准则外，Willam–Warnke 准则 [49] 也被广泛用于预测混凝土及其他粘结摩擦材料的三轴破坏。Willam–Warnke 模型的规范化屈服面为：
$$
\Lambda(I_1, J_2, \theta) = \frac{1}{\sigma_c}\sqrt{\frac{2}{15}}\frac{1}{r(\theta)}\sqrt{3J_2} + \beta_W I_1 - 1 = 0
\tag{2.25}
$$
其对应的等效应力测度为：
$$
\sigma_{\mathrm{eq}} = \frac{1}{\sigma_c}\sqrt{\frac{2}{15}}\frac{1}{r(\theta)}\sqrt{3J_2} + \beta_W I_1
\tag{2.26}
$$
其中函数 $r(\theta)$ 由下式给出：
$$
r(\theta) = \frac{u(\theta) + v(\theta)}{w(\theta)}
\tag{2.27}
$$
式中：
$$
\left.
\begin{aligned}
u(\theta) &= 2r_c(r_c^2 - r_t^2)\cos(\theta + \pi/6) \\
v(\theta) &= r_c(2r_t - r_c)\sqrt{4(r_c^2 - r_t^2)\cos^2(\theta + \pi/6) + 5r_t^2 - 4r_t r_c} \\
w(\theta) &= 4(r_c^2 - r_t^2)\cos^2(\theta + \pi/6) + (r_c - 2r_t)^2
\end{aligned}
\right\}
\tag{2.28}
$$
参数 $r_c$ 与 $r_t$ 分别表示为：
$$
r_c = \sqrt{\frac{6}{5}}\frac{\sigma_b\sigma_t}{3\sigma_b\sigma_t + \sigma_c(\sigma_b - \sigma_t)}, \quad r_t = \sqrt{\frac{6}{5}}\frac{\sigma_b\sigma_t}{\sigma_c(2\sigma_b + \sigma_t)}
\tag{2.29}
$$
参数 $\beta_W$ 给出为：
$$
\beta_W = \frac{\sigma_b - \sigma_t}{3\sigma_b\sigma_t}
\tag{2.30}
$$
Willam–Warnke 屈服面的凸性条件要求 $r_t > r_c/2$。

式 (2.26) 中乘在 $\sqrt{3J_2}$ 前面的项 $\frac{1}{\sigma_c}\sqrt{\frac{2}{15}}\frac{1}{r(\theta)}$ 可以重新化简写为：
$$
\alpha(\theta) = \frac{A_W \cos^2(\theta + \pi/6) + B_W}{C_W \cos(\theta + \pi/6) + \sqrt{D_W \cos^2(\theta + \pi/6) + E_W}}
\tag{2.31}
$$
其中系数为：
$$
\left.
\begin{aligned}
A_W &= \frac{4}{\sigma_c}\sqrt{\frac{2}{15}}(r_c^2 - r_t^2), \quad B_W = \frac{1}{\sigma_c}\sqrt{\frac{2}{15}}(r_c - 2r_t)^2, \quad C_W = 2r_c(r_c^2 - r_t^2) \\
D_W &= 4r_c^2(r_c - 2r_t)^2(r_c^2 - r_t^2), \quad E_W = r_c^2(r_c - 2r_t)^2(5r_t^2 - 4r_t r_c)
\end{aligned}
\right\}
\tag{2.32}
$$

若取 $A_W \neq 0, C_W = 1$，且 $B_W = D_W = E_W = 0$，上式中的 $\alpha(\theta)$ 退化为 $\alpha(\theta) = A_W \cos(\theta + \pi/6)$，这与式 (2.20) 中推导出的 Tresca 与 Mohr–Coulomb 准则的 $\hat{\alpha}(\theta)$ 函数形式惊人地相似。同样地，若取 $A_W = C_W = D_W = 0, E_W = 1$ 且 $B_W \neq 0$，则 $\alpha(\theta)$ 退化为常数 $\alpha(\theta) = B_W = \text{const}$，这正是 von Mises、Drucker–Prager 和 Bresler–Pister 准则的情形。这一深刻观察为我们构建包含上述所有失效准则的广义 $\alpha(\theta)$ 通用函数形式提供了关键指引。

---

# 3 统一屈服函数

上一节讨论的所有失效准则的等效应力测度均满足式 (2.6) 给出的通用形式。具体而言，数学结果表明所有这些准则均可由关于 $I_1$ 的二次多项式经线函数 $G(I_1)$ 以及具有与式 (2.31) 类似结构的偏应力函数 $\alpha(\theta)$ 来表征。因此，我们将上述所有经典模型统一为一个单一的屈服函数（采用式 2.5 的规范化形式），其等效应力测度定义为[^2]：
$$
\sigma_{\mathrm{eq}} = \hat{\alpha}(\theta)\sqrt{3J_2} + \hat{\beta}I_1 + \hat{\gamma}I_1^2
\tag{3.1}
$$
其中偏应力函数 $\hat{\alpha}(\theta)$ 表达为：
$$
\hat{\alpha}(\theta) = \frac{A\cos^2\hat{\theta} + B}{C\cos\hat{\theta} + \sqrt{D\cos^2\hat{\theta} + E}}
\tag{3.2}
$$
修正 Lode 角 $\hat{\theta}$ 表达为：
$$
\hat{\theta} = \frac{1}{3}\arcsin\left[\zeta\sin 3\theta\right] + \bar{\theta}, \quad \zeta \leq 1
\tag{3.3}
$$

[^2]: 这里引入的统一屈服函数还可以进一步推广以容纳其他非关联塑性与岩土准则，如 Lade–Duncan [61] 与 Matsuoka–Nakai [62] 准则。

通过合理选取式 (3.1)–(3.3) 中的参数，即可精确重现前述各个经典屈服准则。表 1 汇总了对应于各准则的统一参数取值。

<center><b>
表 1：定义统一等效应力测度的参数汇总（式 3.1–3.3）
</b></center>

| 失效准则 | $A$ | $B$ | $C$ | $D$ | $E$ | $\zeta$ | $\bar{\theta}$ | $\hat{\beta}$ | $\hat{\gamma}$ |
|---|---|---|---|---|---|---|---|---|---|
| von Mises | $0$ | $\frac{1}{\sigma_{\mathrm{lim}}}$ | $0$ | $0$ | $1$ | $1$ | $0$ | $0$ | $0$ |
| Drucker–Prager | $0$ | $\frac{\sigma_c + \sigma_t}{2\sigma_c\sigma_t}$ | $0$ | $0$ | $1$ | $1$ | $0$ | $\frac{\sigma_c - \sigma_t}{2\sigma_c\sigma_t}$ | $0$ |
| Tresca | $\frac{2}{\sqrt{3}\sigma_{\mathrm{lim}}}$ | $0$ | $1$ | $0$ | $0$ | $\leq 1$[^a] | $0$ | $0$ | $0$ |
| Mohr–Coulomb | $A_{\mathrm{MC}}$[^b] | $0$ | $1$ | $0$ | $0$ | $\leq 1$[^a] | $\tilde{\theta}$ | $\frac{\sigma_c - \sigma_t}{3\sigma_c\sigma_t}$ | $0$ |
| Bresler–Pister | $0$ | $\alpha_{\mathrm{BP}}$[^c] | $0$ | $0$ | $1$ | $1$ | $0$ | $\beta_{\mathrm{BP}}$[^c] | $\gamma_{\mathrm{BP}}$[^c] |
| Willam–Warnke | $A_W$[^d] | $B_W$[^d] | $C_W$[^d] | $D_W$[^d] | $E_W$[^d] | $1$ | $\frac{\pi}{6}$ | $\frac{\sigma_b - \sigma_t}{3\sigma_b\sigma_t}$ | $0$ |

[^a]: 取 $\zeta < 1$ 可使偏应力平面上的六棱柱/六棱锥顶点获得圆角光滑化 [60]。
[^b]: $A_{\mathrm{MC}} = \frac{2\alpha}{3}\sqrt{3 + (\beta/\alpha)^2}$，其中 $\alpha$ 与 $\beta$ 由式 (2.13) 给出，$\tilde{\theta}$ 由式 (2.20) 给出。
[^c]: $\alpha_{\mathrm{BP}}, \beta_{\mathrm{BP}}$ 与 $\gamma_{\mathrm{BP}}$ 由式 (2.24) 给出。
[^d]: $A_W, B_W, C_W, D_W$ 与 $E_W$ 由式 (2.32) 给出。

如图 1 所示，我们利用式 (3.1) 与表 1 中的参数绘制了本文讨论的各个经典准则在主应力空间中的三维屈服面。

![[GiraldoLondono2020_Fig1.png]]

<center><b>
图 1：由规范化屈服函数 (2.5) 与统一等效应力测度 (3.1)–(3.3) 生成的三维屈服面：(a) von Mises, (b) Drucker–Prager, (c) Tresca, (d) Mohr–Coulomb, (e) Bresler–Pister, (f) Willam–Warnke。绘制参数对应表 1，取 $\sigma_{\mathrm{lim}} = 1, \sigma_t = 0.5, \sigma_c = 1, \sigma_b = 1.25$，且 Tresca 与 Mohr–Coulomb 取 $\zeta = 0.99$。
</b></center>

从图 1 可以观察到，统一屈服函数没有对 Drucker–Prager、Mohr–Coulomb、Bresler–Pister 和 Willam–Warnke 模型的顶角顶点（apex）进行光滑化；在结构受到纯静水拉伸荷载的情况下，这可能会给拓扑优化带来困难。虽然可以采用例如 Abbo & Sloan [63] 的双曲线逼近方法对锥顶顶点进行光滑化，但由于这种情况仅在极其特殊的静水拉压应力状态下才会发生，因此我们在本研究中未引入顶点平滑。

如前所述，对 Tresca 或 Mohr–Coulomb 模型设置 $\zeta < 1$ 会导致偏应力平面上的六边形顶点被光滑圆角化。图 2 展示了圆角参数 $\zeta$ 对式 (3.3) 计算出的修正 Lode 角 $\hat{\theta}$ 的影响，以及它对 Tresca 屈服面顶点圆角化的几何平滑效果。

![[GiraldoLondono2020_Fig2.png]]

<center><b>
图 2：(a) 当 $\bar{\theta} = 0$ 时，不同圆角参数 $\zeta$ 下由式 (3.3) 计算的修正 Lode 角 $\hat{\theta}$。(b, c) 圆角参数使得在 $\theta = \pm\pi/6$ 处满足 $\mathrm{d}\hat{\theta}/\mathrm{d}\theta = 0$，从而为 Tresca 与 Mohr–Coulomb 模型形成光滑屈服面。(d–f) 分别取 $\zeta = 1, 0.9$ 和 $0.5$ 时 Tresca 屈服面的圆角平滑效果。
</b></center>

这些结果表明，在 $\theta = \pm\pi/6$ 处导数 $\mathrm{d}\hat{\theta}/\mathrm{d}\theta = 0$，这保证了偏应力曲线上棱角点的光滑过渡；随着 $\zeta$ 的减小，Tresca 屈服面的截面逐渐变得平滑圆润，并在极限下逼近具有圆形横截面的圆柱面（von Mises 准则）。

---

# 4 拓扑优化提法

本节给出基于上述统一屈服函数的局部应力约束拓扑优化的通用理论框架。该提法旨在寻找能够在承受外加荷载时不发生局部材料失效的最轻结构。为确保不发生材料失效，我们在整个设计域 $\Omega$ 内的 $K$ 个评估点处施加局部应力约束 $g_j$。施加局部约束是为了使提法与经典连续介质力学保持一致，后者严格将应力定义为一个局部物理量 [64]。在连续统设定下，拓扑优化问题表述为：
$$
\left.
\begin{aligned}
\inf_{\rho \in \mathcal{A}} \quad & m(\rho) \\
\text{s.t.} \quad & g_j(\rho, \boldsymbol{u}) \leq 0, \quad j = 1, \ldots, K
\end{aligned}
\right\}
\tag{4.1}
$$
其中 $m(\rho)$ 是结构相对于设计域 $\Omega$ 总质量（体积）的归一化质量，其根据密度场 $\rho$ 定义为：
$$
m(\rho) = \frac{1}{|\Omega|}\int_{\Omega} m_V(\rho)\,\mathrm{d}x
\tag{4.2}
$$
式中 $|\Omega|$ 为设计域的总质量（体积），$m_V(\rho)$ 为体积插值函数，它将点 $x \in \Omega$ 处的密度 $\rho$ 与该点处的体积分数关联起来。在本研究中，我们采用**阈值投影函数（threshold projection function）**定义体积插值 [65]：
$$
m_V(\rho) = \frac{\tanh(\beta\eta) + \tanh(\beta(\rho - \eta))}{\tanh(\beta\eta) + \tanh(\beta(1 - \eta))}
\tag{4.3}
$$
其中 $\beta$ 控制投影的陡峭程度（aggressiveness），$\eta$ 为阈值，密度值高于 $\eta$ 的点被投影为 1，低于 $\eta$ 的点被投影为 0。图 3 绘制了 $\eta = 0.5$ 时不同 $\beta$ 取值下的阈值投影函数曲线。

![[GiraldoLondono2020_Fig3.png]]

<center><b>
图 3：取 $\eta = 0.5$ 时不同 $\beta$ 取值下的阈值投影函数 (4.3)。随着 $\beta$ 增大，高于 $\eta$ 的密度被投影为 1，低于 $\eta$ 的密度被投影为 0。
</b></center>

为了保证拓扑优化问题具有良好的数学适定性（消除棋盘格与网格依赖性），我们将密度场限制在容许密度函数空间 $\mathcal{A}$ 内：
$$
\mathcal{A} = \left\{ P_F(z) : z \in L^{\infty}(\Omega; [0, 1]) \right\}
\tag{4.4}
$$
该空间由正则化卷积滤波算子定义：
$$
P_F(z)(x) = \int_{\Omega} F(x, \bar{x})z(\bar{x})\,\mathrm{d}\bar{x}
\tag{4.5}
$$
其中非线性滤波核算子为：
$$
F(x, \bar{x}) = c(x)\left[\max\left(1 - \frac{\|x - \bar{x}\|_2}{R}, 0\right)\right]^q
\tag{4.6}
$$
式中归一化常数 $c(x)$ 满足 $\int_{\Omega}F(x, \bar{x})\,\mathrm{d}\bar{x} = 1$，$R$ 为滤波半径，$\|x - \bar{x}\|_2$ 为点 $x$ 与 $\bar{x}$ 之间的欧氏距离，$q \geq 1$ 为非线性滤波指数[^3]。

[^3]: 在此亦可使用线性帽子滤波（$q=1$）或高斯滤波等其他滤波算子。

局部应力约束 $g_j(\rho, \boldsymbol{u})$ 依赖于物理密度场 $\rho$ 以及非线性弹性变分问题的解 $\boldsymbol{u} \in \mathcal{V}$[^4]：
$$
\boldsymbol{u} = \inf_{\boldsymbol{u}}\left[ \Pi(\rho, \boldsymbol{u}) + \frac{\epsilon}{2}\boldsymbol{u}\cdot\boldsymbol{u} \right]
\tag{4.7}
$$
其中 $\epsilon$ 为 Tikhonov 正则化因子 [66–68]，容许位移空间为：
$$
\mathcal{V} = \left\{ \boldsymbol{u} \in H^1(\Omega, \mathbb{R}^3) : \boldsymbol{u}|_{\Gamma_D} = \boldsymbol{0} \right\}
\tag{4.8}
$$

[^4]: 在变分问题 (4.7) 中加入 Tikhonov 正则化项 $\frac{\epsilon}{2}\boldsymbol{u}\cdot\boldsymbol{u}$，是为了防止密度趋于零时总刚度矩阵发生奇异 [66–68]。数值实现中取 $\epsilon = 10^{-10}\mathrm{mean}[\mathrm{diag}(\boldsymbol{K}_T)]$，其中 $\boldsymbol{K}_T$ 为刚度矩阵。

系统的总势能泛函表示为：
$$
\Pi(\rho, \boldsymbol{u}) = \int_{\Omega} m_E(\rho)W_0(\boldsymbol{u}, x)\,\mathrm{d}\Omega - \int_{\Omega} m_V(\rho)\boldsymbol{b}\cdot\boldsymbol{u}\,\mathrm{d}\Omega - \int_{\Gamma_t}\boldsymbol{t}\cdot\boldsymbol{u}\,\mathrm{d}S
\tag{4.9}
$$
其中 $m_E(\rho)$ 为刚度插值函数，$W_0(\boldsymbol{u}, x)$ 为实体基体材料的应变能密度，$\boldsymbol{b}$ 为 $\rho = 1$ 时的体力向量（如重力），$\boldsymbol{t}$ 为施加在面力边界 $\Gamma_t$ 上的面力向量。Dirichlet 边界 $\Gamma_D$ 与 Neumann 边界 $\Gamma_t$ 构成边界 $\partial\Omega$ 的划分（$\Gamma_D \cup \Gamma_t = \partial\Omega, \Gamma_D \cap \Gamma_t = \emptyset$）。

在本研究中，我们采用以下两种刚度插值函数：
$$
m_E(\rho) = \tilde{\rho}^p \quad (\text{SIMP}), \qquad m_E(\rho) = \frac{\tilde{\rho}}{1 + p_0(1 - \tilde{\rho})} \quad (\text{RAMP})
\tag{4.10}
$$
其中 $\tilde{\rho} = m_V(\rho)$ 为投影后的物理体积分数，$p \geq 1$ 为 SIMP 惩罚指数，$p_0 \geq 0$ 为 RAMP 惩罚参数。**在不考虑自重的问题中我们采用 SIMP 插值 [69–71]；在考虑自重的问题中我们必须采用 RAMP 插值 [72]**。这是因为在考虑自重时，如果使用 SIMP 模型，当 $\rho \to 0$ 时重力与刚度的比值将趋于无穷大，从而导致低密度空洞单元处发生数值位移发散不稳定性 [73]；这一类数值不稳定性在应力约束拓扑优化中同样屡见不鲜 [18]。

平衡条件 (4.7) 适用于具有任意应变能密度 $W_0$ 的材料。为了将本文核心聚焦于统一屈服函数，我们考虑线弹性材料：
$$
W_0 = \frac{1}{2}\varepsilon_{ij}C_{ijkl}\varepsilon_{kl}
\tag{4.11}
$$
其中 $\varepsilon_{ij}$ 为小应变张量，$C_{ijkl}$ 为线性各向同性弹性张量。

为了对优化问题 (4.1) 进行数值求解，我们将位移场和密度场进行有限元离散。将设计域 $\Omega$ 剖分为单元 $\Omega_e, e=1,\ldots,N_e$；并在每个单元 $\Omega_e$ 内假定常数单元设计密度 $z_e$。由此，离散化的拓扑优化问题表述为：
$$
\left.
\begin{aligned}
\min_{\boldsymbol{z}} \quad & m(\boldsymbol{z}) = \frac{1}{|\Omega|}\sum_{e=1}^{N_e} \tilde{\rho}_e v_e \\
\text{s.t.} \quad & g_j(\boldsymbol{z}, \boldsymbol{u}) \leq 0, \quad j = 1, \ldots, N_c \\
& 0 \leq z_e \leq 1, \quad e = 1, \ldots, N_e \\
\text{with:} \quad & \boldsymbol{u}(\boldsymbol{z}) = \arg\min_{\boldsymbol{u}}\left[ \Pi(\boldsymbol{z}, \boldsymbol{u}) + \frac{\epsilon}{2}\boldsymbol{u}^{\mathsf T}\boldsymbol{u} \right]
\end{aligned}
\right\}
\tag{4.12}
$$
式中 $\boldsymbol{z}$ 为设计变量向量，$\tilde{\rho}_e = m_V(\rho_e)$ 为单元 $e$ 的体积分数，$v_e = |\Omega_e|$ 为实体单元体积。滤波后的密度向量表示为：
$$
\boldsymbol{\rho}(\boldsymbol{z}) = \boldsymbol{P}\boldsymbol{z}
\tag{4.13}
$$
滤波矩阵 $\boldsymbol{P}$ 的分量由式 (4.6) 离散给出：
$$
P_{ij} = \frac{w_{ij}v_j}{\sum_{k=1}^{N_e} w_{ik}v_k}, \quad w_{ij} = \left[\max\left(1 - \frac{\|x_i - x_j\|_2}{R}, 0\right)\right]^q
\tag{4.14}
$$
总势能离散为：
$$
\Pi(\boldsymbol{z}, \boldsymbol{u}) = \sum_{e=1}^{N_e} \int_{\Omega_e} m_E(\rho_e)W_0(\boldsymbol{u}_e)\,\mathrm{d}\Omega - \boldsymbol{f}_{\mathrm{ext}}^{\mathsf T}\boldsymbol{u}
\tag{4.16}
$$
外力向量 $\boldsymbol{f}_{\mathrm{ext}} = \boldsymbol{f}_n + \boldsymbol{f}_b$ 由节点外荷载 $\boldsymbol{f}_n$ 与重力体力向量 $\boldsymbol{f}_b$ 组成：
$$
\boldsymbol{f}_n^e = \int_{\Gamma_t^e} \boldsymbol{N}_e^{\mathsf T}\boldsymbol{t}\,\mathrm{d}S, \quad \boldsymbol{f}_b^e = \int_{\Omega_e} m_V(\rho_e)\boldsymbol{N}_e^{\mathsf T}\boldsymbol{b}\,\mathrm{d}\Omega
\tag{4.18}
$$
其中 $\boldsymbol{N}_e$ 为单元形函数，$\boldsymbol{b} = \gamma\hat{\boldsymbol{n}}$ 为体力向量，$\gamma$ 为实体材料容重，$\hat{\boldsymbol{n}}$ 为重力方向单位向量（如 $\hat{\boldsymbol{n}} = [0, 0, -1]^{\mathsf T}$）。式 (4.18) 中 $m_V(\rho_e)$ 项显式表明体力外载直接依赖于设计变量。

## 4.1 (a) 多项式消失约束

我们引入一种新型应力约束形式，称之为**多项式消失约束（polynomial vanishing constraint）**。该约束是对拓扑优化中传统消失约束（vanishing constraint）的变体拓展，定义为：
$$
g_j(\boldsymbol{z}, \boldsymbol{u}) = m_E(\rho_j)\Lambda_j\left(\Lambda_j^2 + 1\right), \quad \text{其中 } \Lambda_j = \sigma_{\mathrm{eq}, j} - 1
\tag{4.19}
$$
其中 $\sigma_{\mathrm{eq}, j}$ 是在评估点 $x_j$ 处由统一屈服函数 (3.1)–(3.3) 计算得到的无量纲等效应力测度。在本研究中，我们在每个有限单元的形心处设置一个应力评估点（$N_c = N_e$）。

使用多项式消失约束 (4.19) 具有两项突出的理论与数值优势：
1. **大超应力区域的立方加速收敛**：当 $\sigma_{\mathrm{eq}, j} \gg 1$（应力严重超标）时，约束由三次项支配，即 $g_j(\boldsymbol{z}, \boldsymbol{u}) \propto (\sigma_{\mathrm{eq}, j} - 1)^3$。因此，优化器会施加强烈惩罚，迅速将设计驱向整体低应力分布状态，极大加速应力约束的满足过程；
2. **活跃状态附近的局部渐近自洽**：当约束接近激活状态（即 $\sigma_{\mathrm{eq}, j} \to 1, \Lambda_j \to 0$）时，三次项衰减消失，约束退化为由线性项支配，即表现为经典消失约束的行为 [75]，保持了理论上的良定收敛性。

## 4.2 (b) 归一化增广拉格朗日方法

我们采用 AL 方法求解优化问题 (4.12)。在传统 AL 方法中 [23, 24]，原始约束优化问题被转化为一系列无约束子问题。在第 $k$ 步 AL 迭代中，需求解如下 AL 目标函数的极小值：
$$
\mathcal{J}^{(k)}(\boldsymbol{z}) = \frac{1}{|\Omega|}\sum_{e=1}^{N_e}\tilde{\rho}_e v_e + \sum_{j=1}^{N_c}\left[\lambda_j^{(k)}h_j(\boldsymbol{z}, \boldsymbol{u}) + \frac{\mu^{(k)}}{2}h_j(\boldsymbol{z}, \boldsymbol{u})^2\right]
\tag{4.20}
$$
其中：
$$
h_j(\boldsymbol{z}, \boldsymbol{u}) = \max\left[g_j(\boldsymbol{z}, \boldsymbol{u}), -\frac{\lambda_j^{(k)}}{\mu^{(k)}}\right], \quad \forall j = 1, \ldots, N_c
\tag{4.21}
$$
式中 $\lambda_j^{(k)}$ 为 Lagrange 乘子估计值，$\mu^{(k)}$ 为罚因子 [22]。乘子与罚因子的逐代更新格式为：
$$
\lambda_j^{(k+1)} = \lambda_j^{(k)} + \mu^{(k)}h_j\left(\boldsymbol{z}^{(k)}, \boldsymbol{u}\right), \quad \forall j = 1, \ldots, N_c
\tag{4.22}
$$
$$
\mu^{(k+1)} = \min\left[\alpha_{\mu}\mu^{(k)}, \mu_{\max}\right]
\tag{4.23}
$$
其中 $\alpha_{\mu} > 1$ 为罚因子增长参数，$\mu_{\max}$ 为上限截断值，以防止优化步中出现数值病态。

我们的工程实践表明，随着有限元网格的加密（即应力约束数 $N_c$ 达到数十万甚至百万级时），式 (4.20) 中第二项惩罚项的数值将完全压倒第一项体积目标函数，从而严重破坏优化算法的平衡收敛性。为了使 AL 方法能够求解具有任意海量约束的问题，我们**将 AL 函数的罚项相对于约束数目进行归一化**（除以 $N_c$）[22]。这一关键修正彻底消除了网格规模对优化平衡态的病态干扰：
$$
\mathcal{J}^{(k)}(\boldsymbol{z}) = \frac{1}{|\Omega|}\sum_{e=1}^{N_e}\tilde{\rho}_e v_e + \frac{1}{N_c}\sum_{j=1}^{N_c}\left[\lambda_j^{(k)}h_j(\boldsymbol{z}, \boldsymbol{u}) + \frac{\mu^{(k)}}{2}h_j(\boldsymbol{z}, \boldsymbol{u})^2\right]
\tag{4.24}
$$
在每个 AL 外步迭代中，我们运行若干步内部 MMA 迭代（通常 $N_{\mathrm{MMA}} = 5$）来近似求解归一化函数 (4.24) 的极小值。灵敏度分析推导详见附录 A。

---

# 5 数值算例

我们给出两个典型的三维数值算例，以展示统一屈服函数处理各种不同失效准则的能力，并研究自重效应对优化拓扑构型的深刻影响。除非另有说明，优化中统一采用表 2 所列的通用算法参数。

<center><b>
表 2：数值算例通用的输入参数汇总
</b></center>

| 参数 | 说明 | 取值 |
|---|---|---|
| $\lambda_j^{(0)}$ | 初始 Lagrange 乘子估计值 | $0$ |
| $\mu^{(0)}$ | 初始罚因子 | $10$ |
| $\mu_{\max}$ | 最大罚因子上限 | $10\,000$ |
| $\alpha_{\mu}$ | 罚因子更新增长参数 | $1.05$ |
| $p$ | SIMP 惩罚因子（无自重算例） | $3$ |
| $p_0$ | RAMP 惩罚因子（含自重算例） | $3.5$ |
| $q$ | 非线性滤波指数 | $3$ |
| $N_{\mathrm{MMA}}$ | 每个 AL 步内的 MMA 内迭代步数 | $5$ |
| $\beta^{(0)}$ | 初始阈值投影参数（每 5 个 AL 步增加 0.5，上限 15） | $1$ |
| $\eta$ | 阈值投影密度界限 | $0.5$ |
| $\boldsymbol{z}^{(0)}$ | 初始均匀设计密度初值 | $0.5$ |
| $tol$ | 算法收敛容差（满足 $\sum|z_e^{(k+1)} - z_e^{(k)}| < tol$ 且 $\max(g_j) < 0.005$ 时停机） | $0.0015$ |

金属材料取弹性模量 $E = 200\text{ GPa}$，泊松比 $\nu = 0.3$，屈服强度 $\sigma_{\mathrm{lim}} = 250\text{ MPa}$；类混凝土材料取 $E = 30\text{ GPa}, \nu = 0.2$。

## 5.1 (a) 牛腿设计 (Corbel design)

本算例研究失效准则类型对三维牛腿结构拓扑优化构型的影响，几何外形如图 4 所示。设计域尺寸由 $L = 1\text{ m}, t = 0.5\text{ m}$ 确定，外加集中力 $P$ 沿宽度方向均布在 $d = 0.05\text{ m}$ 的条带区域上。根据材料强度不同，施加荷载大小相应调整：对于延性金属（von Mises 与 Tresca），施加荷载取 $P = 10\,000\text{ kN}$；对于水泥基胶凝材料，施加荷载取 $P = 600\text{ kN}$。材料属性与荷载汇总见表 3。本算例忽略结构自重影响，设计域采用 250,000 个规则六面体单元离散。

![[GiraldoLondono2020_Fig4.png]]

<center><b>
图 4：牛腿问题的几何尺寸与荷载条件。几何由 $L = 1\text{ m}, t = 0.5\text{ m}$ 定义，荷载 $P$ 在 $d = 0.05\text{ m}$ 范围内均匀分布。
</b></center>

<center><b>
表 3：求解牛腿问题所采用的材料属性与荷载大小
</b></center>

| 失效准则 | $E$ (GPa) | $\nu$ | $\sigma_{\mathrm{lim}}$ (MPa) | $\sigma_t$ (MPa) | $\sigma_c$ (MPa) | $\sigma_b$ (MPa) | 荷载 $P$ (kN) |
|---|---|---|---|---|---|---|---|
| von Mises 与 Tresca | $200$ | $0.3$ | $250$ | — | — | — | $10\,000$ |
| Drucker–Prager 与 Mohr–Coulomb | $30$ | $0.2$ | — | $10.5$ | $35$ | — | $600$ |
| Bresler–Pister 与 Willam–Warnke | $30$ | $0.2$ | — | $10.5$ | $35$ | $52.5$ | $600$ |

图 5 给出了各失效准则下的拓扑优化最终构型与等效应力分布。

![[GiraldoLondono2020_Fig5.png]]

<center><b>
图 5：牛腿问题在统一失效准则下的优化拓扑构型（左）与等效应力分布（右）：(a) von Mises, (b) Tresca, (c) Drucker–Prager, (d) Mohr–Coulomb, (e) Bresler–Pister, (f) Willam–Warnke。
</b></center>

图 5a, b 分别对应 von Mises 与 Tresca 准则。在这两个准则中，静水压力对失效没有影响，优化构型呈现高度对称的传力杆系结构。而图 5c–f 分别对应 Drucker–Prager、Mohr–Coulomb、Bresler–Pister 和 Willam–Warnke 准则；在这些准则中，静水应力分量不可忽略，从而打破了结构的对称性。在这些非对称构型中，受拉杆件明显粗于受压杆件；这是由于类混凝土材料的抗压强度（$35\text{ MPa}$）显著高于抗拉强度（$10.5\text{ MPa}$），受拉区需要分布更多材料来满足更苛刻的抗拉应力约束。

尤其值得注意的是，对于 Drucker–Prager 准则（图 5c），在负静水应力区域（如底部凹角受压处），构型出现了明显的**颈缩（necking）现象**。这是因为根据 Drucker–Prager 准则，在纯静水压缩应力下材料理论上永不发生失效，因此优化器在强静水压区域无需布置大量材料。此外，图 5c–f 中的所有非对称构型均共享一个共同特征：顶部凹角处由一根粗大的受拉构件横跨，而受压构件则在底部凹角处汇交。

图 5b, d 中采用的圆角参数为 $\zeta = 0.99$。为了探讨圆角参数 $\zeta$ 对优化结果的影响，图 6 对比了 $\zeta = 0.95$ 与 $\zeta = 0.50$ 时 Tresca 准则下的优化拓扑。

![[GiraldoLondono2020_Fig6.png]]

<center><b>
图 6：不同圆角参数下的优化拓扑（左）、主应力空间内的光滑 Tresca 屈服面（中）以及偏应力平面上的八面体投影剖面（右）：(a) $\zeta = 0.95$, (b) $\zeta = 0.50$。
</b></center>

结果显示，优化构型受 $\zeta$ 取值的影响微乎其微；且无论 $\zeta$ 取何值，结构内所有应力评估点均严格收敛在圆角屈服面的内部，证明局部应力约束得到了严格满足。

## 5.2 (b) 穹顶设计 (Dome design)

本算例研究自重效应对三维空间结构优化构型的决定性影响，几何模型如图 7 所示。盒形设计域边长 $L = 10\text{ m}$，高度为 $L/4 = 2.5\text{ m}$，在中心半径 $r = 0.25\text{ m}$ 的圆形区域施加垂直荷载 $P$，底部四角由 $d = 1\text{ m}$ 的刚性方形垫片支承。我们考虑两种失效准则：金属材料的 von Mises 准则与类混凝土材料的 Willam–Warnke 准则（$\sigma_t = 7\text{ MPa}, \sigma_c = 35\text{ MPa}, \sigma_b = 52.5\text{ MPa}$）。同样采用 250,000 个单元离散。

![[GiraldoLondono2020_Fig7.png]]

<center><b>
图 7：穹顶问题的几何尺寸与支承荷载条件。
</b></center>

为了量化外载荷与结构自重的相对影响，我们定义外加荷载 $P$ 与实体初始设计域总自重 $W = \gamma L^3/4$ 的比值 $P/W$。我们考察四个典型的比值：$P/W = -0.1$（向上提拉）、$P/W = 0.01$（自重起主导控制作用）、$P/W = 1$（外载与自重相当）以及 $P/W = \infty$（忽略自重）。为了保证构型之间的可比性，在不同 $P/W$ 下通过调整荷载 $P$ 使得最终构型具有相似的体积分数，荷载取值见表 4。

<center><b>
表 4：获得图 8 与图 9 优化拓扑所施加的荷载大小 $P$（$\times 10^3\text{ kN}$）
</b></center>

| 失效准则 | $P/W = -0.1$ | $P/W = 0.01$ | $P/W = 1$ | $P/W = \infty$ |
|---|---|---|---|---|
| von Mises | $-177$ | $39$ | $195$ | $195$ |
| Willam–Warnke | $-10.4$ | $6$ | $30$ | $30$ |

图 8 展示了 von Mises 准则下的优化结果。

![[GiraldoLondono2020_Fig8.png]]

<center><b>
图 8：von Mises 准则下不同 $P/W$ 比值的穹顶拓扑构型（左）与等效应力分布（右）：(a) $P/W = -0.1$, (b) $P/W = 0.01$, (c) $P/W = 1$, (d) $P/W = \infty$。
</b></center>

当 $P/W = -0.1$（图 8a）时，外力向上提拉，优化构型在受力点正下方形成一个实体配重块，以自身的重力来抵消向上的拉力，从而降低整体传递到支座处的反力。当 $P/W = 0.01$（图 8b）时，自重效应占绝对主导，构型演化为通过内部桁架结构将中心荷载传递到外围拱形构件的复合体系。当 $P/W = 1$ 与 $\infty$（图 8c, d）时，自重影响退居次要，构型趋向于由四根直接连接支座与加载点的倾斜压杆组成的简洁空间桁架。

图 9 展示了类混凝土材料在 Willam–Warnke 准则下的优化构型。

![[GiraldoLondono2020_Fig9.png]]

<center><b>
图 9：Willam–Warnke 准则下不同 $P/W$ 比值的穹顶拓扑构型（左）与等效应力分布（右）：(a) $P/W = -0.1$, (b) $P/W = 0.01$, (c) $P/W = 1$, (d) $P/W = \infty$。
</b></center>

由于类混凝土材料极其抗拉薄弱，当 $P/W = -0.1$（图 9a）时，为了防止加载点由于拉伸应力过大而发生脆性破坏，我们将荷载作用半径由 $r = 0.25\text{ m}$ 增大到 $r = 0.66\text{ m}$。在自重占主导的 $P/W = 0.01$（图 9b）工况下，Willam–Warnke 准则演化出两道相互正交且在跨中交汇的**纯压双拱体系**。与金属体系（图 8b 含有受拉撑杆）完全不同，由于混凝土极度不耐拉，优化器自主消除了任何主要受拉构件，全部由受压拱承载。而在 $P/W = 1$ 与 $\infty$ 时，加力点下方演化出一个庞大厚实的实体核心块，并与四根粗壮的斜向受压支柱相连，以承受加载点下方复杂的三向受压应力状态，极大提升了结构的局部承载能力。

---

# 6 结论

在本文中，我们证明了包括 von Mises、Drucker–Prager、Tresca、Mohr–Coulomb、Bresler–Pister 和 Willam–Warnke 在内的多种经典工程失效准则，均可以通过一个单一的函数——**统一屈服函数**进行统一定义。我们将该统一屈服函数应用于求解具有局部应力约束的质量最小化拓扑优化问题。

为处理规模庞大的局部约束，我们采用了**归一化增广拉格朗日（AL）方法**，该方法消除了罚项随网格加密的无界增长，保证了与连续介质力学中应力作为局部物理量的一致性。得益于统一屈服函数的数学通用性，本文公式自然地将应力约束拓扑优化的适用范围从传统的延性金属拓展到包括混凝土、岩石、土壤、陶瓷及高分子多孔发泡材料在内的广大压力相关与拉压异性材料。

此外，本文考虑了结构自重及更一般的**设计相关荷载（design-dependent loading）**。针对自重问题，采用 RAMP 插值模型替代传统的 SIMP 模型，成功避免了低密度空洞单元中质量与刚度比值发散所引发的严重数值不稳定性。数值结果清晰表明：失效准则的合理选取与自重效应的准确计入，对于获取兼具物理合理性与工程可行性的结构优化拓扑构型均至关重要。

---

# 文末声明

- **数据可用性（Data accessibility）**：本文在线版本附带电子补充材料，向授权用户开放。
- **作者贡献（Authors’ contributions）**：G.H.P. 负责研究设计；O.G.-L. 与 G.H.P. 构思数学模型、解释计算结果、分析数据并撰写论文；O.G.-L. 实现了计算程序并执行了数值模拟；所有作者均对论文最终稿进行了审查与批准。
- **利益冲突（Competing interests）**：作者声明不存在竞争性利益冲突。
- **基金资助（Funding）**：本项工作得到美国国家科学基金会（NSF）项目资助（资助号：1663244）以及佐治亚理工学院 Raymond Allen Jones 讲席教授基金的支持。
- **免责声明（Disclaimer）**：文中所述信息与作者见解不代表资助机构的立场与观点。
- **致谢与题献（Acknowledgements）**：谨以此文纪念 Daniel C. Drucker 教授（1918–2001）[^6]。此外，作者衷心感谢匿名审稿人提出的富有价值的宝贵评审意见，这些意见显著提升了本文的论述质量与清晰度。

[^6]: G.H. Paulino 荣获 2020 年度美国机械工程师学会（ASME）Daniel C. Drucker 奖章。

---

# 附录 A 灵敏度分析

我们采用基于梯度的优化算法求解离散优化问题 (4.12)。为此，需要计算归一化 AL 函数 (4.24) 对设计变量 $z_j$ 的导数，通过链式法则表示为：
$$
\frac{\partial\mathcal{J}^{(k)}}{\partial z_j} = \sum_{i=1}^{N_e}\frac{\partial\mathcal{J}^{(k)}}{\partial \tilde{\rho}_i}\frac{\partial\tilde{\rho}_i}{\partial\rho_i}\frac{\partial\rho_i}{\partial z_j} = \sum_{i=1}^{N_e}\frac{\partial\mathcal{J}^{(k)}}{\partial \tilde{\rho}_i}\frac{\partial\tilde{\rho}_i}{\partial\rho_i}P_{ij}
\tag{A 1}
$$
其中阈值投影导数由式 (4.3) 给出：
$$
\frac{\partial\tilde{\rho}_i}{\partial\rho_i} = \frac{\beta\left[1 - \tanh^2(\beta(\rho_i - \eta))\right]}{\tanh(\beta\eta) + \tanh(\beta(1 - \eta))}
\tag{A 2}
$$
$P_{ij}$ 为式 (4.14) 的滤波矩阵。归一化 AL 函数 (4.24) 对物理体积分数 $\tilde{\rho}_i$ 的偏导数为：
$$
\frac{\partial\mathcal{J}^{(k)}}{\partial\tilde{\rho}_i} = \frac{1}{|\Omega|}\frac{\partial}{\partial\tilde{\rho}_i}\sum_{e=1}^{N_e}\tilde{\rho}_e v_e + \frac{1}{N_c}\frac{\partial\mathcal{P}^{(k)}}{\partial\tilde{\rho}_i} = \frac{v_i}{|\Omega|} + \frac{1}{N_c}\frac{\partial\mathcal{P}^{(k)}}{\partial\tilde{\rho}_i}
\tag{A 3}
$$
其中罚项为：
$$
\mathcal{P}^{(k)} = \sum_{j=1}^{N_c}\left[\lambda_j^{(k)}h_j(\boldsymbol{z}, \boldsymbol{u}) + \frac{\mu^{(k)}}{2}h_j(\boldsymbol{z}, \boldsymbol{u})^2\right]
\tag{A 4}
$$
罚项对物理体积分数的导数为：
$$
\frac{\partial\mathcal{P}^{(k)}}{\partial\tilde{\rho}_i} = \sum_{j=1}^{N_c}\left[\lambda_j^{(k)} + \mu^{(k)}h_j(\boldsymbol{z}, \boldsymbol{u})\right]\left[\frac{\partial h_j(\boldsymbol{z}, \boldsymbol{u})}{\partial\tilde{\rho}_i} + \frac{\partial h_j(\boldsymbol{z}, \boldsymbol{u})}{\partial\boldsymbol{u}}\cdot\frac{\partial\boldsymbol{u}}{\partial\tilde{\rho}_i}\right]
\tag{A 5}
$$
为避免直接求解计算量极其巨大的隐式导数 $\partial\boldsymbol{u}/\partial\tilde{\rho}_i$，我们引入**伴随方法（adjoint method）**。将线弹性平衡方程残差写为：
$$
\boldsymbol{R} = \frac{\partial\Pi}{\partial\boldsymbol{u}} + \epsilon\boldsymbol{u} = \boldsymbol{f}_{\mathrm{int}} - \boldsymbol{f}_{\mathrm{ext}} + \epsilon\boldsymbol{u} = \boldsymbol{0}
\tag{A 6}
$$
将伴随项 $\boldsymbol{\xi}^{\mathsf T}(\partial\boldsymbol{R}/\partial\tilde{\rho}_i)$ 加到式 (A 5) 中：
$$
\frac{\partial\mathcal{P}^{(k)}}{\partial\tilde{\rho}_i} = \sum_{j=1}^{N_c}\left[\lambda_j^{(k)} + \mu^{(k)}h_j\right]\left[\frac{\partial h_j}{\partial\tilde{\rho}_i} + \frac{\partial h_j}{\partial\boldsymbol{u}}\frac{\partial\boldsymbol{u}}{\partial\tilde{\rho}_i}\right] + \boldsymbol{\xi}^{\mathsf T}\left[\boldsymbol{K}_T\frac{\partial\boldsymbol{u}}{\partial\tilde{\rho}_i} + \frac{\partial\boldsymbol{f}_{\mathrm{int}}}{\partial\tilde{\rho}_i} - \frac{\partial\boldsymbol{f}_b}{\partial\tilde{\rho}_i} + \epsilon\frac{\partial\boldsymbol{u}}{\partial\tilde{\rho}_i}\right]
\tag{A 7}
$$
其中利用了节点外力 $\boldsymbol{f}_n$ 与设计变量无关而体力 $\boldsymbol{f}_b$ 依赖于设计变量的事实。令包含 $\partial\boldsymbol{u}/\partial\tilde{\rho}_i$ 的所有系数项之和为零，可得伴随方程：
$$
\left(\boldsymbol{K}_T + \epsilon\boldsymbol{I}\right)\boldsymbol{\xi} = -\sum_{j=1}^{N_c}\left[\lambda_j^{(k)} + \mu^{(k)}h_j(\boldsymbol{z}, \boldsymbol{u})\right]\frac{\partial h_j(\boldsymbol{z}, \boldsymbol{u})}{\partial\boldsymbol{u}}
\tag{A 9}
$$
求解伴随位移向量 $\boldsymbol{\xi}$ 后，罚项导数简化为：
$$
\frac{\partial\mathcal{P}^{(k)}}{\partial\tilde{\rho}_i} = \sum_{j=1}^{N_c}\left[\lambda_j^{(k)} + \mu^{(k)}h_j(\boldsymbol{z}, \boldsymbol{u})\right]\frac{\partial h_j(\boldsymbol{z}, \boldsymbol{u})}{\partial\tilde{\rho}_i} + \boldsymbol{\xi}^{\mathsf T}\left[\frac{\partial\boldsymbol{f}_{\mathrm{int}}}{\partial\tilde{\rho}_i} - \frac{\partial\boldsymbol{f}_b}{\partial\tilde{\rho}_i}\right]
\tag{A 8}
$$
代回式 (A 3) 即可得到整个目标函数的灵敏度表达式：
$$
\frac{\partial\mathcal{J}^{(k)}}{\partial\tilde{\rho}_i} = \frac{v_i}{|\Omega|} + \frac{1}{N_c}\left\{ \sum_{j=1}^{N_c}\left[\lambda_j^{(k)} + \mu^{(k)}h_j(\boldsymbol{z}, \boldsymbol{u})\right]\frac{\partial h_j(\boldsymbol{z}, \boldsymbol{u})}{\partial\tilde{\rho}_i} + \boldsymbol{\xi}^{\mathsf T}\left[\frac{\partial\boldsymbol{f}_{\mathrm{int}}}{\partial\tilde{\rho}_i} - \frac{\partial\boldsymbol{f}_b}{\partial\tilde{\rho}_i}\right] \right\}
\tag{A 10}
$$

各具体偏导数如下：
当 $g_j(\boldsymbol{z}, \boldsymbol{u}) < -\lambda_j^{(k)}/\mu^{(k)}$ 时，$\partial h_j/\partial\tilde{\rho}_i = 0$；否则：
$$
\frac{\partial h_j(\boldsymbol{z}, \boldsymbol{u})}{\partial\tilde{\rho}_i} = \frac{\partial m_E(\rho_i)}{\partial\tilde{\rho}_i}\Lambda_j\left(\Lambda_j^2 + 1\right)
\tag{A 11}
$$
由于为线性材料，$\boldsymbol{f}_{\mathrm{int}} = \boldsymbol{K}_T\boldsymbol{u}$，因此：
$$
\frac{\partial\boldsymbol{f}_{\mathrm{int}}}{\partial\tilde{\rho}_i} = \frac{\partial m_E(\rho_i)}{\partial\tilde{\rho}_i}\boldsymbol{k}_0^i\boldsymbol{u}_i
\tag{A 12}
$$
其中 $\boldsymbol{k}_0^i$ 为单元实体刚度矩阵，$\boldsymbol{u}_i$ 为单元位移向量。体力偏导数给出为：
$$
\frac{\partial\boldsymbol{f}_b^e}{\partial\tilde{\rho}_i} = \frac{\partial m_V(\rho_i)}{\partial\tilde{\rho}_i}\boldsymbol{f}_{b0}^i, \quad \boldsymbol{f}_{b0}^i = \int_{\Omega_i}\boldsymbol{N}_e^{\mathsf T}\boldsymbol{b}\,\mathrm{d}\Omega
\tag{A 13}
$$

对于伴随方程右端项 $\partial h_j/\partial\boldsymbol{u}$：当 $g_j < -\lambda_j^{(k)}/\mu^{(k)}$ 时为 0；否则：
$$
\frac{\partial h_j}{\partial\boldsymbol{u}} = \frac{\partial g_j}{\partial\boldsymbol{u}} = \frac{\partial g_j}{\partial\Lambda_j}\left[ \frac{\partial\Lambda_j}{\partial I_1}\frac{\partial I_1}{\partial\boldsymbol{\sigma}} + \frac{\partial\Lambda_j}{\partial J_2}\frac{\partial J_2}{\partial\boldsymbol{\sigma}} + \frac{\partial\Lambda_j}{\partial J_3}\frac{\partial J_3}{\partial\boldsymbol{\sigma}} \right]\cdot\frac{\partial\boldsymbol{\sigma}}{\partial\boldsymbol{u}}
\tag{A 14}
$$
其中由多项式消失约束式 (4.19) 可知：
$$
\frac{\partial g_j}{\partial\Lambda_j} = m_E(\tilde{\rho}_j)\left(3\Lambda_j^2 + 1\right)
$$
统一屈服函数对三个应力不变量的偏导数显式表示为：
$$
\left.
\begin{aligned}
\frac{\partial\Lambda_j}{\partial I_1} &= \frac{\partial\sigma_{\mathrm{eq}, j}}{\partial I_1} = \hat{\beta} + 2\hat{\gamma}I_1 \\
\frac{\partial\Lambda_j}{\partial J_2} &= \frac{\partial\sigma_{\mathrm{eq}, j}}{\partial J_2} = \frac{\partial\hat{\alpha}(\theta)}{\partial\theta}\frac{\partial\theta}{\partial J_2}\sqrt{3J_2} + \frac{3\hat{\alpha}(\theta)}{2\sqrt{3J_2}} \\
\frac{\partial\Lambda_j}{\partial J_3} &= \frac{\partial\sigma_{\mathrm{eq}, j}}{\partial J_3} = \frac{\partial\hat{\alpha}(\theta)}{\partial\theta}\frac{\partial\theta}{\partial J_3}\sqrt{3J_2}
\end{aligned}
\right\}
\tag{A 15}
$$
其中导数 $\partial\hat{\alpha}(\theta)/\partial\theta, \partial\theta/\partial J_2, \partial\theta/\partial J_3$ 分别由式 (3.2)、(3.3) 与 (2.7) 给出。

应力不变量对 Voigt 形式 Cauchy 应力向量 $\boldsymbol{\sigma} = [\sigma_{11}, \sigma_{22}, \sigma_{33}, \sigma_{23}, \sigma_{13}, \sigma_{12}]^{\mathsf T}$ 的导数可显式求得：
- 第一不变量 $I_1 = \boldsymbol{M}\boldsymbol{\sigma}$（$\boldsymbol{M} = [1, 1, 1, 0, 0, 0]$），故 $\partial I_1/\partial\boldsymbol{\sigma} = \boldsymbol{M}^{\mathsf T}$；
- 第二偏应力不变量 $J_2 = \frac{1}{3}\boldsymbol{\sigma}^{\mathsf T}\boldsymbol{V}\boldsymbol{\sigma}$，故 $\partial J_2/\partial\boldsymbol{\sigma} = \frac{2}{3}\boldsymbol{V}\boldsymbol{\sigma}$；
- 第三偏应力不变量为：
$$
J_3 = s_{11}s_{22}s_{33} + 2\sigma_{23}\sigma_{13}\sigma_{12} - \left(s_{11}\sigma_{23}^2 + s_{22}\sigma_{13}^2 + s_{33}\sigma_{12}^2\right)
\tag{A 16}
$$
其对 Cauchy 应力的解析导数表示为 [63]：
$$
\frac{\partial J_3}{\partial\boldsymbol{\sigma}} =
\begin{bmatrix}
s_{22}s_{33} - \sigma_{23}^2 \\
s_{11}s_{33} - \sigma_{13}^2 \\
s_{11}s_{22} - \sigma_{12}^2 \\
2(\sigma_{13}\sigma_{12} - s_{11}\sigma_{23}) \\
2(\sigma_{12}\sigma_{23} - s_{22}\sigma_{13}) \\
2(\sigma_{23}\sigma_{13} - s_{33}\sigma_{12})
\end{bmatrix}
+ \frac{J_2}{3}
\begin{bmatrix}
1 \\
1 \\
1 \\
0 \\
0 \\
0
\end{bmatrix}
\tag{A 17}
$$
最后，应力对位移的偏导数通过线弹性本构直接计算：$\partial\boldsymbol{\sigma}/\partial\boldsymbol{u} = \boldsymbol{D}\boldsymbol{B}$，其中 $\boldsymbol{D}$ 为材料弹性刚度矩阵，$\boldsymbol{B}$ 为应变–位移几何矩阵。

---

# 附录 B 经典屈服准则汇总

第 3 节中引入的统一屈服函数能够精确重现第 2 节介绍的所有经典屈服准则。表 5 汇总了统一屈服函数 (3.1) 中所采用的偏应力函数 $\hat{\alpha}(\theta)$ 与修正 Lode 角 $\hat{\theta}$ 的显式解析表达式；表 6 汇总了所有六种经典屈服准则的最终统一等效应力测度 $\sigma_{\mathrm{eq}}$。

<center><b>
表 5：经典屈服准则的偏应力函数 $\hat{\alpha}(\theta)$ 与修正 Lode 角 $\hat{\theta}$ 汇总
</b></center>

| 失效准则 | 偏应力函数 $\hat{\alpha}(\theta)$ | 修正 Lode 角 $\hat{\theta}$ |
|---|---|---|
| von Mises | $\hat{\alpha}(\theta) = \frac{1}{\sigma_{\mathrm{lim}}}$ | $\hat{\theta} = \theta$ |
| Drucker–Prager | $\hat{\alpha}(\theta) = \frac{\sigma_c + \sigma_t}{2\sigma_c\sigma_t}$ | $\hat{\theta} = \theta$ |
| Tresca[^5a] | $\hat{\alpha}(\theta) = \frac{2}{\sqrt{3}\sigma_{\mathrm{lim}}}\cos\hat{\theta}$ | $\hat{\theta} = \frac{1}{3}\arcsin[\zeta\sin 3\theta]$ |
| Mohr–Coulomb[^5a][^5b] | $\hat{\alpha}(\theta) = \frac{2\alpha}{3}\sqrt{3 + \left(\frac{\beta}{\alpha}\right)^2}\cos\hat{\theta}$ | $\hat{\theta} = \frac{1}{3}\arcsin[\zeta\sin 3\theta] + \tilde{\theta}$ |
| Bresler–Pister[^5c] | $\hat{\alpha}(\theta) = \alpha_{\mathrm{BP}}$ | $\hat{\theta} = \theta$ |
| Willam–Warnke[^5d] | $\hat{\alpha}(\theta) = \frac{A_W \cos^2\hat{\theta} + B_W}{C_W \cos\hat{\theta} + \sqrt{D_W \cos^2\hat{\theta} + E_W}}$ | $\hat{\theta} = \theta + \frac{\pi}{6}$ |

[^5a]: 取 $\zeta < 1$ 获得顶点光滑圆角化 [60]。
[^5b]: $\alpha$ 与 $\beta$ 由式 (2.13) 给出，$\tilde{\theta}$ 由式 (2.20) 给出。
[^5c]: $\alpha_{\mathrm{BP}}$ 由式 (2.24) 给出。
[^5d]: $A_W, B_W, C_W, D_W$ 与 $E_W$ 由式 (2.32) 给出。

<center><b>
表 6：经典屈服准则的统一等效应力测度 $\sigma_{\mathrm{eq}}$ 汇总
</b></center>

| 失效准则 | 等效应力测度 $\sigma_{\mathrm{eq}}$ |
|---|---|
| von Mises 与 Tresca | $\sigma_{\mathrm{eq}} = \hat{\alpha}(\theta)\sqrt{3J_2}$ |
| Drucker–Prager 与 Mohr–Coulomb[^6b] | $\sigma_{\mathrm{eq}} = \hat{\alpha}(\theta)\sqrt{3J_2} + \hat{\beta}I_1$ |
| Bresler–Pister[^6c] | $\sigma_{\mathrm{eq}} = \hat{\alpha}(\theta)\sqrt{3J_2} + \beta_{\mathrm{BP}}I_1 + \gamma_{\mathrm{BP}}I_1^2$ |
| Willam–Warnke | $\sigma_{\mathrm{eq}} = \hat{\alpha}(\theta)\sqrt{3J_2} + \frac{\sigma_b - \sigma_t}{3\sigma_b\sigma_t}I_1$ |

[^6b]: Drucker–Prager 取 $\hat{\beta} = \frac{\sigma_c - \sigma_t}{2\sigma_c\sigma_t}$；Mohr–Coulomb 取 $\hat{\beta} = \frac{\sigma_c - \sigma_t}{3\sigma_c\sigma_t}$。
[^6c]: $\beta_{\mathrm{BP}}$ 与 $\gamma_{\mathrm{BP}}$ 由式 (2.24) 给出。

---

# 参考文献

1. Duysinx P, Bendsøe MP. 1998 Topology optimization of continuum structures with local stress constraints. *Int. J. Numer. Methods Eng.* 43, 1453–1478.
2. Sved G, Ginos Z. 1968 Structural optimization under multiple loading. *Int. J. Mech. Sci.* 10, 803–805.
3. Kirsch U, Taye S. 1986 On optimal topology of grillage structures. *Eng. Comput.* 1, 229–243.
4. Kirsch U. 1989 Optimal topologies in truss structures. *Comput. Methods Appl. Mech. Eng.* 72, 15–28.
5. Kirsch U. 1990 On singular topologies in optimum structural design. *Struct. Optim.* 2, 133–142.
6. Rozvany GIN, Birker T. 1994 On singular topologies in exact layout optimization. *Struct. Optim.* 8, 228–235.
7. Yang RJ, Chen CJ. 1996 Stress-based topology optimization. *Struct. Optim.* 12, 98–105.
8. Duysinx P, Sigmund O. 1998 New developments in handling stress constraints in optimal material distribution. In *Proc. 7th AIAA/USAF/NASA/ISSMO Symp. on Multidisciplinary Analysis and Optimization*, St Louis, MO, USA, 2–4 September 1998, vol. 1, pp. 1501–1509.
9. Luo Y, Wang MY, Kang Z. 2013 An enhanced aggregation method for topology optimization with local stress constraints. *Comput. Methods Appl. Mech. Eng.* 254, 31–41.
10. De Leon DM, Alexandersen J, Fonseca JS, Sigmund O. 2015 Stress-constrained topology optimization for compliant mechanism design. *Struct. Multidiscip. Optim.* 52, 929–943.
11. Kiyono C, Vatanabe S, Silva E, Reddy J. 2016 A new multi-p-norm formulation approach for stress-based topology optimization design. *Compos. Struct.* 156, 10–19.
12. Lee K, Ahn K, Yoo J. 2016 A novel P-norm correction method for lightweight topology optimization under maximum stress constraints. *Comput. Struct.* 171, 18–30.
13. Lian H, Christiansen AN, Tortorelli DA, Sigmund O. 2017 Combined shape and topology optimization for minimization of maximal von Mises stress. *Struct. Multidiscip. Optim.* 55, 1541–1557.
14. Liu H, Yang D, Hao P, Zhu X. 2018 Isogeometric analysis based topology optimization design with global stress constraint. *Comput. Methods Appl. Mech. Eng.* 342, 625–652.
15. Xia L, Zhang L, Xia Q, Shi T. 2018 Stress-based topology optimization using bi-directional evolutionary structural optimization method. *Comput. Methods Appl. Mech. Eng.* 333, 356–370.
16. Fan Z, Xia L, Lai W, Xia Q, Shi T. 2019 Evolutionary topology optimization of continuum structures with stress constraints. *Struct. Multidiscip. Optim.* 59, 647–658.
17. Le C, Norato J, Bruns T, Ha C, Tortorelli D. 2010 Stress-based topology optimization for continua. *Struct. Multidiscip. Optim.* 41, 605–620.
18. Lee E, James KA, Martins JRRA. 2012 Stress-constrained topology optimization with design-dependent loading. *Struct. Multidiscip. Optim.* 46, 647–661.
19. Holmberg E, Torstenfelt B, Klarbring A. 2013 Stress constrained topology optimization. *Struct. Multidiscip. Optim.* 48, 33–47.
20. Kreisselmeier G, Steinhauser R. 1979 Systematic control design by optimizing a vector performance index. *IFAC Proc. Vol.* 12, 113–117.
21. Park YK. 1995 Extensions of optimal layout design using the homogenization method. PhD thesis, University of Michigan, Ann Arbor.
22. Senhora FV, Giraldo-Londoño O, Menezes IFM, Paulino GH. 2020 Topology optimization with local stress constraints: a stress aggregation-free approach. *Struct. Multidiscip. Optim.*
23. Bertsekas DP. 1999 *Nonlinear programming*, 2nd edn. Belmont, MA: Athena Scientific.
24. Nocedal J, Wright SJ. 2006 *Numerical optimization*, 2nd edn. Berlin, Germany: Springer.
25. Izmailov AF, Solodov MV, Uskov EI. 2012 Global convergence of Augmented Lagrangian methods applied to optimization problems with degenerate constraints, including problems with complementarity constraints. *SIAM J. Optim.* 22, 1579–1606.
26. Andreani R, Haeser G, Schuverdt ML, Silva PJ. 2012 A relaxed constant positive linear dependence constraint qualification and applications. *Math. Program.* 135, 255–273.
27. Pereira JT, Fancello EA, Barcellos CS. 2004 Topology optimization of continuum structures with material failure constraints. *Struct. Multidiscip. Optim.* 26, 50–66.
28. Fancello EA. 2006 Topology optimization for minimum mass design considering local failure constraints and contact boundary conditions. *Struct. Multidiscip. Optim.* 32, 229–240.
29. Emmendoerfer H Jr, Fancello EA. 2014 A level set approach for topology optimization with local stress constraints. *Int. J. Numer. Methods Eng.* 99, 129–156.
30. Emmendoerfer H Jr, Fancello EA. 2016 Topology optimization with local stress constraint based on level set evolution via reaction-diffusion. *Comput. Methods Appl. Mech. Eng.* 305, 62–88.
31. Emmendoerfer Jr H, Silva ECN, Fancello EA. 2019 Stress-constrained level set topology optimization for design-dependent pressure load problems. *Comput. Methods Appl. Mech. Eng.* 344, 569–601.
32. Da Silva GA, Beck AT, Cardoso EL. 2018 Topology optimization of continuum structures with stress constraints and uncertainties in loading. *Int. J. Numer. Methods Eng.* 113, 153–178.
33. da Silva GA, Beck AT, Sigmund O. 2019 Topology optimization of compliant mechanisms with stress constraints and manufacturing error robustness. *Comput. Methods Appl. Mech. Eng.* 354, 397–421.
34. da Silva GA, Beck AT, Sigmund O. 2019 Stress-constrained topology optimization considering uniform manufacturing uncertainties. *Comput. Methods Appl. Mech. Eng.* 344, 512–537.
35. von Mises R. 1913 Mechanik der festen Koerper in plastisch deformahlem Zustand. *Goettinger Narchrichten* 4, 582–592.
36. Amstutz S, Novotny AA, de Souza Neto EA. 2012 Topological derivative-based topology optimization of structures subject to Drucker–Prager stress constraints. *Comput. Methods Appl. Mech. Eng.* 233, 123–136.
37. Bruggi M, Duysinx P. 2012 Topology optimization for minimum weight with compliance and stress constraints. *Struct. Multidiscip. Optim.* 46, 369–384.
38. Luo Y, Kang Z. 2012 Topology optimization of continuum structures with Drucker–Prager yield stress constraints. *Comput. Struct.* 90, 65–75.
39. Bruggi M, Duysinx P. 2013 A stress–based approach to the optimal design of structures with unilateral behavior of material or supports. *Struct. Multidiscip. Optim.* 48, 311–326.
40. Duysinx P, Van Miegroet L, Lemaire E, Brüls O, Bruyneel M. 2008 Topology and generalized shape optimization: why stress constraints are so important? *Int. J. Simul. Multidisci. Des. Optim.* 2, 253–259.
41. Raghava R, Caddell RM, Yeh GS. 1973 The macroscopic yield behaviour of polymers. *J. Mater. Sci.* 8, 225–232.
42. Gali S, Dolev G, Ishai O. 1981 An effective stress/strain concept in the mechanical characterization of structural adhesive bonding. *Int. J. Adhesion Adhes.* 1, 135–140.
43. Jeong SH, Park SH, Choi DH, Yoon GH. 2012 Topology optimization considering static failure theories for ductile and brittle materials. *Comput. Struct.* 110, 116–132.
44. Yoon GH. 2017 Brittle and ductile failure constraints of stress-based topology optimization method for fluid–structure interactions. *Comput. Math. Appl.* 74, 398–419.
45. Tresca H. 1869 Mémoire sur l’écoulement des corps solides. Paris, France: Imprimerie Impériale.
46. Drucker DC, Prager W. 1952 Soil mechanics and plastic analysis for limit design. *Q. Appl. Math.* 10, 157–165.
47. Coulomb C. 1776 Essai sur une application des regles de maximis et minimis a quelques problemes de statique relatifs a l’architecture. *Mem. Acad. R. Div. Sav.* 7, 343–387.
48. Bresler B, Pister KS. 1958 Strength of concrete under combined stresses. *ACI J.* 551, 321–345.
49. Willam KJ, Warnke EP. 1975 Constitutive model for the triaxial behaviour of concrete. In *Proc. International Association for Bridge and Structural Engineering*, vol. 19, pp. 1–30.
50. Drucker DC. 1950 Some implications of work hardening and ideal plasticity. *Q. Appl. Math.* 7, 411–418.
51. Drucker D, Prager W, Greenberg H. 1952 Extended limit design theorems for continuous media. *Q. Appl. Math.* 9, 381–389.
52. Drucker DC. 1953 Coulomb friction, plasticity, and limit loads. Technical report. Providence, RI: Division of Applied Mathematics, Brown University.
53. Drucker DC. 1953 Limit analysis of two and three dimensional soil mechanics problems. *J. Mech. Phys. Solids* 1, 217–226.
54. Drucker DC. 1956 On uniqueness in the theory of plasticity. *Q. Appl. Math.* 14, 35–42.
55. Drucker DC. 1957 A definition of stable inelastic material. Technical report. Providence, RI: Brown University.
56. Drucker DC. 1957 Soil mechanics and work-hardening theories of plasticity. *Trans. ASCE* 122, 338–346.
57. National Academy of Engineering. 2015 *Memorial tributes*, vol. 19. Washington, DC: National Academies Press.
58. Lode W. 1926 Versuche über den Einfluß der mittleren Hauptspannung auf das Fließen der Metalle Eisen, Kupfer und Nickel. *Zeitschrift für Physik* 36, 913–939.
59. Crisfield MA. 1997 *Non-linear analysis of solids and structures*, vol. 2. New York, NY: Wiley.
60. Lagioia R, Panteghini A. 2016 On the existence of a unique class of yield and failure criteria comprising Tresca, von Mises, Drucker-Prager, Mohr-Coulomb, Galileo-Rankine, Matsuoka-Nakai and Lade-Duncan. *Proc. R. Soc. A* 472, 20150713.
61. Lade PV, Duncan JM. 1975 Lastoplastic stress-strain theory for cohesionless soil. *J. Geotech. Geoenviron. Eng.* 101, 1037–1053.
62. Matsuoka H, Nakai T. 1974 Stress-deformation and strength characteristics of soil under three different principal stresses. *Proc. Jpn Soc. Civil Eng.* 232, 59–70.
63. Abbo AJ, Sloan SW. 1995 A smooth hyperbolic approximation to the Mohr–Coulomb yield criterion. *Comput. Struct.* 54, 427–441.
64. Gurtin ME. 1981 *An introduction to continuum mechanics*. Mathematics in Science and Engineering, vol. 158. New York, NY: Academic Press.
65. Wang F, Lazarov BS, Sigmund O. 2011 On projection methods, convergence and robust formulations in topology optimization. *Struct. Multidiscip. Optim.* 43, 767–784.
66. Tikhonov AN, Arsenin VY. 1977 *Methods for solving ill-posed problems*. New York, NY: John Wiley and Sons.
67. Talischi C, Paulino GH. 2013 An operator splitting algorithm for Tikhonov-regularized topology optimization. *Comput. Methods Appl. Mech. Eng.* 253, 599–608.
68. Ramos A, Paulino G. 2016 Filtering structures out of ground structures—a discrete filtering tool for structural design optimization. *Struct. Multidiscip. Optim.* 54, 95–116.
69. Bendsøe MP. 1989 Optimal shape design as a material distribution problem. *Struct. Optim.* 1, 193–202.
70. Zhou M, Rozvany GIN. 1991 The COC algorithm, Part II. Topological, geometrical and generalized shape optimization. *Comput. Methods Appl. Mech. Eng.* 89, 309–336.
71. Rozvany GI, Zhou M, Birker T. 1992 Generalized shape optimization without homogenization. *Struct. Optim.* 4, 250–252.
72. Stolpe M, Svanberg K. 2001 An alternative interpolation scheme for minimum compliance topology optimization. *Struct. Multidiscip. Optim.* 22, 116–124.
73. Bruyneel M, Duysinx P. 2005 Note on topology optimization of continuum structures including self-weight. *Struct. Multidiscip. Optim.* 29, 245–256.
74. Bourdin B. 2001 Filters in topology optimization. *Int. J. Numer. Methods Eng.* 50, 2143–2158.
75. Cheng GD, Jiang Z. 1992 Study on topology optimization with stress constraints. *Eng. Optim.* 20, 129–148.
