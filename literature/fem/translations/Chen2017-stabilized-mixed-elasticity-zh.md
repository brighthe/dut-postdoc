---
title: "翻译：Stabilized Mixed Finite Element Methods for Linear Elasticity on Simplicial Grids in ℝⁿ"
tags:
  - translation
  - mixed-fem
  - elasticity
  - stabilization
  - simplicial-grids
status: "read"
date_created: 2026-09-22
date_updated: 2026-09-28
source: "../sources/Chen2017-stabilized-mixed-elasticity.pdf"
citekey: "chenStabilizedMixedFinite2017"
language: "zh-CN"
---

# Stabilized Mixed Finite Element Methods for Linear Elasticity on Simplicial Grids in $\mathbb{R}^n$

---

# 信息

- **中文标题**：$\mathbb{R}^n$ 中单纯形网格上线弹性问题的稳定化混合有限元方法
- **作者**：Long Chen（陈龙）$^1$；Jun Hu（胡俊）$^2$；Xuehai Huang（黄学海）$^{3,*}$
- **单位**：
  - $1$: 加州大学欧文分校数学系（Irvine, CA 92697, USA）
  - $2$: 北京大学数学科学学院、LMAM（北京 100871）
  - $3$: 温州大学数学与信息科学学院（温州 325035）
- **期刊**：*Computational Methods in Applied Mathematics*
- **卷 / 期 / 页码**：17(1): 17–31
- **DOI**：10.1515/cmam-2016-0035
- **收稿 / 修回 / 录用**：2016-10-14 / 2016-10-19 / 2016-10-20
- **通讯作者**：Xuehai Huang（xuehaihuang@gmail.com）

# 摘要

在本文中，我们针对单纯形网格上的线弹性问题设计了两类稳定化混合有限元方法。在第一类单元中，对于 $1 \le k \le n$，分别采用 $H(\mathrm{div}, \Omega; \mathbb{S})\text{-}P_k$ 与 $L^2(\Omega; \mathbb{R}^n)\text{-}P_{k-1}$ 逼近应力与位移空间，并引入基于三角剖分棱边/面处的离散位移跃度的稳定化技术；在第二类单元中，对于 $1 \le k \le n$，采用 $H_0^1(\Omega; \mathbb{R}^n)\text{-}P_k$ 逼近位移空间，并采用 Brezzi、Fortin 与 Marini [19] 建议的稳定化技术。我们建立了离散 inf-sup 条件，并据此给出了相应的先验误差分析。理论分析的核心工具是两个特殊的插值算子，它们基于每个单元上一个关键的多项式 $H(\mathrm{div})$ 泡函数空间构造而成。这些方法的显著特征是在最低阶情形下拥有很少的全局自由度。我们给出了若干数值结果以验证理论估计。

**关键词**：线弹性；稳定化混合有限元方法；误差分析；单纯形网格；Inf-Sup 条件。

---

# 1 引言

设 $\Omega \subset \mathbb{R}^n$ 为有界多面体，记 $\mathbb{S}$ 为全体 $n \times n$ 对称张量构成的空间。在载荷 $f \in L^2(\Omega; \mathbb{R}^n)$ 作用下，线弹性问题的 Hellinger–Reissner 混合形式为：求 $(\sigma, u) \in \Sigma \times V := H(\mathrm{div}, \Omega; \mathbb{S}) \times L^2(\Omega; \mathbb{R}^n)$，使得
$$
a(\sigma, \tau) + b(\tau, u) = 0 \qquad \forall \tau \in \Sigma,
\tag{1.1}
$$
$$
-b(\sigma, v) = \int_\Omega f \cdot v \, \mathrm{d}x \qquad \forall v \in V,
\tag{1.2}
$$
其中
$$
a(\sigma, \tau) := \int_\Omega \mathcal{A}\sigma : \tau \, \mathrm{d}x, \qquad b(\tau, v) := \int_\Omega \operatorname{div}\tau \cdot v \, \mathrm{d}x,
$$
$\mathcal{A}$ 为四阶柔度张量，定义为
$$
\mathcal{A}\sigma := \frac{1}{2\mu}\left(\sigma - \frac{\lambda}{n\lambda + 2\mu}(\mathrm{tr}\,\sigma)\delta\right).
$$
这里 $\delta := (\delta_{ij})_{n \times n}$ 为 Kronecker 张量，$\mathrm{tr}$ 为迹算子，正常数 $\lambda$ 与 $\mu$ 为 Lamé 常数。由于应力张量的对称性要求，设计具有多项式形函数的 $H(\mathrm{div}, \Omega; \mathbb{S})$ 协调有限元十分困难。因此在上个世纪，复合单元是逼近应力的主要选择之一（参见 [7, 30, 46, 56]）。

本世纪初，Arnold 与 Winther 在 [10] 中构造了二维情形下首个具有多项式形函数的 $H(\mathrm{div}, \Omega; \mathbb{S})$ 协调混合有限元，该单元随后在 [1, 4] 中被推广到三维四面体网格，在 [42] 中被推广到任意维单纯形网格。在这些单元中，位移空间由 $L^2(\Omega; \mathbb{R}^n)$-$P_{k-1}$ 逼近，应力空间则由 $H(\mathrm{div}, \Omega; \mathbb{S})$-$P_{k+n-1}$ 中散度属于 $L^2(\Omega; \mathbb{R}^n)$-$P_{k-1}$ 的函数构成的空间逼近，$k \ge 2$。最近，Hu 与 Zhang 在 [40, 41] 中证明了更紧凑的一对空间 $H(\mathrm{div}, \Omega; \mathbb{S})$-$P_k$ 与 $L^2(\Omega; \mathbb{R}^n)$-$P_{k-1}$ 在三角形与四面体网格（$n = 2, 3$）上对 $k \ge n+1$ 稳定；Hu 在 [37] 中将这些稳定有限元推广到任意维单纯形网格上 $k \ge n+1$ 的情形。其中的一个关键观察是：每个单元上多项式 $H(\mathrm{div})$ 泡函数空间的散度空间，恰好是分片刚体运动空间关于离散位移空间的正交补空间。随后，通过用 $H^1(\Omega; \mathbb{S})$-$P_k$ 空间控制分片刚体运动空间，证明了 $k \ge n+1$ 时的离散 inf-sup 条件。然而，要证明 $H(\mathrm{div}, \Omega; \mathbb{S})$-$P_k$ 与 $L^2(\Omega; \mathbb{R}^n)$-$P_{k-1}$ 这一对空间在 $1 \le k \le n$ 时仍然稳定，则颇为棘手。为此，Hu 与 Zhang 在 [42] 中对每个 $n-1$ 维单形，用分片多项式的 $H(\mathrm{div}, \Omega; \mathbb{S})$-$P_{n+1}$ 面泡函数丰富了 $H(\mathrm{div}, \Omega; \mathbb{S})$-$P_k$ 空间。Gong、Wu 与 Xu 在 [31] 中利用非协调对称应力逼近构造了两类内罚混合有限元方法，这些非协调混合方法的稳定性由 $H(\mathrm{div})$ 非协调面泡函数空间保证。[21] 研究了一种用 Crouzeix–Raviart 非协调线性元逼近应力的内罚混合有限元方法。为了去掉 $H(\mathrm{div}, \Omega; \mathbb{S})$ 协调元中出现的顶点自由度，并使所得混合有限元方法可杂交化，[5, 11, 32, 57] 发展了三角形与四面体网格上的非协调混合元。矩形网格上的对称协调混合有限元参见 [3, 12, 23, 36, 38]，对称非协调混合有限元参见 [39, 47, 58, 59]。为了在保持离散应力空间对称性的同时放松其跨剖分内部面的连续性，人们提出了许多间断 Galerkin 方法 [20, 24, 27, 43–45]、可杂交化间断 Galerkin 方法 [35, 51]、弱 Galerkin 方法 [22, 55] 以及杂交高阶（hybrid high-order）方法 [29]。线弹性问题的弱对称混合有限元方法参见 [2, 6, 8, 9, 15, 26, 28, 33, 34, 48–50, 53]。

