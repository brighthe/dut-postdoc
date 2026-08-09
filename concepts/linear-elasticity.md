---
title: "线弹性方程、变分形式与有限元离散"
type: concept
aliases:
  - Linear Elasticity Foundation
  - 线弹性有限元基础
  - 位移型线弹性
tags:
  - linear-elasticity
  - finite-element
  - variational-form
status: in-progress
date_added: 2026-07-29
date_update: 2026-08-01
---

# 线弹性方程、变分形式与有限元离散

> **一句话**：小变形静力线弹性从平衡方程和 Hooke 定律出发，经弱形式与向量 Lagrange 有限元离散得到 $\mathbf K\mathbf U=\mathbf F$，为结构分析及后续线性求解方法提供统一的连续模型和离散算子基础。

本页整理位移型、小变形、静力、各向同性线弹性的最小有限元理论闭环：

$$
\begin{aligned}
\boldsymbol u
&\longrightarrow
\boldsymbol\varepsilon(\boldsymbol u)
\longrightarrow
\boldsymbol\sigma(\boldsymbol u)
\longrightarrow
\text{强形式与边界条件},\\
\text{强形式}
&\longrightarrow
a(\boldsymbol u,\boldsymbol v)=\ell(\boldsymbol v)
\longrightarrow
(\mathbf K_e,\mathbf f_e)
\longrightarrow
\mathbf K\mathbf U=\mathbf F.
\end{aligned}
$$

本页采用**位移型、小变形、静力、各向同性线弹性**。均匀材料是基础情形；为连接拓扑优化，§2.3 和 §6 只补充设计相对密度如何参数化本构与离散刚度。动力学、有限变形、非线性材料、应力—位移混合元，以及拓扑优化中的目标函数、约束、灵敏度、滤波、投影和优化更新不属于本页范围。

## 1. 模型假设与几何

设 $\Omega\subset\mathbb R^d$（$d=2$ 或 $3$）为有界弹性体，$\Gamma_D$ 和 $\Gamma_N$ 是边界上互不相交的相对开集，并满足

$$
\partial\Omega
=
\overline{\Gamma_D}\cup\overline{\Gamma_N},
\qquad
\Gamma_D\cap\Gamma_N=\varnothing.
\tag{1}
$$

两者的闭包可以在测度为零的界面处相交。$\Gamma_D$ 上施加位移边界条件，$\Gamma_N$ 上施加表面力边界条件。基本未知量为位移场

$$
\boldsymbol u:\Omega\to\mathbb R^d.
\tag{2}
$$

本页采用以下假设：

- 位移和转动足够小，可以在线性化后的参考构形上计算应变；
- 忽略惯性和时间效应，只考虑静力平衡；
- 基础模型中的材料为线性、均匀、各向同性弹性体；密度参数化扩展允许弹性参数随空间和设计变量变化，但每个材料点仍满足线性各向同性本构；
- Cauchy 应力张量对称，不考虑体偶力；
- $\Gamma_D$ 具有足够的测度以排除刚体模态。

最后一条是位移型问题唯一性的重要条件。若采用纯 Neumann 边界，解只在刚体运动意义下唯一，还必须满足外载荷的整体平衡兼容条件。

## 2. 应变、本构与材料参数

### 2.1 小应变张量

小变形假设下，位移对应的线性化应变为

$$
\boldsymbol\varepsilon(\boldsymbol u)
=
\frac12\left(
\nabla\boldsymbol u+\nabla\boldsymbol u^{\mathsf T}
\right).
\tag{3}
$$

它只保留位移梯度的对称部分；反对称部分描述无穷小刚体转动，不产生弹性应变能。

### 2.2 各向同性 Hooke 定律

一般线弹性本构可以写成

$$
\boldsymbol\sigma(\boldsymbol u)
=
\mathbb C:\boldsymbol\varepsilon(\boldsymbol u),
\tag{4}
$$

其中 $\mathbb C$ 为四阶弹性张量。对各向同性材料，

