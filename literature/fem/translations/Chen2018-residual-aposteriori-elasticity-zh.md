---
title: "翻译：Residual-based a posteriori error estimates for symmetric conforming mixed finite elements for linear elasticity problems"
tags:
  - translation
  - mixed-fem
  - elasticity
  - a-posteriori
  - hu-zhang-element
  - adaptive-fem
status: "read"
date_created: 2026-09-22
date_updated: 2026-09-22
source: "../sources/Chen2018-residual-aposteriori-elasticity.pdf"
citekey: "chenResidualbasedPosterioriError2018"
language: "zh-CN"
---

# Residual-based a posteriori error estimates for symmetric conforming mixed finite elements for linear elasticity problems

---

# 信息

- **中文标题**：线弹性问题对称协调混合有限元基于残差的后验误差估计
- **作者**：Long Chen（陈龙）；Jun Hu（胡俊）；Xuehai Huang（黄学海）；Hongying Man（满红英，通信作者）
- **单位**：
  1. 美国加利福尼亚大学欧文分校数学系（Department of Mathematics, University of California at Irvine, Irvine, CA 92697, USA）
  2. 北京大学数学科学学院，数学及其应用教育部重点实验室（LMAM and School of Mathematical Sciences, Peking University, Beijing 100871, China）
  3. 温州大学数学与信息科学学院（College of Mathematics and Information Science, Wenzhou University, Wenzhou 325035, China）
  4. 北京理工大学数学与统计学院（School of Mathematics and Statistics, Beijing Institute of Technology, Beijing 100081, China）
