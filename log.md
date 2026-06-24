# 时间线 · log

> Append-only。每次 ingest / query / lint / 重要 edit 追加一条。格式：
> `## [YYYY-MM-DD] <类型> | <简述>`，下挂改动文件或关键结论。只增不改历史条目。
## [2026-06-24] edit | 重构并统一 Google DeepMind 代理规则 (Codex/Antigravity)
- 将 Codex 与 Antigravity 的规则文件统一合并为 `ai/agents/AGENTS.md`，避免配置冗余。
- 提炼了真正属于 Codex & Antigravity 专用的规则补充（包括 Git 沙箱路径约束、PowerShell 中文编码写入防乱码避坑指南、命令行 Python/Node 别名限制以及 Commit 权限规范），剔除了通用的 LLM Wiki 说明。
- 删除了根目录下冗余的 `ANTIGRAVITY.md` 入口文件，将 root `AGENTS.md` 与 `CLAUDE.md` 更新为指向统一的 `ai/agents/AGENTS.md`。
- 修复了 `CLAUDE.md` 与 `AGENTS.md` 中指向 `ai/claude/` 等文件夹的链接写法，统一修改为指向对应的 `.md` 规则文件，解决 Obsidian 因无法解析纯文件夹链接而频繁在根目录误创建文件夹/文件的 Bug。


## [2026-06-24] edit | 完善文献笔记引用信息，对齐 PIML+HPC 统一文献精读模板
- 在 [[literature/topology-opt/Huang2022-problemindependentmachine]] 与 [[literature/topology-opt/Ma2026-highperformanceparallel]] 笔记头部同时保留 Zotero 引用信息（包含作者、期刊、DOI、Zotero Link）和“完整中文译文”链接，实现引文与译文信息双收录；并在 [[literature/topology-opt/Lei2018-machinelearningdriven]] 中新增了完整中文译文占位链接（待译）。
- 将误在根目录创建的译文占位笔记 [[literature/topology-opt/translations/Lei2018-machinelearningdriven-zh]] 归位移动至 `literature/topology-opt/translations/` 目录下，并清理了根目录下冗余的 `translations` 目录。
- 修复并优化了因服务器重置中断导致的 `Ma2026` 笔记历史格式损坏。

## [2026-06-24] edit | 搭建 Obsidian + Zotero + LLM 自动化知识流，重构文献引用键与笔记
- 建立 Zotero Better BibTeX 到 `assets/refs.bib` 的后台自动增量导出。
- 更换并配置 Obsidian 端的 `ZotLit` 插件（Eta 模板），使其无缝读取 Zotero 本地数据库及标注。
- 将已有文献及中文翻译（Ma2026, Huang2022）重构命名为 Zotero 自动生成的 Citation Key，全局自动修正 13 个关联文件中的双链。
- 通过 Zotero + ZotLit 导入并精读新文献 [[literature/topology-opt/Lei2018-machinelearningdriven]]，自动生成结构化笔记。

## [2026-06-24] edit | 同步博士后入站集中考核安排
- 根据 `C:\workspace\heliangos\wechat\大连理工大学博士后\teachers\石圣哲.md`，更新 `talks/2026-postdoc-entry-assessment/README.md`：记录 2026 年 7 月第一周集中考核、个人汇报 PPT 约 8 分钟、业绩一览表需确认/补交等约束。

## [2026-06-24] edit | 英文化仓库路径名
- 将入站考核答辩目录重命名为 `talks/2026-postdoc-entry-assessment/`，保留正文中文，降低 LaTeX、Git、AI 工具和跨平台路径处理的摩擦。

## [2026-06-24] init | 按 Karpathy LLM Wiki 方法论补强 Codex 知识库初始化
- 新增 [[concepts/llm-wiki]]：沉淀 LLM Wiki 的三层架构、ingest/query/lint 操作映射、人与 Codex 的分工。
- 更新 [[index]]、[[concepts/_index]]、[[CLAUDE]]、`README.md`、`assets/refs.bib`，将仓库入口从 Claude 表述切换为 Codex，并登记 `KarpathyLLMWiki`。

## [2026-06-24] edit | 参考 structural-dynamics-software 改为多 AI 工具入口
- 新增 `ai/common/llm-wiki-workflow.md`、`ai/codex/AGENTS.md`、`ai/claude/CLAUDE.md`，把通用 LLM Wiki 工作流与工具专用入口分离。
- 将根 [[AGENTS]]、[[CLAUDE]] 改为轻量入口，更新 [[index]]、[[concepts/llm-wiki]]、`README.md`，避免知识库 schema 绑定单一 AI 工具。

## [2026-06-18] lint | 归位根目录空文件 + 标记引用键不一致
- 根目录空文件 `Guo2023-PIML-substructure.md` → 移入 [[literature/others/Guo2023-PIML-substructure]]，套模板做成「待精读」存根，保留文件名以维持 [[literature/topology-opt/Huang2022-problemindependentmachine]] 的反向链接。
- 在 [[literature/_index]]「其他」区登记。
- **未决（待你确认）**：同系列 PIML 论文存在 `Guo20xx-*` 与 `Zheng20xx-*` 两套 cite key（子结构/data-free/并行），需确认真实第一作者后统一。

## [2026-06-18] init | 接入 Karpathy LLM Wiki 模式
- 新增 Schema 层 [[CLAUDE]]：三层架构、写作约定、ingest/query/lint 工作流。
- 新增根总目录 [[index]] 与本时间线 [[log]]。
- 新增 `concepts/`（概念页）、`entities/`（实体页）两区，各含 `_index.md` 与模板。
- 种子页：[[concepts/piml]]、[[entities/guo-xu-team]]（由既有 `literature/`、`research/` 内容提炼）。
- 原有 `literature/`、`research/`、`papers/`、`talks/`、`assets/` 结构保持不变。

---

### 历史回填（据 git 记录，非当日逐条）
- 2026-06-10 ingest | [[research/piml-matrix-free-execution-plan]] 执行计划，补 2019 ML-MMC 前史文献。
- 2026-06-07 ingest | [[research/piml-matrix-free-high-performance-solver-survey]]、[[research/mmc-mmv-numerical-discretization-survey]] 两篇调研。
- 2026-06-06 ingest | [[literature/topology-opt/Ma2026-highperformanceparallel]] 笔记 + 译文 + 配图。
- 2026-06-04 init | 建库：[[literature/_index]]、[[research/_index]]、[[research/guo-xu-team-overview]]、[[research/postdoc-research-plan]]、模板与 `refs.bib`。
