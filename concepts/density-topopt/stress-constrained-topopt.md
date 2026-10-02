---
title: "局部应力约束拓扑优化"
type: concept
aliases:
  - Stress-Constrained Topology Optimization
  - Stress Relaxation
  - Singular Optima
  - Stress Singularity
  - 应力约束拓扑优化
  - 应力松弛
  - 奇异最优解
  - 应力奇异性
tags:
  - topology-optimization
  - density-method
  - stress-constraint
  - relaxation
status: "draft"
date_added: 2026-09-02
date_update: 2026-09-16
---

# 局部应力约束拓扑优化

应力约束问题关注结构的局部强度：在减少材料用量或改善整体性能的同时，限制非孔洞区域的应力不超过许用值。

## 1. 应力与 von Mises 等效应力

在小变形线弹性框架下，给定设计域 $\Omega$、材料密度 $\rho\in\mathcal X$ 和运动学容许位移 $\boldsymbol u\in\mathcal V$，柯西应力由广义胡克定律给出：

$$
\boldsymbol\sigma(\boldsymbol u)(\boldsymbol x)
=\mathbb C(\rho(\boldsymbol x)):\boldsymbol\varepsilon(\boldsymbol u)(\boldsymbol x),
\qquad \boldsymbol x\in\Omega.
$$

其中 $\mathbb C(\rho)$ 为依赖密度的弹性刚度张量，$\boldsymbol\varepsilon(\boldsymbol u)$ 为线性应变张量。采用 Voigt 记号，von Mises 等效应力写为：

$$
\sigma^{\mathrm{vM}}(\boldsymbol u_\rho)(\boldsymbol x)
=\sqrt{\hat{\boldsymbol\sigma}(\boldsymbol u_\rho)(\boldsymbol x)^{\mathsf T}
\boldsymbol M\hat{\boldsymbol\sigma}(\boldsymbol u_\rho)(\boldsymbol x)}.
$$

三维 von Mises 分量表达式见 Holmberg 等 [8]。下列二次型矩阵是按所列 Voigt 分量顺序对该表达式的代数改写；二维矩阵由相应平面假设导出。

### 1.1 三维情形

$$
\hat{\boldsymbol\sigma}
=[\sigma_{xx},\sigma_{yy},\sigma_{zz},\tau_{xy},\tau_{yz},\tau_{zx}]^{\mathsf T},
\qquad
\boldsymbol M=
\begin{bmatrix}
1&-0.5&-0.5&0&0&0\\
-0.5&1&-0.5&0&0&0\\
-0.5&-0.5&1&0&0&0\\
0&0&0&3&0&0\\
0&0&0&0&3&0\\
0&0&0&0&0&3
\end{bmatrix}.
$$

### 1.2 二维平面应力

在平面应力假设下，$\sigma_{zz}=0$，取：

$$
\hat{\boldsymbol\sigma}=[\sigma_{xx},\sigma_{yy},\tau_{xy}]^{\mathsf T},
\qquad
\boldsymbol M=
\begin{bmatrix}
1&-0.5&0\\
-0.5&1&0\\
0&0&3
\end{bmatrix}.
$$

### 1.3 二维平面应变

在各向同性线弹性平面应变假设下，由三维胡克定律有：

$$
0=\varepsilon_{zz}=\frac{\sigma_{zz}-\nu(\sigma_{xx}+\sigma_{yy})}{E},
\qquad \sigma_{zz}=\nu(\sigma_{xx}+\sigma_{yy}),
\qquad \tau_{yz}=\tau_{zx}=0.
$$

将这些关系代入三维 von Mises 表达式并合并同类项，使用面内应力向量即可得到：

$$
\boldsymbol M=
\begin{bmatrix}
1-\nu+\nu^2&-(0.5+\nu-\nu^2)&0\\
-(0.5+\nu-\nu^2)&1-\nu+\nu^2&0\\
0&0&3
\end{bmatrix},
$$

其中 $\nu$ 为泊松比。平面应变下不能直接使用平面应力的权重矩阵。

## 2. 局部应力约束的连续模型

局部应力约束拓扑优化通过改变材料分布减少材料用量，同时要求结构满足弹性平衡与局部强度条件。其依赖关系为：密度决定刚度，刚度决定平衡位移，位移决定应变与应力。局部应力约束与变分平衡的连续统框架见 Giraldo-Londoño 和 Paulino [10]；以下以未松弛的实体应力约束为本页的基准模型，并明确所用的密度、载荷与孔洞处理假设。

### 2.1 设计域与容许密度

设 $\Omega\subset\mathbb R^d$（$d=2$ 或 $3$）为固定的有界 Lipschitz 设计域。本节用 $\rho(\boldsymbol x)\in[0,1]$ 表示进入本构、体积目标和应力约束的物理相对密度：$\rho=1$ 表示实体材料，$\rho=0$ 表示设计上的孔洞，$0<\rho<1$ 表示灰度材料。

给定互不相交的固定实体区 $\Omega_{\mathrm{keep}}$ 与固定孔洞区 $\Omega_{\mathrm{passive\text{-}void}}$，基本容许密度集合为

$$
\mathcal X_0=
\left\{\rho\in L^\infty(\Omega)\;\middle|\;
0\leq\rho\leq1\ \text{a.e. in }\Omega,\quad
\rho=1\ \text{a.e. in }\Omega_{\mathrm{keep}},\quad
\rho=0\ \text{a.e. in }\Omega_{\mathrm{passive\text{-}void}}
\right\}.
$$

没有固定区域时，对应集合取空集。实际采用的 $\mathcal X\subseteq\mathcal X_0$ 还可包含正则化或长度尺度要求；仅有上述取值约束，并不保证连续优化问题存在最优解。若采用过滤与投影，$\mathcal X$ 应限制为相应映射可生成的物理密度集合。本节的 $\rho$ 对应三场记号中的 $\overline\rho$，不与过滤前的原始设计变量混用，见 [[regularization-and-length-scale-control|正则化与长度尺度控制]]。

