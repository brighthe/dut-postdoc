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
date_update: 2026-09-16
---

# 胡张应力—位移混合元、变分形式与低阶稳定化

> 胡张元把应力提升为 $H(\mathrm{div})$ 顺应、对称张量值的主未知量，与分片不连续位移元组成对称不定鞍点系统，直接逼近应力——这让应力场自带物理可解释性；代价是低次空间不满足离散 inf-sup，需矩阵型跳量惩罚稳定化，且 traction/位移边界语义与位移型元相反。

本页整理应力—位移混合元的理论闭环：混合变分形式 → $H(\mathrm{div})$ 应力空间与不连续位移空间 → 鞍点系统 → 边界条件的对偶语义与牵引数据的可施加性 → 低次稳定化 → 收敛阶与阶次下限。
它**复用位移型 [[../linear-elasticity]] 的几何、记号与 Hooke 本构**，只引入混合变量与相应离散。

本页**不覆盖**实现层内容：程序分层、配置键、自由度编号与装配映射算法、角点松弛可用的网格拓扑限制、FEALPy 4.0 API 迁移，均见 `soptx:docs/fem/huzhang-mixed-fem-implementation.md`；外载荷的程序架构见 `soptx:docs/fem/load-handling-implementation.md`。3D 无松弛空间构造的端到端验证尚未完成，本页不作断言。

---

## 1. 模型假设与几何

与 [[../linear-elasticity]] §1 相同的记号：设 $\Omega\subset\mathbb R^d$（$d=2$ 或 $3$）为有界弹性体，$\Gamma_D$ 和 $\Gamma_N$ 是边界上互不相交的相对开集且 $\partial\Omega=\overline{\Gamma_D}\cup\overline{\Gamma_N}$。
$\Gamma_D$ 上施加位移边界条件，$\Gamma_N$ 上施加表面力边界条件。
小变形、静力、各向同性线弹性，Hooke 本构以**柔度张量** $A=\boldsymbol C^{-1}$（满足 $\boldsymbol\varepsilon=A\boldsymbol\sigma$）表达，与 [[../linear-elasticity]] §2.2 的 $\boldsymbol C$ 互为逆。
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

牵引条件在混合形式下是本质条件，必须写进应力法向迹自由度。这就把一个位移法里不存在的问题摆上台面：给定的牵引数据能否被 $\Sigma_h$ 的法向迹**精确表示**，以及写入自由度的操作是否**良定义**。三个环节彼此独立——标架定向、迹空间包含、多面共享点的一致性——任一环节失效都会让离散载荷偏离物理载荷，且不随网格加密消失。

先给出各类外载荷的总体判据：

| 载荷 | 在胡张混合法中的处理 | 与位移法的关系 |
|---|---|---|
| 连续面牵引 $\boldsymbol t$ | 本质条件，在应力法向迹自由度上强插值 $(\boldsymbol\sigma_h\boldsymbol n)\vert_{\Gamma_N}=\boldsymbol t$ | 连续分片一次数据是迹空间的子集（§2.5.2），强插值为恒等映射、无截断；位移法侧求积亦精确，两法施加同一载荷泛函 |
| 集中力 $\boldsymbol P\delta_{\boldsymbol x_0}$ | 不可直接施加：位移检验空间 $\boldsymbol V=[L_2(\Omega)]^d$ 无逐点值，应力法向迹空间 $H^{-1/2}(\partial\Omega)$ 也容不下点测度 | 位移法在离散层可用点值泛函，混合法没有对应机制；受控对比须先把点力按特征尺度 $l$ 分布化，再由连续 $P_1$ 迹投影得到 $\boldsymbol t_h$，两法施加同一份 $\boldsymbol t_h$ |
| 体力 $\boldsymbol b$ | $\int_\Omega\boldsymbol b\cdot\boldsymbol v_h\,\mathrm dx$ 进入位移方程右端，不涉及本质条件 | 两法完全一致 |

