# A problem-independent machine learning (PIML) enhanced substructure-based approach for large-scale structural analysis and topology optimization of linear elastic structures

## 完整中文译文

> 原笔记：[[../Huang2023-PIML-substructure]]
> Zotero 条目：`zotero://select/library/items/5XMDKI6A`
> PDF 附件：`zotero://open-pdf/library/items/DAC5HA9I`
> 说明：本页用于放置 Huang 2023 的完整中文译稿；当前先建立章节框架，译文后续逐步补入。

---

# 0 元数据

- 论文：Huang et al. 2023, *Extreme Mechanics Letters*, 63:102041
- DOI：10.1016/j.eml.2023.102041
- Better BibTeX key：`huangProblemindependentMachineLearning2023`
- Zotero item key：`5XMDKI6A`
- PDF attachment key：`DAC5HA9I`

# 摘要

由高度非均质材料组成的结构的结构分析通常涉及求解大规模线性代数方程组，即使在线弹性范围内这也是非常耗时的。此外，迭代大规模有限元分析的巨大计算成本也阻碍了拓扑优化作为强大设计工具的广泛使用，特别是当所需的设计分辨率非常高时。为了打破阻碍大规模结构分析和设计优化问题高效求解的瓶颈，在本文中，提出了一种通用的机器学习（ML）增强的基于子结构的框架。其核心思想是求助于经典的基于子结构的有限元分析方法，并通过离线训练的深度神经网络，在表征子结构内材料分布的参数与对应的缩聚刚度矩阵/数值形函数之间建立隐式映射。与大多数现有的 ML 增强方法相反，所提出的框架真正独立于结构几何、边界条件和外部载荷的形式，并且一旦离线训练完成，就可以应用于求解由相同类型的偏微分方程控制的各种边值问题。借助现代人工智能技术，所提出的方法在某种意义上复兴了有限元分析中经典的子结构方法。与传统范式相比，对于测试的大规模算例，它能够在令人满意的精度下实现 $10^4-10^5$ 倍的求解效率。该方法的有效性还在非自伴随拓扑优化问题（即 3D 柔顺机构设计）中得到了验证。最后，为了展示所提出方法在处理超大规模三维问题方面的能力，在不借助任何并行计算技术的情况下，在一台笔记本电脑上求解了一个包含约 $10^9$ 个设计变量和 $3 \times 10^9$ 个自由度（Dofs）的三维拓扑优化问题。

# 1 引言

如今，有限元分析（FEA）已经成为工业界分析和设计产品不可或缺的工具。与此同时，基于 FEA 发展起来的拓扑优化技术为工程师创造创新结构和产品提供了强大的工具。这两种技术都已在各个应用领域取得了成功 [1-4]。然而，求解拓扑优化问题通常需要执行数百次 FEA，这实际上是一个非常耗时的过程，特别是对于大规模三维（3D）问题。因此，如何减少拓扑优化中 FEA 的计算量一直是一个长期受到广泛关注的热点研究课题。人们已经提出了许多方法来加速求解过程，包括并行技术 [5-9]、多尺度方法 [10-12]、多分辨率拓扑优化方法 [13-17]、设计变量缩减方法 [18,19] 以及自由度消除策略 [20] 等等。

近年来，随着机器学习技术的快速发展，ML 在高维空间建立端到端函数映射的能力已得到广泛证实和接受，例如在图像识别 [21]、机器翻译 [22] 以及求解高维偏微分方程 [23] 等方面。这些成功的应用为 ML 在极少人工干预下从高维数据集中提取独特特征的能力提供了有力证据。受这些成就的鼓舞，研究人员开始探索为湍流建模 [24,25]、材料发现 [26,27] 和数值模拟 [28] 等开发 ML 增强方法的可能性。特别地，许多研究人员利用机器学习技术来减少与连续体结构拓扑优化相关的计算量。例如，在最近一些研究的方法中，机器学习技术被用于在给定的优化参数（如设计域的宽度/长度、边界条件以及外部载荷的位置/大小）与优化结构之间建立端到端的关联 [29-31]，从而实现实时拓扑优化。尽管沿着这个方向已经取得了令人信服的结果，但是当这些端到端方法被用于处理与训练数据集中的样本问题截然不同的问题时，它们的表现仍缺乏深入的探索 [32]。

与基于端到端 ML 模型建立雄心勃勃的实时拓扑优化方法的尝试相反，许多研究人员也提出在多尺度拓扑优化框架下开发 ML 增强的拓扑优化方法。例如，Chi 等人提出了一种有效的拓扑优化在线机器学习（ML）方法，该方法在多分辨率框架下运行，通过从拓扑优化过程的初始迭代中收集训练数据 [33]。后来，通过集成离线训练策略进一步增强了该方法，将模型训练过程与实际拓扑优化中的实施分离开来 [34]。在这个改进的方法中，建立了一个 ML 模型来预测在精细分辨率下更新设计变量所需的灵敏度。这是通过将粗分辨率超单元上的单一排布位移场和局部材料密度作为输入来实现的。数值算例表明，该方法可以处理规模高达 3800 万设计变量的设计问题，并可提供高达 30 倍的加速比。在文献 [35] 中，提出了一种有限元卷积神经网络（FE-CNNs）来构建高效的结构拓扑优化算法 [35]。构建的 FE-CNN 函数充当高分辨率和低分辨率有限元解之间的映射，以减少优化的计算时间。数值实验表明，使用该方法可以大幅减少高分辨率拓扑优化中涉及的计算工作量。最近，Li 等人提出了一种被称为卷积层次深度学习神经网络-张量分解（C-HiDeNN-TD）的新框架，仅使用单台个人计算机（PC）来处理计算上极具挑战性的十亿级规模拓扑优化问题 [36]。通过应用精心设计的变量分离方案，C-HiDeNN-TD 技术将超大规模 3D FEA 问题的求解分解为一系列较小的一维（1D）问题，从而显著降低了搜索高分辨率 3D 拓扑设计的计算成本。

尽管上述方法取得了显著成就，但仍然存在一些值得进一步探索的挑战性问题。首先，开发出的 ML 模型并非完全独立于问题设置，特别是在端到端方法中。这些模型中的大多数仅适用于一组特定的问题设置。一旦涉及的参数发生改变，就必须相应地建立一个新的 ML 模型。这极大地削弱了 ML 增强方法的通用性。其次，由于在大多数端到端 ML 增强方法中，必须求解一定数量的边值甚至优化问题以生成样本，因此训练过程可能非常耗时。在这种情况下，只能生成数量有限的样本（特别是对于大规模高分辨率拓扑优化问题），这将不可避免地降低生成的 ML 模型的预测能力，因为基于 ML 的预测的准确性高度依赖于训练样本的数量和质量。第三，在建立 ML 模型时必须遵守的输入和输出参数之间明确无误的关系，尚未得到认真考虑。例如，粗分辨率超晶胞的位移场实际上是由设计域中所有单元的材料密度决定的，而不仅仅如某些先前工作中所假设的那样，只由位于超晶胞内的单元的材料密度决定。最后，宏观上假设的材料密度场（例如文献 [34] 中）无法表征具有微尺度特征尺寸的结构细节，因此无法充分发挥高分辨率拓扑优化的优势。

