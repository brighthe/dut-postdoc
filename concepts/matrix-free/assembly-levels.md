---
title: "Matrix-Free 装配层次"
type: concept
aliases:
  - Matrix-Free Assembly Levels
  - Operator Assembly Levels
  - FA/LA/EA/PA/UA
tags:
  - matrix-free
  - finite-element
  - assembly
  - partial-assembly
  - operator
status: in-progress
date_added: 2026-07-21
date_update: 2026-07-26
---

# Matrix-Free 装配层次

> **一句话**：Matrix-Free 不是单一实现，而是由“算子数据保存到哪一层”区分的实现谱系；本库统一采用兼容 libCEED 与 MFEM 的 `FA/TA → LA → EA/EbE → PA/QA → UA/NONE` 五级分类。

## 统一算子表示

有限元离散算子可抽象为

$$
\mathbf A
=
\mathbf P^T
\mathbf G^T
\mathbf B^T
\mathbf D
\mathbf B
\mathbf G
\mathbf P,
$$

- $\mathbf P$：并行 true DOF 与进程局部 DOF 的映射；
- $\mathbf G$：进程局部 DOF 与单元 DOF 的限制和回填；
- $\mathbf B$：单元自由度到积分点的插值或微分；
- $\mathbf D$：积分权重、几何 Jacobian、材料系数和积分点物理核。

一次典型算子作用可读作 `true DOF → local/element DOF → quadrature data → element/local DOF → true DOF`。“装配层次”描述上述因子中哪些乘积被提前计算并保存；不同软件的原生命名并不完全相同。

## 五级分类

| 层级 | 本页规范名称 | 主要保存对象 | MatVec 的主要形式 | Matrix-Free 口径 |
|---|---|---|---|---|
| 1 | Full/True Assembly（FA/TA，全局/真自由度全组装） | 全局稀疏矩阵 $\mathbf A$ | 全局稀疏矩阵向量乘 | 不属于 Matrix-Free |
| 2 | Local Assembly（LA，进程局部组装） | 每个 MPI rank 的局部稀疏矩阵 | halo exchange + 局部稀疏矩阵向量乘 | 通常不属于 Matrix-Free |
| 3 | Element Assembly / Element-by-Element（EA/EbE，单元组装） | 稠密单元矩阵 $\mathbf A_e=\mathbf B_e^T\mathbf D_e\mathbf B_e$ | gather → $\mathbf A_e\mathbf x_e$ → scatter-add | 属于广义全局 Matrix-Free |
| 4 | Partial/Quadrature Assembly（PA/QA，部分/积分点组装） | 积分点数据 $\mathbf D_e$ 或等价 PA 数据 | gather → $\mathbf B_e$ → $\mathbf D_e$ → $\mathbf B_e^T$ → scatter-add | 现代高阶有限元的主流 Matrix-Free 路线 |
| 5 | Unassembled / Matrix-Free（UA/MF/NONE，无组装） | 不保存完整 $\mathbf A_e$，也不预存实质性的 $\mathbf D_e$ | 从几何和系数即时计算算子作用 | 严格意义的 fully Matrix-Free |

三个容易混淆的边界是：EA 保存完整单元矩阵；PA 只保存积分点或等价 PA 数据；UA 在每次 apply 时从几何、系数或状态即时计算这些数据。没有全局稀疏矩阵并不自动等于 PA 或 UA。

## 框架术语映射

