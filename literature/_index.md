---
title: "文献阅读笔记总索引"
type: index
aliases:
  - "文献层入口"
tags:
  - literature
status: in-progress
date_added: null
date_update: 2026-09-03
---

# 文献阅读笔记总索引

> 本页是文献层的**唯一入口**：子主题目录不再各自建 `_index.md`，全部已入库文献在本页逐篇登记。

## 目录结构

`literature/` 下共四个目录：`fem/`（有限元离散方法）、`matrix-free/`（Matrix-Free 与 EBE 算法）、`topopt/`（拓扑优化，按 `gpu-hpc/`、`mmc-mmv/`、`piml/`、`stress-constrained/` 分子类），以及 `inbox/`——**尚未确定分类的论文**，只放 PDF、不建译文页，归属确定后整批移入前三者。

每个主题目录下 `sources/` 放原文 PDF（不入 Git），`translations/` 放 `-zh` 译文。跨文献的证据综合由 [[../research/piml-matrix-free-gpu/piml-research-guide\|PIML]]、[[../research/piml-matrix-free-gpu/matrix-free-research-guide\|Matrix-Free]]、[[../research/piml-matrix-free-gpu/gpu-hpc-research-guide\|GPU/HPC]] 三份 research guide 承担（对应 [[../research/long-term-research-lines\|两条研究主线]]），本页只回答"库里有哪些证据、到什么状态"。

## 已入库文献

共 **15 篇译文 + 3 篇仅有原文**。`状态` 取自各 `-zh` frontmatter，是 `draft → read → done` 的唯一事实源，本页不另立状态账；未达 `done` 的译文不作为全文级证据。`raw` 指同主题 `sources/` 下是否有对应 PDF（PDF 不入 Git，见"管理边界"）。

### `matrix-free/`

| 译文 | 中文标题 | 出处 | 状态 | raw |
|---|---|---|---|---|
| [[matrix-free/translations/Kronbichler2012-parallel-cell-operator-zh\|Kronbichler 2012]] | 并行基于单元的有限元算子应用通用接口 | *Computers & Fluids* 63: 135–147 | `draft` | ✓ |

### `topopt/gpu-hpc/`

| 译文 | 中文标题 | 出处 | 状态 | raw |
|---|---|---|---|---|
| [[topopt/gpu-hpc/translations/Traff2023-GPU-topology-optimisation-zh\|Träff 2023]] | 简单高效的 GPU 加速拓扑优化：代码与应用 | *CMAME* 410: 116043 | `draft` | ✓ |
| [[topopt/gpu-hpc/translations/Zhou2025-efficientaccelerationstrategies-zh\|Zhou 2025]] | 面向快速三维拓扑优化的多重网格预条件共轭梯度高效加速策略 | *J. Comput. Math.* 43(5): 1063–1091 | `draft` | ✓ |

### `topopt/mmc-mmv/`

| 译文 | 中文标题 | 出处 | 状态 | raw |
|---|---|---|---|---|
| [[topopt/mmc-mmv/translations/Zhang2016-MMC-topology-zh\|Zhang 2016（MMC）]] | 基于移动可变形组件（MMC）与替代材料模型的拓扑优化新方法 | *SMO* 53: 1243–1260 | `read` | ✓ |
| [[topopt/mmc-mmv/translations/Zhang2016-minimum-length-scale-zh\|Zhang 2016（最小长度尺度）]] | 基于移动可变形组件（MMC）方法的结构拓扑优化最小长度尺度控制 | *CMAME* | `draft` | ✓ |
| [[topopt/mmc-mmv/translations/Zhang2017-MMV-3D-zh\|Zhang 2017（MMV）]] | 基于移动可变形空洞（MMV）方法的显式三维拓扑优化 | *CMAME* 322: 590–614 | `read` | ✓ |
| [[topopt/mmc-mmv/translations/Lei2018-machinelearningdriven-zh\|Lei 2018]] | 基于移动可变形组件（MMC）框架的机器学习驱动实时拓扑优化 | *J. Appl. Mech.* 86(1): 011004 | `done` | ✓ |

### `topopt/piml/`

