---
title: "翻译：Problem-independent machine learning-enhanced structural topology optimization of complex design domains based on isoparametric elements"
tags:
  - translation
  - PIML
  - topology-opt
  - substructure
  - isoparametric
status: "done"
date_created: 2026-08-04
date_updated: 2026-09-10
source: "../sources/Zhang2024-isoparametric-PIML.pdf"
citekey: "zhangProblemindependentMachineLearningenhanced2024a"
language: "zh-CN"
---

# Problem-independent machine learning-enhanced structural topology optimization of complex design domains based on isoparametric elements

---

# 信息

- **中文标题**：基于等参单元的问题无关机器学习增强复杂设计域结构拓扑优化
- **作者**：Linfeng Zhang（张林峰）；Mengcheng Huang（黄孟成）；Chang Liu（刘畅）；Zongliang Du（杜宗亮）；Tianchen Cui（崔天晨）$^*$；Xu Guo（郭旭）$^*$
- **单位**：大连理工大学工程力学系、工业装备结构分析优化与 CAE 软件国家重点实验室（State Key Laboratory of Structural Analysis, Optimization and CAE Software for Industrial Equipment, Department of Engineering Mechanics, Dalian University of Technology, Dalian 116023, PR China）
- **期刊**：*Extreme Mechanics Letters*
- **卷 / 期 / 文章号**：72: 102237
- **DOI**：10.1016/j.eml.2024.102237
- **收稿 / 修回 / 录用 / 在线发表**：2024-06-11 / 2024-09-14 / 2024-09-19 / 2024-09-20
- **通讯作者**：Tianchen Cui（cuitianchen@dlut.edu.cn）；Xu Guo（guoxu@dlut.edu.cn）

# 摘要

拓扑优化通常需要进行数十次乃至数百次迭代，而每次迭代都需要完成一次完整的有限元分析（FEA）。显著的计算开销限制了拓扑优化在工程中的应用，尤其限制了包含复杂设计域的高分辨率问题。针对这一问题，本文提出一种基于等参单元的问题无关机器学习（PIML）模型。该模型能够有效降低有限元分析的计算时间，从而实现高效拓扑优化，并将可求解问题的范围扩展至复杂设计域。

其核心思想是利用子结构方法，通过机器学习模型建立子结构内部单元几何形状和材料分布到其数值形函数之间的映射。样本生成与模型训练均在线下完成，因此训练后的机器学习模型可以直接用于拓扑优化过程。由于子结构的形函数具有问题无关性，当优化问题的几何形状或边界条件发生变化时，无需重新生成样本或修改所提出的机器学习模型。数值算例表明，在不采用并行计算技术的情况下，所提出的机器学习模型可将拓扑优化效率提高一个数量级。

**关键词**：机器学习（Machine learning）；拓扑优化（Topology optimization）；子结构（Substructure）；等参单元（Isoparametric elements）

---

# 1 引言

结构拓扑优化旨在预定的设计域内合理分配给定数量的可用材料以实现结构性能最优，现已成为工程结构设计不可或缺的工具。学者们提出了诸多高效的拓扑优化方法 [1–9]，部分经典方法已被集成到商业软件中用以指导工程结构设计。然而，结构拓扑优化往往需要数十至数百次迭代，每次迭代都需要完整的结构响应分析，导致极大的计算开销，尤其是对于复杂设计域中的高分辨率拓扑优化问题。为此，研究人员从不同视角开发了多种拓扑优化加速算法，包括并行计算 [10–14]、多尺度方法 [15–22]、多分辨率方法 [23–29]、自由度缩减技术 [30] 以及近似重分析方法 [31]，均在不同程度上提升了计算效率。

近年来，随着人工智能技术的快速发展，结合拓扑优化与机器学习以加速拓扑优化进程的研究吸引了广泛关注。一类被称为“端到端（end-to-end）”的机器学习拓扑优化方法试图直接建立给定优化参数（如设计域、边界条件、外载荷位置与大小）与最终优化结构之间的映射关系。例如，将结构拓扑视为图像，卷积神经网络首先被用于构建拓扑优化代理模型 [32]，以密度分布及最近一次密度更新量作为神经网络输入，输出最优结构拓扑。该方法仅需传统拓扑优化迭代的少数步即可建立从迭代中间结果到最终结构的映射，从而缩短拓扑优化时间。Kallioras 等 [33] 利用深度置信网络构建机器学习模型，将前 36 次拓扑优化迭代得到的密度场作为输入，输出最优结构密度场，在微调输出结果后，部分算例所需的迭代步数减少了 80% 以上。Bielecki 等 [34] 结合前馈神经网络与卷积神经网络构建了三阶段机器学习模型：第一阶段以前馈网络输入材料属性、优化参数和边界条件并输出最优拓扑；第二阶段用卷积神经网络预测更高分辨率结构；第三阶段通过少量传统优化迭代验证收敛性。此后，Yu 等 [35] 提出一种非迭代拓扑优化方法，引入结合卷积神经网络与条件生成对抗网络（cGAN）的两阶段模型，先在低分辨率数据集上训练，再由 cGAN 直接生成高分辨率最优拓扑而无需任何拓扑优化迭代。Patel 等 [36] 提出了三阶段神经网络辅助拓扑优化框架，在宏观尺度进行若干次传统拓扑优化迭代后，利用神经网络获得高分辨率拓扑，并通过卷积网络改善结构连通性。基于移动可变形组件（MMC）拓扑优化方法，Lei 等 [37] 将最优结构近似为一系列特征值的线性组合，利用支持向量回归（SVR）和 K 近邻（KNN）算法实现数据驱动模型的非线性回归，实现了实时拓扑优化。尽管“端到端”机器学习拓扑优化方法可实现接近实时的优化，但仍存在诸多局限：首先，其有效性严重依赖预设的优化参数（设计域、边界条件、外载荷位置/大小），一旦参数变动，就必须重新生成样本并重新训练模型；其次，优化结果取决于样本分辨率，不同分辨率问题需匹配相应数据集，高分辨率下的训练成本极其高昂；最后，此类模型的泛化能力仍需进一步探索 [38]。

除“端到端”方法外，利用机器学习模型加速或替代拓扑优化中的某些子步骤成为新的研究热点。Keshavarzzadeh 等 [39] 通过人工神经网络建立低分辨率迭代结果与低秩逼近插值系数之间的映射关系，进而获得高分辨率位移场以降低计算成本。Tan 等 [40] 提出了自适应可扩展深度学习方法 MapNet，将粗尺度应变能场和细尺度密度场作为输入，通过加速有限元分析实现大规模拓扑优化。Chi 等 [41] 提出了一种通用机器学习拓扑优化框架，在拓扑优化早期迭代中在线训练机器学习模型，在不牺牲精度的前提下显著加速大规模问题。随后，Senhora 等 [42] 通过将训练好的模型与拓扑优化过程解耦，发展了离线训练技术，获得了显著加速比。Luo 等 [43] 引入了兼顾像素误差与物理约束的损失函数，将预测结构柔度与实际结构柔度的误差作为物理约束项。Lu 等 [44] 使用偏微分方程定义的损失函数约束神经网络，在光学全息与 Stokes 流体等反问题中展示了基于 PDE 硬约束的有效性。Xia 等 [45] 针对基于多分辨率 SIMP 的等几何拓扑优化构建了在线生成与更新数据集的机器学习模型，以粗单元柔度、控制点密度和单元密度为输入，输出细单元灵敏度。此外，Deng 等 [46] 提出了替代有限元分析的在线训练机器学习模型，在柔度最小化、流固耦合、强化传热与桁架优化等问题中实现了实时响应分析。Li 等 [47] 基于卷积神经网络，将传统迭代得到的粗尺度优化密度场输入网络预测细尺度密度场，实现粗到细模型的映射以加速优化过程。上述研究取得了显著进展，但仍有关键问题亟待解决：首先，机器学习的概率近似正确（PAC）特性无法保证优化结果的安全可信；其次，对于在线训练模型，样本数量有限容易制约复杂设计域高分辨率问题的模型精度；对于离线模型，对预设优化参数的依赖表明其泛化性与可移植性仍需进一步提升。

为解决上述问题，Huang 等 [48, 49] 提出了**问题无关机器学习（Problem-Independent Machine Learning, PIML）**技术。其核心理念是引入子结构方法进行结构响应分析，通过神经网络建立子结构内部材料分布到其数值形函数之间的隐式映射，进而显著提升有限元分析与拓扑优化的效率。该方法具有多重优势：第一，子结构内部材料分布与其数值形函数之间在理论上存在唯一确定映射，保证了机器学习模型的确定性精度；第二，模型输出的子结构数值形函数独立于宏观设计域、载荷和边界条件，因而适用于同类控制方程的任意边界值问题；第三，样本生成过程简单直接，在个人计算机上即可轻松生成数十万量级的样本集；第四，借助 PIML 技术，拓扑优化中的有限元分析效率可提升数个数量级。然而，原有的 PIML 方法 [48, 49] 采用规则四边形（六面体）网格离散设计域；而实际工程中的复杂结构往往需要使用更灵活的**等参单元**进行分析与设计。因此，若能将 PIML 方法推广至等参单元，将极大拓展原始 PIML 方法的工程适用范围。

