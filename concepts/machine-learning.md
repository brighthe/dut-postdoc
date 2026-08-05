---
title: "机器学习：模型、架构、学习对象与训练范式"
type: concept
aliases:
  - 机器学习：架构、学习对象与训练范式
  - 机器学习分类框架
  - machine-learning taxonomy
tags:
  - machine-learning
  - scientific-machine-learning
  - PINN
  - neural-operator
status: in-progress
date_added: 2026-07-29
date_update: 2026-07-31
---

# 机器学习：模型、架构、学习对象与训练范式

> **一句话**：机器学习不存在唯一且穷尽的分类；应至少从模型族与架构、学习对象、训练信号／物理融合方式和任务目标四个相互独立的维度定位一个方法。

## 定义与分类边界

“SVR”“KNN”“MLP”“PINN”“DeepONet”和“Diffusion Model”并不处于同一分类层级：SVR/KNN 是经典监督回归模型，MLP 是神经网络架构，PINN 是把物理约束写入训练的范式，DeepONet 是面向函数到函数映射的模型族，Diffusion Model 则通常按生成任务与训练机制界定。把它们放入同一棵互斥的分类树会混淆“使用什么模型”“模型学习什么”和“如何训练”。

因此，描述一个机器学习方法时，应先分别说明下列四个维度，再说明具体应用问题。

## 一、四个正交维度

| 维度 | 回答的问题 | 常见类别或实例 | 说明 |
|---|---|---|---|
| **模型族与架构** | 使用哪类预测机制；若使用神经网络，其计算图怎样组织信息与参数？ | 经典监督模型：线性回归、SVR、KNN、树模型；神经网络：MLP、CNN、Transformer、GNN 等 | 模型选择受样本规模、维度、数据拓扑和推理要求影响；同一模型或架构可服务不同学习对象与训练范式。 |
| **学习对象** | 模型近似的是一个函数、一个算子、表示还是分布？ | 函数学习、算子学习、表征／降维学习、生成建模 | 这是理解科学机器学习中模型角色的主维度，不能由网络名称直接判断。 |
| **训练信号与物理融合** | 参数由什么目标约束或更新？ | 监督学习、自监督学习、PINN residual 训练、能量／变分训练、混合训练 | PINN 是训练范式，不是一种固定神经网络架构；它可以使用 MLP，也可与数据监督或其他约束结合。 |
| **任务目标** | 输出服务于什么计算或决策？ | 求解／预测、分类、表示／降维、生成、控制与优化 | 一个模型可以同时服务多个目标；最终仍要以其进入真实计算链后的下游指标评价。 |

### 1. 模型族与神经网络架构

机器学习模型并不等于神经网络。SVR、KNN 和树模型等经典方法与 MLP、CNN、Transformer 等神经网络可以解决相同的监督预测任务，但其归纳偏置、样本需求、训练过程和部署成本不同。使用神经网络时，网络架构进一步规定计算图、参数共享方式与信息交互范围；它仍不直接规定模型学习的是函数还是算子，也不直接规定训练是否包含物理约束。

