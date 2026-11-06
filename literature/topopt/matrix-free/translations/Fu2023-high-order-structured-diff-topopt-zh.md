---
title: "翻译：Multiphysics Simulation and Optimization using High-Order Finite Elements with Structured Differentiation"
tags:
  - translation
  - topology-opt
  - matrix-free
  - partial-assembly
  - high-order-fem
  - automatic-differentiation
  - multiphysics
status: "draft" # draft | read | done
date_created: 2026-09-26
date_updated: 2026-10-05
source: "../sources/Fu2023-high-order-structured-diff-topopt.pdf"
citekey: "Fu2023-high-order-structured-diff-topopt"
language: "zh-CN"
---

# Multiphysics Simulation and Optimization using High-Order Finite Elements with Structured Differentiation

---
# 信息

- **中文标题**：基于结构化自动微分与高阶有限元的多物理场仿真与拓扑优化
- **作者**：Yicong Fu（付轶聪 / 傅轶聪）$^1$；Bao Li（李宝 / 李保）$^1$；Graeme J. Kennedy$^1$（中文名待确认）
- **单位**：
  - $1$: Daniel Guggenheim School of Aerospace Engineering, Georgia Institute of Technology, Atlanta, Georgia, USA（佐治亚理工学院航空航天工程学院）
- **会议 / 出处**：*AIAA SCITECH 2023 Forum* (23–27 January 2023, National Harbor, MD & Online)
- **论文号**：AIAA 2023-0530
- **DOI**：https://doi.org/10.2514/6.2023-0530
- **会议日期**：2023-01-23 至 2023-01-27（原文仅印会议日期，未印单篇发表日期）
- **内容说明**：摘要与第 1 节为全文翻译；第 2–6 节为按原文逐节的精读整理（论述转述压缩，公式、编号、参数与数值按原文），**非逐句翻译**。章节编号由原文 I–VI、A/B/C 改为阿拉伯数字。

# 摘要

耦合多物理场有限元仿真的设计优化问题由于高效计算工具开发的困难而具有挑战性。为了减轻此类障碍，我们提出了一个利用结构化自动微分的面向优化的多物理场仿真框架。通过以结构化方式实现自动微分，可以从偏微分方程（PDE）多物理场系统的弱形式中计算有限元方程的残差、无矩阵（matrix-free）雅可比–向量积（Jacobian-vector products）和伴随项。框架支持包括 $L^2$、$H^1$ 和 $H(\text{div})$ 在内的混合函数空间，允许 PDE 系统的不同分量在不同函数空间内进行数值评估。采用高阶单元的 $p$-refinement（$p$ 型网格加密）以更低的计算成本实现更高的求解精度。应用和分解（Sum-factorization）以最优的时间复杂度计算高阶单元基函数，并采用无矩阵方法（matrix-free）计算雅可比–向量积[^PA-note]。模型 PDE 问题的精度和性能研究表明，$p$-refinement 在求解效率上优于 $h$-refinement。最后，求解了线弹性与热传导的拓扑优化问题，展示了该多物理场设计与优化框架的综合能力。

[^PA-note]: 译者判断（非原文内容）：原文只称 “matrix-free Jacobian-vector products” 并以和分解实现，未使用 partial assembly（PA）一词。结合作者开源代码（`smdogroup/a2d`、`smdogroup/a2d-multiphysics` 中的 `MatrixFree` 类在积分点预存导数矩阵 `qmat`）推断其实现对应高阶有限元中的 PA；该判断未经原文证实，引用时应标注为译者推断。

# 1 引言

多物理场仿真在单一强耦合仿真中耦合了系统的多个物理层面。在复杂工程系统设计优化的背景下，多物理场数值仿真能够产生更现实的设计，因为它们捕获了孤立学科分析所忽略的耦合效应。在航空航天工程领域，相关的物理模型可能包括结构力学、结构热力学、空气动力学、声学、波动传播和电磁学。文献中有许多多物理场仿真和设计优化的例子。例如，Burghardt 等人 [8] 提出了一种针对流体、热和结构问题的通用的基于梯度的多物理场优化方法；Babcock 等人 [4] 对电动机进行了静磁–热耦合分析；Kim 等人 [25] 对涉及力学、电学和机电分析的压电系统进行了多物理场拓扑优化；Kang 和 James [24] 考虑了非线性热机械效应对形状记忆合金进行了拓扑优化；Rosu 等人 [42] 针对电机设计提出了电磁、热和力学耦合的多物理场仿真；Economon 等人 [14] 开发了 SU2，用于求解非结构网格拓扑上的 PDE 多物理场问题；Astaneh 等人 [3] 通过耦合电化学和热模型在电池开发中执行基于仿真的设计优化。

广泛采用多物理场仿真的一个障碍是物理模型的正向和灵敏度分析需要大量的开发工作和计算时间。用于多物理场仿真的计算框架可分为两类：单整框架（monolithic frameworks，将所有分析紧密集成到单一系统中）和异构方法（heterogeneous methods，利用多种离散、代码和求解策略）。紧密集成框架的例子包括 FreeFEM [20]、MFEM [2]、FEniCS/DOLFIN [29]、Sundance [30] 和 SU2 [14]，而异构框架的例子包括多学科耦合问题，如 OpenMDAO [17] 和 FUNtoFEM [23, 26]。在这项工作中，我们专注于紧密集成的方法，依靠有限元方法进行底层离散。这种方法的一个关键挑战是在所提出的框架内实现多个物理模型的额外负担。对于受非线性偏微分方程控制的物理问题，这一障碍十分显著，手工形成线性化既耗时又容易出现人为错误。为了应对上述挑战并简化多物理场分析和优化的开发过程，我们提出了一种用于求解具有有限元方法的线性和非线性偏微分方程的结构化微分框架。

通过以结构化的方式利用自动微分技术来获得离散化中的关键项，可以减少开发多物理场问题分析代码的工作量，而不会牺牲多物理场框架的计算性能和效率。

# 2 多物理场问题列式

> 第 2–6 节为按原文逐节的精读整理，非逐句翻译：论述以中文转述并压缩，公式、编号、参数与数值按原文给出，译者推断以脚注或“译者注”标出。

本节给出框架统一处理的变分形式，并以热传导、Helmholtz 滤波、线弹性三个算例说明各自需要的导数。

## 2.1 控制方程

**设定。** 以 Galerkin 有限元离散，近似解 $u_h\in V_h$ 满足半线性变分形式
$$
R(x_h, u_h, v_h) = 0, \quad \forall v_h \in V_h \tag{1}
$$
- $x_h\in X_h$ 为给定的设计变量，$V_h$ 为相应的有限维函数空间；
- 半线性形式对测试函数 $v_h$ 线性，对 $u_h$、$x_h$ 可以非线性；
- 求得 $u_h$ 后，泛函 $f(x_h,u_h)$ 作为优化的目标或约束；
- 为简化表述，只考虑全域积分，不含边界面积分。