鉴于此，本文提出了一种基于等参单元的 PIML 模型，并将其应用于复杂设计域的高分辨率拓扑优化问题。该方法利用神经网络建立等参子结构内部单元几何形状与材料分布到其数值形函数的隐式映射；通过在机器学习模型中嵌入基于力学原理的物理约束，保证了等参子结构缩聚刚度矩阵的秩性质。在继承原始 PIML 模型优势的同时，该方法将 PIML 增强拓扑优化成功推向复杂几何设计域。

本文其余部分安排如下：第 2 节介绍基于等参单元的子结构方法，并从力学原理性质推导子结构形函数的不变性；第 3 节提出基于等参单元的 PIML 模型，阐述网络架构、训练流程与样本生成；第 4 节给出拓扑优化数学列式；第 5 节通过若干数值算例验证计算效率与通用性；第 6 节给出结论。

---

# 2 面向 PIML 的等参单元子结构方法

对于高分辨率拓扑优化问题，减少有限元方程中的自由度数量有助于加快分析与优化进程。子结构方法通过压缩内部自由度实现有限元方程的降维。然而，在原始 PIML 方法 [48, 49] 中，结构被离散为规则单元，并采用规则四边形（六面体）子结构作为样本。虽然样本生成过程简单，但难以准确刻画复杂设计域的边界几何特征。如图 1(a) 所示，当使用规则单元离散不规则设计域时，有限元模型与实际几何模型之间存在显著几何失真；为保证有限元分析精度，必须在边界附近细化网格。而如图 1(b) 所示，采用等参单元离散设计域，可以在单元数量相同的情况下更精确地拟合几何边界，既避免了计算开销激增，又提升了分析精度。在优化迭代过程中，各子结构内部细网格单元的密度持续更新，需要反复重新计算子结构形函数，该过程涉及耗时的矩阵求逆。因此，引入机器学习技术建立子结构几何信息及材料分布到其形函数的映射，能够大幅提升复杂域高分辨率结构分析与拓扑优化的效率。

![[Zhang2024_Fig1.png]]

<center><b>
图 1：采用相同数量的不同类型单元离散设计域。(a) 规则单元；(b) 等参单元。
</b></center>

## 2.1 基于等参单元的子结构方法

本节介绍基于等参单元的子结构方法。以图 2(a) 所示的二维复杂结构为例，将结构离散为等参单元后，可导出有限元平衡方程：

$$
\mathbf{K} \boldsymbol{u} = \boldsymbol{f},
\tag{1}
$$

其中 $\mathbf{K}$ 为结构总刚度矩阵，$\boldsymbol{u}$ 为位移向量，$\boldsymbol{f}$ 为载荷向量。若方程自由度数为 $n$，求解有限元方程的计算复杂度通常为 $\mathcal{O}(n^2) \sim \mathcal{O}(n^3)$。对于高分辨率问题，线性代数方程组的求解规模巨大，计算时间往往难以承受。为此，引入子结构方法，按指定分辨率将细网格划分为若干子结构以缩减方程维数。如图 2(b) 所示，每个红色四边形代表一个子结构。

![[Zhang2024_Fig2.png]]

<center><b>
图 2：(a) 设计域的细网格；(b) 设计域划分为子结构。
</b></center>

考虑图 3 所示的单个子结构，根据节点在子结构内部的位置，节点被划分为边界节点（红色圆圈）与内部节点（蓝色圆圈）。子结构的静力平衡方程为：

$$
\mathbf{K}^i \boldsymbol{u}^i =
\begin{bmatrix}
\mathbf{K}_{11}^i & \mathbf{K}_{12}^i \\
\mathbf{K}_{21}^i & \mathbf{K}_{22}^i
\end{bmatrix}
\begin{bmatrix}
\boldsymbol{u}_1^i \\
\boldsymbol{u}_2^i
\end{bmatrix}
=
\begin{bmatrix}
\boldsymbol{f}_1^i \\
\boldsymbol{f}_2^i
\end{bmatrix}
= \boldsymbol{f}^i,
\tag{2}
$$

其中子结构刚度矩阵 $\mathbf{K}^i$ 被划分为四个分块矩阵：$\mathbf{K}_{11}^i$、$\mathbf{K}_{12}^i$、$\mathbf{K}_{21}^i$ 和 $\mathbf{K}_{22}^i$。细网格节点位移向量 $\boldsymbol{u}^i$ 分为两部分：$\boldsymbol{u}_1^i$ 表示子结构边界节点位移，$\boldsymbol{u}_2^i$ 表示子结构内部节点位移。施加在子结构上的外载荷为 $\boldsymbol{f}^i$，同样分为边界载荷 $\boldsymbol{f}_1^i$ 和内部载荷 $\boldsymbol{f}_2^i$。注意，内部节点外力 $\boldsymbol{f}_2^i = \boldsymbol{0}$。

![[Zhang2024_Fig3.png]]

<center><b>
图 3：包含内部细单元的第 $i$ 个子结构。
</b></center>

由式 (2) 的第二行可得子结构的缩聚平衡方程：

$$
\mathbf{K}_s^i \boldsymbol{u}_1^i = \boldsymbol{f}_1^i,
\tag{3}
$$

$$
\mathbf{K}_s^i \triangleq \mathbf{K}_{11}^i - \mathbf{K}_{12}^i (\mathbf{K}_{22}^i)^{-1} \mathbf{K}_{21}^i,
\tag{4}
$$

其中 $\mathbf{K}_s^i$ 为子结构静力缩聚刚度矩阵（Schur 补）。显而易见，式 (3) 的维度远小于式 (1)。求解式 (3) 得到边界位移 $\boldsymbol{u}_1^i$ 后，子结构内部细网格节点的位移可由下式求出：

$$
\boldsymbol{u}_2^i = -(\mathbf{K}_{22}^i)^{-1} \mathbf{K}_{21}^i \boldsymbol{u}_1^i,
\tag{5}
$$

$$
\mathbf{N}^i \triangleq -(\mathbf{K}_{22}^i)^{-1} \mathbf{K}_{21}^i,
\tag{6}
$$

其中子结构数值形函数记为 $\mathbf{N}^i \in \mathbb{R}^{2N_0 \times 2N_1}$，$N_0$ 和 $N_1$ 分别表示子结构的内部细节点数与边界细节点数。由于式 (6) 涉及矩阵求逆，计算耗时较大，限制了速度优势。因此，本研究利用神经网络建立等参子结构内部单元形状及材料分布到其数值形函数的隐式映射；同时引入线性边界条件假定以简化训练过程。

## 2.2 线性边界条件假定

保证机器学习模型预测精度的关键之一是尽可能减少输出神经元数量。为减少输出神经元并降低训练难度，本文引入线性边界条件假定 [48]。据此，子结构边界细节点位移 $\boldsymbol{u}_1^i$（图 4 中绿色圆圈所示）沿子结构边界呈线性变化：

$$
\boldsymbol{u}_1^i = \mathbf{B} \tilde{\boldsymbol{u}}^i,
\tag{7}
$$

其中 $\mathbf{B}$ 表示双线性插值矩阵，$\tilde{\boldsymbol{u}}^i$ 表示粗网格节点位移，$\boldsymbol{u}_1^i$ 表示子结构边界上的细网格节点位移。

![[Zhang2024_Fig4.png]]

<center><b>
图 4：考虑线性边界假定的 $5 \times 5$ 分辨率子结构。
</b></center>

将式 (7) 代入式 (5)，可得：

$$
\boldsymbol{u}_2^i = \mathbf{N}_2^i \tilde{\boldsymbol{u}}^i,
\tag{8}
$$

$$
\mathbf{N}_2^i \triangleq -(\mathbf{K}_{22}^i)^{-1} \mathbf{K}_{21}^i \mathbf{B},
\tag{9}
$$

其中 $\mathbf{N}_2^i \in \mathbb{R}^{2N_0 \times 8}$ 表示与内部节点相关的子结构数值形函数。由此建立了细网格位移 $\boldsymbol{u}^i$ 与粗节点位移 $\tilde{\boldsymbol{u}}^i$ 之间的映射关系：

$$
\boldsymbol{u}^i = \mathbf{N}^i \tilde{\boldsymbol{u}}^i,
\tag{10}
$$

$$
\mathbf{N}^i \triangleq
\begin{bmatrix}
\mathbf{B} \\
\mathbf{N}_2^i
\end{bmatrix}.
\tag{11}
$$

与式 (6) 不同，在线性边界假定下，子结构数值形函数 $\mathbf{N}^i$ 具有式 (11) 所示的新定义。需要说明的是，结构材料分布变化会导致子结构刚度矩阵 $\mathbf{K}^i$ 改变，进而引起数值形函数 $\mathbf{N}_2^i$ 的改变。因此，在每个优化迭代步中均需重新计算 $\mathbf{N}_2^i$。

将式 (10) 代入式 (2)，并在两端同时左乘 $(\mathbf{N}^i)^{\mathsf T}$，可得：

$$
(\mathbf{N}^i)^{\mathsf T} \mathbf{K}^i \mathbf{N}^i \tilde{\boldsymbol{u}}^i = (\mathbf{N}^i)^{\mathsf T} \boldsymbol{f}^i.
\tag{12}
$$

定义线性假定下的子结构缩聚刚度矩阵为：

$$
\tilde{\mathbf{K}}^i \triangleq (\mathbf{N}^i)^{\mathsf T} \mathbf{K}^i \mathbf{N}^i.
\tag{13}
$$

组装所有子结构的缩聚刚度矩阵，可得子结构方法的整体平衡方程：

