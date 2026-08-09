---
title: "PIML 局部力学算子技术线研究指南"
topic: "二维与三维 PIML 局部力学算子的技术路线与证据边界"
aliases:
  - "research/piml-model-selection/_index"
  - "research/piml-model-selection/selection-framework"
  - "research/technical-lines/piml-task-line"
  - "piml-task-line"
  - "research/postdoc-plan/long-term/direction-1-piml-matrix-free/liu-chang-model-selection-task-line"
  - "research/piml-matrix-free/liu-chang-model-selection-task-line"
  - "research/piml-model-selection/liu-chang-model-selection-task-line"
  - "research/piml-model-selection/lei2018-problem-specific-baseline"
  - "discussions/liu-chang/first-formal-piml-evidence-baseline-task"
  - "first-formal-piml-evidence-baseline-task"
tags:
  - technical-line
  - research-guide
  - PIML
  - substructuring
  - operator-learning
  - topology-optimization
status: "in-progress"
date_start: 2026-07-21
date_update: 2026-08-09
related:
  - piml/mathematical-foundations
  - method-lineage
  - machine-learning
  - ../piml-matrix-free-gpu/_index
  - ../piml-matrix-free-gpu/project-plan
---

# PIML 局部力学算子技术线研究指南

## 一、定位、事实所有权与研究目标

