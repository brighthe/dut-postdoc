---
title: "PIML 数学基础"
type: concept
aliases:
  - PIML mathematical foundations
  - PIML 数学原理
  - 问题无关机器学习数学基础
tags:
  - PIML
  - EMsFEM
  - finite-element
  - machine-learning
status: in-progress
date_added: 2026-06-18
date_update: 2026-07-26
---

# PIML 数学基础

> **一句话**：Problem-Independent Machine Learning（PIML）学习由局部材料分布决定、可嵌入有限元分析的局部力学表示；Huang 2022 的基础实现以 EMsFEM 多尺度形函数为学习对象，其后的子结构路线改以静力缩聚刚度和子结构形函数为载体。

## 1. 问题无关性的数学含义

设 $E$ 是一个粗单元或局部区域，$\boldsymbol{\rho}^E$ 是其中的细尺度材料分布，$\mathcal{R}^E$ 是形函数、缩聚刚度或其他局部力学表示。固定控制方程、离散方式、单元类型和材料模型后，可以把局部构造过程写成

$$
\mathcal{R}^E
=
\mathcal{G}\!\left(
\boldsymbol{\rho}^E;
\mathcal{L},\mathcal{D},\mathcal{M}
\right),
$$

其中 $\mathcal{L}$、$\mathcal{D}$ 和 $\mathcal{M}$ 分别表示控制算子、离散设置和材料模型。PIML 用参数化模型 $\mathcal{G}_{\theta}$ 逼近这一局部映射：

$$
\widehat{\mathcal{R}}^E
=
\mathcal{G}_{\theta}\!\left(\boldsymbol{\rho}^E\right).
$$

“问题无关”是指该局部映射不直接依赖宏观设计域、整体边界条件和外载荷，因此训练后的模型可在相同 $\mathcal{L}$、$\mathcal{D}$ 和 $\mathcal{M}$ 设置下复用。它不表示模型能够无条件跨 PDE、跨离散、跨单元或跨本构泛化。

## 2. Huang 2022 的基础路线：PIML + EMsFEM

Huang 2022 把 PIML 放入扩展多尺度有限元（EMsFEM）的粗细两级网格中：

```text
粗单元内部细尺度密度
  -> EMsFEM 多尺度形函数
  -> 粗单元刚度矩阵
  -> 粗尺度有限元分析
```

对粗单元 $E$，多尺度形函数矩阵 $\boldsymbol{N}^E$ 把粗尺度自由度映射到细尺度位移：

$$
\boldsymbol{u}^{h,E}
\approx
\boldsymbol{N}^E \boldsymbol{u}^{H,E}.
$$

若粗单元包含若干细单元 $f$，其粗尺度刚度可以写为

$$
\boldsymbol{K}^E
=
\sum_f
\left(\boldsymbol{N}_f^E\right)^{T}
\boldsymbol{k}^f
\boldsymbol{N}_f^E,
$$

其中 $\boldsymbol{k}^f$ 是细单元刚度。基础 PIML 学习的是

$$
\boldsymbol{\rho}^E
\longmapsto
\widehat{\boldsymbol{N}}^E
\longmapsto
\widehat{\boldsymbol{K}}^E,
$$

不是直接预测最终拓扑，也不是直接预测某个宏观边值问题的全局位移场。

## 3. 监督训练与力学约束

Huang 2022 仍采用监督训练：随机生成局部材料分布，通过局部 EMsFEM 计算精确形函数和粗单元刚度作为标签。其训练目标可以概括为

$$
\mathcal{J}(\theta)
=
\lambda_N
\left\|
\widehat{\boldsymbol{N}}^E-\boldsymbol{N}^E
\right\|_F^2
+
\lambda_K
\left\|
\widehat{\boldsymbol{K}}^E-\boldsymbol{K}^E
\right\|_F^2,
$$

其中第一项控制形函数误差，第二项约束由预测形函数得到的刚度。$\lambda_N$ 和 $\lambda_K$ 表示两类误差的权重；具体训练设置与实验数字见论文笔记。

在线阶段将各粗单元预测刚度组装为粗尺度系统：

$$
\boldsymbol{K}^{H}\boldsymbol{U}^{H}
=
\boldsymbol{F}^{H},
$$

求得粗尺度自由度后，再通过多尺度形函数恢复需要的细尺度响应。

## 4. 降维与 PIML 的职责边界

Huang 2022 同时包含两个不同机制：

- **EMsFEM 降维**：用粗尺度自由度表示细尺度响应，降低全局求解规模；
- **PIML 学习替代**：用离线训练模型替代优化迭代中的局部多尺度形函数构造。

