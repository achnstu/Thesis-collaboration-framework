# 文献工作流与写法参考

## 模块执行与验收

先固定待支持的论断、主题范围、现有文献和所需产出，只检索或精读本轮相关材料。不为核对一条引文重建全文综述，也不默认运行 PaperSpine 全流程。

完成后从采用的每条引文反查实际来源及相应原文位置，再从待支持论断反查是否遗漏、错配或超出原文范围。元数据核对、摘要筛选和原文支持分别按实际状态记录。已核且版本未变的来源可复用，存在具体冲突时才扩查。只有元数据不能声称原文支持已核。

需要起草或改写综述时，同时执行 [文字自检](writing-review.md)，但不因检索任务自动改写作者正文。来源记录可直接交接给写作模块，无需附一套重复报告。

## 从问题到证据

1. 按研究问题拆分检索主题，记录关键词、同义词、时间范围、数据库、检索日期和筛选条件。资料不足时识别可用数据库或工具，优先利用用户现有文献库。
2. 将候选文献去重并核对题名、作者、年份、刊物、卷期、页码、DOI 或其他稳定标识。区分正式发表、预印本和会议版本，不根据不完整摘要猜测元数据。
3. 先读摘要筛选，再查实际原文的相关段落、图表、方法和限制。为每个论点记录来源页码或段落、作者实际主张与适用条件。拿不到原文时标“未核原文”，不宣称充分支持。
4. 按研究路线、问题和方法综合文献，分析各自适用条件、进展和不足。参考论文只用于学习论证结构，不把其数据、观点或研究结论移植为作者成果。
5. 引文绑定具体句子。写入 Word 时保护 Zotero 等已有引用域，文末条目、正文引用域和唯一文献数分别核查。替换文献时复核受影响的其他引用与编号。

## 工作表字段

| 文献 ID | 作者、题名、年份、出处、DOI | 版本及来源 | 原文定位 | 可支持的具体主张 | 限制 | 使用位置 | 核验状态 |
|---|---|---|---|---|---|---|---|
| 待填写 | 待填写 | 待填写 | 页码或段落 | 待填写 | 待填写 | 章、节或句子 | 元数据已核/原文待核/支持已核 |

依据可用许可决定是否保存原文及是否公开分享。文献检索工具返回的摘要或元数据是线索，不能替代核验。对于政策、标准、软件版本等时效性材料，记录版本和访问日期。

## 检查

综述中的比较维度要一致，分清文献结论和本文判断。数字、比较对象、实验条件、否定、适用范围及引文位置与原文对应。撤回、勘误或版本冲突需另行说明。缺少出处或支持不足时保留为待补项，不编造引文。

## 经典写法片段

