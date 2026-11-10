---
name: project-origin-figures
description: 用当前项目的字段、划分和版式制作并验收原生可编辑 Origin 图。
---

# 项目 Origin 制图适配

触发词: “论文 Origin 作图”, “训练数据制图”, “Origin 回改”。

先读当前作者的图表计划与数据说明，明确真实列、单位、训练测试划分和统计层级。历史项目的图号、文件名与结论不作为输入。没有本项目原始文件时，直接使用包内 [合成数据示例](../../examples/waterfall/manifest.json) 学习或验证操作，不编造正式结果。

通用流程见 [作图与验收](../../references/figures.md)，瀑布图见 [制作方法](../../references/origin-perspective-waterfall.md)。原生软件控制统一走 [EditaPlot](../editaplot/SKILL.md) 的隔离实例、任务队列和回开核验，所需源码随包保留，不依赖外部同名技能。

作者明确要求的字号、字体、物理尺寸和输出格式优先。输入只读，显示辅助列只放工程副本，新候选目录避免覆盖手工修改。保存后回开逐点核对数据与绑定，查看实际 PNG，并分别记录程序检查、图面检查、作者确认和文档插图检查。
