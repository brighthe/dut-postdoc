---
title: "翻译：Machine Learning-Driven Real-Time Topology Optimization Under Moving Morphable Component-Based Framework"
status: "done"
date_created: 2026-07-27
date_updated: 2026-07-27
source: "[[../Lei2018-machinelearningdriven]]"
citekey: "Lei2018-machinelearningdriven"
language: "zh-CN"
---

# Machine Learning-Driven Real-Time Topology Optimization Under Moving Morphable Component-Based Framework

## 完整中文译文

> 原笔记：[[../Lei2018-machinelearningdriven]]
> Zotero 条目：`zotero://select/library/items/FFDWEI2C`
> PDF 附件：`zotero://open-pdf/library/items/4287MX5D`
> 说明：本页用于放置 Lei et al. 的完整中文译稿。按原文章节逐批审阅确认；参考文献保留正文编号，不重复录入英文文献表。

---

# 0 元数据

- **题名**：Machine Learning-Driven Real-Time Topology Optimization Under Moving Morphable Component-Based Framework
- **中文暂译**：基于移动可变形组件（MMC）框架的机器学习驱动实时拓扑优化
- **作者**：Xin Lei; Chang Liu; Zongliang Du; Weisheng Zhang; Xu Guo
- **单位**：大连理工大学工业装备结构分析国家重点实验室、工程力学系、国际计算力学中心
- **期刊**：Journal of Applied Mechanics
- **卷 / 期 / 文章号**：86(1): 011004
- **DOI**：10.1115/1.4041319
- **在线发表 / 正式卷期**：2018-10-05 / 2019-01-01
- **Zotero 条目 key**：`FFDWEI2C`
- **Zotero 附件 key**：`4287MX5D`
- **Better BibTeX key**：`Lei2018-machinelearningdriven`
- **译文状态**：全文译毕并完成公式、图表与关联页面核验

# 摘要

本文旨在探讨如何利用机器学习（machine learning, ML）技术实现实时结构拓扑优化——即一旦给定目标函数/约束函数以及外部激励/边界条件，便几乎瞬时获得规定设计域内一定量材料的优化分布；这是各领域工程师所追求的终极梦想。为此，本文采用所谓基于移动可变形组件（Moving Morphable Component, MMC）的显式拓扑优化框架生成训练集，并利用支持向量回归（support vector regression, SVR）[^abstract-svr-typo]和 K 最近邻（K-nearest neighbors, KNN）机器学习模型，建立表征优化结构布局/拓扑的设计参数与外载荷之间的映射。与现有方法相比，所提方法不仅能够显著减少训练数据量、降低参数空间维数，而且有望通过学习过程，针对不同外载荷所对应的优化结构形成工程直觉。文中给出的数值算例验证了所提方法的有效性和优势。

**关键词**：实时优化；拓扑优化；机器学习；移动可变形组件（MMC）

[^abstract-svr-typo]: 原文作 “supported vector regression”，标准术语应为 “support vector regression”；此处按标准术语译为“支持向量回归”。

# 1 引言

结构拓扑优化旨在给定设计域内以最优方式分布一定数量的材料，从而获得优异的结构性能。自 Rozvany [1]、Cheng 和 Olhoff [2]、Bendsøe 和 Kikuchi [3] 以及 Rozvany 和 Zhou [4] 的开创性工作以来，结构拓扑优化受到了日益广泛的研究关注。关于拓扑优化近期发展的前沿综述，请读者参阅文献 [5–8] 及其中所列参考文献。

尽管结构拓扑优化无需预先给定结构形式便具有创造创新结构设计的巨大潜力，但必须指出，拓扑优化问题的求解是一项耗时的任务，尤其是在考虑三维（three-dimensional, 3D）问题时。其原因在于，为了以可接受的分辨率表征材料分布，通常需要使用大量有限元——对于固体各向同性材料惩罚（Solid Isotropic Material with Penalization, SIMP）方法而言——或大量网格节点——对于水平集方法而言；在传统求解框架中尤其如此。这必然会给结构响应计算和数值优化带来巨大的计算开销 [9,10]。

