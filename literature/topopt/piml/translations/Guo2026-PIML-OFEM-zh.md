---
title: "翻译：PIML-OFEM: A New Large-Scale Structural Analysis Method Based on Problem-Independent Machine Learning and Overlapping Finite Element Technique"
tags:
  - translation
  - PIML
  - topology-opt
  - substructure
  - OFEM
  - oversampling
status: "done"
date_created: 2026-08-04
date_updated: 2026-09-10
source: "../sources/Guo2026-PIML-OFEM.pdf"
citekey: "guoPIMLOFEMNewLargeScale2026"
language: "zh-CN"
---

# PIML-OFEM: A New Large-Scale Structural Analysis Method Based on Problem-Independent Machine Learning and Overlapping Finite Element Technique

---

# 信息

- **中文标题**：PIML-OFEM：一种基于问题无关机器学习与重叠有限元技术的新型大规模结构分析方法
- **作者**：Yilin Guo（郭一麟）$^1$；Chang Liu（刘畅）$^{1,*}$；Zongliang Du（杜宗亮）$^{1,2}$；Jin Liu（刘进）$^1$；Jingyu Feng（冯靖宇）$^1$；Xinyang Zhang（张欣阳）$^1$；Yang Li（李阳）$^1$；Tianxing Yang（杨添行）$^1$；Changyu Shen（申长雨）$^{1,3,*}$；Xu Guo（郭旭）$^{1,2,*}$
- **单位**：
  - $1$: 大连理工大学工程力学系、工业装备结构分析优化与 CAE 软件国家重点实验室（大连 116023）
  - $2$: 大连市工业软件研究院（大连 116085）
  - $3$: 郑州大学材料科学与工程学院、材料成型及模具技术教育部重点实验室（郑州 450002）
- **来源**：arXiv.org
- **版本**：arXiv:2607.22019v1
- **提交日期**：2026-07-24
- **证据等级**：arXiv v1 预印本，不作为已正式发表期刊论文表述。
- **通讯作者**：Chang Liu（c.liu@dlut.edu.cn）；Changyu Shen（shency@zzu.edu.cn）；Xu Guo（guoxu@dlut.edu.cn）

# 摘要

高分辨率结构分析与大规模异质结构快速设计，既需要精确的降阶模型，也需要高效的在线计算。在传统多尺度有限元框架下，针对不同材料分布在线构造多尺度形函数面临高昂的计算代价；而前期发展的基于子结构的问题无关机器学习（PIML）技术，其分析精度常受限于子结构边界上假设的位移分布形式。为应对上述挑战，我们提出 PIML-OFEM——一种由问题无关机器学习加速的重叠有限元方法。

该方法仅保留每个子结构的角节点自由度，并通过在扩展域上求解局部边值问题，构造与这些自由度相关联的数值基函数。这种降阶模型的构造方式无需在目标子结构边界预设位移假设，显著提升了数值基函数再现子结构局部变形的能力。进一步引入单位分解重叠有限元格式，将子结构上独立构造的数值基函数插值为具有全局连续性的整体基函数。为避免在线求解子结构上的数值基函数，我们训练了一个 U-Net，用于学习从子结构杨氏模量分布到其数值基函数的确定性映射。由于该学习过程不依赖于特定的荷载工况与边界条件，所习得的数值形函数可适用于任意同类结构分析与优化问题的求解。

数值算例表明，PIML-OFEM 获得的位移与单元应变能与细尺度有限元结果高度吻合，其在线计算成本显著低于直接有限元分析，同时计算精度大幅优于基于边界线性插值的 PIML 方法。当将该方法嵌入拓扑优化流程时，PIML-OFEM 能够实现小滤波半径的高分辨率优化，并保留包括类秩-2 微结构局部模式在内的细尺度结构特征。通过融合基于力学原理的局部独立降阶、全局连续耦合以及问题无关的机器学习技术，PIML-OFEM 为大尺度异质结构分析与高分辨率拓扑优化建立了一种高效的人工智能赋能数值计算新范式。

**关键词**：问题无关机器学习（Problem-Independent Machine Learning, PIML）；重叠有限元（Overlapping finite element）；超采样数值基函数（Oversampled numerical basis function）；拓扑优化（Topology optimization）；U-Net

---

# 1 引言

高效且具可扩展性的数值仿真方法是复杂工程结构分析与优化设计的基石。对于具有高度非均匀材料分布、复杂几何边界或强烈局部响应的结构，传统有限元方法通常需要极高分辨率的细网格来准确捕捉位移、应变与应变能分布。特别是在结构拓扑优化中 [1]，有限元分析必须在优化循环中反复执行，其计算成本随设计自由度数和网格分辨率的提高呈爆发式增长。因此，如何在保持细尺度分析精度的同时大幅削减在线求解成本，是大规模异质结构分析与高分辨率拓扑优化中的核心挑战。

近年来，机器学习方法为加速科学计算提供了新思路，并已被应用于湍流建模 [2–4]、材料设计 [5–7] 和数值仿真 [8–10]。然而，许多机器学习增强的数值方法仍表现出显著的问题依赖性。例如，某些端到端模型直接学习特定几何形状、边界条件和外载荷形式到整体物理场的映射 [11–18]；另一些方法将神经网络视为可训练的函数逼近器，并针对特定问题重新优化网络参数，如 HiDeNN 方法 [19–22] 及将分段多项式和弱形式残差引入神经表征的相关工作 [23, 24]。在拓扑优化中，机器学习还被用于直接预测灵敏度以消除位移场求解 [25, 26]。这类方法针对特定算例可达到很高效率，但一旦结构尺寸、材料拓扑、边界条件或载荷形式发生改变，往往需要重新训练或重新优化，极大地限制了泛化能力与模型复用性。

为了提升机器学习模型在力学分析中的可移植性，问题无关机器学习模型被引入大规模力学分析与拓扑优化中 [27–30]。该类方法的核心思想不是学习特定边值问题的全局解，而是学习由局部材料分布唯一决定的局部数值算子或多尺度数值形函数。由于这些局部映射与整体结构几何、外载荷及宏观边界条件解耦，所训练的模型在原理上可跨任务复用于同类偏微分方程控制的结构分析中。基于这一构想，郭旭团队提出了**问题无关机器学习（PIML）**范式，通过子结构缩聚显著缩减在线自由度规模 [31, 32]，并利用离线训练的神经网络快速预测局部数值形函数，显著提升了求解效率。

尽管 PIML 方法已被成功推广至超高分辨率拓扑优化 [33]、点阵结构 [34]、壳层填充复合结构 [35] 以及复杂几何设计域结构优化 [36]，但现有的基于子结构缩聚的 PIML 框架仍面临精度与效率的基础权衡：若每个二维子结构仅保留 4 个角节点（共 8 个自由度），通常必须假设子结构边界位移沿边界呈线性变化；这一边界线性假定削弱了方法表征复杂局部变形、孔洞邻域应力扰动以及集中载荷附近局部尖锐响应的能力。如果通过增加边界控制自由度或引入高阶边界插值来提升精度 [37]，则会急剧增大缩聚系统的规模，降低全局刚度矩阵的稀疏度，并大幅增加神经网络预测的输出维度，从而削弱子结构降阶的原本效率优势。因此，如何在不增加边界控制自由度的前提下显著提升子结构边界及内部位移恢复精度，是当前 PIML 子结构方法亟待攻克的关键瓶颈。

**超采样技术（Oversampling techniques）**为消除上述“边界层误差（Boundary layer errors）”提供了有效途径 [38, 39]。通过在覆盖目标子结构的扩展区域上求解局部边值问题，可构造自适应于局部非均匀材料分布的多尺度数值基函数，从而避免在目标子结构边界上人为强加线性或高阶插值假定。然而，仅引入超采样形函数尚不足以构成全局可用的降阶分析框架：由于各子结构的超采样形函数由其各自局部材料分布独立决定，相邻子结构在共享公共角节点位移协调的同时，沿共享交界面通常产生不一致的位移分布，导致全局位移场发生物理间断，严重破坏了应变、应变能以及拓扑优化灵敏度等高阶衍生量的可靠性。此外，若在线逐个求解子结构的超采样局部方程，计算量巨大，难以满足大规模拓扑优化的多轮迭代需求。

