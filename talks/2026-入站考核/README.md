# 2026 入站考核 · 科研工作汇报（Beamer 幻灯片）

## 文件说明

| 文件/目录 | 说明 |
|-----------|------|
| `template.tex` | 主文件，幻灯片内容 |
| `pptheader.tex` | 导言区：宏包、主题、样式 |
| `mycommand.tex` | 自定义命令 |
| `figures/` | 插图（矢量 PDF） |
| `logo.png` / `logo.pdf` / `photo.jpg` | 封面/页眉素材 |

## 如何编译

用 **XeLaTeX**（支持中文）编译，编译**两次**以生成目录：

- **TeXstudio**：默认编译器选 XeLaTeX，点编译即可（按两次或用"构建并查看"）
- **命令行**：`xelatex template.tex` 执行两遍

## 注意

编译产生的中间文件（`*.aux` / `*.log` / `*.nav` / `*.snm` / `*.toc` /
`*.synctex.gz` 等）和成品 `template.pdf` 都已被仓库根目录 `.gitignore` 忽略，
直接在本目录编译即可，不会污染版本控制。`figures/` 下的矢量图与
`logo.pdf` 正常跟踪。