为了解决上述挑战，Huang 等人提出了一种用于大规模拓扑优化的通用且与问题无关的机器学习（PIML）框架 [37]。在该框架中，所谓的扩展多尺度有限元方法（EMsFEM）被用于 FEA，而相应的 EMsFEM 形函数（代表了粗分辨率单元的形函数与其单元级材料密度之间的隐式映射）是通过离线 ML 方案构建的。由于 ML 仅在粗分辨率单元上进行，且 EMsFEM 形函数实际上是问题无关的，因此一旦建立，它们就可以用于求解由同类型偏微分方程（PDEs）控制、具有各种问题设置的任何拓扑优化问题。针对二维问题的数值算例表明，该方法确实能够显著减少 FEA 的时间。然而，值得注意的是，在文献 [37] 中，仅研究了二维（2D）问题，基于 PIML 方法的有效性及其潜力尚未得到充分开发。

在当前工作中，我们在更一般的基于子结构的 FEA 框架下重构了 PIML 方法，并提出通过考虑保秩（rank-preserving）属性来提高 PIML 的质量。通过这种方式，建立了一个用于 3D 线弹性结构大规模分析和拓扑优化的通用 PIML 框架。结果表明，与传统拓扑优化方法相比，所提出的 PIML 增强的子结构方法可将求解效率提高几个数量级。通过使用所提出的方法，即使是对于 FEA 涉及 10 亿设计变量和 30 亿自由度（Dofs）的超大规模拓扑问题，也可以在个人计算机上高效求解。

本文的其余部分组织如下。在第 2 节中，详细描述了提出的问题无关机器学习（PIML）增强的子结构方法。在第 3 节中，讨论了与其数值实现相关的问题。在第 4 节中，求解了一组大规模拓扑优化问题以证明提出方法的有效性。在第 5 节中，我们对当前工作进行了总结，并探讨了可能的扩展和未来工作。

# 2 方法

## 2.1 线弹性分析与拓扑优化问题的数学模型

占据 $\mathbb{R}^N$ ($N=1, 2$ 或 $3$) 中具有适当几何规律性的开有界域 $\Omega$ 的固体的通用线弹性分析问题，可以通过位移场 $\boldsymbol{u}$ 以下面的弱形式公式化：
$$
\begin{aligned}
&\text{寻找 } \boldsymbol{u} \in H^1(\Omega)\\
&\text{使得 } a(\boldsymbol{u}, \boldsymbol{v}) = l(\boldsymbol{v}), \quad \forall \boldsymbol{v} \in H_0^1(\Omega),\\
&\boldsymbol{u} = \bar{\boldsymbol{u}}, \quad \text{在 } S_u \text{ 上},
\end{aligned} \tag{1}
$$
其中 $H^1(\Omega) = [H^1(\Omega)]^N$，且 $H^1(\Omega)$ 表示在 $L^2(\Omega)$（在 $\Omega$ 上定义的平方可积函数空间）中具有小于或等于一阶广义偏导数的函数的 Sobolev 空间。式 (1) 中的双线性形式 $a(\boldsymbol{u}, \boldsymbol{v})$ 和线性形式 $l(\boldsymbol{v})$ 分别表示为
$$
a(\boldsymbol{u}, \boldsymbol{v}) = \int_{\Omega} \mathbb{E}(\boldsymbol{x}) : \nabla \boldsymbol{u} : \nabla \boldsymbol{v} dV \tag{2}
$$
和
$$
l(\boldsymbol{v}) = \int_{\Omega} \boldsymbol{f} \cdot \boldsymbol{v} dV + \int_{S_t} \boldsymbol{t} \cdot \boldsymbol{v} dS, \tag{3}
$$
在式 (2) 和 (3) 中，$\mathbb{E}(\boldsymbol{x})$ 是弹性张量，$\boldsymbol{f}$ 和 $\boldsymbol{t}$ 分别是体积力密度和 Neumann 边界 $S_t$ 上的面力。符号 $\bar{\boldsymbol{u}}$ 表示在 Dirichlet 边界 $S_u$ 上的给定强制位移，$\boldsymbol{v} \in H_0^1(\Omega)$ 是测试函数，且 $H_0^1(\Omega) = \{ \boldsymbol{v} | \boldsymbol{v} \in H^1(\Omega), \boldsymbol{v} = \boldsymbol{0} \text{ 在 } S_u \text{ 上} \}$。

相应地，在经典固体各向同性材料惩罚（SIMP）框架下，线弹性结构的通用拓扑优化问题可以被公式化为：
$$
\begin{aligned}
&\text{寻找 } \rho(\boldsymbol{x}) \in L^\infty(\Omega), \quad \boldsymbol{u} \in H^1(\Omega)\\
&\text{最小化 } f(\rho, \boldsymbol{u})\\
&\text{满足条件：}\\
&\quad a_\rho(\boldsymbol{u}, \boldsymbol{v}) = l(\boldsymbol{v}), \quad \forall \boldsymbol{v} \in H_0^1(\Omega),\\
&\quad \boldsymbol{u} = \bar{\boldsymbol{u}}, \quad \text{在 } S_u \text{ 上},\\
&\quad 0 \leq \rho(\boldsymbol{x}) \leq 1, \forall \boldsymbol{x} \in \Omega,\\
&\quad g_i(\rho, \boldsymbol{u}) \leq 0, \quad i = 1, \dots, m,
\end{aligned} \tag{4}
$$
其中 $a_\rho(\boldsymbol{u}, \boldsymbol{v}) = \int_{\Omega} (\rho(\boldsymbol{x}))^p \mathbb{E}(\boldsymbol{x}) : \nabla \boldsymbol{u} : \nabla \boldsymbol{v} dV$，$p$ 表示惩罚参数。在式 (4) 中，$f(\rho, \boldsymbol{u})$ 和 $g_i(\rho, \boldsymbol{u}) \leq 0$, $i = 1, \dots, m$ 分别是一般的目标泛函/函数和约束泛函/函数。

## 2.2 有限元分析的子结构方法

