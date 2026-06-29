---
title: "进度与决策 · 考核 Part 2 / PIML 原型（分支）"
tags:
  - progress
  - decision-log
  - defense
  - PIML
  - matrix-free
  - topology-optimization
status: "in-progress"
date: 2026-06-29
related:
  - soptx-piml-multiscale-integration-plan
  - piml_multiscale_math_principles
  - soptx-matrix-free-integration-plan
  - matrix_free_math_principles
  - one-week-defense-sprint-plan
  - piml-matrix-free-execution-plan
---

# 进度与决策 · 考核 Part 2 / PIML 原型（分支）

> 本文件是 [[status]]（AI 接续入口 hub）下「考核 Part 2 / PIML」工作线的**分支**，记录细节与决策。
> 进度推进时更新本文件，并同步 [[status]] 对应行。

## 1. 一句话现状

进站考核 8 分钟 deck 的 **Part 2（博后科研计划）帧 6 已定稿**；**帧 7「能力 B」口径已定**
（PIML 走**路线①·子结构静力缩聚**）；PIML 原型的**四件套文档体系已建并对齐路线①**；
下一步去 `soptx_heliang` 实现 **T1→T2→V1**（不需先读 Huang 2023）。

## 2. 答辩 deck（`talks/2026-postdoc-entry-assessment/template-8min.tex`）

| 帧 | 状态 |
|---|---|
| 帧 6 · 总览与承接 | **已定稿**：4×4 对称承接（左「计算基础/离散基础」↔ 右「两方面四主线」），顶对齐 `[t]`、紧凑、底部留页脚余量；Matrix-Free 迁移作右侧内部虚线 |
| 帧 7 · 方向一 PIML+Matrix-Free | **口径已定，待真图**：右侧【前期基础】现为 TikZ 占位，待 `piml_baseline.pdf` / `piml_pred_error.pdf`（PIML）与 Matrix-Free 结果后填 |
| 帧 8 · 方向二 MMC | 未动；**编译有 `\ifthenelse` 报错**（缺 `\usepackage{ifthen}`）待修 |
| 帧 9 · 工作计划/目标/平台 | 未动 |

- **能力 A（Matrix-Free）口径**（已升级，2026-06-29 据 soptx 实况）：soptx 已实现**真·无矩阵 contraction**（2D/3D standard，测试禁用装配 fallback 仍通过 = 不形成局部 `Ke`）+ matvec≡组装 K·x、CG 解≡组装直解（机器精度，4 passed）+ **NumPy benchmark 已建**（时间/内存，真实测但非 GPU/MPI 性能）。**诚实边界：无 GPU/MPI 性能优势**，GPU/多后端为下一步，mfleo 作高性能潜力参照。帧 7 能力 A 可用**真实 NumPy benchmark 数据**（不必再依赖合成 `plot_mf_scaling.py`）。实现实时态以 soptx `ai/common/progress-matrix-free.md` 为准。
- deck 排版偏好已沉淀到 `talks/.../outline-8min.md`「视觉基调 · 排版细则」。

## 3. 文档体系（拓扑优化状态方程的两条分析后端，结构对称）

| 层 | Matrix-Free | PIML 多尺度 |
|---|---|---|
| 总体计划（dut-postdoc/research） | `soptx-matrix-free-integration-plan` | `soptx-piml-multiscale-integration-plan` |
| 数学原则（dut-postdoc/research） | `matrix_free_math_principles` | `piml_multiscale_math_principles` |
| 实现备忘录（soptx_heliang/docs） | `matrix_free_architecture_notes` | `piml_multiscale_architecture_notes` |
| AI 接续上下文（soptx_heliang/docs） | `ai/common/matrix_free_context` | `ai_piml_context` |

两条后端共用 `LagrangeFEMAnalyzer` 的 `operator_backend = assembled | matrix_free | piml_multiscale`，
并在"PIML 预测局部缩聚刚度 → 全局 Matrix-Free 作用"处咬合。

## 4. 关键决策记录（本会话，2026-06-29）

