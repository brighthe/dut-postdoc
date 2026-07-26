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
- 种子页：[[concepts/piml/mathematical-foundations]]、[[entities/guo-xu-team]]（由既有 `literature/`、`research/` 内容提炼）。
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

## [2026-07-21] edit | 为 Claude Code 启用共享工作流自动导入
- 在根 `CLAUDE.md` 中使用 `@ai/llm-wiki-workflow.md`，由 Claude Code 在会话启动时自动加载共享工作流，不再依赖模型主动读取。
- 保留 `index.md` 按任务读取及全部 Claude Code 专用补充；`index.md` 与 `README.md` 已检查，本次不改变内容地图、目录结构或人类入口说明，无需修改。

## [2026-07-21] edit | 机器级 git/SSH 配置上移至 workstation 仓库
- `ai/git-workflow.md` 瘦身：新机启动语、原生 git 原则、SSH over 443、一次性配置、本机现状、排错等账户级/机器级内容统一由 `workstation` 仓库 `git/README.md` 承载（含匿名可读的 raw URL），本文件只保留 dut-postdoc 特有的操作要点（远程地址、Codex 沙箱 `--git-dir` 兜底）与提交纪律（根门面文件门禁等）。
- `ai/llm-wiki-workflow.md` 提交前门禁一句的表述同步微调，说明机器级 Git/SSH 事实已外移。
- `index.md` 与 `README.md` 已检查：内容地图与目录结构均未变化（`ai/git-workflow.md` 文件仍在原位），无需修改。

## [2026-07-21] edit | 建立根级工作汇报归档并整理郭旭老师汇报材料
- 新建 [[work-reports/_index]]、[[work-reports/guo-xu/_index]] 与 [[assets/templates/advisor-work-report]]，定义工作汇报事实源分工、`preparing → reported → follow-up-done` 生命周期和复用模板。
- 将郭旭老师近期汇报正文迁移为 [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]]；原 [[research/postdoc-plan/guo-xu-meeting-briefing-2026-07]] 保留为唯一历史 redirect。
- 更新 [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-gpu-and-model-selection-technical-synthesis]]：统一“已经完成 / 正在准备 / 后续设想”状态口径，明确 PIML、Matrix-Free、GPU/HPC 与模型选型合作线索的事实边界。
- 同步 [[index]]、`README.md` 与 `ai/llm-wiki-workflow.md`，把 `work-reports/` 定义为根级 Wiki 内容类型；[[research/_index]] 恢复为研究计划、调研与技术综合入口。
- 跨仓库沟通记录与研究院任务文件仅作只读参考，未修改。

## [2026-07-21] edit | 去重郭旭老师当面汇报的跨仓库提纲
- 在 [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] 增加“入站流程 → 研究院任务 → 科研主线 → 模型选型线索”的当面汇报顺序，并保持原有技术章节编号不变。
- 技术汇报页只保留刘畅老师所提模型选型问题的技术背景、评价框架和合作边界，不再复制发送材料等真实沟通过程。
- `heliangos` 联系人档案同步压缩为约见、行政状态、事实源指针和会面礼节；研究院实时任务仍以 `dut-institute-work/hpc/plan.md` 为准。
- 检查根 [[index]] 与工作汇报两级 `_index.md`：现有入口和事实源分工仍准确，无需修改。

## [2026-07-21] edit | 将工作汇报重构为自包含的完整底稿
- 将 [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] 从偏技术提纲重排为十三章完整工作汇报，补入可直接口述的入站进展、研究院任务及衔接关系，并恢复刘畅老师合作线索的必要沟通背景。
- 明确“汇报页自包含、外部事实源持续维护”的边界：本页保留完成本次汇报所需的带日期事实快照，不复制具体财务账号、逐字微信、完整行政流水或研究院实时任务账。
- `heliangos` 郭旭老师档案删除重复的四方面汇报提纲，只在约见待办中保留本汇报页路径和会面礼节；聊天记录与行政历史保持不变。
- 同步 [[index]]、`README.md`、`ai/llm-wiki-workflow.md`、工作汇报两级索引和通用模板，将工作汇报统一定义为“自包含的会前完整底稿、会后结论与行动项”。

