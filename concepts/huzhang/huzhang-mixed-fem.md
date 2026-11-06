---
title: "胡张应力—位移混合元、变分形式与低阶稳定化"
type: concept
aliases:
  - huzhang-mixed-fem
  - Hu-Zhang
  - 胡张元
  - 胡张混合元
  - 应力-位移混合有限元
  - stress-displacement mixed FEM
tags:
  - finite-element
  - mixed-finite-element
  - hdiv
  - saddle-point
  - linear-elasticity
  - stabilization
status: in-progress
date_added: 2026-08-07
date_update: 2026-10-16
---

# 胡张应力—位移混合元、变分形式与低阶稳定化

> 胡张元把应力提升为 $H(\mathrm{div})$ 顺应、对称张量值的主未知量，与分片不连续位移元组成对称不定鞍点系统，直接逼近应力——这让应力场自带物理可解释性；代价是低次空间不满足离散 inf-sup，需矩阵型跳量惩罚稳定化，且 traction/位移边界语义与位移型元相反。

本页整理应力—位移混合元的理论闭环：混合变分形式 → $H(\mathrm{div})$ 应力空间与不连续位移空间 → 鞍点系统 → 边界条件的对偶语义与牵引数据的可施加性 → 低次稳定化 → 收敛阶与阶次下限。
它**复用位移型 [[linear-elasticity]] 的几何、记号与 Hooke 本构**，只引入混合变量与相应离散。

本页**不覆盖**实现层内容：程序分层、配置键、自由度编号与装配映射算法、角点松弛可用的网格拓扑限制、FEALPy 4.0 API 迁移，均见 `soptx:docs/fem/huzhang-mixed-fem-implementation.md`；外载荷的程序架构见 `soptx:docs/fem/load-handling-implementation.md`。3D 无松弛空间构造的端到端验证尚未完成，本页不作断言。

---

## 1. 模型假设与几何

与 [[linear-elasticity]] §1 相同的记号：设 $\Omega\subset\mathbb R^d$（$d=2$ 或 $3$）为有界弹性体，$\Gamma_D$ 和 $\Gamma_N$ 是边界上互不相交的相对开集且 $\partial\Omega=\overline{\Gamma_D}\cup\overline{\Gamma_N}$。
$\Gamma_D$ 上施加位移边界条件，$\Gamma_N$ 上施加表面力边界条件。
小变形、静力、各向同性线弹性，Hooke 本构以**柔度张量** $A=\boldsymbol C^{-1}$（满足 $\boldsymbol\varepsilon=A\boldsymbol\sigma$）表达，与 [[linear-elasticity]] §2.2 的 $\boldsymbol C$ 互为逆。
设计密度在混合形式下作用于柔度张量 $A_\rho$ 而非刚度张量 $\boldsymbol C_\rho$，见 §2.6。

---

## 2. 应力—位移混合变分形式

### 2.1 混合变量

主未知量从位移元的一族提升为两族：

$$
\boldsymbol\sigma:\Omega\to\mathbb S^d,
\qquad
\boldsymbol u:\Omega\to\mathbb R^d,
\tag{1}
$$

其中 $\mathbb S^d$ 为 $d\times d$ 对称张量空间。
应力不再由位移的导数后处理得到，而是作为独立未知量直接求解。

### 2.2 混合弱形式

对强形式 $-\operatorname{div}\boldsymbol\sigma=\boldsymbol b$ 乘 $H(\mathrm{div})$ 检验函数 $\boldsymbol\tau$ 并分部积分，利用位移边界 $\boldsymbol u=\bar{\boldsymbol u}$ on $\Gamma_D$ 把边界项留在应力方程一侧；对位移检验函数 $\boldsymbol v\in[L_2]^d$ 原样内积散度方程。
得**混合弱形式**：找 $(\boldsymbol\sigma,\boldsymbol u)\in\Sigma\times V$，使对所有 $(\boldsymbol\tau,\boldsymbol v)\in\Sigma\times V$ 成立