随设计变化的孔洞区域记为

$$
\Omega_{\mathrm{void}}(\rho)=\{\boldsymbol x\in\Omega\mid\rho(\boldsymbol x)=0\}.
$$

它包含固定孔洞区，也包含优化过程中形成的孔洞；上述集合及后续约束均按几乎处处的意义理解。

### 2.2 给定密度后的弹性状态问题

将外边界分为位移边界 $\Gamma_D$ 与牵引边界 $\Gamma_N$，两者互不相交且闭包覆盖 $\partial\Omega$。给定可作 $H^1$ 提升的位移数据 $\boldsymbol u_D$，定义

$$
\begin{aligned}
\mathcal V&=\{\boldsymbol u\in[H^1(\Omega)]^d:
\boldsymbol u=\boldsymbol u_D\ \text{on }\Gamma_D\},\\
\mathcal V_0&=\{\boldsymbol v\in[H^1(\Omega)]^d:
\boldsymbol v=\boldsymbol0\ \text{on }\Gamma_D\}.
\end{aligned}
$$

边界条件按迹的意义施加，并假定支承足以排除刚体运动。小变形应变为 $\boldsymbol\varepsilon(\boldsymbol u)=(\nabla\boldsymbol u+\nabla\boldsymbol u^{\mathsf T})/2$。密度相关的弹性双线性型为

$$
a_\rho(\boldsymbol u,\boldsymbol v)
=\int_\Omega
\boldsymbol\varepsilon(\boldsymbol v):\mathbb C(\rho):
\boldsymbol\varepsilon(\boldsymbol u)\,\mathrm dx.
$$

本节取设计无关的体力 $\boldsymbol b$ 与边界牵引 $\overline{\boldsymbol t}$，假定其定义的载荷泛函在 $\mathcal V_0$ 上有界：

$$
\ell(\boldsymbol v)
=\int_\Omega\boldsymbol b\cdot\boldsymbol v\,\mathrm dx
+\int_{\Gamma_N}\overline{\boldsymbol t}\cdot\boldsymbol v\,\mathrm ds.
$$

此处积分写法适用于具有相应可积性的载荷；一般情形使用对偶配对。自重等设计相关载荷须改写为 $\ell_\rho$，不属于此处的固定载荷假设。给定 $\rho$ 后，平衡位移 $\boldsymbol u_\rho\in\mathcal V$ 满足

$$
a_\rho(\boldsymbol u_\rho,\boldsymbol v)=\ell(\boldsymbol v),
\qquad\forall\boldsymbol v\in\mathcal V_0.
$$

本构与弱形式见 [[../linear-elasticity|线弹性方程]]，载荷空间及理想点力的限制见 [[../external-loads|外载荷与等效节点力]]。

固定域求解还需区分理想孔洞与残余刚度。若 $\mathbb C(0)=0$，孔洞区域不提供弹性能，以上双线性型在全域 $H^1$ 空间上可能失去强制性，不能直接断言位移解存在且唯一。严格的材料域模型需在实际承载区域上定义状态问题，并检查支承、连通性、自由边界及载荷是否与材料分布相容。

固定域计算通常采用 Ersatz 软材料，例如

$$
\mathbb C(\rho)=m(\rho)\mathbb C_0,\qquad
m(\rho)=m_{\min}+(1-m_{\min})\rho^p,
\qquad 0<m_{\min}<1,\quad p\geq1.
$$

其中 $\mathbb C_0$ 为实体材料刚度张量，$m_{\min}$ 为残余相对刚度。在 $\mathbb C_0$ 正定、支承满足上述条件且载荷有界时，正的刚度下限保证该固定域状态问题的强制性。此时 $\rho=0$ 区域在计算中仍是软材料，并非严格无刚度的孔洞；$m_{\min}$ 也不是密度下界。下述模型采用固定域上的软材料近似：零密度区域不计入材料体积，也不施加强度约束，但在平衡方程中仍保留残余刚度。因此，设计上的孔洞与计算中的零刚度区域并不等同。

### 2.3 应力度量与约束区域

在同一当前位移场下，实体应力与表观应力分别定义为

$$
\boldsymbol\sigma^{\mathrm{solid}}(\boldsymbol u_\rho)
=\mathbb C_0:\boldsymbol\varepsilon(\boldsymbol u_\rho),
\qquad
\boldsymbol\sigma^{\mathrm{app}}(\boldsymbol u_\rho,\rho)
=\mathbb C(\rho):\boldsymbol\varepsilon(\boldsymbol u_\rho).
$$

表观应力进入平衡方程；本页选择实体应力的 von Mises 等效值作为未松弛的强度约束对象。实体应力不是重新求解满密度结构得到的应力。两种应力在 $\rho=1$ 时一致，灰度区一般不同，其标量插值关系见 §3.2；§1 中由密度相关本构直接定义的应力属于表观应力。

给定与设计无关的应力评价区域 $\Omega_{\mathrm{eval}}\subseteq\Omega$，定义实际约束区域

$$
\Omega_{\mathrm s}(\rho)
=\Omega_{\mathrm{eval}}\cap\{\boldsymbol x\in\Omega:\rho(\boldsymbol x)>0\}.
$$

默认在所有非孔洞区域施加应力约束，即取 $\Omega_{\mathrm{eval}}=\Omega$。局部应力约束并不要求排除加载或支承邻域。在二维、三维经典线弹性实体模型中，非零理想点载荷及承担非零集中反力的点支承会引起应力奇异性；有限范围支承的端部或边界条件交接处也可能出现奇异性，但不能仅凭存在支承就断言应力无界，见 §5。