针对上述难题，本文提出了一种基于问题无关机器学习的重叠有限元子结构分析框架，命名为 **PIML-OFEM**。该框架首先为每个子结构构造基于超采样的多尺度数值基函数，二维问题中仅保留 4 个角节点（8 个自由度），以增强低维缩聚空间对局部复杂变形的表达能力；随后，引入**重叠有限元（Overlapping Finite Element）**与**单位分解（Partition of Unity）**思想 [40–48]，通过权函数加权组合将相邻子结构的局部插值协调为全局连续的位移场，消除了独立子结构形函数在共享界面引起的位移跳跃；在此基础上，遵循 PIML 框架 [27–29] 训练 U-Net 模型，学习从超采样区材料分布到局部数值基函数的确定性非线性映射，以批处理神经网络推理替代昂贵的在线局部边值问题求解。

本文的主要贡献体现在四个方面：
1. **构造了无需在目标子结构边界施加线性位移假设的超采样数值基函数**，在仅保留 4 个角节点（8 个自由度）的前提下显著增强了复杂局部变形的恢复能力；
2. **引入了基于单位分解的重叠有限元位移协调机制**，将独立子结构的局部降阶位移场嵌入全局连续位移空间，使得计算结果可安全用于应变、应变能及拓扑优化灵敏度等连续性敏感的后处理任务；
3. **建立了面向局部材料分布的 U-Net 预测模型**，使机器学习模块与全局结构尺寸、边界条件和载荷形式彻底解耦，具备严格的问题无关性；
4. **利用正交笛卡尔网格与有限的 16 类重叠细单元类型，将与权函数相关的积分和局部刚度计算完全离线预处理并内存复用**，保持了在线组装与求解流程的高效性。

本文其余部分安排如下：第 2 节介绍基于超采样数值基函数的子结构降阶建模；第 3 节阐述基于单位分解重叠有限元的全局位移协调方法及其与超采样降阶映射的耦合；第 4 节介绍快速预测超采样基函数的 U-Net 模型、训练数据与损失函数；第 5 节通过悬臂梁、复杂孔洞拓扑及高分辨率拓扑优化算例验证精度、效率与泛化性；第 6 节给出结论与未来展望。

---

# 2 基于超采样数值基函数的子结构降阶建模

本节首先回顾经典子结构缩聚的基本列式，在此基础上为独立子结构构建超采样数值基函数。需要说明的是，本节重点在于建立单子结构的局部降阶空间及其缩聚刚度；拼合多个独立子结构形函数所引起的全局位移协调问题将在第 3 节通过重叠有限元单位分解法解决。

## 2.1 经典子结构静力缩聚方法

子结构方法本质上是一种静力凝聚方法，其核心思想是消除每个子域内部的自由度，仅保留边界自由度参与全局方程求解；求得边界自由度后，再通过数值基函数反求子结构内部位移。若完整保留子结构的全部边界自由度，该凝聚过程在离散代数方程层面上不存在额外截断误差，与原细网格系统严格等价。

![[Guo2026_OFEM_Fig1.png]]

<center><b>
图 1：经典子结构静力缩聚。(a) 分析域划分为子结构；(b) 节点自由度划分为内部集与边界集；(c) 基于角节点自由度对子结构边界位移进行线性插值。
</b></center>

在线弹性、微小变形有限元框架下，如图 1(a) 所示，将分析域剖分为若干子结构 $\Omega^j$（$j = 1, \dots, N$）。每个子结构内部的静力平衡方程可独立写为：

$$
\mathbf{K}^j \boldsymbol{u}^j = \boldsymbol{f}^j,
\tag{1}
$$

其中 $\mathbf{K}^j$ 为子结构刚度矩阵，$\boldsymbol{u}^j$ 和 $\boldsymbol{f}^j$ 分别为子结构细网格位移向量与载荷向量。如图 1(b) 所示，将节点分为内部节点（下标 $i$）和边界节点（下标 $b$），方程 (1) 分块重写为：

$$
\mathbf{K}^j \boldsymbol{u}^j =
\begin{bmatrix}
\mathbf{K}_{bb}^j & (\mathbf{K}_{ib}^j)^{\mathsf T} \\
\mathbf{K}_{ib}^j & \mathbf{K}_{ii}^j
\end{bmatrix}
\begin{Bmatrix}
\boldsymbol{u}_b^j \\
\boldsymbol{u}_i^j
\end{Bmatrix}
=
\begin{Bmatrix}
\boldsymbol{f}_b^j \\
\boldsymbol{f}_i^j
\end{Bmatrix}.
\tag{2}
$$

假设子结构内部节点不承受外载荷（$\boldsymbol{f}_i^j = \boldsymbol{0}$，存在内部载荷的情况见文献 [37]），由第二行可得内部位移与边界位移的解析关系：

$$
\boldsymbol{u}_i^j = -(\mathbf{K}_{ii}^j)^{-1} \mathbf{K}_{ib}^j \boldsymbol{u}_b^j.
\tag{3}
$$

代回式 (2) 第一行，得到对应于边界位移 $\boldsymbol{u}_b^j$ 的缩聚刚度矩阵 $\mathbf{K}_s^j$：

$$
\mathbf{K}_s^j = \mathbf{K}_{bb}^j - (\mathbf{K}_{ib}^j)^{\mathsf T} (\mathbf{K}_{ii}^j)^{-1} \mathbf{K}_{ib}^j.
\tag{4}
$$

将各子结构缩聚刚度矩阵装配为全局缩聚方程：

$$
\mathbf{K}_s \boldsymbol{u}_b = \boldsymbol{f}_b,
\tag{5}
$$

其中 $\mathbf{K}_s = \sum_{j=1}^N (\mathbf{G}^j)^{\mathsf T} \mathbf{K}_s^j \mathbf{G}^j$，$\mathbf{G}^j$ 为子结构装配定位矩阵，$\boldsymbol{f}_b = \sum_{j=1}^N \mathbf{G}^j \boldsymbol{f}_b^j$。解出 $\boldsymbol{u}_b$ 后，代入式 (3) 即可恢复各子结构内部位移。

由式 (3) 可知内部节点位移与边界位移之间存在线性映射，可表示为数值基函数矩阵形式：

$$
\boldsymbol{u}_i^j = \mathbf{N}_s^j \boldsymbol{u}_b^j,
\tag{6}
$$

其中 $\mathbf{N}_s^j = -(\mathbf{K}_{ii}^j)^{-1} \mathbf{K}_{ib}^j \in \mathbb{R}^{n_i \times n_b}$ 为多尺度数值基函数矩阵。将内部与边界自由度合并后，子结构全部节点位移可表达为：

$$
\boldsymbol{u}^j =
\begin{bmatrix}
\boldsymbol{u}_i^j \\
\boldsymbol{u}_b^j
\end{bmatrix}
=
\begin{bmatrix}
\mathbf{N}_s^j \\
\mathbf{I}
\end{bmatrix}
\boldsymbol{u}_b^j = \mathbf{N}^j \boldsymbol{u}_b^j,
\tag{7}
$$

其中 $\mathbf{I} \in \mathbb{R}^{n_b \times n_b}$ 为单位矩阵，$\mathbf{N}^j$ 将边界自由度映射为子结构全体自由度。缩聚刚度矩阵亦可对称表示为 [29]：

$$
\mathbf{K}_s^j = (\mathbf{N}^j)^{\mathsf T} \mathbf{K}^j \mathbf{N}^j.
\tag{8}
$$

