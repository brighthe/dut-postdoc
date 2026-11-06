---
title: "基于 Lagrange 边界位移插值的 PIML 子结构分析"
type: concept
aliases:
  - PIML Lagrange Substructural Analysis
tags:
  - PIML
  - substructure
  - static-condensation
  - lagrange
status: draft
date_added: 2026-10-25
date_update: 2026-10-25
---

# 基于 Lagrange 边界位移插值的 PIML 子结构分析

沿用 [[../substructure/exact-substructural-lagrange|精确 Lagrange 子结构分析]] 的边界插值与求解框架，以 PIML 预测形函数的内部恢复矩阵，再由当前材料刚度作能量投影。仅讨论形函数预测；共同样本、训练目标与约束见 [[piml-substructural|PIML 总览]]。相对细网格解，同时存在边界插值误差与内部延拓代理误差。

假设同精确页：小应变线弹性静力、非重叠规则矩形／长方体子结构、接口网格及插值迹协调、统一次数 $p\ge1$、内部无载荷、位移约束位于子结构边界，且 $\mathbf K^j\succeq0,\mathbf K_{ii}^j\succ0$。几何、离散、编号及材料参数域相容时才可复用模型。

沿用精确页的 $\mathbf S_p^j,\mathbf q^j,\mathbf A_r^j,\mathbf Q,\mathbf K_{r,p}^j,\mathbf P_p$；预测算子及其解加帽号。新增 $\mathbf T_p^j$ 表示插值自由度到内部位移的精确映射，$\mathbf N_p^j=[\mathbf S_p^j;\mathbf T_p^j]$ 为对应形函数矩阵。

| 计算环节 | 精确 Lagrange | PIML 替代 |
|---|---|---|
| 边界插值 | 固定 $\mathbf S_p^j$ | 相同 |
| 局部刚度构造 | 内部求解后缩聚、投影 | 预测内部映射，再作能量投影 |
| 全局求解 | 求解插值自由度 | 保留组装与约束形式，使用预测刚度 |
| 内部恢复 | 局部回代 | 用构造刚度的同一预测映射恢复 |

## 1. 矩阵组装与边界位移插值

### 1.1 局部矩阵与自由度分块

细网格刚度与边界表示同精确页：

$$
\mathbf K^j(\boldsymbol\eta^j)
=\sum_{e\subset\Omega^j}(\mathbf G_e^j)^{\mathsf T}\mathbf K_e\mathbf G_e^j
=\begin{bmatrix}\mathbf K_{bb}^j&\mathbf K_{bi}^j\\\mathbf K_{ib}^j&\mathbf K_{ii}^j\end{bmatrix},
\qquad \mathbf u_b^j=\mathbf S_p^j\mathbf q^j.
\tag{1}
$$

$\boldsymbol\eta^j$ 为局部材料参数。沿用精确页的节点计数：$n_b$ 为细边界节点数，$n_r$ 为唯一边界插值点数，$\mathbf S_p^j\in\mathbb R^{d n_b\times d n_r}$，$\mathbf q^j\in\mathbb R^{d n_r}$，$d=2,3$。PIML 不改变边界块；当前材料场的 $\mathbf K^j$ 作用仍需计算，可不显式组装。

### 1.2 任意次数的一维基函数

取 $0=t_0<\cdots<t_p=1$，定义

$$
\ell_a^{(p)}(t)=\prod_{\substack{c=0\\c\ne a}}^p\frac{t-t_c}{t_a-t_c},
\qquad \ell_a^{(p)}(t_c)=\delta_{ac}.
\tag{2}
$$

