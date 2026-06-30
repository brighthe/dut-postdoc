---
title: "面向 MMC/MMV 显式拓扑优化的高精度数值离散与高效结构分析方法研究——技术调研"
tags:
  - MMC
  - MMV
  - topology-optimization
  - numerical-discretization
  - ersatz
  - XFEM
  - IGA
  - VEM
  - PIML
  - fast-analysis
status: "draft"
date: 2026-06-07
source: "Research Report.pdf（郭旭团队技术综述，大连理工大学）"
---

# 面向 MMC/MMV 显式拓扑优化的高精度数值离散与高效结构分析方法研究

---

## 一、框架核心：分析模型与几何模型解耦

MMC（Guo, Zhang & Zhong, JAM 2014, 81(8):081009）和 MMV（Zhang et al., CMAME 2017, 322:590–614）的根本创新在于：

- **拓扑几何**：用少量几何参数（组件中心、长、厚、倾角，或样条孔洞控制点）**显式描述**；
- **结构响应**：仍在一套（通常固定的）背景有限元网格上求解。

这一"**双模型解耦**"是所有后续数值离散工作的出发点——既带来优势（设计变量极少、边界清晰、天然对接 CAD），也带来难题（如何把连续几何精确映射到离散网格）。

---

## 二、固定网格上的几何投影与数值积分（核心方案）

### 2.1 ersatz 材料模型 + 节点 TDF 投影（基础方案）

**代表作**：Zhang W, Yuan J, Zhang J, Guo X, *A new topology optimization approach based on Moving Morphable Components (MMC) and the ersatz material model*, Struct Multidisc Optim, 2016, 53(6):1243–1260（附 188 行 MATLAB 代码）。

**核心机制**：

- 采用双线性四节点四边形单元；
- 将所有组件 TDF 取并（max）得到整体结构 TDF φˢ，在每个单元的四个节点上取值；
- 经正则化 Heaviside 投影后，对四节点取平均（带惩罚指数 q）得到单元 ersatz 杨氏模量：

$$E_e = E^s \cdot \frac{1}{4}\sum_{i=1}^{4} \left[H_\varepsilon\!\left((\varphi^s)_i^e\right)\right]^q, \quad q=2$$

- 正则化 Heaviside 为三次多项式，含两个参数：
  - 过渡带半宽 ε = (2~4)·min(Δx, Δy)（与网格尺寸绑定）
  - 弱材料密度下限 α = 10⁻³（避免整体刚度阵奇异）

**数值难题**：超椭圆 TDF 在零水平集附近梯度剧变，四节点平均产生网格相关的灰度过渡与刚度高估，小特征易丢失（"孤岛"现象）。

### 2.2 三维与高效实现：256 行代码

Du Z, Cui T, Liu C, Zhang W, Guo Y, Guo X, *An efficient and easy-to-extend Matlab code of the MMC method for three-dimensional topology optimization*, Struct Multidisc Optim, 2022, 65:158（arXiv:2201.02491）。

- 在 188 行 2D 方案基础上推广到 3D；
- 引入**函数聚合**（function aggregation）实现精确灵敏度分析；
- 用"**载荷传递路径识别**"算法剔除不在传力路径上的 DOF 以加速 FEA。

### 2.3 投影变换 MMC（PMMC）——降低插值误差

*A projective transformation-based topology optimization using moving morphable components*, CMAME, 2020。

- 任意组件视为"与设计变量无关的组件模板"的投影；
- 配合单元内**分层特征重构**（hierarchical feature construction）在单元内重建内部细节；
- 降低插值误差，实现不受背景网格质量影响的高精度特征表示与灵敏度分析；
- 同时采用 XFEM 捕捉边界，保证几何模型与分析模型一致。

### 2.4 多分辨率离散（解耦的极致）

Liu C, Zhu Y, Sun Z, Li D, Du Z, Zhang W, Guo X, *An efficient MMC-based approach for multi-resolution topology optimization*, Struct Multidisc Optim, 2018, 58(6):2455–2479（arXiv:1805.02008）。

**技术路线**：借用 Nguyen et al.（2009, MTOP）的**超单元/hyper-element**技术，使用两套不同分辨率网格：

| 网格角色 | 用途 |
|---|---|
| 粗网格（FEA 网格）| 插值位移场，控制 DOF 数 |
| 细背景网格（几何网格）| 描述组件几何，每个单元用中心一个积分点 |

**关键性质**：加密几何网格不增加设计变量数（设计变量绑定组件数而非网格）。

**悬臂梁算例性能**：

