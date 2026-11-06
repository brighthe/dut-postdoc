---
title: "基于 PIML 的子结构分析"
type: concept
aliases:
  - piml-substructural
  - 子结构 PIML
  - 子结构静力缩聚 PIML 算子
  - 子结构 PIML 算子
tags:
  - PIML
  - static-condensation
  - schur-complement
  - finite-element
  - matrix-free
  - GPU
status: in-progress
date_added: 2026-08-13
date_update: 2026-10-26
---

# 基于 PIML 的子结构分析

PIML 子结构分析学习局部材料分布到局部力学算子的映射，以离线训练后的预测替代在线局部求解。三个分支均采用**形函数预测**：预测内部恢复矩阵，以当前材料刚度作能量投影，求解全局接口系统，再用同一映射恢复内部位移。本页维护方法定位、分支导航与共同训练约束；具体矩阵、求解和误差公式由分支页维护。

## 1. 方法定位与适用范围

离线流程为“材料样本 → 精确标签或能量目标 → 训练模型”；在线流程为“材料输入 → 预测内部映射 → 能量投影 → 全局接口求解 → 位移恢复”。PIML 替代的是局部内部映射的构造，全局求解仍需执行。方法在 PIML 中的位置见 [[piml-paradigm]]，精确基准见 [[../substructure/exact-substructural|精确子结构总览]]。

统一记边界位移为 $\mathbf u_b^j=\boldsymbol\Psi^j\mathbf q^j$，预测形函数为 $\widehat{\mathbf N}^j=[\boldsymbol\Psi^j;\widehat{\mathbf T}^j]$。$\boldsymbol\Psi^j$ 固定边界表示，$\widehat{\mathbf T}^j$ 将接口坐标映射到内部位移；网络不直接预测当前载荷下的全局解。

