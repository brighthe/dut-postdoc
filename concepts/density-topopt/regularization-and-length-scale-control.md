---
title: "正则化与长度尺度控制"
type: concept
aliases:
  - Regularization in Topology Optimization
  - Length Scale Control
  - Density Filter
  - Sensitivity Filter
  - Heaviside Projection
  - Three-Field Formulation
  - 密度过滤与投影
  - 密度过滤
  - 灵敏度过滤
  - Heaviside 投影
  - 三场表述
tags:
  - topology-optimization
  - density-method
  - regularization
  - filter
  - projection
status: "in-progress"
date_added: 2026-09-01
date_update: 2026-09-02
---

# 正则化与长度尺度控制

> 变密度拓扑优化为恢复问题良定性、抑制棋盘格与网格依赖、控制最小特征尺度而引入的显式正则化路线：灵敏度过滤只修正梯度场，密度过滤把设计变量经紧支卷积核映射为物理密度，Heaviside 型投影配合 $\beta$ 延拓再把过滤必然带来的灰度过渡带锐化为近 0/1 设计；三者共用同一个由 $r_{\min}$ 定义的长度尺度。

## 1. 为什么必须正则化

连续体拓扑优化本质上是在无限维函数空间中寻求最优材料分布 $\rho(\boldsymbol{x})$。由于缺乏必要的正则性约束，该问题在数学上通常不适定：最优化序列没有极限，随着网格细化，结构会衍生出无限精细的微观分支而不收敛于确定的宏观构型。在离散求解中，这一不适定性与低阶位移元的离散误差叠加，表现为四类数值病态，前三类互相独立：

1. **棋盘格（checkerboard）**：0/1 交替的单元图案。它是**离散误差的产物而非最优解**——低阶位移元对这种图案的数值刚度存在人为高估，高于任何等体积的均匀微结构，优化器因而把它误判为高效材料布局。未加过滤时棋盘格解的柔顺度值在对比中表面上最低，正是这种虚假刚度的体现。
2. **网格依赖（mesh dependence）**：细化网格得到的不是同一构型的更精确表达，而是杆件更多、更细的新构型。这是连续问题本身缺乏解的紧性的直接后果。
3. **无最小尺寸**：结果中出现任意细的构件，不可制造，且其力学响应落在离散精度之外。
4. **局部极值**：惩罚型材料插值与投影都使问题非凸，优化易停在初始猜测附近的局部解。它不由长度尺度直接治愈，但正则化路线里的延拓策略（第 4.2 节）就是为它设计的。

前三者共同的补救是**引入一个与网格无关的长度尺度**。基于卷积积分的过滤技术及其衍生的非线性投影，是目前处理该问题最主流的数值框架；即便采用惩罚型材料插值，若缺乏过滤、投影等正则化机制，离散求解中仍会伴随棋盘格、网格依赖与局部极值等典型数值问题。

## 2. 灵敏度过滤与密度过滤

两条路线共用同一个卷积核（第 3 节），实现代价接近，但作用对象与数学性质不同。

### 2.1 灵敏度过滤

灵敏度过滤由 Sigmund [1] 提出，本质是对目标泛函梯度场的卷积平滑：它**修正搜索方向而不改变设计变量本身**。在连续域 $\Omega$ 上，修正后的灵敏度场定义为原始灵敏度场在局部邻域内的密度加权平均：

$$
\widetilde{\frac{\delta\mathcal{J}}{\delta\rho}}(\boldsymbol{x})
= \frac{1}{\max\{\gamma,\rho(\boldsymbol{x})\}\,\psi(\boldsymbol{x})}
\int_{\Omega} w(\|\boldsymbol{y}-\boldsymbol{x}\|)\,\rho(\boldsymbol{y})\,
\frac{\delta\mathcal{J}}{\delta\rho}(\boldsymbol{y})\,\mathrm{d}\boldsymbol{y},
\qquad
\psi(\boldsymbol{x}) = \int_{\Omega} w(\|\boldsymbol{y}-\boldsymbol{x}\|)\,\mathrm{d}\boldsymbol{y},
$$

其中 $\gamma > 0$ 是防止低密度处分母奇异的极小正数，$\psi$ 是卷积核在设计域内的归一化因子。单元密度表征下的离散形式为