本文旨在用尽可能少的全局自由度，为线弹性问题设计稳定的混合有限元方法。为此，我们提出任意维单纯形网格上的两类稳定化混合有限元方法。在第一类方法中，对 $1 \le k \le n$，我们采用 [37] 中构造的 $H(\mathrm{div}, \Omega; \mathbb{S})$-$P_k$ 与 $L^2(\Omega; \mathbb{R}^n)$-$P_{k-1}$ 分别逼近应力与位移。为简化记号，我们用上标 $(\cdot)^{\mathrm{div}}$ 表示 $H(\mathrm{div}, \Omega; \mathbb{S})$ 协调元，$(\cdot)^{-1}$ 表示间断元，$(\cdot)^{0}$ 表示 $H^1(\Omega; \mathbb{R}^n)$ 或 $H^1(\Omega; \mathbb{S})$ 连续元。与 [31, 42] 中用分片多项式面泡函数丰富 $P_k^{\mathrm{div}}$ 元的做法不同，我们受 [24] 中为线弹性问题构造的间断 Galerkin 方法启发，在 Hellinger–Reissner 混合形式中加入一个跃度稳定化项，使离散方法稳定。借助 [37, 40, 41] 中建立的部分 inf-sup 条件 (2.1) 与一个精心设计的应力插值算子，我们建立了紧凑形式的离散 inf-sup 条件，进而给出所得稳定化 $P_k^{\mathrm{div}} - P_{k-1}^{-1}$ 元的先验误差分析。

在第二类稳定化混合有限元方法中，我们采用 [19] 建议的稳定化技术，并用 $H_0^1(\Omega; \mathbb{R}^n)$-$P_k$ 逼近位移空间。该稳定化技术的优点在于，与应力相关的双线性型的强制性条件自动成立，因而只需关注离散 inf-sup 条件。为恢复 inf-sup 条件，我们首先用每个单元上 $(k+1)$ 次多项式 $H(\mathrm{div})$ 泡函数空间丰富的 $H^1(\Omega; \mathbb{S})$-$P_k$ 逼近应力空间。离散 inf-sup 条件借助另一个特殊的应力插值算子建立，随后由混合有限元方法的标准理论导出 $(P_k^0 + B_{k+1}^{\mathrm{div}}) - P_k^0$ 的先验误差估计。然而，由于与 $H(\mathrm{div})$ 范数度量的应力误差相耦合，位移在 $L^2(\Omega; \mathbb{R}^n)$ 范数下的收敛阶是次优的。为弥补这一点，我们改用 $H(\mathrm{div}, \Omega; \mathbb{S})$-$P_{k+1}$ 逼近应力空间，所得的稳定有限元对即 Hood–Taylor 型 $P_{k+1}^{\mathrm{div}} - P_k^0$。[19] 中曾提到，尚不清楚 [13, 14, 54] 中的 Hood–Taylor 元对线弹性问题是否稳定。我们通过在每个单元上用同次多项式 $H(\mathrm{div})$ 泡函数空间丰富应力的 Hood–Taylor 元空间 $P_{k+1}^0$，解决了这一问题。

注意，构造前述两个插值算子的关键要素是每个单元上多项式的 $H(\mathrm{div})$ 泡函数空间。需要指出，对于应力，我们在 $H(\mathrm{div}, \Omega; \mathbb{S})$ 范数下得到了最优误差估计，而在 $L^2(\Omega; \mathbb{S})$ 范数下的误差估计是次优的。据我们所知，在最低阶情形 $k = 1$，本文方法的全局自由度少于文献中任何已有的线弹性混合型对称有限元方法。具体而言，$k = 1$ 时稳定化混合有限元方法 (3.1)–(3.2)、(4.1)–(4.2) 与 (4.9)–(4.10) 的应力与位移全局自由度分别为
$$
\frac{n(n+1)}{2}|\mathcal{V}| + n|\mathcal{T}|, \qquad
\frac{n(n+1)}{2}\big(|\mathcal{V}| + |\mathcal{T}|\big) + n|\mathcal{V}|, \qquad
\frac{n(n+1)}{2}|\mathcal{V}| + \frac{(n-1)(n+2)}{2}|\mathcal{E}| + \frac{n(n+1)}{2}|\mathcal{T}| + n|\mathcal{V}|.
$$
这里 $|\mathcal{V}|$、$|\mathcal{E}|$、$|\mathcal{T}|$ 分别为剖分的顶点数、棱数与单元数。

当位移采用相同次数的多项式空间时，Hood–Taylor 型元 $P_{k+1}^{\mathrm{div}} - P_k^0$ 与稳定化元 $P_{k+1}^{\mathrm{div}} - P_k^{-1}$ 具有相同的收敛阶，比稳定化元 $(P_k^0 + B_{k+1}^{\mathrm{div}}) - P_k^0$ 高一阶。值得一提的是，为达到相同的收敛阶，稳定化元 $P_{k+1}^{\mathrm{div}} - P_k^{-1}$ 比 Hood–Taylor 型元 $P_{k+1}^{\mathrm{div}} - P_k^0$ 需要更多的全局自由度。

本文其余部分组织如下。第 2 节给出后文所用的记号与定义。第 3 节针对线弹性问题设计并分析一种间断位移的稳定化混合有限元方法。第 4 节针对线弹性问题提出第二类连续位移的稳定化混合有限元方法。第 5 节给出若干数值实验以验证理论结果。

---

# 2 预备知识（Preliminaries）

设 $\mathcal{T}_h$ 为区域 $\Omega$ 的形状正则单纯形网格，$\mathcal{F}_h$ 为所有 $n-1$ 维面的集合。对任意 $F \in \mathcal{F}_h$，其直径记为 $h_F$。$P_m(G)$ 表示区域 $G$ 上总次数不超过 $m$ 的多项式空间。

### 对称张量面跃度算子 $\mathcal{J}\cdot\mathcal{K}$

