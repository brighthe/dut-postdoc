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
date_update: 2026-07-21
---

# Matrix-Free 装配层次

> **一句话**：Matrix-Free 不是单一实现，而是由“算子数据保存到哪一层”区分的实现谱系；本库统一采用兼容 libCEED 与 MFEM 的 `FA/TA → LA → EA/EbE → PA/QA → UA/NONE` 五级分类。

## 定义与适用边界

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

其中：

- $\mathbf P$ 处理并行 true DOF 与进程局部 DOF 的映射；
- $\mathbf G$ 处理进程局部 DOF 与单元 DOF 的限制和回填；
- $\mathbf B$ 将单元自由度插值或微分到积分点；
- $\mathbf D$ 表示积分权重、几何 Jacobian、材料系数和积分点物理核；
- $\mathbf A$ 是最终全局算子。

“装配层次”描述上述因子中哪些乘积被提前计算和保存。不同软件的枚举名称并不完全相同，因此本页是一套跨框架统一术语，不宣称所有文献都固定采用同一套五级命名。

## 五级分类

| 层级 | 本页规范名称 | 主要保存对象 | MatVec 的主要形式 | Matrix-Free 口径 |
|---|---|---|---|---|
| 1 | Full/True Assembly（FA/TA，全局/真自由度全组装） | 全局稀疏矩阵 $\mathbf A$ | 全局稀疏矩阵向量乘 | 不属于 Matrix-Free |
| 2 | Local Assembly（LA，进程局部组装） | 每个 MPI rank 的局部稀疏矩阵 | halo exchange + 局部稀疏矩阵向量乘 | 通常不属于 Matrix-Free |
| 3 | Element Assembly / Element-by-Element（EA/EbE，单元组装） | 稠密单元矩阵 $\mathbf A_e=\mathbf B_e^T\mathbf D_e\mathbf B_e$ | gather → $\mathbf A_e\mathbf x_e$ → scatter-add | 属于广义全局 Matrix-Free |
| 4 | Partial/Quadrature Assembly（PA/QA，部分/积分点组装） | 积分点数据 $\mathbf D_e$ 或等价 PA 数据 | gather → $\mathbf B_e$ → $\mathbf D_e$ → $\mathbf B_e^T$ → scatter-add | 现代高阶有限元的主流 Matrix-Free 路线 |
| 5 | Unassembled / Matrix-Free（UA/MF/NONE，无组装） | 不保存完整 $\mathbf A_e$，也不预存实质性的 $\mathbf D_e$ | 从几何和系数即时计算算子作用 | 严格意义的 fully Matrix-Free |

### FA/TA：全局矩阵

显式形成并保存 $\mathbf A$。它便于使用成熟的稀疏直接法、AMG、ILU 等矩阵型求解器和预条件器，但全局存储与内存带宽成本最高。

### LA：进程局部矩阵

每个 MPI rank 保存本地稀疏矩阵，通过通信完成全局作用。它没有在单个进程保存完整的全局矩阵，但核心计算仍是稀疏矩阵向量乘，因此不能仅凭“分布式”称为 Matrix-Free。

### EA/EbE：单元矩阵

不组装全局稀疏矩阵，但保存每个单元的完整 $\mathbf A_e$：

$$
\mathbf y
=
\sum_e
\mathbf G_e^T
\mathbf A_e
\mathbf G_e\mathbf x.
$$

它也常被称为 element-by-element、local-matrix Matrix-Free 或 global Matrix-Free。判断关键是“仍保存完整单元矩阵”，因此 EA/EbE 不应写成 PA。

### PA/QA：积分点数据

不保存 $\mathbf A$ 或完整 $\mathbf A_e$，仅预计算积分点上的 $\mathbf D_e$ 或等价 PA 数据：

$$
\mathbf y
=
\sum_e
\mathbf G_e^T
\mathbf B_e^T
\mathbf D_e
\mathbf B_e
\mathbf G_e\mathbf x.
$$

$\mathbf B_e$ 和 $\mathbf B_e^T$ 在 apply 阶段执行；对张量积高阶单元通常结合 sum factorization。PA 通过增加部分重复计算换取更低的数据存储和访存量。

### UA/NONE：完全无组装

除必要的网格、系数或状态外，不保存完整单元矩阵和实质性的积分点算子数据；$\mathbf D_e$ 在每次 apply 时按需计算。它的更新成本最低，但可能比 PA 产生更多重复计算。

## 框架术语映射

| 本页层级 | libCEED | MFEM |
|---|---|---|
| FA/TA | TA/A | FULL；LEGACY 也是全组装路径 |
| LA | LA | 没有完全对应的独立 `AssemblyLevel` |
| EA/EbE | EA | ELEMENT |
| PA/QA | QA/PA | PARTIAL |
| UA/MF | UA/U | NONE |

因此，“五级分类”适合作为跨框架比较坐标；具体实现仍应同时注明所用框架及其原生命名。

## 快速识别流程

按以下顺序判断一个实现的装配层次：