## [2026-07-21] edit | 按三条技术线重构工作汇报的科研部分
- 将 [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] 第四节改为 PIML、Matrix-Free、GPU/HPC 三条技术线，每条线统一呈现“已完成、汇报边界、后续工作”。
- 将 `soptx` 单次 GPU MatVec 加速与内存数据归入 GPU/HPC，Matrix-Free 部分聚焦算子正确性、状态方程和求解器接口；原有数值不变。
- 第五节收敛为局部—全局接口、结构保持、Krylov 收敛、端到端性能和优化闭环等跨线问题；第六节只维护整体融合顺序、理由和首批交付结果。
- 关联页与索引已检查，没有页面依赖第四至第六节旧标题，无需同步修改。

## [2026-07-21] edit | 建立跨方向复用的三条长期技术线
- 新建 [[research/technical-lines/_index]]，明确长期技术线不从属于固定的研究方向编号，并区分技术线 guide、概念页、科研计划、综合页、答辩 guide 与工作汇报的职责。
- 新建 [[research/technical-lines/piml-research-guide]]、[[research/technical-lines/matrix-free-research-guide]] 与 [[research/technical-lines/gpu-hpc-research-guide]]，分别沉淀数学/执行对象、当前证据、事实边界、工作包、Benchmark、里程碑、风险和跨线接口。
- 同步 [[research/_index]]、根 [[index]] 与 `README.md`，登记 `research/technical-lines/`；在郭旭老师工作汇报第四节和当前融合 synthesis 中补充三份长期 guide 入口。
- 原 `direction-1-piml-matrix-free/` 下综合调研和执行计划暂不移动，继续负责当前博士后计划中的跨线组合与阶段安排。

## [2026-07-21] ingest | 统一 Matrix-Free 五级装配层次与项目定位
- 新建 [[concepts/matrix-free/assembly-levels]]，采用兼容 libCEED 与 MFEM 的 `FA/TA → LA → EA/EbE → PA/QA → UA/NONE` 五级存储分类，并区分广义 Matrix-Free、严格 UA/NONE 与 Shell Matrix 接口。
- 更新 [[research/technical-lines/matrix-free-research-guide]]：将当前基础区分为积分点 contraction 原型、`mfleo` PA 工程路径和 `xihe/matrix_free_3` EA/EbE 分布式 Maxwell 原型，明确各自证据边界。
- 同步 [[concepts/_index]]、[[research/technical-lines/_index]]、根 [[index]]、长期综合调研与帧 8 答辩 guide；工作汇报现有 `mfleo PA / Matrix-Free` 表述准确，保持不改。
- 两个公司仓库只按 `origin/develop` 做只读事实核对，未复制代码、内部数据或客户算例，也未修改公司仓库。

## [2026-07-22] edit | 收敛 Matrix-Free 技术线指南边界
- 重构 [[research/technical-lines/matrix-free-research-guide]]，删除 PIML 和 GPU/HPC 的研究任务、融合路线与跨线接口，只保留 Matrix-Free 的装配层次、算子作用、Krylov、预条件、更新策略和软件接口。
- 将原 PIML 接入工作包替换为 EA/EbE、PA/QA 与 UA/NONE 的装配层级和更新策略对照；验收、交付物与风险统一改为应用无关口径。
- 保留 `mfleo` C++/CUDA PA 路径、`xihe/matrix_free_3` MPI EA/EbE 路径和当前多后端原型，作为 Matrix-Free 分类与实现事实，而不在本页展开硬件性能工程。
- 经授权检查反向引用、技术线索引、根索引和工作汇报；现有入口描述与调整后的边界一致，无需同步修改。