经过适当的有限元（FE）离散化后，式 (1) 中边值问题的近似解 $\boldsymbol{u}^h \in \mathbb{R}^n$ 可以通过求解以下线性代数方程组找到：
$$
\boldsymbol{K}^h \boldsymbol{u}^h = \boldsymbol{f}^h, \tag{5}
$$
其中 $\boldsymbol{K}^h \in \mathbb{R}^{n \times n}$ 是全局刚度矩阵，$n$ 表示总自由度数，$\boldsymbol{f}^h \in \mathbb{R}^n$ 是等效节点力向量。当所考虑的结构由高度非均质材料组成时，通常需要非常密集的 FE 网格来精确表征材料分布，以确保结构分析的准确性。这不可避免地会导致 $\boldsymbol{K}^h$ 维度巨大，并因此显著增加求解时间，因为求解式 (5) 的计算复杂度近似正比于 $n^2 \sim n^3$，这取决于所采用的求解过程以及 $\boldsymbol{K}^h$ 的条件数。因此，在不牺牲求解精度的前提下，减少式 (5) 求解时间的一个自然方法就是使 $n$ 的值尽可能小。

减少有限元分析中自由度数的一种经典方法是所谓的子结构方法。在这种方法中，如图 1 所示，首先将结构的离散化模型分解为一组子结构 $\Omega_h^j$（$j = 1, \dots, N_s$），并且对于每个 $\Omega_h^j$，根据它们的相对位置将与其关联的所有节点分类为边界节点 $N^{jb}$ 和内部节点 $N^{ji}$。

![[Huang2023_Fig1.png]]
<center>图 1：$m=5$ 的三维子结构示意图。</center>

那么 $\Omega_h^j$ 的离散平衡方程可以表示为
$$
\boldsymbol{K}_j^h \boldsymbol{u}_j^h =
\begin{pmatrix}
\boldsymbol{K}_{jbb}^h & (\boldsymbol{K}_{jib}^h)^\top \\
\boldsymbol{K}_{jib}^h & \boldsymbol{K}_{jii}^h
\end{pmatrix}
\begin{pmatrix}
\boldsymbol{u}_{jb}^h \\
\boldsymbol{u}_{ji}^h
\end{pmatrix}
=
\begin{pmatrix}
\boldsymbol{f}_{jb}^h \\
\boldsymbol{0}
\end{pmatrix}, \tag{6}
$$
其中 $\boldsymbol{u}_{jb}^h \in \mathbb{R}^{Nn_{jb}}$ 和 $\boldsymbol{u}_{ji}^h \in \mathbb{R}^{Nn_{ji}}$（即分别总共有 $n_{jb}$ 个边界节点和 $n_{ji}$ 个内部节点）是分别与 $N^{jb}$ 和 $N^{ji}$ 相关的位移向量。在式 (6) 中，$\boldsymbol{f}_{jb}^h$ 是与 $\boldsymbol{u}_{jb}^h$ 相关的外部载荷向量，并且不失一般性地假设与 $\boldsymbol{u}_{ji}^h$ 相关的外部载荷为零。

由式 (6)，可计算出 $\Omega_h^j$ 上的凝聚形式平衡方程为
$$
\tilde{\boldsymbol{K}}_j^h \boldsymbol{u}_{jb}^h = \tilde{\boldsymbol{f}}_{jb}^h, \tag{7}
$$
其中 $\tilde{\boldsymbol{K}}_j^h = \boldsymbol{K}_{jbb}^h - (\boldsymbol{K}_{jib}^h)^\top (\boldsymbol{K}_{jii}^h)^{-1} (\boldsymbol{K}_{jib}^h)$ 就是所谓的缩聚刚度矩阵（condensed stiffness matrix）。一旦确定了 $\boldsymbol{u}_{jb}^h$，我们就得到了 $\boldsymbol{u}_{ji}^h = - (\boldsymbol{K}_{jii}^h)^{-1} (\boldsymbol{K}_{jib}^h) \boldsymbol{u}_{jb}^h$。

缩聚刚度矩阵 $\tilde{\boldsymbol{K}}_j^h$ 和 $\tilde{\boldsymbol{f}}_{jb}^h$ ($j = 1, \dots, N_s$) 可以分别组装成全局缩聚刚度矩阵 $\tilde{\boldsymbol{K}}^h = \bigwedge_{j=1}^{N_s} \tilde{\boldsymbol{K}}_j^h$ 和全局缩聚外载荷向量 $\tilde{\boldsymbol{f}}^h = \bigwedge_{j=1}^{N_s} \tilde{\boldsymbol{f}}_j^h$。缩聚位移向量 $\boldsymbol{u}_b^h = ((\boldsymbol{u}_{1b}^h)^\top, \dots, (\boldsymbol{u}_{N_s b}^h)^\top)^\top$ 可以通过求解 $\tilde{\boldsymbol{K}}^h \boldsymbol{u}_b^h = \tilde{\boldsymbol{f}}^h$ 确定。进一步地，如果在 $\Omega_h^j$ 中的位移场 $\boldsymbol{u}_j(\boldsymbol{x}) \in \mathbb{R}^N$ 被插值为
$$
\boldsymbol{u}_j^h(\boldsymbol{x}) = \boldsymbol{N}_b(\boldsymbol{x})\boldsymbol{u}_{jb}^h + \boldsymbol{N}_i(\boldsymbol{x})\boldsymbol{u}_{ji}^h, \tag{8a}
$$
其中 $\boldsymbol{N}_b(\boldsymbol{x}) \in \mathbb{R}^{N \times Nn_{jb}}$ 和 $\boldsymbol{N}_i(\boldsymbol{x}) \in \mathbb{R}^{N \times Nn_{ji}}$ 分别是与 $\boldsymbol{u}_{jb}^h$ 和 $\boldsymbol{u}_{ji}^h$ 相关联的形函数。例如，当 $N = 2$ 时，我们有
$$
\boldsymbol{N}_b(\boldsymbol{x}) = 
\begin{bmatrix}
N_{jb1}(\boldsymbol{x}) & & \dots & N_{jbn_{jb}}(\boldsymbol{x}) & \\
& N_{jb1}(\boldsymbol{x}) & \dots & & N_{jbn_{jb}}(\boldsymbol{x})
\end{bmatrix} \tag{8b}
$$
以及
$$
\boldsymbol{N}_i(\boldsymbol{x}) = 
\begin{bmatrix}
N_{ji1}(\boldsymbol{x}) & & \dots & N_{jin_{ji}}(\boldsymbol{x}) & \\
& N_{ji1}(\boldsymbol{x}) & \dots & & N_{jin_{ji}}(\boldsymbol{x})
\end{bmatrix}. \tag{8c}
$$
根据式 (8) 和 $\boldsymbol{u}_{ji}^h = - (\boldsymbol{K}_{jii}^h)^{-1} (\boldsymbol{K}_{jib}^h) \boldsymbol{u}_{jb}^h$，我们可以得到
$$
\boldsymbol{u}_j^h(\boldsymbol{x}) = \boldsymbol{N}_b(\boldsymbol{x})\boldsymbol{u}_{jb}^h + \boldsymbol{N}_i(\boldsymbol{x})\boldsymbol{u}_{ji}^h = \boldsymbol{N}_j(\boldsymbol{x})\boldsymbol{u}_{jb}^h, \tag{9}
$$
其中 $\boldsymbol{N}_j(\boldsymbol{x}) = \left[ \boldsymbol{N}_b(\boldsymbol{x}) - \boldsymbol{N}_i(\boldsymbol{x}) (\boldsymbol{K}_{jii}^h)^{-1} (\boldsymbol{K}_{jib}^h) \right] \in \mathbb{R}^{N \times Nn_{jb}}$ 是与子结构 $\Omega_h^j$ 相关联的形函数。