设两个相邻单纯形 $K^+$ 与 $K^-$ 共享内界面 $F$，单位外法向分别为 $\nu^+$ 与 $\nu^-$。对于向量值函数 $w$，记 $w^+ := w|_{K^+}, w^- := w|_{K^-}$。定义矩阵值跃度为：
$$
\mathcal{J}w\mathcal{K} := \frac{1}{2}\left(w^+(\nu^+)^{\mathsf T} + \nu^+(w^+)^{\mathsf T} + w^-(\nu^-)^{\mathsf T} + \nu^-(w^-)^{\mathsf T}\right).
$$
在边界 $\partial\Omega$ 上的面 $F$ 上，定义为：
$$
\mathcal{J}w\mathcal{K} := \frac{1}{2}\left(w\nu^{\mathsf T} + \nu w^{\mathsf T}\right).
$$

### 局部 $H(\mathrm{div})$ 泡函数空间与代数特征

对于每个单元 $K \in \mathcal{T}_h$，定义 $k$ 次 $H(\mathrm{div}, K; \mathbb{S})$ 泡函数空间为：
$$
B_{K,k} := \left\{\tau \in P_k(K; \mathbb{S}) : \tau\nu|_{\partial K} = 0\right\}.
$$
易知 $B_{K,1} = \{0\}$。当 $k \ge 2$ 时，设 $x_0, \dots, x_n$ 为 $K$ 的顶点，$\lambda_i$ 为对应重心坐标。对棱边 $x_i x_j$（$i \ne j$），设切向量为 $t_{i,j}$，$T_{i,j} := t_{i,j} t_{i,j}^{\mathsf T}$，则（Hu 2015）：
$$
B_{K,k} = \sum_{0 \le i < j \le n} \lambda_i \lambda_j P_{k-2}(K) T_{i,j}.
$$
全局空间定义为：
$$
\begin{aligned}
B_{k,h} &:= \left\{\tau \in H(\mathrm{div}, \Omega; \mathbb{S}) : \tau|_K \in B_{K,k}, \forall K \in \mathcal{T}_h\right\}, \\
\widetilde{\Sigma}_{k,h} &:= \left\{\tau \in H^1(\Omega; \mathbb{S}) : \tau|_K \in P_k(K; \mathbb{S}), \forall K \in \mathcal{T}_h\right\}, \\
\Sigma_{k,h} &:= \widetilde{\Sigma}_{k,h} + B_{k,h}, \\
V_{k-1,h} &:= \left\{v \in L^2(\Omega; \mathbb{R}^n) : v|_K \in P_{k-1}(K; \mathbb{R}^n), \forall K \in \mathcal{T}_h\right\}.
\end{aligned}
$$
单元 $K$ 上的局部刚体运动空间 $\mathcal{R}(K)$ 及其在 $P_{k-1}(K; \mathbb{R}^n)$ 上的正交补定义为：
$$
\begin{aligned}
\mathcal{R}(K) &:= \left\{v \in H^1(K; \mathbb{R}^n) : \varepsilon(v) = 0\right\}, \\
\mathcal{R}^\perp(K) &:= \left\{v \in P_{k-1}(K; \mathbb{R}^n) : \int_K v \cdot w \, \mathrm{d}x = 0, \forall w \in \mathcal{R}(K)\right\}.
\end{aligned}
$$
由 Hu & Zhang（2014, 2015）与 Hu（2015），核心恒等式成立：
$$
\mathcal{R}^\perp(K) = \operatorname{div} B_{K,k}, \quad \forall K \in \mathcal{T}_h.
\tag{2.1}
$$

### 自由度与泡函数插值算子

**引理 2.1**：矩阵场 $\tau \in P_k(K; \mathbb{S})$ 可由以下自由度唯一确定：
1. 对 $K$ 的每个 $\ell$ 维单纯形 $\Delta_\ell$（$0 \le \ell \le n-1$），具 $\ell$ 个线性无关切向 $t_1, \dots, t_\ell$ 与 $n-\ell$ 个线性无关法向 $\nu_1, \dots, \nu_{n-\ell}$，量 $t_l^{\mathsf T}\tau\nu_i$ 与 $\nu_i^{\mathsf T}\tau\nu_j$ 在 $\Delta_\ell$ 上不超过 $k-\ell-1$ 次的各阶矩（$l=1,\dots,\ell; i,j=1,\dots,n-\ell$）；
2. 单元矩：对任意 $\varsigma \in P_{k-2}(K; \mathbb{S})$ 的取值 $\int_K \tau : \varsigma \, \mathrm{d}x$。

**单元泡函数插值算子** $I_{k,h}^b$：对任意 $\tau \in L^2(\Omega; \mathbb{S})$，定义 $I_{k,h}^b \tau \in \Sigma_{k,h}$ 满足：
- 引理 2.1 的第一组自由度取值全为 0；
- 对任意 $\varsigma \in P_{k-2}(K; \mathbb{S})$，$\int_K I_{k,h}^b \tau : \varsigma \, \mathrm{d}x = \int_K \tau : \varsigma \, \mathrm{d}x$。

由此定义的插值算子属于泡函数空间 $I_{k,h}^b \tau \in B_{k,h}$，并满足局部稳定性估计：
$$
\|I_{k,h}^b \tau\|_{0,K} \lesssim \|\tau\|_{0,K}, \quad \forall K \in \mathcal{T}_h.
\tag{2.3}
$$

---

# 3 间断位移的稳定化混合有限元方法

对于 $1 \le k \le n$，间断位移稳定化混合格式为：求 $(\sigma_h, u_h) \in \Sigma_{k,h} \times V_{k-1,h}$ 使得：
$$
\begin{aligned}
a(\sigma_h, \tau_h) + b(\tau_h, u_h) &= 0 \quad &&\forall \tau_h \in \Sigma_{k,h}, \\
-b(\sigma_h, v_h) + c(u_h, v_h) &= \int_\Omega f \cdot v_h \, \mathrm{d}x \quad &&\forall v_h \in V_{k-1,h},
\end{aligned}
\tag{3.1--3.2}
$$
其中位移跃度稳定化双线性型与对应半范数定义为：
$$
c(u_h, v_h) := \sum_{F \in \mathcal{F}_h} h_F \int_F \mathcal{J}u_h\mathcal{K} : \mathcal{J}v_h\mathcal{K} \, \mathrm{d}s, \qquad \|v_h\|_c^2 := c(v_h, v_h).
$$
复合范数记为 $\|v_h\|_{0,c}^2 := \|v_h\|_0^2 + \|v_h\|_c^2$。

### 复合插值算子与逼近性质

设 $I_h^{\mathrm{SZ}}$ 为张量/向量形式的 Scott–Zhang 插值算子。对 $\tau \in H^1(\Omega; \mathbb{S})$，构造复合插值算子：
$$
I_h \tau := I_h^{\mathrm{SZ}}\tau + I_{k,h}^b(\tau - I_h^{\mathrm{SZ}}\tau) \in \Sigma_{k,h}.
$$
其满足正交性质：
$$
\int_K (I_h \tau - \tau) : \varsigma \, \mathrm{d}x = 0, \quad \forall \varsigma \in P_{k-2}(K; \mathbb{S}), \forall K \in \mathcal{T}_h.
\tag{3.4}
$$
**引理 3.1**：对整数 $m, k \ge 1$ 与任意 $\tau \in H^m(\Omega; \mathbb{S})$，有：
$$
\sum_{K \in \mathcal{T}_h} h_K^{-2}\left(\|\tau - I_h \tau\|_{0,K}^2 + h_K \|\tau - I_h \tau\|_{0,\partial K}^2\right) \lesssim h^{2\min\{k, m-1\}} \|\tau\|_m^2.
\tag{3.5}
$$