**数值积分。** 在网格 $\mathcal T_h$（$\bigcup_{K\in\mathcal T_h}K=\Omega$）上用积分公式计算：
$$
R_h(x_h, u_h, v_h) = \sum_{K \in \mathcal{T}_h} \sum_{q \in Q_K} w_q |\det J_q|\, I_h(x_h|_q, u_h|_q, v_h|_q) \tag{2}
$$
$Q_K$ 为单元 $K$ 的积分点集，$w_q$ 与 $\det J_q$ 为积分点 $q$ 处的积分权重与单元映射 Jacobian 行列式，$I_h$ 为离散被积函数。此后省略 $|_q$，$I_h$ 的自变量一律理解为积分点上的取值。

**所需导数与 $I_h$ 的对应关系。** 对 $I_h$ 关于 $v_h,u_h,x_h$ 及其出现在被积函数中的梯度、旋度、散度求导：

| 所需项 | 对 $I_h$ 的求导方式 |
|---|---|
| 离散残差 | 对 $v_h$ 及作用于 $v_h$ 的微分算子求一阶导 |
| Jacobian | 先对 $v_h$ 及其微分算子、再对 $u_h$ 及其微分算子求混合二阶导 |
| 伴随–向量积 | 令 $v_h=\psi_h$（伴随变量），对 $x_h$ 求导 |

这些导数不手工实现，而由第 3.1 节的结构化微分计算。该方法只处理积分点上的量，与计算 $x_h,u_h,v_h$ 所用的单元基函数无关。

## 2.2 势能问题

许多力学问题可由总势能驻值原理导出。总势能写成积分点求和
$$
\Pi_h(x_h, u_h) = \sum_{K \in \mathcal{T}_h} \sum_{q \in Q_K} w_q |\det J_q|\, \pi_h(x_h|_q, u_h|_q) \tag{3}
$$
其中 $\pi_h$ 为积分点上的势能密度。令其关于 $u_h$ 的一阶变分为零：
$$
\delta \Pi_h(x_h, u_h, \delta u_h) = \sum_{K \in \mathcal{T}_h} \sum_{q \in Q_K} w_q |\det J_q|\, \delta \pi_h(x_h|_q, u_h|_q, \delta u_h|_q) = 0, \quad \forall \delta u_h \in V_h \tag{4}
$$
取 $R_h(x_h,u_h,v_h)=\delta\Pi_h(x_h,u_h,v_h)$，并在每个积分点令 $I_h=\delta\pi_h$，式 (4) 即归入半线性形式 (2)。此时形成 Jacobian 所需的是 $\pi_h$ 关于 $u_h$ 及其微分算子的二阶导数。

## 2.3 多物理场算例

### 2.3.1 热传导

**强形式。** 用于拓扑优化、采用 RAMP 惩罚 [48] 的稳态热传导：
$$
-\nabla \cdot \left( \kappa_0 \frac{x}{1 + q(1-x)} \nabla u \right) = g, \qquad u|_{\Gamma_0} = 0, \qquad n \cdot \nabla u|_{\Gamma_1} = 0
$$
- 温度 $u\in H^1(\Omega)$；$\Gamma_0$ 上 Dirichlet、$\Gamma_1$ 上 Neumann 条件，$\Gamma_0\cup\Gamma_1=\partial\Omega$；
- $g$ 为体热源，$\kappa_0$ 为导热系数，$q$ 为 RAMP 惩罚参数；
- 设计变量 $x\in L^2(\Omega)$，$0\le x\le 1$。

**变分形式与被积函数。**
$$
R(x,u,v)=\int_\Omega \left(\kappa_0\frac{x}{1+q(1-x)}\nabla u\cdot\nabla v-gv\right)\mathrm d\Omega=0,\qquad \forall v\in H^1_0(\Omega)
$$
$H^1_0(\Omega)$ 为满足本质边界条件 $u|_{\Gamma_0}=0$ 的 $H^1$ 函数空间。被积函数为
$$
I_h(x_h, u_h, v_h) = \kappa_0 \frac{x_h}{1 + q(1-x_h)} \nabla_h u_h \cdot \nabla_h v_h - v_h g \tag{5}
$$
$\nabla_h$ 为离散梯度。

**导数。**
- 残差：
$$
\frac{\partial I_h}{\partial v_h}=-g,\qquad
\frac{\partial I_h}{\partial \nabla_h v_h}=\kappa_0\frac{x_h}{1+q(1-x_h)}\nabla_h u_h
$$
- Jacobian：沿 $\nabla_h u_h$ 的搜索方向 $\nabla_h p_h$ 取方向导数，
$$
\frac{\partial^2 I_h}{\partial \nabla_h v_h \partial \nabla_h u_h} \cdot \nabla_h p_h = \kappa_0 \frac{x_h}{1 + q(1-x_h)} \nabla_h p_h
$$
- 伴随–残差积对设计变量的导数（$\psi_h$ 为伴随变量）：
$$
\frac{\partial I_h}{\partial x_h} = \kappa_0 \frac{1+q}{(1 + q(1-x_h))^2} \nabla_h u_h \cdot \nabla_h \psi_h
$$

作者指出这个简单算例的导数可以手推，结构化微分的价值在更复杂的导数上。

### 2.3.2 拓扑优化 Helmholtz 滤波

Helmholtz PDE 在拓扑优化中用于控制设计的长度尺度、得到网格无关解 [28]，强形式为
$$
\rho - r_0^2 \nabla^2 \rho = x, \quad n \cdot \nabla u|_{\partial \Omega} = 0 \tag{6}
$$
$r_0$ 为特征长度，输入为设计变量 $x\in L^2(\Omega)$（$0\le x\le1$），输出为滤波密度 $\rho\in H^1(\Omega)$[^helmholtz-bc]。

[^helmholtz-bc]: 译者注：式 (6) 边界条件按原文照录为 $n\cdot\nabla u$；按上下文，滤波问题的未知量是 $\rho$，此处应为 $n\cdot\nabla\rho$。

