---
title: "翻译：PolyStress: a Matlab implementation for local stress-constrained topology optimization using the augmented Lagrangian method"
tags:
  - translation
  - topology-optimization
  - stress-constraints
status: "read"
date_created: 2026-09-07
date_updated: 2026-09-08
source: "../sources/GiraldoLondono2021-polystress-stress-constrained.pdf"
citekey: "GiraldoLondono2021-polystress"
language: "zh-CN"
---

# PolyStress: a Matlab implementation for local stress-constrained topology optimization using the augmented Lagrangian method

---

# 信息

- **中文标题**：PolyStress：基于增广拉格朗日方法的局部应力约束拓扑优化 Matlab 实现
- **作者**：Oliver Giraldo-Londoño; Glaucio H. Paulino
- **单位**：佐治亚理工学院土木与环境工程学院；密苏里大学土木与环境工程系
- **期刊**：*Structural and Multidisciplinary Optimization* (SMO)
- **卷 / 期 / 页码**：63: 2065–2097
- **年份**：2021
- **收稿 / 修回 / 接收**：2019-12-28 / 2020-06-03 / 2020-10-06
- **在线发表**：2021-02-10
- **DOI**：10.1007/s00158-020-02760-8
- **责任编辑**：Ole Sigmund
- **题献**：献给 Martin Philip Bendsøe 教授（1955-12-29 至今）
- **电子补充材料**：在线版本包含仅向授权用户开放的补充材料。

# 摘要

本文介绍 PolyStress：一个考虑线性与材料非线性问题、用于局部应力约束拓扑优化的 Matlab 实现。PolyStress 建立在 PolyTop 之上；PolyTop 是一个面向非结构多边形有限元、用于柔顺度最小化的教学代码。为求解非线性弹性问题，本文实现了 Newton-Raphson 格式，可处理由给定应变能密度函数定义的非线性材料模型。为求解应力约束问题，本文采用基于增广拉格朗日方法的方案；该方案与应力的局部定义保持一致，不使用传统约束聚合技术。本文讨论应力约束问题的若干理论方面，包括所实现增广拉格朗日方法的细节；还介绍作为电子补充材料提供的 PolyStress Matlab 实现。文中给出多个数值算例，以展示 PolyStress 求解应力约束拓扑优化问题的能力，以及它容纳任意非线性材料模型的模块化特性。全文另有六个附录，其中附录 A 给出一组基准算例库；这些算例均有详细说明，可供读者开展超出本文范围的进一步研究。

**关键词**：无聚合方法；局部应力约束；拓扑优化；增广拉格朗日；Matlab

# 1 引言

1988 年：Bendsøe 和 Kikuchi（1988）的里程碑式论文正是在这一年发表，它促成了现代拓扑优化框架的形成。后来，Bendsøe 教授又撰写了那本奠基性的专著（Bendsøe 1995），以统一方式介绍连续体与离散结构的拓扑、形状和材料设计方法，为新研究者进入该领域打开了大门。因此，这本专著对推动该领域的发展产生了重大影响。受 Bendsøe 开放科学精神的启发，我们希望本文及其配套软件 PolyStress 能邀请更多研究者采用与连续介质力学一致的局部方法研究应力约束拓扑优化。

本文属于一系列采用 Matlab 编写、面向非结构多边形有限元网格的拓扑优化教学代码（Talischi et al. 2012a, 2012b; Pereira et al. 2016; Sanders et al. 2018）。该系列的第一篇论文是 PolyTop（Talischi et al. 2012b），用于求解非结构多边形有限元上的柔顺度最小化问题；配套网格生成代码 PolyMesher 则由 Talischi et al.（2012a）给出。由于 PolyTop 采用模块化结构，只需修改拓扑优化程序或分析程序，便可求解多种拓扑优化问题。例如，PolyFluid（Pereira et al. 2016）通过少量修改分析程序，构成了求解 Stokes 流功率耗散拓扑优化的代码；PolyMat（Sanders et al. 2018）则通过修改 PolyTop，求解可能含有多个体积约束的多材料结构柔顺度最小化问题。

本文沿用 PolyTop 的总体结构开发 PolyStress，面向考虑材料非线性的局部应力约束拓扑优化。为求解应力约束问题，我们利用 PolyTop 的模块化结构修改优化程序，实现增广拉格朗日（augmented Lagrangian, AL）方法（Bertsekas 1999; Nocedal and Wright 2006）。该方法能够按照应力的局部定义求解问题，无需采用约束聚合技术。同时，我们用 Newton-Raphson 格式替换标准有限元分析程序，以求解考虑材料非线性的状态方程。非线性有限元代码采用模块化编写方式，可以嵌入任意材料模型。

本文受到 Martin P. Bendsøe 教授在计算设计优化与应用数学领域开创性贡献的启发（Bendsøe 1989）。例如，Duysinx 和 Bendsøe（1998）坚持“约束的局部性质”，本文遵循的正是这一一致性思路。

本文其余部分组织如下：第 2 节在连续统框架下给出应力约束拓扑优化问题，第 3 节讨论问题离散化；第 4 节介绍 AL 方法及本文实现的 AL 公式，第 5 节讨论灵敏度分析；第 6 节说明 PolyStress 的 Matlab 实现，第 7 节给出多个算例；第 8 节为说明，第 9 节为结论。随后给出若干附录：附录 A 提供基准算例库，其余附录集中展示 Matlab 代码的关键部分。

# 2 连续统设定下的拓扑优化问题

本节在连续统框架下介绍局部应力约束拓扑优化的公式。首先说明具有一般目标函数和约束函数的经典连续体拓扑优化问题；随后仍在连续统框架下聚焦应力约束问题，给出问题陈述及应力约束定义，并在下一节将其离散化；最后讨论本文采用的应力约束定义，即多项式消失约束。

## 2.1 一般优化问题

在一般二维拓扑优化问题中，我们要寻找结构的形状 $\omega\subseteq\mathbb{R}^2$，使给定目标函数 $f(\omega,\boldsymbol{u}_\omega)$ 最小，同时满足约束 $g_j(\omega,\boldsymbol{u}_\omega)\leq0$，$j=1,\ldots,K$。形状 $\omega$ 通常定义在扩展域 $\Omega$ 上，且 $\omega\subseteq\Omega\subseteq\mathbb{R}^2$（见图 1）。一般而言，目标函数和约束均依赖结构形状 $\omega$，也依赖某个边值问题的解 $\boldsymbol{u}_\omega$。相应优化问题写为

$$
\begin{aligned}
\inf_{\omega\in\mathcal O}\quad &f(\omega,\boldsymbol{u}_\omega)\\
\text{s.t.}\quad &g_j(\omega,\boldsymbol{u}_\omega)\leq0,\quad j=1,\ldots,K,
\end{aligned}
\tag{1}
$$

其中，$\mathcal O$ 表示容许形状空间。就本文讨论而言，$\boldsymbol{u}_\omega\in\mathcal V_\omega$ 满足非线性弹性变分问题

$$
\boldsymbol{u}_\omega=\inf_{\boldsymbol{u}}\Pi_\omega(\boldsymbol{u}),\qquad
\Pi_\omega(\boldsymbol{u})=
\int_\omega W_0(\boldsymbol{u},\boldsymbol{x})\,\mathrm d\boldsymbol{x}
-\int_{\widetilde\Gamma_N}\boldsymbol{t}\cdot\boldsymbol{u}\,\mathrm dS,
\tag{2}
$$

其中

$$
\mathcal V_\omega=\left\{\boldsymbol{u}\in H^1(\omega,\mathbb R^2):
\boldsymbol{u}|_{\partial\omega\cap\Gamma_D}=\boldsymbol{0}\right\}
\tag{3}
$$

是容许位移空间，$\Pi_\omega(\boldsymbol{u})$ 为系统总势能，$W_0(\boldsymbol{u},\boldsymbol{x})$ 为构成形状 $\omega$ 的实体材料的应变能密度；$\Gamma_D$ 与 $\Gamma_N$ 构成 $\partial\Omega$ 的一个划分，$\boldsymbol{t}$ 是施加在 $\widetilde\Gamma_N\subseteq\Gamma_N$ 上的非零面力。

![[GiraldoLondono2021_Fig1.png]]

<center><b>
图 1：扩展设计域与边界条件（改编自 Talischi et al. 2012b）
</b></center>

为采用常见离散技术和优化算法联立求解优化问题 (1) 与变分问题 (2)，引入与 $\omega$ 相关的特征函数 $\chi_\omega$，将式 (2) 改写在 $\Omega$ 上会更方便：[^1]

$$
\boldsymbol{u}_\omega=\inf_{\boldsymbol{u}}\Pi(\boldsymbol{u}),\qquad
\Pi(\boldsymbol{u})=
\int_\Omega\chi_\omega W_0(\boldsymbol{u},\boldsymbol{x})\,\mathrm d\boldsymbol{x}
-\int_{\widetilde\Gamma_N}\boldsymbol{t}\cdot\boldsymbol{u}\,\mathrm dS,
\quad \boldsymbol{u}_\omega\in\mathcal V,
\tag{4}
$$

$$
\mathcal V=\left\{\boldsymbol{u}\in H^1(\Omega,\mathbb R^2):
\boldsymbol{u}|_{\Gamma_D}=\boldsymbol{0}\right\}.
\tag{5}
$$

与式 (3) 不同，$\mathcal V$ 不依赖于 $\omega$。由此可在容许空间 $\mathcal A_{\mathcal O}=\{\chi_\omega:\omega\in\mathcal O\}$ 上定义形状 $\omega$。

由于 $\mathcal A_{\mathcal O}$ 不是向量空间，求解式 (1) 将成为计算代价过高的整数规划问题。为此，引入形状的连续参数化 $\rho\in[0,1]$，并将 $\rho$ 解释为取值在 $[0,1]$ 内的密度函数。为恢复优化问题的二值性质，通常使用实体各向同性材料惩罚（solid isotropic material with penalization, SIMP）等惩罚函数（Bendsøe 1989; Zhou and Rozvany 1991; Rozvany et al. 1992）。采用 SIMP 连续参数化后，式 (4) 变为

$$
\begin{aligned}
\boldsymbol{u}&=\inf_{\boldsymbol{u}}\Pi(\rho,\boldsymbol{u}),\\
\Pi(\rho,\boldsymbol{u})&=\int_\Omega[\epsilon+(1-\epsilon)\rho^p]
W_0(\boldsymbol{u},\boldsymbol{x})\,\mathrm d\boldsymbol{x}
-\int_{\widetilde\Gamma_N}\boldsymbol{t}\cdot\boldsymbol{u}\,\mathrm dS,
\quad\boldsymbol{u}\in\mathcal V,
\end{aligned}
\tag{6}
$$

其中 $p>1$ 为惩罚因子。

直接使用连续参数化 $\rho$ 求解式 (1) 仍不能使问题适定。为保证适定性，本文通过正则化映射 $P_F$ 对容许设计空间间接施加正则性，令 $\rho=P_F(\eta)$，其中 $\eta$ 为设计函数。这样，$\rho$ 可继承定义 $P_F$ 的核 $F$ 的光滑性质。具体地，正则化映射由设计函数 $\eta$ 与光滑核 $F$ 的卷积定义（Bourdin 2001; Borrvall and Petersson 2001）：

$$
P_F(\eta)(\boldsymbol{x})=\int_\Omega F(\boldsymbol{x},\bar{\boldsymbol{x}})
\eta(\bar{\boldsymbol{x}})\,\mathrm d\bar{\boldsymbol{x}}.
\tag{7}
$$

本文采用半径为 $R$ 的非线性核

$$
F(\boldsymbol{x},\bar{\boldsymbol{x}})=c(\boldsymbol{x})
\max\left(1-\frac{\|\boldsymbol{x}-\bar{\boldsymbol{x}}\|}{R},0\right)^q,
\tag{8}
$$

归一化系数 $c(\boldsymbol{x})$ 取为使

$$
\int_\Omega F(\boldsymbol{x},\bar{\boldsymbol{x}})\,\mathrm d\bar{\boldsymbol{x}}=1.
\tag{9}
$$

式 (8) 中 $q\geq1$ 为过滤指数；取 $q=1$ 时即得到传统线性帽形核。

Talischi et al.（2012b）指出，可在 $\Omega$ 上定义算子 $P_s(\eta(\boldsymbol{x}))$，按所需行为映射 $\eta(\boldsymbol{x})$，以对容许形状施加其他布局或制造约束，例如挤出、图案重复或梯度约束。本文用 $P_s$ 对容许形状集合施加对称性。例如，关于 $x_1$ 轴对称时

$$
P_s(\eta(\boldsymbol{x}))=\eta(x_1,|x_2|),
\tag{10}
$$

关于 $x_2$ 轴对称时

$$
P_s(\eta(\boldsymbol{x}))=\eta(|x_1|,x_2).
\tag{11}
$$

施加对称性时，需要结合对称映射与过滤，将容许密度场空间定义为

$$
\mathcal A=\left\{P(\eta):\eta\in L^\infty(\Omega;[0,1])\right\},
\qquad P(\eta)=(P_F\circ P_s)(\eta).
\tag{12}
$$

附录 B 将说明，本文修改了 PolyTop 的 `PolyFilter` 程序，使其在计算过滤算子的同时能够施加关于 $x_1$ 轴、$x_2$ 轴或二者的对称性。

综上，以连续参数化密度场 $\rho$ 表示的一般拓扑优化问题为

$$
\begin{aligned}
\inf_{\rho\in\mathcal A}\quad &f(\rho,\boldsymbol{u})\\
\text{s.t.}\quad &g_j(\rho,\boldsymbol{u})\leq0,\quad j=1,\ldots,K,
\end{aligned}
\tag{13}
$$

其中 $\mathcal A$ 由式 (12) 定义，位移场 $\boldsymbol{u}$ 满足