$$
\tilde{\mathbf{K}} \tilde{\boldsymbol{u}} = \tilde{\boldsymbol{f}},
\tag{14}
$$

$$
\tilde{\mathbf{K}} = \sum_{i=1}^{n_s} \tilde{\mathbf{K}}^i,
\tag{15}
$$

其中 $\tilde{\mathbf{K}}$ 为组装所有子结构缩聚刚度矩阵 $\tilde{\mathbf{K}}^i$ 得到的总体刚度矩阵，$n_s$ 为设计域内的子结构总数，$\tilde{\boldsymbol{u}}$ 和 $\tilde{\boldsymbol{f}}$ 分别表示子结构的粗网格位移向量与载荷向量。

通过引入线性边界条件假定，神经网络的输出神经元尺寸被显著压缩。在此基础上，进一步结合基于力学原理的物理约束，不仅能减少待预测的神经元数量，更能保证神经网络的预测精度。

## 2.3 子结构形函数的不变性

由式 (13) 得到的刚度矩阵是半正定的，其零特征值表明在刚体位移（平移与旋转）下结构不产生应变能。所提出的方法引入基于力学的物理约束，确保机器学习模型的输出自然满足刚体位移模式，从而提升神经网络的预测精度。

在微小变形假设下，根据刚体位移场的性质可导出子结构形函数的不变性。推导如下：

设弹性体上某点在力作用下沿 $x$ 轴和 $y$ 轴产生大小分别为 $u$ 和 $v$ 的位移。弹性体的几何方程为：

$$
\begin{cases}
\varepsilon_x = \dfrac{\partial u}{\partial x}, \\[2mm]
\varepsilon_y = \dfrac{\partial v}{\partial y}, \\[2mm]
\gamma_{xy} = \dfrac{\partial v}{\partial x} + \dfrac{\partial u}{\partial y},
\end{cases}
\tag{16}
$$

其中 $\varepsilon_x$、$\varepsilon_y$ 和 $\gamma_{xy}$ 为弹性体内该点的应变分量。令所有应变分量恒等于零：

$$
\varepsilon_x = \varepsilon_y = \gamma_{xy} = 0,
\tag{17}
$$

则有：

$$
\frac{\partial u}{\partial x} = 0, \quad \frac{\partial v}{\partial y} = 0, \quad \frac{\partial v}{\partial x} + \frac{\partial u}{\partial y} = 0.
\tag{18}
$$

对式 (18) 的前两项积分，位移可表示为：

$$
u = f_1(y), \quad v = f_2(x).
\tag{19}
$$

将式 (19) 代入式 (18) 的第三项，得：

$$
-\frac{\mathrm{d}f_1(y)}{\mathrm{d}y} = \frac{\mathrm{d}f_2(x)}{\mathrm{d}x}.
\tag{20}
$$

由于式 (20) 左端仅为 $y$ 的函数，右端仅为 $x$ 的函数，两端必等于常数。令其为 $c_0$，则有：

$$
\frac{\mathrm{d}f_1(y)}{\mathrm{d}y} = -c_0, \quad \frac{\mathrm{d}f_2(x)}{\mathrm{d}x} = c_0.
\tag{21}
$$

对式 (21) 积分并代回式 (19)，得到：

$$
u = u_0 - c_0 y, \quad v = v_0 + c_0 x.
\tag{22}
$$

式 (22) 表示平面刚体位移场。其中 $u_0$ 表示沿 $x$ 轴的平移分量，$v_0$ 表示沿 $y$ 轴的平移分量，$c_0$ 表示弹性体的微小旋转角。在刚体位移过程中，结构应变能恒为零：

$$
\mathbf{K}^i \boldsymbol{\phi}^i = \mathbf{0}, \quad \tilde{\mathbf{K}}^i \tilde{\boldsymbol{\phi}}^i = \mathbf{0}.
\tag{23}
$$

式 (23) 表明刚度矩阵存在秩亏。将式 (13) 代入式 (23) 的第二式，并在第一式两端左乘 $(\mathbf{N}^i)^{\mathsf T}$，得：

$$
(\mathbf{N}^i)^{\mathsf T} \mathbf{K}^i \boldsymbol{\phi}^i = \mathbf{0}, \quad (\mathbf{N}^i)^{\mathsf T} \mathbf{K}^i \mathbf{N}^i \tilde{\boldsymbol{\phi}}^i = \mathbf{0}.
\tag{24}
$$

由此可知，子结构数值形函数 $\mathbf{N}^i$ 具有平移与旋转不变性，即满足：

$$
\mathbf{N}^i \tilde{\boldsymbol{\phi}}^i = \boldsymbol{\phi}^i,
\tag{25}
$$

$$
\tilde{\boldsymbol{\phi}}^i =
\begin{bmatrix}
\tilde{\boldsymbol{\phi}}_t^i & \tilde{\boldsymbol{\phi}}_r^i
\end{bmatrix}, \quad
\boldsymbol{\phi}^i =
\begin{bmatrix}
\boldsymbol{\phi}_t^i & \boldsymbol{\phi}_r^i
\end{bmatrix},
\tag{26}
$$

其中 $\tilde{\boldsymbol{\phi}}^i$ 和 $\boldsymbol{\phi}^i$ 分别表示粗尺度与细尺度的位移模态。$\tilde{\boldsymbol{\phi}}_t^i$ 和 $\boldsymbol{\phi}_t^i$ 代表平移模态，$\tilde{\boldsymbol{\phi}}_r^i$ 和 $\boldsymbol{\phi}_r^i$ 代表旋转模态。

### 2.3.1 平移不变性

假设子结构按式 (22) 沿 $x$ 轴和 $y$ 轴发生刚体平移，$u_0$ 和 $v_0$ 为平移量。令 $c_0 = 0$，有：

$$
\tilde{\boldsymbol{\phi}}_t^i = \mathbf{J}_{4,1} \otimes \mathbf{X}_0, \quad \boldsymbol{\phi}_t^i = \mathbf{J}_{N,1} \otimes \mathbf{X}_0, \quad \mathbf{X}_0 =
\begin{bmatrix}
u_0 & 0 \\
0 & v_0
\end{bmatrix},
\tag{27}
$$

其中 $\mathbf{J}_{m,n}$ 表示元素全为 1 的 $m \times n$ 矩阵，$N$ 为单个子结构内的细节点总数，$\mathbf{X}_0$ 为位移矩阵，$\otimes$ 表示 Kronecker 积。

将式 (27) 代入式 (25)，可导出子结构数值形函数的平移不变性表达式：

$$
\mathbf{N}^i (\mathbf{J}_{4,1} \otimes \mathbf{X}_0) = \mathbf{J}_{N,1} \otimes \mathbf{X}_0,
\tag{28}
$$

其中子结构数值形函数 $\mathbf{N}^i$ 可展开为：

$$
\mathbf{N}^i =
\begin{bmatrix}
N_{1xx}^{i1} & N_{1xy}^{i1} & N_{2xx}^{i1} & N_{2xy}^{i1} & N_{3xx}^{i1} & N_{3xy}^{i1} & N_{4xx}^{i1} & N_{4xy}^{i1} \\
N_{1yx}^{i1} & N_{1yy}^{i1} & N_{2yx}^{i1} & N_{2yy}^{i1} & N_{3yx}^{i1} & N_{3yy}^{i1} & N_{4yx}^{i1} & N_{4yy}^{i1} \\
N_{1xx}^{i2} & N_{1xy}^{i2} & N_{2xx}^{i2} & N_{2xy}^{i2} & N_{3xx}^{i2} & N_{3xy}^{i2} & N_{4xx}^{i2} & N_{4xy}^{i2} \\
N_{1yx}^{i2} & N_{1yy}^{i2} & N_{2yx}^{i2} & N_{2yy}^{i2} & N_{3yx}^{i2} & N_{3yy}^{i2} & N_{4yx}^{i2} & N_{4yy}^{i2} \\
\vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots \\
N_{1xx}^{iN} & N_{1xy}^{iN} & N_{2xx}^{iN} & N_{2xy}^{iN} & N_{3xx}^{iN} & N_{3xy}^{iN} & N_{4xx}^{iN} & N_{4xy}^{iN} \\
N_{1yx}^{iN} & N_{1yy}^{iN} & N_{2yx}^{iN} & N_{2yy}^{iN} & N_{3yx}^{iN} & N_{3yy}^{iN} & N_{4yx}^{iN} & N_{4yy}^{iN}
\end{bmatrix},
\tag{29}
$$

其中 $N_{jxy}^{il}$ 表示粗节点 $j$ 沿 $y$ 轴产生单位位移时在细节点 $l$ 处引起的沿 $x$ 轴的位移响应。将式 (29) 代入式 (28)，易得形函数平移不变性的标量展开式：

$$
\sum_{j=1}^M N_{jxx}^{il} = 1, \quad \sum_{j=1}^M N_{jxy}^{il} = 0, \quad \sum_{j=1}^M N_{jyx}^{il} = 0, \quad \sum_{j=1}^M N_{jyy}^{il} = 1, \quad (j = 1, \dots, M; \; l = 1, \dots, N),
\tag{30}
$$

其中 $M$ 表示子结构的粗节点数。由于本文采用二维四节点等参单元，故 $M = 4$。

### 2.3.2 旋转不变性

假设子结构按式 (22) 发生微小旋转，此时令 $u_0 = v_0 = 0$。旋转模态可表示为：