## [2026-07-22] edit | 强化 xihe 的 EA/EbE 工程关系
- 在 [[research/technical-lines/matrix-free-research-guide]] 中将本地 `C:\workspace\xihe` 的 `origin/develop/examples/matrix_free_3` 定位为 EA/EbE 的主要工程实现与验证基础之一。
- 明确该路径采用 Python、FEALPy backend 与 MPI CPU 多进程，保存单元局部张量并执行 gather、局部作用、scatter-add 和共享自由度同步；不将其误写为固定 PyTorch/CUDA 或专门的 OpenMP 多线程实现。
- 用关系表区分当前 contraction 原型、`mfleo` PA/QA 工程基础和 `xihe` EA/EbE 分布式应用基础，并保留各自正确性、收敛性和集成边界。
- `xihe` 继续作为公司仓库独立维护；本知识库只记录高层方法和验证结论，不复制代码、内部数据、运行日志或客户算例，也不建立跨仓库运行依赖。

## [2026-07-22] edit | 将 Matrix-Free 技术线升级为统一框架目标
- 在 [[research/technical-lines/matrix-free-research-guide]] 中确立 FA/TA、LA、EA/EbE、PA/QA、UA/NONE 五级装配，Python/C++ 双语言，以及 CPU/GPU、single/MPI 的完整目标支持矩阵。
- 增加离散问题、装配策略、算子协议、执行后端、分布式、求解预条件和诊断 Benchmark 七层架构，并定义 `setup/update/apply/diagonal`、真残差和跨实现一致性的最低支持语义。
- 将工作包重构为统一规范、Python CPU/MPI、C++ CPU/MPI、GPU-aware MPI、预条件与收敛保障、统一 Benchmark 六个阶段，首个共享参考问题采用现有线弹性能力而不重复实现成熟有限元组件。
- 明确算子与预条件器可以采用不同装配层级；框架完成态必须逐格验证五级 × 双语言 × CPU/GPU × single/MPI，缺少预条件、真残差或 GPU-aware MPI 证据的组合不得标为完成。

## [2026-07-22] query | 审计统一 Matrix-Free 框架的当前覆盖差距
- 基于当前可访问事实源整理 [[research/technical-lines/matrix-free-research-guide]] 的现状矩阵：`xihe` 提供 Python EA/EbE CPU/MPI 原型，`mfleo` 提供 C++ PA/QA CPU/GPU/MPI 工程基础，当前 contraction 原型提供单 rank Python 多后端证据。
- FEALPy/SOPTX 线弹性组件由用户确认存在，但当前环境没有对应本地仓库或可重放入口，因此只作为待恢复的可复用基础，不把间接资料当作完成证据。
- 当前主要缺口是五级统一协议、Python GPU-aware MPI、C++ EA/UA、跨语言共享测试、完整预条件组合和自动验收状态账；目标支持矩阵仍是完成态，不代表现状。

## [2026-07-22] edit | 完成郭旭老师第一次线下汇报最终承载文档
- 将 [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] 重构为单文件分层入口：前部为 15–20 分钟连续口述主稿，后部保留技术证据、融合路线、模型选型线索、事实边界和会后行动项。
- 只读核对 `heliangos` 行政/沟通记录、`dut-institute-work/hpc/plan.md` 任务状态，以及本库帧 7/8/9 guide 和三条技术线指南；统一 `1.6e-3/8.2e-3`、`11.9×`、`3.72×–12.74×` 等数字的准确口径。
- 同步 [[work-reports/guo-xu/_index]]，将会前汇报与待请教问题标为已准备；根 [[index]]、工作汇报总索引、研究页与 README 已检查，现有入口、状态和职责未变化，无需修改。

## [2026-07-22] edit | 将首次汇报收敛为四项任务
- 根据用户确认，将 [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] 的会前内容明确收敛为四部分：入站进展、研究院任务、PIML × Matrix-Free × GPU 科研主线、与刘畅老师的讨论。
- 删除现场快速导航、时间配额、独立证据区、风险提示表等过度分层；关键数字、事实边界和待请教问题改为就近放入对应任务。
- PIML、Matrix-Free、GPU 作为第三项科研任务内部的一条融合主线，不再在顶层拆成多个任务；会后记录明确标注为不属于会前四部分。