**混合列式。** 不直接用式 (6)，而引入通量 $\sigma=-r_0\nabla\rho$：
$$
\begin{aligned}
\rho + r_0 \operatorname{div}(\sigma) - x &= 0 \\
\sigma + r_0 \nabla \rho &= 0
\end{aligned} \tag{7}
$$
其中 $\rho\in L^2(\Omega)$、$\sigma\in H_0(\operatorname{div},\Omega)$。试探函数 $u=(\rho,\sigma)$，测试函数 $v=(\eta,\tau)$，弱形式为
$$
R(x,(\rho,\sigma),(\eta,\tau))=\int_\Omega\bigl(\sigma\cdot\tau-r_0\operatorname{div}(\tau)\,\rho-r_0\operatorname{div}(\sigma)\,\eta-\rho\eta+x\eta\bigr)\,\mathrm d\Omega \tag{8}
$$
对应的被积函数（$\operatorname{div}_h$ 为离散散度）：
$$
I_h(x_h, (\rho_h, \sigma_h), (\eta_h, \tau_h)) = \sigma_h \cdot \tau_h - r_0 \operatorname{div}_h(\tau_h) \rho_h - r_0 \operatorname{div}_h(\sigma_h) \eta_h - \rho_h \eta_h + x_h \eta_h \tag{9}
$$
与热传导相同，式 (9) 在积分点上的一阶、二阶导数给出离散方程与伴随所需的项。

### 2.3.3 拓扑优化线弹性

结构拓扑优化常以各向同性线弹性为模型来优化刚度或强度 [46]。
- 未知量为位移场 $u_h\in[H^1(\Omega)]^3$，带相应的 Dirichlet 条件；
- 应变 $E\in\mathbb S^3$：$E=\tfrac12\bigl(\nabla_h u_h+\nabla_h u_h^{\mathsf T}\bigr)$；
- 应力 $S\in\mathbb S^3$，各向同性 Hooke 定律：$S=2\mu E+\lambda\operatorname{tr}(E)\,I$，$\mu,\lambda$ 为 Lamé 参数。

施加 RAMP 惩罚 [48] 后，总势能中的应变能密度为
$$
\pi_h(x_h, u_h) = \frac{1}{2} \frac{x_h}{1 + q(1-x_h)} \operatorname{tr}(S E) \tag{10}
$$
离散残差与 Jacobian 分别需要式 (10) 关于 $\nabla_h u_h$ 的一阶与二阶导数。

# 3 自动微分

**基本概念。** 自动微分（AD）对代码中的数值计算求导，依赖两点：编程语言基本运算与内建函数的偏导表达式，以及链式法则 [18, 35, 37]。AD 把计算分解为一元、二元基本运算，按链式法则累积各变量的导数；可处理分支、循环与递归，且没有截断误差 [5, 18]。原文的比较是：比符号微分快 [12, 35]，比有限差分准。

| 维度 | 选项 | 原文要点 |
|---|---|---|
| 模式 | 前向 | 逐列计算 Jacobian，代价随输入个数增长 |
| | 反向 | 逐行计算 Jacobian，代价随输出个数增长；需存储的数据比前向多 [15, 18]，有降低内存的技术 [18] |
| 实现 | 源码变换 | 解析源码，生成求导代码 |
| | 运算符重载 | 定义同时携带值与导数的扩展数据类型 [35] |

**文献综述（压缩）。**
- 结构力学：Chinchalkar [11] 用 AD 构造伴随项并做形状灵敏度；Hou 等 [22] 求热有限元问题对设计变量的一、二阶导；Rothe 与 Hartmann [43] 比较手推、有限差分与 AD 求切线刚度，结论是 AD 准确且实现量小；Chandrasekhar 等 [9] 用 JAX 求二维拓扑优化导数；Vigliotti 与 Auricchio [49] 以应变能积分为自由能，用 AD 直接得到残差力向量（梯度）与切线刚度（Hessian）。
- CFD：Mader 等 [34] 为 Euler 求解器选择性地用 AD 构造离散伴随；Lyu 等 [31] 推广到 RANS 并用着色提高效率；He 等 [19] 为 OpenFOAM [50] 实现离散伴随；Sagebaum 等 [44, 45] 基于表达式模板开发 CoDiPack，并为 SU2 [14] 实现离散伴随。
- 机器学习：动态计算图与可微编程推动了 AD 的应用 [5]；autograd [32, 33]、PyTorch [40]、TensorFlow [1] 等支持在 CPU、GPU 上执行 AD [5, 39]。

## 3.1 面向多物理场仿真的结构化自动微分

**目标与取舍。** 结构化微分用于计算有限元积分点上各量的导数，要求在时间和内存上都高效。与通用 AD 工具的区别：
- 按 Giles [16] 的方法，对积分点级的小型稠密矩阵、向量运算直接实现一阶与二阶导数；
- 由这些矩阵、向量导出的标量量（如迹）的导数由用户实现，反向模式的调用栈也由用户管理；
- 这增加了实现工作量，换来可以跳过被动变量（passive variables）求导的灵活性，从而提高计算效率。

在有限元中，求导对象是被积函数 $I_h$ 或 $\pi_h$。

**记号。** 设标量函数 $f(y(x)):\mathbb R^n\to\mathbb R$，输入 $x\in\mathbb R^n$，中间变量 $y\in\mathbb R^m$。链式法则（Einstein 求和）为
$$
\frac{\partial f}{\partial x_i}=\frac{\partial f}{\partial y_j}\frac{\partial y_j}{\partial x_i}.
$$
定义伴随量 $\bar y_j=\partial f/\partial y_j$、$\bar x_i=\partial f/\partial x_i$，反向模式关系为
$$
\bar x_i=\bar y_j\frac{\partial y_j}{\partial x_i}.
$$

**一阶导数示例：各向同性线弹性。** 取式 (10) 且不含设计变量依赖（等价于 $q=0$）。残差是 $\pi_h$ 关于 $u_h$ 与 $\nabla_h u_h$（视为独立变量）的一阶导，令 $f=\pi_h$，反向扫描依次为
$$
\bar S=\tfrac12\,\bar\pi_h\,E,\qquad
\bar E=\tfrac12\,\bar\pi_h\,S+2\mu\,\bar S+\lambda\operatorname{tr}(\bar S)\,I,\qquad
\overline{\nabla_h u_h}=\bar E .
$$
迹运算的输出是标量，种子 $\bar\pi_h=1$ 由用户给定。实现采用 C++ 类模板的运算符重载，所有中间量的存储与原变量相同。

**二阶导数：Hessian–向量积。** 二阶导数通过 Hessian–向量积计算，有两种用途：直接做一次矩阵–向量积，或在积分点上构造 Jacobian 矩阵。（译者注：原文未说明算例采用哪一种；对应开源代码 `MatrixFree::initialize` 采用后者、即 PA 的判断为译者推断，见摘要脚注。）

