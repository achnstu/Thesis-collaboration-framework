# Thesis Collaboration Framework

面向学位论文和期刊返修的通用论文协作技能。它以研究问题和可追溯证据为主线，连接论文框架、写作、文献、图表、Word 排版、补充材料与审稿回复，既支持完整论文项目，也支持单独的写作或修订任务。

**当前版本：2026-11-15 更新版。** 核心技能以提交 [`1831af4`](https://github.com/achnstu/Thesis-collaboration-framework/commit/1831af4) 为基准，尚未设立正式版本号或发行标签。

## 当前版本包含什么

- **论文主线与协作**：把研究问题、章节职责、论点和证据对应起来，按需使用任务卡、共享记录与交接材料。单人或单对话也可使用，无须强制建立多代理流程。
- **具体写作方法**：说明摘要、结论、数据结果和公式释义如何组织，提供连贯的中英文虚构示例及公开论文的写法分析。示例只用于学习，不能当作真实研究结果。见 [写作与证据](thesis-framework-workflow/references/writing.md)、[写作示例](thesis-framework-workflow/references/writing-examples.md)。
- **语言与作者风格**：以作者认可的现稿为基准。中文按需结合内嵌 humanizer-zh 和 lieflat-less-ai-tone，PaperSpine 按实际任务选用。英文长句和语态依语境调整，被动语态不是中文写作要求。
- **公式与结果核对**：同一变量沿用同一完整符号，同一完整符号对应一个含义。区分瞬时量、均值和估计量，并核对上下标、单位及相关文件。结果描述保留比较条件、关键数值和指标取舍，不把代理指标直接写成寿命结论。
- **返修与文档保护**：以作者当前成稿为依据，按授权范围协调正文、补充材料和回复信，保护 Word 中的公式对象、引用域和人工修改。附可编辑表格模板及工具选择说明。
- **图表与跨环境使用**：先核对数据口径和图表要回答的问题，再选择图型。包内含合成数据、透视瀑布图示例和自动化源码，按实际能力验证，不假定每台机器都已安装 Origin 或 Word。

## 如何使用

将 [thesis-framework-workflow](thesis-framework-workflow/) **整个目录**复制到所用 agent 的技能目录，或在对话中直接提供其中的 [SKILL.md](thesis-framework-workflow/SKILL.md) 路径，让 agent 根据任务读取相关参考文件。路径相对技能包解析，不依赖原作者的工程、用户名、盘符或历史对话。不同 agent 的发现方式和权限可能不同，按其实际能力使用。

例如，可以提出：“请使用论文框架技能，依据我提供的结果修改摘要，保留比较对象和数值，只给文字版。” 也可以要求核对公式符号，或组织某一章的论点与证据。实际稿件、数据和学校或期刊规范由使用者提供。

首次迁移及可选的包检查见 [兼容说明](thesis-framework-workflow/references/portability.md)。核心写作规则可离线阅读，原生绘图、文档编辑和特定脚本需要相应软件或依赖。模板、章数、图型及格式应按当前研究和作者要求调整。

## 来源与分发

感谢 [EditaPlot](https://github.com/hang-jin/editaplot)、[Humanizer-zh](https://github.com/op7418/Humanizer-zh)、[lieflat-less-ai-tone](thesis-framework-workflow/embedded/lieflat-less-ai-tone/README.md)、[PaperSpine](https://github.com/WUBING2023/PaperSpine) 及其他创作者。第三方来源和适用范围见 [SOURCES.md](SOURCES.md) 和 [分发说明](thesis-framework-workflow/references/portability.md#分享与第三方许可)。

本项目的通用流程、模板与新增示例按仓库许可证分享。内嵌材料适用各自许可证，不能将根目录 Apache-2.0 推广至全部第三方内容。历史受限快照未因本次更新获得新增授权。复制技能不等于安装 Origin、Word 或运行环境。
