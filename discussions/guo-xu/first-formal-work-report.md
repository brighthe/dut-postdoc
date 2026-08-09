---
title: "第一次正式工作汇报：Matrix-Free 阶段结果与 PIML–GPU 研究任务"
aliases:
  - "discussions/guo-xu/2026-07-piml-matrix-free-gpu"
  - "2026-07-piml-matrix-free-gpu"
  - "discussions/guo-xu/2026-07-matrix-free-progress-piml-gpu-tasks"
  - "2026-07-matrix-free-progress-piml-gpu-tasks"
advisor: "郭旭"
report_period: "2026-07"
meeting_date: "待确定"
meeting_mode: "当面"
status: "preparing"
date_start: 2026-07-20
date_update: 2026-08-09
tags:
  - 工作汇报
  - PIML
  - Matrix-Free
  - GPU
  - 拓扑优化
topics:
  - "Matrix-Free 当前正式结果"
  - "PIML–Matrix-Free–GPU 研究衔接"
  - "下一步研究请教"
related:
  - "discussions/guo-xu/_index"
  - "concepts/piml/_index"
  - "concepts/matrix-free/_index"
  - "concepts/gpu-hpc/_index"
  - "research/technical-lines/matrix-free-research-guide"
  - "research/technical-lines/piml-research-guide"
  - "research/technical-lines/gpu-hpc-research-guide"
  - "research/piml-matrix-free-gpu/_index"
  - "research/piml-matrix-free-gpu/project-plan"
---

# 第一次正式工作汇报：Matrix-Free 阶段结果与 PIML–GPU 研究任务

郭老师，我已经将“面向大规模拓扑优化的 PIML Matrix-Free 求解与 GPU 协同加速方法研究”确定为博士后核心研究项目。现阶段优先推进 WP1：二维、三维线弹性 Matrix-Free 统一验证；二维、三维单 rank FA/EA 均已在 clean revision `608cedf25038ed690f6db3be5b3f24f92329c5ec` 形成可追溯数值证据。此后 Matrix-Free 接口仍有调整，当前目标 revision 尚待统一重放；WP2 的 PIML/GPU 和 WP3 的三线融合仍处于准备或门禁阶段，尚无可以作为本人阶段成果汇报的统一算例结果。

这次主要向您汇报我已经完成的工作和当前数值结果，说明三条技术线准备怎样衔接，并请您指导下一步优先解决的科学问题及第一阶段成果出口。

## 一、本次汇报的目标

总体研究目标是：

> 面向大规模拓扑优化，研究 PIML Matrix-Free 求解与 GPU 协同加速方法。

这条主线已经确定。本次希望进一步明确：

1. Matrix-Free 下一步优先补齐哪个装配层级、预条件和并行问题；
2. PIML 应首先学习什么局部力学对象，并用什么全局结果评价；
3. 三条技术线应从哪个接口开始连接，第一阶段优先形成什么论文成果。

## 二、我目前完成的工作

目前已经形成 revision-scoped 数值证据的技术工作是二维、三维线弹性 FA/EA CPU 单 rank 正确性验证。FA 形成全局稀疏矩阵并作为黄金参考；EA/EbE 缓存单元刚度，通过 gather、单元作用和 scatter-add 完成全局 MatVec。两组证据均来自 clean revision `608cedf25038ed690f6db3be5b3f24f92329c5ec`，`git_dirty=false`。

在 $8\times 8$、$16\times 16$ 和 $32\times 32$ 三档网格上，EA/FA 原始 MatVec 最大相对误差为 $1.63\times 10^{-16}$，CG 最大真相对残差为 $8.99\times 10^{-11}$，EA-CG/FA 最大解相对误差为 $8.88\times 10^{-12}$，制造解误差的观测收敛阶为 $1.94$ 和 $1.98$。结果来自 clean revision，能够追溯到代码版本、运行参数和原始产物。

三维采用 $4\times 4\times 4$、$8\times 8\times 8$ 和 $16\times 16\times 16$ 三档网格，EA/FA 原始 MatVec 最大相对误差为 $3.39\times 10^{-16}$，CG 最大真相对残差为 $9.27\times 10^{-11}$，EA-CG/FA 最大解相对误差为 $5.77\times 10^{-11}$，制造解误差的观测收敛阶为 $1.26$ 和 $1.68$。这些数值只代表上述 revision；后续接口变更尚未在新的 clean revision 上统一重放。

