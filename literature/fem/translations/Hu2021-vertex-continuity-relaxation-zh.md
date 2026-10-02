---
title: "翻译：Partial relaxation of C0 vertex continuity of stresses of conforming mixed finite elements for the elasticity problem"
tags:
  - translation
  - mixed-fem
  - elasticity
  - vertex-relaxation
  - adaptive-fem
status: "read"
date_created: 2026-09-09
date_updated: 2026-09-22
source: "../sources/Hu2021-vertex-continuity-relaxation.pdf"
citekey: "huPartialRelaxation02021"
language: "zh-CN"
---

# Partial relaxation of $C^0$ vertex continuity of stresses of conforming mixed finite elements for the elasticity problem

---

# 信息

- **中文标题**：弹性问题协调混合有限元应力顶点 $C^0$ 连续性的部分松弛
- **作者**：Jun Hu（胡俊）；Rui Ma（马睿）
- **单位**：北京大学数学科学学院，数学及其应用教育部重点实验室（LMAM and School of Mathematical Sciences, Peking University, Beijing 100871, China）
- **期刊**：*Computational Methods in Applied Mathematics*
- **卷 / 期 / 页码**：21(1): 89–108，2021
- **DOI**：[10.1515/cmam-2020-0003](https://doi.org/10.1515/cmam-2020-0003)
- **本地版本**：[arXiv:1807.08090v2](https://arxiv.org/abs/1807.08090v2)，2019-09-11，22 页。本译文正文依据本地 PDF 全文完整翻译与核对。

# 摘要

针对近期由 Hu 和 Zhang 提出的用于线弹性问题的协调三角形混合有限元，本文通过重组全局自由度对其进行了扩展。具体而言，通过最新顶点二分（newest vertex bisection, NVB）策略由初始网格 $\mathcal{T}_0$ 逐级加密得到的自适应网格序列 $\mathcal{T}_1, \dots, \mathcal{T}_N$ 具备一个关键的分层结构，即网格 $\mathcal{T}_\ell$ 的新增顶点 $x_e$ 是上一级粗网格 $\mathcal{T}_{\ell-1}$ 某条边 $e$ 的中点。本文利用该分层结构，部分松弛了原始单元在 $\mathcal{T}_\ell$ 上的离散应力空间中对称矩阵值函数的顶点 $C^0$ 连续性，进而导出了一个扩展的离散应力空间：对于位于具有单位切向量 $t_e$ 和单位法向量 $n_e = t_e^\perp$ 的粗边 $e$ 上的内顶点 $x_e$，将原始离散应力空间中与顶点 $x_e$ 相关的纯切向分量基函数 $\phi_{x_e}(x) t_e t_e^T$ 沿边 $e$ 分裂为两个基函数 $\phi_{x_e}^+(x) t_e t_e^T$ 与 $\phi_{x_e}^-(x) t_e t_e^T$，其中 $\phi_{x_e}(x)$ 是 $\mathcal{T}_\ell$ 上 $k$ 次（$k$ 等于离散应力的多项式次数）标量 Lagrange 元的节点基函数，$\phi_{x_e}^+(x)$ 和 $\phi_{x_e}^-(x)$ 分别表示其在边 $e$ 两侧的限制。由于其余两个基函数 $\phi_{x_e}(x) n_e n_e^T$ 和 $\phi_{x_e}(x)(n_e t_e^T + t_e n_e^T)$ 与原始离散应力空间中关联于 $x_e$ 的基函数相同，扩展离散应力空间中与节点 $x_e$ 关联的全局基函数个数由原来的 3 个增加为 4 个。其结果是，尽管 $\mathcal{T}_\ell$ 上的扩展离散应力空间仍然是 $\boldsymbol{H}(\mathrm{div})$ 的子空间，但其中离散应力沿粗边 $e$ 的纯切向分量在此类顶点 $x_e$ 处不再被强制要求连续。该扩展离散应力空间的核心特征在于其具有**嵌套性**（nestedness），即粗网格 $\mathcal{T}$ 上的空间是 $\mathcal{T}$ 的任意细化网格 $\widehat{\mathcal{T}}$ 上对应空间的子空间，这使得标准自适应算法的收敛性证明得以严格建立。该思想进一步被推广用于在离散层面上精确施加一般的面力边界条件。数值实验展示了所提方法在均匀网格与自适应网格上的优良性能。

**关键词**：线弹性（linear elasticity）；嵌套混合有限元（nested mixed finite element）；自适应算法（adaptive algorithm）  
**AMS 主题分类**：65N30，74B05

---

# 1 引言

在科学与工程计算中，求解最频繁的问题之一或许就是弹性力学方程组。有限元方法（FEM）最初于 1950 年代被发明用于分析弹性结构的应力。基于 Hellinger-Reissner（H-R）变分原理的混合有限元方法能给出直接的应力逼近，因为该方法将应力和位移同时作为独立变量；相比之下，位移有限元方法仅能给出间接的应力逼近。著名的胡-鹫津（Hu-Washizu）原理的建立者胡海昌先生曾指出，H-R 原理比最小势能原理和最小余能原理更为普遍，且更适合进行数值求解 [20]。事实上，混合有限元对于近不可压缩材料能够完全免除体积自锁（locking），可应用于塑性材料，并且能够更精确地逼近力平衡条件和面力边界条件。然而，应力张量的对称性约束以及混合有限元离散格式的稳定性条件，使得线弹性混合元的设计出奇地困难，长期以来一直被视为一个悬而未决的公开问题 [3]。正如 Arnold 在 2002 年国际数学家大会（ICM）报告中所总结的那样：“从 1960 年代开始，对弹性力学混合有限元长达四十年的搜寻，始终未能在多项式形函数空间中找到任何稳定的对称单元” [Arnold, ICM 2002]。

自 1960 年代以来，许多数学家致力于攻克这一难题，但多数工作妥协于采用弱对称元（weakly symmetric elements）[4, 5, 8] 或复合单元（composite elements）[29]。2002 年，利用弹性微分复形（elasticity complexes），Arnold 与 Winther 在二维三角形网格上构造了首个具有多项式形函数的对称混合有限元族（即 AW 单元）[6]，随后被推广到三维四面体网格 [3]（关于三维一阶单元参见 [1]）以及二维矩形网格 [2]。近期，本文第一作者及其合作者提出了一个设计与分析弹性力学方程组混合有限元的新框架，由此推导出一族具有最优收敛阶的协调对称混合有限元。此外，这些单元非常易于编程实现，因为它们的基函数建立在标量 Lagrange 有限元基函数的基础之上，完全可以手工显式写出。该框架的核心要素包括：在单纯形网格和张量积网格上统一的离散应力空间结构、两个基本代数引理，以及两步稳定性分析方法，详见文献 [21, 22, 24, 25, 26]。

然而，由于对称性约束，上述所有在三角形网格上构建的协调对称混合有限元都对离散应力在内部顶点处强加了 $C^0$ 连续性要求。这种顶点的 $C^0$ 连续性直接导致了有限元空间**嵌套性**（nestedness）的丧失。事实上，设网格 $\widehat{\mathcal{T}}$ 是由粗网格 $\mathcal{T}$ 加密得到的容许细网格，$\widehat{\mathcal{T}}$ 的新增内部顶点 $x_e$ 是 $\mathcal{T}$ 某条粗边 $e$ 的中点，记 $t_e$ 和 $n_e = t_e^\perp$ 分别为边 $e$ 的单位切向量和单位法向量。细网格 $\widehat{\mathcal{T}}$ 上的离散应力空间 $\Sigma(\widehat{\mathcal{T}})$ 中的任何对称矩阵值函数在上述顶点 $x_e$ 处的所有分量都是连续的。然而，对于粗网格 $\mathcal{T}$ 上离散应力空间 $\Sigma(\mathcal{T})$ 中的对称矩阵值函数 $\tau$，其两个法向分量 $n_e^T \tau n_e$ 和 $t_e^T \tau n_e$ 在 $x_e$ 处是连续的，但其纯切向分量 $t_e^T \tau t_e$ 在该点却不必连续。这意味着 $\tau$ 通常不属于细网格空间 $\Sigma(\widehat{\mathcal{T}})$，从而 $\Sigma(\mathcal{T}) \not\subset \Sigma(\widehat{\mathcal{T}})$，即空间不具备嵌套性。

关于混合 Poisson 问题自适应混合有限元方法的收敛性分析，已有大量的理论成果 [7, 10, 14, 17, 23, 28]，文献 [27] 则研究了 Kirchhoff 板弯曲问题。这些已有成果均建立在自适应网格上离散空间具有嵌套性的前提之下。由文献 [1, 3, 6, 21, 22, 24, 25, 26] 中有限元离散应力空间的非嵌套性，导致基于这两族三角形混合单元后验误差估计子 [11, 12, 18] 的自适应算法在数学理论分析上遇到了本质困难。事实上，对于包括混合法在内的非嵌套协调有限元方法标准自适应算法的收敛性分析，文献中唯一的肯定性结论见于文献 [31]，但该文献中的非嵌套性是由一种极其特殊的网格加密策略引起的，而本文所面临的非嵌套性则源于离散应力空间内部函数在顶点处的额外光滑性。文献 [31] 中的技术是否能够推广到当前情形尚不明确。

本文的目的之一，是通过重组全局自由度，对文献 [21, 24] 中由 Hu 和 Zhang 提出的线弹性协调三角形混合有限元进行扩展。所涉及的容许网格序列 $\mathcal{T}_1, \dots, \mathcal{T}_N$ 是通过最新顶点二分（NVB）策略 [30] 由初始网格 $\mathcal{T}_0$ 逐级加密生成的。如前所述，这些网格具有一个关键的分层结构，即网格 $\mathcal{T}_\ell$ 的新增顶点 $x_e$ 是粗网格 $\mathcal{T}_{\ell-1}$ 某条边 $e$ 的中点。本文将利用这一分层结构，部分松弛原始单元在 $\mathcal{T}_\ell$ 上的离散应力空间 $\Sigma(\mathcal{T}_\ell)$ 中对称矩阵值函数的顶点 $C^0$ 连续性，从而得到一个扩展离散应力空间 $\widetilde{\Sigma}(\mathcal{T}_\ell)$。对于位于粗边 $e$（单位切向量为 $t_e$，单位法向量为 $n_e = t_e^\perp$）上的内顶点 $x_e$，设 $\phi_{x_e}(x)$ 为 $\mathcal{T}_\ell$ 上 $k$ 次标量 Lagrange 元的节点基函数（$k$ 等于离散应力的多项式阶数），$\phi_{x_e}^+(x)$ 和 $\phi_{x_e}^-(x)$ 分别表示其在边 $e$ 两侧的限制。扩展 $\Sigma(\mathcal{T}_\ell)$ 的核心思想是：保持对称矩阵值函数 $\tau \in \Sigma(\mathcal{T}_\ell)$ 法向分量 $\tau n_e$ 的连续性，而将纯切向分量 $t_e^T \tau t_e$ 在顶点 $x_e$ 处沿边 $e$ 分裂为两部分。具体实现方式为：将基函数 $\phi_{x_e}(x) t_e t_e^T$ 分裂为两个基函数 $\phi_{x_e}^+(x) t_e t_e^T$ 和 $\phi_{x_e}^-(x) t_e t_e^T$，同时保留关联于顶点 $x_e$ 的另外两个基函数 $\phi_{x_e}(x) n_e n_e^T$ 和 $\phi_{x_e}(x)(n_e t_e^T + t_e n_e^T)$。也就是说，尽管 $\mathcal{T}_\ell$ 上的扩展离散应力空间 $\widetilde{\Sigma}(\mathcal{T}_\ell)$ 仍然是 $\boldsymbol{H}(\mathrm{div})$ 的子空间，但其中离散应力沿粗边 $e$ 的纯切向分量在此类顶点 $x_e$ 处不再必须连续。因此，与扩展离散应力空间节点 $x_e$ 相关的全局基函数数目由原始空间的 3 个增加为 4 个。该扩展离散应力空间的一个关键特性在于其嵌套性，即 $\widetilde{\Sigma}(\mathcal{T}_{\ell-1}) \subset \widetilde{\Sigma}(\mathcal{T}_\ell)$。利用这一嵌套性，本文证明了标准自适应算法的最优收敛性。

本文的另一目的在于在离散层面上施加一般的面力边界条件。所针对的情形为多边形区域 $\Omega$ 的角点 $x_c$ 是两条边界边 $e_1$ 与 $e_2$ 的唯一交点。记 $t_i$ 和 $n_i$ 分别为 $e_i$（$i=1,2$）的单位切向量与外法向量。施加在 $e_1$ 与 $e_2$ 上的通用面力边界条件 $\sigma n_i|_{e_i}$ 可能是**不一致**（不连续）的，即满足 $n_2^T \sigma n_1|_{e_1}(x_c) \neq n_1^T \sigma n_2|_{e_2}(x_c)$。若在角点 $x_c$ 处直接使用原始离散应力空间的顶点自由度，这种不一致性会导致施加该边界条件时遭遇本质困难。事实上，对于文献 [6, 21, 24] 中的所有单元，网格 $\mathcal{T}$ 上的离散应力空间 $\Sigma(\mathcal{T})$ 中的任何 $\tau$ 都恒满足 $n_2^T \tau n_1|_{e_1}(x_c) = n_1^T \tau n_2|_{e_2}(x_c)$。因此，只要 $n_2^T \sigma n_1|_{e_1}(x_c) \neq n_1^T \sigma n_2|_{e_2}(x_c)$，即使 $\sigma n_i|_{e_i}$ 本身是不超过 $k$ 次的多项式，面力边界条件也无法被精确施加。针对此问题，文献 [13] 妥协于采用最小二乘法来获得面力边界条件的某种近似。本文克服这一困难的思想是：将角点处的三角形分割为两个子三角形，然后松弛跨越这两个子三角形公共边的纯切向分量的连续性。这最终在角点处引入了 4 个自由度。由此，原本可能不一致的面力边界条件得以施加；特别是当 $\sigma n_i|_{e_i}$ 是不超过 $k$ 次的多项式时，该边界条件可以被精确施加。在均匀网格和自适应网格上针对 L 形区域基准问题及 Cook 膜问题的数值算例表明，该策略能够显著提高离散应力的计算精度，尤其是在粗网格上，这是因为在粗网格上由非精确边界条件引起的误差往往占据主导地位。

全文通篇中，$L^2(\omega; X)$ 表示在区域 $\omega$ 上定义的值域位于有限维向量空间 $X$ 中的平方可积函数空间。在本文中，$X$ 可以是 $\mathbb{S} := \mathbb{R}_{\mathrm{sym}}^{d \times d}$、$R^d$ 或 $\mathbb{R}$（$d=2,3$）。$H^m(\omega; X)$ 表示 Sobolev 空间，其函数在 $X$ 中取值，且所有不超过 $m$ 阶的广义偏导数均平方可积；$\boldsymbol{H}(\mathrm{div}, \omega; \mathbb{S})$ 表示具有平方可积散度的对称矩阵值函数空间。记 $\|\cdot\|_{m,\omega}$ 为 $H^m(\omega)$ 上的范数，$|\cdot|_{m,\omega}$ 为半范数；$(\cdot, \cdot)_\omega$ 表示区域 $\omega$ 上的标准 $L^2$ 内积，当 $\omega = \Omega$ 时下标通常省略。$\langle \cdot, \cdot \rangle_\Gamma$ 表示边界 $\Gamma$ 上的 $L^2$ 内积。对于标量函数 $\varphi \in H^1(\Omega; \mathbb{R})$ 及向量函数 $v = (v_1, v_2)^T \in H^1(\Omega; \mathbb{R}^2)$，定义
$$
\operatorname{Curl}\varphi := \left(-\frac{\partial\varphi}{\partial x_2}, \frac{\partial\varphi}{\partial x_1}\right), \quad 
\operatorname{Curl}v := \begin{pmatrix} -\frac{\partial v_1}{\partial x_2} & \frac{\partial v_1}{\partial x_1} \\ -\frac{\partial v_2}{\partial x_2} & \frac{\partial v_2}{\partial x_1} \end{pmatrix}.
$$
对于向量函数 $v = (v_1, v_2)^T \in H^1(\Omega; \mathbb{R}^2)$ 及矩阵函数 $\tau = (\tau_{ij})_{2 \times 2}$，定义
$$
\operatorname{curl}v := \frac{\partial v_2}{\partial x_1} - \frac{\partial v_1}{\partial x_2}, \quad 
\operatorname{curl}\tau := \begin{pmatrix} \frac{\partial\tau_{12}}{\partial x_1} - \frac{\partial\tau_{11}}{\partial x_2} \\ \frac{\partial\tau_{22}}{\partial x_1} - \frac{\partial\tau_{21}}{\partial x_2} \end{pmatrix}.
$$
记号 $A \lesssim B$ 表示存在与网格尺寸无关的正常数 $C > 0$ 使得 $A \le CB$。记号 $|\cdot|$ 根据上下文分别表示区域的面积、线段的长度、集合的基数（测度）或实数的绝对值。

本文其余部分安排如下：第 2 节介绍基本记号及三角形网格上的混合有限元方法 [21, 24]，包括其自由度与基函数。第 3 节通过在细化网格新增内节点处部分松弛离散应力的顶点 $C^0$ 连续性，设计自适应网格上的嵌套混合有限元，并严格证明对应自适应算法的最优收敛性。第 4 节在区域 $\Omega$ 的角点处松弛顶点 $C^0$ 连续性，以便精确施加 $\Gamma_N$ 上的不一致面力边界条件，并对三维情形进行讨论。第 5 节汇报数值实验结果。

---

# 2 预备知识

本节介绍线弹性力学问题的应力-位移混合形式以及文献 [21, 24] 中的混合有限元方法。

## 2.1 混合变分形式

设 $\Omega \subset \mathbb{R}^2$ 为具有边界 $\Gamma := \partial\Omega = \Gamma_D \cup \Gamma_N$（$\Gamma_D \cap \Gamma_N = \emptyset$）的单连通有界多边形区域。给定外力体载荷 $f \in V := L^2(\Omega; \mathbb{R}^2)$、Dirichlet 边界位移 $u_D \in H^1(\Omega; \mathbb{R}^2)$ 以及 Neumann 边界面力 $g \in L^2(\Gamma_N; \mathbb{R}^2)$，采用应力-位移混合形式表述的混合边界条件线弹性问题为：求 $(\sigma, u) \in \Sigma_g \times V$ 满足
$$
\begin{cases}
(\mathbb{A}\sigma, \tau) + (\operatorname{div}\tau, u) = \langle u_D, \tau n \rangle_{\Gamma_D}, & \forall \tau \in \Sigma_0, \\
(\operatorname{div}\sigma, v) = (f, v), & \forall v \in V,
\end{cases}
\tag{2.1}
$$
其中测试函数空间定义为
$$
W := \{ v \in H^1(\Omega; \mathbb{R}^2) \mid v|_{\Gamma_D} = 0 \},
$$
$$
\Sigma_g := \{ \sigma \in \boldsymbol{H}(\mathrm{div}, \Omega; \mathbb{S}) \mid \langle \psi, \sigma n \rangle_{\Gamma_N} = \langle \psi, g \rangle_{\Gamma_N}, \; \forall \psi \in W \},
$$
$\Sigma_0 := \Sigma_g|_{g \equiv 0}$，且 $n$ 表示 $\partial\Omega$ 的单位外法向量。表征材料特性的顺度张量（compliance tensor）$\mathbb{A}: \mathbb{S} \to \mathbb{S}$ 对称正定，且其特征值一致有界。对于均匀各向同性材料，顺度张量由下式给出：
$$
\mathbb{A}\tau = \frac{1}{2\mu}\left( \tau - \frac{\lambda}{2\mu + 2\lambda} \operatorname{tr}(\tau) I \right),
$$
其中 $\mu > 0$ 与 $\lambda \ge 0$ 为 Lamé 常数，$I$ 为二阶单位矩阵，$\operatorname{tr}(\tau)$ 为矩阵 $\tau$ 的迹。为叙述简便，本文假设 $\mathbb{A}$ 为常数张量。

## 2.2 三角剖分

设 $\mathcal{T}_0$ 为 $\Omega$ 的初始形状正则三角形剖分，用 $\mathbb{T} := \mathbb{T}(\mathcal{T}_0)$ 表示通过最新顶点二分（NVB）策略 [30] 对 $\mathcal{T}_0$ 进行有限次连续二分剖分得到的所有容许正则三角剖分的集合。给定 $\mathcal{T} \in \mathbb{T}$，记 $\widehat{\mathcal{T}}$ 为 $\mathcal{T}$ 的一个细化网格，并用 $\mathcal{T} \setminus \widehat{\mathcal{T}} := \{ K \in \mathcal{T} \mid K \notin \widehat{\mathcal{T}} \}$ 表示从 $\mathcal{T}$ 到 $\widehat{\mathcal{T}}$ 发生细化的单元集合。记 $h_K := |K|^{1/2}$，网格尺寸 $h = \max_{K \in \widehat{\mathcal{T}}} h_K$。记 $\widehat{\mathcal{E}}$（以及 $\widehat{\mathcal{E}}(\Omega)$ 和 $\widehat{\mathcal{E}}(\Gamma)$）分别为 $\widehat{\mathcal{T}}$ 的所有（以及内部和边界）单元边的集合。对于任意三角形 $K \in \widehat{\mathcal{T}}$，用 $\mathcal{E}(K)$ 表示其所有边的集合。对于任意边 $e \in \widehat{\mathcal{E}}$，记 $t_e$ 为单位切向量，$n_e := t_e^\perp$ 为单位法向量；特别地，若 $e \in \widehat{\mathcal{E}}(\Gamma)$，则 $n_e = n$ 为单位外法向量。函数 $w$ 跨越公共边 $e = K_1 \cap K_2$ 的跳跃算子定义为
$$
[w]_e := (w|_{K_1})|_e - (w|_{K_2})|_e;
$$
特别地，当 $e \in \widehat{\mathcal{E}}(\Gamma)$ 时，约定 $[w]_e := w|_e$。记 $\mathcal{V}(\widehat{\mathcal{T}})$（以及 $\mathcal{V}_0(\widehat{\mathcal{T}})$）为 $\widehat{\mathcal{T}}$ 的所有（以及内部）顶点的集合。NVB 细化算法将每个新生成的顶点 $x_e \in \mathcal{V}(\widehat{\mathcal{T}}) \setminus \mathcal{V}(\mathcal{T}_0)$ 构造为某条边 $e$ 的中点（该边关联切向量 $t_e$ 和法向量 $n_e$）。对于任意内部新节点 $x_e \in \mathcal{V}_0(\widehat{\mathcal{T}}) \setminus \mathcal{V}(\mathcal{T}_0)$，定义两个局部片（patches）$\omega_{x_e}^+$ 与 $\omega_{x_e}^-$ 如下：
$$
\begin{aligned}
\omega_{x_e}^+ &:= \bigcup \{ K \in \widehat{\mathcal{T}} \mid x_e \in K, \; (\operatorname{mid}(K) - x_e) \cdot n_e > 0 \}, \\
\omega_{x_e}^- &:= \bigcup \{ K \in \widehat{\mathcal{T}} \mid x_e \in K, \; (\operatorname{mid}(K) - x_e) \cdot n_e < 0 \}.
\end{aligned}
\tag{2.2}
$$
对于任意整数 $k \ge 0$，记 $P_k(\omega; X)$ 为在区域 $\omega$ 上定义、在有限维向量空间 $X$ 中取值且次数不超过 $k$ 的多项式空间。设 $x_i$（$1 \le i \le 3$）为单元 $K \in \widehat{\mathcal{T}}$ 的三个顶点，$\lambda_i$ 为关于顶点 $x_i$ 的重心坐标，记 $t_{i,j} = x_j - x_i$ 为边 $x_i x_j$ 的切向量。

## 2.3 混合有限元方法

给定单元 $K \in \widehat{\mathcal{T}}$，利用秩为 1 的对称矩阵 $S_{i,j} := t_{i,j} t_{i,j}^T$（$1 \le i < j \le 3$），定义如下空间 [21, 24]：
$$
\Sigma_{k,b}(K) := \sum_{1 \le i < j \le 3} \lambda_i \lambda_j P_{k-2}(K; \mathbb{R}) S_{i,j}.
$$
注意到对于任意函数 $\tau \in \Sigma_{k,b}(K)$ 以及单元 $K$ 的任意边 $e$（外法向量为 $n_e$），法向分量 $\tau n_e|_e$ 恒等于零。这表明 $\Sigma_{k,b}(K)$ 是单元 $K$ 上的 $\boldsymbol{H}(\mathrm{div}, K; \mathbb{S})$ 泡状函数空间（bubble function space）。在 $\widehat{\mathcal{T}}$ 的每个单元上配备此泡状函数空间后，即可在 $\widehat{\mathcal{T}}$ 上定义结构简洁且性质优良的离散应力空间 $\Sigma(\widehat{\mathcal{T}})$，当 $k \ge 3$ 时定义为：
$$
\Sigma(\widehat{\mathcal{T}}) := \{ \sigma \in \boldsymbol{H}(\mathrm{div}, \Omega; \mathbb{S}) \mid \sigma = \sigma_c + \sigma_b, \; \sigma_c \in \boldsymbol{H}^1(\Omega; \mathbb{S}), \; \forall K \in \widehat{\mathcal{T}}, \; \sigma_c|_K \in P_k(K; \mathbb{S}), \; \sigma_b|_K \in \Sigma_{k,b}(K) \}.
\tag{2.3}
$$
需要指出的是，$\sigma_c$ 是对称矩阵值的 $H^1$ Lagrange 有限元函数，即 $\sigma_c$ 的每个分量都是 $\widehat{\mathcal{T}}$ 上的标量 Lagrange 有限元函数。换言之，离散应力空间 $\Sigma(\widehat{\mathcal{T}})$ 是对称矩阵值 $H^1$ Lagrange 有限元空间与上述各单元 $\boldsymbol{H}(\mathrm{div})$ 泡状函数空间之和。单元 $K$ 上的泡状函数空间 $\Sigma_{k,b}(K)$ 在该单元的两步稳定性分析中起着至关重要的作用 [21, 24]。

接下来给出单元 $K$ 上应力形函数空间 $P_k(K; \mathbb{S})$ 的局部自由度。事实上，对称矩阵场 $\tau \in P_k(K; \mathbb{S})$ 可以由以下三组自由度唯一确定（参见图 2.1 中针对 $k=3$ 的实心点与箭头所示）[21]：
1. $\tau$ 在单元三个顶点处的数值；
2. 对于每条边 $e$，$n_e^T \tau n_e$ 与 $t_e^T \tau n_e$ 在边 $e$ 上的最高 $k-2$ 阶矩积分；
3. 对任意 $\xi \in \Sigma_{k,b}(K)$，矩阵内积积分 $\int_K \tau : \xi \,\mathrm{d}x$。

![[Hu2021_Fig2_1.png]]

<center><b>
图 2.1：$k=3$ 时 $\Sigma(\widehat{\mathcal{T}})$ 的局部自由度
</b></center>

为了便于编程实现，下面显式给出 $k=3$ 时 $\Sigma(\widehat{\mathcal{T}})$ 的全局基函数。这需要用到 3 次标量 Lagrange 元的节点基函数，其在单元 $K$ 上的解析表达式为：
$$
\begin{aligned}
\phi_0(x) &= 27\lambda_1 \lambda_2 \lambda_3, \\
\phi_i(x) &= \frac{9}{2}\lambda_i \left(\lambda_i - \frac{1}{3}\right)\left(\lambda_i - \frac{2}{3}\right), \quad i = 1, 2, 3, \\
\phi_{ij}(x) &= \frac{27}{2}\lambda_{i+1} \lambda_{i+2} \left(\lambda_{i+j} - \frac{1}{3}\right), \quad i = 1, 2, 3, \; j = 1, 2.
\end{aligned}
$$

![[Hu2021_Fig2_2.png]]

<center><b>
图 2.2：单元 $K$ 上 3 次 Lagrange 有限元的十个节点基函数
</b></center>

同时还需要对称矩阵空间 $\mathbb{S}$ 的两组基。第一组为 $\mathbb{S}$ 的标准正交基：
$$
S_1 = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}, \quad 
S_2 = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad 
S_3 = \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix}.
\tag{2.4}
$$
第二组基针对各边定义。具体而言，给定单元 $K$ 的边 $e_i$，定义 $S_{e_i} := t_{e_i} t_{e_i}^T$ 以及 $S_{e_i, m}^\perp$（$m=1,2$）满足
$$
S_{e_i, 1}^\perp := n_{e_i} n_{e_i}^T, \quad S_{e_i, 2}^\perp := n_{e_i} t_{e_i}^T + t_{e_i} n_{e_i}^T,
\tag{2.5}
$$
由此易见 $S_{e_i, m}^\perp : S_{e_i} = 0$ 且 $S_{e_i, 1}^\perp : S_{e_i, 2}^\perp = 0$。

