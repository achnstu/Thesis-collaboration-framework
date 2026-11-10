"""Read a portable, read-only eight-series CSV manifest using the standard library."""
import csv
import hashlib
import json
import math
from pathlib import Path
import re


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate_style(config):
    transparency = config.get('fill_transparency_percent', 75)
    if not isinstance(transparency, int) or not 0 <= transparency <= 100:
        raise ValueError('fill_transparency_percent must be an integer from 0 to 100')
    for note in config.get('annotations', []):
        if not isinstance(note.get('text'), str):
            raise ValueError('Annotation text must be a string')
        if not all(math.isfinite(float(note[k])) and 0 <= float(note[k]) <= 1 for k in ('x', 'y')):
            raise ValueError('Annotation x/y must be fractions from 0 to 1 within the plot layer')
        if not math.isfinite(float(note.get('size_pt', 9))) or float(note.get('size_pt', 9)) <= 0:
            raise ValueError('Annotation size_pt must be positive and finite')
        if not math.isfinite(float(note.get('rotation_deg', 0))):
            raise ValueError('Annotation rotation_deg must be finite')
        if not re.fullmatch(r'#[0-9A-Fa-f]{6}', note.get('color', '#303840')):
            raise ValueError('Annotation color must be a six-digit HEX color')


def read_series(path, config, item, scale):
    source = (path.parent / item['file']).resolve()
    before = digest(source)
    if item.get('sha256') and before != item['sha256']:
        raise ValueError(f'Source hash changed: {source.name}')
    with source.open(encoding='utf-8-sig', newline='') as handle:
        rows = list(csv.DictReader(handle))
    x = [float(row[config['x_column']]) for row in rows]
    raw_y = [float(row[config['y_column']]) for row in rows]
    y = [value * scale for value in raw_y]
    if len(x) < 2 or not all(math.isfinite(v) for v in x + y):
        raise ValueError(f'Need finite paired values: {source.name}')
    if x[0] != 0 or any(b <= a for a, b in zip(x, x[1:])):
        raise ValueError(f'Time must start at zero and increase: {source.name}')
    if min(y) < 0 or max(y) > 9:
        raise ValueError('This reference style spans 0-9 units; adapt its full geometry before use')
    if item.get('color') and not re.fullmatch(r'#[0-9A-Fa-f]{6}', item['color']):
        raise ValueError('Series color must be a six-digit HEX color')
    return dict(id=item['id'], label=item.get('label', item['id']), color=item.get('color'),
                source=str(source), x=x, raw_y=raw_y, y=y), before


def load_manifest(path):
    path = Path(path).resolve()
    config = json.loads(path.read_text(encoding='utf-8-sig'))
    if config.get('schema_version') != 1 or len(config.get('series', [])) != 8:
        raise ValueError('Manifest schema 1 requires exactly eight series for this geometry')
    scale = float(config.get('y_scale', 1))
    if not math.isfinite(scale) or scale <= 0:
        raise ValueError('y_scale must be finite and positive')
    validate_style(config)
    panels = []
    hashes = {str(path): digest(path)}
    for item in config['series']:
        panel, before = read_series(path, config, item, scale)
        hashes[panel['source']] = before
        panels.append(panel)
    if len({p['id'] for p in panels}) != 8:
        raise ValueError('Series ids must be unique')
    maximum = max(p['x'][-1] for p in panels)
    ticks = config.get('time_ticks', [maximum * i / 4 for i in range(5)])
    if not ticks or any(not math.isfinite(float(t)) or not 0 <= t <= maximum for t in ticks):
        raise ValueError('Time ticks must lie within the true time range')
    if any(b <= a for a, b in zip(ticks, ticks[1:])):
        raise ValueError('Time ticks must be strictly increasing')
    config['time_ticks'] = ticks
    return config, panels, hashes


def candidate_target(directory, stem):
    directory = Path(directory).resolve()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}', stem):
        raise ValueError('Use a simple ASCII output stem, up to 64 characters')
    if directory.exists():
        raise FileExistsError('Choose a new candidate directory; existing results are preserved')
    return directory / stem


def check_hashes(hashes):
    for path, expected in hashes.items():
        if digest(path) != expected:
            raise ValueError(f'Source changed during rendering: {Path(path).name}')


def set_time_geometry(style, panels, ticks):
    factor = max(p['x'][-1] for p in panels) / 2060
    style.TIME_MAX = 2060 * factor
    style.TIME_TICKS = tuple(ticks)
    style.TIME_COORD_SCALE = factor
    style.DEPTH_X = 180 * factor
    style.TIME_TILT = .0026 / factor
    style.XLIM = (-420 * factor, 3580 * factor)
    style.SCALE_X = style.WIDTH * .86 / (style.XLIM[1] - style.XLIM[0])
    style.ANGLE_X = math.degrees(math.atan2(-style.TIME_TILT * style.SCALE_Y, style.SCALE_X))
    style.ANGLE_DEPTH = math.degrees(math.atan2(style.DEPTH_Y * style.SCALE_Y, style.DEPTH_X * style.SCALE_X))
    style.SERIES_LABELS = [p['label'] for p in panels]
    return factor