以下以原文短引提供定位，再用中文复述其完整写法逻辑。复述是对相关摘要、结论或讨论的阅读分析，不是原文译稿，也不是这些论文每句话都值得照搬。公开作者、题名和 DOI 在下方对应。教学段落另集中在 [同一案例的完整写法](writing-examples.md#摘要结论与结果的连贯示例)，不把来源事实改写成本研究成果。

### 1. 摘要把难题、方法能力与验证接起来

**原文短引**：“A core challenge is to shape and maintain a high-temperature plasma within the tokamak vessel.” N1，Abstract。

完整逻辑：先确定控制对象，再解释为什么它难控，包括维数、频率和多种构型的要求。随后介绍控制架构能接受什么目标、控制哪些执行器以及满足什么约束。方法不是停在算法名上，而是接到真实设备上完成的多类构型控制，再以具体控制能力支持意义判断。

可以借鉴的关系是“问题具有哪些具体要求 → 设计如何响应要求 → 哪类实验检验这些能力 → 结果支持什么用途”。这使方法和验证都由问题引出。自身只有仿真时，验证句必须停留在仿真，不因采用同类学习算法就借用实际装置结论。原文中较强的评价措辞也不自动成为本框架默认语气。

### 2. 摘要从可解释的瓶颈走向核心贡献

**原文短引**：“Structural coverage is bottlenecked by the months to years of painstaking effort required to determine a single protein structure.” N2，Abstract。

完整逻辑：先说明结构知识的重要性与覆盖不足，继而指出实验获取结构的时间瓶颈。再把问题收束为由序列预测结构，以及现有方法在特定困难情形下的精度不足。提出模型后，用独立评测中的准确性说明贡献，最后交代使这一能力成立的设计思想。

这篇摘要并未机械采用“背景、方法、结果、意义各一句”的顺序，关键设计说明放在验证之后，仍能形成完整逻辑。可借鉴的是用真实瓶颈限定问题，用恰当的验证说明能力，而非一定在摘要列出多组百分比。领域历史、精度等级和“首次”等优先性判断不能移植，必须由当前研究自己的文献与结果支持。

### 3. 工程摘要与结论共同呈现多层比较

**原文短引**：“Strategy adaptability was tested using designed operational conditions and actual navigation conditions.” L1，PDF 页 1，Highlights。完整组织对照 Abstract 及 PDF 页 22–23，Conclusions。

摘要从能量管理与局部控制相互影响这一关系出发，介绍上层策略和局部控制器，再交代不同负荷与硬件在环评价，随后报告主要能耗和动态指标。结论回到该层级设计，分别回答不同工况、不同控制器及不同指标上的比较，并保留某些动态指标未占优的取舍。最后将模型简化、数据与硬件验证不足连接到后续研究。

可借鉴的是先说明“为什么比较这些组合”，再报告“哪项指标在什么条件下改善”，结论继续解释组合的适用判断。不能只摘总体优势而删掉指标取舍，也不将实际航行记录驱动的硬件在环测试写成完整船舶实装验证。多工况的数字可以在自己的摘要中拆句或逐条件对应，原文长句不是必须模仿的样式。

### 4. 比较结果先交代基准的职责与信息条件

**原文定位**：L2，PDF 页 8 的基准说明，以及 Abstract 和 Conclusions，PDF 页 1、14–15。下方保留该文完整摘要，避免在此重复摘句。

完整逻辑：摘要先将研究目标限定为航次成本，再介绍用历史负荷训练、用另一时间段数据测试的安排，最后在相同状态空间分辨率的条件下报告相对于离线参考的成本表现。结果章节先定义训练数据验证与独立数据评价的区别，并说明离线规划需要未来负荷信息，随后才展开平均结果和代表航次。结论据这些证据回答方法在何种历史数据基础上可用于功率分配，再提出连续空间等后续工作。

可借鉴的是“评价对象 → 比较条件 → 观察结果 → 可作出的判断”，而不是用“接近最优”替代精度、信息条件和评价指标。数据来自真实记录不等于控制器已完成实船闭环验证，成本上的比较也不自动延伸到排放或所有动态指标。

### 5. 结论沿研究问题逐层收束，保留不同指标的尺度

**原文短引**：“By contrast, hydrogen consumption varied modestly across the module-rating configurations.” L5，PDF 页 14，Conclusion。

完整逻辑：开头概括改造对象、记录数据和负荷分解—配置—模块优化三部分工作。主体首先回答哪种分解在主要电源平滑和储能负担之间较均衡，再回答不同混合配置如何改变缓冲需求，最后回答模块额定功率如何影响模型退化。模块结果的解释联系活跃模块数、低功率运行及启停等分解项，同时指出氢耗变化幅度较小。综合判断因此落在保留模块差异进行建模的必要性，而非笼统的全部指标改善。

可借鉴的是结论的层级来自前文研究问题，各层结果共同支持最后的认识。模型分解可以支持模型内的解释，不能自动升级为直接老化试验证据。自己的结论需要保留这种证据层级，即使使用了真实负荷记录也一样。

### 6. 公式后的释义解释参数如何参与方法

**原文短引**：“\(k_p\) is the constraint penalty factor of the SOC value of the battery.” L3，PDF 页 13，Eq. (31) 后。

完整逻辑：先交代用于功率分配的多目标代价，再给出代价项及其组合。式后介绍预测步骤内的消耗、退化代价、参考状态偏差和惩罚因子的作用，随后把退化项展开成更具体的组成。读者先知道为什么有这个目标，再理解新符号如何参与计算，而不是只收到一串取值。

可以借鉴“作用 → 公式 → 新量及角色 → 必要的进一步定义”。释义仍须核对完整符号、量纲和作用域，已有量不重复说明。本文献的术语、大小写或符号不能当作自身定义正确的证明，也不能为模仿写法而给自己的目标函数新增代价项。完整自拟释义见 [公式示例](writing-examples.md#公式说明解释新量及作用不重复参数表)。

### 7. 展望由研究尚未回答的权衡引出具体工作

**原文短引**：“Future work will extend the framework towards multi-objective optimisation” L5，PDF 页 14，Conclusion。

完整逻辑：前面发现模型退化对模块配置较敏感，而氢耗变化较小，说明两类目标的关系值得进一步研究。展望因此提出将退化和效率共同纳入优化，用具体的多目标表述研究它们的取舍，并说明希望澄清节能与负荷诱发退化之间的联系。

可借鉴的是“现有发现或缺口 → 后续方法 → 要回答的新问题”，而不是只写“继续优化框架”。方法名称应服务于问题，展望用计划语气，不宣称尚未进行的优化必然同时改善全部指标，也不把某种求解形式当作覆盖所有权衡解的保证。

### 8. 讨论先承认比较差异，再把适用假设连到改进方向

**原文短引**：“By contrast, Swift’s perception system assumes that the appearance of the environment is consistent with what was observed during training.” N3，Discussion。

完整逻辑：先概括已达到的竞赛表现，再解释系统与人类在感知信息、延迟和相机刷新方面各有什么差异。随后讨论碰撞恢复及环境外观变化对适用性的影响，明确识别依赖训练环境外观的假设，再提出增加条件多样性的训练方式，并说明这将服务于什么样的比赛设置。

可借鉴的是把边界写成具体的技术关系，而不是在主张后反复加“需谨慎理解”。总体获胜、最快单次和每场均获胜是不同判断，优势与例外应按实际记录表述。没有相同的外观假设或竞赛任务时，不搬用该局限，也不机械保留 By contrast。

### 原文段落精读：摘要到结论的完整衔接

以下四段保留原文句子，仅整理 PDF 换行、断词及上下标显示。它们的算法、数值和主张属于来源论文，与本包虚构案例及用户成果分开。出处的作者、题名和 DOI 见下方相同编号，借鉴时还需按当前作者的语言规则调整，不把已经发表视为措辞和归因必然正确。

**A. 完整摘要：问题、方法、数据与受条件限定的结果。** L2，Applied Energy，PDF 页 1，Abstract。

> Hybrid fuel cell and battery propulsion systems have the potential to offer improved emission performance for coastal ships with access to H2 replenishment and battery charging infrastructures in ports. However, such systems could be constrained by high power source degradation and energy costs. Cost-effective energy management strategies are essential for such hybrid systems to mitigate the high costs. This article presents a Double Q reinforcement learning based energy management system for such systems to achieve near-optimal average voyage cost. The Double Q agent is trained using stochastic power profiles collected from continuous monitoring of a passenger ferry, using a plug-in hybrid fuel cell and battery propulsion system model. The energy management strategies generated by the agent were validated using another test dataset collected over a different period. The proposed methodology provides a novel approach to optimal use hybrid fuel cell and battery propulsion systems for ships. The results show that without prior knowledge of future power demands, the strategies can achieve near-optimal cost performance (96.9%) compared to those derived from using dynamic programming with the equivalent state space resolution.

| 原段位置 | 起的作用 | 写自己论文时怎样处理 |
|---|---|---|
| 前三句 | 应用对象及约束引出成本问题 | 留下解释研究问题所需的背景，不必照搬三句铺垫 |
| 第四句 | 指出方法及其成本目标 | 写清设计作用，不只列算法名 |
| 第五、六句 | 交代训练数据与另一时间段测试 | 用真实协议说明证据从哪里来 |
| 第七句 | 提出方法意义 | 判断是否新增信息，自己的稿件可省去重复评价 |
| 最后一句 | 结果连同无未来负荷信息及相同分辨率条件 | 关键数字、基准和条件绑定，不能只摘百分比 |

这段不是一句“应用了强化学习”之后直接报效果。数据和比较条件使最后的性能判断可解释。96.9% 是该来源对成本表现的表述，不能当作节省 96.9%，也不能用于本研究。来源中较重复的系统名称和评价语不必照搬，组织逻辑与语言选择分别判断。

**B. 结论开头：概括做法和实际完成的验证。** L1，Applied Energy，PDF 页 22，Section 5 Conclusions 首段。

> This study proposed a hierarchical energy management method for ship FCBHPS, combining the NMPC-based EM strategy and a local controller. Comparative tests of the performance of six typical EM strategies were conducted based on HiLs. The research yielded the following conclusions:

第一句将系统、方法及两个层级关联，第二句给完成的比较范围，第三句转入主要发现。它展示结论怎样承接研究工作，不能单独作为完整结论。FCBHPS、EM 和 HiLs 沿用该文术语，不要求其他论文采用。自己的结论可直接进入主要发现，不必重复末句的引导套语，也不必同样用编号列表。

**C. 结论主体：先给发现，再解释差异并保留另一指标的变化尺度。** L5，International Journal of Hydrogen Energy，PDF 页 14，Section 6 Conclusion 的模块层分析段。

> At the subsystem level, the degradation-minimising MPC showed that PEMFC degradation depends strongly on the selected module power rating. The 35 × 200 kW configuration exhibited the lowest cumulative degradation, whereas the 100 × 70 kW configuration exhibited the highest cumulative degradation. This difference was mainly driven by the larger number of active modules required in the lower-rated configurations, which increased cumulative exposure to low-power operation and start–stop events. By contrast, hydrogen consumption varied modestly across the module-rating configurations.

段内顺序为“模块层问题 → 哪些配置的模型结果不同 → 模型中哪些暴露项解释差异 → 氢耗没有同幅变化”。最后一句让读者明白退化与能耗的敏感性不同。自己的段落需要具有相应分解证据才能写成原因，不能仅凭两组总指标复制 mainly driven by。这里的退化是论文模型的分析对象，不由本摘录升级为实测寿命。

**D. 展望段：说清要补的工作和它要澄清的关系。** L5，同页 Conclusion 末段。

> Future work will extend the framework towards multi-objective optimisation using weighted-sum formulations that jointly consider degradation and efficiency. This will enable exploration of Pareto-optimal trade-offs between lifetime preservation and hydrogen consumption, clarifying how gains in fuel economy relate to accelerated load-induced degradation.

第一句给后续方法和联合目标，第二句交代它要研究的科学关系，承接前面的不同指标表现。迁移时根据自己的缺口决定验证，不因参考文献采用加权和就替自己的研究确定求解方法。尚未执行的工作宜表述为计划检验什么，避免把计划写成必然同时改善全部目标。

这四段分别展示完整摘要、结论开头、结论发现段和展望段，不要求拼接成一篇新论文。自己的摘要与结论应从同一份真实证据构建，具体写法见 [连贯中英案例](writing-examples.md#摘要结论与结果的连贯示例)。

### 将阅读分析转为自己的写法

先用当前证据写一句研究主张，再检查该主张需要哪些方法、验证和结果支撑。选取上面适合的信息关系，形成自然段，最后按本包语言规则审查语态、句长、术语和符号。论证链缺失时回到材料补核，不能靠套句填上未知事实。

来源可以启发组织，但不规定段落长度、被动语态比例或固定措辞。摘要与结论的完整中英案例和逐段作用在 [改写示例](writing-examples.md#摘要结论与结果的连贯示例)，一般方法在 [写作规则](writing.md#摘要结论结果与公式释义)。原文只保留已注明的短引，不复制整段为自己的论文。

## 写作参考论文的阅读记录

以下保留公开题名、作者、稳定出处和实际阅读范围，来源分类及其与修稿经验的关系见 [写作规则](writing.md#文献学习与经验来源)。

### 相关领域全文

下列五篇以本地全文为阅读基础。仅列公开出处，不复制原始 PDF、私人库路径或真实手稿。页码为所读 PDF 页序，版本不同可按章节定位。阅读范围是相关章节，并非逐页审读整篇。

| 编号与公开出处 | 实际阅读位置 | 写法启发及边界 |
|---|---|---|
| L1 · Liu et al. **Multi-objective hierarchical energy management strategy for fuel cell/battery hybrid power ships**. Applied Energy 379 (2025), 124981. [DOI](https://doi.org/10.1016/j.apenergy.2024.124981) | 摘要、模型释义、结果、结论，PDF 页 1、5、13–14、16–17、22–23 | 能耗、动态质量和计算代价分别讨论，说明不同工况与硬件在环各验证什么。不能借其寿命叙述为自身代理指标加结论 |
| L2 · Wu, Partridge & Bucknall. **Cost-effective reinforcement learning energy management for plug-in hybrid fuel cell and battery ships**. Applied Energy 275 (2020), 115258. [DOI](https://doi.org/10.1016/j.apenergy.2020.115258) | 摘要、公式、Section 6、Section 7，PDF 页 1、3–4、8–15 | 区分训练集验证、独立测试和代表轨迹，交代 DP 与在线方法的信息条件。成本与排放的方向不能混写 |
| L3 · Lin, Ren & Xu. **Stochastic velocity-prediction conscious energy management strategy based self-learning Markov algorithm for a fuel cell hybrid electric vehicle**. Energy 320 (2025), 135167. [DOI](https://doi.org/10.1016/j.energy.2025.135167) | 摘要、转移概率、目标函数、预测结果、结论，PDF 页 1、6、13、15、20 | 预测精度与控制效果分别验证，交代时间和预测跨度条件，释义说明代价项作用。符号和量纲仍需独立核对 |
| L4 · Fan et al. **LSTM-augmented DRL for generalisable energy management of hydrogen-hybrid ship propulsion systems**. eTransportation 25 (2025), 100442. [DOI](https://doi.org/10.1016/j.etran.2025.100442) | 摘要、Section 4 相关实验、Section 5，PDF 页 1、15–16、24、29–30 | 区分算法、特征、权重及测试条件的作用，多组百分比须与指标对应。泛化表述由本研究实际协议决定 |
| L5 · Kamilakis et al. **Energy management and module-level optimisation of load-induced PEMFC degradation in retrofit hybrid maritime power systems**. International Journal of Hydrogen Energy 254 (2026), 155747. [DOI](https://doi.org/10.1016/j.ijhydene.2026.155747) | 摘要、指标定义、配置比较、结论，PDF 页 1、5、12–14 | 分清能效、功率动态和模型退化，结合分解项讨论差异。真实负荷加退化模型仍不等于直接老化试验 |

### 高水平跨领域论文及算法来源

| 编号与公开出处 | 实际阅读位置 | 写法启发及边界 |
|---|---|---|
| N1 · Degrave et al. **Magnetic control of tokamak plasmas through deep reinforcement learning**. Nature 602 (2022), 414–419. [DOI](https://doi.org/10.1038/s41586-021-04301-9) | Abstract、Learning control and training architecture、Control demonstrations、Discussion | 区分控制目标、模拟训练与实际设备演示，具体证据对应实际控制结论。其设备验证不能转为其他论文的事实 |
| N2 · Jumper et al. **Highly accurate protein structure prediction with AlphaFold**. Nature 596 (2021), 583–589. [DOI](https://doi.org/10.1038/s41586-021-03819-2) | Abstract、The AlphaFold network、Interpreting the neural network、Discussion | 方法设计紧扣验证问题，整体性能与组件消融分开，意义受基准范围约束。不要求所有摘要都列百分比 |
| N3 · Kaufmann et al. **Champion-level drone racing using deep reinforcement learning**. Nature 620 (2023), 982–987. [DOI](https://doi.org/10.1038/s41586-023-06419-4) | Abstract、Results、Discussion | 总体优势与局部例外同时呈现，解释与假设分层，信息及延迟差异影响比较。总体获胜不能改成每次、每段均最优 |
| A1 · Haarnoja et al. **Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor**. ICML, PMLR 80 (2018), 1861–1870. [公开全文入口](https://proceedings.mlr.press/v80/haarnoja18b.html) | Abstract、Sections 4–6，PDF 页 1、4–8 | 先交代优化目标，再解释新符号和分布作用，比较与消融分开。该文相关曲线使用五次试验的 min–max 阴影，不能默认其为 SD 或 CI。这是会议论文，不标为期刊 |

### 写作资料

| 编号与公开出处 | 实际阅读位置 | 可借鉴范围 |
|---|---|---|
| W1 · Mensh & Kording. **Ten simple rules for structuring papers**. PLOS Computational Biology 13 (2017), e1005619. [DOI](https://doi.org/10.1371/journal.pcbi.1005619) | 重点为 Rules 5、7、8 及相关结构说明 | 摘要形成完整逻辑，结果按贡献组织，讨论联系贡献、局限和意义。不照搬第一人称句式或统一段落模板 |
| W2 · **ICMJE Recommendations: Preparing a Manuscript for Submission to a Medical Journal**. [原文](https://www.icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html) | Abstract、Results、Discussion，访问日期 2026-11-14 | 摘要与全文一致、挑选主结果、不逐项复述表格、结论不过度外推。临床报告和结构摘要要求不推广到所有工程论文 |

这些是写法的阅读依据，不是自动加入用户论文的参考文献清单。公开作者、题名和 DOI 保持真实，私人手稿及教学例子保持匿名。除明确标注的原文短引外，归纳以自己的话说明，不搬用原句、数据、方法或强结论为用户成果。离线使用本包即可读取归纳规则和示例，联网原文不是执行这些写作规则的前提。
