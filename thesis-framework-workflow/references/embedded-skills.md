# 内嵌技能清单与使用边界

快照按原目录完整复制至 `embedded/`，供迁移后按需读取。源技能保留其作者、许可证与原文，不修改其内部引用。入口工作流及当前项目/用户要求优先于历史快照中的路径、过时样式和额外流程。内嵌技能不必全部执行，也不因使用主技能要求创建其全部中间产物。

| 任务 | 内嵌入口 | 用途 |
|---|---|---|
| 全文研究、结构、证据、章节与审计 | `embedded/paper-spine/SKILL.md` 及 `embedded/paper-spine-*` | 按需借鉴研究、build、rewrite、citation、audit、LaTeX 与 translation 子流程。原入口按已安装独立技能路由，在本包改为直接打开相邻同名目录。主流程不调用以降低 AI 检测率为目标的 `paper-spine-humanize`，中文表达使用下行技能及本包写作规则。 |
| 中文润色 | `embedded/humanizer-zh/SKILL.md` | 保留事实、语气和限定，处理空话与重复。 |
| 文献检索和核验 | `embedded/nature-academic-search/SKILL.md` | 适用于确需检索时核对元数据及原文支持。 |
| 数据图设计 | `embedded/nature-figure/SKILL.md` | 选择统计图型和验收，按目标模板确定风格。 |
| Origin 数据图与模板 | `embedded/editaplot/SKILL.md` | 读取其科学语义、Origin 安全与回开验证规则。选用内置模板时遵循该模板的实际语义确认和能力门禁。 |
| 本项目 Origin | `embedded/markov-thesis-origin-figures/SKILL.md` | 本机与项目专用实例，路径和旧字体必须核对。 |
| Origin 桥接 | `embedded/origin-mcp-local/SKILL.md` | 按现有安装探测服务，失败需如实报告。 |
| Word 原生公式 | `embedded/md-bare-var-to-native-equation/SKILL.md` | 规范数学表达与 OMML 检查。 |
| DOCX 操作 | `embedded/docx/SKILL.md`、`embedded/officecli/SKILL.md` | 选择当前环境可用工具，保护对象并检查页面。 |

PaperSpine 配置 UI、网络检索、LaTeX、Word、Origin、MathType、Pandoc 及 MCP 服务属于外部运行依赖，复制技能不会一并安装或保证可用。其脚本可能包含原机器路径或依赖同级已安装技能，先检查并适配，禁止盲目运行。优先使用文档中可迁移原则，再根据本机实际工具执行。不存在本机软件时继续完成可执行部分，并明确缺口。

EditaPlot 快照来自本机 `editaplot-main/skill/editaplot`，含技能文档、参考、脚本、素材和许可证，不含完整仓库、运行引擎、虚拟环境或 Origin。其运行时和 launcher 需要完整仓库及本机环境，读取 `embedded/editaplot/references/runtime.md` 核验后使用。原 `origin-mcp-local` 和项目 Origin 技能中指向全局 EditaPlot 的旧路径失效时，先阅读本包的 EditaPlot 入口和参考文件，再独立定位已安装运行时，不能把快照当成已安装运行引擎。项目专用绘图脚本和 EditaPlot 通用模板是不同路线，分别按其适用规则核验，用户确认的论文统计与格式优先。
