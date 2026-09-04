# dut-postdoc

大连理工大学博士后期间的个人研究知识库。按 [Karpathy「LLM Wiki」模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 运转——由多种 AI 工具增量构建与维护的、相互链接的 Markdown wiki。Codex & Antigravity 入口见 [AGENTS.md](AGENTS.md)，Claude Code 入口见 [CLAUDE.md](CLAUDE.md)，通用工作流见 [ai/llm-wiki-workflow.md](ai/llm-wiki-workflow.md)。

全局 AI 工具配置与跨设备迁移说明由个人工具仓库 `C:\workspace\workstation`（GitHub: `brighthe/workstation`）维护；本仓库只记录 `dut-postdoc` 的项目级规则、工作流与研究状态。

## 仓库用途

在「原始资料」与「我」之间维护一个持久、结构化、可被 LLM 读写的中间层，每次提问不必从零重读论文。三层架构：

- **原始源层**：官方及个人原件保存在 iCloud，学术论文附件保存在 Zotero；AI 只读不改，不纳入版本控制
- **Wiki 层**：文献笔记、调研、工作汇报、概念页、实体页、论文草稿与历史事件档案
- **Schema 层**：`ai/` + 根目录工具入口 + `ai/templates/` 定义约定与工作流

## 目录结构

```
dut-postdoc/
├── AGENTS.md           # Codex & Antigravity 根入口
├── CLAUDE.md           # Claude Code 根入口
├── ai/                 # 多 AI 工具共享的工作流
│   ├── llm-wiki-workflow.md   # 常驻规则：边界、架构、写作约定与路由
│   ├── core-operations.md     # Ingest/Query/Lint 详细步骤（按需）
│   ├── page-schemas.md        # 页面模板绑定与状态机细则（按需）
│   ├── git-workflow.md
│   ├── paper-translation-workflow.md
│   └── talks-ppt-editing-rules.md
├── index.md            # 根总目录：全库内容地图
├── log.md              # 时间线：每次 ingest/query/lint 追加
│
├── literature/         # 文献层：原始 PDF 副本、中文译文与全文 Markdown
│   ├── topopt/         # 拓扑优化文献主题（按研究问题分四个子类）
│   │   ├── _index.md   # 主题入口、子类归属、citation key 与最近一级状态导航
│   │   ├── stress-constrained/  # 应力约束拓扑优化（PolyStress、Holmberg）
│   │   ├── mmc-mmv/    # MMC / MMV 显式拓扑优化
│   │   ├── piml/       # Problem-Independent 机器学习
│   │   ├── gpu-hpc/    # Matrix-Free / GPU 交叉应用
│   │   │   └── 每个子类内含 sources/（原始 PDF，不入 Git）与 translations/（-zh 中文译文，入 Git）
│   │   └── assets/     # 图片等派生资源（主题级共用，不下沉到子类）
│   ├── matrix-free/    # Matrix-Free 方法文献入口与跨主题索引
│   ├── fem/            # 有限元方法
│   └── others/
├── research/           # 研究计划、课题、技术线、执行工作流与项目申请
│   ├── _index.md       # research 目录入口：先读这里
│   ├── long-term-research-lines.md  # 个人长期科研主线与博士后成果路线的统一事实源
│   ├── benchmark-cases/      # 外部工程 Benchmark 的数学模型复原
│   ├── piml-matrix-free-gpu/ # 博士后核心研究项目：总计划、统一入口与跨线技术调研
│   ├── mmc-mmv/             # 课题：MMC/MMV 数值离散与高效分析调研
│   ├── technical-lines/     # 跨课题复用的 PIML、Matrix-Free、GPU/HPC 长期技术线
│   └── funding/             # 项目与基金申请台账
├── entities/           # 实体中心与科研讨论：人物档案、师门关系及历次工作汇报
│   ├── _index.md       # 实体总索引与讨论入口
│   ├── relationships.md # 人物关系：郭旭→刘畅→郭一麟 师门链
│   ├── guo-xu/         # 郭旭院士（学术画像、研究体系、历次汇报）
│   ├── liu-chang/      # 刘畅教授（学术画像、PIML选型谱系、历次汇报）
│   └── guo-yilin/      # 郭一麟博士（合作线索、GPU加速交流）
├── concepts/           # 稳定概念：简单概念单页，复杂主题使用子目录
│   ├── _index.md       # 概念域入口
│   ├── llm-wiki.md、linear-elasticity.md、machine-learning.md 等  # 简单概念单页
│   ├── mmc/
│   │   ├── _index.md   # MMC 主题入口
│   │   └── mathematical-foundations.md
│   ├── piml/
│   │   ├── _index.md   # Problem-Independent 项目释义与 Physics-Informed 外部背景边界
│   │   ├── mathematical-foundations.md
│   │   ├── method-lineage.md
│   │   └── reference-libraries/  # FEALPy SciML 等参考库架构分析
│   ├── linear-solvers/
│   │   ├── _index.md   # 线性求解器体系入口：分类树与三条判定线
│   │   ├── direct-methods.md
│   │   ├── stationary-iterations.md
│   │   ├── krylov-subspace-methods.md
│   │   ├── preconditioning.md
│   │   └── multigrid.md
│   ├── matrix-free/
│   │   ├── _index.md   # Matrix-Free 主题入口
│   │   ├── assembly-levels.md
│   │   └── method-lineage.md
│   ├── huzhang/
│   │   ├── _index.md   # Hu–Zhang 混合有限元主题入口
│   │   └── huzhang-mixed-fem.md
│   └── gpu-hpc/
│       ├── _index.md   # GPU/HPC 主题入口
│       ├── parallel-levels.md  # 进程/线程/设备内三层并行粒度与各层卡点
│       ├── heterogeneous-execution-modes.md  # GPU 异构并行实现方式的四维分类
│       ├── distributed-operator-and-shared-dofs.md  # MPI 分区、共享自由度与分布式算子第一原理
│       ├── performance-model.md  # 端到端性能模型与五级计时/扩展性/可复现记录口径
│       └── reference-libraries/  # FEALPy、MFEM 的 GPU/MPI 架构分析与对比
├── papers/             # 自己写的论文草稿
├── talks/              # 准备中或仍需维护的报告/讲稿（LaTeX）
├── archive/            # 已完成事件的最终交付物与准备材料
│   └── 2026-postdoc-entry-assessment/
└── assets/
    ├── refs.bib        # 共用参考文献库
    └── templates/      # 各类页面模板
```

`_index.md` 是语义入口，不与物理文件夹机械地一一对应。只有当一个目录形成明确主题、包含多个权威页面或需要跨目录连接稳定知识、当前研究、文献证据、科研讨论与历史档案时，才建立 `_index.md`。复杂主题入口统一按“稳定知识—主题机制节—项目与技术线入口—文献证据—关联入口—管理边界”六节组织：主题机制节的标题按主题实际内容命名，回答“这个主题机械上是什么形状、动代码前先读哪几页”；关联入口合并关联主题、工作汇报与历史档案并以角色前缀标注；管理边界必须保留独立标题，是判断禁区的依据。入口页只负责导航、页面职责和事实所有权说明，不复制其他页面正文，也不建立第二套任务状态账。

## 三个核心操作（详见 [ai/core-operations.md](ai/core-operations.md)）

- **Ingest**：核验论文与 Zotero → PDF 副本入 `sources/`、建立中文译文骨架 → 逐节对照 PDF 翻译并核验 → 在 `research/` 相应页面说明论文与研究主线的相关性 → 更新 `refs.bib`、关联页面、索引与 `log.md`
- **Query**：提问 → AI 在 wiki 内检索、带引用作答 → 有价值的问答回填成永久页面
- **Lint**：定期体检，报告矛盾/过期/孤页/缺链/空缺

## 使用说明

- 收录新论文：从 Zotero 复制原始 PDF 到 `literature/<主题>[/<子类>]/sources/<AuthorYear-short-topic>.pdf`（不入 Git）；中文译文使用同一 basename 加 `-zh`。Zotero Citation Key 保存在译文 frontmatter、主题 `_index.md` 表格和 `refs.bib` 中；单篇文献笔记层（`notes/`）已于 2026-08-30 移除，论文与研究主线的相关性在 `research/` 下相应 guide 或调研页说明
- 新建中文译文：复制 `ai/templates/translation-note.md` 到对应 `translations/` 目录，按原文章节建框架并遵循 `ai/paper-translation-workflow.md` 逐节推进和核验；`sources/` 中的 PDF 是唯一核验基准
- 文献阅读先从 `literature/_index.md` 按个人研究主线进入；单篇论文仍按主要贡献选择物理目录，交叉论文可在多条主线中出现但不复制文件
- 新建调研 / 简单概念页 / 实体页：分别复制 `research-survey.md` / `concept-note.md` / `entity-note.md`
- 新建复杂主题入口：复制 `ai/templates/topic-index.md` 到 `concepts/<主题>/_index.md`，按主题实际内容命名主题机制节；确实没有可落地机制链路时可整节删除，但不得为凑结构编造流程，「管理边界」一节必须保留
- 新建工作汇报：复制 `ai/templates/advisor-work-report.md` 到 `entities/<对象>/`，并按 `preparing → reported → follow-up-done` 更新同一页面
- 进入内容目录时先读该目录 `_index.md`；页面间一律用 Obsidian `[[wikilink]]` 互链
- 新增、移动、删除或重组页面后，收尾检查对应目录 `_index.md`；影响全库导航时同步根 `index.md`
- 报告完成后，先将长期事实抽取到概念页、技术线或调研页，再把最终交付物和准备材料整体移入 `archive/<event>/`
- 专项工作流按任务加载：Ingest/Lint 见 [core-operations.md](ai/core-operations.md)，新建/升级页面见 [page-schemas.md](ai/page-schemas.md)，PPT/讲稿见 [talks-ppt-editing-rules.md](ai/talks-ppt-editing-rules.md)，论文翻译见 [paper-translation-workflow.md](ai/paper-translation-workflow.md)，提交/推送见 [git-workflow.md](ai/git-workflow.md)
- 原始资料的存储职责以 [ai/git-workflow.md](ai/git-workflow.md#原始资料与派生文件的存储归属) 为准：iCloud 保存官方及个人原件，Zotero 保存论文附件，Git 不作为原件归档位置
- 参考文献统一维护在 `literature/refs.bib`

## 研究入口

本仓库以博士后核心研究项目为主要牵引，围绕 PIML、Matrix-Free 和 GPU/HPC 组织主线二的两年科研工作；同时维护 Hu–Zhang、VEM 等博士阶段延续成果。基金申请是条件性资助渠道，工作汇报、技术线、概念页和文献笔记分别承担执行沟通、能力建设与证据沉淀。

- [全库内容地图与当前科研架构](index.md)
- [个人长期科研主线与博士后成果路线](research/long-term-research-lines.md)
- [博士后核心研究项目两年计划](research/piml-matrix-free-gpu/project-plan.md)

---

*大连理工大学 · 博士后研究*
