---
title: "子结构有限元与静力缩聚"
type: concept
aliases:
  - Substructure FEM
  - Static Condensation
  - Schur Complement Condensation
  - 精确全接口静力缩聚
  - 角点线性迹降阶
tags:
  - finite-element
  - substructure
  - static-condensation
  - schur-complement
status: in-progress
date_added: 2026-08-09
date_update: 2026-09-02
---

# 子结构有限元与静力缩聚

子结构静力缩聚首先通过 Exact Schur 消去各子结构的内部自由度，同时保留全部接口自由度；在此基础上，可以进一步选取低维接口迹空间压缩接口。精确全接口缩聚与原有限元系统代数等价，接口迹空间降阶则是在精确缩聚系统上施加的 Ritz 子空间近似。接口迹空间可以采用多种构造方式，本页重点介绍角点线性迹降阶。

## 定义与边界

本页维护经典子结构有限元的稳定数学骨架，并明确区分两个递进层次：

$$
\text{原始有限元系统}
\xrightarrow{\text{Exact Schur}}
\text{精确全接口系统}
\xrightarrow{\mathbf u_b^j=\mathbf T_j\mathbf q_j}
\text{低维接口迹系统}.
$$

| 层次 | 局部内部消元 | 接口迹空间 | 与原离散系统的关系 |
|---|---|---|---|
| 精确全接口静力缩聚 | Exact Schur | `full_trace`，保留全部边界自由度 | 满足本页所列前提时代数等价 |
| 接口迹空间降阶 | Exact Schur | 低阶多项式、谱基、POD 基或自适应富集基等 | Ritz 子空间近似；角点线性迹通常偏硬 |

两层的区别不在于 Schur 补是否精确，而在于是否继续限制接口位移空间。角点线性迹降阶对应第二层中的 `linear_corner` 特例。

## 1. 子结构划分、边界与固定符号

子结构可以理解为把细网格单元分成若干组：**一个子结构包含许多单元，不是一个大单元**。划分不改变原来的细网格，也不把相邻部分断开。

![[substructure-partition.svg]]

图中按“整体划分—单块放大—节点分层”展示同一个三维例子。整个结构沿 $x,y,z$ 方向分别划分为 12、4、4 个子结构，共 $12\times4\times4=192$ 个；每个子结构沿三个方向各含 4 个六面体单元，共 $4\times4\times4=64$ 个。第一幅每个小块表示一个子结构，第二幅每个小格才表示一个单元。

全网格沿各方向的单元数为 $(12\times4)\times(4\times4)\times(4\times4)=48\times16\times16$，共 12,288 个单元。对一阶六面体位移元，每个子结构沿每个方向有 5 个节点，共 $5^3=125$ 个节点。

第三幅将这 125 个节点沿 $z$ 方向分成五层展开。顶、底两层各有 25 个节点，全部位于子结构边界；中间三层各有 16 个边界节点和 9 个内部节点。因此，内部节点共 $3\times9=27$ 个，边界节点共 $2\times25+3\times16=98$ 个。三维位移元每节点有三个位移自由度，对应内部 $27\times3=81$ 个、边界 $98\times3=294$ 个自由度。

缩聚时先消去蓝色内部节点的位移未知量，保留红色边界节点的位移未知量。相邻子结构的共享边界节点在全局装配时合并；接口系统求解后，再逐块恢复内部位移。这里的“边界”相对于每个子结构而言，既包括块间公共接口，也包括位于整个结构外边界的部分；**保留边界位移不等于把边界固定**，固定条件仍由原物理问题决定。

边界节点包括面内节点、棱上节点和角点；完整接口缩聚保留它们的全部位移自由度，而非只保留八个角点。公共边界节点由邻块共享，不能用每块边界自由度乘块数来计算全局接口自由度。

### 1.1 连续域划分与边界集合

设线弹性域 $\Omega\subset\mathbb R^d$（$d=2,3$）被划分为 $M$ 个子结构 $\Omega^j$。非重叠的准确含义是子结构内部互不相交，而闭包允许在公共接口相交：

$$
\overline\Omega=\bigcup_{j=1}^{M}\overline{\Omega^j},
\qquad
(\Omega^j)^\circ\cap(\Omega^k)^\circ=\varnothing
\quad(j\ne k).
$$

内部骨架定义为

$$
\Gamma_{\mathrm{int}}
=
\bigcup_{j<k}
\left(\partial\Omega^j\cap\partial\Omega^k\right).
$$

