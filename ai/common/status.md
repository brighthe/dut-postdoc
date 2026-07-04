---
title: "项目状态 · AI 接续入口（dut-postdoc）"
tags:
  - status
  - hub
  - ai-context
status: "in-progress"
date: 2026-07-04
---

# 项目状态 · AI 接续入口

> **新窗口 / 新 AI 对话先读这一份**（工具无关：Claude / Codex / Antigravity）。
> 本文件是本仓库唯一状态 hub：记录当前工作线状态、Part 2 deck 共识、逐帧 guide 入口和后续续接方式。

## 工作线一览

| 工作线 | 当前状态 | 下一步 | 主要入口 |
|---|---|---|---|
| 考核 deck · Part 1（博士工作，帧 1-5b） | 已可定稿；承担“计算数学基础、先进有限元、博士成果”铺垫 | 正式答辩前只按时间和口播习惯微调讲法，不再重构内容 | `talks/2026-postdoc-entry-assessment/template-8min.tex`；`talks/2026-postdoc-entry-assessment/script-8min.md` |
| 考核 deck · Part 2（博后计划，帧 6-11；帧 10 拆为 10a/10b） | PPT 主体与逐帧 guide 均可定稿；Part 2 不再汇总进 `script-8min.md`，以各帧 guide 为准 | 后续只做错别字、事实源或版式级 QA，不再重构路线 | 本文件 §2-§6；逐帧 guide 见 §3 |
| Matrix-Free 原型 · 能力 A（入站前基础验证） | 真·无矩阵 contraction、MatVec/CG 一致、NumPy/PyTorch CPU/CUDA 三档跑通；另有 GPU/MPI/预条件子基础 | 后续迁移到 PIML × Matrix-Free 全局原型；帧 8 侧已作为入站前基础验证 | `research/postdoc-plan/defense-sprint/direction-1-piml-matrix-free/frame8_matrix_free_pipeline_guide.md` |
| PIML 多尺度原型 · 能力 B（soptx） | 帧 7 PPT + guide 已定稿；真实 PIML 预测误差已回填：`L=5 1.6e-3` / `L=10 8.2e-3` | 非阻塞可选：补 `piml_baseline.pdf` 宏微映射图，或继续推进结构保持参数化/全局 Matrix-Free 咬合 | `research/postdoc-plan/defense-sprint/direction-1-piml-matrix-free/frame7_piml_pipeline_guide.md` |
| MMC 方向二 · 能力 C（帧 10a/10b） | 范围收敛为前向切割 Demo + 后续接入路线；帧 10a/10b guide 已统一入口 | 非阻塞可选：输出更清晰/矢量局部图，或将 `mmc_cut_mesh_prototype.py` 整理进 soptx 包并加最小测试 | `research/postdoc-plan/defense-sprint/direction-2-mmc-mmv/frame10_mmc_pipeline_guide.md` |

## 入站考核答辩最终口径（2026-07-03）

- **整体可定稿**：当前 16 页 PPT 的宏观叙事、Part 1/Part 2 承接关系、帧 6-11 的逐帧 guide 口径均已完成最终审查，可作为入站考核答辩定稿版本。
- **Part 2 管理方式**：Part 2 不需要汇总进 `script-8min.md`；后续讲法以帧 6/7/8/9/10/11 的 guide 为权威入口。不要把 `script-8min.md` 中 Part 2 未闭环误判为答辩内容未完成。
- **与郭旭老师期望的对应关系**：PPT 已体现拓扑优化、PIML、MMC/MMV、工业软件/工程场景，以及非线性分析扩展等方向；对应关系主要由帧 6 总览、帧 10/11 计划与平台支撑承接。
- **数学方向特色**：PPT 结构中已有“计算数学 → 先进有限元/高精度离散 → 快速算法/预条件子/高性能实现 → 计算力学问题”的优势链条；正式讲述时可在帧 6 或帧 11 主动点明，不需要再在 PPT 主帧增加文字。
- **最终检查顺序**：先做全局叙事审查，再逐帧检查 PPT 与对应 guide；Part 1 可参考 `script-8min.md`，Part 2 只看逐帧 guide。

