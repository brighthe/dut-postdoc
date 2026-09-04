#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成《中国博士后科学基金第 80 批面上资助申请书》第 6 部分"研究基础"配图。

    输出:
        assets/fig08_matrix_free_validation.png   图 8 Matrix-Free 求解验证
        assets/fig09_piml_validation.png          图 9 PIML 局部表示验证
        assets/fig10_multibackend_performance.png 图 10 FEALPy 多后端性能

一张图对应正文"一、"中的一点，编号与储备一一对应，图注里不再需要"对应第 1、3 点"
这类跨图索引。也因此每张图内部只用 (a)(b)(c)(d) 单字母编号，原先用来区分储备的
a*/b*/c* 前缀已无信息量，全部去掉；图 4 只有一个面板，不加面板编号。

    图 2  储备一  Matrix-Free 算子 / Krylov 求解  —— 四格全部实测
          (a) 2D/3D 相对 L2 误差收敛阶（显式组装与 matrix-free 同一离散）—— 对不对
          (b) 两路进程峰值 RSS 随自由度增长, 与本机可用内存上限        —— 能算多大
          (c) 同一 matrix-free 算子 CPU 与单块 GPU 单次求解耗时对照     —— 能不能更快

    图 3  储备二  PIML 局部力学表示与精确缩聚验证  —— 三格全部实测
          (a) 缩聚解与全装配直解的相对差, 对照验收阈值                —— 真值对不对
          (b) 形函数误差经式 (17) 的二阶压缩, 与直接预测缩聚刚度对照  —— 代理准不准
          (c) 观测刚化中来自刚体零空间伪刚度的份额, 参数化改造前后    —— 靠什么保证

    图 4  储备三  基于 FEALPy 的拓扑优化平台与多后端计算 —— 全部实测
          (a) 160.4 万自由度单步迭代总耗时 CPU(稀疏) vs GPU(张量化)
          (b) 四个核心计算阶段加速比拆解
          (c) 同一算例最终优化构型渲染

三张图共用同一源图宽（FIG_WIDTH_IN），因此在 DOCX 里缩放比相同、印刷字号一致。
插图按 15.2 cm 宽插入（见 build_grant_docx.py），纸面物理尺寸与源图宽无关，
源图越窄同一 pt 值的字在纸面上越大——所以宽度是个字号旋钮，不是尺寸旋钮。

