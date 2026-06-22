# dut-postdoc

大连理工大学博士后期间的个人研究知识库。按 [Karpathy「LLM Wiki」模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 运转——由 Claude Code 增量构建与维护的、相互链接的 Markdown wiki。给 Claude 的工作约定与工作流见 [CLAUDE.md](CLAUDE.md)。

## 仓库用途

在「原始资料」与「我」之间维护一个持久、结构化、可被 LLM 读写的中间层，每次提问不必从零重读论文。三层架构：

- **原始源层**：论文 PDF / 文章 / 图片，Claude 只读不改，本地存放不入版本控制
- **Wiki 层**：文献笔记、调研、概念页、实体页、论文草稿
- **Schema 层**：`CLAUDE.md` + `assets/templates/` 定义约定与工作流

## 目录结构

```
dut-postdoc/
├── CLAUDE.md            # Schema 层：约定 + ingest/query/lint 工作流
├── index.md            # 根总目录：全库内容地图
├── log.md              # 时间线：每次 ingest/query/lint 追加
│
├── literature/         # 文献笔记（单篇论文级 ≈ summary）
│   ├── topology-opt/   # 拓扑优化
│   ├── fem/            # 有限元方法
│   └── others/
├── research/           # 调研（课题/方向级 ≈ synthesis）
├── concepts/           # 概念页（跨源提炼，如 PIML）
├── entities/           # 实体页（人/团队/方法/软件）
├── papers/             # 自己写的论文草稿
├── talks/              # 报告/讲稿（LaTeX）
└── assets/
    ├── refs.bib        # 共用参考文献库
    └── templates/      # 各类页面模板
```

## 三个核心操作（详见 [CLAUDE.md](CLAUDE.md)）

- **Ingest**：给一篇新资料 → Claude 读 → 过要点 → 写笔记 → 更新 `refs.bib` → 横向刷新概念/实体/调研页 → 更新索引与 `log.md`
- **Query**：提问 → Claude 在 wiki 内检索、带引用作答 → 有价值的问答回填成永久页面
- **Lint**：定期体检，报告矛盾/过期/孤页/缺链/空缺

## 使用说明

- 新建文献笔记：复制 `assets/templates/literature-note.md` 放入对应子目录
- 新建调研 / 概念页 / 实体页：分别复制 `research-survey.md` / `concept-note.md` / `entity-note.md`
- 页面间一律用 Obsidian `[[wikilink]]` 互链；新增页面后在对应 `_index.md` 与根 `index.md` 登记
- 所有 PDF 原文本地存放，不纳入版本控制（见 `.gitignore`）
- 参考文献统一维护在 `assets/refs.bib`

## 研究方向

- 拓扑优化（Topology Optimization）
- 有限元方法（Finite Element Method）

---

*大连理工大学 · 博士后研究*