1. **帧 6 承接结构**：4×4 对称；右列严格对应计划书「两方面四主线」；第 4 行收紧为「高阶多分辨率框架 → 主线四（多重网格/子结构复用）」，去掉 Matrix-Free 错配；Matrix-Free 迁移改为右列内部「主线二→主线四」虚线（两方面互通）。
2. **PIML 路线①（子结构静力缩聚）over ②（EMsFEM 角节点）**：四判据全偏①——评委是郭旭团队（懂这条线）/ 考核是研究计划而非成果 / 题目是"PIML + Matrix-Free"需子结构形式 / 一周冲刺①风险低且几乎不需补读论文。Huang 2022（②）退为奠基。
3. **B 路线（训极小预测器取真实预测误差 ~1e-3）over A（仅 mock）**：为能与团队论文做量级参照。

> 本会话其他**跨项目**决策（记忆两层模型、聊天公式用 widget 渲染）已写入全局 `~/.claude/CLAUDE.md`，速查见 [[status]] 全局约定。

## 5. PIML 原型要点（路线①，详见 `soptx-piml-multiscale-integration-plan`）

- **精确构造（ExactPredictor 真值）**：子结构静力缩聚 `N^j=[-(K_ii)^-1 K_ib; I]`，`K_s^j=(N^j)^T K^j N^j`。数学精确、无边界条件假设；正是全局 Matrix-Free 消费的逐子结构算子。
- **验证**：V1 缩聚精确（K_s^j vs 全尺度 Schur 补，rel_error<1e-10）；V4 极小预测器预测误差 ~1e-3，对照团队子结构 PIML。
- **帧 7「能力 B」三项口径**：① 求解降至子结构接口自由度 + K̂_s^j 喂 Matrix-Free 不组装全局、破内存墙（承接能力 A / Ma 2026）；② 缩聚精确 + 预测误差 ~1e-3 对照团队工作；③ 连通图 + 承接（共用 SOPTX 后端、承接博士 FEALPy/可微分基础）。
- **长期计划映射**：对应 `piml-matrix-free-execution-plan` 阶段一 **T1.3.2（复现 2023 子结构 PIML）**。

## 6. 阅读状态

- **已读**：Huang 2022（EMsFEM-PIML 奠基）、Ma 2026（并行 + Matrix-Free 子结构）、`piml-matrix-free-high-performance-solver-survey`（§3 含 Schur 缩聚推导，路线①直接依据）。
- **待读**：**Huang 2023（子结构 PIML）**——路线①的方法本身。**不阻塞起步**（T1–T2–V1 用经典缩聚即可）；在 **T4（训练预测器）前**消化，用于保真 + V4 对照锚点 + 深入理解。**PDF 不在仓库**，需提供后才能精读并补 `literature/topology-opt/Huang2023-PIML-substructure.md` 笔记。
- **理解校准**：后续工作两面交织——(a) 实现程序 T1→V4；(b) 读 Huang 2023 以保真/对照/理解，但仅 T4–V4 段需要。

## 7. 下一步待办

- [ ] `soptx_heliang` 开分支 `codex/piml-multiscale-prototype`
- [ ] T1 粗/细两级网格与局部映射
- [ ] T2 子结构静力缩聚（精确 N^j / K_s^j）
- [ ] V1 缩聚精确性测试（`rel_error < 1e-10`）—— 第一个机器精度正确性结果
- [ ] 读 Huang 2023 + 补笔记 + 回填 V4 对照数
- [ ] T4/T4b 极小预测器训练 + V4 预测精度 + 出图（`piml_baseline.pdf` / `piml_pred_error.pdf`）
- [ ] 帧 7 LaTeX 按能力 B 口径填图；修帧 8 `\ifthenelse`

## 关联文档

- [[status]] — AI 接续入口 hub（先读）
- [[soptx-piml-multiscale-integration-plan]] — PIML 原型主计划（任务/验证/答辩口径）
- [[piml_multiscale_math_principles]] — PIML 数学原理（子结构缩聚 + Matrix-Free 协同）
- [[soptx-matrix-free-integration-plan]] · [[matrix_free_math_principles]] — 姊妹 Matrix-Free 文档
- [[piml-matrix-free-execution-plan]] — 24 个月长期计划
- [[one-week-defense-sprint-plan]] — 答辩前一周冲刺
- [[postdoc-research-plan]] — 博士后科研计划（上位）
