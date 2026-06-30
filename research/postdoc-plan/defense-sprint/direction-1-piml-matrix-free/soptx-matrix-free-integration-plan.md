---
title: "SOPTX 中 Matrix-Free 线弹性算子与拓扑优化集成计划"
tags:
  - execution-plan
  - matrix-free
  - SOPTX
  - FEALPy
  - topology-optimization
  - GPU
  - high-performance-computing
status: "in-progress"
date: 2026-06-26
date_update: 2026-06-29
related:
  - one-week-defense-sprint-plan
  - matrix_free_math_principles
  - piml-matrix-free-execution-plan
---

# SOPTX 中 Matrix-Free 线弹性算子与拓扑优化集成计划

> **当前实现进度以 soptx 仓库 `ai/common/progress-matrix-free.md` 为准**（权威实时态）。
> 本文档是**计划/路线图**（描述意图与任务划分），不随实现进度逐步改写；现状/已完成情况看 soptx 的 progress 文档。
> 截至 2026-06-29：soptx 已完成阶段一~四（matvec/CG 一致、2D/3D 真·contraction 不形成 Ke、NumPy benchmark），下一步 GPU/多后端。

本文档用于把答辩前 Matrix-Free 高性能求解能力的展示，落实为一个可逐项实现、验证和生成图表的短期开发计划。

当前策略是：**尽量减少对 FEALPy 的修改，将 Matrix-Free 原型主要整理到 SOPTX 中实现**。FEALPy 继续作为网格、有限元空间、自由度映射和基础后端支撑；SOPTX 负责线弹性积分子、SIMP 材料插值、拓扑优化循环、多后端/GPU 能力和 Matrix-Free 求解模块。

## 1. 总体目标

在 SOPTX 中建立一个最小可运行的 Matrix-Free 线弹性结构分析模块，使拓扑优化流程能够从传统的

```text
组装全局刚度矩阵 K(rho) -> solve(K, f)
```

切换为

```text
Matrix-Free 算子作用 y = K(rho)x -> Krylov 迭代求解
```

并完成以下验证：

1. **正确性验证**：Matrix-Free `matvec(x)` 与显式组装矩阵 `K @ x` 在机器精度内一致；
2. **求解闭环验证**：在一个小型 MBB 梁或悬臂梁算例中，Matrix-Free CG 能求解状态方程；
3. **拓扑优化接入验证**：SOPTX 单次或多次优化迭代可选择 Matrix-Free 分析器；
4. **性能展示验证**：记录 MatVec 时间、CG 迭代次数、内存估计和 GPU/多后端潜力，为答辩图表提供依据。

## 1.1 开发仓库与分支约定

本文档只作为 `dut-postdoc` 知识库中的任务计划与答辩口径记录。实际程序开发应切换到 SOPTX 仓库进行：

```text
C:\workspace\soptx_heliang
```

建议在 SOPTX 仓库中新建独立功能分支：

```text
codex/matrix-free-interface
```

该分支只承载 Matrix-Free 接口版原型，避免污染 `develop` 主线。实现过程中应遵守以下约定：

1. **代码修改发生在 SOPTX 仓库**：不要在 `dut-postdoc` 中放置临时代码或测试脚本；
2. **计划与结论沉淀在 dut-postdoc**：阶段性设计、验证结果和答辩口径回填到本文档或相关 research 文档；
3. **先接口版，后高性能版**：第一轮只要求打通 `action()`、`matvec()`、`K @ x` 对比和 CG 调用，不要求立即实现真正不形成 `Ke` 的张量收缩 kernel；
4. **每个阶段有可运行测试**：新增功能必须配套一个最小测试或 benchmark，避免只写接口不验证。

推荐切换后的第一组 Git 操作：

```text
cd C:\workspace\soptx_heliang
git switch develop
git pull
git switch -c codex/matrix-free-interface
```

若本地 `develop` 已有未提交改动，应先检查并决定是否暂存、提交或另开分支，不应直接覆盖。

## 2. 软件分工

