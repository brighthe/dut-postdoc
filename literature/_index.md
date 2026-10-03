---
title: "文献总索引"
type: index
aliases:
  - "文献层入口"
  - "文献阅读笔记总索引"
tags:
  - literature
status: in-progress
date_added: 2026-06-24
date_update: 2026-10-03
---

# 文献总索引

> 本页是文献层的**唯一入口**：子主题目录不再各自建 `_index.md`，全部已入库文献在本页逐篇登记。

## 目录结构

`literature/` 下共五个目录：`fem/`（有限元离散方法）、`matrix-free/`（Matrix-Free 与 EBE 算法）、`fem-libraries/`（有限元框架与库的官方描述论文，按软件而非方法归类，对应 `concepts/` 的 L3「外部实现对象」层，如 MFEM、libCEED、DOLFINx、Firedrake；以算法为主的实现论文仍归 `matrix-free/` 等方法目录）、`topopt/`（拓扑优化，按 `element-types/`、`frameworks/`、`gpu-hpc/`、`matrix-free/`、`mixed-fem/`、`mmc-mmv/`、`piml/`、`stress-constrained/`、`substructuring/` 分子类；其中 `element-types/` 只收「单元类型或阶次选择本身作为研究对象」的文献，与 `mixed-fem/` 的变分格式之争互补，`frameworks/` 收录以拓扑优化通用框架、模块化架构与教学代码为主要贡献的文献，`substructuring/` 收录以子结构、多尺度粗单元或区域分解求解拓扑优化平衡方程为主要贡献的文献（网络预测局部算子的仍归 `piml/`），`matrix-free/` 收录以 matrix-free 算子作用（免组装全局刚度矩阵）为主要贡献的拓扑优化文献，与通用 FEM 算法的顶层 `matrix-free/` 对应，以 GPU 上多重网格或 PCG 加速策略为主的仍归 `gpu-hpc/`；研究 GPU 实现或约束类型的文献仍按其主题归入对应子类），以及 `inbox/`——**尚未确定分类的论文**，只放 PDF、不建译文页，归属确定后整批移入前四者。

每个主题目录下 `sources/` 放原文 PDF 的本地副本（不入 Git，主档见「存储与维护说明」），`translations/` 放 `-zh` 译文。跨文献的证据综合由 [[../research/piml-matrix-free-gpu/piml-research-guide\|PIML]]、[[../research/piml-matrix-free-gpu/matrix-free-research-guide\|Matrix-Free]]、[[../research/piml-matrix-free-gpu/gpu-hpc-research-guide\|GPU/HPC]] 三份 research guide 承担（对应 [[../research/long-term-research-lines\|两条研究主线]]），本页只回答"库里有哪些证据、到什么状态"。

## 已入库文献

共 **50 篇译文**。`状态` 取自各 `-zh` frontmatter，是 `draft → read → done` 的唯一事实源，本页不另立状态账；未达 `done` 的译文不作为全文级证据。`raw` 指同主题 `sources/` 下是否有对应 PDF（PDF 不入 Git，见"存储与维护说明"）。

### `fem/`

