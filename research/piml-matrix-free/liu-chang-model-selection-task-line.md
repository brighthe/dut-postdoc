---
title: "刘畅老师模型选型线：任务安排与判据交付路线"
topic: "围绕模型选型痛点的任务序列、交付定义与授权边界"
aliases:
  - research/postdoc-plan/long-term/direction-1-piml-matrix-free/liu-chang-model-selection-task-line
tags:
  - model-selection
  - PIML
  - task-line
  - collaboration
status: "in-progress"
date_start: 2026-07-30
date_update: 2026-07-30
related:
  - piml-matrix-free-gpu-and-model-selection-technical-synthesis
  - piml-research-guide
  - liu-chang
---

# 刘畅老师模型选型线：任务安排与判据交付路线

> **用途**：回答「在刘畅老师这条线上，接下来按什么顺序做什么、每一步交付什么、做到什么程度才算真正回应了他的选型问题」。
>
> **事实所有权**：本页拥有交付等级 D0–D3 的定义与任务序列 T1–T7；技术论证与原型数值只引用 [[piml-matrix-free-gpu-and-model-selection-technical-synthesis]]，PIML 门禁只引用 [[../technical-lines/piml-research-guide]]，书目只引用 [[../../entities/liu-chang]]，本页不复制上述内容。

## 0. 本页边界

| 内容 | 权威页面 | 本页角色 |
|---|---|---|
| 选型框架、结合点 A–E、benchmark 设计 | [[piml-matrix-free-gpu-and-model-selection-technical-synthesis]] §5 | 只引用，不复制 |
| 刘老师公开书目、模型选型史、结合点强弱速查 | [[../../entities/liu-chang]] | 只引用，不复制 |
| PIML 技术线阶段门禁（原型恢复、结构保持、误差传播） | [[../technical-lines/piml-research-guide]] | 复用其门禁，不另立第二套 |
| 与刘老师的真实沟通过程 | 沟通仓库（`heliangos`） | 本页不记录 |

## 1. 目标：什么才算「交付一条判据」

这条线的风险是停留在框架层面——问题分解和 benchmark 设计对刘老师而言只是把他已知的困难重述得更准确。因此以**交付等级**定义进度，只有 D1 及以上才算对他的问题有实质回应：

| 等级 | 内容 | 状态（2026-07-30） |
|---|---|---|
| **D0** | 问题分解（六维函数）、候选族对照、benchmark 设计 | 已完成，见 synthesis §5.2–5.5；**属路径，不属判据** |
| **D1** | 先验判据：结构保持硬门槛（对称/SPD/刚体模态是进入 CG/GMRES 的必要条件，与 MSE 无关） | 已析出（synthesis §5.4 后），**缺本地实证** |
| **D2** | 定量关系：局部 $K_s$ 误差 → CG 迭代数 / 接口位移误差 / 柔顺度误差的实测曲线 | 未开始；是「从试错变成约束问题」的第一步 |
| **D3** | 统一 benchmark 与 Pareto 前沿（synthesis §5.5），在确认的问题边界上执行 | 依赖与刘老师确认问题边界，不得提前 |

**近期成功标准**：下一次与刘老师技术交流时，手上至少有 D1 的本地实证和 D2 的一条曲线——即「我测过了」而不是「我有个框架」。
**长期成功标准**：D3 成为双方认可的共同课题；在此之前一切表述遵守 synthesis §6 的「不能过度声称」。

## 2. 当前事实快照（2026-07-30）

- 五篇合著已入库精读，六篇公开工作待 ingest（书目与优先级见 [[../../entities/liu-chang]]）。
- PIML 原型代码已定位：`soptx` 远端分支 `origin/codex/piml-multiscale-prototype`，未合入 main，工作树内无可重放入口；接口求解为 `spsolve` 直解，**无迭代求解路径**，CG 迭代数指标当前测不出来。
- 本地已有二维平面应变线弹性 PINN 门禁通过经验（2026-07-29，`log.md`），可作 DFENN 对照基线。
- 与刘老师的沟通事实与合作边界以 synthesis §5.1 为准：只有痛点表述，无合作安排。

## 3. 任务序列

### T1 — ingest 两篇 P0（DFENN、CMAME 456）

- **前置**：用户在 Zotero 建条目并提供 Citation Key。
- **交付**：两篇精读页（`literature/` 按模板）+ `refs.bib` 条目。
- **完成判据（复核项）**：精读后必须显式回答——① DFENN/CMAME 是否已在输出侧做结构保持？若是，synthesis §5.6 结合点 A 的差异化空间需再收窄；② 硬门槛判据（D1）是否已被其上升为选型准则？③ 结合点 F（DFENN vs 本地 PINN 门禁对照）是否值得立项写入 §5.6。
- **执行**：AI 主执行，用户供源。

### T2 — 恢复 PIML 原型并过门禁

