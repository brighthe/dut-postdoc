---
title: 子结构分析总览
type: concept
aliases:
  - exact-substructural
  - 精确子结构分析
  - Substructure Analysis Overview
  - 子结构有限元与静力缩聚
  - Substructure FEM
  - Static Condensation
  - Schur Complement Condensation
  - 精确全接口静力缩聚
  - 角点线性迹降阶
tags:
  - finite-element
  - substructure
  - static-condensation
  - schur-complement
status: in-progress
date_added: 2026-08-09
date_update: 2026-11-06
---

# 子结构分析总览

子结构分析将细网格按块组织，在每块上构造由少数接口自由度到块内位移的局部基函数，求解接口系统后恢复全场。本目录按两个独立的轴组织：局部基函数如何构造，接口如何协调。精确族在目标子结构上做静力缩聚（Static Condensation）并限制迹空间，接口共享、天然协调；保留完整接口时与原细网格系统代数等价，限制边界位移空间时得到迹降阶近似。超采样族在扩展域上构造基函数、以重叠单位分解恢复协调，见 [[oversampling-substructural|超采样子结构分析]]。几何组织与接口示意见 [[substructure-partition-and-cover|子结构划分与覆盖]]；本页 §1 明确适用范围，§2 与 §4 总结精确族的共同框架与分支关系，§3 概述超采样族的构造，§5 列误差来源；具体推导见各分支页。

## 1. 子结构划分与适用范围

精确族采用非重叠子结构划分，相邻块通过共享自由度与相容的边界表示保证协调。非重叠划分的单元归属、内部／边界节点分类、全局计数，以及与重叠覆盖的图示对照，统一见 [[substructure-partition-and-cover|子结构划分与覆盖]]。重叠覆盖与超采样扩展域是不同几何对象，不能仅凭扩展域相交判断接口协调方式。

