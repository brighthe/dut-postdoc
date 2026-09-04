---
title: "面向大规模拓扑优化的 PIML Matrix-Free 求解与 GPU 协同加速方法研究"
topic: "博士后核心研究项目"
aliases:
  - "博士后核心研究项目"
  - "结构保持 PIML 局部算子与 GPU 加速 Matrix-Free 求解"
  - "已做与未做清单"
  - "面向大规模拓扑优化的 PIML Matrix-Free 求解与 GPU 协同加速研究综述"
  - "面向大规模结构拓扑优化的 PIML 与 Matrix-Free 高性能求解方法"
  - "面向大规模拓扑优化的结构保持 PIML、Matrix-Free 与 GPU 融合研究综述"
  - research/piml-matrix-free/piml-matrix-free-high-performance-solver-survey
  - research/postdoc-plan/long-term/direction-1-piml-matrix-free/piml-matrix-free-high-performance-solver-survey
tags:
  - postdoc
  - core-research-project
  - topology-optimization
  - PIML
  - matrix-free
  - substructuring
  - GPU
  - high-performance-computing
  - status
status: "in-progress"
date_start: 2026-07-22
date_update: 2026-09-04
source: "郭旭老师团队在大规模结构拓扑优化中 PIML 与 Matrix-Free 高性能求解的研究报告.pdf"
related:
  - "../long-term-research-lines.md"
  - "./_index.md"
  - "./matrix-free-research-guide.md"
  - "./piml-research-guide.md"
  - "./gpu-hpc-research-guide.md"
---

# 面向大规模拓扑优化的 PIML Matrix-Free 求解与 GPU 协同加速方法研究

项目按四个方面组织：PIML、Matrix-Free、并行与高性能执行，以及 PIML + Matrix-Free + GPU 融合。前三项分别建立单线基线，第四项研究三线耦合。各基线均需从单次结构分析推进到完整拓扑优化。

各表「状态」栏图标：✅ 已完成 · 🟡 部分完成 · ❓ 待核实 · ⬜ 未开展。

## 一、PIML

本部分研究可复用局部力学表示、结构保持和误差控制。全局接口矩阵采用 CPU 显式组装，用于隔离 Matrix-Free 和 GPU 的影响。

