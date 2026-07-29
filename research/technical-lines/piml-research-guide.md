---
title: "PIML 局部力学算子技术线研究指南"
topic: "PIML 技术线的已有能力、目标差距、实施路线与阶段完成边界"
tags:
  - technical-line
  - research-guide
  - PIML
  - substructuring
  - operator-learning
  - topology-optimization
status: "in-progress"
date_start: 2026-07-21
date_update: 2026-07-29
related:
  - piml/mathematical-foundations
  - method-lineage
  - ../workflows/pinn-machine-learning-workflow
  - piml-matrix-free-gpu-and-model-selection-technical-synthesis
---

# PIML 局部力学算子技术线研究指南

> **定位**：本页是 PIML 技术线的长期第一入口，集中回答“目前已经具备什么能力、距离最终目标还有什么差距、下一步如何推进以及何时可以标记完成”。PIML 的问题无关性定义、子结构缩聚记法与学习映射见 [[../../concepts/piml/mathematical-foundations]]，方法谱系见 [[../../concepts/piml/method-lineage]]。
>
> **当前主要研究对象**：以二维 Q4、平面应力子结构作为首个统一参考问题，粗网格 $8\times8$、子结构内细分 $L=5$ 与 $L=10$ 两档；三维、非结构网格与非线性状态变量仅作为后续扩展方向。
>
> **当前事实底线**：已跑通子结构缩聚与极小 MLP 预测局部 $K_s$ 的前向原型，但原型代码和结果记录位置尚未恢复，当前仍缺少可重放的线弹性 PIML 训练入口。结构保持参数化、全局误差传播、多尺度灵敏度和拓扑优化闭环尚未完成。

## 一、技术线目标与边界

最终目标不是直接预测某个给定载荷和边界条件下的拓扑，而是学习可在多个整体问题中复用的局部力学表示——多尺度形函数 $\mathbf N^j$ 或缩聚刚度 $\mathbf K_s^j$——并保证它进入结构分析与优化后仍然可信。

| 维度 | 最终目标 |
|---|---|
| 学习对象 | $\mathbf N^j$、$\mathbf K_s^j$、连续算子表示及其结构保持参数可统一描述、切换和比较 |
| 结构保持 | 对称性、SPD、刚体模态、分区单位和能量一致性有明确的硬保证与软约束划分 |
| predictor 接口 | 输入、输出、结构检查、回退和评价字段语义统一并冻结 |
| 误差传播 | 局部误差 → 位移 → 柔顺度 → 灵敏度 → 拓扑的量化链条闭合 |
| 可信回退 | 结构检查失败或不确定度过高时自动回退精确消元 |
| 训练范式 | 监督、data-free 与 operator learning 在同一接口下可比 |
| 优化闭环 | 多尺度恢复、灵敏度、OC/MMA 与过滤全流程跑通并验证拓扑稳定性 |

本技术线负责局部算子的学习映射、结构保持、误差传播、可信回退和统一评价，并向 Matrix-Free 提供批量局部算子与结构检查结果、向 GPU/HPC 提供固定形状 batch 与缓存需求。全局无矩阵作用、Krylov 与预条件见 [[matrix-free-research-guide]]，GPU 内核与端到端性能见 [[gpu-hpc-research-guide]]，数学定义与方法谱系见对应概念页；某个阶段性课题如何组合三条线由计划与综合页维护。

### 核心研究问题

1. 应学习 $\mathbf N^j$、$\mathbf K_s^j$、连续算子表示，还是它们的结构保持参数？
2. 如何严格或近似保证对称性、正定性、刚体模态、秩和能量一致性？
3. 局部误差如何传播到全局位移、柔顺度、灵敏度、Krylov 收敛和最终拓扑？
4. 监督、data-free 与混合训练在标签成本、结构性质和部署性能上如何比较？
5. 如何识别高风险子结构并自动回退精确消元？
6. 线性弹性之外，非线性状态变量和切线算子如何进入“问题无关”的状态空间？

问题 1 的对照端是 [[../../literature/topology-opt/Lei2018-machinelearningdriven]] 代表的问题相关直接预测（载荷参数 → MMC 设计变量 → 最终构型）。它与本技术线的分界正是“学最终设计”与“学可复用局部算子”，谱系定位见 [[../../concepts/piml/method-lineage]] §3。

