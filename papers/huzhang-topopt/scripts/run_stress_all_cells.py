"""使用现有 SOPTX driver 运行全受约束单元验收, 原始代码与结果只读.

运行方式
--------
WSL ihpcm Python: run_stress_all_cells.py --order 2 (依次运行 2, 3, 4).
独立结果写入论文目录下 results/stress-all-cells, 不支持覆盖已有阶次目录.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import os

sys.dont_write_bytecode = True
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--order', type=int, choices=(2, 3, 4), required=True)
parser.add_argument('--run-name', default='stress-all-cells', help='独立结果目录名')
parser.add_argument('--threads', type=int, default=1, help='BLAS/OpenMP 线程数, 缺省为 1')
args = parser.parse_args()
assert args.threads >= 1
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[key] = str(args.threads)
repo = Path('/home/brighthe/codespace/soptx')
experiment = repo / 'experiments/paper_topopt_huzhang'
assert Path(args.run_name).name == args.run_name
root = Path(__file__).resolve().parents[1] / 'results' / args.run_name
root.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(experiment))
path = experiment / 'run_cantilever_stress.py'
source = path.read_text(encoding='utf-8')
# 核心优化器已支持 None; driver 终态复核原来直接对阈值作数值比较, 在此同步口径.
old = 'solid = rho >= ACCEPTANCE_SOLID_THRESHOLD'
new = 'solid = (~to_np(parts["pad_mask"]).astype(bool) if ACCEPTANCE_SOLID_THRESHOLD is None else rho >= ACCEPTANCE_SOLID_THRESHOLD)'
assert source.count(old) == 1
source = source.replace(old, new)
namespace = dict(__name__='stress_all_cells_driver', __file__=str(path))
exec(compile(source, str(path), 'exec'), namespace)
namespace['ACCEPTANCE_SOLID_THRESHOLD'] = None
namespace['OUTPUT_DIR'] = root / namespace['CASE_ID']
namespace['VIEW_ROOT'] = root / 'frames'
label = namespace['run_label']('huzhang', args.order)
target = namespace['OUTPUT_DIR'] / label
assert not target.exists(), f'拒绝覆盖已有结果: {target}'
target.mkdir(parents=True)
files = [path, *sorted((repo/'src/soptx').rglob('*.py'))]
hashes = {str(p.relative_to(repo)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(target/'source_manifest.json').write_text(json.dumps(hashes, indent=2)+'\n', encoding='utf-8')
(target/'driver_effective.py').write_text(source, encoding='utf-8')
(target/'protocol.json').write_text(json.dumps(dict(acceptance_solid_threshold=None,
    acceptance='all non-exempt cells', initial_density=namespace['INITIAL_DENSITY'],
    exact_restart=False, order=args.order, output_dir=str(namespace['OUTPUT_DIR']),
    view_root=str(namespace['VIEW_ROOT']), threads={key: os.environ.get(key) for key in
    ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS')}), indent=2)+'\n', encoding='utf-8')
status = namespace['main'](['--analyzer', 'huzhang', '--order', str(args.order)])
changed = [name for name,h in hashes.items() if hashlib.sha256((repo/name).read_bytes()).hexdigest()!=h]
(target/'source_verification.json').write_text(json.dumps(dict(changed_during_run=changed),indent=2)+'\n', encoding='utf-8')
raise SystemExit(status)
