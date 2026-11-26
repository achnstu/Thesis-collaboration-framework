# 下柱上折线双 Y 轴组合图

[图面预览](preview.png) · [登记信息](entry.json) · [数据清单](data/manifest.json)

下部总量柱图读左轴，上部时序折线读右轴。两个原生 Origin 图层共享画框位置，各自绑定 X 数据。柱图类别的位置不代表折线中的时刻。随包三柱三线为合成数据，实际复用时重新确认物理量、单位及两套 X 域。

完整方法、可见右轴刻度及可选顶部时间轴见[组合图说明](../../references/origin-bar-line-dual-axis.md)。运行入口为 [render_bar_line_dual_axis.py](../../scripts/render_bar_line_dual_axis.py)，`--manifest` 选择本文件夹的 `data/manifest.json`，`--output-dir` 选择数据目录外的新目录。

该图型已固化右轴数值显示、默认轴题清理和保存后回开检查。配置改变后仍须查看实际图面，不把原示例验证当作新数据的排版验收。
