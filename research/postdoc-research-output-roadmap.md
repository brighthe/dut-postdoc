---
title: "博士后科研成果路线"
topic: "博士延续成果、核心项目工作包、论文组合与资助渠道"
aliases:
  - 博士后论文路线
  - 博士后成果组合
tags:
  - research-roadmap
  - publication-plan
  - postdoc-funding
  - topology-optimization
  - Hu-Zhang
  - VEM
  - PIML
  - matrix-free
  - GPU
status: "in-progress"
date_start: 2026-07-31
date_update: 2026-08-09
---

# 博士后科研成果路线

> 本页把 [[long-term-research-lines|两条个人长期科研主线]] 映射为博士阶段延续成果、[[piml-matrix-free-gpu/project-plan|博士后核心研究项目]]的 WP1–WP3 论文组合与资助渠道，维护各成果的科学问题、相互边界和启动条件。本页不维护项目目标、行政积分、投稿状态或基金申报状态，也不替代具体论文稿件、技术线 guide 和基金执行页。

## 一、事实分工

- 中期累计 2 分、出站累计 5 分、论文和项目计分条件及个人积分台账，以 `heliangos:career/dlut-postdoc/research-points.md` 为唯一事实源。
- 中期与出站的行政节点和成果认定边界，分别以 `heliangos:career/dlut-postdoc/midterm-assessment.md`、`heliangos:career/dlut-postdoc/exit-assessment.md` 为准。
- 三篇 A 类论文是个人风险控制主线，不等于三篇论文当前已经完成、投稿、接收或获得学院认定。
- 中国博士后科学基金面上资助以实际获批为成果目标；提交申请、进入评审或公示均不写成已经完成。
- 核心项目状态独立于基金结果；基金未获批不终止研究，基金获批也不表示 WP1–WP3 或项目已经完成。
- PIML 的方法边界、模型选型与证据综合由 [[technical-lines/piml-research-guide]] 维护，项目级状态由 [[piml-matrix-free-gpu/project-plan]] 维护；GPU/HPC 的当前状态和完成门禁由 [[technical-lines/gpu-hpc-research-guide]] 维护；Matrix-Free 的长期阶段、验收原则、当前状态、推进顺序和完成记录统一由 [[technical-lines/matrix-free-research-guide]] 维护。

## 二、论文与项目组合

