---
title: "基于 Bernstein 边界位移插值的 PIML 子结构分析"
type: concept
aliases:
  - PIML Bernstein Substructural Analysis
  - Bézier 边界位移 PIML 子结构分析
tags:
  - PIML
  - substructure
  - static-condensation
  - bernstein
status: draft
date_added: 2026-10-25
date_update: 2026-10-25
---

# 基于 Bernstein 边界位移插值的 PIML 子结构分析

沿用 [[../substructure/exact-substructural-bernstein|精确 Bernstein 子结构分析]] 的边界表示与求解框架，以 PIML 预测形函数的内部恢复矩阵，再由当前材料刚度作能量投影。仅讨论形函数预测；控制系数一般不是控制点参数位置的实际位移。共同训练与力学约束见 [[piml-substructural|PIML 总览]]，本文为该框架在 Bernstein 坐标下的推导。

假设同精确页：小应变线弹性静力、非重叠规则矩形／长方体子结构、匹配接口网格与协调边界表示、统一次数 $p\ge1$、内部无载荷、位移约束位于子结构边界，且 $\mathbf K^j\succeq0,\mathbf K_{ii}^j\succ0$。

沿用精确页的 $\mathbf S_{B,p}^j,\mathbf c^j,\mathbf A_B^j,\boldsymbol\eta,\mathbf K_{B,p}^j,\mathbf D,\mathbf T^j,\mathcal T$；预测算子及其解加帽号。**$\boldsymbol\eta$ 是全局控制系数**，本页材料输入另记为 $\boldsymbol\mu^j$（对应总览的材料参数 $\boldsymbol\eta^j$）。新增 $\mathbf T_{B,p}^j$ 表示内部恢复矩阵，与换基矩阵 $\mathbf T^j$ 区分。

| 计算环节 | 精确 Bernstein | PIML 替代 |
|---|---|---|
| 边界表示 | 固定 $\mathbf S_{B,p}^j$ | 相同 |
| 局部刚度构造 | 内部求解后缩聚、投影 | 预测内部映射，再作能量投影 |
| 全局求解 | 求解控制系数 | 保留组装与约束形式，使用预测刚度 |
| 内部恢复 | 局部回代 | 用构造刚度的同一预测映射恢复 |

## 1. 矩阵组装与边界位移表示

### 1.1 局部矩阵与自由度分块

$$
\mathbf K^j(\boldsymbol\mu^j)=\sum_{e\subset\Omega^j}(\mathbf G_e^j)^{\mathsf T}\mathbf K_e\mathbf G_e^j
=\begin{bmatrix}\mathbf K_{bb}^j&\mathbf K_{bi}^j\\\mathbf K_{ib}^j&\mathbf K_{ii}^j\end{bmatrix},
\qquad \mathbf u_b^j=\mathbf S_{B,p}^j\mathbf c^j.
\tag{1}
$$

沿用精确页的节点计数：$n_b$ 为细边界节点数，$n_r$ 为唯一控制点数，$\mathbf c^j\in\mathbb R^{d n_r}$、$\mathbf S_{B,p}^j\in\mathbb R^{d n_b\times d n_r}$，$d=2,3$。PIML 保留当前材料场的 $\mathbf K^j$ 作用及固定边界块，不预测边界控制系数；控制系数由全局方程求得。

### 1.2 任意次数的一维基函数

$$
B_a^p(t)=\binom pa t^a(1-t)^{p-a},\quad a=0,\ldots,p,
\qquad \sum_aB_a^p(t)=1,\quad \sum_a\frac ap B_a^p(t)=t.
\tag{2}
$$

