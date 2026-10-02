---
title: "翻译：基于混合有限元的不可压缩介质拓扑优化 (Topology optimization of incompressible media using mixed finite elements)"
tags:
  - translation
  - mixed-fem
  - topology-optimization
  - incompressible
status: "done"
date_created: 2026-09-08
date_updated: 2026-09-11
source: "../sources/Bruggi2007-topopt-incompressible-mixed-fem.pdf"
citekey: "Bruggi2007-topologyoptimization"
language: "zh-CN"
---

# Topology Optimization of Incompressible Media Using Mixed Finite Elements

---

# 信息

- **中文标题**：基于混合有限元的不可压缩介质拓扑优化
- **英文标题**：Topology optimization of incompressible media using mixed finite elements
- **作者**：Matteo Bruggi; Paolo Venini
- **作者单位**：帕维亚大学结构力学系（Department of Structural Mechanics, University of Pavia, Via Ferrata 1, I-27100 Pavia, Italy）
- **期刊**：*Computer Methods in Applied Mechanics and Engineering* (CMAME)
- **卷 / 期 / 页码**：Vol. 196, No. 33–34, pp. 3151–3164 (2007)
- **DOI**：[10.1016/j.cma.2007.02.013](https://doi.org/10.1016/j.cma.2007.02.013)
- **收稿 / 修回 / 录用**：Received 15 November 2006; Revised 23 February 2007; Accepted 27 February 2007; Available online 23 May 2007
- **Better BibTeX key**：`Bruggi2007-topologyoptimization`

---

# 摘要

在结构拓扑优化中，不可压缩与近不可压缩材料（如橡胶弹性体、含油多孔介质等）的应用面临着严重的数值自锁困难。当泊松比趋于不可压缩极限（$\nu \to 0.5$）时，传统的基于位移的有限元格式会产生严重的**体积自锁**（Volumetric Locking），导致虚假的极高刚度，进而严重误导材料分布的拓扑演化。为了从物理与变分底层彻底克服这一难题，本文提出了一种基于**二变量真正混合有限元**（Truly-mixed Finite Element Method）的线弹性结构连续介质拓扑优化框架。

该方法采用基于对称应力张量与位移矢量的第二 Hellinger–Reissner 变分原理，引入了满足离散 inf-sup（Babuška–Brezzi）稳定条件的 **Johnson–Mercier (JM)** 复合三角形平衡应力单元。应力场在单元间严格保持法向牵引力连续性，位移场则采用片元分段线性、全局间断的函数逼近。在此变分格式下，当材料趋于不可压缩极限时，柔度双线性型在数学上依然保持一致有界与正定性，完全消除了体积自锁。针对不可压缩介质在低密度空洞区域由体积模量奇异性引发的人工刚度问题，本文提出了两种有效的材料插值松弛方案。数值算例表明：不可压缩材料的最优拓扑构型与经典可压缩材料截然不同；混合有限元格式天然免疫于棋盘格数值不稳定；对于自平衡载荷系统，该方法能够在无需施加多余刚体位移约束的条件下稳定求解。

---

# 1 引言与研究动机 (Introduction and motivation)

拓扑优化自 Bendsøe 与 Kikuchi [2] 开创均质化方法以来，在过去二十年间取得了巨大的发展 [3, 4, 20]。在传统基于密度的拓扑优化（如 SIMP 方法）中，广泛采用纯位移有限元方法（Displacement-based FEM）作为状态方程求解器。然而，在诸多重大工业与工程应用中，需要设计由不可压缩或近不可压缩弹性材料（如天然橡胶、硅胶聚合物、高聚物密封件、软组织仿生结构以及固液两相饱和多孔介质）构成的承载构件。

在线弹性理论中，当材料的泊松比逼近物理极限 $\nu \to 0.5$ 时，第一 Lamé 常数 $\lambda = \frac{E\nu}{(1+\nu)(1-2\nu)} \to \infty$，体积模量 $K \to \infty$。在基于标准位移格式的低阶有限元逼近中，由于有限元位移插值空间的约束过度限制了散度自由场（$\operatorname{div}\mathbf{u} = 0$）的表达能力，系统会出现剧烈的**体积自锁**（Volumetric Locking）现象 [6]。数值刚度被虚假地高估若干数量级，应力场伴随严重的寄生压力振荡，位移响应趋近于零。在拓扑优化循环中，体积自锁会导致伴随灵敏度失真，不仅使优化过程极易陷入虚假的局部极小，而且会导致生成过厚、低效且完全不合理的结构构型。

为了解决这一问题，部分学者尝试采用选择性减缩积分（Selective Reduced Integration, SRI）或平均应变 B-bar 方法；另有学者借鉴不可压缩 Stokes 流动与线弹性问题的数学相似性，利用速度–压力混合格式或流体拓扑优化思想来处理不可压缩结构 [5, 15]。然而，低阶位移–压力混合单元（如 $Q_1-P_0$ 或 $P_1-P_0$）往往不能满足离散 inf-sup 稳定性条件，极易诱发数值压力棋盘格；高阶位移–压力单元则极大增加了拓扑优化的自由度负担。

另一方面，混合有限元方法（Mixed Finite Element Method）为克服上述力学难题提供了本质的变分求解路径 [1, 7]。基于 Hellinger–Reissner 变分原理，将对称应力张量 $\boldsymbol{\sigma}$ 与位移向量 $\mathbf{u}$ 同时作为独立未知量。应力试探函数直接属于对称张量 $H(\operatorname{div}, \Omega)$ 空间，天然保证了跨单元边界法向牵引力（Normal Traction）的严格连续性，且应力与位移的散度平衡方程在弱形式下精确满足。特别地，由于柔度双线性型在不可压缩极限下保持有界，满足离散 inf-sup 条件的混合元能够从根本上免疫体积自锁。

本文的目标是建立一套**真正基于二变量混合有限元**（Truly-mixed FEM，直接以对称应力与位移为求解变量）的不可压缩介质连续体拓扑优化新框架。其核心贡献与特征包括：
1. **采用 Johnson–Mercier (JM) 复合三角形平衡单元** [19]，其在宏观三角形内细分三个子三角形，利用分段线性多项式构造对称且具有连续法向迹的应力场，位移场采用完全不协调的片元分段线性多项式，严格通过了离散 inf-sup 条件；
2. **揭示并明确了混合有限元特有的边界条件施加机制**：与位移法相反，柯西应力边界条件在全局组装刚度矩阵层面以强形式精确施加，而位移约束则在右端项通过对偶积分以弱形式施加；
3. **提出了针对不可压缩介质混合拓扑优化的两相材料插值松弛方案**：克服了在零密度空洞区域因泊松比为 0.5 导致体积模量不消失的人工刚度缺陷；
4. **通过大量数值基准测试**证实：不可压缩介质的最佳拓扑形态与可压缩介质存在根本性差异；混合有限元格式天然消除了棋盘格数值模式；对于无外支座的自平衡载荷系统，混合鞍点格式能够无需任何伪边界约束而自然收敛。

---

# 2 连续问题 (The continuous problem)

## 2.1 连续介质的各向同性弹性问题

设 $\Omega \subset \mathbb{R}^2$ 为具有 Lipschitz 连续边界 $\Gamma = \partial\Omega$ 的开有界单连通域。边界划分为两部分：狄利克雷位移边界 $\Gamma_u$ 与诺依曼应力牵引边界 $\Gamma_t$，满足 $\Gamma = \overline{\Gamma}_u \cup \overline{\Gamma}_t$ 且 $\Gamma_u \cap \Gamma_t = \emptyset$。为了保证结构的刚体位移被有效约束，假设 $\Gamma_u$ 的测度严格大于零（对于自平衡载荷系，该假设可进一步放宽，见第 5 节）。

设 $\boldsymbol{\sigma}$ 和 $\boldsymbol{\tau}$ 分别表示待求与检验的二阶对称应力张量场；$\mathbf{u}$ 和 $\mathbf{v}$ 分别表示待求与检验的位移矢量场；$\mathbb{C}$ 为四阶弹性张量（满足逐点椭圆性与正定对称性）；$\mathbf{g}$ 为平方可积的体力向量场。

在 Hellinger–Reissner 变分框架下，存在两种对偶的变分表述形式。第一种形式采用常规位移与间断应力，其函数空间分别定义为：
$$
\mathbf{V} = \left[ H_0^1(\Omega) \right]^2, \tag{1}
$$
$$
\mathbf{R} = \left\{ \boldsymbol{\tau} : \tau_{ij} \in L^2(\Omega), \, \tau_{ij} = \tau_{ji} \right\}. \tag{2}
$$
对应的变分方程为：寻找 $(\boldsymbol{\sigma}, \mathbf{u}) \in \mathbf{R} \times \mathbf{V}$，使得：
$$
\begin{cases}
\displaystyle \int_\Omega \mathbb{C}^{-1}\boldsymbol{\sigma} : \boldsymbol{\tau} \, \mathrm{d}\Omega - \int_\Omega \boldsymbol{\varepsilon}(\mathbf{u}) : \boldsymbol{\tau} \, \mathrm{d}\Omega = 0, & \forall \boldsymbol{\tau} \in \mathbf{R}, \\
\displaystyle \int_\Omega \boldsymbol{\varepsilon}(\mathbf{v}) : \boldsymbol{\sigma} \, \mathrm{d}\Omega = \int_\Omega \mathbf{g} \cdot \mathbf{v} \, \mathrm{d}\Omega, & \forall \mathbf{v} \in \mathbf{V},
\end{cases} \tag{3}
$$
其中“$:$”表示二阶张量的双缩并（Double Contraction），“$\cdot$”表示向量点积，$\boldsymbol{\varepsilon}(\cdot)$ 为对称微应变算子：
$$
\boldsymbol{\varepsilon}(\mathbf{u}) = \frac{1}{2}\left( \nabla\mathbf{u} + \nabla^\top\mathbf{u} \right) \triangleq \nabla^S \mathbf{u}. \tag{4}
$$

第二种形式（即本文数值实现采用的变分格式）通过利用 Gauss–Green 散度定理，将导数正则性转移至应力场，从而使位移场完全退化为间断函数。引入如下希尔伯特空间：
$$
\mathbf{W} = \left[ L^2(\Omega) \right]^2, \tag{5}
$$
$$
\mathbf{H} = \mathbf{H}(\operatorname{div}, \Omega) = \left\{ \boldsymbol{\tau} : \tau_{ij} = \tau_{ji}, \, \tau_{ij} \in L^2(\Omega), \, \operatorname{div}\boldsymbol{\tau} \in \mathbf{W} \right\}. \tag{6}
$$
由此获得**第二 Hellinger–Reissner 变分格式**：寻找 $(\boldsymbol{\sigma}, \mathbf{u}) \in \mathbf{H} \times \mathbf{W}$，使得：
$$
\begin{cases}
\displaystyle \int_\Omega \mathbb{C}^{-1}\boldsymbol{\sigma} : \boldsymbol{\tau} \, \mathrm{d}\Omega + \int_\Omega \operatorname{div}\boldsymbol{\tau} \cdot \mathbf{u} \, \mathrm{d}\Omega - \int_\Gamma \mathbf{u} \cdot (\boldsymbol{\tau} \cdot \mathbf{n}) \, \mathrm{d}\Gamma = 0, & \forall \boldsymbol{\tau} \in \mathbf{H}(\operatorname{div}, \Omega), \\
\displaystyle \int_\Omega \operatorname{div}\boldsymbol{\sigma} \cdot \mathbf{v} \, \mathrm{d}\Omega = - \int_\Omega \mathbf{g} \cdot \mathbf{v} \, \mathrm{d}\Omega, & \forall \mathbf{v} \in \mathbf{W}(\Omega),
\end{cases} \tag{7}
$$
其中 $\mathbf{n}$ 为边界外法向单位矢量。式 (7) 严格符合混合变分格式的标准抽象框架：略去边界项，寻找 $(\boldsymbol{\sigma}, \mathbf{u}) \in \mathbf{H} \times \mathbf{W}$ 使得：
$$
\begin{cases}
a(\boldsymbol{\sigma}, \boldsymbol{\tau}) + b(\boldsymbol{\tau}, \mathbf{u}) = 0, & \forall \boldsymbol{\tau} \in \mathbf{H}(\operatorname{div}, \Omega), \\
b(\boldsymbol{\sigma}, \mathbf{v}) = - (\mathbf{g}, \mathbf{v}), & \forall \mathbf{v} \in \mathbf{W}(\Omega),
\end{cases} \tag{8}
$$
其中 $(\cdot, \cdot)$ 为 $\mathbf{W}$ 上的标准 $L^2$ 内积，$a(\cdot, \cdot)$ 与 $b(\cdot, \cdot)$ 双线性型定义为：
$$
a(\boldsymbol{\sigma}, \boldsymbol{\tau}) = \int_\Omega \mathbb{C}^{-1}\boldsymbol{\sigma} : \boldsymbol{\tau} \, \mathrm{d}\Omega = \int_\Omega \left( \frac{1}{2\mu} \boldsymbol{\sigma}^D : \boldsymbol{\tau}^D + \frac{1}{2(\lambda+\mu)} \operatorname{tr}(\boldsymbol{\sigma}) \operatorname{tr}(\boldsymbol{\tau}) \right) \mathrm{d}\Omega, \tag{9}
$$
$$
b(\boldsymbol{\tau}, \mathbf{u}) = \int_\Omega \operatorname{div}\boldsymbol{\tau} \cdot \mathbf{u} \, \mathrm{d}\Omega. \tag{10}
$$
在式 (9) 中，上标 $D$ 表示张量的偏量部分（Deviatoric Part），即 $\boldsymbol{\sigma}^D = \boldsymbol{\sigma} - \frac{1}{2}\operatorname{tr}(\boldsymbol{\sigma})\mathbf{I}$；$\operatorname{tr}(\cdot)$ 表示二阶张量的迹；$\lambda$ 和 $\mu$ 为各向同性弹性介质的 Lamé 常数。

> **力学与数学核心注记**：
> 观察双线性型式 (9) 可以得出关于不可压缩介质的至关重要的数学性质：当介质趋于**不可压缩极限**（$\nu \to 0.5 \iff \lambda \to \infty$）时，体积项系数 $\frac{1}{2(\lambda+\mu)} \to 0$。因此，$a(\boldsymbol{\sigma}, \boldsymbol{\tau})$ 非但不会发散，反而稳定地退化为偏应力张量的内积：
> $$
> \lim_{\nu \to 0.5} a(\boldsymbol{\sigma}, \boldsymbol{\tau}) = \int_\Omega \frac{1}{2\mu} \boldsymbol{\sigma}^D : \boldsymbol{\tau}^D \, \mathrm{d}\Omega.
> $$
> 这一特性是混合有限元方法从**连续变分底层彻底免疫体积自锁**的理论根基所在。变分问题式 (8) 的适定性（存在唯一解）由经典 Brezzi 鞍点理论保证，主要依赖于 $b(\cdot, \cdot)$ 在对偶空间满足 inf-sup 条件以及 $a(\cdot, \cdot)$ 在 $b(\cdot, \cdot)$ 的零空间核函数上的椭圆性 [7]。

---

# 3 有限元逼近 (Finite element approximation)

## 3.1 有限元空间

构建满足对称性要求且通过离散 inf-sup 条件的对称张量有限元空间一直是计算力学中的公认难题 [1, 6]。为了离散应力场，本文引入了著名的 **Johnson–Mercier (JM) 复合三角形单元** [19]。该单元是极少数在二维完全混合格式下能够严格通过 inf-sup 条件并保持应力严格对称性的高保真单元之一。

![[Bruggi2007_Fig1.png]]

<center><b>
图 1：细分为三个内部子三角形的 JM 复合三角形有限元网格单元构造。
</b></center>

如图 1 所示，网格中的每个宏观三角形单元 $K$ 进一步由其重心连接三个顶点，剖分为三个内部子三角形 $T_1, T_2, T_3$。由此定义宏观单元上的 Johnson–Mercier 应力空间：
$$
\mathrm{JM}(K) = \left\{ \boldsymbol{\tau} \mid \boldsymbol{\tau} \in \mathbf{H}(\operatorname{div}, K); \, \left. \boldsymbol{\tau} \right|_{T_j} \in \left[ P_1(T_j) \right]_s^4, \, j=1, 2, 3 \right\}, \tag{11}
$$
其中 $P_1(T_j)$ 表示在子三角形 $T_j$ 上的线性多项式空间，下标 $s$ 表示张量对称性。在每个宏观三角形 $K$ 上，JM 应力张量 $\boldsymbol{\tau} \in \mathrm{JM}(K)$ 由如下 **15 个独立自由度** 唯一确定 [19]：
1. **12 个边界应力通量自由度**：在单元 3 条外边 $e_i$（$i=1, 2, 3$）上，以一阶多项式测试法向牵引力通量：
   $$
   \int_{e_i} (\boldsymbol{\tau} \cdot \mathbf{n}) \cdot \mathbf{w} \, \mathrm{d}s, \quad \forall \mathbf{w} \in \left[ P_1(e_i) \right]^2, \, i = 1, 2, 3; \tag{12}
   $$
2. **3 个单元平均应力分量自由度**：在宏观三角形 $K$ 域内对常应力张量求平均积：
   $$
   \int_K \boldsymbol{\tau} : \mathbf{w} \, \mathrm{d}\Omega, \quad \forall \mathbf{w} \in \left[ P_0(K) \right]_s^4. \tag{13}
   $$
由此构成的全局离散对称应力空间为：
$$
\mathbf{H}_h = \left\{ \boldsymbol{\tau}_h \in \mathbf{H}(\operatorname{div}, \Omega) \mid \left. \boldsymbol{\tau}_h \right|_K \in \mathrm{JM}(K), \, \forall K \in \mathcal{T}_h \right\}. \tag{14}
$$

对于位移场，采用单元内分段线性、跨单元全局断开的函数逼近：
$$
\mathbf{W}_h = \left\{ \mathbf{v}_h \in \mathbf{W}(\Omega) \mid \left. \mathbf{v}_h \right|_K \in \left[ P_1(K) \right]^2, \, \forall K \in \mathcal{T}_h \right\}. \tag{15}
$$
离散混合变分方程表述为：寻找 $(\boldsymbol{\sigma}_h, \mathbf{u}_h) \in \mathbf{H}_h \times \mathbf{W}_h$，使得：
$$
\begin{cases}
\displaystyle \int_\Omega \mathbb{C}^{-1}\boldsymbol{\sigma}_h : \boldsymbol{\tau}_h \, \mathrm{d}\Omega + \int_\Omega \operatorname{div}\boldsymbol{\tau}_h \cdot \mathbf{u}_h \, \mathrm{d}\Omega = \int_{\Gamma_u} \mathbf{u}_h \cdot (\boldsymbol{\tau}_h \cdot \mathbf{n}) \, \mathrm{d}\Gamma, & \forall \boldsymbol{\tau}_h \in \mathbf{H}_h, \\
\displaystyle \int_\Omega \operatorname{div}\boldsymbol{\sigma}_h \cdot \mathbf{v}_h \, \mathrm{d}\Omega = - \int_\Omega \mathbf{g} \cdot \mathbf{v}_h \, \mathrm{d}\Omega, & \forall \mathbf{v}_h \in \mathbf{W}_h.
\end{cases} \tag{16}
$$

## 3.2 离散矩阵–向量方程

将离散试探函数与检验函数代入式 (16)，全局有限元总装后导出如下分块不定鞍点代数系统：
$$
\begin{bmatrix}
\mathbf{A}_{rr} & \mathbf{B}_{ru} \\
\mathbf{B}_{ur} & \mathbf{0}
\end{bmatrix}
\begin{bmatrix}
\boldsymbol{\sigma} \\
\mathbf{u}
\end{bmatrix}
=
\begin{bmatrix}
\mathbf{p} \\
\mathbf{g}
\end{bmatrix}, \tag{17}
$$
其中各子矩阵与右端载荷向量的矩阵元具体由以下积分计算：
$$
\begin{aligned}
\mathbf{A}_{rr}(\mathbb{C}^{-1}) &= \int_\Omega \left( \frac{1}{2\mu} \boldsymbol{\sigma}^D : \boldsymbol{\tau}^D + \frac{1}{2(\lambda+\mu)} \operatorname{tr}(\boldsymbol{\sigma}) \operatorname{tr}(\boldsymbol{\tau}) \right) \mathrm{d}\Omega, \\
\mathbf{B}_{ru} &= \int_\Omega \mathbf{u} \cdot \operatorname{div}\boldsymbol{\tau} \, \mathrm{d}\Omega, \quad \mathbf{B}_{ur} = \mathbf{B}_{ru}^\top = \int_\Omega \mathbf{v} \cdot \operatorname{div}\boldsymbol{\sigma} \, \mathrm{d}\Omega, \\
\mathbf{g} &= - \int_\Omega \mathbf{g} \cdot \mathbf{v} \, \mathrm{d}\Omega, \\
\mathbf{p} &= \int_{\Gamma_u} \overline{\mathbf{u}} \cdot (\boldsymbol{\tau} \cdot \mathbf{n}) \, \mathrm{d}\Gamma.
\end{aligned}
$$

### 3.2.1 应力与位移自由度配置

如图 2 所示，JM 复合三角形单元的自由度具体配置如下：
- **应力自由度（圆圈标记，共 15 个）**：
  - 在单元的 3 条边上，取 $1/3$ 和 $2/3$ 处的离散点作为应力通量评估点，每个点具有 2 个法向与切向分量，共 $3 \times 2 \times 2 = 12$ 个自由度；
  - 3 个单元域内平均应力张量分量：$\int_K \sigma_{xx} \, \mathrm{d}\Omega$、$\int_K \sigma_{yy} \, \mathrm{d}\Omega$ 和 $\int_K \sigma_{xy} \, \mathrm{d}\Omega$。
- **位移自由度（正方形标记，共 6 个）**：
  - 在宏观三角形的 3 个顶点处，每个节点具有 2 个位移分量，共 $3 \times 2 = 6$ 个自由度。由于位移场跨单元完全间断，相邻三角形即便共享空间几何顶点，其位移节点也是互相独立的，不参与跨单元组装。

![[Bruggi2007_Fig2.png]]

<center><b>
图 2：单元自由度示意图：应力自由度用圆圈表示（共 15 个），位移自由度用正方形表示（共 6 个）。
</b></center>

### 3.2.2 边界条件的施加机制

在混合有限元框架下施加边界条件与传统位移法存在**本质差异**，这也是深刻理解混合变分原理的关键点：

1. **柯西应力牵引条件（$\boldsymbol{\sigma} \cdot \mathbf{n} = \overline{\mathbf{t}}$）——强形式精确施加**：
   在 JM 单元中，边界法向应力通量 $\boldsymbol{\sigma} \cdot \mathbf{n}$ 本身就是单元的基本节点自由度。因此，在受力边界 $\Gamma_t$ 上，已知的表面牵引力 $\overline{\mathbf{t}}$ 像位移法处理已知位移一样，**在全局组装后的代数矩阵方程 (17) 层面，直接通过对应行和列的操作以强形式精确施加**。
2. **位移边界条件（$\mathbf{u} = \overline{\mathbf{u}}$）——弱形式对偶积分施加**：
   在真正混合格式中，应力是基本未知量，而位移扮演着拉格朗日乘子的角色。根据变分方程 (16) 的第一式，位移边界条件通过代数方程 (17) 右端项中的对偶积分项以**弱形式**施加：
   $$
   \mathbf{p}_u = \int_{\Gamma_u} \overline{\mathbf{u}} \cdot (\boldsymbol{\tau} \cdot \mathbf{n}) \, \mathrm{d}\Gamma.
   $$
3. **齐次位移约束（零位移固支边界 $\overline{\mathbf{u}} = \mathbf{0}$）**：
   当需要在边界上施加固定约束时，对应的弱积分项自然恒等于零（$\mathbf{p}_u = \mathbf{0}$）。这意味着：**在零位移边界处，只要完全不对边界应力通量施加任何外力约束（使其作为纯未知量自由求解），代数系统求解出的对应对偶位移在弱积分意义下将被严格强制为零**。

> **对比本知识库自研工作 [[../../../papers/huzhang-topopt/arbitrary-order-huzhang-topopt-draft-zh|Hu–Zhang 混合元拓扑优化]] §2.3**：
> 在 Hu–Zhang 框架中，为了规避对非齐次边界条件的代数修改，采用了引入提升场 $\boldsymbol{\sigma}_g$ 的完全变分改写路线；而 Bruggi 与 Venini (2007) 的处理方式则是直接在总装矩阵上强置应力通量自由度，并把位移条件通过边界对偶积分送入右端项。

### 3.2.3 混合矩阵–向量方程的求解

矩阵方程 (17) 是典型的大规模**对称不定鞍点系统**。早期文献常采用经典 Uzawa 算法或其不精确变体，但此类迭代法在拓扑优化中严重依赖于人工松弛因子的精细调整，且随密度演化收敛极不稳定。

为此，本文采用高度优化的工业级直接稀疏求解器 **PARDISO** [24, 25]，其专门针对对称不定系统设计了快速 LDL$^\top$ 分解算法。在后文典型的数值测试中，网格包含约 4000 个单元，自由度总数达到约 60,000 个，系数矩阵包含约 100 万个非零元素。在普通工作站上，PARDISO 仅需约 2 秒即可完成矩阵符号与数值分解，后续回代求解耗时几乎可以忽略不计。

---

# 4 不可压缩介质的拓扑优化设计 (Topology optimal design of incompressible media)

## 4.1 预备说明

在基于连续体拓扑优化的经典 SIMP 框架中，如果使用纯位移有限元方法求解不可压缩介质，单元刚度矩阵在全设计域发生不可压缩自锁。算法不仅难以生成清晰的细长受弯构件，而且会导致优化过早停滞于低刚度的局部极小。混合有限元从根本上消除了体积自锁，为高保真不可压缩拓扑设计铺平了道路。

## 4.2 柔顺度格式 (Compliance formulation)

在线弹性结构中，外载荷功等于系统应变能。在混合有限元中，由于总应力是系统的原生主变量，优化问题自然表述为基于**总余能**（Complementary Energy）的最小化列式：
$$
\begin{aligned}
\min_{\boldsymbol{\rho}} \quad & C(\boldsymbol{\rho}) = \boldsymbol{\sigma}^\top \mathbf{A}_{rr}(\boldsymbol{\rho}) \boldsymbol{\sigma} = \int_\Omega \mathbb{C}^{-1}(\boldsymbol{\rho}) \boldsymbol{\sigma} : \boldsymbol{\sigma} \, \mathrm{d}\Omega \\
\text{s.t.} \quad & \begin{bmatrix} \mathbf{A}_{rr}(\boldsymbol{\rho}) & \mathbf{B}_{ru} \\ \mathbf{B}_{ur} & \mathbf{0} \end{bmatrix} \begin{bmatrix} \boldsymbol{\sigma} \\ \mathbf{u} \end{bmatrix} = \begin{bmatrix} \mathbf{p} \\ \mathbf{g} \end{bmatrix}, \\
& \int_\Omega \rho \, \mathrm{d}\Omega \le V^*, \\
& 0 < \rho_{\min} \le \rho \le 1.
\end{aligned} \tag{18}
$$
根据标准伴随法灵敏度分析，由于状态方程满足平衡鞍点条件，柔顺度关于设计变量 $\rho$ 的偏导数具有极具对称性的解析表达：
$$
\frac{\partial C}{\partial \rho} = - \boldsymbol{\sigma}^\top \frac{\partial \mathbf{A}_{rr}(\boldsymbol{\rho})}{\partial \rho} \boldsymbol{\sigma} = - \int_\Omega \frac{\partial \mathbb{C}^{-1}(\boldsymbol{\rho})}{\partial \rho} \boldsymbol{\sigma} : \boldsymbol{\sigma} \, \mathrm{d}\Omega. \tag{19}
$$
式 (19) 展现了混合格式在灵敏度评估中的独特优越性：**灵敏度完全由原状态应力张量二次型直接求得，无需额外求解任何附加的伴随线性方程组**。

## 4.3 混合格式的材料插值特点

### 4.3.1 混合框架下的 SIMP 方法与松弛机制

在传统 SIMP 中，杨氏模量由人工密度幂律插值：$E(\rho) = \rho^t E_0$。然而，对于不可压缩介质，若保持泊松比恒为 $\nu = 0.5$，体积模量为：
$$
K(\rho) = \frac{E(\rho)}{3(1 - 2\nu)} \to \infty. \tag{21}
$$
**当密度趋近于零（$\rho \to 0$）的空洞区域，若 $K$ 仍然保持无限大，空洞介质将被赋予不可压缩的非物理抗体积变形能力！** 这导致空洞域在静水压受力下产生巨大的虚假刚度，破坏了拓扑演化的真实物理传力路径。

![[Bruggi2007_Fig3.png]]

<center><b>
图 3：密度场上的杨氏模量 $E(\rho)$ 与泊松比 $\nu(\rho)$ 插值曲线。(a) 满足式 (22)–(23) 的有理松弛规律；(b) 剪切模量与体积模量独立惩罚规律。
</b></center>

为彻底消除该缺陷，本文提出并对比了两种松弛策略：

#### 方案 1：泊松比有理松弛模型 (Relaxation on Poisson Ratio)

在惩罚杨氏模量 $E(\rho) = \rho^t E_0$ 的同时，对泊松比采用与密度相关的渐进松弛：
$$
\nu(\rho) = \nu_{\min} + \rho^s (\nu_0 - \nu_{\min}), \tag{22}
$$
或采用可控渐近的有理插值形式：
$$
\nu(\rho) = \frac{\nu_{\min} + c_1 \rho^s}{1 + c_2 \rho^s}, \tag{23}
$$
其中当 $\rho = 1$ 时 $\nu = \nu_0 = 0.5$；而在空洞下限 $\rho \to 0$ 时，$\nu$ 松弛至标准可压缩基准值 $\nu_{\min} \approx 0.3$。如图 3 所示，这确保了低密度单元的体积模量同步退化为零。

#### 方案 2：体积模量与剪切模量独立惩罚 (Independent $K$ and $G$ Penalization)

将各向同性应变能直接在体积模量 $K$ 与剪切模量 $G$ 上解耦，分别施加独立的 SIMP 幂律插值：
$$
G(\rho) = \rho^t G_0, \tag{24}
$$
$$
K(\rho) = \rho^s K_0, \quad s > t. \tag{25}
$$
通过选取 $s > t$（例如 $t = 3, s = 6$），使得体积模量在中间密度和低密度区比剪切模量衰减得更快，从而彻底抑制虚假刚度。

### 4.3.2 计算细节与数值滤波

- **优化求解器**：采用移动渐近线法（MMA）[30] 处理多变量非线性规划；
- **节点密度与单元密度映射**：为了降低求解规模并保持连续性，采用节点密度 $\rho_n$ 作为独立优化未知量，各三角形单元的密度 $\rho_e$ 由其 3 个顶点的节点密度算术平均确定；
- **灵敏度过滤**：采用标准权重滤波算子消除高频网格依赖性。

## 4.4 平面应变设计 (Plane strain designs)

必须在力学机理上严格区分平面应变（Plane Strain）与平面应力（Plane Stress）：
- **平面应变**：面外应变严格受限 $\varepsilon_{zz} = 0$。当 $\nu = 0.5$ 时，体积应变 $\operatorname{tr}(\boldsymbol{\varepsilon}) = \varepsilon_{xx} + \varepsilon_{yy} = 0$，材料在面内处于严格的几何不可压缩约束。这是检验体积自锁的最严苛试金石。
- **平面应力**：面外可自由发生泊松收缩，$\varepsilon_{zz} = - \frac{\nu}{1-\nu}(\varepsilon_{xx}+\varepsilon_{yy})$。即便 $\nu = 0.5$，面内位移场也不会产生体积锁死。
因此，后文的数值测试重点聚焦于**平面应变**工况。

---

# 5 数值研究 (Numerical studies)

## 5.1 总体说明与双重验证程序

为了排除局部极小值对拓扑对比的干扰，本节所有算例均执行严格的**双重反向重分析校验**（Double-check Procedure）：
- 将可压缩材料（$\nu = 0.35$ 或 $0.25$）优化得到的拓扑记为构型 A；将不可压缩材料（$\nu = 0.5$）优化得到的拓扑记为构型 B；
- 分别在可压缩和不可压缩两种力学物性下，重新分析构型 A 与构型 B 的真实柔顺度；
- 数据汇总于附录 B 的表 1 至表 8 中。结果无一例外地证实：在不可压缩物性下，构型 B 的柔顺度必然显著优于构型 A，证明新构型是材料不可压缩性驱动出的真实全局最优结构。

## 5.2 单点载荷桥式结构 (算例 1)

如图 4 所示，设计域为长宽比 $2:1$ 的矩形板，下底面两端固定，上表面中心承受竖直向下集中载荷。网格剖分为 $32 \times 32$ 个矩形宏观单元（每个矩形细分为 4 个 JM 三角形，共 4096 个有限元）。

![[Bruggi2007_Fig4.png]]

<center><b>
图 4：算例 1：单点载荷桥式结构的几何域、载荷与约束条件。
</b></center>

![[Bruggi2007_Fig5.png]]

<center><b>
图 5：算例 1：未采用材料松弛时的不可压缩平面应变优化构型（$C=37.1$）及其局部应力集中图。
</b></center>

![[Bruggi2007_Fig6.png]]

<center><b>
图 6：算例 1：采用 $K$ 与 $G$ 独立插值松弛方案后的不可压缩平面应变优化构型（$C=37.7$）。
</b></center>

![[Bruggi2007_Fig7.png]]

<center><b>
图 7：算例 1：经典可压缩材料（$\nu = 0.35$）下的优化构型（$C=43.1$）。
</b></center>

对比图 6 与图 7：
- 可压缩材料（图 7）展现出典型的 Michell 桁架结构，由两根主斜支撑拱组成；
- 不可压缩材料（图 6）呈现出截然不同的结构构型，中心演化出极为坚实的压杆网络，外周环绕闭合的应变能吸收环；
- 若不施加材料松弛（图 5），由于空洞单元的不可压缩性，载荷附近的低密度材料直接吸收了大量虚假静水压能，生成了不切实际的“外挂”虚假传力膜。

## 5.3 两点载荷桥式结构 (算例 2)

第二个算例采用与第一个算例完全相同的几何域，但载荷条件与约束位置略有调整（见图 8）。结构底面两端简支，上表面承受两个对称布置的集中垂直载荷。

![[Bruggi2007_Fig8.png]]

<center><b>
图 8：算例 2：两点载荷桥式结构的几何域、载荷与约束边界。
</b></center>

![[Bruggi2007_Fig9.png]]

<center><b>
图 9：算例 2 优化设计构型对比：上排为平面应变状态（左：$\nu=0.35, C=117.2$；右：$\nu=0.5, C=100.5$）；下排为平面应力状态。
</b></center>

这一特定的边界受载条件非常适合用来深入考察前文所介绍的两种材料插值松弛方案的数值收敛特性：
1. **体积与剪切模量独立 SIMP 插值方案**：数值分析表明，增大惩罚指数 $s$（分析中测试了 $3 \le s \le 12$ 的宽广范围）对最终优化结果几乎没有任何影响，无论是最终拓扑构型还是收敛的柔顺度数值均保持一致稳定；
2. **有理式松弛方案（式 23）**：相比之下，引入数值松弛因子 $m$ 会对较大的松弛程度表现出一定的参数依赖性（$r$ 依赖性）。当松弛参数 $r > 0.01$ 时，柔顺度随之逐渐增加，优化设计逐步退化并越来越接近可压缩工况的最终构型。正如 4.4 节所讨论的插值与松弛特性，两种方案仅在较小的松弛参数 $r$ 下才预期得到完全一致的解。实际上，采用双 SIMP 方案时，最高密度处的泊松比对插值完全不敏感；而在有理松弛方案中，随着 $r$ 的增大，泊松比在较高密度区受到的数值松弛影响逐渐加剧。

此外，图 10 给出了获得图 9 中最终设计构型时算法的收敛历程曲线。该图清楚表明：所分析的四种工况展现出了非常相近的收敛速率，达到最小柔顺度所需的迭代步数大致相当（约 30~40 次迭代即可稳定收敛）。

![[Bruggi2007_Fig10.png]]

<center><b>
图 10：算例 2 算法迭代收敛曲线。
</b></center>

图 9 清晰证明：在平面应变下，不可压缩材料的最优拓扑在两个加载点之间发展出了粗壮的水平承压拱，刚度较可压缩拓扑提升了超过 14%；而在平面应力下，两者的构型几乎完全重合，再次验证了体积约束在平面应变下的主导地位。

## 5.4 支承装置 (算例 3)

本算例研究图 11 所示的几何构型。由于载荷分布与约束布置的特殊性，本问题既可视为经典的桥梁设计问题，更结合材料的不可压缩背景，可视为典型的**支承装置**（Bearing Device，工程中通常由天然或合成橡胶材料制造）拓扑设计问题。本算例的目标是对该矩形域进行优化以将载荷有效传递至地面，同时避免在平面应变不可压缩工况下陷入非物理的虚假构型（文献 [27] 曾对类似算例给出过深入探讨）。

![[Bruggi2007_Fig11.png]]

<center><b>
图 11：算例 3：支承装置的几何域、载荷与支承边界。
</b></center>

图 12（左）展示了采用标准杨氏模量单一 SIMP 幂律插值所获得的最优拓扑。正如 4.4 节所深入剖析的人工刚度缺陷，图 12（右）的 von Mises 应力云图直观地揭示出：未松弛的低密度单元因其体积模量未被有效惩罚为零，直接吸收了外部均布压强，并将该外载荷直接“短路”传递至底面约束边界，从而导致优化程序输出了虚假的极低柔顺度数值（$C=14,616$）。

为彻底规避此类非物理伪构型，本算例采用了式 (24)–(25) 所定义的剪切模量与体积模量独立插值方案。在该特定算例中，为了加速收敛并避免在中等密度区域（而非仅在低密度下界）残留不可压缩性，更有效的做法是在式 (25) 中采用更高的惩罚指数（即取 $s > 6$），或者如文献 [27] 所建议，为满密度基底材料指定较低的初始体积模量基数（即取 $K_{q=1} < 10^{-3} \sim 10^{-4}$）。

![[Bruggi2007_Fig12.png]]

<center><b>
图 12：算例 3：无松弛时不可压缩平面应变优化构型及 von Mises 应力云图。
</b></center>

图 13 完整对比了平面应变（上排）与平面应力（下排）条件下的最优设计：
- **首先关注平面应变设计（图 13 上排）**：
  - 可压缩材料（左上，$\nu=0.35, C=41,940$）展现出典型的**三拱门框架结构**，包含两根分叉中央主立柱以及两侧两根较为细长且倾斜的边立柱；
  - 不可压缩材料（右上，$\nu=0.5, C=39,168$）的柔顺度较可压缩构型优化了约 **10%**，其受力构型发生了本质突变：结构演化为仅由单根粗壮中央主立柱和两侧分叉边立柱构成的**双拱门拓扑**。与可压缩设计相比，该构型表现出由较少数量但截面厚度显著增大的粗实杆件组成。
- **进一步考察平面应力设计（图 13 下排）**：
  - 无论是可压缩材料（左下，$\nu=0.35, C=47,628$）还是不可压缩材料（右下，$\nu=0.5, C=46,656$），二者均统一收敛为具有单根中央立柱的**三拱门框架**。尽管两者在主立柱的分叉细部形态上略有差异，但彼此高度相似，且与前述平面应变下的构型存在极其显著的力学形态差异。

本算例的研究清楚地证实：结构的拓扑优化形态同时受到二维平面假定（平面应变 vs 平面应力）以及材料本身可压缩特性的极其深刻的交互影响。

![[Bruggi2007_Fig13.png]]

<center><b>
图 13：算例 3 优化构型对比：上排为平面应变（左：$\nu=0.35, C=41940$；右：$\nu=0.5, C=39168$）；下排为平面应力。
</b></center>

## 5.5 面内受载板与自平衡系统 (算例 4 与算例 5)

本节数值研究以最后两个算例收尾，这两个算例针对处于**近各向同性应力状态**（Nearly-isotropic Stress Condition）下的平面受载板件。这一特定力学工况驱动最终设计能够极其显著地发挥被优化材料的不可压缩物理潜能。

### 5.5.1 算例 4：四边对称受载自平衡板

首先考虑图 14 所示的面内受载方板。该板件承受一组整体完全自平衡的外载荷系，**完全不需要外加任何接地固定支承约束**。在经典的基于位移的有限元分析中，此类无支承自平衡受力工况会带来极大的数值困难，因为若不人为引入额外的虚假位移约束，刚体位移无法被消除，刚度矩阵将呈奇异状态。而在本文的混合有限元变分框架下，由于状态方程天然具有鞍点结构的自平衡投影特性，无需任何人为辅助边界即可直接稳定求解。

![[Bruggi2007_Fig14.png]]

<center><b>
图 14：算例 4：四边对称受载自平衡板的几何域与载荷设置（利用四分之一对称性求解）。
</b></center>

图 15 给出了利用四分之一对称性求解得到的优化构型对比：
- **平面应变状态（图 15 上排）**：
  - 可压缩材料（左上，$\nu=0.25, C=335.2$）的最优构型由外周封闭环形圈构成，该外环既直接与边界载荷相连，又通过构成刚性三角形的桁架杆件连接，主承力外环内部进一步由细杆组成的子结构予以加劲增强。因此，该结构的显著特征是存在一个连接所有需要最小化位移之载荷作用点的多边形网络；
  - 相反，不可压缩材料（右上，$\nu=0.5, C=240.4$）的核心抗力结构演化为一个极厚的中心正方形框，在节点处或通过连接副框架直接与外载荷相连。值得高度关注的是，该几何形态围绕这一闭合且处于等静应力状态的正方形厚壁展开，极其充分地利用了材料在不可压缩极限下的静水压强化效应，**使得结构的整体刚度提升了 25% 以上（柔顺度降低超过 28%）！**
- **平面应力状态（图 15 下排）**：
  - 可以很容易看出，可压缩（左下，$\nu=0.25, C=325.8$）与不可压缩（右下，$\nu=0.5, C=322.6$）的最优拓扑几乎没有明显差异。两种情况下，主要的中心对称载荷均通过交叉式（十字形）主框架直接相互连接，角部载荷则由较为纤细的辅助杆件连接。

关于算法收敛性，图 16 给出了图 15 最小化求解过程中的柔顺度演化历程曲线：
- 平面应力状态下的两种情况以及平面应变可压缩情况均在 100 次迭代以内实现稳定收敛；
- 而平面应变不可压缩工况展现出了更为迅猛的收敛速率，仅需约 **30 次迭代**即可迅速稳定在最优值。

![[Bruggi2007_Fig16.png]]

<center><b>
图 16：算例 4 柔顺度收敛历史曲线：不可压缩平面应变状态仅需约 30 步即快速收敛。
</b></center>

![[Bruggi2007_Fig15.png]]

<center><b>
图 15：算例 4 优化设计对比：上排平面应变（左：$\nu=0.25, C=335.2$；右：$\nu=0.5, C=240.4$）；下排平面应力。
</b></center>

### 5.5.2 算例 5：多点密集自平衡受载板

面内受载板的第二个算例针对图 17 所示的更密集外载荷分布系统。图 18 分别给出了平面应变下 $\nu=0.25$（左）与 $\nu=0.5$（右）的最优构型。

![[Bruggi2007_Fig17.png]]

<center><b>
图 17：算例 5：多点密集自平衡载荷板的几何域与载荷设置。
</b></center>

![[Bruggi2007_Fig18.png]]

<center><b>
图 18：算例 5 平面应变优化构型对比：左为可压缩（$\nu=0.25, C=756.4$）；右为不可压缩（$\nu=0.5, C=491.0$）。
</b></center>

- 在前一算例中观察到的可压缩材料多边形骨架拓扑，在本算例中由于外载荷施加点数量显著增加而变得更加密集复杂。与之前类似，外圈多边形抗力环由包含更细二级构件的内部网格予以增强；
- 相反，不可压缩材料（$\nu=0.5$）的设计则演化为一圈将所有受载区域紧密连为一体的**极厚外承力环**。这一外环使材料内部完全处于**近各向同性应力状态**，从而在该工况下爆发出不可压缩材料极强的几何刚化效应。数值结果证实，不可压缩设计（$C=491.0$）较可压缩设计（$C=756.4$）实现了**超过 35% 的惊人刚度提升**！

---

# 6 结论与进行中的研究 (Conclusions and ongoing research)

本文建立了一套基于 Johnson–Mercier 复合三角形二变量真正混合有限元的不可压缩介质连续体拓扑优化新方法。
1. **彻底免疫体积自锁**：基于第二 Hellinger–Reissner 变分原理，在连续与离散层面保证了柔度双线性型在不可压缩极限下的良好一致有界性；
2. **揭示边界机制**：系统厘清了混合有限元应力通量强施加与位移对偶弱施加的数学原理，为混合元拓扑优化理论奠定了基础；
3. **消除低密度伪刚度**：提出的泊松比松弛及剪切/体积模量独立惩罚模型，成功克服了不可压缩空洞区域的人工刚度；
4. **天然免疫棋盘格与支持自平衡求解**：混合应力平衡机制从源头消除了位移元中常见的棋盘格杂波，且对无支承自平衡载荷系统展现出了独特的求解鲁棒性。

进行中的工作包括将本混合格式拓展至三维应力约束拓扑优化以及流固耦合压力载荷问题中 [27]。

---

# 致谢 (Acknowledgements)

第一作者衷心感谢丹麦技术大学（DTU）拓扑优化研究组（TopOpt Group），特别感谢 Martin Bendsøe 教授、Ole Sigmund 教授和 Mathias Stolpe 教授在本文多项主题讨论中给予的启发与指导。同时感谢两位匿名审稿人为提升论文质量和清晰度所提出的建设性意见。

---

# 附录 A 棋盘格问题与 JM 格式的收敛性分析

在以单元常应变为代表的低阶位移有限元中，由于单元间应变能量的不连续性，拓扑优化极易出现交替黑白相间的**棋盘格**（Checkerboard Pattern）数值不稳定 [28]。

在本文的混合有限元格式中，应力场 $\boldsymbol{\sigma}_h \in \mathbf{H}(\operatorname{div}, \Omega)$ 在单元界面上被强制要求法向牵引力 $\boldsymbol{\sigma} \cdot \mathbf{n}$ 严格连续。这一跨单元的强力学连续性约束从数学上极大地抑制了高频应力激荡。图 19 明确对比了直接基于单元常密度的 JM 格式与基于位移元的 CST 格式：JM 混合元在完全不依赖任何图像后处理滤波的情况下，优化构型依然保持完全光滑连续、天然无棋盘格。图 20 进一步证明了 JM 格式与位移格式具有完全一致的优良收敛速率。

![[Bruggi2007_Fig19.png]]

<center><b>
图 19：算例 1 构型对比：(左) JM 混合元基于单元常密度；(右) 基于节点密度的 CST 位移元优化结果。
</b></center>

![[Bruggi2007_Fig20.png]]

<center><b>
图 20：算例 1 收敛历程对比曲线：JM 格式与位移基格式展现出相近且稳定的收敛速率。
</b></center>


---

# 附录 B 数值算例收敛双重验证表 (Double-check tables)

本附录汇集了第 5 节所有数值算例的交叉复算数据（表 1 至表 8）。每一行记录了在特定材料设计（可压缩/不可压缩）下获得的最优构型，在两种不同物性下重新分析评估的柔顺度数值 $C$。所有数据均严格满足对角线极小性，证实了收敛解的最优性。

<center><b>
表 1：算例 1 平面应变柔顺度评估
</b></center>

| 设计目标 | 评估物性：$\nu = 0.35$ | 评估物性：$\nu = 0.5$ |
| :--- | :--- | :--- |
| **按 $\nu = 0.35$ 设计** | **43.1** | 38.0 |
| **按 $\nu = 0.5$ 设计** | 43.8 | **37.7** |

<center><b>
表 2：算例 2 平面应变柔顺度评估
</b></center>

| 设计目标 | 评估物性：$\nu = 0.35$ | 评估物性：$\nu = 0.5$ |
| :--- | :--- | :--- |
| **按 $\nu = 0.35$ 设计** | **117.2** | 103.5 |
| **按 $\nu = 0.5$ 设计** | 118.7 | **100.5** |

<center><b>
表 3：算例 2 平面应力柔顺度评估
</b></center>

| 设计目标 | 评估物性：$\nu = 0.35$ | 评估物性：$\nu = 0.5$ |
| :--- | :--- | :--- |
| **按 $\nu = 0.35$ 设计** | **131.8** | 134.0 |
| **按 $\nu = 0.5$ 设计** | 132.1 | **133.7** |

<center><b>
表 4：算例 3 平面应变柔顺度评估
</b></center>

| 设计目标 | 评估物性：$\nu = 0.35$ | 评估物性：$\nu = 0.5$ |
| :--- | :--- | :--- |
| **按 $\nu = 0.35$ 设计** | **41,940** | 40,231 |
| **按 $\nu = 0.5$ 设计** | 48,590 | **39,168** |

<center><b>
表 5：算例 3 平面应力柔顺度评估
</b></center>

| 设计目标 | 评估物性：$\nu = 0.35$ | 评估物性：$\nu = 0.5$ |
| :--- | :--- | :--- |
| **按 $\nu = 0.35$ 设计** | **47,628** | 47,268 |
| **按 $\nu = 0.5$ 设计** | 47,917 | **46,656** |

<center><b>
表 6：算例 4 平面应变柔顺度评估
</b></center>

| 设计目标 | 评估物性：$\nu = 0.25$ | 评估物性：$\nu = 0.5$ |
| :--- | :--- | :--- |
| **按 $\nu = 0.25$ 设计** | **335.2** | 252.6 |
| **按 $\nu = 0.5$ 设计** | 346.9 | **240.4** |

<center><b>
表 7：算例 4 平面应力柔顺度评估
</b></center>

| 设计目标 | 评估物性：$\nu = 0.25$ | 评估物性：$\nu = 0.5$ |
| :--- | :--- | :--- |
| **按 $\nu = 0.25$ 设计** | **325.8** | 323.9 |
| **按 $\nu = 0.5$ 设计** | 329.5 | **322.6** |

<center><b>
表 8：算例 5 平面应变柔顺度评估
</b></center>

| 设计目标 | 评估物性：$\nu = 0.25$ | 评估物性：$\nu = 0.5$ |
| :--- | :--- | :--- |
| **按 $\nu = 0.25$ 设计** | **756.4** | 544.4 |
| **按 $\nu = 0.5$ 设计** | 804.7 | **491.0** |

---

# 参考文献 (References)

[1] D.N. Arnold, F. Brezzi, J.D. Douglas, PEERS: a new mixed finite element for plane elasticity, Japan J. Appl. Math. 1 (1984) 347–367.
[2] M. Bendsøe, N. Kikuchi, Generating optimal topologies in structural design using a homogenization method, Comput. Methods Appl. Mech. Engrg. 71 (2) (1988) 197–224.
[3] M. Bendsøe, O. Sigmund, Material interpolation schemes in topology optimization, Arch. Appl. Mech. 69 (1999) 635–654.
[4] M. Bendsøe, O. Sigmund, Topology Optimization – Theory, Methods and Applications, Springer, New York, 2003.
[5] T. Borrvall, J. Petersson, Topology optimization of fluids in Stokes flow, Int. J. Numer. Methods Engrg. 41 (2003) 77–107.
[6] D. Braess, Finite Elements, Cambridge University Press, 1997.
[7] F. Brezzi, M. Fortin, Mixed and Hybrid Finite Element Methods, Springer-Verlag, New York, 1991.
[8] T.E. Bruns, D.A. Tortorelli, Topology optimization of nonlinear elastic structures and compliant mechanisms, Comput. Methods Appl. Mech. Engrg. 190 (2001) 3443–3459.
[9] T.E. Bruns, O. Sigmund, D.A. Tortorelli, Numerical methods for the topology optimization of structures that exhibit snap-through, Int. J. Numer. Methods Engrg. 55 (2002) 1215–1237.
[10] M. Bruyneel, P. Duysinx, Note on topology optimization of continuum structures including self-weight design, Struct. Multidisc. Optim. 29 (4) (2005) 245–256.
[11] B.-C. Cheng, N. Kikuchi, Topology optimization with design dependent loads, Comput. Methods Appl. Mech. Engrg. 37 (2001) 57–70.
[12] A. Diaz, N. Kikuchi, Solution to shape and topology eigenvalue optimization problems using a homogenization method, Int. J. Numer. Methods Engrg. 35 (3) (1992) 1487–1502.
[13] G. Duvaut, Mécanique de Milieux Continus, Masson, 1992.
[14] P. Duysinx, M. Bendsøe, Topology optimization of continuum structures with local stress constraints, Int. J. Numer. Methods Engrg. 43 (1998) 1453–1478.
[15] A. Gersborg-Hansen, O. Sigmund, R.B. Haber, Topology optimization of channel flow problems, Struct. Multidisc. Optim. 30 (3) (2005) 181–192.
[16] V.B. Hammer, Checkmate? Nodal densities in topology optimization, in: Proc. II Max Planck Workshop on Engineering Design Optimization 2001, Dept. of Mathematics, DTU, Denmark.
[17] V.B. Hammer, N. Olhoff, Topology optimization of continuum structures subjected to pressure loading, Struct. Multidisc. Optim. 19 (2000) 85–92.
[18] W. Han, B.D. Reddy, On the finite element method for mixed variational inequalities arising in elastoplasticity, SIAM J. Numer. Anal. 32 (6) (1995) 1778–1807.
[19] C. Johnson, B. Mercier, Some equilibrium finite elements methods for two dimensional elasticity problems, Numer. Math. 30 (1978) 103–116.
[20] N. Olhoff, H.A. Eschenauer, Topology optimization of continuum structures – a review, Appl. Mech. Rev. 54 (2001) 331–390.
[21] N.L. Pedersen, Maximization of eigenvalues using topology optimization, Struct. Multidisc. Optim. 20 (1) (2001) 2–11.
[22] J. Petersson, Some convergence results in perimeter-controlled topology optimization, Comput. Methods Appl. Mech. Engrg. 171 (1999) 123–140.
[23] S. Schwarz, K. Maute, E. Ramm, Topology and shape optimization for elastoplastic structural response, Comput. Methods Appl. Mech. Engrg. 190 (2001) 2135–2155.
[24] O. Schenk, K. Gärtner, Solving unsymmetric sparse systems of linear equations with PARDISO, J. Future Generation Comput. Syst. 20 (3) (2004) 475–487.
[25] O. Schenk, K. Gärtner, On fast factorization pivoting methods for symmetric indefinite systems, Elec. Trans. Numer. Anal. 23 (2006) 158–179.
[26] O. Sigmund, A new class of extremal composites, J. Mech. Phys. Solids 48 (2) (2000) 397–428.
[27] O. Sigmund, P.M. Clausen, Topology optimization using a mixed formulation: an alternative way to solve pressure load problems, Comput. Methods Appl. Mech. Engrg. 196 (13–16) (2007) 1874–1889.
[28] O. Sigmund, J. Petersson, Numerical instabilities in topology optimization: a survey on procedures dealing with checkerboards, mesh-dependencies and local minima, Struct. Multidisc. Optim. 16 (1) (1998) 68–75.
[29] M. Stolpe, K. Svanberg, An alternative interpolation scheme for minimum compliance optimization, Struct. Multidisc. Optim. 22 (2001) 116–124.
[30] K. Svanberg, Method of moving asymptotes – a new method for structural optimization, Int. J. Numer. Methods Engrg. 24 (3) (1987) 359–373.
[31] G.H. Yoon, J.S. Jensen, O. Sigmund, Topology optimization of acoustic-structure interaction problems using a mixed finite element formulation, Int. J. Numer. Methods Engrg. 70 (9) (2007) 1049–1075.