### 紧凑双线性型与离散 Inf-Sup 条件

将问题写为紧凑形式：求 $(\sigma_h, u_h) \in \Sigma_{k,h} \times V_{k-1,h}$ 使得
$$
\mathcal{B}(\sigma_h, u_h; \tau_h, v_h) = \int_\Omega f \cdot v_h \, \mathrm{d}x, \quad \forall (\tau_h, v_h) \in \Sigma_{k,h} \times V_{k-1,h},
$$
其中：
$$
\mathcal{B}(\sigma_h, u_h; \tau_h, v_h) := a(\sigma_h, \tau_h) + b(\tau_h, u_h) - b(\sigma_h, v_h) + c(u_h, v_h).
$$
**引理 3.2（离散 Inf-Sup 条件）**：对任意 $(\tilde{\sigma}_h, \tilde{u}_h) \in \Sigma_{k,h} \times V_{k-1,h}$，成立：
$$
\|\tilde{\sigma}_h\|_{H(\mathrm{div},\mathcal{A})} + \|\tilde{u}_h\|_{0,c} \lesssim \sup_{(\tau_h, v_h) \in \Sigma_{k,h} \times V_{k-1,h}} \frac{\mathcal{B}(\tilde{\sigma}_h, \tilde{u}_h; \tau_h, v_h)}{\|\tau_h\|_{H(\mathrm{div},\mathcal{A})} + \|v_h\|_{0,c}}.
\tag{3.8}
$$
*证明要点*：对给定的 $(\tilde{\sigma}_h, \tilde{u}_h)$，检验函数取为：
$$
\tau_h = \tilde{\sigma}_h + \gamma_1 \tau_1 + \gamma_2 I_h \tau_2, \qquad v_h = \tilde{u}_h - \gamma_3 \operatorname{div}\tilde{\sigma}_h,
$$
其中：
1. $\tau_1 \in B_{k,h}$ 满足 $\operatorname{div}\tau_1 = \tilde{u}_h^\perp$（利用了泡函数空间的散度映射性质 (2.1)）；
2. $\tau_2 \in H_0^1(\Omega; \mathbb{S})$ 满足连续层面的散度方程 $\operatorname{div}\tau_2 = \tilde{u}_h - \tilde{u}_h^\perp$，通过分部积分与正交性 (3.4) 将残差转化为边界跃度项；
3. 通过逆不等式控制 $\|\operatorname{div}\tilde{\sigma}_h\|_c \le C_3 \|\operatorname{div}\tilde{\sigma}_h\|_0$；
4. 选取参数 $\gamma_1 = \frac{2}{3C_1^2}$，$\gamma_2 = \min\left\{\frac{2}{9C_2^2}, \frac{\gamma_1}{1+3C_2^2}\right\}$，$\gamma_3 = \frac{2}{3C_3^2}$，吸收各项交叉项后得到全局正定性与 inf-sup 稳定性。

### 先验误差估计

**定理 3.3**：设 $(\sigma, u)$ 为式 (1.1)–(1.2) 的精确解，$(\sigma_h, u_h)$ 为采用 $P_k^{\mathrm{div}} - P_{k-1}^{-1}$ 单元的稳定化混合格式 (3.1)–(3.2) 的离散解。若 $\sigma \in H^{k+1}(\Omega; \mathbb{S})$ 且 $u \in H^k(\Omega; \mathbb{R}^n)$，则：
$$
\|\sigma - \sigma_h\|_{H(\mathrm{div},\mathcal{A})} + \|u - u_h\|_{0,c} \lesssim h^k\left(\|\sigma\|_{k+1} + \|u\|_k\right).
$$

---

# 4 连续位移的两类稳定化混合有限元方法

采用 Brezzi, Fortin & Marini（1993）建议的稳定化技术，位移采用连续有限元逼近。定义有限元空间：
$$
\Sigma_{k,h}^* := \widetilde{\Sigma}_{k,h} + B_{k+1,h}, \qquad W_{k,h} := V_{k,h} \cap H_0^1(\Omega; \mathbb{R}^n).
$$

### 第一种格式：$(P_k^0 + B_{k+1}^{\mathrm{div}}) - P_k^0$

变分格式为：求 $(\sigma_h, u_h) \in \Sigma_{k,h}^* \times W_{k,h}$ 使得：
$$
\begin{aligned}
a^*(\sigma_h, \tau_h) + b(\tau_h, u_h) &= -\int_\Omega f \cdot \operatorname{div}\tau_h \, \mathrm{d}x \quad &&\forall \tau_h \in \Sigma_{k,h}^*, \\
-b(\sigma_h, v_h) &= \int_\Omega f \cdot v_h \, \mathrm{d}x \quad &&\forall v_h \in W_{k,h},
\end{aligned}
\tag{4.1--4.2}
$$
其中双线性型 $a^*(\cdot, \cdot)$ 定义为：
$$
a^*(\sigma_h, \tau_h) := a(\sigma_h, \tau_h) + \int_\Omega \operatorname{div}\sigma_h \cdot \operatorname{div}\tau_h \, \mathrm{d}x.
$$
**优点**：双线性型 $a^*(\cdot, \cdot)$ 在 $H(\mathrm{div}, \Omega; \mathbb{S})$ 上关于范数 $\|\cdot\|_{H(\mathrm{div},\mathcal{A})}$ 的强制性自动成立。

定义高阶泡函数插值算子 $I_h^* \tau := I_h^{\mathrm{SZ}}\tau + I_{k+1,h}^b(\tau - I_h^{\mathrm{SZ}}\tau)$，其正交性为：
$$
\int_K (I_h^* \tau - \tau) : \varsigma \, \mathrm{d}x = 0, \quad \forall \varsigma \in P_{k-1}(K; \mathbb{S}), \forall K \in \mathcal{T}_h.
\tag{4.3}
$$
由此导出：
$$
b(I_h^* \tau, v_h) = b(\tau, v_h), \quad \forall \tau \in H^1(\Omega; \mathbb{S}), \forall v_h \in W_{k,h}.
\tag{4.5}
$$
**引理 4.2（离散 Inf-Sup 条件）**：
$$
\|v_h\|_0 \lesssim \sup_{0 \ne \tau_h \in \Sigma_{k,h}^*} \frac{b(\tau_h, v_h)}{\|\tau_h\|_{H(\mathrm{div},\mathcal{A})}}, \quad \forall v_h \in W_{k,h}.
\tag{4.6}
$$
**定理 4.3（误差估计）**：若 $\sigma \in H^{k+1}(\Omega; \mathbb{S})$ 且 $u \in H^{k+1}(\Omega; \mathbb{R}^n)$，则：
$$
\|\sigma - \sigma_h\|_{H(\mathrm{div},\mathcal{A})} + \|u - u_h\|_0 \lesssim h^k\left(\|\sigma\|_{k+1} + h\|u\|_{k+1}\right).
$$
注意：位移在 $L^2$ 模下的收敛阶为 $O(h^k)$，相对于位移空间多项式次数 $k$ 是次优的（受限于应力 $H(\mathrm{div})$ 误差的耦合）。

