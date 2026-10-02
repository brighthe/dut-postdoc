---
title: "翻译：{{title}}"
tags:
  - translation
status: "draft" # draft | read | done
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
source: "../sources/{{basename}}.pdf"
citekey: "{{zotero_citation_key}}"
language: "zh-CN"
---

<!-- 模板填写说明（生成译文后删除）：
版式参考 literature/topopt/piml/translations/Huang2023-PIML-substructure-zh.md；仅参考结构，不复制其文献事实、章节名称或完成状态。
文件名为 {{basename}}-zh.md，basename 使用 AuthorYear-short-topic，与 Zotero Citation Key 分离。
source 相对于生成后的译文文件定位原始 PDF；日期填写真实日期，tags 按论文主题补充。
citekey 必须核实；来源与 key 保留在 frontmatter，不在正文重复列出。需要 Zotero 跳转时，可添加已核实的链接，不生成未知 key。
状态含义见 [[../page-schemas#页面属性与状态]]，核验条件与证据使用边界见 [[../page-schemas#译文要求]]；复制后调整为目标页面的相对链接。
-->

# {{title}}

---

# 信息

- **中文标题**：{{title_zh}}
- **作者**：{{Given Family}}（{{中文名}}）$^1$；{{Given Family}}（{{中文名}}）$^{1,2,*}$；……
- **单位**：
  - $1$: {{第一单位中文名}}（{{城市}} {{邮编}}）
  - $2$: {{第二单位中文名}}（{{城市}} {{邮编}}）
- **期刊**：*{{journal}}*
- **卷 / 期 / 页码或文章号**：{{volume_issue_pages_or_article_number}}
- **DOI**：{{doi}}
- **收稿 / 修回 / 录用 / 在线发表**：{{received}} / {{revised}} / {{accepted}} / {{online}}
- **通讯作者**：{{Given Family}}（{{email}}）；……

<!-- 信息区填写说明：
字段按实际出版类型取舍，不适用项整条删除，未核实项标“待确认”；不为凑格式补写原文没有的日期或单位。
作者按原文顺序，姓名保留原文拼写；中文名仅在已核实时补注，未知不臆造，可在条目末尾集中标注“XX、YY 中文名待确认”。
角标用数字，与单位列表编号对应；通讯作者用 $^*$，与通讯作者条目的邮箱一致。单位只有一个时不编号，直接写单位全称。
期刊页码与文章号按原文形式写，如“63: 102041”或“48 (2013) 1031–1055”。
日期字段以原文 Article history 为准，缺项删除对应位置；无 Article history 时改用“在线发表 / 正式卷期”。
预印本改用“来源 / 版本 / 提交日期 / 证据等级”四项，并写明不作为已正式发表论文表述，示例见 literature/topopt/piml/translations/Guo2026-PIML-OFEM-zh.md。
-->

# 摘要

> 待翻译。

**关键词**：{{中文关键词}}（{{原文关键词}}）；……

<!-- 关键词以原文 Keywords 为准，逐条中英对照，顺序不变；原文无 Keywords 时整行删除，不从摘要提炼。 -->

# 1 {{原文一级章节标题的中文译名}}

> 待翻译。

<!-- 按原文目录继续建立 # 2、## 2.1、### 2.1.1 等层级，保留原编号；不将参考论文的章节固化为通用结构。
正文引用体例忠实原文；译者说明用脚注与原文区分。图表与公式的详细规则见 [[../page-schemas#译文要求]]（复制后调整相对链接）。
以下为排版示例，使用时放到对应正文位置；不要把示例或占位符留在完成稿中。

![[{{figure_prefix}}_Fig1.png]]

<center><b>
图 1：{{中文图注}}
</b></center>

<center><b>
表 1：{{中文表题}}
</b></center>

{{表格或表格图片}}

figure_prefix 用 basename 的 AuthorYear 部分，图件命名为 {{figure_prefix}}_Fig{{n}}.png，存放在主题级 assets/（如 literature/topopt/assets/），按裸文件名嵌入；图号与公式编号均以原文为准。

$$
{{latex}}
\tag{1}
$$
-->

<!-- 可选文末小节：逐篇核对原文，原文有哪节就把哪节从本注释复制到下面的 --- 之上，顺序随原文；原文没有的不补写，本注释在完成稿中删除。
附录位于参考文献之前，编号沿用原文（附录 A、式 (A1) 等）。

# CRediT 作者贡献说明

- **{{Given Family}}**：{{贡献角色中文译名}}。

# 利益冲突声明

{{译文}}

# 数据可用性声明

{{译文}}

# 致谢

{{译文；列全基金名称与批准号，不合并、不省略编号}}
-->

---

# 参考文献

[1] {{Author A, Author B}}, {{Title}}, {{Journal abbrev.}} {{vol}} ({{year}}) {{pages}}, https://doi.org/{{doi}}.

<!-- 参考文献填写说明：
逐条转录原文，编号与正文引用一致；条目之间空一行。
DOI 统一写成 https://doi.org/10.xxxx/yyyy；原文印作 http://dx.doi.org/ 或 doi: 时只改前缀，号码照录。
原文 DOI、卷期或页码本身有误时按原文照录，在交付说明中提示，不在页面内擅自更正。
PDF 提取产生的乱码（如 ë、æ、连字符断行）按原文字形修正；页码范围用 en dash。
-->