## [2026-07-22] edit | 增加首次汇报四项任务追踪
- 在 [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] 顶部增加四个 Todo，分别追踪入站进展、研究院任务、科研主线和与刘畅老师讨论四部分是否达到可汇报状态。
- 明确 Todo 勾选表示事实已核对、内容已定稿，不表示已经实际向郭老师汇报；页面生命周期继续保持 `preparing`。

## [2026-07-22] edit | 标明入站任务的 heliangos 关联
- 在 [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] 的任务追踪、汇报结构和第一部分标题中标明“入站进展”关联 `heliangos`。
- 明确入站手续、真实沟通和约见状态以 `heliangos` 为事实源，本汇报页只保存本次汇报所需的状态快照；未修改外部仓库。

## [2026-07-22] edit | 基于 heliangos 完成入站进展部分
- 只读核对 `heliangos` 中石圣哲、郭旭、刘畅等联系人档案，将 [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] 第一部分更新为“已完成—当前节点—后续流程”。
- 确认 7 月 5 日入站考核已完成，7 月 17 日导师出资报销单已代签、盖章并提交；当前等待审核表补章照片和系统退回，重新提交后衔接人事处入职及 A 字楼 210 登记。
- 勾选“入站进展”Todo，并将四部分总进度改为 `1/4`；`heliangos` 仅作为只读事实源，未作修改。

## [2026-07-22] edit | 将入站进展压缩为现场口述
- 按工作汇报承载文档的定位，将 [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] 第一部分从流程账压缩为一段可直接向郭旭老师口述的内容。
- `heliangos` 继续作为事实源，但审核表、系统退回和入职登记等细节不再在汇报页展开维护。

## [2026-07-22] edit | 标明研究院任务的 dut-institute-work 关联
- 在 [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] 的任务追踪、汇报结构和第二部分标题中标明“研究院任务”关联 `dut-institute-work`。
- 本汇报页只承载向郭旭老师汇报的内容，研究院任务实时状态继续由外部仓库维护；未修改 `dut-institute-work`。

## [2026-07-22] edit | 将科研主线拆分为三条技术线
- 将 [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] 第三项任务明确关联 `research/technical-lines/`，内部按 PIML、Matrix-Free、GPU/HPC 三点展开。
- 三线融合调整为三点之后的收束，保留“精确 $K_s$ Matrix-Free → Krylov/预条件 → PIML 替换 → GPU”的近期顺序和必要请教问题。

## [2026-07-22] edit | 统一首次汇报任务的仓库级关联
- 将 [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] 第三项科研主线的顶层关联从内部目录 `research/technical-lines/` 修正为仓库 `dut-postdoc`，与前两项保持同一抽象层级。
- `research/technical-lines/` 继续作为 `dut-postdoc` 内部三条技术线的内容入口，不再作为顶层任务关联对象。

## [2026-07-22] edit | 删除科研主线的冗余本仓库标记
- 删除 [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] 第三项科研主线在 Todo、汇报结构和标题中的“关联 `dut-postdoc`”；当前仓库上下文已隐含该归属。
- 仅对 `heliangos`、`dut-institute-work` 等跨仓库事实源保留显式关联标记。

## [2026-07-22] edit | 强调前两项关联外部仓库
- 将 [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] 前两项在 Todo、汇报结构和章节标题中的关系统一写为“关联外部仓库”，分别指向 `heliangos` 和 `dut-institute-work`。
- 当前仓库内的科研主线继续不加仓库标记，以区分跨仓库事实引用与本库内容。

## [2026-07-22] edit | 从章节标题移除外部仓库标记
- 将 [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] 第一、第二部分的标题恢复为“入站进展”和“研究院任务”。
- 外部仓库关联仅保留在任务追踪与汇报结构中，不再写入现场汇报的章节标题。

## [2026-07-22] edit | 标明 Matrix-Free 子任务关联范围
- 在 [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] 的 `3.2 Matrix-Free` 下标明内部文档 [[research/technical-lines/matrix-free-research-guide]]，以及外部仓库 `xihe`、`mfleo`。
- 关联信息独立置于正文开头，不写入小节标题；公司仓库仅作为事实来源，不复制代码、内部数据或内部文档。