### 第二种格式：Hood–Taylor 型 $P_{k+1}^{\mathrm{div}} - P_k^0$

为恢复位移在 $L^2$ 模下的最优收敛率，将应力有限元空间进一步丰富至 $\Sigma_{k+1,h}$：
求 $(\sigma_h, u_h) \in \Sigma_{k+1,h} \times W_{k,h}$ 使得：
$$
\begin{aligned}
a^*(\sigma_h, \tau_h) + b(\tau_h, u_h) &= -\int_\Omega f \cdot \operatorname{div}\tau_h \, \mathrm{d}x \quad &&\forall \tau_h \in \Sigma_{k+1,h}, \\
-b(\sigma_h, v_h) &= \int_\Omega f \cdot v_h \, \mathrm{d}x \quad &&\forall v_h \in W_{k,h}.
\end{aligned}
\tag{4.9--4.10}
$$
**推论 4.4（最优收敛阶）**：在 $\sigma \in H^{k+2}(\Omega; \mathbb{S})$ 与 $u \in H^{k+1}(\Omega; \mathbb{R}^n)$ 的正则性假定下：
$$
\|\sigma - \sigma_h\|_{H(\mathrm{div},\mathcal{A})} + \|u - u_h\|_0 \lesssim h^{k+1}\left(\|\sigma\|_{k+2} + \|u\|_{k+1}\right).
\tag{4.11}
$$

**注记 4.5（解决 Hood–Taylor 元弹性稳定性悬案）**：
有限元对 $\Sigma_{k+1,h} \times W_{k,h}$ 恰好是流体力学经典的 Hood–Taylor 元（Taylor & Hood 1973; Boffi 1994, 1997）由单元多项式 $H(\mathrm{div})$ 泡函数空间 $B_{k+1,h}$ 补充增强而得。因此，本文对 Brezzi, Fortin & Marini（1993, Example 3.3）提出的“Hood–Taylor 元对于线弹性力学是否稳定”给出了肯定的解答。

**注记 4.6（右端无载荷惩罚项的变体格式）**：
为了保持如 (1.1) 与 (3.1) 那样的右端零向量结构，可采用以下变体格式：求 $(\sigma_h, u_h) \in \Sigma_{k+1,h} \times W_{k,h}$ 使得：
$$
\begin{aligned}
a^\circ(\sigma_h, \tau_h) + b(\tau_h, u_h) &= 0 \quad &&\forall \tau_h \in \Sigma_{k+1,h}, \\
-b(\sigma_h, v_h) &= \int_\Omega f \cdot v_h \, \mathrm{d}x \quad &&\forall v_h \in W_{k,h},
\end{aligned}
$$
其中双线性型为：
$$
a^\circ(\sigma, \tau) := \int_\Omega \mathcal{A}\sigma : \tau \, \mathrm{d}x + \sum_{F \in \mathcal{F}_h} h_F \int_F [\operatorname{div}\sigma] \cdot [\operatorname{div}\tau] \, \mathrm{d}s.
$$
其在核空间 $K_h := \{\tau_h \in \Sigma_{k+1,h} : b(\tau_h, v_h) = 0, \forall v_h \in W_{k,h}\}$ 上关于范数 $\interleave \tau_h \interleave^2 := \|\tau_h\|_{H(\mathrm{div},\mathcal{A})}^2 + \sum_{F \in \mathcal{F}_h} h_F \|[\operatorname{div}\tau_h]\|_{0,F}^2$ 满足强制性。

---

# 5 数值结果（Numerical Results）

设置弹性力学参数 $\lambda = 0.3, \mu = 0.35$，在区域 $\Omega$ 的均匀单纯形网格剖分 $\mathcal{T}_h$ 上进行测试。

### 5.1 二维纯位移问题（$\Omega = (-1, 1)^2$）

解析位移场设为：
$$
u(x_1, x_2) = \begin{pmatrix}
x_1 (1 - x_1^2)(1 - x_2^2)^2 \\
x_2 (1 - x_2^2)(1 - x_1^2)^2
\end{pmatrix} - \frac{80}{7}\begin{pmatrix}
-x_2 (1 - x_2^2)(1 - x_1^2)^2 \\
x_1 (1 - x_1^2)(1 - x_2^2)^2
\end{pmatrix},
$$
精确应力由本构关系 $\sigma = 2\mu\varepsilon(u) + \lambda(\mathrm{tr}\,\varepsilon(u))\delta$ 计算得出，外力载荷 $f = -\operatorname{div}\sigma$。

图 1 给出了二维单纯形单元上应力有限元空间 $\Sigma_{2,h}$ 局部自由度的几何分布记忆示意图：

![[Chen2017_Fig1.png]]

**图 1：二维中 $\Sigma_{2,h}$ 的单元局部自由度示意图。**

对于间断位移稳定化单元 $P_k^{\mathrm{div}} - P_{k-1}^{-1}$，在 $k=1$（此时因泡函数空间 $B_{K,1}=\{0\}$，退化为连续应力空间 $P_1^0$）与 $k=2$ 时的数值误差 $\|\sigma - \sigma_h\|_{H(\mathrm{div},\mathcal{A})}$、$\|u_h\|_c$ 与 $\|u - u_h\|_0$ 随网格尺寸 $h$ 的变化分别列于表 1 与表 2。从表中可以观察到，全部三项误差均数值上达到了最优收敛阶 $O(h^k)$，与定理 3.3 的理论分析结论一致。


**表 1：二维稳定化 $P_1^0 - P_0^{-1}$ 单元数值误差**

| $h$ | $\Vert \sigma - \sigma_h \Vert_{H(\mathrm{div},\mathcal{A})}$ | 收敛阶 | $\Vert u_h \Vert_c$ | 收敛阶 | $\Vert u - u_h \Vert_0$ | 收敛阶 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $2^{-1}$ | 1.9436E+01 | — | 5.7136E+00 | — | 2.8981E+00 | — |
| $2^{-2}$ | 1.0703E+01 | 0.86 | 3.7894E+00 | 0.59 | 1.6073E+00 | 0.85 |
| $2^{-3}$ | 5.7982E+00 | 0.88 | 2.1600E+00 | 0.81 | 8.3356E-01 | 0.95 |
| $2^{-4}$ | 3.0580E+00 | 0.92 | 1.1484E+00 | 0.91 | 4.2521E-01 | 0.97 |
| $2^{-5}$ | 1.5780E+00 | 0.95 | 5.9220E-01 | 0.96 | 2.1527E-01 | 0.98 |
| $2^{-6}$ | 8.0346E-01 | 0.97 | 3.0101E-01 | 0.98 | 1.0848E-01 | 0.99 |
| $2^{-7}$ | 4.0590E-01 | 0.99 | 1.5187E-01 | 0.99 | 5.4494E-02 | 0.99 |

**表 2：二维稳定化 $P_2^{\mathrm{div}} - P_1^{-1}$ 单元数值误差**

