# 内嵌技能清单与使用边界

工具资料与适配入口保存在 `embedded/`，供迁移后按需读取。保留第三方作者与许可证，项目专用入口已匿名化。核心方法由根工作流和 references 自包含说明，不以全局安装同名技能为前提。当前项目与用户要求优先于历史样式和额外流程，内嵌工具不必全部执行。

| 任务 | 内嵌入口 | 用途 |
|---|---|---|
| 全文研究、结构、证据、章节与审计 | `embedded/paper-spine/SKILL.md` 及 `embedded/paper-spine-*` | 按需借鉴研究、build、rewrite、citation、audit、LaTeX 与 translation 子流程。原入口按已安装独立技能路由，在本包改为直接打开相邻同名目录。主流程不调用以降低 AI 检测率为目标的 `paper-spine-humanize`，中文表达使用下行技能及本包写作规则。 |
| 中文润色 | `embedded/humanizer-zh/SKILL.md` | 保留事实、语气和限定，处理空话与重复。 |
| 文献检索和核验 | `embedded/nature-academic-search/SKILL.md` | 适用于确需检索时核对元数据及原文支持。 |
| 数据图设计 | `embedded/nature-figure/SKILL.md` | 选择统计图型和验收，按目标模板确定风格。 |
| Origin 数据图与模板 | `embedded/editaplot/SKILL.md` | 运行源码和模板随包提供。读取科学语义、安全与回开规则。自定义透视瀑布图从根 scripts 的 manifest 入口调用同一后端，见下文集成说明。选用 catalog 模板时保留其语义门禁。 |
| 当前使用者的项目 Origin | `embedded/project-origin-figures/SKILL.md` | 匿名适配原则，不含原作者工程路径或预设图号，输入由当前使用者提供。 |
| Origin 桥接 | `embedded/origin-mcp-local/SKILL.md` | 按现有安装探测服务，失败需如实报告。 |
| Word 原生公式 | `embedded/md-bare-var-to-native-equation/SKILL.md` | 规范数学表达与 OMML 检查。 |
| DOCX 操作 | `embedded/docx/SKILL.md`、`embedded/officecli/SKILL.md` | 选择当前环境可用工具，保护对象并检查页面。 |

论文写作先使用本包 [写作原则](writing.md) 与 [改写示例](writing-examples.md)，再按需求读取内嵌润色、rewrite 或 audit，避免将工程交付记录写成论文。DOCX 操作按 [工具选择](word-tooling.md) 路由，三线表由 [学术表格](academic-tables.md) 的目标样式控制，不套用其他工具的默认网格或底色。OfficeCLI 已内嵌不等于本次实际执行，必须按命令和结果记录。

PaperSpine 配置 UI、网络检索、LaTeX、Word、Origin、MathType、Pandoc 及 MCP 服务属于外部运行依赖，复制技能不会一并安装或保证可用。其脚本可能包含原机器路径或依赖同级已安装技能，先检查并适配，禁止盲目运行。优先使用文档中可迁移原则，再根据本机实际工具执行。不存在本机软件时继续完成可执行部分，并明确缺口。

EditaPlot 的文档、CLI、runtime/src、runtime/templates、依赖清单和 Apache-2.0 LICENSE/NOTICE 均位于本包 `embedded/editaplot/`，不含虚拟环境、Origin 应用或私人配置。路径从当前文件相对解析，不需要作者电脑上的另一份仓库。参见 [瀑布图集成](../embedded/editaplot/references/thesis-waterfall-integration.md) 与 [首次使用和环境兼容](portability.md)。通用 CLI 与自定义瀑布图分别按自己的能力与验收范围运行，作者确认的科学口径及图级样式优先。旧工具文档中的 setup 安装全局技能不是使用本包的必需步骤。