$$
\tilde{\boldsymbol{\phi}}_r^i = (\mathbf{I}_4 \otimes \boldsymbol{\omega}) \tilde{\boldsymbol{x}}^i, \quad \boldsymbol{\phi}_r^i = (\mathbf{I}_N \otimes \boldsymbol{\omega}) \boldsymbol{x}^i,
\tag{31}
$$

$$
\boldsymbol{\omega} =
\begin{bmatrix}
0 & -c_0 \\
c_0 & 0
\end{bmatrix}, \quad
\boldsymbol{x}^i = \left[ x_1^i, y_1^i, \dots, x_N^i, y_N^i \right]^{\mathsf T}, \quad
\tilde{\boldsymbol{x}}^i = \left[ \tilde{x}_1^i, \tilde{y}_1^i, \dots, \tilde{x}_4^i, \tilde{y}_4^i \right]^{\mathsf T},
\tag{32}
$$

其中 $\boldsymbol{\omega}$ 为令 $c_0 = 1$ 的旋转矩阵，$\boldsymbol{x}^i$ 和 $\tilde{\boldsymbol{x}}^i$ 分别表示细网格节点与粗网格节点的坐标向量，$\mathbf{I}_k$ 表示 $k \times k$ 单位矩阵。将式 (31)–(32) 代入式 (25)，可导出子结构数值形函数的旋转不变性表达式：

$$
\mathbf{N}^i (\mathbf{I}_4 \otimes \boldsymbol{\omega}) \tilde{\boldsymbol{x}}^i = (\mathbf{I}_N \otimes \boldsymbol{\omega}) \boldsymbol{x}^i.
\tag{33}
$$

---

# 3 基于等参单元的 PIML 模型

本节提出基于等参单元的 PIML 模型。该模型利用机器学习技术建立子结构内部单元几何形状和材料分布到其数值形函数之间的映射。神经网络的输入参数包括单个子结构内部所有细网格单元的密度以及子结构的节点坐标，输出为对应的数值形函数。该方法使得数值形函数可由神经网络快速预测生成，从而省去了求逆计算时间，充分发挥了子结构方法的高速分析优势。

## 3.1 机器学习模型的架构与训练流程

机器学习模型采用深度前馈神经网络（Deep Feedforward Neural Network）构建，如图 5 所示。以 $5 \times 5$ 分辨率为例，每个子结构包含 $n_0 = 5^2$ 个细网格单元。$x_i^c$ 和 $y_i^c$ 表示子结构粗网格节点的坐标，$\rho_i \in (0, 1)$ 表示子结构内部细网格单元的密度，$N_0 = (5 - 1)^2$ 表示子结构内部细节点的数量。神经网络以粗网格节点坐标与细网格单元密度为输入，通过 11 个隐藏层最终输出子结构对应的数值形函数。隐藏层的神经元数目分别为 $[100, 120, 140, 160, 180, 200, 180, 160, 140, 120, 100, \text{output}]$，对应的激活函数指定为 `["tanh", "elu", "tanh", "elu", "tanh", "elu", "elu", "tanh", "elu", "tanh", "elu"]`。

训练框架基于 TensorFlow 2.6.2，损失函数采用均方误差（MSE）评估预测形函数与真实数值形函数之间的偏差。优化器选用 Adam，前 1000 个 epoch 学习率设为 0.0001，后续 epoch 调整为 0.00001，总共训练 3000 个 epoch。

显然，数值形函数仅取决于子结构单元几何形状与内部细单元密度分布，与外载荷及宏观边界条件无关，这赋予了所提出的机器学习模型**问题无关性（Problem-Independent）**。一旦模型完成离线训练，即可直接应用于具有相同单元类型的任意边值问题。

![[Zhang2024_Fig5.png]]

<center><b>
图 5：深度神经网络结构示意图。
</b></center>

## 3.2 施加于神经网络的物理约束

神经网络具有概率收敛特性且拟合能力有限。如果无约束地直接输出数值形函数，机器学习模型的精度往往较差。为增强模型的计算精度，本文对网络输出施加物理约束，确保其精确满足子结构数值形函数的平移与旋转不变性（式 (28) 与式 (33)）。

在线性边界条件假定下，对应于子结构边界节点的数值形函数 $\mathbf{B}$ 是常数矩阵。因此，神经网络只需预测对应于子结构内部节点的数值形函数 $\mathbf{N}_2^i$。对 $\mathbf{N}_2^i$ 施加物理约束可得：

$$
\mathbf{N}_2^i (\mathbf{J}_{4,1} \otimes \mathbf{X}_0) = \mathbf{J}_{N_0,1} \otimes \mathbf{X}_0,
\tag{34}
$$

$$
\mathbf{N}_2^i (\mathbf{I}_4 \otimes \boldsymbol{\omega}) \tilde{\boldsymbol{x}}^i = (\mathbf{I}_{N_0} \otimes \boldsymbol{\omega}) \boldsymbol{x}_0^i,
\tag{35}
$$

其中 $\boldsymbol{x}_0^i = [x_k^i, y_k^i, \dots, x_{N_0}^i, y_{N_0}^i]^{\mathsf T}$ 表示对应于子结构内部细网格节点的坐标向量。式 (34) 和式 (35) 分别给出了预测形函数 $\mathbf{N}_2^i$ 必须满足的平移与旋转不变性约束，$N_0$ 为内部细节点数。

将 $\mathbf{N}_2^i$ 按式 (29) 相同方式展开：

$$
\mathbf{N}_2^i =
\begin{bmatrix}
N_{1xx}^{ik} & N_{1xy}^{ik} & N_{2xx}^{ik} & N_{2xy}^{ik} & N_{3xx}^{ik} & N_{3xy}^{ik} & N_{4xx}^{ik} & N_{4xy}^{ik} \\
N_{1yx}^{ik} & N_{1yy}^{ik} & N_{2yx}^{ik} & N_{2yy}^{ik} & N_{3yx}^{ik} & N_{3yy}^{ik} & N_{4yx}^{ik} & N_{4yy}^{ik} \\
\vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots & \vdots \\
N_{1xx}^{iN_0} & N_{1xy}^{iN_0} & N_{2xx}^{iN_0} & N_{2xy}^{iN_0} & N_{3xx}^{iN_0} & N_{3xy}^{iN_0} & N_{4xx}^{iN_0} & N_{4xy}^{iN_0} \\
N_{1yx}^{iN_0} & N_{1yy}^{iN_0} & N_{2yx}^{iN_0} & N_{2yy}^{iN_0} & N_{3yx}^{iN_0} & N_{3yy}^{iN_0} & N_{4yx}^{iN_0} & N_{4yy}^{iN_0}
\end{bmatrix}
=
\begin{bmatrix}
\mathbf{N}_2^{iL} & \mathbf{N}_2^{iR}
\end{bmatrix},
\tag{36}
$$

其中 $\mathbf{N}_2^i$ 的列秩为 5。

为在神经网络中施加物理约束，将 $\mathbf{N}_2^i$ 划分为两个列分块矩阵：线性无关的 $\mathbf{N}_2^{iL} \in \mathbb{R}^{2N_0 \times 5}$，以及与 $\mathbf{N}_2^{iL}$ 线性相关的 $\mathbf{N}_2^{iR} \in \mathbb{R}^{2N_0 \times 3}$。神经网络仅需输出 $\mathbf{N}_2^{iL}$，而 $\mathbf{N}_2^{iR}$ 则通过式 (34)–(35) 直接解析求解。求解推导如下：

为简化推导，定义式 (34)–(35) 右端为 $\boldsymbol{\phi}_t^{i0} \triangleq \mathbf{J}_{N_0,1} \otimes \mathbf{X}_0$，$\boldsymbol{\phi}_r^{i0} \triangleq (\mathbf{I}_{N_0} \otimes \boldsymbol{\omega}) \boldsymbol{x}_0^i$。则内部节点数值形函数应满足：

$$
\begin{bmatrix}
\mathbf{N}_2^{iL} & \mathbf{N}_2^{iR}
\end{bmatrix}
\begin{bmatrix}
\tilde{\boldsymbol{\phi}}_t^i & \tilde{\boldsymbol{\phi}}_r^i
\end{bmatrix}
=
\begin{bmatrix}
\boldsymbol{\phi}_t^{i0} & \boldsymbol{\phi}_r^{i0}
\end{bmatrix}.
\tag{37}
$$

$\tilde{\boldsymbol{\phi}}_t^i$ 与 $\tilde{\boldsymbol{\phi}}_r^i$ 的定义与式 (27) 和式 (31) 保持一致。$\boldsymbol{\phi}_t^{i0}$ 与 $\boldsymbol{\phi}_r^{i0}$ 是由 $\boldsymbol{\phi}_t^i$ 与 $\boldsymbol{\phi}_r^i$ 中对应于内部细节点的行组成的矩阵。将 $\tilde{\boldsymbol{\phi}}_t^i$ 和 $\tilde{\boldsymbol{\phi}}_r^i$ 按行分块，可得：

$$
\begin{bmatrix}
\mathbf{N}_2^{iL} & \mathbf{N}_2^{iR}
\end{bmatrix}
\begin{bmatrix}
\tilde{\boldsymbol{\phi}}_{t1}^i & \tilde{\boldsymbol{\phi}}_{r1}^i \\
\tilde{\boldsymbol{\phi}}_{t2}^i & \tilde{\boldsymbol{\phi}}_{r2}^i
\end{bmatrix}
=
\begin{bmatrix}
\boldsymbol{\phi}_t^{i0} & \boldsymbol{\phi}_r^{i0}
\end{bmatrix}.
\tag{38}
$$

