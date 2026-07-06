# A mechanics-based data-free problem independent machine learning (PIML) model for large-scale structural analysis and design optimization

## 完整中文译文

> 原笔记：[[../Huang2024-PIML-datafree]]
> Zotero 条目：`zotero://select/library/items/CGQZ2HXL`
> PDF 附件：`C:\Users\Lenovo\Zotero\storage\R85965MZ\Huang 等 - 2024 - A mechanics-based data-free ...pdf`
> 说明：正文（摘要—结论）、附录 A/B 与图 1–14 均已补齐；图片存于 `topology-opt/assets/Huang2024_FigX.png`。

---

# 0 元数据

- **题名**：A mechanics-based data-free Problem Independent Machine Learning (PIML) model for large-scale structural analysis and design optimization
- **中文暂译**：一种基于力学机制的无数据问题无关机器学习（PIML）模型：用于大规模结构分析与设计优化
- **作者**：Mengcheng Huang; Chang Liu; Yilin Guo; Linfeng Zhang; Zongliang Du; Xu Guo
- **单位**：大连理工大学 工程力学系 工业装备结构分析优化与 CAE 软件国家重点实验室；大连理工大学宁波研究院
- **期刊**：Journal of the Mechanics and Physics of Solids
- **年份**：2024
- **卷/文章号**：193:105893
- **DOI**：10.1016/j.jmps.2024.105893
- **Zotero key**：CGQZ2HXL
- **Better BibTeX key**：Huang2024-mechanicsbaseddatafree
- **译文状态**：全文译毕并配图（正文＋附录 A/B、式 1–25、表 1–3、图 1–14）

# 摘要

机器学习（ML）增强的快速结构分析与设计近年来受到了广泛关注。然而，在大多数相关工作中，ML 模型的泛化能力与数据集生成的巨大成本是最受诟病的两个方面。本文结合了子结构方法的通用性与算子学习（operator learning）架构优越的预测能力这两方面的优势。具体而言，借助一种新颖的基于力学的损失函数，无需准备数据集即可训练出一个从子结构内材料分布到相应连续多尺度形函数的轻量级神经网络映射。由此，本文提出了一种问题无关机器学习（PIML）模型[^abstract-typo]，它可普遍适用于任意尺寸、各种边界条件下大规模结构的高效线弹性分析与设计优化。若干算例验证了本文工作在效率提升以及各类优化问题上的有效性。这一基于 PIML 模型的设计与优化框架可进一步推广到大规模多物理场问题。

**关键词**：大规模结构分析（Large-scale structural analysis）；拓扑优化（Topology optimization）；问题无关机器学习（Problem Independent Machine Learning）；无数据（Data free）；算子学习（Operator learning）

[^abstract-typo]: 原文此处作 “a problem machine learning model (PIML)”，对照缩写 PIML 及全文语境可知漏掉了 “independent” 一词，此处译为“问题无关机器学习”。

# 1 引言

结构分析与拓扑优化已在工程中得到广泛应用（Rozvany, 2009；Deaton 和 Grandhi, 2014；Guo 和 Cheng, 2010；Sigmund 和 Maute, 2013）。然而，作为一种为结构设计出最优性能的合理方法，拓扑优化的求解过程通常需要对中间结构进行数十至数百次迭代数值分析，对于大规模优化问题，这部分可能占到 95% 以上的计算成本。因此，提高大规模结构数值分析的效率，对于推动拓扑优化研究与应用的前沿至关重要。文献中，人们已采用并行算法（Borrvall 和 Petersson, 2001；Aage 和 Lazarov, 2013；Aage 等, 2017；Liu 等, 2018a）、多重网格方法（Amir 等, 2014；Hackbusch, 2013；Le Maître 等, 2003）、冗余自由度（DOFs）消除技术（Zhang 等, 2017；Du 等, 2022）以及降阶建模（Amsallem 等, 2015；Hoang 等, 2016；Dutta 等, 2018；Xiao 等, 2020）等方法来提升拓扑优化的求解效率。

随着人工智能的快速发展，机器学习（ML）增强的拓扑优化方法近来受到了广泛关注。Sosnovik 和 Oseledets 在 SIMP 框架内使用卷积神经网络（CNNs），只需少数几步迭代即可获得最终优化设计（Sosnovik 和 Oseledets, 2019）。为进一步实现实时拓扑优化，Yu 等直接构建了一个将设计信息映射到最终优化结构的 CNN 模型（Yu 等, 2019）。该工作后来通过采用基于残差学习的 Res-U-Net 网络得到改进，显著增强了预测模型在超弹性结构优化中的性能（Abueidda 等, 2020）。Lei 等在可移动变形组件（MMC）框架内使用支持向量机，将外部载荷的位置与方向映射到最终优化构型中各组件的几何参数（Lei 等, 2019），此工作又借助 Res-U-Net 网络（Zheng 等, 2021）和 CNNs（Geng 等, 2023）得到改进。更多以最优设计为输出的端到端机器学习模型可参见 Woldseth 等（2022）。

与图像识别（Shafiq 和 Gu, 2022）、智能翻译（Cho 等, 2014）等领域不同，结构分析与优化过程涉及大量专家知识。已有报道指出，简单地应用机器学习技术来为结构响应或性能建立全局代理模型存在显著局限（Woldseth 等, 2022）。最突出的挑战在于，现有代理模型是问题相关（problem-specific）的，对于未包含在训练样本中的模型，其预测精度会显著下降。为增强神经网络的适用性并确保所训练模型的通用性，机器学习技术也被用于加速有限元分析，而非追求端到端映射。例如，Keshavarzzadeh 等提出了一种基于神经网络与低秩近似理论来计算细网格响应的新方法（Keshavarzzadeh 等, 2021）。Zhang 等将 CNNs 与张量分解相结合，取得了比传统张量分解和适当广义分解（PGD）更高的精度（Zhang 等, 2022）。Yue 等提出了一种有限元卷积神经网络，将高分辨率有限元解映射为低分辨率解（Yue 等, 2021）。Chi 等利用迭代过程中收集的训练数据，在多分辨率框架下提出了一种高效的拓扑优化在线机器学习方法（Chi 等, 2021），并进一步发展为离线训练、在线预测。数值算例表明，该方法能够处理分辨率达数千万的大规模设计问题，将结构分析效率提升约 30 倍（Senhora 等, 2022）。

为保证 ML 增强方案独立于拓扑优化问题的设定（如边界条件、设计域和外部载荷等），Huang 等提出了一种问题无关机器学习（PIML）算法，可应用于同一控制方程下的各种设计问题（Huang 等, 2022, 2023）。与大规模结构的全尺度分析不同，子结构方法或扩展多尺度有限元方法（EMsFEM）能够在粗网格上以缩减的自由度求解平衡方程。PIML 模型着眼于切除这些方法中最耗时的部分——通过训练人工神经网络（ANNs），在子结构内材料分布与多尺度形函数之间建立隐式映射，而多尺度形函数描述了粗网格自由度与全部自由度之间的关系。数值算例表明，与使用全尺度分析的传统算法相比，PIML 增强的流程对于大规模算例可实现两个数量级以上的求解效率提升。然而，在监督学习的处理方式下（Huang 等, 2022, 2023），现有 PIML 模型主要存在三个有待进一步解决的问题：（1）使用经典的均方误差（MSE）作为损失函数虽然直接，但未充分考虑多尺度形函数背后的物理原理，这限制了所训练模型的泛化能力；（2）对于相对较大的三维子结构，例如由 10×10×10 甚至更多细尺度单元构成的子结构，由于输出数量庞大，构建有效的轻量级 ANNs 颇具挑战；（3）为相对较大的三维子结构生成数据集的时间成本相当高昂。

为解决上述三个问题，本文将每个节点处的多尺度形函数矩阵升级为坐标的连续函数，并使用深度算子网络来预测该函数。此外，通过重访子结构方法，本文提出了一种新颖的基于力学的损失函数，使深度算子网络无需包含多尺度形函数值的数据集即可得到良好训练。因此，本文工作的三大优势可概括为：（1）在保持网络架构不变的前提下，可用于任意尺寸的子结构；（2）由于无需包含多尺度形函数值的数据集，训练这一无监督 PIML 模型的成本可大幅降低；（3）本文工作可用于任意尺寸、各种边界条件下大规模结构的高效线弹性分析与设计优化。

本文其余部分组织如下：第 2 节重访子结构方法，以阐明多尺度形函数的物理含义；随后简要勾勒现有的监督学习 PIML 模型，以说明其核心思想与局限（第 3 节）；第 4 节介绍基于力学的无数据 PIML 模型及其在大规模结构分析与优化中的应用；第 5 节的三个数值算例展示了本文工作的有效性；最后，第 6 节给出结论性评述。

# 2 重访子结构方法

