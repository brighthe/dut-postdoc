---
title: "MMC 原型在 SOPTX/FEALPy 框架中的集成与执行计划"
tags:
  - integration-plan
  - MMC
  - FEALPy
  - sprint
status: "in-progress"
date: 2026-06-30
related:
  - postdoc-research-plan
  - one-week-defense-sprint-plan
  - mmc_math_principles
---

# MMC 原型在 SOPTX/FEALPy 框架中的集成与执行计划

本文档定义了将 **MMC (Moving Morphable Components)** 方法接入我们现有有限元底座 (SOPTX/FEALPy) 的架构设计与工程执行路线。
特别地，针对即将到来的博后进站答辩，本文档拆解了答辩前的一周冲刺任务（即**能力 C：显式几何与高阶网格切割的原型展示**）。

---

## 1. 冲刺目标与范围定义 (One-Week Sprint Scope)

根据 `one-week-defense-sprint-plan`，我们**不在这几天的冲刺中开发包含敏度分析的完整 MMC 优化器**。
为了在答辩帧 8 中呈现最具视觉冲击力与技术深度的“前期基础”，我们将聚焦于**正向的几何映射与网格切割环节**。

**产出标的物**：一张名为 `mmc_baseline.pdf` 的高质量矢量图（直接用于替换 PPT 帧 8 的 TikZ 占位图），该图必须清晰展现：
1. 底层粗糙的高阶背景网格。
2. 跨越网格的显式 MMC 组件边界。
3. 被切开的单元内部，严格按几何边界分布的适应性高斯积分点。

---

## 2. 软件架构接口设计

在 SOPTX/FEALPy 体系下，我们需要建立一套轻量级的几何映射工具箱，主要包含以下核心类：

### 2.1 `MMCComponent`（几何定义类）
- **功能**：描述单一 MMC 组件的参数化模型。
- **属性**：中心坐标 `(xc, yc)`，几何尺寸 `(L, W)`，倾角 `theta`，平滑参数 `m`。
- **方法**：
  - `__call__(x, y)`：评估拓扑描述函数 (TDF) 的值，判定空间点的内外归属。
  - `get_bounding_box()`：返回粗筛包围盒，用于加速单元相交测试。

### 2.2 `MeshCutter`（背景网格切割器）
- **功能**：处理 FEALPy 背景网格与 `MMCComponent` 集合的求交运算。
- **输入**：背景网格对象（如 `QuadrangleMesh`），全局组件集合。
- **处理流程**：
  1. 遍历背景单元，调用单元节点的 TDF 值。
  2. 根据 TDF 符号变化，将单元打上 `SOLID`, `VOID`, `CUT` 标签。
  3. 针对 `CUT` 单元，调用等值线提取算法（如基于 `skimage.measure.find_contours` 或自写简单的 Marching Squares）获取切割面段。

### 2.3 `IntegrationPointGenerator`（自适应积分点生成器）
- **功能**：为切割后的子多边形分配高阶高斯积分点。
- **实现逻辑**：
  - 针对被切割的 `SOLID` 子区域，进行 Delaunay 三角剖分（可调用 `scipy.spatial.Delaunay`）。
  - 在每个子三角形内部映射标准的三角形 3 点或 6 点高斯积分坐标与权重。

---

## 3. 答辩 Demo 执行步骤 (T1 → V1)

以下任务计划在接下来的一到两天内执行完成，脚本统一存放在 `research/mmc-prototype/mmc_cut_mesh.py`。

### T1：构建背景环境与几何对象
- 利用 FEALPy 初始化一个分辨率较低的 2D 背景四边形网格（例如 $10 \times 10$），以便在图中能清楚看清单元。
- 实例化一个倾斜的 `MMCComponent`（如 $L=6.0, W=1.5, \theta=30^\circ$），使其斜穿网格中心。

### T2：单元状态评估与边界重构
- 提取网格所有单元的顶点坐标，计算全局 TDF。
- 筛选出处于 `CUT` 状态的过渡单元集合。
- 在这些单元内部计算出边界线段的端点，重构出边界轮廓。

### T3：自适应积分点布设
- 对 `SOLID` 单元采用标准的 Tensor Product $3 \times 3$ 高斯积分。
- 对 `CUT` 单元内部的实体侧多边形进行三角化，布置高阶积分点。
- 收集所有属于材料域的积分点真实空间坐标 $(x_g, y_g)$。

### V1：成果可视化绘制
使用 Matplotlib 构建答辩图表：
- **底图**：绘制灰色的背景网格线。
- **几何轮廓**：用醒目的颜色（如绿色半透明）叠加 MMC 组件的真实几何外形。
- **细节标识**：
  - 用深色圆点标出所有的有效高阶高斯积分点。
  - 放大并用红色边框高亮某一个典型的被切割单元，凸显积分点只分布在实体侧（与传统 ersatz 方法的全域插值形成对比）。
- 保存输出高清 PDF 供 LaTeX 使用。

---

## 4. 博后长期阶段接口预留 (Future Extensions)

在完成答辩验证后，上述基础模块将为后续博后计划（方向二）的深入开展奠定基础：
1. **接入高阶分析基类**：将生成的 $(x_g, y_g, w_g)$ 直接输入到 SOPTX 现有的任意次 Lagrange / 胡张混合元组装引擎（替换原有的均匀网格积分点）。
2. **对接 Matrix-Free 算子**：将基于切割网格的局部刚度阵直接推入基于 Krylov 方法的无矩阵乘法操作中，从而避免处理悬挂节点时的复杂全局组装。
3. **AD 灵敏度支持**：在 PyTorch/JAX 后端中重新实现上述 `MeshCutter` 和求积逻辑，使得目标函数相对于 MMC 几何参数的导数可以通过计算图自动反向传播获得，彻底免除繁琐的手工解析求导。

---

## 5. 参考文献

集成开发过程中需对照以下基础文献进行算法复现与数据校验：

1. **核心算法基准参考**（含 188 行 MATLAB 代码，用于对照 TDF 定义与边界切割）：
   - Zhang W, Yuan J, Zhang J, Guo X. *A new topology optimization approach based on Moving Morphable Components (MMC) and the ersatz material model*, Struct Multidisc Optim, 2016, 53(6):1243–1260.
2. **MMV 原型实现参考**：
   - Zhang W, Chen J, Zhu Y, Zhou J, Xue D, Lei X, Guo X. *Explicit three dimensional topology optimization via Moving Morphable Void (MMV) approach*, Computer Methods in Applied Mechanics and Engineering, 2017, 322:590-614.
3. **高精度边界积分参考**（指导如何避免 ersatz 误差，建立真正的边界追踪）：
   - Zhang W, Li D, Zhang J, Guo X. *Minimum length scale control in structural topology optimization based on the MMC approach*, CMAME, 2016, 311:327–355.