```text
模型族与架构
├─ 经典监督模型
│  ├─ 线性与核方法：线性回归、SVR
│  ├─ 邻域方法：KNN
│  └─ 树模型：Decision Tree、Random Forest、Gradient Boosting
└─ 神经网络
   ├─ 前馈网络：MLP
   ├─ 卷积网络：CNN、ResNet、U-Net
   ├─ 序列／注意力网络：RNN、LSTM、GRU、Transformer
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

| 方法示例 | 模型与架构 | 学习对象 | 训练范式 | 任务目标 |
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

## 四、经典监督回归基线：SVR 与 KNN

SVR 和 KNN 都可以处理有限维监督回归，但二者的预测机制不同。它们不是神经网络，也不决定学习对象是否具有物理意义；模型是否合适仍需结合样本规模、输入维度、特征尺度、输出结构和下游评价判断。

### 1. 支持向量回归

支持向量回归（Support Vector Regression, SVR）用带正则化的函数逼近训练数据。在线性特征空间中可写为

$$
f(\boldsymbol x)=\boldsymbol w^{\mathsf T}\phi(\boldsymbol x)+b,
$$

其中 $\phi$ 可以由核函数隐式定义。经典 $\varepsilon$-SVR 通过以下问题平衡函数平滑性与超过 $\varepsilon$ 容忍带的预测误差：

$$
\min_{\boldsymbol w,b,\boldsymbol\xi,\boldsymbol\xi^*}
\frac{1}{2}\lVert\boldsymbol w\rVert^2
+C\sum_{i=1}^{n}\left(\xi_i+\xi_i^*\right),
$$

并满足

$$
\begin{aligned}
y_i-f(\boldsymbol x_i)&\leq\varepsilon+\xi_i,\\
f(\boldsymbol x_i)-y_i&\leq\varepsilon+\xi_i^*,\\
\xi_i,\xi_i^*&\geq0.
\end{aligned}
$$

关键配置包括正则化参数 $C$、容忍带宽 $\varepsilon$、核函数及其参数。SVR 可以通过核处理非线性关系，但通常需要统一特征尺度；标准形式面向标量输出，向量输出常通过逐分量模型或多输出封装处理。

### 2. K 最近邻回归

K 最近邻（K-Nearest Neighbors, KNN）回归根据查询点附近的 $k$ 个训练样本直接形成预测。设 $\mathcal N_k(\boldsymbol x)$ 是按距离度量选出的邻域，则

$$
\widehat y(\boldsymbol x)
=
\frac{\displaystyle\sum_{i\in\mathcal N_k(\boldsymbol x)}\omega_i y_i}
{\displaystyle\sum_{i\in\mathcal N_k(\boldsymbol x)}\omega_i},
$$

其中 $\omega_i$ 可取常数，也可随距离衰减。关键配置包括邻居数 $k$、距离度量和权重方式。KNN 几乎没有参数拟合过程，但需要保存训练样本并在推理时搜索邻域；它对特征尺度和无关维度敏感，在高维空间中还会受到距离区分能力下降的影响。

### 3. 选型对比

| 维度 | SVR | KNN |
|---|---|---|
| 预测机制 | 正则化函数逼近，可借助核表示非线性 | 基于局部邻域的样本插值或平滑 |
| 主要超参数 | $C$、$\varepsilon$、核函数及核参数 | $k$、距离度量、邻域权重 |
| 特征缩放 | 重要，会影响间隔与核距离 | 重要，直接影响邻居选择 |
| 训练与推理 | 训练需求解优化问题；预测依赖支持向量数量 | 训练主要是保存数据；预测需要邻域搜索 |
| 样本与维度 | 常用于小到中等规模、经过适当表示的监督回归 | 低维且局部相似性可靠时直观有效，高维下易退化 |
| 外推能力 | 由核、正则化和训练范围共同决定，不能默认可靠 | 主要依赖训练样本覆盖，通常不适合远离样本的外推 |
| 物理保证 | 默认没有，需由表示、损失、后处理或下游求解补充 | 默认没有，需由表示、后处理或下游求解补充 |

该表只给出一般机制，不能脱离数据划分和超参数选择预判哪一种模型更优。两者都应使用独立验证／测试数据评价，并与最简单的常数、线性或其他问题相关基线比较。

具体论文采用了什么输入输出、样本规模、降维方式和评价指标，应由对应 `literature/` 精读页维护；本页只保留可跨论文复用的模型定义、选型维度和一般边界。

## 五、参考来源

- [Goodfellow, Bengio & Courville, *Deep Learning*](https://www.deeplearningbook.org/) — 神经网络与表征学习的基础教材。
- [Vaswani et al. (2017), *Attention Is All You Need*](https://arxiv.org/abs/1706.03762) — Transformer。
- [Scarselli et al. (2009), *The Graph Neural Network Model*](https://doi.org/10.1109/TNN.2008.2005605) — 图神经网络早期基础工作。
- [Kingma & Welling (2014), *Auto-Encoding Variational Bayes*](https://arxiv.org/abs/1312.6114)；[Goodfellow et al. (2014), *Generative Adversarial Nets*](https://arxiv.org/abs/1406.2661)；[Ho et al. (2020), *Denoising Diffusion Probabilistic Models*](https://arxiv.org/abs/2006.11239) — VAE、GAN 与 diffusion 的代表工作。
- [Raissi, Perdikaris & Karniadakis (2019), *Physics-informed neural networks*](https://doi.org/10.1016/j.jcp.2018.10.045) — PINN。
- [Lu et al. (2021), *Learning nonlinear operators via DeepONet*](https://doi.org/10.1038/s42256-021-00302-5)；[Li et al. (2021), *Fourier Neural Operator*](https://arxiv.org/abs/2010.08895) — 神经算子。
- [Smola & Schölkopf (2004), *A tutorial on support vector regression*](https://doi.org/10.1023/B:STCO.0000035301.49549.88) — SVR 的损失、核表示与优化基础。
- [Stone (1977), *Consistent Nonparametric Regression*](https://doi.org/10.1214/aos/1176343886) — 近邻等非参数回归的一致性基础。

## 相关页面

- [[pca-pod]] — PCA/POD 低维表示、系数和重构的一般数学定义。
- [[../research/workflows/machine-learning-workflow]] — 可重放机器学习项目的完整生命周期。
- [[../research/workflows/pinn-machine-learning-workflow]] — 一维 Poisson PINN 方法实例。
- [[../research/workflows/linear-elasticity-pinn-machine-learning-workflow]] — 小变形静力线弹性 PINN 方法契约。
- [[piml/ml-roles-and-boundaries]] — 计算力学中 PINN、PIML 等路线按计算角色的比较。
