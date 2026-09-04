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
date_update: 2026-09-03
---

# 外载荷：连续形式、适定性与有限元离散

外载荷按作用的几何实体分为体力、面牵引、线载荷、集中力四类（三维四类，二维三类），各类数据落在不同的对偶空间中；其正则性决定载荷泛函是否有界、问题是否适定，也决定它在位移型与应力—位移混合型两套变分形式中是作为右端泛函弱施加还是作为本质约束强施加，以及离散层可用的等效节点力与迹投影格式。

---

## 1. 载荷数据与正则性

记 $\partial\Omega=\Gamma_D\cup\Gamma_N$，$\Gamma_D\cap\Gamma_N=\emptyset$，位移检验空间 $\boldsymbol V_0=\{\boldsymbol v\in[H^1(\Omega)]^d:\boldsymbol v|_{\Gamma_D}=\boldsymbol 0\}$。

外载荷总是作用在某个几何实体上：整个区域、边界面、棱线、单个点。$d$ 维问题的实体维数只有 $m=0,1,\dots,d$ 这几档，与网格实体一一对应（单元、面、棱、节点），所以外载荷按作用实体的维数恰好分 $d+1$ 类——三维四类，二维三类。按余维 $d-m$ 排开：

| 余维 $d-m$ | 三维实体（载荷） | 二维实体（载荷） | 泛函在 $\boldsymbol V_0$ 上 |
|---|---|---|---|
| $0$ | 单元（体力） | 单元（体力） | 有界 |
| $1$ | 面（面牵引） | 边（边界牵引、内部曲线载荷） | 有界 |
| $2$ | 棱（线载荷） | 点（集中力） | 无界 |
| $3$ | 点（集中力） | —— | 无界 |

二维少的是余维 $3$ 那一档：集中力上移到余维 $2$，而三维余维 $2$ 上的线载荷在二维没有对应实体。因此「线载荷」在两个维数里不是同一个对象——三维指棱上的载荷，余维 $2$，泛函无界，与点力同类；二维指边界边或区域内部曲线上的载荷，余维 $1$，泛函有界，与面牵引同类（§3.1）。

载荷数据是该实体上的力密度（单位体积、单位面积、单位长度上的力），或在点上直接就是合力向量。它进入变分形式的方式统一为载荷与 $\boldsymbol v$ 在该实体上的配对，正则性和配对形式见下表。

初应力、热应变型的等效载荷不在此列：它不是作用在某个实体上的力，而是本构中的非弹性应变，等效节点力由 $\int_\Omega\boldsymbol\sigma_0:\boldsymbol\varepsilon(\boldsymbol v)\,\mathrm dx$ 给出，与 $\boldsymbol v$ 的梯度而不是 $\boldsymbol v$ 本身配对。

| 载荷 | 记号 | 支集维数 | 自然所属空间 | 在 $\boldsymbol V_0$ 上的配对 |
|---|---|---|---|---|
| 体力 | $\boldsymbol b$ | $d$ | $[L_2(\Omega)]^d$（更弱可取 $[H^{-1}(\Omega)]^d$） | $\int_\Omega\boldsymbol b\cdot\boldsymbol v\,\mathrm dx$ |
| 面牵引 | $\boldsymbol g$ | $d-1$ | $[H^{-1/2}(\Gamma_N)]^d$（工程上取 $[L_2(\Gamma_N)]^d$） | $\langle\boldsymbol g,\gamma\boldsymbol v\rangle_{H^{-1/2}\times H^{1/2}}$ |
| 线载荷（$d=3$ 棱上） | $\boldsymbol q$ | $1$ | $\Lambda$ 上的线密度，无 $H^{-1}$ 表示（§3.1） | 见 §3 |
| 集中力 | $\boldsymbol P$（作用于 $\boldsymbol x_0$） | $0$ | 点上的合力向量，无 $H^{-1}$ 表示（§3.1） | 见 §3 |

