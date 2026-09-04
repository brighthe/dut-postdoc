---
title: "非线性有限元：几何非线性与材料非线性"
type: concept
aliases:
  - Nonlinear Finite Element Method
  - 几何非线性
  - 材料非线性
  - Geometric Nonlinearity
  - Material Nonlinearity
tags:
  - nonlinear-fem
  - finite-element
  - newton-raphson
  - constitutive-model
status: draft
date_added: 2026-08-31
date_update: 2026-09-03
---

# 非线性有限元：几何非线性与材料非线性

> **一句话**：变形不再小、或本构不再线性时，$\mathbf K\mathbf U=\mathbf F$ 退化为残量方程 $\boldsymbol R(\mathbf U)=\boldsymbol 0$，须按载荷步 × Newton 步迭代求解；几何非线性与材料非线性成因不同，切线刚度结构与状态存储也不同。

[[linear-elasticity|线弹性页]]限定「位移型、小变形、静力、各向同性」，本页是它范围之外的那一半：放松哪条假设得到哪种非线性、代价是什么。只做定性框架与判据，不做连续介质力学推导；接触非线性、动力学、屈曲后分析只提及不展开。

## 1. 线性从哪里来，非线性就从哪里破

线弹性的 $\mathbf K\mathbf U=\mathbf F$ 是线性方程组，依赖三条彼此独立的假设：

| # | 假设 | 具体含义 | 打破后得到 |
| --- | --- | --- | --- |
| 1 | 小变形（小位移小应变） | 应变是位移的线性函数 $\boldsymbol\varepsilon=\tfrac12(\nabla\boldsymbol u+\nabla\boldsymbol u^{\mathsf T})$；平衡写在未变形构型上 | **几何非线性** |
| 2 | 线性本构 | $\boldsymbol\sigma=\mathbb C:\boldsymbol\varepsilon$，$\mathbb C$ 是常张量，与变形历史无关 | **材料非线性** |
| 3 | 线性边界条件 | 载荷与约束不随变形改变 | 接触/随动载荷非线性（本页不展开） |

三者可单独出现，也可同时出现。$\mathbf K$ 一旦依赖于解 $\mathbf U$ 本身，方程就不再是线性的：

$$
\underbrace{\mathbf K\,\mathbf U=\mathbf F}_{\text{线弹性}}
\quad\Longrightarrow\quad
\underbrace{\boldsymbol R(\mathbf U)\;:=\;\boldsymbol F_{\text{int}}(\mathbf U)-\mathbf F_{\text{ext}}=\boldsymbol 0}_{\text{非线性}}
$$

其中 $\boldsymbol F_{\text{int}}$ 是内力向量。拓扑优化里的 $\mathbf K(\boldsymbol\rho)$ 不算非线性有限元：$\boldsymbol\rho$ 在每次结构分析内部是冻结的，解 $\mathbf U$ 时方程仍然线性。本页说的非线性是 $\mathbf K$ 依赖 $\mathbf U$。

## 2. 几何非线性：变形大到不能忽略构型改变

### 2.1 应变度量与平衡构型

线性应变对刚体转动不为零（转一圈会算出虚假应变），必须换成客观的有限应变度量，常用 Green–Lagrange 应变

$$
\boldsymbol E=\tfrac12\!\left(\boldsymbol F^{\mathsf T}\boldsymbol F-\boldsymbol I\right),
\qquad
\boldsymbol F=\boldsymbol I+\nabla_{\!X}\boldsymbol u
$$

$\boldsymbol F$ 是变形梯度，$\boldsymbol E$ 对 $\boldsymbol u$ 是二次的，非线性由此进入。平衡则必须在变形后的构型上满足：按参考构型的选取，分总 Lagrange 格式（参考未变形构型）与更新 Lagrange 格式（每步更新参考构型）。

### 2.2 切线刚度多出一项

线性化后的切线刚度分裂为两部分：

$$
\mathbf K_T(\mathbf U)=\underbrace{\mathbf K_{\text{mat}}}_{\text{材料/本构贡献}}+\underbrace{\mathbf K_{\sigma}(\boldsymbol\sigma)}_{\text{几何/初应力刚度}}
$$

$\mathbf K_{\sigma}$ 由当前应力状态产生，可以是负定的——屈曲、失稳因此能被捕捉，代价是 $\mathbf K_T$ 在极值点附近不再正定。

### 2.3 共旋格式：大转动 + 小应变

工程中大量问题位移和转动很大，单元自身应变却仍很小（细长结构、薄壁、点阵、软体大幅摆动）。共旋（co-rotational）格式为每个单元/子结构提取一个刚体转动 $\boldsymbol R$，在随体坐标系里沿用小应变线弹性的单元刚度，再旋转回全局：

$$
\mathbf K_e^{\text{global}}\;\approx\;\boldsymbol R\,\tilde{\mathbf K}_e\,\boldsymbol R^{\mathsf T}
$$

大转动因此被隔离到局部之外，局部刚度仍只由材料分布决定，不随全局变形状态改变。依赖「局部量与全局解耦」的降阶或代理方法，要看的正是这一条。相关工作见 §6 所列 Lv/Liu/H.W. Zhang 的多尺度共旋方法（本库无译文页，**待确认**）。

## 3. 材料非线性：本构关系不再是常数矩阵

$\boldsymbol\sigma$ 不再正比于 $\boldsymbol\varepsilon$。按是否依赖变形历史分成性质完全不同的两类：