于是，关联于单元 $K$ 的离散应力空间全局基函数构造如下：
$$
\begin{aligned}
\theta_{ij} &= \phi_i(x) S_j, \quad i = 0, 1, 2, 3, \; j = 1, 2, 3, \\
\alpha_{ij} &= \phi_{ij}(x)|_K S_{e_i}, \quad i = 1, 2, 3, \; j = 1, 2, \\
\beta_{ijm} &= \phi_{ij}(x) S_{e_i, m}^\perp, \quad i = 1, 2, 3, \; j = 1, 2, \; m = 1, 2.
\end{aligned}
\tag{2.6}
$$
在此，$\phi_{ij}(x)|_K$ 表示 $\phi_{ij}(x)$ 在单元 $K$ 上的限制。注意到基函数 $\alpha_{ij}$ 本身就是一个 $\boldsymbol{H}(\mathrm{div})$ 泡状函数，因为在单元 $K$ 的任意边 $e$ 上都有 $\alpha_{ij} n_e|_e = 0$。此外，若 $e_i$ 是单元 $K$ 与单元 $K'$ 的公共边，则对应于单元 $K'$ 的 $\boldsymbol{H}(\mathrm{div})$ 泡状基函数为 $\alpha'_{ij} = \phi_{ij}(x)|_{K'} S_{e_i}$，它同样是 $\Sigma(\widehat{\mathcal{T}})$ 的基函数且与 $\alpha_{ij}$ 线性无关。特别强调的是，$\Sigma(\widehat{\mathcal{T}})$ 的每一个基函数均可写成标量 Lagrange 元素基函数（或其在某单元上的限制）与对称矩阵空间 $\mathbb{S}$ 的某个基矩阵的张量乘积。