### 2.1 FEALPy 侧：尽量保持只读依赖

FEALPy 侧原则上不新增 Matrix-Free 主模块，只复用已有能力：

- mesh / cell / node 数据结构；
- finite element space；
- quadrature rule；
- cell-to-dof 映射；
- boundary dof 查询；
- backend manager 或张量后端接口。

如确有必要，只在 FEALPy 中补充极薄的访问接口，不把 Matrix-Free 业务逻辑放入 FEALPy。

### 2.2 SOPTX 侧：新增 Matrix-Free 分析模块

SOPTX 是本计划的主承载位置。建议新增或整理如下模块：

```text
soptx/
  analysis/
    matrix_free/
      __init__.py
      elasticity_operator.py
      boundary.py
      diagonal.py
      krylov.py
  benchmarks/
    benchmark_matrix_free_elasticity.py
  examples/
    mbb_matrix_free.py
  tests/
    test_matrix_free_vs_assembled.py
```

若 SOPTX 现有目录命名不同，应保持原项目风格，将上述功能并入已有 `analysis`、`solver`、`integrator` 或 `benchmark` 层。

## 3. 核心代码任务

### T1. 为现有线弹性积分子增加局部算子作用接口

SOPTX 中已经实现线弹性积分子，因此 Matrix-Free 不应重写一套弹性理论，而应在已有积分子上补充 `action()` 方法。

建议接口：

```python
class LinearElasticIntegrator:
    def assemble(self, ...):
        """已有：返回单元矩阵或组装全局矩阵所需贡献。"""
        ...

    def action(self, xe, rho, material_model):
        """
        新增：Matrix-Free 局部算子作用。

        Parameters
        ----------
        xe
            单元局部位移向量，形如 (NC, ldof, GD)。
        rho
            单元密度或积分点密度。
        material_model
            SIMP 或其他材料插值模型。

        Returns
        -------
        ye
            单元局部刚度作用结果，形如 (NC, ldof, GD)。
        """
        ...
```

该接口内部执行：

```text
局部位移 xe
  -> 高斯点位移梯度 grad u
  -> 应变 epsilon(u)
  -> SIMP 材料参数 E(rho), lambda(rho), mu(rho)
  -> 应力 sigma
  -> B^T sigma 积分回单元节点力 ye
```

验收标准：

- 同一个积分子既能 `assemble()`，也能 `action()`；
- 两者使用相同的形函数梯度、Jacobian、权重和材料插值逻辑；
- 不出现两套彼此独立的线弹性实现。

### T2. 实现 `MatrixFreeElasticityOperator`

新增 SOPTX 侧算子封装：

```python
class MatrixFreeElasticityOperator:
    def __init__(
        self,
        mesh,
        space,
        integrator,
        material_model,
        rho,
        backend=None,
        dirichlet_dofs=None,
    ):
        self.mesh = mesh
        self.space = space
        self.integrator = integrator
        self.material_model = material_model
        self.rho = rho
        self.backend = backend
        self.dirichlet_dofs = dirichlet_dofs

    def update_density(self, rho):
        self.rho = rho

    def matvec(self, x):
        x = self.apply_input_bc(x)
        xe = self.gather(x)
        ye = self.integrator.action(xe, self.rho, self.material_model)
        y = self.scatter_add(ye)
        y = self.apply_output_bc(y, x)
        return y
```

关键子函数：

```python
def gather(self, x):
    cell2dof = self.space.cell_to_dof()
    return x[cell2dof]

def scatter_add(self, ye):
    cell2dof = self.space.cell_to_dof()
    y = zeros_global_vector()
    backend.scatter_add(y, cell2dof, ye)
    return y
```

验收标准：

- `matvec(x)` 不显式组装全局矩阵；
- 支持密度更新 `update_density(rho)`；
- 支持 NumPy 后端，后续可扩展 PyTorch/JAX；
- Dirichlet 自由度处理与组装式分析保持一致。

### T3. 实现边界条件处理

Matrix-Free 中不能通过修改矩阵行列处理 Dirichlet 边界，因此需要向量级处理。

