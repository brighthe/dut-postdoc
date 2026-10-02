---
title: "翻译：Efficient large-scale 3D topology optimization with matrix-free MATLAB code"
tags:
  - translation
  - topology-opt
  - matrix-free
  - multigrid
  - matlab
status: "read" # draft | read | done
date_created: 2026-09-24
date_updated: 2026-09-24
source: "../sources/Wang2025-top3d-xl-matrix-free-matlab.pdf"
citekey: "Wang2025-top3d-xl-matrix-free-matlab"
language: "zh-CN"
---

# Efficient large-scale 3D topology optimization with matrix-free MATLAB code

---

# 信息

- **中文标题**：基于 matrix-free MATLAB 代码的高效大规模三维拓扑优化
- **作者**：Junpeng Wang（王俊鹏）$^{1,*}$；Niels Aage$^2$；Jun Wu（吴俊）$^3$；Ole Sigmund$^2$；Rüdiger Westermann$^1$（Niels Aage、Ole Sigmund、Rüdiger Westermann 中文名待确认）
- **单位**：
  - $1$: 慕尼黑工业大学计算机图形与可视化（Computer Graphics and Visualization）（德国慕尼黑）[^单位1]
  - $2$: 丹麦技术大学土木与机械工程系（丹麦 Kongens Lyngby）
  - $3$: 代尔夫特理工大学可持续设计工程系（荷兰代尔夫特）
- **期刊**：*Structural and Multidisciplinary Optimization*
- **文章类型**：Educational paper
- **卷 / 文章号**：68: 174
- **DOI**：https://doi.org/10.1007/s00158-025-04127-3
- **收稿 / 修回 / 录用 / 在线发表**：2025-05-16 / 2025-07-16 / 2025-08-19 / 2025-09-06
- **通讯作者**：Junpeng Wang（junpeng.wang@tum.de）

[^单位1]: 原文单位名印作 “Computer Graphics and Visualzation”，拼写照原文存疑，此处按 Visualization 理解。

# 摘要

本文提出了一种用于三维大规模基于密度的拓扑优化（TO）以及多孔填充优化（PIO）的高效 MATLAB 框架。该框架在同等模拟规模下展现出与既有 MATLAB 实现相当的计算效率，并且能够在配备 64 GB 内存的标准个人计算机（PC）上支持高达 1.28 亿六面体模拟单元的超大规模模型。此外，它能够处理任意非长方体设计域，且不要求单元空间分辨率满足 2 的幂次方倍率限制。为了实现这一目标，技术贡献主要集中在线弹性静力有限元法（FEM）线性方程组的求解上。本文提出了一种定制的基于单元的无矩阵（element-based matrix-free）计算模板，以规避大规模有限元中巨大的内存消耗；通过充分利用 MATLAB 内置的高效矩阵–向量运算和索引功能，保证了其计算效率。进一步地，我们通过非二进 Galerkin 粗化（non-dyadic Galerkin coarsening）和对角松弛（diagonal relaxation）方案，提升了 MATLAB 实现的几何多重网格方法（geometric multigrid method）的计算效率并降低了内存开销。全部代码均在开源代码仓库公开：https://github.com/PSLer/TOP3D_XL。

**关键词**：拓扑优化（Topology optimization）；多孔填充（Porous infill）；多重网格方法（Multigrid method）；Matrix-free（Matrix-free）

# 1 结果复现

所有关键细节均已在本文中阐述，并已包含在相关联的代码仓库中。文中的所有结果均可据此复现。

# 2 引言

拓扑优化（TO）是一种获取满足预定义目标与约束的优化结构的通用工具。其中最简单且被最广泛研究的问题是线弹性结构的柔顺度最小化。在此类问题中，目标是在满足可用材料量约束的前提下，最大化结构抵抗外力的刚度。在其基础形式中，基于密度的拓扑优化在设计域的一阶有限元离散上运行以计算柔顺度，这需要求解一个大型稀疏线性方程组 $\boldsymbol{K}\boldsymbol{U} = \boldsymbol{F}$，其中全局刚度矩阵 $\boldsymbol{K}$ 是在各向同性材料本构假设下由各个单元刚度矩阵组装而成的。单元灵敏度在每次迭代中根据柔顺度和材料消耗的导数，决定哪些单元应该增加或减少材料，从而迭代地指导材料分布。[^章节编号]

在以往的工作中，学者们提出了面向教学目的（见 Wang 等 2021 年的综述）或面向并行计算架构追求最高性能与模型分辨率的 MATLAB 及高性能拓扑优化实现。对于基于 CPU 的并行实现，可参见（Borrvall and Petersson 2001; Evgrafov et al. 2008; Aage et al. 2015; Liu et al. 2018; Lin et al. 2022; Wu et al. 2024）；对于 GPU 加速方法，可参见（Wadbro and Berggren 2009; Schmidt and Schulz 2011; Challis et al. 2014; Martínez-Frutos et al. 2015; Wu et al. 2016; Herrero-Pérez and Castejón 2021; Träff et al. 2023）。教学代码在模型分辨率上通常显著落后于性能优化方案，这主要是由于教学代码显式表示了庞大的刚度矩阵 $\boldsymbol{K}$。性能优化的代码则通过在 CPU 和 GPU 上高效实现（基于节点的）matrix-free 表示来获得极高的模型分辨率。结合用于求解结构位移响应的多重网格求解器，研究人员已经开发出了高效的拓扑优化系统。然而，这通常需要精细的调优以及针对特定计算机系统的适配，使得非专家用户难以理解这些代码。为了进一步提升性能，代码中通常还会固化额外的模型限制，例如沿不同坐标轴方向的有限元数量呈 2 的幂次方倍率，或者设计域必须为填满的长方体（Mukherjee et al. 2021）。

本研究的动机在于证明：采用纯 MATLAB 实现的教学代码可以在避免苛刻模型约束的同时，显著缩小与性能优化实现在模型分辨率和计算速度上的差距。图 1 展示了这一差距，并展示了通过精心重构计算模块以充分利用 MATLAB 核心特性及常用优化技术所能达到的性能。

![[Wang2025_Fig1.png]]

<center><b>
图 1：近期 MATLAB 教学拓扑优化代码（Ferrari and Sigmund 2020，蓝色曲线）和（Amir et al. 2014，绿色曲线）在配备 64 GB 内存的 6 核 CPU 台式机系统上的性能统计，测试直至该系统支持的最高可能分辨率。这两种代码均显著限制了可求解的分辨率，且要求三维模拟网格的空间分辨率呈 2 的幂次方倍率。借助本文提出的 MATLAB 代码（红色曲线），模拟分辨率得到了显著提升，同时保持了多重网格方法关于模拟单元数的线性时间复杂度。红色虚线对应于使用物理上固定、独立于网格分辨率的滤波半径时的性能统计。
</b></center>

为此，我们引入了一种基于单元的 matrix-free 格式，该格式特别适合执行 MATLAB 所擅长的高效矩阵–向量运算。该方法彻底消除了组装全局刚度矩阵 $\boldsymbol{K}$ 的需要。此外，我们针对求解大型线性方程组的几何多重网格求解器提出了针对性适配，以进一步降低内存占用并提高计算效率（Peetz and Elbanna 2021; Herrero-Pérez and Picó-Vicente 2023）。我们展示了如何利用这些优化来提升经典拓扑优化及其局部体积约束变体——多孔填充优化（porous infill optimization, PIO，Wu et al. 2018; Dou 2020）的计算性能。PIO 能够生成仿生多孔骨架结构，并已被拓展至多材料设计（Li et al. 2020）、纤维增强结构设计（Li et al. 2021）以及梯度多孔结构生成（Schmidt et al. 2019）。此类错综复杂的多孔内部构型严重阻碍了几何多重网格求解器的收敛性，正好可用于严格验证本框架的稳健性。

本文余下部分的结构安排如下：第 2 节简要回顾拓扑优化与多孔填充优化的数学模型；第 3 节详细描述几何多重网格方法的改进细节；第 4 节介绍基于单元的 matrix-free 格式；第 5 节与第 6 节分别阐述实现细节与数值验证结果；最后在第 7 节对全文进行总结。

[^章节编号]: 原文章节标题将“Replication of results”编为第 1 节，引言为第 2 节；但正文中的章节交叉引用（引言末段的文章结构说明、第 3 节“Sect. 4”指 PDE 过滤、4.2 节“see Sect. 4”与“In Sect. 6”、第 5 节“As discussed in Sect. 3”、第 7 节“as discussed in Sect. 4”）均比标题编号小 1，即按不计第 1 节的编号书写。译文标题保留原文编号，正文引用照原文转录，阅读时需加 1 对应。

