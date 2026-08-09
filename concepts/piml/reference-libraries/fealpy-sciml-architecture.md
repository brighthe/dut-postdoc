---
title: "FEALPy SciML 与机器学习基础设施架构"
type: concept
aliases:
  - FEALPy SciML Architecture
  - FEALPy 机器学习基础设施
  - fealpy.ml
  - FEALPy PINN 基础设施
tags:
  - FEALPy
  - SciML
  - PINN
  - machine-learning
  - python
  - pytorch
  - autograd
status: draft
date_added: 2026-08-07
date_update: 2026-08-07
---

# FEALPy SciML 与机器学习基础设施架构 (FEALPy SciML Architecture)

本文档沉淀 FEALPy 框架在科学机器学习（Scientific Machine Learning, SciML）与物理信息机器学习（PIML / PINN）方面的底层基础设施设计、模块架构与求解链分工。

---

## 1. 架构定位与模块分工

FEALPy 的 `fealpy.ml` 模块旨在将传统有限元 (FEM) 的网格、高斯积分与几何能力，与 PyTorch 深度学习框架的自动微分 (Autograd) 和神经网络模块进行无缝融合，提供专为偏微分方程 (PDE) 求解设计的 SciML 基础设施：

```text
FEALPy SciML 基础设施 (fealpy.ml)
├── grad.gradient           <-- [自动微分引擎] 高阶 PDE 残差与张量梯度链
├── sampler                 <-- [空间配点采样器] 域内 (ISampler) 与 边界 (BoxBoundarySampler) 采样
├── modules.Solution        <-- [网格-网络绑定容器] 神经网络包装与 FEALPy 网格高斯积分 error 估计
└── fealpy.mesh + pyevtk    <-- [计算力学后处理] 无结构网格导出 (.vtu) 与 ParaView 云图对接
```

---

## 2. 自动微分与高阶 PDE 残差算子 (`fealpy.ml.grad.gradient`)

在 Physics-Informed ML 中，PDE 的强形式残差需要对神经网络的输入坐标 $\boldsymbol{x}$ 求一阶及二阶偏导数。

### 2.1 链式求导机制
FEALPy 封装了 PyTorch 的 `torch.autograd.grad`，支持高阶张量梯度的批量计算：

```python
from fealpy.ml.grad import gradient

# 1. 计算位移场 u 对坐标 x 的一阶梯度 (Jacobian 矩阵 J_ij = du_i / dx_j)
grad_u = gradient(u_pred, x, create_graph=True)

# 2. 对称化得到 Cauchy 应变张量 epsilon
strain = 0.5 * (grad_u + grad_u.transpose(-1, -2))

# 3. 计算二阶应力散度 (div_sigma = div(C : epsilon))
# 通过二次调用 gradient 对应力张量求空间偏导
```

### 2.2 激活函数连续性约束
由于二阶 PDE 物理残差要求自动微分计算图二次可微，FEALPy 体系必须搭配 $C^\infty$ 无穷次连续可微的激活函数（如 $\tanh$、$\text{Sine}$ 或 $\text{GELU}$）。$\text{ReLU}$ 等分段线性函数的二阶导数几乎处处为零，会导致物理残差 Loss 陷入零梯度陷阱。

---

## 3. 配点采样器体系 (`fealpy.ml.sampler`)

PDE 强形式求解需要在问题物理域 $\Omega$ 及边界 $\partial\Omega$ 上离散采配点。FEALPy 提供了面向多维空间几何的配点采样器：

### 3.1 采样器分类
1. **域内采样器 (`ISampler`)**：在 $d$ 维超矩形或复杂几何域 $\Omega$ 内生成内部配点 $\boldsymbol{x}^{(int)}$。
2. **边界采样器 (`BoxBoundarySampler`)**：在 $d-1$ 维边界外表面 $\partial\Omega$ 上生成边界配点 $\boldsymbol{x}^{(bnd)}$，并保存边界法向向量 $\boldsymbol{n}$。

### 3.2 采样模式对比
* **`random` 动态采样模式**：
  在每个训练 Epoch 重新随机生成均匀分布配点。能有效覆盖连续空间，防止神经网络在固定配点上产生过拟合凹陷，泛化误差低。
* **`linspace` 固定网格采样模式**：
  在训练前一次性生成固定张量网格配点，训练全程重用。计算开销小，但在复杂场下容易在固定配点间产生局域残差震荡。

---

## 4. 网格与神经网络绑定容器 (`fealpy.ml.modules.Solution`)

FEALPy 提供了 `Solution` 包装器，将 PyTorch 的 `nn.Module` 神经网络与 FEALPy 的连续几何网格 (`TriangleMesh` / `TetrahedronMesh`) 进行解耦绑定：

### 4.1 核心职能
1. **前向预测接口**：同标准 `nn.Module`，支持 `net(x)` 位移/温度场预测。
2. **有限元网格数值积分评估器 (`estimate_error`)**：
   在 FEALPy 几何网格上自动利用高斯数值积分点，将 PINN 连续预测场与精确解/FEM 数值解进行空间重采样与高斯积分，精准计算全场 $L_2$ 范数绝对误差与相对误差：
   $$
   e_{L_2} = \left( \int_\Omega \|\hat{\boldsymbol{u}}(\boldsymbol{x}) - \boldsymbol{u}_{\text{exact}}(\boldsymbol{x})\|_2^2 \, \text{d}\boldsymbol{x} \right)^{1/2}
   $$

---

## 5. 计算力学可视化与数据导出 (`pyevtk`)

为了消除与传统计算力学后处理的鸿沟，FEALPy 基础设施支持将离散网格与 PINN 全场预测数据导出为标准 VTK 无结构网格 (`.vtu`) 格式：

* **网格拓扑转换**：将 FEALPy `Mesh.entity('node')` 与 `Mesh.entity('cell')` 转换为 VTK 节点与单元连通性矩阵（如 `VTK_TRIANGLE` 或 `VTK_TETRA`）。
* **场数据绑定**：将 PINN 预测场 $\hat{\boldsymbol{u}}$、精确场 $\boldsymbol{u}_{\text{exact}}$ 以及点值绝对误差模长绑定为 Point Data。
* **后处理集成**：导出的 `.vtu` 可直接在 ParaView 中实现 2D/3D 空间任意截面切片（Slice）、主应力矢量箭头发射与变分等值面提取。

---

## 6. 相关页面

* [[../../pinn-paradigm|PINN 通用概念与范式]]
* [[../../gpu-hpc/reference-libraries/fealpy-architecture|FEALPy 多后端与张量引擎架构]]
* **SOPTX PINN 线弹性算例数理规范**：`soptx/examples/pinn_elasticity/math_spec.md` (`/home/brighthe/workspace/soptx/examples/pinn_elasticity/math_spec.md`)
* **SOPTX 2D/3D PINN 消融测试与诊断报告**：`soptx/examples/pinn_elasticity/outputs/results_analysis.md` (`/home/brighthe/workspace/soptx/examples/pinn_elasticity/outputs/results_analysis.md`)