| 译文 | 中文标题 | 出处 | 状态 | raw |
|---|---|---|---|---|
| [[topopt/piml/translations/Huang2022-problemindependentmachine-zh\|Huang 2022]] | 基于问题无关机器学习（PIML）的拓扑优化——一种通用方法 | *EML* 56: 101887 | `read` | ✓ |
| [[topopt/piml/translations/Huang2023-PIML-substructure-zh\|Huang 2023]] | 一种通用（与问题无关）机器学习增强的基于子结构的大规模线弹性结构分析与拓扑优化方法 | *EML* 63: 102041 | `done` | ✓ |
| [[topopt/piml/translations/Huang2024-PIML-datafree-zh\|Huang 2024]] | 一种基于力学机制的无数据问题无关机器学习（PIML）模型：用于大规模结构分析与设计优化 | *JMPS* 193: 105893 | `done` | ✓ |
| [[topopt/piml/translations/Zhang2024-isoparametric-PIML-zh\|Zhang 2024（等参 PIML）]] | 基于等参单元的问题无关机器学习增强复杂设计域结构拓扑优化 | *EML* 72: 102237 | `draft` | ✓ |
| [[topopt/piml/translations/Xu2025-PIML-lattice-MMC-zh\|Xu 2025（PIML–MMC 点阵）]] | 基于移动可变形构件法的问题无关机器学习增强三维点阵复合结构优化 | *Composite Structures* 369: 119330 | `draft` | ✓ |
| [[topopt/piml/translations/Ma2026-highperformanceparallel-zh\|Ma 2026]] | 基于问题无关机器学习（PIML）的大规模拓扑优化高性能并行算法 | *Acta Mech. Sin.* 42(3): 425942 | `read` | ✓ |
| [[topopt/piml/translations/Guo2026-highgeneralization-bezier-zh\|Guo 2026（Bézier）]] | 基于子结构边界位移三次 Bézier 插值的高泛化 AI 增强力学分析与拓扑优化 | *CMAME* 456: 118955 | `draft` | ✓ |
| [[topopt/piml/translations/Guo2026-PIML-OFEM-zh\|Guo 2026（PIML-OFEM）]] | PIML-OFEM：一种基于问题无关机器学习与重叠有限元技术的大规模结构分析新方法 | arXiv v1 预印本 | `draft` | ✓ |

### 仅有原文、尚无译文

下列 PDF 已在库但未建 `-zh` 页；元数据由 PDF 首页核验，BibTeX 条目已补入 `literature/refs.bib`（citation key 为手工命名，**待与 Zotero 核验**）。

| 目录 | 文献 | 出处 |
|---|---|---|
| `fem/sources/` | Hu & Zhang (2016), *Finite element approximations of symmetric tensors on simplicial grids in Rⁿ: The lower order case* | *M3AS* 26(9): 1649–1669，DOI `10.1142/S0218202516500408`，citekey `Hu2016-symmetrictensorslower` |
| `topopt/stress-constrained/sources/` | Holmberg, Torstenfelt & Klarbring (2013), *Stress constrained topology optimization* | *SMO* 48: 33–47，DOI `10.1007/s00158-012-0880-7`，citekey `Holmberg2013-stressconstrained` |
| `topopt/stress-constrained/sources/` | Giraldo-Londoño & Paulino (2021), *PolyStress: a Matlab implementation for local stress-constrained topology optimization using the augmented Lagrangian method* | *SMO* 63: 2065–2097，DOI `10.1007/s00158-020-02760-8`，citekey `GiraldoLondono2021-polystress` |

`refs.bib` 中的 `huFiniteElementApproximations2015`（*JCM* 33(3): 283–296）是同系列的 **higher order case**，与 `fem/sources/` 下的 lower order case 是两篇不同论文，勿混用 citation key。

## 当前 ingest 队列

本表是未建单篇笔记文献的唯一 `to-ingest` 状态账。只有全文、Zotero item 和 Better BibTeX Citation Key 均核验，并完成笔记、BibTeX 与关联同步后，才从本表移除。