子结构方法最初是作为一种静力缩聚（static condensation）方法而发展起来的，用以缩减刚度矩阵和质量矩阵的自由度（Guyan, 1965；Wilson, 1974）。如图 1(a) 所示，结合区域分解与有限元方法，每个子结构 $\Omega_j$（$j=1,\dots,N$，注意 $\Omega_j$ 包含多个细尺度单元）内的平衡可独立地表示为：

$$\boldsymbol{K}^j \boldsymbol{u}^j = \boldsymbol{f}^j \tag{1}$$

其中 $\boldsymbol{K}^j$ 是子结构 $\Omega_j$ 的刚度矩阵，$\boldsymbol{u}^j$ 与 $\boldsymbol{f}^j$ 分别是该子结构的位移向量与力向量。接着，如图 1(b)，将每个子结构的节点分为内部节点与边界节点，分别用下标 i 与 b 表示。于是式 (1) 可分解为如下形式：

$$\begin{pmatrix} \boldsymbol{K}^j_{bb} & \left(\boldsymbol{K}^j_{ib}\right)^{\mathsf{T}} \\ \boldsymbol{K}^j_{ib} & \boldsymbol{K}^j_{ii} \end{pmatrix} \begin{pmatrix} \boldsymbol{u}^j_b \\ \boldsymbol{u}^j_i \end{pmatrix} = \begin{pmatrix} \boldsymbol{f}^j_b \\ \boldsymbol{f}^j_i \end{pmatrix} \tag{2}$$

不失一般性，假设外载荷不作用于内部节点，即 $\boldsymbol{f}^j_i = \boldsymbol{0}$。将其代入上式，可得 $\boldsymbol{u}^j_b$ 与 $\boldsymbol{u}^j_i$ 之间的关系式 (3)。实际上，当 $\boldsymbol{f}^j_i \neq \boldsymbol{0}$ 时子结构方法同样适用，详细推导见附录 A。

$$\boldsymbol{u}^j_i = -\left(\boldsymbol{K}^j_{ii}\right)^{-1}\boldsymbol{K}^j_{ib}\,\boldsymbol{u}^j_b \tag{3}$$

进一步将式 (3) 代入式 (2)，可得到仅包含边界节点自由度的缩聚刚度矩阵 $\boldsymbol{K}^j_s$：

$$\boldsymbol{K}^j_s = \boldsymbol{K}^j_{bb} - \left(\boldsymbol{K}^j_{ib}\right)^{\top}\left(\boldsymbol{K}^j_{ii}\right)^{-1}\boldsymbol{K}^j_{ib} \tag{4}$$

然后，通过组装各子结构的缩聚刚度矩阵，可得到全局缩聚刚度矩阵 $\boldsymbol{K}_s = \sum_j \boldsymbol{G}^j \boldsymbol{K}^j_s$，其中 $\boldsymbol{G}^j$ 表示第 $j$ 个子结构用于组装的定位矩阵。如此，无需求解原始的全尺度平衡方程，只需求解如下缩聚平衡方程即可获得各子结构边界节点的位移向量：

$$\boldsymbol{K}_s \boldsymbol{u}_b = \boldsymbol{f}_b \tag{5}$$

随后，各子结构内部节点的位移可分别由式 (3) 得到。值得注意的是，上述推导是从矩阵运算的角度进行的，掩盖了缩聚刚度矩阵背后的物理内涵。此外，研究发现，直接用机器学习从子结构内的材料分布预测缩聚刚度矩阵并不能得到令人满意的结果。因此，为进一步挖掘其物理意义，本文从多尺度形函数的角度重新推导缩聚刚度矩阵。

![[Huang2024_Fig1.png]]

<div align="center">

图 1：(a) 由子结构划分的结构域；(b) 子结构 $\Omega_j$ 的节点位移分为内部节点位移向量 $\boldsymbol{u}^j_i$ 与边界节点位移向量 $\boldsymbol{u}^j_b$；(c) 子结构 $\Omega_j$ 边界上的线性变形假设。

</div>

## 2.1 子结构方法的复现

借助位移插值的思想，式 (3) 可重写为如下线性变换关系：

$$\boldsymbol{u}^j_i = \boldsymbol{N}^j_s \boldsymbol{u}^j_b \tag{6}$$

其中 $\boldsymbol{N}^j_s \in \mathbb{R}^{n_i \times n_b}$ 是由边界节点位移计算内部节点位移的多尺度形函数，$n_i$ 与 $n_b$ 分别表示子结构内部节点与边界节点的总自由度数。于是，整个子结构的节点位移可表示为：

$$\boldsymbol{u}^j = \begin{bmatrix} \boldsymbol{u}^j_i \\ \boldsymbol{u}^j_b \end{bmatrix} = \begin{bmatrix} \boldsymbol{N}^j_s \\ \boldsymbol{I} \end{bmatrix} \boldsymbol{u}^j_b = \boldsymbol{N}^j \boldsymbol{u}^j_b$$

其中 $\boldsymbol{N}^j$ 表示由边界节点位移计算第 $j$ 个子结构节点位移的（离散）多尺度形函数矩阵。第 $j$ 个子结构的总应变能可换一种方式计算为：

$$W^j = \frac{1}{2}\left(\boldsymbol{u}^j\right)^{\top}\boldsymbol{K}^j\boldsymbol{u}^j = \frac{1}{2}\left(\boldsymbol{u}^j_b\right)^{\top}\left(\boldsymbol{N}^j\right)^{\top}\boldsymbol{K}^j\boldsymbol{N}^j\boldsymbol{u}^j_b = \frac{1}{2}\left(\boldsymbol{u}^j_b\right)^{\top}\boldsymbol{K}^j_s\boldsymbol{u}^j_b \tag{7}$$

因此，缩聚刚度矩阵可由多尺度形函数计算为：

$$\boldsymbol{K}^j_s = \left(\boldsymbol{N}^j\right)^{\top}\boldsymbol{K}^j\boldsymbol{N}^j \tag{8}$$

值得注意的是，将 $\boldsymbol{N}^j_s = -\left(\boldsymbol{K}^j_{ii}\right)^{-1}\boldsymbol{K}^j_{ib}$ 代入式 (8)，并利用式 (2)，即可复现式 (4) 中缩聚刚度矩阵的精确表达式。与式 (4) 由矩阵运算得到的缩聚刚度矩阵相比，上式清楚地表明：子结构的缩聚刚度矩阵可通过多尺度形函数矩阵对全局刚度矩阵作对称变换而得到。

尽管经典子结构方法能够降低全局刚度矩阵的维数，但其自由度的缩减相当有限。特别地，将细网格边长固定为 1，对于图 1(a) 所示由均匀各向同性材料构成的二维悬臂梁，将结构域用不同数目、每个含 $m \times m$ 细网格的均匀子结构离散，如表 1 所示。子结构方法所得节点位移向量与全尺度分析基准之间的相对误差（$U_{\mathrm{RE}} = \lVert \boldsymbol{U}_{\mathrm{Fine}} - \boldsymbol{U}_{\mathrm{sub}} \rVert / \boldsymbol{U}_{\mathrm{Fine}}$）始终可忽略不计。然而，与全尺度分析的时间成本 $t_F$ 相比，子结构分析算法的时间成本 $t_{\mathrm{sub}}$ 在二维情形下始终大得多。这是因为在表 1 的二维问题中，求解原始平衡方程的时间成本本就微不足道，故由全局刚度矩阵维数缩减所带来的效率提升极为有限；而计算缩聚全局刚度矩阵的额外开销（尤其是含求逆运算 $-\left(\boldsymbol{K}^j_{ii}\right)^{-1}\boldsymbol{K}^j_{ib}$ 的项）反而增加了总时间成本，且其矩阵带宽更大。

在三维情形下，如表 1 所示，由于子结构内自由度的缩减比例大得多，随着子结构数目的增加，子结构方法的效率优势逐渐显现。但遗憾的是，即使三维悬臂梁的有限单元数增至 250,000，子结构方法的时间成本（由 $5\times5\times5$ 单元构成的子结构约 691.3 s，由 $10\times10\times10$ 单元构成的子结构约 1052.3 s）也仅略小于全尺度分析所耗时间（约 1320 s）[^t-hardware]。此外，子结构算法的时间成本大多花在求解缩聚全局刚度矩阵上（内部节点位移插值所耗时间可忽略）。这促使我们进一步缩减经典子结构方法中的自由度，以获得更高的效率。


<div align="center">

表 1：用均匀子结构离散的悬臂梁，分别采用全尺度有限元分析与子结构方法的结果（计算缩聚全局刚度矩阵的时间成本记于圆括号内）。

</div>

