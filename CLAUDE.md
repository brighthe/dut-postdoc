# CLAUDE.md

本文件指导 Claude Code 在 `dut-postdoc` 中工作。

全局 Claude Code / AI 工具配置由个人工具仓库 `C:\workspace\workstation`（GitHub: `brighthe/workstation`）维护；本文件只记录 `dut-postdoc` 的项目级补充规则。不要把该工具仓库视为本知识库的内容来源或运行依赖。

## 必读入口

Claude Code 开始任务前，应先读取并遵守：

1. [index.md](index.md)：全库内容地图；先从这里定位当前研究方向、内容入口和对应领域 `_index.md`。
2. [ai/llm-wiki-workflow.md](ai/llm-wiki-workflow.md)：工具无关的 LLM Wiki 方法论、目录结构、ingest/query/lint 工作流，以及按任务加载的专项规则入口。
3. 本文件：Claude Code 专用补充。

## Claude Code 专用补充

- **交流语言**：在本仓库工作时，一律使用简体中文与用户交流（正文说明、解释、问答均用中文）；代码、命令、文件名、专有名词与原文引用可保留英文。
- 本仓库是个人研究知识库，不是代码项目。核心工作是维护 Markdown/Obsidian wiki。
- 不要把 `CLAUDE.md` 当成独立 schema；通用规则与专项工作流路由以 [ai/llm-wiki-workflow.md](ai/llm-wiki-workflow.md) 为准。
