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
date_update: 2026-08-14
---

# 胡张应力—位移混合元、变分形式与低阶稳定化

> **一句话**：胡张元把应力提升为 $H(\mathrm{div})$ 顺应、对称张量值的主未知量，与分片不连续位移元组成对称不定鞍点系统，直接逼近应力——这让应力场自带物理可解释性；代价是低次空间不满足离散 inf-sup，需矩阵型跳量惩罚稳定化，且 traction/位移边界语义与位移型元相反。

本页整理应力—位移混合元的最小理论闭环：混合变分形式 → $H(\mathrm{div})$ 应力空间与不连续位移空间 → 鞍点系统 → 低次稳定化 → 收敛阶结果。
它**复用位移型 [[../linear-elasticity]] 的几何、记号与 Hooke 本构**，只引入混合变量与相应离散。

本页**不覆盖**：角点松弛在 SOPTX 中的实现与 checkerboard 网格拓扑限制、FEALPy 4.0 实现与 API 迁移细节（属实现，见 SOPTX 文档 `docs/fem/huzhang-mixed-fem.md`）、3D 无松弛空间构造的端到端验证，以及 SOPTX 代码的逐符号映射（见 SOPTX `examples/huzhang_elasticity/math_spec.md`）。

---

## 1. 模型假设与几何

与 [[../linear-elasticity]] §1 相同的记号：设 $\Omega\subset\mathbb R^d$（$d=2$ 或 $3$）为有界弹性体，$\Gamma_D$ 和 $\Gamma_N$ 是边界上互不相交的相对开集且 $\partial\Omega=\overline{\Gamma_D}\cup\overline{\Gamma_N}$。
$\Gamma_D$ 上施加位移边界条件，$\Gamma_N$ 上施加表面力边界条件。
小变形、静力、各向同性线弹性，Hooke 本构以**柔度张量** $A=\boldsymbol C^{-1}$（满足 $\boldsymbol\varepsilon=A\boldsymbol\sigma$）表达，与 [[../linear-elasticity]] §2.2 的 $\boldsymbol C$ 互为逆。
混合元不采用 §2.3 的设计密度参数化。

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

### 2.4 边界条件与外载荷处理

在应力—位移混合有限元中，由于独立主未知量变为对称应力 $\boldsymbol\sigma$，边界条件与外载荷的处理方式与经典位移元呈现**严格的变分对偶性**。

#### 2.4.1 边界条件的对偶语义与牵引提升（Lifting）

| 物理边界类型 | 物理方程 | 标准位移法 (LFEM) | 胡张混合法 (HZMFEM) | 变分对偶本质 |
|---|---|---|---|---|
| **位移边界 $\Gamma_D$** | $\boldsymbol u = \bar{\boldsymbol u}$ | **本质边界（强施加）**<br>直接在位移自由度上置行置值 | **自然边界（弱施加）**<br>弱加进应力方程右端项 (2) | **几何约束对偶**（位移强 $\leftrightarrow$ 混合弱） |
| **牵引边界 $\Gamma_N$** | $\boldsymbol\sigma\boldsymbol n = \boldsymbol t$ | **自然边界（弱施加）**<br>通过边界虚功积分进入外力向量 | **本质边界（强施加）**<br>强加在应力法向迹自由度上 | **外力载荷对偶**（位移弱 $\leftrightarrow$ 混合强） |

**非齐次牵引提升（Traction Lifting）**：
在混合法中，牵引边界 $\Gamma_N$ 上的非齐次载荷 $\boldsymbol t$ 作为本质条件有两种处理方式：
1. **代数消元法**：直接对已知边界应力自由度置行置值；
2. **牵引提升（Lifting）**：取设计无关的 $\boldsymbol\sigma_g$ 满足 $\boldsymbol\sigma_g\boldsymbol n = \boldsymbol t$ on $\Gamma_N$，令 $\boldsymbol\sigma = \boldsymbol\sigma_0 + \boldsymbol\sigma_g$（其中 $\boldsymbol\sigma_0$ 满足齐次牵引条件 $\boldsymbol\sigma_0\boldsymbol n = \mathbf{0}$），右端相应出现 $-a_\rho(\boldsymbol\sigma_g,\boldsymbol\tau)$ 与 $-b(\boldsymbol\sigma_g,\boldsymbol v)$ 两项。

