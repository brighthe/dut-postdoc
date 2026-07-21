# Git 提交与推送工作流（本仓库）

> **触发时机**：用户要求提交（commit）或推送（push）到远程时，先读本文件再操作。本文件是操作规程，不是用户发起型任务，无需启动语——用户说“提交/推送”即触发。
>
> **机器级 git / SSH 配置已上移**：原生 git 原则、SSH over 443 鉴权、新机器一次性配置、各机现状与排错，统一见 `workstation` 仓库的 git 模块（[github.com/brighthe/workstation → git/README.md](https://github.com/brighthe/workstation/blob/main/git/README.md)；新机器可读 raw 版 `https://raw.githubusercontent.com/brighthe/workstation/main/git/README.md`）。本文件只保留 **dut-postdoc 特有**的操作要点与提交纪律。

## 操作要点（本仓库）

- 远程：`git@github.com:brighthe/dut-postdoc.git`（SSH over 443，配置见上方 workstation 指针）。
- **Claude Code 在本机操作 git 用 PowerShell**（原生 Windows git），别用 Bash 工具（cygwin）。
- **Codex PowerShell 沙箱**：执行本仓库 Git 命令时，显式使用 `git --git-dir=C:\workspace\dut-postdoc\.git --work-tree=C:\workspace\dut-postdoc <command>`，避免沙箱无法正确定位仓库（仅本机 heliang-windows-laptop 需要）。

## 提交纪律

- **仅在用户明确要求时**提交/推送。
- **根门面文件提交门禁**：每次有意义的提交都必须在 `log.md` 追加本次变更记录；提交前必须检查 `index.md` 与 `README.md`，分别在内容入口/导航/研究状态或目录结构/工具入口/协作流程/研究主线受影响时更新。无需修改时应在提交前汇报中明确“已检查，无需更新”，不得制造机械性 diff。用户明确要求 commit/push 即视为授权执行这三项检查和必要同步，无需再次询问；三项检查未完成不得提交或推送。
- 本仓库长期有多处**在建的无关改动**（`talks/`、`research/`、`concepts/`、`index.md` 等）。提交前用 `git status` 甄别，**只 `git add` 本次任务相关文件**，不要 `git add -A` 把用户其它在建工作一起提交。
- 对同时含“会话前改动 + 本次改动”的文件，先 `git diff` 确认内容再决定是否纳入。
- 提交信息用**简体中文**；如添加 AI 协作尾注，应按实际执行工具填写，不得固定或冒用其他工具身份（例如 Codex 使用 `Co-Authored-By: Codex <noreply@openai.com>`）。
- 在 `main` 上**直接提交，不开分支、不走 PR**（个人知识库，历史即如此）。
