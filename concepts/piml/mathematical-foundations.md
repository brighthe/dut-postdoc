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
date_update: 2026-08-09
---

# PIML 数学基础

> **一句话**：PIML（Problem-Independent Machine Learning，问题无关机器学习）在固定的局部力学载体上学习“局部材料分布 → 可嵌入传统全局平衡求解的局部表示”，而不直接学习某个宏观边值问题的全局解或最终拓扑。

## 1. 页面定位与问题无关性

设 $E$ 是粗单元、子结构或其他局部力学载体，$\boldsymbol\rho^E$ 是其中的细尺度材料分布，$\mathcal R^E$ 是该载体产生的局部力学表示。固定控制方程 $\mathcal L$、离散设置 $\mathcal D$、材料模型 $\mathcal M$ 与载体拓扑 $\mathcal C$ 后，精确局部构造写为

$$
\mathcal R^E
=
\mathcal G\!\left(
\boldsymbol\rho^E;
\mathcal L,\mathcal D,\mathcal M,\mathcal C
\right).
$$

PIML 用参数化模型逼近该局部映射：

$$
\widehat{\mathcal R}^E
=
\mathcal G_\theta\!\left(\boldsymbol\rho^E\right).
$$

“问题无关”只表示该映射不直接依赖宏观设计域、整体边界条件和外载荷；模型仅可在相同的 $\mathcal L$、$\mathcal D$、$\mathcal M$ 与 $\mathcal C$ 范围内复用。它不意味着可无条件跨 PDE、离散、单元、材料或局部载体泛化。

当 $\boldsymbol\rho^E$ 是拓扑优化设计相对密度时，它通过材料插值进入局部本构和有限元刚度；该密度相关线弹性算子由 [[../linear-elasticity]] 维护。PIML 学习其生成的局部表示，不替代或隐式重新定义材料插值。

Problem-Independent PIML 与最终设计代理、PINN 解场学习的角色边界见 [[../ml-roles-and-boundaries]]。

## 2. 统一局部力学载体契约

无论载体是 EMsFEM 粗单元还是经典子结构，PIML 都遵守相同的局部—全局契约：

```text
局部输入 rho^E
  -> 精确局部力学构造
  -> 精确标签 R_exact^E
  -> PIML 预测 R_hat^E
  -> 传统全局平衡、细尺度恢复与下游评价
```

| 契约要素 | 数学角色 | 不随预测来源改变的责任 |
|---|---|---|
| 局部输入 | $\boldsymbol\rho^E$ 及固定的载体配置 | 决定局部本构与精确标签；不含宏观载荷或边界条件。 |
| 精确标签 | $\mathcal R_{\mathrm{exact}}^E$ | 学习目标、误差评价与精确回退的数学真值。 |
| 预测表示 | $\widehat{\mathcal R}^E$ | 必须满足与所选表示相适配的结构条件。 |
| 全局接入 | 局部表示进入装配或算子作用 | 保持传统全局平衡问题，而非由网络直接替代全局解。 |
| 下游评价 | 位移、柔顺度、恢复场及后续优化量 | 判断局部误差能否接受，不能只用局部 MSE。 |

该契约是局部算子构造的数学依据：精确计算与 PIML 预测应使用相同的局部输入、输出语义与全局接入方式；数据与部署层面的工程约定由 [[../../research/technical-lines/piml-research-guide]] 维护，本页不展开。

## 3. 局部载体

### 3.1 EMsFEM 粗单元

Huang 2022 在 EMsFEM 粗细两级网格中学习局部密度到多尺度形函数的映射，再由形函数构造粗单元刚度并完成粗尺度分析。其数学角色是说明 PIML 的问题无关性不依赖于子结构这一特定载体；相关论文事实由 [[../../literature/topology-opt/notes/Huang2022-problemindependentmachine]] 维护。

### 3.2 子结构静力缩聚

在经典子结构有限元载体中，设第 $j$ 个子结构 $\Omega^j$ 为规则矩形/六面体子域，细网格为 $Q4$/六面体单元。§2 的局部—全局契约在子结构载体上的具体化为：

| 量 | 定义与形状 | 角色 |
|---|---|---|
| $\boldsymbol\rho^j$ | 子结构细网格上的逐单元设计相对密度，形状 $(n_1^j,\dots,n_d^j)$ | 局部 PIML 输入；不含宏观载荷与边界条件 |
| $\mathbf K^j$ | $\mathbb R^{(n_i+n_b)\times(n_i+n_b)}$ | 由 $\boldsymbol\rho^j$ 经 modified SIMP 插值（见 [[../linear-elasticity]] §2.3、§6）装配的局部未缩聚刚度 |
| $\mathcal R_{\mathrm{exact}}^j=(\mathbf N_{\mathrm{exact}}^j,\mathbf K_{s,\mathrm{exact}}^j)$ | $\mathbf N^j\in\mathbb R^{n_i\times n_b}$、$\mathbf K_s^j\in\mathbb R^{n_b\times n_b}$ | 精确缩聚标签（PIML 学习目标） |
| $\widehat{\mathbf N}^j$ 或 $\widehat{\mathbf K}_s^j$ | 与精确标签相同形状 | PIML 预测表示 |

局部自由度采用节点级划分：节点坐标落在子结构边界面坐标容差内的自由度归为接口自由度 $b$，其余为内部自由度 $i$；节点 $n$ 的第 $k$ 个位移分量的自由度为 $d n+k$。$n_i$、$n_b$ 由该约定唯一确定，并同时约束精确标签、预测输出、全局映射与细尺度恢复；划分与编号的数学事实由 [[../substructural-condensation]] §2.1 唯一维护。

