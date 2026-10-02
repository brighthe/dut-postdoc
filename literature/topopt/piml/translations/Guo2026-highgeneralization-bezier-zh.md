---
title: "翻译：High-Generalization AI-Enhanced mechanical analysis and topology optimization via cubic bézier interpolation of substructure boundary displacements"
tags:
  - translation
  - PIML
  - topology-opt
  - bezier
  - DeepONet
  - substructure
status: "done"
date_created: 2026-08-04
date_updated: 2026-09-10
source: "../sources/Guo2026-highgeneralization-bezier.pdf"
citekey: "guoHighGeneralizationAIEnhancedMechanical2026"
language: "zh-CN"
---

# High-Generalization AI-Enhanced mechanical analysis and topology optimization via cubic bézier interpolation of substructure boundary displacements

---

# 信息

- **中文标题**：基于子结构边界位移三次 Bézier 插值的高泛化 AI 增强力学分析与拓扑优化
- **作者**：Yilin Guo（郭一麟）$^1$；Chang Liu（刘畅）$^{1,*}$；Zongliang Du（杜宗亮）$^{1,2}$；Yibo Jia（贾一波）$^1$；Chao Jiang（姜超）$^1$；Xu Guo（郭旭）$^{1,2,*}$；Changyu Shen（申长雨）$^{1,3,*}$
- **单位**：
  - $1$: 大连理工大学工程力学系、工业装备结构分析优化与 CAE 软件国家重点实验室（大连 116023）
  - $2$: 大连工业软件研究院（大连 116085）
  - $3$: 郑州大学材料科学与工程学院、材料成型及模具教育部重点实验室（郑州 450002）
- **期刊**：*Computer Methods in Applied Mechanics and Engineering*
- **卷 / 期 / 文章号**：456: 118955
- **DOI**：10.1016/j.cma.2026.118955
- **收稿 / 修回 / 录用 / 在线发表**：2025-09-18 / 2026-03-27 / 2026-03-27 / 2026-04-08
- **通讯作者**：Chang Liu（c.liu@dlut.edu.cn）；Xu Guo（guoxu@dlut.edu.cn）；Changyu Shen（shency@zzu.edu.cn）

# 摘要

近年来，诸多研究致力于利用机器学习（ML）提高大规模结构分析与拓扑优化的效率；然而，强大的泛化能力以及高精度的训练与预测精度仍然难以兼得。本文将子结构方法的通用性与算子学习框架的高精度优势相结合。在子结构分析的框架下，训练深度算子网络（DeepONet）以学习从三次 Bézier 插值边界位移场到对应子结构内部位移场的高保真映射。该映射仅依赖于子结构内部的材料分布，在理论上具有唯一对应关系。数值算例证实了所提框架的有效性与稳定性。相较于精确子结构方法以及基于线性边界位移假定的 ML 增强变体，本文方法在计算效率与计算精度之间取得了极具优势的平衡。

**关键词**：大规模分析（Large-scale analysis）；拓扑优化（Topology optimization）；高阶有限元（Higher-order finite element）；子结构方法（Substructure method）；深度算子网络（Deep operator networks）

---

# 1 引言

在工程实践中，由高度非均匀材料组成的结构——以下统称为**高度异质结构**（Highly Heterogeneous Structures）——屡见不鲜，典型代表包括纤维增强复合材料、包含大量微裂纹或微孔隙的岩石、多功能生物结构以及具有非均匀单胞的点阵结构，如图 1 所示。这类结构的一个决定性特征是构成材料的力学性质在空间分布上具有极强的不均匀性。针对此类系统的有限元分析（FEA），通常需要极高分辨率的网格（包含数百万乃至数十亿个单元）来刻画材料的空间分布并获得精确的结构响应。之所以存在这种要求，是因为在传统的基于位移的有限元格式中，通常假设每个单元内具有均匀的材料属性，以确保单元位移插值函数的光滑性 [5]。与此同时，随着增材制造的飞速发展，旨在通过优化设计域内材料空间分布以实现最优结构力学性能的拓扑优化技术，近年来在工业界引起了广泛关注 [6]。在广为流行的基于人工密度的拓扑优化框架中 [7–9]，同样需要在设计域上建立高分辨率的网格离散，以获得具有精细特征尺寸的高性能结构构型。

![[Guo2026_Bezier_Fig1.png]]
<center><b>
图 1：工程中的典型高度异质结构。(a) 纤维增强复合材料 [1]；(b) 具有非均匀单胞的点阵结构拓扑优化 [2, 3]；(c) 包含大量微裂纹或微孔隙的岩石 [4]。
</b></center>

采用高分辨率网格的直接后果，是导致有限元分析中的自由度（DOFs）数量以及拓扑优化中的设计变量规模呈爆炸式增长，伴随而来的是底层求解器计算成本的急剧增加。以线弹性小变形假定下的静态分析为例，在经典数值分析框架中，结构力学分析通常转化为求解一个超大规模的线性代数方程组。当采用直接求解法时，计算效率强烈依赖于系统自由度规模，并随自由度数量增加呈指数级恶化。在有限元框架下，如参考文献 [10] 所述，尽管系数矩阵（刚度矩阵）呈现出优良的稀疏性，但三维问题仍然满足以下计算复杂度估计：$T_s = \mathcal{O}(n^2)$，其中 $T_s$ 表示有限元分析的计算复杂度，$n$ 表示自由度数量。显然，当 $n$ 极大时，计算负担变得极其沉重（甚至由于内存限制，在标准个人计算机上完全无法启动计算）——这一现象通常被称为“维度灾难”。另一方面，随着计算网格的细化，全局刚度矩阵 $\mathbf{K}$ 的条件数 $\mathrm{Cond}(\mathbf{K})$ 也会急剧恶化。事实上，满足 $\mathrm{Cond}(\mathbf{K}) \propto h^{-2m}$，其中 $h$ 是离散有限元的特征尺寸（网格尺寸），$m$ 是控制方程偏微分算子的最高阶数。这不仅对迭代求解器的收敛性构成了严峻挑战，而且损害了数值结果的可靠性，该现象被称为“网格细化困境”（Refinement Dilemma）。

为应对上述挑战，研究人员在经典数值分析框架内开展了大量富有成效的工作。发展了包括降阶方法 [11–16]、均质化方法 [17–20] 和多尺度 $\text{FE}^2$ 方法 [21–24] 在内的多种技术，以减轻高度异质结构有限元分析的计算负担。尽管取得了这些进展，但仍存在若干瓶颈：加速效果往往依赖于严格的先验建模假设，且可达到的加速比最终受制于现有的计算资源。因此，在计算复杂度的先验约束下，传统数值分析框架内进一步提升高度异质结构 FEA 效率的空间已趋近饱和，迫切需要探索新的研究方向。

近年来，人工智能（AI）和数据科学的迅猛发展推动了计算力学和拓扑优化的变革。通过将 AI 和数据驱动技术与经典算法相结合，力学界开始攻关长期存在的难题，取得了一系列引人瞩目的进展 [25–31]。例如，Tang 等人结合卷积神经网络（CNN）与位移场的张量分解表示，提出了一套高效计算方法 [32, 33]。程耿东与聂玉峰发展了有限元聚类分析技术，将异质结构分析的经典代表性体积单元（RVE）方法与数据科学中的聚类算法相结合，建立了统一的降阶框架，并将其推广到各类复合材料非线性特性的高效预测中 [34–36]。与此同时，物理信息神经网络（PINN）获得了广泛关注；通过将控制方程和边界条件作为软约束嵌入损失函数，基于 PINN 的模型可显著增强力学现象的建模与预测 [37–39]。

相比于单次结构响应分析，大规模问题下的拓扑优化计算负担尤为繁重，因其采用迭代更新机制，需要反复求解伴随灵敏度分析引起的超大规模线性方程组。因此，拓扑优化成为了检验新型高效数值方法的绝佳试验场。利用机器学习加速拓扑优化的研究大体可分为两类：
1. **端到端（End-to-End）直接预测优化结果**：直接利用神经网络从载荷和边界条件预测最终结构构型 [40–44]。此类方法避开了昂贵的有限元迭代求解，实现了令人瞩目的加速比。然而，由于神经网络通常只在特定设计域、边界条件和网格拓扑下训练，其泛化能力往往受限。一旦遭遇未见过的几何外形或载荷工况，预测精度往往大幅下降，且缺乏显式的力学机制保障。
2. **物理/数值计算流程中的代理替代**：将机器学习模块作为传统拓扑优化管线中的加速组件，例如作为有限元求解器、重均质化或投影算子的代理模型 [45–48]。

在这一背景下，黄敏等提出并发展了**问题无关机器学习**（Problem-Independent Machine Learning, PIML）框架 [49, 50]。PIML 的核心构想是将大规模连续介质设计域划分为大量局部子结构（Substructures）。神经网络不直接面对宏观问题整体，而是专门学习局部子结构中“材料拓扑分布 $\to$ 多尺度数值形函数/局部缩聚刚度”之间的映射。由于该映射仅取决于子结构内部的材料分布与局部线弹性力学机制，与全局边界条件、外载荷及宏观结构拓扑完全解耦，因而具备极强的泛化能力（跨 BVP 零样本迁移复用）。

然而，现有的 PIML 子结构方法通常引入了**边界位移线性假定**（Linear Boundary Displacement Assumption），即强行假设相邻子结构界面的位移沿边界线呈线性分布。尽管这一假定能够极大地压缩参与全局组装的界面自由度（二维仅保留 4 个角节点，三维仅保留 8 个顶点），但在面对复杂的内部材料拓扑或局部高应力梯度（如集中外力、复杂孔洞边界）时，线性位移假定引入了过大的人工刚度约束（锁死效应），导致：
- 分析精度显著下降，难以反映高阶变形模式；
- 在拓扑优化中产生严重的人工棋盘格或网格依赖性；
- 迫使优化算法采用过大的空间滤波半径 $R_{\min}$，从而扼杀了小尺度精细构件和分支拓扑的生成能力。

