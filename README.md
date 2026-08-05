# dut-postdoc

大连理工大学博士后期间的个人研究知识库。按 [Karpathy「LLM Wiki」模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 运转——由多种 AI 工具增量构建与维护的、相互链接的 Markdown wiki。Codex & Antigravity 入口见 [AGENTS.md](AGENTS.md)，Claude Code 入口见 [CLAUDE.md](CLAUDE.md)，通用工作流见 [ai/llm-wiki-workflow.md](ai/llm-wiki-workflow.md)。

全局 AI 工具配置与跨设备迁移说明由个人工具仓库 `C:\workspace\workstation`（GitHub: `brighthe/workstation`）维护；本仓库只记录 `dut-postdoc` 的项目级规则、工作流与研究状态。

## 仓库用途

在「原始资料」与「我」之间维护一个持久、结构化、可被 LLM 读写的中间层，每次提问不必从零重读论文。三层架构：

- **原始源层**：官方及个人原件保存在 iCloud，学术论文附件保存在 Zotero；AI 只读不改，不纳入版本控制
- **Wiki 层**：文献笔记、调研、工作汇报、概念页、实体页、论文草稿与历史事件档案
- **Schema 层**：`ai/` + 根目录工具入口 + `assets/templates/` 定义约定与工作流

## 目录结构

```
dut-postdoc/
├── AGENTS.md           # Codex & Antigravity 根入口
├── CLAUDE.md           # Claude Code 根入口
├── ai/                 # 多 AI 工具共享的工作流
│   ├── llm-wiki-workflow.md
│   ├── git-workflow.md
│   ├── paper-translation-workflow.md
│   └── talks-ppt-editing-rules.md
├── index.md            # 根总目录：全库内容地图
├── log.md              # 时间线：每次 ingest/query/lint 追加
│
├── literature/         # 文献笔记（单篇论文级 ≈ summary）
│   ├── topology-opt/   # 拓扑优化文献主题
│   │   ├── _index.md   # 主题入口与最近一级状态导航
│   │   ├── notes/      # AuthorYear-short-topic 单篇笔记；纯文件容器
│   │   ├── translations/ # 中文译文
│   │   └── assets/     # 图片等派生资源
│   ├── matrix-free/    # Matrix-Free 方法文献入口与跨主题索引
│   ├── piml/           # Physics-Informed ML、PINN 与 neural operator 文献入口
│   ├── fem/            # 有限元方法
│   └── others/
├── research/           # 研究计划、课题、技术线、执行工作流与项目申请
│   ├── _index.md       # research 目录入口：先读这里
│   ├── long-term-research-lines.md  # 个人长期科研主线：研究方向最高层事实源
│   ├── postdoc-research-output-roadmap.md  # 博士后论文组合与面上资助目标
│   ├── piml-matrix-free-gpu/ # 博士后核心研究项目：总计划、统一入口与跨线技术调研
│   ├── mmc-mmv/             # 课题：MMC/MMV 数值离散与高效分析调研
│   ├── technical-lines/     # 跨课题复用的 PIML、Matrix-Free、GPU/HPC 长期技术线
│   ├── workflows/           # 通用研究执行与训练工作流
│   └── funding/             # 项目与基金申请台账
├── work-reports/       # 周期性工作汇报：自包含的会前完整底稿、会后结论与行动项
│   ├── _index.md       # 工作汇报事实源分工、生命周期和新建流程
│   ├── guo-xu/         # 面向郭旭老师的历次工作汇报
│   └── liu-chang/      # 面向刘畅老师的历次工作汇报
├── concepts/           # 稳定概念：简单概念单页，复杂主题使用子目录
│   ├── _index.md       # 概念域入口
│   ├── llm-wiki.md     # 简单概念页
│   ├── pca-pod.md      # PCA/POD 表示、系数、重构与截断误差
│   ├── mmc/
│   │   ├── _index.md   # MMC 主题入口
│   │   └── mathematical-foundations.md
│   ├── piml/
│   │   ├── _index.md   # Problem-Independent 项目释义与 Physics-Informed 外部背景边界
│   │   ├── mathematical-foundations.md
│   │   └── method-lineage.md
│   ├── matrix-free/
│   │   ├── _index.md   # Matrix-Free 主题入口
│   │   ├── assembly-levels.md
│   │   ├── distributed-operator-and-shared-dofs.md
│   │   └── method-lineage.md
│   └── gpu-hpc/
│       ├── _index.md   # GPU/HPC 主题入口
│       ├── performance-model.md
│       └── method-lineage.md
├── entities/           # 实体页（人物/团队/机构/软件）
├── papers/             # 自己写的论文草稿
├── talks/              # 准备中或仍需维护的报告/讲稿（LaTeX）
├── archive/            # 已完成事件的最终交付物与准备材料
│   └── 2026-postdoc-entry-assessment/
└── assets/
    ├── refs.bib        # 共用参考文献库
    └── templates/      # 各类页面模板
```

`_index.md` 是语义入口，不与物理文件夹机械地一一对应。只有当一个目录形成明确主题、包含多个权威页面或需要跨目录连接稳定知识、当前研究、文献证据、工作汇报与历史档案时，才建立 `_index.md`。复杂主题入口只负责导航、页面职责和事实所有权说明，不复制其他页面正文，也不建立第二套任务状态账。

## 三个核心操作（详见 [ai/llm-wiki-workflow.md](ai/llm-wiki-workflow.md)）

- **Ingest**：核验论文与 Zotero → 建立文献笔记和中文译文骨架 → 逐节翻译并核验 → 回填正式笔记 → 更新 `refs.bib`、关联页面、索引与 `log.md`
- **Query**：提问 → AI 在 wiki 内检索、带引用作答 → 有价值的问答回填成永久页面
- **Lint**：定期体检，报告矛盾/过期/孤页/缺链/空缺

## 使用说明

- 新建文献笔记：复制 `assets/templates/literature-note.md` 到 `literature/<主题>/notes/<AuthorYear-short-topic>.md`，先只建立 `draft` 元数据骨架；中文译文使用同一 basename 加 `-zh`，达到 `done` 后再回填正文并升级状态。Zotero Citation Key 独立保存在 frontmatter 和 `refs.bib` 中
- 建立文献主题入口：复制 `assets/templates/literature-topic-index.md` 到 `literature/<主题>/_index.md`；`notes/` 不建立 `_index.md`
- 专题任务需要统一模型选型证据时，将 `assets/templates/model-selection-evidence-card.md` 片段插入单篇笔记的“证据边界与可复现性”，不建立独立证据文件
- 新建中文译文：在文献笔记骨架之后复制 `assets/templates/translation-note.md` 到对应 `translations/` 目录，按原文章节建框架并遵循 `ai/paper-translation-workflow.md` 逐节推进和核验
- 文献阅读先从 `literature/_index.md` 按个人研究主线进入；单篇笔记仍按论文主要贡献选择物理目录，交叉论文可在多条主线中出现但不复制文件
- 新建调研 / 简单概念页 / 实体页：分别复制 `research-survey.md` / `concept-note.md` / `entity-note.md`
- 新建复杂主题入口：复制 `assets/templates/topic-index.md` 到 `concepts/<主题>/_index.md`，删除没有实际内容的可选章节
- 新建工作汇报：复制 `assets/templates/advisor-work-report.md` 到 `work-reports/<对象>/`，并按 `preparing → reported → follow-up-done` 更新同一页面
- 进入内容目录时先读该目录 `_index.md`；页面间一律用 Obsidian `[[wikilink]]` 互链
- 新增、移动、删除或重组页面后，收尾检查对应目录 `_index.md`；影响全库导航时同步根 `index.md`
- 报告完成后，先将长期事实抽取到概念页、技术线或调研页，再把最终交付物和准备材料整体移入 `archive/<event>/`
- 专项工作流按任务加载：PPT/讲稿见 [talks-ppt-editing-rules.md](ai/talks-ppt-editing-rules.md)，论文翻译见 [paper-translation-workflow.md](ai/paper-translation-workflow.md)，提交/推送见 [git-workflow.md](ai/git-workflow.md)
- 原始资料的存储职责以 [ai/llm-wiki-workflow.md](ai/llm-wiki-workflow.md#原始资料存储职责) 为准：iCloud 保存官方及个人原件，Zotero 保存论文附件，Git 不作为原件归档位置
- 参考文献统一维护在 `assets/refs.bib`

## 研究入口

本仓库以博士后核心研究项目为主要牵引，围绕 PIML、Matrix-Free 和 GPU/HPC 组织主线二的两年科研工作；同时维护 Hu–Zhang、VEM 等博士阶段延续成果。基金申请是条件性资助渠道，工作汇报、技术线、概念页和文献笔记分别承担执行沟通、能力建设与证据沉淀。

- [全库内容地图与当前科研架构](index.md)
- [个人长期科研主线](research/long-term-research-lines.md)
- [博士后核心研究项目两年计划](research/piml-matrix-free-gpu/project-plan.md)

---

*大连理工大学 · 博士后研究*