- **期刊**：*Science China Mathematics*（《中国科学：数学》英文版）
- **卷 / 期 / 页码**：61(6): 973–992，2018
- **接收日期**：2017-06-02；录用日期：2017-10-30；在线发表：2018-04-20
- **DOI**：[10.1007/s11425-017-9181-2](https://doi.org/10.1007/s11425-017-9181-2)
- **本地版本**：`literature/fem/sources/Chen2018-residual-aposteriori-elasticity.pdf`（SHA-256: `30de680284742dc4a28dbda55d228e845c3c962c164fa952af5417819fe9f59c`），20 页。本译文正文依据该原刊 PDF 全文完整翻译、整理与核对。

# 摘要

本文针对带有 Dirichlet 边界条件以及混合边界条件的平面线弹性问题，提出了对称混合有限元方法的基于残差的后验误差估计子。证明了所提后验误差估计子的可靠性（reliability，即可靠上界）与有效性/效率性（efficiency，即局部下界）。最后，给出了若干数值算例以验证理论分析结果。

**关键词**：对称混合有限元（symmetric mixed finite element），线弹性问题（linear elasticity problems），后验误差估计子（a posteriori error estimator），自适应方法（adaptive method）  
**MSC(2010) 主题分类**：65N30，73C02

---

# 1 引言

在本文中，我们致力于为平面线弹性问题的对称混合有限元方法建立基于残差的后验误差估计子。设 $\Omega \subset \mathbb{R}^2$ 为具有边界 $\Gamma := \partial\Omega$ 的有界多边形区域。基于 Hellinger-Reissner（H-R）变分原理，带有齐次 Dirichlet 边界条件的线弹性问题的应力-位移形式如下：求 $(\sigma, u) \in \Sigma \times V := \boldsymbol{H}(\mathrm{div}, \Omega; \mathbb{S}) \times L^2(\Omega; \mathbb{R}^2)$，使得
$$
\begin{cases}
(\mathcal{A}\sigma, \tau) + (\operatorname{div}\tau, u) = 0, & \forall \tau \in \Sigma, \\
(\operatorname{div}\sigma, v) = (f, v), & \forall v \in V,
\end{cases}
\tag{1.1}
$$
其中 $\mathbb{S} \subset \mathbb{R}^{2 \times 2}$ 为对称矩阵空间，应力的对称张量空间与位移的向量空间分别定义为
$$
\boldsymbol{H}(\operatorname{div}, \Omega; \mathbb{S}) := \{(\tau_{ij})_{2 \times 2} \in \boldsymbol{H}(\operatorname{div}, \Omega) \mid \tau_{12} = \tau_{21}\},
\tag{1.2}
$$
$$
L^2(\Omega; \mathbb{R}^2) := \{(u_1, u_2)^T \mid u_1, u_2 \in L^2(\Omega)\}.
\tag{1.3}
$$
表征材料性质的柔度张量（compliance tensor）$\mathcal{A}: \mathbb{S} \to \mathbb{S}$ 对称正定，且其特征值一致有上界。在齐次各向同性情形下，柔度张量由 $\mathcal{A}\tau = (\tau - \frac{\lambda}{2\mu + 2\lambda} \operatorname{tr}\tau \boldsymbol{I}) / (2\mu)$ 给出，其中 $\mu > 0$ 和 $\lambda \ge 0$ 为 Lamé 常数，$\boldsymbol{I}$ 为单位矩阵，$\operatorname{tr}\tau = \tau_{11} + \tau_{22}$ 为矩阵 $\tau$ 的迹。为简便起见，本文假定 $\mathcal{A}$ 为常矩阵，并将在后文评注推广到分片常矩阵的情形。

由于应力张量的对称性约束，即使对于二维问题，构造 (1.1) 的稳定协调有限元也是极其困难的，正如 Arnold 在 2002 年国际数学家大会（ICM）的大会报告中所述 [3]。为了克服这一困难，学者们发展了许多线弹性弱对称混合有限元方法（参见 [6, 7, 10, 21, 25]）。该方向的一项重要突破是 Arnold 与 Winther [8] 以及 Arnold 等人 [5] 的工作。特别是，这两篇文献提出了离散稳定方法的一个充分条件，指出离散复形的精确性可保证混合方法的稳定性。基于该条件，学者们在单纯形和矩形网格上针对二维和三维问题相继构造了协调混合有限元（参见 [1, 4, 5, 8, 9]）。近期，基于对称矩阵值分片多项式 $\boldsymbol{H}(\operatorname{div})$ 空间的一个关键结构以及两个基本代数结果，胡俊 [27, 28] 提出了一个设计与分析弹性力学混合有限元的新框架。由此，在单纯形网格和张量积网格上，构造出了在任意空间维数下均具有多项式形函数的最优对称混合有限元族（更多细节详见 [27–31]）。理论与数值分析表明，对称混合有限元方法是进行稳健应力逼近的流行选择（参见 [15, 17]）。

在过去的几十年中，基于自适应网格加密的计算已被证明是科学计算中有用且高效的工具。当求解区域包含凹角（re-entering corner）时，应力在角点处具有奇异性，必须采用非均匀自适应网格以捕捉奇异性。基于局部网格加密的自适应有限元方法能够恢复最优收敛阶。该技术背后的核心在于设计优良的后验误差估计子，从而为网格应当如何加密以及在何处加密提供明确指导。基于残差的后验误差估计子为网格的细化与粗化提供了局部指标，并允许控制整体误差是否低于给定阈值。针对 Poisson 方程混合有限元离散，已建立了各种后验误差估计子 [2, 13, 19, 22, 26, 33, 35]。然而，向线弹性混合有限元的推广却非常有限。在文献 [14, 32, 34] 中，作者们仅给出了非对称混合有限元的后验误差估计子。

应力张量的对称性给后验误差分析带来了本质困难。由于逼近的仅是对称部分而非全位移梯度，文献 [14, 18, 32, 34] 中发展的后验误差分析方法无法直接套用。为了克服这一困难，Carstensen 和 Gedicke [16] 提出通过将应力分解为位移梯度及梯度的非对称部分，从而将非对称混合有限元的后验分析框架推广到对称单元情形。文献 [16] 为 Arnold-Winther（AW）对称单元提出了一种稳健的基于残差的后验误差估计子，但该估计子中涉及对梯度非对称部分 $\operatorname{skew}(\operatorname{grad} u) = (\operatorname{grad} u - (\operatorname{grad} u)^T)/2$ 的任意非对称逼近 $\gamma_h$。此外，为了保证估计子的有效性，$\gamma_h$ 被选取为后处理位移的非对称梯度。

本文的目标是为文献 [8, 29]（亦见 [27, 31]）中发展的协调对称混合有限元解提出一种基于残差的后验误差估计子，并建立其理论上的上界（可靠性）与下界（有效性）。我们将遵循文献 [8] 中的指导原则：充分利用连续与离散的线弹性复形（参见 (2.2) 和 (2.3)）。

给定三角形剖分 $\mathcal{T}_h$ 上的有限元应力逼近 $\sigma_h$，我们构造如下记为 $\eta$ 的后验误差估计子：
$$
\eta^2(\sigma_h, \mathcal{T}_h) := \sum_{K \in \mathcal{T}_h} \eta_K^2(\sigma_h) + \sum_{e \in \mathcal{E}_h} \eta_e^2(\sigma_h),
$$
其中
$$
\eta_K^2(\sigma_h) := h_K^4 \|\operatorname{curl}\operatorname{curl}(\mathcal{A}\sigma_h)\|_{0,K}^2, \quad \eta_e^2(\sigma_h) := h_e \|J_{e,1}\|_{0,e}^2 + h_e^3 \|J_{e,2}\|_{0,e}^2,
$$
$$
J_{e,1} := \begin{cases}
[(\mathcal{A}\sigma_h)t_e \cdot t_e]_e, & \text{若 } e \in \mathcal{E}_h(\Omega), \\
((\mathcal{A}\sigma_h)t_e \cdot t_e)|_e, & \text{若 } e \in \mathcal{E}_h(\Gamma),
\end{cases}
$$
$$
J_{e,2} := \begin{cases}
[\operatorname{curl}(\mathcal{A}\sigma_h) \cdot t_e]_e, & \text{若 } e \in \mathcal{E}_h(\Omega), \\
(\operatorname{curl}(\mathcal{A}\sigma_h) \cdot t_e - \partial_{t_e}((\mathcal{A}\sigma_h)t_e \cdot \nu_e))|_e, & \text{若 } e \in \mathcal{E}_h(\Gamma),
\end{cases}
$$
$\mathcal{E}_h$ 为 $\mathcal{T}_h$ 的所有边构成的集合。我们记 $\mathcal{E}_h = \mathcal{E}_h(\Omega) \cup \mathcal{E}_h(\Gamma)$，其中 $\mathcal{E}_h(\Omega)$ 为内部边集合，$\mathcal{E}_h(\Gamma)$ 为位于边界上的单元边集合。对于任意边 $e \in \mathcal{E}_h$，设 $\nu_e = (n_1, n_2)^T$ 为单位外法向量，$t_e = (-n_2, n_1)^T$ 为沿边 $e$ 的单位切向量。令 $h_K$ 为单元 $K$ 的直径，$h_e$ 为边 $e$ 的长度。数据震荡（data oscillation）定义为
$$
\operatorname{osc}^2(f, \mathcal{T}_h) := \sum_{K \in \mathcal{T}_h} h_K^2 \|f - Q_h f\|_{0,K}^2,
$$
其中 $Q_h$ 是到离散位移空间上的 $L^2$ 正交投影算子。

利用线弹性微分复形导出的 Helmholtz 分解（参见 [8, 14]），我们建立了如下可靠性上界估计：
$$
\|\sigma - \sigma_h\|_{\mathcal{A}} \le C_1 (\eta(\sigma_h, \mathcal{T}_h) + \operatorname{osc}(f, \mathcal{T}_h)).
$$
此外，遵循 Alonso [2] 的方法，我们证明了如下效率性下界估计：
$$
C_2 \eta(\sigma_h, \mathcal{T}_h) \le \|\sigma - \sigma_h\|_{\mathcal{A}}.
$$
我们还将上述结论推广到了混合边界值问题，其中误差估计子在 Dirichlet 边界边上进行了相应修正，修正后估计子的可靠性与有效性可类似获证。

在文献 [20] 中，作者通过对 $(\sigma_h, u_h)$ 进行后处理构造了一个超收敛近似位移 $u_h^*$。利用该结果以及应力的后验误差估计，我们在一个网格依赖范数下给出了位移误差 $\|u - u_h^*\|_{1,h}$ 的后验误差估计。

为了与文献 [16] 中的后验误差估计子进行对比，我们将其估计子重述如下：
$$
\begin{aligned}
\widetilde{\eta}^2(\sigma_h, \mathcal{T}_h) := &\operatorname{osc}^2(f, \mathcal{T}_h) + \operatorname{osc}^2(g, \mathcal{E}_h(\Gamma_N)) + \sum_{K \in \mathcal{T}_h} h_K^2 \|\operatorname{curl}(\mathcal{A}\sigma_h + \gamma_h)\|_{0,K}^2 \\
&+ \sum_{e \in \mathcal{E}_h(\Omega)} h_e \|[\mathcal{A}\sigma_h + \gamma_h]_e \tau_e\|_{0,e}^2 + \sum_{e \in \mathcal{E}_h(\Gamma_D)} h_e \|(\mathcal{A}\sigma_h + \gamma_h - \nabla u_D)\tau_e\|_{0,e}^2.
\end{aligned}
$$
为了保证该估计子的有效性，上述估计子中引入了非对称梯度 $\operatorname{skew}(\operatorname{grad} u)$ 的一个足够精确的多项式非对称逼近 $\gamma_h$。由于全局逼近甚至极小化可能计算代价过高，Carstensen 和 Gedicke [16] 借鉴 Stenberg [38] 的思想，通过后处理位移 $u_h^*$ 计算该充分精确的逼近 $\gamma_h = \operatorname{skew}(\operatorname{grad} u_h^*)$。显而易见，文献 [16] 的估计子与本文提出的估计子截然不同。本文提出的估计子直接利用对称应力张量，完全不需要对非对称部分进行任何逼近，因此在计算上更为高效。

本文剩余部分结构安排如下：第 2 节介绍记号与离散有限元问题；第 3 节提出应力的后验误差估计子并证明其可靠性与有效性；第 4 节将第 3 节的结论推广至混合边界值问题；第 5 节给出位移的后验误差估计；第 6 节给出数值实验以验证估计子的有效性。全文通篇使用记号 “$\lesssim \cdots$” 表示 “$\le C \cdots$”，其中 $C$ 为与网格尺寸 $h$ 及 Lamé 常数 $\lambda$ 均无关的通用常数，在不同出现处其取值可不同。

---

# 2 记号与预备知识

全文通篇采用关于 Sobolev 空间与范数的标准记号。为简便起见，记 $\|\cdot\| := \|\cdot\|_{L^2(\Omega)}$ 为 $L^2$ 范数。$(\cdot, \cdot)_K$ 表示区域 $K$ 上的标准 $L^2$ 内积，当 $K = \Omega$ 时下标通常省略。$\langle \cdot, \cdot \rangle_\Gamma$ 表示边界 $\Gamma$ 上的 $L^2$ 内积。简记 $\partial_{x_i} := \partial/\partial x_i$，$\partial_{x_i x_j}^2 := \partial^2/\partial x_i \partial x_j$（$j=1,2$），$\partial_\nu := \partial/\partial \nu$，$\partial_t := \partial/\partial t$。对于标量函数 $\phi \in H^1(\Omega; \mathbb{R})$ 及向量函数 $v = (v_1, v_2)^T \in H^1(\Omega; \mathbb{R}^2)$，定义
$$
\operatorname{Curl}\phi := \left(-\frac{\partial \phi}{\partial x_2}, \frac{\partial \phi}{\partial x_1}\right), \quad \operatorname{Curl}v := \begin{pmatrix} -\partial v_1/\partial x_2 & \partial v_1/\partial x_1 \\ -\partial v_2/\partial x_2 & \partial v_2/\partial x_1 \end{pmatrix}.
$$
向量场 $v$ 梯度的对称部分记为 $\varepsilon(v)$，定义为
$$
\varepsilon(v) := \frac{1}{2}(\operatorname{grad} v + (\operatorname{grad} v)^T).
$$
对于张量函数 $\tau = (\tau_{ij})_{2 \times 2} \in H^1(\Omega; \mathbb{R}^{2 \times 2})$，定义
$$
\operatorname{curl}\tau := \begin{pmatrix} \partial \tau_{12}/\partial x_1 - \partial \tau_{11}/\partial x_2 \\ \partial \tau_{22}/\partial x_1 - \partial \tau_{21}/\partial x_2 \end{pmatrix}, \quad \operatorname{div}\tau := \begin{pmatrix} \partial \tau_{11}/\partial x_1 + \partial \tau_{12}/\partial x_2 \\ \partial \tau_{21}/\partial x_1 + \partial \tau_{22}/\partial x_2 \end{pmatrix},
$$
即微分算子 $\operatorname{curl}$ 和 $\operatorname{div}$ 是逐行作用在张量上的。

设 $\mathcal{T}_h$ 为由三角形组成的 $\bar{\Omega}$ 的形状正则剖分，其边集记为 $\mathcal{E}_h$。用 $\mathcal{E}_h(\Omega)$ 表示所有内部边的集合，$\mathcal{E}_h(\Gamma)$ 表示边界 $\Gamma$ 上的所有单元边的集合。对于任意三角形 $K \in \mathcal{T}_h$，记 $E(K)$ 为其边集。对于任意边 $e \in E(K)$，设 $\nu_e = (n_1, n_2)^T$ 为单位外法向量，$t_e = (-n_2, n_1)^T$ 为沿边 $e$ 的单位切向量，$h_K$ 为单元 $K$ 的直径，$h_e$ 为边 $e$ 的长度，$h = \max_{K \in \mathcal{T}_h}\{h_K\}$ 为剖分 $\mathcal{T}_h$ 的最大网格尺寸。量 $w$ 跨越公共边 $e = \bar{K}_+ \cap \bar{K}_-$ 的跳跃定义为
$$
[w]_e := (w|_{K_+})_e - (w|_{K_-})_e.
$$
特别地，若 $e \in \mathcal{E}_h(\Gamma)$，则规定 $[w]_e := w|_e$。

设 $\Sigma_h \times V_h \subseteq \Sigma \times V$ 为定义在网格 $\mathcal{T}_h$ 上的对称协调混合有限元空间。则问题 (1.1) 的离散混合有限元格式为：求 $(\sigma_h, u_h) \in \Sigma_h \times V_h$，使得
$$
\begin{cases}
(\mathcal{A}\sigma_h, \tau_h) + (\operatorname{div}\tau_h, u_h) = 0, & \forall \tau_h \in \Sigma_h, \\
(\operatorname{div}\sigma_h, v_h) = (f, v_h), & \forall v_h \in V_h.
\end{cases}
\tag{2.1}
$$

下文简要介绍胡-张（Hu-Zhang）单元（参见 [27, 29, 31]）。对于每个 $K \in \mathcal{T}_h$，设 $P_k(K)$ 为 $K$ 上总次数不超过 $k$ 的多项式空间，定义
$$
P_k(K; \mathbb{S}) := \{\tau \in L^2(K; \mathbb{R}^{2 \times 2}) \mid \tau_{ij} \in P_k(K), \tau_{ij} = \tau_{ji}, 1 \le i \le 2, 1 \le j \le 2\},
$$
$$
P_k(K; \mathbb{R}^2) := \{v \in L^2(K; \mathbb{R}^2) \mid v_i \in P_k(K), 1 \le i \le 2\}.
$$
定义 $\boldsymbol{H}(\operatorname{div}, K; \mathbb{S})$ 泡函数空间为
$$
B_{K,k} := \{\tau \in P_k(K; \mathbb{S}) : \tau \nu|_{\partial K} = 0\}.
$$
胡-张混合有限元空间由以下形式给出：
$$
\Sigma_h := \widetilde{\Sigma}_{k,h} + B_{k,h},
$$
$$
V_h := \{v \in L^2(\Omega; \mathbb{R}^2) : v|_K \in P_{k-1}(K; \mathbb{R}^2), \forall K \in \mathcal{T}_h\},
$$
其中整数 $k \ge 3$，且
$$
B_{k,h} := \{\tau \in \boldsymbol{H}(\operatorname{div}, \Omega; \mathbb{S}) : \tau|_K \in B_{K,k}, \forall K \in \mathcal{T}_h\},
$$
$$
\widetilde{\Sigma}_{k,h} := \{\tau \in H^1(\Omega; \mathbb{S}) : \tau|_K \in P_k(K; \mathbb{S}), \forall K \in \mathcal{T}_h\}.
$$

对于上述单元，具有如下先验误差估计：

> **定理 2.1（先验误差估计，参见 [27, 29, 31]）**  
> 设 $(\sigma, u)$ 为 (1.1) 的精确解，$(\sigma_h, u_h)$ 为 (2.1) 的离散近似解。则满足
> $$
> \|\sigma - \sigma_h\|_0 \lesssim h^m \|\sigma\|_m, \quad 1 \le m \le k+1,
> $$
> $$
> \|\operatorname{div}(\sigma - \sigma_h)\|_0 \lesssim h^m \|\operatorname{div}\sigma\|_m, \quad 0 \le m \le k,
> $$
> $$
> \|u - u_h\|_0 \lesssim h^m \|u\|_{m+1}, \quad 1 \le m \le k.
> $$

在连续情形下，线弹性问题的如下复形为正合序列（exact sequence，参见 [8]）：
$$
P_1(\Omega) \longrightarrow H^2(\Omega) \xrightarrow{\operatorname{Curl}\operatorname{Curl}} \boldsymbol{H}(\operatorname{div}, \Omega; \mathbb{S}) \xrightarrow{\operatorname{div}} L^2(\Omega; \mathbb{R}^2).
\tag{2.2}
$$
在离散情形下，类似地有如下离散正合序列：
$$
P_1(\Omega) \longrightarrow \Phi_h \xrightarrow{\operatorname{Curl}\operatorname{Curl}} \Sigma_h \xrightarrow{\operatorname{div}} V_h.
\tag{2.3}
$$
正如文献 [8] 所指出的，对于 Arnold-Winther 单元，空间 $\Phi_h$ 恰好是在顶点处具有 $C^2$ 连续性的 $C^1$ 分片多项式空间，即著名的高阶 Hermite 或 Argyris 有限元空间。胡-张单元则是 Arnold-Winther 单元的富集，它在每个单元上添加了所有次数为 $k$ 且全局属于 $\boldsymbol{H}(\operatorname{div}, \Omega; \mathbb{S})$ 但不必无散度的分片多项式矩阵。因此，胡-张单元对应的势函数空间 $\Phi_h$ 与 Arnold-Winther 单元完全相同。

> **引理 2.2（Helmholtz 型分解，参见 [8, 14]）**  
> 对于任意 $\tau \in L^2(\Omega; \mathbb{S})$，存在 $v \in H_0^1(\Omega; \mathbb{R}^2)$ 及 $\phi \in H^2(\Omega)/P_1(\Omega)$，使得
> $$
> \tau = \mathcal{C}\varepsilon(v) + \operatorname{Curl}\operatorname{Curl}\phi,
> \tag{2.4}
> $$
> 并且该分解在加权 $L^2$ 内积 $(\mathcal{C}^{-1}\cdot, \cdot) := (\mathcal{A}\cdot, \cdot)$ 下是正交的，即
> $$
> \|\tau\|_{\mathcal{A}}^2 = \|\varepsilon(v)\|_{\mathcal{A}^{-1}}^2 + \|\operatorname{Curl}\operatorname{Curl}\phi\|_{\mathcal{A}}^2,
> \tag{2.5}
> $$
> 其中 $P_1(\Omega)$ 是 $\Omega$ 上的线性多项式空间，范数定义为 $\|\cdot\|_{\mathcal{A}}^2 = (\mathcal{A}\cdot, \cdot)$。

注意到 $(\mathcal{A}^{-1}\mathcal{A}\tau, \tau) = (\tau, \tau) = (\mathcal{A}(\mathcal{A}^{-1}\tau), \tau)$，利用算子 $\mathcal{A}$ 的有界性与矫顽性，可得如下范数等价关系：对于任意 $\tau \in \Sigma$，存在与 Lamé 常数 $\lambda$ 无关的正常数 $C_1, C_2$，使得
$$
C_2 \|\tau\|_{\mathcal{A}}^2 = C_2 (\mathcal{A}\tau, \tau) \le \|\tau\|_0^2 \le C_1 (\mathcal{A}^{-1}\tau, \tau) = C_1 \|\tau\|_{\mathcal{A}^{-1}}^2.
\tag{2.6}
$$

本文的核心目标是为胡-张有限元方法建立 $\sigma - \sigma_h$ 的后验误差估计。值得一提的是，本文所设计的后验误差估计子可极其直接地推广至 Arnold-Winther 单元（参见 [8]）。

---

# 3 应力的后验误差估计

在本节中，我们将证明误差估计子的可靠性与有效性。主要观察在于：尽管原问题是鞍点问题，但应力误差 $\sigma - \sigma_h$ 正交于无散子空间，而误差中非无散的部分则可利用离散系统的稳定性由数据震荡所控制。

对于任意 $\tau_h \in \Sigma_h$，误差估计子定义为
$$
\eta^2(\tau_h, \mathcal{T}_h) := \sum_{K \in \mathcal{T}_h} \eta_K^2(\tau_h) + \sum_{e \in \mathcal{E}_h} \eta_e^2(\tau_h),
\tag{3.1}
$$
其中
$$
\eta_K^2(\tau_h) := h_K^4 \|\operatorname{curl}\operatorname{curl}(\mathcal{A}\tau_h)\|_{0,K}^2, \quad \eta_e^2(\tau_h) := h_e \|J_{e,1}\|_{0,e}^2 + h_e^3 \|J_{e,2}\|_{0,e}^2,
$$
$$
J_{e,1} := \begin{cases}
[(\mathcal{A}\tau_h)t_e \cdot t_e]_e, & \text{若 } e \in \mathcal{E}_h(\Omega), \\
((\mathcal{A}\tau_h)t_e \cdot t_e)|_e, & \text{若 } e \in \mathcal{E}_h(\Gamma),
\end{cases}
$$
$$
J_{e,2} := \begin{cases}
[\operatorname{curl}(\mathcal{A}\tau_h) \cdot t_e]_e, & \text{若 } e \in \mathcal{E}_h(\Omega), \\
(\operatorname{curl}(\mathcal{A}\tau_h) \cdot t_e - \partial_{t_e}((\mathcal{A}\tau_h)t_e \cdot \nu_e))|_e, & \text{若 } e \in \mathcal{E}_h(\Gamma).
\end{cases}
$$
数据震荡定义为
$$
\operatorname{osc}^2(f, \mathcal{T}_h) := \sum_{K \in \mathcal{T}_h} h_K^2 \|f - Q_h f\|_{0,K}^2,
$$
其中 $Q_h$ 是到离散位移空间 $V_h$ 上的 $L^2$ 正交投影算子。

## 3.1 稳定性结果

为叙述简便，将线弹性混合形式简记为 $\mathcal{L}(\sigma, u) = f$。算子的自然稳定性为 $\|\sigma\|_{\boldsymbol{H}(\operatorname{div})} + \|u\| \lesssim \|f\|$。然而，针对一类特殊的数据摄动，可以证明更强的稳定性。

> **引理 3.1**  
> 设 $f_h$ 为 $f$ 到 $V_h$ 上的 $L^2$ 投影，令 $(\sigma, u) = \mathcal{L}^{-1}f$ 以及 $(\widetilde{\sigma}, \widetilde{u}) = \mathcal{L}^{-1}f_h$。则有
> $$
> \|\sigma - \widetilde{\sigma}\|_{\mathcal{A}} \lesssim \operatorname{osc}(f, \mathcal{T}_h).
> \tag{3.2}
> $$

*证明*：利用 (1.1) 的第一个方程并令 $v = u - \widetilde{u}$，
$$
\begin{aligned}
(\mathcal{A}(\sigma - \widetilde{\sigma}), \sigma - \widetilde{\sigma}) &= -(\operatorname{div}(\sigma - \widetilde{\sigma}), u - \widetilde{u}) = -(f - Q_h f, u - \widetilde{u}) \\
&= (f - Q_h f, Q_h v - v) \\
&\le \sum_{K \in \mathcal{T}_h} \|f - Q_h f\|_{0,K} \|v - Q_h v\|_{0,K} \\
&\lesssim \sum_{K \in \mathcal{T}_h} \|f - Q_h f\|_{0,K} h_K |v|_{1,K} \\
&\lesssim \left(\sum_{K \in \mathcal{T}_h} h_K^2 \|f - Q_h f\|_{0,K}^2\right)^{1/2} \|\varepsilon(v)\|_0,
\end{aligned}
$$
此处利用了 Korn 不等式。由于 $\varepsilon(v) = \mathcal{A}(\sigma - \widetilde{\sigma})$，由 (2.6) 可知
$$
\|\varepsilon(v)\|_0 \lesssim \|\sigma - \widetilde{\sigma}\|_{\mathcal{A}}.
$$
由此即得到所需的稳定性估计。  
证毕。

震荡项 $\operatorname{osc}(f, \mathcal{T}_h)$ 是 $\|f - f_h\|_{-1}$ 的上界，且相比于误差估计子是高阶小量。

## 3.2 正交性

对于任意 $\phi \in H^2(\Omega)$，有 $\operatorname{Curl}\operatorname{Curl}\phi \in \boldsymbol{H}(\operatorname{div}, \Omega; \mathbb{S})$。利用正合序列性质 $\operatorname{div}\operatorname{Curl}\operatorname{Curl} = 0$，可得
$$
(\mathcal{A}\widetilde{\sigma}, \operatorname{Curl}\operatorname{Curl}\phi) = -(\widetilde{u}, \operatorname{div}\operatorname{Curl}\operatorname{Curl}\phi) = 0.
\tag{3.3}
$$
类似地，对于任意 $\phi_h \in \Phi_h$，有
$$
(\mathcal{A}\sigma_h, \operatorname{Curl}\operatorname{Curl}\phi_h) = -(u_h, \operatorname{div}\operatorname{Curl}\operatorname{Curl}\phi_h) = 0.
$$
因此，我们享有部分正交性：
$$
(\mathcal{A}(\widetilde{\sigma} - \sigma_h), \operatorname{Curl}\operatorname{Curl}\phi_h) = 0, \quad \forall \phi_h \in \Phi_h.
\tag{3.4}
$$

## 3.3 可靠性上界

记 $S_h^5$ 为 Argyris 有限元空间，由次数不超过 5 的 $C^1$ 分片多项式构成，即
$$
\begin{aligned}
S_h^5 := \{&v \in L^2(\bar{\Omega}) : v|_K \in P_5(K), \forall K \in \mathcal{T}_h, \\
&v \text{ 及其一阶和二阶偏导数在网格顶点处均连续}, \\
&v \text{ 在边中点处沿法向导数连续}\}.
\end{aligned}
$$
遵循文献 [23, 37]，我们可以定义准插值算子 $\mathcal{I}_h: H^2(\Omega) \to S_h^5$，该算子保持函数在 $\mathcal{T}_h$ 所有顶点处的取值。在每个单元 $K \in \mathcal{T}_h$ 上，对任意 $v \in H^2(\Omega)$，$\mathcal{I}_h v|_K \in P_5(K)$ 且满足：
- $\mathcal{I}_h v|_K(a_{i,K}) = v(a_{i,K}), \quad 1 \le i \le 3$;
- $\partial_{x_j}(\mathcal{I}_h v|_K)(a_{i,K}) = N_h^{-1}(a_{i,K}) \sum_{K' \in S(a_{i,K})} \partial_{x_j}(P_h v|_{K'})(a_{i,K}), \quad 1 \le i \le 3, j = 1, 2$;
- $\partial_{x_j x_l}^2(\mathcal{I}_h v|_K)(a_{i,K}) = N_h^{-1}(a_{i,K}) \sum_{K' \in S(a_{i,K})} \partial_{x_j x_l}^2(P_h v|_{K'})(a_{i,K}), \quad 1 \le i \le 3, 1 \le j \le l \le 2$;
- $\partial_\nu(\mathcal{I}_h v|_K)(a_{3+i,K}) = N_h^{-1}(a_{3+i,K}) \sum_{K' \in S(a_{3+i,K})} \partial_\nu(P_h v|_{K'})(a_{3+i,K}), \quad 1 \le i \le 3$,