因此，降维是 Huang 2022 采用的数值载体，不是 PIML 定义本身的必要条件。只要学习对象是可由局部信息决定、能够嵌入后续力学求解并在不同宏观问题中复用的局部表示，就可以讨论 Problem-Independent 的学习方式。

## 5. 子结构缩聚与 PIML 学习映射

Huang 2022 以粗单元多尺度形函数为局部载体；Huang 2023 之后的子结构路线把同一「局部密度 → 局部力学表示」映射改写到经典子结构静力缩聚框架中。方法演化脉络见 [[method-lineage]]，本节给出统一记法。

对子结构 $\Omega^j$，按边界自由度与内部自由度分块：

$$
\mathbf K^j =
\begin{bmatrix}
\mathbf K_{\mathrm{bb}}^j & (\mathbf K_{\mathrm{ib}}^j)^T\\
\mathbf K_{\mathrm{ib}}^j & \mathbf K_{\mathrm{ii}}^j
\end{bmatrix}.
$$

消去内部自由度，得到精确缩聚刚度与内部位移恢复关系：

$$
\mathbf K_s^j =
\mathbf K_{\mathrm{bb}}^j
-
(\mathbf K_{\mathrm{ib}}^j)^T
(\mathbf K_{\mathrm{ii}}^j)^{-1}
\mathbf K_{\mathrm{ib}}^j,
$$

$$
\mathbf u_{\mathrm i}^j =
-
(\mathbf K_{\mathrm{ii}}^j)^{-1}
\mathbf K_{\mathrm{ib}}^j
\mathbf u_{\mathrm b}^j.
$$

$\mathbf K_s^j$ 只作用在边界/接口自由度上，$\mathbf u_{\mathrm i}^j$ 给出由边界自由度延拓回内部的细尺度响应。子结构形函数 $\mathbf N^j$ 即由该延拓关系与边界基构成。

在这一框架下，PIML 学习的基本映射是

$$
\mathcal F_\theta:\boldsymbol\rho^j
\longmapsto
\widehat{\mathbf N}^j
\quad\text{或}\quad
\widehat{\mathbf K}_s^j,
$$

即用参数化模型替代「对子结构内部自由度做消元求逆」这一在优化迭代中反复出现的局部计算。它与 §1 的 $\mathcal G_\theta$ 是同一问题无关性定义在子结构载体上的具体化：学习对象仍由局部密度决定，不依赖宏观设计域、整体边界条件和外载荷；宏观问题只出现在全局接口方程中。

直接预测 $\widehat{\mathbf K}_s^j$ 与先预测 $\widehat{\mathbf N}^j$ 再构造刚度并不等价：后者天然继承形函数与刚度之间的能量一致关系，前者则可能破坏该关系，需要额外的结构保持手段（见 §6）。

## 6. 数学边界

- 问题无关性只在固定控制方程、离散、单元和材料模型的范围内成立。
- EMsFEM 形函数的边界构造和粗细尺度选择会引入离散误差；PIML 不能自动消除该基线误差。
- §5 的静力缩聚在数学上等价于 Schur 补，本身是精确的；其残差只反映浮点舍入，必须与 PIML 预测误差分开报告，不能相互替代。
- 形函数误差较小不自动保证刚度、全局位移、柔顺度、灵敏度或最终拓扑误差较小，必须逐层验证。
- 预测刚度应进一步检查对称性、半正定性、刚体模态和能量一致性，不能只报告回归损失。

## 7. 后续数学扩展

- **子结构 PIML**：将局部表示改为子结构形函数和静力缩聚刚度，统一记法见 §5，完整方法关系见 [[method-lineage]]。
- **Mechanics-based data-free PIML**：以最小势能等力学目标替代局部真值标签；本页不展开完整变分推导。
- **并行与 Matrix-Free**：改变局部表示的生成、存储和应用方式，但不改变问题无关性的基本定义。

## 8. 来源与相关页面

- [[../../literature/topology-opt/Huang2022-problemindependentmachine]] — EMsFEM 形函数学习与问题无关性起点。
- [[../../literature/topology-opt/Huang2023-PIML-substructure]] — 子结构形函数与缩聚刚度扩展。
- [[../../literature/topology-opt/Huang2024-PIML-datafree]] — mechanics-based data-free 扩展。
- [[method-lineage]] — 从 Lei 前史到并行 PIML 的方法谱系。
- [[../../research/technical-lines/piml-research-guide]] — 当前能力、目标差距、实施路线与验收标准。
