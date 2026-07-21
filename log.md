# 时间线 · log

> Append-only。每次 ingest / query / lint / 重要 edit 追加一条。格式：
> `## [YYYY-MM-DD] <类型> | <简述>`，下挂改动文件或关键结论。只增不改历史条目。
## [2026-06-24] edit | 在通用工作流中要求主动检查前需提前询问确认
- 在通用规范 [[ai/llm-wiki-workflow.md]] 中增加了“必须提前询问用户”的限制：AI 在对关联文件进行检索校验以及对 index/log 进行自动检查更新前，必须提前向用户说明并征得确认，确保用户对检查过程知情。

## [2026-06-24] edit | 在通用工作流中新增关联文件同步更新校验规则
- 在通用规范 [[ai/llm-wiki-workflow.md]] 中增加了“关联更新与同步校验”的约定，要求在修改或新建任何 wiki 文件后，必须主动检查与它关联的其它文件，确保它们同步更新。

## [2026-06-24] edit | 重构并统一 Google DeepMind 代理规则 (Codex/Antigravity)
- 将 Codex 与 Antigravity 的规则文件统一合并为 `ai/agents/AGENTS.md`，避免配置冗余。
- 提炼了真正属于 Codex & Antigravity 专用的规则补充（包括 Git 沙箱路径约束、PowerShell 中文编码写入防乱码避坑指南、命令行 Python/Node 别名限制以及 Commit 权限限制），剔除了通用的 LLM Wiki 说明。
- 在通用规则 [[ai/llm-wiki-workflow]] 中新增了“主动检查与自动更新索引/日志”的强制性 AI 行为规范，使其作为通用的 Wiki 准则同时适用于 Claude Code、Codex 和 Antigravity。
- 删除了根目录下冗余的 `ANTIGRAVITY.md` 入口文件，将 root `AGENTS.md` 与 `CLAUDE.md` 更新为指向统一的 `ai/agents/AGENTS.md`。
- 修复了 `CLAUDE.md` 与 `AGENTS.md` 中指向 `ai/claude/` 等文件夹的链接写法，统一修改为指向对应的 `.md` 规则文件，解决 Obsidian 因无法解析纯文件夹链接而频繁在根目录误创建文件夹/文件的 Bug。
- 同步更新了根目录下的 `README.md`，增加 Antigravity 的说明并对齐了最新的目录结构图。



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
- 2026-06-10 ingest | [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-execution-plan]] 执行计划，补 2019 ML-MMC 前史文献。
- 2026-06-07 ingest | [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-high-performance-solver-survey]]、[[research/postdoc-plan/long-term/direction-2-mmc-mmv/mmc-mmv-numerical-discretization-survey]] 两篇调研。
- 2026-06-06 ingest | [[literature/topology-opt/Ma2026-highperformanceparallel]] 笔记 + 译文 + 配图。
- 2026-06-04 init | 建库：[[literature/_index]]、[[research/_index]]、[[research/teams/guo-xu-team-overview]]、[[research/postdoc-plan/postdoc-research-plan]]、模板与 `refs.bib`。

## [2026-06-30] edit | Huang 2023 子结构 PIML Zotero 协同框架
- 从 Zotero 本地库确认 Huang et al. 2023 条目（DOI: 10.1016/j.eml.2023.102041，Zotero key `5XMDKI6A`，Better BibTeX key `huangProblemindependentMachineLearning2023`）与 PDF 附件；当前 Zotero notes/annotations 为空。
- 新增 `literature/topology-opt/Huang2023-PIML-substructure.md` 与 `literature/topology-opt/translations/Huang2023-PIML-substructure-zh.md`（完整中文译文承载页，当前仅建章节框架、后续逐步补译），将旧 `literature/others/Guo2023-PIML-substructure.md` 改为重定向页。
- 更新 `assets/refs.bib`、`literature/_index.md`、`ai/common/progress-part2-piml.md` 与 `research/postdoc-plan/defense-sprint/direction-1-piml-matrix-free/soptx-piml-multiscale-integration-plan.md`：当前仅确认 Huang 2023 的 Zotero 元数据并建立笔记/译文框架，论文尚未正式精读；子结构路线、预测对象、误差指标与 V4 对照口径待后续精读回填。

