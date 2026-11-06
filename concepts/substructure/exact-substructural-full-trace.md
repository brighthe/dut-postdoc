---
title: "保留全部边界节点位移的精确子结构分析"
type: concept
aliases:
  - full_trace
  - 完整边界位移子结构分析
  - Full Trace Static Condensation
tags:
  - finite-element
  - substructure
  - static-condensation
  - schur-complement
status: draft
date_added: 2026-10-23
date_update: 2026-10-25
---

# 保留全部边界节点位移的精确子结构分析

`full_trace` 在各子结构内消去内部自由度，保留全部边界节点位移，求解全局边界方程后回代内部位移。本文考虑线弹性静力问题，子结构沿细网格单元边界非重叠划分、界面协调，内部载荷为零，位移约束位于子结构边界上。

记局部边界、内部位移为 $\mathbf u_b^j,\mathbf u_i^j$，全场位移为 $\mathbf U\in\mathbb R^{N_h}$，全局边界位移为 $\mathbf U_\Gamma\in\mathbb R^{N_\Gamma}$。边界骨架 $\Gamma=\bigcup_j\partial\Omega^j$ 包含块间界面和物理外边界上的全部节点，共享自由度按全局编号只计一次。

`full_trace` 指保留全部边界位移。显式 Schur 补形成缩聚矩阵，隐式 Schur 补只计算其向量作用；共享参考单元 EA 则用于实现局部刚度作用，可与隐式 Schur 补结合，不改变边界空间或缩聚算子。两者的组合如下：

| 局部刚度作用 | 显式 Schur 补（§2.1） | 隐式 Schur 补（§2.2） |
|---|---|---|
| 局部刚度块 | 形成 $\mathbf K_s^j$ 并组装 $\mathbf K_\Gamma$ | 局部块乘法加内部求解，式 (5) |
| 共享参考单元 EA（§2.2.1） | 一般不组合：仍须逐块形成 $\mathbf K_s^j$ 并存储 $\mathbf K_\Gamma$，单元层作用不减少这部分存储 | 两次单元作用加内部求解，式 (7) |

以本页为精确基准、预测内部恢复矩阵并通过能量投影构造局部刚度的分析见 [[../piml/piml-substructural-full-trace|保留全部边界节点位移的 PIML 子结构分析]]。

## 1. 矩阵组装

传统有限元将单元刚度 $\mathbf K_e$ 组装为全局矩阵；子结构方法按块组织单元，局部矩阵按边界 $b$、内部 $i$ 分块：

$$
\mathbf K=\sum_e\mathbf A_e^{\mathsf T}\mathbf K_e\mathbf A_e,
\qquad
\mathbf K^j=\sum_{e\subset\Omega^j}(\mathbf G_e^j)^{\mathsf T}\mathbf K_e\mathbf G_e^j
=\begin{bmatrix}
\mathbf K_{bb}^j&\mathbf K_{bi}^j\\
\mathbf K_{ib}^j&\mathbf K_{ii}^j
\end{bmatrix}.
\tag{1}
$$

$\mathbf A_e$、$\mathbf G_e^j$ 分别从全场和子结构位移中提取单元位移。式 (1) 定义矩阵关系；采用单元层实现时，无需完整存储 $\mathbf K^j$。

## 2. 静力缩聚

内部无载荷，且固定边界后的 $\mathbf K_{ii}^j$ 可逆时，内部平衡给出

