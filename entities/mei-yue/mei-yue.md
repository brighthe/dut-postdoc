---
title: "梅跃"
type: entity
entity_kind: person
aliases:
  - 梅跃
  - Mei Yue
  - Mei, Yue
  - Yue Mei
  - mei-yue
  - entities/mei-yue
  - entities/mei-yue/mei-yue
tags:
  - work-report
  - Mei-Yue
  - PIML
  - inverse-problem
  - CAE-software
status: in-progress
date_added: 2026-08-31
date_update: 2026-11-02
---

# 梅跃

> 大连理工大学教授、博士生导师，研究方向包括 CAE 软件研发、计算力学正反问题与非线性有限元算法。身份与公开研究方向沿用本页 2026-08-31 的主页整理记录，本次未重新核验。
>
> **与我的关系**：博士后入站学术环节的对接老师之一，曾审阅科研计划与进站考核表，见 [[wechat-log|微信沟通档案]]。2026-08-31 就基金申请书提出七条修改意见，并谈及 Matrix-Free 与 cut 单元工作，具体记录见 [[entities/mei-yue/report#2.1 第一次讨论（2026-08-31，已进行）|第一次讨论记录]]。据 [[../zang-xinyu/zang-xinyu|臧昕禹]] 页记录，2026-09-04 臧昕禹经梅老师建议来信，交流三维 CutFEM 的 Matrix-Free 求解性能问题。

## 基本信息

| 项 | 内容 |
|---|---|
| 身份 | 教授、博士生导师（据原页官方主页整理记录） |
| 所属单位 | 大连理工大学 · 力学与航空航天学院 · 工程力学系；工业装备结构分析优化与 CAE 软件全国重点实验室（沿用原页记录）；大连理工大学宁波研究院亦见 Ma 2026 作者单位脚注 |
| 职务 | 大连工业软件创新发展研究院常务副院长（据原页官方主页整理记录，本次未重新核验） |
| 学术谱系 | 待确认；现有 [[../relationships|师门链与人物关系]] 尚未登记其师承 |
| 研究方向 | CAE 软件研发、基于医学影像技术的软组织力学行为重建、结构无损检测、非线性有限元算法（顺序沿用原页主页记录） |
| 公开主页 | <http://faculty.dlut.edu.cn/meiyue/zh_CN/index.htm> |
| Google Scholar | <https://scholar.google.com/citations?user=aMNdUkUAAAAJ> |

## 已入库的 PIML 与相关合著论文

以下作者位置与本地 `literature/refs.bib` 及对应文献页一致；仅列本库已建立文献入口的合著工作，不代表其全部研究成果，也不据署名位置推断个人贡献或团队分工。

| 论文 | 作者位置 | 内容 |
|---|---|---|
| [[../../literature/topopt/piml/translations/Huang2022-problemindependentmachine-zh|Huang 2022]] | 第 6 作者，共 9 位 | 局部密度 → EMsFEM 粗单元形函数 |
| [[../../literature/topopt/piml/translations/Ma2026-highperformanceparallel-zh|Ma 2026]] | 第 6 作者，共 7 位 | PIML 与并行计算结合的大规模拓扑优化，涉及 Matrix-Free 实现与并行多重网格 |

论文内容与核验状态以对应文献页为准；本次未重新核验原始 PDF。

## 待核验的背景与讨论问题

- Texas A&M University 任教经历及约 2013–2017 的起止时间：沿用原页第三方检索线索，原页未提供可追溯出处，待权威资料确认。
- 反问题工作中的正问题规模、线性或非线性模型、求解器与计算瓶颈：现有记录不足，尚不能判断 Matrix-Free/GPU 的适用性或加速收益。
- 2026-08-31 面谈提及的 cut 单元方法与上述 CutFEM 交流之间的具体对应关系、所复用的计算量及对应论文：待确认，不直接视为同一项工作。
