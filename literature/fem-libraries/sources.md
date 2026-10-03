---
title: "有限元框架源码仓库登记表"
tags:
  - fem-libraries
  - source-archive
  - MFEM
  - libCEED
  - FEniCS
status: "active"
date_added: 2026-09-05
date_update: 2026-10-03
---

# 有限元框架源码仓库登记表

wiki 页面中的逻辑标识 `<仓库名>:<仓库内相对路径>`（如 `mfem:fem/bilinearform.hpp`）由本表解析。源码属原始源层，人拥有、AI 只读；本地副本放 WSL 代码根，不复制进本仓库，规则见 [[../../schema/page-schemas#存储与来源|存储与来源]]。论文 PDF 不在本表登记。

| 逻辑名        | 内容                                                             | upstream                                | 本地副本                                |
| ---------- | -------------------------------------------------------------- | --------------------------------------- | ----------------------------------- |
| `mfem`     | 库源码、examples/miniapps、Doxygen 注释                               | `https://github.com/mfem/mfem.git`      | `Ubuntu-24.04:~/codespace/mfem`     |
| `mfem-web` | mfem.org 站点源（MkDocs），用户文档、howto、performance 等页                 | `https://github.com/mfem/web.git`       | `Ubuntu-24.04:~/codespace/mfem-web` |
| `libceed`  | 库源码、examples，用户手册在 `doc/sphinx/`                               | `https://github.com/CEED/libCEED.git`   | `Ubuntu-24.04:~/codespace/libceed`  |
| `dolfinx`  | 库源码（网格核心 `cpp/dolfinx/mesh/`）、`python/demo`，C++ 文档在 `cpp/doc/` | `https://github.com/FEniCS/dolfinx.git` | `Ubuntu-24.04:~/codespace/dolfinx`  |


