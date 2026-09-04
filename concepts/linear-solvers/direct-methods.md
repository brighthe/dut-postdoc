---
title: "稀疏直接法"
type: concept
aliases:
  - Direct Methods
  - Sparse Direct Solvers
  - LU 分解
  - Cholesky 分解
  - 稀疏直接求解器
tags:
  - numerical-algebra
  - linear-solver
  - direct-method
status: draft
date_added: 2026-09-03
date_update: 2026-09-04
---

# 稀疏直接法

> 直接法把 $\mathbf A$ 分解为三角因子后回代求解，结果只受舍入误差影响，不依赖谱分布；代价是分解过程的填充（fill-in）使三维问题的内存与运算量随自由度数超线性增长，这是大规模三维有限元问题不能依赖直接法的根本原因。它在迭代法体系中保留两个角色：迭代法与 Matrix-Free 算子的正确性对照基线（新求解路径先在小规模问题上与直接解比对），以及[[multigrid|多重网格]]最粗层的求解器（最粗层规模小到直接分解几乎免费）。

## 1. 分解与回代

一般矩阵用 LU 分解 $\mathbf A=\mathbf L\mathbf U$，对称正定矩阵用 Cholesky 分解 $\mathbf A=\mathbf L\mathbf L^{\mathsf T}$，对称不定矩阵用 $\mathbf L\mathbf D\mathbf L^{\mathsf T}$ 分解。求解分两次三角回代：先解 $\mathbf L\mathbf y=\mathbf b$，再解 $\mathbf U\mathbf x=\mathbf y$。对称正定情形不需要选主元，存储与运算量约为 LU 的一半，有限元刚度矩阵通常属于这一类。

分解一次后可以对任意多个右端项以回代成本重复求解，这是直接法相对迭代法的结构性优势：多载荷工况、灵敏度分析中的伴随求解、同一矩阵下的多次求解都能复用因子。

## 2. 填充与排序

对稀疏 $\mathbf A$，消元会在原本为零的位置产生新的非零元，称为填充。填充量由消元顺序决定，稀疏直接求解器的核心工作是在分解前对矩阵重排序以压低填充，常用策略有最小度（minimum degree / AMD）与嵌套剖分（nested dissection / METIS）。

填充的增长量级由问题的空间维数决定。对规则网格上的二阶椭圆问题，采用嵌套剖分排序时：

| 维数 | 因子非零元 | 分解运算量 |
|---|---|---|
| 二维 | $O(n\log n)$ | $O(n^{3/2})$ |
| 三维 | $O(n^{4/3})$ | $O(n^{2})$ |

二维问题的填充接近线性，直接法在百万自由度量级仍是合理选择；三维问题的因子非零元与运算量都远超原矩阵，内存随 $n$ 超线性增长，千万自由度以上通常不可行。

## 3. 主流实现与并行模型

MUMPS、PARDISO、CPardiso、SuperLU / SuperLU_DIST、PCLU（PETSc 内置 LU）是有限元软件中常见的稀疏直接求解器。它们在算法上同属分解—回代框架，差别集中在**并行模型**上，而并行模型决定了可达的问题规模上限与接口形态。

| | MKL PARDISO | CPardiso | MUMPS |
|---|---|---|---|
| 来源 | Intel，fork 自 Basel/Schenk 的 PARDISO | 同左 | CERFACS / IRIT / INRIA / ENS Lyon，学术开源 |
| 算法 | supernodal left-right looking | 同左 | 多波前（multifrontal） |
| **并行模型** | 共享内存 OpenMP 多线程，**单进程** | MPI + OpenMP | MPI + OpenMP（MPI 为设计核心） |
| 跨节点 | 不支持 | 支持 | 支持 |
| 单进程运行 | 本即单进程 | 1 rank 即可 | 链 `libmpiseq` 桩库可编成单进程构建 |
| 矩阵输入 | 单进程 CSR | 集中 / 分布可选 | 集中 COO / 分布可选，另有 element 格式 |
| 许可 | Intel 专有，免费可用 | 同左 | CeCILL-C 开源 |

表外的能力三者大体齐平：都覆盖实/复 × 对称/非对称（PARDISO 系用 `mtype` 选择，MUMPS 分成 `SMUMPS` / `DMUMPS` / `CMUMPS` / `ZMUMPS` 四个库）、都支持对称不定分解与惯性（负特征值个数）计数、out-of-core，以及 METIS / AMD 系排序（分布式实现另接 ParMETIS，MUMPS 另有 SCOTCH 系与 PORD）。函数入口与各项开关的具体编号见厂商手册 [4][5]，本页不复制会随版本变动的参数名。

两处命名易混淆之处需要固定：