| $m$ | 缩减自由度比例 | 子结构数目 | $U_{\mathrm{RE}}$ | $t_F$ (s) | $t_{\mathrm{sub}}$ (s) |
|---|---|---|---|---|---|
| **5 (2D)** | 0.6305 | 40×20 | $3.1440\times10^{-12}$ | 0.131 | 0.563 (0.469) |
| | 0.6362 | 100×50 | $1.5833\times10^{-12}$ | 1.051 | 3.599 (2.870) |
| | 0.6381 | 200×100 | $1.3202\times10^{-11}$ | 4.507 | 14.456 (13.320) |
| **10 (2D)** | 0.8040 | 40×20 | $2.5598\times10^{-12}$ | 0.609 | 2.646 (2.242) |
| | 0.8076 | 100×50 | $5.3495\times10^{-12}$ | 4.506 | 17.407 (14.490) |
| | 0.8088 | 200×100 | $1.7767\times10^{-11}$ | 20.264 | 73.722 (59.305) |
| **5 (3D)** | 0.4030 | 4×2×2 | $8.6324\times10^{-14}$ | 0.3197 | 0.8228 (0.3377) |
| | 0.4641 | 10×5×5 | $1.8108\times10^{-13}$ | 20.4318 | 23.7235 (4.9864) |
| | 0.4872 | 20×10×10 | $6.6940\times10^{-13}$ | $1.3287\times10^{3}$ | 691.3140 (32.0512) |
| **10 (3D)** | 0.6451 | 4×2×2 | $2.0279\times10^{-14}$ | 6.1650 | 35.8163 (16.8391) |
| | 0.6938 | 10×5×5 | $6.7571\times10^{-13}$ | $1.3221\times10^{3}$ | $1.0523\times10^{3}$ (254.350) |

[^t-hardware]: 原文脚注：本文时间成本均在配备 Intel(R) Xeon(R) Gold 6256 3.60 GHz CPU 与 512.0 GB 内存的台式机上测量。

## 2.2 基于边界变形线性假设的高效子结构分析

为进一步提高分析效率，一个自然的想法是进一步缩减子结构的独立边界节点，例如假设子结构边界上的位移可由顶点节点的位移线性插值得到（$\boldsymbol{u}^j_b = \boldsymbol{L}\boldsymbol{u}^j_v$，其中 $\boldsymbol{L} \in \mathbb{R}^{n_b \times n_v}$ 为线性插值矩阵，$n_v$ 为每个子结构顶点节点的自由度数），如图 1(c) 所示。与式 (7)、(8) 类似，边界节点线性假设下的缩聚刚度矩阵可表示为：

$$\tilde{\boldsymbol{K}}^j_s = \left(\boldsymbol{N}^j\boldsymbol{L}\right)^{\top}\boldsymbol{K}^j\left(\boldsymbol{N}^j\boldsymbol{L}\right) \triangleq \left(\tilde{\boldsymbol{N}}^j\right)^{\top}\boldsymbol{K}^j\tilde{\boldsymbol{N}}^j \tag{9}$$

其中 $\tilde{\boldsymbol{N}}^j = \boldsymbol{N}^j\boldsymbol{L}$ 是由顶点节点位移插值出子结构节点位移向量的多尺度形函数。如此，缩聚刚度矩阵的维数被进一步降低。

实际上，式 (9) 恰好等价于采用线性边界假设的扩展多尺度有限元方法（EMsFEM）（Zhang 等, 2014）——后者需要通过在子结构边界上分别施加线性变化的位移约束来获得。因此，式 (9) 显著降低了缩聚刚度矩阵的计算量。

还值得注意的是，这种基于边界变形线性假设的子结构分析，可视为用带一阶有限元的粗网格（即子结构）来分析整个结构，其中子结构内细网格的材料分布决定了单元刚度矩阵。

表 2 比较了三维悬臂梁分别由全尺度分析与带边界变形线性假设的子结构方法分析所得的相对误差与时间成本，以检验线性变形假设的效率与影响。显然，在线性变形假设下，子结构方法的分析结果会偏离全尺度分析结果。尽管如此，当子结构数目增加到 $10\times5\times5$ 时，相对误差 $U_{\mathrm{RE}}$ 已在 3% 以内。在 h 加密下，带边界变形线性假设的子结构方法也像经典有限元分析方法那样收敛（Hughes, 2012）。这一性质保证了在大规模分析问题中，对子结构采用边界变形线性假设的合理性。此外，与表 1 中的经典子结构方法相比，缩减自由度的比例显著提高（对于由 $20\times10\times10$ 个含 $5\times5\times5$ 细网格的子结构离散的悬臂梁，缩聚全局刚度矩阵的维数仅约为全尺度分析全局刚度矩阵规模的 1%）。此时缩聚刚度矩阵的求解时间变得可忽略。在这种情况下，$t_{\mathrm{sub}}$ 主要就是表 2 括号中所记的计算缩聚全局刚度矩阵的时间成本。这启发我们在下一节采用机器学习来切除式 (9) 中计算多尺度形函数 $\boldsymbol{N}^j\boldsymbol{L}$ 与缩聚刚度矩阵的时间成本。

**注释（Remark）**：为提高子结构方法的精度，此处的线性变形假设可放宽到更高阶的变形模式，例如采用以 B 样条描述的子结构边界变形假设（Li 和 Hu, 2022）。此时只需将 $\tilde{\boldsymbol{N}}^j$ 中的常数矩阵 $\boldsymbol{L}$ 修改为相应的高阶插值矩阵即可，后续所有 ML 流程均可直接实施，只是采用子结构边界的高阶变形假设会牺牲一定的求解效率。


<div align="center">

表 2：三维悬臂梁分别采用全尺度分析与带边界变形线性假设的子结构方法的结果（计算缩聚全局刚度矩阵的时间成本记于圆括号内）。

</div>

| $m$ | 缩减自由度比例 | 子结构数目 | $U_{\mathrm{RE}}$ | $t_F$ (s) | $t_{\mathrm{sub}}$ (s) |
|---|---|---|---|---|---|
| **5 (3D)** | 0.9823 | 4×2×2 | 0.1157 | 0.3359 | 0.2508 (0.2485) |
| | 0.9885 | 10×5×5 | 0.0283 | 21.6170 | 3.3141 (3.2863) |
| | 0.9903 | 20×10×10 | 0.0098 | $1.3221\times10^{3}$ | 28.7572 (28.3495) |
| **10 (3D)** | 0.9975 | 4×2×2 | 0.1192 | 6.6628 | 16.6714 (16.6658) |
| | 0.9985 | 10×5×5 | 0.0292 | $1.3221\times10^{3}$ | 243.6129 (243.5502) |

# 3 基于监督学习的问题无关机器学习（PIML）模型

本节首先介绍所谓问题无关机器学习（PIML）模型的思想，然后详述训练监督式机器学习模型的要点。

## 3.1 PIML 模型简介

子结构方法可普遍地用于分析非均质结构（例如结构拓扑优化问题中的中间设计），且独立于边界约束与载荷条件。对于如图 1(a) 由均匀子结构离散的结构，多尺度形函数（或缩聚刚度矩阵）由子结构内的材料分布决定，即

$$\tilde{\boldsymbol{N}}^j = \mathcal{F}\left(E_1, \dots, E_{m^2}\right) \tag{10}$$

作为示例，每个细网格中的杨氏模量一般代表子结构内材料属性的分布。一旦该映射 $\mathcal{F}$ 被机器学习模型捕获，它便可用于所有具有相同尺寸与细网格离散的子结构（$\Omega_i, i=1,\dots,N$），而与非均质结构的边界约束和载荷条件无关。在获得每个子结构的多尺度形函数（最耗时的部分）之后，如后文数值所示，计算式 (9) 中的缩聚刚度矩阵、在保留自由度上求解平衡方程、以及在内部节点自由度上插值位移，都将非常高效。因此，该模型被命名为 PIML 模型（Huang 等, 2022, 2023），它可应用于具有相同控制方程的有限元分析（例如线弹性问题），并不同于现有的端到端型机器学习模型。

![[Huang2024_Fig2.png]]

<div align="center">

图 2：关于多尺度形函数的物理约束：(a) 沿 $x$ 方向平动，$\boldsymbol{V}_1=(1,0,\dots,1,0)^{\top}$；(b) 沿 $y$ 方向平动，$\boldsymbol{V}_2=(0,1,\dots,0,1)^{\top}$；(c) 转动，$\boldsymbol{x}_v$ 与 $\boldsymbol{x}_i$ 分别为顶点节点与内部节点的坐标向量，$\boldsymbol{R}_v$ 与 $\boldsymbol{R}_i$ 分别为顶点节点与内部节点的转动矩阵。

</div>

## 3.2 通过监督学习训练 PIML 模型

在经典的基于 SIMP 的拓扑优化方法中（Sigmund 和 Maute, 2013），假设材料分布在每个有限单元内是均匀的，第 $i$ 个单元的杨氏模量与其密度 $\rho_i \in [0,1]$ 的关系为 $E_i = E_{\min} + \rho_i^3\left(E_0 - E_{\min}\right)$。因此，一个自然的做法是：从子结构内的随机密度分布计算多尺度形函数以生成数据集，然后训练一个从密度场到多尺度形函数的神经网络映射。值得注意的是，多尺度形函数具有一些内在性质或物理要求，这些对训练 ML 模型至关重要。

特别地，

