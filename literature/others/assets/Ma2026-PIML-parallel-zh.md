# A high-performance parallel algorithm based on problem independent machine learning (PIML) for large-scale topology optimization
## 完整中文译文

> 原笔记：[[../Ma2026-PIML-parallel]]

---

# 摘要

尽管大规模拓扑优化能够提供广阔的设计空间，但“维度灾难”限制了其在实际工程中的广泛应用。多种加速技术已被集成到拓扑优化中，在大规模问题上引起了极大关注并取得了显著进展。本研究旨在探讨将并行计算与机器学习技术相结合，能为提升大规模拓扑优化算法的效率带来多大的增益。据此，提出了一种并行的、问题无关机器学习（PIML）增强的拓扑优化方法。PIML 模型大幅降低了缩聚刚度矩阵的维度及其计算开销，而并行计算进一步降低了每个进程的工作负载，并使得并行多重网格求解器的应用成为可能。此外，还开发了诸如无矩阵实现（matrix-free implementation）、均匀粗单元的直接缩聚以及调整计算资源限制等几种技术，以进一步提高计算效率。通过多个数值算例验证了所提方法的弱扩展效率、强扩展加速比以及最大可达效率，结果表明，与传统拓扑优化算法相比，该方法在可处理的问题规模和求解效率上均有显著提升。

**关键词：** 拓扑优化，大规模，问题无关机器学习（PIML），并行计算

# 1 引言

拓扑优化作为一种强大且合理的设计方法，近年来引起了广泛关注并取得了实质性进展 。特别是，各种拓扑优化方法——包括固体各向同性材料惩罚（SIMP）方法 [1-3]、水平集方法（LSM） [4,5]、进化结构优化（ESO）方法 [6,7] 以及移动可变形组件（MMC）方法 [8-10] 等——已被开发出来，并成功应用于各个研究领域 [11-14] 与工业实践中 [15-17] 。在工程应用中，大规模拓扑优化如今已获得了广泛的关注 。这归因于大规模、高分辨率的网格能够捕捉到更多的几何细节，这不仅有利于工程结构的集成设计，还能提供更广阔的设计空间，从而创造出更注重性能的新型结构 。然而，众所周知的“维度灾难”挑战为求解大规模三维拓扑优化问题带来了高昂的计算开销和低下的计算效率 。随着优化问题规模的增加，有限元分析（FEA）中的单次迭代变得非常耗时，导致内存使用量的激增和求解器难度的攀升 。这些挑战已经成为限制大规模拓扑优化在工程中实际应用的显著瓶颈 。

为了解决这些问题，在大规模拓扑优化的计算效率提升方面不断取得进展 。随着软硬件能力的显著提升，基于消息传递接口（MPI）或开放多处理（OpenMP）的中央处理器（CPU）并行计算，以及基于计算统一设备架构（CUDA）平台的图形处理器（GPU）并行计算，被用于加速拓扑优化过程 。早在2001年，Borrvall 和 Petersson 就利用高性能计算机（HPCs），结合区域分解技术实现了三维拓扑优化的并行计算 。随后，Aage 等人基于 SIMP 方法和便携、可扩展的科学计算工具包（PETSc）开发了大规模拓扑优化程序 。通过该程序，他们还使用 8000 个 CPU 完成了十亿体素分辨率下波音 777 机翼的优化设计 。Liu 等人引入了一种基于紧支径向基函数参数化水平集方法（LSM）的大规模拓扑优化方法，并成功将其扩展到非结构网格的拓扑优化中 。针对与弹性和热传导相关的大规模拓扑优化问题，Kambampati 等人实现了基于 LSM 和体动态 B+ 树的高效并行算法 。Xiong 等人利用开源计算平台 FEniCS，实现了基于 BESO 方法的高分辨率拓扑优化 。近年来，在 GPU 加速拓扑优化方面也涌现出许多优秀工作，例如单 GPU 并行化的 SIMP 算法、多 GPU 计算的拓扑优化 以及 GPU 加速的微结构设计 。

