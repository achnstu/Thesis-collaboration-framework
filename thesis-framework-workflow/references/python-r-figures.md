# 内嵌 Python / R 科研绘图能力

本模块从用户提供的 nature-skills 压缩包中，更新原有 `embedded/nature-figure/`，不另外安装全局技能。包含上游 nature-figure 2.8.0 的 Python 绘图及审查脚本、R 工作流与对齐辅助脚本、按需参考和必要的共享文档。来源与逐文件哈希见 [PROVENANCE.json](../embedded/nature-figure/PROVENANCE.json)，仓库自有内容保留 [LICENSE](../embedded/nature-figure/LICENSE)与[NOTICE](../embedded/nature-figure/NOTICE)。

上游来源和本包适配分别记录。主要文件按原字节内嵌，入口新增了论文工作流说明。实际试运行发现的兼容差异已局部修正：ROC 的梯形积分在 NumPy 1.x 使用等价的 `np.trapz`，火山图下标使用 MathText 并将轴题设为 8 pt，避免 Arial 缺字及下标小于 5 pt，SVG 检查脚本补入旋转计算所需的 `math` 导入。五类图型与 AUC 定义保持原包含义。新增的图例库管理器、依赖探测和 R 合成示例由本包提供，不冒称压缩包原有文件。

这是通用绘图工具区。用户确认、复刻和积累的具体配方保存到 [用户自定义图例库](../figure-library/INDEX.md)。第三方工具被内嵌，不等于其示例成为用户原创，也不把图库中的 Origin 图自动改成 Python/R。

## 按当前任务选择后端

先沿用用户指定语言、已提供的 `.py/.R` 或同一任务已确定的工具。仅当 Python/R 选择实际影响下一步、现有上下文无法确定时，询问一次。用户要求“内嵌两种能力”属于包维护，不要求选择一种。已有 Origin 授权也不因本模块重复询问语言。

Python 入口：[nature-figure/SKILL.md](../embedded/nature-figure/SKILL.md)与[Python 片段](../embedded/nature-figure/static/fragments/backend/python.md)。R 入口：[R 片段](../embedded/nature-figure/static/fragments/backend/r.md)与[R 工作流](../embedded/nature-figure/references/r-workflow.md)。只加载当前语言和相关图型的材料，作者的数据定义、字体与视觉编码优先于外部模板默认值。

一种语言缺少运行时，不用另一种语言的图片冒充已完成。可以继续准备对应脚本和数据映射，并说明实际缺项。读取文件、哈希、PDF 内容检查及不重画科研图的几何审查可独立进行。

## 已内嵌的能力

| 路线 | 随包资源 | 使用边界 |
|---|---|---|
| Python CSV 模板 | [plot_templates.py](../embedded/nature-figure/scripts/plot_templates.py) | 可直接运行 volcano、ROC、dotplot、marginal、paired 五类。需要真实 CSV，`--demo` 仅用于明确的合成测试，不生成统计显著性结论 |
| Python 自定义科研图 | [API 与样式](../embedded/nature-figure/references/api.md)、[图型参考](../embedded/nature-figure/references/chart-types.md)、[常用布局](../embedded/nature-figure/references/common-patterns.md) | matplotlib/seaborn 的柱、线、散点、热力图、分布及多面板等配方，根据实际数据写脚本，并非每种图型都有现成 CLI |
| R 科研图 | [R 工作流](../embedded/nature-figure/references/r-workflow.md)、[R 合成例子](../examples/nature-r/render_example.R) | ggplot2/patchwork 的图型与组图方法，ComplexHeatmap 等按任务载入。压缩包未携带其文档提到的私人 R 模板集合，不宣称已取得那些文件 |
| 多面板对齐 | [Python/JSON 审查器](../embedded/nature-figure/scripts/audit_panel_alignment.py)、[R 测量脚本](../embedded/nature-figure/scripts/panel_alignment.R) | 在最终物理图幅测量绘图区，比较共享边界、宽高和间距。R 图用 R 测量，Python 只检查 JSON，不代画 R 图 |
| 交付前检查 | [源码预检](../embedded/nature-figure/scripts/validate_figure.py)、[PDF 字号](../embedded/nature-figure/scripts/audit_pdf_text.py)、[PDF 碰撞](../embedded/nature-figure/scripts/audit_figure_collisions.py) | 各检查需要相应输入及依赖。自动通过不替代实际看图，缺少 PyMuPDF 时不能声称完成碰撞审查 |

原始列、统计层级和缺测处理以当前数据契约为准。模板中的 AUC、阈值、排序、密度或其他计算需与任务一致，不能将示例默认当成作者已批准的分析。已有准确数据不因使用工具而重算一套统计。

## 依赖检查与隔离环境

[check_figure_backends.py](../scripts/check_figure_backends.py)只探测 Python 包和 Rscript，不安装软件、不打开绘图设备、不写全局配置。Rscript 不在 PATH 时可用 `--rscript` 指定当前主机上的程序路径。

在 **PowerShell** 中按顺序执行：

