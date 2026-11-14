# 学术写作改写对照

触发词: “防御性写作”, “像工程说明”, “论文语言冗余”, “结果分析”, “符号释义合段”。

以下全部是虚构教学例子。每组改写只使用该组给出的事实，不能将数字、方法和结论迁入真实论文，未提供的条件与结果也不补造。修改时先核对研究证据，规则统一见 [写作与证据](writing.md)，再选择合适表达，不要求每段套用同一种句式。

## 英文写作与符号的通俗示例

### 长句：在真正影响阅读时拆分

原文：The same model is used for both datasets, while the policies are trained separately for each dataset and evaluated on their respective test sets.

建议：The same model is used for both datasets. Policies are trained separately for each dataset and evaluated on their respective test sets.

共同设置与分别训练分开表达，仍保留各自测试集。若一句已经清楚，即使句子较长也不强行拆分。短句仍应留在承担同一作用的自然段中。

### 语态：看表达对象，也看作者风格

原文：We train each policy using the same settings.

建议：Each policy is trained using the same settings.

这里重点是训练安排，自然被动表达适用。文献归因另看上下文，例如 “Smith et al. [1] introduced the controller.” 应保留作者和对应引文，不为了被动语态改成无作者的句子。作者或期刊允许第一人称时，不把这条偏好机械升级为禁令。

### 精简：保留必要事实与限定

原文：The proposed method shows a decrease in energy consumption. Energy consumption decreases by 3% compared with the baseline under the tested condition.

建议：Under the tested condition, energy consumption decreases by 3% compared with the baseline.

删除同义重复，保留条件、比较对象、方向和数值。不将测试条件下的结果写成普遍结论。

### 变量到符号：一个量不使用两个名字

假设当前正文定义电池功率为 \(P_{\mathrm{bat},k}\)。插入公式时仍使用 \(P_{\mathrm{bat},k}\)，不要另用 \(P_{b,k}\) 表示同一电池功率。若旧稿存在两个写法，先对照定义和来源确认它们确为同一量，再按授权统一公式、文字、表头及相关文件。

### 符号到变量：一个完整符号不承担两个含义

假设 \(P_{\mathrm{bat},k}\) 已定义为第 \(k\) 步的电池功率，就不能再用完全相同的 \(P_{\mathrm{bat},k}\) 表示燃料电池功率。两种物理量应使用当前稿件中各自已定义的符号。若未定义，先核实并建立明确符号，再解释和使用。

### 不要把不同量误合并

\(P_k\) 可以表示第 \(k\) 步的瞬时功率，\(\bar P_k\) 可以表示事先定义的窗口均值。它们不同，不应因字母相同而删掉横线。\(P_k\) 与 \(P_{k-1}\) 代表同一变量在不同时间步的值。连续时间 \(t\) 与离散步 \(k\) 表示不同概念，不能全局机械替换。求和式 \(\sum_{i=1}^{n} x_i\) 中的 \(i\) 是局部索引，按该式的作用域核对。

### 公式说明：解释新量及作用，不重复参数表

**已知材料**：前文已定义非负源功率 \(P_{\mathrm{g},k}\) 和固定采样间隔 \(\Delta t\)。本例功率单位为 kW、时间单位为 s。给定的研究定义是将供能项与功率增量惩罚归一化后取时域平均，\(E_{\mathrm{ref}}>0\) 以 kJ 计，\(P_{\mathrm{ref}}>0\) 以 kW 计，权重 \(\lambda_{\Delta}\geq0\) 无量纲。

公式前可写：“为折中供能量与相邻时刻的源功率变化，平均无量纲代价定义为”

\[
J=\frac{1}{N}\sum_{k=1}^{N}
\left[
\frac{P_{\mathrm{g},k}\Delta t}{E_{\mathrm{ref}}}
+\lambda_{\Delta}
\left(\frac{\Delta P_{\mathrm{g},k}}{P_{\mathrm{ref}}}\right)^2
\right],
\qquad
\Delta P_{\mathrm{g},k}=P_{\mathrm{g},k}-P_{\mathrm{g},k-1}.
\]

不合适的释义：“where \(P\) is power, \(\Delta P\) is the ramp rate, and \(\lambda\) is a parameter.”

问题是完整符号不匹配、把功率增量误称为变化率，而且未说明新量和权重的作用。可改为：

