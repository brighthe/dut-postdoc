---
title: "刘畅"
type: entity
entity_kind: person
aliases:
  - Liu Chang
  - Chang Liu
  - liu-chang
tags:
  - PIML
  - topology-opt
  - MMC
  - machine-learning
  - operator-learning
  - GNN
status: in-progress
date_added: 2026-07-30
date_update: 2026-08-09
---

# 刘畅

> **一句话**：大连理工大学工程力学系教授，郭旭院士学生，显式拓扑优化（MMC）与「人工智能赋能结构分析与优化」方向的骨干，是本知识库 PIML 主线全部论文的共同作者。**与本人的交集在于：他这条线已横跨多个模型族但缺少可复用的选型判据，而本人的数值线性代数、Krylov/预条件子与 GPU 背景正落在「模型误差如何传播进求解器」这一侧。**

## 基本信息

| 项 | 内容 |
|---|---|
| 类型 | person |
| 所属/单位 | 大连理工大学 · 力学与航空航天学院 · 工程力学系；工业装备结构分析优化与 CAE 软件全国重点实验室 |
| 职称 | 教授、博士生导师 |
| 学术谱系 | 博士导师为郭旭院士（见 [[guo-xu]]） |
| 关键词 | MMC、显式拓扑优化、PIML、算子学习、力学超材料、增材制造 |
| 公开主页 | <https://faculty.dlut.edu.cn/liuchang/zh_CN/> |
| Google Scholar | <https://scholar.google.com/citations?user=B-uZM4EAAAAJ> |