| 框架 | Matrix-Free 入口 | 在五级分类中的理解 |
|---|---|---|
| [libCEED](https://libceed.org/en/latest/libCEEDapi/) | `TA/LA/EA/QA/UA` | 五级分类的主要术语来源 |
| [MFEM](https://mfem.org/howto/assembly_levels/) | `FULL/ELEMENT/PARTIAL/NONE` | 分别对应 FA/EA/PA/UA；LA 没有完全对应的独立 `AssemblyLevel` |
| [deal.II](https://dealii.org/developer/doxygen/deal.II/classFEEvaluation.html) | `MatrixFree`、`FEEvaluation` | 提供高阶 Matrix-Free 算子作用；应按实际缓存对象继续判断 PA 或 UA |
| [PETSc](https://petsc.org/main/manualpages/Mat/MATSHELL/) | `MATSHELL` | 通用 Shell Operator 接口，不代表具体装配层级 |
| [Firedrake](https://www.firedrakeproject.org/matrix-free.html) | `mat_type="matfree"`、`ImplicitMatrix` | 提供隐式算子作用；仍需检查底层保存对象和执行路径 |
| [DOLFINx](https://docs.fenicsproject.org/dolfinx/main/python/demos/demo_matrix-free-petsc.html) | PETSc `SHELL` | 可构造不形成 `MATAIJ` 的算子作用，但 Shell 本身不是装配层级 |
| [NGSolve](https://docu.ngsolve.org/latest/i-tutorials/unit-3.5.1-dgapply/dgapply-scalar.html) | `nonassemble=True` | 支持不组装稀疏矩阵的算子作用；仍需根据实际保存对象分类 |

“五级分类”只作为跨框架比较坐标，具体实现仍应注明框架、原生入口和实际保存对象。`MATSHELL`、`ImplicitMatrix`、`nonassemble=True` 或自定义 `operator.apply()` 只能证明采用了隐式算子接口，不能单独决定其属于 EA、PA 还是 UA。

## 快速识别流程

按以下顺序判断一个实现的装配层次：

1. 是否保存全局或 true-DOF 稀疏矩阵？是则为 FA/TA。
2. 是否仅在每个 MPI rank 保存局部稀疏矩阵？是则为 LA。
3. 是否为每个单元保存完整稠密矩阵 $\mathbf A_e$？是则为 EA/EbE。
4. 是否只保存积分点 $\mathbf D_e$ 或等价 PA 数据？是则为 PA/QA。
5. $\mathbf D_e$ 是否在每次 MatVec 中从几何、系数或当前状态即时计算？是则为 UA/NONE。

## 算子与预条件器可以采用不同层级

Matrix-Free 通常只描述主算子路径，预条件器可以使用另一装配层级。例如，主算子使用 PA，预条件器可以使用对角、块对角或低阶组装代理。因此，性能报告必须分别注明 operator level、preconditioner level，以及 setup、update、apply 和完整 solve 成本。

## 易混淆案例：Ma2026

[[../../literature/topology-opt/Ma2026-highperformanceparallel]] 将多尺度形函数 $\mathbf N^j$ 按需预测、用于形成子结构缩聚刚度后释放，并在粗网格求解后再次预测。这减少了辅助数据的持久存储，但子结构缩聚刚度仍显式形成，粗网格全局缩聚矩阵仍然组装。

因此，Ma2026 的全局缩聚求解按本页五级分类属于第 1 级 FA/TA；论文中的 `matrix-free` 是对辅助数据采用按需重计算的存储优化，不属于第 3—5 级的算子级 Matrix-Free。完整方法边界和后续团队成果更新见 [[method-lineage]]。

## 来源与证据

- [MFEM: Use partial assembly and matrix-free assembly](https://mfem.org/howto/assembly_levels/) — `FULL/ELEMENT/PARTIAL/NONE` 的官方定义。
- [MFEM: Performance and Partial Assembly](https://mfem.org/performance/) — PA 的 $\mathbf B^T\mathbf D\mathbf B$ 分解、积分点存储与 GPU 性能背景。
- [libCEED: Interface Concepts](https://libceed.org/en/latest/libCEEDapi/) — `TA/LA/EA/QA/UA` 的跨层存储分类。
- [PETSc: MATSHELL](https://petsc.org/main/manualpages/Mat/MATSHELL/) — Shell Matrix 是用户自定义数据结构和 MatVec 的接口。

## 相关页面

- [[_index]] — Matrix-Free 稳定方法理解的子知识库入口。
- [[method-lineage]] — 郭旭老师团队公开 Matrix-Free 相关成果的方法谱系。
- [[../../research/technical-lines/matrix-free-research-guide]] — 当前基础、目标差距、推进路线与阶段门禁。
- [[../../research/technical-lines/gpu-hpc-research-guide]]
- [[../../research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-high-performance-solver-survey]]
- [[../../work-reports/guo-xu/2026-07-piml-matrix-free-gpu]]