# 3 拓扑优化

针对各向同性线弹性问题的基于密度的拓扑优化数学模型定义如下：

$$
\min_{\boldsymbol{\rho}} \quad c = \frac{1}{2}\boldsymbol{U}^{\mathrm{T}}\boldsymbol{K}(\boldsymbol{\rho})\boldsymbol{U},
\tag{1}
$$

$$
\text{s.t.} \quad \boldsymbol{K}\boldsymbol{U} = \boldsymbol{F},
\tag{2}
$$

$$
g(\boldsymbol{\rho}) \le 0,
\tag{3}
$$

$$
\rho_e \in [0.0,\ 1.0],\ \forall e.
\tag{4}
$$

其中 $c$ 为柔顺度，$\boldsymbol{F}$ 和 $\boldsymbol{U}$ 分别为外力载荷向量与位移向量。$\boldsymbol{K}$ 表示依赖于伪密度场 $\boldsymbol{\rho}$ 的全局刚度矩阵，$\rho_e$ 为单元 $e$ 的材料密度，向量 $\boldsymbol{\rho}$ 包含所有单元的密度变量。不等式约束 $g(\boldsymbol{\rho}) \le 0$ 可表示全局或局部材料体积约束。为避免数值不稳定性（如棋盘格和网格依赖性），在优化过程中通常引入过滤和投影操作：

$$
\begin{aligned}
\tilde{\boldsymbol{\rho}} &= \mathcal{F}(\boldsymbol{\rho}, r) \\
\bar{\boldsymbol{\rho}} &= \mathcal{P}(\tilde{\boldsymbol{\rho}}, \beta, \eta) \\
E_e(\bar{\rho}_e) &= E_{\min} + \bar{\rho}_e^{\gamma}(E_0 - E_{\min})
\end{aligned}
\tag{5}
$$

这里，$\mathcal{F}$ 和 $\mathcal{P}$ 分别代表平滑滤波算子（滤波半径为 $r$）和投影算子。投影算子由阈值 $\eta$ 和平滑 Heaviside 参数 $\beta$ 参数化。材料插值采用固体各向同性材料惩罚模型（SIMP），其中 $E_0$ 和 $E_{\min}$ 分别代表实体材料和微小空相的杨氏模量，$\gamma$ 为惩罚因子（通常取 $\gamma = 3$），$E_e$ 为单元 $e$ 对应的有效杨氏模量。在全局体积约束下，不等式约束定义为

$$
g(\boldsymbol{\rho}) = \frac{\sum \bar{\rho}_e}{N_e V_0} - 1 \le 0
\tag{6}
$$

其中 $N_e$ 为单元总数，$V_0$ 为预先指定的整体体积比上限。对于多孔填充优化（PIO），约束形式修改为局部体积约束：

$$
\begin{aligned}
g(\boldsymbol{\rho}) &= \frac{\left(\dfrac{1}{N_e}\sum_{i=1}^{N_e}\hat{\rho}_i^{p}\right)^{\frac{1}{p}}}{V_{e0}} - 1 \le 0, \\
\hat{\rho}_e &= \frac{\sum_{j\in\mathbb{N}_e}\bar{\rho}_j}{|\mathbb{N}_e|},\quad \mathbb{N}_e = \{\, j \mid \|x_j - x_e\|_2 \le R_e \,\},\ \forall e
\end{aligned}
\tag{7}
$$

在此约束下，所得结构构型演变为局部具有最大指定体积比 $V_{e0}$ 的多孔填充结构。式 (7) 的原始形式包含 $N_e$ 个约束函数，直接求解极其繁琐。为此，利用 $p$-范数函数将所有约束凝聚为一个单一的可微表达式，如式 (7) 所示，在本文的数值算例中取 $p = 16$。局部体积的计算亦可重新表述为一个 PDE 滤波器，如 Träff 等（2021）所示。

本框架同时支持全局和局部体积约束。这不仅满足了多样的功能需求，而且由于两类约束所形成的密度场在材料异质性（heterogeneity）上存在剧烈差异，能够进一步验证本文提出的线性方程组求解器的稳健性与通用性。这是因为介质的异质性程度对几何多重网格方法的收敛行为起着决定性作用（Fish and Belsky 1995; Erlangga et al. 2006; Liu et al. 2020）。

**求解**（Solving）：求解式 (1)–(4) 对应的优化问题涉及迭代更新设计变量，以在满足约束条件的同时极小化目标函数。我们采用优化准则法（Optimality Criteria, OC）求解经典拓扑优化（TO），并采用移动渐近线法（Method of Moving Asymptotes, MMA）求解多孔填充优化（PIO）（Svanberg 1987; Träff et al. 2023; Wu et al. 2018）。出于计算兼容性考虑，我们选择 PDE 滤波器（Lazarov and Sigmund 2011），因为它与局部体积约束的施加机制完全同构（Träff et al. 2021）。

在标准基于密度的 TO 或 PIO 中，结构设计由有限元显式表达，这导致了高昂的计算开销，尤其是需要刻画细致的结构构型时。该开销主要源于每一步优化中求解大规模有限元线性系统，这对收敛性和内存占用构成了严峻挑战。被广泛采纳的高效解决方案是几何多重网格预条件共轭梯度求解器（MGCG，Amir et al. 2014），并结合面向大规模问题的 matrix-free 计算模板（Aage et al. 2015; Wu et al. 2016）。然而，其高效的纯 MATLAB 实现仍未被充分探索。以下各节将详细讨论定制的几何多重网格方法以及基于单元的 matrix-free 计算模板。

# 4 几何多重网格方法

由于其卓越的收敛性能，MGCG 被广泛用于求解 TO 与 PIO 中的有限元方程，并辅以其他性能优化，例如使用上一优化步的解向量 $\boldsymbol{U}$ 作为当前优化步的初值猜测。算法 1 给出了 MGCG 的代码执行框架。

```text
算法 1：MGCG
输入：F, U, M, \epsilon_0
输出：U
 1: r_1 = F - K * U
 2: z_1 = p_1 = \mathcal{G}(r_1)
 3: x_1 = z_1^T * r_1, f = ||F||_2
 4: for j = 1 : M do
 5:     v = K * p_j   % Matrix-free 刚度矩阵与向量乘法
 6:     \lambda_j = x_1 / (p_j^T * v)
 7:     U = U + \lambda_j * p_j
 8:     r_{j+1} = r_j - \lambda_j * v
 9:     if ||r_{j+1}||_2 < f * \epsilon_0 then break end if
10:     z_{j+1} = \mathcal{G}(r_{j+1})   % 多重网格预条件 (V-cycle)
11:     x_2 = z_{j+1}^T * r_{j+1}
12:     p_{j+1} = z_{j+1} + (x_2 / x_1) * p_j
13:     x_1 = x_2
14: end for
```

在算法 1 中，$\mathcal{G}$ 表示多重网格预条件子，即通过 V 循环由残差 $\boldsymbol{r}$ 计算修正量 $\boldsymbol{z}$。参数 $M$ 和 $\epsilon_0$ 分别控制最大迭代次数与基于残差的收敛容差。

## 4.1 V 循环

几何多重网格方法结合网格层级结构与松弛方案，递归地将细网格残差限制（restrict）到相邻的粗网格上，在粗网格求解修正量，然后将其插值（interpolate）回细网格。这一过程构成了所谓的 V 循环（V-cycle），它以残差 $\boldsymbol{r}$ 为输入并返回修正项 $\boldsymbol{z}$。算法 2 概述了 V 循环的主要计算步骤。

```text
算法 2：标准 V 循环（Standard V-cycle）
输入：r^{[l]}, l = 1, L \ge 2
输出：z^{[1]}
 1: % 限制阶段（Restriction）
 2: for l = 1 : 1 : L - 1 do
 3:     z^{[l]} = w \cdot r^{[l]} ./ D^{[l]}   % 施加平滑器（前平滑）
 4:     r^{[l]} = r^{[l]} - K^{[l]} * z^{[l]}   % 计算更新残差
 5:     r^{[l+1]} = (P^{[l+1]})^T * r^{[l]}    % 限制残差至粗网格
 6: end for
 7: 求解：K^{[L]} * z^{[L]} = r^{[L]}           % 最粗网格上直接求解
 8: % 插值修正阶段（Interpolation）
 9: for l = L - 1 : -1 : 1 do
10:     z^{[l]} = z^{[l]} + P^{[l+1]} * z^{[l+1]}   % 插值粗网格修正项并累加
11:     z^{[l]} = z^{[l]} + w \cdot (r^{[l]} - K^{[l]} * z^{[l]}) ./ D^{[l]}   % 施加平滑器（后平滑）
12: end for
```

