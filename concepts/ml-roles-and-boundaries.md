---
title: "计算力学中的机器学习：作用位置与方法边界"
type: concept
aliases:
  - ml-roles-and-boundaries
  - piml/ml-roles-and-boundaries
  - 计算力学机器学习路线
  - 机器学习作用位置与方法边界
tags:
  - machine-learning
  - computational-mechanics
  - topology-opt
  - PINN
  - PIML
status: in-progress
date_added: 2026-07-28
date_update: 2026-08-06
---

# 计算力学中的机器学习：作用位置与方法边界

> **一句话**：本文按机器学习在计算链中替代或预测的对象建立宏观方法图谱，横向比较计算力学中的 6 大机器学习路线；具体路线的 5 步通用范式与推导见各自专一范式页。

通用机器学习分类框架（模型族、架构、归纳偏置与 5 阶段生命周期）见 [[machine-learning]]；本文专注于计算力学领域不同机器学习路线的**作用位置、计算角色与方法图谱**。

---

## 1. 分类目的与适用范围

机器学习可以按训练信号、模型类型、学习对象、物理融合方式等不同维度分类。本页选择“学习对象及其在计算链中的作用位置”作为主轴，回答：

> 一个机器学习模型学习什么对象、替代哪一段计算、依赖哪些物理设置，又能在什么范围内复用？

* **全局分类框架**：[[machine-learning]] 维护通用模型族与 5 阶段生命周期骨架。
* **PINN 5 步通用范式**：[[pinn-paradigm]] 专门维护物理信息解场学习的 5 步数学与计算范式。
* **PIML 5 步通用范式**：[[piml/piml-paradigm]] 专门维护问题无关局部算子代理的 5 步端到端流程与数据流图。

---

## 2. 机器学习在计算链中的 6 大作用路线图谱

### 2.1 计算力学 ML 全景图谱

| 方法路线 | 学习对象 | 典型映射 | 在计算链中的作用 | 代表工作或外部对照 |
|---|---|---|---|---|
| **1. 问题相关的最终设计代理** | 最终优化设计 | 问题参数 → 设计变量／拓扑 | 直接生成候选设计，或为完整优化提供热启动 | [[../literature/topology-opt/notes/Lei2018-machinelearningdriven\|Lei2018]]（MMC 实时拓扑优化） |
| **2. 设计表示与分辨率映射** | 不同尺度或分辨率下的设计表示 | 高分辨率设计 ↔ 低分辨率设计 | 将高分辨率问题映射到较低分辨率上优化，再恢复设计 | FE-CNN (2021) |
| **3. 物理信息解场学习 (PINN)** | 特定 PDE 的解场或待识别参数 | 空间坐标 $\boldsymbol{x} \to$ PDE 解场 $\hat{\boldsymbol{u}}(\boldsymbol{x})$ | 以网络近似解函数，替代传统 PDE 求解或服务反问题 | [[pinn-paradigm\|PINN 5步通用范式]]；[Raissi et al. (2019)](https://doi.org/10.1016/j.jcp.2018.10.045) |
| **4. 问题无关的局部力学表示学习 (PIML)** | 局部算子、形函数、缩聚刚度矩阵 | 局部材料分布 $\boldsymbol{\rho}^j \to$ 局部算子 $(\mathbf{N}^j, \mathbf{K}_e^j)$ | 替代反复出现的局部构造，拼装至全局方程求解 | [[piml/piml-paradigm\|PIML 5步通用范式]]；[[../literature/topology-opt/notes/Huang2022-problemindependentmachine\|Huang 2022]] 及其扩展 |
| **5. 本构与多尺度行为学习** | 本构关系、局部响应、均匀化关系 | 实验/微结构信息 → 材料多尺度响应 | 替代或增强材料本构模型及跨尺度关系构造 | MAP123、循环塑性神经网络 |
| **6. 生成式与逆向设计** | 满足给定条件或性能的候选设计 | 性能/草图/条件 → 候选设计 | 生成候选结构、探索非唯一逆解并辅助后续优化 | DiffMat、神经网络草图辅助拓扑优化 |

---

## 3. 核心路线横向对比与范式跳转

下表横向对比当前最需要辨析的三类代表性路线。具体路线的详细 5 步数据流与代数推导均已重构下沉至各自专一范式页：

| 比较维度 | 问题相关的最终设计代理 | 物理信息解场学习 (PINN) | 问题无关的局部力学表示学习 (PIML) |
|---|---|---|---|
| **专一范式入口** | 见 [[../literature/topology-opt/notes/Lei2018-machinelearningdriven\|Lei2018 笔记]] | 👉 **[[pinn-paradigm\|PINN 5步通用范式]]** | 👉 **[[piml/piml-paradigm\|PIML 5步通用范式]]** |
| **学习对象** | 最终优化设计 | 特定 PDE 的解场或待识别参数 | 可复用的局部力学算子/表示 |
| **训练信号** | 优化算法生成的设计标签 | PDE残差、初边值残差 | 局部真值标签或 mechanics-based loss |
| **主要替代环节** | 完整优化的结果生成或初始设计 | 传统 PDE 求解器 | 局部形函数/缩聚/粗单元矩阵构造 |
| **保留全局求解** | 直接预测时跳过；热启动时保留 | 由网络直接逼近解函数 | **完全保留**全局平衡方程 $\mathbf{K}_{\text{global}}\boldsymbol{U}=\mathbf{F}$ |
| **局部力学载体** | 无局部载体（绑定整体设计域） | **无局部载体**（绑定全局域 $\Omega$） | **显式绑定**（子结构/粗单元/重叠网格） |
| **复用边界** | 固定设计域、边界与载荷 | 改变边界/载荷需**重新训练** | **跨宏观 BVP 免重训**，秒级推理复用 |

---

## 4. 术语与方法边界消歧

- **“物理信息解场学习 (PINN)”**：以神经网络直接逼近全局连续解场，依赖全局坐标 $\boldsymbol{x}$，属于 Problem-Dependent 范式。详见 [[pinn-paradigm]]。
- **“问题无关机器学习 (PIML)”**：特指 Huang–Ma 路线中显式绑定局部力学载体（粗单元/子结构），学习“局部材料 $\to$ 局部算子”映射并嵌入全局方程的范式。详见 [[piml/piml-paradigm]]。
- **“问题无关”的限定**：仅表示局部模型不依赖宏观几何、整体边界条件和外载荷；物理 PDE、材料本构和离散单元类型改变时，仍需调整或重新训练模型。

---

## 5. 相关页面

- [[machine-learning|通用机器学习分类与 5 阶段生命周期]]
- [[pinn-paradigm|物理信息神经网络 (PINN) 通用 5 步范式]]
- [[piml/piml-paradigm|问题无关机器学习 (PIML) 通用 5 步范式]]
- [[piml/mathematical-foundations|Problem-Independent 路线的数学基础]]
- [[piml/method-lineage|Huang–Ma PIML 方法演进谱系]]
- [[../research/technical-lines/piml-research-guide|PIML 局部力学算子技术线研究指南]]