三个分支共同假设线弹性静力、非重叠划分、协调接口、内部无载荷、位移约束位于子结构边界，且 $\mathbf K^j\succeq0,\mathbf K_{ii}^j\succ0$。模型复用要求局部几何、离散、编号、材料参数域和接口表示相容；边界空间改变通常需要重训或明确的投影／换基。非零内部载荷还需特解和一致载荷处理，见 [[../substructure/exact-substructural-full-trace#4.1 形函数表示与非零内部载荷|精确 full-trace §4.1]]。超采样基函数加重叠单位分解协调的路线不满足非重叠与协调接口假设，其精确构造见 [[../substructure/oversampling-substructural|超采样子结构分析]]，本页三个分支均不覆盖该路线，本库亦无其 PIML 分支页。

**另一学习对象。** 文献与实现中也有直接预测缩聚刚度的路线 B；形函数预测沿用路线 A 的称呼。路线 B 需单独保证刚度的结构性质，内部恢复另配模型或精确回代。精确回代增加局部求解成本，只保证给定预测边界位移下的内部平衡，不能消除接口误差；独立预测刚度与恢复映射也不自动能量一致。三个分支页均只展开路线 A；学习对象分类见 [[piml-paradigm#2.2 学习对象|PIML 分类]]。

## 2. 接口表示与分支导航

| 分支 | 边界表示与未知量 | 主要区别 | 精确基准 |
|---|---|---|---|
| [[piml-substructural-full-trace\|Full-trace PIML]] | $\boldsymbol\Psi=\mathbf I$，保留全部边界节点位移 | 无迹降阶误差；预测完整内部映射 | [[../substructure/exact-substructural-full-trace\|精确 full-trace]] |
| [[piml-substructural-lagrange\|Lagrange PIML]] | $\boldsymbol\Psi=\mathbf S_p$，未知量为边界插值点位移 | 任意次数；$p=1$ 为角点方案 | [[../substructure/exact-substructural-lagrange\|精确 Lagrange]] |
| [[piml-substructural-bernstein\|Bernstein PIML]] | $\boldsymbol\Psi=\mathbf S_{B,p}$，未知量为控制系数 | 系数一般不等于节点位移；$p=3$ 为三次 Bézier 表示 | [[../substructure/exact-substructural-bernstein\|精确 Bernstein]] |

分支页均按“局部矩阵与边界表示 → 预测与能量投影 → 求解与恢复 → 等价与误差”组织。局部标签与预测维数见各页 §2，约束与全场恢复见 §3，换基、次数提升和误差条件见 §4。

同次 Lagrange 与 Bernstein 在相同参数化、采样及约束下表示同一边界空间；预测内部映射也须同步换基，才能得到相同预测解。Full-trace 描述自由度保留范围，Lagrange／Bernstein 描述边界基底，不是互斥分类。

各页优先沿用相应精确页的记号：完整接口 Schur 补在本页比较语境中记为 $\mathbf K_{s,\mathrm{full}}$，full-trace 页简写为 $\mathbf K_s$。本页材料输入用 $\boldsymbol\eta^j$；Bernstein 页的全局 $\boldsymbol\eta$ 是控制系数，材料输入另记 $\boldsymbol\mu^j$。节点数与自由度数按各分支定义，不混用。

Matrix-Free 是算子实现方式，不改变接口空间：完整接口与角点实现见 [[../matrix-free/mf-piml-substructural]]，单元层 PA 条件见 [[../matrix-free/mf-pa-piml-substructural]]。超采样与重叠单位分解属于其他载体，不能直接套用这里的协调组装；文献与应用谱系统一见 [[piml-paradigm#4. 文献谱系|PIML 文献谱系]]。

## 3. 共同训练与结构约束

### 3.1 网络输出与力学约束

约束针对最终用于计算的映射，网络原始输出可经补全或参数化重构。设 $\mathbf R_q^j,\mathbf R_b^j,\mathbf R_i^j$ 为同一组刚体运动在接口坐标、细边界和内部的表示，则要求

$$
\boldsymbol\Psi^j\mathbf R_q^j=\mathbf R_b^j,\qquad
\widehat{\mathbf T}^j\mathbf R_q^j=\mathbf R_i^j.
\tag{1}
$$

这里 $\mathbf R$ 表示刚体模态。形函数边界块须固定为 $\boldsymbol\Psi^j$；以同一当前材料刚度作能量投影可保证预测刚度对称半正定。对于无额外零能模式的自由子结构，还应使刚度零空间恰好对应刚体运动，变形子空间正定。直接预测刚度时同样须保证这些性质，仅补全对称项和刚体约束并不足够。

全局可解性还要求接口表示列满秩、公共迹协调、给定位移相容，且支承消除全部全局零能模式。约束的具体构造见各分支 §3。

### 3.2 材料样本与训练目标

每个样本描述子结构内细单元的材料分布，例如 $\boldsymbol\eta^{(m)}=[E_1^{(m)}/E_0,\ldots,E_{n_e}^{(m)}/E_0]^{\mathsf T}$。采样域须保证内部矩阵正定；训练、推理采用相同几何、材料归一化、编号与接口坐标。

| 训练方式 | 数据与目标 | 注意事项 |
|---|---|---|
| 监督训练 | 材料样本及精确内部映射标签，最小化预测与标签的矩阵误差 | 标签计算见各分支 §2；可预测独立分量后补全 |
| 无标签能量训练 | 材料样本及当前刚度作用，最小化固定边界块下的能量 | 无须精确形函数标签；有限模型与训练不保证精确平衡 |

省略子结构上标，记样本数为 $M$、精确内部映射为 $\mathbf T^{(m)}$。两种通用目标可写为

$$
\mathcal L_{\mathrm{sup}}
=\frac1M\sum_m\|\widehat{\mathbf T}^{(m)}-\mathbf T^{(m)}\|_F^2,\qquad
\mathcal L_{\mathrm{energy}}
=\frac1{2M}\sum_m\operatorname{tr}
\left[(\widehat{\mathbf N}^{(m)})^{\mathsf T}
\mathbf K^{(m)}\widehat{\mathbf N}^{(m)}\right].
\tag{2}
$$

能量目标是遍历单位接口坐标的应变能之和（本页推导）；固定边界块、内部无载荷且 $\mathbf K_{ii}\succ0$ 时，以内部映射为变量的唯一极小点是精确平衡延拓。边界块不能随网络缩放以降低损失。独立分量损失、补全后的矩阵损失及不同基底下的损失权重可能不同，比较训练方案时须明确度量。

式 (2) 不作为某篇论文训练算法的逐式复现。Huang2024 采用伪结构位移场及变化的位移基，具体方案见 [[../../literature/topopt/piml/translations/Huang2024-PIML-datafree-zh#4.2 基于力学的损失函数|Huang2024 §4.2]] 与其 §4.3。

## 4. 误差与使用边界

应区分三类误差：边界空间限制带来的**迹降阶误差**、内部映射预测带来的**代理误差**、浮点与求解容差带来的**计算误差**。完整接口没有第一项；提高插值次数不自动减小代理误差，独立训练的预测全场空间未必嵌套。

共同的局部误差关系如下。令 $\mathbf T^j=-(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j\boldsymbol\Psi^j$、$\mathbf E^j=\widehat{\mathbf T}^j-\mathbf T^j$，$\mathbf K_r^j$ 为该接口空间的精确刚度。在固定同一边界块和材料刚度时，

$$
\widehat{\mathbf K}_r^j-\mathbf K_r^j
=(\mathbf E^j)^{\mathsf T}\mathbf K_{ii}^j\mathbf E^j\succeq0.
\tag{3}
$$

这是能量投影的直接展开：精确形函数 $\mathbf N^j=[\boldsymbol\Psi^j;\mathbf T^j]$ 的内部刚度作用为零，而预测增量为 $[0;\mathbf E^j]$，故交叉项消失，只剩式 (3) 的二次项。该关系不包含迹降阶误差，也不适用于任意直接预测刚度。

在相同材料与载荷、零内部载荷、齐次支承、同一预测形函数组装及恢复、约束后正定且精确求解的条件下，预测柔度不大于同一接口空间的精确柔度，后者不大于细网格柔度。柔度偏低不表示设计更优；具体能量关系及非零给定位移限制见 [[piml-substructural-full-trace#4. 代数等价与代理误差|full-trace §4]]、[[piml-substructural-lagrange#4.2 Ritz 最佳逼近与柔度|Lagrange §4.2]]、[[piml-substructural-bernstein#4.4 次数提升与 full-trace|Bernstein §4.4]]。

代理系统收敛不等于原细网格平衡。评价应检查恢复场残量、与精确基准的位移／能量偏差，以及推理、能量投影、全局求解和恢复的总成本。拓扑优化中的设计比较须采用统一细网格重分析；应用闭环见 [[../density-topopt/substructural-density-topology-optimization]]。