## [2026-06-30] edit | research 目录按博后计划重组
- 将 `research/` 从单层混放重组为 `postdoc-plan/long-term/`、`postdoc-plan/defense-sprint/` 与 `teams/`：长期调研/执行计划归入 long-term，入站答辩短期数学原则与 SOPTX 集成计划归入 defense-sprint。
- 更新 `research/_index.md`、根 `index.md` 以及显式 `research/...` 路径链接；保留 `research/assets/` 与 `research/figures/` 作为共享资源目录。

## [2026-06-30] edit | 沉淀目录 `_index.md` 优先规则
- 更新 `ai/agents/AGENTS.md` 与 `ai/common/llm-wiki-workflow.md`：Codex/AI 访问内容目录时应先读该目录 `_index.md`；新增、移动、删除或重组目录内容后，收尾必须检查并提醒同步对应 `_index.md`，必要时同步根 `index.md`。
- 同步更新 `ai/claude/CLAUDE.md`，使 Claude Code 专用入口遵循同一目录 `_index.md` 优先与索引同步规则。

## [2026-06-30] edit | 修正 Huang 2023 阅读状态
- 修正 `ai/common/progress-part2-piml.md`、`literature/topology-opt/Huang2023-PIML-substructure.md`、`literature/_index.md` 与 PIML 短期集成计划中的表述：Huang 2023 目前仅完成 Zotero 元数据确认和笔记/译文框架，论文尚未正式精读；相关技术结论、V4 对照口径与答辩表述均待后续精读回填。

## [2026-06-30] edit | 同步根目录门面文件
- 更新根 `index.md`：补登 Huang 2023 draft 文献页与入站答辩短期执行计划入口。
- 更新 `README.md`：说明 `research/` 新结构、目录 `_index.md` 优先规则，以及当前博士后研究计划两大方向与答辩冲刺入口。

## [2026-06-30] edit | 沉淀根门面文件同步规则
- 更新 `ai/common/llm-wiki-workflow.md`：明确 `index.md`、`log.md`、`README.md` 分别是全库地图、时间线与人类入口，是 LLM Wiki 根门面文件；重要内容、目录、规则或状态变化后需收尾检查三者是否同步。
- 同步更新 `ai/agents/AGENTS.md` 与 `ai/claude/CLAUDE.md`，让 Codex/Antigravity 与 Claude Code 都遵循根门面文件同步规则。

## [2026-07-02] edit | 新增帧 7 PIML guide 并修正 MMC 单帧入口
- 新增 [[research/postdoc-plan/defense-sprint/direction-1-piml-matrix-free/frame7_piml_pipeline_guide]]：统一帧 7 的子结构缩聚路线、实测结果、答辩口径、边界与后续补数方式。
- 将 MMC 方向二短期入口从已删除的 `mmc_math_principles` / `soptx-mmc-integration-plan` 修正为 [[research/postdoc-plan/defense-sprint/direction-2-mmc-mmv/frame10_mmc_pipeline_guide]]。
- 同步更新 `ai/status.md`、[[ai/common/progress-part2-piml]]、[[ai/common/progress-part2-mmc]] 与 [[research/_index]]。
## [2026-07-02] edit | 删除被单帧 guide 接管的旧入口文档
- 删除方向一 Matrix-Free 旧入口 `matrix_free_math_principles.md` 与 `soptx-matrix-free-integration-plan.md`，帧 8 后续统一接续 [[research/postdoc-plan/defense-sprint/direction-1-piml-matrix-free/frame8_matrix_free_pipeline_guide]]。
- 确认方向二 MMC 旧入口 `mmc_math_principles.md` 与 `soptx-mmc-integration-plan.md` 已处于删除状态，后续统一接续 [[research/postdoc-plan/defense-sprint/direction-2-mmc-mmv/frame10_mmc_pipeline_guide]]。
- 同步清理 [[research/_index]]、`ai/status.md`、[[ai/common/progress-part2-piml]]、[[ai/common/progress-part2-mmc]] 与帧 8 guide 中的旧入口引用。