值得注意的是，$\tilde{\boldsymbol{K}}^h$ 的维度可能远小于 $\boldsymbol{K}^h$ 的维度。实际上，如果每个子结构被均匀地离散为 $m \times m$ 个单元，那么比率 $r = \dim \tilde{\boldsymbol{K}}^h / \dim \boldsymbol{K}^h$ 的值可以被估计为 $r = 1 - \left(\frac{m-1}{m+1}\right)^N$。此外，如果假设 $\boldsymbol{u}_{jb}^h = \boldsymbol{L}\boldsymbol{a}$，其中 $\boldsymbol{a} \in \mathbb{R}^l$ 表示广义参数向量，而 $\boldsymbol{L} \in \mathbb{R}^{Nn_{jb} \times l}$ 表示常数插值矩阵，则 $r$ 的值可进一步缩减为 $r = \frac{l}{N(m+1)^N}$。例如，如果 $l = 24$, $m = 5$ 且 $N = 3$，那么 $r$ 的值将等于 0.037。这意味着 $\tilde{\boldsymbol{K}}^h$ 的维度大约是 $\boldsymbol{K}^h$ 维度的 3%。理论上，FEA 的计算复杂度将降至 $(3\%)^3$，这无疑将极大地缩短 FEA 所需的时间。

## 2.3 通过机器学习高效构建 $\tilde{\boldsymbol{K}}_j^h$ 和 $\boldsymbol{N}_j(\boldsymbol{x})$

尽管子结构方法在减少自由度数量（即全局刚度矩阵的维度）方面非常有效，但如果缩聚刚度矩阵 $\tilde{\boldsymbol{K}}^h$ 是通过**在线（online）**过程生成的，则结构分析的计算效率无法得到显著提升。这是因为计算每个子结构（$j = 1, \dots, N_s$）的 $\tilde{\boldsymbol{K}}_j^h = \boldsymbol{K}_{jbb}^h - (\boldsymbol{K}_{jib}^h)^\top (\boldsymbol{K}_{jii}^h)^{-1} (\boldsymbol{K}_{jib}^h)$ 和 $\boldsymbol{N}_j(\boldsymbol{x})$ 所涉及的矩阵求逆和乘法操作同样非常耗时，特别是当子结构的数量（即 $N_s$）非常大时。这就解释了为什么子结构方法并没有被广泛用于求解包含高度非均质材料的通用大规模结构分析和拓扑优化问题，在这些问题中，不同子结构的 $\tilde{\boldsymbol{K}}_j^h$ 和 $\boldsymbol{N}_j(\boldsymbol{x})$ 总是有很大差异（在结构分析中），因此必须经常以耗时的、逐个子结构计算的方式动态构建（在拓扑优化中）。

为了充分利用子结构方法带来的显著自由度缩减优势，同时又有效地节省生成 $\tilde{\boldsymbol{K}}_j^h$ 和 $\boldsymbol{N}_j(\boldsymbol{x})$ 的计算开销，在当前工作中，我们提出通过**离线（offline）**机器学习过程，在表征 $\Omega_h^j$ 内材料分布的参数与 $\tilde{\boldsymbol{K}}_j^h$ 及 $\boldsymbol{N}_j(\boldsymbol{x})$ 的元素之间建立某种**与问题无关（problem-independent）**的隐式映射，从而构建 $\tilde{\boldsymbol{K}}_j^h$ 和 $\boldsymbol{N}_j(\boldsymbol{x})$（示意图见图 2）。

![[Huang2023_Fig2.png]]
<center>图 2：PIML 方案示意图。</center>

一旦建立了这些映射，就可以绕过相应的矩阵操作，因此 $\tilde{\boldsymbol{K}}_j^h$ 和 $\boldsymbol{N}_j(\boldsymbol{x})$ 几乎可以瞬间构建完成。

与现有的用于结构分析和优化的 ML 辅助方法相比，所提出的问题无关机器学习（PIML）方案的显著特征可总结如下：
(1) 在每个子结构中表征材料分布的参数与 $\tilde{\boldsymbol{K}}_j^h$ 及 $\boldsymbol{N}_j(\boldsymbol{x})$ 的元素之间存在着唯一的关系。这一属性赋予了机器学习问题以适定性，并在理论上保证了学习过程的有效性以及鲁棒性。
(2) 所提出的学习方案是真正问题无关的，因为 $\tilde{\boldsymbol{K}}_j^h$ 和 $\boldsymbol{N}_j(\boldsymbol{x})$ 都可以局部唯一地确定，而无需考虑所讨论问题的边界条件、设计域的拓扑/形状和外部载荷。一旦 ML 模型训练良好，它们就可以应用于求解受同类偏微分方程控制的任何结构分析和拓扑优化问题。
(3) 在所提出的 ML 框架下，可以高效地生成大量高质量、没有过多数值噪声的样本。这对于确保学习结果的准确性非常重要。实际上，生成每个用于后续机器学习过程的样本，只需要求解一个小规模的线性代数方程组（即 $m \times m$ 且 $m \ll n$）。例如，当 $m = 10$ 时，大约 3 个小时即可生成十万个样本。

尽管学习缩聚刚度和子结构形函数的核心思想很简单，但获得高质量的机器学习结果并不是一项微不足道的任务。在下一节中，将描述训练过程的实施细节。

# 3 PIML 增强子结构方法

<!-- 待补完整中文译文。 -->

## 3.1 神经网络架构

为了降低计算 $\boldsymbol{N}_j^h$ 和 $\tilde{\boldsymbol{K}}_j^h$ 的时间成本，本文构建了一个离线训练的机器学习模型，以取代耗时的在线计算过程。为了说明该方法的通用性，本文使用的机器学习模型仅仅是一个普通的前馈神经网络。该前馈神经网络由一个输入层、几个隐藏层和一个输出层组成，可以简单地表示为：
$$
\boldsymbol{y} = f_l \dots f_2(f_1(\boldsymbol{\rho})) \tag{12}
$$
其中向量 $\boldsymbol{\rho} \in \mathbb{R}^{M \times 1}$ 和 $\boldsymbol{y} \in \mathbb{R}^{N \times 1}$ 分别表示输入层和输出层。符号 $f_1, \dots, f_l$ 表示隐藏层，它们是预先编程的函数表达式。