## 三、Matrix-Free 当前数值结果与证据边界

当前结果包括二维、三维 CPU 单 rank FA/EA 正确性基线。算例采用全 Dirichlet 制造解；EA 是不组装全局刚度矩阵的路径，FA 只作为同离散条件下的参考。

> **证据 provenance 警告（2026-08-09 复核）**：下面两张表的数值来自 revision `608cedf25038ed690f6db3be5b3f24f92329c5ec`，但 `soptx` 中对应的 `evidence/*.json` 此后已被 `4cd4e8da17189eb57f9a68cc316bcdf189c084ec` 上一次 **dirty worktree**（`git_dirty=true`）的运行覆盖，数值也略有变化（如二维 $8\times 8$ 的 CG 真相对残差由 $4.95\times 10^{-11}$ 变为 $5.13\times 10^{-11}$）。因此**本节表格当前无法回溯到仓库中任何一份文件**，且仓库里现存的也不是 clean-revision 正式 evidence。汇报前必须在冻结的 clean target revision 上重放并用新数值替换本节，否则不得对外表述为「已验证结果」。

### 二维 revision-scoped evidence

| 网格 | EA/FA 原始 MatVec 相对误差 | CG 真相对残差 | EA-CG/FA 解相对误差 | 制造解相对 $L^2$ 误差 |
|---|---:|---:|---:|---:|
| $8\times 8$ | $1.45\times 10^{-16}$ | $4.95\times 10^{-11}$ | $8.88\times 10^{-12}$ | $4.61\times 10^{-2}$ |
| $16\times 16$ | $1.63\times 10^{-16}$ | $8.99\times 10^{-11}$ | $6.68\times 10^{-12}$ | $1.20\times 10^{-2}$ |
| $32\times 32$ | $1.58\times 10^{-16}$ | $8.95\times 10^{-11}$ | $3.03\times 10^{-12}$ | $3.05\times 10^{-3}$ |

制造解误差的观测收敛阶约为 $1.94$ 和 $1.98$。这些结果说明二维 EA 与 FA 表示同一个离散线弹性算子，EA 能够在不组装全局刚度矩阵的条件下正确完成 MatVec 和 CG 求解。

### 三维 revision-scoped evidence

| 网格 | EA/FA 原始 MatVec 相对误差 | CG 真相对残差 | EA-CG/FA 解相对误差 | 制造解相对 $L^2$ 误差 |
|---|---:|---:|---:|---:|
| $4\times 4\times 4$ | $2.71\times 10^{-16}$ | $9.27\times 10^{-11}$ | $5.77\times 10^{-11}$ | $6.81\times 10^{-1}$ |
| $8\times 8\times 8$ | $3.18\times 10^{-16}$ | $6.70\times 10^{-11}$ | $1.94\times 10^{-11}$ | $2.85\times 10^{-1}$ |
| $16\times 16\times 16$ | $3.39\times 10^{-16}$ | $8.63\times 10^{-11}$ | $1.99\times 10^{-11}$ | $8.92\times 10^{-2}$ |

制造解误差的观测收敛阶约为 $1.26$ 和 $1.68$。这些结果说明在 revision `608cedf25038ed690f6db3be5b3f24f92329c5ec` 上，三维 EA 与 FA 的 MatVec 和求解结果一致；它们不自动代表后续接口调整后的当前 HEAD。

当前结果边界是：

- 本节表格绑定 revision `608cedf25038ed690f6db3be5b3f24f92329c5ec`，但仓库中对应的 evidence 文件已被 `4cd4e8d` 上的 dirty 运行覆盖；此后分布式求解器注册、CG 初值接口和多 rank FA 防误用等路径又发生过调整，当前目标 revision 尚待统一重放，重放前不存在可引用的正式 evidence；
- 二维、三维 1/2-rank 一致性尚未进入统一正式 evidence，不能作为并行扩展性结果；
- PA/QA、UA/NONE、预条件和性能对照尚未完成；
- GPU 尚无基于当前统一算例的正式结果。

证据 provenance、解释边界和重放后的正式数值以
`soptx:examples/matrix_free_elasticity/results_analysis.md` 为唯一事实源；
二维、三维精简证据文件分别位于：