| 方案 | DOF 数 | FEA 平均耗时/步 |
|---|---|---|
| 几何网格 = FEA 网格（1280×640）| 1,642,242 | 15.18 s |
| 超单元（160×80）| 26,082 | 0.47 s（约 **32×** 加速）|
| 同网格 SIMP | 设计变量 819,200 | — |
| MMC（576 组件）| 设计变量仅 3,456 | — |

**精度量化**：
- 分辨率比 n_be ≤ 8 时，FEA 相对误差 < 4%（可接受）；
- n_be ≥ 10 时，误差不可接受；
- 分布载荷算例对分辨率更敏感（n_be = 3 时即达 47% 误差）。

**IGA 框架下的多分辨率**：*Multiresolution Isogeometric Topology Optimisation Using Moving Morphable Voids*, CMES, 2020——用两套离散层级，以 Greville 配点 ersatz 模型表征模量与密度场，在不增加 DOF 的前提下获得高分辨率设计。

---

## 三、扩展有限元法（XFEM）——固定网格上的边界精确积分

XFEM 是郭旭团队绕开 ersatz 灰度、在固定网格上沿真实边界精确积分的主力工具。

**代表作**：

- Zhang W, Li D, Zhang J, Guo X, *Minimum length scale control in structural topology optimization based on the MMC approach*, CMAME, 2016, 311:327–355。用梯形组件在固定网格上演化，XFEM 做结构响应分析，灵敏度通过沿结构边界的数值积分获得，并给出最小尺度的精确定义。

- *Structural topology optimization through explicit boundary evolution*, JAM, 2017（Zhang, Yang, Zhou, Li, Guo, 84(1):011011）——不依赖 TDF 的边界演化实现。

- PMMC（见 §2.3）亦以 XFEM 提升多组件系统边界与灵敏度精度。

---

## 四、等几何分析（IGA）与 MMC/MMV

IGA 路线把 NURBS 高精度基函数与 MMC/MMV 显式性结合，是团队（及合作者）边界精确离散的另一主线。

### 4.1 MMC-IGA

Hou W, Gai Y, Zhu X, et al., *Explicit isogeometric topology optimization using moving morphable components*, CMAME, 2017, 326:694–712（大连理工胡平团队）。NURBS 片描述设计域，IGA 做响应/灵敏度分析，显著改善原 MMC 的数值稳定性与鲁棒性。

### 4.2 R 函数 + 配点 ersatz

Xie X, Wang S, Xu M, Wang Y, *A new isogeometric TO using MMC based on R-functions and collocation schemes*, CMAME, 2018, 339:61–90。

- 用 R 函数处理组件重叠区 C¹ 不连续问题；
- 比较 uniform/Gauss/Greville 三种配点 ersatz 方案；
- 结论：R 函数收敛率提升 17%–60%，Greville 配点方案优于其他两种。

### 4.3 IGA-MMV + TSA（裁剪面分析）

Zhang W, Li D, Kang P, Guo X, Youn S-K, *Explicit topology optimization using IGA-based moving morphable void (MMV) approach*, CMAME, 2020, 360:112685。

- 把 MMV 框架经 **trimming surface analysis（TSA）** 无缝嵌入 IGA；
- 用 B 样条曲线既描述孔洞几何又提供裁剪信息，可直接防止自交与锯齿边界。

**应力壳扩展**：Zhang W, Jiang S, Liu C, Li D, Kang P, Youn S-K, Guo X, *Stress-related topology optimization of shell structures using IGA/TSA-based MMV approach*, CMAME, 2020, 366:113036。

**合作/外部扩展**：Gai et al.（2020，闭合 B 样条边界 MMV）、自适应截断分层 B 样条 IGA-MMC（THB, Struct Multidisc Optim, 2021）。

---

## 五、移动/自适应网格与体贴合网格

当几何用纯 Lagrangian 方式描述、可生成干净光滑的 CAD 级边界时，团队转向**自适应体贴合重网格**而非固定网格：

### 5.1 加筋板

Jiang X, Liu C, Zhang S, Zhang W, Du Z, et al., *Explicit Topology Optimization Design of Stiffened Plate Structures Based on the MMC Method*, CMES, 2023, 135(2):809–838。

- 基板与加筋均离散为**自适应体贴合网格**（adaptive re-meshing）；
- 用动态更新的板/壳单元 + **自适应基结构**（adaptive ground structure）法；
- 相比固定网格 3D 实体/等效刚度模型分析更准。

### 5.2 薄壁结构统一框架