在大规模分析中，若保留全部边界自由度，缩聚系统依然较大。常规作法是仅保留 4 个角节点自由度，并假设边界位移沿边呈线性插值（图 1(c)）：

$$
\tilde{\mathbf{K}}_s^j = (\mathbf{N}^j \mathbf{L})^{\mathsf T} \mathbf{K}^j (\mathbf{N}^j \mathbf{L}) \triangleq (\tilde{\mathbf{N}}^j)^{\mathsf T} \mathbf{K}^j \tilde{\mathbf{N}}^j,
\tag{9}
$$

其中 $\tilde{\mathbf{N}}^j = \mathbf{N}^j \mathbf{L}$ 为将角节点位移插值为全部节点位移的形函数。

## 2.2 超采样数值基函数的构造与边界处理

在线性边界假定下，由于低阶多项式无法捕捉非均匀材料引起的边界位移高频振荡，必然引入边界层截断误差。为此，本文引入**超采样技术**：不在目标子结构边界上直接施加线性位移假定，而是在覆盖目标子结构的扩展区域内求解局部边值问题，并将求得的位移基向量限制到目标子结构上，使目标边界位移自然反映材料非均匀性。

![[Guo2026_OFEM_Fig2.png]]

<center><b>
图 2：目标子结构 $\Omega_{\mathrm{sub}}^j$ 及其对应的超采样域 $\Omega_{\mathrm{os}}^j$。
</b></center>

如图 2 所示，设目标子结构 $\Omega_{\mathrm{sub}}^j$（红色区域）包含 $m \times m$ 个细单元，外围向各边扩展 $l$ 层细单元形成超采样域 $\Omega_{\mathrm{os}}^j$（绿色区域），总尺寸为 $(m + 2l) \times (m + 2l)$ 个细单元。

目标是仅用 4 个角节点的 8 个位移自由度表征 $\Omega_{\mathrm{sub}}^j$ 内的全部节点位移，且不预设 $\partial\Omega_{\mathrm{sub}}^j$ 上的线性或高阶插值形式。构造步骤如下：

![[Guo2026_OFEM_Fig3.png]]