为彻底打破线性边界位移假设的桎梏，本文提出了一种**基于三次 Bézier 曲线/曲面插值子结构边界位移的高泛化 AI 增强力学分析与拓扑优化方法**。主要贡献与特色如下：
1. **引入高阶 Bézier 边界插值体系**：通过在子结构边界面上引入少量高阶控制点（Control Points），利用三次 Bézier 曲线（二维）与双三次 Bézier 曲面（三维）参数化边界位移场，在保持 $C^0$ 界面协调性的同时，使子结构边界能够自适应捕获复杂的非线性位移曲率；
2. **严格的数学不变性保持**：从理论上证明了 Bézier 边界插值诱导的高阶多尺度数值形函数在刚体平移与刚体转动下的数学不变性，确保了凝聚刚度矩阵零空间维数与物理刚体模态的严格一致；
3. **基于 DeepONet 的高精度算子学习**：借助深度算子网络（DeepONet）的连续坐标表达能力，构建从子结构内部材料场（Branch 网络）到位移响应场（Trunk 网络）的映射模型，并显式引入力学对称性与能量一致性硬约束；
4. **支持小滤波半径的大规模超高分辨率优化**：摆脱了人工数值锁死，在三维悬臂梁、MBB 梁、桥式结构及包含 1038 万细单元的飞翼复杂结构中，将滤波半径缩小至 1.5 倍细网格尺寸，成功获得了丰富且清晰的仿生骨架与内部传力分支，并在十亿级自由度并行算例中验证了拓展潜力。

---

# 2 基于三次 Bézier 插值边界位移的子结构方法

在子结构方法中，大规模结构被划分为多个子结构，并且仅在指定的边界节点子集（控制点）上计算力学响应。通过以此方式约束求解空间，参与有限元分析（FEA）的自由度（DOFs）数量被大幅压缩，带来计算效率的显著提升。由于该自由度缩减操作在全局组装之前、施加宏观边界条件之前在局部独立完成，因此该过程实际上扮演了一个依赖于局部边界条件与几何形态的降阶加速器。关于子结构经典方法的实现可参考 [51]。

![[Guo2026_Bezier_Fig2.png]]
<center><b>
图 2：(a) 将设计域分解为若干子结构；(b) 子结构 $\Omega^j$ 的节点位移划分为内部节点位移 $\mathbf{u}_i^j$ 与边界节点位移 $\mathbf{u}_b^j$；(c) 由控制点位移插值获得子结构 $\Omega^j$ 的边界变形。
</b></center>

## 2.1 经典子结构方法及其性质

子结构方法最初是作为静力缩聚（Static Condensation / Guyan Reduction）技术发展起来的，用于减少刚度矩阵和质量矩阵中的自由度数。其核心思想是仅求解各子结构的边界自由度，而内部自由度随后通过数值形函数（即从边界节点位移到内部节点位移的计算线性映射）恢复。在线弹性小变形设定下，这种降阶过程在数学上是**精确**的：由于内部自由度是通过 Schur 补变换被完全消元的，且可以从保留的边界自由度精确重构，因此不会引入任何截断误差。

下面在线弹性小变形有限元框架下推导子结构方法。在区域分解有限元设定中，如图 2(a) 所示，每个子结构 $\Omega^j$（$j = 1, \dots, N$，每个 $\Omega^j$ 包含大量细观单元）的准静态平衡方程可独立写为：
$$
\mathbf{K}^j \mathbf{u}^j = \mathbf{f}^j, \tag{1}
$$
其中 $\mathbf{K}^j$ 表示第 $j$ 个子结构的刚度矩阵，$\mathbf{u}^j$ 和 $\mathbf{f}^j$ 分别为其节点位移向量和节点载荷向量。如图 2(b) 所示，将每个子结构的节点划分为内部节点集与边界节点集，分别用下标 $\text{i}$ 与 $\text{b}$ 表示。则式 (1) 可分块重排为：
$$
\begin{bmatrix}
\mathbf{K}_{bb}^j & (\mathbf{K}_{ib}^j)^\top \\
\mathbf{K}_{ib}^j & \mathbf{K}_{ii}^j
\end{bmatrix}
\begin{bmatrix}
\mathbf{u}_b^j \\
\mathbf{u}_i^j
\end{bmatrix}
=
\begin{bmatrix}
\mathbf{f}_b^j \\
\mathbf{f}_i^j
\end{bmatrix}. \tag{2}
$$
不失一般性，假设子结构内部节点上没有外载荷作用，即 $\mathbf{f}_i^j = \mathbf{0}$（存在体力或内部载荷时的广义推广见附录 A）。将其代入式 (2) 的第二行，可得内部位移与边界位移的显式消元关系：
$$
\mathbf{u}_i^j = - (\mathbf{K}_{ii}^j)^{-1} \mathbf{K}_{ib}^j \mathbf{u}_b^j. \tag{3}
$$
进一步将式 (3) 代入式 (2) 的第一行，得到关于边界位移 $\mathbf{u}_b^j$ 的缩聚（Schur 补）刚度矩阵：
$$
\mathbf{K}_s^j = \mathbf{K}_{bb}^j - (\mathbf{K}_{ib}^j)^\top (\mathbf{K}_{ii}^j)^{-1} \mathbf{K}_{ib}^j. \tag{4}
$$
将所有子结构的缩聚刚度矩阵组装，即可得到全局缩聚刚度矩阵 $\mathbf{K}_s = \sum_{j=1}^N (\mathbf{G}^j)^\top \mathbf{K}_s^j \mathbf{G}^j$，其中 $\mathbf{G}^j$ 为第 $j$ 个子结构的布尔组装拓扑矩阵。由此，边界位移向量通过求解如下降阶线性方程组确定：
$$
\mathbf{K}_s \mathbf{u}_b = \mathbf{f}_b, \tag{5}
$$
其中 $\mathbf{f}_b$ 为作用于所有边界自由度上的全局等效载荷向量。一旦求解式 (5) 获得全局边界位移 $\mathbf{u}_b$，各子结构的内部位移即可由式 (3) 在局部并行恢复。这种一次性策略显著降低了线性代数系统的规模，极大提升了大规模问题的求解效率。

借用位移插值的概念，式 (3) 可重写为一个线性转换形式：
$$
\mathbf{u}_i^j = \mathbf{N}_s^j \mathbf{u}_b^j, \tag{6}
$$
其中 $\mathbf{N}_s^j \in \mathbb{R}^{n_i \times n_b}$ 为将边界节点位移映射到子结构 $j$ 内部节点位移的多尺度数值形函数矩阵（此处 $n_i$ 和 $n_b$ 分别表示内部和边界自由度数）。比较式 (3) 与式 (6) 可知：
$$
\mathbf{N}_s^j = - (\mathbf{K}_{ii}^j)^{-1} \mathbf{K}_{ib}^j.
$$
相应地，子结构 $j$ 的全域节点位移向量可表示为：
$$
\mathbf{u}^j = \begin{bmatrix} \mathbf{u}_b^j \\ \mathbf{u}_i^j \end{bmatrix} = \begin{bmatrix} \mathbf{I}_{n_b} \\ \mathbf{N}_s^j \end{bmatrix} \mathbf{u}_b^j \triangleq \mathbf{N}^j \mathbf{u}_b^j,
$$
其中 $\mathbf{I}_{n_b} \in \mathbb{R}^{n_b \times n_b}$ 为单位矩阵，$\mathbf{N}^j$ 为边界到位移全场的变形映射矩阵。由此，子结构 $j$ 的缩聚刚度矩阵亦可通过数值形函数表达为能量一致形式：
$$
\mathbf{K}_s^j = (\mathbf{N}^j)^\top \mathbf{K}^j \mathbf{N}^j. \tag{7}
$$

## 2.2 通过子结构界面边界位移插值进一步降低计算复杂度

必须强调，2.1 节介绍的自由度缩聚属于精确模型降阶：其解与在原始细网格上直接求解完全一致。其计算增益来自于将各子结构的内部自由度转移至边界，从而减小了最耗时的全局线性求解规模。

从理论上看，子结构尺寸越大，缩聚掉的内部自由度越多，加速比理应更高。然而，采用直接稀疏求解器时，全局线性系统的计算复杂度一般按 $\mathcal{O}(N \beta^2)$ 缩放，其中 $N$ 为自由度总数，$\beta$ 为全局刚度矩阵的半带宽（Bandwidth）。如图 3 所示：
- 采用精确缩聚（保留全部边界节点）虽然减少了 $N$，但在全局刚度矩阵中产生了密集的非零块（Dense Blocks），导致带宽 $\beta$ 显著增大（图 3(a) 与 3(b) 的对比）。
- 带宽 $\beta$ 的剧增在数学复杂度上会抵消 $N$ 减小带来的优势。实验表明，当保留所有边界节点时，对于大约 $20 \times 20 \times 20$ 或更大的三维子结构，稀疏性恶化导致的额外开销将超过自由度降低带来的收益。

![[Guo2026_Bezier_Fig3.png]]
<center><b>
图 3：不同边界插值方法下全局刚度矩阵（线性代数方程组系数矩阵）中非零元素的分布特征。(a) 边界仅保留两个角节点（线性假设下）；(b) 边界保留四个控制节点（三次曲线插值下）。
</b></center>

因此，边界位移插值方案作为一种在数学上经过优化的策略应运而生。通过引入少量的**边界控制点**（Control Points），使得保留的自由度数量远少于全部边界节点方案（大幅压降 $N$），同时相比全缩聚方案极大地抑制了全局刚度矩阵非零元素的填入（严格控制了 $\beta$ 的增长）。该方法在保持矩阵稀疏性、压低自由度与计算精度之间取得了最优的平衡。

