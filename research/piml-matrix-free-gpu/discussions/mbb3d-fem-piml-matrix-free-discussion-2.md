---
title: "第二次讨论材料：全尺度 FEM 与 PIML 子结构的 Matrix-Free 实现对照"
tags:
  - PIML
  - matrix-free
  - discussion
status: draft
date_added: 2026-11-02
date_update: 2026-11-03
---

# 三维 MBB 梁：全尺度 FEM 与 PIML 子结构的 Matrix-Free 实现对照

## 1. 研究对象与实现层次

围绕三维线弹性拓扑优化中的状态分析，比较全尺度 FEM、PIML 子结构全边界缩聚和角点缩聚的 Matrix-Free 实现，分析各层次省略的存储及相应计算代价。

### 1.1 三类分析模型总览

记单子结构内部、边界及角点自由度数分别为 $n_i,n_b,n_c$，总自由度数为 $n_d=n_i+n_b$；全局自由度数记为 $N_h,N_\Gamma,N_C$。

| 模型 | 全局未知量 | 局部映射与缩聚算子 | 位移恢复 |
|---|---|---|---|
| 全尺度 FEM | 细网格位移 $u\in\mathbb R^{N_h}$ | 无子结构缩聚，细单元刚度 $K_e=E(\rho_e)K^0$ | 直接得到全场位移 |
| PIML 全边界缩聚 | 全部边界位移 $U_\Gamma\in\mathbb R^{N_\Gamma}$ | $\widehat N^j=[I;\widehat N_i^j]$，$\widehat K_s^j=(\widehat N^j)^{\mathsf T}K^j\widehat N^j\in\mathbb R^{n_b\times n_b}$ | 边界位移取全局解，内部位移由 $\widehat N_i^j$ 恢复 |
| PIML 角点缩聚 | 角点位移 $U_C\in\mathbb R^{N_C}$ | $\widehat N^j=[\Psi;\widehat N_i^j]$，$\widehat K_c^j=(\widehat N^j)^{\mathsf T}K^j\widehat N^j\in\mathbb R^{n_c\times n_c}$ | 边界位移由 $\Psi$ 插值，内部位移由 $\widehat N_i^j$ 恢复 |

### 1.2 Matrix-Free 实现的两个作用层次

全尺度 FEM 仅涉及“细单元 $\to$ 全局系统”单层映射；而在子结构与 PIML 框架下，数据流跨越“细单元 $\to$ 子结构分块刚度 $\to$ 局部缩聚算子 $\to$ 全局接口系统 $\to$ 内部位移恢复”多个环节（本稿两类 PIML 均常驻本轮预测映射 $\widehat N_i^j$）。判定各方法在哪一层采用 Matrix-Free，可按以下两个正交层次区分**省略什么、常驻什么、重算什么**：

1. **缩聚算子层（Krylov 矩阵向量积方式）**：区分是否显式形成局部缩聚矩阵 $\widehat K_r^j=(\widehat N^j)^{\mathsf T}K^j\widehat N^j$ 与全局缩聚矩阵 $\widehat K_R=\sum_j(A_r^j)^{\mathsf T}\widehat K_r^jA_r^j$（$A_r^j$ 为子结构缩聚自由度限制矩阵）。**显式缩聚**形成 $\widehat K_r^j$ 并组装 $\widehat K_R$，外层 CG 直接计算 $\widehat K_Rx$；**隐式缩聚**不形成缩聚矩阵，每次 CG 先提取各子结构的缩聚自由度向量，经 $\widehat N^j$ 延拓、细尺度刚度 $K^j$ 作用及 $(\widehat N^j)^{\mathsf T}$ 转置投影，再通过 $(A_r^j)^{\mathsf T}$ 将局部结果累加至全局缩聚自由度，完成算子作用。

2. **细尺度刚度层（细单元刚度作用方式）**：区分细尺度刚度 $K$ 或 $K^j$ 的存储与作用方式。**FA** 显式组装全局刚度 $K$ 或子结构刚度 $K^j$（隐式缩聚下常驻其稀疏分块 $K_{bb}^j,K_{ib}^j,K_{ii}^j$）；**参考 EA** 利用 $K_e=E(\rho_e)K^0$，仅保存一份参考单元刚度 $K^0$ 与各单元材料系数；提取单元自由度向量，施加参考刚度乘法与材料系数缩放，再按自由度映射将单元结果累加至全局或子结构自由度，完成刚度作用。