| 译文 | 中文标题 | 出处 | 状态 | raw |
|---|---|---|---|---|
| [[fem/translations/Hu2016-symmetric-tensors-simplicial-zh\|Hu 2016]] | 单单纯形网格上对称张量的有限元逼近：低阶情形 | *M3AS* 26(9): 1649–1669 | `draft` | ✓ |
| [[fem/translations/Carstensen2019-arnold-winther-aposteriori-zh\|Carstensen 2019]] | 对称混合 Arnold–Winther 有限元的基于残差的后验误差分析（附录 B 给出牵引提升分解与先验误差估计） | *Numer. Math.* 142(2): 205–234 | `draft` | ✓ |
| [[fem/translations/Codina2024-stabilized-mixed-hyperelasticity-zh\|Codina 2024]] | 涉及位移与应力和/或压力的有限应变超弹性稳定化混合模型的有限元逼近——不同方案概述 | *IJNME* 125(18): e7540 | `draft` | ✓ |
| [[fem/translations/Hu2015-symmetric-tensors-higher-order-zh\|Hu2015]] | 单纯形网格上对称张量的有限元逼近：高阶情形 | *Journal of Computational Mathematics*, 33(3): 283–296, 2015 | `draft` | ✓ |
| [[fem/translations/Chen2024-geometric-face-edge-elements-zh\|Chen2024]] | 高阶面元与棱元的几何分解及高效实现 | *Communications in Computational Physics*, 35(4): 1045–1072, 2024 | `draft` | ✓ |
| [[fem/translations/Hu2021-vertex-continuity-relaxation-zh\|Hu 与 Ma 2021]] | 弹性问题协调混合有限元应力顶点连续性的部分松弛 | *CMAM* 21(1): 89–108 | `read` | ✓ |
| [[fem/translations/Hu2014-rectangular-mixed-elasticity-zh\|Hu 等 2014]] | 任意空间维数下矩形网格上线弹性问题的一种简单协调混合有限元 | *J. Sci. Comput.* 58: 367–379 | `draft` | ✓ |
| [[fem/translations/Chen2017-stabilized-mixed-elasticity-zh\|Chen 等 2017]] | 单纯形网格上 $\mathbb{R}^n$ 中线弹性的稳定化混合有限元方法（最低阶自由度最少；含间断位移跃度稳定化与连续位移稳定化两类格式） | *CMAM* 17(1): 17–31 | `read` | ✓ |
| [[fem/translations/Chen2018-fast-auxiliary-space-preconditioners-zh\|Chen 等 2018]] | 混合形式线弹性问题的快速辅助空间预条件子（基于应力非协调元与位移向量 Laplacian 辅助空间的统一 FASP 框架） | *Math. Comp.* 87(312): 1601–1633 | `read` | ✓ |
| [[fem/translations/Chen2018-residual-aposteriori-elasticity-zh\|Chen 等 2018]] | 线弹性问题对称协调混合有限元基于残差的后验误差估计（基于线弹性微分复形与 Argyris 准插值，直接估计对称应力而无需非对称梯度逼近） | *Sci. China Math.* 61(6): 973–992 | `read` | ✓ |
| [[fem/translations/Hou1999-msfem-convergence-zh\|Hou 等 1999]] | 快速振荡系数椭圆问题多尺度有限元方法的收敛性（MsFEM 线性边界的共振误差与过采样） | *Math. Comp.* 68(227): 913–943 | `draft` | ✓ |
| [[fem/translations/Zhang2010-emsfem-heterogeneous-zh\|Zhang 等 2010]] | 用于非均质材料力学分析的扩展多尺度有限元方法（EMsFEM；比较线性、过采样与周期边界） | *Acta Mech. Sin.* 26(6): 899–920 | `draft` | ✓ |
| [[fem/translations/Babuska1992-locking-elasticity-zh\|Babuška & Suri 1992]] | 弹性问题有限元逼近中的自锁效应（定义自锁度与鲁棒性；分析三角形与矩形网格各阶 h 版本自锁阶，证明 p 与 h-p 版本能量范数下无自锁） | *Numer. Math.* 62: 439–463 | `draft` | ✓ |


### `matrix-free/`