## [2026-07-22] edit | 精简 Matrix-Free 装配层次概念页
- 将 [[concepts/matrix-free/assembly-levels]] 从项目事实与研究进度混合页精简为概念判定页，保留统一算子表示、五级分类、框架术语映射、快速识别及算子/预条件器层级关系。
- 移除重复的五级逐项展开、当前项目映射、Benchmark 字段和开放研究问题；这些内容已由 [[research/technical-lines/matrix-free-research-guide]] 的当前基础、研究问题、验收指标和推进路线承接。
- 同步修正根索引、长期技术线索引和 Matrix-Free guide 中对概念页职责的说明；汇报页入口与内容无需修改。

## [2026-07-22] edit | 补充 Matrix-Free 第三方框架映射
- 在 [[concepts/matrix-free/assembly-levels]] 的框架术语映射中补充 deal.II、Firedrake、DOLFINx 和 NGSolve，并保留 libCEED、MFEM、PETSc 的代表性入口。
- 明确区分装配层级与 Shell/隐式算子接口：仅凭 `MATSHELL`、`ImplicitMatrix`、`nonassemble=True` 或 `operator.apply()` 不能判定 EA、PA 或 UA。
- 仅记录官方入口和分类边界，不扩展为 API 教程、性能排名或软件选型文档。

## [2026-07-22] edit | 重构 Matrix-Free 技术线研究指南
- 将 [[research/technical-lines/matrix-free-research-guide]] 收敛为“技术线目标—当前已有基础—成果边界—目标差距—实施路线—验收标准—事实来源”七部分，集中回答目前已经做到什么和未来准备做到什么。
- 将现状明确分为“已完成、部分完成或待核实、尚未完成”，保留 contraction 原型、`mfleo` PA 工程路径和 `xihe/matrix_free_3` EA/EbE 原型的证据边界，不将三类基础写成已融合系统。
- 下一步路线依次覆盖统一规范与参考基线、Python CPU/MPI、C++ 对齐、预条件与 GPU/GPU-aware MPI、精确 $K_s$ 到 PIML $\widehat K_s$ 的融合；验收继续要求真残差、预条件成本、峰值内存和端到端 solve。
- 同步更新 [[research/_index]]、[[research/technical-lines/_index]] 和 [[concepts/matrix-free/assembly-levels]] 中的 guide 定位说明；汇报页无需修改。

## [2026-07-22] edit | 明确 Matrix-Free 当前以线弹性求解为主
- 在 [[research/technical-lines/matrix-free-research-guide]] 的定位区和目标边界中明确以三维线弹性方程作为首个统一参考问题，优先建立 Matrix-Free 算子、Krylov、预条件及 CPU/GPU/MPI 验证闭环。
- 保留长期技术线的通用标题；Maxwell/PML 现阶段仅作为已有 EA/EbE 分布式实现的工程参考，在线弹性闭环后再用于检验跨 PDE 通用性。

## [2026-07-22] edit | 将 xihe 算例验证设为 Matrix-Free 第一阶段
- 重写 [[research/technical-lines/matrix-free-research-guide]] 的下一步路线：先恢复、跑通并验证 `xihe/matrix_free_3`，再提取 EA/EbE 分布式接口、迁移三维线弹性、对齐 `mfleo` PA/单 GPU 路径，最后接入精确 $K_s$ 与 PIML $\widehat K_s$。
- 第一阶段明确当前缺少仓库内默认网格、`pyproject.toml` 未显式声明 `fealpy`、README 无运行命令且已有日志未收敛；仅运行到结束不算完成，验收要求固定环境和输入、通过 1 rank/2 ranks 检查并记录真实残差、制造解误差和切向边界误差。
- 同步 [[work-reports/guo-xu/2026-07-piml-matrix-free-gpu]] 与 [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-gpu-and-model-selection-technical-synthesis]] 的近期顺序；长期执行计划保持不变，未修改或运行公司仓库 `xihe`。

