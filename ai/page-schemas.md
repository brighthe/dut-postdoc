# 页面模板绑定与状态机细则

> **触发时机**：新建或升级文献笔记、中文译文、主题索引、汇报页，或执行事件归档前读取本文件。通用写作约定（语言、命名、frontmatter 强制、双链、链接路径）仍以 [llm-wiki-workflow.md](llm-wiki-workflow.md)「写作约定」为准，本文件只收页面类型、模板绑定与状态流转。

## 页面类型与归属目录

- **summary（文献笔记）**：一篇论文一页，落在 `literature/<主题>/notes/`；`notes/` 只是文件容器，不建立 `_index.md` 或第二套状态账。
- **synthesis（调研）**：一个课题跨多篇论文，落在 `research/`，用 `assets/templates/research-survey.md`。
- **discussion（科研讨论）**：以人为对象的汇报/交流页，落在 `discussions/<对象>/`；同一页面持续维护本次实际要汇报/交流的全部内容、必要事实快照、会后结论和行动项，讨论时无需跳转其他仓库补充正文。人物关系（师门链、合作背景）由 `discussions/relationships.md` 统一维护。
- **concept（概念页）**：反复出现的概念经跨源提炼后落在 `concepts/`；简单概念用 `assets/templates/concept-note.md` 建单页，具有多个稳定子页面的复杂主题用 `concepts/<主题>/` 子目录并以 `assets/templates/topic-index.md` 建统一语义入口。
- **entity（实体页）**：一个人/团队/机构/方法/软件的档案卡，落在 `entities/`，用 `assets/templates/entity-note.md`。
- **archive（事件档案）**：已完成、不再主动维护的事件材料，落在 `archive/<event>/`；归档前先把长期有效事实抽取到概念页、技术线或调研页（细则见下文「报告与事件归档生命周期」）。

## 文献笔记模板与状态

`assets/templates/literature-note.md` 是 `literature/<主题>/notes/` 中单篇笔记 frontmatter schema 与正文骨架的唯一规范来源；新建或迁移文献笔记时按该模板填写，不维护并行的 Zotero/ZotLit 生成模板。文献状态依次为：`draft`（只保存已核验元数据、页面框架和译文入口，不形成正文技术结论）、`read`（对应中文译文已经 `done`，笔记已精读回填，但公式、图表、证据边界或关联同步尚未全部终审）、`done`（译文与全文证据核验、frontmatter、链接和关联同步均完成）。中文译文达到 `done` 前，文献笔记不得升级为 `read`／`done`，不得作为全文级证据使用。日期统一使用 `date_added`、`date_read`、`date_update`；未知或尚不适用的可选字段写 YAML `null`。`year` 记录正式卷期年份，online-first 日期另记为 `date_online`；页码与文章号分别使用 `pages`、`article`。Citation Key 统一存入 `zotero_citation_key`，不得另建 `citekey`。

## 模型选型证据卡

`assets/templates/model-selection-evidence-card.md` 是按需插入单篇笔记的模板片段，不是独立 Wiki 页面。仅在专题任务需要统一比较时放入“证据边界与可复现性”；填好的卡片继续由该单篇笔记唯一维护，每格必须填写论文事实或“未报告”，并区分作者主张与证据边界。

## 文献主题索引

`assets/templates/literature-topic-index.md` 是 `literature/<主题>/_index.md` 的规范骨架，维护主题范围、按子主题组织的论文入口、最近一级状态、交叉主题和归类规则；不复制单篇正文。单篇状态以页面 frontmatter 为权威来源，主题索引只做最近一级同步。

## 中文译文模板与状态

`assets/templates/translation-note.md` 是译文 frontmatter 与正文骨架的唯一模板，具体翻译和核验过程遵循 [paper-translation-workflow.md](paper-translation-workflow.md)。先建立元数据文献笔记骨架和对应译文骨架，再逐节翻译；译文状态使用 `draft`（未完成）、`read`（内容已整理但尚待逐页核验）和 `done`（清单声明的内容已经核验）。只有译文 `done` 后才回填正式文献笔记。

## 复杂主题入口模板与职责

`assets/templates/topic-index.md` 是复杂主题 `_index.md` 的规范骨架。主题入口按“稳定知识—主题机制节—项目与技术线入口—文献证据—关联入口—管理边界”六节组织。其中**主题机制节**的标题按主题实际内容命名（如“Matrix-Free 算子作用与装配层次”“鞍点结构与稳定化”），用一张最小机制图加 `### 程序实现必读入口` 回答“这个主题机械上是什么形状、动代码前先读哪几页”；确实没有可落地机制链路时可整节删除，但不得为凑结构编造流程。**关联入口**合并原先的关联主题、关联实现、工作汇报与历史档案，每条以角色前缀标注，没有对应页面的角色直接不写。**管理边界必须保留独立标题**，不并入关联入口，也不压成无标题的收尾段——它是规则而非导航，是 AI 工具判断禁区的依据。跨仓库路径一律使用 `repo:path` 相对写法，不写机器绝对路径。入口页只维护导航、页面职责和事实所有权，不复制其他页面正文，不建立第二套任务状态账，不维护固定文件数或全部关键词命中清单。

## 工作汇报生命周期与边界

工作汇报页使用 `preparing → reported → follow-up-done`；未实际汇报不得标为 `reported`。页面应自包含本次实际要汇报的全部内容，包括必要的行政/工作状态摘要、技术事实、研究路线、合作线索和待请教问题；外部事实源仍各自维护完整原始记录与实时状态。真实消息、逐字交流、约见过程、关系状态、完整行政流水和敏感标识由对应沟通仓库维护，项目任务实时状态以项目仓库为准；汇报页只保留有日期和来源说明的必要快照，不建立并行事实账。

## 报告与事件归档生命周期

`talks/` 只保存准备中或仍需维护的演示文稿。事件完成后，先抽取长期知识，再把最终交付物和准备材料整体移入 `archive/<event>/`，状态统一为 `archived` 并记录事件日期和归档日期。活跃页面不得继续把归档 guide 当作当前事实源；归档内的历史脚本、话术和阶段状态不再持续更新。