其中 $a_{i,K}$（$1 \le i \le 3$）为 $K$ 的顶点，$a_{3+i,K}$（$1 \le i \le 3$）为 $K$ 的边中点，$\nu$ 为单元 $K$ 在边中点处的外法向，
$$
S(a_{i,K}) := \bigcup \{K' \in \mathcal{T}_h : a_{i,K} \in K'\}, \quad N_h(a_{i,K}) := \operatorname{card}\{K' : K' \in S(a_{i,K})\},
$$
$P_h$ 是从 $L^2(\Omega)$ 到 $\mathcal{T}_h$ 上次数不超过 5 的间断多项式空间上的 $L^2$ 投影算子。显然，插值算子 $\mathcal{I}_h$ 由上述自由度唯一确定。进一步，$\mathcal{I}_h$ 具有投影性质，即
$$
\mathcal{I}_h v = v, \quad \forall v \in S_h^5,
\tag{3.5}
$$
并且对任意 $v \in H^2(\Omega)$，它保持顶点处的函数值不变：
$$
\mathcal{I}_h v(a_{i,K}) = v(a_{i,K}), \quad \forall K \in \mathcal{T}_h, 1 \le i \le 3.
\tag{3.6}
$$
类似于文献 [23, 37] 中的缩放论证，可得如下插值估计：
$$
|v - \mathcal{I}_h v|_{m,K} \lesssim h_K^{2-m} |v|_{2, S_K}, \quad 0 \le m \le 2, \forall K \in \mathcal{T}_h,
\tag{3.7}
$$
$$
|v - \mathcal{I}_h v|_{m,e} \lesssim h_e^{2-m-1/2} |v|_{2, S_e}, \quad 0 \le m \le 1, \forall e \in \mathcal{E}_h,
\tag{3.8}
$$
其中 $S_K = \bigcup \{K_i \in \mathcal{T}_h : K_i \cap K \ne \emptyset\}$，$S_e = \bigcup \{K_i \in \mathcal{T}_h : K_i \cap e \ne \emptyset\}$。

