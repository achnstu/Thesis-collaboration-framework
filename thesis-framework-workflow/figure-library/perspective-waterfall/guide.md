# 多轨迹透视瀑布图

[图面预览](preview.png) · [登记信息](entry.json) · [数据清单](data/manifest.json)

该配方用原生 Origin 曲线、透明填充及参考平面组织多条轨迹。投影深度只是样本分层，真实时间和功率保留在工作簿，不能用页面高度直接比较不同航程幅值。随包八条轨迹为合成数据。

完整方法、显示变换、独立环境和验收见[图型说明](../../references/origin-perspective-waterfall.md)。运行入口为 [render_waterfall.py](../../scripts/render_waterfall.py)，`--manifest` 选择本文件夹的 `data/manifest.json`，`--output-dir` 选择数据目录外的新目录。

在技能根目录运行前，按[迁移说明](../../references/portability.md)准备 Python 和 Origin。原生三维 `glWater3D` 是另一条能力测试路线，不把二维投影工程描述成可旋转三维图。
