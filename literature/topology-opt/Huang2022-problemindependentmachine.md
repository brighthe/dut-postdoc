---
title: Problem-independent machine learning (PIML)-based topology optimization—A universal approach
authors:
  - Huang, Mengcheng
  - Du, Zongliang
  - Liu, Chang
  - Zheng, Yonggang
  - Cui, Tianchen
  - Mei, Yue
  - Li, Xiao
  - Zhang, Xiaoyu
  - Guo, Xu
year: 2022
journal: "Extreme Mechanics Letters"
doi: "10.1016/j.eml.2022.101887"
tags:
  - PIML
  - topology-opt
  - EMsFEM
  - machine-learning
  - multiscale-FEM
status: done
rating: 5
date_added: 2026-06-04
date_read: 2026-06-04
---

# Problem-independent machine learning (PIML)-based topology optimization—A universal approach

> **引用**：Huang, Mengcheng; Du, Zongliang; Liu, Chang; Zheng, Yonggang; Cui, Tianchen; Mei, Yue; Li, Xiao; Zhang, Xiaoyu; Guo, Xu. *Extreme Mechanics Letters*, 2022. [DOI](https://doi.org/10.1016/j.eml.2022.101887) | [Zotero Link](zotero://select/library/items/TSLB5VAR)
> **完整中文译文**：[[translations/Huang2022-problemindependentmachine-zh]]

## 一句话概括

在 EMsFEM 框架下，离线训练神经网络学习粗分辨率单元形函数与局部材料密度之间的映射，从而构造真正"问题无关"的机器学习模型，显著降低大规模拓扑优化中有限元分析的计算开销。

## 研究问题

拓扑优化的主要计算瓶颈是每轮迭代的有限元分析（FEA）。已有 ML 加速方法存在三个缺陷：
1. 训练数据依赖特定边界条件/载荷，**非真正问题无关**
2. 局部依赖假设的理论合理性存疑
3. 粗分辨率单元尺寸受限，加速比有限

本文目标：以统一方式解决上述三个问题。

## 方法

### 核心思路

将 EMsFEM（扩展多尺度有限元法）引入拓扑优化框架，并用离线训练的神经网络替代每步迭代中耗时的形函数在线构造。

### 物理先验与网络架构

* **PIML 的"问题无关性"来源**：所学习的 EMsFEM 形函数本质上是底层控制 PDE 对应 Green 函数的离散版本，与宏观边界条件、设计域、外载荷**完全无关**，仅由粗单元内部局部材料密度决定。
* **拓扑优化问题设置（SIMP + 密度过滤）**：
  $$
  \min_{\boldsymbol{\rho},\boldsymbol{U}}\ C = \boldsymbol{U}^T\boldsymbol{K}\boldsymbol{U},\quad \text{s.t.}\ \boldsymbol{K}\boldsymbol{U}=\boldsymbol{F},\ V/V_0 \leq f,\ 0\leq\rho_e\leq 1
  $$
  材料插值：$E_e(\rho_e)=E_{\min}+\rho_e^p(E_0-E_{\min})$，惩罚参数 $p=3$。
  密度过滤：$\tilde{\rho}_e = \frac{\sum_{i\in N_e}H_{ei}\rho_i}{\sum_{i\in N_e}H_{ei}}$，$H_{ei}=\max(0,r_{\min}-d(i,e))$
* **EMsFEM 框架**：两级网格（粗/细）。多尺度形函数 $N_{ixx}^l, N_{ixy}^l, N_{iyx}^l, N_{iyy}^l$ 将粗节点位移映射到细网格节点位移：
  $$
  \boldsymbol{K}^E = \sum_{f=1}^{m} (\boldsymbol{N}_f)^T \boldsymbol{k}^f \boldsymbol{N}_f
  $$
  满足分区单位分解条件。
* **ANN 构造与训练**：
  - **输入**：粗单元内 $m$ 个细单元的密度值（$m=25$ 或 $m=100$）
  - **输出**：12 个独立形函数分量的节点值
  - **训练数据**：随机生成局部密度，无需求解任何拓扑优化问题
  - **损失函数**：预测形函数与精确形函数的 MSE + **预测刚度矩阵与精确刚度矩阵的 MSE**（物理约束项，关键！）
  - **网络结构**（$m=100$）：11 个隐层，激活函数交替 `tanh/elu`，每层宽度 100→200→100
  - **优化器**：Adam，学习率 0.001

### 算法降维与加速来源

* **在线求解流程加速**：
  1. EMsFEM 将全局方程组维度从 $O(n)$ 降至 $O(n/L)$，求解复杂度从 $O(n^3)$ 降至 $O((n/L)^3)$。
  2. ANN 前向推断替代耗时的形函数在线构造。
  3. 引入密度阈值 $\bar{\rho}=0.95$，$\underline{\rho}=0.002$，纯实体/弱材料单元直接查表，跳过 ANN 推断。

## 实验 / 数值验证

### 算例规模与扩展性

* **MBB 梁（超大规模）**：达到 **2亿** 细单元级别（$2000\times1000$ 粗网格，每粗单元含 $10\times10$ 细单元），仅需个人工作站即可求解，单步 FEA 约 2 分钟，FEA 时间降低约 2 个数量级。
* **短悬臂梁与 L 型梁**：分别对不同尺度的细网格和粗/细比进行了验证。

### 精度与效率权衡

* 对比了不同粗/细比（如 $5\times5$ 和 $10\times10$）的刚度（柔顺度）精度与加速比。
* 物理约束损失项成功保证了刚度矩阵预测的高精度。

| 算例 | 细网格规模 | 粗/细比 | $C_{\text{ANN-EMs}}$ vs $C_{\text{EMs}}$ 相对误差 | 单步加速比 |
|------|-----------|---------|--------------------------------------------------|-----------|
| 短悬臂梁 | $3200\times1600$ | $5\times5$ | $3.00\times10^{-4}$ | ~4× |
| 短悬臂梁 | $3200\times1600$ | $10\times10$ | $8.72\times10^{-3}$ | ~4× |
| L 型梁 | $2000\times2000$ | $5\times5$ | $1.18\times10^{-3}$ | — |
| MBB 梁 | — | $5\times5$ | $5.21\times10^{-4}$ | ~3.3× |
| MBB 梁（超大规模） | **2亿**细单元 | $10\times10$ | — | FEA 降低~2个数量级 |

## 主要结论

- PIML 模型一次训练，可无修改地用于任意载荷/边界条件的拓扑优化问题
- 形函数具有**理论局部决定性**，其他已有方法不具备此性质
- 训练数据仅需随机密度场，不依赖任何预先求解的拓扑优化结果
- FEA 时间可降低约两个数量级；超大规模问题（2亿变量）在个人工作站上可解

## 优点与局限

**优点：**
- 真正问题无关，泛化能力强
- 训练成本极低（随机密度场即可）
- 无缝嵌入标准 SIMP 流程，改动最小
- 物理约束损失项保证刚度矩阵精度

**局限：**
- EMsFEM 采用线性边界条件，可能引入误差（可用 oversampling 改进）
- 普通全连接网络，$m=100$ 时输出维度大（972），误差略高于 $m=25$
- 设计变量更新（OC）仍占 >85% 总时间，未解决优化器瓶颈

## 对我研究的启发

- **与 MMC 结合**：论文本身已指出，将 PIML 置于 MMC 框架可进一步降低设计变量数量 1~2 个数量级，同时消除 OC 更新瓶颈——这是明确的后续方向
- **双模量扩展**：EMsFEM 形函数学习目前仅针对线弹性 PDE；若底层本构为双模量非光滑材料，需结合 PVP 变分底座改造损失函数（见 [[Guo2014-bimodulus-variational]]）
- **Data-free 改进**：损失函数第二项（刚度矩阵 MSE）仍需 FEA 标注数据；后续 data-free PIML 工作将其替换为最小势能原理，可完全消除标注依赖

## 相关文献

- [[Guo2022-MMC-review]] — MMC/MMV 综述，PIML 与显式优化结合的宏观背景
- [[Guo2023-PIML-substructure]] — 本文的子结构扩展，引入力学先验约束
- [[Guo2023-PIML-data-free]] — data-free 版本，用最小势能原理替代监督学习
- [[Guo2025-PIML-parallel]] — 128 亿变量并行扩展