由此可直接导出形函数的其余部分 $\mathbf{N}_2^{iR}$：

$$
\mathbf{N}_2^{iR} =
\begin{bmatrix}
\boldsymbol{\phi}_t^{i0} - \mathbf{N}_2^{iL} \tilde{\boldsymbol{\phi}}_{t1}^i & \boldsymbol{\phi}_r^{i0} - \mathbf{N}_2^{iL} \tilde{\boldsymbol{\phi}}_{r1}^i
\end{bmatrix}
\begin{bmatrix}
\tilde{\boldsymbol{\phi}}_{t2}^i & \tilde{\boldsymbol{\phi}}_{r2}^i
\end{bmatrix}^{-1}.
\tag{39}
$$

将网络预测值 $\mathbf{N}_2^{iL}$ 与物理约束计算所得的 $\mathbf{N}_2^{iR}$ 按式 (36) 拼接，即可得到严格满足平移与旋转不变性的数值形函数 $\mathbf{N}_2^i$。

最重要的是，除预测值 $\mathbf{N}_2^{iL}$ 外，式 (39) 中的所有矩阵仅与节点坐标相关，而与结构的材料拓扑无关。机器学习模型完成离线训练后，完整的数值形函数可通过简单的矩阵乘法直接求得，无需在线进行耗时的矩阵求逆，从而极大提升了有限元分析的效率。

## 3.3 样本生成流程

以随机生成的等参子结构作为样本，分别在 $5 \times 5$ 和 $10 \times 10$ 分辨率下生成子结构样本，并分别训练两套神经网络。

样本生成流程如图 6 所示：
1. **极坐标随机生成四个角点**：角点极坐标值 $(r_i, \theta_i)$ 的取值范围如图 6(a) 所示；
2. **直角坐标转换与坐标平移**：将极坐标转换为直角坐标，并以第四个节点为原点平移子结构；
3. **坐标归一化**：如图 6(b)–(c) 所示，对节点坐标进行归一化，以降低神经网络对输入尺寸的敏感性；
4. **细网格离散与随机密度填充**：将子结构按指定分辨率离散为细网格，并赋予随机密度分布。

基于线性边界条件假定，对应于边界节点的数值形函数 $\mathbf{B}$ 为已知常数矩阵；精确计算内部节点对应的数值形函数 $\mathbf{N}_2^i$ 即可完成一个样本的构建。重复图 6 所示流程，总共生成 60 万（0.6 million）个样本用于训练。

![[Zhang2024_Fig6.png]]

<center><b>
图 6：样本生成流程图。
</b></center>

此外，需从数据集中剔除质量较差的样本，例如过度畸变甚至非凸的形状（如图 7(a)–(c) 所示）。为确保有限元分析精度，在结构离散化中本就应避免非凸或严重扭曲的单元。为此设置剔除准则：子结构的各内角必须介于 $30^\circ$ 至 $150^\circ$ 之间，否则予以剔除。虽然这一筛选可能在一定程度上降低样本覆盖率，但显著降低了神经网络的训练难度，并增强了对常规形状子结构的拟合能力。更重要的是，在实际工程的前处理阶段，完全可以通过控制网格划分质量来避免内角小于 $30^\circ$ 或大于 $150^\circ$ 的过度畸变网格，从而有效规避样本覆盖范围之外的风险。

![[Zhang2024_Fig7.png]]

<center><b>
图 7：子结构内角小于 $30^\circ$ 或大于 $150^\circ$ 的劣质样本需被剔除。(a) 内角大于 $180^\circ$；(b) 内角大于 $150^\circ$；(c) 内角小于 $30^\circ$。
</b></center>

与原始 PIML 方法相比，本文模型完整继承了其全部核心优势：第一，输入与输出之间存在理论上唯一的映射关系，保证了模型的有效性与鲁棒性；第二，模型具备纯粹的问题无关性，训练所需的不同形状与密度分布的子结构样本与边界条件无关，一次离线训练即可适用于任意同类边值问题而无需重训；第三，引入等参单元建模，使该方法可以直接用于求解具有复杂几何设计域的拓扑优化问题。

---

# 4 拓扑优化问题设定

所提出的机器学习模型旨在提升有限元分析效率并加速结构拓扑优化进程，所采用的拓扑优化列式与传统方法保持一致。为简便起见，本文采用基于密度过滤的 SIMP 方法 [50, 51] 求解静载荷下的结构柔度最小化问题，数学列式如下：

$$
\begin{aligned}
\text{求}\quad & \boldsymbol{\rho} = (\rho_1, \rho_2, \dots, \rho_n)^{\mathsf T} \\
\text{最小化}\quad & f = \boldsymbol{u}^{\mathsf T} \mathbf{K} \boldsymbol{u} \\
\text{满足条件：}\quad & \mathbf{K}\boldsymbol{u} = \boldsymbol{f}, \\
& g = \frac{V(\boldsymbol{\rho})}{V_0} - \bar{V} \leq 0, \\
& 0 \leq \rho_e \leq 1, \quad e = 1, 2, \dots, n,
\end{aligned}
\tag{40}
$$

其中 $\boldsymbol{\rho}$ 为设计变量向量，$\rho_e$ 为第 $e$ 个单元的相对密度，$n$ 为结构网格单元总数；$f$ 和 $g$ 分别为目标函数（柔度）与体积约束函数；$V(\boldsymbol{\rho})$ 与 $V_0$ 分别表示结构的实体材料体积与设计域总几何体积，$\bar{V}$ 为给定的体积分数上限；$\mathbf{K}$ 为结构总体刚度矩阵，$\boldsymbol{u}$ 和 $\boldsymbol{f}$ 分别为位移向量与外载荷向量。上述列式旨在寻找最佳密度分布 $\boldsymbol{\rho}$，使结构柔度最小，同时满足体积约束、平衡方程及设计变量界限。

与以往研究 [48, 49] 不同，本文方法将**单元几何形状参数**作为额外输入引入神经网络，并基于等参单元构建子结构样本训练机器学习模型，从而实现了复杂设计域的高分辨率拓扑优化。整个计算流程如图 8 所示：

- **Step 1**：离散设计域，生成细网格；
- **Step 2**：将细网格按指定分辨率划分为子结构，并在子结构系统上施加载荷与边界条件；
- **Step 3**：利用所提方法求解粗分辨率网格的位移：
  - 遍历每个粗分辨率单元；
  - 利用 ANN 预测对应的数值形函数；
  - 计算子结构缩聚刚度矩阵；
  - 组装子结构缩聚刚度矩阵并求解粗分辨率问题；
- **Step 4**：重构并计算细分辨率网格的位移；
- **Step 5**：灵敏度分析；
- **Step 6**：通过优化准则法（OC）更新设计变量；
- **Step 7**：收敛性检查：若未满足收敛准则，返回 Step 3 继续迭代；否则终止优化过程。

![[Zhang2024_Fig8.png]]

<center><b>
图 8：所提出方法的计算流程图。
</b></center>

---

# 5 数值算例

本节通过两个典型数值算例（悬挂三角支架算例与蛇形梁算例）验证所提出算法的可靠性与计算效率。文中训练了分别对应于 $5 \times 5$ 和 $10 \times 10$ 子结构分辨率的两套机器学习模型。实体材料与弱材料的杨氏模量分别设为 $E_0 = 1$ 和 $E_{\min} = 10^{-3}$，泊松比均为 $\nu = 0.3$。引入最小相对密度阈值 $\rho_{\min} = 10^{-3}$ 以防止子结构刚度矩阵发生奇异。采用优化准则法（OC 优化器）更新设计变量，当目标函数在最近连续五次迭代中的相对变化量 $objVr5$ [30] 小于 $10^{-7}$ 时判定为收敛并终止优化。所有算例均在一台配备 Intel(R) Xeon(R) Gold 6132 CPU 与 128 GB 内存的工作站上进行串行计算（未使用并行加速技术）。

## 5.1 悬挂三角支架算例

第一个算例为实际工程中的典型结构：悬挂三角支架（Suspension triangle）的拓扑优化 [52]，如图 9 所示。对于具有复杂几何边界的设计域，采用非结构化网格是必不可少的。悬挂三角支架承受以下约束与载荷：左下方圆盘中心施加全固定约束，上方圆盘中心施加水平位移约束，外载荷施加于右下方圆盘中心（载荷大小 $f_x = 0.5, f_y = 0.5$）。体积分数上限设为 $\bar{V} = 0.4$，过滤半径取为细网格平均尺寸的 3 倍。计算采用 $5 \times 5$ 分辨率的子结构，将结构划分为三种不同数量的细网格进行计算与优化：
- **Case 1**：50 万（0.5 million）细单元（四边形等参单元）；
- **Case 2**：170 万（1.7 million）细单元（四边形等参单元）；
- **Case 3**：520 万（5.2 million）细单元（三角形与四边形混合等参单元）。

优化结果汇总于表 1。

![[Zhang2024_Fig9.png]]

<center><b>
图 9：悬挂三角支架问题示意图。
</b></center>

<center><b>
表 1：悬挂三角支架问题的优化结果与计算效率对比。
</b></center>

![[Zhang2024_Table1.png]]