两者在前向求解中等价。但在密度拓扑优化中，柔度张量 $a_\rho$ 依赖材料密度 $\rho$；若沿用代数消元法而不显式分离齐次未知量与给定提升，在对能量目标求导时极易遗漏提升交叉项。因此拓扑优化中统一采用 Lifting 表述（见 [[../../papers/arbitrary-order-huzhang-topopt-draft-zh]] §2.2 与 §3.2），目标与导数一律基于总应力 $\boldsymbol\sigma = \boldsymbol\sigma_0 + \boldsymbol\sigma_g$ 展开。

#### 2.4.2 表面牵引载荷离散机制（分布力与集中力）

##### 1. 分布力（连续面力 / 均布牵引）的处理
对于施加在边界 $\Gamma_N$ 上的连续表面力 $\boldsymbol t(\boldsymbol x)$（如二维轴承装置顶部的常数均布压应力 $\boldsymbol t_0$）：
* **位移法 (LFEM)**：属于自然边界条件，通过边界高斯弱积分计算外力向量：
  $$
  \boldsymbol F_i = \int_{\Gamma_N} \boldsymbol t(\boldsymbol x) \cdot \boldsymbol v_i\,\mathrm ds \quad (q = 2k + 2).
  $$
* **胡张混合法 (HZMFEM)**：属于本质边界条件，直接在对称应力法向迹自由度上强插值施加：
  $$
  (\boldsymbol\sigma_h \boldsymbol n)\big|_{\Gamma_N} = \boldsymbol t(\boldsymbol x).
  $$
* **两法等价性**：对于常数均布面力，常数函数天然属于任意阶多项式迹空间（强插值无截断、高斯积分精确），两法在**数学上 $100\%$ 精确等价**。

##### 2. 集中力（点载荷）的处理
对于作用在边界点 $\boldsymbol x_0 \in \Gamma_N$ 上的集中载荷 $\boldsymbol P = P\boldsymbol e$（如两端固支梁底边中点载荷）：
* **位移法 (LFEM) 原生机制**：位移空间 $V \subset H^1$ 具有空间连续性，点力可直接作为点值泛函 $\langle \boldsymbol P\delta_{\boldsymbol x_0}, \boldsymbol v_h \rangle = \boldsymbol P \cdot \boldsymbol v_h(\boldsymbol x_0)$ 累加到对应几何节点的右端外力分量中；
* **胡张混合法 (HZMFEM) 的非适定性与分布化**：
  * 位移测试空间仅为分片不连续的 $V = [L_2(\Omega)]^d$，在二维及以上无连续点值定义（$\delta_{\boldsymbol x_0} \notin V^*$）；
  * 应力法向迹空间 $H^{-1/2}(\partial\Omega)$ 亦无法容纳点测度。因此集中力在混合变分形式中**数学非适定**，无法直接赋给法向迹自由度；
  * 必须在物理特征尺度 $l$（如 $l = 1\,\mathrm{mm}$）上转化为局部均布面力：$\bar{\boldsymbol t}_l(\boldsymbol x) = \frac{P}{l}\chi_{\Gamma_{N,l}}(\boldsymbol x)\boldsymbol e$。
* **受控对比中的统一离散与守恒**：
  * 若位移法使用节点点力而混合法使用局部均布面力，两者吸收的载荷泛函将产生外生差异，破坏受控对比的公允性；
  * 为此，在连续分片一次迹空间 $W_h^1(\Gamma_N)$ 上对 $\bar{\boldsymbol t}_l$ 作 $L^2$ 投影求得连续牵引函数 $\boldsymbol t_h$，严格保持合力守恒 $\int_{\Gamma_N}\boldsymbol t_h\,\mathrm ds = \boldsymbol P$ 与一阶力矩守恒；
  * **两法统一施加**：位移法通过 Neumann 弱积分 $\int_{\Gamma_N} \boldsymbol t_h \cdot \boldsymbol v_h\,\mathrm ds$ 施加，胡张混合法通过应力法向迹 $(\boldsymbol\sigma_h \boldsymbol n)|_{\Gamma_N} = \boldsymbol t_h$ 强插值施加，彻底消除载荷形式引入的人为误差。

#### 2.4.3 体积力（Body Force）的处理

对于域内分布的体积力 $\boldsymbol b(\boldsymbol x) \in [L_2(\Omega)]^d$，位移法与胡张混合法均通过与位移检验函数的分片内积 $\int_\Omega \boldsymbol b \cdot \boldsymbol v_h\,\mathrm dx$ 进入系统方程，两法处理方式完全一致。

