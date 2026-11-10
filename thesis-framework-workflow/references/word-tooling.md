# Word 工具选择与对象保护

触发词: “怎么调用 Word”, “OfficeCLI”, “DOCX 定点修改”, “Word 原生渲染”, “只替换图片”。

先确认任务是新建文档、编辑普通内容、保护复杂对象，还是验证实际排版，再选当前机器可用的工具。技能文档被读取、命令被探测、文件实际改写、页面已核验是不同状态，不能混称为“已使用并验证”。

## 已核实的方法与工具分工

匿名返修案例实际使用 `python-docx` 创建表格和回复信，用 `lxml` 与 ZIP 成员级修改保护公式、引用域及已有媒体，再用 `win32com.client.DispatchEx('Word.Application')` 创建独立 Word 实例，重新分页并导出 PDF 供逐页查看。在已检查的相关对话与执行脚本中，未发现 OfficeCLI 实际改写这些稿件的记录。包中存在 OfficeCLI 技能入口不等于当时执行了它。

| 工作 | 可选工具 | 验证边界 |
|---|---|---|
| 新建普通段落、样式、表格、图题和回复信 | `python-docx` 或 OfficeCLI | 回开核对文本及对象，随后渲染 |
| 查询结构、批量修改工具明确支持的属性 | OfficeCLI | 先读包内技能和当前版本 help，再读取修改结果 |
| 保留 MathType/OLE、OMML、引文域，定点改少数节点 | OOXML、`lxml`、`zipfile` | 比较目标节点及非目标 ZIP 成员，检查关系和内容类型 |
| 仅替换已嵌入的同格式图件 | ZIP 媒体成员定点替换 | 必须先经关系映射确认目标，检查尺寸、关系及其余成员 |
| 实际 Word 排版、EMF 显示、页码与 PDF | Windows Microsoft Word COM | 记录 Word 版本、页数并查看导出页面 |
| 无 Word 的机器 | 可用的文档编辑器或渲染器 | 明确实际使用的软件，不称已完成 Word 原生或 OLE 可编辑验收 |

编辑入口见 [DOCX](../embedded/docx/SKILL.md) 与 [OfficeCLI](../embedded/officecli/SKILL.md)。不要因为工具可用就重写作者当前稿件。

## OfficeCLI 的正确接入

优先读取当前版本 `help`，不猜属性。先在候选副本完成一处小修改，核对读回值和页面，再扩大范围。使用驻留会话时，在 Python、Word 或其他程序读取文件之前执行 `save` 或 `close`，避免外部工具看到尚未落盘的内容。不要让多个工具同时写同一个文件。

OfficeCLI 的结构校验与 HTML 预览不等同于 Microsoft Word 对 EMF、OLE、引用域及分页的显示。执行记录应写明实际命令、成功状态、改动范围、读回及渲染工具。尚未运行时写“可选入口，未执行”，不要把文档中的能力写成当前任务的验证结论。

## 保护对象的定点编辑

编辑前保存可恢复副本，并记录源稿哈希、目标范围和对象基线。存在公式、字段、书签、修订或 OLE 的段落，不直接对整个 `paragraph.text` 或 `cell.text` 赋值。先按节点边界定位，保留公式位置、字段指令、显示结果、编号制表位及必要格式。

对象数量和字节不变只证明保护有效，还要核对公式语义、上下标、均值横线、定义、单位与实现是否一致。发现原式有误时，单独提出并按授权修正，不能把“对象未动”写成“公式正确”。

仅更新图件时，通过 `document.xml` 的图片关系 ID 查询 `.rels` 的实际 Target，不凭 `image1.emf` 猜测。仅在媒体类型、尺寸策略与关系均适用时替换对应 ZIP 成员。若格式变化，需同步内容类型和关系，不能只改扩展名。检查其余 ZIP 成员内容字节相同，不能要求整个压缩包的字节相同。

候选验收后再检查源稿哈希。作者在期间手改过时，以最新源稿重新定位并应用本轮改动。文件被 Word/WPS 锁定时保留候选，等待正常保存关闭，不终止用户进程或强行覆盖。

## Word COM 生命周期与原生核验

仅在 Windows、已安装 Word 且 COM 可用时执行。用 `DispatchEx` 创建本任务独立实例，设置不可见及适当提示策略，用绝对路径只读打开候选，执行 `Repaginate()`、`ComputeStatistics(2)` 和 `ExportAsFixedFormat(..., 17)`。在 `finally` 中关闭本任务文档和本任务实例，不退出用户已有 Word 窗口。

PDF 导出后再渲染为 PNG 并查看受影响页面。表格重排、新建文档或全篇格式变化需要覆盖所有相关页。定点替换图件可同时比较前后页数、图题同页性、图片尺寸和未改页像素。只有同环境、同设置的比较才适合使用像素差，不把“无像素差”当作语义或可编辑性证明。

字体从作者主稿或模板读取。示例使用 Arial 只是示范，不强制更改其他作者文档。Word、WPS 和其他渲染器可能有不同分页，分别报告软件和实际检查范围。

## 包内可编辑示例

[两级表头 DOCX](../assets/templates/two-level-three-line-table.docx) 可独立打开，[PNG](../assets/templates/two-level-three-line-table.png) 供无 Word 的读者查看。示例采用“物理类别—数学指标及单位”，各类别短线留断口，指标为原生 OMML。全部数值虚构，作者及关键词元数据不含私人信息。表头分组、列名、数值和表注可直接修改，字体与线宽以目标格式为准。

[生成脚本](../scripts/build_table_example.py) 仅用于重新生成示例，依赖当前环境的 `python-docx`，不依赖 COM、OfficeCLI 或原作者目录。Word COM 仅用于本次页面核验，不是阅读模板或运行核心技能的前置条件。

重新生成时，在 PowerShell 中按顺序粘贴以下步骤。输入实际技能目录，输出写到新的临时文件，不覆盖包内模板：

```powershell
$skillDirectory = Read-Host '输入此技能目录的完整路径'
Set-Location -LiteralPath $skillDirectory
$tableExample = Join-Path ([System.IO.Path]::GetTempPath()) ('table-example-' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.docx')
py -3.12 -B -X utf8 .\scripts\build_table_example.py --output $tableExample
```

已有环境缺少 `python-docx` 时，使用已配置的项目文档环境，或在隔离环境安装该依赖。其他系统在终端进入实际技能目录后，用该环境的 Python 执行同一脚本并指定新输出路径。生成脚本只负责结构，不声称已完成本机 Word 显示检查。没有网页服务，运行结束即停止。
