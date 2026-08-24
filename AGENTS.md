# AGENTS.md

本文件指导 Codex 及 Antigravity (Gemini Code Assistant) 在 `dut-postdoc` 工作区中进行工作。

## 必读入口

开始任务前，先读取并遵守 [ai/llm-wiki-workflow.md](ai/llm-wiki-workflow.md)：它包含定位与边界（全局配置归属、`index.md` 路由）、工具无关的 LLM Wiki 方法论、目录结构、ingest/query/lint 工作流，以及按任务加载的专项规则入口。

## Codex & Antigravity 专用补充

- **中文 Markdown 编码**：编辑中文文档时保持 UTF-8；使用 PowerShell 整体读写文件时必须显式指定 `-Encoding UTF8`，修改后检查乱码和 Mojibake。