此外，随着人工智能的进步，机器学习（ML）已被引入拓扑优化中以加速求解过程 。例如，利用 ML 技术可以建立问题描述（包括设计域、边界和载荷条件）与优化设计之间的端到端映射 。基于训练有素的模型，几乎可以实现实时的结构拓扑优化 。为了提高 ML 模型的可扩展性，人工智能也被用于加速有限元分析（FEA） 。在双分辨率设置下，粗分辨率网格的 FEA 结果和细分辨率网格的材料刚度分布被用于预测灵敏度信息 ，与传统的拓扑优化算法相比，该方法可实现超过 30 倍的加速 。此外，提出了一种有限元卷积神经网络，通过建立高分辨率与低分辨率有限元解之间的关系，来构建高效的结构拓扑优化算法，将效率提高了多达一个数量级 。Li 等人提出了一种所谓的卷积-分层深度学习神经网络-张量分解框架，通过将 3D 力学问题分解为几个易于处理的小型 1D 问题，使用个人电脑来解决十亿级规模的拓扑优化问题 。最近，一种问题无关机器学习（PIML）技术被提出，该技术适用于具有任意设计域和载荷/边界条件的拓扑优化问题，可减少与 FEA 相关的计算时间，并能够将大规模 3D 拓扑优化问题的求解效率提升 2-3 个数量级 。

值得注意的是，上述大多数研究我们要么将并行计算要么将机器学习作为单一工具来使用（排除了那些使用 GPU 并行计算训练的端到端型 ML 模型）。沿着加速有限元分析（FEA）的思路，有必要研究通过同时利用并行计算（硬件层面）和 ML 算法（算法层面），我们能在多大程度上拓宽线弹性结构大规模拓扑优化的边界 。为此，本文提出了一种全并行化的 PIML 增强拓扑优化框架 。PIML 模型极大地降低了系统平衡线性代数方程组的维度，而并行计算则进一步减少了每个进程中的计算任务 。此外，还集成了诸如多尺度形函数的无矩阵实现（matrix-free implementation）以及解除计算资源限制等多种技术，以在结构拓扑优化问题的可处理维度和效率上实现突破 。

本文其余部分的组织结构如下：第二节介绍了针对 SIMP 方法的 PIML 增强子结构方法的基本思想 。接着，第三节详细说明了并行 PIML 增强拓扑优化算法的实现 。第四部分展示了所提算法在个人电脑和超级计算机平台上的数值验证 。在第五节探讨了所提并行算法的可扩展性（scalability）和最优求解效率之后 ，最后一节给出了结论性评述 。

# 2 面向线弹性结构大规模拓扑优化的 PIML 增强子结构方法

本节首先给出了结构拓扑优化的问题描述，随后简要介绍了用于大规模拓扑优化的原始 PIML 增强框架，以阐明将其与并行计算相结合的必要性。

## **2.1 结构拓扑优化的问题表述**

对于在 $\mathbb{R}^N (N = 1, 2, \text{或 } 3)$ 空间中占据且具有适当几何正则性的开有界域 $\Omega$ 的线弹性固体，其平衡状态可通过弱形式描述为：

寻找 $\boldsymbol{u} \in \boldsymbol{H}^1(\Omega)$，

使得 $\int_{\Omega} \mathbb{E}(\boldsymbol{x}) : \nabla\boldsymbol{u} : \nabla\boldsymbol{v} dV = \int_{\Omega} \boldsymbol{f} \cdot \boldsymbol{v} dV + \int_{S_t} \boldsymbol{t} \cdot \boldsymbol{v} dS, \quad (1)$

对所有 $\boldsymbol{v} \in \boldsymbol{H}_0^1(\Omega)$ 且在 $S_u$ 上 $\boldsymbol{u} = \bar{\boldsymbol{u}}$ 成立，

其中 $\boldsymbol{H}^1(\Omega) = [H^1(\Omega)]^N$，而 $H^1(\Omega)$ 表示在 $L^2(\Omega)$（即定义在 $\Omega$ 上的平方可积函数空间）中具有阶数小于或等于 1 的广义偏导数的 Sobolev 空间。$\mathbb{E}(\boldsymbol{x})$ 为弹性张量。$\boldsymbol{f}$ 和 $\boldsymbol{t}$ 分别代表体力密度以及定义在 Neumann 边界 $S_t$ 上的面力密度。符号 $\bar{\boldsymbol{u}}$ 表示定义在 Dirichlet 边界 $S_u$ 上的给定（规定）位移，而 $\boldsymbol{v} \in \boldsymbol{H}_0^1(\Omega)$ 是测试函数，其中 $\boldsymbol{H}_0^1(\Omega) = \{ \boldsymbol{v} \mid \boldsymbol{v} \in \boldsymbol{H}^1(\Omega), \text{在 } S_u \text{ 上 } \boldsymbol{v} = \mathbf{0} \}$。