$$
\widetilde{\frac{\partial c}{\partial\rho_e}}
= \frac{1}{\max\{\gamma,\rho_e\}}\;
\frac{\sum_{s} H_{es}\, v_s\, \rho_s\, \dfrac{\partial c}{\partial\rho_s}}
{\sum_{s} H_{es}\, v_s},
$$

$H_{es}$、$v_s$ 的定义见第 3 节。被平滑的是灵敏度场的高频振荡，但设计变量场本身未被约束，故其正则化作用体现在优化更新方向的修正上，而非对设计空间的严格限制。

### 2.2 密度过滤

密度过滤由 Bruns 与 Tortorelli [2] 提出，Bourdin [3] 进一步证明在适当条件下它能保证拓扑优化问题解的存在性。核心思想是**解耦「数学设计空间」与「物理材料空间」**：原始设计变量 $\rho(\boldsymbol{x})$ 只是纯粹的优化参数，真正决定结构物理响应的是经平滑映射后的物理密度

$$
\tilde\rho(\boldsymbol{x}) = \frac{1}{\psi(\boldsymbol{x})}\int_{\Omega} w(\|\boldsymbol{y}-\boldsymbol{x}\|)\,\rho(\boldsymbol{y})\,\mathrm{d}\boldsymbol{y}.
$$

这是从 $L^\infty(\Omega)$ 到物理密度空间的线性平滑算子。目标泛函与约束泛函 $\mathcal{F}$ 均定义在 $\tilde\rho$ 上，其对 $\rho$ 的灵敏度由链式法则严格给出（第 5 节）。**约定**：仅采用密度过滤而未引入投影时，状态方程求解、性能泛函计算与最终设计结果均应以 $\tilde\rho$ 为准，而不是以 $\rho$ 为准。

### 2.3 两条路线的比较

| | 灵敏度过滤 [1] | 密度过滤 [2-3] |
|---|---|---|
| 作用对象 | 灵敏度 $\partial\Phi/\partial\rho_e$ | 设计变量本身，$\rho \mapsto \tilde\rho$ |
| 设计变量到物理密度的映射 | 恒等映射，$\boldsymbol\rho = \boldsymbol d$，正则化只作用于梯度 | 线性密度映射，$\boldsymbol\rho = f(\boldsymbol d)$，一个设计变量影响邻域内多个物理密度 |
| 优化问题 | 未改变；被求解的目标与被使用的梯度不一致 | 显式地在物理密度 $\tilde\rho$ 上定义 |
| 灵敏度 | 启发式加权，无严格变分来源 | 链式法则严格传递 |
| 收敛所得 | 不对应任何显式目标函数的稳定点 | 是被求解问题的稳定点；解的存在性有证明 |
| 同一 $r_{\min}$ 下的构型倾向 | 0/1 分布更锐利，边界灰度带窄 | 更保守，边界灰度带略宽；柔顺度与迭代步数普遍略增 |

最后一行是观测事实而非理论性质：在低阶位移元的二维 MBB 梁基准上，两种过滤都能让三种网格尺度下的主承载路径保持一致、杆件宽度稳定在由 $r_{\min}$ 决定的物理尺度附近，从而消除棋盘格与网格依赖；差别只在边界锐度与收敛效率的折中，这也是位移法基准算例中常以灵敏度过滤作为默认尺度控制手段的原因。

**一致性要求**：两者给出的构型往往视觉接近，但只有密度过滤给出**一致的优化问题**。当格式本身要求灵敏度与前向变分严格一致（例如混合变分格式下的解析灵敏度推导）时，必须取密度过滤——否则一致性在最外层一步被破坏。

## 3. 卷积核、过滤半径与离散实现

### 3.1 紧支卷积核与 $r_{\min}$

两类过滤共用具有紧支集的多项式衰减核

$$
w(r) = \max\{0,\; r_{\min} - r\}^{q}, \qquad q \ge 1,
$$

其中 $r = \|\boldsymbol{y}-\boldsymbol{x}\|_2$ 为两点欧氏距离，$r_{\min}$ 为过滤半径，$q$ 控制衰减速率：$q = 1$ 退化为常用的**线性锥形核**；$q > 1$ 时权重随距离衰减更快，邻域内远处点的影响被进一步削弱。核在半径外恒为零，故过滤只在局部邻域生效。