|   $h$    | $\Vert \sigma - \sigma_h \Vert_{H(\mathrm{div},\mathcal{A})}$ | 收敛阶  | $\Vert u_h \Vert_c$ | 收敛阶  | $\Vert u - u_h \Vert_0$ | 收敛阶  |
| :------: | :-----------------------------------------------------------: | :--: | :-----------------: | :--: | :---------------------: | :--: |
|   $1$    |                          1.1868E+01                           |  —   |     5.0478E+00      |  —   |       2.4374E+00        |  —   |
| $2^{-1}$ |                          4.6400E+00                           | 1.35 |     1.7436E+00      | 1.53 |       7.1254E-01        | 1.77 |
| $2^{-2}$ |                          1.4841E+00                           | 1.64 |     4.6132E-01      | 1.92 |       1.8285E-01        | 1.96 |
| $2^{-3}$ |                          4.2227E-01                           | 1.81 |     1.1783E-01      | 1.97 |       4.6102E-02        | 1.99 |
| $2^{-4}$ |                          1.1120E-01                           | 1.92 |     2.9546E-02      | 2.00 |       1.1556E-02        | 2.00 |
| $2^{-5}$ |                          2.8378E-02                           | 1.97 |     7.3651E-03      | 2.00 |       2.8912E-03        | 2.00 |
| $2^{-6}$ |                          7.1562E-03                           | 1.99 |     1.8358E-03      | 2.00 |       7.2294E-04        | 2.00 |

连续位移稳定化混合有限元方法 (4.1)–(4.2) 在 $k=1$ 时的数值结果列于表 3。可见应力误差 $\Vert \sigma - \sigma_h \Vert_{H(\mathrm{div},\mathcal{A})}$ 的收敛阶为 $O(h)$，与定理 4.3 相符；位移误差 $\Vert u - u_h \Vert_0$ 的收敛阶约为 1.7，高于定理 4.3 预测的理论阶（1.0），但仍属于次优阶。

**表 3：二维稳定化 $(P_1^0 + B_2^{\mathrm{div}}) - P_1^0$ 单元数值误差**

| $h$ | $\Vert \sigma - \sigma_h \Vert_{H(\mathrm{div},\mathcal{A})}$ | 收敛阶 | $\Vert u - u_h \Vert_0$ | 收敛阶 |
|:---:|:---:|:---:|:---:|:---:|
| $2^{-1}$ | 1.3570E+01 | — | 5.9057E+00 | — |
| $2^{-2}$ | 7.5576E+00 | 0.84 | 2.1407E+00 | 1.46 |
| $2^{-3}$ | 4.1592E+00 | 0.86 | 6.2487E-01 | 1.78 |
| $2^{-4}$ | 2.2977E+00 | 0.86 | 1.9626E-01 | 1.67 |
| $2^{-5}$ | 1.2391E+00 | 0.89 | 6.2250E-02 | 1.66 |
| $2^{-6}$ | 6.4969E-01 | 0.93 | 1.9087E-02 | 1.71 |
| $2^{-7}$ | 3.3399E-01 | 0.96 | 5.7719E-03 | 1.73 |

Hood–Taylor 型连续位移稳定化混合有限元方法 (4.9)–(4.10) 在 $k=1$ 时的数值结果列于表 4。应力误差 $\Vert \sigma - \sigma_h \Vert_{H(\mathrm{div},\mathcal{A})}$ 与位移误差 $\Vert u - u_h \Vert_0$ 均达到了最优的 $O(h^2)$ 收敛阶，证实了推论 4.4 式 (4.11) 的理论估计。

**表 4：二维稳定化 $P_2^{\mathrm{div}} - P_1^0$ 单元数值误差**

| $h$ | $\Vert \sigma - \sigma_h \Vert_{H(\mathrm{div},\mathcal{A})}$ | 收敛阶 | $\Vert u - u_h \Vert_0$ | 收敛阶 |
|:---:|:---:|:---:|:---:|:---:|
| $1$ | 1.0966E+01 | — | 6.0260E+00 | — |
| $2^{-1}$ | 3.5092E+00 | 1.64 | 1.5579E+00 | 1.95 |
| $2^{-2}$ | 9.0380E-01 | 1.96 | 3.3148E-01 | 2.23 |
| $2^{-3}$ | 2.2504E-01 | 2.01 | 7.2219E-02 | 2.20 |
| $2^{-4}$ | 5.5922E-02 | 2.01 | 1.6506E-02 | 2.13 |
| $2^{-5}$ | 1.3981E-02 | 2.00 | 4.1182E-03 | 2.00 |
| $2^{-6}$ | 3.4746E-03 | 2.01 | 9.5159E-04 | 2.11 |

### 5.2 三维纯位移问题（$\Omega = (0, 1)^3$）

在单位立方体区域 $\Omega = (0, 1)^3$ 上求解纯位移问题，解析位移场取为：
$$
u(x_1, x_2, x_3) = \begin{pmatrix}
24 \\ 25 \\ 26
\end{pmatrix} x_1(1 - x_1) x_2(1 - x_2) x_3(1 - x_3).
$$
精确应力 $\sigma$ 与体力载荷 $f$ 由式 (1.1)–(1.2) 导出。

表 5 与表 6 汇总了间断位移稳定化单元 $P_k^{\mathrm{div}} - P_{k-1}^{-1}$ 在 $k=1, 2$ 时的数值误差。容易看出，误差 $\Vert \sigma - \sigma_h \Vert_{H(\mathrm{div},\mathcal{A})}$、$\Vert u_h \Vert_c$ 与 $\Vert u - u_h \Vert_0$ 的数值收敛阶均为最优的 $O(h^k)$，由定理 3.3 给予理论保证。

<center><b>
表 5：三维稳定化 $P_1^0 - P_0^{-1}$ 单元数值误差（Table 5. Numerical errors for the stabilized $P_1^0 - P_0^{-1}$ element in 3D）
</b></center>

| $h$ | $\Vert \sigma - \sigma_h \Vert_{H(\mathrm{div},\mathcal{A})}$ | 收敛阶 | $\Vert u_h \Vert_c$ | 收敛阶 | $\Vert u - u_h \Vert_0$ | 收敛阶 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $2^{-1}$ | 4.1723E+00 | — | 4.0747E-01 | — | 2.4720E-01 | — |
| $2^{-2}$ | 2.3595E+00 | 0.82 | 3.5554E-01 | 0.20 | 1.7403E-01 | 0.51 |
| $2^{-3}$ | 1.2849E+00 | 0.88 | 2.5527E-01 | 0.48 | 1.1168E-01 | 0.64 |
| $2^{-4}$ | 6.8023E-01 | 0.92 | 1.5243E-01 | 0.74 | 6.3889E-02 | 0.81 |
| $2^{-5}$ | 3.5167E-01 | 0.95 | 8.3310E-02 | 0.87 | 3.4309E-02 | 0.90 |

<center><b>
表 6：三维稳定化 $P_2^{\mathrm{div}} - P_1^{-1}$ 单元数值误差（Table 6. Numerical errors for the stabilized $P_2^{\mathrm{div}} - P_1^{-1}$ element in 3D）
</b></center>