建议新增：

```python
class MatrixFreeDirichletBC:
    def __init__(self, fixed_dofs):
        self.fixed_dofs = fixed_dofs

    def apply_input(self, x):
        ...

    def apply_output(self, y, x=None):
        ...
```

第一阶段可采用简化策略：

- `matvec` 输入前将固定自由度置零；
- `matvec` 输出后将固定自由度置为与求解器约定一致的值；
- RHS 中固定自由度对应项置零。

验收标准：

- 与 SOPTX 组装式边界处理结果一致；
- 小算例中不会因边界自由度处理导致 CG 发散。

### T4. 实现 Krylov 求解器接口

第一阶段可先实现无预条件 CG：

```python
class MatrixFreeCGSolver:
    def __init__(self, tol=1e-8, maxiter=500, preconditioner=None):
        self.tol = tol
        self.maxiter = maxiter
        self.preconditioner = preconditioner

    def solve(self, operator, rhs, x0=None):
        ...
```

接口调用：

```python
op.update_density(rho)
u, info = cg_solver.solve(op, force)
```

`info` 至少记录：

- 是否收敛；
- 迭代次数；
- 初始残差；
- 最终残差；
- 总耗时；
- 平均 MatVec 耗时。

验收标准：

- 小型 SPD 线弹性问题中 CG 正常收敛；
- 同一 RHS 下，Matrix-Free CG 解与组装式求解结果误差可控；
- 求解器接口不绑定 SciPy，方便后续多后端迁移。

### T5. 实现基础预条件器

第一阶段可以不做预条件器，但建议预留接口。

最小可行预条件：

```python
class MatrixFreeJacobiPreconditioner:
    def __init__(self, operator):
        self.diag = estimate_diagonal(operator)

    def apply(self, r):
        return r / self.diag
```

后续可扩展：

- 单元对角累加 Jacobi；
- 块 Jacobi；
- 低阶组装代理预条件器；
- 几何多重网格；
- 子结构 Schwarz 预条件。

验收标准：

- 预条件接口与 CG 解耦；
- 可比较无预条件与 Jacobi 预条件的迭代次数。

## 4. SOPTX 拓扑优化流程接入

### T6. 新增分析器选项

在 SOPTX 现有拓扑优化配置中加入：

```text
analysis_type = "assembled" | "matrix_free"
```

原流程：

```python
K = analysis.assemble_stiffness_matrix(rho)
u = solver.solve(K, force)
```

新增流程：

```python
operator.update_density(rho)
u, info = matrix_free_solver.solve(operator, force)
```

验收标准：

- 同一个算例可在组装式分析和 Matrix-Free 分析之间切换；
- 密度更新后不重新组装全局刚度矩阵，只更新 `operator.rho`；
- 目标函数、灵敏度接口保持对上层优化器透明。

### T7. 单步分析闭环

先不跑完整拓扑优化，只固定一组密度 `rho`，完成：

```text
rho -> MatrixFreeOperator -> CG solve -> displacement u -> compliance
```

验收标准：

- 柔顺度与组装式路径结果接近；
- 位移向量相对误差可记录；
- CG 残差曲线可输出。

### T8. 多步优化闭环

在 MBB 梁或悬臂梁小算例中跑若干步优化迭代：

```text
rho_k -> Matrix-Free solve -> compliance/sensitivity -> filter -> OC/MMA -> rho_{k+1}
```

验收标准：

- 前 5-10 步迭代可稳定运行；
- 柔顺度下降趋势合理；
- 与组装式路径的趋势一致。

## 5. 验证与图表任务

### V1. Matrix-Free vs 组装矩阵 MatVec 正确性

测试文件：

```text
soptx/tests/test_matrix_free_vs_assembled.py
```

测试逻辑：

```python
K = assembled_analysis.assemble_stiffness_matrix(rho)
op = MatrixFreeElasticityOperator(...)

x = random_vector()
y_ref = K @ x
y_mf = op.matvec(x)

rel_error = norm(y_ref - y_mf) / norm(y_ref)
assert rel_error < 1e-10
```

