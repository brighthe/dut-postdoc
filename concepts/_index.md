---
title: "概念页总索引"
type: index
tags:
  - concepts
  - knowledge-base
status: in-progress
date_added: 2026-06-22
date_update: 2026-09-03
---

# 概念页总索引

> 跨多个来源提炼的稳定概念。本目录**按事实的适用范围分层，不按主题分类，也不按页面体量**：判据是「把某条研究线整个删掉，这一页是否仍然成立」——仍然成立的是通用基础，放顶层；只在某个研究单元的问题设定下才有意义的，放对应主题子目录。分层定义、放置顺序与边界见[[#三层结构与放置规则|下方规则]]。简单概念模板：[[../ai/templates/concept-note]]；复杂主题入口模板：[[../ai/templates/topic-index]]。

## 力学与离散基础

被多条技术线共同依赖的连续模型与离散代数，不专属任何一条线，因此保持在 `concepts/` 顶层。

| 概念 | 别名 | 一句话 | 状态 |
|---|---|---|---|
| [[linear-elasticity]] | Linear Elasticity / 位移型线弹性 | 小变形静力各向同性线弹性（二维与三维）的强形式、弱形式与 Lagrange 有限元离散 | in-progress |
| [[external-loads]] | External Loads / 外载荷 / 等效节点力 | 体力、面牵引与集中力的所属对偶空间与载荷泛函有界性、纯 Neumann 相容性、集中力非适定性与特征尺度分布化、一致节点力与 $P_1$ 迹 $L^2$ 投影 | in-progress |
| [[nonlinear-fem]] | Nonlinear FEM / 几何非线性 / 材料非线性 | 放松小变形与线性本构假设后的残量方程与 Newton 求解；几何非线性（Green-Lagrange、几何刚度、共旋格式）与材料非线性（路径相关性、返回映射、内变量）的分野 | draft |
| [[gpu-hpc/distributed-operator-and-shared-dofs]] | Distributed Finite Element Operator / 分布式有限元算子 | MPI 单元分区、共享自由度、输入同步与输出归约、加权 Krylov 内积和全局解收集；第一原理基础 | complete |
| [[gpu-hpc/parallel-levels]] | Parallel Levels / 并行的三个层级 | 进程（MPI）、线程（节点内）、设备内（SIMT）各自切什么、撞什么墙；与装配层级正交的第二坐标轴 | in-progress |
| [[huzhang/huzhang-mixed-fem]] | Hu–Zhang Mixed FEM / 胡张元 / 应力-位移混合有限元 | 应力提升为 H(div) 对称张量主未知量的混合元：Hellinger-Reissner 变分、鞍点系统、顶点应力连续性部分松弛、低次跳量稳定化与收敛阶结果 | in-progress |
| [[substructural-condensation]] | Substructure FEM / 子结构有限元与静力缩聚 | 消除子结构内部节点自由度（Schur 补），将求解降维至接口自由度系统，精确数学等价于全尺度求解 | in-progress |

## 机器学习基础

通用 ML 方法与计算力学中的定位，同样跨线共享。项目自有的 PIML 释义见下方 `piml/` 主题目录。

| 概念 | 别名 | 一句话 | 状态 |
|---|---|---|---|
| [[machine-learning]] | Machine Learning / 机器学习分类框架与通用生命周期 | 以模型族与架构、学习对象、训练信号与任务目标四个正交维度定位 ML 方法，并提供通用生命周期与 5 阶段执行骨架 | in-progress |
| [[ml-roles-and-boundaries]] | 计算力学 ML 6 大路线全景图谱 | 横向比较计算力学中 6 大机器学习路线（Lei2018、FE-CNN、PINN、PIML、本构学习、生成设计）的作用位置与计算角色 | in-progress |
| [[pinn-paradigm]] | Physics-Informed Neural Networks / PINN | 基于自动微分与物理残差 Loss 的无网格求解通用 5 步范式与计算力学 ML 入门映射 | in-progress |

## 主题目录

子目录有两类：对应 `research/` 下项目或课题单元的研究单元目录，以及不专属任何研究线、但已由多个稳定子页构成一个方法体系的 L1 方法体系目录（`finite-elements/`、`linear-solvers/`）。两类的 `_index.md` 都只负责跨目录导航、页面职责和事实所有权说明。

| 主题 | 别名 | 一句话 | 状态 |
|---|---|---|---|
| [[finite-elements/_index\|Finite Elements]] | Finite Elements / 有限元单元体系 | 实体单元（Solid）、板壳单元（Shell）等离散算子构造、抗自锁技术与局部刚度矩阵计算闭环 | in-progress |
| [[linear-solvers/_index|Linear Solvers]] | Linear Solvers / 线性方程组求解器体系 | 直接法、定常迭代、Krylov 与多重网格的分类树与三条判定线、收敛机制、预条件信息需求与并行同步点 | draft |
| [[huzhang/_index\|Hu–Zhang]] | Hu–Zhang Mixed FEM / 胡张元 | 任意次对称应力-位移混合有限元、跳量稳定化、角点松弛与拓扑优化 | in-progress |
| [[density-topopt/_index\|Density Topopt]] | Density-Based Topology Optimization / 变密度法拓扑优化 | 密度法的正则化映射链条（过滤—投影）、材料插值与约束处理基础，独立于具体离散格式 | in-progress |
| [[mmc/_index\|MMC]] | Moving Morphable Components / 移动可变形组件 | 以显式组件参数、拓扑描述函数和优化闭环表示结构拓扑 | in-progress |
| [[piml/_index\|PIML]] | Problem-Independent Machine Learning / 问题无关机器学习 | 维护项目 PIML 的正式释义，并连接 Physics-Informed ML 等外部方法背景 | in-progress |
| [[matrix-free/_index\|Matrix-Free]] | Matrix-Free Assembly Levels / 矩阵无关有限元 | 统一装配层次、方法谱系与当前技术路线 | in-progress |
| [[gpu-hpc/_index\|GPU/HPC]] | GPU / High-Performance Computing / 异构高性能计算 | 统一异构执行模式分类、并行层级坐标、端到端性能模型与当前异构并行技术路线 | in-progress |

## 知识库自身

| 概念 | 别名 | 一句话 | 状态 |
|---|---|---|---|
| [[llm-wiki]] | LLM Wiki / 个人 AI 知识库 | 把 LLM 放在原始资料与研究者之间，持续维护可追溯、互链的 Markdown wiki | done |

---

## 三层结构与放置规则

| 层 | 位置 | 判据 | 例 |
|---|---|---|---|
| L1 通用基础 | `concepts/` 顶层；已形成多个稳定子页的方法体系可建 L1 方法体系目录 | 在任何一条研究线之外仍然成立；经典方法与通用离散代数 | [[linear-elasticity]]、[[nonlinear-fem]]、[[machine-learning]]、[[linear-solvers/_index]] |
| L2 研究单元专属 | `concepts/<主题>/` | 只在某个 `research/` 单元的问题设定下有意义；该单元消失则本页失去对象 | [[gpu-hpc/distributed-operator-and-shared-dofs]]、[[matrix-free/assembly-levels]] |
| L3 外部实现对象 | `<主题>/reference-libraries/` | 描述的是某个具体软件而非方法本身 | [[gpu-hpc/reference-libraries/mfem-architecture]] |

新建页面按以下顺序判定位置：

1. 内容是当前状态、进度、单篇论文事实还是阶段表达？→ 不进本目录，分别归 `research/`、`literature/`、`entities/`。
2. 描述的是某个具体软件？→ L3。
3. 删掉相关研究线后是否仍成立？成立 → L1；不成立 → L2。
4. 第 3 步确实两可 → 默认 L2；等第二条研究线依赖它时再上提到 L1，并同步改写其自身出链与全部入链。

## 管理边界

- 本目录只收稳定概念。当前任务状态、实施阶段与预计日期由 `research/` 维护，单篇论文事实由 `literature/` 维护，面向导师与合作者的阶段表达由 `entities/` 维护，已完成事件的历史材料由 `archive/` 维护。
- 分层依据是事实的适用范围，不是页面体量。L1 页面不因行数增长而下沉到子目录，L2 页面也不因篇幅短小而上提。
- L1 单页不因篇幅下沉到子目录。只有当一个通用方法体系已形成多个各自独立成立的稳定子页时，才建立 L1 方法体系目录（如 `finite-elements/`、`linear-solvers/`），由其 `_index.md` 承担该体系的分组导航；目录名只能是方法体系名，不得写成研究线归属。顶层单页的分组导航仍由本页表格承担。
- 研究单元目录一一对应 `research/` 下的项目或课题单元，不存在对应研究单元时不新建；L1 方法体系目录按上一条判据建立。
- 子目录内不强求统一的页面集。`method-lineage`、`mathematical-foundations`、`reference-libraries/` 按该研究单元是否有对应对象决定有无，缺失不视为缺陷，不为形式整齐而补建。
- 页面间链接一律使用相对于当前文件的路径，不用 vault 根路径或跨目录裸文件名；写作约定见 [[../ai/llm-wiki-workflow#写作约定]]。移动页面时必须同步改写其自身出链与全部入链。
- 本页不维护固定文件数，只登记概念页与主题入口。

---

*新建简单概念页时复制 [[../ai/templates/concept-note]]；对应的研究单元成立、且已形成多个需要说明关系与边界的页面后，复制 [[../ai/templates/topic-index]] 建立语义 `_index.md`，删除没有实际内容的可选章节，并在本表和 [[../index]] 登记主题入口。*
