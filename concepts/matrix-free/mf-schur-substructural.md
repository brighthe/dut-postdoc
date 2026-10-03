---
title: "子结构 Schur 补 Matrix-Free 算子"
type: concept
aliases:
  - mf-schur-substructural
  - 子结构 Schur 补算子
  - Schur complement matrix-free operator for substructuring
tags:
  - matrix-free
  - static-condensation
  - schur-complement
  - substructure
  - operator
status: draft
date_added: 2026-10-03
date_update: 2026-10-03
---

# 子结构 Schur 补 Matrix-Free 算子

> 按 [[../exact-substructural|精确子结构分析]] 的流程，给出两条接口路径结合 Matrix-Free 的做法：完整接口（`full_trace`）不形成 $\mathbf K_s^j$，作用时现算；角点接口（`linear_corner`）保存 $n_c^j\times n_c^j$ 的局部 $\mathbf K_{s,\mathrm{corner}}^j$。两者都不组装全局接口矩阵，精确算术下与显式路径恒等。

## 1. 共同环节

1. **局部刚度**（[[../exact-substructural#1.2 局部问题与适用假设|§1.2]]）：原式为分块刚度
   $$
   \mathbf K^j=\begin{bmatrix}\mathbf K_{bb}^j&\mathbf K_{bi}^j\\ \mathbf K_{ib}^j&\mathbf K_{ii}^j\end{bmatrix}.
   $$
   只组装 $\mathbf K_{ii}^j$ 并做 Cholesky 分解；$\mathbf K_{bb}^j$、$\mathbf K_{ib}^j$ 不保存，按 [[assembly-levels#2.3.2 共享参考 EA：只保存 $\mathbf K_e^0$ 与 $s_e$|共享参考 EA]] 由单元刚度现算：
   $$
   \mathbf K_e=s_e\mathbf K_e^0,
   \qquad
   \mathbf K^j\mathbf v=\sum_{e\subset\Omega^j}(\mathbf G_e^j)^{\mathsf T}\,s_e\mathbf K_e^0\,\mathbf G_e^j\mathbf v .
   $$
   其中 $\mathbf G_e^j$ 从子结构局部向量中提取单元 $e$ 的自由度，$s_e=E(\overline\rho_e)/E_0$。子结构材料均匀（$s_e\equiv s_j$）时 $\mathbf K^j=s_j\mathbf K_{\mathrm{ref}}$，$\mathbf T^j$ 与 $s_j$ 无关、缩聚刚度按 $s_j$ 缩放，可共用一份分解与缩聚结果。
2. **位移恢复**（[[../exact-substructural#3.3 子结构位移恢复|§3.3]]，式 (2.1)）：复用 $\mathbf K_{ii}^j$ 的同一分解：
   $$
   \mathbf u_i^j=\mathbf w_i^j+\mathbf T_{\mathrm{full}}^j\mathbf u_b^j,
   \qquad
   \mathbf T_{\mathrm{full}}^j=-(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j .
   $$
   完整接口取 $\mathbf u_b^j=\mathbf A_b^j\mathbf U_\Gamma$；角点接口取 $\mathbf u_c^j=\mathbf A_c^j\mathbf U_C$、$\mathbf u_b^j=\mathbf L^j\mathbf u_c^j$，此时 $\mathbf T_{\mathrm{full}}^j\mathbf u_b^j=\mathbf T_{\mathrm{corner}}^j\mathbf u_c^j$，$\mathbf T_{\mathrm{corner}}^j$（$n_i^j\times n_c^j$）可在 §3 第 1 条中保存，或重新求解。

载荷（完整接口用式 (2.3)：$\widetilde{\mathbf f}_b^j=\mathbf f_b^j-\mathbf K_{bi}^j\mathbf w_i^j$，$\mathbf w_i^j=(\mathbf K_{ii}^j)^{-1}\mathbf f_i^j$；角点接口再用式 (2.15)：$\mathbf f_c^j=(\mathbf L^j)^{\mathsf T}\widetilde{\mathbf f}_b^j$）、支承反力或乘子与灵敏度不需改动。

## 2. 完整接口路径

1. **缩聚刚度**（[[../exact-substructural#2.1 局部静力缩聚及其变分形式|§2.1]] 式 (2.2)）：原式为
   $$
   \mathbf K_s^j=\mathbf K_{bb}^j-\mathbf K_{bi}^j(\mathbf K_{ii}^j)^{-1}\mathbf K_{ib}^j .
   $$
   不形成 $\mathbf K_s^j$，作用时分两步现算：
   $$
   \mathbf K_{ii}^j\mathbf v_i=-\mathbf K_{ib}^j\mathbf x_b,
   \qquad
   \mathbf K_s^j\mathbf x_b=\mathbf K_{bb}^j\mathbf x_b+\mathbf K_{bi}^j\mathbf v_i .
   $$
2. **组装与求解**（[[../exact-substructural#3.1 完整接口组装与求解|§3.1]] 式 (3.3)、(3.5)）：原式为
   $$
   \mathbf K_\Gamma=\sum_{j}(\mathbf A_b^j)^{\mathsf T}\mathbf K_s^j\mathbf A_b^j,
   \qquad
   (\mathbf K_\Gamma)_{FF}(\mathbf U_\Gamma)_F=(\mathbf F_\Gamma)_F-(\mathbf K_\Gamma)_{FD}\mathbf d_D .
   $$
   不组装 $\mathbf K_\Gamma$，逐子结构作用后累加，再对自由子块用 CG 求解：
   $$
   \mathbf K_\Gamma\mathbf x=\sum_{j}(\mathbf A_b^j)^{\mathsf T}\Big(\mathbf K_s^j\big(\mathbf A_b^j\mathbf x\big)\Big).
   $$

## 3. 角点接口路径

1. **缩聚刚度**（[[../exact-substructural#2.2.2 角点接口空间|§2.2.2]] 式 (2.13)、(2.14)）：原式为
   $$
   \mathbf T_{\mathrm{corner}}^j=\mathbf T_{\mathrm{full}}^j\mathbf L^j,
   \qquad
   \mathbf K_{s,\mathrm{corner}}^j=(\mathbf L^j)^{\mathsf T}\mathbf K_{s,\mathrm{full}}^j\mathbf L^j .
   $$
   不形成 $\mathbf K_{s,\mathrm{full}}^j$，只对 $n_c^j$ 个右端做内部求解，形成并保存 $\mathbf K_{s,\mathrm{corner}}^j$：
   $$
   \mathbf K_{ii}^j\mathbf T_{\mathrm{corner}}^j=-\mathbf K_{ib}^j\mathbf L^j,
   \qquad
   \mathbf K_{s,\mathrm{corner}}^j=(\mathbf L^j)^{\mathsf T}\big(\mathbf K_{bb}^j\mathbf L^j+\mathbf K_{bi}^j\mathbf T_{\mathrm{corner}}^j\big).
   $$
2. **组装与求解**（[[../exact-substructural#3.2 角点接口组装与求解|§3.2]] 式 (3.8)、(3.11)）：原式为
   $$
   \mathbf K_C=\sum_{j}(\mathbf A_c^j)^{\mathsf T}\mathbf K_{s,\mathrm{corner}}^j\mathbf A_c^j,
   \qquad
   \begin{pmatrix}\mathbf K_C&\mathbf C_D^{\mathsf T}\\\mathbf C_D&\mathbf 0\end{pmatrix}
   \begin{pmatrix}\mathbf U_C\\\boldsymbol\lambda_D\end{pmatrix}
   =\begin{pmatrix}\mathbf F_C\\\mathbf d_D\end{pmatrix}.
   $$
   不组装 $\mathbf K_C$，逐子结构作用后累加：
   $$
   \mathbf K_C\mathbf x=\sum_{j}(\mathbf A_c^j)^{\mathsf T}\Big(\mathbf K_{s,\mathrm{corner}}^j\big(\mathbf A_c^j\mathbf x\big)\Big).
   $$
   鞍点系统不能直接用 CG，支承按以下一种方式消去：$\mathbf C_D$ 去除冗余行后恰为角点自由度的布尔选取时，取自由子块 $\mathbf P_F\mathbf K_C\mathbf P_F^{\mathsf T}$；一般情形取 $\operatorname{null}(\mathbf C_D)$ 的基 $\mathbf Z$ 与特解 $\mathbf C_D\mathbf U_p=\mathbf d_D$，令 $\mathbf U_C=\mathbf U_p+\mathbf Z\mathbf y$，求解
   $$
   \mathbf Z^{\mathsf T}\mathbf K_C\mathbf Z\,\mathbf y=\mathbf Z^{\mathsf T}\big(\mathbf F_C-\mathbf K_C\mathbf U_p\big).
   $$
   在精确子结构分析 §3.2 的唯一解条件下（$\mathbf K_C$ 在 $\ker(\mathbf C_D)$ 上正定），两种方式的系统算子均对称正定，用 CG 求解。