沿任意方向 $\dot x\in\mathbb R^n$，
$$
\frac{\partial^2 f}{\partial x_i \partial x_j} \dot{x}_j = \frac{\partial^2 f}{\partial y_k \partial y_l} \frac{\partial y_k}{\partial x_i} \frac{\partial y_l}{\partial x_j} \dot{x}_j + \frac{\partial f}{\partial y_k} \frac{\partial^2 y_k}{\partial x_i \partial x_j} \dot{x}_j .
$$
引入前向切向量 $\dot y\in\mathbb R^m$ 与 Hessian–向量积变量 $\hat x\in\mathbb R^n$、$\hat y\in\mathbb R^m$：
$$
\dot y_j=\frac{\partial y_j}{\partial x_i}\dot x_i,\qquad
\hat y_i=\frac{\partial^2 f}{\partial y_i\partial y_j}\dot y_j,\qquad
\hat x_i=\frac{\partial^2 f}{\partial x_i\partial x_j}\dot x_j ,
$$
则
$$
\hat{x}_i = \hat{y}_k \frac{\partial y_k}{\partial x_i} + \bar{y}_k \frac{\partial^2 y_k}{\partial x_i \partial x_j} \dot{x}_j .
$$

计算流程为三趟扫描：
1. 反向扫描，求一阶伴随 $\bar y$；
2. 前向扫描，由 $\dot x$ 求 $\dot y$；
3. 反向扫描，累积得到 $\hat x$。

中间量 $\dot y$、$\hat y$、$\bar y$ 的存储都与 $y$ 相同，因此 Hessian–向量积的总存储约为原始代码的 4 倍。

# 4 高阶有限元离散

**动机与文献（压缩）。** 高阶有限元有望以更低成本获得更高的解与泛函精度，前提是有限元运算与求解流程对阶数 $p$ 的复杂度要优化好；$d$ 维问题上朴素的有限元矩阵计算可达 $\mathcal O(p^{3d})$。
- Orszag [38]：对张量积插值用 sum factorization 计算全阶算子的 Jacobian–向量积，并以低阶算子作预条件，Jacobian–向量积达到最优的 $\mathcal O(p^{d+1})$；
- Melenk 等 [36]：高阶单元刚度矩阵组装的高效积分算法；
- 沿 Orszag 思路、全阶矩阵从不组装的 matrix-free 预条件研究：Deville 与 Mund [13] 评估伪谱有限元椭圆问题的低阶预条件；Bello-Maldonado 与 Fischer [6] 用高阶离散的 GLL 点构造低阶矩阵并施加 AMG，求解 Poisson 方程；Pazner 等 [41] 为 de Rham 复形单元构造低阶预条件并结合 AMG。

**本文做法。** 六面体单元上的张量积基函数；用 sum factorization 计算高阶 Jacobian 的作用而不组装矩阵；在每个单元的 GLL 点上构造低阶网格作预条件，以光滑聚合多重网格作 CG 的预条件子。

## 4.1 高阶有限元基

**单元映射。** 参考单元 $\hat K$ 经微分同胚 $K=F(\hat K)$ 映到物理单元，$x=F(\hat x)$，Jacobian $J(\hat x)=\nabla F(\hat x)$ 在 $\hat K$ 上处处可逆。六面体参考域 $\hat K=[-1,1]^3$；$H^1(K)$、$H(\operatorname{div},K)$、$L^2(K)$ 的基先在 $\hat K$ 上构造再映射到物理单元 [7, 47]。

**一维 Lagrange 多项式。** $[-1,1]$ 上 $n$ 个 Gauss–Legendre–Lobatto（GLL）点记为 $l_n$，$n$ 个 Gauss–Legendre（GL）点记为 $g_n$。以 GLL 点插值的 $p$ 次 Lagrange 多项式记为
$$
\ell_i^{(p)}(\hat x;\,l_{p+1}),\qquad i=1,\dots,p+1,
$$
以 GL 点插值者记法类推。

**三类基函数。**

| 空间 | 参考单元上的基 | 个数 | 到物理单元的映射 |
|---|---|---|---|
| $H^1(\hat K)$ | $\ell_i^{(p)}(\hat x_1;l_{p+1})\,\ell_j^{(p)}(\hat x_2;l_{p+1})\,\ell_k^{(p)}(\hat x_3;l_{p+1})$，$i,j,k=1,\dots,p+1$ | $(p+1)^3$ | $u_h(x)=\hat u_h(\hat x)$，$\nabla_h u_h(x)=(\nabla\hat u_h(\hat x))\,J^{-1}$ |
| $H(\operatorname{div},\hat K)$ | $B_{p,1}\cup B_{p,2}\cup B_{p,3}$，见下式 | $3(p+1)p^2$ | Piola 变换，见下式 |
| $L^2(\hat K)$ | $\ell_i^{(p-1)}(\hat x_1;g_p)\,\ell_j^{(p-1)}(\hat x_2;g_p)\,\ell_k^{(p-1)}(\hat x_3;g_p)$，$i,j,k=1,\dots,p$ | $p^3$ | $u_h(x)=\hat u_h(\hat x)$ |

$H^1$ 梯度变换中 $\nabla(\cdot)$ 按行向量约定。

$H(\operatorname{div},\hat K)$ 的向量基（$e_1,e_2,e_3$ 为笛卡尔基）：法向分量方向用 $p$ 次 GLL 插值，其余两个方向用 $p-1$ 次 GL 插值，
$$
\begin{aligned}
B_{p,1}&=\bigl\{e_1\,\ell_i^{(p)}(\hat x_1;l_{p+1})\,\ell_j^{(p-1)}(\hat x_2;g_p)\,\ell_k^{(p-1)}(\hat x_3;g_p)\ \big|\ i=1,\dots,p+1;\ j,k=1,\dots,p\bigr\},\\
B_{p,2}&=\bigl\{e_2\,\ell_i^{(p-1)}(\hat x_1;g_p)\,\ell_j^{(p)}(\hat x_2;l_{p+1})\,\ell_k^{(p-1)}(\hat x_3;g_p)\ \big|\ j=1,\dots,p+1;\ i,k=1,\dots,p\bigr\},\\
B_{p,3}&=\bigl\{e_3\,\ell_i^{(p-1)}(\hat x_1;g_p)\,\ell_j^{(p-1)}(\hat x_2;g_p)\,\ell_k^{(p)}(\hat x_3;l_{p+1})\ \big|\ k=1,\dots,p+1;\ i,j=1,\dots,p\bigr\}.
\end{aligned}
$$
Piola 变换及其散度关系（$\operatorname{div}_{\hat K}$ 为参考单元上的散度）：
$$
u_h(x) = \frac{1}{\det J}\, J\, \hat{u}_h(\hat{x}), \qquad \operatorname{div}_h u_h(x) = \frac{1}{\det J} \operatorname{div}_{\hat{K}} \hat{u}_h(\hat{x})
$$

## 4.2 代数多重网格预条件子

![[Fu2023_Fig1.png]]