| 译文 | 中文标题 | 出处 | 状态 | raw |
|---|---|---|---|---|
| [[matrix-free/translations/Kronbichler2012-parallel-cell-operator-zh\|Kronbichler 2012]] | 并行基于单元的有限元算子应用通用接口 | *Computers & Fluids* 63: 135–147 | `draft` | ✓ |
| [[matrix-free/translations/Kolev2021-CEED-exascale-discretizations-zh\|Kolev 2021]] | 高效的百亿亿次离散：高阶有限元方法（CEED 总论：算子分解、BP 基准、libCEED） | *IJHPCA* 35(6): 527–552 | `draft` | ✓ |
| [[matrix-free/translations/Fischer2020-scalability-PDE-solvers-zh\|Fischer 2020]] | 高性能 PDE 求解器的可扩展性（BP1–BP6 在 libCEED、MFEM、Nek5000、deal.II 上的强扩展比较） | *IJHPCA* 34(5): 562–586（待确认，PDF 为 OnlineFirst） | `draft` | ✓ |
| [[matrix-free/translations/Abdelfattah2021-GPU-exascale-discretizations-zh\|Abdelfattah 2021]] | 面向高效百亿亿次离散的 GPU 算法（libCEED、MAGMA、MFEM、libParanumal、Nek 的 GPU kernel 与应用） | *Parallel Computing* 108: 102841 | `draft` | ✓ |
| [[matrix-free/translations/Brown2022-matrix-free-p-multigrid-solids-zh\|Brown 2022]] | 借助 Matrix-free p-多重网格实现性能可移植的固体力学（libCEED/Ratel 超弹性、p-MG + AMG） | arXiv:2204.01722v3（发表状态待确认） | `draft` | ✓ |

### `fem-libraries/`

本目录对应软件的源码仓库（upstream、WSL 本地副本）登记在 [[fem-libraries/sources]]，页面引用源码写 `<仓库名>:<相对路径>` 并由该表解析。

| 译文 | 中文标题 | 出处 | 状态 | raw |
|---|---|---|---|---|
| [[fem-libraries/translations/Anderson2021-MFEM-modular-library-zh\|Anderson 2021]] | MFEM：一个模块化有限元方法库 | *CAMWA* 81: 42–74 | `draft` | ✓ |
| [[fem-libraries/translations/Andrej2024-MFEM-high-performance-zh\|Andrej 2024]] | MFEM 中的高性能有限元（2021 论文的后续：GPU、四级装配、LOR 求解器） | *IJHPCA* 38(5): 447–467 | `draft` | ✓ |
| [[fem-libraries/translations/Brown2021-libCEED-fast-algebra-zh\|Brown 2021]] | libCEED：面向高阶基于单元离散的快速代数（restriction–basis–QFunction 算子分解的软件论文） | *JOSS* 6(63): 2945 | `draft` | ✓ |

### `topopt/element-types/`

以单元类型或阶次选择本身为研究对象的拓扑优化文献。与 `mixed-fem/` 的分工是：本目录比较同一位移变分格式下的不同单元，`mixed-fem/` 比较不同变分格式。

| 译文 | 中文标题 | 出处 | 状态 | raw |
|---|---|---|---|---|
| [[topopt/element-types/translations/Sarkar2025-quad-elements-topopt-zh\|Sarkar & Kumar 2025]] | 四边形单元拓扑优化：对比研究、代码与教程（Q4/Q8/Q9；全文翻译，含图表及 MATLAB 附录） | *CAEE* 33(3): e70031 | `done` | ✓ |

### `topopt/frameworks/`

以拓扑优化通用框架、模块化架构与教学代码为主要贡献的文献；通用有限元软件归入 `fem-libraries/`，单元类型与阶次比较归入 `element-types/`。

| 译文 | 中文标题 | 出处 | 状态 | raw |
|---|---|---|---|---|
| [[topopt/frameworks/translations/Talischi2012-polytop-zh\|Talischi 等 2012（PolyTop）]] | PolyTop：采用非结构多边形有限元网格的通用拓扑优化框架的 Matlab 实现（全文翻译，含图表及 MATLAB 附录） | *SMO* 45(3): 329–357 | `done` | ✓ |

### `topopt/gpu-hpc/`

| 译文 | 中文标题 | 出处 | 状态 | raw |
|---|---|---|---|---|
| [[topopt/gpu-hpc/translations/Traff2023-GPU-topology-optimisation-zh\|Träff 2023]] | 简单高效的 GPU 加速拓扑优化：代码与应用 | *CMAME* 410: 116043 | `draft` | ✓ |
| [[topopt/gpu-hpc/translations/Zhou2025-efficientaccelerationstrategies-zh\|Zhou 2025]] | 面向快速三维拓扑优化的多重网格预条件共轭梯度高效加速策略 | *J. Comput. Math.* 43(5): 1063–1091 | `draft` | ✓ |

