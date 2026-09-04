# 核心操作步骤（Ingest / Query / Lint）

> **触发时机**：执行 Ingest（吸收新资料）或 Lint（健康检查）前读取本文件。Query 步骤简单，常驻摘要已足够，本文件仅作完整参考。三类操作的一句话定义与路由见 [llm-wiki-workflow.md](llm-wiki-workflow.md)「三个核心操作」。

## 1. Ingest（吸收新资料）

当用户给一篇新论文/文章/图片时：

1. **核验原始资料**：读取 PDF/图片/链接，确认 Zotero item、附件和 Better BibTeX Citation Key。
2. **落位源文件并建译文骨架**：从 Zotero 复制原始 PDF 到 `literature/<主题>/sources/<basename>.pdf`（不入 Git）；用 `ai/templates/translation-note.md` 按原文章节建立 `draft` 中文译文。译文直接对照该 PDF 逐节撰写，PDF 是唯一事实来源。
3. **逐节翻译与核验**：遵循 [paper-translation-workflow.md](paper-translation-workflow.md) 与用户逐节确认；译文完成全局终审后标记为 `done`。
4. **说明相关性**：不建单篇文献笔记（`notes/` 层已于 2026-08-30 移除）；论文与研究主线的相关性、证据边界写入 `research/` 下相应 guide 或调研页，`-zh` 译文 frontmatter 的 `status` 按精读程度升级为 `read` 或 `done`。
5. **更新 `refs.bib`**：补上并核验该文献条目。
6. **横向刷新**：更新受影响的 **概念页**（`concepts/`）、**实体页**（`entities/`）、相关 **调研**（`research/`）。一次 ingest 可能要动 5-15 个文件。
7. **更新索引**：更新最近的主题 `_index.md`；只有新增、移动或删除稳定入口并影响高层导航时，才同步必要的父级 `_index.md` 和根 `index.md`。
8. **记一笔 log**。

状态流转与模板绑定细则见 [page-schemas.md](page-schemas.md)。

## 2. Query（查询）

用户提问时：

1. 在 wiki 内**搜索**相关页，通常按 `concepts/` -> `entities/` -> `research/` -> `literature/` 的顺序最高效。
2. **综合**作答，**带引用**，标注来源页 `[[...]]`。
3. 如果这条问答有长期价值，**回填**成一个永久页面，或补进已有页面，并更新 `index.md`。

## 3. Lint（健康检查）

用户说「lint / 体检 / 整理」时，扫描并报告，不擅自大改，先列清单：

- **矛盾**：不同页面对同一事实的冲突说法。
- **过期**：与新资料冲突的旧结论。
- **孤页**：没有任何页面链入的页面。
- **缺链**：本该互链却没链的页面、指向不存在页面的死链。
- **空缺**：`_index.md`/`index.md` 漏登记的页面；frontmatter 缺字段。
- 在 `log.md` 记一笔 lint 结果。
