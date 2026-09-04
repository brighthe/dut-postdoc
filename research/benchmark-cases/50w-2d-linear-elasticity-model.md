---
title: "50w-2d 板壳线弹性 BDF 数学模型"
topic: "大规模薄壁板壳与多点约束系统的张量化数学复原与自由度闭合"
aliases:
  - 50w-2d 数学模型
  - 50w-2d BDF
  - 50w-2d 壳模型
tags:
  - benchmark-case
  - benchmark-candidate
  - linear-elasticity
  - shell-structure
  - CQUAD4
  - MITC4
  - RBE2
  - RBE3
  - BDF
  - SOL-101
status: "draft"
date_start: 2026-08-30
date_update: 2026-08-30
source: "DLUTFEM-20260720:testcases/50w-2d.bdf"
source_sha256: "64D2783811E4619147CDB4652FA3F095CCA86F6240567EE21408097578EE5E1D"
source_size_bytes: 13828970
source_last_modified: "2025-12-10 15:52:14"
related:
  - "./_index.md"
  - "./10w-3d-linear-elasticity-model.md"
  - "../../concepts/linear-elasticity.md"
  - "../../concepts/finite-elements/shell-elements.md"
  - "../../concepts/matrix-free/assembly-levels.md"
---

# `50w-2d.bdf` 板壳线弹性模型

## 算例定位

这是一个包含近 10 万四边形壳单元、2 万余个多点约束（MPC）的大规模工业级薄壁结构模型。它适合考察有限元求解器在工业板壳单元技术（Reissner–Mindlin 运动学、MITC4 抗剪切锁定、钻转动自由度稳定、非协调膜元）以及复杂工业约束网络（高密度 RBE2/RBE3/SPC）下的张量化装配、代数消除与大规模线性静力求解性能。

目前该模型是**前向线性静力分析测试模型**，不包含拓扑优化设计域、材料插值方案或局部应力约束，不能直接作为二维连续体拓扑优化论文算例。

**候选用途：** GPU 张量化有限元求解器基准测试、多点约束消元与投影算法性能验证、大规模板壳前向计算基准。

---

## 1. 单元离散与单刚计算接口

本算例全场 97,782 个单元全部采用四节点双线性四边形板壳单元（`CQUAD4`）离散。每个单元包含 4 个角节点，每个节点拥有 3 个平移与 3 个转角共 6 个自由度，单元自由度向量为：

$$
\boldsymbol u^e = [u_1, v_1, w_1, \theta_{x1}, \theta_{y1}, \theta_{z1},\ \dots,\ u_4, v_4, w_4, \theta_{x4}, \theta_{y4}, \theta_{z4}]^{\mathsf T} \in \mathbb R^{24}.
\tag{1}
$$

### 1.1 CQUAD4 专用抗自锁特化配置

相较于通用的板壳有限元理论体系（详见理论母页 [[../../concepts/finite-elements/shell-elements|shell-elements]]），`CQUAD4` 是在“4 节点一阶四边形”拓扑下的极致工程特化版本，其专用算子特化配置如下：

| 特化维度 | 通用板壳理论体系 | `CQUAD4` 专用特化实现（本算例） |
|---|---|---|
| **单元拓扑与自由度** | 任意节点数 $N_v$（$6N_v$ 维刚度） | **严格 4 节点双线性四边形，闭环于 $24 \times 24$ 刚度** |
| **膜抗弯自锁** | EAS / Allman / 非协调元 | **Wilson 4 气泡元（$1-\xi^2, 1-\eta^2$）内部 Schur 补静力消元（$16\to 12$ 维）** |
| **薄板剪切自锁** | MITC 族 / DKT 约束体系 | **Bathe 专属 4 边中点 MITC4 协变剪切采样插值** |
| **钻转动 $\theta_z$ 稳定** | 连续旋度差值能量变分泛函 | **中心单点求积 + 双秩一张量（$\boldsymbol Q_1$ 旋度差 + $\boldsymbol Q_2$ 沙漏正则化）** |
| **空间翘曲修正** | 三角形天然共面，高阶壳曲面参数化 | **专属 $24\times 24$ 非共面刚体模态几何投影矩阵 $\boldsymbol T_w$** |

### 1.2 全局单刚闭环计算接口

每个 `CQUAD4` 单元在全局 Cartesian 坐标系下的单元刚度矩阵 $\boldsymbol K^e \in \mathbb R^{24\times 24}$ 统一通过如下标准接口闭环输出：