面牵引进入的合法性来自迹算子 $\gamma:[H^1(\Omega)]^d\to[H^{1/2}(\partial\Omega)]^d$ 有界且满射，因此 $H^{1/2}$ 的对偶 $H^{-1/2}$ 是 $\boldsymbol g$ 能被 $\boldsymbol V_0$ 吸收的最大空间。

## 2. 载荷泛函的有界性与纯 Neumann 相容性

载荷泛函

$$
\ell(\boldsymbol v)
=
\int_\Omega\boldsymbol b\cdot\boldsymbol v\,\mathrm dx
+
\langle\boldsymbol g,\gamma\boldsymbol v\rangle_{\Gamma_N}
$$

在 $\boldsymbol b\in[L_2(\Omega)]^d$、$\boldsymbol g\in[H^{-1/2}(\Gamma_N)]^d$ 时对 $\boldsymbol V_0$ 有界。此处只列 §1 四类中泛函有界的两类，线载荷与集中力写不进这两项，原因见 §3。当 $\mathrm{meas}_{d-1}(\Gamma_D)>0$ 时 $a$ 由 Korn 不等式在 $\boldsymbol V_0$ 上强制，Lax–Milgram 给出唯一解。

$\Gamma_D=\emptyset$（纯 Neumann）时 $a$ 的核为刚体运动空间 $\mathrm{RM}$，$\dim\mathrm{RM}=3\ (d=2)$、$6\ (d=3)$。此时可解性要求载荷数据自平衡：

$$
\int_\Omega\boldsymbol b\,\mathrm dx+\int_{\Gamma_N}\boldsymbol g\,\mathrm ds=\boldsymbol 0,
\qquad
\int_\Omega\boldsymbol x\times\boldsymbol b\,\mathrm dx+\int_{\Gamma_N}\boldsymbol x\times\boldsymbol g\,\mathrm ds=\boldsymbol 0,
$$

其中 $d=2$ 时叉积退化为标量 $x_1b_2-x_2b_1$，对应 $\mathrm{RM}$ 中唯一的转动模式。两式合起来就是 $\ell(\boldsymbol v)=0,\ \forall\boldsymbol v\in\mathrm{RM}$；解在相差一个刚体运动的意义下唯一。这是载荷数据本身的约束，与离散无关；离散层的表现是刚度矩阵奇异，而不是右端项异常。

## 3. 低维支集载荷的适定性

### 3.1 连续层：低维支集与 $H^{-1}$

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
| 一维杆 | $1$ | $s>1/2$ | $s=1$ | $\delta\in H^{-1}$，唯一适定的情形 |

因此 $d\ge2$ 时点力问题的连续解不在 $[H^1(\Omega)]^d$ 中：二维 Flamant/Kelvin 解 $\boldsymbol u\sim\log r$、$\boldsymbol\sigma\sim r^{-1}$，能量 $\int_0^R r^{-2}\cdot r\,\mathrm dr$ 对数发散；三维 Kelvin 解 $\boldsymbol u\sim r^{-1}$、$\boldsymbol\sigma\sim r^{-2}$，能量 $\int_0^R r^{-4}\cdot r^2\,\mathrm dr$ 发散。

线载荷的判据由迹定理给出：$H^s(\mathbb R^n)$ 到 $m$ 维子流形上的迹存在当且仅当 $s>(n-m)/2$。$m=0$ 退回上式，$m=n-1$ 给出面牵引所在的 $H^{-1/2}$，点力、线载荷与面牵引用的是同一条判据，只是 $m$ 不同。

| 场景 | $n$ / $m$ | 需要的阶 | 实际可用的阶 | 结论 |
|---|---|---|---|---|
| 三维棱上的线载荷 $\boldsymbol q$ | $3$ / $1$ | $s>1$ | $s=1$ | 泛函无界，与点力同类 |
| 二维内部曲线上的线载荷 | $2$ / $1$ | $s>1/2$ | $s=1$ | 泛函有界，连续问题适定 |

因此「低维支集」在连续层不是一个统一的坏情形：$m=0$（任意 $d\ge2$）与 $m=1,\ d=3$ 不适定，$m=1,\ d=2$ 适定。适定与否由余维数 $n-m$ 决定，与 $\ell(\phi_i)$ 用什么手段求值不是同一判据；后者不影响适定性，只是离散层的算法选择（§5）。

