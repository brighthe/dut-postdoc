"""Restore Fig. 5.9 from the all-cell k=3 run; original inputs are read-only.

Run with the SOPTX Python environment, passing --experiment. A single frozen
state solve extracts centroid principal stresses; no optimization is performed.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

for key in ('BLIS_NUM_THREADS', 'OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[key] = '1'
sys.dont_write_bytecode = True
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--experiment', type=Path, required=True)
parser.add_argument('--quantity-titles', action='store_true', help='Replot saved arrays with descriptive panel titles')
args = parser.parse_args()
experiment = args.experiment.resolve()
paper = Path(__file__).resolve().parents[1]
root = paper / 'results/stress-all-cells-blis1'
case = root / 'cantilever-middle-2d-stress'
run = case / 'analyzer-huzhang__lfem_constraint-apparent__load_pad_radius-1.5__order-3__solid_thr-None'
old_probe = case / 'postprocess/discretization_probe/huzhang-3-pad-solid__fields.npz'
original_stem = paper / 'figures/stress_hz_k3_convergence_all_cells'
stem = original_stem.with_name(original_stem.name + '_quantity_titles') if args.quantity_titles else original_stem
hashes = {}
def record(path):
    hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
for path in (run / 'history.json', run / 'summary.json', run / 'density_final.vtu',
             old_probe, paper / 'figures/stress_cubic_convergence.png',
             experiment / 'run_cantilever_stress.py', experiment / 'config.py',
             experiment / 'analysis/discretization_probe.py', experiment / 'plots/_base.py'):
    record(path)
for path in (experiment.parents[1] / 'src').rglob('*.py'):
    record(path)
sys.path.insert(0, str(experiment))
import config
config.OUTPUT_DIR = root
config.VIEW_DIR = root / 'probe-views'
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from analysis import discretization_probe as probe
from plots._base import paper_rcparams
from soptx.backend import backend_manager as bm

bm.set_backend('numpy')
rho, summary = probe.load_design(run)
assert summary['acceptance_solid_threshold'] is None
if args.quantity_titles:
    record(original_stem.with_suffix('.npz'))
    record(original_stem.with_suffix('.png'))
    with np.load(original_stem.with_suffix('.npz')) as saved:
        np.testing.assert_array_equal(rho, saved['density'])
        keep = saved['accepted_mask'].astype(bool)
        sig1, sig2, vm, g = (saved[key].copy() for key in ('sig1', 'sig2', 'vm', 'g'))
    assert keep.sum() == 6384
else:
    result = probe.evaluate('huzhang', 3, rho)
    pad = probe.pad_mask_from_summary(result['pipeline'].mesh, summary, len(rho))
    keep = ~pad
    assert keep.sum() == 6384
    stress = probe._apparent_stress_huzhang(result['pipeline'], result['state'],
        bm.arange(len(rho)), bm.array([[1/3, 1/3, 1/3]]))[:, 0, :]
    stress /= probe.run_cantilever_stress.STRESS_LIMIT
    xx, yy, xy = stress.T
    mid = (xx + yy) / 2
    rad = np.sqrt(((xx - yy) / 2)**2 + xy**2)
    sig1, sig2 = mid + rad, mid - rad
    vm = np.sqrt(sig1**2 - sig1*sig2 + sig2**2)
    g = result['constraint_value']
with np.load(old_probe) as old:
    # The solver floors squared von Mises stress at 1e-12 before taking
    # the square root. Principal stresses retain the unfloored tensor values.
    vm_floor = 1e-6 / probe.run_cantilever_stress.STRESS_LIMIT
    np.testing.assert_allclose(np.maximum(vm, vm_floor), old['vm_app__huzhang-3'],
                               rtol=1e-6, atol=1e-12)
    np.testing.assert_allclose(g, old['g__huzhang-3'], rtol=1e-6, atol=1e-9)
    np.testing.assert_array_equal(keep, old['accepted_mask'])
history = json.loads((run / 'history.json').read_text())
steps = np.asarray(history['iter_indices'])
scalars = history['scalar_histories']
volume = np.asarray(scalars['volfrac'])
gmax = np.asarray(scalars['max_relative_violation_solid'])
np.testing.assert_allclose(gmax, scalars['max_relative_violation'])
np.testing.assert_allclose(volume[-1], summary['volume_fraction'])
np.testing.assert_allclose(gmax[-1], g[keep].max(), rtol=1e-6, atol=1e-9)
assert len(steps) == 315 and (gmax > 0).all()
tol = summary['relative_stress_tolerance']
assert g[keep].max() <= tol

paper_rcparams()
fig = plt.figure(figsize=(5.9, 2.65))
grid = fig.add_gridspec(1, 2, width_ratios=(1.25, 1), wspace=.65,
                       left=.10, right=.90, bottom=.18, top=.88)
ax = fig.add_subplot(grid[0, 0])
blue, green = '#1f77b4', '#2ca02c'
lv, = ax.plot(steps, volume, color=blue, lw=1.1, label='$f_V$')
ax.set(xlabel='MMA iteration', ylabel='Volume fraction $f_V$', ylim=(.30, .70))
ax.yaxis.label.set_color(blue)
ax.set_title('(a) Optimization history' if args.quantity_titles else '(a) $k=3$', fontsize=8 if args.quantity_titles else 9)
ax.grid(ls=':', lw=.5, alpha=.5)
tw = ax.twinx()
lg, = tw.plot(steps, gmax, color=green, lw=.9, ls='--', label=r'$g_{\max}$')
lt = tw.axhline(tol, color=green, lw=.9, ls=':', label=rf'$\delta_g={tol:g}$')
tw.set(yscale='log', ylim=(min(tol, gmax.min())*.5, gmax.max()*2),
       ylabel=r'Max. local constraint $g_{\max}$')
tw.yaxis.label.set_color(green)
tw.legend(handles=[lv, lg, lt], loc='upper right', fontsize=7, framealpha=.95)
ax2 = fig.add_subplot(grid[0, 1])
theta = np.linspace(0, 2*np.pi, 500)
c, s = np.cos(theta), np.sin(theta)
scale = np.sqrt(c*c-c*s+s*s)
ellipse, = ax2.plot(c/scale, s/scale, color='#d62728', lw=1,
                    label=r'$\sigma_{\mathrm{vm}}=\bar\sigma$')
# Draw small stresses first so the dense cluster at the origin does not hide
# the higher-stress cells. All constrained cells remain in the scatter data.
indices = np.flatnonzero(keep)
indices = indices[np.argsort(vm[indices])]
scatter = ax2.scatter(sig1[indices], sig2[indices], c=vm[indices],
                      cmap='jet', vmin=0, vmax=1, s=2.5, linewidths=0, rasterized=True)
proxy = Line2D([], [], ls='none', marker='o', ms=3, color='#ff9900',
               label=r'Constrained cells ($\mathcal{E}_{\mathrm{acc}}$)')
ax2.legend(handles=[ellipse, proxy], loc='upper left', fontsize=6,
           borderpad=.3, handlelength=1.2, framealpha=.95)
ax2.set(xlim=(-1.5, 1.5), ylim=(-1.5, 1.9), aspect='equal',
        xlabel=r'$\sigma_1/\bar\sigma$', ylabel=r'$\sigma_2/\bar\sigma$')
ax2.set_title('(b) Final principal stress distribution' if args.quantity_titles else '(b) $k=3$', fontsize=8 if args.quantity_titles else 9)
ax2.grid(ls=':', lw=.5, alpha=.5)
cb = fig.colorbar(scatter, cax=ax2.inset_axes([1.05, 0, .05, 1]), ticks=np.linspace(0, 1, 6))
cb.set_label(r'$\sigma_{\mathrm{vm}}/\bar\sigma$', fontsize=8)
cb.ax.tick_params(labelsize=7)
for axis in (ax, tw, ax2):
    axis.tick_params(labelsize=7)
    axis.xaxis.label.set_size(8)
    axis.yaxis.label.set_size(8)
fig.savefig(stem.with_suffix('.png'), dpi=600, bbox_inches='tight', pad_inches=.04)
plt.close(fig)
np.savez_compressed(stem.with_suffix('.npz'), iterations=steps, volfrac=volume,
    gmax=gmax, density=rho, accepted_mask=keep, sig1=sig1, sig2=sig2, vm=vm, g=g)
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == h for p, h in hashes.items())
report = dict(order=3, iterations=len(steps), accepted_cells=int(keep.sum()),
    volume_fraction=float(volume[-1]), max_g=float(g[keep].max()), tolerance=tol,
    max_vm_ratio=float(vm[keep].max()), principal_stress_order='sig1 >= sig2',
    evaluation='element centroid; apparent stress / stress limit; no density cutoff',
    vm_comparison_floor=vm_floor,
    frozen_reanalysis_matches_saved_probe=True, source_files_unchanged=True,
    source_files_sha256=hashes)
stem.with_suffix('.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k != 'source_files_sha256'}, indent=2))
