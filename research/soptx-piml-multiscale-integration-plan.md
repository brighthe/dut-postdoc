---
title: "SOPTX 中 PIML 多尺度预测原型与拓扑优化集成计划"
tags:
  - execution-plan
  - PIML
  - EMsFEM
  - multiscale-FEM
  - SOPTX
  - FEALPy
  - topology-optimization
status: "in-progress"
date: 2026-06-29
related:
  - piml-matrix-free-execution-plan
  - piml_multiscale_math_principles
  - soptx-matrix-free-integration-plan
  - one-week-defense-sprint-plan
---

# SOPTX 中 PIML 多尺度预测原型与拓扑优化集成计划

本文档把答辩前 **PIML 多尺度预测能力的展示**，落实为一个可逐项实现、验证和生成图表的短期
开发计划。它与 [[soptx-matrix-free-integration-plan]] 在 Matrix-Free 上的角色对应：
是"PIML 多尺度预测原型"在任务层面的主计划。

与 [[piml-matrix-free-execution-plan]] 的关系：那份是 24 个月的**长期任务计划**。本原型采用
**子结构缩聚形式（路线①）**，因此对应其阶段一 **T1.3.2「复现 2023 子结构 PIML」** 的最小前向核心
（Huang 2022 的 EMsFEM 角节点形式即 T1.3.1，本原型不采用、作奠基引用）；同时对应
[[one-week-defense-sprint-plan]] Day 3-4，目标是**打通单步前向管道并产出可视化图表**，
不追求工业级完整度。理论依据见 [[piml_multiscale_math_principles]]，奠基论文见
[[../literature/topology-opt/Huang2022-problemindependentmachine]]。

**形函数构造形式（路线①·已定，2026-06-29）**：原型采用**子结构静力缩聚（Schur 补）**构造精确
多尺度形函数与等效刚度——$\boldsymbol N^j=[-(\boldsymbol K_{ii}^j)^{-1}\boldsymbol K_{ib}^j;\ \boldsymbol I]$，
$\boldsymbol K_s^j=(\boldsymbol N^j)^T\boldsymbol K^j\boldsymbol N^j$（见 [[piml_multiscale_math_principles]] 与
[[piml-matrix-free-high-performance-solver-survey]] 第三节）。选这条而非 Huang 2022 的 EMsFEM 角节点形式，
原因有二：① 缩聚**数学上精确、无边界条件假设**，自洽且**仅凭已有调研即可实现、几乎不需补读新论文**；
② 它正是高性能终局（[[piml-matrix-free-execution-plan]] 主线二、Ma 2026 并行 Matrix-Free）所用的
**逐子结构算子形式**——预测出的 $\boldsymbol K_s^j$ 可直接喂给全局 Matrix-Free 作用
$\boldsymbol y=\sum_j(\boldsymbol A^j)^T\boldsymbol K_s^j(\boldsymbol A^j\boldsymbol x)$，与 [[soptx-matrix-free-integration-plan]] 咬合。
Huang 2022 的全 EMsFEM（角节点 + 线性 BC）复现保留为 [[piml-matrix-free-execution-plan]] 阶段一 T1.3.1，
答辩中作奠基/动机引用。

当前策略与 Matrix-Free 一致：**尽量减少对 FEALPy 的修改，将 PIML 多尺度预测原型
主要整理到 SOPTX 中实现**。FEALPy 继续提供网格、有限元空间、自由度映射与基础后端；
SOPTX 负责粗/细两级网格组织、局部细单元刚度、PIML 预测器（原型期用 mock）、
粗尺度等效刚度组装与求解。

## 1. 总体目标

在 SOPTX 中建立一个最小可运行的 **PIML 多尺度前向分析原型**，跑通

```text
宏观（粗网格）密度分布
  -> 子结构（粗单元）内局部细尺度密度 ρ^j
  -> PIML 预测器（原型期 mock / 极小训练）-> 缩聚算子 N̂^j
  -> 子结构等效刚度 K̂_s^j = (N̂^j)^T K^j N̂^j
  -> 组装接口缩聚方程 K^cond U_b = F_b  （单步，可选求解）
```

并完成以下验证：

1. **管道连通性验证**：从宏观密度输入到接口缩聚方程组装，单步前向全程跑通、无接口断点；
2. **算子性质验证**：$\widehat{\boldsymbol N}$ 满足分区单位（刚体平移/转动再现）；
   $\widehat{\boldsymbol K}_s$ 对称、（去刚体后）正定；
3. **缩聚精确性验证**：`ExactPredictor` 的静力缩聚 $\boldsymbol K_s^j$ 与全尺度细网格在该子结构上的
   Schur 补**数学上等价**、机器精度一致（作为预测的对照真值）；