<center><b>
图 1：二维四边形单元上 $H^1$、$H(\operatorname{div})$ 和 $L^2$ 基函数的自由度示意以及低阶预条件网格剖分：（a）$H^1(\hat{K}), p=5$；（b）$H(\operatorname{div}, \hat{K}), p=5$；（c）$L^2(\hat{K}), p=4$；（d）低阶预条件网格剖分
</b></center>

**构造。** 沿 GLL 网格把高阶六面体单元剖开，形成低阶离散；以低阶矩阵经光滑聚合 AMG 作全阶问题的预条件。四边形单元上的空间与低阶剖分见图 1。

**谱检验。** 预条件效果通过单个高阶单元上的广义特征值问题间接评估：
$$
K v = \lambda K_1 v \tag{11}
$$
$K$、$K_1$ 分别为高阶单元及其低阶近似的 Jacobian 矩阵。去掉对应零空间的零特征值后，记 $\kappa(K_1^{-1}K)=|\lambda_{\max}|/|\lambda_{\min}|$。仿照 Bello-Maldonado 与 Fischer [6]，用图 2 的畸变六面体单元，分别对 Poisson 与线弹性离散考察 $\kappa$ 随阶数 $p$ 与畸变长宽比 AR 的变化（图 3）。

![[Fu2023_Fig2.png]]

<center><b>
图 2：用于谱分析研究的具有变化长宽比 $\text{AR} = b/a$ 和多项式阶数 $p$ 的畸变六面体单元（图中 $\text{AR} = 8, p = 10$）
</b></center>

![[Fu2023_Fig3.png]]

<center><b>
图 3：随着多项式阶数和单元几何长宽比变化的条件数 $\kappa(K_1^{-1} K)$：（a）泊松问题雅可比矩阵的条件数；（b）线弹性问题雅可比矩阵的条件数
</b></center>

**结果。**
- $p=1$ 时两矩阵重合，$\kappa=1$；
- $\kappa$ 随 $p$ 与 AR 增大而增大，但在所考察范围内 Poisson 问题 $<60$、线弹性问题 $<160$；
- $\text{AR}=1$ 时分别 $<25$ 和 $<40$。

作者据此认为基于 $K_1$ 的低阶预条件用于全阶问题“有潜力”表现良好；这是单单元谱的间接证据，不是全局迭代次数的测试。

## 4.3 精度与可扩展性研究

用两个模型问题检验高阶离散的精度。

**Poisson 问题。** 球形区域（图 4），外表面施加 Dirichlet 条件：
$$
-\nabla^2u=r^4,\qquad u\in H^1(\Omega),\qquad u|_{\partial\Omega}=0,
$$
解析解按原文为
$$
u^*=\frac{1}{42}\left(r^6-R^6\right),
$$
$R$ 为球半径[^poisson-sign]。线性系统用 PCG 求解至相对收敛容差 $10^{-14}$。

[^poisson-sign]: 译者注：按原文照录。三维中 $\nabla^2 r^6=42\,r^4$，故原文 $u^*$ 满足 $-\nabla^2u^*=-r^4$，与所写方程差一个符号；与 $-\nabla^2u=r^4$ 及 $u|_{\partial\Omega}=0$ 一致的解应为 $u^*=\tfrac{1}{42}(R^6-r^6)$。已对照原文第 9 页渲染页确认原文即如此印刷。符号不影响误差曲线的形态，但无法从原文判断代码实际采用哪一种。

![[Fu2023_Fig4.png]]

<center><b>
图 4：多项式阶数 $p = 10$ 的球体网格剖面示意
</b></center>

**结果（$p=1\sim10$）。**
- 图 5：无论以自由度数还是求解时间为横轴，阶数越高误差下降越快，作者据此认为 $p$-refinement 比全局 $h$-refinement 更高效；
- 图 6：线性系统求解时间与自由度数呈线性关系，且与阶数无关，作者以此说明框架实现的可扩展性。图中另画有 slope = 1 的参考三角形；各阶数曲线大体贴近该斜率并彼此靠拢[^fig6-note]。

[^fig6-note]: 译者注：“各阶数曲线大体贴近并彼此靠拢”是译者对图 6 的目视读数，原文正文只称线性关系。原文未给出各阶数的迭代次数或单次算子作用耗时，因此该结果反映的是 matrix-free 算子、低阶 AMG 预条件与 PCG 的整体表现，不能单独归因于其中某一项。

![[Fu2023_Fig5.png]]

<center><b>
图 5：泊松问题的精度与可扩展性研究：（a）不同多项式阶数下作为未知量数函数的解误差 $\|u - u^*\|_2$；（b）不同多项式阶数下作为求解时间函数的解误差 $\|u - u^*\|_2$
</b></center>

![[Fu2023_Fig6.png]]

<center><b>
图 6：泊松问题在不同多项式阶数下求解时间随未知量数的变化
</b></center>

**混合 Helmholtz 问题。** 作为混合单元实现的演示，求解混合形式 (7)，右端给定为
$$
u+r_0\operatorname{div}(\sigma)=R^2-r^2,\qquad \sigma+r_0\nabla u=0,\qquad n\cdot\sigma|_{\partial\Omega}=0,
$$
其中 $\sigma\in H(\operatorname{div},\Omega)$、$u\in L^2(\Omega)$。
- 求解：对每个单元的 $L^2(\Omega)$ 自由度做静态凝聚，在低阶网格上施加常规光滑聚合 AMG 作预条件；
- 作者明言这是此类问题公认的较差预条件，更有效的选择留待未来 [21, 27]；
- 图 7 给出 $p=1,2,3$ 的误差随自由度数的变化。原文未写出此问题的参考解 $u^*$。

![[Fu2023_Fig7.png]]

<center><b>
图 7：混合 Helmholtz 问题的精度研究：不同多项式阶数（$p=1, 2, 3$）下解误差 $\|u - u^*\|_2$ 随未知量数的变化曲线
</b></center>

# 5 结果

本节以热与力学两类拓扑优化算例演示框架：体积约束下最小化散热器热柔度，以及体积约束下最小化外载作用的结构柔度。设计更新均用 ParOpt 优化包 [10] 中的移动渐近线法（MMA）。

## 5.1 散热器拓扑优化

**问题。**
$$
\begin{aligned}
\min_x \quad & \int_{\Omega} u g \, \mathrm{d}\Omega \\
\text{s.t.} \quad & 0 \le x \le 1, \quad \int_{\Omega} x \, \mathrm{d}\Omega \le V_0 \\
\text{governed by} \quad & -\nabla \cdot \left( \kappa_0 \frac{x}{1+q(1-x)} \nabla u \right) = g,\qquad u|_{\Gamma_0}=u_0,\qquad n\cdot\nabla u|_{\Gamma_1}=0
\end{aligned}
$$
- $\Omega$ 为设计域，$\Gamma_0$ 为施加 Dirichlet（等温热沉）条件的部分边界，$u_0$ 为热沉温度；
- $x$ 为设计变量，$u$ 为温度，$g$ 为域内给定热源，$V_0$ 为体积上限，$\kappa_0$ 为导热系数；
- 参数：$g=1$，$u_0=0$，$V_0=0.4V$（$V$ 为设计域体积）；
- 网格：结构化六面体网格，取不同阶数；图 8 为 $p=9$ 的实例。

