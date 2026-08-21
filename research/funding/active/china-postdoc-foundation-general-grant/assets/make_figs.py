#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成《中国博士后科学基金第 80 批面上资助申请书》第 6 部分"研究基础"配图。

    输出:
        assets/fig2_matrix_free.png     图 2 Matrix-Free 求解（储备一）
        assets/fig3_piml_accuracy.png   图 3 PIML 局部响应恢复精度（储备二）
        assets/fig4_multibackend.png    图 4 FEALPy 多后端加速比（储备三）

一张图对应正文"一、"中的一点，编号与储备一一对应，图注里不再需要"对应第 1、3 点"
这类跨图索引。也因此每张图内部只用 (a)(b)(c)(d) 单字母编号，原先用来区分储备的
a*/b*/c* 前缀已无信息量，全部去掉；图 4 只有一个面板，不加面板编号。

    图 2  储备一  Matrix-Free 算子 / Krylov 求解  —— (a)(b) 实测，(c) 占位
          (a) 2D/3D 相对 L2 误差收敛阶（显式组装与 matrix-free 同一离散）—— 对不对
          (b) 两路进程峰值 RSS 随自由度增长, 与本机可用内存上限        —— 能算多大
          (c) 单次算子作用耗时构成随设备数的变化（算术塌缩, 同步膨胀）  —— 卡在哪

    图 3  储备二  PIML 局部力学表示与精确缩聚验证  —— 三格全部实测
          (a) 缩聚解与全装配直解的相对差, 对照验收阈值                —— 真值对不对
          (b) 形函数误差经式 (17) 的二阶压缩, 与直接预测缩聚刚度对照  —— 代理准不准
          (c) 观测刚化中来自刚体零空间伪刚度的份额, 参数化改造前后    —— 靠什么保证

    图 4  储备三  基于 FEALPy 的拓扑优化平台与多后端计算
          同一算例在 NumPy / PyTorch / JAX 上的加速比（横向条形，无面板编号）

三张图共用同一源图宽（FIG_WIDTH_IN），因此在 DOCX 里缩放比相同、印刷字号一致。
插图按 15.2 cm 宽插入（见 build_grant_docx.py），纸面物理尺寸与源图宽无关，
源图越窄同一 pt 值的字在纸面上越大——所以宽度是个字号旋钮，不是尺寸旋钮。

##############################################################################
#  数据来源声明                                                               #
#                                                                            #
#  * 图 2(a)(b) 是 **实测数据**，全部读自 soptx 的入库快照                      #
#      experiments/matrix_free_capability/figure_data/fig2_data.json          #
#    （常量 FIG2_SNAPSHOT，路径可用环境变量 SOPTX_ROOT 覆盖）。本文件内         #
#    **不再手抄任何误差值**：快照由该目录的 run.py 采集，自带 provenance        #
#    与门禁，逐档数值同时渲染进它的 results_analysis.md。                       #
#    上游产物仍是那三处，但已由 cases.toml 固定参数、由 run.py 调度：           #
#      manufactured_convergence_{2d_tri_sinusoidal,3d_tet_divfree-poly}_p1_*.json #
#      stage1-validation-all.json ／ peak_rss_3d_tet_*.json                    #
#    仍未解决的是**溯源**：上游 JSON 里没有 git 字段（validate.py 不写          #
#    environment 块，benchmark_cpu_ea.py 连时间戳都不写），快照只能记下采集时   #
#    的 revision 与 dirty 标志。当前快照 reproducible=False（工作区 dirty），   #
#    **正式投递前须在 clean revision 上重跑固化**。                             #
#  * 图 3 三格 **全部为实测**，出处见各 data_* 的 docstring：                    #
#      examples/substructure_elasticity/outputs/lagrange_comparison_{2d,3d}.json #
#      examples/piml_substructure_elasticity/outputs/eq17_second_order.json    #
#      examples/piml_substructure_elasticity/outputs/piml_exact_comparison.json #
#    因此图 3 **不画水印**，改用 footnote() 给数据出处。                        #
#  * 图 2(c)、图 4 仍是 **占位示意数据**，投递前必须逐项替换为实测。            #
#    图面已加"占位"水印与脚注，水印仅在 PLACEHOLDER = True 时绘制；             #
#    图 2 的脚注逐格标明哪一格实测、哪一格占位，不要连脚注一起删。              #
#    图 2 的水印**只打在 (c) 轴内**（watermark(..., ax=ax_c)），不整幅覆盖——    #
#    整幅水印会盖到已实测的 (a)(b)，也会被单格切图横向切碎。图 4 整张都是占位，  #
#    仍用整幅水印。                                                            #
#  * 图 2 除合并图外还输出三张单格切图 fig2_matrix_free_panel_{a,b,c}.png，     #
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
#  因此: 不写内存墙与端到端加速的结论, 改画"对不对 / 能算多大 / 卡在哪"。       #
#  瓶颈定位恰是研究内容 1、2 的立项依据。                                       #
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
from matplotlib.ticker import LogLocator, NullFormatter, NullLocator
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

# 置为 False 即去掉"占位"水印与脚注（数据全部换成实测后再改）
PLACEHOLDER = True

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_FIG2 = os.path.join(HERE, "fig2_matrix_free.png")
# 图 2 的单格切图。合并图进申请书, 单格图供 soptx 的按图面分格文档引用
# (合并图 2394 px 宽, 按文档宽渲染时单格只剩约 296 px, 刻度读不了)。
OUT_FIG2_PANEL = os.path.join(HERE, "fig2_matrix_free_panel_{}.png")
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

OUT_FIG3 = os.path.join(HERE, "fig3_piml_accuracy.png")
OUT_FIG4 = os.path.join(HERE, "fig4_multibackend.png")

# 插图在 DOCX 中的宽度（build_grant_docx.py 里写死 15.2 cm），用于反推印刷字号。
# 三张图共用同一源图宽 => 缩放比相同 => 印刷字号一致。纸面高度由各自的
# figsize 高宽比决定, 与这个值无关, 所以统一宽度不会把图 3 压扁。
DOCX_WIDTH_IN = 15.2 / 2.54
FIG_WIDTH_IN = 8.0

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
# 配色（dataviz 参考调色板 slot 1/2/3，未改动；单一浅色模式，面向印刷）
# --------------------------------------------------------------------------
SURFACE = "#ffffff"
INK = "#0b0b0b"        # 主文字
INK_2 = "#52514e"      # 次文字 / 轴
GRID = "#dcdbd6"
C_BLUE = "#2a78d6"     # slot 1
C_ORANGE = "#eb6834"   # slot 2
C_AQUA = "#1baf7a"     # slot 3
# 同色浅阶: 图 2(c) 的堆叠段。段内用明度区分"装配/求解", 色相仍归属路径,
# 这样 (a)(b)(c) 三格里蓝=显式组装、橙=Matrix-Free 的对应关系不被打断。
C_BLUE_L = "#a9cbf2"
C_ORANGE_L = "#f8bb9f"