PIML 分析路径的分类维度与文献依据见 [[piml-research-guide#2.3 PIML 代表性分析路径|PIML 代表性分析路径]]；该表以「分析组织」列区分 Full-domain 与 Substructure，本节任务名则自带「子结构」限定，两者指同一组路径。本项目当前重点实现“角点线性迹子结构缩聚变密度拓扑优化基线”和“角点线性迹 PIML 路线 A（形函数预测—变分构造）”。

### 1.1 候选局部表示

| 候选表示          | 学习输出          | 状态  | 当前结果与适用范围                                                                                                                                                                                         |
| ------------- | ------------- | :-: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 多尺度形函数 + 变分构造 | $\mathbf N$   | ✅ | 24 子结构系统下全场位移误差 `0.15%`、柔顺度误差 `0.20%`；形函数误差 `8.97%` 经变分构造后局部刚度误差降至 `0.44%`，log-log 斜率为 `2.00`；当前主路线，来源见 [[../../literature/topopt/piml/translations/Huang2023-PIML-substructure-zh\|Huang 2023]] |
| 缩聚刚度直接预测      | $\mathbf K_s$ | ✅ | 同一比较条件下全场位移误差 `2.01%`、柔顺度误差 `3.64%`；采用 Cholesky 参数化，作为对照路线                                                                                                                                        |
| 坐标连续形函数       | $\mathbf N$   | ⬜ | 计划以 DeepONet 输出形函数，并用伪结构总应变能训练，来源见 [[../../literature/topopt/piml/translations/Huang2024-PIML-datafree-zh\|Huang 2024]]                                                                          |
| 边界位移场到内部位移场   | 场到场           | ⬜ | 三次 Bézier 表示尚未实现，来源见 [[../../literature/topopt/piml/translations/Guo2026-highgeneralization-bezier-zh\|Guo 2026 Bézier]]                                                                         |
| 超采样数值基函数      | 局部降阶基         | ⬜ | 属于重叠载体，需重新定义接口自由度和 gather/scatter 语义，来源见 [[../../literature/topopt/piml/translations/Guo2026-PIML-OFEM-zh\|Guo 2026 PIML-OFEM]]                                                                  |

当前载体为互不重叠的子结构，$\Omega^j\cap\Omega^k=\varnothing$。形函数路线源于 [[../../literature/topopt/piml/translations/Huang2022-problemindependentmachine-zh|Huang 2022]]；Cholesky 参数化是本项目增加的结构设计。

### 1.2 结构分析基线

| 研究任务          | 状态  | 当前结果与适用范围                                                                                                                                                                                                                       |
| ------------- | :-: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 精确子结构静力缩聚     |  ✅  | 与全装配直解的位移、柔顺度相对差 `<2e-12`，作为 PIML 的精确基线和回退目标                                                                                                                                                                                    |
| 子结构 PIML 结构分析 |  ✅  | 24 子结构全局接口矩阵显式组装路径已完成求解和内部位移恢复；代理在役 `0/24` 回退                                                                                                                                                                                   |
| 结构保持          |  ✅  | 多尺度形函数路线满足 $\widetilde{\mathbf K}-\mathbf K_s=\mathbf E^{\mathsf T}\mathbf K_{ii}\mathbf E\succeq0$，刚体零空间残量 `1.2e-16`；直接预测路线采用 $\widehat{\mathbf K}_s=\mathbf R_\perp\mathbf L\mathbf L^{\mathsf T}\mathbf R_\perp^{\mathsf T}$ |
| 子结构层精确回退      |  ✅  | 条件触发后回退精确 FEA 并记录 `used_fallback`；故障注入已验证门禁能够触发；尚未进入拓扑演化过程                                                                                                                                                                      |
| 载荷缩聚          |  ⬜  | 当前继承内部自由度不受载假设；推广到内部受载需补充缩聚载荷和位移恢复项                                                                                                                                                                                             |
| 几何形状作为输入      |  ⬜  | 当前几何固定，改变子结构形状会导致输入输出维度不匹配                                                                                                                                                                                                      |
| 分布外检测         |  ⬜  | 留出集为独立均匀采样，尚未测试拓扑演化产生的空间相关密度场                                                                                                                                                                                                   |

### 1.3 PIML 拓扑优化闭环

| 研究任务                    | 状态  | 当前结果与适用范围                                                                                                                                                                                                                  |
| ----------------------- | :-: | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 完整接口子结构缩聚变密度拓扑优化        |  ⬜  | 接口迹取 `full_trace`，不作接口降阶，设计变量仍为细网格单元密度。判据是与普通 Lagrange FA 逐迭代柔度、体积分数、灵敏度和最终拓扑一致到舍入精度（等价前提见 [[../../concepts/substructural-condensation#2.6 “精确等价”的条件与边界\|精确等价的条件与边界]]）。用途是分离缩聚—恢复—伴随链路的实现误差与式 (16) 迹降阶误差；保留全部接口自由度，仅限小规模验证 |
| 角点线性迹子结构缩聚变密度拓扑优化       | 🟡  | 精确局部 Schur 缩聚 + 式 (16) 角点线性迹 + CPU 显式宏观求解，不引入 PIML、Matrix-Free 或 GPU。密度—局部网格—单元序双向映射、MBB 载荷与约束契约、三维宏观八角点映射已修复，2D/3D 映射与边界专项测试、式 (16) 能量恒等、精确路径灵敏度有限差分均已通过；尚需在统一工况下重跑 2D/3D 完整优化并固定可重放证据                                    |
| 角点线性迹 PIML 路线 A 变密度拓扑优化 |  ✅  | 已完成 2D（24 子结构）与 3D（48 个 Hex8 子结构）MBB 梁闭环：形函数预测与式 (17) 变分构造、细观位移恢复、伴随灵敏度、空间滤波与 OC 更新。相对角点线性迹子结构缩聚基线，2D 最终柔度误差 `3.02%`（47 步 vs 41 步），3D `3.65%`（42 步 vs 36 步）；证据见 `soptx:experiments/piml_substructure_topopt/`              |
| 角点线性迹 PIML 路线 B 变密度拓扑优化 |  ⬜  | 在与路线 A 相同的 `linear_corner` 接口迹与 SIMP 设置下直接预测角点降阶刚度 $(\widetilde{\mathbf K}_j^h)^L$；需完成结构性质与灵敏度检查、2D/3D MBB 闭环，并与基线及路线 A 对比柔度历史、体积分数、迭代数和最终拓扑                                                                               |

普通 Lagrange FA 是各路径共用的正确性参照，不在本节单列独立任务。完整接口子结构缩聚与 FA 代数等价，其拓扑优化闭环不产生独立数值结论，因此只作为实现门禁单列任务，不作为精度参照；三条路径的关系是「完整接口 → 角点线性迹 → PIML 局部代理」，后两步分别引入迹降阶误差与代理误差。代表性路径的分类、接口迹与文献来源见 [[piml-research-guide#2.3 PIML 代表性分析路径]]；后续其他类型的 PIML 拓扑优化在本表新增独立任务。

## 二、Matrix-Free

本部分使用精确局部算子，研究无全局矩阵的算子作用、Krylov 求解和完整拓扑优化。PIML 近似与 GPU 加速不进入该基线。

Matrix-Free 分析路径的装配层级、局部载体、保存／重算对象及文献依据见 [[matrix-free-research-guide#2.3 Matrix-Free 代表性分析路径|Matrix-Free 代表性分析路径]]。本项目当前重点实现“单元级 EA/EbE 精确 Matrix-Free”和“子结构载体精确 EA Matrix-Free”，FA/TA 只作正确性参照，PA/QA 与 UA/NONE 在前两条路径闭环后推进。

### 2.1 结构分析基线

| 研究任务 | 状态 | 当前结果与适用范围 |
|---|:--:|---|
| FA 结构分析参照 | ✅ | 完成 2D/3D 制造解 $L_2$ 收敛阶、载荷等效与残差验证；证据见 `soptx:examples/lagrange_elasticity/` |
| FA 显式装配内存机制与容量极限 | ✅ | 完成 FA 各路线内存机制与容量上限测试；证据见 `soptx:experiments/fa_assembly_capability/` |
| EA 单元装配内存机制与容量极限 | 🟡 | 验证算子代数恒等（误差 `<1e-12`）；尚未基于模式先行新架构重新标定；证据见 `soptx:experiments/ea_assembly_capability/` |
| 子结构载体的精确 EA Matrix-Free 算子 | 🟡 | NumPy/PyTorch 双后端与显式装配恒等 `<1e-15`，裸 CG 端到端一致；尚无独立时间和峰值内存实测 |
| PA/QA 部分组装 | ⬜ | 存储进一步下降需从 PA 开始，装配层次见 [[../../concepts/matrix-free/assembly-levels]] |
| UA（严格 fully matrix-free） | ⬜ | 尚未实现；MFEM 中对应 `AssemblyLevel::NONE` |
| GMRES / Flexible Krylov | ⬜ | 已写入研究方案，尚未实现 |
| 预条件子 | ⬜ | 无预条件 CG 的迭代数随分辨率按 64→134→250→493→600 增长 |

### 2.2 Matrix-Free 拓扑优化闭环

| 研究任务                       |  状态  | 当前结果与适用范围                                                                                                                                              |
| -------------------------- | :--: | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| FA 变密度拓扑优化                 | ❓ | 作为 Matrix-Free 路径的验收参照；需核实材料插值、滤波、灵敏度、OC/MMA 更新、柔顺度与体积分数历史及最终拓扑是否已有可重放证据                                                                               |
| EA/EbE Matrix-Free 变密度拓扑优化 | 🟡 | `soptx:examples/topopt_platform/topopt_3d_simp_real.py` 已接通完整 SIMP 优化循环，完成三维 GPU 全流程和小规模 NumPy/PyTorch 验证；尚缺完整 FA 迭代参照及统一条件下的柔顺度、灵敏度、体积分数历史、迭代数和最终拓扑对照 |
| 精确子结构 Matrix-Free 密度法拓扑优化  | ⬜ | 在完整优化循环中接通接口求解、内部位移恢复、灵敏度和密度更新，并与 FA 参照比较柔顺度历史、优化迭代数及最终拓扑；作为后续子结构 PIML–Matrix-Free 融合的直接基线                                                             |

FA 路径仅作为正确性参照，不计入 Matrix-Free 任务完成状态。

后续 MMC/MMV 等其他拓扑描述方法在本表新增独立任务。

## 三、并行与高性能执行

本部分固定离散问题、算子来源和停止准则，按并行层级比较正确性、完整时间和峰值内存。线程级、进程级与设备级在此都是**评价口径的受控变量**，不是独立研究对象；PIML 与 Matrix-Free 的算法增量分别由前两部分评价。

所有加速比的分母都由并行配置决定，因此本部分每条时间类结论都必须附带线程数、进程数与设备的实际取值，口径与当前缺口见 §3.5。

### 3.1 线程级（节点内）

| 研究任务     | 状态  | 当前结果与适用范围                                                                                                                                    |
| -------- | :-: | -------------------------------------------------------------------------------------------------------------------------------------------- |
| 线程级并行    |  ⬜  | 待同构节点。本机为 i9-14900KF（8 P-core + 16 E-core 混合架构），WSL2 只暴露虚拟化的「16 核 × 2 线程」拓扑、无法核绑定，且系统 `libdmumps-5.6` 未链 `libgomp`（无 OpenMP），不具备可信的线程扩展性测量条件 |
| 吃线程环节的识别 | 🟡  | 按实现路径分析（非实测）：装配、Matrix-Free 算子作用、直接法数值分解、PIML 推理与训练为计算受限可并行段；密度/灵敏度滤波、SIMP 插值、OC 更新在 NumPy 后端串行、在 PyTorch 后端并行但受内存带宽限制。尚无线程扫描实测曲线            |

### 3.2 进程级（MPI）

| 研究任务 | 状态 | 当前结果与适用范围 |
|---|:--:|---|
| 纯 MPI 并行 CG 参照 | ✅ | 823,875 自由度，16 进程相对单进程 `3.69` 倍，迭代数恒为 `493`；与 GPU 属于不同并行层级。该倍数取得时未控制每进程的 BLAS 线程数，存在 oversubscribe 导致低估的可能，待复核 |
| 直接法的 MPI 路径 | ⬜ | `soptx:src/soptx/solvers/direct.py` 的两条 MUMPS 路径都走 `set_centralized_sparse` 集中式输入、解在 host 上取回，因此无法比较多进程布局。阶段划分上须区分：`DirectSolver` 已拆成 `setup` 的 `job=4`（分析 + 数值分解）与 `_solve` 的 `job=3`（只回代），因子在实例内缓存，同一矩阵多右端项可复用；但 `job=4` 仍把**分析与数值分解绑在一起**，稀疏结构不变、只有数值改变的重复求解每次都在重做符号分析，而函数式 `spsolve` 的 `_mumps_solve` 走 `job=6`，三阶段全部重做。两项改造互相独立：多进程测量的前置是把集中式输入换成 `ICNTL(18)=3` 分布式；符号分解复用的前置是把 `job=4` 拆成全程一次 `job=1` 加每步 `job=2`，后者对本项目「每步在同一网格上重装配」的优化循环本身即为收益。两者都不需要更换求解器库；求解器的并行模型、三阶段接口与构建判别见 [[../../concepts/linear-solvers/direct-methods#3. 主流实现与并行模型]]。**前置检查**：若系统 MUMPS 链接的是 `libmpiseq` 桩库，则该构建无法多进程运行，接口改造前需先确认链接的是真实 MPI 库 |

### 3.3 设备级（GPU）

| 研究任务 | 状态 | 当前结果与适用范围 |
|---|:--:|---|
| 单卡 GPU 结构求解 | ✅ | 相对同后端 CPU 的 16 条 `torch` 线程约 `16` 倍，中位数 `16.08`、区间 `14.9`–`16.6`。该 16 线程是 PyTorch 读取 WSL2 虚拟拓扑得到的默认值而非选定配置，口径见 §3.5 |
| 多后端统一调度 | ✅ | FEALPy 平台由 `76.07 s` 降至 `4.82 s`，加速 `15.8` 倍；求解阶段 `17.0` 倍；两侧误差 `<1e-14`；`n_dofs 1604043`。端到端与求解阶段两个倍数接近，说明 CPU 侧的串行段已计入分母 |
| PIML 批量推理与缩聚重构 | ❓ | `experiments/piml_capability` 记录单卡 24–384 子结构用时 `0.23~3.32 ms`、相对 CPU `22~26` 倍；结果页尚未统一回填，CPU 分母的线程配置亦未记录 |
| PIML 批量训练 | ❓ | 有 2000 样本、4000 epochs 的训练配置，但训练设备和批量训练实测尚未明确 |
| 单节点多卡 GPU | ⬜ | 计划在项目中后期研究 |
| 多节点 MPI–GPU | ⬜ | 计划在项目后期研究 |
| GPU 直接法对照 | ⬜ | MUMPS、PARDISO、CPardiso 均为 CPU 求解器（依据见 [[../../concepts/linear-solvers/direct-methods#5. GPU 支持现状]]），因此本项目的直接法基线天然是 CPU-only。当前取保守口径：报数时显式声明直接法基线为 CPU 满配，GPU 倍数只用于 Matrix-Free 路径的同后端自比，不与直接法混谈。若要形成干净的「GPU 直接法 vs GPU Matrix-Free」算法对比，需接入 cuDSS（其 MG / MGMN 模式分别对应上两行）；显存容量比主存更早触及填充增长上限，对本项目的内存墙论证有利。列为后备任务，不进入前三项基线闭环的关键路径 |

### 3.4 完整拓扑优化基线

| 研究任务 | 状态 | 当前结果与适用范围 |
|---|:--:|---|
| GPU 完整拓扑优化 | ❓ | 需在统一算例、停止准则和计时口径下核实完整优化历史、CPU/GPU 结果一致性、端到端时间及峰值显存 |

### 3.5 计时口径与环境记录

| 研究任务 | 状态 | 当前结果与适用范围 |
|---|:--:|---|
| CPU 基线的线程配置 | 🟡 | 实测当前环境 `OMP_NUM_THREADS` / `OPENBLAS_NUM_THREADS` / `MKL_NUM_THREADS` 均未设置，各组件按各自默认运行：PyTorch `16`、numpy/scipy 的 OpenBLAS 按在线 CPU 数 `32`、MKL `16`、scipy SuperLU 串行 `1`、系统 MUMPS 无 OpenMP。§3.2 与 §3.3 的全部加速比分母均在此未受控状态下取得 |
| 报数运行的口径约定 | ⬜ | 拟约定：凡进入证据页、申请书或论文的时间数字，必须以命令行前缀显式固定三个线程变量并记录取值，CPU 基线同时报 1 线程与满配两个端点；测量工具拟落在 `soptx:examples/parallel_execution/benchmark_thread_scaling.py`，只扫 §3.1 识别出的计算受限段。直接法一侧另需记录 **BLAS 后端**（MKL / OpenBLAS）与 MPI×线程布局：同一 MUMPS 在不同布局下换后端可反转快慢结论，外部实测见 `dut-institute-work:staging/cpardiso-mumps-solver-comparison.md`（该文件待迁入 `hpc/`，指针需随之更新） |

## 四、PIML + Matrix-Free + GPU

本部分在前三项完整拓扑优化基线的基础上，让 PIML 预测的局部算子进入 Matrix-Free 全局作用，并在 GPU 上完成预测、局部作用、归约和 Krylov 求解。

$$
\widehat{\mathbf A}\mathbf x
:=
\sum_j
\mathbf G_j^{\mathsf T}
\widehat{\mathbf K}_j
\mathbf G_j\mathbf x .
$$

| 研究任务 | 状态 | 当前结果与适用范围 |
|---|:--:|---|
| PIML 近似 Matrix-Free 算子正确性 | ✅ | PIML 局部算子已进入 gather—局部作用—scatter-add，与对应显式路径恒等；限 24 子结构，无预条件和性能实测 |
| PIML → Matrix-Free → Krylov GPU 全链 | ⬜ | 尚未形成预测、局部作用、gather/scatter、归约和 Krylov 全程显存驻留的计算链 |
| 精确 Matrix-Free 真残差复核 | ⬜ | 尚未实现 |
| 自适应精度控制、缺陷校正和预条件更新 | ⬜ | 尚未实现 |
| 拓扑演化下的动态可靠性 | ⬜ | 尚未形成分布外识别、精确回退与全局求解联动 |
| 融合完整拓扑优化流程 | ⬜ | 依赖 §1.3、§2.2 和 §3.2 三项完整拓扑优化基线 |
| 四类路径逐层消融 | ⬜ | 比较精确组装、精确 Matrix-Free、PIML 近似组装和 PIML 近似 Matrix-Free，统一评价精度、收敛、时间和显存 |
| 百万级以上与多节点扩展 | ⬜ | 当前 PIML 路径只验证到 24 子结构 |
| 局部误差到全局谱、预条件和 Krylov 收敛的传播机制 | ⬜ | 尚未形成理论与数值证据 |
| 时间—显存—通信性能模型 | ⬜ | 尚未建立 |
| 缓存、按需重算和算子融合 | ⬜ | 尚未开展系统实验 |
| 离线训练、在线预测、单次求解和完整流程的成本分解 | ⬜ | 尚未形成统一统计 |

依赖关系为：

$$
\text{PIML 基线}
+
\text{Matrix-Free 基线}
+
\text{并行执行基线}
\longrightarrow
\text{三线融合} .
$$