## 2. 全尺度 FEM 的 Matrix-Free 实现

### 2.1 刚度算子的两种实现方案

在结构化六面体网格与 SIMP 本构下，$K_e=E(\rho_e)K^0$，其中 $K^0\in\mathbb R^{n_{\mathrm{loc}}\times n_{\mathrm{loc}}}$ 为单位模量的共享参考单元刚度。

1. **全局 FA**：每轮将单元贡献组装为全局 CSR 矩阵，并直接执行稀疏矩阵向量乘：
   $$
   K=\sum_e A_e^{\mathsf T}\bigl(E(\rho_e)K^0\bigr)A_e,\qquad y=Kx.
   $$
2. **参考 EA**：不形成全局矩阵，也不逐单元保存 $K_e$；仅保留一份 $K^0$ 和各单元模量，每步通过 $A_e$ 提取单元自由度向量，施加参考刚度乘法与模量缩放，再通过 $A_e^{\mathsf T}$ 将单元结果累加至全局自由度，完成刚度作用：
   $$
   y=\sum_e A_e^{\mathsf T}\bigl(E(\rho_e)K^0A_ex\bigr).
   $$

## 3. PIML 子结构的 Matrix-Free 实现

### 3.1 PIML 子结构缩聚与位移恢复

将子结构 $j$ 的自由度分为边界 $b$ 与内部 $i$，刚度矩阵写为
$$
K^j=\begin{bmatrix}K_{bb}^j&K_{bi}^j\\K_{ib}^j&K_{ii}^j\end{bmatrix}
\in\mathbb R^{n_d\times n_d},\qquad n_d=n_b+n_i,\qquad K_{bi}^j=(K_{ib}^j)^{\mathsf T}.
$$
以下考虑子结构内部无外载的情形。PIML 根据当前单元模量预测内部映射的独立列，并由刚体运动约束补全 $\widehat N_i^j$；该映射在本轮求解与恢复中复用。

**全边界缩聚。** 精确内部映射为 $N_i^j=-(K_{ii}^j)^{-1}K_{ib}^j\in\mathbb R^{n_i\times n_b}$。以预测映射 $\widehat N_i^j\in\mathbb R^{n_i\times n_b}$ 构造
$$
\widehat N^j=\begin{bmatrix}I_{n_b}\\\widehat N_i^j\end{bmatrix}\in\mathbb R^{n_d\times n_b},\qquad
\widehat u^j=\widehat N^ju_b^j\in\mathbb R^{n_d},\qquad u_b^j\in\mathbb R^{n_b},\qquad
\widehat K_s^j=(\widehat N^j)^{\mathsf T}K^j\widehat N^j\in\mathbb R^{n_b\times n_b}.
$$
组装全局边界系统，施加支承后求解：
$$
\widehat K_\Gamma=\sum_j(A_b^j)^{\mathsf T}\widehat K_s^jA_b^j\in\mathbb R^{N_\Gamma\times N_\Gamma},\qquad
\widehat K_\Gamma U_\Gamma=F_\Gamma,\qquad U_\Gamma,F_\Gamma\in\mathbb R^{N_\Gamma}.
$$
$F_\Gamma$ 为细网格载荷的边界分量。求解后取 $u_b^j=A_b^jU_\Gamma\in\mathbb R^{n_b}$，由 $\widehat u_i^j=\widehat N_i^ju_b^j\in\mathbb R^{n_i}$ 恢复内部位移。