$$
\begin{aligned}
\boldsymbol{u}&=\inf_{\boldsymbol{u}}\Pi(\rho,\boldsymbol{u}),\\
\Pi(\rho,\boldsymbol{u})&=\int_\Omega m_E(\rho)W_0(\boldsymbol{u},\boldsymbol{x})\,\mathrm d\boldsymbol{x}
-\int_{\widetilde\Gamma_N}\boldsymbol{t}\cdot\boldsymbol{u}\,\mathrm dS,
\quad\boldsymbol{u}\in\mathcal V.
\end{aligned}
\tag{14}
$$

$m_E(\rho)$ 是由某点密度计算该点刚度的材料插值函数，例如 SIMP 中 $m_E(\rho)=\epsilon+(1-\epsilon)\rho^p$。类似地，不同物理量可采用不同插值函数。例如对局部体积分数，可定义 $m_V(\rho)=\rho$。[^2] 结构相对于整个设计域的体积分数为

$$
f(\rho)=\frac{1}{|\Omega|}\int_\Omega m_V(\rho)\,\mathrm d\boldsymbol{x}.
\tag{15}
$$

后文的局部应力约束质量最小化问题正是采用该目标函数。

## 2.2 应力约束问题

典型应力约束拓扑优化旨在寻找能够承受给定荷载、且域内任何位置均不发生材料失效的最轻结构。为限制 $\boldsymbol{x}_j\in\Omega$ 处的应力，施加材料失效约束 $g_j(\rho,\boldsymbol{u})\leq0$，$j=1,\ldots,K$。在连续统框架下，该问题写为

$$
\begin{aligned}
\inf_{\rho\in\mathcal A}\quad &f(\rho)=\frac{1}{|\Omega|}\int_\Omega m_V(\rho)\,\mathrm d\boldsymbol{x}\\
\text{s.t.}\quad &g_j(\rho,\boldsymbol{u})\leq0,\quad j=1,\ldots,K,\\
\text{with:}\quad &\boldsymbol{u}=\inf_{\boldsymbol{u}}\Pi(\rho,\boldsymbol{u}),\quad\boldsymbol{u}\in\mathcal V,\\
&\Pi(\rho,\boldsymbol{u})=\int_\Omega m_E(\rho)W_0(\boldsymbol{u},\boldsymbol{x})\,\mathrm d\boldsymbol{x}
-\int_{\widetilde\Gamma_N}\boldsymbol{t}\cdot\boldsymbol{u}\,\mathrm dS.
\end{aligned}
\tag{16}
$$

目标函数 $f(\rho)$ 表示结构的质量比（体积分数），由体积插值函数 $m_V(\rho)$ 定义。为促进黑白设计，本文采用基于阈值投影函数（Wang et al. 2011）的体积插值

$$
m_V(\rho)=\frac{\tanh(\beta\eta)+\tanh[\beta(\rho-\eta)]}
{\tanh(\beta\eta)+\tanh[\beta(1-\eta)]}.
\tag{17}
$$

材料插值函数取为[^3]

$$
m_E(\rho)=
\begin{cases}
\epsilon+(1-\epsilon)[h(\rho)]^p, & \text{SIMP},\\[2mm]
\epsilon+(1-\epsilon)\dfrac{h(\rho)}{1+p_0[1-h(\rho)]}, & \text{RAMP},
\end{cases}
\tag{18}
$$

其中 $h(\rho)=m_V(\rho)$ 为 $\boldsymbol{x}\in\Omega$ 处的体积分数。

## 2.3 多项式消失约束

理论上，为防止任意 $\boldsymbol{x}_j\in\Omega$ 处发生材料失效，应逐点施加应力约束 $g_j(\rho,\boldsymbol{u})$；这来自经典连续介质力学中应力的局部定义。实际计算中需选取有限个评价点，使约束数 $K$ 有限。例如离散后可在每个有限元形心评价应力，于是 $K=N$，其中 $N$ 是有限元个数。本文采用的约束称为多项式消失约束（Giraldo-Londoño and Paulino 2020），它是传统消失约束[^4]（Cheng and Jiang 1992）的变体：

$$
g_j(\rho,\boldsymbol{u})=m_E(\rho)\Lambda_j(\Lambda_j^2+1),
\qquad \Lambda_j=\frac{\sigma_j^v}{\sigma_{\mathrm{lim}}}-1,
\tag{19}
$$

其中 $\sigma_j^v$ 为评价点 $\boldsymbol{x}_j$ 处的 von Mises 应力，$\sigma_{\mathrm{lim}}$ 为材料应力限值。$\sigma_j^v$ 所依赖的 Cauchy 应力张量由实体材料应变能密度计算：

$$
\boldsymbol{\sigma}=\frac{\partial W_0}{\partial\boldsymbol{\varepsilon}},
\tag{20}
$$

其中 $W_0$ 为储能密度函数，$\boldsymbol{\varepsilon}$ 为无穷小应变张量。

Giraldo-Londoño and Paulino（2020）指出，多项式消失约束有两项优点。第一，当 $\sigma_j^v/\sigma_{\mathrm{lim}}\gg1$，即约束严重违反时，$g_j$ 按 $(\sigma_j^v/\sigma_{\mathrm{lim}}-1)^3$ 缩放，从而推动优化器得到整体应力更低的解。第二，当 $\sigma_j^v/\sigma_{\mathrm{lim}}\to1$，即约束接近满足时，$g_j$ 按 $(\sigma_j^v/\sigma_{\mathrm{lim}}-1)$ 缩放，从而保持传统消失约束的性质。图 2 比较了两类约束随 $\Lambda_j$ 的变化；多项式消失约束对违反约束的惩罚更严厉，但在 $\Lambda_j\approx0$ 时与传统约束表现相近。

![[GiraldoLondono2021_Fig2.png]]

<center><b>
图 2：传统消失约束（Cheng and Jiang 1992）与多项式消失约束（Giraldo-Londoño and Paulino 2020）随 $\Lambda_j$ 的变化；$\Lambda_j>0$ 表示应力约束被违反
</b></center>

多项式消失约束与传统消失约束的主要区别是式 (19) 中的 $\Lambda_j^3$ 项。尽管该三次项提高了应力约束的非线性，本文所有算例均未出现由此导致的不利影响。相反，非线性惩罚能比传统约束采用的线性惩罚更快地将解推向整体应力较低的状态。本文未进一步研究其他形式，但也可以用别的非线性惩罚函数替代这里的三次函数。[^5]

# 3 离散化

为数值求解式 (16)，需要离散设计域，从而离散设计空间 $\mathcal A$ 与位移空间 $\mathcal V$。以下分别说明这两个场的离散方式，最后明确写出 PolyStress 所实现的离散局部应力约束拓扑优化问题。

## 3.1 离散设计空间与过滤算子

用固定剖分 $\mathcal T_h=\{\Omega_\ell\}_{\ell=1}^N$ 离散 $\Omega$，其特征网格尺寸为 $h$，满足 $\Omega_k\cap\Omega_\ell=\varnothing$（$k\neq\ell$）且 $\bigcup_{\ell=1}^N\overline\Omega_\ell=\overline\Omega$。据此定义设计空间的分片常数离散：

$$
\mathcal A_h=\left\{P(\eta_h):0\leq\eta_h\leq1,
\ \eta_h|_{\Omega_\ell}=\mathrm{const.}\ \forall\ell\right\}.
\tag{21}
$$

离散设计函数为

$$
\eta_h=\sum_{\ell=1}^N z_\ell\chi_{\Omega_\ell}(\boldsymbol{x}),
\tag{22}
$$

其中 $\chi_{\Omega_\ell}$ 为单元 $\Omega_\ell$ 的特征函数，$\boldsymbol{z}=\{z_\ell\}_{\ell=1}^N$ 为设计变量向量。

实现中，以同样在每个单元上为常数的场 $\widetilde\rho_h$ 替代 $\rho_h$：

$$
\widetilde\rho_h(\boldsymbol{x})=\sum_{\ell=1}^N y_\ell\chi_{\Omega_\ell}(\boldsymbol{x}),
\tag{23}
$$

其中 $y_\ell=\rho_h(\boldsymbol{x}_\ell^*)$，$\boldsymbol{x}_\ell^*$ 为单元 $\ell$ 的形心。Talischi et al.（2012b）指出，这一定义给出映射 $P$ 的离散化，并将单元值向量 $\boldsymbol{y}$ 与设计变量 $\boldsymbol{z}$ 关联为

$$
\boldsymbol{y}=\boldsymbol{P}\boldsymbol{z},
\tag{24}
$$

其中 $\boldsymbol{P}$ 是连续映射 $P$ 的离散对应物，即过滤矩阵。不施加对称性时

$$
P_{\ell k}=\int_{\Omega_k}F(\boldsymbol{x}_\ell^*,\bar{\boldsymbol{x}})
\,\mathrm d\bar{\boldsymbol{x}}.
\tag{25}
$$

采用式 (8) 的非线性核后

$$
P_{\ell k}=\frac{w_{\ell k}v_k}{\sum_{j=1}^Nw_{\ell j}v_j},
\tag{26}
$$

$$
w_{\ell k}=\max\left(0,1-\frac{\|\boldsymbol{x}_\ell-\boldsymbol{x}_k\|_2}{R}\right)^q,
\tag{27}
$$

其中 $R$ 为过滤半径，$\|\boldsymbol{x}_\ell-\boldsymbol{x}_k\|_2$ 为单元 $\ell$ 与 $k$ 的形心距离，$q$ 为过滤指数，$v_k$ 为单元 $k$ 的面积。

## 3.2 离散位移场与状态方程的求解

为求解式 (14)，在同一剖分 $\mathcal T_h$ 上离散位移场。离散变分问题是在 $\mathcal V_h=\operatorname{span}\{\boldsymbol{N}_i\}_{i=1}^M$ 中寻找 $\boldsymbol{u}_h$，使

$$
\begin{aligned}
\boldsymbol{u}_h&=\inf_{\boldsymbol{u}}\Pi(\rho,\boldsymbol{u}),\\
\Pi(\rho,\boldsymbol{u})&=\int_\Omega m_E(\rho_h)W_0(\boldsymbol{u},\boldsymbol{x})\,\mathrm d\boldsymbol{x}
-\int_{\widetilde\Gamma_N}\boldsymbol{t}\cdot\boldsymbol{u}\,\mathrm dS,
\end{aligned}
\tag{28}
$$

其中 $\{\boldsymbol{N}_i\}_{i=1}^M$ 构成 $\mathcal V_h$ 的基，$M$ 为位移自由度数。采用标准有限元过程，以形函数近似

$$
\boldsymbol{u}_h=\sum_{i=1}^M U_i\boldsymbol{N}_i(\boldsymbol{x}).
\tag{29}
$$

于是式 (28) 变为

$$
\begin{aligned}
\boldsymbol{U}&=\arg\min_{\boldsymbol{U}}\Pi(\boldsymbol{z},\boldsymbol{U}),\\
\Pi(\boldsymbol{z},\boldsymbol{U})&=\sum_{\ell=1}^N\int_{\Omega_\ell}
m_E(y_\ell)W_0(\boldsymbol{u}_\ell,\boldsymbol{x})\,\mathrm d\boldsymbol{x}
-\boldsymbol{F}_{\mathrm{ext}}\cdot\boldsymbol{U},
\end{aligned}
\tag{30}
$$

其中 $\boldsymbol{U}=\{U_i\}_{i=1}^M$ 为节点位移向量，设计无关的外部节点力为

$$
(\boldsymbol{F}_{\mathrm{ext}})_i=
\int_{\widetilde\Gamma_N}\boldsymbol{t}\cdot\boldsymbol{N}_i\,\mathrm dS,
\tag{31}
$$

$\boldsymbol{u}_\ell$ 为单元 $\Omega_\ell$ 的节点位移向量。式 (30) 的离散平衡条件为

$$
\boldsymbol{R}=\frac{\partial\Pi}{\partial\boldsymbol{U}}
=\boldsymbol{F}_{\mathrm{int}}-\boldsymbol{F}_{\mathrm{ext}}=\boldsymbol{0},
\tag{32}
$$

其中内力

$$
(\boldsymbol{F}_{\mathrm{int}})_i=
\int_\Omega m_E(\rho_h)\boldsymbol{\sigma}\cdot\nabla\boldsymbol{N}_i\,\mathrm d\boldsymbol{x}
\tag{33}
$$

$$
=\sum_{\ell=1}^N\int_{\Omega_\ell}m_E(y_\ell)
\boldsymbol{\sigma}\cdot\nabla\boldsymbol{N}_i\,\mathrm d\boldsymbol{x}.
\tag{34}
$$

式 (32) 的非线性方程组用 Newton-Raphson 格式迭代求解，其一致切线矩阵为

$$
(\boldsymbol{K}_T)_{ij}=
\int_\Omega m_E(\rho_h)\boldsymbol{C}_T\nabla\boldsymbol{N}_i:\nabla\boldsymbol{N}_j\,\mathrm d\boldsymbol{x}
\tag{35}
$$

$$
=\sum_{\ell=1}^N\int_{\Omega_\ell}m_E(y_\ell)
\boldsymbol{C}_T\nabla\boldsymbol{N}_i:\nabla\boldsymbol{N}_j\,\mathrm d\boldsymbol{x},
\tag{36}
$$

其中 $\boldsymbol{C}_T$ 为材料切线模量矩阵。

## 3.3 离散拓扑优化问题

将 $\Omega$ 上的设计空间与位移场离散后，最终局部应力约束拓扑优化问题为

$$
\begin{aligned}
\min_{\boldsymbol{z}\in[0,1]^N}\quad &f(\boldsymbol{z})=
\frac{\boldsymbol{A}^{\mathsf T}m_V(\boldsymbol{y})}{\boldsymbol{A}^{\mathsf T}\boldsymbol{1}}\\
\text{s.t.}\quad &g_j(\boldsymbol{z},\boldsymbol{U})=
m_E(y_j)\Lambda_j(\Lambda_j^2+1)\leq0,\quad j=1,\ldots,N,\\
\text{with:}\quad &\Lambda_j=\frac{\sigma_j^v}{\sigma_{\mathrm{lim}}}-1,\\
&\boldsymbol{U}=\arg\min_{\boldsymbol{U}}\Pi(\boldsymbol{z},\boldsymbol{U}),\\
&\Pi(\boldsymbol{z},\boldsymbol{U})=
\sum_{\ell=1}^N\int_{\Omega_\ell}m_E(y_\ell)W_0(\boldsymbol{u}_\ell,\boldsymbol{x})
\,\mathrm d\boldsymbol{x}-\boldsymbol{F}_{\mathrm{ext}}\cdot\boldsymbol{U}.
\end{aligned}
\tag{37}
$$