$$
\int_\Omega (A\boldsymbol\sigma):\boldsymbol\tau\,\mathrm{d}x
-\int_\Omega \boldsymbol u\cdot(\mathrm{div}\,\boldsymbol\tau)\,\mathrm{d}x
=-\int_{\Gamma_D}\bar{\boldsymbol u}\cdot(\boldsymbol\tau\boldsymbol n)\,\mathrm{d}s,
\tag{2}
$$

$$
\int_\Omega (\mathrm{div}\,\boldsymbol\sigma)\cdot\boldsymbol v\,\mathrm{d}x
=-\int_\Omega \boldsymbol b\cdot\boldsymbol v\,\mathrm{d}x.
\tag{3}
$$

### 2.3 鞍点系统

(2)(3) 离散后成为**对称不定鞍点系统**：

$$
\begin{bmatrix} A & B \\ B^{\mathsf T} & 0 \end{bmatrix}
\begin{bmatrix} \boldsymbol\sigma_h \\ \boldsymbol u_h \end{bmatrix}
=\begin{bmatrix} \boldsymbol f_\sigma \\ \boldsymbol f_u \end{bmatrix},
\tag{4}
$$

其中 $A$ 为柔度矩阵块（(2) 中 $(A\boldsymbol\sigma):\boldsymbol\tau$），$B$ 为应力—位移耦合块（$\int_\Omega \mathrm{div}\,\boldsymbol\tau\cdot\boldsymbol u$）。
$(2,2)$ 块为零是鞍点结构的特征，也是 §4 稳定化的切入点。

### 2.4 边界条件的对偶语义

在应力—位移混合有限元中，由于独立主未知量变为对称应力 $\boldsymbol\sigma$，边界条件的施加方式与经典位移元呈现**严格的变分对偶性**。

| 物理边界类型 | 物理方程 | 标准位移法 (LFEM) | 胡张混合法 (HZMFEM) | 变分对偶本质 |
|---|---|---|---|---|
| **位移边界 $\Gamma_D$** | $\boldsymbol u = \bar{\boldsymbol u}$ | **本质边界（强施加）**<br>直接在位移自由度上置行置值 | **自然边界（弱施加）**<br>弱加进应力方程右端项 (2) | **几何约束对偶**（位移强 $\leftrightarrow$ 混合弱） |
| **牵引边界 $\Gamma_N$** | $\boldsymbol\sigma\boldsymbol n = \boldsymbol t$ | **自然边界（弱施加）**<br>通过边界虚功积分进入外力向量 | **本质边界（强施加）**<br>强加在应力法向迹自由度上 | **外力载荷对偶**（位移弱 $\leftrightarrow$ 混合强） |

### 2.5 牵引边界数据的可施加性

牵引条件在混合形式下是本质条件，必须写进应力法向迹自由度。这就把一个位移法里不存在的问题摆上台面：给定的牵引数据能否被 $\Sigma_h$ 的法向迹**精确表示**，以及写入自由度的操作是否**良定义**。三个环节彼此独立——标架定向、迹空间包含、多面共享点的一致性——任一环节失效都可能改写离散边界数据；误差是否随网格加密减小取决于具体处理，不能一概断言。

先给出各类外载荷的总体判据：

| 载荷 | 在胡张混合法中的处理 | 与位移法的关系 |
|---|---|---|
| 连续面牵引 $\boldsymbol t$ | 本质条件，在应力法向迹自由度上强插值 $(\boldsymbol\sigma_h\boldsymbol n)\vert_{\Gamma_N}=\boldsymbol t$ | 须先确认数据属于所用应力空间的法向迹空间（§2.5.2）；可表示且插值精确时，配合位移法的精确求积，两法使用同一牵引数据 |
| 集中力 $\boldsymbol P\delta_{\boldsymbol x_0}$ | 不可直接施加：位移检验空间 $\boldsymbol V=[L_2(\Omega)]^d$ 无逐点值，应力法向迹空间 $H^{-1/2}(\partial\Omega)$ 也容不下点测度 | 位移法在离散层可用点值泛函，混合法没有对应机制；受控对比先把点力按特征尺度 $l$ 分布化，再构造公用离散牵引；若采用连续 $P_1$ 投影，仍须核对结果属于 $T_h$ |
| 体力 $\boldsymbol b$ | $\int_\Omega\boldsymbol b\cdot\boldsymbol v_h\,\mathrm dx$ 进入位移方程右端，不涉及本质条件 | 两法完全一致 |

