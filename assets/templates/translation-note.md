---
title: "翻译：{{title}}"
aliases: []
status: "draft" # draft | read | done
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
source: "[[../notes/{{source_note}}]]"
citekey: "{{zotero_citation_key}}"
language: "zh-CN"
---

<!-- 文件名使用对应文献笔记的 {{source_note}} basename + -zh，与 Zotero Citation Key 分离。建立本页前先建立对应的 draft 文献笔记骨架；本页 status: done 后，才回填并升级正式文献笔记。 -->

# {{title}}

## 中文译文（未完成）

> 原笔记：[[../notes/{{source_note}}]]
> Zotero 条目：`zotero://select/library/items/{{zotero_item_key}}`
> PDF 附件：`zotero://open-pdf/library/items/{{zotero_attachment_key}}`
> 说明：本页译文尚未完成；缺失部分保留待补标记。

---

# 0 元数据

- **题名**：{{title}}
- **中文暂译**：{{title_zh}}
- **作者**：{{authors}}
- **期刊**：{{journal}}
- **年份**：{{year}}
- **DOI**：{{doi}}
- **Better BibTeX key**：`{{zotero_citation_key}}`
- **Zotero item key**：`{{zotero_item_key}}`
- **PDF attachment key**：`{{zotero_attachment_key}}`
- **译文状态**：译文尚未完成，缺失部分保留待补标记

# 摘要

<!-- 待补完整中文译文。 -->

# 1 {{按原文章节填写}}

<!-- 按原文目录继续建立 H1/H2/H3 层级，不使用固定的通用章节代替原文章节。 -->

<!-- 图片与图注示例：

![[{{zotero_citation_key}}_Fig1.png]]

<div align="center">

图 1：中文图注，可包含行内公式 $...$。

</div>
-->

<!-- 行间公式示例：

$$
{{latex}}
\tag{1}
$$
-->

# 译后检查清单

- [ ] 摘要、正文、附录及必要的致谢均已处理。
- [ ] 公式内容、编号与 LaTeX 环境已对照 PDF 核验。
- [ ] 图片、表格、图注及本地资产均已检查。
- [ ] 脚注、引用、链接和 Markdown 结构静态检查通过。
- [ ] 原笔记及必要关联页面已同步。

<!-- 状态与标题同步：
draft：## 中文译文（未完成）
read：## 中文译文（待逐页核验）
done：## 完整中文译文
-->
