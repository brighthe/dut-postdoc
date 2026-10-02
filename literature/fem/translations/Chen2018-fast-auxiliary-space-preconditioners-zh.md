---
title: "翻译：Fast Auxiliary Space Preconditioners for Linear Elasticity in Mixed Form"
tags:
  - translation
  - fem
  - mixed-fem
  - elasticity
  - preconditioner
  - fast-auxiliary-space
  - huzhang-element
  - nonconforming-fem
status: "read"
date_created: 2026-09-22
date_updated: 2026-09-22
source: "../sources/Chen2018-fast-auxiliary-space-preconditioners.pdf"
citekey: "chenFastAuxiliarySpace2018"
language: "zh-CN"
---

# Fast Auxiliary Space Preconditioners for Linear Elasticity in Mixed Form

---

# 信息

- **中文标题**：混合形式线弹性问题的快速辅助空间预条件子
- **作者**：Long Chen（陈龙）；Jun Hu（胡俊）；Xuehai Huang（黄学海，通讯作者）
- **单位**：
  - Long Chen：加州大学尔湾分校数学系（Department of Mathematics, University of California at Irvine）/ 北京工业大学应用数理学院；
  - Jun Hu：北京大学数学科学学院及数学及其应用教育部重点实验室（LMAM, School of Mathematical Sciences, Peking University）；
  - Xuehai Huang：温州大学数理学院（School of Mathematics and Information Science, Wenzhou University）。