在经典的 SIMP（固体各向同性材料惩罚）框架 [46] 下，每个有限元被赋予一个密度值 $\rho_e$ ，并且第 $e$ 个单元的杨氏模量被插值表示为 $E_e = E_{\min} + \rho_e^3(E_0 - E_{\min})$，$e = 1, 2, ..., n$ 。其中 $E_0$、$E_{\min}$ 和 $n$ 分别表示固体材料的杨氏模量、为避免可能出现的矩阵奇异性而设定的空隙（孔洞）材料的杨氏模量，以及设计域中有限元的总数 。体积约束下最小柔顺性设计问题的数学形式被离散化为 ：

寻找 $\boldsymbol{\rho} = (\rho_1, \rho_2, ..., \rho_n)^{\text{T}}$ ，
最小化 $c = \boldsymbol{F}^{\text{T}}\boldsymbol{U}$ ， 
满足约束： $\boldsymbol{K}(\boldsymbol{\rho})\boldsymbol{U} = \boldsymbol{F}$ ， 
$g = V(\boldsymbol{\rho}) - \bar{V} \le 0$ ， 
$0 \le \rho_i \le 1, \quad i = 1, 2, ..., n$ ， (2)

其中 $\boldsymbol{K}(\boldsymbol{\rho})$、$\boldsymbol{U}$ 和 $\boldsymbol{F}$ 分别为全局刚度矩阵、节点位移向量和外部节点力向量 。符号 $V$ 为固体材料的体积分数，$\bar{V}$ 为其上限 。

对于大规模三维拓扑优化问题，求解平衡状态的线性代数方程组将极其耗时且需要庞大的内存。为了缓解这一问题，Huang 等人 [43,44] 提出了所谓的面向大规模结构分析与拓扑优化的 PIML 增强子结构方法，正如后续小节所述。

## **2.2 PIML 增强的子结构方法——串行算法**

### _2.2.1 经典子结构方法_

在经典的子结构方法中，设计域被离散为一组子结构 $\Omega^j, j = 1, 2, ..., N_s$。对于由细观尺度上 $m \times m \times m$ 个有限元组成的每一个 $\Omega^j$，与其关联的自由度（DoFs）被划分为边界自由度（用下标“b”标识）和内部自由度（用下标“i”标识），如图 1 所示。那么，$\Omega^j$ 的离散平衡方程可以分解为：

$$\boldsymbol{K}^j \boldsymbol{u}^j = \begin{pmatrix} \boldsymbol{K}_{\text{bb}}^j & (\boldsymbol{K}_{\text{ib}}^j)^{\text{T}} \\ \boldsymbol{K}_{\text{ib}}^j & \boldsymbol{K}_{\text{ii}}^j \end{pmatrix} \begin{pmatrix} \boldsymbol{u}_{\text{b}}^j \\ \boldsymbol{u}_{\text{i}}^j \end{pmatrix} = \begin{pmatrix} \boldsymbol{f}_{\text{b}}^j \\ \boldsymbol{f}_{\text{i}}^j \end{pmatrix}, \quad (3)$$

其中 $\boldsymbol{K}^j$ 和 $\boldsymbol{u}^j$ 分别是第 $j$ 个子结构的刚度矩阵和节点位移向量。符号 $\boldsymbol{u}_{\text{b}}^j, \boldsymbol{f}_{\text{b}}^j \in \mathbb{R}^{n_{\text{b}}^j}$ 和 $\boldsymbol{u}_{\text{i}}^j, \boldsymbol{f}_{\text{i}}^j \in \mathbb{R}^{n_{\text{i}}^j}$ 分别是第 $j$ 个子结构边界节点和内部节点的节点位移向量与节点力向量。不失一般性地，假定内部节点的节点力向量 $\boldsymbol{f}_{\text{i}}^j$ 为零。那么方程 (3) 可以等价地表达为其缩聚形式：

$$\boldsymbol{K}_{\text{s}}^j \boldsymbol{u}_{\text{b}}^j = \boldsymbol{f}_{\text{b}}^j, \quad (4)$$

其中 $\boldsymbol{K}_{\text{s}}^j = \boldsymbol{K}_{\text{bb}}^j - (\boldsymbol{K}_{\text{ib}}^j)^{\text{T}} (\boldsymbol{K}_{\text{ii}}^j)^{-1} \boldsymbol{K}_{\text{ib}}^j$