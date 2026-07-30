# 知识库总目录 · index

> 全库内容地图。按 [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 模式维护：原始源 → wiki → schema 三层。工具入口见 [[AGENTS]] / [[CLAUDE]]，通用方法论见 [[concepts/llm-wiki]]，时间线见 [[log]]。
>
> **每次 ingest 后更新本页。** 分区细目见各 `_index.md`。

## 导航

| 区 | 内容 | 索引 |
|---|---|---|
| 📄 文献笔记 | 单篇论文精读（summary） | [[literature/_index]] |
| 🔬 调研 | 课题/方向综合（synthesis） | [[research/_index]] |
| 📋 工作汇报 | 自包含的会前完整底稿、会后结论与行动项 | [[work-reports/_index]] |
| 💡 概念页 | 跨源概念提炼 | [[concepts/_index]] |
| 👥 实体页 | 人/团队/方法/软件档案 | [[entities/_index]] |
| ✍️ 论文草稿 | 自己写的稿件 | `papers/` |
| 🎤 活跃报告 | 准备中或仍需维护的 LaTeX 幻灯片 | [[talks/README]] |
| 🗄️ 历史档案 | 已完成事件的最终交付物与准备材料 | [[archive/_index]] |

## 文献笔记

| 笔记 | 方向 | 年份 | 状态 |
|---|---|---|---|
| [[literature/topology-opt/Lei2018-machinelearningdriven]] | 拓扑优化 | 2019 | done |
| [[literature/topology-opt/Huang2022-problemindependentmachine]] | 拓扑优化 | 2022 | done |
| [[literature/topology-opt/Huang2023-PIML-substructure]] | 拓扑优化 | 2023 | done |
| [[literature/topology-opt/Huang2024-PIML-datafree]] | 拓扑优化 | 2024 | draft |
| [[literature/topology-opt/Ma2026-highperformanceparallel]] | 拓扑优化 | 2026 | done |

## 工作汇报

| 归档 / 汇报 | 状态 |
|---|---|
| [[work-reports/_index]] | in-progress |
| [[work-reports/guo-xu/_index]] | in-progress |
| [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] | preparing |

## 调研

| 课题 | 状态 |
|---|---|
| [[research/technical-lines/_index]] | in-progress |
| [[research/technical-lines/piml-research-guide]] | in-progress |
| [[research/technical-lines/matrix-free-research-guide]] | in-progress |
| [[research/technical-lines/gpu-hpc-research-guide]] | in-progress |
| [[research/funding/postdoc-funding-applications]] | draft |
| [[research/postdoc-plan/postdoc-research-plan]] | in-progress |
| [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-high-performance-solver-survey]] | in-progress |
| [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-gpu-and-model-selection-technical-synthesis]] | in-progress |
| [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/liu-chang-model-selection-task-line]] | in-progress |
| [[research/postdoc-plan/long-term/direction-2-mmc-mmv/mmc-mmv-numerical-discretization-survey]] | draft |

## 历史档案

| 事件 | 日期 | 状态 |
|---|---|---|
| [[archive/2026-postdoc-entry-assessment/README\|2026 博士后入站考核答辩]] | 2026-07-05 | archived |

## 概念页

| 概念 | 一句话 |
|---|---|
| [[concepts/llm-wiki]] | 个人 AI 知识库模式：由 AI 工具维护原始资料与研究者之间的持久 Markdown 中间层 |
| [[concepts/linear-elasticity\|线弹性]] | 小变形静力各向同性线弹性的连续模型、变分形式与 Lagrange 有限元离散 |
| [[concepts/piml/_index\|PIML]] | 问题无关机器学习主题入口 |
| [[concepts/matrix-free/_index\|Matrix-Free]] | Matrix-Free 稳定知识与当前研究主题入口 |
| [[concepts/gpu-hpc/_index\|GPU/HPC]] | 端到端性能模型、公开 HPC 谱系与异构并行当前研究主题入口 |

## 实体页

| 实体 | 类型 | 一句话 |
|---|---|---|
| [[entities/guo-xu]] | 人 | 郭旭：中国科学院院士，MMC/MMV 显式拓扑优化与 PIML 主导者，本人合作导师 |
| [[entities/liu-chang]] | 人 | 刘畅：大连理工大学工程力学系教授，MMC 显式拓扑优化与 AI 赋能结构分析优化，PIML 主线全部论文共同作者 |

---

*维护：每次 ingest/query 回填后更新此页与对应 `_index.md`。*