在算法 2 中，$\boldsymbol{K}^{[l]}$、$\boldsymbol{r}^{[l]}$ 和 $\boldsymbol{z}^{[l]}$ 分别代表第 $l$ 层的系统刚度矩阵、残差向量与修正向量。层级索引 $1$ 和 $L$ 分别对应最细网格层与最粗网格层。$\left(\boldsymbol{P}^{[l+1]}\right)^{\mathrm{T}}$ 为将第 $l$ 层的残差限制到第 $l+1$ 层的限制算子（prolongation operator 的转置）。其转置算子 $\boldsymbol{P}^{[l+1]}$ 则用于将第 $l+1$ 层的修正量插值回第 $l$ 层。采用阻尼 Jacobi 平滑器消除当前细网格上的高频误差，阻尼因子 $w$ 设为 $0.65$。$\boldsymbol{D}^{[l]}$ 为矩阵 $\boldsymbol{K}^{[l]}$ 的对角线元素向量。

**层级表示**（Hierarchical representation）：由最细分辨率层级上的全局刚度矩阵 $\boldsymbol{K}^{[l=1]}$ 出发，粗网格层级上的系统矩阵通过 Galerkin 粗化公式递归计算：

$$
\boldsymbol{K}^{[l+1]} = \left(\boldsymbol{P}^{[l+1]}\right)^{\mathrm{T}}\boldsymbol{K}^{[l]}\boldsymbol{P}^{[l+1]},\quad l = 1 : L - 1.
\tag{8}
$$

![[Wang2025_Fig2.png]]

<center><b>
图 2：蓝色所示第 $l+1$ 层的一个六面体单元（$h_e^{[l+1]}$）及其在第 $l$ 层嵌套的 8 个黑色六面体单元（$[h_e]^{[l]}$）的几何示意图。
</b></center>

对于嵌套的笛卡尔网格层级，第 $l+1$ 层的每个粗单元嵌套了第 $l$ 层的 8 个细单元（见图 2），延长算子（prolongation operator）基于三线性（trilinear）有限元形函数构建。也就是说，细网格顶点处的物理量由相邻更粗网格顶点处的物理量通过三线性插值获得。对于二进层级（dyadic hierarchy），即单元尺寸从 $l$ 层到 $l+1$ 层直接翻倍，各层之间采用相同的单元延长算子，称之为单元延长算子 $\boldsymbol{P}_e$。

**边界条件**（Boundary conditions）：为了在更粗的分辨率层级上计算修正量，在最细网格顶点处指定的边界条件必须准确传递给粗网格系统矩阵。我们采用 Amir 等（2014）提出的方案来解决这一问题。具体而言，识别出全局刚度矩阵 $\boldsymbol{K}$ 中与固定自由度（fixed DOFs）对应的行列并分成两组处理：将 $\boldsymbol{K}$ 对角线上的对应条目设为 1，其余非对角条目全部清零（见图 3a），无论在优化过程中包含固定自由度的单元弹性张量是否发生更新。这样处理保证了施加边界条件后 $\boldsymbol{K}$ 的维度保持不变，从而保证了在不同层级之间传递数据时的数据对齐（data alignment）。

![[Wang2025_Fig3.png]]

<center><b>
图 3：在全局刚度矩阵（a）及涉及固定自由度的单元刚度矩阵（b）上施加边界条件。在（b）中，数字标号 1/x 表示该顶点（含该自由度）被 x 个有限元单元所共享。
</b></center>

一旦边界条件被正确施加并传递，即可通过松弛方案计算第 $2$ 到 $L-1$ 层的修正项。在最粗层级 $L$，一个维度大幅缩减的线性系统直接通过 Cholesky 分解求解。

## 4.2 多重网格预条件子

预条件化的核心目的在于提高迭代求解器在求解大型线性方程组时的收敛速率与数值稳定性。一个高效的预条件子应当在大幅减少总迭代次数的同时，保持极低的单步计算开销。在本文中，我们对标准 V 循环引入了两项定制改进，以增强其预条件性能。

**非二进 V 循环**（Non-dyadic V-cycle）：首先需要强调的是，本文方法建立在全局刚度矩阵的 matrix-free 表示之上以降低内存消耗。我们不显式组装全局矩阵，而是将其表示为独立的单元刚度矩阵集合（详见第 5 节）。这在第 1 层（$\boldsymbol{K}^{[1]}$）尤为有利，因为除 SIMP 本构（式 (5)）导出的杨氏模量缩放系数外，所有单元的刚度矩阵完全相同。因此，我们仅需存储一个单位杨氏模量下的标准单元刚度矩阵以及一个记录各单元缩放因子的向量。

然而，这一优势无法直接延伸到第 2 至第 $L$ 层的粗网格系统矩阵。在粗网格上，由于粗化投影的影响，每个粗单元的刚度矩阵各不相同，必须显式存储。这会导致极高的内存消耗，或者需要在迭代过程中实时重新组装，从而构成高分辨率几何多重网格方法的核心瓶颈。例如，在 $512^3$ 的模拟网格上，仅存储 $\boldsymbol{K}^{[2]}$ 的粗单元刚度矩阵就需要约 72 GB 内存。

为克服这一难题，我们采用了 Wu 等（2016）提出的非二进 V 循环（non-dyadic V-cycle）：在网格层级与 V 循环构建中直接跳过第 2 层，直接由第 1 层计算第 3 层上的计算模板。这种做法充分利用了几何多重网格粗化方案的灵活性——粗化率并不严格限定为 2，可以采用更大的抽取倍率。在工程实现上，该策略无缝融入了笛卡尔网格的嵌套层级结构，仅需在第 1 层与第 3 层之间构造一个新的单元延长算子 $\hat{\boldsymbol{P}}_e$。该算子与 $\boldsymbol{P}_e$ 类似，只是每个粗单元内包含了更多的细分辨率单元。

在非二进 V 循环中，由于三线性插值在跨度更大的单元上执行，最细层级的残差和插值向量精度有所下降，这可能导致 V 循环的迭代步数略微上升。然而，由于跳过了第 2 层的所有运算并降低了 V 循环初始化的开销，其单步迭代计算量和内存占用大幅降低。在第 7 节中我们证明，即使在严格的容差要求下，这种改进最终也显著缩短了总求解时间。

**对角松弛**（Diagonal relaxation）：为进一步压缩总求解时间，我们基于非二进 V 循环略去了所有中间层的矩阵–向量乘法。具体而言，我们省略算法 2 中的第 6 行，并将第 13 行简化为简单的对角松弛：

$$
\boldsymbol{z}^{[l]} = \boldsymbol{z}^{[l]} + w\,\boldsymbol{r}^{[l]} ./ \boldsymbol{D}^{[l]}
\tag{9}
$$

尽管这种处理由于在限制与插值过程中对高频与低频误差的阻尼能力较弱而使得迭代次数有所增加，但它极大地降低了单步迭代的计算成本。传统的非二进 V 循环在单次 MGCG 迭代中需要在第 1 层执行三次 $\boldsymbol{K}^{[1]}\boldsymbol{u}$ 计算，并在第 $3$ 至 $L-1$ 层分别执行两次 $\boldsymbol{K}^{[l]}\boldsymbol{u}$ 计算（参见算法 1 第 7 行，算法 2 第 6、13 行）；而所提出的改进方法在单次迭代中**仅需在最细层执行一次** $\boldsymbol{K}^{[1]}\boldsymbol{u}$ 计算（即算法 1 第 7 行）。只要由此导致的迭代步数增长不超过 2 倍，总计算时间就依然能实现净缩减。此外，内存消耗得以进一步降低，因为第 $2$ 到 $L-1$ 层的 $\boldsymbol{K}^{[l]}$ 矩阵无需再做任何存储。

我们在第 7 节（图 8 与图 9）中展示了 V 循环及其变体的收敛行为。后文中我们将这三种 V 循环实现分别记为标准 V 循环（Standard V-cycle）、非二进 V 循环（Non-dyadic V-cycle）与自适应非二进 V 循环（Adapted Non-dyadic V-cycle）。

# 5 基于单元的 matrix-free 格式