假设子结构 $j$ 的全部边界节点位移由一组指定的边界控制点位移插值得到：
$$
\mathbf{u}_b^j = \mathbf{S}^j \mathbf{u}_r^j,
$$
其中 $\mathbf{u}_r^j$ 汇集了子结构 $j$ 的边界控制点（插值点）位移向量，$\mathbf{S}^j \in \mathbb{R}^{n_b \times n_r}$ 为相应的边界插值矩阵（$n_r$ 为 $\mathbf{u}_r^j$ 对应的自由度总数）。此时，子结构 $j$ 对应的缩聚刚度矩阵可表示为：
$$
\mathbf{K}_s^j = (\mathbf{N}^j \mathbf{S}^j)^\top \mathbf{K}^j (\mathbf{N}^j \mathbf{S}^j) \triangleq (\widetilde{\mathbf{N}}^j)^\top \mathbf{K}^j \widetilde{\mathbf{N}}^j, \tag{8}
$$
其中 $\widetilde{\mathbf{N}}^j = \mathbf{N}^j \mathbf{S}^j$ 表示与边界控制点自由度相联系的“控制点到全场变形映射矩阵”。在实际应用中，式 (8) 中的 $\mathbf{S}^j$ 可以选取为任意边界位移插值矩阵。不同的 $\mathbf{S}^j$ 选择直接定义了边界位移的近似函数空间，从而主导了有限元分析的整体精度。

本文的核心创新点在于：仅求解关键边界控制节点处的位移，并利用**三次 Bézier 曲线/曲面**插值恢复出完整的边界节点位移场。相比于线性插值，三次 Bézier 插值在二维下每条边仅增加 2 个内部控制点，却提供了强大的非线性变形拟合能力（见图 4）。

![[Guo2026_Bezier_Fig4.png]]
<center><b>
图 4：对于相同的真实位移变形，两种不同插值模式给出的位移拟合形态。(a) 采用包含 4 个控制点的高阶曲线插值；(b) 采用仅含 2 个控制点的线性插值。
</b></center>

只要插值矩阵 $\mathbf{S}$ 具有解析解析式、Kronecker 积结构和仿射不变性（见 2.4 节），就能够进行高度向量化的并行组装，并与本文的深度学习代理模型无缝集成。利用由式 (8) 组装得到的缩聚刚度矩阵 $\mathbf{K}_s$，通过求解降阶代数方程组：
$$
\mathbf{K}_s \mathbf{u}_r = \mathbf{f}_r,
$$
即可得到控制点的位移，其中 $\mathbf{f}_r$ 为保证系统总势能守恒的全局控制点等效载荷向量（双重载荷下的严格推导见附录 A）。

## 2.3 采用三次 Bézier 曲线的子结构边界位移插值

图 5 给出了三次 Bézier 曲线子结构方法的离散示意图。粗尺度子结构的边界节点被划分为两类：落在控制点处的节点（记为 $\beta_p$）与非控制节点的其余边界节点（记为 $\beta_c$）。内部节点集记为 $\beta_i$。

![[Guo2026_Bezier_Fig5.png]]
<center><b>
图 5：基于 Bézier 曲线插值的子结构方法示意图。角隅节点用粉色圆圈表示，边界控制节点用橙色圆圈表示；非控制边界节点用黑色圆圈表示；内部节点用紫色圆圈表示。
</b></center>

在二维情况下，参数化变量 $t \in [0, 1]$ 沿子结构边界边的三次 Bézier 曲线定义为：
$$
\mathbf{B}(t) = \sum_{s=0}^3 b_s(t) \mathbf{P}_s, \quad 0 \le t \le 1, \tag{9}
$$
其中 Bernstein 基底多项式 $b_s(t)$ 为：
$$
b_s(t) = \binom{3}{s} (1 - t)^{3-s} t^s, \quad s = 0, 1, 2, 3. \tag{10}
$$
这里 $\mathbf{P}_s \in \mathbb{R}^2$ 为控制点坐标，$\binom{3}{s}$ 为二项式系数。显然有 $\mathbf{B}(0) = \mathbf{P}_0$ 和 $\mathbf{B}(1) = \mathbf{P}_3$，曲线精确插值其两个端点。

![[Guo2026_Bezier_Fig6.png]]
<center><b>
图 6：集中载荷作用下采用两种不同边界插值子结构分析得到的变形图。(a) 采用边界位移 Bézier 曲线假定；(b) 采用边界位移线性假定。
</b></center>

将各边界线段重新参数化映射为 $t \in [0, 1]$。设第 $i$ 条边界段上 4 个控制节点的位移向量为 $\mathbf{u}_{p-\text{edge}}^i = [(\mathbf{u}_1^p)^\top, \dots, (\mathbf{u}_4^p)^\top]^\top \in \mathbb{R}^8$。则该段上第 $l$ 个边界节点的位移 $\mathbf{u}_{lb}^i$ 由三次 Bézier 曲线插值给出：
$$
\mathbf{u}_{lb}^i = \mathbf{S}_i(t(\mathbf{x}_{lb}^i)) \mathbf{u}_{p-\text{edge}}^i, \quad l = 1, 2, \dots, n_{ib}, \tag{11}
$$
其中插值矩阵显式定义为：
$$
\mathbf{S}_i(t) = \begin{bmatrix} 1 & t & t^2 & t^3 \end{bmatrix}
\begin{bmatrix}
1 & 0 & 0 & 0 \\
-3 & 3 & 0 & 0 \\
3 & -6 & 3 & 0 \\
-1 & 3 & -3 & 1
\end{bmatrix} \otimes \mathbf{I}_2, \quad 0 \le t \le 1. \tag{12}
$$
此处 $n_{ib}$ 为第 $i$ 段上的边界节点数，$\mathbf{x}_{lb}^i$ 为对应物理坐标，$\otimes$ 表示 Kronecker 积，$\mathbf{I}_2$ 为 $2 \times 2$ 单位矩阵。通过在各段边界上进行标准 Scatter-Add 组装，子结构第 $m$ 个边界节点的插值矩阵为：
$$
\widehat{\mathbf{S}}(\mathbf{x}_{mb}) = \sum_{i=1}^4 \mathbf{S}_i(\mathbf{x}_{mb}), \quad m = 1, 2, \dots, N_b. \tag{13}
$$
将所有边界节点的行块堆叠，即获得子结构层级的整体 Bézier 插值矩阵 $\mathbf{S}^j$：
$$
\mathbf{S}^j = \begin{bmatrix} \widehat{\mathbf{S}}(\mathbf{x}_{1b}); & \dots; & \widehat{\mathbf{S}}(\mathbf{x}_{mb}); & \dots; & \widehat{\mathbf{S}}(\mathbf{x}_{N_bb}) \end{bmatrix}. \tag{14}
$$

对于三维六面体子结构，边界退化为面，插值形式自然升阶为**双三次 Bézier 曲面**（Bicubic Bézier Surfaces）。设 $\mathbf{t} = (t_{x1}, t_{x2}) \in [0, 1]^2$ 为沿边界平面两个相互正交方向的面内参数坐标。双三次 Bézier 曲面表示为：
$$
\mathbf{B}(\mathbf{t}) = \sum_{s=0}^3 \sum_{h=0}^3 b_s(t_{x1}) b_h(t_{x2}) \mathbf{P}_{sh}, \tag{15}
$$
每个六面体面具有 16 个控制点 $\mathbf{P}_{sh} \in \mathbb{R}^3$。设第 $i$ 个面上 16 个控制节点的位移集成为 $\mathbf{u}_{p-\text{face}}^i \in \mathbb{R}^{48}$。则面上第 $l$ 个边界节点的位移插值为：
$$
\mathbf{u}_{lb}^i = \mathbf{S}_{x1}(t_{x1}(\mathbf{x}_{lb}^i)) \mathbf{S}_{x2}(t_{x2}(\mathbf{x}_{lb}^i)) \mathbf{u}_{p-\text{face}}^i, \tag{16}
$$
其中：
$$
\mathbf{S}_{x1} = \mathbf{S}_0(t_{x1}) \otimes \mathbf{I}_3, \quad \mathbf{S}_{x2} = \mathbf{S}_0(t_{x2}) \otimes \mathbf{I}_{12}, \tag{17}
$$
$$
\mathbf{S}_0(t) = \begin{bmatrix} 1 & t & t^2 & t^3 \end{bmatrix}
\begin{bmatrix}
1 & 0 & 0 & 0 \\
-3 & 3 & 0 & 0 \\
3 & -6 & 3 & 0 \\
-1 & 3 & -3 & 1
\end{bmatrix}. \tag{18}
$$
此处 $\mathbf{I}_3 \in \mathbb{R}^{3 \times 3}$，$\mathbf{I}_{12} \in \mathbb{R}^{12 \times 12}$。乘积 $\mathbf{S}_{x1} \mathbf{S}_{x2} \in \mathbb{R}^{3 \times 48}$，与位移维度精确匹配。最终通过类似方式对 6 个面进行散布累加组装：
$$
\widehat{\mathbf{S}}(\mathbf{x}_{mb}) = \sum_{i=1}^6 \mathbf{S}_{x1}(t_{x1}(\mathbf{x}_{mb}^i)) \mathbf{S}_{x2}(t_{x2}(\mathbf{x}_{mb}^i)), \tag{19}
$$
$$
\mathbf{S}^j = \begin{bmatrix} \widehat{\mathbf{S}}(\mathbf{x}_{1b}); & \dots; & \widehat{\mathbf{S}}(\mathbf{x}_{mb}); & \dots; & \widehat{\mathbf{S}}(\mathbf{x}_{N_bb}) \end{bmatrix}.
$$
对于标准六面体子结构，每个子结构共具有 56 个独立控制点（8 个角隅顶点、24 个边内控制点、24 个面内控制点），自由度总数仅为 $56 \times 3 = 168$。插值矩阵满足 $\mathbf{S}^j \in \mathbb{R}^{3N_b \times 168}$。

## 2.4 Bézier 插值数值形函数的数学不变性证明

将三次 Bézier 插值引入子结构后，第 $j$ 个子结构映射内部自由度到控制点自由度的高阶多尺度数值形函数矩阵为：
$$
\widetilde{\mathbf{N}}_s^j = \mathbf{N}_s^j \mathbf{S}^j. \tag{20}
$$
由此，子结构内部单元节点的位移向量可表示为：
$$
\mathbf{u}_i^j = \widetilde{\mathbf{N}}_s^j \mathbf{u}_r^j = \mathbf{N}_s^j \mathbf{S}^j \mathbf{u}_r^j. \tag{21}
$$
矩阵 $\widetilde{\mathbf{N}}_s^j$ 必须满足标准有限元形函数的基本要求以避免出现非物理性态 [52–54]。在任意刚体运动下，无论子结构内部材料分布如何，内部位移 $\mathbf{u}_i^j$ 必须与控制点位移 $\mathbf{u}_r^j$ 保持不变的关系。由于刚体运动可严格分解为平移与转动，因此只需分别验证 $\widetilde{\mathbf{N}}_s^j$ 的平移与旋转不变性。

