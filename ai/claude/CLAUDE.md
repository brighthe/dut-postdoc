# CLAUDE.md

本文件指导 Claude Code 在 `dut-postdoc` 中工作。

## 必读规则

Claude Code 开始任务前，应先读取并遵守：

1. [../common/status.md](../common/status.md)：**项目状态 · AI 接续入口（hub）**——先读这一份掌握各工作线现状与下一步，再点进对应分支看细节。
2. [../common/llm-wiki-workflow.md](../common/llm-wiki-workflow.md)：工具无关的 LLM Wiki 方法论、目录结构、ingest/query/lint 工作流。
3. [../common/talks-ppt-editing-rules.md](../common/talks-ppt-editing-rules.md)：工具无关的 `talks/` 下 PPT 修改规则。
4. 本文件：Claude Code 专用补充。

## Claude Code 专用补充

- 本仓库是个人研究知识库，不是代码项目。核心工作是维护 Markdown/Obsidian wiki。
- 不要把 `CLAUDE.md` 当成独立 schema；通用规则以 `ai/common/llm-wiki-workflow.md` 为准。
- 访问任意内容目录（如 `literature/`、`research/`、`concepts/`、`entities/` 及其重要子目录）时，先阅读该目录下的 `_index.md`（若存在），用它掌握目录内容、分组与入口；再打开具体文件。
- 每次新增、移动、删除或重组某目录下的内容后，收尾时必须提醒并检查对应目录的 `_index.md` 是否需要同步更新；若影响全库导航，也要同步根 `index.md`。
- `index.md`、`log.md`、`README.md` 是仓库的三件根门面文件：分别对应全库地图、时间线与人类入口。目录结构、工具入口、协作规则或重要研究状态变化后，收尾时必须检查它们是否需要同步。
- 对论文、网页、图片等资料做 ingest 时，先和用户确认一句话概括、问题、用途，再写入 wiki。
- 涉及未发表想法和团队内部信息时，保守措辞，避免联网补全敏感细节。