$$\tilde{\boldsymbol{N}}^j = \begin{bmatrix} \boldsymbol{N}^j_s\boldsymbol{L} \\ \boldsymbol{L} \end{bmatrix} \triangleq \begin{bmatrix} \tilde{\boldsymbol{N}}^j_s \\ \boldsymbol{L} \end{bmatrix}$$

由于 $\boldsymbol{L}$ 是常数矩阵，只需预测 $\tilde{\boldsymbol{N}}^j_s$。排除 $\boldsymbol{L}$ 减少了预测任务，更重要的是，确保了子结构之间位移的连续性。由于在刚体运动下子结构的所有节点位移都可仅由顶点节点的位移唯一确定，因此存在如图 2 所示的三个物理约束。这些物理约束可统一写为

$$\tilde{\boldsymbol{N}}^j_s \boldsymbol{\phi}_i = \boldsymbol{b}_i, \quad i = 1, \dots, M \tag{11}$$

其中 $M$ 表示刚体运动的数目。如此，多尺度形函数矩阵中独立列的数目为 $(n_i - M)$，$\tilde{\boldsymbol{N}}^j_s$ 的前 $(n_i - M)$ 列构成一个缩减多尺度形函数 $\tilde{\boldsymbol{N}}^j_{sR}$。为使正文简洁，三维子结构物理约束的精确表达式见附录 B。

图 3 给出了二维子结构 PIML 模型的流程图。模型的输入是子结构内密度（或杨氏模量）的分布。通过 ANNs，预测出缩减多尺度形函数 $\tilde{\boldsymbol{N}}^j_{sR}$。最后，根据式 (11) 的物理要求，即可得到 $\tilde{\boldsymbol{N}}^j_s$。除了降低输出维数之外，这种处理还严格保证了多尺度形函数的物理要求。即使预测 $\tilde{\boldsymbol{N}}^j_{sR}$ 存在一些误差，所计算的 $\tilde{\boldsymbol{N}}^j_s$ 仍可视为具有特定变形假设的多尺度形函数。得到 $\tilde{\boldsymbol{N}}^j$ 后，应使用式 (9) 而非式 (4) 来获得物理上一致的缩聚刚度矩阵。

借助监督式机器学习，如 Huang 等 (2023) 所提出的，训练图 3 中的 PIML 模型时采用均方误差（MSE）作为损失函数。尽管遵循第 2 节的方程可以直接生成高质量数据集，但对于相对大规模的三维子结构，主要存在三个缺点：（1）由于 MSE 缺乏多尺度形函数背后的物理内涵，所训练 PIML 模型的泛化能力有限；（2）随着子结构尺寸增大，必须使用重型神经网络，训练更加困难；（3）随着子结构尺寸增大，需要更多训练数据，生成数据集的时间成本很高。特别地，对于由 $10\times10\times10$ 细尺度单元构成的子结构，即使在线性变形假设下，多尺度形函数中也约有 40,000 个独立分量需要预测。在先前工作（Huang 等, 2023）中，同时训练 9 个独立的 ANNs 来预测 $\tilde{\boldsymbol{N}}^j_{sR}$。此外，在我们的台式机上生成 1 个样本约需 1 s，而 Huang 等 (2023) 中通常需要 100 万个样本才能训练出一个精度合理的神经网络。可以想见，对于更大的三维子结构或采用更高阶的边界变形插值假设，输出的数量与生成数据集的时间成本将呈爆炸式增长。因此，有必要对上述基于监督学习的 PIML 模型 ANN 框架进行升级。

![[Huang2024_Fig3.png]]

<div align="center">

图 3：PIML 模型从子结构内密度（材料属性）分布预测多尺度形函数的流程图。

</div>

# 4 基于力学的无数据 PIML 模型及其在大规模结构分析与优化中的应用

为建立对任意尺寸子结构均有效的 PIML 模型，第 4.1 节在子结构内材料的分布函数与连续多尺度形函数之间建立一个轻量级算子学习框架，满足 $\boldsymbol{u}(x,y,z) = \tilde{\boldsymbol{N}}(x,y,z;\boldsymbol{\rho})\,\boldsymbol{u}_v$。随后，第 4.2 与 4.3 节基于最小总势能原理，提出一个具有物理意义的损失函数，以实现 PIML 模型的无数据无监督学习。最后，第 4.4 节借助 PIML 模型勾勒基于 SIMP 的拓扑优化的表述与灵敏度结果。

## 4.1 基于深度算子网络（DeepONet）的轻量级网络

与只能应用于具有某些特定边界条件的偏微分方程（PDEs）的传统神经网络不同，神经算子框架（DeepONet）是 Lu 等（2021）基于算子的通用逼近原理提出的一种新颖机器学习框架，专门为求解具有各种边界条件的 PDEs 而设计。遵循“算子定义了从函数到函数的映射”这一思想，在 DeepONet 中，输入与输出都是函数，而神经网络表示该算子。处理输入函数的网络称为分支网络（branch network），与输出函数对应的网络称为主干网络（trunk network）。

可以假设连续多尺度形函数等价于由图 4 所示 DeepONet 表示的一个算子，满足 $\boldsymbol{u}(x,y,z) = \tilde{\boldsymbol{N}}(x,y,z,\boldsymbol{\rho}\,|\,\boldsymbol{d})\,\boldsymbol{u}_v$。在实现中，$\boldsymbol{\rho}$ 保存子结构内每个细网格中心处的单元密度值；$\boldsymbol{d}$ 表示神经算子的参数，例如 $\boldsymbol{\xi}, \boldsymbol{\omega}, \boldsymbol{\varphi}, \boldsymbol{\theta}, \boldsymbol{\zeta}, \boldsymbol{\phi}$ 等。具体而言，$\sigma$ 表示激活函数（如 tanh、elu 等）；$\boldsymbol{\xi}, \boldsymbol{\omega}, \boldsymbol{\varphi}$ 表示权重矩阵，而 $\boldsymbol{\theta}, \boldsymbol{\zeta}, \boldsymbol{\phi}$ 是 BP（反向传播）神经元的偏置。在此 DeepONet 框架内，分支网络用于提取子结构内材料分布的特征，记为 $\boldsymbol{B}(\boldsymbol{\rho})$；相应地，主干网络负责对子结构内的坐标进行编码，记为 $\boldsymbol{T}(\boldsymbol{x})$。随后，遵循算子的通用逼近定理，将这两部分逐元素相乘，即 $\boldsymbol{T}(\boldsymbol{x}) \cdot \boldsymbol{B}(\boldsymbol{\rho})$，作为最终输出层的输入，如图 4 中虚线框所示。需要指出，$\boldsymbol{B}(\boldsymbol{\rho})$ 与 $\boldsymbol{T}(\boldsymbol{x})$ 并不限于单层 BP 神经元，它们可用其他机器学习模型表示，例如 CNN 或图神经网络。

与图 3 中先前的神经网络相比，坐标变量也被设为 DeepONet 的输入，类似于对原多尺度形函数的一种升尺度（upscaling）操作。这里不是简单地把三个坐标变量与 $m^3$ 个密度值汇集成一个输入向量，而是先用两个独立的子网络（即分支网络与主干网络）分别捕获这两类变量的内在特征，然后通过非线性运算将它们的输出组合以产生最终输出。此外，DeepONet 的输出只包含特定坐标处的多尺度形函数，与图 3 的神经网络相比，这大幅减少了输出变量的数目。为产生整个多尺度形函数 $\tilde{\boldsymbol{N}}^j_{sR}$，可以给定内部节点的坐标与子结构的密度向量，并行地使用训练好的 DeepONet。理论上，该架构可应用于任意尺寸子结构的 PIML 模型，而无需担心多尺度形函数维数过大。

![[Huang2024_Fig4.png]]

<div align="center">

图 4：预测三维子结构连续多尺度形函数的非堆叠（unstacked）DeepONet 架构。网络输出内部节点 $(x_k, y_k, z_k)$ 处的多尺度形函数。

</div>

## 4.2 基于力学的损失函数

对于只有位移边界条件的子结构，第 $j$ 个子结构的最小势能原理可表述如下：

$$\begin{aligned} \text{find} \quad & \boldsymbol{u}^j \\ \min \quad & \left(\boldsymbol{u}^j\right)^{\top}\boldsymbol{K}^j\boldsymbol{u}^j/2 \\ \text{s.t.} \quad & \boldsymbol{u}^j = \bar{\boldsymbol{u}}^j, \quad \text{on } S_u^j \end{aligned} \tag{12}$$

其中 $S_u^j$ 指第 $j$ 个子结构的位移边界。鉴于子结构的内部节点不受外力、边界节点受给定位移边界条件的假设，势能中的外力功部分消失，只剩下应变能。此外，利用本文引入的多尺度形函数，当边界位移固定时，子结构内的位移场可用这些多尺度形函数插值，即 $\boldsymbol{u}^j = \tilde{\boldsymbol{N}}^j \boldsymbol{u}^j_v$。

因此，式 (12) 可改写为以多尺度形函数为设计变量的数学优化表述：

