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
date_update: 2026-08-07
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

### 2.4 边界条件语义（与位移型元相反）

| 边界 | 数学 | 离散方式 |
|---|---|---|
| 位移边界 $\Gamma_D:\ \boldsymbol u=\bar{\boldsymbol u}$ | **自然**边界 | 弱加进应力方程右端项 (2) |
| 牵引边界 $\Gamma_N:\ \boldsymbol\sigma\cdot\boldsymbol n=\boldsymbol t$ | **本质**边界 | 强加在应力自由度上（置行/置值法修改矩阵与右端） |

与 [[../linear-elasticity]] §5 的位移型元相反：那里 $\Gamma_D$ 本质、$\Gamma_N$ 自然。

**非齐次牵引的两种实现**。作为本质边界条件，$\Gamma_N$ 上的非齐次牵引有两种落地方式：

1. **消元法**：对已知的边界应力自由度置行置值，把它们从未知量中消去；
2. **牵引提升（lifting）**：取设计无关的 $\boldsymbol\sigma_g$ 满足 $\boldsymbol\sigma_g\boldsymbol n=\boldsymbol t$ on $\Gamma_N$，令 $\boldsymbol\sigma=\boldsymbol\sigma_0+\boldsymbol\sigma_g$ 且 $\boldsymbol\sigma_0$ 满足齐次牵引条件，右端相应出现 $-a(\boldsymbol\sigma_g,\boldsymbol\tau)$ 与 $-b(\boldsymbol\sigma_g,\boldsymbol v)$ 两项。

两者对**前向求解**等价。但当柔度张量依赖设计密度时，$-a_\rho(\boldsymbol\sigma_g,\boldsymbol\tau)$ 仍随密度变化，且目标泛函与灵敏度必须对**总应力** $\boldsymbol\sigma_0+\boldsymbol\sigma_g$ 求导；若沿用消元法而不显式区分齐次未知部分与给定提升，容易在灵敏度中遗漏提升的交叉项。因此密度法拓扑优化中应采用 lifting 表述，见 [[../../papers/arbitrary-order-huzhang-topopt-draft-zh]] §2.3 与 §4.5。

---

## 3. 有限元空间与离散 inf-sup

### 3.1 应力空间 $\Sigma_h$

$\Sigma_h\subset H(\mathrm{div};\mathbb S)$：对称张量值、法向迹跨单元连续，次数 $k$。
Hu–Zhang 用 subsimplex（顶点/边/单元面/单元体）上的多指标构造 Bubble 丰富基底，对称性通过对称指标展开为独立分量。

### 3.2 位移空间 $V_h$

分片不连续 Lagrange $P_{k-1}$，张量值（维度 $=d$），跨单元无连续性要求。

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

---

## 6. 来源与证据

本页根据博士论文第五章重新组织，不复制论文正文。原始事实源为：

- `xtu-phd-thesis:thesis/brightPhD.pdf#第五章` — Hu–Zhang 元构造、混合弱形式与鞍点结构
- `xtu-phd-thesis:thesis/brightPhD.pdf#表5.2` — 带稳定化的收敛阶对照
- `xtu-phd-thesis:thesis/brightPhD.pdf#第5.4.2-5.4.3节` — 矩阵型跳量惩罚、物理量纲缩放与 $H(\mathrm{div})$ 降阶归因
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
