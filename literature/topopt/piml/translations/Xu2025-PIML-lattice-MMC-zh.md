---
title: "翻译：Problem-Independent Machine Learning (PIML) enhanced 3D lattice composite structures optimization via moving morphable components approach"
tags:
  - translation
  - PIML
  - topology-opt
  - substructure
  - MMC
  - lattice
status: "done"
date_created: 2026-08-04
date_updated: 2026-09-10
source: "../sources/Xu2025-PIML-lattice-MMC.pdf"
citekey: "xuProblemindependentMachineLearning2025"
language: "zh-CN"
---

# Problem-Independent Machine Learning (PIML) enhanced 3D lattice composite structures optimization via moving morphable components approach

---

# 信息

- **中文标题**：基于移动可变形构件法的问题无关机器学习增强三维点阵复合结构优化
- **作者**：Wu Xu（徐武）$^1$；Chang Liu（刘畅）$^{1,2,*}$；Yilin Guo（郭一麟）$^1$；Mengcheng Huang（黄孟成）$^1$；Xu Guo（郭旭）$^{1,2,*}$
- **单位**：
  - $1$: 大连理工大学工程力学系、工业装备结构分析优化与 CAE 软件国家重点实验室、计算力学国际研究中心（大连 116023）
  - $2$: 大连理工大学宁波研究院（宁波 315016）
- **期刊**：*Composite Structures*
- **卷 / 期 / 文章号**：369: 119330
- **DOI**：10.1016/j.compstruct.2025.119330
- **收稿 / 修回 / 录用 / 在线发表**：2024-12-21 / 2025-05-07 / 2025-05-25 / 2025-05-27
- **通讯作者**：Chang Liu（c.liu@dlut.edu.cn）；Xu Guo（guoxu@dlut.edu.cn）

# 摘要

点阵结构凭借优异的力学性能，正在越来越多的工程领域中得到应用。本文提出一种基于移动可变形构件（MMC）方法的三维点阵结构设计与优化新方法，并引入机器学习技术以提高计算效率。该方法利用具有显式几何参数的构件描述空间变化的材料分布；同时，基于 B 样条（B-Spline）基函数建立分区坐标映射（PCM），实现点阵结构的梯度变化，使杆件厚度、单胞形状和局部取向均可调节，并保持结构的完全连通。

针对大规模有限元分析带来的计算挑战，本文采用问题无关机器学习（PIML）模型表征复杂结构的力学响应。数值结果表明，该方法能够在不同边界条件下生成相邻微结构之间拓扑过渡平滑的梯度点阵结构，并且与周期点阵结构相比，其承载能力得到显著提高。此外，PIML 方法显著提升了复杂点阵复合结构设计的计算效率，为机器学习在大规模结构优化中的进一步应用提供了有价值的思路。

**关键词**：三维点阵复合结构（3D lattice composite structure）；问题无关机器学习（Problem-Independent Machine Learning, PIML）；移动可变形构件法（Moving Morphable Components, MMC）；分区坐标映射（Partitioned Coordinate Mapping, PCM）；大规模拓扑优化（Large-scale topology optimization）

---

# 1 引言

点阵结构由一系列在三维空间中按特定模式排列且具有空间变化拓扑的互连单胞组成 [1, 2]。近年来，具有复杂微观几何形状的点阵结构因其优异的物理性能和多功能应用潜力吸引了广泛关注。这些应用包括轻量化飞行器与航天运载器设计 [3, 4]、能量吸收装置 [5, 6]、隔振系统 [7]、热交换机构 [8–10] 以及医用植入物 [11–13]。与均匀周期点阵或泡沫多孔结构相比，梯度点阵结构凭借单胞尺寸与空间取向的连续梯度变化展现出更为卓越的力学性能。这些梯度变化赋予了结构更高的设计柔度，可根据多功能需求进行定制设计。此外，增材制造（AM）技术的逐层堆叠成形能力解决了复杂微观几何形状的制造难题，为设计人员充分利用复杂点阵结构优化产品性能提供了前所未有的设计自由度 [14, 15]。

点阵结构的优异性能高度依赖于微观单胞拓扑，即材料在空间中的微观分布形态。拓扑优化（TO）是在给定设计空间内确定材料最优分布的有效数学方法。自 Bendsøe 和 Kikuchi 开创性工作 [16] 以来，过去几十年中发展了多种代表性方法，包括固体各向同性材料惩罚法（SIMP）[17, 18]、渐进结构优化法（ESO）[19, 20]、水平集方法 [21] 以及移动可变形构件/移动可变形空洞（MMC/MMV）方法 [22–24]。这些方法已被成功应用于各类工程结构设计，并在满足特定功能要求的点阵结构优化中得到了重点关注。

均质化方法在多尺度设计中应用广泛，因其分层列式在计算效率与精度之间实现了良好折中。Cheng 等 [25] 提出了一种利用渐近均质化确定等效应变能与相对密度关系的梯度点阵优化方法，并引入应力约束保证制造性。在相关平行研究中，Wang 等 [26]、Zhang 等 [27, 28] 和 Zhu 等 [29] 分别利用高阶多项式、Kriging 代理模型和人工神经网络（ANN）构建了等效力学性能与参数化微结构变量之间的拟合模型。通过离线对若干预设微结构进行迭代分析，大幅降低了多尺度拓扑优化的计算负担。然而，传统与坐标轴对齐的立方体单胞形态与周期排列限制了设计空间；为进一步提升承载能力，微结构的旋转自由度必须被纳入优化考量以主动适应局部主应力方向 [30]。

为此，Daynes 等 [31–33] 利用拓扑优化得到的主应变场和最优相对密度场，定制了梯度点阵中各桁架杆件尺寸、形状与取向的空间变化。Groen 等 [34, 35] 与 Allaire 等 [36, 37] 分别借助图像排序技术与间断 Galerkin 方法对均质化结果进行后处理，平滑了周期单胞的宏观取向。在 MMC/MMV 框架下，Liu 等 [38–40] 提出了具有天然平滑连通性保证的单胞分布优化方法，大幅减少了设计变量数。Wu 等 [41] 沿主应力方向布置内部杆件、沿外边界布置轮廓杆件，构建了与几何边界保形的共形点阵。Chen 等 [42] 发展了基于有限元网格的复杂共形点阵参数化建模方法；Zhao 等 [43] 提出了涵盖非均匀、共形及随机点阵的混合几何建模方法。近期，非均匀有理 B 样条（NURBS）超曲面被用于表征代表性体积单元（RVE）尺度与宏观尺度的材料伪密度场 [44]，在多材料点阵热力学多功能优化中展示了显著优势 [45–47]。

然而，上述全尺度分析优化问题的求解规模受到计算能力的严重制约。精确刻画非均匀材料分布必须依赖极其密集的细网格有限元剖分。尽管计算量巨大，单尺度全有限元分析在精细点阵设计中依然具备独特优势：第一，传统有限元能天然适应任意复杂自由曲面几何，而均质化方法在处理规则单胞与自由曲面边界的不匹配时极其困难，尤其是在包含实体外壳与点阵填充的复合结构中 [3, 39, 48–50]；第二，均质化方法固定的单胞几何（二维正方形、三维立方体）难以保证非均匀梯度点阵在相邻微结构间的几何协调与完全连通；第三，尺度分离假设在宏微观交界处容易产生非连通缺陷，需额外引入复杂的几何约束避免力学性能退化 [51]。

全尺度分析面临的决定性瓶颈是优化迭代过程中高昂的有限元分析成本。为此学者们探索了并行计算 [52–54]、多分辨率方法 [55, 56]、变量缩减 [22, 57] 和自由度消除技术 [58, 59]。近年来，结合人工智能与机器学习（ML）加速拓扑优化的研究迅速增加。其中一类流行方法是“端到端”直接预测最优拓扑以实现实时拓扑优化 [60–62]。但该类方法严重依赖训练集与目标问题在边界条件及分辨率上的相似度，一旦出现分布外（OOD）参数往往难以输出可靠结果，且高分辨率样本集的生成成本极其昂贵。

另一条极具潜力的路线是通过降低迭代分析开销来加速拓扑优化。Chi 等 [63] 提出了两尺度在线训练框架；随后引入带残差连接的卷积网络结合离线训练策略 [64]，在包含 3800 万变量的大规模问题中实现了最高 30 倍加速。更进一步，Huang 等提出了**问题无关机器学习（Problem-Independent Machine Learning, PIML）**框架 [65] 并拓展至三维线弹性分析 [66]。PIML 将设计域分解为子结构，通过离线机器学习建立子结构内部材料分布到多尺度数值形函数矩阵的确定性隐式映射，从而将全尺度有限元分析转化为规模显著缩减的子结构界面系统求解。由于 PIML 学习的是局部的力学算子表示，模型完全与宏观载荷、边界条件和宏观几何解耦，具有真正的“问题无关性”，已在多达 30 亿自由度的问题中展现了卓越的加速比与精度。此外，物理信息神经网络（PINN）[67]、深度能量法 [68] 及混合学习方法 [69] 也从不同角度为力学计算提供了新的思路。

基于上述背景，本文提出了一种在 MMC 框架下融合 PIML 加速的三维点阵增强复合结构拓扑优化方法：首先，基于周期复制函数（PRF）建立微观周期点阵的显式几何描述；其次，基于 B 样条基函数构建**分区坐标映射（PCM）**引入空间变形梯度场，将周期点阵平滑变换为梯度点阵结构，在保证相邻单胞天然光滑连通的前提下实现杆件厚度、单胞尺寸与局部取向的主动调节；最后，利用离线预训练的 PIML 模型预测子结构数值形函数，大幅削减大规模有限元分析开销。

本文其余部分组织如下：第 2 节介绍基于 MMC 与 PCM 的点阵结构几何描述；第 3 节阐述 PIML 增强的子结构高效分析方法及网络架构；第 4 节给出优化问题数学列式；第 5 节讨论有限元实现与解析灵敏度推导；第 6 节通过 MBB 梁、扭转箱及人体近端股骨填充等典型三维算例验证算法的有效性与加速比；第 7 节给出结论与展望。

