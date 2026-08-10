---
title: "GPU/HPC 端到端性能模型与测量口径"
type: concept
aliases:
  - GPU/HPC performance model
  - End-to-end performance model
  - 异构并行性能模型
tags:
  - GPU
  - HPC
  - performance-engineering
  - roofline
  - scalability
  - profiling
status: in-progress
date_added: 2026-07-26
date_update: 2026-08-03
---

# GPU/HPC 端到端性能模型与测量口径

> **一句话**：GPU/HPC 性能结论必须同时说明测量层级、数值正确性、基线、硬件、规模和计时边界；kernel 更快只是局部证据，只有完整 solve 或完整优化迭代的墙钟时间、内存和扩展性才能支撑端到端结论。

## 1. 五级测量边界

同一实现至少区分以下五级，不允许把低层结果外推为高层结论：

| 层级 | 测量对象 | 必须包含 | 不能替代 |
|---|---|---|---|
| Kernel | 单个 CUDA/CPU kernel | 明确输入规模、精度、同步点和重复统计 | 完整 MatVec |
| Operator / MatVec | 一次完整算子作用 | gather、局部计算、scatter-add、必要通信与同步 | Krylov solve |
| Solve | 一次线性或非线性求解 | setup/update、预条件、MatVec、向量原语、归约、通信和迭代数 | 完整优化迭代 |
| Optimization iteration | 一轮完整优化 | PIML、局部构造、solve、恢复、灵敏度、过滤、优化器与通信 | 完整任务 |
| End-to-end task | 从输入到最终结果的完整运行 | 初始化、迭代、必要 I/O、收敛判定和最终验证 | 无 |

对 PIML × Matrix-Free 拓扑优化，一轮时间可写为

$$
T_{\mathrm{iter}}
=
T_{\mathrm{PIML}}
+T_{\mathrm{local}}
+T_{\mathrm{solve}}
+T_{\mathrm{recover}}
+T_{\mathrm{sens}}
+T_{\mathrm{filter}}
+T_{\mathrm{opt}}
+T_{\mathrm{comm}}.
$$

各项必须采用互斥且可复核的计时边界；若通信、同步或数据搬移与计算重叠，应同时报告关键路径墙钟时间，不能简单累加重复区间。

## 2. 加速比与扩展效率

同一问题、同一正确性门禁和一致计时边界下，加速比定义为

$$
S_p=\frac{T_{\mathrm{base}}}{T_p}.
$$

基线必须写明算法、实现、硬件、进程/线程/设备数、精度和软件版本。若基线同时改变算法或离散，结果应称为“联合收益”，不能只归因于 GPU。

### 强扩展

固定总问题规模，增加资源数 $p$：

$$
S_p^{\mathrm{strong}}=\frac{T_1}{T_p},
\qquad
E_p^{\mathrm{strong}}=\frac{T_1}{pT_p}.
$$

### 弱扩展

保持每个进程或设备的工作量近似恒定：

$$
E_p^{\mathrm{weak}}=\frac{T_1}{T_p}.
$$

弱扩展必须同时说明局部规模、全局规模、划分方式、粗网格和停止准则是否随 $p$ 改变。强弱扩展结果均应报告计算、点对点通信、全局归约、负载不均衡和粗网格成本。

## 3. Roofline 与瓶颈判断

算术强度定义为

$$
I=\frac{\text{floating-point operations}}{\text{bytes transferred}},
$$

经典 Roofline 上界写为

$$
P_{\mathrm{attainable}}
\le
\min\!\left(P_{\mathrm{peak}},\, I\,B_{\mathrm{mem}}\right),
$$

其中 $P_{\mathrm{peak}}$ 是相应精度下的计算峰值，$B_{\mathrm{mem}}$ 是实测内存带宽。Roofline 用于判断 kernel 更可能受算力还是带宽限制，但不能解释完整 solve 中的 launch、同步、通信、负载不均衡和预条件成本。

PIML 推理、局部 contraction、scatter-add、稀疏/无矩阵算子、点积归约和粗网格求解具有不同算术强度，应分别测量；不得用一个 kernel 的 Roofline 位置代表完整应用。

## 4. 异构执行与通信口径

### CPU/GPU

