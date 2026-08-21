#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成申请书第 3 部分图 1：PIML–Matrix-Free 求解与 GPU 协同加速总体技术路线图。

旧版由 mermaid 导出，纸面高宽比约 3.7:1，四段容器不对齐、线细字瘦，
按 15.2 cm 插入后印刷字号偏低。本脚本按图 2/3/4 同一源图宽与配色重画：
四段等高对齐，主路径实线、回退虚线，印刷字号目标 >= 7 pt。
严格匿名，不出现姓名、单位或导师信息。
"""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "fig1_technical_route.png")

DOCX_WIDTH_IN = 15.2 / 2.54
FIG_WIDTH_IN = 8.0
FIG_HEIGHT_IN = 3.05

SURFACE = "#ffffff"
PANEL = "#f6f5f2"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#dcdbd6"
C_BLUE = "#2a78d6"
C_ORANGE = "#eb6834"
C_AQUA = "#1baf7a"
C_PURPLE = "#5b4aa8"
C_RED = "#c43c3c"

FONT_CANDIDATES = [
    (r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\msyhbd.ttc"),
    ("/mnt/c/Windows/Fonts/msyh.ttc", "/mnt/c/Windows/Fonts/msyhbd.ttc"),
    ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
     "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
    ("/System/Library/Fonts/PingFang.ttc", None),
]


def setup_font():
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
        print(f"[font] {name}  ({regular})")
        return name
    print("[font] 警告: 未找到中文字体")
    return None


def round_box(ax, x, y, w, h, fc, ec, lw=1.4, radius=0.08, z=2):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.0,rounding_size={radius}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z,
        mutation_aspect=1.0,
    )
    ax.add_patch(patch)
    return patch


def arrow(ax, p0, p1, color=INK, lw=1.8, style="-|>", rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(
        p0, p1, arrowstyle=style, mutation_scale=12,
        linewidth=lw, color=color, linestyle=ls,
        connectionstyle=f"arc3,rad={rad}", zorder=5,
        shrinkA=0, shrinkB=0,
    ))


def build_fig1():
    fig, ax = plt.subplots(figsize=(FIG_WIDTH_IN, FIG_HEIGHT_IN), dpi=240)
    ax.set_xlim(0.0, 12.0)
    ax.set_ylim(0.0, 4.55)
    ax.axis("off")
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    colors = [C_BLUE, C_ORANGE, C_AQUA, C_PURPLE]
    titles = [
        "①  统一基线",
        "②  PIML–Matrix-Free\n重构",
        "③  多后端与 GPU\n并行求解",
        "④  拓扑演化\n可靠闭环",
    ]
    cards = [
        ["2D / 3D 拓扑优化定义", "精确组装 / Matrix-Free 基线"],
        ["PIML 局部表示预测", "Matrix-Free 算子按需作用\n局部作用 + 全局累加"],
        ["多后端数据驻留与批处理", "并行预条件 Krylov 求解器"],
        ["残差检测与精确回退", "消融对照与端到端验证"],
    ]

    n = 4
    margin, gap = 0.12, 0.46
    sw = (12.0 - 2 * margin - (n - 1) * gap) / n
    xs = [margin + i * (sw + gap) for i in range(n)]
    y0, y1 = 0.92, 4.42
    header_h = 0.92
    inner_gap = 0.10
    body_top = y1 - header_h - 0.10
    body_bot = y0 + 0.12
    card_h = (body_top - body_bot - inner_gap) / 2.0

    for i, (x, color, title, (c1, c2)) in enumerate(zip(xs, colors, titles, cards)):
        round_box(ax, x, y0, sw, y1 - y0, PANEL, GRID, lw=1.15, radius=0.10, z=1)
        round_box(ax, x, y1 - header_h, sw, header_h, color, color, lw=0.8, radius=0.10, z=3)
        # cover the lower rounded corners of the header so it sits flush on the panel
        ax.add_patch(plt.Rectangle((x, y1 - header_h), sw, 0.16, facecolor=color,
                                   edgecolor="none", zorder=3))
        ax.text(x + sw / 2.0, y1 - header_h / 2.0, title,
                ha="center", va="center", fontsize=10.2, color=SURFACE,
                fontweight="bold", zorder=4)

        cy1 = body_top - card_h
        cy2 = body_bot
        for cy, text in ((cy1, c1), (cy2, c2)):
            round_box(ax, x + 0.10, cy, sw - 0.20, card_h, SURFACE, color,
                      lw=1.55, radius=0.07, z=3)
            ax.text(x + sw / 2.0, cy + card_h / 2.0, text,
                    ha="center", va="center", fontsize=9.4, color=INK,
                    linespacing=1.35, zorder=4)

        mid_x = x + sw / 2.0
        arrow(ax, (mid_x, cy1), (mid_x, cy2 + card_h), color=color, lw=1.5)

        if i < n - 1:
            x_from = x + sw
            x_to = xs[i + 1]
            y_arr = (cy1 + cy2 + card_h) / 2.0
            arrow(ax, (x_from + 0.04, y_arr), (x_to - 0.04, y_arr),
                  color=INK, lw=1.9)

    # 回退：第 4 段底部回到第 2 段底部（与正文“精确回退”对应）
    x2c = xs[1] + sw / 2.0
    x4c = xs[3] + sw / 2.0
    y_loop = 0.38
    ax.plot([x4c, x4c, x2c, x2c], [y0, y_loop, y_loop, y0],
            color=C_RED, lw=1.7, ls=(0, (4.0, 2.2)), zorder=5, solid_capstyle="butt")
    ax.annotate(
        "", xy=(x2c, y0 - 0.01), xytext=(x2c, y_loop + 0.12),
        arrowprops=dict(arrowstyle="-|>", color=C_RED, lw=1.7,
                        mutation_scale=11),
        zorder=6,
    )
    ax.text((x2c + x4c) / 2.0, y_loop + 0.16, "残差超限  /  精确回退",
            ha="center", va="bottom", fontsize=8.8, color=C_RED,
            fontweight="bold", zorder=6)

    scale = DOCX_WIDTH_IN / FIG_WIDTH_IN
    print(f"[scale] 源图 {FIG_WIDTH_IN}×{FIG_HEIGHT_IN} in -> 纸面 "
          f"{DOCX_WIDTH_IN:.2f}×{FIG_HEIGHT_IN * scale:.2f} in "
          f"({15.2:.1f}×{FIG_HEIGHT_IN * scale * 2.54:.2f} cm), 缩放比 {scale:.2f}")
    for src, name in ((10.2, "段标题"), (9.4, "卡片正文"), (8.8, "回退标注")):
        print(f"[scale]   {name:8s} {src:4.1f}pt -> {src * scale:4.1f}pt")

    fig.savefig(OUT, dpi=240, bbox_inches="tight", pad_inches=0.06,
                facecolor=SURFACE)
    plt.close(fig)
    print(f"[out] {OUT}")


if __name__ == "__main__":
    setup_font()
    build_fig1()
