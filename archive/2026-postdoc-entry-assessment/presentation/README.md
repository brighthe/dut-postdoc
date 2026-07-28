---
title: "2026 入站考核 · 科研工作汇报（Beamer 幻灯片）"
tags:
  - archive
  - defense
  - beamer
status: "archived"
event_date: 2026-07-05
date_archived: 2026-07-26
---

# 2026 入站考核 · 科研工作汇报（Beamer 幻灯片）

> 本目录是 2026 年 7 月 5 日博士后入站考核的最终演示档案，已从原 `talks/2026-postdoc-entry-assessment/` 归档。下列安排与材料状态按答辩完成时的历史语境保留，不再作为当前入站流程事实源。

## 考核记录

- **场景**：大连理工大学力学与航空航天学院博士后进站集中考核。
- **时间**：2026 年 7 月 5 日。
- **汇报要求**：个人汇报 PPT，时长约 8 分钟。
- **最终状态**：入站考核已完成；后续入站手续不在本档案维护。

## 文件说明

| 文件/目录 | 说明 |
|-----------|------|
| `template-8min.tex` | 8 分钟进站考核汇报版正式主文件（精简至13内容帧） |
| `template-8min.pdf` | 受 Git 跟踪的答辩定稿 PDF |
| `outline-8min.md` | 8 分钟版本的结构大纲与排版设计记录 |
| `script-8min.md` | 8 分钟版本的配套逐字口语讲稿 |
| `pptheader.tex` | 导言区：宏包、主题、样式 |
| `mycommand.tex` | 自定义命令 |
| `figures/` | 插图（矢量 PDF） |
| `photo.jpg` | 封面照片素材 |

## 如何编译

用 **XeLaTeX**（支持中文）编译，编译**两次**以生成目录：

- **TeXstudio**：打开 `template-8min.tex`，默认编译器选 XeLaTeX，点编译即可（按两次或用"构建并查看"）。
- **命令行**：`xelatex template-8min.tex` 执行两遍。

## 注意

编译产生的中间文件（`*.aux` / `*.log` / `*.nav` / `*.snm` / `*.toc` /
`*.synctex.gz` 等）由仓库根目录 `.gitignore` 忽略；定稿
`template-8min.pdf` 与 `figures/` 下的图件正常受 Git 跟踪。

本目录已归档，不再主动重新编译或覆盖定稿 PDF。若需要复用版式，应复制到
`talks/` 下的新报告目录后再修改。
