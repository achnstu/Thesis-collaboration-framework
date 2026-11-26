# 来源与致谢

感谢各项目作者和贡献者分享学术写作、文献检索、图形制作及文档处理方法。下表说明本仓库内嵌材料的已知来源，不能根据目录名称推断版权或授权。

| 内嵌技能 | 来源及用途 | 许可或状态 |
|---|---|---|
| `editaplot` | [EditaPlot](https://github.com/hang-jin/editaplot)，可编辑 Origin 科研图 | Apache-2.0，见原目录 LICENSE 和 NOTICE。现已随包提供自动化 runtime/src、templates、依赖清单及来源记录，不含 Origin 或 Python 虚拟环境。 |
| `humanizer-zh` | 本机修订版，正文注明参考 [Humanizer](https://github.com/blader/humanizer)、[Humanizer-zh](https://github.com/op7418/Humanizer-zh) 和 [stop-slop](https://github.com/hardikpandya/stop-slop) | 本地快照含 MIT LICENSE，保留原作者声明。 |
| `paperspine-v6`（含 `paper-spine`、`paper-spine-study`、`paper-spine-followwriting`、`paper-spine-figures`、`paper-spine-review`、`paper-spine-deliver`） | [PaperSpine V6](https://github.com/WUBING2023/PaperSpine/releases/tag/v6.0.0-beta.2)，参考引导写作、研究、图表、审阅与交付方法 | 官方 6.0.0-beta.2 快照，保留 MIT LICENSE 及 `upstream.json`（来源、归档哈希与逐文件校验值）。主流程只取其写作与论证方法，不执行以降低 AI 检测率为目标的子技能。 |
| `nature-figure` 及必要的 `nature-shared` 参考 | [nature-skills](https://github.com/Yuan1z0825/nature-skills)，用户提供的归档中 nature-figure 2.8.0 的 Python/R 绘图、组图和检查方法 | 仓库自有内容保留原 Apache-2.0 [LICENSE](thesis-framework-workflow/embedded/nature-figure/LICENSE) 和 [NOTICE](thesis-framework-workflow/embedded/nature-figure/NOTICE)，归档与逐文件哈希、兼容性改动见 [PROVENANCE.json](thesis-framework-workflow/embedded/nature-figure/PROVENANCE.json)。原有 figures4papers 第三方素材权利单独处理，不能据主仓库许可推定可复制、修改或发表。 |
| `nature-academic-search` | 本地学术检索技能 | 上游来源与再分发授权尚未核实。配置 JSON 为本地路径占位示例，不包含在 Git 发布内容中。 |
| `officecli` | 本地 OfficeCLI 操作技能，正文介绍 [officecli.ai](https://officecli.ai/) | 本地快照的确切上游版本及再分发授权尚未核实。 |
| `docx` | Anthropic 文档技能，本地副本包含 LICENSE.txt | 原许可证注明禁止分发、转授权或转移，需核对适用协议及权利人的许可。 |
| `md-bare-var-to-native-equation` | 本地技能，作者注明集美大学罗强 | 本地包含 Apache-2.0 LICENSE，原文含第三方转换资源，其独立权利与分发条件尚需核实。 |
| `project-origin-figures`、`origin-mcp-local` | 本项目整理的匿名 Origin 绘图与桥接入口 | 当前使用者提供输入，不包含原作者工程路径。旧入口保留兼容转向。 |

仓库中的通用流程、协调模板和案例由本项目根据论文工作整理。感谢原工具、技能作者、论文作者及审阅者提供的方法与反馈。内嵌许可证和版权声明均保留在相应目录。

感谢 [nature-skills](https://github.com/Yuan1z0825/nature-skills) 的开放分享。本次引入的 45 个模块文件中，42 个保留归档原字节，另 3 个的集成说明和兼容性改动单独记录。用户自定义图例库、登记工具与 R 合成示例属于本包新增适配，不冒称上游原有文件。Python 展示图由内嵌模板的显式合成数据生成，R 尚未在本轮主机运行，不以方法文档代替执行证据。

本包教学数据、表格模板及新图型预览不含真实论文结果。既有 DOCX 与 figures4papers 历史素材未在此次图型更新中增加新原始文件，其原许可边界仍须分别核对。figures4papers 的具体权利说明见 [THIRD_PARTY_NOTICES.md](thesis-framework-workflow/embedded/nature-figure/assets/figures4papers/THIRD_PARTY_NOTICES.md)。