---

# 2 基于 MMC 和 PCM 的点阵结构描述

本方法通过具有显式几何信息的构件简化点阵结构的参数化建模。首先回顾三维 MMC 方法的基本列式，进而阐述基于 MMC 的点阵显式几何表达与基于 B 样条 PCM 的可定制梯度点阵生成。

## 2.1 面向三维问题的 MMC 拓扑优化

三维 MMC 方法 [70] 旨在更直观、几何显式地求解拓扑优化问题。其基本设计基元为一组由几何参数驱动的移动可变形构件，通过优化构件的空间位置、倾角和尺寸来获得最优结构拓扑。

在 Eulerian 描述框架下，第 $i$ 个构件在设计域 $D$ 中所占据的实体材料区域 $\Omega_i^s$ 可由拓扑描述函数（TDF）表示为：

$$
\begin{cases}
\phi_i(\boldsymbol{x}) > 0, & \text{若 } \boldsymbol{x} \in \Omega_i^s, \\
\phi_i(\boldsymbol{x}) = 0, & \text{若 } \boldsymbol{x} \in \partial\Omega_i^s, \\
\phi_i(\boldsymbol{x}) < 0, & \text{若 } \boldsymbol{x} \in D \setminus (\Omega_i^s \cup \partial\Omega_i^s),
\end{cases}
\tag{1}
$$

其中 $\Omega_i^s \subset D$。为详细刻画构件的位置与几何特征，第 $i$ 个构件的 TDF $\phi_i(\boldsymbol{x})$ 可由其特征尺寸参数显式计算：