- CPU 与 GPU 对照必须使用一致离散、输入、停止准则和数值容差。
- GPU 计时必须在预热后进行，并在计时区间边界显式同步；异步 launch 时间不能直接作为 kernel 完成时间。
- host-to-device、device-to-host、device-to-device 搬移是否计入，应随测量层级明确说明；端到端结果必须计入真实发生的数据搬移。
- FP64、FP32 和混合精度应分别报告残差、响应误差、迭代数及最终优化差异。

### MPI、多 GPU 与 GPU-aware MPI

- MPI 结果必须说明 rank、线程、节点、设备绑定、网格划分和 owned/ghost 数据语义。
- “GPU-aware MPI”表示 MPI 实现能够直接处理设备缓冲区；它不是仅由 MPI 标准版本即可保证的能力，必须记录具体 MPI 实现、版本、传输路径和验证结果。
- 多 GPU 计时必须覆盖 halo exchange、设备间传输、全局归约、粗网格和负载不均衡；只测每卡局部 kernel 不能支撑多 GPU 扩展结论。

## 5. 数据组织与时间—空间权衡

| 选择 | 主要收益 | 主要代价 | 必须测量 |
|---|---|---|---|
| 固定形状 batch | 提高吞吐与规则访存 | 边界类型、尾 batch 和 padding 可能浪费 | 吞吐、延迟、padding 比例、显存 |
| 缓存 $K_s$ 或中间表示 | 减少重复推理和局部构造 | 增加显存与更新成本 | 命中率、峰值显存、update 与 solve 时间 |
| 按需重算 | 降低持久存储 | 增加算力与调用次数 | 重算次数、墙钟时间、能耗或吞吐 |
| Kernel fusion | 减少 launch 和中间写回 | 增加寄存器压力和实现复杂度 | launch 数、带宽、占用率、端到端收益 |
| 混合精度 | 提升吞吐、降低内存 | 可能破坏结构性质或增加迭代 | 误差、迭代数、回退率、完整 solve |

比较方案时应输出误差—时间—内存 Pareto 前沿，而不是脱离数值约束给出单一“最快方案”。

## 6. 最小可复现性能记录

每条性能结果至少记录：

1. 问题定义：PDE、离散、网格、DOF、子结构数、材料参数、精度和停止准则；
2. 硬件：CPU、内存、GPU、互连、节点和设备数；
3. 软件：OS、编译器、Python/CUDA、框架、MPI、驱动和关键依赖版本；
4. 执行：命令、环境变量、rank/thread/device 绑定、随机种子和输入；
5. 计时：层级、预热、同步、重复次数、统计量和包含/排除项；
6. 正确性：参考路径、误差范数、残差、迭代数、结构性质和最终响应；
7. 资源：峰值主存/显存、数据搬移、通信量和 profiler 版本；
8. 结论：基线、绝对时间、加速比、瓶颈判断、适用范围和失败模式。

性能回归应比较相同基准配置下的统计结果，并保留正确性门禁。若硬件、依赖、算法或计时边界变化，应建立新基线，不能直接与旧结果做提交级回归。

## 7. 来源与证据

- Williams, Waterman & Patterson, 2009, [Roofline: An Insightful Visual Performance Model for Multicore Architectures](https://doi.org/10.1145/1498765.1498785)，`refs.bib` cite key：`Williams2009-roofline`。
- [NVIDIA CUDA C++ Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/) — profiling、正确性、精度、内存和扩展实践。
- [NVIDIA Nsight Systems User Guide](https://docs.nvidia.com/nsight-systems/UserGuide/) — 聚焦关键区间、时间线与 CPU/GPU/MPI profiling。
- [MPI Forum: MPI Documents](https://www.mpi-forum.org/docs/) — MPI 标准入口；具体设备缓冲区支持仍需以所用 MPI 实现为准。
- [[../../literature/topology-opt/notes/Ma2026-highperformanceparallel]] — CPU/MPI 强弱扩展和完整优化流程并行的本研究语境。
- [[../../research/piml-matrix-free-gpu/high-performance-solver-survey]] — 端到端时间分解、GPU/异构并行和性能瓶颈调研。

## 8. 相关页面

- [[_index]] — GPU/HPC 主题入口。
- [[method-lineage]] — 郭旭老师团队公开 HPC 方法谱系。
- [[../../research/technical-lines/gpu-hpc-research-guide]] — 当前研究目标、性能边界、证据锚点与阶段门禁。
- [[../matrix-free/assembly-levels]] — 算子装配层次与数据保存边界。
- [[../piml/mathematical-foundations]] — PIML 局部学习对象和结构性质。
