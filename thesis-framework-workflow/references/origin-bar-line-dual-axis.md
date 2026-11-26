# Origin 下柱上折线双 Y 轴组合图

触发词：“下柱上折线”、“上面折线下面柱状图”、“总量柱图与时序曲线合图”、“双 Y 轴组合图”、“复用柱线组合样式”。

用于在同一画框内展示几种策略的总量比较及对应时序。下部是从零开始的渐变柱，读左轴。上部是原生折线，读右轴。两层共享画框位置，各自绑定 X 数据。此处的上下分区是本图型的视觉组织，不是标准的同 X 柱线叠加图。

主入口：[render_bar_line_dual_axis.py](../scripts/render_bar_line_dual_axis.py)。输入模板：[manifest.json](../examples/bar-line-dual-axis/manifest.json)、[总量表](../examples/bar-line-dual-axis/totals.csv)及[时序表](../examples/bar-line-dual-axis/curves.csv)。[合成示例预览](../assets/bar-line-dual-axis/example.png)仅展示样式，不含真实实验数据。

## 数据与适用条件

- 柱图 X 表示类别，折线 X 表示时间或另一连续自变量，不能把某柱的横向位置解释为对应时刻。`line_x_axis.show=true` 可显示顶部时间轴，此时画框 top 至少为 10%，例如 `layer_percent=[25,13,52,74]`。参考复刻式布局默认隐藏该轴，正式使用时应显示或在图注明确时间范围与两套 X 域。
- 柱高和曲线分别来自只读 CSV。总量与时序的统计、单位及对应关系由作者确认，脚本不积分、不归一化、不拟合、不平滑、不插值，不要求总量必然等于曲线终值。
- 柱高非负，左轴从零开始。折线须有至少两个有限、严格递增的 X，Y 落在声明的上部可见范围。缺测、重复时间及超界值会报告错误，不静默删点、连缺口或截去极值。
- 原截图曲线单位曾写作 g/s。共享示例采用明确的“累计氢耗 (g)”及虚构数据，不沿用截图的单位歧义、算法名或数值。真实瞬时氢耗率仍可使用本图型，但须改成对应单位。
- 同一模型的颜色、线型、符号沿用当前项目编码。中性渐变柱、紫色参考线及降幅标注是可选样式，不覆盖作者已有图形约定。降幅线不是误差棒。

## 原生构造与已解决的问题

创建两个等位置、等大小的 Origin 原生图层。第一层绘制柱、类别文字、柱值、参考虚线及比较括线。第二层透明叠加折线与右轴，X/Y 均解除与第一层的数值链接。工作簿保留原数据，辅助线单独存在 `DisplayGeometry` 工作簿。图例、轴、文字、柱和曲线均可在 OPJU 中编辑，不嵌入图片冒充数据图。

右轴的 `upper_limits=[a,b,step]` 定义上部实际读数，`upper_fraction=f` 指定上部占整个画框的高度比例。完整图层右轴范围计算为 `[b-(b-a)/f,b]`，只在 a…b 设置原生刻度。下方留白用于柱图，隐藏区域的负刻度不是测量值。左轴上限必须使全部柱高处于下部分区，预检会拦截重叠。

可复用的 Origin 细节：

- 用 `layer.unit=1` 和显式页面尺寸固定两层几何，`layer.link=0` 解除链接，第二层背景透明并去掉额外边框。
- `showAxes` 和 `showLabels` 是轴对共享的位字段。设置右轴时最后写 `layer.y.showAxes=2;layer.y.showLabels=2;`，并启用 `y2.showlabel`。之后再写 `y2.showAxes=1` 会改变轴对显示，曾造成右轴数字消失。保存后要回读并看实际导出。
- 用 `layer.y2.ticksbydata$` 明确列出右轴的可见数值，不能只画刻度线却隐藏数字。
- 原生 `set -pfm 3`、`-pfb`、`-pff` 设置双色渐变。`-vg` 表示柱间空隙百分比，应小于 100。`-w` 使用 1/500 pt，而轴线宽直接使用 pt。
- 删除模板生成的 `xb/xt/yl/yr` 及旧图例，再添加显式轴题，防止第一条曲线名称被自动当作右轴标题。右轴标题留出刻度文字空间。

实现分别在 [输入契约](../scripts/bar_line_inputs.py)、[原生样式](../scripts/origin_bar_line_style.py)和[回开验证](../scripts/verify_bar_line_dual_axis.py)。这是独立图型入口，不冒充 EditaPlot 通用 catalog 已注册模板。

## 清单中可改的内容

`schema_version=1`、`chart_type="bar-line-dual-axis"`。CSV 文件相对清单解析，与当前终端目录无关，可带可选 `sha256`。不接受机器专属的绝对 CSV 路径。

