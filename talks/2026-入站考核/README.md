# 2026 入站考核 · 科研工作汇报（Beamer 幻灯片）

## 文件说明

| 文件/目录 | 说明 |
|-----------|------|
| `template.tex` | 主文件，幻灯片内容 |
| `pptheader.tex` | 导言区：宏包、主题、样式 |
| `mycommand.tex` | 自定义命令 |
| `latexmkrc` | 编译配置（XeLaTeX，产物输出到 `build/`） |
| `figures/` | 插图（矢量 PDF） |
| `logo.png` / `logo.pdf` / `photo.jpg` | 封面/页眉素材 |
| `build/` | 编译产物输出目录（已被 `.gitignore` 忽略） |

## 如何编译（推荐：命令行，跨设备通用）

进入本目录，执行：

```bash
latexmk
```

`latexmk` 会自动读取 `latexmkrc`，用 XeLaTeX 编译、自动判断编译遍数，
所有产物（含最终 `template.pdf`）输出到 `build/`，源目录保持干净。

- **WSL / Linux / macOS**：直接 `latexmk`
- **Windows 上从外部调用 WSL 内的 latexmk**：`wsl latexmk`
- 清理产物：`latexmk -C`

成品 PDF 位于 `build/template.pdf`。

## 在 TeXstudio 中编译（每台设备一次性设置）

> 仓库无法保存 TeXstudio 的全局配置，换设备需按此设置一次。
> 若 LaTeX 装在 WSL 里，命令需加 `wsl` 前缀。

1. **选项 → 设置 TeXstudio → 命令**，把 **Latexmk** 一行改为：
   ```
   wsl latexmk -silent %.tex
   ```
   （引擎与输出目录由本目录的 `latexmkrc` 接管，无需在此指定）

2. **构建** 页 → **默认编译器** 选 `Latexmk`。

3. **构建** 页 → **PDF 附加搜索路径（PDF Paths）** 填 `build`，
   这样内置预览器能在 `build/` 里找到 `template.pdf`。

设置完成后，绿色编译按钮即走 latexmk，产物进 `build/`，源目录不再产生中间文件。

## 注意

- `build/` 整个目录及顶层 `template.pdf` 已被仓库根目录 `.gitignore` 忽略，
  不会进入版本控制；`figures/` 下的矢量图与 `logo.pdf` 正常跟踪。
- 编译时若出现 `Annotation out of page boundary` 警告，是页脚导航按钮
  超出页边所致，不影响内容，可忽略。