## Part 2 Deck 当前结构

| PDF 页 | 帧 | 定位 | 主入口 |
|---|---|---|---|
| 9/16 | 帧 6 | 博士后科研计划总览与承接关系 | `research/postdoc-plan/defense-sprint/frame6_postdoc_plan_overview_guide.md` |
| 10/16 | 帧 7 | PIML 增强多尺度前向分析原型 | `research/postdoc-plan/defense-sprint/direction-1-piml-matrix-free/frame7_piml_pipeline_guide.md` |
| 11/16 | 帧 8 | Matrix-Free 无矩阵高性能求解原型 | `research/postdoc-plan/defense-sprint/direction-1-piml-matrix-free/frame8_matrix_free_pipeline_guide.md` |
| 12/16 | 帧 9 | PIML × Matrix-Free × GPU 融合路线 | `research/postdoc-plan/defense-sprint/direction-1-piml-matrix-free/frame9_piml_matrix_free_pipeline_guide.md` |
| 13/16 | 帧 10a | MMC/MMV 显式几何到数值分析接口 | `research/postdoc-plan/defense-sprint/direction-2-mmc-mmv/frame10_mmc_pipeline_guide.md` |
| 14/16 | 帧 10b | 先进离散与快速算法接入路线 | `research/postdoc-plan/defense-sprint/direction-2-mmc-mmv/frame10_mmc_pipeline_guide.md` |
| 15/16 | 帧 11 | 工作计划、预期目标与平台支撑 | `research/postdoc-plan/defense-sprint/frame11_work_plan_goals_platform_guide.md` |

## Part 2 已定共识

### 帧 6 · 总览与承接关系

- 右侧第四条已定为 **“高效分析与快速算法接入”**。
- guide 中左侧第四项按 **“分析-设计解耦与信息复用”** 解释，不再强绑定具体“高阶多分辨率框架”。
- 承接链：分析-设计解耦与信息复用 → 减少优化迭代中的重复分析成本 → 可复用局部/全局算子、快速更新和高性能求解 → 高效分析与快速算法接入。
- 主线三解决“离散得准”；主线四解决“求解得快、软件可复用”。

### 帧 7 · PIML 原型

- 帧 7 是方向一的局部层证据：PIML 从局部密度/材料分布预测子结构等效刚度或等效算子。
- 真实预测误差已回填，不能再用 Mock 误差替代。
- 数值不得凭记忆修改；后续看 `frame7_piml_pipeline_guide.md` 和 soptx 权威结果。

### 帧 8 · Matrix-Free 原型

- 帧 8 是入站前基础验证，不声称博士后方向一一体化系统已经完成。
- Matrix-Free 表达“不改变有限元离散，只把全局矩阵存储/组装替换为按需算子作用”。
- GPU/MPI/预条件结果说明已有并行和预条件子工程经验；PPT 主帧不强调具体软件包名。

### 帧 9 · 融合路线

- 帧 9 是 **帧 7 + 帧 8 合起来的方向一融合路线页**，不是新的数值结果页。
- 底部参考文献只保留 Ma 2026；Huang 2022/2023 已在帧 7 支撑 PIML 基础。
- Ma 2026 的“形函数按需预测/释放”和本路线进一步“指向全局算子作用”的区别放在 guide 中解释，不压入 PPT 脚注。

### 帧 10a · MMC/MMV 显式几何接口

- 题目和核心口径收束为 **“显式几何到数值分析接口”**。
- 当前只证明 TDF → 背景网格映射 → solid/void/cut 分类 → cut 单元边界重构 → 实体侧积分点 `(x,y,w)` 的前向接口。
- 当前数值：`40×20=800` 单元；`Solid 140 / Void 580 / Cut 80`；全域 Ersatz `3200` 点 → 实体侧 `1028` 点。
- 不声称完成刚度组装、结构求解、灵敏度或优化闭环。
- 三篇 MMC/MMV 文献只在帧 10a 底部出现一次；支撑路线依据，不是当前数值来源。

### 帧 10b · 先进离散与快速算法接入

- 右侧流程已定：