**角点假设下的缩聚。** 边界位移满足 $u_b^j=\Psi q^j$，其中 $\Psi\in\mathbb R^{n_b\times n_c}$ 为三线性插值矩阵。该假设减少边界自由度，同时引入边界插值近似；精确内部映射为 $N_i^j=-(K_{ii}^j)^{-1}K_{ib}^j\Psi\in\mathbb R^{n_i\times n_c}$。以预测映射 $\widehat N_i^j\in\mathbb R^{n_i\times n_c}$ 构造
$$
\widehat N^j=\begin{bmatrix}\Psi\\\widehat N_i^j\end{bmatrix}\in\mathbb R^{n_d\times n_c},\qquad
\widehat u^j=\widehat N^jq^j\in\mathbb R^{n_d},\qquad q^j\in\mathbb R^{n_c},\qquad
\widehat K_c^j=(\widehat N^j)^{\mathsf T}K^j\widehat N^j\in\mathbb R^{n_c\times n_c}.
$$
组装全局角点系统，施加与边界插值相容的支承后求解：
$$
\widehat K_C=\sum_j(A_c^j)^{\mathsf T}\widehat K_c^jA_c^j\in\mathbb R^{N_C\times N_C},\qquad
\widehat K_CU_C=F_C,\qquad F_C=P^{\mathsf T}F_\Gamma,\qquad U_C,F_C\in\mathbb R^{N_C}.
$$
其中 $P\in\mathbb R^{N_\Gamma\times N_C}$ 为全局角点到完整边界的协调插值，满足 $A_b^jP=\Psi A_c^j$。求解后取 $q^j=A_c^jU_C$，由 $u_b^j=\Psi q^j\in\mathbb R^{n_b}$ 和 $\widehat u_i^j=\widehat N_i^jq^j\in\mathbb R^{n_i}$ 恢复位移。

### 3.2 刚度算子的四种实现方案

1. **显式缩聚 + FA**：按批构造完整子结构刚度 $K^j\in\mathbb R^{n_d\times n_d}$，通过 Galerkin 投影形成局部缩聚矩阵：
   $$
   \widehat K_s^j=(\widehat N^j)^{\mathsf T}K^j\widehat N^j
   \quad\text{或}\quad
   \widehat K_c^j=(\widehat N^j)^{\mathsf T}K^j\widehat N^j.
   $$
   随后分别组装为全局缩聚矩阵，每步 CG 直接执行
   $$
   \text{全边界：}\quad y=\widehat K_\Gamma x,\qquad
   \text{角点：}\quad y=\widehat K_Cx.
   $$
   全局缩聚矩阵常驻；$K^j$ 在局部缩聚矩阵构造后释放，局部缩聚矩阵在组装后释放；$\widehat N_i^j$ 用于局部缩聚矩阵构造，并常驻供位移恢复使用。
2. **显式缩聚 + 参考 EA**：不显式构造完整子结构刚度 $K^j$，而是利用共享参考单元刚度 $K^0$，将各细单元的刚度贡献投影并累加为局部缩聚矩阵：
   $$
   \begin{aligned}
   \text{全边界：}\quad \widehat K_s^j
   &=\sum_{e\subset\Omega^j}(G_e^j\widehat N^j)^{\mathsf T}E(\rho_e)K^0(G_e^j\widehat N^j),\\
   \text{角点：}\quad \widehat K_c^j
   &=\sum_{e\subset\Omega^j}(G_e^j\widehat N^j)^{\mathsf T}E(\rho_e)K^0(G_e^j\widehat N^j).
   \end{aligned}
   $$
   随后分别组装为全局缩聚矩阵，每步 CG 直接执行
   $$
   \text{全边界：}\quad y=\widehat K_\Gamma x,\qquad
   \text{角点：}\quad y=\widehat K_Cx.
   $$
   全局缩聚矩阵常驻；局部缩聚矩阵在组装后释放，作用中间量用后释放；$\widehat N_i^j$ 用于局部缩聚矩阵构造，并常驻供位移恢复使用。
3. **隐式缩聚 + 局部 FA**：按批构造完整子结构刚度 $K^j$，提取并常驻稀疏块 $K_{bb}^j,K_{ib}^j,K_{ii}^j$，局部缩聚矩阵和全局缩聚矩阵均不显式形成。每步 CG 提取各子结构的缩聚自由度向量，经 $\widehat N^j$ 延拓、局部刚度块作用及 $(\widehat N^j)^{\mathsf T}$ 转置投影，再将局部结果累加至全局缩聚自由度：
   $$
   \begin{aligned}
   \text{全边界：}\quad y&=\sum_j(A_b^j)^{\mathsf T}(\widehat N^j)^{\mathsf T}K^j(\widehat N^jA_b^jx),\\
   \text{角点：}\quad y&=\sum_j(A_c^j)^{\mathsf T}(\widehat N^j)^{\mathsf T}K^j(\widehat N^jA_c^jx).
   \end{aligned}
   $$
   局部稀疏刚度块 $K_{bb}^j、K_{ib}^j、K_{ii}^j$ 常驻；完整 $K^j$ 在提取稀疏块后释放，作用中间量用后释放；$\widehat N_i^j$ 常驻，用于每步 CG 的算子作用及位移恢复。
