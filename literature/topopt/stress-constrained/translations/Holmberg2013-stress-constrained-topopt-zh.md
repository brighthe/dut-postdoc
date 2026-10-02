---
title: "翻译：Stress constrained topology optimization"
tags:
  - translation
  - topology-optimization
  - stress-constraints
status: "done"
date_created: 2026-09-07
date_updated: 2026-09-08
source: "../sources/Holmberg2013-stress-constrained-topopt.pdf"
citekey: "Holmberg2013-stressconstrained"
language: "zh-CN"
---

# Stress constrained topology optimization

---

# 信息

- **中文标题**：应力约束拓扑优化
- **作者**：Erik Holmberg; Bo Torstenfelt; Anders Klarbring
- **单位**：林雪平大学管理与工程系力学分部、固体力学分部；Erik Holmberg 的现地址为 Saab AB（按原文标注）
- **期刊**：*Structural and Multidisciplinary Optimization* (SMO)
- **卷 / 期 / 页码**：48: 33–47
- **年份**：2013
- **在线发表**：2013-02-01
- **DOI**：10.1007/s00158-012-0880-7

# 摘要

本文提出并评估了一种在拓扑优化中处理应力约束的方法。应力约束与最小化质量或最大化刚度的目标函数结合使用；此外，为了比较，文中还讨论了传统的基于刚度的问题表述。我们采用聚类技术，利用修正的 P 范数将若干应力评估点的应力归入多个组，以减少应力约束数目，从而降低计算成本。本文详细说明了问题表述和灵敏度分析，并采用一般形式，使其能够处理不同单元类型以及二维和三维结构。不过，数值算例限于采用双线性四边形单元的二维结构。文中通过拓扑优化中两个著名算例——L 形梁和 MBB 梁——比较三种问题表述及不同的应力约束处理方法。与应力约束拓扑优化的另一些论文不同，我们发现，本文问题表述所得拓扑与传统优化设计明显不同，因为它确实能够避免应力集中。因此，该方法可用于生成工业应用中的概念设计。

**关键词**：拓扑优化；应力约束；聚类；SIMP；MMA

# 1 引言

许多工业应用都希望获得更轻的设计，而结构优化是生成轻量化结构的有效方法。拓扑优化（Bendsøe and Sigmund 2003）是结构优化的第一阶段，用于概念设计，因此也是能够实现最大质量减小的阶段。拓扑优化不需要初始设计；设计变量作为单元属性的缩放因子，决定某个单元应属于结构构件还是孔洞。

在传统拓扑优化问题表述中，给定材料用量后使刚度最大。传统优化设计通常包含很高的应力集中，而且正如下文将展示的，有时甚至包含会引起应力奇异性的几何形状。因此，为满足应力约束等工程要求，往往需要进行大量人工调整或形状优化。所需拓扑改动常常十分剧烈，所以拓扑优化更多被用来帮助寻找最优载荷路径，而不是直接得到概念设计。本文在拓扑优化阶段就引入应力约束，从而能够得到比传统问题表述结果更接近最终设计的复杂设计。因此，拓扑优化中的应力约束可以进一步减轻重量，并简化后续设计工作。

本文考虑线弹性各向同性材料，并且只关注所谓的黑白设计，即最终设计中只允许实体材料和孔洞。这可以简化结果解释，也便于在今后的工作中评估三维结构。尽管最终设计追求整数值 1（黑）和 0（白），本文仍使用连续设计变量，并通过带惩罚的实体各向同性材料模型（Solid Isotropic Material with Penalization，SIMP）惩罚中间设计变量值，从而得到黑白设计。SIMP 最初由 Bendsøe（1989）提出，Rozvany et al.（1992）后来提出了这一名称。本文还采用类似的问题表述惩罚应力，具体见 Le et al.（2010）以及本文第 4 节。

本文采用设计变量过滤器（Bruns and Tortorelli 2001）消除网格依赖和棋盘格现象。过滤器还强制规定结构构件的最小宽度，从而避免仅由一层或两层单元组成的构件产生人为刚度。

在拓扑优化中使用应力约束的目的，并非精确控制应力水平，而是避免高应力集中，生成无需大幅修改便能继续发展为满足应力要求的最终设计的方案。拓扑优化是一种需要后处理和进一步分析的概念设计工具，但目标是从更好的起点出发，使后续设计工作更加直接。

应力准则是工程设计中最重要的准则之一，因此从拓扑优化诞生之初就受到讨论。被视为拓扑优化起源的 Bendsøe and Kikuchi（1988）虽然没有在问题表述中使用应力约束，却已经提及这一问题。更早以前，Dorn et al.（1964）已在桁架优化中使用应力约束。近年来，Svanberg and Werme（2007）、Le et al.（2010）和 París et al.（2009）等对其进行了研究。需要指出的是，与传统刚度最大化问题相比，应力约束会带来额外困难：Sved and Ginos（1968）在桁架优化问题中发现，当杆件截面积趋于零时，应力约束会被违反，因而杆件不能被移除，这就是所谓的奇异性。二维和三维问题中同样存在奇异性：设计变量趋于零时，仍可能残留不消失的应力。设计变量值很低的区域仍可能发生应变，从而产生非零、甚至异常高的应力，尽管该区域代表孔洞，其应力实际上应为零。Guo et al.（2001）、Kirsch（1990）和 Rozvany and Birker（1994）等许多论文都讨论了奇异性问题。避免该问题的一种方法是采用 Cheng and Guo（1997）提出的 $\epsilon$ 松弛；Duysinx and Bendsøe（1998）与 Duysinx and Sigmund（1998）在应力约束问题中采用了这一方法。本文使用 Bruggi（2008）提出的应力惩罚，它不仅进一步惩罚中间设计变量，还能避免奇异性问题。Duysinx and Bendsøe（1998）给出了展示奇异性问题的简单算例。图 1 用本文方法处理该算例：没有遇到奇异性问题，而且在两根杆件之间形成了孔洞；若不对 Duysinx and Bendsøe（1998）的应力问题表述采用 $\epsilon$ 松弛，则无法得到这一结果。

![[Holmberg2013_Fig1.png]]

<center><b>
图 1：Duysinx and Bendsøe（1998）采用的简单算例
</b></center>

Duysinx and Bendsøe（1998）还讨论了局部应力约束数量过多所引起的问题。由于应力是局部量，必须采用大量局部应力约束，问题因此计算代价高昂，需要高效方法处理计算负担。Duysinx and Sigmund（1998）采用类似问题表述提出了全局应力量度，将全部应力归入一个应力约束。全局应力量度显著减少了计算时间，但对局部应力的控制较弱，在某些情况下难以接受。鉴于这些缺点，本文既不特别关注局部方法，也不特别关注全局方法，而是采用聚类方法：使用数量适中的应力约束，并将多个应力评估点归入每个约束。这与 París et al.（2010）的分块聚合以及 Le et al.（2010）的区域应力量度有一定相似性。

还应指出，应力约束拓扑问题也已采用水平集方法求解，例如 Allaire and Jouve（2008）、Amstutz and Novotny（2010）以及 Guo et al.（2011）。水平集方法采用两个相，通常分别表示实体材料和空域；应力约束只施加于实体相，因此不会出现奇异性问题。最终设计也不存在基于过滤 SIMP 的问题表述中实体与空域之间残留的中间设计变量过渡层。不过，设计变量数量仍然很大，因此需要用逼近局部应力的全局应力量度（Allaire and Jouve 2008; Amstutz and Novotny 2010）或活跃集策略（Guo et al. 2011）降低计算成本。

本文使用双线性四边形单元。尽管该单元存在缺点（例如 Cook et al. 2002），但在拓扑优化问题中十分常见。它并不特别适合应力分析，不过由于形式简单、计算成本低，而且 Le et al.（2010）等先前的应力问题已采用该单元并取得较好结果，本文仍选择使用。应力在单元形心处评估，该位置对应超收敛应力点。问题和灵敏度分析采用一般形式表述，以便今后考虑不同单元类型。