另一方面，众所周知，实现实时拓扑优化是结构工程师追求的终极梦想。所谓实时拓扑优化，是指一旦给定目标函数/约束函数和外载荷，便能够几乎瞬时获得规定设计域内的优化材料分布。可以想象，如果工程师只需在桌面上拖动鼠标，便能几乎立即获得不同载荷工况下相应的优化设计，那将多么令人振奋！然而，对于实际工程问题——通常是大规模三维问题——而言，这是一项极具挑战性的任务，因为即使只考虑单一载荷工况，也会涉及巨大的计算开销。

从数学角度看，实现实时拓扑优化的一种可能途径，是在表征给定外载荷的参数与表征结构几何/拓扑的参数之间建立显式映射。然而，上述映射函数可能非常复杂，例如可能包含非光滑点或不连续点，因而难以通过传统函数逼近技术构造。随着人工智能（artificial intelligence, AI）技术的快速发展，机器学习已经成为一种强有力的工具：它能够通过训练过程，从直接测量或数值计算得到的输入与输出样本数据中提取复杂关系，进而利用所揭示的关系进行预测 [11,12]。事实上，机器学习已经在众多领域获得了成功应用 [13–15]。

近年来，利用机器学习技术求解拓扑优化问题也成为许多研究工作的关注重点。例如，Sosnovik 和 Oseledets [16] 提出了一种深度学习方法，用于加速数值拓扑优化过程。在他们的工作中，采用卷积神经网络（convolutional neural network, CNN）建立数值迭代早期所得中间结果与最终优化结构之间的映射。Gu 等人 [17] 提出利用机器学习设计兼具优异韧性和强度的复合材料结构。他们同样采用 CNN 作为机器学习模型，并证明了机器学习能够利用非常有限的训练数据搜索优化复合材料设计。近期，文献 [18] 又提出了一种数据驱动方法，用于预测变载荷工况下的优化拓扑。该方法将若干指定载荷工况所对应的优化拓扑二值图像作为训练数据，并采用前馈神经网络构造映射，以预测给定载荷条件下的优化拓扑。

尽管上述工作已经清楚地展示了人工智能与拓扑优化相结合的潜在优势，但要将实时拓扑优化这一令人振奋的构想变为现实，仍有一些挑战性问题亟待解决。

第一个问题与机器学习训练过程所涉及的高昂计算成本有关。上述工作均采用基于传统隐式几何描述的 SIMP 方法进行拓扑优化。正如文献 [19] 及后续研究 [20–24] 所深入讨论的，对于高分辨率三维拓扑优化问题，即使只执行一次拓扑优化也可能需要很长的计算时间；而在数据积累阶段，为生成后续模型训练所需的数据，还必须求解一定数量的拓扑优化问题，其计算成本更是不言而喻。

第二个问题来自训练阶段：需要从所得训练数据中提取优化结构的特征。对于大多数机器学习模型而言，该阶段的计算开销高度依赖于设计空间的维数，即设计变量数量。考虑到 SIMP 方法和自由形式水平集方法的设计空间通常具有很高维数，若基于传统隐式方法所得的优化结果进行特征提取，计算需求无疑将极其高昂。

上述基于 SIMP 的机器学习范式还存在另一个缺点：由于采用二值像素/体素图像描述优化结构拓扑，所学习到的优化结构特征知识不可避免地具有网格相关性[^intro-mesh-typo]，而且难以用于建立力学直觉。

[^intro-mesh-typo]: 原文此处作 “mesh-independent（网格无关）”，但这与本段对像素/体素表示的批评、下一段提出的“使所学知识网格无关”这一目标及全文论证均相矛盾；此处按上下文应为 “mesh-dependent（网格相关）”。

本文试图通过建立一种新的求解框架，解决上述机器学习驱动实时拓扑优化面临的挑战。与已有方法相比，所提框架旨在以计算效率更高的方式完成数据积累和模型训练，同时使学习过程获得的知识具有网格无关性，并能够直接启发工程直觉的形成。