## 二、当前已有基础

| 基础 | 已经做到的内容 | 当前边界 |
|---|---|---|
| 精确子结构前向链路 | 已跑通“局部细尺度密度 → 静力缩聚 → $K_s^j$ → 全局接口缩聚方程 → 接口求解/细尺度恢复”；与全尺度 Schur 补误差达 $10^{-15}$ 量级，接口解与全尺度直解一致到 $10^{-14}$–$10^{-12}$ | 属精确基线，反映实现正确与浮点舍入，**不是 PIML 预测误差**；仅覆盖二维 Q4、平面应力、单一悬臂算例 |
| PIML 预测原型 | 极小 MLP 直接预测局部 $K_s$，逐子结构相对误差均值 $5\times5$ 为 $1.6\times10^{-3}$、$10\times10$ 为 $8.2\times10^{-3}$，两档均优于局部平均密度 Mock 对照；已有 `ExactPredictor`/`MockPredictor`/`TrainedPredictor` 共用调用接口 | 2026-07-03 实测，事实入口见 §六；原型代码路径待确认；只学 $K_s$、无结构保持参数化；**只是局部误差**，未传播到位移、柔顺度或灵敏度 |
| 团队公开方法基础 | Huang 2022/2023/2024 与 Ma 2026 已形成可核实的方法谱系与数学基础页 | 属可复用基础，不等于本技术线已完成对应实现 |

团队 PIML 主线是“EMsFEM 形函数学习 → 子结构形函数/缩聚刚度学习 → mechanics-based data-free 训练 → 并行与按需预测的大规模实现”，长期演进统一维护在 [[../../concepts/piml/method-lineage]]，本页不建第二份谱系。本技术线的接续任务是补齐该谱系尚未闭合的环节：结构保持的硬性参数化、误差到全局响应与灵敏度的量化传播、可信回退，以及多 predictor 的同口径选型；这是拟推进方向，不能写成团队已完成的公开成果。

## 三、当前成果边界

### 已完成

- 精确子结构缩聚链路与全尺度 Schur 补在机器精度上一致，可作为后续所有预测路线的真值基线。
- 极小 MLP 基线已产出真实局部 $K_s$ 预测误差，两档粗细比均明显优于 Mock 对照。

### 部分完成或待核实

- 数值有活跃事实入口，但原型代码与结果记录文件的本地位置未核实，当前不具备可重放入口。
- 预测误差随粗细比、密度分布和子结构类型的稳定性未系统验证；两档结果来自同一受控网络容量与训练量。
- 预测算子的对称性、SPD、刚体模态和能量一致性未测量，只有回归意义上的相对误差。

### 尚未完成

- 尚未形成结构保持的参数化表示或后处理修正，也未冻结 predictor 的检查、回退与评价字段。
- 尚未建立局部误差到位移、柔顺度、灵敏度和拓扑的量化传播链条，以及误差指示器与精确回退机制。
- 尚未补齐多尺度位移恢复、灵敏度计算与 OC/MMA 优化闭环。
- 尚未在统一接口下比较 MLP 之外的模型，也未扩展到三维、非结构网格与非线性。

当前只证明局部前向原型和受控 MLP 基线可行，不能声称 PIML 已形成完整优化系统。

## 四、目标与当前差距