最后的优化问题由移动渐近线法（Method of Moving Asymptotes，MMA）（Svanberg 1987）求解。

本文结构如下：第 2 节介绍问题表述；第 3 节和第 4 节分别讨论设计变量过滤器与惩罚技术；第 5 节给出聚类方法所用的应力量度，第 6 节讨论不同聚类技术；第 7 节计算相关梯度，第 8 节评述建模要点；第 9 节给出数值结果，第 10 节给出结论。

# 2 问题表述

本文优化由有限元法（Finite Element Method，FEM）（Hughes 1987）离散的结构。设计变量收集于向量 $\mathbf{x}$ 中，是单元属性的缩放因子，即优化中每个有限元对应一个设计变量。文献中常把设计变量解释为厚度、孔隙率或复合材料描述，但本文更倾向于把它们视为没有物理解释的数学缩放因子。优化追求缩放因子为 0 或 1 的最终设计，因此没有必要赋予中间设计变量值物理解释。第 4 节说明如何得到这种最终设计。设计变量 $\mathbf{x}$ 经过过滤（见第 3 节），从而建立 $\mathbf{x}$ 与变量 $\boldsymbol{\rho}$ 的关系，即 $\boldsymbol{\rho}=\boldsymbol{\rho}(\mathbf{x})$。后者称为过滤变量，并被视为物理变量，因为它们定义刚度并进入质量计算。设计 $\boldsymbol{\rho}(\mathbf{x})$ 的平衡方程为

$$
\mathbf{K}(\boldsymbol{\rho}(\mathbf{x}))\mathbf{u}=\mathbf{F},
\tag{1}
$$

其中，$\mathbf{K}(\boldsymbol{\rho}(\mathbf{x}))$ 为结构的整体刚度矩阵，$\mathbf{u}$ 为整体节点位移向量，$\mathbf{F}$ 为已知外载荷向量。

本文采用嵌套问题表述，即平衡方程（1）不像 Bendsøe et al.（1994）所述的同时问题表述那样作为约束。位移向量被看作设计变量的给定函数，并由有限元分析求解。对于给定设计 $\boldsymbol{\rho}(\mathbf{x})$ 和可逆刚度矩阵，位移向量关于 $\mathbf{x}$ 的函数为

$$
\mathbf{u}=\mathbf{u}(\mathbf{x})=\mathbf{K}^{-1}(\boldsymbol{\rho}(\mathbf{x}))\mathbf{F}.
$$

本文讨论并比较三种问题表述。第一种是本文主要关注的问题：在应力约束下最小化质量，写为

$$
(\mathrm{P}_1)\quad
\begin{cases}
\displaystyle \min_{\mathbf{x}} & \displaystyle \sum_{e=1}^{n_e}m_e\rho_e(\mathbf{x})\\[6pt]
\mathrm{s.t.} & \sigma_i^{PN}(\mathbf{x})\leq \bar{\sigma},\quad i=1,\ldots,n_c,\\
& \underline{x}_e\leq x_e\leq \bar{x}_e,\quad e=1,\ldots,n_e.
\end{cases}
$$

其中，$n_e$ 为设计变量数，$m_e$ 为与设计变量 $e$ 对应单元的实体单元质量；第 $e$ 个过滤变量记为 $\rho_e(\mathbf{x})$，第 $e$ 个设计变量为 $x_e$。箱式约束上下限分别为 $\bar{x}_e=1$ 和 $\underline{x}_e=\epsilon$，其中 $\epsilon$ 是用于避免刚度矩阵奇异的小正数。本文采用基于 von Mises 应力的修正 P 范数作为应力量度，第 $i$ 个聚类的应力量度记为 $\sigma_i^{PN}(\mathbf{x})$，详见第 5 节。聚类数，也即应力约束数，记为 $n_c$，应力限值为 $\bar{\sigma}$。也可以采用 von Mises 以外的应力量度。Duysinx and Bendsøe（1998）、Le et al.（2010）和 París et al.（2009）等采用过与 $(\mathrm{P}_1)$ 类似的问题表述，但应力量度的具体形式不同。

第二种问题表述以柔顺度目标取代质量目标，即寻求刚度最大的设计。该目标需要限制设计域内可分配的体积或质量。为便于同 $(\mathrm{P}_1)$ 比较，本文约束可用质量。据作者所知，此前只有 Werme（2008）结合 Svanberg and Werme（2007）提出的离散方法使用过这一问题表述。第二种问题表述为

$$
(\mathrm{P}_2)\quad
\begin{cases}
\displaystyle \min_{\mathbf{x}} & \displaystyle \frac{1}{2}\mathbf{F}^{T}\mathbf{u}(\mathbf{x})\\[6pt]
\mathrm{s.t.} & \sigma_i^{PN}(\mathbf{x})\leq \bar{\sigma},\quad i=1,\ldots,n_c,\\
& \displaystyle \sum_{e=1}^{n_e}m_e\rho_e(\mathbf{x})\leq \bar{M},\\
& \underline{x}_e\leq x_e\leq \bar{x}_e,\quad e=1,\ldots,n_e,
\end{cases}
$$

其中，$\bar{M}$ 为允许的总质量。

第三种是本文仅用于比较的传统刚度问题表述。在该问题中，在质量约束下最小化柔顺度。关于基于这一问题表述的重要论文，可参见 Bendsøe and Sigmund（2003）及其中所列参考文献。该问题写为

$$
(\mathrm{P}_3)\quad
\begin{cases}
\displaystyle \min_{\mathbf{x}} & \displaystyle \frac{1}{2}\mathbf{F}^{T}\mathbf{u}(\mathbf{x})\\[6pt]
\mathrm{s.t.} & \displaystyle \sum_{e=1}^{n_e}m_e\rho_e(\mathbf{x})\leq \bar{M},\\
& \underline{x}_e\leq x_e\leq \bar{x}_e,\quad e=1,\ldots,n_e.
\end{cases}
$$

# 3 设计变量过滤

本文采用设计变量过滤器（Bruns and Tortorelli 2001），即对相邻设计变量 $x_j$ 加权平均，得到过滤变量 $\boldsymbol{\rho}$。过滤变量 $\boldsymbol{\rho}$ 被视为物理变量，因为它们进入刚度矩阵和质量的计算，而 $\mathbf{x}$ 没有物理解释。设计变量过滤器为

$$
\rho_e(\mathbf{x})=
\frac{\displaystyle\sum_{j\in\Omega_e}w_jx_j}
{\displaystyle\sum_{j\in\Omega_e}w_j},
$$

其中，$\Omega_e$ 是与设计变量 $e$ 对应单元形心距离不超过过滤半径 $r_0$ 的单元形心所对应的设计变量索引集合，如图 2 所示。这里采用锥形权重，即权重随 $r_j$ 线性减小；$r_j$ 是分别与设计变量 $j$ 和 $e$ 对应的两个单元形心之间的距离，因此

$$
w_j=\frac{r_0-r_j}{r_0}.
$$

![[Holmberg2013_Fig2.png]]

<center><b>
图 2：设计变量过滤器示意图
</b></center>

注意，对所有未包含在集合 $\Omega_e$ 中的设计变量，权重均为零。从实现角度看，可以构造包含权重的矩阵 $\mathbf{W}$，使得

$$
\rho_e(\mathbf{x})=\sum_{j=1}^{n_e}W_{ej}x_j.
\tag{2}
$$

# 4 惩罚机制

为了生成黑白结构，需要引入惩罚函数，使中间设计变量值付出不成比例的代价。本文以黑白设计为目标，采用 SIMP 惩罚中间设计变量值对应的刚度，并采用类似的惩罚来处理应力。

