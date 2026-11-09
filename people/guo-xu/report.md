---
title: "郭旭工作阅读与讨论问题"
aliases:
  - 郭旭工作汇报与讨论问题
advisor: "郭旭"
status: preparing
date_start: 2026-11-03
date_update: 2026-11-04
tags:
  - 工作汇报
  - PIML
  - Matrix-Free
  - GPU
  - 合作交流
related:
  - "./guo-xu"
  - "./reports/overview"
  - "./reports/2026-09-10-sgsim-framework-meeting"
---

# 郭旭工作阅读与讨论问题

> 用于向合作导师 [[guo-xu|郭旭]] 老师汇报 PIML、Matrix-Free 与 GPU 相关研究进展，以及博士阶段延续论文审阅与合作署名事宜。第一部分整理文献依据、郭老师的核心关注点与我方已有材料入口；第二部分按讨论轮次记录拟发送内容与实际反馈。目前第二部分均为待发送准备稿，历史沟通记录另见 [[../../sources/wechat/guo-xu/wechat-log|微信沟通档案]] 与 [[reports/overview|工作汇报总览]]。

## 一、基础调研

### 1.1 阅读范围

郭旭老师的已入库合著论文见 [[guo-xu#已入库的 PIML 与相关合著论文|人物页论文表]]。以下列出围绕 PIML 子结构多尺度计算、大规模并行与 Matrix-Free 汇报所重点参考的代表性工作，不表示已入库文献全部完成精读。

| 论文 | 本次关注的内容 |
|---|---|
| [[../../literature/topopt/piml/translations/Huang2022-problemindependentmachine-zh\|Huang 2022]] | PIML 局部多尺度形函数学习及其在宏观结构分析与拓扑优化中的应用 |
| [[../../literature/topopt/piml/translations/Huang2023-PIML-substructure-zh\|Huang 2023]] | 子结构静力缩聚下的形函数预测与等效刚度构造，作为我方实现与对照的基准 |
| [[../../literature/topopt/piml/translations/Huang2024-PIML-datafree-zh\|Huang 2024]] | DeepONet 与基于力学的 data-free 训练 |
| [[../../literature/topopt/piml/translations/Ma2026-highperformanceparallel-zh\|Ma 2026]] | PIML 子结构路线的大规模并行拓扑优化与多尺度形函数按需预测释放 |
| [[../../literature/topopt/piml/translations/Guo2026-highgeneralization-bezier-zh\|Guo 2026 Bézier]] | 三次 Bézier 边界位移参数化与内部响应预测 |
| [[../../literature/topopt/piml/translations/Guo2026-PIML-OFEM-zh\|Guo 2026 PIML-OFEM]] | 超采样数值基函数与重叠有限元 |

### 1.2 郭老师关注的五个核心方向

据 [[../../sources/wechat/guo-xu/wechat-log|微信沟通档案]]（2026-07-01、07-05）及 [[reports/2026-09-10-sgsim-framework-meeting|2026-09-10 线下汇报]]、[[reports/overview|工作汇报总览]]，郭老师对博士后主线工作明确提出了以下五个关注重点：

| 关注点 | 具体要求与背景 | 来源入口 |
|---|---|---|
| Matrix-Free 在 PIML 中的应用 | 用无矩阵技术解决大规模计算中矩阵组装和内存需求过大的问题 | [[../../sources/wechat/guo-xu/wechat-log#2026-07-01（星期三）\|2026-07-01 沟通]]、[[reports/overview#1. Matrix-Free 在 PIML 应用中的进展\|总览 §1]] |
| GPU 在 PIML 中的应用 | 结合 GPU 编程大幅提升 PIML 训练、预测与求解效率 | [[../../sources/wechat/guo-xu/wechat-log#2026-07-01（星期三）\|2026-07-01 沟通]]、[[../../sources/wechat/guo-xu/wechat-log#2026-07-05（星期日，线下见面）\|2026-07-05 线下]] |
| Matrix-Free 与 GPU 的联合应用 | 打通预测、局部算子作用与迭代求解的端到端 GPU 无矩阵流程 | [[reports/overview#3. Matrix-Free + GPU 在 PIML 应用中的进展\|总览 §3]] |
| 可求解的问题规模 | 将计算规模持续往上推（远期目标：桌面级设备求解亿至十亿级细网格问题） | [[../../sources/wechat/guo-xu/wechat-log#2026-07-01（星期三）\|2026-07-01 沟通]]、[[reports/overview#4. 目前能求解多大规模的问题\|总览 §4]] |
| 在团队软件框架下运行 | 后续工作需落地到研究院软件框架（[[../../software/sgsim/sgsim\|SGSim]]）中，形成可复用的软件能力 | [[../../sources/wechat/guo-xu/wechat-log#2026-07-01（星期三）\|2026-07-01 沟通]]、[[reports/2026-09-10-sgsim-framework-meeting\|2026-09-10 线下汇报]] |


## 二、讨论问题

### 2.1 第一次讨论

**PIML-GPU 与 Matrix-Free 工作汇报**：向郭老师汇报近期围绕 PIML-GPU（含与郭一麟博士的交流进展）以及全尺度有限元与 PIML 子结构 Matrix-Free 实现所开展的对照实验。

**何亮：**

郭老师，针对 PIML 结合 GPU 和 Matrix-Free 提升计算效率、降低大规模计算存储开销的工作，想向您汇报一下目前的进展：

1. PIML-GPU 方面：基于统一张量接口实现了单机单卡 GPU 上的 PIML 子结构算法，不同计算后端与 CPU/GPU 共用同一套代码。在 165 万单元的三维 MBB 梁算例上，相比 16 核 CPU，GPU 在离线样本生成与网络训练上分别加速约 26 倍和 14 倍，在线子结构矩阵组装与单轮结构分析分别加速 7.2 倍和 3.5 倍（当前角点系统规模较小，单轮分析的加速收益相对有限）。另外我也和郭一麟博士做了交流，他那边三维 PIML-OFEM 已基本实现 GPU 化并在撰写论文。下一步将考虑向多机多卡拓展，并与郭一麟博士进一步交流 GPU 实现技术路径，结合两边经验优化现有实现，提高计算效率、扩大可计算规模。

2. PIML-Matrix-Free 方面：针对 PIML 子结构全边界缩聚和边界角点缩聚，从两个层次做了四种实现对照：缩聚算子层考虑不形成和组装缩聚矩阵，直接完成算子作用；细尺度刚度层考虑不组装子结构刚度，利用共享参考单元刚度完成计算。全边界缩聚下，两个层次结合，25.7 万单元算例的峰值显存由 10.97 GiB 降至 2.45 GiB，降低约 77.7%；边界角点缩聚下，当前测试中保留小规模显式缩聚系统、仅在细尺度刚度层采用共享参考单元刚度更省显存，368.5 万单元算例由 5.84 GiB 降至 4.91 GiB，降低约 16.1%。下一步将与郭一麟博士进一步交流，探讨 Matrix-Free 和 PIML-OFEM 的结合；同时研究子结构细分数对显存开销及各实现方案相对优势的影响，探索细尺度刚度层的部分组装 PA、不组装 UA 与不同缩聚方式的结合，推进 MPI 多 GPU、多节点并行，并研究适配的预条件方法和预测形函数按需重算策略，进一步降低显存、提高求解效率、扩大可计算规模。PIML-Matrix-Free 方面的具体实现和完整显存对照结果已整理在文档里，随消息一并发给您，供您参考。

**研究院项目进展汇报**：向郭老师简要汇报在研究院软件框架下的项目推进与后续计划。

**何亮：**

另外跟您汇报一下研究院项目这边的进展：目前我和算海这边已经跑通了 SGSim × TensorFem 异构有限元计算的 Demo 流程，同时我也和黄靖翔博士讨论了解了 SGSim 中已有的 PIML 相关内容。目前的主要问题是 TensorFem 现有 Demo 在多进程分区交互、基础模块边界划分以及扩展接口上还不够清晰统一。下一步安排：先和算海分阶段推进 TensorFem 的架构重构以及与 SGSim 的结合，后续再逐步把 PIML-GPU 和 Matrix-Free 相关工作接入进来。

**胡张元论文汇报**：在汇报完上述工作、且论文经刘畅与梅跃老师先行把关后，顺带向郭老师汇报博士阶段论文已写完、准备投稿，请郭老师把关，并邀请他共同署名作为通讯作者。

**何亮：**

郭老师，我还把之前博士阶段的一部分工作整理成了一篇论文，主要将高阶 Hu–Zhang 混合有限元引入密度法拓扑优化，以对称应力和位移为独立未知量，建立了非结构化网格下支持柔顺度最小化与局部应力约束体积最小化的计算框架。目前论文已经写完、准备投稿，想请您帮我把把关，同时也想邀请您一起署名作为通讯作者，不知道您觉得是否合适？。