![[Fu2023_Fig8.png]]

<center><b>
图 8：导热散热问题的设计域与网格示意（单元多项式阶数 $p = 9$）
</b></center>

**惩罚与后处理。** 两个算例都用 RAMP 惩罚 [48] 以求得边界清晰的 0-1 设计。经 300 次 MMA 迭代得到各阶数的设计（图 9，色标为温度分布）。
- 六面体单元的自由度随 $p$ 立方增长，作者相应减少单元数，使全局自由度大致不变（数值见图 9）；
- 设计变量收敛时趋近 0 或 1，但本质上仍连续，图中显示的是 $x\ge0.5$ 的等值体后处理结果。

**滤波。** 滤波在拓扑优化中用于网格无关与长度尺度控制，在低阶单元下还用于抑制棋盘格。本文的做法是：
- 用比求解空间更低阶的多项式插值密度场；
- 再以 Bernstein 多项式把密度插值回求解空间，借其单位分解性质自动满足 $0\le x\le1$。

**观察。** 图 9 的设计表现出网格依赖，并在表面出现周期性图案。作者将其归因于这种低阶 Bernstein 滤波本身不具网格无关性，计划改用带长度尺度控制的显式滤波。

![[Fu2023_Fig9.png]]

<center><b>
图 9：采用不同多项式阶数有限元基的热传导问题拓扑优化结果：（a）$p = 2$，自由度 $531,441$；（b）$p = 3$，自由度 $570,775$；（c）$p = 4$，自由度 $531,441$；（d）$p = 5$，自由度 $531,441$；（e）$p = 6$，自由度 $548,887$；（f）$p = 7$，自由度 $563,550$；（g）$p = 8$，自由度 $611,585$；（h）$p = 9$，自由度 $532,900$
</b></center>

## 5.2 最小化结构柔度拓扑优化

线弹性各向同性结构的柔度最小化等价于最小化变形应变能。问题写为
$$
\begin{aligned}
\min_x \quad & \int_{\Omega} \pi(x, u) \, \mathrm{d}\Omega \\
\text{s.t.} \quad & 0 \le x \le 1, \quad \int_{\Omega} x \, \mathrm{d}\Omega \le V_0 \\
\text{governed by} \quad & \delta \Pi(x, u, \delta u, f) = 0 \quad \forall \delta u,\qquad u|_{\Gamma_0}=u_0
\end{aligned} \tag{12}
$$
$u$ 为位移场，$\Gamma_0$ 为位移给定为 $u_0$ 的部分边界，$\pi$ 为点上的弹性能，$\Pi$ 为系统势能，$f$ 为外加保守面力，$V_0$ 为体积上限；控制方程以变分形式给出。

**两个算例。**

| 算例 | 约束 | 载荷 | 网格示意 | 全局自由度 | 阶数 |
|---|---|---|---|---|---|
| 悬臂梁 | 一侧全部自由度固定 | 另一侧部分区域施加竖向面力 | 图 10 | 约 142 万～149 万 | $p=2,3,4,5,7,8,9,10$ |
| 空心圆柱 | 另一端与加载位置对应的四个部分全部自由度固定 | 一端四个等分部分施加扭转面力 | 图 11 | 约 104 万～106 万 | $p=2,4,5,7,10$ |

两例均用高阶六面体单元剖分，图 10、图 11 给出 $p=10$ 网格的局部。

![[Fu2023_Fig10.png]]

<center><b>
图 10：三维悬臂梁弯曲问题的计算域与网格示意（单元多项式阶数 $p = 10$）
</b></center>

![[Fu2023_Fig11.png]]

<center><b>
图 11：三维空心受扭圆柱问题的计算域与网格示意（单元多项式阶数 $p = 10$）
</b></center>

**结果。** 问题 (12) 经 300 次 MMA 迭代求解，设计见图 12、图 13，色标为位移大小。与散热算例一样，随 $p$ 增大相应减少单元数，使自由度大致不变。
- 悬臂梁：随 $p$ 增大，侧部与中部连接上下两面的杆件逐渐缩小并最终消失；同时开始出现周期性齿状伪影；
- 伪影成因与散热算例相同，即在 Bernstein 多项式张成的设计空间中优化，作者认为可用显式滤波改善；
- 空心圆柱：各阶数下的优化设计保持一致。

![[Fu2023_Fig12.png]]

<center><b>
图 12：采用不同多项式阶数有限元基的悬臂梁拓扑优化结果：（a）$p=2$，自由度 $1,469,061$；（b）$p=3$，自由度 $1,484,679$；（c）$p=4$，自由度 $1,486,875$；（d）$p=5$，自由度 $1,423,053$；（e）$p=7$，自由度 $1,456,920$；（f）$p=8$，自由度 $1,454,355$；（g）$p=9$，自由度 $1,460,730$；（h）$p=10$，自由度 $1,423,053$
</b></center>

![[Fu2023_Fig13.png]]

<center><b>
图 13：采用不同多项式阶数的空心受扭圆柱拓扑优化结果：（a）$p = 2$，自由度 $1,041,984$；（b）$p = 4$，自由度 $1,041,984$；（c）$p = 5$，自由度 $1,045,440$；（d）$p = 7$，自由度 $1,064,448$；（e）$p = 10$，自由度 $1,037,520$
</b></center>

# 6 结论

**工作内容。**
1. 高阶有限元多物理场仿真与优化框架；以结构化方式实现 AD，减少为（可能非线性的）多物理场 PDE 及其离散伴随方程形成 Jacobian 线性化的开发量与人为错误；
2. 为以更低成本获得更高的解与泛函精度，采用 $H^1$、$H(\operatorname{div})$、$L^2$ 高阶单元离散；
3. 以 sum factorization 优化 matrix-free Jacobian–向量积的计算复杂度；
4. 为加速线性求解并保留使用非结构网格的灵活性，采用 AMG 预条件。

**作者给出的结论。**
- $p=1\sim10$ 的研究表明，在相同计算资源下高阶单元的误差下降更快；
- 求解流程的计算成本随问题规模线性增长，与阶数无关；
- 高阶单元与其低阶近似的谱研究表明，条件数随阶数与网格畸变仅温和增长，说明低阶预条件具有潜在有效性；
- 拓扑优化演示：散热结构最小化热柔度，最多约 61.1 万自由度、$p=9$；弯曲与扭转载荷下最小化结构柔度，最多约 148 万自由度、$p=10$。