**尺寸含义**：一个纯 0/1 跃变经核过滤后展开为宽度约 $r_{\min}$ 的过渡带，故可分辨的最小构件尺度与 $r_{\min}$ 同量级。反过来说，**灰度过渡带是过滤的必然产物，不是收敛不良的症状**——它是换取良定性所付的代价，需要由第 4 节的投影单独偿还。$r_{\min}$ 应按设计域的绝对物理长度度量而不是按单元数度量，否则网格细化会连带改变被控制的特征尺度。

### 3.2 单元密度表征

设计变量与单元一一对应。记 $\boldsymbol{x}_e$ 为单元 $e$ 的几何中心，$\mathrm{dist}(e,s) = \|\boldsymbol{x}_e - \boldsymbol{x}_s\|$，离散卷积权重为连续核在单元中心的采样：

$$
H_{es} = w\big(\mathrm{dist}(e,s)\big) = \max\{0,\; r_{\min} - \mathrm{dist}(e,s)\}^{q},
\qquad
\tilde\rho_e = \frac{\sum_{s} H_{es}\, v_s\, \rho_s}{\sum_{s} H_{es}\, v_s},
$$

其中 $v_s$ 为单元测度，求和实际只跑过邻域索引集 $\mathcal{N}_e = \{s \mid H_{es} > 0\}$。$H_{es} = H_{se}$ 对称，这一点在第 5 节的转置回传中会用到。

### 3.3 节点密度表征

设计变量定义在网格顶点上，权重 $H_{ik} = \max\{0,\; r_{\min} - \mathrm{dist}(i,k)\}^{q}$ 按节点坐标计算。节点没有天然测度，需引入与节点关联的**控制体积** $v_i$，实现上采用集中质量近似：把各单元测度按其顶点数均分后累加到相应顶点。此后密度过滤形式与单元密度完全平行：

$$
\tilde\rho_i = \frac{\sum_{k} H_{ik}\, v_k\, \rho_k}{\sum_{k} H_{ik}\, v_k}.
$$

节点密度下的灵敏度过滤需额外用 $v_i / v_k$ 把「对节点变量的导数」换算成「单位体积的导数」再加权，形式上比单元密度版本多一组测度因子；密度过滤的链式法则则不需要这一换算。

### 3.4 三条性质

- **保界性**：权重非负且分母为权重之和，$\tilde\rho_e$ 是 $\{\rho_s\}$ 的凸组合，故 $\rho_s \in [\rho_{\min},1] \Rightarrow \tilde\rho_e \in [\rho_{\min},1]$，无需额外投影回可行盒。
- **体积加权的必要性**：$v_s$ 使非均匀网格上的加权保持几何一致；均匀网格上它退化为常数并被分母约去。
- **边界截断**：域边界处邻域被截断，分母按实际邻域求和仍保持凸组合，但边界处的等效过滤半径小于内部，边界构件因此略窄于内部构件。

## 4. Heaviside 投影与三场表述

### 4.1 从两场到三场

密度过滤的低通特性不可避免地在结构边界引入较宽的灰度带：既增加制造难度，也使有限元分析中的材料属性被低估或高估。Guest 等 [4] 与 Sigmund [5] 提出在密度过滤之后引入基于 Heaviside 函数的非线性投影，变量体系由此扩展为标准的**三场表述**：

$$
\rho(\boldsymbol{x}) \xrightarrow{\ \text{过滤算子}\ } \tilde\rho(\boldsymbol{x}) \xrightarrow{\ \text{投影算子}\ } \bar\rho(\boldsymbol{x}),
$$

$\rho$ 为原始设计变量，$\tilde\rho$ 为过滤后的中间场，$\bar\rho$ 为最终进入状态方程与性能评估的物理密度。引入投影后，$\tilde\rho$ 不再承担物理材料属性的角色。

理想的投影算子是阈值 $\eta \in (0,1)$ 处的阶跃 $\bar\rho = \mathcal{H}(\tilde\rho - \eta)$，但它在 $\eta$ 处不可微，无法用于基于伴随法与梯度的优化，因此实际计算采用光滑逼近。常用两类：

**（1）指数型投影** [4]（常被直接称为 Heaviside 投影）：