## [2026-07-02] edit | 新增 8 分钟汇报 Part 1 逐字讲稿
- 在 `talks/2026-postdoc-entry-assessment/` 目录下新增 `script-8min.md` 作为 8 分钟汇报的逐字口语讲稿。
- 扩写了帧 2 方法一的讲解细节（包括离散构造机制与单分辨率网格绑定的局限性），方便排练时按需裁剪。
- 同步更新该目录的 `README.md` 文件树结构。
- 扩写了帧 3 方法二的讲解细节（明确了三层网格解耦机制，并利用应力不连续的痛点设计了向方法三的天然过渡）。
- 扩写了帧 4 方法三的讲解细节（详细解释了 $H(\mathrm{div})$ 空间与抗体积闭锁的原理，并增加了应力约束成果的口头引申表达）。

## [2026-07-03] edit | 沉淀入站考核答辩最终口径
- 更新 `ai/status.md`：确认当前 16 页 PPT 与 Part 2 逐帧 guide 可作为定稿口径，后续只做错别字、事实源或版式级 QA。
- 明确 `script-8min.md` 只作为 Part 1 连续讲稿入口；Part 2 不再汇总进该文件，后续以帧 6/7/8/9/10/11 guide 为权威入口。
- 沉淀全局审查顺序：先看整体叙事，再逐帧核对 PPT 与对应 guide；郭旭老师期望与计算数学特色主要由帧 6、10、11 及口头讲法承接。

## [2026-07-20] edit | 沉淀郭旭老师近期技术汇报与模型选型框架
- 新增 [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-gpu-and-model-selection-technical-synthesis]]：严格区分已完成、正在准备和后续设想，统一梳理 PIML、Matrix-Free、GPU/HPC 证据、研究院现实任务、六步融合路线及科学计算约束下的模型选型 benchmark。
- 新增 [[research/postdoc-plan/guo-xu-meeting-briefing-2026-07]]：形成面向郭旭老师的汇报要点、事实边界、近期路线和待请教问题，后续可回到 `heliangos` 压缩成当面口语稿。
- 同步 [[research/_index]]、[[index]] 与 `ai/status.md`；修正 [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-execution-plan]] 和 [[concepts/piml/method-lineage]] 中 Huang 2023/2024 已完成阅读后的过期状态，不改变长期里程碑完成度。

## [2026-07-21] edit | 简化 AI 配置与工作流目录
- 将 Codex/Antigravity 与 Claude Code 的项目规则分别收敛到根目录 `AGENTS.md`、`CLAUDE.md`，删除原有 `ai/agents/` 与 `ai/claude/` 两层转发入口。
- 将 5 份共享状态与工作流文档从 `ai/common/` 上移到 `ai/`，同步修正现行导航、Schema 说明、内部链接和状态入口。
- 保留历史日志中的旧路径事实及外部 `soptx` 路径，不提交、不推送。

## [2026-07-21] edit | 删除 AI 状态总账并强化提交前门面检查
- 删除 `ai/status.md`；当前研究状态由根 `index.md`、领域 `_index.md`、具体研究/汇报文档和逐帧 guide 分别承载，不再维护第二套跨领域状态总账。
- 统一根工具规则、Git 工作流和 LLM Wiki 工作流的提交前门禁：每次有意义的提交更新 `log.md`，并强制检查、按需更新 `index.md` 与 `README.md`。
- 本次 `README.md` 已同步目录结构和提交规则；`index.md` 已检查，内容入口未受影响，无需修改。

## [2026-07-21] edit | 收敛 AI 规则为单一事实源
- 精简根 `AGENTS.md` 与 `CLAUDE.md`：只保留标准入口和工具特有补充，不再复制 `_index`、提交门禁、PPT、Git/SSH 或易过期环境规则。
- 在 `ai/llm-wiki-workflow.md` 统一定义 PPT/讲稿、论文翻译和 Git 提交/推送三类按需路由；完整提交门禁仅由 `ai/git-workflow.md` 承载。
- 将 Codex Git 沙箱兜底收敛到 Git 工作流“本机现状”，Poppler 路径继续由 PPT 专项工作流承载；`README.md` 已同步，`index.md` 已检查且无需修改。
- 提交尾注改为按实际协作工具填写；本次由 Codex 执行，不再固定使用 Claude 署名。
