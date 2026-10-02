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
date_update: 2026-09-15
---

# 外载荷：连续形式、适定性与有限元离散

外载荷处理包括确定物理载荷、构造离散载荷数据和施加到有限元方程三个步骤。本文按载荷类型、分布载荷离散、集中载荷处理与核验展开；正则性与适定性推导集中放在附录 A。


## 1. 外载荷的类型与连续表示

外载荷按作用位置区分：体力作用于区域，牵引作用于边界，线载荷作用于曲线，集中力作用于点。

体力、面牵引和线载荷均属于分布载荷，分别以单位体积、单位面积和单位长度上的力描述；集中力则以作用于一点的合力描述。

| <span style="display:inline-block; min-width:100px">类型</span> | <span style="display:inline-block; min-width:180px">数据及单位</span> | <span style="display:inline-block; min-width:300px">对试验位移的作用</span> |
|---|---|---|
| 体力 | $\boldsymbol b$，力/体积 | $\int_\Omega\boldsymbol b\cdot\boldsymbol v\,\mathrm dx$ |
| 面牵引 | $\boldsymbol g$，力/面积 | $\int_{\Gamma_N}\boldsymbol g\cdot\boldsymbol v\,\mathrm ds$ |
| 线载荷 | $\boldsymbol q$，力/长度 | $\int_\Lambda\boldsymbol q\cdot\boldsymbol v\,\mathrm ds$ |
| 集中力 | $\boldsymbol P$，力 | $\boldsymbol P\cdot\boldsymbol v(\boldsymbol x_0)$ |

注：表中单位按三维情形列示；二维边界牵引采用线力表示时，单位为力/长度。

## 2. 分布载荷的离散

给定体力函数 $\boldsymbol b$ 或边界牵引函数 $\boldsymbol g$ 后，需要将其转化为离散方程中的载荷向量或边界自由度条件。两类有限元的处理过程如下：

| 载荷 | 位移法 | 应力—位移混合法 |
|---|---|---|
| 体力 $\boldsymbol b$ | 单元积分 → 装配右端向量 | 单元积分 → 装配平衡方程右端向量 |
| 牵引 $\boldsymbol g$ | 边界积分 → 装配右端向量 | 构造离散法向迹 → 确定边界应力自由度 |

### 2.1 体力的离散

两种方法均将体力与各自离散位移空间的基函数相乘并积分。记 $\boldsymbol\psi_i$ 为相应的向量基函数，体力载荷分量为

$$
(f_b)_i=\int_\Omega\boldsymbol b\cdot\boldsymbol\psi_i\,\mathrm dx
=\sum_{K\in\mathcal T_h}\int_K\boldsymbol b\cdot\boldsymbol\psi_i\,\mathrm dx.
$$

实际计算时，在每个单元内对体力与局部基函数的乘积作数值积分，再按局部到全局的自由度映射累加。由此得到体力载荷向量，并按所采用平衡方程的符号约定放入右端。

两种方法的积分装配过程相同，但位移空间及基函数不同，因此向量的维数和分量通常不同。

### 2.2 边界牵引的离散

位移法将牵引与位移基函数在受载边界上相乘并积分：

$$
(f_g)_i=\int_{\Gamma_N}\boldsymbol g\cdot\boldsymbol\psi_i\,\mathrm ds
=\sum_{F\in\mathcal F_h^N}\int_F\boldsymbol g\cdot\boldsymbol\psi_i\,\mathrm ds,
$$

其中 $\mathcal F_h^N$ 为牵引边界上的网格面集合，二维时为边集合。逐面计算积分并装配后，得到牵引载荷向量 $\boldsymbol f_g$，与体力载荷向量一起进入位移方程右端。加载区仅覆盖某个面的部分区域时，积分应限制在实际加载区域内。

混合法则将牵引作为应力的边界条件施加。先由 $\boldsymbol g$ 构造应力空间可表示且满足边界相容条件的离散牵引 $\boldsymbol g_h$，再确定相应的边界应力自由度，使

$$
\boldsymbol\sigma_h\boldsymbol n=\boldsymbol g_h
\qquad\text{on }\Gamma_N.
$$

具体过程为：按应力元的自由度定义对牵引进行插值或投影，得到边界自由度的给定值；随后通过消元或提升，将这些已知量纳入离散方程。采用提升时，写成

