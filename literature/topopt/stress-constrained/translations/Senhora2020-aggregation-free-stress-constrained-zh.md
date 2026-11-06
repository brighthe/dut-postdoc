---
title: "翻译：Topology optimization with local stress constraints: a stress aggregation-free approach"
tags:
  - translation
  - topology-optimization
  - stress-constraints
  - augmented-lagrangian
status: "draft"
date_created: 2026-10-13
date_updated: 2026-10-13
source: "../sources/Senhora2020-aggregation-free-stress-constrained.pdf"
citekey: "Senhora2020-aggregation-free-stress-constrained"
language: "zh-CN"
---

# Topology optimization with local stress constraints: a stress aggregation-free approach

---

# 信息

- **中文标题**：考虑局部应力约束的拓扑优化：一种无应力聚合方法
- **作者**：Fernando V. Senhora$^{1,2}$；Oliver Giraldo-Londoño$^1$；Ivan F. M. Menezes$^2$；Glaucio H. Paulino$^{1,*}$
- **单位**：
  - $1$: 佐治亚理工学院土木与环境工程学院（School of Civil and Environmental Engineering, Georgia Institute of Technology，亚特兰大，GA 30332，美国）
  - $2$: 里约热内卢天主教大学（Pontifical Catholic University of Rio de Janeiro (PUC-Rio)，里约热内卢，R.J. 22453，巴西）
- **期刊**：*Structural and Multidisciplinary Optimization*
- **卷 / 期 / 页码**：62(4): 1639–1668 (2020)[^issue-note]
- **DOI**：https://doi.org/10.1007/s00158-020-02573-9
- **收稿 / 修回 / 录用 / 在线发表**：2018-07-23 / 2020-02-27 / 2020-03-09 / 2020-08-20
- **通讯作者**：Glaucio H. Paulino（paulino@gatech.edu）

[^issue-note]: 译者注：原文 PDF 页眉印为 `Structural and Multidisciplinary Optimization (2020) 62:1639–1668`，期号 `4` 经 CrossRef 元数据核验。

# 摘要

本文借助增广拉格朗日（augmented Lagrangian, AL）方法，提出了一种考虑局部应力约束的质量最小化一致性拓扑优化列式。为了高效求解含大量约束的问题，我们对增广拉格朗日函数的惩罚项和目标函数项同时进行了修正：惩罚项的修正使算法在网格加密下获得一致的解，而目标函数项的修正则驱动质量最小化趋向黑白（0/1）解。此外，我们引入了一种分片消失约束（piecewise vanishing constraint），其所得结果优于采用松弛应力约束所得的结果。尽管保持应力的局部本质需要施加大量应力约束，但本文提出的列式仅需计算一个伴随向量，从而能够高效评估灵敏度。文中给出了若干二维与三维拓扑优化算例，每个算例均包含大量局部应力约束。

**关键词**：一致性拓扑优化（Consistent topology optimization）；增广拉格朗日（Augmented Lagrangian）；应力约束（Stress constraints）；应力松弛（Stress relaxation）；von Mises 应力（von Mises stress）；无聚合（Aggregation-free）

# 1 引言

> 全文逐段精译待补；本节核心内容与公式如下。

受 Cauchy 连续介质力学思想（Cauchy 四面体极限过程）的启发，本文在边值问题求解与优化阶段均将应力作为局部量处理：

$$
\boldsymbol{\sigma} \cdot \mathbf{n} = \lim_{\Delta a \to 0} \frac{\Delta \mathbf{f}(\mathbf{n})}{\Delta a},
\tag{1}
$$

其中 $\boldsymbol{\sigma}$ 为应力张量，$\mathbf{n}$ 为微元面积 $\mathrm{d}a$ 的法向单位向量，$\mathrm{d}\mathbf{f}(\mathbf{n})$ 为微元内力向量。

一致地求解局部应力约束拓扑优化面临两大挑战：
1. 应力需逐点满足，导致约束数量庞大、计算开销高昂；
2. 应力约束问题的最优解通常位于维数低于设计空间的退化区域（奇异最优解），需要基于梯度的优化算法能够进入这些退化区域。

本文采用增广拉格朗日（AL）方法配合分片消失约束（piecewise vanishing constraint），在每个优化步仅需额外求解一次伴随线性方程组即可处理全部局部应力约束。

# 2 相关工作

> 待翻译。本节综述柔顺度最小化的局限性、全局/分块应力聚合方法（KS 函数、$p$-范数与 $p$-均值、聚类方法）、有效集（active set）方法、拓扑导数方法、增广拉格朗日（AL）方法在密度法与水平集法中的应用，以及奇异最优解（MPVCs，带消失约束的数学规划）与松弛策略（$\varepsilon$-松弛、$qp$-松弛、光滑正则化、损伤方法及下界聚合松弛）的研究脉络。

# 3 奇异最优解简述

## 3.1 对角方域问题（Diagonal square problem）

> 待翻译。图 1 待提取。

为在变密度拓扑优化框架下演示奇异最优解现象（对应桁架拓扑优化中的经典三杆桁架问题），构造边长 $L = 2$、划分为 $2 \times 2$ 网格的对角方域问题：两个对角单元密度固定为 $1$，另外两个单元密度由设计变量 $\rho_1, \rho_2$ 控制。体积最小化列式为：