高分辨率的拓扑优化（TO）与多孔填充优化（PIO）需要极大的内存空间，这主要是由于全局刚度矩阵 $\boldsymbol{K}$ 的组装与存储所致。如第 4 节所述，$\boldsymbol{K}$ 的作用主要是执行矩阵–向量乘法（$\boldsymbol{K}\boldsymbol{u}$）以及为 V 循环计算粗层级刚度矩阵。采用 matrix-free 表达可以在无需显式组装或存储 $\boldsymbol{K}$ 的情况下完成这些运算。matrix-free 格式极大受益于 SIMP 材料模型以及笛卡尔规则网格（其中所有单元具有相同的几何形状和尺寸）。因此，所有单元共享相同的单元应变矩阵，单元刚度矩阵仅相差一个标量缩放因子：

$$
\boldsymbol{K}_e(\bar{\rho}_e) = E_e(\bar{\rho}_e)\int_{\Omega_e}\boldsymbol{B}_e^{\mathrm{T}}\boldsymbol{S}_0\boldsymbol{B}_e\,\mathrm{d}x = E_e(\bar{\rho}_e)\boldsymbol{K}_{e0},
\tag{10}
$$

其中 $\boldsymbol{K}_{e0}$ 为单位杨氏模量下的标准单元刚度矩阵，$\boldsymbol{S}_0$ 为对应的各向同性弹性张量，$\boldsymbol{B}_e$ 为单元应变–位移矩阵。借助矩阵 $\boldsymbol{K}_{e0}$ 以及存储各单元杨氏模量的向量 $[\boldsymbol{E}_e]$，第 1 层上的所有单元刚度矩阵便可完全被隐式表达。

Matrix-free 格式根据 $\boldsymbol{K}\boldsymbol{u}$ 是按节点循环还是按单元循环计算，可分为基于节点（node-based）和基于单元（element-based）两类。基于节点的方案循环遍历所有节点，通过带索引的内存寻址读取当前节点所属单元的刚度矩阵，并与该节点对应的 $3\times 1$ 位移向量相乘。我们的实验表明，在 MATLAB 中，这类索引寻址循环会导致性能急剧恶化。因此，我们转向基于单元的表示，该格式允许 MATLAB 在通用单元刚度矩阵与节点位移向量之间高效执行批处理矩阵乘法。为此，我们将各个节点的位移向量按列组织进一个单元位移矩阵中，从而充分发挥 MATLAB 内置高效矩阵运算引擎的优势。

![[Wang2025_Fig4.png]]

<center><b>
图 4：在基于单元的 matrix-free 格式下执行 $\boldsymbol{K}\boldsymbol{u}$ 的计算流程。左上方提供了传统的显式组装格式作为对比参考。$N_e$ 和 $N_D$ 分别表示单元总数和系统自由度总数。$\boldsymbol{T}$ 为存储单元–顶点连接拓扑关系的矩阵。
</b></center>

**计算 $\boldsymbol{K}\boldsymbol{u}$**（Conducting $\boldsymbol{K}\boldsymbol{u}$）：在线弹性有限元分析中，计算量最大的核心步骤是计算 $\boldsymbol{K}\boldsymbol{u}$，其中 $\boldsymbol{u}_{[N_D\times 1]}$ 存储每个网格节点的位移向量。$\boldsymbol{K}\boldsymbol{u}$ 可以拆解为一系列单元级矩阵–向量乘积 $\boldsymbol{K}_e \boldsymbol{u}_e$，其中 $\boldsymbol{u}_{e[24\times 1]}$ 存储单元 $e$ 的 8 个顶点自由度值。这些局部自由度通过利用网格拓扑连接矩阵 $\boldsymbol{T}_{[N_e\times 8]}$ 索引提取得到（对应图 4 中的 Step 1）。令 $\boldsymbol{Y} = \boldsymbol{K}\boldsymbol{u}$，$\boldsymbol{Y}_e = \boldsymbol{K}_e \boldsymbol{u}_e$，并将所有单元的 $\boldsymbol{Y}_e$ 组织为一个矩阵 $[\boldsymbol{Y}_e]_{[24\times N_e]}$。随后，按照拓扑连接列表 $\boldsymbol{T}$ 将 $[\boldsymbol{Y}_e]$ 中的条目累加写回到全局向量的对应位置即可得到 $\boldsymbol{Y}$（对应图 4 中的 Step 4）。该过程的完整 MATLAB 代码已在附录 A 中给出。

在实际实现中，为了充分利用式 (10) 的结构特性，$\boldsymbol{K}_e \boldsymbol{u}_e$ 的计算被划分为两步：首先，用标准刚度矩阵 $\boldsymbol{K}_{e0}$ 乘以 $[\boldsymbol{u}_e]$（图 4 中的 Step 2）。此时必须考虑包含固定自由度的特殊单元刚度矩阵（见图 3b）以施加狄利克雷边界条件。具体做法是用预先计算好的特殊矩阵与 $[\boldsymbol{u}_e]$ 对应列的乘积，替换 $[\boldsymbol{Y}_{e0}]$ 中的对应列。接下来，将 $[\boldsymbol{Y}_{e0}]$ 按列乘以单元杨氏模量向量 $[\boldsymbol{E}_e]$（图 4 中的 Step 3）。值得注意的是，若采用在将乘积向量投影回全局索引后再将固定自由度强制置零的简易方案，实验发现会导致迭代收敛性发生显著恶化。

![[Wang2025_Fig5.png]]

<center><b>
图 5：使用 MATLAB 显式稀疏矩阵格式（紫色柱状图）与提出的基于单元 matrix-free 格式执行 $\boldsymbol{K}\boldsymbol{u}$ 的性能对比统计。步骤 1 至 4 对应于图 4 的各个阶段。
</b></center>

图 5 对比了提出的基于单元 matrix-free 格式与 MATLAB 内置稀疏矩阵–向量乘法（`sparse`）的计算效率。测试算例为一个长方体设计域，分别离散为 $48 \times 24 \times 24$、$96 \times 48 \times 48$、$192 \times 96 \times 96$、$384 \times 192 \times 192$ 与 $768 \times 384 \times 384$ 个模拟单元。在每种工况下分别对比耗时。由于内存限制，MATLAB 显式方法在超过前三个分辨率后直接内存溢出（Out of Memory）。基于单元的 matrix-free 格式相比于 MATLAB 内置稀疏矩阵乘法慢大约一倍，但其展现出了严格关于问题规模的线性扩展性。随着分辨率的提高，图 4 中的 Step 1 和 Step 4 占总运行时间的比例显著提升，这是因为这两个步骤涉及繁重的数组索引寻址，而 MATLAB 目前在单线程中执行此类索引操作。相比之下，涉及矩阵–向量乘法的 Step 2 和 Step 3 则充分受益于 MATLAB 底层的多线程自动并行优化。

同样地，TO 和 PIO 中采用的 PDE 滤波器也能够从该 matrix-free 格式中受益。PDE 滤波通过求解 Helmholtz 型微分方程实现，在标准 FEM 离散下同样表现为线性方程组（Lazarov and Sigmund 2011）。其系统矩阵由网格各顶点的核函数装配而成，在统一滤波半径下保持恒定。我们通过图 4 所示的乘法方案迭代求解该系统。滤波操作每个节点仅包含 1 个自由度（力学问题为 3 个），且矩阵条件数极佳，因此在实际优化中滤波的计算开销完全可以忽略不计。

**粗网格计算**（Coarse grid computation）：在采用对角松弛方案后，对于 $l \in [2 : L-1]$，一旦提取了对角线元素（$\boldsymbol{D}^{[l]}$）并计算了更粗一层的 $\boldsymbol{K}^{[l+1]}$，就不再需要存储 $\boldsymbol{K}^{[l]}$。$\boldsymbol{K}^{[2]}$ 的计算依赖于 $\boldsymbol{K}^{[1]}$，但在 matrix-free 格式下 $\boldsymbol{K}^{[1]}$ 不再显式存储。为此，我们建议先由 $[\boldsymbol{K}_e^{[1]}]$ 计算单元刚度矩阵 $[\boldsymbol{K}_e^{[2]}]$，然后对于 $l > 2$ 递归计算 $[\boldsymbol{K}_e^{[l]}]$。具体而言，在每个粗网格分辨率下，$\boldsymbol{K}^{[l]}$ 均可由对应的 $[\boldsymbol{K}_e^{[l]}]$ 隐式表示；仅有最粗层 $[\boldsymbol{K}_e^{[L]}]$ 需要显式组装成全局矩阵以供 Cholesky 直接分解。我们在附录 B 中提供了从 matrix-free 格式的 $\boldsymbol{K}^{[l]}$（$l = 1 : L-1$）中提取对角项 $\boldsymbol{D}^{[l]}$ 的 MATLAB 代码。

