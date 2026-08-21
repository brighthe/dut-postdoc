# Physics-Informed Neural Networks (PINN) 通用概念与求解范式

本文阐述 Physics-Informed Neural Networks (PINN) 求解偏微分方程（PDE）的连续物理模型、自动微分残差算子与离散 Loss 构造范式。

---

## 1. 连续介质力学与 PDE 通用表达

在有界区域 $\Omega \subset \mathbb{R}^d$ 上，考虑微分算子驱动的 PDE 控制方程：

$$
\mathcal{N}[\boldsymbol{u}](\boldsymbol{x}) = \boldsymbol{f}(\boldsymbol{x}), \quad \boldsymbol{x} \in \Omega
$$

与边界条件 $\mathcal{B}[\boldsymbol{u}](\boldsymbol{x}) = \boldsymbol{g}(\boldsymbol{x}), \ \boldsymbol{x} \in \partial\Omega$。

---

## 2. 通用 5 步 PINN 求解范式与流程图

无论求解何种偏微分方程（Poisson、线弹性、流体 Navier-Stokes 等），PINN 均遵循以下通用的 5 步计算骨架与训练闭环：

```mermaid
flowchart TD
    A(["1 · 定义 PDE 边值问题<br/>计算域 Ω · 控制方程 · 边界条件 ∂Ω"])
    B["2 · 初始化 PINN 求解器<br/>MLP 网络 <b>u</b><sub>θ</sub> · 优化器 · Loss 权重 · 采样器"]
    C["3A · 配点动态采样<br/>域内配点 <b>X</b><sub>int</sub> · 边界配点 <b>X</b><sub>bnd</sub>"]
    D["3B · 前向传播与自动微分<br/>预测位移 <b>û</b> · 空间梯度 ∇<b>u</b> · 物理残差算子"]
    E["3C · 构造 Physics-Informed Loss<br/>PDE 残差 MSE + 边界残差 MSE 加权组合"]
    F["3D · 反向传播与参数更新<br/>zero_grad() → loss.backward() → optimizer.step()"]
    G{"到达记录/评估节点？"}
    H["3E · 训练诊断<br/>记录 Loss 项 · 计算相对 L2 误差"]
    I{"达到最大 Epoch 或停止条件？"}
    J["4 · 冻结模型并进行全域推理预测<br/>解场分布比较 · 误差分析 · 可视化"]
    K(["5 · 输出结果与证据落盘<br/>Checkpoint · 评估指标 JSON · 训练曲线"])

    A --> B --> C --> D --> E --> F --> G
    G -- "否" --> I
    G -- "是" --> H --> I
    I -- "否：进入下一 Epoch" --> C
    I -- "是" --> J --> K
```

### 2.1 步骤 1：PINN 的解场参数化