$$
\boldsymbol\sigma(\boldsymbol u)
=
2\mu\boldsymbol\varepsilon(\boldsymbol u)
+
\lambda\operatorname{tr}\!\left(
\boldsymbol\varepsilon(\boldsymbol u)
\right)\boldsymbol I
=
2\mu\boldsymbol\varepsilon(\boldsymbol u)
+
\lambda\operatorname{div}(\boldsymbol u)\boldsymbol I.
\tag{5}
$$

$\lambda$ 和 $\mu$ 为 Lamé 常数，其中 $\mu$ 也是剪切模量。以 Young 模量 $E$ 和 Poisson 比 $\nu$ 表示时，三维各向同性材料满足

$$
\lambda
=
\frac{E\nu}{(1+\nu)(1-2\nu)},
\qquad
\mu
=
\frac{E}{2(1+\nu)}.
\tag{6}
$$

三维应变能正定要求

$$
\mu>0,
\qquad
\lambda+\frac{2}{3}\mu>0,
\tag{7}
$$

等价于体积模量为正。用 $(E,\nu)$ 参数化时，通常写为 $E>0$ 且 $-1<\nu<1/2$。

二维平面应变和平面应力会得到不同的降维本构矩阵。本页以三维本构为主，不展开二维矩阵。

### 2.3 非均匀材料与拓扑优化设计密度

这里必须区分两种含义不同的“密度”：

- **质量密度** $\rho_{\mathrm m}$ 具有质量/体积量纲，进入惯性项；在静力自重问题中还可通过 $\boldsymbol b=\rho_{\mathrm m}\boldsymbol g_0$ 进入体力；
- **设计相对密度** $\rho\in[0,1]$ 是拓扑优化中的无量纲材料变量，用来参数化局部弹性性质。它不是质量密度本身，也不会在没有材料插值模型时自动改变刚度。

对空间非均匀或由设计变量控制的线弹性材料，可将式 (4) 中的本构张量及其 Voigt 矩阵写为

$$
\mathbb C
=
\mathbb C\!\left(\boldsymbol x,\rho(\boldsymbol x)\right),
\qquad
\mathbf D
=
\mathbf D\!\left(\boldsymbol x,\rho(\boldsymbol x)\right).
\tag{8}
$$

若实体基准材料在空间上均匀，且只让 Young 模量随设计相对密度变化而保持 Poisson 比 $\nu$ 不变，则常用的 modified SIMP 插值写为

$$
E(\rho)
=
E_{\min}+\rho^p(E_0-E_{\min}),
\qquad
\mathbf D(\rho)
=
\frac{E(\rho)}{E_0}\mathbf D_0.
\tag{9}
$$

其中 $E_0$ 和 $\mathbf D_0$ 表示实体材料的 Young 模量和本构矩阵，$E_{\min}>0$ 是避免空域单元导致全局刚度奇异的弱材料下限。$p>1$ 用于惩罚中间密度、推动设计趋向 $0$–$1$ 分布；$p=3$ 是常见设置，但不是线弹性或 SIMP 的普遍定律。式 (9) 的比例关系依赖于基准材料均匀且 $\nu$ 固定；若基准材料本身随空间变化，应相应使用 $E_0(\boldsymbol x)$ 和 $\mathbf D_0(\boldsymbol x)$；若同时插值 Poisson 比或采用其他材料模型，则应由相应材料参数重新构造 $\mathbb C(\boldsymbol x,\rho)$ 或 $\mathbf D(\boldsymbol x,\rho)$。

## 3. 强形式

设 $\boldsymbol b$ 为单位体积体力，$\boldsymbol g$ 为 $\Gamma_N$ 上给定的面力，$\boldsymbol u_D$ 为 $\Gamma_D$ 上给定的位移。静力线弹性边值问题为：求 $\boldsymbol u$，使

$$
\begin{aligned}
-\operatorname{div}\boldsymbol\sigma(\boldsymbol u)
&=\boldsymbol b
&&\text{in }\Omega,\\
\boldsymbol u
&=\boldsymbol u_D
&&\text{on }\Gamma_D,\\
\boldsymbol\sigma(\boldsymbol u)\boldsymbol n
&=\boldsymbol g
&&\text{on }\Gamma_N,
\end{aligned}
\tag{10}
$$

