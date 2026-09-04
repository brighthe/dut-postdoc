---
title: "第一次正式工作汇报：PIML–GPU–Matrix-Free 小型 Demo 与对照结果"
aliases:
  - "discussions/guo-xu/2026-07-piml-matrix-free-gpu"
  - "2026-07-piml-matrix-free-gpu"
  - "discussions/guo-xu/2026-07-matrix-free-progress-piml-gpu-tasks"
  - "2026-07-matrix-free-progress-piml-gpu-tasks"
  - "entities/guo-xu/first-formal-work-report"
advisor: "郭旭"
report_period: "2026-07—2026-08"
meeting_date: "待确定"
meeting_mode: "当面"
status: "preparing"
date_start: 2026-07-20
date_update: 2026-08-28
tags:
  - 工作汇报
  - PIML
  - Matrix-Free
  - GPU
  - 拓扑优化
topics:
  - "PIML–GPU–Matrix-Free 小型 Demo"
  - "改进 PIML 与传统路线对照"
  - "后续研究价值判断"
related:
  - "./guo-xu"
  - "../../concepts/piml/_index"
  - "../../concepts/matrix-free/_index"
  - "../../concepts/gpu-hpc/_index"
  - "../../research/piml-matrix-free-gpu/matrix-free-research-guide"
  - "../../research/piml-matrix-free-gpu/piml-research-guide"
  - "../../research/piml-matrix-free-gpu/gpu-hpc-research-guide"
  - "../../research/piml-matrix-free-gpu/_index"
  - "../../research/piml-matrix-free-gpu/project-plan"
---

# 第一次正式工作汇报：PIML–GPU–Matrix-Free 小型 Demo 与对照结果

> **核心结论**：已初步跑通 PIML + GPU + Matrix-Free 小型 Demo。形函数—变分构造路线比直接预测缩聚刚度的基线更准，GPU 批量计算和 Matrix-Free 求解接口均已通过验证。

## 1. Demo 设计

基线路线直接预测缩聚刚度 $\widehat{\mathbf K}_s$，再显式组装全局接口矩阵。改进路线预测多尺度形函数 $\widehat{\mathbf N}$，通过变分能量构造 $\widehat{\mathbf K}_s$，并直接用于 Matrix-Free 全局作用：

$$
\widehat{\mathbf A}\mathbf x
=
\sum_j
\mathbf G_j^{\mathsf T}
\widehat{\mathbf K}_{s,j}
\mathbf G_j\mathbf x .
$$

计算链为：

```text
局部材料密度 → PIML 形函数 → 变分局部算子
             → GPU 批量计算 → Matrix-Free Krylov 求解
```

## 2. 对照结果

精度对照采用相同训练预算、随机种子和 24 子结构 MBB 梁算例。

| 指标 | 直接预测 $\mathbf K_s$ | $\widehat{\mathbf N}$ + 变分构造 | 改善倍数 |
|---|---:|---:|---:|
| 留出集局部算子平均误差 | $4.20\%$ | $0.435\%$ | $9.7$ 倍 |
| 在役局部算子平均误差 | $2.90\%$ | $0.092\%$ | $31.5$ 倍 |
| 接口位移相对误差 | $2.05\%$ | $0.155\%$ | $13.2$ 倍 |
| 全场位移相对误差 | $2.01\%$ | $0.153\%$ | $13.1$ 倍 |
| 柔顺度相对误差 | $3.64\%$ | $0.197\%$ | $18.5$ 倍 |

形函数平均误差为 $8.97\%$，经变分构造后局部刚度平均误差降至 $0.435\%$。受控扰动的 log-log 斜率为 $2.003$，与二阶误差关系一致。该构造同时保持刚体零空间和半正定结构。

## 3. GPU 与 Matrix-Free 验证

### GPU 批量计算

在 NVIDIA GeForce RTX 5080 上测试三维 PIML 批量预测与变分刚度构造。并发规模为 24–384 个子结构时，GPU 单步耗时为 $0.237$–$4.325\text{ ms}$，相对同一 PyTorch CPU 计算链加速 $20.3$–$29.2$ 倍。

### Matrix-Free 求解

24 子结构、574 个接口自由度算例的结果为：

- PyTorch Matrix-Free MatVec 与显式路径相对差：$3.40\times10^{-16}$；
- 自由子空间作用相对差：$3.68\times10^{-16}$；
- CG 迭代数：341；
- CG 真相对残差：$8.69\times10^{-11}$。

NumPy 对照中，Matrix-Free CG 与显式矩阵 CG 的解相对差为 $1.34\times10^{-13}$，迭代数相差 1 步。

## 4. 当前结论与边界

- 形函数—变分构造路线在局部算子、位移和柔顺度上均优于本次直接预测刚度基线；
- PIML 局部计算适合 GPU 批处理；
- PIML 局部算子可以直接进入 Matrix-Free Krylov 求解，无需形成全局接口刚度矩阵。

当前仍是模块化小型 Demo。精度与 Matrix-Free 求解采用二维 24 子结构算例，GPU 测试采用三维局部批量计算；两部分尚未纳入同一次端到端计时。预条件、动态真残差复核、自适应回退和完整拓扑优化仍待开展。

## 5. 待讨论议题

1. 第一项工作应重点突出变分结构保持，还是 PIML 与 Matrix-Free/Krylov 的结合？
2. 是否以形函数—变分构造为主线，以直接预测缩聚刚度为对照？
3. 下一步优先接通 GPU 端到端求解，还是先研究局部误差对全局谱性质和 Krylov 收敛的影响？
4. 首批正式算例从二维受控问题、三维构件还是拓扑优化过程切入？

---

*项目状态与证据边界见 [[../../research/piml-matrix-free-gpu/project-plan|核心项目计划]]；代码与原始产物见 `soptx:examples/piml_substructure_elasticity/`。*