**限制与插值**（Restriction and interpolation）：为进一步削减内存，V 循环中的限制与插值操作同样可以采用基于单元的 matrix-free 格式实现，从而无需显式组装全局延长算子（$\boldsymbol{P}^{[l]}, l = 2 : L$）。类似于计算 $\boldsymbol{K}\boldsymbol{u}$ 的策略，这些操作完全可以在单元级别独立完成。随后，将各单元的残差向量（$\boldsymbol{r}_e^{[l]}$）和修正向量（$\boldsymbol{z}_e^{[l]}$）按全局自由度索引累加投影，分别生成 $\boldsymbol{r}^{[l]}$ 和 $\boldsymbol{z}^{[l]}$。与计算 $\boldsymbol{K}\boldsymbol{u}$ 的唯一区别在于，网格顶点处的物理量由共享该顶点的所有相邻单元共同决定，因此此处需要进行平均化加权处理。

# 6 实现细节

## 6.1 非长方体设计域

在工程实际中，TO 和 PIO 的设计域往往并非填满的长方体，这意味着无法直接构建规则嵌套的网格层级。对于基于单元的多重网格求解器而言，边界上的粗单元在下一细层可能无法恰好包含 8 个有效单元，这会打破单元操作的数据对齐并削弱计算效率。为此，我们针对六面体模拟网格提出了专门的适配方案。

![[Wang2025_Fig6.png]]

<center><b>
图 6：设计域离散与层级网格构建。(a) 由闭合三角形网格给出的设计域几何边界；(b) 采用笛卡尔网格离散包围盒（橙色）；(c) 适度扩大的包围盒（紫色），以保证沿各轴向的单元数能被整除；(d) 网格多层层级结构（绿色），较粗层级上的网格边分别以橙色和品红色标示。
</b></center>

考虑由任意闭合曲面定义的三维几何域（图 6a）及其轴对齐包围盒。构建模拟网格的第一步是用笛卡尔网格离散该包围盒。几何曲面内部和外部的体素分别标记为实体（1）和虚空（0）。对应于实体体素的六面体单元被提取出来构建 FEM 模拟模型（图 6b）。

我们的第一项策略是确保对于给定的总层数 $L$ 能够成功构建嵌套网格层级：即在所有层级 $l$ 上，沿三个坐标轴的网格单元数除以 $2^l$ 必须恒为整数。这一条件可以通过在外围补充若干层虚空六面体单元极其方便地实现（图 6c）。

第二项策略解决粗层级边界单元未能包含 8 个细层实体单元的情况。为此，我们在模拟网格层级中将这些属于粗单元范围内的虚空单元同样纳入计算拓扑（图 6d）。这些附加的虚空单元被赋予零刚度，且它们所对应的孤立顶点从力学平衡求解中剔除，从而严格保持原始几何模型的力学属性。

该策略具有双重优势：首先，由于实体体素未受任何改动，它完全不引入额外的有效自由度；其次，它维持了各单元在内存中统一的计算布局，大幅简化了代码实现并保持了规整的内存访问模式。

## 6.2 内存访问优化

通过对 MGCG 求解器进行性能剖析，我们发现 Step 1（图 4）是全流程中内存占用最高的环节。在该步骤中，顶点维度的位移向量 $\boldsymbol{u}$ 需要被重构为单元维度的矩阵 $[\boldsymbol{u}_e]$，这需要占用 $24 \times 8 \times N_e$ 字节的内存（24 为每个六面体单元的自由度数，8 代表双精度浮点数字节数）。例如，在 $512^3$ 单元的模拟网格上，单单存储 $[\boldsymbol{u}_e]$ 就需要消耗 24 GB 内存。

为了避免在内存中一次性分配如此巨大的连续数据块，我们基于全局单元索引将单元划分为若干较小的单元块（chunk），确保每个分块不超过预设的目标容量。这确保了每个独立数据块均能完整容纳在可用内存中，避免了操作系统频繁的硬盘交换（paging/swap）。随后，依次对各个分块独立执行 Step 1 至 Step 4，仅读取相关的数据子集。此外，为 $[\boldsymbol{u}_e]$ 分配的内存缓冲区在处理后续分块时被反复复用。

将计算划分为按分块处理的小任务可能会轻微牺牲一部分并行峰值性能，但它显著降低了求解器对问题绝对规模的敏感度，尤其是在中端硬件配置下，从而大幅提升了模型分辨率的可扩展性。在实践中，我们发现将分块大小设置为 $10^7$ 个单元（约占用 1.8 GB 内存）能够在配备 64 GB 内存的机器上取得计算效率与规模扩展性之间的极佳平衡。

# 7 结果

下面我们从多个角度展示该 MATLAB 拓扑优化与多孔填充优化框架的性能。所有数值实验均在一台运行 Windows 系统、配备 Intel Xeon W-2235 CPU（6 核，3.8 GHz）与 64 GB 内存的台式 PC 上完成。对于共轭梯度求解器，我们设置了一个相对宽松的收敛容差 $\epsilon_0 = 10^{-3}$，已验证其在仅考虑最小柔顺度问题时能够给出高度稳定的数值解。此外，最大迭代次数 $M$ 统一设为 600（除针对极严容差 $\epsilon_0 = 10^{-12}$ 的极限验证外，日常优化步从未触发该上限）。

拓扑优化（OC）与多孔填充优化（MMA）的设计变量更新步长限制（move limit）分别设为 0.2 和 0.1。所有算例均在 MATLAB R2023b 中运行。固体材料杨氏模量和泊松比分别设为 1.0 和 0.3。在所有多孔填充（PIO）算例中，设计域最外围的两层单元均预设为被动实体单元。框架最终输出两种标准格式的文件用于下游视觉检查与工程制造：一是 STL 格式的等值面结构构型，二是 NIFTI 格式的连续三维体素密度场（后者可直接使用 Wang 等 2025 年开发的基于 WebGL 的体绘制器进行交互式观察）。

实验设置结构如下：首先利用“股骨（Femur）”与“磨牙（Molar）”模型（图 7）验证所提出的 V 循环变体；接着采用标准基准悬臂梁（Cantilever，图 10）将本框架在计算效率与模型扩展性上与现有主流 MATLAB 代码进行横向对比；最后通过“GE 支架（GE Bracket）”（图 12）展示框架对多工况载荷优化的良好支持。

![[Wang2025_Fig7.png]]

<center><b>
图 7：问题描述（a, d）及对应的拓扑优化（TO，b, e）与多孔填充优化（PIO，c, f）设计结果。绿色箭头指示载荷施加位置与方向，青色半透明区域为固定约束面。对于“Femur”和“Molar”，最高测试分辨率均设为 400，分别对应约 470 万和 820 万个有限元单元。
</b></center>

**V 循环变体比较**（Comparison of V-cycle variants）：我们在“Femur”和“Molar”上分别使用标准 V 循环（Standard V-cycle）、非二进 V 循环（Non-dyadic V-cycle）与自适应非二进 V 循环（Adapted Non-dyadic V-cycle）执行 TO（图 7b, e）与 PIO（图 7c, f）。对于 TO 仅使用平滑滤波，而对于 PIO 则同时使用平滑滤波与 Heaviside 投影（见式 (5)）。

![[Wang2025_Fig8.png]]

<center><b>
图 8：不同 V 循环实现的拓扑优化（TO）统计。(a) 各 V 循环实现在优化各步求解有限元方程所需的 MGCG 迭代次数（Femur）；(b) 各实现单步处理时间及全流程总时间（见图例，Femur）；(c) 和 (d) 分别展示“Molar”算例对应的迭代步数与时间统计。
</b></center>

![[Wang2025_Fig9.png]]

<center><b>
图 9：采用不同 V 循环实现执行多孔填充优化（PIO）的收敛统计。图表排版与图 8 保持一致。
</b></center>

图 8 展示了 TO 的性能统计。图 8a 与 8c 分别记录了“Femur”和“Molar”在各优化步中求解有限元线性系统所需的 MGCG 迭代次数，图 8b 与 8d 记录了对应的单步耗时。结果表明，标准 V 循环所需的迭代步数最少，但由于单步迭代的计算开销最高，其总处理时间最长。所提出的自适应非二进 V 循环（Adapted Non-dyadic V-cycle）尽管所需的迭代步数有所上升，但凭借极低的单步计算负荷，在单步耗时和总耗时上均取得了显著的最优性能。非二进 V 循环表现居中。