其中 $\boldsymbol n$ 为边界单位外法向量。第一式表达局部线动量平衡，第三式中的 $\boldsymbol\sigma\boldsymbol n$ 是边界牵引力。

## 4. 弱形式与最小势能

定义满足位移边界条件的试探空间和对应的齐次测试空间

$$
\begin{aligned}
\boldsymbol V_D
&=
\left\{
\boldsymbol v\in[H^1(\Omega)]^d:
\boldsymbol v=\boldsymbol u_D\ \text{on }\Gamma_D
\right\},\\
\boldsymbol V_0
&=
\left\{
\boldsymbol v\in[H^1(\Omega)]^d:
\boldsymbol v=\boldsymbol 0\ \text{on }\Gamma_D
\right\}.
\end{aligned}
\tag{11}
$$

将平衡方程与任意 $\boldsymbol v\in\boldsymbol V_0$ 作内积并应用 Green 公式，利用 $\boldsymbol v|_{\Gamma_D}=0$、自然边界条件和应力对称性，有

$$
\int_\Omega
\boldsymbol\sigma(\boldsymbol u):
\boldsymbol\varepsilon(\boldsymbol v)\,\mathrm dx
=
\int_\Omega
\boldsymbol b\cdot\boldsymbol v\,\mathrm dx
+
\int_{\Gamma_N}
\boldsymbol g\cdot\boldsymbol v\,\mathrm ds.
\tag{12}
$$

定义

$$
\begin{aligned}
a(\boldsymbol u,\boldsymbol v)
&=
\int_\Omega
\boldsymbol\sigma(\boldsymbol u):
\boldsymbol\varepsilon(\boldsymbol v)\,\mathrm dx,\\
\ell(\boldsymbol v)
&=
\int_\Omega
\boldsymbol b\cdot\boldsymbol v\,\mathrm dx
+
\int_{\Gamma_N}
\boldsymbol g\cdot\boldsymbol v\,\mathrm ds,
\end{aligned}
\tag{13}
$$

则弱形式为

$$
\text{求 }\boldsymbol u\in\boldsymbol V_D,
\qquad
a(\boldsymbol u,\boldsymbol v)=\ell(\boldsymbol v)
\quad
\forall\boldsymbol v\in\boldsymbol V_0.
\tag{14}
$$

各向同性本构下，

$$
a(\boldsymbol u,\boldsymbol v)
=
\int_\Omega
\left[
2\mu\,
\boldsymbol\varepsilon(\boldsymbol u):
\boldsymbol\varepsilon(\boldsymbol v)
+
\lambda\,
\operatorname{div}(\boldsymbol u)
\operatorname{div}(\boldsymbol v)
\right]\mathrm dx.
\tag{15}
$$

在材料正定、载荷连续且 $\Gamma_D$ 足以消除刚体模态时：

- Korn 不等式用对称梯度控制 $[H^1]^d$ 范数；
- $a(\cdot,\cdot)$ 在 $\boldsymbol V_0$ 上连续且强制；
- Lax–Milgram 定理给出弱解的存在唯一性。

系统总势能为

$$
\Pi(\boldsymbol v)
=
\frac12a(\boldsymbol v,\boldsymbol v)-\ell(\boldsymbol v).
\tag{16}
$$

弱解也可以表述为 $\boldsymbol V_D$ 上的总势能极小点。在材料正定且 Dirichlet 约束足以排除刚体模态时，离散刚度矩阵在消除受约束自由度后对称正定，因此可以采用共轭梯度法求解。

## 5. 向量 Lagrange 有限元离散

令 $\mathcal T_h$ 为 $\Omega$ 的相容网格，标量连续 Lagrange 空间记为 $S_h^p\subset H^1(\Omega)$。位移空间是其 $d$ 维向量扩展：

$$
\boldsymbol V_h=[S_h^p]^d,
\qquad
\boldsymbol V_{h,0}=\boldsymbol V_h\cap\boldsymbol V_0,
\qquad
\boldsymbol V_{h,D}
=
\left\{
\boldsymbol v_h\in\boldsymbol V_h:
\boldsymbol v_h=I_h\boldsymbol u_D\ \text{on }\Gamma_D
\right\},
\tag{17}
$$