> 其中，\(N\) 为评价时域内的采样区间数，\(\Delta P_{\mathrm{g},k}\) 为相邻采样时刻的源功率差。\(E_{\mathrm{ref}}\) 和 \(P_{\mathrm{ref}}\) 分别为能量与功率的正参考尺度，\(\lambda_{\Delta}\) 调节功率增量惩罚相对供能项的权重。

> where \(N\) is the number of sampling intervals in the evaluation horizon, and \(\Delta P_{\mathrm{g},k}\) is the difference between consecutive source-power outputs. The positive reference scales \(E_{\mathrm{ref}}\) and \(P_{\mathrm{ref}}\) normalize energy and power, respectively. The dimensionless weight \(\lambda_{\Delta}\) sets the relative penalty on power increments.

已定义的 \(P_{\mathrm{g},k}\) 与 \(\Delta t\) 无需再解释，参数表中的全部数值也无需重列。英文句法和 where 大小写随其与公式的衔接及当前规范处理。

量纲检查：kW 乘 s 得 kJ，两项均无量纲。若要定义变化率，应另用已核准的符号，例如 \(r_{\mathrm{g},k}=\Delta P_{\mathrm{g},k}/\Delta t\)，其单位为 kW/s。功率增量均方的单位为 kW²，不能换名为变化率均方。

本例的归一化和权重定义已在材料中给定，不意味着语言润色可以替真实研究新增归一化项、调整目标函数或改变权重量纲。

### 相邻符号集中解释

原文：δ 是死区。δ 的值为 120 W。ΔP 是功率变化。ΔP 表示相邻时刻输出的差。死区作用于功率变化惩罚。

改写：δ = 120 W 为功率变化惩罚的死区宽度，ΔP 表示相邻时刻的输出功率差。

英文：The deadband width δ = 120 W applies to the power-change penalty, where ΔP is the difference between consecutive power outputs.

结合公式所在位置衔接，保留真实稿件的可编辑对象。

## 从操作流程转为研究叙述

### 同一发现中的数字与解释合在一段

以下沿用后文连贯案例的虚构事实。分成三段时，比较与取舍被割开：

> 缓变负荷下，方案 B 的平均能量消耗比方案 A 低 6.0%。
>
> 同一条件下，源功率增量均方降低 30.0%，归一化跟踪误差从 1.5% 增至 1.8%。
>
> 结果说明能耗和功率动态改善伴随跟踪精度代价。

可以合为一个段落：

> 缓变负荷下，方案 B 的平均能量消耗比方案 A 低 6.0%，源功率增量均方降低 30.0%，但归一化跟踪误差从 1.5% 增至 1.8%。能耗和功率动态改善伴随跟踪精度代价。

数字和解释都服务于同一比较，合段后仍用两句表达，不把所有内容接成一个长句。后续若开始讨论输入维数的混杂或另一个研究问题，再另起段落。

### 去除工程流水账，保留研究协议

原文：我们先运行脚本生成训练曲线，再读取每个种子的 CSV，把结果写入工作簿，逐行检查后导出图像。每条轨迹的能耗先累计，然后在三个独立训练种子间计算均值和样本标准差。

改写：能耗先在每条轨迹内累计，再在三个独立训练种子间计算均值和样本标准差。

英文：Energy consumption is accumulated within each trajectory and then summarized as the mean and sample standard deviation across three independent training seeds.

保留影响统计解释的聚合层级，文件操作留在复现记录。实际研究有多条轨迹时，还必须交代轨迹之间如何汇总，不能照抄这句替代真实协议。

### 用设计目的组织方法

原文：第一步读取负荷，第二步分成慢变和快变部分，第三步让储能单元处理快变部分，第四步由主要电源分担慢变部分。

改写：负荷分解用于区分慢变需求与快速波动。储能单元承担快速波动，主要电源协调分担慢变需求，从而使功率分配对应不同的响应尺度。

改写只解释已有设计的作用，没有补造分解算法、频率阈值或稳定性结论。真正的计算步骤、公式与参数仍需在方法中定义，按目标格式放置。

## 结果中的事实、取舍与边界

### 从自我辩护转为具体结果