### `topopt/matrix-free/`

| 译文 | 中文标题 | 出处 | 状态 | raw |
|---|---|---|---|---|
| [[topopt/matrix-free/translations/Wang2025-top3d-xl-matrix-free-matlab-zh\|Wang 等 2025（TOP3D_XL）]] | 基于 matrix-free MATLAB 代码的高效大规模三维拓扑优化（全文翻译，含算法 1–2、MATLAB 附录及全部图表） | *SMO* 68: 174 | `read` | ✓ |
| [[topopt/matrix-free/translations/Yang2026-fused-gather-gemm-scatter-zh\|Yang 等 2026]] | 基于融合 Gather–GEMM–Scatter 核函数的 Matrix-Free 三维 SIMP 拓扑优化（全文翻译，含算法 1、表 1–11 位图与数据、图 1–14 高清图件及附录 A–B） | arXiv:2604.18020v1 | `done` | ✓ |
| [[topopt/matrix-free/translations/Fu2023-high-order-structured-diff-topopt-zh\|Fu 等 2023]] | 基于结构化自动微分与高阶有限元的多物理场仿真与拓扑优化（支持混合空间 $H^1/H(\text{div})/L^2$、和分解 PA 机制及低阶 AMG 预条件；含全部图 1–13 高分辨率图件与 50 篇参考文献） | *AIAA SciTech 2023*, 10.2514/6.2023-0530 | `read` | ✓ |

### `topopt/mixed-fem/`

真混合（应力–位移）变分格式下的拓扑优化，对应投稿论文 [[high-order-huzhang-topopt-draft-zh|任意次 Hu–Zhang 混合元拓扑优化]] 的直接前序工作；应力约束这一交叉属性由 frontmatter tags 表达，不在 `stress-constrained/` 重复登记。

| 译文 | 中文标题 | 出处 | 状态 | raw |
|---|---|---|---|---|
| [[topopt/mixed-fem/translations/Bruggi2007-topopt-incompressible-mixed-fem-zh\|Bruggi 2007]] | 基于混合有限元的不可压缩介质拓扑优化（Johnson–Mercier 真混合格式；牵引边界在总装矩阵层面按行列操作施加） | *CMAME* 196(33–34): 3151–3164 | `done` | ✓ |
| [[topopt/mixed-fem/translations/Bruggi2008-mixed-fem-stress-constrained-zh\|Bruggi 2008]] | 应力约束拓扑优化的混合有限元方法（应力为主变量、qp 松弛） | *IJNME* 73(12): 1693–1714 | `done` | ✓ |
| [[topopt/mixed-fem/translations/Bruggi2016-topopt-mixed-fem-regular-grids-zh\|Bruggi 2016]] | 规则网格上基于混合有限元的拓扑优化（HMZ 真混合单元在规则网格上的实现；柔顺度以余能表述、SIMP 惩罚柔度张量；不可压缩介质的应力约束设计） | *CMAME* 305: 133–153 | `done` | ✓ |
| [[topopt/mixed-fem/translations/Castanar2022-topopt-incompressible-mixed-td-zh\|Castañar 等 2022]] | 基于拓扑导数与混合格式的不可压缩结构拓扑优化（u/p 与 u/p/e 稳定化混合元、偏量/球偏极化张量分解、水平集拓扑导数更新） | *CMAME* 390: 114438 | `done` | ✓ |

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
| [[topopt/piml/translations/Zhang2024-isoparametric-PIML-zh\|Zhang 2024（等参 PIML）]] | 基于等参单元的问题无关机器学习增强复杂设计域结构拓扑优化 | *EML* 72: 102237 | `done` | ✓ |
| [[topopt/piml/translations/Xu2025-PIML-lattice-MMC-zh\|Xu 2025（PIML–MMC 点阵）]] | 基于移动可变形构件法的问题无关机器学习增强三维点阵复合结构优化 | *Composite Structures* 369: 119330 | `done` | ✓ |
| [[topopt/piml/translations/Ma2026-highperformanceparallel-zh\|Ma 2026]] | 基于问题无关机器学习（PIML）的大规模拓扑优化高性能并行算法 | *Acta Mech. Sin.* 42(3): 425942 | `read` | ✓ |
| [[topopt/piml/translations/Guo2026-highgeneralization-bezier-zh\|Guo 2026（Bézier）]] | 基于子结构边界位移三次 Bézier 插值的高泛化 AI 增强力学分析与拓扑优化 | *CMAME* 456: 118955 | `done` | ✓ |
| [[topopt/piml/translations/Guo2026-PIML-OFEM-zh\|Guo 2026（PIML-OFEM）]] | PIML-OFEM：一种基于问题无关机器学习与重叠有限元技术的大规模结构分析新方法 | arXiv v1 预印本 | `done` | ✓ |