针对不同的问题，$\boldsymbol{\rho}$ 和 $\boldsymbol{y}$ 是不同的，需要根据问题进行具体设置。在本文提出的方法中，分别使用了两个前馈神经网络来预测 $\boldsymbol{N}_j^h$ 和 $\tilde{\boldsymbol{K}}_j^h$ 的元素。值得注意的是，并非 $\boldsymbol{N}_j^h$ 和 $\tilde{\boldsymbol{K}}_j^h$ 的所有元素都需要作为前馈神经网络的输出。对于 $\boldsymbol{N}_j^h = \begin{bmatrix} \boldsymbol{N}_{j1} \\ \boldsymbol{N}_{j2} \end{bmatrix}$，由于 $\boldsymbol{N}_{j1}$ 是一个已知的单位矩阵，因此只需要预测 $\boldsymbol{N}_{j2}$ 部分；对于 $\tilde{\boldsymbol{K}}_j^h$，利用其作为对称矩阵的性质，只需要学习 $\tilde{\boldsymbol{K}}_j^h$ 的上三角阵列部分。

此外，根据式 (7) 和式 (10)，对于每个 $j = 1, \dots, N_s$，基于有限元分析（FEA）的理论知识，$\boldsymbol{N}_j^h$ 和 $\tilde{\boldsymbol{K}}_j^h$ 可以由该子结构内每个有限元的材料属性和单元类型唯一确定。因此，当模型中的单元类型一致时（在当前工作中，对于二维问题使用了双线性插值单元，即 $N_l(\boldsymbol{x}) = \frac{1}{4}(1-x_{1l} x_1)(1-x_{2l} x_2)$），$\boldsymbol{N}_j^h$ 和 $\tilde{\boldsymbol{K}}_j^h$ 仅由子结构中单元的材料属性决定。

对于线弹性材料，材料参数包括杨氏模量和泊松比。与泊松比相比，杨氏模量在工业设计和分析过程中更为关键。因此，在本文提出的方法中，子结构内单元的杨氏模量被用作前馈神经网络的输入参数，而泊松比固定为 0.3。对于均匀离散为 $m \times m$ 个单元的子结构，输入参数 $\boldsymbol{\rho}$ 的维度（即 $M$）等于 $m \times m$。

## 3.2 内嵌力学机制的机器学习

在 3.1 节中，尽管我们利用单位矩阵和对称矩阵的性质显著减少了前馈神经网络的输出参数，但 $\boldsymbol{N}_j^h$ 和 $\tilde{\boldsymbol{K}}_j^h$ 仍然分别有高达 $N n_{ji} \times N n_{jb}$ 和 $(N n_{jb} + 1)N n_{jb} / 2$ 个输出参数。此外，从力学原理出发，为了保证子结构发生刚体位移时结构应变能为零，有限元分析的解空间应包含子结构的平动和转动。因此，在机器学习过程中，必须对 $\boldsymbol{N}_j^h$ 和 $\tilde{\boldsymbol{K}}_j^h$ 施加相应的几何约束。同时，这些几何约束也可以进一步大幅减少与 $\boldsymbol{N}_j^h$ 和 $\tilde{\boldsymbol{K}}_j^h$ 对应的神经网络输出参数。对于 $\boldsymbol{N}_j^h = \begin{bmatrix} \boldsymbol{N}_{j1} \\ \boldsymbol{N}_{j2} \end{bmatrix}$，由于 $\boldsymbol{N}_{j1}$ 是已知的，几何约束只需施加在 $\boldsymbol{N}_{j2}$ 上。以三维情形为例，如果子结构发生整体平移，则需要满足以下约束：
$$
\begin{aligned}
&\sum_{l=1}^{n_{jb}} (\boldsymbol{N}_{j2})_{l,xx}^k = 1, \sum_{l=1}^{n_{jb}} (\boldsymbol{N}_{j2})_{l,xy}^k = 0, \sum_{l=1}^{n_{jb}} (\boldsymbol{N}_{j2})_{l,xz}^k = 0, \quad k=1,\dots,n_{ji}, \\
&\sum_{l=1}^{n_{jb}} (\boldsymbol{N}_{j2})_{l,yx}^k = 0, \sum_{l=1}^{n_{jb}} (\boldsymbol{N}_{j2})_{l,yy}^k = 1, \sum_{l=1}^{n_{jb}} (\boldsymbol{N}_{j2})_{l,yz}^k = 0, \quad k=1,\dots,n_{ji}, \\
&\sum_{l=1}^{n_{jb}} (\boldsymbol{N}_{j2})_{l,zx}^k = 0, \sum_{l=1}^{n_{jb}} (\boldsymbol{N}_{j2})_{l,zy}^k = 0, \sum_{l=1}^{n_{jb}} (\boldsymbol{N}_{j2})_{l,zz}^k = 1, \quad k=1,\dots,n_{ji}.
\end{aligned} \tag{13}
$$

类似地，如果子结构以恒定角位移 $\boldsymbol{\theta} \in \mathbb{R}^{3 \times 1}$ 旋转，则需要施加以下方程约束以避免虚假应变：
$$
\boldsymbol{I}_{n_{ji}} \otimes \boldsymbol{\omega_x} = \boldsymbol{N}_{j2} (\boldsymbol{I}_{n_{jb}} \otimes \boldsymbol{\omega_X}) \tag{14}
$$
其中，采用与单位矩阵 $\boldsymbol{I}_{n_{ji}}$（大小为 $n_{ji} \times n_{ji}$）的 Kronecker 乘积 $\otimes$ 来匹配向量 $\boldsymbol{x}$ 的维度。$\boldsymbol{\omega}$ 是由角位移 $\boldsymbol{\theta}$ 计算得到的旋转矩阵。符号 $\boldsymbol{x} = [\boldsymbol{x}_1, \dots, \boldsymbol{x}_{n_{ji}}]^T \in \mathbb{R}^{3 n_{ji} \times 1}$ 和 $\boldsymbol{X} = [\boldsymbol{X}_1, \dots, \boldsymbol{X}_{n_{jb}}]^T \in \mathbb{R}^{3 n_{jb} \times 1}$ 分别表示内部节点和边界节点的坐标。

类似地，对于 $\tilde{\boldsymbol{K}}_j^h$，应满足以下几何约束：
$$
\tilde{\boldsymbol{K}}_j^h \boldsymbol{\varphi} = \boldsymbol{0}, \tag{15}
$$
其中符号 $\boldsymbol{\varphi} \in \mathbb{R}^{3 n_{jb} \times 6}$ 是一个常数矩阵，并且 $\boldsymbol{\varphi}$ 由子结构发生整体平移或以恒定角度旋转时的位移向量组成。通过施加上述几何约束，在 $N=3$ 时，$\boldsymbol{N}_j^h$ 和 $\tilde{\boldsymbol{K}}_j^h$ 的神经网络输出数量可以分别减少到 $N n_{ji} \times (N n_{jb} - 6)$ 和 $(N n_{jb} - 5)(N n_{jb} - 6) / 2$。