位移空间取完全不连续的 $C^{-1}\text{-}P_{k-1}$ 空间：
$$
V(\widehat{\mathcal{T}}) := \{ v \in L^2(\Omega; \mathbb{R}^2) \mid v|_K \in P_{k-1}(K; \mathbb{R}^2), \; \forall K \in \widehat{\mathcal{T}} \}.
\tag{2.7}
$$
设 $g(\widehat{\mathcal{T}}) := \alpha(\widehat{\mathcal{T}}) n|_{\Gamma_N}$（其中 $\alpha(\widehat{\mathcal{T}}) \in \Sigma(\widehat{\mathcal{T}})$）表示 $g$ 的某种近似。针对式 (2.1) 的混合有限元离散格式为：求 $(\sigma(\widehat{\mathcal{T}}), u(\widehat{\mathcal{T}})) \in \left( \Sigma(\widehat{\mathcal{T}}) \cap \Sigma_{g(\widehat{\mathcal{T}})} \right) \times V(\widehat{\mathcal{T}})$ 满足
$$
\begin{cases}
(\mathbb{A}\sigma(\widehat{\mathcal{T}}), \tau(\widehat{\mathcal{T}})) + (\operatorname{div}\tau(\widehat{\mathcal{T}}), u(\widehat{\mathcal{T}})) = \langle u_D, \tau(\widehat{\mathcal{T}}) n \rangle_{\Gamma_D}, & \forall \tau(\widehat{\mathcal{T}}) \in \Sigma(\widehat{\mathcal{T}}) \cap \Sigma_0, \\
(\operatorname{div}\sigma(\widehat{\mathcal{T}}), v(\widehat{\mathcal{T}})) = (f, v(\widehat{\mathcal{T}})), & \forall v(\widehat{\mathcal{T}}) \in V(\widehat{\mathcal{T}}).
\end{cases}
\tag{2.8}
$$

---

# 3 自适应混合有限元方法

由式 (2.3) 可知，$\Sigma(\widehat{\mathcal{T}})$ 中的函数在所有顶点处均具有 $C^0$ 连续性。正如引言所述，当 $\widehat{\mathcal{T}}$ 是通过 NVB 加密得到的 $\mathcal{T}$ 的容许细化网格时，离散应力空间是非嵌套的，即粗网格空间 $\Sigma(\mathcal{T})$ 并非细网格空间 $\Sigma(\widehat{\mathcal{T}})$ 的子空间。实际上，$\widehat{\mathcal{T}}$ 的新增内部节点 $x_e$ 是 $\mathcal{T}$ 某条粗边 $e$ 的中点，记 $t_e$ 和 $n_e = t_e^\perp$ 分别为其单位切向量和单位法向量。细网格顶点的 $C^0$ 连续性要求 $\Sigma(\widehat{\mathcal{T}})$ 中函数的所有分量在顶点 $x_e$ 处必须整体连续。然而，对于粗网格空间 $\Sigma(\mathcal{T})$ 中的函数 $\tau$，其纯切向分量 $t_e^T \tau t_e$ 在该顶点并不保证连续。因此 $\tau$ 不一定属于细网格空间 $\Sigma(\widehat{\mathcal{T}})$，从而 $\Sigma(\mathcal{T}) \not\subset \Sigma(\widehat{\mathcal{T}})$。在缺乏嵌套性的情况下，直接分析自适应算法的最优收敛性极其困难。在标准自适应算法中，容许网格序列 $\mathcal{T}_1, \dots, \mathcal{T}_N$ 依据后验误差估计子通过 NVB 细化生成 [30]。由于当 $m > \ell$ 时 $\Sigma(\mathcal{T}_\ell)$ 通常不是 $\Sigma(\mathcal{T}_m)$ 的子空间，因而在本质上极难证明拟正交性（quasi-orthogonality），而拟正交性恰恰是自适应有限元算法最优收敛性分析的关键基石 [10, 23]。在已有文献中，尚无由于有限元空间额外光滑性导致非嵌套性的自适应算法收敛性分析。

本节通过松弛 $\Sigma(\widehat{\mathcal{T}})$ 中函数在顶点处的 $C^0$ 连续性，针对 NVB 细化网格构造扩展应力空间 $\widetilde{\Sigma}(\widehat{\mathcal{T}})$。对于自适应算法生成的容许嵌套网格序列 $\mathcal{T}_0, \mathcal{T}_1, \dots, \mathcal{T}_N$，该构造产生一列严格嵌套的离散空间 $\widetilde{\Sigma}(\mathcal{T}_0) \subset \widetilde{\Sigma}(\mathcal{T}_1) \subset \dots \subset \widetilde{\Sigma}(\mathcal{T}_N)$。基于这一嵌套空间族，并采用文献 [23] 的统一分析框架，本文将严格证明自适应算法的最优收敛性。为叙述简洁，本节仅考虑齐次 Dirichlet 边界条件 $\Gamma_D = \Gamma$ 且 $u_D \equiv 0$。

## 3.1 自适应网格上的扩展应力空间

扩展应力空间 $\widetilde{\Sigma}(\widehat{\mathcal{T}})$ 通过重组第 2.3 节中 $\Sigma(\widehat{\mathcal{T}})$ 的顶点全局自由度 (1)，使其具备分层结构。设 $\widehat{\mathcal{T}} \in \mathbb{T}$ 为任意容许网格。回顾任意新增内部节点 $x_e \in \mathcal{V}_0(\widehat{\mathcal{T}}) \setminus \mathcal{V}(\mathcal{T}_0)$（$e$ 为粗网格的一条边，$x_e$ 为其几何中点）对应着以 $x_e$ 为顶点的相邻三角形划分出的两个局部片 $\omega_{x_e}^+$ 与 $\omega_{x_e}^-$。此时，不再强制要求应力张量 $\tau$ 在 $x_e$ 处的所有分量全局连续，而是允许分量 $t_e^T \tau t_e$ 在 $x_e$ 处具有两个不同的极限值：一个在 $\omega_{x_e}^+$ 中，另一个在 $\omega_{x_e}^-$ 中。相应地，关联于顶点 $x_e$ 的基函数被丰富扩充为 4 个基函数：
$$
\phi_{x_e}(x) n_e n_e^T, \quad \phi_{x_e}(x)(n_e t_e^T + t_e n_e^T), \quad \tau_{x_e}^+ := \phi_{x_e}^+(x) t_e t_e^T, \quad \tau_{x_e}^- := \phi_{x_e}^-(x) t_e t_e^T.
\tag{3.1}
$$
其中，当 $x \in \omega_{x_e}^+$ 时 $\phi_{x_e}^+(x) = \phi_{x_e}(x)$，在其余区域恒为零；类似地，$\phi_{x_e}^-(x)$ 为在 $\omega_{x_e}^-$ 上的对应限制。

定义丰富函数空间 $\mathcal{E}(\widehat{\mathcal{T}}) := \operatorname{span}_{x_e \in \mathcal{V}_0(\widehat{\mathcal{T}}) \setminus \mathcal{V}(\mathcal{T}_0)} \{ \tau_{x_e}^+, \tau_{x_e}^- \}$。于是扩展离散应力空间定义为：
$$
\widetilde{\Sigma}(\widehat{\mathcal{T}}) := \Sigma(\widehat{\mathcal{T}}) + \mathcal{E}(\widehat{\mathcal{T}}).
\tag{3.2}
$$
注意到对于任意 $\tau(\widehat{\mathcal{T}}) \in \mathcal{E}(\widehat{\mathcal{T}})$ 及任意内边 $e \in \widehat{\mathcal{E}}(\Omega)$，法向分量 $\tau(\widehat{\mathcal{T}}) n_e$ 跨越 $e$ 都是连续的。这确保了 $\mathcal{E}(\widehat{\mathcal{T}}) \subset \boldsymbol{H}(\mathrm{div}, \Omega; \mathbb{S})$，从而保证了 $\widetilde{\Sigma}(\widehat{\mathcal{T}}) \subset \boldsymbol{H}(\mathrm{div}, \Omega; \mathbb{S})$。

位移场仍由式 (2.7) 中的 $V(\widehat{\mathcal{T}})$ 逼近。针对式 (2.1)（齐次 Dirichlet 条件）的扩展混合有限元格式为：求 $(\sigma(\widehat{\mathcal{T}}), u(\widehat{\mathcal{T}})) \in \widetilde{\Sigma}(\widehat{\mathcal{T}}) \times V(\widehat{\mathcal{T}})$ 满足
$$
\begin{cases}
(\mathbb{A}\sigma(\widehat{\mathcal{T}}), \tau(\widehat{\mathcal{T}})) + (\operatorname{div}\tau(\widehat{\mathcal{T}}), u(\widehat{\mathcal{T}})) = 0, & \forall \tau(\widehat{\mathcal{T}}) \in \widetilde{\Sigma}(\widehat{\mathcal{T}}), \\
(\operatorname{div}\sigma(\widehat{\mathcal{T}}), v(\widehat{\mathcal{T}})) = (f, v(\widehat{\mathcal{T}})), & \forall v(\widehat{\mathcal{T}}) \in V(\widehat{\mathcal{T}}).
\end{cases}
\tag{3.3}
$$
为记号简便，在本节通篇中，记号 $(\sigma(\widehat{\mathcal{T}}), u(\widehat{\mathcal{T}})) \in \widetilde{\Sigma}(\widehat{\mathcal{T}}) \times V(\widehat{\mathcal{T}})$ 均特指扩展离散问题 (3.3) 的解，而非原始问题 (2.8) 的解。

> **定理 3.1（适定性与误差估计）**：当 $k \ge 3$ 时，扩展离散问题 (3.3) 存在唯一解 $(\sigma(\widehat{\mathcal{T}}), u(\widehat{\mathcal{T}})) \in \widetilde{\Sigma}(\widehat{\mathcal{T}}) \times V(\widehat{\mathcal{T}})$，且满足先验误差估计：
> $$
> \|\sigma - \sigma(\widehat{\mathcal{T}})\|_{\boldsymbol{H}(\mathrm{div})} + \|u - u(\widehat{\mathcal{T}})\|_0 \le C h^k (\|\sigma\|_{k+1} + \|u\|_k).
> \tag{3.4}
> $$

*证明*：原始离散问题 (2.8) 的适定性与先验误差估计见文献 [21, 24]。由于 $\operatorname{div}\Sigma(\widehat{\mathcal{T}}) = V(\widehat{\mathcal{T}})$ 且 $\operatorname{div}\mathcal{E}(\widehat{\mathcal{T}}) \subset V(\widehat{\mathcal{T}})$ 蕴含了 $\operatorname{div}\widetilde{\Sigma}(\widehat{\mathcal{T}}) = V(\widehat{\mathcal{T}})$，再结合空间包含关系 $\Sigma(\widehat{\mathcal{T}}) \subset \widetilde{\Sigma}(\widehat{\mathcal{T}})$，直接由混合有限元经典理论（参见例如 [8, Prop. 5.4.1]）即可导出式 (3.3) 的适定性及误差估计式 (3.4)。$\blacksquare$

> **定理 3.2（嵌套性 Nestedness）**：对于任意容许网格 $\mathcal{T} \in \mathbb{T}$ 及其细化网格 $\widehat{\mathcal{T}}$，对应扩展应力空间满足严格嵌套关系：
> $$
> \widetilde{\Sigma}(\mathcal{T}) \subset \widetilde{\Sigma}(\widehat{\mathcal{T}}).
> $$

*证明*：设 $e \in \mathcal{E}(\Omega)$ 为粗网格的一条内部边，其相连的两个三角形为 $K_j \in \mathcal{T}$（$j=1,2$）。对 $e$ 及 $K_j$ 进行二分加密后，在边中点 $x_e := \operatorname{mid}(e) \in \mathcal{V}_0(\widehat{\mathcal{T}}) \setminus \mathcal{V}(\mathcal{T})$ 处引入了 4 个新的全局自由度。对于任意 $\tau(\mathcal{T}) \in \widetilde{\Sigma}(\mathcal{T})$，多项式张量场 $\tau(\mathcal{T})|_{K_j} \in P_k(K_j; \mathbb{S})$ 沿边 $e$ 是连续的，且其法向分量在 $x_e$ 处全局连续。因此，$\tau(\mathcal{T})$ 可以由式 (3.1) 中的基函数以及细网格扩展应力空间 $\widetilde{\Sigma}(\widehat{\mathcal{T}})$ 的其余基函数（例如 $k=3$ 时的式 (2.6)）线性表出。证毕。$\blacksquare$

