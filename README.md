# dut-postdoc

大连理工大学博士后期间的个人研究知识库。按 [Karpathy「LLM Wiki」模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 运转——由多种 AI 工具增量构建与维护的、相互链接的 Markdown wiki。Codex & Antigravity 入口见 [AGENTS.md](AGENTS.md)，Claude Code 入口见 [CLAUDE.md](CLAUDE.md)，通用工作流见 [ai/llm-wiki-workflow.md](ai/llm-wiki-workflow.md)。

全局 AI 工具配置与跨设备迁移说明由个人工具仓库 `C:\workspace\workstation`（GitHub: `brighthe/workstation`）维护；本仓库只记录 `dut-postdoc` 的项目级规则、工作流与研究状态。

## 仓库用途

在「原始资料」与「我」之间维护一个持久、结构化、可被 LLM 读写的中间层，每次提问不必从零重读论文。三层架构：

- **原始源层**：论文 PDF / 文章 / 图片，AI 只读不改，本地存放不入版本控制
- **Wiki 层**：文献笔记、调研、概念页、实体页、论文草稿
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
├── research/           # 博后研究计划、长期调研与入站答辩短期验证
│   ├── _index.md       # research 目录入口：先读这里
│   ├── postdoc-plan/
│   │   ├── postdoc-research-plan.md
│   │   ├── long-term/       # 长期科研路线：两大方向调研与执行计划
│   │   └── defense-sprint/  # 入站答辩短期数学原则、原型计划与出图
│   └── teams/          # 合作团队与平台背景
├── concepts/           # 概念页（跨源提炼，如 PIML）
├── entities/           # 实体页（人/团队/方法/软件）
├── papers/             # 自己写的论文草稿
├── talks/              # 报告/讲稿（LaTeX）
└── assets/
    ├── refs.bib        # 共用参考文献库
    └── templates/      # 各类页面模板
```

## 三个核心操作（详见 [ai/llm-wiki-workflow.md](ai/llm-wiki-workflow.md)）

- **Ingest**：给一篇新资料 → AI 读 → 过要点 → 写笔记 → 更新 `refs.bib` → 横向刷新概念/实体/调研页 → 更新索引与 `log.md`
- **Query**：提问 → AI 在 wiki 内检索、带引用作答 → 有价值的问答回填成永久页面
- **Lint**：定期体检，报告矛盾/过期/孤页/缺链/空缺

## 使用说明

- 新建文献笔记：复制 `assets/templates/literature-note.md` 放入对应子目录
- 新建调研 / 概念页 / 实体页：分别复制 `research-survey.md` / `concept-note.md` / `entity-note.md`
- 进入内容目录时先读该目录 `_index.md`；页面间一律用 Obsidian `[[wikilink]]` 互链
- 新增、移动、删除或重组页面后，收尾检查对应目录 `_index.md`；影响全库导航时同步根 `index.md`
- 专项工作流按任务加载：PPT/讲稿见 [talks-ppt-editing-rules.md](ai/talks-ppt-editing-rules.md)，论文翻译见 [paper-translation-workflow.md](ai/paper-translation-workflow.md)，提交/推送见 [git-workflow.md](ai/git-workflow.md)
- 所有 PDF 原文本地存放，不纳入版本控制（见 `.gitignore`）
- 参考文献统一维护在 `assets/refs.bib`

## 研究方向

- 博后研究计划总领：`research/postdoc-plan/postdoc-research-plan.md`
- 方向一：PIML 增强多尺度分析 + Matrix-Free 高性能求解
- 方向二：MMC/MMV 显式拓扑优化先进数值分析
- 入站答辩短期冲刺：`research/postdoc-plan/defense-sprint/`

---

*大连理工大学 · 博士后研究*