> **来源与边界**：集中力分布化与轴承均布载荷的设置参考 xtu-phd-thesis:thesis/brightPhD.pdf#第5.6.1节 与 5.6.3 节。本文只维护数学原理与适用边界，不把某次运行的数值结论写为稳定知识。程序分层、配置键与运行验收量由 soptx:docs/fem/huzhang-mixed-fem-implementation.md 维护。

---

## 3. 有限元空间与离散 inf-sup

### 3.1 应力空间 $\Sigma_h$

$\Sigma_h\subset H(\mathrm{div};\mathbb S)$：对称张量值、法向迹跨单元连续，次数 $k$。
Hu–Zhang 用 subsimplex（顶点/边/单元面/单元体）上的多指标构造 Bubble 丰富基底，对称性通过对称指标展开为独立分量。

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

> **来源**：本节第 1 条的两单元限制、第 4 条的自由度归属，均按 SOPTX `src/soptx/fem/spaces/huzhang_fe_space_2d.py`（`_get_corner_data`、`node_to_internal_dof`、`cell_to_dof`）于 2026-08-07 核对。[[../../papers/arbitrary-order-huzhang-topopt-draft-zh]] §3.4 与 §4.4 已同步为同一算法。

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

$\gamma_0$ 的取值敏感性通过网格与材料参数消融考察，见 [[../../papers/arbitrary-order-huzhang-topopt-draft-zh]] §3.3。

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

## 5. 收敛性结果（论文第五章对照）

> **证据边界**：本节数值来自博士论文第五章，属历史结论，只用于恢复问题定义与预期阶次，**不作为 CICP 投稿证据**。投稿证据须由新的实验入口重算，口径见 [[../../papers/arbitrary-order-huzhang-topopt-outline]] §四。

数值验证设置：单位正方形域、平面应变、$\lambda=1$、$\mu=0.5$、光滑制造解（精确位移 $u_1=u_2=\sin\pi x\sin\pi y$），$\Gamma_D=\{x=0\}\cup\{y=0\}$ 施加齐次位移、$\Gamma_N=\{x=1\}\cup\{y=1\}$ 施加精确牵引。
制造解完整定义见 SOPTX 制造解文档。

**高阶 $k\ge3$（无稳定化）**：

- 应力 $L^2$ 误差达到 $\mathcal O(h^{k+1})$ 的理论最优超收敛；对比同阶位移元（$P_{k-1}$ 位移）因形函数求导应力降至 $\mathcal O(h^{k-1})$，胡张元在应力场刻画上优势显著；
- 位移 $L^2$ 误差与应力 $H(\mathrm{div})$ 误差均为 $\mathcal O(h^{k})$ 最优收敛；$H(\mathrm{div})$ 误差由应力 $L^2$ 逼近与散度误差共同主导，其收敛证实法向牵引力跨单元连续。

**低阶 $k=1,2$（稳定化）**，论文表 5.2（SOPTX 逐格复现，见其 `results_analysis.md`）：

| $k$ | $\|\boldsymbol u-\boldsymbol u_h\|_{0}$ | $\|\boldsymbol\sigma-\boldsymbol\sigma_h\|_{0}$ | $\|\boldsymbol\sigma-\boldsymbol\sigma_h\|_{H(\mathrm{div})}$ |
|---|---|---|---|
| 1 | 1（最优） | 1.5 | 1（最优） |
| 2 | 2 | 2 | 1（**降阶**） |

- $k=1$：位移 $L^2$ 与应力 $H(\mathrm{div})$ 均严格达到 1 阶最优，消除低阶单元的自锁与数值震荡；
- $k=2$：位移、应力 $L^2$ 保持 2 阶，应力 $H(\mathrm{div})$ 向 1 阶退化。归因：混合边界下稳定化不施加于 $\Gamma_N$（§4.3），局部稳定化减弱叠加非多项式牵引在 $\Gamma_N$ 上的投影误差，主导并降低散度逼近精度——与纯位移边界下 Chen 等（稳定化混合元）的 2 阶最优不同。

**阶次下限：静力可用 $\ne$ 拓扑优化可用**。上表容易被读成"$k=1$ 已经够用"，但论文第五章的算例把 $k=1$ 排除在外，理由不在收敛阶而在 §3.2 的 RM 完备性。三层结论必须分开陈述：