## 3.2 误差估计子与自适应算法

为建立自适应算法，本文采用文献 [18] 中提出的基于残差的后验误差估计子 $\eta^2(\widehat{\mathcal{T}}) := \sum_{K \in \widehat{\mathcal{T}}} \eta^2(\widehat{\mathcal{T}}, K)$，其中局部估计子定义为：
$$
\eta^2(\widehat{\mathcal{T}}, K) := h_K^4 \|\operatorname{curl}\operatorname{curl}(\mathbb{A}\sigma(\widehat{\mathcal{T}}))\|_{0,K}^2 + \sum_{e \in \mathcal{E}(K)} \left( h_K \|J_{e,1}\|_{0,e}^2 + h_K^3 \|J_{e,2}\|_{0,e}^2 \right),
\tag{3.5}
$$
边的跳跃项分别定义为：
$$
J_{e,1} := \begin{cases}
[(\mathbb{A}\sigma(\widehat{\mathcal{T}}))t_e \cdot t_e]_e, & \text{若 } e \in \widehat{\mathcal{E}}(\Omega), \\
(\mathbb{A}\sigma(\widehat{\mathcal{T}}))t_e \cdot t_e|_e, & \text{若 } e \in \widehat{\mathcal{E}}(\Gamma),
\end{cases}
$$
$$
J_{e,2} := \begin{cases}
[\operatorname{curl}(\mathbb{A}\sigma(\widehat{\mathcal{T}})) \cdot t_e]_e, & \text{若 } e \in \widehat{\mathcal{E}}(\Omega), \\
\left( \operatorname{curl}(\mathbb{A}\sigma(\widehat{\mathcal{T}})) \cdot t_e - \partial_{t_e}((\mathbb{A}\sigma(\widehat{\mathcal{T}}))t_e \cdot n_e) \right)|_e, & \text{若 } e \in \widehat{\mathcal{E}}(\Gamma).
\end{cases}
$$
对于任意单元子集 $\mathcal{M} \subseteq \widehat{\mathcal{T}}$，记 $\eta^2(\widehat{\mathcal{T}}, \mathcal{M}) := \sum_{K \in \mathcal{M}} \eta^2(\widehat{\mathcal{T}}, K)$。设 $Q_{\widehat{\mathcal{T}}}$ 为到位移空间 $V(\widehat{\mathcal{T}})$ 上的 $L^2$ 正交投影算子。数据振荡项（data oscillation）定义为：
$$
\operatorname{osc}^2(f, \mathcal{M}) := \sum_{K \in \mathcal{M}} h_K^2 \|f - Q_{\widehat{\mathcal{T}}} f\|_{0,K}^2.
$$
设 $(\sigma, u)$ 为式 (2.1)（$\Gamma_D = \Gamma$，$u_D \equiv 0$）的精确解，$(\sigma(\widehat{\mathcal{T}}), u(\widehat{\mathcal{T}})) \in \widetilde{\Sigma}(\widehat{\mathcal{T}}) \times V(\widehat{\mathcal{T}})$ 为式 (3.3) 的数值解。在 $L^2(\Omega; \mathbb{S})$ 上定义加权范数 $\|\cdot\|_{\mathbb{A}} := (\mathbb{A}\cdot, \cdot)^{1/2}$。

> **定理 3.3（可靠性与有效性 Reliability and Efficiency）**：存在仅依赖于 $\widehat{\mathcal{T}}$ 形状正则性的正常数 $C_{\mathrm{Rel}}$ 与 $C_{\mathrm{Eff}}$，使得
> $$
> \|\sigma - \sigma(\widehat{\mathcal{T}})\|_{\mathbb{A}}^2 \le C_{\mathrm{Rel}} \left( \eta^2(\widehat{\mathcal{T}}) + \operatorname{osc}^2(f, \widehat{\mathcal{T}}) \right) \quad \text{（可靠性）},
> \tag{3.6}
> $$
> $$
> \eta^2(\widehat{\mathcal{T}}) \le C_{\mathrm{Eff}} \|\sigma - \sigma(\widehat{\mathcal{T}})\|_{\mathbb{A}}^2 \quad \text{（有效性）}.
> \tag{3.7}
> $$

*证明*：文献 [18] 已经对第 2.3 节中混合有限元原始空间的误差估计子可靠性与有效性给出了证明。注意到扩展应力空间 $\widetilde{\Sigma}(\widehat{\mathcal{T}})$ 与原始应力空间 $\Sigma(\widehat{\mathcal{T}})$ 仅在顶点自由度上存在差异。因此，采用与文献 [18, Thm. 3.1] 完全类似的论证可证可靠性 (3.6)，而采用与文献 [18, Thm. 3.2] 完全类似的论证可证有效性 (3.7)。详细细节在此略去。此外，下文定理 3.9 中的离散可靠性亦可直接推导得出可靠性。$\blacksquare$

设 $\widetilde{\Sigma}(\mathcal{T}_\ell)$ 和 $V(\mathcal{T}_\ell)$ 分别表示自适应网格 $\mathcal{T}_\ell$ 上的对应空间（$\ell \in \mathbb{N}_0$）。自适应算法描述如下：

```
算法：嵌套混合有限元自适应算法 (AFEM Loop)
输入：标记参数 0 < θ < 1，初始三角网格 T_0。置 ℓ := 0。
1. SOLVE：在 T_ℓ 上求解离散问题 (3.3)，得到数值解 (σ(T_ℓ), u(T_ℓ)) ∈ \widetilde{Σ}(T_ℓ) × V(T_ℓ)。
2. ESTIMATE：根据式 (3.5) 计算后验误差估计子 η^2(T_ℓ)。
3. MARK：选取具有（近似）最小基数的标记单元子集 M_ℓ ⊂ T_ℓ，使得 Dörfler 标记条件成立：
   θ ( η^2(T_ℓ) + osc^2(f, T_ℓ) ) ≤ η^2(T_ℓ, M_ℓ) + osc^2(f, M_ℓ)。
4. REFINE：通过 NVB 细化 M_ℓ 中的每个三角形 K，生成新网格 T_{ℓ+1}。
5. 置 ℓ := ℓ + 1，转至步骤 1。
```

## 3.3 最优收敛性

由于采用了基于残差的估计子，最优性分析的核心任务是严格证明**拟正交性**（quasi-orthogonality）和**离散可靠性**（discrete reliability）。

设 $(\sigma(\mathcal{T}), u(\mathcal{T})) \in \widetilde{\Sigma}(\mathcal{T}) \times V(\mathcal{T})$ 与 $(\sigma(\widehat{\mathcal{T}}), u(\widehat{\mathcal{T}})) \in \widetilde{\Sigma}(\widehat{\mathcal{T}}) \times V(\widehat{\mathcal{T}})$ 分别为式 (3.3) 在网格 $\mathcal{T}$ 及其细化网格 $\widehat{\mathcal{T}}$ 上的离散解。记 $Q_{\mathcal{T}}$（以及 $Q_{\widehat{\mathcal{T}}}$）为到 $V(\mathcal{T})$（以及 $V(\widehat{\mathcal{T}})$）上的 $L^2$ 投影算子。为分析拟正交性与离散可靠性，引入辅助中间解 $(\widehat{\sigma}(\widehat{\mathcal{T}}), \widehat{u}(\widehat{\mathcal{T}})) \in \widetilde{\Sigma}(\widehat{\mathcal{T}}) \times V(\widehat{\mathcal{T}})$，其满足：
$$
\begin{cases}
(\mathbb{A}\widehat{\sigma}(\widehat{\mathcal{T}}), \tau(\widehat{\mathcal{T}})) + (\operatorname{div}\tau(\widehat{\mathcal{T}}), \widehat{u}(\widehat{\mathcal{T}})) = 0, & \forall \tau(\widehat{\mathcal{T}}) \in \widetilde{\Sigma}(\widehat{\mathcal{T}}), \\
(\operatorname{div}\widehat{\sigma}(\widehat{\mathcal{T}}), v(\widehat{\mathcal{T}})) = (Q_{\mathcal{T}} f, v(\widehat{\mathcal{T}})), & \forall v(\widehat{\mathcal{T}}) \in V(\widehat{\mathcal{T}}).
\end{cases}
\tag{3.8}
$$

> **引理 3.4**：设 $(\sigma(\widehat{\mathcal{T}}), u(\widehat{\mathcal{T}}))$ 为式 (3.3) 的解，$(\widehat{\sigma}(\widehat{\mathcal{T}}), \widehat{u}(\widehat{\mathcal{T}}))$ 为式 (3.8) 的解。则有
> $$
> \|\sigma(\widehat{\mathcal{T}}) - \widehat{\sigma}(\widehat{\mathcal{T}})\|_{\mathbb{A}} \lesssim \operatorname{osc}(f, \mathcal{T} \setminus \widehat{\mathcal{T}}).
> $$

*证明*：对于任意 $f \in L^2(\Omega; \mathbb{R}^2)$，将线弹性混合变分问题 (2.1)（$\Gamma_D = \Gamma$，$u_D \equiv 0$）简记为算子方程 $\mathcal{L}(\sigma, u) = f$。令 $(\xi, z) = \mathcal{L}^{-1}(1 - Q_{\mathcal{T}})Q_{\widehat{\mathcal{T}}} f$。由文献 [18, Lemma 3.1] 的先验稳定性结果可知：
$$
\|\xi\|_{\mathbb{A}} \lesssim \operatorname{osc}(Q_{\widehat{\mathcal{T}}} f, \mathcal{T}) = \operatorname{osc}(Q_{\widehat{\mathcal{T}}} f, \mathcal{T} \setminus \widehat{\mathcal{T}}).
\tag{3.9}
$$
注意到 $(\sigma(\widehat{\mathcal{T}}) - \widehat{\sigma}(\widehat{\mathcal{T}}), u(\widehat{\mathcal{T}}) - \widehat{u}(\widehat{\mathcal{T}}))$ 正是 $(\xi, z)$ 在网格 $\widehat{\mathcal{T}}$ 上的混合有限元逼近解。根据最佳 $L^2$ 逼近性质 [8]：
$$
\|\xi - (\sigma(\widehat{\mathcal{T}}) - \widehat{\sigma}(\widehat{\mathcal{T}}))\|_{\mathbb{A}} \lesssim \inf_{\tau(\widehat{\mathcal{T}}) \in \widetilde{\Sigma}(\widehat{\mathcal{T}})} \|\xi - \tau(\widehat{\mathcal{T}})\|_{\mathbb{A}} \le \|\xi\|_{\mathbb{A}}.
$$
结合式 (3.9) 及三角不等式即完成证明。$\blacksquare$

> **定理 3.5（拟正交性 Quasi-orthogonality）**：对于任意 $0 < \delta < 1$，存在常数 $C_0 > 0$，使得
> $$
> (1 - \delta)\|\sigma - \sigma(\widehat{\mathcal{T}})\|_{\mathbb{A}}^2 \le \|\sigma - \sigma(\mathcal{T})\|_{\mathbb{A}}^2 - \|\sigma(\widehat{\mathcal{T}}) - \sigma(\mathcal{T})\|_{\mathbb{A}}^2 + \frac{C_0}{\delta}\operatorname{osc}^2(f, \mathcal{T} \setminus \widehat{\mathcal{T}}).
> $$

*证明*：回顾式 (3.8) 中的 $\widehat{\sigma}(\widehat{\mathcal{T}})$。由于 $\operatorname{div}(\widehat{\sigma}(\widehat{\mathcal{T}}) - \sigma(\mathcal{T})) = 0$，在式 (3.3) 中选取测试函数 $\tau(\widehat{\mathcal{T}}) = \widehat{\sigma}(\widehat{\mathcal{T}}) - \sigma(\mathcal{T}) \in \widetilde{\Sigma}(\widehat{\mathcal{T}})$，可得：
$$
\begin{aligned}
(\mathbb{A}(\sigma - \sigma(\widehat{\mathcal{T}})), \sigma(\widehat{\mathcal{T}}) - \sigma(\mathcal{T})) &= (\mathbb{A}(\sigma - \sigma(\widehat{\mathcal{T}})), \sigma(\widehat{\mathcal{T}}) - \widehat{\sigma}(\widehat{\mathcal{T}}) + \widehat{\sigma}(\widehat{\mathcal{T}}) - \sigma(\mathcal{T})) \\
&= (\mathbb{A}(\sigma - \sigma(\widehat{\mathcal{T}})), \sigma(\widehat{\mathcal{T}}) - \widehat{\sigma}(\widehat{\mathcal{T}})).
\end{aligned}
$$
结合引理 3.4，存在常数 $C_0 > 0$ 满足：
$$
(\mathbb{A}(\sigma - \sigma(\widehat{\mathcal{T}})), \sigma(\widehat{\mathcal{T}}) - \sigma(\mathcal{T})) \le \sqrt{C_0} \|\sigma - \sigma(\widehat{\mathcal{T}})\|_{\mathbb{A}} \operatorname{osc}(f, \mathcal{T} \setminus \widehat{\mathcal{T}}).
$$
再由代数恒等式 $\|\sigma - \sigma(\mathcal{T})\|_{\mathbb{A}}^2 = \|\sigma - \sigma(\widehat{\mathcal{T}})\|_{\mathbb{A}}^2 + \|\sigma(\widehat{\mathcal{T}}) - \sigma(\mathcal{T})\|_{\mathbb{A}}^2 + 2(\mathbb{A}(\sigma - \sigma(\widehat{\mathcal{T}})), \sigma(\widehat{\mathcal{T}}) - \sigma(\mathcal{T}))$ 及 Young 不等式即可完成证明。$\blacksquare$

