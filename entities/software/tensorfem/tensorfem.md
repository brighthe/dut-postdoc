---
title: "TensorFem：SGSim 张量有限元计算后端"
tags:
  - TensorFem
  - SGSim
  - FEM
  - GPU
status: draft
date_added: 2026-10-22
date_update: 2026-10-22
---

# TensorFem：SGSim 张量有限元计算后端

TensorFem 是本人正在开发、与 SGSim 衔接的有限元数值计算框架。按当前进展汇报，SGSim 负责模型导入、数据库与结果输出，TensorFem 承担数值计算和结果恢复，并支持不同张量计算后端。SGSim 的既有 PIML 模块另见 [[../sgsim/sgsim|SGSim 档案]]；不能将该模块的能力直接视为 TensorFem 已有能力。

本页依据《SGSim × TensorFem 异构有限元计算进展》整理截至 2026-10-22 的介绍性快照，不替代项目源码和实时开发记录。以下“已有”均指汇报所述，尚未独立核验源码、构建配置或原始测试结果。

## 1. 定位与计算流程

汇报的“总体架构”页给出两种输入路径：

- **Service 入口**：通过 SGSim 当前 Service 和 `DBServiceFactorySP`，由 `SgServiceAnalysisReader` 读取模型数据。
- **独立 .db 入口**：由 `Hdf5ModelReader` 读取 HDF5 `.db`，先读取 Model，再经 `AnalysisDataBuilder` 形成 `AnalysisData`。

数据进入 TensorFem 后，通过张量后端完成有限元数值计算，并与 PETSc 求解器衔接。结果经结果 Service 在同进程写回，再由 `SGExporter` 输出标准 HDF5；汇报另列独立 `.db` 路径的终端比较与退出码机制。

可将其职责概括为：

```text
SGSim 模型 / 独立 HDF5 .db
    → 输入适配与 AnalysisData
    → TensorFem 有限元计算与装配
    → PETSc 线性求解
    → 结果恢复与写回
    → SGSim 标准输出
```

SGSim 原生计算分支保留为对照。上述流程是对汇报架构图的概括，不代表已经核实各阶段的全部实现细节。

## 2. 张量后端与求解器

| 层次 | 汇报列出的路径 | 作用 |
|---|---|---|
| 张量计算后端 | `xtensor CPU` | CPU 张量计算路径 |
| 张量计算后端 | `Torch CPU` | Torch 的 CPU 计算路径 |
| 张量计算后端 | `Torch CUDA` | Torch 的 GPU 计算路径 |
| 线性求解器 | `PETSc CPU / CUDA` | 与数值计算后端衔接的线性求解层 |

因此，TensorFem 应介绍为支持多种张量后端的有限元框架，而非仅有 Torch 一条路径。张量后端与线性求解器属于不同层次。

**LibTorch 的表述边界**：用户已明确后续开发计划基于 LibTorch；汇报展示了 `Torch CPU` 与 `Torch CUDA`，但没有直接写出 LibTorch 的依赖和链接配置。若这些路径通过 PyTorch 的 C++ 接口实现，即属于 LibTorch 的使用；具体版本、构建方式和接口范围仍需源码确认。已有 Torch 张量计算能力，也不自动意味着已有神经网络模型导出、加载和推理接口。

## 3. 已展示的能力与验证范围

汇报“TensorFem 展望”页将以下内容列为已有基础：

- Hex/Tet 单元。
- CPU/GPU 计算路径。
- 多进程运行。
- Service 接口及 SGSim 结果输出。

汇报还展示结果正确性、实数与复数计算运行时间、阶段耗时、并行效率、内存和显存等对照。具体结论受算例、进程数、后端与求解配置约束；本介绍不摘录未经回查原始数据的加速比，也不将多进程运行等同于多 GPU 分布式能力已经完善。

## 4. 与 PIML 的后续衔接

当前讨论希望将离线训练得到的 PIML 模型接入 TensorFem/SGSim 的在线计算。这属于后续接口设计方向，汇报未证明已经实现。

SGSim 既有 PIML 说明采用 JSON 权重与激活函数配置，通过 C++/Eigen 执行前馈推理，详见 [[../sgsim/sgsim#1.4 训练与推理|SGSim 的训练与推理]]。TensorFem 的 Torch 后端为讨论 LibTorch 推理接入提供了基础，但仍需明确：

1. 离线端交付哪些模型文件与配置，在线端如何加载。
2. 材料输入的物理含义、预处理及编号顺序。
3. 网络输出的含义、排列与形函数补全方式。
4. 推理结果如何接入粗单元刚度计算、载荷映射及位移恢复。
5. 如何通过相同输入下的参考结果验证新旧推理路径一致。

这些是待确认的接口问题，不将 SOPTX 的 checkpoint 格式直接视为 SGSim 已支持的格式。

## 5. 后续开发方向

汇报列出的方向为：

- **计算核心独立化**：明确 DBManager 输入与回写边界，使计算核心、张量后端和求解器分别演进。
- **有限元内核扩展**：完善单元与材料计算契约，从 Hex/Tet 扩展单元与本构，验证后端一致性。
- **分布式能力完善**：完善单元与自由度归属、跨 rank 约束，逐步验证多卡多进程及通信开销。
- **性能与验证闭环**：补齐阶段时间、内存与通信观测，结合数学性质、后端一致性和原生结果对照开展优化。

Matrix-Free 在汇报中是按内存与性能证据进一步探索的路线，本页不将其列为已完成能力。

## 参考依据

- 《SGSim × TensorFem 异构有限元计算进展》，汇报标注 2026.10：“总体架构”“阶段用时”“TensorFem 展望”等页面。用户提供的本地来源为 `C:/workspace/dut-institute-work/reports/materials/biweekly-05/SGSim_TensorFem进展汇报.html`；该路径仅用于本次溯源，原件归档标识待登记。本轮未复制或修改原件。
- [[../sgsim/sgsim|SGSim 档案]] §1.4：依据《SGSim_PIML说明.pdf》整理的既有推理方式。
- 2026-10-22 本次讨论：用户确认 TensorFem 为本人正在开发的框架，并说明后续开发计划基于 LibTorch。