| 层次 | $k=1$ | 依据 |
|---|---|---|
| 离散 inf-sup 稳定性 | 裸格式不满足，**跳量稳定化可恢复** | §3.3、§4 |
| 静力收敛性 | **可用**，位移 $L^2$ 与应力 $H(\mathrm{div})$ 均达 1 阶最优 | 本节上表 |
| 变密度拓扑优化 | **不可用** | §3.2 RM 不完备 |

机理：$P_0$ 位移无法表征单元局部微小转动，低密度区域的局部应变能评估严重失真，使演化过度依赖人工界面惩罚，进而诱发数值震荡与非物理拓扑。
因此稳定化格式在拓扑优化中的下限取 $k=2$（$P_1$ 位移已完备含 RM，提供稳健的底层物理驱动），$k=3,4$ 用于考察高阶原生（无惩罚）格式。这是 SOPTX 侧 `comparison_orders = 2,3,4` 白名单的唯一实质依据——它与迹空间可表示性无关：$\Sigma_h$ 的法向迹是跨边连续的 $k$ 次多项式，连续 $P_1$ 迹载荷（§2.5.3）对任意 $k\ge1$ 都可精确表示。

---

## 6. 来源与证据

本页根据博士论文第五章重新组织，不复制论文正文。原始事实源为：

- `xtu-phd-thesis:thesis/brightPhD.pdf#第五章` — Hu–Zhang 元构造、混合弱形式与鞍点结构
- `xtu-phd-thesis:thesis/brightPhD.pdf#表5.2` — 带稳定化的收敛阶对照
- `xtu-phd-thesis:thesis/brightPhD.pdf#第5.4.2-5.4.3节` — 矩阵型跳量惩罚、物理量纲缩放与 $H(\mathrm{div})$ 降阶归因
- `xtu-phd-thesis:thesis/brightPhD.pdf#第5.6.2节` — 两端固支梁算例排除 $k=1$ 的理由（$P_0$ 位移不完备包含 RM 空间）
- Hu & Zhang, arXiv:1406.7457 — 单纯形网格上弹性问题的共形混合有限元族（原始胡张元）
- Hu & Ma, *CMAM* 21(1) (2021), 89–108, doi:10.1515/cmam-2020-0003 — 弹性问题共形混合元应力顶点 $C^0$ 连续性的部分松弛
- Chen–Hu–Huang, *Math. Comp.* 87 (2018), Corollary 3.7(3.18) — $k\ge n+1$ 时应力超收敛

论文源码与定稿 PDF 由 `xtu-phd-thesis` 维护；本知识库只维护从中提炼的可复用理论。
本页不替代混合有限元专著或论文正文，也不把当前混合元推广到动力学、有限变形或非线性材料。

## 7. 关联实现与论文全链条地图

| 阶段 / 视图 | 路径 / 链接 | 职责与定位 |
|---|---|---|
| **理论概念 (Theory)** | [[huzhang-mixed-fem]] (本页) | 变分原理、鞍点结构、跳量稳定化缩放律、角点松弛理论 |
| **软件架构 (Architecture)** | `\\wsl.localhost\Ubuntu-24.04\home\brighthe\workspace\soptx\docs\fem\huzhang-mixed-fem-implementation.md` | `soptx.fem` 底层类图、`A/B/J` 组装器、FEALPy 4.0 兼容与测试套件 |
| **算例规范 (Math Spec)** | `\\wsl.localhost\Ubuntu-24.04\home\brighthe\workspace\soptx\examples\huzhang_elasticity\math_spec.md` | 符号-代码 1 对 1 映射、鞍点结构代数描述、双验收标准 |
| **实测数据 (Results)** | `\\wsl.localhost\Ubuntu-24.04\home\brighthe\workspace\soptx\examples\huzhang_elasticity\results_analysis.md` | 收敛误差实测数据、观测阶、相对残差与诊断分析报告 |
| **投稿大纲 (Outline)** | [[../../papers/arbitrary-order-huzhang-topopt-outline]] | 投稿目标 CICP 规格、7 个 Case 证据矩阵、投稿门禁规划 |
| **中文初稿 (Draft)** | [[../../papers/arbitrary-order-huzhang-topopt-draft-zh]] | 论文中文初稿全文（包含第 6.1 节高低阶前向收敛双表） |

## 相关页面

- [[_index]] — 概念页总索引。
- [[../linear-elasticity]] — 位移型线弹性基础（本页的出发问题）。
- [[../../literature/topology-opt/notes/Huang2022-problemindependentmachine]] — modified SIMP 材料插值，与胡张元应力场的物理可解释性相关。
