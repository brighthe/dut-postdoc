---
title: "MMC 数学基础：显式组件、TDF、Ersatz 与优化闭环"
type: concept
aliases:
  - MMC mathematical foundations
  - Moving Morphable Components
  - 移动可变形组件
tags:
  - MMC
  - topology-opt
  - TDF
  - ersatz
  - MMA
status: in-progress
date_added: 2026-07-31
date_update: 2026-08-02
---

# MMC 数学基础：显式组件、TDF、Ersatz 与优化闭环

> **一句话**：MMC 用有限个具有明确几何意义的组件参数描述结构边界，通过 TDF 把显式几何投影到分析模型，再由状态方程、灵敏度和优化器更新组件位置、尺寸与形状。

## 1. 组件设计变量

二维可变厚度组件可由

$$
\boldsymbol D_i
=
\left(
x_{0i},y_{0i},L_i,t_{i1},t_{i2},t_{i3},\theta_i
\right)^{\mathrm T}
$$

描述，其中 $(x_{0i},y_{0i})$ 是中心，$L_i$ 是半长，$t_{i1},t_{i2},t_{i3}$ 控制沿轴向变化的半宽，$\theta_i$ 是倾角。实际代码也可能用 $\sin\theta_i$ 作为优化变量以改善数值稳定性，因此参数含义与存储参数必须在实现契约中分别说明。

$n$ 个组件的整体设计向量为

$$
\boldsymbol D
=
\left(
\boldsymbol D_1^{\mathrm T},
\ldots,
\boldsymbol D_n^{\mathrm T}
\right)^{\mathrm T}.
$$

## 2. 局部坐标与 TDF

对第 $i$ 个组件，先将全局坐标旋转到组件局部坐标：

$$
\begin{bmatrix}
x'\\y'
\end{bmatrix}
=
\begin{bmatrix}
\cos\theta_i & \sin\theta_i\\
-\sin\theta_i & \cos\theta_i
\end{bmatrix}
\begin{bmatrix}
x-x_{0i}\\
y-y_{0i}
\end{bmatrix}.
$$

为与“组件内部为正”的约定及 Zhang 2016 附录代码中的前置负号一致，一种可变厚度超椭圆型拓扑描述函数写为

