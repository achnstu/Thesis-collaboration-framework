# 本机执行与 Origin 2026 坑点

## 可复现入口

正式脚本位置：
`C:/Users/zwzhu/Desktop/萝卜论文/markov_drl/大论文/图表文件夹/01_Origin作图/第2章_原理与建模`。

- `C2_load_origin.py`：D01/D02 的数据导入、多层图、字体、导出、回开验证。
- `C2_D01.py`、`C2_D02.py`：单图入口。
- `C2_D03.py`：航程等权双分布、显式阶梯节点、统计及原始表副本回读。

打开 PowerShell，先进入项目技能目录，按顺序运行。以下是 D03 示例，D01/D02 只替换 Figure 值。

```powershell
cd "C:\Users\zwzhu\Desktop\萝卜论文\markov_drl\大论文\.skills\markov-thesis-origin-figures"
& ".\scripts\draw_chapter2.ps1" -Figure C2-D03 -CheckOnly
& ".\scripts\draw_chapter2.ps1" -Figure C2-D03
```

这是一次性任务，没有网页或常驻服务。正常结束会释放自建 Origin 实例。需要保留窗口时添加 `-KeepOpen`。不要强杀可能正在保存的 Python 或 Origin。失败先读章目录的 `C2_D03_run.log` 和验收 JSON。

## 环境与生命周期

本机运行时：

`C:/Users/zwzhu/.local/share/editaplot/editaplot-main/runtime/.editaplot-venv/Scripts/python.exe`

Origin：`D:/Program Files/OriginLab/Origin2026/Origin64.exe`。
EditaPlot 引擎默认从用户 `.local/share/editaplot/editaplot-main/runtime/src` 导入，可用 `EDITAPLOT_ENGINE_HOME` 指向 runtime 根。

开始新的独立作图任务时读取已安装的 `C:/Users/zwzhu/.codex/skills/editaplot/SKILL.md` 和所需安全、验证参考。运行其只读 doctor。首次环境或版本变化后做真实独立实例 smoke，核验能力。相同任务内环境未变且已成功，不重复启动 smoke。

这是项目专用路线，复用 EditaPlot 的生命周期、串行队列和验证工具，不是其内置模板渲染命令。作者的统计定义、目录、字体和三格式交付优先。通用模板的语义确认哈希不得手改绕过，新图若改用通用模板则走该模板真实门禁。

新脚本按已有实现使用：

1. `require_interactive_origin_context()` 验证真实 Windows 执行上下文。
2. `origin_job_slot(job_kind="render")` 串行占用。
3. `OriginSession(keep_open=...)` 启动独立、归当前任务所有的实例。
4. 读入只读源表 → 声明显示转换 → 原生对象绘图 → 导出 → 保存 → 回开核验。

不 attach 用户已有工程，不改安装、DCOM、注册表或系统 Graph Options。队列等待不重复提交。遇激活失败按运行时的有界清理和重试策略处理，保留诊断，不靠循环试到成功。

MCP `origin` 可用于连接、导表和通用操作。当前窗口未暴露工具时，优先直接用已验证的项目脚本，不反复重装。连接问题读 `C:/Users/zwzhu/.codex/skills/origin-mcp-local/SKILL.md`。桥接若持有同一 job slot，需正常 shutdown 后再启独立脚本，不能双路同时占用。

## 已验证的 API 单位和写法

- 本机 `font(宋体)` 返回有效码 404，`font(Times New Roman)` 返回 374，`font(SimSun)` 返回 0。动态读取并核查，不把 font code 当跨机器常量。
- 页宽高使用英寸：先 `page.updatetoprinter=0;page.kar=0;doc -uw;`，再 `graph.obj.PutWidth(cm/2.54)`、`PutHeight(cm/2.54)`。回读用 `page.width/page.resx*2.54`、`page.height/page.resy*2.54`。
- 图层百分比坐标必须 `unit=1`、`factor=1`。`layer -x` 返回 v1宽、v2高、v3左、v4上，用 `read_layer_geometry_percent` 双路径核查，不能把 v1 当左边距。
- 曲线 `set -w` 单位是 1/500 pt，0.7 pt 使用 `-w 350`。实线 `-d 0`、虚线 `-d 1`，用 `get -w/-d/-c` 回读。坐标轴 thickness 直接写 0.6。
- 文本需明确字号、字体、旋转、位置和 `attach=1`。回读图例时把 `\r\n` 规范为 `\n` 再比文本，不能把 Windows 换行误判成内容变化。
- 旋转中文的实际字形可能超出对象报告的框，D03 左绘图区留 1.20 cm 边距才完整。应看导出图验证，不能只信对象框。

原生全页导出（正式实现见 `C2_load_origin.export`）：

```text
expGraph type:=png export:=page filename:="C2-D03" path:="<output>"
 overwrite:=replace sysopts:=0 tr.Margin:=2 tr.SpeedMode:=2
 tr1.Unit:=2 tr1.Width:=3898 tr2.PNG.DotsPerInch:=600;
expGraph type:=emf export:=page filename:="C2-D03" path:="<output>"
 overwrite:=replace sysopts:=0 tr.Margin:=2 tr.SpeedMode:=2
 tr.Advanced.Resolution:=1 tr1.Unit:=3 tr1.Width:=100;
```

16.5 cm × 600 dpi 约 3898 px。`tr.Margin:=2` 保留全页，否则默认紧裁剪会改变物理图幅。`tr.SpeedMode:=2` 避免导出抽点。PNG DPI 必须读取元数据验证，不能只用像素宽度推断。

## 新图适配

直接复用最接近的正式章脚本，保留源表哈希、输入角色、显示转换和回开核验。新曲线类型先查 originpro 本地源码及对应官方 API，做最小原生能力试验。实际生成 OPJU、PNG、EMF，回开逐点检查并看图通过后，才能称本项目路线已验证。图幅按内容调整，不把 D03 的具体边距强套所有图。

官方依据：

- https://docs.originlab.com/externalpython/
- https://docs.originlab.com/labtalk/ref/layer-axis-obj/
- https://docs.originlab.com/labtalk/ref/set-cmd/
- https://docs.originlab.com/x-function/ref/details-of-treenodes-in-export-graph/

2026-10-25：Origin 2026 的 EditaPlot 真实 smoke、MCP 官方 smoke、第2章三张专用图均实际完成。通用运行时仍可能将该版本报告为 `compatible_unverified`，保留原报告，另记录本机具体路线证据，不伪改成全模板认证。