图 9 汇报了对应的 PIO 统计，进一步印证了上述结论：自适应非二进 V 循环在三种实现中取得了最短的处理耗时。

对比图 8 与图 9 还揭示了更深层次的规律：尽管有限元线性系统的规模完全相同，但在相同网格下求解 PIO 比求解 TO 需要显著更多的 MGCG 迭代次数，因而单步耗时更长。这源于 PIO 具有更高空间频率、更剧烈非均质性的材料密度分布，使得系数矩阵在几何上更加病态，严重恶化了几何多重网格求解器的收敛性。

尤为明显的是，在第 150 至 250 个优化步之间，单步迭代次数急剧攀升。这种现象通常是由持续扩大的密度场异质性与尚未衰减的大更新步长共同作用引起的。

自适应非二进 V 循环在 TO 和 PIO 中均展现了最高的计算效率，同时由于彻底无需存储第 2 到 $L-1$ 层的单元刚度矩阵，实现了最低的内存消耗。最后我们观察到，PIO 迭代曲线中的局部尖峰与光滑 Heaviside 投影中 $\beta$ 参数的延拓更新密切相关。

**计算效率**（Computational efficiency）：为客观评估本框架的计算效率，我们将其与现有的代表性开源代码进行基准对比。为确保公平性与一致性，我们将对比严格限定在 Amir 等（2014）与 Ferrari and Sigmund（2020）的 MATLAB 实现上，且聚焦于其线性系统求解模块。

Amir 等采用了显式稀疏矩阵格式的 MGCG 求解器；Ferrari 与 Sigmund 则采用了直接求解器并借助外部 C++ 程序实现高效的刚度矩阵组装。为了在高分辨率下进行公平比较，根据 Ferrari and Sigmund（2020）文中的建议，我们将 Ferrari 代码中的直接求解器替换为 Amir 的 MGCG 求解器。此时两套对比代码均通过显式 MGCG 求解大规模系统，仅在组装方式上存在差异：Ferrari 与 Sigmund（2020）通过 MATLAB 的 MEX 接口调用 C++ 代码组装，效率优于 MATLAB 原生的 `sparse()` 函数。

我们排除了与 Träff 等（2023）中基于节点的 matrix-free 代码的比较（其受制于繁重的显式循环索引，速度显著偏慢），以及 Liu and Tovar（2014）的直接求解器（在高分辨率下直接内存耗尽）。

![[Wang2025_Fig10.png]]

<center><b>
图 10：(a) 悬臂梁（Cantilever）算例问题描述；(b) 采用物理固定的独立滤波半径在不同网格分辨率下优化得到的完全一致的拓扑优化构型。
</b></center>

我们采用悬臂梁（Cantilever）作为性能基准。设计域尺寸为 $1.0 \times 0.5 \times 0.5$（图 10a），分别离散为 $48 \times 24 \times 24$（R48）、$96 \times 48 \times 48$（R96）、$192 \times 96 \times 96$（R192）、$300 \times 150 \times 150$（R300）、$384 \times 192 \times 192$（R384）、$768 \times 384 \times 384$（R768）以及 $800 \times 400 \times 400$（R800）个六面体单元。

除分辨率外，所有算例均采用完全一致的参数：材料体积分数上限 $V_0 = 0.12$，优化步数 50 步，PDE 滤波半径 $r = \sqrt{3}$ 倍单元尺寸。此外，为验证网格无关性，我们还测试了在物理空间上保持恒定绝对滤波半径的算例（图 10b），其滤波半径分别设置为：R48 为 $\sqrt{3}$，R96 为 $2\sqrt{3}$，R192 为 $4\sqrt{3}$，R300 为 $6\sqrt{3}$，R384 为 $8\sqrt{3}$，R768 为 $16\sqrt{3}$，R800 为 $17\sqrt{3}$。

图 1 给出了各方法在不同网格规模下的总运行时间统计。采用 Ferrari and Sigmund（2020）的代码时，在 R192 分辨率下组装全局刚度矩阵即发生内存溢出；而 Amir 等（2014）的代码在 R300 时因超出内存而发生崩溃（得益于 MATLAB 自动的虚拟内存硬盘交换，其支撑上限略高）。撇开内存溢出不谈，既有实现均无法直接支持类似 R300 这样的网格，因为它们强制要求各轴向分辨率呈 2 的幂次方倍率。相比之下，本文的纯 MATLAB 代码能够平稳运行直至测试的最高分辨率（R800，包含 1.28 亿有限元单元），且完美支持任意非 2 的幂次网格（如 R300）。

就计算耗时而言，Ferrari and Sigmund（2020）在 R48 和 R96 尺度上效率最高，这归功于其基于 OpenMP 加速的 C++ 组装内核。在 R48、R96 和 R192 上，本框架的计算效率与 Amir 等（2014）相当；更重要的是，本方法从 R48 一路延伸到 R800 始终保持了几乎严格的近线性计算复杂度扩展性。

<center><b>
表 1：悬臂梁（Cantilever）算例的单元数、柔顺度（c）及非离散度指标（MDN）统计。滤波半径 r 的取值表示其所跨越的单元数。
</b></center>

| 模型 | 单元数 | Ferrari et al. 2020 ($r=\sqrt{3}$) $c$ | MDN | Amir et al. 2014 ($r=\sqrt{3}$) $c$ | MDN | Ours ($r=\sqrt{3}$) $c$ | MDN | Ours $c$ | MDN | $r$ |
|---|---|---|---|---|---|---|---|---|---|---|
| R48 | 27,648 | 963.467 | 0.153 | 963.464 | 0.153 | 965.226 | 0.156 | 965.226 | 0.156 | $\sqrt{3}$ |
| R96 | 221,184 | 695.020 | 0.089 | 695.020 | 0.089 | 679.250 | 0.091 | 886.209 | 0.143 | $2\sqrt{3}$ |
| R192 | 1,769,472 | – | – | 609.529 | 0.057 | 591.716 | 0.057 | 866.852 | 0.140 | $4\sqrt{3}$ |
| R300 | 6,750,000 | – | – | – | – | 566.538 | 0.043 | 843.392 | 0.135 | $6\sqrt{3}$ |
| R384 | 14,155,776 | – | – | – | – | 555.891 | 0.036 | 861.937 | 0.139 | $8\sqrt{3}$ |
| R768 | 113,246,208 | – | – | – | – | 545.192 | 0.020 | 860.676 | 0.139 | $16\sqrt{3}$ |
| R800 | 128,000,000 | – | – | – | – | 545.068 | 0.020 | 861.685 | 0.139 | $17\sqrt{3}$ |

各算例对应的柔顺度 $c$ 以及表征材料 0-1 离散程度的指标 $\text{MDN} = \frac{4}{N_e}\sum_{e}\bar{\rho}_e(1-\bar{\rho}_e)$ 汇总在表 1 中。

![[Wang2025_Fig11.png]]

<center><b>
图 11：(a) 在极严容差 $\epsilon_0 = 10^{-12}$ 下得到的多孔填充优化（PIO）结果（直接以体素密度值展示），其在视觉上与 $\epsilon_0 = 10^{-3}$ 下的结果完全一致；(b) 和 (c) 分别展示三种对比工况在各优化步中的 MGCG 迭代次数与耗时统计。
</b></center>

在悬臂梁模型上，我们进一步设计了一个极限实验，以验证即使将收敛容差大幅收紧至 $\epsilon_0 = 10^{-12}$，提出的 V 循环仍然能够稳定收敛。具体而言，我们在 R192 网格上运行多孔填充优化（参数为 $R_e = 8, r = 2\sqrt{3}, V_{e0} = 0.6$），分别测试：（1）标准 V 循环搭配 $\epsilon_0 = 10^{-12}$；（2）自适应非二进 V 循环搭配 $\epsilon_0 = 10^{-12}$；（3）自适应非二进 V 循环搭配 $\epsilon_0 = 10^{-3}$。优化在完成 300 步或当 MDN 低于 0.01 时终止。图 11 的结果证明，自适应非二进 V 循环在极严容差下依然能够保持高效、稳健的求解能力，且 $\epsilon_0 = 10^{-3}$ 下得到的结构与 $\epsilon_0 = 10^{-12}$ 下得到的结构无肉眼可见差异。

![[Wang2025_Fig12.png]]

<center><b>
图 12：(a) “GE Bracket”算例的问题描述：最大网格分辨率设为 512，对应约 1100 万个有限元单元；4 组不同载荷工况以不同颜色的箭头标出，固定约束面以黑色标出。(b) 与 (c) 分别展示对应的拓扑优化（TO）与多孔填充优化（PIO）结果。
</b></center>