$$\begin{aligned} \text{find} \quad & \tilde{\boldsymbol{N}}^j_s(\boldsymbol{d}) \\ \min \quad & J^j = \frac{1}{2}\left(\tilde{\boldsymbol{N}}^j\boldsymbol{u}^j_v\right)^{\mathsf{T}}\boldsymbol{K}^j\left(\tilde{\boldsymbol{N}}^j\boldsymbol{u}^j_v\right) \\ \text{s.t.} \quad & \tilde{\boldsymbol{N}}^j_s(\boldsymbol{d})\boldsymbol{\phi}_i = \boldsymbol{b}_i, \quad i=1,\dots,M \\ & \tilde{\boldsymbol{N}}^j = \begin{bmatrix} \tilde{\boldsymbol{N}}^j_s(\boldsymbol{d}) \\ \boldsymbol{L} \end{bmatrix} \end{aligned} \tag{13}$$

由于神经算子表示多尺度形函数，上述表述本质上是在优化这些神经算子的参数 $\boldsymbol{d}$（例如图 4 中的 $\boldsymbol{\xi}, \boldsymbol{\omega}, \boldsymbol{\varphi}, \boldsymbol{\theta}, \boldsymbol{\zeta}, \boldsymbol{\phi}$ 等）。如第 3 节所述，式 (13) 中的约束编码了多尺度形函数的内在物理性质，确保 $\tilde{\boldsymbol{N}}^j_s$ 能够表示子结构的刚体运动。

至关重要的是，对于任意给定的边界位移 $\boldsymbol{u}^j_v$，使式 (13) 中应变能最小的多尺度形函数恰好对应于精确的多尺度形函数。这一性质使得式 (13) 中适用于单个子结构的目标函数可推广到多个子结构的应变能。具体而言，

$$\tilde{\boldsymbol{N}}^{j*}_s = \arg\min J^j\left(\tilde{\boldsymbol{N}}^j_s\right),\ j=1,\dots,N \quad\Rightarrow\quad \tilde{\boldsymbol{N}}^{1*}_s,\dots,\tilde{\boldsymbol{N}}^{N*}_s = \arg\min \sum_{j=1}^N J^j\left(\tilde{\boldsymbol{N}}^j_s\right) \tag{14}$$

其中 arg min 表示取最小值的自变量，$\tilde{\boldsymbol{N}}^{j*}_s$ 是第 $j$ 个子结构的精确多尺度形函数。

式 (14) 促使我们引入一个由 $N$ 个子结构组成的伪结构（pseudo structure）。将式 (13) 中的目标函数设为整个伪结构的应变能，就可以在每次迭代中用这些子结构的多种密度分布来训练 DeepONet 模型。实际上，由于细尺度单元的刚度矩阵是已知的，计算整个伪结构的应变能无需组装全局刚度矩阵。DeepONet 的损失函数计算为：

$$J = \sum_{j=1}^N \left(\tilde{\boldsymbol{N}}^j\boldsymbol{u}^j_v\right)^{\top}\boldsymbol{K}^j\left(\tilde{\boldsymbol{N}}^j\boldsymbol{u}^j_v\right)/2 = \sum_{j=1}^N\sum_{e=1}^{m^3}\left(\boldsymbol{u}^j_e\right)^{\top}\boldsymbol{k}^j_e\boldsymbol{u}^j_e/2 \tag{15}$$

其中 $\boldsymbol{u}^j_e$ 与 $\boldsymbol{k}^j_e$ 分别是第 $j$ 个子结构中第 $e$ 个细尺度单元的单元位移向量与单元刚度矩阵。

![[Huang2024_Fig5.png]]

<div align="center">

图 5：连续多尺度形函数无监督学习的流程图。

</div>

## 4.3 无数据 PIML 模型的无监督学习

上一小节引入了一种新颖的基于力学机制的损失函数，以避免生成带多尺度形函数的样本。值得注意的是，为使用式 (15) 的损失函数，必须保持伪结构相邻子结构之间的位移连续性。尽管理论上，精确的多尺度形函数 $\tilde{\boldsymbol{N}}^j$ 对任意 $\bar{\boldsymbol{u}}^j_v$ 都能使损失函数取得最小值，但实践中发现，固定 $\bar{\boldsymbol{u}}^j_v$ 可能导致优化结果陷入局部极小，造成训练过程的显著波动。基于这些考虑，无监督学习框架的训练流程如图 5 所示。

**i. 伪结构的初始化。** 为同时使用一定量的密度分布来训练 DeepONet，应首先设置一个由多个子结构组成的伪结构。需要注意的是，多尺度形函数仅取决于子结构内的材料分布，而与伪结构的几何和边界位移均无关。因此，伪结构内子结构的数目不会影响训练好的模型的精度。本文以 $10\times10\times5$ 个均匀子结构（粗网格）离散伪结构作为示例，每个子结构由 $10\times10\times10$ 个细尺度单元组成。然后，保存伪结构的节点、粗/细单元的索引以及其他模型信息，供后续计算损失函数使用。

**ii. 随机密度分布与正交位移基的生成。** 为与先前的监督学习保持一致，随机生成伪结构的密度场 2000 次，共保存 100 万个子结构密度场。此外，为保证给定子结构位移场的代表性，还预先保存了共 $11\times11\times6\times3 = 2178$ 个归一化向量，作为给定位移场的完备正交基。在训练过程中，$\boldsymbol{u}_v \in \mathbb{R}^{2178\times1}$ 随每个迭代步变化。

**iii. 计算损失函数以更新 DeepONet。** 对于伪结构一对生成的密度分布与正交位移基，由 DeepONet 生成每个子结构的多尺度形函数 $\tilde{\boldsymbol{N}}^j$，然后计算伪结构中每个细网格的节点位移向量。最后，将式 (15) 的损失函数取为所有细网格单元应变能之和。随后，为使损失函数最小化，采用自动微分技术计算损失函数的灵敏度，并用 Adam 优化器相应地更新 $\boldsymbol{d}$。

**iv. 检查收敛、更新密度并给出用于进一步训练的位移场。** 为提高 DeepONet 的预测能力，若训练过程的迭代次数尚未达到阈值，则在下一次迭代中选取另一组细网格密度分布与固定的子结构位移进行训练。

以我们的经验，使用由 1000 个细网格组成的子结构的 100 万个密度分布、训练 40–50 个 epoch，DeepONet 的预测精度即可达到相当好的水平。有趣的是，如后续章节所示，所提出的无监督学习模型的精度高于监督学习训练的 PIML 模型。这主要是因为，新颖的损失函数从全局能量层面训练多尺度形函数，提高了泛化能力；而监督学习中的 MSE 只是评估预测值与精确值之间的数值差异，对多尺度形函数背后的力学机制视而不见。还发现，由于采用了新颖的损失函数，即使不采取特殊处理，所提出的无监督学习框架中也很少观察到过拟合；相比之下，在先前的监督学习模型中，必须精心设计正则化项来缓解过拟合。对于由 $10\times10\times10$ 细网格组成的子结构，在我们的台式机上训练无监督 PIML 模型约需 2–3 天。监督学习模型的训练时间与之接近，但生成训练数据集还需要多得多的时间。

## 4.4 基于 PIML 模型的大规模结构分析与拓扑优化

一旦 DeepONet 训练完成，就可用于对由相同子结构离散、具有任意位移边界与载荷条件的大规模结构进行高效线弹性分析。PIML 模型的优势使其尤其适用于大规模结构拓扑优化问题（Huang 等, 2022, 2023）。以体积约束下的最小柔顺性设计问题为例，SIMP 方法中的数学表述如下：

$$\begin{aligned} \text{find} \quad & \boldsymbol{\rho} = \left(\rho_1, \dots, \rho_{Nm^3}\right)^{\top} \\ \min \quad & f = \boldsymbol{F}^{\top}\boldsymbol{U} \\ \text{s.t.} \quad & \boldsymbol{K}_{\mathrm{ML}}(\boldsymbol{\rho})\,\boldsymbol{U} = \boldsymbol{F} \\ & g = V(\boldsymbol{\rho}) - \bar{V} \leq 0 \\ & 0 \leq \rho_i \leq 1, \quad i=1,\dots,Nm^3 \end{aligned} \tag{16}$$

其中 $N$ 与 $m^3$ 分别为整个结构中子结构的数目与每个子结构内细网格的数目，$\boldsymbol{K}_{\mathrm{ML}}(\boldsymbol{\rho})$ 是利用式 (9) 与 DeepONet 预测的多尺度形函数、组装各子结构缩聚刚度矩阵而得到的全局刚度矩阵。符号 $V$ 是实体材料的体积，其上界为 $\bar{V}$。

为消除数值不稳定性（例如棋盘格现象与网格依赖性），此处采用密度过滤（Sigmund 和 Maute, 2013）。每次迭代中，通过对设计变量过滤得到物理密度场：

$$\tilde{\rho}_e = \frac{\sum_{i\in N_e} H_{ei}\rho_i}{\sum_{i\in N_e} H_{ei}}, \quad H_{ei} = \max\left(0,\ r_{\min} - d(i,e)\right) \tag{17}$$

