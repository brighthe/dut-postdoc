---
title: "郭老师线下汇报 2026-09-10"
advisor: "郭旭"
meeting_date: "2026-09-10"
meeting_mode: "线下"
status: "reported" # preparing | reported | follow-up-done
date_start: 2026-09-10
date_update: 2026-09-10
tags:
  - 工作汇报
  - PIML
  - matrix-free
  - GPU
  - SGSim
related:
  - "./overview"
  - "../guo-xu"
---

# 郭老师线下汇报 2026-09-10

跨次汇总见 [[overview|工作汇报总览]]。

## 汇报内容

- PIML + GPU 与 PIML + Matrix-Free 均已跑通。
- 规模算不大，只到 1000 万单元量级，原因是当前基于 FEALPy。该数字为口头口径，与 [[overview#4. 目前能求解多大规模的问题|总览 §4]] 记录不一致，待核对。

## 郭老师反馈

- 后续要能在研究院的软件框架（SGSim）下做。
- 问“异构”是什么意思。答：支持 GPU。

## 待办

- [ ] 问清 SGSim 代码访问权限与对接人，以及有无 MPI/GPU 层。
- [ ] 诊断 FEALPy 路径规模受限的具体原因，确认迁移后是否解除。
- [ ] 核对“1000 万单元”对应的路径与环节，补入总览 §4。
- [ ] 计算力学大会报名与经费本次是否已问：待补。
