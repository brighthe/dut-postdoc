---
title: "翻译：A high-performance parallel algorithm based on problem independent machine learning (PIML) for large-scale topology optimization"
tags:
  - translation
  - PIML
  - topology-opt
  - parallel-computing
  - multigrid
status: "read"
date_created: 2026-06-09
date_updated: 2026-09-10
source: "../sources/Ma2026-highperformanceparallel.pdf"
citekey: "Ma2026-highperformanceparallel"
language: "zh-CN"
---

# A high-performance parallel algorithm based on problem independent machine learning (PIML) for large-scale topology optimization

---

# 信息

- **中文标题**：基于问题无关机器学习（PIML）的大规模、高性能并行拓扑优化算法
- **作者**：Xinyu Ma（马新宇）$^1$；Mengcheng Huang（黄孟成）$^1$；Zongliang Du（杜宗亮）$^{1,3,*}$；Yilin Guo（郭一麟）$^1$；Chang Liu（刘畅）$^{1,3,*}$；Yue Mei（梅越）$^2$；Xu Guo（郭旭）$^{1,3,*}$
- **单位**：
  - $1$: 大连理工大学工程力学系、工业装备结构分析优化与 CAE 软件国家重点实验室（大连 116023）
  - $2$: 清华大学航天航空学院工程力学系应用力学教育部重点实验室（北京 100084）
  - $3$: 大连理工大学宁波研究院（宁波 315016）
- **期刊**：*Acta Mechanica Sinica*
- **卷 / 期 / 文章号**：42(3): 425942
- **DOI**：10.1007/s10409-025-25942-x
- **在线发表 / 正式卷期**：2025-09-30 / 2026-01
- **通讯作者**：Zongliang Du（zldu@dlut.edu.cn）；Chang Liu（c.liu@dlut.edu.cn）；Xu Guo（guoxu@dlut.edu.cn）

# 摘要

大规模拓扑优化能够提供更广阔的设计空间，但“维度灾难”问题仍然制约其在工程实践中的广泛应用。近年来，随着高性能计算和人工智能的飞速发展，先进计算工具与拓扑优化的深度融合在大规模问题上取得了显著进展，并引发广泛关注。本文旨在将并行计算与机器学习这两类强大的计算范式联合用于提升大规模拓扑优化算法的效率和规模。据此，本文提出一种并行化、问题无关的机器学习（PIML）增强型拓扑优化方法。该方法中，PIML 模型显著降低了有限元缩聚刚度矩阵的维度及相应计算开销；并行计算进一步分摊每个进程的工作负载，并采用并行多重网格算法用于高效的有限元求解。此外，引入均匀粗单元直接缩聚与无矩阵实现（matrix-free implementation）等技术，以进一步提升计算效率与可扩展性。通过多组数值算例系统验证了方法的可行性、有效性与误差表现，并评估了其弱扩展效率、强扩展加速比以及最大可达效率。结果表明，与传统拓扑优化算法相比，所提方法在可解问题规模与求解效率方面均实现了显著提升。

**关键词**：拓扑优化（Topology optimization）；大规模（Large-scale）；问题无关机器学习（Problem-independent machine learning, PIML）；并行计算（Parallel computing）

# 1 引言

拓扑优化作为一种强大且合理的设计方法，近年来引起了广泛关注并取得了实质性进展。特别是，各种拓扑优化方法——包括固体各向同性材料惩罚（SIMP）方法 [1–3]、水平集方法（LSM）[4, 5]、进化结构优化（ESO）方法 [6, 7] 以及移动可变形组件（MMC）方法 [8–10] 等——已被开发出来，并成功应用于各个研究领域 [11–14] 与工业实践中 [15–17]。在工程应用中，大规模拓扑优化如今已获得了广泛的关注 [18]。这归因于大规模、高分辨率的网格能够捕捉到更多的几何细节，这不仅有利于工程结构的集成设计，还能提供更广阔的设计空间，从而创造出更注重性能的新型结构。然而，众所周知的“维度灾难”挑战为求解大规模三维拓扑优化问题带来了高昂的计算开销和低下的计算效率。随着优化问题规模的增加，有限元分析（FEA）中的单次迭代变得非常耗时，导致内存使用量的激增和求解器难度的攀升。这些挑战已经成为限制大规模拓扑优化在工程中实际应用的显著瓶颈。

为了解决这些问题，在大规模拓扑优化的计算效率提升方面不断取得进展 [19]。随着软硬件能力的显著提升，基于消息传递接口（MPI）[20] 或开放多处理（OpenMP）[21] 的中央处理器（CPU）并行计算，以及基于统一计算设备架构（CUDA）平台的图形处理器（GPU）并行计算 [22]，被用于加速拓扑优化过程。早在 2001 年，Borrvall 和 Petersson [23] 就利用高性能计算机（HPCs），结合区域分解技术实现了三维拓扑优化的并行计算。随后，Aage 等人 [24] 基于 SIMP 方法和便携可扩展科学计算工具包（PETSc）开发了大规模拓扑优化程序。通过该程序，他们还使用 8000 个 CPU 完成了十亿体素分辨率下波音 777 机翼的优化设计 [25]。Liu 等人 [26] 引入了一种基于紧支径向基函数参数化水平集方法（LSM）的大规模拓扑优化方法，并成功将其扩展到非结构网格的拓扑优化中 [27]。针对与弹性和热传导相关的大规模拓扑优化问题，Kambampati 等人 [28] 实现了基于 LSM 和体动态 B+ 树的高效并行算法。Xiong 等人 [29] 利用开源计算平台 FEniCS，实现了基于 BESO 方法的高分辨率拓扑优化。近年来，在 GPU 加速拓扑优化方面也涌现出许多优秀工作，例如单 GPU 并行化的 SIMP 算法 [30]、多 GPU 计算的拓扑优化 [31] 以及 GPU 加速的微结构设计 [32]。

此外，随着人工智能的进步，机器学习（ML）已被引入拓扑优化中以加速求解过程 [33]。例如，利用 ML 技术可以建立问题描述（包括设计域、边界和载荷条件）与优化设计之间的端到端映射 [34–38]。基于训练有素的模型，几乎可以实现实时的结构拓扑优化。为了提高 ML 模型的可扩展性，人工智能也被用于加速有限元分析（FEA）。在双分辨率设置下，粗分辨率网格的 FEA 结果和细分辨率网格的材料刚度分布被用于预测灵敏度信息 [39, 40]，与传统的拓扑优化算法相比，该方法可实现超过 30 倍的加速。此外，研究人员提出了一种有限元卷积神经网络（FE-CNN），通过建立高分辨率与低分辨率有限元解之间的关系来构建高效的结构拓扑优化算法，将效率提高了多达一个数量级 [41]。Li 等人 [42] 提出了一种被称为卷积-分层深度学习神经网络-张量分解（C-HiDeNN-TD）的框架，通过将 3D 力学问题分解为几个易于处理的小型 1D 问题，使用个人电脑来解决十亿级规模的拓扑优化问题。最近，一种问题无关机器学习（PIML）技术被提出，该技术适用于具有任意设计域和载荷/边界条件的拓扑优化问题，可减少与 FEA 相关的计算时间，并能够将大规模 3D 拓扑优化问题的求解效率提升 2–3 个数量级 [43–45]。

值得注意的是，上述大多数研究要么将并行计算要么将机器学习作为单一工具来使用（排除了那些使用 GPU 并行计算训练的端到端型 ML 模型）。沿着加速有限元分析（FEA）的思路，有必要研究通过同时利用并行计算（硬件层面）和 ML 算法（算法层面），我们能在多大程度上拓宽线弹性结构大规模拓扑优化的边界。为此，本文提出了一种全并行化的 PIML 增强拓扑优化框架。PIML 模型极大地降低了系统平衡线性代数方程组的维度，而并行计算则进一步减少了每个进程中的计算任务。此外，还集成了诸如多尺度形函数的无矩阵实现（matrix-free implementation）以及解除计算资源限制等多种技术，以在结构拓扑优化问题的可处理维度和效率上实现突破。

本文其余部分的组织结构如下：第 2 节介绍了针对 SIMP 方法的 PIML 增强子结构方法的基本思想；第 3 节详细说明了并行 PIML 增强拓扑优化算法的实现；第 4 节展示了所提算法在个人电脑和超级计算机平台上的数值验证；在第 5 节探讨了所提并行算法的可扩展性（scalability）和最优求解效率之后，最后一节给出了结论性评述。

# 2 面向线弹性结构大规模拓扑优化的 PIML 增强子结构方法

本节首先给出了结构拓扑优化的问题描述，随后简要介绍了用于大规模拓扑优化的原始 PIML 增强框架，以阐明将其与并行计算相结合的必要性。

## 2.1 结构拓扑优化的问题表述

对于在 $\mathbb{R}^N$ ($N = 1, 2$ 或 $3$) 空间中占据且具有适当几何正则性的开有界域 $\Omega$ 的线弹性固体，其平衡状态可通过弱形式描述为：