对于使所评价应力无界的理想化模型，可以修改载荷或支承模型以处理奇异源，也可以限制应力约束的评价范围；若保留奇异源，则不能要求其完整邻域满足有限、网格无关的局部应力上限。若选择不在特定邻域施加应力约束，应从 $\Omega_{\mathrm{eval}}$ 中排除相应的固定物理区域，并明确强度评价不覆盖该区域，见 §5.2。固定实体区仅规定密度为 $1$，是否施加应力约束需另行指定。

给定许用应力 $\bar\sigma>0$，未松弛约束为

$$
\frac{\sigma_{\mathrm{vm}}^{\mathrm{solid}}(\boldsymbol u_\rho)(\boldsymbol x)}{\bar\sigma}-1\leq0,
\qquad\text{a.e. }\boldsymbol x\in\Omega_{\mathrm s}(\rho).
$$

这里“局部”指评价区域内几乎处处满足要求，而非只限制某个全局平均值。一般 $H^1$ 位移仅给出 $L^2$ 应力，并不保证应力连续或有界，因此采用几乎处处的表述；它仍不允许应力在奇异点邻域的正测度区域内超过许用值。离散评价点上的满足不等于上述连续约束已得到保证。

在灰度区沿用实体材料许用值，是本页基准模型的选择，并非已知微结构强度的普遍定律。理想孔洞不承担材料强度要求；在 Ersatz 模型中排除 $\rho=0$ 区域，也不意味着该处计算应力严格为零。

### 2.4 局部应力约束下的最小体积问题

以上定义给出固定域上的基准问题：

$$
\begin{aligned}
\min_{\rho\in\mathcal X,\;\boldsymbol u\in\mathcal V}\quad
&V(\rho)=\int_\Omega\rho\,\mathrm dx,\\
\text{subject to}\quad
&a_\rho(\boldsymbol u,\boldsymbol v)=\ell(\boldsymbol v),
&&\forall\boldsymbol v\in\mathcal V_0,\\
&\frac{\sigma_{\mathrm{vm}}^{\mathrm{solid}}(\boldsymbol u)(\boldsymbol x)}{\bar\sigma}-1\leq0,
&&\text{a.e. }\boldsymbol x\in\Omega_{\mathrm s}(\rho).
\end{aligned}
$$

三维中 $V$ 为材料体积，二维中按单位厚度计；固定厚度 $t$ 下的实际体积为 $t\int_\Omega\rho\,\mathrm dx$。固定实体区的体积为常数，保留在目标中不改变最优设计。也可用 $V/|\Omega|$ 作为体积分数目标。

平衡方程将 $\boldsymbol u$ 限定为当前设计的状态解 $\boldsymbol u_\rho$，因此也可消去状态变量，将问题写为仅对 $\rho$ 优化、应力约束隐含依赖 $\boldsymbol u_\rho$ 的形式。若改用柔顺度等目标 $\mathcal J(\boldsymbol u_\rho,\rho)$，应同时明确是否另设体积上限等约束，不能仅更换目标名称就视为同一问题。

上述模型尚未放宽低密度区的强度要求：只要 $\rho>0$，就要求实体应力不超过许用值；当 $\rho=0$ 时，该要求撤去。这种随材料存在与否而变化的约束结构，是下一节讨论奇异最优解与松弛处理的起点。状态方程中的残余刚度与应力约束的松弛是两个不同的建模步骤。

## 3. 奇异最优解与松弛处理

本节的奇异性指材料消失时可行域退化，不以应力场无界为前提。应力场奇异性是另一种机制，见 §5；两者可以同时存在。

### 3.1 材料消失引起的约束奇异性

在变密度法中，当材料密度趋于零时，单元刚度随之减小，但由实体材料本构计算的应力未必趋于零。如果对所有正密度单元直接施加实体应力约束，某些低密度状态仍可能因应力超限而不可行；而在理想孔洞处，材料强度约束又不再适用。这种材料消失时约束条件的变化，使含孔洞的设计可能位于可行域的退化部分，常规梯度优化难以到达。松弛方法通过放宽低密度区域的应力限制，为材料逐步移除提供可行空间 [1,2]。

### 3.2 实体应力与表观应力

为区分后续松弛模型中的应力度量，先定义实体应力与表观应力，并说明二者在标量刚度插值下的关系。

本节采用标量刚度插值 $\mathbb C(\overline\rho)=m(\overline\rho)\mathbb C_0$，即密度仅改变刚度的整体大小，本构各分量之间的比例保持不变。令相对刚度 $m=E(\overline\rho)/E_0$，且 $0<m\leq1$。在此假设下，表观应力等于实体应力乘以 $m$：

$$
\boldsymbol\sigma^{\mathrm{solid}}=\mathbb C_0:\boldsymbol\varepsilon(\boldsymbol u),
\qquad \boldsymbol\sigma^{\mathrm{app}}=m\boldsymbol\sigma^{\mathrm{solid}},
\qquad \sigma_{\mathrm{vm}}^{\mathrm{app}}=m\sigma_{\mathrm{vm}}^{\mathrm{solid}}.
$$

最后一个等式利用 von Mises 应力的一次正齐次性。实体应力是用实体材料本构 $\mathbb C_0$ 作用于当前位移场的应变得到的应力；表观应力是用密度插值后的本构 $\mathbb C(\overline\rho)=m\mathbb C_0$ 作用于同一应变得到的应力，因此 $\boldsymbol\sigma^{\mathrm{app}}=m\boldsymbol\sigma^{\mathrm{solid}}$。两者均对应当前密度分布下的状态，实体应力不是另行求解满密度结构得到的应力。

### 3.3 松弛模型

承 §3.1，原问题的应力约束随材料有无而通断：$\rho_e>0$ 时要求 $\sigma_{\mathrm{vm},e}^{\mathrm{solid}}\leq\bar\sigma$，$\rho_e=0$ 时不施加约束。因此可行域中“某些单元密度为零”的部分是设计空间中的低维退化子集，没有内点，只经由降维的边界与其余部分相连；最优解若落在这类子集上，从可行域内部出发的下降路径无法到达。松弛把这一通断改为连续过渡——约束在低密度处逐渐变弱而不是突然消失——从而把该子集加厚为有内点的集合。

