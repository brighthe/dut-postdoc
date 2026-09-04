---
title: "局部应力约束拓扑优化"
type: concept
aliases:
  - Stress-Constrained Topology Optimization
  - Stress Relaxation
  - Singularity Phenomenon
  - 应力约束拓扑优化
  - 应力松弛
  - 应力奇异性
tags:
  - topology-optimization
  - density-method
  - stress-constraint
  - relaxation
status: "draft"
date_added: 2026-09-02
date_update: 2026-09-02
---

# 局部应力约束拓扑优化

> 以体积为目标、逐单元局部 von Mises 应力为约束的变密度拓扑优化：其松弛约束模型只在密度端点上与真实屈服条件一致，中间密度是模型盲区，由此决定了停机判据的正确写法与投影的必要性。

## 1. 问题设定与应力奇异性

与体积约束下的柔顺度最小化不同，应力约束问题把强度条件直接写成逐单元的局部不等式约束，以材料用量为目标：

$$
\min_{\rho}\ V(\bar\rho)
\quad\text{s.t.}\quad
\sigma_{\mathrm{vm}}(\bar\rho_e) \le \bar\sigma,\ e = 1,\dots,N_e ,
$$

其中 $\bar\rho$ 为经过滤与投影后的物理密度（过滤—投影链条本身见 [[regularization-and-length-scale-control]]），$\bar\sigma$ 为许用应力。该表述带来两个在柔顺度问题中不存在的困难：

1. **应力奇异性（singularity phenomenon）**：低密度区刚度趋零，但按插值后的弹性张量算出的应力并不同步趋零，形成非物理的虚假应力；直接施加 $\sigma_{\mathrm{vm}} \le \bar\sigma$ 会使可行域在 $\rho \to 0$ 处退化为低维子集，优化器无法把材料删干净。Duysinx 与 Bendsøe [1] 首先系统分析了该现象并给出 $\varepsilon$-松弛处理。
2. **约束规模**：约束数与单元数同阶，逐条处理代价高，通常以 p-norm、KS 等聚合函数或增广 Lagrange 方法收敛到少数全局约束 [2-4]。

## 2. $\varepsilon$-松弛约束模型与它的盲区

消除奇异性的常用做法是把约束改写为松弛形式

$$
g_e = \frac{\sigma_{\mathrm{vm}}^{\mathrm{app}}(\bar\rho_e)}{\bar\sigma} - \eta(\bar\rho_e) \le 0,
\qquad
\eta(\bar\rho_e) = \bar\rho_e^{\,p} + \varepsilon\big(1 - \bar\rho_e^{\,p}\big),
$$

其中 $\sigma_{\mathrm{vm}}^{\mathrm{app}}$ 为表观应力。本项目所用的无分母表观应力形式与式中记号见 [[../../papers/arbitrary-order-huzhang-topopt-draft-zh]] §4.1、§4.3。

该模型**只在两个端点上与真实屈服条件一致**：$\bar\rho = 1$ 时 $\eta = 1$，严格恢复 $\sigma_{\mathrm{vm}} \le \bar\sigma$；$\bar\rho \to 0$ 时表观应力与阈值同时趋零，约束平滑退化为良定的 $-\varepsilon \le 0$。中间密度处的 $\eta$ 是人为插值，**不对应任何真实材料的强度**——中间密度是该模型的盲区。

## 3. 停机判据陷阱

由盲区得到一个实践上容易踩的推论：若以**未减去阈值**的度量 $\max_e \sigma_{\mathrm{vm}}^{\mathrm{app}}/\bar\sigma \le 1$ 作为达标或停机判据（工程实现中常见，因为它直观且与真实屈服条件同形），则灰度设计的表观应力带有刚度插值因子而被系统性压低，可以在**不改善构型**的前提下取得"名义达标"。该判据与真实约束 $g_e \le 0$ 等价，当且仅当设计已近似取到 $\{0,1\}$。

这一"灰度驻点"现象已在 SOPTX 的悬臂梁应力约束算例上观测到；实测轨迹与参数取值由 `soptx:experiments/huzhang_topopt_paper/results_analysis.md` 维护，本页不复制其中数字。

## 4. 与过滤—投影链条的耦合

在体积约束下的柔顺度最小化中，黑白化有自发驱动力，密度过滤本身就能收敛到接近 0/1 的设计；而在以体积为目标的局部应力约束问题中，这种驱动力不存在：目标只推动密度整体下降，约束在中间密度处又只受人为插值 $\eta$ 支配。因此投影不是构型修饰，而是使停机判据与约束模型自洽的必要环节；只用密度过滤会停在应力约束不激活的灰度驻点上。两类问题的对照见 [[regularization-and-length-scale-control]] §6。

## 5. 谱系定位与待补方向

- **松弛谱系**：$\varepsilon$-松弛 [1] 与 qp 松弛的关系、二者对 $\eta$ 形状的影响，待补。
- **约束聚合**：聚类 p-norm 聚合 [3]、增广 Lagrange 逐单元处理 [4] 是 SOPTX 应力约束算例的直接参照（PolyFilter 三次密度过滤、tanh 投影参数取值亦源于 [4]），细节待译文完成后回填；两篇 PDF 已在 `literature/topopt/stress-constrained/sources/`。
- **混合元框架**：以 Hu–Zhang 元（[[../huzhang/huzhang-mixed-fem]]）直接求解应力场时，表观应力随密度自然衰减，可免除人工松弛，机理见博士论文第五章 [5]，待提炼入本页。

## 参考文献

[1] DUYSINX P, BENDSØE M P. Topology optimization of continuum structures with local stress constraints[J]. International Journal for Numerical Methods in Engineering, 1998, 43(8): 1453-1478.
[2] LE C, NORATO J, BRUNS T, et al. Stress-based topology optimization for continua[J]. Structural and Multidisciplinary Optimization, 2010, 41(4): 605-620.
[3] HOLMBERG E, TORSTENFELT B, KLARBRING A. Stress constrained topology optimization[J]. Structural and Multidisciplinary Optimization, 2013, 48(1): 33-47.
[4] GIRALDO-LONDOÑO O, PAULINO G H. PolyStress: a Matlab implementation for local stress-constrained topology optimization using the augmented Lagrangian method[J]. Structural and Multidisciplinary Optimization, 2021, 63(4): 2065-2097.
[5] 何亮. 基于高阶有限元的变密度拓扑优化算法设计与实现[D]. 湘潭: 湘潭大学, 2026.
