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
- **内容说明**：摘要与第 1 节为全文翻译；第 2–6 节目前为摘要式整理，**非全文翻译**。已知缺失包括式 (8) 与热传导变分形式、第 3 节 AD 文献综述与结构化微分推导（含线弹性算例）、第 4 节文献综述与 $H^1$/$H(\text{div})$/$L^2$ 基函数定义、混合 Helmholtz 预条件说明、第 5 节边界条件与参数及后处理说明、第 6 节的具体规模与未来工作细节。章节编号由原文 I–VI、A/B/C 改为阿拉伯数字。待补译。

# 摘要

耦合多物理场有限元仿真的设计优化问题由于高效计算工具开发的困难而具有挑战性。为了减轻此类障碍，我们提出了一个利用结构化自动微分的面向优化的多物理场仿真框架。通过以结构化方式实现自动微分，可以从偏微分方程（PDE）多物理场系统的弱形式中计算有限元方程的残差、无矩阵（matrix-free）雅可比–向量积（Jacobian-vector products）和伴随项。框架支持包括 $L^2$、$H^1$ 和 $H(\text{div})$ 在内的混合函数空间，允许 PDE 系统的不同分量在不同函数空间内进行数值评估。采用高阶单元的 $p$-refinement（$p$ 型网格加密）以更低的计算成本实现更高的求解精度。应用和分解（Sum-factorization）以最优的时间复杂度计算高阶单元基函数，并采用无矩阵方法（matrix-free）计算雅可比–向量积[^PA-note]。模型 PDE 问题的精度和性能研究表明，$p$-refinement 在求解效率上优于 $h$-refinement。最后，求解了线弹性与热传导的拓扑优化问题，展示了该多物理场设计与优化框架的综合能力。

[^PA-note]: 译者判断（非原文内容）：原文只称 “matrix-free Jacobian-vector products” 并以和分解实现，未使用 partial assembly（PA）一词。结合作者开源代码（`smdogroup/a2d`、`smdogroup/a2d-multiphysics` 中的 `MatrixFree` 类在积分点预存导数矩阵 `qmat`）推断其实现对应高阶有限元中的 PA；该判断未经原文证实，引用时应标注为译者推断。

# 1 引言

多物理场仿真在单一强耦合仿真中耦合了系统的多个物理层面。在复杂工程系统设计优化的背景下，多物理场数值仿真能够产生更现实的设计，因为它们捕获了孤立学科分析所忽略的耦合效应。在航空航天工程领域，相关的物理模型可能包括结构力学、结构热力学、空气动力学、声学、波动传播和电磁学。文献中有许多多物理场仿真和设计优化的例子。例如，Burghardt 等人 [8] 提出了一种针对流体、热和结构问题的通用的基于梯度的多物理场优化方法；Babcock 等人 [4] 对电动机进行了静磁–热耦合分析；Kim 等人 [25] 对涉及力学、电学和机电分析的压电系统进行了多物理场拓扑优化；Kang 和 James [24] 考虑了非线性热机械效应对形状记忆合金进行了拓扑优化；Rosu 等人 [42] 针对电机设计提出了电磁、热和力学耦合的多物理场仿真；Economon 等人 [14] 开发了 SU2，用于求解非结构网格拓扑上的 PDE 多物理场问题；Astaneh 等人 [3] 通过耦合电化学和热模型在电池开发中执行基于仿真的设计优化。

广泛采用多物理场仿真的一个障碍是物理模型的正向和灵敏度分析需要大量的开发工作和计算时间。用于多物理场仿真的计算框架可分为两类：单整框架（monolithic frameworks，将所有分析紧密集成到单一系统中）和异构方法（heterogeneous methods，利用多种离散、代码和求解策略）。紧密集成框架的例子包括 FreeFEM [20]、MFEM [2]、FEniCS/DOLFIN [29]、Sundance [30] 和 SU2 [14]，而异构框架的例子包括多学科耦合问题，如 OpenMDAO [17] 和 FUNtoFEM [23, 26]。在这项工作中，我们专注于紧密集成的方法，依靠有限元方法进行底层离散。这种方法的一个关键挑战是在所提出的框架内实现多个物理模型的额外负担。对于受非线性偏微分方程控制的物理问题，这一障碍十分显著，手工形成线性化既耗时又容易出现人为错误。为了应对上述挑战并简化多物理场分析和优化的开发过程，我们提出了一种用于求解具有有限元方法的线性和非线性偏微分方程的结构化微分框架。

