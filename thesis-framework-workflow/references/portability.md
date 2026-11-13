# 独立使用与环境兼容

直接复制当前技能目录即可保留知识、模板、数据示例与制图源码。目录名称、盘符、用户名和上级项目均可不同，不读取原作者的其他目录或全局技能。个人模板、真实稿件与科研数据是使用者按任务提供的输入，不是包本身的依赖。核心任务从根 SKILL.md 路由，不自动执行所有内嵌技能。

不同 AI 客户端的发现机制和工具权限不同。若未自动识别此技能，把复制后目录的 `SKILL.md` 提供给当前 agent，并按入口中的相对链接读取适用参考。只具备文本读取能力时仍可使用论文框架、语言规则和示例。写作基础所参考的 `embedded/humanizer-zh/` 与 `embedded/lieflat-less-ai-tone/` 均随包提供，不需要访问原电脑。样本、项目规则和目标期刊规范由当前使用者提供，中文语料规则不直接作为英文语法规则。不同模型对同一指令的执行可能不同，实际使用时以内容核查为准，不能仅凭格式通过就断言所有 agent 的结果一致。

## 能力与平台

| 能力 | 依赖 | 兼容范围与缺项处理 |
|---|---|---|
| 框架、证据、写作、协作与交接 | 读取 Markdown 的工具或 AI 客户端 | 不依赖操作系统、原工程或原会话 |
| 查看示例与学习图面 | 包内 PNG | 普通图片查看器即可，示例不代表读者的实验数据 |
| 包检查、合成 CSV 预检 | Python 3.11/3.12，标准库 | Windows/macOS/Linux 可运行设计，不启动 Origin，不写输出 |
| 原生 Origin 图与 OPJU 回开 | 物理 Windows x64、独立安装的 Origin/OriginPro、Python 3.11/3.12 及依赖 | 当前实测为 Windows + Python 3.12 + Origin 2026。本机输出证据不推广为其他系统实测，其他构建按能力核验 |
| 编辑及查看 Word/WPS | 当前电脑可用文档工具、相应字体 | 无 Word 时可做结构检查，但不宣称完成实际 Word 版式或 OLE 验收 |
| LaTeX、MathType、Pandoc、文献数据库或 MCP | 按当前任务选择的工具 | 均为可选外部能力，不随技能复制安装，也不是使用核心方法的前提 |

macOS/Linux 可使用工作流、示例、文本及数据预检。本包不把在这些系统生成的图片冒充原生 Origin 工程。跨机器字体、Origin 构建、打印驱动和 Office 版本可能影响字形与页面，实际输出须回开及查看，不能保证像素跨系统完全一致。

## 文件职责

- `references/` 与 `assets/templates/`：按任务读取的完整方法与工作底稿。
- `examples/waterfall/`：八条合成 CSV 和 manifest.json，内含源哈希，全部可独立检查。
- `assets/waterfall/`：由包内合成数据生成的 Origin PNG 示例及标签细节。没有截图中的桌面、路径或工作代号。
- `assets/templates/two-level-three-line-table.docx` 及同名 PNG：虚构指标的两级表头示例。物理类别、数学指标与单位分层，组线留断口，可自定义，读取不依赖原作者软件路径。
- `scripts/build_table_example.py`：从虚构数据生成可编辑表格，依赖当前主机的 `python-docx`，不启动 Word。已安装环境可直接使用，没有该依赖时仍可阅读包内 DOCX 或 PNG。
- `scripts/render_waterfall.py`：manifest 相对路径读取数据、只读预检与新候选目录渲染。
- `embedded/editaplot/runtime/`：EditaPlot 自动化源码和模板，不含 Python 虚拟环境、软件安装包或私人配置。保留 Apache-2.0 LICENSE、NOTICE 与来源记录。
- `embedded/` 其他工具：按需参考的文档和脚本，不要求安装到任何全局技能路径。文档操作和可选 UI 的外部程序按当前主机定位，不猜测其他人的目录。