离散可靠性的分析需要借助某种 $H^2(\Omega)$ 协调有限元空间。回顾式 (2.2) 中的子区域 $\omega_{x_e}^+$ 与 $\omega_{x_e}^-$。文献 [15] 中针对 $k \ge 3$ 构造的逼近 $H^2(\Omega)$ 的 $H^2$ 协调有限元空间 $S^{k+2}(\widehat{\mathcal{T}})$，通过在顶点附近进行修正扩展了高阶 Argyris 单元空间，其定义为：
$$
\begin{aligned}
S^{k+2}(\widehat{\mathcal{T}}) := \{ \varphi \in L^2(\Omega) \mid &\forall K \in \widehat{\mathcal{T}}, \; \varphi|_K \in P_{k+2}(K; \mathbb{R}); \; \varphi \text{ 与 } \nabla\varphi \text{ 在所有顶点处连续}; \\
&\nabla\varphi \text{ 跨越所有内部边连续}; \; \nabla^2\varphi \text{ 在每个初始顶点 } x \in \mathcal{V}(\mathcal{T}_0) \\
&\text{及每个边界顶点 } x \in \mathcal{V}(\widehat{\mathcal{T}}) \setminus \mathcal{V}_0(\widehat{\mathcal{T}}) \text{ 处连续}; \\
&n_e^T \nabla^2\varphi t_e \text{ 与 } t_e^T \nabla^2\varphi t_e \text{ 在每个内部节点 } x_e \in \mathcal{V}_0(\widehat{\mathcal{T}}) \setminus \mathcal{V}(\mathcal{T}_0) \text{ 处连续}; \\
&n_e^T \nabla^2\varphi n_e \text{ 在 } \omega_{x_e}^+ \text{ 和 } \omega_{x_e}^- \text{ 内部趋于 } x_e \text{ 时分别连续} \}.
\end{aligned}
\tag{3.10}
$$
与标准高阶 Argyris 元中的函数不同，函数 $\varphi(\widehat{\mathcal{T}}) \in S^{k+2}(\widehat{\mathcal{T}})$ 的二阶偏导数分量 $n_e^T \nabla^2\varphi(\widehat{\mathcal{T}}) n_e$ 在所有内部新增顶点 $x_e \in \mathcal{V}_0(\widehat{\mathcal{T}}) \setminus \mathcal{V}(\mathcal{T}_0)$ 处并不要求整体连续。

> **引理 3.6（离散 Helmholtz 分解）**：对于任意满足 $\operatorname{div}\tau(\widehat{\mathcal{T}}) = 0$ 的 $\tau(\widehat{\mathcal{T}}) \in \widetilde{\Sigma}(\widehat{\mathcal{T}})$，存在 $\varphi(\widehat{\mathcal{T}}) \in S^{k+2}(\widehat{\mathcal{T}})$ 使得 $\tau(\widehat{\mathcal{T}}) = \operatorname{Curl}\operatorname{Curl}\varphi(\widehat{\mathcal{T}})$。

*证明*：通过计算空间维数来证明。记 $K_{\widehat{\mathcal{T}}}(\mathrm{div}) := \{ \tau(\widehat{\mathcal{T}}) \in \widetilde{\Sigma}(\widehat{\mathcal{T}}) \mid \operatorname{div}\tau(\widehat{\mathcal{T}}) = 0 \}$ 为 $\widetilde{\Sigma}(\widehat{\mathcal{T}})$ 的离散散度核空间。易见 $\operatorname{Curl}\operatorname{Curl} S^{k+2}(\widehat{\mathcal{T}}) \subseteq K_{\widehat{\mathcal{T}}}(\mathrm{div})$。空间 $K_{\widehat{\mathcal{T}}}(\mathrm{div})$ 的维数等于 $\widetilde{\Sigma}(\widehat{\mathcal{T}})$ 的维数减去 $V(\widehat{\mathcal{T}})$ 的维数，即
$$
\begin{aligned}
\dim K_{\widehat{\mathcal{T}}}(\mathrm{div}) &= 3|\mathcal{V}(\widehat{\mathcal{T}})| + |\mathcal{V}_0(\widehat{\mathcal{T}}) \setminus \mathcal{V}(\mathcal{T}_0)| + 2(k-1)|\widehat{\mathcal{E}}| + \frac{3k(k-1)}{2}|\widehat{\mathcal{T}}| - k(k+1)|\widehat{\mathcal{T}}| \\
&= 3|\mathcal{V}(\widehat{\mathcal{T}})| + |\mathcal{V}_0(\widehat{\mathcal{T}}) \setminus \mathcal{V}(\mathcal{T}_0)| + 2(k-1)|\widehat{\mathcal{E}}| + \frac{k(k-5)}{2}|\widehat{\mathcal{T}}|.
\end{aligned}
$$
而空间 $\operatorname{Curl}\operatorname{Curl} S^{k+2}(\widehat{\mathcal{T}})$ 的维数为：
$$
6|\mathcal{V}(\widehat{\mathcal{T}})| + |\mathcal{V}_0(\widehat{\mathcal{T}}) \setminus \mathcal{V}(\mathcal{T}_0)| + (2k-5)|\widehat{\mathcal{E}}| + \frac{(k-2)(k-3)}{2}|\widehat{\mathcal{T}}| - 3.
$$
由于 $\Omega$ 是单连通多边形区域，Euler 示性数公式满足：
$$
|\mathcal{V}(\widehat{\mathcal{T}})| - |\widehat{\mathcal{E}}| + |\widehat{\mathcal{T}}| = 1.
$$
代入化简即可得 $\dim \operatorname{Curl}\operatorname{Curl} S^{k+2}(\widehat{\mathcal{T}}) = \dim K_{\widehat{\mathcal{T}}}(\mathrm{div})$，从而 $\operatorname{Curl}\operatorname{Curl} S^{k+2}(\widehat{\mathcal{T}}) = K_{\widehat{\mathcal{T}}}(\mathrm{div})$。证毕。$\blacksquare$

> **引理 3.7（准插值算子 Quasi-interpolation）**：设 $S^{k+2}(\mathcal{T})$ 与 $S^{k+2}(\widehat{\mathcal{T}})$ 为式 (3.10) 针对 $\mathcal{T}$ 和 $\widehat{\mathcal{T}}$ 定义的空间。存在准插值算子 $\Pi_{\mathcal{T},\nabla^2}: S^{k+2}(\widehat{\mathcal{T}}) \to S^{k+2}(\mathcal{T})$，其在 $\mathcal{T}$ 的所有顶点处保持函数值不变，且对任意 $\varphi(\widehat{\mathcal{T}}) \in S^{k+2}(\widehat{\mathcal{T}})$ 满足：
> 1. 对任意 $x \in \mathcal{V}(\mathcal{T})$，$\Pi_{\mathcal{T},\nabla^2}\varphi(\widehat{\mathcal{T}})(x) = \varphi(\widehat{\mathcal{T}})(x)$；
> 2. 对任意 $K \in \mathcal{T} \cap \widehat{\mathcal{T}}$（未细化单元），$\Pi_{\mathcal{T},\nabla^2}\varphi(\widehat{\mathcal{T}})|_K = \varphi(\widehat{\mathcal{T}})|_K$；
> 3. 对任意 $K \in \mathcal{T}$，设局部片 $\Omega(K) := \operatorname{int}\left( \bigcup \{ K' \in \mathcal{T} \mid \operatorname{dist}(K, K') = 0 \} \right)$，则成立局部逼近估计：
> $$
> \sum_{m=0}^2 h_K^{m-2} |\varphi(\widehat{\mathcal{T}}) - \Pi_{\mathcal{T},\nabla^2}\varphi(\widehat{\mathcal{T}})|_{m,K} \le C_{\mathrm{apx}} |\varphi(\widehat{\mathcal{T}})|_{2,\Omega(K)},
> \tag{3.11}
> $$
> 其中常数 $C_{\mathrm{apx}}$ 仅依赖于初始网格 $\mathcal{T}_0$ 的形状正则性。

*证明*：空间 $S^{k+2}(\widehat{\mathcal{T}})$ 的准插值算子在文献 [15] 中通过推广高阶 Argyris 有限元空间的准插值方法 [19] 构造得到，并证明了性质 (2) 与 (3)。为进一步保持粗网格顶点处的函数值，只需将对应于顶点函数值自由度的基函数线性组合系数直接替换为函数在这些顶点处的精确值即可。证毕。$\blacksquare$

> **引理 3.8**：设 $(\sigma(\mathcal{T}), u(\mathcal{T})) \in \widetilde{\Sigma}(\mathcal{T}) \times V(\mathcal{T})$ 为式 (3.3) 在 $\mathcal{T}$ 上的解，$(\widehat{\sigma}(\widehat{\mathcal{T}}), \widehat{u}(\widehat{\mathcal{T}})) \in \widetilde{\Sigma}(\widehat{\mathcal{T}}) \times V(\widehat{\mathcal{T}})$ 为式 (3.8) 的解。则有
> $$
> \|\sigma(\mathcal{T}) - \widehat{\sigma}(\widehat{\mathcal{T}})\|_{\mathbb{A}}^2 \lesssim \eta^2(\mathcal{T}, \mathcal{T} \setminus \widehat{\mathcal{T}}).
> $$

*证明*：记 $\xi(\widehat{\mathcal{T}}) := \sigma(\mathcal{T}) - \widehat{\sigma}(\widehat{\mathcal{T}})$。由于 $\operatorname{div}\xi(\widehat{\mathcal{T}}) = 0$，由引理 3.6 可知存在 $\varphi(\widehat{\mathcal{T}}) \in S^{k+2}(\widehat{\mathcal{T}})$ 使得 $\xi(\widehat{\mathcal{T}}) = \operatorname{Curl}\operatorname{Curl}\varphi(\widehat{\mathcal{T}})$。取引理 3.7 中的准插值算子 $\Pi_{\mathcal{T},\nabla^2}$，令 $\psi(\widehat{\mathcal{T}}) := \varphi(\widehat{\mathcal{T}}) - \Pi_{\mathcal{T},\nabla^2}\varphi(\widehat{\mathcal{T}}) \in S^{k+2}(\widehat{\mathcal{T}})$。在式 (3.8) 中选测试函数 $\tau(\widehat{\mathcal{T}}) = \xi(\widehat{\mathcal{T}})$，在 $\mathcal{T}$ 上的式 (3.3) 中选测试函数 $\tau(\mathcal{T}) = \operatorname{Curl}\operatorname{Curl}(\Pi_{\mathcal{T},\nabla^2}\varphi(\widehat{\mathcal{T}}))$，再利用引理 3.7(2) 在未细化单元上残差为零的性质，可得：
$$
\begin{aligned}
\|\xi(\widehat{\mathcal{T}})\|_{\mathbb{A}}^2 &= (\mathbb{A}(\sigma(\mathcal{T}) - \widehat{\sigma}(\widehat{\mathcal{T}})), \xi(\widehat{\mathcal{T}})) = (\mathbb{A}\sigma(\mathcal{T}), \operatorname{Curl}\operatorname{Curl}\psi(\widehat{\mathcal{T}})) \\
&= \sum_{K \in \mathcal{T} \setminus \widehat{\mathcal{T}}} (\mathbb{A}\sigma(\mathcal{T}), \operatorname{Curl}\operatorname{Curl}\psi(\widehat{\mathcal{T}}))_K.
\end{aligned}
$$
分部积分两次可得：
$$
\begin{aligned}
\|\xi(\widehat{\mathcal{T}})\|_{\mathbb{A}}^2 &= \sum_{K \in \mathcal{T} \setminus \widehat{\mathcal{T}}} (\operatorname{curl}\operatorname{curl}(\mathbb{A}\sigma(\mathcal{T})), \psi(\widehat{\mathcal{T}}))_K + \sum_{K \in \mathcal{T} \setminus \widehat{\mathcal{T}}} \sum_{e \in \mathcal{E}(K)} \langle (\mathbb{A}\sigma(\mathcal{T}))t \cdot t, \operatorname{Curl}\psi(\widehat{\mathcal{T}}) \cdot t \rangle_e \\
&\quad - \sum_{K \in \mathcal{T} \setminus \widehat{\mathcal{T}}} \sum_{e \in \mathcal{E}(K)} \langle \operatorname{curl}(\mathbb{A}\sigma(\mathcal{T})) \cdot t, \psi(\widehat{\mathcal{T}}) \rangle_e + \sum_{K \in \mathcal{T} \setminus \widehat{\mathcal{T}}} \sum_{e \in \mathcal{E}(K)} \langle (\mathbb{A}\sigma(\mathcal{T}))t \cdot n, \operatorname{Curl}\psi(\widehat{\mathcal{T}}) \cdot n \rangle_e.
\end{aligned}
\tag{3.12}
$$
由于顺度张量 $\mathbb{A}$ 对称连续，$(\mathbb{A}\sigma(\mathcal{T})t) \cdot n = (\mathbb{A}\sigma(\mathcal{T})n) \cdot t = (t^T \sigma(\mathcal{T})n)/(2\mu)$ 跨越内部边 $e$ 保持连续。又由于引理 3.7(1) 保证了 $\psi(\widehat{\mathcal{T}})$ 在每个粗网格顶点 $x \in \mathcal{V}(\mathcal{T})$ 处均为零，再次分部积分可得：
$$
\begin{aligned}
\sum_{K \in \mathcal{T} \setminus \widehat{\mathcal{T}}} \sum_{e \in \mathcal{E}(K)} \langle (\mathbb{A}\sigma(\mathcal{T}))t \cdot n, \operatorname{Curl}\psi(\widehat{\mathcal{T}}) \cdot n \rangle_e &= -\sum_{K \in \mathcal{T} \setminus \widehat{\mathcal{T}}} \sum_{e \in \mathcal{E}(\Gamma) \cap \mathcal{E}(K)} \langle (\mathbb{A}\sigma(\mathcal{T}))t_e \cdot n_e, \partial_{t_e}\psi(\widehat{\mathcal{T}}) \rangle_e \\
&= \sum_{K \in \mathcal{T} \setminus \widehat{\mathcal{T}}} \sum_{e \in \mathcal{E}(\Gamma) \cap \mathcal{E}(K)} \langle \partial_{t_e}((\mathbb{A}\sigma(\mathcal{T}))t_e \cdot n_e), \psi(\widehat{\mathcal{T}}) \rangle_e.
\end{aligned}
$$
结合式 (3.12)，利用迹不等式以及式 (3.11) 关于 $\psi(\widehat{\mathcal{T}})$ 的局部逼近估计，并利用 $|\varphi(\widehat{\mathcal{T}})|_{2,\Omega} \lesssim \|\xi(\widehat{\mathcal{T}})\|_0$，可推导得出：
$$
\|\xi(\widehat{\mathcal{T}})\|_{\mathbb{A}}^2 \lesssim \sum_{K \in \mathcal{T} \setminus \widehat{\mathcal{T}}} \eta(\mathcal{T}, K) |\varphi(\widehat{\mathcal{T}})|_{2,\Omega(K)} \lesssim \eta(\mathcal{T}, \mathcal{T} \setminus \widehat{\mathcal{T}}) \|\xi(\widehat{\mathcal{T}})\|_0.
\tag{3.13}
$$
由于 $\operatorname{div}\xi(\widehat{\mathcal{T}}) = 0$ 且 $\int_\Omega \operatorname{tr}\xi(\widehat{\mathcal{T}}) \,\mathrm{d}x = \int_\Omega \operatorname{tr}(\sigma(\mathcal{T}) - \widehat{\sigma}(\widehat{\mathcal{T}})) \,\mathrm{d}x = 0$，由文献 [9, Prop. 9.1.1] 的经典不等式知 $\|\xi(\widehat{\mathcal{T}})\|_0 \lesssim \|\xi(\widehat{\mathcal{T}})\|_{\mathbb{A}}$。代入式 (3.13) 即证毕。$\blacksquare$

