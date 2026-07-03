---
title: "Explicit three dimensional topology optimization via Moving Morphable Void (MMV) approach"
authors:
  - Zhang, Weisheng
  - Chen, Jishun
  - Zhu, Xuefeng
  - Zhou, Jianhua
  - Guo, Xu
year: 2017
journal: "Computer Methods in Applied Mechanics and Engineering"
volume: 322
pages: "590-614"
doi: "10.1016/j.cma.2017.07.031"
zotero_key: "M3GVBM67"
zotero_citation_key: "zhangExplicitThreeDimensional2017"
tags:
  - MMV
  - topology-opt
  - 3D
status: "done"
rating: 4
date_added: "2026-07-03"
date_read: "2026-07-03"
---

# Explicit three dimensional topology optimization via Moving Morphable Void (MMV) approach

> **引用**：Zhang, Weisheng, et al. *Computer Methods in Applied Mechanics and Engineering*, 2017. 
> **完整中文译文**：[[translations/Zhang2017-MMV-3D-zh]]
> **Zotero/Better BibTeX key**：`zhangExplicitThreeDimensional2017`
> **阅读状态**：精读已完成。

## 一句话概括

提出了一种基于移动可变形空洞 (Moving Morphable Voids, MMV) 的三维 (3D) 显式拓扑优化方法，通过控制少量几何参数显式演化空洞区域，并结合有效的自由度移除技术，大幅降低了 3D 拓扑优化中庞大的设计变量数量和有限元分析的计算成本，且彻底消除了灰度单元。

## 研究问题

在传统的三维拓扑优化（如变密度法 SIMP、水平集方法 LSM 等）中，有限元分析的自由度 (DOFs) 和与优化相关的设计变量数量通常随网格分辨率呈三次方增长，极易达到百万级别，导致极其庞大的计算开销（常常被描述为“维度灾难”）。虽然近期发展了以组件为构建块的移动可变形组件 (MMC) 方法来减少设计变量，但 3D 组件的描述、重叠处理与相交运算非常复杂。本文的动机在于开发一种更高效、稳健的 3D 拓扑优化方法。

## 方法

采用 **Moving Morphable Voids (MMV)** 方法作为核心思路。相较于“添加组件 (MMC)”，该方法是通过在实体域中“挖除”和移动一系列参数化控制的空洞 (Voids) 来演化出最优拓扑。

### 关键假设与几何描述

1. **结构表达**：最优材料分布由设计域减去一组封闭的三维空洞曲面包围的区域所决定。
2. **拓扑描述函数 (TDF)**：通过构建 TDF，将结构的拓扑变化显式映射到固定的有限元网格（Ersatz 材料模型）上。
3. **参数化插值**：提出了通过中心点、径向距离、经纬度角定义的星形/非星形区域几何描述。利用 **Hermite 插值**或 **NURBS 插值**方案，可以用极少数的控制变量来显式定义复杂的三维空洞形状。

### 技术细节：自由度 (DOF) 移除技术

由于优化模型（几何控制）和分析模型（固定网格 FEA）完全解耦，并且空洞区域的力学性能被惩罚为极小值（类似 Ersatz 模型），因此可以实现**有效的节点自由度 (DOF) 移除**：
- 在每次分析前，将完全位于空洞内部且不承受外部载荷/非固定边界的节点的 DOF 从整体刚度矩阵中剔除。
- 这一处理直接降低了每次 FEA 求解方程组的维数，且由于 3D 空洞体积较大，移除的自由度比例极高，FEA 计算效率获得了近一至两个数量级的提升。

## 实验 / 数值验证

分别采用 Hermite 和 NURBS 几何描述方案对多个基准算例进行了测试：

| 算例 | 指标/考察点 | 本文结果 |
|------|------|----------|
| **短悬臂梁 (Short cantilever beam)** | 优化结果差异、FEA 耗时 | Hermite 与 NURBS 均能有效求解，优化后刚度相近。使用 DOF 移除技术后，FEA 单步求解耗时可缩短一半以上。 |
| **L 形椅 (L-bracket/chair)** | 复杂边界与几何约束、棋盘格现象 | 算法能够自然地抑制棋盘格和网格依赖现象，无须额外的启发式过滤或人工参数调优。 |
| **扭转梁 (Twisting beam)** | 复杂 3D 传力路径，MMV vs MMC | 与 MMC 方法对比，两者均得到类似圆柱壳的网格结构；MMC 构建传力路径效率高（前十步），MMV 在后期的收敛更加稳健，且均是完美的纯黑白结构。 |

## 主要结论

1. 成功将 MMV 方法推广至 3D 拓扑优化。
2. **极大减少了设计变量数量**，比基于网格的传统方法少了 2~3 个数量级（例如将一百万个变量减少到几百、几千个）。
3. 结合 DOF 移除技术，**显著提升了 FEA 分析效率**（特别是当允许材料体积分数较小或空洞较多时）。
4. 优化结构几何边界明确，从根本上消除了 3D 拓扑优化中难以避免的**灰色单元**现象。

## 优点与局限

**优点：**
- **计算效率高**：设计变量少，配合 DOF 移除，极大缓解了 3D 优化的维度灾难。
- **优化结果清晰**：纯黑白结构（0-1 惩罚），后处理方便，可直接对接 CAD。
- **几何表达解耦**：拓扑和形状的分辨率独立于有限元网格分辨率。

**局限：**
- 本文中的实现和时间对比均基于单核计算环境，在现代多核并行环境下的效率优势和扩展性需要进一步研究。
- 求解极为复杂的精细点阵结构时，可能需要引入数量极为庞大的初始空洞。

## 对我研究的启发

- **自由度缩减思想**：这种“优化与分析解耦 -> 预先剔除无效节点 DOF -> 稀疏求解”的工程技巧，在涉及等几何分析 (IGA)、无网格法甚至 BEM 的分析中，也是非常直接且值得借鉴的计算提速手段。
- **显式描述的价值**：NURBS 和 Hermite 描述 3D 形状带来的参数控制自由度使得从拓扑结果逆向恢复 CAD 模型更加容易，这对面向制造的拓扑优化有巨大的工程意义。

## 相关文献

- **MMC 原始文献**：Guo, X., Zhang, W., & Zhong, W. (2014). Doing topology optimization explicitly and geometrically—a new moving morphable components based framework. *Journal of Applied Mechanics*, 81(8).
- **MMV 的 2D 先导文献**：Zhang, W., Zhong, W., & Guo, X. (2015). Explicit topology optimization of structural and multiphysics systems via Moving Morphable Void (MMV) approach. *CMAME*, 290, 290-316.

## 附注

- **公式附录**：详细记录了 Hermite 和 NURBS 方案下目标函数对几何控制变量的具体求导公式，由于公式复杂且较多，已全文收录至 [[translations/Zhang2017-MMV-3D-zh]] 中的附录部分。