$$
\boldsymbol\sigma_h=\boldsymbol\sigma_{0,h}+\boldsymbol\sigma_{g,h},
\qquad
\boldsymbol\sigma_{g,h}\boldsymbol n=\boldsymbol g_h,
\qquad
\boldsymbol\sigma_{0,h}\boldsymbol n=\boldsymbol0
\quad\text{on }\Gamma_N.
$$

将该分解代入离散方程后，把已知提升的贡献移至右端，求解齐次应力修正与位移。因此，牵引在位移法中通过边界积分形成载荷向量，在应力—位移混合法中通过给定法向迹确定边界应力自由度（混合法中非齐次牵引条件的提升处理与拓扑优化求导考量，见 [[huzhang/huzhang-mixed-fem#2.4 边界条件的对偶语义与牵引提升|牵引提升]]）。

**两法离散机制的数学差异与受控对齐**：
边界牵引在两类有限元中的离散机制存在本质差异：
- **位移法中为自然边界条件（弱施加）**：原始牵引 $\boldsymbol g$ 作为线性泛函作用于位移检验函数，不要求 $\boldsymbol g$ 属于多项式空间或在面上连续，通过数值求积直接吸收进载荷向量；
- **应力—位移混合法中为本质边界条件（强施加）**：离散应力法向迹 $(\boldsymbol\sigma_h\boldsymbol n)|_F$ 必须严格落在预设的迹多项式空间内，连续牵引 $\boldsymbol g$ 必须先经插值或投影转化为离散法向迹 $\boldsymbol g_h$。

除常数均布面力等天然属于应力法向迹空间的情形（此时强插值无截断、求积精确，两法吸收完全相同的连续载荷）外，当 $\boldsymbol g$ 为非线性分布或局部跳跃载荷时，两法直接离散吸收的载荷泛函在数学上并不等价，包含外生的载荷表征误差。独立工程求解时两法各自按标准流程离散；但在需要消除外生数据偏差的算法受控对比中，必须预先对齐载荷数据，可采用 §3.4 的连续 $P_1$ 迹空间 $L^2$ 投影构造两法公用的离散牵引。

## 3. 集中载荷的处理

集中载荷有两条处理路线：直接点力装配保留理想点力模型；有限宽度分布化将其替换为接触区上的分布牵引。

| 路线 | 处理顺序 | 适用范围 |
|---|---|---|
| 直接点力 | 集中力 → 形函数点值 → 节点力 | 位移法的固定网格离散 |
| 有限宽度载荷 | 集中力 → 分布牵引 → 可选的 $P_1$ 投影 → 有限元施加 | 位移法与应力—位移混合法的受控对比 |


### 3.1 位移法中的直接点力装配

集中力通过形函数在作用点处的值装配，无需对 Dirac 分布作高斯求积：

$$
\boldsymbol F_i=\boldsymbol P\,\phi_i(\boldsymbol x_0),
\qquad
\boldsymbol x_0=\boldsymbol x_{i_0}
\ \Longrightarrow\
\boldsymbol F_i=\boldsymbol P\,\delta_{i i_0},
$$

后一步用 Lagrange 基的插值性质 $\phi_i(\boldsymbol x_j)=\delta_{ij}$。作用点落在节点上时合力整份进入该节点；落在单元内部时按 $\phi_i(\boldsymbol x_0)$ 分配到该单元全部节点，单位分解保证 $\sum_i\boldsymbol F_i=\boldsymbol P$。两种情形装配层都无近似。



### 3.2 理想点力的连续空间限制

二维、三维线弹性中，理想点力通常不是标准 $H^1$ 位移空间上的有界载荷泛函。二维点力附近的应力具有 $r^{-1}$ 奇异性，相应能量对数发散。固定网格下能够求解，不意味着加载点位移、柔顺度或点邻域应力具有网格无关的极限；远离加载点的局部收敛应另行讨论。

Hellinger–Reissner 形式的连续位移空间为 $[L^2(\Omega)]^d$，不存在有界点值泛函，边界 Dirac 也不属于标准法向迹所需的 $H^{-1/2}$ 空间。离散分片多项式虽可在单元内取值，但界面上可能多值，不能据此直接建立标准混合形式中的一致点力施加方式。正则性判据见附录 A.2；应力约束中的影响见 [[density-topopt/stress-constrained-topopt#5. 应力奇异性]]。


### 3.3 有限宽度分布化

对长度为 $l$ 的二维边界接触区，将集中力改写为均布线牵引

$$
\bar{\boldsymbol t}_l(\boldsymbol x)=\frac{\boldsymbol P}{l}\,\chi_{\Gamma_{N,l}}(\boldsymbol x),
\qquad
\int_{\Gamma_{N,l}}\bar{\boldsymbol t}_l\,\mathrm ds=\boldsymbol P .
$$

$\bar{\boldsymbol t}_l\in[L_2(\Gamma_N)]^d$，消除了理想点力对标准能量空间的障碍。三维面载荷应以接触面积代替 $l$；分布化不保证接触区端点或几何角点处应力光滑。$l$ 是建模量而非数值参数：$l\to0$ 的极限正是 附录 A.2 的非适定问题，因此 $l$ 由物理接触条件确定后固定，不随网格加密变化。位移法与混合法作受控对比时必须使用同一个 $\bar{\boldsymbol t}_l$，否则两者吸收的载荷泛函不同，比较结果含外生偏差。

### 3.4 连续 $P_1$ 迹空间上的 $L^2$ 投影

这里投影的是分布化后的牵引，而非理想点力；该投影不保证非负性或严格保持原加载区的支集。

设 $W_h^1(\Gamma_N)$ 为 $\Gamma_N$ 上的连续分片一次迹空间。求 $\boldsymbol t_h\in[W_h^1]^d$ 使

$$
\int_{\Gamma_N}\boldsymbol t_h\cdot\boldsymbol w_h\,\mathrm ds
=
\int_{\Gamma_N}\bar{\boldsymbol t}_l\cdot\boldsymbol w_h\,\mathrm ds,
\qquad
\forall\,\boldsymbol w_h\in[W_h^1]^d .
$$

守恒性由检验函数取特殊元素直接得到：

| 取 $\boldsymbol w_h$ | 得到 | 结论 |
|---|---|---|
| 常向量 $\boldsymbol e_c\in[W_h^1]^d$ | $\int\boldsymbol t_h\cdot\boldsymbol e_c=\int\bar{\boldsymbol t}_l\cdot\boldsymbol e_c$ | 合力守恒 $\int_{\Gamma_N}\boldsymbol t_h\,\mathrm ds=\boldsymbol P$ |
| 坐标线性函数 $x_j\boldsymbol e_c\in[W_h^1]^d$ | $\int x_j\boldsymbol t_h\cdot\boldsymbol e_c=\int x_j\bar{\boldsymbol t}_l\cdot\boldsymbol e_c$ | 一阶力矩守恒 |

在按边界节点顺序编号的单条开折线上，质量矩阵 $M_{ij}=\int_{\Gamma_N}\phi_i\phi_j\,\mathrm ds$ 在一维迹网格上为三对角，阶数为单元数加一。右端 $\int\bar{\boldsymbol t}_l\cdot\phi_i$ 必须按载荷区与单元的解析重叠区间积分：$\bar{\boldsymbol t}_l$ 含指示函数，在跨越载荷区端点的单元上不连续，高斯求积对该单元不精确，会破坏上表两条守恒律。

### 3.5 两类有限元使用同一离散牵引

得到 $\boldsymbol t_h$ 后两套形式可统一施加：位移法按 $\int_{\Gamma_N}\boldsymbol t_h\cdot\boldsymbol v_h\,\mathrm ds$ 弱积分，混合法按 $(\boldsymbol\sigma_h\boldsymbol n)|_{\Gamma_N}=\boldsymbol t_h$ 强插值。两条路径的机制并不对称——一个积分、一个插值——因此「施加同一份连续数据」不足以保证得到同一个离散载荷泛函；使两者重合的是迹空间的包含关系。

记 $\Sigma_h$ 在边界面 $F\subset\Gamma_N$ 上的法向迹空间为 $T_h$。应力空间取 $H(\mathrm{div})$ 协调的 $k$ 次元时法向迹跨面连续且逐面为 $k$ 次多项式，即

$$
T_h=\bigl\{\,\boldsymbol q\in[C^0(\Gamma_N)]^d\ :\ \boldsymbol q|_F\in[P_k(F)]^d,\ \forall F\subset\Gamma_N\,\bigr\}.
$$

连续分片一次迹空间因此满足

$$
[W_h^1]^d\subseteq T_h,\qquad \forall\,k\ge 1,
$$

于是对 §3.4 得到的 $\boldsymbol t_h\in[W_h^1]^d$，强插值算子是**恒等映射**：$(\boldsymbol\sigma_h\boldsymbol n)|_{\Gamma_N}=\boldsymbol t_h$ 逐点精确成立，没有插值误差，§3.4 表中的合力与一阶力矩守恒原样传到离散层。位移法侧对分片一次被积函数采用足够精度的求积同样精确，两法这才落到同一个载荷泛函上。

反面同样要记住：未投影的 $\bar{\boldsymbol t}_l$ 含指示函数，在跨越载荷区端点的那条边内部间断，$\bar{\boldsymbol t}_l\notin T_h$。对它做强插值等于用 $T_h$ 中某个元素去替换真实数据，该边上的载荷被改写，两条守恒律随之破坏，离散合力偏离 $\boldsymbol P$——此时两法解的已不是同一个问题，不能用作方法对照。

需要区分两件事：两法使用同一离散牵引数据是可以保证的（上式），但离散解不必相同，那是两套离散格式自身的逼近性质。

## 4. 载荷离散的核验

核验应检查实际进入方程的数据，而不仅是输入参数。

| 核验项 | 检查内容 |
|---|---|
| 加载区域 | 实际加载边、接触宽度和作用位置是否符合物理模型；按边中心选择整边可能改变接触区 |
| 合力 | 位移法装配载荷的合力、应力—位移混合法插值后法向迹的积分是否与给定合力一致 |
| 合力矩 | 相对同一参考点，离散载荷力矩是否与给定载荷一致 |
| 分布一致性 | 方法对比是否采用同一牵引函数与加载区域；仅合力相同不足以确认 |
| 对称降维 | 半域的载荷份额与目标量恢复到全域的规则是否一致 |

接触区端点落在网格边内部时，应按真实重叠区间积分。整边选取后重新归一化可保持合力，但不一定保持载荷分布。线性求解残差只能检查代数方程求解精度，不能代替上述核验。载荷向接口的等效传递见 [[exact-substructural]]。

## 附录 A：载荷正则性与适定性

以下讨论标准线弹性能量空间，记 $\boldsymbol V_0=\{\boldsymbol v\in[H^1(\Omega)]^d:\boldsymbol v|_{\Gamma_D}=\boldsymbol0\}$，$a$ 为线弹性双线性型。附录给出正文所用正则性结论的依据。


### A.1 载荷泛函的有界性与纯 Neumann 相容性

载荷泛函

$$
\ell(\boldsymbol v)
=
\int_\Omega\boldsymbol b\cdot\boldsymbol v\,\mathrm dx
+
\langle\boldsymbol g,\gamma\boldsymbol v\rangle_{\Gamma_N}
$$

在 $\boldsymbol b\in[L_2(\Omega)]^d$、$\boldsymbol g\in[H^{-1/2}(\Gamma_N)]^d$ 时对 $\boldsymbol V_0$ 有界。此处只列 §1 四类中泛函有界的两类，线载荷与集中力写不进这两项，原因见附录 A.2。当 $\mathrm{meas}_{d-1}(\Gamma_D)>0$ 时 $a$ 由 Korn 不等式在 $\boldsymbol V_0$ 上强制，Lax–Milgram 给出唯一解。

$\Gamma_D=\emptyset$（纯 Neumann）时 $a$ 的核为刚体运动空间 $\mathrm{RM}$，$\dim\mathrm{RM}=3\ (d=2)$、$6\ (d=3)$。此时可解性要求载荷数据自平衡：

$$
\int_\Omega\boldsymbol b\,\mathrm dx+\int_{\Gamma_N}\boldsymbol g\,\mathrm ds=\boldsymbol 0,
\qquad
\int_\Omega\boldsymbol x\times\boldsymbol b\,\mathrm dx+\int_{\Gamma_N}\boldsymbol x\times\boldsymbol g\,\mathrm ds=\boldsymbol 0,
$$

其中 $d=2$ 时叉积退化为标量 $x_1b_2-x_2b_1$，对应 $\mathrm{RM}$ 中唯一的转动模式。两式合起来就是 $\ell(\boldsymbol v)=0,\ \forall\boldsymbol v\in\mathrm{RM}$；解在相差一个刚体运动的意义下唯一。这是载荷数据本身的约束，与离散无关；离散层的表现是刚度矩阵奇异，而不是右端项异常。

### A.2 低维支集与 Sobolev 正则性

点力能否进入某个空间的对偶，取决于 Dirac 测度落在哪一阶负指标 Sobolev 空间：

$$
\delta_{\boldsymbol x_0}\in H^{-s}(\mathbb R^n)
\iff
s>\frac n2 .
$$

（判据由 $\|\delta\|_{H^{-s}}^2=\int_{\mathbb R^n}(1+|\boldsymbol\xi|^2)^{-s}\,\mathrm d\boldsymbol\xi$ 是否收敛给出。）

| 场景 | $n$ | 需要的阶 | 实际可用的阶 | 结论 |
|---|---|---|---|---|
| 点力对位移空间 $[H^1(\Omega)]^d$ | $d=2$ | $s>1$ | $s=1$ | $\delta\notin H^{-1}$，泛函无界 |
| 点力对位移空间 $[H^1(\Omega)]^d$ | $d=3$ | $s>3/2$ | $s=1$ | $\delta\notin H^{-1}$，泛函无界 |
| 边界点力对法向迹空间 $H^{-1/2}(\Gamma_N)$ | $d-1=1$ | $s>1/2$ | $s=1/2$ | $\delta\notin H^{-1/2}$，临界失败 |
| 边界点力对法向迹空间 $H^{-1/2}(\Gamma_N)$ | $d-1=2$ | $s>1$ | $s=1/2$ | $\delta\notin H^{-1/2}$ |
| 一维杆 | $1$ | $s>1/2$ | $s=1$ | $\delta\in H^{-1}$，该表中满足能量空间要求的情形 |

因此 $d\ge2$ 时点力问题的连续解不在 $[H^1(\Omega)]^d$ 中：二维 Flamant/Kelvin 解 $\boldsymbol u\sim\log r$、$\boldsymbol\sigma\sim r^{-1}$，能量 $\int_0^R r^{-2}\cdot r\,\mathrm dr$ 对数发散；三维 Kelvin 解 $\boldsymbol u\sim r^{-1}$、$\boldsymbol\sigma\sim r^{-2}$，能量 $\int_0^R r^{-4}\cdot r^2\,\mathrm dr$ 发散。

线载荷的判据由迹定理给出：$H^s(\mathbb R^n)$ 到 $m$ 维子流形上的迹存在当且仅当 $s>(n-m)/2$。$m=0$ 退回上式，$m=n-1$ 给出面牵引所在的 $H^{-1/2}$，点力、线载荷与面牵引用的是同一条判据，只是 $m$ 不同。

| 场景 | $n$ / $m$ | 需要的阶 | 实际可用的阶 | 结论 |
|---|---|---|---|---|
| 三维棱上的线载荷 $\boldsymbol q$ | $3$ / $1$ | $s>1$ | $s=1$ | 泛函无界，与点力同类 |
| 二维内部曲线上的线载荷 | $2$ / $1$ | $s>1/2$ | $s=1$ | 泛函有界，连续问题适定 |

因此「低维支集」在连续层不是一个统一的坏情形：$m=0$（任意 $d\ge2$）与 $m=1,\ d=3$ 不适定，$m=1,\ d=2$ 适定。适定与否由余维数 $n-m$ 决定，与 $\ell(\phi_i)$ 用什么手段求值不是同一判据；后者不影响适定性，只是离散层的算法选择（§2、§3）。

## 参考依据

| 类型 | 来源 | 支撑内容 |
|---|---|---|
| 文献 | `Brezzi1991-mixedhybrid` | 混合变分形式与应力法向迹空间 |
| 标准结果 | Sobolev 迹定理、Dirac 正则性、Kelvin/Flamant 奇性、Korn 不等式 | 附录 A 的连续空间判据与相容条件；沿用原页依据 |
| 本页推导 | 投影中取常向量与线性试验函数 | 投影的合力、力矩守恒 |
| 实现资料 | `soptx:docs/fem/load-handling-implementation.md` | 载荷协议、点力与分布牵引装配路径、解析重叠积分；具体接口以程序文档为准 |
