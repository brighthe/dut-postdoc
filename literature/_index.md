---
title: "文献阅读笔记总索引"
type: index
aliases:
  - "literature/piml/_index"
  - "物理信息机器学习文献入口"
tags:
  - literature
status: in-progress
date_added: null
date_update: 2026-08-04
---

# 文献阅读笔记总索引

> 本页是文献层的唯一总入口和当前 ingest 队列。研究 guide 维护跨文献综合，单篇笔记维护论文事实；只有形成实际笔记集合的主题才建立独立入口，不为仅有候选清单的主题预建目录。

## 按个人研究主线导航

| 个人研究主线 | 文献与综合入口 | 组织边界 |
|---|---|---|
| [[../research/long-term-research-lines#主线一：高精度数值离散与拓扑优化\|主线一]] | [[topology-opt/_index\|拓扑优化已入库文献]] | 当前覆盖 MMC/MMV、机器学习和 PIML 拓扑优化；Hu–Zhang 与 VEM 外部文献尚未形成稳定笔记集合 |
| [[../research/long-term-research-lines#主线二：智能高性能计算力学\|主线二]] | [[matrix-free/_index\|Matrix-Free 方法文献]]；[[../research/technical-lines/matrix-free-research-guide\|Matrix-Free 证据综合]]；[[../research/technical-lines/piml-research-guide\|PIML 证据综合]]；[[topology-opt/_index\|拓扑优化应用文献]] | 主题入口管理实际笔记，guide 回答“证据如何支撑研究”，本页只维护 ingest 队列；单篇论文只保存一份 |

## 已入库文献

- [[topology-opt/_index]] — 当前实际存在的拓扑优化、MMC/MMV、PIML 与交叉应用笔记、译文和派生图片。
- [[matrix-free/_index]] — 以 Matrix-Free 方法为主要贡献的实际笔记与译文；拓扑优化交叉论文只建立链接。
- `literature/others/Guo2023-PIML-substructure.md` — 历史 redirect，不作为当前入口重复登记。

单篇笔记的 frontmatter 是 `draft → read → done` 状态的唯一事实源；中文译文达到 `done` 前，笔记保持 `draft` 且不作为全文级证据。本页不复制已建立笔记的逐篇状态。

## 当前 ingest 队列

本表是未建单篇笔记文献的唯一 `to-ingest` 状态账。只有全文、Zotero item 和 Better BibTeX Citation Key 均核验，并完成笔记、BibTeX 与关联同步后，才从本表移除。

| 方向 | 文献 | 当前作用与证据入口 | 状态 |
|---|---|---|---|
| Matrix-Free | Hughes, Levit & Winget (1983), *An element-by-element solution algorithm for problems of structural and solid mechanics* | EBE 历史起点；[[../research/technical-lines/matrix-free-research-guide#四、证据锚点及结论边界]] | `to-ingest` |
| Matrix-Free | Liu, Zhou & Yang (2007), *A distributed memory parallel element-by-element scheme based on Jacobi-conditioned conjugate gradient for 3D finite element analysis* | 国内 distributed-memory EBE/MPI；同上 | `to-ingest` |
| Matrix-Free × TO | Bian & Fang (2017), *Large-scale buckling-constrained topology optimization based on assembly-free finite element analysis* | 国内 assembly-free 三维拓扑优化；同上 | `to-ingest` |
| Matrix-Free | Pazner (2020), *Efficient Low-Order Refined Preconditioners for High-Order Matrix-Free Continuous and Discontinuous Galerkin Methods* | Matrix-Free 主算子与组装预条件器；同上 | `to-ingest` |
| GPU/HPC × TO | Wadbro & Berggren (2009), *Megapixel Topology Optimization on a Graphics Processing Unit* | 商品级 GPU 上的早期完整拓扑优化；[[../research/technical-lines/gpu-hpc-research-guide#三、国内外研究现状、研究缺口与选题价值]] | `to-ingest` |
| GPU/HPC × Matrix-Free × TO | Schmidt & Schulz (2011/2012), *A 2589 line topology optimization code written for the graphics card* | 三维线弹性全 GPU 与 Matrix-Free CG；同上 | `to-ingest` |
| GPU/HPC × Matrix-Free | Martínez-Frutos & Herrero-Pérez (2015), *Efficient matrix-free GPU implementation of Fixed Grid Finite Element Analysis* | DoF-level Matrix-Free、数据局部性和显存；同上 | `to-ingest` |
| GPU/HPC × TO | Martínez-Frutos & Herrero-Pérez (2016), *Large-scale robust topology optimization using multi-GPU systems* | 多 GPU 任务级与数据级并行；同上 | `to-ingest` |
| GPU/HPC × Matrix-Free | Abdelfattah et al. (2021), *GPU Algorithms for Efficient Exascale Discretizations* | NVIDIA/AMD 高阶 Matrix-Free 与性能可移植；同上 | `to-ingest` |
| GPU/HPC × TO | Herrero-Pérez & Martínez Castejón (2021), *Multi-GPU acceleration of large-scale density-based topology optimization* | 分布式 CG、聚合 AMG、混合精度和多 GPU 容量；同上 | `to-ingest` |
| GPU/HPC × TO | Hou et al. (2025), *Parallel computing on GPU with CuPy and vectorized SpMV for large-scale topology optimization* | 国内 Python/CuPy GPU 路线；全局矩阵边界待全文核验；同上 | `to-ingest` |
| GPU/HPC × TO | Liu et al. (2026), *Concurrent 3D topology optimization ... with CPU-GPU heterogeneous parallelism* | 国内 CPU–GPU 异构响应与灵敏度路线；同上 | `to-ingest` |
| Physics-Informed ML | Raissi et al. (2019), *Physics-informed neural networks* | PINN 正／反问题范式；[[../research/technical-lines/piml-research-guide#4.1 核心文献证据矩阵]] | `to-ingest` |
| Physics-Informed ML | Karniadakis et al. (2021), *Physics-informed machine learning* | Physics-Informed ML 总体框架；同上 | `to-ingest` |
| Operator Learning | Lu et al. (2021), *Learning nonlinear operators via DeepONet* | 非线性算子学习表示；同上 | `to-ingest` |
| Structure-Preserving ML | Xu et al. (2021), SPD-NN constitutive learning | Cholesky 因子化保持对称正定的类比；同上 | `to-ingest` |
| Physics-Informed TO | PINNTO (2023) | energy-based PINN 替代结构分析；同上 | `to-ingest` |

已建立 `draft` 笔记与译文骨架的 [[matrix-free/notes/Kronbichler2012-parallel-cell-operator|Kronbichler 2012]]、[[topology-opt/notes/Zhou2025-efficientaccelerationstrategies|Zhou 2025]]、[[topology-opt/notes/Traff2023-GPU-topology-optimisation|Träff 2023]]、[[topology-opt/notes/Zhang2024-isoparametric-PIML|Zhang 2024（等参 PIML）]]、[[topology-opt/notes/Xu2025-PIML-lattice-MMC|Xu 2025（PIML–MMC 点阵）]]、[[topology-opt/notes/Guo2026-highgeneralization-bezier|Guo 2026（Bézier）]]、[[topology-opt/notes/Guo2026-PIML-OFEM|Guo 2026（PIML-OFEM）]]，以及已经完成 ingest 的 [[topology-opt/notes/Ma2026-highperformanceparallel|Ma 2026]]，均不在只管理“尚未建立笔记”文献的本表重复登记；其状态以单篇 frontmatter 和所属主题索引为准。

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

- 单篇论文只保存一份；交叉属性通过 frontmatter tags、research guide 和概念页表达。
- 未来单篇笔记的物理落点在实际 ingest 时按主要问题和已有内容规模决定，不为候选清单预建空主题目录。
- 原始 PDF 保存在 Zotero，不复制到 Git；只有官方摘要或元数据时，不形成全文级技术结论。
- `topology-opt/` 与 `matrix-free/` 均已有实际笔记和译文，因此保留真实主题入口；PIML 通用文献尚未形成实际笔记集合，继续由研究 guide 和本页队列管理。

---

*模板：[[../assets/templates/literature-note]]*
