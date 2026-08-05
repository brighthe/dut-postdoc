---
title: "{{topic}} 文献入口"
type: index
aliases: []
tags:
  - literature
status: "draft" # draft | in-progress | done
date_added: null
date_update: null
---

# {{topic}} 文献入口

> 本页只管理以 {{topic}} 为主要贡献的实际文献。单篇论文事实保存在 `notes/`，中文译文保存在 `translations/`；交叉主题只链接原笔记，不复制文件或建立第二套状态账。

## 主题范围

<!-- 说明本主题纳入什么、不纳入什么，以及交叉论文的归类原则。 -->

## 已建立文献

| 文献 | 主要定位 | 交叉主题 | 状态 |
|---|---|---|---|
| [[notes/{{note_name}}]] |  |  | draft |

单篇笔记 frontmatter 是 `draft → read → done` 状态的权威来源；本表只同步最近一级状态。中文译文达到 `done` 前，笔记保持 `draft`，不得作为全文级证据。

## 交叉主题

- [[../{{other-topic}}/notes/{{note_name}}]] — 笔记保留在其主要研究问题所属主题，本页只建立交叉链接。

## 当前 ingest 队列

- [[../_index#当前 ingest 队列]] — 尚未建立单篇笔记的候选只由文献总索引维护，本页不复制队列。

## 关联研究与概念

- [[../../research/technical-lines/{{guide}}]] — 跨文献证据综合与研究边界。
- [[../../concepts/{{concept}}/_index]] — 稳定概念、方法谱系与当前研究入口。

## 归类边界

- 单篇论文只保存一份，按主要研究问题或主要贡献确定物理目录；交叉属性通过 tags、主题索引和 research guide 表达。
- `notes/` 与 `translations/` 是文件容器，不建立子级索引或第二套状态账。
- 原始 PDF 保存在 Zotero，不复制到 Git；只有摘要或元数据时，不形成全文级技术结论。
- 本页只登记已经建立实际笔记的论文；尚未建立笔记的文献仍由 [[../_index#当前 ingest 队列|文献总索引]]统一管理。