其中 $\boldsymbol{A}=\{|\Omega_\ell|\}_{\ell=1}^N$ 为单元面积向量，$\sigma_j^v$ 是单元 $\Omega_j$ 形心 $\boldsymbol{x}_j^*$ 处的 von Mises 应力。$m_V(\cdot)$ 与 $m_E(\cdot)$ 分别按式 (17) 和 (18) 计算，状态变量 $\boldsymbol{U}$ 由前述有限元法求得。上述问题对每个单元施加一个应力约束，适用于单一荷载工况。[^6]

# 4 增广拉格朗日框架

应力约束拓扑优化的主要困难之一，是必须施加大量应力约束，才能防止所有评价点发生材料失效。在式 (37) 中，应力约束数 $N$ 与有限元单元数相同。为降低处理众多约束的计算代价，最常见做法是将局部应力约束聚合成一个全局约束或若干分组约束（例如 Yang and Chen 1996; Luo et al. 2013; De Leon et al. 2015; Kiyono et al. 2016; Lee et al. 2016; Lian et al. 2017; Liu et al. 2018; Xia et al. 2018; Fan et al. 2019; Lee et al. 2010, 2012; Holmberg et al. 2013b）。采用这些聚类技术时，最终设计往往依赖分组数、每组中的单元或应力评价点数量，以及估计组内最大应力所用的范数函数，例如 $p$-norm（Park 1995）或 KS 函数（Kreisselmeier and Steinhauser 1979）。不仅设计依赖这些选择，而且某些范数函数不能保证处处满足应力限值。基于这些观察，可以认为聚类或聚合方法不适合处理现实设计问题。

与上述方法相比，AL 方法（Bertsekas 1999; Nocedal and Wright 2006）能够在局部满足应力约束，是求解式 (37) 的一种有吸引力的方案。已有多项研究用 AL 方法求解应力约束拓扑优化（Pereira et al. 2004; Fancello 2006; Emmendoerfer and Fancello 2014, 2016; Emmendoerfer et al. 2019; da Silva et al. 2018）。AL 方法将原约束问题转化为一系列以原问题增广拉格朗日函数 $L_\mu(\boldsymbol{z},\boldsymbol{\lambda})$ 为目标的无约束问题。第 $k$ 个 AL 步求解[^7]

$$
\min_{\boldsymbol{z}\in[0,1]^N}L_{\mu^{(k)}}(\boldsymbol{z},\boldsymbol{\lambda}^{(k)})
=f(\boldsymbol{z})+P^{(k)}(\boldsymbol{z},\boldsymbol{U}),
\tag{38}
$$

其中惩罚项为

$$
P^{(k)}(\boldsymbol{z},\boldsymbol{U})=
\sum_{j=1}^N\left[\lambda_j^{(k)}h_j(\boldsymbol{z},\boldsymbol{U})
+\frac{\mu^{(k)}}{2}h_j(\boldsymbol{z},\boldsymbol{U})^2\right],
\tag{39}
$$

$$
h_j(\boldsymbol{z},\boldsymbol{U})=
\max\left[g_j(\boldsymbol{z},\boldsymbol{U}),-
\frac{\lambda_j^{(k)}}{\mu^{(k)}}\right].
\tag{40}
$$

$\boldsymbol{\lambda}^{(k)}=\{\lambda_j^{(k)}\}_{j=1}^N$ 为 Lagrange 乘子估计向量，$\mu^{(k)}>0$ 为二次惩罚因子。通常按

$$
\mu^{(k+1)}=\min[\alpha\mu^{(k)},\mu_{\max}]
\tag{41}
$$

更新惩罚因子，其中 $\alpha>1$，$\mu_{\max}$ 用于避免数值不稳定；Lagrange 乘子估计按

$$
\lambda_j^{(k+1)}=\lambda_j^{(k)}+
\mu^{(k)}h_j(\boldsymbol{z}^{(k)},\boldsymbol{U})
\tag{42}
$$

更新。

未经归一化时，上述 AL 方法不适合大规模应力约束拓扑优化，因为 $N$ 增大后惩罚项 $P^{(k)}$ 会压倒目标项 $f$，从而损害收敛性。Senhora et al.（2020）为此对惩罚项作归一化：

$$
\min_{\boldsymbol{z}\in[0,1]^N}J^{(k)}(\boldsymbol{z},\boldsymbol{U})
=f(\boldsymbol{z})+\frac{1}{N}P^{(k)}(\boldsymbol{z},\boldsymbol{U}).
\tag{43}
$$

与式 (38) 相比，式 (43) 仅多了按约束数 $N$ 对惩罚项归一化。这使大约束数问题能够避免数值不稳定，因此本文采用该式。da Silva et al.（2019a）通过将目标函数乘以有限元单元数提出了类似归一化策略；da Silva et al.（2019b）则按单元数归一化初始与最大惩罚参数 $\mu^{(0)}$ 和 $\mu_{\max}$，以提高 AL 方法稳健性。这些研究均说明归一化项的重要性。

![[GiraldoLondono2021_Fig3.png]]

<center><b>
图 3：本文用于局部应力约束拓扑优化的 AL 框架流程图
</b></center>

图 3 所示流程首先读取有限元问题与优化器输入，然后在 $k=0$ 时初始化 $\lambda_j^{(k)}$ 和 $\mu^{(k)}$；随后用移动渐近线法（method of moving asymptotes, MMA；Svanberg 1987）近似最小化式 (43)；根据所得解更新 $\lambda_j^{(k)}$ 和 $\mu^{(k)}$，直至收敛。具体地，当 $N^{-1}\sum_{e=1}^N|z_{i+1,e}^{(k)}-z_{i,e}^{(k)}|<\mathrm{Tol}$ 且 $\max_j(\sigma_j^v/\sigma_{\mathrm{lim}})-1<\mathrm{TolS}$ 时认为收敛，其中 `Tol` 与 `TolS` 分别为设计变量变化和应力约束容差，$i$ 是同一 AL 子问题 $k$ 中的 MMA 迭代号，$e$ 是设计变量分量下标。

$\mu^{(0)}$、$\mu_{\max}$、$\alpha$ 和 $\boldsymbol{\lambda}^{(0)}$ 均影响 AL 方法性能，其中初始乘子影响最小，可取 $\boldsymbol{\lambda}^{(0)}=\boldsymbol{0}$。惩罚因子的更新参数需先标定：$\mu^{(0)}$ 不能过小，否则收敛很慢；$\mu_{\max}$ 不能过大，否则可能病态；建议取较小的 $\alpha$（如 $1<\alpha<2$），使 $\mu^{(k)}$ 在连续 AL 子问题之间适度增长。根据作者经验，针对某一问题（如传统 L 形支架）确定的参数通常也适用于多种其他问题。

# 5 灵敏度分析

本文采用梯度优化算法求解式 (37)，因此需要式 (43) 中归一化 AL 函数的灵敏度。由链式法则

$$
\frac{\mathrm dJ^{(k)}}{\mathrm dz_e}=
\sum_{\ell=1}^N\left(
\frac{\partial E_\ell}{\partial z_e}\frac{\mathrm dJ^{(k)}}{\mathrm dE_\ell}
+\frac{\partial V_\ell}{\partial z_e}\frac{\mathrm dJ^{(k)}}{\mathrm dV_\ell}
\right),
\tag{44}
$$

向量形式为

$$
\frac{\mathrm dJ^{(k)}}{\mathrm d\boldsymbol{z}}=
\frac{\partial\boldsymbol{E}}{\partial\boldsymbol{z}}
\frac{\mathrm dJ^{(k)}}{\mathrm d\boldsymbol{E}}+
\frac{\partial\boldsymbol{V}}{\partial\boldsymbol{z}}
\frac{\mathrm dJ^{(k)}}{\mathrm d\boldsymbol{V}},
\tag{45}
$$

其中 $\boldsymbol{E}=m_E(\boldsymbol{y})$ 与 $\boldsymbol{V}=m_V(\boldsymbol{y})$ 分别包含与设计有关的刚度和体积分数信息。将归一化 AL 函数分为目标项与惩罚项，可写为

$$
\frac{\mathrm dJ^{(k)}}{\mathrm d\boldsymbol{z}}=
\frac{\partial\boldsymbol{E}}{\partial\boldsymbol{z}}
\left(\frac{\partial f}{\partial\boldsymbol{E}}+
\frac1N\frac{\partial P^{(k)}}{\partial\boldsymbol{E}}\right)
+\frac{\partial\boldsymbol{V}}{\partial\boldsymbol{z}}
\left(\frac{\partial f}{\partial\boldsymbol{V}}+
\frac1N\frac{\partial P^{(k)}}{\partial\boldsymbol{V}}\right).
\tag{46}
$$

由于 $\boldsymbol{E}=m_E(\boldsymbol{Pz})$、$\boldsymbol{V}=m_V(\boldsymbol{Pz})$，有

$$
\frac{\partial\boldsymbol{E}}{\partial\boldsymbol{z}}=
\boldsymbol{P}^{\mathsf T}\boldsymbol{J}_{m_E}(\boldsymbol{Pz}),
\qquad
\frac{\partial\boldsymbol{V}}{\partial\boldsymbol{z}}=
\boldsymbol{P}^{\mathsf T}\boldsymbol{J}_{m_V}(\boldsymbol{Pz}),
\tag{47}
$$

其中 $\boldsymbol{J}_{m_E}=\operatorname{diag}(m_E'(y_1),\ldots,m_E'(y_N))$，$\boldsymbol{J}_{m_V}=\operatorname{diag}(m_V'(y_1),\ldots,m_V'(y_N))$（Talischi et al. 2012b）。由式 (37)，目标项灵敏度为

$$
\frac{\partial f}{\partial E_\ell}=0,
\qquad
\frac{\partial f}{\partial V_\ell}=\frac{A_\ell}{\boldsymbol{A}^{\mathsf T}\boldsymbol{1}}.
\tag{48}
$$

$P^{(k)}$ 不直接依赖 $V_\ell$，因此

$$
\frac{\partial P^{(k)}}{\partial V_\ell}=0.
\tag{49}
$$

但 $P^{(k)}$ 通过应力约束直接依赖单元刚度参数 $E_\ell$，故

$$
\frac{\partial P^{(k)}}{\partial E_\ell}=
\sum_{j=1}^N[\lambda_j^{(k)}+\mu^{(k)}h_j]
\left[\frac{\partial h_j}{\partial E_\ell}+
\frac{\partial h_j}{\partial\boldsymbol{U}}\cdot
\frac{\partial\boldsymbol{U}}{\partial E_\ell}\right].
\tag{50}
$$

为避免高代价地计算 $\partial\boldsymbol{U}/\partial E_\ell$，采用伴随法。由平衡条件 (32)，平衡点残差的灵敏度满足

$$
\frac{\partial\boldsymbol{R}}{\partial E_\ell}=
\frac{\partial\boldsymbol{F}_{\mathrm{int}}}{\partial\boldsymbol{U}}
\frac{\partial\boldsymbol{U}}{\partial E_\ell}+
\frac{\partial\boldsymbol{F}_{\mathrm{int}}}{\partial E_\ell}-
\frac{\partial\boldsymbol{F}_{\mathrm{ext}}}{\partial E_\ell}
=\boldsymbol{K}_T\frac{\partial\boldsymbol{U}}{\partial E_\ell}+
\frac{\partial\boldsymbol{F}_{\mathrm{int}}}{\partial E_\ell}=\boldsymbol{0},
\tag{51}
$$

其中假定外力与设计变量无关。在式 (50) 中加入 $\boldsymbol{\xi}^{\mathsf T}\partial\boldsymbol{R}/\partial E_\ell$：

$$
\begin{aligned}
\frac{\partial P^{(k)}}{\partial E_\ell}={}&
\sum_{j=1}^N[\lambda_j^{(k)}+\mu^{(k)}h_j]
\left[\frac{\partial h_j}{\partial E_\ell}+
\frac{\partial h_j}{\partial\boldsymbol{U}}\cdot
\frac{\partial\boldsymbol{U}}{\partial E_\ell}\right]\\
&+\boldsymbol{\xi}^{\mathsf T}\left(
\boldsymbol{K}_T\frac{\partial\boldsymbol{U}}{\partial E_\ell}+
\frac{\partial\boldsymbol{F}_{\mathrm{int}}}{\partial E_\ell}\right).
\end{aligned}
\tag{52}
$$

选取伴随向量 $\boldsymbol{\xi}$ 消去所有含 $\partial\boldsymbol{U}/\partial E_\ell$ 的项，得到

$$
\frac{\partial P^{(k)}}{\partial E_\ell}=
\sum_{j=1}^N[\lambda_j^{(k)}+\mu^{(k)}h_j]
\frac{\partial h_j}{\partial E_\ell}+
\boldsymbol{\xi}^{\mathsf T}
\frac{\partial\boldsymbol{F}_{\mathrm{int}}}{\partial E_\ell},
\tag{53}
$$

其中 $\boldsymbol{\xi}$ 满足

$$
\boldsymbol{K}_T\boldsymbol{\xi}=-
\sum_{j=1}^N[\lambda_j^{(k)}+\mu^{(k)}h_j]
\frac{\partial h_j}{\partial\boldsymbol{U}}.
\tag{54}
$$

由式 (40)，当 $g_j(\boldsymbol{z})<-\lambda_j^{(k)}/\mu^{(k)}$ 时 $\partial h_j/\partial\boldsymbol{U}=0$；否则

$$
\frac{\partial h_j}{\partial\boldsymbol{U}}=
\frac{\partial g_j}{\partial\boldsymbol{U}}=
\frac{\partial g_j}{\partial\sigma_j^v}
\frac{\partial\sigma_j^v}{\partial\boldsymbol{\sigma}}
\frac{\partial\boldsymbol{\sigma}}{\partial\boldsymbol{U}}.
\tag{55}
$$