$$
\begin{aligned}
\min_{(\rho_1, \rho_2)} \quad & m(\rho_1, \rho_2) = \rho_1 + \rho_2 \\
\text{s.t.} \quad & g_1 = \frac{\sigma_1^v}{\sigma_{\mathrm{lim}}} - 1 \le 0, \quad \rho_1 > 0 \\
& g_2 = \frac{\sigma_2^v}{\sigma_{\mathrm{lim}}} - 1 \le 0, \quad \rho_2 > 0 \\
& 0 \le \rho_i \le 1, \quad i = 1, 2 \\
\text{with:} \quad & \mathbf{K}(\rho_1, \rho_2)\mathbf{u} = \mathbf{f},
\end{aligned}
\tag{2}
$$

其中 $\sigma_1^v, \sigma_2^v$ 为单元形心处的表观“局部”von Mises 应力（基于实体弹性矩阵 $\mathbf{D}_0$ 计算），$\sigma_{\mathrm{lim}} = 1$，单元刚度矩阵 $\mathbf{k}_e = [\epsilon + (1 - \epsilon)\rho_e^p]\mathbf{k}_0$，$p = 3$，Ersatz 刚度 $\epsilon = 1 \times 10^{-6}$，$E_0 = 1$，$\nu = 0.3$，外载 $\mathbf{P} = [0.1, -0.1]^{\mathsf{T}}$。当 $\rho_1 = 0$ 或 $\rho_2 = 0$ 时对应应力约束失效，全局最优解位于与可行域主体不连通的坐标轴退化区域上。

## 3.2 寻找奇异最优解的策略

> 待翻译。图 2 待提取。

- **消失约束（vanishing constraints，Cheng and Jiang 1992）**：

$$
\tilde{g}_1 = \rho_1 g_1 \quad \text{and} \quad \tilde{g}_2 = \rho_2 g_2.
\tag{3}
$$

- **$\varepsilon$-松弛方法（Cheng and Guo 1997; Duysinx and Sigmund 1998b）**：

$$
g_\varepsilon(\rho) = \frac{\sigma^v}{\sigma_{\mathrm{lim}}} - 1 - \frac{\varepsilon}{\rho} \le 0,
\tag{4}
$$

同时要求设计变量下界修改为 $\rho_i \ge \varepsilon^2$。

- **$qp$-松弛方法（Bruggi 2008）**：

$$
g_{qp}(\rho) = \rho^{p-q}\frac{\sigma^v}{\sigma_{\mathrm{lim}}} - 1 \le 0, \qquad q < p.
\tag{5}
$$

# 4 增广拉格朗日方法

> 待翻译。

针对含等式约束的优化问题：

$$
\begin{aligned}
\min_{\mathbf{z} \in \mathbb{R}^n} \quad & f(\mathbf{z}) \\
\text{s.t.} \quad & h_j(\mathbf{z}) = 0 \quad \forall j = 1, \dots, N_c,
\end{aligned}
\tag{6}
$$

AL 方法在第 $k$ 步求解如下无约束子问题：

$$
\min_{\mathbf{z} \in \mathbb{R}^n} \quad J^{(k)}(\mathbf{z}) = f(\mathbf{z}) + \sum_{j=1}^{N_c} \left[ \lambda_j^{(k)} h_j(\mathbf{z}) + \frac{\mu^{(k)}}{2} h_j(\mathbf{z})^2 \right],
\tag{7}
$$

子问题一阶最优性条件为：

$$
\nabla J^{(k)}(\mathbf{z}^{(k)}) = \nabla f(\mathbf{z}^{(k)}) + \sum_{j=1}^{N_c} \left[ \lambda_j^{(k)} + \mu^{(k)} h_j(\mathbf{z}^{(k)}) \right] \nabla h_j(\mathbf{z}^{(k)}) = \mathbf{0}.
\tag{8}
$$

与原问题 KKT 条件对比可得：

$$
\lambda_j^* \nabla h_j(\mathbf{z}^*) \approx \left[ \lambda_j^{(k)} + \mu^{(k)} h_j(\mathbf{z}^{(k)}) \right] \nabla h_j(\mathbf{z}^{(k)}),
\tag{9}
$$

即：

$$
\lambda_j^* \approx \lambda_j^{(k)} + \mu^{(k)} h_j(\mathbf{z}^{(k)}) \quad \text{or} \quad h_j(\mathbf{z}^{(k)}) \approx \frac{\lambda_j^* - \lambda_j^{(k)}}{\mu^{(k)}}.
\tag{10}
$$

据此给出拉格朗日乘子估计量与罚因子的更新格式：

$$
\lambda_j^{(k+1)} = \lambda_j^{(k)} + \mu^{(k)} h_j(\mathbf{z}^{(k)}), \quad \forall j = 1, \dots, N_c,
\tag{11}
$$

$$
\mu^{(k+1)} = \alpha \mu^{(k)}, \quad (\alpha > 1).
\tag{12}
$$

不等式约束的扩展推导见附录 A。

# 5 一致性应力约束拓扑优化列式

> 待翻译。

本文求解的应力约束质量最小化优化问题列式为：

$$
\begin{aligned}
\min_{\mathbf{z}} \quad & m(\mathbf{z}) = \sum_{e=1}^{N_e} \tilde{\rho}_e v_e \\
\text{s.t.} \quad & g_j(\mathbf{z}) \le 0, \quad j = 1, \dots, N_c \\
& 0 \le z_e \le 1, \quad e = 1, \dots, N_e \\
\text{with:} \quad & \mathbf{K}(\mathbf{z})\mathbf{u} = \mathbf{f},
\end{aligned}
\tag{13}
$$