> **定理 3.9（离散可靠性 Discrete Reliability）**：存在正常数 $C$ 使得
> $$
> \|\sigma(\widehat{\mathcal{T}}) - \sigma(\mathcal{T})\|_{\mathbb{A}}^2 \le C \left( \eta^2(\mathcal{T}, \mathcal{T} \setminus \widehat{\mathcal{T}}) + \operatorname{osc}^2(f, \mathcal{T} \setminus \widehat{\mathcal{T}}) \right).
> $$

*证明*：由三角不等式 $\|\sigma(\widehat{\mathcal{T}}) - \sigma(\mathcal{T})\|_{\mathbb{A}} \le \|\sigma(\mathcal{T}) - \widehat{\sigma}(\widehat{\mathcal{T}})\|_{\mathbb{A}} + \|\sigma(\widehat{\mathcal{T}}) - \widehat{\sigma}(\widehat{\mathcal{T}})\|_{\mathbb{A}}$，直接结合引理 3.4 和引理 3.8 即证。$\blacksquare$

凭借定理 3.5 的拟正交性与定理 3.9 的离散可靠性，仿照文献 [10, 16, 23, 27, 28] 的公理化框架，即可严格建立自适应算法的收敛性与最优收敛速率。

> **引理 3.10（估计子削减 Estimator Reduction）**：设 $(\sigma(\mathcal{T}_\ell), u(\mathcal{T}_\ell)) \in \widetilde{\Sigma}(\mathcal{T}_\ell) \times V(\mathcal{T}_\ell)$ 分别为离散问题 (3.3) 在嵌套网格序列 $\mathcal{T}_\ell$ 与 $\mathcal{T}_{\ell-1}$ 上的数值解。则对任意正常数 $\epsilon > 0$，存在 $\lambda := 1 - 2^{-1/2} < 1$ 与常数 $C_\epsilon > 0$ 使得
> $$
> \eta^2(\mathcal{T}_\ell) \le (1 + \epsilon)\left( \eta^2(\mathcal{T}_{\ell-1}) - \lambda \eta^2(\mathcal{T}_{\ell-1}, \mathcal{M}_{\ell-1}) \right) + C_\epsilon \|\sigma(\mathcal{T}_\ell) - \sigma(\mathcal{T}_{\ell-1})\|_{\mathbb{A}}^2,
> $$
> 且
> $$
> \operatorname{osc}^2(f, \mathcal{T}_\ell) \le \operatorname{osc}^2(f, \mathcal{T}_{\ell-1}) - \lambda \operatorname{osc}^2(f, \mathcal{T}_{\ell-1} \setminus \mathcal{T}_\ell).
> $$

*证明*：证明过程完全遵循文献 [16, Corollary 4.4] 的标准论证。$\blacksquare$

> **定理 3.11（拟收缩收敛性 Contraction Property）**：给定 $f \in L^2(\Omega; \mathbb{R}^2)$，设 $(\sigma, u)$ 为式 (2.1) 的精确解，$(\sigma(\mathcal{T}_\ell), u(\mathcal{T}_\ell))$ 为自适应算法生成的离散解序列。则存在常数 $0 < \alpha < 1$ 以及 $\beta > 0, \gamma > 0$，使得总误差泛函满足几何级数收缩：
> $$
> \mathcal{E}_\ell \le \alpha \mathcal{E}_{\ell-1},
> $$
> 其中总误差泛函定义为
> $$
> \mathcal{E}_\ell := \|\sigma - \sigma(\mathcal{T}_\ell)\|_{\mathbb{A}}^2 + \gamma \eta^2(\mathcal{T}_\ell) + (\beta + \gamma)\operatorname{osc}^2(f, \mathcal{T}_\ell).
> $$

*证明*：结合引理 3.10、后验误差可靠性 (3.6) 以及拟正交性定理 3.5 即可推导完成。详细推导参见文献 [10, 23, 28]。$\blacksquare$

对于 $s > 0$，定义非线性逼近类（approximation class）$\mathcal{A}^s$ 为：
$$
\mathcal{A}^s := \left\{ (\sigma, f) \;\middle|\; |\sigma, f|_s := \sup_{N > 0} N^s \inf_{\substack{|\mathcal{T}| - |\mathcal{T}_0| \le N \\ \tau \in \widetilde{\Sigma}(\mathcal{T})}} \left( \|\sigma - \tau\|_{\mathbb{A}}^2 + \operatorname{osc}^2(f, \mathcal{T}) \right)^{1/2} < \infty \right\}.
$$

> **定理 3.12（最优收敛阶与复杂度 Optimality）**：设 $\mathcal{M}_\ell$ 为满足 Dörfler 标记准则的最小基数标记集，$(\sigma, u)$ 为式 (2.1) 的精确解，$(\mathcal{T}_\ell, \widetilde{\Sigma}(\mathcal{T}_\ell) \times V(\mathcal{T}_\ell), \sigma(\mathcal{T}_\ell), u(\mathcal{T}_\ell))$ 为带有标记参数 $\theta$ 的自适应混合有限元方法生成的网格、离散空间及数值解序列。则对任意 $(\sigma, f) \in \mathcal{A}^s$，下述最优收敛估计成立：
> $$
> \|\sigma - \sigma(\mathcal{T}_\ell)\|_{\mathbb{A}}^2 + \operatorname{osc}^2(f, \mathcal{T}_\ell) \lesssim |\sigma, f|_s^2 (|\mathcal{T}_\ell| - |\mathcal{T}_0|)^{-2s}.
> $$

*证明*：基于引理 3.10、拟正交性定理 3.5、离散可靠性定理 3.9 及有效性估计 (3.7)，应用文献 [10, 23, 28] 的标准公理化自适应最优性证明方法即可证得结论。$\blacksquare$

---

# 4 角点处的扩展应力空间

本节致力于处理式 (2.1) 中具有 $|\Gamma_N| > 0$ 且 $g \not\equiv 0$ 的非齐次面力边界条件情形。

## 4.1 二维情形

回顾式 (2.3) 中定义的离散应力空间 $\Sigma(\widehat{\mathcal{T}})$。为在 $\Gamma_N$ 上施加一般的面力边界条件 $g$，需要构造某种逼近 $g(\widehat{\mathcal{T}}) = \alpha(\widehat{\mathcal{T}}) n|_{\Gamma_N}$（其中 $\alpha(\widehat{\mathcal{T}}) \in \Sigma(\widehat{\mathcal{T}})$）。由于 $\alpha(\widehat{\mathcal{T}})$ 在每个边界顶点处都是连续的，通常不能直接将 $g(\widehat{\mathcal{T}})$ 取为 $g$ 的常规节点插值。

为阐明这一点，考虑图 4.1(a) 所示的情形：多边形区域 $\Omega$ 边界上的一个角点 $x_c$ 是两条边界边 $e^+$ 和 $e^-$ 的唯一公共交点。记 $t_i$ 和 $n_i$（$i = +, -$）分别为边 $e^i$ 的单位切向量与单位外法向量。若施加在 $e^+$ 与 $e^-$ 上的面力边界条件 $g|_{e^i}$ 是**一致**（连续）的，即满足
$$
(n_-^T g|_{e^+})(x_c) = (n_+^T g|_{e^-})(x_c),
$$
则常规的节点插值可以良好定义如下：
$$
S^{11} \phi_{x_c}(x) S_1 + S^{12} \phi_{x_c}(x) S_2 + S^{22} \phi_{x_c}(x) S_3 + \tau,
\tag{4.1}
$$
其中 $\tau \in \Sigma(\widehat{\mathcal{T}})$ 且在 $x_c$ 处取值为零。$\phi_{x_c}(x)$ 是关联于顶点 $x_c$ 的 $k$ 次标量 Lagrange 节点基函数，$S_i$ 是式 (2.4) 给出的对称矩阵标准基。组合系数 $S^{11}, S^{12}, S^{22}$ 是如下方程组唯一解 $S \in \mathbb{S}$ 的三个独立分量：
$$
\begin{cases}
n_+^T S n_+ = (n_+^T g|_{e^+})(x_c), \\
n_-^T S n_- = (n_-^T g|_{e^-})(x_c), \\
n_+^T S n_- = (n_+^T g|_{e^-})(x_c).
\end{cases}
$$

然而，一般的面力边界条件可能是**不一致**（不连续）的，即
$$
(n_-^T g|_{e^+})(x_c) \neq (n_+^T g|_{e^-})(x_c).
$$
这种不一致性为在离散应力空间 $\Sigma(\widehat{\mathcal{T}})$ 中施加该边界条件带来了本质困难。特别是，式 (4.1) 中的常规节点插值甚至无法定义，因为组合系数矩阵 $S$ 必须同时满足如下四个方程：
$$
\begin{cases}
n_+^T S n_+ = (n_+^T g|_{e^+})(x_c), \\
n_-^T S n_- = (n_-^T g|_{e^-})(x_c), \\
n_+^T S n_- = (n_+^T g|_{e^-})(x_c), \\
n_-^T S n_+ = (n_-^T g|_{e^+})(x_c).
\end{cases}
$$
当边界条件不一致时，由于矩阵 $S$ 的对称性必然要求 $n_+^T S n_- = n_-^T S n_+$，上述由 4 个方程构成的系统无解。其结果是，即使面力 $g|_{e^i}$ 本身是不超过 $k$ 次的多项式，也无法精确施加该边界条件。文献 [13] 采用最小二乘法来妥协处理该问题。

下面将第 3.1 节中处理非嵌套性的思想推广到角点处，以实现角点处的精确节点插值。

解决这一困难的核心思想是：**将角点处的三角形分割为两个子三角形，然后松弛跨越这两个子三角形公共内边的纯切向分量的连续性**。为此，首先将包含角点 $x_c$ 的单元 $K$ 剖分为由两个三角形 $K^+$ 与 $K^-$ 组成的局部片，记公共内边为 $e = K^+ \cap K^-$，如图 4.1(b) 所示。离散应力的纯切向分量在角点 $x_c$ 处跨越边 $e$ 时不再强制连续。因此，可以将该自由度分裂为分别属于 $K^+$ 和 $K^-$ 的两个独立自由度。在图 4.1(c) 中，实心点代表这两个分离的纯切向自由度，空心圆圈代表跨越边 $e$ 保持连续的两个法向分量自由度。

![[Hu2021_Fig4_1.png]]

<center><b>
图 4.1：角点顶点 $x_c$ 处的自由度演变示意图：(a) 处理前；(b) 划分为两个子三角形；(c) 切向分量分裂；(d) 处理后
</b></center>

为定义节点插值，关联于顶点 $x_c$ 的扩展应力空间的 4 个基函数构造如下（如图 4.1(d) 所示）：
$$
\tau_1 = \phi_{x_c} \begin{cases}
S_{e^+, 1}^\perp + c_1 S_{e^+}, & \text{在 } K^+ \text{ 上}, \\
d_1 S_{e^-}, & \text{在 } K^- \text{ 上},
\end{cases}
\quad 
\tau_2 = \phi_{x_c} \begin{cases}
S_{e^+, 2}^\perp + c_2 S_{e^+}, & \text{在 } K^+ \text{ 上}, \\
d_2 S_{e^-}, & \text{在 } K^- \text{ 上},
\end{cases}
\tag{4.2}
$$
$$
\tau_3 = \phi_{x_c} \begin{cases}
c_3 S_{e^+}, & \text{在 } K^+ \text{ 上}, \\
S_{e^-, 1}^\perp + d_3 S_{e^-}, & \text{在 } K^- \text{ 上},
\end{cases}
\quad 
\tau_4 = \phi_{x_c} \begin{cases}
c_4 S_{e^+}, & \text{在 } K^+ \text{ 上}, \\
S_{e^-, 2}^\perp + d_4 S_{e^-}, & \text{在 } K^- \text{ 上}.
\end{cases}
$$
其中 $\phi_{x_c}$ 是关联于 $x_c$ 的标量 Lagrange 节点基函数，其余矩阵记号由式 (2.5) 定义。常数 $c_i, d_i$（$1 \le i \le 4$）由 $\tau_i$ 跨越公共内边 $e$ 的法向连续性条件确定。例如，给定边 $e$ 的单位法向量 $n_e$，$\tau_1$ 的法向连续性要求满足如下线性方程组：
$$
\left( S_{e^+, 1}^\perp + c_1 S_{e^+} \right) n_e = d_1 S_{e^-} n_e.
\tag{4.3}
$$
回顾矩阵 $S_{e^+} = t_{e^+} t_{e^+}^T$（切向量为 $t_{e^+}$），对于 $S_{e^-}$ 同理。设 $t_{e^+} = (a, b)^T$，定义其正交行向量为 $t_{e^+}^\perp = (b, -a)$；$t_{e^-}^\perp$ 的定义类似。记 $D$ 为由两个列向量组成的矩阵 $(t_{e^+}, t_{e^-})$ 的行列式。初等代数运算可直接给出如下逆矩阵：
$$
\left( S_{e^+} n_e, \; -S_{e^-} n_e \right)^{-1} = \left( (t_{e^+}^T n_e) t_{e^+}, \; -(t_{e^-}^T n_e) t_{e^-} \right)^{-1} = \frac{1}{D} \begin{pmatrix} \frac{1}{t_{e^+}^T n_e} t_{e^-}^\perp \\ \frac{1}{t_{e^-}^T n_e} t_{e^+}^\perp \end{pmatrix}.
$$
只要边界边 $e^+$ 与 $e^-$ 不平行（即角点处的内角不为 $\pi$），方程组 (4.3) 的系数矩阵必非奇异，从而常数 $c_1, d_1$ 存在且唯一。同理可求出其余常数。