$$
\boxed{
\boldsymbol K^e = \boldsymbol T_e \left( \boldsymbol T_w^{\mathsf T} \boldsymbol K_{\mathrm{local}}^e \boldsymbol T_w \right) \boldsymbol T_e^{\mathsf T} \in \mathbb R^{24\times 24}
}
\tag{2}
$$

其中：
1. **局部刚度 $\boldsymbol K_{\mathrm{local}}^e \in \mathbb R^{24\times 24}$**：由 12 维膜子空间刚度 $\widetilde{\boldsymbol K}_{\mathrm{mem}}^e$（Wilson 气泡元凝聚 + $\boldsymbol Q_1/\boldsymbol Q_2$ 钻转动稳定项）与 12 维板子空间刚度 $\boldsymbol K_{\mathrm{plt}}^e$（MITC4 边中点剪切混合插值）通过正交布尔投影矩阵 $\boldsymbol P_{\mathrm{mem}}, \boldsymbol P_{\mathrm{plt}}$ 拼接而成；
2. **空间变换算子**：$\boldsymbol T_w \in \mathbb R^{24\times 24}$ 为非共面翘曲修正矩阵，$\boldsymbol T_e \in \mathbb R^{24\times 24}$ 为全局三维方向余弦正交旋转矩阵；
3. **理论与算子唯一定义**：上述所有抗自锁机理、分块矩阵定义（$\boldsymbol K_{uu}, \boldsymbol K_{u\alpha}, \boldsymbol K_{\alpha\alpha}$）、Drilling 稳定算子（$\boldsymbol Q_1, \boldsymbol Q_2$）、MITC4 高斯求积算子（$\boldsymbol B_b, \boldsymbol D, \boldsymbol B_s, \boldsymbol A_s$）及变换矩阵的严格数学推导，由理论母页 **[[../../concepts/finite-elements/shell-elements|shell-elements]]** 统一权威维护，本算例文档直接调用其闭环接口。

---

### 1.3 `SGFem::Quad4ShellCalculator` 算法实现伪代码

工业求解器（`SGFem`）中 `CQUAD4` 单刚计算器（`Quad4ShellCalculator::ComputeStiffness`）的 7 步核心执行流伪代码如下：

