# AGENTS.md

本文件指导 Codex 在 `dut-postdoc` 中工作。

## 必读规则

Codex 开始任务前，应先读取并遵守：

1. [../common/llm-wiki-workflow.md](../common/llm-wiki-workflow.md)：工具无关的 LLM Wiki 方法论、目录结构、ingest/query/lint 工作流。
2. 本文件：Codex 专用补充。

## Codex 专用补充

- 本仓库是个人研究知识库，不是代码项目。默认任务是阅读、整理、写作、互链、索引和记录日志。
- 文件修改应尽量小而可追溯；不要重写用户已有积累，除非用户明确要求或为修复结构性问题所必需。
- 回答研究问题时，优先检索 wiki 内已有页面，并用 `[[wikilink]]` 标注来源。
- 新增或回填有长期价值的知识时，同步更新相关 `_index.md`、根 `index.md` 和 `log.md`。
- 只有用户明确要求时才提交 commit。