## 4.1 刚度惩罚

从实体材料单元刚度矩阵 $\hat{\mathbf{K}}_e$ 装配整体刚度矩阵 $\mathbf{K}(\boldsymbol{\rho}(\mathbf{x}))$ 时，引入 SIMP 惩罚函数 $\eta_K(\rho_e(\mathbf{x}))$：

$$
\mathbf{K}(\boldsymbol{\rho}(\mathbf{x}))=
\sum_{e=1}^{n_e}\eta_K(\rho_e(\mathbf{x}))\hat{\mathbf{K}}_e.
$$

SIMP 惩罚函数为

$$
\eta_K(\rho_e(\mathbf{x}))=(\rho_e(\mathbf{x}))^q,
$$

其中 $q>1$ 为惩罚因子。本文取 $q=3$，已有多位作者证明该取值效果良好。

## 4.2 应力惩罚

应力评估点 $a$ 处的实体材料应力向量用 Voigt 记号写为

$$
\hat{\boldsymbol{\sigma}}_a(\mathbf{x})=
\left(
\hat{\sigma}_{ax}\ \hat{\sigma}_{ay}\ \hat{\sigma}_{az}\
\ \hat{\tau}_{axy}\ \hat{\tau}_{ayz}\ \hat{\tau}_{azx}
\right)^T.
$$

它在有限元分析中计算为

$$
\hat{\boldsymbol{\sigma}}_a(\mathbf{x})=
\mathbf{E}\mathbf{B}_a\mathbf{u}(\mathbf{x}),
$$

其中，$\mathbf{E}$ 为本构矩阵，$\mathbf{B}_a$ 为应力评估点 $a$ 对应的应变—位移矩阵。对于中间设计变量值，还要惩罚实体材料应力，从而得到惩罚后的应力量 $\boldsymbol{\sigma}_a(\mathbf{x})$：

$$
\boldsymbol{\sigma}_a(\mathbf{x})=
\eta_S(\rho_e(\mathbf{x}))\hat{\boldsymbol{\sigma}}_a(\mathbf{x}),
\tag{3}
$$

其中，$\rho_e(\mathbf{x})$ 是应力评估点 $a$ 所属单元对应的过滤变量。应力惩罚 $\eta_S(\rho_e(\mathbf{x}))$ 的构造方式，使 $\boldsymbol{\sigma}_a(\mathbf{x})$ 在设计变量取中间值时增大，从而使这些中间值承担不成比例的代价。根据本文的经验，下式效果良好：

$$
\eta_S(\rho_e(\mathbf{x}))=(\rho_e(\mathbf{x}))^{1/2}.
\tag{4}
$$

式（4）对应 Bruggi（2008）的惩罚形式，但按照 Le et al.（2010）的建议选用了特定指数。

与 Duysinx and Bendsøe（1998）等的应力计算相比，式（4）所得应力在设计变量取中间值时不具备物理意义。不过，本文追求黑白设计；该应力惩罚使 $\rho_e=1$ 时 $\boldsymbol{\sigma}_a$ 与 $\hat{\boldsymbol{\sigma}}_a$ 一致，并且

$$
\lim_{\rho_e\to 0}\boldsymbol{\sigma}_a(\mathbf{x})=\mathbf{0}.
$$

后一性质正是本文不发生奇异性问题的原因。Kočvara and Stingl（2012）最近也得出了相同观察，他们所用应力问题表述具有同样性质。

# 5 应力量度

von Mises 应力量度常用于本文所考虑的静载结构设计，因此本文在优化中采用它作为应力量度。应力评估点 $a$ 处的惩罚 von Mises 应力 $\sigma_a^{vM}(\mathbf{x})$ 是对应惩罚应力向量（3）的函数：

$$
\sigma_a^{vM}(\mathbf{x})=
\left(
\sigma_{ax}^2+\sigma_{ay}^2+\sigma_{az}^2
-\sigma_{ax}\sigma_{ay}-\sigma_{ay}\sigma_{az}-\sigma_{az}\sigma_{ax}
+3\tau_{axy}^2+3\tau_{ayz}^2+3\tau_{azx}^2
\right)^{1/2}.
\tag{5}
$$

本文讨论三种应力约束方法：局部、全局和聚类方法。局部与全局方法（Duysinx and Bendsøe 1998; Duysinx and Sigmund 1998）分别表示对模型中的每个应力评估点施加一个约束（局部），或对整个模型只施加一个应力约束（全局）。然而，两种方法在实践中都不理想：局部方法代价过高，而全局方法过于粗略。因此，本文采用聚类方法（París et al. 2010; Le et al. 2010），把应力评估点划分为多个聚类，每个聚类施加一个应力约束，由此在应力控制质量和计算成本之间取得折中。根据本文经验，即使只采用少量应力约束，也可以避免引起应力奇异性的几何形状，并在一定程度上避免应力集中。第 6 节讨论如何将应力评估点划分到聚类中，以及如何更新聚类；其中还说明，局部和全局方法都可视为聚类方法的特殊情况。

为了构造问题 $(\mathrm{P}_1)$ 和 $(\mathrm{P}_2)$ 所用的聚类应力量度，将多个应力评估点的应力归入同一聚类，并利用修正 P 范数计算单一应力量度。Yang and Chen（1996）、Le et al.（2010）以及 Duysinx and Sigmund（1998）曾采用某种相似方法，但如下文所述，本文的修正方式有所不同。第 $i$ 个聚类的 P 范数应力量度 $\sigma_i^{PN}(\mathbf{x})$ 为

$$
\sigma_i^{PN}(\mathbf{x})=
\left(
\frac{1}{N_i}\sum_{a\in\Omega_i}
\left(\sigma_a^{vM}(\mathbf{x})\right)^p
\right)^{1/p},
\tag{6}
$$

其中，$p$ 为 P 范数因子，$\Omega_i$ 为第 $i$ 个聚类中的应力评估点集合，$N_i$ 为 $\Omega_i$ 中的应力评估点数。若所有应力均相同，即 $\sigma_a^{vM}(\mathbf{x})=\sigma^{vM}$，则

$$
\begin{aligned}
\sigma_i^{PN}(\mathbf{x})
&=\left(\frac{1}{N_i}\sum_{a\in\Omega_i}
\left(\sigma_a^{vM}(\mathbf{x})\right)^p\right)^{1/p}\\
&=\left(\frac{1}{N_i}\right)^{1/p}
\left(N_i(\sigma^{vM})^p\right)^{1/p}
=\sigma^{vM},
\end{aligned}
\tag{7}
$$

即 P 范数量度能够精确表示局部应力。在其他情况下，式（6）的 $\sigma_i^{PN}(\mathbf{x})$ 会低估最大局部应力。Duysinx and Sigmund（1998）对与式（6）类似、但不含聚类方法且采用 $\epsilon$ 松弛的表达式证明了这一点。他们还证明，取 $N_i=1$ 时，该表达式始终高于最大应力。两个结果概括为

$$
\left(
\frac{1}{N_i}\sum_{a\in\Omega_i}
\left(\sigma_a^{vM}(\mathbf{x})\right)^p
\right)^{1/p}
\leq
\max_{a\in\Omega_i}\sigma_a^{vM}(\mathbf{x})
\leq
\left(
\sum_{a\in\Omega_i}
\left(\sigma_a^{vM}(\mathbf{x})\right)^p
\right)^{1/p}.
$$

由于问题 $(\mathrm{P}_1)$ 和 $(\mathrm{P}_2)$ 中的应力约束可写为

$$
\left(
\sum_{a\in\Omega_i}
\left(\sigma_a^{vM}(\mathbf{x})\right)^p
\right)^{1/p}
\leq N_i^{1/p}\bar{\sigma},
$$

