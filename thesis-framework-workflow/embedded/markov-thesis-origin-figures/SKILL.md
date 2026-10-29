---
name: markov-thesis-origin-figures
description: 为本机 Markov-DRL 中文硕士论文调用 Origin 2026 绘制原生可编辑科研数据图，统一统计口径、子图编号和中西文字体，交付 OPJU、600 dpi PNG、EMF。用于该论文的 Origin 出图、回改和验收，含已验证的第2章快速入口。
---

# 我们的硕士论文 Origin 作图

触发词: "按我们的 Origin skill 作图", "大论文 Origin 作图", "Origin 版 C2", "硕士论文 Origin 出图"

论文根目录：`C:/Users/zwzhu/Desktop/萝卜论文/markov_drl/大论文`。
本机 Origin 2026（10.30）、CPython 3.12.14，2026-10-25 已实际完成第2章三张数据图。

## 先确定科学口径

读取论文根目录的 `AGENTS.md`、`写作管理/中文图表规划.md` 当前定位号，以及 `写作管理/绘图错误总结与大论文作图规则.md`。
遵循项目写作检查技能的当前图表相关项。已有定位号和作者确认的单位、分组、统计定义直接沿用。只有缺失信息会改变科学含义时才询问，不要求重复批准已明确的口径。

只读绘图 CSV 或登记工作簿。明确绘制列、只保留列、单位换算、缺测和统计层级。不得静默插值、补零、平滑、拟合、删异常或重算另一种加权统计。未知列不自动变成曲线。

## 快速执行已有第2章图

使用 [scripts/draw_chapter2.ps1](scripts/draw_chapter2.ps1)，只运行用户指定的一张图。先用 `-CheckOnly` 核对输入与脚本，再按请求实际绘制。它调用正式章目录中的原生 Origin 脚本，代码与图同存，便于回改。

- C2-D01：训练 Voyage 001–008，4×2，每航程真实时间。
- C2-D02：测试 Voyage 009–012，2×2，每航程真实时间。
- C2-D03：航程等权的持续曲线和绝对增量 ECDF，1×2。

命令、运行环境及新图适配方法见 [references/origin-workflow.md](references/origin-workflow.md)。D03 或其他经验分布必须另读 [references/chapter2-semantics.md](references/chapter2-semantics.md)。

请求重绘某图即授权更新该定位号的 Origin 输出。已验收的其他图、MATLAB 版和源数据保持原样。新图保存在 `图表文件夹/01_Origin作图/对应章节`，脚本使用 `C2_D03.py` 这类名称，输出使用 `C2-D03` 这类定位号。

## 论文版式

- 原生 Origin 工作簿、曲线、轴和文本，不能用嵌入位图冒充可编辑图。
- 中文宋体，英文和数字 Times New Roman。正文标签约 9 pt，刻度 8 pt。Origin 富文本用 `\f:宋体(负载) \f:Times New Roman((kW))`。MATLAB 的 `\fontname{SimSun}` 不能搬进 Origin。
- 多面板按行写 `(a)、(b)…`，每面板都有完整轴名、单位和内容子标题。图内不加整图总标题。单面板不加编号。
- 主曲线约 0.7 pt，轴线 0.6 pt，浅灰网格。页面宽度通常 16.5 cm，高度随面板调整，不能靠缩小文字挤版。
- 可比较的负载时序纵轴统一从 0 起，每 1 kW。横轴精确止于各航程末个有效时间，刻度单独取整。分布图保留长尾，概率轴分别用 0–1 或 0–100%。
- 模型视觉编码读取现行规则及 `03_MATLAB作图/公共函数/thesis_plot_style.m`。训练 `#0072B2` 实线，测试 `#D55E00` 虚线，两面板一致。
- 正式交付只用同名 OPJU、600 dpi PNG、EMF。通用 EditaPlot 的 Arial、PDF/TIF 及默认输出目录不替代作者的论文规范。

## 验收后再报告完成

实际运行并记录 Origin 环境。回开保存的 OPJU，逐点核对工作簿、曲线绑定、轴范围、文本、颜色线型、字号线宽及物理图幅。源文件 SHA-256 前后一致，PNG 元数据约 600 dpi，三种文件非空。

打开 PNG 逐面板看中文、编号、完整轴名、图例、裁切与长尾，记录 `visual_qa.status`。尤其检查旋转中文的实际墨迹，Origin 文本框坐标在页内不保证字形未切边。图面检查未完成时明确写待验收。

保存 `定位号_verify.json` 和运行日志，更新对应图表规划及章 README。最终回复简短，给工程、预览和必要限制。Origin 2026 的成功证据仅覆盖已执行路线，不声称所有模板均已验证。
