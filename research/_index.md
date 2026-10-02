---
title: "研究路线与调研总览"
type: index
tags:
  - research
status: in-progress
date_added: 2026-06-04
date_update: 2026-09-08
---

# 研究路线与调研总览

> 本目录收录个人科研主线、博士后核心项目、专题课题、工程 Benchmark 算例与基金申请台账。子目录不单建 `_index.md`，统一由本页进行总览导航；页面状态以各页 frontmatter 为准，本页不另记。人物与团队档案归 `entities/`，稳定概念归 `concepts/`，单篇文献归 `literature/`，已完成事件归 `archive/`，代码与运行规范由对应代码仓库（如 `soptx`）维护。

## 个人科研主线

| 页面 / 规划 | 说明 |
|---|---|
| [[long-term-research-lines]] | 个人长期科研方向与博士后成果路线的最高层事实源：两条主线、博士延续成果与核心项目论文组合 |

## Hu–Zhang 拓扑优化 `huzhang-topopt/`

| 研究记录 | 说明 |
|---|---|
| [[huzhang-topopt/stress-constraint-acceptance]] | 应力约束停止与验收准则的来源、比较和数值验证边界 |

## 博士后核心研究项目 `piml-matrix-free-gpu/`

| 核心项目 | 说明 |
|---|---|
| [[piml-matrix-free-gpu/project-plan\|面向大规模拓扑优化的 PIML Matrix-Free 求解与 GPU 协同加速方法研究]] | 项目统一入口：总体目标、阶段路线、依赖关系与三条推进线指南的唯一事实源 |

## 专题课题 `mmc-mmv/`

| 课题调研 | 说明 |
|---|---|
| [[mmc-mmv/mmc-mmv-numerical-discretization-survey]] | MMC/MMV 高精度数值离散与高效结构分析技术调研；合作与应用课题 |

## 工程 Benchmark 算例 `benchmark-cases/`

| 算例模型 | 说明 |
|---|---|
| [[benchmark-cases/10w-3d-linear-elasticity-model]] | 10w-3d 三维线弹性 BDF 数学模型复原 |
| [[benchmark-cases/50w-2d-linear-elasticity-model]] | 50w-2d 板壳线弹性 BDF 数学模型复原（Reissner–Mindlin + MITC4 + 统一消元） |
| [[benchmark-cases/50w-2d计算]] | 50w-2d 早期数学流程原稿快照（待进一步整理或归档） |
| [[benchmark-cases/sources]] | 算例原始模型文件的归档索引（iCloud 位置、SHA-256） |

## 项目与基金申请 `funding/`

| 申请台账 | 说明 |
|---|---|
| [[funding/postdoc-funding-applications]] | 国家—辽宁省—大连市三级基金申请总台账（统一入口） |
| [[funding/china-postdoctoral-science-foundation-2026-guide-notes]] | 2026 年中国博士后科学基金政策与申请要点速查 |
| [[funding/publications-ledger]] | 代表性成果台账：论文、项目、软著与奖励 |
| [[funding/grant-writing-review-notes]] | 本子写作意见汇编：同行与评审反馈纪要 |
| [[funding/sources]] | 基金官方文件的原始链接、iCloud 归档位置和 SHA-256 |

### 申报批次推进

| 批次 | 页面 | 状态 |
|---|---|---|
| 中国博士后科学基金第 80 批面上资助 | [[funding/active/china-postdoc-foundation-general-grant/80th-2026\|申报主页]]、[[funding/active/china-postdoc-foundation-general-grant/80th-2026-application-draft\|正文草稿]] | active |
| 国资计划 | [[funding/next-cycle/china-postdoc-innovation-talent-support-plan/2026]]、[[funding/next-cycle/china-postdoc-innovation-talent-support-plan/2027]] | planned |
| 国自然青年基金 | [[funding/next-cycle/nsfc-youth-fund/2027]] | planned |
| 博士后科学基金特别资助 | [[funding/next-cycle/china-postdoc-foundation-special-grant/2027]] | planned |
| 辽宁省自然科学基金 | [[funding/next-cycle/liaoning-natural-science-fund/2026]]、[[funding/next-cycle/liaoning-natural-science-fund/2027]] | planned |
| 大连市人才支持 | [[funding/watchlist/dalian-talent-support/2026]] | watchlist |

## 维护说明

- **单一事实源（SSOT）**：本页仅记录课题与项目的高层入口与导航，各课题的技术事实由各自页面维护，实测代码数据归代码仓库（如 `soptx`）。
- **历史考核区分**：入站阶段科研计划正文见 [[../archive/2026-postdoc-entry-assessment/postdoc-research-plan]]，作为入站时点的历史事实存档，不作为当前活跃科研总领。
- **模板指引**：目录语义索引模板见 [[../schema/templates/directory-index]]；课题调研与研究计划暂不设模板，按实际内容组织。附件存放于 `research/assets/`。
