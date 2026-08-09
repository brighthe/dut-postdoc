---
title: "GPU 异构执行模式"
type: concept
aliases:
  - GPU Heterogeneous Execution Modes
  - GPU 异构并行实现方式
  - 异构并行方法分类
tags:
  - GPU
  - HPC
  - heterogeneous-computing
  - multi-gpu
  - gpu-aware-mpi
status: complete
date_added: 2026-08-06
date_update: 2026-08-07
---

# GPU 异构执行模式

> **一句话**：GPU 异构并行由硬件拓扑、执行层级、编程模型和数据/精度策略四个正交维度构成；解答异构实现方式时，必须分别标注四维坐标，不能概括为单一的“用了 GPU”。
> 
> **定位**：本页是异构并行实现的**分类与硬件执行规范 (How & HPC)**（第 3 柱）。配合代数第一原理（[[distributed-operator-and-shared-dofs]]）与架构解耦框架（[[distributed-algebra-and-execution-decoupling]]）。

---

## 1. 四个正交维度

| 维度 | 核心关切与回答的问题 | 关键分类策略 |
|---|---|---|
| **硬件拓扑** (§2) | 使用哪些计算资源，它们如何拓扑连接？ | 纯 CPU $\to$ 单 GPU 卸载 $\to$ CPU-GPU 协同 $\to$ 单机多 GPU $\to$ 多节点 GPU-aware MPI |
| **执行层级** (§3) | 异构加速覆盖计算链的哪一段？ | kernel $\to$ MatVec/算子 $\to$ solve 求解 $\to$ 优化迭代 $\to$ 完整端到端任务 |
| **编程模型** (§4) | 用什么语言/接口/编译方式表达代码？ | 原生 (CUDA/HIP) $\to$ 指令式 (OpenMP) $\to$ Python JIT $\to$ 高层库 (CuPy) $\to$ 可移植后端 |
| **数据与精度** (§5) | 数据如何组织搬移，精度如何选择？ | 缓存/按需/融合内核；FP64 / FP32 / 混合精度 (Mixed Precision) |

---

## 2. 硬件拓扑的五种基本模式

| 硬件拓扑模式 | 资源与通信特征 | 主要适用场景 | 结论与外推边界 |
|---|---|---|---|
| **纯 CPU（参考基线）** | 单核/多核 CPU；无设备搬移，线程共享内存 | 算法正确性参考、组装式基线 | 不包含 GPU，但所有 GPU 结论均需与其对比 |
| **单 GPU 卸载** | 1 CPU Host + 1 GPU；Host-Device 显存搬移 | 单算子加速（如 Matrix-Free MatVec） | 搬移/Launch 开销易抵消收益；不可外推至多 GPU |
| **CPU–GPU 协同** | 多核 CPU + 1 或多 GPU；按并行性分配任务 | 复杂优化流程（CPU 管优化器/滤波，GPU 管求解） | 必须明确任务划分；联合收益不能全部归因 GPU |
| **单机多 GPU** | 1 节点内多 GPU；NVLink/PCIe/P2P 通信 | 扩展显存容量、并行不确定性量化 | 设备间带宽低于设备内；效率由负载均衡决定 |
| **多节点 GPU-aware MPI** | 多节点 × 多 GPU；MPI 直接传输 GPU 显存缓冲区 | 十亿级自由度、强弱扩展、分布式求解 | 依赖 GPU-aware MPI；Halo exchange 与通信-计算重叠需独立验证 |

---

## 3. 执行层级的五级阶梯

加速结论不能跨层外推：单 kernel 或 MatVec 加速**不自动等于**求解器 (solve) 加速，solve 加速**不自动等于**完整任务加速。

```text
kernel (单核) → MatVec (算子级) → solve (求解器) → 迭代 (单步优化) → 完整任务 (端到端)
```

---

## 4. 编程模型六档分类

| 编程模型档位 | 代表技术 | 特征 | 供应商锁定 |
|---|---|---|---|
| **原生 GPU 语言** | CUDA, HIP | 显式 kernel、手动显存管理；性能天花板最高 | 高 |
| **指令式 (Directive)** | OpenMP target offload, OpenACC | 编译器生成设备代码，宿主代码改动极小 | 低—中 |
| **Python 控制 + 原生底层** | pybind11 + C++/CUDA | Python 管控制与 IO，C++/CUDA 管热路径算子 | 取决于底层 |
| **Python JIT 编译** | JAX, Taichi (@jit) | 装饰器即时编译；开发极快，适合快速原型 | 中 |
| **高层库接口** | CuPy, PyTorch, NVIDIA Warp | 库调用自动映射到设备；Warp 编译为 PTX 近原生 | 高 |
| **可移植后端** | Kokkos, libCEED | 同一源码经后端抽象适配多种厂商设备 | 低 |

- FEALPy 架构见 [[reference-libraries/fealpy-architecture]]（Python 运行时分派），MFEM 架构见 [[reference-libraries/mfem-architecture]]（C++ 编译期展开），对比见 [[reference-libraries/fealpy-mfem-gpu-backend-comparison]]。

---

## 5. 关键易混淆判定规则

1. **Ma2026 纯 CPU/MPI 节点**：团队当前公开的分布式 HPC 节点为纯 CPU，不可声称已有 GPU 分布式实现（见 [[method-lineage]]）。
2. **SpMV 向量化 ≠ Matrix-Free**：从已生成的全局稀疏矩阵做 GPU SpMV 属于 FA 装配层的 GPU 化，不等于 EA/PA/UA 矩阵无关路线。
3. **CPU–GPU 协同加速 ≠ 完整任务加速**：仅将灵敏度放到 GPU、其余留 CPU 的协同模式，结论必须严格标注为“灵敏度环节加速”，不能写作端到端任务加速。

---

## 相关页面

- [[distributed-operator-and-shared-dofs]] — 代数第一原理（第 1 柱）。
- [[distributed-algebra-and-execution-decoupling]] — 系统架构解耦框架（第 2 柱）。
- [[performance-model]] — 五级计时口径、Roofline 与扩展性模型。
- [[method-lineage]] — 团队公开 HPC 成果谱系。