### `topopt/stress-constrained/`

| 译文 | 中文标题 | 出处 | 状态 | raw |
|---|---|---|---|---|
| [[topopt/stress-constrained/translations/Holmberg2013-stress-constrained-topopt-zh\|Holmberg 2013]] | 应力约束拓扑优化 | *SMO* 48(1): 33–47 | `draft` | ✓ |
| [[topopt/stress-constrained/translations/GiraldoLondono2021-polystress-stress-constrained-zh\|Giraldo-Londoño 2021（PolyStress）]] | PolyStress：基于增广拉格朗日方法的局部应力约束拓扑优化 Matlab 实现 | *SMO* 63(4): 2065–2097 | `draft` | ✓ |
| [[topopt/stress-constrained/translations/GiraldoLondono2020-unified-stress-constraints-zh\|Giraldo-Londoño 2020（统一屈服准则）]] | 考虑多种失效准则的局部应力约束拓扑优化统一方法：von Mises、Drucker–Prager、Tresca、Mohr–Coulomb、Bresler–Pister 与 Willam–Warnke | *Proc. R. Soc. A* 476: 20190861 | `read` | ✓ |

### `topopt/substructuring/`

以子结构、多尺度粗单元或区域分解求解拓扑优化平衡方程为主要贡献的文献，按 [[../concepts/piml/piml-substructural]] 开篇总览表的「精确」两行收录：`linear_corner` 类的多尺度粗单元方法与 `full_trace` 类的区域分解方法；方法奠基文献归入 `fem/`。

| 译文 | 中文标题 | 出处 | 状态 | raw |
|---|---|---|---|---|
| [[topopt/substructuring/translations/Liu2018-msfem-topopt-zh\|Liu 等 2018]] | 基于多尺度有限元方法的高效结构拓扑优化（多节点粗单元，边界取振荡或分段振荡值） | *SMO* 58(4): 1411–1430 | `draft` | ✓ |
| [[topopt/substructuring/translations/Evgrafov2008-fetidp-topopt-zh\|Evgrafov 等 2008]] | 基于对偶–原始子结构求解器的大规模并行拓扑优化（FETI-DP） | *SMO* 36(4): 329–345 | `draft` | ✓ |
| [[topopt/substructuring/translations/Kocvara2016-interface-preconditioning-topopt-zh\|Kočvara 等 2016]] | 拓扑优化问题的约束界面预条件（内点法 + 非重叠区域分解界面 Schur 补） | *SIAM J. Sci. Comput.* 38(1): A128–A145 | `draft` | ✓ |

## 当前 ingest 队列

本表是未建单篇笔记文献的唯一 `to-ingest` 状态账。只有全文存入 iCloud `文献库/`、元数据按 DOI 经 CrossRef 核验并确定 citekey，并完成笔记、BibTeX 与关联同步后，才从本表移除。

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