| $h$ | $\Vert \sigma - \sigma_h \Vert_{H(\mathrm{div},\mathcal{A})}$ | 收敛阶 | $\Vert u_h \Vert_c$ | 收敛阶 | $\Vert u - u_h \Vert_0$ | 收敛阶 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $2^{-1}$ | 1.4440E+00 | — | 1.7738E-01 | — | 8.3035E-02 | — |
| $2^{-2}$ | 3.8864E-01 | 1.89 | 5.2337E-02 | 1.76 | 2.2979E-02 | 1.85 |
| $2^{-3}$ | 9.9734E-02 | 1.96 | 1.3657E-02 | 1.94 | 5.9084E-03 | 1.96 |
| $2^{-4}$ | 2.5160E-02 | 1.99 | 3.4507E-03 | 1.98 | 1.4873E-03 | 1.99 |

表 7 与表 8 给出了三维 Hood–Taylor 型连续位移稳定化单元 $P_{k+1}^{\mathrm{div}} - P_k^0$ 在 $k=1, 2$ 时的误差与收敛阶。数值结果确证了推论 4.4 式 (4.11) 所预测的最优收敛阶：$k=1$ 时为 $O(h^2)$，$k=2$ 时为 $O(h^3)$。

<center><b>
表 7：三维稳定化 $P_2^{\mathrm{div}} - P_1^0$ 单元数值误差（Table 7. Numerical errors for the stabilized $P_2^{\mathrm{div}} - P_1^0$ element in 3D）
</b></center>

| $h$ | $\Vert \sigma - \sigma_h \Vert_{H(\mathrm{div},\mathcal{A})}$ | 收敛阶 | $\Vert u - u_h \Vert_0$ | 收敛阶 |
|:---:|:---:|:---:|:---:|:---:|
| $2^{-1}$ | 1.4391E+00 | — | 2.3509E-01 | — |
| $2^{-2}$ | 3.8148E-01 | 1.92 | 5.4959E-02 | 2.10 |
| $2^{-3}$ | 9.6524E-02 | 1.98 | 1.1730E-02 | 2.23 |
| $2^{-4}$ | 2.4182E-02 | 2.00 | 2.6368E-03 | 2.15 |

<center><b>
表 8：三维稳定化 $P_3^{\mathrm{div}} - P_2^0$ 单元数值误差（Table 8. Numerical errors for the stabilized $P_3^{\mathrm{div}} - P_2^0$ element in 3D）
</b></center>

| $h$ | $\Vert \sigma - \sigma_h \Vert_{H(\mathrm{div},\mathcal{A})}$ | 收敛阶 | $\Vert u - u_h \Vert_0$ | 收敛阶 |
|:---:|:---:|:---:|:---:|:---:|
| $2^{-1}$ | 2.7531E-01 | — | 3.9149E-02 | — |
| $2^{-2}$ | 3.7035E-02 | 2.89 | 5.7416E-03 | 2.77 |
| $2^{-3}$ | 4.7120E-03 | 2.97 | 7.8312E-04 | 2.87 |


---

# 致谢与基金资助

- **致谢**：第一作者 L. Chen 于 2015 年秋季访问北京大学期间完成了这项工作，感谢北京大学的接待与支持，以及其富有活力的科研氛围。
- **基金资助**：
  - 第一作者受美国国家科学基金会 NSF（项目号 DMS-1418934）资助；
  - 第二作者受国家自然科学基金 NSFC（项目号 11625101, 11271035, 91430213, 11421101）资助；
  - 第三作者受国家自然科学基金 NSFC（项目号 11301396, 11671304）及浙江省自然科学基金（项目号 LY17A010010, LY15A010015, LY15A010016, LY14A010020）资助。

---

# 参考文献（References）

