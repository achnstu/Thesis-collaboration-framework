# 原生 Origin 工作流

本适配器不包含任何作者工程的默认路径或原始数据。直接按本包 [独立使用](../../../references/portability.md) 运行示例，按 [CSV 清单契约](../../../references/origin-perspective-waterfall.md#复现脚本与运行) 接入当前用户提供的数据。

原生绘图使用相邻 EditaPlot 的隔离会话、显式图幅、原生曲线及文本、源哈希和回开验证。不能仅因安装了同版本 Origin 就声称支持所有图型。没有 Origin 的电脑仍可读取规则、查看包内 PNG 与运行只读预检，OPJU 的生成和回开保持未执行。

若需要执行已有项目脚本，可使用 scripts/draw_figure.ps1，显式提供 Python 与脚本路径。CheckOnly 仅检查语法，不能代替实际源数据和图形验收。