| 编号 | 成果方向 | 所属主线 | 规划定位 | 当前研究入口 | 关键边界 |
|---|---|---|---|---|---|
| 论文一 | Hu–Zhang 混合有限元拓扑优化 | 高精度数值离散与拓扑优化 | 博士延续成果；保障论文；中期优先 | [[../papers/arbitrary-order-huzhang-topopt-outline]]、[[../papers/arbitrary-order-huzhang-topopt-draft-zh]] | 不纳入核心项目工作包；投稿、接收、期刊级别与计分认定另行维护 |
| 论文二 | 无稳定化项虚单元拓扑优化 | 高精度数值离散与拓扑优化 | 博士延续成果；保障论文；中期并行 | 对应长期调研与论文页待形成稳定内容后建立 | 不纳入核心项目工作包；须形成独立的理论、算法与拓扑优化证据链 |
| 论文三（A） | WP1：Matrix-Free/GPU | 智能高性能计算力学 | 核心项目基础成果；保障论文；承担出站论文主线 | [[piml-matrix-free-gpu/project-plan#三、工作包与依赖]]、[[technical-lines/matrix-free-research-guide]]、[[technical-lines/gpu-hpc-research-guide]] | 使用精确有限元或精确子结构算子，不引入学习算子 |
| 论文四（B） | WP2：PIML/GPU | 智能高性能计算力学 | 核心项目局部算子成果；目标扩展论文 | [[piml-matrix-free-gpu/project-plan#三、工作包与依赖]]、[[technical-lines/piml-research-guide]]、[[technical-lines/gpu-hpc-research-guide]] | 不引入全局 Matrix-Free 融合；GPU 必须参与算法与数据流协同设计 |
| 论文五（C） | WP3：PIML/Matrix-Free/GPU | 智能高性能计算力学 | 核心项目条件性融合成果 | [[piml-matrix-free-gpu/project-plan]]、[[piml-matrix-free-gpu/high-performance-solver-survey]] | 只有 WP1、WP2 的核心门禁分别通过后才启动，不能只是两篇工作的程序拼接 |
| 面上资助 | 核心项目的条件性资助渠道 | 智能高性能计算力学 | 最多三次个人申报机会；以获批为资助目标 | [[funding/postdoc-funding-applications]]、[[funding/active/china-postdoc-foundation-general-grant/80th-2026]] | 第 80 批为第一次；未获批且仍符合资格时才启用后续机会；获批不等于项目完成 |

论文一、论文二是博士阶段工作的延续与成果转化，论文三（WP1）是核心项目的保障成果；三者共同构成博士后阶段论文风险控制。论文四（WP2）和论文五（WP3）用于扩展核心项目的学术产出上限，不预先纳入三篇论文的刚性保障。

## 三、智能高性能计算力学的三层论文

### A / WP1：Matrix-Free/GPU

**核心问题**：如何在三维结构分析和拓扑优化中，通过统一的 Matrix-Free 算子、预条件 Krylov 方法以及 CPU/GPU/MPI 异构执行降低完整求解时间和峰值内存？

**研究范围**：

- 统一 FA、LA、EA、PA/QA 和 UA/NONE 等装配层级的离散问题、算子语义和验证口径。
- 建立可用的 Krylov 与预条件路径，同时报告真残差、迭代数、完整 solve 时间和峰值内存。
- 比较 CPU、单 GPU、MPI 及后续多 GPU 的正确性、计算—通信分解和强弱扩展。
- 在结构分析或拓扑优化的反复更新场景中验证 update、apply、preconditioner 和完整迭代成本。

**排除项**：本论文始终使用精确有限元或精确子结构算子，不使用 PIML 预测结果；PIML 引入的误差和结构保持问题不属于本论文。

### B / WP2：PIML/GPU

**核心问题**：如何通过可复用且结构性质可检查的 PIML 局部力学表示和 GPU 批量计算，服务二维、三维结构分析，并控制局部预测到全局响应的误差传播？

**研究范围**：

- 将多尺度形函数、缩聚刚度及其他满足问题无关性和下游接口要求的局部力学表示作为候选；对“预测 \(N\) 后构造 \(K_s=N^{\mathsf T}KN\)”与“直接预测 \(K_s\)”等已有路线并列评价，不预设主次。
- 比较对称性、正定性、能量一致性、位移、柔顺度、灵敏度和细尺度恢复误差。
- 设计适合 GPU 的样本表示、固定或分层 batch、混合尺寸处理和训练/推理数据流。
- 比较精确计算、缓存局部表示和 GPU 按需预测的精度—吞吐—显存权衡。
- 建立分布外检测、结构检查和精确回退，但不接入全局 Matrix-Free Krylov 管线。

**排除项**：仅把现有网络迁移到 CUDA、只报告训练加速或只报告单次推理吞吐，不足以构成本论文的独立贡献。

### C / WP3：PIML/Matrix-Free/GPU

**核心问题**：如何把 GPU 批量预测的局部力学表示直接嵌入 Matrix-Free Krylov 求解与拓扑优化迭代，并在预测误差、收敛性、时间和内存之间建立可解释的端到端权衡？

**启动条件**：

- A 已形成可靠的 Matrix-Free/GPU 算子、预条件和完整 solve 基线。
- B 已形成可重放的二维、三维 PIML/GPU 路径、结构检查和精确回退。
- 两条路径使用一致的局部算子接口、精度定义、硬件计时边界和拓扑优化参考问题。

**必须新增的融合贡献**：

- PIML 推理与局部算子作用的融合数据流。
- 预测、缓存、压缩和按需重算的动态策略。
- 结构检查、分布外检测与精确回退对 Krylov 收敛的影响。
- GPU scatter-add、batch 调度、通信与全局归约的协同。
- 完整结构分析或拓扑优化中的精度—时间—内存 Pareto 前沿。

如果不能形成上述独立耦合机制和端到端证据，C 只作为系统集成或软件成果，不拆分为独立论文。

## 四、核心项目与资助映射

核心项目名称、总体目标、WP1–WP3、两年阶段和条件性资助策略统一由 [[piml-matrix-free-gpu/project-plan]] 维护。本页只记录成果关系：论文 A、B、C 分别对应 WP1、WP2、WP3；基金申请是项目的资助渠道，不是与项目并列的科研方向。

第 80 批面上资助是核心项目的第一次申报版本。若未获批、个人仍符合资格且后续批次正式开放，可按新增认识和证据形成第二、第三次申报；任一次获批后停止后续面上申报。具体批次、资格、材料、提交节点和实际状态只由 [[funding/postdoc-funding-applications]] 及对应执行页维护。

## 五、维护规则

- 论文主题、主贡献或 A/B/C 边界发生变化时更新本页；投稿状态、目标期刊和接收状态不在本页维护。
- 具体论文形成稳定框架后，在 `papers/` 建立独立稿件并由本页链接，不把正文复制回本页。
- 项目名称、WP1–WP3、阶段和项目级启动条件只由 [[piml-matrix-free-gpu/project-plan]] 维护；单线技术事实、验收门禁和当前关键动作由对应 technical-line guide 维护；三线交叉现状、耦合机制、研究假设和评价契约由 [[piml-matrix-free-gpu/high-performance-solver-survey]] 维护；本页只维护论文成果边界和风险组合。
- 行政考核和积分策略变化时先更新 `heliangos:career/dlut-postdoc/`，本页仅在成果组合受到影响时更新简短结论和事实源指针。
