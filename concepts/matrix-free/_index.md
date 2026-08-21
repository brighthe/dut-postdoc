---
title: "Matrix-Free 主题入口"
type: index
tags:
  - matrix-free
  - finite-element
status: in-progress
date_added: 2026-07-26
date_update: 2026-08-10
---

# Matrix-Free 主题入口

> 本页连接 Matrix-Free 的稳定知识、文献证据和当前研究。**Matrix-Free 不是二值属性，而是由「算子数据保存到哪一层」区分的实现谱系**；本主题统一采用 [[assembly-levels]] 的 `FA/TA → LA → EA/EbE → PA/QA → UA/NONE` 五级口径，「没有全局稀疏矩阵」不自动等于 PA 或 UA。判定依据是主算子路径的实际保存对象与 MatVec 数据流，不是某种接口是否只暴露隐式算子调用。主题名同样不代表团队已有算子级 Matrix-Free 成果：当前正式时间线只有 Ma2026 一个节点，其全局缩聚求解按五级分类属于第 1 级 FA/TA，论文中的 `matrix-free` 指辅助数据的按需重计算；纳入标准与公开成果谱系见 [[method-lineage]]。

## 稳定知识

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[assembly-levels]] | Matrix-Free 五级装配层次、跨框架术语和判定边界 | in-progress |
| [[krylov-subspace-methods]] | Krylov 子空间方法在 Matrix-Free 模式下的求解机制、预条件与 GPU 异构特性 | draft |
| [[method-lineage]] | 郭旭老师团队公开 Matrix-Free 相关成果的方法谱系；当前直接节点为 Ma2026 | draft |

## Matrix-Free 算子作用与装配层次

> 本节只提供主题地图；不复制统一算子表示的推导、五级分类判据、通信协议或程序实测数字。

```text
x (T-vector, true DOF)
  --P--> L (进程局部 DOF) --G--> E (单元 DOF) --B--> Q (积分点)
  --D--> Q
  --B^T--> E --G^T--> L --P^T--> y (T-vector)
```

装配层次就是在这条因子链上选一个**预计算前缘**：前缘以外的因子在 setup 阶段乘起来并保存，前缘以内的留到每次 apply 执行。五级分类没有引入新算子，只是同一条链的不同求值方式。四个因子的定义、$\mathbf P$ 与 $\mathbf G$ 的层次区分、五级判据与存储代价对照，全部由 [[assembly-levels]] 维护。

### 程序实现必读入口

启动或讨论 SOPTX 中的 Matrix-Free 程序实现前，按下表进入相应的数学、工程与代码事实源；本页只提供阅读顺序和职责路由。

| 入口 | 职责 |
|---|---|
| [[assembly-levels]] | 五级分类判据、预计算前缘、跨层级不变量与跨框架术语映射；判定一份实现属于哪一级的唯一依据。 |
| [[../gpu-hpc/distributed-operator-and-shared-dofs]] | 因子链中 $\mathbf P$ 这一层的数学事实源：单元分区、共享自由度、同步归约与加权内积的正确性不变量。 |
| [[krylov-subspace-methods]] | MatVec 之上的迭代求解机制、预条件与收敛判据。 |
| [[../../research/technical-lines/matrix-free-research-guide]] | 研究目标、装配边界、统一验收原则与阶段门禁。 |

关联实现：`soptx:examples/matrix_free_elasticity/`，维护当前二维、三维可执行线弹性基线；具体入口与运行方式见该目录 `README.md`，实测数值与证据 provenance 的唯一事实源是同目录 `results_analysis.md`，当前只有 dirty worktree 的开发证据，尚无 clean-revision 正式 evidence。

## 项目与技术线入口

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[../../research/technical-lines/matrix-free-research-guide]] | 长期目标、能力边界、阶段模型、统一验收原则与当前任务状态 | in-progress |
| [[../../research/piml-matrix-free-gpu/_index]] | 以 GPU 加速 Matrix-Free 求解为核心内容之一的博士后核心研究项目入口 | in-progress |
| [[../../research/piml-matrix-free-gpu/high-performance-solver-survey]] | 三条技术线组合后的方法关系、开放问题与研究切入点 | in-progress |

## 文献证据

- [[../../literature/matrix-free/_index]] — 以 Matrix-Free 方法为主要贡献的实际文献、译文与交叉主题入口。
- [[../../literature/matrix-free/notes/Kronbichler2012-parallel-cell-operator]] — 并行 cell-based 有限元算子应用的 `draft` 骨架；当前仅按正式摘要使用证据，中文译文待完成。
- [[../../literature/_index#当前 ingest 队列]] — 尚未建立单篇笔记的 Matrix-Free 论文和储备候选入口。
- [[../../literature/topology-opt/notes/Ma2026-highperformanceparallel]] — 当前唯一经证实、明确使用 `matrix-free` 表述的团队论文。

## 关联入口

- 关联主题：[[../gpu-hpc/distributed-operator-and-shared-dofs]] — MPI 单元分区、共享自由度、同步归约与分布式 MatVec 的统一数学描述。该页对全部装配层级成立（FA/LA 的 MPI 求解同样需要），属跨技术线的通用基础，与 `concepts/gpu-hpc/` 下的系统解耦框架协同组成分布式体系。
- 关联主题：[[../linear-elasticity]] — 当前三维参考问题的连续模型、变分形式和有限元离散基础。
- 关联主题：[[../gpu-hpc/reference-libraries/mfem-architecture]] — [[assembly-levels]] 五级分类的术语来源之一；该页作为软件对象由 `gpu-hpc/reference-libraries/` 唯一维护。
- 关联主题：[[../piml/_index]] — PIML 稳定知识、方法谱系与当前研究入口。
- 关联主题：[[../gpu-hpc/_index]] — GPU/HPC 端到端性能模型、公开成果谱系与当前研究入口。
- 工作汇报：[[../../discussions/guo-xu/first-formal-work-report]] — 面向郭旭老师的第一次正式工作汇报，保存本次实际要汇报的 Matrix-Free 阶段结果、事实边界和待请教问题；它是阶段表达快照，不是内部任务状态、程序实现或数值 evidence 的事实源。
- 历史档案：[[../../archive/2026-postdoc-entry-assessment/README]] — 2026 年博士后入站考核答辩的历史材料总览，其中包含当时的 Matrix-Free 计划、图件和表达；档案不再维护当前研究事实，不在本页逐一列出内部文件。

## 管理边界

- 装配层次推导与判定判据由 [[assembly-levels]] 维护，分布式通信协议与正确性不变量由 [[../gpu-hpc/distributed-operator-and-shared-dofs]] 维护，单篇论文事实由 `literature/` 维护，实测数值由 SOPTX 的 `results_analysis.md` 维护。
- 不在概念页维护当前任务状态、实施阶段或预计交付日期；这些只由 [[../../research/technical-lines/matrix-free-research-guide#五、阶段门禁与当前执行状态]] 维护。
- 工作汇报只保存阶段表达，历史档案只保存历史语境；二者都不反向覆盖概念定义、当前任务状态和工程 evidence。
- 不把 PIML 前序论文直接标为 Matrix-Free 成果，也不把尚未公开的设想写成团队既有路线。
- 新成果只有在论文、预印本、专利或公开软件等来源可核实时，才进入正式时间线。
- 本页按职责列出 Matrix-Free 的权威入口，不维护容易过期的文件总数，也不登记只因索引、日志、参考文献或顺带讨论而命中关键词的全部文件。
