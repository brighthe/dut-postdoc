---
title: null
aliases: []
authors: []
year: null
date_online: null
journal: null
volume: null
issue: null
pages: null
article: null
doi: null
zotero_key: null
zotero_citation_key: null
tags: []
status: "draft"          # draft | read | done
rating: null             # 1–5
date_added: null
date_read: null
date_update: null
---

<!-- 将本模板复制到 literature/<主题>/notes/{{note_name}}.md；note_name 使用 AuthorYear-short-topic，与 Zotero Citation Key 分离。 -->
<!-- 新论文先建立本 draft 骨架与对应译文骨架；译文 status: done 前只填写已核验元数据、链接和占位，不回填正文技术结论。 -->

# {{title}}

> **引用**：{{authors}}. *{{journal}}*, {{year}}. [DOI](https://doi.org/{{doi}}) | [Zotero Link](zotero://select/library/items/{{zotero_key}})

<!-- 建立译文骨架后，在引用块中补充；按状态使用准确标签：
> **中文译文框架（待翻译）**：[[../translations/{{note_name}}-zh]]
译文完成并核验后改为：
> **完整中文译文**：[[../translations/{{note_name}}-zh]]
-->

## 一句话概括

<!-- 用一句话概括论文解决的问题、核心方法与最重要的证据边界。 -->

## 研究问题

<!-- 本文要解决什么问题？现有方法的具体瓶颈是什么？ -->

## 方法

### 问题设置与关键假设

<!-- 说明研究对象、输入输出、适用条件以及论文实际验证的参数范围。 -->

### 方法流程与关键对象

<!-- 说明数据、变量、模型或求解器在离线/在线阶段的流向，不预设具体算法类型。 -->

### 关键数学关系

<!-- 只保留理解方法所必需的核心关系式；完整推导链接到译文或附注。 -->

## 实验 / 数值验证

<!-- 区分独立数据/直接求解次数、重采样规模、测试点和单例演示。 -->

| 算例 / 数据 | 变化参数与规模 | 方法设置 | 指标 / 对比 | 主要结果 |
|---|---|---|---|---|
|  |  |  |  |  |

## 证据边界与可复现性

<!-- 记录未验证的推广、未报告的超参数/硬件/时间，以及结论依赖的表示或评价假设。 -->

<!-- 若专题任务要求统一模型选型证据，在本节插入 assets/templates/model-selection-evidence-card.md。
填好的证据卡保留在本单篇笔记中，不建立独立事实文件；不适用时不要保留空表。 -->

## 主要结论

<!-- 只写论文证据直接支持的结论。 -->

## 批判性评价

### 优点

- {{优点}}

### 局限

- {{局限}}

## 对我研究的启发

### 可复用思路

<!-- 哪些方法或评价框架可以直接复用？ -->

### 待验证假设

<!-- 明确区分个人研究假设与论文已经证明的结论。 -->

## 相关文献与页面

- [[]]
- [[]]

## 附注

<!-- 公式推导、图表解读和来源核对记录等补充内容。 -->

### Zotero 标注与高亮

<!-- 使用 Zotero Eta 模板生成时由 annots include 自动填充。 -->