| 工况 | 本文方法（$5 \times 5$ 分辨率子结构） | 传统细网格拓扑优化（Fine Mesh） |
|---|---|---|
| **Case 1**：<br/>50 万细单元（四边形） | $\bar{t}_{\mathrm{FEA}} = 0.24\text{ s}$<br/>$\bar{t}_{\mathrm{TO}} = 5.18\text{ s}$<br/>$C = 127.54$<br/>$C_f = 128.70$ | $\bar{t}_{\mathrm{FEA}} = 21.41\text{ s}$<br/>$\bar{t}_{\mathrm{TO}} = 24.46\text{ s}$<br/>$C = 125.18$<br/>$C_f = C$ |
| **Case 2**：<br/>170 万细单元（四边形） | $\bar{t}_{\mathrm{FEA}} = 0.84\text{ s}$<br/>$\bar{t}_{\mathrm{TO}} = 16.96\text{ s}$<br/>$C = 128.85$<br/>$C_f = 129.98$ | $\bar{t}_{\mathrm{FEA}} = 104.36\text{ s}$<br/>$\bar{t}_{\mathrm{TO}} = 114.29\text{ s}$<br/>$C = 138.52$<br/>$C_f = C$ |
| **Case 3**：<br/>520 万细单元（三角形+四边形混合） | $\bar{t}_{\mathrm{FEA}} = 6.21\text{ s}$<br/>$\bar{t}_{\mathrm{TO}} = 90.07\text{ s}$<br/>$C = 129.29$<br/>$C_f = 120.09$ | $\bar{t}_{\mathrm{FEA}} = 737.34\text{ s}$<br/>$\bar{t}_{\mathrm{TO}} = 804.57\text{ s}$<br/>$C = 131.16$<br/>$C_f = C$ |

从表 1 可以看出，本文方法获得的最优拓扑构型与直接细网格优化结果总体高度吻合，且随着网格分辨率的提高，展现出越来越丰富的细微结构特征。将本文优化构型的柔度 $C$ 与细网格重分析柔度 $C_f$ 进行比较：在 Case 1 与 Case 2 中，柔度相对误差均小于 1%，且细网格柔度 $C_f$ 略微低于子结构柔度 $C$，这归因于线性边界假定为子结构施加了额外运动学约束从而略微增大了子结构刚度；在包含三角形与四边形混合等参网格的 Case 3 中，由于混合网格插值差异，$C_f$ 略大于 $C$，柔度误差依然保持在 8% 以内。这充分验证了所提出方法的计算精度与对复杂边界网格的适应能力。

在计算效率方面，对比单步优化分析中的平均 FEA 求解时间 $\bar{t}_{\mathrm{FEA}}$ 和单步平均总时间 $\bar{t}_{\mathrm{TO}}$：
- 对于本文方法，Case 1、Case 2 和 Case 3 的 $\bar{t}_{\mathrm{FEA}}$ 分别仅为 $0.24\text{ s}$、$0.84\text{ s}$ 和 $6.21\text{ s}$，单步总时间 $\bar{t}_{\mathrm{TO}}$ 分别为 $5.18\text{ s}$、$16.96\text{ s}$ 和 $90.07\text{ s}$；
- 对于传统细网格优化，$\bar{t}_{\mathrm{FEA}}$ 分别为 $21.41\text{ s}$、$104.36\text{ s}$ 和 $737.34\text{ s}$，$\bar{t}_{\mathrm{TO}}$ 分别为 $24.46\text{ s}$、$114.29\text{ s}$ 和 $804.57\text{ s}$。

如图 10 所示，本文方法在三个工况下将有限元方程求解时间 $\bar{t}_{\mathrm{FEA}}$ 分别缩减了 **89 倍**（Case 1）、**124 倍**（Case 2）和 **119 倍**（Case 3）；拓扑优化单步总时间 $\bar{t}_{\mathrm{TO}}$ 相应加快了 **5 倍**、**7 倍** 和 **9 倍**。

从时间占比来看，在传统细网格优化中，$\bar{t}_{\mathrm{FEA}}$ 占单步总时间 $\bar{t}_{\mathrm{TO}}$ 的比例分别高达 87.53%（Case 1）、91.31%（Case 2）和 91.64%（Case 3），证实有限元分析是拓扑优化的决定性瓶颈；而在本文方法中，$\bar{t}_{\mathrm{FEA}}$ 占 $\bar{t}_{\mathrm{TO}}$ 的比例急剧降至 4.63%（Case 1）、4.95%（Case 2）和 6.89%（Case 3）。这意味着有限元方程的求解已不再是拓扑优化的主要计算瓶颈，刚度矩阵的装配与灵敏度计算等其他子步骤逐渐成为主要计算开销。

图 11 展示了 Case 2（170 万单元）的目标函数与体积分数约束的迭代历史曲线。本文方法（红色实线）与传统细网格优化（红色虚线）均在约 50 步内收敛，且体积约束函数（蓝色曲线）在优化全过程中平稳满足。

![[Zhang2024_Fig10.png]]

<center><b>
图 10：在 170 万单元分辨率下计算悬挂三角支架问题时，所提方法与细网格优化的效率对比。
</b></center>

![[Zhang2024_Fig11.png]]

<center><b>
图 11：在 170 万单元分辨率下悬挂三角支架算例的迭代历史。
</b></center>

## 5.2 蛇形梁算例

图 12 所示的蛇形梁（Serpentine beam）问题 [52] 进一步展示了所提出方法在不同子结构分辨率下的效率提升规律。结构左侧边界完全固定，右下角承受垂直集中载荷（$f = 1$），体积分数上限设定为 0.4。算例分别采用 $5 \times 5$ 和 $10 \times 10$ 两种子结构分辨率；过滤半径在 $5 \times 5$ 分辨率下取单元尺寸的 3 倍，在 $10 \times 10$ 分辨率和直接细网格优化中取单元尺寸的 7 倍。设计域全部采用四边形等参单元离散，分别设置四种不同规模的细网格单元数进行优化计算：
- **Case 1**：10 万（0.1 million）细单元；
- **Case 2**：50 万（0.5 million）细单元；
- **Case 3**：100 万（1.0 million）细单元；
- **Case 4**：500 万（5.0 million）细单元。

优化结果汇总于表 2。

![[Zhang2024_Fig12.png]]

<center><b>
图 12：蛇形梁问题示意图。
</b></center>

<center><b>
表 2：不同分辨率下所提方法与细网格优化的优化结果与计算效率对比。
</b></center>

![[Zhang2024_Table2.png]]

| 细网格规模                    | 本文方法（$5 \times 5$ 分辨率）                                                                                  | 本文方法（$10 \times 10$ 分辨率）                                                                                | 传统细网格拓扑优化（Fine Mesh）                                                                                      |
| ------------------------ | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Case 1**：<br/>10 万细单元  | $\bar{t}_{\mathrm{FEA}} = 0.0349\text{ s}$<br/>$\bar{t}_{\mathrm{TO}} = 0.85\text{ s}$<br/>$C = 373.29$ | $\bar{t}_{\mathrm{FEA}} = 0.0073\text{ s}$<br/>$\bar{t}_{\mathrm{TO}} = 1.52\text{ s}$<br/>$C = 409.98$ | $\bar{t}_{\mathrm{FEA}} = 2.38\text{ s}$<br/>$\bar{t}_{\mathrm{TO}} = 3.25\text{ s}$<br/>$C = 424.28$     |
| **Case 2**：<br/>50 万细单元  | $\bar{t}_{\mathrm{FEA}} = 0.226\text{ s}$<br/>$\bar{t}_{\mathrm{TO}} = 4.68\text{ s}$<br/>$C = 372.13$  | $\bar{t}_{\mathrm{FEA}} = 0.042\text{ s}$<br/>$\bar{t}_{\mathrm{TO}} = 8.77\text{ s}$<br/>$C = 373.55$  | $\bar{t}_{\mathrm{FEA}} = 21.52\text{ s}$<br/>$\bar{t}_{\mathrm{TO}} = 27.59\text{ s}$<br/>$C = 382.10$   |
| **Case 3**：<br/>100 万细单元 | $\bar{t}_{\mathrm{FEA}} = 0.479\text{ s}$<br/>$\bar{t}_{\mathrm{TO}} = 8.98\text{ s}$<br/>$C = 374.32$  | $\bar{t}_{\mathrm{FEA}} = 0.096\text{ s}$<br/>$\bar{t}_{\mathrm{TO}} = 18.65\text{ s}$<br/>$C = 370.02$ | $\bar{t}_{\mathrm{FEA}} = 65.36\text{ s}$<br/>$\bar{t}_{\mathrm{TO}} = 53.61\text{ s}$<br/>$C = 380.80$   |
| **Case 4**：<br/>500 万细单元 | $\bar{t}_{\mathrm{FEA}} = 6.39\text{ s}$<br/>$\bar{t}_{\mathrm{TO}} = 79.15\text{ s}$<br/>$C = 384.02$  | $\bar{t}_{\mathrm{FEA}} = 1.55\text{ s}$<br/>$\bar{t}_{\mathrm{TO}} = 65.11\text{ s}$<br/>$C = 200.87$  | $\bar{t}_{\mathrm{FEA}} = 771.44\text{ s}$<br/>$\bar{t}_{\mathrm{TO}} = 877.83\text{ s}$<br/>$C = 383.68$ |