> 职称以官方主页为准；部分第三方学者聚合页仍标注「副教授」，属过期信息。
>
> **事实所有权**：本页拥有其公开学术身份、署名工作书目与跨源提炼的模型选型史；通用选型判据和任务排序引用 [[../research/technical-lines/piml-research-guide#2.3 模型选型与统一比较契约|PIML 研究指南]]，Lei 2018/2019 的论文证据引用 [[../literature/topology-opt/notes/Lei2018-machinelearningdriven#模型选型证据卡]]，具体汇报引用 [[../discussions/liu-chang/_index]]。PIML × Matrix-Free × GPU 的跨线研究假设由 [[../research/piml-matrix-free-gpu/high-performance-solver-survey]] 维护；真实沟通过程由沟通仓库维护，本页不复制上述内容。

## 可考虑的结合点（概览）

通用选型论证、评价门槛与比较契约以 [[../research/technical-lines/piml-research-guide#2.3 模型选型与统一比较契约]] 为准；只有学习对象进入迭代求解器时，才进一步参考 [[../research/piml-matrix-free-gpu/high-performance-solver-survey]] 的跨线科学问题。本表只做会前速查，不复制其内容。「强弱」一列是基于其公开工作覆盖面所作的判断，非其本人表态。

| 结合点 | 为什么与他相关 | 强弱 |
|---|---|---|
| **B：误差传播与模型评价** | 他缺的正是判据本身；本人可把评价从 ML 指标推进到 $\widehat K_s\to\widehat u\to\widehat{\nabla J}\to$ 拓扑差异的数值分析链 | **最强**，建议主谈 |
| **D：模型与 Krylov / 预条件子协同** | 其公开工作未见涉及迭代求解器侧；「迭代数与总 solve 时间」作为选型目标是本人独有角度 | **强** |
| **E：面向 GPU 的模型—算子融合** | 同上，其线上未见显存—算力权衡与 Roofline 分解 | **强** |
| **C：学习算子与精确算子的混合回退** | 工程软件（SiPESC/DLUTopt）落地关心的可靠性问题，与其增材制造/工程应用背景相容 | 中性 |
| **A：结构保持的输出参数化** | 与 CMAME 2026 的 Bézier 参数化同属「改参数化而非改网络容量」，**已不是空白切入点**；须按输入侧/输出侧区分后再提 | **需差异化**，勿重复其结论 |

**交付状态提醒**：上表「强弱」指的是**话题相关性**，不代表已有可交付结论。结构保持硬门槛和统一比较契约见 [[../research/technical-lines/piml-research-guide#2.3 模型选型与统一比较契约]]；B 与 D 目前都只有分散片段，尚未串成定量关系曲线，面谈时应表述为研究切入点，不可表述为已解决其选型问题。

另有一条待评估的潜在接口：**DFENN 与本人二维平面应变线弹性 PINN 门禁经验的对照**。DFENN 的卖点是取消 CPINN/CENN 的罚参数，而本人有该类问题的一手实操与门禁数据（见 [[../research/technical-lines/piml-research-guide]] 及 `log.md` 2026-07-29 条目），可作为有实操依据的对话入口。是否纳入模型选型专题，须在论文正式 ingest 后再判断。

## 概况

主页自述的三个研究方向为：复杂曲面薄壁结构显式拓扑优化方法、面向增材制造的先进结构创成式设计技术、**人工智能赋能的结构高效分析与优化新范式**。第三条是其正式研究方向，不是合作附带产物。

在 AI/ML 方向上，其署名工作多为「学生一作 + 本人二作」模式，覆盖面横跨传统回归、MLP、算子学习、图网络与 FEM–NN 耦合等多个模型族。

## 关注的方向 / 方法

- **显式拓扑优化**：MMC/MMV 几何参数化及其在薄壁、曲面、点阵结构中的推广。
- **PIML 局部力学表示与响应映射**：学习可跨宏观几何、整体边界条件和载荷复用的局部表示或响应关系，具体对象不预设为形函数或缩聚刚度。
- **算子学习与输入输出参数化**：以 DeepONet 等把离散矩阵输出改写为坐标连续函数，并通过边界场参数化提升泛化性。
- **FEM 与神经网络的一致耦合**：以变分一致的界面缩聚替代罚参数型 PINN 域分解。
- **力学超材料的数据库化设计**：以图网络建立几何参数与等效弹性张量之间的双向映射。

## 已建立文献入口的合著工作

以下条目在本库已有单篇文献入口，作者顺序以各页 frontmatter 为准。新增四篇仍为 `draft`，仅使用元数据／摘要级证据。

| 论文 | 其作者位置 | ML 方法 | 学习对象／作用 | 证据状态 |
|---|---|---|---|---|
| [[../literature/topology-opt/notes/Lei2018-machinelearningdriven]] | 第 2 作者 | PCA + SVR / KNN（未用神经网络） | 载荷位置 → MMC 组件参数（112 维定长向量） | 全文笔记 |
| [[../literature/topology-opt/notes/Huang2022-problemindependentmachine]] | 第 3 作者 | 监督式神经网络 | 局部密度 → EMsFEM 粗单元形函数 | 全文笔记 |
| [[../literature/topology-opt/notes/Huang2023-PIML-substructure]] | 第 3 作者 | 监督式神经网络 | 子结构密度 → 多尺度形函数 / 缩聚刚度 | 全文笔记 |
| [[../literature/topology-opt/notes/Huang2024-PIML-datafree]] | 第 2 作者 | DeepONet + data-free 力学损失 | 密度分支 + 坐标主干 → 坐标连续形函数 | 全文笔记 |
| [[../literature/topology-opt/notes/Zhang2024-isoparametric-PIML]] | 第 3 作者 | 机器学习 + 等参单元 | 单元几何形状与材料分布 → 数值形函数 | `draft`，摘要级 |
| [[../literature/topology-opt/notes/Xu2025-PIML-lattice-MMC]] | 第 2 作者 | PIML + MMC | 三维梯度点阵复合结构的高效分析与优化 | `draft`，摘要级 |
| [[../literature/topology-opt/notes/Ma2026-highperformanceparallel]] | 第 5 作者 | 不更换网络，转向并行与按需预测 | 多尺度形函数路线的工程化与规模化 | 全文笔记 |
| [[../literature/topology-opt/notes/Guo2026-highgeneralization-bezier]] | 第 2 作者 | DeepONet + Bézier 参数化 | 参数化边界位移场 → 子结构内部位移场 | `draft`，摘要级 |
| [[../literature/topology-opt/notes/Guo2026-PIML-OFEM]] | 第 2 作者 | U-Net + overlapping FEM | 杨氏模量分布 → 超采样数值基函数 | `draft`，arXiv v1 摘要级 |

## 尚未入库的公开工作（待 ingest 核验）

下表来源为 2026-07-30 的公开检索（个人主页、Google Scholar、出版商页面），**作者顺序、卷期、页码与 DOI 尚未经 Zotero 条目核对**，正式入库前不得作为引用事实使用。

| 年份 | 论文 | 期刊 | 模型族 | 优先级 |
|---|---|---|---|---|
| 2026 | DFENN: A penalty-free variational framework coupling finite elements and neural networks via interface condensation | JMPS 215 | FEM ⊕ NN 域分解，界面静力缩聚 | P0 |
| 2025 | Intelligent design of mechanical metamaterials: a GCNN-based structural genome database approach | National Science Review 12: nwaf053 | 图卷积网络（GCNN） | P1 |
| 2025 | Data-driven based stable analysis algorithm for nonlinear truss structures with geometric instabilities | Computational Mechanics | data-driven | P2 |

其中尚未入库的 P0 工作技术要点（据公开摘要，待精读确认）：

- **DFENN**：将计算域划分为非重叠子域，分别由有限元离散和神经网络逼近；通过静力缩聚把有限元子域的刚度贡献显式映射到界面，实现变分一致耦合，从而**避免 CPINN / CENN 所需的人为罚参数**。SSRN 预印本标题直接使用 "Hyperparameter-Free"。

## 跨源提炼：这条线本身是一部模型选型史

把上述工作按时间排列，可以看到模型更换均由**学习对象、物理约束和部署条件**驱动，而非由「哪个网络更强」驱动：

1. **2018 不用神经网络**：MMC 已把设计压缩为 112 维定长向量，独立直接优化标签仅 50/62 个，样本规模决定了 PCA + 浅层回归比神经网络更合理。
2. **2022 采用 MLP**：学习对象由「最终设计」换为「局部形函数」后，输入输出定长且标签可离线批量生成，MLP 作为最省事的基线。
3. **2024 表示与输入同时扩展**：Huang 2024 用 DeepONet 将离散形函数改为坐标连续表示；Zhang 2024 把单元几何形状与材料分布共同作为输入，扩展到复杂设计域。
4. **2025 应用对象分化**：GCNN 工作面向图邻接的超材料单胞几何—性能映射；Xu 2025 则把 PIML 与 MMC、分区坐标映射和三维梯度点阵优化结合。
5. **2026 多条路线并行**：Bézier 工作改变边界位移输入参数化，PIML-OFEM 转向超采样重叠数值基函数，DFENN 则研究消除 FEM–NN 界面耦合中的人为罚参数。

其中 Zhang 2024、Xu 2025、Guo 2026 Bézier 和 PIML-OFEM 当前只完成元数据／摘要级入库；上述定位不等同于全文证据卡或本人复现结论。

由此可以推断（**待与本人确认**）：其技术痛点并非「不了解有哪些网络」，而是「每换一个问题就要重新试一轮、重新调一轮，缺少可复用的选型判据，且调参过程本身不可靠」。DFENN 以「无罚参数」为核心卖点，是这一推断的间接佐证。

## 与我的关联

- 其 AI 方向与本人博士后方向一直接重叠；结合点速查见本页「可考虑的结合点」，通用模型选型原则与证据边界由 [[../research/technical-lines/piml-research-guide]] 维护，项目级阶段与状态由 [[../research/piml-matrix-free-gpu/project-plan]] 维护，具体交流材料由 [[../discussions/liu-chang/_index]] 维护，本页不复制其内容。
- PIML 历史证据由 [[../research/technical-lines/piml-research-guide]] 维护，条件化融合假设由 [[../research/piml-matrix-free-gpu/high-performance-solver-survey]] 维护；只有所选学习对象确实进入求解器或批量部署时，才把 Krylov 行为和 GPU 成本纳入下游评价。
- 真实沟通过程、约见安排与关系状态由沟通仓库维护，本页只保留公开学术身份与技术事实。

## 待确认

- 尚未入库表中三篇工作的作者顺序、卷期、页码、DOI 及 Citation Key，须以 Zotero 条目为准后再引用。
- 各篇中其是否为通讯作者，公开检索未能确认。
- 其在 PIML 系列中的具体分工（方法设计、学生指导或算例组织）无公开证据，不作推断。

## 相关来源

- 个人主页：<https://faculty.dlut.edu.cn/liuchang/zh_CN/>（职称、研究方向、在研项目）
- Google Scholar：<https://scholar.google.com/citations?user=B-uZM4EAAAAJ>（论文列表与年份）
- `refs.bib` cite key：`Lei2018-machinelearningdriven`、`huangProblemindependentMachineLearning2022`、`huangProblemindependentMachineLearning2023`、`Huang2024-mechanicsbaseddatafree`、`zhangProblemindependentMachineLearningenhanced2024a`、`xuProblemindependentMachineLearning2025`、`Ma2026-highperformanceparallel`、`guoHighGeneralizationAIEnhancedMechanical2026`、`guoPIMLOFEMNewLargeScale2026`

## 相关页面

- [[guo-xu]] — 其博士导师，研究体系、稳定研究方向与权威入口。
- [[../concepts/piml/method-lineage]] — 「直接预测最终设计 → 学习可复用局部算子」的方法谱系。
- [[../concepts/ml-roles-and-boundaries]] — 各类 ML 角色与问题无关性的适用边界。
- [[../research/technical-lines/piml-research-guide]] — PIML 技术线总入口。
- [[../research/technical-lines/piml-research-guide#2.3 模型选型与统一比较契约]] — 通用六维选型框架。
- [[../research/piml-matrix-free-gpu/high-performance-solver-survey]] — 条件性三线融合研究问题。