`inbox/sources/` 是尚未确定主题归属的论文 PDF 副本的暂存容器（不入 Git），目前收纳 [[../concepts/density-topopt/regularization-and-length-scale-control]] 所引的正则化与长度尺度控制经典文献，以及一篇 ELM 求解 PDE 的 SciML 文献。暂存阶段只放 PDF 与 `literature/refs.bib` 条目，**不建 `-zh` 译文页**；待归属确定后整篮移入 `topopt/` 相应子类，再在目标目录建页，避免搬迁时改写双链。PDF 文件名按 `AuthorYear-short-topic.pdf`。

| 文献 | citation key | 预期 PDF 文件名 | 被引位置 | 状态 |
|---|---|---|---|---|
| Haber, Jog & Bendsøe (1996), *A new approach to variable-topology shape design using a constraint on perimeter* | `Haber1996-perimeterconstraint`（元数据待按 DOI 核验） | `Haber1996-perimeterconstraint.pdf` | 概念页 §7 周长约束 | `unsorted` |
| Sigmund (1997), *On the design of compliant mechanisms using topology optimization* | `sigmundDesignCompliantMechanisms1997a` | `Sigmund1997-designcompliantmechanisms.pdf` | 概念页 §2.1 灵敏度过滤 | `unsorted` |
| Sigmund & Petersson (1998), *Numerical instabilities in topology optimization* | `sigmundNumericalInstabilitiesTopology1998` | `Sigmund1998-numericalinstabilities.pdf` | 概念页 §1 数值不稳定性综述 | `unsorted` |
| Petersson & Sigmund (1998), *Slope constrained topology optimization* | `peterssonSlopeConstrainedTopology1998` | `Petersson1998-slopeconstrained.pdf` | 概念页 §7 斜率约束 | `unsorted` |
| Bourdin (2001), *Filters in topology optimization* | `bourdinFiltersTopologyOptimization2001` | `Bourdin2001-filterstopologyoptimization.pdf` | 概念页 §2.2 密度过滤存在性 | `unsorted` |
| Bruns & Tortorelli (2001), *Topology optimization of non-linear elastic structures and compliant mechanisms* | `brunsTopologyOptimizationNonlinear2001` | `Bruns2001-topologyoptimizationnonlinear.pdf` | 概念页 §2.2 密度过滤提出 | `unsorted` |
| Guest, Prévost & Belytschko (2004), *Achieving minimum length scale in topology optimization using nodal design variables and projection functions* | `guestAchievingMinimumLength2004b` | `Guest2004-achievingminimumlength.pdf` | 概念页 §4.1 指数型投影 | `unsorted` |
| Sigmund (2007), *Morphology-based black and white filters for topology optimization* | `sigmundMorphologybasedBlackWhite2007b` | `Sigmund2007-morphologybasedblackwhite.pdf` | 概念页 §4.1、§7 形态学过滤 | `unsorted` |
| Xu, Cai & Cheng (2010), *Volume preserving nonlinear density filter based on Heaviside functions* | `xuVolumePreservingNonlinear2010` | `Xu2010-volumepreservingnonlinear.pdf` | 概念页 §7 体积保持过滤 | `unsorted` |
| Wang, Lazarov & Sigmund (2011), *On projection methods, convergence and robust formulations in topology optimization* | `wangProjectionMethodsConvergence2011a` | `Wang2011-projectionmethodsconvergence.pdf` | 概念页 §4.1–4.3 tanh 投影与稳健三场 | `unsorted` |
| Lazarov & Sigmund (2011), *Filters in topology optimization based on Helmholtz-type differential equations* | `Lazarov2011-helmholtzpdefilter`（元数据待按 DOI 核验） | `Lazarov2011-helmholtzpdefilter.pdf` | 概念页 §7 PDE 过滤 | `unsorted` |
| De Falco, Schiassi & Calabrò (2026), *Least squares with equality constraints extreme learning machines for the resolution of PDEs* | `DeFalco2026-lse-elm-pdes` | `DeFalco2026-lse-elm-pdes.pdf`（已入库） | 暂无；ELM/PINN 求解 PDE，候选 SciML 方向 | `unsorted` |