### 3.2 离散层：位移法为何仍可用

$\boldsymbol V_h\subset[C^0(\bar\Omega)]^d$ 且有限维，点值泛函 $\ell_h(\boldsymbol v_h)=\boldsymbol P\cdot\boldsymbol v_h(\boldsymbol x_0)$ 在 $\boldsymbol V_h$ 上有界，离散问题存在唯一解。代价与边界：

| 性质 | 结论 |
|---|---|
| 固定 $h$ 下的可解性 | 成立 |
| $h\to0$ 的全局收敛 | 不成立，$\|\boldsymbol u_h\|_{H^1}$ 无界增长（二维为 $O(\log(1/h))$），加载点位移无极限 |
| 远场收敛 | 在任意满足 $\boldsymbol x_0\notin\bar\omega$ 的子域 $\omega$ 上仍收敛 |
| 可用观测量 | 加载点位移、点邻域应力不能作为收敛性判据或优化目标 |

### 3.3 混合法：点值泛函不存在

Hellinger–Reissner 形式中位移检验空间为分片不连续的 $\boldsymbol V=[L_2(\Omega)]^d$，其对偶仍是 $L_2$，故 $\delta_{\boldsymbol x_0}\notin\boldsymbol V^*$；即便在离散层 $\boldsymbol V_h$ 也无逐点值可言。应力侧的 $H(\mathrm{div})$ 法向迹落在 $H^{-1/2}(\partial\Omega)$（`Brezzi1991-mixedhybrid`），由 §3.1 表格同样容不下点测度。因此点力在混合变分形式中既不能作为右端泛函，也不能赋给法向迹自由度。

### 3.4 特征尺度分布化

在物理特征尺度 $l$（接触宽度、垫板长度等）上把集中力改写为局部均布牵引

$$
\bar{\boldsymbol t}_l(\boldsymbol x)=\frac{\boldsymbol P}{l}\,\chi_{\Gamma_{N,l}}(\boldsymbol x),
\qquad
\int_{\Gamma_{N,l}}\bar{\boldsymbol t}_l\,\mathrm ds=\boldsymbol P .
$$

$\bar{\boldsymbol t}_l\in[L_2(\Gamma_N)]^d$，问题恢复适定。$l$ 是建模量而非数值参数：$l\to0$ 的极限正是 §3.1 的非适定问题，因此 $l$ 由物理接触条件确定后固定，不随网格加密变化。位移法与混合法作受控对比时必须使用同一个 $\bar{\boldsymbol t}_l$，否则两者吸收的载荷泛函不同，比较结果含外生偏差。

## 4. 两套变分形式中的地位

| 物理边界 | 物理方程 | 位移型（LFEM） | 应力—位移混合型（Hu–Zhang） |
|---|---|---|---|
| 位移边界 $\Gamma_D$ | $\boldsymbol u=\bar{\boldsymbol u}$ | 本质，强施加于位移自由度 | 自然，弱加进应力方程右端 |
| 牵引边界 $\Gamma_N$ | $\boldsymbol\sigma\boldsymbol n=\boldsymbol g$ | 自然，经边界积分进入 $\ell(\boldsymbol v)$ | 本质，强插值于应力法向迹自由度 |
| 体力 $\boldsymbol b$ | — | $\int_\Omega\boldsymbol b\cdot\boldsymbol v_h\,\mathrm dx$ | $\int_\Omega\boldsymbol b\cdot\boldsymbol v_h\,\mathrm dx$，两法一致 |

牵引在混合形式中不是泛函而是约束，这是「载荷泛函」不足以覆盖本页全部对象的原因，也是同一份载荷数据在两套形式中被要求不同正则性的根源。

