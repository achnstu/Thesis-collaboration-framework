"""Standard-library input contract for the native bar/line dual-axis composition."""

import csv
import hashlib
import json
import math
from pathlib import Path
import re


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def numbers(values, name):
    result = [float(value) for value in values]
    if not result or not all(math.isfinite(value) for value in result):
        raise ValueError(f'{name} requires finite numeric values')
    return result


def limits(values, name):
    result = numbers(values, name)
    if len(result) != 3 or result[0] >= result[1] or result[2] <= 0:
        raise ValueError(f'{name} must be [minimum, maximum, positive increment]')
    if (result[1] - result[0]) / result[2] > 100:
        raise ValueError(f'{name} has too many ticks for this compact composition')
    return result


def color(value):
    if not isinstance(value, str) or not re.fullmatch(r'#[0-9A-Fa-f]{6}', value):
        raise ValueError('Colors must be six-digit HEX strings')
    return value


def read_csv(manifest, item, hashes):
    file = Path(item['file'])
    if file.is_absolute():
        raise ValueError('CSV paths must be relative to the manifest for portability')
    source = (manifest.parent / file).resolve()
    before = digest(source)
    if item.get('sha256') and item['sha256'] != before:
        raise ValueError(f'Source hash mismatch: {file.name}')
    if str(source) in hashes and hashes[str(source)] != before:
        raise ValueError('Source changed while reading the manifest')
    hashes[str(source)] = before
    with source.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
    if not rows:
        raise ValueError(f'Empty CSV: {file.name}')
    return rows


def validate_layout(config):
    page = numbers(config.get('page_cm', [13.5, 13.5]), 'page_cm')
    rect = numbers(config.get('layer_percent', [25, 5, 52, 82]), 'layer_percent')
    if len(page) != 2 or min(page) <= 0:
        raise ValueError('page_cm needs two positive dimensions')
    if len(rect) != 4 or min(rect) < 0 or min(rect[2:]) <= 0:
        raise ValueError('layer_percent needs [left, top, positive width, positive height]')
    if rect[0] + rect[2] > 100 or rect[1] + rect[3] > 100:
        raise ValueError('Layer rectangle must fit on the page')
    if config.get('line_x_axis', {}).get('show', False) and rect[1] < 10:
        raise ValueError('Reserve at least 10 percent top margin when showing the time axis')
    config['page_cm'], config['layer_percent'] = page, rect
    config['font'] = config.get('font', 'Times New Roman')
    if not isinstance(config['font'], str) or not config['font'].strip():
        raise ValueError('font must be a nonempty installed font name')
    if any(token in config['font'] for token in (';', '(', ')', '"', '\n')):
        raise ValueError('font contains unsupported LabTalk expression characters')
    config['font_sizes'] = {
        'ticks': 10.5, 'axis': 16, 'legend': 10.5, 'category': 11,
        'value': 11, 'comparison': 10.5, **config.get('font_sizes', {})}
    config['font_sizes'] = dict(zip(config['font_sizes'], numbers(config['font_sizes'].values(), 'font_sizes')))
    if min(config['font_sizes'].values()) <= 0:
        raise ValueError('Font sizes must be positive')
    for key in ('axis_width_pt', 'line_width_pt'):
        config[key] = numbers([config.get(key, .65)], key)[0]
        if config[key] <= 0:
            raise ValueError(f'{key} must be positive')


def validate_axes(config):
    for name in ('left_axis', 'right_axis', 'line_x_axis'):
        if not isinstance(config[name].get('title'), str) or not config[name]['title']:
            raise ValueError(f'{name}.title must identify the physical quantity and unit')
    left = limits(config['left_axis']['limits'], 'left_axis.limits')
    upper = limits(config['right_axis']['upper_limits'], 'right_axis.upper_limits')
    time = limits(config['line_x_axis']['limits'], 'line_x_axis.limits')
    if left[0] != 0:
        raise ValueError('The column axis starts at zero')
    fraction = float(config['right_axis'].get('upper_fraction', 5 / 11))
    if not math.isfinite(fraction) or not .2 <= fraction <= .7:
        raise ValueError('right_axis.upper_fraction must be between 0.2 and 0.7')
    config['left_axis']['limits'] = left
    config['right_axis']['upper_limits'] = upper
    config['line_x_axis']['limits'] = time
    config['right_axis']['upper_fraction'] = fraction
    # The unused lower band is display space, never a negative measurement.
    lower = upper[1] - (upper[1] - upper[0]) / fraction
    config['right_axis']['full_limits'] = [lower, upper[1], upper[2]]
    count = math.floor((upper[1] - upper[0]) / upper[2] + 1e-10)
    config['right_axis']['ticks'] = [upper[0] + i * upper[2] for i in range(count + 1)]


