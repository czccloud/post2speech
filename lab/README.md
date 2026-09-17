# lab/ — 治理区（迭代的日常工作区）

这里装的是"规则是怎么被校准和检验的"全部 apparatus，**运行时不会被加载**。装 skill 后 agent 只读根目录的 `SKILL.md` + `references/` + `profiles/`；这里的文件只在迭代、审计、教学时打开。

| 子目录 | 内容 |
|--------|------|
| `calibration/` | 每轮朗读校准的完整记录 + 差异率汇总（metrics.md） |
| `corpus/` | 固定测试输入集（多题材，回归用） |
| `regression/` | 负样本库（cases/）+ 回归结果归档（results/）+ 执行规程（RUNBOOK.md） |
| `ab-tests/` | A/B 盲测记录与胜率汇总 |
| `docs/` | 方法论（methodology.md） |
| `demo/` | 可听对比样本（音频 + 文本对照） |
| `scripts/` | 可选工具（MiniMax TTS、声音克隆），不在 skill 依赖链上 |

## 旧路径映射

2026-09-17 起，上述目录从仓库根迁入 `lab/`（决策见根目录 `CHANGELOG.md` 当日条目）。**此日期之前归档的记录**（校准记录、负样本、回归结果、盲测记录）中写的 `calibration/...`、`corpus/...`、`regression/...`、`ab-tests/...`、`docs/...`、`demo/...`、`scripts/...` 等无前缀路径，一律对应 `lab/` 下的同名路径。归档记录是历史事实，不批量改写。

## 改动纪律

- 本区是日常工作区：加校准记录、负样本、回归结果、题材输入都是常规操作，按各子目录的 README/TEMPLATE/RUNBOOK 执行。
- 但只要迭代结论要落进**运行时区**（`references/`、`profiles/`、`SKILL.md`），就必须走根目录 `AGENTS.md` 的完整流程（归因 + CHANGELOG + 回归）。
