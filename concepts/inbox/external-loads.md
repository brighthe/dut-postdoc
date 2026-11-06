---
title: "外载荷：连续形式、适定性与有限元离散"
type: concept
aliases:
  - External Loads
  - 外载荷与载荷泛函
  - 等效节点力
  - Consistent Nodal Load
tags:
  - external-load
  - finite-element
  - variational-form
  - well-posedness
status: in-progress
date_added: 2026-09-03
date_update: 2026-10-25
---

# 外载荷：连续形式、适定性与有限元离散

外载荷处理分为三个层次：确定连续载荷模型、构造离散表示、施加到有限元方程。集中力正则化属于第一层，P1 投影属于第二层，两者不能混同。

## 1. 外载荷的类型与连续表示

| 类型 | 数据及单位（三维） | 对试验位移的作用 |
|---|---|---|
| 体力 | $\boldsymbol b$，力/体积 | $\int_\Omega\boldsymbol b\cdot\boldsymbol v\,dx$ |
| 面牵引 | $\boldsymbol g$，力/面积 | $\int_{\Gamma_N}\boldsymbol g\cdot\boldsymbol v\,ds$ |
| 线载荷 | $\boldsymbol q$，力/长度 | $\int_\Lambda\boldsymbol q\cdot\boldsymbol v\,ds$ |
| 集中力 | $\boldsymbol P$，力 | $\boldsymbol P\cdot\boldsymbol v(\boldsymbol x_0)$ |

二维边界牵引采用线力表示时，单位为力/长度。表中作用须在相应函数空间上有定义：例如三维理想线载荷与点力通常不属于标准 $H^1$ 位移空间的有界载荷，二维曲线上的分布载荷则可由迹定理处理。

标准线弹性中，$\boldsymbol b\in[L^2(\Omega)]^d$、$\boldsymbol g\in[H^{-1/2}(\Gamma_N)]^d$ 给出有界载荷泛函；纯 Neumann 问题还要求总合力与总力矩为零，解只在相差刚体运动的意义下唯一。

## 2. 分布载荷的离散

### 2.1 体力的离散

位移法与应力—位移混合法都将体力与各自位移空间的基函数相乘积分：

$$
(f_b)_i=\sum_{K\in\mathcal T_h}\int_K\boldsymbol b\cdot\boldsymbol\psi_i\,dx.
$$

逐单元积分后按自由度映射装配。两法的位移空间不同，所得向量的维数、分量及方程符号约定不必相同。

### 2.2 边界牵引的离散

| 方法 | 牵引的角色 | 离散操作 |
|---|---|---|
| 位移法 | 自然边界条件 | $(f_g)_i=\int_{\Gamma_N}\boldsymbol g\cdot\boldsymbol\psi_i\,ds$，装配右端向量 |
| 应力—位移混合法 | 应力的本质边界条件 | 构造可表示的 $\boldsymbol g_h$，确定边界应力自由度，使 $\boldsymbol\sigma_h\boldsymbol n=\boldsymbol g_h$ |

