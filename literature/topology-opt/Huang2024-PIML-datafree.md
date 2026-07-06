---
title: A mechanics-based data-free problem independent machine learning (PIML) model for large-scale structural analysis and design optimization
authors:
  - Huang, Mengcheng
  - Liu, Chang
  - Guo, Yilin
  - Zhang, Linfeng
  - Du, Zongliang
  - Guo, Xu
year: 2024
journal: Journal of the Mechanics and Physics of Solids
volume: 193
article: 105893
doi: 10.1016/j.jmps.2024.105893
zotero_key: CGQZ2HXL
zotero_citation_key: Huang2024-mechanicsbaseddatafree
tags:
  - PIML
  - topology-opt
  - data-free
  - mechanics-based-loss
  - operator-learning
  - large-scale
status: done
rating:
date_added: 2026-07-05
date_read: 2026-07-06
---

# A mechanics-based data-free problem independent machine learning (PIML) model for large-scale structural analysis and design optimization

> **引用**：Huang, Mengcheng; Liu, Chang; Guo, Yilin; Zhang, Linfeng; Du, Zongliang; Guo, Xu. *Journal of the Mechanics and Physics of Solids*, 2024, 193:105893. [DOI](https://doi.org/10.1016/j.jmps.2024.105893) | [Zotero Link](zotero://select/library/items/CGQZ2HXL)
> **中文译文框架**：[[translations/Huang2024-PIML-datafree-zh]]
> **Zotero/Better BibTeX key**：`Huang2024-mechanicsbaseddatafree`

## 一句话概括

在 Huang 2022 的监督式 EMsFEM 形函数学习与 Huang 2023 的子结构 PIML 框架之后，本文进一步用基于力学原理的 data-free 训练目标替代显式监督标签，以降低局部真值样本生成成本，并增强 PIML 局部力学映射的物理一致性。

## 研究问题

PIML 的基本思想是学习局部材料分布到局部力学表示之间的问题无关映射，但 Huang 2022/2023 仍依赖局部 FEA/EMsFEM/子结构缩聚真值作为监督标签。对于更大规模、更复杂的结构分析和设计优化问题，标签生成成本、网络输出物理一致性和跨问题复用能力仍是核心挑战。

本文关注的问题：

1. 如何在不预先生成大规模监督标签的情况下训练 PIML 模型；
2. 如何把线弹性力学原理直接嵌入力学损失函数；
3. 如何在大规模结构分析与设计优化中保持 PIML 的问题无关性和可复用性。

## 方法

### 核心思路

本文把子结构的多尺度形函数（描述粗网格自由度 → 全部自由度的映射）从离散矩阵升级为**坐标的连续函数**，用**深度算子网络 DeepONet**（分支网络编码材料密度分布、主干网络编码坐标，两者逐元素相乘）来预测。训练不再依赖监督标签，而是把若干子结构拼成一个"**伪结构（pseudo structure）**"，以其**总应变能（最小势能原理）**作为 data-free 损失函数（式 15），用自动微分 + Adam 做无监督训练。详细中文译文见 [[translations/Huang2024-PIML-datafree-zh]]。

### 学习对象

- **网络输入**：子结构内各细网格中心的单元密度（或杨氏模量）分布 $\boldsymbol\rho$，以及内部节点坐标 $(x,y,z)$；
- **网络输出**：该坐标处的（缩减）连续多尺度形函数 $\tilde{\boldsymbol N}^j_{sR}$；完整多尺度形函数由式 (11) 的**刚体运动物理约束**复现，再经式 (9) 得缩聚刚度矩阵；
- **与 Huang 2023 的继承**：仍是子结构多尺度形函数路线，但把"离散形函数矩阵"升级为"坐标连续函数 + 算子学习"，输出维度大幅下降，可用于**任意尺寸**子结构（同一网络架构）；
- **operator learning**：即 DeepONet（Lu et al. 2021），branch/trunk 双子网络。

### 力学型 data-free 损失

- **来自最小势能原理**：仅位移边界条件下，第 $j$ 个子结构的势能只剩应变能（式 12）；以多尺度形函数为设计变量改写为式 (13)，其最小值恰对应精确多尺度形函数；
- **推广到伪结构**：损失 = 由 $N$ 个子结构组成的伪结构的全部细网格单元应变能之和（式 15），**无需组装全局刚度矩阵、无需任何多尺度形函数真值标签**；
- **消除的监督**：相比 Huang 2022/2023 的"形函数 MSE + 刚度矩阵 MSE"监督损失，完全消除监督标签；仅需随机密度场 + 预存正交位移基（$11\times11\times6\times3=2178$ 个归一化向量），训练时 $\boldsymbol u_v$ 每步变化以避免陷入局部极小。

### 与前序 PIML 的关系

| 文献 | 学习对象 | 训练方式 | 主要推进 |
|---|---|---|---|
| [[Huang2022-problemindependentmachine]] | EMsFEM 形函数 | 监督式，依赖局部 EMsFEM 真值 | 提出问题无关 PIML |
| [[Huang2023-PIML-substructure]] | 子结构形函数 / 缩聚刚度矩阵 | 监督式，依赖局部缩聚真值 | 推进到子结构缩聚框架 |
| 本文 | 连续多尺度形函数（DeepONet 算子） | mechanics-based data-free（伪结构应变能，无监督） | 任意尺寸子结构、消除标签成本、增强物理一致性 |

## 实验 / 数值验证

三个三维算例（基材 $E_0=1,\ \nu=0.3,\ E_{\min}=10^{-7}$；统一用 $m=10$ 子结构；OC 更新设计变量）：

- **悬臂梁**：PIML 与 EMsFEM/全尺度位移场接近（相对误差约 6%）；用 $50\times25\times25$ 子结构时柔顺性相对全尺度误差降至 4.7%，结构分析提速约 **87 倍**；无监督模型精度**优于**监督式，且几乎不见过拟合；
- **三维扭转箱**：研究过滤半径影响；因多尺度形函数比一阶有限元更灵活，过滤半径可**小于**子结构尺寸（甚至 0.4 倍）而不出 QR 花纹（多分辨率方法做不到）；1152 万单元时每步提速 **>230 倍**，可解至 **1.8 亿单元**（全尺度已超内存）；
- **三维柔顺机构**：非自伴随问题，PIML 输出位移与 EMsFEM 接近，验证对非自伴随优化的有效性。

训练成本：$10\times10\times10$ 子结构的无监督模型约 **2–3 天**（与监督式接近，但省去生成数据集的大量时间）。

## 主要结论

- 用**坐标连续化 + DeepONet 算子学习 + 基于最小势能的 data-free 损失**，实现无监督、无标签的 PIML；
- 适用于任意尺寸子结构、任意边界/载荷的大规模线弹性分析与刚度相关拓扑优化，效率较全尺度分析提升**两个数量级以上**；
- 无监督模型精度**反超**监督式（从全局能量层面学习，泛化更好，几乎不过拟合）；
- 本质推进不只是换网络结构，而是**改变训练目标与样本生成范式**（监督标签 → 力学能量损失）。

## 优点与局限

**优点：**

- 完全消除局部真值标签生成（data-free 无监督），大幅降低训练前的样本准备成本；
- 直接嵌入最小势能原理，物理一致性更强；
- 网络输出维度小，同一架构可用于任意尺寸子结构；无监督下精度反超监督式、几乎无过拟合。

**局限：**

- 立方体子结构 + 线性边界假设会高估刚度，低体积分数/粗子结构下需较大过滤半径或加密；
- 对不连通材料分布（QR 花纹）预测精度显著下降；
- 复杂几何用规则立方体子结构离散困难；超大规模串行实现仍耗时耗内存；
- 训练一次仍需约 2–3 天。
- 未来方向（原文）：高阶变形假设、等参 PIML（几何信息作额外输入）、并行 PIML、多物理场推广。

## 对我研究的启发

- **从监督标签到力学约束**：本文需要重点关注如何用力学型损失替代局部真值标签，这直接关系到 PIML 的训练成本和物理一致性。
- **与子结构路线的关系**：需确认本文是否仍沿用子结构形函数/缩聚刚度矩阵，还是转向更一般的局部算子学习。
- **与高阶/多分辨率分析的关系**：若 data-free loss 依赖能量或弱形式，它与高阶有限元、密度积分网格和多分辨率材料描述之间可能存在自然结合点。

## 待读问题（已随全文精读与翻译解决）

1. ~~原文目录与正式章节标题~~ → 已核定并译出（见 [[translations/Huang2024-PIML-datafree-zh]]）。
2. ~~data-free 损失的精确数学表达~~ → 最小势能 → 伪结构总应变能（式 12–15）。
3. ~~网络输入/输出与 Huang 2023 的差异~~ → 离散形函数矩阵 → 坐标连续函数 + DeepONet 算子，输出降维、任意尺寸。
4. ~~数值算例的规模、误差、效率数据~~ → 见上"实验/数值验证"（87× / >230× / 1.8 亿单元 / 误差约 4.7–6%）。

## 相关文献

- [[Huang2022-problemindependentmachine]] — PIML 奠基论文，EMsFEM 形函数监督学习。
- [[Huang2023-PIML-substructure]] — PIML 增强子结构形函数与缩聚刚度矩阵。
- [[Ma2026-highperformanceparallel]] — PIML 与并行计算、按需预测/释放结合。