通过以结构化的方式利用自动微分技术来获得离散化中的关键项，可以减少开发多物理场问题分析代码的工作量，而不会牺牲多物理场框架的计算性能和效率。

# 2 多物理场问题列式

在本节中，我们描述了多物理场问题控制方程的变分形式，并给出了几个算例。

## 2.1 控制方程

多物理场问题的控制方程采用有限元法进行离散。利用 Galerkin 方法，近似解 $u_h \in V_h$ 满足控制方程的半线性变分形式：
$$
R(x_h, u_h, v_h) = 0, \quad \forall v_h \in V_h \tag{1}
$$
其中给定设计变量 $x_h \in X_h$，$V_h$ 是适当的有限维函数空间。在控制变分陈述 (1) 中，半线性形式关于测试函数参数 $v_h$ 是线性的，关于解参数 $u_h$ 和设计变量 $x_h$ 可能是非线性的。一旦获得解 $u_h$，就可以评估感兴趣的泛函，使得 $f(x_h, u_h)$ 可以在优化问题的背景下用作目标或约束。为了简化表述，我们重点关注半线性形式 (1) 仅为全域积分而不包含边界积分的情形。

在有限元网格上使用数值积分公式计算半线性形式：
$$
R_h(x_h, u_h, v_h) = \sum_{K \in \mathcal{T}_h} \sum_{q \in Q_K} w_q |\det J_q| I_h(x_h|_q, u_h|_q, v_h|_q) \tag{2}
$$
其中计算域 $\Omega$ 划分为单元 $K \in \mathcal{T}_h$ 使得 $\bigcup_{K \in \mathcal{T}_h} K = \Omega$，$Q_K$ 是单元 $K$ 上的积分点集合，$w_q$ 是积分权重，$\det J_q$ 是单元几何变换的雅可比行列式，$I_h$ 是控制方程变分形式的离散化被积函数。

控制方程的离散形式、雅可比矩阵以及基于伴随的梯度计算所需项，是通过对被积函数 $I_h$ 关于测试函数 $v_h$、试探解 $u_h$、设计变量 $x_h$ 及其梯度、散度或旋度等微分算子求导获得的：
- 离散残差：对 $I_h$ 关于测试函数参数 $v_h$ 及其微分算子求一阶导数；
- 雅可比矩阵：对 $I_h$ 关于测试函数 $v_h$ 及其微分算子求一阶导，再关于试探解 $u_h$ 及其微分算子求二阶混合导数；
- 伴随向量积：令试探函数等于伴随变量 $v_h = \psi_h$，对设计变量 $x_h$ 求导。

我们不采用手工推导这些导数，而是实现了一种结构化自动微分方法（Structured Differentiation）在积分点级别直接求导（见第 3.1 节）。该方法完全局限于网格积分点上计算的物理量，与计算 $x_h, u_h, v_h$ 所采用的单元基函数无关。

## 2.2 势能问题

在许多力学问题中，控制方程可直接从驻值原理（如总势能驻值原理）导出。总势能通常写为全域积分：
$$
\Pi_h(x_h, u_h) = \sum_{K \in \mathcal{T}_h} \sum_{q \in Q_K} w_q |\det J_q| \pi_h(x_h|_q, u_h|_q) \tag{3}
$$
通过令势能的一阶变分等于零，得到变分方程：
$$
\delta \Pi_h(x_h, u_h, \delta u_h) = \sum_{K \in \mathcal{T}_h} \sum_{q \in Q_K} w_q |\det J_q| \delta \pi_h(x_h|_q, u_h|_q, \delta u_h|_q) = 0, \quad \forall \delta u_h \in V_h \tag{4}
$$
只要令 $R_h(x_h, u_h, v_h) = \delta \Pi_h(x_h, u_h, v_h)$ 并定义 $I_h = \delta \pi_h$，便可直接转化为半线性形式 (2)。此时构造雅可比所需的导数正是能量密度 $\pi_h$ 关于解变量 $u_h$ 及其微分算子的二阶导数。