**多载荷工况**（Multiple loading conditions）：在最后一个数值实验中，我们使用“GE Bracket”算例展示框架对多载荷工况的处理能力。在此类问题中，目标函数（式 (1)）修改为各工况柔顺度的加权和。对于 PIO，局部影响半径 $R_e$ 与局部体积上限 $V_{e0}$ 在全域统一设置为 6 个单元尺寸与 0.6。对于 TO，全局体积分数设定为 0.45。两类算例的平滑滤波半径均设为 2 个单元尺寸，固定区域最外围 5 层单元与受载区域最外围 15 层单元均设为被动实体单元。

图 12a 包含了 4 个独立的载荷工况，意味着在每个优化迭代步需要求解 4 个线性方程组。注意到所有工况具有相同的固定边界，因此 V 循环的层级初始化在每个优化步仅需执行一次。TO 结果（图 12b）在迭代 50 步后获得，PIO 结果（图 12c）在迭代 300 步后获得，分别耗时 7.6 小时和 144 小时。

对于多载荷工况，本文目前的方案是对每个载荷步依次执行独立的迭代求解。相比于基于矩阵直接分解（factorization-based）的求解器（单次分解后可极低成本地求解多个右端项），本方法在处理大量右端项时的效率优势有所减弱。然而，直接分解法面临着平方乃至指数级增长的内存与运算复杂度瓶颈，而这恰恰是本文方法所致力攻克的核心难题。

# 8 结论

本文提出并深入剖析了一套用于三维基于密度的拓扑优化及多孔填充优化的高效纯 MATLAB 实现框架，聚焦于高分辨率模拟域上线弹性有限元静力分析方程的高效求解。我们证明，共轭梯度法中广泛采用的多重网格预条件子可以与基于单元的 matrix-free 计算模板进行有机融合。通过针对性优化 matrix-free 内存与运算格式以充分利用 MATLAB 内置计算引擎，并辅以自适应非二进 V 循环技术，本方法相比既有 MATLAB 方案实现了质的飞跃——支持的网格分辨率提升了近两个数量级（达到 1.28 亿单元）。此外，该框架具备极高的工程实用性，能无缝适应任意非长方体几何域、非 2 的幂次分辨率及多载荷工况。

尽管该框架展现出了强大的性能优势，但受限于 MATLAB 自身机制，其进一步优化存在固有瓶颈：最核心的制约在于 MATLAB 频繁执行的数组索引寻址操作均为**单线程执行**，这在基于单元的 matrix-free 矩阵–向量乘法中构成了主要耗时环节。该限制也解释了为何纯 MATLAB 框架的绝对性能仍低于最顶尖的 C/C++ 实现。

潜在的突破途径包括借助 MATLAB GPU 加速或 MEX 混合编程。然而，GPU 路线受制于中端显卡有限的显存容量，难以直接承载超高分辨率模拟；而 MEX 方案需要依赖外部 C/C++ 编译代码，这与本工作追求“纯 MATLAB 实现”的教学初衷相悖。在未来的工作中，我们将持续关注 MATLAB 底层在多线程索引寻址能力上的演进，以期彻底攻克该性能瓶颈。

# 附录 A

在提出的基于单元 matrix-free 格式下执行 $\boldsymbol{Y} = \boldsymbol{K}\boldsymbol{u}$ 的 MATLAB 核心演示代码：

```matlab
%% 执行 "Y = Ku"
%% Step 1: 提取局部节点位移矩阵
Y = zeros(numNodes, 3);
uMat = zeros(size(eNodMat, 1), 24);
tmp = u(:, 1); uMat(:, 1:3:24) = tmp(eNodMat);
tmp = u(:, 2); uMat(:, 2:3:24) = tmp(eNodMat);
tmp = u(:, 3); uMat(:, 3:3:24) = tmp(eNodMat);

%% 边界条件处理阶段 1: 处理含固定自由度的特殊单元
eleWithFixedDOFs = find(mapUniqueKes_ > 0);
eleWithFixedDOFsLocal = mapUniqueKes_(eleWithFixedDOFs);
subDisVecUnique = uMat(eleWithFixedDOFs, :);
for kk = 1:numel(eleWithFixedDOFs)
    ss = eleWithFixedDOFsLocal(kk);
    subDisVecUnique(kk, :) = subDisVecUnique(kk, :) * ...
        (reshape(uniqueKesFree_(:, ss), 24, 24) * Ee(eleWithFixedDOFs(kk)) + ...
         reshape(uniqueKesFixed_(:, ss), 24, 24));
end

%% Step 2 & 3: 批处理单元乘法与杨氏模量缩放
uMat = uMat * Ke .* Ee(:);

%% 边界条件处理阶段 2: 回填特殊边界单元的乘积
uMat(eleWithFixedDOFs, :) = subDisVecUnique;

%% Step 4: 全局装配（累加写回）
tmp = uMat(:, 1:3:24);
Y(:, 1) = Y(:, 1) + accumarray(eNodMat(:), tmp(:), [numNodes, 1]);
tmp = uMat(:, 2:3:24);
Y(:, 2) = Y(:, 2) + accumarray(eNodMat(:), tmp(:), [numNodes, 1]);
tmp = uMat(:, 3:3:24);
Y(:, 3) = Y(:, 3) + accumarray(eNodMat(:), tmp(:), [numNodes, 1]);
Y = Y'; Y = Y(:);
```

# 附录 B

从存储为 matrix-free 格式的第 $l$ 层刚度矩阵 $\boldsymbol{K}^{[l]}$（$l = 1 : L-1$）中提取对角线向量 $\boldsymbol{D}^{[l]}$ 的 MATLAB 核心演示代码：

```matlab
%% 提取第 l 层刚度矩阵 K 的对角线元素 D
D_l = zeros(numNodes_l, 3);
eNodMatTmp = eNodMat_l'; eNodMatTmp = eNodMatTmp(:);

if l == 1
    % 最细网格层：由单位杨氏模量 Ke0 与单元弹性模量向量缩放得到
    diagKe = diag(Ke0);
    diagKe = diagKe(:) .* E(:)'; %% E: 单元杨氏模量向量
    eleWithFixedDOFs = find(mapUniqueKes_ > 0);
    eleWithFixedDOFsLocal = mapUniqueKes_(eleWithFixedDOFs);
    for kk = 1:numel(eleWithFixedDOFs)
        kKeFreeDOFs = reshape(uniqueKesFree_(:, eleWithFixedDOFsLocal(kk)), 24, 24);
        kKeFixedDOFs = reshape(uniqueKesFixed_(:, eleWithFixedDOFsLocal(kk)), 24, 24);
        diagKe(:, eleWithFixedDOFs(kk)) = diag(kKeFreeDOFs) * E(eleWithFixedDOFs(kk)) + ...
            diag(kKeFixedDOFs);
    end
    tmp = diagKe(1:3:end, :); tmp = tmp(:);
    D_l(:, 1) = D_l(:, 1) + accumarray(eNodMatTmp, tmp, [numNodes_l, 1]);
    tmp = diagKe(2:3:end, :); tmp = tmp(:);
    D_l(:, 2) = D_l(:, 2) + accumarray(eNodMatTmp, tmp, [numNodes_l, 1]);
    tmp = diagKe(3:3:end, :); tmp = tmp(:);
    D_l(:, 3) = D_l(:, 3) + accumarray(eNodMatTmp, tmp, [numNodes_l, 1]);
else
    % 粗网格层：Ks 存储第 l 层的单元刚度矩阵，排列尺寸为 24 x 24 x numElements_l
    KsTmp = reshape(Ks, 24*24, numElements_l);
    diagKeBlock = KsTmp(1:25:(24*24), :);
    tmp = diagKeBlock(1:3:end, :); tmp = tmp(:);
    D_l(:, 1) = D_l(:, 1) + accumarray(eNodMatTmp, tmp, [numNodes_l, 1]);
    tmp = diagKeBlock(2:3:end, :); tmp = tmp(:);
    D_l(:, 2) = D_l(:, 2) + accumarray(eNodMatTmp, tmp, [numNodes_l, 1]);
    tmp = diagKeBlock(3:3:end, :); tmp = tmp(:);
    D_l(:, 3) = D_l(:, 3) + accumarray(eNodMatTmp, tmp, [numNodes_l, 1]);
end

D_l = reshape(D_l', numDOFs_l, 1);
```

# 致谢

所有重要细节均已在正文中公开。完整代码（TOP3D_XL）可通过摘要中提供的链接获取。