这样做改变了问题：可行域被放大，松弛问题的解一般不是原问题的解。最终 0–1 设计中实体单元的密度趋于 1，原问题的可行性由满密度端的约束决定。于是对松弛形式有两条要求：孔洞端放宽须足以使退化子集可达，满密度端的放宽须归零。$\varepsilon$ 松弛与应力惩罚都可写成 $\sigma_{\mathrm{vm}}^{\mathrm{app}}/\bar\sigma\leq T(\rho)$，差别集中在阈值函数 $T$；下表按这两条逐行对照，其中 $T/m$ 是等价的实体应力上限。

| 形式                       | $T(\rho)$                           | $\rho\to0$ 时的实体应力上限 $T/m$ | $T(1)$                   |
| ------------------------ | ----------------------------------- | ------------------------- | ------------------------ |
| 不松弛（原问题）                 | $\rho^{p}$                          | $1$（不放宽）                  | $1$                      |
| 经典 $\varepsilon$-松弛 [12] | $\rho^{p}\sqrt{1+\varepsilon/\rho}$ | $\to\infty$               | $\sqrt{1+\varepsilon}>1$ |
| $q$–$p$ 松弛 [3,4]         | $\rho^{q}$，$q<p$                    | $\to\infty$               | $1$                      |
| §3.3.1 的形式               | $m+\varepsilon(1-m)$                | $\to\infty$               | $1$                      |

取固定松弛量的经典形式满足第一条而不满足第二条，其在 $\rho=1$ 处的残留偏差须靠 $\varepsilon$ 延拓事后消去；令松弛量随密度变化并在 $\rho\to1$ 归零，两条可同时满足，$q$–$p$ 松弛与 §3.3.1 的形式属于这一类。孔洞端的阈值另须与刚度插值的下限相匹配（§3.3.2 末）。

加厚图景来自桁架问题的 $\varepsilon$ 松弛分析 [1,2]，连续体离散下通常作为设计依据而非已证结论；$T(1)=1$ 也只是阈值函数自身的性质，不等于原问题不存在奇异最优解。

以上三类按约束表达式的书写形态命名，不等同于机制划分：$\varepsilon$ 松弛与应力惩罚同属抬高阈值，$q$–$p$ 松弛可恒等改写为取自适应松弛量的 $\varepsilon$ 松弛（§3.3.2）。消失约束不属于 $\sigma_{\mathrm{vm}}^{\mathrm{app}}/\bar\sigma\leq T$ 的写法：密度因子乘在约束函数之外，正密度处的可行域并未放宽，不能仅凭这一因子断言退化子集已变得可达。以下各节在 §3.2 的标量刚度插值假设下给出各形式的定义与代数推导。

#### 3.3.1 $\varepsilon$ 松弛

$\varepsilon$ 松弛引入与密度相关的松弛项，在密度趋零时放宽应力限制，使孔洞端能够满足松弛后的条件 [2,12]。

松弛模型规定约束如何放宽，应力表示规定公式用哪一种应力变量表达。因此，$\varepsilon$ 松弛不限定必须使用表观应力。

本节讨论当前采用的一种具体形式。在 §3.2 的标量本构插值假设下，它可用实体应力比或表观应力比等价表达；这两种写法不是两个不同的松弛模型。取 $0\leq\varepsilon\leq1$，定义

$$
\eta(m)=m+\varepsilon(1-m),\qquad
g_\varepsilon=\frac{\sigma_{\mathrm{vm}}^{\mathrm{app}}}{\bar\sigma}-\eta(m)\leq0.
$$

在实体应力表示下，同一公式为 $g_\varepsilon=m\left(\frac{\sigma_{\mathrm{vm}}^{\mathrm{solid}}}{\bar\sigma}-1\right)-\varepsilon(1-m)$。对 $m>0$，可行条件等价于

$$
\frac{\sigma_{\mathrm{vm}}^{\mathrm{solid}}}{\bar\sigma}\leq1+\varepsilon\left(\frac1m-1\right).
$$

$m=1$ 时恢复 $\frac{\sigma_{\mathrm{vm}}^{\mathrm{solid}}}{\bar\sigma}\leq1$；固定 $m>0$ 并令 $\varepsilon\to0$ 时也恢复此条件。对 $\varepsilon>0$，低刚度处的实体应力上限随 $m$ 减小而放宽。形式上 $m\to0$ 时 $\eta\to\varepsilon$，但沿状态解序列仍须满足 $\frac{\sigma_{\mathrm{vm}}^{\mathrm{app}}}{\bar\sigma}\leq\eta$；不能仅凭密度趋零断言可行。若 $\frac{\sigma_{\mathrm{vm}}^{\mathrm{solid}}}{\bar\sigma}$ 有界，则 $\frac{\sigma_{\mathrm{vm}}^{\mathrm{app}}}{\bar\sigma}=m\frac{\sigma_{\mathrm{vm}}^{\mathrm{solid}}}{\bar\sigma}\to0$、$g_\varepsilon\to-\varepsilon$。

本节形式与经典平方形式 $\bigl(\sigma_{\mathrm{vm}}^{\mathrm{solid}}/\bar\sigma\bigr)^2\leq1+\varepsilon/\rho$ [12] 的差别在满密度端：后者在 $m=1$ 处仍留有 $O(\varepsilon)$ 松弛量，最优解依赖 $\varepsilon$ 的取值，因而通常需配合 $\varepsilon$ 延拓 [3]；本节形式的松弛量 $\varepsilon(1-m)$ 在 $m=1$ 处严格为零，最终 0–1 设计不携带松弛偏差，该性质与 $q$–$p$ 松弛一致（§3.3.2）。