$$
\begin{aligned}
&\text{寻找}\quad \boldsymbol{u} \in \boldsymbol{H}^1(\Omega) \\
&\text{使得}\quad \int_{\Omega} \mathbb{E}(\boldsymbol{x}) : \nabla\boldsymbol{u} : \nabla\boldsymbol{v}\,\mathrm{d}V = \int_{\Omega} \boldsymbol{f} \cdot \boldsymbol{v}\,\mathrm{d}V + \int_{S_t} \boldsymbol{t} \cdot \boldsymbol{v}\,\mathrm{d}S, \quad \forall \boldsymbol{v} \in \boldsymbol{H}_0^1(\Omega), \\
&\hspace{3.2em}\boldsymbol{u} = \bar{\boldsymbol{u}}, \quad \text{在 } S_u \text{ 上},
\end{aligned}
\tag{1}
$$

其中 $\boldsymbol{H}^1(\Omega) = [H^1(\Omega)]^N$，而 $H^1(\Omega)$ 表示在 $L^2(\Omega)$（即定义在 $\Omega$ 上的平方可积函数空间）中具有阶数小于或等于 1 的广义偏导数的 Sobolev 空间。$\mathbb{E}(\boldsymbol{x})$ 为弹性张量。$\boldsymbol{f}$ 和 $\boldsymbol{t}$ 分别代表体力密度以及定义在 Neumann 边界 $S_t$ 上的面力密度。符号 $\bar{\boldsymbol{u}}$ 表示定义在 Dirichlet 边界 $S_u$ 上的给定（规定）位移，而 $\boldsymbol{v} \in \boldsymbol{H}_0^1(\Omega)$ 是测试函数，其中 $\boldsymbol{H}_0^1(\Omega) = \{ \boldsymbol{v} \mid \boldsymbol{v} \in \boldsymbol{H}^1(\Omega), \boldsymbol{v} = \boldsymbol{0} \text{ 在 } S_u \text{ 上} \}$。

在经典的 SIMP（固体各向同性材料惩罚）框架 [46] 下，每个有限元被赋予一个密度值 $\rho_e$，并且第 $e$ 个单元的杨氏模量被插值表示为 $E_e = E_{\min} + \rho_e^3(E_0 - E_{\min})$ ($e = 1, 2, \dots, n$)。其中 $E_0$、$E_{\min}$ 和 $n$ 分别表示固体材料的杨氏模量、为避免可能出现的矩阵奇异性而设定的空隙（孔洞）材料的杨氏模量，以及设计域中有限元的总数。体积约束下最小柔顺性设计问题的数学形式被离散化为：

$$
\begin{aligned}
\text{寻找}\quad & \boldsymbol{\rho} = (\rho_1, \rho_2, \dots, \rho_n)^{\mathrm{T}}, \\
\text{最小化}\quad & c = \boldsymbol{F}^{\mathrm{T}}\boldsymbol{U}, \\
\text{满足}\quad & \boldsymbol{K}(\boldsymbol{\rho})\boldsymbol{U} = \boldsymbol{F}, \\
& g = V(\boldsymbol{\rho}) - \bar{V} \le 0, \\
& 0 \le \rho_i \le 1, \quad i = 1, 2, \dots, n.
\end{aligned}
\tag{2}
$$

其中 $\boldsymbol{K}(\boldsymbol{\rho})$、$\boldsymbol{U}$ 和 $\boldsymbol{F}$ 分别为全局刚度矩阵、节点位移向量和外部节点力向量。符号 $V$ 为固体材料的体积分数，$\bar{V}$ 为其上限。

对于大规模三维拓扑优化问题，求解平衡状态的线性代数方程组将极其耗时且需要庞大的内存。为了缓解这一问题，Huang 等人 [43, 44] 提出了所谓的面向大规模结构分析与拓扑优化的 PIML 增强子结构方法，正如后续小节所述。

## 2.2 PIML 增强的子结构方法——串行算法

### 2.2.1 经典子结构方法

在经典的子结构方法中，设计域被离散为一组子结构 $\Omega^j$ ($j = 1, 2, \dots, N_s$)。对于由细观尺度上 $m \times m \times m$ 个有限元组成的每一个 $\Omega^j$，与其关联的自由度（DOFs）被划分为边界自由度（用下标“b”标识）和内部自由度（用下标“i”标识），如图 1 所示。那么，$\Omega^j$ 的离散平衡方程可以分解为：

$$
\boldsymbol{K}^j \boldsymbol{u}^j =
\begin{pmatrix}
\boldsymbol{K}_{\mathrm{bb}}^j & (\boldsymbol{K}_{\mathrm{ib}}^j)^{\mathrm{T}} \\
\boldsymbol{K}_{\mathrm{ib}}^j & \boldsymbol{K}_{\mathrm{ii}}^j
\end{pmatrix}
\begin{pmatrix}
\boldsymbol{u}_{\mathrm{b}}^j \\
\boldsymbol{u}_{\mathrm{i}}^j
\end{pmatrix}
=
\begin{pmatrix}
\boldsymbol{f}_{\mathrm{b}}^j \\
\boldsymbol{f}_{\mathrm{i}}^j
\end{pmatrix}.
\tag{3}
$$

其中 $\boldsymbol{K}^j$ 和 $\boldsymbol{u}^j$ 分别是第 $j$ 个子结构的刚度矩阵和节点位移向量。符号 $\boldsymbol{u}_{\mathrm{b}}^j, \boldsymbol{f}_{\mathrm{b}}^j \in \mathbb{R}^{n_{\mathrm{b}}^j}$ 和 $\boldsymbol{u}_{\mathrm{i}}^j, \boldsymbol{f}_{\mathrm{i}}^j \in \mathbb{R}^{n_{\mathrm{i}}^j}$ 分别是第 $j$ 个子结构边界节点和内部节点的节点位移向量与节点力向量。不失一般性地，假定内部节点的节点力向量 $\boldsymbol{f}_{\mathrm{i}}^j$ 为零。那么式 (3) 可以等价地表达为其缩聚形式：

$$
\boldsymbol{K}_{\mathrm{s}}^j \boldsymbol{u}_{\mathrm{b}}^j = \boldsymbol{f}_{\mathrm{b}}^j,
\tag{4}
$$

其中 $\boldsymbol{K}_{\mathrm{s}}^j = \boldsymbol{K}_{\mathrm{bb}}^j - (\boldsymbol{K}_{\mathrm{ib}}^j)^{\mathrm{T}} (\boldsymbol{K}_{\mathrm{ii}}^j)^{-1} \boldsymbol{K}_{\mathrm{ib}}^j$ 即为所谓的第 $j$ 个子结构的缩聚刚度矩阵（condensed stiffness matrix）。

![[Ma2026_Fig1.png]]

<center><b>
图 1：PIML 模型中 $m = 5$ 的三维子结构示意图。
</b></center>

在子结构方法中，$\boldsymbol{K}_{\mathrm{s}}^j$ 和 $\boldsymbol{f}_{\mathrm{b}}^j$ ($j = 1, 2, \dots, N_s$) 可以分别被组装成全局缩聚刚度矩阵 $\boldsymbol{K}_{\mathrm{s}} = \bigwedge_{j=1}^{N_s} \boldsymbol{K}_{\mathrm{s}}^j$ 以及全局缩聚外载荷向量 $\boldsymbol{f}_{\mathrm{s}} = \bigwedge_{j=1}^{N_s} \boldsymbol{f}_{\mathrm{b}}^j$。缩聚位移向量 $\boldsymbol{u}_{\mathrm{s}}$ 可以通过求解 $\boldsymbol{K}_{\mathrm{s}}\boldsymbol{u}_{\mathrm{s}} = \boldsymbol{f}_{\mathrm{s}}$ 来确定。在确定了边界位移 $\boldsymbol{u}_{\mathrm{b}}^j$ 之后，我们可以得到内部位移 $\boldsymbol{u}_{\mathrm{i}}^j = -(\boldsymbol{K}_{\mathrm{ii}}^j)^{-1}\boldsymbol{K}_{\mathrm{ib}}^j\boldsymbol{u}_{\mathrm{b}}^j$ ($j = 1, 2, \dots, N_s$)。

### 2.2.2 面向大规模结构分析与拓扑优化的 PIML 模型

基于经典子结构方法，子结构 $\Omega^j$ 内的连续位移场 $\tilde{\boldsymbol{u}}^j(\boldsymbol{x}) \in \mathbb{R}^{n^j}$ ($n^j = n_{\mathrm{b}}^j + n_{\mathrm{i}}^j$) 可以被插值为：

$$
\tilde{\boldsymbol{u}}^j(\boldsymbol{x}) = \tilde{\boldsymbol{N}}_{\mathrm{b}}^j(\boldsymbol{x})\boldsymbol{u}_{\mathrm{b}}^j + \tilde{\boldsymbol{N}}_{\mathrm{i}}^j(\boldsymbol{x})\boldsymbol{u}_{\mathrm{i}}^j = \tilde{\boldsymbol{N}}^j(\boldsymbol{x})\boldsymbol{u}_{\mathrm{b}}^j.
\tag{5}
$$

其中，$\tilde{\boldsymbol{N}}_{\mathrm{b}}^j(\boldsymbol{x}) \in \mathbb{R}^{n^j \times n_{\mathrm{b}}^j}$ 和 $\tilde{\boldsymbol{N}}_{\mathrm{i}}^j(\boldsymbol{x}) \in \mathbb{R}^{n^j \times n_{\mathrm{i}}^j}$ 分别是与 $\boldsymbol{u}_{\mathrm{b}}^j$ 和 $\boldsymbol{u}_{\mathrm{i}}^j$ 关联的传统形函数。与子结构 $\Omega^j$ 关联的传统形函数可以通过下式计算得到：