各类外载荷数据的正则性判据、$\delta$ 的负阶 Sobolev 指标、一致节点力系数与 $P_1$ 迹 $L^2$ 投影的守恒性证明由 [[../external-loads]] 维护，本页只给在胡张形式下起作用的三条判据。

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
T_h=\bigl\{(\boldsymbol\sigma_h\boldsymbol n)\vert_{\Gamma_N}\ :\ \boldsymbol\sigma_h\in\Sigma_h\bigr\}.
$$

由 §3.1 的构造，$\Sigma_h$ 的法向迹跨面连续且逐面为 $k$ 次多项式向量，故对 $\Gamma_N$ 的面剖分上的连续分片一次标量空间 $W_h^1$ 有

$$
[W_h^1]^d\subseteq T_h\qquad\text{对任意 }k\ge 1 .
$$

**推论**：对 $\boldsymbol t_h\in[W_h^1]^d$，把 $\boldsymbol t_h$ 强插值到法向迹自由度是**恒等映射**——不截断、不投影、无信息损失；位移法侧对同一 $\boldsymbol t_h$ 的 Neumann 弱积分用足够阶数求积亦精确。两法因此施加同一个载荷泛函，方法对照才是在同一载荷下进行。注意这不等于"同一离散解"：两法的离散空间不同，解自然不同，相等的是载荷——那正是对照要控制的变量。

**反例**：含面内跳跃的原始阶跃牵引 $\bar{\boldsymbol t}_l$ 不属于 $T_h$（$T_h$ 逐面多项式且跨面连续，容不下面内间断），对它做节点插值会改写跨越载荷区端点那一面上的数据，使离散合力偏离 $\boldsymbol P$。此类数据必须先按 [[../external-loads]] §3.4 投影到 $[W_h^1]^d$ 再施加；包含关系与恒等性的完整论证见该页 §3.5。

#### 2.5.3 共享顶点与角点上的良定义性

一个顶点（3D 中为棱边）通常被多个边界面共享，写入时同一个自由度会被各面各写一次。是否良定义分三种情形：

1. **数据在共享点连续、两侧标架相同**：各面给出同一个值，写入顺序无关，良定义；
2. **数据在共享点两侧不等、标架相同**（同一条直边上的载荷区端点）：两个候选值不等，"后写者胜"会把端点值整份判给写入次序靠后的一侧，破坏载荷的镜像对称性并引入净力矩——合力可能仍对，力矩已错，且不随 $k$ 增大消失。良定义的写入是取两侧平均，它保持合力且与 $[W_h^1]^d$ 中插值点的唯一化一致。但按 §2.5.2，这类间断数据本就不该直接施加；投影之后数据连续，平均自动退化为情形 1。**平均是对未投影数据的兜底，不构成对它的许可**；
3. **几何角点**：两侧边界面的标架 $(\boldsymbol n_f,\boldsymbol t_f)$ 本身不同，同一个应力张量在两侧给出不同的标架分量，不存在可取的公共值。这不是仲裁问题而是无解问题——顶点处强制单值会使节点插值方程组无解。唯一出路是 §3.4 的自由度分裂：让两侧各持一份纯切向自由度，分裂后该角点在每一侧只被写入一次，写入退化为唯一。分裂可用的网格拓扑前提同样见 §3.4。

### 2.6 非齐次牵引提升与密度参数化

位移法把设计密度作用在刚度张量 $\boldsymbol C_\rho$ 上；混合形式的主未知量是应力，密度进入的是柔度张量 $A_\rho=\boldsymbol C_\rho^{-1}$，出现在双线性型 $a_\rho(\boldsymbol\sigma,\boldsymbol\tau)$ 中（插值格式与记号沿用 [[../linear-elasticity]] §2.3；modified SIMP 与应力场物理可解释性的关系见 [[../../literature/topopt/piml/translations/Huang2022-problemindependentmachine-zh]]）。这一差别决定了非齐次牵引必须如何处理。

牵引边界 $\Gamma_N$ 上的非齐次载荷 $\boldsymbol t$ 作为本质条件有两种处理方式：