#### 3.3.2 应力惩罚（$q$–$p$ 松弛）

应力惩罚通过密度插值改变应力限值随密度衰减的速率。$q$–$p$ 松弛取应力惩罚指数 $q$ 小于刚度惩罚指数 $p$，把未松弛的限值 $\rho^{p}\bar\sigma$ 改写为 $\rho^{q}\bar\sigma$ [3,4]：

$$
g_{qp}=\frac{\sigma_{\mathrm{vm}}^{\mathrm{app}}}{\bar\sigma}-\rho^{q}\leq0,\qquad q<p.
$$

该形式表面上不含松弛参数，但与 $\varepsilon$ 松弛同属抬高限值的机制。写成平方形式，$(\sigma_{\mathrm{vm}}^2-\rho^{2q}\bar\sigma^2)\rho\leq0$ 可恒等改写为

$$
(\sigma_{\mathrm{vm}}^2-\rho^{2p}\bar\sigma^2)\rho\leq(\rho^{2q}-\rho^{2p})\rho\bar\sigma^2,
$$

即取自适应松弛量 $\varepsilon(\rho)=(\rho^{2q}-\rho^{2p})\rho\bar\sigma^2$ 的 $\varepsilon$ 松弛 [3]。

该 $\varepsilon(\rho)$ 在 $\rho\to1$ 时归零，最终 0–1 设计不携带松弛偏差；取固定 $\varepsilon$ 的经典形式在 $\rho=1$ 处仍有残留松弛，这也是经典形式通常需要配合 $\varepsilon$ 延拓的理由之一 [3]。

与 §3.3.1 形式的差别在孔洞端：$q$–$p$ 松弛的限值 $\rho^{q}$ 随密度趋零，§3.3.1 的形式保留正下限 $\varepsilon$。在 msimp 插值下 $m\to E_{\min}/E_0>0$，孔洞单元的表观应力不严格为零；限值若无下界，则只要实体应力不为零，充分小的密度处必有 $m\,\sigma_{\mathrm{vm}}^{\mathrm{solid}}/\bar\sigma>\rho^{q}$ 而被判为违约。正下限 $\varepsilon$ 提供与 $E_{\min}$ 相匹配的容差。

#### 3.3.3 消失约束

消失约束在约束函数中引入密度因子，使约束在孔洞端自动消失 [1]。多项式消失约束进一步引入应力违约量的三次项，增强对较大违约量的惩罚 [5]。令 $s=\frac{\sigma_{\mathrm{vm}}^{\mathrm{solid}}}{\bar\sigma}-1$，定义

$$
g_{\mathrm v}=m(s^3+s)=m\,s(1+s^2)\leq0.
$$

对任意 $m>0$，因为 $1+s^2>0$，有 $g_{\mathrm v}\leq0\iff \frac{\sigma_{\mathrm{vm}}^{\mathrm{solid}}}{\bar\sigma}\leq1$。三次项改变约束尺度和梯度，不改变正刚度处的严格可行域。

“消失”指在独立且有限的 $\frac{\sigma_{\mathrm{vm}}^{\mathrm{solid}}}{\bar\sigma}$ 下令 $m=0$，约束函数为零；沿真实状态解的极限则要求 $m(s^3+s)\to0$，不能忽略应力随材料移除而增长的可能性。若保留 $m_{\min}>0$ 的残余刚度，计算中不存在严格的 $m=0$，零容差的约束仍要求 $\frac{\sigma_{\mathrm{vm}}^{\mathrm{solid}}}{\bar\sigma}\leq1$。

因此，多项式消失约束与取 $\varepsilon>0$ 的表观应力松弛具有不同可行域。采用相同 AL 算法并不使两者成为同一模型。


### 3.4 约束尺度与容差

结果评估须区分模型可行性与实体区强度：前者检查模型规定的全部局部约束及其容差，后者在明确定义的实体区域内报告应力峰值，并注明密度阈值与应力度量。低密度处的表观应力受本构插值影响，不能直接解释为实体材料强度；只报告实体区峰值也不能替代全部局部约束的验收。

松弛参数 $\varepsilon$ 定义模型，约束容差 $\epsilon_g$ 定义数值验收。由 $g_\varepsilon\leq\epsilon_g$ 得

$$
\frac{\sigma_{\mathrm{vm}}^{\mathrm{app}}}{\bar\sigma}\leq\eta+\epsilon_g,\qquad
\frac{\sigma_{\mathrm{vm}}^{\mathrm{app}}}{\eta\bar\sigma}-1\leq\frac{\epsilon_g}{\eta}\quad(\eta>0).
$$

固定绝对容差不等于相对局部阈值的固定精度。多项式模型的 $g_{\mathrm v}\leq\epsilon_g$ 则等价于 $s^3+s\leq\epsilon_g/m$，低刚度处也可能容许较大的实体应力超限。

还须区分多项式约束与加权应力指标 $r_{\mathrm w}=m\frac{\sigma_{\mathrm{vm}}^{\mathrm{solid}}}{\bar\sigma}-1$：前者严格可行蕴含 $r_{\mathrm w}\leq0$，反向不成立。例如 $m=0.1$、$\frac{\sigma_{\mathrm{vm}}^{\mathrm{solid}}}{\bar\sigma}=2$ 时，$r_{\mathrm w}=-0.8$，但 $g_{\mathrm v}=0.2>0$。展示应力、验收指标与优化约束应分别定义。

本节公式为上述定义的直接代数推导；松弛方法的文献背景沿用 [1,2,5]，不将本节具体公式直接等同于这些文献的全部模型。项目验收口径见 [[../../research/huzhang-topopt/stress-constraint-acceptance]]。

## 4. 大量局部约束的处理

有限元中通常在单元中心或积分点评价应力。网格细化会增加局部约束数量，进而增加灵敏度计算、存储与优化求解的负担。常用的处理策略包括：

