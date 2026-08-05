---
title: "PCA 与 POD：低维表示、系数和重构"
type: concept
aliases:
  - Principal Component Analysis
  - Proper Orthogonal Decomposition
  - PCA
  - POD
tags:
  - machine-learning
  - dimensionality-reduction
  - model-reduction
status: "in-progress"
date_added: 2026-07-31
date_update: 2026-08-03
---

# PCA 与 POD：低维表示、系数和重构

> **一句话**：PCA/POD 从一组高维样本中提取低维正交基，用少量系数表示和重构样本；中心化与非中心化处理对应不同的数学对象，必须在实验契约中明确区分。

## 1. 快照矩阵

设有 $L$ 个 $q$ 维样本

$$
\boldsymbol d_1,\ldots,\boldsymbol d_L\in\mathbb R^q,
$$

按列组成快照矩阵

$$
\boldsymbol X
=
\begin{bmatrix}
\boldsymbol d_1 & \cdots & \boldsymbol d_L
\end{bmatrix}
\in\mathbb R^{q\times L}.
$$

PCA/POD 的目标不是直接改变样本的物理含义，而是寻找一个低维子空间，使样本在该子空间中的投影误差尽可能小。

## 2. 中心化 PCA

先计算样本均值

$$
\bar{\boldsymbol d}
=
\frac{1}{L}\sum_{j=1}^L\boldsymbol d_j,
$$

再构造中心化矩阵

$$
\boldsymbol X_c
=
\begin{bmatrix}
\boldsymbol d_1-\bar{\boldsymbol d}
&
\cdots
&
\boldsymbol d_L-\bar{\boldsymbol d}
\end{bmatrix}.
$$

对其作奇异值分解

$$
\boldsymbol X_c
=
\boldsymbol U\boldsymbol\Sigma\boldsymbol Z^{\mathrm T}.
$$

取前 $M$ 个左奇异向量组成

$$
\boldsymbol V_M
=
\begin{bmatrix}
\boldsymbol v_1 & \cdots & \boldsymbol v_M
\end{bmatrix}.
$$

样本的低维系数与重构分别为

$$
\boldsymbol w
=
\boldsymbol V_M^{\mathrm T}
\left(\boldsymbol d-\bar{\boldsymbol d}\right),
$$

$$
\widehat{\boldsymbol d}
=
\bar{\boldsymbol d}
+
\boldsymbol V_M\boldsymbol w.
$$

因此，中心化 PCA 表示的是相对于样本均值的主要变化方向。

## 3. 非中心化 PCA / POD

若不减去样本均值，直接分解

$$
\boldsymbol X
=
\boldsymbol U\boldsymbol\Sigma\boldsymbol Z^{\mathrm T},
$$

则系数和重构写为

$$
\boldsymbol w
=
\boldsymbol V_M^{\mathrm T}\boldsymbol d,
\qquad
\widehat{\boldsymbol d}
=
\boldsymbol V_M\boldsymbol w.
$$

这种写法保留了样本相对于原点的整体幅值，更接近许多快照型 POD 的使用方式。它与中心化 PCA 不是同一个变换，二者的基、系数和截断误差不能混用。

[[../literature/topology-opt/notes/Lei2018-machinelearningdriven]] 对应原文直接由设计矩阵构造特征问题，并写成 $\boldsymbol D^{\mathrm{opt}}\approx\boldsymbol V\boldsymbol w$，没有显式均值项。因此，按其公开公式实现时应首先建立非中心化 PCA/POD 基线；中心化版本可以作为独立对照，但不能写成论文原设定。

## 4. PCA 系数

PCA 系数

$$
\boldsymbol w
=
\begin{bmatrix}
w_1 & \cdots & w_M
\end{bmatrix}^{\mathrm T}
$$

是一个样本在所选特征基下的低维坐标。$\boldsymbol v_i$ 是第 $i$ 个基向量，$w_i$ 是该基向量在当前样本中的权重。

需要区分：

- $\boldsymbol v_i$ 是特征基，不是回归输出；
- $w_i$ 是样本坐标，不是特征值或方差贡献率；
- 奇异值或特征值反映各方向在样本集合中的总体能量；
- 回归模型可以学习外部问题参数到 $\boldsymbol w$ 的映射，再由基重构高维对象。

## 5. 截断维数与误差

若奇异值按

$$
\sigma_1\ge\cdots\ge\sigma_r>0
$$

排列，则前 $M$ 个模态的累计能量占比可写为

$$
\eta_M
=
\frac{\sum_{i=1}^M\sigma_i^2}
{\sum_{i=1}^r\sigma_i^2}.
$$

样本重构误差可按相对二范数或 Frobenius 范数报告：

$$
e_j
=
\frac{\left\|\widehat{\boldsymbol d}_j-\boldsymbol d_j\right\|_2}
{\left\|\boldsymbol d_j\right\|_2},
$$

$$
e_X
=
\frac{\left\|\widehat{\boldsymbol X}-\boldsymbol X\right\|_F}
{\left\|\boldsymbol X\right\|_F}.
$$

$M$ 的选择不能只看能量占比；若重构对象还要进入有限元、优化或其他下游计算，还需检查截断误差对物理响应和最终任务指标的影响。

## 6. 数值实现门禁

一个可验证的 PCA/POD 实现至少应检查：

1. $\boldsymbol V_M^{\mathrm T}\boldsymbol V_M\approx\boldsymbol I$；
2. 取满秩基时能在数值容差内重构快照矩阵；
3. 增大 $M$ 时，训练快照的最优投影误差不增；
4. 中心化版本能够恢复并正确使用训练集均值；
5. 数据划分完成后再用 train 数据拟合基，validation/test 不得参与建基；
6. 重复样本会改变快照分布的权重，但不会增加独立物理标签；
7. 特征向量允许整体变号，验证应比较重构和子空间，而不是逐元素比较基向量符号。

## 7. 与监督回归的关系

当高维输出可被低维基表示时，可以把监督学习任务拆成

$$
\boldsymbol p
\longmapsto
\boldsymbol w(\boldsymbol p)
\longmapsto
\widehat{\boldsymbol d}(\boldsymbol p).
$$

第一步由 SVR、KNN、神经网络或其他回归器完成，第二步由固定低维基重构。PCA/POD 是输出表示与降维方法，不决定回归模型族，也不自动提供物理约束。

## 来源与证据

- [[../literature/topology-opt/notes/Lei2018-machinelearningdriven]] — 非中心化表示、低维系数回归和高维设计重构的论文实例。
- [[machine-learning]] — SVR/KNN、学习对象、训练信号与任务目标的一般分类。
- [[../research/workflows/machine-learning-workflow]] — 数据划分、预处理、评价和可重放产物约定。

## 开放问题

1. 如何对具有置换、旋转或其他等价性的对象先做对齐，再建立低维基？
2. 应按表示误差还是下游物理误差选择 $M$？
3. 当测试样本显著偏离训练子空间时，如何触发拒绝或精确回退？

## 相关页面

- [[mmc/mathematical-foundations]] — MMC 设计向量及组件对应问题。
- [[piml/_index]] — Problem-Independent PIML 主题入口。
- [[../research/technical-lines/piml-research-guide#2.3 模型选型与统一比较契约]] — PIML 模型选型中的表示、数据和比较原则。
