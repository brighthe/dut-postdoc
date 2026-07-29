---
title: "机器学习：架构、学习对象与训练范式"
type: concept
aliases:
  - 机器学习分类框架
  - machine-learning taxonomy
tags:
  - machine-learning
  - scientific-machine-learning
  - PINN
  - neural-operator
status: in-progress
date_added: 2026-07-29
date_update: 2026-07-29
---

# 机器学习：架构、学习对象与训练范式

> **一句话**：机器学习不存在唯一且穷尽的分类；应至少从神经网络架构、学习对象、训练信号／物理融合方式和任务目标四个相互独立的维度定位一个模型。

## 定义与分类边界

“MLP”“PINN”“DeepONet”和“Diffusion Model”并不处于同一分类层级：MLP 是神经网络架构，PINN 是把物理约束写入训练的范式，DeepONet 是面向函数到函数映射的模型族，Diffusion Model 则通常按生成任务与训练机制界定。把它们放入同一棵互斥的分类树会混淆“网络如何计算”“模型学习什么”和“如何训练”。

因此，描述一个机器学习方法时，应先分别说明下列四个维度，再说明具体应用问题。

## 一、四个正交维度

| 维度 | 回答的问题 | 常见类别或实例 | 说明 |
|---|---|---|---|
| **神经网络架构** | 神经网络怎样组织信息与参数？ | 前馈网络：MLP；卷积网络：CNN、ResNet、U-Net；序列网络：RNN、LSTM、GRU、Transformer；图网络：GNN、GCN、GAT | 架构主要由输入输出的局部性、网格性、序列性或图拓扑决定；同一架构可服务不同学习对象与训练范式。 |
| **学习对象** | 模型近似的是一个函数、一个算子、表示还是分布？ | 函数学习、算子学习、表征／降维学习、生成建模 | 这是理解科学机器学习中模型角色的主维度，不能由网络名称直接判断。 |
| **训练信号与物理融合** | 参数由什么目标约束或更新？ | 监督学习、自监督学习、PINN residual 训练、能量／变分训练、混合训练 | PINN 是训练范式，不是一种固定神经网络架构；它可以使用 MLP，也可与数据监督或其他约束结合。 |
| **任务目标** | 输出服务于什么计算或决策？ | 求解／预测、分类、表示／降维、生成、控制与优化 | 一个模型可以同时服务多个目标；最终仍要以其进入真实计算链后的下游指标评价。 |

### 1. 神经网络架构

神经网络架构规定计算图、参数共享方式与信息交互范围。它不直接规定模型学习的是函数还是算子，也不直接规定训练是否包含物理约束。

```text
神经网络架构
├─ 前馈网络：MLP
├─ 卷积网络：CNN、ResNet、U-Net
├─ 序列网络：RNN、LSTM、GRU、Transformer
└─ 图网络：GNN、GCN、GAT
```

编码—解码网络（Autoencoder、VAE）和生成模型（GAN、Diffusion Model）通常按其学习目标或生成机制识别；它们也可以采用卷积、注意力或图网络等不同架构作为骨干。

### 2. 函数学习与算子学习

**函数学习（function learning）**近似有限维输入到有限维输出的映射，例如

$$
f_\theta: \mathbb{R}^{m}\longrightarrow\mathbb{R}^{n}.
$$

坐标型 PINN 将空间（以及可选的时间、参数）作为输入，并输出该位置的解场值；因此通常属于函数学习。

**算子学习（operator learning）**学习函数／场到函数／场的映射，例如

$$
\mathcal{G}: a(\boldsymbol{x})\longmapsto u(\boldsymbol{x}),
$$

其中 $a$ 可为系数场、源项、初边值或几何描述，$u$ 为对应解场。DeepONet 和 Fourier Neural Operator（FNO）是典型神经算子模型族。算子学习的关键不是输入输出张量“看起来很大”，而是目标映射本身是函数到函数的关系，并通常关心对采样分辨率或离散的泛化。

### 3. 训练信号与物理融合

| 范式 | 主要训练信号 | 物理信息的进入位置 |
|---|---|---|
| 监督学习 | 输入—标签对 | 标签往往由实验、仿真或解析解生成 |
| 自监督学习 | 样本自身构造的预测或一致性目标 | 可无显式物理模型 |
| PINN | PDE、边界／初始条件 residual，及可选观测数据 | 强形式 residual 经自动微分写入 loss |
| 能量／变分训练 | 势能、能量泛函、弱形式或约束目标 | 物理变分结构直接构成 objective |
| 混合训练 | 上述信号的组合 | 数据与物理项共同约束模型 |

这些范式可复用同一参数更新骨架：`zero_grad → forward → loss → backward → optimizer.step`；差别在于 sample、loss 的构造及评价门禁。完整工程闭环见 [[../research/workflows/machine-learning-workflow]]。

### 4. 任务目标