| 策略                  | 基本处理                   | 主要权衡                         |
| ------------------- | ---------------------- | ---------------------------- |
| 有效集 [4]             | 选取违反约束或接近边界的评价点参与当前优化  | 保留局部条件，但有效集变化可能引起迭代振荡        |
| 聚合与聚类 [6–8]         | 用 P-范数或 KS 函数构造全局或分组约束 | 减少约束数量，需控制聚合近似与局部峰值之间的偏差     |
| 增广拉格朗日方法（ALM）[9,10] | 将逐点约束的乘子项和罚项纳入增广目标     | 保留局部约束结构，通过一系列子问题求解，不等同于约束聚合 |

全局聚合与分组聚类的差异在于约束分组范围。ALM 则通过改变求解形式处理大量局部约束，而不是将它们近似为少数聚合不等式。各局部约束的贡献合入标量增广目标后，可统一组织伴随灵敏度计算，避免为每条约束分别形成完整梯度；局部约束的评价及相应乘子的存储、更新仍然需要进行 [9,10]。

## 5. 应力奇异性

### 5.1 点载荷下的应力发散与可行域失效

由二维弹性力学经典解（半平面边界集中力的 Flamant 解或全平面 Kelvin 解），包围点载荷的截面周长正比于半径 $r$，截面内力与外力平衡 $\int_{\Gamma_r} \boldsymbol{\sigma}\boldsymbol{n}\,\mathrm ds = \boldsymbol P$ 决定了理想点载荷附近的连续应力严格具有 $r^{-1}$ 奇异性（相应三维截面积正比于 $r^2$，具有 $r^{-2}$ 奇异性）。在有限元离散中，局部网格尺度 $h$ 相当于数值截断半径（$r \sim h$），导致加载点邻域的应力峰值随网格细化呈 $O(h^{-1})$ 持续增大，不收敛到有限值；具体序列不保证单调，受网格、采样点与应力恢复方式影响。载荷数据的正则性判据与两套变分形式中的施加方式见 [[../external-loads#3.2 理想点力的连续空间限制|外载荷 §3.2]]。

| 优化中的量                           | 点载荷下的典型行为                       | 后果                                 |
| ------------------------------- | ------------------------------- | ---------------------------------- |
| 柔顺度 $\ell(\boldsymbol u_h)$     | 二维为 $O(\log(1/h))$ 发散           | 目标值随网格漂移；发散缓慢不保证优化拓扑具有网格无关性        |
| 加载点邻域的 $\sigma^{\mathrm{vM}}_h$ | 按 $r\sim h$ 取值，呈 $O(h^{-1})$ 增长 | 对有限许用应力，足够细的网格会出现超限，优化可能在加载点附近堆积材料 |

若约束评价区域包含理想点载荷邻域，任何有限的 $\bar\sigma$ 都无法约束其连续应力峰值。因此，要求有限、网格无关的局部应力上限时，不能直接沿用单个节点承受全部集中力的理想化。固定网格上的数值可行不代表连续模型可行；另一种有限范围的评价方式是不将指定的固定物理邻域纳入应力约束评价，见 §5.2。

将集中力改写为特征宽度 $l$ 上的静力等效分布牵引，可消除该点力奇异源。$l$ 由物理接触条件确定后固定，不随网格加密变化；分布化并不保证全域应力有界，还需检查载荷作用段端部、几何与支承条件，见 [[../external-loads#3.3 有限宽度分布化|外载荷 §3.3]]。

### 5.2 载荷分布化与应力约束评价范围

| 处理 | 做法 | 作用 |
|---|---|---|
| 载荷分布化 [8,10] | 点载荷换成有限边界段上静力等效的分布牵引 | 消除点载荷引起的 $r^{-1}$ 奇异，不保证消除其他奇异源 |
| 局部不施加应力约束并保留实体 [8,10] | 加载点邻域密度固定为 1，且不纳入应力约束评价 | 不消除点载荷奇异性，只把该邻域移出验收范围 |

不施加应力约束的区域应按固定物理尺寸定义，不随网格加密缩小。这些区域仍参与弹性平衡计算；其外的应力仍需检查收敛性。该评价不覆盖这些区域的强度，也不消除点载荷引起的柔顺度发散。

### 5.3 分布化不消除的奇异源

分布化只处理点载荷奇异源。角点附近还可能出现 $r^{\lambda-1}$ 型应力项，$\lambda$ 由开角、边界条件及材料参数对应的特征问题确定 [11]。当存在 $\operatorname{Re}\lambda<1$ 的奇异模态且其系数非零时，应力场可能无界；不能仅凭存在角点就断言实际载荷下必有应力发散。

| 潜在奇异源 | 位置 | 载荷分布化是否消除 |
|---|---|---|
| 集中力 | 加载点 | 消除该点力奇异源 |
| 位移—牵引混合边界角点 | $\Gamma_D$ 与 $\Gamma_N$ 的交点，如悬臂梁固支端的上下角 | 否，需单独分析边界条件与开角 |
| 凹角 | 开角大于 $\pi$ 的再入角，如 L 形支架内角 | 否，需单独分析局部几何与边界条件 |

§3 的奇异最优解不在本表范围：它描述可行域退化，不要求应力场无界。若上述奇异模态使所评价的 von Mises 应力无界，则离散峰值虽通常在每个固定网格上有限，却不能收敛到有限的连续峰值。

点力和尖锐凹角可分别理解为忽略了接触宽度和圆角半径；混合边界问题还涉及理想刚性支承及边界条件类型突变，不能统一归结为某个物理长度为零。加密网格不会自行消除连续模型中的奇异源。

| 潜在奇异源 | 需检查的模型理想化 | 可考虑的处理 | 适用条件 |
|---|---|---|---|
| 集中力 | 接触宽度为零 | 静力等效分布牵引 | $l$ 由接触条件确定，见 §5.2 |
| 混合边界角点 | 理想刚性支承与边界条件突变 | Robin 边界 $\boldsymbol\sigma\boldsymbol n+k\boldsymbol u=\boldsymbol 0$，或弹性支承垫 | 需物理支承刚度及作用范围，并重新检查端部与角点 |
| 凹角 | 尖锐内角 | 引入圆角 | 设计域须允许改变该边界，且网格能够分辨圆角 |

混合边界的交接即使位于光滑边界上，也可能产生应力奇异性；几何倒角不保证消除边界条件交接引起的奇异。有限刚度的 Robin 支承改变了支承模型，但不自动规定刚度沿边界平滑过渡；是否需要过渡区、端部是否仍有奇异，应结合具体模型分析。上表是建模选择，不构成应力有界性的保证。

当设计域允许改变凹角边界、存在相应材料布置空间时，应力约束优化可能通过形成圆角降低峰值，L 形支架是常用算例 [8,10]。这一行为不保证发生；圆角能否形成及被准确分辨，受设计空间、过滤或投影、网格和优化过程影响。过滤半径 $r_{\min}$ 不能直接作为圆角半径 $R$ 的保证，见 [[regularization-and-length-scale-control#3. 卷积核、过滤半径与离散实现|正则化与尺度控制 §3]]。若凹角边界由 passive 区域或固定设计域边界锁定，优化不能通过移动该边界消除尖角。

无法改变奇异源时，可按 §5.2 将指定的角点邻域排除在应力约束评价范围之外，必要时配合实体保留；强度评价结论仅适用于其余评价区域。

若验收区域包含未处理的应力奇异点，离散最大应力不能作为网格无关的强度指标。采用固定物理尺度的载荷、几何与支承模型，或明确不施加应力约束的固定物理区域后，应在一致的物理模型、应力度量与评价区域上开展网格收敛检查。固定网格比较只能说明该离散设置下的差异，不能替代收敛性验证；不同方法的网格可以不同，但物理模型与评价口径必须一致。

## 6. 应力的离散与约束评价

前五节的模型与判据都建立在连续应力场上。实际求解在有限元离散上进行，而应力的**得到方式**不唯一：它决定离散应力的误差阶、跨单元连续性与峰值行为，进而改变约束评价的结果。应力的离散方式因此是这类问题的一个独立建模变量，不只是求解细节。

### 6.1 导出应力与独立应力

| 路线 | 应力来源 | 跨单元连续性 | 典型 $L^2$ 误差阶 |
|---|---|---|---|
| 位移型离散 | 导出量，$\boldsymbol\sigma_h=\mathbb C(\rho):\boldsymbol\varepsilon(\boldsymbol u_h)$ | 一般不连续，法向牵引亦不连续 | 位移取 $P_p$、解足够光滑并满足标准逼近假设时为 $O(h^p)$ |
| 应力—位移混合离散 | 独立未知量，与 $\boldsymbol u_h$ 同时求解 | $H(\operatorname{div})$ 相容性保证法向牵引 $\boldsymbol\sigma_h\boldsymbol n$ 跨单元连续，切向分量一般仍不连续 | 依空间与阶次而定，可达 $O(h^{k+1})$ |

三条边界必须同时声明：

- $H(\operatorname{div})$ 相容**不等于**全部应力分量连续，更不等于 von Mises 等效应力连续。$\sigma_{\mathrm{vm}}$ 是分量的非线性组合，法向牵引连续不蕴含它连续；
- 上述误差阶以解的光滑性为前提。§5 的奇异点邻域不满足该前提，任何一条路线都不能在那里套用光滑解的最优阶；
- 误差阶是 $L^2$ 意义下的全局量，而局部应力约束是几乎处处的逐点条件。$L^2$ 收敛不蕴含逐点收敛，也不控制峰值——这正是 §2.3 末“离散评价点上的满足不等于连续约束已得到保证”在离散侧的根据。

### 6.2 评价点与应力恢复

约束通常在单元形心或积分点评价。评价点位置、是否做节点平均或超收敛恢复，都会改变离散峰值：不连续应力场在单元边界处有跳跃，恢复操作把跳跃抹平，所得峰值一般低于逐单元取值。恢复后的场不再是原离散解，不能用它的光滑性反过来论证约束满足。

评价口径因此至少包含五项，缺一项则离散结果不可比：

| 口径项 | 内容 | 相关节 |
|---|---|---|
| 物理模型 | 载荷、支承与几何的理想化程度 | §5.2、§5.3 |
| 应力度量 | 取实体应力还是表观应力 | §2.3 |
| 松弛形式与参数 | $\varepsilon$ 松弛、$q$–$p$ 松弛或消失约束及其参数 | §3.3 |
| 评价点与恢复方式 | 形心、积分点；是否节点平均或超收敛恢复 | 本节 |
| 评价区域 | $\Omega_{\mathrm{eval}}$ 及排除的固定物理区域 | §2.3、§5.2 |

### 6.3 网格收敛与方法对照

固定网格上的应力差异可以来自离散精度，也可以来自上表任一口径项；只有先固定口径，剩余差异才归因于离散。相应地：

- 收敛性检查须在同一物理模型与同一评价口径上进行，且只在不含未处理奇异源的区域内（§5.3 末）；
- 不同离散路线的网格可以不同，但评价口径必须一致；单元数或自由度数相等不构成“等精度”；
- 两条路线得到的体积分数或最大应力比不能单独判定孰更准确，还须核对约束可行性与同一构型下的分析结果。

混合离散的空间构造、法向迹连续性与收敛阶见 [[../huzhang/huzhang-mixed-fem|胡张混合元]]；位移法与混合法在应力约束框架下的逐项对照见 [[../../papers/huzhang-topopt/stress-constrained-topopt-models-and-algorithms|LFEM 与 Hu–Zhang 模型与算法]] §5。

## 7. 应力约束问题的非凸性与迭代稳定性

局部应力约束对设计的依赖既非线性又非局部：$\sigma_{\mathrm{vm}}^{\mathrm{solid}}$ 由状态解 $\boldsymbol u_\rho$ 决定，而 $\boldsymbol u_\rho$ 来自全局平衡方程，因此单个 $\rho_e$ 的扰动会改变整个应力场。与对 $\rho$ 线性且逐点可加的体积约束相比，有三个后果：

1. **灵敏度不稀疏**：每条局部约束的梯度都须经伴随方程求得，且一般对全体设计变量非零。§4 的三种策略应对的是约束规模，并不改变依赖的非局部性；
2. **可行域随松弛参数变形**：§3 的松弛把退化子集（§3.1）重新接回可行域，可行域形状依赖 $\varepsilon$、$q$ 的取值，参数路径因而属于问题定义，不是调参细节；
3. **约束活跃状态切换**：评价点应力接近许用值时，微小密度变化即可使约束在活跃与非活跃之间翻转。采用有效集时直接表现为迭代振荡（§4 表），采用 ALM 时表现为乘子的往复更新。

与正则化的耦合只记接口：投影使物理密度对设计变量的导数在阈值附近变陡，加剧上述非线性，故须配合 $\beta$ 延拓而非一次取到大 $\beta$；但对本页这类以体积为目标的问题，投影不是可选的边界锐化——问题本身没有把密度推向 $\{0,1\}$ 的驱动力，缺少投影会停在应力约束不激活的灰度驻点上。两条分别见 [[regularization-and-length-scale-control#4.2 $\beta$ 延拓|正则化与尺度控制 §4.2]] 与 [[regularization-and-length-scale-control#6.2 以体积为目标的局部应力约束问题：驱动力不存在|同页 §6.2]]。

**判据与边界**：

- 步长限制（move limit）、序列凸近似的渐近线参数与松弛/投影的延拓路径都直接控制上述切换的频率，它们是算法设置，不是问题定义；
- 相同的算法设置只说明两条路径的条件可比，**不保证得到相同的局部最优解**，也不要求优化轨迹或迭代步数一致——问题非凸，轨迹对初值与参数路径敏感；
- 收敛判定须依据明确的停止准则，不能以固定迭代步数代替；不同实现中同名参数（渐近线下限、move limit）的含义与量纲未必一致，跨实现比较前须逐项核实。停止准则的具体形式见 [[../../papers/huzhang-topopt/stress-constrained-topopt-models-and-algorithms|LFEM 与 Hu–Zhang 模型与算法]] §6。

## 参考依据

[1] CHENG G, JIANG Z. Study on topology optimization with stress constraints[J]. Engineering Optimization, 1992, 20(2): 129–148. DOI: 10.1080/03052159208941276.

[2] CHENG G D, GUO X. $\varepsilon$-relaxed approach in structural topology optimization[J]. Structural Optimization, 1997, 13(4): 258–266. DOI: 10.1007/BF01197454.

[3] BRUGGI M. On an alternative approach to stress constraints relaxation in topology optimization[J]. Structural and Multidisciplinary Optimization, 2008, 36(2): 125–141. DOI: 10.1007/s00158-007-0203-6.

[4] BRUGGI M, DUYSINX P. Topology optimization for minimum weight with compliance and stress constraints[J]. Structural and Multidisciplinary Optimization, 2012, 46(3): 369–384. DOI: 10.1007/s00158-012-0759-7.

[5] GIRALDO-LONDOÑO O, PAULINO G H. A unified approach for topology optimization with local stress constraints considering various failure criteria: von Mises, Drucker–Prager, Tresca, Mohr–Coulomb, Bresler–Pister and Willam–Warnke[J]. Proceedings of the Royal Society A, 2020, 476(2238): 20190861. DOI: 10.1098/rspa.2019.0861. [[../../literature/topopt/stress-constrained/translations/GiraldoLondono2020-unified-stress-constraints-zh|中文译文]]

[6] LE C, NORATO J, BRUNS T, et al. Stress-based topology optimization for continua[J]. Structural and Multidisciplinary Optimization, 2010, 41(4): 605–620. DOI: 10.1007/s00158-009-0440-y.

[7] PARÍS J, NAVARRINA F, COLOMINAS I, et al. Block aggregation of stress constraints in topology optimization of structures[J]. Advances in Engineering Software, 2010, 41(3): 433–441. DOI: 10.1016/j.advengsoft.2009.03.006.

[8] HOLMBERG E, TORSTENFELT B, KLARBRING A. Stress constrained topology optimization[J]. Structural and Multidisciplinary Optimization, 2013, 48(1): 33–47. DOI: 10.1007/s00158-012-0880-7.

[9] PEREIRA J T, FANCELLO E A, BARCELLOS C S. Topology optimization of continuum structures with material failure constraints[J]. Structural and Multidisciplinary Optimization, 2004, 26(1): 50–66. DOI: 10.1007/s00158-003-0301-z.

[10] GIRALDO-LONDOÑO O, PAULINO G H. PolyStress: a MATLAB implementation for local stress-constrained topology optimization using the augmented Lagrangian method[J]. Structural and Multidisciplinary Optimization, 2021, 63(4): 2065–2097. DOI: 10.1007/s00158-020-02760-8.

[11] WILLIAMS M L. Stress singularities resulting from various boundary conditions in angular corners of plates in extension[J]. Journal of Applied Mechanics, 1952, 19(4): 526–528.

[12] DUYSINX P, BENDSØE M P. Topology optimization of continuum structures with local stress constraints[J]. International Journal for Numerical Methods in Engineering, 1998, 43(8): 1453–1478. DOI: 10.1002/(SICI)1097-0207(19981230)43:8<1453::AID-NME480>3.0.CO;2-2.