```cpp
// 输入：4 节点局部坐标 coord (4x3), 截面材料刚度 secConstant, 全局旋转矩阵 Tele (24x24), 翘曲参数 zWarp, 偏置 zoff
// 输出：全局 24 维单元刚度矩阵 kg (24x24)
Matrix ComputeStiffness(coord, secConstant, Tele, zWarp, zoff)
{
    Matrix K_mem(12, 12) = 0, K_plt(12, 12) = 0;
    Matrix K_md(12, 4)   = 0, K_dd(4, 4)    = 0; // 气泡耦合与自刚度
    Real_t GV = 0.0;                             // 旋度惩罚体积积分

    // =========================================================================
    // 阶段 1: 2x2 (4点) 高斯数值积分循环 (Gauss Integration Loop)
    // =========================================================================
    for (int iGauss = 0; iGauss < 4; ++iGauss)
    {
        Real_t weight = GaussWeight[iGauss];
        Real_t detJ, detJ_b;
        Real_t t = GetGaussThickness(iGauss);    // 截面厚度

        // --- 1.1 膜子空间 (Membrane): 协调应变 B 与非协调气泡应变 G ---
        Matrix B, G, Cm;
        ComputeMembraneStrainMatrix(iGauss, coord, _OUT B, _OUT detJ);
        ComputeIncompatibleBubbleMatrix(iGauss, detJ, JT0, _OUT G);
        secConstant.GetCm(t, _OUT Cm);           // 膜截面本构 Cm = t * C0

        Real_t dV = detJ * weight;
        K_mem += B.T() * Cm * B * dV;           // 节点本征刚度 K_uu
        K_md  += B.T() * Cm * G * dV;           // 膜弯气泡耦合刚度 K_uα
        K_dd  += G.T() * Cm * G * dV;           // 气泡自刚度 K_αα
        GV    += dV * Cm(2, 2);                 // 累加剪切体积用于 Drilling

        // --- 1.2 板子空间 (Plate): 弯曲曲率 Bb 与 MITC4 边中点剪切 Bs ---
        Matrix Bb, Bs, Cb, Cs;
        secConstant.GetCb(t, _OUT Cb);          // 弯曲本构 Cb = (t^3/12) * C0
        secConstant.GetCs(t, _OUT Cs);          // 剪切本构 Cs = (5/6) * G * t * I2
        ComputeBendingCurvature(iGauss, coord, _OUT Bb, _OUT detJ_b);
        ComputeMITC4ShearStrain(coord, detJ_b, xi, eta, _OUT Bs); // 4边中点采样滤波

        K_plt += Bb.T() * Cb * Bb * (detJ_b * weight);
        K_plt += Bs.T() * Cs * Bs * (detJ_b * weight);
    }

    // =========================================================================
    // 阶段 2: 非协调气泡元 Schur 补静力消元 (Static Condensation)
    // =========================================================================
    K_mem -= K_md * K_dd.Inverse() * K_md.T();   // 16维扩展刚度凝聚回 12x12

    // =========================================================================
    // 阶段 3: Drilling 双秩一张量人工稳定 (Q1 旋度差 + Q2 沙漏正则化)
    // =========================================================================
    Real_t delta2 = 1.0e-4 * 100.0;             // KROT6 缩放系数
    Matrix Q1 = ExtractCurlDifferenceVector(coord);    // Q1 (1x12): 节点转角与中心连续旋度差
    K_mem += Q1.T() * (Q1 * (GV * delta2));

    Real_t lambda = 1.0e-10 * GV * 100.0 / 4.0;
    Matrix Q2 = { 0, 0, 0.25, 0, 0, -0.25, 0, 0, 0.25, 0, 0, -0.25 }; // Q2 (1x12): 沙漏摆动
    K_mem += Q2.T() * (Q2 * lambda);

    // =========================================================================
    // 阶段 4: 局部 24 维布尔正交分块拼装 (Local Assembly)
    // =========================================================================
    Vector indexM = { 0, 1, 5, 6, 7, 11, 12, 13, 17, 18, 19, 23 }; // 膜自由度 [u, v, θz]
    Vector indexP = { 2, 3, 4, 8, 9, 10, 14, 15, 16, 20, 21, 22 }; // 板自由度 [w, θx, θy]

    Matrix K_local(24, 24) = 0;
    K_local.BlockFill(indexM, indexM, K_mem);
    K_local.BlockFill(indexP, indexP, K_plt);

    // =========================================================================
    // 阶段 5: 非共面空间翘曲修正 (Warping Correction Tw)
    // =========================================================================
    if (fabs(zWarp) > 1.0e-6)
    {
        Matrix Tw = BuildWarpingMatrix24(zWarp); // 24x24 刚体投影矩阵
        K_local   = Tw.T() * K_local * Tw;
    }

    // =========================================================================
    // 阶段 6: 中面偏置刚体运动学映射 (Offset Transformation Toff)
    // =========================================================================
    if (fabs(zoff) > 1.0e-6)
    {
        Matrix Toff = BuildOffsetMatrix24(zoff); // 24x24 偏置矩阵 (ZOFFS)
        K_local     = Toff.T() * K_local * Toff;
    }

    // =========================================================================
    // 阶段 7: 全局三维方向余弦正交旋转 (Global Rotation Tele)
    // =========================================================================
    Matrix kg = Tele * K_local * Tele.T();       // 输出最终 24 维全局单刚
    return kg;
}
```

---

## 2. 算例模型参数与截面分区

### 2.1 规模概览与截面厚度分布

| 项目 | 数据 |
|---|---|
| 分析类型 | `SOL 101` 线性静力分析 |
| 节点网格 | 98,910 个 `GRID`（原始未约束自由度 $N_0 = 593,460$） |
| 壳单元 | 97,782 个四节点 `CQUAD4` |
| 材料分区 | 1 个 `MAT1` ($E=2\times 10^5, \nu=0.3$)，3 种截面厚度 PSHELL |
| 面载荷 | 32,594 个 `PLOAD4` 面（作用于 PID 4 单元，压强 $p=-5\times 10^{-6}$） |
| 多点约束 (MPC) | 10,543 个 `RBE2` + 10,948 个 `RBE3`（共从属 $128,946$ 自由度） |
| 单点约束 (SPC) | 1,635 个 `SPC` 节点（全固定 `123456`，共约束 $9,810$ 自由度） |
| 最终有效自由度 | $N_F = 454,704$ |

