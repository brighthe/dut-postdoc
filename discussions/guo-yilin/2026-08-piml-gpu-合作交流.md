---
title: "郭一麟博士 PIML 合作交流：GPU 加速工作介绍"
aliases:
  - 郭一麟合作交流
  - Guo Yilin cooperation
advisor: "郭一麟博士（合作者，郭旭老师介绍）"
report_period: "2026-08"
meeting_date: "待确定"
meeting_mode: "待定"
status: "preparing" # preparing | reported | follow-up-done
date_start: 2026-08-06
date_update: 2026-08-06
tags:
  - 工作汇报
  - 合作交流
  - GPU
  - PIML
topics:
  - "GPU 加速工作介绍；PIML 合作线索"
related:
  - "../../concepts/gpu-hpc/heterogeneous-execution-modes"
  - "../../concepts/gpu-hpc/reference-libraries/fealpy-architecture"
  - "../../concepts/gpu-hpc/reference-libraries/mfem-architecture"
---

# 郭一麟博士 PIML 合作交流：GPU 加速工作介绍

> **定位**：本页保存面向郭一麟博士（郭旭老师 2026-08 介绍的合作线索，PIML 方向）的首次交流材料底稿、事实边界和后续行动项。介绍正文可独立发送；真实沟通记录由沟通仓库维护，本页只保留带来源的必要摘要。

## 一、本次交流的目标

**背景快照（2026-08-06）**：郭旭老师介绍郭一麟博士在做 PIML 相关工作，可能涉及 GPU 加速技术，建议双方交流（引荐来源：郭旭老师；逐字沟通记录在沟通仓库 heliangos/wechat，本页不复制）。

交流目标：

- 让郭博士在「FEALPy 非共同知识」的假设下，快速建立对我 GPU 加速工作的坐标系（编程模型分类）与两条实例路线的认知；
- 了解对方 PIML 工作中 GPU 加速的具体场景（训练 / 推理 / 求解），判断两路线中哪些可直接复用；
- 不预设立场，交流后根据对方实际需求决定后续合作方向。

## 二、交流材料：GPU 加速工作介绍（三部分）

### 2.1 GPU 编程模型的分类

异构并行实现按编程模型大致分六档，从低到高抽象：原生 GPU 语言（CUDA/HIP，手写 kernel）→ 指令式（OpenMP/OpenACC，编译器从注释生成设备代码）→ Python 控制 + 原生底层（如 pybind11 桥接）→ Python+JIT（Taichi/JAX，装饰器即时编译为设备代码）→ 高层库接口（PyTorch/CuPy，调用库写好的 kernel）→ 可移植后端（Kokkos/MFEM/libCEED，同一源码适配多种厂商设备）。核心区别在「谁写 kernel、如何适配不同硬件」。

### 2.2 多后端抽象路线（我目前用的）

Python 运行时对象分派模式：统一入口 BackendManager 通过 `__getattr__` 属性重定向，让同一份用户代码在 numpy/pytorch/cupy/taichi 等后端下无改动执行；GPU 执行经 PyTorch（高层库接口，调用库写好的 kernel）与 Taichi（Python+JIT，可自写 kernel 即时编译）两条路径。我正基于这套框架做 GPU 上的弹性问题求解。

### 2.3 C++ 可移植后端路线（第三方开源库 MFEM）

MFEM 是 LLNL 开发的成熟开源有限元库（C++），多后端机制是「编译期展开 + 运行时分派」的混合：`Device` 单例在运行时按优先级链选择后端组合（CUDA/HIP/OpenMP/RAJA 等 15 个后端）；`mfem::forall` 宏在编译期把同一份 `MFEM_HOST_DEVICE` lambda 展开为对应后端的实际调用——用户用 lambda 写计算、不手写 kernel（编译产物即原生 CUDA/HIP kernel），换后端只需重新编译。

## 三、当前状态与事实边界

| 技术线 / 任务 | 当前状态 | 已有证据 | 尚不能说明什么 |
|---|---|---|---|
| 多后端抽象路线（介绍 2.2） | PyTorch 路径已验证；Taichi/JAX 机制存在未验证；CuPy 为占位实现不可用 | soptx `gpu_elasticity` minimal_demo CPU/CUDA 逐位一致（真相对残差 ≤ 1e-10） | 介绍正文按约定不强调未完成路径，边界在本页记录自用 |
| MFEM 路线（介绍 2.3） | 机制知识沉淀完成（Device/forall/Backend::Id） | [[../../concepts/gpu-hpc/reference-libraries/mfem-architecture|mfem-architecture]]（论文官方口径 + 源码核查） | 未实际用 MFEM 跑 GPU 问题，覆盖范围以论文口径为准 |
| 对方 PIML 工作 | 待交流 | Xu 2025（`xuProblemindependentMachineLearning2025`，作者含 Guo, Yilin）为团队公开 PIML 成果之一 | 对方当前 GPU 需求场景、具体方向未知 |

## 四、已有研究基础与本工作的增量

- 介绍所依据的知识：[[../../concepts/gpu-hpc/heterogeneous-execution-modes|六档分类]]、[[../../concepts/gpu-hpc/reference-libraries/fealpy-architecture|fealpy-architecture]]、[[../../concepts/gpu-hpc/reference-libraries/mfem-architecture|mfem-architecture]]——2026-08-06 整理完成，事实边界见各页。
- 工程实践：`soptx/examples/gpu_elasticity`（FEALPy GPU 流程，PyTorch 后端验证）。
- 本次介绍本身不构成新研究增量；价值在建立合作对话的共同基础。

## 五、接下来 TODOLIST

- [ ] 发出三部分介绍（2026-08 版本，正文见 §2）
- [ ] 记录对方回复与 GPU 需求场景
- [ ] 根据反馈更新本页结论与行动项

## 六、待确认事项与决策表

| 待确认事项 | 当前判断 | 希望对方 / 后续决定 |
|---|---|---|
| 对方 PIML 工作中 GPU 加速的具体场景（训练 / 推理 / 求解） | 未知 | 交流中了解，判断两路线可复用性 |
| 交流方式与时间 | 待确定 | 经郭旭老师牵线后约定 |

## 七、会后任务

- [ ] 根据交流反馈更新介绍材料与后续行动。

## 八、会后结论与行动项

> 当前尚未交流。交流后只记录实际结论，不预写。

| 行动项 | 来源 | 状态 | 截止时间 | 证据 / 结果 |
|---|---|---|---|---|
| 待补充 | 待补充 | 待开始 | 待确定 | 待补充 |

## 九、关联文档

- [[../../concepts/gpu-hpc/heterogeneous-execution-modes]] — 六档编程模型分类（介绍 §2.1 的事实源）。
- [[../../concepts/gpu-hpc/reference-libraries/fealpy-architecture]] — 多后端抽象机制（介绍 §2.2 的事实源）。
- [[../../concepts/gpu-hpc/reference-libraries/mfem-architecture]] — MFEM 机制（介绍 §2.3 的事实源）。
- [[../../concepts/piml/method-lineage]] — 团队公开 PIML/HPC 成果谱系（Xu 2025 含 Guo, Yilin 的上下文）。
- [[../guo-xu/_index|郭旭老师工作汇报入口]] — 引荐背景。
