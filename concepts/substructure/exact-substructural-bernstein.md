---
title: "基于 Bernstein 边界位移插值的子结构分析"
type: concept
aliases:
  - Bernstein Boundary Displacement Interpolation
  - Bézier 边界位移子结构分析
tags:
  - finite-element
  - substructure
  - static-condensation
  - bernstein
status: draft
date_added: 2026-10-24
date_update: 2026-10-25
---

# 基于 Bernstein 边界位移插值的子结构分析

用 Bernstein 基函数表示子结构边界位移，在细边界节点处求值得到节点位移，通过局部静力平衡消去内部自由度，求解全局控制系数后恢复位移场。与 [[exact-substructural-full-trace|full-trace]] 相比，局部缩聚仍精确计算，但边界空间限制通常引入近似；文件名中的 `exact` 不表示与细网格解相同。这里沿用“插值”的称呼，控制系数一般不是对应位置的实际位移。

适用条件与 [[exact-substructural-lagrange|Lagrange 页]] 相同：小应变线弹性静力、沿细网格单元边界非重叠划分的规则矩形／长方体子结构、匹配接口网格、统一次数 $p\ge1$。内部载荷默认置零，位移约束位于子结构边界，固定边界后的内部矩阵可逆。边界包括内部接口和物理外边界，其位移不全是预先给定的量。

以本页为精确基准、预测内部形函数并通过能量投影构造刚度的流程见 [[../piml/piml-substructural-bernstein|Bernstein PIML 子结构分析]]。

## 1. 矩阵组装与边界位移表示

### 1.1 局部矩阵与自由度分块

沿用边界 $b$、内部 $i$ 分块，记本块控制系数为 $\mathbf c^j$：

$$
\mathbf K^j=\sum_{e\subset\Omega^j}(\mathbf G_e^j)^{\mathsf T}\mathbf K_e\mathbf G_e^j
=\begin{bmatrix}\mathbf K_{bb}^j&\mathbf K_{bi}^j\\\mathbf K_{ib}^j&\mathbf K_{ii}^j\end{bmatrix},
\qquad \mathbf u_b^j=\mathbf S_{B,p}^j\mathbf c^j.
\tag{1}
$$

$\mathbf G_e^j$ 提取单元位移，$\mathbf c^j\in\mathbb R^{d n_r}$ 包含 $n_r$ 个唯一控制点的位移系数，$\mathbf S_{B,p}^j\in\mathbb R^{d n_b\times d n_r}$ 在 $n_b$ 个细边界节点处评价基函数，$d=2,3$。控制系数是广义位移自由度；除端点等特殊位置外，不等于辅助位移多项式在控制点参数位置的值。

### 1.2 任意次数的一维基函数

在 $[0,1]$ 上定义

$$
B_a^p(t)=\binom pa t^a(1-t)^{p-a},\quad a=0,\ldots,p,
\qquad
B_a^p(t)\ge0,\quad \sum_{a=0}^pB_a^p(t)=1,\quad
\sum_{a=0}^p\frac ap B_a^p(t)=t.
\tag{2}
$$

端点满足 $B_a^p(0)=\delta_{a0}$、$B_a^p(1)=\delta_{ap}$，故端点位移等于端点系数；内部一般没有节点插值性。辅助边界场 $\widehat{\mathbf u}(t)=\sum_a B_a^p(t)\mathbf c_a$ 通常满足 $\widehat{\mathbf u}(a/p)\ne\mathbf c_a$。式 (2) 保证常数和一次场可再现，包括仿射参数化下的小变形刚体运动。

### 1.3 二维子结构：逐边表示

每条边仿射参数化到 $[0,1]$，在细节点 $\mathbf x_m$ 处求值：

$$
\mathbf u_b(\mathbf x_m)=\sum_{a=0}^p B_a^p(t(\mathbf x_m))\mathbf c_a.
\tag{3}
$$

系数乘以 $\mathbf I_d$ 并放入相应控制点列，即得 $\mathbf S_{B,p}^j$ 的行块。角点共享，四边形有 $4p$ 个唯一控制点。边方向反转时按 $B_a^p(1-t)=B_{p-a}^p(t)$ 反转控制点编号。