4. **隐式缩聚 + 参考 EA**：局部缩聚矩阵和全局缩聚矩阵均不显式形成；也不构造完整 $K^j$ 或局部刚度块。每步 CG 提取各子结构的缩聚自由度向量，经 $G_e^j\widehat N^j$ 延拓并提取单元自由度向量，施加共享参考单元刚度 $K^0$ 与单元模量 $E(\rho_e)$ 的作用，再通过 $(G_e^j\widehat N^j)^{\mathsf T}$ 转置投影，将各单元贡献累加至子结构缩聚自由度，最后累加至全局缩聚自由度：
   $$
   \begin{aligned}
   \text{全边界：}\quad y
   &=\sum_j\sum_{e\subset\Omega^j}(A_b^j)^{\mathsf T}(G_e^j\widehat N^j)^{\mathsf T}E(\rho_e)K^0\bigl(G_e^j\widehat N^jA_b^jx\bigr),\\
   \text{角点：}\quad y
   &=\sum_j\sum_{e\subset\Omega^j}(A_c^j)^{\mathsf T}(G_e^j\widehat N^j)^{\mathsf T}E(\rho_e)K^0\bigl(G_e^j\widehat N^jA_c^jx\bigr).
   \end{aligned}
   $$
   共享参考刚度 $K^0$、单元材料系数、自由度索引常驻；位移延拓、单元刚度作用、转置投影及按自由度映射累加所需的临时向量和工作数组用后释放；$\widehat N_i^j$ 常驻，用于每步 CG 的算子作用及位移恢复。

## 4. 数值实验结果

### 4.1 实验设置

硬件：CPU：16 核 32 线程，可用内存 45 GiB；NVIDIA GeForce RTX 5070 Ti，可用显存 16 GB。

软件：Ubuntu 24.04，Python 3.12.13；NumPy 2.5.3，SciPy 1.18.1，PyTorch 2.11.0（CUDA 12.8）。

**（1）模型与问题规模**

| 参数       | 取值                                                                                       |
| -------- | ---------------------------------------------------------------------------------------- |
| 问题       | 三维 MBB 梁，顶面中心竖直集中力 $-1$；左端两底角点 $u_x=u_y=u_z=0$，右端两底角点 $u_y=u_z=0$                        |
| 材料       | $E_0=1$，$E_{\min}=10^{-7}$，$\nu=0.3$；修正 SIMP，惩罚指数 $p=3$                                  |
| 网格与离散    | 结构化六面体，$h=1$；一阶 Lagrange 位移元，各方向 2 点 Gauss 积分（每单元 8 个积分点），单元位移自由度数 $n_{\mathrm{loc}}=24$ |
| 子结构划分    | 每个子结构含 $m\times m\times m = 5\times 5\times 5 = 125$ 个细单元，节点数 $6^3=216$                  |
| 单子结构自由度数 | 总自由度 $n_d=648$；内部自由度 $n_i=3(m-1)^3=192$；边界自由度 $n_b=3(6m^2+2)=456$；角点自由度 $n_c=24$         |

**（2）求解与测量配置**

| 参数类别     | 取值与约定                                                                                                  |
| -------- | ------------------------------------------------------------------------------------------------------ |
| 线性系统求解 | 无预条件 CG，相对容差 $10^{-3}$，绝对容差 0，最大迭代次数 10000 |
| 后端与设备    | GPU：PyTorch/CUDA 单卡                                                                                    |
| 子结构批处理规模 | 每批 256 个子结构                                                                                            |
| 进程与线程    | 1 个 Python 进程，单线程运行，不使用 MPI                                                                            |
| 显存口径与上限  | 按 PyTorch 已分配张量的峰值显存统计；显存分配器上限为 $14\text{ GiB}$                                                        |

