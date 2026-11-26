"""Native Origin styling for separate-domain bars below and time curves above."""

from pathlib import Path
import sys

ENGINE = Path(__file__).resolve().parents[1] / 'embedded/editaplot/runtime'
if not (ENGINE / 'src/origin_sciplot').is_dir():
    raise FileNotFoundError('Copy the whole skill: bundled Origin runtime source is missing')
sys.path.insert(0, str(ENGINE / 'src'))
from origin_sciplot.origin_backend.execution_context import require_interactive_origin_context
from origin_sciplot.origin_backend.job_queue import origin_job_slot
from origin_sciplot.origin_backend.session import OriginSession


def configure_layer(layer, rect):
    layer.activate()
    layer.set_int('unit', 1)
    layer.set_int('fixed', 1)
    layer.set_float('factor', 1)
    for key, value in zip(('left', 'top', 'width', 'height'), rect):
        layer.set_float(key, value)


def label(op, layer, config, name, content, x, y, size, color='#000000', rotate=0):
    """Position the native text centre relative to the shared plotting rectangle."""
    layer.activate()
    obj = layer.add_label(content)
    obj.name = name
    for key, value in {'attach': 1, 'show': 1, 'font': int(op.lt_float(f'font({config["font"]})')),
                       'bold': 0, 'color': op.ocolor(color), 'background': 0}.items():
        obj.set_int(key, int(value))
    obj.set_float('fsize', size)
    obj.set_float('rotate', rotate)
    op.lt_exec('doc -uw;')
    left, top, width, height = config['layer_percent']
    xp, yp = left + width*x, top + height*y
    obj.set_float('left', op.lt_float('page.width')*xp/100 - obj.get_float('width')/2)
    obj.set_float('top', op.lt_float('page.height')*yp/100 - obj.get_float('height')/2)
    return obj


def axes(op, layer, config):
    layer.activate()
    font = int(op.lt_float(f'font({config["font"]})'))
    if not font:
        raise ValueError('Requested font is not available in this Origin installation')
    for axis in ('x', 'y', 'x2', 'y2'):
        for key, value in {'label.font': font, 'label.color': 1, 'label.numFormat': 1,
                           'minorTicks': 0, 'ticks': 2, 'showGrids': 0, 'atZero': 0}.items():
            layer.set_int(f'{axis}.{key}', value)
        for key, value in {'label.pt': config['font_sizes']['ticks'],
                           'thickness': config['axis_width_pt'],
                           'tickthickness': .55, 'ticklength': 2.1}.items():
            layer.set_float(f'{axis}.{key}', value)
    for name in ('legend', 'Legend', 'xb', 'xt', 'yl', 'yr'):
        old = layer.label(name)
        if old:
            old.remove()


def worksheet(op, name, x, y, xname='X', yname='Y'):
    sheet = op.new_book('w', name)[0]
    sheet.from_list(0, x, lname=xname, axis='X')
    sheet.from_list(1, y, lname=yname, axis='Y')
    return sheet


def line(layer, sheet, y=1, x=0, color='#000000', width=.65, dash=0, marker=0):
    layer.activate()
    plot = layer.add_plot(sheet, y, x, type='y' if marker else 'l')
    plot.color = color
    plot.set_cmd(f'-w {round(width*500)}', f'-d {dash}')
    if marker:
        plot.symbol_kind = marker
        plot.symbol_size = 2.0
    return plot


def guide(layer, sheet, name, x, y, color, width=.55, dash=0):
    index = sheet.cols
    sheet.cols = index + 2
    sheet.from_list(index, x, lname=name+' X', axis='X')
    sheet.from_list(index+1, y, lname=name+' Y', axis='Y')
    return line(layer, sheet, index+1, index, color, width, dash)


def bar_annotations(op, layer, config, bars, helpers):
    spec = config['bars']
    count = len(bars['values'])
    maximum = config['left_axis']['limits'][1]
    shade = spec['guide_color']
    for index, (category, value) in enumerate(zip(bars['categories'], bars['values'])):
        xp = (index+.5)/count
        label(op, layer, config, f'Category{index+1}', category, xp, 1.031,
              config['font_sizes']['category'])
        label(op, layer, config, f'Value{index+1}', format(value, spec.get('value_format', '.1f')),
              xp, (maximum-value)/maximum-.0147, config['font_sizes']['value'], shade)
        if spec.get('guide_lines', True):
            guide(layer, helpers, f'TotalGuide{index+1}', [.5, count+.5], [value, value], shade, dash=1)
    if spec.get('category_dividers', True):
        for index in range(count-1):
            xp = index+1.5
            guide(layer, helpers, f'Divider{index+1}', [xp, xp], [0, maximum], '#BDBDBD', .5, 1)
    label(op, layer, config, 'LeftTitle', config['left_axis']['title'], -.1514, .4962,
          config['font_sizes']['axis'], rotate=90)
    label(op, layer, config, 'RightTitle', config['right_axis']['title'], 1.252, .4962,
          config['font_sizes']['axis'], rotate=90)


