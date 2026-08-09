---
title: "Matrix-Free 文献入口"
type: index
aliases:
  - "Matrix-Free 文献入口"
tags:
  - literature
  - matrix-free
status: in-progress
date_added: 2026-08-04
date_update: 2026-08-04
---

# Matrix-Free 文献入口

> 本页只管理以 Matrix-Free 有限元算子及其求解方法为主要贡献的实际文献。单篇论文事实保存在 `notes/`，中文译文保存在 `translations/`；以拓扑优化为主要问题的交叉论文继续保存在 `literature/topology-opt/`，本页只建立链接，不复制笔记或 ingest 队列。

## 主题范围

纳入以省略全局矩阵、基于单元或求积点的算子作用、sum factorization、Matrix-Free 预条件与并行实现为主要贡献的论文。仅在应用中使用 Matrix-Free，或以拓扑优化、PIML、GPU 应用为主要问题的论文，按其主要贡献保存在相应主题。

## 已建立文献

| 文献 | 主要定位 | 交叉主题 | 状态 |
|---|---|---|---|
| [[notes/Kronbichler2012-parallel-cell-operator]] | 并行 cell-based 有限元算子应用；[[translations/Kronbichler2012-parallel-cell-operator-zh\|中文译文]]待完成 | finite-element, sum-factorization, MPI, shared-memory, vectorization | draft |

单篇笔记 frontmatter 是 `draft → read → done` 状态的权威来源；本表只同步最近一级状态。中文译文达到 `done` 前，笔记保持 `draft`，不得作为全文级证据。

## 拓扑优化交叉文献

- [[../topology-opt/notes/Traff2023-GPU-topology-optimisation]] — GPU 加速三维拓扑优化；当前为摘要／元数据级证据，译文待完成。
- [[../topology-opt/notes/Zhou2025-efficientaccelerationstrategies]] — 三维拓扑优化中的 Matrix-Free 与 MGPCG；当前为摘要／元数据级证据，译文待完成。
- [[../topology-opt/notes/Ma2026-highperformanceparallel]] — PIML 局部多尺度形函数按需预测与释放；全局粗尺度矩阵仍组装。

## 当前 ingest 队列

- [[../_index#当前 ingest 队列]] — 尚未建立单篇笔记的 Matrix-Free 候选只由文献总索引维护，本页不复制队列。

## 关联研究与概念

- [[../../research/technical-lines/matrix-free-research-guide]] — Matrix-Free 国内外研究现状、证据综合与执行门禁。
- [[../../research/piml-matrix-free-gpu/high-performance-solver-survey]] — PIML、Matrix-Free 与 GPU 三线交叉证据。
- [[../../concepts/matrix-free/_index]] — Matrix-Free 装配层级、稳定知识与当前研究入口。

## 归类边界

- 单篇论文只保存一份，按主要研究问题或主要贡献确定物理目录；交叉属性通过 tags、主题索引和 research guide 表达。
- `notes/` 与 `translations/` 是文件容器，不建立子级索引或第二套状态账。
- 原始 PDF 保存在 Zotero，不复制到 Git；只有摘要或元数据时，不形成全文级技术结论。
- 本页只登记已经建立实际笔记的论文；尚未建立笔记的文献仍由 [[../_index#当前 ingest 队列|文献总索引]]统一管理。
