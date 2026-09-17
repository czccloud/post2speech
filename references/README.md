# references/ — 规则文件

口语化改写规则的存放处。Skill 运行时只需要 `core.md`，其余两个目录是治理与历史结构。

## 结构与加载规则

| 文件/目录 | 作用 | 谁加载 |
|-----------|------|--------|
| `core.md` | 规则主体，所有模型共享（当前 v1.0，2026-09-16 由 GLM 5.3 与 Kimi K3 两份分模型规则机械合并而成） | 所有模型默认只加载它 |
| `overlays/<model>.md` | 某模型相对 core 的**实测偏离**补丁，有校准记录佐证才写，几行以内 | 仅当当前模型有对应文件、且文件里声明了与 core 的实测分歧时才叠加 |
| `legacy/` | 2026-09-16 之前的分模型规则文件（glm-5.3 v1.3、kimi-k3 v1.8），冻结不再迭代 | 不加载，仅供查阅 |

为什么规则主体只有一份：本项目对齐的 ground truth 是"人怎么说话"（真人朗读的 ASR 转写稿），不随模型变化。模型特异性差异默认不存在，除非被校准记录证明——证明了才进 overlay。决策与理由见根目录 `CHANGELOG.md` 2026-09-16 条目。

## 为什么 legacy/ 不能删

legacy/ 不是待清理的旧文件，是"可追溯"这条核心原则的实物证据：

1. **归档记录的引用还活着**。`calibration/`、`regression/cases/`、`ab-tests/` 里有几十处引用写着 `references/kimi-k3.md` 第 X 条、`references/glm-5.3.md` v1.3——这些是历史事实，按 `AGENTS.md` 不许改。legacy/ 在，这些引用就查得到原文；删了只剩 CHANGELOG 的转述。
2. **core.md 的来源凭证**。core.md 头部声明由 legacy 两个版本机械合并而来，合并是否忠实靠 legacy 可对照。
3. **overlay 的判据基线**。将来做"同一份 core 喂多个模型"的对比实验时，legacy 是现成的对照组。

可以安全删除的时机：core.md 跑过多轮真实校准、legacy 条文全部被覆盖或被证明作废之后——届时在 `CHANGELOG.md` 记一条再删。

## 修改规则时

流程与守则见根目录 `AGENTS.md`，要点：规则只能来自"AI 输出 vs 真人朗读 ASR 转写"的真实差异；改动默认只进 `core.md`；同一轮必须在 `CHANGELOG.md` 记归因日志；改完按 `regression/RUNBOOK.md` 跑回归。