<center><b>
图 3：施加在超采样域外部边界上用于求解 $\boldsymbol{\psi}_x^{1'}$ 的位移边界条件示意图。
</b></center>

1. **超采样外部边界条件施加**：将超采样域 $\Omega_{\mathrm{os}}^j$ 的 4 个外部角节点标记为 $1', 2', 3', 4'$。如图 3 所示，以角点 $1'$ 的 $x$ 方向自由度为例，置其位移为 1，其余 7 个外部角点自由度置 0；在超采样域外边界四条边上进行线性插值作为弹性力学局部边值问题的 Dirichlet 边界条件；
2. **求解辅助局部边值问题**：在 $\Omega_{\mathrm{os}}^j$ 上求解有限元方程，获得对应的位移解向量 $\boldsymbol{\psi}_x^{1'} \in \mathbb{R}^{2(m+2l+1)^2}$。对所有 8 个外角点自由度依次求解，得到 8 个辅助基向量 $\boldsymbol{\psi}_x^{1'}, \boldsymbol{\psi}_y^{1'}, \dots, \boldsymbol{\psi}_x^{4'}, \boldsymbol{\psi}_y^{4'}$；
3. **限制截断至目标子结构**：从各辅助基向量中提取属于目标子结构 $\Omega_{\mathrm{sub}}^j$ 内部及边界节点的元素，获得目标子结构位移基向量 $\boldsymbol{\varphi}_x^{j'} \in \mathbb{R}^{2(m+1)^2}$（$j' = 1, 2, 3, 4$）。将 8 个基向量按列拼装成初始基函数矩阵：

$$
\boldsymbol{\Phi} = \left[ \boldsymbol{\varphi}_x^{1'}, \boldsymbol{\varphi}_y^{1'}, \boldsymbol{\varphi}_x^{2'}, \boldsymbol{\varphi}_y^{2'}, \boldsymbol{\varphi}_x^{3'}, \boldsymbol{\varphi}_y^{3'}, \boldsymbol{\varphi}_x^{4'}, \boldsymbol{\varphi}_y^{4'} \right] = [\boldsymbol{\phi}_1, \dots, \boldsymbol{\phi}_8] \in \mathbb{R}^{2(m+1)^2 \times 8};
\tag{10}
$$

4. **Kronecker-$\delta$ 归一化正交变换**：定义行提取算子 $\mathcal{M}$，提取 $\boldsymbol{\Phi}$ 中对应于目标子结构 4 个实际角节点的 8 个自由度行，得方阵 $\mathbf{T} = \mathcal{M}(\boldsymbol{\Phi}) \in \mathbb{R}^{8 \times 8}$。由于 $\mathbf{T} \neq \mathbf{I}$，破坏了形函数在角节点处的插值特性。为此引入组合系数矩阵 $\mathbf{C} = (C_{ij}) \in \mathbb{R}^{8 \times 8}$ 进行线性组合：

$$
\tilde{\boldsymbol{\phi}}_i = \sum_{j=1}^8 C_{ji} \boldsymbol{\phi}_j, \quad \tilde{\boldsymbol{\Phi}} = [\tilde{\boldsymbol{\phi}}_1, \dots, \tilde{\boldsymbol{\phi}}_8] = \boldsymbol{\Phi} \mathbf{C},
\tag{11-12}
$$

要求 $\tilde{\boldsymbol{\Phi}}$ 在角节点处严格满足 Kronecker-$\delta$ 属性：

$$
\mathcal{M}(\tilde{\boldsymbol{\Phi}}) = \mathcal{M}(\boldsymbol{\Phi} \mathbf{C}) = \mathbf{T} \mathbf{C} = \mathbf{I}_{8 \times 8} \implies \mathbf{C} = \mathbf{T}^{-1}.
\tag{13-14}
$$

由此得到满足角节点精确插值性质的超采样数值基函数矩阵：

$$
\tilde{\boldsymbol{\Phi}} = \boldsymbol{\Phi} \mathbf{T}^{-1} = \boldsymbol{\Phi} (\mathcal{M}(\boldsymbol{\Phi}))^{-1}.
\tag{15}
$$

子结构细网格位移即可由 8 个角节点位移 $\boldsymbol{u}_c^j$ 表达：

$$
\boldsymbol{u}^j = \tilde{\boldsymbol{\Phi}}^j \boldsymbol{u}_c^j.
\tag{16}
$$

子结构应变能及局部投影缩聚刚度矩阵为：

$$
W^j = \frac{1}{2} (\boldsymbol{u}^j)^{\mathsf T} \mathbf{K}^j \boldsymbol{u}^j = \frac{1}{2} (\boldsymbol{u}_c^j)^{\mathsf T} \mathbf{K}_r^j \boldsymbol{u}_c^j,
\tag{17}
$$

$$
\mathbf{K}_r^j = (\tilde{\boldsymbol{\Phi}}^j)^{\mathsf T} \mathbf{K}^j \tilde{\boldsymbol{\Phi}}^j.
\tag{18}
$$

![[Guo2026_OFEM_Fig4.png]]

<center><b>
图 4：超出物理结构边界的超采样域处理策略。(a) 边界邻近子结构的分类；(b) 跨固定端边界的镜像延拓；(c) 跨自由边界的弱材料延拓。
</b></center>

对于靠近宏观结构外边界 $\partial\Omega$ 的子结构，超采样层会凸出结构外部。如图 4 所示，本文采取分类延拓策略：
- **自由边界**：外延区域单元赋予弱材料弹性模量；
- **固定约束边界（Dirichlet 边界）**：采用镜像对称延拓，即外延点 $\boldsymbol{x}$ 处的虚拟模量取其在物理域内的镜像点模量：$\boldsymbol{E}_{\mathrm{vir}}(\boldsymbol{x}) = \boldsymbol{E}(\mathcal{R}_\Gamma(\boldsymbol{x}))$。该延拓仅用于构造局部基函数，全局求解时仍严格施加真实的宏观边界条件。

---

# 3 基于单位分解重叠有限元的位移协调方法

式 (16) 在单子结构内部构造了高保真位移场，但由于相邻子结构的超采样基函数是独立求解的，在共享边界上除角节点外必然产生位移跳跃：

$$
\boldsymbol{u}^{j_1}(\boldsymbol{x}) \neq \boldsymbol{u}^{j_2}(\boldsymbol{x}), \quad \boldsymbol{x} \in (\partial\Omega_{\mathrm{sub}}^{j_1} \cap \partial\Omega_{\mathrm{sub}}^{j_2}) \setminus \Omega_c^{j_1 j_2},
\tag{21}
$$

导致应变场出现虚假跳跃和灵敏度失真。本节引入单位分解重叠有限元机制，将独立的局部降阶场无缝缝合为全局连续位移场。

## 3.1 子结构的重叠覆盖与细网格构造

若直接让均匀网格的子结构相互重叠非整数个单元（如重叠 $h/2$），会将交界区切割为非均匀的微小碎片单元（图 5），增加单元类型与装配难度。

![[Guo2026_OFEM_Fig5.png]]

<center><b>
图 5：直接重叠均匀离散子结构产生的非均匀全局网格。(a) 具有局部均匀细网格的 9 个子结构；(b) 9 个子结构直接叠加；(c) 所产生的非均匀积分网格。
</b></center>

![[Guo2026_OFEM_Fig6.png]]

<center><b>
图 6：以特定非均匀细单元替换组成子结构的均匀细单元示意图。
</b></center>

为此，本文设计了一种特殊的子结构内部非均匀网格划分（图 6）：在需要与邻居重叠的边上，最外层边界细单元在垂直重叠带方向由 $h \times h$ 扩展为 $2h \times h$；在角点处双向扩展为 $2h \times 2h$。当相邻子结构以宽度 $h$ 相互重叠时，重叠后的全局网格依然拼装为**全局完全均匀的 $h \times h$ 笛卡尔网格**！

<center><b>
表 1：重叠子结构中的局部单元分类。
</b></center>

| 单元类别 | 几何尺寸 | 在子结构中的位置 |
|---|---|---|
| **内部细单元** | $h \times h$ | 子结构内部 $(m-4) \times (m-4)$ 区域（图 6 白色单元） |
| **边缘扩展单元** | $2h \times h$ 或 $h \times 2h$ | 重叠边界边，不含两端角元（图 6 蓝色单元） |
| **角部扩展单元** | $2h \times 2h$ | 两条正交重叠带的交汇角隅（图 6 绿色单元） |

根据子结构在宏观矩形排列中的相对位置，子结构被划分为 9 种拓扑类型，如表 2 和图 7 所示。图 8 展示了 9 种类型各取一个组成的 $3 \times 3$ 排列，其叠加后精确复原为标准均匀笛卡尔网格。

<center><b>
表 2：矩形排列中的 9 类子结构拓扑。
</b></center>

| 类别编号 | 拓扑类型 | 与相邻子结构的重叠方向 | 数量 |
|---|---|---|---|
| Type 1 | 左上角（Up Left Corner） | 下、右 | 1 |
| Type 2 | 上边界（Up） | 下、左、右 | $n_{\mathrm{slx}} - 2$ |
| Type 3 | 右上角（Up Right Corner） | 下、左 | 1 |
| Type 4 | 左边界（Left） | 上、下、右 | $n_{\mathrm{sly}} - 2$ |
| Type 5 | 内部（Internal） | 上、下、左、右 | $(n_{\mathrm{slx}} - 2) \times (n_{\mathrm{sly}} - 2)$ |
| Type 6 | 右边界（Right） | 上、下、左 | $n_{\mathrm{sly}} - 2$ |
| Type 7 | 左下角（Bottom Left Corner） | 上、右 | 1 |
| Type 8 | 下边界（Bottom） | 上、左、右 | $n_{\mathrm{slx}} - 2$ |
| Type 9 | 右下角（Bottom Right Corner） | 上、左 | 1 |

![[Guo2026_OFEM_Fig7.png]]

<center><b>
图 7：9 种不同拓扑类型的子结构示意图。
</b></center>

![[Guo2026_OFEM_Fig8.png]]

<center><b>
图 8：包含每类子结构各一个代表的 $3 \times 3$ 排列；其叠加生成完全均匀的笛卡尔细网格。(a) 9 个子结构的重叠；(b) 生成的均匀笛卡尔细网格。
</b></center>

## 3.2 基于重叠有限元的位移协调

设局部单元总数为 $N_e$。定义在局部单元 $\Omega_l$ 上的权函数 $\omega_l(\boldsymbol{x})$ 需满足单位分解性质：非负、在 $\Omega_l$ 外部为 0，且在全域处处满足 $\sum_{l=1}^{N_e} \omega_l(\boldsymbol{x}) = 1$。

定义局部单元上的辅助函数：

$$
P_l(\boldsymbol{x}) = \sum_r h_r^l(\boldsymbol{x}) p_r^l,
\tag{22}
$$

其中 $h_r^l(\boldsymbol{x})$ 为标准 Q4 形函数，$p_r^l$ 为节点标记值（若节点处于与其它单元共享的重叠交界外边缘上则取 0，否则取 1，见图 9）。归一化权函数定义为：

$$
w_l(\boldsymbol{x}) = \frac{P_l(\boldsymbol{x})}{\sum_l P_l(\boldsymbol{x})}.
\tag{23}
$$

![[Guo2026_OFEM_Fig9.png]]

<center><b>
图 9：两个 $h \times 2h$ 单元在 $x$ 方向重叠示意图，灰色区域表示重叠部分。(a) 子结构 I 与 II 边界上的单元 A 和单元 B；(b) 重叠时单元 A 与 B 相互覆盖的位置；(c) 对应节点的标记值 $p_r^l$（绿色数字表示自由度全局编号）。
</b></center>

设局部单元位移场由标准 Q4 等参插值给出：$\boldsymbol{u}_l(\boldsymbol{x}) = \mathbf{H}_l(\boldsymbol{x}) \boldsymbol{q}_l$。全局协调位移场表示为加权和：

$$
\boldsymbol{u}_{\mathrm{global}}(\boldsymbol{x}) = \sum_{l=1}^{N_e} w_l(\boldsymbol{x}) \boldsymbol{u}_l(\boldsymbol{x}) = \sum_{l=1}^{N_e} w_l(\boldsymbol{x}) \mathbf{H}_l(\boldsymbol{x}) \boldsymbol{q}_l,
\tag{25}
$$

对应的应变场为：

$$
\boldsymbol{\varepsilon}(\boldsymbol{x}) = \sum_{l=1}^{N_e} \mathbf{B}_l(\boldsymbol{x}) \boldsymbol{q}_l, \quad
\mathbf{B}_l =
\begin{bmatrix}
\frac{\partial}{\partial x} & 0 \\
0 & \frac{\partial}{\partial y} \\
\frac{\partial}{\partial y} & \frac{\partial}{\partial x}
\end{bmatrix}
(w_l(\boldsymbol{x}) \mathbf{H}_l(\boldsymbol{x})).
\tag{26-27}
$$

重叠单元之间的耦合刚度仅存在于它们的公共重叠区域：

$$
\mathbf{K}_{\mathrm{global}}(\alpha, \beta) = \int_{\Omega_\alpha \cap \Omega_\beta} \mathbf{B}_\alpha^{\mathsf T} \mathbf{C} \mathbf{B}_\beta \,\mathrm{d}\Omega.
\tag{29}
$$

极为关键的是：由于最终积分域是严格均匀的笛卡尔 $h \times h$ 网格，根据同时覆盖该网格的子结构数量及相对位置，二维问题中的所有细单元可彻底归类为 **16 类标准细单元**（表 3 与图 10）。

<center><b>
表 3：细网格单元类型与覆盖子结构数量 $N_{\mathrm{OV}}$。
</b></center>

| 类型编号 $t$ | 覆盖子结构数 $N_{\mathrm{OV}}$ | 局部刚度块维度 | 所在空间位置 |
|---|---|---|---|
| **1** | 1 | $8 \times 8$ | 子结构内部未重叠的 $h \times h$ 细单元 |
| **2–5** | 1 | $8 \times 8$ | $x/y$ 方向边缘重叠区靠单侧子结构的一半（4 个子类） |
| **8–11** | 1 | $8 \times 8$ | 邻近角部重叠区靠单侧子结构的四分之一象限 |
| **6, 7, 12, 13, 14, 15** | 2 | $16 \times 16$ | 被两个子结构同时覆盖的边缘重叠带 |
| **16** | 4 | $32 \times 32$ | 被四个子结构同时覆盖的正交角隅重叠区 |

![[Guo2026_OFEM_Fig10.png]]

<center><b>
图 10：16 种细网格单元类型。(a) 16 类细单元图册；(b) 各类型在重叠笛卡尔网格中的空间分布位置。
</b></center>

对于每类单元，参考坐标系下的被积函数形式完全固定且独立于材料模量。因此，可使用 $3 \times 3$ Gauss 积分在**主循环开始前一次性离线计算 16 个单位杨氏模量刚度矩阵 $\mathbf{K}_0^t$ 并驻留内存**。在线装配时仅需对单元模量 $E_e$ 进行标量乘法缩放：

$$
\mathbf{K}_e = E_e \mathbf{K}_0^t,
\tag{30}
$$

使得重叠有限元的全局组装耗时与传统有限元保持完全相同的线性渐进复杂度！

## 3.3 超采样降阶映射与重叠有限元的耦合

在重叠有限元空间中，局部自由度 $\boldsymbol{q}_l$ 不再作为独立求解未知量，而是由所属子结构的角节点位移通过超采样矩阵 $\tilde{\boldsymbol{\Phi}}^j$ 与提取算子 $R_l$ 直接获得：

$$
\boldsymbol{u}_{\mathrm{global}}(\boldsymbol{x}) = \sum_l w_l(\boldsymbol{x}) \mathbf{H}_l(\boldsymbol{x}) \boldsymbol{q}_l, \quad \boldsymbol{q}_l = R_l(\tilde{\boldsymbol{\Phi}}^j \boldsymbol{u}_c^j).
\tag{31}
$$

全局降阶映射矩阵组装为 $\tilde{\boldsymbol{\Phi}}_{\mathrm{global}} = \bigvee_{j=1}^N \tilde{\boldsymbol{\Phi}}^j$。全局缩聚刚度矩阵由标准 Galerkin 投影生成：

$$
\mathbf{K}_{\mathrm{global}}^{c,\mathrm{OV}} = (\tilde{\boldsymbol{\Phi}}_{\mathrm{global}})^{\mathsf T} \mathbf{K}_{\mathrm{global}}^{\mathrm{OV}} \tilde{\boldsymbol{\Phi}}_{\mathrm{global}}.
\tag{33}
$$

在线求解极小维度的角节点方程 $\mathbf{K}_{\mathrm{global}}^{c,\mathrm{OV}} \boldsymbol{u}_c = \boldsymbol{f}_{\mathrm{eq}}$ 得到角点位移后，直接通过稀疏矩阵乘法恢复全局连续位移场，彻底消除了界面应变跳跃。

---

# 4 使用 U-Net 快速预测超采样数值基函数

在线逐个求解子结构超采样边值问题十分耗时。本节构建基于 U-Net 的数据驱动模型，直接学习从超采样区材料模量分布到局部超采样基函数的映射。

## 4.1 U-Net 网络结构

![[Guo2026_OFEM_Fig11.png]]

<center><b>
图 11：用于预测超采样数值基函数的 U-Net 深度神经网络架构。
</b></center>

对于内部包含 $m \times m$ 个细单元、外延 $l$ 层的子结构，超采样域网格规模为 $m_{\mathrm{os}} \times m_{\mathrm{os}}$（$m_{\mathrm{os}} = m + 2l$）。输入为单通道二维特征图——超采样弹性模量矩阵 $\boldsymbol{E}_{\mathrm{os}} \in \mathbb{R}^{m_{\mathrm{os}} \times m_{\mathrm{os}}}$。

网络输出经过刚体模态与角节点归一化硬约束后补全为完整基函数矩阵 $\boldsymbol{\Phi}_{\mathrm{ML}} \in \mathbb{R}^{n_s \times n_c}$。网络采用包含 3 级卷积下采样的 Encoder（ResBlock + GroupNorm + GELU）与对称 Decoder，末端 Bottleneck 具有大感受野以融合长程力学耦合特征，并通过跨层 Skip Connection 保留细观几何边缘（图 11）。为 9 类子结构分别独立训练 9 个 U-Net 模型。

## 4.2 训练数据与损失函数

对 $m=10, l=6$（$m_{\mathrm{os}} = 22$），离线随机生成 20,000 个非均匀材料样本（均匀分布 $E_{\mathrm{sample}} \sim \mathcal{U}[10^{-6}, 1]$），其中 19,000 个用于训练，1,000 个用于验证。

定义复合损失函数：

$$
L = \lambda_{\mathrm{data}} L_{\mathrm{data}} + \lambda_K L_K,
\tag{38}
$$

其中 $L_{\mathrm{data}}$ 为对局部异常样本鲁棒的 Smooth L1 损失；$L_K$ 为保证预测基函数具有力学能量保真度的**刚度保真度相对误差损失（Stiffness-fidelity error）**：

$$
L_K = \frac{\| (\tilde{\boldsymbol{\Phi}}_{\mathrm{ML}}^j)^{\mathsf T} \mathbf{K}_{\mathrm{loc}}^j \tilde{\boldsymbol{\Phi}}_{\mathrm{ML}}^j - (\tilde{\boldsymbol{\Phi}}^j)^{\mathsf T} \mathbf{K}_{\mathrm{loc}}^j \tilde{\boldsymbol{\Phi}}^j \|_F}{\| (\tilde{\boldsymbol{\Phi}}^j)^{\mathsf T} \mathbf{K}_{\mathrm{loc}}^j \tilde{\boldsymbol{\Phi}}^j \|_F + \varepsilon}.
\tag{39}
$$

训练采用 AdamW 优化器，初始学习率 $2 \times 10^{-4}$，配合余弦退火重启调度；前 50 个 epoch 仅使用数据项预热，之后启用刚度保真项（$\lambda_{\mathrm{data}} = 1.0, \lambda_K = 0.1$）。

## 4.3 训练结果

在一台 NVIDIA GeForce RTX 4090 GPU 上训练。验证集 MAE 在第 1 个 epoch 为 0.0897，至第 100 个 epoch 降至 0.0214，在第 897 个 epoch 触发早停机制。最终训练损失为 0.009496，验证损失为 0.006241，最优验证 MAE 为 0.016082（图 12）。

![[Guo2026_OFEM_Fig12.png]]

<center><b>
图 12：U-Net 模型的训练与验证收敛曲线。(a) 损失曲线；(b) 平均绝对误差（MAE）曲线。
</b></center>

## 4.4 在线预测与计算流程

在线阶段，若子结构超采样域模量极差 $<10^{-3}$，直接复用预先存储的均质模量形函数；非均质子结构按类型批量送入 U-Net 推理。求得角节点位移后，以恢复位移作为初始场，采用 Jacobi 预条件共轭梯度法（PCG）在全局细网格方程上执行 1~2 秒的残差极小步修正，使应变能与伴随灵敏度精度达到极致。

---

# 5 数值算例

所有算例均在一台配备 Intel Core i9-13900K CPU、NVIDIA RTX 4090 GPU 与 128 GB 内存的工作站上完成，平面应力状态，泊松比 $\nu = 0.3$。子结构尺寸取 $m=10$，超采样外延 $l=6$ 层。

## 5.1 误差指标

- **节点相对位移误差**：$\eta_u^\beta = \frac{\| \boldsymbol{u}_{\mathrm{est}}^\beta - \boldsymbol{u}_{\mathrm{ref}}^\beta \|_2}{\| \boldsymbol{u}_{\mathrm{ref}}^\beta \|_2 + 10^{-12}}$，全域平均为 $\bar{\eta}_u$；
- **单元应变能相对误差**：$\eta_{\mathrm{SE}}^e = \frac{| SE_{\mathrm{est}}^e - SE_{\mathrm{ref}}^e |}{| SE_{\mathrm{ref}}^e | + 10^{-12} \max_e |SE_{\mathrm{ref}}^e|}$。

## 5.2 悬臂梁算例

测试图 13 所示的 $2 \times 1$ 悬臂梁，右下角受集中荷载 $f=1$。

![[Guo2026_OFEM_Fig13.png]]

<center><b>
图 13：悬臂梁算例的几何与边界条件。
</b></center>

![[Guo2026_OFEM_Fig14.png]]

<center><b>
图 14：不同离散与降阶策略下的悬臂梁变形对比。(a) 经典细网格 FEM；(b) 基于线性边界位移假定的传统 PIML；(c) PIML-OFEM（划分为 $8 \times 4$ 重叠子结构）。
</b></center>

1. **均匀全实心结构**：对比显示传统线性边界 PIML 在子结构界面存在明显刚度过硬缺陷，而 PIML-OFEM 变形场与直接细网格 FEM 完全重合，界面处无任何位移跳跃或网格畸变（图 14）；
2. **双圆孔非均匀结构（1801×901 细网格）**：FEM 耗时 12.39 s，PIML-OFEM 仅耗时 2.64 s（线性求解仅 1.04 s），平均位移误差仅 $\bar{\eta}_u = 0.0140$，最大挠度预测为 70.97（参考值 71.30）（图 15(a)）；
3. **随机振荡模量结构（1801×901 细网格）**：在无空间相关性的极端高频扰动下，PIML-OFEM 耗时 5.83 s（FEM 为 13.80 s），位移误差保持在 0.0692（图 15(b)），证实了 U-Net 应对强非均匀扰动的鲁棒性。

![[Guo2026_OFEM_Fig15.png]]

<center><b>
图 15：非均匀悬臂梁算例中的位移预测结果与误差分布。(a) 双圆孔算例；(b) 随机杨氏模量算例。
</b></center>

## 5.3 复杂孔洞拓扑算例

考虑图 16 所示包含倾斜椭圆孔、圆孔与菱形孔的 $4 \times 1$ 复杂结构，右下角受垂直力，网格规模为 **3601×901（324 万单元）**。

![[Guo2026_OFEM_Fig16.png]]

<center><b>
图 16：复杂孔洞拓扑结构的材料分布与边界条件。
</b></center>

![[Guo2026_OFEM_Fig17.png]]

<center><b>
图 17：复杂孔洞拓扑结构在集中力作用下的力学分析结果。(a) 经典 FEM 位移云图；(b) PIML-OFEM 位移云图；(c) 绝对位移误差；(d) 相对位移误差；(e) 经典 FEM 单元应变能云图；(f) PIML-OFEM 单元应变能云图；(g) 单元应变能相对误差云图。
</b></center>

<center><b>
表 5.1：复杂孔洞算例中不同力学分析方法的计算效率与全域平均位移误差 $\bar{\eta}_u$ 对比。
</b></center>

| 分析方法 | 计算耗时 (s) | 全域平均位移误差 $\bar{\eta}_u$ |
|---|---|---|
| **经典直接 FEM** | 39.85 | —（参考基准） |
| **PIML-EMS-LBC（线性边界假定）** | 11.14 | 0.0199 |
| **PIML-OFEM（本文方法）** | **12.06** | **0.0066** |
| **OFEM-SUB（在线无 ML 超采样）** | 146.77 | 0.0046 |

由表 5.1 与图 17 可知：
- 基于线性边界的 PIML-EMS-LBC 无法反映孔洞附近的非线性位移畸变，误差达 0.0199；
- 本文 PIML-OFEM 将误差大幅降低 3 倍至 **0.0066**，最大挠度预测为 343.00（参考值 344.70），耗时仅 12.06 s；
- 在线精确求解超采样基函数的 OFEM-SUB 耗时高达 146.77 s，表明 U-Net 预测带来了超过 **12 倍的加速**；
- 实体区域单元应变能相对误差普遍低于 $8 \times 10^{-3}$（图 17(g)），为拓扑优化灵敏度计算提供了坚实保障。

## 5.4 拓扑优化算例

将 PIML-OFEM 嵌入标准 SIMP 流程，体积分数限值取 0.5。

1. **Michell 梁算例（3061×1531 细单元，约 470 万单元）**：
   采用小滤波半径 $r_{\min} \approx \sqrt{3}$ 细单元尺寸。如图 18 所示，PIML-OFEM 稳定收敛，成功呈现出具有丰富多尺度特征的分级承载网络，局部形态在定性上高度契合均质化理论给出的**类秩-2（Rank-2）微结构**特征（图 18(d)）。

![[Guo2026_OFEM_Fig18.png]]

<center><b>
图 18：Michell 梁拓扑优化问题。(a) 设计域与边界条件；(b) 文献 [49] 在 1600×800 网格下基于反均质化方法得到的结果；(c) 采用 PIML-OFEM 直接优化得到的结果（3061×1531 网格）；(d) 图 (c) 结构的局部微结构拓扑细节。
</b></center>

2. **悬臂梁高分辨率拓扑优化（3061×1531 细单元）**：
   传统线性边界子结构方法因界面数值误差，必须使用 $r_{\min} \geq 5$ 的强滤波维持数值稳定，抹杀了细微结构（图 19(a)）；而 PIML-OFEM 即使在 $r_{\min} = 2$ 和 $r_{\min} = \sqrt{3}$ 下依然极其稳定，单步分析仅需 33 s（直接 FEM 需 105 s），涌现出大量纤细的次级传力分支构型（图 19(b)–(c)）。

![[Guo2026_OFEM_Fig19.png]]

<center><b>
图 19：不同结构分析模型下的悬臂梁拓扑优化构型。(a) 传统线性边界位移假定子结构法（$r_{\min}=5$）；(b) PIML-OFEM（$r_{\min}=2$）；(c) PIML-OFEM（$r_{\min}=\sqrt{3}$）。
</b></center>

---

# 6 结论

针对大规模异质结构分析与高分辨率拓扑优化中计算效率与边界精度的固有矛盾，本文提出了基于问题无关机器学习的重叠有限元子结构分析框架（PIML-OFEM）：
1. **超采样数值基函数**摆脱了目标子结构边界位移的线性假定，二维问题仅保留 4 个角节点即可充分捕捉非均匀材料引起的局部高梯度响应；
2. **单位分解重叠有限元**在保证全局笛卡尔细网格规整性的同时，消除了独立子结构在共享边界上的位移跳跃，构建了能量弱协调的全局连续位移场；
3. **U-Net 局部算子学习**实现了问题无关的高保真基函数秒级批处理推理，结合离线单刚预积分，极大降低了在线求解耗时。

**未来研究展望**：
- 拓展至三维六面体结构、几何/材料非线性及结构动力学问题；
- 探索多尺度、变尺寸子结构的统一神经网络表征，结合后验误差估计实现局部自适应超采样与精确有限元重分析；
- 融合制造工艺约束与微结构多尺度并发优化。

---

# 利益冲突声明

所有作者声明不存在利益冲突。

# 作者贡献声明 (CRediT)

- **Yilin Guo**：方法学，调查研究，形式分析，验证，软件，数据审定，可视化，资金争取，论文撰写 – 初稿，论文撰写 – 审阅与编辑。
- **Chang Liu**：概念构思，方法学，调查研究，形式分析，资金争取，论文撰写 – 初稿，论文撰写 – 审阅与编辑。
- **Zongliang Du**：形式分析，验证，论文撰写 – 审阅与编辑。
- **Jin Liu**：软件。
- **Jingyu Feng**：软件。
- **Xinyang Zhang**：软件。
- **Yang Li**：软件。
- **Tianxing Yang**：软件。
- **Changyu Shen**：资源，指导，论文撰写 – 审阅与编辑。
- **Xu Guo**：概念构思，方法学，项目管理，资源，资金争取，指导，论文撰写 – 审阅与编辑。

# 致谢

本研究得到辽宁省科技重大专项（No. 2024JH1/11700045）、国家自然科学基金（No. 124B2042, 12472344）和大连市科技人才创新支持计划（No. 2024RG001）的资助。

---

# 参考文献

[1] N. Aage, E. Andreassen, B. S. Lazarov, and O. Sigmund, Giga-voxel computational morphogenesis for structural design, Nature 550, 84 (2017). https://doi.org/10.1038/nature23911

[2] K. Duraisamy, G. Iaccarino, and H. Xiao, Turbulence Modeling in the Age of Data, Annu. Rev. Fluid Mech. 51, 357 (2019). https://doi.org/10.1146/annurev-fluid-010518-040547

[3] J. Hu, Z. Lu, and Y. Yang, Improving prediction of preferential concentration in particle-laden turbulence using the neural-network interpolation, Phys. Rev. Fluids 9, 034606 (2024). https://doi.org/10.1103/PhysRevFluids.9.034606

[4] Y. Wang, Z. Li, Z. Yuan, W. Peng, T. Liu, and J. Wang, Prediction of turbulent channel flow using Fourier neural operator-based machine-learning strategy, Phys. Rev. Fluids 9, 084604 (2024). https://doi.org/10.1103/PhysRevFluids.9.084604

[5] K. Guo, Z. Yang, C. H. Yu, and M. J. Buehler, Artificial intelligence and machine learning in design of mechanical materials, Mater. Horiz. 8, 1153 (2021). https://doi.org/10.1039/D0MH01451F

[6] H. Jin, E. Zhang, and H. D. Espinosa, Recent Advances and Applications of Machine Learning in Experimental Solid Mechanics: A Review, Appl. Mech. Rev. 75, 061001 (2023). https://doi.org/10.1115/1.4062966

[7] C. S. Ha, D. Yao, Z. Xu, C. Liu, H. Liu, D. Elkins, M. Kile, V. Deshpande, Z. Kong, M. Bauchy, and X. Zheng, Rapid inverse design of metamaterials based on prescribed mechanical behavior through machine learning, Nat. Commun. 14, 5765 (2023). https://doi.org/10.1038/s41467-023-40854-1

[8] S. Deshpande, J. Lengiewicz, and S. P. A. Bordas, Probabilistic deep learning for real-time large deformation simulations, Comput. Methods Appl. Mech. Eng. 398, 115307 (2022). https://doi.org/10.1016/j.cma.2022.115307

[9] L. Sun, H. Gao, S. Pan, and J. X. Wang, Surrogate modeling for fluid flows based on physics-constrained deep learning without simulation data, Comput. Methods Appl. Mech. Eng. 361, 112732 (2020). https://doi.org/10.1016/j.cma.2019.112732

[10] P. T. Nguyen, Y. Heider, D. M. Kochmann, and F. Aldakheel, Deep learning-aided inverse design of porous metamaterials, Comput. Methods Appl. Mech. Eng. 449, 118499 (2026). https://doi.org/10.1016/j.cma.2025.118499

[11] X. Lei, C. Liu, Z. Du, W. Zhang, and X. Guo, Machine Learning-Driven Real-Time Topology Optimization Under Moving Morphable Component-Based Framework, J. Appl. Mech. 86, 011004 (2019). https://doi.org/10.1115/1.4041319

[12] D. Geng, J. Yan, Q. Xu, Q. Zhang, M. Zhou, Z. Fan, and H. Li, Real-Time structure topology optimization using CNN driven Moving Morphable component method, Eng. Struct. 290, 116376 (2023). https://doi.org/10.1016/j.engstruct.2023.116376

[13] S. Cai, Z. Mao, Z. Wang, M. Yin, and G. E. Karniadakis, Physics-informed neural networks (PINNs) for fluid mechanics: a review, Acta Mech. Sin. 37, 1727 (2021). https://doi.org/10.1007/s10409-021-01148-1

[14] G. E. Karniadakis, I. G. Kevrekidis, L. Lu, P. Perdikaris, S. Wang, and L. Yang, Physics-informed machine learning, Nat. Rev. Phys. 3, 422 (2021). https://doi.org/10.1038/s42254-021-00314-5

[15] J. Song, W. Cao, F. Liao, and W. Zhang, VW-PINNs: A volume weighting method for PDE residuals in physics-informed neural networks, Acta Mech. Sin. 41, 324140 (2025). https://doi.org/10.1007/s10409-024-24140-x

[16] L. Lu, P. Jin, G. Pang, Z. Zhang, and G. E. Karniadakis, Learning nonlinear operators via DeepONet based on the universal approximation theorem of operators, Nat. Mach. Intell. 3, 218 (2021). https://doi.org/10.1038/s42256-021-00302-5

[17] L. Lu, X. Meng, Z. Mao, and G. E. Karniadakis, DeepXDE: A Deep Learning Library for Solving Differential Equations, SIAM Rev. 63, 208 (2021). https://doi.org/10.1137/19M1274067

[18] L. Lu, R. Pestourie, W. Yao, Z. Wang, F. Verdugo, and S. G. Johnson, Physics-Informed Neural Networks with Hard Constraints for Inverse Design, SIAM J. Sci. Comput. 43, B1105 (2021). https://doi.org/10.1137/21M1397908

[19] S. Saha, Z. Gan, L. Cheng, J. Gao, O. L. Kafka, X. Xie, H. Li, M. Tajdari, H. A. Kim, and W. K. Liu, Hierarchical Deep Learning Neural Network (HiDeNN): An artificial intelligence (AI) framework for computational science and engineering, Comput. Methods Appl. Mech. Eng. 373, 113452 (2021). https://doi.org/10.1016/j.cma.2020.113452

[20] L. Zhang, Y. Lu, S. Tang, and W. K. Liu, HiDeNN-TD: Reduced-order hierarchical deep learning neural networks, Comput. Methods Appl. Mech. Eng. 389, 114414 (2022). https://doi.org/10.1016/j.cma.2021.114414

[21] H. Li, S. Knapik, Y. Li, C. Park, J. Guo, S. Mojumder, Y. Lu, W. Chen, D. W. Apley, and W. K. Liu, Convolution Hierarchical Deep-Learning Neural Network Tensor Decomposition (C-HiDeNN-TD) for high-resolution topology optimization, Comput. Mech. 72, 363 (2023). https://doi.org/10.1007/s00466-023-02333-8

[22] Y. Lu, H. Li, L. Zhang, C. Park, S. Mojumder, S. Knapik, Z. Sang, S. Tang, D. W. Apley, G. J. Wagner, and W. K. Liu, Convolution Hierarchical Deep-learning Neural Networks (C-HiDeNN): finite elements, isogeometric analysis, tensor decomposition, and beyond, Comput. Mech. 72, 333 (2023). https://doi.org/10.1007/s00466-023-02336-5

[23] P. Ramuhalli, L. Udpa, and S. S. Udpa, Finite-Element Neural Networks for Solving Differential Equations, IEEE Trans. Neural Netw. 16, 1381 (2005). https://doi.org/10.1109/TNN.2005.857945

[24] C. Wu, C. Liu, Y. Guo, and X. Guo, DFENN: A penalty-free variational framework coupling finite elements and neural networks via interface condensation, J. Mech. Phys. Solids 215, 106703 (2026). https://doi.org/10.1016/j.jmps.2026.106703

[25] F. V. Senhora, H. Chi, Y. Zhang, L. Mirabella, T. L. E. Tang, and G. H. Paulino, Machine learning for topology optimization: Physics-based learning through an independent training strategy, Comput. Methods Appl. Mech. Eng. 398, 115116 (2022). https://doi.org/10.1016/j.cma.2022.115116

[26] H. Chi, Y. Zhang, T. L. E. Tang, L. Mirabella, L. Dalloro, L. Song, and G. H. Paulino, Universal machine learning for topology optimization, Comput. Methods Appl. Mech. Eng. 375, 112739 (2021). https://doi.org/10.1016/j.cma.2019.112739

[27] M. Huang, Z. Du, C. Liu, Y. Zheng, T. Cui, Y. Mei, X. Li, X. Zhang, and X. Guo, Problem-independent machine learning (PIML)-based topology optimization—A universal approach, Extreme Mech. Lett. 56, 101887 (2022). https://doi.org/10.1016/j.eml.2022.101887

[28] M. Huang, T. Cui, C. Liu, Z. Du, J. Zhang, C. He, and X. Guo, A Problem-Independent Machine Learning (PIML) enhanced substructure-based approach for large-scale structural analysis and topology optimization of linear elastic structures, Extreme Mech. Lett. 63, 102041 (2023). https://doi.org/10.1016/j.eml.2023.102041

[29] M. Huang, C. Liu, Y. Guo, L. Zhang, Z. Du, and X. Guo, A mechanics-based data-free Problem Independent Machine Learning (PIML) model for large-scale structural analysis and design optimization, J. Mech. Phys. Solids 193, 105893 (2024). https://doi.org/10.1016/j.jmps.2024.105893

[30] Y. Guo, Z. Du, C. Liu, W. Zhang, S. Tang, W. Hao, Z. Zhao, C. Wu, Z. Xu, T. Bian, Z. Dai, Z. Yang, W. Huo, C. Shen, and X. Guo, AI-enhanced and data-driven mechanical analysis and structural topology optimization, Sci. China Technol. Sci. (2026). https://doi.org/10.1007/s11431-026-3336-9

[31] R. R. Craig Jr. and M. C. C. Bampton, Coupling of substructures for dynamic analyses, AIAA J. 6, 1313 (1968). https://doi.org/10.2514/3.4741

[32] J. A. Gutierrez and A. K. Chopra, A substructure method for earthquake analysis of structures including structure‐soil interaction, Earthq. Eng. Struct. Dyn. 6, 51 (1978). https://doi.org/10.1002/eqe.4290060107

[33] X. Ma, M. Huang, Z. Du, Y. Guo, C. Liu, Y. Mei, and X. Guo, A high-performance parallel algorithm based on problem independent machine learning (PIML) for large-scale topology optimization, Acta Mech. Sin. 42, 425942 (2026). https://doi.org/10.1007/s10409-025-25942-x

[34] C. Liu, W. Xu, W. Huo, Y. Guo, and X. Guo, Surface lattice structure design via computational conformal mapping and structural optimization, Comput. Methods Appl. Mech. Eng. 451, 118680 (2026). https://doi.org/10.1016/j.cma.2025.118680

[35] X. Cao, W. Xu, S. Zhao, Y. Guo, C. Liu, and X. Guo, Design of 3D Shell-Graded Infill Structures Based on Moving Morphable Void and Triply Periodic Minimal Surfaces, In: X. Feng and K. Zhou (eds.), Computational and Experimental Simulations in Engineering: Proceedings of ICCES 2025, Vol. 4, Mechanisms and Machine Science, Vol. 201, Springer, Cham, 841-852 (2026). https://doi.org/10.1007/978-3-032-17313-3_64

[36] L. Zhang, M. Huang, C. Liu, Z. Du, T. Cui, and X. Guo, Problem-independent machine learning-enhanced structural topology optimization of complex design domains based on isoparametric elements, Extreme Mech. Lett. 72, 102237 (2024). https://doi.org/10.1016/j.eml.2024.102237

[37] Y. Guo, C. Liu, Z. Du, Y. Jia, C. Jiang, X. Guo, and C. Shen, High-Generalization AI-Enhanced mechanical analysis and topology optimization via cubic bézier interpolation of substructure boundary displacements, Comput. Methods Appl. Mech. Eng. 456, 118955 (2026). https://doi.org/10.1016/j.cma.2026.118955

[38] H. W. Zhang, Y. Liu, S. Zhang, J. Tao, J. K. Wu, and B. S. Chen, Extended multiscale finite element method: its basis and applications for mechanical analysis of heterogeneous materials, Comput. Mech. 53, 659 (2014). https://doi.org/10.1007/s00466-013-0924-x

[39] H. W. Zhang, J. K. Wu, J. Lü, and Z. D. Fu, Extended multiscale finite element method for mechanical analysis of heterogeneous materials, Acta Mech. Sin. 26, 899 (2010). https://doi.org/10.1007/s10409-010-0393-9

[40] K. J. Bathe and L. Zhang, The finite element method with overlapping elements – A new paradigm for CAD driven simulations, Comput. Struct. 182, 526 (2017). https://doi.org/10.1016/j.compstruc.2016.10.020

[41] W. L. Nicomedes and K. J. Bathe, An effective overlapping finite element for three-dimensional incompressible linear elasticity, Comput. Methods Appl. Mech. Eng. 457, 118613 (2026). https://doi.org/10.1016/j.cma.2025.118613

[42] W. L. Nicomedes, K. J. Bathe, F. J. S. Moreira, and R. C. Mesquita, Overlapping finite elements for the Navier-Stokes equations, Comput. Struct. 299, 107343 (2024). https://doi.org/10.1016/j.compstruc.2024.107343

[43] S. Lee and K. J. Bathe, An enhancement of overlapping finite elements, Comput. Struct. 260, 106704 (2022). https://doi.org/10.1016/j.compstruc.2021.106704

[44] J. Huang and K. J. Bathe, On the convergence of overlapping elements and overlapping meshes, Comput. Struct. 244, 106429 (2021). https://doi.org/10.1016/j.compstruc.2020.106429

[45] J. Huang and K. J. Bathe, Overlapping finite element meshes in AMORE, Adv. Eng. Softw. 144, 102791 (2020). https://doi.org/10.1016/j.advengsoft.2020.102791

[46] J. Huang and K. J. Bathe, Quadrilateral overlapping elements and their use in the AMORE paradigm, Comput. Struct. 222, 25 (2019). https://doi.org/10.1016/j.compstruc.2019.05.011

[47] L. Zhang, K. T. Kim, and K. J. Bathe, The new paradigm of finite element solutions with overlapping elements in CAD – Computational efficiency of the procedure, Comput. Struct. 199, 1 (2018). https://doi.org/10.1016/j.compstruc.2018.01.003

[48] L. Zhang and K. J. Bathe, Overlapping finite elements for a new paradigm of solution, Comput. Struct. 187, 64 (2017). https://doi.org/10.1016/j.compstruc.2017.03.008

[49] J. P. Groen and O. Sigmund, Homogenization-based topology optimization for high-resolution manufacturable microstructures, Int. J. Numer. Methods Eng. 113, 1148 (2018). https://doi.org/10.1002/nme.5575