为了表述清晰，记 $\mathbf{1}_m \in \mathbb{R}^{m \times 1}$ 为全 1 向量，$\mathbf{I}_m \in \mathbb{R}^{m \times m}$ 为单位矩阵。

### 平移不变性证明

在刚体平移下，结构中所有点的位移必须完全相同。不失一般性，设所有边界控制点在各坐标方向上的位移均为单位量，即 $\mathbf{u}_r^j = \mathbf{1}_{n_r} \in \mathbb{R}^{n_r \times 1}$。由 Bernstein 基底的单位分解性（Partition of Unity）：
$$
\sum_{s=0}^3 b_s(t) = 1, \tag{22}
$$
可得边界上任意插值点的位移严格为 1，即：
$$
\mathbf{S}^j \mathbf{u}_r^j = \mathbf{u}_b^j = \mathbf{1}_{n_b} \in \mathbb{R}^{n_b \times 1}.
$$
根据式 (21)，内部位移为：
$$
\mathbf{u}_i^j = \mathbf{N}_s^j \mathbf{S}^j \mathbf{1}_{n_r} = \mathbf{N}_s^j \mathbf{1}_{n_b}. \tag{23}
$$
由于经典子结构内部映射 $\mathbf{N}_s^j$ 自身是精确且满足平移不变性的 [50]，恒有 $\mathbf{N}_s^j \mathbf{1}_{n_b} = \mathbf{1}_{n_i}$。代入式 (23) 即得：
$$
\widetilde{\mathbf{N}}_s^j \mathbf{1}_{n_r} = \mathbf{u}_i^j = \mathbf{1}_{n_i}, \tag{24}
$$
证毕，高阶数值形函数矩阵 $\widetilde{\mathbf{N}}_s^j$ 严格满足**平移不变性**。

### 旋转不变性证明

在二维情况下，考虑刚体转动角度 $\boldsymbol{\theta} \in \mathbb{R}^{2 \times 1}$，对应正交旋转矩阵为 $\boldsymbol{\omega} \in \mathbb{R}^{2 \times 2}$。内部节点位移向量必须满足：
$$
\mathbf{u}_i^j = (\mathbf{I}_{n_i} \otimes \boldsymbol{\omega}) \mathbf{x}_i = \widetilde{\mathbf{N}}_s^j \mathbf{u}_r^j = \mathbf{N}_s^j \mathbf{S}^j \mathbf{u}_r^j, \tag{25}
$$
其中 $\mathbf{u}_r^j = (\mathbf{I}_{n_r} \otimes \boldsymbol{\omega}) \mathbf{X}_r$ 为控制点在刚体旋转下的位移，$\mathbf{x}_i$ 和 $\mathbf{X}_r$ 分别为内部节点与控制点的初始空间坐标。由 Bézier 曲线的**仿射不变性**（Affine Invariance / Linearity）：
$$
\boldsymbol{\omega} \mathbf{B}(t) = \boldsymbol{\omega} \sum_{s=0}^3 b_s(t) \mathbf{P}_s = \sum_{s=0}^3 b_s(t) (\boldsymbol{\omega} \mathbf{P}_s). \tag{26}
$$
结合式 (9)–(14) 与式 (26)，可得边界节点位移精确满足：
$$
\mathbf{u}_b^j = (\mathbf{I}_{n_b} \otimes \boldsymbol{\omega}) \mathbf{x}_b = \mathbf{S}^j (\mathbf{I}_{n_r} \otimes \boldsymbol{\omega}) \mathbf{X}_r = \mathbf{S}^j \mathbf{u}_r^j. \tag{27}
$$
将式 (27) 代入式 (25)，由于经典子结构内部映射已严格保持旋转不变性，即 $\mathbf{N}_s^j \mathbf{u}_b^j = \mathbf{u}_i^j$，故恒有：
$$
\widetilde{\mathbf{N}}_s^j \mathbf{u}_r^j = \mathbf{N}_s^j (\mathbf{S}^j \mathbf{u}_r^j) = \mathbf{N}_s^j \mathbf{u}_b^j = \mathbf{u}_i^j. \tag{28}
$$
证毕，$\widetilde{\mathbf{N}}_s^j$ 严格满足**旋转不变性**。

**力学意义**：平移与旋转不变性直接决定了凝聚刚度矩阵 $\mathbf{K}_s$ 的零空间维数（Nullity）。在二维中，$\mathbf{K}_s$ 必须精确包含 3 个刚体模态（2 个平移、1 个转动）；在三维中必须精确包含 6 个刚体模态（3 个平移、3 个转动）。利用该结构特性，可以在神经网络训练中显式剥离这些先验已知模态，大幅降低网络学习负担。

---

# 3 基于深度算子网络（DeepONet）的问题无关机器学习框架

![[Guo2026_Bezier_Fig7.png]]
<center><b>
图 7：基于深度算子网络（DeepONet）的机器学习框架总体架构。
</b></center>

## 3.1 基于 DeepONet 的模型架构与训练

受普遍算子逼近定理启发的深度算子网络（DeepONet）由两部分组成：用于编码输入函数（材料分布）的 **Branch 网络**，以及用于编码连续评估坐标（离散空间点）的 **Trunk 网络**。

设子结构内离散杨氏模量场为 $\boldsymbol{\rho}^j = [\rho_1^j, \dots, \rho_{m^3}^j]^\top \in [0, 1]^{m^3}$。Branch 网络接受 $\boldsymbol{\rho}^j$ 作为输入，输出特征向量 $\mathbf{b}(\boldsymbol{\rho}^j) \in \mathbb{R}^p$；Trunk 网络接受评估点的空间局部坐标 $\mathbf{x} \in \mathbb{R}^3$ 作为输入，输出特征向量 $\mathbf{t}(\mathbf{x}) \in \mathbb{R}^p$。DeepONet 对高阶数值形函数分量的预测通过内积形式给出：
$$
\widetilde{N}_{kl}^j(\mathbf{x}) \approx \sum_{q=1}^p b_q^l(\boldsymbol{\rho}^j) t_q^k(\mathbf{x}) + c_0^{kl}, \tag{29}
$$
其中 $c_0^{kl}$ 为可学习偏置项。对于三维 $5 \times 5 \times 5$ 子结构，Trunk 网络输入为内部各粗网格节点的局部坐标；Branch 网络采用含 4 层密集残差连接的 MLP 架构，隐藏层维度为 256~512，激活函数采用 GELU。

## 3.2 训练过程中施加物理约束

利用 2.4 节证明的数学不变性，可将刚体模态作为硬约束施加。设刚体位移基向量矩阵为 $\boldsymbol{\Phi} = [\boldsymbol{\phi}_1, \dots, \boldsymbol{\phi}_M]$（二维 $M=3$，三维 $M=6$），其中每列代表一个刚体模态。根据式 (24) 和 (28)，数值形函数必须精确满足：
$$
\widetilde{\mathbf{N}}_s^j \boldsymbol{\Phi}_r = \boldsymbol{\Phi}_i \triangleq \mathbf{b}, \tag{30}
$$
其中 $\boldsymbol{\Phi}_r \in \mathbb{R}^{n_r \times M}$ 与 $\boldsymbol{\Phi}_i \in \mathbb{R}^{n_i \times M}$ 分别为控制点与内部节点的刚体模态矩阵。在实际实现中，将形函数矩阵按列分割为网络预测部分 $\widetilde{\mathbf{N}}_{\text{out}}^j$ 与由物理约束显式确定的补全部分 $\widetilde{\mathbf{N}}_{\text{cal}}^j$：
$$
\begin{bmatrix} \widetilde{\mathbf{N}}_{\text{out}}^j & \widetilde{\mathbf{N}}_{\text{cal}}^j \end{bmatrix} \begin{bmatrix} \boldsymbol{\Phi}_1 \\ \boldsymbol{\Phi}_2 \end{bmatrix} = \mathbf{b}, \tag{31}
$$
神经网络仅需预测 $\widetilde{\mathbf{N}}_{\text{out}}^j$（输出自由度由 56 降至 50），而 $\widetilde{\mathbf{N}}_{\text{cal}}^j$ 通过直接求解代数系统式 (31) 确定：
$$
\widetilde{\mathbf{N}}_{\text{cal}}^j = (\mathbf{b} - \widetilde{\mathbf{N}}_{\text{out}}^j \boldsymbol{\Phi}_1) \boldsymbol{\Phi}_2^{-1}. \tag{32}
$$
这在构造上**无条件保证了刚体平移与转动不变性**，消除了非物理的伪刚体位移误差，并显著降低了训练难度。

## 3.3 样本生成与收敛性分析

在 PIML 框架下，样本生成完全摆脱了对宏观有限元迭代循环的依赖。由于 $\widetilde{\mathbf{N}}_s^j$ 仅由子结构内部材料分布决定，训练样本可直接在离散单元上通过随机场生成。采用 Simplex 连续噪声在 $[0, 1]$ 之间抽样，以模拟拓扑优化演化中产生的各类连续与离散材料拓扑。

![[Guo2026_Bezier_Fig8.png]]
<center><b>
图 8：DeepONet 模型随训练数据集规模的收敛性分析。(a) 测试集误差 ($\log_{10} \text{MSE}$) 随样本量演化，在 $10^5$ 样本后趋于平缓；(b) 训练效率（单位训练时间的精度增益）随样本量急剧下降，表明 $10^5$ 为计算与精度的最优平衡点。
</b></center>

如图 8 所示，针对 $5 \times 5 \times 5$ 子结构进行了数据集规模收敛性分析（样本量从 $1 \times 10^4$ 到 $5 \times 10^5$）。结果表明，测试均方误差在样本量达到 $10^5$ 时已降至 $1.846 \times 10^{-5}$，继续增加样本带来的边际精度收益迅速递减，因此选择 $10^5$ 作为标准训练规模。

