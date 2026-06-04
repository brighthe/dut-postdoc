# dut-postdoc

大连理工大学博士后期间的研究论文阅读笔记与调研记录。

## 仓库用途

本仓库用于管理博士后研究阶段的知识积累，包含：

- **文献阅读笔记**（`literature/`）：针对单篇论文的精读笔记，涵盖拓扑优化、有限元方法等方向
- **研究调研**（`research/`）：面向课题/研究方向的综合调研与分析
- **论文草稿**（`papers/`）：自主撰写的论文草稿与写作过程记录
- **共用资源**（`assets/`）：统一的参考文献库（`refs.bib`）与笔记模板

## 目录结构

```
dut-postdoc/
├── literature/          # 文献阅读笔记（单篇论文级别）
│   ├── topology-opt/    # 拓扑优化
│   ├── fem/             # 有限元方法
│   └── others/
├── research/            # 研究调研（课题/方向级别）
├── papers/              # 自己写的论文草稿
└── assets/
    ├── refs.bib         # 共用参考文献库
    └── templates/       # 笔记模板
```

## 使用说明

- 新建文献笔记时，复制 `assets/templates/literature-note.md` 并放入对应子目录
- 新建调研笔记时，复制 `assets/templates/research-survey.md`
- 所有 PDF 原文请本地存放，不纳入版本控制（见 `.gitignore`）
- 参考文献统一维护在 `assets/refs.bib`

## 研究方向

- 拓扑优化（Topology Optimization）
- 有限元方法（Finite Element Method）

---

*大连理工大学 · 博士后研究*
