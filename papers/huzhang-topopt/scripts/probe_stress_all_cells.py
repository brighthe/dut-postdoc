"""对全单元验收的新运行进行独立终态复核, 保存约束和牵引跳量证据."""
from pathlib import Path
import argparse
import json
import sys
import hashlib
import numpy as np

sys.dont_write_bytecode = True
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--order', type=int, choices=(2,3,4), required=True)
parser.add_argument('--run-name', default='stress-all-cells')
args = parser.parse_args()
experiment = Path('/home/brighthe/codespace/soptx/experiments/paper_topopt_huzhang')
assert Path(args.run_name).name == args.run_name
root = Path(__file__).resolve().parents[1] / 'results' / args.run_name
sys.path.insert(0, str(experiment))
import config
config.OUTPUT_DIR = root
config.VIEW_DIR = root / 'probe-views'
from analysis import discretization_probe as probe
from soptx.backend import backend_manager as bm

bm.set_backend('numpy')
label = f'analyzer-huzhang__lfem_constraint-apparent__load_pad_radius-1.5__order-{args.order}__solid_thr-None'
run = root / probe.CASE_ID / label
assert (run/'summary.json').exists(), '优化尚未完成'
probe.OUTPUT_DIR = root
probe.VIEW_DIR = root / 'probe-views'
payload, fields, mesh = probe.probe_design(run)
assert all(c['passed'] for c in payload['checks'].values()), payload['checks']
pad = fields['pad_mask'].astype(bool)
g = fields[f'g__huzhang-{args.order}']
assert np.isfinite(g).all()
payload['all_constrained_review'] = dict(count=int((~pad).sum()),
    max_g=float(g[~pad].max()), above_tolerance=int((g[~pad] > probe.DELTA_G).sum()),
    tolerance=probe.DELTA_G, density_cutoff=None)
payload['probe_source_sha256'] = hashlib.sha256(Path(probe.__file__).read_bytes()).hexdigest()
probe.write_outputs(payload, fields, mesh)
probe.print_markdown(payload)
print(json.dumps(payload['all_constrained_review']))
