---
title: "SGSim"
type: entity
entity_kind: software
aliases:
  - SGSim
  - sgsim
  - entities/sgsim
  - entities/sgsim/sgsim
tags:
  - SGSim
  - CAE-software
  - PIML
  - substructure
status: draft
date_added: 2026-10-17
date_update: 2026-10-17
source: "黄靖翔博士撰写的《SGSim_PIML说明.pdf》（2026-10-15 微信接收，3 页）"
related:
  - "../guo-xu/reports/overview"
  - "../guo-xu/reports/2026-09-10-sgsim-framework-meeting"
---

# SGSim

> 研究院软件框架，由郭老师团队研发，本人未参与。2026-09-10 线下汇报时郭老师要求后续工作能在 SGSim 下运行，见 [[../guo-xu/reports/2026-09-10-sgsim-framework-meeting|2026-09-10 线下汇报]]。本页目前只整理其 PIML 模块；§1 依据黄靖翔博士撰写的《SGSim_PIML说明》，§2 为本页对照本库概念的推导，§3 列待确认事项。

## 基本信息

| 项 | 内容 |
|---|---|
| 定位 | 研究院软件框架；本库 [[../guo-xu/reports/overview#5. 在团队软件代码框架下运行\|工作汇报总览 §5]] 记为郭老师团队研发 |
| 实现语言 | C++；PIML 前馈计算用 Eigen 矩阵运算实现 |
| 代码组织 | 有限元计算位于 `SGFem/Task` 子模块，输入、结果数据结构位于 `DataStructure/`；PIML 代码在 **dev 分支** |
| 本人参与 | 未参与研发；尚无代码访问权限记录 |
| 文档状况 | 《SGSim_PIML说明》由黄靖翔博士撰写；该文档称 PIML 目前暂无专门技术文档，接口与调用方式主要参考源码及测试用例 |

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

**SGSim 内没有模型训练流程**：源码只用已有模型参数推理，不含训练脚本、训练数据集和优化器流程。

默认运行时从可执行程序旁的 `Data/EN_5/` 目录加载 JSON 格式的权重与激活函数配置，用 4 个前馈神经网络完成预测；网络参数由 `PIMLNetData` 加载。计算过程为：

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

## 2. 与本库概念的对应（本页推导）

以下为对照本库概念页的推导，未经 SGSim 源码或开发者核实。

- **接口类型与路线**：只保留 8 个角节点的粗单元对应 [[../../concepts/piml/piml-substructural#4.2 角点接口空间|PIML 子结构 §4.2]] 的 `linear_corner`；先预测形函数、再由细网格刚度计算粗单元刚度，对应其中的路线 A，即 $\widehat{\mathbf K}_c=\widehat{\mathbf N}^{\mathsf T}\mathbf K\widehat{\mathbf N}$，$n_c=24$。“基准形函数”应对应式 (4.6) 中已知的边界插值块 $\mathbf L^j$，待确认。
- **规模**：5×5×5 规则六面体细分共 $6^3=216$ 个细节点、648 个细尺度自由度，减去 24 个角点自由度后，网络需补全的形函数块最多为 $624\times 24$；实际是否只预测内部节点、边界非角点由插值给出，取决于“内部节点”的口径。
- **均匀单元缓存**：`MTYPE = 0/1` 直接取缓存刚度，与 [[../../concepts/matrix-free/mf-piml-substructural#1. 共同环节|子结构 PIML Matrix-Free 算子 §1]] 中“材料均匀时直接取精确参考值、代替网络预测”的做法一致。
- **载荷与恢复**：$\mathbf f_c=\mathbf N^{\mathsf T}\mathbf f_f$ 与 $\mathbf u_f=\mathbf N\mathbf u_c$ 使用同一形函数矩阵，对应 [[../../concepts/piml/piml-substructural#5.3 子结构位移恢复|PIML 子结构 §5.3]] 的位移恢复。
- **Matrix-Free 衔接**：当前显式形成 $\widehat{\mathbf K}_c$ 并组装全局稀疏矩阵，属于 [[../../concepts/matrix-free/mf-piml-substructural#3. 角点接口路径|子结构 PIML Matrix-Free 算子 §3]] 中保存局部刚度、组装全局矩阵的做法。改为不组装全局矩阵时，切入点是 `IElementCalculator` 的单元计算、`ComputeElementMatries()` 的组装以及 `StaticSolver` 所用的线性求解器接口。
- **训练外置**：SGSim 只推理，网络训练须在外部完成后导出为 `EN_5` 格式的 JSON 参数；本人的 FEALPy/SOPTX 训练结果若要接入，需先对齐网络结构、输入编号与输出格式。

## 3. 待确认

- [ ] 代码访问权限、对接人及 dev 分支对应的 commit 或版本。
- [ ] 有无 MPI 或 GPU 并行层；说明文档未提及。
- [ ] 4 个前馈网络各自预测的内容，以及 `EN_5` 的训练来源与对应文献。
- [ ] “内部节点”是否包含边界非角点节点；“基准形函数”的具体定义。
- [ ] `MTYPE = 0` 弱刚度矩阵的弱材料取值。
- [ ] 应力恢复为何不并入 `DataRecovery()`，后续是否计划并入。
- [ ] 全局线性求解器类型（直接法或迭代法）及可求解规模。

## 参考依据

- 《SGSim_PIML说明.pdf》，黄靖翔博士撰写，2026-10-15 经微信接收，3 页：§1 全部内容，原件未登记。
- [[../guo-xu/reports/overview|郭老师工作汇报总览]] §5：SGSim 定位与研发方。