Bendsøe & Sigmund (2004) 专著（`Bendsoe2004-topologyoptimizationa`）不复制到 `inbox/`。前 9 条 citation key 直接沿用 `xtu-phd-thesis:thesis/reference/ref.bib` 的既有 key；标注"元数据待按 DOI 核验"的两条 key 已是 basename 形式，符合新文献 citekey 规则，予以保留，只需核验 `literature/refs.bib` 中的作者、卷期与页码。

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
| [Ratnakar, Kiran & Sharma 2022](https://doi.org/10.1108/EC-01-2022-0022) | 非结构网格、对称 EA/EbE 与 GPU 拓扑优化 |
| [Schussnig et al. 2025](https://doi.org/10.1016/j.cma.2024.117600) | 非线性固体、高阶 Matrix-Free 与 hp-multigrid |
| [Wei, Liu & Guo, WCCM–ECCOMAS 2026](https://wccm-eccomas2026.org/event/contribution/b0feec06-031e-11f1-919d-000c29ddfc0c), *Problem Independent Machine Learning-Based Fast and High Accuracy Topology Optimization for Large Scale Heat Conduction Structures* | PIML 向大规模传热拓扑优化及内部节点热载荷处理扩展的会议摘要线索；当前仅有官方 contribution 页面，不建立单篇笔记或 BibTeX，待正式会议论文／摘要 PDF 或后续期刊版本 |

## 存储与维护说明

- **唯一入口**：新增文献必须在本页「已入库文献」登记，否则视为未入库；单篇论文只保存一份，交叉属性由 frontmatter tags、research guide 与概念页表达，不建重定向桩页。
- **raw 层**：原始 PDF 的主档平铺在 iCloud `文献库/`（相对 `iCloudDrive`），本地副本放在所属主题的 `sources/` 下（`.gitignore` 排除，不入 Git）。PDF 文件名与译文页 basename 严格对应（`AuthorYear-short-topic.pdf` ↔ `AuthorYear-short-topic-zh.md`），`-zh` 译文以相对路径 `source: "../sources/<同名>.pdf"` 指向它（**不是 citekey**，citekey 另存 `citekey:` 字段）。PDF 是事实源，与译文冲突时以 PDF 为准。
- **raw 的回溯靠文件名，不逐篇登记路径**：iCloud `文献库/` 不分子目录，主档路径由 basename 唯一确定，仓库内重组主题目录时 iCloud 不随之移动。`sources/` 只是供 AI 直接读取的本地副本，丢失后运行仓库根 `restore_sources_from_icloud.ps1`（`-Preview` 只预演）从 `文献库/` 按文件名恢复；脚本按译文页 `source:` 字段定位，无译文页的 PDF 须在 `refs.bib` 条目 `note` 中写明 `本地 PDF <仓库相对路径>`，否则报告为 UNREGISTERED。新入库论文先存入 `文献库/`，再复制到 `sources/`；同名文件不覆盖。出版信息由 DOI（预印本用 arXiv ID + 版本号）经 CrossRef 核验，记录在 `literature/refs.bib`；既有 citekey 保留，新文献 citekey 取 basename。无 DOI、无第三方托管的原件（如基金官方文件）另按 [[../research/funding/sources]] 的「iCloud 相对路径 + SHA-256」方式登记。参考库源码仓库不缓存到本仓库，按 [[fem-libraries/sources]] 的「upstream + WSL 副本」方式登记，版本标在引用点。
- **派生资源**：图片等派生资源统一放 `topopt/assets/`（主题级共用，不下沉到子类），正文按 Obsidian 全库文件名解析引用 `![[名.png]]`，不写相对路径。
- **目录只在有实际内容时建立**：不为候选清单预建空主题目录；`inbox/` 是唯一例外的暂存容器，只放 PDF 副本（`inbox/sources/`，不入 Git）与对应 `refs.bib` 条目，不作为长期落点。
- 只有官方摘要或元数据时，不形成全文级技术结论。

---

*模板：目录索引见 [[../schema/templates/directory-index]]，中文译文见 [[../schema/templates/translation-note]]*