- **MKL PARDISO（oneMKL PARDISO）与 CPardiso（oneMKL Cluster Sparse Solver）是 oneMKL 中的两个独立求解器**，不是同一求解器的两种模式。二者算法血统相同、`iparm` 约定相似，但函数入口、链接依赖（后者额外需要 `mkl_blacs` 与 MPI）与矩阵输入格式都不同，代码层面不能互换；**只有后者支持分布式内存**。
- **MUMPS（MUltifrontal Massively Parallel Solver）只有一份代码**，MPI 是其设计核心；所谓「串行版」是链接了空实现桩库 `libmpiseq` 的构建，不是另一个求解器。链了桩库的构建无法多进程运行，判别方式是检查实际链接的是 `libmpiseq` 还是真实 MPI 库。

上游原版 PARDISO 现由 Panua Technologies 维护（Panua-PARDISO），与 Intel 的两个实现不是同一套代码；文献与文档中「PARDISO」一词三者常混用。

分布式内存模型买到的是**容量上限**：因子切分到各进程后可跨节点累加内存，规模不再受单节点内存限制。代价是通信开销与切分带来的冗余，因此在同一节点内、相同核数下，把因子切碎的多进程配置通常慢于单进程多线程配置。三层并行的一般语义见 [[../gpu-hpc/parallel-levels]]。

## 4. 三阶段接口与符号分解复用

上述实现都把求解拆成三个可单独调用的阶段：

| 阶段 | 做什么 | 依赖 |
|---|---|---|
| 分析（符号分解） | 排序、构造消元树、确定因子稀疏结构 | 只依赖 $\mathbf A$ 的稀疏结构 |
| 数值分解 | 计算 $\mathbf L$、$\mathbf U$ 的数值 | 依赖 $\mathbf A$ 的数值 |
| 回代 | 前代与回代 | 依赖因子与右端项 $\mathbf b$ |

阶段划分在两种场景下产生实际收益：同一矩阵、多个右端项时复用因子，只重复第三阶段（见 §1）；**稀疏结构不变、只有数值改变的重复求解**时，第一阶段只需执行一次，此后每次只跑数值分解与回代。后者是同一网格上反复重装配刚度矩阵的迭代流程的典型形态。

接口上，MUMPS 用 `job` 参数选择阶段（1 分析、2 数值分解、3 回代，4、5、6 为组合），PARDISO 系用 `phase` 参数（11、22、33 及其组合）。实现层常见的浪费是把「一次做完三阶段」的组合调用写死在求解函数里，使符号分解无法在重复求解间复用。

## 5. GPU 支持现状

**上述三个实现都是 CPU 求解器**：符号分析、消元树调度与数值分解的主体都在 CPU 上执行，因子驻留主存。已有的 GPU 路径都带很强的限定条件：MKL PARDISO 可经 oneMKL 的 OpenMP Offload 接口卸载，目标设备为 Intel GPU；MUMPS mainline 无 CUDA 后端，只能通过替换底层 BLAS（如 XKBlas 构建选项）让稠密前沿计算借用 GPU（其官网另有「CPU 与 GPU」的表述，但截至 5.9.0（2026-04）未见对应的 mainline CUDA 特性说明，此处按发行版文档记，**待以 release notes 核实**）；CPardiso 无 GPU 路径。

判断一个求解器是否为 GPU 求解器，判据是**因子与求解过程是否常驻显存并由 GPU 主导**，而不是某个环节能否卸载。按此判据，具备原生 GPU 后端的稀疏直接求解器另有其列：NVIDIA cuDSS（单卡、单节点多卡、多节点多卡三种模式，多节点通过 CUDA-aware MPI 或 NCCL 通信）、SuperLU_DIST、STRUMPACK、PaStiX。GPU 直接法的容量约束比 CPU 更紧：因子必须放进显存，而显存通常远小于主存，§2 的填充增长量级因此更早成为限制。

## 参考文献

[1] DAVIS T A. Direct Methods for Sparse Linear Systems[M]. Philadelphia: SIAM, 2006. 稀疏分解、填充与排序算法。**refs.bib 尚无条目。**
[2] GEORGE A. Nested dissection of a regular finite element mesh[J]. SIAM Journal on Numerical Analysis, 1973, 10(2): 345-363. 嵌套剖分排序及其填充与运算量的量级结果。**refs.bib 尚无条目。**
[3] SAAD Y. Iterative Methods for Sparse Linear Systems[M]. 2nd ed. Philadelphia: SIAM, 2003. §3 稀疏矩阵与直接法基础。**refs.bib 尚无条目。**
[4] Intel. oneMKL Developer Reference: PARDISO / Parallel Direct Sparse Solver for Clusters. §3 的函数入口、`iparm`、矩阵输入格式与 OpenMP Offload 目标设备。**厂商文档，非文献条目。**
[5] MUMPS Technologies. MUMPS User's Guide. §3 的 `ICNTL` / `job` 语义、`libmpiseq` 构建与算术类型分库。**厂商文档，非文献条目。**
[6] NVIDIA. cuDSS Documentation. §5 的 GPU 直接法模式划分（单卡 / MG / MGMN）。**厂商文档（Preview 状态），非文献条目。**
