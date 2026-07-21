# 知识库总目录 · index

> 全库内容地图。按 [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 模式维护：原始源 → wiki → schema 三层。工具入口见 [[AGENTS]] / [[CLAUDE]]，通用方法论见 [[concepts/llm-wiki]]，时间线见 [[log]]。
>
> **每次 ingest 后更新本页。** 分区细目见各 `_index.md`。

## 导航

| 区 | 内容 | 索引 |
|---|---|---|
| 📄 文献笔记 | 单篇论文精读（summary） | [[literature/_index]] |
| 🔬 调研 | 课题/方向综合（synthesis） | [[research/_index]] |
| 💡 概念页 | 跨源概念提炼 | [[concepts/_index]] |
| 👥 实体页 | 人/团队/方法/软件档案 | [[entities/_index]] |
| ✍️ 论文草稿 | 自己写的稿件 | `papers/` |
| 🎤 报告讲稿 | LaTeX 幻灯片 | `talks/` |

## 文献笔记

| 笔记 | 方向 | 年份 | 状态 |
|---|---|---|---|
| [[literature/topology-opt/Lei2018-machinelearningdriven]] | 拓扑优化 | 2018 | done |
| [[literature/topology-opt/Huang2022-problemindependentmachine]] | 拓扑优化 | 2022 | done |
| [[literature/topology-opt/Huang2023-PIML-substructure]] | 拓扑优化 | 2023 | done |
| [[literature/topology-opt/Huang2024-PIML-datafree]] | 拓扑优化 | 2024 | draft |
| [[literature/topology-opt/Ma2026-highperformanceparallel]] | 拓扑优化 | 2026 | done |

## 调研

| 课题 | 状态 |
|---|---|
| [[research/postdoc-plan/postdoc-research-plan]] | in-progress |
| [[research/postdoc-plan/guo-xu-meeting-briefing-2026-07]] | in-progress |
| [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-high-performance-solver-survey]] | in-progress |
| [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-execution-plan]] | in-progress |
| [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-gpu-and-model-selection-technical-synthesis]] | in-progress |
| [[research/postdoc-plan/long-term/direction-2-mmc-mmv/mmc-mmv-numerical-discretization-survey]] | draft |
| [[research/postdoc-plan/defense-sprint/one-week-defense-sprint-plan]] | in-progress |
| [[research/teams/guo-xu-team-overview]] | done |

## 概念页

| 概念 | 一句话 |
|---|---|
| [[concepts/llm-wiki]] | 个人 AI 知识库模式：由 AI 工具维护原始资料与研究者之间的持久 Markdown 中间层 |
| [[concepts/piml]] | 问题无关机器学习：学习可复用局部力学表示，用于拓扑优化与高效分析 |
| [[concepts/piml/method-lineage]] | PIML 方法谱系：EMsFEM 形函数、子结构缩聚、data-free 与并行大规模优化 |

## 实体页

| 实体 | 类型 | 一句话 |
|---|---|---|
| [[entities/guo-xu-team]] | 团队 | 郭旭院士团队：MMC/MMV 显式拓扑优化、PIML、多尺度、SiPESC、混合变分数值方法 |

---

*维护：每次 ingest/query 回填后更新此页与对应 `_index.md`。*