# 作者贡献

- **Junpeng Wang（王俊鹏）**：概念构思、软件开发、方法论、论文撰写 - 审阅与编辑。
- **Niels Aage**：概念构思、方法论、论文撰写 - 审阅与编辑。
- **Jun Wu（吴俊）**：概念构思、方法论。
- **Ole Sigmund**：概念构思、论文撰写 - 审阅与编辑。
- **Rüdiger Westermann**：概念构思、方法论、论文撰写 - 审阅与编辑、指导、经费获取。

# 资助

本研究得到德国研究联合会（DFG）项目基金资助（项目批准号：WE 2754/10-1）。N. Aage 与 O. Sigmund 感谢 Villum 基金会通过 Villum 研究员项目“Amstrad”（批准号：VIL54487）提供的资金支持。

# 数据可用性声明

文中所涉及的所有数据均可在公开发布的代码仓库中获取。

# 利益冲突声明

作者声明不存在任何利益冲突。

---

# 参考文献

Aage N, Andreassen E, Lazarov BS (2015) Topology optimization using PETSc: an easy-to-use, fully parallel, open source topology optimization framework. Struct Multidiscip Optim 51:565–572. https://doi.org/10.1007/S00158-014-1157-0

Amir O (2015) Revisiting approximate reanalysis in topology optimization: on the advantages of recycled preconditioning in a minimum weight procedure. Struct Multidiscip Optim 51:41–57. https://doi.org/10.1007/s00158-014-1098-7

Amir O, Aage N, Lazarov BS (2014) On multigrid-cg for efficient topology optimization. Struct Multidiscip Optim 49:815–829. https://doi.org/10.1007/s00158-013-1015-5

Borrvall T, Petersson J (2001) Large-scale topology optimization in 3d using parallel computing. Comput Methods Appl Mech Eng 190(46–47):6201–6229. https://doi.org/10.1016/S0045-7825(01)00216-X

Challis VJ, Roberts AP, Grotowski JF (2014) High resolution topology optimization using graphics processing units (gpus). Struct Multidiscip Optim 49(2):315–325. https://doi.org/10.1007/s00158-013-0980-z

Dou S (2020) A projection approach for topology optimization of porous structures through implicit local volume control. Struct Multidiscip Optim 62(2):835–850. https://doi.org/10.1007/s00158-020-02539-x

Erlangga YA, Oosterlee CW, Vuik C (2006) A novel multigrid based preconditioner for heterogeneous helmholtz problems. SIAM J Sci Comput 27(4):1471–1492. https://doi.org/10.1137/040615195

Evgrafov A, Rupp CJ, Maute K, Dunn ML (2008) Large-scale parallel topology optimization using a dual-primal substructuring solver. Struct Multidiscip Optim 36(4):329–345. https://doi.org/10.1007/s00158-007-0190-7

Ferrari F, Sigmund O (2020) A new generation 99 line matlab code for compliance topology optimization and its extension to 3d. Struct Multidiscip Optim 62:2211–2228. https://doi.org/10.1007/s00158-020-02629-w

Fish J, Belsky V (1995) Multigrid method for periodic heterogeneous media part 1: Convergence studies for one-dimensional case. Comput Methods Appl Mech Eng 126(1–2):1–16. https://doi.org/10.1016/0045-7825(95)00811-E

Herrero-Pérez D, Castejón PJM (2021) Multi-gpu acceleration of large-scale density-based topology optimization. Adv Eng Softw 157:103006. https://doi.org/10.1016/j.advengsoft.2021.103006

Herrero-Pérez D, Picó-Vicente SG (2023) A parallel geometric multigrid method for adaptive topology optimization. Struct Multidiscip Optim 66(10):225. https://doi.org/10.1007/s00158-023-03675-w

Lazarov BS, Sigmund O (2011) Filters in topology optimization based on helmholtz-type differential equations. Int J Numer Meth Eng 86(6):765–781. https://doi.org/10.1002/nme.3072

Li H, Gao L, Li H, Li X, Tong H (2021) Full-scale topology optimization for fiber-reinforced structures with continuous fiber paths. Comput Methods Appl Mech Eng 377:113668. https://doi.org/10.1016/j.cma.2021.113668

Li H, Gao L, Li H, Tong H (2020) Spatial-varying multi-phase infill design using density-based topology optimization. Comput Methods Appl Mech Eng 372:113354. https://doi.org/10.1016/j.cma.2020.113354

Lin H, Liu H, Wei P (2022) A parallel parameterized level set topology optimization framework for large-scale structures with unstructured meshes. Comput Methods Appl Mech Eng 397:115112. https://doi.org/10.1016/j.cma.2022.115112

Liu H, Hu Y, Zhu B, Matusik W, Sifakis E (2018) Narrow-band topology optimization on a sparsely populated grid. ACM Transactions on Graphics (TOG) 37(6):1–14. https://doi.org/10.1145/3272127.3275012

Liu X, Réthoré J, Baietto MC, Sainsot P, Lubrecht AA (2020) An efficient finite element based multigrid method for simulations of the mechanical behavior of heterogeneous materials using ct images. Comput Mech 66:1427–1441. https://doi.org/10.1007/s00466-020-01909-y

Liu K, Tovar A (2014) An efficient 3d topology optimization code written in matlab. Struct Multidiscip Optim 50(6):1175–1196. https://doi.org/10.1007/s00158-014-1107-x

Martínez-Frutos J, Martínez-Castejón PJ, Herrero-Pérez D (2015) Fine-grained gpu implementation of assembly-free iterative solver for finite element problems. Computers & Structures 157:9–18. https://doi.org/10.1016/j.compstruc.2015.05.010

Mukherjee S, Lu D, Raghavan B, Breitkopf P, Dutta S, Xiao M, Zhang W (2021) Accelerating large-scale topology optimization: state-of-the-art and challenges. Arch Comput Methods Eng 28(7):4549–4571. https://doi.org/10.1007/s11831-021-09544-3

Peetz D, Elbanna A (2021) On the use of multigrid preconditioners for topology optimization. Struct Multidiscip Optim 63:835–853. https://doi.org/10.1007/s00158-020-02750-w

Schmidt MP, Pedersen CB, Gout C (2019) On structural topology optimization using graded porosity control. Struct Multidiscip Optim 60:1437–1453. https://doi.org/10.1007/s00158-019-02275-x

Schmidt S, Schulz V (2011) A 2589 line topology optimization code written for the graphics card. Comput Vis Sci 14:249–256. https://doi.org/10.1007/s00791-012-0180-1

Svanberg K (1987) The method of moving asymptotes—a new method for structural optimization. Int J Numer Meth Eng 24(2):359–373. https://doi.org/10.1002/nme.1620240207

Träff EA, Rydahl A, Karlsson S, Sigmund O, Aage N (2023) Simple and efficient gpu accelerated topology optimisation: Codes and applications. Comput Methods Appl Mech Eng 410:116043

Träff EA, Sigmund O, Aage N (2021) Topology optimization of ultra high resolution shell structures. Thin-Walled Struct 160:107349. https://doi.org/10.1016/j.tws.2020.107349

Wadbro E, Berggren M (2009) Megapixel topology optimization on a graphics processing unit. SIAM Rev 51(4):707–721. https://doi.org/10.1137/070699822

Wang C, Zhao Z, Zhou M, Sigmund O, Zhang XS (2021) A comprehensive review of educational articles on structural and multidisciplinary optimization. Struct Multidiscip Optim 64(5):2827–2880. https://doi.org/10.1007/s00158-021-03050-7

Wang J, Bukenberger DR, Niedermayr S, Neuhauser C, Wu J, Westermann R (2025) Sgldbench: A benchmark suite for stress-guided lightweight 3d designs. arXiv preprint arXiv:2501.03068

Wu J, Aage N, Westermann R, Sigmund O (2018) Infill optimization for additive manufacturing—approaching bone-like porous structures. IEEE Trans Visual Comput Graphics 24(2):1127–1140. https://doi.org/10.1109/TVCG.2017.2655523

Wu J, Dick C, Westermann R (2016) A system for high-resolution topology optimization. IEEE Trans Visual Comput Graphics 22(3):1195–1208. https://doi.org/10.1109/TVCG.2015.2502588

Wu J, Zhu J, Gao J, Gao L, Liu H (2024) A cad-oriented parallel-computing design framework for shape and topology optimization of arbitrary structures using parametric level set. Comput Methods Appl Mech Eng 431:117292. https://doi.org/10.1016/j.cma.2024.117292