## 首次检查

打开 PowerShell，粘贴下列完整步骤。先通过输入选择你实际复制的技能目录，再检查包与合成数据，无须知道原作者路径：

```powershell
$skillDirectory = Read-Host '输入此技能目录的完整路径'
Set-Location -LiteralPath $skillDirectory
py -3.12 -B -X utf8 .\scripts\check_package.py
$demoOutput = Join-Path ([System.IO.Path]::GetTempPath()) ('waterfall-demo-' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
py -3.12 -B -X utf8 .\scripts\render_waterfall.py --manifest .\examples\waterfall\manifest.json --output-dir $demoOutput --check-only
```

若电脑用 `python` 而非 `py`，将 `py -3.12` 替换为已确认的 Python 3.11/3.12 命令。macOS/Linux 在终端进入实际技能目录后用 `python3 -B scripts/check_package.py` 和 `python3 -B scripts/render_waterfall.py --manifest examples/waterfall/manifest.json --output-dir /tmp/waterfall-demo --check-only`。这些是一次性检查，不启动网页或后台服务，正常结束即可。

## Windows 原生制图

先按上节进入技能目录。首次需要原生渲染时，使用项目隔离环境安装依赖，不复制别人的虚拟环境。以下命令需要网络取得 Python 包，已有兼容环境时直接使用它，不重复安装或修改全局 Python：

```powershell
py -3.12 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r .\embedded\editaplot\runtime\requirements-runtime.txt -c .\embedded\editaplot\runtime\requirements-runtime.lock
& .\.venv\Scripts\python.exe -B .\embedded\editaplot\scripts\editaplot.py doctor
& .\.venv\Scripts\python.exe -B -X utf8 .\scripts\render_waterfall.py --manifest .\examples\waterfall\manifest.json --output-dir $demoOutput
```

Origin 由脚本创建独立实例并正常关闭，不要求用户提前启动，不接管已有工程。不使用网页服务。运行中观察阶段输出，失败时保留诊断并检查正常清理，不因等待直接强杀进程。输出目录已存在时选新目录，不删除旧目录。安装依赖不等于已生成 OPJU，`doctor` 也不等于实际制图验收。

## 接入自己的数据

复制 manifest 和 CSV 到当前使用者的数据目录，修改清单的文件名、列名、单位缩放、标签及划分。CSV 路径相对 manifest 解析，可不使用任何原工程结构。可选源 SHA 在文件内容改变后应由使用者重新登记，不忽略不匹配。详见 [数据契约与制图](origin-perspective-waterfall.md#复现脚本与运行)。真实数据不打包进共享技能。

## 迁移与隐私检查

移动或改名后从新位置运行 `scripts/check_package.py` 和 demo 预检。诊断只输出相对资源名、能力和错误类型，不写用户名、盘符、原实验编号或历史会话。源文件哈希可记录，含真实绝对路径的本次运行报告属于本地核验材料，不复制进共享技能。

检查范围包含根入口、相对链接、资源缺失、包内数据哈希、缓存及私人路径。第三方作者署名、许可与上游软件名不属于本项目工作代号，不做匿名篡改。已有第三方快照仍遵循各自许可证，公开或第三方分享前按 [分发说明](publication-review.md) 核对范围。

此前的实际检查记录见 [匿名验证记录](validation.json)，其中链接数量和环境反映记录时的版本，不代表当前包已重新执行同样的全部检查。每次更新或迁移后重新运行检查。示例清单或数据缺失、损坏时，包检查以非零状态报告缺失资源和样本错误类型，不将失败误报为通过。

历史检查中，关闭 site-packages 后包检查与数据预检通过，目录移到中文及空格路径并从其他工作目录调用后，本机原生 Origin 出图、回开、标签与便签检查通过。另以 Word 16.0 原生导出一页表格模板并检查图面、两级表头、数学对象及分组短线，不推广为全部长表或其他软件实测。写作材料为人工整理的通用方法与虚构例句，不含作者研究数据。