将 Helmholtz 分解应用于误差 $\widetilde{\sigma} - \sigma_h$，由于 $\operatorname{div}(\widetilde{\sigma} - \sigma_h) = f_h - f_h = 0$，其位移部分为零，故有
$$
\widetilde{\sigma} - \sigma_h = \mathcal{C}\varepsilon(v) + \operatorname{Curl}\operatorname{Curl}\phi = \operatorname{Curl}\operatorname{Curl}\phi
\tag{3.9}
$$
以及
$$
\|\operatorname{Curl}\operatorname{Curl}\phi\|_{\mathcal{A}} = \|\widetilde{\sigma} - \sigma_h\|_{\mathcal{A}},
\tag{3.10}
$$
其中 $\phi \in H^2(\Omega)/P_1(\Omega)$。由此推得
$$
\|\widetilde{\sigma} - \sigma_h\|_{\mathcal{A}}^2 = (\mathcal{A}(\widetilde{\sigma} - \sigma_h), \operatorname{Curl}\operatorname{Curl}\phi).
$$
由于 $\operatorname{Curl}\operatorname{Curl}(\mathcal{I}_h \phi) \in \Sigma_h$，由正交性 (3.4) 与方程 (3.3)，
$$
\begin{aligned}
(\mathcal{A}(\widetilde{\sigma} - \sigma_h), \operatorname{Curl}\operatorname{Curl}\phi) &= (\mathcal{A}(\widetilde{\sigma} - \sigma_h), \operatorname{Curl}\operatorname{Curl}(\phi - \mathcal{I}_h \phi)) \\
&= -(\mathcal{A}\sigma_h, \operatorname{Curl}\operatorname{Curl}(\phi - \mathcal{I}_h \phi)).
\end{aligned}
$$
进行分部积分得：
$$
\begin{aligned}
(\mathcal{A}\sigma_h, \operatorname{Curl}\operatorname{Curl}(\phi - \mathcal{I}_h \phi)) = &-\sum_{K \in \mathcal{T}_h} (\operatorname{curl}(\mathcal{A}\sigma_h), \operatorname{Curl}(\phi - \mathcal{I}_h \phi))_K + \sum_{K \in \mathcal{T}_h} \langle (\mathcal{A}\sigma_h)t, \operatorname{Curl}(\phi - \mathcal{I}_h \phi)\rangle_{\partial K} \\
= &\sum_{K \in \mathcal{T}_h} (\operatorname{curl}\operatorname{curl}(\mathcal{A}\sigma_h), \phi - \mathcal{I}_h \phi)_K - \sum_{K \in \mathcal{T}_h} \langle \operatorname{curl}(\mathcal{A}\sigma_h) \cdot t, \phi - \mathcal{I}_h \phi\rangle_{\partial K} \\
&+ \sum_{K \in \mathcal{T}_h} \langle (\mathcal{A}\sigma_h)t, \operatorname{Curl}(\phi - \mathcal{I}_h \phi)\rangle_{\partial K}.
\end{aligned}
\tag{3.11}
$$
等号右端第二项可以改写为：
$$
\sum_{K \in \mathcal{T}_h} \langle \mathcal{A}\sigma_h t, \operatorname{Curl}(\phi - \mathcal{I}_h \phi)\rangle_{\partial K} = \sum_{K \in \mathcal{T}_h} \langle (\mathcal{A}\sigma_h)t \cdot t, \operatorname{Curl}(\phi - \mathcal{I}_h \phi) \cdot t\rangle_{\partial K} + \sum_{K \in \mathcal{T}_h} \langle (\mathcal{A}\sigma_h t) \cdot \nu, \operatorname{Curl}(\phi - \mathcal{I}_h \phi) \cdot \nu\rangle_{\partial K}.
$$
因为柔度张量 $\mathcal{A}$ 是对称且连续的，$(\mathcal{A}\sigma_h t) \cdot \nu = (\mathcal{A}\sigma_h \nu) \cdot t = (t^T \sigma_h \nu)/(2\mu)$，且 $(\mathcal{A}\sigma_h t) \cdot \nu$ 跨越内部单元边是连续的，这意味着：
$$
\begin{aligned}
\sum_{K \in \mathcal{T}_h} \langle (\mathcal{A}\sigma_h t) \cdot \nu, \operatorname{Curl}(\phi - \mathcal{I}_h \phi) \cdot \nu\rangle_{\partial K} &= -\sum_{e \in \mathcal{E}_h(\Gamma)} \langle (\mathcal{A}\sigma_h t_e) \cdot \nu_e, \partial_{t_e}(\phi - \mathcal{I}_h \phi)\rangle_e \\
&= \sum_{e \in \mathcal{E}_h(\Gamma)} \langle \partial_{t_e}((\mathcal{A}\sigma_h t_e) \cdot \nu_e), \phi - \mathcal{I}_h \phi\rangle_e,
\end{aligned}
$$
此处利用了 $\phi - \mathcal{I}_h \phi$ 在网格顶点处消失的事实 (3.6)。因此，
$$
\begin{aligned}
\sum_{K \in \mathcal{T}_h} \langle \mathcal{A}\sigma_h t, \operatorname{Curl}(\phi - \mathcal{I}_h \phi)\rangle_{\partial K} = &\sum_{e \in \mathcal{E}_h(\Omega)} \langle [(\mathcal{A}\sigma_h t_e) \cdot t_e]_e, \partial_{\nu_e}(\phi - \mathcal{I}_h \phi)\rangle_e \\
&+ \sum_{e \in \mathcal{E}_h(\Gamma)} \langle (\mathcal{A}\sigma_h t_e) \cdot t_e, \partial_{\nu_e}(\phi - \mathcal{I}_h \phi)\rangle_e \\
&+ \sum_{e \in \mathcal{E}_h(\Gamma)} \langle \partial_{t_e}((\mathcal{A}\sigma_h t_e) \cdot \nu_e), \phi - \mathcal{I}_h \phi\rangle_e.
\end{aligned}
$$
代入 (3.11) 可得：
$$
\begin{aligned}
(\mathcal{A}\sigma_h, \operatorname{Curl}\operatorname{Curl}(\phi - \mathcal{I}_h \phi)) = &\sum_{K \in \mathcal{T}_h} (\operatorname{curl}\operatorname{curl}(\mathcal{A}\sigma_h), \phi - \mathcal{I}_h \phi)_K \\
&+ \sum_{e \in \mathcal{E}_h(\Omega)} \langle [(\mathcal{A}\sigma_h t_e) \cdot t_e]_e, \partial_{\nu_e}(\phi - \mathcal{I}_h \phi)\rangle_e \\
&- \sum_{e \in \mathcal{E}_h(\Omega)} \langle [\operatorname{curl}(\mathcal{A}\sigma_h) \cdot t_e]_e, \phi - \mathcal{I}_h \phi\rangle_e \\
&+ \sum_{e \in \mathcal{E}_h(\Gamma)} \langle (\mathcal{A}\sigma_h t_e) \cdot t_e, \partial_{\nu_e}(\phi - \mathcal{I}_h \phi)\rangle_e \\
&+ \sum_{e \in \mathcal{E}_h(\Gamma)} \langle \partial_{t_e}((\mathcal{A}\sigma_h t_e) \cdot \nu_e) - \operatorname{curl}(\mathcal{A}\sigma_h) \cdot t_e, \phi - \mathcal{I}_h \phi\rangle_e,
\end{aligned}
$$
从而有
$$
\begin{aligned}
\|\widetilde{\sigma} - \sigma_h\|_{\mathcal{A}}^2 &= (\mathcal{A}(\widetilde{\sigma} - \sigma_h), \operatorname{Curl}\operatorname{Curl}\phi) \\
&\lesssim \left[\sum_{K \in \mathcal{T}_h} h_K^4 \|\operatorname{curl}\operatorname{curl}(\mathcal{A}\sigma_h)\|_{0,K}^2 + \sum_{e \in \mathcal{E}_h} (h_e \|J_{e,1}\|_{0,e}^2 + h_e^3 \|J_{e,2}\|_{0,e}^2)\right]^{1/2} |\phi|_{2} \\
&\lesssim \left[\sum_{K \in \mathcal{T}_h} \eta_K^2(\sigma_h) + \sum_{e \in \mathcal{E}_h} \eta_e^2(\sigma_h)\right]^{1/2} \|\operatorname{Curl}\operatorname{Curl}\phi\|_0.
\end{aligned}
\tag{3.12}
$$
由文献 [14]，(3.9) 中定义的 $\phi$ 满足 $\operatorname{div}(\operatorname{Curl}\operatorname{Curl}\phi) = 0$ 且
$$
\int_\Omega \operatorname{tr}(\operatorname{Curl}\operatorname{Curl}\phi) \, dx = \int_\Omega \operatorname{tr}(\widetilde{\sigma} - \sigma_h) \, dx = 0.
$$
利用文献 [11, Proposition 9.1.1]，可知
$$
\|\operatorname{Curl}\operatorname{Curl}\phi\|_0 \le C \|\operatorname{Curl}\operatorname{Curl}\phi\|_{\mathcal{A}},
$$
其中常数 $C$ 与 Lamé 常数 $\lambda$ 无关。将其与 (3.10) 和 (3.12) 结合，得到
$$
\|\widetilde{\sigma} - \sigma_h\|_{\mathcal{A}} \lesssim \left[\sum_{K \in \mathcal{T}_h} \eta_K^2(\sigma_h) + \sum_{e \in \mathcal{E}_h} \eta_e^2(\sigma_h)\right]^{1/2}.
$$
结合三角不等式与摄动结果 (3.2)，即导出期望的误差上界：
$$
\begin{aligned}
\|\sigma - \sigma_h\|_{\mathcal{A}} &\le \|\sigma - \widetilde{\sigma}\|_{\mathcal{A}} + \|\widetilde{\sigma} - \sigma_h\|_{\mathcal{A}} \\
&\lesssim \left[\sum_{K \in \mathcal{T}_h} \eta_K^2(\sigma_h) + \sum_{e \in \mathcal{E}_h} \eta_e^2(\sigma_h)\right]^{1/2} + \operatorname{osc}(f, \mathcal{T}_h).
\end{aligned}
$$

综上所述，我们证明了如下可靠性上界定理：

> **定理 3.2（误差估计子的可靠性）**  
> 设 $(\sigma, u)$ 为混合问题 (1.1) 的解，$(\sigma_h, u_h)$ 为混合有限元格式 (2.1) 的解。若柔度张量 $\mathcal{A}$ 连续，则存在仅依赖于三角形网格的形状正则性以及多项式阶数 $k$ 的正常数 $C_1$，使得
> $$
> \|\sigma - \sigma_h\|_{\mathcal{A}} \le C_1 (\eta(\sigma_h, \mathcal{T}_h) + \operatorname{osc}(f, \mathcal{T}_h)).
> \tag{3.13}
> $$

> **注 3.3（分片常数/不连续 $\mathcal{A}$ 的修正）**  
> 当柔度张量 $\mathcal{A}$ 为分片常数（不连续）时，可将 $\eta(\sigma_h, \mathcal{T}_h)$ 修正如下：
> $$
> \eta^2(\sigma_h, \mathcal{T}_h) := \sum_{K \in \mathcal{T}_h} h_K^4 \|\operatorname{curl}\operatorname{curl}(\mathcal{A}\sigma_h)\|_{0,K}^2 + \sum_{e \in \mathcal{E}_h} h_e \|[(\mathcal{A}\sigma_h)t_e \cdot t_e]\|_{0,e}^2 + \sum_{e \in \mathcal{E}_h} h_e^3 \|[\operatorname{curl}(\mathcal{A}\sigma_h) \cdot t_e - \partial_{t_e}((\mathcal{A}\sigma_h)t_e \cdot \nu_e)]\|_{0,e}^2.
> $$
> 与连续系数 $\mathcal{A}$ 的情形相比，由于矩阵 $\mathcal{A}$ 的间断性，该估计子在所有内部边上包含了一个额外项——即 $\partial_{t_e}((\mathcal{A}\sigma_h)t_e \cdot \nu_e)$ 的跳跃。类似地，可证明该估计子的可靠性：
> $$
> \|\sigma - \sigma_h\|_{\mathcal{A}} \lesssim \eta(\sigma_h, \mathcal{T}_h) + \operatorname{osc}(f, \mathcal{T}_h).
> $$

> **注 3.4（无闭锁 $L^2$ 范数控制）**  
> 由文献 [11, Proposition 9.1.1]，有
> $$
> \|\tau\|_0 \lesssim \|\tau\|_{\mathcal{A}} + \|\operatorname{div}\tau\|_{-1}, \quad \forall \tau \in \widehat{\Sigma},
> $$
> 其中 $\widehat{\Sigma} := \{\tau \in \Sigma : (\operatorname{tr}\tau, 1) = 0\}$。结合 (3.13) 以及事实 $\|f - f_h\|_{-1} \lesssim \operatorname{osc}(f, \mathcal{T}_h)$，立得
> $$
> \|\sigma - \sigma_h\|_0 \lesssim \|\sigma - \sigma_h\|_{\mathcal{A}} + \|\operatorname{div}(\sigma - \sigma_h)\|_{-1} \lesssim \eta(\sigma_h, \mathcal{T}_h) + \operatorname{osc}(f, \mathcal{T}_h),
> $$
> 即我们能够以独立于 Lamé 常数 $\lambda$ 的常数控制应力的 $L^2$ 范数，这意味着该估计对于近不可压缩材料（$\lambda \to \infty$）具有一致无闭锁性（locking-free）。

## 3.4 效率性下界

我们遵循 Alonso [2] 的框架证明在 (3.1) 中定义的后验误差估计子的效率性。与文献 [2] 类似，我们需要如下引理：

> **引理 3.5**  
> 对于任意单元 $K \in \mathcal{T}_h$，给定 $p_K \in L^2(K)$，$q_e \in L^2(e)$，$r_e \in L^2(e)$（$e \in \partial K$），存在唯一的 $\psi_K \in P_{k+5}(K)$（$k \ge 1$），满足
> $$
> \begin{cases}
> (\psi_K, v)_K = (p_K, v)_K, & \forall v \in P_{k-1}(K), \\
> \langle \psi_K, s\rangle_e = \langle q_e, s\rangle_e, & \forall s \in P_{k-1}(e), \\
> \langle \partial_\nu \psi_K, s\rangle_e = \langle r_e, s\rangle_e, & \forall s \in P_k(e), \\
> \partial^\alpha \psi_K(P) = 0, \quad |\alpha| \le 2, & \forall \text{ 顶点 } P \in K,
> \end{cases}
> \tag{3.14}
> $$
> 其中 $P_k(e)$ 表示边 $e$ 上次数不超过 $k$ 的多项式空间。此外，满足如下稳定性估计：
> $$
> \|\psi_K\|_{0,K}^2 \lesssim \|p_K\|_{0,K}^2 + \sum_{e \in \partial K} (h_e \|q_e\|_{0,e}^2 + h_e^3 \|r_e\|_{0,e}^2).
> \tag{3.15}
> $$