4. **PIML 预测精度验证**：用**极小预测器**（随机局部密度离线训练，损失 = 算子 MSE + 缩聚刚度 MSE）
   的预测 $\widehat{\boldsymbol K}_s^j$ 对照精确 $\boldsymbol K_s^j$，给出粗/细比 $5\times5$、$10\times10$ 下的
   相对误差，进入**团队子结构 PIML 工作量级（~$10^{-3}$）**；
5. **可视化交付**：宏观粗网格 ↔ 子结构内细观映射图（`piml_baseline.pdf`）+ 预测误差对照（`piml_pred_error.pdf`）。

> 注意诚实边界：原型训练**极小预测器**，仅为取得**可对照已发表论文的预测误差**，
> **不追求生产级精度/泛化、不跑优化循环、不做完整误差传播分析**——这些属于
> [[piml-matrix-free-execution-plan]] 阶段一/二。答辩口径：声称"前向管道打通 + 静力缩聚机器精度精确 +
> PIML 预测误差进入团队论文量级 + 全局求解降至子结构接口自由度且与 Matrix-Free 咬合（不组装全局、突破内存墙）"。

## 1.1 开发仓库与分支约定

本文档只作为 `dut-postdoc` 知识库中的任务计划与答辩口径记录。实际程序开发应切换到 SOPTX 仓库：

```text
C:\workspace\soptx_heliang
```

建议新建独立功能分支（与 Matrix-Free 的 `matrix-free-interface` 并列）：

```text
codex/piml-multiscale-prototype
```

约定（与 [[soptx-matrix-free-integration-plan]] 一致）：

1. **代码修改发生在 SOPTX 仓库**，不要在 `dut-postdoc` 放临时代码；
2. **计划与结论沉淀在 dut-postdoc**，阶段性设计/验证回填到本文档或相关 research 文档；
3. **先 mock 预测器，后真实 ANN**：第一轮只要求打通 `predict() -> N̂ -> K̂^E -> 组装`，
   `predict()` 内部可用查表 / 解析映射 / 精确局部求解，不要求立即训练网络；
4. **每个阶段有可运行测试**：新增功能配套最小测试或 benchmark，避免只写接口不验证。

## 2. 软件分工

### 2.1 FEALPy 侧：保持只读依赖

只复用已有能力：粗/细网格构造、LagrangeFESpace、quadrature、cell-to-dof 映射、
boundary dof 查询、backend manager。如确有必要只补极薄访问接口，不把多尺度业务逻辑放入 FEALPy。

### 2.2 SOPTX 侧：新增 PIML 多尺度分析模块

建议新增或整理如下模块（命名随 SOPTX 现有风格调整）：

```text
soptx/
  analysis/
    multiscale/
      __init__.py
      coarse_fine_mesh.py        # 粗/细两级网格与映射关系
      multiscale_shape.py        # 多尺度形函数（精确求解 + 预测接口）
      equivalent_stiffness.py    # K^E = Σ N^T k N 组装
      piml_predictor.py          # PIML 预测器抽象（mock / trained 两实现）
  benchmarks/
    benchmark_piml_forward.py
  examples/
    piml_baseline_forward.py     # 单步前向 demo + 出图
  tests/
    test_equivalent_stiffness_vs_fullscale.py
    test_shape_function_partition_of_unity.py
```

## 3. 核心代码任务

### T1. 粗/细两级网格与局部映射

在一个二维矩形域上构造粗网格，每个粗单元内部细分为 $m=L\times L$ 个细单元
（如 $5\times5$、$10\times10$），建立粗节点自由度 ↔ 粗单元内细节点自由度的索引映射。

验收：给定粗单元编号，可取出其内部细单元集合、细节点、以及 coarse→fine 自由度映射。

### T2. 精确多尺度形函数 / 等效刚度（子结构静力缩聚，作为基线真值）

对每个子结构（粗单元），按**静力缩聚（Schur 补）**消去内部自由度：

$$
\boldsymbol N^j=\begin{bmatrix}-(\boldsymbol K_{ii}^j)^{-1}\boldsymbol K_{ib}^j\\ \boldsymbol I\end{bmatrix},
\qquad
\boldsymbol K_s^j=(\boldsymbol N^j)^T\boldsymbol K^j\boldsymbol N^j
=\boldsymbol K_{bb}^j-(\boldsymbol K_{ib}^j)^T(\boldsymbol K_{ii}^j)^{-1}\boldsymbol K_{ib}^j .
$$

它是 mock/ANN 预测的**对照真值**与训练标注来源，**数学上精确、无边界条件假设**
（区别于 Huang 2022 的 EMsFEM 角节点 + 线性 BC 构造，后者属阶段一 T1.3.1）。