$\partial g_j/\partial\sigma_j^v$ 可由式 (37) 直接得到。von Mises 应力为

$$
\sigma_j^v=\sqrt{\boldsymbol{\sigma}^{\mathsf T}\boldsymbol{V}_0\boldsymbol{\sigma}},
\qquad
\boldsymbol{V}_0=
\begin{bmatrix}
1&-1/2&0\\
-1/2&1&0\\
0&0&3
\end{bmatrix},
\tag{56}
$$

其中 $\boldsymbol{\sigma}=[\sigma_{11}\ \sigma_{22}\ \sigma_{12}]^{\mathsf T}$ 是由 $\boldsymbol{\sigma}=\partial W_0/\partial\boldsymbol{\varepsilon}$ 得到的 Voigt 记号 Cauchy 应力向量。因此

$$
\frac{\partial\sigma_j^v}{\partial\boldsymbol{\sigma}}=
\frac{\boldsymbol{V}_0\boldsymbol{\sigma}}{\sigma_j^v}.
\tag{57}
$$

最后

$$
\frac{\partial\boldsymbol{\sigma}}{\partial\boldsymbol{U}}=
\frac{\partial\boldsymbol{\sigma}}{\partial\boldsymbol{\varepsilon}}
\frac{\partial\boldsymbol{\varepsilon}}{\partial\boldsymbol{U}}=
\boldsymbol{D}\boldsymbol{B},
\tag{58}
$$

其中 $\boldsymbol{\varepsilon}$ 为 Voigt 记号无穷小应变向量，$\boldsymbol{D}$ 为材料切线矩阵，$\boldsymbol{B}$ 为应变—位移矩阵。

[^1]: 特征函数定义为：$\boldsymbol{x}\in\omega$ 时 $\chi_\omega=1$，否则 $\chi_\omega=0$。实际计算采用 Ersatz 材料模型保证边值问题解的存在唯一性；即在 $\chi_\omega=0$ 的区域使用 $\epsilon+(1-\epsilon)\chi_\omega$，其中 $\epsilon\ll1$ 为 Ersatz 参数。
[^2]: 后文采用基于阈值投影函数的体积插值函数，以获得清晰的黑白设计。
[^3]: Talischi et al.（2012b）在采用 Guest et al.（2004）的光滑 Heaviside 函数时使用了类似方法。
[^4]: 在基于密度的拓扑优化中，传统消失约束可写为 $g_j(\rho,\boldsymbol{u})=\rho\Lambda_j$，其中 $\Lambda_j=\sigma_j^v/\sigma_{\mathrm{lim}}-1$。
[^5]: 若要探索其他非线性项，例如在式 (19) 中以 $\Lambda_j^4$ 替代 $\Lambda_j^3$，需修改 `PolyStress.m` 内的 `PenalFnc`；后文会给出类似修改示例。
[^6]: 多荷载工况下约束数为 $N_c=mN$，其中 $m$ 为荷载工况数。当前 PolyStress 仅实现单一荷载工况；Senhora et al.（2020）给出了多荷载工况实现细节。
[^7]: 文中称式 (38) 为无约束 AL 子问题，但它实际仍含箱式约束。

# 6 PolyStress 的 Matlab 实现

本文沿用 PolyTop 的总体结构实现式 (37)，并对有限元分析程序作相应修改以求解式 (30)，对优化程序作相应修改以实现 AL 方法。作为优化程序修改的一部分，本文实现了一个适于求解无约束最小化问题的 MMA 版本。以下说明这些修改。

## 6.1 输入数据与 PolyScript

与 PolyTop 相同，PolyStress 用名为 `PolyScript` 的 Matlab 脚本集中定义全部运行参数。所有输入参数装入两个结构体数组 `fem` 和 `opt`。`fem` 保存有限元分析所需信息，如网格、荷载、支承和材料属性；`opt` 保存拓扑优化信息，如过滤矩阵、材料插值函数和优化器参数。表 1 列出 `fem` 字段，表 2 列出 `opt` 字段。

<center><b>
表 1：`fem` 结构体字段
</b></center>

| 字段 | 含义 |
|---|---|
| `fem.NNode` | 节点数 |
| `fem.NElem` | 单元数 |
| `fem.Node` | $[\mathrm{NNode}\times2]$ 节点数组 |
| `fem.Element` | $[\mathrm{NElem}\times\mathrm{Var}]$ 单元 cell 数组 |
| `fem.Supp` | $[\mathrm{NSupp}\times3]$ 支承数组 |
| `fem.Load` | $[\mathrm{NLoad}\times3]$ 荷载数组 |
| `fem.Passive` | 被动单元数组 |
| `fem.Thickness` | 单元厚度 |
| `fem.MatModel` | 材料模型名称字符串 |
| `fem.MatParam` | $[1\times\mathrm{Var}]$ 材料模型参数数组 |
| `fem.SLim` | 材料屈服应力 |
| `fem.TolR` | 力残差范数容差 |
| `fem.MaxIter` | Newton-Raphson 最大迭代次数 |
| `fem.MEX` | 是否使用 MEX 函数（`'Yes'` 或 `'No'`） |
| `fem.ElemArea`$^\dagger$ | 单元面积数组 |
| `fem.W`$^\dagger$ | Gauss 点权重 |
| `fem.dNdxi`$^\dagger$ | Gauss 点处形函数导数 |
| `fem.ElemNDof`$^\dagger$ | 单元自由度数数组 |
| `fem.k0`$^\dagger$ | 局部刚度矩阵条目数组 |
| `fem.i`$^\dagger$ | `fem.k0` 稀疏组装索引数组 |
| `fem.j`$^\dagger$ | `fem.k0` 稀疏组装索引数组 |
| `fem.e`$^\dagger$ | 与 `fem.k0` 对应的单元编号数组 |
| `fem.eDof`$^\dagger$ | 全局荷载向量稀疏组装索引数组 |
| `fem.DofE`$^\dagger$ | 与全局荷载向量对应的单元编号数组 |
| `fem.iK0`$^\dagger$ | 单元刚度矩阵稀疏组装索引数组 |
| `fem.jK0`$^\dagger$ | 单元刚度矩阵稀疏组装索引数组 |
| `fem.Fext`$^\dagger$ | 全局外力向量 |
| `fem.FreeDofs`$^\dagger$ | 自由自由度数组 |
| `fem.B0`$^\dagger$ | 单元形心处应变—位移矩阵 |
| `fem.rowD`$^\dagger$ | 单元切线矩阵稀疏组装行索引 |
| `fem.colD`$^\dagger$ | 单元切线矩阵稀疏组装列索引 |
| `fem.U`$^\dagger$ | 每次优化迭代的收敛位移向量 |
| `fem.L`$^\dagger$ | 刚度矩阵 Cholesky 分解得到的下三角矩阵 |
| `fem.s`$^\dagger$ | Cholesky 分解的置换向量 |
| `fem.fNL`$^\dagger$ | 假定全部单元为实体时的力向量 |
| `fem.VMStress0`$^\dagger$ | 单元形心处 von Mises 应力数组 |

$^\dagger$ 标出的字段若为空，将在 `PolyStress` 内部赋值。

与 PolyTop 相比，新增或变化的 `fem` 字段主要服务于非线性有限元分析，如 `fem.MatModel`、`fem.MatParam`、`fem.TolR` 和 `fem.MaxIter`；另一些字段用于评价 von Mises 应力，如 `fem.SLim`、`fem.B0`、`fem.rowD`、`fem.colD`、`fem.eDof` 和 `fem.VMStress0`。`opt` 方面的变化主要涉及 MMA 优化器字段 `opt.Move`、`opt.Osc`、`opt.AsymInit`、`opt.AsymInc`、`opt.AsymDecr`，以及阈值投影函数式 (17) 中惩罚参数 $\beta$ 的延拓字段 `opt.contB`。`opt.contB=[BFreq,B0,Binc,Bmax]` 分别给出 $\beta$ 的更新频率、初值、增量和最大值。程序按

```matlab
if mod(Iter,BFreq)==0; B = min(B+Binc,Bmax); end
```

更新 $\beta$。

<center><b>
表 2：`opt` 结构体字段
</b></center>

| 字段 | 含义 |
|---|---|
| `opt.zMin` | 设计变量下界 |
| `opt.zMax` | 设计变量上界 |
| `opt.zIni` | 设计变量初始数组 |
| `opt.MatIntFnc` | 材料插值函数句柄 |
| `opt.contB` | 阈值投影延拓参数 |
| `opt.P` | 将设计变量映射为单元变量的矩阵 |
| `opt.Tol` | 设计变量收敛容差 |
| `opt.TolS` | 应力约束收敛容差 |
| `opt.MaxIter` | AL 最大步数 |
| `opt.MMA_Iter` | 每个 AL 步的 MMA 迭代数 |
| `opt.lambda0` | Lagrange 乘子估计初值 |
| `opt.mu0` | AL 惩罚因子初值 |
| `opt.mu_max` | AL 惩罚因子最大值 |
| `opt.alpha` | 惩罚因子更新参数 |
| `opt.Move` | MMA 更新中的容许移动步长 |
| `opt.Osc` | MMA 更新中的振荡参数 |
| `opt.AsymInit` | MMA 更新中的渐近线初始参数 |
| `opt.AsymInc` | MMA 更新中的渐近线增大参数 |
| `opt.AsymDecr` | MMA 更新中的渐近线减小参数 |

与 PolyTop 类似，`PolyScript` 调用 `PolyMesher`（Talischi et al. 2012a）获得有限元网格、边界条件与外荷载，并调用 `PolyFilter` 计算过滤矩阵 $\boldsymbol{P}$。本文修改了 PolyTop 的 `PolyFilter`：实现式 (26)–(27) 的非线性过滤器，并增加关于 $x_1$ 轴、$x_2$ 轴或二者施加密度场对称性的功能。[^8]

在填写 `opt` 前，`PolyScript` 调用辅助函数 `MatIntFnc`。给定输入向量 $\boldsymbol{y}$ 和参数集合 `params`，该函数输出刚度向量 $\boldsymbol{E}=m_E(\boldsymbol{y})$、体积分数向量 $\boldsymbol{V}=m_V(\boldsymbol{y})$ 及对应灵敏度向量 $\partial\boldsymbol{E}/\partial\boldsymbol{y}$ 与 $\partial\boldsymbol{V}/\partial\boldsymbol{y}$；与 PolyTop 一样，这两个灵敏度向量表示相应 Jacobian 矩阵的对角项。由于 PolyTop 不含式 (17) 的阈值投影函数，本文相应修改了 `MatIntFnc`。[^9]

## 6.2 PolyStress 中增广拉格朗日函数的计算

本文用 AL 方法求解式 (37)，每个 AL 步都需求解子问题 (43)。归一化 AL 函数分为目标项 `ObjectiveFnc` 与惩罚项 `PenalFnc`。目标项采用 PolyTop 中 `ConstraintFnc` 的轻微修改版本，差别仅在于 PolyStress 不需要体积分数上限。惩罚项采用独立实现，并调用两个辅助函数：非线性有限元程序 `NLFEM` 和 von Mises 应力计算程序 `von_Mises_Stress`。前者求位移向量 $\boldsymbol{U}$，后者计算所有单元形心处的 von Mises 应力及其对位移向量的灵敏度。用于计算归一化 AL 函数及其灵敏度的函数称为 `AL_Function`，随 PolyStress 代码提供，见附录 E。

## 6.3 非线性有限元分析程序

本文采用基于 Newton-Raphson 方法并带弱线搜索算法[^10]的非线性有限元程序求解式 (30)。其主要部分为

```matlab
U = fem.U; % Use previously converged U as initial guess
[K,~,Res,~,fem] = GlobalK(fem,U,E); % Initial stiffness mtrx. & Res vector
nRes0 = norm(fem.Fext); nRes = nRes0; % Initial norm of force residual
% NEWTON-RAPHSON ITERATIONS
Iter = 0; % Initialize Newton-Raphson iteration counter
while (nRes>fem.TolR*nRes0 && Iter<=fem.MaxIter)
    [Delta_U,L,s] = SolveLinSys(K,Res);
    [K,~,Res,nRes,fem,U] = LineSearch(U,Delta_U,nRes,-K*Res./nRes,fem,E);
    Iter = Iter+1;
end
fem.L = L; fem.s = s; % Store Cholesky decomposition information
fem.U = U; % Store converged displacement vector
```

增量位移 `Delta_U` 由 `SolveLinSys` 求得，该程序采用切线刚度矩阵 $\boldsymbol{K}_T$ 的 Cholesky 分解；随后通过弱线搜索更新 $\boldsymbol{U}$。收敛后，程序保存位移向量 $\boldsymbol{U}$，并保存刚度矩阵分解得到的下三角矩阵 $\boldsymbol{L}$ 与置换向量 $\boldsymbol{s}$，以便高效计算伴随向量。只有材料模型非线性时才调用非线性有限元程序；线性材料则直接求解 $\boldsymbol{K}_T\boldsymbol{U}=\boldsymbol{F}_{\mathrm{ext}}$，其中刚度矩阵由预处理阶段保存的实体单元刚度矩阵计算。

有限元分析通常是拓扑优化的瓶颈，非线性材料尤其如此。为提高非线性分析效率，计算全局刚度矩阵的程序被转换为 MEX 函数。用户首次用 PolyStress 优化非线性结构时，`GlobalK` 会自动编译 MEX 文件，但仅在用户选择使用时编译：`fem.MEX='Yes'` 时生成 MEX 函数，`fem.MEX='No'` 时采用传统 Matlab 函数。完整非线性分析程序见附录 F。

PolyStress 中的 Newton-Raphson 程序只用一个荷载步求解非线性弹性变分问题。单荷载步配合弱线搜索足以有效求解本文全部问题。[^11]

## 6.4 双线性材料模型