*证明*：类似于文献 [36]，由上述自由度唯一确定了这样一个函数 $\psi_K$。标准的齐次化量纲缩放论证即可导出 (3.15)。  
证毕。

> **定理 3.6（误差估计子的有效性/效率性）**  
> 设 $(\sigma, u)$ 为混合问题 (1.1) 的解，$(\sigma_h, u_h)$ 为混合有限元格式 (2.1) 的解。若柔度张量 $\mathcal{A}$ 连续，则存在仅依赖于网格形状正则性以及多项式阶数 $k$ 的正常数 $C_2$，使得
> $$
> C_2 \eta(\sigma_h, \mathcal{T}_h) \le \|\sigma - \sigma_h\|_{\mathcal{A}}.
> \tag{3.16}
> $$

*证明*：估计子 $\eta^2(\sigma_h, \mathcal{T}_h)$ 可以重写为
$$
\begin{aligned}
\eta^2(\sigma_h, \mathcal{T}_h) = &\sum_{K \in \mathcal{T}_h} (\operatorname{curl}\operatorname{curl}(\mathcal{A}\sigma_h), h_K^4 \operatorname{curl}\operatorname{curl}(\mathcal{A}\sigma_h))_K + \sum_{K \in \mathcal{T}_h} \sum_{e \in \partial K} \langle (\mathcal{A}\sigma_h)t_e \cdot t_e, h_e J_{e,1}\rangle_e \\
&+ \sum_{K \in \mathcal{T}_h} \sum_{e \in \partial K \cap \mathcal{E}_h(\Omega)} \langle \operatorname{curl}(\mathcal{A}\sigma_h) \cdot t_e, h_e^3 J_{e,2}\rangle_e \\
&+ \sum_{K \in \mathcal{T}_h} \sum_{e \in \partial K \cap \mathcal{E}_h(\Gamma)} \langle \operatorname{curl}(\mathcal{A}\sigma_h) \cdot t_e - \partial_{t_e}((\mathcal{A}\sigma_h)t_e \cdot \nu_e), h_e^3 J_{e,2}\rangle_e.
\end{aligned}
$$
在每个单元 $K \in \mathcal{T}_h$ 上，对 $p_K = h_K^4 \operatorname{curl}\operatorname{curl}(\mathcal{A}\sigma_h)|_K$，$q_e = -h_e^3 J_{e,2}$ 以及 $r_e = h_e J_{e,1}$（对每条边 $e \in \partial K$）应用引理 3.5。令 $\psi|_K = \psi_K$。由于 $\psi_K$ 及其一阶与二阶偏导数在所有网格顶点处均为 0，且法向导数跨单元边界连续，故 $\psi$ 实际上属于次数为 $k+5$（$k \ge 1$）的高阶 Argyris 有限元空间，从而 $\psi \in H^2(\Omega)$。利用 (3.15)，推得
$$
\|\psi\|_{0,K}^2 \lesssim h_K^8 \|\operatorname{curl}\operatorname{curl}(\mathcal{A}\sigma_h)\|_{0,K}^2 + \sum_{e \in \partial K} (h_e^7 \|J_{e,2}\|_{0,e}^2 + h_e^5 \|J_{e,1}\|_{0,e}^2).
\tag{3.17}
$$
结合 (3.14)，可得
$$
\begin{aligned}
\eta^2(\sigma_h, \mathcal{T}_h) = &\sum_{K \in \mathcal{T}_h} (\operatorname{curl}\operatorname{curl}(\mathcal{A}\sigma_h), \psi_K)_K - \sum_{K \in \mathcal{T}_h} \sum_{e \in \partial K} \langle \operatorname{curl}(\mathcal{A}\sigma_h) \cdot t_e, \psi_K\rangle_e \\
&+ \sum_{K \in \mathcal{T}_h} \sum_{e \in \partial K} \langle (\mathcal{A}\sigma_h)t_e \cdot t_e, \partial_{\nu_e} \psi_K\rangle_e + \sum_{K \in \mathcal{T}_h} \sum_{e \in \partial K \cap \mathcal{E}_h(\Gamma)} \langle \partial_{t_e}((\mathcal{A}\sigma_h)t_e \cdot \nu_e), \psi_K\rangle_e.
\end{aligned}
\tag{3.18}
$$
由于 $(\mathcal{A}\sigma_h)t_e \cdot \nu_e$ 跨越内部单元边 $e$ 连续，所以在内部边上有 $[(\mathcal{A}\sigma_h)t_e \cdot \nu_e]_e = 0$。注意到 $\psi \in H^2(\Omega)$ 且在网格各顶点处消失，分部积分得：
$$
\sum_{K \in \mathcal{T}_h} \sum_{e \in \partial K \cap \mathcal{E}_h(\Gamma)} \langle \partial_{t_e}((\mathcal{A}\sigma_h)t_e \cdot \nu_e), \psi_K\rangle_e = -\sum_{K \in \mathcal{T}_h} \sum_{e \in \partial K \cap \mathcal{E}_h(\Gamma)} \langle (\mathcal{A}\sigma_h)t_e \cdot \nu_e, \partial_{t_e}\psi_K\rangle_e = -\sum_{K \in \mathcal{T}_h} \sum_{e \in \partial K} \langle (\mathcal{A}\sigma_h)t_e \cdot \nu_e, \partial_{t_e}\psi_K\rangle_e.
\tag{3.19}
$$
于是 (3.18) 的后两项之和化简为：
$$
\begin{aligned}
&\sum_{K \in \mathcal{T}_h} \sum_{e \in \partial K} \langle (\mathcal{A}\sigma_h)t_e \cdot t_e, \partial_{\nu_e} \psi_K\rangle_e + \sum_{K \in \mathcal{T}_h} \sum_{e \in \partial K \cap \mathcal{E}_h(\Gamma)} \langle \partial_{t_e}((\mathcal{A}\sigma_h)t_e \cdot \nu_e), \psi_K\rangle_e \\
=& \sum_{K \in \mathcal{T}_h} \sum_{e \in \partial K} \langle (\mathcal{A}\sigma_h)t_e \cdot t_e, \operatorname{Curl}\psi_K \cdot t_e\rangle_e - \sum_{K \in \mathcal{T}_h} \sum_{e \in \partial K} \langle (\mathcal{A}\sigma_h)t_e \cdot \nu_e, -\operatorname{Curl}\psi_K \cdot \nu_e\rangle_e \\
=& \sum_{K \in \mathcal{T}_h} \sum_{e \in \partial K} \langle (\mathcal{A}\sigma_h)t_e, \operatorname{Curl}\psi_K\rangle_e.
\end{aligned}
\tag{3.20}
$$
将 (3.20) 代入 (3.18) 得：
$$
\eta^2(\sigma_h, \mathcal{T}_h) = \sum_{K \in \mathcal{T}_h} \left( (\operatorname{curl}\operatorname{curl}(\mathcal{A}\sigma_h), \psi_K)_K - \sum_{e \in \partial K} \langle \operatorname{curl}(\mathcal{A}\sigma_h) \cdot t_e, \psi_K\rangle_e + \sum_{e \in \partial K} \langle (\mathcal{A}\sigma_h)t_e, \operatorname{Curl}\psi_K\rangle_e \right).
$$
对第一项分部积分两次，
$$
\begin{aligned}
\eta^2(\sigma_h, \mathcal{T}_h) &= \sum_{K \in \mathcal{T}_h} (\mathcal{A}\sigma_h, \operatorname{Curl}\operatorname{Curl}\psi_K)_K = \sum_{K \in \mathcal{T}_h} (\mathcal{A}(\sigma_h - \sigma), \operatorname{Curl}\operatorname{Curl}\psi_K)_K \\
&\lesssim \|\sigma - \sigma_h\|_{\mathcal{A}} \left(\sum_{K \in \mathcal{T}_h} h_K^{-4} \|\psi\|_{0,K}^2\right)^{1/2},
\end{aligned}
$$
此处利用了 $\operatorname{Curl}\operatorname{Curl}\psi \in \Sigma$ 以及逆不等式。由 (3.17)，
$$
\sum_{K \in \mathcal{T}_h} h_K^{-4} \|\psi\|_{0,K}^2 \lesssim \sum_{K \in \mathcal{T}_h} h_K^4 \|\operatorname{curl}\operatorname{curl}(\mathcal{A}\sigma_h)\|_{0,K}^2 + \sum_{e \in \mathcal{E}_h} (h_e \|J_{e,1}\|_{0,e}^2 + h_e^3 \|J_{e,2}\|_{0,e}^2) = \eta^2(\sigma_h, \mathcal{T}_h).
$$
结合上述两个不等式，即有
$$
\eta(\sigma_h, \mathcal{T}_h) \lesssim \|\sigma - \sigma_h\|_{\mathcal{A}}.
$$
证毕。

> **注 3.7**  
> 对于不连续的 $\mathcal{A}$ 以及注 3.3 中定义的修正误差估计子，利用类似的论证同样可以证明其有效性。

---

# 4 混合边界问题的后验误差估计

齐次 Dirichlet 边界条件下的线弹性后验误差估计可以推广到具有混合边界条件的问题。在本节中，我们讨论如下带有混合边界条件的线弹性问题。设 $\Omega \subset \mathbb{R}^2$ 为具有边界 $\Gamma := \partial\Omega = \Gamma_D \cup \Gamma_N$ 的有界多边形区域，且 $\Gamma_D \cap \Gamma_N = \emptyset, \Gamma_N \ne \emptyset$。给定数据 $f \in L^2(\Omega; \mathbb{R}^2)$，$u_D \in H^1(\Omega; \mathbb{R}^2)$ 以及 $g \in L^2(\Gamma_N; \mathbb{R}^2)$，求 $(\sigma, u) \in \Sigma_g \times V$，使得
$$
\begin{cases}
(\mathcal{A}\sigma, \tau) + (\operatorname{div}\tau, u) = \langle u_D, \tau\nu\rangle_{\Gamma_D}, & \forall \tau \in \Sigma_0, \\
(\operatorname{div}\sigma, v) = (f, v), & \forall v \in V,
\end{cases}
\tag{4.1}
$$
其中
$$
\Sigma_0 := \left\{\sigma \in \boldsymbol{H}(\operatorname{div}, \Omega; \mathbb{S}) \;\middle|\; \int_{\Gamma_N} \psi \cdot (\sigma\nu) \, ds = 0, \forall \psi \in \mathcal{D}(\Gamma_N; \mathbb{R}^2)\right\},
$$
$$
\Sigma_g := \left\{\sigma \in \boldsymbol{H}(\operatorname{div}, \Omega; \mathbb{S}) \;\middle|\; \int_{\Gamma_N} \psi \cdot (\sigma\nu) \, ds = \int_{\Gamma_N} \psi \cdot g \, ds, \forall \psi \in \mathcal{D}(\Gamma_N; \mathbb{R}^2)\right\},
$$
此处 $\mathcal{D}$ 表示检验函数空间。令 $\Sigma_{0,h} := \Sigma_0 \cap \Sigma_h$，$\Sigma_{g,h} := \Sigma_g \cap \Sigma_h$，混合有限元方法求 $(\sigma_h, u_h) \in \Sigma_{g,h} \times V_h$，使得
$$
\begin{cases}
(\mathcal{A}\sigma_h, \tau_h) + (\operatorname{div}\tau_h, u_h) = \langle u_D, \tau_h \nu\rangle_{\Gamma_D}, & \forall \tau_h \in \Sigma_{0,h}, \\
(\operatorname{div}\sigma_h, v_h) = (f, v_h), & \forall v_h \in V_h.
\end{cases}
\tag{4.2}
$$