```text
实体侧积分点 (x,y,w)
→ 先进离散局部积分 / 局部算子
→ 算子接口：组装 / Matrix-Free
→ Krylov 求解 + 预条件子
→ GPU / 多后端并行加速
```

- “已有基础”已定：高阶/混合离散的快速求解与预条件子构造经验，可作为后续求解底座。
- 底部收束为 GPU/Matrix-Free 等可作为方向二后续求解底座，不写“也可服务方向一”。
- PPT 主帧不反复强调算海团队/FEALPy；来源背景放在 guide 与答辩追问中。

### 帧 11 · 工作计划、目标与平台支撑

- 中期栏保留 **“非线性分析扩展”**，因为有郭旭老师 2026-07-01 微信交流依据：PIML 在非线性问题上也很出色。
- “先进离散方法接入”不写进平台支撑；它属于方法体系/方向二中期任务。
- “方法体系”已定为：**PIML + Matrix-Free + GPU 高性能分析；MMC/MMV 显式几何 + 先进离散 + 快速算法。**
- 平台支撑只讲能力来源：郭旭院士团队提供拓扑优化、MMC/MMV、PIML、工业软件场景；算海团队提供计算数学、先进离散、快速算法和高性能实现基础。

## Part 2 版式与 QA 约定

- 帧 7/8/9/10a/10b 的蓝色小标题区域保持一致：标题与顶部段落距离略增，标题到下方横线距离收紧。
- 帧 10a/10b 底部参考文献只在 10a 出现完整三篇 MMC/MMV 文献，10b 不重复。
- 帧 9 底部参考文献只保留 Ma 2026，不附长括号解释。
- 所有 PPT 修改后必须 XeLaTeX 编译；2026-07-03 帧 10a 术语更新后，已通过工作区内 MiKTeX 用户目录重定向完成两遍 XeLaTeX 编译，PDF 16 页，Overfull 保持 13，未新增 Overfull。
- 2026-07-03 更新帧 10a 可见口径：顶部引导句和左侧流程末框均收束为“实体侧积分点 `(x,y,w)`”，避免误读为已完成高阶离散；frame10 guide 已同步说明当前只证明积分数据入口。
- 2026-07-03 仅重排 `frame10_mmc_pipeline_guide.md` 为与帧 7/8/9 一致的定稿型结构；PPT 未改，因此未重新编译。
- 2026-07-03 仅补充 `frame10_mmc_pipeline_guide.md` 8.9：明确帧 10b 右侧流程中前两步是数据入口/离散接口，后三步才是快速算法主体；PPT 未改，因此未重新编译。
- 2026-07-03 恢复帧 11 平台支撑可见口径为“算海团队（计算数学 / 高性能数值实现）”；`frame11_work_plan_goals_platform_guide.md` 已说明“计算数学”具体包含高精度离散、先进有限元、快速算法、预条件子与数值 PDE 求解等能力，技术任务仍由帧 10b 和方法体系承接。
- 2026-07-03 更新帧 11 近期栏：`PIML 前向流程` 改为 `PIML 基本流程`；guide 中说明其含义为离线训练、在线预测和嵌入粗尺度分析的基本链路，不等于完整拓扑优化闭环已完成。guide 第 7 节讲稿已精简为一个约 90 秒版本。
- 2026-07-04 仅更新 `frame6_postdoc_plan_overview_guide.md` 7.1 建议讲稿：按帧 6 图面顺序解释左侧两类博士积累、右侧两方面四主线、四根承接箭头和“求解框架复用”虚线边界；PPT 未改，因此未重新编译。
- 2026-07-04 仅更新 `frame7_piml_pipeline_guide.md` Mock 对照口径：把“不做缩聚”收紧为“在线阶段不对子结构重新缩聚”，并把“约一个量级”改为 `$5\times5` 约 13 倍、`$10\times10` 约 3.3 倍的分档表述；PPT 未改，因此未重新编译。
- 2026-07-04 术语统一：把「预条件」统一为「预条件子」（preconditioner 算子义）。帧 8/9 的 PPT（栏标题、④ 标题、结果口径、帧 9 流程框「Krylov + 预条件子」、并行层面）与 `frame8`/`frame9` guide 已改为「预条件子」，仅技术义保留「预条件」（如“预条件路线”“收敛仍依赖预条件”）；帧 10b 本就是该标准。已重新 XeLaTeX ×2，PDF 仍 16 页、Overfull 保持 13 无新增，`template-8min.pdf` 已更新。
- 2026-07-04 仅更新 `frame9_piml_matrix_free_pipeline_guide.md` 8.6 讲稿：把“全程都不显式组装全局矩阵”收紧为“目标链路的核心是尽量避免显式组装全局缩聚矩阵”，避免误听为 PIML × Matrix-Free × GPU 端到端系统已完成；PPT 未改，因此未重新编译。
- 2026-07-04 仅更新 `frame10_mmc_pipeline_guide.md` 8.11 讲稿：补充实体侧 `1028` 个积分点由 Solid 单元 `560` 个与 Cut 单元实体侧重构 `468` 个构成；PPT 未改，因此未重新编译。