$$
\tilde{\boldsymbol{N}}^j(\boldsymbol{x}) = \tilde{\boldsymbol{N}}_{\mathrm{b}}^j(\boldsymbol{x}) - \tilde{\boldsymbol{N}}_{\mathrm{i}}^j(\boldsymbol{x}) (\boldsymbol{K}_{\mathrm{ii}}^j)^{-1} \boldsymbol{K}_{\mathrm{ib}}^j \in \mathbb{R}^{n^j \times n_{\mathrm{b}}^j}.
\tag{6}
$$

由于子结构中与每个节点相关联的形函数具有单位分解（partition of unity）特性，第 $j$ 个子结构的节点位移向量也可以表示为：

$$
\boldsymbol{u}^j =
\begin{pmatrix}
\boldsymbol{u}_{\mathrm{i}}^j \\
\boldsymbol{u}_{\mathrm{b}}^j
\end{pmatrix}
=
\begin{bmatrix}
-(\boldsymbol{K}_{\mathrm{ii}}^j)^{-1}\boldsymbol{K}_{\mathrm{ib}}^j \\
\boldsymbol{I}_{n_{\mathrm{b}}^j \times n_{\mathrm{b}}^j}
\end{bmatrix}
\boldsymbol{u}_{\mathrm{b}}^j
\triangleq
\boldsymbol{N}^j \boldsymbol{u}_{\mathrm{b}}^j.
\tag{7}
$$

其中 $\boldsymbol{N}^j \in \mathbb{R}^{n^j \times n_{\mathrm{b}}^j}$ 是一个常数矩阵，代表离散形函数或所谓的多尺度形函数 [43]。此外，第 $j$ 个子结构的缩聚刚度矩阵可计算为：

$$
\boldsymbol{K}_{\mathrm{s}}^j = (\boldsymbol{N}^j)^{\mathrm{T}} \boldsymbol{K}^j \boldsymbol{N}^j.
\tag{8}
$$

子结构方法可应用于具有任意设计域和边界条件的结构优化问题。然而，在拓扑优化过程中，由于子结构中每个有限元的材料分布和弹性属性通常在迭代中不断变化，因此每次迭代都需要重新计算子结构的缩聚刚度矩阵。为了加速面向大规模结构分析的经典子结构方法，Huang 等人 [44] 建议在子结构的边界上附加一些变形假设，例如沿着子结构边缘的线性变形。因此，边界位移 $\boldsymbol{u}_{\mathrm{b}}^j$ 可以由顶点节点的节点位移向量确定为 $\boldsymbol{u}_{\mathrm{b}}^j = \boldsymbol{L}\boldsymbol{u}_{\mathrm{v}}^j$，其中 $\boldsymbol{L} \in \mathbb{R}^{n_{\mathrm{b}}^j \times n_{\mathrm{v}}^j}$ 代表线性插值矩阵，$n_{\mathrm{v}}^j$ 是第 $j$ 个子结构中顶点节点的自由度数量。那么，带有线性变形假设的多尺度形函数和单元缩聚刚度矩阵可以表示为：

$$
\begin{cases}
\bar{\boldsymbol{N}}^j = \boldsymbol{N}^j \boldsymbol{L} =
\begin{bmatrix}
\bar{\boldsymbol{N}}_{\mathrm{s}}^j \\
\boldsymbol{L}
\end{bmatrix}, \\[6pt]
\bar{\boldsymbol{K}}_{\mathrm{s}}^j = (\bar{\boldsymbol{N}}^j)^{\mathrm{T}} \boldsymbol{K}^j \bar{\boldsymbol{N}}^j = \boldsymbol{L}^{\mathrm{T}} (\boldsymbol{N}^j)^{\mathrm{T}} \boldsymbol{K}^j \boldsymbol{N}^j \boldsymbol{L}.
\end{cases}
\tag{9}
$$

对于由细观尺度上 $m \times m \times m$ 个有限元组成的三维子结构，当 $m = 5$ 时，其子结构缩聚刚度矩阵的维度为 $273 \times 273$（当 $m = 10$ 时为 $993 \times 993$）；而引入线性变形假设后，无论是 $m = 5$ 还是 $m = 10$，其单元缩聚刚度矩阵的维度均降为 $24 \times 24$。尽管线性变形假设可能会高估子结构的刚度，但已有验证表明，当子结构的总体数量变得更大时，这一问题将得到显著缓解 [43, 44]。

值得注意的是，在六种刚体运动状态下，子结构内部节点的位移值完全可以由顶点节点的位移来确定，而与内部的材料分布无关。在数学上，这种刚体运动要求可以表示为 $\bar{\boldsymbol{N}}^j\boldsymbol{\phi}_i = \boldsymbol{b}_i$ ($i = 1, 2, \dots, 6$)，其中 $\boldsymbol{\phi}_i$ 和 $\boldsymbol{b}_i$ 的精确表达式在文献 [45] 中给出。因此，多尺度形函数 $\bar{\boldsymbol{N}}^j$ 可以通过使用维度为 $3(m - 1)^3 \times (24 - 6)$ 的缩减多尺度形函数 $\bar{\boldsymbol{N}}_{\mathrm{sR}}^j$ 以及刚体运动要求来恢复。在文献 [44] 中，通过离线机器学习过程建立了一个问题无关的隐式映射，该映射将表征 $\Omega^j$ 内部材料分布的参数（即 $\rho_1, \rho_2, \dots, \rho_{m^3}$ 或 $E_1, E_2, \dots, E_{m^3}$）与 $\bar{\boldsymbol{N}}_{\mathrm{sR}}^j$ 联系起来（示意图见图 2）。一旦建立了这种映射，它就可以用来分析和优化任何由包含 $m^3$ 个细观单元的类似子结构离散的线弹性拓扑优化问题。与传统的子结构分析方法相比，缩聚刚度矩阵的耗时计算被 PIML 模型预测的多尺度形函数的高效矩阵乘法所取代。

![[Ma2026_Fig2.png]]

<center><b>
图 2：PIML 增强的子结构分析算法示意图。
</b></center>

### 2.2.3 串行 PIML 增强结构分析与拓扑优化算法的数值性能

将经典 SIMP 方法中的有限元分析（FEA）替换为 PIML 增强的子结构分析算法，文献 [44] 中的研究在大规模三维拓扑优化问题上取得了显著成果。在一台配备 Intel(R) Xeon(R) Gold 6256 3.60 GHz CPU 和 512.0 GB 内存（RAM）的台式机上，对于设计域分别由 165 万和 1172 万个细观单元离散化以实现刚度最大化的 MBB 梁算例，使用 $m = 5$ 的 PIML 模型时，与采用全尺度分析的经典 SIMP 方法相比，单次迭代的求解效率分别可加速约 470 倍和 320 倍。此外，对于由 10.24 亿（$1600 \times 800 \times 800$）个细观单元组成的短悬臂梁算例，使用 PIML 模型（$m = 10$）的串行算法单次迭代的平均时间开销为 5677.8 秒。

一方面，通过使用 PIML 模型，通常需要借助超级计算机采用经典 SIMP 方法进行并行计算才能求解的 10.24 亿有限元三维拓扑优化问题 [25, 47]，现在可以在一台台式机上以串行方式求解，从而显著降低了大规模拓扑优化问题对计算资源的需求。另一方面，除了花费 53.55% 的时间开销用于求解子结构（粗网格）的平衡方程外，对于该悬臂梁算例 [44]，计算全局缩聚刚度矩阵与细观网格位移向量花费了 26.15% 的时间，而更新设计变量则花费了 20.3% 的时间。这进一步促使我们为所提出的 PIML 增强子结构方法开发一种并行计算框架，以期从以下三个方面提升求解效率：

- **求解子结构的平衡方程**：尽管带有线性变形假设的 PIML 模型显著降低了平衡方程的维度，但对于包含数十亿单元的超大规模拓扑优化问题，即使取 $m = 10$，仍然需要分析数以百万计的子结构。众所周知，刚度矩阵的条件数和带宽会随着自由度（DOFs）数量的增加而恶化。因此，有必要使用高性能并行迭代算法代替串行算法来求解大规模子结构的平衡方程。
- **计算子结构的缩聚刚度矩阵和内部节点位移**：需要为每个子结构预测或计算多尺度形函数、单元缩聚刚度矩阵以及细观尺度位移。由于不同子结构中这些量的计算过程是相互独立的，因此自然而然地会选择并行分布式计算来实现结构不同部分的同步计算，从而降低每个进程的工作负载并提高求解效率。
- **更新设计变量**：在本方法中，设计变量与细观尺度单元相关联。需要执行滤波和灵敏度分析，以便基于最优性准则（OC）[48] 或数学规划方法（例如移动渐近线法 MMA）[49] 更新设计变量。已有研究表明，对于具有数百万设计变量的拓扑优化，必须对 MMA 进行并行化以更新密度场 [20]。

值得注意的是，PIML 模型继承了子结构方法天然易于并行计算和具备良好可扩展性的优点，这意味着在分布式计算中不需要设置幽灵区域（ghost regions）。此外，一旦神经网络在预测多尺度形函数方面被充分训练，它就可以应用于任意设计域（只要其由类似的子结构离散化）的结构拓扑优化，而完全独立于外部载荷与边界条件。这两个特征是并行 PIML 增强的大规模结构分析与拓扑优化算法取得成功的关键点。