| PID / MID | 单元数量 | 截面厚度 $t$ | 膜刚度 $\boldsymbol A = t\boldsymbol C_0$ | 弯曲刚度 $\boldsymbol D = \frac{t^3}{12}\boldsymbol C_0$ | 剪切刚度 $\boldsymbol A_s = \frac{5}{6}Gt\boldsymbol I_2$ | 载荷分布 |
|---|---:|---:|---|---|---|---|
| **PID 1** | 32,594 | $0.8$ | $0.8\,\boldsymbol C_0$ | $0.04267\,\boldsymbol C_0$ | $0.6667\,G\boldsymbol I_2$ | 无 |
| **PID 3** | 32,594 | $2.5$ | $2.5\,\boldsymbol C_0$ | $1.30208\,\boldsymbol C_0$ | $2.0833\,G\boldsymbol I_2$ | 无 |
| **PID 4** | 32,594 | $0.3$ | $0.3\,\boldsymbol C_0$ | $0.00225\,\boldsymbol C_0$ | $0.25\,G\boldsymbol I_2$ | 承受 `PLOAD4 21` 均匀面压 |

---

### 2.2 PLOAD4 面载荷等效节点力

面压载荷作用于 PID 4 区域（32,594 个单元），压力标量为 $p = -5\times 10^{-6}$。通过双线性插值转化为单元 24 维一致等效节点力向量：

$$
\boldsymbol f^e = \int_{\Omega_e} p\,N_a(\xi,\eta)\,\boldsymbol n_e\,\mathrm dA \in \mathbb R^{24}.
\tag{3}
$$

---

## 3. 边界条件与多点约束代数消除

### 3.1 自由度维度闭合分析

```
未约束全局自由度 N0 = 98,910 × 6 = 593,460
   │
   ├─ MPC 从属自由度 ND = (10,543 [RBE2] + 10,948 [RBE3]) × 6 = 128,946
   │
   ▼
MPC 独立自由度 NI = N0 - ND = 464,514
   │
   ├─ SPC 固定自由度 NS = 1,635 × 6 = 9,810
   │
   ▼
最终保留自由自由度 NF = NI - NS = 454,704
```

维度闭合严格成立：$N_F = 454,704$ 为最终线性方程组的阶数。

---

### 3.2 多点约束 (MPC) 的代数构造

#### 1. RBE2 刚性从属约束
`RBE2` 强制从节点与独立主节点之间保持空间刚体运动：

$$
\begin{bmatrix}
\boldsymbol u_d \\
\boldsymbol\theta_d
\end{bmatrix}
=
\begin{bmatrix}
\boldsymbol I_3 & -\widehat{\boldsymbol r}_{dm} \\
\boldsymbol 0 & \boldsymbol I_3
\end{bmatrix}
\begin{bmatrix}
\boldsymbol u_m \\
\boldsymbol\theta_m
\end{bmatrix},
\qquad
\widehat{\boldsymbol r}_{dm} =
\begin{bmatrix}
0 & -r_z & r_y \\
r_z & 0 & -r_x \\
-r_y & r_x & 0
\end{bmatrix}.
\tag{4}
$$

#### 2. RBE3 加权插值约束
`RBE3` 将参考从属节点的位移定义为一组独立节点位移的加权平均，满足静力平衡等效条件：

$$
\boldsymbol q_{\mathrm{ref}} = \sum_{j \in \mathcal N_{\mathrm{ind}}} w_j \boldsymbol T_j \boldsymbol q_j,
\qquad
\sum_{j} w_j = 1.
\tag{5}
$$

---

### 3.3 统一约束投影与全局线性系统装配

将所有 RBE2、RBE3 以及齐次 SPC 约束统一表示为从属自由度向自由自由度的线性映射，定义全局约束投影矩阵 $\boldsymbol T \in \mathbb R^{N_0 \times N_F}$：

$$
\boldsymbol q = \boldsymbol T \boldsymbol q_F.
\tag{6}
$$

利用虚功原理，最终全局求解系统为

$$
\boxed{
\boldsymbol K_F \boldsymbol q_F = \boldsymbol f_F
}
\tag{7}
$$

其中全局刚度与载荷直接由单元算子通过局部提取算子 $\boldsymbol T_e \in \mathbb R^{24 \times N_F}$ 投影求和得到：