全局刚度矩阵组装与 SIMP 插值为：

$$
\mathbf{K}(\mathbf{z}) = \operatorname*{\mathbb{A}}_{e=1}^{N_e} \mathbf{k}_e, \quad \text{with} \quad \mathbf{k}_e = [\epsilon + (1 - \epsilon)\rho_e^p]\mathbf{k}_0.
\tag{14}
$$

过滤密度 $\boldsymbol{\rho}(\mathbf{z}) = \mathbf{P}\mathbf{z}$ 采用多项式过滤器（Zegard and Paulino 2016）：

$$
P_{ij} = \frac{w_{ij}v_j}{\sum_{k=1}^{N_e} w_{ik}v_k}, \quad \text{with} \quad w_{ij} = \max\left[0, 1 - \frac{\|\mathbf{x}_i - \mathbf{x}_j\|_2}{r}\right]^s,
\tag{15}
$$

当 $s = 1$ 时退化为传统线性过滤器。质量函数中单元体积分数 $\tilde{\rho}_e$ 采用光滑 Heaviside 投影（Guest et al. 2004）以惩罚中间密度：

$$
\tilde{\rho}_e = 1 - e^{-\beta \rho_e(\mathbf{z})} + \rho_e(\mathbf{z}) e^{-\beta}, \quad (\beta \ge 0).
\tag{16}
$$

## 5.1 分片消失应力约束（Piecewise vanishing stress constraint）

> 待翻译。

为避免传统消失约束在 AL 函数中产生负惩罚项并保持 $C^1(\mathbf{z})$ 连续性，定义分片消失约束：

$$
g_j(\mathbf{z}) = \begin{cases} \rho_j^p (\sigma_j^v / \sigma_{\mathrm{lim}} - 1)^2 & \text{if } \sigma_j^v / \sigma_{\mathrm{lim}} > 1 \\ 0 & \text{otherwise}. \end{cases}
\tag{17}
$$

## 5.2 应力测度（Stress Measure）

> 待翻译。

基于 $qp$-松弛（取 $p - q = 0.5$），定义用于绘图与自适应权重更新的应力测度：

$$
\widetilde{\sigma}^v = \rho^{0.5}\sigma^v.
\tag{18}
$$

## 5.3 增广拉格朗日方法

> 待翻译。

引入三项修正（单元质量权重因子 $\gamma_e^{(k)}$、惩罚项缩放因子 $\eta$、界面惩罚项 $F(\mathbf{z})$）后，第 $k$ 个 AL 子问题的目标泛函为：

$$
J^{(k)}(\mathbf{z}) = \sum_{e=1}^{N_e} \gamma_e^{(k)} \tilde{\rho}_e v_e + \eta \sum_{j=1}^{N_c} \left[ \lambda_j^{(k)} g_j(\mathbf{z}) + \frac{\mu^{(k)}}{2} g_j(\mathbf{z})^2 \right] + \delta F(\mathbf{z}),
\tag{19}
$$

其中当过滤半径延拓（filter reduction）激活时 $\delta = 1$，否则 $\delta = 0$。

## 5.4 自适应权重因子 $\gamma_e$

> 待翻译。图 3 待提取。

为推动设计趋向黑白（0/1）并跳出高体积局部最优解，根据单元应力测度 $\widetilde{\sigma}_e^v$ 自适应更新 $\gamma_e^{(k)}$：

$$
\gamma_e^{(k+1)} = \begin{cases} \max(a_1 \gamma_e^{(k)} + b_1, \gamma_L) & \text{if } \widetilde{\sigma}_e^v > \sigma_{\mathrm{lim}} \\ \min(a_2 \gamma_e^{(k)} + b_2, \gamma_U) & \text{otherwise}, \end{cases}
\tag{20}
$$

随着优化收敛，$\widetilde{\sigma}_e^v \le \sigma_{\mathrm{lim}}$，使得 $\gamma_e^{(k)} \to \gamma_U$，目标函数仅乘以常数 $\gamma_U$，不改变原问题的最优点。

## 5.5 缩放因子 $\eta$

> 待翻译。

为在网格加密或粗化（约束数 $N_c$ 变化）时保持目标函数项与惩罚项的量级之比近似恒定，令：

$$
\eta = 1 / N_c.
\tag{21}
$$

# 6 灵敏度分析

> 待翻译。

由链式法则计算 AL 函数对设计变量的导数：

$$
\frac{\mathrm{d}J^{(k)}}{\mathrm{d}z_j} = \sum_{i=1}^{N_e} \frac{\partial J^{(k)}}{\partial \rho_i} \frac{\mathrm{d}\rho_i}{\mathrm{d}z_j} = \sum_{i=1}^{N_e} \frac{\partial J^{(k)}}{\partial \rho_i} P_{ij},
\tag{22}
$$

$$
\frac{\partial J^{(k)}}{\partial \rho_i} = \frac{\partial}{\partial \rho_i} \sum_{e=1}^{N_e} \gamma_e \tilde{\rho}_e v_e + \eta \frac{\partial}{\partial \rho_i} \sum_{j=1}^{N_c} \left[ \lambda_j g_j(\mathbf{z}) + \frac{\mu}{2} g_j(\mathbf{z})^2 \right].
\tag{23}
$$

