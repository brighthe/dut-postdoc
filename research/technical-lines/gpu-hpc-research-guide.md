---
title: "GPU/HPC 异构并行与端到端性能技术线研究指南"
topic: "GPU 批处理、性能工程、显存、多后端、MPI 与多节点扩展"
tags:
  - technical-line
  - research-guide
  - GPU
  - HPC
  - heterogeneous-computing
  - MPI
  - performance-engineering
status: "in-progress"
date_start: 2026-07-21
date_update: 2026-07-21
related:
  - frame8_matrix_free_pipeline_guide
  - piml-matrix-free-execution-plan
  - piml-matrix-free-gpu-and-model-selection-technical-synthesis
---

# GPU/HPC 异构并行与端到端性能技术线研究指南

> **定位**：本页是 GPU/HPC 技术线的长期第一入口，负责批处理、数据布局、GPU 内核、显存、端到端 profiling、多后端、MPI 和多节点扩展。它服务多种数值方法，不从属于固定的 PIML × Matrix-Free 研究方向。
>
> **当前事实底线**：已经有 soptx 单次 GPU MatVec 证据和独立 mfleo GPU/MPI、端到端 CG、预条件子工程经验；尚未完成 PIML 批量推理与子结构 Matrix-Free 的一体化 GPU 管线，也没有实现桌面端十亿细网格。

## 一、技术线目标与边界

GPU/HPC 的目标不是只优化单个 kernel，而是把数值算法转化为可解释、可扩展、可集成的端到端性能能力。核心判断标准是完整 solve 或完整优化迭代的墙钟时间、峰值内存和扩展效率。

本技术线负责：

- PIML 推理、局部算子作用和批处理数据布局；
- Matrix-Free 提取、局部计算、scatter-add、向量更新和归约；
- CPU、CUDA、多后端和混合精度策略；
- GPU 显存、缓存、数据搬移和 kernel fusion；
- MPI、GPU-aware MPI、多 GPU 和多节点扩展；
- Roofline、端到端时间分解、强弱扩展和性能回归；
- 可复用性能模块和软件部署接口。

本技术线不负责：

- PIML 模型物理正确性的定义，见 [[piml-research-guide]]；
- Matrix-Free 算子、Krylov 和预条件算法的数学正确性，见 [[matrix-free-research-guide]]；
- 只凭单次 kernel 加速宣称完整求解或完整优化加速。

## 二、执行模型与性能账

完整优化迭代的时间应拆分为：

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

GPU/HPC 的最小性能账至少记录：

- 输入规模、自由度、子结构数、粗细网格比和精度；
- CPU/GPU 型号、进程/线程/设备数和软件版本；
- 预热、重复次数、同步点和计时边界；
- kernel 时间、完整 solve 时间和完整优化迭代时间；
- 峰值主存/显存、数据搬移量和通信量；
- Krylov 迭代数、预条件配置和数值误差；
- 强扩展、弱扩展、吞吐和性能回归。

## 三、当前已有基础

### 3.1 soptx GPU 算子证据

- 13.2 万 DOF 下，单次 GPU MatVec 约为 CPU 路径的 $11.9\times$。
- 内存估计从 42.1 MB 降至 4.0 MB。
- NumPy、PyTorch CPU、CUDA 三后端结果一致。

### 3.2 mfleo GPU/MPI 工程经验

- 已完成 650 万 DOF 的 GPU/MPI 端到端 CG。
- 1–32 个 MPI 进程配置下，相对同规模 MFEM PA 基线约 $3.72\times$–$12.74\times$。
- P2 tet 的 Jacobi、Chebyshev 预条件子测试：CPU 约 $1.20\times$–$1.21\times$，GPU 多数配置约 $4\times+$。

### 3.3 当前证据的准确读法

- $11.9\times$ 是 soptx 单次 GPU MatVec 加速，不是完整 solve 加速。
- mfleo 结果证明已有 GPU/MPI、Krylov 和预条件子工程基础，不是当前 soptx/PIML 融合系统的结果。
- 桌面端十亿细网格是长期架构牵引目标，当前尚未实现或验证。

## 四、核心研究问题

1. PIML 推理、局部算子作用和 scatter-add 应缓存、按需计算还是融合为一个管线？
2. 数据布局怎样兼顾规则子结构批处理、边界子结构和多种后端？
3. 当前瓶颈是算力、显存带宽、原子回填、数据搬移、归约、预条件还是通信？
4. 单次 MatVec 加速能否转化为完整 solve 和完整优化迭代收益？
5. FP64、FP32 与混合精度如何影响局部结构性质、Krylov 收敛和最终拓扑？
6. 多 GPU/多节点下如何处理全局归约、粗网格和负载不均衡？
7. 如何建立跨设备、跨后端和跨提交可复现的性能回归体系？

## 五、后续工作包

### WP-G1：可复现性能基线