| 方向 | 文献 | 当前作用与证据入口 | 状态 |
|---|---|---|---|
| Matrix-Free | Hughes, Levit & Winget (1983), *An element-by-element solution algorithm for problems of structural and solid mechanics* | EBE 历史起点；[[../research/piml-matrix-free-gpu/matrix-free-research-guide#四、证据锚点及结论边界]] | `to-ingest` |
| Matrix-Free | Liu, Zhou & Yang (2007), *A distributed memory parallel element-by-element scheme based on Jacobi-conditioned conjugate gradient for 3D finite element analysis* | 国内 distributed-memory EBE/MPI；同上 | `to-ingest` |
| Matrix-Free × TO | Bian & Fang (2017), *Large-scale buckling-constrained topology optimization based on assembly-free finite element analysis* | 国内 assembly-free 三维拓扑优化；同上 | `to-ingest` |
| Matrix-Free | Pazner (2020), *Efficient Low-Order Refined Preconditioners for High-Order Matrix-Free Continuous and Discontinuous Galerkin Methods* | Matrix-Free 主算子与组装预条件器；同上 | `to-ingest` |
| GPU/HPC × TO | Wadbro & Berggren (2009), *Megapixel Topology Optimization on a Graphics Processing Unit* | 商品级 GPU 上的早期完整拓扑优化；[[../research/piml-matrix-free-gpu/gpu-hpc-research-guide#三、国内外研究现状、研究缺口与选题价值]] | `to-ingest` |
| GPU/HPC × Matrix-Free × TO | Schmidt & Schulz (2011/2012), *A 2589 line topology optimization code written for the graphics card* | 三维线弹性全 GPU 与 Matrix-Free CG；同上 | `to-ingest` |
| GPU/HPC × Matrix-Free | Martínez-Frutos & Herrero-Pérez (2015), *Efficient matrix-free GPU implementation of Fixed Grid Finite Element Analysis* | DoF-level Matrix-Free、数据局部性和显存；同上 | `to-ingest` |
| GPU/HPC × TO | Martínez-Frutos & Herrero-Pérez (2016), *Large-scale robust topology optimization using multi-GPU systems* | 多 GPU 任务级与数据级并行；同上 | `to-ingest` |
| GPU/HPC × Matrix-Free | Abdelfattah et al. (2021), *GPU Algorithms for Efficient Exascale Discretizations* | NVIDIA/AMD 高阶 Matrix-Free 与性能可移植；同上 | `to-ingest` |
| GPU/HPC × TO | Herrero-Pérez & Martínez Castejón (2021), *Multi-GPU acceleration of large-scale density-based topology optimization* | 分布式 CG、聚合 AMG、混合精度和多 GPU 容量；同上 | `to-ingest` |
| GPU/HPC × TO | Hou et al. (2025), *Parallel computing on GPU with CuPy and vectorized SpMV for large-scale topology optimization* | 国内 Python/CuPy GPU 路线；全局矩阵边界待全文核验；同上 | `to-ingest` |
| GPU/HPC × TO | Liu et al. (2026), *Concurrent 3D topology optimization ... with CPU-GPU heterogeneous parallelism* | 国内 CPU–GPU 异构响应与灵敏度路线；同上 | `to-ingest` |
| Physics-Informed ML | Raissi et al. (2019), *Physics-informed neural networks* | PINN 正／反问题范式；[[../research/piml-matrix-free-gpu/piml-research-guide#4.1 核心文献证据矩阵]] | `to-ingest` |
| Physics-Informed ML | Karniadakis et al. (2021), *Physics-informed machine learning* | Physics-Informed ML 总体框架；同上 | `to-ingest` |
| Operator Learning | Lu et al. (2021), *Learning nonlinear operators via DeepONet* | 非线性算子学习表示；同上 | `to-ingest` |
| Structure-Preserving ML | Xu et al. (2021), SPD-NN constitutive learning | Cholesky 因子化保持对称正定的类比；同上 | `to-ingest` |
| Physics-Informed TO | PINNTO (2023) | energy-based PINN 替代结构分析；同上 | `to-ingest` |

已建立 `-zh` 译文页面的文献一律不在本表重复登记——本表只管理"尚未建立页面"的文献；已入库者见上文「已入库文献」，状态以各 `-zh` frontmatter 为准。

## 待归类文献（`inbox/`）

`inbox/sources/` 是尚未确定主题归属的论文 PDF 副本的暂存容器（不入 Git），目前收纳 [[../concepts/density-topopt/regularization-and-length-scale-control]] 所引的正则化与长度尺度控制经典文献。暂存阶段只放 PDF 与 `literature/refs.bib` 条目，**不建 `-zh` 译文页**；待归属确定后整篮移入 `topopt/` 相应子类，再在目标目录建页，避免搬迁时改写双链。PDF 文件名按 `AuthorYear-short-topic.pdf`。

| 文献 | citation key | 预期 PDF 文件名 | 被引位置 | 状态 |
|---|---|---|---|---|
| Haber, Jog & Bendsøe (1996), *A new approach to variable-topology shape design using a constraint on perimeter* | `Haber1996-perimeterconstraint`（待与 Zotero 核验） | `Haber1996-perimeterconstraint.pdf` | 概念页 §7 周长约束 | `unsorted` |
| Sigmund (1997), *On the design of compliant mechanisms using topology optimization* | `sigmundDesignCompliantMechanisms1997a` | `Sigmund1997-designcompliantmechanisms.pdf` | 概念页 §2.1 灵敏度过滤 | `unsorted` |
| Sigmund & Petersson (1998), *Numerical instabilities in topology optimization* | `sigmundNumericalInstabilitiesTopology1998` | `Sigmund1998-numericalinstabilities.pdf` | 概念页 §1 数值不稳定性综述 | `unsorted` |
| Petersson & Sigmund (1998), *Slope constrained topology optimization* | `peterssonSlopeConstrainedTopology1998` | `Petersson1998-slopeconstrained.pdf` | 概念页 §7 斜率约束 | `unsorted` |
| Bourdin (2001), *Filters in topology optimization* | `bourdinFiltersTopologyOptimization2001` | `Bourdin2001-filterstopologyoptimization.pdf` | 概念页 §2.2 密度过滤存在性 | `unsorted` |
| Bruns & Tortorelli (2001), *Topology optimization of non-linear elastic structures and compliant mechanisms* | `brunsTopologyOptimizationNonlinear2001` | `Bruns2001-topologyoptimizationnonlinear.pdf` | 概念页 §2.2 密度过滤提出 | `unsorted` |
| Guest, Prévost & Belytschko (2004), *Achieving minimum length scale in topology optimization using nodal design variables and projection functions* | `guestAchievingMinimumLength2004b` | `Guest2004-achievingminimumlength.pdf` | 概念页 §4.1 指数型投影 | `unsorted` |
| Sigmund (2007), *Morphology-based black and white filters for topology optimization* | `sigmundMorphologybasedBlackWhite2007b` | `Sigmund2007-morphologybasedblackwhite.pdf` | 概念页 §4.1、§7 形态学过滤 | `unsorted` |
| Xu, Cai & Cheng (2010), *Volume preserving nonlinear density filter based on Heaviside functions* | `xuVolumePreservingNonlinear2010` | `Xu2010-volumepreservingnonlinear.pdf` | 概念页 §7 体积保持过滤 | `unsorted` |
| Wang, Lazarov & Sigmund (2011), *On projection methods, convergence and robust formulations in topology optimization* | `wangProjectionMethodsConvergence2011a` | `Wang2011-projectionmethodsconvergence.pdf` | 概念页 §4.1–4.3 tanh 投影与稳健三场 | `unsorted` |
| Lazarov & Sigmund (2011), *Filters in topology optimization based on Helmholtz-type differential equations* | `Lazarov2011-helmholtzpdefilter`（待与 Zotero 核验） | `Lazarov2011-helmholtzpdefilter.pdf` | 概念页 §7 PDE 过滤 | `unsorted` |

Bendsøe & Sigmund (2004) 专著（`Bendsoe2004-topologyoptimizationa`）留在 Zotero，不复制到 `inbox/`。前 9 条 citation key 直接沿用 `xtu-phd-thesis:thesis/reference/ref.bib` 的 Better BibTeX key；标注"待与 Zotero 核验"的两条为临时 key，核验后需同步替换本表与 `literature/refs.bib`。

## 储备候选池

下列文献只是后续 PA、GPU、MPI、预条件或拓扑优化调研的发现记录，不属于当前 ingest 队列，不维护第二套状态账；准备实际阅读时再移入上表。

| 文献 | 候选作用 |
|---|---|
| [Suresh 2013](https://doi.org/10.1007/s00158-012-0807-3) | 多核 CPU、EA/EbE 与 Pareto 拓扑优化 |
| [Yadav & Suresh 2014](https://doi.org/10.1115/1.4028591) | 低阶固体力学、assembly-free deflated CG 与 GPU |
| [Wu, Dick & Westermann 2016](https://doi.org/10.1109/TVCG.2015.2502588) | GPU multigrid、按需 stencil 与高分辨率拓扑优化 |
| [Martínez-Frutos et al. 2017](https://doi.org/10.1016/j.advengsoft.2017.01.009) | Matrix-Free PCG、Jacobi/GMG 与完整拓扑优化计时 |
| [Kronbichler & Ljungkvist 2019](https://doi.org/10.1145/3322813) | 高阶 Matrix-Free multigrid 的 GPU 映射 |
| [Kronbichler & Kormann 2019](https://doi.org/10.1145/3325864) | DG sum factorization、SIMD、MPI 与 Roofline |
| [Davydov et al. 2020](https://doi.org/10.1002/nme.6336) | 非线性固体力学与 geometric multigrid |
| [Davydov & Kronbichler 2020](https://doi.org/10.1145/3399736) | MPI 稀疏多向量数据结构与扩展性 |
| [Brown et al. 2021](https://doi.org/10.21105/joss.02945) | libCEED 的 restriction–basis–QFunction 算子分解 |
| [Ratnakar, Kiran & Sharma 2022](https://doi.org/10.1108/EC-01-2022-0022) | 非结构网格、对称 EA/EbE 与 GPU 拓扑优化 |
| [Schussnig et al. 2025](https://doi.org/10.1016/j.cma.2024.117600) | 非线性固体、高阶 Matrix-Free 与 hp-multigrid |
| [Wei, Liu & Guo, WCCM–ECCOMAS 2026](https://wccm-eccomas2026.org/event/contribution/b0feec06-031e-11f1-919d-000c29ddfc0c), *Problem Independent Machine Learning-Based Fast and High Accuracy Topology Optimization for Large Scale Heat Conduction Structures* | PIML 向大规模传热拓扑优化及内部节点热载荷处理扩展的会议摘要线索；当前仅有官方 contribution 页面，不建立单篇笔记或 BibTeX，待正式会议论文／摘要 PDF 或后续期刊版本 |

## 管理边界

- **唯一入口**：新增文献必须在本页「已入库文献」登记，否则视为未入库；单篇论文只保存一份，交叉属性由 frontmatter tags、research guide 与概念页表达，不建重定向桩页。
- **raw 层**：原始 PDF 放在所属主题的 `sources/` 下（`.gitignore` 排除，不入 Git），PDF 文件名与译文页 basename 严格对应（`AuthorYear-short-topic.pdf` ↔ `AuthorYear-short-topic-zh.md`），`-zh` 译文以相对路径 `source: "../sources/<同名>.pdf"` 指向它（**不是 citekey**，citekey 另存 `citekey:` 字段）。PDF 是事实源，与译文冲突时以 PDF 为准。
- **raw 的回溯靠标识符，不靠存储位置**：论文的可再获得性由 DOI（预印本用 arXiv ID + 版本号）保证，附件由 Zotero 托管，`literature/refs.bib` 的 citation key 是二者之间的桥。`sources/` 只是供 AI 直接读取的本地缓存，丢失后按 DOI 或 citekey 重建，**不登记 iCloud 路径**——绝对路径不可移植且会腐化。无 DOI、无第三方托管的原件（如基金官方文件）另按 [[../research/funding/sources]] 的「iCloud 相对路径 + SHA-256」方式登记。
- **派生资源**：图片等派生资源统一放 `topopt/assets/`（主题级共用，不下沉到子类），正文按 Obsidian 全库文件名解析引用 `![[名.png]]`，不写相对路径。
- **目录只在有实际内容时建立**：不为候选清单预建空主题目录；`inbox/` 是唯一例外的暂存容器，只放 PDF 副本（`inbox/sources/`，不入 Git）与对应 `refs.bib` 条目，不作为长期落点。
- 只有官方摘要或元数据时，不形成全文级技术结论。

---

*模板：[[../ai/templates/translation-note]]*