$$
\bar\rho = 1 - e^{-\beta\tilde\rho} + \tilde\rho\, e^{-\beta},
\qquad
\frac{\mathrm{d}\bar\rho}{\mathrm{d}\tilde\rho} = \beta e^{-\beta\tilde\rho} + e^{-\beta}.
$$

$\beta \to 0$ 时退化为近似线性关系，$\beta$ 增大时非线性增强并趋于 0/1。它不显式给出独立的阈值位置，可视为一类**单侧强化**的光滑投影，在部分微结构设计与特征尺度控制问题中有应用。

**（2）双曲正切型投影** [6]（常被称为阈值投影）：

$$
\bar\rho = \frac{\tanh(\beta\eta) + \tanh\big(\beta(\tilde\rho - \eta)\big)}{\tanh(\beta\eta) + \tanh\big(\beta(1-\eta)\big)},
\qquad
\frac{\mathrm{d}\bar\rho}{\mathrm{d}\tilde\rho}
= \beta\,\frac{1 - \tanh^{2}\big(\beta(\tilde\rho - \eta)\big)}{\tanh(\beta\eta) + \tanh\big(\beta(1-\eta)\big)}
= \frac{\beta\,\operatorname{sech}^{2}\big(\beta(\tilde\rho - \eta)\big)}{\tanh(\beta\eta) + \tanh\big(\beta(1-\eta)\big)} .
$$

- $\eta \in (0,1)$ 是阈值，控制灰度向黑白转换的分界位置，可独立调节；取 $\eta = 0.5$ 时映射关于中点近似对称，投影前后体积分数近似守恒；
- $\beta \to 0$ 时退化为恒等映射，$\beta \to \infty$ 时趋于 $\eta$ 处的阶跃函数；
- 映射单调且把 $[0,1]$ 映入 $[0,1]$，故 $\bar\rho$ 仍是合法密度，可直接送入材料插值。

由于对称性好且阈值可独立调节，tanh 型在实际拓扑优化中更为常用。

### 4.2 $\beta$ 延拓

直接从大 $\beta$ 起步，目标泛函表现出强非凸性：梯度在 $\tilde\rho \approx \eta$ 处极尖锐、在其余处几乎为零，优化器早熟收敛于初始猜测附近的局部解；$\beta$ 过小则投影作用弱，难以抑制灰度。因此采用**延拓（continuation）**：初期取较小的 $\beta$（如 $\beta = 1$），此时问题近似凸性较好、利于寻找全局轮廓，随迭代推进逐步增大 $\beta$ 以锐化边界。常见两种更新策略：

- **乘法式**：每若干步 $\beta \leftarrow 2\beta$，锐化快，适合约束弱耦合的问题；
- **加法式**：每若干步 $\beta \leftarrow \beta + \Delta\beta$，锐化缓，适合约束与密度强耦合、锐化会显著改变可行域的问题（局部应力约束属此类）。

**实现注意**：$\beta$ 每次更新都会突变目标与梯度的量级。序列凸近似类优化器（MMA 及其变体）通常需要在 $\beta$ 更新时重置渐近线与设计历史，否则前一 $\beta$ 下拟合的近似模型会在新 $\beta$ 下产生持续振荡。这一耦合是实现层面的，但去掉投影时会连带失去它，属于容易被忽略的副作用。

### 4.3 稳健三场形式

单场投影只锐化边界，不提供尺寸保证。Wang 等 [6] 在同一 $\tilde\rho$ 上取三个阈值 $\eta_{\mathrm{ero}} > \eta_{\mathrm{int}} > \eta_{\mathrm{dil}}$ 投影出腐蚀/中间/膨胀三个设计，对三者的最差响应做 min–max，以中间设计作为交付构型。它换来对制造公差（均匀过刻蚀或欠刻蚀）的稳健性和真正可控的最小尺寸：腐蚀设计仍连通即保证实体最小尺寸，膨胀设计仍有孔即保证孔洞最小尺寸。代价是每步三次前向求解与三倍灵敏度。腐蚀/膨胀的概念借自第 7 节表中的形态学黑白过滤。

## 5. 链式法则灵敏度

引入过滤与投影后，任意物理量 $\mathcal{F}$ 对原始设计变量的灵敏度按两层映射逐层回传。连续域上的变分形式为

