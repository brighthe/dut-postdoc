---
title: "基于 Lagrange 边界位移插值的子结构分析"
type: concept
aliases:
  - Lagrange Boundary Displacement Interpolation
tags:
  - finite-element
  - substructure
  - static-condensation
  - lagrange
status: draft
date_added: 2026-10-24
date_update: 2026-10-25
---

# 基于 Lagrange 边界位移插值的子结构分析

用较少的 Lagrange 插值自由度表示子结构全部细网格边界节点位移，通过局部静力平衡消去内部自由度，求解全局插值自由度后恢复位移场。与 [[exact-substructural-full-trace|full-trace]] 相比，本方法限制了允许的边界位移空间，通常引入边界近似误差；局部静力缩聚仍精确计算，文件名中的 `exact` 不表示降阶解与细网格解相同。

本文考虑小应变线弹性静力问题、沿细网格单元边界非重叠划分的规则矩形／长方体子结构，接口网格匹配，采用统一次数 $p\ge1$。内部载荷默认置零，位移约束位于子结构边界，固定边界后的内部矩阵可逆。边界包括块间接口和物理外边界；边界位移是待求量，不等于给定位移边界条件。

以本页为精确基准、用预测内部映射和能量投影替代局部缩聚的流程见 [[../piml/piml-substructural-lagrange|Lagrange PIML 子结构分析]]。

## 1. 矩阵组装与边界位移插值

### 1.1 局部矩阵与自由度分块

沿用 full-trace 的局部组装及边界 $b$、内部 $i$ 分块：

$$
\mathbf K^j=\sum_{e\subset\Omega^j}(\mathbf G_e^j)^{\mathsf T}\mathbf K_e\mathbf G_e^j
=\begin{bmatrix}\mathbf K_{bb}^j&\mathbf K_{bi}^j\\\mathbf K_{ib}^j&\mathbf K_{ii}^j\end{bmatrix},
\qquad
\mathbf u_b^j=\mathbf S_p^j\mathbf q^j.
\tag{1}
$$

$\mathbf G_e^j$ 提取单元位移，$\mathbf q^j\in\mathbb R^{d n_r}$ 汇集本块 $n_r$ 个唯一边界插值点的位移分量，$\mathbf S_p^j\in\mathbb R^{d n_b\times d n_r}$ 在 $n_b$ 个细边界节点处评价插值函数，$d=2,3$。插值点不必与细网格节点重合；$\mathbf q^j$ 是辅助边界多项式在插值点处的值。

插值约束作用于细网格节点值。节点之间仍按原细网格有限元形函数表示位移，因此 $p>1$ 时，最终细网格迹一般不等于辅助多项式在所有位置的值。

### 1.2 任意次数的一维基函数

在 $[0,1]$ 上选取互异节点 $0=t_0<t_1<\cdots<t_p=1$，定义

$$
\ell_a^{(p)}(t)=\prod_{\substack{c=0\\c\ne a}}^p\frac{t-t_c}{t_a-t_c},
\qquad
\ell_a^{(p)}(t_c)=\delta_{ac},\quad
\sum_{a=0}^p\ell_a^{(p)}(t)=1,\quad
\sum_{a=0}^p t_a\ell_a^{(p)}(t)=t.
\tag{2}
$$

式 (2) 分别给出节点插值性、常数与一次多项式再现性。一般推导不限定节点分布；下文具体例子使用等距节点 $t_a=a/p$。

### 1.3 二维子结构：逐边插值

将每条边参数化到 $[0,1]$，对边上细节点 $\mathbf x_m$，有

$$
\mathbf u_b(\mathbf x_m)
=\sum_{a=0}^p\ell_a^{(p)}(t(\mathbf x_m))\mathbf q_a.
\tag{3}
$$

将标量求值系数乘以 $\mathbf I_d$ 并放入对应点的列，即得 $\mathbf S_p^j$ 的行块。四条边共享角点只编号一次，唯一插值点数为 $n_r=4+4(p-1)=4p$。

