"""Replot existing probe data; never run a solver or write to the source repository.

Usage (WSL): python plot_stress_hz_summary.py --experiment /path/to/paper_topopt_huzhang
Requires the original experiment's numpy, matplotlib and vtk environment.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--experiment', type=Path, required=True)
parser.add_argument('--results-root', type=Path, help='独立运行结果目录; 缺省读取原始实验结果')
parser.add_argument('--suffix', default='', help='新输出文件后缀, 用于保留已有图件')
parser.add_argument('--column-headings', action='store_true', help='两列统一标题, 子图仅标编号和阶次')
parser.add_argument('--orders', type=int, nargs='+', choices=(2, 3, 4), default=[2, 3, 4])
parser.add_argument('--full-panel-titles', action='store_true', help='子图标题包含完整物理量名称')
parser.add_argument('--panel-labels-only', action='store_true', help='子图仅标注 (a)、(b) 等编号')
parser.add_argument('--quantity-panel-titles', action='store_true', help='子图标注编号与物理量，阶次仅在图注说明')
parser.add_argument('--include-order', action='store_true', help='物理量子图标题同时标明阶次')
args = parser.parse_args()
assert len(set(args.orders)) == len(args.orders)
order_tag = ''.join(map(str, args.orders))
experiment = args.experiment.resolve()
sys.path.insert(0, str(experiment))
import config
if args.results_root is not None:
    config.OUTPUT_DIR = args.results_root.resolve()
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.tri import Triangulation
from plots._base import load_probe_mesh, paper_rcparams

out = Path(__file__).resolve().parents[1] / 'figures'
probe_dir = config.OUTPUT_DIR / 'cantilever-middle-2d-stress/postprocess/discretization_probe'
hashes = {}
def record(path):
    path = path.resolve()
    hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()

for name in ('plots/_base.py', 'plots/stress_cubic_topologies.py',
             'plots/stress_hz_orders_topologies.py', 'plots/stress_traction_jump.py',
             'analysis/discretization_probe.py', 'config.py'):
    record(experiment / name)
for name in ('stress_cubic_topologies.png', 'stress_cubic_convergence.png',
             'stress_hz_orders_topologies.png', 'stress_traction_jump.png'):
    record(out / name)
if args.suffix:
    for name in ('stress_hz_k234_topologies.png', 'stress_hz_traction_statistics.json'):
        record(out / name)

paper_rcparams()
if args.column_headings:
    record(out / 'stress_hz_k234_topologies_all_cells.png')
    fig = plt.figure(figsize=(5.9, 1.6 * len(args.orders) + .2))
    grid = fig.add_gridspec(len(args.orders) + 1, 3, height_ratios=(.14, *([1] * len(args.orders))),
                           width_ratios=(1, 1, .035), hspace=.28, wspace=.08)
    for j, heading in enumerate(('Physical density', 'Apparent von Mises stress ratio')):
        ax = fig.add_subplot(grid[0, j])
        ax.set_axis_off()
        ax.text(.5, .5, heading, ha='center', va='center', fontsize=9)
else:
    fig = plt.figure(figsize=(5.9, 4.7 * len(args.orders) / 3))
    grid = fig.add_gridspec(len(args.orders), 3, width_ratios=(1, 1, .035), hspace=.28, wspace=.08)
rows = []
for i, k in enumerate(args.orders):
    tag = f'huzhang-{k}-pad-solid'
    label = f'huzhang-{k}'
    npz = probe_dir / f'{tag}__fields.npz'
    meta = probe_dir / f'{tag}__probe.json'
    record(npz)
    record(meta)
    provenance = json.loads(meta.read_text(encoding='utf-8'))
    record(config.OUTPUT_DIR / provenance['design_run_dir'] / 'density_final.vtu')
    record(config.OUTPUT_DIR / provenance['design_run_dir'] / 'summary.json')
    points, cells, rho_vtu = load_probe_mesh(probe_dir, tag)
    with np.load(npz) as fields:
        rho = fields['density']
        vm = fields[f'vm_app__{label}']
        jump = fields[f'absjump__{label}']
        mask = (rho > .9) & ~fields['pad_mask'].astype(bool)
    assert cells.shape == (6400, 3)
    np.testing.assert_allclose(rho, rho_vtu, rtol=1e-12, atol=1e-14)
    assert np.isfinite(vm).all() and np.isfinite(jump).all() and (jump >= 0).all()
    values = jump[mask]
    row = dict(k=k, solid_cells=int(mask.sum()), median=float(np.median(values)),
               p95=float(np.quantile(values, .95, method='linear')), maximum=float(values.max()))
    rows.append(row)
    tri = Triangulation(points[:, 0], points[:, 1], cells)
    for j, (values_plot, cmap, title) in enumerate(((rho, 'gray_r', 'Density'), (vm, 'jet', 'Stress ratio'))):
        row_index = i + int(args.column_headings)
        ax = fig.add_subplot(grid[row_index, j])
        artist = ax.tripcolor(tri, facecolors=values_plot, cmap=cmap, vmin=0, vmax=1, edgecolors='none', rasterized=True)
        ax.set_aspect('equal')
        ax.set_axis_off()
        panel_title = f'({chr(97+2*i+j)}) $k={k}$'
        if args.full_panel_titles:
            title = ('Physical density', 'Apparent von Mises stress ratio')[j]
        display_title = panel_title if args.column_headings else f'{panel_title}: {title}'
        if args.panel_labels_only:
            display_title = f'({chr(97+2*i+j)})'
        if args.quantity_panel_titles:
            quantity = ('Final physical density',
                        r'Apparent von Mises stress ratio $\sigma_{\mathrm{vm}}/\bar\sigma$')[j]
            display_title = f'({chr(97+2*i+j)}) {quantity}'
            if args.include_order:
                display_title = f'{panel_title}: {quantity}'
        ax.set_title(display_title,
                     fontsize=8 if (args.full_panel_titles or args.quantity_panel_titles) else 9, pad=4)
    cb = fig.colorbar(artist, cax=fig.add_subplot(grid[row_index, 2]), ticks=np.linspace(0, 1, 6))
    cb.ax.tick_params(labelsize=8, length=2)
fig.savefig(out / f'stress_hz_k{order_tag}_topologies{args.suffix}.png', dpi=600, bbox_inches='tight', pad_inches=.04)
plt.close(fig)
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == h for p, h in hashes.items())
report = dict(mask='density > 0.9 and not pad_mask; count cells, not unique faces',
              indicator='A_e = max of internal-face traction-jump RMS / sigma_bar; sigma_bar = 180',
              quantile_method='numpy.quantile(method=linear)', rows=rows,
              source_files_sha256=hashes, source_files_unchanged=True)
stats_tag = '' if args.orders == [2, 3, 4] else f'_k{order_tag}'
(out / f'stress_hz_traction_statistics{stats_tag}{args.suffix}.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
print(json.dumps(rows, indent=2))