各类外载荷数据的正则性判据、$\delta$ 的负阶 Sobolev 指标、一致节点力系数与 $P_1$ 迹 $L^2$ 投影的守恒性证明由 [[external-loads]] 维护，本页只给在胡张形式下起作用的三条判据。

#### 2.5.1 边界自由度的边标架与外法向定向

边界面上的应力自由度不是笛卡尔分量，而是该面局部正交标架 $(\boldsymbol n_f,\boldsymbol t_f)$ 下的分量（§3.1：边子单纯形上的张量标架取该边的单位法向与单位切向）。标架由**面自身的几何定向**决定，与该面相对于 $\Omega$ 的内外无关：$\boldsymbol n_f$ 与外法向 $\boldsymbol n$ 可能同向也可能反向。记

$$
s=\boldsymbol n_f\cdot\boldsymbol n\in\{+1,-1\}.
$$

翻转面的定向会让 $\boldsymbol n_f$ 与 $\boldsymbol t_f$ **同时**反号，因此标架分量 $\boldsymbol\sigma:(\boldsymbol n_f\otimes\boldsymbol n_f)$、$\boldsymbol\sigma:(\boldsymbol n_f\otimes\boldsymbol t_f)$、$\boldsymbol\sigma:(\boldsymbol t_f\otimes\boldsymbol t_f)$ 本身都是定向无关的——每个标架向量出现偶数次。定向只在**数据转换**时进入：牵引数据以向量 $\bar{\boldsymbol t}=\boldsymbol\sigma\boldsymbol n$ 给出，而 $\boldsymbol n$ 是外法向、与面定向无关，于是 $\boldsymbol\sigma\boldsymbol n_f=s\,\bar{\boldsymbol t}$，写入自由度的两个标架分量各含 $\boldsymbol n_f$ 一次：

$$
\sigma_{nn}=s\,(\boldsymbol n_f\cdot\bar{\boldsymbol t}),\qquad
\sigma_{nt}=s\,(\boldsymbol t_f\cdot\bar{\boldsymbol t}).
$$

若数据改以应力张量 $\bar{\boldsymbol\sigma}$ 的分量给出，则两个标架向量各出现两次、$s$ 平方消去，转换自洽、无需定向信息。**判据**：数据到标架分量的转换中 $\boldsymbol n_f$ 出现奇数次时必须乘 $s$，偶数次时不得乘。

漏乘 $s$ 的后果分两种形态，须逐算例判读，不可一概而论：

- **$s$ 在整个 $\Gamma_N$ 上取常值**：等价于 $\bar{\boldsymbol t}\to-\bar{\boldsymbol t}$，离散解整体反号。柔顺度 $C=\boldsymbol f^{\mathsf T}\boldsymbol K^{-1}\boldsymbol f$ 及其对密度的导数都是位移的二次型，对全局反号免疫，优化轨迹与最终构型不变；
- **$s$ 在 $\Gamma_N$ 上分片取值不一**：这是真正的载荷分布损坏，合力与合力矩都不再是物理值，任何基于该载荷的结论都不成立。

#### 2.5.2 迹空间包含关系与强插值的恒等性

记 $\Gamma_N$ 上的离散法向迹空间

$$
T_h=\bigl\{(\boldsymbol\sigma_h\boldsymbol n)\vert_{\Gamma_N}:\boldsymbol\sigma_h\in\Sigma_h\bigr\}.
$$

逐面多项式次数只是可表示性的一个条件。$H(\mathrm{div})$ 协调性保证的是**同一内部公共面两侧、采用共同法向时的法向迹连续**，不保证不同边界面上的牵引向量连续；几何角点处法向变化，还须检查共享应力自由度的相容约束。因此，不能仅由 $k\ge1$ 推出任意边界上的 $[W_h^1]^d\subseteq T_h$。