只要定义了储能函数 $W_0$，上述非线性有限元程序便能容纳任意非线性材料模型。所有材料模型均由非线性有限元程序通过 `material_model` 函数调用。其中一种模型属于锥分片线弹性材料（conewise linear elastic materials），它是双模量材料的推广（Curnier et al. 1994）。为定义其应变能密度，将无穷小应变空间 $\mathcal E$ 划分为压缩子域 $\mathcal E_c=\{\boldsymbol{\varepsilon}\in\mathcal E\mid\chi(\boldsymbol{\varepsilon})<0\}$ 与拉伸子域 $\mathcal E_t=\{\boldsymbol{\varepsilon}\in\mathcal E\mid\chi(\boldsymbol{\varepsilon})>0\}$，其中 $\chi(\boldsymbol{\varepsilon})=\operatorname{tr}(\boldsymbol{\varepsilon})$ 用于保证 $W_0$ 连续可微。Cauchy 应力张量在整个 $\mathcal E$ 上连续的锥分片线弹性材料，其储能密度为

$$
W_0(\boldsymbol{\varepsilon})=
\frac12\lambda(\boldsymbol{\varepsilon})\operatorname{tr}^2(\boldsymbol{\varepsilon})
+\mu\operatorname{tr}(\boldsymbol{\varepsilon}^2),
\tag{59}
$$

其中 $\mu$ 为剪切模量，Lamé 参数

$$
\lambda(\boldsymbol{\varepsilon})=
\begin{cases}
\lambda_c,&\operatorname{tr}(\boldsymbol{\varepsilon})<0,\\
\lambda_t,&\operatorname{tr}(\boldsymbol{\varepsilon})>0.
\end{cases}
\tag{60}
$$

Cauchy 应力和材料模量张量分别为

$$
\begin{aligned}
\boldsymbol{\sigma}(\boldsymbol{\varepsilon})&=
\frac{\partial W_0}{\partial\boldsymbol{\varepsilon}}=
\lambda(\boldsymbol{\varepsilon})\operatorname{tr}(\boldsymbol{\varepsilon})\boldsymbol{I}
+2\mu\boldsymbol{\varepsilon},\\
\boldsymbol{C}_T(\boldsymbol{\varepsilon})&=
\frac{\partial^2W_0}{\partial\boldsymbol{\varepsilon}^2}=
\lambda(\boldsymbol{\varepsilon})\boldsymbol{I}\otimes\boldsymbol{I}
+2\mu\boldsymbol{I}\mathbin{\underline\otimes}\boldsymbol{I}.
\end{aligned}
\tag{61}
$$

对任意二阶张量 $\boldsymbol{a}$、$\boldsymbol{b}$，$(\boldsymbol{a}\otimes\boldsymbol{b})_{ijkl}=a_{ij}b_{kl}$，$(\boldsymbol{a}\mathbin{\underline\otimes}\boldsymbol{b})_{ijkl}=\tfrac12(a_{ik}b_{jl}+a_{il}b_{jk})$。以拉伸 Young 模量 $E_t$ 和压缩 Young 模量 $E_c$ 表示时

$$
\lambda_c=\frac{\mu(E_c-2\mu)}{3\mu-E_c},
\qquad
\lambda_t=\frac{\mu(E_t-2\mu)}{3\mu-E_t}.
\tag{62}
$$

当 $\operatorname{tr}(\boldsymbol{\varepsilon})>0$ 时，材料以 $(E_t,\mu)$ 表现为线弹性；当 $\operatorname{tr}(\boldsymbol{\varepsilon})<0$ 时，以 $(E_c,\mu)$ 表现为线弹性。即使 $E_t\neq E_c$，应变能密度和应力张量在整个应变空间及 $\mathcal E_t$ 与 $\mathcal E_c$ 的界面上仍连续，证明见附录 C。

在 PolyStress 中，$\operatorname{tr}(\boldsymbol{\varepsilon})<0$ 时用压缩性质 $(E_c,\mu)$ 计算应力与材料切线矩阵，$\operatorname{tr}(\boldsymbol{\varepsilon})>0$ 时用拉伸性质 $(E_t,\mu)$。该模型由补充材料中的 `material_model` 实现。在 `PolyScript` 中使用双线性模型时应设置

```matlab
fem.MatModel = 'Bilinear';
fem.MatParam = [Et,Ec,G];
```

其中 `Et`、`Ec`、`G` 分别为拉伸 Young 模量、压缩 Young 模量和剪切模量。

## 6.5 设计变量更新方案

PolyTop 用基于最优性准则（optimality criteria, OC）的方法更新设计变量；应力约束问题则需要不同的更新方案。本文实现了适于求解式 (43) 这类无约束问题的 MMA 版本。每个 AL 步中，不直接求解式 (43)，而求解近似凸子问题

$$
\begin{aligned}
\min_{\boldsymbol{z}\in[0,1]^N}\quad
&\widetilde J^{(k)}(\boldsymbol{z})=r^{(k)}+
\sum_{\ell=1}^N\left[
\frac{p_\ell^{(k)}}{U_\ell^{(k)}-z_\ell}+
\frac{q_\ell^{(k)}}{z_\ell-L_\ell^{(k)}}\right]\\
\text{s.t.}\quad &\bar\alpha_\ell^{(k)}\leq z_\ell\leq\bar\beta_\ell^{(k)},
\quad\ell=1,\ldots,N.
\end{aligned}
\tag{63}
$$

其中 $\bar\alpha_\ell^{(k)}=\max[\underline z_\ell,\alpha_\ell^{(k)}]$，$\bar\beta_\ell^{(k)}=\min[\bar z_\ell,\beta_\ell^{(k)}]$；取 $\alpha_\ell^{(k)}=0.9L_\ell^{(k)}+0.1z_\ell^{(k)}$、$\beta_\ell^{(k)}=0.9U_\ell^{(k)}+0.1z_\ell^{(k)}$，以满足 $L_\ell^{(k)}<\alpha_\ell^{(k)}<z_\ell^{(k)}<\beta_\ell^{(k)}<U_\ell^{(k)}$。移动限值为 `move` 时，$\underline z_\ell=\max[0,z_\ell^{(k)}-\mathrm{move}]$，$\bar z_\ell=\min[1,z_\ell^{(k)}+\mathrm{move}]$。此外[^12]

$$
p_\ell^{(k)}=(U_\ell^{(k)}-z_\ell^{(k)})^2
\left[\max\left(\frac{\partial J}{\partial z_\ell},0\right)+
\tau\left|\frac{\partial J}{\partial z_\ell}\right|+
\frac{\theta}{U_\ell^{(k)}-L_\ell^{(k)}}\right],
\tag{64}
$$

$$
q_\ell^{(k)}=(z_\ell^{(k)}-L_\ell^{(k)})^2
\left[-\min\left(\frac{\partial J}{\partial z_\ell},0\right)+
\tau\left|\frac{\partial J}{\partial z_\ell}\right|+
\frac{\theta}{U_\ell^{(k)}-L_\ell^{(k)}}\right],
\tag{65}
$$

$$
r^{(k)}=J(\boldsymbol{z}^{(k)})-
\sum_{\ell=1}^N\left[
\frac{p_\ell^{(k)}}{U_\ell^{(k)}-z_\ell^{(k)}}+
\frac{q_\ell^{(k)}}{z_\ell^{(k)}-L_\ell^{(k)}}\right],
\tag{66}
$$

其中 $\tau=10^{-3}$、$\theta=10^{-6}$，$\partial J/\partial z_\ell$ 在 $\boldsymbol{z}=\boldsymbol{z}^{(k)}$ 处计算。

下、上渐近线 $L_\ell^{(k)}$ 与 $U_\ell^{(k)}$ 按 Svanberg（1987）计算。前两次迭代 $k=1,2$ 时

$$
L_\ell^{(k)}=z_\ell^{(k)}-s_\ell^{(k)}(\bar z_\ell-\underline z_\ell),
\qquad
U_\ell^{(k)}=z_\ell^{(k)}+s_\ell^{(k)}(\bar z_\ell-\underline z_\ell),
\tag{67}
$$

$k\geq3$ 时

$$
\begin{aligned}
L_\ell^{(k)}&=z_\ell^{(k)}-s_\ell^{(k)}
(z_\ell^{(k-1)}-L_\ell^{(k-1)}),\\
U_\ell^{(k)}&=z_\ell^{(k)}+s_\ell^{(k)}
(U_\ell^{(k-1)}-z_\ell^{(k-1)}).
\end{aligned}
\tag{68}
$$

当前 Matlab 实现中，$k=1,2$ 时 $s_\ell^{(k)}=\mathrm{AsymInit}$；其后

$$
s_\ell^{(k)}=
\begin{cases}
\mathrm{AsymInc},&(z_\ell^{(k)}-z_\ell^{(k-1)})(z_\ell^{(k-1)}-z_\ell^{(k-2)})>0,\\
\mathrm{AsymDecr},&(z_\ell^{(k)}-z_\ell^{(k-1)})(z_\ell^{(k-1)}-z_\ell^{(k-2)})<0,\\
1,&\text{其他情况},
\end{cases}
\tag{69}
$$

其中 `AsymInit`、`AsymInc`、`AsymDecr` 在 `opt` 中给定。

式 (63) 的极小点可显式求得，从而显著提高计算效率（Senhora 2019）：

$$
z_\ell^*=\max\{\bar\alpha_\ell^{(k)},\min[\bar\beta_\ell^{(k)},B_\ell]\},
\tag{70}
$$

$$
B_\ell=\frac{L_\ell^{(k)}p_\ell^{(k)}-U_\ell^{(k)}q_\ell^{(k)}+
(U_\ell^{(k)}-L_\ell^{(k)})\sqrt{p_\ell^{(k)}q_\ell^{(k)}}}
{p_\ell^{(k)}-q_\ell^{(k)}}.
\tag{71}
$$

上述方案在附录 E 所示 `PolyStress` 内的 `MMA_unconst` 子程序中实现。

[^8]: 附录 B 进一步说明本文施加对称性的方法。
[^9]: 若式 (17) 计算 $m_V(\boldsymbol{y})$、式 (18) 的 SIMP 计算 $m_E(\boldsymbol{y})$，则 `params=[p,B,eta0]`，分别对应 $p$、$\beta$、$\eta$。
[^10]: 弱线搜索算法取自 Ascher and Greif（2011），*A First Course in Numerical Methods*，SIAM。
[^11]: 也可实现多荷载步，只需在非线性有限元程序中增加覆盖全部荷载步的循环。
[^12]: 虽然本文使用的 $p_\ell^{(k)}$、$q_\ell^{(k)}$ 表达式与 Svanberg（1987）论文中的不同，但它们对应 Svanberg 的 Matlab MMA 实现。

# 7 数值结果

本节通过多个算例展示 PolyStress 的不同功能。所有结果均采用表 3 所列同一组参数，全文保持不变。

<center><b>
表 3：全部算例采用的输入参数
</b></center>

| 参数 | 数值 |
|---|---:|
| 初始 Lagrange 乘子估计 $\lambda_j^{(0)}$ | 0 |
| 初始惩罚因子 $\mu^{(0)}$ | 10 |
| 最大惩罚因子 $\mu_{\max}$ | 10,000 |
| 惩罚因子更新参数 $\alpha$ | 1.10 |
| SIMP 惩罚因子 $p$ | 3.5 |
| 非线性过滤指数 $q$ | 3 |
| Ersatz 参数 $\epsilon$ | $10^{-8}$ |
| 每个 AL 步的 MMA 迭代数 `MMA_Iter` | 5 |
| 初始阈值投影惩罚因子 $\beta$ | 1 |
| 最大阈值投影惩罚因子 $\beta_{\max}$ | 10 |
| 阈值投影密度 $\eta$ | 0.5 |
| 初始猜测 $\boldsymbol{z}^{(0)}$ | 0.5 |
| 设计变量收敛容差 `Tol` | 0.002 |
| 应力约束收敛容差 `TolS` | 0.003 |
| AL 最大步数 `MaxIter` | 150 |

$\beta$ 从 1 开始，每 5 个 AL 步增加 1，直至 $\beta_{\max}=10$，即 `[BFreq,B0,Binc,Bmax]=[5,1,1,10]`。

除非另行说明，以下问题均采用式 (18) 中的 SIMP 材料插值。为绘图，本节 von Mises 应力图均以归一化形式表示；单元 $\ell$ 形心处的归一化 von Mises 应力为

$$
\widetilde\sigma_\ell^v=E_\ell\sigma_\ell^v/\sigma_{\mathrm{lim}},
\tag{72}
$$

其中 $E_\ell=m_E(y_\ell)$，$\sigma_\ell^v$ 由式 (56) 给出。

## 7.1 基准问题

本节求解应力约束文献中的若干典型基准问题，用以检验 PolyStress 处理不断增加的单元/约束数量、通过正则化过滤器施加对称性以及处理强几何奇异性的能力。所有基准问题均采用线性材料，即设置 `fem.MatModel='Bilinear'`、`fem.MatParam=[E0,E0,G]`，其中 $E_0$ 为 Young 模量，$G=E_0/[2(1+\nu_0)]$ 为剪切模量，$\nu_0$ 为实体材料 Poisson 比。

### 7.1.1 L 形支架

第一个算例是应力约束文献中广泛采用的 L 形支架（例如 Pereira et al. 2004; Bruggi 2008; Paris et al. 2009, 2010; Lee et al. 2010; Guo et al. 2011; Bruggi and Duysinx 2012; Xia et al. 2012; Luo et al. 2013; Zhang et al. 2013; Holmberg et al. 2013a, 2013b; Emmendoerfer and Fancello 2014, 2016; Lee et al. 2016; Verbart et al. 2016; da Silva et al. 2018, 2019a）。其设计域与边界条件见图 4。材料参数为 $E_0=70\ \mathrm{GPa}$、$\nu_0=0.25$、$\sigma_{\mathrm{lim}}=100\ \mathrm{MPa}$。

![[GiraldoLondono2021_Fig4.png]]

<center><b>
图 4：L 形支架设计域与边界条件
</b></center>

用 PolyMesher 生成四个逐步加密的规则四边形网格，单元数约从 50,000 增至 500,000；过滤半径取 $R=0.05\ \mathrm m$。图 5 表明，各级网格所得优化拓扑彼此一致。