**（3）PIML 离线样本与网络配置**

两类样本均采用 `float64` 精度；全边界网络采用 `float32` 训练，角点网络采用 `float64` 训练。两类网络均输入 125 维归一化单元模量 $\widehat E_e=E(\tilde\rho_e)/E_0\in[10^{-7},1)$，预测内部映射的独立列，再由刚体运动约束补全。两类网络均采用 MLP，隐藏层使用 tanh、ELU 激活，输出层为线性层；采用 Adam 优化器，训练批量为 256。损失函数为刚体运动约束补全后的内部位移映射与精确标签之间的逐元素 MSE。

| 配置项        | 全边界缩聚                                | 角点缩聚                                      |
| ---------- | ------------------------------------ | ----------------------------------------- |
| 独立输出维数     | $86\,400$                            | $3\,456$                                  |
| 网络结构       | 16 个 MLP 并联，各含 15 个隐藏层，宽 $60\sim200$ | 4 个 MLP 并联，各含 15 个隐藏层，宽 $60\sim200\sim60$ |
| 训练 / 验证样本数 | $32\,000$ / $3\,200$                 | $400\,000$ / $40\,000$                    |
| 选模验证损失     | $8.73\times10^{-7}$                  | $6.39\times10^{-6}$                       |

### 4.2 全尺度 FEM

统计单次结构分析的峰值显存，包含准备、组装、求解，不含优化更新；显存上限为 14 GiB。

| 网格 | 全局组装 FA 峰值（GiB） | 共享参考 EA 峰值（GiB） |
|---|---:|---:|
| $240\times40\times40$ | 3.386 | 0.662 |
| $390\times65\times65$ | OOM | 2.780 |

共享参考 EA 在保持同一有限元刚度算子的前提下，省去全局刚度矩阵及组装缓存，使 240 档峰值显存降低约 80.4%，并在 FA 组装 OOM 的 390 档完成分析。通过共享参考单元刚度直接计算算子作用，可以有效降低存储开销。


### 4.3 PIML 子结构全边界缩聚

统计单次结构分析的峰值显存，包含准备、算子组装、边界条件处理、求解及位移恢复，不含优化更新；显存上限为 14 GiB。

| 细网格划分                   | 显式缩聚 + FA<br>峰值显存（GiB） | 显式缩聚 + 参考 EA<br>峰值显存（GiB） | 隐式缩聚 + 局部 FA<br>峰值显存（GiB） | 隐式缩聚 + 参考 EA<br>峰值显存（GiB） |
| ----------------------- | ---------------------: | ------------------------: | ------------------------: | ------------------------: |
| $210\times 35\times 35$ |                 10.971 |                     8.792 |                     3.698 |                 **2.446** |
| $240\times 40\times 40$ |                    OOM |                    12.411 |                     4.702 |                 **3.230** |
| $270\times 45\times 45$ |                    OOM |                       OOM |                     5.981 |                 **4.225** |
| $390\times 65\times 65$ |                    OOM |                       OOM |                       OOM |                **10.982** |

四种路径的状态分析峰值均出现在算子组装阶段。选取 $210\times35\times35$ 细网格，比较该规模下各方案的算子构造方式及存储开销。

- **显式缩聚 + FA → 显式缩聚 + 参考 EA**：显式 FA 按批构造完整子结构刚度 $K^j\in\mathbb R^{648\times648}$，提取局部刚度块 $K_{bb}^j,K_{ib}^j,K_{ii}^j$，再通过预测映射 $\widehat N_i^j\in\mathbb R^{192\times456}$ 形成局部缩聚矩阵 $\widehat K_s^j\in\mathbb R^{456\times456}$；显式参考 EA 利用共享参考单元刚度 $K^0\in\mathbb R^{24\times24}$ 和单元模量 $E(\rho_e)$，通过单元刚度作用与投影累加直接形成 $\widehat K_s^j$，省去完整 $K^j$ 及局部刚度块的构造。两者均常驻全局边界矩阵 $\widehat K_\Gamma\in\mathbb R^{425232\times425232}$ 及组装缓存；批次 $\widehat K_s^j$ 组装后释放，其余构造与校验中间量用后释放。算子临时存储峰值由 **3.419 降至 1.240 GiB**，算子常驻存储均为 **5.799 GiB**。