# 3 并行 PIML 模型增强的大规模结构分析与拓扑优化

由于所提出的 PIML 模型增强子结构方法涉及两种尺度的网格（即子结构网格与细观单元网格），因此在分布式并行计算框架中，一个至关重要的问题是如何分摊工作负载（例如对这些网格进行划分）。本节将介绍并行优化流程、网格分解以及求解器设置。为了节省内存，多尺度形函数是在无矩阵（matrix-free）环境中计算的 [50]。所有相关设置均基于 PETSc 高性能求解器工具包 [51]。

## 3.1 并行优化流程

基于 PIML 模型的拓扑优化框架的串行与并行流程如图 3 所示。与串行实现不同，在并行算法中，网格（包括用于子结构分析的粗网格及其关联的细网格）被分解成不同的区块（segments），并分配给各种计算进程（即 CPU 核心）。随后，来自不同网格区块的计算任务将在它们对应的进程中同时（同步）执行。

![[Ma2026_Fig3.png]]

<center><b>
图 3：PIML 增强型大规模拓扑优化的串行和并行算法流程图。
</b></center>

在初始化之后，在串行流程中，所有的多尺度形函数 $\bar{\boldsymbol{N}}^j$ 被依次计算并存储在内存中，随后根据式 (9) 计算单元缩聚刚度矩阵。然而，对于一个被离散为 $800 \times 400 \times 400 = 1.28$ 亿个细观单元的设计域，使用传统的双精度浮点型（double-type）变量存储所有的多尺度形函数将消耗大约 98.1 GB 的内存。受大规模矩阵求解算法中常用的无矩阵（matrix-free）方法的启发，在并行程序中（如图 3 所示），多尺度形函数由独立进程使用 PIML 模型进行预测，并在并行计算完缩聚刚度矩阵后**不予保存（即清空内存）**。这在并行环境中实现了计算速度与内存消耗之间的绝佳平衡。

随后，使用并行多重网格算法 [52] 求解子结构的节点位移向量。由于多尺度形函数没有被显式存储，必须再次对它们进行预测，以获得细观单元的节点位移。接着，可以计算目标函数的值以验证是否收敛。除非满足收敛要求，否则将按照经典的 SIMP 方法为每个细观单元计算目标函数的灵敏度：

$$
\frac{\partial c}{\partial \rho_e} = -p \rho_e^{p-1} (E_0 - E_{\min}) \boldsymbol{u}_e^{\mathrm{T}} \boldsymbol{k}_0 \boldsymbol{u}_e.
\tag{10}
$$

其中 $\boldsymbol{k}_0$ 是实体单元（$\rho_e = 1$）的刚度矩阵，$p = 3$，而 $\boldsymbol{u}_e$ 表示第 $e$ 个单元的节点位移向量。在使用并行化的移动渐近线算法（MMA）更新设计变量之后，为了缓解众所周知的棋盘格问题（checkerboard issue），在之前串行的基于 PIML 的算法中使用了密度滤波器 [43–45]。对于超大规模的三维设计问题，计算和保存权重因子矩阵将极其昂贵。因此，我们采用了基于亥姆霍兹型（Helmholtz-type）微分方程的 PDE 滤波器 [53]。其核心思想是将滤波后的密度场 $\tilde{\rho}$ 隐式定义为亥姆霍兹型微分方程的解：

$$
-r^2 \nabla^2 \tilde{\rho} + \tilde{\rho} = \rho,
\tag{11}
$$

并在设计域的边界上施加齐次 Neumann 边界条件：

$$
\frac{\partial \tilde{\rho}}{\partial \boldsymbol{n}} = 0.
\tag{12}
$$

在式 (11) 中，$r$ 是一个长度参数，即 PDE 滤波器的滤波半径。具体的实现可参见文献 [53]。尽管在每次迭代中都需要求解亥姆霍兹型微分方程，但在使用并行实现时，其时间开销是微乎其微的。此外，还利用了海维赛德（Heaviside）投影法来处理灰度区域（gray regions），其中投影密度 $\hat{\rho}_e$ 和海维赛德函数 $\operatorname{H}(\tilde{\rho})$ 写成如下形式 [54]：

$$
\hat{\rho}_e = \operatorname{H}(\tilde{\rho}_e) = \frac{\tanh(\beta \eta) + \tanh[\beta (\tilde{\rho}_e - \eta)]}{\tanh(\beta \eta) + \tanh[\beta (1 - \eta)]}.
\tag{13}
$$

## 3.2 网格分解

进程管理与网格划分对于本研究中的并行计算至关重要。正如第 2 节所述，PIML 增强的分析算法涉及细观网格的细分以及粗观网格（子结构）的划分。因此，必须确保在特定的进程内，粗网格与细网格之间存在一一对应关系。在当前工作中，在每个进程内部，排序是沿着 $x$、$y$ 和 $z$ 方向顺序进行的。

对于图 4 所示的 $2 \times 1 \times 1$ 设计域，总共使用了 $1600 \times 800 \times 800 = 10.24$ 亿个细观单元来离散密度场。所提出的并行 PIML 模型增强子结构方法通过三个层次加速了结构分析：并行计算、PIML 模型以及并行多重网格算法。具体而言，如图 4 所示，设计域首先被划分为 $20 \times 10 \times 10$ 个子域，并分别分配给 2000 个 CPU 核心，以减少每个进程的工作负载。采用 PIML 模型，每个进程负责处理 512 个 $m = 10$ 的子结构。最后，利用多重网格算法求解线性代数方程组，当多重网格层级（multigrid level）设置为 4 时，第 4 层的一个最粗网格包含了 $2^3 \times 2^3 \times 2^3 = 512$ 个子结构。因此，每个 CPU 核心只需要处理 1 个最粗网格。这三层策略对于实现有限元分析（FEA）的超高效率至关重要。

![[Ma2026_Fig4.png]]

<center><b>
图 4：$m = 10$ 时并行 PIML 增强求解策略中的网格分解示意图（包含 10.24 亿个单元的三维设计域被分配到 2000 个 CPU 核心）。
</b></center>

注意到这样一个事实：每个子结构的单元缩聚刚度矩阵、内部节点位移值、灵敏度信息以及应变能与其他子结构是相互独立的，因此除了执行 `MatAssemblyBegin`（启动粗网格全局刚度矩阵的组装）和 `DMLocalToGlobalBegin`（将细观网格的位移传回全局位移向量）这两个命令外，不需要进行任何信息通信。因此，在 PETSc 中，幽灵节点（ghost nodes）和幽灵单元被设置为 `DM_BOUNDARY_NONE`。正如第 5 节所分析的那样，这避免了在涉及大量 CPU 的高性能计算（HPC）中，由于频繁的信息交换而导致的大规模计算效率下降问题。基于 PETSc 的并行数据布局信息，网格分解和数据结构变得方便且直观。这些也进一步印证了 PIML 方法卓越的并行特性。

## 3.3 平衡方程的求解器设置

如前所述，采用包含 $10 \times 10 \times 10$ 个单元的均匀子结构，PIML 增强的子结构方法可以将自由度（DOFs）降低到全尺度分析自由度的约 1/1000。然而，对于具有 100 亿自由度的超大规模问题，使用串行求解器来求解涉及约 1000 万自由度的线性代数方程组仍然非常耗时。因此，在这项工作中，我们利用 PETSc 结合多重网格预条件（MG）方法和广义最小残差法（GMRES）[55] 算法，来求解粗网格的平衡方程 [56]。作为一种迭代线性求解器，多重网格算法的相对收敛容差设定为 $10^{-8}$，或者最大迭代次数设定为 30 次。对于所有层级（除最粗网格层外）的平滑器，每次向上和向下平滑扫描的平滑迭代次数均设置为 4。同时，根据问题规模、计算效率和计算资源设置合适的多重网格层级非常重要，关于多重网格层级选择的详细讨论见第 5.2 节。

# 4 数值算例

本文在个人电脑和高性能计算（HPC）环境中研究了几个数值算例，以测试所提出的框架。对于本工作中的所有算例，实体和孔洞材料的杨氏模量分别设置为 1 和 $10^{-7}$。泊松比设置为 0.3。采用了 PDE 滤波器和海维赛德（Heaviside）投影，其中 $\beta$ 的初始值和最终值分别设置为 0.1 和 48，$\eta$ 设置为 0.0。$\beta$ 每 10 步增加一次，从 0.1 开始，当小于 7 时每次增加 1，然后以 1.2 的倍数递增。在大约 180 步之后，它达到 48 并保持不变。除非另有说明，多重网格层级设置为 4。有限元分析（FEA）由 PETSc 3.19 修订版提供支持。个人电脑配备了 Intel(R) Xeon(R) Gold 6248R CPU @ 3.00 GHz、48 个核心以及 512 GB 内存。此外，我们采用了北京超级云计算中心（ChinaHPC）的 Norm3 分区，该分区包含 400 个计算节点，每个节点包含 128 GB 内存（内存带宽为 120 GB/s）和 28 个 CPU 核心（Intel Xeon E5-2680v4，基础频率 2.4 GHz，最大睿频 3.3 GHz）。在并行 PIML 增强拓扑优化算法中，采用具有线性变形假设且 $m = 10$（包含 1000 个细观单元）的均匀子结构来降低计算成本。最大迭代次数设置为 200。

## 4.1 个人电脑验证