验收：$\boldsymbol N^j$ 满足分区单位（刚体模态再现）；$\boldsymbol K_s^j$ 与全尺度 Schur 补一致（机器精度）。

### T3. 接口缩聚方程组装

把各子结构 $\boldsymbol K_s^j$ 按**接口（边界）自由度**组装为全局缩聚刚度 $\boldsymbol K^{\text{cond}}$，
形成接口方程 $\boldsymbol K^{\text{cond}}\boldsymbol U_b=\boldsymbol F_b$。

验收：$\boldsymbol K^{\text{cond}}$ 对称、（去刚体后）正定；**全局求解自由度 = 接口自由度**
（远小于全尺度细网格自由度，且可进一步走 Matrix-Free 不显式组装 $\boldsymbol K^{\text{cond}}$）。

### T4. PIML 预测器抽象、mock 与极小训练实现

定义统一预测接口，提供三种实现：

```python
class MultiscalePredictor:
    def predict(self, rho_local):
        """输入粗单元内 m 个细单元密度，返回多尺度形函数 N̂（或等效刚度 K̂^E）。"""
        ...

class ExactPredictor(MultiscalePredictor):
    """精确求解局部问题（基线 / 标注真值）。"""

class MockPredictor(MultiscalePredictor):
    """查表 / 解析映射，先打通接口与管道。"""

class TrainedPredictor(MultiscalePredictor):
    """极小 MLP，随机局部密度离线训练；损失 = 算子 MSE + 缩聚刚度 MSE。"""
```

验收：三种实现接口互换；对实体（ρ≈1）/弱材料（ρ≈0）极端输入返回合理缩聚算子。

### T4b. 极小预测器训练

随机生成局部密度场作样本、`ExactPredictor`（静力缩聚）提供标注，训练一个**极小 MLP**
（优先 PyTorch/JAX 后端，不可用则退化为 NumPy/sklearn 小网络）。仅为取得对照论文的预测误差，
**不追求生产级精度/泛化**。

验收：`TrainedPredictor` 在测试集上的预测误差进入团队子结构 PIML 量级（~$10^{-3}$，见 V4）。

### T5. 单步前向分析闭环

固定一组宏观密度 $\boldsymbol\rho$，完成：

```text
ρ -> ρ_local（逐粗单元）-> predict -> K̂^E -> 组装 K^coarse
（可选）施加边界/载荷 -> 求解 U^coarse -> 恢复 u^fine
```

验收：单步前向跑通；若求解，则与全尺度细网格直解结果趋势一致、相对误差可记录。

## 4. 验证与图表任务

### V1. 静力缩聚精确性（精确路径）

测试 `test_equivalent_stiffness_vs_fullscale.py`：用 `ExactPredictor` 的 $\boldsymbol K_s^j$
与该子结构在全尺度细网格上的精确 Schur 补比较，`rel_error < 1e-10`。

> 答辩口径：静力缩聚在数学上与全尺度 Schur 补**等价**；PIML 改变的是"如何**快速获得** $\boldsymbol K_s^j$
> （按需预测替代内部自由度消元）"，不改变离散模型。

### V2. 形函数分区单位分解

测试 `test_shape_function_partition_of_unity.py`：$\boldsymbol N$ 各分量行和满足分区单位、
刚体平移/转动下 $\boldsymbol K^{E}$ 作用为零（机器精度）。

### V3. 前向管道连通性与可视化

`examples/piml_baseline_forward.py` 跑通单步前向，并绘制：

1. 宏观粗网格 + 某粗单元高亮；
2. 该粗单元内部细网格密度分布；
3. coarse→fine 形函数映射示意（`u^fine = N̂ u^coarse`）。

保存为 `piml_baseline.pdf`（同时输出到
`dut-postdoc/talks/2026-postdoc-entry-assessment/figures/`）。

### V4. PIML 预测精度（对照团队子结构 PIML）

用 `TrainedPredictor` 的预测 $\widehat{\boldsymbol K}_s^j$ 对照 `ExactPredictor` 的精确 $\boldsymbol K_s^j$
（及接口求解的柔顺度），给出粗/细比 $5\times5$、$10\times10$ 下的相对误差：

| 粗/细比 | 预测误差量级（目标） |
|---|---|
| $5\times5$ | ~$10^{-3}$ |
| $10\times10$ | ~$10^{-2}$ |

> 锚点：静力缩聚本身**精确**（机器精度，见 V1）；预测误差是极小网络拟合精确缩聚算子的误差。
> 量级对照**团队子结构 PIML（Huang 2023）**——该论文确切数待阶段一 T1.1.3 精读后回填；
> Huang 2022（EMsFEM 角节点）作奠基引用。