为此，本文采用新近发展的基于移动可变形组件（MMC）的显式拓扑优化方法 [19–26]，建立一种适合支撑机器学习驱动实时拓扑优化的新求解框架。采用这一处理方式，是因为 MMC 方法能够利用少量且具有明确物理意义的设计变量，高效求解拓扑优化问题。初步研究表明，所提框架确实具有综合解决上述挑战性问题的潜力。

本文其余部分安排如下。第 2 节介绍在所谓 MMC 框架下进行结构拓扑优化的基本思想及相应的问题列式。第 3 节构建 MMC 框架下实现实时结构拓扑优化的范式，并讨论与其数值实现有关的一些技术问题。第 4 节通过数值算例验证所提范式的有效性。最后，第 5 节给出若干展望性讨论并总结全文。

# 2 基于移动可变形组件（MMC）的拓扑优化

本节简要介绍作为机器学习驱动实时拓扑优化范式基础的 MMC 框架。如文献 [19] 所述，MMC 方法的基本思想是将一组可变形组件作为拓扑优化的基本构件，并通过组件之间的变形、合并和重叠实现结构拓扑变化。在固定有限元网格上数值实现 MMC 方法的一种方式，是引入如下拓扑描述函数（topology description function, TDF）来表示设计域中的材料分布：

$$
\begin{cases}
\phi^s(\boldsymbol{x})>0, & \boldsymbol{x}\in\Omega^s,\\
\phi^s(\boldsymbol{x})=0, & \boldsymbol{x}\in\partial\Omega^s,\\
\phi^s(\boldsymbol{x})<0, & \boldsymbol{x}\in D\setminus\left(\Omega^s\cup\partial\Omega^s\right).
\end{cases}
\tag{1.1}
$$

其中，$D$ 表示给定设计域，$\Omega^s\subset D$ 表示由 $n$ 个实体材料组件构成的区域。实际上，如图 1 所示，由于

$$
\Omega^s=\bigcup_{i=1}^{n}\Omega_i^s,
$$

其中 $\Omega_i^s$ 是第 $i$ 个组件所占据的区域，因而 $\phi^s(\boldsymbol{x})$ 可构造为

$$
\phi^s(\boldsymbol{x})
=\max\left(\phi_1(\boldsymbol{x}),\ldots,\phi_n(\boldsymbol{x})\right),
$$

其中 $\phi_i(\boldsymbol{x})$ 表示第 $i$ 个组件的 TDF。关于如何利用一组物理意义明确的显式几何参数，在二维或三维情形下构造不同轮廓组件的 TDF，更多细节请参阅文献 [19,22,24]。

![[Lei2018_Fig1.png]]

<p align="center">图 1：基于 MMC 的拓扑优化方法示意图：（a）组件的初始布局；（b）优化过程；（c）组件的优化布局。</p>

本文仅考虑二维情形，并采用如下 TDF 描述第 $i$ 个组件的几何形状：