可知结构中的最大局部应力低于 $N_i^{1/p}\bar{\sigma}$。然而，若构造聚类使其趋近式（7）的情形，则也能趋近所期望的 $\sigma^{vM}\leq\bar{\sigma}$。另一方面，$1/N_i$ 项相当于对限值进行内置缩放，实践证明有利于优化问题收敛。特别是在最初几次迭代中，由初始几何形状引起的应力奇异性可能使一些点具有极高应力，该项能够避免相应问题。

优化结构中的局部应力会高于应力限值，但如前所述，在这一概念设计阶段，只要几何形状能够避免应力奇异性，并且应力峰值容易消除，本文允许存在一些应力峰值。

还应注意，Le et al.（2010）以单元 $a$ 的体积为基础采用单元缩放因子，而不是式（6）中的 $1/N_i$。根据以上讨论，由于较小单元中的应力可能高于较大单元，离散方式会影响局部应力。为了使 P 范数值更接近最大局部应力，Le et al. 根据前一次迭代的应力值对当前值进行缩放。本文问题表述也可以使用这一方法；不过，若按第 6 节所述构造聚类，无论是否采用该缩放，都能得到较好的应力控制。

增大式（6）中的指数 $p$，会使 P 范数值更加接近每个聚类中的最大应力。应用 Duysinx and Sigmund（1998）给出的极限可得

$$
\lim_{p\to\infty}
\left(
\frac{1}{N_i}\sum_{a\in\Omega_i}
\left(\sigma_a^{vM}(\mathbf{x})\right)^p
\right)^{1/p}
=\max_{a\in\Omega_i}\sigma_a^{vM}(\mathbf{x}).
$$

遗憾的是，$p$ 值过高会引起数值问题。另一个极端是 $p=1$，此时得到每个聚类的平均应力。Le et al.（2010）评估了不同的 $p$ 值，Duysinx and Sigmund（1998）也进行了讨论。根据这些论文和本文测试，数值算例采用 $p=8$。

根据应力约束值和 $p$ 值，式（6）中的 $(\sigma_a^{vM}(\mathbf{x}))^p$ 可能变得非常大，从而造成数值精度问题。一种解决方法是用 $\bar{\sigma}$ 对 $\sigma_a^{vM}(\mathbf{x})$ 进行归一化，得到数学上等价的问题表述。因此，问题 $(\mathrm{P}_1)$ 和 $(\mathrm{P}_2)$ 中的应力约束 $\sigma_i^{PN}(\mathbf{x})\leq\bar{\sigma}$ 替换为

$$
\left(
\frac{1}{N_i}\sum_{a\in\Omega_i}
\left(\frac{\sigma_a^{vM}(\mathbf{x})}{\bar{\sigma}}\right)^p
\right)^{1/p}
\leq 1.
$$

# 6 应力评估点的聚类分配

采用聚类的主要目的，是把局部方法中的 $n_e$ 个约束减少为 $n_c\ll n_e$ 个聚类约束，同时仍保留控制局部应力的可能性。聚类数 $n_c$ 在很大程度上决定局部应力受到约束的程度。两个极端情形是 $n_c=1$ 和 $n_c=n_e$，分别回到全局方法和局部方法。

式（6）利用 P 范数把多个应力评估点的应力聚合为一个约束，并将应力提高到 $p$ 次幂。因此，即使其他评估点的应力可能很低，一个局部高应力也能够抬高 P 范数值。另一方面，由于存在 $1/N_i$ 项，P 范数值低于最大局部应力。显然，如何构造聚类，即哪些评估点属于集合 $\Omega_i$，会影响问题。本文提出两种将评估点划分到聚类的方法：本节后文介绍的应力水平法和分布应力法。

为了使 $\sigma_i^{PN}(\mathbf{x})$ 始终能够较好地逼近局部应力，可能需要在迭代过程中更新各聚类中的应力评估点分配。然而，改变聚类内部评估点的分配就意味着改变问题。因此，相邻迭代求解的是不同但相似的问题，整个过程实际上求解了一系列相关问题。需要注意，MMA 使用前两次迭代的设计变量来确定移动限，详见 Svanberg（1987）。更新聚类时，当前迭代的设计变量来自一个与此前变量所对应问题略有不同的问题，这可能使移动限过于保守或过于激进。不过，本文仍能收敛到可行设计，并未观察到由此产生的问题。

## 6.1 应力水平法

应力水平聚类法把应力水平相近的应力评估点归入同一聚类。该方法会使不同 $\sigma_i^{PN}(\mathbf{x})$ 值之间具有较大差异，但每个聚类内部评估点的应力尽可能接近。由于趋近式（7）的情形，P 范数量度能够较好地逼近聚类成员的应力。另一个优点是，在许多问题中，低应力水平聚类对应的应力约束最终会变为非活跃约束。

各聚类按式（8）所示方式组织。首先根据应力水平对所有应力评估点按降序排序，前 $n_e/n_c$ 个点构成聚类 1，接下来的 $n_e/n_c$ 个点构成聚类 2，依此类推。除最后一个聚类可能包含较少点外，每个聚类中的点数相同。聚类方式为

$$
\underbrace{\sigma_1\geq\sigma_2\geq\cdots\geq\sigma_{n_e/n_c}}_{\text{聚类 }1}
\geq
\underbrace{\cdots\geq\sigma_{2n_e/n_c}}_{\text{聚类 }2}
\geq\cdots\geq
\underbrace{\sigma_{(n_c-1)n_e/n_c}\geq\cdots\geq\sigma_{n_e}}_{\text{聚类 }n_c}.
\tag{8}
$$

## 6.2 分布应力法

在分布应力聚类法中，每个聚类都包含跨越整个应力范围的应力评估点，因此各聚类得到近似相同的应力值。采用这一方法的动机是希望优化更容易收敛，因为高局部应力会被数量可能很大的低局部应力所削弱。因此，式（6）的聚类应力量度会低于采用应力水平法时的值。

应力评估点同样按照应力降序排列。第一个点放入聚类 1，第二个点放入聚类 2，依此类推，直至第 $n_c$ 个点；随后将聚类计数器重置，从聚类 1 重新开始。当每次迭代都更新聚类时，该方法与 Le et al.（2010）的方法相同。其问题表述可表示为

$$
\underbrace{\sigma_1}_{\text{聚类 }1}
\geq\underbrace{\sigma_2}_{\text{聚类 }2}
\geq\cdots\geq
\underbrace{\sigma_{n_c-1}}_{\text{聚类 }(n_c-1)}
\geq\underbrace{\sigma_{n_c}}_{\text{聚类 }n_c}
\geq\underbrace{\sigma_{n_c+1}}_{\text{聚类 }1}
\geq\cdots\geq
\underbrace{\sigma_{n_e}}_{\text{聚类 }n_c}.
$$

# 7 灵敏度分析

用于求解优化问题的移动渐近线法（Svanberg 1987）需要约束和目标函数的一阶灵敏度信息。问题 $(\mathrm{P}_1)$ 中质量目标 $f_0$ 的梯度为

$$
\frac{\partial f_0}{\partial x_b}
=\sum_{e=1}^{n_e}m_e\frac{\partial\rho_e(\mathbf{x})}{\partial x_b}
=\sum_{e=1}^{n_e}m_eW_{eb}.
\tag{9}
$$

其中，$W_{eb}$ 为式（2）定义的过滤权重。可以看到，由于过滤器的作用，质量梯度受到相邻设计变量影响。不过，对于本文数值算例，每个单元的尺寸和材料均相同，所有实体单元质量相等，即 $m_e=m$，因而式（9）可写为

$$
\frac{\partial f_0}{\partial x_b}
=\sum_{e=1}^{n_e}m_eW_{eb}
=m\sum_{e=1}^{n_e}W_{eb}=m,
$$

因为

