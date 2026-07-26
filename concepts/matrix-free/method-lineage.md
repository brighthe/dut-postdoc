---
title: "郭旭老师团队 Matrix-Free 方法谱系"
type: concept
aliases:
  - Matrix-Free method lineage
  - 郭旭团队 Matrix-Free 方法演进
tags:
  - matrix-free
  - method-lineage
  - PIML
  - substructure
  - topology-opt
status: draft
date_added: 2026-07-26
date_update: 2026-07-26
---

# 郭旭老师团队 Matrix-Free 方法谱系

> **一句话**：截至 2026-07-26，当前公开且可核实的直接节点只有 Ma2026；其 `matrix-free` 指多尺度形函数按需预测和释放，粗网格全局缩聚矩阵仍然形成并组装，因此尚不是全局算子级 Matrix-Free。

## 1. 范围与纳入标准

本页长期记录郭旭老师团队公开 Matrix-Free 相关成果如何演进。正式时间线只纳入满足以下条件之一、且能核对具体技术对象的成果：

- 正式论文或可公开核实的预印本；
- 已公开专利；
- 具有公开说明和可核实技术边界的软件成果。

仅在标题、摘要或实现说明中出现 `matrix-free` 还不够；必须进一步回答：

1. 没有形成或没有长期保存的对象是什么；
2. Krylov 中的 MatVec 使用什么数据；
3. 全局、局部和预条件矩阵分别是否形成；
4. 按 [[assembly-levels]] 应归入哪一级。

团队内部设想、尚未公开结果和本人的后续计划不进入正式时间线。

## 2. 与 PIML 方法谱系的关系

Ma2026 首先属于郭旭老师团队的 PIML 演进：

```text
EMsFEM 形函数学习
  → 子结构形函数 / 缩聚刚度学习
  → mechanics-based data-free
  → 并行 PIML 与多尺度形函数按需预测 / 释放
```

完整的前序论文关系见 [[../piml/method-lineage]]。Huang2022—Huang2024 构成 PIML 和子结构方法基础，但当前没有足够证据将其作为独立的 Matrix-Free 节点重复登记。

## 3. 当前时间线

| 时间 | 代表成果 | Matrix-Free 对象 | 全局算子定位 | 证据状态 |
|---|---|---|---|---|
| 2026 | [[../../literature/topology-opt/Ma2026-highperformanceparallel]] | 多尺度形函数 $\mathbf N^j$ 按需预测、使用后释放 | 粗网格全局缩聚矩阵仍形成和组装，属于第 1 级 FA/TA | 已核实 |

当前只有一个正式节点，不能据此表述为团队已经形成了完整、连续的算子级 Matrix-Free 路线。

## 4. Ma2026：多尺度形函数按需预测与释放

### 4.1 计算过程

对子结构 $j$，PIML 预测多尺度形函数 $\mathbf N^j$，并据此形成缩聚刚度

$$
\mathbf K_s^j
=
(\mathbf N^j)^{\mathrm T}
\mathbf K^j
\mathbf N^j.
$$

并行实现采用以下时间—空间权衡：

```text
PIML 预测 N^j
  → 形成 K_s^j
  → 释放 N^j
  → 组装并求解全局粗网格缩聚系统
  → 再次预测 N^j
  → 恢复细网格位移并计算灵敏度
```

不长期保存全部 $\mathbf N^j$，避免了多尺度形函数随问题规模增长造成的内存压力；代价是至少增加一次 PIML 推理。

### 4.2 仍然形成和保存的对象

- 每个子结构的缩聚刚度 $\mathbf K_s^j$ 会显式形成；
- 各子结构贡献会组装成粗网格全局缩聚矩阵；
- PETSc 的多重网格预处理 GMRES 在该组装系统上求解；
- 论文实现不是通过即时局部作用完成 $y=\mathbf K_s x$。

### 4.3 按五级分类的定位

Ma2026 的粗网格线性求解属于第 1 级 FA/TA，而不是 EA、PA 或 UA。论文所称 `matrix-free` 是对辅助数据 $\mathbf N^j$ 的按需重计算和存储规避，与“全局算子在 MatVec 时保存到哪一层”是两个正交维度。

因此，准确表述是：

> Ma2026 实现了多尺度形函数存储层面的 Matrix-Free-inspired 优化；尚未实现全局缩聚算子级 Matrix-Free。

## 5. 方法演进的长期观察维度

后续出现新成果时，统一按以下维度追加和比较：

| 维度 | 需要回答的问题 |
|---|---|
| Matrix-Free 对象 | 省略的是形函数、单元矩阵、积分点数据还是全局矩阵？ |
| 算子层级 | FA/TA、LA、EA/EbE、PA/QA 或 UA/NONE？ |
| 局部表示 | 使用精确 $\mathbf K_s^j$、预测 $\widehat{\mathbf K}_s^j$，还是即时积分点作用？ |
| 全局求解 | Krylov、真残差和预条件是否形成闭环？ |
| 并行与硬件 | CPU、MPI、GPU、多 GPU 或 GPU-aware MPI 覆盖到哪一层？ |
| 证据 | 是否给出正确性、收敛性、内存和端到端性能口径？ |

## 6. 当前尚未由公开成果闭合的环节

截至 2026-07-26，在当前已核实的团队公开成果中，尚未确认以下环节已经闭合：

- 不组装全局缩聚矩阵、直接执行 $y=\mathbf K_s x$ 的算子级 Matrix-Free；
- Matrix-Free 主算子与可扩展预条件器的系统组合；
- 面向该算子的 GPU kernel、端到端 GPU 求解和多 GPU 扩展；
- GPU-aware MPI 及跨节点正确性、收敛性和性能验证。

这些是公开成果谱系中的当前空白，不等于团队内部不存在尚未公开的研究。

## 7. 更新规则

- 新成果先建立或更新对应 `literature/` 笔记，再从本页引用，不在谱系页复制完整论文内容。
- 每个节点必须同时记录“贡献”和“仍然形成的矩阵”，避免仅凭作者术语判断装配层级。
- 预印本、专利或软件成果必须标明证据类型；未经公开来源核实的内容不得标为完成。
- 本人的研究任务、实施顺序和验收门禁只更新 [[../../research/technical-lines/matrix-free-research-guide]]。

## 8. 来源与证据

- [[../../literature/topology-opt/Ma2026-highperformanceparallel]] — 论文事实、算法流程、实验结果与边界。
- [Ma et al., 2026, Acta Mechanica Sinica](https://doi.org/10.1007/s10409-025-25942-x) — 出版社 DOI 入口。
- [[../piml/method-lineage]] — PIML 的前序方法谱系。
- [[assembly-levels]] — 五级装配层次及跨框架判定口径。

## 9. 相关页面

- [[_index]] — Matrix-Free 子知识库入口。
- [[../../research/technical-lines/matrix-free-research-guide]] — 当前能力、目标差距、实施路线与阶段门禁。
- [[../../entities/guo-xu-team]] — 郭旭老师团队实体页。
