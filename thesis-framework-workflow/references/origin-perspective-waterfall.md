# Origin 多航程透视瀑布图

触发词: “透视瀑布图”, “多航程瀑布图”, “增加壁面和底面”, “瀑布图透明度”, “EP 标签遮挡”, “复用瀑布图样式”。

适用于已选择用层叠时序展示个体轨迹及持续时间的任务。此处“瀑布图”指带填充的多条透视时序，不是财务增减瀑布柱图。有两条不同的 Origin 路线：原生 `glWater3D` 是可旋转三维图层，见下节。本文其余的透视方案用二维仿射投影及 Origin 原生曲线、填充面和文字构成，视角由绘图参数确定。精确比较幅值或细微差异时配合二维图。

## Origin 原生三维瀑布模板

用户需要在 Origin 中旋转视角时，可调用 Origin 自带 `glWater3D`。调用前按 EditaPlot 安全规则使用独立实例和任务队列，工作表至少有一个 Y 列，并可指定 X 列。官方 `plotxy` 示例是：

```text
plotxy iy:=(1,2:4) plot:=210 ogl:=<new template:=glWater3D>;
```

该调用把第 1 列作为共同 X，第 2 至 4 列作为三条 Y 曲线，样本沿 Z 方向排列。列标签可作为 Z 轴标签。输入须按真实 X/Y 关系绑定。不同时间序列不能仅凭行号套用同一 X，须使用经核实的独立 X/Y 绑定或合理构造对齐表，缺测保持缺失，不插值或伪造零值。独立 X/Y 及不等长场景尚需针对目标数据验证。

可运行 [原生模板合成示例](../scripts/native_waterfall_demo.py)，其数据由公式生成，不含原始研究数据。Origin 2026（10.30018）上已实际调用并保存、回开 OPJU，检查三条曲线、原始数值以及 `is3D=1`、`is3DGL=1` 和 `coortype=16`，同时导出 PNG、PDF、TIFF 并查看 PNG。默认图例存在遮挡，图面是能力测试，不是论文成品。示意图见 [原生三维示例](../assets/waterfall/native-3d-example.png)。

此验证不覆盖其他版本及不同 X/Y 布局，也不意味着已复现本文二维方案的颜色、75% 透明度、EP 标签、无外框和参考视角。EditaPlot 历史实验发现 OpenGL 填充或边线颜色的图面效果可能与属性读数不同，必须查看实际导出。按当前任务另行验证样式、三维旋转、坐标、图例、遮挡与文档插图效果，不仅凭属性写入成功就报告验收通过。原生模板随 Origin 安装提供，不包含在本 skill 中。

在 Windows PowerShell 中先进入当前技能目录、确认已按 [兼容说明](portability.md) 配好 Python 与 Origin，再用新目录运行：

```powershell
$skillDirectory = Read-Host '输入此技能目录的完整路径'
Set-Location -LiteralPath $skillDirectory
$candidate = Join-Path ([System.IO.Path]::GetTempPath()) ('origin-3d-waterfall-' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
& .\.venv\Scripts\python.exe -B -X utf8 .\scripts\native_waterfall_demo.py --output-dir $candidate
```