$$
\sum_{e=1}^{n_e}W_{eb}=1.
$$

问题 $(\mathrm{P}_2)$ 和 $(\mathrm{P}_3)$ 中的柔顺度目标 $C=\frac{1}{2}\mathbf{F}^T\mathbf{u}(\mathbf{x})$ 具有一个著名的自伴随梯度：

$$
\frac{\partial C(\mathbf{x})}{\partial x_b}
=-\frac{1}{2}\mathbf{u}^T(\mathbf{x})
\frac{\partial\mathbf{K}(\boldsymbol{\rho}(\mathbf{x}))}{\partial x_b}
\mathbf{u}(\mathbf{x}),
$$

详见 Christensen and Klarbring（2008）。

应力约束是式（6）中的 P 范数应力，其梯度由链式法则得到：

$$
\begin{aligned}
\frac{\partial\sigma_i^{PN}(\mathbf{x})}{\partial x_b}
&=\sum_{a\in\Omega_i}
\frac{\partial\sigma_i^{PN}(\mathbf{x})}{\partial\sigma_a^{vM}}
\frac{\partial\sigma_a^{vM}(\mathbf{x})}{\partial x_b}\\
&=\sum_{a\in\Omega_i}
\frac{\partial\sigma_i^{PN}(\mathbf{x})}{\partial\sigma_a^{vM}}
\left(\frac{\partial\sigma_a^{vM}(\mathbf{x})}{\partial\boldsymbol{\sigma}_a}\right)^T
\frac{\partial\boldsymbol{\sigma}_a(\mathbf{x})}{\partial x_b}.
\end{aligned}
\tag{10}
$$

式（10）中的各导数在以下小节中计算。

## 7.1 P 范数对 von Mises 应力的导数

式（10）中的 $\partial\sigma_i^{PN}(\mathbf{x})/\partial\sigma_a^{vM}$ 通过对式（6）求导得到：

$$
\begin{aligned}
\frac{\partial\sigma_i^{PN}(\mathbf{x})}{\partial\sigma_a^{vM}}
&=\frac{1}{p}
\left(\frac{1}{N_i}\sum_{a\in\Omega_i}
\left(\sigma_a^{vM}(\mathbf{x})\right)^p\right)^{1/p-1}
\frac{p}{N_i}\left(\sigma_a^{vM}(\mathbf{x})\right)^{p-1}\\
&=\left(\frac{1}{N_i}\sum_{a\in\Omega_i}
\left(\sigma_a^{vM}(\mathbf{x})\right)^p\right)^{1/p-1}
\frac{1}{N_i}\left(\sigma_a^{vM}(\mathbf{x})\right)^{p-1}.
\end{aligned}
$$

## 7.2 von Mises 应力的导数

von Mises 应力（5）对各应力分量的导数为

$$
\begin{aligned}
\frac{\partial\sigma_a^{vM}(\mathbf{x})}{\partial\sigma_{ax}}
&=\frac{1}{2\sigma_a^{vM}(\mathbf{x})}
\left(2\sigma_{ax}(\mathbf{x})-\sigma_{ay}(\mathbf{x})-\sigma_{az}(\mathbf{x})\right),\\
\frac{\partial\sigma_a^{vM}(\mathbf{x})}{\partial\sigma_{ay}}
&=\frac{1}{2\sigma_a^{vM}(\mathbf{x})}
\left(2\sigma_{ay}(\mathbf{x})-\sigma_{ax}(\mathbf{x})-\sigma_{az}(\mathbf{x})\right),\\
\frac{\partial\sigma_a^{vM}(\mathbf{x})}{\partial\sigma_{az}}
&=\frac{1}{2\sigma_a^{vM}(\mathbf{x})}
\left(2\sigma_{az}(\mathbf{x})-\sigma_{ax}(\mathbf{x})-\sigma_{ay}(\mathbf{x})\right),\\
\frac{\partial\sigma_a^{vM}(\mathbf{x})}{\partial\tau_{axy}}
&=\frac{3}{\sigma_a^{vM}(\mathbf{x})}\tau_{axy}(\mathbf{x}),\\
\frac{\partial\sigma_a^{vM}(\mathbf{x})}{\partial\tau_{ayz}}
&=\frac{3}{\sigma_a^{vM}(\mathbf{x})}\tau_{ayz}(\mathbf{x}),\\
\frac{\partial\sigma_a^{vM}(\mathbf{x})}{\partial\tau_{azx}}
&=\frac{3}{\sigma_a^{vM}(\mathbf{x})}\tau_{azx}(\mathbf{x}).
\end{aligned}
$$

## 7.3 应力分量的导数

惩罚应力向量（3）对设计变量 $x_b$ 的导数为

$$
\begin{aligned}
\frac{\partial\boldsymbol{\sigma}_a(\mathbf{x})}{\partial x_b}
&=\sum_{r=1}^{n_a}
\frac{\partial\boldsymbol{\sigma}_a}{\partial\rho_r}
\frac{\partial\rho_r(\mathbf{x})}{\partial x_b}\\
&=\sum_{r=1}^{n_a}
\frac{\partial\eta_S(\rho_e(\mathbf{x}))}{\partial\rho_r}
\frac{\partial\rho_r(\mathbf{x})}{\partial x_b}
\mathbf{E}\mathbf{B}_a\mathbf{u}(\mathbf{x})
+\eta_S(\rho_e(\mathbf{x}))\mathbf{E}\mathbf{B}_a
\frac{\partial\mathbf{u}(\mathbf{x})}{\partial x_b},
\end{aligned}
\tag{11}
$$

其中，$n_a$ 为应力评估点总数；采用式（4）的惩罚时，只有 $r=e$ 时 $\partial\eta_S(\rho_e(\mathbf{x}))/\partial\rho_r\neq 0$。因此可去掉求和，式（11）化为

$$
\frac{\partial\boldsymbol{\sigma}_a(\mathbf{x})}{\partial x_b}
=\frac{\partial\eta_S(\rho_e(\mathbf{x}))}{\partial\rho_e}
\frac{\partial\rho_e(\mathbf{x})}{\partial x_b}
\mathbf{E}\mathbf{B}_a\mathbf{u}(\mathbf{x})
+\eta_S(\rho_e(\mathbf{x}))\mathbf{E}\mathbf{B}_a
\frac{\partial\mathbf{u}(\mathbf{x})}{\partial x_b}.
\tag{12}
$$

## 7.4 伴随法

本问题的设计变量 $\mathbf{x}$ 数量很大，但借助聚类可以把约束数保持在适中水平。因此，伴随法更适合求解式（10）。式（12）中的 $\partial\mathbf{u}(\mathbf{x})/\partial x_b$ 由整体状态方程（1）计算。应用链式法则得到

$$
\sum_{r=1}^{n_e}
\frac{\partial\mathbf{K}(\boldsymbol{\rho}(\mathbf{x}))}{\partial\rho_r}
\frac{\partial\rho_r(\mathbf{x})}{\partial x_b}
\mathbf{u}(\mathbf{x})
+\mathbf{K}(\boldsymbol{\rho}(\mathbf{x}))
\frac{\partial\mathbf{u}(\mathbf{x})}{\partial x_b}=\mathbf{0},
$$

由此可得

$$
\frac{\partial\mathbf{u}(\mathbf{x})}{\partial x_b}
=-\mathbf{K}^{-1}(\boldsymbol{\rho}(\mathbf{x}))
\left[
\sum_{r=1}^{n_e}
\frac{\partial\mathbf{K}(\boldsymbol{\rho}(\mathbf{x}))}{\partial\rho_r}
\frac{\partial\rho_r(\mathbf{x})}{\partial x_b}
\mathbf{u}(\mathbf{x})
\right].
\tag{13}
$$

将式（13）代入式（12），再将式（12）代入式（10），得到