其中 $d(i,e)$ 表示第 $i$ 与第 $e$ 个细尺度单元中心之间的距离，$N_e$ 是满足 $d(i,e) \leq r_{\min}$、位于第 $e$ 个单元影响域内的单元索引集，$H_{ei}$ 是过滤操作中的权重因子，$r_{\min}$ 表示过滤半径。

为便于实现，灵敏度结果按全尺度分析的拓扑优化方式计算：

$$\begin{cases} \dfrac{\partial f}{\partial \rho_j} = -\sum_{e\in N_j} \dfrac{3H_{je}\tilde{\rho}_e^2}{\sum_{i\in N_e} H_{ei}}\left(E_0 - E_{\min}\right)\boldsymbol{u}_e^{\top}\boldsymbol{k}_e\boldsymbol{u}_e \\[3mm] \dfrac{\partial g}{\partial \rho_j} = \sum_{e\in N_j} \dfrac{H_{je}}{\sum_{i\in N_e} H_{ei}} \end{cases} \tag{18}$$

其中 $\boldsymbol{k}_e$ 与 $\boldsymbol{u}_e$ 是第 $e$ 个细尺度单元的单元刚度矩阵与节点位移向量。

对于第 5.3 节的柔顺机构设计算例，目标函数与相应的灵敏度结果为：

$$\begin{cases} f = \boldsymbol{l}^{\top}\boldsymbol{U} \\[3mm] \dfrac{\partial f}{\partial \rho_j} = -\sum_{e\in N_j}\dfrac{3H_{je}\tilde{\rho}_e^2}{\sum_{i\in N_e}H_{ei}}\left(E_0 - E_{\min}\right)\boldsymbol{u}_e^{\top}\boldsymbol{k}_e\boldsymbol{u}_e^{\mathrm{ad}} \end{cases} \tag{19}$$

其中 $\boldsymbol{l}$ 是标识输出位移的指示向量，节点伴随位移向量 $\boldsymbol{u}_e^{\mathrm{ad}}$ 通过求解伴随方程 $\boldsymbol{K}_{\mathrm{ML}}\boldsymbol{U}^{\mathrm{ad}} = \boldsymbol{l}$ 得到。PIML 增强拓扑优化求解过程的更多细节见 Huang 等（2022, 2023）的相关工作。

# 5 数值算例

本节研究三个示例算例，以验证无数据 PIML 模型在大规模结构分析与拓扑优化中的有效性。首先，研究一个相对小规模、通常对预测误差更敏感的悬臂梁算例，以说明无数据无监督学习模型更好的泛化能力；该算例中还讨论了子结构边界变形线性假设的影响。随后，优化一个三维扭转箱（torsion box），以探究所提出的 PIML 增强拓扑优化算法在不同过滤半径下的性能。最后，研究一个柔顺机构算例，以进一步检验 PIML 模型在大规模非自伴随结构优化问题中的有效性。基材的杨氏模量与泊松比分别为 $E_0=1$、$\nu=0.3$，$E_{\min}=10^{-7}$。在 PIML 模型中，所有算例都使用针对 $m=10$ 子结构多尺度形函数训练好的 DeepONet。在全尺度分析中，所有细尺度单元均采用八节点六面体（brick）单元建模。此外，采用优化准则（OC）法更新设计变量，当目标函数值在最后连续五次迭代中的相对变化小于 0.0002 时终止优化过程。所有算例均在配备 Intel(R) Xeon(R) Gold 6256 3.60 GHz CPU 与 512.0 GB 内存的台式机上求解。

## 5.1 悬臂梁算例

如图 6 所示，一个 $2\times1\times1$ 的悬臂梁左端固定，右下边缘受幅值 $p=1$ 的均匀向下分布载荷。它由 $20\times10\times10$ 个子结构离散，每个子结构由 $10\times10\times10$ 个细尺度网格组成。在细尺度单元中生成随机密度场分布。

为说明训练好的 DeepONet 模型的精度，图 7 分别比较了由带线性边界假设的 EMsFEM、PIML 增强分析算法与全尺度分析所得的中截面（图 6 中点划线标识）位移分布。值得注意的是，即使对于具有随机材料分布的悬臂梁，PIML 与 EMsFEM 算法所得的位移场也相当接近。相应结构柔顺性值的相对差异为 6.20%（$C_{\mathrm{EMs}}=89.46$，$C_{\mathrm{PIML}}=83.89$）。与全尺度分析结果相比，主要位移分量（即 $U_x$ 与 $U_z$）的分布相似。位移向量的相对误差为 $\lVert\boldsymbol{U}_{\mathrm{EMs}}-\boldsymbol{U}_{\mathrm{PIML}}\rVert/\lVert\boldsymbol{U}_{\mathrm{EMs}}\rVert = 6.27\%$ 与 $\lVert\boldsymbol{U}_{\mathrm{Fine}}-\boldsymbol{U}_{\mathrm{PIML}}\rVert/\lVert\boldsymbol{U}_{\mathrm{Fine}}\rVert = 6.33\%$。这充分证明了 DeepONet 与基于力学机制的 PIML 模型的有效性。

对于该悬臂梁的拓扑优化，体积分数与过滤半径分别设为 0.12 与子结构尺寸的 0.5 倍。该问题用三种结构分析策略求解：(a) EMsFEM 算法；(b) Huang 等 (2023) 中基于监督学习 PIML 模型的子结构分析；(c) 基于所提出 DeepONet 的 PIML 模型的子结构分析。相应的优化设计如图 8(a)–(c) 所示，并用不同算法重新分析这些设计的结构柔顺性值。可以发现，由于子结构边界位移的线性假设，EMsFEM 与 PIML 模型所得柔顺性值均小于全尺度分析结果 $C_{\mathrm{Fine}}$。然而，如图 8 所示，PIML 模型相比全尺度分析有约两个数量级的效率提升。

尽管基于监督学习与基于 DeepONet 的 PIML 模型的拓扑优化最终目标函数值接近（395.08 与 394.29），但图 8(c) 中基于 DeepONet 的 PIML 模型的优化设计比图 8(b) 中先前监督学习模型所得的对应设计平滑得多、性能也更好。基于 DeepONet 的 PIML 模型所得结构柔顺性与 EMsFEM 及全尺度分析结果之间的相对误差，也远小于基于监督学习 PIML 模型的相应误差。这表明无监督学习模型具有更好的泛化能力。

为说明优化结构的合理性，图 9 给出了图 8(c) 设计的应力分量 $\sigma_{xx}$、$\sigma_{xy}$、$\sigma_{xz}$ 的分布。显然，高水平应力沿主要结构构件分布，表明优化结构形成了理想的传力路径，使材料得到充分利用。此外，PIML 方法所得应力场与 EMsFEM 方法所得几乎无法区分，凸显了基于力学机制的 PIML 模型的精度。即使与全尺度分析结果相比，尽管量值上存在差异，但各方法的应力集中区域相当一致。由于识别应力集中区域对带应力约束的结构优化至关重要，所提出的算法也适用于与应力相关的拓扑优化。

尽管如此，用 $20\times10\times10$ 个子结构离散设计域时，即使对训练良好的 DeepONet，由于边界变形的线性假设，PIML 模型的结构柔顺性（$C_{\mathrm{PIML}}^{\mathrm{usp}}$）与全尺度建模结果（$C_{\mathrm{Fine}}$）之间仍存在显著差异。如表 2 所示，通过增加子结构数目可缓解该问题。图 8(d) 展示了子结构数目为 $50\times25\times25$ 时、基于 DeepONet 的 PIML 模型所得的优化悬臂梁。可以发现，无监督 PIML 模型所得柔顺性值与全尺度分析之间的相对误差降至 4.7%（$C_{\mathrm{PIML}}^{\mathrm{usp}}=321.81$，$C_{\mathrm{Fine}}=337.76$），且结构分析的求解效率提升约 87 倍，这充分证明了 PIML 模型在大规模结构分析与设计问题中的有效性。

![[Huang2024_Fig6.png]]

<div align="center">

图 6：悬臂梁算例示意图。

</div>

![[Huang2024_Fig7.png]]

<div align="center">

图 7：悬臂梁中截面处由 EMsFEM 算法、PIML 模型与全尺度分析所得位移场的等值线图。

</div>

![[Huang2024_Fig8.png]]

<div align="center">

图 8：不同算法所得的优化悬臂梁及每次迭代的平均结构分析耗时：(a) $20\times10\times10$ 子结构，EMsFEM 分析；(b) $20\times10\times10$ 子结构，监督学习 PIML 模型分析；(c) $20\times10\times10$ 子结构，无监督学习 PIML 模型分析；(d) $50\times25\times25$ 子结构，无监督学习 PIML 模型分析。

</div>

![[Huang2024_Fig9.png]]

<div align="center">