对二维原空间的牵引–牵引角点，共同对称应力值要求 $n_2^Tg_1=n_1^Tg_2$。即使 $g_1=g_2$，这一条件也未必成立。例如直角两边取 $n_1=(1,0)^T,n_2=(0,1)^T$ 和相同牵引 $g_1=g_2=(1,0)^T$，等式两侧分别为 $0$ 和 $1$。连续分片一次数据因此不能无条件视为原迹空间的子集。局部条件的推导与空间扩展见 [[vertex-continuity-relaxation]]。

准确的使用条件是：先确认给定 $\boldsymbol t_h\in T_h$，并采用在该迹空间上具有再现性的插值或自由度赋值，再得到 $(\boldsymbol\sigma_h\boldsymbol n)|_{\Gamma_N}=\boldsymbol t_h$。位移法对同一数据使用足够精确的边界求积，两法使用同一牵引函数；两种形式的检验空间不同，不把它们笼统称为同一个离散载荷泛函，更不意味着离散解相同。

若原始牵引在一个边界面内部跳跃，它不能被该面上的单个多项式迹精确表示。可先按 [[external-loads]] §3.2 构造连续 $P_1$ 投影，但随后仍须核对投影结果是否属于 $T_h$；若不属于，需调整离散空间或明确引入进一步的数据近似。连续投影本身不解除几何角点的应力相容约束。

#### 2.5.3 共享顶点与角点上的良定义性

共享自由度必须给出一致的赋值；需要区分三种二维情形：

1. **同一直边上的共享点，数据连续**：采用一致的标架与定向后，两侧给出相同值，写入顺序不影响结果。
2. **同一直边上的共享点，数据跳跃**：原空间的共同顶点应力不能同时实现两个不同的牵引端点值。“后写者胜”会引入顺序依赖；简单平均也不普遍保证合力与力矩守恒。若采用数据近似，应明示投影或其他规则并检验实际边界积分，不能把平均当作精确施加原数据。
3. **不平行两边形成的牵引–牵引角点**：是否有共同对称应力值取决于 $n_2^Tg_1=n_1^Tg_2$，而不是仅取决于两边的标架不同。不相容时，§3.4 的自由度分裂可解除该障碍；也可以近似处理牵引，但须承认数据误差。相容数据不因几何角点本身而无解。

位移–牵引角点只有一侧给定牵引，位移侧反力由解确定，因此没有上述两侧给定牵引的相容性冲突。它是否存在奇异性、松弛是否改善逼近，是另外的问题。逐步矩阵例子和共同法向示意见 [[vertex-continuity-relaxation]]。

### 2.6 非齐次牵引提升与密度参数化

位移法把设计密度作用在刚度张量 $\boldsymbol C_\rho$ 上；混合形式的主未知量是应力，密度进入的是柔度张量 $A_\rho=\boldsymbol C_\rho^{-1}$，出现在双线性型 $a_\rho(\boldsymbol\sigma,\boldsymbol\tau)$ 中（插值格式与记号沿用 [[linear-elasticity]] §2.3；modified SIMP 与应力场物理可解释性的关系见 [[../../literature/topopt/piml/translations/Huang2022-problemindependentmachine-zh]]）。这一差别决定了非齐次牵引必须如何处理。

牵引边界 $\Gamma_N$ 上的非齐次载荷 $\boldsymbol t$ 作为本质条件有两种处理方式：

1. **代数消元法**：直接对已知边界应力自由度置行置值；
2. **牵引提升（Lifting）**：取设计无关的 $\boldsymbol\sigma_g$ 满足 $\boldsymbol\sigma_g\boldsymbol n=\boldsymbol t$ on $\Gamma_N$，令 $\boldsymbol\sigma=\boldsymbol\sigma_0+\boldsymbol\sigma_g$（其中 $\boldsymbol\sigma_0$ 满足齐次牵引条件 $\boldsymbol\sigma_0\boldsymbol n=\mathbf 0$），右端相应出现 $-a_\rho(\boldsymbol\sigma_g,\boldsymbol\tau)$ 与 $-b(\boldsymbol\sigma_g,\boldsymbol v)$ 两项。