$$
\frac{\delta\mathcal{F}}{\delta\rho(\boldsymbol{x})}
= \int_{\Omega} w(\|\boldsymbol{y}-\boldsymbol{x}\|)\,\frac{1}{\psi(\boldsymbol{y})}
\left(\frac{\delta\mathcal{F}}{\delta\bar\rho(\boldsymbol{y})}\cdot\frac{\mathrm{d}\bar\rho}{\mathrm{d}\tilde\rho}\Big|_{\boldsymbol{y}}\right)\mathrm{d}\boldsymbol{y},
$$

它利用了投影是**点对点的局部映射**（$\bar\rho(\boldsymbol{y})$ 只取决于 $\tilde\rho(\boldsymbol{y})$）而过滤是**全域积分映射**这一结构差异。单元密度表征下的离散形式为

$$
\frac{\partial\mathcal{F}}{\partial\rho_e}
= \sum_{j}\frac{\partial\mathcal{F}}{\partial\bar\rho_j}\,
\frac{\mathrm{d}\bar\rho_j}{\mathrm{d}\tilde\rho_j}\,
\frac{\partial\tilde\rho_j}{\partial\rho_e},
\qquad
\frac{\partial\tilde\rho_j}{\partial\rho_e} = \frac{H_{je}\, v_e}{\sum_{s} H_{js}\, v_s},
$$

利用 $H_{je} = H_{ej}$ 可整理为 $v_e \sum_j H_{ej}\,(\cdot)_j / \sum_s H_{js} v_s$ 的形式，即过滤矩阵的转置作用于投影调制后的物理灵敏度。节点密度表征下把 $e, j, s$ 换成节点索引、$v$ 换成控制体积即可，形式完全相同。去掉投影层（$\mathrm{d}\bar\rho/\mathrm{d}\tilde\rho \equiv 1$）即退化为纯密度过滤的链式法则。

结构上：过滤是**与设计无关的常量稀疏矩阵**（网格不变则只需组装一次，且其转置即为回传算子），投影是**对角缩放**。二者与物理求解完全解耦——物理侧只需提供 $\partial\mathcal{F}/\partial\bar\rho_j$，正则化链条不进入伴随方程。

**驱动力的空间分布**：反向传播时物理灵敏度先经投影导数做局部加权调制，再经卷积核空间平滑传播。投影导数在灰度区域大、在接近纯黑白区域小，因此「过滤 + 投影」把优化驱动力集中传递到结构边界附近，这是它比单纯过滤更有效推动几何边界演化、提升构型清晰度的机理。

## 6. 何时必须投影：与问题类型的耦合

同一条过滤—投影链条在不同问题里的必要性并不相同，判据是**问题本身是否自带把密度推向 $\{0,1\}$ 端点的驱动力**。

### 6.1 体积约束下的柔顺度最小化：黑白化有自发驱动力

体积约束在最优解处活跃，材料预算被固定；在预算固定的前提下，SIMP 类惩罚使中间密度"刚度代价高于体积收益"，于是灰度在力学上不划算，优化自发趋于近 0/1。此时**过滤已经足够**，投影只是可选的边界锐化手段。

### 6.2 以体积为目标的局部应力约束问题：驱动力不存在

此类问题目标函数就是体积，可行域由逐单元的局部应力约束定义，**没有任何机制把 $\bar\rho$ 推向端点**；与此同时，为压制应力集中处的数值噪声通常取较大的 $r_{\min}$，过滤每一步都在制造更宽的过渡带。缺少投影时，二者合力把设计推向弥散的灰度解。

更本质的原因在约束模型自身：消除应力奇异性所用的松弛约束**只在 $\bar\rho = 1$ 与 $\bar\rho \to 0$ 两个端点上与真实屈服条件一致**，中间密度处的阈值是人为插值，不对应任何真实材料的强度。因此在这类问题中，投影不是构型修饰，而是使约束模型与停机判据自洽的必要环节；只用密度过滤会停在应力约束不激活的灰度驻点上。松弛模型的具体形式、由此导出的停机判据陷阱与实测证据见 [[stress-constrained-topopt]]。

## 7. 并行的正则化路线：谱系定位

过滤—投影链条不是唯一的正则化方式。下列路线与它目标相同（恢复良定性、控制长度尺度或抑制灰度），本页只定位它们与卷积过滤的关系，不展开：

