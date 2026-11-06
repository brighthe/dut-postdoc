---
title: SGSim
type: entity
entity_kind: software
aliases:
  - SGSim
  - sgsim
  - entities/software/sgsim
  - entities/software/sgsim/sgsim
tags:
  - SGSim
  - CAE-software
  - PIML
  - substructure
status: draft
date_added: 2026-10-17
date_update: 2026-10-23
source: 黄靖翔博士撰写的《SGSim_PIML说明.pdf》
related:
  - ../../guo-xu/reports/overview
  - ../../guo-xu/reports/2026-09-10-sgsim-framework-meeting
---

# SGSim

## 基本信息

| 项    | 内容                                                                        |
| ---- | ------------------------------------------------------------------------- |
| 定位   | 研究院软件框架                                                                   |
| 实现语言 | C++；PIML 前馈计算用 Eigen 矩阵运算实现                                               |
| 代码组织 | 有限元计算位于 `SGFem/Task` 子模块，输入、结果数据结构位于 `DataStructure/`；PIML 代码在 **dev 分支** |
| 文档状况 | 《SGSim_PIML说明》由黄靖翔博士撰写；该文档称 PIML 目前暂无专门技术文档，接口与调用方式主要参考源码及测试用例            |

## 1. PIML 模块

SGSim 中的 PIML 用于三维线弹性静力分析：以 PIML 子结构作为粗单元，用已训练的神经网络预测多尺度形函数，计算粗单元刚度，再接入 SGSim 的有限元组装、求解和结果恢复流程。

### 1.1 支持范围

- **单元配置**：默认推理配置为 5×5×5 细分的 PIML 子结构。每个粗单元内含 125 个规则六面体细单元；粗单元有 8 个角节点，每节点 X、Y、Z 三个平动自由度，粗单元刚度矩阵为 24×24。
- **材料**：各向同性线弹性参数。粗单元内部材料分布由细单元材料分布值描述，并据此分三类：

| 类型 | 标识 | 处理方式 |
|---|---|---|
| 全空单元 | `MTYPE = 0` | 使用缓存的弱刚度矩阵 |
| 全实体单元 | `MTYPE = 1` | 使用缓存的实体粗单元刚度矩阵 |
| 边界 / 混合单元 | `MTYPE = 2` | 按细尺度材料分布预测形函数，再计算粗单元刚度 |

- **载荷与约束**：已接入粗节点载荷、细尺度载荷向粗节点的映射，以及粗节点平动自由度的单点约束。
- **输出**：粗节点位移、约束反力，以及粗单元内部的细尺度位移。

### 1.2 模型数据接口

模型通过以下数据结构及对应数据库服务传入计算模块：

| 数据结构 | 作用 |
|---|---|
| `BOXData` | 包围盒尺寸、各方向粗网格数量及粗单元内部细分数量，并提供节点编号关系 |
| `COARSEData` | 粗单元及材料分布类型 |
| `MATBData` | 边界 / 混合粗单元内部的细尺度材料分布 |
| `PIMLSPCData` | 粗节点的单点约束 |
| `PIMLCOARSELOADData` | 粗节点载荷的作用节点、方向和幅值 |
| `PIMLFINELOADData` | 载荷作用的粗单元及其内部细单元分布 |

对应服务为 `IBOXService`、`ICOARSEService`、`IMATBService`、`IPIMLSPCService`、`IPIMLCOARSELOADService`、`IPIMLFINELOADService`，通过 `DBServiceFactory` 获取。已有测试包含 VGM 模型导入后调用静力求解器的示例。

### 1.3 C++ 计算接口

核心类 `PIMLElementCalculator` 实现统一的 `IElementCalculator` 接口，以 `ELETYPE_COARSE` 注册到 `ElementCalculatorFactory`。

| 接口 | 功能 |
|---|---|
| `SetCalculationParameters()` | 设置几何、材料参数，加载网络参数并准备计算缓存 |
| `calculateStiffness()` | 计算单个粗单元的刚度矩阵和多尺度形函数矩阵 |
| `calculateNPredict()` | 获取用于载荷映射及位移恢复的多尺度形函数矩阵 |
| `PrepareCoarseLoads()` | 将细尺度载荷映射为粗节点载荷 |
| `ComputeElementMatries()` | 遍历粗单元，计算并组装刚度矩阵；名称沿用源码拼写 |
| `DataRecovery()` | 由粗节点位移恢复细尺度位移，并写入数据库 |

- 求解层保留 `PIMLSolver::Solve()`，同时已接入通用 `StaticSolver` 流程。细尺度载荷映射在 `MModel` 初始化阶段接入，保证静力求解前已备好粗尺度载荷。
- 应力、应变和应变能的计算与存储实现位于 `ComputeStressStiffness()`。当前 PIML 的 `DataRecovery()` 只负责细尺度位移恢复，应力等计算在相关测试中额外调用。

### 1.4 训练与推理

