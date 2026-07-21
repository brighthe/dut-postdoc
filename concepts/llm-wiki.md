---
title: "LLM Wiki · 个人 AI 知识库模式"
type: concept
aliases:
  - LLM Wiki
  - Personal Knowledge Base Pattern
  - 个人 AI 知识库
tags:
  - knowledge-base
  - llm-workflow
  - methodology
status: done
date_added: 2026-06-24
date_update: 2026-06-24
---

# LLM Wiki · 个人 AI 知识库模式

> **一句话**：把 LLM 放在「原始资料」与「研究者」之间，持续维护一个结构化、可追溯、互相链接的 Markdown wiki，让每次提问都站在已沉淀的知识层上，而不是从零重读资料。

## 定义

LLM Wiki 不是一次性聊天记录，也不是简单的向量检索库，而是一个由 LLM 持续维护的中间知识层：原始 PDF、网页、图片等资料保持只读；LLM 将其压缩、重组、交叉链接为 wiki 页面；研究者通过这个 wiki 查询、追问、写作和规划。方法论来源见 Karpathy 的 *LLM Wiki: A Personal Knowledge Base Pattern*（`KarpathyLLMWiki`）。

在 `dut-postdoc` 中，这个模式被具体化为三层：

- **原始源层**：论文 PDF、文章、图片、网页等事实来源。人选择资料，Codex 只读，不改写原始材料。
- **Wiki 层**：文献笔记、调研页、概念页、实体页、论文草稿。Codex 负责增量创建、更新、互链和索引。
- **Schema 层**：`ai/`、根目录工具入口、模板、目录约定和日志格式。人制定规则，AI 工具遵守规则执行。

## 关键要点

- **人的优势**：决定读什么、为什么读、哪些问题值得问、哪些结论真的有研究价值。
- **LLM 的优势**：做持续的 bookkeeping，包括建页、补链、更新索引、维护引用、把零散问答回填成永久知识。
- **知识形态**：以 Markdown/Obsidian 双链为主；每个页面尽量短而可组合，能被后续 LLM 快速读取。
- **可追溯性**：综合判断必须能回到文献笔记、调研页或 `assets/refs.bib`，拿不准的内容标注「待确认」。
- **增量性**：每次 ingest/query/lint 都让库变得更好一点，而不是只解决当下对话。

## 在本库中的操作映射

| 操作 | 触发 | 产物 | 必做维护 |
|---|---|---|---|
| Ingest | 新论文、文章、图片、链接 | `literature/` 文献笔记，必要时刷新 `concepts/`、`entities/`、`research/` | 更新 `assets/refs.bib`、相关 `_index.md`、[[../index]]、[[../log]] |
| Query | 研究问题、写作问题、比较问题 | 带 wiki 引用的回答；有长期价值时回填页面 | 搜索顺序优先 `concepts/` → `entities/` → `research/` → `literature/` |
| Lint | “lint / 体检 / 整理” | 问题清单，不先擅自大改 | 检查矛盾、过期、孤页、缺链、索引遗漏、frontmatter 缺字段 |

## 与相关概念的关系

- **区别于 RAG**：RAG 偏向检索原文片段；LLM Wiki 偏向维护一个长期演化的、人和 LLM 都能读写的知识中间层。
- **区别于笔记软件**：普通笔记依赖人手工维护；LLM Wiki 把维护成本转给 Codex，使链接、索引、状态、引用能持续更新。
- **连接研究工作流**：[[../literature/_index]] 保存单篇论文理解，[[../research/_index]] 保存跨文献综合，[[../concepts/_index]] 保存概念沉淀，[[../entities/_index]] 保存团队/方法/软件档案。

## 在我研究中的位置

`dut-postdoc` 的目标不是收藏资料，而是支撑博士后阶段的研究判断与写作：围绕 [[piml]]、拓扑优化、有限元方法、矩阵无关求解、高性能计算等方向，把论文精读、技术路线、团队谱系、开放问题和论文草稿放进同一套可追溯结构里。具体工具可以是 Codex、Claude Code 或后续其他 AI 助手；共同遵守的知识库规则放在 `ai/llm-wiki-workflow.md`。

## 开放问题

1. 哪些问答值得回填为永久页面，哪些只需要留在对话里？
2. 调研页应该多频繁重写，而不是只追加？
3. 对未发表想法和团队内部信息，哪些内容应只保留为模糊描述？

## 相关页面

- [[../AGENTS]]
- [[../CLAUDE]]
- [[../index]]
- [[../log]]
- [[piml]]
- [[../research/postdoc-plan/postdoc-research-plan]]