| 路线 | 机理 | 与卷积过滤的关系 |
|---|---|---|
| 周长约束 [7] | 对设计的总周长（或 $\rho$ 的全变差）加上界，直接限制构件数量与细碎程度 | 全局约束而非局部映射；周长上界难以先验选取，且不直接给出最小尺寸 |
| 斜率约束 [8] | 逐点限制 $\lvert\nabla\rho\rvert \le 1/r$，强制密度过渡带宽度不小于 $r$ | 局部但以大量点态约束实现，优化器负担重；密度过滤可视为把「过渡带宽度不小于 $r_{\min}$」由约束改写成映射 |
| 形态学黑白过滤 [5] | 以图像形态学的腐蚀/膨胀（open/close）算子替代线性核，直接产生近 0/1 结果 | 与线性过滤同属「作用于密度场的映射」，但算子非线性；稳健三场形式的腐蚀/膨胀设计即从这里借来的概念 |
| 体积守恒非线性密度过滤 [9] | 针对传统密度过滤不能保证中间单元过滤前后体积一致的问题，用 Heaviside 型非线性核实现体积守恒 | 把「过滤 + 投影」两步合成一步非线性映射，可得极稳定的纯 0/1 分布 |
| PDE（Helmholtz 型）过滤 [10] | 解 $-r^{2}\nabla^{2}\tilde\rho + \tilde\rho = \rho$ 得到过滤场，边界条件替代邻域搜索 | 与卷积过滤等价的隐式形式：核由 PDE 的 Green 函数给出；无需邻域索引与常量稀疏矩阵存储，适合并行与非结构网格 |

两条**不属于本页**、但常被误当作正则化替代品的路线，在此明确排除：

- **提高单元阶次或改用非协调元**：高阶位移元能削弱棋盘格的虚假刚度，但博士论文第三章 [11] 的无过滤对照表明，单纯提高位移插值阶次不能作为鲁棒的正则化手段替代物理过滤，在节点密度表征下还会诱发极低效的「准收敛」；一旦施加统一物理半径的显式正则化，它便主导拓扑演化，高阶元的差异退居其次。离散格式对棋盘格的影响归 [[../linear-elasticity]]。
- **显式几何描述**：MMC 等以组件几何参数为设计变量的路线不经过密度映射，其最小尺寸由组件参数的盒约束直接给出，归 [[../mmc/_index]]。

## 参考文献

[1] SIGMUND O. On the design of compliant mechanisms using topology optimization[J]. Mechanics of Structures and Machines, 1997, 25(4): 493-524.
[2] BRUNS T E, TORTORELLI D A. Topology optimization of non-linear elastic structures and compliant mechanisms[J]. Computer Methods in Applied Mechanics and Engineering, 2001, 190(26-27): 3443-3459.
[3] BOURDIN B. Filters in topology optimization[J]. International Journal for Numerical Methods in Engineering, 2001, 50(9): 2143-2158.
[4] GUEST J K, PRÉVOST J H, BELYTSCHKO T. Achieving minimum length scale in topology optimization using nodal design variables and projection functions[J]. International Journal for Numerical Methods in Engineering, 2004, 61(2): 238-254.
[5] SIGMUND O. Morphology-based black and white filters for topology optimization[J]. Structural and Multidisciplinary Optimization, 2007, 33(4-5): 401-424.
[6] WANG F, LAZAROV B S, SIGMUND O. On projection methods, convergence and robust formulations in topology optimization[J]. Structural and Multidisciplinary Optimization, 2011, 43(6): 767-784.
[7] HABER R B, JOG C S, BENDSØE M P. A new approach to variable-topology shape design using a constraint on perimeter[J]. Structural Optimization, 1996, 11(1): 1-12.
[8] PETERSSON J, SIGMUND O. Slope constrained topology optimization[J]. International Journal for Numerical Methods in Engineering, 1998, 41(8): 1417-1434.
[9] XU S, CAI Y, CHENG G. Volume preserving nonlinear density filter based on Heaviside functions[J]. Structural and Multidisciplinary Optimization, 2010, 41(4): 495-505.
[10] LAZAROV B S, SIGMUND O. Filters in topology optimization based on Helmholtz-type differential equations[J]. International Journal for Numerical Methods in Engineering, 2011, 86(6): 765-781.
[11] 何亮. 基于高阶有限元的变密度拓扑优化算法设计与实现[D]. 湘潭: 湘潭大学, 2026.