对比不同子结构分辨率的计算效率可知：
- 在 FEA 求解时间 $\bar{t}_{\mathrm{FEA}}$ 上，$5 \times 5$ 分辨率在 Case 1 至 Case 4 中分别为 $0.0349\text{ s}$、$0.226\text{ s}$、$0.479\text{ s}$ 和 $6.39\text{ s}$；而 $10 \times 10$ 分辨率则进一步缩减至 $0.0073\text{ s}$、$0.042\text{ s}$、$0.096\text{ s}$ 和 $1.55\text{ s}$。子结构分辨率越高，粗网格宏观方程的自由度越少，有限元求解的效率优势越显著。相对于直接细网格分析，$5 \times 5$ 子结构加速了 68 倍（Case 1）、95 倍（Case 2）、136 倍（Case 3）和 120 倍（Case 4）；而 $10 \times 10$ 子结构加速了 **326 倍**（Case 1）、**512 倍**（Case 2）、**680 倍**（Case 3）和 **497 倍**（Case 4）。
- 在拓扑优化单步总时间 $\bar{t}_{\mathrm{TO}}$ 上，在较低网格规模下（Case 1~3），由于 FEA 耗时已非主要矛盾，提高子结构分辨率带来的总时间缩减并不显著（$10 \times 10$ 因内部重构计算略微增加了前处理开销）；但在 500 万单元的大规模算例（Case 4）中，$\bar{t}_{\mathrm{TO}}$ 从直接细网格的 $877.83\text{ s}$ 分别降至 $79.15\text{ s}$（$5 \times 5$）和 $65.11\text{ s}$（$10 \times 10$）。拓扑优化整体效率分别提升了 **11 倍** 与 **13 倍**，$10 \times 10$ 分辨率的综合加速效果最终超越了 $5 \times 5$ 分辨率。

综合来看，有限元方程求解时间 $\bar{t}_{\mathrm{FEA}}$ 减少了 **两个数量级**，而拓扑优化总耗时 $\bar{t}_{\mathrm{TO}}$ 降低了 **一个数量级**，显著加速了高分辨率复杂域拓扑优化。

在优化构型方面，随着单元数量的增加，结构除主传力路径外，在 $10 \times 10$ 分辨率的 Case 4 中展现出极其细致的分支网状结构，在满足体积分数的同时大幅提升了结构刚度；而 $5 \times 5$ 分辨率的结果则展示出更具启发性的材料布局形式，对实现创新工程结构设计具有重要指导意义。

---

# 6 结论

为了实现复杂设计域高分辨率拓扑优化问题的高效静力分析与优化设计，本文利用二维四节点等参单元构建了问题无关机器学习（PIML）模型。通过离线样本生成与模型训练，训练后的机器学习模型可直接嵌入拓扑优化流程中，无需对任意几何形状的设计域或边界条件进行任何额外重新训练。同时，通过引入刚体位移力学原理约束，显著提升了神经网络的预测精度。在不依赖并行计算技术的前提下，数值算例表明该方法使有限元方程求解效率提升了两个数量级以上，并将大规模拓扑优化的整体求解效率提高了一个数量级。

基于六面体单元的 PIML 模型可将本工作推广至三维问题；随着三维数值形函数元素数量的大幅增加，如何保证对应机器学习模型的预测精度需要深入研究。此外，尽管细分子结构能有效捕捉细微拓扑特征，但宏观结构的外轮廓边界仍然由粗网格单元几何决定，细化过程未能进一步提升有限元模型与实际几何模型的贴合度。等几何分析（IGA）方法有望解决更复杂几何设计域的保形建模问题，构建基于 IGA 的 PIML 模型是未来值得深入探索的方向。相关工作正在广泛研究中，后续将另行报道。

---

# CRediT 作者贡献说明

- **Chang Liu**：论文撰写 – 审阅与编辑，论文撰写 – 初稿，验证，调查研究。
- **Tianchen Cui**：论文撰写 – 审阅与编辑，论文撰写 – 初稿，验证，指导，方法学，数据审定。
- **Zongliang Du**：验证，指导，调查研究，数据审定。
- **Xu Guo**：论文撰写 – 审阅与编辑，指导，方法学，资金争取，概念构思。
- **Mengcheng Huang**：论文撰写 – 初稿，验证，调查研究。
- **Linfeng Zhang**：论文撰写 – 审阅与编辑，论文撰写 – 初稿，指导，方法学，形式分析，数据审定，概念构思。

# 利益冲突声明

作者声明不存在可能影响本文报道工作的已知经济利益竞争或人际关系冲突。

# 数据可用性声明

本文涉及的研究数据可根据合理要求向作者索取。

# 致谢

本研究得到国家重点研发计划（No. 2023YFB3309104）、国家自然科学基金（No. 11821202）和高等学校学科创新引智计划（111 计划，No. B14013）的资助。

---

# 参考文献

[1] O.M. Querin, G.P. Steven, Y.M. Xie, Evolutionary structural optimisation (ESO) using a bidirectional algorithm, Eng. Comput. 15 (8) (1998) 1031–1048, https://doi.org/10.1108/02644409810244129.

[2] M.Y. Wang, X. Wang, D. Guo, A level set method for structural topology optimization, Comput. Methods Appl. Mech. Engrg. 192 (1-2) (2003) 227–246, https://doi.org/10.1016/S0045-7825(02)00559-5.

[3] G. Allaire, F. Jouve, A.-M. Toader, Structural optimization using sensitivity analysis and a level-set method, J. Comput. Phys. 194 (1) (2004) 363–393, https://doi.org/10.1016/j.jcp.2003.09.032.

[4] G.I.N. Rozvany, A critical review of established methods of structural topology optimization, Struct. Multidiscip. Optim. 37 (3) (2008) 217–237, https://doi.org/10.1007/s00158-007-0217-0.

[5] X. Guo, G.-D. Cheng, Recent development in structural design and optimization, Acta Mech. Sin. 26 (6) (2010) 807–823, https://doi.org/10.1007/s10409-010-0395-7.

[6] J.D. Deaton, R.V. Grandhi, A survey of structural and multidisciplinary continuum topology optimization: post 2000, Struct. Multidiscip. Optim. 49 (1) (2014) 1–38, https://doi.org/10.1007/s00158-013-0956-z.

[7] O. Sigmund, K. Maute, Topology optimization approaches, Struct. Multidiscip. Optim. 48 (6) (2013) 1031–1055, https://doi.org/10.1007/s00158-013-0978-6.

[8] W. Zhang, J. Yuan, J. Zhang, X. Guo, A new topology optimization approach based on Moving Morphable Components (MMC) and the ersatz material model, Struct. Multidiscip. Optim. 53 (6) (2016) 1243–1260, https://doi.org/10.1007/s00158-015-1372-3.

[9] W. Zhang, J. Chen, X. Zhu, J. Zhou, D. Xue, X. Lei, X. Guo, Explicit three dimensional topology optimization via Moving Morphable Void (MMV) approach, Comput. Methods Appl. Mech. Engrg. 322 (2017) 590–614, https://doi.org/10.1016/j.cma.2017.05.002.

[10] T. Borrvall, J. Petersson, Large-scale topology optimization in 3D using parallel computing, Comput. Methods Appl. Mech. Engrg. 190 (46-47) (2001) 6201–6229, https://doi.org/10.1016/S0045-7825(01)00216-X.

[11] N. Aage, B.S. Lazarov, Parallel framework for topology optimization using the method of moving asymptotes, Struct. Multidiscip. Optim. 47 (4) (2013) 493–505, https://doi.org/10.1007/s00158-012-0869-2.

[12] T. Zegard, G.H. Paulino, Toward GPU accelerated topology optimization on unstructured meshes, Struct. Multidiscip. Optim. 48 (3) (2013) 473–485, https://doi.org/10.1007/s00158-013-0920-y.

[13] N. Aage, E. Andreassen, B.S. Lazarov, Topology optimization using PETSc: An easy-to-use, fully parallel, open source topology optimization framework, Struct. Multidiscip. Optim. 51 (3) (2015) 565–572, https://doi.org/10.1007/s00158-014-1157-0.

[14] T. Smit, N. Aage, S.J. Ferguson, B. Helgason, Topology optimization using PETSc: a Python wrapper and extended functionality, Struct. Multidiscip. Optim. 64 (6) (2021) 4343–4353, https://doi.org/10.1007/s00158-021-03018-7.

[15] L. Liu, J. Yan, G. Cheng, Optimum structure with homogeneous optimum truss-like material, Comput. Struct. 86 (13-14) (2008) 1417–1425, https://doi.org/10.1016/j.compstruc.2007.04.030.

[16] J. Kato, D. Yachi, K. Terada, T. Kyoya, Topology optimization of micro-structure for composites applying a decoupling multi-scale analysis, Struct. Multidiscip. Optim. 49 (4) (2014) 595–608, https://doi.org/10.1007/s00158-013-0994-6.

[17] X. Liang, J. Du, Concurrent multi-scale and multi-material topological optimization of vibro-acoustic structures, Comput. Methods Appl. Mech. Engrg. 349 (2019) 117–148, https://doi.org/10.1016/j.cma.2019.02.010.

[18] A. Pizzolato, A. Sharma, K. Maute, A. Sciacovelli, V. Verda, Multi-scale topology optimization of multi-material structures with controllable geometric complexity - Applications to heat transfer problems, Comput. Methods Appl. Mech. Engrg. 357 (2019) 112552, https://doi.org/10.1016/j.cma.2019.07.021.

[19] H. Zhang, X. Ding, H. Li, M. Xiong, Multi-scale structural topology optimization of free-layer damping structures with damping composite materials, Compos. Struct. 212 (2019) 609–624, https://doi.org/10.1016/j.compstruct.2019.01.059.