### 1.4 三维子结构：逐面张量积插值

在每个面取仿射参数 $(s,t)\in[0,1]^2$，采用每个方向次数不超过 $p$ 的 $Q_p$ 表示：

$$
\mathbf u_b(\mathbf x_m)
=\sum_{a=0}^p\sum_{c=0}^p
\ell_a^{(p)}(s(\mathbf x_m))\ell_c^{(p)}(t(\mathbf x_m))\mathbf q_{ac}.
\tag{4}
$$

顶点、棱内部、面内部的插值点分别编号，六面体唯一边界插值点数为

$$
n_r=8+12(p-1)+6(p-1)^2.
\tag{5}
$$

相邻面和相邻子结构在公共实体上使用相同物理插值点与自由度，按参数方向反转或交换建立编号对应，保证公共细节点位移一致。每个细边界节点的行只写一次；棱或顶点上相邻面给出相同值，不能将这些位移值重复相加。

### 1.5 一次、二次与三次

等距节点下，一维基函数向量为

$$
\begin{aligned}
\boldsymbol\ell^{(1)}(t)&=(1-t,\ t),\\
\boldsymbol\ell^{(2)}(t)&=((1-t)(1-2t),\ 4t(1-t),\ t(2t-1)),\\
\boldsymbol\ell^{(3)}(t)&=\big(
-\tfrac92(t-\tfrac13)(t-\tfrac23)(t-1),\
\tfrac{27}2t(t-\tfrac23)(t-1),\
-\tfrac{27}2t(t-\tfrac13)(t-1),\
\tfrac92t(t-\tfrac13)(t-\tfrac23)\big).
\end{aligned}
\tag{6}
$$

| 次数 | 二维：边上的表示 | 三维：面上的表示 | 四边形插值点数 | 六面体插值点数 |
|---|---|---|---:|---:|
| $p=1$ | 线性 | 双线性 $Q_1$ | 4 | 8 |
| $p=2$ | 二次 | 双二次 $Q_2$ | 8 | 26 |
| $p=3$ | 三次 | 双三次 $Q_3$ | 12 | 56 |

$p=1$ 即角点方案。三维可称“八角点 $Q_1$ 边界迹插值”：它是体三线性表示在边界上的限制，面上双线性、棱上线性；内部位移仍由平衡方程恢复。三次 Lagrange 与三次 Bernstein 张成相同的一维多项式空间，但系数意义不同，见 §4.4。

### 1.6 角点方案与一般几何映射

$p=1$ 时，记 $\mathbf S_1^j=\mathbf L^j$、$\mathbf q^j=\mathbf u_c^j$；角点形函数及其内部延拓为