我们将第 3 节中定义的后验误差估计子修正如下：
$$
\eta^2(\sigma_h, \mathcal{T}_h) := \sum_{K \in \mathcal{T}_h} \eta_K^2(\sigma_h) + \sum_{e \in \mathcal{E}_h} \eta_e^2(\sigma_h),
$$
其中
$$
\eta_K^2(\sigma_h) := h_K^4 \|\operatorname{curl}\operatorname{curl}(\mathcal{A}\sigma_h)\|_{0,K}^2, \quad \eta_e^2(\sigma_h) := h_e \|J_{e,1}\|_{0,e}^2 + h_e^3 \|J_{e,2}\|_{0,e}^2,
$$
$$
J_{e,1} := \begin{cases}
[(\mathcal{A}\sigma_h)t_e \cdot t_e]_e, & \text{若 } e \in \mathcal{E}_h(\Omega), \\
((\mathcal{A}\sigma_h)t_e \cdot t_e - \partial_{t_e}(u_D \cdot t_e))|_e, & \text{若 } e \in \mathcal{E}_h(\Gamma_D),
\end{cases}
$$
$$
J_{e,2} := \begin{cases}
[\operatorname{curl}(\mathcal{A}\sigma_h) \cdot t_e]_e, & \text{若 } e \in \mathcal{E}_h(\Omega), \\
(\operatorname{curl}(\mathcal{A}\sigma_h) \cdot t_e + \partial_{t_e t_e}^2(u_D \cdot \nu) - \partial_{t_e}((\mathcal{A}\sigma_h)t_e \cdot \nu_e))|_e, & \text{若 } e \in \mathcal{E}_h(\Gamma_D),
\end{cases}
$$
其中 $\mathcal{E}_h(\Gamma_D)$ 是 Dirichlet 边界上的单元边集合。

类似于第 3 节，我们能够证明该后验误差估计子的可靠性与有效性。

> **定理 4.1（混合边界下误差估计子的可靠性与有效性）**  
> 设 $(\sigma, u)$ 为混合问题 (4.1) 的解，$(\sigma_h, u_h)$ 为混合有限元格式 (4.2) 的解。若柔度张量 $\mathcal{A}$ 连续，则存在仅依赖于网格形状正则性以及多项式阶数 $k$ 的正常数 $C_3, C_4$，使得
> $$
> \|\sigma - \sigma_h\|_{\mathcal{A}} \le C_3 (\eta(\sigma_h, \mathcal{T}_h) + \operatorname{osc}(f, \mathcal{T}_h) + \operatorname{osc}(g, \mathcal{E}_h(\Gamma_N))),
> \tag{4.3}
> $$
> 并且
> $$
> C_4 \eta(\sigma_h, \mathcal{T}_h) \le \|\sigma - \sigma_h\|_{\mathcal{A}} + \operatorname{osc}(u_D, \mathcal{E}_h(\Gamma_D)),
> \tag{4.4}
> $$
> 其中 Dirichlet 边界数据 $u_D$ 与 Neumann 边界条件 $g$ 的数据震荡分别定义为：
> $$
> \operatorname{osc}^2(g, \mathcal{E}_h(\Gamma_N)) := \sum_{e \in \mathcal{E}_h(\Gamma_N)} h_e \|g - g_h\|_{0,e}^2,
> $$
> $$
> \operatorname{osc}^2(u_D, \mathcal{E}_h(\Gamma_D)) := \sum_{e \in \mathcal{E}_h(\Gamma_D)} h_e \|\partial_{t_e}(u_D \cdot t_e) - \partial_{t_e}(u_{D,h} \cdot t_e)\|_{0,e}^2 + \sum_{e \in \mathcal{E}_h(\Gamma_D)} h_e^3 \|\partial_{t_e t_e}^2(u_D \cdot \nu_e) - \partial_{t_e t_e}^2(u_{D,h} \cdot \nu_e)\|_{0,e}^2,
> $$
> $g_h$ 是 $g$ 到 $P_k(\mathcal{E}_h(\Gamma_N); \mathbb{R}^2)$ 上的分片 $L^2$ 投影，$u_{D,h}$ 是 $u_D$ 到 $P_k(\mathcal{E}_h(\Gamma_D); \mathbb{R}^2)$ 上的分片 $L^2$ 投影。

---

# 5 位移的后验误差估计

在本节中，我们讨论近期在文献 [20] 中构造的超收敛后处理位移的后验误差估计。理论分析的核心要点包括文献 [20] 中建立的离散 inf-sup 条件与破裂空间 $H^1(\mathcal{T}_h; \mathbb{R}^2)$ 上的范数等价性，以及应力后验误差估计 (3.13) 和 (3.16)。此处破裂空间定义为：
$$
H^1(\mathcal{T}_h; \mathbb{R}^2) := \{v \in L^2(\Omega; \mathbb{R}^2) : v|_K \in H^1(K; \mathbb{R}^2), \forall K \in \mathcal{T}_h\}.
$$
对任意 $v \in H^1(\mathcal{T}_h; \mathbb{R}^2)$，定义如下依赖于网格的范数：
$$
|v|_{1,h}^2 := \|\varepsilon_h(v)\|_0^2 + \sum_{e \in \mathcal{E}_h} h_e^{-1} \|[v]\|_{0,e}^2,
$$
其中对任意 $K \in \mathcal{T}_h$，有 $\varepsilon_h(v)|_K = \varepsilon(v|_K)$。

首先回顾文献 [20] 中利用 $(\sigma_h, u_h)$ 构造的超收敛后处理位移。为此，令
$$
V_h^* := \{v \in L^2(\Omega; \mathbb{R}^2) : v|_K \in P_{k+1}(K; \mathbb{R}^2), \forall K \in \mathcal{T}_h\}.
$$
后处理位移定义如下（参见 [12, 20, 35]）：在每个单元 $K \in \mathcal{T}_h$ 上，求 $u_h^* \in V_h^*$，使得
$$
(u_h^*, v)_K = (u_h, v)_K, \quad \forall v \in P_{k-1}(K; \mathbb{R}^2),
\tag{5.1}
$$
$$
(\varepsilon(u_h^*), \varepsilon(w))_K = (\mathcal{A}\sigma_h, \varepsilon(w))_K, \quad \forall w \in (I - Q_h)V_h^*|_K.
\tag{5.2}
$$

我们回顾如下两个有用的结论（参见 [20]）：离散 inf-sup 条件
$$
|v_h|_{1,h} \lesssim \sup_{0 \ne \tau_h \in \Sigma_h} \frac{(\operatorname{div}\tau_h, v_h)}{\|\tau_h\|_0}, \quad \forall v_h \in V_h,
\tag{5.3}
$$
以及范数等价性
$$
|v - Q_h v|_{1,h} \approx \|\varepsilon_h(v - Q_h v)\|_0, \quad \forall v \in H^1(\mathcal{T}_h; \mathbb{R}^2).
\tag{5.4}
$$

> **定理 5.1（位移后验误差估计）**  
> 设 $(\sigma, u)$ 为混合问题 (1.1) 的解，$(\sigma_h, u_h)$ 为混合有限元方法 (2.1) 的解，$u_h^*$ 为由 (5.1)–(5.2) 定义的后处理位移。则有
> $$
> \|\sigma - \sigma_h\|_{\mathcal{A}} + |u - u_h^*|_{1,h} \lesssim \eta(\sigma_h, \mathcal{T}_h) + \|\mathcal{A}\sigma_h - \varepsilon_h(u_h^*)\|_0 + \operatorname{osc}(f, \mathcal{T}_h),
> \tag{5.5}
> $$
> 以及
> $$
> \eta(\sigma_h, \mathcal{T}_h) + \|\mathcal{A}\sigma_h - \varepsilon_h(u_h^*)\|_0 \lesssim \|\sigma - \sigma_h\|_{\mathcal{A}} + |u - u_h^*|_{1,h}.
> \tag{5.6}
> $$

*证明*：在离散 inf-sup 条件 (5.3) 中取 $v_h = Q_h(u - u_h^*)$，利用 (5.1)、(1.1) 的第一个方程及 (2.1)，可得：
$$
\begin{aligned}
|Q_h(u - u_h^*)|_{1,h} &\lesssim \sup_{0 \ne \tau_h \in \Sigma_h} \frac{(\operatorname{div}\tau_h, Q_h(u - u_h^*))}{\|\tau_h\|_0} \\
&= \sup_{0 \ne \tau_h \in \Sigma_h} \frac{(\operatorname{div}\tau_h, u - u_h)}{\|\tau_h\|_0} \\
&= \sup_{0 \ne \tau_h \in \Sigma_h} \frac{(\mathcal{A}(\sigma - \sigma_h), \tau_h)}{\|\tau_h\|_0} \\
&\le \|\mathcal{A}(\sigma - \sigma_h)\|_0.
\end{aligned}
$$
在 (5.4) 中选取 $v = u - u_h^*$，有
$$
\begin{aligned}
|v - Q_h v|_{1,h} &\approx \|\varepsilon_h(v - Q_h v)\|_0 \le \|\varepsilon_h(u - u_h^*)\|_0 + |Q_h(u - u_h^*)|_{1,h} \\
&= \|\mathcal{A}\sigma - \varepsilon_h(u_h^*)\|_0 + |Q_h(u - u_h^*)|_{1,h} \\
&\lesssim \|\mathcal{A}\sigma_h - \varepsilon_h(u_h^*)\|_0 + \|\mathcal{A}(\sigma - \sigma_h)\|_0.
\end{aligned}
$$
结合上述两式即导出：
$$
|u - u_h^*|_{1,h} \lesssim \|\mathcal{A}\sigma_h - \varepsilon_h(u_h^*)\|_0 + \|\mathcal{A}(\sigma - \sigma_h)\|_0,
$$
将其与 (3.13) 结合即证得可靠性 (5.5)。

接下来证明有效性 (5.6)。由三角不等式：
$$
\begin{aligned}
\|\mathcal{A}\sigma_h - \varepsilon_h(u_h^*)\|_0 &\le \|\mathcal{A}(\sigma - \sigma_h)\|_0 + \|\mathcal{A}\sigma - \varepsilon_h(u_h^*)\|_0 \\
&= \|\mathcal{A}(\sigma - \sigma_h)\|_0 + \|\varepsilon_h(u - u_h^*)\|_0 \\
&\lesssim \|\sigma - \sigma_h\|_{\mathcal{A}} + |u - u_h^*|_{1,h}.
\end{aligned}
$$
结合定理 3.6 中的 (3.16)，即完成了有效性的证明。  
证毕。

---

# 6 数值实验

在本节中，我们通过若干数值算例检验后验误差估计子的性能。

在第一个算例中，设 $\Omega = (0, 1)^2$，$k = 3$，$\mu = 1$，右端项取为
$$
f(x, y) = \pi^3 \begin{pmatrix} -\sin(2\pi y)(2\cos(2\pi x) - 1) \\ \sin(2\pi x)(2\cos(2\pi y) - 1) \end{pmatrix},
$$
精确解取自文献 [16, Section 5.2]：
$$
u(x, y) = \frac{\pi}{2} \begin{pmatrix} \sin^2(\pi x)\sin(2\pi y) \\ -\sin^2(\pi y)\sin(2\pi x) \end{pmatrix}.
$$
采用均匀三角形网格剖分 $\Omega$。在 $\lambda = 10$ 和 $\lambda = 10000$ 下的先验与后验误差估计结果分别列于表 1 和表 2 中。从表 1 和表 2 可以看出，$\|\sigma - \sigma_h\|_{\mathcal{A}}$、$\|\nabla_h(u - u_h^*)\|_0$、$\eta(\sigma_h, \mathcal{T}_h)$ 以及 $\|\mathcal{A}\sigma_h - \varepsilon_h(u_h^*)\|_0$ 的收敛阶均为 $O(h^4)$。因此，对于光滑解，后验误差估计子 $\eta(\sigma_h, \mathcal{T}_h)$ 以及 $\eta(\sigma_h, \mathcal{T}_h) + \|\mathcal{A}\sigma_h - \varepsilon_h(u_h^*)\|_0$ 关于网格尺寸 $h$ 和 Lamé 常数 $\lambda$ 均是一致可靠且有效的。

