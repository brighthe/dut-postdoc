---
title: "大连理工大学郭旭院士团队研究体系"
topic: "郭旭院士团队 · 显式拓扑优化 / PIML / 计算力学"
tags:
  - topology-opt
  - MMC
  - MMV
  - PIML
  - FEM
  - variational-principles
  - industrial-software
status: "done"
date_start: 2026-06-04
date_update: 2026-06-04
source: "[[../literature/_index]]"
---

# 大连理工大学郭旭院士团队研究体系

> [郭旭院士个人主页](https://faculty.dlut.edu.cn/2000011087/)  
> 依托：工业装备结构分析国家重点实验室

团队打破传统基于像素/体素（Pixel/Voxel）的隐式拓扑优化范式，主导开发了**显式拓扑优化理论（MMC/MMV）**，并在**工业级软件工程化（SiPESC / 星派仿真）**与**问题无关机器学习（PIML）**赋能的超大规模结构优化方面取得了具有国际影响力的突破。

---

# 研究方向一：显式拓扑优化 (MMC/MMV)

移动变形组件（Moving Morphable Components, MMC）及移动变形孔洞（Moving Morphable Voids, MMV）方法的核心思想是利用一组具备显式几何特征的组件来描述结构的拓扑与形状。区别于传统基于体素的密度法（SIMP），本框架的本质是在**低维连续几何参数空间**中进行寻优。

**参数输入**：组件 / 孔洞初始几何参数

**STEP1：显式几何表征与全局拓扑组装**

在优化初始化及每次迭代开始时，需要将底层的数学参数转化为连续空间中的几何实体与拓扑边界。其构建流程主要分为两步：

1. **局部连续表征（组件构造）**： 提取设计空间内第 $i$ 个组件的显式几何变量集合 $D^i$，在参考坐标系下构造拓扑描述函数（Topological Description Function, TDF） $\phi_i(x)$，解析且平滑地定义组件边界。对于具有复杂骨架结构的情况，可采用距离函数定义以实现几何解耦。
2. **全局拓扑映射（布尔组装）**： 利用布尔算子将所有 $n$ 个局部函数合成为全局拓扑描述函数 $\phi^s(x)$。其中，实体组件（MMC）通过**并集算子** $\phi^s(x) = \max(\phi_1, \dots, \phi_n)$ 实现材料叠加；变形孔洞（MMV）则通过**交集算子** $\phi^s(x) = \min(\phi_1, \dots, \phi_n)$ 实现空间侵蚀。

**STEP 2：物理场空间离散与数值求解**

1. **通用离散范式（几何映射）**： 包括**等效材料模型（Ersatz Material Model）**（利用正则化 Heaviside 函数将显式边界的演化转化为固定背景网格上的伪密度积分问题），以及**扩展有限元法（XFEM）**（基于等值面追踪边界，并通过引入富集项刻画界面的弱不连续性）等。
2. **控制方程求解（全局分析）**： 经 Galerkin 投影后，均统一归结为求解包含几何参数 $\mathbf{D}$ 隐式依赖的整体代数方程组：
$$\mathbf{K}(\mathbf{D}) \mathbf{U} = \mathbf{F}.$$

**STEP 3：灵敏度推导与链式传导**

1. **物理场敏度求解（全局推导）**： 基于伴随变量法（Adjoint Method）构造伴随方程，求解目标函数 $J$ 对于中间离散物理场的导数。
2. **几何参数敏度映射（局部传导）**：
$$\frac{\partial J}{\partial D_j^i} = \sum \left( \frac{\partial J}{\partial \text{物理场}} \times \frac{\partial \text{物理场}}{\partial \text{几何参数}} \right)$$

**STEP 4：几何参数空间驱动的优化迭代**

将低维显式敏度信息输入 MMA 等优化器，驱动组件发生**平移、旋转、缩放、变形以及相互融合/吞噬**，直至收敛后输出解析拓扑与 CAD 形态（IGES/STEP）。

## 核心文献

- **奠基与开山之作**
  - [[literature/topology-opt/Guo2014-MMC-explicit]] — _Doing Topology Optimization Explicitly and Geometrically_（MMC 奠基，低维显式几何参数化）
  - [[literature/topology-opt/Zhang2016-MMC-ersatz]] — _A new topology optimization approach based on MMC and the ersatz material model_（引入等效材料模型，188 行 Matlab 代码）
  - [[literature/topology-opt/Guo2016-boundary-evolution]] — _Structural Topology Optimization Through Explicit Boundary Evolution_（B 样条显式边界演化）

- **形态与维度拓展**
  - [[literature/topology-opt/Zhang2017-MMC-curved]] — _Explicit structural topology optimization based on MMC with curved skeletons_（曲骨架组件）
  - [[literature/topology-opt/Zhang2017-MMV-3D]] — _Explicit three dimensional topology optimization via Moving Morphable Void (MMV) approach_（三维 MMV）

- **物理约束攻坚**
  - [[literature/topology-opt/Xia2018-MMV-stress]] — _A MMV-based explicit approach for topology optimization considering stress constraints_（应力约束）
  - [[literature/topology-opt/Wang2020-shell-graded-infill]] — _Optimal design of shell-graded-infill structures by a hybrid MMC-MMV approach_（增材制造壳-填充结构）

- **权威综述**
  - [[literature/topology-opt/Guo2022-MMC-review]] — _A comprehensive review of explicit topology optimization based on MMC method_

---

# 研究方向二：问题无关机器学习 (PIML)

问题无关机器学习（Problem-Independent Machine Learning, PIML）方法的核心思想不是针对某一特定载荷、边界条件或优化目标训练端到端代理模型，而是学习可嵌入有限元分析框架的**局部力学算子**。

**阶段一：离线代理模型构建**

- 定义局部观测域（粗网格单元、Patch 窗口或微观单胞）
- 构建神经网络 $\mathcal{F}_{\theta}$：以局部材料密度分布 $\boldsymbol{\rho}_e$ 为输入，输出局部等效刚度矩阵 $\mathbf{k}_e$
- 支持**数据驱动**（监督学习）与**物理驱动**（最小势能原理作为损失函数，无监督）双范式

**阶段二：在线拓扑优化循环**

1. PIML 前向推断批量获取所有子域等效刚度矩阵
2. 组装全局刚度矩阵，求解 $\mathbf{K}\mathbf{U} = \mathbf{F}$
3. 伴随法 + 自动微分计算灵敏度
4. MMA / OC 更新设计变量

## 核心文献

- **前导探索**
  - [[literature/others/Wang2020-ML-MMC-realtime]] — _Machine learning-driven real-time topology optimization under MMC-based framework_（SVR/KNN + MMC 端到端映射）

- **PIML 方法提出**
  - [[literature/topology-opt/Huang2022-problemindependentmachine]] — _Problem-independent machine learning (PIML)-based topology optimization—a universal approach_（ANN + EMsFEM，奠基之作）

- **大规模结构分析拓展**
  - [[literature/others/Zheng2023-PIML-substructure]] — _PIML enhanced substructure-based approach for large-scale structural analysis_（力学先验约束，10 亿设计变量）
  - [[literature/others/Zheng2024-PIML-isoparametric]] — _PIML-enhanced structural topology optimization based on isoparametric elements_（等参元，复杂几何域）

- **Data-free 模型**
  - [[literature/others/Zheng2023-PIML-data-free]] — _A mechanics-based data-free PIML model_（最小势能原理无监督，JMPS）

- **三维点阵与高性能并行**
  - [[literature/others/Zheng2024-PIML-MMC-3D-lattice]] — _PIML enhanced 3D lattice composite structures optimization via MMC_
  - [[literature/others/Zheng2025-PIML-parallel]] — _A high-performance parallel algorithm based on PIML_（128 亿设计变量）

---

# 研究方向三：复杂力学行为变分原理与多尺度计算

在处理复杂大变形、双模量等非光滑本构材料，以及多尺度微观结构设计时，团队从底层泛函构造入手，建立了坚实的力学与数学底座。

---

# 研究方向四：工业软件与高性能计算布局（SiPESC）

核心抓手是 **SiPESC**（Software Integration Platform for Engineering and Scientific Computation）平台：结构有限元分析、结构优化、多学科优化、拓扑优化、大规模可视化和工程数据库等模块构成集成化 CAE 软件底座；通过插件式、组件化和开放式接口设计，将显式拓扑优化、PIML、子结构降维、大规模并行求解等方法嵌入工程流程。

## 核心文献

- _面向集成化 CAE 软件开发的 SiPESC 研发工作进展_（平台总览）
- _SiPESC.FEMS 的单元计算模块设计模式_（有限元内核）
- _通用集成优化软件 SiPESC.OPT 的设计与实现_（优化模块）
- _数据驱动的结构分析与设计专题序_（未来方向布局）

---

# 研究方向五：混合变分问题与极值型数值计算技术

## 核心挑战

经典 Hellinger-Reissner 泛函存在**全局鞍点性质**（代数方程组不定）与**非光滑本构失效**两大瓶颈。

## 破局路径：PVP + 极值型杂交元

1. **PVP 驱动的局部极值化重构**：在单元级引入假设应力杂交元，利用 PVP 将非光滑本构转化为局部**参数化二次规划（PQP）极小值问题**
2. **静态凝聚**：单元级 Schur 补降维 $K_{schur}=B_{e}(A_{e})^{-1}B_{e}^{T}$
3. **全局正定系统**：组装后全局刚度矩阵严格对称正定（SPD），彻底绕开 LBB 稳定性约束

## 核心文献

- [[literature/fem/Zhong1988-PVP]] — _Parametric variational principles and their quadratic programming solutions in plasticity_（钟万勰，PVP 奠基）
- [[literature/fem/Zhang2005-PVP-Voronoi]] — _PVP based elastic-plastic analysis with Voronoi FEM_（张洪武，非鞍点杂交元落地）
- [[literature/fem/Zhang2007-PVP-PFEM]] — _PVP based elastic-plastic analysis with polygonal and Voronoi cell FEM_
- [[literature/topology-opt/Guo2014-bimodulus-variational]] — _Variational principles and bounding theorems for bi-modulus materials_（郭旭，双模量变分底座）
- [[literature/topology-opt/Guo2024-bimodulus-large-deformation]] — _Finite deformation analysis of bi-modulus thermoelastic structures_（郭旭，大变形热力耦合）

---

## 研究切入点（个人思考）

### 方向 A：双模量问题的极值型杂交元离散

将 PVP 变分底座（方向五）与 Voronoi/多边形杂交元（张洪武工作）相结合，消除双模量大变形问题的全局鞍点，为 PIML 在非线性材料场景的落地打通底层算力通道。

### 方向 B：PIML 局部算子学习的物理约束增强

在 data-free PIML 框架中引入双模量本构的 PVP 极小值形式作为损失函数，同时满足"问题无关"泛化性与非光滑本构的物理一致性。

### 方向 C：MMC/MMV 与 PIML 的协同加速

沿用现有 3D MMC+PIML 点阵工作（方向二），向复杂曲面薄壁结构（方向四专利）延伸，结合等参元 PIML（方向二）处理非规则设计域。