```powershell
$skillDirectory = Read-Host '输入此技能目录的完整路径'
Set-Location -LiteralPath $skillDirectory
$figurePython = Read-Host '输入用于绘图的 Python 可执行文件路径或命令名'
& $figurePython -B -X utf8 .\scripts\check_figure_backends.py --backend all
```

Python CSV 模板需要 NumPy 和 Matplotlib，seaborn 用于相关自定义配方，PyMuPDF 用于 PDF 碰撞检查。没有兼容依赖时，复用已有隔离环境或在用户选定位置建立虚拟环境，再按需安装 [requirements-plotting.txt](../embedded/nature-figure/requirements-plotting.txt)。例如在当前技能目录使用独立 `.figure-venv`，不修改全局 Python：

```powershell
& $figurePython -m venv .figure-venv
& .\.figure-venv\Scripts\python.exe -m pip install -r .\embedded\nature-figure\requirements-plotting.txt
$figurePython = (Resolve-Path -LiteralPath '.\.figure-venv\Scripts\python.exe').Path
```

安装需要网络和当前用户的环境更改授权，包内操作不会自动执行上述命令。已有环境满足需求时不重复安装。

R 示例需要 Rscript、ggplot2、patchwork、jsonlite、svglite、ragg 和可用的 Cairo PDF 设备。ComplexHeatmap/circlize 等仅在对应任务使用，不作为普通曲线的必装项。R、Python 应用、虚拟环境和软件包二进制不随 skill 分发，目标主机按实际能力准备。

## 运行 Python CSV 模板

先完成上面的 PowerShell 目录与 Python 选择，继续执行。示例用新目录与显式 `--demo`，只生成虚构的配对数据图：

```powershell
$pythonOutput = Join-Path ([System.IO.Path]::GetTempPath()) ('nature-python-' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
New-Item -ItemType Directory -Path $pythonOutput | Out-Null
& $figurePython -B -X utf8 .\embedded\nature-figure\scripts\plot_templates.py paired --demo --output (Join-Path $pythonOutput 'paired-demo')
& $figurePython -B -X utf8 .\embedded\nature-figure\scripts\audit_pdf_text.py (Join-Path $pythonOutput 'paired-demo.pdf')
```

正式数据用 `--input <CSV>` 替换 `--demo`，先查[模板字段](../embedded/nature-figure/references/template-catalog.md)和该子命令 `--help`。模板输出 SVG、PDF、600 dpi TIFF 和 QA JSON，不默认输出 PNG。用户更改后的源码、数据绑定与最终图面分别检查。

## 运行 R 示例

在同一 PowerShell 中先确认 `Rscript` 及上述 R 包可用，再运行以下命令。当前示例基于本文件位置定位内嵌模块和合成 CSV，不依赖下载文件夹或原作者工程：

```powershell
$rExecutable = Read-Host '输入 Rscript 可执行文件路径或命令名'
$rOutput = Join-Path ([System.IO.Path]::GetTempPath()) ('nature-r-' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
& $figurePython -B -X utf8 .\scripts\check_figure_backends.py --backend r --rscript $rExecutable
$env:NATURE_QA_PYTHON = $figurePython
& $rExecutable --vanilla .\examples\nature-r\render_example.R $rOutput
```

R 示例输出 SVG、PDF、600 dpi TIFF、PNG 及对齐记录，科研图全部由 R 生成。Python 只执行对齐 JSON 审查。`panel_alignment.R` 上游默认的 `skills/nature-figure/...` 审查脚本路径需要显式替换，随包示例已传入本包相对解析出的路径。用户编写其他 R 脚本时沿用这一做法。

以上命令均为一次性运行，不启动网页或常驻服务。正常完成即退出，运行窗口需要取消时按 Ctrl+C，不停止无关进程。本轮主机未发现 Rscript，因此 R 示例尚未执行，目标主机应先运行包探测、R 示例和实际图面检查，不能仅凭内嵌源码宣称 R 渲染通过。

macOS/Linux 可按相同结构使用 Python 和 Rscript，路径从当前技能目录解析，字体与导出设备需在目标主机验证。Origin 库条目仍受 Windows/Origin 能力边界限制。

## 来源、许可与共享

新引入的绘图脚本和参考取自用户所供压缩包，归档哈希和上游版本留在模块内。Nature 品牌和示例风格不构成期刊认可，实际投稿要求按目标刊物核实。

原有 `figures4papers` 素材未随此次更新增加新脚本或图片，补入了上游[第三方说明](../embedded/nature-figure/assets/figures4papers/THIRD_PARTY_NOTICES.md)。上游没有明确授予这些素材的复制、修改或发表权时，应参考其视觉结构，以原创代码和用户数据实现，不能据主仓库 Apache-2.0 推定素材已获授权。共享整个技能包前仍按[分发规则](portability.md#分享与第三方许可)检查既有受限素材。

压缩包内含可选外部图像 API 路线，其存在不触发调用授权。当前任务仅集成离线 Python/R 绘图与检查，不配置密钥、不上传数据、不修改全局偏好。

本次集成的检查范围集中记录于[验证记录](figure-library-integration-validation.json)。原包文件、兼容性修改、本包新增资源和实际执行结果分别登记，不将“已嵌入”“静态通过”“实际渲染通过”混为一项。
