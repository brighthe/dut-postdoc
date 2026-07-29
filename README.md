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
│   ├── topology-opt/   # 拓扑优化
│   ├── fem/            # 有限元方法
│   └── others/
├── research/           # 研究计划、技术线、执行工作流与项目申请
│   ├── _index.md       # research 目录入口：先读这里
│   ├── technical-lines/     # 跨研究方向复用的 PIML、Matrix-Free、GPU/HPC 长期技术线
│   ├── workflows/           # 通用研究执行与训练工作流
│   └── postdoc-plan/
│   │   ├── postdoc-research-plan.md
│   │   └── long-term/       # 长期科研路线：两大方向调研与跨线综合
├── work-reports/       # 周期性工作汇报：自包含的会前完整底稿、会后结论与行动项
│   ├── _index.md       # 工作汇报事实源分工、生命周期和新建流程
│   └── guo-xu/         # 面向郭旭老师的历次工作汇报
├── concepts/           # 稳定概念：简单概念单页，复杂主题使用子目录
│   ├── _index.md       # 概念域入口
│   ├── llm-wiki.md     # 简单概念页
│   ├── piml/
│   │   ├── _index.md   # PIML 主题入口
│   │   ├── mathematical-foundations.md
│   │   └── method-lineage.md
│   ├── matrix-free/
│   │   ├── _index.md   # Matrix-Free 主题入口
│   │   ├── assembly-levels.md
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

`_index.md` 是语义入口，不与物理文件夹机械地一一对应。只有当一个目录形成明确主题、包含多个权威页面或需要跨目录连接稳定知识、研究路线与文献证据时，才建立 `_index.md`。

## 三个核心操作（详见 [ai/llm-wiki-workflow.md](ai/llm-wiki-workflow.md)）

- **Ingest**：给一篇新资料 → AI 读 → 过要点 → 写笔记 → 更新 `refs.bib` → 横向刷新概念/实体/调研页 → 更新索引与 `log.md`
- **Query**：提问 → AI 在 wiki 内检索、带引用作答 → 有价值的问答回填成永久页面
- **Lint**：定期体检，报告矛盾/过期/孤页/缺链/空缺

## 使用说明

- 新建文献笔记：复制 `assets/templates/literature-note.md` 放入对应子目录
- 新建调研 / 概念页 / 实体页：分别复制 `research-survey.md` / `concept-note.md` / `entity-note.md`
- 新建工作汇报：复制 `assets/templates/advisor-work-report.md` 到 `work-reports/<对象>/`，并按 `preparing → reported → follow-up-done` 更新同一页面
- 进入内容目录时先读该目录 `_index.md`；页面间一律用 Obsidian `[[wikilink]]` 互链
- 新增、移动、删除或重组页面后，收尾检查对应目录 `_index.md`；影响全库导航时同步根 `index.md`
- 报告完成后，先将长期事实抽取到概念页、技术线或调研页，再把最终交付物和准备材料整体移入 `archive/<event>/`
- 专项工作流按任务加载：PPT/讲稿见 [talks-ppt-editing-rules.md](ai/talks-ppt-editing-rules.md)，论文翻译见 [paper-translation-workflow.md](ai/paper-translation-workflow.md)，提交/推送见 [git-workflow.md](ai/git-workflow.md)
- 原始资料的存储职责以 [ai/llm-wiki-workflow.md](ai/llm-wiki-workflow.md#原始资料存储职责) 为准：iCloud 保存官方及个人原件，Zotero 保存论文附件，Git 不作为原件归档位置
- 参考文献统一维护在 `assets/refs.bib`

## 研究方向

- 长期技术线：`research/technical-lines/`（PIML、Matrix-Free、GPU/HPC）
- 博后研究计划总领：`research/postdoc-plan/postdoc-research-plan.md`
- 方向一：PIML 增强多尺度分析 + Matrix-Free 高性能求解
- 方向二：MMC/MMV 显式拓扑优化先进数值分析
- 郭旭老师工作汇报：`work-reports/guo-xu/`
- 已完成的 2026 入站考核答辩：`archive/2026-postdoc-entry-assessment/`

---

*大连理工大学 · 博士后研究*