<div align="center"><b>表 1：第一个算例在 $\lambda = 10$ 时的数值误差与收敛阶</b></div>

| $h$ | $\|\sigma - \sigma_h\|_{\mathcal{A}}$ | 阶数 | $\|\nabla_h (u - u_h^*)\|_0$ | 阶数 | $\eta(\sigma_h, \mathcal{T}_h)$ | 阶数 | $\|\mathcal{A}\sigma_h - \varepsilon_h(u_h^*)\|_0$ | 阶数 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $2^{-1}$ | 6.6998E−01 | — | 7.9544E−01 | — | 1.6615E+01 | — | 4.0073E−02 | — |
| $2^{-2}$ | 5.2451E−02 | 3.68 | 6.0585E−02 | 3.71 | 1.3585E+00 | 3.61 | 9.3899E−03 | 2.09 |
| $2^{-3}$ | 3.6139E−03 | 3.86 | 4.5839E−03 | 3.72 | 1.0918E−01 | 3.64 | 7.1387E−04 | 3.72 |
| $2^{-4}$ | 2.2714E−04 | 3.99 | 3.0676E−04 | 3.90 | 7.4510E−03 | 3.87 | 4.5925E−05 | 3.96 |
| $2^{-5}$ | 1.4193E−05 | 4.00 | 1.9600E−05 | 3.97 | 4.7919E−04 | 3.96 | 2.8824E−06 | 3.99 |
| $2^{-6}$ | 8.8742E−07 | 4.00 | 1.2347E−06 | 3.99 | 3.0263E−05 | 3.99 | 1.8040E−07 | 4.00 |
| $2^{-7}$ | 5.5567E−08 | 4.00 | 7.7435E−08 | 3.99 | 1.8992E−06 | 3.99 | 1.1306E−08 | 4.00 |

<div align="center"><b>表 2：第一个算例在 $\lambda = 10000$ 时的数值误差与收敛阶</b></div>

| $h$ | $\|\sigma - \sigma_h\|_{\mathcal{A}}$ | 阶数 | $\|\nabla_h (u - u_h^*)\|_0$ | 阶数 | $\eta(\sigma_h, \mathcal{T}_h)$ | 阶数 | $\|\mathcal{A}\sigma_h - \varepsilon_h(u_h^*)\|_0$ | 阶数 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $2^{-1}$ | 6.6096E−01 | — | 7.7905E−01 | — | 1.6050E+01 | — | 4.3292E−02 | — |
| $2^{-2}$ | 5.1630E−02 | 3.68 | 5.8762E−02 | 3.73 | 1.3066E+00 | 3.62 | 9.0182E−03 | 2.26 |
| $2^{-3}$ | 3.5430E−03 | 3.87 | 4.3977E−03 | 3.74 | 1.0508E−01 | 3.64 | 6.8780E−04 | 3.71 |
| $2^{-4}$ | 2.2220E−04 | 4.00 | 2.9277E−04 | 3.91 | 7.1542E−03 | 3.88 | 4.4330E−05 | 3.96 |
| $2^{-5}$ | 1.3873E−05 | 4.00 | 1.8668E−05 | 3.97 | 4.5947E−04 | 3.96 | 2.7853E−06 | 3.99 |
| $2^{-6}$ | 8.6708E−07 | 4.00 | 1.1751E−06 | 3.99 | 2.8998E−05 | 3.99 | 1.7442E−07 | 4.00 |
| $2^{-7}$ | 5.4210E−08 | 4.00 | 7.3695E−08 | 4.00 | 1.8195E−06 | 3.99 | 1.0922E−08 | 4.00 |

接下来，我们利用后验误差估计子 $\eta(\sigma_h, \mathcal{T}_h)$ 设计混合有限元自适应算法，即算法 1。在算法 1 的求解（SOLVE）部分，采用基于近似块因子分解预条件子的广义极小残量法（GMRES，参见 [20]）；数值算例表明该求解器在自适应网格上同样高度高效且稳健。

---

**算法 1：混合有限元方法 (2.1) 的自适应算法**  
给定参数 $0 < \vartheta < 1$ 以及初始网格 $\mathcal{T}_0$。令 $m := 0$。
1. **SOLVE（求解）**：在网格 $\mathcal{T}_m$ 上求解混合有限元格式 (2.1)，得到离散解 $(\sigma_m, u_m) \in \Sigma_m \times V_m$。
2. **ESTIMATE（估计）**：逐单元计算局部误差指标 $\eta^2(\sigma_m, \mathcal{T}_m)$。
3. **MARK（标记）**：采用 Dörfler 标记策略选取基数最小的子集 $\mathcal{S}_m \subset \mathcal{T}_m$，使得
   $$
   \eta^2(\sigma_m, \mathcal{S}_m) \ge \vartheta \eta^2(\sigma_m, \mathcal{T}_m).
   $$
4. **REFINE（加密）**：利用最新顶点二分（NVB）对至少含有一条边属于 $\mathcal{S}_m$ 的每个三角形 $K$ 进行细分，获得新网格 $\mathcal{T}_{m+1}$。
5. 令 $m := m + 1$ 并返回步骤 1。

---

现在我们构造一个解具有奇异性的算例来测试算法 1。设 L 形区域 $\Omega = (-1, 1) \times (-1, 1) \setminus [0, 1) \times (-1, 0]$。令
$$
\Phi_1(\theta) = \begin{pmatrix} ((z + 2)(\lambda + \mu) + 4\mu)\sin(z\theta) - z(\lambda + \mu)\sin((z-2)\theta) \\ z(\lambda + \mu)(\cos(z\theta) - \cos((z-2)\theta)) \end{pmatrix},
$$
$$
\Phi_2(\theta) = \begin{pmatrix} z(\lambda + \mu)(\cos((z-2)\theta) - \cos(z\theta)) \\ -((2 - z)(\lambda + \mu) + 4\mu)\sin(z\theta) - z(\lambda + \mu)\sin((z-2)\theta) \end{pmatrix},
$$
$$
\Phi(\theta) = (z(\lambda + \mu)\sin((z-2)\omega) + ((2 - z)(\lambda + \mu) + 4\mu)\sin(z\omega))\Phi_1(\theta) - z(\lambda + \mu)(\cos((z-2)\omega) - \cos(z\omega))\Phi_2(\theta),
$$
其中 $z \in (0, 1)$ 是代数方程 $(\lambda + 3\mu)^2 \sin^2(z\omega) = (\lambda + \mu)^2 z^2 \sin^2\omega$ 的实根，$\omega = 3\pi/2$。极坐标下的精确奇异解取为（参见 [24, Subsection 4.6]）：
$$
u(r, \theta) = \frac{1}{(\lambda + \mu)^2}(r^2 \cos^2\theta - 1)(r^2 \sin^2\theta - 1)r^z \Phi(\theta).
$$
经计算，当 $\lambda = 10$ 时 $z = 0.561586549334359$；当 $\lambda = 10000$ 时 $z = 0.544505718203590$。同样取 $k = 3$ 且 $\mu = 1$。

算法 1 在不同标记参数 $\vartheta$ 与 Lamé 常数 $\lambda$ 下生成的若干自适应网格展示在图 1 中（其中 #dofs 表示自由度总数）。自适应算法 1 非常优异地捕捉到了拐角原点 $(0, 0)$ 处精确解的奇异性。针对 $\vartheta = 0.1, 0.2$ 以及 $\lambda = 10, 10000$ 的自适应算法收敛历史分别绘制在图 2 和图 3 中。由图 2 和图 3 可以看出，无论 $\lambda = 10$ 还是 $\lambda = 10000$，误差 $\|\sigma - \sigma_h\|_{\mathcal{A}}$ 与估计子 $\eta(\sigma_h, \mathcal{T}_h)$ 的收敛阶均达到 $O((\#\mathrm{dofs})^{-2})$，这与理论分析完全一致。对于二维均匀网格，$(\#\mathrm{dofs})^{-2} \approx h^4$，这意味着误差与后验估计子均恢复了最优收敛阶。

![图 1：算例 2 中算法 1 在不同 $\vartheta$ 和 $\lambda$ 下生成的网格](Chen2018_Residual_Fig1.png)
<div align="center"><b>图 1：算例 2 中算法 1 在不同 $\vartheta$ 和 $\lambda$ 下生成的网格（(a) 初始网格；(b) #dofs = 198,098, $\vartheta = 0.1, \lambda = 10$；(c) #dofs = 129,624, $\vartheta = 0.2, \lambda = 10$；(d) #dofs = 138,323, $\vartheta = 0.2, \lambda = 10000$）</b></div>

<br>

![图 2：算例 2 在 $\lambda = 10$ 时误差 $\|\sigma - \sigma_h\|_{\mathcal{A}}$ 与 $\eta(\sigma_h, \mathcal{T}_h)$ 随自由度数变化的对数收敛曲线](Chen2018_Residual_Fig2.png)
<div align="center"><b>图 2：算例 2 在 $\lambda = 10$ 时误差 $\|\sigma - \sigma_h\|_{\mathcal{A}}$ 与 $\eta(\sigma_h, \mathcal{T}_h)$ 随自由度数（#dofs）变化的对数收敛曲线</b></div>

<br>

![图 3：算例 2 在 $\lambda = 10000$ 时误差 $\|\sigma - \sigma_h\|_{\mathcal{A}}$ 与 $\eta(\sigma_h, \mathcal{T}_h)$ 随自由度数变化的对数收敛曲线](Chen2018_Residual_Fig3.png)
<div align="center"><b>图 3：算例 2 在 $\lambda = 10000$ 时误差 $\|\sigma - \sigma_h\|_{\mathcal{A}}$ 与 $\eta(\sigma_h, \mathcal{T}_h)$ 随自由度数变化的对数收敛曲线</b></div>

<br>

第三个算例考虑文献 [16, Subsection 5.3] 中测试的带一般边界条件的 L 形基准问题，求解区域为旋转 L 形区域，初始网格如图 4 所示。在边界 $x^2 = y^2$ 上施加 Neumann 边界条件，而在 $\Omega$ 的其余边界上施加 Dirichlet 边界条件。极坐标下的精确解由下式给出：
$$
\begin{pmatrix} u_r(r, \theta) \\ u_\theta(r, \theta) \end{pmatrix} = \frac{r^\alpha}{2\mu} \begin{pmatrix} -(\alpha + 1)\cos((\alpha + 1)\theta) + (C_2 - \alpha - 1)C_1 \cos((\alpha - 1)\theta) \\ (\alpha + 1)\sin((\alpha + 1)\theta) + (C_2 + \alpha - 1)C_1 \sin((\alpha - 1)\theta) \end{pmatrix}.
$$
常数分别定义为 $C_1 := -\cos((\alpha + 1)\omega)/\cos((\alpha - 1)\omega)$ 以及 $C_2 := -2(\lambda + 2\mu)/(\lambda + \mu)$，其中对于 $\omega = 3\pi/4$，$\alpha = 0.544483736782$ 是方程 $\alpha \sin(2\omega) + \sin(2\omega\alpha) = 0$ 的正根。Lamé 参数为
$$
\lambda = \frac{E\nu}{(1 + \nu)(1 - 2\nu)}, \quad \mu = \frac{E}{2(1 + \nu)},
$$
其中弹性模量 $E = 10^5$，泊松比 $\nu = 0.4999$。体力 $f(x, y)$ 和 Neumann 边界数据均为零，Dirichlet 边界条件直接取自精确解。易知对任意 $s < 1 + \alpha$ 均有 $u \in H^s(\Omega; \mathbb{R}^2)$。在均匀网格上取 $k = 3, 4, 5$ 的数值误差列于表 3–5 中。从中可以观察到，由于精确解 $u$ 的奇异性，$\|\sigma - \sigma_h\|_{\mathcal{A}}$ 和 $\eta(\sigma_h, \mathcal{T}_h)$ 的收敛阶均退化为 $O(h^\alpha)$。因此，在均匀网格上采用更高阶的有限元并不能带来更高的收敛速度。

![图 4：旋转 L 形区域及其初始网格](Chen2018_Residual_Fig4.png)
<div align="center"><b>图 4：旋转 L 形区域及其初始网格</b></div>

<br>

<div align="center"><b>表 3：算例 3 在均匀网格上 $k = 4$ 时的数值误差与收敛阶</b></div>