| 目标 | 典型方法或实例 | 产出 |
|---|---|---|
| 求解／预测 | 回归网络、PINN、神经算子 | 标量、类别、响应或解场 |
| 表示／降维 | Autoencoder、VAE、降阶表示 | 低维潜变量或可重构表示 |
| 生成 | GAN、Diffusion Model | 满足条件的样本、图像、场或设计候选 |
| 控制／优化 | 强化学习、可微优化、代理辅助优化 | 策略、更新动作或设计候选 |

## 二、多维分类的组合示例

一个具体方法应同时在四个维度上定位，不能只用某个网络名称或训练范式概括全部属性：

| 方法示例 | 神经网络架构 | 学习对象 | 训练范式 | 任务目标 |
|---|---|---|---|---|
| 坐标型 PINN | 通常采用 MLP，也可采用其他可微架构 | 函数学习：坐标／参数到特定解场 | PDE、初边值条件 residual 及可选观测数据 | 求解给定边值问题或识别方程参数 |
| Neural Operator | DeepONet、FNO 等 | 算子学习：函数／场到函数／场 | 监督学习、物理约束训练或二者混合 | 预测一族参数化问题的解场 |
| PIML 局部代理 | MLP、DeepONet 等，取决于具体方法 | 场到矩阵代理或局部力学表示学习 | 监督学习或 mechanics-based 训练 | 加速局部力学表示的构造并服务下游全局计算 |

这张表展示的是维度组合，而不是三个互斥的机器学习类别。例如，“PINN”描述训练中如何引入物理约束，不替代 MLP 等神经网络架构描述；“Neural Operator”主要由学习对象界定，也可以采用不同训练信号。坐标型 PINN 的具体物理与训练过程见 [[../research/workflows/pinn-machine-learning-workflow]] 和 [[../research/workflows/linear-elasticity-pinn-machine-learning-workflow]]。

## 三、算子学习的判别边界

通常所说的 Neural Operator 以函数空间之间的映射为学习对象：

$$
\mathcal{G}:\mathcal{A}\longrightarrow\mathcal{U},
\qquad
a(\boldsymbol{x})\longmapsto u(\boldsymbol{x}).
$$

实际训练必然使用有限采样或离散张量，但“输入输出以数组存储”本身不能判定模型属于算子学习。关键在于目标是否表示一族函数／场之间的映射，以及模型是否具有与其声明一致的离散或采样泛化能力。

例如，以下映射

$$
\rho^j\longmapsto\mathbf{K}_s^j
$$

若以固定维度的离散局部密度描述为输入、固定维度的缩聚刚度矩阵为输出，更准确地称为 **field-to-matrix surrogate（场到矩阵代理）** 或局部力学表示学习；不能仅因 $\rho^j$ 来源于密度场就自动称为通常意义上的 Neural Operator。与之相比，跨一族问题学习

$$
\rho(\boldsymbol{x})\longmapsto\boldsymbol{u}(\boldsymbol{x})
$$

这样的场到场关系，更符合算子学习的典型定义。PIML 的具体计算角色、复用范围与问题无关性边界见 [[piml/ml-roles-and-boundaries]] 和 [[piml/mathematical-foundations]]。

## 四、参考来源

- [Goodfellow, Bengio & Courville, *Deep Learning*](https://www.deeplearningbook.org/) — 神经网络与表征学习的基础教材。
- [Vaswani et al. (2017), *Attention Is All You Need*](https://arxiv.org/abs/1706.03762) — Transformer。
- [Scarselli et al. (2009), *The Graph Neural Network Model*](https://doi.org/10.1109/TNN.2008.2005605) — 图神经网络早期基础工作。
- [Kingma & Welling (2014), *Auto-Encoding Variational Bayes*](https://arxiv.org/abs/1312.6114)；[Goodfellow et al. (2014), *Generative Adversarial Nets*](https://arxiv.org/abs/1406.2661)；[Ho et al. (2020), *Denoising Diffusion Probabilistic Models*](https://arxiv.org/abs/2006.11239) — VAE、GAN 与 diffusion 的代表工作。
- [Raissi, Perdikaris & Karniadakis (2019), *Physics-informed neural networks*](https://doi.org/10.1016/j.jcp.2018.10.045) — PINN。
- [Lu et al. (2021), *Learning nonlinear operators via DeepONet*](https://doi.org/10.1038/s42256-021-00302-5)；[Li et al. (2021), *Fourier Neural Operator*](https://arxiv.org/abs/2010.08895) — 神经算子。

## 相关页面

- [[../research/workflows/machine-learning-workflow]] — 可重放机器学习项目的完整生命周期。
- [[../research/workflows/pinn-machine-learning-workflow]] — 一维 Poisson PINN 方法实例。
- [[../research/workflows/linear-elasticity-pinn-machine-learning-workflow]] — 小变形静力线弹性 PINN 方法契约。
- [[piml/ml-roles-and-boundaries]] — 计算力学中 PINN、PIML 等路线按计算角色的比较。