此外，如果假设子结构边界具有固定的变形模式，如线性或抛物线形式，则可以进一步对 $\boldsymbol{N}_j^h$ 和 $\tilde{\boldsymbol{K}}_j^h$ 施加额外的几何约束。例如，假设子结构边界变形模式为线性（这对于大规模结构是合理的），可以添加以下几何约束：
$$
\boldsymbol{u}_j^h = \begin{bmatrix} \boldsymbol{u}_{jb}^h \\ \boldsymbol{u}_{ji}^h \end{bmatrix} = (\boldsymbol{N}_j^h)^L \boldsymbol{u}_c; \quad (\boldsymbol{N}_j^h)^L = \boldsymbol{N}_j^h \boldsymbol{L} \tag{16a}
$$
$$
(\tilde{\boldsymbol{K}}_j^h)^L = \boldsymbol{L}^T \left( \boldsymbol{K}_{jbb}^h - \boldsymbol{K}_{jib}^{hT} (\boldsymbol{K}_{jii}^h)^{-1} \boldsymbol{K}_{jib}^h \right) \boldsymbol{L} \tag{16b}
$$

## 3.3 神经网络训练与样本生成

上一节详细介绍了 PIML 的网络结构。本小节将简要描述 PIML 的训练过程，包括样本生成、损失函数和训练方法。

首先，与需要在一个实际优化过程中收集训练样本的端到端实时拓扑优化 [29–31, 38–40] 或 Fernando 等人 [34] 提出的通用神经网络相比，本文提出的 PIML 方法的训练样本可以通过随机过程生成。这是因为 $\boldsymbol{N}_j^h$ 和 $\tilde{\boldsymbol{K}}_j^h$ 仅由子结构内部单元的杨氏模量决定。由于本文仅研究线弹性问题，因此可以将杨氏模量归一化，并在 $[0, 1]$ 范围内通过随机过程生成训练样本。对于均匀离散为 $m \times m$ 个单元的子结构，可以通过 $m \times m$ 个随机数来构成一个用于训练的样本。

其次，神经网络的输出是去除了不变量（即 $\boldsymbol{N}_{j1}$）以及 $\boldsymbol{N}_{j2}$ 和 $\tilde{\boldsymbol{K}}_j^h$ 中的非独立量之后剩余的部分，这对于问题无关机器学习方法的成功至关重要。因此，为了更准确地衡量神经网络的输出，必须根据式 (13)–(15) 在神经网络输出的基础上补全 $\boldsymbol{N}_{j2}$ 和 $\tilde{\boldsymbol{K}}_j^h$。预测输出与精确输出（即 $\boldsymbol{N}_{j2}$ 和 $\tilde{\boldsymbol{K}}_j^h$）之间的均方误差被用作第一类损失函数。此外，为了保证子结构增强宏观分析的正确性，直接由神经网络预测得到的刚度矩阵 $\tilde{\boldsymbol{K}}_j^h$ 应与由神经网络预测得到的 $\boldsymbol{N}_j^h$ 计算出来的矩阵保持一致。因此，本文为用于预测 $\boldsymbol{N}_j^h$ 的神经网络的训练定义了另一类损失函数。第二类损失函数是由预测的 $\boldsymbol{N}_j^h$ 计算得到的缩聚刚度矩阵与由预测 $\tilde{\boldsymbol{K}}_j^h$ 的神经网络得到的矩阵之间的均方误差。与物理信息神经网络 [23] 类似，第二类损失函数就像是添加在 PIML 输出上的物理约束。然而，第二类损失函数不可避免地会增加训练的计算量。因此，在 PIML 的训练过程中，第二类损失函数仅在训练过程的最后阶段被加入，以检验训练效果或进一步降低预测值与真实输出之间的均方误差。

在当前工作中，我们构建并训练了五组神经网络（$\boldsymbol{N}_j^h$ 和 $\tilde{\boldsymbol{K}}_j^h$，或 $(\boldsymbol{N}_j^h)^L$ 和 $(\tilde{\boldsymbol{K}}_j^h)^L$）。对于 $N = 2$ 的情况，共有三组神经网络。第一组用于预测 $m = 5$ 时的 $\boldsymbol{N}_j^h$ 和 $\tilde{\boldsymbol{K}}_j^h$。第二组和第三组神经网络用于预测 $(\boldsymbol{N}_j^h)^L$ 和 $(\tilde{\boldsymbol{K}}_j^h)^L$，其中一组为 $m = 5$，另一组为 $m = 10$。对于 $N = 3$ 的情况，有两组神经网络用于预测 $(\boldsymbol{N}_j^h)^L$ 和 $(\tilde{\boldsymbol{K}}_j^h)^L$，即对应的 $m = 5$ 和 $m = 10$。为了简洁起见，这里我们仅详细介绍用于预测 $m = 5$ 且 $N = 3$ 时 $(\boldsymbol{N}_j^h)^L$ 和 $\tilde{\boldsymbol{K}}_j^h$ 的神经网络。其他的神经网络与此类似。

对于三维实体模型，当 $m = 5$ 时，$\boldsymbol{N}_{j2}$ 的数值总数将高达 4608。而如果 $m = 10$，输出量将达到 39,366 个。要用单一的前馈神经网络获得如此极佳的隐式映射将非常困难。为了降低训练难度，我们使用了一系列神经网络来预测 $(\boldsymbol{N}_j^h)^L$。详细而言，单一神经网络的输出仅为 $(\boldsymbol{N}_{j2})^L$ 的一部分数值，如图 3 所示。

![[Huang2023_Fig3.png]]
<center>图 3：预测三维子结构 $(\boldsymbol{N}_{j2})^L$ 的神经网络架构。</center>

对于 $m = 5$ 的情况，构建并训练了四个神经网络，并生成了 400,000 个随机样本对其进行训练。对于每个神经网络，总共有 15 个隐藏层，其中的激活函数分别设置为 [tanh, elu, tanh, elu, tanh, elu, tanh, elu, elu, tanh, elu, tanh, elu, tanh, elu]，每层中激活函数的数量分别设置为 [60, 80, 100, 120, 140, 160, 180, 200, 180, 160, 140, 120, 100, 80, 60]。对于二维问题，使用单一的前馈神经网络即足以预测 $\tilde{\boldsymbol{K}}_j^h$ 或 $(\tilde{\boldsymbol{K}}_j^h)^L$。

## 3.4 基于 PIML 的拓扑优化流程

一旦本文提出的神经网络模型训练完毕，它便可用于分析和优化任何使用双线性插值单元离散化的问题。与传统的子结构分析方法相比，该方法唯一的区别在于使用神经网络来替代传统计算，以求得 $\boldsymbol{N}_j^h$ 和 $\tilde{\boldsymbol{K}}_j^h$。

