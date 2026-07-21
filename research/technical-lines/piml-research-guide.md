---
title: "PIML 局部力学算子技术线研究指南"
topic: "PIML 局部形函数与等效算子的结构保持、误差传播和优化闭环"
tags:
  - technical-line
  - research-guide
  - PIML
  - substructuring
  - operator-learning
  - topology-optimization
status: "in-progress"
date_start: 2026-07-21
date_update: 2026-07-21
related:
  - piml
  - method-lineage
  - piml-matrix-free-gpu-and-model-selection-technical-synthesis
---

# PIML 局部力学算子技术线研究指南

> **定位**：本页是 PIML 技术线的长期第一入口，负责局部力学表示、结构保持、误差传播、灵敏度和优化闭环。它不从属于固定的研究方向编号，也不负责全局 Matrix-Free 求解器或 GPU 性能实现的细节。
>
> **当前事实底线**：已经跑通子结构缩聚与极小 MLP 预测局部 $K_s$ 的前向原型；尚未完成结构保持参数化、全局误差传播、多尺度灵敏度和完整拓扑优化闭环。

## 一、技术线目标与边界

PIML 的长期目标不是直接预测某个给定载荷和边界条件下的最终拓扑，而是学习能够在多个整体问题中复用的局部力学表示，例如多尺度形函数 $\mathbf N^j$ 或缩聚刚度 $\mathbf K_s^j$。

本技术线负责：

- 局部材料或几何状态到局部力学算子的学习映射；
- 物理约束、结构保持和可信度判断；
- 局部预测误差向全局响应、灵敏度与优化结果的传播；
- 监督、data-free、operator learning 与混合精确回退策略；
- PIML 模型进入结构分析和拓扑优化前的统一评价。

本技术线不负责：

- 全局算子的无矩阵作用、Krylov 和预条件器实现，见 [[matrix-free-research-guide]]；
- GPU 内核、数据搬移、MPI 和端到端性能工程，见 [[gpu-hpc-research-guide]]；
- 某个阶段性课题如何组合三条技术线，见对应计划与综合页。

## 二、数学对象与最小接口

对子结构 $\Omega^j$，按边界和内部自由度分块：

$$
\mathbf K^j =
\begin{bmatrix}
\mathbf K_{\mathrm{bb}}^j & (\mathbf K_{\mathrm{ib}}^j)^T\\
\mathbf K_{\mathrm{ib}}^j & \mathbf K_{\mathrm{ii}}^j
\end{bmatrix}.
$$

精确缩聚刚度和内部位移恢复为：

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

PIML 学习的基本映射是：

$$
\mathcal F_\theta:\boldsymbol\rho^j
\longmapsto
\widehat{\mathbf N}^j
\quad\text{或}\quad
\widehat{\mathbf K}_s^j.
$$

最小软件接口应至少包含：

- 输入：局部密度、几何/材料参数、子结构类型与必要状态变量；
- 输出：$\widehat{\mathbf N}^j$、$\widehat{\mathbf K}_s^j$ 或结构保持参数；
- 检查：形状、对称性、最小特征值、刚体模态、能量一致性和置信度；
- 回退：结构检查失败或不确定度过高时调用精确局部消元；
- 评价：局部误差、全局响应、求解器影响和部署成本使用统一记录格式。

## 三、当前已有基础

### 3.1 精确子结构前向链路

- 已跑通“局部细尺度密度 → 子结构静力缩聚 → $K_s^j$ → 全局接口缩聚方程 → 接口求解/细尺度恢复”。
- 精确缩聚与全尺度 Schur 补误差达到 $10^{-15}$ 量级。
- 接口解与全尺度直解保持 $10^{-14}$–$10^{-12}$ 量级一致。

### 3.2 PIML 预测原型

- 已训练极小 MLP 直接预测局部 $K_s$。
- 部署算例上逐子结构相对预测误差均值：
  - $5\times5$：$1.6\times10^{-3}$；
  - $10\times10$：$8.2\times10^{-3}$。
- 两档结果均优于只使用局部平均密度的 Mock 对照。

### 3.3 当前证据的准确读法

- $10^{-15}$ 级结果属于精确缩聚基线，不是 PIML 预测误差。
- $1.6\times10^{-3}$ 和 $8.2\times10^{-3}$ 是局部 $K_s$ 误差，不代表位移、柔顺度、灵敏度或最终拓扑误差。
- 当前只证明局部前向原型和受控 MLP 基线可行，不能声称 PIML 已形成完整优化系统。

## 四、核心研究问题

1. 应学习 $\mathbf N^j$、$\mathbf K_s^j$、连续算子表示，还是它们的结构保持参数？
2. 如何严格或近似保证对称性、正定性、刚体模态、秩和能量一致性？
3. 局部算子误差如何传播到全局位移、柔顺度、灵敏度、Krylov 收敛和最终拓扑？
4. 监督、data-free 与混合训练在标签成本、结构性质和部署性能上如何比较？
5. 如何识别高风险子结构并自动回退精确消元？
6. 线性弹性之外，非线性状态变量和切线算子应如何进入“问题无关”的状态空间？

## 五、后续工作包

### WP-P1：统一基准与精确真值