# 字号按 DOCX 缩放比反推：source_pt * (15.2cm / FIG_WIDTH) >= 7 pt
plt.rcParams.update({
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
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


def report_print_sizes(name, fig_width_in):
    scale = DOCX_WIDTH_IN / fig_width_in
    print(f"[scale] {name} 图宽 {fig_width_in}in -> DOCX {DOCX_WIDTH_IN:.2f}in, "
          f"缩放比 {scale:.2f}")
    for key in ("xtick.labelsize", "axes.labelsize", "axes.titlesize", "legend.fontsize"):
        eff = plt.rcParams[key] * scale
        flag = "OK" if eff >= 6.0 else "过小"
        print(f"[scale]   {key:20s} {plt.rcParams[key]:5.1f}pt -> {eff:4.1f}pt  {flag}")


def panel_title(ax, text):
    """统一的面板标题：左对齐、加粗、贴在轴框上方。"""
    ax.set_title(text, loc="left", fontweight="bold", color=INK, pad=7)


def recessive_axes(ax, grid_axis="y"):
    ax.grid(True, axis=grid_axis, linestyle="--", alpha=0.55, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def footnote(fig, text, color=INK_2, size=9.0):
    """图底脚注。与 watermark 分开: 实测图也需要脚注(数据出处), 但不该有水印。"""
    fig.text(0.5, 0.004, text, fontsize=size, color=color, ha="center", va="bottom")


def watermark(fig, note, ax=None):
    """绘制"占位示意数据"水印与图底红字脚注, 仅在 ``PLACEHOLDER`` 为真时生效.

    参数:
        fig: 承载脚注的 ``Figure``.
        note: 图底红字脚注文本, 逐格说明哪一格实测、哪一格占位.
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
    装配方法 ``fast``, 无预条件 CG(``rtol=1e-10``), 四档 n = 8/16/32/64, 自由度
    2,187 / 14,739 / 107,811 / 823,875。

    **口径是进程驻留集高水位**(``resource.getrusage(RUSAGE_SELF).ru_maxrss``,
    与 ``/usr/bin/time -v`` 的 ``Maximum resident set size`` 同源, 实测逐 KiB
    吻合), 不是算子长期保存数组的字节数。后者只统计 CSR 的 COO 三元组或 EA 侧
    缓存的 ``K_e``, 既不含组装期临时量也不含 Krylov 工作向量。

    **必须一个进程测一个层级。** ``benchmark_cpu_ea.py`` 缺省的 ``serial-fa-ea``
    在同一进程里先后建 FA 与 EA, 高水位只等于两者的较大值, EA 隔离不出来。因此
    这批数据走的是该脚本的 ``--mode serial-peak-rss``, 八个独立进程。

    实测本身推翻了两条曾经想写进本格的说法:

      * **EA 省的不是"存得少", 而是"不物化全局 COO/CSR"。** n=64 上 FA 的
        ``operator`` 阶段单步涨 16.04 GiB, 而最终留下的 CSR 只有 0.81 GiB ——
        峰值的 95% 是组装过程量。EA 缓存的 ``K_e`` 反而有 1.83 GiB, 是 FA 稳态
        CSR 的 2.3 倍; 只看稳态存储, EA 是**更费**内存的那一个。
      * **倍数是 1.9 不是 3.8。** 早先按"每自由度非零元 vs 每积分点 double"推
        的 3.8 倍是目标形态下的估算, 实测四档的峰值比为 1.09 / 1.45 / 1.78 /
        1.89 —— 最粗档偏低是因为解释器基线(0.158 GiB)还没被摊薄。扣掉基线后
        四档稳定在 1.74 / 1.93 / 1.88 / 1.91。

    "可算规模约为 1.9 倍"这句话成立, 依据是两条线扣基线后**都是自由度的一次
    函数**: 从 n=16 到 n=64 自由度涨 55.9 倍, FA 的基线以上峰值涨 59.5 倍
    (指数 1.016), EA 涨 60.1 倍(指数 1.018)。线性增长下, 内存上限固定时可算
    规模之比就等于内存之比。

    **横轴止于实测最大规模, 不外推。** 天花板取本机实际可用内存 47 GiB
    (``MemTotal = 49,325,728 kB``), 而不是某块 GPU 的显存 —— 这批数是 CPU 主机
    RSS, 拿显存当天花板会把两种资源混为一谈。GPU 路径(阶段 1c)未开始。

    **只画内存、不画时间。** 少存就得多算, 这个取舍是 memory-vs-recompute, 本格
    只出示内存这一侧的事实; 谁更优是研究内容 2 要回答的问题。作为对照, 同一批
    运行里 n=64 的 CG 时间 EA 111.2 s 对 FA 76.8 s, EA 更慢, 但两者迭代数同为
    493、真相对残差同为 ``1.053e-10``, 即同一个离散、同一条收敛轨迹。

    **全部数值读自快照** ``FIG2_SNAPSHOT`` 的 ``panels.b``, 与 (a) 同一份出处,
    本函数不再手抄。上游是 ``examples/matrix_free_elasticity/benchmark_cpu_ea.py``
    的八次独立运行(每档一个进程, 因为 ``ru_maxrss`` 是进程级高水位, 同进程里
    先建 FA 再建 EA 会把 EA 的峰值抬高), 产物
    ``peak_rss_3d_tet_polynomial_p1_{fa,ea}_fast_n{8,16,32,64}.json``。
    口径与逐阶段分解见 SOPTX ``experiments/matrix_free_capability/results_analysis.md``
    §3。绝对值不可移植(随机器、BLAS 与分配器变化), 可引用的是同机同批次的相对关系。

    返回:
        dof: 四档自由度数.
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


def data_bottleneck_breakdown():
    """占位: 单次算子作用的耗时构成占比, 随 GPU 数变化。

    四段口径(合计 100%):
      * 单元核算术  —— 局部 K_e 作用的浮点部分;
      * 访存        —— gather/scatter-add 的不规则访存与显存带宽等待;
      * 通信同步    —— 共享自由度的一致化与归约(跨设备);
      * 全局归约    —— Krylov 内积与范数的 all-reduce(与迭代数直接挂钩)。

    **这一格是全图性价比最高的一格。** 它不证明"我很快", 而证明"我知道
    下一步该修哪里": 局部算术随设备数被摊薄, 跨设备开销却随设备数膨胀,
    两条相反的斜率交叉在某个设备数上——那个交叉点就是本项目要往后推的东西。
    研究内容 1(GPU 单元核与多卡扩展)与研究内容 2(存储策略取舍)的立项依据
    都在这一格里, 比任何文献综述都硬。

    画占比而不画绝对时间: 绝对时间随设备数单调下降, 看上去一片大好,
    构成的此消彼长反而被压平; 绝对总时间用柱顶文字标出, 信息不丢。

    **应在拓扑优化算例上测量, 不是制造解。** matrix-free 在拓扑优化里的
    价值来自"每个设计迭代密度变了、刚度必须重建", 制造解上的单次求解
    展示不出这一点。
    """
    n_gpu = np.array([1, 2, 4, 8, 16])
    share = np.array([          # 行: 设备数; 列: 算术 / 访存 / 通信同步 / 全局归约
        [62, 31, 2, 5],
        [55, 28, 9, 8],
        [44, 24, 21, 11],
        [32, 18, 36, 14],
        [21, 13, 48, 18],
    ], dtype=float)
    total_ms = np.array([12.4, 6.8, 3.9, 2.6, 2.1])
    labels = ["单元核算术", "访存", "通信同步", "全局归约"]
    return n_gpu, share, total_ms, labels


# --------------------------------------------------------------------------
# 图 3 的三组数据全部为实测, 逐个 docstring 记录取数路径。
# --------------------------------------------------------------------------

def data_condensation_equivalence():
    """实测: 静力缩聚求解与 Lagrange 全装配直解的代数等价性。

    出自 SOPTX ``examples/substructure_elasticity/compare_lagrange.py``, 冻结在
    ``outputs/lagrange_comparison_{2d,3d}.json``, 逐字转录自同目录
    ``results_analysis.md`` 第 4.1 节 (两份 ``passed`` 均为 ``true``)。

    两条链是**同一个离散的两种解法**: 全装配直解与"缩聚接口求解 + 内部回填",
    因此二者之差只应是浮点累积, 不含任何离散误差。这一格因而是 PIML 的入场券——
    代理学的是缩聚算子, 若缩聚本身与直解不等价, 后两格的精度全部无意义。

    口径:
      * 2D ``HalfMBBBeamRight2d``, ``n_sub = 6x2``, ``n_fine = 5x5``, 682 全尺度自由度;
      * 3D ``FullMBBBeam3d``, ``n_sub = 6x2x2``, ``n_fine = 4x4x4``, 6,075 全尺度自由度;
      * 位移为全场相对 ``L2``, 柔度为标量相对差, 验收阈值 ``1e-11``。

    **正文的 ``1e-14`` 是错的**: 实测最大的一项是 2D 位移 ``1.92e-12``, 比 ``1e-14``
    低两个量级。改口径为"``1e-12`` 量级、验收阈值 ``1e-11``"。

    返回:
        labels: 四个指标名, 按 2D/3D 分组.
        values: 对应的相对差.
        colors: 2D 蓝 / 3D 橙, 与图 2(a) 的维度配色一致.
        gate: 验收阈值.
    """
    labels = ["3D 柔度", "3D 位移场", "2D 柔度", "2D 位移场"]
    values = np.array([5.6164e-13, 7.1006e-13, 1.7974e-12, 1.9224e-12])
    colors = [C_ORANGE, C_ORANGE, C_BLUE, C_BLUE]
    return labels, values, colors, 1.0e-11


def data_piml_routes():
    """实测: 形函数路线的二阶误差压缩, 与直接预测缩聚刚度路线的对照。

    出自 SOPTX ``examples/piml_substructure_elasticity/``:
      * 扫描与形函数路线 —— ``verify_shape_function_route.py``,
        ``outputs/eq17_second_order.json`` 的 ``sweep_points``、``loglog_slope``、
        ``eps_N_mean``、``eps_K17_mean``;
      * 直接预测路线 —— ``compare_exact.py``,
        ``outputs/piml_exact_comparison.json`` 的 ``holdout_ks_relative_error_mean``。

    两条路线**同一物理问题、同一密度分布、同一训练预算**
    (``FullMBBBeam2d``, ``12x2`` 子结构 x ``5x5`` 细网格, ``--seed 2026``,
    2000 样本 / 4000 轮 / ``lr 0.005``), 且都在 200 样本留出集上取均值, 可直接比较。

    机理: 设预测形函数 ``N_hat = N* + E``, 由 Huang 2023 式 (17)
    ``K_tilde = P^T K P`` 反推缩聚刚度, 则一阶项因 ``K_ii N* = -K_ib`` 逐项抵消,

        ``K_tilde(N* + E) - K_s == E^T K_ii E``

    是恒等式而非近似。故误差关于 ``||E||`` 严格二阶(实测 log-log 斜率 2.0030),
    且因 ``K_ii`` 对称正定, 误差阵半正定——式 (17) 只可能高估刚度。

    扫描的 12 个点是**受控扰动**: 在精确 ``N`` 上叠加指定量级的随机方向扰动,
    每量级取 8 个方向的均值。训练网络的实测点略低于该线, 是因为网络误差不是
    各向同性的随机方向; 这是观测事实, 不作修饰。

    返回:
        eps_n, eps_k: 受控扫描的 12 个点.
        slope: log-log 拟合斜率.
        net_n, net_k: 训练网络在留出集上的 (形函数误差, 式 (17) 后的刚度误差).
        direct_k: 直接预测缩聚刚度路线在同一留出集上的刚度误差.
    """
    eps_n = np.array([
        1.0000000000e-04, 2.0805675382e-04, 4.3287612811e-04, 9.0062802021e-04,
        1.8738174229e-03, 3.8986037025e-03, 8.1113083079e-03, 1.6876124758e-02,
        3.5111917342e-02, 7.3052715427e-02, 1.5199110830e-01, 3.1622776602e-01])
    eps_k = np.array([
        8.1866949381e-09, 3.5473507602e-08, 1.5725586350e-07, 6.7284581556e-07,
        2.8788442639e-06, 1.2587697054e-05, 5.3923617706e-05, 2.3266998306e-04,
        1.0577958071e-03, 4.6164747610e-03, 1.9514354902e-02, 8.1876053532e-02])
    return {
        "eps_n": eps_n, "eps_k": eps_k, "slope": 2.0030,
        "net_n": 0.08973309813, "net_k": 0.00435081315,
        "direct_k": 0.04199983811,
    }


def data_rigid_pollution():
    """实测: 观测刚化中来自刚体零空间伪刚度的份额, 参数化改造前后。

    出自 SOPTX ``examples/piml_substructure_elasticity/compare_exact.py`` 的
    ``energy_rigid_pollution_share`` 字段; 改造后的值读自当前
    ``outputs/piml_exact_comparison.json``, 改造前的值记在同目录
    ``results_analysis.md`` 第 2.2(c) 与 3.1 节 (版本二)。

    机制链: 自由漂浮子结构的缩聚刚度 ``K_s`` 恰有 ``n_rigid`` 个零特征值, 刚体模态
    是最软的方向, 而装配后各子结构的接口位移**实测 99.98% 落在该子空间**。
    严格正定的 ``L L^T`` 参数化在结构上无法表示秩亏, 必然向该子空间注入正伪刚度:
    实测伪刚度仅为最小非零特征值的 ``1.6%``, 却被平方量级放大约 ``2500`` 倍,
    贡献了观测刚化的 ``96.8%``。

    把预测限制到刚体模态的正交补上
    (``K_s_hat = R_perp L L^T R_perp^T``) 之后, 秩亏成为构造性质, 这条通道被关闭,
    该份额降到 ``3.3e-13``——13 个量级。

    **这一格证明的不是精度, 而是"范数看不出来的东西"**: ``1.6%`` 的伪刚度在相对
    Frobenius 范数下微不足道, 能量后果却占了误差的绝大部分。近奇异算子必须按物理
    结构 (零空间、正定性、能量) 检查, 不能只看范数——这正是研究内容 1 的结构保持与
    研究内容 3 的物理结构检查的立项依据。

    返回:
        labels: 两种参数化.
        share: 刚化中来自零空间污染的份额.
        notes: 各自在图面上直接标注的份额文本.
    """
    labels = ["无零空间约束\n" + r"$\widehat{\mathbf{K}}_s=\mathbf{LL}^{\mathsf{T}}$",
              "限制到变形子空间\n" + r"$\mathbf{R}_\perp\mathbf{LL}^{\mathsf{T}}\mathbf{R}_\perp^{\mathsf{T}}$"]
    share = np.array([0.968, 3.2944854739e-13])
    notes = ["96.8%", r"$3\times10^{-13}$"]
    return labels, share, notes


def data_backends():
    """占位: 同一拓扑优化算例在三种后端上的单步装配+求解耗时。

    标签不再折行: 图 4 用横向条形, 后端名当 y 轴刻度, 有整行宽度可用。
    """
    labels = ["NumPy (CPU)", "PyTorch (GPU)", "JAX (GPU)"]
    times = np.array([128.0, 11.5, 8.7])
    return labels, times, times[0] / times


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
                        textcoords="offset points", fontsize=7.8, color=color,
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

    # 图例只回答"哪条线是哪个维度", 不承担结论。放左下: 两条线都从左上走到右下,
    # 左下与右上各空出一块, 图例取左下: 右上留白, 不再填东西。
    # 第三条用中性灰的空心圆: 它代表的是"空心这种画法", 不是某一个维度, 所以
    # 不能沿用蓝或橙; 两条曲线上的环各自沿用本维度的 marker 形状。
    legend_handles = [
        Line2D([0], [0], color=C_BLUE, lw=2.0, ls="-", marker="o", ms=5.8,
               mec=SURFACE, mew=1.0, label="2D 三角形"),
        Line2D([0], [0], color=C_ORANGE, lw=2.0, ls="--", marker="s", ms=5.8,
               mec=SURFACE, mew=1.0, label="3D 四面体"),
        Line2D([0], [0], color=INK_2, lw=0.0, marker="o", ms=7.5, mfc="none",
               mew=1.4, label="Matrix-Free"),
    ]
    legend = ax.legend(handles=legend_handles, loc="lower left", fontsize=8.0,
                       frameon=True, framealpha=0.95, edgecolor=GRID,
                       handlelength=2.0, handletextpad=0.55, borderpad=0.4,
                       # y 锚点原为 0.10, 是给下方那行核验小字让位; 小字删掉后落回角上
                       labelspacing=0.3, bbox_to_anchor=(0.005, 0.02))
    legend.get_frame().set_linewidth(0.8)

    # 不在图面上写"P1 理论阶 2 · 收敛阶门禁 1.5"。这两个数由图说明给出(申请书里
    # 图说明就紧跟在图下方), 而图面上六个观测阶 1.83→2.00 自己就朝 2 收, 趋势
    # 不必再用一行小字复述。
    # 代价要记住: 门禁 1.5 在这张图上没有几何位置(y 轴是误差, 不是收敛阶), 删掉
    # 这行之后它**只**存在于图说明里 —— 图说明中"通过门禁(下限 1.5)"那句因此
    # 不可删减, 见申请书草稿的核验边界。
    panel_title(ax, "(a) 正确性验证")


def draw_panel_b(ax, dof, mem_asm, mem_mf, mem_base, mem_ceiling):
    """把图 2(b)"可计算规模"画进 ``ax``.

    参数:
        ax: 目标 ``Axes``.
        dof: 自由度数组.
        mem_asm: 显式组装的进程峰值内存, 单位 GiB.
        mem_mf: matrix-free 的进程峰值内存, 单位 GiB.
        mem_base: 解释器基线, 单位 GiB.
        mem_ceiling: 本机可用内存上限, 单位 GiB.
    """
    # 只画两条线: 存储层级(EA/PA/UA)的细分是研究内容 2 的题目, 不是研究基础的
    # 展示对象; 本格只需回答"同一台机器上能算多大", 一个对比就够。两条线相隔
    # 约 0.28 个数量级, 直接标注放得下, 因此不用图例。
    # 两条线在最细档才明显分开, 所以标注不能都挂在同一档上: 蓝线标在倒数第二档
    # 的左上、橙线标在最细档的右下, 两个标注与两条线各自错开。
    series = [("显式组装", mem_asm, C_BLUE, "o", 2, (-7, 7), "bottom", "right"),
              ("Matrix-Free", mem_mf, C_ORANGE, "s", 3, (6, -4), "top", "left")]
    for name, m, c, mk, ia, off, va, ha in series:
        ax.loglog(dof, m, color=c, lw=2.2, marker=mk, ms=6.0,
                  mec=SURFACE, mew=1.2, zorder=4)
        ax.annotate(name, xy=(dof[ia], m[ia]), xytext=off,
                    textcoords="offset points", fontsize=9, color=c,
                    ha=ha, va=va, fontweight="bold")

    # 天花板: 让"能算多大"落在一台具体机器上, 而不是抽象的增长趋势。取本机实际
    # 可用内存, 不取某块 GPU 的显存 —— 这批数是 CPU 主机 RSS, 两种资源不可混。
    ax.axhline(mem_ceiling, color=INK_2, lw=1.2, ls="--", alpha=0.9, zorder=2)
    ax.text(dof[0] * 1.05, mem_ceiling * 1.22, f"本机可用内存 {mem_ceiling:.0f} GiB",
            fontsize=8.5, color=INK_2, ha="left", va="bottom")
    # 解释器基线: 最粗档两条线几乎并拢, 不解释会被读成"小规模上 EA 没用"。
    ax.axhline(mem_base, color=INK_2, lw=1.0, ls=":", alpha=0.75, zorder=2)
    ax.text(dof[-1] * 5.0, mem_base * 1.14, "解释器基线",
            fontsize=8.0, color=INK_2, ha="right", va="bottom")

    ax.set_xlabel("自由度数")
    ax.set_ylabel("进程峰值内存 (GiB)")
    ax.set_xlim(dof[0] / 2.4, dof[-1] * 5.5)
    ax.set_ylim(mem_base / 2.2, mem_ceiling * 3.6)
    ax.xaxis.set_major_locator(LogLocator(base=10.0, numticks=5))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_minor_formatter(NullFormatter())
    recessive_axes(ax, grid_axis="both")
    # 本格的结论句。倍数取最细档、且是扣掉解释器基线之后的比值: 基线是常数项,
    # 不随问题规模走, 留在分子分母里只会把倍数往 1 拉。
    ratio = (mem_asm[-1] - mem_base) / (mem_mf[-1] - mem_base)
    # 结论框放左上: 两条线自左下走向右上, 左上是本格唯一一块两条线都不经过的空
    # 白; 右下已经让给解释器基线那条虚线及其标注。
    ax.text(0.03, 0.79,
            f"同一内存上限下可算规模\n约为显式组装的 {ratio:.1f} 倍",
            transform=ax.transAxes, fontsize=8.5, color=INK, ha="left", va="top",
            linespacing=1.5,
            bbox=dict(boxstyle="round,pad=0.32", fc="white", ec=GRID, alpha=0.95))
    panel_title(ax, "(b) 可计算规模")


def draw_panel_c(ax, n_gpu, share, total_ms, seg_labels):
    """把图 2(c)"并行瓶颈"画进 ``ax``. 当前为占位示意数据.

    参数:
        ax: 目标 ``Axes``.
        n_gpu: 横轴的 GPU 数.
        share: ``(len(n_gpu), 4)`` 的耗时占比, 各行和为 1.
        total_ms: 各档单次算子作用的总耗时, 单位 ms.
        seg_labels: 四个构成段的名字.
    """
    x = np.arange(len(n_gpu))
    cum = np.vstack([np.zeros(len(x)), np.cumsum(share, axis=1).T])
    seg_colors = [C_BLUE, C_BLUE_L, C_ORANGE_L, C_ORANGE]   # 蓝=局部计算, 橙=跨设备开销
    for j in range(share.shape[1]):
        ax.fill_between(x, cum[j], cum[j + 1], color=seg_colors[j],
                        linewidth=0.0, zorder=3)
        # 段与段之间留一条 surface 色的分隔线(2 px), 与堆叠柱的处理一致
        ax.plot(x, cum[j + 1], color=SURFACE, lw=1.6, zorder=4)

    # 直接标注四段: 每段标在自己最宽的地方, 因此不需要图例
    seg_ink = ["white", INK, INK, "white"]      # 深色块配白字, 浅色块配墨字
    band_anchor = [(0.6, 0), (0.6, 1), (3.4, 2), (3.4, 3)]
    for xa, j in band_anchor:
        yc = np.interp(xa, x, (cum[j] + cum[j + 1]) / 2.0)
        ax.text(xa, yc, seg_labels[j], ha="center", va="center",
                fontsize=8.5, color=seg_ink[j], fontweight="bold", zorder=5)

    # 绝对总时间不丢: 标在 100% 线之上, 不另开一根纵轴
    for i, t in enumerate(total_ms):
        label = f"{t:.1f} ms" if i == len(total_ms) - 1 else f"{t:.1f}"
        ax.text(i, 102.5, label, ha="center", va="bottom",
                fontsize=8.5, color=INK_2)

    ax.set_xticks(x)
    ax.set_xticklabels([f"{g}" for g in n_gpu])
    ax.set_xlabel("GPU 数")
    ax.set_ylabel("单次算子作用耗时占比 (%)")
    ax.set_xlim(0, len(x) - 1)
    ax.set_ylim(0, 116)
    ax.set_yticks([0, 25, 50, 75, 100])
    recessive_axes(ax, grid_axis="y")
    ax.grid(False)                 # 面积图里网格线会被色块盖住一半, 反而更乱
    panel_title(ax, "(c) 并行瓶颈")


def build_fig2_panels(cv, mem, bd):
    """把图 2 的三格各自画进一张单独的画布, 供按图面分格的文档逐格引用.

    与合并图共用同一批 ``draw_panel_*``, 因此内容与样式不可能漂移; 唯一的差别
    是画布形状 —— 合并图里每格只分到约 2.9 in 宽, 单格图给到整张 4.6 in, (a)
    的五个 "1/N" 刻度标签才不至于挤成一团。

    先前从合并图上按包围盒切图的做法已废弃: 切图必然继承三等分的窄格子, 而窄
    正是要解决的问题。

    参数:
        cv: ``data_convergence()`` 的返回值.
        mem: ``data_peak_memory()`` 的返回值.
        bd: ``data_bottleneck_breakdown()`` 的返回值.

    返回:
        写出的文件路径列表, 顺序为 (a)(b)(c).
    """
    dof, mem_asm, mem_mf, mem_base, mem_ceiling = mem
    n_gpu, share, total_ms, seg_labels = bd
    panels = (
        ("a", lambda ax: draw_panel_a(ax, cv)),
        ("b", lambda ax: draw_panel_b(ax, dof, mem_asm, mem_mf,
                                      mem_base, mem_ceiling)),
        ("c", lambda ax: draw_panel_c(ax, n_gpu, share, total_ms, seg_labels)),
    )
    paths = []
    for label, draw in panels:
        fig = plt.figure(figsize=FIG2_PANEL_SIZE, dpi=200,
                         constrained_layout=True)
        if label == "c" and PLACEHOLDER:
            fig.get_layout_engine().set(rect=(0.0, 0.075, 1.0, 1.0))
        ax = fig.subplots(1, 1)
        draw(ax)
        if label == "c":
            # 合并图那条脚注讲的是三格, 单格图换成只讲本格的一行
            watermark(fig, "注：占位示意数据，正式投递前须替换为实测值。", ax=ax)
        path = OUT_FIG2_PANEL.format(label)
        fig.savefig(path, bbox_inches="tight", pad_inches=0.14)
        paths.append(path)
        print(f"[out] {path}")
        plt.close(fig)
    return paths


def build_fig2():
    """图 2: 三格分别回答"对不对 / 能算多大 / 卡在哪"。

    这是研究基础栏目的三个必答问题, 按评审的阅读顺序排:
      (a) 排除造假——离散正确性是入场券, 因此**只给一格, 不扩张**;
      (b) 排除吹牛——规模能力落到一块具体硬件上, 且**止于实测最大规模**;
      (c) 证明真懂——瓶颈的定量定位, 也是唯一能把研究基础和研究内容焊死的一格。

    (a)(b) 为实测; (c) 目前是占位, 待测量后替换(替换清单见图注与各 data_* 的
    docstring)。水印只落在 (c) 轴内, 不整幅覆盖已实测的两格。

    三格的画法在 draw_panel_a/b/c 里, 合并图与 build_fig2_panels 的单格图共用
    同一批函数, 只是画布不同; 合并图是进申请书的那一张, 三格是一个论证的三步,
    不拆。

    小标题取名规则: 三个面板标题就是图题里并列的三个词
    (正确性 / 可计算规模 / 并行瓶颈), 图题因而成为三格的目录, 读者不必读图注
    就能建立对应。两条约束:
      * **不重复轴标签**。(b) 的 y 轴已写"进程峰值内存 (GB)", 所以标题写
        "可计算规模"——轴说不出来的那一半; (c) 同理。
      * **不写结论**。(b)(c) 是占位, 标题若写成"规模上限抬高""同步成为主导",
        就是拿没测出来的结果当论断; 名词短语只说"这一格在看什么"。
      * 口语版记号(对不对 / 能算多大 / 卡在哪)是设计时的内部助记, 留在
        申请书草稿的核验边界里, 不上图面——这是国家级基金申请书。
    """
    cv = data_convergence()
    dof, mem_asm, mem_mf, mem_base, mem_ceiling = data_peak_memory()
    n_gpu, share, total_ms, seg_labels = data_bottleneck_breakdown()

    fig = plt.figure(figsize=(FIG_WIDTH_IN, 3.6), dpi=200, constrained_layout=True)
    fig.get_layout_engine().set(rect=(0.0, 0.085, 1.0, 1.0))
    # (a) 要放下五个 "1/N" 刻度标签, 等宽三分会把它们挤成一团; (b) 的纵轴标题
    # 又比另外两格长, 所以宽度按 1.12 : 1 : 0.98 分。
    ax_a, ax_b, ax_c = fig.subplots(
        1, 3, gridspec_kw={"width_ratios": [1.12, 1.0, 0.98]}
    )

    draw_panel_a(ax_a, cv)
    draw_panel_b(ax_b, dof, mem_asm, mem_mf, mem_base, mem_ceiling)
    draw_panel_c(ax_c, n_gpu, share, total_ms, seg_labels)

    watermark(fig, "注：(a)(b) 为实测（线弹性制造解，p = 1）；(c) 为占位示意数据，正式投递前须替换为实测值。"
                   "(b) 已改为进程峰值 RSS 实测（CPU 主机 RSS，横轴止于实测最大规模、未外推）；\n"
                   "(c) 应在拓扑优化算例上测量——matrix-free 的价值来自每个设计迭代重建刚度，制造解的单次求解展示不出这一点。",
              ax=ax_c)
    fig.savefig(OUT_FIG2, bbox_inches="tight", pad_inches=0.14)
    print(f"[out] {OUT_FIG2}")
    plt.close(fig)

    # 把申请书图说明逐字引用、但图面上不画的那几个数打出来。图说明是这些数字在
    # 定稿里的唯一载体(图面上的核验小字已删), 所以每次重绘都要有机会对一眼。
    print(f"[图说明核对] EA/FA 解相对差 2D {cv['gap_2d']:.0e} / 3D {cv['gap_3d']:.0e}"
          f" · 比对档 2D {cv['dof_ea_coarse_2d']:,} / 3D {cv['dof_ea_coarse_3d']:,} 自由度"
          f" · 门禁下限 {cv['gate']}")
    build_fig2_panels(cv, (dof, mem_asm, mem_mf, mem_base, mem_ceiling),
                      (n_gpu, share, total_ms, seg_labels))


# ==========================================================================
# 图 3 —— PIML 局部响应恢复精度（储备二）
# ==========================================================================

def build_fig3():
    """图 3: 三格分别回答"真值对不对 / 代理准不准 / 靠什么保证"。

    与图 2 同构的三问, 落到 PIML 这一点上:
      (a) 排除造假——代理学的是缩聚算子, 缩聚本身若与全装配直解不等价, 后两格的
          精度全部无意义, 因此**只给一格, 不扩张**;
      (b) 排除吹牛——两条候选路线在**同一预算下**的精度, 并给出差距的机理
          (式 (17) 的二阶压缩), 而不是只报一个好看的数;
      (c) 证明真懂——``1.6%`` 的零空间伪刚度占了误差的 ``96.8%``, 说明近奇异算子
          必须按物理结构检查而非范数; 这一格把研究基础与研究内容 1、3 焊死。

    三格全部实测, 因此不画水印, 改用脚注给数据出处。

    原先的四格云图 (密度 / 参考解 / 恢复解 / 误差) 全部废弃, 两个原因:
      * 那批数据是合成的——生成脚本在精确 ``N`` 上叠加高斯平滑噪声冒充网络预测,
        图面上"界面附近误差偏大"的结构是造出来的, 不是测出来的;
      * 即便换成实测, 单个子结构的云图也只能回答"这一个子结构像不像", 回答不了
        "两条路线该选哪条""误差会不会在装配后被放大"这两个真问题。
    纸面高度同时由 14.0 cm 降到约 5.1 cm, 与图 2、图 4 齐平。
    """
    eq_labels, eq_vals, eq_colors, eq_gate = data_condensation_equivalence()
    rt = data_piml_routes()
    pol_labels, pol_share, pol_notes = data_rigid_pollution()

    fig = plt.figure(figsize=(FIG_WIDTH_IN, 3.6), dpi=200, constrained_layout=True)
    fig.get_layout_engine().set(rect=(0.0, 0.085, 1.0, 1.0))
    # (a) 要放下五个 "1/N" 刻度标签, 等宽三分会把它们挤成一团; (b) 的纵轴标题
    # 又比另外两格长, 所以宽度按 1.12 : 1 : 0.98 分。
    ax_a, ax_b, ax_c = fig.subplots(
        1, 3, gridspec_kw={"width_ratios": [1.12, 1.0, 0.98]}
    )

    # ---- (a) 缩聚解与全装配直解的相对差, 对照验收阈值 ----
    ax = ax_a
    # 四个数跨不到一个量级, 柱状图在对数轴上要从某个人为的左端起画, 那个左端会被
    # 读成"零"。棒棒糖图只用点的位置编码数值, 连线仅作视线引导, 没有这个歧义。
    y = np.arange(len(eq_vals))
    x_left = 8.0e-14
    for yi, v, c in zip(y, eq_vals, eq_colors):
        ax.plot([x_left, v], [yi, yi], color=c, lw=1.6, alpha=0.55, zorder=3)
        ax.plot([v], [yi], marker="o", ms=8.0, color=c, mec=SURFACE, mew=1.2,
                zorder=4)
        # 数值标签会横穿阈值虚线, 垫一层 surface 底色让线断在字外
        ax.annotate(f"{v:.2e}", xy=(v, yi), xytext=(9, 0),
                    textcoords="offset points", fontsize=8.6, color=INK,
                    ha="left", va="center", zorder=5,
                    bbox=dict(boxstyle="round,pad=0.16", fc=SURFACE,
                              ec="none", alpha=0.92))

    # 验收阈值画成竖直参照线: 与图 2(b) 的"单卡显存"同一手法——让"够不够好"落在
    # 一条事先定死的线上, 而不是由读者自己判断 1e-12 算不算小。标注贴线脚而非
    # 线头: 顶端要留给面板标题, 竖排文字在这个高度上必然顶出轴框。
    ax.axvline(eq_gate, color=INK_2, lw=1.2, ls="--", alpha=0.9, zorder=2)
    ax.text(eq_gate * 1.25, -0.74, f"验收阈值\n{eq_gate:.0e}",
            fontsize=8.4, color=INK_2, ha="left", va="bottom", linespacing=1.45)

    ax.set_xscale("log")
    ax.set_xlim(x_left, 3.0e-10)
    ax.set_ylim(-0.78, len(y) - 0.38)
    ax.set_yticks(y)
    ax.set_yticklabels(eq_labels)
    ax.set_xlabel("与全装配直解的相对差")
    ax.xaxis.set_major_locator(LogLocator(base=10.0, numticks=4))
    ax.xaxis.set_minor_formatter(NullFormatter())
    recessive_axes(ax, grid_axis="x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    # 四个十进制刻度挤在三分之一页宽里, 12 pt 会连成一片; 10 pt 折算到纸面
    # 仍有 7.5 pt, 高于本脚本自查的 6 pt 下限。(b) 同理。
    ax.tick_params(axis="x", labelsize=10)
    panel_title(ax, "(a) 缩聚算子正确性")

    # ---- (b) 形函数误差 -> 缩聚刚度误差: 二阶压缩 ----
    ax = ax_b
    # 受控扰动扫描: 这条线是本格的论据, 不是数据点的陪衬, 所以用中性墨色——它
    # 属于"规律"而非某一条路线; 两条路线才用蓝/橙。
    ax.loglog(rt["eps_n"], rt["eps_k"], color=INK_2, lw=1.6, ls="-",
              marker="o", ms=3.6, mec=SURFACE, mew=0.6, zorder=4)
    ax.annotate(f"受控扰动扫描\n斜率 {rt['slope']:.2f}",
                xy=(rt["eps_n"][3], rt["eps_k"][3]), xytext=(7, -2),
                textcoords="offset points", fontsize=8.2, color=INK_2,
                ha="left", va="top", linespacing=1.45)

    # 直接预测缩聚刚度路线没有形函数误差可言(它用精确 N 做恢复), 因此在这张
    # 横轴上没有位置, 只能画成水平参照线——这本身就是两条路线的结构差别。
    ax.axhline(rt["direct_k"], color=C_ORANGE, lw=1.8, ls="--", zorder=3)
    ax.text(6.5e-5, rt["direct_k"] * 1.35,
            f"直接预测 $\\mathbf{{K}}_s$   {rt['direct_k'] * 100:.2f}%",
            fontsize=8.6, color=C_ORANGE, ha="left", va="bottom",
            fontweight="bold")

    # 训练网络的实测点。落在扫描线略下方是观测事实(网络误差不是各向同性随机方向),
    # 不作修饰; 竖直虚线把它的横坐标引到轴上并标出 8.97%, 让"形函数自己错了近一成"
    # 这件事看得见——不然读者会以为 0.44% 是形函数的精度。
    ax.plot([rt["net_n"], rt["net_n"]], [3e-9, rt["net_k"]], color=C_BLUE,
            lw=1.0, ls=":", alpha=0.85, zorder=3)
    ax.plot([rt["net_n"]], [rt["net_k"]], marker="*", ms=15.0, color=C_BLUE,
            mec=SURFACE, mew=1.0, zorder=6)
    ax.annotate(f"$\\mathbf{{N}}$ + 式(17)\n{rt['net_k'] * 100:.2f}%",
                xy=(rt["net_n"], rt["net_k"]), xytext=(11, -3),
                textcoords="offset points", fontsize=8.6, color=C_BLUE,
                ha="left", va="top", fontweight="bold", linespacing=1.45)
    ax.text(rt["net_n"], 4.2e-9, f"{rt['net_n'] * 100:.2f}%",
            fontsize=8.2, color=C_BLUE, ha="center", va="bottom")

    ax.set_xlabel(r"形函数相对误差 $\varepsilon_N$")
    ax.set_ylabel(r"缩聚刚度相对误差 $\varepsilon_K$")
    ax.set_xlim(6.0e-5, 0.62)
    ax.set_ylim(3.0e-9, 0.32)
    ax.xaxis.set_major_locator(LogLocator(base=10.0, numticks=5))
    ax.yaxis.set_major_locator(LogLocator(base=10.0, numticks=5))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_minor_formatter(NullFormatter())
    recessive_axes(ax, grid_axis="both")
    ax.tick_params(axis="x", labelsize=10)
    panel_title(ax, "(b) 局部表示精度")

    # ---- (c) 观测刚化的来源构成: 零空间污染 vs 变形子空间拟合 ----
    ax = ax_c
    # 与图 2(c) 同一手法: 100% 构成 + 段内直接标注, 不用图例。份额本身跨 13 个
    # 量级, 但这里编码的是"占误差的多少", 不是量级, 所以线性轴才是对的。
    y = np.arange(len(pol_share))
    # 段内直接标注, 因此不设图例; 每段标在自己最宽的那一行:
    # 橙段在第一行占 96.8%, 蓝段在第二行占满全宽。第二行的橙段宽 3e-11 %,
    # 画不出来, 它的份额只能以文字给出。
    seg_labels = ["刚体零空间伪刚度\n96.8%", "变形子空间拟合\n(污染 " + pol_notes[1] + ")"]
    seg_pos = [(pol_share[0] * 100 - 2.5, 0, "right", "white"),
               (97.5, 1, "right", INK)]
    for yi, s in zip(y, pol_share):
        ax.barh(yi, s * 100, 0.52, color=C_ORANGE, edgecolor=SURFACE,
                linewidth=1.2, zorder=3)
        ax.barh(yi, (1 - s) * 100, 0.52, left=s * 100, color=C_BLUE_L,
                edgecolor=SURFACE, linewidth=1.2, zorder=3)
    for text, (xa, yi, ha, color) in zip(seg_labels, seg_pos):
        ax.text(xa, yi, text, ha=ha, va="center", fontsize=8.6, color=color,
                fontweight="bold", linespacing=1.45, zorder=5)

    ax.set_yticks(y)
    ax.set_yticklabels(pol_labels, fontsize=8.8, linespacing=1.5)
    ax.set_xlabel("占观测刚化的份额 (%)")
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 25, 50, 75, 100])
    # 上界给面板标题留白, 下界腾出结论句的位置; 数值大的一端在下 => 改造前在上,
    # 自上而下读。这里直接给定 ylim, 不用 invert_yaxis(), 后者会被 set_ylim 覆盖。
    ax.set_ylim(2.35, -0.62)
    recessive_axes(ax, grid_axis="x")
    ax.grid(False)                     # 同图 2(c): 网格线会被色块盖掉一半
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    # 本格的结论句: 范数上微不足道的量, 能量后果可以是主导项
    ax.text(50, 1.92, "伪刚度仅为最小非零特征值的 1.6%,\n"
                      "因位移 99.98% 落在该子空间而被放大约 2500 倍",
            fontsize=8.2, color=INK, ha="center", va="center", linespacing=1.5,
            bbox=dict(boxstyle="round,pad=0.32", fc="white", ec=GRID, alpha=0.95))
    panel_title(ax, "(c) 物理结构检查")

    # 脚注必须折行: fig.text 不自动换行, 而 bbox_inches="tight" 会把超出画布的
    # 单行文字连同画布一起撑宽——图 3 的源图宽一旦大于图 2, 缩放比就不同, 三图
    # "印刷字号一致"的前提当场失效(实测单行版把画布从 2438 px 撑到 3587 px,
    # 字号从 9.0 pt 掉到 6.1 pt)。每行控制在图 2 脚注的长度以内。
    footnote(fig, "注：三格均为实测，出处依次为 substructure_elasticity/lagrange_comparison_{2d,3d}.json、\n"
                  "piml_substructure_elasticity/{eq17_second_order, piml_exact_comparison}.json。(b) 两条路线同一算例、"
                  "同一密度分布、同一训练预算（seed 2026，2000 样本／4000 轮），均在 200 样本留出集上取均值。")
    fig.savefig(OUT_FIG3, bbox_inches="tight", pad_inches=0.14)
    plt.close(fig)
    print(f"[out] {OUT_FIG3}")


# ==========================================================================
# 图 4 —— FEALPy 多后端加速比（储备三）
# ==========================================================================

def build_fig4():
    """单面板, 横向条形。

    两个刻意的取舍:

    1. **横向而非纵向。** 图按 15.2 cm 宽固定插入, 单面板要压到 4 cm 出头高
       才不至于吃掉半页, 竖条在这个比例里又矮又胖; 横条正好用满整行宽度,
       后端名当 y 轴刻度也不必再折行成 "NumPy\\n(CPU)"。
    2. **条长编码加速比而非耗时。** 耗时编码时 128 s 一根条独占 94% 轴长,
       两个 GPU 后端挤成看不出差别的短桩——恰好把最该被读出来的对比压没了。
       加速比编码则三根条都可读, ×1.0 的基线短桩是应有之义。绝对耗时不丢,
       写在条端标签里。
    """
    labels, times, speedup = data_backends()

    fig = plt.figure(figsize=(FIG_WIDTH_IN, 2.35), dpi=200, constrained_layout=True)
    if PLACEHOLDER:
        fig.get_layout_engine().set(rect=(0.0, 0.115, 1.0, 1.0))
    ax = fig.subplots(1, 1)

    y = np.arange(len(labels))
    bars = ax.barh(y, speedup, 0.58, color=[C_BLUE, C_ORANGE, C_AQUA],
                   edgecolor=SURFACE, linewidth=1.2, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()                      # NumPy 基线在最上, 自上而下读
    ax.set_xlabel("相对 NumPy (CPU) 的加速比")
    ax.set_xlim(0, speedup.max() * 1.30)
    ax.set_xticks([0, 5, 10, 15])

    for b, t, s in zip(bars, times, speedup):
        ax.text(b.get_width() + speedup.max() * 0.025,
                b.get_y() + b.get_height() / 2,
                f"×{s:.1f}   {t:.1f} s", ha="left", va="center",
                fontsize=10.5, color=INK)

    recessive_axes(ax, grid_axis="x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)

    watermark(fig, "注：为占位示意数据，正式投递前须替换为实测值。")
    fig.savefig(OUT_FIG4, bbox_inches="tight", pad_inches=0.14)
    plt.close(fig)
    print(f"[out] {OUT_FIG4}")


def main():
    setup_font()
    report_print_sizes("图2/3/4", FIG_WIDTH_IN)
    build_fig2()
    build_fig3()
    build_fig4()


if __name__ == "__main__":
    main()
