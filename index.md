# 知识库总目录 · index

> 全库内容地图。按 [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 模式维护：原始源 → wiki → schema 三层。工具入口见 [[AGENTS]] / [[CLAUDE]]，通用方法论见 [[concepts/llm-wiki]]，时间线见 [[log]]。
>
> **仅在稳定入口或高层导航发生变化时更新本页。** 分区细目、叶子页面和单篇状态见各 `_index.md`。

## 当前科研架构

> 本仓库以[[research/piml-matrix-free-gpu/project-plan|博士后核心研究项目]]为博士后阶段的主要牵引，而不是以某一次基金申请为科研总领。项目不因基金未获批而终止，基金获批也不等同于项目完成。

- [[research/long-term-research-lines|个人长期科研主线与博士后成果路线]]
  - **主线一：高精度数值离散与拓扑优化**——博士阶段工作的延续与成果转化，不纳入核心项目的三条推进线。
    - [[papers/arbitrary-order-huzhang-topopt-outline|Hu–Zhang 论文]]：论文框架与正文写作。
    - [[research/vem-topopt-long-term-survey|VEM 调研与论文]]：无稳定化项虚单元拓扑优化的长期调研与论文入口。
  - **主线二：智能高性能计算力学**——由[[research/piml-matrix-free-gpu/project-plan|博士后核心研究项目]]作为当前主要实施载体。
    - **精确 Matrix-Free/GPU 基线**——精确求解基线、Krylov、预条件和 CPU/GPU/MPI 证据。
    - **PIML 局部表示**——结构保持局部力学算子、模型选型、训练推理和精确回退。
    - **三线融合**——在前两条推进线门禁通过后的条件性融合与端到端验证。
- 执行与支撑
  - [[research/funding/postdoc-funding-applications|基金申请]]——核心项目的条件性资助渠道；第 80 批是第一次申请，不是项目本身。
  - [[entities/_index|实体中心与科研讨论]]——以实体（人物）为中心统一维护学术画像、导师汇报、合作者交流与师门关系，不建立第二套研究状态账。
  - [[research/piml-matrix-free-gpu/_index|PIML–Matrix-Free–GPU 项目分支]]——PIML、Matrix-Free、GPU/HPC 三个分支的研究指南和项目任务。
  - [[concepts/_index|concepts]]、[[literature/_index|literature]]——稳定知识、范式流程与论文证据；具体计算程序与运行规范由代码仓库（如 `soptx`）维护。

## 导航

| 区 | 内容 | 索引 |
|---|---|---|
| 📄 文献 | 单篇论文中文译文（`sources/` 原始 PDF + `-zh` 译文） | [[literature/_index]] |
| 🔬 研究路线与调研 | 长期主线、课题与方向综合（synthesis） | [[research/_index]] |
| 👥 实体与讨论 | 人物档案、师门关系及历次科研汇报/交流 | [[entities/_index]] |
| 💡 概念页 | 跨源概念提炼 | [[concepts/_index]] |
| ✍️ 论文草稿 | 自己写的稿件 | `papers/` |
| 🎤 活跃报告 | 准备中或仍需维护的 LaTeX 幻灯片 | [[talks/README]] |
| 🗄️ 历史档案 | 已完成事件的最终交付物与准备材料 | `archive/` |

## 论文草稿

| 稿件 | 目标期刊 | 状态 |
|---|---|---|
| [[papers/arbitrary-order-huzhang-topopt-outline\|任意次 Hu–Zhang 混合有限元拓扑优化投稿论文框架]] | CICP（首选，证据门禁后复核） | outline |
| [[papers/arbitrary-order-huzhang-topopt-draft-zh\|任意次 Hu–Zhang 混合有限元拓扑优化中文版初稿]] | CICP（首选，证据门禁后复核） | drafting |

## 文献

| 入口 | 内容 |
|---|---|
| [[literature/_index\|文献总索引]] | 当前 ingest 队列、储备候选池与研究主线导航 |
| [[literature/matrix-free/_index\|Matrix-Free 方法文献]] | 以 Matrix-Free 方法为主要贡献的译文与交叉主题链接 |
| [[literature/topopt/_index\|拓扑优化已入库文献]] | 单篇译文、原始 PDF 副本和派生图片 |

## 实体与科研讨论

| 实体 / 入口 | 类型 | 一句话 / 定位 | 状态 |
|---|---|---|---|
| [[entities/_index\|实体总索引]] | 索引 | 实体档案、科研讨论与师门关系网络总览 | in-progress |
| [[entities/guo-xu/guo-xu\|郭旭]] | 人物 / 导师 | 中国科学院院士，MMC/MMV 显式拓扑优化与 PIML 主导者，本人合作导师 | in-progress |
| [[entities/liu-chang/liu-chang\|刘畅]] | 人物 / 合作者 | 大连理工大学工程力学系教授，MMC 显式拓扑优化与 AI 赋能结构分析优化，PIML 主线全部论文共同作者 | in-progress |
| [[entities/guo-yilin/guo-yilin\|郭一麟]] | 人物 / 合作者 | 博士，PIML 方向，PIML × GPU 合作线索 | in-progress |
| [[entities/mei-yue/mei-yue\|梅跃]] | 人物 / 合作者 | 大连理工大学教授，大连工业软件创新发展研究院常务副院长，计算力学正反问题与 CAE 软件研发 | in-progress |
| [[entities/relationships\|师门链与人物关系]] | 关系 | 郭旭→刘畅→郭一麟 师门传承与合作背景 | in-progress |

## 研究路线与调研

| 课题 | 状态 |
|---|---|
| [[research/long-term-research-lines\|个人长期科研主线与博士后成果路线]] | in-progress |
| [[research/funding/postdoc-funding-applications]] | draft |
| [[research/piml-matrix-free-gpu/_index\|博士后核心研究项目：PIML Matrix-Free × GPU 协同加速]] | in-progress |
| [[research/mmc-mmv/mmc-mmv-numerical-discretization-survey]] | draft |

## 历史档案

| 档案 | 日期 | 状态 |
|---|---|---|
| [[archive/2026-postdoc-entry-assessment/README\|2026 博士后入站考核答辩]] | 2026-07-05 | archived |

## 概念页

| 概念 | 一句话 |
|---|---|
| [[concepts/llm-wiki]] | 个人 AI 知识库模式：由 AI 工具维护原始资料与研究者之间的持久 Markdown 中间层 |
| [[concepts/linear-elasticity\|线弹性]] | 小变形静力各向同性线弹性的连续模型、变分形式与 Lagrange 有限元离散 |
| [[concepts/external-loads\|外载荷]] | 体力/面牵引/集中力的对偶空间与适定性、两套变分形式下的弱施加与强施加、一致节点力与 $P_1$ 迹 $L^2$ 投影 |
| [[concepts/huzhang/_index\|胡张混合元]] | 应力—位移混合有限元的统一语义入口：鞍点结构与稳定化、程序实现必读入口、论文路线与文献证据 |
| [[concepts/density-topopt/_index\|密度法拓扑优化]] | 密度法统一语义入口：设计变量到物理响应的映射链条（过滤—投影—插值）、程序实现必读入口与文献证据 |
| [[concepts/mmc/_index\|MMC]] | MMC 统一语义入口：显式几何到优化闭环的主题地图、研究路线、文献证据与历史档案 |
| [[concepts/piml/_index\|PIML]] | PIML 统一语义入口：术语边界、子结构缩聚主题地图、程序实现必读入口、项目入口与文献证据 |
| [[concepts/matrix-free/_index\|Matrix-Free]] | Matrix-Free 统一语义入口：装配层次主题地图、程序实现必读入口、技术线入口、文献证据与关联入口 |
| [[concepts/gpu-hpc/_index\|GPU/HPC]] | GPU/HPC 统一语义入口：三层解耦主题地图、程序实现必读入口、技术线入口、文献证据与关联入口 |
| [[concepts/linear-solvers/_index|线性求解器]] | 线性方程组求解器统一语义入口：直接法 / 定常迭代 / Krylov / 多重网格分类树、程序实现必读入口与关联入口 |

---

*维护：叶子页面变化更新最近的主题 `_index.md`；只有稳定入口或高层导航变化时才同步本页。*
