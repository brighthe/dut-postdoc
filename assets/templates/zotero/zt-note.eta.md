---
title: "<%= it.title.replace(/:/g, ' -') %>"
authors: [<% if (it.creators && it.creators.length > 0) { %><%= it.creators.map(c => '"' + (c.lastName ? c.lastName + ", " + c.firstName : c.name) + '"').join(', ') %><% } %>]
year: <%= it.date ? (String(it.date).match(/\d{4}/) ? String(it.date).match(/\d{4}/)[0] : String(it.date)) : "" %>
journal: "<%= it.publicationTitle || "" %>"
volume: <%= it.volume || "" %>
pages: "<%= it.pages || "" %>"
doi: "<%= it.DOI || "" %>"
zotero_key: "<%= it.key || "" %>"
zotero_citation_key: "<%= it.citekey || "" %>"
tags: []
status: "draft"
rating: 
date_added: <%~ it.dateAdded %>
date_read: 
---

# <%= it.title %>

> **引用**：<% if (it.creators && it.creators.length > 0) { %><%= it.creators.map(c => c.lastName ? c.lastName + ", " + c.firstName : c.name).join("; ") %><% } %>. *<%= it.publicationTitle || "" %>*, <%= it.date ? (String(it.date).match(/\d{4}/) ? String(it.date).match(/\d{4}/)[0] : String(it.date)) : "" %>. [DOI](https://doi.org/<%= it.DOI || "" %>) | [Zotero Link](<%= it.backlink %>)
> **完整中文译文**：[[translations/<%= it.citekey || "citekey" %>-zh]]
> **Zotero/Better BibTeX key**：`<%= it.citekey || "citekey" %>`
> **阅读状态**：当前为 Zotero 元数据确认 + 精读笔记框架页；论文尚未正式精读，正文技术结论需后续逐节核对后再定稿。
## 一句话概括

<!-- 用一句话说明本文最核心的贡献 -->

## 研究问题
<!-- 本文要解决什么问题？动机是什么？（如FEA计算开销、内存维度灾难、泛化能力、边界条件依赖等） -->

## 方法

### 核心思路
<!-- E.g. 多尺度有限元（EMsFEM）/ 子结构缩聚 / 离线-在线两阶段 -->

### 物理先验与网络架构
<!-- E.g. 输入输出设计、损失函数（监督刚度MSE / 物理驱动势能极小Data-free）、网络结构与数据生成方式 -->

### 算法降维与加速来源
<!-- E.g. 全局方程降维、Matrix-free 内存优化（如按需重算形函数）、查表快速路径 -->

## 实验 / 数值验证

### 算例规模与扩展性
<!-- E.g. 三维大算例、强扩展性（核数增加）、弱扩展性（规模与核数同步增加）、通信与求解器开销 -->

### 精度与效率权衡
<!-- E.g. 位移/柔顺度相对误差、单步 FEA 时间、总时间加速比 -->

| 算例 | 网格规模 | 资源 (CPU核/GPU) | 相对误差 (vs 全尺度) | 单步时间/加速比 |
|------|----------|-----------------|---------------------|----------------|
|      |          |                 |                     |                |

## 主要结论

## 优点与局限

**优点：**
- 

**局限：**
- 

## 对我研究的启发
<!-- 结合您博后计划的启发：如何与 MMC/MMV 结合、如何进行 GPU 移植、如何设计非光滑/双模量本构等 -->

## 相关文献

- [[]]
- [[]]

## 附注

### Zotero 标注与高亮
<%~ include("annots", it.annotations) %>