### 1.4 三维子结构：逐面张量积表示

在每个面取仿射参数 $(s,t)\in[0,1]^2$，采用 $Q_p$ 表示：

$$
\mathbf u_b(\mathbf x_m)=\sum_{a=0}^p\sum_{b=0}^p
B_a^p(s(\mathbf x_m))B_b^p(t(\mathbf x_m))\mathbf c_{ab},
\qquad n_r=8+12(p-1)+6(p-1)^2.
\tag{4}
$$

相邻面、相邻子结构在公共棱和面上共享同一组控制系数，按参数反转或交换转换编号，保证公共位移一致。顶点、棱内部、面内部控制点分别合并；每个细边界节点行只写一次，不能将相邻面的相同位移重复相加。

式 (3)、(4) 约束细节点值；节点之间仍使用原细网格有限元形函数，因此最终细网格迹一般不等于辅助高次多项式在所有位置的值。这与 Lagrange 页的采样约定一致。

### 1.5 一次、二次与三次

一维基函数向量为

$$
\begin{aligned}
\mathbf B^1(t)&=(1-t,\ t),\\
\mathbf B^2(t)&=((1-t)^2,\ 2t(1-t),\ t^2),\\
\mathbf B^3(t)&=((1-t)^3,\ 3t(1-t)^2,\ 3t^2(1-t),\ t^3).
\end{aligned}
\tag{5}
$$

| 次数 | 二维：边上的表示 | 三维：面上的表示 | 四边形控制点数 | 六面体控制点数 |
|---|---|---|---:|---:|
| $p=1$ | 线性 | 双线性 $Q_1$ | 4 | 8 |
| $p=2$ | 二次 | 双二次 $Q_2$ | 8 | 26 |
| $p=3$ | 三次 | 双三次 $Q_3$ | 12 | 56 |

一次基与端点 Lagrange 基相同，即角点方案。三次 Bernstein 曲线及其双三次张量积对应 Guo2026 的 cubic Bézier 边界表示；这里不将该文表中未明确基底的二次方案认定为 Bernstein。

## 2. 静力缩聚与控制系数上的方程

内部无载荷时，局部平衡给出

