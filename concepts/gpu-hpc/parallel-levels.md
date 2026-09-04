---
title: "并行的三个层级：进程、线程与设备内"
type: concept
aliases:
  - Parallel Levels
  - 进程级/线程级/设备内并行
  - Process / Thread / SIMT Parallelism
  - Two-Level Hybrid Parallelism
tags:
  - HPC
  - MPI
  - GPU
  - parallelism
  - matrix-free
  - PIML
status: "in-progress"
date_added: 2026-08-22
date_update: 2026-09-03
---

# 并行的三个层级：进程、线程与设备内

> **一句话**：同一条 PIML–Matrix-Free–Krylov 计算链在进程、线程、设备内三层上各有一套卡点，**任一层的加速结论都不能外推到另一层**。
>
> **定位**：并行**层级**这一坐标轴的定义页，与装配层级（[[../matrix-free/assembly-levels]]）正交，只回答「切在哪一层、这层的墙是什么」。

## 定义

并行的层级 = 计算被切分并同时执行的粒度所在的硬件/软件边界。

| 层级            | 执行实体                 | 地址空间            | 典型接口                           |
| ------------- | -------------------- | --------------- | ------------------------------ |
| **进程级**       | OS 进程（MPI rank），可跨节点 | 各自独立，靠消息传递      | MPI                            |
| **线程级**       | 同一进程内的线程，限节点内        | 共享              | OpenMP、`torch.set_num_threads` |
| **设备内（SIMT）** | GPU 上数万条硬件线程         | 设备全局显存 + 片上共享内存 | CUDA kernel、PyTorch CUDA 算子    |

HPC 的标准提法是 two-level hybrid（外层 MPI + 内层设备）。本页把内层拆成线程与 SIMT，因为两者撞的墙不同：线程级撞节点内共享内存带宽，SIMT 级撞原子加冲突与访存合并度。**讨论跨节点扩展性用两级即可，定位具体卡点必须用三层。**