目标函数部分与惩罚项部分分别为：

$$
\frac{\partial}{\partial \rho_i} \sum_{e=1}^{N_e} \gamma_e \tilde{\rho}_e v_e = \gamma_i \frac{\partial \tilde{\rho}_i}{\partial \rho_i} v_i = \gamma_i \left(\beta e^{-\beta \rho_i(\mathbf{z})} + e^{-\beta}\right) v_i,
\tag{24}
$$

$$
\frac{\partial}{\partial \rho_i} \sum_{j=1}^{N_c} \left[ \lambda_j g_j(\mathbf{z}) + \frac{\mu}{2} g_j(\mathbf{z})^2 \right] = \sum_{j=1}^{N_c} \left[ \lambda_j + \mu g_j(\mathbf{z}) \right] \frac{\partial g_j(\mathbf{z})}{\partial \rho_i}.
\tag{25}
$$

当约束激活时（利用 $g_j(\mathbf{z}) = h_j(\mathbf{z})$）：

$$
\begin{aligned}
\frac{\partial h_j(\mathbf{z})}{\partial \rho_i} &= \frac{\partial}{\partial \rho_i} \left[ \rho_j^p (\sigma_j^v / \sigma_{\mathrm{lim}} - 1)^2 \right] \\
&= p \rho_j^{p-1} \delta_{ij} (\sigma_j^v / \sigma_{\mathrm{lim}} - 1)^2 + \frac{2\rho_j^p}{\sigma_{\mathrm{lim}}} (\sigma_j^v / \sigma_{\mathrm{lim}} - 1) \left( \frac{\partial \sigma_j^v}{\partial \mathbf{u}} \right)^{\mathsf{T}} \frac{\partial \mathbf{u}}{\partial \rho_i}.
\end{aligned}
\tag{26}
$$

对平衡方程求导：

$$
\frac{\partial \mathbf{K}}{\partial \rho_i}\mathbf{u} + \mathbf{K}\frac{\partial \mathbf{u}}{\partial \rho_i} = \mathbf{0}.
\tag{27}
$$

引入伴随向量 $\boldsymbol{\xi}$：

$$
\begin{aligned}
\frac{\partial}{\partial \rho_i} \sum_{j=1}^{N_c} \left[ \lambda_j g_j(\mathbf{z}) + \frac{\mu}{2} g_j(\mathbf{z})^2 \right] &= \sum_{j=1}^{N_c} \left[ \lambda_j + \mu g_j(\mathbf{z}) \right] p \rho_j^{p-1} \delta_{ij} (\sigma_j^v / \sigma_{\mathrm{lim}} - 1)^2 \\
&\quad + \sum_{j=1}^{N_c} \left[ \lambda_j + \mu g_j(\mathbf{z}) \right] \frac{2\rho_j^p}{\sigma_{\mathrm{lim}}} (\sigma_j^v / \sigma_{\mathrm{lim}} - 1) \left( \frac{\partial \sigma_j^v}{\partial \mathbf{u}} \right)^{\mathsf{T}} \frac{\partial \mathbf{u}}{\partial \rho_i} \\
&\quad + \boldsymbol{\xi}^{\mathsf{T}} \left( \frac{\partial \mathbf{K}}{\partial \rho_i}\mathbf{u} + \mathbf{K}\frac{\partial \mathbf{u}}{\partial \rho_i} \right),
\end{aligned}
\tag{28}
$$

消去含 $\partial \mathbf{u} / \partial \rho_i$ 的项可得：

$$
\frac{\partial}{\partial \rho_i} \sum_{j=1}^{N_c} \left[ \lambda_j g_j(\mathbf{z}) + \frac{\mu}{2} g_j(\mathbf{z})^2 \right] = \left[ \lambda_i + \mu g_i(\mathbf{z}) \right] p \rho_i^{p-1} (\sigma_i^v / \sigma_{\mathrm{lim}} - 1)^2 + \boldsymbol{\xi}^{\mathsf{T}} \frac{\partial \mathbf{K}}{\partial \rho_i}\mathbf{u},
\tag{29}
$$

其中伴随向量 $\boldsymbol{\xi}$ 满足单一伴随方程：

$$
\mathbf{K}\boldsymbol{\xi} = -\sum_{j=1}^{N_c} \left[ \lambda_j + \mu g_j(\mathbf{z}) \right] \frac{2\rho_j^p}{\sigma_{\mathrm{lim}}} (\sigma_j^v / \sigma_{\mathrm{lim}} - 1) \frac{\partial \sigma_j^v}{\partial \mathbf{u}}.
\tag{30}
$$

利用单元刚度导数：

$$
\frac{\partial \mathbf{k}_i}{\partial \rho_i} = p(1 - \epsilon)\rho_i^{p-1}\mathbf{k}_0,
\tag{31}
$$

得到对过滤密度的偏导数及对设计变量的最终灵敏度：

$$
\frac{\partial J^{(k)}}{\partial \rho_i} = \gamma_i \left(\beta e^{-\beta \rho_i(\mathbf{z})} + e^{-\beta}\right) v_i + \eta \left[ \left(\lambda_i + \mu g_i(\mathbf{z})\right) p \rho_i^{p-1} (\sigma_i^v / \sigma_{\mathrm{lim}} - 1)^2 + p(1 - \epsilon)\rho_i^{p-1}\boldsymbol{\xi}_i^{\mathsf{T}}\mathbf{k}_0\mathbf{u}_i \right],
\tag{32}
$$

