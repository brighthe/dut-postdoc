---
title: "翻译：PIML-OFEM: A New Large-Scale Structural Analysis Method Based on Problem-Independent Machine Learning and Overlapping Finite Element Technique"
aliases:
  - guoPIMLOFEMNewLargeScale2026-zh
status: draft
date_created: 2026-08-04
date_updated: 2026-08-04
source: "[[../notes/Guo2026-PIML-OFEM]]"
citekey: "guoPIMLOFEMNewLargeScale2026"
language: "zh-CN"
---

# PIML-OFEM: A New Large-Scale Structural Analysis Method Based on Problem-Independent Machine Learning and Overlapping Finite Element Technique

## 中文译文（未完成）

> 原笔记：[[../notes/Guo2026-PIML-OFEM]]
> Zotero 条目：父条目 key 待补
> PDF 附件：`zotero://open-pdf/library/items/JVG2F9WE`
> 证据等级：arXiv v1 预印本，不作为已正式发表期刊论文表述。
> 说明：本页当前仅建立与原文一致的章节框架；所有正文、公式、图表和图注均待逐节翻译与核验。

---

# 0 元数据

- **题名**：PIML-OFEM: A New Large-Scale Structural Analysis Method Based on Problem-Independent Machine Learning and Overlapping Finite Element Technique
- **中文暂译**：PIML-OFEM：一种基于问题无关机器学习与重叠有限元技术的大规模结构分析新方法
- **作者**：Yilin Guo；Chang Liu；Zongliang Du；Jin Liu；Jingyu Feng；Xinyang Zhang；Yang Li；Tianxing Yang；Changyu Shen；Xu Guo
- **来源**：arXiv.org
- **版本**：arXiv:2607.22019v1
- **提交日期**：2026-07-24
- **Better BibTeX key**：`guoPIMLOFEMNewLargeScale2026`
- **Zotero item key**：待补
- **PDF attachment key**：`JVG2F9WE`
- **译文状态**：仅建立框架，正文尚未开始翻译

# 摘要

高分辨率结构分析与大规模异质结构的快速设计既需要精确的降阶模型，也需要高效的在线计算。在传统多尺度有限元框架下，针对不同材料分布在线构造多尺度形函数会产生难以承受的计算开销；与此同时，既有基于子结构的问题无关机器学习（PIML）方法，其分析精度通常受到子结构边界位移分布预设形式的限制。为解决上述问题，本文提出 PIML-OFEM，即一种由问题无关机器学习加速的重叠有限元方法。

该方法仅保留各子结构角节点的自由度，并通过在扩展域上求解局部边值问题，构造与这些自由度对应的数值基函数。这种降阶建模方法无需预设目标子结构边界上的位移分布，显著增强了数值基函数复现子结构局部变形的能力。进一步引入基于分片统一的重叠有限元格式，将相互独立构造的数值基函数插值为全局连续的基函数。

为避免在线求解数值基函数，本文训练 U-Net 学习子结构内部杨氏模量分布到数值基函数之间的确定性映射。由于该学习过程不依赖具体载荷条件或边界条件，所得数值基函数可以复用于同类结构分析与优化问题。数值算例表明，PIML-OFEM 得到的位移和单元应变能与细尺度有限元结果高度一致；其在线计算成本显著低于直接有限元分析，计算精度也明显优于采用线性边界插值的 PIML 方法。

将其嵌入拓扑优化框架后，PIML-OFEM 能够支持采用较小过滤半径的高分辨率优化，并保留细尺度结构特征，包括局部类似秩-2 微结构的构型。通过融合基于力学原理的局部独立降阶、全局连续耦合与问题无关机器学习，PIML-OFEM 为大规模异质结构分析和高分辨率拓扑优化建立了一种高效的 AI 增强计算范式。

# 1 引言

> 待翻译。

# 2 基于超采样数值基函数的子结构降阶建模

> 待翻译。

## 2.1 经典子结构静力缩聚方法

> 待翻译。

## 2.2 超采样数值基函数的构造与边界处理

> 待翻译。

# 3 基于分片统一方法的重叠有限元位移协调方法

> 待翻译。

## 3.1 子结构的重叠覆盖与细尺度网格构造

> 待翻译。

## 3.2 基于重叠有限元的位移协调

> 待翻译。

## 3.3 超采样降阶映射与重叠有限元的耦合

> 待翻译。

# 4 使用 U-Net 快速预测超采样数值基函数

> 待翻译。

## 4.1 U-Net 网络结构

> 待翻译。

## 4.2 训练数据与损失函数

> 待翻译。

## 4.3 训练结果

> 待翻译。

## 4.4 在线预测与计算流程

> 待翻译。

# 5 数值算例

> 待翻译。

## 5.1 误差指标

> 待翻译。

## 5.2 悬臂梁算例

> 待翻译。

## 5.3 复杂孔洞拓扑算例

> 待翻译。

## 5.4 拓扑优化算例

> 待翻译。

# 6 结论

> 待翻译。

# 致谢

> 待翻译。

# 参考文献

> 待核对原文引用，不翻译文献题名。

# 译后检查清单

- [ ] 摘要、正文、附录及必要的致谢均已处理。
- [ ] 公式内容、编号与 LaTeX 环境已对照 PDF 核验。
- [ ] 图片、表格、图注及本地资产均已检查。
- [ ] 脚注、引用、链接和 Markdown 结构静态检查通过。
- [ ] 原笔记及必要关联页面已同步。