绘制预测误差对照图/表，保存为 `piml_pred_error.pdf`（同输出到 deck figures 目录）。

## 5. 最小可执行顺序

| 阶段 | 任务 | 交付物 | 验收 |
|---|---|---|---|
| 1 | 粗/细网格与映射 | `coarse_fine_mesh.py` | 映射可取用 |
| 2 | 子结构静力缩聚 | `multiscale_shape.py` | 分区单位 + 刚体模态再现 |
| 3 | 接口缩聚组装 | `equivalent_stiffness.py` | 对称正定；求解自由度=接口 |
| 4 | 缩聚精确性测试 | `test_equivalent_stiffness_vs_fullscale.py` | `rel_error < 1e-10` |
| 5 | mock 预测器 + 接口 | `piml_predictor.py` | 与 ExactPredictor 互换 |
| 6 | 单步前向闭环 | `piml_baseline_forward.py` | 管道跑通 |
| 7 | **极小预测器训练** | `train_piml_predictor.py` + 模型权重 | 测试集预测误差入团队量级 |
| 8 | **预测精度对照** | `piml_pred_error.pdf` + 误差表 | 对照团队子结构 PIML（~1e-3） |
| 9 | 管道可视化出图 | `piml_baseline.pdf` | 可用于答辩 |

## 6. 答辩展示口径

推荐表述（路线①·子结构缩聚 + Matrix-Free 咬合）：

> 我在 SOPTX/FEALPy 上搭建了 PIML 多尺度预测的单步前向核心管道：宏观粗网格密度 →
> 极小 PIML 预测器 → 逐子结构静力缩聚算子 $\widehat{\boldsymbol K}_s^j$ → 组装接口方程。
> 静力缩聚在数学上**精确**（与全尺度 Schur 补机器精度一致）；PIML 预测的缩聚刚度相对误差进入
> 团队子结构 PIML 工作的量级（~$10^{-3}$）；全局求解规模降至子结构**接口自由度**，且预测出的
> $\widehat{\boldsymbol K}_s^j$ 可**直接喂给全局 Matrix-Free 作用、不组装全局缩聚刚度**——这正是题目
> "PIML 预测 + Matrix-Free 求解"的咬合点。后续升级为结构保持网络、多层预条件与 GPU/大规模并行。

建议答辩页展示三项（帧 7「能力 B」口径）：

1. **求解降维 + 不组装**：全局求解降至子结构接口自由度；$\widehat{\boldsymbol K}_s^j$ 喂给 Matrix-Free
   **不组装全局、突破内存墙**（承接能力 A / Ma 2026）——主卖点；
2. **预测精度**：静力缩聚精确（机器精度）+ PIML 预测误差 ~$10^{-3}$，**对照团队子结构 PIML**——可信度；
3. **连通图 + 承接**：`piml_baseline.pdf` 宏微映射；与 Matrix-Free
   （[[soptx-matrix-free-integration-plan]]）共用 SOPTX 分析后端、承接博士 FEALPy/可微分基础设施。

底部结论：

> 从"在线求解局部细尺度问题"升级为"离线训练、在线预测"的多尺度分析，
> 为大规模拓扑优化的 PIML 增强结构分析提供可落地的软件入口。

## 7. 关联文档与参考论文

**关联文档（dut-postdoc）**

- [[piml_multiscale_math_principles]] — 数学原理（子结构缩聚构造形式、Matrix-Free 协同）
- [[piml-matrix-free-execution-plan]] — 24 个月长期任务计划（本原型 = 其 T1.3.1 最小前向核心）
- [[piml-matrix-free-high-performance-solver-survey]] — 调研（§3 子结构 Schur 缩聚，**路线①直接依据**）
- [[soptx-matrix-free-integration-plan]] — 姊妹计划（Matrix-Free，能力 A⊗B 咬合点）
- [[one-week-defense-sprint-plan]] — 答辩前一周冲刺（本原型 = Day 3-4）

**参考论文（literature/topology-opt）**

- [[../literature/topology-opt/Huang2022-problemindependentmachine]] — Huang 2022, *EML* 56:101887：EMsFEM-PIML 奠基；ANN 配方与"问题无关性"来源；其全 EMsFEM 复现归长期计划阶段一 T1.3.1。
- [[../literature/topology-opt/Huang2023-PIML-substructure]] — Huang 2023, *EML* 63:102041：子结构 PIML；**V4 预测误差对照锚点**（待 T1.1.3 精读回填确切数）。
- [[../literature/topology-opt/Ma2026-highperformanceparallel]] — Ma 2026, *Acta Mech. Sin.* 42：并行 + Matrix-Free 子结构形式；高性能终局、能力 A⊗B 的方法依据。
