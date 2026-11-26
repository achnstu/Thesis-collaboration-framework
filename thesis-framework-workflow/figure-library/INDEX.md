# 用户自定义图例库

这里保存当前用户确认、复刻和逐步积累的科研图型。“图例库”在此表示可复用的图型与作图配方集合，不仅是图内的 legend。每种图型独立成夹，包含预览、可运行的数据清单、示例数据、登记信息及复用入口。用户可以继续收录 Origin、Python、R 或其他工具的图型。

## 已收录图型

| 图型 | 预览 | 文件夹与复用入口 | 当前验证范围 |
|---|---|---|---|
| 多轨迹透视瀑布图 | [查看](perspective-waterfall/preview.png) | [perspective-waterfall](perspective-waterfall/guide.md)，[数据清单](perspective-waterfall/data/manifest.json) | 原生 Origin 二维投影、八条合成轨迹，已有保存回开与视觉记录 |
| 下柱上折线双 Y 轴组合图 | [查看](bar-line-dual-axis/preview.png) | [bar-line-dual-axis](bar-line-dual-axis/guide.md)，[数据清单](bar-line-dual-axis/data/manifest.json) | 原生 Origin 双图层、三柱三线，已有迁移目录与回开检查 |

图型的详细方法仍由包内共享 `scripts/` 与 `references/` 维护，文件夹通过相对链接复用，避免维护两套同名实现。迁移时复制整个技能包。现有 `examples/` 和 `assets/` 入口保留兼容，图例库文件夹中的副本用于集中浏览和独立的数据配置。

这两项是用户定制的图型配方，随包示例均为 synthetic。作者原始试作的截图近似数据不转成真实实验数据，也不作为共享默认数据。原生三维瀑布模板的有限能力测试仍见[瀑布图说明](../references/origin-perspective-waterfall.md#origin-原生三维瀑布模板)，不与二维投影图型混称。

## 如何继续保存复刻图型

用户确认一次复刻或新设计后，可将选定的脚本、配置、示例数据和预览保存到 `figure-library/<自选id>/`。登记 `entry.json` 应说明图型名、工具、数据性质、来源/许可、用户确认范围及实际验收范围。只保存本次必要材料，不自动收录整份研究数据、模型、凭据或无关文件。

工具提供 [register_figure_example.py](../scripts/register_figure_example.py)，按[登记模板](registration-spec.example.json)逐文件复制资源、核对哈希并生成条目。`source` 相对登记清单解析，也可由当前用户明确选择绝对源文件。`target` 必须在新图型文件夹内。已有条目不自动覆盖，更新由用户授权后定点修改。脚本列出的 `entry.json` 是实际登记真值，下面命令会显示以后新增的所有条目。

在 **PowerShell** 中按顺序运行。先进入复制后的技能目录，选择 Python 3.11+，再填入已准备好的登记 JSON 路径：

```powershell
$skillDirectory = Read-Host '输入此技能目录的完整路径'
Set-Location -LiteralPath $skillDirectory
$libraryPython = Read-Host '输入 Python 可执行文件路径或命令名'
& $libraryPython -B -X utf8 .\scripts\register_figure_example.py --list
$registration = Read-Host '输入本次图型登记 JSON 的完整路径'
& $libraryPython -B -X utf8 .\scripts\register_figure_example.py --spec $registration --check-only
& $libraryPython -B -X utf8 .\scripts\register_figure_example.py --spec $registration
```

这是一次性文件登记，不启动 Origin、绘图软件、网页或服务，无需后台停止操作。登记脚本不代表图型已绘图验收，程序、实际图面与作者确认分别记录。正式复用时用用户自己的已核验数据替换示例，并在本地项目保留绘图代码。

## 第三方绘图能力

第三方模板作为工具与方法来源，独立于用户自定义条目管理。Python/R 能力从 [内嵌绘图说明](../references/python-r-figures.md)进入。把某种外部模板实际适配成用户确认的图型后，才按上述流程登记，保留其来源与许可，不把第三方作品归为用户原创。
