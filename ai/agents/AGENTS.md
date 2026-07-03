# AGENTS.md

本文件指导 Codex 及 Antigravity (Gemini Code Assistant) 在 `dut-postdoc` 工作区中进行工作。

## 必读规则

在开始任务前，应先读取并遵守：

1. [../common/status.md](../common/status.md)：**项目状态 · AI 接续入口（hub）**——先读这一份掌握各工作线现状与下一步，再点进对应分支看细节。
2. [../common/llm-wiki-workflow.md](../common/llm-wiki-workflow.md)：工具无关 of LLM Wiki 方法论、目录结构、ingest/query/lint 工作流。
3. [../common/talks-ppt-editing-rules.md](../common/talks-ppt-editing-rules.md)：工具无关的 `talks/` 下 PPT 修改规则。
4. 本文件：Codex & Antigravity 专用补充。

## 专用补充

- **目录 `_index.md` 优先规则**：Codex / Antigravity 访问任意内容目录（如 `literature/`、`research/`、`concepts/`、`entities/` 及其重要子目录）时，第一件事应先阅读该目录下的 `_index.md`（若存在），用它快速掌握目录内容、分组与入口；再打开具体文件。每次新增、移动、删除或重组某目录下的内容后，收尾时必须提醒并检查对应目录的 `_index.md` 是否需要同步更新。
- **根门面文件同步规则**：`index.md`（全库地图）、`log.md`（时间线）与 `README.md`（人类入口）是 LLM Wiki 的三件根门面文件。目录结构、工具入口、协作规则或重要研究状态变化后，收尾时必须检查它们是否需要同步。
- **Git 沙箱环境路径约束**：由于 PowerShell 沙箱环境 of 限制，直接运行常规 Git 命令会报错 `fatal: not a git repository`。在此环境下执行任何 Git 命令时，必须显式附加参数：`git --git-dir=c:\workspace\dut-postdoc\.git --work-tree=c:\workspace\dut-postdoc <command>` 以确保正常定位。
- **多字节（中文）字符编辑防乱码**：避免使用内置 of `replace_file_content` 和 `multi_replace_file_content` 对包含中文 of Markdown 笔记进行局部替换，这在 Windows 环境下极易导致严重的编码匹配失败和 Mojibake（乱码）损坏。涉及中文的修改，优先使用 PowerShell 的 `Get-Content`/`Set-Content`（须指定 `-Encoding UTF8`）或 `[System.IO.File]::WriteAllText`（指定 UTF-8 无 BOM 编码）进行安全覆写，或直接使用 `write_to_file` 进行全文覆盖写入。
- **命令行工具环境约束**：系统中的 `python` 与 `node` 命令行并未处于可用状态（如 python 仅为 Windows 应用商店的安装别名，运行会抛出退出码 1 ）。在需要进行文本处理或逻辑编写时，优先使用内置的 PowerShell 语言处理。
- **Commit 与 Push 限制**：平时的任务执行中只需保持本地工作区更改，除非用户在请求中明确出现 `commit`、`push` 或 `提交/推送至远程仓库` 等指示，否则严禁自动执行提交与推送操作。
