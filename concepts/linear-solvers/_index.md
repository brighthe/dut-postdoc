---
title: "线性方程组求解器主题入口"
type: index
tags:
  - numerical-algebra
  - linear-solver
  - krylov
  - multigrid
  - preconditioning
status: draft
date_added: 2026-09-03
date_update: 2026-09-04
---

# 线性方程组求解器主题入口

> 本页是大型稀疏方程组 $\mathbf A\mathbf x=\mathbf b$ 求解器体系的统一语义入口：只负责分类树、页面职责和事实所有权说明，不复制各页推导。本目录是 L1 通用基础的目录形态（与 `finite-elements/` 同类），不对应任何 `research/` 研究单元；「求解器」在本目录只指线性方程组求解器，不含非线性 Newton 外层（见 [[../nonlinear-fem]]）与优化器。工程上说「迭代法」默认指预条件 Krylov，定常迭代基本只作为预条件子或多重网格光滑子出现。

## 稳定知识

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[direct-methods]] | LU / Cholesky 稀疏直接法：填充、排序、多右端复用、三维不可行的根源，以及 MUMPS / PARDISO / CPardiso 的并行模型、三阶段接口与 GPU 支持对照 | draft |
| [[stationary-iterations]] | 定常迭代 $\mathbf x_{k+1}=\mathbf G\mathbf x_k+\mathbf c$：分裂格式、谱半径判据与光滑性质 | draft |
| [[krylov-subspace-methods]] | Krylov 子空间投影法：CG / MINRES / GMRES 分族、收敛界、与定常迭代的区别、并行同步点 | draft |
| [[preconditioning]] | 预条件的形式、目标与各类预条件子对矩阵信息的需求 | draft |
| [[multigrid]] | 几何 / 代数多重网格：光滑—限制—粗校正—延拓骨架，作为求解器或预条件子 | draft |

## 求解器分类树与三条判定线

> 本节只提供主题地图；收敛证明、算法细节与实测数字由各页维护。

```text
求解线性方程组 A x = b
├── 直接法：LU / Cholesky 分解 —— MUMPS、CPardiso、PCLU          → [[direct-methods]]
└── 迭代法
    ├── 定常（经典）迭代：Jacobi、Gauss-Seidel、SOR、Richardson  → [[stationary-iterations]]
    ├── Krylov 子空间方法：CG、MINRES、GMRES、BiCGSTAB            → [[krylov-subspace-methods]]
    └── 多重网格：几何 / 代数 MG —— HYPRE BoomerAMG               → [[multigrid]]
```

树上的每一层对应一条判定线：

| 判定线 | 一侧 | 另一侧 |
|---|---|---|
| 是否显式形成 $\mathbf A$ 的分解 | 直接法：形成 $\mathbf L\mathbf U$ 或 $\mathbf L\mathbf L^{\mathsf T}$，一次分解后回代 | 迭代法：只用 $\mathbf A$ 作用于向量的结果 |
| 每步作用的算子是否固定 | 定常迭代：$\mathbf G$ 与 $k$ 无关，收敛率被 $\rho(\mathbf G)$ 锁死 | Krylov：在不断长大的子空间里取最优解，有效算子随 $k$ 变化 |
| 是否跨尺度传递误差 | 单层方法：只在同一网格上迭代 | 多重网格：高频分量在细网格消去，低频分量交给粗网格 |

四类方法不是并列的替代品，而是嵌套的：定常迭代是多重网格的光滑子和最廉价的预条件子，多重网格是 Krylov 最强的预条件子之一，直接法是最粗层求解器和一切迭代法的正确性对照基线。预条件是横跨迭代法三支的公共机制，单独成页 [[preconditioning]]。

### 程序实现必读入口

在任何不显式组装全局矩阵的算子表示之上接 Krylov 求解前，按下表进入相应事实源；本页只提供阅读顺序。

| 入口 | 职责 |
|---|---|
| [[krylov-subspace-methods]] | 方法分族、收敛判据与并行下的内积同步点。 |
| [[preconditioning]] | 每类预条件子需要矩阵的哪一层信息。 |
| [[../matrix-free/assembly-levels#3. 三条跨层级不变量]] | 装配层级约束的是预条件器而不是求解器；主算子与预条件子可取不同层级。 |
| [[../gpu-hpc/distributed-operator-and-shared-dofs#4. 重叠加权内积与 Krylov 求解器收敛理论]] | 共享自由度下 Krylov 内积必须按引用计数加权的定理与实现约定。 |
| [[../gpu-hpc/parallel-levels#3. 两个绕不开的断点]] | scatter-add 与内积两处跨执行实体同步在进程 / 线程 / 设备三层的形态。 |

关联实现：`soptx:src/soptx/fem/solvers/matrix_free_solver.py` — 加权内积与 `weighted_cg` 的落地；实测数值与证据 provenance 由 `soptx:examples/matrix_free_elasticity/results_analysis.md` 唯一维护。

## 项目与技术线入口

| 页面 | 一句话 | 状态 |
|---|---|---|
| [[../../research/piml-matrix-free-gpu/matrix-free-research-guide]] | 精确 Matrix-Free 基线的 Krylov / 预条件闭环要求与开放问题 | in-progress |
| [[../../research/piml-matrix-free-gpu/project-plan]] | 三条技术线组合后的求解器与预条件依赖关系 | in-progress |

## 文献证据

- [[../../literature/matrix-free/translations/Kronbichler2012-parallel-cell-operator-zh]] — 只需算子作用接口的 Krylov 求解与单元级算子按需作用的结合路径；译文 `draft`，当前仅按正式摘要使用证据。
- Saad 2003 *Iterative Methods for Sparse Linear Systems*、Trefethen & Bau 1997、Briggs–Henson–McCormick 2000 是各页共用的教科书来源，`refs.bib` 尚无条目，各页参考文献单独列出。

## 关联入口

- [[../matrix-free/_index]] — 关联主题：Krylov 只需算子作用接口，这一性质是 Matrix-Free 各装配层级的外层求解前提。
- [[../gpu-hpc/_index]] — 关联主题：并行层级与端到端性能模型，内积归约是强扩展的主要拐点。
- [[../linear-elasticity]] — 关联主题：$\mathbf K\mathbf U=\mathbf F$ 的来源与对称正定性的根据。
- [[../nonlinear-fem]] — 关联主题：Newton 步内的切线系统求解，Krylov 方法在非线性下的适用性。
- [[../finite-elements/_index]] — 关联主题：同为 L1 方法体系目录的先例。

## 管理边界

- 本目录只写脱离任何研究线仍然成立的求解器分类、收敛机制与信息需求；本人方案的判断、路线取舍与待验证问题由 `research/` 维护，不在本目录出现「在我研究中的位置」「开放问题」小节。
- 装配层级判据由 `../matrix-free/assembly-levels` 维护，分布式内积加权定理由 `../gpu-hpc/distributed-operator-and-shared-dofs` 维护，三层并行卡点由 `../gpu-hpc/parallel-levels` 维护，本目录只链接不复制。
- 单篇论文事实由 `literature/` 维护，实测数值由对应代码仓库维护。
- 本页不维护固定文件数，也不登记只因索引、日志或顺带讨论而命中关键词的全部文件。