`soptx:examples/matrix_free_elasticity/evidence/cpu-single-rank-fa-ea-2d.json`

`soptx:examples/matrix_free_elasticity/evidence/cpu-single-rank-fa-ea-3d.json`

（上述两份文件当前为 `git_dirty=true` 的开发证据，不可引用为正式结果。）

## 四、PIML–Matrix-Free–GPU 的研究衔接

我目前对三条技术线的衔接理解是：

```text
二维、三维 PIML 可复用局部力学表示／响应映射
        ↓
表示相适配的局部算子或局部作用接口
        ↓
Matrix-Free 全局算子作用与 Krylov 求解
        ↓
GPU 批量局部计算、scatter-add 和迭代求解
```

- **PIML** 负责构造可复用的局部力学表示或响应映射；多尺度形函数、缩聚刚度、Bézier 参数化子结构响应和超采样数值基函数是证据中出现的不同候选，不预设主次；
- **Matrix-Free** 负责在不组装完整全局矩阵的条件下完成全局算子作用和求解；
- **GPU** 负责批量局部计算、全局归约和 Krylov 过程的异构执行。

现有全文证据已经证明局部形函数或缩聚刚度可以进入大规模结构分析；新建 `draft` 文献入口又提供了等参几何输入、Bézier 边界位移参数化、重叠数值基函数和三维点阵应用等摘要级支线。它们均未给出 PIML–全局 Matrix-Free–GPU 闭环，Ma 2026 仍形成并组装全局粗网格矩阵。我的拟研究增量是筛选能够提供稳定全局算子接口的候选局部表示，进一步考察其能否直接进入算子级 Matrix-Free 求解，并在 GPU 上形成可验证的端到端计算链。

本轮新增的摘要级证据锚点为：[[../../literature/topology-opt/notes/Zhang2024-isoparametric-PIML|Zhang 2024 等参 PIML]]、[[../../literature/topology-opt/notes/Xu2025-PIML-lattice-MMC|Xu 2025 PIML–MMC 点阵]]、[[../../literature/topology-opt/notes/Guo2026-highgeneralization-bezier|Guo 2026 Bézier]] 和 [[../../literature/topology-opt/notes/Guo2026-PIML-OFEM|Guo 2026 PIML-OFEM]]。四篇均保持 `draft`，其中 PIML-OFEM 为 arXiv v1；这里不使用其全文级公式、实验数据或性能结论。

这仍是研究设想，不是已经完成的系统。当前尚未运行 PIML 程序，也没有 PIML 或 GPU 数值结果。

## 五、拟开展的下一步工作

1. **Matrix-Free**：先选定 clean target revision，统一重放二维、三维单 rank FA/EA，并固化 1/2-rank rank-invariance evidence 与 provenance；随后实现并验证 PA/QA，再研究 UA/NONE、预条件、更多 ranks 以及 Strong/Weak scaling。
2. **PIML**：分别建立二维、三维精确局部问题基线，以多尺度形函数、缩聚刚度及其他满足全局接口要求的表示为候选，统一真值、接口求解、必要的细尺度恢复与下游评价后再开展学习模型验证。
3. **GPU 与融合**：在单线正确性基线稳定后，先建立 Matrix-Free 单 GPU 完整求解，再接入 PIML 的批量局部预测和算子作用。

每一步都使用同一离散问题、精确参考和停止准则，先验证正确性和结构性质，再比较时间、内存和扩展性。

## 六、希望郭老师指导的问题

1. 在已经确定的博士后核心研究项目中，WP1 最值得聚焦的科学问题和论文出口是什么，WP2、WP3 应如何与之衔接？
2. 在先闭合二维、三维 1/2-rank rank invariance 的基础上，PA/QA 与预条件应如何组合成第一项可发表成果？首批结果应覆盖哪些算例、装配层级和并行规模？
3. 面向全局 Matrix-Free 接口，PIML 应如何从多尺度形函数、缩聚刚度及其他可复用局部力学表示中确定候选路线，并以结构性质、全局位移、柔顺度、必要的细尺度恢复和部署成本进行并列评价？

我希望通过这次交流，把三条技术线收敛为一个明确的首项研究任务，并确定下一次汇报需要带来的首个数值结果。