| 字段 | 含义 |
|---|---|
| `synthetic` | 合成示例标记。为 true 时图内显示 Synthetic example，真实研究输入不得冒用示例数据 |
| `page_cm`、`layer_percent` | 图幅及共享画框 `[left,top,width,height]` |
| `font`、`font_sizes`、`axis_width_pt`、`line_width_pt` | 已安装字体及物理字号/线宽。中文可按项目约定使用 Origin 富文本字体命令 |
| `left_axis.title/limits` | 柱图物理量、单位及 `[0,max,step]` |
| `right_axis.title/upper_limits/upper_fraction` | 折线物理量、可见刻度范围及上部高度比例 |
| `line_x_axis.title/limits/show` | 连续 X 轴名称、范围及是否显示顶部轴 |
| `bars.file/category_column/value_column` | 总量表、类别列和数值列，CSV 行顺序决定柱顺序 |
| `bars.fill_colors/edge_color/gap_percent/value_format` | 两种渐变色、边线色、柱间空隙和柱值格式 |
| `bars.legend/guide_color/guide_lines/category_dividers` | 柱图例、辅助线颜色、总量虚线及类别分隔线 |
| `series[]` | 每条折线的 id、label、file、x_column、y_column、color、marker。可各用独立 CSV 和时间长度 |
| `comparisons[]` | 选定 `from/to` 类别、括线位置 x 和文字方向 orientation。可省略 |

比较百分比按 `(from-to)/from×100%` 计算，分母必须为正。括线 `x` 使用柱图显示坐标，第一柱中心为 1。`orientation` 可取 horizontal 或 vertical，`format` 默认为 `.1f`。负值保留负号，不把增长静默改成降幅。

更换类别数、长标签、负值折线、字体或图幅后应检查相应布局。脚本支持满足契约的多条曲线和至少两类柱，但实际图面示例验证覆盖三类柱、三条曲线，其他密度不自动宣称排版已通过。

## 独立运行与迁移

复制**整个原技能目录**即可携带脚本、示例和 `embedded/editaplot/runtime` 源码。不要求原电脑的项目、AGENTS.md、全局 skill、临时剪贴板图片、Origin MCP、EditaPlot 安装路径或环境变量。无需备份工程作为模板，脚本从原生对象创建新图。

`--check-only` 仅用 Python 3.11+ 标准库，可在没有 Origin 和第三方包的环境运行。实际制图需要 Windows x64、已安装 Origin/OriginPro、CPython 3.11/3.12，以及[兼容说明](portability.md#windows-原生制图)所列隔离环境依赖。复制技能不会安装 Origin，也不会使原生自动化在 macOS/Linux 运行。已验证主机为 Origin 2026，其他版本在目标主机验证。

在 **PowerShell** 中运行，先选择复制后的技能目录和已准备好的 Python。完整顺序如下，输出采用新目录，不覆盖已存在结果：

```powershell
$skillDirectory = Read-Host '输入此技能目录的完整路径'
Set-Location -LiteralPath $skillDirectory
$figurePython = Read-Host '输入兼容 Python 可执行文件路径或命令名'
$candidate = Join-Path ([System.IO.Path]::GetTempPath()) ('bar-line-demo-' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
& $figurePython -B -X utf8 .\scripts\render_bar_line_dual_axis.py --manifest .\examples\bar-line-dual-axis\manifest.json --output-dir $candidate --check-only
& $figurePython -B -X utf8 .\scripts\render_bar_line_dual_axis.py --manifest .\examples\bar-line-dual-axis\manifest.json --output-dir $candidate
Get-Content -LiteralPath (Join-Path $candidate 'bar-line-dual-axis_run.jsonl') -Tail 10
```

没有兼容依赖时先按[隔离环境配置](portability.md#windows-原生制图)准备，勿修改全局 Python。脚本是一次性运行，不启动网页或常驻服务，正常结束自动释放自建 Origin 实例。可从另一 PowerShell 查看日志。确需取消时在运行窗口按 Ctrl+C，由会话清理处理，不强杀其他 Python/Origin 进程。

macOS/Linux 终端先 `cd` 到复制后的技能目录，只运行预检：

```bash
python3 -I -S scripts/render_bar_line_dual_axis.py --manifest examples/bar-line-dual-axis/manifest.json --output-dir /tmp/bar-line-demo --check-only
```

输出包括同名 OPJU、600 dpi PNG、EMF，以及预览、灰度图、运行日志和 `_verify.json`。输入副本及重写后的相对清单存于 `inputs/`，可换电脑再次交给本入口。源 CSV 不改写。原生编辑以 OPJU 为准，不仅凭 EMF 扩展名声称全部对象为矢量。

## 验收

脚本实际保存并回开 OPJU，逐点比对全部柱值、类别及每条折线 X/Y，核对图层、轴限、原生右轴刻度和可见性、渐变模式、颜色、标签、物理图幅、输入哈希及导出 DPI。输出清单会保留比较方向和百分比，回读不会把结构验证写成视觉验收。

最终查看 PNG 和灰度预览，核对右轴每个数字、轴题间距、无额外分区横线、上下区域不重叠、柱值与比较标注、曲线末端及图例。`visual_qa.status` 默认 pending，看图后再据实际范围记录。新主机验证至少完成这轮检查，不将本机历史通过推广为所有 Origin 版本通过。

迁移核验记录见 [图型验证记录](bar-line-dual-axis-validation.json)。其中只记录实际完成的搬移目录、无第三方包预检及原生回开范围，不声称已在另一台物理电脑测试。