def load_bars(path, config, hashes):
    spec = config['bars']
    rows = read_csv(path, spec, hashes)
    categories = [row[spec['category_column']].strip() for row in rows]
    values = numbers([row[spec['value_column']] for row in rows], 'Bar values')
    if len(categories) < 2 or not all(categories) or len(set(categories)) != len(categories):
        raise ValueError('Need at least two unique, nonempty bar category labels')
    if min(values) < 0:
        raise ValueError('This composition supports nonnegative bars')
    ceiling = config['left_axis']['limits'][1] * (1 - config['right_axis']['upper_fraction'])
    if max(values) >= ceiling:
        raise ValueError('Bars overlap the upper line band; increase the left-axis maximum')
    fill = spec.get('fill_colors', ['#785398', '#F4EFF7'])
    if len(fill) != 2:
        raise ValueError('bars.fill_colors requires two gradient colors')
    spec['fill_colors'] = [color(value) for value in fill]
    spec['edge_color'] = color(spec.get('edge_color', '#4F3A66'))
    spec['guide_color'] = color(spec.get('guide_color', '#9A28FF'))
    gap = float(spec.get('gap_percent', 65))
    if not math.isfinite(gap) or not 0 <= gap < 100:
        raise ValueError('bars.gap_percent must be at least 0 and less than 100')
    spec['gap_percent'] = gap
    format(values[0], spec.get('value_format', '.1f'))
    return {'categories': categories, 'values': values}


def load_curves(path, config, hashes):
    curves = []
    lo, hi = config['right_axis']['upper_limits'][:2]
    xmin, xmax = config['line_x_axis']['limits'][:2]
    for item in config['series']:
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{0,31}', item['id']):
            raise ValueError('Series ids must be short ASCII identifiers')
        if not isinstance(item.get('label'), str) or not item['label']:
            raise ValueError('Every series needs a nonempty label')
        rows = read_csv(path, item, hashes)
        x = numbers([row[item['x_column']] for row in rows], 'Curve X')
        y = numbers([row[item['y_column']] for row in rows], 'Curve Y')
        if len(x) < 2 or any(b <= a for a, b in zip(x, x[1:])):
            raise ValueError('Each curve needs at least two strictly increasing X values')
        if min(x) < xmin or max(x) > xmax or min(y) < lo or max(y) > hi:
            raise ValueError('Curve values exceed their declared visible axis limits')
        marker = item.get('marker', 2)
        if not isinstance(marker, int) or not 0 <= marker <= 20:
            raise ValueError('marker must be an Origin symbol number from 0 to 20')
        curves.append({**item, 'color': color(item['color']), 'marker': marker, 'x': x, 'y': y})
    if not curves or len({item['id'] for item in curves}) != len(curves):
        raise ValueError('Need one or more curves with unique ids')
    return curves


def validate_comparisons(config, bars):
    values = dict(zip(bars['categories'], bars['values']))
    for item in config.get('comparisons', []):
        baseline, target = values[item['from']], values[item['to']]
        if baseline <= 0:
            raise ValueError('Percentage comparison denominator must be positive')
        xpos = numbers([item['x']], 'Comparison X')[0]
        if not .5 <= xpos <= len(values) + .5:
            raise ValueError('Comparison X must lie inside the bar category domain')
        if item.get('orientation', 'vertical') not in ('horizontal', 'vertical'):
            raise ValueError('Comparison orientation must be horizontal or vertical')
        item['percent'] = (baseline - target) / baseline * 100
        format(item['percent'], item.get('format', '.1f'))


def load_manifest(path):
    path = Path(path).resolve()
    config = json.loads(path.read_text(encoding='utf-8-sig'))
    if config.get('schema_version') != 1 or config.get('chart_type') != 'bar-line-dual-axis':
        raise ValueError('Expected schema_version=1 and chart_type=bar-line-dual-axis')
    hashes = {str(path): digest(path)}
    validate_layout(config)
    validate_axes(config)
    bars = load_bars(path, config, hashes)
    curves = load_curves(path, config, hashes)
    validate_comparisons(config, bars)
    check_hashes(hashes)
    return config, bars, curves, hashes


def check_hashes(hashes):
    for path, expected in hashes.items():
        if digest(path) != expected:
            raise ValueError(f'Source changed while rendering: {Path(path).name}')


def candidate_target(directory, stem):
    target = Path(directory).resolve()
    if target.exists():
        raise FileExistsError('Choose a new output directory; existing results are preserved')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}', stem):
        raise ValueError('Use an ASCII output stem of up to 64 characters')
    return target / stem