两者在前向求解中等价。但在密度拓扑优化中 $a_\rho$ 依赖 $\rho$；若沿用代数消元法而不显式分离齐次未知量与给定提升，在对能量目标求导时极易遗漏提升交叉项。因此拓扑优化中统一采用 Lifting 表述（见 [[../../papers/huzhang-topopt/high-order-huzhang-topopt-draft-zh]] §2.2 与 §3.2），目标与导数一律基于总应力 $\boldsymbol\sigma=\boldsymbol\sigma_0+\boldsymbol\sigma_g$ 展开。

---

## 3. 有限元空间与离散 inf-sup

### 3.1 应力空间 $\Sigma_h$

$\Sigma_h\subset H(\mathrm{div};\mathbb S)$：对称张量值、法向迹跨单元连续，次数 $k$。
Hu–Zhang 用 subsimplex（顶点/边/单元面/单元体）上的多指标构造 Bubble 丰富基底，对称性通过对称指标展开为独立分量。
张量标架按子单纯形维数分级：$i$ 维子单纯形上，$d(d+1)/2$ 个对称张量分量中恰有 $i(i+1)/2$ 个跨单元断开、其余保持连续；边子单纯形上的标架取该边的单位法向与单位切向 $(\boldsymbol n_f,\boldsymbol t_f)$，顶点与单元内部取笛卡尔基。正是这一分级同时给出 $H(\mathrm{div})$ 协调性与逐点对称性，也决定了法向迹逐面为不超过 $k$ 次多项式；内部公共面采用共同法向时两侧迹相等，但不同边界面的牵引数据仍需满足 §2.5.2 的可表示性条件。边标架的几何定向与外法向的关系见 §2.5.1。

### 3.2 位移空间 $V_h$

分片不连续 Lagrange $P_{k-1}$，张量值（维度 $=d$），跨单元无连续性要求。

**刚体位移（RM）完备性**：单元上的刚体位移空间 $\mathrm{RM}(K)=\{\boldsymbol a+\boldsymbol\omega\times\boldsymbol x\}$ 含平动与无穷小转动，转动部分对 $\boldsymbol x$ 是一次的（[[linear-elasticity]] §2.1：位移梯度的反对称部分即无穷小刚体转动，不产生应变能）。
因此 $\mathrm{RM}(K)\subset V_h|_K$ 当且仅当 $k-1\ge1$，即 $k\ge2$。
$k=1$ 的 $P_0$ 位移只含平动，**不完备包含 RM**，丧失表征单元局部微小转动的能力。这对静力求解不致命（§5），但在变密度拓扑优化中有决定性后果，见 §5 末。

### 3.3 离散 inf-sup 条件

该配对满足离散 inf-sup 的充分条件是 $k\ge d+1$。
**低次情形** $k\le d$（2D 即 $k=1,2$）时 $V_h$ 相对 $\Sigma_h$ 太小，鞍点系统 (4) 的 $(2,2)$ 零块使问题不稳定，必须补跳量稳定化。

### 3.4 顶点应力连续性的部分松弛（角点松弛）

原 Hu–Zhang 空间的连续 Lagrange 部分与顶点取零的 $H(\mathrm{div})$ bubble 共同带来顶点应力单值约束。该约束强于 $H(\mathrm{div})$ 所需的内部法向迹连续：二维不相容牵引–牵引角点可能无法由一个对称应力值满足两侧牵引。位移–牵引交界本身不构成这个障碍。

Hu–Ma (2021) §4.1 在角点附近构造两个子三角形，沿内部公共边拆分角点纯切向应力自由度，保留法向迹自由度共享。二维两单元情形由 3 个独立角点自由度扩展为 4 个；在共同法向 $n_e$ 下保留 $S_Rn_e=S_Tn_e$，允许 $S_R-S_T=\alpha t_et_e^T$。新空间扩大，但仍属于对称 $H(\mathrm{div})$ 空间，且公共边整条的法向迹连续必须保持。

