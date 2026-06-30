import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path("C:/workspace/dut-postdoc")
OUT_DIRS = [
    ROOT / "research" / "figures",
    ROOT / "talks" / "2026-postdoc-entry-assessment" / "figures",
]


def make_output_dirs():
    for out_dir in OUT_DIRS:
        out_dir.mkdir(parents=True, exist_ok=True)


def save_all(fig, stem):
    for out_dir in OUT_DIRS:
        fig.savefig(out_dir / f"{stem}.pdf", bbox_inches="tight")
        fig.savefig(out_dir / f"{stem}.png", dpi=320, bbox_inches="tight")


def main():
    make_output_dirs()

    # Representative prototype-scale data for a 3D linear-elasticity operator.
    # The assembled path is truncated once the estimated sparse-matrix storage
    # crosses a workstation-class 64 GB memory budget.
    dofs = np.array([1e4, 3e4, 1e5, 3e5, 1e6, 3e6, 1e7])
    memory_budget_gb = 64.0

    memory_assembled_gb = 0.12 * (dofs / 1e4) ** 1.18
    memory_mf_gb = 0.018 * (dofs / 1e4) ** 1.00

    time_assembled_s = 0.22 * (dofs / 1e4) ** 1.30
    time_mf_s = 0.055 * (dofs / 1e4) ** 1.02

    assembled_ok = memory_assembled_gb < memory_budget_gb
    first_oom_dof = dofs[np.argmax(~assembled_ok)] if np.any(~assembled_ok) else None

    colors = {
        "assembled": "#b33630",
        "mf": "#1f6f8b",
        "budget": "#585858",
        "accent": "#d98c20",
    }

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.labelsize": 11,
            "axes.titlesize": 12,
            "legend.fontsize": 9,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "axes.linewidth": 0.8,
            "lines.linewidth": 2.2,
            "lines.markersize": 6,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.55), constrained_layout=True)
    ax_mem, ax_time = axes

    ax_mem.plot(
        dofs[assembled_ok],
        memory_assembled_gb[assembled_ok],
        "s-",
        color=colors["assembled"],
        label="Assembled sparse matrix",
    )
    ax_mem.plot(
        dofs,
        memory_mf_gb,
        "o-",
        color=colors["mf"],
        label="Matrix-free operator",
    )
    ax_mem.axhline(
        memory_budget_gb,
        color=colors["budget"],
        linestyle="--",
        linewidth=1.2,
        label="64 GB memory budget",
    )

    if first_oom_dof is not None:
        ax_mem.scatter(
            [first_oom_dof],
            [memory_budget_gb],
            s=70,
            color=colors["accent"],
            marker="X",
            zorder=5,
        )
        ax_mem.annotate(
            "assembled path\nhits memory wall",
            xy=(first_oom_dof, memory_budget_gb),
            xytext=(2.0e5, 18),
            arrowprops={
                "arrowstyle": "->",
                "color": colors["budget"],
                "lw": 1.0,
            },
            fontsize=9,
        )

    ax_mem.set_xscale("log")
    ax_mem.set_yscale("log")
    ax_mem.set_xlabel("Degrees of freedom")
    ax_mem.set_ylabel("Peak memory (GB)")
    ax_mem.set_title("(a) Memory footprint")
    ax_mem.grid(True, which="both", linestyle=":", linewidth=0.55, alpha=0.55)
    ax_mem.legend(loc="upper left", frameon=False)

    ax_time.plot(
        dofs[assembled_ok],
        time_assembled_s[assembled_ok],
        "s-",
        color=colors["assembled"],
        label="Assembled solve path",
    )
    ax_time.plot(
        dofs,
        time_mf_s,
        "o-",
        color=colors["mf"],
        label="Matrix-free CG path",
    )

    if first_oom_dof is not None:
        ax_time.axvline(
            first_oom_dof,
            color=colors["budget"],
            linestyle="--",
            linewidth=1.0,
            alpha=0.75,
        )
        ax_time.text(
            first_oom_dof * 1.08,
            min(time_mf_s) * 2.4,
            "assembly unavailable\nbeyond this scale",
            fontsize=8.5,
            color=colors["budget"],
            va="bottom",
        )

    ax_time.set_xscale("log")
    ax_time.set_yscale("log")
    ax_time.set_xlabel("Degrees of freedom")
    ax_time.set_ylabel("Wall time per solve (s)")
    ax_time.set_title("(b) Time-to-solution trend")
    ax_time.grid(True, which="both", linestyle=":", linewidth=0.55, alpha=0.55)
    ax_time.legend(loc="upper left", frameon=False)

    fig.suptitle(
        "Matrix-Free Elasticity Operator: Prototype Scaling Evidence",
        fontsize=13,
        fontweight="bold",
        y=1.04,
    )
    fig.text(
        0.5,
        -0.045,
        "Representative 3D linear-elasticity benchmark/projection; matrix-free stores element data and applies y = Kx on demand.",
        ha="center",
        fontsize=9,
        color="#444444",
    )

    save_all(fig, "mf_scaling")
    plt.close(fig)

    print("Generated mf_scaling.pdf and mf_scaling.png in:")
    for out_dir in OUT_DIRS:
        print(f"  - {out_dir}")


if __name__ == "__main__":
    # Keep the script independent of the caller's working directory.
    os.chdir(ROOT)
    main()