> **注记 4.1（三个子三角形情形）**：设角点 $x_c$ 周围汇聚了三个三角形 $K^+, K, K^-$，公共内边分别为 $e_1 = K^+ \cap K$ 与 $e_2 = K^- \cap K$，如图 4.2 所示。为松弛 $x_c$ 处的连续性，类似的论证可在角点处构造 5 个新的基函数如下：
> $$
> \tau_1 = \phi_{x_c} \begin{cases}
> S_{e^+, 1}^\perp + c_1 S_{e^+}, & \text{在 } K^+ \text{ 上}, \\
> d_1 S_{e_2}, & \text{在 } K \text{ 上}, \\
> 0, & \text{在 } K^- \text{ 上},
> \end{cases}
> \quad 
> \tau_2 = \phi_{x_c} \begin{cases}
> S_{e^+, 2}^\perp + c_2 S_{e^+}, & \text{在 } K^+ \text{ 上}, \\
> d_2 S_{e_2}, & \text{在 } K \text{ 上}, \\
> 0, & \text{在 } K^- \text{ 上},
> \end{cases}
> $$
> $$
> \tau_3 = \phi_{x_c} \begin{cases}
> 0, & \text{在 } K^+ \text{ 上}, \\
> c_3 S_{e_1}, & \text{在 } K \text{ 上}, \\
> S_{e^-, 1}^\perp + d_3 S_{e^-}, & \text{在 } K^- \text{ 上},
> \end{cases}
> \quad 
> \tau_4 = \phi_{x_c} \begin{cases}
> 0, & \text{在 } K^+ \text{ 上}, \\
> c_4 S_{e_1}, & \text{在 } K \text{ 上}, \\
> S_{e^-, 2}^\perp + d_4 S_{e^-}, & \text{在 } K^- \text{ 上},
> \end{cases}
> \tag{4.4}
> $$
> $$
> \tau_5 = \phi_{x_c} \begin{cases}
> S_{e^+}, & \text{在 } K^+ \text{ 上}, \\
> c_5 S_{e_1, 1}^\perp + d_5 S_{e_1, 2}^\perp + g_5 S_{e_1}, & \text{在 } K \text{ 上}, \\
> h_5 S_{e^-}, & \text{在 } K^- \text{ 上}.
> \end{cases}
> $$
> 利用 $\tau_j$（$j=1,2$）跨越 $e_1$ 的法向连续性可唯一确定 $c_j, d_j$；利用 $\tau_j$（$j=3,4$）跨越 $e_2$ 的法向连续性可确定 $c_j, d_j$；利用 $\tau_5$ 跨越 $e_1$ 和 $e_2$ 的法向连续性可确定系数 $c_5, d_5, g_5, h_5$。

![[Hu2021_Fig4_2.png]]

<center><b>
图 4.2：围绕角点 $x_c$ 汇聚的三个子三角形示意图
</b></center>

## 4.2 三维情形的讨论

本小节简要探讨如何将四面体网格上线弹性混合有限元 [21, 25] 的离散应力空间进行类似扩展。除顶点 $C^0$ 连续性外，三维离散应力张量在棱边上亦存在一定的连续性约束。若在边界 $\Gamma_N$ 上三个平面相交的角点处存在不一致面力边界条件，则需要同时处理与顶点和棱边关联的自由度。

给定图 4.3 所示的四面体单元 $K := x_0 x_1 x_2 x_3$，设 $x_0$ 为角点顶点。为松弛顶点及棱边处的某些连续性，引入单元质心 $x'_0$，将四面体 $K$ 剖分为四个子四面体。其目标是构造与顶点 $x_0$ 以及棱边 $x_0 x_1, x_0 x_2, x_0 x_3$ 关联的新基函数。记 $n_1, n_2, n_3$ 分别为面 $F_1 := x_0 x_2 x_1$、面 $F_2 := x_0 x_1 x_3$ 以及面 $F_3 := x_0 x_3 x_2$ 的单位外法向量。

![[Hu2021_Fig4_3.png]]

<center><b>
图 4.3：角点四面体 $K$ 及其质心子剖分示意图
</b></center>