Jiang X, Liu C, Du Z, Huo W, Zhang X, Liu F, Guo X, *A unified framework for explicit layout/topology optimization of thin-walled structures based on MMC method and adaptive ground structure approach*, CMAME, 2022, 396:115047。

- Lagrangian 几何描述 + 自适应重网格 + 全壳模型（动态更新壳单元）；
- 发展节点驱动自适应基结构正则化。

### 5.3 四叉树自适应网格

MMV 应力问题中亦采用**四叉树自适应网格**做 FEA（Zhang et al., CMAME 2018, 334:381–413），在边界切割单元处局部加密。

---

## 六、其他高效离散技术

### 6.1 标度边界有限元法（SBFEM）

Zhang et al., *A scaled boundary finite element based explicit topology optimization approach for three-dimensional structures*, IJNME, 2020。SBFEM 做 3D 结构分析，边界区域用细网格、内部用粗网格的自适应加密，显著降低 3D 优化 DOF。

### 6.2 边界元法（BEM）

Zhang et al., *Explicit structural topology optimization using boundary element method-based moving morphable void approach*, IJNME, 2021。MMV 孔洞边界天然适合 BEM 只离散边界的特性。

### 6.3 无网格 MMC（ML-MMC）

*A meshless moving morphable component-based method for structural topology optimization without weak material*, Acta Mech Sinica, 2022。

- 仅在组件占据的实心区做分析；
- 通过无网格形函数自适应影响域耦合离散组件；
- **无需弱材料即可避免刚度阵奇异**——对大变形、动力/屈曲问题尤其有利。

### 6.4 混合有限元（mixed FEM）

见于水下吸声材料 MMC 应用（Struct Multidisc Optim, 2025, *A MMC-based topology optimization method for underwater sound absorption materials using a mixed finite element formulation*），属应用驱动的离散选择。

### 6.5 虚单元法（VEM）——开放接口

VEM 目前主要由外部团队推动（Antonietti、Bruggi、Paulino 的 PolyTop 等），尚未见郭旭团队主导的 VEM-MMC/MMV 专文。

**潜在价值**：MMC 组件边界切割固定网格产生的正是多边形/带悬挂节点单元，VEM 对此天然免疫且无需显式积分——这是一个值得用 FEALPy 等支持多边形/VEM 的平台去填补的空白，亦是胡张混合元研究背景可以衔接的方向。

---

## 七、快速/降阶分析方法

### 7.1 超单元/多分辨率（最成熟方案）

见 §2.4。悬臂梁算例约 32× 加速，n_be ≤ 8 时 FEA 误差 < 4%。

### 7.2 问题无关机器学习（PIML）

**系列论文**：

| 版本 | 文献 | 核心效果 |
|---|---|---|
| 基础版 | Huang M, Du Z, Liu C, et al., Extreme Mech Lett, 2022, 56:101887 | 问题无关，EMsFEM 框架 |
| 子结构增强版 | Huang, Cui, Liu, Du, Zhang, He, Guo, EML, 2023, 63:102041 | 10⁴–10⁵× 求解效率提升 |
| 无数据力学驱动版 | Huang, Liu, Guo, Zhang, Du, Guo, JMPS, 2024, 193:105893 | >2 orders 效率改善 |
| 高性能并行版 | Acta Mech Sinica, 2025 | GPU 并行加速 |

**核心**：在扩展多尺度有限元（EMsFEM）框架下，用轻量神经网络建立粗尺度多尺度形函数与细尺度材料分布的映射，加速大规模 FEA。

### 7.3 代理模型/实时优化

Lei X, Liu C, Du Z, Zhang W, Guo X, *Machine learning-driven real-time topology optimization under MMC-based framework*, JAM, 2019, 86(1):011004。

- 用 SVR/KNN 建立设计参数与外部条件的映射实现近实时优化；
- MMC 低维几何参数特别适合做 ML 标签。

### 7.4 降阶模型（ROM）

MMC/MMV 自身降阶专文较少；动力学拓扑优化降阶参见 Li Q, Sigmund O, Jensen JS, Aage N, *Reduced-order methods for dynamic problems in topology optimization*, CMAME, 2021, 387:114149（外部，但常被团队引用）。ROM 在 MMC 动力学问题上仍是空白。

---

## 八、方法体系脉络梳理