$$
\begin{aligned}
\frac{\partial\sigma_i^{PN}(\mathbf{x})}{\partial x_b}
=\sum_{a\in\Omega_i}
\Bigg\{&
\frac{\partial\sigma_i^{PN}(\mathbf{x})}{\partial\sigma_a^{vM}}
\left(\frac{\partial\sigma_a^{vM}(\mathbf{x})}{\partial\boldsymbol{\sigma}_a}\right)^T\\
&\times\Bigg[
\frac{\partial\eta_S(\rho_e(\mathbf{x}))}{\partial\rho_e}
\frac{\partial\rho_e(\mathbf{x})}{\partial x_b}
\mathbf{E}\mathbf{B}_a\mathbf{u}(\mathbf{x})\\
&\quad-\eta_S(\rho_e(\mathbf{x}))\mathbf{E}\mathbf{B}_a
\mathbf{K}^{-1}(\boldsymbol{\rho}(\mathbf{x}))
\left(
\sum_{r=1}^{n_e}
\frac{\partial\mathbf{K}(\boldsymbol{\rho}(\mathbf{x}))}{\partial\rho_r}
\frac{\partial\rho_r(\mathbf{x})}{\partial x_b}
\mathbf{u}(\mathbf{x})
\right)
\Bigg]\Bigg\}.
\end{aligned}
\tag{14}
$$

现在定义伴随变量 $\boldsymbol{\lambda}_i$：

$$
\boldsymbol{\lambda}_i^T=
\sum_{a\in\Omega_i}
\frac{\partial\sigma_i^{PN}(\mathbf{x})}{\partial\sigma_a^{vM}}
\left(\frac{\partial\sigma_a^{vM}(\mathbf{x})}{\partial\boldsymbol{\sigma}_a}\right)^T
\mathbf{E}\mathbf{B}_a
\mathbf{K}^{-1}(\boldsymbol{\rho}(\mathbf{x})),
$$

这意味着可由伴随方程计算：

$$
\mathbf{K}(\boldsymbol{\rho}(\mathbf{x}))\boldsymbol{\lambda}_i
=\sum_{a\in\Omega_i}
\frac{\partial\sigma_i^{PN}(\mathbf{x})}{\partial\sigma_a^{vM}}
\mathbf{B}_a^T\mathbf{E}^T
\frac{\partial\sigma_a^{vM}(\mathbf{x})}{\partial\boldsymbol{\sigma}_a}.
$$

将伴随变量代入式（14），最终得到梯度

$$
\begin{aligned}
\frac{\partial\sigma_i^{PN}(\mathbf{x})}{\partial x_b}
=\sum_{a\in\Omega_i}
&\frac{\partial\sigma_i^{PN}(\mathbf{x})}{\partial\sigma_a^{vM}}
\left(\frac{\partial\sigma_a^{vM}(\mathbf{x})}{\partial\boldsymbol{\sigma}_a}\right)^T
\frac{\partial\eta_S(\rho_e(\mathbf{x}))}{\partial\rho_e}
\frac{\partial\rho_e(\mathbf{x})}{\partial x_b}
\mathbf{E}\mathbf{B}_a\mathbf{u}(\mathbf{x})\\
&-\eta_S(\rho_e(\mathbf{x}))\boldsymbol{\lambda}_i^T
\left[
\sum_{r=1}^{n_e}
\frac{\partial\mathbf{K}(\boldsymbol{\rho}(\mathbf{x}))}{\partial\rho_r}
\frac{\partial\rho_r(\mathbf{x})}{\partial x_b}
\mathbf{u}(\mathbf{x})
\right],
\end{aligned}
$$

其中，$\partial\sigma_i^{PN}(\mathbf{x})/\partial\sigma_a^{vM}$ 和 $\partial\sigma_a^{vM}(\mathbf{x})/\partial\boldsymbol{\sigma}_a$ 分别在第 7.1 节和第 7.2 节中推导。

# 8 建模要点


## 8.1 载荷施加

优化问题采用应力约束时，必须以适合应力计算的方式向结构施加载荷。传统问题 $(\mathrm{P}_3)$ 中可能足够的点载荷，会产生难以降低的高局部应力，即使整个设计域都变成实体也可能如此。该高应力会影响聚类，从而影响最终设计。因此，载荷必须分配到多个节点，使载荷施加区域足够大，以将应力保持在应力限值以下。另一种方法是从设计变量集合中排除载荷附近的单元：这些单元保持为实体结构单元，不参与优化。图 3 给出有限元网格的一个局部，载荷施加在右上角；灰色单元被排除在优化问题之外。

![[Holmberg2013_Fig3.png]]

<center><b>
图 3：以灰色标出的排除单元
</b></center>

## 8.2 网格划分

另一个需要考虑的问题是离散化，即单元尺寸。设计变量过滤器保证结构构件的厚度约大于 $2r_0$。因此，在采用应力约束时，为得到黑白设计，选择单元尺寸必须同时考虑应力限值和过滤半径。如果单元过大，可能得到这样的设计：由中间设计变量值构成的结构构件中，应力低于限值，但由于过滤器的作用，构件无法进一步减薄。此时解可能包含具有中间设计变量值的结构构件，而更细网格则能够形成更薄的实体构件。

# 9 算例

本节给出上述应力约束方法应用于二维平面应力结构的算例。该方法已在有限元程序 TRINITAS（Torstenfelt 2012）中实现。除基于柔顺度的设计外，所有设计的初始状态均为 $\rho_e(\mathbf{x})=0.5$。本文所示最终设计均在收敛之后继续进行了大量迭代。表 1 和表 2 所示最终解附有收敛曲线。与 Svanberg（2002）的建议值相比，本文缩小了 MMA 的移动限，使求解器更为保守。需要指出，不同 MMA 参数会产生不同最终解，这也是本文选择较保守求解器设置的原因。如第 6 节所述，重新聚类时并不重置 MMA。MMA 的移动限根据前几次迭代的设计变量值确定；重新聚类时，这些变量对应于一个略有不同的问题，但本文仍然收敛到可行设计。

图中显示过滤变量 $\boldsymbol{\rho}$ 和惩罚 von Mises 应力 $\sigma_a^{vM}$。图像没有进行后处理：黑色表示过滤变量为 1，灰色表示其取最小值 $\epsilon$。应力云图应以彩色查看；蓝—绿色范围表示应力低于或等于应力限值，黄—红色范围表示应力高于限值。

## 9.1 L 形梁

L 形梁是应力约束拓扑优化中的常用测试算例，可参见 Duysinx and Bendsøe（1998）、Duysinx and Sigmund（1998）、Le et al.（2010）和 París et al.（2009）等；采用水平集方法优化 L 形梁的工作可参见 Allaire and Jouve（2008）、Amstutz and Novotny（2010）以及 Guo et al.（2011）。L 形梁设计域包含一个具有初始几何应力奇异性的内角，如图 4 所示。这类设计域适合工业应用，例如 L 形梁可以作为某一设备的连接件，而内角可能源于避让其他设备的要求，也可能源于设备本身的形状。拓扑优化是概念设计工具，因此设计域应易于构造和划分网格。为此，设计域内角没有设置圆角。

![[Holmberg2013_Fig4.png]]

<center><b>
图 4：L 形梁问题的几何形状
</b></center>

L 形梁的尺寸见图 4，其中 $L=200\ \mathrm{mm}$，结构厚度为 $1\ \mathrm{mm}$。设计域采用 6400 个等尺寸四节点单元划分，每个单元设置一个应力评估点。应力在超收敛点处评估；对于该单元类型，超收敛点位于单元形心。材料采用典型航空铝材，材料参数为：Young 模量 $71{,}000\ \mathrm{MPa}$，密度 $2.8\times10^{-9}\ \mathrm{ton/mm^3}$，Poisson 比 0.33，屈服极限 $350\ \mathrm{MPa}$；优化中的应力限值同样取 $350\ \mathrm{MPa}$。数值算例采用 10 个聚类，即 10 个应力约束；不过，如图 5 所示，即使约束数量低得多，也能得到避免高应力集中的设计。