原文：在相同测试条件下，方案 B 的能耗比方案 A 低 2%，跟踪误差高 1%。但是，这不能说明方案 B 全面优于方案 A，也不能保证在其他条件下仍然有效，结果需要谨慎理解。

改写：在相同测试条件下，方案 B 的能耗比方案 A 低 2%，跟踪误差高 1%，表现出能耗与跟踪精度之间的权衡。

删除的是没有新增信息的自我辩护。条件与取舍已包含在观察结果中。

### 必要边界保留一次

原文：方案 B 在新数据集上重新训练，并在独立测试集上降低了能耗。因此，该方法具有很强的泛化能力。不过，模型已经重新训练，所以这并非直接迁移，也不足以证明任何数据都适用。

改写：方案 B 在新数据集上重新训练后，在独立测试集上获得了更低的能耗，补充验证了该方法在这一数据设置下的效果。

“重新训练”和实际验证范围合入正面陈述，去掉证据未支持的泛化结论和重复补救句。若审稿问题专门询问直接迁移，在回复中明确回答该实验是否执行。

### 代理指标与研究动机

原文：减轻运行负担是本研究目标。方案 B 降低了功率增量平方均值。我们没有测量退化。结果证明寿命得到延长。但这不是寿命实验，也不能保证寿命一定延长。

改写：方案 B 降低了功率增量平方均值，说明相邻时刻的功率变化减小，与减轻运行负担的研究目标一致。长期退化及寿命效应留待进一步验证。

实际测得什么就解释什么。是否需要最后一句取决于全文是否讨论寿命和读者是否可能据此误解，不将其作为所有代理指标段落的固定尾句。

### 提前终止：删提醒，保留比较范围

已知材料：方案 B 的测试提前结束，累计指标只计算已运行区段，方案 A 完整运行。

不合适：“方案 B 的累计能耗更低，因此经济性更好，但结果需要谨慎理解。”

可写：“方案 B 提前结束测试，累计能耗仅覆盖已运行区段，与方案 A 完整测试结果的覆盖范围不同。”

能量总量受运行时长影响，不能用删去提醒后的低累计值继续证明节能。是否另算共同区段、单位时间指标或纳入失败评价，由真实研究设计决定，不由润色补造。

## 摘要结论与结果的连贯示例

本节用同一个完全虚构的储能辅助供能研究，连接摘要、引言末段、方法概述、结果、讨论和结论。它展示各部分怎样沿同一问题与证据展开，不是任何真实手稿的匿名翻版。原文或材料没有提供的文献评述、参数及实验不由润色补造。

### 先限定可用事实

- 研究考察能耗、源功率变化和负荷跟踪的关系。方案 A 使用当前状态，方案 B 额外引入由历史负荷计算的近期变化特征，帮助表示当前负荷变化。
- 两方案采用同一类策略学习器、相同训练数据、训练预算和系统约束，其余学习设置一致。输入维数不同，尚未设置等维输入对照。
- 每个方案训练 6 次。测试使用同一仿真系统中的 4 条预留负荷，每类变化条件各 2 条，各条时长相同，测试记录与训练记录分开。测试时策略参数冻结。
- 累计能量先逐条计算，再在每个训练重复内对同类的 2 条测试记录取均值，最后对 6 个训练重复计算均值与样本 SD。其他指标先逐条计算，再按同一分组顺序平均。相对变化采用方案均值之差除以 A 的均值。
- 表中的跟踪误差为误差 RMS 除以额定功率后用百分数表示。功率增量均方表示相邻时刻源功率差的平方平均，采样间隔固定。两项仅给出跨重复均值。
- 缓变负荷下，6 个对应训练重复中有 5 个的 B 能量指标低于 A，另 1 个更高。尚未进行推断检验、退化试验或硬件验证。对应重复共享数据划分与测试负荷，不据此假定其他随机因素完全相同。

| 测试条件 | 指标 | 方案 A | 方案 B |
|---|---|---:|---:|
| 缓变负荷 | 能量 / kWh，均值 ± SD | 150.0 ± 6.0 | 141.0 ± 4.0 |
| 快变负荷 | 能量 / kWh，均值 ± SD | 120.0 ± 5.0 | 116.4 ± 4.0 |
| 缓变负荷 | 归一化跟踪误差 / %，均值 | 1.5 | 1.8 |
| 缓变负荷 | 源功率增量均方 / kW²，均值 | 0.50 | 0.35 |