$$
\mathbf K_{ib}^j\mathbf u_b^j+\mathbf K_{ii}^j\mathbf u_i^j=\mathbf0
\quad\Longrightarrow\quad
\mathbf u_i^j=-(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j\mathbf u_b^j.
\tag{2}
$$

代入边界行的刚度作用，得到局部 Schur 补：

$$
\mathbf K_{bb}^j\mathbf u_b^j+\mathbf K_{bi}^j\mathbf u_i^j
=\mathbf K_s^j\mathbf u_b^j,
\qquad
\mathbf K_s^j=\mathbf K_{bb}^j-\mathbf K_{bi}^j(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j.
\tag{3}
$$

以下逆矩阵均通过线性系统求解实现。令 $\mathbf A_b^j$ 提取本块边界位移，即 $\mathbf u_b^j=\mathbf A_b^j\mathbf U_\Gamma$；$\mathbf f_b^j$ 为本块外载荷，各外载荷只分配一次。

自由漂浮子结构的完整局部刚度可能因刚体运动而半正定，这不妨碍固定完整边界后的内部块可逆；密度法须保留严格正的刚度下界。

**内部求解。** 在线弹性材料张量一致正定、子结构网格连通且固定完整边界后无内部机构、孤立分量或离散零能模式的条件下， $\mathbf K_{ii}^j$ 对称正定，取 Cholesky 分解 $\mathbf K_{ii}^j=\mathbf L_i^j(\mathbf L_i^j)^{\mathsf T}$，每次内部求解化为两次三角回代。因子逐子结构缓存，系数不变时供式 (3) 的缩聚或式 (5) 的算子作用、迭代求解的预条件对角以及式 (10) 的位移恢复复用，密度更新后重新组装分解。改用 LU 等其他精确分解只影响计算量与舍入，不改变第 4 节的等价性。

### 2.1 显式 Schur 补

形成各块 $\mathbf K_s^j$，组装全局边界矩阵与载荷：

$$
\mathbf K_\Gamma=\sum_j(\mathbf A_b^j)^{\mathsf T}\mathbf K_s^j\mathbf A_b^j
\in\mathbb R^{N_\Gamma\times N_\Gamma},
\qquad
\mathbf F_\Gamma=\sum_j(\mathbf A_b^j)^{\mathsf T}\mathbf f_b^j.
\tag{4}
$$

### 2.2 隐式 Schur 补

不形成 $\mathbf K_s^j$ 和 $\mathbf K_\Gamma$，载荷仍按式 (4) 组装。给定边界输入向量 $\mathbf v_\Gamma$，逐块提取、内部求解并累加：

$$
\begin{aligned}
\mathbf v_b^j&=\mathbf A_b^j\mathbf v_\Gamma,
&\mathbf K_{ii}^j\mathbf z_i^j&=\mathbf K_{ib}^j\mathbf v_b^j,\\
\mathbf y_b^j&=\mathbf K_{bb}^j\mathbf v_b^j-\mathbf K_{bi}^j\mathbf z_i^j,
&\mathbf K_\Gamma\mathbf v_\Gamma&=\sum_j(\mathbf A_b^j)^{\mathsf T}\mathbf y_b^j.
\end{aligned}
\tag{5}
$$

其中 $\mathbf z_i^j$ 是辅助求解向量。代入其表达式即得 $\mathbf y_b^j=\mathbf K_s^j\mathbf v_b^j$，因此这就是 Schur 层的 Matrix-Free；局部刚度块仍可显式存储。

#### 2.2.1 结合单元层 Matrix-Free

进一步用**共享参考单元 EA**替代局部块乘法。适用条件是各单元的类型、尺寸与形状、坐标方向、局部自由度排列及积分规则相同，本构仅按单元标量 $s_e$ 缩放。记共享基准刚度为 $\mathbf K_0$，则

$$
\mathbf K_e=s_e\mathbf K_0,
\qquad
\mathcal K^j(\mathbf x)
=\sum_{e\subset\Omega^j}(\mathbf G_e^j)^{\mathsf T}s_e\mathbf K_0(\mathbf G_e^j\mathbf x)
=\mathbf K^j\mathbf x.
\tag{6}
$$

例如固定泊松比的 SIMP 模型，取 $s_e=E(\rho_e)/E_0$，其中 $\rho_e$ 为单元内恒定的物理密度，$\mathbf K_0$ 按基准模量 $E_0$ 计算。单元刚度数据只保存一份 $\mathbf K_0$ 和各单元的 $s_e$，式 (5) 的局部作用改写为

$$
\begin{bmatrix}\mathbf a_b^j\\\mathbf a_i^j\end{bmatrix}
=\mathcal K^j\left(\begin{bmatrix}\mathbf v_b^j\\\mathbf0\end{bmatrix}\right),
\qquad
\mathbf K_{ii}^j\mathbf z_i^j=\mathbf a_i^j,
\qquad
\mathbf y_b^j=\mathbf a_b^j-
\left[\mathcal K^j\left(\begin{bmatrix}\mathbf0\\\mathbf z_i^j\end{bmatrix}\right)\right]_b.
\tag{7}
$$

其中 $[\cdot]_b$ 提取边界分量，两次单元作用分别计算边界输入和内部修正的贡献，结果按式 (5) 累加到全局。

无需保存 $\mathbf K_{bb}^j,\mathbf K_{bi}^j,\mathbf K_{ib}^j$；$\mathbf K_{ii}^j$ 仍按当前 $s_e$ 逐子结构组装分解，因子的缓存与复用同第 2 节“内部求解”。共享的是单元基准刚度，内部矩阵及分解因子通常各块不同。

### 2.3 局部界面力与支承反力

取子结构为隔离体，边界行还包括相邻子结构的未知界面力 $\boldsymbol\lambda^j$ 与受约束行的支承反力 $\mathbf r_D^j$：

$$
\mathbf K_s^j\mathbf u_b^j
=\widetilde{\mathbf f}_b^j+\boldsymbol\lambda^j+\mathbf r_D^j,
\qquad
\boldsymbol\lambda^j
=\int_{\partial\Omega^j\cap\Gamma_{\mathrm{int}}}
(\mathbf N_b^j)^{\mathsf T}\mathbf t_{\mathrm{int}}^j\,\mathrm ds.
$$

$\mathbf N_b^j$ 为细网格边界形函数矩阵，$\Gamma_{\mathrm{int}}$ 为块间界面；$\widetilde{\mathbf f}_b^j$ 的一般形式见式 (14)，内部无载荷时等于 $\mathbf f_b^j$。外载包括体力与物理外边界面力，外边界单元面按唯一归属积分，同一载荷只计一次。协调组装后界面力成对抵消，支承反力保留在受约束行，由残量计算；自由行即第 3 节求解的方程。

## 3. 求解与位移恢复

传统有限元求解全场位移，子结构方法求解边界位移：

$$
\mathbf K\mathbf U=\mathbf F,
\qquad
\mathbf K_\Gamma\mathbf U_\Gamma=\mathbf F_\Gamma.
\tag{8}
$$

本文的整体平衡方程均在自由行上成立，受约束行施加给定位移。两种方法使用相同约束并假设解唯一。例如，令 $D,F$ 分别为受约束、自由分量集合，$(\mathbf U_\Gamma)_D=\mathbf d_D$，边界系统实际求解

$$
(\mathbf K_\Gamma)_{FF}(\mathbf U_\Gamma)_F
=(\mathbf F_\Gamma)_F-(\mathbf K_\Gamma)_{FD}\mathbf d_D.
\tag{9}
$$

### 3.1 显式求解

使用已组装的 $\mathbf K_\Gamma$，按式 (9) 提取自由子块并修正右端，通过直接法或迭代法求得边界位移。

### 3.2 隐式求解

不组装 $\mathbf K_\Gamma$，向迭代求解器提供式 (5) 的算子作用。将输入的受约束分量置零、取输出自由分量，即得到式 (9) 的自由子块作用；非零给定位移的右端修正也通过一次算子作用计算。

### 3.3 共同的位移恢复

两种方式求得 $\mathbf U_\Gamma$ 后，均逐块回代内部位移并恢复全场：

$$
\begin{aligned}
\mathbf u_b^j&=\mathbf A_b^j\mathbf U_\Gamma,
\qquad
\mathbf u_i^j=-(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j\mathbf u_b^j,\\
\mathbf U&=\mathbf R_\Gamma^{\mathsf T}\mathbf U_\Gamma
+\sum_j(\mathbf R_i^j)^{\mathsf T}\mathbf u_i^j.
\end{aligned}
\tag{10}
$$

$\mathbf R_\Gamma$、$\mathbf R_i^j$ 分别提取全场中的边界和第 $j$ 块内部自由度，转置将位移放回对应位置；共享边界位移只写入一次。

## 4. 代数等价

原细网格系统按全局边界 $\Gamma$ 和全部内部 $I$ 重排为

$$
\begin{bmatrix}
\mathbf K_{\Gamma\Gamma}&\mathbf K_{\Gamma I}\\
\mathbf K_{I\Gamma}&\mathbf K_{II}
\end{bmatrix}
\begin{bmatrix}\mathbf U_\Gamma\\\mathbf U_I\end{bmatrix}
=\begin{bmatrix}\mathbf F_\Gamma\\\mathbf0\end{bmatrix},
\qquad
\mathbf K_{II}=\operatorname{diag}_j(\mathbf K_{ii}^j).
\tag{11}
$$

不同子结构内部无直接耦合，因此 $\mathbf K_{II}$ 为块对角矩阵。消去 $\mathbf U_I$，得到

$$
\begin{aligned}
\mathbf K_{\Gamma\Gamma}-\mathbf K_{\Gamma I}\mathbf K_{II}^{-1}\mathbf K_{I\Gamma}
&=\sum_j(\mathbf A_b^j)^{\mathsf T}
\left[\mathbf K_{bb}^j-\mathbf K_{bi}^j(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j\right]\mathbf A_b^j\\
&=\mathbf K_\Gamma.
\end{aligned}
\tag{12}
$$

故全局消元与逐块缩聚后组装相同，且

$$
\mathbf K\mathbf U=\mathbf F
\quad\Longleftrightarrow\quad
\begin{cases}
\mathbf K_\Gamma\mathbf U_\Gamma=\mathbf F_\Gamma,\\
\mathbf U_I=-\mathbf K_{II}^{-1}\mathbf K_{I\Gamma}\mathbf U_\Gamma.
\end{cases}
\tag{13}
$$

在相同离散、材料、载荷与位移约束下，精确算术和精确求解时，显式与隐式路径得到同一个细网格解。共享参考单元 EA 满足式 (6) 时也保持该等价性；这些实现均不引入额外的近似误差，实际数值差异来自浮点运算及内部、全局求解误差。

**非零内部载荷。** 若 $\mathbf f_i^j\ne\mathbf0$，Schur 补不变，将式 (4) 中的局部载荷和式 (10) 中的内部恢复改为

$$
\widetilde{\mathbf f}_b^j
=\mathbf f_b^j-\mathbf K_{bi}^j(\mathbf K_{ii}^j)^{-1}\mathbf f_i^j,
\qquad
\mathbf u_i^j=(\mathbf K_{ii}^j)^{-1}
\left(\mathbf f_i^j-\mathbf K_{ib}^j\mathbf u_b^j\right).
\tag{14}
$$

### 4.1 形函数表示与非零内部载荷

为与子结构总览及 PIML 页的记号对应，定义

$$
\mathbf T_{\mathrm{full}}^j=-(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j,
\qquad
\mathbf w_i^j=(\mathbf K_{ii}^j)^{-1}\mathbf f_i^j,
\qquad
\mathbf N_{\mathrm{full}}^j=
\begin{bmatrix}\mathbf I\\\mathbf T_{\mathrm{full}}^j\end{bmatrix}.
$$

于是 $\mathbf u^j=[\mathbf0;\mathbf w_i^j]+\mathbf N_{\mathrm{full}}^j\mathbf u_b^j$。由内部平衡与刚度对称性直接得到

$$
\mathbf K_s^j=(\mathbf N_{\mathrm{full}}^j)^{\mathsf T}\mathbf K^j\mathbf N_{\mathrm{full}}^j,
\qquad
\widetilde{\mathbf f}_b^j=(\mathbf N_{\mathrm{full}}^j)^{\mathsf T}\mathbf f^j
=\mathbf f_b^j+(\mathbf T_{\mathrm{full}}^j)^{\mathsf T}\mathbf f_i^j,
\qquad
\mathbf f^j=\begin{bmatrix}\mathbf f_b^j\\\mathbf f_i^j\end{bmatrix}.
$$

非零内部载荷需要仿射恢复，不能仅写成形函数乘边界位移。进一步令 $\mathbf u_b^j=\boldsymbol\Psi^j\mathbf q^j$ 时，$\mathbf N_r^j=\mathbf N_{\mathrm{full}}^j\boldsymbol\Psi^j$，刚度与载荷按同一基投影，见 [[exact-substructural-lagrange#2. 静力缩聚与插值自由度上的方程|Lagrange §2]]。整体定位见 [[exact-substructural|子结构分析总览]]。

## 参考文献

- Gosselet, P., & Rey, C. (2006). Non-overlapping domain decomposition methods in structural mechanics. *Archives of Computational Methods in Engineering*, **13**, 515–572. [https://doi.org/10.1007/BF02905857](https://doi.org/10.1007/BF02905857)