$I_h\boldsymbol u_D$ 表示与离散边界自由度一致的插值或投影；当 $\boldsymbol u_D=\boldsymbol 0$ 时，它退化为齐次边界空间。

Galerkin 离散为

$$
\text{求 }\boldsymbol u_h\in\boldsymbol V_{h,D},
\qquad
a(\boldsymbol u_h,\boldsymbol v_h)=\ell(\boldsymbol v_h)
\quad
\forall\boldsymbol v_h\in\boldsymbol V_{h,0}.
\tag{18}
$$

若 $\{\boldsymbol\phi_I\}_{I=1}^{N}$ 为全局矢量基函数，则

$$
\boldsymbol u_h
=
\sum_{I=1}^{N}U_I\boldsymbol\phi_I,
\qquad
\mathbf U=(U_1,\ldots,U_N)^{\mathsf T}.
\tag{19}
$$

对每个单元 $e$，用布尔限制矩阵 $\mathbf G_e$ 从全局自由度提取单元自由度：

$$
\mathbf U_e=\mathbf G_e\mathbf U.
\tag{20}
$$

## 6. Voigt 记号、应变矩阵与单元算子

三维工程应变和应力向量可记为

$$
\widehat{\boldsymbol\varepsilon}
=
\begin{bmatrix}
\varepsilon_{xx}&
\varepsilon_{yy}&
\varepsilon_{zz}&
2\varepsilon_{xy}&
2\varepsilon_{xz}&
2\varepsilon_{yz}
\end{bmatrix}^{\mathsf T},
\qquad
\widehat{\boldsymbol\sigma}
=
\begin{bmatrix}
\sigma_{xx}&
\sigma_{yy}&
\sigma_{zz}&
\sigma_{xy}&
\sigma_{xz}&
\sigma_{yz}
\end{bmatrix}^{\mathsf T}.
\tag{21}
$$

各向同性三维本构矩阵为

$$
\mathbf D
=
\begin{bmatrix}
2\mu+\lambda&\lambda&\lambda&0&0&0\\
\lambda&2\mu+\lambda&\lambda&0&0&0\\
\lambda&\lambda&2\mu+\lambda&0&0&0\\
0&0&0&\mu&0&0\\
0&0&0&0&\mu&0\\
0&0&0&0&0&\mu
\end{bmatrix},
\qquad
\widehat{\boldsymbol\sigma}
=
\mathbf D\widehat{\boldsymbol\varepsilon}.
\tag{22}
$$

设 $\mathbf N_e(\boldsymbol x)$ 为单元矢量形函数矩阵，$\mathbf B_e(\boldsymbol x)$ 为其对称梯度按式 (21) 排列得到的应变—位移矩阵，则

$$
\boldsymbol u_h|_{\Omega_e}
=
\mathbf N_e\mathbf U_e,
\qquad
\widehat{\boldsymbol\varepsilon}(\boldsymbol u_h)
=
\mathbf B_e\mathbf U_e.
\tag{23}
$$

单元刚度矩阵和单元载荷向量为

$$
\begin{aligned}
\mathbf K_e
&=
\int_{\Omega_e}
\mathbf B_e^{\mathsf T}
\mathbf D
\mathbf B_e\,\mathrm dx,\\
\mathbf f_e
&=
\int_{\Omega_e}
\mathbf N_e^{\mathsf T}\boldsymbol b\,\mathrm dx
+
\int_{\Gamma_N\cap\partial\Omega_e}
\mathbf N_e^{\mathsf T}\boldsymbol g\,\mathrm ds.
\end{aligned}
\tag{24}
$$

经数值积分，第一式可以写为

$$
\mathbf K_e
\approx
\sum_{q=1}^{N_q}
w_{eq}\,
\mathbf B_{eq}^{\mathsf T}
\mathbf D_{eq}
\mathbf B_{eq},
\tag{25}
$$