![[GiraldoLondono2021_Fig5.png]]

<center><b>
图 5：不同网格加密水平下的 L 形支架拓扑（上）与 von Mises 应力图（下）
</b></center>

为分析 PolyStress 的效率，程序运行 200 次迭代，即 40 个 AL 步、每步 5 次 MMA 迭代，并用 Matlab profiler 统计时间。[^13]

<center><b>
表 4：L 形支架前 200 次优化迭代的运行时间分解
</b></center>

| 项目 | 50,176 | 99,856 | 200,704 | 501,264 |
|---|---:|---:|---:|---:|
| 预计算 | 33.7 (11.6%) | 58.2 (9.4%) | 116.8 (7.1%) | 291.4 (4.7%) |
| 计算 $\boldsymbol{P}$ | 13.5 (4.7%) | 36.0 (5.8%) | 366.7 (22.2%) | 2480.2 (40.0%) |
| 组装 $\boldsymbol{K}$ | 99.4 (34.3%) | 203.9 (32.8%) | 419.8 (25.4%) | 1065.0 (17.2%) |
| 求解 $\boldsymbol{KU}=\boldsymbol{F}$ | 58.8 (20.3%) | 138.7 (22.3%) | 308.0 (18.6%) | 886.9 (14.3%) |
| 评价 von Mises 应力 | 14.2 (4.9%) | 28.0 (4.5%) | 59.3 (3.6%) | 149.8 (2.4%) |
| AL 函数及灵敏度 | 45.1 (15.5%) | 97.3 (15.7%) | 213.0 (12.9%) | 618.8 (10.0%) |
| 映射 $\boldsymbol z$、$\boldsymbol E$、$\boldsymbol V$ | 5.0 (1.7%) | 18.7 (3.0%) | 80.3 (4.9%) | 492.9 (7.9%) |
| 更新设计变量 | 0.8 (0.3%) | 1.5 (0.2%) | 7.8 (0.5%) | 19.1 (0.3%) |
| 绘制解 | 14.1 (4.9%) | 27.3 (4.4%) | 54.9 (3.3%) | 136.2 (2.2%) |
| 其他 | 5.2 (1.8%) | 11.7 (1.9%) | 25.3 (1.5%) | 67.3 (1.1%) |
| `PolyScript` 总时间 | **290** | **621** | **1652** | **6208** |

时间单位为秒，括号内为 `PolyScript` 总运行时间百分比。

对于小网格（少于约 100,000 个单元），大部分时间用于组装刚度矩阵和求解线性系统，预计算与过滤矩阵 $\boldsymbol P$ 的计算相对较少。网格增至 200,000 个单元以上时，预计算占比仍小，但过滤矩阵计算显著增加：200,704 单元时约占总时间 22%，501,264 单元时约占 40%。

作者还用 PolyTop 求解同一问题，将其与 PolyStress 比较。表 5 一方面比较两种程序直到收敛的总运行时间，另一方面比较前 200 次迭代的时间。

<center><b>
表 5：PolyStress 与 PolyTop 的运行时间比较
</b></center>

| 网格规模 | PolyStress 总时间 (s) | PolyStress 迭代数 | PolyStress / 200 次迭代 (s) | PolyTop 总时间 (s) | PolyTop 迭代数 | PolyTop / 200 次迭代 (s) |
|---:|---:|---:|---:|---:|---:|---:|
| 50,176 | 500 | 333 | 290 | 335 | 222 | 261 |
| 99,856 | 1063 | 327 | 621 | 727 | 223 | 616 |
| 200,704 | 2883 | 362 | 1652 | 1891 | 230 | 1462 |
| 501,264 | 9439 | 309 | 6208 | 8164 | 230 | 4826 |

表 5 表明，同迭代数下 PolyStress 的计算时间均大于 PolyTop，这符合预期；前三个网格的增幅小于 13%，501,264 单元网格约为 29%。额外代价来自 von Mises 应力计算和 AL 参数更新等 PolyTop 不需要的工作。直到收敛时，PolyStress 需要更多迭代；这是因为局部应力约束问题高度非线性，需要大量迭代才能满足全部局部约束。PolyTop 的比较采用 `Tol=10^-4`。[^14]

PolyStress 也可采用传统消失约束

$$
g_j(\boldsymbol z,\boldsymbol U)=m_E(y_j)\Lambda_j\leq0,
\qquad j=1,\ldots,N.
$$

只需将 `PolyStress.m` 第 73、77、79 行替换为

```matlab
73 g = E.*s;
77 dhdVM(a1) = E(a1).*1/fem.SLim;
79 dPenaldE(a1) = (lambda(a1)+mu.*h(a1)).*s(a1);
```

作者对 50,176 单元 L 形支架采用该约束，并重新标定初始惩罚因子，发现 $\mu^{(0)}=200$ 可得到满意结果。图 6 分别给出传统消失约束与多项式消失约束结果。两者均局部满足应力约束；中间的 von Mises 应力图和右侧屈服面图均显示所有应力评价点位于 von Mises 包络内。但两者拓扑和最优体积分数不同：传统约束得到 $f(\boldsymbol z^*)=0.34$，多项式约束得到 $f(\boldsymbol z^*)=0.33$。由于问题非凸，改变模型参数或约束定义会使优化器收敛至不同局部极小点，这种差异符合预期。

![[GiraldoLondono2021_Fig6.png]]

<center><b>
图 6：50,176 单元 L 形支架的优化拓扑（左）、von Mises 应力图（中）和 von Mises 屈服面（右）；(a) 传统消失约束，(b) 多项式消失约束
</b></center>

### 7.1.2 门式框架

下一个基准问题是门式框架（Le et al. 2010; Lian et al. 2017; da Silva et al. 2019a），几何与边界条件见图 7。设计域用 PolyMesher 离散为 100,000 个多边形有限元。[^15] 线性材料参数为 $E_0=100\ \mathrm{GPa}$、$\nu_0=0.25$、$\sigma_{\mathrm{lim}}=1000\ \mathrm{MPa}$。

![[GiraldoLondono2021_Fig7.png]]

<center><b>
图 7：门式框架设计域与边界条件
</b></center>

本例比较 SIMP 与 RAMP 插值，RAMP 在式 (18) 中取 $p_0=3.5$。过滤半径取 $R=0.25\ \mathrm m$，并通过过滤算子施加关于 $y$ 轴的对称性：`P=PolyFilter(fem,R,q,'Y')`，其中 $q=3$。虽然不施加对称也能得到近似对称的解，但多边形网格本身不关于 $y$ 轴对称，因此显式施加对称性。图 8 表明，无论 SIMP 还是 RAMP，PolyStress 都从门式框架下部中央凹角的应力集中区移除了材料。由于应力约束问题高度非线性，两种插值得到不同解；二者均局部满足应力约束。

![[GiraldoLondono2021_Fig8.png]]

<center><b>
图 8：采用 (a) SIMP 与 (b) RAMP 得到的门式框架拓扑（左）、von Mises 应力图（中）及屈服面（右）
</b></center>

### 7.1.3 眼杆

眼杆是 Pereira et al.（2004）提出的实际设计问题，目标是优化悬索桥眼杆链中的一个眼杆。几何与边界条件见图 9。孔边受到大小为 $P$ 的水平分布荷载，其分布函数为 $t(x,y)=r^2-y^2$，其中 $(x,y)=(0,0)$ 为圆心，$r$ 为圆半径。

![[GiraldoLondono2021_Fig9.png]]

<center><b>
图 9：眼杆设计域与边界条件
</b></center>

材料参数为 $E_0=200\ \mathrm{GPa}$、$\nu_0=0.3$、$\sigma_{\mathrm{lim}}=450\ \mathrm{MPa}$。设计域采用 100,000 个多边形有限元，过滤半径 $R=0.04\ \mathrm m$。[^16] 图 10 显示，受荷边界上出现两个小孔；传统设计方法不易得到这种特征，说明基于应力的拓扑优化能够产生非直观设计。

![[GiraldoLondono2021_Fig10.png]]

<center><b>
图 10：眼杆拓扑（左）与 von Mises 应力图（右）
</b></center>

### 7.1.4 裂纹

裂纹问题见 Emmendoerfer and Fancello（2014, 2016）及 Chu et al.（2018）。本文求解 Emmendoerfer and Fancello（2014）问题的轻微修改版本，见图 11；由于对称，只建模一半设计域。[^17] 该问题检验 PolyStress 处理裂纹尖端等强奇异性的能力。

![[GiraldoLondono2021_Fig11.png]]

<center><b>
图 11：裂纹设计域与边界条件
</b></center>

材料参数为 $E_0=70\ \mathrm{GPa}$、$\nu_0=0.25$、$\sigma_{\mathrm{lim}}=100\ \mathrm{MPa}$。采用 100,352 个规则四边形单元及 $R=0.045\ \mathrm m$，得到图 12 的拓扑。PolyStress 将裂纹尖端圆滑化，从而消除引起应力集中的几何奇异性。

![[GiraldoLondono2021_Fig12.png]]

<center><b>
图 12：裂纹拓扑（左）与 von Mises 应力图（右）
</b></center>

## 7.2 牛腿设计

本例对图 13 所示牛腿结构进行优化，得到三个设计：线性材料、拉伸主导双线性材料，以及关于 $x$ 轴施加对称性的同一拉伸主导双线性材料。两类材料的单轴应力—应变曲线见图 13b；对称性通过 `P=PolyFilter(fem,R,q,'X')` 施加。线性材料参数为 $E_0=70\ \mathrm{GPa}$、$\nu_0=0.25$；双线性材料参数为 $E_t=70\ \mathrm{GPa}$、$E_c=28\ \mathrm{GPa}$、$G=28\ \mathrm{GPa}$。设计域采用 79,524 个规则四边形单元，过滤半径 $R=0.15\ \mathrm m$。[^18]

![[GiraldoLondono2021_Fig13.png]]

<center><b>
图 13：牛腿设计；(a) 设计域与边界条件，(b) 线性和双线性材料的单轴应力—应变曲线
</b></center>

线性材料结果见图 14a，按预期关于 $x$ 轴对称，最优体积分数为 0.23。双线性材料的非对称结果见图 14b，图 14a 中部分压缩主导区域被移除，体积分数为 0.22。施加对称性后得到图 14c；由于对称性通过过滤算子隐式增加了约束，其体积分数按预期增至 0.25。

![[GiraldoLondono2021_Fig14.png]]

<center><b>
图 14：牛腿拓扑（上）与 von Mises 应力图（下）；(a) 线性材料，(b) 拉伸主导双线性材料，(c) 通过过滤算子施加对称性的拉伸主导双线性材料
</b></center>

## 7.3 天线支撑支架设计

本例优化图 15a 所示天线支撑支架。共考虑三种材料：一种线性材料，参数为 $E_0=120\ \mathrm{GPa}$、$\nu_0=0.3$、$\sigma_{\mathrm{lim}}=1000\ \mathrm{MPa}$；另两种采用可压缩 Ogden 模型（Ogden 1972; Feng et al. 2006）的非线性材料：

$$
\begin{aligned}
W_0(\varepsilon_1,\varepsilon_2,\varepsilon_3)={}&
\sum_{p=1}^n\frac{\mu_p}{\alpha_p}
(\lambda_1^{\alpha_p}+\lambda_2^{\alpha_p}+\lambda_3^{\alpha_p}-3)\\
&+\sum_{p=1}^n\frac{\mu_p}{\alpha_p\beta_p}
[(\lambda_1\lambda_2\lambda_3)^{-\alpha_p\beta_p}-1],
\end{aligned}
\tag{73}
$$

其中 $\alpha_p$、$\mu_p$、$\beta_p$、$n$ 为材料参数，$\lambda_i=\varepsilon_i+1$（$i=1,2,3$）是在小变形下定义的主伸长率。将 Ogden 模型加入 PolyStress 只需在 `material_model` 中加入应力向量 $\boldsymbol\sigma$ 和材料切线矩阵 $\boldsymbol D$；解析表达式见 Chi et al.（2019）。本文取单项模型 $n=1$，并在同一 $E_0$、$\nu_0$ 下分别取 $\alpha_1=100$ 和 $\alpha_1=-100$，对应拉伸主导与压缩主导材料。`PolyScript` 中设置

```matlab
fem.MatModel = 'Ogden';
fem.MatParam = [mu1,alpha1,beta1];
```

其中 $\mu_1=E_0/[\alpha_1(1+\nu_0)]$，$\beta_1=\nu_0/(1-2\nu_0)$。[^19]

![[GiraldoLondono2021_Fig15.png]]

<center><b>
图 15：天线支撑支架问题；(a) 设计域与边界条件，(b) 三种材料的单轴应力—应变曲线；竖向虚线为曲线与 $\sigma_{11}/\sigma_{\mathrm{lim}}=\pm1$ 的交点
</b></center>

图 15b 的单轴应力按 $\sigma_{\mathrm{lim}}$ 归一化，可由曲线与 $\sigma_{11}/\sigma_{\mathrm{lim}}=\pm1$ 的交点估计最优设计中的应变范围：线性材料约为 $[-8,8]\times10^{-3}$；拉伸主导 Ogden 1 约为 $[-12,6]\times10^{-3}$；压缩主导 Ogden 2 约为 $[-6,12]\times10^{-3}$。

设计域采用 30,000 个多边形有限元与 $R=0.07\ \mathrm m$，[^20][^radius-discrepancy] 得到图 16。拓扑和变形程度对材料模型高度敏感：线性材料主应变约在 $[-8,8]\times10^{-3}$；拉伸主导材料的压缩变形大于拉伸变形，主应变约在 $[-12,6]\times10^{-3}$；压缩主导材料的拉伸变形更大，主应变约在 $[-6,12]\times10^{-3}$。三者与图 15b 的预期一致，且应变足够小，仍适用小应变弹性理论。[^21]

![[GiraldoLondono2021_Fig16.png]]

<center><b>
图 16：天线支撑支架拓扑（左）、von Mises 应力图（中）及主应变图（右）；(a) 线性材料，(b) 拉伸主导材料 Ogden 1，(c) 压缩主导材料 Ogden 2
</b></center>