⚠️ [[_index#分布式系统的三层解耦]] 的 L1/L2/L3 是**职责分层**（这处改动归谁管），本页是**并行粒度分层**（计算切在哪儿），同名不同义。

## 关键要点

### 1. 三层 × 两侧的卡点

Matrix-Free 是宿主框架，PIML 是换进去的局部表示零件，故每层分两侧看。

| 层级 | 切什么 | Matrix-Free 侧卡点 | PIML 侧卡点 |
|---|---|---|---|
| **进程（节点间 MPI）** | 区域分解：每 rank 一块互不相交的单元 | ① 界面共享自由度的同步归约（halo）；② Krylov 每步内积的全局 `Allreduce` | ① **分区须与子结构边界对齐**（见下）；② 网络权重每 rank 各存一份（常数尺寸，不随规模增长） |
| **线程（节点内）** | 单元块 → OpenMP / BLAS / torch 线程 | 共享内存带宽墙：EA 算术强度约 `0.25 flop/byte`，加线程很快买不到加速 | 本课题不在 CPU 上做在线推理，耦合弱 |
| **设备内（SIMT）** | 单元/自由度 → 数万 CUDA 线程 | ① scatter-add 写竞态（`index_add` 原子加）；② 单元刚度阵访存合并度 | ① 批量推理的 SM 占用率与 batch 形状；② 权重常驻显存 |

**分区对齐是 PIML 特有的约束**（由两页事实推出，尚无实测，标「待验证」）。纯 Matrix-Free 的分区只要互斥且完备（[[distributed-operator-and-shared-dofs]] 第 1 节）怎么切都对；但 PIML 的局部表示在**整个子结构**上缩聚（[[../piml/piml-substructural]]），分区界面若横穿子结构，其接口自由度被切成两半，缩聚算子就无法在单 rank 内完成作用。**故分区面必须是子结构面的子集。**

### 2. 进程层：通信子与三种通信模式

进程层具体怎么切，由通信子（谁和谁通信）与通信模式（怎么通信）共同确定。选错不会算错，但会让通信走错物理通道。

| 通信子 | 创建/获取 | 适用场景 |
|---|---|---|
| **全局** | `MPI.COMM_WORLD` | 本次计算启动的全部进程组（默认基准） |
| **单进程隔离** | `MPI.COMM_SELF` | 单卡/单核完全隔离，用于 P=1 对照与调试 |
| **任务拆分** | `comm.Split(color, key)` | 多物理场/混合任务：拆成流体组、固体组或异步 I/O 组 |
| **节点内共享内存** | `comm.Split_type(MPI.COMM_TYPE_SHARED)` | 同机多卡/NUMA：同节点进程走 POSIX 共享内存，跳过网络协议栈 |
| **空间拓扑感知** | `comm.Create_dist_graph(...)` | 把子域几何邻接告知通信库，由底层优化路由 |

| 通信模式 | 典型调用 | 在分布式有限元中承担什么 |
|---|---|---|
| **集合 (Collective)** | `bcast`、`scatter`、`reduce`、`Allreduce` | 网格分发与参数广播；**Krylov 每步内积的全局归约** |
| **点对点 (P2P)** | `Send`/`Recv`、`Isend`/`Irecv` | 界面自由度同步归约 $\mathcal{S}$ 的底层通道；**非阻塞版是计算-通信重叠的前提**——传界面数据的同时算子域内部单元 |
| **单边 (RMA)** | `MPI.Win` 的 `Put`/`Get`/`Accumulate` | 零拷贝远程内存访问，适合动态非平衡负载；本课题当前未使用 |

⚠️ 通信模式只影响延迟隐藏程度，**不改变代数结果**：换非阻塞或单边通信不影响 $P$-rank 与 1-rank 的逐点一致性门禁。

### 3. 两个绕不开的断点

Matrix-Free + Krylov 只有两处必须跨执行实体交互，其余（gather、单元作用、AXPY）在三层上都无依赖：

1. **全局累加（scatter-add）——写冲突**：进程级表现为界面归约，SIMT 级为原子加竞态，线程级为伪共享。三种解法（原子加 / 单元着色 / 按自由度归约）见 [[../matrix-free/assembly-levels#2.3 EA/EbE：单元矩阵作用]]，本页不重复。
2. **Krylov 内积——全局同步**：CG 每步 2 次内积，进程级是 `Allreduce`，SIMT 级是 block reduction。共享自由度下须按引用计数加权才等于串行内积（[[distributed-operator-and-shared-dofs#4. 重叠加权内积与 Krylov 求解器收敛理论]] 定理 4）。实现参照：`soptx:src/soptx/fem/solvers/matrix_free_solver.py` 的 `weighted_norm`、`dot_fn` 与 `weighted_cg` 即此加权约定的落地。

这两处是 Matrix-Free 结构本身的性质，不是实现缺陷。

### 4. 瓶颈迁移：换成 PIML 后每层的墙都换位置

| | 精确单元作用（EA） | PIML 局部表示 |
|---|---|---|
| 算术强度 | 约 `0.25 flop/byte`，memory-bound | 批量推理化为稠密 GEMM，**可能**转为 compute-bound |
| 显存随规模 | 需流过全部 $\{\mathbf A_e\}$，随单元数线性增长 | 权重常数尺寸，不随单元数增长 |
| SIMT 侧卡点 | 访存合并度 | SM 占用率与 batch 形状 |

⚠️ **「转为 compute-bound」是待验证假设，不是实测结论**，拿到 Roofline 实测前不得当既有事实引用。显存不随规模增长这一条也需与 PA 路线对照——PA 同样能让每次作用的读取量不随单元矩阵增长。

### 5. 两处必须先消歧的用词

1. **「并行」的默认含义随语境变**：HPC/FEM 语境（PETSc、MFEM、MPI）默认指进程级，PyTorch 语境默认指线程级或设备内；跨语境说「已经并行了」双方理解不同。
2. **训练并行 ≠ 求解并行**：PIML 离线训练的 DDP 切的是样本，与在线求解切单元无关，扩展性结论不可互引。

## 与相关概念的关系

- **同一现实的另一种切法**：[[heterogeneous-execution-modes#2. 硬件拓扑的六种基本模式]] — 六种可部署配置即本页三层的开关组合（如「多节点 GPU-aware MPI」= 进程 + 设备内），该表另附各配置的外推边界，本页不重复。
- **正交**：[[../matrix-free/assembly-levels]] — 与 FA/LA/EA/PA/UA 构成二维坐标；只有「EA × SIMT 的原子加冲突」这种两坐标陈述才可排查，「Matrix-Free 在 GPU 上慢」不可排查。
- **下位事实源**：[[distributed-operator-and-shared-dofs]]（进程层代数正确性）、[[performance-model]]（各层测量口径）。

## 来源与证据

- [[../matrix-free/assembly-levels]] — EA `0.25 flop/byte`、scatter-add 写竞态三解、MPI 与装配层级正交。
- [[distributed-operator-and-shared-dofs]] — 分区互斥/完备契约、同步归约算子 $\mathcal S$、加权内积定理 4。
- [[../piml/piml-substructural]] — 子结构划分与内部/接口自由度分类。
- **待补**：线程级带宽饱和点、SIMT 占用率与访存合并度均无本课题实测，本页一律不写具体数值。

## 在我研究中的位置

讨论任何性能或扩展性结论前先钉死「哪一层」，避免把单卡 SIMT 的加速比说成跨节点扩展性，或把训练侧数据并行说成求解侧并行能力。当前实现与实测边界由 [[../../research/piml-matrix-free-gpu/gpu-hpc-research-guide]] 维护，本页不记录任务状态。

## 开放问题

1. PIML 批量推理在本课题的实际 batch 规模下是否真的越过 Roofline 拐点转为 compute-bound？
2. 「分区面必须是子结构面的子集」能否放宽到允许子结构跨 rank 缩聚？代价是多少次额外通信？
3. 线程级是否值得单独优化，还是直接跳到设备内？需节点内带宽饱和曲线实测才能判断。

## 相关页面

- [[_index]] — GPU/HPC 主题入口
- [[../linear-solvers/krylov-subspace-methods]] — Krylov 分族、收敛机制与并行同步点；求解器体系入口见 [[../linear-solvers/_index]]
- [[../piml/_index]] — PIML 局部表示与批量推理
