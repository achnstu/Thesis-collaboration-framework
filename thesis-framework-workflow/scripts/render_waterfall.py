"""Render a portable CSV manifest through the bundled EditaPlot Origin backend."""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import platform
import struct
import sys

from waterfall_inputs import candidate_target, check_hashes, load_manifest, set_time_geometry


def import_style():
    path = Path(__file__).with_name('origin_waterfall_style.py')
    spec = importlib.util.spec_from_file_location('waterfall_style', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def tables(op, panels):
    for i, panel in enumerate(panels):
        raw = op.new_book('w', f'Source{i+1:03d}')[0]
        raw.from_list(0, panel['x'], lname='Source time', axis='X')
        raw.from_list(1, panel['raw_y'], lname='Source value', axis='Y')
        sheet = op.new_book('w', f'ep{i+1:03d}')[0]
        sheet.from_list(0, panel['x'], lname='Real time', axis='X')
        sheet.from_list(1, panel['y'], lname='Scaled value', axis='Y')


def render(config, panels, hashes, target):
    import numpy as np

    style = import_style()
    factor = set_time_geometry(style, panels, config['time_ticks'])
    style.STEM = target.name
    style.FILL_TRANSPARENCY = config.get('fill_transparency_percent', 75)
    style.COLORS = [panel.get('color') or style.COLORS[i] for i, panel in enumerate(panels)]
    style.require_interactive_origin_context()
    target.parent.mkdir(parents=True, exist_ok=False)
    with style.origin_job_slot(job_kind='portable-perspective-waterfall'):
        with style.OriginSession(keep_open=False) as session:
            op = session.op
            tables(op, panels)
            expected = style.originals(op)
            graph = op.new_graph('PerspectiveWaterfall', template='Line')
            graph.name = 'PerspectiveWaterfall'
            layer = style.configure(op, graph)
            reference = style.reference_planes(op, layer)
            print('Built native reference planes.', flush=True)
            records = [style.trace(op, layer, i) for i in reversed(range(8))]
            theta = math.radians(style.ANGLE_X)
            pos = style.offset(style.project(style.TIME_MAX / 2, 0, 0),
                               .90 * math.sin(theta), -.90 * math.cos(theta))
            style.label(op, layer, 'TimeTitle', config.get('x_title', 'Time (s)'), *pos, 10, style.ANGLE_X)
            style.label(op, layer, 'LoadTitle', config.get('y_title', 'Value'), -200 * factor, 4.5, 10, 90)
            style.label(op, layer, 'DatasetLabel', config.get('dataset_label', ''), -220 * factor, 34, 10)
            for i, note in enumerate(config.get('annotations', [])):
                x = style.XLIM[0] + float(note['x']) * (style.XLIM[1] - style.XLIM[0])
                y = style.YLIM[0] + float(note['y']) * (style.YLIM[1] - style.YLIM[0])
                style.label(op, layer, f'Annotation{i+1}', note['text'], x, y,
                            float(note.get('size_pt', 9)), float(note.get('rotation_deg', 0)),
                            note.get('color', '#303840'))
            graph.activate()
            assert op.save(str(target.with_suffix('.opju')))
            assert op.open(str(target.with_suffix('.opju')), asksave=False)
            graph = op.find_graph('PerspectiveWaterfall')
            state = style.verify(op, graph, expected, records, reference)
            for i, note in enumerate(config.get('annotations', [])):
                obj = graph[0].label(f'Annotation{i+1}')
                assert obj.text == note['text'], 'Saved annotation text changed'
                angle = float(note.get('rotation_deg', 0))
                assert abs((obj.get_float('rotate') - angle + 180) % 360 - 180) <= .051
            for i, panel in enumerate(panels):
                sheet = op.find_sheet('w', f'[ep{i+1:03d}]Sheet1')
                np.testing.assert_array_equal(sheet.to_list(0), panel['x'])
                np.testing.assert_array_equal(sheet.to_list(1), panel['y'])
            check_hashes(hashes)
            exported = style.export(op, graph, target)
            report = dict(synthetic=config.get('synthetic', False), source_files=hashes,
                          source_verification=dict(source_files_unchanged=True, exact_xy_readback=True,
                                                   series=8, points=sum(len(p['x']) for p in panels)),
                          records=records, reopened=state, reference_geometry=reference,
                          annotations=config.get('annotations', []),
                          environment=session.environment.to_dict(), export=exported,
                          visual_qa=dict(status='pending'))
            target.with_name(target.name + '_verify.json').write_text(
                json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
            print(json.dumps(report['source_verification']), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--stem', default='perspective-waterfall')
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    target = candidate_target(args.output_dir, args.stem)
    config, panels, hashes = load_manifest(args.manifest)
    if any(target.parent.is_relative_to(Path(p).parent) for p in hashes):
        raise ValueError('Use a candidate directory outside the source-data directory')
    if args.check_only:
        print(json.dumps(dict(valid=True, synthetic=config.get('synthetic', False), series=8,
                              points=sum(len(p['x']) for p in panels),
                              origin_started=False, outputs_written=False)), flush=True)
        return
    if platform.system() != 'Windows' or struct.calcsize('P') != 8 or sys.version_info[:2] not in ((3, 11), (3, 12)):
        parser.error('Native Origin rendering needs physical Windows x64 and CPython 3.11/3.12; check-only is portable')
    render(config, panels, hashes, target)


if __name__ == '__main__':
    main()
