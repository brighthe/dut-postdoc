# LLM Wiki 通用工作流

本文件是 `dut-postdoc` 的工具无关常驻规则：任何 AI 工具在本仓库工作时先加载并遵守本文件，各工具入口文件只补充工具差异。方法论背景（Karpathy LLM Wiki 模式：在「原始资料」和「我」之间维护一个可被 LLM 读写的持久中间层）与仓库全貌见 [README.md](../README.md)。

## 定位与边界

- 全局 AI 工具配置由个人工具仓库 `C:\workspace\workstation`（GitHub: `brighthe/workstation`）维护；本仓库只记录 `dut-postdoc` 的项目级规则，不把工具仓库当作内容来源或运行依赖。
- 需要定位内容、判断新页面归属或不熟悉全库布局时，先读 [index.md](../index.md)（全库内容地图）；目录树与面向人类的说明见 [README.md](../README.md)。

## 三层边界

- **原始源层**（论文 PDF、官方文件、个人原件）：人拥有，AI 只读、**永不修改**，是最终事实来源；不入版本控制。
- **Wiki 层**（文献笔记、调研、工作汇报、概念页、实体页、论文草稿、事件档案）：AI 增量创建、维护与互链。
- **Schema 层**（`ai/` + 根目录工具入口 + `assets/templates/`）：人定，AI 遵守。
- 存储归属：iCloud 存官方及个人原件，Zotero 存论文附件，Git 只存 Markdown 知识、模板与确有公开价值的派生资产；细则见 [git-workflow.md](git-workflow.md)「原始资料与派生文件的存储归属」。

## 写作约定

- **语言**：全中文（专有名词、方法名、变量保留英文）。
- **文件名与 Citation Key**：文献页面用 `AuthorYear-short-topic` basename（如 `Huang2022-problemindependentmachine.md`），中文译文同 basename 加 `-zh`；Citation Key 与文件名分离，只存 `zotero_citation_key` 和 `assets/refs.bib`。
- **强制 Frontmatter**：新建或更新文档必须按对应模板将顶部 YAML 属性（`status`、`tags`、日期、作者/年份等）全部真实、完整填写，不得遗漏或留白。
- **页面模板与状态机**：新建或升级任何页面前必须读 [page-schemas.md](page-schemas.md)。
- **双链**：页面间一律用 Obsidian `[[wikilink]]`，链接给足；链尚不存在的页面也可以，标记「将来要补的页」。
- **链接路径**：一律用相对于当前文件的路径（同目录写文件名，跨目录用 `../`），不用 vault 根路径或跨目录裸文件名。移动或重命名页面时必须同步改写该页全部出链和指向它的全部入链，并复核每条链接可按相对路径解析；解析失败时不回退为按文件名匹配。例外：`assets/` 下二进制资产嵌入沿用裸文件名（`![[xx.png]]`），口径见 [paper-translation-workflow.md](paper-translation-workflow.md) §3.3。
- **可溯源、不编造**：综合性结论标注来源页 `[[...]]` 或 `refs.bib` cite key；拿不准的事实标「待确认」，绝不虚构数据、结论或文献。
- **语义 `_index.md`**：只在目录形成明确主题、包含多个权威页面或需要跨目录连接时建立，不按物理文件夹机械创建；进入内容目录先读其 `_index.md`。页面变更后同步最近的语义 `_index.md`；单页 frontmatter 是状态的权威来源，不向父级和根索引逐层复制；仅稳定入口或全库高层导航变化时才同步 `concepts/_index.md` 或根 `index.md`。
- **关联更新须先询问**：新建或修改页面后应检查关联页面（反向双链、交叉引用等）是否需同步，但执行该检索校验前必须先询问用户并获确认，严禁默默修改单页之外的内容或未经询问执行后台检查。提交前门面检查的授权以 [git-workflow.md](git-workflow.md) 为准。

## 根门面文件

- **`log.md`**：append-only 时间线。任何 ingest/query/lint/重要 edit 完成后追加一条，只增不改历史条目：

```markdown
## [YYYY-MM-DD] <ingest|query|lint|edit> | <简述>
- 动了哪些文件 / 关键结论
```

- **`index.md`**：全库稳定入口与高层导航，仅入口级变化时更新；**`README.md`**：面向人类的仓库说明，目录结构、工具入口、协作约定或研究主线变化时同步。
- **收尾检查**：完成 ingest、目录重组、规则变更或重要研究状态更新后，检查对应 `_index.md` 与三件根门面文件是否需同步；暂不更新应说明原因。提交门禁以 [git-workflow.md](git-workflow.md) 为唯一权威来源。

## 安全与隐私

- 论文等原始源 PDF 不入版本控制；最终演示交付物等派生 PDF 可按档案需要显式纳入 Git。
- 这是用户个人的研究积累；涉及未发表想法、团队内部信息时谨慎措辞，不外传、不联网检索敏感人名/单位细节。

## 按任务加载的专项工作流

以下文件只在对应任务触发时读取，不作为所有任务的全局必读项：

- **Ingest / Lint**：吸收新资料（核验原件、建双骨架、翻译、回填、横向刷新、更新索引）或健康检查（矛盾/过期/孤页/缺链/空缺，先列清单不擅自大改）前，读 [core-operations.md](core-operations.md)。
- **Query**：wiki 内检索、带引用综合作答、有长期价值时回填成页面；可直接执行，检索顺序通常 `concepts/` → `entities/` → `research/` → `literature/` 最高效。
- **新建或升级页面**：文献笔记、译文、主题索引、汇报页或事件归档前，读 [page-schemas.md](page-schemas.md)。
- **PPT / 讲稿**：修改 `talks/` 下 PPT、讲稿、逐帧 guide 或执行 PDF/截图 QA 前，读 [talks-ppt-editing-rules.md](talks-ppt-editing-rules.md)。
- **论文翻译**：翻译或完善论文译文前，读 [paper-translation-workflow.md](paper-translation-workflow.md)。
- **Git 提交与推送**：用户明确要求 commit/push 时，读 [git-workflow.md](git-workflow.md)。