$$
\phi_i(\boldsymbol{x}) = 1 - \left[ \left(\frac{x'}{L_1^i}\right)^6 + \left(\frac{y'}{L_2^i}\right)^6 + \left(\frac{z'}{L_3^i}\right)^6 \right]^{\frac{1}{6}},
\tag{2}
$$

其中 $L_1^i, L_2^i, L_3^i$ 分别表示对应构件的半长、半宽与半高。虽然引入更多参数可描述构件的变截面轮廓，但后文引入的分区坐标映射（PCM）技术同样可以间接调节截面厚度，因此本文选用厚度均匀的长方体构件。如图 1 所示，定义位于第 $i$ 个构件几何中心的局部笛卡尔坐标系 $o-x'y'z'$。局部坐标与全局坐标 $O-xyz$ 的空间坐标变换关系为：

$$
\begin{bmatrix}
x' \\ y' \\ z'
\end{bmatrix}
= \mathbf{R}_i
\begin{bmatrix}
x - x_0^i \\ y - y_0^i \\ z - z_0^i
\end{bmatrix},
\tag{3a}
$$

$$
\mathbf{R}_i(\theta_1^i, \theta_2^i, \theta_3^i) =
\begin{bmatrix}
c_2 c_3 & -c_2 s_3 & s_2 \\
s_1 s_2 c_3 + c_1 s_3 & -s_1 s_2 s_3 + c_1 c_3 & -s_1 c_2 \\
-c_1 s_2 c_3 + s_1 s_3 & c_1 s_2 s_3 + s_1 c_3 & c_1 c_2
\end{bmatrix},
\tag{3b}
$$

其中 $s_1 = \sin\theta_1^i, s_2 = \sin\theta_2^i, s_3 = \sin\theta_3^i$，$c_1 = \sqrt{1 - s_1^2}, c_2 = \sqrt{1 - s_2^2}, c_3 = \sqrt{1 - s_3^2}$，$\theta_1^i, \theta_2^i, \theta_3^i$ 分别表示第 $i$ 个构件绕局部坐标轴的欧拉旋转角，$(x_0^i, y_0^i, z_0^i)^{\mathsf T}$ 表示构件中心点在全局坐标系中的坐标。

![[Xu2025_Fig1.png]]

<center><b>
图 1：全局笛卡尔坐标系（黑线）与局部坐标系（彩色线）中三维构件的几何描述。(a) 总览；(b)–(d) 全局坐标系旋转至局部坐标系的过程。
</b></center>

因此，每个构件由 9 个显式几何参数表征：$\boldsymbol{d}_i = (x_0^i, y_0^i, z_0^i, L_1^i, L_2^i, L_3^i, \theta_1^i, \theta_2^i, \theta_3^i)^{\mathsf T}$。获得各构件的 $\phi_i$ 后，整个结构的 TDF 可由所有 $n$ 个构件的极大值函数表示：$\phi_s = \max(\phi_1, \dots, \phi_n)$。为在灵敏度推导中保持可微性，本文采用 Kreisselmeier-Steinhauser (K-S) 函数 [71] 进行光滑近似：

$$
\phi_s = \frac{1}{\lambda} \ln\left( \sum_{i=1}^n \exp(\lambda \phi_i) \right),
\tag{4}
$$

其中 $\lambda$ 为充分大的正数，本文取 $\lambda = 100$。实体材料区域可表达为 $\Omega^s = \{ \boldsymbol{x} \mid \boldsymbol{x} \in D, \phi_s(\boldsymbol{x}) \geq 0 \}$。结构总设计变量向量记为 $\boldsymbol{d} = (\boldsymbol{d}_1^{\mathsf T}, \dots, \boldsymbol{d}_n^{\mathsf T})^{\mathsf T}$。

## 2.2 梯度点阵结构的显式几何描述

### 2.2.1 梯度点阵结构的拓扑描述函数生成

与周期点阵不同，梯度点阵结构的单胞在空间中不具备周期性，其尺寸、形状和空间取向随位置连续演变。本文的核心思想是引入参数化的显式变形场将周期点阵微观特征变换为梯度构型，具体分三步实现，如图 2 所示：

![[Xu2025_Fig2.png]]

<center><b>
图 2：所提出方法的渐进式显式几何描述流程。(a) 单个构件的 TDF；(b) 典型单胞（以面心立方 FCC 为例）；(c) 利用周期复制函数（PRF）生成的周期点阵；(d) 具有天然连通性与平滑空间变化的梯度点阵 TDF。
</b></center>

- **第一步：生成单胞基元（Prototype lattice cell）**：在无量纲笛卡尔空间 $D^{\mathrm{cell}} = [0, 1]^3$ 中定义单胞拓扑。根据 MMC 框架，单胞中第 $k$ 个构件（$k = 1, \dots, N_C$）的 TDF $\phi_k(\boldsymbol{x}; \boldsymbol{d}_k)$ 由式 (2)–(3) 给出。通过 K-S 函数聚合单胞内全部 $N_C$ 个独立构件：

$$
\phi^{\mathrm{cell}}(\boldsymbol{x}; \boldsymbol{d}^{\mathrm{cell}}) = \frac{1}{\lambda} \ln\left( \sum_{k=1}^{N_C} \exp(\lambda \phi_k(\boldsymbol{x}; \boldsymbol{d}_k)) \right),
\tag{5}
$$

其中 $\boldsymbol{d}^{\mathrm{cell}} = (\boldsymbol{d}_1^{\mathsf T}, \dots, \boldsymbol{d}_{N_C}^{\mathsf T})^{\mathsf T}$。例如，常用的面心立方（FCC）单胞可由 $N_C = 12$ 个构件组合而成（图 2(b)）。

- **第二步：生成宏观均匀周期点阵**：若直接在整个设计域对所有单胞的构件逐一计算 TDF，计算开销极其高昂。为此引入**周期复制函数（Periodic Replicating Function, PRF）** $T(\boldsymbol{x}, \boldsymbol{t})$ [73]，本文采用分量形式的锯齿波函数：

$$
T(x, t_x) = \frac{x}{t_x} - \mathrm{floor}\left(\frac{x}{t_x}\right), \quad
T(y, t_y) = \frac{y}{t_y} - \mathrm{floor}\left(\frac{y}{t_y}\right), \quad
T(z, t_z) = \frac{z}{t_z} - \mathrm{floor}\left(\frac{z}{t_z}\right),
\tag{6a-c}
$$

其中 $\boldsymbol{t} = (t_x, t_y, t_z)^{\mathsf T}$ 表示 PRF 在三个方向的周期，分别等于单胞的长、宽、高。周期点阵在整个设计域 $D$ 上的 TDF 表达为：

$$
\phi^p(\boldsymbol{x}; \boldsymbol{d}^p) = \frac{1}{\lambda} \ln\left( \sum_{k=1}^{N_C} \exp\left(\lambda \phi_k(T(\boldsymbol{x}, \boldsymbol{t}); \boldsymbol{d}_k)\right) \right).
\tag{7}
$$

- **第三步：引入空间梯度扰动构建梯度点阵**：基于连续介质力学原理，非均匀梯度点阵可视为均匀周期点阵（初始构型）在某种空间变形梯度场作用下的当前构型。为此在全局坐标系中施加扰动映射 $(\tilde{x}, \tilde{y}, \tilde{z})^{\mathsf T}$：

$$
\begin{bmatrix}
\tilde{x} \\ \tilde{y} \\ \tilde{z}
\end{bmatrix}
=
\begin{bmatrix}
x + f(x, y, z) \\
y + g(x, y, z) \\
z + h(x, y, z)
\end{bmatrix},
\tag{8}
$$

$$
f(x, y, z) = \sum_{n=1}^{n_1} \alpha_n \psi_x(x, y, z), \quad
g(x, y, z) = \sum_{m=1}^{m_1} \beta_m \psi_y(x, y, z), \quad
h(x, y, z) = \sum_{w=1}^{w_1} \gamma_w \psi_z(x, y, z).
\tag{9}
$$

将扰动后的空间坐标代入，最终获得梯度点阵结构的 TDF $\phi^g(\boldsymbol{x}; \boldsymbol{d}^g)$：

$$
\phi^g(\boldsymbol{x}; \boldsymbol{d}^g) = \frac{1}{\lambda} \ln\left( \sum_{k=1}^{N_C} \exp\left(\lambda \phi_k(T(\tilde{\boldsymbol{x}}, \boldsymbol{t}); \boldsymbol{d}_k)\right) \right).
\tag{10}
$$

![[Xu2025_Fig3.png]]

<center><b>
图 3：基于相同初始布局通过分区坐标映射（PCM）生成的三个梯度点阵算例。(a) 初始周期布局；(b) 相邻单胞间不协调的材料过渡；(c) 带有尖角的不平滑过渡；(d) 梯度结构中协调的材料分布与平滑过渡。
</b></center>

### 2.2.2 基于 B 样条的分区坐标映射构造

若各子区域独立施加任意扰动，相邻子区域交界面极易出现材料错位或尖角断裂（图 3(b)–(c)）。为此，本文采用具备分段光滑性与紧支特性的 **B 样条基函数** 构建三维分区坐标映射（PCM）。

在一维参数空间中，给定由非递减坐标构成的节点向量 $\boldsymbol{\xi} = \{ \xi_0, \xi_1, \dots, \xi_{n+p+1} \}$，根据 Cox-de-Boor 递推公式 [74]，0 阶 B 样条基函数定义为：

$$
N_{i,0}(\xi) =
\begin{cases}
1, & \text{若 } \xi_i \leq \xi < \xi_{i+1}, \\
0, & \text{其他},
\end{cases}
\tag{11}
$$

对于 $p \geq 1$ 阶基函数，递推关系为：

$$
N_{i,p}(\xi) = \frac{\xi - \xi_i}{\xi_{i+p} - \xi_i} N_{i,p-1}(\xi) + \frac{\xi_{i+p+1} - \xi}{\xi_{i+p+1} - \xi_{i+1}} N_{i+1,p-1}(\xi).
\tag{12}
$$

通过单变量 B 样条基函数的张量积，PCM 的扰动函数构建为：

$$
\begin{cases}
f(x, y, z) = \sum_{i=1}^n \sum_{j=1}^m \sum_{r=1}^w \hat{\alpha}_{i,j,r} P_{i,j,r} N_{i,p}(x) M_{j,q}(y) W_{r,l}(z), \\[2mm]
g(x, y, z) = \sum_{i=1}^n \sum_{j=1}^m \sum_{r=1}^w \hat{\beta}_{i,j,r} P_{i,j,r} N_{i,p}(x) M_{j,q}(y) W_{r,l}(z), \\[2mm]
h(x, y, z) = \sum_{i=1}^n \sum_{j=1}^m \sum_{r=1}^w \hat{\gamma}_{i,j,r} P_{i,j,r} N_{i,p}(x) M_{j,q}(y) W_{r,l}(z),
\end{cases}
\tag{13}
$$

其中 $P_{i,j,r}$ 为三维控制网格节点坐标，$\hat{\alpha}_{i,j,r}, \hat{\beta}_{i,j,r}, \hat{\gamma}_{i,j,r}$ 为对应控制节点上的扰动系数（即拓扑优化的设计变量）。

![[Xu2025_Fig4.png]]

<center><b>
图 4：利用 B 样条基函数构建的三维分区坐标映射原理图。
</b></center>

如图 4 所示，B 样条基函数的紧支特性保证了每个控制节点仅影响其局部的子区域；$p$ 阶 B 样条在子区域内部保证 $C^p$ 连续，跨子区域边界保证至少 $C^{p-1}$ 连续，从数学上根除了相邻单胞错位与断裂风险，实现了图 3(d) 所示的光滑天然连通性。因此，优化过程中单胞构件参数保持固定，仅将 PCM 扰动系数作为设计变量：$\boldsymbol{d}^g = (\boldsymbol{\alpha}^{\mathsf T}, \boldsymbol{\beta}^{\mathsf T}, \boldsymbol{\gamma}^{\mathsf T})^{\mathsf T}$。

---

# 3 PIML 增强的梯度点阵结构高效分析

三维梯度点阵全尺度有限元分析需要极密集的六面体网格。为攻克方程维度带来的计算瓶颈，本文将经典子结构静力缩聚方法与问题无关机器学习相结合。

## 3.1 用于有限元分析的子结构方法

如图 5 所示，将总体设计域划分为 $N_s$ 个非重叠子结构 $\Omega^j$（$j = 1, \dots, N_s$）。子结构内部包含 $m_s^3$ 个细网格单元。在 $\Omega^j$ 中，保留边界节点自由度数记为 $n_b^j$，待缩聚内部节点自由度数记为 $n_i^j$。

![[Xu2025_Fig5.png]]

<center><b>
图 5：设计域三维子结构分解示意图。最左图为初始设计域 $\Omega$；第二幅图为划分为多个子结构 $\Omega^j$；第三幅图显示每个子结构内部包含 $m_s^3$（$m_s=5$）个细网格单元；最右图为用于力学分析的均匀细网格。
</b></center>

第 $j$ 个子结构的有限元平衡方程按边界自由度（下标 $b$）与内部自由度（下标 $i$）分块写为：

$$
\mathbf{K}^j \boldsymbol{u}^j =
\begin{bmatrix}
\mathbf{K}_{bb}^j & \mathbf{K}_{bi}^j \\
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
\tag{14}
$$

在无内部体力载荷条件下（$\boldsymbol{f}_i^j = \boldsymbol{0}$，存在体力的情况见附录 A），内部节点位移由边界位移唯一确定：

$$
\boldsymbol{u}_i^j = -(\mathbf{K}_{ii}^j)^{-1} \mathbf{K}_{ib}^j \boldsymbol{u}_b^j = \mathbf{N}_s^j \boldsymbol{u}_b^j,
\tag{15}
$$

其中 $\mathbf{N}_s^j \triangleq -(\mathbf{K}_{ii}^j)^{-1} \mathbf{K}_{ib}^j$ 为多尺度数值形函数矩阵。从而子结构全部细节点位移表示为：

$$
\boldsymbol{u}^j =
\begin{bmatrix}
\mathbf{I} \\
\mathbf{N}_s^j
\end{bmatrix}
\boldsymbol{u}_b^j = \mathbf{N}^j \boldsymbol{u}_b^j.
$$

子结构的静力缩聚平衡方程为：

$$
\mathbf{K}_s^j \boldsymbol{u}_b^j = \boldsymbol{f}_b^j,
\tag{16}
$$

$$
\mathbf{K}_s^j = \mathbf{K}_{bb}^j - \mathbf{K}_{bi}^j (\mathbf{K}_{ii}^j)^{-1} \mathbf{K}_{ib}^j.
$$

组装所有子结构的缩聚刚度矩阵可得全局边界方程 $\mathbf{K}_s \boldsymbol{u}_b = \boldsymbol{f}_s$，其自由度数相比原系统急剧缩减。

此外，子结构的总应变能可表征为：

$$
W^j = \frac{1}{2} (\boldsymbol{u}^j)^{\mathsf T} \mathbf{K}^j \boldsymbol{u}^j = \frac{1}{2} (\boldsymbol{u}_b^j)^{\mathsf T} (\mathbf{N}^j)^{\mathsf T} \mathbf{K}^j \mathbf{N}^j \boldsymbol{u}_b^j = \frac{1}{2} (\boldsymbol{u}_b^j)^{\mathsf T} \mathbf{K}_s^j \boldsymbol{u}_b^j,
\tag{17}
$$

$$
\mathbf{K}_s^j = (\mathbf{N}^j)^{\mathsf T} \mathbf{K}^j \mathbf{N}^j.
\tag{18}
$$

式 (18) 表明，缩聚刚度矩阵 $\mathbf{K}_s^j$ 可由多尺度数值形函数 $\mathbf{N}^j$ 对原刚度矩阵进行对称转换求得。因此，通过离线机器学习建立材料密度到形函数 $\mathbf{N}^j$ 的映射，即可完全规避在线矩阵求逆操作。

## 3.2 力学信息机器学习模型的架构

采用八节点等参六面体单元，在线弹性范围内材料杨氏模量由单元伪密度插值决定，泊松比保持常数（$\nu_s = 0.3$）。神经网络的输入为子结构内部全部细单元的相对密度向量，输出为数值形函数 $\mathbf{N}^j$。

为消除冗余输出并嵌入物理规律，采取以下策略：
1. **形函数单位分解性质**：将 $\mathbf{N}^j$ 划分为预设的单位阵 $\mathbf{N}_{j1} = \mathbf{I}$ 与待预测的内部形函数 $\mathbf{N}_{j2} = \mathbf{N}_s^j$；
2. **刚体位移零应变能约束**：子结构在刚体平移与旋转时不产生应变能，由此可得平移约束方程（式 19a–19c）：

$$
\sum_{l=1}^{n_{jb}} (\mathbf{N}_{j2})_{kl,xx} = 1, \quad \sum_{l=1}^{n_{jb}} (\mathbf{N}_{j2})_{kl,xy} = 0, \quad \sum_{l=1}^{n_{jb}} (\mathbf{N}_{j2})_{kl,xz} = 0, \quad (k = 1, \dots, n_{ji}),
\tag{19a}
$$

$$
\sum_{l=1}^{n_{jb}} (\mathbf{N}_{j2})_{kl,yx} = 0, \quad \sum_{l=1}^{n_{jb}} (\mathbf{N}_{j2})_{kl,yy} = 1, \quad \sum_{l=1}^{n_{jb}} (\mathbf{N}_{j2})_{kl,yz} = 0, \quad (k = 1, \dots, n_{ji}),
\tag{19b}
$$

$$
\sum_{l=1}^{n_{jb}} (\mathbf{N}_{j2})_{kl,zx} = 0, \quad \sum_{l=1}^{n_{jb}} (\mathbf{N}_{j2})_{kl,zy} = 0, \quad \sum_{l=1}^{n_{jb}} (\mathbf{N}_{j2})_{kl,zz} = 1, \quad (k = 1, \dots, n_{ji}).
\tag{19c}
$$

以及刚体旋转约束方程：

$$
(\mathbf{I}_{n_{ji}} \otimes \boldsymbol{\omega}) \boldsymbol{x} = \mathbf{N}_{j2} (\mathbf{I}_{n_{jb}} \otimes \boldsymbol{\omega}) \mathbf{X},
\tag{20}
$$

其中 $\otimes$ 为 Kronecker 积，$\boldsymbol{\omega}$ 为反对称自旋矩阵，$\boldsymbol{x}$ 和 $\mathbf{X}$ 分别表示内部节点与边界节点的坐标向量。
3. **线性边界位移插值假定**：进一步引入边界线性位移假设，仅保留子结构 8 个角节点的位移自由度，将待预测矩阵维度压缩至 $3n_{ji} \times 18$；
4. **子结构对称分组网络输出**：对于 $m_s = 5$（$5^3 = 125$ 单元）和 $m_s = 10$（$10^3 = 1000$ 单元），独立输出维度分别为 3,456 与 39,366。为了降低训练难度，构建了 $m_s - 1$ 个结构相同的前馈网络，每个网络独立输出与特定节点组相关的四分之一部分。

每个前馈神经网络包含输入层、15 个隐藏层和输出层，各隐藏层神经元数设置为 $[60, 80, 100, 120, 140, 160, 180, 200, 180, 160, 140, 120, 100, 80, 60]$，交替采用 `tanh` 与 `elu` 激活函数以维持梯度稳定性。在 TensorFlow 2.6.2 下基于 MSE 损失和 Adam 优化器训练 3000 个 epoch。通过随机生成 40 万个包含非均匀材料分布的子结构样本集完成离线训练。

---

# 4 优化问题数学建模

本文旨在在可用材料体积约束 $\bar{V}$ 下，通过优化梯度点阵构型最大化结构的整体刚度（即最小化外力功柔度 $C$）。基于连续介质线弹性力学与 MMC 几何参数化，数学列式为：

$$
\begin{aligned}
\text{求}\quad & \boldsymbol{d}^g = (\boldsymbol{\alpha}^{\mathsf T}, \boldsymbol{\beta}^{\mathsf T}, \boldsymbol{\gamma}^{\mathsf T})^{\mathsf T}, \quad \boldsymbol{u}(\boldsymbol{x}) \in \mathcal{H}^1(\Omega) \\
\text{最小化}\quad & C = \int_{\Omega} H(\phi^g(\boldsymbol{x}; \boldsymbol{d}^g)) \boldsymbol{f} \cdot \boldsymbol{u} \,\mathrm{d}V + \int_{\Gamma_t} \boldsymbol{t} \cdot \boldsymbol{u} \,\mathrm{d}S \\
\text{满足条件：}\quad & \int_{\Omega} \mathbb{E}(H(\phi^g(\boldsymbol{x}; \boldsymbol{d}^g))) : \boldsymbol{\varepsilon}(\boldsymbol{u}) : \boldsymbol{\varepsilon}(\boldsymbol{v}) \,\mathrm{d}V \\
& \quad = \int_{\Omega} H(\phi^g(\boldsymbol{x}; \boldsymbol{d}^g)) \boldsymbol{f} \cdot \boldsymbol{v} \,\mathrm{d}V + \int_{\Gamma_t} \boldsymbol{t} \cdot \boldsymbol{v} \,\mathrm{d}S, \quad \forall \boldsymbol{v} \in \mathcal{U}_{\mathrm{ad}}, \\
& V = \int_{\Omega} H(\phi^g(\boldsymbol{x}; \boldsymbol{d}^g)) \,\mathrm{d}V \leq \bar{V}, \\
& \boldsymbol{d}^g \subset \mathcal{U}_{\boldsymbol{d}^g}, \\
& \boldsymbol{u} = \bar{\boldsymbol{u}}, \quad \text{在 } \Gamma_u \text{ 上},
\end{aligned}
\tag{21}
$$

其中 $\mathcal{U}_{\mathrm{ad}} = \{ \boldsymbol{v} \mid \boldsymbol{v} \in \mathcal{H}^1(\Omega), \boldsymbol{v} = \boldsymbol{0} \text{ 在 } \Gamma_u \text{ 上} \}$ 为运动容许位移场集合，$H(x)$ 为标准 Heaviside 阶跃函数，$\mathbb{E}$ 为四阶弹性张量。

---

# 5 数值实现

## 5.1 有限元分析的等效材料模型

采用三维八节点六面体单元剖分，第 $e$ 个细网格单元的刚度矩阵通过替代材料模型计算：

$$
\mathbf{K}_e = \int_{\Omega_e} \rho_e \mathbf{B}^{\mathsf T} \mathbf{D}^s \mathbf{B} \,\mathrm{d}V,
\tag{22}
$$

其中 $\mathbf{D}^s$ 为实体材料的各向同性线弹性本构矩阵。单元伪密度 $\rho_e$（即神经网络输入）通过单元 8 个角节点上的全局 TDF 值进行正规化 Heaviside 插值：

$$
\rho_e = \frac{1}{8} \sum_{i=1}^8 H_\epsilon((\phi^g)_i^e),
\tag{23}
$$

$$
H_\epsilon(x) =
\begin{cases}
1, & \text{若 } x > \epsilon, \\
\dfrac{3(1 - \Lambda)}{4} \left( \dfrac{x}{\epsilon} - \dfrac{x^3}{3\epsilon^3} \right) + \dfrac{1 + \Lambda}{2}, & \text{若 } |x| \leq \epsilon, \\
\Lambda, & \text{其他},
\end{cases}
\tag{24}
$$

其中 $\epsilon$ 为过渡区宽度参数，$\Lambda = 10^{-3}$ 为防止刚度矩阵奇异的微小下限参数。

## 5.2 灵敏度分析

目标函数与体积约束对特定设计变量 $\alpha_t$ 的灵敏度由伴随法给出：

$$
\frac{\partial C}{\partial \alpha_t} = -\sum_{e=1}^{NE} \boldsymbol{u}_e^{\mathsf T} \frac{\partial \mathbf{K}_e}{\partial \alpha_t} \boldsymbol{u}_e = -\frac{1}{8} \sum_{e=1}^{NE} \left( \sum_{i=1}^8 \frac{\partial H_\epsilon((\phi^g)_i^e)}{\partial \alpha_t} \boldsymbol{u}_e^{\mathsf T} \mathbf{K}_e^s \boldsymbol{u}_e \right),
\tag{25}
$$

$$
\frac{\partial V}{\partial \alpha_t} = \frac{1}{8} \sum_{e=1}^{NE} \left( \sum_{i=1}^8 \frac{\partial H_\epsilon((\phi^g)_i^e)}{\partial \alpha_t} \right).
\tag{26}
$$

根据复合函数链式求导法则，核心导数项展开为：

$$
\frac{\partial H_\epsilon(\phi^g)}{\partial \alpha_t} = \frac{\partial H_\epsilon(\phi^g)}{\partial \phi^g} \left( \sum_{k=1}^{N_C} \frac{\partial \phi^g}{\partial \phi_k} \frac{\partial \phi_k}{\partial \tilde{x}} \right) \frac{\partial \tilde{x}}{\partial \alpha_t},
\tag{27a}
$$

$$
\frac{\partial H_\epsilon(\phi^g)}{\partial \beta_t} = \frac{\partial H_\epsilon(\phi^g)}{\partial \phi^g} \left( \sum_{k=1}^{N_C} \frac{\partial \phi^g}{\partial \phi_k} \frac{\partial \phi_k}{\partial \tilde{y}} \right) \frac{\partial \tilde{y}}{\partial \beta_t}, \quad
\frac{\partial H_\epsilon(\phi^g)}{\partial \gamma_t} = \frac{\partial H_\epsilon(\phi^g)}{\partial \phi^g} \left( \sum_{k=1}^{N_C} \frac{\partial \phi^g}{\partial \phi_k} \frac{\partial \phi_k}{\partial \tilde{z}} \right) \frac{\partial \tilde{z}}{\partial \gamma_t},
\tag{27b-c}
$$

其中由 K-S 函数导出：

$$
\frac{\partial \phi^g}{\partial \phi_k} = \frac{\exp(\lambda \phi_k)}{\sum_{j=1}^{N_C} \exp(\lambda \phi_j)}.
\tag{28}
$$

对于 PCM 变换坐标的导数项，由于各坐标方向共用相同的 B 样条控制网格，其偏导数由基函数张量积直接给出：

$$
\frac{\partial \tilde{x}}{\partial \alpha_t} = \frac{\partial \tilde{y}}{\partial \beta_t} = \frac{\partial \tilde{z}}{\partial \gamma_t} = \sum_{i=1}^n \sum_{j=1}^m \sum_{r=1}^w N_{i,p}(x) M_{j,q}(y) W_{r,l}(z).
\tag{29}
$$

注意：式 (29) 中的偏导数仅取决于初始网格坐标，与优化迭代无关，可在迭代开始前**一次性离线预先计算并缓存**。$\partial \phi_k / \partial \tilde{x}, \partial \phi_k / \partial \tilde{y}, \partial \phi_k / \partial \tilde{z}$ 的解析展开式详见附录 B。

## 5.3 优化流程

整体算法流程包含五个主要阶段，如图 6 所示：
1. **模型初始化**：离散设计域 $D$，划分子结构，施加边界条件与外载荷；
2. **构建初始周期点阵**：定义单胞基元 TDF，通过 PRF 延拓至全设计域；
3. **生成梯度点阵**：计算 PCM 空间坐标扰动，根据节点 TDF 生成各子结构的细网格密度场 $\boldsymbol{\rho}(\boldsymbol{x})$；
4. **PIML 增强结构分析**：由 ANN 快速预测子结构数值形函数 $\mathbf{N}^j$，组装缩聚刚度矩阵 $\tilde{\mathbf{K}}$ 并求解位移场；
5. **灵敏度分析与变量更新**：计算解析导数，利用移动渐近线法（MMA）更新 PCM 扰动系数，直至满足收敛准则。

![[Xu2025_Fig6.png]]

<center><b>
图 6：基于问题无关机器学习（PIML）增强的梯度点阵结构拓扑优化计算流程图。
</b></center>

---

# 6 数值算例

所有算例均在一台配备 Intel Xeon Gold 6256 CPU (@3.6 GHz) 与 512 GB 内存的工作站上使用 MATLAB R2019a 进行单线程求解（无并行加速），利用 ParaView 进行体素化模型三维可视化。结构材料采用无量纲杨氏模量 $E_s = 1$ 与泊松比 $\nu_s = 0.3$。优化求解器选用 MMA 算法 [77]，收敛判据为连续五次迭代目标函数相对变化小于 $10^{-3}$，MMA 算法参数如表 1 所示。PCM 默认采用二次均匀 B 样条基函数。

<center><b>
表 1：MMA 算法控制参数。
</b></center>

| 参数名 | 设定值 | 说明 |
|---|---|---|
| `epsimin` | $10^{-9}$ | 容差下限 |
| `raa0` | $0.01$ | 初始渐近线移动系数 |
| `albefa` | $0.8$ | 变量上下界缩放系数 |
| `asyinit` | $0.05$ | 渐近线初始步长 |
| `asyincr` | $1.0$ | 渐近线递增系数 |
| `asydecr` | $0.8$ | 渐近线递减系数 |

## 6.1 MBB 梁算例

设计域尺寸为长 $DL = 6$、宽 $DW = 1.2$、高 $DH = 1.2$。上下表面覆盖厚度为 0.04 的非设计实体外壳，顶面中心施加单位垂直集中载荷，材料总体积分数约束为 $\bar{V} = 0.2$。子结构尺寸取 $m_s = 5$，整个模型不做对称性简化，如图 7 所示。

![[Xu2025_Fig7.png]]

<center><b>
图 7：MBB 梁算例的问题设置与边界条件示意图。
</b></center>

![[Xu2025_Fig8.png]]

<center><b>
图 8：MBB 梁算例的初始周期设计 ((a)–(c)) 与优化梯度设计 ((d)–(f))。Case 1 至 Case 3 网格与单胞数量依次递增；(g)–(i) 分别给出了 Case 2 优化梯度构型在不同位置对称面上的剖面图。
</b></center>

设计域划分为 $15 \times 3 \times 3$ 个 B 样条子区域，扰动系数范围限制在 $[-1.0, 1.0]$。针对三种不同离散规模进行优化测试，优化结果汇总于表 2。

<center><b>
表 2：不同工况下有限元单元数 $N_f$、单胞数 $N_c$ 以及 PIML 模型柔度 $C_{\mathrm{PIML}}$ 与扩展多尺度有限元法（EMsFEM）重分析柔度 $C_{\mathrm{EMs}}$ 对比。
</b></center>

| 工况 | 细有限元网格数 $N_f$ | 初始单胞数 $N_c$ | 初始周期设计 $C_{\mathrm{PIML}}$ | 初始周期设计 $C_{\mathrm{EMs}}$ | 优化梯度设计 $C_{\mathrm{PIML}}$ | 优化梯度设计 $C_{\mathrm{EMs}}$ |
|---|---|---|---|---|---|---|
| **Case 1** | $450 \times 90 \times 90$ ($3,645,000$) | $30 \times 6 \times 6$ ($1,080$) | $222.10$ | $228.81$ | $164.75$ | $169.50$ |
| **Case 2** | $600 \times 120 \times 120$ ($8,640,000$) | $40 \times 8 \times 8$ ($2,560$) | $245.59$ | $251.68$ | $183.38$ | $187.56$ |
| **Case 3** | $750 \times 150 \times 150$ ($16,875,000$) | $50 \times 10 \times 10$ ($5,000$) | $250.19$ | $256.11$ | $189.31$ | $193.62$ |

如图 8 所示，优化后的梯度点阵在整个设计域中表现出连续平滑的单胞尺寸、形状与取向变化。相比初始周期结构，PIML 评估的结构柔度在三个工况下均**降低了近 25%**（即刚度大幅提升）。与高精度 EMsFEM 重分析结果相比，PIML 预测的相对误差均严格保持在 **3% 以内**。

![[Xu2025_Fig9.png]]

<center><b>
图 9：Result 2 中 $xOz$ 对称面上的材料分布。(a) 结构增强区域标注；(b) $xOz$ 平面上所有子结构的相对密度分布 $\rho_{ss}$；(c) 相对密度阈值为 0.2 的分布图。
</b></center>

![[Xu2025_Fig10.png]]

<center><b>
图 10：优化梯度点阵结构中所有子结构相对密度 $\rho_{ss}$ 的分布直方图。相对密度小于 0.15 的子结构占比超过 67%，而密度大于 0.5 的子结构仅占 5%。
</b></center>

图 9 与图 10 显示，材料自适应地向顶面载荷作用区与两端简支支座等高应力区聚集，低应力区的单胞明显收缩，且中间过渡区保持交织，证明了 PCM 具备极佳的局部材料重分布能力。

![[Xu2025_Fig11.png]]

<center><b>
图 11：不同扰动系数取值范围 $\bar{\alpha}$ 与不同分区划分网格下的优化结果对比。
</b></center>

图 11 进一步表明，放宽扰动范围或细化 PCM 分区可扩展设计空间、获得更优的刚度性能。在 MMC 显式描述下，对应工况的设计变量总数仅为 297、768 和 1575，比同规模基于密度的拓扑优化方法低数个数量级。

![[Xu2025_Fig12.png]]

<center><b>
图 12：MBB 梁算例中 PIML 框架单步迭代计算时间细分占比对比饼图。包含预测形函数与刚度准备时间 $t_{\mathrm{pre}}$、位移求解时间 $t_{\mathrm{disp}}$、灵敏度分析时间 $t_{\mathrm{sens}}$、TDF 生成时间 $t_{\mathrm{TDF}}$ 及 MMA 更新时间 $t_{\mathrm{other}}$。
</b></center>

如图 12 所示，单步平均总耗时从 Case 1（364 万单元）的 $52.54\text{ s}$ 仅微增至 Case 3（1687 万单元）的 $334.85\text{ s}$；其中 $t_{\mathrm{TDF}}$ 耗时始终维持在约 3%，展示了卓越的大规模求解效率。

## 6.2 扭转箱算例

为验证方法在扭转主导问题中的适用性并探索更大子结构尺寸的加速效果，设计了图 13 所示的三维扭转箱算例。设计域尺寸为 $120 \times 120 \times 60$，底部完全固定，顶面四角施加正交于对角线的面内扭矩载荷，体积分数约束为 $\bar{V} = 0.15$。细网格单元规模高达 **23,328,000**（2332 万单元）。采用 $6 \times 6 \times 3$ 的 PCM 分区，初始单胞选用 FCC，设计变量共 588 个（图 14）。

![[Xu2025_Fig13.png]]

<center><b>
图 13：扭转箱算例的问题设置与边界条件。
</b></center>

![[Xu2025_Fig14.png]]

<center><b>
图 14：扭转箱初始周期设计的 (a) 全景图、(b) $xOy$ 平面对称剖面图以及 (c) $xOz$ 平面对称剖面图。
</b></center>

![[Xu2025_Fig15.png]]

<center><b>
图 15：优化梯度设计的 (a) 全景图、(b) $xOy$ 平面对称剖面图以及 (c) $xOz$ 平面对称剖面图。
</b></center>

![[Xu2025_Fig16.png]]

<center><b>
图 16：$m_s = 5$ 与 $m_s = 10$ 子结构尺寸下目标函数的收敛历史曲线及若干中间迭代步设计构型（$xOy$ 截面俯视图）。
</b></center>

对比 $m_s = 5$ 与 $m_s = 10$ 两种子结构尺寸（图 15–16）：
- 优化后扭转箱最外层杆件平滑聚拢形成闭合薄壳以抵抗剪切扭转，内部材料向外迁移，与传统连续体密度法形成的空心抗扭箱构型一致；
- $m_s = 5$ 经 205 步收敛至柔度 $46.69$；$m_s = 10$ 经 274 步收敛至 $27.55$。

![[Xu2025_Fig17.png]]

<center><b>
图 17：扭转箱算例在不同子结构尺寸下的计算时间对比饼图。
</b></center>

如图 17 所示，当子结构尺寸增大至 $m_s = 10$ 时，全局缩聚刚度矩阵维度大幅缩减，位移求解时间 $t_{\mathrm{disp}}$ 占总时间比例从 32% 骤降至 3.6%，单步求解时间实现约 **40 倍加速**，单步平均总时间从 $867.81\text{ s}$ 降低至 $370.86\text{ s}$。

## 6.3 股骨近端填充设计

第三个算例为具有复杂自由曲面几何与多载荷工况的人体近端股骨骨小梁填充设计 [79]（图 18）。

![[Xu2025_Fig18.png]]

<center><b>
图 18：近端股骨填充算例的问题设置。(a) $xOy$ 平面视图；(b) $xOz$ 平面视图。
</b></center>

![[Xu2025_Fig19.png]]

<center><b>
图 19：不规则设计域的体素化过程。(a) 带有轴对齐包围盒的设计域；(b) 非设计实体皮质骨外壳；(c) 填充周期点阵结构的近端股骨体素化模型。
</b></center>

如图 19 所示，通过**轴对齐包围盒（AABB）**与**二值体素化技术 [81]**建立计算网格。外层为模拟人体致密皮质骨的非设计实体壳层，内部空间填充梯度松质骨点阵。整体设计域包围盒尺寸为 $15 \times 9 \times 6$，体积分数限制为 $\bar{V} = 0.04$（占内部空间的 21%），采用 $6 \times 5 \times 4$ 分区。测试了两个不同离散精度的工况：
- **Case 1**：648 万（$300 \times 180 \times 120$）体素单元；
- **Case 2**：2187 万（$450 \times 270 \times 180$）体素单元。

![[Xu2025_Fig20.png]]

<center><b>
图 20：Case 1 设计的剖面图。(a) 初始周期点阵填充设计；(b) 优化梯度点阵填充结果（红绿虚线高亮显示空间变化的单胞取向）。
</b></center>

![[Xu2025_Fig21.png]]

<center><b>
图 21：Case 2 高分辨率设计的剖面图。(a) 初始周期点阵填充设计；(b) 优化梯度点阵填充结果，局部放大图显示致密微结构的细节。
</b></center>

如图 20 与图 21 所示，优化后的微观杆件沿主应力迹线方向发生自适应偏转，单胞大小沿受力路径形成显著梯度，Case 1 和 Case 2 的承载性能相比初始周期填充分别提升了 **14%** 与 **10%**。

![[Xu2025_Fig22.png]]

<center><b>
图 22：两工况下采用/不采用多余自由度剔除（Redundant DOF removal）技术的 PIML 框架计算时间对比。
</b></center>

由于股骨模型包围盒内存在高达 70% 的非设计空区域，利用**多余自由度剔除技术 [59]**消除全空子结构后（图 22），位移求解时间 $t_{\mathrm{disp}}$ 降至未剔除时的 **10% 以下**，在 2187 万单元的大规模算例中将单步有限元求解压缩到了极致。

---

# 7 结论与展望

本文提出了一种基于 MMC 显式拓扑优化框架与问题无关机器学习（PIML）的三维点阵复合结构高效设计方法：
1. 利用 B 样条分区坐标映射（PCM）的高阶连续性，在保持相邻微结构天然光滑连通的前提下，实现了三维梯度点阵单胞尺寸、几何形状与空间取向的显式协同控制；
2. 结合基于力学原理的 PIML 子结构预测模型，将大规模三维有限元分析复杂度缩减数个数量级，并成功应用于上千万自由度的弯曲、扭转及生物骨骼填充设计中。

**未来研究方向**：
- 结合增材制造工艺约束（如悬垂角限制、最小特征尺寸控制）；
- 将 PIML 推广至动力学响应、热传导及多物理场耦合优化；
- 拓展至基于三周期极小曲面（TPMS）等隐式表征的点阵构型；
- 放宽子结构界面的线性位移假定，发展高阶边界位移插值算子以消除子结构刚度过刚风险。

---

# CRediT 作者贡献说明

- **Wu Xu**：论文撰写 – 初稿，可视化，指导，软件，资源，调查研究，数据审定。
- **Chang Liu**：论文撰写 – 审阅与编辑，论文撰写 – 初稿，验证，软件，资源，方法学，调查研究，资金争取，形式分析，概念构思。
- **Yilin Guo**：可视化，验证，软件，调查研究，数据审定。
- **Mengcheng Huang**：软件，方法学。
- **Xu Guo**：论文撰写 – 审阅与编辑，方法学，资金争取。

# 利益冲突声明

作者声明不存在可能影响本文报道工作的已知经济利益竞争或人际关系冲突。

# 数据可用性声明

本文涉及的研究数据可根据合理要求向作者索取。

# 致谢

本研究得到国家重点研发计划（No. 2022YFB3303000）、国家自然科学基金（No. 12472344）和高等学校学科创新引智计划（111 计划，No. B14013）的资助。

---

# 附录 A. 子结构方法中考虑体力的情况

当子结构内部存在不可忽略的体力载荷（$\boldsymbol{f}_i^j \neq \boldsymbol{0}$）时，子结构内部位移与边界位移的关系广义化为：

$$
\boldsymbol{u}_i^j = (\mathbf{K}_{ii}^j)^{-1} (\boldsymbol{f}_i^j - \mathbf{K}_{ib}^j \boldsymbol{u}_b^j).
\tag{A1}
$$

代入平衡方程后，当前子结构边界节点的平衡方程写为：

$$
\left( \mathbf{K}_{bb}^j - \mathbf{K}_{bi}^j (\mathbf{K}_{ii}^j)^{-1} \mathbf{K}_{ib}^j \right) \boldsymbol{u}_b^j = \tilde{\boldsymbol{f}}^j = \boldsymbol{f}_b^j - \mathbf{K}_{bi}^j (\mathbf{K}_{ii}^j)^{-1} \boldsymbol{f}_i^j.
\tag{A2}
$$

缩聚刚度矩阵的形式保持不变，右端等效外力项可改写为 $\boldsymbol{f}_b^j + (\mathbf{N}_s^j)^{\mathsf T} \boldsymbol{f}_i^j$。这表明即使存在体力，多尺度形函数矩阵 $\mathbf{N}_s^j$ 依然具有问题无关性，本文的 PIML 离线预测策略完全适用。

---

# 附录 B. 灵敏度表达式中的各项解析求导

本节给出链式求导中各项偏导数的显式表达式：

$$
\frac{\partial \phi_k}{\partial \tilde{x}} = \frac{\partial \phi_k}{\partial T} \frac{\partial T}{\partial x'} \frac{\partial x'}{\partial \tilde{x}} + \frac{\partial \phi_k}{\partial T} \frac{\partial T}{\partial y'} \frac{\partial y'}{\partial \tilde{x}} + \frac{\partial \phi_k}{\partial T} \frac{\partial T}{\partial z'} \frac{\partial z'}{\partial \tilde{x}}.
\tag{A3}
$$

对于立方体单胞，$\partial T / \partial x' = \partial T / \partial y' = \partial T / \partial z' = 1$，因此有：

$$
\frac{\partial \phi_k}{\partial \tilde{y}} = \frac{\partial \phi_k}{\partial x'} \frac{\partial x'}{\partial \tilde{y}} + \frac{\partial \phi_k}{\partial y'} \frac{\partial y'}{\partial \tilde{y}} + \frac{\partial \phi_k}{\partial z'} \frac{\partial z'}{\partial \tilde{y}},
\tag{A4}
$$

$$
\frac{\partial \phi_k}{\partial \tilde{z}} = \frac{\partial \phi_k}{\partial x'} \frac{\partial x'}{\partial \tilde{z}} + \frac{\partial \phi_k}{\partial y'} \frac{\partial y'}{\partial \tilde{z}} + \frac{\partial \phi_k}{\partial z'} \frac{\partial z'}{\partial \tilde{z}}.
\tag{A5}
$$

引入以下紧凑记号：

$$
w \triangleq \left(\frac{x'}{L_1^k}\right)^6 + \left(\frac{y'}{L_2^k}\right)^6 + \left(\frac{z'}{L_3^k}\right)^6,
\tag{A6}
$$

$$
\bar{x} = \frac{x'}{L_1^k}, \quad \bar{y} = \frac{y'}{L_2^k}, \quad \bar{z} = \frac{z'}{L_3^k},
\tag{A7}
$$

$$
\mathbf{R} \triangleq
\begin{bmatrix}
\cos\theta_2^k \cos\theta_3^k & -\cos\theta_2^k \sin\theta_3^k & \sin\theta_2^k \\
\cos\theta_1^k \sin\theta_3^k + \sin\theta_1^k \sin\theta_2^k \cos\theta_3^k & \cos\theta_1^k \cos\theta_3^k - \sin\theta_1^k \sin\theta_2^k \sin\theta_3^k & -\sin\theta_1^k \cos\theta_2^k \\
\sin\theta_1^k \sin\theta_3^k - \cos\theta_1^k \sin\theta_2^k \cos\theta_3^k & \sin\theta_1^k \cos\theta_3^k + \cos\theta_1^k \sin\theta_2^k \sin\theta_3^k & \cos\theta_1^k \cos\theta_2^k
\end{bmatrix}.
\tag{A8}
$$

则偏导数的解析表达式分别为：

$$
\frac{\partial \phi_k}{\partial \tilde{x}} = -w^{-\frac{5}{6}} \left( \frac{\bar{x}^5}{L_1^k} R_{11} + \frac{\bar{y}^5}{L_2^k} R_{21} + \frac{\bar{z}^5}{L_3^k} R_{31} \right),
\tag{A9}
$$

$$
\frac{\partial \phi_k}{\partial \tilde{y}} = -w^{-\frac{5}{6}} \left( \frac{\bar{x}^5}{L_1^k} R_{12} + \frac{\bar{y}^5}{L_2^k} R_{22} + \frac{\bar{z}^5}{L_3^k} R_{32} \right),
\tag{A10}
$$

$$
\frac{\partial \phi_k}{\partial \tilde{z}} = -w^{-\frac{5}{6}} \left( \frac{\bar{x}^5}{L_1^k} R_{13} + \frac{\bar{y}^5}{L_2^k} R_{23} + \frac{\bar{z}^5}{L_3^k} R_{33} \right).
\tag{A11}
$$

---

# 参考文献

[1] Y. Tang, G. Dong, Q. Zhou, Y.F. Zhao, Lattice structure design and optimization with additive manufacturing constraints, IEEE Trans. Autom. Sci. Eng. 15 (2018) 1546–1562, https://doi.org/10.1109/TASE.2017.2685643.

[2] C. Pan, Y. Han, J. Lu, Design and optimization of lattice structures: A review, Appl. Sci.-Basel 10 (2020) 1–36, https://doi.org/10.3390/APP10186374.

[3] C. Wang, J. Zhu, M. Wu, J. Hou, H. Zhou, L. Meng, et al., Multi-scale design and optimization for solid-lattice hybrid structures and their application to aerospace vehicle components, Chin. J. Aeronaut. 34 (2021) 386–398, https://doi.org/10.1016/j.cja.2020.08.015.

[4] H. Zhou, X. Cao, C. Li, X. Zhang, H. Fan, H. Lei, et al., Design of self-supporting lattices for additive manufacturing, J. Mech. Phys. Solids 148 (2021) 104298, https://doi.org/10.1016/j.jmps.2021.104298.

[5] H. Yin, W. Zhang, L. Zhu, F. Meng, J. Liu, G. Wen, Review on lattice structures for energy absorption properties, Compos. Struct. 304 (2023) 116397, https://doi.org/10.1016/j.compstruct.2022.116397.

[6] S. Li, H. Zhu, G. Feng, L. Xiao, W. Song, Influence mechanism of cell-arrangement strategy on energy absorption of dual-phase hybrid lattice structure, Int. J. Impact Eng. 175 (2023) 104528, https://doi.org/10.1016/j.ijimpeng.2023.104528.

[7] X. Li, X. Yu, W. Zhai, Additively manufactured deformation-recoverable and broadband sound-absorbing microlattice inspired by the concept of traditional perforated panels, Adv. Mater. 33 (2021) 2104552, https://doi.org/10.1002/adma.202104552.

[8] L. Cheng, J. Liu, A.C. To, Concurrent lattice infill with feature evolution optimization for additive manufactured heat conduction design, Struct. Multidiscip. Optim. 58 (2018) 511–535, https://doi.org/10.1007/s00158-018-1905-7.

[9] K.J. Maloney, K.D. Fink, T.A. Schaedler, J.A. Kolodziejska, A.J. Jacobsen, C.S. Roper, Multifunctional heat exchangers derived from three-dimensional micro-lattice structures, Int. J. Heat Mass Transf. 55 (2012) 2486–2493, https://doi.org/10.1016/j.ijheatmasstransfer.2012.01.011.

[10] C. Imediegwu, R. Murphy, R. Hewson, M. Santer, Multiscale thermal and thermo-structural optimization of three-dimensional lattice structures, Struct. Multidiscip. Optim. 65 (2022) 13, https://doi.org/10.1007/s00158-021-03087-8.

[11] P.F. Egan, V.C. Gonella, M. Engensperger, S.J. Ferguson, K. Shea, Computationally designed lattices with tuned properties for tissue engineering using 3D printing, PLoS One 12 (2017) e0182902, https://doi.org/10.1371/journal.pone.0182902.

[12] N. Soro, H. Attar, E. Brodie, M. Veidt, A. Molotnikov, M.S. Dargusch, Evaluation of the mechanical compatibility of additively manufactured porous Ti–25Ta alloy for load-bearing implant applications, J. Mech. Behav. Biomed. Mater. 97 (2019) 149–158, https://doi.org/10.1016/j.jmbbm.2019.05.019.

[13] R.M. Gorguluarslan, S.K. Choi, C.J. Saldana, Uncertainty quantification and validation of 3D lattice scaffolds for computer-aided biomedical applications, J. Mech. Behav. Biomed. Mater. 71 (2017) 428–440, https://doi.org/10.1016/j.jmbbm.2017.04.011.

[14] J. Zhu, H. Zhou, C. Wang, L. Zhou, S. Yuan, W. Zhang, A review of topology optimization for additive manufacturing: Status and challenges, Chin. J. Aeronaut. 34 (2021) 91–110, https://doi.org/10.1016/j.cja.2020.09.020.

[15] F. Veloso, J. Gomes-Fonseca, P. Morais, J. Correia-Pinto, A.C.M. Pinho, J.L. Vilaça, Overview of methods and software for the design of functionally graded lattice structures, Adv. Eng. Mater. 24 (2022) 2200483, https://doi.org/10.1002/adem.202200483.

[16] M.P. Bendsøe, N. Kikuchi, Generating optimal topologies in structural design using a homogenization method, Comput. Meth. Appl. Mech. Eng. 71 (1988) 197–224, https://doi.org/10.1016/0045-7825(88)90086-2.

[17] M.P. Bendsøe, Optimal shape design as a material distribution problem, Struct. Optim. 1 (1989) 193–202, https://doi.org/10.1007/BF01650949.

[18] M. Zhou, G.I.N. Rozvany, The COC algorithm, Part II: Topological, geometrical and generalized shape optimization, Comput. Meth. Appl. Mech. Eng. 89 (1991) 309–336, https://doi.org/10.1016/0045-7825(91)90046-9.

[19] Y.M. Xie, G.P. Steven, A simple evolutionary procedure for structural optimization, Comput. Struct. 49 (1993) 885–896, https://doi.org/10.1016/0045-7949(93)90035-C.

[20] X. Huang, Y.M. Xie, Convergent and mesh-independent solutions for the bi-directional evolutionary structural optimization method, Finite Elem. Anal. Des. 43 (2007) 1039–1049, https://doi.org/10.1016/j.finel.2007.06.006.

[21] M.Y. Wang, X. Wang, D. Guo, A level set method for structural topology optimization, Comput. Meth. Appl. Mech. Eng. 192 (2003) 227–246, https://doi.org/10.1016/S0045-7825(02)00559-5.

[22] X. Guo, W. Zhang, W. Zhong, Doing topology optimization explicitly and geometrically—A new moving morphable components based framework, J. Appl. Mech.-Trans. ASME 81 (2014) 081009, https://doi.org/10.1115/1.4027609.

[23] X. Guo, W. Zhang, J. Zhang, J. Yuan, Explicit structural topology optimization based on moving morphable components (MMC) with curved skeletons, Comput. Meth. Appl. Mech. Eng. 310 (2016) 711–748, https://doi.org/10.1016/j.cma.2016.07.018.

[24] W. Zhang, W. Yang, J. Zhou, D. Li, X. Guo, Structural topology optimization through explicit boundary evolution, J. Appl. Mech.-Trans. ASME 84 (2016) 011011, https://doi.org/10.1115/1.4034972.

[25] L. Cheng, J. Bai, A.C. To, Functionally graded lattice structure topology optimization for the design of additive manufactured components with stress constraints, Comput. Meth. Appl. Mech. Eng. 344 (2019) 334–359, https://doi.org/10.1016/j.cma.2018.10.010.

[26] C. Wang, X. Gu, J. Zhu, H. Zhou, S. Li, W. Zhang, Concurrent design of hierarchical structures with three-dimensional parameterized lattice microstructures for additive manufacturing, Struct. Multidiscip. Optim. 61 (2020) 869–894, https://doi.org/10.1007/s00158-019-02408-2.

[27] Y. Zhang, M. Xiao, Z. Ding, M. Xu, G. Jiang, L. Gao, Dynamic response-oriented multiscale topology optimization for geometrically asymmetric sandwich structures with graded cellular cores, Comput. Meth. Appl. Mech. Eng. 416 (2023) 116367, https://doi.org/10.1016/j.cma.2023.116367.

[28] Y. Zhang, M. Xiao, X. Zhang, L. Gao, Topological design of sandwich structures with graded cellular cores by multiscale optimization, Comput. Meth. Appl. Mech. Eng. 361 (2020) 112749, https://doi.org/10.1016/j.cma.2019.112749.

[29] L. Zhu, L. Sun, X. Wang, N. Li, Optimisation of three-dimensional hierarchical structures with tailored lattice metamaterial anisotropy, Mater. Des. 210 (2021) 110083, https://doi.org/10.1016/j.matdes.2021.110083.

[30] J. Wu, O. Sigmund, J.P. Groen, Topology optimization of multi-scale structures: a review, Struct. Multidiscip. Optim. 63 (2021) 1455–1480, https://doi.org/10.1007/s00158-021-02881-8.

[31] S. Daynes, S. Feih, W.F. Lu, J. Wei, Optimisation of functionally graded lattice structures using isostatic lines, Mater. Des. 127 (2017) 215–223, https://doi.org/10.1016/j.matdes.2017.04.082.

[32] S. Daynes, S. Feih, W.F. Lu, J. Wei, Design concepts for generating optimised lattice structures aligned with strain trajectories, Comput. Meth. Appl. Mech. Eng. 354 (2019) 689–705, https://doi.org/10.1016/j.cma.2019.05.053.

[33] S. Daynes, S. Feih, Bio-inspired lattice structure optimisation with strain trajectory aligned trusses, Mater. Des. 213 (2022) 110320, https://doi.org/10.1016/j.matdes.2021.110320.

[34] J.P. Groen, O. Sigmund, Homogenization-based topology optimization for high-resolution manufacturable microstructures, Int. J. Numer. Methods Eng. 113 (2018) 1148–1163, https://doi.org/10.1002/nme.5575.

[35] J.P. Groen, F.C. Stutz, N. Aage, J.A. Bærentzen, O. Sigmund, De-homogenization of optimal multi-scale 3D topologies, Comput. Meth. Appl. Mech. Eng. 364 (2020) 112979, https://doi.org/10.1016/j.cma.2020.112979.

[36] G. Allaire, P. Geoffroy-Donders, O. Pantz, Topology optimization of modulated and oriented periodic microstructures by the homogenization method, Comput. Math. Appl. 78 (2019) 2197–2229, https://doi.org/10.1016/j.camwa.2018.08.007.

[37] P. Geoffroy-Donders, G. Allaire, O. Pantz, 3-d topology optimization of modulated and oriented periodic microstructures by the homogenization method, J. Comput. Phys. 401 (2020) 108994, https://doi.org/10.1016/j.jcp.2019.108994.

[38] C. Liu, Z. Du, W. Zhang, Y. Zhu, X. Guo, Additive manufacturing-oriented design of graded lattice structures through explicit topology optimization, J. Appl. Mech.-Trans. ASME 84 (2017) 081008, https://doi.org/10.1115/1.4036941.

[39] C. Liu, Z. Du, Y. Zhu, W. Zhang, X. Zhang, X. Guo, Optimal design of shell-graded-infill structures by a hybrid MMC-MMV approach, Comput. Meth. Appl. Mech. Eng. 369 (2020) 113187, https://doi.org/10.1016/j.cma.2020.113187.

[40] W. Xu, C. Liu, Y. Guo, Z. Du, W. Zhang, X. Guo, Graded infill lattice structures design based on the moving morphable component method and partitioned coordinate mapping technique, Compos. Struct. 326 (2023) 117613, https://doi.org/10.1016/j.compstruct.2023.117613.

[41] J. Wu, W. Wang, X. Gao, Design and optimization of conforming lattice structures, IEEE Trans. Vis. Comput. Graph. 27 (2021) 43–56, https://doi.org/10.1109/TVCG.2019.2938946.

[42] W. Chen, X. Zheng, S. Liu, Finite-element-mesh based method for modeling and optimization of lattice structures for additive manufacturing, Materials 11 (2018) 2073, https://doi.org/10.3390/ma11112073.

[43] Y. Tang, G. Dong, Y.F. Zhao, A hybrid geometric modeling method for lattice structures fabricated by additive manufacturing, Int. J. Adv. Manuf. Technol. 102 (2019) 4011–4030, https://doi.org/10.1007/s00170-019-03308-x.

[44] M. Montemurro, K. Refai, A. Catapano, Thermal design of graded architected cellular materials through a CAD-compatible topology optimisation method, Compos. Struct. 280 (2022) 114862, https://doi.org/10.1016/j.compstruct.2021.114862.

[45] G. Bertolino, M. Montemurro, Two-scale topology optimisation of cellular materials under mixed boundary conditions, Int. J. Mech. Sci. 216 (2022) 106961, https://doi.org/10.1016/j.ijmecsci.2021.106961.

[46] M. Montemurro, G. Bertolino, E. Panettieri, Topology optimisation of architected cellular materials from additive manufacturing: Analysis, design, and experiments, Structures 47 (2023) 2220–2239, https://doi.org/10.1016/j.istruc.2022.12.032.

[47] M. Montemurro, T. Roiné, J. Pailhès, Multi-scale design of multi-material lattice structures through a CAD-compatible topology optimisation algorithm, Eng. Struct. 273 (2022) 115009, https://doi.org/10.1016/j.engstruct.2022.115009.

[48] M.Y. Wang, H. Zong, Q. Ma, Y. Tian, M. Zhou, Cellular level set in B-splines (CLIBS): A method for modeling and topology optimization of cellular structures, Comput. Meth. Appl. Mech. Eng. 349 (2019) 378–404, https://doi.org/10.1016/j.cma.2019.02.026.

[49] G. Dong, Y. Tang, D. Li, Y.F. Zhao, Design and optimization of solid lattice hybrid structures fabricated by additive manufacturing, Addit. Manuf. 33 (2020) 101116, https://doi.org/10.1016/j.addma.2020.101116.

[50] Y. Guo, C. Liu, X. Guo, Shell-infill composite structure design based on a hybrid explicit-implicit topology optimization method, Compos. Struct. 337 (2024) 118029, https://doi.org/10.1016/j.compstruct.2024.118029.

[51] C. Liu, Z. Du, W. Zhang, X. Zhang, Y. Mei, X. Guo, Design of optimized architected structures with exact size and connectivity via an enhanced multidomain topology optimization strategy, Comput. Mech. 67 (2021) 743–762, https://doi.org/10.1007/s00466-020-01961-8.

[52] N. Aage, B.S. Lazarov, Parallel framework for topology optimization using the method of moving asymptotes, Struct. Multidiscip. Optim. 47 (2013) 493–505, https://doi.org/10.1007/s00158-012-0869-2.

[53] A. Evgrafov, C.J. Rupp, K. Maute, M.L. Dunn, Large-scale parallel topology optimization using a dual-primal substructuring solver, Struct. Multidiscip. Optim. 36 (2008) 329–345, https://doi.org/10.1007/s00158-007-0190-7.

[54] N. Aage, E. Andreassen, B.S. Lazarov, O. Sigmund, Giga-voxel computational morphogenesis for structural design, Nature 550 (2017) 84–86, https://doi.org/10.1038/nature23911.

[55] C. Liu, Y. Zhu, Z. Sun, D. Li, Z. Du, W. Zhang, et al., An efficient moving morphable component (MMC)-based approach for multi-resolution topology optimization, Struct. Multidiscip. Optim. 58 (2018) 2455–2479, https://doi.org/10.1007/s00158-018-2114-0.

[56] H. Liu, Y. Wang, H. Zong, M.Y. Wang, Efficient structure topology optimization by using the multiscale finite element method, Struct. Multidiscip. Optim. 58 (2018) 1411–1430, https://doi.org/10.1007/s00158-018-1972-9.

[57] W. Zhang, J. Yuan, J. Zhang, X. Guo, A new topology optimization approach based on Moving Morphable Components (MMC) and the ersatz material model, Struct. Multidiscip. Optim. 53 (2016) 1243–1260, https://doi.org/10.1007/s00158-015-1372-3.

[58] W. Zhang, J. Chen, X. Zhu, J. Zhou, D. Xue, X. Lei, et al., Explicit three dimensional topology optimization via Moving Morphable Void (MMV) approach, Comput. Meth. Appl. Mech. Eng. 322 (2017) 590–614, https://doi.org/10.1016/j.cma.2017.05.002.

[59] Z. Du, T. Cui, C. Liu, W. Zhang, Y. Guo, X. Guo, An efficient and easy-to-extend Matlab code of the Moving Morphable Component (MMC) method for three-dimensional topology optimization, Struct. Multidiscip. Optim. 65 (2022) 158, https://doi.org/10.1007/s00158-022-03239-4.

[60] D. Wang, C. Xiang, Y. Pan, A. Chen, X. Zhou, Y. Zhang, A deep convolutional neural network for topology optimization with perceptible generalization ability, Eng. Optimiz. 54 (2022) 973–988, https://doi.org/10.1080/0305215X.2021.1902998.

[61] X. Lei, C. Liu, Z. Du, W. Zhang, X. Guo, Machine learning-driven real-time topology optimization under moving morphable component-based framework, J. Appl. Mech.-Trans. ASME 86 (2019) 011004, https://doi.org/10.1115/1.4041319.

[62] Y. Yu, T. Hur, J. Jung, I.G. Jang, Deep learning for determining a near-optimal topological design without any iteration, Struct. Multidiscip. Optim. 59 (2019) 787–799, https://doi.org/10.1007/s00158-018-2101-5.

[63] H. Chi, Y. Zhang, T.L.E. Tang, L. Mirabella, L. Dalloro, L. Song, et al., Universal machine learning for topology optimization, Comput. Meth. Appl. Mech. Eng. 375 (2021) 112739, https://doi.org/10.1016/j.cma.2019.112739.

[64] F.V. Senhora, H. Chi, Y. Zhang, L. Mirabella, T.L.E. Tang, G.H. Paulino, Machine learning for topology optimization: Physics-based learning through an independent training strategy, Comput. Meth. Appl. Mech. Eng. 398 (2022) 115116, https://doi.org/10.1016/j.cma.2022.115116.

[65] M. Huang, Z. Du, C. Liu, Y. Zheng, T. Cui, Y. Mei, et al., Problem-independent machine learning (PIML)-based topology optimization—A universal approach, Extreme Mech. Lett. 56 (2022) 101887, https://doi.org/10.1016/j.eml.2022.101887.

[66] M. Huang, T. Cui, C. Liu, Z. Du, J. Zhang, C. He, et al., A Problem-Independent Machine Learning (PIML) enhanced substructure-based approach for large-scale structural analysis and topology optimization of linear elastic structures, Extreme Mech. Lett. 63 (2023) 102041, https://doi.org/10.1016/j.eml.2023.102041.

[67] M. Raissi, P. Perdikaris, G.E. Karniadakis, Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations, J. Comput. Phys. 378 (2019) 686–707, https://doi.org/10.1016/j.jcp.2018.10.045.

[68] E. Samaniego, C. Anitescu, S. Goswami, V.M. Nguyen-Thanh, H. Guo, K. Hamdia, et al., An energy approach to the solution of partial differential equations in computational mechanics via machine learning: Concepts, implementation and applications, Comput. Meth. Appl. Mech. Eng. 362 (2020) 112790, https://doi.org/10.1016/j.cma.2019.112790.

[69] J.N. Fuhg, N. Bouklas, The mixed deep energy method for resolving concentration features in finite strain hyperelasticity, J. Comput. Phys. 451 (2022) 110839, https://doi.org/10.1016/j.jcp.2021.110839.

[70] W. Zhang, D. Li, J. Yuan, J. Song, X. Guo, A new three-dimensional topology optimization method based on moving morphable components (MMCs), Comput. Mech. 59 (2017) 647–665, https://doi.org/10.1007/s00466-016-1365-0.

[71] G. Kreisselmeier, R. Steinhauser, Systematic control design by optimizing a vector performance index, IFAC Proc. 12 (1979) 113–117, https://doi.org/10.1016/S1474-6670(17)65584-8.

[72] Z. Du, W. Hao, X. Chen, X. Hou, W. Huo, C. Liu, et al., Artificial intelligence-enhanced bioinspiration: Design of optimized mechanical lattices beyond deep-sea sponges, Extreme Mech. Lett. 62 (2023) 102033, https://doi.org/10.1016/j.eml.2023.102033.

[73] O. Fryazinov, T. Vilbrandt, A. Pasko, Multi-scale space-variant FRep cellular structures, Comput.-Aided Des. 45 (2013) 26–34, https://doi.org/10.1016/j.cad.2011.09.007.

[74] L. Piegl, W. Tiller, The NURBS Book Monographs in visual communications, Springer Berlin, Heidelberg, 1995, https://doi.org/10.1007/978-3-642-97385-7.

[75] F. Niu, S. Xu, G. Cheng, A general formulation of structural topology optimization for maximizing structural stiffness, Struct. Multidiscip. Optim. 43 (2011) 561–572, https://doi.org/10.1007/s00158-010-0585-8.

[76] M. Montemurro, On the structural stiffness maximisation of anisotropic continua under inhomogeneous Neumann–Dirichlet boundary conditions, Compos. Struct. 287 (2022) 115289, https://doi.org/10.1016/j.compstruct.2022.115289.

[77] K. Svanberg, The method of moving asymptotes—a new method for structural optimization, Int. J. Numer. Methods Eng. 24 (1987) 359–373, https://doi.org/10.1002/nme.1620240207.

[78] O. Sigmund, N. Aage, E. Andreassen, On the (non-)optimality of Michell structures, Struct. Multidiscip. Optim. 54 (2016) 361–373, https://doi.org/10.1007/s00158-016-1420-7.

[79] J.A. Simões, M.A. Vaz, S. Blatcher, M. Taylor, Influence of head constraint and muscle forces on the strain distribution within the intact femur, Med. Eng. Phys. 22 (2000) 453–459, https://doi.org/10.1016/S1350-4533(00)00056-4.

[80] P.J. Schneider, D.H. Eberly, Geometric tools for computer graphics, Elsevier, 2003, pp. 481–662, https://doi.org/10.1016/B978-1-55860-594-7.X5000-0.

[81] M. Aleksandrov, S. Zlatanova, D.J. Heslop, Voxelisation algorithms and data structures: a review, Sensors 21 (2021) 8241, https://doi.org/10.3390/s21248241.