MLP 的统一前向数学、维度约定和代码映射见
[[machine-learning#MLP：统一数学定义]]。PINN 在此通用骨干上指定学习对象为
连续解场:

$$
\hat{\boldsymbol{u}}_\theta: \boldsymbol{x}\in\Omega\subset\mathbb{R}^d
\longmapsto \hat{\boldsymbol{u}}(\boldsymbol{x})\in\mathbb{R}^{d_{\mathrm{out}}}.
$$

因此 $\boldsymbol{x}$ 必须保留自动微分计算图, 且激活函数的可微阶数必须满足下游 PDE 残差的求导要求.
本页后续内容只定义 PINN 特有的配点、自动微分、物理残差和优化过程.

### 2.2 步骤 2：配点采样 (Collocation Sampling)
PINN 属于无网格 Data-Free 方法，训练配点在计算域中动态生成：
* 域内配点集 $\mathcal{X}_{\text{int}} = \{\boldsymbol{x}_i^{(int)}\}_{i=1}^{N_{\text{int}}} \subset \Omega$
* 边界配点集 $\mathcal{X}_{\text{bnd}} = \{\boldsymbol{x}_j^{(bnd)}\}_{j=1}^{N_{\text{bnd}}} \subset \partial\Omega$

### 2.3 步骤 3：自动微分求导链与激活函数的 $C^k$ 阶数约束
PINN 利用自动微分（Automatic Differentiation, AD）精确计算解场关于空间坐标的高阶偏导数，克服了传统数值求导（如有限差分法）的截断误差与网格依赖：
$$
\nabla \hat{\boldsymbol{u}} = \text{AD}\left(\hat{\boldsymbol{u}}(\boldsymbol{x}); \boldsymbol{x}\right)
$$
进而显式构造点值 PDE 控制残差 $\boldsymbol{R}_{\text{int}}(\boldsymbol{x}; \boldsymbol{\theta})$ 与边界残差 $\boldsymbol{R}_{\text{bnd}}(\boldsymbol{x}; \boldsymbol{\theta})$。

##### 主流自动微分 (AD) 后端接口对照
PINN 的物理残差求导机制独立于具体软件框架，不同计算框架的 AD 实现接口如下：

| AD 计算框架 | 一阶/高阶偏导接口 | 特点与在 SciML 中的应用场景 |
|---|---|---|
| **JAX** | `jax.grad` / `jax.vmap` / `jax.jvp` | 函数式变换、极佳的高阶微分表达能力，结合 XLA JIT 编译在物理计算中性能强悍 |
| **PyTorch** | `torch.autograd.grad(..., create_graph=True)` | 动态计算图，工程生态最完善（如 `soptx` 默认后端） |
| **TensorFlow** | `tf.GradientTape(persistent=True)` | 经典框架，早期 PINN 论文 (Raissi 2019) 原始实现 |
| **Julia** | `Enzyme.jl` / `Zygote.jl` | 科学计算 (Scientific ML) 生态原生高阶自动微分 |

> **激活函数的 $C^k$ 阶数约束**：
> 若 PDE 包含 $m$ 阶偏导数（如线弹性与 Poisson 方程中的二阶偏导 $m=2$），激活函数必须满足 $C^k$ 连续可微（$k \ge m$）。
> * $\text{ReLU}(x) = \max(0,x)$ 的二阶导数几乎处处为 0，若用于 2 阶 PDE 会导致物理残差求导失效！
> * PINN 必须选用高阶连续可微激活函数，如 $\tanh(x) \in C^\infty$、$\text{SiLU}(x)$ 或 $\sin(x)$。

### 2.4 步骤 4：Physics-Informed Loss 函数构造
将域内残差与边界残差的均方误差（MSE）加权组合：
$$
\mathcal{L}(\boldsymbol{\theta}) = w_{\text{int}} \cdot \underbrace{\frac{1}{N_{\text{int}}} \sum_{i=1}^{N_{\text{int}}} \left\| \boldsymbol{R}_{\text{int}}(\boldsymbol{x}_i^{(int)}; \boldsymbol{\theta}) \right\|_2^2}_{\mathcal{L}_{\text{int}}} + w_{\text{bnd}} \cdot \underbrace{\frac{1}{N_{\text{bnd}}} \sum_{j=1}^{N_{\text{bnd}}} \left\| \boldsymbol{R}_{\text{bnd}}(\boldsymbol{x}_j^{(bnd)}; \boldsymbol{\theta}) \right\|_2^2}_{\mathcal{L}_{\text{bnd}}}
$$

### 2.5 步骤 5：梯度下降优化循环 (Optimization Loop)
利用 Adam 或 L-BFGS 优化器，按标准三步曲反向传播并更新网络权重：
```text
optimizer.zero_grad() → loss.backward() → optimizer.step()
```

---

## 3. 计算力学学者的通用概念映射卡片

将经典有限元（FEM）概念映射到深度学习（PyTorch/PINN）的对应组件：

| 经典计算力学 / FEM 概念 | PyTorch / PINN 对应组件 | 通用原理 |
|---|---|---|
| 试探函数 / 网格形函数插值 | 多层感知机 (MLP Neural Network) | 用连续神经网络逼近未知解场 |
| 形函数求导 $\mathbf{B}$ 矩阵 | 自动微分 `torch.autograd.grad` | 链式法则求解场关于坐标的高阶偏导 |
| 控制方程残差 / 最小势能原理 | 损失函数 (Loss Function: MSE) | 将 PDE 与边界条件转化为标量优化目标 |
| 积分点 / 采样点 | 配点 (Collocation Points) | 域内与边界的无网格坐标采样 |
| 整体刚度矩阵求解 $K U = F$ | Adam / L-BFGS 梯度下降优化器 | 迭代更新网络参数 $\boldsymbol{\theta}$ |

---

## 4. 范式对比：PINN vs [[piml/piml-paradigm|Problem-Independent PIML]]

| 维度 | PINN (Problem-Dependent) | PIML (Problem-Independent / Huang–Ma 路线) |
|---|---|---|
| **输入** | 空间坐标 $\boldsymbol{x} \in \mathbb{R}^d$ | 局部材料分布 / 几何配置 $\rho(\boldsymbol{x})$ |
| **输出** | 空间某点响应 $\hat{\boldsymbol{u}}(\boldsymbol{x})$ | 局部多尺度形函数 $\boldsymbol{N}(x)$ / 缩聚刚度矩阵 $\mathbf{K}_e$ |
| **训练数据** | 无数据 (Data-Free)，靠 Collocation 点残差 | 局部材料样本集 (Supervised 或 Data-Free Mechanics) |
| **重训需求** | 载荷 / 边界条件改变后**必须重新训练** | 训练完成后，**跨宏观 BVP 免重训、秒级推理** |
| **项目角色** | 物理残差算子基线、ML 入门与对比 Baseline | 博士后核心研究项目 WP2 的主线攻关方向 |

---

## 5. 常见物理问题的实例化索引

### 5.1 线弹性方程 (Linear Elasticity) 物理算子与求导规范

在轴对齐有界区域 $\Omega \subset \mathbb{R}^d \ (d \in \{2, 3\})$ 上，线弹性静力平衡控制方程为：

$$
-\nabla \cdot \boldsymbol{\sigma}(\boldsymbol{u}) = \boldsymbol{b} \quad \text{in } \Omega, \quad \boldsymbol{u} = \bar{\boldsymbol{u}} \quad \text{on } \partial\Omega
$$

#### 1. 应变与 Hooke 本构
小变形 Cauchy 应变 $\boldsymbol{\varepsilon} = \frac{1}{2}(\nabla \boldsymbol{u} + (\nabla \boldsymbol{u})^{\mathsf{T}})$，Hooke 本构点值应力张量为：
$$
\boldsymbol{\sigma}(\boldsymbol{u}) = \lambda \operatorname{tr}(\boldsymbol{\varepsilon})\mathbf{I} + 2\mu\boldsymbol{\varepsilon}
$$

#### 2. 基于 PyTorch Autograd 的物理残差求导链
由位移预测求一阶梯度矩阵 $J_{ij} = \frac{\partial \hat{u}_i}{\partial x_j} = \text{autograd}(\hat{u}_i, x_j; \text{create\_graph=True})$，构造应力后对应力张量各分量求坐标二阶散度：
$$
\boldsymbol{R}_{\text{int}}(\boldsymbol{x}; \boldsymbol{\theta}) = -\sum_{j=1}^d \frac{\partial \hat{\sigma}_{ij}}{\partial x_j} - \boldsymbol{b}(\boldsymbol{x}), \quad \boldsymbol{R}_{\text{bnd}}(\boldsymbol{x}; \boldsymbol{\theta}) = \hat{\boldsymbol{u}}(\boldsymbol{x}; \boldsymbol{\theta}) - \bar{\boldsymbol{u}}(\boldsymbol{x})
$$

* **代码实现参照**：`soptx/examples/pinn_elasticity`

---

## 6. 相关页面

* [[linear-elasticity|线弹性]] — 静力各向同性线弹性方程与变分形式
* [[machine-learning|机器学习]] — 经典回归、神经网络与函数/算子学习分类，含 SciML 归纳偏置
* [[piml/_index|PIML 术语与主题入口]] — Problem-Independent 路线说明
* [[piml/reference-libraries/fealpy-sciml-architecture|FEALPy SciML 与机器学习基础设施架构]] — PINN 求解链的框架侧实现基础
* [[gpu-hpc/reference-libraries/fealpy-architecture|FEALPy 多后端与张量引擎架构]] — 后端分派与 GPU 执行路径