1. **代数消元法**：直接对已知边界应力自由度置行置值；
2. **牵引提升（Lifting）**：取设计无关的 $\boldsymbol\sigma_g$ 满足 $\boldsymbol\sigma_g\boldsymbol n=\boldsymbol t$ on $\Gamma_N$，令 $\boldsymbol\sigma=\boldsymbol\sigma_0+\boldsymbol\sigma_g$（其中 $\boldsymbol\sigma_0$ 满足齐次牵引条件 $\boldsymbol\sigma_0\boldsymbol n=\mathbf 0$），右端相应出现 $-a_\rho(\boldsymbol\sigma_g,\boldsymbol\tau)$ 与 $-b(\boldsymbol\sigma_g,\boldsymbol v)$ 两项。

两者在前向求解中等价。但在密度拓扑优化中 $a_\rho$ 依赖 $\rho$；若沿用代数消元法而不显式分离齐次未知量与给定提升，在对能量目标求导时极易遗漏提升交叉项。因此拓扑优化中统一采用 Lifting 表述（见 [[high-order-huzhang-topopt-draft-zh]] §2.2 与 §3.2），目标与导数一律基于总应力 $\boldsymbol\sigma=\boldsymbol\sigma_0+\boldsymbol\sigma_g$ 展开。

---

## 3. 有限元空间与离散 inf-sup

### 3.1 应力空间 $\Sigma_h$

$\Sigma_h\subset H(\mathrm{div};\mathbb S)$：对称张量值、法向迹跨单元连续，次数 $k$。
Hu–Zhang 用 subsimplex（顶点/边/单元面/单元体）上的多指标构造 Bubble 丰富基底，对称性通过对称指标展开为独立分量。
张量标架按子单纯形维数分级：$i$ 维子单纯形上，$d(d+1)/2$ 个对称张量分量中恰有 $i(i+1)/2$ 个跨单元断开、其余保持连续；边子单纯形上的标架取该边的单位法向与单位切向 $(\boldsymbol n_f,\boldsymbol t_f)$，顶点与单元内部取笛卡尔基。正是这一分级同时给出 $H(\mathrm{div})$ 协调性与逐点对称性，也决定了法向迹逐面为 $k$ 次多项式、跨面连续（§2.5.2 据此判定可施加性）。边标架的几何定向与外法向的关系见 §2.5.1。

### 3.2 位移空间 $V_h$

分片不连续 Lagrange $P_{k-1}$，张量值（维度 $=d$），跨单元无连续性要求。

**刚体位移（RM）完备性**：单元上的刚体位移空间 $\mathrm{RM}(K)=\{\boldsymbol a+\boldsymbol\omega\times\boldsymbol x\}$ 含平动与无穷小转动，转动部分对 $\boldsymbol x$ 是一次的（[[../linear-elasticity]] §2.1：位移梯度的反对称部分即无穷小刚体转动，不产生应变能）。
因此 $\mathrm{RM}(K)\subset V_h|_K$ 当且仅当 $k-1\ge1$，即 $k\ge2$。
$k=1$ 的 $P_0$ 位移只含平动，**不完备包含 RM**，丧失表征单元局部微小转动的能力。这对静力求解不致命（§5），但在变密度拓扑优化中有决定性后果，见 §5 末。

### 3.3 离散 inf-sup 条件

该配对满足离散 inf-sup 的充分条件是 $k\ge d+1$。
**低次情形** $k\le d$（2D 即 $k=1,2$）时 $V_h$ 相对 $\Sigma_h$ 太小，鞍点系统 (4) 的 $(2,2)$ 零块使问题不稳定，必须补跳量稳定化。

### 3.4 顶点应力连续性的部分松弛（角点松弛）

胡张元构造中，为获得"晶格点 × 张量基元"的点值自由度，网格顶点处对部分应力分量施加单值约束（等价于顶点 $C^0$ 连续性）。
当顶点位于复杂边界交汇处（相邻两段边界施加不同类型边界条件，或牵引数据在角点两侧不相容）时，强制该顶点所有相关应力分量单值会使节点插值方程组无解，离散应力无法精确匹配两侧物理边界条件。
借鉴 Hu–Ma (2021) 的**顶点应力连续性局部松弛**策略，仅在复杂边界顶点处做局部拆分：