$$
\frac{\mathrm{d}J^{(k)}}{\mathrm{d}z_j} = \sum_{i=1}^{N_e} \gamma_i \left(\beta e^{-\beta \rho_i(\mathbf{z})} + e^{-\beta}\right) v_i P_{ij} + \eta \sum_{i=1}^{N_e} \left[ \left(\lambda_i + \mu g_i(\mathbf{z})\right) p \rho_i^{p-1} (\sigma_i^v / \sigma_{\mathrm{lim}} - 1)^2 + p(1 - \epsilon)\rho_i^{p-1}\boldsymbol{\xi}_i^{\mathsf{T}}\mathbf{k}_0\mathbf{u}_i \right] P_{ij}.
\tag{33}
$$

# 7 实现细节

## 7.1 非凸性处理（Addressing non-convexity）

> 待翻译。当优化停滞（`Change < tol` 且约束尚未满足）时，重启 AL 参数 $\mu, \lambda_j$ 及权重因子 $\gamma_e$（2D 最多重启 4 次，3D 最多重启 2 次）。

## 7.2 应力约束的严格满足（Achieving stress constraint satisfaction）

> 待翻译。

因为分片消失约束 (17) 在满足约束时梯度为零，为在接近收敛时实现严格的应力约束满足，以 $\gamma_e^{(k)}$ 作为违约指示器逐步降低未满足单元的人工应力上限 $\sigma_{\mathrm{lim}}^e$：

$$
\sigma_{\mathrm{lim}}^e = \left( \frac{\gamma_U \sigma_{\mathrm{lim}}^R + (1 - \sigma_{\mathrm{lim}}^R)\gamma_e^{(k)} - \gamma_L}{\gamma_U - \gamma_L} \right) \sigma_{\mathrm{lim}},
\tag{34}
$$

最大折减系数 $\sigma_{\mathrm{lim}}^R$ 按子问题递减：

$$
(\sigma_{\mathrm{lim}}^R)^{(k+1)} = \max\left(1.25(\sigma_{\mathrm{lim}}^R)^{(k)} - 0.26, \, 0.65\right).
\tag{35}
$$

## 7.3 过滤半径延拓（Continuation on filter radius）

> 待翻译。包含算法 1（`Filter_Reduction` 伪代码）与界面惩罚项（interphase penalization）：

$$
F(\mathbf{z}) = \frac{2}{N_e} \sum_{e=1}^{N_e} \bar{\rho}_e (1 - \bar{\rho}_e^3), \qquad (\bar{\boldsymbol{\rho}} = \mathbf{P}_0\mathbf{z}).
\tag{36}
$$

## 7.4 优化算法（Optimization algorithm）

> 待翻译。包含算法 2（`MODIFIED AUGMENTED LAGRANGIAN` 三层循环伪代码：外层重启循环、内层 AL 步循环、最内层 MMA 近似极小化循环）。

# 8 数值算例

> 待翻译。表 1 给出全部算例通用默认数值参数：$\lambda_j^{(1)} = 300$，$\mu^{(1)} = 5000$，$\gamma_e^{(1)} = 0.0$，$\alpha = 1.05$，$p = 3$，$\beta = 3$，$\mathbf{z}^{(1)} = 0.5$，$\epsilon = 10^{-6}$，$a_1, a_2, b_1, b_2 = 0.7, 2.5, -0.1, 0.5$，$\gamma_L, \gamma_U = 0, 4$，$\mathrm{tol} = 0.0005$，$\mathrm{outerTol} = 0.2\,\mathrm{tol}$，$\mathrm{maxOuterIter} = 4\text{ (2D)}$ 或 $2\text{ (3D)}$；MMA 参数为 $\mathrm{asyinit} = 0.2, \mathrm{asyinc} = 1.2, \mathrm{asydec} = 0.7, \mathrm{move} = 0.1$。

## 8.1 对角方域算例（Diagonal square）

> 待翻译。图 4 待提取。

## 8.2 二维 L 形支架（2D L-bracket）

> 待翻译。图 5、表 2、表 3、图 6 待提取与整理（对比 16,380 / 160,000 / 500,000 网格下线性过滤、多项式过滤 $s=3$、Heaviside 投影与过滤半径缩减策略）。

### 8.2.1 正则化技术的影响（Effect of regularization techniques）

> 待翻译。分析实体与孔洞之间扩散过渡带（中间密度）引起的局部表观 von Mises 应力尖峰，以及通过过滤半径缩减消除伪应力集中的机理。

## 8.3 多工况二维扳手（2D Wrench with multiple load cases）

> 待翻译。表 4、图 7、图 8 待提取与整理（100,000 个多边形单元，PolyMesher + PolyTop，2 个载荷工况，共 $N_c = 2N_e = 200,000$ 个局部应力约束）。

## 8.4 三维 L 形支架（3D L-bracket）

> 待翻译。图 9、图 10 待提取（265,000 与 1,728,000 个六面体单元）。

## 8.5 三维门式刚架（3D portal frame）

> 待翻译。图 11、表 5、图 12、图 13 待提取与整理（633,240 与 1,236,375 个单元）。

# 9 计算效率评估