详细解释由 [[vertex-continuity-relaxation|应力顶点连续性与角点松弛]] 维护：包含原空间为何施加顶点连续、牵引相容条件、自由边也是牵引边、共同法向与实际界面力、逐步矩阵求解，以及位移–牵引角点的区别。

边界数据相容时不必为精确施加牵引而松弛；原文 §5.2 另外考察了零牵引奇异角点的逼近改善。§3 的内部顶点松弛用于嵌套空间，不与边界动机混同。原文也讨论多单元及三维扩展，“两单元、3 变 4”只是本节采用的具体构造。

既有实现记录：SOPTX 使用网格中已存在的内部公共边，要求角点恰好关联两个单元、各含一条相应边界边；该实现限制不是 Hu–Ma 一般方法的适用上限。本轮未重新核验实现，编号、拓扑检查和装配映射以 `soptx:docs/fem/huzhang-mixed-fem-implementation.md` 为入口。既有源码定位保留于 §6。

论文当前稿 [[../../papers/huzhang-topopt/high-order-huzhang-topopt-draft-zh]] §3.2 保留处理概要；历史详细表述见 [[../../papers/huzhang-topopt/high-order-huzhang-topopt-draft-zh-old]] §3.4。本概念页的解释性例子不作为这些算例的实际边界数据。

---

## 4. 低阶稳定化：矩阵型跳量惩罚

### 4.1 数学格式

对 $k\le d$，在位移分量上补面跳量惩罚 $c(\boldsymbol u_h,\boldsymbol v_h)$：

$$
c(\boldsymbol u_h,\boldsymbol v_h)
=\sum_{F\in\mathcal F_h}\alpha\,h_F\int_F
[\![\boldsymbol u_h]\!]:[\![\boldsymbol v_h]\!]\,\mathrm{d}s,
\tag{5}
$$

$$
[\![\boldsymbol w]\!]=\tfrac12(\boldsymbol w\boldsymbol\nu^{\mathsf T}
+\boldsymbol\nu\boldsymbol w^{\mathsf T}),
\tag{6}
$$

其中 $[\![\boldsymbol w]\!]$ 是矩阵跳量（对称梯度型），$\mathcal F_h$ 取**内部面与位移边界面的并集、不含牵引边界面**：

$$
\mathcal F_h=\{\text{内部面}\}\cup\Gamma_D
\quad(\text{不施加于 }\Gamma_N).
\tag{7}
$$

### 4.2 缩放律 $\alpha=\mu/L_0^2$ 与 $h_F$ 幂次

论文式物理量纲缩放取

$$
\alpha=\frac{\mu}{L_0^{2}},
\qquad
L_0=\max(\text{计算域包围盒边长}),
\tag{8}
$$

系数总效果为 $\alpha\cdot h_F$。
2D 面测度 $h_F$ 本身是一阶小量，惩罚块整体随 $h_F^2\to0$ 弱一致衰减。
选择依据：

1. **量纲匹配**：$\mu$ 是剪切模量（应力单位），除以特征尺度平方后与柔度块 $A\sim1/\mu$ 在 $h\to0$ 时保持幂次协调，惩罚不改变原问题的收敛速率；
2. **弱一致性**：$h_F^2$ 衰减使 $c(\cdot,\cdot)\to0$ 弱收敛于零，恢复 inf-sup 而不改变极限解。

**密度相关材料下的记号补充**。式 (8) 中的 $\mu$ 指均质材料的剪切模量。在密度法拓扑优化中 $\mu=\mu(\rho)$ 随设计变化，直接代入会使惩罚强度随设计漂移；此时应取固定的参考剪切模量 $\mu_{\mathrm{ref}}$，并显式引入无量纲参数 $\gamma_0$：

