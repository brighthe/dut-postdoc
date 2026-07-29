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
date_update: 2026-07-29
---

# Matrix-Free 装配层次

> **一句话**：Matrix-Free 不是单一实现，而是由“算子数据保存到哪一层”区分的实现谱系；本库统一采用兼容 libCEED 与 MFEM 的 `FA/TA → LA → EA/EbE → PA/QA → UA/NONE` 五级分类。

本页从已经离散的有限元算子出发，回答“程序预先形成和保存什么”。三维线弹性的
平衡方程、弱形式、向量 Lagrange 离散以及
$\mathbf K_e=\int_{\Omega_e}\mathbf B_e^{\mathsf T}\mathbf D\mathbf B_e\,\mathrm dx$
如何产生，见 [[../linear-elasticity]]。

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

其中 $\mathbf P$ 不只是一个抽象乘号：在 MPI 环境中，它具体涉及单元分区、owned/ghost 或重叠自由度、halo exchange、共享输入一致化、输出归约和全局内积。其数学定义与正确性不变量见 [[distributed-operator-and-shared-dofs]]。

## 五级分类

| 层级 | 本页规范名称 | 主要保存对象 | MatVec 的主要形式 | Matrix-Free 口径 |
|---|---|---|---|---|
| 1 | Full/True Assembly（FA/TA，全局/真自由度全组装） | 全局稀疏矩阵 $\mathbf A$ | 全局稀疏矩阵向量乘 | 不属于 Matrix-Free |
| 2 | Local Assembly（LA，进程局部组装） | 每个 MPI rank 的局部稀疏矩阵 | halo exchange + 局部稀疏矩阵向量乘 | 通常不属于 Matrix-Free |
| 3 | Element Assembly / Element-by-Element（EA/EbE，单元组装） | 稠密单元矩阵 $\mathbf A_e=\mathbf B_e^T\mathbf D_e\mathbf B_e$ | gather → $\mathbf A_e\mathbf x_e$ → scatter-add | 属于广义全局 Matrix-Free |
| 4 | Partial/Quadrature Assembly（PA/QA，部分/积分点组装） | 积分点数据 $\mathbf D_e$ 或等价 PA 数据 | gather → $\mathbf B_e$ → $\mathbf D_e$ → $\mathbf B_e^T$ → scatter-add | 现代高阶有限元的主流 Matrix-Free 路线 |
| 5 | Unassembled / Matrix-Free（UA/MF/NONE，无组装） | 不保存完整 $\mathbf A_e$，也不预存实质性的 $\mathbf D_e$ | 从几何和系数即时计算算子作用 | 严格意义的 fully Matrix-Free |

三个容易混淆的边界是：EA 保存完整单元矩阵；PA 只保存积分点或等价 PA 数据；UA 在每次 apply 时从几何、系数或状态即时计算这些数据。没有全局稀疏矩阵并不自动等于 PA 或 UA。

### 以主算子路径判定

若主算子路径缓存每个单元的完整稠密矩阵 $\mathbf A_e$，但不形成全局稀疏矩阵，则该路径属于 EA/EbE；若主路径只保存积分点数据或等价因子，则应判为 PA/QA；若这些数据在每次 MatVec 中即时生成，则应判为 UA/NONE。为调试或黄金对照另行构造的 FA/TA 算子不改变主路径的分类。分类依据是实际保存对象和 MatVec 数据流，而不是某种语言接口是否只暴露隐式算子调用。

## 装配层次的算子形式

暂不展开 MPI true/local 映射时，令 $\mathbf G_e$ 表示从全局自由度到单元 $e$ 自由度的布尔限制矩阵，$\mathbf A_e$ 表示该单元的局部算子。这里的单元限制矩阵 $\mathbf G_e$ 与 MPI 层从 true DOF 到 rank-local DOF 的限制矩阵 $\mathbf R_r$ 不同；后者见 [[distributed-operator-and-shared-dofs]]。

### FA/TA：全局矩阵作用

FA/TA 在 setup 阶段完成单元贡献的 scatter-add，形成并保存全局稀疏矩阵：

$$
\begin{aligned}
\mathbf A_{\mathrm{FA}}
&=
\sum_e
\mathbf G_e^{\mathsf T}
\mathbf A_e
\mathbf G_e,
\\
\mathbf y_{\mathrm{FA}}
&=
\mathbf A_{\mathrm{FA}}\mathbf x.
\end{aligned}
$$

### EA/EbE：单元矩阵作用

EA/EbE 不形成全局稀疏矩阵，而是保存单元矩阵集合 $\{\mathbf A_e\}$，在每次 MatVec 中直接计算

$$
\mathbf y_{\mathrm{EA}}
=
\sum_e
\mathbf G_e^{\mathsf T}
\left[
\mathbf A_e
\left(\mathbf G_e\mathbf x\right)
\right].
$$

EA 的算子作用可以进一步分解为

$$
\mathbf x_e=\mathbf G_e\mathbf x,
\qquad
\mathbf y_e=\mathbf A_e\mathbf x_e,
\qquad
\mathbf y_{\mathrm{EA}}=\sum_e\mathbf G_e^{\mathsf T}\mathbf y_e.
$$

其中三步依次为 gather、单元矩阵作用和 scatter-add。在精确算术下，EA 与 FA 表示同一个离散算子，即

$$
\mathbf y_{\mathrm{EA}}
=
\mathbf y_{\mathrm{FA}}.
$$

浮点计算中，两条路径可能因组装和求和顺序不同而产生舍入误差量级的数值差异，但这不改变二者的代数等价性。在线弹性问题中，$\mathbf A_e$ 对应单元刚度矩阵 $\mathbf K_e$，$\mathbf A_{\mathrm{FA}}$ 对应全局刚度矩阵 $\mathbf K$。

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

这里还必须把两个正交维度分开：

- **MPI 分布方式**回答网格如何分区、谁拥有 true DOF、ghost 如何更新以及局部贡献如何归约；
- **装配层级**回答每个 rank 为一次算子作用预先保存了全局矩阵、局部矩阵、单元矩阵、积分点数据还是更少的数据。

因此，MPI 可以分别与 FA、LA、EA、PA 或 UA 组合。PETSc `MATSHELL`、Firedrake `mat_type="matfree"` 和 NGSolve `nonassemble=True` 都不能单独说明采用哪种 MPI 分区与共享 DOF 协议。各框架的 owner/ghost 数据流及其与对等重叠副本代数的关系见 [[distributed-operator-and-shared-dofs#13. 与主流有限元框架的对应|分布式框架对应表]]。

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
- [[../linear-elasticity]] — 线弹性连续模型、变分形式、有限元离散与单元刚度算子。
- [[distributed-operator-and-shared-dofs]] — MPI 网格分区、共享自由度同步、加权内积与全局解收集。
- [[method-lineage]] — 郭旭老师团队公开 Matrix-Free 相关成果的方法谱系。
- [[../../research/technical-lines/matrix-free-research-guide]] — 当前基础、目标差距、推进路线与阶段门禁。
- [[../../research/technical-lines/gpu-hpc-research-guide]]
- [[../../research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-high-performance-solver-survey]]
- [[../../work-reports/guo-xu/2026-07-piml-matrix-free-gpu]]
