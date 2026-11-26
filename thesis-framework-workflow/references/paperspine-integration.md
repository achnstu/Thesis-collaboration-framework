# PaperSpine V6 写作与工作台适配

本包接入 **6.0.0-beta.2**，来源为 [官方 V6 发布](https://github.com/WUBING2023/PaperSpine/releases/tag/v6.0.0-beta.2)。[来源记录](../embedded/paperspine-v6/upstream.json) 保存版本、发布序号和安装包 SHA-256，[MIT 许可证](../embedded/paperspine-v6/LICENSE) 随包保留。`embedded/paperspine-v6/skills/` 是未改写的官方六技能快照，本文件负责本地适配。旧 3.x `paper-spine-rewrite`、`paper-spine-audit`、`paper-spine-ui` 和 `paper-spine-update` 不再作为本框架入口，即使磁盘上仍存在历史目录。

## 各自负责什么

| 部分 | 职责 | 按需入口 |
|---|---|---|
| 论文框架 | 当前稿、证据边界、章节职责、作者约定、缩写、完整符号及一次文字复查 | [写作执行](writing-review.md)、[写作方法](writing.md) |
| 中文语言模块 | 清理实际的空话、重复和生硬表达，保留作者声音 | [humanizer-zh](../embedded/humanizer-zh/SKILL.md)、[lieflat](../embedded/lieflat-less-ai-tone/SKILL.md) |
| Followwriting | 学习真实参考的论证动作、段落组织和句子功能，形成独立稿件 | [Followwriting](../embedded/paperspine-v6/skills/paper-spine-followwriting/SKILL.md) |
| Web 工作台 | 配置、研究定位、图件选择、手稿预览、投稿周期与反馈的同任务状态 | 宿主 `paper-spine-web:paper-spine-web` 和官方 manager |

局部润色直接用框架与语言模块。参考引导的起草、实质改写、逐段对标或逐句对照，加载 Followwriting 及其链接的 [写作方法](../embedded/paperspine-v6/skills/paper-spine/references/reference-guided-writing.md) 和 [直接科研表达](../embedded/paperspine-v6/skills/paper-spine/references/assertive-scientific-writing.md)。需要图形界面或恢复已有 Web 论文时再接入工作台，不把安装、网页或配置作为文字工作的前提。

## 写作方法的现行入口

写作执行统一进入 [writing.md 的参考引导写作与论证重构](writing.md#参考引导写作与论证重构)，其中已吸收内嵌方法，并直接链接 Followwriting、参考引导写作、写作理由矩阵与科研表达原文。[写作提示词](../assets/templates/writing-prompts.md)用于填入本次范围和现行材料，[借鉴示例](writing-examples.md#参考写法的借鉴与退回)展示怎样落实及撤回错误对应。执行后只做 [一轮文字复查](writing-review.md#写后反向检查从实际成稿出发)，本文件集中维护方法边界与网页连接。

## 方法适配边界

| 上游方法或默认 | 在本框架中的适配 |
|---|---|
| 先确立贡献、安排证据，再借鉴参考 | 已融入写作模块。区分主比较、解释性分析与适用范围，段落先有职责和本研究证据 |
| 写作理由矩阵与逐句映射 | 吸收“原问题—写作动作—依据—成稿效果”，复用提纲或现有记录，不强制十列表、贡献编号文件或逐行 PASS/FAIL |
| 参考学习数量及通用主动表达 | 按本轮目标、实际可得资料及作者约定执行，局部改写不强制“3+3”，自然被动等现行语言规则继续优先 |
| 新写作者与独立审阅者 | 默认执行者写作，加本框架已授权的一名只读文字复查者，不因此启动新写作代理或多轮全文审查 |
| 全文交付与渲染 | 服从用户范围。只要文字就只交文字，Word、页面和格式检查在对应文档任务中按实际需要实施 |

原版 `embedded/paperspine-v6/skills/` 保留来源和许可证，项目适配不写回其方法文件。写作决策、对照和核验说明保存在需要的工作记录中，论文正文仍表达研究问题、方法、结果与讨论。Web 配置中的作者表达偏好与当前明确要求一并执行，不能由参考论文替代作者声音。

## 工作台与同一论文续写

工作台是宿主执行研究与写作的界面和状态层。它不会因启动服务就自动写论文。宿主必须把真实产物、完成进度和作者反馈写入同一任务。

- 使用宿主安装的 Web 技能，先读取其 `skills-root.json` 和 `paper-spine/installation.json`，由其中的 manager 进入。当前可用桥接脚本为 [paperspine_workbench.py](../scripts/paperspine_workbench.py)，它只定位正式安装，不安装依赖或切到旧源码。
- 启动只返回本地地址和 profile。接入具体论文时，读取 Web 技能中的 `references/product-v1-workflow.md`，用 `web host tools --tool <名称>` 查看所需接口。通过 `paperspine_open_task` 创建或恢复产品任务，并核实作者选择的材料，随后仅打开返回的同任务 URL。安装测试不等于已创建或配置真实论文。
- 配置与授权材料是前提时，等待实际 Web 确认，不把宿主写入的提议当成作者同意。作者在聊天中已授权的独立工作可继续，不能用超时推定选择。
- 当前界面以配置、论文定位、科研配图、手稿和投稿周期组织。写作期间同一任务的内部里程碑使用 `draft`，证据研究用 `research`，配置用 `intake`。其余操作按当前接口，不把展示标签猜成 API 枚举。
- 实际文件用 `paperspine_publish_artifact` 登记，再用 `paperspine_commit_milestone` 记录真实阶段、摘要和 artifact_ids。使用刚读取的公共 `task_version` 作为 expected_version，写后回读，不能把本地存盘等同于网页阶段已更新。
- 恢复时核对相同 profile、task_id、授权材料、当前稿、pending choices 和反馈。用 `web host snapshot --summary --task-id <ID>` 读取简要状态，在现有续写位置保存事件 sequence 和下一步。task_version 与事件 sequence 是不同游标，不能混用，也不按最近任务猜选论文。
- 变更期刊或回到配置时保留同一论文记录，按接口回到 `intake`，再核对新规范。原始数据和作者现稿优先，不能用旧状态覆盖手改。状态通过官方接口更新，不直接编辑生成的桥接 JSON 或数据库。

纯文字模式也能按“现稿、证据、采用的参考与定位、已完成范围、待办”接续。未启用 Web 时不宣称保存了网页任务。图表仍由本框架的图表模块选择后端，Word 定点修改仍遵守对象保护规则，不因开启工作台替换 Origin 或破坏公式、引文域。

## 本机启动与停止

Windows 上在 PowerShell 使用以下顺序，先输入复制后的本技能目录。当前机器已有 Python 3.13，不能直接使用默认指向 Python 3.8 的 `python`：

```powershell
$frameworkDirectory = Read-Host '输入论文框架技能目录的完整路径'
Set-Location -LiteralPath $frameworkDirectory
py -3.13 -B .\scripts\paperspine_workbench.py status
py -3.13 -B .\scripts\paperspine_workbench.py web launch --no-open
```

在浏览器打开启动结果中的 `address`，论文接入后使用返回的同任务 URL。查看状态或停止服务，在同一 PowerShell 与目录执行：

```powershell
py -3.13 -B .\scripts\paperspine_workbench.py web status
py -3.13 -B .\scripts\paperspine_workbench.py web stop
```

服务后台运行，`web status` 返回 PID 和 profile。停止前保存工作，`web stop` 只处理该正式安装绑定的服务。其他主机选择已确认的 Python 3.12+ 执行桥接脚本，只有官方支持的宿主与系统才启动 Web。未安装 manager 时脚本报出具体缺口，文字方法仍可用。

## 版本与更新

宿主由官方 V6 edition manager 管理，项目方法快照单独固定版本。通过 [官方清单](https://wubing2023.github.io/PaperSpine/v6/channel.json) 与对应 checksum 核对 ZIP，再更新宿主。为避免宿主升级后与项目快照无声漂移，本次安装关闭自动更新，手动更新时同时复核本适配及快照。复制技能不携带 profile、论文数据、密钥或 Python 二进制。

项目快照不调用 main 频道的 3.x updater。`upstream.json` 只说明已嵌入的来源，不能替代当前宿主的 manager status，也不能将历史测试记录当作新版本已通过。保留上游 `skills/` 原文，将作者习惯与流程差异放在本适配中。更新后只核验版本、受影响链接与入口、写作适配及实际使用的 Web 能力，不重跑无关实验或文档排版。