以下限于小应变线弹性静力、沿细单元边界非重叠划分、接口网格匹配且位移约束位于子结构边界的情形。固定边界后的内部块 $\mathbf K_{ii}^j$ 须可逆，全局约束须排除未约束刚体运动；材料正定性、内部机构及零能模式的条件见 [[exact-substructural-full-trace#2. 静力缩聚|full-trace §2]]。非协调接口与重叠区域分解不在精确族内；超采样基函数与重叠单位分解协调见 [[oversampling-substructural|超采样子结构分析]]。

## 2. 精确族的统一计算框架

局部自由度按边界 $b$、内部 $i$ 分块。内部消元给出 Schur 补及等效边界载荷：

$$
\mathbf K_s^j=\mathbf K_{bb}^j-\mathbf K_{bi}^j(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j,
\qquad
\widetilde{\mathbf f}_b^j=\mathbf f_b^j-\mathbf K_{bi}^j(\mathbf K_{ii}^j)^{-1}\mathbf f_i^j.
$$

用迹基矩阵 $\boldsymbol\Psi^j$ 表示边界节点位移，再将刚度与载荷投影到同一坐标：

$$
\mathbf u_b^j=\boldsymbol\Psi^j\mathbf q^j,
\qquad
\mathbf K_r^j=(\boldsymbol\Psi^j)^{\mathsf T}\mathbf K_s^j\boldsymbol\Psi^j,
\qquad
\mathbf f_r^j=(\boldsymbol\Psi^j)^{\mathsf T}\widetilde{\mathbf f}_b^j.
$$

“迹”指位移场在边界上的限制，$\operatorname{range}(\boldsymbol\Psi^j)$ 决定允许的边界位移。相邻块须采用协调的边界表示；按共享自由度组装、施加相容位移约束并求解后，逐块恢复

$$
\mathbf u_i^j=(\mathbf K_{ii}^j)^{-1}
\left(\mathbf f_i^j-\mathbf K_{ib}^j\mathbf u_b^j\right).
$$

逆矩阵通过线性系统求解实现。内部自由度逐块放回，共享边界位移只写一次。全过程为：**局部消元 → 选择边界表示 → 全局组装与求解 → 内部恢复**。完整接口的推导见 [[exact-substructural-full-trace]]，插值空间上的投影与约束见 [[exact-substructural-lagrange]]。

## 3. 超采样族的构造概要

超采样族同样只保留角点自由度，但不在目标子结构上缩聚。对每块 $\Omega_{\mathrm{sub}}^j$ 取每侧外扩 $l$ 层细单元的扩展域 $\Omega_{\mathrm{os}}^j$，在其外边界施加角点线性插值条件求解 8 个局部问题，把解限制回目标块并作角点归一化，得基函数 $\tilde{\boldsymbol\Phi}^j$；目标边界上的位移由材料分布诱导，不再是线性。各块基函数独立，共享边上不协调，因此相邻块以宽 $h$ 的带重叠，用单位分解权函数组装协调的细尺度刚度 $\mathbf K_{\mathrm{global}}^{\mathrm{OV}}$，再投影到角点空间：

$$
\mathbf K_{\mathrm{global}}^{\mathrm{c,OV}}=\tilde{\boldsymbol\Phi}_{\mathrm{global}}^{\mathsf T}\,\mathbf K_{\mathrm{global}}^{\mathrm{OV}}\,\tilde{\boldsymbol\Phi}_{\mathrm{global}} .
$$

全过程为：**扩展域局部求解 → 限制与角点归一化 → 重叠协调组装 → 角点空间投影与求解 → 位移恢复**。与精确族相比，局部求解规模增大，且须专门设计可重新拼成均匀网格的重叠覆盖，换来的是边界层误差的消除；构造、误差来源与代价见 [[oversampling-substructural|超采样子结构分析]]。

## 4. 接口空间、基底与计算实现

这三个维度应分别选择：接口空间决定允许的位移，基底决定其坐标，计算实现决定如何存储与作用算子。

| 页面 / 表示 | 自由度与空间 | 与其他表示的关系 |
|---|---|---|
| [[exact-substructural-full-trace\|full-trace]] | 全部细边界节点位移，$\boldsymbol\Psi^j=\mathbf I$ | 保留完整接口空间，作为细网格精确基准 |
| [[exact-substructural-lagrange\|Lagrange]] | 边／面多项式在插值点的值，通过采样矩阵表示细边界节点位移 | $p=1$ 为角点方案；提高次数可扩大边界空间，满足覆盖与秩条件时恢复 full-trace |
| [[exact-substructural-bernstein\|Bernstein]] | 边／面多项式的控制系数，一般不是控制点处实际位移 | 同次、同参数化、同采样和等价约束下，与 Lagrange 为可逆换基 |

因此 full-trace 与 Lagrange／Bernstein 并非互斥分类；前者说明保留范围，后两者说明基底。角点方案在二维边上线性，在三维面上双线性 $Q_1$，内部位移仍由平衡决定；一般几何映射的条件见 [[exact-substructural-lagrange#1.6 角点方案与一般几何映射|Lagrange §1.6]]。

显式 Schur 补形成矩阵，隐式 Schur 补只计算向量作用，两者可实现同一个接口问题；单元层 Matrix-Free 又是局部刚度作用的实现选择，不自动改变接口空间。各分支页给出对应实现，专门的算子组织见 [[../matrix-free/mf-schur-substructural|子结构 Schur 补 Matrix-Free 算子]]。

上表三页同属精确族：局部基函数来自目标子结构的精确缩聚加迹空间限制，相邻块共享迹、拼装后天然协调。§3 的超采样族改变基函数来源，并以重叠协调补救由此产生的不协调。两族按两个轴对照如下，详见 [[oversampling-substructural|超采样子结构分析]]。

| | 接口协调：共享迹 | 接口协调：重叠单位分解 |
|---|---|---|
| **基函数：目标子结构精确缩聚 + 迹空间** | full-trace、Lagrange、Bernstein | 无此组合 |
| **基函数：扩展域超采样后限制** | 多尺度有限元中的非协调超采样（本库无来源） | [[oversampling-substructural\|超采样子结构分析]] |

按接口协调方式，第一列常称非重叠子结构，第二列称重叠子结构；本目录以两轴为分类主干，该术语只作别名。

## 5. 主要结论与误差来源

- **完整接口**：相同细网格、材料、载荷与约束下，精确消元和精确求解恢复同一个细网格解，不增加缩聚近似误差。这是相对离散系统的精确性，不消除有限元离散误差。
- **受限接口空间**：在协调、相容约束及正定条件下，得到该空间中的 Ritz 最佳逼近。相同载荷、齐次位移约束下，降阶柔度不大于完整接口柔度；非零给定位移不能直接套用此结论。证明及条件见 [[exact-substructural-lagrange#4.2 Ritz 最佳逼近与柔度|Lagrange §4.2]]。
- **提高次数与更换基底**：固定划分、采样及物理约束，空间嵌套时提高次数使最佳逼近误差不增；同一空间内可逆换基不改变精确位移。具体误差量级另需正则性、材料与网格条件，见 [[exact-substructural-lagrange#4.5 误差定位与量级的适用边界|Lagrange §4.5]]。
- **边界层误差**：角点方案的迹限制在目标边界附近形成受人为线性条件支配的区域，是受限接口空间误差在角点方案中的主要表现。超采样把线性条件移到扩展域外边界以缓解之，但其子空间与迹空间不嵌套，本节前两条的嵌套与柔度结论不直接适用，见 [[oversampling-substructural#5. 与精确子结构族的关系|超采样 §5]]。
- **计算误差**：浮点运算及内部、全局求解容差与边界空间近似是不同误差来源。若以 PIML 预测局部算子，还需单独计入代理误差，见 [[../piml/piml-substructural|PIML 子结构分析]]。
