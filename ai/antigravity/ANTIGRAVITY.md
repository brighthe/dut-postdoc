# ANTIGRAVITY.md

本文件指导 Antigravity (Gemini Code Assistant) 在 `dut-postdoc` 中工作。

## 必读规则

Antigravity 开始任务前，应先读取并遵守：

1. [../common/llm-wiki-workflow.md](../common/llm-wiki-workflow.md)：工具无关的 LLM Wiki 方法论、目录结构、ingest/query/lint 工作流。
2. 本文件：Antigravity 专用补充。

## Antigravity 专用补充

- **个人研究知识库定位**：本仓库不是传统的软件开发项目，而是一个结构化的 Markdown 知识库。所有操作的核心是阅读、整理、链接和维护。
- **防止 Windows 编码与合并冲突**：在 Windows (PowerShell) 环境下，使用代码编辑工具对包含非 ASCII（中文）字符的文件进行局部替换（`replace_file_content`）容易发生编码匹配失败及文本损坏。对于涉及大量中文段落的文件修改，建议优先使用 PowerShell 的 `Get-Content`/`Set-Content`（显式指定 UTF-8）进行安全替换，或使用 `write_to_file` 整页覆写。
- **双链与关联更新**：新增、移动或更新文献笔记时，必须同时使用 `[[wikilink]]` 格式将关联概念页、研究调研页、索引页（`index.md` 和各 `_index.md`）进行横向刷新。
- **关于 Commit**：只有在用户明确要求提交或推送时，才执行 git commit/push 操作，平时保持工作区干净即可。