> 待翻译。表 6 汇总全部二维与三维算例的网格规模、正则化方式、MMA 总迭代次数与计算耗时（2D 采用 Cholesky 分解并复用前后代回代求解状态与伴随方程；3D 采用 MATLAB GPU 实现的 Jacobi 预条件共轭梯度法 PCG）。

# 10 结论

> 待翻译。

# 致谢

谨以此文纪念 Augustin-Louis Cauchy（1789 年 8 月 21 日 – 1857 年 5 月 23 日）。感谢 Emily D. Sanders 女士提出的宝贵建议，这些建议有助于改进本手稿。

**资助信息（Funding information）**：F.V.S.、O.G.-L. 与 G.H.P. 感谢美国国家科学基金会（US National Science Foundation，批准号 #1663244）以及佐治亚理工学院 Raymond Allen Jones 讲席教授基金的资助。F.V.S. 与 I.F.M.M. 感谢巴西资助机构 CNPQ 和 FAPERJ 以及巴西里约热内卢天主教大学计算机图形技术组（Tecgraf/PUC-Rio）提供的支持。

# 伦理标准合规声明（Compliance with ethical standards）

- **利益冲突声明（Conflict of interest）**：作者声明不存在利益冲突。
- **结果可复现性声明（Replication of results）**：本文包含数值实现的详细说明，并给出了全部数值算例的输入参数以便复现结果。为促进本文原创思想的传播，我们随后在 SMO 期刊发表了一篇面向应力约束拓扑优化的教学论文及配套 Matlab 代码（Giraldo-Londoño and Paulino 2020）。

# 附录 A：面向不等式约束的增广拉格朗日方法

> 待翻译。

对于不等式约束优化问题：

$$
\begin{aligned}
\min_{\mathbf{z} \in \mathbb{R}^n} \quad & f(\mathbf{z}) \\
\text{s.t.} \quad & g_j(\mathbf{z}) \le 0 \quad \forall j = 1, \dots, N_c \\
& \mathbf{L} \le \mathbf{z} \le \mathbf{U},
\end{aligned}
\tag{37}
$$

引入松弛变量 $s_j \ge 0$ 将不等式约束转化为等式约束：

$$
h_j(\mathbf{z}) = g_j(\mathbf{z}) + s_j = 0, \quad s_j \ge 0, \quad j = 1, \dots, N_c.
\tag{38}
$$

第 $k$ 步近似子问题为：

$$
\begin{aligned}
\min_{\mathbf{z}, \mathbf{s}} \quad & J^{(k)}(\mathbf{z}, \mathbf{s}) = f(\mathbf{z}) + \sum_{j=1}^{N_c} \left[ \lambda_j^{(k)} \left(g_j(\mathbf{z}) + s_j\right) + \frac{\mu^{(k)}}{2} \left(g_j(\mathbf{z}) + s_j\right)^2 \right] \\
\text{s.t.} \quad & \mathbf{L} \le \mathbf{z} \le \mathbf{U} \\
& s_j \ge 0 \quad \forall j = 1, \dots, N_c.
\end{aligned}
\tag{39}
$$

对固定 $\mathbf{z}$，关于 $s_j$ 的极小化问题：

$$
\begin{aligned}
\min_{s_j} \quad & \left[ \lambda_j^{(k)} \left(g_j(\mathbf{z}) + s_j\right) + \frac{\mu^{(k)}}{2} \left(g_j(\mathbf{z}) + s_j\right)^2 \right] \\
\text{s.t.} \quad & s_j \ge 0
\end{aligned}
\tag{40}
$$

具有闭式解：

$$
s_j = \max\left[0, -\left(\frac{\lambda_j^{(k)}}{\mu^{(k)}} + g_j(\mathbf{z})\right)\right] \quad \forall j = 1, \dots, N_c.
\tag{41}
$$

代入式 (38) 得：

$$
h_j(\mathbf{z}) = \max\left[g_j(\mathbf{z}), -\frac{\lambda_j^{(k)}}{\mu^{(k)}}\right] \quad \forall j = 1, \dots, N_c.
\tag{42}
$$

将分片消失约束式 (17) 代入式 (42) 时（因 $\lambda_j^{(k)} \ge 0, \mu^{(k)} > 0, g_j(\mathbf{z}) \ge 0$），恒有 $h_j(\mathbf{z}) = g_j(\mathbf{z})$。

# 附录 B：表观“局部”von Mises 应力与应力测度对比

> 待翻译。图 14 待提取。

# 附录 C：分片消失约束与 $\varepsilon$-松弛对比

> 待翻译。图 15 待提取。

# 附录 D：权重因子 $\gamma_e$ 的影响

> 待翻译。图 16 待提取。

# 附录 E：缩放因子 $\eta$ 的影响

> 待翻译。图 17 待提取。

# 附录 F：AL 参数重启次数的影响

> 待翻译。图 18 待提取。

# 附录 G：应力上限 $\sigma_{\mathrm{lim}}$ 的影响

> 待翻译。图 19 待提取。

# 附录 H：符号表（Nomenclature）

> 待翻译。

---

# 参考文献

Achtziger W, Kanzow C (2008) Mathematical programs with vanishing constraints: optimality conditions and constraint qualifications. Math Program 114(1):69–99

Achtziger W, Hoheisel T, Kanzow C (2013) A smoothing-regularization approach to mathematical programs with vanishing constraints. Comput Optim Appl 55(3):733–767