- 固化二维/三维子结构、粗细网格比、材料参数和密度分布集合。
- 统一精确缩聚、形函数、位移恢复和局部谱指标的计算接口。
- 保留 MLP 作为最小可复现基线，避免模型复杂度掩盖数值问题。

### WP-P2：结构保持表示

- 比较直接预测 $K_s$、预测形函数后构造 $K_s$、因子化参数和谱修正路线。
- 将对称性、正定性、刚体模态、分区单位和能量一致性纳入训练或后处理。
- 明确哪些性质必须硬保证，哪些可以作为软约束和验收指标。

### WP-P3：误差传播与可信回退

- 建立
  $\|\widehat K_s-K_s\|\to\|\widehat u-u\|\to\|\widehat{\nabla J}-\nabla J\|\to$ 拓扑差异的量化链条。
- 记录预测误差对 CG/GMRES 迭代数和预条件后谱性质的影响。
- 建立局部误差指示器、不确定度或结构检查失败时的精确回退策略。

### WP-P4：灵敏度与优化闭环

- 补齐多尺度位移恢复、应变能和灵敏度计算。
- 接入 OC/MMA 与过滤流程，验证目标收敛、约束满足和拓扑稳定性。
- 比较纯精确、纯 PIML 和混合回退三种路径的误差—时间 Pareto 前沿。

### WP-P5：模型选型与扩展

- 在同一 predictor 接口下比较 MLP、DeepONet/operator learning 及必要候选模型。
- 不以局部 MSE 排名，统一比较结构性质、全局响应、求解器影响和部署成本。
- 在基础链路稳定后，再讨论复杂边界、非结构网格、非线性和多物理场扩展。

## 六、Benchmark 与验收指标

| 指标组 | 核心指标 |
|---|---|
| 局部精度 | $\|\widehat K_s-K_s\|_F/\|K_s\|_F$、形函数误差、能量误差、谱误差 |
| 结构性质 | 对称误差、SPD 通过率、最小特征值、刚体模态与分区单位误差 |
| 全局响应 | 位移、柔顺度、细尺度恢复和灵敏度误差 |
| 求解影响 | CG 是否中断、CG/GMRES 迭代数、残差历史和预条件后谱聚集 |
| 优化结果 | 目标与约束收敛、拓扑一致性、灰度和震荡情况 |
| 数据训练 | 标签生成成本、训练时间、参数量、FLOPs 和分布外退化 |
| 部署性能 | batch throughput、延迟、显存和端到端 solve 时间 |

验收原则：

- 所有模型必须通过同一精确真值、数据划分和全局求解接口评价。
- 任何局部误差数字必须同时说明它是否已传递到全局响应与优化结果。
- 最终输出 Pareto 前沿和适用条件，不输出脱离问题约束的单一“最佳模型”。

## 七、阶段性交付物

| 阶段 | 交付物 |
|---|---|
| 近期 | 精确缩聚与 MLP 基线、结构检查脚本、统一局部指标表 |
| 中期 | 结构保持 predictor、误差传播报告、可信回退原型 |
| 后期 | 灵敏度与拓扑优化闭环、模型选型 benchmark、非线性扩展设计 |

## 八、主要风险与回退

| 风险 | 回退策略 |
|---|---|
| 预测算子破坏 SPD 或刚体模态 | 因子化/谱修正；失败子结构回退精确消元 |
| 局部误差小但全局误差或迭代数恶化 | 将全局响应和求解器指标纳入训练选择，不只看 MSE |
| 每次调用推理成本过高 | 缓存 $K_s$、缓存压缩表示或采用混合按需策略 |
| 训练分布外退化 | 不确定度检测、主动补样和保守回退 |
| 非线性状态空间过大 | 先冻结线性弹性接口，再逐步加入状态变量和切线算子 |

## 九、跨技术线接口

- 向 Matrix-Free 提供批量局部算子、结构检查结果和可信回退接口。
- 向 GPU/HPC 提供固定形状 batch、模型计算图、精度策略和缓存需求。
- 从 Matrix-Free 接收全局残差、迭代数和谱信息，用于评价模型是否数值安全。
- 从 GPU/HPC 接收推理、局部作用和数据搬移成本，用于选择缓存或按需计算策略。
- 可被 PIML × Matrix-Free、PIML × MMC/MMV、非线性分析和其他后续课题复用。

## 十、证据与关联文档

- [[concepts/piml]] — PIML 概念说明。
- [[concepts/piml/method-lineage]] — 团队 PIML 方法谱系。
- [[literature/topology-opt/Huang2022-problemindependentmachine]] — EMsFEM-PIML 奠基工作。
- [[literature/topology-opt/Huang2023-PIML-substructure]] — 三维子结构 PIML。
- [[literature/topology-opt/Huang2024-PIML-datafree]] — mechanics-based data-free PIML。
- [[research/postdoc-plan/defense-sprint/direction-1-piml-matrix-free/frame7_piml_pipeline_guide]] — 当前原型数字与答辩证据。
- [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-gpu-and-model-selection-technical-synthesis]] — 模型选型与跨线综合。
- [[matrix-free-research-guide]]、[[gpu-hpc-research-guide]] — 另外两条长期技术线。
- [[_index]] — 长期技术线总入口。