图 9：由 EMsFEM 算法、PIML 模型与全尺度分析所得图 8(c) 优化设计的三个应力分量（即 $\sigma_{xx}$、$\sigma_{xy}$、$\sigma_{xz}$）分布。

</div>

## 5.2 三维箱型算例

为检验 PIML 模型在相对复杂应力状态下的性能，并研究过滤半径对优化设计的影响，此处考虑图 10 所示的箱型算例。红色圆盘区域为非设计域，半径为 1.5、厚度为 0.15。作为示例，一对扭矩用集中载荷建模。体积分数上界设为 0.02。

根据对称性，用基于 DeepONet 的 PIML 模型、以不同参数设置优化 1/8 设计域，如图 11 所示。对于相对较少的子结构数目（即由 $24\times20\times24$ 个子结构离散），当过滤半径为子结构尺寸的 0.5 倍时，优化设计中存在棋盘格花纹，如图 11(a)。将过滤半径增大到子结构尺寸的 0.6 倍时，该问题在图 11(b) 中显著缓解。这是由于多尺度形函数的线性变形假设高估了子结构的刚度，而这一缺陷在子结构相对较粗、且设计问题体积分数较低时会更为显著。正如 Sigmund 等 (2016) 所指出的，该算例的最优设计并非图 11(b) 那样常见的 Michell 结构，而是一个闭壁壳体结构。将子结构加密为 $48\times40\times48$、采用相同过滤半径时，图 11(c) 中的优化设计与理论最优设计一致，且没有二维码状（QR）花纹。

值得注意的是，多分辨率拓扑优化同样用粗尺度网格分析结构，并用细尺度网格的密度分布描述拓扑。由于粗单元刚度矩阵是由其细尺度网格单元刚度矩阵加权求和得到的（Liu 等, 2018b；Nguyen 等, 2010），此类算法也会高估刚度，且当采用一阶有限元时，过滤半径必须始终大于子结构的尺寸。这牺牲了多分辨率拓扑优化方法对大规模问题的意义，因为结构细节被抑制了。在本文中，多尺度形函数为子结构呈现出更灵活的单元刚度矩阵。因此，即使采用线性变形假设，过滤半径也可以小于子结构的尺寸。更有趣的是，随着子结构分辨率的提高，过滤半径可以进一步减小。图 11(d) 表明，即使过滤半径减小到子结构尺寸的 0.4 倍，也能获得没有 QR 花纹的球状优化结构。

所提出 PIML 模型在结构拓扑优化中的实用性由表 3 予以证明。对于包含 1152 万个细尺度单元的设计域，使用 PIML 模型每次迭代的平均时间为 49.07 s，显著快于全尺度分析所需的 11761.28 s，这代表求解效率提升 230 倍以上[^t3-swap]。即使对于表 3 中更大规模的问题（全尺度分析超出我们台式机的内存容量），PIML 模型仍是可行的解决方案。对于包含 9216 万与 1.8 亿个单元的设计域，PIML 方法单次迭代的平均时间成本分别为 517.51 s 与 1175.86 s。

![[Huang2024_Fig10.png]]

<div align="center">

图 10：三维箱型算例的问题设置（Liu 等, 2018b）。

</div>

![[Huang2024_Fig11.png]]

<div align="center">

图 11：不同参数设置下所得的优化结构：(a) $24\times20\times24$ 子结构、$r_{\min}$ 为子结构尺寸的 0.5 倍；(b) $24\times20\times24$ 子结构、$r_{\min}$ 为子结构尺寸的 0.6 倍；(c) $48\times40\times48$ 子结构、$r_{\min}$ 为子结构尺寸的 0.5 倍；(d) $60\times50\times60$ 子结构、$r_{\min}$ 为子结构尺寸的 0.4 倍。

</div>


<div align="center">

表 3：不同细网格数目下，PIML 方法与全尺度分析单次迭代的平均时间成本。

</div>

| 细尺度单元数 | PIML 模型耗时 (s) | 全尺度分析耗时 (s) |
|---|---|---|
| $1.152\times10^{7}$ | 49.07 | 11 761.28 |
| $9.216\times10^{7}$ | 517.51 | \\ |
| $1.8\times10^{8}$ | 1175.86 | \\ |

[^t3-swap]: 原文此句为“PIML 模型每次迭代平均 11761.28 s，显著快于全尺度分析的 49.07 s”，与表 3 的数值恰好对调（表 3 显示 PIML 为 49.07 s、全尺度为 11761.28 s），且“230 倍以上”的效率提升也应为 $11761.28/49.07\approx240$。此处按表 3 的正确对应关系译出。

## 5.3 柔顺机构算例

为进一步证明无数据 PIML 模型的有效性，此处给出一个三维柔顺机构设计问题，如图 12 所示。左侧的上、下边缘固定。在位于左侧中心的输入端口施加一个推力载荷 $F_{\mathrm{in}}=1$，目标函数是使右侧输出端口 AB 缩短的距离最大化。输入/输出点处弹簧的弹性常数为 $k_{\mathrm{in}}=k_{\mathrm{out}}=0.1$。

由于对称性，仅将一半设计域用 $50\times20\times25$ 个子结构离散并优化。目标函数值与相关灵敏度按式 (19) 修改，其中 $\boldsymbol{l}$ 对应于施加在图 12 中 A、B 两点的一对单位集中载荷。固定过滤半径为子结构尺寸的 0.5 倍，用无监督学习 PIML 模型得到体积分数上界分别为 0.2、0.1、0.05 的优化设计，如图 13 所示。体积分数为 20% 的优化设计是一个 2.5D 结构，类似于著名二维柔顺机构（Sigmund 和 Maute, 2013）的拉伸体。随着最大许可体积分数减小，优化结构变得更薄，拓扑在图 13(b) 与 (c) 中变得更复杂。此外，与精确分析结果（EMsFEM 所得 $U_{\mathrm{out}}^{\mathrm{EMs}}$）相比，输出位移值（$U_{\mathrm{out}}^{\mathrm{PIML}}$）分别与之相当接近。

为说明柔顺机构的工作原理，图 14(a) 给出了优化设计图 13(a) 的前视图。施加载荷后，铰链将左侧的推力转化为右侧的回拉。如此，钳口彼此靠近，从而可以夹起某些物体，如图 14(b)。此外，图 14(c) 展示了输出端口 AB 缩短距离的稳定收敛历程。所有这些事实都证明了所提出的无数据 PIML 模型对一般非自伴随拓扑优化问题的有效性。

![[Huang2024_Fig12.png]]

<div align="center">

图 12：三维柔顺机构问题的问题设置。

</div>

![[Huang2024_Fig13.png]]

<div align="center">

图 13：不同体积分数的优化柔顺机构。

</div>

![[Huang2024_Fig14.png]]

<div align="center">

图 14：图 13(a) 优化柔顺机构的前视图：(a) 原始构型；(b) 推力载荷下的变形构型；(c) 目标函数值的迭代历程。

</div>

# 6 结论

本文提出了一种基于力学的无数据问题无关机器学习（PIML）模型，用于大规模结构分析与设计优化。基于经典子结构方法，将衡量粗自由度（DOFs）与全自由度之间关系的多尺度形函数升级为坐标的函数，然后用算子学习技术预测之。此外，提出了一种新颖的基于力学的损失函数，无需关于多尺度形函数的数据即可训练 ML 模型。所提出的无监督 PIML 模型适用于任意尺寸的子结构，以及具有任意问题设置的大规模线弹性结构分析与刚度相关的拓扑优化。相比使用全尺度分析的求解流程，求解效率可提升两个数量级以上。

然而，在立方体子结构边界的线性变形假设下，本 PIML 模型主要有三个局限：(1) 对于材料分布不连通的子结构（例如 QR 花纹），预测精度可能显著下降；(2) 对于几何复杂的结构，用规则立方体子结构离散会很困难或代价高昂；(3) 对于超大规模拓扑优化问题（例如飞机的整体设计），串行实现的 PIML 增强子结构方法仍可能耗时耗内存。

因此，本文工作可从多个方向拓展：(1) 放宽线性变形假设，采用具有更高阶变形假设的更灵活子结构，以提高 PIML 模型对中等规模结构的精度；(2) 通过将子结构的几何信息作为额外输入，训练等参（isoparametric）PIML 模型，以更好地适用于几何复杂结构的大规模拓扑优化；(3) 开发并行 PIML 模型，充分发挥子结构方法与超级计算机在超大规模结构分析与设计优化中的作用；(4) 将 PIML 增强子结构方法拓展到多物理场的大规模分析与优化问题。相关工作正在广泛研究中，将在后续报道。

# 附录 A 面力与体力同时作用下的子结构方法

在有限元方法中，体力可以转化为结构域中分布的节点外力。不失一般性，同时受面力与体力作用的子结构平衡方程可表述为：

