---
title: "子结构 PIML Matrix-Free 算子"
type: concept
aliases:
  - mf-piml-substructural
  - 子结构 PIML 算子
  - PIML matrix-free operator for substructuring
tags:
  - matrix-free
  - piml
  - substructure
  - operator
status: draft
date_added: 2026-10-03
date_update: 2026-10-03
---

# 子结构 PIML Matrix-Free 算子

> 按 [[../piml/piml-substructural|基于 PIML 的子结构分析]] 的流程，给出两条接口路径结合 Matrix-Free 的做法。PIML 以网络预测的 $\widehat{\mathbf T}^j$（路线 A）或 $\widehat{\mathbf K}_s^j$（路线 B）替代内部求解，不再分解 $\mathbf K_{ii}^j$；Matrix-Free 作用于能量投影中的细网格作用与全局接口矩阵的不组装。精确内部求解时的做法见 [[mf-schur-substructural|子结构 Schur 补 Matrix-Free 算子]]。

## 1. 共同环节

1. **局部刚度**（[[../piml/piml-substructural#1.1 局部问题与适用假设|PIML §1.1]] 式 (1.1)）：原式为
   $$
   \mathbf K^j(\boldsymbol\eta^j)=\begin{bmatrix}\mathbf K_{bb}^j&\mathbf K_{bi}^j\\ \mathbf K_{ib}^j&\mathbf K_{ii}^j\end{bmatrix}.
   $$
   不组装 $\mathbf K^j$，也不分解 $\mathbf K_{ii}^j$。路线 A 能量投影所需的 $\mathbf K^j\mathbf v$ 按 [[assembly-levels#2.3.2 共享参考 EA：只保存 $\mathbf K_e^0$ 与 $s_e$|共享参考 EA]] 现算：
   $$
   \mathbf K_e=s_e\mathbf K_e^0,
   \qquad
   \mathbf K^j\mathbf v=\sum_{e\subset\Omega^j}(\mathbf G_e^j)^{\mathsf T}\,s_e\mathbf K_e^0\,\mathbf G_e^j\mathbf v ,
   $$
   其中 $\mathbf G_e^j$ 从子结构局部向量中提取单元 $e$ 的自由度，$s_e=E(\overline\rho_e)/E_0$。路线 B 在求解阶段不需要 $\mathbf K^j$。子结构材料均匀（$s_e\equiv s_j$）时可直接取精确参考值 $\mathbf T^j=\mathbf T_{\mathrm{ref}}$、$\mathbf K_s^j=s_j\mathbf K_{s,\mathrm{ref}}$，代替网络预测。
2. **位移恢复**（[[../piml/piml-substructural#5.3 子结构位移恢复|PIML §5.3]] 式 (5.10)、(5.11)）：路线 A 用构造刚度的同一预测形函数矩阵：
   $$
   \widehat{\mathbf u}^j=\widehat{\mathbf N}^j\widehat{\mathbf q}^j,
   \qquad
   \widehat{\mathbf N}^j=\begin{bmatrix}\boldsymbol\Psi^j\\ \widehat{\mathbf T}^j\end{bmatrix},
   $$
   完整接口取 $\boldsymbol\Psi^j=\mathbf I$、$\widehat{\mathbf q}^j=\mathbf A_b^j\widehat{\mathbf U}_\Gamma$，角点接口取 $\boldsymbol\Psi^j=\mathbf L^j$、$\widehat{\mathbf q}^j=\mathbf A_c^j\widehat{\mathbf U}_C$。$\widehat{\mathbf T}^j$ 可保存，或按需重新推理。路线 B 另配形函数模型时同上；改用局部精确求解时按式 (5.11)，需组装并分解 $\mathbf K_{ii}^j$。

载荷（式 (5.2)、(5.6)，内部无载荷）、支承反力或乘子不需改动。

## 2. 完整接口路径

1. **缩聚刚度**（[[../piml/piml-substructural#4.1 完整接口空间|PIML §4.1]] 式 (4.1)–(4.4)）：路线 A 原式为
   $$
   \widehat{\mathbf N}_{\mathrm{full}}^j=\begin{bmatrix}\mathbf I\\ \widehat{\mathbf T}_{\mathrm{full}}^j\end{bmatrix},
   \qquad
   \widehat{\mathbf K}_{s,\mathrm{full}}^j=(\widehat{\mathbf N}_{\mathrm{full}}^j)^{\mathsf T}\mathbf K^j\widehat{\mathbf N}_{\mathrm{full}}^j .
   $$
   不形成 $\widehat{\mathbf K}_{s,\mathrm{full}}^j$，作用时现算：
   $$
   \mathbf y=\mathbf K^j\begin{bmatrix}\mathbf x_b\\ \widehat{\mathbf T}_{\mathrm{full}}^j\mathbf x_b\end{bmatrix},
   \qquad
   \widehat{\mathbf K}_{s,\mathrm{full}}^j\mathbf x_b=\mathbf y_b+(\widehat{\mathbf T}_{\mathrm{full}}^j)^{\mathsf T}\mathbf y_i ,
   $$
   其中 $\mathbf y_b$、$\mathbf y_i$ 为 $\mathbf y$ 的边界与内部分量。$\widehat{\mathbf T}_{\mathrm{full}}^j$ 不满足内部平衡，$\mathbf y_i\ne\mathbf 0$，第二项不能省去；作用需常驻 $\widehat{\mathbf T}_{\mathrm{full}}^j$（$n_i^j\times n_b^j$）或每次重新推理。路线 B 直接预测稠密 $\widehat{\mathbf K}_{s,\mathrm{full}}^j=\mathcal G_{\mathrm{full}}(\boldsymbol\eta^j;\boldsymbol\theta)$ 并保存。
2. **组装与求解**（[[../piml/piml-substructural#5.1 完整接口组装与求解|PIML §5.1]] 式 (5.2)、(5.3)）：原式为
   $$
   \widehat{\mathbf K}_\Gamma=\sum_{j}(\mathbf A_b^j)^{\mathsf T}\widehat{\mathbf K}_{s,\mathrm{full}}^j\mathbf A_b^j,
   \qquad
   (\widehat{\mathbf K}_\Gamma)_{FF}(\widehat{\mathbf U}_\Gamma)_F=(\mathbf F_\Gamma)_F-(\widehat{\mathbf K}_\Gamma)_{FD}\mathbf d_D .
   $$
   不组装 $\widehat{\mathbf K}_\Gamma$，逐子结构作用后累加，再对自由子块用 CG 求解：
   $$
   \widehat{\mathbf K}_\Gamma\mathbf x=\sum_{j}(\mathbf A_b^j)^{\mathsf T}\Big(\widehat{\mathbf K}_{s,\mathrm{full}}^j\big(\mathbf A_b^j\mathbf x\big)\Big).
   $$
   CG 要求预测局部刚度满足 PIML §3.1 的对称、刚体零空间与变形子空间正定性；路线 A 的能量投影自动保证对称半正定。

## 3. 角点接口路径

1. **缩聚刚度**（[[../piml/piml-substructural#4.2 角点接口空间|PIML §4.2]] 式 (4.5)–(4.9)）：路线 A 原式为
   $$
   \widehat{\mathbf N}_{\mathrm{corner}}^j=\begin{bmatrix}\mathbf L^j\\ \widehat{\mathbf T}_{\mathrm{corner}}^j\end{bmatrix},
   \qquad
   \widehat{\mathbf K}_{s,\mathrm{corner}}^j=(\widehat{\mathbf N}_{\mathrm{corner}}^j)^{\mathsf T}\mathbf K^j\widehat{\mathbf N}_{\mathrm{corner}}^j .
   $$
   形成并保存 $\widehat{\mathbf K}_{s,\mathrm{corner}}^j$：对 $\widehat{\mathbf N}_{\mathrm{corner}}^j$ 的 $n_c^j$ 列各做一次局部作用，
   $$
   \mathbf Y^j=\mathbf K^j\widehat{\mathbf N}_{\mathrm{corner}}^j,
   \qquad
   \widehat{\mathbf K}_{s,\mathrm{corner}}^j=(\widehat{\mathbf N}_{\mathrm{corner}}^j)^{\mathsf T}\mathbf Y^j .
   $$
   路线 B 直接预测并保存 $\widehat{\mathbf K}_{s,\mathrm{corner}}^j=\mathcal G_{\mathrm{corner}}(\boldsymbol\eta^j;\boldsymbol\theta)$。
2. **组装与求解**（[[../piml/piml-substructural#5.2 角点接口组装与求解|PIML §5.2]] 式 (5.6)、(5.9)）：原式为
   $$
   \widehat{\mathbf K}_C=\sum_{j}(\mathbf A_c^j)^{\mathsf T}\widehat{\mathbf K}_{s,\mathrm{corner}}^j\mathbf A_c^j,
   \qquad
   \begin{pmatrix}\widehat{\mathbf K}_C&\mathbf C_D^{\mathsf T}\\\mathbf C_D&\mathbf 0\end{pmatrix}
   \begin{pmatrix}\widehat{\mathbf U}_C\\\widehat{\boldsymbol\lambda}_D\end{pmatrix}
   =\begin{pmatrix}\mathbf F_C\\\mathbf d_D\end{pmatrix}.
   $$
   不组装 $\widehat{\mathbf K}_C$，逐子结构作用后累加：
   $$
   \widehat{\mathbf K}_C\mathbf x=\sum_{j}(\mathbf A_c^j)^{\mathsf T}\Big(\widehat{\mathbf K}_{s,\mathrm{corner}}^j\big(\mathbf A_c^j\mathbf x\big)\Big).
   $$
   支承的消去（布尔选取取自由子块，或零空间法）同 [[mf-schur-substructural#3. 角点接口路径|子结构 Schur 补算子 §3]]。