计算对应关系：缓变负荷能量下降 6.0%，快变负荷下降 3.0%，缓变负荷功率增量均方下降 30.0%。跟踪误差增加 0.3 个百分点，相对增幅为 20.0%，两种表达不能混用。这些事实没有提供快变负荷下的跟踪误差或功率动态结果，不能自行补齐。

### 同一事实在各部分怎样使用

可用的研究问题是：加入近期负荷变化信息后，能耗是否降低，源功率变化与跟踪精度怎样取舍？这里没有提供完整领域综述，所以引言示例只演示研究问题与本文工作段，不假称填补了某个领域空白。

| 事实 | 在本文论证中的位置 |
|---|---|
| 方案 B 加入近期变化特征 | 方法说明输入设计，摘要概括其作用，引言将其连接到研究问题 |
| 两类条件能量分别降低 6.0% 和 3.0% | 结果给出对应比较，摘要压缩主发现，结论回答有效范围 |
| 缓变负荷动态指标降低但误差升高 | 结果陈述取舍，讨论解释它为何影响评价，结论归纳设计判断 |
| 六个缓变重复中五个改善 | 结果交代分布，讨论及结论避免把平均优势写成逐次保证 |
| 尚无等维对照、退化及硬件验证 | 讨论限定解释，展望提出与缺口对应的验证，不在每句后反复提醒 |

### 摘要：方法、条件与关键取舍对应

不合适的概括：“构建先进智能框架，显著提高综合性能，证明其具备广泛泛化能力并能延长设备寿命。”

中文完整示例：

> 本研究考察储能辅助供能系统中能耗、源功率变化与负荷跟踪之间的权衡。方案 B 在策略输入中加入近期负荷变化特征，以补充当前状态信息。在同一仿真系统中，每种方案训练 6 次，并在 4 条预留负荷上与仅使用当前状态的基准比较。缓变和快变负荷下的平均能量消耗分别降低 6.0% 和 3.0%。缓变负荷下，源功率增量均方降低 30.0%，但归一化跟踪误差从 1.5% 增至 1.8%。所测试的两类条件均呈现较低平均能耗，缓变条件下的功率动态改善则伴随跟踪精度代价。

英文完整示例：

> This study examines the trade-off among energy use, source-power variation and load tracking in a storage-assisted power system. A recent demand-trend feature was added to the policy input to supplement current-state information. The method was compared with a baseline using only current-state inputs in the same simulation model. Six training runs per method were evaluated on four held-out load traces. Mean energy consumption was reduced by 6.0% under slowly varying loads and by 3.0% under rapidly varying loads. Under slowly varying loads, the mean squared source-power increment was reduced by 30.0%, while the normalized tracking error increased from 1.5% to 1.8%. The results show lower mean energy consumption under both tested load conditions, with a tracking-accuracy cost under slowly varying loads.

| 摘要中的信息 | 怎样连接前后 |
|---|---|
| 开头的问题 | 给出后续必须同时评价的三个方面，不从宏大背景绕行 |
| 特征设计及作用 | 回答方法做了什么，不靠算法名堆砌贡献 |
| 仿真、基准及测试 | 交代结果成立的对象和范围，训练重复不误写为轨迹数量 |
| 两类能耗结果 | 相同指标分别对应条件，不写成不明来源的“最高降低 6.0%” |
| 动态指标与误差 | 在同一条件中呈现收益及代价，避免用“综合更优”遮盖 |
| 最后判断 | 直接回答问题，不引入寿命、实装或普适性等新结论 |

如果字数紧，可将最后一句的判断融入主结果句，删除重复概括，不能把关键代价删掉。若研究重点转为单一工况，应按真实目标重新取舍。这里两种语言均使用完整自然段，英文方法和评价安排优先自然被动，不要求中文同步被动化。

### 引言末段：把问题连接到本文工作

> 本研究关注近期负荷变化信息对储能辅助供能策略的影响，比较其对能耗、源功率变化和负荷跟踪的作用。为此，在仅使用当前状态的策略基础上增加由历史负荷计算的变化特征。两种方案在相同训练预算和系统约束下进行比较，并在缓变与快变负荷上评价。分析分别考察平均表现、训练重复间的差异以及功率动态和跟踪精度的取舍。