按照图 4 施加 $1500\ \mathrm{N}$ 点载荷，载荷下方 $3\times2$ 个单元不属于设计空间，参见图 3。设计变量过滤器的过滤半径取 $r_0=1.5$ 倍单元尺寸。

表 1 和表 2 给出问题 $(\mathrm{P}_1)$ 的 L 形梁解，比较两种聚类方法和不同重新聚类频率。


<center><b>
表 1：问题 $(\mathrm{P}_1)$ 的 L 形梁——采用“应力水平”聚类法及不同更新频率
</b></center>

![[Holmberg2013_Table1.png]]

| 重新聚类频率 | 每次迭代 | 每 50 次迭代 | 不重新聚类 |
|---|---:|---:|---:|
| 质量 $M$（$\mathrm{kg}\times10^{-3}$） | 24.76 | 23.75 | 20.11 |
| 柔顺度 $C$（$\mathrm{N\,mm}$） | 10,330 | 10,820 | 15,105 |

如第 6 节所述，采用应力水平聚类法并在每次迭代中更新聚类时，会趋近式（7）的情形。表 1 也说明，这一组合从平均意义上获得了最好的局部应力控制和更均匀的应力分布。每 50 次迭代更新聚类时，局部应力控制稍差；完全不更新聚类时，结构中很大比例区域的应力过高。虽然应力约束仍然得到满足，但聚类在第一次迭代中构造，此后 $\sigma_i^{PN}$ 已不能很好地逼近局部应力。这也解释了为什么质量可以更低，而柔顺度更高。不过，这种设置能够更有效地避开奇异点：右侧竖向构件远离边界，从而允许形成更大的圆角。

还可以看到，表 1 中的收敛曲线在每次迭代都更新聚类时会出现小幅振荡；每 50 次迭代更新时，曲线会在更新时发生跳变；不重新聚类时，曲线相对平滑。

<center><b>
表 2：问题 $(\mathrm{P}_1)$ 的 L 形梁——采用“分布应力”聚类法及不同更新频率
</b></center>

![[Holmberg2013_Table2.png]]

| 重新聚类频率 | 每次迭代 | 每 50 次迭代 | 不重新聚类 |
|---|---:|---:|---:|
| 质量 $M$（$\mathrm{kg}\times10^{-3}$） | 20.63 | 20.67 | 20.66 |
| 柔顺度 $C$（$\mathrm{N\,mm}$） | 13,277 | 12,999 | 12,828 |

表 2 采用相同的重新聚类频率，但使用分布应力法，聚类由最高与最低应力的混合构成。正如预期，其局部应力控制不如应力水平法，不同重新聚类频率得到的设计也非常相似。

![[Holmberg2013_Fig5.png]]

<center><b>
图 5：“应力水平”法仅采用三个应力约束并在每次迭代重新聚类的算例
</b></center>

## 9.2 MBB 梁

MBB 梁是拓扑优化中的另一个常用算例。本文利用对称性，只对梁的右半部分建模。材料、载荷大小和应力限值均与 L 形梁相同。点载荷施加于梁的中心，边界条件和尺寸见图 6，其中 $L=100\ \mathrm{mm}$，厚度为 $1\ \mathrm{mm}$。设计域由 4800 个单元划分，应力约束采用 10 个聚类。设计变量过滤半径略大于 L 形梁：实践表明，取 $r_0=2$ 倍单元尺寸，可得到不会包含过多细小结构构件的解。与前述算例相同，载荷附近的单元不作为设计变量，以避免应力集中。

![[Holmberg2013_Fig6.png]]

<center><b>
图 6：MBB 问题的几何形状
</b></center>

与 L 形梁相同，采用两种聚类方法和不同重新聚类频率求解问题 $(\mathrm{P}_1)$，结果见表 3 和表 4。两种聚类方法和重新聚类频率之间的差异，与 L 形梁的结果类似。从应力角度看，应力水平法并在每次迭代重新聚类时得到的设计最好。

<center><b>
表 3：问题 $(\mathrm{P}_1)$ 的 MBB 梁——采用“应力水平”聚类法及不同更新频率
</b></center>

![[Holmberg2013_Table3.png]]

| 重新聚类频率 | 每次迭代 | 每 50 次迭代 | 不重新聚类 |
|---|---:|---:|---:|
| 质量 $M$（$\mathrm{kg}\times10^{-3}$） | 27.66 | 25.85 | 24.28 |
| 柔顺度 $C$（$\mathrm{N\,mm}$） | 11,535 | 11,728 | 15,000 |

<center><b>
表 4：问题 $(\mathrm{P}_1)$ 的 MBB 梁——采用“分布应力”聚类法及不同更新频率
</b></center>

![[Holmberg2013_Table4.png]]

| 重新聚类频率 | 每次迭代 | 每 50 次迭代 | 不重新聚类 |
|---|---:|---:|---:|
| 质量 $M$（$\mathrm{kg}\times10^{-3}$） | 23.03 | 25.42 | 24.76 |
| 柔顺度 $C$（$\mathrm{N\,mm}$） | 16,035 | 15,885 | 15,105 |

## 9.3 三种问题表述的比较

下面比较问题 $(\mathrm{P}_1)$、$(\mathrm{P}_2)$ 和 $(\mathrm{P}_3)$，以说明三者结果的差异以及应力约束的作用。表 5 中，问题 $(\mathrm{P}_1)$ 的结果沿用表 2 的结果，并把该问题所得最优质量作为问题 $(\mathrm{P}_2)$ 和 $(\mathrm{P}_3)$ 的质量约束限值。

<center><b>
表 5：三种问题表述的比较
</b></center>

![[Holmberg2013_Table5.png]]

| 算例 | 指标 | $(\mathrm{P}_1)$ | $(\mathrm{P}_2)$ | $(\mathrm{P}_3)$ |
|---|---|---:|---:|---:|
| L 形梁 | 柔顺度 $C$ | 13,276 | 14,347 | 10,960 |
| MBB 梁 | 柔顺度 $C$ | 16,035 | 16,530 | 13,300 |

对于 L 形梁，问题 $(\mathrm{P}_3)$ 所得拓扑存在本质差异：材料布置在内角处，形成几何应力奇异性，需要进行大幅修改才能消除。正如预期，问题 $(\mathrm{P}_1)$ 的最大应力更低，应力在结构中的分布也均匀得多，但代价是刚度低于问题 $(\mathrm{P}_3)$。因此，在已知允许质量且应力和刚度都很重要时，可以采用问题 $(\mathrm{P}_2)$。需要指出，当允许质量像表 5 一样低时，问题 $(\mathrm{P}_2)$ 可能难以找到可行设计，这也是其柔顺度高于问题 $(\mathrm{P}_1)$ 的原因。因此，建议采用略高的质量，如图 7 所示，这能更合理地发挥问题 $(\mathrm{P}_2)$ 的作用。

![[Holmberg2013_Fig7.png]]

<center><b>
图 7：问题 $(\mathrm{P}_2)$ 的允许质量比表 5 高约 $5\%$，柔顺度为 $C=12{,}336$
</b></center>

对于 MBB 梁同样可以看到，采用问题 $(\mathrm{P}_1)$ 时，所得拓扑不同于问题 $(\mathrm{P}_3)$ 的柔顺度设计。梁高从加载所在的对称线向右角支座逐渐减小。这是因为载荷 $F$ 产生弯矩，并在梁内由力偶承担。弯矩在施加载荷的对称线上达到最大，随后朝支座方向线性减小至零，因此可以向支座方向逐渐降低梁高以减小质量。