如图 5 所示，悬臂梁的左侧被固定，并在右侧底边施加大小为 $F = 1$ 的均布力。$2 \times 1 \times 1$ 的设计域被离散为 $240 \times 120 \times 120$ 个细观单元，PDE 滤波半径为 0.042，最大体积分数为 0.12。使用 48 个 CPU 核心，每次迭代的平均计算时间仅约为 3.1 秒。如图 6(a) 所示，优化后的结构通过 PIML 方法得出的结构柔顺性为 $C_{\mathrm{PIML}} = 325.9$，相比之下，通过全尺度分析得出的精确柔顺性为 $C_{\mathrm{exact}} = 377.0$，对应的相对误差为 13.96%。这种差异是由于子结构边界线性变形的假设造成的，尤其是在小规模（网格尺度较小）的情况下。

![[Ma2026_Fig5.png]]

<center><b>
图 5：悬臂梁算例的设计域和边界条件。
</b></center>

随着子结构数量的增加，这个问题可以得到有效改善。设计域被进一步离散为 $80 \times 40 \times 40$ 个子结构，PDE 滤波半径设置为 0.0125（密度滤波器会消耗过多的存储空间）。使用 40 个 CPU 核心，并行 PIML 增强拓扑优化算法的平均每次迭代计算时间约为 105.9 秒。如图 6(b) 所示，优化后的悬臂梁展现出明显不同的拓扑构型和更多的结构细节，其中加载线和固定端由板状构件连接，呈现出符合力学理性的载荷传递路径。正如预期的那样，这种更大规模设计的结构柔顺性值降低了，且 PIML 方法的精度得到了显著提高（$C_{\mathrm{PIML}} = 257.8$ 且 $C_{\mathrm{exact}} = 270.99$，相对误差降至 4.9%）。同时，并行 PIML 增强算法即使在个人电脑上也展现出了极具吸引力的计算效率。作为对比，即使在相同的设置下使用北京超算（ChinaHPC）平台的 250 个 CPU 核心，对优化后的设计进行全尺度分析也需要耗费 1972.5 秒。关于 PIML 算法在效率和精度之间权衡的更详细讨论，可以参见第 5.4 节。

![[Ma2026_Fig6.png]]

<center><b>
图 6：使用所提方法获得的优化悬臂梁：(a) PDE 滤波器半径为 0.042，结构柔顺度为 377.0，共 345.6 万个单元；(b) PDE 滤波器半径为 0.0125，结构柔顺度为 270.99，共 1.28 亿个单元。
</b></center>

此外，如图 7 所示，尺寸为 $6 \times 1 \times 1$ 的 MBB 梁算例也在同一台个人电脑上进行了测试。最大体积分数设定为 0.12。利用 30 个 CPU 核心，并行 PIML 增强拓扑优化算法在对称边界条件下对四分之一的设计域进行了计算，该区域被离散为 $50 \times 100 \times 300$ 个细观单元。多重网格层级设置为 1，滤波半径分别设置为细网格尺寸的 5 倍和 7 倍。使用并行 PIML 增强算法，对应的每次迭代平均计算时间分别为 2.6 秒和 2.8 秒。此外，正如预期的那样，对于图 8(a) 中的优化结构，从全尺度分析中获得的柔顺性值为 218.1，而图 8(b) 中具有更大滤波半径的优化结构则具有更高的柔顺度值，为 221.9。

![[Ma2026_Fig7.png]]

<center><b>
图 7：MBB 梁算例的设计域和边界条件。
</b></center>

![[Ma2026_Fig8.png]]

<center><b>
图 8：使用所提方法获得的优化 MBB 梁：(a) 150 万个单元，密度滤波器半径为 0.05，单步耗时 2.6 s，结构柔顺度为 218.1；(b) 150 万个单元，密度滤波器半径为 0.07，单步耗时 2.8 s，结构柔顺度为 221.9。
</b></center>

## 4.2 超级计算机验证

在个人电脑上的验证突显了并行 PIML 增强拓扑优化算法惊人的效率。在本小节中，所有数值算例都在拥有更多计算资源的高性能计算（HPC）平台上进行研究，这进一步突显了所提出的算法在求解大规模拓扑优化问题效率方面的惊人能力。

### 4.2.1 10 亿单元悬臂梁算例

此处重新探讨了文献 [44] 中采用串行 PIML 增强求解算法分析过的悬臂梁算例，该算例由 $1600 \times 800 \times 800$ 个均匀细观单元（约 30.8 亿自由度）离散。最大可用体积分数设定为 0.12，偏微分方程（PDE）滤波半径设定为 0.00625。

在使用 2000 个 CPU 核心进行计算时，每个进程（process）分担 $8 \times 8 \times 8 = 512$ 个粗网格（子结构）单元。完成 200 步迭代总共耗时 6654 秒，平均单步迭代耗时 33.3 秒。作为对比，此前串行 PIML 增强算法的平均单步耗时为 5677.8 秒[^1]，这意味着本并行算法实现了约 170 倍的加速。特别地，各计算部分对应的时间分布如图 9 所示。值得注意的是，此前最耗时的环节——即粗网格结构的有限元分析（FEA）求解——在总时间中的占比从 54% 骤降至仅 13%，从而彻底消除了大规模拓扑优化问题中计算极为耗时这一普遍痛点。

[^1]: 原文脚注：配备 Intel(R) Xeon(R) Gold 6256 3.60 GHz CPU 和 512.0 GB 内存的台式机。

![[Ma2026_Fig9.png]]

<center><b>
图 9：10 亿单元悬臂梁算例中串行算法以及使用 2000 和 8192 个 CPU 核心的并行 PIML 增强算法的计算成本分布。
</b></center>

优化后的结构如图 10 所示，经 PIML 方法预测的结构柔顺度（compliance）为 243.3。作为对比，在文献 [44] 中，由于采用了更大的滤波半径，所得到的优化结构经 PIML 预测的柔顺度为 289.09。此外，当使用充足的计算资源时（详细讨论见下文第 5.2 节），即使用 8192 个 CPU 核心，整个求解过程仅耗时 3084.2 秒（约 51.4 分钟），平均单步迭代耗时仅 15.4 秒，展现出求解效率的显著提升。

![[Ma2026_Fig10.png]]

<center><b>
图 10：通过并行 PIML 增强算法获得的 10 亿单元悬臂梁优化设计。
</b></center>

### 4.2.2 百亿级自由度的悬臂梁算例

对于图 5 中的悬臂梁算例，其设计域被离散为 $2400 \times 1200 \times 1200 = 3,456,000,000$ 个细观尺度单元，节点自由度（DOFs）数量超过了 100 亿[^2]。将偏微分方程（PDE）滤波半径设定为 0.0042，并调用 6750 个 CPU 核心，包含 200 步迭代的优化过程在 2 小时 20 分 6 秒内完成，平均单步迭代耗时仅为 42.0 秒。

[^2]: 原文脚注：值得注意的是，由于网格规模超大，必须使用命令 `./configure --with-64-bit-indices` 将整数数据转换为 64 位。这不可避免地会导致内存消耗增加并降低计算效率。

优化后的结构如图 11 所示，它比图 10 中包含 10 亿单元的优化设计显得更加精细与微妙。具体而言，图 12(a) 展示了该百亿自由度悬臂梁在 $1/4$ 和 $1/2$ 位置处的截面视图。为了清晰展现其内部新颖的空腔结构，图中颜色根据密度场的大小进行渲染。此外，优化后的设计还展现出如图 12(b) 所示的丰富局部细节，这与拓扑优化的力学基本原理高度吻合。

![[Ma2026_Fig11.png]]

<center><b>
图 11：通过并行 PIML 增强算法获得的百亿自由度悬臂梁优化设计。
</b></center>

![[Ma2026_Fig12.png]]

<center><b>
图 12：百亿自由度优化悬臂梁的 (a) 1/4 和 1/2 位置切片视图及 (b) 局部结构细节。
</b></center>

如图 13(a) 所示，目标函数值在前 50 次迭代中急剧下降，而体积约束曲线中出现的振荡，是由于每 10 次迭代对投影参数 $\beta$ 进行周期性调整所致。值得注意的是，如图 13(b) 所示，单步迭代的总耗时以及计算全局缩聚刚度矩阵的时间开销，均呈现出先急剧增加、随后逐渐下降，并最终趋于平稳的趋势。这一现象主要归因于预测多尺度形函数所耗费时间的变化。在初始设计中，所有的密度值被均匀地设定为体积分数的上限，因此，单元缩聚刚度矩阵可以直接获取而无需经过模型预测。但在优化的早期阶段，会出现大量的灰度（中间密度）单元，相应的单元缩聚刚度矩阵需要依靠预测的多尺度形函数来计算，从而导致计算时间增加。随着中间设计变得非均匀（异质化），有限元分析（FEA）的求解开销也会增加。而在 30 次迭代之后，优化设计的拓扑构型变得更加明朗，更多的密度演化为离散值（0 或 1），进而使得计算开销随之下降。

![[Ma2026_Fig13.png]]

<center><b>
图 13：百亿自由度悬臂梁算例的收敛历史：(a) 目标函数值与体积约束；(b) 每次迭代总耗时及计算全局缩聚刚度矩阵耗时。
</b></center>

### 4.2.3 33.2 亿单元的类桥梁算例