外边界另行分为 Dirichlet 与 Neumann 部分：

$$
\partial\Omega
=
\overline{\Gamma_D}\cup\overline{\Gamma_N},
\qquad
\Gamma_D\cap\Gamma_N=\varnothing.
$$

$\Gamma_{\mathrm{int}}$ 上的界面力是相邻子结构之间的未知作用—反作用；$\Gamma_N$ 上才施加给定物理面力。装配时内部界面力通过平衡相消，不能把同一 Neumann 载荷在相邻子结构上重复计入。

全域弱形式与材料张量的基本约定见[[linear-elasticity|线弹性]]。本页从其有限元离散后的局部代数系统出发。

### 1.2 固定符号

对第 $j$ 个子结构，统一使用以下符号：

| 符号 | 含义 |
|---|---|
| $\mathbf u_i^j,\mathbf u_b^j$ | 内部自由度与完整边界自由度 |
| $\mathbf N_{\mathrm{int}}^j$ | 内部位移关于完整边界位移的齐次恢复矩阵 |
| $\mathbf H_j=[(\mathbf N_{\mathrm{int}}^j)^{\mathsf T},\mathbf I]^{\mathsf T}$ | 从完整边界位移扩展到全部局部自由度的算子 |
| $\mathbf T_j$ | 从一般降阶接口坐标映射到完整边界位移的局部迹基 |
| $\mathbf L_j$ | $\mathbf T_j$ 的角点线性插值特例 |
| $\mathbf A_j$ | 从全局接口向量提取第 $j$ 个局部完整接口向量的 Boolean 矩阵 |
| $\mathbf A_{c,j}$ | 从全局粗接口向量提取第 $j$ 个局部角点向量的 Boolean 矩阵 |
| $\mathbf K_s^j$ | 精确完整接口 Schur 缩聚刚度 |
| $\mathbf K_c^j$ | 角点线性迹降阶后的局部刚度 |

$\mathbf L_j$ 只表示局部迹插值，$\mathbf A_j$ 与 $\mathbf A_{c,j}$ 只表示局部—全局 Boolean 装配；二者不得共用符号。

## 2. Schur 补静力缩聚的严谨数学推导

本节是第一层：**Exact Schur + full trace**。它只消去内部自由度，完整保留子结构边界上的有限元迹自由度。通过静力平衡消去非保留自由度的经典做法通常称为 Guyan reduction [1]。

### 2.1 局部分块系统与可解性

按内部自由度 $i$ 与边界自由度 $b$ 排列后，局部系统为

$$
\begin{bmatrix}
\mathbf K_{ii}^j & \mathbf K_{ib}^j\\
\mathbf K_{bi}^j & \mathbf K_{bb}^j
\end{bmatrix}
\begin{bmatrix}
\mathbf u_i^j\\
\mathbf u_b^j
\end{bmatrix}
=
\begin{bmatrix}
\mathbf f_i^j\\
\mathbf f_b^j+\boldsymbol\lambda^j
\end{bmatrix},
\qquad
\mathbf K_{bi}^j=(\mathbf K_{ib}^j)^{\mathsf T}.
$$

$\boldsymbol\lambda^j$ 表示完整接口上的相互作用力。局部完整刚度 $\mathbf K^j$ 对自由漂浮子结构通常因刚体模态而半正定，但这不妨碍 $\mathbf K_{ii}^j$ 可逆。要断言 $\mathbf K_{ii}^j$ 对称正定，至少需要：

- 线弹性材料张量在实体区域上一致正定；密度法中需有严格正的刚度下界；
- 子结构网格连通，且固定完整边界迹后不存在内部机构、孤立分量或零能模式；
- 内部/边界自由度划分正确，局部离散与约束没有秩缺失。

若这些条件不成立，不能直接使用 Cholesky 或无条件写 $(\mathbf K_{ii}^j)^{-1}$；应先处理奇异性。下文的逆矩阵记号均表示求解线性方程组，数值实现不应显式构造逆矩阵。

### 2.2 内部恢复、非零内部载荷与列问题

第一行给出