## 2.3 多物理场算例

### 2.3.1 热传导
采用 RAMP 材料惩罚模型的稳态导热方程：
$$
-\nabla \cdot \left( \kappa_0 \frac{x}{1 + q(1-x)} \nabla u \right) = g, \quad u|_{\Gamma_0} = 0, \quad n \cdot \nabla u|_{\Gamma_1} = 0
$$
变分被积函数为：
$$
I_h(x_h, u_h, v_h) = \kappa_0 \frac{x_h}{1 + q(1-x_h)} \nabla_h u_h \cdot \nabla_h v_h - v_h g \tag{5}
$$
其关于 $\nabla_h v_h$ 与 $\nabla_h u_h$ 的混合二阶导数为：
$$
\frac{\partial^2 I_h}{\partial \nabla_h v_h \partial \nabla_h u_h} \cdot \nabla_h p_h = \kappa_0 \frac{x_h}{1 + q(1-x_h)} \nabla_h p_h
$$
关于设计变量 $x_h$ 的伴随导数为：
$$
\frac{\partial I_h}{\partial x_h} = \kappa_0 \frac{1+q}{(1 + q(1-x_h))^2} \nabla_h u_h \cdot \nabla_h \psi_h
$$

### 2.3.2 拓扑优化 Helmholtz 滤波
Helmholtz PDE 用于拓扑优化中的长度尺度控制以实现网格无关解：
$$
\rho - r_0^2 \nabla^2 \rho = x, \quad n \cdot \nabla u|_{\partial \Omega} = 0 \tag{6}
$$
引入通量 $\sigma = -r_0 \nabla \rho$，建立混合形式：
$$
\begin{aligned}
\rho + r_0 \operatorname{div}(\sigma) - x &= 0 \\
\sigma + r_0 \nabla \rho &= 0
\end{aligned} \tag{7}
$$
其中 $\rho \in L^2(\Omega)$，$\sigma \in H_0(\operatorname{div}, \Omega)$。弱混合形式的被积函数为：
$$
I_h(x_h, (\rho_h, \sigma_h), (\eta_h, \tau_h)) = \sigma_h \cdot \tau_h - r_0 \operatorname{div}_h(\tau_h) \rho_h - r_0 \operatorname{div}_h(\sigma_h) \eta_h - \rho_h \eta_h + x_h \eta_h \tag{9}
$$

### 2.3.3 拓扑优化线弹性
三维各向同性线弹性问题，位移场 $u_h \in [H^1(\Omega)]^3$。应变张量 $E = \frac{1}{2}(\nabla_h u_h + \nabla_h u_h^{\mathsf T})$，柯西应力 $S = 2\mu E + \lambda \operatorname{tr}(E) I$。应变能密度函数为：
$$
\pi_h(x_h, u_h) = \frac{1}{2} \frac{x_h}{1 + q(1-x_h)} \operatorname{tr}(S E) \tag{10}
$$
对 $\pi_h$ 关于 $\nabla_h u_h$ 求一阶和二阶导数分别得到离散残差和切线刚度（雅可比矩阵）。

# 3 自动微分

自动微分（AD）通过基本算术运算、内建函数的偏导表达式和微积分链式法则，在计算机代码中精确高效地计算导数。分为前向模式（Forward mode，按输入逐列计算）与反向模式（Reverse mode，按输出逐行计算）。常见实现方式包括源码转换（Source transformation）与运算符重载（Operator overloading）。

## 3.1 面向多物理场仿真的结构化自动微分