1. 是否保存全局或 true-DOF 稀疏矩阵？是则为 FA/TA。
2. 是否仅在每个 MPI rank 保存局部稀疏矩阵？是则为 LA。
3. 是否为每个单元保存完整稠密矩阵 $\mathbf A_e$？是则为 EA/EbE。
4. 是否只保存积分点 $\mathbf D_e$ 或等价 PA 数据？是则为 PA/QA。
5. $\mathbf D_e$ 是否在每次 MatVec 中从几何、系数或当前状态即时计算？是则为 UA/NONE。

不能根据“代码提供 `operator.apply()`”“使用 PETSc `MatShell`”或“没有全局 CSR”单独判定装配层次；这些事实只说明上层使用算子接口。

## 算子与预条件器可以采用不同层级

Matrix-Free 通常只描述主算子路径。实际求解器可以采用混合方案，例如：

- 主算子使用 PA，预条件器组装对角线、块对角或低阶稀疏代理；
- 主算子使用 UA，预条件器使用 EA 或 LA；
- PETSc `MatShell` 封装 PA/UA 算子，同时使用单独的 assembled preconditioning matrix；
- 优化迭代中复用预条件层次，而只更新 PA/UA 的局部系数。

因此，报告性能时必须分别写明 operator level、preconditioner level、setup/update 成本和 apply 成本。

## 当前项目映射

| 事实源 | 当前定位 | 判断依据与边界 |
|---|---|---|
| `mfleo` 的 `develop` 分支 | PA/QA | 基于 MFEM Partial Assembly 接口，以 C++/CUDA kernel 执行算子作用；保存 PA setup 数据，不保存完整全局矩阵或完整单元矩阵 |
| `xihe/develop/examples/matrix_free_3` | EA/EbE | FEALPy integrator 的 `.const(pspace)` 先形成并保存单元局部张量，MatVec 时执行单元 gather、局部张量作用、scatter-add 和 MPI 同步，不组装全局稀疏矩阵 |
| 当前积分点 contraction 原型 | PA 或 UA 待核实 | 已确认不形成全局 $\mathbf K$ 和单元 $\mathbf K_e$；仍需核对 $\mathbf D_e$ 是否预存，不能仅凭 contraction 形式强行归类 |
| PETSc Shell Matrix 集成 | 接口层，不是装配层级 | `MatShell` 可以包装 EA、PA、UA 或其他自定义数据结构，必须继续检查其内部存储和 apply 实现 |

公司仓库只作为事实源；本页仅记录可复用的非敏感技术结论，不复制代码、内部数据或客户算例。

## Benchmark 应统一记录的字段

| 维度 | 建议字段 |
|---|---|
| 装配层级 | operator level、preconditioner level、实际保存对象 |
| 正确性 | 与 FA 参考解的 MatVec 误差、能量误差、真残差 |
| 存储 | bytes/DoF、峰值内存、矩阵/单元/积分点/预条件数据分项 |
| 计算 | setup、update、operator apply、preconditioner apply、完整 solve |
| 收敛 | Krylov 类型、迭代数、残差历史、停止准则 |
| 可扩展性 | 问题规模、MPI ranks、GPU 数、强/弱扩展效率 |

## 来源与证据

- [MFEM: Use partial assembly and matrix-free assembly](https://mfem.org/howto/assembly_levels/) — `FULL/ELEMENT/PARTIAL/NONE` 的官方定义。
- [MFEM: Performance and Partial Assembly](https://mfem.org/performance/) — PA 的 $\mathbf B^T\mathbf D\mathbf B$ 分解、积分点存储与 GPU 性能背景。
- [libCEED: Interface Concepts](https://libceed.org/en/latest/libCEEDapi/) — `TA/LA/EA/QA/UA` 的跨层存储分类。
- [PETSc: MATSHELL](https://petsc.org/main/manualpages/Mat/MATSHELL/) — Shell Matrix 是用户自定义数据结构和 MatVec 的接口。
- [FEALPy: integrator.py](https://github.com/weihuayi/fealpy/blob/master/fealpy/fem/integrator.py) — `Integrator.const(space)` 形成并保留局部积分张量的接口语义。
- `mfleo`、`xihe` 的 `origin/develop` — 当前项目映射的只读事实源。

## 在我研究中的位置

- 为 [[../research/technical-lines/matrix-free-research-guide]] 提供统一的装配层级术语和 Benchmark 字段。
- 为 PIML 局部算子接入、预条件代理和 GPU 数据布局选择提供存储—计算—更新成本坐标。
- 防止把“没有全局稀疏矩阵”“使用 Shell Matrix”“PA”和“fully Matrix-Free”混写成同一概念。

## 开放问题

1. 当前积分点 contraction 原型是否缓存 $\mathbf D_e$，应归为 PA 还是 UA？
2. PIML 预测的局部 $\widehat{\mathbf K}_s$ 若作为完整局部矩阵保存，应归入 EA，还是需要设计积分点/低秩表示进入 PA/UA？
3. 不同装配层级与低阶代理、AMG、Schwarz 等预条件器的最优组合如何随阶次、网格和硬件变化？

## 相关页面

- [[../research/technical-lines/matrix-free-research-guide]]
- [[../research/technical-lines/gpu-hpc-research-guide]]
- [[../research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-high-performance-solver-survey]]
- [[../work-reports/guo-xu/2026-07-piml-matrix-free-gpu]]