无内部载荷（$\mathbf f_i^j=\boldsymbol 0$）时，精确标签由 Schur 补缩聚定义：

$$
\mathbf N_{\mathrm{exact}}^j
=
-\mathbf K_{ii}^{-1}\mathbf K_{ib},
\qquad
\mathbf K_{s,\mathrm{exact}}^j
=
\mathbf K_{bb}-\mathbf K_{bi}\mathbf K_{ii}^{-1}\mathbf K_{ib}.
$$

> [!IMPORTANT]
> **唯一数学事实源**：上述缩聚的推导、刚体模态、能量一致性、接口 Scatter-Add、全局接口系统方程与细尺度恢复，均由 [[../substructural-condensation]] 唯一维护。本页不重复推导或接口系统方程，只把精确缩聚结果作为 PIML 学习目标引用。

对子结构路线，局部—全局映射链为

```text
rho^j -> K^j -> (N_exact^j, K_s,exact^j)
      -> (N_hat^j 或 K_s,hat^j)
      -> K_global = sum_j L_j^T K_s^j L_j, K_global U_b = F_b
      -> u_i^j = N^j u_b^j
      -> 下游评价
```

预测与精确表示共用同一全局接入（[[../substructural-condensation]] §4.1）：局部表示经 Scatter-Add 进入全局接口系统，宏观边界条件和外载荷只在全局接口系统中出现，因此不改变局部 PIML 映射的问题无关性。路线 A 的 $\widehat{\mathbf K}_s^j=(\widehat{\mathbf N}^j)^{\mathsf T}\mathbf K^j\widehat{\mathbf N}^j$ 依赖 $\mathbf K^j$；路线 B 直接给出 $\widehat{\mathbf K}_s^j$，但不保持与 $\mathbf N$ 的恢复/能量构造关系（见 §4）。Huang 2023 的子结构路线事实由 [[../../literature/topology-opt/notes/Huang2023-PIML-substructure]] 维护。

## 4. 可学习表示与路线 A/B

对子结构载体，PIML 的学习对象为

$$
\mathcal F_\theta:\boldsymbol\rho^j
\longmapsto
\widehat{\mathbf N}^j
\quad\text{或}\quad
\widehat{\mathbf K}_s^j.
$$

- **路线 A：预测形函数。**预测 $\widehat{\mathbf N}^j$，再构造

  $$
  \widehat{\mathbf K}_s^j
  =
  (\widehat{\mathbf N}^j)^{\mathsf T}
  \mathbf K^j
  \widehat{\mathbf N}^j.
  $$

  这样预测形函数、内部位移恢复与缩聚刚度保持显式构造关系；该路线不构成对长期学习对象的排他性预设。

- **路线 B：直接预测缩聚刚度。**$\boldsymbol\rho^j\mapsto\widehat{\mathbf K}_s^j$ 与路线 A 在同一精确标签与下游任务下比较；其输出不依赖 $\mathbf K^j$，但不天然保持与 $\mathbf N^j$ 的恢复/能量关系。

Huang 2024 的连续形函数与 mechanics-based 训练扩展由 [[../../literature/topology-opt/notes/Huang2024-PIML-datafree]] 维护；本页不预设具体网络架构或训练损失。

## 5. 结构性质、误差与精确回退

精确缩聚误差仅反映浮点舍入，必须与 PIML 预测误差分开报告。对每种预测表示，至少区分以下层次：

- **局部表示误差**：$\widehat{\mathbf N}^j$ 或 $\widehat{\mathbf K}_s^j$ 与精确标签的差异；
- **结构条件**：路线 A 检查形函数、边界/完备性或已确认的构造条件；路线 B 必须检查或硬保持对称性、适用条件下的半正定性或约束后正定性、刚体模态与能量一致性；
- **下游误差**：接口位移、柔顺度、细尺度恢复、灵敏度及最终优化结果，不能由局部 MSE 代替；
- **可信处置**：预测违反结构条件、超出训练分布或导致下游误差不可接受时，回退至相同契约下的精确局部构造。

形函数误差较小不自动保证刚度、全局响应或优化轨迹准确；结构检查和局部—全局误差传播是 PIML 研发的必要部分，而非训练后的可选附加项。

## 6. 来源与证据

- [[../../literature/topology-opt/notes/Huang2022-problemindependentmachine]] — EMsFEM 形函数学习与问题无关性起点。
- [[../../literature/topology-opt/notes/Huang2023-PIML-substructure]] — 子结构形函数与缩聚刚度扩展。
- [[../../literature/topology-opt/notes/Huang2024-PIML-datafree]] — 连续形函数与 mechanics-based data-free 扩展。

## 相关页面

- [[../linear-elasticity]] — 设计相对密度参数化本构、单元刚度与全局平衡方程。
- [[../substructural-condensation]] — 子结构缩聚的唯一数学事实源。
- [[../ml-roles-and-boundaries]] — 相关机器学习路线的作用位置与方法边界。
- [[piml-paradigm]] — PIML 通用五步范式与代数映射。
- [[method-lineage]] — 从 Lei 前史到并行 PIML 的方法谱系。
- [[../../research/technical-lines/piml-research-guide]] — 研究目标、模型选型、统一比较契约与证据边界。