结构化微分（Structured Differentiation）的目标是高效、高精度地在单元积分点上计算物理量的导数：
1. **积分点级密集小矩阵/向量运算**：基于 Giles [16] 的方法在积分点级别为小规模稠密矩阵和向量运算实现一阶与二阶微分；
2. **反向模式栈**：用户管理反向模式调用栈，具备灵活性以避免对被动变量（passive variables）求导；
3. **二阶导数（Hessian-vector products）计算流程**：
   对于标量函数 $f(y(x)): \mathbb{R}^n \to \mathbb{R}$，沿任意方向 $\dot{x} \in \mathbb{R}^n$ 的 Hessian–向量积为：
   $$
   \frac{\partial^2 f}{\partial x_i \partial x_j} \dot{x}_j = \frac{\partial^2 f}{\partial y_k \partial y_l} \frac{\partial y_k}{\partial x_i} \frac{\partial y_l}{\partial x_j} \dot{x}_j + \frac{\partial f}{\partial y_k} \frac{\partial^2 y_k}{\partial x_i \partial x_j} \dot{x}_j
   $$
   定义前向切向量 $\dot{y}_j = \frac{\partial y_j}{\partial x_i} \dot{x}_i$，以及二阶变量 $\hat{y}_i = \frac{\partial^2 f}{\partial y_i \partial y_j} \dot{y}_j$ 和 $\hat{x}_i = \frac{\partial^2 f}{\partial x_i \partial x_j} \dot{x}_j$，则 Hessian–向量积可写为：
   $$
   \hat{x}_i = \hat{y}_k \frac{\partial y_k}{\partial x_i} + \bar{y}_k \frac{\partial^2 y_k}{\partial x_i \partial x_j} \dot{x}_j
   $$
   该算法包含三次扫描：
   - 首先执行一次**反向 AD 扫描**计算一阶导数 $\bar{y}$；
   - 接着执行一次**前向 AD 扫描**计算切向量 $\dot{y}$；
   - 最后执行一次**反向 AD 扫描**累积得到 Hessian 向量积 $\hat{x}$。
   其总内存开销仅约为原始被积函数计算代码的 4 倍。
4. **二阶导数的两种应用途径**：
   - 直接用于 Krylov 迭代中单次 Jacobian–向量积的实时计算；
   - 或构造积分点处的雅可比矩阵。（译者注：原文仅称二阶导数可用于单次矩阵–向量积或构造积分点处的雅可比矩阵；对应代码 `MatrixFree::initialize` 及“PA 模式”的说法为译者推断，见摘要脚注。）

# 4 高阶有限元离散

高阶有限元（$p$-FEM）能够以更低的自由度达到更高的精度。然而，朴素高阶有限元装配具有 $\mathcal{O}(p^{3d})$ 的极其高昂的计算复杂度。Orszag [38] 提出了基于张量积插值的和分解（Sum-Factorization）方法，将雅可比–向量积的复杂度降低到理论最优的 $\mathcal{O}(p^{d+1})$。

## 4.1 高阶有限元基

三维六面体单元参考域 $\hat{K} = [-1, 1]^3$。微分映射 $K = F(\hat{K})$，雅可比矩阵 $J(\hat{x}) = \nabla F(\hat{x})$。
- **$H^1$ 空间基**：在参考单元上采用 Gauss–Legendre–Lobatto（GLL）节点的 Lagrange 插值多项式张量积构造；
- **$H(\text{div})$ 空间基**：构造方向向量基，并通过 Piola 变换映射到物理单元：
  $$
  u_h(x) = \frac{1}{\det J} J \hat{u}_h(\hat{x}), \quad \operatorname{div}_h u_h(x) = \frac{1}{\det J} \operatorname{div}_{\hat{K}} \hat{u}_h(\hat{x})
  $$
- **$L^2$ 空间基**：采用 Gauss–Legendre 点构建张量积基。

## 4.2 代数多重网格预条件子

![[Fu2023_Fig1.png]]

<center><b>
图 1：二维四边形单元上 $H^1$、$H(\operatorname{div})$ 和 $L^2$ 基函数的自由度示意以及低阶预条件网格剖分：（a）$H^1(\hat{K}), p=5$；（b）$H(\operatorname{div}, \hat{K}), p=5$；（c）$L^2(\hat{K}), p=4$；（d）低阶预条件网格剖分
</b></center>