- 冻结 CPU、GPU 和多后端一致性算例、计时方法和硬件信息格式。
- 区分 kernel、MatVec、solve 和完整优化迭代四级性能指标。
- 建立性能结果表与回归阈值，禁止只记录最快一次运行。

### WP-G2：PIML 批量推理

- 子结构按固定模板和形状分批，测量 batch throughput、延迟和显存。
- 比较“预测并缓存 $K_s$”与“每次 MatVec 按需推理”的内存—算力权衡。
- 评估推理与局部 $K_sx_s$ 融合，减少中间张量写回。

### WP-G3：Matrix-Free GPU 管线

- 实现局部提取、算子作用、scatter-add、向量更新和归约。
- 分析原子操作、颜色划分、分区回填和批处理大小的影响。
- 将预条件器和 Krylov 原语纳入同一 profiling，不把 MatVec 单独当作最终结果。

### WP-G4：完整优化流程

- GPU 化细尺度位移恢复、应变能、灵敏度和 PDE 滤波等潜在新瓶颈。
- 输出 $T_{\mathrm{iter}}$ 各分项及其比例，解释任何长期占比超过 60% 的环节。
- 比较 CPU、单 GPU 和多 GPU 下的误差—时间—内存 Pareto 前沿。

### WP-G5：多节点与软件集成

- 推进 GPU-aware MPI、通信隐藏和域/子结构划分。
- 开展强扩展、弱扩展和不同粗网格策略测试。
- 将后端选择、设备资源和性能诊断封装为可复用模块。

## 六、Benchmark 与验收指标

| 指标组 | 核心指标 |
|---|---|
| 正确性 | CPU/GPU 相对误差、残差、结构性质和最终响应误差 |
| Kernel | 延迟、吞吐、带宽、FLOPs、占用率和 launch 数量 |
| 求解 | MatVec、预条件、向量操作、迭代数和完整 solve 时间 |
| 完整流程 | 推理、恢复、灵敏度、过滤、优化和通信时间分解 |
| 内存 | 主存、显存、缓存、工作区和峰值占用 |
| 扩展性 | 单卡/多卡/多节点强弱扩展效率和通信占比 |
| 可复现性 | 硬件软件版本、重复次数、方差和性能回归 |

最低验收门槛：

- 所有加速比明确基线、硬件、规模和计时边界。
- GPU 与参考路径在约定容差内一致，并同时报告求解迭代数。
- 端到端结论以完整 solve 或完整优化迭代为主，单 kernel 数据只作解释。
- 多节点结论同时报告计算、通信、归约和粗网格成本。

## 七、阶段性交付物

| 阶段 | 交付物 |
|---|---|
| 近期 | CPU/GPU 基线、统一 profiling、PIML 推理与局部算子批处理原型 |
| 中期 | 端到端 GPU Matrix-Free solve、显存—吞吐报告、完整迭代时间分解 |
| 后期 | 多 GPU/多节点扩展曲线、性能回归体系和可复用异构后端模块 |

## 八、主要风险与回退

| 风险 | 回退策略 |
|---|---|
| PIML 推理覆盖 MatVec 收益 | 缓存 $K_s$、压缩表示或融合推理与局部作用 |
| scatter-add 原子冲突严重 | 颜色划分、分区缓冲或分阶段归并 |
| 预条件和归约成为新瓶颈 | 采用局部块预条件、通信隐藏和减少同步的 Krylov 变体 |
| 显存不足限制规模 | 流式批处理、重计算、压缩存储和分区执行 |
| 多 GPU 扩展效率差 | 优先优化负载划分、粗网格和全局归约，再扩大节点数 |
| 性能结果跨机器不可比 | 固化配置、硬件信息和基准协议，报告绝对时间与归一化指标 |

## 九、跨技术线接口

- 从 PIML 接收模型计算图、batch 形状、精度要求、缓存和回退策略。
- 从 Matrix-Free 接收局部提取、算子作用、scatter-add、Krylov 和预条件原语。
- 向 PIML 返回推理吞吐、显存和缓存—重算 Pareto 数据。
- 向 Matrix-Free 返回各算子和预条件环节的性能瓶颈，指导算法和数据结构调整。
- 可为 PIML、MMC/MMV、常规有限元、非线性求解和工程软件提供异构后端。

## 十、证据与关联文档

- [[research/postdoc-plan/defense-sprint/direction-1-piml-matrix-free/frame8_matrix_free_pipeline_guide]] — soptx GPU 与 mfleo 工程结果的事实来源。
- [[research/postdoc-plan/defense-sprint/direction-1-piml-matrix-free/frame9_piml_matrix_free_pipeline_guide]] — PIML × Matrix-Free × GPU 融合接口。
- [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-high-performance-solver-survey]] — GPU/异构并行与性能瓶颈调研。
- [[research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-execution-plan]] — GPU、多节点和软件集成工作包。
- [[piml-research-guide]]、[[matrix-free-research-guide]] — 另外两条长期技术线。
- [[_index]] — 长期技术线总入口。
