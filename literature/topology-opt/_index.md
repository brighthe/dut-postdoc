---
title: "拓扑优化文献入口"
type: index
tags:
  - literature
  - topology-opt
status: in-progress
date_added: 2026-07-31
date_update: 2026-08-04
---

# 拓扑优化文献入口

> 本页是拓扑优化文献主题入口。以拓扑优化、结构分析与设计优化为主要研究问题的单篇论文事实保存在 `notes/`，中文译文保存在 `translations/`，图片等派生资源保存在 `assets/`；论文涉及的 PIML、Matrix-Free、GPU/HPC 等交叉属性通过 `tags` 和其他主题索引表达，不重复存储笔记。

## PIML 与机器学习

| 文献 | 主要定位 | 交叉主题 | 状态 |
|---|---|---|---|
| [[notes/Lei2018-machinelearningdriven]] | MMC 框架下的机器学习驱动拓扑优化 | machine-learning, MMC | done |
| [[notes/Huang2022-problemindependentmachine]] | Problem-Independent PIML 拓扑优化 | PIML, EMsFEM | read |
| [[notes/Huang2023-PIML-substructure]] | PIML 增强子结构分析与拓扑优化 | PIML, substructure | read |
| [[notes/Huang2024-PIML-datafree]] | Mechanics-based data-free PIML | PIML, mechanics-based-loss | done |
| [[notes/Zhang2024-isoparametric-PIML]] | 面向复杂设计域的等参单元 PIML；[[translations/Zhang2024-isoparametric-PIML-zh\|中文译文]]待完成 | PIML, isoparametric-elements, complex-domain | draft |
| [[notes/Xu2025-PIML-lattice-MMC]] | PIML、MMC 与分区坐标映射结合的三维梯度点阵复合结构优化；[[translations/Xu2025-PIML-lattice-MMC-zh\|中文译文]]待完成 | PIML, MMC, graded-lattice | draft |
| [[notes/Guo2026-highgeneralization-bezier]] | 三次 Bézier 边界位移插值与 DeepONet 增强的高泛化子结构分析；[[translations/Guo2026-highgeneralization-bezier-zh\|中文译文]]待完成 | PIML, DeepONet, substructure | draft |
| [[notes/Guo2026-PIML-OFEM]] | 基于超采样数值基函数、重叠有限元和 U-Net 的 PIML-OFEM；[[translations/Guo2026-PIML-OFEM-zh\|中文译文]]待完成 | PIML, overlapping-FEM, preprint | draft |
| [[notes/Ma2026-highperformanceparallel]] | 大规模并行 PIML 拓扑优化 | PIML, matrix-free, parallel-computing | done |

### Physics-Informed 拓扑优化候选

[Jeong et al. 2023, PINNTO](https://doi.org/10.1016/j.engstruct.2022.115484) 学习特定设计状态下的解场，与 Huang–Ma 路线学习可复用局部力学表示的对象不同。其 `to-ingest` 状态只在 [[../_index#当前 ingest 队列|文献总索引]]维护，统一比较见 [[../../research/technical-lines/piml-research-guide#三、国内外研究现状、研究缺口与选题价值]]。

## MMC / MMV

| 文献 | 主要定位 | 状态 |
|---|---|---|
| [[notes/Zhang2016-MMC-topology]] | MMC 与 ersatz material 模型 | draft |
| [[notes/Zhang2016-minimum-length-scale]] | MMC 最小尺度控制 | draft |
| [[notes/Zhang2017-MMV-3D]] | 三维 MMV 显式拓扑优化 | done |

## Matrix-Free / GPU 交叉应用

Matrix-Free 与 GPU/HPC 的核心证据、算子边界和外推限制分别由 [[../../research/technical-lines/matrix-free-research-guide#四、证据锚点及结论边界]]、[[../../research/technical-lines/gpu-hpc-research-guide#四、证据锚点及结论边界]] 综合；当前 ingest 队列与储备候选池由 [[../_index]] 统一维护。候选论文完成 ingest 后，再按主要问题和实际内容规模确定物理落点。

| 文献 | 主要定位 | 状态 |
|---|---|---|
| [[notes/Traff2023-GPU-topology-optimisation]] | 单 GPU 三维拓扑优化的摘要／元数据级证据；[[translations/Traff2023-GPU-topology-optimisation-zh\|中文译文]]与精读待完成 | draft |
| [[notes/Zhou2025-efficientaccelerationstrategies]] | 文献笔记与[[translations/Zhou2025-efficientaccelerationstrategies-zh\|中文译文]]骨架；正文待逐节翻译与精读 | draft |
| [[notes/Ma2026-highperformanceparallel]] | PIML、CPU/MPI、多重网格与按需预测／释放；全局粗矩阵仍组装 | done |

本表登记已经建立单篇笔记的交叉论文，并同步其最近一级状态；它表示当前知识库状态，不表示公开研究中只有这些相关论文。

## 交叉主题入口

- [[../../research/technical-lines/matrix-free-research-guide]] — Matrix-Free 方法证据及其在拓扑优化中的应用边界。
- [[../../research/technical-lines/piml-research-guide]] — Physics-Informed ML、PINN、neural operator 与结构保持学习的证据综合。
- [[../_index]] — 当前 ingest 队列与储备候选池。
- [[../../concepts/piml/_index]] — PIML 稳定知识与方法谱系。
- [[../../concepts/matrix-free/_index]] — Matrix-Free 装配层次、方法边界与研究入口。
- [[../../concepts/gpu-hpc/_index]] — GPU/HPC 性能口径、研究现状支撑与当前技术线入口。

## 归类规则

- 单篇笔记只保存一份，按论文的主要研究问题或主要贡献确定物理目录。
- `notes/` 是纯文件容器，不建立 `_index.md`、README 或第二套状态账；论文状态以单篇笔记 frontmatter 为权威来源，本页只维护最近一级同步。
- `Zhou 2025` 的主问题是三维拓扑优化，因此保存在本主题的 `notes/`；其 Matrix-Free 属性由 `tags`、technical-line guide 和概念页共同索引。
- `Ma2026` 的主问题是大规模拓扑优化，因此保存在本主题的 `notes/`；其 Matrix-Free 属性由 `tags`、technical-line guide 和概念页共同索引。