- **显式缩聚 + FA → 隐式缩聚 + 局部 FA**：隐式局部 FA 不形成 $\widehat K_s^j$ 和 $\widehat K_\Gamma$，改为在每步 CG 中结合预测映射 $\widehat N_i^j$ 与局部刚度块 $K_{bb}^j,K_{ib}^j,K_{ii}^j$ 完成算子作用。相较显式 FA，省去全局边界矩阵及组装缓存，但局部刚度块由投影后释放改为所有子结构的稀疏数值及共享索引常驻，并保留算子辅助数据。完整 $K^j$ 仍按批构造，在提取刚度块后释放；构造、校验及算子作用中间量用后释放。算子临时存储峰值由 **3.419 降至 0.938 GiB**，算子常驻存储由 **5.799 降至 0.467 GiB**。

- **显式缩聚 + FA → 隐式缩聚 + 参考 EA**：隐式参考 EA 同时省去完整 $K^j$、局部刚度块 $K_{bb}^j,K_{ib}^j,K_{ii}^j$ 及两级缩聚矩阵 $\widehat K_s^j,\widehat K_\Gamma$ 的构造，在每步 CG 中结合预测映射 $\widehat N_i^j$、共享参考单元刚度 $K^0$ 和单元模量 $E(\rho_e)$ 完成位移延拓、单元刚度作用、转置投影与按自由度映射累加。相较显式 FA，不再常驻全局边界矩阵及组装缓存，转而保留 $K^0$、$E(\rho_e)$、自由度索引及算子辅助数据；初始化、校验及算子作用中间量用后释放。算子临时存储峰值由 **3.419 降至 0.037 GiB**，算子常驻存储由 **5.799 降至 0.015 GiB**。

**结论**：当前全边界缩聚实验中，缩聚算子层的隐式化与细尺度刚度层的参考 EA 均能有效降低显存开销。前者省去局部缩聚矩阵 $\widehat K_s^j$、全局边界缩聚矩阵 $\widehat K_\Gamma$ 及其组装缓存；后者利用共享参考单元刚度 $K^0$ 和单元模量 $E(\rho_e)$ 完成刚度作用，避免完整子结构刚度 $K^j$ 的批次构造，并在隐式缩聚下进一步省去局部刚度块 $K_{bb}^j,K_{ib}^j,K_{ii}^j$ 的常驻存储。两者结合的**隐式缩聚 + 参考 EA** 在各测试规模下峰值显存最低。此时，算子存储已大幅压缩，预测内部位移映射 $\widehat N_i^j$、有限元模型与分析数据、网络与预测数据等共有开销成为整体显存的主要负担。


### 4.4 PIML 子结构角点缩聚

统计单次结构分析的峰值显存，包含准备、算子组装、边界条件处理、求解及位移恢复，不含优化更新；显存上限为 14 GiB。

| 细网格划分                 | 显式缩聚 + FA<br>峰值显存（GiB） | 显式缩聚 + 参考 EA<br>峰值显存（GiB） | 隐式缩聚 + 局部 FA<br>峰值显存（GiB） | 隐式缩聚 + 参考 EA<br>峰值显存（GiB） |
| --------------------- | ---------------------: | ------------------------: | ------------------------: | ------------------------: |
| $390\times65\times65$ |                  3.674 |                 **2.219** |                     5.932 |                     2.241 |
| $450\times75\times75$ |                  4.620 |                 **3.380** |                     8.523 |                     3.430 |
| $510\times85\times85$ |                  5.844 |                 **4.905** |                    11.902 |                     4.977 |
| $570\times95\times95$ |                  7.389 |                 **6.834** |                       OOM |                     6.938 |
|                       |                        |                           |                           |                           |

