"""Native Origin revision: balanced perspective, reference planes and typography.

Raw and original projection columns are retained byte-for-byte as numeric arrays.
New display columns use x=time+180*(i+0.65),
y=load+3.3*(i+0.65)-0.0026*time. The front bay is display space only.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import sys

import numpy as np
from PIL import Image

ENGINE = Path(__file__).resolve().parents[1] / 'embedded/editaplot/runtime'
if not (ENGINE / 'src/origin_sciplot').is_dir():
    raise FileNotFoundError('The bundled embedded/editaplot/runtime source is missing')
sys.path.insert(0, str(ENGINE / 'src'))
from origin_sciplot.origin_backend.execution_context import require_interactive_origin_context
from origin_sciplot.origin_backend.job_queue import origin_job_slot
from origin_sciplot.origin_backend.session import OriginSession
from origin_sciplot.origin_backend.verify_utils import _read_plot_option

STEM = 'perspective-waterfall'
WIDTH, HEIGHT = 18.0, 13.5
XLIM, YLIM = (-420, 3580), (-10, 36)
DEPTH_X, DEPTH_Y, TIME_TILT, TIME_MAX = 180.0, 3.3, .0026, 2060.0
TIME_TICKS = (0,500,1000,1500,2000)
TIME_COORD_SCALE = 1.0
FRONT_SETBACK = .65
REAR_DEPTH = 7+FRONT_SETBACK
FILL_TRANSPARENCY = 75
SCALE_X = WIDTH*.86/(XLIM[1]-XLIM[0])
SCALE_Y = HEIGHT*.82/(YLIM[1]-YLIM[0])
ANGLE_X = math.degrees(math.atan2(-TIME_TILT*SCALE_Y,SCALE_X))
ANGLE_DEPTH = math.degrees(math.atan2(DEPTH_Y*SCALE_Y,DEPTH_X*SCALE_X))
COLORS = ['#0072B2','#D55E00','#009E73','#CC79A7','#56B4E9','#E69F00','#000000','#882255']
SERIES_LABELS = [f'ep{i+1:03d}' for i in range(8)]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require_new_outputs(output_dir):
    if output_dir.exists():
        raise FileExistsError('Choose a new candidate directory. Existing results are preserved.')
    return output_dir / STEM


def originals(op):
    result = {}
    for book in op.pages('w'):
        for sheet in book:
            values = [sheet.to_list(j) for j in range(sheet.cols)]
            result[sheet.lt_range()] = dict(columns=sheet.cols, sha256=hashlib.sha256(
                json.dumps(values, allow_nan=True).encode()).hexdigest())
    return result


def verify_originals(op, expected):
    for ref, record in expected.items():
        sheet = op.find_sheet('w', ref)
        values = [sheet.to_list(j) for j in range(record['columns'])]
        assert hashlib.sha256(json.dumps(values, allow_nan=True).encode()).hexdigest() == record['sha256'], ref


def add_line(layer, sheet, name, x, y, color, width=.5, dash=0):
    c = sheet.cols
    sheet.cols = c+2
    sheet.from_list(c, x, lname=name+' X', axis='X')
    sheet.from_list(c+1, y, lname=name+' Y', axis='Y')
    layer.activate()
    p = layer.add_plot(sheet, c+1, c, type='l')
    p.color = color
    p.set_cmd(f'-w {round(width*500)}', f'-d {dash}')
    return p


def add_region(op, layer, sheet, name, x, upper, lower, fill, edge, edge_width=.45):
    top = add_line(layer, sheet, name+' upper', x, upper, edge, edge_width)
    add_line(layer, sheet, name+' lower', x, lower, edge, edge_width)
    top.set_fill_area(int(op.ocolor(fill)), type=9, below=int(op.ocolor(fill)))
    top.set_cmd('-pfm 3')
    return top


def project(time, voyage, power=0):
    return time+DEPTH_X*voyage, power+DEPTH_Y*voyage-TIME_TILT*time


def offset(point, dx_cm, dy_cm):
    return point[0]+dx_cm/SCALE_X, point[1]+dy_cm/SCALE_Y


def line_3d(layer, sheet, name, points, color, width=.5, dash=0):
    xy=[project(*p) for p in points]
    return add_line(layer,sheet,name,[p[0] for p in xy],[p[1] for p in xy],color,width,dash)


def plane(op, layer, sheet, name, corners, color):
    vertices=[project(*p) for p in corners]
    xs=sorted(set(p[0] for p in vertices))
    upper,lower=[],[]
    for x in xs:
        crossings=[]
        for a,b in zip(vertices,vertices[1:]+vertices[:1]):
            if abs(a[0]-b[0])<1e-10:
                if abs(x-a[0])<1e-10:
                    crossings.extend([a[1],b[1]])
                continue
            if not min(a[0],b[0])-1e-10<=x<=max(a[0],b[0])+1e-10:
                continue
            crossings.append(a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]))
        assert crossings
        upper.append(max(crossings));lower.append(min(crossings))
    return add_region(op,layer,sheet,name,xs,upper,lower,color,color,0)


def label(op, layer, name, text, x, y, size=9, rotation=0, color='#303840'):
    layer.activate()
    obj = layer.add_label(text)
    obj.name = name
    for key, val in dict(attach=1,show=1,font=int(op.lt_float('font(Arial)')),
                         bold=0,color=int(op.ocolor(color)),background=0).items():
        obj.set_int(key, val)
    obj.set_float('fsize', size)
    obj.set_float('rotate', rotation)
    op.lt_exec('doc -uw;')
    pw, ph = op.lt_float('page.width'), op.lt_float('page.height')
    px = pw*(layer.get_float('left')+layer.get_float('width')*(x-XLIM[0])/(XLIM[1]-XLIM[0]))/100
    py = ph*(layer.get_float('top')+layer.get_float('height')*(YLIM[1]-y)/(YLIM[1]-YLIM[0]))/100
    obj.set_float('left', px-obj.get_float('width')/2)
    obj.set_float('top', py-obj.get_float('height')/2)
    return obj


def reference_planes(op, layer):
    sheet = op.new_sheet('w', lname='Perspective reference geometry, not measurements')
    sheet.get_book().name = 'ViewGeometry'
    sheet.cols = 0
    floor_colors=['#FAFBFC','#F8FAFC','#F7F9FB','#F6F8FA','#F5F7FA','#F3F6F9','#F1F5F8','#EFF3F7']
    rear_colors=['#EEF3F7','#F2F5F8','#F6F8FA']
    wall_colors=['#D6DFE8','#D9E2EB','#DCE5ED','#DFE7EF','#E2EAF1','#E5ECF3','#E8EEF5','#EBF1F6']
    boundaries=[0]+[i+FRONT_SETBACK for i in range(8)]
    for i, fill in enumerate(floor_colors):
        a,b=boundaries[i:i+2]
        plane(op,layer,sheet,f'Floor band {i+1}',
              [(0,a,0),(TIME_MAX,a,0),(TIME_MAX,b,0),(0,b,0)],fill)
    for i, fill in enumerate(rear_colors):
        p=3*i
        plane(op,layer,sheet,f'Rear wall band {i+1}',
              [(0,REAR_DEPTH,p),(TIME_MAX,REAR_DEPTH,p),(TIME_MAX,REAR_DEPTH,p+3),(0,REAR_DEPTH,p+3)],fill)
    for i, fill in enumerate(wall_colors):
        a,b=boundaries[i:i+2]
        plane(op,layer,sheet,f'Wall band {i+1}',
              [(0,a,0),(0,b,0),(0,b,9),(0,a,9)],fill)
    line_3d(layer,sheet,'Wall upper edge',[(0,0,9),(0,REAR_DEPTH,9)],'#8293A2',.55)
    line_3d(layer,sheet,'Rear wall upper edge',[(0,REAR_DEPTH,9),(TIME_MAX,REAR_DEPTH,9)],'#B2C0CC',.45)
    line_3d(layer,sheet,'Rear wall right edge',[(TIME_MAX,REAR_DEPTH,0),(TIME_MAX,REAR_DEPTH,9)],'#B2C0CC',.45)
    line_3d(layer,sheet,'Floor right edge',[(TIME_MAX,0,0),(TIME_MAX,REAR_DEPTH,0)],'#C0CCD7',.45)
    line_3d(layer,sheet,'Floor rear edge',[(0,REAR_DEPTH,0),(TIME_MAX,REAR_DEPTH,0)],'#C0CCD7',.45)
    for power in [3,6]:
        line_3d(layer,sheet,f'{power} kW on wall',[(0,0,power),(0,REAR_DEPTH,power)],'#AEBCC9',.3)
        line_3d(layer,sheet,f'{power} kW on rear wall',[(0,REAR_DEPTH,power),(TIME_MAX,REAR_DEPTH,power)],'#CFD8E0',.25)
    for i in range(8):
        depth=i+FRONT_SETBACK
        line_3d(layer,sheet,f'Wall lane {i+1}',[(0,depth,0),(0,depth,9)],'#C1CDD8',.25)
        if i != 7:
            line_3d(layer,sheet,f'Floor lane {i+1}',[(0,depth,0),(TIME_MAX,depth,0)],'#D6DFE7',.25)
        point=project(0,depth,9)
        theta=math.radians(ANGLE_DEPTH)
        normal=(-math.sin(theta),math.cos(theta))
        end=offset(point,.11*normal[0],.11*normal[1])
        add_line(layer,sheet,f'Voyage tick {i+1}',[point[0],end[0]],[point[1],end[1]],'#71808C',.5)
        pos=offset(point,.68*normal[0],.68*normal[1])
        label(op,layer,f'Voyage{i+1}',SERIES_LABELS[i],*pos,8.8,ANGLE_DEPTH-90)
    line_3d(layer,sheet,'Wall rear edge',[(0,REAR_DEPTH,0),(0,REAR_DEPTH,9)],'#8293A2',.55)
    for time in TIME_TICKS[1:]:
        line_3d(layer,sheet,f'{time} s reference',[(time,0,0),(time,REAR_DEPTH,0)],'#BECBD6',.33,1)
        line_3d(layer,sheet,f'{time} s on rear wall',[(time,REAR_DEPTH,0),(time,REAR_DEPTH,9)],'#D4DDE5',.25)
    line_3d(layer,sheet,'Depth baseline',[(0,0,0),(0,REAR_DEPTH,0)],'#71808C',.6)
    line_3d(layer,sheet,'Time axis',[(0,0,0),(TIME_MAX,0,0)],'#404C56',.65)
    line_3d(layer,sheet,'Power axis',[(0,0,0),(0,0,9)],'#404C56',.65)
    for time in TIME_TICKS:
        point=project(time,0,0)
        theta=math.radians(ANGLE_X)
        normal=(math.sin(theta),-math.cos(theta))
        end=offset(point,.10*normal[0],.10*normal[1])
        add_line(layer,sheet,f'Time tick {time}',[point[0],end[0]],[point[1],end[1]],'#404C56',.5)
        pos=offset(point,.32*normal[0],.32*normal[1])
        label(op,layer,f'TimeTick{time}',str(time),*pos,8.5)
    for power in [0,3,6,9]:
        add_line(layer, sheet, f'Power tick {power}', [-22*TIME_COORD_SCALE,0], [power,power], '#404C56', .5)
        label(op, layer, f'PowerTick{power}', str(power), -65*TIME_COORD_SCALE, power, 8.5)
    return dict(worksheet=sheet.lt_range(),plots=len(layer.plot_list()),
                floor_colors=floor_colors,rear_colors=rear_colors,wall_colors=wall_colors,
                front_setback=FRONT_SETBACK,lane_depths=[i+FRONT_SETBACK for i in range(8)],
                floor_vertices=[project(*p) for p in [(0,0,0),(TIME_MAX,0,0),(TIME_MAX,REAR_DEPTH,0),(0,REAR_DEPTH,0)]],
                rear_vertices=[project(*p) for p in [(0,REAR_DEPTH,0),(TIME_MAX,REAR_DEPTH,0),(TIME_MAX,REAR_DEPTH,9),(0,REAR_DEPTH,9)]],
                wall_vertices=[project(*p) for p in [(0,0,0),(0,REAR_DEPTH,0),(0,REAR_DEPTH,9),(0,0,9)]])


def trace(op, layer, index):
    sheet = op.find_sheet('w', f'[ep{index+1:03d}]Sheet1')
    x, y = np.array(sheet.to_list(0)), np.array(sheet.to_list(1))
    depth=index+FRONT_SETBACK
    sheet.from_list(5, (x+DEPTH_X*depth).tolist(), lname='优化透视时间', units='display', axis='X')
    sheet.from_list(6, (y+DEPTH_Y*depth-TIME_TILT*x).tolist(), lname='优化透视负载', units='display', axis='Y')
    sheet.from_list(7, (DEPTH_Y*depth-TIME_TILT*x).tolist(), lname='优化透视基线', units='display', axis='Y')
    layer.activate()
    p = layer.add_plot(sheet, 6, 5, type='l')
    p.color = COLORS[index]
    p.set_cmd('-w 0', '-d 0')
    baseline = layer.add_plot(sheet, 7, 5, type='l')
    baseline.color = COLORS[index]
    baseline.set_cmd('-w 125')
    fill = int(op.ocolor(COLORS[index]))
    p.set_fill_area(fill, type=9, below=fill)
    p.transparency=FILL_TRANSPARENCY
    p.set_cmd('-pfm 3','-paaf 0')
    outline=layer.add_plot(sheet,6,5,type='l')
    outline.color=COLORS[index]
    outline.transparency=0
    outline.set_cmd('-pf 0','-w 450','-d 0')
    return dict(voyage=f'ep{index+1:03d}', worksheet=sheet.lt_range(), count=len(x),
                raw_xy_sha256=hashlib.sha256(np.vstack([x,y]).tobytes()).hexdigest(), color=COLORS[index],
                fill_transparency_percent=FILL_TRANSPARENCY,transparency_for_fill_only=True)


def configure(op, graph):
    graph.activate()
    op.lt_exec('page.updatetoprinter=0;page.kar=0;doc -uw;')
    graph.obj.PutWidth(WIDTH/2.54)
    graph.obj.PutHeight(HEIGHT/2.54)
    graph.set_int('background', int(op.ocolor('#FFFFFF')))
    layer = graph[0]
    layer.set_int('unit', 1)
    layer.set_int('fixed', 1)
    layer.set_int('border', 0)
    layer.set_int('showframe', 0)
    layer.set_float('factor', 1)
    for key, value in dict(left=8,top=7,width=86,height=82).items():
        layer.set_float(key, value)
    layer.set_xlim(*XLIM, 500)
    layer.set_ylim(*YLIM, 10)
    for axis in ['x','x2','y','y2']:
        for prop in ['showAxes','showLabels','showlabel','showGrids']:
            layer.set_int(f'{axis}.{prop}', 0)
        layer.set_int(f'{axis}.label.font', int(op.lt_float('font(Arial)')))
    for native in list(layer.obj.GraphObjects):
        obj = layer.label(native.GetName())
        if obj:
            obj.set_int('show', 0)
    return layer


def verify(op, graph, expected, records, reference):
    verify_originals(op, expected)
    layer = graph[0]
    assert len(layer.plot_list()) == reference['plots']+3*len(records)
    assert layer.get_int('showframe') == 0
    voyage_objects=[layer.label(f'Voyage{i+1}') for i in range(8)]
    centers=np.array([[o.get_float('left')+o.get_float('width')/2,
                       o.get_float('top')+o.get_float('height')/2] for o in voyage_objects])
    steps=np.diff(centers,axis=0)
    assert np.max(np.abs(steps-steps.mean(axis=0)))<=2, 'Voyage label centers are not evenly spaced'
    angles=[o.get_float('rotate') for o in voyage_objects]
    assert max(angles)-min(angles)<.01, 'Voyage labels are not parallel'
    assert all(abs((a-(ANGLE_DEPTH-90)+180)%360-180)<=.051 for a in angles)
    first=voyage_objects[0]
    obstacles=[layer.label('PowerTick9'),layer.label('LoadTitle')]
    label_gap=min(o.get_float('top') for o in obstacles)-first.get_float('top')-first.get_float('height')
    assert label_gap>0, 'ep001 overlaps the power axis labels'
    visible_labels=[]
    for native in layer.obj.GraphObjects:
        if native.GetObjectType() != 2:
            continue
        obj=layer.label(native.GetName())
        if obj.get_int('show'):
            assert obj.get_int('font') == int(op.lt_float('font(Arial)'))
            visible_labels.append(dict(name=obj.name,text=obj.text,font='Arial',size=obj.get_float('fsize')))
    surfaces=[]
    for i, fill in enumerate(reference['floor_colors']+reference['rear_colors']+reference['wall_colors']):
        plot=layer.plot_list()[2*i]
        actual_fill=_read_plot_option(op,plot,'-pfb','__surface_fill')
        assert actual_fill == op.ocolor(fill)
        assert _read_plot_option(op,plot,'-pfv','__surface_type') == 9
        surfaces.append(dict(plot=2*i+1,fill=fill))
    for j,rec in enumerate(records):
        i = int(rec['voyage'][2:])-1
        depth=i+FRONT_SETBACK
        w = op.find_sheet('w', rec['worksheet'])
        x,y = np.array(w.to_list(0)), np.array(w.to_list(1))
        assert hashlib.sha256(np.vstack([x,y]).tobytes()).hexdigest() == rec['raw_xy_sha256']
        np.testing.assert_array_equal(w.to_list(5), x+DEPTH_X*depth)
        np.testing.assert_array_equal(w.to_list(6), y+DEPTH_Y*depth-TIME_TILT*x)
        np.testing.assert_array_equal(w.to_list(7), DEPTH_Y*depth-TIME_TILT*x)
        plot=layer.plot_list()[reference['plots']+3*j]
        assert plot.transparency==FILL_TRANSPARENCY
        assert _read_plot_option(op,plot,'-w','__fill_width')==0
        outline=layer.plot_list()[reference['plots']+3*j+2]
        assert outline.transparency==0
        assert _read_plot_option(op,outline,'-pf','__outline_fill')==0
    return dict(raw_and_original_columns_unchanged=True, projection_verified=True,surfaces=surfaces,
                label_layout=dict(uniform_spacing=True,parallel=True,ep001_clearance_page_units=label_gap),
                labels=visible_labels,
                plots=len(layer.plot_list()), page_cm=[graph.obj.GetWidth()*2.54,graph.obj.GetHeight()*2.54],
                geometry={k:layer.get_float(k) for k in ['left','top','width','height','x.from','x.to','y.from','y.to']})


def export(op, graph, target):
    graph.activate()
    assert op.lt_exec(f'expGraph type:=png export:=page filename:="{target.name}" '
                      f'path:="{target.parent.as_posix()}" overwrite:=replace sysopts:=0 '
                      f'tr.Margin:=2 tr.SpeedMode:=2 tr1.Unit:=2 tr1.Width:={round(WIDTH/2.54*600)} '
                      'tr2.PNG.DotsPerInch:=600;')
    assert op.lt_exec(f'expGraph type:=emf export:=page filename:="{target.name}" '
                      f'path:="{target.parent.as_posix()}" overwrite:=replace sysopts:=0 '
                      'tr.Margin:=2 tr.SpeedMode:=2 tr.Advanced.Resolution:=1 tr1.Unit:=3 tr1.Width:=100;')
    with Image.open(target.with_suffix('.png')) as im:
        meta = dict(pixels=list(im.size), dpi=list(im.info.get('dpi',[])))
    assert len(meta['dpi']) == 2 and all(abs(v-600)<.1 for v in meta['dpi'])
    graph.save_fig(str(target.parent/f'{STEM}_preview.png'), width=1800)
    return meta


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--source-graph',required=True)
    parser.add_argument('--dataset-label',default='')
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--check-only',action='store_true',help='Check paths and hash without starting Origin')
    args=parser.parse_args()
    target=require_new_outputs(args.output_dir)
    if not args.source.is_file() or args.source.suffix.lower()!='.opju':
        raise ValueError('Source must be the original eight-voyage OPJU backup')
    source_hash=digest(args.source)
    if args.check_only:
        print(json.dumps(dict(source_sha256=source_hash,origin_started=False,
                              project_structure='not_checked_without_Origin')),flush=True)
        return
    args.output_dir.mkdir(parents=True,exist_ok=False)
    require_interactive_origin_context()
    with origin_job_slot(job_kind='optimize-perspective-waterfall'):
        with OriginSession(keep_open=False) as session:
            op=session.op
            assert op.open(str(args.source),asksave=False)
            expected=originals(op)
            for i in range(8):
                sheet=op.find_sheet('w',f'[ep{i+1:03d}]Sheet1')
                if sheet is None or not 2<=sheet.cols<=5:
                    raise ValueError('Use the original ep001-ep008 backup, not a finished figure')
            old=op.find_graph(args.source_graph)
            old.name='PreviousPerspective'
            graph=op.new_graph('PerspectiveWaterfall',template='Line')
            graph.name='PerspectiveWaterfall'
            layer=configure(op,graph)
            reference=reference_planes(op,layer)
            print('Reference planes and scales built.',flush=True)
            records=[trace(op,layer,i) for i in reversed(range(8))]
            theta=math.radians(ANGLE_X)
            pos=offset(project(TIME_MAX/2,0,0),.90*math.sin(theta),-.90*math.cos(theta))
            label(op,layer,'TimeTitle','Time (s)',*pos,10,ANGLE_X)
            label(op,layer,'LoadTitle','Load power (kW)',-200,4.5,10,90)
            label(op,layer,'DatasetLabel',args.dataset_label,-220,34,10)
            # Preserve the earlier graph inside the isolated candidate project.
            graph.activate()
            op.lt_exec('doc -uw;')
            state=verify(op,graph,expected,records,reference)
            assert op.save(str(target.with_suffix('.opju')))
            assert op.open(str(target.with_suffix('.opju')),asksave=False)
            graph=op.find_graph('PerspectiveWaterfall')
            reopened=verify(op,graph,expected,records,reference)
            meta=export(op,graph,target)
            assert digest(args.source)==source_hash
            report=dict(source_sha256=source_hash,source_unchanged=True,original_tables=expected,
                        environment=session.environment.to_dict(),records=records,
                        projection='x=time+180*(i+0.65); y=load+3.3*(i+0.65)-0.0026*time; i=0..7, display only',
                        projection_angles_deg=dict(time=ANGLE_X,depth=ANGLE_DEPTH),
                        fill_style=dict(transparency_percent=FILL_TRANSPARENCY,fill_only=True,opaque_contours=True,
                                        implementation='separate native fill and contour plots'),
                        typography=dict(font='Arial',ticks_pt=8.5,voyages_pt=8.8,titles_pt=10),
                        reference_geometry=reference,before_save=state,reopened=reopened,export=meta,
                        visual_qa=dict(status='pending'))
            (args.output_dir/f'{STEM}_verify.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
            print('Saved, reopened and verified original data and display projection.',flush=True)


if __name__=='__main__':
    main()
