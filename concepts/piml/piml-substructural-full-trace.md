---
title: "保留全部边界节点位移的 PIML 子结构分析"
type: concept
aliases:
  - PIML Full Trace Substructural Analysis
tags:
  - PIML
  - substructure
  - static-condensation
  - schur-complement
status: draft
date_added: 2026-10-25
date_update: 2026-10-25
---

# 保留全部边界节点位移的 PIML 子结构分析

本页沿用 [[../substructure/exact-substructural-full-trace|精确 full-trace]] 的“矩阵组装 → 局部缩聚 → 接口求解 → 位移恢复”流程，保留全部边界节点位移，以 PIML 预测形函数的内部恢复矩阵（总览的路线 A），再通过能量投影构造局部刚度。假设线弹性静力、非重叠划分、接口协调、内部无载荷，位移约束位于子结构边界。

沿用精确页的 $\mathbf K^j,\mathbf K_s^j,\mathbf A_b^j,\mathbf U_\Gamma,\mathbf U$；预测算子及其解加帽号。$\mathbf K_s^j$ 即 [[piml-substructural|总览]] 的 $\mathbf K_{s,\mathrm{full}}^j$，$\mathbf T_{\mathrm{full}}^j,\mathbf N_{\mathrm{full}}^j$ 与精确页 §4.1 同义。边界骨架包含块间接口和物理外边界，共享自由度只计一次。

| 计算环节 | 精确 full-trace | PIML 替代 |
|---|---|---|
| 局部算子构造 | 分解内部块并求解 | 预测内部恢复矩阵，再作能量投影 |
| 全局接口求解 | 求解精确接口系统 | 保留组装与约束形式，使用预测局部刚度 |
| 内部恢复 | 局部回代 | 用构造刚度的同一预测矩阵恢复 |

## 1. 矩阵组装

细网格与局部刚度的定义同精确页：

$$
\mathbf K=\sum_e\mathbf A_e^{\mathsf T}\mathbf K_e\mathbf A_e,
\qquad
\mathbf K^j(\boldsymbol\eta^j)
=\sum_{e\subset\Omega^j}(\mathbf G_e^j)^{\mathsf T}\mathbf K_e\mathbf G_e^j
=\begin{bmatrix}\mathbf K_{bb}^j&\mathbf K_{bi}^j\\\mathbf K_{ib}^j&\mathbf K_{ii}^j\end{bmatrix}.
\tag{1}
$$

$\boldsymbol\eta^j$ 为局部材料参数；$\mathbf A_e,\mathbf G_e^j$ 分别提取全场和子结构中的单元位移。要求 $\mathbf K^j\succeq0,\mathbf K_{ii}^j\succ0$，具体条件同精确页。保留当前材料场的 $\mathbf K^j$ 作用，可不显式组装。

## 2. 局部缩聚刚度的 PIML 替代

学习目标为精确内部恢复矩阵，对应的 Schur 补用于刚度对照：