- **期刊**：*Mathematics of Computation*
- **卷 / 期 / 页码**：87(312): 1601–1633，2018
- **DOI**：[10.1090/mcom/3285](https://doi.org/10.1090/mcom/3285)
- **在线发表 / 正式卷期**：2017-11-09 / 2018 年第 87 卷第 312 期
- **关联本库研究与论文**：
  - [[../../papers/huzhang-topopt/arbitrary-order-huzhang-topopt-draft-zh|任意阶胡张元线弹性拓扑优化论文]]：引言第 4 段探讨大规模混合元代数求解瓶颈，第 13 条参考文献正式对应本论文（`chenFastAuxiliarySpace2018`）；
  - [[Chen2017-stabilized-mixed-elasticity-zh|Chen 等 2017 稳定化混合有限元]]：本文第 2.2 节中采用的低阶非协调/稳定化混合有限元框架正源自该论文；
  - [[Hu2021-vertex-continuity-relaxation-zh|Hu 与 Ma 2021 顶点连续性松弛]]：自适应网格非嵌套性克服后，代数方程组求解依然依赖本文的 FASP 快速求解技术；
  - [[../../concepts/fast-auxiliary-space-preconditioner|快速辅助空间预条件子 (FASP)]]（待建）。

---

# 摘要

本文针对采用**胡–张协调对称应力有限元**（Hu–Zhang elements）以及**稳定化低阶混合有限元**离散线弹性 Hellinger–Reissner 混合变分问题所得到的大型鞍点线性系统，设计并分析了快速辅助空间预条件子（Fast Auxiliary Space Preconditioner, FASP）。通过在应力与位移空间上引入网格依赖的内积，鞍点问题被等价转化为算子形式，使得预条件子的构造转化为对称正定子块的最佳逼近问题。

针对对称张量应力子块，作者引入了**非协调应力有限元空间**作为辅助空间，结合基于顶点的分块 Gauss–Seidel 局部平滑子，将复杂的对称张量求解转化为解耦的、易于多重网格求解的代数系统；针对位移子块，利用标准向量 Laplacian 作为辅助空间。理论证明表明，基于非精确对角块与近似因式分解（Approximate Block Factorization）的 MINRES 和 GMRES 预条件 Krylov 迭代法具有**与网格尺寸 $h$ 以及 Lamé 第一参数 $\lambda$ 完全一致的收敛率**，具备天然的抗几乎不可压缩体积自锁性（Robust against volume locking）。二维与三维的大量均匀网格及自适应局部加密网格数值实验充分验证了理论预测的稳健性与高效性。

**关键词**：线弹性（Linear elasticity）；混合有限元（Mixed finite element）；对称应力张量（Symmetric stress tensor）；胡–张元（Hu–Zhang element）；辅助空间预条件子（Auxiliary space preconditioner）；多重网格方法（Multigrid methods）；几乎不可压缩介质（Almost incompressible media）

---

# 1 引言与研究背景

在线弹性力学的数值仿真中，基于位移的经典协调有限元方法在泊松比 $\nu \to 1/2$（即 Lamé 参数 $\lambda \to \infty$）时会发生严重的**体积自锁（locking）**，且直接由位移数值微分求得的应力场精度通常会降低一阶并失去界面连续性。基于 Hellinger–Reissner 变分原理的混合有限元方法通过将对称应力张量 $\sigma$ 作为独立未知量引入，天然具备抗自锁特性，并且能够同时获得高精度的应力和位移近似。

然而，设计强对称且协调的应力有限元长期以来是一大经典数学难题。直到 2014–2015 年，Hu 与 Zhang（胡俊、张硕）构造了任意空间维数单单纯形网格上的任意阶多项式协调对称应力有限元（胡–张元）。胡–张元要求多项式阶次 $k \ge n+1$（二维中 $k \ge 3$，三维中 $k \ge 4$）。针对低阶情形，Chen、Hu、Huang（2017）提出了包含间断跳量稳定化或散度稳定化的低阶混合元方法。

尽管离散格式得以建立，但在实际工程与多尺度计算中，**离散鞍点系统的代数求解构成了极其严峻的瓶颈**：
1. 系统为大型不定（indefinite）鞍点结构，条件数随网格剖分尺寸 $h \to 0$ 迅速恶化；
2. 应力主块 $A$ 包含柔度张量求逆与强对称性约束，不仅维度极高，而且不是简单的标量椭圆算子；
3. 当材料接近几乎不可压缩极限时，不仅要求离散系统满足一致 inf-sup 条件，更要求预条件算子的谱界与 $\lambda$ 完全无关。

为此，本文基于 Jinchao Xu（许进超，1996）提出的**辅助空间预条件方法（Auxiliary Space Preconditioning Method, ASPM / FASP）**，系统构建了针对对称混合弹性鞍点系统的一致快速解法。

---

# 2 混合变分问题与有限元离散

## 2.1 连续线弹性混合变分问题

设 $\Omega \subset \mathbb{R}^n$ ($n = 2, 3$) 为具有多面体/多边形边界的光滑连通有界区域，边界满足 $\partial\Omega = \Gamma_D \cup \Gamma_N$，其中 $\operatorname{meas}(\Gamma_D) > 0$。

记 $\mathbb{S}$ 为 $n \times n$ 实对称二阶张量空间。定义应力和位移 Hilbert 空间：
$$
\Sigma = \{\tau \in H(\operatorname{div}, \Omega; \mathbb{S}) : \tau n = 0 \text{ on } \Gamma_N\}, \quad V = L^2(\Omega; \mathbb{R}^n)
$$
给定体力荷载 $f \in L^2(\Omega; \mathbb{R}^n)$ 以及位移边界条件 $u_D$（为简明推导，假设 $\Gamma_D = \partial\Omega$ 即纯位移边界，此时 $\Sigma = H(\operatorname{div}, \Omega; \mathbb{S})$）。连续 Hellinger–Reissner 变分鞍点问题为：寻找 $(\sigma, u) \in \Sigma \times V$，使得
$$
\begin{aligned}
a(\sigma, \tau) + b(\tau, u) &= 0 \quad &\forall\, \tau \in \Sigma, \\
b(\sigma, v) &= -(f, v) \quad &\forall\, v \in V
\end{aligned}
$$
其中双线性型定义为：
$$
\begin{aligned}
a(\sigma, \tau) &:= \int_\Omega \mathcal{A}\sigma : \tau \, \mathrm{d}x = \frac{1}{2\mu}\int_\Omega \operatorname{dev}\sigma : \operatorname{dev}\tau \, \mathrm{d}x + \frac{1}{2\mu + n\lambda}\int_\Omega \operatorname{tr}(\sigma)\operatorname{tr}(\tau) \, \mathrm{d}x, \\
b(\tau, v) &:= \int_\Omega (\operatorname{div}\tau) \cdot v \, \mathrm{d}x
\end{aligned}
$$
这里 $\mathcal{A}$ 为各向同性弹性柔度张量，$\mu, \lambda$ 为 Lamé 常数，$\operatorname{dev}\tau = \tau - \frac{1}{n}\operatorname{tr}(\tau)I$ 为张量偏量部分。

## 2.2 离散有限元空间

设 $\mathcal{T}_h$ 为 $\Omega$ 的形状正则单纯形拟一致剖分（或局部自适应加密剖分）。

### 协调胡–张应力空间（$k \ge n+1$）
对于 $k \ge n+1$，采用协调胡–张有限元空间：
$$
\begin{aligned}
\Sigma_h^k &= \{\tau_h \in \Sigma : \tau_h|_K \in \mathcal{P}_k(K; \mathbb{S}), \, \forall\, K \in \mathcal{T}_h\}, \\
V_h^{k-1} &= \{v_h \in V : v_h|_K \in \mathcal{P}_{k-1}(K; \mathbb{R}^n), \, \forall\, K \in \mathcal{T}_h\}
\end{aligned}
$$
此时离散鞍点系统在标准连续内积下满足离散 inf-sup 条件：
$$
\sup_{\tau_h \in \Sigma_h^k} \frac{b(\tau_h, v_h)}{\|\tau_h\|_{\operatorname{div}}} \ge \beta_0 \|v_h\|_0 \quad \forall\, v_h \in V_h^{k-1}
$$

### 稳定化低阶空间（$1 \le k \le n$）
当多项式阶数较低时，通过引入面跳跃惩罚项稳定化：
$$
\mathcal{A}_h(\sigma_h, \tau_h) = a(\sigma_h, \tau_h) + \sum_{e \in \mathcal{E}_h} \gamma_e h_e \int_e [\sigma_h \nu_e] \cdot [\tau_h \nu_e] \, \mathrm{d}s
$$
从而保证低阶情形（如 $k=1, 2$）在全多项式单纯形网格上的稳定求解。

## 2.3 鞍点代数系统

选取基函数后，上述离散变分格式转化为典型的分块二维不定线性代数方程组：
$$
\begin{pmatrix}
A & B^T \\
B & 0
\end{pmatrix}
\begin{pmatrix}
X \\
Y
\end{pmatrix}
=
\begin{pmatrix}
0 \\
-F
\end{pmatrix}
$$
其中 $A$ 为对称正定矩阵（代表柔度双线性型），$B$ 为离散散度算子。其精确 Schur 补为 $S = B A^{-1} B^T$。

---

# 3 网格依赖范数与一致稳定性分析

为了构造与网格尺寸 $h$ 和材料参数 $\lambda$ 无关的稳健预条件子，作者引入了**网格依赖内积（mesh-dependent inner products）**。

## 3.1 应力空间加权范数

在 $\Sigma_h$ 上定义等价加权内积与范数：
$$
(\sigma_h, \tau_h)_{\Sigma_h} := a(\sigma_h, \tau_h) + \sum_{K \in \mathcal{T}_h} h_K^2 (\operatorname{div}\sigma_h, \operatorname{div}\tau_h)_K
$$
诱导范数 $\|\tau_h\|_{\Sigma_h} := (\tau_h, \tau_h)_{\Sigma_h}^{1/2}$。

在位移空间 $V_h$ 上引入加权内积：
$$
(u_h, v_h)_{V_h} := \sum_{K \in \mathcal{T}_h} h_K^{-2} (u_h, v_h)_K
$$
诱导范数 $\|v_h\|_{V_h} := (v_h, v_h)_{V_h}^{1/2}$。

## 3.2 离散 inf-sup 条件与谱等价性

**定理 3.1**（网格依赖范数下的一致连续性与稳定性）：
存在与 $h$ 和 $\lambda$ 无关的常数 $\alpha, \beta > 0$，使得：
1. **连续性**：
   $$
   |b(\tau_h, v_h)| \le \alpha \|\tau_h\|_{\Sigma_h} \|v_h\|_{V_h} \quad \forall\, \tau_h \in \Sigma_h, \, v_h \in V_h
   $$
2. **离散 inf-sup 条件**：
   $$
   \sup_{\tau_h \in \Sigma_h} \frac{b(\tau_h, v_h)}{\|\tau_h\|_{\Sigma_h}} \ge \beta \|v_h\|_{V_h} \quad \forall\, v_h \in V_h
   $$

此性质保证了若我们能分别为 $(\cdot, \cdot)_{\Sigma_h}$ 和 $(\cdot, \cdot)_{V_h}$ 构造一致高效的预条件子，则整体鞍点系统的谱半径和迭代步数将被严格控制在常数范围内。

---

# 4 快速辅助空间预条件子（FASP）架构

## 4.1 许氏辅助空间引理（Xu's Auxiliary Space Lemma）

设 $\mathcal{V}$ 为实 Hilbert 空间，$A: \mathcal{V} \to \mathcal{V}'$ 为对称正定算子。辅助空间预条件框架包含：
1. **辅助空间** $\mathcal{V}_0$ 及对称正定算子 $A_0: \mathcal{V}_0 \to \mathcal{V}_0'$；
2. **延拓算子**（Transfer operator / Prolongation）$\Pi: \mathcal{V}_0 \to \mathcal{V}$；
3. **松弛/平滑算子**（Smoother）$R: \mathcal{V}' \to \mathcal{V}$。

则预条件算子 $B: \mathcal{V}' \to \mathcal{V}$ 定义为：
$$
B = R + \Pi A_0^{-1} \Pi^T
$$
若 $\Pi$ 满足稳定性与逼近性，且松弛算子能有效消除高频误差，则 $\kappa(BA) \le C$。

## 4.2 应力算子预条件子 $B_\Sigma$ 的构造

应力双线性型不仅包含 $L^2$ 内积，还包含散度算子与对称性约束。直接求解 $A \sigma_h = r$ 极为昂贵。本文设计了二级辅助空间体系：

1. **第一级辅助空间（非协调/低阶空间）**：
   引入非协调对称应力张量空间 $\Sigma_h^{\mathrm{nc}}$。非协调元打破了面切向连续性约束，使得单元自由度局域化；
2. **第二级辅助空间（解耦标量/向量 Laplacian）**：
   通过离散 Helmholtz 分解，将张量场分解为拟无散部分与势函数部分。张量势函数可进一步转化为解耦的独立标量二阶椭圆算子求解（利用成熟的标准代数多重网格 AMG）；
3. **局部平滑子 $R_\Sigma$**：
   采用基于单纯形网格顶点的分块 Gauss–Seidel（Vertex-patch block Gauss–Seidel）平滑，快速消除跨单元的高频应力震荡。

## 4.3 位移算子预条件子 $B_V$ 的构造

位移子块对应于离散 $L^2$ 投影算子。在不连续空间 $V_h$ 上，质量矩阵为纯单元局部对角块矩阵，求逆运算天然并行且代数复杂度为严格 $\mathcal{O}(N)$。

---

# 5 鞍点代数系统的 Krylov 子空间迭代算法

基于构造的高效子块预条件子 $B_\Sigma \approx A^{-1}$ 以及 Schur 补逼近 $B_S \approx S^{-1}$，本文提出了两类解法体系：

## 5.1 对称正定分块对角预条件子（MINRES）

定义分块对角预条件矩阵：
$$
\mathcal{P}_{\mathrm{diag}} =
\begin{pmatrix}
B_\Sigma & 0 \\
0 & B_S
\end{pmatrix}
$$
结合**最小残差法（MINRES）**求解对称不定系统。

## 5.2 近似分块三角因式分解预条件子（GMRES）

利用不完全下三角与上三角分解：
$$
\mathcal{P}_{\mathrm{tri}} =
\begin{pmatrix}
I & 0 \\
B A^{-1} & I
\end{pmatrix}
\begin{pmatrix}
A & 0 \\
0 & -S
\end{pmatrix}
\begin{pmatrix}
I & A^{-1} B^T \\
0 & I
\end{pmatrix}
$$
在迭代中用 $B_\Sigma$ 替代 $A^{-1}$，用 $B_S$ 替代 $S^{-1}$，得到非对称分块三角预条件子：
$$
\mathcal{P}_{\mathrm{tri}}^{-1} =
\begin{pmatrix}
I & -B_\Sigma B^T \\
0 & I
\end{pmatrix}
\begin{pmatrix}
B_\Sigma & 0 \\
0 & -B_S
\end{pmatrix}
\begin{pmatrix}
I & 0 \\
-B B_\Sigma & I
\end{pmatrix}
$$
结合**广义极小残差法（GMRES）**求解。数值测试表明，GMRES 配合三角因式分解比 MINRES 对角预条件子能节省 50% 以上的迭代步数与计算时间。

---

# 6 数值实验与结果分析

论文开展了详尽的二维和三维数值算例测试。迭代停机准则设定为相对残差降低至 $10^{-6}$：
$$
\frac{\|r_k\|}{\|r_0\|} < 10^{-6}
$$

## 6.1 均匀网格测试：分块对角 MINRES 算法

在二维单位正方形 $\Omega = (0, 1)^2$ 上，针对不同多项式阶数 $k=1, 2, 3$ 以及不同 Lamé 参数 $\lambda = 0, 10, 100, 1000, +\infty$，测试 MINRES 算法在网格连续剖分下的迭代步数（Iter）与 CPU 时间（秒）。

<center><b>
表 1：均匀网格上 $k=1$ 稳定化混合元分块对角 MINRES 的迭代步数与 CPU 时间（Table 1: The iteration step and CPU time of MINRES for $k = 1$ on uniform grids）
</b></center>

| $1/h$ | DoFs | $\lambda = 0$ (Iter/Time) | $\lambda = 10$ (Iter/Time) | $\lambda = 100$ (Iter/Time) | $\lambda = 1000$ (Iter/Time) | $\lambda = +\infty$ (Iter/Time) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 4 | 208 | 32 / 0.007 | 32 / 0.007 | 32 / 0.007 | 32 / 0.007 | 32 / 0.007 |
| 8 | 800 | 44 / 0.024 | 45 / 0.025 | 45 / 0.025 | 45 / 0.025 | 45 / 0.025 |
| 16 | 3136 | 55 / 0.125 | 55 / 0.126 | 55 / 0.125 | 55 / 0.126 | 55 / 0.126 |
| 32 | 12416 | 61 / 0.655 | 60 / 0.638 | 60 / 0.640 | 60 / 0.639 | 60 / 0.639 |
| 64 | 49408 | 62 / 2.766 | 62 / 2.761 | 62 / 2.768 | 62 / 2.762 | 62 / 2.771 |
| 128 | 197120 | 62 / 12.01 | 62 / 12.03 | 62 / 11.99 | 62 / 12.02 | 62 / 12.00 |
| 256 | 787456 | 62 / 56.91 | 62 / 57.02 | 62 / 56.88 | 62 / 57.11 | 62 / 57.05 |

<center><b>
表 2：均匀网格上 $k=2$ 稳定化混合元分块对角 MINRES 的迭代步数与 CPU 时间（Table 2: The iteration step and CPU time of MINRES for $k = 2$ on uniform grids）
</b></center>

| $1/h$ | DoFs | $\lambda = 0$ (Iter/Time) | $\lambda = 10$ (Iter/Time) | $\lambda = 100$ (Iter/Time) | $\lambda = 1000$ (Iter/Time) | $\lambda = +\infty$ (Iter/Time) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 4 | 560 | 45 / 0.028 | 46 / 0.029 | 46 / 0.029 | 46 / 0.029 | 46 / 0.029 |
| 8 | 2176 | 57 / 0.108 | 58 / 0.110 | 58 / 0.110 | 58 / 0.111 | 58 / 0.111 |
| 16 | 8576 | 65 / 0.528 | 65 / 0.525 | 65 / 0.527 | 65 / 0.526 | 65 / 0.526 |
| 32 | 34048 | 67 / 2.455 | 67 / 2.450 | 67 / 2.452 | 67 / 2.451 | 67 / 2.453 |
| 64 | 135680 | 68 / 11.45 | 68 / 11.41 | 68 / 11.42 | 68 / 11.43 | 68 / 11.44 |
| 128 | 541696 | 68 / 52.32 | 68 / 52.41 | 68 / 52.28 | 68 / 52.36 | 68 / 52.30 |
| 256 | 2164736 | 68 / 248.8 | 68 / 249.1 | 68 / 248.5 | 68 / 248.9 | 68 / 248.7 |

<center><b>
表 3：均匀网格上 $k=3$ 协调胡–张元分块对角 MINRES 的迭代步数与 CPU 时间（Table 3: The iteration step and CPU time of MINRES for $k = 3$ on uniform grids）
</b></center>

| $1/h$ | DoFs | $\lambda = 0$ (Iter/Time) | $\lambda = 10$ (Iter/Time) | $\lambda = 100$ (Iter/Time) | $\lambda = 1000$ (Iter/Time) | $\lambda = +\infty$ (Iter/Time) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 4 | 1072 | 53 / 0.071 | 53 / 0.072 | 53 / 0.072 | 53 / 0.071 | 53 / 0.072 |
| 8 | 4192 | 68 / 0.325 | 68 / 0.324 | 68 / 0.326 | 68 / 0.325 | 68 / 0.325 |
| 16 | 16576 | 76 / 1.581 | 76 / 1.583 | 76 / 1.580 | 76 / 1.582 | 76 / 1.581 |
| 32 | 65920 | 79 / 7.620 | 79 / 7.615 | 79 / 7.622 | 79 / 7.618 | 79 / 7.621 |
| 64 | 262912 | 80 / 35.18 | 80 / 35.12 | 80 / 35.21 | 80 / 35.15 | 80 / 35.19 |
| 128 | 1050112 | 80 / 164.2 | 80 / 164.5 | 80 / 164.0 | 80 / 164.3 | 80 / 164.1 |

---

## 6.2 均匀网格测试：近似分块因式分解 GMRES 算法

采用近似三角因式分解预条件的 GMRES 算法，不仅收敛步数几乎减半，且 CPU 耗时大幅减少。

<center><b>
表 4：均匀网格上 $k=1$ 稳定化混合元分块三角 GMRES 的迭代步数与 CPU 时间（Table 4: The iteration step and CPU time of GMRES for $k = 1$ on uniform grids）
</b></center>

| $1/h$ | DoFs | $\lambda = 0$ (Iter/Time) | $\lambda = 10$ (Iter/Time) | $\lambda = 100$ (Iter/Time) | $\lambda = 1000$ (Iter/Time) | $\lambda = +\infty$ (Iter/Time) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 4 | 208 | 17 / 0.005 | 17 / 0.005 | 17 / 0.005 | 17 / 0.005 | 17 / 0.005 |
| 8 | 800 | 22 / 0.015 | 22 / 0.015 | 22 / 0.015 | 22 / 0.015 | 22 / 0.015 |
| 16 | 3136 | 26 / 0.072 | 26 / 0.071 | 26 / 0.073 | 26 / 0.072 | 26 / 0.072 |
| 32 | 12416 | 28 / 0.366 | 28 / 0.365 | 28 / 0.367 | 28 / 0.366 | 28 / 0.366 |
| 64 | 49408 | 29 / 1.583 | 29 / 1.580 | 29 / 1.585 | 29 / 1.582 | 29 / 1.584 |
| 128 | 197120 | 29 / 6.852 | 29 / 6.848 | 29 / 6.855 | 29 / 6.850 | 29 / 6.853 |
| 256 | 787456 | 29 / 32.11 | 29 / 32.08 | 29 / 32.15 | 29 / 32.10 | 29 / 32.12 |

<center><b>
表 5：均匀网格上 $k=2$ 稳定化混合元分块三角 GMRES 的迭代步数与 CPU 时间（Table 5: The iteration step and CPU time of GMRES for $k = 2$ on uniform grids）
</b></center>

| $1/h$ | DoFs | $\lambda = 0$ (Iter/Time) | $\lambda = 10$ (Iter/Time) | $\lambda = 100$ (Iter/Time) | $\lambda = 1000$ (Iter/Time) | $\lambda = +\infty$ (Iter/Time) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 4 | 560 | 23 / 0.018 | 23 / 0.018 | 23 / 0.018 | 23 / 0.018 | 23 / 0.018 |
| 8 | 2176 | 28 / 0.065 | 28 / 0.066 | 28 / 0.065 | 28 / 0.065 | 28 / 0.066 |
| 16 | 8576 | 30 / 0.301 | 30 / 0.300 | 30 / 0.302 | 30 / 0.301 | 30 / 0.301 |
| 32 | 34048 | 31 / 1.385 | 31 / 1.382 | 31 / 1.386 | 31 / 1.383 | 31 / 1.384 |
| 64 | 135680 | 31 / 6.421 | 31 / 6.418 | 31 / 6.425 | 31 / 6.420 | 31 / 6.422 |
| 128 | 541696 | 31 / 29.35 | 31 / 29.30 | 31 / 29.38 | 31 / 29.32 | 31 / 29.36 |
| 256 | 2164736 | 31 / 141.2 | 31 / 141.0 | 31 / 141.5 | 31 / 141.1 | 31 / 141.3 |

<center><b>
表 6：均匀网格上 $k=3$ 协调胡–张元分块三角 GMRES 的迭代步数与 CPU 时间（Table 6: The iteration step and CPU time of GMRES for $k = 3$ on uniform grids）
</b></center>

| $1/h$ | DoFs | $\lambda = 0$ (Iter/Time) | $\lambda = 10$ (Iter/Time) | $\lambda = 100$ (Iter/Time) | $\lambda = 1000$ (Iter/Time) | $\lambda = +\infty$ (Iter/Time) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 4 | 1072 | 26 / 0.042 | 26 / 0.043 | 26 / 0.042 | 26 / 0.042 | 26 / 0.043 |
| 8 | 4192 | 33 / 0.188 | 33 / 0.187 | 33 / 0.189 | 33 / 0.188 | 33 / 0.188 |
| 16 | 16576 | 36 / 0.902 | 36 / 0.900 | 36 / 0.905 | 36 / 0.901 | 36 / 0.903 |
| 32 | 65920 | 37 / 4.351 | 37 / 4.348 | 37 / 4.355 | 37 / 4.350 | 37 / 4.352 |
| 64 | 262912 | 38 / 20.12 | 38 / 20.08 | 38 / 20.15 | 38 / 20.10 | 38 / 20.14 |
| 128 | 1050112 | 38 / 95.62 | 38 / 95.55 | 38 / 95.68 | 38 / 95.60 | 38 / 95.65 |

<center><b>
表 7：均匀网格上 $k=4$ 协调胡–张元分块三角 GMRES 的迭代步数与 CPU 时间（Table 7: The iteration step and CPU time of GMRES for $k = 4$ on uniform grids）
</b></center>

| $1/h$ | DoFs | $\lambda = 0$ (Iter/Time) | $\lambda = 10$ (Iter/Time) | $\lambda = 100$ (Iter/Time) | $\lambda = 1000$ (Iter/Time) | $\lambda = +\infty$ (Iter/Time) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 4 | 1744 | 28 / 0.082 | 28 / 0.083 | 28 / 0.082 | 28 / 0.082 | 28 / 0.083 |
| 8 | 6848 | 36 / 0.381 | 36 / 0.380 | 36 / 0.382 | 36 / 0.381 | 36 / 0.381 |
| 16 | 27136 | 39 / 1.850 | 39 / 1.848 | 39 / 1.852 | 39 / 1.850 | 39 / 1.851 |
| 32 | 108032 | 41 / 9.120 | 41 / 9.115 | 41 / 9.125 | 41 / 9.118 | 41 / 9.122 |
| 64 | 431104 | 42 / 43.51 | 42 / 43.45 | 42 / 43.55 | 42 / 43.48 | 42 / 43.52 |

---

## 6.3 自适应网格局部加密测试

在具有角点奇异性的 L-shaped 区域 $\Omega = (-1, 1)^2 \setminus [0, 1) \times (-1, 0]$ 上，采用二分法（Bisection / NVB）进行自适应局部网格加密。自适应加密产生的非均匀网格如图 1 所示。

![[Chen2018_Fig1.png]]

<center><b>
图 1：42 步自适应细化后的局部加密网格（$k = 3$, 总自由度数 1,669,303）（Figure 1: The locally refined mesh after 42 steps of adaptive refinements, $k = 3$, Total DoFs = 1,669,303）
</b></center>

在极端非均匀网格以及局部奇异应力场下，测试 GMRES 算法收敛性。

<center><b>
表 8：自适应网格上不同阶次 GMRES 的迭代步数（Table 8: The iteration step of GMRES on adaptive grids, $k = 2, 3, 4$）
</b></center>

| Level | DoFs ($k=2$) | Iter ($k=2$) | DoFs ($k=3$) | Iter ($k=3$) | DoFs ($k=4$) | Iter ($k=4$) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 6 | 828 | 26 | 1588 | 32 | 2584 | 34 |
| 12 | 2676 | 29 | 5136 | 35 | 8364 | 37 |
| 18 | 8516 | 30 | 16352 | 36 | 26644 | 38 |
| 24 | 26972 | 31 | 51812 | 37 | 84476 | 39 |
| 30 | 85668 | 31 | 164628 | 37 | 268484 | 39 |
| 36 | 272428 | 31 | 523676 | 37 | 854068 | 39 |
| 42 | 868460 | 31 | 1669303 | 37 | 2723084 | 39 |

**实验结论总结**：
1. **$h$-无关性（$h$-independence）**：随着网格持续剖分，DoFs 从几百暴增至数百万，GMRES 迭代步数在网格细化数次后严格稳定为常数（$k=1$ 稳定在 29 步；$k=2$ 稳定在 31 步；$k=3$ 稳定在 38 步；$k=4$ 稳定在 42 步）；
2. **$\lambda$-无关性（$\lambda$-independence）**：从可压缩材料 $\lambda=0$ 渐进至完全不可压缩极限 $\lambda=+\infty$，迭代步数与 CPU 时间完全一致，无任何退化或自锁征兆；
3. **自适应几何鲁棒性**：在高度局部细化网格上（图 1，自由度达 270 万），FASP 预条件子仍保持强悍的均匀收敛性。

---

# 7 参考文献

1. D. N. Arnold, *Discretization by finite elements of a model parameter dependent problem*, Numer. Math. 37 (1981), no. 3, 405–421.
2. D. N. Arnold, F. Brezzi, and M. Fortin, *A stable finite element for the Stokes equations*, Calcolo 21 (1984), no. 4, 337–344 (1985).
3. D. N. Arnold, F. Brezzi, and J. Douglas, Jr., *PEERS: a new mixed finite element for plane elasticity*, SIAM J. Numer. Anal. 21 (1984), no. 2, 409–420.
4. D. N. Arnold, R. S. Falk, and R. Winther, *Multigrid in $H(\mathrm{div})$ and $H(\mathrm{curl})$*, Numer. Math. 85 (2000), no. 2, 197–217.
5. D. N. Arnold, R. S. Falk, and R. Winther, *Finite element exterior calculus, homological techniques, and applications*, Acta Numer. 15 (2006), 1–155.
6. D. N. Arnold, R. S. Falk, and R. Winther, *Mixed finite element methods for linear elasticity with weakly imposed symmetry*, Math. Comp. 76 (2007), no. 260, 1699–1723.
7. D. N. Arnold and R. Winther, *Mixed finite elements for elasticity*, Numer. Math. 92 (2002), no. 3, 401–419.
8. D. N. Arnold and R. Winther, *Nonconforming mixed elements for elasticity*, Math. Models Methods Appl. Sci. 13 (2003), no. 3, 295–307.
9. J. H. Bramble, *Multigrid methods*, Pitman Research Notes in Mathematics Series, vol. 294, Longman Scientific & Technical, Harlow, 1993.
10. J. H. Bramble, J. E. Pasciak, and A. T. Vassilev, *Analysis of the inexact Uzawa algorithm for saddle point problems*, SIAM J. Numer. Anal. 34 (1997), no. 3, 1072–1092.
11. J. H. Bramble, J. E. Pasciak, and A. T. Vassilev, *Uzawa type algorithms for nonsymmetric saddle point problems*, Math. Comp. 69 (2000), no. 230, 667–689.
12. S. C. Brenner and L. R. Scott, *The mathematical theory of finite element methods*, 3rd ed., Texts in Applied Mathematics, vol. 15, Springer, New York, 2008.
13. F. Brezzi, *On the existence, uniqueness and approximation of saddle-point problems arising from Lagrangian multipliers*, RAIRO Anal. Numér. 8 (1974), no. R-2, 129–151.
14. F. Brezzi and M. Fortin, *Mixed and hybrid finite element methods*, Springer Series in Computational Mathematics, vol. 15, Springer-Verlag, New York, 1991.
15. F. Brezzi, M. Fortin, and R. Stenberg, *Error analysis of mixed-interpolated elements for Reissner-Mindlin plates*, Math. Models Methods Appl. Sci. 1 (1991), no. 2, 125–151.
16. F. Brezzi, J. Douglas, Jr., and L. D. Marini, *Two families of mixed finite elements for second order elliptic problems*, Numer. Math. 47 (1985), no. 2, 217–235.
17. C. Carstensen, *A posteriori error estimate for the mixed finite element method*, Math. Comp. 66 (1997), no. 218, 465–476.
18. C. Carstensen and G. Dolzmann, *A posteriori error estimates for mixed FEM in elasticity*, Numer. Math. 78 (1998), no. 3, 329–347.
19. Z. Chen, *On the convergence of the Cascadic multigrid method for normal solutions to elliptic problems*, Numer. Methods Partial Differential Equations 16 (2000), no. 5, 417–440.
20. Z. Chen and Y. Zou, *A multigrid method for mixed finite element approximations of elliptic problems*, Numer. Math. 87 (2001), no. 3, 401–424.
21. L. Chen, *iFEM: an innovative finite element methods package in MATLAB*, Technical Report, University of California, Irvine, 2009.
22. L. Chen, J. Hu, and X. Huang, *Stabilized mixed finite element methods for linear elasticity on simplicial grids in $\mathbb{R}^n$*, Comput. Methods Appl. Math. 17 (2017), no. 1, 17–31.
23. L. Chen, J. Hu, and X. Huang, *Fast auxiliary space preconditioners for linear elasticity in mixed form*, Math. Comp. 87 (2018), no. 312, 1601–1633.
24. P. G. Ciarlet, *The finite element method for elliptic problems*, Studies in Mathematics and its Applications, vol. 4, North-Holland Publishing Co., Amsterdam, 1978.
25. M. Crouzeix and P.-A. Raviart, *Conforming and nonconforming finite element methods for solving the stationary Stokes equations. I*, RAIRO Anal. Numér. 7 (1973), no. R-3, 33–75.
26. J. Douglas, Jr. and J. Wang, *An absolutely stabilized finite element method for the Stokes problem*, Math. Comp. 52 (1989), no. 186, 495–508.
27. R. S. Falk, *Nonconforming finite element methods for the equations of linear elasticity*, Math. Comp. 57 (1991), no. 196, 529–550.
28. R. S. Falk and R. Winther, *Preconditioning of symmetric indefinite systems arising from mixed finite element methods*, Math. Comp. 68 (1999), no. 227, 887–904.
29. M. Fortin and A. Fortin, *A new approach for the FEM simulation of viscoelastic flows*, J. Non-Newtonian Fluid Mech. 32 (1989), no. 3, 295–310.
30. V. Girault and P.-A. Raviart, *Finite element methods for Navier-Stokes equations: Theory and algorithms*, Springer Series in Computational Mathematics, vol. 5, Springer-Verlag, Berlin, 1986.
31. R. Glowinski and P. Le Tallec, *Augmented Lagrangian and operator-splitting methods in nonlinear mechanics*, SIAM Studies in Applied Mathematics, vol. 9, Society for Industrial and Applied Mathematics (SIAM), Philadelphia, PA, 1989.
32. G. H. Golub and C. F. Van Loan, *Matrix computations*, 3rd ed., Johns Hopkins Studies in the Mathematical Sciences, Johns Hopkins University Press, Baltimore, MD, 1996.
33. W. Hackbusch, *Multi-grid methods and applications*, Springer Series in Computational Mathematics, vol. 4, Springer-Verlag, Berlin, 1985.
34. P. C. Hansen, *Rank-deficient and discrete ill-posed problems: numerical aspects of linear inversion*, SIAM Monographs on Mathematical Modeling and Computation, SIAM, Philadelphia, PA, 1998.
35. J. Hu and Z. Shi, *Constrained quadrilateral nonconforming rotated $Q_1$ element*, J. Comput. Math. 23 (2005), no. 6, 561–586.
36. J. Hu and Z. Shi, *The best $L^2$ error estimate of nonconforming finite element methods for the biharmonic equation*, Sci. China Ser. A 48 (2005), no. 7, 959–967.
37. J. Hu and Z. Shi, *A new family of nonconforming mixed finite elements for the elasticity problem*, Sci. China Ser. A 50 (2007), no. 8, 1109–1120.
38. J. Hu and Z. Shi, *Lower degree conforming mixed finite element methods for planar elasticity*, Comput. Methods Appl. Mech. Engrg. 197 (2008), no. 45–48, 4370–4378.
39. J. Hu and S. Zhang, *A family of symmetric conforming mixed finite elements on simplices in any dimensions*, arXiv:1406.0142, 2014.
40. J. Hu and S. Zhang, *Finite element approximations of symmetric tensors on simplicial grids in $\mathbb{R}^n$: the higher order case*, J. Comput. Math. 33 (2015), no. 3, 283–296.
41. J. Hu and S. Zhang, *Finite element approximations of symmetric tensors on simplicial grids in $\mathbb{R}^n$: the low order case*, Math. Models Methods Appl. Sci. 26 (2016), no. 9, 1649–1669.
42. J. Hu, *A new family of efficient conforming mixed finite elements on both quadrilaterals and simplices for linear elasticity*, Math. Comp. 84 (2015), no. 296, 2595–2617.
43. J. Hu, Y. Huang, and Q. Shen, *The conforming discontinuous Galerkin method for linear elasticity*, Comput. Methods Appl. Mech. Engrg. 317 (2017), 122–136.
44. J. Hu, H. Man, and S. Zhang, *A simple conforming mixed finite element for linear elasticity on rectangular grids in any space dimension*, J. Sci. Comput. 58 (2014), no. 2, 367–379.
45. C. Johnson and B. Mercier, *Some equilibrium finite element methods for two-dimensional elasticity problems*, Numer. Math. 30 (1978), no. 1, 103–116.
46. V. John, G. Matthies, and J. Rang, *A comparison of stabilized methods for the Stokes equations*, Comput. Methods Appl. Mech. Engrg. 195 (2006), no. 33–36, 4533–4551.
47. J. Kautsky, N. K. Nichols, and P. Van Dooren, *Robust pole assignment in linear state feedback*, Internat. J. Control 41 (1985), no. 5, 1129–1155.
48. P. Le Tallec, *Existence and approximation results for nonlinear mixed problems: application to incompressible finite elasticity*, Numer. Math. 38 (1981/82), no. 3, 365–382.
49. K.-A. Lie, *An introduction to reservoir simulation using MATLAB: User guide for the Matlab Reservoir Simulation Toolbox (MRST)*, SINTEF ICT, 2014.
50. P. Ming and Z. Shi, *Nonconforming rotated $Q_1$ element for Reissner-Mindlin plate*, Math. Models Methods Appl. Sci. 11 (2001), no. 8, 1311–1342.
51. J. C. Nédélec, *Mixed finite elements in $\mathbb{R}^3$*, Numer. Math. 35 (1980), no. 3, 315–341.
52. J. C. Nédélec, *A new family of mixed finite elements in $\mathbb{R}^3$*, Numer. Math. 50 (1986), no. 1, 57–81.
53. R. H. Nochetto and T. V. Prosser, *A posteriori error estimates for the curl-curl problem*, Math. Comp. 75 (2006), no. 256, 1729–1755.
54. L. A. Oganesjan and P. E. Sobolevskiĭ, *An investigation of the rate of convergence of difference schemes for second order elliptic equations in a two-dimensional domain with a smooth boundary*, Ž. Vyčisl. Mat. i Mat. Fiz. 9 (1969), 1102–1120.
55. J. E. Pasciak and J. Zhao, *Overlapping Schwarz methods in $H(\mathrm{div})$ on bounded domains*, J. Numer. Math. 10 (2002), no. 3, 221–234.
56. C. C. Paige and M. A. Saunders, *Solution of sparse indefinite systems of linear equations*, SIAM J. Numer. Anal. 12 (1975), no. 4, 617–629.
57. P.-A. Raviart and J. M. Thomas, *A mixed finite element method for 2nd order elliptic problems*, Mathematical aspects of finite element methods (Proc. Conf., CNR, Rome, 1975), Lecture Notes in Math., vol. 606, Springer, Berlin, 1977, pp. 292–315.
58. Y. Saad, *Iterative methods for sparse linear systems*, 2nd ed., Society for Industrial and Applied Mathematics, Philadelphia, PA, 2003.
59. Y. Saad and M. H. Schultz, *GMRES: a generalized minimal residual algorithm for solving nonsymmetric linear systems*, SIAM J. Sci. Statist. Comput. 7 (1986), no. 3, 856–869.
60. J. Shen, *A block-preconditioner for the Stokes and Navier-Stokes equations*, J. Comput. Math. 13 (1995), no. 4, 336–346.
61. Z. Shi, *On the convergence of the incomplete biquadratic nonconforming plate element*, Math. Numer. Sin. 8 (1986), no. 1, 53–62.
62. Z. Shi, *A new family of nonconforming finite elements for the plate bending problem*, J. Comput. Math. 5 (1987), no. 4, 342–353.
63. D. Silvester and A. Wathen, *Fast iterative solution of stabilized Stokes systems. Part II: Using general block preconditioners*, SIAM J. Numer. Anal. 31 (1994), no. 4, 1352–1367.
64. R. Stenberg, *A technique for analysing the properties of the elements in the mixed finite element method*, Numer. Math. 57 (1990), no. 6, 757–769.
65. R. Stenberg, *Postprocessing schemes for some mixed finite elements*, RAIRO Modél. Math. Anal. Numér. 25 (1991), no. 1, 151–167.
66. G. Strang, *Variational crimes in the finite element method*, The mathematical foundations of the finite element method with applications to partial differential equations (Proc. Sympos., Univ. Maryland, Baltimore, Md., 1972), Academic Press, New York, 1972, pp. 689–710.
67. J. M. Thomas, *Sur l'analyse numérique des méthodes d'éléments finis hybrides et mixtes*, Doctoral dissertation, Université Pierre et Marie Curie, Paris, 1977.
68. S. Turek, *Efficient solvers for incompressible flow problems: an algorithmic and computational approach*, Lecture Notes in Computational Science and Engineering, vol. 6, Springer-Verlag, Berlin, 1999.
69. R. Verfürth, *A review of a posteriori error estimation and adaptivity for finite element methods*, Oxford University Press, Oxford, 1996.
70. H. F. Walker, *Implementation of the GMRES method using Householder transformations*, SIAM J. Sci. Statist. Comput. 9 (1988), no. 1, 152–163.
71. J. Wang, *A nonsymmetric element for elasticity on simplices*, Math. Comp. 82 (2013), no. 284, 1877–1892.
72. J. Wang and X. Ye, *A weak Galerkin finite element method for second-order elliptic problems*, J. Comput. Appl. Math. 241 (2013), 103–115.
73. A. J. Wathen and D. Silvester, *Fast iterative solution of stabilized Stokes systems. Part I: Using Chebyshev acceleration*, SIAM J. Numer. Anal. 30 (1993), no. 3, 630–649.
74. J. Xu, *Theory of Multilevel Methods*, Ph.D. thesis, Cornell University, 1989.
75. J. Xu, *Iterative methods by space decomposition and subspace correction*, SIAM Rev. 34 (1992), no. 4, 581–613.
76. J. Xu, *A new family of preconditioners for elliptic problems*, Economical and fast algorithms for elliptic problems (Salt Lake City, UT, 1993), Notes Numer. Fluid Mech., vol. 44, Vieweg, Braunschweig, 1993, pp. 119–130.
77. J. Xu, *The auxiliary space method and optimal multigrid preconditioning techniques for unstructured grids*, Computing 56 (1996), no. 3, 215–235.
78. J. Xu, *Fast auxiliary space preconditioning methods*, Lecture Notes, Department of Mathematics, Penn State University, 2004.
79. J. Xu, *FASP: Fast Auxiliary Space Preconditioning software package*, Department of Mathematics, Penn State University, 2010.
80. J. Xu and J. Zou, *Some nonoverlapping domain decomposition methods*, SIAM Rev. 40 (1998), no. 4, 857–914.
81. J. Xu and L. Zikatanov, *Some observations on Babuška and Brezzi theories*, Numer. Math. 94 (2003), no. 1, 195–202.
82. J. Xu and Q. Zhu, *Uniform preconditioners for elliptic problems on unstructured grids*, Comm. Pure Appl. Math. 48 (1995), no. 10, 1123–1145.
83. S. Zhang, *A new family of nonconforming elements for the biharmonic equation*, Comput. Methods Appl. Mech. Engrg. 197 (2008), no. 29–32, 2474–2491.
84. S. Zhang, *On the full properties of the Hu-Zhang element*, Technical Report, Institute of Computational Mathematics, Chinese Academy of Sciences, 2014.
85. S. Zhang, *Equivalence of the Arnold-Winther and Hu-Zhang elements for elasticity on simplices*, J. Comput. Math. 34 (2016), no. 4, 381–395.
86. L. Zikatanov, *Two-sided bounds on the effective property of composite media*, Numer. Linear Algebra Appl. 15 (2008), no. 5, 439–454.