Amstutz S, Novotny AA (2010) Topological optimization of structures subject to von Mises stress constraints. Struct Multidiscip Optim 41(3):407–420

Andreani R, Haeser G, Schuverdt M, Silva P (2012) A relaxed constant positive linear dependence constraint qualification and applications. Math Program 135(1–2):255–273

Bell E. T. (1986) Men of Mathematics. Simon and Schuster

Bendsøe MP (1989) Optimal shape design as a material distribution problem. Struct Optim 1:193–202

Bendsøe MP, Kikuchi N (1988) Generating optimal topologies in structural design using a homogenization method. Comput Methods Appl Mech Eng 71(2):197–224

Bendsøe MP (1995) Optimization of structural topology, shape, and material. Springer, Berlin

Bendsøe MP, Sigmund O (1999) Material interpolation schemes in topology optimization. Arch Appl Mech 69(9–10):635–654

Bendsøe MP, Sigmund O (2003) Topology optimization: theory, methods and applications. Springer, Berlin

Bertsekas DP (1996) Constrained optimization and Lagrange multiplier methods (ptimization and Neural Computation Series), 1 ed. Athena Scientific

Bertsekas DP (1999) Nonlinear programming, 2nd ed. Athena Scientific

Borrvall T, Petersson J (2001) Topology optimization using regularized intermediate density control. Comput Methods Appl Mech Eng 190(37–38):4911–4928

Bourdin B (2001) Filters in topology optimization. Int J Numer Methods Eng 50(9):2143–2158

Bruggi M (2008) On an alternative approach to stress constraints relaxation in topology optimization. Struct Multidiscip Optim 36(2):125–141

Bruggi M, Duysinx P (2012) Topology optimization for minimum weight with compliance and stress constraints. Struct Multidiscip Optim 46(3):369–384

Cauchy AL (1827) De la pression ou tension dans un corps solide. Exercices Math 2:42–56

Cheng G, Jiang Z (1992) Study on topology optimization with stress constraints. Eng Optim 20(2):129–148

Cheng G (1995) Some aspects on truss topology optimization. Struct Optim 10(3–4):173–179

Cheng G, Guo X (1997) $\varepsilon$-relaxed approach in structural topology optimization. Struct Optim 13(4):258–266

Christensen P, Klarbring A (2008) An introduction to structural optimization. Solid Mechanics and Its Applications. Springer, Netherlands

da Silva GA, Beck AT, Sigmund O (2019) Stress-constrained topology optimization considering uniform manufacturing uncertainties. Comput Methods Appl Mech Eng 344:512–537

Duysinx P, Bendsøe MP (1998a) Topology optimization of continuum structures with local stress constraints. Int J Numer Methods Eng 43(8):1453–1478

Duysinx P, Sigmund O (1998b) New developments in handling stress constraints in optimal material distribution. In: Proceedings of the 7th AIAA/USAF/NASA/ISSMO Symposium on Multidisciplinary Analysis and Optimization, vol 1, pp 1501–1509

Emmendoerfer Jr, H, Fancello EA (2014) A level set approach for topology optimization with local stress constraints. Int J Numer Methods Eng 99(2):129–156

Emmendoerfer Jr, H, Fancello EA (2016) Topology optimization with local stress constraint based on level set evolution via reaction-diffusion. Comput Methods Appl Mech Eng 305:62–88

Ermoliev YM, Kryazhimskii AV, Ruszczyński A (1997) Constraint aggregation principle in convex optimization. Math Program 76(3):353–372

Gibson I, Rosen D, Stucker B (2015) Additive manufacturing technologies: 3D printing, rapid prototyping, and direct digital manufacturing, vol 2. Springer, Berlin

Giraldo-Londoño O, Paulino GH (2020) PolyStress: a Matlab implementation for local stress-constrained topology optimization considering material nonlinearity. Struct Multidiscip Optim. https://doi.org/10.1007/s00158-020-02664-7

Guest JK, Prévost JH, Belytschko T (2004) Achieving minimum length scale in topology optimization using nodal design variables and projection functions. Int J Numer Methods Eng 61(2):238–254

Guo X, Zhang WS, Wang MY, Wei P (2011) Stress-related topology optimization via level set approach. Comput Methods Appl Mech Eng 200(47–48):3439–3452

Gurtin ME (1981) An introduction to continuum mechanics, vol 158. Academic Press

Hoheisel T, Kanzow C (2008) Stationary conditions for mathematical programs with vanishing constraints using weak constraint qualifications. J Math Anal Appl 337(1):292–310

Holmberg E, Torstenfelt B, Klarbring A (2013) Stress constrained topology optimization. Struct Multidiscip Optim 48(1):33–47

Izmailov AF, Solodov MV, Uskov EI (2012) Global convergence of augmented lagrangian methods applied to optimization problems with degenerate constraints, including problems with complementarity constraints. SIAM J Optim 22(4):1579–1606

James K, Lee E, Martins J (2012) Stress-based topology optimization using an isoparametric level set method. Finite Elem Anal Des 58:20–30

Kirsch U (1989) Optimal topologies in truss structures. Comput Methods Appl Mech Eng 72(1):15–28

Kirsch U, Taye S (1986) On optimal topology of grillage structures. Eng Comput 1:229–243

Kirsch U (1990) On singular topologies in optimum structural design. Struct Optim 2(3):133–142