外荷载幅值会影响优化结果：荷载越大，最优体积分数越大，反之亦然。但作者认为荷载幅值只影响最优体积分数，不影响最优结构中的最大和最小应变，因为应变极值主要由 $\sigma_{\mathrm{lim}}$ 限制。为验证这一点，作者对线性材料天线支架采用多个 $P/P_0$ 求解，其中 $P_0$ 是图 16 的荷载。图 17 表明，随着 $P/P_0$ 增大，最优体积分数增加，而最大应变保持不变；$P/P_0$ 超过约 1.4 后不再存在可行解。

![[GiraldoLondono2021_Fig17.png]]

<center><b>
图 17：外荷载幅值对线性材料天线支架结果的影响；(a) 最优体积分数随 $P/P_0$ 的变化，(b) 最优设计最大主应变随 $P/P_0$ 的变化
</b></center>

## 7.4 吊钩设计

最后一个算例是图 18 所示吊钩。线性材料参数为 $E_0=100\ \mathrm{GPa}$、$\nu_0=0.25$、$\sigma_{\mathrm{lim}}=120\ \mathrm{MPa}$。本例比较 PolyStress 的应力设计与 PolyTop 的柔顺度设计。两者使用相同材料插值和延拓方案：体积插值用式 (17)，刚度插值用式 (18) 的 SIMP。PolyTop 从 $\beta=1$ 开始，每 25 次迭代令 $\beta$ 增加 1、$p$ 增加 0.5。[^22] 柔顺度最小化在 $p=1$ 时为凸问题，因此从 $p=1$ 开始延拓有助于惩罚中间密度并得到黑白解；应力约束问题即使 $p=1$ 也非凸，故这种 $p$ 延拓没有明显优势。

![[GiraldoLondono2021_Fig18.png]]

<center><b>
图 18：吊钩设计域与边界条件
</b></center>

采用 100,000 个多边形有限元和 $R=0.04\ \mathrm m$ 得到图 19。[^23] 两种设计体积分数均为 0.35，但拓扑显著不同。在应力设计中，圆孔下方材料向设计域外边界移动，使孔边与设计域下部应力均低于限值；柔顺度设计中，圆孔下方杆件间距较小，导致孔两侧和设计域下部发生应力集中，超过应力限值约 150%。该比较说明，若要使结构在给定荷载下避免材料失效，基于应力的公式十分重要。

![[GiraldoLondono2021_Fig19.png]]

<center><b>
图 19：吊钩拓扑（左）与 von Mises 应力图（右）；(a) PolyStress 应力设计，(b) PolyTop 柔顺度设计；两者体积分数均为 0.35，柔顺度设计超过应力限值约 150%
</b></center>

[^13]: 计算使用 Matlab 2017a，硬件为 Xeon(R) CPU E5-1660 v3 @ 3.00 GHz、256 GB RAM。
[^14]: PolyTop 采用收敛容差 `Tol=10^-4`。
[^15]: 运行本例时，将 `PolyScript.m` 第 11 行替换为 `[Node,Element,Supp,Load,~]=PolyMesher(@PortalDomain,NElem,100)`，并取 `NElem=100000`。
[^16]: 运行本例时，将 `PolyScript.m` 第 11 行替换为 `[Node,Element,Supp,Load,~]=PolyMesher(@EyeBarDomain,NElem,100)`，并取 `NElem=100000`。
[^17]: 运行本例时，将 `PolyScript.m` 第 11 行替换为 `[Node,Element,Supp,Load]=Mesh_Crack_Prob(Ne_ap); NElem=size(Element,1)`，并取 `Ne_ap=100000`。
[^18]: 运行本例时，将 `PolyScript.m` 第 11 行替换为 `[Node,Element,Supp,Load]=Mesh_Corbel(Ne_ap); NElem=size(Element,1)`，并取 `Ne_ap=80000`。
[^19]: 式 (73) 中 $n>1$ 时，设置 `fem.MatParam=[mu1,alpha1,beta1,...,mun,alphan,betan]`。
[^20]: 运行本例时，将 `PolyScript.m` 第 11 行替换为 `[Node,Element,Supp,Load,~]=PolyMesher(@AntennaDomain,NElem,100)`，并取 `NElem=30000`。
[^21]: 如果应变继续增大到小应变弹性不再成立，则必须把整个公式修改为有限变形形式，超出本文范围。
[^22]: PolyTop 每个延拓步的 25 次迭代与 PolyStress 的 5 个 AL 步一致，因为 PolyStress 每个 AL 步执行 5 次 MMA 迭代，即每个延拓步有 `MMA_Iter*BFreq=25` 次有限元求解。
[^23]: 运行本例时，将 `PolyScript.m` 第 11 行替换为 `[Node,Element,Supp,Load,~]=PolyMesher(@HookDomain,NElem,100)`，并取 `NElem=100000`。

# 8 说明（Remarks）

本文给出多个基准问题，展示 PolyStress 在不同网格加密程度与不同设计域上求解应力约束拓扑优化的能力。经典 L 形支架采用约 50,000 至约 500,000 个单元的多种网格，所得解不随网格规模发生实质变化。针对线性材料 L 形支架的计算效率分析表明，虽然 PolyStress 处理成千上万个局部约束，其运行时间与仅含一个体积约束、用于柔顺度最小化的 PolyTop 仍处于同一数量级。

除基准问题外，本文还求解两个非线性材料问题。第一个是由线性或双线性材料构成的牛腿；双线性材料算例表明，只需修改计算过滤密度场的函数，PolyStress 便可得到对称设计。第二个是采用可压缩 Ogden 材料的天线支撑支架；单项 Ogden 模型分别表示拉伸主导与压缩主导材料，所得拓扑清楚显示最优设计对材料模型高度敏感。最后还设计了线性材料吊钩，并与 PolyTop 结果比较，说明基于应力的框架对于获得承受给定荷载且避免材料失效的结构十分重要。

# 9 结论

本文提出一个基于增广拉格朗日方法、考虑局部且不聚合应力约束的拓扑优化框架，并据此开发教学 Matlab 代码 PolyStress。该代码属于面向非结构多边形有限元网格的一系列教学代码，与 PolyTop、PolyFluid 和 PolyMat 一脉相承。PolyStress 考虑材料非线性，因此修改 PolyTop 的分析程序，用 Newton-Raphson 方法求解非线性有限元问题；同时修改优化算法，引入 AL 方法求解局部应力约束问题。

AL 方法将含大量约束的原问题转化为一系列无约束问题，并用适于无约束 AL 子问题的 MMA 版本更新设计变量。无约束子问题的凸近似具有显式解，能够显著节省计算资源。

PolyStress 是技术文献中首个面向应力约束拓扑优化的教学代码。作者希望它能推动研究者学习并探索 AL 方法，求解超出本文范围的优化问题。由于 PolyStress 能够处理大量应力约束，作者也希望它能连接学术研究与商业软件开发，使拓扑优化适用于工业问题。

本文以 Duysinx 和 Bendsøe（1998）的一段话作结：

> “提高应力场分析质量同样具有重要意义，这能使应力设计方法更适用于多种应用。”

在本文语境下，工程应用中的应力设计方法有赖于应力约束拓扑优化与连续介质力学之间的一致性。因此，无论优化阶段还是相关边值问题的数值求解阶段，都应对局部应力进行处理。

# 致谢

本文献给 Martin P. Bendsøe 教授。他激发了作者对本文以及 Senhora et al.（2020）、Giraldo-Londoño and Paulino（2020）等近期研究工作的兴趣。更具体地说，Paulino 教授与 Bendsøe 教授在第十届世界结构与多学科优化大会（WCSMO 10，2013 年 5 月 19–24 日，美国佛罗里达州 Orlando）期间的一次早期讨论，点燃了作者对本主题的求知兴趣。

**经费说明**：本研究得到美国国家科学基金会项目 #1663244 及 Georgia Institute of Technology Raymond Allen Jones Chair 的支持。

**伦理标准遵循**

**免责声明**：本文结果的解释仅代表作者观点，不一定反映资助方或资助机构的观点。

**利益冲突**：作者声明不存在利益冲突。

**结果复现**：本文全部结果均可用电子补充材料所提供代码复现。

# 附录 A：基准算例库

本附录汇总全文设计问题，包括设计域说明以及生成各问题有限元网格所需的 Matlab 文件名。

<center><b>
表 6：PolyStress 提供的算例（原文设计域几何图）
</b></center>

![[GiraldoLondono2021_Table6_1.png]]

![[GiraldoLondono2021_Table6_2.png]]

<center><b>
表 6：PolyStress 提供的算例
</b></center>

| 设计域 | 说明 |
|---|---|
| L 形支架 | PolyMesher 域文件：`@LbracketDomain`；尺寸与荷载：$L=1$、$d=0.06$、$P=2$；线性材料：$E_0=70\ \mathrm{GPa}$、$\nu_0=0.25$、$\sigma_{\mathrm{lim}}=100\ \mathrm{MPa}$；过滤半径：$R=0.05$ |
| 门式框架 | PolyMesher 域文件：`@PortalDomain`；尺寸与荷载：$L=12$、$H=6$、$d=1$、$P=300$；线性材料：$E_0=100\ \mathrm{GPa}$、$\nu_0=0.25$、$\sigma_{\mathrm{lim}}=1000\ \mathrm{MPa}$；过滤半径：$R=0.25$ |
| 眼杆 | PolyMesher 域文件：`@EyeBarDomain`；尺寸与荷载：$L=1.6$、$H=0.8$、$R=0.15$、$d=0.15$、$P=70$；线性材料：$E_0=200\ \mathrm{GPa}$、$\nu_0=0.3$、$\sigma_{\mathrm{lim}}=450\ \mathrm{MPa}$；过滤半径：$R=0.04$ |
| 裂纹 | PolyMesher 域文件：`@CrackDomain`；尺寸与荷载：$L=2$、$d=0.1$、$P=5$；线性材料：$E_0=70\ \mathrm{GPa}$、$\nu_0=0.25$、$\sigma_{\mathrm{lim}}=100\ \mathrm{MPa}$；过滤半径：$R=0.045$ |
| 牛腿 | PolyMesher 域文件：`@CorbelDomain`；尺寸与荷载：$L=2$、$d=0.3$、$P=15$；材料 1：线性，$E_0=70\ \mathrm{GPa}$、$\nu_0=0.25$、$\sigma_{\mathrm{lim}}=90\ \mathrm{MPa}$；材料 2：双线性，$E_t=70\ \mathrm{GPa}$、$E_c=28\ \mathrm{GPa}$、$G=28\ \mathrm{GPa}$、$\sigma_{\mathrm{lim}}=90\ \mathrm{MPa}$；过滤半径：$R=0.15$ |
| 天线支撑支架 | PolyMesher 域文件：`@AntennaDomain`；尺寸与荷载：$L=1$、$H=1.75$、$d=0.048$、$P=40$；材料 1：线性，$E_0=120\ \mathrm{GPa}$、$\nu_0=0.3$、$\sigma_{\mathrm{lim}}=1000\ \mathrm{MPa}$；材料 2、3：可压缩 Ogden，$E_0=120\ \mathrm{GPa}$、$\nu_0=0.3$、$\alpha_1=\pm100$、$\sigma_{\mathrm{lim}}=1000\ \mathrm{MPa}$；过滤半径：$R=0.08$ |
| 吊钩 | PolyMesher 域文件：`@HookDomain`；尺寸取 Talischi et al.（2012b）的 $1/100$，$P=5$；线性材料：$E_0=100\ \mathrm{GPa}$、$\nu_0=0.25$、$\sigma_{\mathrm{lim}}=120\ \mathrm{MPa}$；过滤半径：$R=0.04$ |

# 附录 B：利用正则化过滤器施加对称性

在连续统框架下，可用算子 $P_s(\eta(\boldsymbol{x}))$ 对容许密度场空间施加对称性；该算子按所需对称性映射设计函数，例如关于 $x_1$ 轴对称时 $P_s(\eta(\boldsymbol{x}))=\eta(x_1,|x_2|)$。对称化容许密度场空间由式 (12) 给出，对应正则化映射 $P(\eta)=(P_F\circ P_s)(\eta)$。

离散后，对称化过滤矩阵 $\boldsymbol P$ 为

$$
P_{\ell k}=\frac{w_{\ell k}v_k}{\sum_{j=1}^Nw_{\ell j}v_j},
\qquad
w_{\ell k}=\max\left(0,1-\frac{\|\widetilde{\boldsymbol{x}}_\ell-
\widetilde{\boldsymbol{x}}_k\|_2}{R}\right)^q,
\tag{74}
$$

其中，关于 $x_1$ 轴对称时

$$
\widetilde{\boldsymbol{x}}_\ell=[x_1^\ell,|x_2^\ell|]^{\mathsf T},
\tag{75}
$$

关于 $x_2$ 轴对称时

$$
\widetilde{\boldsymbol{x}}_\ell=[|x_1^\ell|,x_2^\ell]^{\mathsf T},
\tag{76}
$$

同时关于 $x_1$、$x_2$ 轴对称时

$$
\widetilde{\boldsymbol{x}}_\ell=[|x_1^\ell|,|x_2^\ell|]^{\mathsf T}.
\tag{77}
$$

通过过滤矩阵施加对称性的功能已经加入电子补充材料中的 `PolyFilter`。

# 附录 C：双线性材料模型的连续性证明

Curnier et al.（1994）指出，式 (59) 的应变能函数在整个无穷小应变空间 $\mathcal E$ 中连续。当 $\chi(\boldsymbol\varepsilon)=\operatorname{tr}(\boldsymbol\varepsilon)>0$ 时，材料在拉伸子域 $\mathcal E_t$ 中以 $(\lambda_t,\mu)$ 表现为线弹性；当 $\operatorname{tr}(\boldsymbol\varepsilon)<0$ 时，在压缩子域 $\mathcal E_c$ 中以 $(\lambda_c,\mu)$ 表现为线弹性。以下证明应变能与应力张量在整个应变空间中连续。

首先证明应变能密度连续。由式 (59)–(60)，$\operatorname{tr}(\boldsymbol\varepsilon)>0$ 时

