"""Test the Origin glWater3D template with synthetic shared-X data."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

RUNTIME = Path(__file__).resolve().parents[1] / 'embedded/editaplot/runtime/src'
sys.path.insert(0, str(RUNTIME))
from origin_sciplot.origin_backend.execution_context import require_interactive_origin_context
from origin_sciplot.origin_backend.job_queue import origin_job_slot
from origin_sciplot.origin_backend.session import OriginSession


def graph_state(op):
    graph = op.find_graph('NativeWaterfall')
    if not graph:
        raise RuntimeError('The saved graph could not be found')
    layer = graph[0]
    state = {'is3D': layer.get_int('is3D'), 'is3DGL': layer.get_int('is3DGL'),
             'coortype': layer.get_int('coortype'), 'plots': len(layer.plot_list())}
    if state != {'is3D': 1, 'is3DGL': 1, 'coortype': 16, 'plots': 3}:
        raise RuntimeError(f'Unexpected graph state: {state}')
    return graph, state


def create(op, output):
    sheet = op.new_sheet('w', lname='Synthetic')
    sheet.get_book().name = 'SyntheticSource'
    sheet_ref = sheet.lt_range()
    x = [float(i) for i in range(121)]
    columns = [x] + [[2 + .6*j + .4*math.sin(i/12+j) for i in range(121)] for j in range(3)]
    for i, values in enumerate(columns):
        sheet.from_list(i, values, lname='Time' if i == 0 else f'Series {i}', axis='X' if i == 0 else 'Y')
    sheet.activate()
    command = 'plotxy iy:=(1,2:4) plot:=210 ogl:=<new template:=glWater3D>;'
    if not op.lt_exec(command):
        raise RuntimeError('Origin plotxy could not create the 3D Waterfall')
    graph = op.find_graph()
    if not graph:
        raise RuntimeError('Origin did not create a graph')
    graph.name = 'NativeWaterfall'
    _, before = graph_state(op)
    if not op.save(str(output / 'native-waterfall.opju')):
        raise RuntimeError('Origin could not save the project')
    if not op.open(str(output / 'native-waterfall.opju'), asksave=False):
        raise RuntimeError('Origin could not reopen the project')
    graph, after = graph_state(op)
    sheet = op.find_sheet('w', sheet_ref)
    if sheet is None:
        raise RuntimeError('Saved source sheet is missing')
    for i, expected in enumerate(columns):
        values = sheet.to_list(i)
        if len(values) != len(expected) or not all(math.isclose(a, b, abs_tol=1e-12, rel_tol=1e-12) for a, b in zip(values, expected)):
            raise RuntimeError('Saved source values differ from the synthetic input')
    exports = {}
    for extension in ('png', 'pdf', 'tif'):
        path = output / f'native-waterfall.{extension}'
        graph.save_fig(str(path), width=1600)
        if not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError(f'Missing {extension} export')
        exports[extension] = {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    return {'template': 'glWater3D', 'command': command, 'before': before, 'after': after,
            'reopened_synthetic_values': True, 'exports': exports, 'visual_qa': 'pending'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True, help='New empty destination for the synthetic probe')
    args = parser.parse_args()
    output = args.output_dir.resolve()
    if output.exists():
        raise FileExistsError('Choose a new output directory; existing files are preserved')
    require_interactive_origin_context()
    output.mkdir(parents=True, exist_ok=False)
    with origin_job_slot(job_kind='native-waterfall-demo'):
        with OriginSession(keep_open=False) as session:
            result = create(session.op, output)
            result['environment'] = session.environment.to_dict()
            (output / 'probe.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
            print(json.dumps({'template': result['template'], 'saved_reopened': True,
                              'native_3d': result['after']['is3DGL'] == 1,
                              'values_checked': True, 'visual_qa': 'pending'}), flush=True)


if __name__ == '__main__':
    main()
