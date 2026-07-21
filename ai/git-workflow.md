# Git 提交与推送工作流（本仓库）

> **触发时机**：用户要求提交（commit）或推送（push）到远程时，先读本文件再操作。本文件是操作规程，不是用户发起型任务，无需启动语——用户说“提交/推送”即触发。
>
> 本文件**工具无关**（各 AI 通用），且**尽量机器无关**：可移植的方法见 §1–§3，某台机器的具体值见 §4「本机现状」。

## §0 新机器启动语（复制即用）

**推荐做法：把本文件（git-workflow.md）发给新机器上的 agent，附这句话**（默认克隆本仓库，换别的仓库改路径即可）：

> 照这份 git-workflow.md（重点 §1、§3）把这台 Windows 电脑的 git 环境配好，用 PowerShell 原生 git（别用 cygwin/MSYS）。配到需要加公钥那步，把 id_ed25519.pub 打印给我、停下等我加到 GitHub。加好后把 git@github.com:brighthe/dut-postdoc.git（SSH）clone 到 C:\workspace，并 ls-remote 验证鉴权。

- 手上没有本文件、但有网时，可改让 agent 先读它的 raw 版：`https://raw.githubusercontent.com/brighthe/dut-postdoc/main/ai/git-workflow.md`。
- §1/§3 是**账户级、每台机器配一次即终身通用**；之后在这台机上再拉你名下别的仓库，只需把上面命令里的仓库名一换。
- 唯一必须你手动的一步是**把公钥加到 GitHub**（沙箱里 agent 代替不了）。

## §1 用操作系统原生 git（跨 Agent 通用原则）

git/ssh 操作要用**操作系统原生 git**——它的 ssh 会去读 `~/.ssh`（Windows 上即 `C:\Users\<你>\.ssh`）。**不要用把 `HOME` 改写到别处的 POSIX 模拟环境**（cygwin / MSYS / WSL 里指向别处的 ssh），否则读不到密钥与 config，会误报 `no such identity` / `Host key verification failed`——其实配置是好的。

- **Claude Code**：用 **PowerShell**（原生 Windows git），别用 **Bash 工具**（cygwin）。
- **Codex / Antigravity 等**：用各自能调用系统原生 git 的方式，避开 MSYS/cygwin 版 git。
- **诊断鉴权**（只读、不改动任何东西）：`git -C <repo> ls-remote --heads origin`。

## §2 鉴权方式：SSH over 443

- 远程用 SSH：`git@github.com:brighthe/dut-postdoc.git`。
- **沙箱封 SSH 22 端口**、**HTTPS 在沙箱无法鉴权**（无凭据助手、无缓存凭据、无 `gh`、无交互 tty）→ 统一走 GitHub 的 **SSH over 443**（`ssh.github.com:443`）。
- 靠**全局 `~/.ssh/config`** 把 `github.com` 映射到 443，每台机器配一次即整机所有仓库生效，无需逐仓库设置。

## §3 新机器一次性配置（任何机器照此即可提交）

1. 生成**无口令** ed25519 密钥（非交互推送需无口令）：
   `ssh-keygen -t ed25519 -C "<设备名>" -f ~/.ssh/id_ed25519 -N ""`
2. 把 `~/.ssh/id_ed25519.pub` 加到 **GitHub 账户**的 SSH keys（标题按**设备**命名，如 `heliang-windows-laptop`；账户级密钥对 brighthe 名下所有仓库生效）。
3. 在 `~/.ssh/config` 追加（`~` 由原生 git/ssh 正确解析，**不写绝对路径**即可移植）：
   ```
   Host github.com
       HostName ssh.github.com
       Port 443
       User git
       IdentityFile ~/.ssh/id_ed25519
       IdentitiesOnly yes
       StrictHostKeyChecking accept-new
       UserKnownHostsFile ~/.ssh/known_hosts
   ```
4. 验证：在**原生 shell**（非 cygwin）里 `ssh -T git@github.com` 应回显 `Hi brighthe!`。之后 `git clone` / `git push` 自动走 443。
5. **配置提交身份**（账户级，一次即所有仓库通用；缺这步 commit 会报 `Author identity unknown`）：
   `git config --global user.name "brighthe"`、`git config --global user.email "brighthe98@gmail.com"`。

## §4 本机现状（仅 heliang-windows-laptop，参考）

- 密钥 `C:\Users\Lenovo\.ssh\id_ed25519`（无口令）；config 已配 443；公钥标题 `heliang-windows-laptop`。
- 各仓库 `.git/config` 另设了等价的 `core.sshCommand`（绝对路径）——历史遗留、**只对本机有效**；有 §3 的全局 config 就够，新机器**不必**再设。
- 在本机 Codex PowerShell 沙箱中执行本仓库 Git 命令时，显式使用 `git --git-dir=C:\workspace\dut-postdoc\.git --work-tree=C:\workspace\dut-postdoc <command>`，避免沙箱无法正确定位仓库。
- ⚠️ 以上绝对路径与 `core.sshCommand` **仅本机**有效；换机器一律照 §3 走。

## §5 提交纪律

- **仅在用户明确要求时**提交/推送。
- **根门面文件提交门禁**：每次有意义的提交都必须在 `log.md` 追加本次变更记录；提交前必须检查 `index.md` 与 `README.md`，分别在内容入口/导航/研究状态或目录结构/工具入口/协作流程/研究主线受影响时更新。无需修改时应在提交前汇报中明确“已检查，无需更新”，不得制造机械性 diff。用户明确要求 commit/push 即视为授权执行这三项检查和必要同步，无需再次询问；三项检查未完成不得提交或推送。
- 本仓库长期有多处**在建的无关改动**（`talks/`、`research/`、`concepts/`、`index.md` 等）。提交前用 `git status` 甄别，**只 `git add` 本次任务相关文件**，不要 `git add -A` 把用户其它在建工作一起提交。
- 对同时含“会话前改动 + 本次改动”的文件，先 `git diff` 确认内容再决定是否纳入。
- 提交信息用**简体中文**；如添加 AI 协作尾注，应按实际执行工具填写，不得固定或冒用其他工具身份（例如 Codex 使用 `Co-Authored-By: Codex <noreply@openai.com>`）。
- 在 `main` 上**直接提交，不开分支、不走 PR**（个人知识库，历史即如此）。

## §6 排错速查

- `could not read Username for 'https://github.com'` → 远程是 HTTPS；`git remote set-url origin git@github.com:brighthe/dut-postdoc.git`。
- `Connection closed by ... port 22` → 没走 443；检查 `~/.ssh/config` 的 443 段（§3）。
- `no such identity` / `Host key verification failed` → 多半在 cygwin/MSYS 环境里跑的；换系统原生 git（§1）。