该段提出本研究要回答的问题、方法增量和评价思路，没有提前复制百分比。真正的引言前文还需用可核实文献解释为什么研究该关系，不能以本段冒充完整综述。贡献表述对应实际做出的比较，不自动声称方法首创或机制已证实。

### 方法与评价概述：让比较有明确对象

> 方案 A 仅以当前状态作为策略输入，方案 B 在此基础上加入由历史负荷计算的近期变化特征。两种方案采用同类策略学习器、相同训练数据、训练预算和系统约束，每种方案进行 6 次训练。训练完成后冻结参数，并在 4 条与训练记录分开的预留负荷上评价，其中缓变与快变条件各包含 2 条等时长记录。
>
> 能量先在每条测试记录内累计，再在每个训练重复内对同类的两条记录取均值，最后计算六个训练重复的均值与样本标准差。功率增量均方和归一化跟踪误差先逐条计算，再按相同分组顺序平均。相对变化以方案均值之差除以方案 A 的均值计算。

前段说明设计与评价对象，后段定义统计层级。主文的真实方法还须给出学习器、特征构造、约束及参数等可复现定义，不能因概述读起来完整就跳过缺失信息。此处只使用已给事实，输入维数是否受控在相关解释位置交代。

### 结果段：数字用于论证，SD 不替代检验

> 在缓变负荷下，方案 B 的平均能量消耗由方案 A 的 150.0 kWh 降至 141.0 kWh，降幅为 6.0%，跨训练重复的 SD 从 6.0 kWh 降至 4.0 kWh。六个对应重复中有五个获得较低能量消耗，另一个更高。与此同时，源功率增量均方从 0.50 kW² 降至 0.35 kW²，归一化跟踪误差从 1.5% 增至 1.8%。能耗和功率动态指标改善伴随跟踪精度代价。
>
> 快变负荷下，平均能量消耗由 120.0 kWh 降至 116.4 kWh，降幅为 3.0%，小于缓变条件下的平均降幅。两类测试都呈现平均能耗降低，收益幅度随条件变化。

先讨论缓变条件下的主要发现和取舍，再用另一条件说明平均收益的范围。这里未提供快变条件的动态与误差数据，不能假定其变化方向相同。描述性差异不等于经过统计检验的条件效应，较小 SD 不证明统计显著或学习机制。

六个训练重复各测试四条记录，共有 24 次轨迹评价，按本例协议不能写成 24 次独立训练重复。表格承载完整数值，正文选择回答研究问题的比较。

### 讨论段：解释设计含义，保持证据层级

> 两类负荷下的平均能耗均降低，支持在所测试的仿真条件下继续评估包含近期负荷信息的输入设计。缓变负荷中较小的源功率增量伴随较大的跟踪误差，说明评价这一设计时需要同时考虑能耗、功率动态和跟踪精度。仅选一个有利指标不足以反映这种取舍。训练重复中出现一次能量上升，也表明平均改善没有覆盖每次比较。
>
> 当前对照同时改变了信息内容与输入维数，因此尚不能将差异完全归因于近期变化信息。等维输入对照可进一步辨别两者的作用。功率增量指标反映的是运行动态，后续可结合退化模型与老化数据研究其与长期退化的联系。

讨论将观察转换为设计判断，并解释现有比较能辨别到哪里。没有把“趋势特征改善预测，所以能耗一定降低”写成机制，因为材料既没有相应预测评价，也没有排除全部替代解释。边界集中在受影响的解释处，不在每个结果句后重复。

### 结论：回答问题，不重复整张表

中文完整示例：

> 本研究考察了储能辅助供能系统中能耗、源功率变化和负荷跟踪的关系。方案 B 在当前状态输入中加入近期负荷变化特征。含有该特征的方案与当前状态基准在相同训练预算和系统约束下进行比较。评价覆盖同一仿真系统中的两类预留负荷和多次训练重复。
>
> 加入近期负荷变化特征的方案在两类条件下均获得较低的平均能量消耗，缓变与快变负荷下的降幅分别为 6.0% 和 3.0%。缓变条件下，源功率增量均方降低 30.0%，归一化跟踪误差增加 0.3 个百分点。这一结果体现出能耗、功率变化与跟踪精度之间的取舍，评价该设计需要同时考虑三者。缓变条件下的能量改善出现在六次重复中的五次，平均优势没有覆盖每次比较。
>
> 当前结果支持进一步研究近期负荷信息在此类输入设计中的作用，但信息内容与输入维数的贡献仍需区分。后续可设置等维对照，以进一步辨别两者。退化模型与老化数据可用于研究功率动态指标和长期退化的关系，目标硬件上的时序测试可检验实际执行的可行性。

