---
title: "基于超采样基函数与重叠协调的子结构分析"
type: concept
aliases:
  - oversampling-substructural
  - 超采样子结构分析
  - Oversampling Substructure Analysis
  - 重叠子结构分析
  - Overlapping Finite Element Substructure
tags:
  - finite-element
  - substructure
  - oversampling
  - overlapping-fem
  - partition-of-unity
status: draft
date_added: 2026-10-26
date_update: 2026-11-06
---

# 基于超采样基函数与重叠协调的子结构分析

子结构只保留角点自由度时，常规做法是假定边界位移由角点线性插值得到，再在目标子结构上做静力缩聚。超采样（oversampling）改变局部基函数的来源：在包住目标子结构的扩展域上求解局部边值问题，把人为的线性边界条件推到扩展域外边界，再将解限制回目标子结构，使目标边界上的位移由材料分布与局部响应决定。代价是各子结构基函数独立构造，共享边上位移不再连续；重叠有限元（overlapping finite element, OFEM）用单位分解权函数把相邻子结构的局部位移加权成唯一的全局位移场，恢复协调性。本页只写这两步的力学构造与它们同精确子结构族的关系；用神经网络替代局部求解的部分见 [[../piml/piml-substructural|PIML 子结构分析]]。

本页限于二维小应变线弹性静力、规则正方形子结构、细网格匹配、内部无载荷、位移约束位于子结构边界。扩展到三维在原理上直接，但本库来源只给出二维构造，三维细节标“待确认”。

## 1. 角点迹假定与边界层误差

[[exact-substructural|精确子结构族]]在目标子结构 $\Omega^j$ 上做精确缩聚，再用迹基 $\boldsymbol\Psi^j$ 限制边界位移空间。角点方案取 $\boldsymbol\Psi^j=\mathbf L$，边界位移沿每条边由两端角点线性插值，二维每块只剩 $n_c=8$ 个自由度。此时局部基函数

$$
\tilde{\mathbf N}^j=\mathbf N^j\mathbf L,
\qquad
\tilde{\mathbf K}_s^j=(\tilde{\mathbf N}^j)^{\mathsf T}\mathbf K^j\tilde{\mathbf N}^j
$$