对于每个子四面体 $K_m := \operatorname{conv}(x'_0 \cup F_m)$（$1 \le m \le 3$），存在三个线性无关的对称矩阵 $S_{j,m}$ 使得 $S_{j,m} n_m = 0$（$1 \le j \le 3$），以及三个线性无关的对称矩阵 $S_{i,m}^\perp$ 使得 $S_{i,m}^\perp : S_{j,m} = 0$（$1 \le i \le 3$）。假设具有如下形式：
$$
\tau_{i,1} = \phi_{x_0} \begin{cases}
S_{i,1}^\perp + \sum_{j=1}^3 c_{j,1} S_{j,1}, & \text{在 } K_1 \text{ 上}, \\
\sum_{j=1}^3 d_{j,1} S_{j,2}, & \text{在 } K_2 \text{ 上}, \\
\sum_{j=1}^3 e_{j,1} S_{j,3}, & \text{在 } K_3 \text{ 上},
\end{cases}
$$
其中 $\phi_{x_0}$ 为关联于 $x_0$ 的标量 Lagrange 基函数，待定常数为 $c_{j,1}, d_{j,1}, e_{j,1}$（共 9 个）。易验 $\tau_{i,1} n_m|_{F_m} = 0$（$m=2,3$）。利用跨越子四面体内部公共面的法向连续性条件，只要面 $F_m$（$1 \le m \le 3$）中任意两个不共面，即可唯一解出这些常数。由此，$\tau_{i,1}$（$1 \le i \le 3$）构成了关联于顶点 $x_0$ 的 3 个新基函数。类似地可构造与顶点 $x_0$ 关联的其余 6 个基函数（共 9 个）。

对于棱边 $x_0 x_1$ 上的任意内部节点 $a$，定义：
$$
\xi_{i,1} = \phi_a \begin{cases}
S_{i,1}^\perp + \sum_{j=1}^3 c_{j,1} S_{j,1}, & \text{在 } K_1 \text{ 上}, \\
\sum_{j=1}^3 d_{j,1} S_{j,2}, & \text{在 } K_2 \text{ 上},
\end{cases}
$$
其中 $\phi_a$ 为关于节点 $a$ 的标量 Lagrange 基函数。注意到跨越内部面 $x_1 x'_0 x_0$ 的法向连续性仅强加了 3 个约束条件，因此在 $K_1 \cup K_2$ 上存在局部的 $\boldsymbol{H}(\mathrm{div})$ 泡状函数。设 $t, t_1, t_2$ 分别为棱边 $x_0 x_1, x_0 x_2, x_0 x_3$ 的切向量，$n$ 为面 $x_1 x'_0 x_0$ 的法向量，对应的 3 个 $\boldsymbol{H}(\mathrm{div})$ 泡状函数显式为：
$$
b_1 = \begin{cases} \phi_a t t^T, & \text{在 } K_1 \text{ 上}, \\ 0, & \text{在 } K_2 \text{ 上}, \end{cases} \quad 
b_2 = \begin{cases} 0, & \text{在 } K_1 \text{ 上}, \\ \phi_a t t^T, & \text{在 } K_2 \text{ 上}, \end{cases} \quad 
b_3 = \begin{cases} \frac{\phi_a}{t_1^T n}(t_1 t^T + t t_1^T), & \text{在 } K_1 \text{ 上}, \\ \frac{\phi_a}{t_2^T n}(t_2 t^T + t t_2^T), & \text{在 } K_2 \text{ 上}. \end{cases}
$$
在泡状函数约束下，只要面 $F_1$ 与 $F_2$ 不平行，便存在唯一的常数组 $c_{j,1}, d_{j,1}$。于是 $\xi_{i,1}$（$1 \le i \le 3$）构成了关联于棱边 $x_0 x_1$ 的 3 个新基函数。

---

# 5 数值实验

本节给出 5 个数值算例，将第 2.3 节介绍的文献 [24] 中的 $k=3$ 协调混合有限元在应力空间松弛顶点 $C^0$ 连续性前后的计算表现进行系统对比。算例 5.2–5.4 分别在均匀网格和自适应网格上展示采用第 4.1 节角点松弛策略的效果；算例 5.5 则验证第 3.1 节构造的嵌套离散应力空间自适应混合有限元算法的最优收敛速率。

## 5.1 界面问题

设 $x = (x_1, x_2)^T$。考虑一个分片常数应力场
$$
\sigma = \begin{pmatrix} \sigma_{11} & 0 \\ 0 & 0 \end{pmatrix},
$$
其纯切向分量 $\sigma_{11}$ 跨越直线 $x_2 = 0.5$ 发生间断跳跃，如图 5.1(a) 所示。假设网格 $\widehat{\mathcal{T}}$ 的任意边与直线 $x_2 = 0.5$ 的交集或者为空集，或者为一个顶点，或者整条边重合。回顾式 (2.3) 的离散应力空间 $\Sigma(\widehat{\mathcal{T}})$，由于其中的矩阵值函数在 $\widehat{\mathcal{T}}$ 的每个顶点处都是 $C^0$ 连续的，显然真实解 $\sigma \notin \Sigma(\widehat{\mathcal{T}})$，因此原始混合有限元格式 (2.8) 无法精确求解该应力。

针对位于界面 $x_2 = 0.5$ 上的顶点 $a$（如图 5.1 所示），采用第 3.1 节的策略，将沿 $x_2 = 0.5$ 的纯切向分量自由度分裂为分别由上部平面和下部平面共享的两个独立自由度。在图 5.1 中，两个实心点表示分裂后的两个切向自由度，空心圆圈表示法向分量自由度。对 $x_2 = 0.5$ 上的所有顶点作完全类似的处理。通过将所有切向分量跨越 $x_2 = 0.5$ 不连续的新基函数加入到 $\Sigma(\widehat{\mathcal{T}})$ 中，即可构造扩展应力空间 $\widetilde{\Sigma}(\widehat{\mathcal{T}})$。

![[Hu2021_Fig5_1.png]]

<center><b>
图 5.1：界面点 $a$ 处自由度示意图：(a) 处理前；(b) 处理后
</b></center>

考虑 $\sigma$ 在 $\widetilde{\Sigma}(\widehat{\mathcal{T}})$ 中的插值。定义插值算子 $I_{\widehat{\mathcal{T}}}\sigma_{11}$ 在顶点 $a$ 处于 $x_2 = 0.5$ 下方的每个单元中取值为 1，在上方每个单元中取值为 10。因此 $I_{\widehat{\mathcal{T}}}\sigma_{11} = \sigma_{11}$ 完全重合。由于混合元计算误差由插值误差控制，基于扩展应力空间 $\widetilde{\Sigma}(\widehat{\mathcal{T}})$ 的混合有限元方法能够精确解出该应力场（误差达到机器精度）。

## 5.2 均匀网格上带角点处理的 L 形区域基准问题

考虑图 5.2 所示的旋转 L 形多边形区域 $\Omega \subset \mathbb{R}^2$ 上的基准模型问题。在极坐标系 $(r, \varphi)$ 下，精确位移解解析表达式为：
$$
\begin{aligned}
u_r(r, \varphi) &= \frac{r^\alpha}{2\mu} \left( -(\alpha + 1)\cos((\alpha + 1)\varphi) + (C_2 - \alpha - 1)C_1 \cos((\alpha - 1)\varphi) \right), \\
u_\varphi(r, \varphi) &= \frac{r^\alpha}{2\mu} \left( (\alpha + 1)\sin((\alpha + 1)\varphi) + (C_2 + \alpha - 1)C_1 \sin((\alpha - 1)\varphi) \right),
\end{aligned}
$$
其中常数分别定义为 $C_1 := -\frac{\cos((\alpha + 1)\omega)}{\cos((\alpha - 1)\omega)}$，以及 $C_2 := \frac{2(\lambda + 2\mu)}{\lambda + \mu}$。当 $\omega = 3\pi/4$ 时，参数 $\alpha = 0.544483736782$ 为超越方程 $\alpha\sin(2\omega) + \sin(2\omega\alpha) = 0$ 的最小正根。材料弹性模量取 $E = 10^5$，泊松比取 $\nu = 0.499$（对应近不可压缩状态）。体载荷与外表面力均设为零，Dirichlet 边界条件由精确解给定。该精确解在坐标原点（内凹角点）$x_c$ 处具有极强的应力奇异性。

![[Hu2021_Fig5_2.png]]

<center><b>
图 5.2：L 形区域的初始粗网格剖分与边界设置
</b></center>

计算所用的网格序列通过对图 5.2 的初始网格进行逐级均匀加密生成。虽然由于面力为零，此处并不强制需要处理角点自由度，但考虑到精确解在 $x_c$ 处的奇异性，按第 4.1 节的策略在 $x_c$ 处松弛 $C^0$ 连续性。表 5.1 给出了松弛处理前后的误差与收敛阶对比。由表 5.1 可知，松弛处理后，应力误差 $\|\sigma - \sigma(\widehat{\mathcal{T}})\|_{\mathbb{A}}$ 与位移误差 $\|u - u(\widehat{\mathcal{T}})\|_0$ 均得到了大幅削减，这是因为在原点 $x_c$ 处松弛连续性引入了更多的局部自由度，更好地捕捉了角点处的奇异行为。

<center><b>
表 5.1：均匀网格上 L 形区域基准问题的误差与收敛阶对比
</b></center>

| 网格层级 | $\|\sigma - \sigma(\widehat{\mathcal{T}})\|_{\mathbb{A}}$（处理前） | 收敛阶 | $\|\sigma - \sigma(\widehat{\mathcal{T}})\|_{\mathbb{A}}$（处理后） | 收敛阶 | $\|u - u(\widehat{\mathcal{T}})\|_0$（处理前） | 收敛阶 | $\|u - u(\widehat{\mathcal{T}})\|_0$（处理后） | 收敛阶 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 7.5143E-03 | — | 3.1046E-03 | — | 7.2407E-06 | — | 2.1190E-06 | — |
| 2 | 5.5899E-03 | 0.4268 | 2.1945E-03 | 0.5005 | 3.8230E-06 | 0.9214 | 8.9234E-07 | 1.2477 |
| 3 | 3.9400E-03 | 0.5046 | 1.5147E-03 | 0.5348 | 1.8422E-06 | 1.0533 | 3.6866E-07 | 1.2753 |
| 4 | 2.7379E-03 | 0.5251 | 1.0416E-03 | 0.5402 | 8.8088E-07 | 1.0644 | 1.5774E-07 | 1.2247 |
| 5 | 1.8894E-03 | 0.5351 | 7.1517E-04 | 0.5424 | 4.1866E-07 | 1.0732 | 6.9708E-08 | 1.1782 |

## 5.3 均匀网格上带角点处理的 Cook 膜问题

Cook 膜（Cook's membrane）问题的几何区域为四边形，其四个顶点坐标分别为 $(0, 0)$、$(48, 44)$、$(48, 60)$ 和 $(0, 44)$。该结构在左边界（$x_1 = 0$）完全固定（$u = 0$），在右边界（$x_1 = 48$）施加沿坚直方向向上的均布面力载荷 $\sigma n = (0, 1)^T$，其余上下两条边界均为自由表面（$\sigma n = 0$），如图 5.3 所示。材料弹性模量取 $E = 10^5$，泊松比取 $\nu = 0.499$。在右侧两个角点 $x_{c,1} = (48, 60)$ 和 $x_{c,2} = (48, 44)$ 处，存在本质不一致的面力边界条件。

![[Hu2021_Fig5_3.png]]

<center><b>
图 5.3：Cook 膜问题的几何模型、边界条件与初始网格
</b></center>

本算例在角点 $x_{c,1}$ 与 $x_{c,2}$ 处松弛 $C^0$ 连续性。由于该问题无解析解，参考解采用在最终级网格两次均匀加密后的极细网格上使用标准连续 $P_5$ 有限元计算得到。在处理前，由于角点处边界条件的不一致性，采用最小二乘法来确定这两个右侧角点处的应力自由度。表 5.2 列出了处理前后的应力与位移误差对比。结果表明，松弛处理后误差明显降低，尤其是在粗网格上精度提升更为显著。这主要是因为在粗网格上，非精确施加的面力边界条件所带来的误差起着主导作用。

<center><b>
表 5.2：均匀网格上 Cook 膜问题的误差与收敛阶对比
</b></center>

| 网格层级 | $\|\sigma - \sigma(\widehat{\mathcal{T}})\|_{\mathbb{A}}$（处理前） | 收敛阶 | $\|\sigma - \sigma(\widehat{\mathcal{T}})\|_{\mathbb{A}}$（处理后） | 收敛阶 | $\|u - u(\widehat{\mathcal{T}})\|_0$（处理前） | 收敛阶 | $\|u - u(\widehat{\mathcal{T}})\|_0$（处理后） | 收敛阶 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 0.0488 | — | 0.0341 | — | 6.2925E-03 | — | 2.1216E-03 | — |
| 2 | 0.0299 | 0.7048 | 0.0241 | 0.5001 | 3.0423E-03 | 1.0485 | 1.0712E-03 | 0.9859 |
| 3 | 0.0190 | 0.6556 | 0.0167 | 0.5286 | 1.4886E-03 | 1.0311 | 5.3616E-04 | 0.9985 |
| 4 | 0.0121 | 0.6470 | 0.0113 | 0.5685 | 7.2422E-04 | 1.0395 | 2.7651E-04 | 0.9553 |

## 5.4 自适应网格上带角点处理的 Cook 膜问题

在 $|\Gamma_N| \neq 0$ 且 $\Gamma_D$ 上 $u_D \not\equiv 0$ 的一般情况下，式 (3.5) 中的后验误差估计子 $\eta^2(\widehat{\mathcal{T}})$ 修正为文献 [18, Sec. 4] 中的形式，边的跳跃项修改为：
$$
J_{e,1} := \begin{cases}
[(\mathbb{A}\sigma(\widehat{\mathcal{T}}))t_e \cdot t_e]_e, & \text{若 } e \in \widehat{\mathcal{E}}(\Omega), \\
\left( (\mathbb{A}\sigma(\widehat{\mathcal{T}}))t_e \cdot t_e - \partial_{t_e}(u_D \cdot t_e) \right)|_e, & \text{若 } e \in \widehat{\mathcal{E}}(\Gamma_D),
\end{cases}
$$
$$
J_{e,2} := \begin{cases}
[\operatorname{curl}(\mathbb{A}\sigma(\widehat{\mathcal{T}})) \cdot t_e]_e, & \text{若 } e \in \widehat{\mathcal{E}}(\Omega), \\
\left( \operatorname{curl}(\mathbb{A}\sigma(\widehat{\mathcal{T}})) \cdot t_e + \partial_{t_e t_e}(u_D \cdot n_e) - \partial_{t_e}((\mathbb{A}\sigma(\widehat{\mathcal{T}}))t_e \cdot n_e) \right)|_e, & \text{若 } e \in \widehat{\mathcal{E}}(\Gamma_D).
\end{cases}
$$
此时后验误差可靠性估计满足：
$$
\|\sigma - \sigma(\widehat{\mathcal{T}})\|_{\mathbb{A}}^2 \le C_{\mathrm{Rel}}^g \left( \eta^2(\widehat{\mathcal{T}}) + \operatorname{osc}^2(f, \widehat{\mathcal{T}}) + \operatorname{osc}^2(g, \widehat{\mathcal{E}}(\Gamma_N)) \right),
$$
其中面力数据振荡项定义为 $\operatorname{osc}^2(g, \widehat{\mathcal{E}}(\Gamma_N)) := \sum_{e \in \widehat{\mathcal{E}}(\Gamma_N)} h_e \|g - g(\widehat{\mathcal{T}})\|_{0,e}^2$。

定义总后验误差估计子为 $\eta := \left( \eta^2(\widehat{\mathcal{T}}) + \operatorname{osc}^2(f, \widehat{\mathcal{T}}) + \operatorname{osc}^2(g, \widehat{\mathcal{E}}(\Gamma_N)) \right)^{1/2}$。用 $\sigma(\widehat{\mathcal{T}})^O$ 与 $\eta^O$ 分别表示角点处理前由混合元格式 (2.8) 计算得到的离散应力与总估计子；用 $\sigma(\widehat{\mathcal{T}})^M$ 与 $\eta^M$ 表示在角点 $x_{c,1}$ 和 $x_{c,2}$ 处松弛 $C^0$ 连续性后的对应结果。参考解由极细网格上的标准连续 $P_5$ 有限元计算。收敛曲线如图 5.4 所示。由图 5.4 可见，在自适应加密初始阶段，非精确面力边界条件引起的误差占主导地位，未处理角点的结果明显劣于松弛处理后的结果；在经过若干次局部加密后，由于非精确边界条件的误差被显著稀释和削减，两者误差表现趋于一致。

![[Hu2021_Fig5_4.png]]

<center><b>
图 5.4：Cook 膜问题误差 $\|\sigma - \sigma(\widehat{\mathcal{T}})\|_{\mathbb{A}}$ 及估计子 $\eta$ 随自由度数（#dofs）的收敛历史对比
</b></center>

## 5.5 两种混合元自适应算法的比较

本算例在 L 形区域基准问题上比较文献 [24] 中的原始 $k=3$ 混合有限元与第 3.1 节提出的扩展嵌套混合有限元的自适应表现。结果展示于图 5.5 中。记 $\sigma(\widehat{\mathcal{T}})^O$ 与 $\eta^O$ 分别为原始单元的离散应力和总估计子，$\sigma(\widehat{\mathcal{T}})^E$ 与 $\eta^E$ 分别为扩展嵌套单元的对应结果。图 5.5 给出了两者的收敛历史对比曲线。数值结果表明，两族单元在自适应循环中的收敛速率和误差精度表现高度吻合、差别极小，这充分验证了本文提出的扩展嵌套混合有限元不仅在理论上具备严格的最优收敛性保证，而且在实际自适应计算中完全保持了原始混合元优异的高精度求解性能。

![[Hu2021_Fig5_5.png]]

<center><b>
图 5.5：L 形区域基准问题两种混合元自适应算法的误差 $\|\sigma - \sigma(\widehat{\mathcal{T}})\|_{\mathbb{A}}$ 及估计子 $\eta$ 随自由度数对比
</b></center>

---

# 基金资助

- 本文作者受国家自然科学基金项目（项目号：11625101、11421101）资助。

---

# 参考文献（References）

[1] S. Adams and B. Cockburn, A mixed finite element method for elasticity in three dimensions, *J. Sci. Comput.* 25 (2005), pp. 515–521.  
[2] D. N. Arnold and G. Awanou, Rectangular mixed finite elements for elasticity, *Math. Models Methods Appl. Sci.* 15 (2005), pp. 1417–1429.  
[3] D. N. Arnold, G. Awanou, and R. Winther, Finite elements for symmetric tensors in three dimensions, *Math. Comp.* 77 (2008), pp. 1229–1251.  
[4] D. N. Arnold, F. Brezzi, and J. Douglas, PEERS: A new mixed finite element for plane elasticity, *Jpn. J. Appl. Math.* 1 (1984), pp. 347–367.  
[5] D. N. Arnold, R. Falk, and R. Winther, Mixed finite element methods for linear elasticity with weakly imposed symmetry, *Math. Comp.* 76 (2007), pp. 1699–1723.  
[6] D. N. Arnold and R. Winther, Mixed finite elements for elasticity, *Numer. Math.* 92 (2002), pp. 401–419.  
[7] R. Becker and S. Mao, An optimally convergent adaptive mixed finite element method, *Numer. Math.* 111 (2008), pp. 35–54.  
[8] D. Boffi, F. Brezzi, and M. Fortin, Reduced symmetry elements in linear elasticity, *Commun. Pure Appl. Anal.* 8 (2009), pp. 95–121.  
[9] D. Boffi, F. Brezzi, and M. Fortin, *Mixed Finite Element Methods and Applications*, Springer, Heidelberg, 2013.  
[10] C. Carstensen, M. Feischl, M. Page, and D. Praetorius, Axioms of adaptivity, *Comput. Math. Appl.* 67 (2014), pp. 1195–1253.  
[11] C. Carstensen, D. Gallistl, and J. Gedicke, Residual-based a posteriori error analysis for symmetric mixed Arnold–Winther FEM, *Numer. Math.* 142 (2019), pp. 205–234.  
[12] C. Carstensen and J. Gedicke, Robust residual-based a posteriori Arnold–Winther mixed finite element analysis in elasticity, *Comput. Methods Appl. Mech. Engrg.* 300 (2016), pp. 245–264.  
[13] C. Carstensen, D. Günther, J. Reininghaus, and J. Thiele, The Arnold–Winther mixed FEM in linear elasticity. Part I: Implementation and numerical verification, *Comput. Methods Appl. Mech. Engrg.* 197 (2008), pp. 3014–3023.  
[14] C. Carstensen and R. H. W. Hoppe, Error reduction and convergence for an adaptive mixed finite element method, *Math. Comp.* 75 (2006), pp. 1033–1042.  
[15] C. Carstensen and J. Hu, An extended Argyris finite element method with optimal standard adaptive and multigrid V-cycle algorithms, preprint (2019), arXiv:1905.00688.  
[16] J. M. Cascon, C. Kreuzer, R. H. Nochetto, and K. G. Siebert, Quasi-optimal convergence rate for an adaptive finite element method, *SIAM J. Numer. Anal.* 46 (2008), pp. 2524–2550.  
[17] L. Chen, M. Holst, and J. Xu, Convergence and optimality of adaptive mixed finite element methods, *Math. Comp.* 78 (2009), pp. 35–53.  
[18] L. Chen, J. Hu, X. Huang, and H. Man, Residual-based a posteriori error estimates for symmetric conforming mixed finite elements for linear elasticity problems, *Sci. China Math.* 61 (2018), pp. 973–992.  
[19] V. Girault and L. R. Scott, Hermite interpolation of nonsmooth functions preserving boundary conditions, *Math. Comp.* 71 (2002), pp. 1043–1074.  
[20] H. C. Hu, On some variational principles in the theory of elasticity and the theory of plasticity, *Acta Phys. Sin.* 10 (1954), pp. 259–290.  
[21] J. Hu, Finite element approximations of symmetric tensors on simplicial grids in $\mathbb{R}^n$: The higher order case, *J. Comput. Math.* 33 (2015), pp. 283–296.  
[22] J. Hu, A new family of efficient conforming mixed finite elements on both rectangular and cuboid meshes for linear elasticity in the symmetric formulation, *SIAM J. Numer. Anal.* 53 (2015), pp. 1438–1463.  
[23] J. Hu and G. Yu, A unified analysis of quasi-optimal convergence for adaptive mixed finite element methods, *SIAM J. Numer. Anal.* 56 (2018), pp. 296–316.  
[24] J. Hu and S. Zhang, A family of conforming mixed finite elements for linear elasticity on triangular grids, preprint (2014), arXiv:1406.7457.  
[25] J. Hu and S. Zhang, A family of symmetric mixed finite elements for linear elasticity on tetrahedral grids, *Sci. China Math.* 58 (2015), pp. 297–307.  
[26] J. Hu and S. Zhang, Finite element approximations of symmetric tensors on simplicial grids in $\mathbb{R}^n$: The lower order case, *Math. Models Methods Appl. Sci.* 26 (2016), pp. 1649–1669.  
[27] J. Huang, X. Huang, and Y. Xu, Convergence of an adaptive mixed finite element method for Kirchhoff plate bending problems, *SIAM J. Numer. Anal.* 49 (2011), pp. 574–607.  
[28] J. Huang and Y. Xu, Convergence and complexity of arbitrary order adaptive mixed element methods for the Poisson equation, *Sci. China Math.* 55 (2012), pp. 1083–1098.  
[29] C. Johnson and B. Mercier, Some equilibrium finite element methods for two-dimensional elasticity problems, *Numer. Math.* 30 (1978), pp. 103–116.  
[30] R. Stevenson, The completion of locally refined simplicial partitions created by bisection, *Math. Comp.* 77 (2008), pp. 227–241.  
[31] X. Zhao, J. Hu, and Z. Shi, Convergence analysis of the adaptive finite element method with the red-green refinement, *Sci. China Math.* 53 (2010), pp. 499–512.
