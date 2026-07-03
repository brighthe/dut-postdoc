# Minimum length scale control in structural topology optimization based on the moving morphable components (MMC) approach

## 完整中文译文

> 原笔记：[[../Zhang2016-minimum-length-scale]]
> Zotero 条目： zotero://select/library/items/6CKKE5R3
> PDF 附件： zotero://open-pdf/library/items/QC8BKFTX
> 说明： 本页用于放置 Zhang et al. 2016 论文的完整中文译稿。

---

# 0 元数据

* 论文：Zhang, Weisheng, et al. 2016, *Computer Methods in Applied Mechanics and Engineering*
* DOI： 10.1016/j.cma.2016.08.022
* Better BibTeX key: `zhangMinimumLengthScale2016`
* Zotero item key: `6CKKE5R3`

# 摘要
本文提出了一种在拓扑优化中以直接且显式的方式控制最小尺寸（minimum length scale）的新方法。该方法基于所谓的移动可变形组件（Moving Morphable Components, MMC）求解框架构建，在该框架下，通过在固定的有限元网格上改变一组梯形结构组件的形状和布局，即可获得优化的结构拓扑。采用扩展有限元法（eXtended Finite Element Method, XFEM）进行结构响应分析，并通过沿结构边界进行数值积分来获取形状敏度信息。基于所提出的求解框架，本文还给出了结构最小尺寸的精确定义。与现有方法相比，所提出的方法只需对一组几何设计变量设置下界，即可实现最小尺寸控制。为了获得完全的最小尺寸控制，只需显式地考虑少量施加在相交区域尺寸上的纯几何约束。数值算例验证了所提出方法的有效性。
# 1 引言
结构拓扑优化是一种旨在通过在设计域内合理分布给定数量的材料来设计创新结构的计算方法。自从 Rozvany [1]、Cheng 和 Olhoff [2]、Bendsøe 和 Kikuchi [3] 的开创性贡献以来，该方法已发展到一个相对成熟的阶段。如今，除了力学问题，拓扑优化在声学、电磁学和光学等各种物理学科中也得到了应用。关于拓扑优化最新进展的综述，请读者参阅文献 [4–7] 及其参考文献。

尽管拓扑优化已经取得了显著成就，但仍存在一些尚未得到很好解决的挑战性问题。其中之一就是如何以显式且局部的方式控制结构的最小尺寸（即结构的最小特征尺寸）[6]。一般而言，结构的最小尺寸对应于连续体结构中杆的最小横截面直径、板的最小厚度以及一组圆孔的最小半径等。

<!-- 待补充译文 -->
# 2 方法

<!-- 待补充译文 -->

# 3 结论

<!-- 待补充译文 -->