的内部由局部平衡决定，边界却被迫取线性形状。材料非均匀时真实边界位移并非线性，边界附近形成一层形函数受人为边界条件支配的区域，产生边界层误差（boundary layer error）；按 [[exact-substructural-lagrange#4.2 Ritz 最佳逼近与柔度|Lagrange §4.2]] 的 Ritz 结论，受限空间高估刚度、低估柔度。子结构越大、边界附近孔洞与集中载荷越多，这一误差越明显。

消除边界层误差有两条路。一条是提高边界插值次数，扩大迹空间，代价是缩聚系统自由度增加、稀疏度下降，见 [[exact-substructural-lagrange|Lagrange 页]]与 [[exact-substructural-bernstein|Bernstein 页]]。另一条是本页的超采样：保持 8 个角点自由度不变，改变基函数的构造方式。

## 2. 超采样基函数

### 2.1 扩展域上的局部问题

对目标子结构 $\Omega_{\mathrm{sub}}^j$（$m\times m$ 个细单元）取同心的扩展域 $\Omega_{\mathrm{os}}^j\supset\Omega_{\mathrm{sub}}^j$，每侧向外多出 $l$ 层细单元，共 $(m+2l)\times(m+2l)$ 个单元、$2(m+2l+1)^2$ 个位移自由度。记扩展域四个角点为 $1',\dots,4'$。

对扩展域角点 $j'$ 的 $x$ 方向自由度，令其为 1、其余 7 个扩展域角点自由度为 0，沿扩展域外边界每条边由两端角点线性插值得到 Dirichlet 边界条件，在 $\Omega_{\mathrm{os}}^j$ 上求解弹性问题，得位移向量 $\boldsymbol\psi_x^{j'}\in\mathbb R^{2(m+2l+1)^2}$；$y$ 方向同理得 $\boldsymbol\psi_y^{j'}$。8 个局部问题共用同一刚度矩阵，只需一次分解、8 个右端项。

线性插值假定仍然存在，但只作用于 $\partial\Omega_{\mathrm{os}}^j$。把 $\boldsymbol\psi$ 限制到 $\Omega_{\mathrm{sub}}^j$ 的节点，得 $\boldsymbol\varphi_x^{j'},\boldsymbol\varphi_y^{j'}\in\mathbb R^{2(m+1)^2}$，按列排成

$$
\boldsymbol\Phi=\left[\boldsymbol\varphi_x^{1'}\ \boldsymbol\varphi_y^{1'}\ \cdots\ \boldsymbol\varphi_x^{4'}\ \boldsymbol\varphi_y^{4'}\right]\in\mathbb R^{n_s\times 8},
\qquad n_s=2(m+1)^2 .
$$

$\boldsymbol\Phi$ 的 8 列张成目标子结构上的一个 8 维位移空间，目标边界 $\partial\Omega_{\mathrm{sub}}^j$ 上的位移由扩展域内的材料分布与局部响应诱导，可以振荡，不再是线性。

### 2.2 限制与角点归一化

$\boldsymbol\Phi$ 的列对应扩展域角点，不对应目标子结构角点，不满足 Kronecker-$\delta$ 性质。记 $\mathcal M$ 为提取目标子结构 8 个角点自由度所在行的限制算子，$\mathbf T=\mathcal M(\boldsymbol\Phi)\in\mathbb R^{8\times8}$。取列组合 $\tilde{\boldsymbol\Phi}=\boldsymbol\Phi\mathbf C$ 使 $\mathcal M(\tilde{\boldsymbol\Phi})=\mathbf T\mathbf C=\mathbf I_8$，得

$$
\tilde{\boldsymbol\Phi}^j=\boldsymbol\Phi\,\mathbf T^{-1}\in\mathbb R^{n_s\times n_c},
\qquad
\mathbf u^j=\tilde{\boldsymbol\Phi}^j\mathbf u_c^j .
$$

$\tilde{\boldsymbol\Phi}^j$ 与精确族的 $\tilde{\mathbf N}^j$ 作用相同：把角点位移映射为子结构全部节点位移。换基不改变 $\operatorname{range}(\boldsymbol\Phi)$，只改变坐标。归一化要求 $\mathbf T$ 非奇异；来源指出对有效材料分布与合适的 $l$ 该矩阵数值可逆，病态时需正则化、剔除样本或改用局部精确求解。

### 2.3 刚体模态与结构外边界

扩展域外边界条件是角点值的线性插值，而二维刚体平移与小转动都是线性位移场，故对任一刚体模态，8 个局部问题的线性组合在 $\Omega_{\mathrm{os}}^j$ 上给出精确的刚体解，限制到 $\Omega_{\mathrm{sub}}^j$ 后仍是刚体解。因此精确构造的 $\operatorname{range}(\tilde{\boldsymbol\Phi}^j)$ 自动包含 3 个刚体模态，$\mathbf K_r^j$ 对刚体位移无虚假应变能。这一点是本页由边界条件形式推出的；来源在 U-Net 输出后另做“刚体模态补全”，那是预测值不自动满足该性质时的修正，属 PIML 一侧。

靠近结构边界 $\partial\Omega$ 的子结构，其扩展层会伸出结构之外，需要给伸出部分指定虚拟材料。来源采用分类延拓：伸出自由边（无 Dirichlet 约束）的部分取与弱材料相同的模量；伸出固定边（有 Dirichlet 约束）的部分按边界镜像取真实材料。延拓只用于构造该子结构的基函数，不改变 $\Omega$ 内的材料，也不替代全局边界条件。

### 2.4 局部降阶刚度

子结构的应变能在 $\operatorname{range}(\tilde{\boldsymbol\Phi}^j)$ 上的限制给出

$$
W^j=\tfrac12(\mathbf u_c^j)^{\mathsf T}\mathbf K_r^j\mathbf u_c^j,
\qquad
\mathbf K_r^j=(\tilde{\boldsymbol\Phi}^j)^{\mathsf T}\mathbf K^j\tilde{\boldsymbol\Phi}^j\in\mathbb R^{8\times8},
$$

形式与精确族的 $\tilde{\mathbf K}_s^j=(\tilde{\mathbf N}^j)^{\mathsf T}\mathbf K^j\tilde{\mathbf N}^j$ 完全相同，是局部刚度在 8 维子空间上的能量投影。区别只在子空间：精确族的子空间形如“给定迹 + 局部平衡内部”，这里的子空间由扩展域问题限制而来，目标子结构内部一般不满足以目标边界为边界条件的局部平衡。

## 3. 独立基函数的接口不协调

精确族中相邻子结构共享边界节点，边界位移取自同一组接口未知量，拼装后天然连续。超采样基函数由各子结构自己的扩展域决定，相邻子结构 $j_1,j_2$ 的 $\tilde{\boldsymbol\Phi}^{j_1},\tilde{\boldsymbol\Phi}^{j_2}$ 只在共享角点处因 Kronecker-$\delta$ 性质一致，共享边上非角点位置两侧恢复的位移一般不相等：

$$
\mathbf u_{j_1}(\boldsymbol x)\ne\mathbf u_{j_2}(\boldsymbol x),
\qquad
\boldsymbol x\in(\partial\Omega_{\mathrm{sub}}^{j_1}\cap\partial\Omega_{\mathrm{sub}}^{j_2})\setminus\{\text{共享角点}\}.
$$

直接按 $\tilde{\boldsymbol\Phi}_{\mathrm{global}}=\bigvee_j\tilde{\boldsymbol\Phi}^j$ 拼装得到的全局位移场在共享边上有跳跃。位移本身的误差可能不大，但应变、应变能和拓扑优化灵敏度依赖位移导数，对界面跳跃敏感。多尺度有限元文献中的超采样接受这种非协调并单独论证收敛（来源不在本库，待确认）；本页所述路线不接受非协调，用重叠单位分解把协调性找回来。两类接口的示意见 [[substructure-partition-and-cover#2.1 公共区域与局部位移表示|子结构划分与覆盖 §2.1]]；重叠覆盖与超采样扩展域的区别见 [[substructure-partition-and-cover#3. 重叠覆盖与超采样扩展域|该页 §3]]。

## 4. 单位分解重叠协调

### 4.1 可拼成均匀细网格的重叠覆盖

重叠有限元要求相邻子结构的覆盖区域有公共部分。若均匀 $h\times h$ 网格的子结构直接以非整数倍单元宽度重叠，重叠带会被切成 $(h/2)\times h$ 之类的人为小单元，单元类型增多、组装规则复杂化；重叠宽度取整单元又会使后文权函数的分母在局部为零。来源的做法是先在子结构内部改用非均匀网格：与邻块共享的边上，最外层单元在垂直于重叠带的方向由 $h$ 拉长为 $2h$，两条重叠边交汇处的角单元为 $2h\times2h$。相邻子结构再以宽度 $h$ 重叠，重叠后的区域重新拼成全局均匀的 $h\times h$ 笛卡尔网格。

![[overlapping-substructure-coverage.svg]]

图 ① 为一个内部型子结构的非均匀网格，图 ② 为两块以宽 $h$ 重叠后边缘单元交错、重叠带及两侧半区各为 $h$ 宽，图 ③ 为 $2\times2$ 块重叠后按覆盖块数着色的均匀细网格与 9 类子结构的位置。

子结构是否在某条边上扩展取决于该边有无邻块。矩形排列 $n_{slx}\times n_{sly}$ 中按位置分为 9 类子结构（4 个角、4 条边、1 个内部）；重叠后的细单元按被几个子结构覆盖及相对位置分为 16 类，被 1、2、4 个子结构覆盖的单元局部刚度块分别为 $8\times8$、$16\times16$、$32\times32$。

### 4.2 权函数与协调刚度

记 $\Omega_l$ 为第 $l$ 个局部单元的覆盖区域，$\mathbf u_l(\boldsymbol x)=\mathbf H_l(\boldsymbol x)\mathbf q_l$ 为其上的等参插值。权函数 $w_l$ 需在分析域上连续非负、在 $\Omega_l$ 外为零、处处求和为 1。来源用节点标记构造：

$$
P_l(\boldsymbol x)=\sum_r h_r^l(\boldsymbol x)\,p_r^l,
\qquad
w_l(\boldsymbol x)=\frac{P_l(\boldsymbol x)}{\sum_l P_l(\boldsymbol x)},
$$

其中 $h_r^l$ 为 Q4 形函数，节点位于本单元与其他单元覆盖区域交界上时 $p_r^l=0$，否则 $p_r^l=1$（含结构外边界上的节点）。只要每点至少被一个 $P_l>0$ 的单元覆盖，分母非零。全局位移与应变为

$$
\mathbf u_{\mathrm{global}}(\boldsymbol x)=\sum_l w_l(\boldsymbol x)\mathbf H_l(\boldsymbol x)\mathbf q_l,
\qquad
\mathbf B_l=\partial\!\left(w_l\mathbf H_l\right),
$$

刚度耦合项 $\mathbf K_{\mathrm{global}}(\alpha,\beta)=\int_{\Omega_\alpha\cap\Omega_\beta}\mathbf B_\alpha^{\mathsf T}\mathbf C\mathbf B_\beta\,\mathrm d\Omega$ 只在重叠区域非零。若每个局部插值在其覆盖区域内协调并能重现线性场，加权后的全局插值保持协调与线性完备，可通过分片检验。

积分最终都落在均匀 $h\times h$ 网格上，所有细单元在参考坐标下全等，雅可比为 $(h/2)\mathbf I$。因此 16 类单元各自的被积函数在参考坐标下是固定多项式、与材料无关，可对每类离线计算单位模量刚度 $\mathbf K_0^t$（$3\times3$ Gauss 积分），在线只做 $\mathbf K_e=E_e\mathbf K_0^t$ 的缩放与按预设索引的稀疏组装。重叠协调不改变在线组装的渐近复杂度。

### 4.3 与超采样映射的耦合

超采样决定每个子结构内部如何由角点自由度恢复细尺度位移，重叠单位分解决定不同子结构的局部位移如何合成唯一的全局场；两者作用于不同层次。耦合方式是让局部单元自由度 $\mathbf q_l$ 不再直接参与全局求解，而由所属子结构的超采样映射给出：

$$
\mathbf u_{\mathrm{global}}(\boldsymbol x)=\sum_l w_l(\boldsymbol x)\mathbf H_l(\boldsymbol x)\mathbf q_l,
\qquad
\mathbf q_l=R_l\!\left(\tilde{\boldsymbol\Phi}^j\mathbf u_c^j\right),
$$

$R_l$ 为从子结构节点位移提取单元自由度的限制算子。记重叠有限元组装的全局细尺度刚度为 $\mathbf K_{\mathrm{global}}^{\mathrm{OV}}$，则角点自由度上的降阶系统为 Galerkin 投影

$$
\mathbf K_{\mathrm{global}}^{\mathrm{c,OV}}=\tilde{\boldsymbol\Phi}_{\mathrm{global}}^{\mathsf T}\,\mathbf K_{\mathrm{global}}^{\mathrm{OV}}\,\tilde{\boldsymbol\Phi}_{\mathrm{global}},
\qquad
\mathbf K_{\mathrm{global}}^{\mathrm{c,OV}}\mathbf u_c=\mathbf f_{\mathrm{eq}} .
$$

它在形式上与各子结构 $\mathbf K_r^j$ 的拼装相同，实质不同：$\mathbf K_{\mathrm{global}}^{\mathrm{OV}}$ 已含重叠区域的耦合刚度，降阶矩阵不再是局部缩聚刚度的简单求和。求得 $\mathbf u_c$ 后按 $\tilde{\boldsymbol\Phi}^j$ 恢复各子结构位移，再按权函数合成全局连续场。工作流为：**细尺度协调组装 → 角点空间投影与求解 → 细尺度位移恢复**。

来源在恢复位移后另加少量细尺度残差修正迭代以提高应变能与灵敏度精度；该步骤不改变基函数与协调空间，是实现层面的附加项。

## 5. 与精确子结构族的关系

### 5.1 两轴分类

子结构方法可按两个独立的轴区分：局部基函数如何构造，接口如何协调。

| | 接口协调：共享迹，拼装后天然连续 | 接口协调：独立基函数，重叠单位分解 |
|---|---|---|
| **局部基函数：目标子结构精确缩聚 + 迹空间限制** | [[exact-substructural-full-trace\|full-trace]]、[[exact-substructural-lagrange\|Lagrange]]、[[exact-substructural-bernstein\|Bernstein]] | 无此组合：共享迹已保证协调，无需重叠 |
| **局部基函数：扩展域超采样后限制** | 多尺度有限元中的超采样，非协调（来源不在本库，待确认） | 本页，即 PIML-OFEM 的精确构造 |

选择超采样就落到第二行，再要求协调就只能走第二列，这解释了为什么超采样与重叠协调在本页所述路线中总是成对出现。按接口协调方式，第一列常被称为非重叠子结构，第二列称为重叠子结构；这对术语描述的是补救手段而非出发点，本库以两轴为分类主干。

### 5.2 误差来源

- **边界层误差**：精确族角点方案的主误差，来自目标边界的线性迹假定。超采样把该假定移到 $\partial\Omega_{\mathrm{os}}^j$，残余误差随 $l$ 增大而减小；具体衰减速率依赖材料分布，本库无定量来源。
- **子空间近似**：$\mathbf K_{\mathrm{global}}^{\mathrm{c,OV}}$ 是协调细尺度空间内 $\operatorname{range}(\tilde{\boldsymbol\Phi}_{\mathrm{global}})$ 上的 Galerkin 投影，在该子空间内仍为 Ritz 最佳逼近（本页推导）。但该子空间与 Lagrange 族的迹空间不嵌套，[[exact-substructural#5. 主要结论与误差来源|总览 §5]] 中“提高次数误差不增”与柔度比较的结论不能直接套用。
- **重叠离散差异**：重叠协调后的细尺度刚度 $\mathbf K_{\mathrm{global}}^{\mathrm{OV}}$ 与标准 Q4 网格刚度不同，即使不做降阶，其解也不等同于标准细网格解。来源的全实心悬臂梁算例显示两者位移高度一致，但未给出一般性界。
- **虚拟材料延拓**：边界子结构的延拓规则是来源的经验选择，不同规则给出不同基函数，属建模误差。
- **代理误差**：以网络替代 §2.1 的局部求解时另计，见 [[../piml/piml-substructural|PIML 子结构分析]]。

### 5.3 代价与适用边界

每个子结构的局部求解规模从 $2(m+1)^2$ 升到 $2(m+2l+1)^2$ 个自由度；来源取 $m=10,\ l=6$，节点数之比约 4.4。来源的复杂孔洞算例（$3601\times901$ 细单元）给出代价量级：细网格 FEM 39.85 s，线性边界角点子结构 11.14 s（平均位移误差 0.0199），在线精确求解超采样问题的 OFEM-SUB 146.77 s（误差 0.0046），以 U-Net 替代局部求解的 PIML-OFEM 12.06 s（误差 0.0066）。不借助学习时，超采样换来的精度要以十余倍于线性边界方案的在线时间支付；这也是该路线在文献中总与 PIML 绑定出现的原因。

本页构造依赖规则正方形子结构与均匀笛卡尔细网格：9 类子结构、16 类细单元与 $\mathbf K_0^t$ 的离线复用都以此为前提。一般几何、非匹配网格、三维与非线性问题均需另行构造，来源将其列为未完成工作。

## 参考依据

- [[../../literature/topopt/piml/translations/Guo2026-PIML-OFEM-zh|Guo 2026 PIML-OFEM 译文]]（arXiv:2607.22019v1，预印本）：§2.1 经典缩聚与角点线性假定，§2.2 超采样基函数构造、角点归一化式 (10)–(16)、虚拟材料延拓，§3 重叠覆盖网格设计、权函数式 (22)–(23)、16 类单元与离线刚度复用、耦合式 (31)–(33)，§5 表 5.1 的时间与误差数据。本页 §2–§4 的构造与 §5.3 数据均取自该文，证据等级为单篇预印本。
- Guo 2026 引用的 Zhang 等 2010、2014 扩展多尺度有限元（EMsFEM）论文为超采样在力学分析中的直接来源，Hou & Wu 1997 为多尺度有限元超采样的原始出处；三者均不在本库，§3 与 §5.1 中关于多尺度有限元非协调处理的叙述待确认。
- [[exact-substructural|子结构分析总览]]与 [[exact-substructural-lagrange#4. 与 full-trace 的关系及近似性质|Lagrange §4]]：精确族的统一框架、迹空间与 Ritz 结论，为 §1 与 §5 的对照基准。
- §2.3 刚体模态自动再现与 §5.2 的 Ritz 性质为本页由构造形式推出，来源未明示。