**未来工作。**
- 为含 $H(\operatorname{div})$、$H(\operatorname{curl})$ 的混合有限元列式研究更有效的预条件；
- 把现有的多线程并行扩展到 GPU 等加速设备；
- 探索热–弹性、结构–静磁等耦合多物理场的分析与优化。

---

# 参考文献

[1] M. Abadi, P. Barham, J. Chen, Z. Chen, A. Davis, J. Dean, M. Devin, S. Ghemawat, G. Irving, M. Isard, et al., {TensorFlow}: A system for {Large-Scale} machine learning, in: 12th USENIX Symposium on Operating Systems Design and Implementation (OSDI 16), 2016, pp. 265–283.

[2] R. Anderson, J. Andrej, A. Barker, J. Bramwell, J.-S. Camier, J. C. V. Dobrev, Y. Dudouit, A. Fisher, T. Kolev, W. Pazner, M. Stowell, V. Tomov, I. Akkerman, J. Dahm, D. Medina, and S. Zampini, MFEM: A modular finite element methods library, *Computers & Mathematics with Applications* 81 (2021) 42–74, https://doi.org/10.1016/j.camwa.2020.06.009.

[3] M. Astaneh, J. Andric, L. Löfdahl, and P. Stopp, Multiphysics simulation optimization framework for lithium-ion battery pack design for electric vehicle applications, *Energy* 239 (2022) 122092, https://doi.org/10.1016/j.energy.2021.122092.

[4] T. Babcock, G. Bedonian, and J. E. Hicken, Multidisciplinary analysis of propulsive electric motors during takeoff, in: AIAA Scitech 2021 Forum, 2021, p. 1778, https://doi.org/10.2514/6.2021-1778.

[5] A. G. Baydin, B. A. Pearlmutter, A. A. Radul, and J. M. Siskind, Automatic differentiation in machine learning: a survey, *Journal of Machine Learning Research* 18(1) (2018) 1–43.

[6] P. D. Bello-Maldonado and P. F. Fischer, Scalable low-order finite element preconditioners for high-order spectral element Poisson solvers, *SIAM Journal on Scientific Computing* 41(5) (2019) S2–S18, https://doi.org/10.1137/18M1194997.

[7] D. Boffi, F. Brezzi, and M. Fortin, *Mixed Finite Element Methods and Applications*, Springer Berlin Heidelberg, 2013, https://doi.org/10.1007/978-3-642-36519-5.

[8] O. Burghardt, P. Gomes, T. Kattmann, T. D. Economon, N. R. Gauger, and R. Palacios, Discrete adjoint methodology for general multiphysics problems: A modular and efficient algorithmic outline with implementation in an open-source simulation software, *Structural and Multidisciplinary Optimization* 65(1) (2022) 20, https://doi.org/10.1007/s00158-021-03117-5.

[9] A. Chandrasekhar, S. Sridhara, and K. Suresh, AuTO: a framework for automatic differentiation in topology optimization, *Structural and Multidisciplinary Optimization* 64(6) (2021) 4355–4365, https://doi.org/10.1007/s00158-021-03025-8.

[10] T. W. Chin, M. K. Leader, and G. J. Kennedy, A scalable framework for large-scale 3D multimaterial topology optimization with octree-based mesh adaptation, *Advances in Engineering Software* 135 (2019) 102682, https://doi.org/10.1016/j.advengsoft.2019.05.004.

[11] S. Chinchalkar, The application of automatic differentiation to problems in engineering analysis, *Computer Methods in Applied Mechanics and Engineering* 118(1) (1994) 197–207, https://doi.org/10.1016/0045-7825(94)90113-9.

[12] G. F. Corliss, Applications of differentiation arithmetic, in: Reliability in Computing, Elsevier, 1988, pp. 127–148.

[13] M. O. Deville and E. H. Mund, Finite-element preconditioning for pseudospectral solutions of elliptic problems, *SIAM Journal on Scientific and Statistical Computing* 11(2) (1990) 311–342, https://doi.org/10.1137/0911019.

[14] T. D. Economon, F. Palacios, S. R. Copeland, T. W. Lukaczyk, and J. J. Alonso, SU2: An open-source suite for multiphysics simulation and design, *AIAA Journal* 54(3) (2016) 828–846, https://doi.org/10.2514/1.J053813.

[15] A. H. Gebremedhin and A. Walther, An introduction to algorithmic differentiation, *Wiley Interdisciplinary Reviews: Data Mining and Knowledge Discovery* 10(1) (2020) e1334, https://doi.org/10.1002/widm.1334.

[16] M. B. Giles, Collected matrix derivative results for forward and reverse mode algorithmic differentiation, in: Advances in Automatic Differentiation, Springer, 2008, pp. 35–44, https://doi.org/10.1007/978-3-540-68942-3_4.

[17] J. S. Gray, J. T. Hwang, J. R. R. A. Martins, K. T. Moore, and B. A. Naylor, OpenMDAO: an open-source framework for multidisciplinary design, analysis, and optimization, *Structural and Multidisciplinary Optimization* 59(4) (2019) 1075–1104, https://doi.org/10.1007/s00158-019-02211-z.

[18] A. Griewank and A. Walther, *Evaluating Derivatives: Principles and Techniques of Algorithmic Differentiation*, SIAM, 2008, https://doi.org/10.1137/1.9780898717761.

[19] P. He, C. A. Mader, J. R. R. A. Martins, and K. J. Maki, DAFoam: An open-source adjoint framework for multidisciplinary design optimization with OpenFOAM, *AIAA Journal* 58(3) (2020) 1304–1319, https://doi.org/10.2514/1.J058853.

[20] F. Hecht, New development in FreeFem++, *Journal of Numerical Mathematics* 20(3-4) (2012) 251–265, https://doi.org/10.1515/jnum-2012-0013.

[21] R. Hiptmair and J. Xu, Nodal auxiliary space preconditioning in H(curl) and H(div) spaces, *SIAM Journal on Numerical Analysis* 45(6) (2007) 2483–2509, https://doi.org/10.1137/060660588.

[22] G. Hou, A. Satyanarayana, and S. Tiwari, First-and second-order sensitivity analysis of finite element equations via automatic differentiation, in: 7th AIAA/USAF/NASA/ISSMO Symposium on Multidisciplinary Analysis and Optimization, 1998, p. 4764, https://doi.org/10.2514/6.1998-4764.

[23] K. Jacobson, J. Kiviaho, M. Smith, and G. Kennedy, An aeroelastic coupling framework for time-accurate analysis and optimization, in: 2018 AIAA/ASCE/AHS/ASC Structures, Structural Dynamics, and Materials Conference, 2018, p. 0100, https://doi.org/10.2514/6.2018-0100.

