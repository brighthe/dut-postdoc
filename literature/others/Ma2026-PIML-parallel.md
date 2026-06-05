---
title: A high-performance parallel algorithm based on problem independent machine learning (PIML) for large-scale topology optimization
authors:
  - Ma, # TODO 补全作者列表
year: 2026
journal: # TODO
doi: # TODO
tags:
  - PIML
  - topology-opt
  - parallel-computing
  - matrix-free
  - multigrid
  - large-scale
status: reading
rating:
date_added: 2026-06-05
date_read:
---

# A high-performance parallel algorithm based on problem independent machine learning (PIML) for large-scale topology optimization

> 完整中文译文：[[assets/Ma2026-PIML-parallel-zh]]

## 一句话概括

<!-- TODO -->

## 研究问题

<!-- TODO：大规模拓扑优化的“维度灾难”瓶颈；并行计算（硬件层面）与 PIML（算法层面）结合能在多大程度上拓宽可处理规模与效率边界 -->

## 方法

### 核心思路

<!-- TODO：全并行化的 PIML 增强拓扑优化框架 -->

### PIML 增强子结构方法（串行）

<!-- TODO：经典子结构缩聚 + PIML 学习缩聚刚度矩阵 -->

### 并行实现

<!-- TODO：每进程工作负载划分、并行多重网格求解器、多尺度形函数的 matrix-free 实现、均匀粗单元直接缩聚、计算资源限制调整 -->

## 实验 / 数值验证

<!-- TODO：弱扩展效率、强扩展加速比、最大可达效率；PC 与超算平台 -->

## 主要结论

<!-- TODO -->

## 优点与局限

**优点：**

<!-- TODO -->

**局限：**

<!-- TODO -->

## 对我研究的启发

<!-- TODO -->

## 相关文献

- [[Huang2022-PIML-universal]] — PIML 奠基论文，本文的串行子结构方法基础