$$
W_0=W_0^+=\frac12\lambda_t\operatorname{tr}^2(\boldsymbol\varepsilon)
+\mu\operatorname{tr}(\boldsymbol\varepsilon^2),
\tag{78}
$$

它在 $\mathcal E_t$ 上二阶连续可微。同理，$\operatorname{tr}(\boldsymbol\varepsilon)<0$ 时

$$
W_0=W_0^-=\frac12\lambda_c\operatorname{tr}^2(\boldsymbol\varepsilon)
+\mu\operatorname{tr}(\boldsymbol\varepsilon^2),
\tag{79}
$$

它在 $\mathcal E_c$ 上二阶连续可微。在拉伸与压缩子域的界面 $\operatorname{tr}(\boldsymbol\varepsilon)=0$ 上

$$
W_0|_{\operatorname{tr}(\boldsymbol\varepsilon)=0}
=W_0^+|_{\operatorname{tr}(\boldsymbol\varepsilon)=0}
=W_0^-|_{\operatorname{tr}(\boldsymbol\varepsilon)=0}
=\mu\operatorname{tr}(\boldsymbol\varepsilon^2),
\tag{80}
$$

故应变能跨界面连续。

再证明应力张量 $\boldsymbol\sigma=\partial W_0/\partial\boldsymbol\varepsilon$ 连续。若 $\operatorname{tr}(\boldsymbol\varepsilon)>0$，

$$
\boldsymbol\sigma(\boldsymbol\varepsilon)=\boldsymbol\sigma^+
=\lambda_t\operatorname{tr}(\boldsymbol\varepsilon)\boldsymbol I+2\mu\boldsymbol\varepsilon,
\tag{81}
$$

它在 $\mathcal E_t$ 上连续可微；若 $\operatorname{tr}(\boldsymbol\varepsilon)<0$，

$$
\boldsymbol\sigma(\boldsymbol\varepsilon)=\boldsymbol\sigma^-
=\lambda_c\operatorname{tr}(\boldsymbol\varepsilon)\boldsymbol I+2\mu\boldsymbol\varepsilon,
\tag{82}
$$

它在 $\mathcal E_c$ 上连续可微。在界面上

$$
\boldsymbol\sigma|_{\operatorname{tr}(\boldsymbol\varepsilon)=0}
=\boldsymbol\sigma^+|_{\operatorname{tr}(\boldsymbol\varepsilon)=0}
=\boldsymbol\sigma^-|_{\operatorname{tr}(\boldsymbol\varepsilon)=0}
=2\mu\boldsymbol\varepsilon,
\tag{83}
$$

证明完毕。式 (61) 第二式的弹性张量可在拉伸与压缩子域界面上不连续，但分别在 $\mathcal E_t$ 与 $\mathcal E_c$ 内分片连续。该不连续性未表现出数值不稳定，也未导致收敛问题。

# 附录 D：PolyScript

下图为原文给出的完整 `PolyScript` 程序清单。为保持程序字符、注释和行号与论文完全一致，此处保留原文清单图，不重构为可复制代码。

![[GiraldoLondono2021_AppendixD.png]]

<center><b>
附录 D：`PolyScript` 原文程序清单
</b></center>

# 附录 E：PolyStress

以下三页为原文给出的完整 `PolyStress` 程序清单，依原页顺序保留。

![[GiraldoLondono2021_AppendixE_1.png]]

![[GiraldoLondono2021_AppendixE_2.png]]

![[GiraldoLondono2021_AppendixE_3.png]]

<center><b>
附录 E：`PolyStress` 原文程序清单
</b></center>

# 附录 F：NLFEM

下图为原文给出的完整 `NLFEM` 程序清单。

![[GiraldoLondono2021_AppendixF.png]]

<center><b>
附录 F：`NLFEM` 原文程序清单
</b></center>

[^radius-discrepancy]: 译者注：原文第 7.3 节取过滤半径 0.07 m，附录 A 表 6 的同一算例列为 0.08；两处原值均保留，原文未解释该差异。

# 参考文献

- Bendsøe MP (1989) Optimal shape design as a material distribution problem. *Struct Optim* 1(4):193–202.
- Bendsøe MP, Kikuchi N (1988) Generating optimal topologies in structural design using a homogenization method. *Comput Methods Appl Mech Eng* 93:291–318.
- Bendsøe MP (1995) *Optimization of structural topology, shape, and material*. Springer, Berlin.
- Bendsøe MP, Sigmund O (2003) *Topology optimization: theory, methods and applications*. Springer, Berlin.
- Bertsekas DP (1999) *Nonlinear programming*, 2nd edn. Athena Scientific, Nashua.
- Borrvall T, Petersson J (2001) Topology optimization using regularized intermediate density control. *Comput Methods Appl Mech Eng* 190(37–38):4911–4928.
- Bourdin B (2001) Filters in topology optimization. *Int J Numer Methods Eng* 50(9):2143–2158.
- Bruggi M (2008) On an alternative approach to stress constraints relaxation in topology optimization. *Struct Multidiscip Optim* 36(2):125–141.
- Bruggi M, Duysinx P (2012) Topology optimization for minimum weight with compliance and stress constraints. *Struct Multidiscip Optim* 46(3):369–384.
- Cheng GD, Jiang Z (1992) Study on topology optimization with stress constraints. *Eng Optim* 20(2):129–148.
- Chi H, Ramos DL, Ramos AS Jr, Paulino GH (2019) On structural topology optimization considering material nonlinearity: Plane strain versus plane stress solutions. *Adv Eng Softw* 131:217–231.
- Chu S, Gao L, Xiao M, Luo Z, Li H, Gui X (2018) A new method based on adaptive volume constraint and stress penalty for stress-constrained topology optimization. *Struct Multidiscip Optim* 57(3):1163–1185.
- Curnier A, He QC, Zysset P (1994) Conewise linear elastic materials. *J Elast* 37(1):1–38.
- da Silva GA, Beck AT, Cardoso EL (2018) Topology optimization of continuum structures with stress constraints and uncertainties in loading. *Int J Numer Methods Eng* 113(1):153–178.
- da Silva GA, Beck AT, Sigmund O (2019a) Stress-constrained topology optimization considering uniform manufacturing uncertainties. *Comput Methods Appl Mech Eng* 344:512–537.
- da Silva GA, Beck AT, Sigmund O (2019b) Topology optimization of compliant mechanisms with stress constraints and manufacturing error robustness. *Comput Methods Appl Mech Eng* 354:397–421.
- De Leon DM, Alexandersen J, Fonseca JS, Sigmund O (2015) Stress-constrained topology optimization for compliant mechanism design. *Struct Multidiscip Optim* 52(5):929–943.
- Duysinx P, Bendsøe MP (1998) Topology optimization of continuum structures with local stress constraints. *Int J Numer Methods Eng* 43(8):1453–1478.
- Emmendoerfer H Jr, Fancello EA (2014) A level set approach for topology optimization with local stress constraints. *Int J Numer Methods Eng* 99(2):129–156.
- Emmendoerfer H Jr, Fancello EA (2016) Topology optimization with local stress constraint based on level set evolution via reaction-diffusion. *Comput Methods Appl Mech Eng* 305:62–88.
- Emmendoerfer H Jr, Silva ECN, Fancello EA (2019) Stress-constrained level set topology optimization for design-dependent pressure load problems. *Comput Methods Appl Mech Eng* 344:569–601.
- Fan Z, Xia L, Lai W, Xia Q, Shi T (2019) Evolutionary topology optimization of continuum structures with stress constraints. *Struct Multidiscip Optim* 59(2):647–658.
- Fancello EA (2006) Topology optimization for minimum mass design considering local failure constraints and contact boundary conditions. *Struct Multidiscip Optim* 32(3):229–240.
- Feng ZQ, Peyraut F, He QC (2006) Finite deformations of Ogden’s materials under impact loading. *Int J Nonlin Mech* 41(4):575–585.
- Giraldo-Londoño O, Paulino GH (2020) A unified approach for topology optimization with local stress constraints considering various failure criteria: von Mises, Drucker–Prager, Tresca, Mohr–Coulomb, Bresler–Pister, and William–Warnke. *Proceedings of the Royal Society A* 476:20190861.
- Guest JK, Prévost JH, Belytschko T (2004) Achieving minimum length scale in topology optimization using nodal design variables and projection functions. *Int J Numer Methods Eng* 61(2):238–254.
- Guo X, Zhang WS, Wang MY, Wei P (2011) Stress-related topology optimization via level set approach. *Comput Methods Appl Mech Eng* 200(47–48):3439–3452.
- Holmberg E, Torstenfelt B, Klarbring A (2013a) Global and clustered approaches for stress constrained topology optimization and deactivation of design variables. In: 10th world congress on structural and multidisciplinary optimization.
- Holmberg E, Torstenfelt B, Klarbring A (2013b) Stress constrained topology optimization. *Struct Multidiscip Optim* 48(1):33–47.
- Kiyono C, Vatanabe S, Silva E, Reddy J (2016) A new multi-p-norm formulation approach for stress-based topology optimization design. *Compos Struct* 156:10–19.
- Kreisselmeier G, Steinhauser R (1979) Systematic control design by optimizing a vector performance index. In: *IFAC proceedings volumes*, vol 12, pp 113–117. IFAC Symposium on Computer Aided Design of Control Systems, Zurich, Switzerland, 29–31 August.
- Le C, Norato J, Bruns T, Ha C, Tortorelli D (2010) Stress-based topology optimization for continua. *Struct Multidiscip Optim* 41(4):605–620.
- Lee E, James KA, Martins JRRA (2012) Stress-constrained topology optimization with design-dependent loading. *Struct Multidiscip Optim* 46(5):647–661.
- Lee K, Ahn K, Yoo J (2016) A novel p-norm correction method for lightweight topology optimization under maximum stress constraints. *Comput Struct* 171:18–30.
- Lian H, Christiansen AN, Tortorelly DA, Sigmund O (2017) Combined shape and topology optimization for minimization of maximal von mises stress. *Struct Multidiscip Optim* 55(5):1541–1557.
- Liu H, Yang D, Hao P, Zhu X (2018) Isogeometric analysis based topology optimization design with global stress constraint. *Comput Methods Appl Mech Eng* 342:625–652.
- Luo Y, Wang MY, Kang Z (2013) An enhanced aggregation method for topology optimization with local stress constraints. *Comput Methods Appl Mech Eng* 254:31–41.
- Nocedal J, Wright SJ (2006) *Numerical optimization*, 2nd edn. Springer, Berlin.
- Ogden RW (1972) Large deformation isotropic elasticity–on the correlation of theory and experiment for incompressible rubberlike solids. *Proc Roy Soc Lond Math Phys Sci* 326(1567):565–584.
- Paris J, Navarrina F, Colominas I, Casteleiro M (2009) Topology optimization of continuum structures with local and global stress constraints. *Struct Multidiscip Optim* 39(4):419–437.
- Paris J, Navarrina F, Colominas I, Casteleiro M (2010) Block aggregation of stress constraints in topology optimization of structures. *Adv Eng Softw* 41(3):433–441.
- Park YK (1995) Extensions of optimal layout design using the homogenization method. Ph.D thesis, University of Michigan, Ann Arbor.
- Pereira A, Talischi C, Paulino GH, Menezes IF, Carvalho MS (2016) Fluid flow topology optimization in polytop: stability and computational implementation. *Struct Multidiscip Optim* 54(5):1345–1364.
- Pereira JT, Fancello EA, Barcellos CS (2004) Topology optimization of continuum structures with material failure constraints. *Struct Multidiscip Optim* 26(1–2):50–66.
- Rozvany GI, Zhou M, Birker T (1992) Generalized shape optimization without homogenization. *Structural Optimization* 4(3–4):250–252.
- Sanders ED, Pereira A, Aguiló MA, Paulino GH (2018) Polymat: an efficient matlab code for multi-material topology optimization. *Struct Multidiscip Optim* 58(6):2727–2759.
- Senhora FV (2019) Personal communication.
- Senhora FV, Giraldo-Londoño O, Menezes IFM, Paulino GH (2020) Topology optimization with local stress constraints: a stress aggregation-free approach. *Struct Multidiscip Optim* 62(4):1639–1668.
- Svanberg K (1987) The method of moving asymptotes—A new method for structural optimization. *Int J Numer Methods Eng* 24(2):359–373.
- Talischi C, Paulino GH, Pereira A, Menezes IFM (2012a) Polymesher: a general-purpose mesh generator for polygonal elements written in Matlab. *Struct Multidiscip Optim* 45(3):309–328.
- Talischi C, Paulino GH, Pereira A, Menezes IFM (2012b) Polytop: a Matlab implementation of a general topology optimization framework using unstructured polygonal finite element meshes. *Struct Multidiscip Optim* 45(3):329–357.
- Verbart A, Langelaar M, van Keulen F (2016) Damage approach: a new method for topology optimization with local stress constraints. *Struct Multidiscip Optim* 53(5):1081–1098.
- Wang F, Lazarov BS, Sigmund O (2011) On projection methods, convergence and robust formulations in topology optimization. *Struct Multidiscip Optim* 43(6):767–784.
- Xia L, Zhang L, Xia Q, Shi T (2018) Stress-based topology optimization using bi-directional evolutionary structural optimization method. *Comput Methods Appl Mech Eng* 333:356–370.
- Xia Q, Shi T, Liu S, Wang MY (2012) A level set solution to the stress-based structural shape and topology optimization. *Comput Struct* 90:55–64.
- Yang RJ, Chen CJ (1996) Stress-based topology optimization. *Struct Optim* 12(2):98–105.
- Zhang WS, Guo X, Wang MY, Wei P (2013) Optimal topology design of continuum structures with stress concentration alleviation via level set method. *Int J Numer Methods Eng* 93(9):942–959.
- Zhou M, Rozvany GIN (1991) The COC algorithm, part II: topological, geometrical and generalized shape optimization. *Comput Methods Appl Mech Eng* 89(1–3):309–336.

**出版方声明（Publisher’s note）**：Springer Nature 对已发表地图及机构隶属关系涉及的管辖权主张保持中立。