本页是 PIML 局部力学算子技术线的长期研究指南，维护可跨项目复用的方法边界、能力目标、模型选型原则与证据综合。博士后阶段优先服务 [[../piml-matrix-free-gpu/project-plan#三、工作包与依赖|核心项目 WP2]]；项目级目标、阶段与状态由核心项目计划维护，程序、配置和运行结果由 `soptx` 维护，单篇论文事实由 `literature/` 维护，具体交流内容和导师反馈由 [[../../discussions/liu-chang/_index|刘畅工作汇报]]维护。

面向大规模结构拓扑优化，本技术线的目标是自行建立覆盖二维与三维的 PIML 局部力学表示，使预测算子能够可信地进入全局结构分析，并最终与 Matrix-Free 和 GPU 求解路径连接。

| 能力 | 目标 |
|---|---|
| 精确基线 | 二维、三维均建立与候选局部表示对应的精确真值、接口求解和必要的细尺度恢复 |
| 候选局部表示 | 多尺度形函数、缩聚刚度及其他满足问题无关性和全局接口要求的局部力学表示并列评价，不预设主次 |
| 结构检查 | 根据具体表示检查对称性、正定或半正定性、刚体模态、完备性和能量一致性等必要性质 |
| 全局评价 | 报告候选局部表示误差及其对全局位移、柔顺度和必要细尺度恢复的影响 |
| 工程接口 | 形成可重放的数据生成、训练、推理、检查和精确回退入口 |
| 最终连接 | 向 Matrix-Free 提供局部算子，向 GPU 提供批量推理与局部作用 |

## 二、PIML 技术路线与学习对象边界

### 2.1 术语与路线边界

核心项目题目中的 PIML 指 **Problem-Independent Machine Learning（问题无关机器学习）**，直接承接 Huang–Ma 谱系。它不直接预测最终拓扑或特定宏观边值问题的全局解，而学习可嵌入传统全局平衡求解、能够跨宏观几何、整体边界条件和外载荷复用的局部力学表示。已入库论文中的多尺度形函数和缩聚刚度是代表性实现，不构成对本项目唯一学习输出的预设；PDE、离散方式、单元类型、材料模型或局部表示改变时，不能默认模型继续复用。

Physics-Informed Machine Learning、PINN、neural operator 和结构化学习是本技术线的外部方法背景、表示工具或结构保持类比证据，不是项目 PIML 的正式展开。控制方程、能量原理和代数结构仍可进入问题无关模型的训练、参数化或校正，但应表述为基于力学机理的训练或结构保持机制。采用 mechanics-based loss、DeepONet 或其他物理约束也不自动证明局部算子已经满足所需力学结构。

稳定术语见 [[../../concepts/piml/_index]]，数学定义见 [[../../concepts/piml/mathematical-foundations]]，角色边界见 [[../../concepts/ml-roles-and-boundaries]]，方法演化见 [[../../concepts/piml/method-lineage]]。

### 2.2 学习对象、结构保持与全局接口

二维和三维线弹性局部问题均为必需交付，不把两个维度处理成二选一关系。多尺度形函数 $N$、缩聚刚度 $K_s$ 以及其他满足问题无关性和全局 Matrix-Free 接口要求的局部力学表示均作为候选路线；其中“预测 $N$ 后由 $K_s=N^{\mathsf T}KN$ 构造局部算子”和“直接预测 $K_s$”属于已有文献支持的两种实现。候选路线必须共享问题定义、数据划分、精确真值和下游评价，具体结构条件与恢复接口则按表示分别定义，不能只比较局部 MSE。

本技术线需要回答：

1. 如何统一描述二维、三维子结构中的局部材料分布、内部自由度和接口自由度？
2. 不同候选局部表示在结构保持、误差传播、计算成本和 Matrix-Free 部署方面具有怎样的适用条件与取舍？
3. 如何针对具体表示检查对称性、适用条件下的半正定或约束后正定、刚体模态、分片统一性／线性完备性和能量一致性等必要性质？
4. 局部表示误差如何传播到全局位移、柔顺度、必要的细尺度恢复和 Krylov 收敛？
5. 如何识别不可信预测并回退到精确局部计算？
6. 如何把批量预测和局部算子作用接入 Matrix-Free 与 GPU 执行？

本技术线负责局部学习对象、结构检查、误差传播和精确回退语义。全局无矩阵作用、Krylov 与预条件见 [[matrix-free-research-guide]]；批处理、设备执行、内存与端到端性能见 [[gpu-hpc-research-guide]]。

### 2.3 模型选型与统一比较契约

模型选型不从网络名称开始，而是先冻结学习对象、表示、数据、物理约束、下游任务和部署环境，再筛除不满足硬门槛的方案并形成可解释的多指标取舍。

| 问题维度 | 必须确认的内容 | 对选型的影响 |
|---|---|---|
| 学习对象 | 最终设计、解场、局部形函数、缩聚刚度、响应量或其他对象 | 决定输出参数化、精确真值和研究边界 |
| 表示与数据 | 定长向量、规则栅格、坐标查询、非结构网格或函数；尺度变化、标签数量和成本 | 决定降维方式、候选模型族和数据划分 |
| 训练信号 | 监督标签、PDE／能量约束、data-free 或混合训练 | 决定 objective、采样方法和训练成本 |
| 物理硬约束 | 对称性、正定性、刚体模态、守恒、分片统一性或能量关系 | 决定硬参数化、软约束、后处理和淘汰条件 |
| 下游误差 | 预测量进入有限元、接口求解、灵敏度还是优化循环，局部误差如何传播 | 决定最终评价指标，避免只比较局部 MSE |
| 部署与可靠性 | 延迟、吞吐、内存、硬件、批量方式、失败代价和精确回退 | 决定模型容量、数据布局和混合策略 |

决策顺序固定为：

```text
冻结问题契约
  -> 确定精确真值与简单基线
  -> 用物理硬门槛筛选
  -> 测量局部误差与下游误差传播
  -> 比较部署成本与失败处理
  -> 输出适用条件和 Pareto 取舍
```

- 简单基线可以是常数、线性回归、邻域方法、PCA/POD 加经典回归、小型 MLP 或精确／降阶数值方法，但必须共享数据划分、真值、接口和评价代码。
- 必要结构性质先于平均误差；不满足数学前提的候选不能仅凭较低 MSE 通过。
- 统一比较至少冻结 train/validation/test 职责、输入输出 shape 与单位、精确真值、predictor 接口、参数量、计时边界、硬件、失败条件、回退策略、随机种子、软件版本和机器可读结果。
- 结果同时报告局部精度、结构性质、下游响应、数据与训练成本、推理与内存、分布外失败和回退比例；不输出脱离问题条件的单一“冠军模型”。

本页不对候选模型作脱离具体问题契约的定量优劣结论；此类结论须由可追溯的程序与数值证据支持。

## 三、国内外研究现状、研究缺口与选题价值

### 3.1 范围与判定口径

本节以 Problem-Independent 局部力学学习为项目主线，将 Physics-Informed ML、PINN、neural operator 和结构化参数化作为国际背景与对照。结构保持不能只依据训练 loss 或局部 MSE 判断，而要分别核对分片统一性／线性完备性、对称性、适用条件下的半正定或约束后正定、刚体模态、能量一致性，以及进入全局求解后的真实残差和响应误差。“国内研究”只依据论文原始机构信息判断，不按作者姓名或期刊所在地推断。

### 3.2 国外研究进展

[Raissi et al. 2019](https://doi.org/10.1016/j.jcp.2018.10.045) 建立了以神经网络表示解场、以 PDE 与初边值条件残差训练的 PINN 正问题／反问题范式；[Karniadakis et al. 2021](https://doi.org/10.1038/s42254-021-00314-5) 进一步把数据、数学模型和物理约束的多种融合方式统一到 Physics-Informed ML 框架中。这些工作说明物理知识可以进入机器学习过程，但主要证据对象是连续解场、参数识别或代理模型，不能直接推出有限元局部刚度的对称性、正定性或 Krylov 收敛性。

[Lu et al. 2021](https://doi.org/10.1038/s42256-021-00302-5) 的 DeepONet 用 branch net 编码输入函数、trunk net 编码查询位置，提供了学习非线性算子的通用表示。它为“材料分布函数 → 坐标连续的局部形函数”提供方法基础，但通用逼近能力不等于力学结构的硬保证；具体输出是否满足边界条件、刚体运动和能量关系仍取决于问题构造、损失与参数化。

拓扑优化中，[PINNTO 2023](https://doi.org/10.1016/j.engstruct.2022.115484) 采用 energy-based PINN 替代传统流程中的 FEA，并在无需标签数据的结构拓扑优化算例中验证可行性。该路线学习特定设计状态下的位移场，回答“能否用 PINN 承担结构分析”；Problem-Independent 路线学习可跨宏观问题复用的局部力学表示，回答“能否替代反复局部构造并保留传统全局平衡”。两者是互补对照，不应混写成同一对象。

结构保持方面，[Xu et al. 2021](https://doi.org/10.1016/j.jcp.2020.110072) 在本构学习中让网络预测 Cholesky 因子，再构造对称正定切线刚度，说明把必要代数性质写入参数化通常比只增加误差惩罚更可靠。但该证据对象是材料本构切线，不是拓扑优化子结构的多尺度形函数或缩聚算子；它只能支撑本项目采用结构化参数化的研究动机，不能当作局部算子方案已经解决的证据。

### 3.3 国内与团队路线进展

现有已入库论文显示，大连理工大学团队的路线从问题相关最终设计代理逐步转向可复用局部力学表示：[[../../literature/topology-opt/notes/Lei2018-machinelearningdriven|Lei 2018/2019]] 在固定 MMC 问题下学习最终优化设计，是前史对照，不属于 WP2 的局部算子主线。

[[../../literature/topology-opt/notes/Huang2022-problemindependentmachine|Huang 2022]] 在 EMsFEM 框架中学习局部密度到多尺度形函数的映射，再由预测形函数构造粗单元刚度；随机局部密度不依赖具体优化轨迹，但监督标签仍需要局部 EMsFEM 真值。分片统一关系被用于输出构造，刚度矩阵 MSE 属于软约束；论文仍组装全局粗网格矩阵，不属于全局算子级 Matrix-Free。

[[../../literature/topology-opt/notes/Huang2023-PIML-substructure|Huang 2023]] 把路线扩展到三维经典子结构静力缩聚，比较“预测 $N$ 后由 $K_s=N^{\mathsf T}KN$ 构造缩聚刚度”与“直接预测 $K_s$”两条路径，并显式利用刚体运动约束降低输出维数。前一路径保持形函数、位移恢复和能量计算之间的构造联系；后一路径在线更直接，但论文也指出预测形函数与预测刚度未必严格满足能量一致关系。

[[../../literature/topology-opt/notes/Huang2024-PIML-datafree|Huang 2024]] 使用 DeepONet 表示坐标连续的多尺度形函数，并以伪结构总应变能构造 mechanics-based data-free 训练，消除监督形函数标签；刚体运动继续通过构造复现。该工作把物理信息从标签和刚度软约束推进到变分训练目标，但能量 loss 的降低不自动等于所有代数性质均被硬保证。

[[../../literature/topology-opt/notes/Ma2026-highperformanceparallel|Ma 2026]] 将局部预测、缩聚刚度构造、粗网格求解、位移恢复、灵敏度、滤波和优化更新扩展到 CPU/MPI 流程，并通过 PETSc 多重网格预处理 GMRES 与多尺度形函数按需预测／释放处理数十亿单元问题。这里的 `matrix-free` 主要指不长期保存多尺度形函数；全局粗网格缩聚矩阵仍被形成和组装，因此不能写成学习局部算子已经嵌入全局 Matrix-Free/Krylov 主算子。

四篇新建 `draft` 文献入口补充了表示与应用分支，但当前只完成元数据／摘要核验：[[../../literature/topology-opt/notes/Zhang2024-isoparametric-PIML|Zhang 2024]] 将子结构单元几何形状与材料分布共同作为输入并学习数值形函数，扩展到复杂设计域；[[../../literature/topology-opt/notes/Guo2026-highgeneralization-bezier|Guo 2026 Bézier]] 学习三次 Bézier 参数化边界位移场到子结构内部位移场的映射；[[../../literature/topology-opt/notes/Guo2026-PIML-OFEM|Guo 2026 PIML-OFEM]] 以超采样数值基函数、重叠有限元和 U-Net 构造另一类局部降阶表示，证据等级为 arXiv v1；[[../../literature/topology-opt/notes/Xu2025-PIML-lattice-MMC|Xu 2025]] 将 PIML 与 MMC、分区坐标映射和三维梯度点阵优化结合。它们支持“不预先锁定 $N/K_s$”和“表示选择受几何、边界参数化与应用对象驱动”的判断，但尚不能支持全文级结构性质、性能比较或 PIML–Matrix-Free–GPU 闭环结论。

### 3.4 研究缺口与选题价值

1. **结构性质尚未统一闭合。** 现有工作分别利用分片统一关系、刚体运动构造、刚度软约束或能量目标，但公开证据尚未形成同时覆盖对称性、适用条件下半正定／约束后正定、刚体模态、完备性和能量一致性的统一硬参数化、检测与修正链。
2. **动态拓扑与分布外行为证据不足。** 局部密度随优化持续演化，规则随机样本、固定子结构尺度和固定本构下的精度不能直接外推到非结构网格、复杂几何、极端稀疏材料连通性或新的离散／材料模型。
3. **局部误差尚未系统连接全局迭代。** 已有论文主要报告局部预测、位移、柔顺度、优化设计或流程时间，尚缺少局部算子谱性质—真残差—Krylov 迭代—预条件有效性—灵敏度—最终拓扑的统一传递证据。
4. **全局 Matrix-Free 融合尚未完成。** 现有 Problem-Independent 路线最终仍形成并组装粗尺度矩阵；PINNTO 则替代解场求解。两条路线都不能直接回答预测局部算子如何在不组装全局矩阵时稳定完成算子作用、预条件与精确回退。
5. **GPU 端到端证据仍不完整。** 局部推理和小算子构造具有批量并行潜力，但现有 Huang–Ma 公开证据基于 CPU 或 CPU/MPI；尚不能声称 GPU 批量推理、scatter-add、Krylov 归约和完整拓扑优化已经获得时间—显存收益。

WP2 的选题价值不是再训练一个只追求局部 MSE 的网络，而是面向全局结构分析与 Matrix-Free 接口，比较多尺度形函数、缩聚刚度及其他候选局部表示在结构、精度、降维和部署方面的取舍，建立适用于二维／三维的表示相适配参数化、数值检查、分布外识别和精确回退。对“预测 $N$ 后构造 $K_s$”与“直接预测 $K_s$”等已有路线采用共同问题和下游指标并列评价，不预先指定优先级；哪些结构可以硬保持、哪些只能事后检查，应由具体表示的数学关系和数值证据确定。

WP3 的选题价值在于把通过 WP2 门禁的局部算子嵌入精确 Matrix-Free/GPU 基线，研究学习误差与预条件、Krylov 收敛及拓扑更新的耦合，而不是把三种现有程序顺序连接。只有在同题离散、真值、停止准则和硬件计时边界下同时报告真实残差、位移、柔顺度、灵敏度、最终拓扑、时间和显存／内存，才能判断融合是否真正扩大可解规模。

## 四、证据锚点及结论边界

### 4.1 核心文献证据矩阵

| 证据 | 学习对象与训练信号 | 物理／结构处理 | 拓扑优化与全局求解角色 | 平台证据 | 能支持与不能支持的结论 |
|---|---|---|---|---|---|
| Raissi et al. 2019 | 坐标／参数到 PDE 解场；方程与初边值残差 | 物理主要进入 loss | 可替代特定正／反问题求解；不是局部离散算子 | 以论文算例为准 | 支持 PINN 范式；不支持局部刚度结构或跨问题复用 |
| Karniadakis et al. 2021 | 数据与模型融合的总框架 | 数据、loss、架构等多种入口 | 方法综述，不是单一拓扑优化实现 | 不适用 | 支持外部 Physics-Informed ML 背景；不是项目 PIML 的定义，也不证明具体算子性能 |
| Lu et al. 2021 | 输入函数到输出函数；branch/trunk 监督学习 | 通用 operator representation | 为连续局部形函数表示提供基础；非 TO 实现 | 以论文算例为准 | 支持算子学习表示；不自动保证力学结构 |
| PINNTO 2023 | 当前设计状态到位移场；energy-based、无标签 | 变分能量进入训练 | PINN 替代 FEA，继续进入 SIMP 流程 | 论文结构算例 | 支持 PINN–TO 可行性；不支持可复用局部算子或 Matrix-Free |
| Xu et al. 2021 SPD-NN | 状态到切线刚度的 Cholesky 因子；监督学习 | 通过因子化构造对称正定 | 本构学习类比，不是 TO 子结构 | 论文材料算例 | 支持结构化参数化动机；不证明本项目 $N/K_s$ 路线 |
| Huang 2022 | 局部密度到 EMsFEM $N$；监督形函数与刚度 soft loss | 分片统一构造；刚度 MSE 软约束 | 构造粗单元刚度、组装并求解粗网格 | CPU 工作站 | 支持局部问题无关复用；不支持 data-free、GPU 或全局 Matrix-Free |
| Huang 2023 | 局部密度到 $N$ 或 $K_s$；监督学习 | 刚体运动构造；两条输出路径 | 子结构缩聚、全局缩聚系统与细尺度恢复 | CPU 工作站 | 支持三维子结构路线；直接 $K_s$ 路径不保证与 $N$ 能量一致 |
| Huang 2024 | 密度函数与坐标到连续 $N$；伪结构总应变能 | 刚体运动构造、mechanics-based loss | 构造 $K_s$ 并完成大规模结构分析／优化 | CPU 工作站 | 支持 data-free 与连续表示；不等同于全部结构性质硬保证 |
| Ma 2026 | 局部密度到缩减 $N$；使用既有训练模型 | 六类刚体运动构造 | CPU/MPI 局部计算、组装粗矩阵、MG-GMRES、完整优化 | CPU/MPI、PETSc | 支持并行与按需预测；不支持 GPU 或全局算子级 Matrix-Free |
| Zhang 2024（draft） | 单元几何形状与材料分布到数值形函数；摘要级监督学习描述 | 等参单元；全文结构处理待精读 | 复杂设计域结构分析与拓扑优化 | 摘要未形成统一硬件证据 | 支持几何感知输入与复杂设计域扩展；不支持全文级性能或结构结论 |
| Xu 2025（draft） | PIML 表征三维点阵复合结构力学响应；具体局部接口待精读 | MMC、分区坐标映射与完全连通 | 三维梯度点阵复合结构优化 | 摘要未形成统一硬件证据 | 支持应用范围扩展；不单独证明新的通用局部表示或 Matrix-Free |
| Guo 2026 Bézier（draft） | 三次 Bézier 边界位移场到子结构内部位移场；DeepONet | 边界位移参数化；其他结构性质待精读 | 子结构分析与拓扑优化 | 摘要未形成统一硬件证据 | 支持边界场参数化与响应映射候选；不支持全局 MF/GPU 结论 |
| Guo 2026 PIML-OFEM（draft；arXiv v1） | 杨氏模量分布到超采样数值基函数；U-Net | 重叠有限元、分片统一、角节点自由度 | 大规模异质结构分析与高分辨率拓扑优化 | 预印本摘要级 | 支持另一类局部降阶表示；期刊发表、全文细节与闭环性能待核验 |

国际五篇目前只满足公开来源层级的核验，仍在 [[../../literature/_index#当前 ingest 队列|文献总索引]]中标记为 `to-ingest`；Huang–Ma 单篇全文事实和模型选型证据卡由各自文献笔记唯一维护。新增四篇保持 `draft`，本表只使用已核验元数据／摘要并明确外推边界，不等同于正式精读。

## 五、权威事实来源

- [[../../concepts/piml/_index]] — 项目 PIML 的 Problem-Independent 正式释义及 Physics-Informed 外部方法背景边界。
- [[../../concepts/piml/mathematical-foundations]]、[[../../concepts/piml/method-lineage]] — Problem-Independent 局部力学学习的数学定义与方法谱系。
- [[../../literature/_index#当前 ingest 队列]] — Physics-Informed ML、PINN、neural operator 和结构保持类比的当前待入库文献。
- Huang 2022/2023/2024、Ma 2026 与 Lei 2018/2019 的全文事实和模型选型证据卡 — 由 `literature/topology-opt/notes/` 中对应单篇笔记维护。
- [[matrix-free-research-guide]]、[[gpu-hpc-research-guide]] — Matrix-Free 与 GPU 技术线。
- [[../piml-matrix-free-gpu/_index]]、[[../piml-matrix-free-gpu/project-plan]] — 博士后核心研究项目入口及 WP2/WP3 的目标、状态和依赖。
- [[../piml-matrix-free-gpu/high-performance-solver-survey]] — 跨线关系、开放问题与研究切入点。
- [[../../discussions/liu-chang/_index]] — 面向刘畅老师的单次汇报、导师反馈和会后行动入口。
- [[../../discussions/guo-xu/_index]] — 面向郭旭老师的 PIML 阶段表达入口；汇报页不作为任务状态或研究事实源。