![[Guo2026_Bezier_Fig9.png]]
<center><b>
图 9：DeepONet 框架的训练与验证损失曲线。(a) 训练损失（蓝色实线）与验证损失（橙色虚线）随迭代步数演化；(b) 局部放大图显示 20,000 步后训练与验证损失同步平稳下降，未出现过拟合。
</b></center>

**注记 1 (注记与多尺度算法拓展)**：一旦通过机器学习模型获得高阶数值形函数矩阵 $\widetilde{\mathbf{N}}_s^j$，即可得到子结构的缩聚刚度矩阵 $\mathbf{K}_{\text{ML}}^j$。该策略不仅适用于子结构法，亦可无缝迁移至多重网格方法（Multigrid）中的投影算子学习，以及多尺度有限元（MsFEM）中的多尺度基函数预测。

**注记 2 (格林函数逆算子视角)**：从力学本质来看，$\mathbf{K}_{\text{ML}}^j$ 的第 $(m, n)$ 个元素表示边界第 $n$ 个自由度发生单位位移时在第 $m$ 个自由度上产生的反力。这与弹性力学控制方程的格林函数（Green's function）张量 $\mathbf{G}_{mn}(\mathbf{x}, \mathbf{x}')$ 的逆算子直接相通，为严谨的数学泛化误差分析提供了理论基石。

**注记 3 (输入输出分辨率独立性)**：尽管当前 Branch 网络针对规则体素网格采用了固定维度的 MLP，但由于 Trunk 网络具有连续坐标编码特性，本模型在**输出解空间**上实现了完全的分辨率无关性，克服了细网格节点形函数输出的维度灾难。

---

# 4 数值实现

为了全面评估所提出的基于三次 Bézier 边界插值的 PIML 方法，本节开展系统的力学分析与拓扑优化算例测试。有限元分析由训练完毕的 DeepONet 代理驱动。对于 SIMP 框架，采用准则法（Optimality Criteria, OC）更新设计变量；对于隐式拓扑描述函数（ITDF）框架 [61]，采用移动渐近线法（Method of Moving Asymptotes, MMA）。收敛准则设定为连续 5 步目标函数相对变化小于 $2 \times 10^{-4}$。除特殊声明外，所有算例均在配备 Intel Core i9-13900K CPU 与 128 GB RAM 的工作站上运行。

## 4.1 力学分析算例

### 算例 1：均布载荷悬臂梁

设计域为 $4 \times 1 \times 1$ 的三维悬臂梁，左端完全固支，顶面承受竖直向下的均布载荷，如图 10 所示。网格划分为 $240 \times 60 \times 60$（共 864,000 个细观单元，约 268 万自由度）。分别测试了 $5 \times 5 \times 5$ 与 $10 \times 10 \times 10$ 两种子结构划分模式。

![[Guo2026_Bezier_Fig10.png]]
<center><b>
图 10：均布载荷下的悬臂梁力学分析问题设置。
</b></center>

![[Guo2026_Bezier_Fig11.png]]
<center><b>
图 11：均布载荷下悬臂梁算例的时间–精度 Pareto 前沿对比曲线。
</b></center>

**表 1** 均布载荷悬臂梁算例的时间–精度 Pareto 前沿数据对比

| 子结构尺寸 | 边界插值方案 | 单个子结构控制点数 | 分析耗时 (s) | 相对位移误差 | 加速比 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **$5 \times 5 \times 5$** | 直接有限元 (基准) | – | 307.15 | – | $1.0\times$ |
| | 线性插值 (Linear) | 8 | 0.87 | 7.76% | $\sim 352\times$ |
| | 二次插值 (Quadratic) | 26 | 1.94 | 2.37% | $\sim 158\times$ |
| | **三次 Bézier 插值 (本文)** | **56** | **5.64** | **1.95%** | **$\sim 54\times$** |
| | 全边界节点精确预测 | 152 | 40.76 | 0.84% | $\sim 7.5\times$ |
| **$10 \times 10 \times 10$** | 直接有限元 (基准) | – | 307.15 | – | $1.0\times$ |
| | 线性插值 (Linear) | 8 | 0.81 | 13.64% | $\sim 379\times$ |
| | 二次插值 (Quadratic) | 26 | 1.56 | 5.23% | $\sim 196\times$ |
| | **三次 Bézier 插值 (本文)** | **56** | **2.87** | **2.22%** | **$\sim 106\times$** |
| | 全边界节点精确预测 | 602 | 42.14 | 3.46%* | $\sim 7.3\times$ |

*注：全边界预测在 $10 \times 10 \times 10$ 下由于网络输出维度高达 602，累积预测方差导致误差反而高于控制点插值。

从表 1 可以清晰看出：在 $10 \times 10 \times 10$ 子结构下，线性插值的相对误差高达 13.64%，而三次 Bézier 插值将误差大幅压降至 **2.22%**，同时保持了 **106 倍** 的惊人加速比（分析耗时仅 2.87 秒，而基准有限元需 307 秒）。

### 算例 2：优化后的桥式结构

为检验在非随机材料分布（真实拓扑优化中间构型）下的适应性，选取图 12(a) 所示的桥式结构。在经过 40 步 SIMP 优化得到的结构（图 12(b)）上进行力学分析。

![[Guo2026_Bezier_Fig12.png]]
<center><b>
图 12：(a) 桥式梁拓扑优化问题设置；(b) 经过 40 步优化后获得的桥式梁优化中间结构。
</b></center>

![[Guo2026_Bezier_Fig13.png]]
<center><b>
图 13：桥式结构对应的时间–精度 Pareto 前沿对比。
</b></center>

**表 2** 桥式梁算例的时间–精度 Pareto 前沿数据对比

| 子结构尺寸 | 边界插值方案 | 单个子结构控制点数 | 分析耗时 (s) | 相对位移误差 | 加速比 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **$5 \times 5 \times 5$** | 直接有限元 (基准) | – | 1472.64 | – | $1.0\times$ |
| | 线性插值 (Linear) | 8 | 2.31 | 6.91% | $\sim 638\times$ |
| | 二次插值 (Quadratic) | 26 | 13.45 | 1.92% | $\sim 110\times$ |
| | **三次 Bézier 插值 (本文)** | **56** | **86.62** | **1.28%** | **$\sim 17\times$** |
| **$10 \times 10 \times 10$** | 直接有限元 (基准) | – | 1472.64 | – | $1.0\times$ |
| | 线性插值 (Linear) | 8 | 2.04 | 13.53% | $\sim 722\times$ |
| | 二次插值 (Quadratic) | 26 | 5.58 | 4.69% | $\sim 264\times$ |
| | **三次 Bézier 插值 (本文)** | **56** | **9.39** | **3.90%** | **$\sim 157\times$** |

### 算例 3：集中载荷作用下的悬臂梁

在线性边界假定下，集中载荷会导致严重的局部奇异与刚度高估。在自由端施加集中竖向力（图 14），三次 Bézier 插值高度保真地复现了局部高曲率变形，位移场相对误差仅为 2.14%，而线性插值误差高达 15.82%。

![[Guo2026_Bezier_Fig14.png]]
<center><b>
图 14：集中力作用下的悬臂梁力学分析与位移变形云图对比。
</b></center>

## 4.2 MBB 梁拓扑优化算例

设置长宽高比为 $6 \times 1 \times 1$ 的 MBB 简支梁问题（图 15）。体积分数上限为 0.3。

![[Guo2026_Bezier_Fig15.png]]
<center><b>
图 15：MBB 梁拓扑优化问题几何与边界条件设置。
</b></center>

![[Guo2026_Bezier_Fig16.png]]
<center><b>
图 16：不同有限元网格下线性插值 PIML 与 Bézier 插值 PIML 拓扑优化构型对比。
</b></center>

如图 16 所示，线性插值 PIML 倾向于产生过粗的杆件，且受网格尺度影响极大；而 Bézier 插值 PIML 在不同网格下均获得了光滑、协调的桁架拓扑。

![[Guo2026_Bezier_Fig17.png]]
<center><b>
图 17：SIMP 框架下不同滤波半径对拓扑优化构型的影响。
</b></center>

![[Guo2026_Bezier_Fig18.png]]
<center><b>
图 18：Bézier 插值 PIML 极大地缩小了允许的滤波半径。(a) $R_{\min} = 0.08$；(b) $R_{\min} = 0.06$，呈现出精细的薄壁构件特征。
</b></center>

更重要的是，图 17 与图 18 证实：高精度的 Bézier 边界插值允许优化算法采用极小的滤波半径（如 $R_{\min} = 0.06$，仅为单元尺寸的 1.5 倍），而不会激发数值不稳定或棋盘格，成功生成了具有轻质高强特征的薄壁加筋微结构。

![[Guo2026_Bezier_Fig19.png]]
<center><b>
图 19：相同滤波半径下利用 ITDF（隐式拓扑描述函数）与 SIMP 方法获得的 MBB 梁拓扑优化构型对比。
</b></center>

## 4.3 悬臂梁拓扑优化算例

采用 $4 \times 1 \times 1$ 悬臂梁（图 20），在自由端承受剪切载荷。

![[Guo2026_Bezier_Fig20.png]]
<center><b>
图 20：悬臂梁拓扑优化问题设置。
</b></center>

![[Guo2026_Bezier_Fig21.png]]
<center><b>
图 21：悬臂梁优化构型对比。(a) 线性插值 PIML [55]；(b) Bézier 插值 PIML ($R_{\min} = 5\times$)；(c) Bézier 插值 PIML ($R_{\min} = 3\times$)。
</b></center>

图 21 显示，随着滤波半径减小，Bézier 插值模型在内部自然演化出了优雅的交叉加劲肋骨，整体刚度较线性假定方案提升了 14.2%。

## 4.4 桥式结构拓扑优化算例

测试图 22 所示的大跨度桥式承重结构。

![[Guo2026_Bezier_Fig22.png]]
<center><b>
图 22：桥式梁拓扑优化问题几何与受力设置。
</b></center>