| 能力维度 | 当前状态 | 下一道关键门槛 |
|---|---|---|
| 训练工具链 | 默认一维 Poisson PINN 已实测运行，并已形成 [[../workflows/pinn-machine-learning-workflow\|PINN 机器学习全过程]]；当前软件源码映射见其附录，seed、精确 history、checkpoint、干净 revision 与重复运行仍未冻结 | 先完成 Poisson PINN 可重放门禁，再把同一训练骨架切换到线弹性问题；该工具链证据不计作 PIML 方法进展 |
| 参考基准 | 单一二维悬臂算例，两档粗细比 | 冻结二维/三维子结构、粗细网格比、材料参数与密度分布集合 |
| 学习对象 | 只直接预测 $K_s$ | 建立预测 $\mathbf N^j$、预测 $\mathbf K_s^j$、因子化参数三条路线的同口径比较 |
| 结构保持 | 未纳入训练或后处理 | 明确硬保证与软约束划分，报告刚体模态残差与去刚体子空间最小特征值 |
| predictor 接口 | 三实现共用调用接口 | 补齐并冻结结构检查、回退与评价字段，成为跨模型正式契约 |
| 误差传播 | 只有局部 $K_s$ 误差 | 先打通到位移与柔顺度，再到灵敏度 |
| 可信回退 | 无 | 建立局部误差指示器与精确消元回退路径 |
| 优化闭环 | 未接入 | 接入 OC/MMA 与过滤，验证目标收敛与拓扑稳定性 |
| 模型选型 | 仅极小 MLP | 在同一接口下比较 DeepONet 与 operator learning |
| 事实源 | 原型仓库路径待确认 | 定位并恢复原型代码与 `frame7_piml_pipeline_results.md` |

当前最优先的工作不是增加模型复杂度，而是先把可重放的训练环境和精确真值基线立起来；在基线可复现之前，任何新模型的比较结果都缺乏可核对的参照。

## 五、下一步实施路线

### 阶段 1：理解并冻结一维 Poisson PINN 训练工具链

- 以 `fealpy:example/ml/poisson_pinn_example.py` 和 `fealpy:fealpy/ml/poisson_pinn_model.py` 为入口，按 [[../workflows/pinn-machine-learning-workflow]] 说明默认一维 Poisson 问题、MLP、配点、自动微分、PDE/边界 residual、加权 loss、反向传播、误差估计和绘图。
- 2026-07-29 的当前单次运行观察为：loss `49.431482 → 5.62×10^-4`，21 个日志点中的最低值为 `2.25×10^-4`，程序训练计时 `7.580 s`；图中最低 $L^2$ error 约 $8\times10^{-5}$，只作为估读值。
- **定位边界**：该算例学习特定 Poisson 边值问题的解场，只用于理解和验证 PINN 训练工具链，不是 Problem-Independent PIML；运行结果不得表述为 PIML 方法能力进展。
- **门禁**：冻结 Python、PyTorch、FEALPy revision、device、dtype、完整配置、全部 seed 与唯一运行命令；精确 history/metrics 落盘，保存 best/last checkpoint；在干净 revision 上重复运行并满足预先定义的一致性容差。当前尚未满足这些条件，阶段 1 保持未完成。

### 阶段 2：恢复原型并冻结基准与精确真值

- 起点是：算例设置与数值结论已有活跃事实入口，但原型仓库路径待确认，`frame7_piml_pipeline_results.md` 与 `train_piml_predictor.py` 位置未核实，历史记录指向分支 `codex/piml-multiscale-prototype`；这些是待处理项，不是已完成结果。
- 定位并恢复原型代码与结果记录，固化子结构、粗细网格比、材料参数和密度分布集合；统一精确缩聚、形函数、位移恢复与局部谱指标接口，保留极小 MLP 作为最小可复现基线。
- **门禁**：精确缩聚与全尺度 Schur 补误差复现到 $10^{-15}$ 量级；MLP 基线复现到 $1.6\times10^{-3}$（$5\times5$）与 $8.2\times10^{-3}$（$10\times10$）。任一项未复现则阶段保持未完成并进入诊断。

### 阶段 3：结构保持表示与接口冻结

- 比较直接预测 $K_s$、预测形函数后构造 $K_s$、因子化参数与谱修正四条路线，将对称性、刚体零空间、变形子空间正定性、分区单位和能量一致性纳入训练或后处理，明确哪些硬保证、哪些为软约束。
- 冻结 predictor 的输入、输出、结构检查、回退与评价字段，形成后续所有模型共用的接口契约。
- **门禁**：对称性、刚体模态残差、投影子空间最小特征值和能量一致性达到约定阈值，局部精度不劣于阶段 2 基线；接口字段冻结并可被至少两种 predictor 实现。

### 阶段 4：误差传播与可信回退