| $h$ | $\|\sigma - \sigma_h\|_{\mathcal{A}}$ | 阶数 | $\eta(\sigma_h, \mathcal{T}_h)$ | 阶数 | $\eta(\sigma_h, \mathcal{T}_h)/\|\sigma - \sigma_h\|_{\mathcal{A}}$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $\sqrt{2}/2$ | 5.3787E−03 | — | 8.4604E−04 | — | 1.57E−01 |
| $\sqrt{2}/2^2$ | 3.7715E−03 | 0.5121 | 6.0103E−04 | 0.4933 | 1.59E−01 |
| $\sqrt{2}/2^3$ | 2.6141E−03 | 0.5288 | 4.2105E−04 | 0.5134 | 1.61E−01 |
| $\sqrt{2}/2^4$ | 1.8017E−03 | 0.5370 | 2.9171E−04 | 0.5294 | 1.62E−01 |
| $\sqrt{2}/2^5$ | 1.2383E−03 | 0.5409 | 2.0101E−04 | 0.5373 | 1.62E−01 |
| $\sqrt{2}/2^6$ | 8.5005E−04 | 0.5428 | 1.3814E−04 | 0.5411 | 1.63E−01 |

<div align="center"><b>表 4：算例 3 在均匀网格上 $k = 3$ 时的数值误差与收敛阶</b></div>

| $h$ | $\|\sigma - \sigma_h\|_{\mathcal{A}}$ | 阶数 | $\eta(\sigma_h, \mathcal{T}_h)$ | 阶数 | $\eta(\sigma_h, \mathcal{T}_h)/\|\sigma - \sigma_h\|_{\mathcal{A}}$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $\sqrt{2}/2$ | 6.6585E−03 | — | 4.5431E−04 | — | 6.82E−02 |
| $\sqrt{2}/2^2$ | 4.7264E−03 | 0.4944 | 3.2749E−04 | 0.4722 | 6.93E−02 |
| $\sqrt{2}/2^3$ | 3.2966E−03 | 0.5198 | 2.3212E−04 | 0.4966 | 7.04E−02 |
| $\sqrt{2}/2^4$ | 2.2791E−03 | 0.5325 | 1.6180E−04 | 0.5207 | 7.10E−02 |
| $\sqrt{2}/2^5$ | 1.5689E−03 | 0.5387 | 1.1182E−04 | 0.5330 | 7.13E−02 |
| $\sqrt{2}/2^6$ | 1.0777E−03 | 0.5418 | 7.6957E−05 | 0.5390 | 7.14E−02 |
| $\sqrt{2}/2^7$ | 7.3957E−04 | 0.5432 | 5.2859E−05 | 0.5419 | 7.15E−02 |

<div align="center"><b>表 5：算例 3 在均匀网格上 $k = 5$ 时的数值误差与收敛阶</b></div>

| $h$ | $\|\sigma - \sigma_h\|_{\mathcal{A}}$ | 阶数 | $\eta(\sigma_h, \mathcal{T}_h)$ | 阶数 | $\eta(\sigma_h, \mathcal{T}_h)/\|\sigma - \sigma_h\|_{\mathcal{A}}$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $\sqrt{2}/2$ | 4.5148E−03 | — | 1.2961E−03 | — | 2.87E−01 |
| $\sqrt{2}/2^2$ | 3.1444E−03 | 0.5219 | 9.1388E−04 | 0.5041 | 2.91E−01 |
| $\sqrt{2}/2^3$ | 2.1721E−03 | 0.5337 | 6.3609E−04 | 0.5228 | 2.93E−01 |
| $\sqrt{2}/2^4$ | 1.4946E−03 | 0.5393 | 4.3929E−04 | 0.5341 | 2.94E−01 |
| $\sqrt{2}/2^5$ | 1.0265E−03 | 0.5420 | 3.0223E−04 | 0.5395 | 2.94E−01 |

接着，我们在自适应网格上测试后验误差估计子 $\eta(\sigma_h, \mathcal{T}_h)$。取 $k = 3, 4, 5$ 且 $\vartheta = 0.1$ 时算法 1 的自适应收敛曲线分别绘制在图 5 和图 6 中。图 5 和图 6 清楚地表明，误差 $\|\sigma - \sigma_h\|_{\mathcal{A}}$ 与后验估计子 $\eta(\sigma_h, \mathcal{T}_h)$ 的收敛阶均达到了最优的 $O((\#\mathrm{dofs})^{-(k+1)/2})$。

![图 5：算例 3 在 $\vartheta = 0.1$ 时误差 $\|\sigma - \sigma_h\|_{\mathcal{A}}$ 随自由度数变化的 $\log_{10}$-$\log_{10}$ 收敛曲线](Chen2018_Residual_Fig5.png)
<div align="center"><b>图 5：算例 3 在 $\vartheta = 0.1$ 时误差 $\|\sigma - \sigma_h\|_{\mathcal{A}}$ 随自由度数变化的 $\log_{10}$-$\log_{10}$ 收敛曲线</b></div>

<br>

![图 6：算例 3 在 $\vartheta = 0.1$ 时后验估计子 $\eta(\sigma_h, \mathcal{T}_h)$ 随自由度数变化的 $\log_{10}$-$\log_{10}$ 收敛曲线](Chen2018_Residual_Fig6.png)
<div align="center"><b>图 6：算例 3 在 $\vartheta = 0.1$ 时后验估计子 $\eta(\sigma_h, \mathcal{T}_h)$ 随自由度数变化的 $\log_{10}$-$\log_{10}$ 收敛曲线</b></div>

---

# 致谢

本项工作得到了美国国家科学基金（Grant No. DMS-1418934）、北京市海外人才聚集工程（海聚工程）、国家自然科学基金（Grant Nos. 11625101, 91430213, 11421101, 11771338, 11671304 和 11401026）、浙江省自然科学基金（Grant Nos. LY17A010010, LY15A010015 和 LY15A010016）以及温州市科技计划项目（Grant No. G20160019）的资助。最后一位作者感谢中国国家留学基金委（CSC）以及加利福尼亚大学欧文分校在其 2014 至 2015 年访问 UC Irvine 期间给予的支持。

---

# 参考文献（References）

[1] Adams S, Cockburn B. A mixed finite element method for elasticity in three dimensions. J Sci Comput, 2001, 25: 515–521  
[2] Alonso A. Error estimators for a mixed method. Numer Math, 1996, 74: 385–395  
[3] Arnold D N. Differential complexes and numerical stability. In: Proceedings of the International Congress of Mathematicians, vol 1. Beijing: Higher Education Press, 2002, 137–157  
[4] Arnold D N, Awanou G. Rectangular mixed finite elements for elasticity. Math Models Methods Appl Sci, 2005, 15: 1417–1429  
[5] Arnold D N, Awanou G, Winther R. Finite elements for symmetric tensors in three dimensions. Math Comp, 2008, 77: 1229–1251  
[6] Arnold D N, Brezzi F, Douglas J. Peers: A new mixed finite element for plane elasticity. Jpn J Appl Math, 1984, 1: 347–367  
[7] Arnold D N, Falk R S, Winther R. Mixed finite element methods for linear elasticity with weakly imposed symmetry. Math Comp, 2007, 76: 1699–1724  
[8] Arnold D N, Winther R. Mixed finite elements for elasticity. Numer Math, 2002, 92: 401–419  
[9] Arnold D N, Winther R. Nonconforming mixed elements for elasticity. Math Models Methods Appl Sci, 2003, 13: 295–307  
[10] Boffi D, Brezzi F, Fortin M. Reduced symmetry elements in linear elasticity. Commun Pure Appl Anal, 2009, 8: 95–121  
[11] Boffi D, Brezzi F, Fortin M. Mixed Finite Element Methods and Applications. Springer Series in Computational Mathematics, vol. 44. Heidelberg: Springer, 2013  
[12] Bramble J H, Xu J. A local post-processing technique for improving the accuracy in mixed finite-element approximations. SIAM J Numer Anal, 1989, 26: 1267–1275  
[13] Carstensen C. A posteriori error estimate for the mixed finite element method. Math Comp, 1997, 66: 465–477  
[14] Carstensen C, Dolzmann G. A posteriori error estimates for mixed FEM in elasticity. Numer Math, 1998, 81: 187–209  
[15] Carstensen C, Eigel M, Gedicke J. Computational competition of symmetric mixed FEM in linear elasticity. Comput Methods Appl Mech Engrg, 2011, 200: 2903–2915  
[16] Carstensen C, Gedicke J. Robust residual-based a posteriori Arnold-Winther mixed finite element analysis in elasticity. Comput Methods Appl Mech Engrg, 2016, 300: 245–264  
[17] Carstensen C, Günther D, Reininghaus J, et al. The Arnold-Winther mixed FEM in linear elasticity. Part I: Implementation and numerical verification. Comput Methods Appl Mech Engrg, 2008, 197: 3014–3023  
[18] Carstensen C, Hu J. A unifying theory of a posteriori error control for nonconforming finite element methods. Numer Math, 2007, 107: 473–502  
[19] Chen L, Holst M, Xu J. Convergence and optimality of adaptive mixed finite element methods. Math Comp, 2009, 78: 35–53  
[20] Chen L, Hu J, Huang X. Fast auxiliary space preconditioner for linear elasticity in mixed form. Math Comp, 2018, 87(312): 1601–1633  
[21] Cockburn B, Gopalakrishnan J, Guzmán J. A new elasticity element made for enforcing weak stress symmetry. Math Comp, 2010, 79: 1331–1349  
[22] Gatica G N, Maischak M. A posteriori error estimates for the mixed finite element method with Lagrange multipliers. Numer Methods Partial Differential Equations, 2005, 21: 421–450  
[23] Girault V, Scott L R. Hermite interpolation of nonsmooth functions preserving boundary conditions. Math Comp, 2002, 71: 1043–1074  
[24] Grisvard P. Singularities in Boundary Value Problems. Research in Applied Mathematics, vol. 22. Paris: Masson, 1992  
[25] Guzmán J. A unified analysis of several mixed methods for elasticity with weak stress symmetry. J Sci Comput, 2010, 44: 156–169  
[26] Hoppe R H W, Wohlmuth B. Adaptive multilevel techniques for mixed finite element discretizations of elliptic boundary value problems. SIAM J Numer Anal, 1997, 34: 1658–1681  
[27] Hu J. Finite element approximations of symmetric tensors on simplicial grids in $\mathbb{R}^n$: The higher order case. J Comput Math, 2015, 33: 283–296  
[28] Hu J. A new family of efficient conforming mixed finite elements on both rectangular and cuboid meshes for linear elasticity in the symmetric formulation. SIAM J Numer Anal, 2015, 53: 1438–1463  
[29] Hu J, Zhang S. A family of conforming mixed finite elements for linear elasticity on triangular grids. arXiv:1406.7457, 2014  
[30] Hu J, Zhang S. A family of symmetric mixed finite elements for linear elasticity on tetrahedral grids. Sci China Math, 2015, 58: 297–307  
[31] Hu J, Zhang S. Finite element approximations of symmetric tensors on simplicial grids in $\mathbb{R}^n$: The lower order case. Math Models Methods Appl Sci, 2016, 26: 1649–1669  
[32] Kim K Y. A posteriori error estimator for linear elasticity based on nonsymmetric stress tensor approximation. J Korean Soc Ind Appl Math, 2012, 16: 1–13  
[33] Larson M G, Målqvist A. A posteriori error estimates for mixed finite element approximations of elliptic problems. Numer Math, 2008, 108: 487–500  
[34] Lonsing M, Verfürth R. A posteriori error estimators for mixed finite element methods in linear elasticity. Numer Math, 2004, 97: 757–778  
[35] Lovadina C, Stenberg R. Energy norm a posteriori error estimates for mixed finite element methods. Math Comp, 2006, 75: 1659–1674  
[36] Morgan J, Scott R. A nodal basis for $C^1$ piecewise polynomials of degree $n \ge 5$. Math Comp, 1975, 29: 736–740  
[37] Shi Z C, Wang M. Finite Element Methods. Beijing: Science Press, 2013  
[38] Stenberg R. A family of mixed finite elements for the elasticity problem. Numer Math, 1988, 53: 513–538  