$$
\gamma_F=\gamma_0\frac{\mu_{\mathrm{ref}}}{L_0^{2}}.
\tag{8'}
$$

$\gamma_0$ 的取值敏感性通过网格与材料参数消融考察，见 [[../../papers/huzhang-topopt/high-order-huzhang-topopt-draft-zh]] §3.3。

作为对比，另一种 γ/h_F 型（DG 标准缩放）在本问题中失效：面测度 $f_m=h_F$ 已乘进积分配置，γ/h_F 与之抵消后净效果为 **$O(\gamma)$ 常数**——惩罚不随 $h\to0$ 衰减，粗层阶看似正常、细层位移/应力阶塌陷、散度发散。

### 4.3 稳定化后的鞍点系统与 $\mathcal F_h$ 选取

稳定化后的鞍点系统变为

$$
\begin{bmatrix} A & B \\ B^{\mathsf T} & -J \end{bmatrix}
\begin{bmatrix} \boldsymbol\sigma_h \\ \boldsymbol u_h \end{bmatrix}
=\begin{bmatrix} \boldsymbol f_\sigma \\ \boldsymbol f_u \end{bmatrix},
\qquad
J_{ij}=c(\boldsymbol\phi_i,\boldsymbol\phi_j).
\tag{9}
$$

$\mathcal F_h$ 为何不含 $\Gamma_N$：牵引边界是本质边界条件，已在应力自由度上强加，无需（也不应）用位移跳量惩罚去"补强"；若对 $\Gamma_N$ 也加惩罚，将把惩罚块贡献引入 traction 载荷路径，改变边界泛函。
位移边界 $\Gamma_D$ 上的位移是自然边界条件，惩罚在这里强化 $\boldsymbol u=\bar{\boldsymbol u}$ 的约束。
这一取舍的直接后果是 **$k=2$ 时 $H(\mathrm{div})$ 收敛阶由 2 降到 1**（见 §5）。

---

## 5. 收敛性结果与阶次下限

数值验证设置：单位正方形域、平面应变、$\lambda=1$、$\mu=0.5$、光滑制造解（精确位移 $u_1=u_2=\sin\pi x\sin\pi y$），$\Gamma_D=\{x=0\}\cup\{y=0\}$ 施加齐次位移、$\Gamma_N=\{x=1\}\cup\{y=1\}$ 施加精确牵引。
制造解完整定义见 `soptx:experiments/paper_topopt_huzhang/`；观测阶的实测复现口径见该目录 `results_analysis.md`。误差绝对值随物理量纲缩放而变，跨来源不可直接比对，只有观测阶是尺度无关量。

**高阶 $k\ge3$（无稳定化）**：

- 应力 $L^2$ 误差达到 $\mathcal O(h^{k+1})$ 的理论最优超收敛；对比同阶位移元（$P_{k-1}$ 位移）因形函数求导应力降至 $\mathcal O(h^{k-1})$，胡张元在应力场刻画上优势显著；
- 位移 $L^2$ 误差与应力 $H(\mathrm{div})$ 误差均为 $\mathcal O(h^{k})$ 最优收敛；$H(\mathrm{div})$ 误差由应力 $L^2$ 逼近与散度误差共同主导，其收敛证实法向牵引力跨单元连续。

**低阶 $k=1,2$（稳定化）**，观测阶如下：

| $k$ | $\|\boldsymbol u-\boldsymbol u_h\|_{0}$ | $\|\boldsymbol\sigma-\boldsymbol\sigma_h\|_{0}$ | $\|\boldsymbol\sigma-\boldsymbol\sigma_h\|_{H(\mathrm{div})}$ |
|---|---|---|---|
| 1 | 1（最优） | 1.5 | 1（最优） |
| 2 | 2 | 2 | 1（**降阶**） |

- $k=1$：位移 $L^2$ 与应力 $H(\mathrm{div})$ 均严格达到 1 阶最优，消除低阶单元的自锁与数值震荡；
- $k=2$：位移、应力 $L^2$ 保持 2 阶，应力 $H(\mathrm{div})$ 向 1 阶退化。归因：混合边界下稳定化不施加于 $\Gamma_N$（§4.3），局部稳定化减弱叠加非多项式牵引在 $\Gamma_N$ 上的投影误差，主导并降低散度逼近精度——与纯位移边界下 Chen 等（稳定化混合元）的 2 阶最优不同。

**阶次下限：静力可用 $\ne$ 拓扑优化可用**。上表容易被读成"$k=1$ 已经够用"，但博士论文第五章的算例把 $k=1$ 排除在外，理由不在收敛阶而在 §3.2 的 RM 完备性。三层结论必须分开陈述：

| 层次 | $k=1$ | 依据 |
|---|---|---|
| 离散 inf-sup 稳定性 | 裸格式不满足，**跳量稳定化可恢复** | §3.3、§4 |
| 静力收敛性 | **可用**，位移 $L^2$ 与应力 $H(\mathrm{div})$ 均达 1 阶最优 | 本节上表 |
| 变密度拓扑优化 | **不可用** | §3.2 RM 不完备 |

机理：$P_0$ 位移无法表征单元局部微小转动，低密度区域的局部应变能评估严重失真，使演化过度依赖人工界面惩罚，进而诱发数值震荡与非物理拓扑。
因此稳定化格式在拓扑优化中的下限取 $k=2$（$P_1$ 位移已完备含 RM，提供稳健的底层物理驱动），$k=3,4$ 用于考察高阶原生（无惩罚）格式。这是 SOPTX 侧 `comparison_orders = 2,3,4` 白名单的唯一实质依据——它与迹空间可表示性无关：局部法向迹为不超过 $k$ 次多项式，连续 $P_1$ 牵引能否精确表示仍须检查具体边界迹空间及角点相容条件（§2.5.2）。

---

## 6. 参考依据

本页根据博士论文第五章与后续核对重新组织，不复制论文正文；论文源码与定稿 PDF 由 `xtu-phd-thesis` 维护，本页只保留从中提炼的可复用理论。

- `xtu-phd-thesis:thesis/brightPhD.pdf#第五章` — 胡张元构造、混合弱形式与鞍点结构（§2.1–§2.3、§3.1–§3.3）
- `xtu-phd-thesis:thesis/brightPhD.pdf#第5.4.2-5.4.3节` — 矩阵型跳量惩罚的构造与 $H(\mathrm{div})$ 降阶归因（§4、§5）
- `xtu-phd-thesis:thesis/brightPhD.pdf#第5.6.1-5.6.3节` — 牵引提升与总应力表述（§2.6）
- `xtu-phd-thesis:thesis/brightPhD.pdf#第5.6.2节` — 两端固支梁算例排除 $k=1$ 的理由：$P_0$ 位移不完备包含 RM 空间（§3.2、§5 阶次下限表）
- Hu & Zhang, arXiv:1406.7457 — 单纯形网格上弹性问题的共形对称应力混合元族，原始胡张元（§3.1）
- Hu & Ma, *CMAM* 21(1) (2021), 89–108, doi:10.1515/cmam-2020-0003 — 顶点应力连续性的部分松弛（§3.4、§2.5.3 情形 3）
- Chen–Hu–Huang, *Math. Comp.* 87 (2018), Corollary 3.7(3.18) — $k\ge n+1$ 时应力超收敛（§5）
- [[external-loads]] §3.2 — 可表示性条件下的牵引施加与 $P_1$ 迹投影的守恒性（§2.5.2）
- `soptx:src/soptx/fem/spaces/huzhang_fe_space_2d.py`（`_get_corner_data`、`node_to_internal_dof`、`cell_to_dof`、`_transform_matrix`）— §3.4 的两单元限制与自由度归属，2026-08-07 核对、2026-09-16 复核
- `soptx:experiments/paper_topopt_huzhang/results_analysis.md` — §5 观测阶的实测复现来源

本页不替代混合有限元专著或论文正文，也不把当前混合元推广到动力学、有限变形或非线性材料；未经实测确认的绝对误差、单次运行的数值结论与投稿证据口径不写入本页。