1. **确定分割线**：Hu–Ma 的一般策略允许在含角点 $x_c$ 的单元内部引入虚拟分割线。SOPTX 采用一个更受限的特例：**分割线取为网格中已存在的一条内部边** $e$，即要求 $x_c$ 恰好由两个单元 $K^+$、$K^-$ 包围、二者恰好共享一条与 $x_c$ 相连的内部边，且各含恰好一条与 $x_c$ 相连的边界边（两条互不相同）。这样无需在单元内部重构子单元基函数，全局网格拓扑也不改变；
2. **自由度解耦**：角点处原本单值的纯切向应力分量（$\mathbb T_e$-型自由度）沿分割边拆分为两个独立自由度，分属 $K^+$、$K^-$，两侧离散应力独立满足各自边界约束；
3. **法向保持单值**：决定法向迹的应力分量（$\mathbb N_e$-型自由度）在 $x_c$ 及分割边 $e$ 上仍严格单值，保持 $H(\mathrm{div})$ 协调性；
4. **局部自由度扩充**：2D 三角形角点对称应力张量原 3 个点值自由度，松弛后 1 个纯切向分量扩展为两个，全局独立自由度由 3 增至 4。记为 $(d_0,d_1,d_2,d_3)$，其中 $d_0,d_1$（$\mathbb N_e$-型）两单元共享，$d_2$、$d_3$ 分别私有于 $K^-$、$K^+$。

效果：把顶点 $C^0$ 连续性引发的插值方程组无解，转化为"分侧满足"的自由度结构，角点邻域精确匹配分割边两侧不相容牵引数据，消除边界条件不精确满足主导的误差集中。
代价是对顶点扇形有结构要求：不满足上述两单元条件的角点必须先做局部网格调整才能启用松弛；SOPTX 对不满足者直接报错而非静默跳过。
该思路可推广至更复杂的二维多单元交汇角点与三维顶点/棱边连续性（Hu–Ma 2021）。

> **来源**：本节第 1 条的两单元限制与第 4 条的自由度归属按 SOPTX 实现核对（出处见 §6）；[[high-order-huzhang-topopt-draft-zh]] §3.4 已同步为同一算法。角点自由度的编号与装配映射属实现，见 `soptx:docs/fem/huzhang-mixed-fem-implementation.md`。

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

$\gamma_0$ 的取值敏感性通过网格与材料参数消融考察，见 [[high-order-huzhang-topopt-draft-zh]] §3.3。

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
因此稳定化格式在拓扑优化中的下限取 $k=2$（$P_1$ 位移已完备含 RM，提供稳健的底层物理驱动），$k=3,4$ 用于考察高阶原生（无惩罚）格式。这是 SOPTX 侧 `comparison_orders = 2,3,4` 白名单的唯一实质依据——它与迹空间可表示性无关：$\Sigma_h$ 的法向迹是跨边连续的 $k$ 次多项式，连续 $P_1$ 迹载荷（§2.5.2）对任意 $k\ge1$ 都可精确表示。

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
- [[../external-loads]] §3.4–§3.5 — 牵引迹空间的包含关系、强插值恒等性与 $P_1$ 迹投影的守恒性（§2.5.2）
- `soptx:src/soptx/fem/spaces/huzhang_fe_space_2d.py`（`_get_corner_data`、`node_to_internal_dof`、`cell_to_dof`、`_transform_matrix`）— §3.4 的两单元限制与自由度归属，2026-08-07 核对、2026-09-16 复核
- `soptx:experiments/paper_topopt_huzhang/results_analysis.md` — §5 观测阶的实测复现来源

本页不替代混合有限元专著或论文正文，也不把当前混合元推广到动力学、有限变形或非线性材料；未经实测确认的绝对误差、单次运行的数值结论与投稿证据口径不写入本页。