- 建立 $\|\widehat K_s-K_s\|\to\|\widehat u-u\|\to\|\widehat{\nabla J}-\nabla J\|\to$ 拓扑差异的量化链条，并记录预测误差对 CG/GMRES 迭代数与预条件后谱性质的影响。
- 建立局部误差指示器、不确定度估计或结构检查失败时的精确回退策略。
- **门禁**：链条各环节均为可复现测量而非估计；回退触发率、触发条件和额外代价可报告。

### 阶段 5：灵敏度与优化闭环

- 补齐多尺度位移恢复、应变能和灵敏度计算，接入 OC/MMA 与过滤流程。
- 比较纯精确、纯 PIML 和混合回退三种路径的误差—时间 Pareto 前沿。
- **门禁**：完成完整优化迭代并给出与精确路径的拓扑一致性判断；三条路径 Pareto 前沿可复现。

### 阶段 6：模型选型与扩展

- 在同一 predictor 接口下比较 MLP、DeepONet/operator learning 及必要候选模型，统一比较结构性质、全局响应、求解器影响和部署成本，不以局部 MSE 排名。
- 选型比较需以问题相关直接预测范式为对照端，依据见 [[../../literature/topology-opt/Lei2018-machinelearningdriven]]（精读已完成，2026-06-24）；团队谱系文献仅剩 Zhang 2024（复杂设计域 PIML）待读，空档见 [[../../concepts/piml/method-lineage]] 时间线。
- 基础链路稳定后再讨论复杂边界、非结构网格、非线性和多物理场扩展。
- **门禁**：所有候选通过同一真值、数据划分和全局接口评价，并同时报告标签成本、训练时间与推理开销；输出适用条件与 Pareto 前沿，而非单一“最佳模型”。

各阶段只有在具备可重放入口、明确事实来源并通过对应门禁后才能标记为“已完成”。**局部 MSE 达标不等于阶段完成**，缺少结构性质、全局响应或求解器影响的结果只能作为局部证据；任何局部误差数字都必须同时说明它是否已传递到全局响应与优化结果。

回退原则：预测算子破坏 SPD 或刚体模态时采用因子化/谱修正，失败子结构回退精确消元；局部误差小但全局响应或迭代数恶化时，把全局指标纳入模型选择；推理成本过高时缓存 $K_s$、缓存压缩表示或与局部作用融合；训练分布外退化时用不确定度检测与主动补样；若原型事实源长期无法恢复，则以精确缩聚公式重建基线并重新训练，明确标注与历史数字的可比性边界。

## 六、事实来源与关联页面

- [[../workflows/pinn-machine-learning-workflow]] — 一维 Poisson PINN 机器学习全过程；当前软件源码映射见附录，只承担训练工具链学习，不是 PIML 方法来源。
- [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-gpu-and-model-selection-technical-synthesis]] §2.1 — PIML 子结构前向原型在本仓库中的**活跃事实入口**，本页数值以其为准；该页也维护模型选型与跨线综合。
- PIML 原型代码、`frame7_piml_pipeline_results.md`、`train_piml_predictor.py` — **本地路径待确认**；历史准备材料见 [[archive/2026-postdoc-entry-assessment/README]] 的 frame7（2026-07-03 实测），归档内容不作为当前事实源。
- 本技术线不以 `C:\workspace\mfleo` 或 `C:\workspace\xihe` 为事实源，两者见 [[matrix-free-research-guide]]。
- [[../../concepts/piml/mathematical-foundations]]、[[../../concepts/piml/method-lineage]] — 数学定义与方法谱系。
- [[../../literature/topology-opt/Huang2022-problemindependentmachine]]、[[../../literature/topology-opt/Huang2023-PIML-substructure]]、[[../../literature/topology-opt/Huang2024-PIML-datafree]] — EMsFEM-PIML、三维子结构与 data-free 三篇奠基文献。
- [[../../literature/topology-opt/Lei2018-machinelearningdriven]] — MMC + SVR/KNN 的问题相关直接预测，谱系前史与阶段 6 的选型对照端。
- [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] — 第一次线下汇报中的 PIML 摘要。
- [[matrix-free-research-guide]]、[[gpu-hpc-research-guide]]、[[_index]] — 另两条技术线与总入口。