输出包含 OPJU、PNG、PDF、TIFF 和 `probe.json`。示例只执行合成数据的能力测试，正式接入用户数据须先适配、回开和逐点核验。更多细节见 Origin 官方 [3D Waterfall](https://docs.originlab.com/origin-help/3d-waterfall-graph/) 与 [plotxy](https://docs.originlab.com/x-function/ref/plotxy/)。

按任务阅读下列部分：科学口径与投影、原生实现与布局、回改与验收、复现脚本与运行。本指南补充 [通用作图规则](figures.md)，本次案例参数不覆盖其他作者、学校或图级要求。

## 科学口径与投影

先核对源文件、训练/测试划分、实际绘制列、单位、点数、时间间隔与范围。保留真实持续时间，不将不等长航程拉伸为同长，不以平滑、插值、补零或删极值换取整齐外观。读取前后核对源 SHA-256。源数据保持只读，显示坐标存于工程副本的独立列，原有列不覆盖。

设真实时间为 t、功率为 p、样本序号 i = 0…n−1。深度 d = i + s，其中 s 为前侧留空的间距。采用：

```text
x_display = t + a*d
y_display = p + b*d - c*t
baseline  = b*d - c*t
```

这里 a、b、c 是显示参数，不能解释为时间、功率或样本间的真实差值。真实零功率位于各样本基线，不是全部位于页面 y=0。图注或配套记录说明深度仅代表样本。时间刻度和功率参考线由同一投影计算，不能只改文字来伪造比例。

已验证参考样式的图级参数：

| 项目 | 参数 |
|---|---|
| 页面与图层 | 18.0 × 13.5 cm，left=8%、top=7%、width=86%、height=82% |
| 显示范围 | x: −420…3580，y: −10…36 |
| 投影 | a=180，b=3.3，c=0.0026，s=0.65 |
| 时间与功率 | 0…2060 s，刻度 0/500/1000/1500/2000，功率参考 0/3/6/9 kW |
| 字体 | Arial 常规，刻度 8.5 pt，EP 请求 8.8 pt、回开读数为 9 pt，轴题 10 pt |
| 填充与轮廓 | 填充透明度 75%，独立轮廓透明度 0%、宽 0.9 pt |
| 颜色顺序 | #0072B2、#D55E00、#009E73、#CC79A7、#56B4E9、#E69F00、#000000、#882255 |

参数适配先保持物理比例。图层在页面上的每显示单位长度为 Sx、Sy，时间方向角度为 atan2(−c·Sy, Sx)，深度方向为 atan2(b·Sy, a·Sx)。所有文字旋转与法向偏移基于这两个物理方向计算，不直接用原始坐标的斜率决定角度。

若新数据最大真实时间为 T，原参考为 2060 s，令 q=T/2060。为了复用同一物理视角，可同步令 a'=180q、c'=0.0026/q、x 显示范围整体乘 q，b、y 范围及图幅保持不变，再用真实秒数标横轴。其他范围要按新数据重新检查，不能截去超出旧 9 kW 上限的观测。

## 原生实现与布局

### 三面空间

先画底面、后壁和左壁，再从远到近画时序。令 D=n−1+s、P 为功率上限。各顶点先用同一 project(t,d,p) 投影：

| 面 | 顶点 (t,d,p) |
|---|---|
| 底面 | (0,0,0)、(T,0,0)、(T,D,0)、(0,D,0) |
| 后壁 | (0,D,0)、(T,D,0)、(T,D,P)、(0,D,P) |
| 左壁 | (0,0,0)、(0,D,0)、(0,D,P)、(0,0,P) |

将投影多边形各顶点 x 位置作为折线节点，计算上下包络，使用两条原生曲线之间的填充构造面。参考几何单独放在 `ViewGeometry` 工作簿，明确不是测量数据。用浅灰蓝分带及细参考线增强空间感，左壁略深、后壁与底面较浅，面和网格不压过数据。分带边界包含前侧空档，后壁和网格一起延伸至新 D。

在此二维构造中隐藏默认 x/x2/y/y2 轴、轴标签与网格，显示由真实刻度经过投影计算的参考轴和标签。设置 `layer.unit=1` 明确图层几何按页面百分比，显式指定图幅、坐标范围、线宽与字号。局部参数不修改全局 Origin 图形选项。

### 透明填充与清楚轮廓

每航程使用三条原生图线：填充上沿、基线、独立轮廓。填充上沿与基线相邻绑定，`set_fill_area(..., type=9)` 配合 `-pfm 3`，填充上沿线宽设为 0，`transparency=75`。随后叠加同一数据坐标的轮廓，设 `transparency=0`、`-pf 0` 关闭轮廓填充，并显式设线宽和颜色。

本机 Origin 2026 中只设置 `-paaf` 没有稳定保证导出的轮廓仍为不透明，因此采用分离的填充和轮廓。回开同时读取透明度与轮廓填充关闭属性，再查看 PNG，不能只凭写入命令未报错就宣布成功。

### EP、轴标题与边框

EP 刻度锚点为 project(0,i+s,P)。沿左壁上沿的统一外法向留出距离，本例刻度长 0.11 cm，标签中心偏移 0.68 cm，八个标签都用相同偏移，旋转角为深度方向角减 90°。先统一后移曲线形成前侧空档，再检查 ep001 与顶端功率刻度和 Load power 标题的间距，避免只移动 ep001 破坏队列。

Load power (kW) 放在前侧竖轴附近，Time (s) 放在时间轴中部，并按时间方向角旋转。图内标记由清单的 dataset_label 提供，合成示例明确标为 Synthetic example，不自动沿用其他作者的命名。

`layer.showframe=0` 才实际关闭本机导出的外侧矩形框，`layer.border=0` 单独使用不充分。无外框不等于删去用于定位空间的轴线及壁面边缘。两者均需保存后回开核对，再看实际导出。

## 回改与验收

先记录当前工程哈希并留可恢复副本。每次重绘生成新候选目录，源文件和用户已改成品不直接覆盖。验收后根据当前授权同步到指定位置，同步前再次核对现有成品是否发生人工修改，覆盖前备份，同步后比对文件哈希。复现初始工程时使用最初备份，不把已含新显示列的成品当成初始输入。

Origin MCP 能正常调用时可使用已验证桥接。桥接失效时记录失败阶段，确认本地运行时可用后使用隔离自动化实例，不因此改注册表、DCOM、全局 Python 或 Origin 安装。Origin 部分串行运行，通过 `require_interactive_origin_context()`、`origin_job_slot(...)` 和 `OriginSession(keep_open=False)` 管理会话，不重置或关闭用户实例。读取 [运行时](../embedded/editaplot/references/runtime.md) 和 [实例安全](../embedded/editaplot/references/origin-safety.md)，快照存在不代表运行引擎已安装。

保存 OPJU 后实际回开，至少核对以下证据：

- **科学数据**：所有原有列哈希一致，每条轨迹真实时间、功率、点数与源表逐点一致，单位换算正确，测试样本未混入。
- **显示坐标与绑定**：逐点验证显示 x、上沿 y、基线及曲线来源，壁面顶点、深度和时间范围一致，保留全长和极值。
- **样式与标签**：三面填充、曲线透明度和轮廓、Arial、实际物理尺寸、无外框。读取八个 EP 中心与相邻差分确认等距，读取旋转确认平行，确认 ep001 与轴题及顶端刻度有正间距。
- **角度精度**：Origin 保存的负角度可能归一到 0…360°，且回开按 0.1° 取整。用圆周角差比较，允许不超过 0.051° 的舍入差，不误判 318.7° 与 −41.3°。
- **实际导出**：OPJU、PNG、EMF 非空，记录尺寸、DPI 和 SHA-256。本例 PNG 为 4252 × 3189 px，元数据约 600 dpi。透明填充在 EMF 中含位图记录，不声明 EMF 全部为矢量，编辑以 OPJU 为准。

查看实际 PNG 的文字墨迹、间距、遮挡、透明效果、曲线末端及裁切。程序检查、AI 图面检查、作者确认与 Word 实际插入检查分别登记。图像未看时 `visual_qa.status` 保持 `pending`，AI 看过可记 `passed_agent_visual_review`，不据此声称作者已确认。

核验记录可沿用脚本的 `source_files/source_sha256`、`source_verification`、`records`、`projection`、`reference_geometry`、`reopened.label_layout`、`fill_style`、`environment`、`export` 和 `visual_qa` 字段。脚本不会自动宣布图面通过，交付时补记输出哈希、备份和同步位置。

## 复现脚本与运行

主入口为 [render_waterfall.py](../scripts/render_waterfall.py)，输入是 [包内合成示例](../examples/waterfall/manifest.json)。不要求原作者 OPJU、数据指针、文件名、训练编号或外部技能。包内八条合成 CSV 共 968 点，明确标为 synthetic，不构成任何真实科研结论。图面可直接查看 [完整 PNG](../assets/waterfall/perspective-example.png) 和 [标签细节](../assets/waterfall/label-detail.png)。

清单包含 schema_version=1、x_column、y_column、y_scale、轴题、dataset_label、time_ticks 和八个 series。每项 series 含自选 id、label、相对 CSV 文件名与可选 sha256。CSV 路径相对清单本身解析，与当前终端目录无关。无 sha256 时仍记录运行前后哈希，有 sha256 时必须匹配。

这是一套可选模板，作者可更换图型或改动布局，不要求论文都照此绘制。标签与便签不固定：

| 清单字段 | 自定义内容 |
|---|---|
| dataset_label | 数据集或图内标题，可留空 |
| x_title / y_title | 坐标名与真实单位 |
| series[].label | 每条轨迹的显示名，不要求叫 ep001 |
| series[].color | 可选六位 HEX 颜色 |
| fill_transparency_percent | 可选 0–100 整数，默认 75 |
| annotations[] | 任意便签文字 text、位置 x/y、字号 size_pt、旋转 rotation_deg 和颜色 color，可不提供 |

便签位置为图层范围的相对坐标，x 从左到右、y 从下到上，均为 0–1。例如 `{"text":"Editable note","x":0.75,"y":0.95,"size_pt":9,"rotation_deg":0,"color":"#303840"}`。这些文字生成原生 Origin 标签，可在 OPJU 中继续双击修改、拖动、增删。重排后仍要查看遮挡与裁切，不把示例字号、文本或位置当成学术规范。

当前已验证模板契约：八条轨迹，时间从 0 开始且严格递增、配对观测有限、换算后的纵轴值在 0–9 范围。采样间隔可以不等长，但不擅自补点，时间单位由清单轴题明确。模板不静默截断超界值。其他曲线数、负值或更大功率范围须适配所有壁面、刻度和验证后再用。

原始 x 和 y 列导入 Source001…Source008，真实时间与按 y_scale 换算后的值导入 ep001…ep008，显示坐标另存。各轨迹保留完整持续时间。output-dir 必须是数据目录外的新候选目录，脚本拒绝覆盖已有文件。默认输出名 perspective-waterfall，可用 --stem 指定匿名文件名，不把项目工作代号写进共享示例。

运行顺序、隔离 Python 安装与跨平台范围见 [独立使用与兼容](portability.md)。先运行 scripts/check_package.py，再对 manifest 运行 --check-only，最后在具备 Origin 的 Windows 电脑实际渲染。预检只用 Python 标准库，不启动 Origin、不写输出。包内源码通过相对路径定位 embedded/editaplot/runtime，不搜索原作者用户名或全局安装目录。

[origin_waterfall_style.py](../scripts/origin_waterfall_style.py) 是共享样式模块，[waterfall_inputs.py](../scripts/waterfall_inputs.py) 负责数据契约和几何缩放。新建图应优先使用 manifest。确需回改用户提供的已有工程时，样式脚本要求显式指定 --source、--source-graph 和新的 --output-dir，不能假定旧工程名。它只适配八个 ep 工作簿前两列的原始结构，已投影成品不能自动当作初始工程。

所需安全与运行文档保留在 [EditaPlot](../embedded/editaplot/SKILL.md)，联动说明见 [内嵌集成](../embedded/editaplot/references/thesis-waterfall-integration.md)。该自定义图型不伪装成通用 catalog 已注册模板。原生输出仍需实际保存、回开、属性核验和 PNG 查看后才能报告完成。