为了进一步验证所提算法的有效性，本文还开展了一个带有非设计区域（non-design region）的类桥梁算例。如图 14 所示，尺寸为 $10 \times 1 \times 3$ 的设计域被离散为 $480 \times 48 \times 144$ 个均匀子结构，每个子结构包含 $m = 10$ 尺度划分的细观单元（总计约 99.8 亿自由度）。粗网格的顶层被设定为实体非设计区域，并承受单位均布载荷。如图 14 所示，固定约束施加在设计域底部的两个角落。最大可用体积分数和滤波半径分别设定为 0.18 和 0.0125。根据几何与载荷对称性，采用所提的并行 PIML 增强算法并调用 3240 个 CPU 核心，仅对一半的设计域进行优化求解。在 2 小时 7 分 4 秒内完成了 200 步迭代，并获得了如图 15 所示的优化设计，平均单步迭代耗时为 38.1 秒。在优化后的设计中，光滑的壳状基底与众多树状分支相融合，将均布载荷高效地传递至底部支撑处。

![[Ma2026_Fig14.png]]

<center><b>
图 14：类桥梁算例的设计域与边界条件。
</b></center>

![[Ma2026_Fig15.png]]

<center><b>
图 15：通过并行 PIML 增强算法获得的 33.2 亿单元类桥梁算例优化设计。
</b></center>

# 5 并行 PIML 增强拓扑优化算法的效率分析

本节旨在研究并行 PIML 增强拓扑优化算法的可扩展性（scalability）。在阐明了程序的弱扩展效率（weak scalability）、最大化资源利用率（maximum resource utilization）以及强扩展性（strong scalability）之后，依托北京超级云计算中心（ChinaHPC）平台最多 9000 个可用 CPU 核心，深入探讨了包含 1600 万至 34.5 亿个单元的三维拓扑优化问题的最优求解效率。

## 5.1 弱扩展效率

可扩展性（scalability 或 scaling）被广泛用于衡量程序在增加资源时提供更强计算能力的并行性能 [57]。在弱扩展（weak scaling）测试中，CPU 核心数与问题规模同步增加，从而保持每个进程的工作负载（workload per process）恒定。为了确保弱扩展性测试的一致性[^3]，多重网格层级（multigrid level）被固定为 4，且 PDE 滤波半径设定为细观网格尺寸的 5 倍。以采用 16 个 CPU 核心求解包含 819 万单元的悬臂梁算例时，并行 PIML 增强拓扑优化算法的平均单步迭代耗时作为基准，记为 $t_{w1}$；将采用更多 CPU 核心求解更大规模对应算例的耗时记为 $t_{wn}$，则弱扩展效率可定义为 $t_{w1}/t_{wn}$。相关的详细信息汇总于表 1 中。

[^3]: 原文脚注：为了进行稳定性测试，固定了部分设置而未考虑可实现的最高速度。关于不同问题规模下的最优求解效率，请参见后文第 5.5 节。

<center><b>
表 1：使用悬臂梁算例测试弱扩展效率。
</b></center>

![[Ma2026_Table1.png]]

理想的弱扩展效率应保持为 1，这意味着无论核心数量多少，程序的挂钟时间（wall-clock time）都将保持不变。然而，如表 1 所示，实际的扩展效率会随着 CPU 核心数的增加而下降。这归因于节点间的数据传输延迟（data transfer latency）随着问题规模和进程数量的增加而增大。值得注意的是，尽管单元数量从 819 万激增至 34.5 亿（规模增加了 421.9 倍），但平均时间开销仅仅增加了 1.2 倍。可以预见，如果拥有更多的可用计算资源，所提算法完全能够在可控的时间开销内解决更大规模的拓扑优化问题。此外还可以观察到，随着问题规模的增大，优化设计结果也逐渐演化出更加丰富的结构细节。

## 5.2 最大化进程利用率的释放

在上一小节中，对于包含上亿单元的拓扑优化问题，仅使用数百个 CPU 核心并不能充分发挥超级计算机的庞大算力。这种限制实际上源于代数多重网格（MG）法中的多重网格层级（multigrid level）设定。例如，当设计域包含 $80 \times 40 \times 40$ 个子结构（对应 1.28 亿个细观单元），且多重网格层级设为 4 时，各个方向上的最粗网格数量必须能够被 $2^3$ 整除。在这种情况下，能够参与并行计算的 CPU 核心数上限被“锁死”在了 $80 \times 40 \times 40 \div 8 \div 8 \div 8 = 250$ 个。若将多重网格层级调整为 3，参与计算的 CPU 核心数上限便可从 250 骤增至 2000。表 2 展示了分别使用 250 和 2000 个 CPU 核心并行计算时，前五步的时间开销以及平均单步迭代耗时。将多重网格层级从 4 降至 3，必然会降低 MG 方法本身的代数求解效率，导致在求解子结构宏观平衡方程上花费更多时间。尽管如此，计算中占据绝对主导地位的部分（即计算全局缩聚刚度矩阵）的时间，能够通过减少每个进程分配到的工作负载而被显著缩短。最终结果是，对于这个 1.28 亿单元的算例，在使用 2000 个 CPU 核心时，平均单步迭代时间大幅降至 7.0 秒，相较于 250 核，求解总效率提升了约 3 到 4 倍。假设超算的计费标准为每核时 0.05 元，使用 2000 核求解该算例的总花费为 38.9 元，而使用 250 核花费 17.4 元。这意味着我们用 2.2 倍的经济成本换取了 3.6 倍的效率飞跃，这在工程实践中被视为一种极其合理的折中（trade-off）。

<center><b>
表 2：不同多重网格层级和最大进程利用率下 PIML 增强拓扑优化算法的时间成本。
</b></center>

![[Ma2026_Table2.png]]

## 5.3 强扩展加速比

在强扩展性（strong scalability）测试中，保持问题规模不变，同时增加 CPU 核心的数量。将使用单核的并行 PIML 增强算法的时间开销记为 $t_{s1}$，将使用 $N$ 个核心时的对应时间记为 $t_{sN}$，则加速比被衡量为 $t_{s1}/t_{sN}$。由于处理器之间存在通信，随着 $N$ 的增加，加速比会下降且无法达到其理想极限（即线性加速比）。对于表 1 中包含 819 万单元的悬臂梁算例，多重网格层级设定为 3，偏微分方程（PDE）滤波半径设定为细观网格尺寸的 5 倍。表 3 展示了当 CPU 核心数从 1 增加到 128 时，所提算法的时间开销与加速比。

<center><b>
表 3：使用 819 万单元悬臂梁算例测试强扩展加速比。
</b></center>

![[Ma2026_Table3.png]]

可以观察到，在使用 4 核和 8 核时实现了超线性加速比（superlinear speedup）。这是因为每个处理器都拥有少量的高速缓存（high-speed cache）来存储可重复使用的数据，从而减少了 PDE 滤波和计算缩聚刚度矩阵的计算时间。这也与所提并行 PIML 增强算法极其出色的并行能力相一致。随着核心数量的进一步增加，通信开销逐渐占据主导地位，加速比随之逐渐下降。尽管如此，在使用 128 个 CPU 核心时，平均单步迭代耗时依然从 247.0 秒被大幅压缩至 3.9 秒，加速比达到 63.3，这也是相当可观的，表明算法没有出现显著的减速停滞趋势。

## 5.4 精度与计算效率分析

正如第 2.2 节所概述的，PIML 模型中关于子结构边界变形的线性假设虽然提升了计算效率，但也不可避免地引入了误差。为了评估这一问题，我们进一步对不同尺度下优化后的悬臂梁进行了全尺度（full-scale）有限元分析。问题设置遵循并行 PIML 增强算法的弱扩展原则，即单元数量与计算资源按比例同步增加。多重网格层级设定为 3，偏微分方程（PDE）滤波半径选取为细观网格尺寸的 5 倍。

在图 16 中，蓝色曲线代表使用 PIML 方法计算出的目标函数值与全尺度分析值之间的相对误差，右侧的颜色标尺指示了全尺度分析下真实的结构柔顺度。特别地，对于包含 145.8 万个细观单元的优化悬臂梁，观察到了高达 19.9% 的明显误差（$C_{\mathrm{PIML}} = 355.4$ 对比 $C_{\mathrm{exact}} = 443.7$），且其最终获得的目标函数值相对较差。这可以归因于，当设计域被较少数量的子结构（$18 \times 9 \times 9$ 个子结构）离散时，变形假设是不充分的。然而，随着问题规模的增大，这一问题得到了显著缓解。例如，当细观单元数量增加至 2.812 亿（对应 $104 \times 52 \times 52$ 个子结构）时，目标函数值的相对误差骤降至 4.2%（$C_{\mathrm{PIML}} = 249.2$ 对比 $C_{\mathrm{exact}} = 260.1$）。此外，优化后的结构展现出了更为丰富的结构细节，且其结构刚度（由于 $C_{\mathrm{exact}}$ 的下降）也得到了显著的提升。

另一方面，在更大规模的优化设计中追求更好的结构性能，不可避免地会牺牲计算效率。为了阐明这种权衡（trade-off），图 16 中的红色曲线展示了并行 PIML 增强算法中平均单步迭代耗时的变化情况。令人瞩目的是，随着问题规模的增大，计算时间并没有出现显著的增长。例如，使用 4294 个 CPU 核心求解包含 2.812 亿个细观单元的设计问题，单步迭代仅耗时 10.1 秒；而在完全相同的计算资源设置下，对该优化设计进行全尺度（高保真）有限元分析却需要耗时 594.0 秒。这有力地突显了并行 PIML 增强方法卓越的计算效率与可扩展性。

