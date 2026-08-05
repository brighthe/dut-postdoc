---
title: "FEALPy 4.0 API 迁移笔记"
type: concept
aliases: [FEALPy 4.0.0 迁移, fealpy_stable, FEALPy API 差异]
tags: [FEALPy, 混合有限元, 迁移, 踩坑]
status: "done"
date_added: 2026-08-05
date_update: 2026-08-05
---

# FEALPy 4.0 API 迁移笔记

> **一句话**：从 FEALPy 3.4.0（fealpy_heliang）迁移到 4.0.0（fealpy_stable）时验证过的 API 行为差异，直接导致 Hu–Zhang 混合有限元求解链不收敛/崩溃；每条都经过数值验证并有修复对照。

## 定义

`dut-postdoc` 的研究代码（`soptx`，WSL compute tier）从旧版 FEALPy 迁移到 4.0.0 时，若干 API 的**行为语义**变化（而非单纯改名）会静默破坏数值结果。本页记录已确认的差异、表现与修复方式，供后续迁移或排错直接引用。

## 关键要点

1. **`grad_shape_function` 默认返回参考坐标导数，非物理梯度**（最重要）
   - 2D 下默认输出 = 物理梯度的一半（参考坐标 x̂=λ1, ŷ=λ2 的导数）；必须带 `variables='x'` 才返回笛卡尔物理梯度 `(NC, NQ, LDOF, GD)`。
   - 表现：`div_basis` 的散度错 2 倍 → σ/位移不收敛（σ L2 停滞 O(1)），且只在**非对称单元**上暴露（对称单元巧合正确，FD 验证通过但换网格就失败）。
   - 修复：2D 与 3D 统一调用 `grad_shape_function(bc, p, variables='x')`。
   - 教训：**有限差分验证必须在多种网格（含非对称）上做**；单个单元通过不保证正确。

2. **`spsolve` 经 `to_scipy()` 共享内存视图传给 scipy SuperLU，会原地修改矩阵**
   - `CSRTensor.to_scipy()` 用 `bm.to_numpy(values)`（numpy 后端是视图），scipy `spsolve` 的 SuperLU 分解会原地改动矩阵（列置换/缩放）。
   - 表现：求解后缓存的 K 被破坏——对称性断言失败（如 1.39 而非 1e-19）、伴随求解复用错误矩阵。
   - 修复：缓存用 `K.copy()`（`CSRTensor.copy()`），spsolve 传入的原对象可被破坏无妨。

3. **`bc_to_point` 返回 `(NC, NQ, GD)` 带单元维**
   - 旧的 `bc_to_point(bc)[0]` 取的是**第一个单元**的点，不是"第一个点"；按单元取需 `bc_to_point(bc, index=[c])`（返回 `(NC, NQ, GD)` 直接使用，不再 `[0]`）。
   - 表现：诊断/组装脚本在非 0 号单元上静默取错点（插值恢复错误、RHS 近乎为零）。

4. **`cell_to_face_sign` → 2D 改名 `cell_to_edge_sign`**
   - 2D 下 face 即 edge；按 `mesh.top_dimension()` 分派，3D 仍用 `cell_to_face_sign`。

5. **`bmat` 的 hstack/vstack 分支会丢块**（blocks 全非 None 时）
   - 表现：`bmat([[A, B], [B.T, -J]])` 的 `-J` 块整体丢失 → K 秩亏（rank 96/135）、SuperLU 分解失败（DGEMV 参数非法）。
   - 修复：改用 `scipy.sparse.bmat`（显式零块）构造后 `CSRTensor.from_scipy` 转回。含 `None` 块的调用（COO 合并分支）不受影响。

6. **`mesh.edgedata` 用户数据字典已移除**
   - 边界标记改由分析器持有（`soptx` 的 `_essential_bc` / `_natural_bc`），测试与旧代码需相应适配。

7. **角点松弛仅支持 2D**
   - `_get_corner_data` 要求 checkerboard 拓扑（每个几何角点恰好 2 个 incident 三角形、共享一条内部边）；3D 无对应实现。无松弛的 3D Hu–Zhang 求解路径存在（`huzhang_fe_space_3d.py`，`variables='x'` 已正确）。

## 与相关概念的关系

- **上位/下位**：[[matrix-free/_index|Matrix-Free]] 与 [[gpu-hpc/_index|GPU/HPC]] 技术线的实现层依赖
- **对比/区分**：与 [[linear-elasticity]] 的关系——位移型线弹性的 Lagrange 离散无此问题；混合元（Hu–Zhang）因涉及散度/梯度/迹而全链路暴露

## 来源与证据

- soptx 仓库修复提交：`fa73d4d`（主修复）、`c4a2d37`（div_basis 简化）——每条差异都经 FD 验证、收敛对照（旧仓库 fealpy 3.4.0 收敛 vs 新版发散）与 pytest 回归
- 旧仓库对比实验：`soptx_heliang` + `fealpy_heliang`（3.4.0）同流程收敛，锁定差异在 FEALPy API 层

## 在我研究中的位置

- 维护 `soptx` Hu–Zhang 混合有限元求解链的直接排错手册；博士论文第五章（任意次 Hu–Zhang 拓扑优化）的 2D 算例链已全部恢复收敛
- 后续任何 FEALPy 相关代码迁移/升级，先对照本页清单

## 开放问题

1. `variables='x'` 是 4.0.0 的显式开关还是默认行为仍会变（跟踪上游）？
2. jump-penalty 的 `0.01·模量/hF` 缩放系数是数值标定的，理论核查待办（degree 2 收敛阶 σ 2.4 阶 vs 理论 3 阶）

## 相关页面

- [[matrix-free/_index|Matrix-Free 主题入口]]
- [[linear-elasticity]]
- [[gpu-hpc/_index|GPU/HPC 主题入口]]