非齐次本质边界在两套形式中都可用提升（lifting）处理：取满足非齐次条件的已知场 $\boldsymbol w_g$，令未知量为齐次部分与 $\boldsymbol w_g$ 之和，把已知项移至右端。位移法中 $\boldsymbol w_g$ 是满足 $\bar{\boldsymbol u}$ 的位移提升，混合法中是满足 $\boldsymbol\sigma_g\boldsymbol n=\boldsymbol g$ 的牵引提升。提升与代数消元在前向求解中等价；两者在设计变量依赖问题中的差异不属本页，由 [[huzhang/huzhang-mixed-fem#2.4 边界条件的对偶语义与牵引提升]] 维护。

## 5. 离散：从载荷数据到节点力

载荷泛函 $\ell$ 是 $\boldsymbol V'$ 中的有界线性泛函，右端向量是它在基函数上的值：

$$
\boldsymbol F_i=\ell(\phi_i).
$$

四类载荷只是把各自的 $\ell$ 代进去，没有第二个式子：

| 载荷 | $\ell(\boldsymbol v)$ | $\boldsymbol F_i=\ell(\phi_i)$ | 是否出现待近似的积分 |
|---|---|---|---|
| 体力 $\boldsymbol b$ | $\int_\Omega\boldsymbol b\cdot\boldsymbol v\,\mathrm dx$ | $\int_\Omega\boldsymbol b\,\phi_i\,\mathrm dx$ | 是，$d$ 维（§5.1.1） |
| 面牵引 $\boldsymbol g$ | $\int_{\Gamma_N}\boldsymbol g\cdot\boldsymbol v\,\mathrm ds$ | $\int_{\Gamma_N}\boldsymbol g\,\phi_i\,\mathrm ds$ | 是，$d-1$ 维（§5.1.1） |
| 线载荷 $\boldsymbol q$（$d=3$ 棱上） | $\int_\Lambda\boldsymbol q\cdot\boldsymbol v\,\mathrm ds$ | $\int_\Lambda\boldsymbol q\,\phi_i\,\mathrm ds$ | 一维积分，$\phi_i$ 在棱上是多项式，可精确算（§5.1.2） |
| 集中力 $\boldsymbol P$ | $\boldsymbol P\cdot\boldsymbol v(\boldsymbol x_0)$ | $\boldsymbol P\,\phi_i(\boldsymbol x_0)$ | 否，是一次函数求值（§5.1.2） |

末两行常被误当作「另一种离散方式」，其实只是代入后不含需要近似的积分。反过来，若把线载荷或集中力硬当成体力密度送进单元求积，求积点取不到它们的支集，求和恒得零——不是精度差，是载荷整个丢失。

$\ell$ 是否有界是另一回事，由 §3 判定：集中力在 $d\ge2$ 时 $\ell$ 在 $[H^1]^d$ 上无界（连续问题不适定），但在有限维 $\boldsymbol V_h$ 上有界，$\boldsymbol F_i$ 照样精确可算。

### 5.1 节点力的求值

$\ell(\phi_i)$ 是需要近似的积分时用求积展开（§5.1.1），是点值或被积函数为多项式的低维积分时直接算出（§5.1.2）。

#### 5.1.1 求积展开

面牵引的节点力是 $\ell$ 在 $\phi_i$ 上的值：

$$
\boldsymbol F_i=\int_{\Gamma_N}\boldsymbol g(\boldsymbol x)\,\phi_i(\boldsymbol x)\,\mathrm ds .
$$

积分按边界面 $F$ 与参考单元上的求积点展开：

$$
\boldsymbol F_i\approx\sum_F\sum_q w_q\,\bigl|J_F(\boldsymbol\xi_q)\bigr|\;\boldsymbol g(\boldsymbol x_q)\,\phi_i(\boldsymbol x_q),
\qquad
\boldsymbol x_q=\boldsymbol x_F(\boldsymbol\xi_q) .
$$

体力同式，$F$ 换成单元、$|J_F|$ 换成单元雅可比、$\mathrm ds$ 换成 $\mathrm dx$。被积函数为多项式且求积次数足够时该式取等号，$\boldsymbol g$ 在面内不连续时不然（§5.2.2）。

常数 $g$ 在长度 $h$ 的 $p$ 次 Lagrange 线单元上的分配，由参考单元 $[-1,1]$ 上的 $\int\hat\phi_i\,\mathrm d\xi\cdot h/2$ 给出：

| $p$ | 节点顺序 | 一致节点力 | 合力 |
|---|---|---|---|
| $1$ | 端、端 | $\tfrac{gh}{2},\ \tfrac{gh}{2}$ | $gh$ |
| $2$ | 端、中、端 | $\tfrac{gh}{6},\ \tfrac{4gh}{6},\ \tfrac{gh}{6}$ | $gh$ |
| $3$ | 端、内、内、端 | $\tfrac{gh}{8},\ \tfrac{3gh}{8},\ \tfrac{3gh}{8},\ \tfrac{gh}{8}$ | $gh$ |

由单位分解 $\sum_i\phi_i\equiv1$，任意次数下 $\sum_i\boldsymbol F_i=\int_{\Gamma_N}\boldsymbol g\,\mathrm ds$。该守恒律与所用次数无关：把 $p=2$ 网格的边界节点按 $p=1$ 规则均分，合力仍然守恒，分布却是错的，合力自检查不出这类错误。

#### 5.1.2 闭式求值

$\ell(\phi_i)$ 不含需要近似的积分时，$\boldsymbol F_i$ 直接算出。集中力最直接：

$$
\boldsymbol F_i=\boldsymbol P\,\phi_i(\boldsymbol x_0),
\qquad
\boldsymbol x_0=\boldsymbol x_{i_0}
\ \Longrightarrow\
\boldsymbol F_i=\boldsymbol P\,\delta_{i i_0},
$$

后一步用 Lagrange 基的插值性质 $\phi_i(\boldsymbol x_j)=\delta_{ij}$。作用点落在节点上时合力整份进入该节点；落在单元内部时按 $\phi_i(\boldsymbol x_0)$ 分配到该单元全部节点，单位分解保证 $\sum_i\boldsymbol F_i=\boldsymbol P$。两种情形装配层都无近似。

线载荷同理，把 $\int_\Lambda\boldsymbol q\,\phi_i\,\mathrm ds$ 化为 $\Lambda$ 与各单元交线上的一维积分闭式求值；$\boldsymbol q$ 为常向量且 $\Lambda$ 与单元棱重合时，结果就是 §5.1.1 表中的一维分配系数。

装配无近似不等于解精确：$\phi_i(\boldsymbol x_0)$ 是有限数，故点值泛函在有限维 $\boldsymbol V_h$ 上有界、$\boldsymbol F_i$ 精确，$h\to0$ 时不收敛的是解而不是这个装配式（§3.2）。混合法中位移检验空间为 $[L_2(\Omega)]^d$，无逐点值可言，本节两式都不存在（§3.3）。

因此集中力有两条处理路线，区别不在求值手段而在是否更换载荷数据：

| 路线 | 做法 | $\ell$ | 代价 |
|---|---|---|---|
| 直接离散 | 按本节求值 $\boldsymbol F_i=\boldsymbol P\,\phi_i(\boldsymbol x_0)$ | $\ell$ 仍是点值泛函 | 装配精确但连续问题不适定（§3.1），$h\to0$ 解不收敛（§3.2），混合法不可用（§3.3） |
| 先正则化 | 按特征尺度改写为 $\bar{\boldsymbol t}_l$，再走 §5.1.1 求积或 §5.2.2 迹投影 | $\ell$ 换成面积分 | 问题恢复适定、两套形式通用，代价是 $l$ 须由物理接触条件确定（§3.4） |

第二条路线改的是载荷数据本身而非算法：正则化之后载荷不再是集中力，走的是面牵引的通道。

### 5.2 离散载荷数据的构造

本节两步改的是载荷数据本身而不是求值算法：先由网格确定离散加载面 $\Gamma_{N,h}$，再决定载荷在其上的函数表示。两步完成后仍按 §5.1 求值。

#### 5.2.1 加载面的几何选取

程序常以「面重心是否满足边界判据」整面选取加载面，得到的离散加载面 $\Gamma_{N,h}$ 是若干整面之并。载荷区端点落在某个面内部时 $\Gamma_{N,h}\neq\Gamma_{N,l}$：

| 量 | 误差 |
|---|---|
| 加载面测度 | 单侧最多相差一个面尺度 $h_F$ |
| 施加合力 | $\bar t\,|\Gamma_{N,h}|$ 与 $\boldsymbol P$ 最多相差 $\bar t\,h_F$，相对误差 $O(h_F/l)$ |
| $l\lesssim h_F$ | 相对误差为 $O(1)$，且不随网格加密自动消失 |

该误差是静默的：方程仍可解、结果仍收敛，只是收敛到另一个问题。规避手段是按 §5.2.2 把载荷表示在迹空间中，或在装配后核对离散合力与 $\boldsymbol P$。

#### 5.2.2 连续 $P_1$ 迹空间上的 $L^2$ 投影

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
| 线性 $s\,\boldsymbol e_c\in[W_h^1]^d$ | $\int s\,\boldsymbol t_h\cdot\boldsymbol e_c=\int s\,\bar{\boldsymbol t}_l\cdot\boldsymbol e_c$ | 一阶力矩守恒 |

质量矩阵 $M_{ij}=\int_{\Gamma_N}\phi_i\phi_j\,\mathrm ds$ 在一维迹网格上为三对角，阶数为单元数加一。右端 $\int\bar{\boldsymbol t}_l\cdot\phi_i$ 必须按载荷区与单元的解析重叠区间积分：$\bar{\boldsymbol t}_l$ 含指示函数，在跨越载荷区端点的单元上不连续，高斯求积对该单元不精确，会破坏上表两条守恒律。

得到 $\boldsymbol t_h$ 后两套形式可统一施加：位移法按 $\int_{\Gamma_N}\boldsymbol t_h\cdot\boldsymbol v_h\,\mathrm ds$ 弱积分，混合法按 $(\boldsymbol\sigma_h\boldsymbol n)|_{\Gamma_N}=\boldsymbol t_h$ 强插值。$\boldsymbol t_h$ 已属于迹多项式空间，强插值无截断、弱积分可精确求积，两法吸收同一载荷泛函。

## 6. 参考文献

| 类型 | 条目 | 对应内容 |
|---|---|---|
| 文献 | `Brezzi1991-mixedhybrid` | $H(\mathrm{div})$ 张量的法向迹落在 $H^{-1/2}(\partial\Omega)$（§3.3） |
| 原始源 | `xtu-phd-thesis:thesis/brightPhD.pdf#第5.6.1节`、同上 5.6.3 节 | 集中力特征尺度分布化与受控对比设定（§3.4） |
| 标准结果 | 未指定单一出处，本页只作陈述与推论 | $\delta\in H^{-s}$ 的指标判据、Kelvin/Flamant 奇性阶、Korn 不等式与刚体核（§2、§3.1） |
| 本页自证 | 参考单元积分、检验函数取常向量与线性 | 一致节点力系数、$L^2$ 迹投影的两条守恒律（§5.1.1、§5.2.2） |
| 程序事实源 | `soptx:docs/fem/load-handling-implementation.md` | 载荷协议分层、四类载荷与三条求解路径的支持矩阵、`degree` 要求、点力投影模式、面重心整面选取与解析重叠积分实现 |
| 关联页面 | [[linear-elasticity]] | 连续弹性模型与位移型弱形式，本页的 $\ell(\boldsymbol v)$ 在该页 §4 定义 |
| 关联页面 | [[huzhang/huzhang-mixed-fem]] | Hellinger–Reissner 鞍点结构、牵引提升在设计相关问题中的作用、角点松弛与稳定化 |
| 关联页面 | [[huzhang/_index]] | 胡张元主题入口 |
| 关联页面 | [[finite-elements/_index]] | 单元级形函数、应变算子与 $\mathbf K_e$，与本页的右端项离散互补 |
| 关联页面 | [[substructural-condensation]] | 静力缩聚中载荷向接口自由度的投影约束 |
| 关联页面 | [[_index]] | 概念页总索引 |

本页不维护任何一次运行的数值结果、程序接口签名与配置键。