采用问题 $(\mathrm{P}_2)$ 时，所得设计更接近问题 $(\mathrm{P}_3)$ 的设计，但应力更低。由于本例采用的允许质量很低，最终收敛解中的应力约束并不可行。不过，与 L 形梁相同，略微提高质量即可得到柔顺度更低的可行解。

最后，在求解问题 $(\mathrm{P}_1)$ 时，本文还尝试从问题 $(\mathrm{P}_3)$ 的 L 形梁收敛解开始优化，以考察进一步优化能否解决内角处的高应力问题。优化算法未能从该起点找到可行解，最终设计与表 5 中问题 $(\mathrm{P}_3)$ 的最终设计相似。

## 9.4 排除的单元

第 8 节讨论了在施加点载荷时，从优化问题中排除选定单元以避免应力集中的做法。排除单元仍然影响设计变量过滤器，这有助于使相邻单元趋于实体；同时，载荷也以不同方式分布，从而可以把解推向所期望的设计。如果不排除单元，而是把载荷分布到三个节点，则可以得到对所表述问题而言更优的设计；但从物理角度看，该设计几乎没有用途，因为载荷方向的微小扰动就可能使结构倒塌。表 6 左图给出一个例子，右图来自表 1。避免不稳定薄弱结构的另一种方法，是增加刚度、屈曲或特征频率约束，或者采用问题 $(\mathrm{P}_2)$。

<center><b>
表 6：排除单元与否所得的不同设计（左：不排除单元；右：排除单元）
</b></center>

![[Holmberg2013_Table6.png]]

# 10 结论

本文提出并评估了一种应力约束拓扑优化方法。该方法已通过数值验证，结果具有良好吸引力。本文给出了理论背景和灵敏度分析，并使理论部分保持对三维结构及其他单元类型的适用性。数值算例表明，尽管优化问题更复杂、计算代价更高，但拓扑优化中的应力约束能够得到更接近最终工程设计的方案，从而简化并加快后续达到可制造产品所需的设计工作。与问题 $(\mathrm{P}_2)$ 和 $(\mathrm{P}_3)$ 相比，问题 $(\mathrm{P}_1)$ 无需人工试验多个允许质量值，而是直接得到给定约束下的最小质量。由于问题 $(\mathrm{P}_1)$ 没有刚度要求，所得设计的柔顺度可能较高。因此，可以增加刚度、屈曲或特征频率约束；另一种选择是采用问题 $(\mathrm{P}_2)$，在给定质量下得到同时受柔顺度和应力约束的结构。

根据第 5 节、第 6 节的讨论以及表 1 至表 4 中 L 形梁和 MBB 梁的结果，应力水平法结合重新聚类是优选方法。该组合能够生成简单的设计，有效避免应力集中，并且只有少量点的应力高于应力限值。

由表 5 可见，采用应力约束时得到的拓扑不同于传统的基于刚度的问题 $(\mathrm{P}_3)$。因此，仅以最大刚度优化结构，再通过局部形状优化消除应力集中并不充分；本文建议从一开始就考虑应力约束。

# 参考文献

- Allaire G, Jouve F (2008) Minimum stress optimal design with the level set method. *Eng Anal Bound Elem* 32(11):909–918.
- Amstutz S, Novotny A (2010) Topological optimization of structures subject to von Mises stress constraints. *Struct Multidisc Optim* 41(3):407–420.
- Bendsøe M (1989) Optimal shape design as a material distribution problem. *Struct Multidisc Optim* 1(4):193–202.
- Bendsøe M, Kikuchi N (1988) Generating optimal topologies in structural design using a homogenization method. *Comput Methods Appl Mech Eng* 71(2):197–224.
- Bendsøe MP, Sigmund O (2003) *Topology optimization—theory, methods, and applications*, 2nd edn. Springer, Berlin.
- Bendsøe M, Ben-Tal A, Zowe J (1994) Optimization methods for truss geometry and topology design. *Struct Multidisc Optim* 7(3):141–159.
- Bruggi M (2008) On an alternative approach to stress constraints relaxation in topology optimization. *Struct Multidisc Optim* 36(2):125–141.
- Bruns T, Tortorelli D (2001) Topology optimization of non-linear elastic structures and compliant mechanisms. *Comput Methods Appl Mech Eng* 190(26–27):3443–3459.
- Cheng G, Guo X (1997) $\epsilon$-relaxed approach in structural topology optimization. *Struct Multidisc Optim* 13(4):258–266.
- Christensen P, Klarbring A (2008) *An introduction to structural optimization*, vol 153. Springer, Berlin.
- Cook R, Malkus D, Plesha M, Witt R (2002) *Concepts and applications of finite element analysis*. Wiley, New York.
- Dorn W, Gomory R, Greenberg H (1964) Automatic design of optimal structures. *J Méc* 3(6):25–52.
- Duysinx P, Bendsøe M (1998) Topology optimization of continuum structures with local stress constraints. *Int J Numer Methods Eng* 43(8):1453–1478.
- Duysinx P, Sigmund O (1998) New developments in handling optimal stress constraints in optimal material distribution. In: 7th AIAA/USAF/NASA/ISSMO symposium on multidisciplinary design optimization, AIAA Paper 98-4906, pp 1501–1509.
- Guo X, Cheng G, Yamazaki K (2001) A new approach for the solution of singular optima in truss topology optimization with stress and local buckling constraints. *Struct Multidisc Optim* 22(5):364–373.
- Guo X, Zhang W, Wang M, Wei P (2011) Stress-related topology optimization via level set approach. *Comput Methods Appl Mech Eng* 200(47):3439–3452.
- Hughes T (1987) *The finite element method: linear static and dynamic finite element analysis*. Prentice-Hall, Englewood Cliffs.
- Kirsch U (1990) On singular topologies in optimum structural design. *Struct Multidisc Optim* 2(3):133–142.
- Kočvara M, Stingl M (2012) Solving stress constrained problems in topology and material optimization. *Struct Multidisc Optim* 46(1):1–15.
- Le C, Norato J, Bruns T, Ha C, Tortorelli D (2010) Stress-based topology optimization for continua. *Struct Multidisc Optim* 41(4):605–620.
- París J, Navarrina F, Colominas I, Casteleiro M (2009) Topology optimization of continuum structures with local and global stress constraints. *Struct Multidisc Optim* 39(4):419–437.
- París J, Navarrina F, Colominas I, Casteleiro M (2010) Block aggregation of stress constraints in topology optimization of structures. *Adv Eng Softw* 41(3):433–441.
- Rozvany G, Birker T (1994) On singular topologies in exact layout optimization. *Struct Multidisc Optim* 8(4):228–235.
- Rozvany G, Zhou M, Birker T (1992) Generalized shape optimization without homogenization. *Struct Multidisc Optim* 4(3):250–252.
- Svanberg K (1987) The method of moving asymptotes—a new method for structural optimization. *Int J Numer Methods Eng* 24(2):359–373.
- Svanberg K (2002) A class of globally convergent optimization methods based on conservative convex separable approximations. *SIAM J Optim* 12(2):555–573.
- Svanberg K, Werme M (2007) Sequential integer programming methods for stress constrained topology optimization. *Struct Multidisc Optim* 34(4):277–299.
- Sved G, Ginos Z (1968) Structural optimization under multiple loading. *Int J Mech Sci* 10(10):803–805.
- Torstenfelt B (2012) The TRINITAS project. http://www.solid.iei.liu.se/Offered_services/Trinitas. Accessed 4 Sept 2012.
- Werme M (2008) Using the sequential linear integer programming method as a post-processor for stress-constrained topology optimization problems. *Int J Numer Methods Eng* 76(10):1544–1567.
- Yang R, Chen C (1996) Stress-based topology optimization. *Struct Multidisc Optim* 12(2):98–105.