## [2026-07-26] edit | 建立郭旭老师团队 Matrix-Free 方法谱系框架
- 新建 [[concepts/matrix-free/_index]] 与 [[concepts/matrix-free/method-lineage]]，参照 PIML 的概念谱系/当前研究指南分层，为后续团队公开成果提供稳定入口和统一更新规则。
- 当前只将 [[literature/topology-opt/Ma2026-highperformanceparallel]] 列为直接节点，明确其 `matrix-free` 是多尺度形函数按需预测和释放；粗网格全局缩聚矩阵仍组装，按五级分类属于第 1 级 FA/TA。
- 在 [[concepts/matrix-free/assembly-levels]] 增加易混淆案例，在 [[research/technical-lines/matrix-free-research-guide]] 增加团队公开成果与当前技术线的衔接；同步必要索引、PIML 谱系、文献笔记和团队实体页，不把未来计划写成既有成果。

## [2026-07-26] edit | 迁移 Matrix-Free 装配层次并补充 Ma2026 接续目标
- 将唯一权威装配层次页迁移为 [[concepts/matrix-free/assembly-levels]]，与 [[concepts/matrix-free/method-lineage]] 共同归入 Matrix-Free 子知识库；不保留旧路径占位页，并同步全库 wikilink。
- 在 [[research/technical-lines/matrix-free-research-guide]] 中明确以 Ma2026 的 FA/TA 全局缩聚系统为参考，依次建立 LA 显式 MPI 基线、EA/EbE 子结构算子、PA-like 因子化作用和 UA/NONE 按需作用。
- LA 用于分布式显式对照、通信验证和预条件基础，不作为核心 Matrix-Free 成果；精确 $K_s^j$ 闭环后再接入 PIML 预测的 $\widehat K_s^j$。

## [2026-07-26] edit | 删除 Matrix-Free guide 的重复验收章节
- 删除 [[research/technical-lines/matrix-free-research-guide]] 中独立的验收表格；真残差、1/N rank、峰值内存、完整 solve 等完成条件继续保留在对应实施阶段。
- 将统一完成边界压缩为一句话，并把事实来源章节顺延为第六节，减少连续阅读中的重复信息。
- 同步研究索引和 Matrix-Free 概念页中对 guide 的职责描述，长期执行计划中的量化里程碑与详细验收标准保持不变。

## [2026-07-26] edit | 将 PIML 方法时间线改为演进流程图
- 在 [[concepts/piml/method-lineage]] 中用 Mermaid 流程图区分 Lei 2018/2019 的前史、Huang 2022—2023 的主线，以及复杂设计域、data-free 和并行大规模实现三个后续扩展方向。
- 将原四列表压缩为文献入口索引表并删除重复的 ASCII 演进链；明确该关系来自公开论文归纳，不代表团队正式 roadmap 或严格引用继承。

## [2026-07-26] edit | 完善 PIML 子知识库结构与方法谱系
- 将原 `concepts/piml.md` 迁移并收敛为 [[concepts/piml/mathematical-foundations]]，只保留问题无关性、局部映射、EMsFEM 基础路线、监督损失及数学边界；子结构和 data-free 作为后续扩展入口。
- 在 [[concepts/piml/method-lineage]] 中增加 Lei 2018/2019 独立小节，明确 MMC/PCA 降维、问题相关性以及它作为 Huang 2022 前史与范式对照的定位。
- 完善 [[concepts/piml/_index]] 并同步根索引、概念索引和全部旧 wikilink；删除未被引用且仅含 `.gitkeep` 的 `concepts/assets/` 空目录。

## [2026-07-26] edit | 将目录索引收敛为语义主题入口
- 将根 [[index]] 与 [[concepts/_index]] 收敛为主题级导航，不再重复平铺 PIML、Matrix-Free 的数学基础、装配层次和方法谱系子页面。
- 将 [[concepts/piml/_index]] 与 [[concepts/matrix-free/_index]] 统一组织为“稳定知识—当前研究—核心文献—边界”，允许主题入口跨目录连接 `research/` 与 `literature/` 的权威页面。
- 更新 `README.md` 目录树与 `ai/llm-wiki-workflow.md`：简单概念使用单页，复杂主题使用子目录；仅在形成明确主题、多个权威页面或跨目录导航需求时建立语义 `_index.md`。
