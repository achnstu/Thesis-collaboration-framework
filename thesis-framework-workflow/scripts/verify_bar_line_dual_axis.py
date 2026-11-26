"""Saved-project and native-export checks for the portable bar/line route."""

import json

import numpy as np
from PIL import Image

from origin_sciplot.origin_backend.verify_utils import (
    _read_plot_option,
    read_layer_geometry_percent,
)

from bar_line_inputs import digest


def close(actual, expected, tolerance=.03):
    if abs(float(actual)-float(expected)) > tolerance:
        raise AssertionError(f'Native value mismatch: {actual} vs {expected}')


def read_data(op, references, bars, curves):
    source = op.find_sheet('w', references['bars'])
    np.testing.assert_array_equal(source.to_list(0), list(range(1, len(bars['values'])+1)))
    np.testing.assert_array_equal(source.to_list(1), bars['values'])
    assert source.to_list(2) == bars['categories'], 'Saved category labels changed'
    for ref, item in zip(references['curves'], curves):
        source = op.find_sheet('w', ref)
        np.testing.assert_array_equal(source.to_list(0), item['x'])
        np.testing.assert_array_equal(source.to_list(1), item['y'])
    return {'exact_xy_readback': True, 'categories': len(bars['values']),
            'curves': len(curves), 'curve_points': sum(len(item['x']) for item in curves)}


def read_labels(op, graph, config, bars):
    first = ['LeftTitle', 'RightTitle']
    first += [f'{kind}{i+1}' for i in range(len(bars['values'])) for kind in ('Category', 'Value')]
    first += [f'Percent{i+1}' for i in range(len(config.get('comparisons', [])))]
    second = ['CurveLegend', 'BarLegend']
    if config.get('synthetic', False):
        second.append('SyntheticNote')
    if config['line_x_axis'].get('show', False):
        second.append('TimeTitle')
    state = {}
    for layer, names in zip(graph, [first, second]):
        layer.activate()
        pw, ph = op.lt_float('page.width'), op.lt_float('page.height')
        for name in names:
            obj = layer.label(name)
            assert obj, f'Missing native label {name}'
            rect = [obj.get_float(key) for key in ('left', 'top', 'width', 'height')]
            assert min(rect[:2]) >= 0, f'Label outside page: {name}'
            assert rect[0]+rect[2] <= pw+.1 and rect[1]+rect[3] <= ph+.1, f'Label clipped: {name}'
            state[name] = {'text': obj.text, 'font': obj.get_float('font'),
                           'size_pt': obj.get_float('fsize'), 'rectangle': rect}
    assert state['LeftTitle']['text'] == config['left_axis']['title']
    assert state['RightTitle']['text'] == config['right_axis']['title']
    return state


def readback(op, graph, config, bars, curves, references):
    assert len(graph) == 2, 'Expected exactly two native graph layers'
    state = []
    for index, layer in enumerate(graph):
        layer.activate()
        geometry = read_layer_geometry_percent(op, layer)
        for key, expected in zip(('left_percent', 'top_percent', 'width_percent', 'height_percent'),
                                 config['layer_percent']):
            close(geometry[key], expected)
        ranges = {key: layer.get_float(key) for key in ('x.from', 'x.to', 'y.from', 'y.to')}
        xlim = [.5, len(bars['values'])+.5] if index == 0 else config['line_x_axis']['limits'][:2]
        close(ranges['x.from'], xlim[0], 1e-8)
        close(ranges['x.to'], xlim[1], 1e-8)
        ylim = config['left_axis']['limits'] if index == 0 else config['right_axis']['full_limits']
        close(ranges['y.from'], ylim[0], 1e-8)
        close(ranges['y.to'], ylim[1], 1e-8)
        state.append({'geometry': geometry, 'limits': ranges, 'plots': len(layer.plot_list())})
    assert len(graph[1].plot_list()) == len(curves)
    for plot, item in zip(graph[1].plot_list(), curves):
        rgb = tuple(int(item['color'][i:i+2], 16) for i in (1, 3, 5))
        assert tuple(plot.color) == rgb, 'Saved curve color changed'
    right = graph[1]
    right.activate()
    assert right.get_int('y.showLabels') == 2, 'Right numeric tick labels must be visible'
    ticks = right.get_str('y2.ticksbydata').strip('"').split()
    np.testing.assert_allclose([float(value) for value in ticks], config['right_axis']['ticks'])
    state[1]['right_ticks'] = [float(value) for value in ticks]
    state[1]['right_tick_labels_visible'] = True
    graph[0].activate()
    gradient = _read_plot_option(op, graph[0].plot_list()[0], '-pfm', '__barlinegradient')
    close(gradient, 3, 1e-8)
    graph.activate()
    physical = [op.lt_float('page.width/page.resx*2.54'), op.lt_float('page.height/page.resy*2.54')]
    for actual, expected in zip(physical, config['page_cm']):
        close(actual, expected)
    return {'layers': state, 'data': read_data(op, references, bars, curves),
            'labels': read_labels(op, graph, config, bars), 'page_cm': physical,
            'gradient_mode': gradient}


def export(op, graph, target, config):
    graph.activate()
    width = round(config['page_cm'][0]/2.54*600)
    settings = {'png': f'tr1.Unit:=2 tr1.Width:={width} tr2.PNG.DotsPerInch:=600',
                'emf': 'tr.Advanced.Resolution:=1 tr1.Unit:=3 tr1.Width:=100'}
    files = {}
    for extension, options in settings.items():
        op.lt_exec(f'expGraph type:={extension} export:=page filename:="{target.name}" '
                   f'path:="{target.parent.as_posix()}" overwrite:=replace sysopts:=0 '
                   f'tr.Margin:=2 tr.SpeedMode:=2 {options};')
        file = target.with_suffix('.'+extension)
        assert file.stat().st_size > 1000, f'{extension} export is empty'
        files[extension] = {'bytes': file.stat().st_size, 'sha256': digest(file)}
    with Image.open(target.with_suffix('.png')) as image:
        dpi = image.info.get('dpi', ())
        assert len(dpi) == 2 and all(abs(value-600) < .1 for value in dpi)
        files['png'].update(pixels=list(image.size), dpi=list(dpi))
        preview = image.copy()
        preview.thumbnail((1000, 1280))
        preview.save(target.with_name(target.name+'_preview.png'))
        preview.convert('L').save(target.with_name(target.name+'_grayscale.png'))
    return files


def write_report(target, report):
    target.with_name(target.name+'_verify.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