![[Ma2026_Fig16.png]]

<center><b>
图 16：不同尺度下并行 PIML 增强算法的精度、效率和优化结构性能。
</b></center>

## 5.5 追求最高 9000 CPU 核心下的最优求解效率

本小节探讨了在北京超级云计算中心（ChinaHPC）平台上，利用最多 9000 个可用核心，针对不同问题规模（从 1600 万到 34.5 亿个单元）所能达到的最快计算速度。针对不同的数值算例，设置了相应的 CPU 核心数和多重网格层级（multigrid level）。最大迭代次数和偏微分方程（PDE）滤波半径分别固定为 200 次和细观单元尺寸的 5 倍。例如，在包含 1600 万单元的悬臂梁算例中，将多重网格层级进一步降至 2，允许调用 2000 个核心，这比将多重网格层级设为 3 并调用 250 个核心，或者设为 4 并调用 16 个核心的算法配置获得了更快的速度。对于 34.5 亿单元的算例，由于可用核心数量的限制，多重网格层级只能设定为 4。详细结果如表 4 所示。

<center><b>
表 4：不同问题规模下实现的最快计算速度。
</b></center>

![[Ma2026_Table4.png]]

表 4 展示了所提算法在求解不同尺度三维拓扑优化问题时令人瞩目的高效率：求解包含数千万单元的算例仅需几分钟（例如，1600 万单元耗时 7.1 分钟，单步迭代 2.1 秒）；求解包含数亿单元的算例仅需几十分钟（例如，1.28 亿单元耗时 23.3 分钟，单步迭代 7.0 秒）；求解高达 10 亿单元级别的问题可控制在一小时内完成（例如，10.24 亿单元耗时 51.4 分钟，单步迭代 15.4 秒）。即使在计算资源不充足的情况下（指超算节点数受限），求解超过 100 亿自由度（DOFs）的算例依然能在 2 小时 20.1 分钟内完成。可以预期，如果拥有更强大的计算资源，并行 PIML 增强拓扑优化算法将能够以更高的求解效率，解决更大规模的三维拓扑优化问题。这种计算效率是传统方法难以达到的。

# 6 结论与展望

在本研究中，我们针对大规模拓扑优化问题开发了一种高性能的并行 PIML 增强方法。所提方法的成功主要可归结于几项关键技术。PIML 增强的子结构方法彻底免去了传统子结构方法中最耗时的计算环节，与全尺度分析相比，能够将自由度（DOFs）降低数个数量级。此外，并行计算进一步利用了子结构方法天然的可扩展性优势，并极大地提高了拓扑优化绝大部分求解过程的效率。在这种架构下，一旦 PIML 模型训练完成，所提的高性能算法便可直接应用于具有各种边界条件且由相同子结构离散的线弹性拓扑优化问题。不仅如此，包括无矩阵实现（matrix-free implementation）以及动态调整并行多重网格求解器层级（multigrid level）在内的一些数值技术，在时间开销、内存占用以及计算资源的充分利用之间实现了绝佳的平衡。

该算法的性能在个人计算机和高性能计算（HPC）环境中均得到了验证。在个人计算机上使用 40 个核心运行并行 PIML 增强算法，包含 1.28 亿个单元的悬臂梁算例的平均单步迭代耗时不到 2 分钟。所提算法在 HPC 环境中的有效性在不同问题规模下得到了证明，即从 1600 万单元到 34.5 亿单元的拓扑优化。新颖的结构构型和更优的结构性能，验证了进行大规模拓扑优化的必要性。具体而言，使用 1024 个 CPU 核心，包含 6552 万个单元的悬臂梁算例的平均单步迭代耗时仅为 5.5 秒；甚至对于超过 100 亿自由度（DOFs）的三维拓扑优化问题，使用 6750 个核心的平均单步迭代耗时也仅为 42.0 秒。

本研究可从多个不同方面进行扩展，以进一步提升其适用性。例如，可以采用子结构边界的高阶变形假设，从而提高 PIML 模型在结构分析中的精度。此外，通过将规则的六面体（砖形）子结构放宽（映射）为等参子结构（isoparametric substructures）[58]，本算法将非常适用于具有复杂设计域的大规模拓扑优化问题。本文所提出的并行 PIML 增强算法还可以与其他显式拓扑优化方法（例如移动可变形组件法，MMC 方法）相结合，从而在实际应用中更加直接地处理与几何相关的约束问题。

---

# 补充信息

## 利益冲突

通讯作者代表所有作者声明不存在利益冲突。

## 作者贡献

- **马新宇**（Xinyu Ma）：方法学（Methodology）、调查研究（Investigation）、形式分析（Formal analysis）、验证（Validation）、软件（Software）、撰写初稿（Writing – original draft）。
- **黄孟成**（Mengcheng Huang）：方法学（Methodology）、调查研究（Investigation）、软件（Software）、审阅与编辑（Writing – review and editing）。
- **杜宗亮**（Zongliang Du）：概念构思（Conceptualization）、方法学（Methodology）、资金获取（Funding acquisition）、指导（Supervision）、撰写初稿（Writing – original draft）、审阅与编辑（Writing – review and editing）。
- **郭一麟**（Yilin Guo）：调查研究（Investigation）、验证（Validation）、可视化（Visualization）、审阅与编辑（Writing – review and editing）。
- **刘畅**（Chang Liu）：验证（Validation）、可视化（Visualization）、审阅与编辑（Writing – review and editing）。
- **梅跃**（Yue Mei）：验证（Validation）、可视化（Visualization）、审阅与编辑（Writing – review and editing）。
- **郭旭**（Xu Guo）：概念构思（Conceptualization）、方法学（Methodology）、资金获取（Funding acquisition）、指导（Supervision）、审阅与编辑（Writing – review and editing）。

## 致谢

本研究得到了国家重点研发计划（项目批准号：2023YFB3309104）、国家自然科学基金（项目批准号：11821202、123721222）、辽宁省科技计划（项目批准号：2023JH2/101600044）和高等学校学科创新引智计划（“111 计划”，项目批准号：B14013）的资助。

---

# 参考文献

[1] M. P. Bendsøe, Optimal shape design as a material distribution problem, Struct. Optimization 1, 193 (1989).

[2] M. Zhou, and G. I. N. Rozvany, The COC algorithm, Part II: Topological, geometrical and generalized shape optimization, Comput. Methods Appl. Mech. Eng. 89, 309 (1991).

[3] M. P. Bendsøe, and O. Sigmund, *Topology Optimization: Theory, Methods, and Applications* (Springer, Berlin, Heidelberg, 2013).

[4] M. Y. Wang, X. Wang, and D. Guo, A level set method for structural topology optimization, Comput. Methods Appl. Mech. Eng. 192, 227 (2003).

[5] G. Allaire, F. Jouve, and A. M. Toader, Structural optimization using sensitivity analysis and a level-set method, J. Comput. Phys. 194, 363 (2004).

[6] Y. M. Xie, and G. P. Steven, A simple evolutionary procedure for structural optimization, Comput. Struct. 49, 885 (1993).

[7] X. Y. Yang, Y. M. Xie, G. P. Steven, and O. M. Querin, Bidirectional evolutionary method for stiffness optimization, AIAA J. 37, 1483 (1999).

[8] X. Guo, W. Zhang, and W. Zhong, Doing topology optimization explicitly and geometrically—A new moving morphable components based framework, J. Appl. Mech. 81, 081009 (2014).

[9] W. Zhang, J. Yuan, J. Zhang, and X. Guo, A new topology optimization approach based on moving morphable components (MMC) and the ersatz material model, Struct. Multidiscip. Optim. 53, 1243 (2016).

[10] Z. Du, T. Cui, C. Liu, W. Zhang, Y. Guo, and X. Guo, An efficient and easy-to-extend Matlab code of the moving morphable component (MMC) method for three-dimensional topology optimization, Struct. Multidiscip. Optim. 65, 158 (2022).

[11] D. C. Koper, C. A. W. Leung, L. C. P. Smeets, P. F. J. Laeven, G. J. M. Tuijthof, and P. A. W. H. Kessler, Topology optimization of a mandibular reconstruction plate and biomechanical validation, J. Mech. Behav. Biomed. Mater. 113, 104157 (2021).

[12] M. B. Dühring, J. S. Jensen, and O. Sigmund, Acoustic design by topology optimization, J. Sound Vib. 317, 557 (2008).

[13] J. H. K. Haertel, K. Engelbrecht, B. S. Lazarov, and O. Sigmund, Topology optimization of a pseudo 3D thermofluid heat sink model, Int. J. Heat Mass Transf. 121, 1073 (2018).

[14] Z. Du, H. Chen, and G. Huang, Optimal quantum valley Hall insulators by rationally engineering Berry curvature and band structure, J. Mech. Phys. Solids 135, 103784 (2020).

[15] J. H. Zhu, W. H. Zhang, and L. Xia, Topology optimization in aircraft and aerospace structures design, Arch. Comput. Methods Eng. 23, 595 (2016).

[16] X. Yan, D. Bao, Y. Zhou, Y. Xie, and T. Cui, Detail control strategies for topology optimization in architectural design and development, Front. Architect. Res. 11, 340 (2022).