```
固定网格近似边界
  └─ ersatz 四节点平均（Zhang 2016, 188行）    ← 默认方案，误差主源
       ├─ 投影变换 PMMC（2020）                 ← 降低插值误差
       ├─ 多分辨率超单元（2018, ~32×）          ← 快速 FEA
       └─ XFEM 精确边界积分（2016 最小尺度）    ← 固定网格精确化

贴体/裁剪精确边界
  ├─ IGA-MMC（2017）+ TSA-MMV（2020）          ← NURBS 高精度
  ├─ 自适应体贴合重网格（加筋板 2022/2023）     ← CAD 级边界
  ├─ 四叉树自适应（MMV 应力 2018）             ← 局部加密
  ├─ SBFEM（3D 降 DOF, 2020）
  ├─ BEM-MMV（2021）
  └─ 无网格 ML-MMC（2022）                     ← 无弱材料

开放接口（待填补）
  └─ VEM + MMC/MMV                             ← 多边形单元天然适配
```

---

## 九、对本研究的启示与定位

### 9.1 当前研究计划的衔接点

本研究计划第二个题目"**面向 MMC/MMV 显式拓扑优化的高精度数值离散与高效结构分析方法研究**"与郭旭团队研究体系的衔接点：

| 研究方向 | 郭旭团队现状 | 本研究可发力点 |
|---|---|---|
| 固定网格 ersatz 精度 | 已有 188/256 行代码基准 | 定量复现误差，建立比较基准 |
| VEM 与 MMC 结合 | 尚无主导成果（开放接口）| **FEALPy 多边形/VEM 天然工具栈** |
| 胡张混合元 + MMV | 仅见于水下吸声 mixed FEM（2025）| 高精度应力约束优化（MMV 应力问题）|
| PIML + MMC/MMV | 团队 EMsFEM-PIML 体系已成熟 | 与博后主线（研究计划 1）衔接 |
| 超单元多分辨率 | 成熟（2018），精度已量化 | 作为快速分析基准，n_be ≤ 8 控制误差 |

### 9.2 建议研究路线

**分阶段路线**（与研究计划第一阶段文献调研对应）：

1. **复现基准**：2D 固定网格 188 行 ersatz 方案，复现 TDF 零水平集附近插值误差；
2. **边界离散对比**：引入 VEM/XFEM，对比 ersatz 与精确边界积分的柔顺度/应力相对误差；
3. **推广**：自适应贴体/IGA-TSA 方向；
4. **快速分析接入**：超单元多分辨率（n_be ≤ 8）或 PIML/EMsFEM 加速。

**基准切换条件**：当边界积分误差成为灵敏度噪声主源（优化震荡、应力虚假峰值）时，即应升级离散方案（ersatz 相对误差 > 5% 时转向 XFEM 或贴体方案）。

### 9.3 最高价值方向：VEM × MMC

MMC 组件边界切割固定网格产生的正是多边形/带悬挂节点单元，VEM 对此天然免疫且无需显式积分。建议在 FEALPy 上实现"**MMC-VEM**"：用 VEM 处理边界切割单元、内部用标准元，对照 ersatz 与 XFEM。这是郭旭团队主线尚未深入、而 FEALPy 多边形/VEM 工具栈恰好擅长的缺口，也是胡张混合元经验可直接迁移的方向。

---

## 十、关键文献列表

| 序号 | 文献 | 关键贡献 |
|---|---|---|
| 1 | Guo, Zhang & Zhong, JAM 2014 | MMC 框架奠基 |
| 2 | Zhang et al., CMAME 2017 | MMV 框架奠基 |
| 3 | Zhang et al., SMO 2016（188行）| 固定网格 ersatz 基准方案 |
| 4 | Du et al., SMO 2022（256行）| 3D MMC 高效实现 |
| 5 | Liu et al., SMO 2018 | 多分辨率超单元，~32× 加速 |
| 6 | Zhang et al., CMAME 2016 | XFEM + 最小尺度控制 |
| 7 | Hou et al., CMAME 2017 | IGA-MMC |
| 8 | Zhang et al., CMAME 2020 | IGA-TSA-MMV |
| 9 | Zhang et al., CMAME 2020（应力壳）| IGA/TSA-MMV 应力壳 |
| 10 | Jiang et al., CMAME 2022 | 薄壁结构统一框架 |
| 11 | Huang et al., EML 2022 | PIML 基础版 |
| 12 | Huang et al., EML 2023 | PIML 子结构增强（10⁴–10⁵×）|
| 13 | Huang et al., JMPS 2024 | PIML 无数据力学驱动版 |
| 14 | Lei et al., JAM 2019 | SVR/KNN 实时优化 |

---

## 关联文档

- [[postdoc-research-plan]] — 博士后科研计划（本调研对应第二个研究题目）
- [[guo-xu-team-overview]] — 郭旭院士团队研究体系总览
- [[literature/topology-opt/Huang2022-problemindependentmachine]] — PIML 奠基论文精读笔记
