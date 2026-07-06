# Git 提交与推送工作流（本仓库）

> **触发时机**：用户要求提交（commit）或推送（push）到远程时，先读本文件再操作。本文件是操作规程，不是用户发起型任务，无需启动语——用户说"提交/推送"即触发。

本文件记录 `dut-postdoc` 在**本机 + AI 沙箱环境**下提交/推送的约定与非显然的坑。常规 git 用法不赘述，只记容易重复踩的点。

## 远程与鉴权：SSH over 443

- 远程：`git@github.com:brighthe/dut-postdoc.git`（SSH）。
- **沙箱封禁 SSH 22 端口**：直接 `ssh git@github.com` 会 `Connection closed by 198.18.0.57 port 22`。必须走 GitHub 的 **SSH over 443**（`ssh.github.com:443`）。
- HTTPS 在沙箱里**无法鉴权**：无凭据助手、无缓存凭据、无 `gh` CLI、无交互 tty（`/dev/tty` 不可用），`git push` 会因 `could not read Username` 失败。所以统一用 SSH。

已完成的持久化配置（正常情况下无需再动）：

- 密钥：`C:\Users\Lenovo\.ssh\id_ed25519`（ed25519，**无口令**，便于非交互推送）。
- `~/.ssh/config`：`github.com` → `HostName ssh.github.com` / `Port 443`，`IdentityFile` 用**绝对路径**。
- 仓库本地 `core.sshCommand = ssh -F C:/Users/Lenovo/.ssh/config -i C:/Users/Lenovo/.ssh/id_ed25519`，使 `git push` 自动走上述配置。
- GitHub 侧公钥标题：`heliang-windows-laptop`（账户级密钥，按**设备**命名，非仓库名）。

## 关键坑

- **沙箱 HOME ≠ Windows 用户目录**：Git Bash/沙箱里 ssh 的 `~` 展开为 `/home/Lenovo`，不是 `C:/Users/Lenovo`。因此 `~/.ssh/config` 里的 `IdentityFile ~/.ssh/id_ed25519`、`UserKnownHostsFile` 等**一律写绝对路径**，否则报 `no such identity`。
- 若日后换成**带口令**的密钥，非交互推送会失败（无处输口令）；需要 ssh-agent 或改回无口令。

## 提交纪律

- **仅在用户明确要求时**提交/推送。
- 本仓库长期有多处**在建的无关改动**（`talks/`、`research/`、`concepts/`、`index.md` 等）。提交前用 `git status` 甄别，**只 `git add` 本次任务相关文件**，不要 `git add -A` 把用户其它在建工作一起提交。
- 对同时含"会话前改动 + 本次改动"的文件，先 `git diff` 确认内容再决定是否纳入。
- 提交信息用**简体中文**，结尾附 `Co-Authored-By: Claude <...>` 尾注。
- 在 `main` 上直接提交（个人知识库，历史即如此），不必开分支/PR。

## 排错速查

- `could not read Username for 'https://github.com'` → 远程被切回 HTTPS 或走了 HTTPS；确认 `git remote -v` 为 SSH。
- `Connection closed by ... port 22` → 走了 22 端口；确认 `~/.ssh/config` 的 443 映射与仓库 `core.sshCommand` 生效。
- `no such identity: /home/…/.ssh/id_ed25519` → config 用了 `~`；改绝对路径。
- 需要临时显式推送：
  `GIT_SSH_COMMAND="ssh -F C:/Users/Lenovo/.ssh/config -i C:/Users/Lenovo/.ssh/id_ed25519" git push origin main`