[1] S. Adams and B. Cockburn, A mixed finite element method for elasticity in three dimensions, *J. Sci. Comput.* 25 (2005), 515–521.  
[2] M. Amara and J. M. Thomas, Equilibrium finite elements for the linear elastic problem, *Numer. Math.* 33 (1979), 367–383.  
[3] D. N. Arnold and G. Awanou, Rectangular mixed finite elements for elasticity, *Math. Models Methods Appl. Sci.* 15 (2005), 1417–1429.  
[4] D. N. Arnold, G. Awanou and R. Winther, Finite elements for symmetric tensors in three dimensions, *Math. Comp.* 77 (2008), 1229–1251.  
[5] D. N. Arnold, G. Awanou and R. Winther, Nonconforming tetrahedral mixed finite elements for elasticity, *Math. Models Methods Appl. Sci.* 24 (2014), 783–796.  
[6] D. N. Arnold, F. Brezzi and J. Douglas, Jr., PEERS: A new mixed finite element for plane elasticity, *Japan J. Appl. Math.* 1 (1984), 347–367.  
[7] D. N. Arnold, J. Douglas, Jr. and C. P. Gupta, A family of higher order mixed finite element methods for plane elasticity, *Numer. Math.* 45 (1984), 1–22.  
[8] D. N. Arnold, R. S. Falk and R. Winther, Mixed finite element methods for linear elasticity with weakly imposed symmetry, *Math. Comp.* 76 (2007), 1699–1723.  
[9] D. N. Arnold and J. J. Lee, Mixed methods for elastodynamics with weak symmetry, *SIAM J. Numer. Anal.* 52 (2014), 2743–2769.  
[10] D. N. Arnold and R. Winther, Mixed finite elements for elasticity, *Numer. Math.* 92 (2002), 401–419.  
[11] D. N. Arnold and R. Winther, Nonconforming mixed elements for elasticity, *Math. Models Methods Appl. Sci.* 13 (2003), 295–307.  
[12] G. Awanou, Two remarks on rectangular mixed finite elements for elasticity, *J. Sci. Comput.* 50 (2012), 91–102.  
[13] D. Boffi, Stability of higher order triangular Hood–Taylor methods for the stationary Stokes equations, *Math. Models Methods Appl. Sci.* 4 (1994), 223–235.  
[14] D. Boffi, Three-dimensional finite element methods for the Stokes problem, *SIAM J. Numer. Anal.* 34 (1997), 664–670.  
[15] D. Boffi, F. Brezzi and M. Fortin, Reduced symmetry elements in linear elasticity, *Commun. Pure Appl. Anal.* 8 (2009), 95–121.  
[16] D. Boffi, F. Brezzi and M. Fortin, *Mixed Finite Element Methods and Applications*, Springer Ser. Comput. Math. 44, Springer, Berlin, 2013.  
[17] S. C. Brenner and L. R. Scott, *The Mathematical Theory of Finite Element Methods*, 3rd ed., Texts Appl. Math. 15, Springer, New York, 2008.  
[18] F. Brezzi, On the existence, uniqueness and approximation of saddle-point problems arising from Lagrangian multipliers, *Rev. Franc. Automat. Inform. Rech. Operat. Sér. Rouge* 8 (1974), 129–151.  
[19] F. Brezzi, M. Fortin and L. D. Marini, Mixed finite element methods with continuous stresses, *Math. Models Methods Appl. Sci.* 3 (1993), 275–287.  
[20] R. Bustinza, A note on the local discontinuous Galerkin method for linear problems in elasticity, *Sci. Ser. A Math. Sci. (N.S.)* 13 (2006), 72–83.  
[21] Z. Cai and X. Ye, A mixed nonconforming finite element for linear elasticity, *Numer. Methods Partial Differential Equations* 21 (2005), 1043–1051.  
[22] G. Chen and X. Xie, A robust weak Galerkin finite element method for linear elasticity with strong symmetric stresses, *Comput. Methods Appl. Math.* 16 (2016), 389–408.  
[23] S.-C. Chen and Y.-N. Wang, Conforming rectangular mixed finite elements for elasticity, *J. Sci. Comput.* 47 (2011), 93–108.  
[24] Y. Chen, J. Huang, X. Huang and Y. Xu, On the local discontinuous Galerkin method for linear elasticity, *Math. Probl. Eng.* 2010 (2010), Article ID 759547.  
[25] P. G. Ciarlet, *The Finite Element Method for Elliptic Problems*, Stud. Math. Appl. 4, North-Holland, Amsterdam, 1978.  
[26] B. Cockburn, J. Gopalakrishnan and J. Guzmán, A new elasticity element made for enforcing weak stress symmetry, *Math. Comp.* 79 (2010), 1331–1349.  
[27] B. Cockburn, D. Schötzau and J. Wang, Discontinuous Galerkin methods for incompressible elastic materials, *Comput. Methods Appl. Mech. Engrg.* 195 (2006), 3184–3204.  
[28] B. Cockburn and K. Shi, Superconvergent HDG methods for linear elasticity with weakly symmetric stresses, *IMA J. Numer. Anal.* 33 (2013), 747–770.  
[29] D. A. Di Pietro and A. Ern, A hybrid high-order locking-free method for linear elasticity on general meshes, *Comput. Methods Appl. Mech. Engrg.* 283 (2015), 1–21.  
[30] B. Fraeijs de Veubeke, Displacement and equilibrium models in the finite element method, in: *Stress Analysis*, John Wiley & Sons, New York (1965), 145–197.  
[31] S. Gong, S. Wu and J. Xu, Mixed finite elements of any order in any dimension for linear elasticity with strongly symmetric stress tensor, preprint (2015), arXiv:1507.01752.  
[32] J. Gopalakrishnan and J. Guzmán, Symmetric nonconforming mixed finite elements for linear elasticity, *SIAM J. Numer. Anal.* 49 (2011), 1504–1520.  
[33] J. Gopalakrishnan and J. Guzmán, A second elasticity element using the matrix bubble, *IMA J. Numer. Anal.* 32 (2012), 352–372.  
[34] J. Guzmán, A unified analysis of several mixed methods for elasticity with weak stress symmetry, *J. Sci. Comput.* 44 (2010), 156–169.  
[35] C. Harder, A. L. Madureira and F. Valentin, A hybrid-mixed method for elasticity, *ESAIM Math. Model. Numer. Anal.* 50 (2016), 311–336.  
[36] J. Hu, A new family of efficient conforming mixed finite elements on both rectangular and cuboid meshes for linear elasticity in the symmetric formulation, *SIAM J. Numer. Anal.* 53 (2015), 1438–1463.  
[37] J. Hu, Finite element approximations of symmetric tensors on simplicial grids in $\mathbb{R}^n$: The higher order case, *J. Comput. Math.* 33 (2015), 283–296.  
[38] J. Hu, H. Man and S. Zhang, A simple conforming mixed finite element for linear elasticity on rectangular grids in any space dimension, *J. Sci. Comput.* 58 (2014), 367–379.  
[39] J. Hu and Z.-C. Shi, Lower order rectangular nonconforming mixed finite elements for plane elasticity, *SIAM J. Numer. Anal.* 46 (2007), 88–102.  
[40] J. Hu and S. Zhang, A family of conforming mixed finite elements for linear elasticity on triangular grids, preprint (2015), arXiv:1406.7457.  
[41] J. Hu and S. Zhang, A family of symmetric mixed finite elements for linear elasticity on tetrahedral grids, *Sci. China Math.* 58 (2015), 297–307.  
[42] J. Hu and S. Zhang, Finite element approximations of symmetric tensors on simplicial grids in $\mathbb{R}^n$: The lower order case, *Math. Models Methods Appl. Sci.* 26 (2016), 1649–1669.  
[43] J. Huang and X. Huang, The hp-version error analysis of a mixed DG method for linear elasticity, preprint (2016), arXiv:1608.04060.  
[44] X. Huang, A reduced local discontinuous Galerkin method for nearly incompressible linear elasticity, *Math. Probl. Eng.* 2013 (2013), Article ID 546408.  
[45] X. Huang and J. Huang, The compact discontinuous Galerkin method for nearly incompressible linear elasticity, *J. Sci. Comput.* 56 (2013), 291–318.  
[46] C. Johnson and B. Mercier, Some equilibrium finite element methods for two-dimensional elasticity problems, *Numer. Math.* 30 (1978), 103–116.  
[47] H.-Y. Man, J. Hu and Z.-C. Shi, Lower order rectangular nonconforming mixed finite element for the three-dimensional elasticity problem, *Math. Models Methods Appl. Sci.* 19 (2009), 51–65.  
[48] M. E. Morley, A family of mixed finite elements for linear elasticity, *Numer. Math.* 55 (1989), 633–666.  
[49] W. Qiu and L. Demkowicz, Mixed hp-finite element method for linear elasticity with weakly imposed symmetry, *Comput. Methods Appl. Mech. Engrg.* 198 (2009), 3682–3701.  
[50] W. Qiu and L. Demkowicz, Mixed hp-finite element method for linear elasticity with weakly imposed symmetry: Stability analysis, *SIAM J. Numer. Anal.* 49 (2011), 619–641.  
[51] W. Qiu, J. Shen and K. Shi, An HDG method for linear elasticity with strong symmetric stresses, preprint (2013), arXiv:1312.1407.  
[52] L. R. Scott and S. Zhang, Finite element interpolation of nonsmooth functions satisfying boundary conditions, *Math. Comp.* 54 (1990), 483–493.  
[53] R. Stenberg, A family of mixed finite elements for the elasticity problem, *Numer. Math.* 53 (1988), 513–538.  
[54] C. Taylor and P. Hood, A numerical solution of the Navier–Stokes equations using the finite element technique, *Comput. & Fluids* 1 (1973), 73–100.  
[55] C. Wang, J. Wang, R. Wang and R. Zhang, A locking-free weak Galerkin finite element method for elasticity problems in the primal formulation, *J. Comput. Appl. Math.* 307 (2016), 346–366.  
[56] V. B. Watwood, Jr. and B. J. Hartz, An equilibrium stress field model for finite element solutions of two-dimensional elastostatic problems, *Int. J. Solids Struct.* 4 (1968), 857–873.  
[57] X. Xie and J. Xu, New mixed finite elements for plane elasticity and Stokes equations, *Sci. China Math.* 54 (2011), 1499–1519.  
[58] S.-Y. Yi, Nonconforming mixed finite element methods for linear elasticity using rectangular elements in two and three dimensions, *Calcolo* 42 (2005), 115–133.  
[59] S.-Y. Yi, A new nonconforming mixed finite element method for linear elasticity, *Math. Models Methods Appl. Sci.* 16 (2006), 979–999.