Kiyono C, Vatanabe S, Silva E, Reddy J (2016) A new multi-p-norm formulation approach for stress-based topology optimization design. Compos Struct 156:10–19. 70th Anniversary of Professor J. N. Reddy

Kreisselmeier G, Steinhauser R (1979) Systematic control design by optimizing a vector performance index. IFAC Proc Vol 12(7):113–117. IFAC Symposium on computer Aided Design of Control Systems, Zurich, Switzerland

Le C, Norato J, Bruns T, Ha C, Tortorelli D (2010) Stress-based topology optimization for continua. Struct Multidiscip Optim 41(4):605–620

Lee E, James KA, Martins JRRA (2012) Stress-constrained topology optimization with design-dependent loading. Struct Multidiscip Optim 46(5):647–661

Lian H, Christiansen AN, Tortorelly DA, Sigmund O (2017) Combined shape and topology optimization for minimization of maximal von Mises stress. Struct Multidiscip Optim 55(5):1541–1557

Love AEH (1892) A treatise on the mathematical theory of elasticity, Vol 1. Cambridge University Press, Cambridge

Malvern LE (1969) Introduction to the mechanics of a continuous Mmedium. Prentice-Hall

Navarrina F, Muiños I, Colominas I, Casteleiro M (2005) Topology optimization of structures: a minimum weight approach with stress constraints. Adv Eng Softw 36(9):599–606

Nocedal J, Wright SJ (2006) Numerical optimization, 2nd ed. Springer, Berlin

Paris J, Navarrina F, Colominas I, Casteleiro M (2009) Topology optimization of continuum structures with local and global stress constraints. Struct Multidiscip Optim 39(4):419–437

Paris J, Navarrina F, Colominas I, Casteleiro M (2010) Block aggregation of stress constraints in topology optimization of structures. Adv Eng Softw 41(3):433–441

Park YK (1995) Extensions of optimal layout design using the homogenization method. Ph.D thesis, University of Michigan, Ann Arbor

Pereira JT, Fancello EA, Barcellos CS (2004) Topology optimization of continuum structures with material failure constraints. Struct Multidiscip Optim 26(1–2):50–66

Petersson J (2001) On continuity of the design-to-state mappings for trusses with variable topology. Int J Eng Sci 39(10):1119–1141

Rozvany GIN, Birker T (1994) On singular topologies in exact layout optimization. Struct Optim 8(4):228–235

Rozvany GIN (2001) On design-dependent constraints and singular topologies. Struct Multidiscip Optim 21(2):164–172

Sharma A, Maute K (2018) Stress-based topology optimization using spatial gradient stabilized XFEM. Struct Multidiscip Optim 57(1):17–38

Sigmund O (2007) Morphology-based black and white filters for topology optimization. Struct Multidiscip Optim 33(4–5):401–424

Sigmund O (2009) Manufacturing tolerant topology optimization. Acta Mech Sinica 25(2):227–239

Stolpe M, Svanberg K (2001) On the trajectories of the epsilon-relaxation approach for stress-constrained truss topology optimization. Struct Multidiscip Optim 21(2):140–151

Svanberg K (1987) The method of moving asymptotes—a new method for structural optimization. Int J Numer Methods Eng 24(2):359–373

Sved G, Ginos Z (1968) Structural optimization under multiple loading. Int J Mech Sci 10(10):803–805

Talischi C, Paulino GH, Pereira A, Menezes IFM (2012a) PolyMesher: a general-purpose mesh generator for polygonal elements written in Matlab. Struct Multidiscip Optim 45(3):309–328

Talischi C, Paulino GH, Pereira A, Menezes IFM (2012b) PolyTop: a Matlab implementation of a general topology optimization framework using unstructured polygonal finite element meshes. Struct Multidiscip Optim 45(3):329–357

Talischi C, Paulino GH (2013) An operator splitting algorithm for Tikhonov-regularized topology optimization. Comput Methods Appl Mech Eng 253:599–608

Timoshenko S, Goodier JN (1951) Theory of elasticity, 2 ed. McGraw-Hill

Verbart A, Langelaar M, van Keulen F (2016) Damage approach: a new method for topology optimization with local stress constraints. Struct Multidiscip Optim 53(5):1081–1098

Verbart A, Langelaar M, Keulen F. v. (2017) A unified aggregation and relaxation approach for stress-constrained topology optimization. Struct Multidiscip Optim 55(2):663–679

Wang MY, Wang S (2005) Bilateral filtering for structural topology optimization. Int J Numer Methods Eng 63(13):1911–1938

Wang F, Lazarov BS, Sigmund O (2011) On projection methods, convergence and robust formulations in topology optimization. Struct Multidiscip Optim 43(6):767–784

Wong KV, Hernandez A (2012) A review of additive manufacturing. ISRN Mechanical Engineering 2012, pp 1–10

Xia Q, Shi T, Liu S, Wang MY (2012) A level set solution to the stress-based structural shape and topology optimization. Comput Struct 90:55–64

Xu S, Cai Y, Cheng G (2010) Volume preserving nonlinear density filter based on Heaviside functions. Struct Multidiscip Optim 41(4):495–505

Yang RJ, Chen CJ (1996) Stress-based topology optimization. Struct Optim 12(2):98–105

Zegard T, Paulino GH (2016) Bridging topology optimization and additive manufacturing. Struct Multidiscip Optim 53(1):175–192
