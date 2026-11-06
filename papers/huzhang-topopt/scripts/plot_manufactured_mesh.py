"""绘制制造解算例的实际网格与边界划分.

Notes
-----
直接调用收敛实验使用的网格工厂, 不组装或求解状态方程.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from soptx.backend import backend_manager as bm
from soptx.mesh import TriangleMesh

def main():
    """生成 n_x = 4 的棋盘格三角形网格图并保存 PNG 与 SVG."""
    bm.set_backend("numpy")
    mesh = TriangleMesh.from_checkerboard_box(box=[0, 1, 0, 1], nx=4, ny=4)
    node = bm.to_numpy(mesh.entity("node"))
    cell = bm.to_numpy(mesh.entity("cell"))
    plt.rcParams.update({"font.family": "serif", "font.size": 12,
                         "mathtext.fontset": "stix", "svg.fonttype": "none"})
    fig, ax = plt.subplots(figsize=(5.5, 5.1))
    ax.triplot(node[:, 0], node[:, 1], cell, color="0.32", linewidth=0.85)
    blue, red = "#2166ac", "#b35806"
    ax.plot([0, 0, 1], [1, 0, 0], color=blue, linewidth=2.2)
    ax.plot([0, 1, 1], [1, 1, 0], color=red, linewidth=2.2, linestyle="--")
    ax.text(-0.08, 0.5, r"$\Gamma_D:\ \mathbf{u}=\mathbf{0}$",
            color=blue, rotation=90, ha="center", va="center")
    ax.text(0.5, -0.10, r"$\Gamma_D:\ \mathbf{u}=\mathbf{0}$",
            color=blue, ha="center", va="center")
    ax.text(0.5, 1.09, r"$\Gamma_N:\ \mathbf{g}=\boldsymbol{\sigma}\mathbf{n}$",
            color=red, ha="center", va="center")
    ax.text(1.10, 0.5, r"$\Gamma_N:\ \mathbf{g}=\boldsymbol{\sigma}\mathbf{n}$",
            color=red, rotation=90, ha="center", va="center")
    ax.text(-0.025, -0.025, r"$0$", ha="right", va="top")
    ax.text(1, -0.025, r"$1$", ha="center", va="top")
    ax.text(-0.025, 1, r"$1$", ha="right", va="center")
    ax.annotate("", xy=(0.35, -0.23), xytext=(0.15, -0.23),
                arrowprops={"arrowstyle": "->", "lw": 1})
    ax.annotate("", xy=(0.15, -0.14), xytext=(0.15, -0.23),
                arrowprops={"arrowstyle": "->", "lw": 1})
    ax.text(0.37, -0.23, r"$x$", va="center")
    ax.text(0.12, -0.15, r"$y$", ha="right", va="center")
    ax.set(xlim=(-0.18, 1.22), ylim=(-0.29, 1.20), aspect="equal")
    ax.axis("off")
    fig.tight_layout(pad=0.3)
    output = Path(__file__).resolve().parents[1] / "figures"
    for suffix in ("png", "svg"):
        fig.savefig(output / f"manufactured_mesh.{suffix}", dpi=300,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"vertices={len(node)}, triangles={len(cell)}; output={output}")

if __name__ == "__main__":
    main()