与全边界缩聚不同，角点缩聚采用参考 EA 后，较大规模算例的整体峰值转移至边界条件处理阶段。这是因为角点缩聚减小了预测映射及缩聚矩阵的规模，参考 EA 又避免了完整子结构刚度的构造，使组装峰值降低，而细网格上的边界识别、载荷与约束处理仍需相应工作空间。选取 $510\times85\times85$ 细网格，两条 FA 路径的整体峰值仍位于算子组装阶段，两条参考 EA 路径则位于边界条件处理阶段。下面比较该规模下各方案的算子构造方式及存储开销。

- **显式缩聚 + FA → 显式缩聚 + 参考 EA**：显式 FA 按批构造完整子结构刚度 $K^j\in\mathbb R^{648\times648}$，提取局部刚度块 $K_{bb}^j,K_{ib}^j,K_{ii}^j$，再结合边界插值 $\Psi\in\mathbb R^{456\times24}$ 与预测映射 $\widehat N_i^j\in\mathbb R^{192\times24}$，形成局部角点缩聚矩阵 $\widehat K_c^j\in\mathbb R^{24\times24}$；显式参考 EA 利用共享参考单元刚度 $K^0\in\mathbb R^{24\times24}$ 和单元模量 $E(\rho_e)$，通过单元刚度作用与投影累加直接形成 $\widehat K_c^j$，省去完整 $K^j$ 及局部刚度块的构造。两者均常驻全局角点矩阵 $\widehat K_C\in\mathbb R^{100116\times100116}$ 及组装缓存；批次 $\widehat K_c^j$ 组装后释放，其余构造中间量用后释放。算子临时存储峰值由 **1.909 降至 0.445 GiB**，算子常驻存储均为 **0.128 GiB**。

- **显式缩聚 + FA → 隐式缩聚 + 局部 FA**：隐式局部 FA 不形成 $\widehat K_c^j$ 和 $\widehat K_C$，改为在每步 CG 中结合边界插值 $\Psi$、预测映射 $\widehat N_i^j$ 与局部刚度块 $K_{bb}^j,K_{ib}^j,K_{ii}^j$ 完成算子作用。相较显式 FA，省去全局角点矩阵及组装缓存，但局部刚度块由投影后释放改为所有子结构的稀疏数值及共享索引常驻，并保留边界投影及算子辅助数据。完整 $K^j$ 仍按批构造，在提取刚度块后释放；构造及算子作用中间量用后释放。角点插值将局部缩聚自由度由 456 降至 24，显著缩小了显式系统，却未缩小细尺度刚度块，因此新增常驻开销超过省去的存储。算子临时存储峰值由 **1.909 降至 1.076 GiB**，算子常驻存储由 **0.128 增至 6.860 GiB**，整体峰值反而增加。

- **显式缩聚 + FA → 隐式缩聚 + 参考 EA**：隐式参考 EA 同时省去完整 $K^j$、局部刚度块 $K_{bb}^j,K_{ib}^j,K_{ii}^j$ 及两级角点缩聚矩阵 $\widehat K_c^j,\widehat K_C$ 的构造，在每步 CG 中结合边界插值 $\Psi$、预测映射 $\widehat N_i^j$、共享参考单元刚度 $K^0$ 和单元模量 $E(\rho_e)$ 完成位移延拓、单元刚度作用、转置投影与按自由度映射累加。相较显式 FA，不再常驻全局角点矩阵及组装缓存，转而保留 $K^0$、$E(\rho_e)$、自由度索引、边界投影及算子辅助数据；初始化、校验及算子作用中间量用后释放。当前实现的边界投影及相关辅助数据超过省去的小规模显式角点系统存储，使算子常驻存储由 **0.128 增至 0.420 GiB**；但省去批次刚度构造后，算子临时存储峰值由 **1.909 降至 0.509 GiB**，整体峰值仍低于显式 FA。不过，相较显式参考 EA，进一步隐式化未带来显存收益，该规模的整体峰值由 **4.905 略增至 4.977 GiB**。

