# 研究路线与调研总览

> 本目录内每个下级目录只承担一条轴：[[long-term-research-lines]] 是个人科研方向总领；`piml-matrix-free-gpu` 维护主线二在博士后阶段的核心研究项目；[[postdoc-research-output-roadmap]] 维护博士延续成果、核心项目论文和风险组合；其他课题目录维护专题或合作问题；`technical-lines` 沉淀跨项目复用的长期技术能力；`workflows` 维护研究执行流程；`funding` 只维护资助机会和批次申请。人与团队等稳定档案统一归入 `entities/`，已完成的入站考核材料见 [[../archive/2026-postdoc-entry-assessment/README]]。

## 总领

| 文档 | 状态 | 说明 |
|---|---|---|
| [[long-term-research-lines]] | in-progress | 个人长期科研方向的最高层事实源：高精度数值离散与拓扑优化、智能高性能计算力学 |

## 博士后阶段成果路线

| 文档 | 状态 | 说明 |
|---|---|---|
| [[postdoc-research-output-roadmap]] | in-progress | 博士阶段延续成果、核心项目 WP1–WP3 论文组合与条件性资助渠道的成果映射 |

## 博士后核心研究项目

| 文档 | 状态 | 说明 |
|---|---|---|
| [[piml-matrix-free-gpu/_index]] | in-progress | “面向大规模拓扑优化的 PIML Matrix-Free 求解与 GPU 协同加速方法研究”的统一导航入口 |
| [[piml-matrix-free-gpu/project-plan]] | in-progress | 项目名称、总体目标、WP1–WP3、两年阶段、项目级状态和资助映射的唯一事实源 |

## 阶段性计划与历史材料

| 文档 | 状态 | 说明 |
|---|---|---|
| [[../archive/2026-postdoc-entry-assessment/postdoc-research-plan]] | archived | 博士后入站阶段科研计划：保留提交时的两大研究方面、四条主线、三阶段与预期目标 |

`archive/2026-postdoc-entry-assessment/postdoc-research-plan.md` 是入站阶段计划正文的**唯一 Markdown 事实源**，但不是当前个人长期科研方向的总领。2026-07-17 曾由其抽离出 `postdoc-research-plan.tex` 用于编译对外发送的 PDF，属一次性派生件，已于 2026-07-30 移出版本控制并由 `.gitignore` 排除；该排版源与产出 PDF 归 iCloud 的 `博士后-大连理工大学/` 保存。若需复现当时交付稿，一律从该历史正文重新抽离，不根据后续研究变化改写原有计划口径。

## 项目与基金申请

### 总台账与政策资料

| 文档 | 状态 | 说明 |
|---|---|---|
| [[funding/postdoc-funding-applications]] | draft | 国家—辽宁省—大连市三级申请总台账：当前唯一申报项、第 80 批行动清单与后续年度路线 |
| [[funding/china-postdoctoral-science-foundation-2026-guide-notes]] | draft | 2026 年中国博士后科学基金政策速查：资助类型、时间线、硬条件、兼容关系与经费管理 |
| [[funding/sources]] | reference | 基金官方文件的原始链接、iCloud 归档位置和 SHA-256 |

### 当前最紧迫

| 文档 | 状态 | 说明 |
|---|---|---|
| [[funding/active/china-postdoc-foundation-general-grant/80th-2026]] | draft | 中国博士后科学基金第 80 批面上资助执行页：资格确认、申报流程、准备资料、倒排计划与提交检查 |

### 下一年度待申请

| 文档 | 状态 | 说明 |
|---|---|---|
| [[funding/next-cycle/china-postdoc-innovation-talent-support-plan/2026]] | closed | 2026 年国资计划 A/B/C 档政策与个人结论：窗口已结束，拟进站阶段未申请，现不能补报 |
| [[funding/next-cycle/china-postdoc-innovation-talent-support-plan/2027]] | preparing | 2027 年国资计划申请准备：A 档主申、B/C 档备选，维护资格、聘期风险、材料与监测节点 |
| [[funding/next-cycle/nsfc-youth-fund/2027]] | preparing | 2027 年国家自然科学基金青年科学基金项目（C 类）准备：个人资格、三年执行期风险、材料与监测节点 |
| [[funding/next-cycle/china-postdoc-foundation-special-grant/2027]] | preparing | 2027 年中国博士后科学基金特别资助准备：基础资格、校内限额遴选、新增成果及材料节点 |
| [[funding/next-cycle/liaoning-natural-science-fund/2026]] | closed | 2026 年辽宁省自然科学基金政策归档：窗口已结束，何亮无法申报该年度博士科研启动项目 |
| [[funding/next-cycle/liaoning-natural-science-fund/2027]] | preparing | 2027 年辽宁省自然科学基金个人路线：沿用 2026 项目框架，博士启动为主线并维护监测节点与材料清单 |

### 观察项

| 文档 | 状态 | 说明 |
|---|---|---|
| [[funding/watchlist/dalian-talent-support/2026]] | monitoring | 大连市人才与科技支持资格结论：当前无可申报项目，仅在合同、户籍或政策变化时复核 |

## 长期研究路线

### 其他当前研究课题

课题目录按主题命名，与 `concepts/` 的主题子库对齐；原 `postdoc-plan/long-term/direction-1|2-*` 编号层级已于 2026-07-30 撤除，旧路径由各页 frontmatter `aliases` 兜底。

| 课题 | 文档 | 状态 | 说明 |
|---|---|---|---|
| MMC / MMV | [[mmc-mmv/mmc-mmv-numerical-discretization-survey]] | draft | 具体合作与应用课题：MMC/MMV 高精度数值离散与高效结构分析，不单列为第三条个人长期主线 |

### 跨课题长期技术线

| 入口 | 状态 | 说明 |
|---|---|---|
| [[technical-lines/_index\|长期技术线索引]] | in-progress | PIML、Matrix-Free、GPU/HPC 三条可跨课题复用的长期技术能力，以及各自 guide、必要的 task line 和事实所有权 |

三条技术线可被多个研究方向复用，不从属于固定的方向编号；具体 guide 与当前任务从该入口继续导航。

### 范式流程与算法实现

- [[../concepts/machine-learning|通用机器学习生命周期]] — 统一由 `concepts/machine-learning` 维护生命周期与 5 阶段骨架。
- 代码实现与运行 SOP 统一由 `soptx` 仓库维护。

## 共享资源

- `research/assets/` — research 相关附件目录，当前以 `.gitkeep` 保留
- 模板：[[../assets/templates/research-survey]]