$$
\mathbf T_{\mathrm{corner}}^j=-(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j\mathbf L^j,
\qquad
\mathbf N_{\mathrm{corner}}^j=
\begin{bmatrix}\mathbf L^j\\\mathbf T_{\mathrm{corner}}^j\end{bmatrix},
\qquad
\mathbf K_{s,\mathrm{corner}}^j
=(\mathbf L^j)^{\mathsf T}\mathbf K_s^j\mathbf L^j
=(\mathbf N_{\mathrm{corner}}^j)^{\mathsf T}\mathbf K^j\mathbf N_{\mathrm{corner}}^j.
$$

本节补充超出前述规则矩形／长方体的几何条件，不将其自动推广到本文所有高次空间与嵌套结论。一般四边形／六面体子结构须给定一一对应的粗参考单元映射 $\mathbf x=\mathbf F^j(\boldsymbol\xi)$，据此确定细边界节点的参考坐标，令 $(\mathbf L^j)_{k,c}=N_c(\boldsymbol\xi_k)\mathbf I_d$。$N_c$ 是张量积 $Q_1$ 角点形函数，二维双线性、三维三线性，不是总次数不超过一的多项式。

相邻子结构须在公共界面采用一致的角点、几何参数化与插值迹；细网格匹配本身不足以保证粗迹协调。采用相同 $Q_1$ 基的等参几何映射时，可以再现物理坐标中的仿射位移及刚体运动。任意细单元集合不自动满足这些几何条件。

## 2. 静力缩聚与插值自由度上的方程

内部无载荷时，消去内部自由度：

$$
\mathbf u_i^j=-(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j\mathbf S_p^j\mathbf q^j,
\qquad
\mathbf K_s^j=\mathbf K_{bb}^j-\mathbf K_{bi}^j(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j.
\tag{7}
$$

下文逆矩阵均通过线性系统求解实现。将 $\mathbf u_b^j=\mathbf S_p^j\mathbf q^j$ 代入缩聚势能 $\frac12(\mathbf u_b^j)^{\mathsf T}\mathbf K_s^j\mathbf u_b^j-(\mathbf u_b^j)^{\mathsf T}\mathbf f_b^j$，对 $\mathbf q^j$ 取变分，得到

$$
\mathbf K_{r,p}^j=(\mathbf S_p^j)^{\mathsf T}\mathbf K_s^j\mathbf S_p^j,
\qquad
\mathbf f_{r,p}^j=(\mathbf S_p^j)^{\mathsf T}\mathbf f_b^j.
\tag{8}
$$

载荷按相同映射投影以保持虚功，不能只抽取插值点上的载荷。降阶平衡只要求允许的边界虚位移下残量正交，不再要求每个自由细边界节点的残量分别为零。

### 2.1 显式构造与组装

令 $\mathbf Q$ 为全局唯一插值自由度，$\mathbf q^j=\mathbf A_r^j\mathbf Q$。形成局部降阶矩阵后组装：

$$
\mathbf K_{r,p}=\sum_j(\mathbf A_r^j)^{\mathsf T}\mathbf K_{r,p}^j\mathbf A_r^j,
\qquad
\mathbf F_{r,p}=\sum_j(\mathbf A_r^j)^{\mathsf T}\mathbf f_{r,p}^j.
\tag{9}
$$

每项外载荷只分配一次。可先形成 $\mathbf K_s^j$ 再投影，也可求解 $\mathbf K_{ii}^j\mathbf Z^j=\mathbf K_{ib}^j\mathbf S_p^j$，直接形成 $(\mathbf S_p^j)^{\mathsf T}(\mathbf K_{bb}^j\mathbf S_p^j-\mathbf K_{bi}^j\mathbf Z^j)$，无需保存完整 Schur 补。

### 2.2 隐式算子作用

给定全局输入 $\mathbf v$，逐块计算

$$
\begin{aligned}
\mathbf v_b^j&=\mathbf S_p^j\mathbf A_r^j\mathbf v,
&\mathbf K_{ii}^j\mathbf z_i^j&=\mathbf K_{ib}^j\mathbf v_b^j,\\
\mathbf y_b^j&=\mathbf K_{bb}^j\mathbf v_b^j-\mathbf K_{bi}^j\mathbf z_i^j,
&\mathbf K_{r,p}\mathbf v&=\sum_j(\mathbf A_r^j)^{\mathsf T}(\mathbf S_p^j)^{\mathsf T}\mathbf y_b^j.
\end{aligned}
\tag{10}
$$

即“边界插值 → Schur 补作用 → 转置投影 → 全局累加”。不形成局部或全局降阶矩阵，结果与式 (9) 的矩阵作用相同。

### 2.3 结合单元层 Matrix-Free

若单元满足共享参考刚度条件 $\mathbf K_e=s_e\mathbf K_0$，定义 $\mathcal K^j(\mathbf x)=\sum_e(\mathbf G_e^j)^{\mathsf T}s_e\mathbf K_0\mathbf G_e^j\mathbf x$。式 (10) 中的块乘法可由

$$
\begin{bmatrix}\mathbf a_b^j\\\mathbf a_i^j\end{bmatrix}
=\mathcal K^j\left(\begin{bmatrix}\mathbf v_b^j\\\mathbf0\end{bmatrix}\right),
\quad
\mathbf K_{ii}^j\mathbf z_i^j=\mathbf a_i^j,
\quad
\mathbf y_b^j=\mathbf a_b^j-
\left[\mathcal K^j\left(\begin{bmatrix}\mathbf0\\\mathbf z_i^j\end{bmatrix}\right)\right]_b
\tag{11}
$$

替代，再按式 (10) 投影累加。共享参考单元 EA 的几何、本构及编号条件见 [[exact-substructural-full-trace#2.2.1 结合单元层 Matrix-Free|full-trace §2.2.1]]。内部矩阵仍可组装分解并在系数不变时复用；插值次数改变不改变该内部矩阵。

## 3. 求解与位移恢复

### 3.1 位移约束与全局求解

全局方程为 $\mathbf K_{r,p}\mathbf Q=\mathbf F_{r,p}$，仅在自由变分方向上要求平衡。若约束可直接指定插值自由度 $\mathbf Q_D=\mathbf d_D$，则

$$
(\mathbf K_{r,p})_{FF}\mathbf Q_F
=(\mathbf F_{r,p})_F-(\mathbf K_{r,p})_{FD}\mathbf d_D.
\tag{12}
$$

例如整个外面固定时，将该面全部插值位移置零即可。若给定的是若干细节点位移，则一般得到 $\mathbf C\mathbf Q=\mathbf d$，不能直接当作某个插值点的约束。要求这些约束在所选空间中可满足；否则需扩充空间或明确采用近似边界数据。

对相容约束，取 $\mathbf C\mathbf Q_0=\mathbf d$，令 $\mathbf Z$ 的列构成 $\ker\mathbf C$ 的基，写 $\mathbf Q=\mathbf Q_0+\mathbf Z\mathbf a$，求解

$$
\mathbf Z^{\mathsf T}\mathbf K_{r,p}\mathbf Z\mathbf a
=\mathbf Z^{\mathsf T}(\mathbf F_{r,p}-\mathbf K_{r,p}\mathbf Q_0).
\tag{13}
$$

显式实现使用组装矩阵，隐式实现使用式 (10) 的作用；约束消去后假设系统正定，排除未约束刚体运动和冗余插值自由度。

也可用 Lagrange 乘子施加约束：

$$
\begin{bmatrix}\mathbf K_{r,p}&\mathbf C^{\mathsf T}\\\mathbf C&\mathbf0\end{bmatrix}
\begin{bmatrix}\mathbf Q\\\boldsymbol\lambda_D\end{bmatrix}
=\begin{bmatrix}\mathbf F_{r,p}\\\mathbf d\end{bmatrix}.
$$

去除冗余约束行后，$\mathbf C$ 行满秩且 $\mathbf K_{r,p}$ 在 $\ker\mathbf C$ 上正定时，该鞍点系统有唯一解。角点方案对应 $\mathbf Q=\mathbf U_C$、$\mathbf C=\mathbf C_D$、$\mathbf K_{r,p}=\mathbf K_C$；不能直接对鞍点系统使用 CG，应采用式 (13) 等约束消去方式。

### 3.2 边界与内部位移恢复

求得 $\mathbf Q$ 后，逐块恢复

$$
\mathbf u_b^j=\mathbf S_p^j\mathbf A_r^j\mathbf Q,
\qquad
\mathbf u_i^j=-(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j\mathbf u_b^j.
\tag{14}
$$

共享边界位移只写入一次，再放回各块内部位移，得到细网格全场。$p$ 限定的是辅助边界多项式的次数，内部位移通常不是 $p$ 次多项式，其细节点值取决于本块材料与平衡方程。

## 4. 与 full-trace 的关系及近似性质

### 4.1 精确缩聚与边界近似

令 $\mathbf P_p$ 将全局插值自由度映射到全局细边界节点，满足 $\mathbf A_b^j\mathbf P_p=\mathbf S_p^j\mathbf A_r^j$，其中 $\mathbf A_b^j$ 为 full-trace 的边界提取矩阵。由式 (9) 得

$$
\mathbf U_{\Gamma,p}=\mathbf P_p\mathbf Q,
\qquad
\mathbf K_{r,p}=\mathbf P_p^{\mathsf T}\mathbf K_\Gamma\mathbf P_p,
\qquad
\mathbf F_{r,p}=\mathbf P_p^{\mathsf T}\mathbf F_\Gamma.
\tag{15}
$$

因此这是 full-trace 系统在受限边界空间上的 Galerkin 投影。显式与隐式实现求解同一个降阶问题；对给定载荷，只有当 full-trace 解属于满足相同约束的插值空间时，才恢复同一个细网格解。算子与求解误差另计，不与边界近似误差混合。

### 4.2 Ritz 最佳逼近与柔度

以下采用相同载荷与齐次位移约束，均在自由边界分量上讨论，使 $\mathbf K_\Gamma$ 正定。令 $\mathcal V_p$ 为插值表示满足这些约束后的子空间，$\mathbf U_\Gamma$ 为 full-trace 解，则

$$
\|\mathbf U_\Gamma-\mathbf U_{\Gamma,p}\|_{\mathbf K_\Gamma}
=\min_{\mathbf V\in\mathcal V_p}\|\mathbf U_\Gamma-\mathbf V\|_{\mathbf K_\Gamma},
\qquad
C-C_p=\|\mathbf U_\Gamma-\mathbf U_{\Gamma,p}\|_{\mathbf K_\Gamma}^2\ge0,
\tag{16}
$$

其中 $C=\mathbf F_\Gamma^{\mathsf T}\mathbf U_\Gamma$、$C_p=\mathbf F_\Gamma^{\mathsf T}\mathbf U_{\Gamma,p}$。式 (16) 来自 Galerkin 正交性；由于内部均为精确平衡延拓，该边界误差能量也等于恢复全场的误差能量。受限模型柔度不大于 full-trace；非零给定位移需先作提升，不能直接套用这里的柔度差公式。

### 4.3 次数、嵌套与满秩

固定子结构划分、仿射参数化、细网格采样和物理约束时，完整多项式空间满足 $P_p\subset P_{p+1}$、$Q_p\subset Q_{p+1}$，故其采样后的协调边界空间亦嵌套。即使不同次数的插值节点集合不嵌套，精确求解下仍有

$$
\mathcal V_p\subseteq\mathcal V_{p+1},
\qquad
\|\mathbf U_\Gamma-\mathbf U_{\Gamma,p+1}\|_{\mathbf K_\Gamma}
\le\|\mathbf U_\Gamma-\mathbf U_{\Gamma,p}\|_{\mathbf K_\Gamma},
\qquad C_p\le C_{p+1}\le C.
\tag{17}
$$

实现时必须保证采样矩阵 $\mathbf S_p^j$ 列满秩，否则存在非零插值系数对应零细节点位移，导致冗余自由度。次数增加并不允许独立自由度无限超过细边界节点数；欠采样时应减少次数或消除冗余基。

例如规则子结构每个坐标方向有 $m$ 个细单元、$m+1$ 个细节点，取 $p\le m$ 可在完整张量网格上保持列满秩；$p=m$ 且插值点取全部细边界节点时，$\mathbf S_p^j$ 为重排后的单位矩阵，退化为 full-trace。一般情况下，是否对所有载荷等价，应检查受约束插值空间是否覆盖完整自由边界空间，不能仅凭“高次”判断。

### 4.4 基底选择与空间选择

若另一个基底满足 $\mathbf S'_p=\mathbf S_p\mathbf T$，其中 $\mathbf T$ 可逆，且界面协调与位移约束按同一物理空间转换，则只改变坐标：

$$
\mathbf q=\mathbf T\mathbf q',\qquad
\mathbf K'_{r,p}=\mathbf T^{\mathsf T}\mathbf K_{r,p}\mathbf T,
\qquad
\mathbf f'_{r,p}=\mathbf T^{\mathsf T}\mathbf f_{r,p}.
\tag{18}
$$

同次 Lagrange 与 Bernstein 多项式基在上述条件下给出相同精确位移，矩阵条件数、浮点误差及学习代理误差则可能不同。提高次数改变近似空间，更换同空间基底不改变其最佳逼近误差。full-trace 描述自由度保留范围，Lagrange 描述基底类型，两者不是互斥分类。

具体换基矩阵、二次实例及约束转换见 [[exact-substructural-bernstein#4. 与 Lagrange、full-trace 的关系|Bernstein 页 §4]]；该页采用控制系数而非插值节点值，并给出相同局部缩聚与全局恢复流程。

**非零内部载荷。** 若 $\mathbf f_i^j\ne\mathbf0$，刚度不变，式 (8) 的载荷及式 (14) 的内部恢复改为

$$
\widetilde{\mathbf f}_{r,p}^j=(\mathbf S_p^j)^{\mathsf T}
\left[\mathbf f_b^j-\mathbf K_{bi}^j(\mathbf K_{ii}^j)^{-1}\mathbf f_i^j\right],
\qquad
\mathbf u_i^j=(\mathbf K_{ii}^j)^{-1}(\mathbf f_i^j-\mathbf K_{ib}^j\mathbf u_b^j).
\tag{19}
$$


### 4.5 误差定位与量级的适用边界

在 §4.2 的零内部载荷、相同外载及齐次位移约束条件下，由 Schur 补组装式与 Galerkin 正交性，可将柔度差分解到各块（本页推导）：

$$
C-C_p=\sum_j\mathbf e_j^{\mathsf T}\mathbf K_s^j\mathbf e_j,
\qquad
\mathbf e_j=\mathbf A_b^j(\mathbf U_\Gamma-\mathbf U_{\Gamma,p}).
$$

这需要一次 full-trace 参考求解，得到的是后验误差定位，不是只用降阶解即可计算的廉价估计器。若内部载荷非零，两种恢复都包含相同的 $\mathbf w_i^j$，误差能量关系仍成立；柔度须按完整外载与仿射恢复位移定义，包含共同的内部载荷常数项。

误差量级还依赖材料与网格条件。记 $H$ 为子结构尺寸、$h$ 为细单元尺寸、$\varepsilon$ 为材料非均质尺度，$C_h$ 为细网格柔度、$C_{Q_1,H}$ 为粗 $Q_1$ 模型柔度。以下量级尚未完成核验：

- **均质或缓变材料**：角点迹的仿射再现性不足以单独推出 $O(H)$ 能量误差和 $O(H^2)$ 柔度误差；还需解的正则性、形状规则网格、材料条件及一致逼近估计。上述量级及“与细网格尺寸 $h$ 无关”的表述待补全证明；缓变材料下仿射位移也不自动满足内部平衡。若粗 $Q_1$ 函数可嵌入同一细网格空间、具有相同允许边界迹，且内部无载荷、齐次支承，则内部能量最小化给出 $C_{Q_1,H}\le C_p\le C_h$（此处 $p=1$）；嵌入条件不满足时不能直接使用。
- **细尺度非均质材料**：在 $h<\varepsilon\ll H$ 的尺度背景下，线性边界 MsFEM 的 $H+\sqrt{\varepsilon/H}$ 共振误差形式仍待核实。[[../../literature/substructuring/translations/Hou1999-msfem-convergence-zh|Hou1999 译文]] §5.2 仍待翻译，范数、常数、尺度约定及由标量椭圆问题迁移到本页弹性离散的条件均待核验；不能据此宣称本页角点法普遍满足该界。
- **拓扑优化密度场**：本页未建立一般先验界。材料跳变与子结构边界交叉处可能出现较大迹误差，这是需数值验证的判断，不预设误差必然集中于这些位置；可用上述分解检查。