[17] S. Mantovani, S. G. Barbieri, M. Giacopini, A. Croce, A. Sola, and E. Bassoli, Synergy between topology optimization and additive manufacturing in the automotive field, Proc. Inst. Mech. Eng. Part B 235, 555 (2021).

[18] S. Mukherjee, D. Lu, B. Raghavan, P. Breitkopf, S. Dutta, M. Xiao, and W. Zhang, Accelerating large-scale topology optimization: State-of-the-art and challenges, Arch. Comput. Methods Eng. 28, 4549 (2021).

[19] Y. Maksum, A. Amirli, A. Amangeldi, M. Inkarbekov, Y. Ding, A. Romagnoli, S. Rustamov, and B. Akhmetov, Computational acceleration of topology optimization using parallel computing and machine learning methods—Analysis of research trends, J. Ind. Inf. Integr. 28, 100352 (2022).

[20] N. Aage, and B. S. Lazarov, Parallel framework for topology optimization using the method of moving asymptotes, Struct. Multidiscip. Optim. 47, 493 (2013).

[21] J. París, I. Colominas, F. Navarrina, and M. Casteleiro, Parallel computing in topology optimization of structures with stress constraints, Comput. Struct. 125, 62 (2013).

[22] J. Martínez-Frutos, and D. Herrero-Pérez, Large-scale robust topology optimization using multi-GPU systems, Comput. Methods Appl. Mech. Eng. 311, 393 (2016).

[23] T. Borrvall, and J. Petersson, Large-scale topology optimization in 3D using parallel computing, Comput. Methods Appl. Mech. Eng. 190, 6201 (2001).

[24] N. Aage, E. Andreassen, and B. S. Lazarov, Topology optimization using PETSc: An easy-to-use, fully parallel, open source topology optimization framework, Struct. Multidiscip. Optim. 51, 565 (2015).

[25] N. Aage, E. Andreassen, B. S. Lazarov, and O. Sigmund, Giga-voxel computational morphogenesis for structural design, Nature 550, 84 (2017).

[26] H. Liu, Y. Tian, H. Zong, Q. Ma, M. Y. Wang, and L. Zhang, Fully parallel level set method for large-scale structural topology optimization, Comput. Struct. 221, 13 (2019).

[27] H. Lin, H. Liu, and P. Wei, A parallel parameterized level set topology optimization framework for large-scale structures with unstructured meshes, Comput. Methods Appl. Mech. Eng. 397, 115112 (2022).

[28] S. Kambampati, C. Jauregui, K. Museth, and H. A. Kim, Large-scale level set topology optimization for elasticity and heat conduction, Struct. Multidiscip. Optim. 61, 19 (2020).

[29] Y. Xiong, Z. L. Zhao, H. Lu, W. Shen, and Y. M. Xie, Parallel BESO framework for solving high-resolution topology optimisation problems, Adv. Eng. Softw. 176, 103389 (2023).

[30] E. A. Träff, A. Rydahl, S. Karlsson, O. Sigmund, and N. Aage, Simple and efficient GPU accelerated topology optimisation: Codes and applications, Comput. Methods Appl. Mech. Eng. 410, 116043 (2023).

[31] D. Herrero-Pérez, and P. J. Martínez-Castejón, Multi-GPU acceleration of large-scale density-based topology optimization, Adv. Eng. Softw. 157-158, 103006 (2021).

[32] D. Zhang, X. Zhai, L. Liu, and X. M. Fu, An optimized, easy-to-use, open-source GPU solver for large-scale inverse homogenization problems, Struct. Multidiscip. Optim. 66, 207 (2023).

[33] R. V. Woldseth, N. Aage, J. A. Bærentzen, and O. Sigmund, On the use of artificial neural networks in topology optimisation, Struct. Multidiscip. Optim. 65, 294 (2022).

[34] X. Lei, C. Liu, Z. Du, W. Zhang, and X. Guo, Machine learning-driven real-time topology optimization under moving morphable component-based framework, J. Appl. Mech. 86, 011004 (2019).

[35] R. Cang, H. Yao, and Y. Ren, One-shot generation of near-optimal topology through theory-driven machine learning, Comput.-Aided Des. 109, 12 (2019).

[36] D. Geng, J. Yan, Q. Xu, Q. Zhang, M. Zhou, Z. Fan, and H. Li, Real-time structure topology optimization using CNN driven moving morphable component method, Eng. Struct. 290, 116376 (2023).

[37] D. Wang, C. Xiang, Y. Pan, A. Chen, X. Zhou, and Y. Zhang, A deep convolutional neural network for topology optimization with perceptible generalization ability, Eng. Optim. 54, 973 (2022).

[38] Z. Du, X. Ma, W. Hao, Y. Liang, X. Zhang, H. Luo, and X. Guo, Real-time generative design of diverse optimized structures with controllable structural complexities and high quality, Extreme Mech. Lett. 77, 102321 (2025).

[39] H. Chi, Y. Zhang, T. L. E. Tang, L. Mirabella, L. Dalloro, L. Song, and G. H. Paulino, Universal machine learning for topology optimization, Comput. Methods Appl. Mech. Eng. 375, 112739 (2021).

[40] F. V. Senhora, H. Chi, Y. Zhang, L. Mirabella, T. L. E. Tang, and G. H. Paulino, Machine learning for topology optimization: Physics-based learning through an independent training strategy, Comput. Methods Appl. Mech. Eng. 398, 115116 (2022).

[41] T. Yue, H. Yang, Z. Du, C. Liu, K. I. Elkhodary, S. Tang, and X. Guo, A mechanistic-based data-driven approach to accelerate structural topology optimization through finite element convolutional neural network (FE-CNN), arXiv: 2106.13652.

[42] H. Li, S. Knapik, Y. Li, C. Park, J. Guo, S. Mojumder, Y. Lu, W. Chen, D. W. Apley, and W. K. Liu, Convolution hierarchical deep-learning neural network tensor decomposition (C-HiDeNN-TD) for high-resolution topology optimization, Comput. Mech. 72, 363 (2023).

[43] M. Huang, Z. Du, C. Liu, Y. Zheng, T. Cui, Y. Mei, X. Li, X. Zhang, and X. Guo, Problem-independent machine learning (PIML)-based topology optimization—A universal approach, Extreme Mech. Lett. 56, 101887 (2022).

[44] M. Huang, T. Cui, C. Liu, Z. Du, J. Zhang, C. He, and X. Guo, A problem-independent machine learning (PIML) enhanced substructure-based approach for large-scale structural analysis and topology optimization of linear elastic structures, Extreme Mech. Lett. 63, 102041 (2023).

[45] M. Huang, C. Liu, Y. Guo, L. Zhang, Z. Du, and X. Guo, A mechanics-based data-free problem independent machine learning (PIML) model for large-scale structural analysis and design optimization, J. Mech. Phys. Solids 193, 105893 (2024).

[46] O. Sigmund, A 99 line topology optimization code written in Matlab, Struct. Multidiscip. Optim. 21, 120 (2001).

[47] Y. Wada, T. Shimada, K. Nishiguchi, S. Okazawa, and M. Tsubokura, Billion-design-variable-scale topology optimization of vehicle frame structure in multiple-load case, Proc. Inst. Mech. Eng. D: J. Automob. Eng. 238, 3863 (2024).

[48] B. Hassani, and E. Hinton, A review of homogenization and topology optimization III—Topology optimization using optimality criteria, Comput. Struct. 69, 739 (1998).

[49] K. Svanberg, The method of moving asymptotes—A new method for structural optimization, Numer. Meth. Eng. 24, 359 (1987).

[50] J. Wu, C. Dick, and R. Westermann, A System for high-resolution topology optimization, IEEE Trans. Vis. Comput. Graph. 22, 1195 (2016).

[51] S. Abhyankar, J. Brown, E. M. Constantinescu, D. Ghosh, B. F. Smith, and H. Zhang, PETSc/TS: A modern scalable ODE/DAE solver library, arXiv: 1806.01437.

[52] J. E. Jones, and S. F. McCormick, Parallel multigrid methods, in: *Parallel Numerical Algorithms* (Springer, Dordrecht, 1997), pp. 203–224.

[53] B. S. Lazarov, and O. Sigmund, Filters in topology optimization based on Helmholtz-type differential equations, Int. J. Numer. Methods Eng. 86, 765 (2011).

[54] F. Wang, B. S. Lazarov, and O. Sigmund, On projection methods, convergence and robust formulations in topology optimization, Struct. Multidiscip. Optim. 43, 767 (2011).

[55] Y. Saad, and M. H. Schultz, GMRES: A generalized minimal residual algorithm for solving nonsymmetric linear systems, SIAM J. Sci. Stat. Comput. 7, 856 (1986).

[56] C. Iwamura, F. S. Costa, I. Sbarski, A. Easton, and N. Li, An efficient algebraic multigrid preconditioned conjugate gradient solver, Comput. Methods Appl. Mech. Eng. 192, 2299 (2003).

[57] V. P. Kumar, and A. Gupta, Analyzing scalability of parallel algorithms and architectures, J. Parallel Distrib. Comput. 22, 379 (1994).

[58] L. Zhang, M. Huang, C. Liu, Z. Du, T. Cui, and X. Guo, Problem-independent machine learning-enhanced structural topology optimization of complex design domains based on isoparametric elements, Extreme Mech. Lett. 72, 102237 (2024).
