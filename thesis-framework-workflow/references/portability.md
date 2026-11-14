# 迁移、复现与分发

整目录复制即可保留核心方法、模板、合成数据和自动化源码。路径从本包或输入清单相对解析，不要求原作者工程、盘符、全局技能或历史会话。真实稿件、数据和目标规范由当前使用者提供。不同客户端的技能发现与工具权限不同，未自动识别时直接提供本包 SKILL.md，并按任务读取其相对链接。

## 能力与依赖

| 任务 | 所需能力 | 实际边界 |
|---|---|---|
| 框架、证据、写作与协作 | 读取 Markdown | 可离线使用，无需 Python、Origin、Word 或 MCP |
| 查看案例图与表格预览 | 图片查看工具 | 包内 PNG 是合成教学示例，不是读者研究结果 |
| 包检查与 CSV 预检 | 兼容的 Python 3.11+，标准库 | 本轮纯检查在 Windows + Python 3.13.2 通过，其他环境实际核验 |
| 原生 Origin 图及 OPJU | Windows x64、已安装 Origin/OriginPro、匹配的 Python 与运行依赖 | 已有历史实测为 Python 3.12 + Origin 2026，不能推广为其他系统实测 |
| 重新生成表格示例 | 兼容 Python 和 python-docx | 不需 Word COM，生成后另验实际显示 |
| Word、MathType、LaTeX 等 | 当前主机相应工具、字体或服务 | 按任务选择，复制技能不会安装这些软件 |

macOS/Linux 可使用文本、示例与兼容的数据预检，不能把输出图片冒充原生 Origin 工程。跨机器字体、Office、Origin 构建与打印驱动可能影响页面，输出需实际回开。不同 agent 的执行一致性也需内容检查，格式或脚本通过不证明所有写作判断一致。

## 首次检查

具备合适 Python 时，在 PowerShell 按顺序执行。输入复制后的真实技能目录，以及已确认的 Python 3.11+ 可执行文件路径或命令名，不使用原作者路径：

```powershell
$skillDirectory = Read-Host '输入此技能目录的完整路径'
Set-Location -LiteralPath $skillDirectory
$checkPython = Read-Host '输入已确认的 Python 3.11+ 可执行文件路径或命令名'
& $checkPython --version
& $checkPython -B -X utf8 .\scripts\check_package.py
$demoOutput = Join-Path ([System.IO.Path]::GetTempPath()) ('waterfall-demo-' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
& $checkPython -B -X utf8 .\scripts\render_waterfall.py --manifest .\examples\waterfall\manifest.json --output-dir $demoOutput --check-only
```

macOS/Linux 在终端进入复制后的技能目录，确认 python3 版本适用，再执行：

```bash
python3 --version
python3 -B scripts/check_package.py
python3 -B scripts/render_waterfall.py --manifest examples/waterfall/manifest.json --output-dir /tmp/waterfall-demo --check-only
```

这些是一次性只读检查，不启动网页、Origin 或后台服务，完成即退出。没有 Python 时仍可阅读核心规则，不能将未执行的包检查报为通过。诊断只共享相对资源名、能力和错误类型，本机绝对路径留在当地记录。

## 模板与示例的使用

按当前任务复制所需模板，不要求创建整套项目。工作区组织及阶段方法集中见 [项目组织](workspace-architecture.md)，写作与图表规则由根入口选择，不在此重列整个流程。

| 包内资源 | 用途 |
|---|---|
| assets/templates/ | 规划、证据映射、图表、排版和交接底稿 |
| examples/sample-results.csv、[完整算例](../examples/worked-example.md) | 虚构数据的聚合、图表设计、文字与预期值 |
| examples/waterfall/、assets/waterfall/ | 八条合成轨迹、源哈希与 Origin PNG 示例 |
| [两级表头 DOCX](../assets/templates/two-level-three-line-table.docx) 及 [PNG](../assets/templates/two-level-three-line-table.png) | 可编辑分组表头与原生公式示例，数值虚构 |
| scripts/ 与 embedded/editaplot/runtime/ | 复现入口、源码、模板与依赖清单，不含应用安装包或虚拟环境 |

模拟材料只验证所列逻辑、数值和显示，不能直接作为真实研究数据。其他内嵌素材的用途与边界见 [内嵌技能清单](embedded-skills.md)，复制前按许可判断，第三方图像和数字不能改称自己的研究结果。

## Windows 原生制图

需要 Origin 时，先确认已安装的软件、x64 环境和当前运行依赖。下列步骤沿用历史验证的 Python 3.12 环境方案，不把它作为纯写作或包检查的强制版本。已有兼容隔离环境则直接复用，不重复安装或修改全局 Python。

先完成上文目录选择，在同一 PowerShell 中执行。安装步骤需网络取得依赖，未安装 Python 3.12 或 Origin 时先处理对应能力缺口：

```powershell
py -3.12 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r .\embedded\editaplot\runtime\requirements-runtime.txt -c .\embedded\editaplot\runtime\requirements-runtime.lock
& .\.venv\Scripts\python.exe -B .\embedded\editaplot\scripts\editaplot.py doctor
& .\.venv\Scripts\python.exe -B -X utf8 .\scripts\render_waterfall.py --manifest .\examples\waterfall\manifest.json --output-dir $demoOutput
```

脚本创建并正常关闭独立 Origin 实例，不接管用户工程。观察阶段输出，失败时保留诊断，不强杀无关进程。输出目录已存在时选择新位置，不删除旧结果。安装成功或 doctor 通过不等于原生工程、页面与图面均已验收，具体契约及回开方法见 [透视瀑布图](origin-perspective-waterfall.md#复现脚本与运行)。

## 接入自己的数据与迁移核验

将清单和 CSV 复制到当前使用者的数据位置，修改文件、列、单位、标签与划分。CSV 路径相对 manifest 解析，源内容改变后重新登记哈希，不忽略哈希冲突。不沿用旧项目训练划分或行数，真实数据不进入共享技能包。

迁移或改名后从新位置运行适用检查，记录输入哈希、参数、软件和实际输出。原生工程、MathType、引文域与页面效果在目标主机单独测试。缺少能力时完成可执行部分，明确未交付的格式或验证，不能由文件存在推断运行成功。

[历史匿名验证记录](validation.json) 反映记录时的环境和包版本，不是当前版本的全部验收。历史曾在中文及空格路径、其他工作目录下验证 Origin 回开和标签，并检查一页 Word 表格，不推广为全部软件或所有长表实测。当前更新只报告本轮真正执行的项目。

## 分享与第三方许可

共享前核对隐私、真实研究材料、私人配置、路径、会话与内部代号，运行包检查并人工检查其未覆盖的内容。第三方署名、商标、许可证与来源不做匿名篡改，技术可迁移不等于可以公开再分发。

- EditaPlot 为 Apache-2.0，保留 LICENSE、NOTICE 和来源记录。humanizer-zh 与 lieflat-less-ai-tone 为 MIT，保留各自许可和署名。后者缺失的宣传图片在本包用文字链接替代。
- docx 历史快照存在第三方分发限制，nature-figure 素材存在非商业及其他许可边界，尚未核清授权的资源也不能据本技能声明可公开分发。核心参考方法不依赖这些历史快照。
- 软件安装包、Python wheels、用户虚拟环境和私人配置不随本包提供。外部依赖适用自己的许可证，复制技能不会转移 Origin 或 Office 许可。
- 实际发布或上传遵守用户授权，不由技能自动触发。向第三方分享整个目录前，按目标核实或排除受限资源，不以包检查通过替代许可判断。
