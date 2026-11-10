# 与论文工作流的透视瀑布图联动

本包已将 EditaPlot 的 runtime/src 和 runtime/templates 随技能保存，CLI 的源码发现逻辑可从 scripts 向父目录定位 runtime，不需要原电脑的安装位置。依赖通过本机隔离 Python 环境取得，不携带虚拟环境或私人 runtime pointer。

论文制图从 [核心作图规则](../../../references/figures.md) 确定科学问题和数据列，再按 [透视瀑布图](../../../references/origin-perspective-waterfall.md) 选用显示投影。实际执行调用 [manifest 渲染入口](../../../scripts/render_waterfall.py)，复用包内 OriginSession、require_interactive_origin_context、origin_job_slot 和回开属性读数。此入口是独立验证的自定义图型，没有冒充 EditaPlot 通用模板 catalog 中的已注册模板。

共享：源哈希和只读输入、隔离实例、会话所有权与正常退出、Origin 部分串行、显式物理图幅、原生对象和保存后回开。论文图级要求覆盖通用字号、输出格式和默认配色，其他模板的统计语义与专用门禁仍按其文档执行。

另提供 [Origin 原生三维瀑布模板](../../../references/origin-perspective-waterfall.md#origin-原生三维瀑布模板) 的隔离合成测试入口，调用 `glWater3D` 并回开核对 OpenGL 三维图层。它与上述二维投影路线并存，当前验证仅覆盖三条共用 X 的合成数据及 Origin 2026，不自动继承另一方案的颜色、透明度和排版。

完整自包含示例见 [示例清单](../../../examples/waterfall/manifest.json) 与 [PNG 图面](../../../assets/waterfall/perspective-example.png)。不需要原作者的数据、OPJU 或历史对话。环境准备与未实测平台范围见 [兼容说明](../../../references/portability.md)。