**说明明确 SGSim 内没有模型训练流程**：程序只用已有模型参数推理，源码不含对应的训练脚本、训练数据集和优化器流程。说明未提供样本生成代码，也未交代已有权重的训练框架及外部训练代码位置。

默认运行时从可执行程序旁的 `Data/EN_5/` 目录加载 JSON 格式的权重与激活函数配置，用 4 个前馈神经网络完成预测；网络参数由 `PIMLNetData` 加载，前向计算在 C++ 中通过 Eigen 矩阵运算实现。推理使用固定权重进行预测，不更新网络参数；它与离线训练是不同阶段。说明未描述 LibTorch 推理路径，是否未使用 LibTorch 列入下文确认。计算过程为：

1. 读取 `BOX`、材料参数及各粗单元的 `COARSE`、`MATB` 数据。
2. 对边界 / 混合单元，将 125 个细单元材料分布值组成网络输入。
3. 调用前馈网络预测内部节点的多尺度形函数，与基准形函数组合得到形函数矩阵 $\mathbf N$。
4. 用 $\mathbf N$ 和细单元刚度计算粗单元刚度，组装整体刚度矩阵。
5. 细尺度载荷按 $\mathbf f_c=\mathbf N^{\mathsf T}\mathbf f_f$ 映射到粗尺度，求解粗尺度静力方程。
6. 由 $\mathbf u_f=\mathbf N\mathbf u_c$ 恢复细尺度位移。

其中 $\mathbf f_c$、$\mathbf f_f$ 分别为粗、细尺度载荷，$\mathbf u_c$、$\mathbf u_f$ 分别为粗、细尺度位移。网络预测的是多尺度形函数，整体位移仍由有限元方程求解。

当前实现显式形成粗单元刚度并组装全局稀疏矩阵，尚未实现 matrix-free 求解接口。说明文档建议与后续 HPC 架构衔接时重点关注单元计算、整体组装及线性求解器之间的接口。

### 1.5 代码位置

| 位置 | 内容 |
|---|---|
| `SGFem/Task/PIML/PIMLSolver.cpp` | PIML 静力求解流程 |
| `SGFem/Task/PIML/PIMLElement/PIMLElementCalculator.cpp` | 网络推理、粗单元刚度、载荷映射和结果恢复 |
| `SGFem/Task/PIML/PIMLElement/StiffnessCache/` | 网络参数加载、基准形函数、刚度缓存及多尺度计算辅助函数 |
| `SGFem/Task/PIML/PIMLElement/EN_5/` | 默认使用的预训练网络参数 |
| `DataStructure/Input/PIML/` | PIML 输入数据结构 |
| `DataStructure/Result/PIML/` | PIML 结果数据结构 |
| `SGFem/Task/PIML/test/` | 数据输入、载荷映射、求解、位移恢复及 VGM 使用示例 |
| `SGFem/Task/PIML/PIMLElement/UnitTest/` | 单元刚度、形函数及辅助计算测试 |

说明文档称程序近期仍在维护，相关工作包括通用静力求解流程接入、载荷映射、计算实现和测试修正。

## 2. 当前理解与待确认问题

当前依据为黄靖翔博士提供的《SGSim_PIML说明.pdf》，尚未核查 SGSim 源码。说明明确网络预测形函数，再结合细单元刚度计算粗刚度；但未明确非重叠划分、角点三线性边界插值及完整变分刚度公式。8 个角节点、24 个自由度不足以单独证明采用了特定的边界插值方法。

`test/` 与 `UnitTest/` 已包含测试及使用示例；后续重点是确定可先跑通的算例、输入数据、运行方法与参考结果，以便与 [[../tensorfem/tensorfem|TensorFem]] 对接。

### 给黄博士的反馈

以下为 2026-10-23 整理的交流草稿，尚未记录发送或回复。前两项为依据说明梳理、拟进一步确认的现状，后三项为实现细节及算例请求。

黄博士您好，我仔细看了您提供的文档，整理了几个问题，想跟您进一步确认一下：

1. 目前 SGSim 的 PIML 模块只加载已有权重进行推理，尚未集成对应的样本生成和网络训练代码。
2. 目前 SGSim 的 PIML 模块读取 JSON 格式的模型参数，通过 C++/Eigen 完成网络推理，未使用 LibTorch。
3. 目前 SGSim 的 PIML 模块是否采用非重叠子结构静力缩聚框架，并由角点位移通过三线性插值确定子结构边界位移？
4. 目前 SGSim 的 PIML 模块是否采用形函数预测路线，再通过变分形式 $K_c=N^{\mathsf T}K_fN$ 构造子结构刚度？
5. 针对说明中已有的测试，是否方便推荐一个算例及其运行方法、参考结果，以便后续与 TensorFem 衔接和开展对照测试？

## 参考依据

- 黄靖翔博士《SGSim_PIML说明.pdf》，3 页，2026-10-15 经微信接收：PIML 支持范围、接口、训练与推理组织及测试代码位置；原件归档标识待登记。
- 2026-10-23 本次讨论：区分文档事实与方法假设，整理五项交流问题；不作为开发者回复或源码核验证据。