$$
\mathbf u_i^j=-(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j\mathbf S_{B,p}^j\mathbf c^j,
\qquad
\mathbf K_s^j=\mathbf K_{bb}^j-\mathbf K_{bi}^j(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j.
\tag{6}
$$

逆矩阵均通过线性系统求解实现。将边界表示代入缩聚势能 $\frac12(\mathbf u_b^j)^{\mathsf T}\mathbf K_s^j\mathbf u_b^j-(\mathbf u_b^j)^{\mathsf T}\mathbf f_b^j$，对 $\mathbf c^j$ 取变分，得到

$$
\mathbf K_{B,p}^j=(\mathbf S_{B,p}^j)^{\mathsf T}\mathbf K_s^j\mathbf S_{B,p}^j,
\qquad \mathbf f_{B,p}^j=(\mathbf S_{B,p}^j)^{\mathsf T}\mathbf f_b^j.
\tag{7}
$$

载荷投影保持虚功，不能抽取或直接分配为控制点处的节点力。边界残量仅对允许的虚位移正交，不要求每个自由细边界节点分别平衡。

### 2.1 显式构造与全局组装

令 $\boldsymbol\eta$ 为全局唯一控制系数，$\mathbf c^j=\mathbf A_B^j\boldsymbol\eta$，则

$$
\mathbf K_{B,p}=\sum_j(\mathbf A_B^j)^{\mathsf T}\mathbf K_{B,p}^j\mathbf A_B^j,
\qquad \mathbf F_{B,p}=\sum_j(\mathbf A_B^j)^{\mathsf T}\mathbf f_{B,p}^j.
\tag{8}
$$

每项外载荷只分配一次。可先形成 Schur 补再投影，也可求解 $\mathbf K_{ii}^j\mathbf Z^j=\mathbf K_{ib}^j\mathbf S_{B,p}^j$，直接形成 $(\mathbf S_{B,p}^j)^{\mathsf T}(\mathbf K_{bb}^j\mathbf S_{B,p}^j-\mathbf K_{bi}^j\mathbf Z^j)$。

### 2.2 隐式算子作用

给定全局输入 $\mathbf v$，逐块计算

$$
\begin{aligned}
\mathbf v_b^j&=\mathbf S_{B,p}^j\mathbf A_B^j\mathbf v,
&\mathbf K_{ii}^j\mathbf z_i^j&=\mathbf K_{ib}^j\mathbf v_b^j,\\
\mathbf y_b^j&=\mathbf K_{bb}^j\mathbf v_b^j-\mathbf K_{bi}^j\mathbf z_i^j,
&\mathbf K_{B,p}\mathbf v&=\sum_j(\mathbf A_B^j)^{\mathsf T}(\mathbf S_{B,p}^j)^{\mathsf T}\mathbf y_b^j.
\end{aligned}
\tag{9}
$$

即“边界求值 → Schur 作用 → 转置投影 → 全局累加”。无需形成降阶矩阵，精确算术下与式 (8) 相同。

### 2.3 结合单元层 Matrix-Free

满足共享参考单元条件 $\mathbf K_e=s_e\mathbf K_0$ 时，定义 $\mathcal K^j(\mathbf x)=\sum_e(\mathbf G_e^j)^{\mathsf T}s_e\mathbf K_0\mathbf G_e^j\mathbf x$，以

$$
\begin{bmatrix}\mathbf a_b^j\\\mathbf a_i^j\end{bmatrix}
=\mathcal K^j\left(\begin{bmatrix}\mathbf v_b^j\\\mathbf0\end{bmatrix}\right),
\quad \mathbf K_{ii}^j\mathbf z_i^j=\mathbf a_i^j,
\quad \mathbf y_b^j=\mathbf a_b^j-
\left[\mathcal K^j\left(\begin{bmatrix}\mathbf0\\\mathbf z_i^j\end{bmatrix}\right)\right]_b
\tag{10}
$$

替代式 (9) 的局部块乘法。共享参考单元 EA 的条件见 [[exact-substructural-full-trace#2.2.1 结合单元层 Matrix-Free|full-trace §2.2.1]]；内部矩阵仍可组装分解并在系数不变时复用，改变边界基底或次数不改变该内部矩阵。

## 3. 求解与位移恢复

### 3.1 位移约束与全局求解

若约束可直接指定控制系数 $\boldsymbol\eta_D=\mathbf d_D$，则求解

$$
(\mathbf K_{B,p})_{FF}\boldsymbol\eta_F
=(\mathbf F_{B,p})_F-(\mathbf K_{B,p})_{FD}\mathbf d_D.
\tag{11}
$$

整面零位移可由该面全部控制系数置零施加；给定非零辅助边界多项式时，须使用其 Bernstein 系数，不能将该函数在 $a/p$ 等位置的值直接赋给控制系数。对于细节点给定位移，一般形成线性组合约束 $\mathbf D\boldsymbol\eta=\mathbf d$；要求约束可由所选空间表示，否则需扩充空间或明确近似边界数据。

取 $\mathbf D\boldsymbol\eta_0=\mathbf d$，以 $\mathbf Z$ 的列构成 $\ker\mathbf D$ 的基，令 $\boldsymbol\eta=\boldsymbol\eta_0+\mathbf Z\mathbf a$，求解

$$
\mathbf Z^{\mathsf T}\mathbf K_{B,p}\mathbf Z\mathbf a
=\mathbf Z^{\mathsf T}(\mathbf F_{B,p}-\mathbf K_{B,p}\boldsymbol\eta_0).
\tag{12}
$$

显式实现使用组装矩阵，隐式实现提供式 (9) 的作用。消去约束后假设系统正定，排除未约束刚体运动及冗余系数。

### 3.2 边界与内部位移恢复

求得 $\boldsymbol\eta$ 后逐块恢复

$$
\mathbf u_b^j=\mathbf S_{B,p}^j\mathbf A_B^j\boldsymbol\eta,
\qquad \mathbf u_i^j=-(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j\mathbf u_b^j.
\tag{13}
$$

共享边界位移只写入一次，再放回内部位移。内部节点值由材料分布与平衡方程决定，一般不是 $p$ 次 Bernstein 多项式场。

## 4. 与 Lagrange、full-trace 的关系

### 4.1 同阶基底变换

在同一边上选取 $p+1$ 个互异 Lagrange 节点 $t_i$，包含端点。以 $T_{ia}=B_a^p(t_i)$ 定义标量求值矩阵，得到

$$
\mathbf q=\mathbf T\mathbf c,
\qquad B_a^p(t)=\sum_{i=0}^p\ell_i^{(p)}(t)T_{ia},
\qquad \mathbf S_{B,p}=\mathbf S_{L,p}\mathbf T.
\tag{14}
$$

式 (14) 先对一个位移分量成立；多分量使用 $\mathbf T\otimes\mathbf I_d$。$\mathbf T$ 可逆，因为次数不超过 $p$ 的多项式由 $p+1$ 个互异节点值唯一确定。面上使用两个方向的张量积变换，编号随向量排列一致调整。

将公共实体只计一次并统一方向，可得到局部变换 $\mathbf T^j$ 与全局可逆变换 $\mathcal T$，满足 $\mathbf A_L^j\mathcal T=\mathbf T^j\mathbf A_B^j$。这里 $\mathbf A_L^j$ 即 Lagrange 页的 $\mathbf A_r^j$，$\mathbf S_{L,p}^j$ 即该页的 $\mathbf S_p^j$。

### 4.2 二次实例：节点值与控制系数

对一个位移分量，取 $t_i=0,\frac12,1$，有

$$
\begin{bmatrix}q_0\\q_1\\q_2\end{bmatrix}
=\begin{bmatrix}1&0&0\\\frac14&\frac12&\frac14\\0&0&1\end{bmatrix}
\begin{bmatrix}c_0\\c_1\\c_2\end{bmatrix},
\qquad c_1=2q_1-\frac12(q_0+q_2).
\tag{15}
$$

例如节点值 $(0,1,0)$ 对应控制系数 $(0,2,0)$，两者均表示 $4t(1-t)$。若把 $(0,1,0)$ 直接作为 Bernstein 系数，则得到 $2t(1-t)$，已经改变了位移函数。

### 4.3 刚度、载荷与解的对应

将局部换基关系代入式 (7)，并按一致编号组装，得到

$$
\begin{aligned}
\mathbf K_{B,p}^j&=(\mathbf T^j)^{\mathsf T}\mathbf K_{L,p}^j\mathbf T^j,
&\mathbf f_{B,p}^j&=(\mathbf T^j)^{\mathsf T}\mathbf f_{L,p}^j,\\
\mathbf Q&=\mathcal T\boldsymbol\eta,
&\mathbf K_{B,p}&=\mathcal T^{\mathsf T}\mathbf K_{L,p}\mathcal T,
\qquad \mathbf F_{B,p}=\mathcal T^{\mathsf T}\mathbf F_{L,p}.
\end{aligned}
\tag{16}
$$

此处 $\mathbf K_{L,p}$、$\mathbf F_{L,p}$ 即 Lagrange 页的 $\mathbf K_{r,p}$、$\mathbf F_{r,p}$。若 Lagrange 约束为 $\mathbf C\mathbf Q=\mathbf d$，相同物理约束在 Bernstein 坐标中为 $\mathbf C\mathcal T\boldsymbol\eta=\mathbf d$，而非机械照搬相同系数值。

在相同次数、参数化、细节点采样、协调空间及等价约束下，两种表示给出相同的精确边界位移、内部位移、能量和柔度。矩阵条目与条件数可以不同，浮点误差、迭代误差或 ML 代理误差也可能不同；这不证明某一种基底普遍更准确或更稳定。

### 4.4 次数提升与 full-trace

由二项式恒等式得 $B_a^p=\frac{p+1-a}{p+1}B_a^{p+1}+\frac{a+1}{p+1}B_{a+1}^{p+1}$。同一函数的升次系数为

$$
\mathbf c'_0=\mathbf c_0,\quad \mathbf c'_{p+1}=\mathbf c_p,
\qquad
\mathbf c'_a=\frac{a}{p+1}\mathbf c_{a-1}
+\left(1-\frac{a}{p+1}\right)\mathbf c_a,\quad a=1,\ldots,p.
\tag{17}
$$

面上分别沿两个方向升次，公共实体采用相同变换。固定划分、仿射参数化、细网格采样和物理约束时，允许的边界空间满足 $\mathcal V_p\subseteq\mathcal V_{p+1}$；单纯升次表示同一场，而求解扩大后的空间允许出现新的位移模式。

在相同载荷、零内部载荷及齐次位移约束下，记 full-trace 解为 $\mathbf U_\Gamma$，降阶解为 $\mathbf U_{\Gamma,p}$，均在自由边界分量上讨论，则由 [[exact-substructural-lagrange#4.2 Ritz 最佳逼近与柔度|Ritz 投影关系]] 得

$$
\|\mathbf U_\Gamma-\mathbf U_{\Gamma,p}\|_{\mathbf K_\Gamma}
=\min_{\mathbf V\in\mathcal V_p}\|\mathbf U_\Gamma-\mathbf V\|_{\mathbf K_\Gamma},
\qquad C-C_p=\|\mathbf U_\Gamma-\mathbf U_{\Gamma,p}\|_{\mathbf K_\Gamma}^2\ge0,
\qquad C_p\le C_{p+1}\le C.
\tag{18}
$$

其中 $C=\mathbf F_\Gamma^{\mathsf T}\mathbf U_\Gamma$、$C_p=\mathbf F_\Gamma^{\mathsf T}\mathbf U_{\Gamma,p}$。非零给定位移需先作提升，不能直接套用此柔度差公式。同阶换基不改变 $\mathcal V_p$，因此不改变边界最佳逼近误差。

采样矩阵须列满秩，避免非零控制系数产生零细节点位移。若各方向有 $m$ 个细单元和 $m+1$ 个细节点，完整张量网格上 $p\le m$ 保持列满秩；$p=m$ 时可覆盖完整细边界空间，Bernstein 求值矩阵为方阵且可逆，通常不是单位矩阵。将相同约束和载荷一并变换后仍与 full-trace 代数等价。一般情形应检查空间覆盖与秩，而非仅凭次数判断。

**非零内部载荷。** 若 $\mathbf f_i^j\ne\mathbf0$，刚度不变，将式 (7) 的载荷及式 (13) 的内部恢复改为

$$
\widetilde{\mathbf f}_{B,p}^j=(\mathbf S_{B,p}^j)^{\mathsf T}
\left[\mathbf f_b^j-\mathbf K_{bi}^j(\mathbf K_{ii}^j)^{-1}\mathbf f_i^j\right],
\qquad \mathbf u_i^j=(\mathbf K_{ii}^j)^{-1}(\mathbf f_i^j-\mathbf K_{ib}^j\mathbf u_b^j).
\tag{19}
$$

## 参考依据

- [[exact-substructural-full-trace|保留全部边界节点位移的精确子结构分析]]：局部分块、Schur 补、Matrix-Free 作用及内部载荷修正的推导起点。
- [[exact-substructural-lagrange|基于 Lagrange 边界位移插值的子结构分析]]：节点采样、协调空间、约束、Ritz 近似及满秩条件的统一框架。
- [[../../literature/topopt/piml/translations/Guo2026-highgeneralization-bezier-zh|Guo et al. (2026)]]，原始 PDF §2.3 式 (9)–(18)：三次 Bernstein 曲线与双三次 Bézier 边界表示。本页任意次数推广、二次换基实例、全局坐标变换及次数提升为数学推导，不作为该文二次算例实现的证据。