$$
\boldsymbol K_F = \sum_{e=1}^{N_e} \boldsymbol T_e^{\mathsf T} \boldsymbol K^e \boldsymbol T_e,
\qquad
\boldsymbol f_F = \sum_{e=1}^{N_e} \boldsymbol T_e^{\mathsf T} \boldsymbol f^e.
\tag{8}
$$

该形式给出了无需先生成未约束大矩阵 $\boldsymbol K$、直接在单元张量层完成 MPC 消除与直接装配的现代 GPU/张量化数学依据。

---

## 4. 与胡张元/拓扑优化研究的关系

| 评价项 | 判断 | 评注 |
|---|---|---|
| 薄壁板壳几何 | 是 | 97,782 个四节点板壳单元 |
| 大规模自由度 | 是 | 原始 59.3w DOF，约束后 45.5w DOF |
| 多点约束 (MPC) 复杂性 | 是 | 21,491 个 RBE2/RBE3 约束网络 |
| 抗剪切自锁机制 | 是 | 采用 MITC4 混合插值 |
| 胡–张（Hu–Zhang）混合元适用性 | 待扩展 | 胡–张混合元目前主要针对三维/二维连续体弹性力学；板壳应力–位移混合元仍属理论扩展方向 |
| 拓扑优化设计域 | 未定义 | 模型未定义设计变量与材料插值模型 |
| 局部应力约束 | 未定义 | 仅定义全局线性静力载荷与位移 |
| 可直接加入当前论文 | 否 | 当前论文针对二维连续体拓扑优化 |
| 合适用途 | 张量化前向求解器基准、MPC 消除代数性能测试 |

---

## 5. 改造成科研/拓扑优化算例的路径

1. **明确板壳拓扑优化范式**：
   - 确定设计域（例如选取 PID 1 或 PID 4 区域作为设计域，PID 3 加强筋区域作为非设计域）；
   - 引入板壳 SIMP 材料插值模型（膜刚度 $\rho^p \boldsymbol A$ 与弯曲刚度 $\rho^p \boldsymbol D$）或板厚优化模型（Thickness Optimization）。
2. **多点约束的伴随敏度分析 (Adjoint Sensitivity with MPC)**：
   - 在含 RBE2/RBE3 约束的系统中，目标函数 $\Phi(\boldsymbol q_F, \boldsymbol\rho)$ 的敏度需要推导伴随方程：
     $$
     \boldsymbol K_F \boldsymbol\lambda_F = -\frac{\partial \Phi}{\partial \boldsymbol q_F},
     \qquad
     \frac{\mathrm d \Phi}{\mathrm d \rho_e} = \frac{\partial \Phi}{\partial \rho_e} + \boldsymbol\lambda_F^{\mathsf T} \boldsymbol T_e^{\mathsf T} \frac{\partial \boldsymbol K^e}{\partial \rho_e} \boldsymbol T_e \boldsymbol q_F.
     $$
3. **混合元与新型离散扩展**：
   - 将 MITC4 剪切场与混合变分原理结合，探索薄壁壳结构中的应力鲁棒求解。

---

<details>
<summary>BDF 复原记录</summary>

- **引用链关系**：`CQUAD4 → PID → PSHELL → MID → MAT1`。
- **单元与截面**：
  - PID 1: 32,594 个单元，厚度 $t=0.8$；
  - PID 3: 32,594 个单元，厚度 $t=2.5$；
  - PID 4: 32,594 个单元，厚度 $t=0.3$；
  - 合计 97,782 个 `CQUAD4` 单元。
- **约束网络**：
  - 10,543 个 `RBE2` 单元（全自由度 `123456`）；
  - 10,948 个 `RBE3` 单元（全自由度 `123456`）；
  - `SPCADD 9` 引用 `SPC 3`，共指定 1,635 个节点全固定（`123456`）；
  - MPC 从属自由度集与 SPC 自由度集无冲突，自由度维度严格闭合于 $N_F = 454,704$。
- **载荷卡片**：
  - `PLOAD4 21` 作用于 PID 4（32,594 个单元），压力标量为 $-5\times 10^{-6}$。
- **源文件校验**：
  - 文件：`DLUTFEM-20260720/testcases/50w-2d.bdf`
  - 大小：13,828,970 字节
  - SHA256：`64D2783811E4619147CDB4652FA3F095CCA86F6240567EE21408097578EE5E1D`
  - 最后修改时间：`2025-12-10 15:52:14`

</details>
