---
title: "A new topology optimization approach based on moving morphable components (MMC) and the ersatz material model"
authors:
  - Zhang, Weisheng
  - Yuan, Jie
  - Zhang, Jian
  - Guo, Xu
year: 2016
journal: "Structural and Multidisciplinary Optimization"
volume: 53
pages: "1243-1260"
doi: "10.1007/s00158-015-1372-3"
zotero_key: "QLN8ZLGS"
zotero_citation_key: "zhangNewTopologyOptimization2016"
tags:
  - MMC
  - topology-opt
  - ersatz-material
status: "draft"
rating: 0
date_added: "2026-04-24"
date_read: "2026-07-03"
---

# A new topology optimization approach based on moving morphable components (MMC) and the ersatz material model

> **引用**：Zhang, Weisheng, et al. *Structural and Multidisciplinary Optimization*, 2016. [DOI](https://doi.org/10.1007/s00158-015-1372-3) 
> **完整中文译文**：[[translations/Zhang2016-MMC-topology-zh]]
> **Zotero/Better BibTeX key**：`zhangNewTopologyOptimization2016`
> **阅读状态**：已完成精读与全文翻译，附 188 行核心 Matlab 代码解析。

## 一句话概括

提出了一种基于移动可变形组件 (MMC) 和替代材料 (Ersatz Material) 模型的新型显式拓扑优化方法，能够利用极少的设计变量实现变厚度组件的高效优化。

## 研究问题

**动机与痛点：**
传统的拓扑优化方法（如 SIMP、水平集等）以“隐式”方式进行拓扑优化，存在几个潜在问题：
1. 难以精确控制结构特征尺寸（因为隐式模型未嵌入显式几何信息）；
2. 隐式拓扑优化的设计变量数量过于庞大，且随有限元网格分辨率增加而剧增；
3. 分析模型和优化模型强耦合，容易引发严重的数值问题（如棋盘格图案、局部振动/屈曲模式）。
虽然早期已提出基于 MMC 的框架 (Guo 等 2014a)，但它需要基于 XFEM 对网格进行子剖分（增加计算开销），并且只允许均匀厚度的组件。本文旨在解决这些弱点。

## 方法

基于 **移动可变形组件 (MMC)** 框架和 **替代材料模型 (ersatz material model)**，以显式的几何化方式执行拓扑优化。

### 核心机制
- **显式几何描述**：整个结构的拓扑由一组可重叠的组件构成，每个组件通过一个显式的拓扑描述函数 (TDF) 表示。
- **可变厚度组件**：在 TDF 中引入更高级的解析式，使得组件的宽度（厚度）可以通过二次函数 (由端点及中间的几个参数 $t_1, t_2, t_3$ 控制) 发生变化，极大地提高了 MMC 的几何建模能力。
- **替代材料模型 FEA**：摒弃复杂的 XFEM，使用经典的 Ersatz Material 模型。根据单元节点上的 TDF 值，利用正则化的 Heaviside 函数直接进行杨氏模量插值（平滑），从而大幅度提升有限元分析和整体计算效率。
- **解析/半解析敏度**：伴随法敏度推导中，为了提升通用性，采用了非常高效的有限差分商来近似组件参数的导数，数值表现极佳。

## 实验 / 数值验证

论文在二维及三维情况下测试了几个经典的柔度最小化基准算例：
1. 短梁问题 (Short Beam)
2. MBB 梁问题
3. 桥梁设计算例
4. 柔性机构问题 (Compliant Mechanism)
5. 3D 短梁问题的扩展尝试

**对比结论**：
相比于传统基于密度的拓扑优化，该方法的设计变量显著减少，并且**与有限元网格的分辨率完全独立**。
例如 3D 算例中，即便使用 40×20×4 (3200 单元) 或加密到 25600 单元的网格，MMC 方法中的设计变量都始终保持 **162 个** (18个组件 × 9个参数)。

## 优点与局限

**优点：**
- **设计变量极少**，有效降维，优化问题本身更加适定。
- **无网格依赖性**（Mesh-independence），不需要传统方法中复杂的灵敏度过滤技术。
- 最终结构边界光滑，没有灰度单元过度问题，不会出现“单点铰链”现象。
- 提供了简洁、复现性强的 188 行 Matlab 开源教学代码。

**局限：**
- 对重叠 (Overlapping) 和组件完全消除的惩罚或机制完全依赖于优化器自适应。
- 对极度复杂拓扑的探索能力一定程度上受限于初始组件的数量和分布（需要给定合理的初始组件数）。

## 对我研究的启发

- Ersatz 材料模型和 MMC 的结合非常优雅，它在保留了显式几何描述优势的同时，享受了基于网格进行刚度装配的极速效率。
- 可变厚度的 TDF 定义 (利用二次函数描述横截面变化) 提供了一种高自由度的特征描述方式，在后续研究（如多尺度结构、物理驱动机器学习）的参数化降维中，具有极高的参考价值。

## 附注

论文中提供了对应于短梁算例的 188 行 Matlab 完整代码。代码结构高度致敬经典的 Sigmund 99 行代码 (2001) 以及 Andreassen 88 行代码 (2011)，采用 MMA 优化算法驱动。代码及注释的完整中文翻译见译文页面。