英文完整示例：

> This study examined the relationship among energy use, source-power variation and load tracking in a storage-assisted power system. A recent demand-trend feature was used to supplement current-state inputs. The feature-augmented method was compared with a current-state baseline under the same training budget and system constraints. Evaluation covered two classes of held-out loads and repeated training runs in the same simulation model.
>
> Lower mean energy consumption was obtained under both load conditions, with reductions of 6.0% for slowly varying loads and 3.0% for rapidly varying loads. Under slowly varying loads, the mean squared source-power increment was reduced by 30.0%, while the normalized tracking error increased by 0.3 percentage points. These findings identify a trade-off among energy use, power variation and tracking accuracy. Energy consumption was lower in five of the six corresponding training runs under slowly varying loads, so the average advantage did not extend to every comparison.
>
> The results support further investigation of recent demand information in this input design. The contributions of information content and input dimension remain to be distinguished. A comparison with equal input dimensions could help separate these effects. Degradation models and ageing data could be used to examine the relationship between power dynamics and long-term degradation. Timing tests on the target hardware could assess execution feasibility.

| 结论的段落 | 所起作用 |
|---|---|
| 工作概括 | 问题、关键设计、基准与完成范围，信息足够而不重写引言 |
| 主要回答 | 按研究问题归纳不同条件的结果，给必要数字，保留取舍及例外 |
| 解释与后续验证 | 不将信息内容的贡献说死，展望分别对应输入混杂、退化和硬件证据缺口 |

开头四句只是本例安排，不规定所有结论四句。结论中的解释和缺口已在讨论建立，没有首次加入实验或未验证机制。英文减少同一句中多个嵌套关系，保留方法与结果作主语的自然主动句，也不为被动语态删除必要施事。

### 摘要和结论怎样保持一致而不重复

摘要先让陌生读者了解问题、做法和主发现，结论给已了解研究的读者明确回答和后续方向。本例两处使用相同条件及降幅，不能为了避免重复换成“最高降低”“全面优于”等改变范围的表达。

摘要保留关键误差从 1.5% 到 1.8% 的变化，结论用 0.3 个百分点概括同一事实，两者口径一致。SD 和逐次例外在结果中较详细展开，结论按其对主判断的影响保留，摘要不必装入全部统计。术语保持一致，详略和句子作用可以不同。

### 两种百分比算法不能换用

另一个独立虚构算例中，两个对应样本的 A 能量为 100、200 kWh，B 为 90、190 kWh。按方案均值计算，降幅为 \((150-140)/150=6.67\%\)。先逐样本计算再平均，结果为 \((10\%+5\%)/2=7.50\%\)。

两种数值回答不同的汇总问题，没有统一适用于所有设计的算法。真实研究应按分析协议选择、说明并保持跨文件一致，不能混入上面的六次训练案例。

## 回复问题与引出图表

### 精简不能遗漏审稿问题

已知问题：审稿人询问为什么设置死区，以及是否做过敏感性实验。材料只说明死区用于避免惩罚小幅变化，尚无敏感性实验。

不充分的回答：已精简有关描述，方法设置合理。

合适的回复内容：死区用于避免对小幅功率变化施加惩罚。本文采用固定死区设置，尚未开展其宽度的敏感性实验。

正文应解释死区的作用和实际取值，回复直接回答两个子问题。是否增加实验由研究计划决定，不能用语言润色冒充已补做。该事实无需在全文每个结果段重述。

### 图表说明保持学术用途

原文：请读者打开补充材料，按照文件编号找到表格，查看每个条件的对应列，我们还做了数值核验。

改写：表 Sx 比较了不同条件下的指标结果。

这句话只用于引出材料。后文仍应基于真实结果说明关键发现，不能以“比较了”代替结果分析。文件定位与核验状态写在交付信息或本地工作记录中。
