---
title: "Hu–Zhang 拓扑优化应力约束验收约定"
tags:
  - huzhang
  - stress-constraint
  - numerical-validation
status: draft
date_added: 2026-09-08
date_update: 2026-09-15
---

# Hu–Zhang 拓扑优化应力约束验收约定

本页保存 LFEM 与 Hu–Zhang 应力约束算例的准则比较、代码核对与待验证的验收选择。数学定义见 [[../../concepts/density-topopt/stress-constrained-topopt]]；论文入口为 [[high-order-huzhang-topopt-draft-zh]]。本页不替代代码仓库中的实现与运行记录。

## 1. 验证目标与方案比较

> **2026-09-14 方案变更，待验证**：后续 LFEM 与 Hu–Zhang 正式对照统一采用表观应力松弛约束，完整模型、LFEM 设计导数及 KKT 残差定义见 [[../../papers/huzhang-topopt/stress-constrained-topopt-models-and-algorithms#7. 统一表观应力约束与一阶最优性检查（待验证）]]。以下 §1–4 保留旧方案来源与运行记录，不作为统一约束方案已通过的证据。新方案需先完成梯度和诊断验证，再进行正式优化；KKT 容差尚未确定，论文结果暂不更新。

目标是验证所用离散松弛约束的可行性，而不只是使优化器返回“收敛”。以下三种口径应分开记录：

| 口径 | 设计变化 | 应力检查 | 依据与边界 |
|---|---|---|---|
| PolyStress 发布代码 | 平均绝对变化 | 加权表观应力比 | 已核对发布包；没有独立原始残差停止阈值 |
| 博士论文表述 | 此前核对记录为最大绝对变化 | 应力验收量的完整定义尚需澄清 | 不能把本文相对超限方案直接称为博士论文标准 |
| 本项目拟采用方案（2026-09-11 改定） | 外层步平均绝对变化 | 表观应力比超出许用水平（LFEM 加权比，Hu–Zhang 为 $g_e$） | 项目适配；容差的数值适用性待验证 |

## 2. PolyStress 代码核对

2026-09-08 核对 PolyStress 作者发布包：`PolyScript.m` 第 44–45 行设置 `Tol=0.002`、`TolS=0.003`；`PolyStress.m` 第 35 行用 `E.*fem.VM_Stress0/fem.SLim` 计算应力指标，第 123 行计算平均设计变化。其正常停止要求：

$$
\frac{1}{N_a}\sum_{j\in\mathcal A}|z_j^{(n)}-z_j^{(n-1)}|
\leq0.002(z_{\max}-z_{\min}),\qquad
\max_e\frac{m_{E,e}\sigma_{\mathrm{solid},e}^{\mathrm{vM}}}{\bar\sigma}
\leq1.003.
$$

其中 $\mathcal A$ 为参与更新的变量集合，$N_a$ 为其大小。代码并未额外要求原始约束最大值不超过 0.003。不能将上述条件解释为未加权实体应力比检查，也不能把 0.003 自动移作原始约束残差容差。


## 3. 项目拟采用的严格验收约定

**以下为项目约定，数值适用性待验证，不是两种方法共同的文献标准，也不表示现有结果已通过。** 设计侧沿用 PolyStress 代码的平均绝对变化，应力侧对表观应力比设绝对容差：

$$
\Delta_z^{(k)}=\frac{1}{N_e}\sum_{e=1}^{N_e}|z_e^{(k+1,0)}-z_e^{(k,0)}|<0.002,
\qquad r_{\max}=\max_e r_e\leq0.003,
$$

$$
r_e^{\mathrm{LFEM}}=\frac{m_{E,e}\sigma_{\mathrm{solid},e}^{\mathrm{vM}}}{\bar\sigma}-1,
\qquad
r_e^{\mathrm{HZ}}=\frac{\sigma_{\mathrm{app},e}^{\mathrm{vM}}}{\bar\sigma}-\eta_e=g_e^{\mathrm{HZ}}.
$$

设计变量按 $[0,1]$ 归一化，$\Delta_z$ 按 ALM 外层步首末设计计（PolyStress 每次迭代只含一次 MMA 更新，其按相邻迭代计的平均变化与此同口径，本项目一个外层步含至多 5 次 MMA 更新，同一数值下略严）。两项同时满足并配合投影延拓完成、连续 3 个外层步持续两条（定义见 `../../papers/huzhang-topopt/stress-constrained-topopt-models-and-algorithms.md` §6）才按此约定正常停止。容差 0.003 表示表观应力比超出许用水平不超过 0.003，对低密度单元不是相对其阈值的 0.3%，因此须一并报告取到 $r_{\max}$ 的单元的密度；Hu–Zhang 的这一用法属于项目适配，不能称为 PolyStress 代码或博士论文已明确验证的标准，也不能据此宣称两种松弛模型物理等价。

修订记录：2026-09-09 曾把设计侧改为最大变化量 $\max_e|\Delta z_e|<0.002$、Hu–Zhang 应力侧改为按 $\eta_e$ 归一的 $\sigma_{\mathrm{app}}/(\eta_e\bar\sigma)-1$；2026-09-11 两项均改回或改定为上式，原因见 §4 与姊妹页 §6.2。

检查使用更新后物理密度重新求解得到的应力。投影参数更新后重新评价，不能沿用旧状态。达到迭代上限但未同时满足条件，应记录“达到上限，未满足停止条件”。局部检查覆盖模型规定的全部应力评价位置；单元中心或积分点检查并不自动证明单元内部任意位置均满足。

最终独立复算并报告 $g_{\max}=\max_e g_e$、$r_{\max}$、最大表观应力比及超限位置。原始残差和表观应力比不额外参与这套停止判断。严格数学可行要求 $g_{\max}\leq0$；通过正容差验收只能表述为“在所设容差内满足离散松弛约束”。设计稳定与约束验收也不构成最优性或离散精度证明。现阶段不另指定未经论证的原始残差正容差，不以现有结果能否通过倒推容差。


## 4. 现有证据与后续验证

2026-09-08 对 `soptx:experiments/paper_topopt_huzhang/outputs/cantilever-middle-2d-stress` 中 12 份保存密度完成当前代码冻结复算：全部存在正的原始局部约束残差，均未通过相对超限 0.003 的检查；部分历史“收敛”记录对应的最终密度重新求解后，表观应力比也超过 1.003。此为当前分析代码对历史密度的复算结论，不是历史版本优化过程的完整重现，也不能推出增加迭代永远无效。

2026-09-09 与 09-10 按当时的最大变化量判据各跑两次 $k=2$（LFEM、Hu–Zhang 各一次无条件放大 $\mu$、一次有条件放大），四次均在 150 个外层步（750 次全局迭代）达上限未收敛：设计变量最大变化被约 0.3% 的灰度带单元的两值翻转钉在移动极限 0.15 上；Hu–Zhang 路径的 $\max_e r_e$（按 $\eta_e$ 归一）停在 1.3 到 2.7，同期 $g_{\max}$ 为 0.0034 到 0.015，最大值落在 $\eta_e\leq0.012$ 的低密度单元；LFEM 路径 $g_{\max}$ 为 0.0067 到 0.04，加权比 $r_{\max}$ 在 0.0002 到 0.017 间往复。物理密度在一个外层步内的平均变化为 $4\times10^{-4}$ 到 $3\times10^{-3}$（2026-09-11 由逐步密度场重算），设计变量的平均变化未逐步保存。据此 2026-09-11 改定 §3 的两项，并把外层上限提到 200、启用 C0 之后的移动极限衰减，待重跑验证；按改定判据，四次旧运行的末态仍不满足 $r_{\max}\leq0.003$。

后续应定位超限评价点及其密度、阈值、应力和状态残差，核查低密度区域的数值误差与约束处理，再检验参数和容差的适用性。不能仅为让既有结果通过而放宽标准。正式实施与实验数据由 SOPTX 维护；待约定与数值验证一致后，再同步论文中的计算条件。

## 5. 松弛参数与当前实现的验收量

通用定义见 [[../../concepts/density-topopt/stress-constrained-topopt#3. 奇异最优解与松弛处理]]；适配器对应关系见 [[../../papers/huzhang-topopt/stress-constrained-topopt-models-and-algorithms#7.1 SOPTX 实现对应关系]]。以下为 2026-09-14 代码核对，不替代前文历史记录。

| 模型 | AL 使用的约束值 | 当前验收量 |
|---|---|---|
| $\varepsilon$ 松弛 | $g=a-[m+\varepsilon(1-m)]$ | $g$ |
| 多项式消失约束 | $g=m[(q-1)^3+(q-1)]$ | 历史加权指标 $mq-1$ |

$q=\sigma_{\mathrm{vm}}^{\mathrm{solid}}/\bar\sigma$，$a=\sigma_{\mathrm{vm}}^{\mathrm{app}}/\bar\sigma$。多项式路径的验收量不是其原始约束残差；通过历史指标不能据此宣布多项式约束可行，诊断时应同时报告 $g_{\max}$。

$\varepsilon=10^{-4}$ 是模型参数，$\epsilon_g=0.003$ 是统一表观应力方案的绝对约束容差。局部阈值 $\eta=m+\varepsilon(1-m)$ 很小时，相对阈值的容许超限为 $\epsilon_g/\eta$，不能解释为处处满足 $0.3\%$ 的相对精度。

验收应分别给出原始约束最大值、模型验收量、超限点的位置与密度，并区分梯度验证、状态求解精度和完整优化可行性。本次新增内容仅核对公式与接口，未运行数值验证。

## 参考依据

- [PolyStress 作者发布包](https://paulinogroup.princeton.edu/journal_papers/2021/PolyStress_Release_version_SMO.zip)：2026-09-08 读取核对，支持第 2 节的代码事实。
- [[../../literature/topopt/stress-constrained/translations/GiraldoLondono2021-polystress-stress-constrained-zh]]：PolyStress 文献入口；具体停止实现以上述发布包为据。
- 博士论文《基于高阶有限元的变密度拓扑优化算法设计与实现》第五章式（5.14）：Hu–Zhang 松弛模型的来源；不作为相对容差 0.003 的直接依据。
- 第 3 节为项目拟采用的数值验收约定；第 4 节为本次讨论已有冻结复算的日期快照，本次文档整理未重跑计算。
