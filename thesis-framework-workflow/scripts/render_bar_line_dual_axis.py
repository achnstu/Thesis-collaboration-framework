"""Render lower gradient columns and upper time curves through native Origin."""

import argparse
import json
from pathlib import Path
import platform
import shutil
import struct
import sys

# Explicit sibling discovery also supports Python -I from an unrelated cwd.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bar_line_inputs import candidate_target, check_hashes, digest, load_manifest


def progress(stage, target=None, **payload):
    row = json.dumps({'stage': stage, **payload}, ensure_ascii=True)
    print(row, flush=True)
    if target:
        with target.with_name(target.name+'_run.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(row+'\n')


def save_replay(target, manifest, hashes):
    """Freeze only this run's inputs and original relative CSV paths for replay."""
    replay = target.parent/'inputs'
    replay.mkdir()
    manifest = manifest.resolve()
    copied = {}
    config = json.loads(manifest.read_text(encoding='utf-8-sig'))
    entries = [config['bars'], *config['series']]
    for index, item in enumerate(entries):
        source = (manifest.parent/item['file']).resolve()
        if str(source) not in copied:
            name = f'source-{index+1:03d}.csv'
            shutil.copyfile(source, replay/name)
            assert digest(replay/name) == hashes[str(source)]
            copied[str(source)] = name
        item['file'] = copied[str(source)]
        item['sha256'] = hashes[str(source)]
    (replay/'manifest.json').write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding='utf-8')
    return 'inputs/manifest.json'


def render(config, bars, curves, hashes, target, manifest):
    # Native dependencies are deliberately lazy: --check-only uses stdlib only.
    import origin_bar_line_style as style
    from verify_bar_line_dual_axis import export, readback, write_report

    style.require_interactive_origin_context()
    target.parent.mkdir(parents=True, exist_ok=False)
    progress('starting_origin', target)
    with style.origin_job_slot(job_kind='bar-line-dual-axis'):
        with style.OriginSession(keep_open=False) as session:
            op = session.op
            progress('origin_connected', target, product=session.environment.to_dict()['origin_product'])
            graph, references = style.draw(op, config, bars, curves)
            progress('native_graph_created', target, bars=len(bars['values']), curves=len(curves))
            before = readback(op, graph, config, bars, curves, references)
            assert op.save(str(target.with_suffix('.opju')))
            assert op.open(str(target.with_suffix('.opju')), asksave=False)
            reopened = op.find_graph('BarLineDual')
            after = readback(op, reopened, config, bars, curves, references)
            assert before == after, 'Saved native graph properties changed on reopen'
            exported = export(op, reopened, target, config)
            check_hashes(hashes)
            replay = save_replay(target, manifest, hashes)
            report = {'schema_version': 1, 'chart_type': 'bar-line-dual-axis',
                      'synthetic': config.get('synthetic', False), 'runtime_source': 'embedded/editaplot/runtime/src',
                      'source_files': [{'file': Path(file).name, 'sha256': value} for file, value in hashes.items()],
                      'source_files_unchanged': True, 'replay_manifest': replay,
                      'independent_x_domains': {'bottom': 'bar category ordinals', 'top': config['line_x_axis']['title'],
                                                'top_axis_visible': config['line_x_axis'].get('show', False)},
                      'right_axis': config['right_axis'], 'comparisons': config.get('comparisons', []),
                      'saved_project': after, 'environment': session.environment.to_dict(), 'export': exported,
                      'opju_sha256': digest(target.with_suffix('.opju')),
                      'visual_qa': {'status': 'pending'}}
            write_report(target, report)
            progress('saved_and_reopened', target, exact_xy_readback=True, right_tick_labels_visible=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--stem', default='bar-line-dual-axis')
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    target = candidate_target(args.output_dir, args.stem)
    config, bars, curves, hashes = load_manifest(args.manifest)
    if any(target.parent.is_relative_to(Path(file).parent) for file in hashes):
        parser.error('Use a new output directory outside the source-data directory')
    if args.check_only:
        progress('preflight_passed', valid=True, synthetic=config.get('synthetic', False),
                 categories=len(bars['values']), curves=len(curves),
                 points=sum(len(item['x']) for item in curves),
                 full_right_limits=config['right_axis']['full_limits'],
                 right_ticks=config['right_axis']['ticks'], origin_started=False, outputs_written=False)
        return
    if platform.system() != 'Windows' or struct.calcsize('P') != 8 or sys.version_info[:2] not in ((3, 11), (3, 12)):
        parser.error('Native rendering needs Windows x64 and CPython 3.11/3.12; check-only is portable')
    render(config, bars, curves, hashes, target, args.manifest)


if __name__ == '__main__':
    main()