为构造有限元问题的低阶预条件子：
- **低阶离散（Low-order preconditioner）**：沿 Gauss–Legendre–Lobatto 网格剖分高阶六面体单元，形成低阶离散；
- **装配与求解**：在低阶网格上装配稀疏低阶矩阵 $K_1$，并对其应用平滑聚合代数多重网格（Smoothed Aggregation AMG）作为全阶 Matrix-Free 高阶问题 $K$ 的预条件子；
- **谱分析与条件数检验**：
  广义特征值问题：
  $$
  K v = \lambda K_1 v \tag{11}
  $$
  对扭曲单元进行谱分析表明，条件数 $\kappa(K_1^{-1} K)$ 随阶数 $p$ 和畸变比（Aspect Ratio, AR）仅适度增长，在 Poisson 问题中小于 60，在线弹性问题中小于 160，在未畸变单元（$\text{AR}=1$）下分别小于 25 和 40，验证了低阶 AMG 预条件子的有效性。

![[Fu2023_Fig2.png]]

<center><b>
图 2：用于谱分析研究的具有变化长宽比 $\text{AR} = b/a$ 和多项式阶数 $p$ 的畸变六面体单元（图中 $\text{AR} = 8, p = 10$）
</b></center>

![[Fu2023_Fig3.png]]

<center><b>
图 3：随着多项式阶数和单元几何长宽比变化的条件数 $\kappa(K_1^{-1} K)$：（a）泊松问题雅可比矩阵的条件数；（b）线弹性问题雅可比矩阵的条件数
</b></center>

## 4.3 精度与可扩展性研究

在球体域上对具有解析解的 Poisson 方程（$-\nabla^2 u = r^4$）进行了精度与可扩展性验证（$p = 1 \sim 10$）：
- 相同自由度下，$p$-refinement 的误差下降速率显著快于全局 $h$-refinement；
- 预条件共轭梯度法（PCG）的求解时间与自由度数呈现完美的线性可扩展性（斜率 slope = 1），证明了 Sum-Factorization 与低阶 AMG 的高效性。
- 对混合形式 Helmholtz 问题也展示了 $p=1, 2, 3$ 的收敛性。

![[Fu2023_Fig4.png]]

<center><b>
图 4：多项式阶数 $p = 10$ 的球体网格剖面示意
</b></center>

![[Fu2023_Fig5.png]]

<center><b>
图 5：泊松问题的精度与可扩展性研究：（a）不同多项式阶数下作为未知量数函数的解误差 $\|u - u^*\|_2$；（b）不同多项式阶数下作为求解时间函数的解误差 $\|u - u^*\|_2$
</b></center>

![[Fu2023_Fig6.png]]

<center><b>
图 6：泊松问题在不同多项式阶数下求解时间随未知量数的变化
</b></center>

![[Fu2023_Fig7.png]]

<center><b>
图 7：混合 Helmholtz 问题的精度研究：不同多项式阶数（$p=1, 2, 3$）下解误差 $\|u - u^*\|_2$ 随未知量数的变化曲线
</b></center>

# 5 结果

## 5.1 散热器拓扑优化

目标函数为最小化热顺应性（在体积分数上限 $V_0 = 0.4V$ 下）：
$$
\begin{aligned}
\min_x \quad & \int_{\Omega} u g \, \mathrm{d}\Omega \\
\text{s.t.} \quad & 0 \le x \le 1, \quad \int_{\Omega} x \, \mathrm{d}\Omega \le V_0 \\
& -\nabla \cdot \left( \kappa_0 \frac{x}{1+q(1-x)} \nabla u \right) = g
\end{aligned}
$$

![[Fu2023_Fig8.png]]

<center><b>
图 8：导热散热问题的设计域与网格示意（单元多项式阶数 $p = 9$）
</b></center>

采用 300 次 MMA 迭代优化。为了在阶数提升时保持全局自由度总数恒定（约 53 万～61 万），单元阶数从 $p=2$ 增加至 $p=9$，同时相应减少单元总数。滤波采用 Bernstein 多项式投影。