常数与一次多项式再现性、节点选取同 [[../substructure/exact-substructural-lagrange#1.2 任意次数的一维基函数|精确页 §1.2]]。插值约束施加在细节点上，节点之间仍由原细网格有限元形函数表示。

### 1.3 二维子结构：逐边插值

边上细节点的位移为

$$
\mathbf u_b(\mathbf x_m)=\sum_{a=0}^p\ell_a^{(p)}(t(\mathbf x_m))\mathbf q_a.
\tag{3}
$$

求值系数乘 $\mathbf I_d$ 后形成 $\mathbf S_p^j$ 的行块；四边共享角点只编号一次，$n_r=4p$。

### 1.4 三维子结构：逐面张量积插值

面上采用 $Q_p$ 插值：

$$
\mathbf u_b(\mathbf x_m)=\sum_{a=0}^p\sum_{c=0}^p
\ell_a^{(p)}(s(\mathbf x_m))\ell_c^{(p)}(t(\mathbf x_m))\mathbf q_{ac},
\qquad n_r=8+12(p-1)+6(p-1)^2.
\tag{4}
$$

公共实体使用相同物理插值点和自由度，按参数方向反转或交换建立对应；共享细边界节点位移只写一次。细网格匹配本身不足以保证插值迹协调。

### 1.5 一次、二次与三次

| 次数 | 二维边插值 | 三维面插值 | 四边形插值点数 | 六面体插值点数 |
|---|---|---|---:|---:|
| $p=1$ | 线性 | 双线性 $Q_1$ | 4 | 8 |
| $p=2$ | 二次 | 双二次 $Q_2$ | 8 | 26 |
| $p=3$ | 三次 | 双三次 $Q_3$ | 12 | 56 |

基函数显式表达见 [[../substructure/exact-substructural-lagrange#1.5 一次、二次与三次|精确页 §1.5]]。次数决定边界空间与模型输出列数，不规定内部位移的多项式次数。

### 1.6 角点方案与一般几何映射

$p=1$ 即 `linear_corner`：$\mathbf S_1^j=\mathbf L^j$、$\mathbf q^j=\mathbf u_c^j$、$\mathbf A_r^j=\mathbf A_c^j$、$\mathbf Q=\mathbf U_C$。下文 $\mathbf T_1^j=\mathbf T_{\mathrm{corner}}^j$、$\mathbf K_{r,1}^j=\mathbf K_{s,\mathrm{corner}}^j$，全局 $\mathbf K_{r,1}=\mathbf K_C$，预测量对应加帽号。

一般四边形／六面体须满足 [[../substructure/exact-substructural-lagrange#1.6 角点方案与一般几何映射|精确页 §1.6]] 的粗几何映射与公共迹条件。相同 $Q_1$ 基的等参几何映射可再现物理仿射位移；该推广不自动适用于下文高次空间的嵌套结论。

与实验说明 `soptx:experiments/topopt_piml_substructure/substructure_linear_corner_piml_shape_vs_exact.md` §1 的符号对应如下（取 $p=1$，预测量对应加帽号）：

| 含义 | 本页 | 实验说明 |
|---|---|---|
| 边界插值矩阵 | $\mathbf S_1^j=\mathbf L^j$ | $L$ |
| 内部恢复矩阵、完整形函数 | $\mathbf T_1^j,\mathbf N_1^j$ | $N_i^j,N^j$ |
| 局部刚度、全局刚度 | $\mathbf K_{r,1}^j,\mathbf K_{r,1}$ | $K_c^j,K_C$ |
| 全局插值位移、载荷 | $\mathbf Q,\mathbf F_{r,1}$ | $U_C,F_C$ |
| 接口提取、全局边界映射 | $\mathbf A_r^j,\mathbf P_1$ | $A_c^j,P$ |
| 内部映射预测误差 | $\mathbf E_1^j$ | $D^j$ |
| 角点、内部刚体模态 | $\mathbf B_r^j,\mathbf B_i^j$ | $Q,\Phi$ |
| 边界节点数／位移自由度数 | $n_b$：节点数 | $n_b$：位移自由度数 |

**同名异义：**本页 $\mathbf Q$ 是全局插值位移向量，实验说明的 $Q\in\mathbb R^{24\times6}$ 是角点刚体模态矩阵，不能混用。边界计数满足 $n_b^{\mathrm{实验}}=d\,n_b^{\mathrm{本页}}$，三维时相差因子 $3$。本页继续沿用精确 Lagrange 页的记号。

## 2. 局部缩聚的 PIML 替代与插值自由度上的方程

精确内部映射与降阶刚度为

$$
\mathbf T_p^j=-(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j\mathbf S_p^j
=\mathbf T_{\mathrm{full}}^j\mathbf S_p^j,
\qquad \mathbf K_{r,p}^j=(\mathbf S_p^j)^{\mathsf T}\mathbf K_s^j\mathbf S_p^j.
\tag{5}
$$

$\mathbf K_s^j$ 为精确 full-trace Schur 补。监督训练离线求解式 (5) 生成 $\mathbf T_p^j$ 标签；在线用 $\widehat{\mathbf T}_p^j=\mathcal F_p(\boldsymbol\eta^j;\boldsymbol\theta)$ 替代该内部求解。输出行数为内部位移自由度数，列数为 $d n_r$；$p=1$ 时即总览原角点模型。$\mathcal F_p$ 包含网络预测与约束补全，同一次线性求解中预测算子固定。

训练目标见 [[piml-substructural#3.2 材料样本与训练目标|总览 §3.2]]。除固定边界块外，需再现刚体运动：记 $\mathbf B_r^j,\mathbf B_b^j,\mathbf B_i^j$ 为同一组刚体模态在插值点、细边界与内部的位移，则要求 $\mathbf S_p^j\mathbf B_r^j=\mathbf B_b^j$、$\widehat{\mathbf T}_p^j\mathbf B_r^j=\mathbf B_i^j$；此处用 $\mathbf B$ 避免与全场自由度提取算子混淆。力学约束见 [[piml-substructural#3.1 网络输出与力学约束|总览 §3.1]]。

### 2.1 显式构造与组装

以同一当前材料刚度作能量投影：

$$
\begin{aligned}
\widehat{\mathbf N}_p^j&=\begin{bmatrix}\mathbf S_p^j\\\widehat{\mathbf T}_p^j\end{bmatrix},\\
\widehat{\mathbf K}_{r,p}^j
&=(\widehat{\mathbf N}_p^j)^{\mathsf T}\mathbf K^j\widehat{\mathbf N}_p^j\\
&=(\mathbf S_p^j)^{\mathsf T}\mathbf K_{bb}^j\mathbf S_p^j
+(\mathbf S_p^j)^{\mathsf T}\mathbf K_{bi}^j\widehat{\mathbf T}_p^j
+(\widehat{\mathbf T}_p^j)^{\mathsf T}\mathbf K_{ib}^j\mathbf S_p^j
+(\widehat{\mathbf T}_p^j)^{\mathsf T}\mathbf K_{ii}^j\widehat{\mathbf T}_p^j.
\end{aligned}
\tag{6}
$$

预测内部场一般不满足精确平衡，四项不能简化为精确 Schur 投影。能量投影保证对称半正定；正确的刚体零空间仍依赖刚体再现及离散无额外零能模式。

令 $\widehat{\mathbf q}^j=\mathbf A_r^j\widehat{\mathbf Q}$，组装

$$
\widehat{\mathbf K}_{r,p}=\sum_j(\mathbf A_r^j)^{\mathsf T}\widehat{\mathbf K}_{r,p}^j\mathbf A_r^j,
\qquad \mathbf f_{r,p}^j=(\mathbf S_p^j)^{\mathsf T}\mathbf f_b^j,
\qquad \mathbf F_{r,p}=\sum_j(\mathbf A_r^j)^{\mathsf T}\mathbf f_{r,p}^j.
\tag{7}
$$

载荷按边界映射投影以保持虚功，不能只抽取插值点载荷；外载只分配一次。内部无载荷时，右端与精确 Lagrange 系统相同。

### 2.2 隐式算子作用

不形成局部或全局降阶矩阵时，对全局输入 $\mathbf v$ 逐块计算

$$
\begin{aligned}
\mathbf v_r^j&=\mathbf A_r^j\mathbf v,\\
\begin{bmatrix}\mathbf a_b^j\\\mathbf a_i^j\end{bmatrix}
&=\mathbf K^j\begin{bmatrix}\mathbf S_p^j\mathbf v_r^j\\\widehat{\mathbf T}_p^j\mathbf v_r^j\end{bmatrix},\\
\mathbf y_r^j&=(\mathbf S_p^j)^{\mathsf T}\mathbf a_b^j
+(\widehat{\mathbf T}_p^j)^{\mathsf T}\mathbf a_i^j,\qquad
\widehat{\mathbf K}_{r,p}\mathbf v=\sum_j(\mathbf A_r^j)^{\mathsf T}\mathbf y_r^j.
\end{aligned}
\tag{8}
$$

精确页中的内部求解由预测矩阵乘法替代。$\mathbf a_i^j$ 一般非零，转置投影的内部项不能省去；式 (8) 与式 (7) 的矩阵作用相同。

### 2.3 结合单元层 Matrix-Free

满足精确页的共享参考单元条件 $\mathbf K_e=s_e\mathbf K_0$ 时，令

$$
\mathcal K^j(\mathbf x)=\sum_{e\subset\Omega^j}(\mathbf G_e^j)^{\mathsf T}s_e\mathbf K_0\mathbf G_e^j\mathbf x,
\qquad
\begin{bmatrix}\mathbf a_b^j\\\mathbf a_i^j\end{bmatrix}
=\mathcal K^j\left(\begin{bmatrix}\mathbf S_p^j\mathbf v_r^j\\\widehat{\mathbf T}_p^j\mathbf v_r^j\end{bmatrix}\right).
\tag{9}
$$

再按式 (8) 投影累加。每次作用需一次细网格刚度作用及预测映射的正、转置乘法，不需在线分解 $\mathbf K_{ii}^j$。也可在 setup 中对 $\widehat{\mathbf N}_p^j$ 各列作用后保存局部刚度，仅省去全局组装；角点实现见 [[../matrix-free/mf-piml-substructural#3. 角点接口路径|PIML Matrix-Free §3]]。

## 3. 求解与位移恢复

### 3.1 位移约束与全局求解

预测系统为 $\widehat{\mathbf K}_{r,p}\widehat{\mathbf Q}=\mathbf F_{r,p}$，仅在自由变分方向上要求平衡。可直接指定插值自由度时，$\widehat{\mathbf Q}_D=\mathbf d_D$，求解

$$
(\widehat{\mathbf K}_{r,p})_{FF}\widehat{\mathbf Q}_F
=(\mathbf F_{r,p})_F-(\widehat{\mathbf K}_{r,p})_{FD}\mathbf d_D.
\tag{10}
$$

一般细边界节点约束通过全局迹映射 $\mathbf P_p$ 转换：$\mathbf A_b^j\mathbf P_p=\mathbf S_p^j\mathbf A_r^j$，$\mathbf C=\mathbf P_p[D,:]$，要求 $\mathbf C\widehat{\mathbf Q}=\mathbf d$。须检查相容性并去除冗余约束；不能把固定细节点等同于固定角点。不相容时需扩充空间或明确近似边界数据。

取 $\mathbf C\mathbf Q_0=\mathbf d$、$\operatorname{range}(\mathbf Z)=\ker\mathbf C$，令 $\widehat{\mathbf Q}=\mathbf Q_0+\mathbf Z\widehat{\mathbf a}$，求解

$$
\mathbf Z^{\mathsf T}\widehat{\mathbf K}_{r,p}\mathbf Z\widehat{\mathbf a}
=\mathbf Z^{\mathsf T}(\mathbf F_{r,p}-\widehat{\mathbf K}_{r,p}\mathbf Q_0).
\tag{11}
$$

显式实现用组装矩阵，隐式实现用式 (8)；约束消去后正定时可用 CG。也可求解乘子系统

$$
\begin{bmatrix}\widehat{\mathbf K}_{r,p}&\mathbf C^{\mathsf T}\\\mathbf C&\mathbf0\end{bmatrix}
\begin{bmatrix}\widehat{\mathbf Q}\\\widehat{\boldsymbol\lambda}_D\end{bmatrix}
=\begin{bmatrix}\mathbf F_{r,p}\\\mathbf d\end{bmatrix}.
\tag{12}
$$

$\mathbf C$ 行满秩且刚度在 $\ker\mathbf C$ 上正定时解唯一；不能直接对该鞍点系统使用 CG。$p=1$ 时 $\mathbf C=\mathbf C_D$，$\mathbf P_1$ 对应原角点记号 $\mathbf P$。

### 3.2 边界与内部位移恢复

两种实现均使用构造刚度的同一预测形函数：

$$
\widehat{\mathbf u}_b^j=\mathbf S_p^j\mathbf A_r^j\widehat{\mathbf Q},
\qquad \widehat{\mathbf u}_i^j=\widehat{\mathbf T}_p^j\mathbf A_r^j\widehat{\mathbf Q}.
\tag{13}
$$

共享边界只写一次，各块内部逐块放回，得到全场 $\widehat{\mathbf U}_p$。内部残量为

$$
\mathbf r_i^j=\mathbf K_{ib}^j\widehat{\mathbf u}_b^j+\mathbf K_{ii}^j\widehat{\mathbf u}_i^j
=\mathbf K_{ii}^j\mathbf E_p^j\widehat{\mathbf q}^j,
\qquad \mathbf E_p^j=\widehat{\mathbf T}_p^j-\mathbf T_p^j.
\tag{14}
$$

代理系统收敛不代表原细网格内部平衡；边界也仅满足允许变分方向上的平衡。内部预测位移不必是 $p$ 次多项式。

## 4. 与 full-trace 的关系及近似性质

### 4.1 精确缩聚与边界近似

可直接预测 $\widehat{\mathbf T}_p^j$，或先预测完整接口映射再投影：

$$
\widehat{\mathbf T}_p^j=\widehat{\mathbf T}_{\mathrm{full}}^j\mathbf S_p^j,
\qquad \widehat{\mathbf N}_p^j=\widehat{\mathbf N}_{\mathrm{full}}^j\mathbf S_p^j,
\qquad \widehat{\mathbf K}_{r,p}^j=(\mathbf S_p^j)^{\mathsf T}\widehat{\mathbf K}_s^j\mathbf S_p^j.
\tag{15}
$$

式 (15) 只对同一完整接口预测映射及其投影成立，不要求先形成完整接口刚度；直接训练的模型不自动满足该关系。完整接口预测见 [[piml-substructural-full-trace#2. 局部缩聚刚度的 PIML 替代|full-trace PIML §2]]。

采用式 (15) 时，全局有 $\widehat{\mathbf K}_{r,p}=\mathbf P_p^{\mathsf T}\widehat{\mathbf K}_\Gamma\mathbf P_p$；两种预测方式的载荷均为 $\mathbf F_{r,p}=\mathbf P_p^{\mathsf T}\mathbf F_\Gamma$。预测映射取精确值时回到精确 Lagrange；边界空间未覆盖 full-trace 时仍有迹降阶误差。

### 4.2 Ritz 最佳逼近与柔度

同一材料场、边界插值下，由 [[piml-substructural#4. 误差与使用边界|总览 §4]] 的能量展开得

$$
\widehat{\mathbf K}_{r,p}^j-\mathbf K_{r,p}^j
=(\mathbf E_p^j)^{\mathsf T}\mathbf K_{ii}^j\mathbf E_p^j\succeq0.
\tag{16}
$$

相同载荷、零内部载荷、齐次位移约束、同一预测形函数组装与恢复、约束后正定且精确求解时，令 $\mathbf U$ 为细网格解，$\mathbf U_p$ 为精确 Lagrange 恢复解，定义 $C=\mathbf F^{\mathsf T}\mathbf U$、$C_p=\mathbf F^{\mathsf T}\mathbf U_p$、$\widehat C_p=\mathbf F^{\mathsf T}\widehat{\mathbf U}_p$。则（本页推导）

$$
\widehat C_p\le C_p\le C,
\qquad C-\widehat C_p=\|\mathbf U-\widehat{\mathbf U}_p\|_{\mathbf K}^2.
\tag{17}
$$

第一项比较来自同一约束空间中的刚度半正定增量；第二个等式来自预测全场空间中的 Ritz 正交性。预测解是在其自身空间中的最佳逼近，不是精确平衡延拓空间中的最佳逼近。不能把 $C_p-\widehat C_p$ 直接写成 $\|\mathbf U_p-\widehat{\mathbf U}_p\|_{\mathbf K}^2$，因为两种全场空间一般不嵌套。非零给定位移不能直接套用式 (17)，也不能跨不同材料设计比较该柔度方向。

### 4.3 次数、嵌套与满秩

边界采样矩阵 $\mathbf S_p^j$ 必须列满秩，次数与采样条件同 [[../substructure/exact-substructural-lagrange#4.3 次数、嵌套与满秩|精确页 §4.3]]。独立训练各次数模型时，边界空间嵌套不保证预测全场空间嵌套，故不能保证 $\widehat C_p\le\widehat C_{p+1}$ 或总误差单调减小。

若所有次数均由同一个固定 $\widehat{\mathbf T}_{\mathrm{full}}^j$ 按式 (15) 投影，且沿用精确页的几何、协调及约束条件，则预测全场空间嵌套，可由 Ritz 原理恢复单调性。插值点覆盖全部细边界节点、$\mathbf S_p^j$ 为重排单位矩阵时，得到 full-trace PIML；内部映射仍须精确才能恢复细网格解。

### 4.4 基底选择与空间选择

若 $\mathbf S'_p=\mathbf S_p\mathbf T$、$\mathbf T$ 可逆，保持同一预测全场空间还需

$$
\widehat{\mathbf T}'_p=\widehat{\mathbf T}_p\mathbf T,
\qquad \widehat{\mathbf K}'_{r,p}=\mathbf T^{\mathsf T}\widehat{\mathbf K}_{r,p}\mathbf T,
\qquad \mathbf f'_{r,p}=\mathbf T^{\mathsf T}\mathbf f_{r,p}.
\tag{18}
$$

界面编号与约束同步转换时，以上只是坐标变换。同次 Lagrange 与 Bernstein 若各自独立训练，预测内部映射未必满足该关系，解也未必相同；预测映射、刚度与约束的对应见 [[piml-substructural-bernstein#4.3 刚度、载荷与解的对应|Bernstein PIML §4.3]]。精确换基条件见 [[../substructure/exact-substructural-lagrange#4.4 基底选择与空间选择|精确页 §4.4]]。

**非零内部载荷。** 精确恢复还需特解 $\mathbf w_i^j=(\mathbf K_{ii}^j)^{-1}\mathbf f_i^j$。仅预测齐次形函数不能给出该特解；载荷投影与仿射恢复须一起处理，不能直接沿用本文零内部载荷流程，见 [[../substructure/exact-substructural-full-trace#4.1 形函数表示与非零内部载荷|精确 full-trace §4.1]]。

### 4.5 误差定位与量级的适用边界

在 §4.2 的条件下，柔度差可分为

$$
C-\widehat C_p=(C-C_p)+(C_p-\widehat C_p).
\tag{19}
$$

两项分别量化边界限制与同一边界空间中的代理所造成的柔度下降，需要细网格和精确 Lagrange 参考求解。内部残量可定位预测平衡缺陷，但不是完整位移误差估计器。材料非均质、细网格采样及网络误差共同影响结果，不能仅由次数 $p$ 推断总误差量级；精确边界误差的适用限制见 [[../substructure/exact-substructural-lagrange#4.5 误差定位与量级的适用边界|精确页 §4.5]]。