- **前置**：用户授权执行（创建 worktree、运行测试与 benchmark 属于改机器状态的操作）；确认 conda 环境（候选 `soptx-gpu`，fealpy/torch 依赖未验证；训练权重 `outputs/*.pt` 可能需重训）。
- **交付**：独立 worktree 中测试与 `benchmark_piml_forward`/`benchmark_piml_trained` 复跑记录。
- **门禁**：直接复用 [[../technical-lines/piml-research-guide]] 阶段 2，判定值以 [[piml-matrix-free-gpu-and-model-selection-technical-synthesis]] §2.1 为准，本页不复述具体数值。任一不复现即停，转入诊断，不进 T3。
- **执行**：AI 提命令，用户授权后执行。

### T3 — CG 路径与扰动扫描（产出 D1 实证 + D2 曲线）

- **前置**：T2 门禁通过。
- **内容**：在 `InterfaceCondensedSystem` 增加 CG 求解分支（保留 `spsolve` 对照）；对同一悬臂算例做两组扫描——对称相对扰动 $10^{-4}\sim10^{-1}$（测 CG 迭代数、接口位移误差、柔顺度误差）与同量级非对称扰动（预期 CG 失效）。
- **交付**：误差—迭代数—响应误差曲线（D2）；非对称组失效记录（D1 本地实证）。结果回填 synthesis §2.1/§5.4 与 [[../technical-lines/piml-research-guide]]。
- **执行**：AI 提改动与命令，用户授权后执行。

### T4 — ingest P1/P2 四篇

- NSR 2025 GCNN、EML 2024 等参元、Composite Structures 2025、Computational Mechanics 2025；完成后同步 synthesis §5.4 证据等级列与实体页。
- 可与 T2/T3 并行；不阻塞主线。

### T5 — 第二次技术交流准备

- **前置**：T1 完成（避免重复其已有结论）；T3 至少产出 D2 一条曲线（否则只能谈框架）。
- **内容**：以 synthesis §5.7 六个问题为提纲确认其具体问题边界；携带 D1 实证与 D2 曲线；如需汇报底稿，新建 `work-reports/liu-chang/` 页面（生命周期 `preparing → reported → follow-up-done`，未实际交流不得标 `reported`）。
- **执行**：AI 备材料，交流由用户本人进行。

### T6 — 统一 benchmark（D3）

- **前置**：T5 确认问题边界；对方对 benchmark 方向有明确回应。**在此之前本任务不启动**，防止在错误的问题设定上消耗算力。
- **内容与指标**：以 synthesis §5.5 为准。

### T7 — 回填与立项决定

- 根据 T1 复核结果决定结合点 F 是否写入 synthesis §5.6；根据 T5 结果更新实体页「待确认」项（痛点性质推断、通讯作者身份等）；每步照常记 `log.md`。

## 4. 依赖关系与并行度

```text
T1（ingest P0，等 Zotero）──┐
                            ├──> T5（二次交流）──> T6（benchmark, D3）
T2（原型恢复）──> T3（D1+D2）┘
T4（ingest P1/P2）——独立并行，不阻塞
T7 贯穿收尾
```

关键路径是 T2→T3：没有 D2 曲线，T5 就只能谈框架，这条线就退化为文献互读。

## 5. 授权与执行边界

| 动作 | 谁决定 |
|---|---|
| Zotero 建条目、给 Citation Key（T1/T4 前置） | 用户 |
| 创建 worktree、装依赖、跑测试/训练/benchmark（T2/T3） | 用户逐次授权，AI 不先斩后奏 |
| 文献笔记、概念页、synthesis 回填等 wiki 写作 | AI 执行，遵守关联同步询问规则 |
| 与刘老师的实际交流及其时机 | 用户 |
| T6 启动 | 用户 + 对方问题边界确认 |

## 6. 风险

- **T1 可能进一步压缩差异化空间**：若 DFENN/CMAME 精读发现其已覆盖输出侧结构保持，结合点 A 与 F 同时贬值；届时主谈点收敛到 B/D/E（求解器侧），该侧其公开工作暂未见涉及（缺失证据，非反证）。
- **T2 门禁可能不复现**：环境、权重缺失或分支腐化；已定义「不复现即停」的处置。
- **问题边界错配**：刘老师的「具体问题」若不是 $K_s$ 类局部算子（见 §5.7 问题 1），D2 曲线的场景需要重设；任务序列不变，算例更换。
- **表述越界**：任何场合不得把 D0 说成已解决选型问题；口径以 synthesis §6 为唯一标准。

## 7. 关联文档

- [[piml-matrix-free-gpu-and-model-selection-technical-synthesis]] — 技术论证、结合点与事实边界的权威底稿。
- [[../../entities/liu-chang]] — 书目、选型史与结合点速查。
- [[../technical-lines/piml-research-guide]] — PIML 阶段门禁的唯一来源。
- [[../technical-lines/matrix-free-research-guide]] — CG/预条件路线（T3 的求解器侧背景）。
- [[piml-matrix-free-high-performance-solver-survey]] — 长期开放问题。
- [[../postdoc-research-plan]] — 博士后科研计划总领。