![[Guo2026_Bezier_Fig23.png]]
<center><b>
图 23：本文提出的机器学习模型在两种不同拓扑优化框架（SIMP 与 ITDF）下获得的优化设计结果。
</b></center>

在 SIMP 与 ITDF 两种截然不同的拓扑描述框架下（图 23），本文模型均稳健收敛至几乎相同的拱形传力构型，证明了方法对不同优化表征与算法引擎的通用适应性。

## 4.5 飞翼结构拓扑优化算例与十亿级自由度并行扩展

为了展现该方法在处理极端复杂工程边界、超大体量设计域中的巨大威力，对具有真实空气动力学外形的**飞翼结构**（Flying Wing Structure）进行拓扑优化。

![[Guo2026_Bezier_Fig24.png]]
<center><b>
图 24：飞翼结构拓扑优化的几何外形与载荷工况设置。设计域从 $540 \times 600 \times 140$ 单元的包围盒中体素化提取。
</b></center>

如图 24 所示，设计域包含下表面气动升力均布载荷以及一层非设计蒙皮域。整个外包络网格规模为 $540 \times 600 \times 140$，有效设计单元数达 **1038 万**（约 3200 万自由度）。优化目标为体积分数 10% 约束下的柔度最小化。

![[Guo2026_Bezier_Fig25.png]]
<center><b>
图 25：不同边界假定与滤波半径下飞翼结构拓扑优化结果对比。(a) 线性插值 PIML ($R_{\min} = 10\times$ 细单元尺寸)；(b) Bézier 插值 PIML ($R_{\min} = 2.5\times$)；(c) Bézier 插值 PIML ($R_{\min} = 1.5\times$)。
</b></center>

对比结果在图 25 中尤为震撼：
- 线性插值由于人工刚性过大，必须采用 $R_{\min} = 10\times$ 的极大滤波半径，构型退化为粗壮单调的块状支撑，柔度目标为 31.5；
- 三次 Bézier 插值在 $R_{\min} = 2.5\times$ 下柔度降至 23.96；在 $R_{\min} = 1.5\times$ 下柔度进一步大幅降低至 **20.29**（刚度提升超过 35%）。

![[Guo2026_Bezier_Fig26.png]]
<center><b>
图 26：对应于图 25(c) 的飞翼优化结构内部细节。(a) 包含非设计蒙皮的全景视图；(b) 隐藏底面蒙皮后暴露出的极其复杂的内部仿生支撑拓扑。
</b></center>

![[Guo2026_Bezier_Fig27.png]]
<center><b>
图 27：飞翼优化结构的多视角观察视图。
</b></center>

![[Guo2026_Bezier_Fig28.png]]
<center><b>
图 28：飞翼优化结构的剖面细节视图，突出了内部光滑连续的加劲肋以及局部微型 MBB 梁状传力特征。
</b></center>

从图 26、图 27 与图 28 可以看出，模型自发生成了极其精细光滑、树状分支的仿生叶脉式加劲肋网络，在关键承力部位自发形成了多级微型桁架与微型 MBB 梁构造。整个拓扑完全没有棋盘格杂波，边界连续光滑。

![[Guo2026_Bezier_Fig29.png]]
<center><b>
图 29：飞翼结构拓扑优化迭代过程中的柔度目标函数收敛历史曲线，展示了在惩罚因子递增策略下的高稳定性。
</b></center>

图 29 表明优化过程在惩罚延续策略下展现出了极佳的平稳单调收敛性。

![[Guo2026_Bezier_Fig30.png]]
<center><b>
图 30：(a) 采用 SIMP 框架、在 6750 个计算核心并行驱动下完成的 **100 亿自由度** 悬臂梁拓扑优化构型，单步迭代仅耗时 42 秒；(b)-(c) 100 亿自由度悬臂梁的局部精细结构细节展示 [66]。
</b></center>

最后，结合前期团队开发的分布式并行 PIML 技术 [66]，利用 6750 个 CPU 核心成功实现了对 **100 亿自由度** 悬臂梁超大规模结构的拓扑优化（图 30），平均每步迭代耗时仅 42 秒，展现了 PIML-Bézier 技术向极大规模工业级高保真分析优化的无缝拓展潜力。

---

# 5 结论

本文针对大规模结构力学分析与高分辨率拓扑优化，提出了一种基于三次 Bézier 边界位移插值的高泛化 AI 增强子结构计算框架。
1. **理论突破**：建立了利用高阶 Bézier 曲线与双三次 Bézier 曲面参数化子结构边界位移的理论体系，彻底克服了传统子结构及既有 PIML 方法依赖线性边界位移假定而导致的人工硬化与数值锁死难题。
2. **不变性保障**：从数学上严格证明了 Bézier 边界插值诱导的高阶数值形函数在刚体平移与转动下的严格不变性，并将其转化为神经网络训练中的硬约束，确保了物理刚体模态的守恒与零空间维数的正确性。
3. **高泛化算子学习**：利用 DeepONet 学习从子结构内部随机材料拓扑到数值基函数的非线性映射，实现了输入材料无关、问题无关、输出连续坐标无关的泛化预测。
4. **小滤波半径与工业级结构设计**：在千万级飞翼复杂结构中实现了 $1.5\times$ 极小滤波半径的稳定优化，自发涌现出了精细复杂的仿生树状加劲筋条网络，极大提升了结构力学性能。

未来工作将进一步把高阶 Bézier 插值技术推广至非线性大变形、结构动力学、瞬态传热及多物理场耦合拓扑优化问题中。

---

# CRediT 作者贡献声明

- **Yilin Guo (郭一麟)**: 论文撰写 – 审阅与编辑、论文撰写 – 原稿、方法论、调查研究、形式分析；
- **Chang Liu (刘畅)**: 论文撰写 – 审阅与编辑、指导、方法论、经费获取、概念构思；
- **Zongliang Du (杜宗亮)**: 论文撰写 – 审阅与编辑、验证、调查研究；
- **Yibo Jia (贾一波)**: 论文撰写 – 审阅与编辑、验证、调查研究；
- **Chao Jiang (姜超)**: 验证、调查研究；
- **Xu Guo (郭旭)**: 论文撰写 – 审阅与编辑、指导、方法论、经费获取、概念构思；
- **Changyu Shen (申长雨)**: 论文撰写 – 审阅与编辑、验证、调查研究。

# 数据可用性声明

支撑本研究结果的数据可在合理请求下由通讯作者提供。

# 利益冲突声明

作者声明不存在可能影响本文报道工作的已知竞争性经济利益或人身关系。

# 致谢

本研究得到国家重点研发计划（项目编号：2023YFB3309104）、国家自然科学基金（项目资助号：124B2042，12472344）以及大连市科技人才创新支持计划（项目编号：2024RG001）的资助。

---

# 附录 A 同时存在表面力与体力时的子结构方法

在有限元方法中，体力可通过单元插值转化为结构域内的等效节点外载荷。当式 (2) 中的内部体力项不为零（即 $\mathbf{f}_i^j \neq \mathbf{0}$）时，第 $j$ 个子结构在表面力和体力共同作用下的平衡方程可写作：
$$
\begin{bmatrix}
\mathbf{K}_{bb}^j & (\mathbf{K}_{ib}^j)^\top \\
\mathbf{K}_{ib}^j & \mathbf{K}_{ii}^j
\end{bmatrix}
\begin{bmatrix}
\mathbf{u}_b^j \\
\mathbf{u}_i^j
\end{bmatrix}
=
\begin{bmatrix}
\widetilde{\mathbf{f}}_b^j \\
\widetilde{\mathbf{f}}_i^j
\end{bmatrix}. \tag{33}
$$
由式 (33) 第二行解出内部位移：
$$
\mathbf{u}_i^j = - (\mathbf{K}_{ii}^j)^{-1} \mathbf{K}_{ib}^j \mathbf{u}_b^j + (\mathbf{K}_{ii}^j)^{-1} \widetilde{\mathbf{f}}_i^j.
$$
将其代入第一行，消元整理可得：
$$
\left( \mathbf{K}_{bb}^j - (\mathbf{K}_{ib}^j)^\top (\mathbf{K}_{ii}^j)^{-1} \mathbf{K}_{ib}^j \right) \mathbf{u}_b^j = \widetilde{\mathbf{f}}_b^j - (\mathbf{K}_{ib}^j)^\top (\mathbf{K}_{ii}^j)^{-1} \widetilde{\mathbf{f}}_i^j. \tag{34}
$$
由式 (34) 可以清晰看出：表面力与体力的存在**完全不会改变子结构缩聚刚度矩阵 $\mathbf{K}_s^j$ 的形式**（式 4）。保持多尺度数值形函数矩阵表达式 $\mathbf{N}_s^j = - (\mathbf{K}_{ii}^j)^{-1} \mathbf{K}_{ib}^j$ 不变，利用 $\mathbf{K}_{ii}^j$ 的对称性，式 (34) 右端等效载荷项可直接改写为：
$$
\widetilde{\mathbf{f}}_b^j + (\mathbf{N}_s^j)^\top \widetilde{\mathbf{f}}_i^j.
$$
这意味着求解全局降阶方程组仅需将外载荷向量替换为：
$$
\widetilde{\mathbf{f}}_b = \sum_{j=1}^N (\mathbf{G}^j)^\top \left( \widetilde{\mathbf{f}}_b^j + (\mathbf{N}_s^j)^\top \widetilde{\mathbf{f}}_i^j \right).
$$
由于数值形函数矩阵 $\mathbf{N}_s^j$ 形式完全未变，本文提出的 PIML 深度学习模型在此类工况下完全通用。类似地，对于引入了边界插值矩阵 $\mathbf{S}^j$ 的高阶子结构，凝聚外载荷向量仅需相应修改为：
$$
\widetilde{\mathbf{f}}_r^j = (\mathbf{S}^j)^\top \left( \widetilde{\mathbf{f}}_b^j + (\mathbf{N}_s^j)^\top \widetilde{\mathbf{f}}_i^j \right).
$$

---

# 附录 B 插值矩阵 $\mathbf{S}$ 的推导