$$
\phi_i(x,y)
=1-\left(\frac{x'}{L_i}\right)^p
-\left(\frac{y'}{b_i(x')}\right)^p,
\tag{1.2}
$$

其中

$$
\begin{bmatrix}
x'\\
y'
\end{bmatrix}
=
\begin{bmatrix}
\cos\theta_i & \sin\theta_i\\
-\sin\theta_i & \cos\theta_i
\end{bmatrix}
\begin{bmatrix}
x-x_{0i}\\
y-y_{0i}
\end{bmatrix}.
\tag{1.3}
$$

$p$ 是一个相对较大的偶整数，本文取 $p=6$。在式 (1.2) 和式 (1.3)[^sec2-eq-ref-typo]中，$L_i$、

$$
b_i(x')
=
\frac{t_i^1+t_i^2-2t_i^3}{2L_i^2}(x')^2
+\frac{t_i^2-t_i^1}{2L_i}x'
+t_i^3,
$$

$(x_{0i},y_{0i})^{\mathrm T}$ 和 $\theta_i$ 分别表示第 $i$ 个组件的半长、二次变化的半厚度函数、中心坐标向量以及倾角。其中，倾角从水平轴开始按逆时针方向度量，具体可参见图 2。

[^sec2-eq-ref-typo]: 原文此处将前文公式写成式 (2.2) 和式 (2.3)，但 PDF 中实际编号为式 (1.2) 和式 (1.3)；此处按实际编号译出。

![[Lei2018_Fig2.png]]

<p align="center">图 2：二维结构组件的几何描述。</p>

这里需要指出，TDF 实际上并不是 MMC 方法不可或缺的组成部分。引入 TDF 只是为了便于在固定网格上实施有限元分析（finite element analysis, FEA）。关于不使用 TDF 实现基于 MMC 的拓扑优化方法，更多讨论请参阅文献 [21,23]。

根据上述描述，MMC 求解框架下的典型拓扑优化问题可表述为

$$
\begin{aligned}
&\text{求}\quad
\boldsymbol{D}
=
\left(
(\boldsymbol{D}^1)^{\mathrm T},
\ldots,
(\boldsymbol{D}^i)^{\mathrm T},
\ldots,
(\boldsymbol{D}^n)^{\mathrm T}
\right)^{\mathrm T},\\
&\text{最小化}\quad I=I(\boldsymbol{D}),\\
&\text{满足}\quad
g_k(\boldsymbol{D})\leq 0,
\qquad k=1,\ldots,m,\\
&\hspace{3.8em}\boldsymbol{D}\in\mathcal{U}_{\boldsymbol{D}}.
\end{aligned}
\tag{1.4}
$$

其中，$I(\boldsymbol{D})$ 是目标函数或目标泛函，$g_k(\boldsymbol{D})$（$k=1,\ldots,m$）是约束函数或约束泛函。在式 (1.4) 中，

$$
\boldsymbol{D}^i
=
\left(
x_{0i},y_{0i},L_i,t_i^1,t_i^2,t_i^3,\theta_i
\right)^{\mathrm T}
\in\mathbb{R}^7,
$$

$\mathcal{U}_{\boldsymbol D}$ 是设计变量向量 $\boldsymbol D$ 所属的容许集。这里将原文设计变量中的 $a_i$ 按全文统一记为半长 $L_i$[^sec2-design-var-typo]。

[^sec2-design-var-typo]: 原文定义 $\boldsymbol D^i$ 时写作 $a_i$，但式 (1.2)、半厚度函数、图 2 以及相关文字均使用 $L_i$ 表示组件半长；此处统一采用 $L_i$。

将与式 (1.4) 中拓扑优化问题有关的给定参数——例如外载荷的位置和大小、边界条件类型以及设计域的几何尺寸——记为

$$
\boldsymbol p\in\mathcal U_{\boldsymbol p},
$$

并将相应的最优解记为

$$
\boldsymbol D^{\mathrm{opt}}
=
\boldsymbol D^{\mathrm{opt}}(\boldsymbol p)
\in
\mathcal O_{\boldsymbol D^{\mathrm{opt}}}
\subset
\mathcal U_{\boldsymbol D}.
$$

机器学习驱动实时拓扑优化的基本思想，就是通过机器学习过程，在 $\mathcal U_{\boldsymbol p}$ 与 $\mathcal O_{\boldsymbol D^{\mathrm{opt}}}$ 之间建立映射

$$
\psi:
\mathcal U_{\boldsymbol p}
\longrightarrow
\mathcal O_{\boldsymbol D^{\mathrm{opt}}},
$$

使得给定 $\boldsymbol p$ 后，几乎能够瞬时得到

$$
\boldsymbol D^{\mathrm{opt}}(\boldsymbol p)
=
\psi(\boldsymbol p).
$$

由于式 (1.4) 中设计空间 $\mathcal U_{\boldsymbol D}$ 的维数远低于传统拓扑优化方法，而且完全不依赖于表征材料分布所采用的网格分辨率，因此可以预期，在所提 MMC 框架下建立机器学习模型将十分高效；这是因为机器学习过程的计算复杂度直接取决于 $\mathcal U_{\boldsymbol D}$ 的维数。

# 3 MMC 求解框架下的机器学习模型

一般而言，机器学习模型的输入根据其特征由一组参数描述，即

$$
\boldsymbol p
=
(p_1,\ldots,p_{n_p})^{\mathrm T},
$$

其中 $n_p$ 表示输入参数的维数。例如，当输入为二维问题中集中载荷的位置时，既可以选择实际坐标

$$
\boldsymbol p=(x_F,y_F)^{\mathrm T},
$$

也可以选择 $p=n_F$，其中 $n_F$ 表示载荷作用节点的编号。

引入机器学习中所谓的广义线性假设后，可以将最优设计变量向量 $\boldsymbol D^{\mathrm{opt}}$ 近似表示为一组特征向量 $\boldsymbol v_1,\ldots,\boldsymbol v_M\in\mathbb R^{7n}$ 的线性组合，即

$$
\boldsymbol D^{\mathrm{opt}}(\boldsymbol p)
\cong
\sum_{i=1}^{M}
w_i(\boldsymbol p)\boldsymbol v_i.
\tag{3.1}
$$

其中，$w_i=w_i(\boldsymbol p)$（$i=1,\ldots,M$）是依赖于 $\boldsymbol p$ 的权重因子；$M$ 是一个给定整数，用于确定表示 $\boldsymbol D^{\mathrm{opt}}$ 时包含的特征向量数量。回顾第 2 节，$n$ 是组件数量，每个组件对应 7 个设计变量。为实现显著降维，通常取 $M\ll 7n$。

假设通过直接优化，在 $K$ 组参数向量

$$
\boldsymbol p_1
=
(p_1^1,\ldots,p_{n_p}^1)^{\mathrm T},
\ldots,
\boldsymbol p_K
=
(p_1^K,\ldots,p_{n_p}^K)^{\mathrm T}
$$

下，获得了 $K$ 个最优设计变量向量

$$
\boldsymbol D_1^{\mathrm{opt}},
\ldots,
\boldsymbol D_K^{\mathrm{opt}}.
$$

通过重采样过程，可将 $(\boldsymbol p_1,\ldots,\boldsymbol p_K)$ 扩展为规模更大的样本集 $(\boldsymbol p_1,\ldots,\boldsymbol p_L)$，其中 $L\gg K$。需要注意，扩展样本集中的两个参数向量 $\boldsymbol p_i$ 和 $\boldsymbol p_j$ 可能相同。

令

$$
\boldsymbol Y^{\mathrm T}
=
\left(
\boldsymbol D_1^{\mathrm{opt}},
\ldots,
\boldsymbol D_L^{\mathrm{opt}}
\right)
\in\mathbb R^{7n\times L},
$$

便可构造 $7n\times7n$ 矩阵 $\boldsymbol Y^{\mathrm T}\boldsymbol Y$。式 (3.1) 中的前 $M$ 个特征向量可通过求解如下特征值问题获得：

$$
\left(
\boldsymbol Y^{\mathrm T}\boldsymbol Y
\right)\boldsymbol v
=
\lambda\boldsymbol v.
\tag{3.2}
$$

这一过程即机器学习中所谓的主成分分析（principal component analysis, PCA）[^sec3-pca-typo]。

[^sec3-pca-typo]: 原文作 “principle component analysis”；标准术语为 “principal component analysis”，此处按标准术语译为“主成分分析”。

随后，求解矩阵方程

$$
\boldsymbol Y^{\mathrm T}
=
\boldsymbol V\boldsymbol W^{\mathrm T},
\tag{3.3}
$$

其中

$$
\boldsymbol V
=
(\boldsymbol v_1,\ldots,\boldsymbol v_M)
\in\mathbb R^{7n\times M},
$$

以及

$$
\boldsymbol W^{\mathrm T}
=
(\boldsymbol w_1,\ldots,\boldsymbol w_L)
\in\mathbb R^{M\times L},
\qquad
\boldsymbol w_i
=
(w_1^i,\ldots,w_M^i)^{\mathrm T}
\in\mathbb R^M,
$$

即可建立如下对应关系：

$$
\boldsymbol p_1
\longrightarrow
\boldsymbol w_1
=
(w_1^1,\ldots,w_M^1)^{\mathrm T},
\ldots,
\boldsymbol p_L
\longrightarrow
\boldsymbol w_L
=
(w_1^L,\ldots,w_M^L)^{\mathrm T}.
\tag{3.4}
$$

获得式 (3.4) 所述数据后，可以采用任意非线性回归方法，在 $\boldsymbol p\in\mathbb R^{n_p}$ 与 $\boldsymbol D^{\mathrm{opt}}\in\mathbb R^{7n}$ 之间建立近似显式映射 $f$。该映射是第 2 节所述

$$
\psi:
\mathcal U_{\boldsymbol p}
\longrightarrow
\mathcal O_{\boldsymbol D^{\mathrm{opt}}}
$$

的近似，可写为

$$
\boldsymbol D^{\mathrm{opt}}=f(\boldsymbol p),
$$

并可用于实现实时拓扑优化。本文采用支持向量回归（SVR）和 K 最近邻（KNN）方法进行非线性回归。上述学习与训练操作均可在离线阶段完成。

这里还需要指出，用 MMC 方法描述材料分布所需的组件数量 $n$，无论在二维还是三维情形下通常约为 $\mathcal O(10^2)$；这远少于 SIMP 方法为获得较高分辨率结构布局所需的像素数量 $m$——对于三维问题，通常约为 $\mathcal O(10^6\text{–}10^7)$。因此，可以预期 MMC 框架下的机器学习过程将比 SIMP 框架下高效得多，因为式 (3.2) 的特征值分析和式 (3.3) 的线性代数方程求解，其计算复杂度均直接取决于相应矩阵的维数。

# 4 数值算例

本节考察图 3a 所示的短梁问题，以说明所提方法的有效性。尺寸为 $2\times1$、厚度为 1 的设计域左端固定，并采用 $200\times100$ 网格进行有限元分析。首先，考虑在设计域右边界施加单位竖向载荷 $\boldsymbol f=\boldsymbol f_1$ 的情形；随后，考虑竖向载荷 $\boldsymbol f=\boldsymbol f_2$ 在图 3a 所示矩形区域内变化的情形。

可用实体材料的体积约束取为

$$
\frac{|\Omega^s|}{|D|}\leq0.4.
$$

实体材料的杨氏模量和泊松比分别取为

$$
E_s=1,\qquad \nu_s=0.3.
$$

![[Lei2018_Fig3a.png]]

<p align="center">图 3a：短梁算例的设计域、边界条件与载荷位置范围。</p>

采用 16 个组件作为 MMC 拓扑优化的基本构件，训练过程中使用的组件初始分布如图 3b 所示。由于每个组件包含 7 个设计变量，设计变量总数为

$$
7\times16=112.
$$

MMC 拓扑优化采用移动渐近线法（method of moving asymptotes, MMA）[29] 求解。

![[Lei2018_Fig3b.png]]

<p align="center">图 3b：16 个组件的初始分布。</p>

首先，将外载荷的竖向位置取为输入参数：

$$
\boldsymbol p=y_f\in[0,1]\subset\mathbb R^1,
\qquad n_p=1.
$$

这里所要实现的实时拓扑优化，是指一旦给定 $y_f$，便能够即时获得结构的优化布局。为此，按照第 3 节所述机器学习流程，建立 $y_f$ 与 $\boldsymbol D^{\mathrm{opt}}\in\mathbb R^{112}$ 之间的映射

$$
\psi:
y_f\in[0,1]\subset\mathbb R^1
\longrightarrow
\boldsymbol D^{\mathrm{opt}}\in\mathbb R^{112}.
$$

具体而言，首先在设计域右边界的 50 个不同竖向位置施加外载荷 $\boldsymbol f_1^i$，并分别进行结构拓扑的直接优化，其中

$$
i=1,\ldots,50,\qquad
K=50,
$$

且载荷位置为

$$
y_f^i=0.01n,
\qquad
n=1,3,5,\ldots,99.
$$

随后，将所得 50 个最优解

$$
\boldsymbol D_1^{\mathrm{opt}}(y_f=0.01),
\boldsymbol D_2^{\mathrm{opt}}(y_f=0.03),
\ldots,
\boldsymbol D_{50}^{\mathrm{opt}}(y_f=0.99)
$$

用作初始样本数据。在均匀重采样假设下，利用 $(\boldsymbol f_1^i,\boldsymbol D_i^{\mathrm{opt}})$（$i=1,\ldots,50$）生成规模为 $L=2000$ 的机器学习重采样数据集，进而构造映射 $\psi$。

一旦获得 $\psi$，便可针对任意 $y_f\in[0,1]$，通过

$$
\boldsymbol D^{\mathrm{opt}}(y_f)
=
\psi(y_f)
$$

即时得到相应的最优解。

表 1–3 比较了所提机器学习流程得到的“优化”构型与 MMC 直接优化所得构型。训练过程采用了不同数量的特征向量，即 $M=10,20,30$，并比较了不同的回归方法。结果表明，所提机器学习方法能够通过学习过程提取优化结构的显著特征，尤其是在 $M$ 取值相对较大时。

<div align="center">

![[Lei2018_Table1.png]]

</div>

<p align="center">表 1：直接优化与机器学习所得结果的比较（<b><i>f</i></b> = <b><i>f</i></b><sub>1</sub>）。</p>

表 1 各组结果依次为：外载荷的竖向坐标；直接优化所得结构及其目标函数值 $c_{\mathrm{obj}}$；采用 $M=20$ 的 SVR 预测结构及其 $c_{\mathrm{obj}}$；采用 $M=20$ 的 KNN 预测结构及其 $c_{\mathrm{obj}}$。

<div align="center">

![[Lei2018_Table2.png]]

</div>

<p align="center">表 2：采用不同特征向量数量得到的结果（<b><i>f</i></b> = <b><i>f</i></b><sub>1</sub>）。</p>

表 2 在相同载荷位置下比较直接优化结果，以及分别采用 $M=10$、$M=20$ 和 $M=30$ 的 SVR 预测结果；每组均给出优化构型及目标函数值 $c_{\mathrm{obj}}$。

还应注意，机器学习流程得到的设计可以作为直接优化的适当初始设计，从而加快收敛。如图 4 所示，以预测设计作为直接优化的初始设计时，只需 20–30 次迭代便可找到优化解。这是当前机器学习流程的另一项优势。

此外还可以看出，对于本文算例，在 MMC 拓扑优化框架下，仅使用 20 个特征向量便能成功提取优化设计的显著特征。相比之下，基于像素图像的方法由于相应设计空间维数很高，很难实现这种低维特征提取。

![[Lei2018_Fig4.png]]

<p align="center">图 4：将机器学习预测结果作为直接优化的初始设计：（a）问题设置；（b）直接优化所得结构，<i>c</i><sub>obj</sub> = 74.61、<i>n</i><sub>iter</sub> = 298；（c）SVR 预测的“优化”结构；（d）以 SVR 预测结果为初始设计进行直接优化所得结构，<i>c</i><sub>obj</sub> = 75.29、<i>n</i><sub>iter</sub> = 23。</p>

表 3 给出了采用 SVR 方法、单位竖向外载荷作用位置在如下二维区域内变化时的结果：

$$
\boldsymbol p
=
(x_f,y_f)^{\mathrm T}
\in
[1.90,2.00]\times[0.27,0.32].
$$

初始样本通过在离散点集

$$
S_{\mathrm{train}}
=
S\setminus S_{\mathrm{test}}
$$

中的各点施加竖向载荷并进行直接优化生成，其中

$$
S=
\left\{
(x,y)\ \middle|\
\begin{aligned}
x&=1.90+0.01n_1, &&n_1=0,1,\ldots,10,\\
y&=0.27+0.01n_2, &&n_2=0,1,\ldots,5
\end{aligned}
\right\},
$$

测试点集为

$$
S_{\mathrm{test}}
=
\left\{
(1.90,0.27),
(1.90,0.31),
(2.00,0.31),
(1.96,0.29)
\right\}.
$$

完整规则点集 $S$ 包含 $11\times6=66$ 个点，去除 4 个测试点后，训练集包含

$$
K=62
$$

个直接优化样本。本算例在训练过程中取

$$
L=500,\qquad M=20.
$$

此时 $n_p=2$。为实现实时拓扑优化，需要建立如下映射：

$$
\psi:
[1.90,2.00]\times[0.27,0.32]
\subset\mathbb R^2
\longrightarrow
\boldsymbol D^{\mathrm{opt}}\in\mathbb R^{112}.
$$

原文在该映射的定义域后误插了集合关系 “$\in[0,1]\subset\mathbb R^2$”，此处按实际二维载荷区域改正[^sec4-domain-typo]。

[^sec4-domain-typo]: 原文写作 $(x_f,y_f)\in[1.90,2.00]\times[0.27,0.32]\in[0,1]\subset\mathbb R^2$，其中二维矩形区域不可能“属于”一维区间 $[0,1]$；正确关系应为该矩形区域是 $\mathbb R^2$ 的子集。

比较结果表明，预测设计保留了直接优化结果中的大多数显著特征。还应注意，机器学习所获得的优化结构知识表现为一组结构组件的布局；这对于形成不同载荷工况下最优结构拓扑的工程直觉十分有帮助。

<div align="center">

![[Lei2018_Table3.png]]

</div>

<p align="center">表 3：直接优化与机器学习所得结果的比较（<b><i>f</i></b> = <b><i>f</i></b><sub>2</sub>）。</p>

表 3 针对 4 个测试载荷坐标，分别给出直接优化构型及其目标函数值 $c_{\mathrm{obj}}$，以及采用 $M=20$ 的 SVR 预测构型及其 $c_{\mathrm{obj}}$。

# 5 结论

本文在 MMC 求解框架下发展了一种机器学习驱动的实时拓扑优化范式。与现有方法相比，所提方法能够降低参数空间维数，显著提高机器学习过程的效率，并使通过学习过程形成工程直觉、进而推测优化结构形态成为可能。文中给出的数值算例验证了所提方法的有效性和优势。

尽管本文采用 MMC 框架建立机器学习范式，但其他基于显式几何描述的求解框架也可以用于实现相同目标，例如文献 [23] 中基于移动可变形孔洞（Moving Morphable Void, MMV）的方法。本文仅通过改变外载荷来研究实时拓扑优化，但所提范式具有足够的通用性，也可涵盖其他变化情形。

此外，许多结构分析问题也可以转化为优化问题，例如将线弹性分析表述为二次规划问题，将单侧约束下的非线性结构分析表述为半定规划问题。因此，所提框架也具有实现实时结构分析的潜力。

还应指出，本文的机器学习过程完全以计算为基础。不过，通过引入能够刻画最优设计独特特征的合理准则，例如 Karush–Kuhn–Tucker（KKT）条件[^sec5-kkt-typo]，有望进一步提高机器学习过程的效率。上述研究方向将在后续工作中继续探索。

[^sec5-kkt-typo]: 原文作 “Karush-Khun-Tucker”，其中 “Khun” 为拼写错误；标准名称为 “Karush–Kuhn–Tucker”。

# 致谢

作者衷心感谢国家重点研发计划（2016YFB0201600、2016YFB0201601、2017YFB0202800、2017YFB0202802）、国家自然科学基金（11732004、11821202、11772026、11772076）、长江学者和创新团队发展计划（PCSIRT）以及高等学校学科创新引智计划（“111 计划”，B14013）的资助。

# 译后检查清单

- [x] 摘要、正文第 1–5 节及致谢均已译毕。
- [x] 式 (1.1)–(1.4) 与式 (3.1)–(3.4) 已对照 PDF 原页核验。
- [x] 表 1–3 与图 1、图 2、图 3a、图 3b、图 4 均已提取、嵌入并配中文图题。
- [x] 原文技术性笔误均已按正确逻辑译出并附译者说明。
- [x] 全篇 Markdown、公式、脚注、链接和图片资产静态检查通过。
- [x] 原阅读笔记及必要关联页面已按全文证据同步。