端点位移等于端点系数，但一般有 $\sum_aB_a^p(k/p)\mathbf c_a\ne\mathbf c_k$。常数和一次场再现性保证仿射参数化下的边界刚体运动可表示；性质与节点采样约定见 [[../substructure/exact-substructural-bernstein#1.2 任意次数的一维基函数|精确页 §1.2]]。

### 1.3 二维子结构：逐边表示

$$
\mathbf u_b(\mathbf x_m)=\sum_{a=0}^p B_a^p(t(\mathbf x_m))\mathbf c_a.
\tag{3}
$$

求值系数乘 $\mathbf I_d$ 后组成 $\mathbf S_{B,p}^j$ 的行块。四边形有 $4p$ 个唯一控制点，角点只编号一次；边方向反转时相应反转系数顺序。

### 1.4 三维子结构：逐面张量积表示

$$
\mathbf u_b(\mathbf x_m)=\sum_{a=0}^p\sum_{b=0}^p
B_a^p(s(\mathbf x_m))B_b^p(t(\mathbf x_m))\mathbf c_{ab},
\qquad n_r=8+12(p-1)+6(p-1)^2.
\tag{4}
$$

公共实体共享控制系数，并按参数反转或交换统一编号；共享细边界节点位移只写一次。约束作用于细节点值，节点之间仍按原细网格有限元形函数表示，不将辅助高次多项式视为最终细网格迹。

### 1.5 一次、二次与三次

| 次数 | 二维边表示 | 三维面表示 | 四边形控制点数 | 六面体控制点数 |
|---|---|---|---:|---:|
| $p=1$ | 线性 | 双线性 $Q_1$ | 4 | 8 |
| $p=2$ | 二次 | 双二次 $Q_2$ | 8 | 26 |
| $p=3$ | 三次 | 双三次 $Q_3$ | 12 | 56 |

基函数显式表达见 [[../substructure/exact-substructural-bernstein#1.5 一次、二次与三次|精确页 §1.5]]。$p=1$ 与角点 Lagrange 表示相同，$p=3$ 为三次 Bézier 边界表示；本页不将一般次数推导等同于某篇论文的具体网络实现。

## 2. 局部缩聚的 PIML 替代与控制系数上的方程

精确内部映射及降阶刚度为

$$
\mathbf T_{B,p}^j=-(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j\mathbf S_{B,p}^j
=\mathbf T_{\mathrm{full}}^j\mathbf S_{B,p}^j,
\qquad \mathbf K_{B,p}^j=(\mathbf S_{B,p}^j)^{\mathsf T}\mathbf K_s^j\mathbf S_{B,p}^j.
\tag{5}
$$

$\mathbf K_s^j$ 为精确 full-trace Schur 补。监督训练离线求解式 (5) 生成内部映射标签；在线用 $\widehat{\mathbf T}_{B,p}^j=\mathcal F_{B,p}(\boldsymbol\mu^j;\boldsymbol\theta)$ 替代该求解。输出行数为内部位移自由度数，列数为 $d n_r$；$\mathcal F_{B,p}$ 包含预测与约束补全，同一次线性求解中预测映射固定。

样本和训练目标见 [[piml-substructural#3.2 材料样本与训练目标|总览 §3.2]]、[[piml-substructural#3.2 材料样本与训练目标|总览 §3.2]]，模型复用要求几何、离散、编号和材料参数域相容。刚体约束须作用于 Bernstein 系数：记 $\mathbf R_{B,p}^j$ 为刚体场的控制系数、$\mathbf R_b^j,\mathbf R_i^j$ 为细边界及内部刚体位移模态，要求 $\mathbf S_{B,p}^j\mathbf R_{B,p}^j=\mathbf R_b^j$、$\widehat{\mathbf T}_{B,p}^j\mathbf R_{B,p}^j=\mathbf R_i^j$。这里的 $\mathbf R$ 均指刚体模态，沿用 [[piml-substructural#3.1 网络输出与力学约束|总览 §3.1]] 的含义。

### 2.1 显式构造与全局组装

$$
\begin{aligned}
\widehat{\mathbf N}_{B,p}^j&=\begin{bmatrix}\mathbf S_{B,p}^j\\\widehat{\mathbf T}_{B,p}^j\end{bmatrix},\\
\widehat{\mathbf K}_{B,p}^j&=(\widehat{\mathbf N}_{B,p}^j)^{\mathsf T}\mathbf K^j\widehat{\mathbf N}_{B,p}^j\\
&=(\mathbf S_{B,p}^j)^{\mathsf T}\mathbf K_{bb}^j\mathbf S_{B,p}^j
+(\mathbf S_{B,p}^j)^{\mathsf T}\mathbf K_{bi}^j\widehat{\mathbf T}_{B,p}^j\\
&\quad+(\widehat{\mathbf T}_{B,p}^j)^{\mathsf T}\mathbf K_{ib}^j\mathbf S_{B,p}^j
+(\widehat{\mathbf T}_{B,p}^j)^{\mathsf T}\mathbf K_{ii}^j\widehat{\mathbf T}_{B,p}^j.
\end{aligned}
\tag{6}
$$

预测内部场一般不满足精确平衡，四项不能按精确 Schur 补简化。当前材料刚度的能量投影保证对称半正定，刚体零空间仍需刚体再现及离散无额外零能模式。

取 $\widehat{\mathbf c}^j=\mathbf A_B^j\widehat{\boldsymbol\eta}$，组装

$$
\widehat{\mathbf K}_{B,p}=\sum_j(\mathbf A_B^j)^{\mathsf T}\widehat{\mathbf K}_{B,p}^j\mathbf A_B^j,
\qquad \mathbf f_{B,p}^j=(\mathbf S_{B,p}^j)^{\mathsf T}\mathbf f_b^j,
\qquad \mathbf F_{B,p}=\sum_j(\mathbf A_B^j)^{\mathsf T}\mathbf f_{B,p}^j.
\tag{7}
$$

载荷通过同一边界映射投影，保持虚功；不能把细节点力直接当作控制点力。外载只分配一次，内部无载荷时右端与精确系统相同。

### 2.2 隐式算子作用

对全局输入 $\mathbf v$，逐块计算

$$
\begin{aligned}
\mathbf v_c^j&=\mathbf A_B^j\mathbf v,\\
\begin{bmatrix}\mathbf a_b^j\\\mathbf a_i^j\end{bmatrix}
&=\mathbf K^j\begin{bmatrix}\mathbf S_{B,p}^j\mathbf v_c^j\\\widehat{\mathbf T}_{B,p}^j\mathbf v_c^j\end{bmatrix},\\
\mathbf y_c^j&=(\mathbf S_{B,p}^j)^{\mathsf T}\mathbf a_b^j
+(\widehat{\mathbf T}_{B,p}^j)^{\mathsf T}\mathbf a_i^j,\qquad
\widehat{\mathbf K}_{B,p}\mathbf v=\sum_j(\mathbf A_B^j)^{\mathsf T}\mathbf y_c^j.
\end{aligned}
\tag{8}
$$

内部线性求解被预测矩阵乘法替代。$\mathbf a_i^j$ 一般非零，内部转置投影项不能省去。固定同一预测映射时，式 (8) 与显式矩阵作用代数等价，可不形成局部及全局降阶矩阵。

### 2.3 结合单元层 Matrix-Free

满足 [[../substructure/exact-substructural-full-trace#2.2.1 结合单元层 Matrix-Free|共享参考单元条件]] $\mathbf K_e=s_e\mathbf K_0$ 时，以

$$
\mathcal K^j(\mathbf x)=\sum_{e\subset\Omega^j}(\mathbf G_e^j)^{\mathsf T}s_e\mathbf K_0\mathbf G_e^j\mathbf x,
\qquad
\begin{bmatrix}\mathbf a_b^j\\\mathbf a_i^j\end{bmatrix}
=\mathcal K^j\left(\begin{bmatrix}\mathbf S_{B,p}^j\mathbf v_c^j\\\widehat{\mathbf T}_{B,p}^j\mathbf v_c^j\end{bmatrix}\right)
\tag{9}
$$

替代式 (8) 的局部矩阵作用。每次需一次细网格刚度作用及预测映射的正、转置乘法，不需在线分解 $\mathbf K_{ii}^j$。也可逐列作用于 $\widehat{\mathbf N}_{B,p}^j$，预先保存局部刚度而不组装全局矩阵；两种存储选择同 [[piml-substructural-lagrange#2.3 结合单元层 Matrix-Free|Lagrange PIML §2.3]]。

## 3. 求解与位移恢复

### 3.1 位移约束与全局求解

预测系统为 $\widehat{\mathbf K}_{B,p}\widehat{\boldsymbol\eta}=\mathbf F_{B,p}$，仅在自由变分方向上要求平衡。可直接指定控制系数时，$\widehat{\boldsymbol\eta}_D=\mathbf d_D$，求解

$$
(\widehat{\mathbf K}_{B,p})_{FF}\widehat{\boldsymbol\eta}_F
=(\mathbf F_{B,p})_F-(\widehat{\mathbf K}_{B,p})_{FD}\mathbf d_D.
\tag{10}
$$

整面固定可将该面全部系数置零；非零辅助位移多项式须转换为 Bernstein 系数，不能直接赋予其在控制点参数位置的函数值。细节点约束一般形成 $\mathbf D\widehat{\boldsymbol\eta}=\mathbf d$，须检查相容性并去除冗余约束。

取 $\mathbf D\boldsymbol\eta_0=\mathbf d$、$\operatorname{range}(\mathbf Z)=\ker\mathbf D$，令 $\widehat{\boldsymbol\eta}=\boldsymbol\eta_0+\mathbf Z\widehat{\mathbf a}$，求解

$$
\mathbf Z^{\mathsf T}\widehat{\mathbf K}_{B,p}\mathbf Z\widehat{\mathbf a}
=\mathbf Z^{\mathsf T}(\mathbf F_{B,p}-\widehat{\mathbf K}_{B,p}\boldsymbol\eta_0).
\tag{11}
$$

显式实现使用组装矩阵，隐式实现提供式 (8) 的作用；消去约束后正定时可用 CG。约束不相容时须扩充空间或明确近似边界数据，预测内部映射不能修正边界空间不足。

### 3.2 边界与内部位移恢复

使用构造刚度的同一预测映射逐块恢复：

$$
\widehat{\mathbf u}_b^j=\mathbf S_{B,p}^j\mathbf A_B^j\widehat{\boldsymbol\eta},
\qquad \widehat{\mathbf u}_i^j=\widehat{\mathbf T}_{B,p}^j\mathbf A_B^j\widehat{\boldsymbol\eta}.
\tag{12}
$$

共享边界只写一次，放回各块内部得到全场 $\widehat{\mathbf U}_{B,p}$。内部位移不必是 $p$ 次 Bernstein 多项式。记 $\mathbf E_{B,p}^j=\widehat{\mathbf T}_{B,p}^j-\mathbf T_{B,p}^j$，内部残量为

$$
\mathbf r_i^j=\mathbf K_{ib}^j\widehat{\mathbf u}_b^j+\mathbf K_{ii}^j\widehat{\mathbf u}_i^j
=\mathbf K_{ii}^j\mathbf E_{B,p}^j\widehat{\mathbf c}^j.
\tag{13}
$$

代理系统收敛不代表原细网格内部平衡；边界平衡也只在允许的虚位移方向成立。

## 4. 与 Lagrange、full-trace 的关系

### 4.1 同阶基底变换

沿用精确页的 $T_{ia}=B_a^p(t_i)$，多分量与面张量积变换按同一编号扩展，有

$$
\mathbf q^j=\mathbf T^j\mathbf c^j,
\qquad \mathbf S_{B,p}^j=\mathbf S_{L,p}^j\mathbf T^j,
\qquad \mathbf A_L^j\mathcal T=\mathbf T^j\mathbf A_B^j.
\tag{14}
$$

$\mathbf S_{L,p}^j,\mathbf A_L^j$ 即 Lagrange 页的 $\mathbf S_p^j,\mathbf A_r^j$。要保持同一预测全场空间，内部映射也须满足

$$
\widehat{\mathbf T}_{B,p}^j=\widehat{\mathbf T}_{L,p}^j\mathbf T^j,
\qquad \widehat{\mathbf N}_{B,p}^j=\widehat{\mathbf N}_{L,p}^j\mathbf T^j.
\tag{15}
$$

这里 $\widehat{\mathbf T}_{L,p}^j$ 即 [[piml-substructural-lagrange#4.4 基底选择与空间选择|Lagrange PIML 页]] 的 $\widehat{\mathbf T}_p^j$。两种基底各自独立训练时，不自动满足式 (15)。

### 4.2 二次实例：节点值与控制系数

取单分量 Lagrange 节点 $0,\frac12,1$：

$$
\begin{bmatrix}q_0\\q_1\\q_2\end{bmatrix}
=\begin{bmatrix}1&0&0\\\frac14&\frac12&\frac14\\0&0&1\end{bmatrix}
\begin{bmatrix}c_0\\c_1\\c_2\end{bmatrix},
\qquad c_1=2q_1-\tfrac12(q_0+q_2).
\tag{16}
$$

节点值 $(0,1,0)$ 对应系数 $(0,2,0)$，表示 $4t(1-t)$；将 $(0,1,0)$ 直接作为系数会得到 $2t(1-t)$。PIML 预测不改变这一边界坐标关系，训练标签、刚体模态及给定位移都必须采用相应坐标。

### 4.3 刚度、载荷与解的对应

式 (15) 成立、使用同一材料刚度且公共实体编号一致时，能量投影给出

$$
\begin{aligned}
\widehat{\mathbf K}_{B,p}^j&=(\mathbf T^j)^{\mathsf T}\widehat{\mathbf K}_{L,p}^j\mathbf T^j,
&\mathbf f_{B,p}^j&=(\mathbf T^j)^{\mathsf T}\mathbf f_{L,p}^j,\\
\widehat{\mathbf K}_{B,p}&=\mathcal T^{\mathsf T}\widehat{\mathbf K}_{L,p}\mathcal T,
&\mathbf F_{B,p}&=\mathcal T^{\mathsf T}\mathbf F_{L,p},\qquad
\widehat{\mathbf Q}=\mathcal T\widehat{\boldsymbol\eta}.
\end{aligned}
\tag{17}
$$

$\mathbf K_{L,p},\mathbf F_{L,p}$ 对应 Lagrange 页的 $\mathbf K_{r,p},\mathbf F_{r,p}$。相同物理约束应从 $\mathbf C\widehat{\mathbf Q}=\mathbf d$ 转换为 $\mathbf D\widehat{\boldsymbol\eta}=\mathbf d$，其中 $\mathbf D=\mathbf C\mathcal T$。由此两种坐标给出相同预测全场、能量和柔度；独立训练则可能给出不同结果，不能据同阶基底等价断言代理误差相同。

### 4.4 次数提升与 full-trace

同一边界函数的升次系数仍为

$$
\mathbf c'_0=\mathbf c_0,\quad\mathbf c'_{p+1}=\mathbf c_p,\qquad
\mathbf c'_a=\frac{a}{p+1}\mathbf c_{a-1}+\left(1-\frac{a}{p+1}\right)\mathbf c_a,
\quad a=1,\ldots,p.
\tag{18}
$$

面上逐方向升次，公共实体同步转换。固定精确页的划分、仿射参数化、采样与物理约束时，边界空间嵌套；独立训练的内部映射却不保证预测全场空间嵌套，故提高次数不保证代理总误差下降。

若采用同一个固定的 [[piml-substructural-full-trace|full-trace 预测映射]]，令 $\widehat{\mathbf T}_{B,p}^j=\widehat{\mathbf T}_{\mathrm{full}}^j\mathbf S_{B,p}^j$，则在协调和约束条件一致时预测全场空间嵌套，可由 Ritz 原理得到相应单调性。也可直接训练 Bernstein 内部映射，无须构造完整接口模型，但不自动具有上述嵌套关系。

同一材料场与边界表示下，由 [[piml-substructural#4. 误差与使用边界|总览 §4]] 得

$$
\widehat{\mathbf K}_{B,p}^j-\mathbf K_{B,p}^j
=(\mathbf E_{B,p}^j)^{\mathsf T}\mathbf K_{ii}^j\mathbf E_{B,p}^j\succeq0.
\tag{19}
$$

相同载荷、零内部载荷、齐次支承、同一预测形函数组装与恢复、约束后正定且精确求解时，令 $\mathbf U$ 为细网格解，$C$ 为其柔度，$C_p$ 为精确 Bernstein 柔度，$\widehat C_p=\mathbf F^{\mathsf T}\widehat{\mathbf U}_{B,p}$，则（本页推导）

$$
\widehat C_p\le C_p\le C,
\qquad C-\widehat C_p=\|\mathbf U-\widehat{\mathbf U}_{B,p}\|_{\mathbf K}^2.
\tag{20}
$$

前两者比较来自同一约束空间中的刚度增量，后者来自预测全场空间中的 Ritz 正交性。总柔度差可分为边界限制的 $C-C_p$ 与代理引入的 $C_p-\widehat C_p$；后者一般不等于精确与预测降阶位移差的能量范数平方。独立训练不同次数时不保证 $\widehat C_p\le\widehat C_{p+1}$。非零给定位移不能直接套用式 (20)，浮点与求解误差另计。

采样矩阵须列满秩；规则完整张量网格每方向有 $m$ 个细单元时，$p\le m$ 的秩条件同 [[../substructure/exact-substructural-bernstein#4.4 次数提升与 full-trace|精确页 §4.4]]。$p=m$ 时边界求值矩阵可逆但通常不是单位矩阵；采用同一 full-trace 预测映射投影并同步变换载荷、约束时，与 full-trace PIML 等价。仅覆盖完整边界空间不保证内部预测精确，也不保证独立训练的两个模型等价。

**非零内部载荷。** 精确恢复还需特解 $\mathbf w_i^j=(\mathbf K_{ii}^j)^{-1}\mathbf f_i^j$；预测齐次形函数不能给出该特解，载荷投影与仿射恢复须一致处理，不能直接沿用本文流程。精确修正见 [[../substructure/exact-substructural-bernstein#4.4 次数提升与 full-trace|精确页 §4.4]]。
