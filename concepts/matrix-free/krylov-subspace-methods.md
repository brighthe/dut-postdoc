---
title: "Krylov 子空间方法"
type: concept
aliases:
  - Krylov Subspace Methods
  - Krylov 迭代法
  - 预条件 Krylov 求解器
tags:
  - numerical-algebra
  - linear-solver
  - matrix-free
  - krylov
  - gpu-hpc
status: draft
date_added: 2026-08-07
date_update: 2026-08-07
---

# Krylov 子空间方法

> **一句话**：通过由初始残差与算子反复作用生成的 Krylov 子空间构建近似解的大型线性方程组迭代求解技术，仅需矩阵-向量乘法作用接口，是 Matrix-Free 算子与 GPU 高性能计算的天然载体。

## 定义

对于大型稀疏线性方程组 $\mathbf{A}\mathbf{x} = \mathbf{b}$（其中 $\mathbf{A} \in \mathbb{R}^{n \times n}$），设初始解为 $\mathbf{x}_0$，初始残差为 $\mathbf{r}_0 = \mathbf{b} - \mathbf{A}\mathbf{x}_0$。第 $k$ 阶 **Krylov 子空间**（Krylov Subspace）定义为由初始残差及其经算子 $\mathbf{A}$ 反复作用所生成的向量空间：

$$
\mathcal{K}_k(\mathbf{A}, \mathbf{r}_0) = \text{span}\left\{ \mathbf{r}_0, \mathbf{A}\mathbf{r}_0, \mathbf{A}^2\mathbf{r}_0, \dots, \mathbf{A}^{k-1}\mathbf{r}_0 \right\}
$$

Krylov 子空间方法在寻找近似解 $\mathbf{x}_k \in \mathbf{x}_0 + \mathcal{K}_k(\mathbf{A}, \mathbf{r}_0)$ 时，通过在子空间中实施投影（Galerkin 投影或极小化残差），将 $n$ 维大型求解问题转化为 $k$ 维子空间上的低阶代数问题（通常 $k \ll n$）。

## 关键要点

- **无矩阵依赖性（Matrix-Free Affinity）**：算法执行过程中不依赖显式形成或存储全局矩阵 $\mathbf{A}$ 的元素，仅需提供算子作用接口 $\mathbf{y} = \mathbf{A}\mathbf{x}$，彻底避免了传统直接法（LU / Cholesky 分解）带来巨额填充（Fill-in）与内存开销。
- **主流算法族谱分类**：
  - **对称正定（SPD）系统**：**共轭梯度法（Conjugate Gradient, CG）** 及其预条件版本 **PCG**。利用 $A$-正交性，递推关系短（仅保留前一步向量），显存与计算开销小。
  - **对称不定系统**：**MINRES**（Minimum Residual）与 **SYMMLQ**，基于 Lanczos 过程。
  - **非对称 / 一般系统**：**GMRES**（Generalized Minimal Residual）、**BiCGSTAB**、**TFQMR**。GMRES 基于 Arnoldi 过程，具备单调残差极小化性质，但长递推需定期重启（Restart）。
- **预条件机制（Preconditioning）**：
  - 条件数 $\kappa(\mathbf{A})$ 过大时收敛缓慢。通过寻找易于求解的近似逆算子 $\mathbf{M}^{-1}$，构造等价方程组 $\mathbf{M}^{-1}\mathbf{A}\mathbf{x} = \mathbf{M}^{-1}\mathbf{b}$。
  - 在 Matrix-Free 框架下，预条件器可以是多网格（Multigrid）、对角缩放、不完全分解或基于代理模型（PIML / 缩聚）的局部/粗尺度算子。
- **GPU 异构计算特征**：
  - **计算密集的算子作用**：$\mathbf{y} = \mathbf{A}\mathbf{x}$ 可在 GPU 上通过按需计算（Compute-on-the-fly）或批量局部作用实现。
  - **访存/通信密集的向量运算**：点积（Dot Product）产生全局归约（Global Reduction）同步开销；AXPY 向量更新属于高访存低算力操作。

## 与相关概念的关系

- **上位概念**：大型稀疏线性方程组迭代求解器 (Iterative Linear Solvers)
- **下位概念**：PCG (Preconditioned Conjugate Gradient)、GMRES、MINRES
- **直接载体**：[[_index|Matrix-Free 主题]]、[[assembly-levels|Matrix-Free 五级装配层次]]、[[../gpu-hpc/distributed-operator-and-shared-dofs]] (分布式算子与全局加权内积)
- **加速硬件**：[[../gpu-hpc/_index|GPU/HPC]] (GPU 异构加速与内存驻留)

## 在我研究中的位置

在申请人的拓扑优化与计算力学研究中，Krylov 子空间方法是连接局部算子表示与全局结构分析的**核心数值求解引擎**：

1. **三维大规模拓扑优化**：直接求解法内存爆表，必须依靠预条件 Krylov 求解器（如 PCG）在 Matrix-Free 模式下完成千万自由度系统的反复静力分析。
2. **PIML 与 Krylov 收敛性研究**：PIML 预测的局部力学表示带来全局算子扰动 $\widehat{\mathbf{A}}$。研究该扰动如何改变谱分布、条件数及代理预条件器质量，进而控制 Krylov 求解器的真残差下降与收敛代数，是课题拟解决的关键科学问题。
3. **GPU 协同执行与数据流**：在 GPU 上实现算子按需作用、Krylov 向量运算、全局归约与预条件更新的高效流水线，避免 CPU–GPU 频繁同步与数据搬移。

## 来源与证据

本页的定义、算法分类及在课题中的应用定位精准参考了以下经典文献与知识库内部文件：

- **定义与投影机制**（§定义）：
  - Saad, Y. (2003). *Iterative Methods for Sparse Linear Systems* (2nd ed.). SIAM. — §6.1 "Krylov Subspace Methods" (定义了 Krylov 子空间与子空间投影过程)。
- **主流算法族谱与递推特征**（§关键要点）：
  - Saad, Y. (2003). *Iterative Methods for Sparse Linear Systems* (2nd ed.). SIAM. — §6.5 (CG/PCG 算法及 short-recurrence 性质), §7.1 (GMRES 算法与 Arnoldi 过程重启机制)。
- **Matrix-Free 算子并行作用**（§无矩阵依赖性）：
  - Kronbichler, M., & Kormann, K. (2012). A generic interface for parallel cell-based finite element operator application. *Computers & Fluids*, 63, 135–147. (对应申请书文献 [1]，论述了基于单元的算子按需作用与预条件 Krylov 结合路径)。
- **在课题研究中的定位与问题提出**（§在我研究中的位置）：
  - [[../../research/funding/active/china-postdoc-foundation-general-grant/80th-2026-application-draft|第 80 批面上资助申请书正文]] — §2 研究内容、§3 技术路线（提出局部 PIML 近似算子对 Krylov 真残差与代理预条件收敛影响的科学问题）。
  - [[../../research/piml-matrix-free-gpu/project-plan|博士后核心研究项目计划]] — WP1 Matrix-Free/GPU 闭环验证。

## 相关页面

- [[_index]] — Matrix-Free 主题入口
- [[assembly-levels]] — Matrix-Free 五级装配层次
- [[../gpu-hpc/distributed-operator-and-shared-dofs]] — 分布式有限元算子与加权 Krylov 内积
- [[../gpu-hpc/_index]] — 异构高性能计算与算子并行
- [[../linear-elasticity]] — 位移型线弹性有限元离散