$$
\mathbf T_{\mathrm{full}}^j=-(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j,
\qquad
\mathbf K_s^j=\mathbf K_{bb}^j-\mathbf K_{bi}^j(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j.
\tag{2}
$$

用 $\widehat{\mathbf T}_{\mathrm{full}}^j=\mathcal F_{\mathrm{full}}(\boldsymbol\eta^j;\boldsymbol\theta)$ 替代内部恢复矩阵的精确求解，输出尺寸为 $n_i^j\times n_b^j$。$\mathcal F_{\mathrm{full}}$ 包含预测与约束补全，$\boldsymbol\theta$ 在在线求解时固定。

监督训练仍需离线精确标签；样本与训练目标见 [[piml-substructural#3.2 材料样本与训练目标|总览 §3.2]]、[[piml-substructural#3.2 材料样本与训练目标|总览 §3.2]]。模型复用以局部几何、离散、编号和材料参数域相容为前提。

### 2.1 显式局部刚度

补入固定单位边界块，以当前材料刚度作能量投影：

$$
\begin{aligned}
\widehat{\mathbf N}_{\mathrm{full}}^j
&=\begin{bmatrix}\mathbf I\\\widehat{\mathbf T}_{\mathrm{full}}^j\end{bmatrix},\\
\widehat{\mathbf K}_s^j
&=(\widehat{\mathbf N}_{\mathrm{full}}^j)^{\mathsf T}\mathbf K^j\widehat{\mathbf N}_{\mathrm{full}}^j\\
&=\mathbf K_{bb}^j+\mathbf K_{bi}^j\widehat{\mathbf T}_{\mathrm{full}}^j
+(\widehat{\mathbf T}_{\mathrm{full}}^j)^{\mathsf T}\mathbf K_{ib}^j
+(\widehat{\mathbf T}_{\mathrm{full}}^j)^{\mathsf T}\mathbf K_{ii}^j\widehat{\mathbf T}_{\mathrm{full}}^j.
\end{aligned}
\tag{3}
$$

预测内部场一般不满足平衡，四项式不能按精确 Schur 补简化。按

$$
\widehat{\mathbf K}_\Gamma
=\sum_j(\mathbf A_b^j)^{\mathsf T}\widehat{\mathbf K}_s^j\mathbf A_b^j,
\qquad
\mathbf F_\Gamma=\sum_j(\mathbf A_b^j)^{\mathsf T}\mathbf f_b^j
\tag{4}
$$

组装接口系统，外载只分配一次。局部预测刚度须对称半正定，并保持正确的刚体零空间；能量投影自动保证对称半正定，刚体再现仍需约束。具体条件见 [[piml-substructural#3.1 网络输出与力学约束|总览 §3.1]]。

### 2.2 隐式局部刚度作用

可不形成局部或全局接口矩阵。给定 $\mathbf v_\Gamma$，逐块计算

$$
\begin{aligned}
\mathbf v_b^j&=\mathbf A_b^j\mathbf v_\Gamma,\\
\begin{bmatrix}\mathbf a_b^j\\\mathbf a_i^j\end{bmatrix}
&=\mathbf K^j\begin{bmatrix}\mathbf v_b^j\\\widehat{\mathbf T}_{\mathrm{full}}^j\mathbf v_b^j\end{bmatrix},\\
\mathbf y_b^j&=\mathbf a_b^j+(\widehat{\mathbf T}_{\mathrm{full}}^j)^{\mathsf T}\mathbf a_i^j,
\qquad
\widehat{\mathbf K}_\Gamma\mathbf v_\Gamma
=\sum_j(\mathbf A_b^j)^{\mathsf T}\mathbf y_b^j.
\end{aligned}
\tag{5}
$$

相对精确页的隐式 Schur 补，内部线性求解被预测矩阵乘法替代；由于 $\mathbf a_i^j$ 一般非零，转置投影项不能省略。预测算子在同一次线性求解中保持固定。

#### 2.2.1 结合单元层 Matrix-Free

满足精确页的共享参考单元条件时，沿用

$$
\mathbf K_e=s_e\mathbf K_0,
\qquad
\mathcal K^j(\mathbf x)
=\sum_{e\subset\Omega^j}(\mathbf G_e^j)^{\mathsf T}s_e\mathbf K_0\mathbf G_e^j\mathbf x.
\tag{6}
$$

式 (5) 的局部作用变为

$$
\begin{bmatrix}\mathbf a_b^j\\\mathbf a_i^j\end{bmatrix}
=\mathcal K^j\left(\begin{bmatrix}\mathbf v_b^j\\\widehat{\mathbf T}_{\mathrm{full}}^j\mathbf v_b^j\end{bmatrix}\right),
\qquad
\mathbf y_b^j=\mathbf a_b^j+(\widehat{\mathbf T}_{\mathrm{full}}^j)^{\mathsf T}\mathbf a_i^j.
\tag{7}
$$

精确页需两次单元作用和一次内部求解；这里为一次单元作用及预测矩阵的正、转置乘法，不需在线分解 $\mathbf K_{ii}^j$。预测矩阵仍需保存或按需重新推理；详细实现见 [[../matrix-free/mf-piml-substructural#2. 完整接口路径|PIML Matrix-Free 完整接口路径]]。

## 3. 求解与位移恢复

精确与预测接口系统分别为

$$
\mathbf K_\Gamma\mathbf U_\Gamma=\mathbf F_\Gamma,
\qquad
\widehat{\mathbf K}_\Gamma\widehat{\mathbf U}_\Gamma=\mathbf F_\Gamma.
\tag{8}
$$

方程仅在自由行成立，受约束行施加同一给定位移。令 $D,F$ 为受约束、自由分量，$(\widehat{\mathbf U}_\Gamma)_D=\mathbf d_D$，实际求解

$$
(\widehat{\mathbf K}_\Gamma)_{FF}(\widehat{\mathbf U}_\Gamma)_F
=(\mathbf F_\Gamma)_F-(\widehat{\mathbf K}_\Gamma)_{FD}\mathbf d_D.
\tag{9}
$$

局部算子满足能量与零空间要求、支承消除全部全局零能模式时，自由子系统正定。预测系统的支承反力由受约束行残量计算。

### 3.1 显式求解

使用式 (4) 的组装矩阵，按式 (9) 修正右端，通过直接法或迭代法求解。

### 3.2 隐式求解

向迭代求解器提供式 (5) 的作用；输入受约束分量置零、输出取自由分量。非零给定位移的右端修正通过一次作用计算，正定时可用 CG。

### 3.3 共同的位移恢复

显式与隐式求解均用构造刚度的同一预测矩阵恢复：

$$
\widehat{\mathbf u}_b^j=\mathbf A_b^j\widehat{\mathbf U}_\Gamma,
\qquad
\widehat{\mathbf u}_i^j=\widehat{\mathbf T}_{\mathrm{full}}^j\widehat{\mathbf u}_b^j,
\qquad
\widehat{\mathbf U}
=\mathbf R_\Gamma^{\mathsf T}\widehat{\mathbf U}_\Gamma
+\sum_j(\mathbf R_i^j)^{\mathsf T}\widehat{\mathbf u}_i^j.
\tag{10}
$$

$\mathbf R_\Gamma,\mathbf R_i^j$ 与精确页一致，分别提取全场边界和本块内部自由度；共享边界只写一次。

## 4. 代数等价与代理误差

固定同一预测算子，显式与隐式实现代数等价；它们通常不等价于原细网格系统。预测矩阵取精确 $\mathbf T_{\mathrm{full}}^j$ 时，退化为精确 full-trace。

令 $\mathbf E^j=\widehat{\mathbf T}_{\mathrm{full}}^j-\mathbf T_{\mathrm{full}}^j$。固定单位边界块、使用同一材料刚度时有

$$
\widehat{\mathbf K}_s^j-\mathbf K_s^j
=(\mathbf E^j)^{\mathsf T}\mathbf K_{ii}^j\mathbf E^j\succeq0,
\tag{11}
$$

推导见 [[piml-substructural#4. 误差与使用边界|总览 §4]]。恢复后的内部残量为

$$
\mathbf r_i^j
=\mathbf K_{ib}^j\widehat{\mathbf u}_b^j+\mathbf K_{ii}^j\widehat{\mathbf u}_i^j
=\mathbf K_{ii}^j\mathbf E^j\widehat{\mathbf u}_b^j.
\tag{12}
$$

因此，代理系统求解收敛不代表原细网格平衡成立。相同载荷、零内部载荷、齐次位移约束、同一预测形函数组装与恢复且系统正定时，Ritz 正交性还给出（本页推导）

$$
C-\widehat C=\|\mathbf U-\widehat{\mathbf U}\|_{\mathbf K}^2\ge0,
\qquad
C=\mathbf F^{\mathsf T}\mathbf U,\quad
\widehat C=\mathbf F^{\mathsf T}\widehat{\mathbf U}.
\tag{13}
$$

这里 $\mathbf U$ 为精确细网格解，范数在自由分量上定义。完整接口没有迹降阶误差，预测系统的偏硬来自内部延拓代理。非零给定位移不能直接套用式 (13)，浮点与求解容差误差另计。
