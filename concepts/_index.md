# 概念页总索引

> 跨多个来源提炼的稳定概念。简单概念使用单页；复杂主题使用带语义 `_index.md` 的子目录，其入口只负责跨目录导航、页面职责和事实所有权说明。简单概念模板：[[../assets/templates/concept-note]]；复杂主题入口模板：[[../assets/templates/topic-index]]。

| 概念 | 别名 | 一句话 | 状态 |
|---|---|---|---|
| [[llm-wiki]] | LLM Wiki / 个人 AI 知识库 | 把 LLM 放在原始资料与研究者之间，持续维护可追溯、互链的 Markdown wiki | done |
| [[machine-learning]] | Machine Learning / 机器学习分类框架 | 以模型族与架构、学习对象、训练范式和任务目标四个正交维度定位机器学习方法 | in-progress |
| [[pca-pod]] | PCA / POD / 主成分分析 / 本征正交分解 | 用特征基与低维系数表示、重构和截断高维快照 | in-progress |
| [[linear-elasticity]] | Linear Elasticity / 位移型线弹性 | 小变形静力各向同性线弹性的强形式、弱形式与 Lagrange 有限元离散 | in-progress |
| [[mmc/_index\|MMC]] | Moving Morphable Components / 移动可变形组件 | 以显式组件参数、拓扑描述函数和优化闭环表示结构拓扑 | in-progress |
| [[piml/_index\|PIML]] | Problem-Independent Machine Learning / 问题无关机器学习 | 维护项目 PIML 的正式释义，并连接 Physics-Informed ML 等外部方法背景 | in-progress |
| [[matrix-free/_index\|Matrix-Free]] | Matrix-Free Assembly Levels / 矩阵无关有限元 | 统一装配层次、方法谱系与当前技术路线 | draft |
| [[gpu-hpc/_index\|GPU/HPC]] | GPU / High-Performance Computing / 异构高性能计算 | 统一端到端性能模型、公开成果谱系与当前异构并行技术路线 | in-progress |
| [[fealpy4-api-notes]] | FEALPy 4.0 API 迁移笔记 / fealpy_stable | 从 FEALPy 3.4 迁移到 4.0 时验证过的 API 行为差异与修复对照（直接影响混合有限元求解链） | done |

---

*新建简单概念页时复制 [[../assets/templates/concept-note]]；复杂主题形成多个稳定页面后复制 [[../assets/templates/topic-index]] 建立语义 `_index.md`，删除没有实际内容的可选章节，并在本表和 [[../index]] 登记主题入口。*