[24] Z. Kang and K. James, Multiphysics design of programmable shape-memory alloy-based smart structures via topology optimization, *Structural and Multidisciplinary Optimization* 65(1) (2022) 24, https://doi.org/10.1007/s00158-021-03101-z.

[25] J. E. Kim, D. S. Kim, P. S. Ma, and Y. Y. Kim, Multi-physics interpolation for the topology optimization of piezoelectric systems, *Computer Methods in Applied Mechanics and Engineering* 199(49) (2010) 3153–3168, https://doi.org/10.1016/j.cma.2010.06.021.

[26] J. Kiviaho, K. Jacobson, M. Smith, and G. Kennedy, A robust and flexible coupling framework for aeroelastic analysis and optimization, in: 18th AIAA/ISSMO Multidisciplinary Analysis and Optimization Conference, 2017, p. 4144, https://doi.org/10.2514/6.2017-4144.

[27] T. V. Kolev and P. S. Vassilevski, Parallel auxiliary space AMG solver for H(div) problems, *SIAM Journal on Scientific Computing* 34(6) (2012) A3079–A3098, https://doi.org/10.1137/110859361.

[28] B. S. Lazarov and O. Sigmund, Filters in topology optimization based on Helmholtz-type differential equations, *International Journal for Numerical Methods in Engineering* 86(6) (2011) 765–781, https://doi.org/10.1002/nme.3072.

[29] A. Logg and G. N. Wells, DOLFIN: Automated finite element computing, *ACM Transactions on Mathematical Software* 37(2) (2010) 20, https://doi.org/10.1145/1731022.1731030.

[30] K. Long, R. Kirby, and B. van Bloemen Waanders, Unified embedded parallel finite element computations via software-based Fréchet differentiation, *SIAM Journal on Scientific Computing* 32(6) (2010) 3323–3351, https://doi.org/10.1137/09076920X.

[31] Z. Lyu, G. K. Kenway, C. Paige, and J. R. Martins, Automatic differentiation adjoint of the Reynolds-averaged Navier-Stokes equations with a turbulence model, in: 21st AIAA Computational Fluid Dynamics Conference, 2013, p. 2581, https://doi.org/10.2514/6.2013-2581.

[32] D. Maclaurin, Modeling, Inference and Optimization with Composable Differentiable Procedures, Ph.D. thesis, Harvard University, 2016.

[33] D. Maclaurin, D. Duvenaud, and R. P. Adams, Autograd: Effortless gradients in NumPy, in: ICML 2015 AutoML Workshop, Vol. 238, 2015.

[34] C. A. Mader, J. R. R. A. Martins, J. J. Alonso, and E. van der Weide, ADjoint: An approach for the rapid development of discrete adjoint solvers, *AIAA Journal* 46(4) (2008) 863–873, https://doi.org/10.2514/1.29123.

[35] J. R. Martins and A. Ning, *Engineering Design Optimization*, Cambridge University Press, 2021, https://doi.org/10.1017/9781108580809.

[36] J. Melenk, K. Gerdes, and C. Schwab, Fully discrete hp-finite elements: fast quadrature, *Computer Methods in Applied Mechanics and Engineering* 190(32) (2001) 4339–4364, https://doi.org/10.1016/S0045-7825(00)00322-4.

[37] U. Naumann, *The Art of Differentiating Computer Programs: An Introduction to Algorithmic Differentiation*, SIAM, 2011, https://doi.org/10.1137/1.9781611972078.

[38] S. A. Orszag, Spectral methods for problems in complex geometries, *Journal of Computational Physics* 37(1) (1980) 70–92, https://doi.org/10.1016/0021-9991(80)90005-4.

[39] A. Paszke, S. Gross, S. Chintala, G. Chanan, E. Yang, Z. DeVito, Z. Lin, A. Desmaison, L. Antiga, and A. Lerer, Automatic differentiation in PyTorch, in: NIPS 2017 Workshop on Autodiff, 2017.

[40] A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan, T. Killeen, Z. Lin, N. Gimelshein, L. Antiga, et al., PyTorch: An imperative style, high-performance deep learning library, *Advances in Neural Information Processing Systems* 32 (2019) 8024–8035.

[41] W. Pazner, T. Kolev, and C. Dohrmann, Low-order preconditioning for the high-order finite element de Rham complex, arXiv:2203.02465 [math.NA] (2022), https://doi.org/10.48550/arXiv.2203.02465.

[42] M. Rosu, P. Zhou, D. Lin, D. M. Ionel, M. Popescu, F. Blaabjerg, V. Rallabandi, and D. Staton, *Multiphysics Simulation by Design for Electrical Machines, Power Electronics and Drives*, John Wiley & Sons, 2017, https://doi.org/10.1002/9781119103462.

[43] S. Rothe and S. Hartmann, Automatic differentiation for stress and consistent tangent computation, *Archive of Applied Mechanics* 85(8) (2015) 1103–1125, https://doi.org/10.1007/s00419-014-0939-6.

[44] M. Sagebaum, T. Albring, and N. R. Gauger, Expression templates for primal value taping in the reverse mode of algorithmic differentiation, *Optimization Methods and Software* 33(4-6) (2018) 1207–1231, https://doi.org/10.1080/10556788.2018.1471140.

[45] M. Sagebaum, T. Albring, and N. R. Gauger, High-performance derivative computations using CoDiPack, *ACM Transactions on Mathematical Software* 45(4) (2019) 39, https://doi.org/10.1145/3356900.

[46] O. Sigmund and K. Maute, Topology optimization approaches, *Structural and Multidisciplinary Optimization* 48(6) (2013) 1031–1055, https://doi.org/10.1007/s00158-013-0978-6.

[47] P. Šolín, K. Segeth, and I. Doležel, *Higher-Order Finite Element Methods*, Chapman and Hall/CRC, 2003, https://doi.org/10.1201/9780203488041.

[48] M. Stolpe and K. Svanberg, An alternative interpolation scheme for minimum compliance topology optimization, *Structural and Multidisciplinary Optimization* 22(2) (2001) 116–124, https://doi.org/10.1007/s001580100129.

[49] A. Vigliotti and F. Auricchio, Automatic differentiation for solid mechanics, *Archives of Computational Methods in Engineering* 28(3) (2021) 875–895, https://doi.org/10.1007/s11831-019-09396-y.

[50] H. G. Weller, G. Tabor, H. Jasak, and C. Fureby, A tensorial approach to computational continuum mechanics using object-oriented techniques, *Computers in Physics* 12(6) (1998) 620–631, https://doi.org/10.1063/1.168744.