在本附录中，显式推导基于 Lagrange、B 样条、NURBS 基函数以及分层多项式的边界插值矩阵 $\mathbf{S}$。通过在式 (8) 中替换对应的矩阵 $\mathbf{S}$，均可在本文所呈现的相同算子学习框架下完成网络训练并加速力学分析。

设 $\mathbf{u}_r^\alpha$ 表示子结构第 $\alpha$ 个边界边/面上的全部边界节点位移向量，$\mathbf{u}_r^\alpha$ 表示该边/面上的边界控制点位移向量。边界映射关系定义为 $\mathbf{u}_b^\alpha = \mathbf{S}^\alpha \mathbf{u}_r^\alpha$。对于 $\mathbf{S}^\alpha$，其矩阵元 $S_{m, i}^\alpha$ 为第 $i$ 个基函数在第 $m$ 个边界节点参数坐标 $\mathbf{x}_m \in [0, 1]$ 处的取值。全局插值矩阵 $\mathbf{S}$ 由所有边界实体组装得到：$\mathbf{S} = \sum_\alpha \mathbf{S}^\alpha$。

## B.1 Lagrange 插值

对于包含 $p + 1$ 个控制点的边界段，Lagrange 多项式 $L_i(\mathbf{x})$ 定义为：
$$
L_i(\mathbf{x}) = \prod_{\substack{j=0 \\ j \neq i}}^p \frac{\mathbf{x} - \mathbf{x}_j}{\mathbf{x}_i - \mathbf{x}_j}, \tag{35}
$$
此时插值矩阵元素为 $S_{m, i}^\alpha = L_i(\mathbf{x}_m)$。

## B.2 B 样条插值

采用 Cox–de Boor 递推公式，在节点向量 $\mathbf{U} = \{u_0, u_1, \dots, u_{n+k+1}\}$ 上定义的 $k$ 阶 B 样条基函数 $B_{i, k}(\mathbf{x})$ 为：
$$
B_{i, 0}(\mathbf{x}) = \begin{cases}
1, & u_i \le \mathbf{x} < u_{i+1}, \\
0, & \text{其他},
\end{cases} \tag{36}
$$
$$
B_{i, k}(\mathbf{x}) = \frac{\mathbf{x} - u_i}{u_{i+k} - u_i} B_{i, k-1}(\mathbf{x}) + \frac{u_{i+k+1} - \mathbf{x}}{u_{i+k+1} - u_{i+1}} B_{i+1, k-1}(\mathbf{x}). \tag{37}
$$
对于二维情况（一维边界边），插值矩阵元为 $S_{m, i}^\alpha = B_{i, k}(\mathbf{x}_m)$。
对于三维情况（二维边界面），设 $u, \omega$ 为两个参数方向，节点向量分别为 $\mathbf{U}_u, \mathbf{U}_\omega$。对应控制点 $P_{i, j}$ 在表面节点 $(\mathbf{x}_u^m, \mathbf{x}_\omega^m)$ 处的插值元为：
$$
S_{m, (i, j)}^\alpha = B_{i, k_u}(\mathbf{x}_u^m) B_{j, k_\omega}(\mathbf{x}_\omega^m). \tag{38}
$$

## B.3 非均匀有理 B 样条 (NURBS) 插值

NURBS 通过引入权重因子 $\omega_i$ 推广了 B 样条。对于二维边界，NURBS 基函数 $R_{i, k}(\mathbf{x})$ 定义为：
$$
R_{i, k}(\mathbf{x}) = \frac{\omega_i B_{i, k}(\mathbf{x})}{\sum_{j=0}^n \omega_j B_{j, k}(\mathbf{x})}. \tag{39}
$$
相应地，插值矩阵元为 $S_{m, i}^\alpha = R_{i, k}(\mathbf{x}_m)$。
对于三维边界面：
$$
S_{m, (i, j)}^\alpha = \frac{\omega_{i, j} B_{i, k_u}(\mathbf{x}_u^m) B_{j, k_\omega}(\mathbf{x}_\omega^m)}{\sum_{p=0}^{n_u} \sum_{q=0}^{n_\omega} \omega_{p, q} B_{p, k_u}(\mathbf{x}_u^m) B_{q, k_\omega}(\mathbf{x}_\omega^m)}. \tag{40}
$$
值得指出的是，**三次 Bézier 曲线/曲面正是 NURBS 曲线在权重恒定、阶数 $k=3$、控制点数 $n=3$ 且节点向量取开均匀向量 $T = \{0, 0, 0, 0, 1, 1, 1, 1\}$ 时的特例**。在此情况下，B 样条基底严格退化为 Bernstein 基底。

## B.4 分层多项式 (Hierarchical Polynomials)

将边界节点坐标与控制点坐标映射至参考区间 $[-1, 1]$，并利用积分勒让德多项式（Integrated Legendre Polynomials）构建分层多项式基底。基底包含线性节点模态与高阶内部模态。
对于线性节点模态 ($p = 1$)：
$$
H_1(\mathbf{x}) = \frac{1 - \mathbf{x}}{2}, \quad H_2(\mathbf{x}) = \frac{1 + \mathbf{x}}{2}. \tag{41}
$$
对于高阶内部模态：
$$
H_{p+1}(\mathbf{x}) = \int_{-1}^{\mathbf{x}} L_p(t) \, \mathrm{d}t, \tag{42}
$$
其中 $L_p$ 为 $p$ 阶勒让德多项式。对于二维边界边，矩阵 $\mathbf{S}^\alpha$ 可写为：
$$
\mathbf{S}^\alpha = \begin{bmatrix}
H_1(\mathbf{x}_1) & \dots & H_{p+1}(\mathbf{x}_1) \\
\vdots & \ddots & \vdots \\
H_1(\mathbf{x}_{N_r}) & \dots & H_{p+1}(\mathbf{x}_{N_r})
\end{bmatrix}. \tag{43}
$$
对于三维情况（子结构的二维边界面），基函数由两个方向的一维分层基底张量积构成：$S_{m, (i, j)}^\alpha = H_i(\mathbf{x}_u^m) H_j(\mathbf{x}_\omega^m)$。

---

---

# 参考文献

[1] M.R. Gurvich, R.B. Pipes, Mechanics of composite materials with high filler content, Compos. Sci. Technol. 55 (4) (1995) 347–358.

[2] J. Liu, Y. Ma, A survey of manufacturing oriented topology optimization methods, Adv. Eng. Softw. 100 (2016) 161–175.

[3] X. Yan, Q. Xia, T. Shi, Concurrent topology optimization of multiscale structures with graded lattice materials, Comput. Methods Appl. Mech. Eng. 362 (2020) 112874.

[4] P. Baud, T. Reuschlé, Y. Ji, T.F. Wong, Mechanical compaction and strain-induced permeability change in porous sandstone, J. Geophys. Res.: Solid Earth 105 (B7) (2000) 16371–16384.

[5] O.C. Zienkiewicz, R.L. Taylor, J.Z. Zhu, The Finite Element Method: Its Basis and Fundamentals, Elsevier, 2005.

[6] M.P. Bendsøe, O. Sigmund, Topology Optimization: Theory, Methods, and Applications, Springer Science & Business Media, 2003.

[7] M.P. Bendsøe, Optimal shape design as a material distribution problem, Struct. Optim. 1 (4) (1989) 193–202.

[8] M. Zhou, G.I.N. Rozvany, The COC algorithm, part II: topological, geometrical and generalized shape optimization, Comput. Methods Appl. Mech. Eng. 89 (1–3) (1991) 309–336.

[9] O. Sigmund, A 99 line topology optimization code written in matlab, Struct. Multidiscip. Optim. 21 (2) (2001) 120–127.

[10] T.A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006.

[11] P. Ladevèze, Nonlinear Computational Structural Mechanics: New Approaches and Non-Incremental Methods of Calculation, Springer, 1999.

[12] D. Ryckelynck, A priori hyperreduction method: an adaptive approach, J. Comput. Phys. 202 (1) (2005) 346–366.

[13] K. Carlberg, C. Bou-Mosleh, C. Farhat, Efficient non-linear model reduction via a least-squares Petrov–Galerkin projection and compressive tensor approximations, Int. J. Numer. Methods Eng. 86 (2) (2011) 155–181.

[14] P. Kerfriden, P. Gosselet, S. Adhikari, S.P.A. Bordas, Bridging proper orthogonal decomposition methods and augmented Newton–Krylov algorithms: an adaptive, model order reduction for highly nonlinear structural mechanics, Comput. Methods Appl. Mech. Eng. 200 (5–8) (2011) 850–866.

[15] A. Radermacher, S. Reese, Pod-based model reduction with empirical interpolation applied to nonlinear elasticity, Int. J. Numer. Methods Eng. 107 (6) (2016) 477–495.

[16] P. Astrid, S. Weiland, K. Willcox, T. Backx, Missing point estimation in models described by P.D.E.s, IEEE Trans. Autom. Control 53 (10) (2008) 2237–2251.

[17] A. Bensoussan, J.L. Lions, G. Papanicolaou, Asymptotic Analysis for Periodic Structures, American Mathematical Society, 1978.

[18] E. Sanchez-Palencia, Non-Homogeneous Media and Vibration Theory, Springer, 1980.

[19] J.M. Guedes, N. Kikuchi, Preprocessing and postprocessing for materials based on the homogenization method with adaptive finite element methods, Comput. Methods Appl. Mech. Eng. 83 (2) (1990) 143–198.

[20] J. Fish, Q. Chen, Higher-order homogenization of initial/boundary-value problems, J. Appl. Mech. 68 (4) (2001) 531–538.

[21] F. Feyel, Multiscale FE2 elastoviscoplastic analysis of composite structures, Comput. Mater. Sci. 16 (1–4) (1999) 344–354.

[22] F. Feyel, J.L. Chaboche, FE2 multiscale approach for modelling the elastoviscoplastic behaviour of long fibre SiC/Ti composite materials, Comput. Methods Appl. Mech. Eng. 183 (3–4) (2000) 309–330.