**结论**：当前角点缩聚实验中，细尺度刚度层的参考 EA 能有效降低显存开销，而缩聚算子层的隐式化未带来进一步收益。前者利用共享参考单元刚度 $K^0$ 和单元模量 $E(\rho_e)$ 完成刚度作用，避免完整子结构刚度 $K^j$ 的批次构造，并在隐式缩聚下省去局部刚度块 $K_{bb}^j,K_{ib}^j,K_{ii}^j$ 的常驻存储。后者虽然省去局部角点缩聚矩阵 $\widehat K_c^j$、全局角点矩阵 $\widehat K_C$ 及其组装缓存，但边界插值 $\Psi$ 已将局部缩聚自由度由 456 降至 24，显著缩小了显式系统；当前隐式实现所需的边界投影及辅助数据，以及局部 FA 路径额外常驻的细尺度刚度块，超过了省去的存储。因此，在细尺度刚度实现相同的条件下，由显式缩聚改为隐式缩聚，峰值显存反而增加。在当前测试范围内，保留小规模显式角点系统、仅在细尺度刚度层采用参考 EA 的**显式缩聚 + 参考 EA** 在各测试规模下峰值显存最低。

随着问题规模增大，两条参考 EA 路径相较显式缩聚 + FA 的**整体峰值显存相对降幅逐渐缩小**：从 390 档到 570 档，显式参考 EA 由 **39.6% 降至 7.5%**，隐式参考 EA 由 **39.0% 降至 6.1%**。在当前实现与测试范围内，预测内部位移映射 $\widehat N_i^j$、细网格模型与分析数据等共有开销，以及边界条件处理所需的工作空间，逐渐成为限制整体显存收益的主要因素。



# 5 下一步安排

1. **缩聚策略与 Matrix-Free 实现的适配。** 当前全边界缩聚实验中，两个层次的 Matrix-Free 均能有效节省显存；角点缩聚后，显式缩聚矩阵显著缩小，当前隐式实现的边界投影及辅助数据，以及局部 FA 路径常驻的刚度块，超过省去的存储，使相同细尺度刚度实现下的峰值显存反而增加。同时，两条参考 EA 路径相较显式 FA 的整体峰值显存相对降幅随规模增大而缩小。后续需量化缩聚自由度数、子结构细分数及问题规模对存储组成与整体峰值的影响，区分缩聚策略本身与当前实现方式的影响，为不同缩聚策略选择合适的实现组合。

2. **子结构细分数 $m$ 的影响。** 现有实验固定 $m=5$、增大粗网格；固定粗网格、提高 $m$ 则改变局部映射与存储规模，四种实现的显存表现及相对优势可能不同。下一步拟补充变化 $m$ 的实验，并在整数剖分允许时开展同细网格对照，以区分子结构划分变化与细网格总规模增长的影响。

3. **细尺度刚度层的 PA 与 UA 扩展。** 当前细尺度刚度层的 Matrix-Free 实现采用共享参考 EA，后续可进一步考虑部分组装 PA 与不组装 UA，研究其与显式、隐式缩聚的结合方式，比较参考刚度、积分点数据及算子作用中间量的存储与计算开销，评估不同缩聚策略、单元阶次及积分配置下的适用性。

4. **MPI 分布式并行。** 为进一步发挥其减少矩阵存储、按单元或子结构计算的优势，后续拟结合 MPI 分布式并行，利用多 GPU 或多节点的存储与计算资源，评估通信、数据分布与负载均衡对并行效率和单设备峰值显存的影响，扩大可求解规模。

5. **预条件子设计。** 为聚焦不同 Matrix-Free 实现的算子计算与存储开销，统一采用无预条件 CG，以避免预条件配置差异对比较的影响。后续研究适配 Matrix-Free 的预条件方法，综合评估预条件子的构造与存储开销、CG 迭代次数及总求解耗时。

6. **共有开销优化与预测映射按需重算。** 针对算子存储压缩后逐渐突出的共有开销，后续优化细网格模型与分析数据、边界条件处理工作数组的存储；同时参考论文 A high-performance parallel algorithm based on problem independent machine learning (PIML) for large-scale topology optimizatiom 中不常驻预测映射、需要时重新预测的做法，研究预测内部位移映射 $\widehat N_i^j$ 的按需重算，评估峰值显存与计算耗时之间的权衡。

7. **PIML-OFEM 的 Matrix-Free 实现。** 目前考虑非重叠子结构有限元，后续拟将 Matrix-Free 实现拓展至已有的 PIML-OFEM 框架，结合其重叠区域耦合方式，研究适用的算子存储与作用方案，评估其在存储开销和计算效率方面的表现。
