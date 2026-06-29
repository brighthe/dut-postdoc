---
title: "项目状态 · AI 接续入口（dut-postdoc）"
tags:
  - status
  - hub
  - ai-context
status: "in-progress"
date: 2026-06-29
---

# 项目状态 · AI 接续入口

> **新窗口 / 新 AI 对话先读这一份**（工具无关：Claude / Codex / Antigravity）。
> 这是**薄索引（hub）**：每条工作线一行（状态 + 下一步 + 分支文档），点进分支看细节。
> 进度推进时，更新对应**分支文档**与本表对应行。

## 工作线一览

| 工作线 | 状态 | 下一步 | 分支 / 文档 |
|---|---|---|---|
| 考核 deck · Part 1（博士工作，帧 1–5b） | 已初步讨论完 | Part 2 收尾后回看一致性 | [[outline-8min]] · `template-8min.tex` |
| 考核 deck · Part 2（博后计划，帧 6–9） | 帧 6 定稿；帧 7 口径已定待真图；帧 8(MMC) 有 `\ifthenelse` 报错；帧 9 未动 | 实现 PIML 原型出图 → 填帧 7；修帧 8 | [[progress-part2-piml]] · [[outline-8min]] |
| Matrix-Free 原型 · 能力 A（soptx） | **真·无矩阵 contraction**（2D/3D standard，不形成 `Ke`）+ matvec/CG 一致 + NumPy benchmark 已建（4 passed）；**无 GPU/MPI 性能** | GPU/多后端可行性 + benchmark | **soptx `ai/common/progress-matrix-free.md`（权威实时态）** · [[soptx-matrix-free-integration-plan]] |
| PIML 多尺度原型 · 能力 B（soptx） | 文档体系建好、路线①(子结构缩聚)已定；soptx 暂无代码 | 开分支 `codex/piml-multiscale-prototype`，T1→T2→V1 | [[progress-part2-piml]] · [[soptx-piml-multiscale-integration-plan]] |
| MMC 方向二 · 能力 C（帧 8） | 仅占位 TikZ + `\ifthenelse` 报错 | 待定 | （待建分支） |

## 全局约定（速查）

- **记忆两层模型**、**聊天数学公式用 widget 渲染 KaTeX** 等 → 见全局 `~/.claude/CLAUDE.md`；本仓库工作流见 [[llm-wiki-workflow]] 与 `ai/claude/CLAUDE.md`。
- 持久事实沉淀：跨项目 → 全局 `~/.claude/CLAUDE.md`；本仓库相关 → `ai/claude/CLAUDE.md` 与 wiki；**不用** project 级 auto-memory。

## 如何续接本项目（标准流程，新窗口/新 AI 必走）

1. **读本 hub** → 在「工作线一览」找到要继续的那一行。
2. **顺链读分支**：进入该行的分支文档；若要写代码/动手，继续读分支指向的**专题文档**（`research/*` 与 soptx 的 `ai_*_context` / 架构备忘录）。
3. **复述确认（验证闸）**：先用三五句回述"当前进度 / 已定关键决策 / 下一步与实现计划"，**等用户确认后再动手**。
4. **收尾回写**：工作结束前更新本 hub 对应行与分支文档——**保持最新是本机制有效的前提**。

> 用户侧固定提问（二选一）：
> - 续接了解：`按 status.md 续接：读 hub 与对应分支，复述当前进度与下一步，确认后继续。`
> - 续接干活：`按 status.md 续接 <工作线>，读到专题文档，复述理解 + 实现计划，确认后动手。`