[23] V. Kouznetsova, M.G.D. Geers, W.A.M. Brekelmans, Multi-scale constitutive modelling of heterogeneous materials via a computational homogenization scheme, Int. J. Numer. Methods Eng. 54 (8) (2002) 1235–1260.

[24] E.W.C. Coenen, V.G. Kouznetsova, M.G.D. Geers, Multi-scale continuous–discontinuous framework for computational-homogenization-based analysis of localized fracture in heterogeneous materials, Int. J. Numer. Methods Eng. 92 (1) (2012) 41–65.

[25] J. Pathak, S. Shankaran, E. Stock, S. Lu, S. Saha, S. Ravichandran, FourCastNet: a global data-driven high-resolution weather model using adaptive Fourier neural operators, (2022), arXiv preprint arXiv:2202.11214.

[26] S.L. Brunton, B.R. Noack, P. Koumoutsakos, Machine learning for fluid mechanics, Annu. Rev. Fluid Mech. 52 (2020) 477–508.

[27] Y. Zhao, L. Zhang, T.A. Zaki, Deep learning for turbulent channel flow using boundary and interior data, Phys. Rev. Fluids 8 (1) (2023) 014604.

[28] D. Xiao, C.E. Heaney, L. Mottet, F. Fang, W. Lin, I.M. Navon, Y. Guo, O.K. Matar, A.G. Robins, C.C. Pain, A reduced order model for turbulent flows in the urban environment using machine learning, Build. Environ. 148 (2019) 323–337.

[29] P. Raccuglia, K.C. Elbert, P.D.F. Adler, C. Falk, M.B. Wenny, A. Mollo, M. Zeller, S.A. Friedler, J. Schrier, A.J. Norquist, Machine-learning-assisted materials discovery using failed experiments, Nature 533 (7601) (2016) 73–76.

[30] G.R. Schleder, A.C.M. Padilha, C.M. Acosta, M. Costa, A. Fazzio, From DFT to machine learning: recent approaches to materials science–a review, J. Phys.: Mater. 2 (3) (2019) 032001.

[31] L. Zhang, J. Han, H. Wang, R. Car, W. E, Deep potential molecular dynamics: a scalable model with the accuracy of quantum mechanics, Phys. Rev. Lett. 120 (14) (2018) 143001.

[32] L. Zhang, Y. Lu, S. Tang, W.K. Liu, HideNN-TD: reduced-order hierarchical deep learning neural networks, Comput. Methods Appl. Mech. Eng. 389 (2022) 114414.

[33] H. Li, S. Knapik, Y. Li, C. Park, J. Guo, S. Mojumder, Y. Lu, W. Chen, D.W. Apley, W.K. Liu, Convolution hierarchical deep-learning neural network tensor decomposition (C-HideNN-TD) for high-resolution topology optimization, Comput. Mech. 72 (2) (2023) 363–382.

[34] G. Cheng, X. Li, Y. Nie, H. Li, FEM-Cluster Based reduction method for efficient numerical prediction of effective properties of heterogeneous material in nonlinear range, Comput. Methods Appl. Mech. Eng. 348 (2019) 157–184.

[35] Y. Nie, Z. Li, G. Cheng, Efficient prediction of the effective nonlinear properties of porous material by FEM-Cluster based analysis (FCA), Comput. Methods Appl. Mech. Eng. 383 (2021) 113921.

[36] Y. Nie, Z. Li, X. Gong, G. Cheng, Fast construction of cluster interaction matrix for data-driven cluster-based reduced-order model and prediction of elastoplastic stress-strain curves and yield surface, Comput. Methods Appl. Mech. Eng. 418 (2024) 116480.

[37] M. Raissi, P. Perdikaris, G.E. Karniadakis, Physics-informed neural networks: a deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations, J. Comput. Phys. 378 (2019) 686–707.

[38] G.E. Karniadakis, I.G. Kevrekidis, L. Lu, P. Perdikaris, S. Wang, L. Yang, Physics-informed machine learning, Nature Rev. Phys. 3 (6) (2021) 422–440.

[39] M. Raissi, A. Yazdani, G.E. Karniadakis, Hidden fluid mechanics: learning velocity and pressure fields from flow visualizations, Science 367 (6481) (2020) 1026–1030.

[40] E. Ulu, R. Zhang, L.B. Kara, A data-driven investigation and estimation of optimal topologies under variable loading configurations, Comput. Method. Biomech. Biomed. Eng.: Imag. Visual. 4 (2) (2016) 61–72.

[41] X. Lei, C. Liu, Z. Du, W. Zhang, X. Guo, Machine learning-driven real-time topology optimization under moving morphable component-based framework, J. Appl. Mech. 86 (1) (2019) 011004.

[42] S. Zheng, H. Fan, Z. Zhang, Z. Tian, K. Jia, Accurate and real-time structural topology prediction driven by deep learning under moving morphable component-based framework, Appl. Math. Model. 97 (2021) 522–535.

[43] D. Geng, J. Yan, Q. Xu, Q. Zhang, M. Zhou, Z. Fan, H. Li, Real-Time structure topology optimization using CNN driven moving morphable component method, Eng. Struct. 290 (2023) 116376.

[44] Y. Yu, T. Hur, J. Jung, I.G. Jang, Deep learning for determining a near-optimal topological design without any iteration, Struct. Multidiscip. Optim. 59 (3) (2019) 787–799.

[45] H. Chi, Y. Zhang, T.L.E. Tang, L. Mirabella, L. Dalloro, L. Song, G.H. Paulino, Universal machine learning for topology optimization, Comput. Methods Appl. Mech. Eng. 375 (2021) 112739.

[46] F.V. Senhora, H. Chi, Y. Zhang, L. Mirabella, T.L.E. Tang, G.H. Paulino, Machine learning for topology optimization: physics-based learning through an independent training strategy, Comput. Methods Appl. Mech. Eng. 398 (2022) 115116.

[47] M.O. Elingaard, N. Aage, J.A. Bærentzen, O. Sigmund, De-homogenization using convolutional neural networks, Comput. Methods Appl. Mech. Eng. 388 (2022) 114197.

[48] J.P. Groen, F.C. Stutz, N. Aage, J.A. Bærentzen, O. Sigmund, De-homogenization of optimal multi-scale 3D topologies, Comput. Methods Appl. Mech. Eng. 364 (2020) 112979.

[49] M. Huang, Z. Du, C. Liu, Y. Zheng, T. Cui, Y. Mei, X. Li, X. Zhang, X. Guo, Problem-independent machine learning (PIML)-based topology optimization-a universal approach, Extreme Mech. Lett. 56 (2022) 101887.

[50] M. Huang, T. Cui, C. Liu, Z. Du, J. Zhang, C. He, X. Guo, A problem-Independent machine learning (PIML) enhanced substructure-based approach for large-scale structural analysis and topology optimization of linear elastic structures, Extreme Mech. Lett. 63 (2023) 102041.

[51] K. Moore, Guyan Reduction, MATLAB Central File Exchange, (2025).

[52] J. Chen, Y. Zhou, Dynamic responses of subgrade under double-line high-speed railway, Soil Dyn. Earthquake Eng. 110 (2018) 1–12.

[53] J.M. Melenk, I. Babuška, The partition of unity finite element method: basic theory and applications, Comput. Methods Appl. Mech. Eng. 139 (1) (1996) 289–314.

[54] S. Rajendran, B.R. Zhang, A “FE-meshfree” QUAD4 element based on partition of unity, Comput. Methods Appl. Mech. Eng. 197 (1) (2007) 128–147.

[55] M. Huang, C. Liu, Y. Guo, L. Zhang, Z. Du, X. Guo, A mechanics-based data-free problem independent machine learning (PIML) model for large-scale structural analysis and design optimization, J. Mech. Phys. Solids 193 (2024) 105893.

[56] T. Yue, H. Yang, Z. Du, C. Liu, K.I. Elkhodary, S. Tang, X. Guo, A mechanistic-based data-driven approach to accelerate structural topology optimization through finite element convolutional neural network (FE-CNN), (2021), arXiv preprint arXiv:2106.13652.

[57] M. Zhou, G.I.N. Rozvany, The COC algorithm, part II: topological, geometrical and generalized shape optimization, Comput. Methods Appl. Mech. Eng. 89 (1–3) (1991) 309–336.

[58] O. Sigmund, A 99 line topology optimization code written in matlab, Struct. Multidiscip. Optim. 21 (2) (2001) 120–127.

[59] E. Andreassen, A. Clausen, M. Schevenels, B.S. Lazarov, O. Sigmund, Efficient topology optimization in MATLAB using 88 lines of code, Struct. Multidiscip. Optim. 43 (1) (2011) 1–16.

[60] F. Ferrari, O. Sigmund, A new generation 99 line matlab code for compliance topology optimization and its extension to 3D, Struct. Multidiscip. Optim. 62 (4) (2020) 2211–2228.

[61] Y. Guo, C. Liu, Y. Jia, C. Shen, X. Guo, A multi-material topology optimization method based on implicit topology description functions, Comput. Methods Appl. Mech. Eng. 436 (2025) 117676.

[62] Z. Du, T. Cui, C. Liu, W. Zhang, Y. Guo, X. Guo, An efficient and easy-to-extend matlab code of the moving morphable component (MMC) method for three-dimensional topology optimization, Struct. Multidiscip. Optim. 65 (5) (2022) 158.

[63] X. Guo, W. Zhang, W. Zhong, Doing topology optimization explicitly and geometrically-a new moving morphable components based framework, J. Appl. Mech. 81 (8) (2014) 081009.

[64] M.Y. Wang, X. Wang, D. Guo, A level set method for structural topology optimization, Comput. Methods Appl. Mech. Eng. 192 (1–2) (2003) 227–246.

[65] N.P. Van Dijk, K. Maute, M. Langelaar, F. Van Keulen, Level-set methods for structural topology optimization: a review, Struct. Multidiscip. Optim. 48 (3) (2013) 437–472.

[66] X. Ma, M. Huang, Z. Du, Y. Guo, C. Liu, Y. Mei, X. Guo, A high-Performance parallel algorithm based on problem independent machine learning (piml) for large-Scale topology optimization, Available at SSRN 5003535 (2024).
