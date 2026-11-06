---
title: "翻译：Design of 3D Shell-Graded Infill Structures Based on Moving Morphable Void and Triply Periodic Minimal Surfaces"
tags:
  - translation
  - PIML
  - MMV
  - TPMS
  - shell-infill
  - lattice
  - topology-opt
status: "draft"
date_created: 2026-10-22
date_updated: 2026-10-22
source: "../sources/Cao2026-shell-graded-TPMS-MMV-PIML.pdf"
citekey: "Cao2026-shell-graded-TPMS-MMV-PIML"
language: "zh-CN"
---

# Design of 3D Shell-Graded Infill Structures Based on Moving Morphable Void and Triply Periodic Minimal Surfaces

---

# 信息

- **中文标题**：基于移动可变形空洞与三周期极小曲面的三维壳-梯度填充结构设计
- **作者**：Xianglong Cao；Wu Xu（徐武）；Shixin Zhao；Yilin Guo（郭一麟）；Chang Liu（刘畅）$^*$；Xu Guo（郭旭）（Xianglong Cao、Shixin Zhao 中文名待确认）
- **单位**：大连理工大学工程力学系、工业装备结构分析优化与 CAE 软件国家重点实验室、计算力学国际研究中心（大连 116023）
- **出版类型**：会议论文集章节。ICCES 2025（第 31 届 International Conference on Computational & Experimental Engineering and Sciences，长沙，2025-05-25 至 05-29）
- **论文集**：*Computational and Experimental Simulations in Engineering*，X. Feng 与 K. Zhou 主编，Mechanisms and Machine Science 第 201 卷，Springer Nature Switzerland（Cham），pp. 841–852
- **DOI**：10.1007/978-3-032-17313-3_64
- **在线发表**：2026-05-01（CrossRef 记录；印刷年份 2026）
- **ISBN**：978-3-032-17312-6（印刷）；978-3-032-17313-3（电子）
- **通讯作者**：Chang Liu（C.Liu@dlut.edu.cn）

> **入库说明（译者）**：本页为摘要级 `draft` 入口，只核验了题录、摘要、关键词、章节结构与结论；正文、公式与图表尚未翻译，不作为全文级证据。原文章节编号本身即为 1 引言（含 1.1–1.4 方法与算例）与 2 结论，本页照录。致谢与基金信息未在原文中出现。本文是 [[Xu2025-PIML-lattice-MMC-zh|Xu 2025]] 点阵路线的会议扩展：外壳由 MMV 显式描述，填充由 TPMS 函数经分区坐标映射（PCM）生成梯度点阵并以 NURBS 基函数保证相邻微结构的光滑过渡，PIML 用于加速全尺度点阵分析；仅给出一个数值算例。

# 摘要

三维壳-多孔结构因其优异的力学性能与轻量化特点，被广泛应用于航空航天、先进制造与生物医学工程。本文提出一种三维壳-梯度多孔结构的拓扑优化框架，将三周期极小曲面（TPMS）与移动可变形空洞（MMV）方法相结合，并辅以问题无关机器学习（PIML）提高优化效率。MMV 方法用于显式定义宏观拓扑，便于直接生成边界明确的壳结构并免去后处理。引入分区坐标映射（PCM）机制，利用 TPMS 函数构造空间梯度变化的填充结构，并通过非均匀有理 B 样条（NURBS）基函数的高阶连续性保证相邻微结构之间的光滑几何过渡。为克服复杂点阵结构全尺度分析的计算挑战，采用 PIML 框架加速结构优化过程。通过一个数值算例验证了所提方法的有效性。

**关键词**：拓扑优化（Topology Optimization）；壳-填充（Shell-infill）；梯度点阵（Graded Lattice）；问题无关机器学习（Problem-Independent Machine Learning）；三周期极小曲面（Triply Periodic Minimal Surface）；分区坐标映射（Partitioned Coordinate Mapping）

# 1 引言

> 待翻译。

## 1.1 方法

> 待翻译。

## 1.2 三维 MMV 方法

> 待翻译。

## 1.3 壳-梯度填充结构的几何描述

> 待翻译。

## 1.4 问题列式与数值实现

> 待翻译。

### 1.4.1 数值算例

> 待翻译。

# 2 结论与贡献

本文提出了一种带梯度点阵填充的三维壳结构拓扑优化框架。该框架集成了三周期极小曲面（TPMS）、坐标扰动技术与移动可变形空洞（MMV）拓扑优化方法。MMV 方法借助精确的数学描述直接生成边界明确的宏观壳结构，免去了传统方法中复杂的后处理。TPMS 用于设计具有特定几何特征的点阵填充结构，分区坐标映射（PCM）技术用于精确优化点阵单胞的形状与尺寸，以灵活适应多样的设计需求。针对复杂点阵结构全尺度分析的高计算成本，框架引入基于问题无关机器学习（PIML）的策略以提高计算效率。数值算例表明了所提框架的有效性：优化得到的壳-梯度点阵结构具有清晰的边界、高效的传力路径以及可定制梯度特性的点阵填充，展现出在先进设计与制造应用中的显著潜力。

---

# 参考文献

> 待转录（原文 15 条，摘要级入库阶段未逐条转录）。