正如前文所述，为了保证理论自洽性并确保细网格上的总应变能等于粗网格上的总应变能，在数值计算中观察到，即便预测的形函数 $\boldsymbol{N}_j^h$（或 $(\boldsymbol{N}_j^h)^L$）包含相当大的误差，利用下式 (17) 计算得到的刚度矩阵仍十分接近精确解：
$$
\tilde{\boldsymbol{K}}_j^h = (\boldsymbol{N}_j^h)^\top \boldsymbol{K}_j^h \boldsymbol{N}_j^h; \quad (\tilde{\boldsymbol{K}}_j^h)^L = ((\boldsymbol{N}_j^h)^L)^\top \boldsymbol{K}_j^h (\boldsymbol{N}_j^h)^L. \tag{17}
$$
因此，在本文框架内，提供了两种结构分析的方法，即计算 $\tilde{\boldsymbol{K}}_j^h$ 或 $(\tilde{\boldsymbol{K}}_j^h)^L$ 的两种途径：第一种方法是直接使用神经网络预测相应的缩聚刚度矩阵以追求效率；第二种方法则是仅通过神经网络预测 $\boldsymbol{N}_j^h$（或 $(\boldsymbol{N}_j^h)^L$），并结合式 (17) 计算 $\tilde{\boldsymbol{K}}_j^h$ 或 $(\tilde{\boldsymbol{K}}_j^h)^L$。通过这样做，可以充分利用刚度矩阵维数的计算优势。

采用所提方法进行拓扑优化的相应流程图如图 4 所示。

![[Huang2023_Fig4.png]]
<center>图 4：所提出的基于 PIML 的拓扑优化方法的流程图。</center>

此外，在拓扑优化过程中，只有细分辨率网格的密度分布会发生变化。同时，当子结构的局部密度分布由完全相同的值组成时，$\boldsymbol{N}_{j2}$ 的值等于纯实体材料子结构的值 $(\boldsymbol{N}_{j2})_{\text{solid}}$。此外，仅包含一种材料的子结构的缩聚刚度矩阵可如下计算：$\rho_m (\tilde{\boldsymbol{K}}_j^h)_{\text{solid}}$，其中 $\rho_m$ 和 $(\tilde{\boldsymbol{K}}_j^h)_{\text{solid}}$ 分别表示该纯实体材料子结构的平均密度和缩聚刚度矩阵。因此，为了进一步提高生成子结构缩聚刚度矩阵的效率，引入了阈值 $\rho_v$ 来判断子结构的局部密度分布是否由同一个值组成。具体而言，如果局部密度分布的最大值与平均密度 $\rho_m$ 之间的绝对差值小于 $\rho_v$，则可以使用 $\rho_m (\tilde{\boldsymbol{K}}_j^h)_{\text{solid}}$ 来计算该子结构的缩聚刚度矩阵。有了这个判断准则，生成子结构缩聚刚度矩阵的计算时间可以显著减少，特别是对于大规模算例或可用体积分数较低的设计问题。

# 4 数值算例

本节提供了一个 MBB 梁算例、一个柔顺机构算例和一个短悬臂梁算例，以验证本文提出的通用机器学习（ML）增强拓扑优化框架的效率和普适性。最后，通过求解一个包含超过 10 亿个细分辨率单元的短悬臂梁算例，展示了该方法处理超大规模三维问题的能力。为了说明神经网络模型的问题无关性，本节中 $m$ 值相同的神经网络均完全相同。所有算例涉及的参数均假设为无量纲。实体材料和弱材料的杨氏模量分别设置为 $E_0 = 1$ 和 $E_{\min} = 10^{-7}$，泊松比均为 0.3。此外，我们设定利用神经网络生成子结构刚度矩阵的阈值 $\rho_v = 10^{-4}$。所有细分辨率单元均由八节点六面体单元（brick elements）表示，其单元刚度矩阵使用二阶高斯积分计算。密度过滤的半径 $r_{\min}$ 均相对于细分辨率单元的尺寸而定。

## 4.1 MBB 梁算例

图 5 中的算例将展示所提方法的卓越求解效率。在顶面中心点施加单位集中载荷。为了说明所提方法对于大规模问题的效率，这里并未利用对称性进行简化，而是对整体模型进行求解。

![[Huang2023_Fig5.png]]
<center>图 5：MBB 梁算例的问题设定。</center>

为了检验所提方法在不同细分辨率单元数量下的性能，我们通过改变细分辨率网格尺寸来改变单元数量，同时保持可用体积分数和密度过滤半径不变。需要说明的是，对于 MBB 梁算例，缩聚刚度矩阵是通过式 (17) 计算得到的，而在柔顺机构优化算例中，刚度矩阵是由神经网络直接预测的，以进一步提高计算效率。此外，采用优化准则（OC）法更新设计变量，并在最后五次连续迭代中目标函数值的相对变化小于 0.0002 时终止优化过程。所有算例均在一台配备 Intel(R) Xeon(R) Gold 6256 3.60GHz CPU 和 512.0GB RAM 的工作站上求解。

在图 6 中，展示了采用 $m = 5$ 的机器学习模型在细分辨率单元数量 $N_F$ 变化时得到的优化结构。显然，随着网格加密，得到的优化结构能够保留相似的宏观拓扑形状，但具有更加清晰的边界。这证明了该方法在不同网格分辨率下的适用性。这也由于以下事实：随着网格的加密，一方面，具有线性变形假设的子结构方法的解越来越接近相应的精确解，另一方面，实际的过滤半径也变得更小。此外，图 6 中所有优化结构的对称性也验证了所提方法的有效性。

![[Huang2023_Fig6.png]]
<center>图 6：在细分辨率单元数量 ($N_F$) 变化时获得的优化结构，采用 $m = 5$ 的情况。</center>

图 7 展示了 $N_F = 1,647,750$ 和 $N_F = 11,718,750$ 时每次迭代的平均时间成本，其中粗网格 FEA 的时间指的是 PIML 方法中计算粗分辨率和细分辨率位移的总时间。而粗网格刚度矩阵的时间指的是由神经网络生成每个子结构的多尺度形函数和单元刚度矩阵所需的时间。最后，优化准则的时间是使用优化准则法更新设计变量的时间。值得注意的是，由于对于 $N_F = 1,647,750$ 和 $N_F = 11,718,750$ 的情况，经典的 SIMP 方法计算时间较长，本文仅报告了前 10 次迭代的平均时间，并且没有给出最终优化结果。此外，受限于计算机存储，对于 $N_F = 37,989,750$ 的模型没有应用传统的 SIMP 方法。具体而言，如图 7 所示，使用传统 SIMP 算法时，细网格下的有限元分析时间几乎占总时间的 100%，而对于本文提出的方法，即使在 $N_F = 11,718,750$ 的情况下，粗网格 FEA 的时间成本也与粗网格刚度矩阵的生成时间处于同一数量级。

![[Huang2023_Fig7.png]]
<center>图 7：在 $N_F = 1,647,750$ 和 $N_F = 11,718,750$ 的情况下，经典 SIMP 方法和基于 PIML 的方法在优化过程中每次迭代的平均时间成本。</center>

## 4.2 柔顺机构算例