$$
\mathbf u_i^j
=
(\mathbf K_{ii}^j)^{-1}\mathbf f_i^j
-
(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j\mathbf u_b^j.
$$

定义

$$
\boxed{
\mathbf N_{\mathrm{int}}^j
:=
-(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j
},
\qquad
\mathbf w_i^j
:=
(\mathbf K_{ii}^j)^{-1}\mathbf f_i^j,
$$

则一般恢复式为

$$
\boxed{
\mathbf u_i^j
=
\mathbf w_i^j
+
\mathbf N_{\mathrm{int}}^j\mathbf u_b^j
}.
$$

当 $\mathbf f_i^j=\mathbf0$ 时，$\mathbf w_i^j=\mathbf0$，内部位移完全由边界迹决定。$\mathbf N_{\mathrm{int}}^j$ 的第 $k$ 列由

$$
\mathbf K_{ii}^j
(\mathbf N_{\mathrm{int}}^j)_{:,k}
=
-\mathbf K_{ib}^j\mathbf e_k
$$

确定：令第 $k$ 个边界自由度取单位值、其余边界自由度为零，再求解内部平衡。这是边界迹的**离散调和延拓**；所有列共享同一次 $\mathbf K_{ii}^j$ 分解。

### 2.3 精确 Schur 补与缩聚载荷

将内部恢复式代入第二行，得到

$$
\boxed{
\mathbf K_s^j\mathbf u_b^j
=
\widetilde{\mathbf f}_b^j+\boldsymbol\lambda^j
},
$$

其中

$$
\boxed{
\mathbf K_s^j
=
\mathbf K_{bb}^j
-
\mathbf K_{bi}^j
(\mathbf K_{ii}^j)^{-1}
\mathbf K_{ib}^j
},
$$

$$
\boxed{
\widetilde{\mathbf f}_b^j
=
\mathbf f_b^j
-
\mathbf K_{bi}^j
(\mathbf K_{ii}^j)^{-1}
\mathbf f_i^j
}.
$$

利用对称性与 $\mathbf N_{\mathrm{int}}^j$ 的定义，也可写成

$$
\widetilde{\mathbf f}_b^j
=
\mathbf f_b^j
+
(\mathbf N_{\mathrm{int}}^j)^{\mathsf T}\mathbf f_i^j.
$$

因此，$\mathbf f_i^j=\mathbf0$ 只是常用简化，不是静力缩聚成立的必要条件。自重、离心力、热等效载荷或其他体力作用在内部自由度上时，必须同时缩聚载荷并保留 $\mathbf w_i^j$。

### 2.4 全场扩展、能量与变分性质

对齐次内部载荷定义全场扩展算子

$$
\boxed{
\mathbf H_j
=
\begin{bmatrix}
\mathbf N_{\mathrm{int}}^j\\
\mathbf I
\end{bmatrix}
},
\qquad
\mathbf u^j=\mathbf H_j\mathbf u_b^j.
$$

由 $\mathbf K_{ii}^j\mathbf N_{\mathrm{int}}^j+\mathbf K_{ib}^j=\mathbf0$ 可得

$$
\boxed{
\mathbf K_s^j
=
\mathbf H_j^{\mathsf T}
\mathbf K^j
\mathbf H_j
}.
$$

当 $\mathbf f_i^j=\mathbf0$ 时，局部应变能严格满足

$$
\frac12(\mathbf u^j)^{\mathsf T}\mathbf K^j\mathbf u^j
=
\frac12(\mathbf u_b^j)^{\mathsf T}\mathbf K_s^j\mathbf u_b^j.
$$

当 $\mathbf f_i^j\ne\mathbf0$ 时，使用仿射恢复

$$
\mathbf u^j
=
\begin{bmatrix}\mathbf w_i^j\\\mathbf0\end{bmatrix}
+
\mathbf H_j\mathbf u_b^j,
$$

消元后的总势能除去与 $\mathbf u_b^j$ 无关的常数后为

$$
\Pi_s^j(\mathbf u_b^j)
=
\frac12(\mathbf u_b^j)^{\mathsf T}\mathbf K_s^j\mathbf u_b^j
-
(\mathbf u_b^j)^{\mathsf T}\widetilde{\mathbf f}_b^j.
$$

因此，$\mathbf N_{\mathrm{int}}^j$ 给出固定边界迹下的离散能量极小延拓，$\mathbf K_s^j$ 是相应的边界 Dirichlet-to-Neumann 离散算子。

### 2.5 全局完整接口装配

设 $\mathbf U_\Gamma$ 是去重后的全局完整接口向量，Boolean 矩阵 $\mathbf A_j$ 满足

$$
\mathbf u_b^j=\mathbf A_j\mathbf U_\Gamma.
$$

内部界面作用力在装配中相消后，全局完整接口系统为

$$
\boxed{
\mathbf K_\Gamma
=
\sum_{j=1}^{M}
\mathbf A_j^{\mathsf T}\mathbf K_s^j\mathbf A_j
},
$$

$$
\boxed{
\mathbf F_\Gamma
=
\sum_{j=1}^{M}
\mathbf A_j^{\mathsf T}\widetilde{\mathbf f}_b^j
}.
$$

施加 $\Gamma_D$ 上的约束后求解 $\mathbf K_\Gamma\mathbf U_\Gamma=\mathbf F_\Gamma$，再逐子结构恢复 $\mathbf u_b^j$ 与 $\mathbf u_i^j$。外载可以在全局层统一生成，也可以一致地分配到局部向量后装配，但同一物理载荷只能计入一次。

### 2.6 “精确等价”的条件与边界

精确全接口静力缩聚与原有限元离散系统代数等价，需要同时满足：

1. 保留全部子结构接口有限元自由度，即 `full_trace`；
2. $\mathbf K_{ii}^j$ 可逆，局部线性方程与 Schur 补计算达到所需精度；
3. 非零内部载荷通过 $\widetilde{\mathbf f}_b^j$ 缩聚，并通过 $\mathbf w_i^j$ 恢复；
4. $\mathbf A_j$ 正确识别共享接口自由度，载荷、Dirichlet 条件与接口平衡一致；
5. 原有限元问题在施加必要的全局约束后可解。

这里的“等价”是**相对于同一个已离散有限元系统**的代数等价，不表示有限元离散与连续真解无误差。只要进一步施加 $\mathbf u_b^j=\mathbf T_j\mathbf q_j$，且 $\operatorname{range}(\mathbf T_j)$ 是完整接口空间的真子空间，一般便不再属于这一等价性结论；角点线性迹 $\mathbf T_j=\mathbf L_j$ 是其中一个特例。

## 3. 接口迹空间降阶：建立在精确全接口层上的第二层

### 3.1 常见接口迹空间

设 $\mathbf q_j$ 为第 $j$ 个子结构的降阶接口坐标，$\mathbf T_j$ 为相应局部迹基，则一般接口降阶写为

$$
\boxed{
\mathbf u_b^j=\mathbf T_j\mathbf q_j
}.
$$

代入精确完整接口系统可得

$$
\boxed{
\mathbf K_r^j
=
\mathbf T_j^{\mathsf T}\mathbf K_s^j\mathbf T_j
},
\qquad
\boxed{
\mathbf f_r^j
=
\mathbf T_j^{\mathsf T}\widetilde{\mathbf f}_b^j
}.
$$

常见的接口迹空间构造方式包括：

| 类型 | 基本构造 | 主要特点 |
|---|---|---|
| 角点低阶多项式迹 | 由角点自由度对边、面上的位移作线性、双线性或三线性插值 | 构造简单、粗自由度少；难以表示复杂接口变形 |
| 高阶多项式迹 | 在边或面上增加高阶节点、层次多项式或高阶形函数 | 几何意义清楚，可系统提高阶次，但粗系统规模随阶次增长 |
| 谱或局部特征模态迹 | 求解接口或局部广义特征值问题，保留低频或低能模态 | 能按谱信息控制空间规模，适合复杂或非均质子结构 |
| POD/降阶基迹 | 对接口位移快照进行 POD 或 SVD，选取主导模态 | 对训练参数域内的数据分布效率较高，但依赖快照代表性 |
| 能量最小化或多尺度迹 | 以局部能量最小延拓构造多尺度接口基 | 能吸收材料非均质性，构造成本通常高于几何插值 |
| 自适应富集迹 | 根据残差、误差指标或局部谱信息逐步增加接口基 | 可针对难点区域控制误差，但需要额外的估计与更新机制 |

这些方法共享同一个 Exact Schur 局部消元层，区别在于 $\operatorname{range}(\mathbf T_j)$ 的构造。Craig–Bampton Component Mode Synthesis 还会引入固定接口内部模态 [2]，其降阶空间不只作用于接口迹，因此不属于这里的纯接口迹降阶。BDDC [3] 与 FETI-DP [4] 中的粗空间主要服务于迭代求解和预条件，也不应直接等同于物理模型的接口迹降阶。

下面重点讨论最简单且与 Huang 2023 子结构构造直接对应的角点线性迹，即取 $\mathbf T_j=\mathbf L_j$。

### 3.2 角点线性迹假设与算子层级

设 $\mathbf u_c^j$ 为第 $j$ 个子结构角点上的粗自由度，$\mathbf L_j$ 将角点位移线性插值到完整边界迹：

$$
\boxed{
\mathbf u_b^j
=
\mathbf L_j\mathbf u_c^j
}.
$$

二维规则四边形子结构通常使用角点双线性迹，三维规则六面体子结构通常使用八角点三线性迹。这里“线性”指预设的低阶边界变形模式，不表示局部材料场或内部解必须均匀。

在第一层全场扩展算子之上定义

$$
\boxed{
\mathbf H_j^L
:=
\mathbf H_j\mathbf L_j
=
\begin{bmatrix}
\mathbf N_{\mathrm{int}}^j\mathbf L_j\\
\mathbf L_j
\end{bmatrix}
}.
$$

这三个算子必须分层理解：

$$
\mathbf u_c^j
\xrightarrow{\mathbf L_j}
\mathbf u_b^j
\xrightarrow{\mathbf H_j}
\mathbf u^j,
\qquad
\mathbf u^j=\mathbf H_j^L\mathbf u_c^j.
$$

### 3.3 角点降阶刚度、载荷与恢复

将 $\mathbf u_b^j=\mathbf L_j\mathbf u_c^j$ 代入完整接口势能，得到

$$
\boxed{
\mathbf K_c^j
=
\mathbf L_j^{\mathsf T}\mathbf K_s^j\mathbf L_j
=
(\mathbf H_j^L)^{\mathsf T}\mathbf K^j\mathbf H_j^L
},
$$

$$
\boxed{
\mathbf f_c^j
=
\mathbf L_j^{\mathsf T}\widetilde{\mathbf f}_b^j
}.
$$

求得 $\mathbf u_c^j$ 后，细尺度位移按

$$
\mathbf u_b^j=\mathbf L_j\mathbf u_c^j,
\qquad
\mathbf u_i^j
=
\mathbf w_i^j
+
\mathbf N_{\mathrm{int}}^j\mathbf L_j\mathbf u_c^j
$$

恢复。Huang 2023 式 (16) 正对应这一层的 $\mathbf H_j^L$ 与 $\mathbf K_c^j$；论文特有的 PIML 输出约束与训练路线见[[piml/piml-substructural|子结构 PIML]]和[[../literature/topopt/piml/translations/Huang2023-PIML-substructure-zh|Huang 2023 中文译文]]。

### 3.4 全局粗接口装配

设 $\mathbf U_C$ 为去重后的全局粗接口向量，Boolean 矩阵 $\mathbf A_{c,j}$ 满足

$$
\mathbf u_c^j=\mathbf A_{c,j}\mathbf U_C.
$$

则全局宏观系统为

$$
\boxed{
\mathbf K_C
=
\sum_{j=1}^{M}
\mathbf A_{c,j}^{\mathsf T}
\mathbf K_c^j
\mathbf A_{c,j}
},
$$

$$
\boxed{
\mathbf F_C
=
\sum_{j=1}^{M}
\mathbf A_{c,j}^{\mathsf T}
\mathbf f_c^j
}.
$$

$\mathbf A_{c,j}$ 负责角点的共享与装配，$\mathbf L_j$ 负责同一子结构内从角点到完整边界的插值，二者作用空间不同。

### 3.5 Ritz 子空间、偏硬性与误差边界

线性迹法把完整接口解限制在较小的试验空间

$$
\mathbf u_b^j\in\operatorname{range}(\mathbf L_j).
$$

在施加 Dirichlet 条件后的全局完整接口算子对称正定、载荷投影一致时，粗解是完整接口能量内积下的 Galerkin/Ritz 投影。因此它具有最佳逼近性质：

$$
\|\mathbf U_\Gamma-\mathbf U_L\|_{\mathbf K_\Gamma}
=
\min_{\mathbf V\in\mathcal V_L}
\|\mathbf U_\Gamma-\mathbf V\|_{\mathbf K_\Gamma},
$$

其中 $\mathcal V_L$ 是所有局部线性迹经过兼容装配形成的全局子空间。对同一力控制问题，柔度满足

$$
C-C_L
=
\|\mathbf U_\Gamma-\mathbf U_L\|_{\mathbf K_\Gamma}^2
\ge0.
$$

所以该模型通常表现为偏硬，即粗解柔度不大于完整接口解柔度。但这一结论不意味着每个位移分量都单调偏小，也不替代具体问题的误差估计。

线性迹层在以下情形下可以给出精确接口结果：完整接口解恰好落在 $\mathcal V_L$ 中。一般非均质材料、局部高梯度、复杂载荷或角部/接口附近的细尺度变形不会满足这一条件。可通过高阶多项式迹、谱/模态迹、POD 基或自适应富集扩大接口空间；这些都属于 `TraceBasis` 的替代，而不是改变 Exact Schur 的局部消元。

## 4. 结构性质与可选扩展

### 4.1 刚体模态保持

对自由漂浮且除刚体运动外没有其他机构的子结构，局部完整刚度与缩聚刚度均为对称半正定。设完整接口上的刚体模态矩阵为 $\mathbf R_b^j$，内部对应模态为 $\mathbf R_i^j$，则精确缩聚满足

$$
\mathbf K_s^j\mathbf R_b^j=\mathbf0,
\qquad
\mathbf N_{\mathrm{int}}^j\mathbf R_b^j=\mathbf R_i^j.
$$

刚体模态数为 $d(d+1)/2$：二维为两个平动与一个转动，三维为三个平动与三个转动。线性迹空间要保持刚体运动，必须满足

$$
\operatorname{range}(\mathbf R_b^j)
\subseteq
\operatorname{range}(\mathbf L_j).
$$

### 4.2 变形正交补与 Cholesky 结构保持

对 $\mathbf R_b^j$ 做正交分解，取其正交补基 $\mathbf R_\perp^j$：

$$
(\mathbf R_b^j)^{\mathsf T}\mathbf R_\perp^j=\mathbf0,
\qquad
(\mathbf R_\perp^j)^{\mathsf T}\mathbf R_\perp^j=\mathbf I.
$$

若局部系统除刚体模态外没有其他零能机构，则限制刚度

$$
\mathbf K_{s,\perp}^j
=
(\mathbf R_\perp^j)^{\mathsf T}
\mathbf K_s^j
\mathbf R_\perp^j
$$

对称正定。令 $\mathbf C_j$ 为其 Cholesky 因子，可以写成

$$
\mathbf K_s^j
=
\mathbf R_\perp^j
\mathbf C_j\mathbf C_j^{\mathsf T}
(\mathbf R_\perp^j)^{\mathsf T}.
$$

这里使用 $\mathbf C_j$ 而不是 $\mathbf L_j$ 表示 Cholesky 因子，以免与迹插值矩阵混淆。该参数化可用于构造保持对称半正定性和刚体零空间的代理算子，但它是结构保持扩展，不是 Exact Schur 或线性迹降阶的必要步骤。

## 参考文献与相关页面

### 已入库文献

- [[../literature/topopt/piml/translations/Huang2023-PIML-substructure-zh|Huang et al. (2023) 中文译文]]：式 (6)–(9) 给出经典子结构分块、Schur 缩聚与位移恢复；式 (16) 给出角点线性迹降阶；式 (17) 给出从形函数/扩展算子构造局部刚度的能量关系。

### 未入库参考文献

1. GUYAN R J. Reduction of stiffness and mass matrices[J]. *AIAA Journal*, 1965, 3(2): 380. DOI: [10.2514/3.2874](https://doi.org/10.2514/3.2874).
2. CRAIG R R, BAMPTON M C C. Coupling of substructures for dynamic analyses[J]. *AIAA Journal*, 1968, 6(7): 1313–1319. DOI: [10.2514/3.4741](https://doi.org/10.2514/3.4741).
3. DOHRMANN C R. A preconditioner for substructuring based on constrained energy minimization[J]. *SIAM Journal on Scientific Computing*, 2003, 25(1): 246–258. DOI: [10.1137/S1064827502412887](https://doi.org/10.1137/S1064827502412887).
4. FARHAT C, LESOINNE M, LE TALLEC P, et al. FETI-DP: A dual–primal unified FETI method—Part I: A faster alternative to the two-level FETI method[J]. *International Journal for Numerical Methods in Engineering*, 2001, 50(7): 1523–1544. DOI: [10.1002/nme.76](https://doi.org/10.1002/nme.76).

### 相关页面

- [[linear-elasticity|线弹性]]：全域弱形式、材料正定性和位移型有限元背景。
- [[piml/piml-substructural|子结构静力缩聚 PIML 算子与物理正定范式]]
- [[matrix-free/mf-ea-substructural|子结构载体 EA Matrix-Free 算子]]
- [[matrix-free/assembly-levels|有限元装配层次]]
- [[../research/piml-matrix-free-gpu/project-plan|PIML–Matrix-Free–GPU 项目计划]]

本页关于非零内部载荷、全接口装配、Ritz 投影与误差恒等的公式由分块高斯消元和对称 Galerkin 投影直接推导。
