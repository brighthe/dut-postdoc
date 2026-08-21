---
title: "面向大规模拓扑优化的 PIML Matrix-Free 求解与 GPU 协同加速研究综述"
aliases:
  - "面向大规模结构拓扑优化的 PIML 与 Matrix-Free 高性能求解方法"
  - "面向大规模拓扑优化的结构保持 PIML、Matrix-Free 与 GPU 融合研究综述"
  - research/piml-matrix-free/piml-matrix-free-high-performance-solver-survey
  - research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-high-performance-solver-survey
tags:
  - PIML
  - matrix-free
  - topology-optimization
  - substructuring
  - multigrid
  - PETSc
  - parallel-computing
  - GPU
  - high-performance-computing
status: "in-progress"
date: 2026-06-07
date_update: 2026-08-13
source: "郭旭老师团队在大规模结构拓扑优化中 PIML 与 Matrix-Free 高性能求解的研究报告.pdf"
---

# 面向大规模拓扑优化的 PIML Matrix-Free 求解与 GPU 协同加速研究综述

> 本页是 [[_index|博士后核心研究项目]]的跨线综合事实源，维护三线交叉现状、证据成熟度、耦合机制、待验证研究假设、统一研究方案和验证协议。项目目标、WP1–WP3、门禁关系与状态由 [[project-plan]] 维护；单线方法与证据由对应 technical-line guide 维护，具体算例、命令和运行 evidence 由对应软件仓库维护。本页冻结融合研究的数学接口、方法对照和评价契约，不建立第二套低层任务账。

## 一、研究问题与范围

大规模拓扑优化需要在材料演化中反复完成结构分析、灵敏度计算和设计更新。本项目关注的核心问题是：

> 如何将 PIML 生成的局部力学表示重构为全局 Matrix-Free 算子作用，并协同组织 GPU 上的预测、局部作用和预条件 Krylov 求解，使其在保持可靠性的同时扩展可解规模并获得端到端收益？

当前范围限定为二维／三维线弹性拓扑优化；本页未加限定的 PIML 均指 Problem-Independent Machine Learning（问题无关机器学习）。局部学习对象采用“可复用局部力学表示”的上位口径，多尺度形函数 $\mathbf N$、缩聚刚度 $\mathbf K_s$ 及其他满足问题无关性和全局接口要求的表示均可作为候选，不预设主次；全局求解采用 Krylov 方法及适用预条件器。单线定义和证据分别见 [[../technical-lines/piml-research-guide]]、[[../technical-lines/matrix-free-research-guide]] 与 [[../technical-lines/gpu-hpc-research-guide]]；稳定概念见 `concepts/`，单篇证据见 `literature/`。本页不维护代码 Todo、实验结果、基金批次状态，也不展开 [[../mmc-mmv/mmc-mmv-numerical-discretization-survey|MMC/MMV]] 的独立问题。

## 二、跨线方法关系与关键事实边界

### 2.1 三条技术线的关系

| 技术线 | 在融合链中的作用 | 主要新增风险 | 单线事实源 |
|---|---|---|---|
| PIML | 生成可复用局部力学表示；具体输出由证据和接口要求确定 | 局部误差和表示特有的结构破坏可能放大全局误差 | [[../technical-lines/piml-research-guide]] |
| Matrix-Free | 决定全局算子保存、重算和作用方式 | 预条件困难，迭代增长可能抵消 MatVec 收益 | [[../technical-lines/matrix-free-research-guide]] |
| GPU/HPC | 执行批量推理、局部作用、归约和通信 | 搬运、scatter-add、同步和粗网格可能成为瓶颈 | [[../technical-lines/gpu-hpc-research-guide]] |

### 2.2 关键事实边界

