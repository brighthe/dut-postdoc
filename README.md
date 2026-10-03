# dut-postdoc

大连理工大学博士后期间的个人研究知识库。按 [Karpathy「LLM Wiki」模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 运转——由多种 AI 工具增量构建与维护的、相互链接的 Markdown wiki。工具无关的通用工作流见仓库根 [AGENTS.md](AGENTS.md)（Codex、OpenCode 直接加载）；[CLAUDE.md](CLAUDE.md) 与 `.agents/rules/dut-postdoc.md` 是 Claude Code、Antigravity IDE 的导入桩，各工具指向同一份规则。

全局 AI 工具配置与跨设备迁移说明由个人工具仓库 `C:\workspace\workstation`（GitHub: `brighthe/workstation`）维护；本仓库只记录 `dut-postdoc` 的项目级规则、工作流与研究状态。

## 仓库用途

在「原始资料」与「我」之间维护一个持久、结构化、可被 LLM 读写的中间层，每次提问不必从零重读论文。三层架构：

- **原始源层**：官方及个人原件、学术论文 PDF 均保存在 iCloud（论文平铺于 `文献库/`）；AI 只读不改，不纳入版本控制
- **Wiki 层**：文献笔记、调研、工作汇报、概念页、实体页、论文草稿与历史事件档案
- **Schema 层**：`schema/` + 根目录工具入口 + `schema/templates/` 定义约定与工作流

## 目录结构

```
dut-postdoc/
├── AGENTS.md           # Codex & Antigravity 根入口
├── CLAUDE.md           # Claude Code 根入口
├── schema/             # 知识库结构规范、维护流程与页面模板
│   ├── llm-wiki-methodology.md # 方法论与设计说明
│   ├── page-schemas.md        # 页面归属与必要约束
│   └── templates/            # 页面骨架与填写示例
├── index.md            # 根总目录：全库内容地图
├── log.md              # 时间线：每次 ingest/query/lint 追加
│
├── literature/         # 文献层：原始 PDF 副本、中文译文与全文 Markdown
│   ├── topopt/         # 拓扑优化文献主题（按研究问题分子类，登记入口统一在 literature/_index.md）
│   │   ├── stress-constrained/  # 应力约束拓扑优化（PolyStress、Holmberg）
│   │   ├── mmc-mmv/    # MMC / MMV 显式拓扑优化
│   │   ├── piml/       # Problem-Independent 机器学习
│   │   ├── gpu-hpc/    # GPU 实现与多重网格 / PCG 加速策略
│   │   ├── matrix-free/  # 以 matrix-free 算子作用为主要贡献的拓扑优化
│   │   ├── mixed-fem/  # 应力–位移真混合格式下的拓扑优化
│   │   ├── element-types/  # 单元类型或阶次选择本身作为研究对象
│   │   ├── frameworks/     # 拓扑优化通用框架、模块化架构与教学代码
│   │   ├── substructuring/ # 子结构、多尺度粗单元与区域分解求解拓扑优化
│   │   │   └── 每个子类内含 sources/（原始 PDF 本地副本，主档在 iCloud 文献库/，不入 Git）与 translations/（-zh 中文译文，入 Git）
│   │   └── assets/     # 图片等派生资源（主题级共用，不下沉到子类）
│   ├── matrix-free/    # Matrix-Free 方法文献入口与跨主题索引
│   ├── fem/            # 有限元方法
│   ├── fem-libraries/  # 有限元框架与库的官方描述论文（MFEM、libCEED 等，按软件归类）
│   └── inbox/          # 尚未确定分类的论文 PDF 暂存（不入 Git）
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
│   │   └── reports/   # 每次汇报独立目录，正文为 report.md，入口见 entities/_index.md
│   ├── liu-chang/      # 刘畅教授（学术画像、PIML选型谱系、历次汇报）
│   └── guo-yilin/      # 郭一麟博士（合作线索、GPU加速交流）
├── concepts/           # 稳定概念：简单概念单页，复杂主题使用子目录
│   ├── _index.md       # 概念域总入口（统一直接索引所有子目录概念页，无二级 _index.md）
│   ├── linear-elasticity.md、machine-learning.md 等  # 简单概念单页
│   ├── mmc/
│   │   └── mathematical-foundations.md
│   ├── piml/
│   │   ├── piml-paradigm.md
│   │   ├── piml-substructural.md
│   │   └── reference-libraries/  # FEALPy SciML 等参考库架构分析
│   ├── linear-solvers/
│   │   ├── linear-solvers-architecture.md  # 求解器体系架构：三条判定线、四层分工与选型流
│   │   ├── direct-methods.md
│   │   ├── stationary-iterations.md
│   │   ├── krylov-subspace-methods.md
│   │   ├── preconditioning.md
│   │   └── multigrid.md
│   ├── matrix-free/
│   │   ├── assembly-levels.md
│   │   └── method-lineage.md
│   ├── density-topopt/
│   │   ├── regularization-and-length-scale-control.md
│   │   ├── stress-constrained-topopt.md
│   │   └── substructural-density-topology-optimization.md
│   ├── huzhang/
│   │   └── huzhang-mixed-fem.md
│   └── gpu-hpc/
│       ├── parallel-levels.md  # 进程/线程/设备内三层并行粒度与各层卡点
│       ├── heterogeneous-execution-modes.md  # GPU 异构并行实现方式的四维分类
│       ├── distributed-operator-and-shared-dofs.md  # MPI 分区、共享自由度与分布式算子第一原理
│       ├── performance-model.md  # 端到端性能模型与五级计时/扩展性/可复现记录口径
│       └── reference-libraries/  # FEALPy、MFEM 的 GPU/MPI 架构分析与对比
├── papers/             # 自己写的论文草稿
├── talks/              # 准备中或仍需维护的报告/讲稿（LaTeX）
└── archive/            # 已完成事件的最终交付物与准备材料
    └── 2026-postdoc-entry-assessment/
```

导航采用“根 `index.md` + 一级内容目录 `_index.md`”架构：全库固定仅 7 个一级目录保留 `_index.md`，彻底消除所有二级 `_index.md`；一级索引直接通过主题分节与两列表格直达各子目录页面。具体约束以 [schema/page-schemas.md](schema/page-schemas.md) 为准，写法见 [目录索引模板](schema/templates/directory-index.md)；全局维护原则由 [AGENTS.md](AGENTS.md) 规定。

## 三个核心操作（见 [方法论](schema/llm-wiki-methodology.md)）

- **Ingest**：PDF 存入 iCloud `文献库/`、按 DOI 核验元数据 → PDF 副本入 `sources/`、建立中文译文骨架 → 逐节对照 PDF 翻译并核验 → 在 `research/` 相应页面说明论文与研究主线的相关性 → 更新 `refs.bib`、关联页面、索引与 `log.md`
- **Query**：提问 → AI 在 wiki 内检索、带引用作答 → 有价值的问答回填成永久页面
- **Lint**：定期体检，报告矛盾/过期/孤页/缺链/空缺

## 使用说明

- 收录新论文：原始 PDF 以 `<AuthorYear-short-topic>.pdf` 存入 iCloud `文献库/`，再复制到 `literature/<主题>[/<子类>]/sources/`（不入 Git）；中文译文使用同一 basename 加 `-zh`。新文献 Citation Key 取 basename，保存在译文 frontmatter、文献总索引 `literature/_index.md` 表格和 `refs.bib` 中，出版信息按 DOI 经 CrossRef 核验；单篇文献笔记层（`notes/`）已于 2026-08-30 移除，论文与研究主线的相关性在 `research/` 下相应 guide 或调研页说明
- 新建中文译文：复制 `schema/templates/translation-note.md` 到对应 `translations/` 目录，按原文章节建框架并遵循 `schema/page-schemas.md` 逐节推进和核验；`sources/` 中的 PDF 是唯一核验基准
- 文献阅读先从 `literature/_index.md` 按个人研究主线进入；单篇论文仍按主要贡献选择物理目录，交叉论文可在多条主线中出现但不复制文件
- 新建概念页：复制 `schema/templates/concept-note.md`
- 新建目录语义索引：复制 `schema/templates/directory-index.md` 到对应目录的 `_index.md`，说明收录范围并维护核心条目导航表格，避免建立第二套状态账
- 新建调研、实体、工作汇报与论文：暂不设专用模板，按实际内容组织，遵循 [schema/page-schemas.md](schema/page-schemas.md) 维护最小元数据与客观事实边界
- 进入内容目录时先读该目录 `_index.md`；页面间一律用 Obsidian `[[wikilink]]` 互链
- 新增、移动、删除或重组页面后，收尾检查对应目录 `_index.md`；影响全库导航时同步根 `index.md`
- 报告完成后，先将长期事实抽取到概念页、技术线或调研页，再把最终交付物和准备材料整体移入 `archive/<event>/`
- 页面要求统一见 [page-schemas.md](schema/page-schemas.md)，模板提供写法；协作与提交纪律见 [AGENTS.md](AGENTS.md)。
- 原始资料的存储职责以 [页面规范](schema/page-schemas.md#存储与来源) 为准：iCloud 保存官方及个人原件与论文 PDF，Git 不作为原件归档位置；换机后运行 `restore_sources_from_icloud.ps1` 从 iCloud `文献库/` 恢复 `literature/**/sources/`。
- 参考文献统一维护在 `literature/refs.bib`

## 研究入口

本仓库以博士后核心研究项目为主要牵引，围绕 PIML、Matrix-Free 和 GPU/HPC 组织主线二的两年科研工作；同时维护 Hu–Zhang、VEM 等博士阶段延续成果。基金申请是条件性资助渠道，工作汇报、技术线、概念页和文献笔记分别承担执行沟通、能力建设与证据沉淀。

- [全库内容地图与当前科研架构](index.md)
- [个人长期科研主线与博士后成果路线](research/long-term-research-lines.md)
- [博士后核心研究项目两年计划](research/piml-matrix-free-gpu/project-plan.md)

---

*大连理工大学 · 博士后研究*