[20] J.P. Groen, C.R. Thomsen, O. Sigmund, Multi-scale topology optimization for stiffness and de-homogenization using implicit geometry modeling, Struct. Multidiscip. Optim. 63 (6) (2021) 2919–2934, https://doi.org/10.1007/s00158-021-02874-7.

[21] J. Wu, O. Sigmund, J.P. Groen, Topology optimization of multi-scale structures: a review, Struct. Multidiscip. Optim. 63 (3) (2021) 1455–1480, https://doi.org/10.1007/s00158-021-02881-8.

[22] Z. Duan, Y. Liu, J. Fan, K. Long, B. Xu, J. Zhu, J. Yan, Concurrent multi-material and multi-scale design optimization of fiber-reinforced composite material and structures for minimum structural compliance, Compos. Struct. 311 (2023) 116796, https://doi.org/10.1016/j.compstruct.2023.116796.

[23] Y.Y. Kim, G.H. Yoon, Multi-resolution multi-scale topology optimization - a new paradigm, Int. J. Solids Struct. 37 (39) (2000) 5529–5559, https://doi.org/10.1016/S0020-7683(99)00251-6.

[24] J. Park, A. Sutradhar, A multi-resolution method for 3D multi-material topology optimization, Comput. Methods Appl. Mech. Engrg. 285 (2015) 571–586, https://doi.org/10.1016/j.cma.2014.10.011.

[25] J.P. Groen, M. Langelaar, O. Sigmund, M. Ruess, Higher-order multi-resolution topology optimization using the finite cell method, Int. J. Numer. Methods Eng. 110 (10) (2016) 903–920, https://doi.org/10.1002/nme.5432.

[26] Q.X. Lieu, J. Lee, A multi-resolution approach for multi-material topology optimization based on isogeometric analysis, Comput. Methods Appl. Mech. Engrg. 323 (2017) 272–302, https://doi.org/10.1016/j.cma.2017.05.009.

[27] C. Liu, Y. Zhu, Z. Sun, D. Li, Z. Du, W. Zhang, X. Guo, An efficient moving morphable component (MMC)-based approach for multi-resolution topology optimization, Struct. Multidiscip. Optim. 58 (6) (2018) 2455–2479, https://doi.org/10.1007/s00158-018-2114-0.

[28] H. Wang, J. Liu, G. Wen, An efficient evolutionary structural optimization method for multi-resolution designs, Struct. Multidiscip. Optim. 62 (2) (2020) 787–803, https://doi.org/10.1007/s00158-020-02536-0.

[29] M. Huang, W. Huo, C. Liu, D. Yang, J. Huang, Z. Du, X. Guo, Substructuring multi-resolution topology optimization with template, Adv. Mech. 51 (4) (2021) 901–909. URL https://lxjz.cstam.org.cn/en/article/doi/10.6052/1000-0992-21-030.

[30] Z. Du, T. Cui, C. Liu, W. Zhang, Y. Guo, X. Guo, An efficient and easy-to-extend Matlab code of the Moving Morphable Component (MMC) method for three-dimensional topology optimization, Struct. Multidiscip. Optim. 65 (5) (2022) 158, https://doi.org/10.1007/s00158-022-03239-4.

[31] O. Amir, M.P. Bendsøe, O. Sigmund, Approximate reanalysis in topology optimization, Int. J. Numer. Methods Eng. 78 (12) (2009) 1474–1491, https://doi.org/10.1002/nme.2536.

[32] I. Sosnovik, I. Oseledets, Neural networks for topology optimization, Russ. J. Numer. Anal. Math. Model. 34 (2017) 215–223, https://doi.org/10.1515/rnam-2019-0018.

[33] N.A. Kallioras, G. Kazakis, N.D. Lagaros, Accelerated topology optimization by means of deep learning, Struct. Multidiscip. Optim. 62 (3) (2020) 1185–1212, https://doi.org/10.1007/s00158-020-02545-z.

[34] D. Bielecki, D. Patel, R. Rai, G.F. Dargush, Multi-stage deep neural network accelerated topology optimization, Struct. Multidiscip. Optim. 64 (6) (2021) 3473–3487, https://doi.org/10.1007/s00158-021-03028-5.

[35] Y. Yu, T. Hur, J. Jung, I.G. Jang, Deep learning for determining a near-optimal topological design without any iteration, Struct. Multidiscip. Optim. 59 (3) (2019) 787–799, https://doi.org/10.1007/s00158-018-2101-5.

[36] D. Patel, D. Bielecki, R. Rai, G. Dargush, Improving connectivity and accelerating multiscale topology optimization using deep neural network techniques, Struct. Multidiscip. Optim. 65 (4) (2022) 126, https://doi.org/10.1007/s00158-022-03223-y.

[37] X. Lei, C. Liu, Z. Du, W. Zhang, X. Guo, Machine Learning-Driven Real-Time Topology Optimization Under Moving Morphable Component-Based Framework, J. Appl. Mech. 86 (1) (2019) 011004, https://doi.org/10.1115/1.4041319.

[38] X. Chen, Z. Zhang, Y. Li, W. Yao, W. Zhou, Research on structure topology optimization design empowered by deep learning method, Adv. Mech. 54 (2) (2024) 1–46, https://doi.org/10.6052/1000-0992-23-052.

[39] V. Keshavarzzadeh, R.M. Kirby, A. Narayan, Robust topology optimization with low rank approximation using artificial neural networks, Comput. Mech. 68 (6) (2021) 1297–1323, https://doi.org/10.1007/s00466-021-02069-3.

[40] R.K. Tan, C. Qian, K. Li, D. Xu, W. Ye, An adaptive and scalable artificial neural network-based model-order-reduction method for large-scale topology optimization designs, Struct. Multidiscip. Optim. 65 (12) (2022) 348, https://doi.org/10.1007/s00158-022-03456-x.

[41] H. Chi, Y. Zhang, T.L.E. Tang, L. Mirabella, L. Dalloro, L. Song, G.H. Paulino, Universal machine learning for topology optimization, Comput. Methods Appl. Mech. Engrg. 375 (2021) 112739, https://doi.org/10.1016/j.cma.2019.112739.

[42] F.V. Senhora, H. Chi, Y. Zhang, L. Mirabella, T.L.E. Tang, G.H. Paulino, Machine learning for topology optimization: Physics-based learning through an independent training strategy, Comput. Methods Appl. Mech. Engrg. 398 (2022) 115116, https://doi.org/10.1016/j.cma.2022.115116.

[43] J. Luo, Y. Li, W. Zhou, Z. Gong, Z. Zhang, W. Yao, An Improved Data-Driven Topology Optimization Method Using Feature Pyramid Networks with Physical Constraints, Comp. Model. Eng. Sci. 128 (3) (2021) 823–848, https://doi.org/10.32604/cmes.2021.016737.

[44] L. Lu, R. Pestourie, W. Yao, Z. Wang, F. Verdugo, S.G. Johnson, Physics-Informed Neural Networks with Hard Constraints for Inverse Design, SIAM J. Sci. Comput. 43 (6) (2021) B1105–B1132, https://doi.org/10.1137/21m1397908.

[45] Z. Xia, H. Zhang, Z. Zhuang, C. Yu, J. Yu, L. Gao, A machine-learning framework for isogeometric topology optimization, Struct. Multidiscip. Optim. 66 (4) (2023) 83, https://doi.org/10.1007/s00158-023-03539-3.

[46] C. Deng, Y. Wang, C. Qin, Y. Fu, W. Lu, Self-directed online machine learning for topology optimization, Nat. Commun. 13 (1) (2022) 388, https://doi.org/10.1038/s41467-021-27713-7.

[47] K. Li, W. Ye, Y. Gao, A 3D Structure Mapping-Based Efficient Topology Optimization Framework, J. Mech. Des. 145 (8) (2023) 081703, https://doi.org/10.1115/1.4062352.

[48] M. Huang, Z. Du, C. Liu, Y. Zheng, T. Cui, Y. Mei, X. Li, X. Zhang, X. Guo, Problem-independent machine learning (PIML)-based topology optimization—A universal approach, Extrem. Mech. Lett. 56 (2022) 101887, https://doi.org/10.1016/j.eml.2022.101887.

[49] M. Huang, T. Cui, C. Liu, Z. Du, J. Zhang, C. He, X. Guo, A Problem-Independent Machine Learning (PIML) enhanced substructure-based approach for large-scale structural analysis and topology optimization of linear elastic structures, Extrem. Mech. Lett. 63 (2023) 102041, https://doi.org/10.1016/j.eml.2023.102041.

[50] O. Sigmund, A 99 line topology optimization code written in Matlab, Struct. Multidiscip. Optim. 21 (2) (2001) 120–127, https://doi.org/10.1007/s001580050176.

[51] E. Andreassen, A. Clausen, M. Schevenels, B.S. Lazarov, O. Sigmund, Efficient topology optimization in MATLAB using 88 lines of code, Struct. Multidiscip. Optim. 43 (1) (2010) 1–16, https://doi.org/10.1007/s00158-010-0594-7.

[52] C. Talischi, G.H. Paulino, A. Pereira, I.F.M. Menezes, PolyTop: a Matlab implementation of a general topology optimization framework using unstructured polygonal finite element meshes, Struct. Multidiscip. Optim. 45 (3) (2012) 329–357, https://doi.org/10.1007/s00158-011-0696-x.
