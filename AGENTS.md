# AGENTS.md

本文件指导 Codex 及 Antigravity (Gemini Code Assistant) 在 `dut-postdoc` 工作区中进行工作。

全局 Codex / AI 工具配置由个人工具仓库 `C:\workspace\workstation`（GitHub: `brighthe/workstation`）维护；本文件只记录 `dut-postdoc` 的项目级补充规则。不要把该工具仓库视为本知识库的内容来源或运行依赖。

## 必读入口

在开始任务前，应先读取并遵守：

1. [index.md](index.md)：全库内容地图；先从这里定位当前研究方向、内容入口和对应领域 `_index.md`。
2. [ai/llm-wiki-workflow.md](ai/llm-wiki-workflow.md)：工具无关的 LLM Wiki 方法论、目录结构、ingest/query/lint 工作流，以及按任务加载的专项规则入口。
3. 本文件：Codex & Antigravity 专用补充。

## Codex & Antigravity 专用补充

- **中文 Markdown 编码**：编辑中文文档时保持 UTF-8；使用 PowerShell 整体读写文件时必须显式指定 `-Encoding UTF8`，修改后检查乱码和 Mojibake。