def comparisons(op, layer, config, bars, helpers):
    values = dict(zip(bars['categories'], bars['values']))
    count, maximum = len(values), config['left_axis']['limits'][1]
    for index, item in enumerate(config.get('comparisons', [])):
        high, low = sorted([values[item['from']], values[item['to']]], reverse=True)
        xpos = float(item['x'])
        shade = config['bars']['guide_color']
        guide(layer, helpers, f'Comparison{index+1}',
              [xpos-.025, xpos+.025, xpos, xpos, xpos-.025, xpos+.025],
              [high, high, high, low, low, low], shade, .6)
        horizontal = item.get('orientation', 'vertical') == 'horizontal'
        xp = (xpos-.5)/count + (0 if horizontal else -.035)
        yp = (maximum-(high+low)/2)/maximum
        label(op, layer, config, f'Percent{index+1}', format(item['percent'], item.get('format', '.1f'))+'%',
              xp, yp, config['font_sizes']['comparison'], shade, 0 if horizontal else 270)


def draw_bars(op, graph, config, bars):
    layer = graph[0]
    configure_layer(layer, config['layer_percent'])
    values, spec = bars['values'], config['bars']
    source = worksheet(op, 'Bars', list(range(1, len(values)+1)), values,
                       'Category ordinal (display only)', spec['value_column'])
    source.from_list(2, bars['categories'], lname=spec['category_column'])
    helpers = op.new_book('w', 'DisplayGeometry')[0]
    layer.activate()
    column = layer.add_plot(source, 1, 0, type=203)
    column.color = spec['edge_color']
    column.set_cmd('-pfm 3', f'-pfb {op.ocolor(spec["fill_colors"][0])}',
                   f'-pff {op.ocolor(spec["fill_colors"][1])}',
                   f'-vg {spec["gap_percent"]}', '-vw 0.65')
    layer.set_xlim(.5, len(values)+.5, 1)
    layer.set_ylim(*config['left_axis']['limits'])
    axes(op, layer, config)
    layer.lt_exec('layer.x.showAxes=3;layer.x.showLabels=0;'
                  'layer.x.ticks=0;layer.x2.ticks=0;layer.y.showAxes=3;'
                  'layer.y.showLabels=1;layer.y2.ticks=0;')
    bar_annotations(op, layer, config, bars, helpers)
    comparisons(op, layer, config, bars, helpers)
    return source.lt_range()


def draw_curves(op, graph, config, curves):
    layer = graph.add_layer(2)
    configure_layer(layer, config['layer_percent'])
    layer.set_int('link', 0)
    layer.set_int('color', 0)
    layer.set_int('border', 0)
    layer.set_int('showframe', 0)
    refs = []
    for index, item in enumerate(curves):
        source = worksheet(op, f'Curve{index+1:03d}', item['x'], item['y'],
                           item['x_column'], item['y_column'])
        line(layer, source, color=item['color'], width=config['line_width_pt'], marker=item['marker'])
        refs.append(source.lt_range())
    layer.set_xlim(*config['line_x_axis']['limits'])
    layer.set_ylim(*config['right_axis']['full_limits'])
    axes(op, layer, config)
    # showAxes/showLabels are bit fields shared by axis and axis2. Set these LAST.
    # Writing y2.showAxes=1 afterwards would switch back to left-axis display.
    ticks = ' '.join(format(value, '.15g') for value in config['right_axis']['ticks'])
    layer.lt_exec(f'layer.y.ticksbydata$="{ticks}";layer.y2.ticksbydata$="{ticks}";'
                  'layer.x.showAxes=0;layer.x.showLabels=0;'
                  'layer.y.showAxes=2;layer.y.showLabels=2;')
    layer.set_int('y2.showlabel', 1)
    if config['line_x_axis'].get('show', False):
        layer.lt_exec('layer.x.showAxes=2;layer.x.showLabels=2;')
        label(op, layer, config, 'TimeTitle', config['line_x_axis']['title'], .5, -.085,
              config['font_sizes']['legend'])
    content = '\n'.join(f'\\l({index+1}) {item["label"]}' for index, item in enumerate(curves))
    label(op, layer, config, 'CurveLegend', content, .163, .1314, config['font_sizes']['legend'])
    label(op, layer, config, 'BarLegend', '\\l(1.1) '+config['bars'].get('legend', 'Total'),
          .3265, .0266, config['font_sizes']['legend'])
    if config.get('synthetic', False):
        label(op, layer, config, 'SyntheticNote', 'Synthetic example', .5, 1.13, 8)
    return refs


def draw(op, config, bars, curves):
    graph = op.new_graph('Bar-line dual-axis composition', template='Line')
    graph.name = 'BarLineDual'
    graph.activate()
    op.lt_exec('page.updatetoprinter=0;page.kar=0;doc -uw;')
    graph.obj.PutWidth(config['page_cm'][0]/2.54)
    graph.obj.PutHeight(config['page_cm'][1]/2.54)
    graph.set_int('background', op.ocolor('#FFFFFF'))
    references = {'bars': draw_bars(op, graph, config, bars)}
    references['curves'] = draw_curves(op, graph, config, curves)
    graph.activate()
    return graph, references