重要 QA 图：

| 内容 | QA 图 |
|---|---|
| 帧 6 第四条改为“高效分析与快速算法接入” | `talks/2026-postdoc-entry-assessment/qa-render/frame6-09-mainline4-fast-algorithms.png` |
| 帧 7 标题区间距 | `talks/2026-postdoc-entry-assessment/qa-render/frame7-10-balanced-title-spacing.png` |
| 帧 8 标题区间距 | `talks/2026-postdoc-entry-assessment/qa-render/frame8-11-balanced-title-spacing.png` |
| 帧 9 标题区和 Ma 2026 脚注口径 | `talks/2026-postdoc-entry-assessment/qa-render/frame9-12-balanced-title-clean-ref.png` |
| 帧 10a 标题区间距 | `talks/2026-postdoc-entry-assessment/qa-render/frame10a-13-balanced-title-spacing.png` |
| 帧 10b 预条件子术语 | `talks/2026-postdoc-entry-assessment/qa-render/frame10b-14-preconditioner-term.png` |
| 帧 11 PIML 基本流程与平台支撑 | `talks/2026-postdoc-entry-assessment/qa-render/frame11-15-piml-basic-flow-platform-15.png` |

## 后续不要轻易推翻的共识

- 帧 9 不补独立数值结果；数值证据由帧 7 和帧 8 承担。
- 帧 10a 当前只证明几何到积分数据接口，不证明结构求解或优化闭环。
- 帧 10b 是后续接入路线，不是已完成耦合结果。
- 帧 11 中“非线性分析扩展”保留，因为有郭老师交流依据。
- “先进离散方法接入”属于方法体系/方向二中期任务，不应写进平台支撑。
- “预条件子”是全 deck 标准术语（指 preconditioner 算子）；帧 8/9 已于 2026-07-04 从「预条件」统一到「预条件子」，仅技术义（如“预条件路线”“收敛依赖预条件”）保留「预条件」。
- PPT 主帧尽量不主动强调算海/FEALPy 标签；来源背景、具体例子和文档依据放在 guide 与答辩追问中。

## 全局约定（速查）

- `talks/` 下 PPT 修改必须先方案后动手；确认后只改指定帧；详见 `ai/common/talks-ppt-editing-rules.md`。
- 若继续讨论 Part 2，先读本文件对应段落，再读具体帧 guide。
- `script-8min.md` 只作为 Part 1 连续讲稿入口；Part 2 不需要汇总到该文件，直接以逐帧 guide 为最终口径。
- 帧 7/8/10 的数值事实仍以 `C:\workspace\soptx_heliang\docs\frame7*_pipeline_results.md`、`frame8*_pipeline_results.md`、`frame10*_pipeline_results.md` 为唯一事实源。

## 如何续接本项目

1. 先读本文件。
2. 找到对应工作线或 Part 2 帧号。
3. 进入对应 guide。
4. 若要改 PPT，先复述当前理解和修改方案，等待用户确认。
5. 修改后编译 PDF，确认无新增 Overfull，并按需渲染目标页截图。