$$\boldsymbol{K}^j\boldsymbol{u}^j = \begin{pmatrix} \boldsymbol{K}^j_{bb} & \left(\boldsymbol{K}^j_{ib}\right)^{\top} \\ \boldsymbol{K}^j_{ib} & \boldsymbol{K}^j_{ii} \end{pmatrix}\begin{pmatrix} \boldsymbol{u}^j_b \\ \boldsymbol{u}^j_i \end{pmatrix} = \begin{pmatrix} \tilde{\boldsymbol{f}}^j_b \\ \tilde{\boldsymbol{f}}^j_i \end{pmatrix} \tag{20}$$

上式可等价变换为：

$$\left(\boldsymbol{K}^j_{bb} - \left(\boldsymbol{K}^j_{ib}\right)^{\top}\left(\boldsymbol{K}^j_{ii}\right)^{-1}\boldsymbol{K}^j_{ib}\right)\boldsymbol{u}^j_b = \tilde{\boldsymbol{f}}^j_b - \left(\boldsymbol{K}^j_{ib}\right)^{\top}\left(\boldsymbol{K}^j_{ii}\right)^{-1}\tilde{\boldsymbol{f}}^j_i \tag{21}$$

显然，体力不影响子结构方法中的缩聚刚度矩阵。注意到 $\left(\boldsymbol{N}^j_s\right)^{\top} = -\left(\boldsymbol{K}^j_{ib}\right)^{\top}\left(\boldsymbol{K}^j_{ii}\right)^{-1}$ 这一事实，式 (21) 的右端可重写为 $\tilde{\boldsymbol{f}}^j_b + \left(\boldsymbol{N}^j_s\right)^{\top}\tilde{\boldsymbol{f}}^j_i$。类似地，对于受体力作用且边界采用线性变形假设的子结构，本 PIML 模型同样适用，唯一的区别在于缩聚外载荷向量应修改为 $\boldsymbol{L}^{\top}\tilde{\boldsymbol{f}}^j_b + \left(\tilde{\boldsymbol{N}}^j_s\right)^{\top}\tilde{\boldsymbol{f}}^j_i$。

# 附录 B 三维子结构物理约束的精确表达式

在由 $m^3$ 个均匀细尺度单元构成的三维子结构中，$\tilde{\boldsymbol{N}}^j_s$ 可表示为

$$\tilde{\boldsymbol{N}}^j_s = \begin{bmatrix} \left(N^j_s\right)^{11}_{xx} & \left(N^j_s\right)^{11}_{xy} & \left(N^j_s\right)^{11}_{xz} & \cdots & \left(N^j_s\right)^{18}_{xx} & \left(N^j_s\right)^{18}_{xy} & \left(N^j_s\right)^{18}_{xz} \\ \left(N^j_s\right)^{11}_{yx} & \left(N^j_s\right)^{11}_{yy} & \left(N^j_s\right)^{11}_{yz} & \cdots & \left(N^j_s\right)^{18}_{yx} & \left(N^j_s\right)^{18}_{yy} & \left(N^j_s\right)^{18}_{yz} \\ \left(N^j_s\right)^{11}_{zx} & \left(N^j_s\right)^{11}_{zy} & \left(N^j_s\right)^{11}_{zz} & \cdots & \left(N^j_s\right)^{18}_{zx} & \left(N^j_s\right)^{18}_{zy} & \left(N^j_s\right)^{18}_{zz} \\ \vdots & \vdots & \vdots & \ddots & \vdots & \vdots & \vdots \\ \left(N^j_s\right)^{(m-1)^3\,1}_{xx} & \left(N^j_s\right)^{(m-1)^3\,1}_{xy} & \left(N^j_s\right)^{(m-1)^3\,1}_{xz} & \cdots & \left(N^j_s\right)^{(m-1)^3\,8}_{xx} & \left(N^j_s\right)^{(m-1)^3\,8}_{xy} & \left(N^j_s\right)^{(m-1)^3\,8}_{xz} \\ \left(N^j_s\right)^{(m-1)^3\,1}_{yx} & \left(N^j_s\right)^{(m-1)^3\,1}_{yy} & \left(N^j_s\right)^{(m-1)^3\,1}_{yz} & \cdots & \left(N^j_s\right)^{(m-1)^3\,8}_{yx} & \left(N^j_s\right)^{(m-1)^3\,8}_{yy} & \left(N^j_s\right)^{(m-1)^3\,8}_{yz} \\ \left(N^j_s\right)^{(m-1)^3\,1}_{zx} & \left(N^j_s\right)^{(m-1)^3\,1}_{zy} & \left(N^j_s\right)^{(m-1)^3\,1}_{zz} & \cdots & \left(N^j_s\right)^{(m-1)^3\,8}_{zx} & \left(N^j_s\right)^{(m-1)^3\,8}_{zy} & \left(N^j_s\right)^{(m-1)^3\,8}_{zz} \end{bmatrix} \tag{22}$$

其中 $\left(N^j_s\right)^{kl}_{pq}$ 表示第 $j$ 个子结构中，由第 $l$ 个顶点节点沿 $q$ 方向的单位位移所引起的第 $k$ 个内部节点沿 $p$ 方向的位移。

对应于六个刚体运动，六组方程（即 $\tilde{\boldsymbol{N}}^j_s\boldsymbol{\phi}_i = \boldsymbol{b}_i,\ i=1,\dots,6$）意味着：对 PIML 模型而言，$\tilde{\boldsymbol{N}}^j_s$ 的前 18 列可归拢为 $\tilde{\boldsymbol{N}}^j_{sR}$。在预测出 $\tilde{\boldsymbol{N}}^j_{sR}$ 之后，完整的 $\tilde{\boldsymbol{N}}^j_s$ 可根据六个物理要求（式 11）、利用以下表达式复现：

$$\begin{cases} \boldsymbol{\phi}_1 = \boldsymbol{b}_1 = (1,0,0,\dots,1,0,0)^{\top} \\ \boldsymbol{\phi}_2 = \boldsymbol{b}_2 = (0,1,0,\dots,0,1,0)^{\top} \\ \boldsymbol{\phi}_3 = \boldsymbol{b}_3 = (0,0,1,\dots,0,0,1)^{\top} \\ \boldsymbol{\phi}_k = \boldsymbol{R}^k_v\boldsymbol{x}_v,\quad \boldsymbol{b}_k = \boldsymbol{R}^k_i\boldsymbol{x}_i,\quad k=4,5,6 \end{cases} \tag{23}$$

其中 $\boldsymbol{x}_v$ 与 $\boldsymbol{x}_i$ 是顶点节点与内部节点的坐标向量。转动矩阵为对角块矩阵，可表示为

$$\boldsymbol{R}^k_v = \begin{bmatrix} \boldsymbol{R}^k_1 & \cdots & \boldsymbol{0} \\ \vdots & \ddots & \vdots \\ \boldsymbol{0} & \cdots & \boldsymbol{R}^k_8 \end{bmatrix}, \qquad \boldsymbol{R}^k_i = \begin{bmatrix} \boldsymbol{R}^k_1 & \cdots & \boldsymbol{0} \\ \vdots & \ddots & \vdots \\ \boldsymbol{0} & \cdots & \boldsymbol{R}^k_{(m-1)^3} \end{bmatrix} \tag{24}$$

其中

$$\boldsymbol{R}^4_1 = \cdots = \boldsymbol{R}^4_{(m-1)^3} = \begin{bmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 0 \end{bmatrix},\quad \boldsymbol{R}^5_1 = \cdots = \boldsymbol{R}^5_{(m-1)^3} = \begin{bmatrix} 0 & 0 & -1 \\ 0 & 0 & 0 \\ 1 & 0 & 0 \end{bmatrix},\quad \boldsymbol{R}^6_1 = \cdots = \boldsymbol{R}^6_{(m-1)^3} = \begin{bmatrix} 0 & 0 & 0 \\ 0 & 0 & -1 \\ 0 & 1 & 0 \end{bmatrix} \tag{25}$$

# 译后检查清单

- [x] 完整作者列表已核对。
- [x] 原文章节标题已按 PDF 原文同步。
- [x] 正文（摘要—结论）与附录 A/B 全文译毕。
- [x] 所有公式编号（式 1–25）与原文一致，`$$`/数学环境成对闭合（全局 Lint 通过）。
- [x] 表 1–3 已排为 Markdown 表格。
- [x] 图 1–14 已从 PDF 无损抽取并放入 `topology-opt/assets/Huang2024_FigX.png`，正文用 `![[Huang2024_FigX.png]]` 嵌入，图注紧随其下。
- [x] 已对照 PDF 原页复核重构公式：式 (10) 映射记号更正为 $\mathcal{F}$、式 (13) 目标函数更正为 $J^j$；式 (22) 大矩阵、式 (23)–(25) 转动矩阵、附录 A 式 (20)/(21) 均确认无误。
- [x] 与 [[../Huang2022-problemindependentmachine]]、[[../Huang2023-PIML-substructure]]、[[../Ma2026-highperformanceparallel]] 的关系已在笔记 [[../Huang2024-PIML-datafree]] 中同步（关系表「本文」行、核心思路、学习对象、损失、实验、结论均已按全文精读补全）。