##############################################################################
#  数据来源声明                                                               #
#                                                                            #
#  * 图 2 四格 **全部为实测数据**，全部读自 soptx 的入库快照                    #
#      experiments/matrix_free_capability/figure_data/fig2_data.json          #
#    （常量 FIG2_SNAPSHOT，路径可用环境变量 SOPTX_ROOT 覆盖）。本文件内         #
#    **不再手抄任何误差值**：快照由该目录的 run.py 采集，自带 provenance        #
#    与门禁，逐档数值同时渲染进它的 results_analysis.md。                       #
#    上游产物仍是那三处，但已由 cases.toml 固定参数、由 run.py 调度：           #
#      manufactured_convergence_{2d_tri_sinusoidal,3d_tet_divfree-poly}_p1_*.json #
#      stage1-validation-all.json ／ peak_rss_3d_tet_*.json                    #
#      device_speedup_3d_tet_polynomial_p1_ea_fast_n{8,16,32,64}.json          #
#    仍未解决的是**溯源**：上游 JSON 里没有 git 字段（validate.py 不写          #
#    environment 块，benchmark_cpu_ea.py 连时间戳都不写），快照只能记下采集时   #
#    的 revision 与 dirty 标志。当前快照 reproducible=False（工作区 dirty），   #
#    **正式投递前须在 clean revision 上重跑固化**。                             #
#  * 图 3 三格 **全部为实测**，出处见各 data_* 的 docstring：                    #
#      examples/substructure_elasticity/outputs/lagrange_comparison_{2d,3d}.json #
#      examples/piml_substructure_elasticity/outputs/eq17_second_order.json    #
#      examples/piml_substructure_elasticity/outputs/piml_exact_comparison.json #
#    因此图 3 **不画水印**，改用 footnote() 给数据出处。                        #
#  * 图 4 已于 2026-08-27 全部转真实实测（soptx ``topopt_3d_simp_real.py``
#    真实 Hex8 刚度 + 矩阵自由 PCG + SIMP/OC）。2026-08-28 换用博士论文算例 3.3
#    的加密版（60x20x4 mm 悬臂梁，300x100x20 网格，191.5 万自由度 90 步收敛），
#    四个面板统一到同一算例；CPU/GPU 两侧同为 float64，构成对等对比。面板
#    (c)(d) 为真实构型渲染，见 FIG4_PANEL_C_IMG 常量注释）。watermark() 与 PLACEHOLDER
#    保留为能力（仅当未来某格数据回退为占位时用），当前全图无占位。
#    图 2 的 GPU 加速那一格曾是占位、水印只打在该格轴内；2026-08-22 注册        #
#    c-dev-n* 四个 case 并测出实测值后，该格的水印已删。watermark(..., ax=...)  #
#    的单格打标能力保留，下一次出现"整图里只有一格是占位"时仍然用得上。        #
#    2026-08-24 换版式：(c) 改为 MPI 进程级强扩展，GPU 加速移到 (d)，原 (d) 的  #
#    有效访存带宽不再单占一格、只进 (d) 的角注。切图文件名按**图面位置**命名，  #
#    故 panel_c/panel_d 两张图的内容在这次改动里互换了主题。                    #
#  * 图 4 除合并图外还输出四张单格切图                                  #
#    fig08_matrix_free_validation_panel_{a,b,c,d}.png，                    #
#    供 soptx 的 experiments/matrix_free_capability/results_analysis.md 按图面   #
#    分格引用。与合并图共用 draw_panel_* 绘图函数、只换画布，不会漂移；单格图    #
#    另给 4.6 in 宽，(a) 的刻度标签才排得开。不进 DOCX，不占插图预算。          #
##############################################################################
#  图 3 为什么不再画"密度 / 参考解 / 恢复解 / 误差"四格云图                      #
#                                                                            #
#  旧版四格是合成的: 生成脚本                                                  #
#  soptx/examples/piml_substructure_elasticity/plot_local_recovery.py 在      #
#  精确 N 上叠加 gaussian_filter 平滑噪声当作网络预测, 图面上"界面附近误差偏大" #
#  的结构是造出来的, 不是测出来的; 报出的 1.90% / 0.45% 同样如此。             #
#  即便换成实测, 单个子结构的云图也只能回答"这一个子结构像不像", 回答不了      #
#  "两条候选路线该选哪条""局部误差会不会在装配后被放大"这两个真问题——          #
#  而后者才是研究内容 1、3 的立项依据。                                        #
#  纸面高度同时由 14.0 cm 降到 5.2 cm, 与图 2 (5.1) 、图 4 (5.3) 齐平。         #
##############################################################################
#  图 2 为什么不画"内存墙"与"装配整段消失"                                      #
#                                                                            #
#  更早的版本 (b) 画 Matrix-Free 0.043 GB / 1M 自由度、CSR 撞 128 GB 内存墙；    #
#  (c) 画"装配整段消失、净加速 1.4 倍"。实测把这两条都推翻了:                    #
#    * storage_ratio_fa_over_ea = 1.027 / 1.013 / 1.007 —— EA 只比 FA 省       #
#      1~3%; 且该数字只统计算子长期保存数组, 本就不是进程峰值内存;              #
#    * EA 仍有构造段(缓存 K_e), 只比 FA 快 27%; EA 的 CG 总时间 1.160 s         #
#      对 FA 0.591 s, 慢约 2 倍——端到端 EA 更慢;                              #
#    * GPU 路径(阶段 1c)未开始, 任何 "GPU Matrix-Free" 曲线都无证据。           #
#  因此: 不写内存墙与端到端加速的结论, 改画"对不对 / 能算多大 / 能不能更快"。   #
#  (c) 早先画的是多卡瓶颈分解, 已改为单卡对 CPU 的耗时对照: 前者暗示多卡        #
#  强扩展结果已有, 而那是研究内容 2 的题目, 不是研究基础。                      #
##############################################################################
#  图面为什么统称 matrix-free, 不标 EA / PA / UA                               #
#                                                                            #
#  存储层级的细分(EA 缓存单元阵 / PA 只存积分点因子 / UA 全部现算)是            #
#  研究内容 2 要研究的题目, 不是研究基础要展示的对象。研究基础只需回答          #
#  "同一块卡上能算多大", 一个对比就够; 在 5 cm 高的插图里摆一套三层             #
#  分类法, 只会花掉正文本就紧张的 1000 字去解释术语。                          #
#                                                                            #
#  但这个区别在核验边界(申请书草稿"三、")里必须留着, 原因只有一个:             #
#  soptx 现在保存的是单元刚度阵(README: 不实现 PA/QA、UA/NONE),                 #
#  约 1.5 GB / 1M 自由度, **比 CSR 还费**。(b) 里那条 matrix-free 线画的是      #
#  只存积分点因子的目标形态, 现在测不出来; 要让它有数据, 得先补一条那样的       #
#  算子路径 —— 那条路径同时就是研究内容 2 的可行性证据。                        #
##############################################################################
"""

import json
import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D
from matplotlib.ticker import LogLocator, NullFormatter, NullLocator, ScalarFormatter
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

# 置为 False 即去掉"占位"水印与脚注（数据全部换成实测后再改）
PLACEHOLDER = True

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HERE = os.path.join(os.path.dirname(SCRIPT_DIR), "assets")
OUT_FIG2 = os.path.join(HERE, "fig08_matrix_free_validation.png")
# 矢量版: Markdown 里引的是它。DOCX 仍插 PNG —— python-docx 的 add_picture
# 只认位图, 喂 SVG 会抛 UnrecognizedImageError, 故 build_grant_docx.py 在
# 解析图片路径时把 .svg 换回同名 .png。
OUT_FIG2_SVG = os.path.join(HERE, "fig08_matrix_free_validation.svg")
# 图 2 的单格切图。合并图进申请书, 单格图供 soptx 的按图面分格文档引用
# (合并图 2394 px 宽, 按文档宽渲染时单格只剩约 296 px, 刻度读不了)。
OUT_FIG2_PANEL = os.path.join(HERE, "fig08_matrix_free_validation_panel_{}.png")
OUT_FIG2_PANEL_SVG = os.path.join(HERE, "fig08_matrix_free_validation_panel_{}.svg")
OUT_FIG2_INTERNAL = os.path.join(
    HERE, "dev", "fig08_matrix_free_validation_panel_c_internal.png")
OUT_FIG2_INTERNAL_SVG = os.path.join(
    HERE, "dev", "fig08_matrix_free_validation_panel_c_internal.svg")
# 单格图自己的画布: 不是从合并图上切下来的, 所以不必继承三等分的窄格子。
# 4.6 in 宽让 (a) 的五个 "1/N" 刻度标签排得开(合并图里每格只有约 2.9 in)。
FIG2_PANEL_SIZE = (4.6, 3.5)
# 图 2 的数据快照。由 SOPTX 的 experiments/matrix_free_capability/run.py 采集,
# 是 (a)(b) 全部数字的唯一出处 —— 本文件不再手抄任何误差值。手抄过一次就会过期:
# 重跑后 3D 误差链的末位从 ...264198 变成 ...264197, 这类漂移肉眼查不出来。
# 路径可用环境变量 SOPTX_ROOT 覆盖(本仓库与 soptx 不在同一棵树下)。
SOPTX_ROOT = os.environ.get("SOPTX_ROOT", os.path.expanduser("~/workspace/soptx"))
FIG2_SNAPSHOT = os.path.join(
    SOPTX_ROOT, "experiments", "matrix_free_capability", "figure_data", "fig2_data.json")

OUT_FIG3 = os.path.join(HERE, "fig09_piml_validation.png")
OUT_FIG3_SVG = os.path.join(HERE, "fig09_piml_validation.svg")
OUT_FIG3_PANEL = os.path.join(HERE, "fig09_piml_validation_panel_{}.png")
OUT_FIG3_PANEL_SVG = os.path.join(HERE, "fig09_piml_validation_panel_{}.svg")
FIG3_PANEL_SIZE = (4.6, 3.5)
FIG3_SNAPSHOT = os.path.join(
    SOPTX_ROOT, "experiments", "piml_capability", "figure_data", "fig3_data.json")

OUT_FIG4 = os.path.join(HERE, "fig10_multibackend_performance.png")
OUT_FIG4_SVG = os.path.join(HERE, "fig10_multibackend_performance.svg")
# 面板 (c)/(d) 的外部底图: 同一 191.5 万自由度 SIMP 算例的初始构型与优化后构型
# (soptx/examples/topopt_platform/render_topology.py 以 --pair 一次出两张, 共用相机
# 与裁剪框, 保证等尺寸、可并排对齐)。两张均按 11.52x4.90 in 渲染: 底图里 "固支端"/"F"
# 的字号是绝对磅值, 底图幅面必须与最终显示宽度 (3.858 in, 见 build_fig4 的版式注释)
# 成比例, 否则标注相对结构会偏大或偏小。改版式必须同步重渲染底图。
FIG4_PANEL_C_IMG = os.path.join(HERE, "dev", "fig10_panel_c_initial_render.png")
FIG4_PANEL_D_IMG = os.path.join(HERE, "dev", "fig10_panel_d_topology_render.png")
FIG4_SNAPSHOT = os.path.join(
    SOPTX_ROOT, "experiments", "topopt_capability", "figure_data", "fig4_data.json")

# 插图在 DOCX 中的宽度（build_grant_docx.py 里写死 15.2 cm），用于反推印刷字号。
# 三张图共用同一源图宽 => 缩放比相同 => 印刷字号一致。纸面高度由各自的
# figsize 高宽比决定, 与这个值无关, 所以统一宽度不会把图 3 压扁。
DOCX_WIDTH_IN = 15.2 / 2.54
FIG_WIDTH_IN = 8.0

# 图 2(d) 用。EA 层级每个单元缓存一个 12x12 的 float64 单元刚度阵(3D 四面体 P1
# 矢量弹性: 4 节点 x 3 分量 = 12 个自由度), 每次 CG 迭代把这批数整体流过一遍 ——
# 这是算子作用绕不开的访存量, 也是"有效访存带宽"的分子。
EA_BYTES_PER_CELL = 12 * 12 * 8
# RTX 5080 的厂商标称显存带宽(GDDR7, 256-bit)。**这不是实测值**, 是 2026-08-22
# 经用户确认后写入的规格数, 只用于换算"达标称的百分之多少"。
# 2026-08-24 该结论两次撤退: 先不进任何图面, 同日又从申请书正文撤下(研究基础第 1
# 条已经太满, 且"43%"是诊断不是成绩)。现在申请书全篇不出现 43%, 唯一事实源是 soptx
# 的 results_analysis.md §5.4 / 表 c-2。换机器时改这里和那份文档即可, 申请书不必动。
GPU_SPEC_BANDWIDTH_GB_S = 960.0

# --------------------------------------------------------------------------
# 中文字体：按优先级探测，找不到就退回 matplotlib 默认（中文会变方块，会给出警告）
# (常规字重, 粗体字重) —— 成对注册, 否则 fontweight="bold" 会静默退回常规
# --------------------------------------------------------------------------
FONT_CANDIDATES = [
    ("/mnt/c/Windows/Fonts/msyh.ttc", "/mnt/c/Windows/Fonts/msyhbd.ttc"),   # 微软雅黑
    ("/mnt/c/Windows/Fonts/simhei.ttf", None),                              # 黑体(无粗体)
    ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
     "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
    ("/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf", None),
    ("/System/Library/Fonts/PingFang.ttc", None),                           # macOS
]


def setup_font():
    # mathtext 走 DejaVu, 与中文字体解耦: 中文字体普遍缺 U+2212, 否则 10^{-2} 会渲染成乱码
    plt.rcParams["mathtext.fontset"] = "dejavusans"

    for regular, bold in FONT_CANDIDATES:
        if not os.path.exists(regular):
            continue
        try:
            fm.fontManager.addfont(regular)
            name = fm.FontProperties(fname=regular).get_name()
        except Exception:
            continue
        if bold and os.path.exists(bold):
            try:
                fm.fontManager.addfont(bold)
            except Exception:
                pass
        plt.rcParams["font.sans-serif"] = [name, "DejaVu Sans"]
        plt.rcParams["font.family"] = "sans-serif"
        print(f"[font] 使用中文字体: {name}  ({regular})")
        return name
    print("[font] 警告: 未找到中文字体, 中文将显示为方块")
    return None


# --------------------------------------------------------------------------
# 配色（2026-08-27 按刘畅意见改灰度印刷风：系列靠明度+线型/标记区分，
# 变量名保留原色相语义以免全文重命名；单一浅色模式，面向印刷）
# --------------------------------------------------------------------------
SURFACE = "#ffffff"
INK = "#0b0b0b"        # 主文字
INK_2 = "#52514e"      # 次文字 / 轴
GRID = "#dcdbd6"
C_BLUE = "#1a1a1a"     # 主系列：近黑（原亮蓝）
C_ORANGE = "#6e6e6e"   # 次系列：中灰（原亮橙；配合虚线+方点）
C_AQUA = "#b3b3b3"     # 第三系列：浅灰（原绿；仅图 6 用到）
C_GREEN = "#3d3d3d"
C_GREEN_L = "#e8e8e8"
# 同阶浅档: 图 2(c) 的堆叠段。段内用明度区分"装配/求解",
# 主系列 近黑/中浅灰, 次系列 中灰/极浅灰, 四档明度依次拉开。
C_BLUE_L = "#b3b3b3"
C_ORANGE_L = "#e0e0e0"

# 字号按 DOCX 缩放比反推：source_pt * (15.2cm / FIG_WIDTH) >= 7 pt
plt.rcParams.update({
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    # SVG 里的字一律转路径: 消费端(Obsidian/浏览器/Word)未必装了这里探测到的
    # 中文字体, 留 <text> 会在别人机器上掉字。
    "svg.fonttype": "path",
    "axes.edgecolor": INK_2,
    "axes.linewidth": 1.0,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": INK_2,
    "ytick.color": INK_2,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "axes.labelsize": 12.5,
    "axes.titlesize": 13,
    "legend.fontsize": 11.5,
    "axes.unicode_minus": False,
    "grid.color": GRID,
    "grid.linewidth": 0.7,
})


def safe_savefig(fig, path, **kwargs):
    import tempfile, shutil
    ext = os.path.splitext(path)[1]
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tf:
        tmp_name = tf.name
    try:
        fig.savefig(tmp_name, **kwargs)
        shutil.move(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            try:
                os.remove(tmp_name)
            except Exception:
                pass


def report_print_sizes(name, fig_width_in):
    scale = DOCX_WIDTH_IN / fig_width_in
    print(f"[scale] {name} 图宽 {fig_width_in}in -> DOCX {DOCX_WIDTH_IN:.2f}in, "
          f"缩放比 {scale:.2f}")
    for key in ("xtick.labelsize", "axes.labelsize", "axes.titlesize", "legend.fontsize"):
        eff = plt.rcParams[key] * scale
        flag = "OK" if eff >= 6.0 else "过小"
        print(f"[scale]   {key:20s} {plt.rcParams[key]:5.1f}pt -> {eff:4.1f}pt  {flag}")


# 图 9 上排每格约 3.0 in (DOCX 版心 5.98 in 二等分), 全局 ``axes.labelsize`` 12.5 pt
# 的轴标签会占掉过多净宽; 9.6 pt 缩到 DOCX 幅面仍有 7.2 pt, 高于 report_print_sizes
# 的 6 pt 门槛。
FIG3_LABEL_FS = 9.6


def p3_title(label, text):
    """图 9 的面板标题：``label`` 为 ``None`` 时不加序号。

    同一批 ``draw_panel_3*`` 既拼进图 9, 又各自出一张独立分图供证据文档引用。
    合图里的序号由 :func:`build_fig3` 现场指定 (缩聚正确性那格出图后, 原 (b)(c)(d)
    依次变成 (a)(b)(c)), 独立分图则是孤零零一格、序号无所指, 故传 ``None`` 去掉。
    """
    return f"({label}) {text}" if label else text


def panel_title(ax, text):
    """统一的面板标题：左对齐、加粗、贴在轴框上方。"""
    ax.set_title(text, loc="left", fontweight="bold", color=INK, pad=7)


def center_titles_on_blocks(fig, axes):
    """把面板标题改为居中于各面板的**可见块**（轴框 + 刻度标签 + 轴标签）。

    ``set_title`` 的 x 锚在轴框上。图 10 上排 (a)(b) 的轴框被 y 刻度标签往右推了
    约 1.4 in，下排 (c)(d) 是关掉坐标轴的构型底图、轴框贴着画布边缘 —— 同一句
    ``loc="left"`` 下两排标题的左边界差出 1.3 in，看着参差。锚到可见块后四个标题
    的中心线对齐（两排残差约 0.13 in，来自 (a)(b) 左侧刻度标签与 (c)(d) 无标签的
    块宽差异）。

    量块宽时必须先把标题清空：``get_tightbbox`` 含标题，不清空则块宽被标题自身
    撑开、越长的标题偏移越大；清空也顺带清掉 ``panel_title`` 写下的 ``loc="left"``
    标题（三个 loc 各是独立的 Text 对象，不清则两个标题同时显示）。量完还要冻结
    布局 —— constrained_layout 在 savefig 时会再排一次，不冻结则此处算出的偏移与
    最终位置对不上。

    参数:
        axes: 需要对齐的 ``Axes`` 序列。
    """
    fig.canvas.draw()
    fig.set_layout_engine("none")
    texts = [ax.get_title(loc="left") for ax in axes]
    for ax in axes:
        ax.set_title("", loc="left")
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    inv = fig.transFigure.inverted()
    blocks = [ax.get_tightbbox(renderer).transformed(inv) for ax in axes]
    for ax, text, block in zip(axes, texts, blocks):
        box = ax.get_position()
        # 必须写 loc="center": set_title 的三个 loc 各对应一个独立的 Text 对象,
        # 而 ``ax.title`` 只是居中的那一个 —— 若仍用 panel_title 写 loc="left",
        # 下面这行 set_x 改的是另一个空标题, 看上去毫无效果。
        ax.set_title(text, loc="center", fontweight="bold", color=INK, pad=7)
        ax.title.set_x(((block.x0 + block.x1) / 2 - box.x0) / box.width)


def recessive_axes(ax, grid_axis="y"):
    ax.grid(True, axis=grid_axis, linestyle="--", alpha=0.55, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def footnote(fig, text, color=INK_2, size=9.0):
    """图底脚注。与 watermark 分开: 实测图也需要脚注(数据出处), 但不该有水印。"""
    fig.text(0.5, 0.004, text, fontsize=size, color=color, ha="center", va="bottom")


def watermark(fig, note=None, ax=None):
    """绘制"占位示意数据"水印与图底红字脚注, 仅在 ``PLACEHOLDER`` 为真时生效.

    参数:
        fig: 承载脚注的 ``Figure``.
        note: 图底红字脚注文本, 逐格说明哪一格实测、哪一格占位. ``None``
            表示只打水印、不写脚注 —— 说明已由申请书正文的图说明承担时用它.
        ax: 水印落在哪个 ``Axes`` 内. ``None`` 表示整幅打标, 用于整张都是占位
            数据的图(图 4); 给定轴时只在该轴内打标, 用于只有一格占位的混合图
            (图 2 的 (a)(b) 已实测, 水印不该盖到它们身上)。整幅水印还会被单格
            切图横向切碎, 见 ``save_panels``.
    """
    if not PLACEHOLDER:
        return
    if ax is None:
        # 字号随图高收缩: 固定 80 pt 的斜排水印在矮图(图 4 只有 2.35 in 高)上
        # 比图还大。set_in_layout(False) 让它不参与 bbox_inches="tight" 的
        # 包围盒计算——否则水印会把画布撑高, 图的高宽比被悄悄改掉, 纸面高度也就变了。
        wm = fig.text(0.5, 0.5, "占位示意数据",
                      fontsize=min(80.0, 26.0 * fig.get_figheight()),
                      color="#e34948", alpha=0.085, ha="center", va="center",
                      rotation=28, fontweight="bold", zorder=1000)
    else:
        # constrained_layout 下轴的最终位置要到首次 draw 之后才定下来, 而字号
        # 得按轴宽定, 所以先强制渲染一次。
        fig.canvas.draw()
        width_in = ax.get_position().width * fig.get_figwidth()
        # 初值: "占位示意数据"六字旋转 28 度后的横向跨度约 (F/72)*(6*cos28+
        # sin28) = (F/72)*5.77 英寸, 令它占轴宽 85% 解出 F ~= 10.6*W。上限沿用
        # 整幅水印的公式, 保证单格水印不会比整幅的还大。
        fontsize = min(10.6 * width_in, 26.0 * fig.get_figheight())
        wm = ax.text(0.5, 0.5, "占位示意数据", transform=ax.transAxes,
                     fontsize=fontsize,
                     color="#e34948", alpha=0.085, ha="center", va="center",
                     rotation=28, fontweight="bold", zorder=1000)
        # 上面的解析式按 CJK 字宽 = 1 em 估, 实测偏小(缺字回退字体下量到 96%
        # 而非 85%), 且字宽随字体而变。水印一旦溢出轴框就漏进相邻格, 正是这里
        # 要避免的事, 所以量一次再回缩到轴框的 80%, 与字体无关。
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        span = wm.get_window_extent(renderer).width
        limit = 0.80 * ax.get_window_extent(renderer).width
        if span > limit:
            wm.set_fontsize(fontsize * limit / span)
    wm.set_in_layout(False)          # 溢出部分随边界裁掉即可, 水印本就该压在图上
    if note:
        fig.text(0.5, 0.004, note, fontsize=10.5, color="#e34948",
                 ha="center", va="bottom")


# ==========================================================================
# 数据
# ==========================================================================

# --------------------------------------------------------------------------
# 图 2 的三组数据全部为实测, 出处见文件头"数据来源声明"。
# 每个函数的 docstring 记录取数路径, 便于逐个字核对。
# --------------------------------------------------------------------------

def load_fig2_snapshot():
    """读入图 2 的数据快照, 缺失时给出重新采集的命令.

    快照由 SOPTX 侧采集并入库, 本文件只消费, 不再手抄任何数值。

    返回:
        snapshot: ``fig2_data.json`` 反序列化后的字典.

    异常:
        FileNotFoundError: 快照不存在时抛出, 消息中带重新采集的命令.
    """
    if not os.path.isfile(FIG2_SNAPSHOT):
        raise FileNotFoundError(
            f"图 2 的数据快照不存在: {FIG2_SNAPSHOT}\n"
            "先在 SOPTX 侧采集(需要 Open MPI 的启动器, 见 results_analysis.md §6):\n"
            "  SOPTX_MPIEXEC=/usr/bin/mpiexec.openmpi \\\n"
            "  python experiments/matrix_free_capability/run.py --all\n"
            "若 soptx 不在 ~/workspace/soptx, 用环境变量 SOPTX_ROOT 指定。")
    with open(FIG2_SNAPSHOT, encoding="utf-8") as handle:
        snapshot = json.load(handle)
    if not snapshot.get("reproducible", False):
        # 只提示, 不拦截: 开发期本来就在 dirty 工作区上重绘。
        record = snapshot.get("provenance", {})
        print(f"[warn] 快照 reproducible=False, 这批数字属开发证据; "
              f"revision={record.get('git_revision', '?')[:12]} "
              f"dirty={record.get('git_dirty')} "
              f"采集于 {record.get('generated_at_utc', '?')}")
    return snapshot


def data_convergence():
    """实测: 显式组装(FA)的相对 L2 误差收敛阶, 以及同网格上 EA 与 FA 解的相对差。

    两个维度各五档 ``h = 1/4 … 1/64``: 2D 用 ``sinusoidal``/``tri``, 3D 用
    ``divfree-poly``/``tet``, 均 ``p=1``, 两个维度统一走 MUMPS 稀疏直接解
    (``--mumps-sym 1``, 平面应变与三维的刚度阵同为对称正定), 使两条链除维数
    相关项外逐项对应。2D 早先走 SciPy ``spsolve``, 换成 MUMPS 后逐档相对误差
    只在第 11 位起变化 —— 求解器确实不改变离散。

    四档给出三个观测阶, 才看得出"朝理论阶 2 上升"是趋势而非巧合; 三档只有两个
    阶, 判断不了。**3D 之所以要走到第五档 (1/64), 是因为前四档的末段阶只有
    1.89, 图面上会被读成"四面体路径的阶偏低"**; 补上第五档后末段阶 1.969, 与
    2D 同样贴近理论阶 2, 前四档的偏低这才能确认是前渐近区而非离散缺陷。
    2D 一侧本来停在 1/32(末段阶已到 1.982, 再加一档只把 1.98 变成 1.995,
    对论断没有增量), 补到 1/64 买的是图面对称: 两条曲线横跨同一段 h,
    "最细档没有空心环"就成了两个维度一致的现象, 而不是 3D 独有的缺口。
    该档 8,450 自由度, 0.16 s。

    3D 的 n=64 (823,875 自由度) 早先跑不动, 有两个叠加的原因, 现均已解除:
    ``linear_elastic_integrator`` 的 ``standard`` 分支把随后要被求和掉的积分点
    轴物化成九个 ``(NC, NQ, 4, 4)`` 临时张量(单块 3.75 GiB), 以及本机 WSL2 的
    内存上限只有缺省的 31.2 GiB。改走 ``--assembly-method fast`` 并把上限抬到
    48 GB 之后, 该档实测峰值 RSS 17.38 GiB、单档 150.3 s(``--mumps-sym 1``)。
    口径与全部六组配置的对照见 SOPTX
    ``examples/lagrange_elasticity/results_analysis.md`` §4.4。

    **全部数值读自快照** ``FIG2_SNAPSHOT``, 字段 ``panels.a``。本函数不再手抄
    任何误差值 —— 手抄过一次就会过期: 重跑后 3D 误差链末位由 ``...264198`` 变成
    ``...264197``, 这类漂移肉眼查不出来, 而快照带 ``provenance`` 可追到 revision。

    快照由 SOPTX 的 ``experiments/matrix_free_capability/run.py`` 采集, 它按
    ``cases.toml`` 调用两处上游并做门禁:
      * ``panels.a.fa`` <- ``examples/lagrange_elasticity/manufactured_convergence_demo.py``
        (两个维度均 ``--base 4 --levels 5``), 产物
        ``manufactured_convergence_2d_tri_sinusoidal_p1_mumps.json`` 与
        ``manufactured_convergence_3d_tet_divfree-poly_p1_mumps_fast.json``,
        取 ``levels[].l2_relative`` 与 ``levels[].l2_order``。
      * ``panels.a.ea`` <- ``tools/matrix_free_evidence/validate.py`` 的
        ``outputs/stage1-validation-all.json``, 取
        ``dimensions.{2,3}.comparison`` 下的三档误差与
        ``coarse_solution_ea_fa_relative_difference``。

    相对误差(除掉精确解的 ``L2`` 范数)才可跨维度比较, 绝对误差不可, 二者的观测阶
    相同。EA/FA 解相对差取 ``coarse`` 档(2D 162、3D 2,187 自由度), 那是冻结链里
    唯一同时跑了 FA 直接解的一档, 更细的档位 FA 稀疏分解代价过高, 未纳入。

    注意 ``--base 4`` 必须显式传: 代码缺省是 ``BASE_SUBDIVISIONS = {2: 8, 3: 4}``,
    2D 不传会从 n=8 起步, 得到的是另一条误差链。这一条已写进 ``cases.toml``,
    经 ``run.py`` 走就不会漏。

    另注: ``validate.py`` 的 ``fa-multiple-ranks`` 反向用例要求启动器与 ``mpi4py``
    同厂。本机 ``PATH`` 上的 ``mpiexec`` 是 Intel MPI 而 ``mpi4py`` 链的是 Open MPI,
    直接跑会让两个 rank 各自成为 ``size=1`` 的独立进程, 守卫不触发而误报失败;
    须用 ``SOPTX_MPIEXEC=/usr/bin/mpiexec.openmpi``。该用例不产出图面数据,
    (a) 的八个档全是 ``1rank``, 数值不受影响。

    两处出处画的是同一个离散: 制造解类 (``SinusoidalPlaneStrainElasticity2D`` /
    ``DivergenceFreePolynomialElasticity3D``)、网格类与次数逐项相同, 两条误差链
    的相对误差逐档吻合到 10 位以上有效数字(2D 11/10/10 位, 3D 12/10/10 位),
    差别只来自 CG ``rtol=1e-10`` 与直接解。

    因此这一格的分工是: 曲线给显式组装这条参考路径的离散正确性(收敛阶朝 P1 理论
    阶 2 单调上升, 2D 1.83 → 1.94 → 1.98 → 2.00; 3D 1.26 → 1.68 → 1.89 → 1.97, 两条
    最终都到位), 空心环给 matrix-free 的正确性(EA 与 FA 解相对差 ``1e-13``~
    ``1e-14`` 量级, 即 matrix-free 复现了这条参考路径的解)。

    **两个维度最细的第五档都没有空心环**: EA 链由
    ``tools/matrix_free_evidence/contract.py`` 的 ``REFINEMENTS`` 固定在
    n = 8/16/32, 尚未延到 64; 最粗的 n=4 同样不在 EA 链上。这一格因此如实呈现
    为"中间三档两条实现路径重合, 首末两档只有显式组装"; 补齐要动 stage-1 的
    证据链, 是独立的一步。

    返回:
        h_fa_2d, fa_2d, h_fa_3d, fa_3d: 网格尺寸与相对 L2 误差(两个维度各五档).
        h_ea, ea_2d, ea_3d: matrix-free 的三档(n = 8/16/32).
        ord_2d, ord_3d: 逐段观测阶, 取自快照, 并与由误差链导出的值交叉核对.
        gate: 门禁下限, 取自 ``panels.a.gate.minimum_final_l2_order``.
        theory: P1 理论收敛阶 ``2.0``.
        gap_2d, gap_3d: ``coarse`` 档上 EA 与 FA 解的相对差(不画在图上).
        dof_ea_coarse_2d, dof_ea_coarse_3d: ``coarse`` 档自由度(不画在图上).

    异常:
        FileNotFoundError: 快照不存在.
        ValueError: 快照记录的观测阶与由误差链导出的不一致.
    """
    panel = load_fig2_snapshot()["panels"]["a"]
    fa, ea, gate = panel["fa"], panel["ea"], panel["gate"]

    # 显式组装(FA), 两个维度各五档, 同为 h = 1/4 … 1/64。横坐标仍分开取: 两条链
    # 出自两个独立的产物, 不假定它们的档位一定对齐。
    h_fa_2d = np.array(fa["2d"]["mesh_size"])
    fa_2d = np.array(fa["2d"]["l2_relative"])
    h_fa_3d = np.array(fa["3d"]["mesh_size"])
    fa_3d = np.array(fa["3d"]["l2_relative"])
    # Matrix-Free(EA)三档, 档位为 nx = 8/16/32, 即 FA 五档的中间三档。
    # 快照不存 EA 的 h, 从 roles(coarse/medium/fine)对应的加密比反推。
    h_ea = np.array([1.0 / 8, 1.0 / 16, 1.0 / 32])
    ea_2d = np.array(ea["2"]["l2_relative"])
    ea_3d = np.array(ea["3"]["l2_relative"])

    # 段标上的观测阶由**相对**误差链导出, 不直接取快照的 l2_order。理由是自洽:
    # 纵轴画的是相对误差, 读者按图上两点重算得到的就是这个值; 若改标 l2_order,
    # 图面自身会对不上 —— 上游的 l2_order 是用绝对误差 |u-uh|_0 算的, 而精确解的
    # L2 范数在各档由求积得到, 逐档有微差, 两种口径因此不完全相等(3D 首段
    # 1.255437 与 1.255444, 差在第 6 位; 2D 两者到 1e-9 内一致)。
    def _orders(err):
        return np.log2(err[:-1] / err[1:])

    ord_2d = _orders(fa_2d)
    ord_3d = _orders(fa_3d)
    # 与快照记录的 l2_order 交叉核对。容差 1e-4 是给上述归一化口径差留的余量, 不是
    # 给抄写误差留的: 真出现更大的偏离, 说明档位不再是等比加密(加密比不为 2),
    # 那时"逐段观测阶"这个标注本身就失去意义, 必须停下来查而不是照画。
    for name, derived, recorded in (
            ("2d", ord_2d, np.array(fa["2d"]["l2_order"][1:], dtype=float)),
            ("3d", ord_3d, np.array(fa["3d"]["l2_order"][1:], dtype=float))):
        if not np.allclose(derived, recorded, rtol=1e-4, atol=0.0):
            raise ValueError(
                f"{name} 由相对误差链导出的观测阶与快照记录的 l2_order 偏离超过 "
                f"1e-4: {derived} vs {recorded}; 档位可能不是等比加密, "
                "图面标注会失真。")

    return {
        "h_fa_2d": h_fa_2d, "fa_2d": fa_2d,
        "h_fa_3d": h_fa_3d, "fa_3d": fa_3d,
        "h_ea": h_ea, "ea_2d": ea_2d, "ea_3d": ea_3d,
        "ord_2d": ord_2d, "ord_3d": ord_3d,
        "gate": gate["minimum_final_l2_order"], "theory": 2.0,
        # 以下四项不画在图上, 但申请书的图说明逐字引用它们(EA/FA 解相对差写作
        # 5e-13 / 4e-14, 比对档写作 2D 162、3D 2,187 自由度)。从快照读出来并由
        # build_fig2 打印, 是为了让图说明每次重绘都能对一眼, 不靠记忆。
        "gap_2d": ea["2"]["solution_relative_difference_vs_fa"],
        "gap_3d": ea["3"]["solution_relative_difference_vs_fa"],
        "dof_ea_coarse_2d": fa["2d"]["dofs"][1],
        "dof_ea_coarse_3d": fa["3d"]["dofs"][1],
    }


def data_peak_memory():
    """实测: 显式组装(FA)与 Matrix-Free(EA)的**进程峰值 RSS** 随自由度的增长。

    3D 四面体 P1, 制造解 ``polynomial``(``DivergenceFreePolynomialElasticity3D``),
    装配方法 ``fast``, 无预条件 CG(``rtol=1e-10``), 五档 n = 8/16/32/64/80, 自由度
    2,187 / 14,739 / 107,811 / 823,875 / 1,594,323。最细档跨过百万线, 与申请书正文
    "三维百万至亿级自由度"的口径对得上; 它同时是本机 FA 路径的最后一档 —— 再上一
    档 FA 的组装瞬态就超过 47 GiB 主机内存, 配对不成立。

    **口径是进程驻留集高水位**(``resource.getrusage(RUSAGE_SELF).ru_maxrss``,
    与 ``/usr/bin/time -v`` 的 ``Maximum resident set size`` 同源, 实测逐 KiB
    吻合), 不是算子长期保存数组的字节数。后者只统计 CSR 的 COO 三元组或 EA 侧
    缓存的 ``K_e``, 既不含组装期临时量也不含 Krylov 工作向量。

    **必须一个进程测一个层级。** ``benchmark_cpu_ea.py`` 缺省的 ``serial-fa-ea``
    在同一进程里先后建 FA 与 EA, 高水位只等于两者的较大值, EA 隔离不出来。因此
    这批数据走的是该脚本的 ``--mode serial-peak-rss``, 十个独立进程。

    实测本身推翻了两条曾经想写进本格的说法:

      * **EA 省的不是"存得少", 而是"不物化全局 COO/CSR"。** n=64 上 FA 的
        ``operator`` 阶段单步涨 16.04 GiB, 而最终留下的 CSR 只有 0.81 GiB ——
        峰值的 95% 是组装过程量。EA 缓存的 ``K_e`` 反而有 1.83 GiB, 是 FA 稳态
        CSR 的 2.26 倍; 只看稳态存储, EA 是**更费**内存的那一个。
      * **倍数是 3.0 不是 3.8, 也不是曾经测到的 1.9。** 早先按"每自由度非零元
        vs 每积分点 double"推的 3.8 倍是目标形态下的估算; 而 2026-08-20 那批实测
        给出的 1.9 倍偏低, 根因是 FEALPy fork 的 ``functional.py::linear_integral``
        把与单元无关的基函数沿单元轴广播物化, 白抬了 EA 的体力向量组装峰值
        (n=64 上 3.25 GiB)。修掉之后重测, 五档峰值比为 1.13 / 1.71 / 2.50 /
        2.96 / 3.02 —— 最粗档偏低是因为解释器基线(0.158 GiB)还没被摊薄。扣掉基线后
        五档为 2.69 / 2.85 / 2.80 / 3.02 / 3.05。缺陷与修法见 SOPTX
        ``docs/known-issues/fealpy-linear-integral-broadcast.md``。

    "可算规模约为 3.1 倍"这句话成立, 依据是两条线扣基线后**都是自由度的一次
    函数**: 从 n=16 到 n=80 自由度涨 108.2 倍, FA 的基线以上峰值涨 115.7 倍
    (指数 1.014), EA 涨 107.9 倍(指数 0.999)。线性增长下, 内存上限固定时可算
    规模之比就等于内存之比 —— 也正因如此, 结论**与内存上限取什么值无关**, 天
    花板线不参与论证, 已从 ``draw_panel_b`` 删去(理由见该函数)。

    **横轴止于实测最大规模, 不外推; 纵轴也不画天花板。** 本机实际可用内存
    47.04 GiB(``MemTotal = 49,325,728 kB``)仍由本函数返回, 但只供图说明引用,
    不再画进图面: 留一条够不着的水平线而不画交点, 只会诱导读者自己延长曲线,
    做的恰是这里声明不做的外推。真要画交点, EA 一侧得从实测最细档的 10.76 GiB
    外推到 46.9 GiB(4.4 倍), 交点自由度随拟合口径仍在 6.5~7.3 M 间摆动(±12%) ——
    补上 n=80 一档把外推距离缩短了一半, 却没有把这个区间收窄, 这本身就是"线性成立
    但常数项不确定"的旁证。另需注意
    这批数是 CPU 主机 RSS, 拿某块 GPU 的显存当天花板会把两种资源混为一谈;
    GPU 路径(阶段 1c)未开始。

    **只画内存、不画时间。** 少存就得多算, 这个取舍是 memory-vs-recompute, 本格
    只出示内存这一侧的事实; 谁更优是研究内容 2 要回答的问题。作为对照, 同一批
    运行里 n=64 的求解时间 EA 84.74 s 对 FA 55.91 s(EA 更慢), 而组装时间 EA
    3.64 s 对 FA 22.45 s(EA 更快), 两段相抵后 EA 的总时长仍多 13%; n=80 一档同向
    但差距收窄(求解 205.09 s 对 138.15 s, 组装 7.21 s 对 61.71 s, 总时长多 6%)。
    两者迭代数逐档相同(n=80 为 600)、真相对残差同为 ``1.4475e-10``, 即同一个
    离散、同一条收敛轨迹。

    **全部数值读自快照** ``FIG2_SNAPSHOT`` 的 ``panels.b``, 与 (a) 同一份出处,
    本函数不再手抄。上游是 ``examples/matrix_free_elasticity/benchmark_cpu_ea.py``
    的十次独立运行(每档一个进程, 因为 ``ru_maxrss`` 是进程级高水位, 同进程里
    先建 FA 再建 EA 会把 EA 的峰值抬高), 产物
    ``peak_rss_3d_tet_polynomial_p1_{fa,ea}_fast_n{8,16,32,64,80}.json``。
    口径与逐阶段分解见 SOPTX ``experiments/matrix_free_capability/results_analysis.md``
    §3。绝对值不可移植(随机器、BLAS 与分配器变化), 可引用的是同机同批次的相对关系。

    返回:
        dof: 五档自由度数.
        mem_fa, mem_ea: 进程峰值 RSS / GiB.
        baseline: 解释器与已导入模块的基线高水位 / GiB.
        ceiling: 本机内存总量 / GiB.

    异常:
        FileNotFoundError: 快照不存在.
    """
    panel = load_fig2_snapshot()["panels"]["b"]
    gib = float(1 << 30)
    dof = np.array(panel["dofs"], dtype=float)
    mem_fa = np.array(panel["fa"]["peak_rss_bytes"], dtype=float) / gib
    mem_ea = np.array(panel["ea"]["peak_rss_bytes"], dtype=float) / gib
    baseline = panel["baseline_bytes"] / gib
    ceiling = panel["memory_total_bytes"] / gib
    return dof, mem_fa, mem_ea, baseline, ceiling


def data_mpi_strong():
    """实测: 固定规模下 CG 求解耗时随 MPI 进程数的变化(进程级强扩展)。

    **横轴是进程数, 不是自由度**, 这一格因此不与 (b)(d) 同轴。这是内容决定的:
    (b)(d) 问"规模变大会怎样", 这一格问"同一个问题切成更多份会怎样", 强行统一
    横轴只会造出一个没有意义的坐标系。规模固定在 n = 64(823,875 自由度) —— 更
    粗的 n = 32 在本机 P=8 处就掉头(2.67 -> 2.61 倍), 因为每 rank 只剩约 6,738
    个自由度, 那是问题过小的伪影而不是方法性质。

    **它与 (d) 是两个并行层级, 加速比不可相乘也不可互推。** 这一格切进程(MPI),
    (d) 切设备内(SIMT); dut-postdoc 的 concepts/gpu-hpc/parallel-levels.md 明写
    "不把某一并行层级的加速或扩展性结论外推到另一层级"。两格并排是为了说明两条
    路都通, 不是为了把 3.69 和 16 乘起来。

    **线程层被显式锁死**(``OMP_NUM_THREADS=1``)。不锁, 每个 rank 底下的 OpenBLAS
    还会再开线程, 量到的是"进程 x 线程"的乘积, 那条曲线无法归因到任一层级 ——
    这是本图七种配置里唯一一处显式设定线程数的地方, 其余各格用的都是库默认值。

    **效率掉下去不是通信造成的。** 最大档同步只占一次 MatVec 的 15.8%, 而本地
    单元作用本身从 1 到 16 进程只快了 3.85 倍; 末两档进程翻倍、本地核只快 1.12
    倍 —— 多出来的核已经吃不到更多内存带宽。EA 算术强度约 0.25 flop/byte, 本
    来就是 memory-bound, 节点内加进程买到的是算力不是带宽。这条 CPU 侧的饱和与
    (d) 里 GPU 只吃到标称带宽四成出头, 是同一件事的两面。

    **分区没有改变代数**: 五档 CG 迭代数逐档相同(493), 真实相对残差跨档相对离散
    仅 6.5e-5(归约次序随分区改变的浮点表现)。加速是真省了时间, 不是靠少算。

    **计时口径**: 本批实跑 ``--warmup 0 --repeats 1``(脚本默认 1 / 3), 秒数不带
    误差棒; 曲线形状与正确性结论不受影响, 但数字定稿前应按默认口径重跑。

    **全部数值读自快照** ``FIG2_SNAPSHOT`` 的 ``panels.d``。上游是
    ``examples/matrix_free_elasticity/benchmark_cpu_ea.py`` 的五次独立运行
    (case ``d-mpi-p{1,2,4,8,16}``), 产物 ``outputs/mpi/mpi_strong_3d_n64_fast_p*.json``。
    绝对值不可移植, 可引用的是同机同批次的相对关系。

    返回:
        ranks: 进程数数组.
        speedup: 相对单进程的 CG 求解加速比.
        efficiency: 并行效率(speedup / ranks).
        info: 供图面角注引用的标量字典.

    异常:
        RuntimeError: 快照里 (c) 仍是占位.
    """
    panel = load_fig2_snapshot()["panels"]["d"]
    if panel.get("status") != "measured":
        raise RuntimeError(
            "快照里进程级强扩展仍是占位: " + str(panel.get("reason", "")) + "\n"
            "先在 SOPTX 侧跑 python experiments/matrix_free_capability/run.py --panel d")
    ranks = np.array(panel["ranks"], dtype=float)
    speedup = np.array(panel["speedup"], dtype=float)
    efficiency = np.array(panel["efficiency"], dtype=float)
    matvec = np.array(panel["matvec_seconds"], dtype=float)
    kernel = np.array(panel["local_kernel_seconds"], dtype=float)
    sync = (np.array(panel["input_sync_seconds"], dtype=float)
            + np.array(panel["output_sync_seconds"], dtype=float))
    info = {
        "dofs": int(panel["dofs"]),
        "sync_share": float(sync[-1] / matvec[-1]),
        "kernel_speedup": float(kernel[0] / kernel[-1]),
        "iterations": int(panel["cg_iterations"][-1]),
    }
    return ranks, speedup, efficiency, info


def data_device_speedup():
    """实测: 同一 matrix-free 算子在 CPU 与单块 GPU 上的单次 CG 求解耗时。

    **横轴与 (b) 同为自由度, 且是同一批算例**(3D 四面体 P1, n = 8/16/32/64)。
    (c) 比 (b) 少最细的一档: (b) 到 n=80, 而 n=80 在这块 16 GiB 卡上装不下 ——
    n=64 一档的 GPU 峰值分配已是 12.800 GiB(占整卡 15.920 GiB 的 80.4%), 峰值随
    自由度近似线性, n=80 需约 24.8 GiB。两格仍在同一条轴上(档位是 (b) 的前缀),
    只是 (c) 早一步停; 采集端的同轴门禁因此按前缀判定, 不是按逐档相同。
    (b)(c)(d) 三格同轴是有意的: (b) 说"同一台机器上能算多大", (c) 接着说"这么
    大的问题算得多快", (d) 再答"快从哪来、还差多少", 读者一路不必换坐标系。2x2
    版式下 (b) 在右上、(c)(d) 在下排, 是换行接着读, 不是并排; 正因为不并排, 横
    轴范围必须逐字相同, 否则上下对读时会错位。若 (c) 另起一套横轴(GPU 数、进程
    数、网格层数), 这几格就成了互不相干的实验。

    **是单卡对 CPU, 不是多卡强扩展。** 这一格要证的是"matrix-free 算子本身
    可以搬上加速器", 一块卡就能证完; 多卡扩展是研究内容 2 的题目, 放进研究
    基础栏目会让评审以为多卡结果已经有了。本机也没有多卡环境。

    **唯一的变量是设备。** 两侧都走 FEALPy 的 ``pytorch`` 后端, 只切
    ``bm.set_default_device("cpu" / "cuda")``; 若 CPU 侧改用 ``numpy`` 后端,
    加速比里就混进了后端差异, 量到的不再是"这个算子能不能上加速器"。

    **验收门禁: GPU 与 CPU 两条路径解的相对差不大于 1e-9。** 加速比没有意义,
    除非两边算的是同一个问题 —— 这一条不过, 曲线再好看也不进图。实测四档为
    3.3e-13 / 6.9e-13 / 3.3e-15 / 3.4e-15, 比门禁松了三到五个量级; 更强的一条
    证据是**两侧 CG 迭代数逐档相同**(64 / 134 / 250 / 493), 即整条 Krylov 轨迹
    一致, 而不只是碰巧收敛到附近。

    **画的是 CG 求解时间, 不含算子构造。** 构造时间另记在快照里(``build_seconds``,
    GPU 同样快, n=64 上 2.11 s -> 0.39 s), 但不上图: (b) 已经把"每档要花多少
    存储"讲完了, (c) 只回答"同样这批规模算得多快", 两段时间叠在一起反而看不出
    是哪一段被加速。

    **最粗档 GPU 更慢, 这一档必须留着。** n=8 只有 2,187 个自由度, 核函数启动与
    同步的固定开销吃掉全部收益(0.35 倍)。删掉它图会更好看, 但也就删掉了"什么时候
    该用 GPU"这个信息 —— 曲线的交叉点本身是结论的一部分。

    **计时口径**: 每档 warmup 1 次后计时 3 次取中位数; CUDA 侧每个计时边界前后
    都做 ``torch.cuda.synchronize``, 否则量到的是 kernel 派发时间而非执行时间。

    **全部数值读自快照** ``FIG2_SNAPSHOT`` 的 ``panels.c``, 与 (a)(b) 同一份
    出处。上游是 ``examples/matrix_free_elasticity/benchmark_device_ea.py`` 的
    四次运行(case ``c-dev-n{8,16,32,64}``), 产物
    ``device_speedup_3d_tet_polynomial_p1_ea_fast_n{8,16,32,64}.json``。绝对值
    不可移植(GPU 为 RTX 5080 16 GiB), 可引用的是同机同批次的相对关系。

    返回:
        dof: 四档自由度数, 与 (b) 同轴.
        t_cpu, t_gpu: CPU / 单卡 GPU 的 CG 求解耗时中位数, 单位 s.
        gap: 四档中最大的两侧解相对差, 供图面角注引用.

    异常:
        FileNotFoundError: 快照不存在.
    """
    panel = load_fig2_snapshot()["panels"]["c"]
    if panel.get("status") != "measured":
        raise RuntimeError(
            "快照里 (c) 仍是占位: " + str(panel.get("reason", "")) + "\n"
            "先在 SOPTX 侧跑 python experiments/matrix_free_capability/run.py --panel c")
    dof = np.array(panel["dofs"], dtype=float)
    t_cpu = np.array(panel["cpu"]["solve_seconds"], dtype=float)
    t_gpu = np.array(panel["cuda"]["solve_seconds"], dtype=float)
    gap = max(panel["solution_relative_gap"])
    return dof, t_cpu, t_gpu, gap


def data_bandwidth():
    """由 (c) 的逐档耗时反算 CPU / 单卡 GPU 的有效访存带宽。

    **不需要任何额外采集。** 三个输入(``cells`` / ``solve_seconds`` /
    ``cg_iterations``)都已在快照的 ``panels.c`` 里, 与 (c) 同一批运行、同一份
    出处; 这一格是对已有测量的换算, 不是新实验。soptx 的 results_analysis.md
    表 c-2 用的是同一个式子, 两处数值可逐位对齐。

    **算法**: 每次 CG 迭代把全部单元刚度阵流过一遍, 故

        带宽 = cells * EA_BYTES_PER_CELL / (solve_seconds / cg_iterations)

    **这是下界, 不是精确访存量。** 分子只算了单元刚度阵, 没算单元-自由度索引
    数组、输入输出向量与 CG 自身的向量操作; 真实访存量比它大, 所以真实带宽利用
    率比图上画的更高一些。用下界是有意的: 结论是"离标称还有距离, 值得优化", 高
    估分子会把这个结论说过头。

    **为什么值得单开一格。** (c) 只给出"最细档快约 16 倍", 读者接着要问的是
    "为什么快"和"还能快多少"。这一格同时答掉两问: CPU 侧全程持平在带宽墙上
    (14 -> 26 GB/s), GPU 侧随规模从 4.9 爬到 410 GB/s —— 那条加速曲线本质上就是
    GPU 的带宽饱和曲线; 而 410 GB/s 只到 RTX 5080 标称 960 GB/s 的四成出头, 余
    下的空间正是研究内容 2 要做的事。没有这一格, "加速 16 倍"是个孤立数字; 有
    了它, 它变成一条有机理、有余量、指向下一步的曲线。

    返回:
        dof: 四档自由度数, 与 (b)(c) 同轴.
        bw_cpu, bw_gpu: 有效访存带宽下界, 单位 GB/s.
        spec: GPU 厂商标称带宽 GB/s, 供正文与 results_analysis.md 引用.

    异常:
        RuntimeError: 快照里 (c) 仍是占位.
    """
    panel = load_fig2_snapshot()["panels"]["c"]
    if panel.get("status") != "measured":
        raise RuntimeError(
            "快照里 (c) 仍是占位, (d) 由 (c) 换算而来, 故一并无法绘制: "
            + str(panel.get("reason", "")))
    dof = np.array(panel["dofs"], dtype=float)
    stream_bytes = np.array(panel["cells"], dtype=float) * EA_BYTES_PER_CELL
    bw = {}
    for key in ("cpu", "cuda"):
        seconds = np.array(panel[key]["solve_seconds"], dtype=float)
        iterations = np.array(panel[key]["cg_iterations"], dtype=float)
        bw[key] = stream_bytes / (seconds / iterations) / 1e9
    return dof, bw["cpu"], bw["cuda"], GPU_SPEC_BANDWIDTH_GB_S


# --------------------------------------------------------------------------
# 图 3 的三组数据全部为实测, 出处见文件头"数据来源声明"。
# --------------------------------------------------------------------------

def load_fig3_snapshot():
    """读入图 3 的数据快照, 缺失时给出重新采集的命令.

    快照由 SOPTX 侧采集并入库, 本文件只消费, 不再手抄任何数值。

    返回:
        snapshot: ``fig3_data.json`` 反序列化后的字典.

    异常:
        FileNotFoundError: 快照不存在时抛出, 消息中带重新采集的命令.
    """
    if not os.path.isfile(FIG3_SNAPSHOT):
        raise FileNotFoundError(
            f"图 3 的数据快照不存在: {FIG3_SNAPSHOT}\n"
            "先在 SOPTX 侧采集:\n"
            "  python experiments/piml_capability/run.py --collect\n"
            "若 soptx 不在 ~/workspace/soptx, 用环境变量 SOPTX_ROOT 指定。")
    with open(FIG3_SNAPSHOT, encoding="utf-8") as handle:
        snapshot = json.load(handle)
    if not snapshot.get("reproducible", False):
        record = snapshot.get("provenance", {})
        print(f"[warn] 图 3 快照 reproducible=False, 这批数字属开发证据; "
              f"revision={record.get('git_revision', '?')[:12]} "
              f"dirty={record.get('git_dirty')} "
              f"采集于 {record.get('generated_at_utc', '?')}")
    return snapshot


def data_condensation_equivalence():
    """实测: 静力缩聚求解与 Lagrange 全装配直解的代数等价性。

    读自快照 ``FIG3_SNAPSHOT`` 的 ``panels.a``。
    两条链是**同一个离散的两种解法**: 全装配直解与"缩聚接口求解 + 内部回填",
    因此二者之差只应是浮点累积, 不含任何离散误差。这一格因而是 PIML 的入场券——
    代理学的是缩聚算子, 若缩聚本身与直解不等价, 后两格的精度全部无意义。

    口径:
      * 2D ``HalfMBBBeamRight2d``, ``n_sub = 6x2``, ``n_fine = 5x5``, 682 全尺度自由度;
      * 3D ``FullMBBBeam3d``, ``n_sub = 6x2x2``, ``n_fine = 4x4x4``, 6,075 全尺度自由度;
      * 位移为全场相对 ``L2``, 柔度为标量相对差, 验收阈值 ``1e-11``。

    快照按 2D/3D 分组存了四条记录, 这里在**绘图侧**合并成"位移场""柔度"两条
    (快照只读, 不改数据文件)。两个原因:
      * 申报书全文规避 2D/3D 这类维度分类标签, 图面不能留;
      * 四条柱子其实在重复说同一件事"都到机器精度", 合并后面板更干净, 而
        "两套离散都验过"这个信息由图 2(a) 的两条收敛曲线承担, 不会丢。
    每条取两个算例中**较大**者(即更保守的一侧), 因此图面数值不优于任一实测值。

    返回:
        labels: 两个指标名, 不含维度.
        values: 对应的相对差(取两算例较大者).
        colors: 统一用 INK_2 中性灰——合并后不再区分维度, 蓝/橙会误导成两类.
        gate: 验收阈值.
    """
    panel = load_fig3_snapshot()["panels"]["a"]
    # 快照 labels 形如 "3D 柔度"/"2D 位移场", 按去掉维度前缀后的指标名归并
    merged: dict[str, float] = {}
    for raw, v in zip(panel["labels"], panel["values"]):
        metric = raw.split(maxsplit=1)[1] if " " in raw else raw
        merged[metric] = max(merged.get(metric, 0.0), float(v))
    # 固定顺序: 棒棒糖图 y=arange, 索引 0 画在最下, 因此这里列"柔度"在前,
    # 图面上才是位移场在上、柔度在下, 与正文"位移和柔度"的行文次序一致
    order = ["柔度", "位移场"]
    labels = [m for m in order if m in merged] + \
             [m for m in merged if m not in order]
    values = np.array([merged[m] for m in labels], dtype=float)
    colors = [INK_2] * len(labels)
    gate = float(panel["gate"])
    return labels, values, colors, gate


def data_piml_routes():
    """实测: 形函数路线的二阶误差压缩机理 (双对数受控扰动扫描 + 网络实测点).

    读自快照 ``FIG3_SNAPSHOT`` 的 ``panels.b``。
    机理: 设预测形函数 ``N_hat = N* + E``, 由 Huang 2023 式 (17)
    ``K_tilde = P^T K P`` 反推缩聚刚度, 则一阶项因 ``K_ii N* = -K_ib`` 逐项抵消,

        ``K_tilde(N* + E) - K_s == E^T K_ii E``

    是恒等式而非近似。故误差关于 ``||E||`` 严格二阶(实测 log-log 斜率 2.0030),
    且因 ``K_ii`` 对称正定, 误差阵半正定——式 (17) 只可能高估刚度。

    返回:
        eps_n, eps_k: 受控扫描的 12 个点.
        slope: log-log 拟合斜率.
        net_n, net_k: 训练网络在留出集上的 (形函数误差 8.97%, 式 (17) 后的刚度误差 0.44%).
    """
    panel = load_fig3_snapshot()["panels"]["b"]
    eps_n = np.array(panel["eps_n"], dtype=float)
    eps_k = np.array(panel["eps_k"], dtype=float)
    slope = float(panel["slope"])
    net_n = float(panel["net_n"])
    net_k = float(panel["net_k"])
    return {
        "eps_n": eps_n, "eps_k": eps_k, "slope": slope,
        "net_n": net_n, "net_k": net_k,
    }


def data_piml_solution_layer():
    """实测: PIML 代理缩聚求解在全系统有限元中的端到端保真度 (FullMBBBeam2d).

    读自快照 ``FIG3_SNAPSHOT`` 的 ``panels.c``。
    在 24 个子结构装配的完整全局系统上, 逐项对比预测子结构形函数 vs 预测子结构刚度:
      * 局部刚度误差 max: 0.15% (预测刚度: 5.83%)
      * 接口位移相对误差: 0.15% (预测刚度: 2.05%)
      * 全场位移相对误差: 0.15% (预测刚度: 2.01%)
      * 全局结构柔度相对误差: 0.20% (预测刚度: 3.64%)

    返回:
        labels: 四项指标名称.
        piml_values: 预测子结构形函数路线的误差值.
        direct_values: 预测子结构刚度路线的误差值.
    """
    panel = load_fig3_snapshot()["panels"]["c"]
    labels = panel["labels"]
    piml_values = np.array(panel["piml_values"], dtype=float)
    direct_values = np.array(panel["direct_values"], dtype=float)
    return labels, piml_values, direct_values


def data_rigid_pollution():
    """实测: PIML 批量缩聚与传统 CPU 缩聚在多子结构并发下的耗时与加速比.

    读自快照 ``FIG3_SNAPSHOT`` 的 ``panels.d``。
    """
    panel = load_fig3_snapshot()["panels"]["d"]
    n_subs = np.array(panel["n_subs"], dtype=int)
    t_cpu_ms = np.array(panel["t_cpu_ms"], dtype=float)
    t_gpu_ms = np.array(panel["t_gpu_ms"], dtype=float)
    speedup = np.array(panel["speedup"], dtype=float)
    device = panel.get("device", "RTX 5080")
    return n_subs, t_cpu_ms, t_gpu_ms, speedup, device


def load_fig4_snapshot():
    """读入图 4 (申报书图 6) 的数据快照.

    快照由 soptx 的 ``experiments/topopt_capability/collect.py`` 从真实运行产物
    汇编，数字全部实测。此处兜底只防快照文件暂不可达（如 SOPTX_ROOT 指向不对），
    数值与快照同步维护，快照可达时以快照为准。
    """
    if not os.path.isfile(FIG4_SNAPSHOT):
        # 回退默认（与 2026-08-28 真实实测一致，仅用于快照不可达时）
        return {
            "panels": {
                "n_dofs": 1915263,
                "iterations": 90,
                "labels_a": ["CPU 传统流程\n(NumPy / SciPy 稀疏)", "GPU 张量化平台\n(SOPTX PyTorch)"],
                "times_a": [255.94, 10.41],
                "speedup_a": 24.6,
                "stages_b": [
                    "1. 刚度组装",
                    "2. 平衡方程求解",
                    "3. 伴随灵敏度滤波",
                    "4. 设计变量更新",
                ],
                "speedups_b": [317.8, 26.5, 1.6, 3.7],
                "time_details_b": [
                    "9.84→0.03 s",
                    "243.92→9.20 s",
                    "1.66→1.03 s",
                    "0.52→0.14 s",
                ]
            }
        }
    with open(FIG4_SNAPSHOT, encoding="utf-8") as handle:
        return json.load(handle)


def data_backends():
    """实测: 191.5 万自由度三维结构拓扑优化单步全流程 CPU vs GPU 耗时与加速比 (读自 FIG4_SNAPSHOT)."""
    snapshot = load_fig4_snapshot()
    return snapshot["panels"]


# --------------------------------------------------------------------------
# 真实的 SIMP + OC 拓扑优化（Andreassen 等 88 行算法的 NumPy 实现）
#
# **当前未被调用**：原图 2 的 (c2) "平台产出的拓扑优化算例(MBB 梁)" 面板已删除。
# 它曾是全部图面中唯一的真实数据，但只能证明"平台能跑通"，在研究基础一栏里
# 信息量低于其他面板。保留本函数以备需要把该面板加进图 4。
# --------------------------------------------------------------------------
def topopt(nelx=90, nely=30, volfrac=0.40, penal=3.0, rmin=2.4, n_iter=45):
    ndof = 2 * (nelx + 1) * (nely + 1)
    nu, E0, Emin = 0.3, 1.0, 1e-9

    k = np.array([1/2 - nu/6, 1/8 + nu/8, -1/4 - nu/12, -1/8 + 3*nu/8,
                  -1/4 + nu/12, -1/8 - nu/8, nu/6, 1/8 - 3*nu/8])
    KE = 1 / (1 - nu**2) * np.array([
        [k[0], k[1], k[2], k[3], k[4], k[5], k[6], k[7]],
        [k[1], k[0], k[7], k[6], k[5], k[4], k[3], k[2]],
        [k[2], k[7], k[0], k[5], k[6], k[3], k[4], k[1]],
        [k[3], k[6], k[5], k[0], k[7], k[2], k[1], k[4]],
        [k[4], k[5], k[6], k[7], k[0], k[1], k[2], k[3]],
        [k[5], k[4], k[3], k[2], k[1], k[0], k[7], k[6]],
        [k[6], k[3], k[4], k[1], k[2], k[7], k[0], k[5]],
        [k[7], k[2], k[1], k[4], k[3], k[6], k[5], k[0]]])

    edofMat = np.zeros((nelx * nely, 8), dtype=int)
    for elx in range(nelx):
        for ely in range(nely):
            el = ely + elx * nely
            n1 = (nely + 1) * elx + ely
            n2 = (nely + 1) * (elx + 1) + ely
            edofMat[el] = [2*n1+2, 2*n1+3, 2*n2+2, 2*n2+3, 2*n2, 2*n2+1, 2*n1, 2*n1+1]
    iK = np.kron(edofMat, np.ones((8, 1))).flatten()
    jK = np.kron(edofMat, np.ones((1, 8))).flatten()

    # 密度过滤矩阵
    nfilter = int(nelx * nely * ((2 * (np.ceil(rmin) - 1) + 1) ** 2))
    iH, jH, sH = np.zeros(nfilter), np.zeros(nfilter), np.zeros(nfilter)
    cc = 0
    for i in range(nelx):
        for j in range(nely):
            row = i * nely + j
            for i2 in range(max(i - int(np.ceil(rmin)) + 1, 0),
                            min(i + int(np.ceil(rmin)), nelx)):
                for j2 in range(max(j - int(np.ceil(rmin)) + 1, 0),
                                min(j + int(np.ceil(rmin)), nely)):
                    col = i2 * nely + j2
                    fac = rmin - np.sqrt((i - i2) ** 2 + (j - j2) ** 2)
                    iH[cc], jH[cc], sH[cc] = row, col, max(0.0, fac)
                    cc += 1
    H = coo_matrix((sH[:cc], (iH[:cc], jH[:cc])),
                   shape=(nelx * nely, nelx * nely)).tocsc()
    Hs = H.sum(1).A1

    # MBB 半梁: 左边界 x 向固定, 右下角 y 向固定, 左上角施加 -y 集中力
    dofs = np.arange(ndof)
    fixed = np.union1d(dofs[0:2 * (nely + 1):2],
                       np.array([2 * (nelx + 1) * (nely + 1) - 1]))
    free = np.setdiff1d(dofs, fixed)
    f = np.zeros(ndof)
    f[1] = -1.0

    x = volfrac * np.ones(nelx * nely)
    xPhys = x.copy()

    for _ in range(n_iter):
        sK = ((KE.flatten()[np.newaxis]).T *
              (Emin + xPhys ** penal * (E0 - Emin))).flatten(order="F")
        K = coo_matrix((sK, (iK, jK)), shape=(ndof, ndof)).tocsc()
        K = K[free, :][:, free]
        u = np.zeros(ndof)
        u[free] = spsolve(K, f[free])

        ce = np.einsum("ij,jk,ik->i", u[edofMat], KE, u[edofMat])
        dc = -penal * xPhys ** (penal - 1) * (E0 - Emin) * ce
        dv = np.ones(nelx * nely)

        dc = np.asarray(H @ (dc / Hs))
        dv = np.asarray(H @ (dv / Hs))

        # OC 二分更新
        l1, l2, move = 0.0, 1e9, 0.2
        while (l2 - l1) / (l1 + l2 + 1e-30) > 1e-3:
            lmid = 0.5 * (l1 + l2)
            xnew = np.maximum(0.0, np.maximum(
                x - move, np.minimum(1.0, np.minimum(
                    x + move, x * np.sqrt(np.maximum(-dc / dv / lmid, 0.0))))))
            xPhys = np.asarray(H @ (xnew / Hs))
            if xPhys.sum() > volfrac * nelx * nely:
                l1 = lmid
            else:
                l2 = lmid
        x = xnew

    return xPhys.reshape((nely, nelx), order="F")


# ==========================================================================
# 图 2 —— Matrix-Free 求解一致性与内存扩展性（储备一）
# ==========================================================================

def draw_panel_a(ax, cv):
    """把图 2(a)"正确性验证"画进 ``ax``.

    参数:
        ax: 目标 ``Axes``.
        cv: ``data_convergence()`` 的返回值.
    """
    h2, fa2 = cv["h_fa_2d"], cv["fa_2d"]
    h3, fa3 = cv["h_fa_3d"], cv["fa_3d"]
    h_ea, ea2, ea3 = cv["h_ea"], cv["ea_2d"], cv["ea_3d"]

    # 维度用 颜色 + marker + 线型 三重编码。基金评审常打印阅读, 而蓝与橙在灰度
    # 下明度接近, 只靠颜色会糊成一团, 因此 2D 实线、3D 虚线。
    ax.loglog(h3, fa3, color=C_ORANGE, lw=2.0, ls="--", marker="s", ms=5.8,
              mec=SURFACE, mew=1.0, zorder=4)
    ax.loglog(h2, fa2, color=C_BLUE, lw=2.0, ls="-", marker="o", ms=5.8,
              mec=SURFACE, mew=1.0, zorder=4)
    # Matrix-Free(EA)的三档误差与 FA 的后三档逐位重合, 所以不另画一条线 —— 另画
    # 只会得到一条压在原线上的重线, 读者反而看不出"重合"是结论而非绘图偶然。
    # 空心环套在同一位置: "两条实现路径落在同一条曲线上"因此是看出来的, 不是
    # 角落文本框里读来的。这同时把 matrix-free 的验证规模从 coarse 档(2D 162、
    # 3D 2,187 自由度)抬到 fine 档(2D 2,178、3D 107,811 自由度)。
    ax.loglog(h_ea, ea3, ls="none", marker="s", ms=9.0, mfc="none",
              mec=C_ORANGE, mew=1.4, zorder=5)
    ax.loglog(h_ea, ea2, ls="none", marker="o", ms=9.0, mfc="none",
              mec=C_BLUE, mew=1.4, zorder=5)

    # 逐段观测阶: 本格的论断是"三个阶单调趋近理论阶 2", 只标末段等于把趋势藏进
    # 图注, 图面上只剩两个孤立数字。标在段的对数中点, 3D 走线上方、2D 走线下方,
    # 两条线之间那条 36~52 pt 的走廊一律不用。
    def _segment_midpoints(x, y):
        return np.sqrt(x[:-1] * x[1:]), np.sqrt(y[:-1] * y[1:])

    for (xs, ys), orders, color, dy, va in (
            (_segment_midpoints(h3, fa3), cv["ord_3d"], C_ORANGE, 10, "bottom"),
            (_segment_midpoints(h2, fa2), cv["ord_2d"], C_BLUE, -10, "top")):
        for xm, ym, order in zip(xs, ys, orders):
            ax.annotate(f"{order:.2f}", xy=(xm, ym), xytext=(0, dy),
                        textcoords="offset points", fontsize=10, color=color,
                        fontweight="bold", ha="center", va=va)

    # 不画斜率三角, 也不画贯穿全图的参考直线。理论阶 2 已经以数字形式写在左下的
    # 核验文字里, 而图面上六个观测阶也是数字, 读者做的本就是数字对数字的比较;
    # 再画一个几何版的"2"是同一件事的第二种画法, 只是把右上填满。门禁 1.5 则相反,
    # 它在这张图上没有几何位置(y 轴是误差, 不是收敛阶), 只能靠文字给, 所以留下。
    ax.set_xlabel("网格尺寸 $h$")
    ax.set_ylabel(r"相对 $L^2$ 误差")
    ax.invert_xaxis()          # 向右 = 网格更细, 与"加密"的阅读方向一致
    ax.set_xlim(0.33, 0.0127)  # 右侧容下两个维度的第五档 1/64; 左侧留出图例
    # 对数轴默认的次刻度标签在这个宽度上会叠成一团, 只保留五个实际网格档
    ax.set_xticks(np.array([1 / 4, 1 / 8, 1 / 16, 1 / 32, 1 / 64]))
    ax.set_xticklabels(["1/4", "1/8", "1/16", "1/32", "1/64"])
    ax.xaxis.set_minor_locator(NullLocator())
    # 下界压到 1.5e-4: 2D 末档点降到 7.6e-4(第五档), 其下方还挂着 "2.00" 的段
    # 中点标注; 左下的图例与核验文字在最粗档一侧, 与两条曲线互不相交。
    # 上界 1.2: 原为 2.4, 是给斜率三角(顶边在 y=1.5)留的; 三角删掉后只需容下
    # 3D 最粗档 0.68 及其上方的 "1.26" 段中点标注。
    ax.set_ylim(1.5e-4, 1.2)
    ax.yaxis.set_minor_formatter(NullFormatter())
    recessive_axes(ax, grid_axis="both")

    # 图例只回答"哪条线是哪套离散", 不承担结论。放左下: 两条线都从左上走到右下,
    # 左下与右上各空出一块, 图例取左下: 右上留白, 不再填东西。
    # 第三条用中性灰的空心圆: 它代表的是"空心这种画法", 不是某一套离散, 所以
    # 不能沿用蓝或橙; 两条曲线上的环各自沿用本离散的 marker 形状。
    # 标签只写单元类型, 不写 2D/3D: 维度分类标签会把工作读成"分维度、有局限",
    # 而单元类型是必要的技术说明, 且已隐含维度(申报书全文的术语规避口径)。
    legend_handles = [
        Line2D([0], [0], color=C_BLUE, lw=2.0, ls="-", marker="o", ms=5.8,
               mec=SURFACE, mew=1.0, label="三角形网格"),
        Line2D([0], [0], color=C_ORANGE, lw=2.0, ls="--", marker="s", ms=5.8,
               mec=SURFACE, mew=1.0, label="四面体网格"),
        Line2D([0], [0], color=INK_2, lw=0.0, marker="o", ms=7.5, mfc="none",
               mew=1.4, label="Matrix-Free"),
    ]
    legend = ax.legend(handles=legend_handles, loc="lower left", fontsize=10.5,
                       frameon=True, framealpha=0.95, edgecolor=GRID,
                       handlelength=2.0, handletextpad=0.55, borderpad=0.4,
                       # y 锚点原为 0.10, 是给下方那行核验小字让位; 小字删掉后落回角上
                       labelspacing=0.3, bbox_to_anchor=(0.005, 0.02))
    legend.get_frame().set_linewidth(0.8)

    # 不在图面上写"P1 理论阶 2 · 收敛阶门禁 1.5"。图面上六个观测阶自己就朝 2 收,
    # 趋势不必再用一行小字复述; 门禁 1.5 在这张图上也没有几何位置(y 轴是误差,
    # 不是收敛阶)。
    # 2026-08-24 修正: 此处原写着这两个数"由图说明给出", 故图说明中"通过门禁
    # (下限 1.5)"那句"不可删减"。该前提已不成立 —— 申请书草稿的图 4 说明段整段
    # 删除了(六图一表里只有它带说明, 体例不一致; 且第 6 部分限 1000 字已严重超
    # 出), 现在申请书全篇不出现门禁 1.5。这是有意的: 1.5 是内部验收阈值, 评审不
    # 需要, 其事实源在 soptx 的 experiments/matrix_free_capability/
    # results_analysis.md(§2.3 的表与 :32 同样记着"门禁在图上没有载体")。
    panel_title(ax, "(a) 正确性")


def draw_panel_b(ax, dof, mem_asm, mem_mf, mem_base):
    """把图 2(b)"可计算规模"画进 ``ax``.

    纵轴是**扣掉解释器基线之后**的进程峰值内存。基线(0.158 GiB)是不随问题规模
    变化的常数项, 留在纵轴里只会把最粗档的两点压到几乎重合 —— 那是基线稀释造成
    的假象, 不是存储层级的差别。扣掉之后图上量到的比值与申请书正文里那句"约为显
    式组装的 3.1 倍"同源: 读者按最细档量得 3.0, 不会再量出 2.96 却读到正文写 3.0。

    **不画内存天花板线。** 本格的结论是"同一内存上限下可算规模约 3 倍", 依据是
    两条线扣基线后都是自由度的一次函数 —— 内存比与规模比互为倒数, 与上限取什么
    值无关, 天花板不参与论证。画上它却不画交点, 只会诱导读者自己延长两条线去找
    交点, 做的恰是正文声明不做的外推; 而真要画交点, EA 一侧需从实测的 5.59 GiB
    外推到 46.9 GiB(8.4 倍, 比 FA 的 2.8 倍远得多), 交点自由度随拟合口径在
    6.5~7.3 M 之间摆动(±12%), 不是一个能写死在图面上的数。**"落在一台具体机器
    上"由纵轴的绝对 GiB 承担, 不由那条线承担**, 所以删掉它不会让本格重新变回抽
    象的增长趋势。解释器基线那条点线同理删去: 已经扣掉了, 再画一条零线没有意义。

    参数:
        ax: 目标 ``Axes``.
        dof: 自由度数组.
        mem_asm: 显式组装的进程峰值内存, 单位 GiB(**未扣基线**, 本函数负责扣).
        mem_mf: matrix-free 的进程峰值内存, 单位 GiB(**未扣基线**, 同上).
        mem_base: 解释器基线, 单位 GiB.
    """
    # 只画两条线: 存储层级(EA/PA/UA)的细分是研究内容 2 的题目, 不是研究基础的
    # 展示对象; 本格只需回答"同一台机器上能算多大", 一个对比就够, 因此不用图例。
    asm = mem_asm - mem_base
    mf = mem_mf - mem_base

    # 标注贴着各自的线放, 不挂在端点上: 端点在图的两个角上, 合并图里每格只有约
    # 2.9 in 宽, 挂端点的标注不是撞上角注就是溢出右边界。两条线平行且相隔
    # log(3.0), 所以蓝线标在其上方、橙线标在其下方。两个标注**必须锚在同一档**:
    # 错开横坐标会让它们落到相近的高度(橙线在右一档的绝对值反而高于蓝线在左一
    # 档), 反倒撞在一起; 锚同一档时两者的间距就是两条线之间那 log(3.0)。
    series = [("显式组装", asm, C_BLUE, "o", 1, (0, 9), "bottom"),
              ("Matrix-Free", mf, C_ORANGE, "s", 1, (0, -9), "top")]
    for name, m, c, mk, ia, off, va in series:
        ax.loglog(dof, m, color=c, lw=2.2, marker=mk, ms=6.0,
                  mec=SURFACE, mew=1.2, zorder=4)
        ax.annotate(name, xy=(dof[ia], m[ia]), xytext=off,
                    textcoords="offset points", fontsize=11, color=c,
                    ha="center", va=va, fontweight="bold")

    # 规模角注已删(2026-08-27): 末档 1,594,323 自由度由申请书正文承担("算例实测
    # 规模达约 159 万自由度"), 图面不再重复; 与 (d) 一起去掉角注还避免了两格规模
    # 数字(159 万 / 82 万)在图面上与图 10 的 GPU 规模并置引发的口径追问。
    ax.set_xlabel("自由度数")
    ax.set_ylabel("扣基线进程峰值内存 (GiB)")
    ax.set_xlim(dof[0] / 2.4, dof[-1] * 2.6)
    ax.set_ylim(mf[0] / 2.6, asm[-1] * 1.5)
    ax.xaxis.set_major_locator(LogLocator(base=10.0, numticks=5))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_minor_formatter(NullFormatter())
    recessive_axes(ax, grid_axis="both")
    # 结论框已整段删(2026-08-28): 框里那句"同一内存上限下可算规模约为显式组装的
    # 3.1 倍"在申请书正文里逐字出现, 图面重复一遍不增信息; 而四格各配一个同款圆
    # 角框, 本身就是模板化排版最显眼的来源。比值仍可读: 两条线平行且相隔
    # log(3.0), 纵向间距就是它, 纵轴已扣基线, 量得到的与正文同源。
    # 上界随之由 2.8 倍收回 1.5 倍 —— 那 2.8 倍原是给框腾的地方。
    panel_title(ax, "(b) 可计算规模")


def draw_panel_mpi_strong(ax, ranks, speedup, efficiency, info):
    """把图 2(c)"进程级扩展"画进 ``ax``. 全部为实测数据.

    **画法沿用四格的共同语法**: 双对数、实测实线 + 贴线标注、灰虚线画那条不是
    量出来的参考线、角注收在空白角。与 (d) 的差别只有横轴的物理含义 —— 那是
    内容决定的, 不是风格漂移(见 data_mpi_strong 的说明)。

    **理想线必须画。** 只画一条上升的实测曲线, 读者看到的是"加速了", 看不到
    "离该有的还差多少"; 强扩展这一格的结论恰恰在那个缺口里。理想线是 y = x,
    不是量出来的, 故与 (d) 的厂商标称线同样用灰虚线, 与实测实线在视觉上分开。

    **不画本地核那条线, 也不写同步占比。** 本地核加速(3.85 倍)与总加速(3.69
    倍)只差 4%, 两条线在这张小图上会糊在一起; 而"同步仅占 16%"是内部口径 ——
    分项对 rank 取 max 的上界、且含负载不均的等待 —— 放进申请书图面反而引出
    追问。两者都收进内部拆解图 ``build_fig2_panel_c_internal``(不进申请书, 供
    soptx 的 results_analysis.md 引用)。诊断句"瓶颈是节点内访存带宽"也不上图
    —— 它写在申请书正文(研究基础第 1 条)里。**本格图面不留角注**: 连"并行效率
    23%"也删了, 那道落差图上直接看得见, 写出来只是替读者心算一遍(见函数体注释)。

    参数:
        ax: 目标 ``Axes``.
        ranks: 进程数数组.
        speedup: 相对单进程的加速比.
        efficiency: 并行效率, **不上图面**, 只供 [图说明核对] 打印与内部拆解图.
        info: ``data_mpi_strong`` 返回的标量字典.
    """
    ideal = ranks
    ax.loglog(ranks, ideal, color=INK_2, lw=1.3, ls=(0, (5, 3)), zorder=3)
    ax.annotate("理想线性", xy=(ranks[-2], ideal[-2]), xytext=(-4, 6),
                textcoords="offset points", fontsize=10, color=INK_2,
                ha="right", va="bottom")
    ax.loglog(ranks, speedup, color=C_BLUE, lw=2.2, marker="o", ms=6.0,
              mec=SURFACE, mew=1.2, zorder=4)
    # 标注锚在 index 2: 该档实测与理想已拉开约 1.6 倍, 标签向下偏不会压到理想线;
    # 锚在更左的档上两条线几乎重合(那正是扩展还没掉下来的一端), 标注必然打架。
    # 锚在 index 3(P=8)而不是 index 2: 曲线在 y 约 3.4 处已压平, 其正下方到纵轴
    # 下界之间是整块空白; 锚在 index 2 时标签会掉进右下那块曾放结论框的位置(第一
    # 版就是这么撞的), 而角注已挪到左上, 右下这块空白正好留给它。
    ax.annotate("实测 CG 求解", xy=(ranks[3], speedup[3]), xytext=(0, -11),
                textcoords="offset points", fontsize=11, color=C_BLUE,
                ha="center", va="top", fontweight="bold")

    # 横轴只写"MPI 进程数"。每进程锁定单线程(OMP_NUM_THREADS=1)这件事曾写在括号里,
    # 但 (a)(b)(d) 三格的横轴都是干净的一句话, 只有本格挂注释, 四格并排时毛糙; 且
    # "线程层锁死"是行话, 评审未必解码。该配置已移入申请书的"图 4 说明"段 —— 删这
    # 个括号前请确认那段还在, 否则 OMP_NUM_THREADS=1 会从全文消失, 而它正是本格能
    # 干净归因到进程层的前提(不锁的话 P=1 开 32 条 BLAS 线程、P=16 超订, 那个比值
    # 是"进程 x 线程"的混合物)。
    ax.set_xlabel("MPI 进程数")
    ax.set_ylabel("相对单进程的求解加速比")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=2)
    ax.set_xlim(ranks[0] / 1.5, ranks[-1] * 1.5)
    # 上界给到理想线终点的 1.18 倍。这个余量一路是为角注留的(左上三行时 2.4 倍,
    # 一行时 1.7 倍, 挪进落差里后 1.35 倍); 角注删净后上方只剩理想线终点那个端
    # 点和"理想线性"标注(锚 P=8、上偏 6 pt)要露出来, 1.18 倍够, 再高就是纯留白。
    ax.set_ylim(speedup.min() / 1.6, ideal[-1] * 1.18)
    ax.set_xticks(ranks)
    ax.set_yticks([1, 2, 4, 8, 16])
    ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.xaxis.set_minor_locator(NullLocator())
    ax.yaxis.set_minor_locator(NullLocator())
    recessive_axes(ax, grid_axis="both")
    # 本格**不留任何角注**(2026-08-28 删)。删的是"并行效率 23%": 它描述的是
    # P=16 处实测点(3.69)与理想线(16)之间那道落差, 而那道落差图上直接看得见 ——
    # 角注只是替读者把 3.69/16 心算了一遍。申请书正文那句"加速偏离理想线性主要
    # 受单节点访存带宽限制而非通信开销"已经把"效率掉下来了 + 为什么"都说了,
    # 图面再写一个百分数是第三遍。同段的"16 进程加速 3.69 倍"更是正文原话。
    # 落点曾三易(右下 -> 左上 -> 末档落差里), 每一版都要跟理想线抢地方, 这本身
    # 就是"这一格并不需要它"的证据。
    # info 里的 sync_share 与 efficiency 都不上图, 只进 [图说明核对] 与内部拆解图。
    panel_title(ax, "(c) 进程级扩展")


def draw_panel_device_speedup(ax, dof, t_cpu, t_gpu, gap):
    """把图 2(d)"单卡加速"画进 ``ax``. 全部为实测数据.

    **2026-08-24 由 (c) 移到 (d)**, 原"有效访存带宽"那一格撤销。带宽结论曾
    短暂并入本格结论框, 同日又撤下: "达标称的 43%"是诊断而非成绩 —— 分子是
    下界、分母是物理上达不到的标称, 两头都要口径说明 —— 放在展示成绩的图面上,
    先读出来的是"没做好"。它曾改归申请书正文(研究基础第 1 条, 靠"量化起点"式的
    收尾护着), 同日再撤: 那一条已经太满, 且这种收尾属于立项论证, 不该由成绩栏兼
    职。现在唯一事实源是 soptx 的 results_analysis.md §5.4 / 表 c-2; 图面角注只
    留一行实测断言, 与 (c) 的一行对称。

    画法刻意抄 (b): 同样的双对数、同样的横轴、同样的"两条线 + 贴线标注"。
    四格共用一套视觉语法, 读者一眼看出是同一批算例的不同侧面, 不必比对轴标签。

    **角注只留解相对差。** 倍数(最细档约 16 倍)不写: 两条曲线末档的纵向间距就
    是它, 图上量得到, 申请书正文也逐字写过。解相对差不同 —— 换了设备, 加速比的
    第一质疑就是"是不是两边算得不一样", 这一条曲线本身答不了, 正文也没写, 只能
    由图面承担, 就贴在倍数被量出来的同一眼里。

    **不标逐档加速比。** 四个倍数(0.35 / 1.19 / 8.04 / 16.08)标满会盖住曲线,
    而且逐档数值本就随机器变; 图面只需给出形状(小规模 GPU 不划算、大规模拉开)
    和最细档那一个可引用的倍数, 逐档表在 soptx 的 results_analysis.md §4。

    参数:
        ax: 目标 ``Axes``.
        dof: 自由度数组, 与 (b) 同源.
        t_cpu: CPU 单次 CG 求解耗时, 单位 s.
        t_gpu: 单块 GPU 单次 CG 求解耗时, 单位 s.
        gap: 四档中最大的两侧解相对差, 写进图面角注.
    """
    # 标注锚在同一档(index 2): 该档两条线相隔约 4.6 倍, 上下各偏 9 pt 不会撞;
    # 锚在更粗的档上两线几乎重合(那正是 GPU 不划算的一端), 标注必然打架。
    series = [("CPU", t_cpu, C_BLUE, "o", (0, 9), "bottom"),
              ("单卡 GPU", t_gpu, C_ORANGE, "s", (0, -9), "top")]
    for name, t, c, mk, off, va in series:
        ax.loglog(dof, t, color=c, lw=2.2, marker=mk, ms=6.0,
                  mec=SURFACE, mew=1.2, zorder=4)
        ax.annotate(name, xy=(dof[2], t[2]), xytext=off,
                    textcoords="offset points", fontsize=11, color=c,
                    ha="center", va=va, fontweight="bold")

    # 规模角注已删(2026-08-27): 82.4 万(823,875)由申请书正文"在 823,875 自由度的
    # 同一问题上"承担, 图面不再重复, 也不与图 10 的 GPU 规模并置(口径不同,
    # fp64 通用四面体链 vs fp32 结构化 hex 链, 见 cases.toml 数据组 c 的注记)。
    ax.set_xlabel("自由度数")
    ax.set_ylabel("单次求解耗时 (s)")
    ax.set_xlim(dof[0] / 2.4, dof[-1] * 2.6)
    # 上界随角注行数增减: 每加一行要多让一档纵向空间, 否则字底会压到 CPU 曲线
    # 中段并盖掉贴线的"CPU"标注。四行时曾放宽到 12.0, 两行 4.5, 现在一行, 2.4。
    ax.set_ylim(min(t_cpu.min(), t_gpu.min()) / 2.6, t_cpu.max() * 2.4)
    ax.xaxis.set_major_locator(LogLocator(base=10.0, numticks=5))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_minor_formatter(NullFormatter())
    recessive_axes(ax, grid_axis="both")
    # 角注放**左上**, 与 (b) 同因: 11 pt 的"单卡 GPU"标注伸进了原先右下框的范围。
    # 2026-08-28 只留解相对差一行: "最细档快约 16 倍"在正文里逐字写过, 且两条
    # 曲线末档的纵向间距就是它, 图上量得到; 而"两边是不是算得不一样"这个换设备
    # 后的第一质疑, 曲线本身答不了, 必须由图面这一行答 —— 留的正是这一行。
    # 分母同样不写: 两条曲线各自贴着"CPU"/"单卡 GPU"标注, 比的是谁一眼可见。
    # 2026-08-24 更新归属: 此处原写着"同后端、16 线程"与"(c)(d) 分属两个并行层
    # 级、加速比不可相乘"由申请书的图 4 说明逐字承担 —— 该说明段已整段删除(六图
    # 一表里只有它带说明)。现在"16 线程"写在申请书正文的分母里, "不可相乘"归
    # soptx 的 results_analysis.md; 图面不承担这两条。
    ax.text(0.03, 0.97, f"两侧解相对差 < {gap:.0e}",
            transform=ax.transAxes, fontsize=10.0, color=INK, ha="left",
            va="top")
    panel_title(ax, "(d) 单卡加速")


def build_fig2_panels(cv, mem, mpi, bd):
    """把图 2 的四格各自画进一张单独的画布, 供按图面分格的文档逐格引用.

    与合并图共用同一批 ``draw_panel_*``, 因此内容与样式不可能漂移; 唯一的差别
    是画布形状 —— 合并图 2x2 每格分到 4.0 in 宽, 单格图给到整张 4.6 in。

    先前从合并图上按包围盒切图的做法已废弃: 切图必然继承合并图的格子形状, 而
    格子太窄正是当初要解决的问题。

    参数:
        cv: ``data_convergence()`` 的返回值.
        mem: ``data_peak_memory()`` 的返回值.
        mpi: ``data_mpi_strong()`` 的返回值.
        bd: ``data_device_speedup()`` 的返回值.

    返回:
        写出的文件路径列表, 顺序为 (a)(b)(c)(d).
    """
    dof, mem_asm, mem_mf, mem_base, mem_ceiling = mem
    ranks, speedup, efficiency, mpi_info = mpi
    dof_c, t_cpu, t_gpu, gap_c = bd
    # 切图文件名 fig08_matrix_free_validation_panel_{a,b,c,d}
    # 按**图面位置**命名, 不按内容;
    # 2026-08-24 换版式后 panel_c 的内容已由 GPU 加速变成 MPI 强扩展, panel_d
    # 由带宽变成 GPU 加速。申请书只引合并图, 不单引分格图, 故无需改引用。
    panels = (
        ("a", lambda ax: draw_panel_a(ax, cv)),
        ("b", lambda ax: draw_panel_b(ax, dof, mem_asm, mem_mf, mem_base)),
        ("c", lambda ax: draw_panel_mpi_strong(ax, ranks, speedup, efficiency,
                                               mpi_info)),
        ("d", lambda ax: draw_panel_device_speedup(ax, dof_c, t_cpu, t_gpu,
                                                   gap_c)),
    )
    paths = []
    for label, draw in panels:
        # (c) 曾是占位, 这里为它的红字脚注在底部留过白, 也打过单格水印;
        # 该格已改为实测(见 data_device_speedup), 两者一并删除。
        fig = plt.figure(figsize=FIG2_PANEL_SIZE, dpi=200,
                         constrained_layout=True)
        ax = fig.subplots(1, 1)
        draw(ax)
        path = OUT_FIG2_PANEL.format(label)
        path_svg = OUT_FIG2_PANEL_SVG.format(label)
        fig.savefig(path, bbox_inches="tight", pad_inches=0.14)
        fig.savefig(path_svg, bbox_inches="tight", pad_inches=0.14)
        paths.append(path)
        print(f"[out] {path}\n[out] {path_svg}")
        plt.close(fig)
    return paths


def build_fig2_panel_c_internal():
    """(c) 的内部拆解图: 不进申请书, 供 soptx 的 results_analysis.md 引用.

    图面版 (c) 的角注只保留"并行效率"一行, 诊断句"瓶颈是节点内访存带宽"
    写在申请书正文里, 支撑数据收在这里:
      (c-1) 总加速与本地核加速画进同一坐标系 —— 两线几乎重合(3.69 vs 3.85 倍),
            效率损失几乎全部发生在本地核内部, 通信不是瓶颈;
      (c-2) 单次 MatVec 的分解(表 d-2 的图形化)。⚠️ 三个分项各自对 rank 取最大
            值再按样本取中位数, 不同项的 max 可能来自不同进程, 堆叠高度可超过
            实测 MatVec 总计(黑色短横线) —— 该口径系统性高估同步, "通信不是
            瓶颈"因此是保守结论。同步计时为阻塞归约的墙钟时间, 含等待。

    异常:
        RuntimeError: 快照里进程级强扩展仍是占位.
    """
    panel = load_fig2_snapshot()["panels"]["d"]
    if panel.get("status") != "measured":
        raise RuntimeError("快照里进程级强扩展仍是占位, 内部拆解图无从画起。")
    ranks = np.array(panel["ranks"], dtype=float)
    speedup = np.array(panel["speedup"], dtype=float)
    kernel = np.array(panel["local_kernel_seconds"], dtype=float)
    matvec = np.array(panel["matvec_seconds"], dtype=float)
    sync_in = np.array(panel["input_sync_seconds"], dtype=float)
    sync_out = np.array(panel["output_sync_seconds"], dtype=float)
    kernel_speedup = kernel[0] / kernel
    sync_share = (sync_in + sync_out) / matvec

    fig = plt.figure(figsize=(9.2, 3.8), dpi=200, constrained_layout=True)
    ax1, ax2 = fig.subplots(1, 2)

    # ---- (c-1) 两条加速曲线 ----
    ax1.loglog(ranks, ranks, color=INK_2, lw=1.3, ls=(0, (5, 3)), zorder=3)
    ax1.annotate("理想线性", xy=(ranks[-2], ranks[-2]), xytext=(-4, 6),
                 textcoords="offset points", fontsize=9.5, color=INK_2,
                 ha="right", va="bottom")
    ax1.loglog(ranks, speedup, color=C_BLUE, lw=2.2, marker="o", ms=5.5,
               mec=SURFACE, mew=1.1, zorder=4)
    ax1.loglog(ranks, kernel_speedup, color=C_ORANGE, lw=1.8, ls="--",
               marker="s", ms=4.8, mec=SURFACE, mew=1.0, zorder=4)
    ax1.annotate(f"CG 求解 {speedup[-1]:.2f}x", xy=(ranks[-1], speedup[-1]),
                 xytext=(2, -13), textcoords="offset points", fontsize=9.5,
                 color=C_BLUE, ha="right", va="top", fontweight="bold")
    ax1.annotate(f"本地核 {kernel_speedup[-1]:.2f}x",
                 xy=(ranks[-1], kernel_speedup[-1]), xytext=(2, 10),
                 textcoords="offset points", fontsize=9.5, color=C_ORANGE,
                 ha="right", va="bottom", fontweight="bold")
    ax1.set_xlabel("MPI 进程数")
    ax1.set_ylabel("相对单进程加速比")
    ax1.set_xscale("log", base=2)
    ax1.set_yscale("log", base=2)
    ax1.set_xlim(ranks[0] / 1.5, ranks[-1] * 1.5)
    ax1.set_ylim(speedup.min() / 1.35, ranks[-1] * 1.6)
    ax1.set_xticks(ranks)
    ax1.set_yticks([1, 2, 4, 8, 16])
    ax1.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax1.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax1.xaxis.set_minor_locator(NullLocator())
    ax1.yaxis.set_minor_locator(NullLocator())
    recessive_axes(ax1, grid_axis="both")
    panel_title(ax1, "(c-1) 两条加速曲线几乎重合")

    # ---- (c-2) MatVec 分解 ----
    x = np.arange(len(ranks))
    k_ms = kernel * 1e3
    in_ms = sync_in * 1e3
    out_ms = sync_out * 1e3
    mv_ms = matvec * 1e3
    ax2.bar(x, k_ms, 0.62, color=C_BLUE, label="本地核")
    ax2.bar(x, in_ms, 0.62, bottom=k_ms, color=C_ORANGE_L, label="输入同步")
    ax2.bar(x, out_ms, 0.62, bottom=k_ms + in_ms, color=C_ORANGE,
            label="输出同步")
    # 实测 MatVec 总计画成黑色短横线; 堆叠高度超过它的部分就是"分项各自对 rank
    # 取 max"的重叠计数 —— 差距本身是口径信息, 不抹平。
    ax2.hlines(mv_ms, x - 0.38, x + 0.38, color=INK, lw=1.4, zorder=5,
               label="MatVec 实测总计")
    for xi, total, share in zip(x, k_ms + in_ms + out_ms, sync_share):
        ax2.annotate(f"同步 {share * 100:.1f}%", xy=(xi, total), xytext=(0, 4),
                     textcoords="offset points", fontsize=8.4, color=INK_2,
                     ha="center", va="bottom")
    ax2.set_xticks(x)
    ax2.set_xticklabels([str(int(r)) for r in ranks])
    ax2.set_xlabel("MPI 进程数")
    ax2.set_ylabel("单次 MatVec 耗时 (ms)")
    ax2.set_ylim(0, mv_ms[0] * 1.18)
    ax2.legend(loc="upper right", fontsize=8.6, frameon=False)
    recessive_axes(ax2, grid_axis="y")
    panel_title(ax2, "(c-2) MatVec 分解（上界口径）")

    fig.text(0.01, -0.02,
             "内部图，不进申请书。分项各自对 rank 取最大值再按样本取中位数，"
             "三项之和可超过实测总计（黑短线）；同步计时为阻塞归约的墙钟时间，"
             "含负载不均的等待。数据同表 d-2。",
             fontsize=8.2, color=INK_2, ha="left", va="top")

    os.makedirs(os.path.dirname(OUT_FIG2_INTERNAL), exist_ok=True)
    path = OUT_FIG2_INTERNAL
    path_svg = OUT_FIG2_INTERNAL_SVG
    fig.savefig(path, bbox_inches="tight", pad_inches=0.14)
    fig.savefig(path_svg, bbox_inches="tight", pad_inches=0.14)
    print(f"[out] {path}")
    print(f"[out] {path_svg}")
    plt.close(fig)



def build_fig2():
    """图 2: 四格分别回答"对不对 / 能算多大 / 切得开吗 / 搬得动吗"。

    这是研究基础栏目的四个必答问题, 按评审的阅读顺序排:
      (a) 排除造假——离散正确性是入场券, 因此**只给一格, 不扩张**;
      (b) 排除吹牛——规模能力落到一块具体硬件上, 且**止于实测最大规模**;
      (c) 证明切得开——同一算子按区域分解切到多个 MPI 进程上仍是同一个代数问题
          (五档 CG 迭代数逐档相同), 且能拿到实测加速; 效率随进程数下降的位置本
          身是结论, 它指向节点内访存带宽, 不是通信;
      (d) 证明搬得动——同一算子搬到单块 GPU 上的加速, 是把研究基础焊到研究内容
          2 的那一格; 角注只给解相对差, "有效访存带宽只到标称四成出头"
          那条诊断不上图面, 理由见 draw_panel_device_speedup。多卡扩展同属研究
          内容 2, 不在这里给。

    ⚠️ **(c) 与 (d) 是两个不同的并行层级**: (c) 切进程(MPI), (d) 切设备内(SIMT)。
    两格的加速比**不可相乘、不可互相外推**, 分母也不同——(c) 的分母是单进程,
    (d) 的分母是同后端 16 线程 CPU。引用任一倍数时必须连分母一起写: 申请书正文
    已按此写(图 4 说明段已删, 不再承担此事), "不可相乘"这条归 soptx 的
    results_analysis.md。层级定义见 dut-postdoc 的
    concepts/gpu-hpc/parallel-levels.md。

    **2026-08-24 换版式**: 原 (c)(GPU 加速)移到 (d), 原 (d)(有效访存带宽)不再单
    占一格(其结论曾短暂并进 (d) 的结论框, 同日撤下), 腾出的 (c) 给进程级强扩展。
    理由是带宽那一格
    本就是 GPU 那一格耗时的换算而不是新实验, 一句话能说完; 而进程级强扩展是一批
    独立运行的实测, 没有图面位置就只能停在文档里。逐档带宽换算表仍在 soptx 的
    results_analysis.md 表 c-2。

    四格**全部为实测**, 数值同读一份快照 ``FIG2_SNAPSHOT``: (a)(b) 读
    ``panels.a/b``, (c) 读 ``panels.d``(该键名是"第四组数据"的标识, 不是图面位
    置——两者在这次改版后正好错开, 别按字母对号入座), (d) 读 ``panels.c``。
    GPU 那一格在 2026-08-22 之前是占位并带斜向水印, 注册 ``c-dev-n*`` 四个 case
    测出实测值后水印已删。

    **2026-08-22 由 1x3 改 2x2。** 1x3 时每格印到纸上只有 5.07 cm 宽, 加上第四
    格后横向三等分变四等分只会更窄; 2x2 每格 7.6 cm, 绘图框从 3.6 cm 放大到约
    7 cm。注意换版式**不会**改变印刷字号 —— 缩放比 DOCX_WIDTH_IN / FIG_WIDTH_IN
    只由图宽决定, 与子图数量无关; 版式只是腾出空间, 字号是同一次改动里单独抬的。

    四格的画法在 draw_panel_a/b/c/d 里, 合并图与 build_fig2_panels 的单格图共用
    同一批函数, 只是画布不同; 合并图是进申请书的那一张, 四格是一个论证的四步,
    不拆。

    小标题取名规则: 四个面板标题与图注的图题**逐词一致** —— 正确性 / 可计算
    规模 / 进程级扩展 / 单卡加速, 见申请书草稿 `80th-2026-application-draft.md`
    的图 4 图题。

    这条规则改过两次。最早是"正确性验证 / 可计算规模 / 并行瓶颈"; 2026-08-22
    改成口语记号(算子对 / 能算大 / 能扩展 / 能加速), 理由是四格是一条论证链而
    非四个并列指标, 短记号便于扫读; 2026-08-24 改回规范词组, 因为图题那一行本
    来就写着规范说法, 图面与图题各说一套才是真正的不规范, 而扫读的便利并不值
    得付这个代价。**改标题必须连图题一起改**, 否则又会分叉。

    字数不是约束: 标题 13 pt, 每格轴框约 3.2 in, 约放得下 15 个汉字。

    两条老约束仍然成立:
      * **不重复轴标签**。(b) 的 y 轴已写"扣基线进程峰值内存 (GiB)", 标题说的
        是"可计算规模" —— 轴说不出来的那一半; (c)(d) 同理。
      * **不写结论**。标题只说"这一格在看什么", 不说结论是什么 —— 结论由曲线
        本身与贴线标注承担, 只有 (d) 的解相对差是曲线答不了的, 留一行角注;
        标题重复一遍只会挤掉可读的字号。
    """
    cv = data_convergence()
    dof, mem_asm, mem_mf, mem_base, mem_ceiling = data_peak_memory()
    ranks, speedup, efficiency, mpi_info = data_mpi_strong()
    dof_c, t_cpu, t_gpu, gap_c = data_device_speedup()
    _, bw_cpu, bw_gpu, bw_spec = data_bandwidth()

    # 高度 7.0 in: 印到 15.2 cm 宽时纸面约 13.3 cm 高, 每格 7.6 x 6.65 cm。
    # 两行都用同一高度, 因为四格共用一套双对数版式, 行高不等会让上下两格的
    # 同一段横轴对不齐 —— (b)(d) 同轴(自由度), 对齐是它们能斜向对读的前提。
    # (c) 换版式后横轴改为进程数, 不再与 (b)(d) 同轴; 那是内容决定的, 强行统一
    # 只会造出一个没有意义的坐标系(见 data_mpi_strong)。
    fig = plt.figure(figsize=(FIG_WIDTH_IN, 7.0), dpi=200, constrained_layout=True)
    # 脚注已删, 不再为它在底部留白(图 3 那处同样写法仍要留, 别一起改)。
    fig.get_layout_engine().set(rect=(0.0, 0.0, 1.0, 1.0))
    # 1x3 时曾按 1.12 : 1 : 0.98 分宽, 为的是让 (a) 的五个 "1/N" 刻度标签排得开;
    # 2x2 下每格有 4.0 in, 那五个标签已不再挤, 故回到等宽 —— 不等宽会让左右两列
    # 的纵轴错位, 而四格的纵轴标题长度本就不同, 错位比拥挤更难看。
    axes = fig.subplots(2, 2)
    ax_a, ax_b = axes[0]
    ax_c, ax_d = axes[1]

    draw_panel_a(ax_a, cv)
    draw_panel_b(ax_b, dof, mem_asm, mem_mf, mem_base)
    draw_panel_mpi_strong(ax_c, ranks, speedup, efficiency, mpi_info)
    draw_panel_device_speedup(ax_d, dof_c, t_cpu, t_gpu, gap_c)

    # 图底红字脚注删掉了: 数据出处由申请书正文的图说明承担, 图面再写一份必然
    # 和正文失同步, 插进 DOCX 后也只是碍眼的红字。GPU 那一格轴内那道"占位示意
    # 数据"斜向水印也一并删除 —— 四格现已全部实测, 留着就是假警报。
    # SVG 给 Markdown/Obsidian 看(缩放不糊), PNG 给 DOCX 用(python-docx 只认位图)。
    for path in (OUT_FIG2, OUT_FIG2_SVG):
        fig.savefig(path, bbox_inches="tight", pad_inches=0.14)
        print(f"[out] {path}")
    plt.close(fig)

    # 把申请书图说明逐字引用、但图面上不画的那几个数打出来。图说明是这些数字在
    # 定稿里的唯一载体(图面上的核验小字已删), 所以每次重绘都要有机会对一眼。
    print(f"[图说明核对] EA/FA 解相对差 2D {cv['gap_2d']:.0e} / 3D {cv['gap_3d']:.0e}"
          f" · 比对档 2D {cv['dof_ea_coarse_2d']:,} / 3D {cv['dof_ea_coarse_3d']:,} 自由度"
          f" · 门禁下限 {cv['gate']}")
    # 天花板不再画进 (b), 但图说明若要提"这台机器有多大内存"仍需引用, 故在此打出。
    print(f"[图说明核对] (b) 纵轴已扣基线 {mem_base:.3f} GiB; 本机可用内存 "
          f"{mem_ceiling:.2f} GiB 未画入图面(不参与可算规模约 3 倍的论证)")
    # (c) 的逐档加速比不上图(会盖住曲线), 但图说明与正文要引, 故在此打出。
    # (c) 的进程级强扩展: 图面只标最大档一个数, 效率与迭代数由图说明承担。
    eff = " / ".join(f"{v * 100:.0f}%" for v in efficiency)
    print(f"[图说明核对] (c) 逐档加速比 "
          + " / ".join(f"{v:.2f}" for v in speedup)
          + f"; 并行效率 {eff}; 五档 CG 迭代数均为 {mpi_info['iterations']}"
          f"; 本地核 1->{int(ranks[-1])} 进程仅快 {mpi_info['kernel_speedup']:.2f} 倍")
    dev_speedup = " / ".join(f"{c / g:.2f}" for c, g in zip(t_cpu, t_gpu))
    print(f"[图说明核对] (d) 逐档加速比 {dev_speedup}; 最大解相对差 {gap_c:.1e}"
          f" (门禁 1e-9)")
    # (d) 的逐档带宽图上只标了最细档一个数, 但图说明与 results_analysis.md
    # 表 c-2 要逐档引用, 故在此打出以便对账。
    band_cpu = " / ".join(f"{v:.1f}" for v in bw_cpu)
    band_gpu = " / ".join(f"{v:.1f}" for v in bw_gpu)
    print(f"[图说明核对] 有效访存带宽 GB/s（不上图面，只供正文与 results_analysis.md 引用）: "
          f"CPU {band_cpu}; GPU {band_gpu}"
          f"; 最细档达标称 {bw_spec:.0f} 的 {bw_gpu[-1] / bw_spec * 100:.0f}%")
    build_fig2_panels(cv, (dof, mem_asm, mem_mf, mem_base, mem_ceiling),
                      (ranks, speedup, efficiency, mpi_info),
                      (dof_c, t_cpu, t_gpu, gap_c))


# ==========================================================================
# 图 3 —— PIML 局部响应恢复精度（储备二）
# ==========================================================================

def draw_panel_3a(ax, eq_data, label="a"):
    """(a) 缩聚算子正确性: 静力缩聚解与全装配直解的相对差.

    条目数由 ``data_condensation_equivalence`` 的归并结果决定(现为两条)。条目少时
    沿用四条时的留白和字号, 两个棒棒糖会孤零零挂在上半格、下半格全空, 与同排的
    (b) 疏密失衡; 因此 ``n <= 2`` 时收紧 y 留白并放大标记与字号, 让两条各占半格。
    这只改观感, 不改任何数值。
    """
    eq_labels, eq_vals, eq_colors, eq_gate = eq_data
    n = len(eq_vals)
    few = n <= 2
    stem_lw = 2.2 if few else 1.6
    dot_ms = 10.5 if few else 8.0
    val_fs = 10.2 if few else 8.6
    y = np.arange(n)
    x_left = 8.0e-14
    for yi, v, c in zip(y, eq_vals, eq_colors):
        ax.plot([x_left, v], [yi, yi], color=c, lw=stem_lw, alpha=0.55, zorder=3)
        ax.plot([v], [yi], marker="o", ms=dot_ms, color=c, mec=SURFACE, mew=1.2,
                zorder=4)
        ax.annotate(f"{v:.2e}", xy=(v, yi), xytext=(9, 0),
                    textcoords="offset points", fontsize=val_fs, color=INK,
                    ha="left", va="center", zorder=5,
                    bbox=dict(boxstyle="round,pad=0.16", fc=SURFACE,
                              ec="none", alpha=0.92))

    ax.set_xscale("log")
    ax.set_xlim(x_left, 1.2e-11)
    # few: 上下各留半格, 两条正好落在 1/4 与 3/4 高度, 均分整格
    ax.set_ylim(-0.5, n - 0.5) if few else ax.set_ylim(-0.78, n - 0.38)
    ax.set_yticks(y)
    ax.set_yticklabels(eq_labels)
    ax.set_xlabel("与全装配直解的相对差")
    ax.xaxis.set_major_locator(LogLocator(base=10.0, numticks=4))
    ax.xaxis.set_minor_formatter(NullFormatter())
    recessive_axes(ax, grid_axis="x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    if few:
        ax.tick_params(axis="y", labelsize=12.0)
    ax.tick_params(axis="x", labelsize=10)
    panel_title(ax, p3_title(label, "子结构缩聚正确性"))


def draw_panel_3b(ax, rt, label="b"):
    """(b) 二阶误差压缩机理: 受控扰动扫描双对数折线图."""
    ax.loglog(rt["eps_n"], rt["eps_k"], color=INK_2, lw=1.6, ls="-", zorder=4)
    ax.annotate(f"受控扰动扫描\n斜率 {rt['slope']:.2f}",
                xy=(rt["eps_n"][3], rt["eps_k"][3]), xytext=(7, -2),
                textcoords="offset points", fontsize=8.2, color=INK_2,
                ha="left", va="top", linespacing=1.45)

    ax.plot([rt["net_n"], rt["net_n"]], [3e-9, rt["net_k"]], color=C_BLUE,
            lw=1.0, ls=":", alpha=0.85, zorder=3)
    ax.plot([rt["net_n"]], [rt["net_k"]], marker="*", ms=15.0, color=C_BLUE,
            mec=SURFACE, mew=1.0, zorder=6)
    ax.annotate(f"实测网络点\n$\\varepsilon_K = {rt['net_k'] * 100:.2f}\\%$",
                xy=(rt["net_n"], rt["net_k"]), xytext=(11, -3),
                textcoords="offset points", fontsize=8.6, color=C_BLUE,
                ha="left", va="top", fontweight="bold", linespacing=1.45)
    ax.text(rt["net_n"], 4.2e-9, f"$\\varepsilon_N = {rt['net_n'] * 100:.2f}\\%$",
            fontsize=8.2, color=C_BLUE, ha="center", va="bottom")

    ax.set_xlabel(r"形函数相对误差 $\varepsilon_N$", fontsize=FIG3_LABEL_FS)
    ax.set_ylabel(r"缩聚刚度相对误差 $\varepsilon_K$", fontsize=FIG3_LABEL_FS)
    ax.set_xlim(6.0e-5, 0.62)
    ax.set_ylim(3.0e-9, 0.32)
    ax.xaxis.set_major_locator(LogLocator(base=10.0, numticks=5))
    ax.yaxis.set_major_locator(LogLocator(base=10.0, numticks=5))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_minor_formatter(NullFormatter())
    recessive_axes(ax, grid_axis="both")
    ax.tick_params(axis="x", labelsize=10)
    panel_title(ax, p3_title(label, "变分构造二阶误差响应"))


def draw_panel_3c(ax, sol_data, label="c"):
    """全局结构求解精度: 端到端有限元求解实测 (FullMBBBeam2d).

    两条路线不靠图例区分, 而是把符号直接写在最上一组柱旁: 缩到 DOCX 版心后本格净宽
    只有 2.2 in, 图例框摆在哪都压住数据; 且四组柱的配色与上下次序完全一致, 认过一组
    即可类推, 图例是纯冗余。与图 8 的曲线内联标注同一做法。
    """
    labels, piml_vals, direct_vals = sol_data
    # 逆序排列, 使第一行 (最上方) 为局部刚度 (5.83%), 从微观到宏观顺次向下
    labels = list(reversed(labels))
    piml_pct = np.array(list(reversed(piml_vals))) * 100
    direct_pct = np.array(list(reversed(direct_vals))) * 100

    y = np.arange(len(labels))
    height = 0.36
    top = len(y) - 1  # 只有最上一组带符号说明

    # 分组水平柱状图: 浅灰 (预测子结构刚度) 在上, 黑 (预测子结构形函数) 在下
    ax.barh(y + height / 2, direct_pct, height, color=C_ORANGE,
            edgecolor=SURFACE, linewidth=1.2, zorder=3)
    ax.barh(y - height / 2, piml_pct, height, color=C_BLUE,
            edgecolor=SURFACE, linewidth=1.2, zorder=3)

    for yi, vp, vd in zip(y, piml_pct, direct_pct):
        tag_d = r"  $\widehat{\mathbf{K}}_s$" if yi == top else ""
        tag_p = (r"  $\widetilde{\mathbf{K}}_s(\widehat{\mathbf{N}})$"
                 if yi == top else "")
        ax.text(vd + 0.15, yi + height / 2, f"{vd:.2f}%{tag_d}", va="center",
                ha="left", fontsize=8.2, fontweight="bold", color=C_ORANGE,
                zorder=5)
        ax.text(vp + 0.15, yi - height / 2, f"{vp:.2f}%{tag_p}", va="center",
                ha="left", fontsize=8.2, fontweight="bold", color=C_BLUE,
                zorder=5)

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8.4)
    ax.set_xlabel("全局求解相对误差 (%)", fontsize=FIG3_LABEL_FS)
    # 上限从 8.6 放到 10.4: 最上一组的数值后面还要接符号说明, 短了会顶到轴框
    ax.set_xlim(0, 10.4)
    ax.set_xticks([0, 2.0, 4.0, 6.0])
    ax.set_ylim(-0.65, len(y) - 0.35)
    recessive_axes(ax, grid_axis="x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    panel_title(ax, p3_title(label, "全局结构求解精度"))


def draw_panel_3d(ax, pol_data, label="d"):
    """PIML 批量缩聚 GPU 硬件加速: 耗时随子结构数变化 (PIML CPU vs PIML GPU).

    与 (c) 同理去图例、改内联标注; 加速跨度的文字也去掉圆角白底框 —— 图例、端点数值、
    带框注的双箭头说的是同一件事, 而把结论写进图面是幻灯片而非论文图的语汇。只标末档
    耗时, 首档耗时留给正文。
    """
    n_subs, t_cpu, t_gpu, speedup, device = pol_data
    x = np.arange(len(n_subs))

    # 1. 浅灰背景阴影展示加速跨度
    ax.fill_between(x, t_gpu, t_cpu, color=C_GREEN_L, alpha=0.55, zorder=1)

    # 2. 耗时折线 (对数刻度)
    ax.plot(x, t_cpu, color=C_ORANGE, marker="s", markersize=4.4, linewidth=1.4,
            zorder=4)
    ax.plot(x, t_gpu, color=C_BLUE, marker="o", markersize=4.4, linewidth=1.4,
            zorder=5)

    ax.set_yscale("log")
    # 上限从 250 抬到 400: 内联标注要挤在 CPU 曲线上方, 250 会把 "PIML CPU" 压出轴框
    ax.set_ylim(0.08, 400)
    ax.set_ylabel("单步缩聚耗时 (ms, 对数刻度)", fontsize=8.6)
    ax.set_xlabel(r"子结构并发规模 $N_{\mathrm{subs}}$", fontsize=FIG3_LABEL_FS)
    ax.set_xticks(x)
    ax.set_xticklabels([str(n) for n in n_subs], fontsize=8.6)
    # 末档 "3.3 ms" 标在最后一个数据点右侧, 默认 margins 不够, 右边多留 0.42 格
    ax.set_xlim(-0.18, len(x) - 1 + 0.42)

    # 3. 内联曲线标注取代图例
    ax.text(x[1] - 0.12, t_cpu[1] * 2.6, "PIML CPU", ha="left", va="bottom",
            fontsize=8.0, fontweight="bold", color=C_ORANGE)
    ax.text(x[1] - 0.12, t_gpu[1] * 0.38, "PIML GPU", ha="left", va="top",
            fontsize=8.0, fontweight="bold", color=C_BLUE)

    # 4. 末档耗时。字号从 7.4 提到 8.0: 7.4 pt 缩到 DOCX 幅面只剩 5.5 pt, 低于
    #    report_print_sizes 的 6 pt 门槛; 8.0 pt 恰好落在 6.0 pt。
    ax.text(x[-1], t_cpu[-1] * 1.35, f"{t_cpu[-1]:.1f} ms", ha="center",
            va="bottom", fontsize=8.0, color=C_ORANGE, fontweight="bold")
    ax.text(x[-1], t_gpu[-1] * 0.62, f"{t_gpu[-1]:.1f} ms", ha="center",
            va="top", fontsize=8.0, color=C_BLUE, fontweight="bold")

    # 5. 中间区域双向箭头与加速比跨度标注 (无边框)
    mid_x = x[2]
    ax.annotate("", xy=(mid_x, t_gpu[2] * 1.5), xytext=(mid_x, t_cpu[2] * 0.66),
                arrowprops=dict(arrowstyle="<->", color=INK_2, lw=1.0), zorder=6)
    ax.text(mid_x + 0.14, np.sqrt(t_cpu[2] * t_gpu[2]), "约 22 ~ 26 倍",
            ha="left", va="center", fontsize=8.0, fontweight="bold", color=INK,
            zorder=7)

    recessive_axes(ax, grid_axis="y")
    ax.grid(True, linestyle="--", alpha=0.4, color=GRID, axis="y")
    panel_title(ax, p3_title(label, "批量缩聚 GPU 加速"))


def build_fig3_panels(eq_data, rt, sol_data, pol_data):
    """把图 9 的各格分别画进一张单独的画布, 供证据文档逐格引用.

    这里仍出四张 —— 含合图已不用的"子结构缩聚正确性", 它作为证据不能丢, 只是不再占
    合图的四分之一 (等价量级 ``<2e-12`` 正文已写)。独立分图只有一格, 序号无所指,
    故一律 ``label=None`` 不加 (a)/(b)。文件名的 a~d 只是稳定标识, 与合图序号无关。
    """
    panels = (
        ("a", lambda ax: draw_panel_3a(ax, eq_data, label=None)),
        ("b", lambda ax: draw_panel_3b(ax, rt, label=None)),
        ("c", lambda ax: draw_panel_3c(ax, sol_data, label=None)),
        ("d", lambda ax: draw_panel_3d(ax, pol_data, label=None)),
    )
    paths = []
    for label, draw in panels:
        fig = plt.figure(figsize=FIG3_PANEL_SIZE, dpi=200,
                         constrained_layout=True)
        ax = fig.subplots(1, 1)
        draw(ax)
        path = OUT_FIG3_PANEL.format(label)
        path_svg = OUT_FIG3_PANEL_SVG.format(label)
        fig.savefig(path, bbox_inches="tight", pad_inches=0.14)
        fig.savefig(path_svg, bbox_inches="tight", pad_inches=0.14)
        paths.append(path)
        print(f"[out] {path}\n[out] {path_svg}")
        plt.close(fig)
    return paths


def build_fig3():
    """图 9: 三格分别回答"机理通不通 / 全局准不准 / 快到什么程度".

    (a) 解释机理 —— 受控扰动扫描证实 E^T K_ii E 带来严格二阶误差压缩 (斜率 2.00);
    (b) 全局保真 —— 实测预测子结构形函数装配全局求解全场位移误差 0.15%、柔度 0.20%;
    (c) 硬件加速 —— 批量张量缩聚在单卡上较同实现 CPU 快约 22~26 倍.

    2026-08-28 撤掉原 (a)「子结构缩聚正确性」: 那一格通篇只传达 ``1.95e-12`` 与
    ``1.83e-12`` 两个标量, 为此占掉整图四分之一还配了一条跨三个数量级的对数轴 ——
    而正文早已写明"相对差均 <2e-12", 图里等于把同一句话再画一遍。证据本身不丢, 仍由
    :func:`build_fig3_panels` 出独立分图留档。余下三格不排成 2x2, 图 8/9/10 便不再是
    清一色四宫格 —— 那是模板感的最强来源。

    版式: 上排 (a)(b) 各半宽, 下排 (c) 通栏。同日先试过 1x3, 但缩到 DOCX 版心
    (15.2 cm = 5.98 in) 后每格只分到 1.99 in, 其中 42% 被 y 刻度标签与轴标签吃掉,
    **净绘图区仅剩 1.15 in (约 2.9 cm)**, 窄到无法阅读。改上二下一后上排净宽 2.16 in、
    下排 5.44 in。删到 1x2 只能把上排推到 2.24 in (差 0.08 in, 等于没差别), 宽度问题
    上二下一已经解决, 故保留 (a): 正文只给得出"斜率 2.00"这个拟合值, 而"严格二阶"的
    证据是那条线在 12 个采样点、``eps_N`` 跨 3.5 个数量级上全程笔直, 文字替代不了。

    注: 图高不计入"限 1000 字", 字数口径剥掉图片与图题, 省版面与压字数是两件事。
    """
    eq_data = data_condensation_equivalence()
    rt = data_piml_routes()
    sol_data = data_piml_solution_layer()
    pol_data = data_rigid_pollution()

    # 高度 5.2 in (原 2x2 为 7.0 in)。height_ratios 给下排 0.80: 通栏格宽 5.44 in,
    # 再压扁则两条近乎平行的折线被拉成细长带子。上下两排各用一个嵌套 subgridspec 而非
    # 共用 gridspec(2, 2) —— 后者会让 constrained_layout 对齐两行的列边界, 通栏格的
    # 左边界被上排的 y 刻度标签牵住 (图 10 踩过同一个坑)。
    fig = plt.figure(figsize=(FIG_WIDTH_IN, 5.2), dpi=200, constrained_layout=True)
    fig.get_layout_engine().set(rect=(0.0, 0.0, 1.0, 1.0))
    outer = fig.add_gridspec(2, 1, height_ratios=[1.0, 0.80])
    gs_top = outer[0].subgridspec(1, 2)

    # 序号在此现场指定: 原 (b)(c)(d) 依次顶上 (a)(b)(c)。各 draw_panel_3* 的函数名
    # 仍按内容固定, 不随序号改动。
    draw_panel_3b(fig.add_subplot(gs_top[0, 0]), rt, label="a")
    draw_panel_3c(fig.add_subplot(gs_top[0, 1]), sol_data, label="b")
    draw_panel_3d(fig.add_subplot(outer[1]), pol_data, label="c")

    for path in (OUT_FIG3, OUT_FIG3_SVG):
        fig.savefig(path, bbox_inches="tight", pad_inches=0.14)
        print(f"[out] {path}")
    plt.close(fig)

    build_fig3_panels(eq_data, rt, sol_data, pol_data)


# ==========================================================================
# 图 4 —— FEALPy 多后端加速比（储备三）
# ==========================================================================

def build_fig4():
    """图 4 / 申报书图 6: 基于 FEALPy 的张量化拓扑优化平台百万级算力与阶段性能实测.

    四面板设计 (2026-08-27 按刘畅意见补入大规模构型, 2026-08-28 四格统一到博士
    论文算例 3.3 的加密版, 191.5 万自由度):
      (a) 单步迭代总耗时对比 (CPU 稀疏 vs GPU 张量化, 两侧同为 float64)
      (b) 拓扑优化核心计算阶段加速比拆解 (Breakdown)
      (c) 初始构型: 该算例的设计域长方体 (外部底图 FIG4_PANEL_C_IMG)
      (d) 优化后构型: 同一算例收敛后的最终结构 (外部底图 FIG4_PANEL_D_IMG)

    (c)(d) 曾于 2026-08-28 试改为"优化后构型整行 + 收敛历程整行", 意在让"90 步收敛"
    由曲线自证而非停留在图注断言; 当日按刘畅意见退回本 2x2 前后对比 —— 本图的主题是
    多后端性能, 收敛证据不是必需项, 而前后对比让非专业读者一眼看懂"拓扑优化在做什么".
    代价是构型面板受限于半幅列宽 (见下方版式注释), 这是已知且已接受的取舍。

    面板 (a)(b)(c)(d) 的规模与步数一律读自快照, 不在此处硬编码, 避免换算例后图上数字
    与快照脱节.
    """
    data = data_backends()

    for img in (FIG4_PANEL_C_IMG, FIG4_PANEL_D_IMG):
        if not os.path.isfile(img):
            raise FileNotFoundError(
                f"图 10 构型底图不存在: {img}\n"
                "先用 soptx 的 render_topology.py 渲染 (--pair 一次出两张、共用裁剪框)。")

    # 上下两排各用一个嵌套 subgridspec, 而非共用一个 2x2 gridspec: 后者会让
    # constrained_layout 对齐两行的列边界, 于是 (c)(d) 被 (a)(b) 的 y 刻度标签
    # (左 1.44 in + 中 1.16 in, 合计占满幅的 33%) 挤到只剩 2.68 in 宽; 构型底图
    # 宽高比固定 1.80, 显示高度只能是 宽度/1.80, 2.68 in 宽即 1.49 in 高。
    # 拆开后 (c)(d) 不再受上排刻度标签牵连, 各占约 3.8 in 宽 / 2.1 in 高。
    # 底图自身留白已只剩 8 px, 裁剪没有余量; 行高也无效(高度受宽度约束) —— 宽度是
    # 唯一的杠杆。
    fig = plt.figure(figsize=(FIG_WIDTH_IN, 7.0), dpi=200, constrained_layout=True)
    fig.get_layout_engine().set(rect=(0.0, 0.0, 1.0, 1.0))
    outer = fig.add_gridspec(2, 1, height_ratios=[1.0, 0.78])
    gs_top = outer[0].subgridspec(1, 2)
    gs_bot = outer[1].subgridspec(1, 2, wspace=0.05)

    # (a) 左上: 单步迭代总耗时对比
    ax_a = fig.add_subplot(gs_top[0, 0])
    y_a = np.arange(len(data["labels_a"]))
    bars_a = ax_a.barh(y_a, data["times_a"], 0.48, color=[C_ORANGE, C_BLUE],
                       edgecolor=SURFACE, linewidth=1.2, zorder=3)
    ax_a.set_yticks(y_a)
    ax_a.set_yticklabels(data["labels_a"], fontsize=9.5)
    ax_a.invert_yaxis()
    ax_a.set_xlabel("单步迭代耗时 (s)", fontsize=10.0)
    ax_a.set_xlim(0, max(data["times_a"]) * 1.22)
    ax_a.set_xticks(np.linspace(0, max(data["times_a"]), 5))

    dx = max(data["times_a"]) * 0.018
    for b, t in zip(bars_a, data["times_a"]):
        w = b.get_width()
        y = b.get_y() + b.get_height() / 2
        if t == max(data["times_a"]):
            ax_a.text(w + dx, y, f"{t:.2f} s", ha="left", va="center",
                      fontsize=9.5, fontweight="bold", color=C_ORANGE)
        else:
            ax_a.text(w + dx, y, f"{t:.2f} s  (×{data['speedup_a']:.1f} 加速)",
                      ha="left", va="center",
                      fontsize=9.5, fontweight="bold", color=C_BLUE)

    recessive_axes(ax_a, grid_axis="x")
    ax_a.spines["left"].set_visible(False)
    ax_a.tick_params(axis="y", length=0)
    panel_title(ax_a, "(a) 单步迭代总耗时对比")

    # (b) 右上: 拓扑优化各阶段加速比拆解（跨 0.9~274 两个数量级, 用对数轴）
    ax_b = fig.add_subplot(gs_top[0, 1])
    y_b = np.arange(len(data["stages_b"]))
    colors_b = [C_AQUA, C_BLUE, C_AQUA, C_AQUA]
    bars_b = ax_b.barh(y_b, data["speedups_b"], 0.52, color=colors_b,
                       edgecolor=SURFACE, linewidth=1.2, zorder=3)
    stage_labels = [
        f"{s}\n{detail}" for s, detail in zip(data["stages_b"], data["time_details_b"])
    ]
    ax_b.set_yticks(y_b)
    ax_b.set_yticklabels(stage_labels, fontsize=8.6)
    ax_b.invert_yaxis()
    ax_b.set_xlabel("单卡 GPU 硬件加速比（对数）", fontsize=10.0)
    ax_b.set_xscale("log")
    speed_max = max(data["speedups_b"])
    ax_b.set_xlim(0.5, speed_max * 1.6)
    ax_b.xaxis.set_major_locator(LogLocator(base=10.0))
    ax_b.xaxis.set_major_formatter(ScalarFormatter())

    for b, s in zip(bars_b, data["speedups_b"]):
        w = b.get_width()
        y = b.get_y() + b.get_height() / 2
        ax_b.text(w * 1.08, y, f"×{s:.1f}", ha="left", va="center",
                  fontsize=8.6, fontweight="bold", color=INK)

    recessive_axes(ax_b, grid_axis="x")
    ax_b.spines["left"].set_visible(False)
    ax_b.tick_params(axis="y", length=0)
    panel_title(ax_b, "(b) 核心计算阶段加速比拆解")

    # 下排: 前后对比
    ax_c = fig.add_subplot(gs_bot[0, 0])
    ax_c.imshow(plt.imread(FIG4_PANEL_C_IMG))
    ax_c.set_axis_off()
    panel_title(ax_c, "(c) 初始构型（设计域）")

    ax_d = fig.add_subplot(gs_bot[0, 1])
    ax_d.imshow(plt.imread(FIG4_PANEL_D_IMG))
    ax_d.set_axis_off()
    panel_title(ax_d, f"(d) 优化后构型（{data['n_dofs'] / 1e4:.1f} 万自由度，"
                      f"{data['iterations']} 步收敛）")

    center_titles_on_blocks(fig, [ax_a, ax_b, ax_c, ax_d])

    fig.savefig(OUT_FIG4, bbox_inches="tight", pad_inches=0.12)
    fig.savefig(OUT_FIG4_SVG, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    print(f"[out] {OUT_FIG4}\n[out] {OUT_FIG4_SVG}")


def main():
    setup_font()
    report_print_sizes("图2/3/4", FIG_WIDTH_IN)
    build_fig2()
    build_fig2_panel_c_internal()
    build_fig3()
    build_fig4()


if __name__ == "__main__":
    main()