1. Huang–Ma 路线已覆盖局部形函数／缩聚算子学习，但 Ma 2026 仍形成并组装全局粗尺度矩阵，不等于全局 Matrix-Free。
2. Zhang 2024、Xu 2025、Guo 2026 Bézier 与 PIML-OFEM 扩展了几何输入、边界参数化、重叠数值基函数和应用对象；四篇当前均为元数据／摘要级 `draft` 证据，仍未提供全局 Matrix-Free/GPU 闭环。
3. 不组装全局矩阵不自动产生端到端优势，必须计入局部重算、预条件和完整 solve／优化成本。
4. GPU kernel 加速不等于完整流程加速，必须计入搬运、推理、归约、同步和回退。
5. 较小的局部表示误差不能替代真残差、响应、灵敏度和最终拓扑评价。
6. 三线融合目前是研究目标而非已有成果；WP3 状态以 [[project-plan#三、工作包与依赖|项目计划]]为准。

### 2.3 三线交叉证据成熟度矩阵

下表只评价当前仓库已核验的核心证据。“直接证据”来自论文自身，“跨源归纳”是组合判断，“待验证假设”不是既有成果。

| 证据层级 | 代表证据 | PIML | 全局 MF | GPU | 预条件 | 完整 TO | 性质与边界 |
|---|---|---:|---:|---:|---:|---:|---|
| 精确局部算子 + MF + GPU | Schmidt–Schulz、Martínez-Frutos、CEED | 否 | 是 | 是 | 部分 | 是／部分 | **直接证据**；不支持学习算子或回退 |
| PIML 表示／应用扩展 + 组装式全局流程 | Huang 2022/2023/2024、Zhang 2024、Xu 2025、Ma 2026、Guo 2026 Bézier、PIML-OFEM | 是 | 否 | 否 | 部分工作涉及 MG-GMRES | 是／部分 | **全文直接证据 + 摘要级补充**；新四篇仍为 `draft`，未形成三线闭环 |
| Physics-Informed／结构化学习 | PINN、DeepONet、SPD-NN、PINNTO、Huang–Ma | 部分 | 否 | 非核心 | 否 | 部分 | **直接证据 + 类比边界**；不能推出统一结构保持 |
| PIML + 全局 MF + GPU 协同执行 | 当前核心证据中尚无直接闭环锚点 | 待验证 | 待验证 | 待验证 | 待验证 | 待验证 | **待验证假设**；不作全球绝对空白判断 |

## 三、开放科学问题

| 交叉问题 | 需要回答的核心关系 | 最小证据 |
|---|---|---|
| PIML 全局求解的 MF 重构 | 可复用局部力学表示如何转化为不组装全局系统矩阵的算子作用，并保持与自由度映射、全局平衡和拓扑更新一致？ | 算子作用对照、结构性质、矩阵形成与存储 |
| MF 预条件、收敛与可靠性 | 近似局部算子、代理预条件器复用与更新、结构检查和精确回退如何共同决定真残差及 Krylov 收敛？ | 结构检查、迭代数、更新时间和回退率 |
| GPU 协同数据流与端到端收益 | 批量预测、局部作用、gather/scatter、向量归约、预条件和缓存—重算如何共同决定收益？ | 时间／显存分解与完整 solve／优化结果 |
| 局部误差向求解和拓扑传播 | 局部表示误差如何传递到位移、柔顺度、灵敏度和最终拓扑，并界定融合方法的适用条件？ | 受控扰动与局部—全局误差关系 |

非线性、接触和多物理场会引入状态与路径依赖，不能直接沿用线弹性结论；只有当前二维／三维线弹性证据链闭合后，才重新定义其学习对象、结构条件和更新策略。

## 四、研究假设、统一研究方案与验证协议

### 4.1 待验证研究假设

1. 将 PIML 局部表示重构为全局 Matrix-Free 算子作用可以降低矩阵形成与存储开销，但其有效性取决于局部计算、全局累加、预条件和迭代增长后的完整成本。
2. GPU 上的批量预测—局部作用—Krylov 协同执行只有在计入搬运、gather/scatter、归约、预条件和回退后仍降低完整成本，才构成有效加速。
3. 结构检查、分布外识别和逐子结构精确回退可以控制全局误差，但有效性取决于回退率、额外成本和结果改善。
4. Matrix-Free 主算子与低频更新的组装代理预条件器，可能比追求“完全无矩阵”形成更合理的迭代数—更新时间—内存折中。

### 4.2 统一问题、记号与局部—全局算子关系

当前统一对象为二维／三维线弹性密度型拓扑优化。在线弹性控制方程、有限元离散和材料插值冻结后，将状态方程与柔顺度型问题概括为

$$
\mathbf A(\boldsymbol\rho)\mathbf u=\mathbf f,
\qquad
\min_{\boldsymbol\rho}\;J(\boldsymbol\rho)=\mathbf f^{\mathsf T}\mathbf u,
\quad
V(\boldsymbol\rho)\leq \bar V,
$$

其中 $\boldsymbol\rho$ 为设计变量，具体插值、约束、过滤和优化器由比较契约冻结，不由本页重新定义；线弹性数学基础见 [[../../concepts/linear-elasticity]]。

对局部区域 $j$，以 $\boldsymbol\rho^j$ 表示局部材料状态，$\mathcal Q^j$ 表示可复用局部力学表示，$\mathbf A_j^\star$ 表示精确局部算子，$\widehat{\mathcal Q}^j$ 与 $\widehat{\mathbf A}_j$ 分别表示 PIML 近似表示及由其得到的局部算子。$\mathbf G_j$ 是全局自由度到局部自由度的限制算子。精确和近似的全局作用分别写为

$$
\mathbf A^\star\mathbf x
=\sum_j\mathbf G_j^{\mathsf T}\mathbf A_j^\star\mathbf G_j\mathbf x,
\qquad
\widehat{\mathbf A}\mathbf x
=\sum_j\mathbf G_j^{\mathsf T}\widehat{\mathbf A}_j\mathbf G_j\mathbf x.
$$

上述求和在实现中按“限制／gather—局部作用—回填／scatter-add”执行，不要求形成全局矩阵。若使用精确局部算子，Matrix-Free 只是同一离散算子的执行方式，不引入模型近似；由 $\mathbf A_j^\star$ 替换为 $\widehat{\mathbf A}_j$ 才产生局部近似及全局算子扰动。多尺度形函数 $\mathbf N$、缩聚刚度 $\mathbf K_s$ 及其他满足问题无关性与全局接口要求的表示均属于 $\mathcal Q^j$ 的候选实现，不预设主次。

### 4.3 跨技术线的概念接口契约

本节冻结研究级输入输出语义，不规定 Python／C++ 类名、函数签名或具体软件 API。三条技术线在进入融合实验前必须能够提供下列共同语义：

| 接口环节 | 输入 | 输出与不变量 | 事实所有权 |
|---|---|---|---|
| 局部状态 | $\boldsymbol\rho^j$、局部类型、几何／离散标识、dtype、device 和版本信息 | 可追溯且可批处理的局部状态；不同 PDE、离散或材料模型不得静默复用 | [[../technical-lines/piml-research-guide\|PIML guide]] |
| 构造／预测与 `update` | 局部状态、缓存状态和更新策略 | 精确或 PIML 局部表示、缓存键、来源标识与更新时间 | [[../technical-lines/piml-research-guide\|PIML guide]]／[[../technical-lines/gpu-hpc-research-guide\|GPU/HPC guide]] |
| `apply`／`diagonal` | 局部表示或局部状态、局部向量 | 局部算子作用及预条件所需对角／块信息；保存对象与装配层级明确 | [[../technical-lines/matrix-free-research-guide\|Matrix-Free guide]] |
| `check`／误差指示 | 局部表示、结构条件、训练分布和可选精确样本 | 表示相适配的结构诊断、分布外标志、误差指示和可执行处置 | [[../technical-lines/piml-research-guide\|PIML guide]] |
| `fallback` | 失败标志、局部状态与精度要求 | 精确局部算子或精确局部作用，并记录触发原因与代价 | [[../technical-lines/piml-research-guide\|PIML guide]]／[[../technical-lines/matrix-free-research-guide\|Matrix-Free guide]] |
| 恢复与灵敏度 | 全局／接口解、局部表示和设计状态 | 必要的细尺度恢复、能量和灵敏度贡献；与参考路径采用同一定义 | [[../technical-lines/piml-research-guide\|PIML guide]]／[[project-plan\|项目拓扑优化流程]] |
| 诊断与 provenance | 方法、硬件、配置和运行状态 | 残差、迭代、时间、内存、回退率、代码 revision 与环境记录 | [[../technical-lines/gpu-hpc-research-guide\|GPU/HPC guide]] 与软件 evidence |

### 4.4 阶段路线、输入输出与门禁

项目依赖保持为 `WP1 ∥ WP2 → WP3`。工作包的当前状态、启动／完成边界与详细事实源以 [[project-plan#三、工作包与依赖|项目计划]] 为准；本节只保留跨线交接所需的输入、阶段输出与门禁。

| 阶段 | 输入 | 阶段输出 | 门禁与停止条件 |
|---|---|---|---|
| WP1：精确 Matrix-Free/GPU 基线 | 冻结的二维／三维问题、可承受规模的精确组装参考及已验真的精确 Matrix-Free 参考 | 统一 `update/apply/diagonal` 语义、正确性、真残差、完整 solve 时间和峰值内存 evidence | 算子、边界、真残差、响应或可重放性未通过时停止，不接入 PIML |
| WP2：PIML/GPU 局部表示 | 精确局部真值、问题契约和候选表示 | 可重放的二维／三维局部表示 provider 及结构、误差、吞吐和内存 evidence | 只达到局部 MSE、缺少结构检查或不能精确回退时停止，不接入全局 Matrix-Free |
| WP3：PIML Matrix-Free/GPU 融合 | 通过门禁的 WP1 算子／求解接口和 WP2 局部表示接口 | 统一结构分析与拓扑优化对照、误差传播、完整时间—内存和适用范围 evidence | 未同时满足精度、真残差、收敛和统一计时边界时不形成端到端收益结论 |

单次算例成功、程序能够连接或基金申请完成均不能解除门禁。若某候选表示或执行策略被最小实验否定，保留失败证据并停止该分支，不通过扩大算例或放宽正确性标准掩盖失败。

### 4.5 “局部算子来源 × 全局执行路径”二维对照契约

主对照矩阵将“局部算子从哪里来”和“全局算子如何执行”正交分开，不再把表示路线与执行路线混合编号：

| 局部算子来源 × 全局执行路径 | 显式组装参考 | Matrix-Free CPU | Matrix-Free GPU |
|---|---|---|---|
| 精确局部算子 | 黄金参考；提供响应、灵敏度、拓扑和可承受规模的时间／内存基线 | 分离 Matrix-Free 对正确性、迭代和内存的影响 | 分离 GPU 执行、数据移动和同步的影响 |
| PIML 候选局部表示 | PIML 组装式参考；分离局部近似与 Matrix-Free 的影响 | 研究局部误差、算子性质、预条件和 Krylov 耦合 | 研究批量预测、局部作用和预条件迭代的端到端协同 |
| PIML／精确混合回退 | 评价回退语义与全局响应改善的参考 | 评价分布外识别、回退率和迭代取舍 | 评价可靠性机制的时间—显存—精度综合代价 |

每次实验只允许在主矩阵上改变一个核心因素。下列维度作为独立控制轴记录，不再与主路径编号混合：

| 控制轴 | 候选设置 | 比较要求 |
|---|---|---|
| 局部表示 | $\mathbf N$、$\mathbf K_s$ 或其他通过证据筛选的表示 | 共享问题、精确真值、数据划分和下游评价，不预设优先级 |
| 预条件 | 对角／块、组装代理及其复用、局部更新或重建 | 主算子与预条件器分别注明装配层级，完整计入 setup／update 成本 |
| PIML 数据策略 | 缓存局部表示、按需预测、预测—局部作用融合 | 共享 predictor、精度、停止准则和完整 solve 接口 |
| 数值精度 | FP64 基线，条件性比较 FP32 或混合精度 | 同时检查结构性质、平衡残差、迭代数和优化结果 |
| 可靠性 | 无回退基线、结构／分布检查、局部精确回退 | 报告触发原因、回退比例、结果改善和额外成本 |

### 4.6 误差、残差、可靠性与处置协议

| 层级 | 必须区分和记录的量 | 作用 |
|---|---|---|
| 局部表示误差 | 与具体 $\mathcal Q^j$ 对应的误差，以及对称性、半正定或约束后正定性、刚体模态、完备性、能量一致性等必要条件 | 判断候选表示是否具备进入全局求解的基本条件 |
| 算子作用误差 | 代表向量或受控扰动下 $\|(\widehat{\mathbf A}-\mathbf A^\star)\mathbf x\|/\|\mathbf A^\star\mathbf x\|$ | 连接局部近似与全局算子扰动，不以局部 MSE 替代 |
| Krylov 递推残差 | 求解器内部更新的残差及其收敛历史 | 判断近似算子上的迭代行为 |
| 精确平衡残差 | $\mathbf r_{\mathrm{eq}}=\mathbf f-\mathbf A^\star\widehat{\mathbf u}$，由精确局部算子的 Matrix-Free 作用复核 | 防止近似算子上的收敛判定掩盖原离散平衡误差 |
| 响应与优化误差 | 位移、柔顺度、灵敏度、约束、目标收敛和最终拓扑差异 | 判断局部加速是否改变工程与优化结论 |

可靠性机制使用“检测—处置—复核”闭环，具体阈值由预实验和统一真值确定，不在研究设计阶段预设为已验证常数：

| 触发类型 | 处置 | 必须复核 |
|---|---|---|
| 分布外、结构检查失败或误差指示超限 | 对相应局部区域执行精确构造／作用，并记录回退原因 | 局部结构、平衡残差、响应改善、回退率和额外时间／显存 |
| 递推残差与精确平衡残差失配 | 提高精确回退比例，必要时停止近似求解路径 | 精确平衡残差和响应误差是否恢复 |
| Krylov 迭代增长或预条件质量退化 | 依次比较预条件器复用、局部更新和重建 | 迭代数、更新时间、完整 solve 与峰值内存 |
| GPU 调度、同步或显存成为瓶颈 | 在缓存、按需预测、融合、流式 batch 或分区执行间切换 | 端到端时间、峰值显存和数值结果保持情况 |

### 4.7 GPU 协同执行与端到端性能协议

异构执行模式的稳定分类（硬件拓扑、执行层级、编程模型、数据/精度策略）见 [[../../concepts/gpu-hpc/heterogeneous-execution-modes]]；本节冻结本项目在其中的取值组合与比较协议。

GPU 路径覆盖“局部特征构造—批量预测—局部作用—gather/scatter—Krylov 向量运算—归约—预条件”，而不是只迁移神经网络推理。统一比较三种数据策略：

| 策略 | 主要收益 | 主要代价与适用条件 |
|---|---|---|
| 预测并缓存局部表示 | 减少重复推理和局部构造 | 增加显存、缓存失效与拓扑更新成本 |
| 每次作用按需预测 | 减少持久存储，适合显存受限 | 增加推理次数；只有重计算低于存储和搬移代价时才可能受益 |
| 预测—局部作用融合 | 减少中间写回、launch 和显存占用 | 增加实现复杂度与寄存器／工作区压力，必须以完整 solve 验证 |

计时与资源报告遵循 [[../../concepts/gpu-hpc/performance-model]] 的 kernel、MatVec、solve、优化迭代和完整任务五级边界。CPU/GPU 对照统一离散、输入、dtype、停止准则、硬件说明、预热与同步语义；离线训练、精确真值生成、在线预测、预条件 setup／update、完整求解和完整优化分别统计。算法、装配层级、精度和硬件同时改变时称为联合收益，不把结果单独归因于 GPU。多 GPU、GPU-aware MPI 和多节点扩展保留为单 GPU 闭环后的条件性阶段，不属于当前基金版本的必达目标。

### 4.8 实验矩阵与评价出口

| 实验层级 | 主要目的 | 必须覆盖 | 主要输出 |
|---|---|---|---|
| 二维局部与结构分析 | 低成本排查接口、结构性质和误差传播 | 精确／候选局部表示、受控扰动、组装／Matrix-Free、预条件更新和回退 | 局部误差—算子扰动—残差—响应误差关系及失败样本 |
| 二维拓扑优化 | 检查材料演化、灵敏度和最终设计传播 | 主对照矩阵中的可执行路径、统一优化参数和停止准则 | 迭代历史、回退率、柔顺度／约束和最终拓扑差异 |
| 三维结构分析 | 验证完整求解、峰值内存和规模增长 | 从可承受精确组装规模逐步过渡到已验证精确 Matrix-Free 真值 | 完整 solve、迭代数、精确平衡残差、时间—显存分解和瓶颈迁移 |
| 三维拓扑优化 | 形成最终端到端适用范围证据 | PIML Matrix-Free CPU/GPU、预条件更新、可靠性机制和完整优化流程 | 位移、柔顺度、灵敏度、最终拓扑、完整时间、峰值内存及规模扩展 |

规模按“小型正确性—中型消融—大型资源边界”递增，每一级继承上一层冻结的离散与正确性门禁。性能没有提升时仍保留瓶颈和失败模式，不能删除失败样本或改用不一致基线；本页不预设加速比、最大规模或最终优胜路线。

### 4.9 Evidence 记录、完成判定与事实所有权

每个可用于项目结论、申请书后续版本或论文的结果，至少绑定问题定义、输入与配置、代码 revision、软件／硬件环境、随机种子或确定性说明、命令、原始日志、正确性与结构检查、残差和迭代、时间与内存以及结论边界。具体文件、命令和数值仍由对应软件仓库维护，本页只记录稳定的跨线结论与 evidence 指针。

WP3 继续保持 `gated`，不因本页形成完整方案而提前启动。只有 WP1、WP2 的接口、正确性、精度和计时边界分别通过核心门禁，且主对照矩阵能够在同一问题上重放，才可形成融合结论。门禁失败、性能无收益或候选表示被否定均属于有效研究结果，但不得标记为“融合完成”。

## 五、第 80 批面上资助申请书证据综合

> 本节是第 80 批面上资助申请书的证据底稿，不是可直接上传的正文。§5.1–§5.5 对应“问题需求—研究现状—交叉缺口—选题价值”，支撑申请书第 1 部分选题依据；§5.6–§5.10 把申请书第 2–5 部分的栏目映射回仓库证据与研究设计。各批内正文仍以 [[../funding/active/china-postdoc-foundation-general-grant/80th-2026-application-draft|申请书正文]] 唯一维护。

### 5.1 问题需求与选题起点

三维高分辨率拓扑优化中的矩阵形成、存储、反复求解和数据搬运相互耦合。局部近似若破坏谱性质、增加 Krylov 迭代或导致拓扑偏移，局部加速便不能转化为端到端收益。因此，本项目同时评价精度、收敛性、时间和峰值内存，研究“局部表示如何获得—全局算子如何作用—计算如何在 GPU 上执行”的完整链路。

### 5.2 国际 Matrix-Free、GPU 与物理信息学习进展

Matrix-Free 已由 EBE 发展到逐单元积分、gather/scatter、向量化、MPI 和多重网格；GPU 拓扑优化也覆盖三维 Matrix-Free CG、多 GPU/AMG 及完整优化。但这些路线主要使用精确局部算子，且装配层级、离散、精度和硬件不同，不能直接回答学习算子进入全局求解后的结构、预条件和回退问题。详见 [[../technical-lines/matrix-free-research-guide#三、国内外研究现状、研究缺口与选题价值]] 与 [[../technical-lines/gpu-hpc-research-guide#三、国内外研究现状、研究缺口与选题价值]]。

Physics-Informed ML、PINN 和 neural operator 已提供物理融合、解场学习和函数到函数映射基础，PINNTO 展示了物理信息学习进入拓扑优化的对照路线。但这些外部方法不自动保证有限元局部算子的代数结构，也未天然覆盖“局部算子—全局平衡—灵敏度—设计更新”的传播链。详见 [[../technical-lines/piml-research-guide#三、国内外研究现状、研究缺口与选题价值]]。

### 5.3 国内 Matrix-Free、GPU 与局部力学学习进展

国内相关研究已覆盖分布式 EBE、assembly-free 拓扑优化、fully Matrix-Free MGPCG、CuPy SpMV 和 CPU–GPU 异构优化，但尚不能合并解释为统一的有限元 PIML/MF/GPU 技术链。

问题无关 PIML 路线由最终拓扑代理转向可复用局部形函数和缩聚算子，发展了监督学习、力学能量无标签训练及 CPU/MPI 按需预测。摘要级新证据又覆盖等参几何输入、三维梯度点阵应用、Bézier 边界位移参数化和超采样重叠数值基函数。Ma 2026 仍显式形成子结构缩聚刚度并组装全局粗尺度矩阵；新增四篇也未提供全局 Matrix-Free/GPU 闭环，因此不能支持三线融合已实现的结论。

### 5.4 交叉研究缺口

1. 现有 PIML 仍显式组装全局粗尺度矩阵，缺少由局部学习表示直接形成全局 Matrix-Free 算子作用的方法。
2. 缺少覆盖批量预测、局部作用、gather/scatter、Krylov 向量运算、归约和预条件的 GPU 协同执行及端到端证据。
3. 缺少 Matrix-Free 主算子、代理预条件器更新、结构检查和精确回退的协同可靠性机制。
4. 缺少局部表示误差向真残差、Krylov、响应、灵敏度和最终拓扑传播的系统证据。

### 5.5 本项目的选题价值

本项目以精确 Matrix-Free/GPU 基线为参照，将 PIML 局部表示重构为无需组装全局系统矩阵的算子作用，并协同研究 GPU 上的批量预测、局部作用和预条件 Krylov 求解。结构检查、误差控制、预条件更新和精确回退用于保证融合计算链可靠；统一的精度—收敛—时间—内存证据用于判断该方法能否降低矩阵形成与存储开销、扩展可解规模并获得端到端收益。

### 5.6 申请书关键论断与证据映射

| 综合论断 | 主要证据 | 可支持与不可外推边界 |
|---|---|---|
| MF 已形成多种实现层级 | Hughes 1983；[[../../literature/matrix-free/notes/Kronbichler2012-parallel-cell-operator\|Kronbichler 2012（摘要级）]]；[[../technical-lines/matrix-free-research-guide#四、证据锚点及结论边界]] | Kronbichler 摘要支持 cell-based 算子及混合并行框架；装配层级的统一判定属于跨源归纳，其译文完成前不补写全文细节 |
| MF 主算子可配组装代理预条件器 | Pazner 2020；[[../../literature/topology-opt/notes/Zhou2025-efficientaccelerationstrategies\|Zhou 2025（摘要级）]] | 支持混合装配层级；Zhou 2025 译文与精读待完成，不证明动态拓扑中的更新策略 |
| GPU 可服务完整拓扑优化，MF/GPU 已有分项证据 | Schmidt 2011；Herrero-Pérez 2021；[[../../literature/topology-opt/notes/Traff2023-GPU-topology-optimisation\|Träff 2023（摘要级）]] | Träff 摘要支持单 GPU 完整优化；其 MF、求解器和硬件细节待译文精读，不外推到 PIML 或相同多节点性能 |
| 国内已有 MF 与异构拓扑优化路线 | Liu 2007；Bian 2017；[[../../literature/topology-opt/notes/Zhou2025-efficientaccelerationstrategies\|Zhou 2025（摘要级）]]；Hou 2025；Liu 2026 | 支持分线进展；Zhou 2025 译文与精读待完成，不代表三线统一实现 |
| 物理与算子结构可进入学习过程 | Raissi 2019；Karniadakis 2021；Lu 2021；Xu 2021 | 支持 loss／表示／参数化；不自动保证本项目结构与收敛 |
| 局部力学表示可跨具体优化设置复用 | Huang 2022/2023/2024 | 适用于相同 PDE、离散和局部类型边界；不外推到任意问题 |
| 局部学习可进入 CPU/MPI 完整优化 | [[../../literature/topology-opt/notes/Ma2026-highperformanceparallel\|Ma 2026]] | 支持按需预测／释放；粗矩阵仍组装，非全局 MF/GPU 闭环 |
| 三线融合构成待验证研究问题 | 第二章证据成熟度矩阵与第三章交叉问题 | 属跨源归纳和研究假设，不能写成已有成果或绝对优先权 |

### 5.7 申请书第 2 节的证据—研究设计映射

> 本表是[[../funding/active/china-postdoc-foundation-general-grant/80th-2026-application-draft#2. 研究内容（研究对象，拟解决的关键科学问题，研究目标，限 2000 字）|申请书第 2 节]]的内部证据底稿，不作为需写入申请正文的参考文献表。已入库 `done/read` 论文和稳定概念页提供直接或全文级依据；摘要级与 `draft` 材料只支持表中注明的有限事实；本项目拟建立的耦合关系均属于待验证研究设计。

| 第 2 节要素 | 仓库证据与综合依据 | 形成的研究设计及边界 |
|---|---|---|
| 研究对象 | [[../../concepts/piml/mathematical-foundations\|PIML 数学基础]]界定可复用局部力学表示；[[../../concepts/matrix-free/assembly-levels\|Matrix-Free 装配层次]]界定全局算子作用；GPU/HPC 性能模型界定完整计算链；统一记号见[[#4.2 统一问题、记号与局部—全局算子关系]] | 限定二维／三维线弹性拓扑优化，连接局部预测、全局作用、预条件 Krylov、GPU 执行与设计更新；不外推至其他 PDE 或物理场 |
| 科学问题 1 | Huang 2022/2023/2024 与 Ma 2026 支持局部表示及其误差进入全局分析；Matrix-Free 技术线支持算子层级、真残差和预条件边界；误差契约见[[#4.6 误差、残差、可靠性与处置协议]] | 研究局部近似经限制／回填、局部作用和全局累加形成的算子扰动，以及结构性质、谱、预条件质量与 Krylov 收敛的关系；不是把近似误差归因于 Matrix-Free 本身 |
| 科学问题 2 | [[../../concepts/gpu-hpc/performance-model\|性能模型]]及 GPU/HPC 技术线表明 kernel、MatVec、solve 与完整优化不可互相替代；现有 PIML 公开证据仍以 CPU/MPI 为主；执行协议见[[#4.7 GPU 协同执行与端到端性能协议]] | 研究批量预测、局部作用、gather/scatter、向量运算、归约、预条件、搬移和同步的耦合，判断端到端收益条件；不以单次推理或单个 kernel 代表完整加速 |
| 研究内容 1／目标 1 | Matrix-Free 技术线的 FA/EA/PA/UA 分类、代理预条件证据和 PIML 技术线的表示相适配检查；统一接口和对照见[[#4.3 跨技术线的概念接口契约]]与[[#4.5 “局部算子来源 × 全局执行路径”二维对照契约]] | 建立精确组装、精确 Matrix-Free 与 PIML 近似 Matrix-Free 的统一基线，研究误差传播和预条件 Krylov；具体学习输出由候选比较确定 |
| 研究内容 2／目标 2 | GPU/HPC 技术线与性能模型的五级计时、数据驻留、缓存—重算和时间—显存口径；完整协议见[[#4.7 GPU 协同执行与端到端性能协议]] | 建立覆盖完整 GPU 计算链的执行方法与性能模型，离线训练、在线预测、单次求解和完整优化分别计量 |
| 研究内容 3／目标 3 | PIML 技术线的分布外识别与精确回退，交叉问题中的拓扑误差传播；实验出口见[[#4.8 实验矩阵与评价出口]] | 建立表示相适配的可靠性机制，以二维机理和三维规模算例逐层消融，界定精度、收敛、时间、内存和规模扩展的适用范围 |

### 5.8 申请书第 3 节的证据—技术步骤—验证指标映射

> 本表是[[../funding/active/china-postdoc-foundation-general-grant/80th-2026-application-draft#3. 研究方案（限 2000 字）|申请书第 3 节]]的内部方法底稿，用于保证每项技术步骤能够回溯至仓库事实并具有明确验证出口；它不改变单篇文献状态，也不把拟开展工作写成已有成果。

| 技术步骤 | 仓库依据与证据边界 | 方案实现 | 验证指标 |
|---|---|---|---|
| 统一基线与局部表示接口 | [[../technical-lines/piml-research-guide\|PIML 技术线]]规定精确真值、候选表示、结构检查和回退语义；Huang 2022/2023/2024 与 Ma 2026 支持已知局部表示路线；项目级接口见[[#4.3 跨技术线的概念接口契约]] | 冻结二维／三维问题契约，建立精确组装、精确 Matrix-Free、PIML 组装式和 PIML Matrix-Free 路径；候选表示不预设主次 | 局部真值、表示特有结构性质、全局响应及训练／部署成本可在同一问题下比较 |
| Matrix-Free 全局作用 | [[../../concepts/matrix-free/assembly-levels\|装配层次]]给出限制—局部作用—回填累加的算子形式；[[../technical-lines/matrix-free-research-guide\|Matrix-Free 技术线]]规定精确基线和接口 | 以 $\mathbf y=\sum_j\mathbf G_j^{\mathsf T}\widehat{\mathbf A}_j\mathbf G_j\mathbf x$ 实现全局作用，先接入精确局部算子，再替换为 PIML 近似算子 | 精确 Matrix-Free 与精确组装的算子作用、平衡残差和结构响应一致；PIML 路径报告局部—全局误差 |
| 预条件 Krylov 与误差监测 | Matrix-Free/PIML 技术线支持真残差、结构性质、代理预条件器和误差传播研究；代理预条件更新在动态拓扑中仍属待验证设计 | 按算子性质选择 Krylov 方法，区分递推残差与由精确局部算子复核的平衡残差，比较预条件器复用、局部更新和重建 | 对称性、半正定或约束后正定性、谱行为、迭代数、更新时间、平衡残差与响应误差 |
| GPU 协同执行与性能模型 | GPU/HPC 性能模型区分 kernel、MatVec、solve、优化迭代和完整任务；GPU/HPC 技术线给出批处理、缓存—重算和数据驻留边界 | 比较缓存局部表示、按需预测和预测—局部作用融合，覆盖 gather/scatter、向量运算、归约和预条件 | 在统一精度、停止准则、硬件和同步语义下报告阶段时间、完整求解／优化时间、迭代数及峰值显存 |
| 拓扑演化可靠性与验证 | [[#4.5 “局部算子来源 × 全局执行路径”二维对照契约]]与 PIML 技术线支持分布外识别、精确回退和表示相适配检查；端到端收益仍是待验证假设 | 监测材料演化、结构检查、平衡残差和预条件质量，按失败类型采用精确回退、预条件更新、缓存或分批执行 | 二维验证误差传播与收敛机理；三维验证位移、柔顺度、灵敏度、优化结果、完整时间、峰值内存和规模扩展 |

### 5.9 申请书第 4 节的证据—创新增量—表述边界映射

> 本表是[[../funding/active/china-postdoc-foundation-general-grant/80th-2026-application-draft#4. 特色与创新之处（限 1000 字）|申请书第 4 节]]的内部创新边界底稿。创新点描述的是由现有证据支持、仍需通过项目验证的研究增量，不构成“首次”“国际空白”或已有融合成果的优先权声明。

| 创新主线 | 已有基础与直接缺口 | 项目创新增量 | 表述边界 |
|---|---|---|---|
| PIML–Matrix-Free | Huang–Ma 路线支持可复用局部力学表示和 CPU/MPI 按需预测；Ma 2026 仍形成并组装全局粗尺度矩阵。Matrix-Free 技术线提供精确算子作用、Krylov 和预条件基线 | 将候选局部表示转化为全局算子按需作用，研究局部误差、算子性质、预条件质量与 Krylov 收敛的耦合 | 不把具体预测 $\mathbf N$ 或 $\mathbf K_s$ 作为创新主次，不把精确 Matrix-Free 基线写成 PIML 融合成果 |
| PIML–GPU | 现有入库 PIML 证据以 CPU/MPI 部署为主；GPU 文献支持批处理和局部计算的分项可行性，但不能证明本项目的 PIML–GPU 路径已经实现 | 面向大量局部区域研究混合类型批处理、数据驻留、缓存—重算和预测—局部作用融合，形成可复用局部力学表示的 GPU 生成、更新与局部执行方法 | 不将普通推理迁移或单个 kernel 加速等同于项目创新，不声称首次实现 PIML–GPU，不预设推理或局部作用加速比 |
| PIML–Matrix-Free–GPU 全链融合与可靠扩展 | 三条技术线已有分项证据，但现有入库文献未提供 PIML 预测、全局 Matrix-Free、预条件 Krylov、GPU 数据流和拓扑演化可靠性的统一闭环；三线融合仍属待验证研究问题 | 将 PIML 预测直接接入 GPU Matrix-Free 作用，并与 gather/scatter、Krylov 向量运算、归约、预条件和设计更新统一组织；以结构检查、精确回退和预条件更新维持拓扑演化下的可靠执行 | 不把分项程序连接写成融合完成，不写成已经保证精度、必然获得端到端收益或达到特定规模 |

### 5.10 申请书第 5 节的依据—阶段—成果边界映射

> 本表是[[../funding/active/china-postdoc-foundation-general-grant/80th-2026-application-draft#5. 研究计划及预期成果（限 500 字）|申请书第 5 节]]的内部计划底稿。两年阶段、WP1–WP3 和门禁以 [[project-plan#三、工作包与依赖|核心项目计划]]为事实源；[[../../archive/2026-postdoc-entry-assessment/postdoc-research-plan|归档入站计划]]只提供“基准复现—方法研究—并行集成—典型验证”及算法原型、软件模块、算例体系的历史组织依据，不恢复其已退出当前项目范围的研究内容。

| 阶段 | 当前项目依据与主要工作 | 阶段出口与成果边界 |
|---|---|---|
| 0—6个月 | WP1/WP2 并行启动：复现并统一精确组装、精确 Matrix-Free/Krylov 和 GPU 基线，冻结二维／三维问题、局部表示接口与评价体系 | 形成可重放的正确性、计时和内存基线；不把基线复现写成融合创新 |
| 6—12个月 | 推进候选 PIML 局部表示、结构检查、误差评价和 GPU 批量预测 | 形成 PIML–GPU 局部执行原型及结构、误差、吞吐和内存 evidence；不预设局部表示主次 |
| 12—18个月 | 在 WP1/WP2 门禁通过后研究 PIML–Matrix-Free 全局作用、代理预条件、误差—收敛关系及三线融合数据流 | WP3 只在接口、精度和计时边界通过后启动；程序连接不等于融合完成 |
| 18—24个月 | 完成拓扑演化可靠性机制以及二维／三维结构分析和拓扑优化端到端对照 | 界定精度、收敛性、时间、内存和规模扩展的适用范围，不预设性能数字或优胜路线 |
| 预期成果 | 汇总 WP1–WP3 可核验输出，并吸收归档计划中的算法原型、可复用模块和典型算例体系口径 | 形成三类算法原型；围绕经验证的科学问题形成论文稿件并投稿；完成软件模块、统一算例与性能评估体系、误差／性能 evidence 及适用条件；不承诺论文篇数、录用／发表、授权或特定软件集成 |

## 六、综合结论与来源

三线结合的辨识度不在程序拼接，而在[[#四、研究假设、统一研究方案与验证协议|统一研究方案与验证协议]]下重构 PIML 的全局 Matrix-Free 求解方式，建立批量预测、局部作用、可复用预条件与 GPU 异构执行之间可验证的耦合机制，并以正交方法对照、完整结构分析和拓扑优化评价准确性、收敛性、规模扩展及精度—时间—内存取舍。

### 权威入口

[[project-plan]] 维护 WP1–WP3；[[../technical-lines/_index]] 连接三份单线 guide；[[../postdoc-research-output-roadmap]] 维护论文边界；[[../../literature/matrix-free/_index]]、[[../../literature/topology-opt/_index]] 与 [[../../literature/_index#当前 ingest 队列]] 管理单篇和待入库证据；[[../../concepts/piml/_index]]、[[../../concepts/matrix-free/_index]]、[[../../concepts/gpu-hpc/_index]] 是稳定概念入口。

### 精简证据清单

**Matrix-Free／GPU**
1. Hughes et al. 1983 — EBE 历史起点 — [DOI](https://doi.org/10.1016/0045-7825(83)90115-9)。
2. Liu et al. 2007 — 分布式 EBE／Jacobi-PCG — [DOI](https://doi.org/10.1016/j.finel.2006.12.007)。
3. [[../../literature/matrix-free/notes/Kronbichler2012-parallel-cell-operator|Kronbichler & Kormann 2012]] — 并行 cell-based MF 的摘要级锚点；中文译文与精读待完成。
4. Bian & Fang 2017 — assembly-free 屈曲拓扑优化 — [DOI](https://doi.org/10.1177/1687814017715422)。
5. Pazner 2020 — MF 主算子与低阶代理预条件 — [DOI](https://doi.org/10.1137/19M1282052)。
6. [[../../literature/topology-opt/notes/Traff2023-GPU-topology-optimisation|Träff et al. 2023]] — 单 GPU 完整拓扑优化的摘要级锚点；Matrix-Free、硬件与求解器细节待译文精读。
7. [[../../literature/topology-opt/notes/Zhou2025-efficientaccelerationstrategies|Zhou et al. 2025]] — fully MF MGCG 与渐进三维拓扑优化的摘要级锚点；译文与精读待完成。
8. Wadbro & Berggren 2009 — GPU 百万变量拓扑优化 — [DOI](https://doi.org/10.1137/070699822)。
9. Schmidt & Schulz 2011 — 三维 GPU MF-CG — [DOI](https://doi.org/10.1007/s00791-012-0180-1)。
10. Martínez-Frutos & Herrero-Pérez 2015 — 固定网格 GPU MF-FEA — [DOI](https://doi.org/10.1016/j.finel.2015.06.005)。
11. Abdelfattah et al. 2021 — CEED GPU 高阶算子 — [DOI](https://doi.org/10.1016/j.parco.2021.102841)。
12. Herrero-Pérez & Martínez Castejón 2021 — 多 GPU 拓扑优化 — [DOI](https://doi.org/10.1016/j.advengsoft.2021.103006)。
13. Hou et al. 2025 — CuPy／SpMV 拓扑优化 — [DOI](https://doi.org/10.1016/j.finel.2025.104388)。
14. Liu et al. 2026 — CPU–GPU 异构层级结构优化 — [DOI](https://doi.org/10.1016/j.cma.2025.118408)。

**Physics-Informed ML／PINN／neural operator**
15. Karniadakis et al. 2021 — Physics-Informed ML 总框架 — [DOI](https://doi.org/10.1038/s42254-021-00314-5)。
16. Raissi et al. 2019 — PINN 正／反问题 — [DOI](https://doi.org/10.1016/j.jcp.2018.10.045)。
17. Lu et al. 2021 — DeepONet 算子学习 — [DOI](https://doi.org/10.1038/s42256-021-00302-5)。
18. Jeong et al. 2023 — PINNTO — [DOI](https://doi.org/10.1016/j.engstruct.2022.115484)。
19. Xu et al. 2021 — SPD-NN 结构化参数化 — [DOI](https://doi.org/10.1016/j.jcp.2020.110072)。

**问题无关 PIML 局部表示与应用路线**
20. [[../../literature/topology-opt/notes/Lei2018-machinelearningdriven|Lei et al. 2019]] — problem-specific 最终设计代理前史 — [DOI](https://doi.org/10.1115/1.4041319)。
21. [[../../literature/topology-opt/notes/Huang2022-problemindependentmachine|Huang et al. 2022]] — 局部密度到多尺度形函数 — [DOI](https://doi.org/10.1016/j.eml.2022.101887)。
22. [[../../literature/topology-opt/notes/Huang2023-PIML-substructure|Huang et al. 2023]] — 子结构形函数与缩聚算子 — [DOI](https://doi.org/10.1016/j.eml.2023.102041)。
23. [[../../literature/topology-opt/notes/Zhang2024-isoparametric-PIML|Zhang et al. 2024]] — 复杂设计域与等参单元；当前为摘要级 `draft` 证据。
24. [[../../literature/topology-opt/notes/Huang2024-PIML-datafree|Huang et al. 2024]] — mechanics-based data-free DeepONet — [DOI](https://doi.org/10.1016/j.jmps.2024.105893)。
25. [[../../literature/topology-opt/notes/Xu2025-PIML-lattice-MMC|Xu et al. 2025]] — PIML、MMC 与三维梯度点阵应用；当前为摘要级 `draft` 证据。
26. [[../../literature/topology-opt/notes/Ma2026-highperformanceparallel|Ma et al. 2026]] — CPU/MPI 按需预测／释放与组装粗矩阵 — [DOI](https://doi.org/10.1007/s10409-025-25942-x)。
27. [[../../literature/topology-opt/notes/Guo2026-highgeneralization-bezier|Guo et al. 2026]] — Bézier 边界位移参数化与内部位移响应映射；当前为摘要级 `draft` 证据。
28. [[../../literature/topology-opt/notes/Guo2026-PIML-OFEM|Guo et al. 2026 PIML-OFEM]] — 超采样数值基函数与重叠有限元；当前为 arXiv v1 摘要级 `draft` 证据。
29. 用户提供，2026-06 — 郭旭老师团队 PIML 与 Matrix-Free 高性能求解研究报告。