$$
\phi_i(x,y)
=
1
-
\left(\frac{x'}{L_i}\right)^p
-
\left(\frac{y'}{f_i(x')}\right)^p,
$$

其中 $p$ 为偶数，$f_i(x')$ 由厚度参数控制。本文采用与 Zhang 2016 一致的符号约定：

$$
\phi_i>0\ \text{表示组件内部},\qquad
\phi_i=0\ \text{表示边界},\qquad
\phi_i<0\ \text{表示组件外部}.
$$

当前入库译文转写的式 (3) 显示为相反号，而附录 `tPhi` 实现使用
`-((x'/L_i)^p+(y'/f_i)^p-1)`；本页采用与代码及式 (1)–(2) 的“正内负外”约定一致的形式。不同文献或代码可能采用相反符号，复现时必须把 TDF、Heaviside 和材料侧约定一起核对。

## 3. 多组件并集与拓扑变化

固体结构是多个组件的并集：

$$
\Omega_s
=
\bigcup_{i=1}^{n}\Omega_i.
$$

在上述符号约定下，整体 TDF 可写为

$$
\phi_s(\boldsymbol x;\boldsymbol D)
=
\max_{1\le i\le n}\phi_i(\boldsymbol x;\boldsymbol D_i).
$$

组件的移动、变形、重叠和隐藏共同产生布局、形状与拓扑变化。`max` 聚合在组件交界处不光滑；具体实现需要说明是直接忽略该非光滑性、采用平滑聚合，还是使用其他灵敏度处理。

## 4. 从显式几何到 Ersatz 有限元

固定背景网格上，可以在单元节点评价 $\phi_s$，再用正则化 Heaviside 函数 $H_\epsilon$ 将几何映射为材料系数。对四节点单元，一种常用插值为

$$
E_e
=
\frac{E}{4}
\sum_{a=1}^{4}
\left[
H_\epsilon\left(\phi_a^e\right)
\right]^q.
$$

其中 $q>1$ 为惩罚指数，$H_\epsilon$ 的弱材料下限用于避免全局刚度矩阵奇异。于是得到

$$
\boldsymbol K(\boldsymbol D)\boldsymbol U
=
\boldsymbol F.
$$

Ersatz 路径实现简单，但 TDF 节点插值、正则化宽度和背景网格会引入边界与刚度误差。它是一个可复现基线，不代表精确边界积分。

## 5. 柔顺度与体积约束

在线弹性柔顺度最小化中，可写成

$$
\min_{\boldsymbol D}
\quad
C(\boldsymbol D)
=
\boldsymbol F^{\mathrm T}\boldsymbol U,
$$

满足

$$
\boldsymbol K(\boldsymbol D)\boldsymbol U
=
\boldsymbol F,
\qquad
V(\boldsymbol D)\le \bar V,
\qquad
\boldsymbol D\in U_D.
$$

对任意几何参数 $a$，伴随消元后的柔顺度灵敏度具有统一形式

$$
\frac{\partial C}{\partial a}
=
-\boldsymbol U^{\mathrm T}
\frac{\partial\boldsymbol K}{\partial a}
\boldsymbol U.
$$

体积灵敏度则来自 $H_\epsilon(\phi_s)$ 对几何参数的导数。解析、自动微分或有限差分都可以实现，但必须通过独立梯度检查确认符号、尺度和组件索引正确。

## 6. 优化闭环

一个最小 MMC 优化循环为：

```text
组件参数 D
  -> 节点 TDF 与多组件聚合
  -> Heaviside / Ersatz 材料系数
  -> 刚度组装与状态求解
  -> 柔顺度、体积及灵敏度
  -> MMA 更新 D
  -> 收敛检查
```

停止条件至少应记录最大设计变量变化、目标变化、约束残差、最大迭代数和状态求解失败。优化器收敛不自动等于找到全局最优；不同初始组件、参数边界和数值平滑可能得到不同局部最优结构。

## 7. 组件对应与表示非唯一

当 MMC 设计向量用作机器学习标签时，还存在一个独立于有限元误差的表示问题：

- 交换两个组件编号，可能得到相同结构但不同向量；
- 组件重叠或被完全覆盖后，其参数可能对当前实体边界不再敏感；
- 退化组件的长度或厚度接近下界时，参数小变化未必对应可见几何变化；
- 两个参数向量接近，不保证 TDF、材料场或结构响应同样接近。

因此，在对一组 MMC 设计做 PCA 或监督回归前，应冻结组件初始布局与编号，并检查跨样本组件对应。评价时至少区分：

1. 设计向量误差；
2. TDF 或材料场差异；
3. 柔顺度、体积和其他物理响应误差。

只比较设计向量的均方误差不能证明预测拓扑在力学上准确。

## 8. 数值验证门禁

一个数学上可信的 MMC 基线至少应通过：

1. 单组件 TDF 的平移、旋转、长度和厚度测试；
2. 多组件并集、重叠和隐藏测试；
3. Heaviside 极限值与材料侧符号测试；
4. 单元刚度和全局状态方程的独立对照；
5. 柔顺度与体积灵敏度的有限差分检查；
6. 体积约束和设计变量边界检查；
7. 固定输入下的可重放优化结果及完整收敛历史。

## 来源与证据

- [[../../literature/topology-opt/notes/Zhang2016-MMC-topology]] — 可变厚度 MMC、Ersatz 有限元、灵敏度与 MATLAB 实现。
- [[../../literature/topology-opt/translations/Zhang2016-MMC-topology-zh]] — 本页公式和数值实现边界的原文对应译文。
- [[../../research/mmc-mmv/mmc-mmv-numerical-discretization-survey]] — Ersatz、精确边界积分与先进离散路线的比较。
- [[../linear-elasticity]] — 线弹性状态方程与有限元离散。

## 在我研究中的位置

MMC 是显式拓扑优化与低维设计表示的基础，可作为代理模型标签生成和几何—分析接口研究的对象。是否进一步使用 PCA、SVR/KNN、Problem-Independent PIML 或高性能求解，需要由具体学习对象和下游任务决定。

## 相关页面

- [[_index]] — MMC 主题入口。
- [[../../literature/topology-opt/notes/Lei2018-machinelearningdriven#模型选型证据卡]] — MMC 低维表示在问题相关最终设计预测中的论文证据。
