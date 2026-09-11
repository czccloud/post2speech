# AGENTS.md — AI 迭代守则

本仓库迭代一个口语化改写 Skill：`SKILL.md` 是路由，具体规则按模型分文件放在 `references/` 下（当前有 GLM 5.3、Kimi K3）。任何 AI 参与本仓库的工作时，必须遵守以下守则。方法论详见 `README.md`，本文件是唯一的行为准则来源。

## 核心铁律

1. **ASR 转写稿是唯一的真理来源。** 规则只能来自"AI 输出 vs 真人朗读（ASR 转写）"的真实差异。禁止凭空想象"人大概会这么说"然后加规则。
2. **归因，不改个案。** 从差异中提炼的是"这类结构如何处理"的通用规律，禁止只把单个句子改顺就完事。
3. **每条规则必须可追溯。** 修改 `references/` 下任一模型规则文件的同一轮，必须在 `CHANGELOG.md` 追加归因日志（差异类型 → 规则改动 → 来源校准记录编号），条目中注明模型名。没有日志的规则改动视为无效。
4. **改完必须回归。** 每次修改 `references/` 下任一模型规则文件后，必须用该模型：
   - 用 `corpus/` 全部输入跑一遍，检查各题材无退化；
   - 用 `regression/` 全部负样本跑一遍，检查旧问题无复发。
5. **bad case 必须入库。** 迭代中发现的任何"不口语"输出，必须按 `regression/TEMPLATE.md` 的格式存入负样本库，不允许"这次记住就好"。

## 目录使用规则

| 场景 | 写到哪 | 格式 |
|------|--------|------|
| 提炼出的改写规则 | `references/` 下对应模型的规则文件（如 `references/kimi-k3.md`） | 按现有分节结构追加/修改，只动当前迭代的那个模型 |
| 规则归因日志 | `CHANGELOG.md` | 按文件头部的条目格式，新条目在最上方 |
| 每轮校准的完整记录 | `calibration/YYYYMMDD-NN.md` | 按 `calibration/TEMPLATE.md` |
| 负样本（bad case） | `regression/cases/NNN-简短描述.md` | 按 `regression/TEMPLATE.md` |
| 回归结果归档 | `regression/results/YYYYMMDD-模型-版本.md` | 按 `regression/results/TEMPLATE.md`，执行规程见 `regression/RUNBOOK.md` |
| 差异率汇总 | `calibration/metrics.md` | 追加一行，数值与当轮校准记录一致 |
| A/B 盲测记录 | `ab-tests/YYYYMMDD-NN.md` | 按 `ab-tests/TEMPLATE.md`，执行规程见 `ab-tests/RUNBOOK.md` |
| A/B 盲测汇总 | `ab-tests/summary.md` | 追加一行，累计胜率看趋势 |
| 新的测试输入 | `corpus/` 对应题材文件 | 追加到文件末尾，标注来源 |

- 编号 `NN`/`NNN` 从现有最大编号递增，不允许跳号或复用。
- 禁止修改已归档的校准记录和负样本（它们是历史事实）；发现错误时在 `CHANGELOG.md` 里说明，而不是改历史。

## 规则写作要求（改 `references/` 下的模型规则文件时）

- 规则要写成**可判定的指令**（"遇到 X 结构时做 Y"），不要写成模糊的期望（"尽量自然一点"）。
- 每条规则尽量附带一个正例或反例，例子必须来自真实校准记录，标注来源编号。
- 通用规则写进主体；因人而异的分歧写法收进「风格开关」一节，默认值明确标注。
- 发现某条规则连续多轮从未被触发，在 `CHANGELOG.md` 提议删除并说明理由，由人确认后再删。

## 迭代流程（AI 侧职责）

1. 按当前模型加载 `references/` 下对应规则文件，用它改写指定输入，输出版本号（模型名 + 规则文件版本 + 日期）。
2. 拿到 ASR 转写版后，逐条 diff，按停顿/语气/标点/冗余词/即兴改写五类归因。
3. 完整记录写入 `calibration/`，提炼的规则改动写入该模型自己的规则文件（不动其他模型的文件），归因写入 `CHANGELOG.md`（注明模型名）。
4. 本轮新发现的 bad case 存入 `regression/`。
5. 用当前模型跑 `corpus/` + `regression/` 回归（步骤和判定标准见 `regression/RUNBOOK.md`），结果按 `regression/results/TEMPLATE.md` 归档；有退化就先修复再收尾。
6. 统计本轮差异率（改动处数量 / 总句数），追加到校准记录中，并在 `calibration/metrics.md` 汇总表加一行。

## 禁止事项

- 禁止在没有真实校准数据的情况下新增规则。
- 禁止跳过回归直接宣称"已收敛"。
- 禁止为了让 diff 变少而改 ASR 转写稿或测试输入。
- 禁止把模型规则文件无限加长：新增规则时检查是否能并入已有规则。
- 禁止跨模型同步规则：一个模型上验证的规律，不直接写进另一个模型的文件。