由于灵敏度分析需要伴随场（adjoint field），柔顺机构设计无疑比刚度设计问题更为复杂。为了进一步测试本文所提算法的普适性，本小节提供了一个三维柔顺机构设计问题，其粗分辨率网格为 $60 \times 20 \times 40$，子结构的 $m = 10$，如图 8 所示。顶面长 200、宽 30 的阴影区域被固定。在左底边的中点施加驱动力 $F_{\text{in}}$，目标函数是最大化右侧表面中心点在 z 方向的位移（$U_{\text{out}}$）。体积分数和过滤半径分别设置为 0.2 和 5。输入/输出点处弹簧的弹性常数为 $K_{\text{in}} = K_{\text{out}} = 0.1$。

![[Huang2023_Fig8.png]]
<center>图 8：柔顺机构算例的问题设定。</center>

如图 9 所示，两种优化结果在结构上相似，呈对称的铰链状，正如预期的那样导致了输出端口的向上运动。图 9 还提供了两种方法在每一步中各部分的平均时间成本，结果表明神经网络可以将计算缩聚刚度矩阵的时间减少 60% 以上。最后，使用 EMsFEM 对最优结构进行分析，图 9 中输出点的相应位移记为 $U_{\text{EMs}}^{\text{out}}$，而 $U_{\text{PIML}}^{\text{out}}$ 表示利用神经网络预测的缩聚刚度矩阵所获得的位移。两种方法优化结果中输出点位移的相对误差（即 $|1 - U_{\text{PIML}}^{\text{out}} / U_{\text{EMs}}^{\text{out}}|$）分别为 7.56% 和 7.65%。比较这两种最优设计，可以发现图 9(a) 的结果包含了更多的细节和更平滑的边界，并且图 9(b) 中 $U_{\text{EMs}}^{\text{out}}$ 的值较小，这意味着性能较差。这可能是由于本研究采用的神经网络架构相对简单，从而牺牲了神经网络模型的预测精度。此外，预测的形函数和预测的缩聚刚度矩阵通常无法满足式 (17) 所描述的关系，换句话说，在利用神经网络预测缩聚刚度矩阵的 PIML 方法中，子结构应变能的总和必须等于细分辨率网格的应变能。我们将在未来的工作中尝试解决这一问题。

![[Huang2023_Fig9.png]]
<center>图 9：通过不同缩聚刚度矩阵计算方法得到的优化结构。</center>

## 4.3 短悬臂梁算例

在一台笔记本电脑上求解了一个包含 10.24 亿细分辨率单元的短悬臂梁，如图 10 所示。左侧表面固定，在右下边缘施加均布载荷。子结构的总数（$N_C$）等于 102.4 万个（$160 \times 80 \times 80$），子结构的 $m = 10$。并且缩聚刚度矩阵通过式 (17) 计算。

![[Huang2023_Fig10.png]]
<center>图 10：包含 10.24 亿个细分辨率单元的短悬臂梁算例的问题设定。</center>

经过 137 次迭代后，在 9-10 天内获得了过滤半径为 5 的优化结构，如图 11 所示。值得注意的是，在整个优化过程中没有使用如并行计算等任何加速技术。唯一的区别是粗分辨率网格上的线性方程组使用了迭代法进行求解。单次迭代步骤的平均时间为 5677.8 秒，如图 12 所示。对于此算例，由于 SIMP 方法中设计变量的数量庞大，即使使用优化准则法来更新设计变量，相关的时间成本仍占总时间的约 26%。

![[Huang2023_Fig11.png]]
<center>图 11：具有 10.24 亿细分辨率单元的优化悬臂梁。</center>

![[Huang2023_Fig12.png]]
<center>图 12：包含 10.24 亿细分辨率单元的短悬臂梁算例每次迭代的平均时间成本。</center>

# 5 结论

在当前工作中，为了显著缩短求解时间，本文在经典的子结构分析框架下开发了一种机器学习增强方法，用于涉及高度非均质材料的大规模线弹性结构分析和拓扑优化。其核心思想是借助子结构方法降低相应线性代数方程组的维数，并通过深度神经网络几乎瞬时地获得缩聚刚度矩阵/数值形函数。与一些代表性的模型相比，所提出的机器学习模型的显著优势在于它是真正的问题无关的，因为当前的机器学习模型仅与所采用的有限元离散格式有关。一旦该模型训练成功，它就可以应用于求解受相同偏微分方程控制、具有任何问题设定（例如边界条件、外部载荷）的边值问题。所提出的方法可以极大地节省计算时间，特别是对于大规模拓扑优化问题。结果表明，利用所提出的方法，在一台笔记本电脑上即可求解一个包含 $10^9$ 个设计变量和 $3 \times 10^9$ 个自由度的三维拓扑优化问题，而无需借助于任何并行计算技术和硬件。

目前的工作还可以在多个方向上进行改进和扩展。相应的路线图可以总结如下：

(1) 在目前的工作中，仅探讨了沿子结构边界的线性位移插值。然而，这将高估子结构的刚度，尤其是当子结构数量（即 $N$）较小时。缓解该问题的一种可能方法是采用如文献 [41] 中那样的高阶位移插值方案，代价是略微增加最终线性代数方程组中的未知数数量。此外，所提出的方法可以结合其他强大的数据压缩和模型降阶技术，以减少表征材料分布和数值形函数的参数数量，从而有望构建更加轻量级且有效的 ML 模型。

(2) 所提出的方法建立在子结构框架之下，这是边界值问题数值求解的通用范式。因此，它可以应用于求解在多物理场仿真（如流固耦合）、未进行尺度分离的高度非均质材料数值均匀化、涉及裂纹扩展/相变/损伤萌生的自由边界前沿追踪等中出现的各种大规模分析/优化问题。在上述所有应用中，由于子结构中材料属性的空间或时间变化，子结构的缩聚刚度矩阵会发生动态变化，所提出的 ML 增强方法可用于对此提供瞬时预测。最后但同样重要的一点是，考虑到动态子结构方法的成功，有理由期望所提出的方法在分析机械系统的大规模动态问题方面也具有巨大的潜力。

(3) 目前的 ML 增强方法具有与其他成熟方法相结合的潜力，例如等几何分析方法 (IGA)、有限元胞法 (FCM) 和切割有限元法 (CutFEM)，以构建全新的有限元分析框架。例如，利用本文所开发的技术，可以建立一个 ML 模型来预测等几何单元的刚度与其控制点坐标之间的关系。这可以有效缓解传统 IGA 中与数值积分相关的大量计算压力。所提出的方法还可以通过学习相应切割模式下的切割单元刚度矩阵，从而与 CutFEM 无缝集成。这可能开辟一条使用固定结构化网格进行高效、准确有限元分析的新途径，即通过将复杂的物理域嵌入到网格中，从而完全避开繁琐的网格生成过程。这是一个非常有趣的研究课题，值得进一步深入调查。