| 类别 | 代表本构 | 路径相关性 | 需存储的状态 |
| --- | --- | --- | --- |
| **路径无关** | 超弹性（Neo-Hookean、Mooney–Rivlin、软组织本构） | 否，应力只由当前 $\boldsymbol F$ 决定 | 无（只需当前构型） |
| **路径相关** | 弹塑性、粘塑性、损伤、断裂 | 是，同一应变可对应不同应力 | 高斯点级内变量（塑性应变、硬化参量、损伤量） |

### 3.1 本构积分与返回映射

路径相关本构在每个高斯点上都要做一次本构积分：给定应变增量先弹性试探，越过屈服面则做返回映射（return mapping）把应力拉回屈服面并更新内变量，还须导出一致切线模量（consistent tangent），否则 Newton 会掉到线性收敛。代价是每个高斯点要持久保存一组内变量，内存占用远高于线弹性；单元刚度与内力的计算从一次矩阵乘变成逐高斯点跑一段含分支（弹性/塑性判定）的本构算法。非关联流动法则与损伤软化还会让 $\mathbf K_T$ 非对称。

### 3.2 路径相关与否是分水岭

超弹虽属材料非线性，但路径无关、无内变量，只是 $\boldsymbol\sigma$ 对 $\boldsymbol F$ 的非线性依赖，比弹塑性容易得多。依赖「局部响应与全局状态解耦」的降阶或代理方法，在路径无关本构下尚有可能沿用，一旦引入内变量与加载历史就不再成立。

## 4. 求解：载荷步 × Newton 步

$\boldsymbol R(\mathbf U)=\boldsymbol 0$ 一般用 Newton–Raphson：

$$
\mathbf K_T(\mathbf U_k)\,\Delta\mathbf U=-\boldsymbol R(\mathbf U_k),
\qquad
\mathbf U_{k+1}=\mathbf U_k+\Delta\mathbf U
$$

配合载荷分步加载与线搜索，强非线性、失稳问题还要弧长法（arc-length）。与线弹性的结构性差异：

| | 线弹性 | 非线性 |
| --- | --- | --- |
| 求解次数 | 1 次线性方程组 | 载荷步数 × 每步 Newton 步数 |
| $\mathbf K$ | 装配一次，全程复用 | 每个 Newton 步作废重算 |
| 谱性质 | SPD | 可能非对称（非关联/损伤）、不定（近极值点） |
| Krylov 方法 | CG | GMRES / BiCGStab |
| 预条件 | 相对成熟 | 显著更难，且每步都要重建或更新 |
| 额外状态 | 无 | 高斯点内变量（仅路径相关本构） |

「每个 Newton 步 $\mathbf K_T$ 作废」决定了不装配类方法在非线性下的相对价值：切线刚度既然每步重算，装配就是纯重复开销，而算子作用只需 $\boldsymbol y=\mathbf K_T\boldsymbol v$；代价是每次作用都要重做本构求值，预条件也更难。见 [[matrix-free/_index|Matrix-Free 主题入口]]。

## 5. 与线弹性的一页对照

| | 线弹性 | 几何非线性 | 材料非线性 |
| --- | --- | --- | --- |
| 破的假设 | — | 小变形 | 线性本构 |
| 应变度量 | $\boldsymbol\varepsilon$（线性） | $\boldsymbol E$（二次） | $\boldsymbol\varepsilon$ 或 $\boldsymbol E$ |
| 平衡构型 | 未变形 | 变形后 | 视是否叠加几何非线性 |
| 切线刚度 | $\mathbf K$ 常量 | $\mathbf K_{\text{mat}}+\mathbf K_\sigma(\boldsymbol\sigma)$ | $\mathbf K_{\text{mat}}(\text{状态})$ |
| 高斯点状态 | 无 | 无（本构仍线性时） | 路径相关时有内变量 |
| 局部量是否与全局状态解耦 | 是 | 共旋格式下分离刚体转动后仍近似成立 | 路径相关时**否** |
| 离散骨架 | 网格、形函数、单元装配、边界条件处理 | 同左 | 同左 |

最后一行是重点：网格、形函数、单元装配、自由度编号、边界条件处理在三列里是同一套。从线弹性走向非线性不是推倒重来，而是在同一骨架外面套上载荷步与 Newton 循环，并把单元层换成状态相关的计算。

## 6. 来源与关联页面

- [[linear-elasticity]] — 小变形线弹性的完整离散闭环，本页的对照基准与起点。
- [[substructural-condensation]] — 静力缩聚，局部消元的经典代数基础。
- [[matrix-free/_index|Matrix-Free 主题入口]]、[[linear-solvers/krylov-subspace-methods]] — 非线性下算子作用与 Krylov 方法的适用性。
- [[piml/piml-paradigm]] — 依赖「局部量与全局解耦」的代理方法；非线性对其成立前提的影响在该页讨论。
- `refs.bib` cite key `huangProblemindependentMachineLearning2022` 的参考文献 [39] — Lv、Liu、H.W. Zhang, *A multiscale co-rotational method for geometrically nonlinear shape morphing of 2D fluid actuated cellular structures*, Mech. Mater. 79 (2014)。**本库无该文译文页，未核验，标「待确认」。**
- 本页正文的连续介质力学与 Newton 求解内容为通用有限元教科书事实，本库尚无对应文献页，未逐条溯源。