输出指标：

| 指标 | 说明 |
|---|---|
| `||Kx||` | 组装矩阵作用结果范数 |
| `||MF(x)||` | Matrix-Free 算子作用结果范数 |
| `rel_error` | 相对误差 |

答辩口径：

> Matrix-Free 改变的是算子实现方式，不改变有限元离散模型；与组装矩阵作用结果保持机器精度一致。

### V2. CG 求解正确性

固定小规模线弹性问题，对比：

```text
组装式 solve(K, f)
Matrix-Free CG solve(op, f)
```

输出指标：

- 位移相对误差；
- 柔顺度相对误差；
- CG 迭代次数；
- 最终残差。

### V3. MatVec 时间与内存估计

benchmark 文件：

```text
soptx/benchmarks/benchmark_matrix_free_elasticity.py
```

记录字段：

```text
ncell
ndof
backend
assembled_matvec_time
matrix_free_matvec_time
assembled_memory_est
matrix_free_memory_est
rel_error
```

第一阶段不必夸大为完整大规模工业验证，只需形成“原型扩展趋势”。

### V4. GPU/多后端验证

若 SOPTX 当前 NumPy / PyTorch / JAX 后端均可运行，优先验证：

- NumPy CPU；
- PyTorch CPU/GPU；
- JAX CPU/GPU。

输出：

- 同一算例不同后端的 `rel_error`；
- 单次 MatVec 时间；
- CG 迭代时间；
- 与已有 SOPTX GPU 加速结果的承接关系。

## 6. 最小可执行顺序

| 阶段 | 任务 | 交付物 | 验收 |
|---|---|---|---|
| 1 | 为现有线弹性积分子补 `action()` | 局部 Matrix-Free kernel | 单元级结果可输出 |
| 2 | 实现 `MatrixFreeElasticityOperator.matvec()` | SOPTX 算子类 | 可对任意向量执行 `y=Kx` |
| 3 | 实现 MatVec 正确性测试 | `test_matrix_free_vs_assembled.py` | `rel_error < 1e-10` |
| 4 | 实现无预条件 CG | `MatrixFreeCGSolver` | 小算例收敛 |
| 5 | 接入单步结构分析 | `rho -> u -> compliance` | 与组装式路径一致 |
| 6 | 接入小规模拓扑优化 | `mbb_matrix_free.py` | 前 5-10 步稳定 |
| 7 | 生成 benchmark 数据 | CSV + 图表 | 可用于答辩 |
| 8 | 扩展 GPU/多后端 | PyTorch/JAX 后端 | 形成异构能力展示 |

## 7. 答辩展示口径

本计划在答辩中的表述应聚焦“可迁移的高性能求解能力”，而不是绑定到某个具体仓库。

推荐表述：

> 由于 SOPTX 中已经实现线弹性积分子、SIMP 材料插值和多后端拓扑优化流程，Matrix-Free 原型不需要大幅修改 FEALPy。后续只需在 SOPTX 中为已有积分子增加局部算子作用接口 `action()`，再封装 `MatrixFreeElasticityOperator.matvec()` 和 Krylov 求解器，即可将原来的“组装矩阵求解”替换为“无矩阵算子作用求解”。这样既保留 FEALPy 作为底层网格与空间支撑，也使 Matrix-Free 高性能模块直接服务 SOPTX，并可进一步迁移到大连理工团队现有 PIML/MMC 与工程软件框架。

建议答辩页展示三项结果：

1. **正确性**：`||Kx - MF(x)|| / ||Kx||` 达机器精度；
2. **GPU/多后端基础**：沿用 SOPTX 已有 CPU/GPU 加速结果；
3. **集成路线**：`已有线弹性积分子 -> action() -> MatrixFreeOperator -> Krylov -> SOPTX 拓扑优化循环`。

底部结论：

> 从“组装式有限元分析”升级为“算子作用式结构分析”，为 PIML 多尺度预测与大规模拓扑优化高性能求解提供可落地的软件入口。