![[Fu2023_Fig9.png]]

<center><b>
图 9：采用不同多项式阶数有限元基的热传导问题拓扑优化结果：（a）$p = 2$，自由度 $531,441$；（b）$p = 3$，自由度 $570,775$；（c）$p = 4$，自由度 $531,441$；（d）$p = 5$，自由度 $531,441$；（e）$p = 6$，自由度 $548,887$；（f）$p = 7$，自由度 $563,550$；（g）$p = 8$，自由度 $611,585$；（h）$p = 9$，自由度 $532,900$
</b></center>

## 5.2 最小化结构柔度拓扑优化

线弹性结构柔度最小化：
$$
\begin{aligned}
\min_x \quad & \int_{\Omega} \pi(x, u) \, \mathrm{d}\Omega \\
\text{s.t.} \quad & 0 \le x \le 1, \quad \int_{\Omega} x \, \mathrm{d}\Omega \le V_0 \\
& \delta \Pi(x, u, \delta u, f) = 0, \quad \forall \delta u
\end{aligned} \tag{12}
$$
研究了两个算例：
1. **三维悬臂梁弯曲问题**：全局自由度控制在约 142 万～148 万，测试阶数 $p = 2, 3, 4, 5, 7, 8, 9, 10$；
2. **空心圆柱受扭转载荷问题**：全局自由度控制在约 104 万，测试阶数 $p = 2, 4, 5, 7, 10$。

![[Fu2023_Fig10.png]]

<center><b>
图 10：三维悬臂梁弯曲问题的计算域与网格示意（单元多项式阶数 $p = 10$）
</b></center>

![[Fu2023_Fig11.png]]

<center><b>
图 11：三维空心受扭圆柱问题的计算域与网格示意（单元多项式阶数 $p = 10$）
</b></center>

图 12 表明，随着 $p$ 增加，侧部和中部连接上下两面的杆件逐渐缩小并最终消失；与热传导问题类似，随 $p$ 增加开始出现周期性齿状伪影。这类网格依赖伪影源于在 Bernstein 多项式张成的设计空间中进行优化，可通过显式滤波加以改善。另一方面，空心圆柱问题的优化设计在不同多项式阶数下保持一致。

![[Fu2023_Fig12.png]]

<center><b>
图 12：采用不同多项式阶数有限元基的悬臂梁拓扑优化结果：（a）$p=2$，自由度 $1,469,061$；（b）$p=3$，自由度 $1,484,679$；（c）$p=4$，自由度 $1,486,875$；（d）$p=5$，自由度 $1,423,053$；（e）$p=7$，自由度 $1,456,920$；（f）$p=8$，自由度 $1,454,355$；（g）$p=9$，自由度 $1,460,730$；（h）$p=10$，自由度 $1,423,053$
</b></center>

![[Fu2023_Fig13.png]]

<center><b>
图 13：采用不同多项式阶数的空心受扭圆柱拓扑优化结果：（a）$p = 2$，自由度 $1,041,984$；（b）$p = 4$，自由度 $1,041,984$；（c）$p = 5$，自由度 $1,045,440$；（d）$p = 7$，自由度 $1,064,448$；（e）$p = 10$，自由度 $1,037,520$
</b></center>

# 6 结论

本文提出了一种基于结构化自动微分的面向优化的高阶多物理场有限元框架：
1. 采用结构化自动微分技术在积分点级别自动化生成非线性多物理场 PDE 离散的残差、Jacobian 向量积与伴随灵敏度；
2. 支持 $H^1, H(\text{div}), L^2$ 等多种函数空间的高阶混合离散；
3. 采用和分解（Sum-Factorization）实现最优计算复杂度的无矩阵雅可比–向量积；
4. 构造了基于 GLL 节点低阶等效网格的代数多重网格（AMG）预条件子；
5. 在 3D 散热与线弹性拓扑优化中展示了高达 $p=10$、上百万自由度的优化计算能力。未来工作包括混合元更高效的预条件子、向 GPU 异构加速扩展等。

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