位移法可直接积分原牵引；加载区只覆盖某条边的一部分时，应按真实作用区积分。混合法须按应力元自由度定义进行赋值，并通过消元或提升纳入方程；提升写为 $\boldsymbol\sigma_h=\boldsymbol\sigma_{0,h}+\boldsymbol\sigma_{g,h}$，其中 $\boldsymbol\sigma_{g,h}\boldsymbol n=\boldsymbol g_h$。混合变分依据沿用 `Brezzi1991-mixedhybrid`；具体推导见 [[huzhang/huzhang-mixed-fem#2.6 非齐次牵引提升与密度参数化|牵引提升]]。

受控对比时应对齐两法使用的牵引函数，并检查求积与迹再现条件。由于检验空间及施加方式不同，这不意味着两法具有同一个离散载荷泛函或相同离散解。

## 3. 集中载荷的处理

两条路线分别是保留理想点力并直接装配，或先将其正则化为分布载荷再施加。

### 3.1 直接点力装配

位移元按形函数点值分配集中力：

$$
\boldsymbol F_i=\phi_i(\boldsymbol x_0)\boldsymbol P.
$$

作用点位于节点时，力全部进入对应节点；否则按作用点处的形函数值分配。单位分解保证 $\sum_i\boldsymbol F_i=\boldsymbol P$。这是离散空间上对点力的直接求值，不消除连续问题的奇异性。

**标准混合模型的限制。** Hu–Zhang 元所离散的 Hellinger–Reissner 模型采用

$$
\boldsymbol\sigma\in H(\operatorname{div},\Omega;\mathbb S),
\qquad \boldsymbol u\in[L^2(\Omega)]^d.
$$

内部点力需要求取 $L^2$ 检验函数的点值，该点值不是有界泛函；边界点力则要求 $\boldsymbol\sigma\boldsymbol n=\boldsymbol P\delta_{\boldsymbol x_0}$，但标准法向迹属于 $H^{-1/2}$，二维、三维边界上的 Dirac 点测度不属于该空间。

这一结论来自 Sobolev 正则性判据 $\delta\in H^{-s}(\mathbb R^n)\iff s>n/2$，边界点力取 $n=d-1$。同样，二维、三维点力通常也不是标准 $H^1$ 位移空间上的有界载荷。固定网格上能求解，不保证加载点位移、柔顺度或局部应力具有有限的网格极限，见 [[density-topopt/stress-constrained-topopt#5. 应力奇异性]]。

因此，在上述标准框架内需要先正则化；若坚持理想点力，须另用奇异解分离或广义解等方法。这个连续空间障碍与共享顶点应力的离散约束是两回事。

### 3.2 正则化后施加

**连续正则化：用分布载荷替代点力。**

在二维直边上，用坐标 $s$ 表示位置，点力的作用为 $\ell(\boldsymbol v)=\boldsymbol P\cdot\boldsymbol v(s_0)$。选非负、紧支集的 $\rho\in L^2(\mathbb R)$，满足 $\int\rho\,d\xi=1$，构造

$$
\bar{\boldsymbol t}_l(s)=\frac{\boldsymbol P}{l}\rho\!\left(\frac{s-s_0}{l}\right),
\qquad
\int\bar{\boldsymbol t}_l\,ds=\boldsymbol P.
$$

合力守恒由变量代换直接得到，前提是支集完全落在加载边界内。若 $\rho$ 关于零对称，则 $\int(s-s_0)\bar{\boldsymbol t}_l\,ds=0$，直边上的合力矩也与原点力一致。截断分布后须重新核验合力与力矩。

取 $\rho=\mathbf1_{[-1/2,1/2]}$，得到宽 $l$ 的均布牵引：

$$
\bar{\boldsymbol t}_l(s)=\frac{\boldsymbol P}{l}\mathbf1_{[s_0-l/2,s_0+l/2]}(s),
\qquad
\ell_l(\boldsymbol v)=\boldsymbol P\cdot\frac1l\int_{s_0-l/2}^{s_0+l/2}\boldsymbol v(s)\,ds.
$$

即用接触区平均位移替代点值。由 Cauchy–Schwarz 不等式与迹定理，固定 $l>0$ 时

$$
|\ell_l(\boldsymbol v)|
\le C_{\mathrm{tr}}\frac{\|\boldsymbol P\|}{\sqrt l}\|\boldsymbol v\|_{H^1(\Omega)}.
$$

因此载荷泛函有界，且 $\bar{\boldsymbol t}_l\in L^2\subset H^{-1/2}$，可作为标准混合模型的牵引数据。区段端点仍可跳跃，正则化不等于应力处处光滑；三维均布面载荷以接触面积代替 $l$。

$$
\underbrace{\boldsymbol P\delta_{s_0}\longrightarrow\bar{\boldsymbol t}_l}_{\text{连续正则化，物理尺度 }l}
\quad\longrightarrow\quad
\underbrace{\boldsymbol t_h=\Pi_h\bar{\boldsymbol t}_l}_{\text{可选的离散投影，网格尺度 }h}.
$$

$l$ 由物理接触条件确定，网格加密时固定 $l$、令 $h\to0$。$l\to0$ 虽恢复分布意义下的点力，却不保证位移或能量有有限极限。后续 $L^2$ 投影的输入是正则化函数，不是 Dirac 测度。

**表示空间与构造方法。**

选定空间 $W_h$ 后，以 $\boldsymbol t_h=\sum_i\boldsymbol c_i\phi_i$ 表示牵引；$\boldsymbol c_i$ 是牵引系数，不是节点力。

| 表示空间 | 逐边函数 | 端点关系 |
|---|---|---|
| 不连续 $P_0$ | 常数 | 相邻边独立 |
| 不连续 $P_1$ | 一次函数 | 相邻边端点值独立 |
| 连续 $P_1$ | 一次函数 | 相邻边共享端点值 |
| 更高阶 $P_k$ | $k$ 次多项式 | 可连续或不连续 |

构造方法包括取值插值与 $L^2$ 投影：前者用指定位置的函数值确定系数，后者用积分正交条件确定系数。常见组合如下，并非互斥、完备的分类：

| 组合 | 性质 |
|---|---|
| 分片常值取样 | 取中点等代表值，一般不保持合力 |
| 分片常值平均 | 即不连续 $P_0$ 的 $L^2$ 投影，逐边保持合力，一般不保持一阶矩 |
| 分片多项式插值 | 一般不保证合力或力矩，跳点须规定取值 |
| 连续或不连续 $P_1$ 的 $L^2$ 投影 | 均可保持合力与一阶矩，区别在局部守恒及端点连续性 |

位移法也可直接对原牵引精确积分，不必显式构造 $\boldsymbol t_h$。边内跳跃不能由该边上的单个多项式精确表示；应对齐分段或接受数据近似。

**重点：$L^2$ 投影。**

投影使选定空间中的平方误差最小：

$$
\boldsymbol t_h=\underset{\boldsymbol z_h\in[W_h]^d}{\operatorname{argmin}}
\frac12\int_{\Gamma_N}\lvert\boldsymbol z_h-\bar{\boldsymbol t}_l\rvert^2\,ds.
$$

取一阶变分，得到

$$
\int_{\Gamma_N}(\boldsymbol t_h-\bar{\boldsymbol t}_l)\cdot\boldsymbol w_h\,ds=0
\quad\forall\boldsymbol w_h\in[W_h]^d.
$$

展开基函数后，每个分量 $c$ 满足

$$
M\mathbf c^{(c)}=\mathbf b^{(c)},\qquad
M_{ij}=\int_{\Gamma_N}\phi_i\phi_j\,ds,\qquad
b_i^{(c)}=\int_{\Gamma_N}\bar t_{l,c}\phi_i\,ds.
$$

基函数线性无关时 $M$ 对称正定。非连续空间可逐边求解，连续空间因共享节点而耦合。取常向量为检验函数得到合力守恒；若空间还包含坐标线性函数，则取 $x_j\boldsymbol e_c$ 得到一阶矩守恒。这些结论均由上述正交条件推导。

连续 P1 保持整条投影边界的合力与一阶矩，不连续 P1 则可逐边保持。投影不保证保持符号或原支集；右端须按载荷区与网格边的真实重叠区间精确积分，不能对跨跳点的整边直接使用未分段求积并假定守恒。

**Hu–Zhang 迹空间与连续 P1 的选择。**

载荷投影后，还须检查

$$
\boldsymbol t_h\in T_h,
\qquad T_h=\{(\boldsymbol\sigma_h\boldsymbol n)|_{\Gamma_N}:\boldsymbol\sigma_h\in\Sigma_h\}.
$$

两种约束必须区分：

- $H(\operatorname{div})$ 协调性要求内部公共边两侧采用同一法向时的法向迹匹配，不要求沿外边界经过顶点时牵引连续。
- 若具体 Hu–Zhang 空间在顶点共享应力矩阵 $S_z$，相邻边端点牵引须满足 $\boldsymbol g_i(z)=S_z\boldsymbol n_i$。同一直边上两侧法向相同，故牵引相等；几何角点则满足 $\boldsymbol n_2^T\boldsymbol g_1=\boldsymbol n_1^T\boldsymbol g_2$，不要求向量相等。

后者是离散空间的额外约束，依据见 [[huzhang/vertex-continuity-relaxation]]。角点松弛不代表所有直边顶点都允许跳跃，须检查具体自由度共享方式。连续 P1 只避免直边端点跳跃，不自动保证 $\boldsymbol t_h\in T_h$；还需核验阶次、几何角点和其他边界条件。

**半梁例子。** 完整梁合力 $P=-3\,\mathrm N$，接触宽度 $l=1\,\mathrm{mm}$。左半域加载区为 $[79.5,80]\,\mathrm{mm}$，强度 $A=P/l=-3\,\mathrm{N/mm}$，合力 $P/2=-1.5\,\mathrm N$。当 $h=1\,\mathrm{mm}$ 时：

| 投影 | 结果与取舍 |
|---|---|
| 不连续 P0 | 在 $[79,80]$ 上取 $A/2$，保持合力，但作用位置由 $79.75$ 移至 $79.5$ |
| 不连续 P1 | 在末边得到 $t_h=A(-1/4+3\xi/2)$，$\xi=(x-79\,\mathrm{mm})/(1\,\mathrm{mm})$；保持合力与一阶矩，但 $x=79$ 处右侧值为 $-A/4$，左邻边为零 |
| 连续 P1 | 在整条底边 $[0,80]$ 上保持合力与一阶矩，并使相邻边端点值一致；可能产生变号尾部和支集扩展 |

以上投影结果由正交条件直接推导。若相关直边顶点仍共享应力，连续 P1 可同时满足守恒与端点一致的需要；不能把这个选择归因于 $H(\operatorname{div})$ 本身。若具体迹空间容许所需跳跃，不连续 P1 也可采用，其 $L^2$ 最佳近似误差不大于连续 P1。投影分段须与有限元边界网格匹配，最终施加后仍须核验。

算例参数依据：`soptx:src/soptx/problems/benchmarks/fixed_fixed.py`，commit `c0b5a69f3af9bddcd571e62822d8732b579a256c`；实现细节见 `soptx:docs/fem/load-handling-implementation.md`。

## 4. 载荷离散的核验

核验实际进入方程的数据，不能只检查输入参数或求解残差。

| 层次 | 检查内容 |
|---|---|
| 连续模型 | 实际加载区、宽度、位置、合力与力矩；半域与完整结构的换算 |
| 载荷投影 | 投影函数的合力、一阶矩、变号及支集变化；投影网格是否匹配 |
| 位移元装配 | 检查施加位移约束前的外载荷向量，区分体力与牵引，并核对自由度排序 |
| 混合元施加 | 积分实际应力法向迹，检查合力、力矩与逐边分布；不能对混合系统右端直接求和替代 |

合力一致不代表分布一致，投影守恒也不保证最终施加正确。约束消元后的右端不宜直接当作物理外载荷；数学上的精确守恒在浮点计算中应按容差判断。载荷向接口的等效传递见 [[substructure/exact-substructural]]。