其中 $w_{eq}$ 吸收参考积分权重和几何 Jacobian。若材料均匀，$\mathbf D_{eq}$ 在积分点间相同；非均匀材料或拓扑优化中则可能随 $e,q$ 变化。

若单元 $e$ 内采用常值设计密度 $\rho_e$，且 Poisson 比固定，则可先计算实体材料单元刚度

$$
\mathbf K_e^0
=
\int_{\Omega_e}
\mathbf B_e^{\mathsf T}
\mathbf D_0
\mathbf B_e\,\mathrm dx.
\tag{26}
$$

再按材料插值缩放：

$$
\mathbf K_e(\rho_e)
=
\frac{E(\rho_e)}{E_0}\mathbf K_e^0.
\tag{27}
$$

若设计密度定义在节点上，或需要在积分点处评价连续密度场，则应在数值积分内部使用 $\rho_{eq}$：

$$
\mathbf K_e(\rho)
\approx
\sum_{q=1}^{N_q}
w_{eq}\,
\mathbf B_{eq}^{\mathsf T}
\mathbf D(\rho_{eq})
\mathbf B_{eq}.
\tag{28}
$$

全局代数系统为

$$
\mathbf K\mathbf U=\mathbf F,
\qquad
\mathbf K
=
\sum_e
\mathbf G_e^{\mathsf T}
\mathbf K_e
\mathbf G_e,
\qquad
\mathbf F
=
\sum_e
\mathbf G_e^{\mathsf T}\mathbf f_e.
\tag{29}
$$

密度参数化后，相同的组装关系写成

$$
\mathbf K(\rho)\mathbf U=\mathbf F,
\qquad
\mathbf K(\rho)
=
\sum_e
\mathbf G_e^{\mathsf T}
\mathbf K_e(\rho)
\mathbf G_e.
\tag{30}
$$

对任意固定的 $\rho$，该平衡问题仍然关于位移 $\mathbf U$ 线性；拓扑优化迭代中的非线性耦合来自 $\mathbf K$ 随 $\rho$ 改变。在通常的固定外载荷模型中，$\mathbf F$ 与 $\rho$ 无关；若考虑自重等设计相关体力，则应相应写成 $\mathbf F(\rho)$。

上述系统还需按选定策略施加 Dirichlet 约束。只要采用相同空间、积分、本构、载荷、边界和自由度编号，显式矩阵与隐式算子就表示同一个离散映射。

## 7. 来源与证据

本页根据博士论文第三章重新组织，不复制论文正文。原始事实源为：

- `xtu-phd-thesis:thesis/brightPhD.pdf#第三章`
- `xtu-phd-thesis:thesis/body/chapter03/chapter03.tex#线弹性问题的连续模型与变分形式`
- `xtu-phd-thesis:thesis/body/chapter03/chapter03.tex#线弹性问题的任意次多单元族拉格朗日有限元方法`
- [[../literature/topology-opt/notes/Huang2022-problemindependentmachine]] — modified SIMP 材料插值及局部材料分布进入有限元分析的文献依据。

论文源码与定稿 PDF 由 `xtu-phd-thesis` 维护；本知识库只维护从中提炼的可复用理论。本页不替代连续介质力学或有限元专著，也不把当前位移型模型推广为混合元、非线性弹性或动力学。

## 相关页面

- [[_index]] — 概念页总索引。
- [[matrix-free/_index]] — Matrix-Free 稳定知识与当前研究的主题入口。
- [[matrix-free/assembly-levels]] — FA/LA/EA/PA/UA 的存储和作用层次。
- [[gpu-hpc/distributed-operator-and-shared-dofs]] — MPI 分区、共享自由度、归约和 Krylov 内积。
- [[piml/mathematical-foundations]] — 从局部材料密度到多尺度形函数或缩聚刚度的 Problem-Independent PIML 映射。
- [[../research/technical-lines/matrix-free-research-guide]] — Matrix-Free 长期目标、阶段模型与统一验收原则。
- [[../research/technical-lines/matrix-free-research-guide#五、阶段门禁与当前执行状态]] — 当前线弹性 Matrix-Free 任务状态与推进顺序。
