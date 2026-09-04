# AGENTS.md

本文件是 Codex 与 OpenCode 在 `dut-postdoc` 的入口桩（[AGENTS.md 约定](https://agents.md/)）。Antigravity IDE 走 `.agents/rules/`，Claude Code 走 `CLAUDE.md`，三者指向同一份规则。

## 必读入口

开始任务前先读取并遵守 [ai/llm-wiki-workflow.md](ai/llm-wiki-workflow.md)：其中含定位与边界、三层架构、写作约定、根门面文件规则，以及按任务加载的专项工作流路由（含 `papers/` 论文撰写的先提议后加载协议）。本文件不支持 `@` 导入，必须主动读取该文件，不得凭本文件推断规则。

## 工具专用补充

- **中文 Markdown 编码**：编辑中文文档时保持 UTF-8；用 PowerShell 整体读写文件必须显式 `-Encoding UTF8`，改完检查乱码与 Mojibake。
- **Codex PowerShell 沙箱**：git 命令需显式 `--git-dir` / `--work-tree`，写法见 [ai/git-workflow.md](ai/git-workflow.md)。
