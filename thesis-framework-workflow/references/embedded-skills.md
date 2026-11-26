# 内嵌技能清单与使用边界

工具资料与适配入口保存在 `embedded/`，供迁移后按需读取。保留第三方作者与许可证，项目专用入口已匿名化。核心方法由根工作流和 references 自包含说明，不以全局安装同名技能为前提。当前项目与用户要求优先于历史样式和额外流程，内嵌工具不必全部执行。

| 任务 | 内嵌入口 | 用途 |
|---|---|---|
| 中文润色 | `embedded/humanizer-zh/SKILL.md`、`embedded/lieflat-less-ai-tone/SKILL.md` | 中文写作经验的重要参考。保留作者声音、事实和限定，针对实际的空话、重复与生硬表达作最小修改。两者不是作者身份鉴定器，也不保证检测结果。 |
| 参考引导写作、研究、图表、审阅与交付 | `embedded/paperspine-v6/skills/paper-spine/SKILL.md` 及同级五个阶段技能 | V6 6.0.0-beta.2 官方快照。论证层级、互补参考及写作动作已融入 [写作模块](writing.md#参考引导写作与论证重构)，执行时直接读取 `paper-spine-followwriting` 和必要原方法。可复用 [任务提示词](../assets/templates/writing-prompts.md)，边界及网页连接见 [适配说明](paperspine-integration.md)。无需全局安装即可读取方法，保留 MIT 许可证与来源，不以检测分数为目标。 |
| 文献检索和核验 | `embedded/nature-academic-search/SKILL.md` | 适用于确需检索时核对元数据及原文支持。 |
| Python/R 科研绘图 | `embedded/nature-figure/SKILL.md` | 已内嵌用户所供 nature-figure 2.8.0 的脚本、静态后端片段与图表参考。Python 提供 CSV 模板和原生脚本，R 提供 ggplot2/patchwork/ComplexHeatmap 工作流与对齐脚本，见 [接入说明](python-r-figures.md)。不依赖全局 nature-skills，也不表示当前主机已安装 R 或全部软件包。 |
| Origin 数据图与模板 | `embedded/editaplot/SKILL.md` | 运行源码和模板随包提供。读取科学语义、安全与回开规则。自定义透视瀑布图从根 scripts 的 manifest 入口调用同一后端，见下文集成说明。选用 catalog 模板时保留其语义门禁。 |
| 当前使用者的项目 Origin | `embedded/project-origin-figures/SKILL.md` | 匿名适配原则，不含原作者工程路径或预设图号，输入由当前使用者提供。旧名 `embedded/markov-thesis-origin-figures/` 保留为兼容入口，只做转向，不承载项目内容。 |
| Origin 桥接 | `embedded/origin-mcp-local/SKILL.md` | 按现有安装探测服务，失败需如实报告。 |
| Word 原生公式 | `embedded/md-bare-var-to-native-equation/SKILL.md` | 规范数学表达与 OMML 检查。 |
| DOCX 操作 | `embedded/docx/SKILL.md`、`embedded/officecli/SKILL.md` | 选择当前环境可用工具，保护对象并检查页面。 |

论文写作先依据作者认可的现稿、当前任务和本包 [写作原则](writing.md) 与 [改写示例](writing-examples.md)。中文润色参考上述两种内嵌技能，英文沿用通用的保真与简洁原则，但不把中文特征规则当成英文规则。lieflat 原技能的白名单、结构保护和不处理外语等边界只适用于直接执行其中文清理任务，不限制用户另行授权的结构调整或英文修改。内嵌规则冲突时依次服从用户当前要求、项目约定和本包适配。PaperSpine 的主动动词、文献学习数量和多代理建议按当前文体与授权适配，不覆盖作者的自然被动语态等约定，也不扩大写回、实验或代理范围。只执行写作阶段时不声称运行了完整研究流程。

DOCX 操作按 [工具选择](word-tooling.md) 路由，三线表由 [学术表格](academic-tables.md) 的目标样式控制，不套用其他工具的默认网格或底色。OfficeCLI 已内嵌不等于本次实际执行，必须按命令和结果记录。

PaperSpine V6 内嵌的是方法与脚本快照，网页工作台及其 Windows Python 在宿主中独立安装，不随本包分发。网络检索、LaTeX、Word、Origin、MathType、Pandoc 及 MCP 同样按任务检查。网页通过 [管理器桥接脚本](../scripts/paperspine_workbench.py) 定位正式安装，不使用历史 3.x UI 或 main 频道更新脚本。缺少宿主运行时仍可离线执行 Followwriting 方法。

EditaPlot 的文档、CLI、runtime/src、runtime/templates、依赖清单和 Apache-2.0 LICENSE/NOTICE 均位于本包 `embedded/editaplot/`，不含虚拟环境、Origin 应用或私人配置。路径从当前文件相对解析，不需要作者电脑上的另一份仓库。参见 [瀑布图集成](../embedded/editaplot/references/thesis-waterfall-integration.md) 与 [首次使用和环境兼容](portability.md)。用户自定义配方集中在 [图例库](../figure-library/INDEX.md)。通用 CLI 与自定义图型分别按自己的能力与验收范围运行，作者确认的科学口径及图级样式优先。旧工具文档中的 setup 安装全局技能不是使用本包的必需步骤。

nature-figure 的仓库自有内容保留 [Apache-2.0 LICENSE](../embedded/nature-figure/LICENSE)、[NOTICE](../embedded/nature-figure/NOTICE)及[来源清单](../embedded/nature-figure/PROVENANCE.json)。`figures4papers` 的既有第三方素材仍受其[单独说明](../embedded/nature-figure/assets/figures4papers/THIRD_PARTY_NOTICES.md)约束，不能据仓库许可证推定可自由复制或发表。此次只更新绘图能力和必要的共享参考，不执行外部图像 API、不安装全局偏好或其他 nature 技能。
