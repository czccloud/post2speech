---
name: oralizer
description: Use when 需要把中文书面文字（帖子、文章、讲稿、汇报、回答）改写成"读出来像人说话"的口语文本，或觉得自己的中文开始有 AI 味、翻译腔、提纲腔。把输出整理成像说话一样自然的中文：按气息断句、话题化停顿、语气词进句中、保留毛边、先结论后细节、禁 AI 腔、禁互联网黑话、禁排比对仗。凡是"这段文字会被用户读出来或念出来"的中文输出，动笔前加载本 skill 过一遍规范。
---

# oralizer — 把书面语改写成"读出来像人说话"的文字

本 skill 的规则主体只有一份：`references/core.md`（通用口语化改写规则，用真人朗读的 ASR 转写稿逐轮校准出来）。规则对齐的是"人怎么说话"，不随模型变化，因此**不再按模型分文件**。

## 使用方式

1. 加载 `references/core.md`，之后所有口语化输出遵守该文件的全部规范。
2. 如果用户在 `profiles/` 下指定了个人 profile（如 `profiles/default.md`），在 core 之上叠加该文件——profile 只覆盖个人偏好（句长、口头禅、数字写法等），条目与 core 冲突时以 profile 为准。
3. 仅当你明确知道当前模型在 `references/overlays/` 下有对应文件、且该文件声明了与 core 的实测分歧时，才叠加对应 overlay；否则不用管 overlays。

## 目录说明

- `references/core.md`：规则主体，所有人共享，社区共同打磨。
- `references/overlays/<model>.md`：某模型相对 core 的实测偏离补丁（有校准记录佐证才写，几行以内）。
- `references/legacy/`：2026-09-16 之前的分模型规则文件（GLM 5.3 v1.3、Kimi K3 v1.8），保留作历史参照，不再迭代。
- `profiles/`：个人风格层，几行到几十行，见 `profiles/default.md`。

## 迭代约定（改规则时必读）

- 规则改动默认只发生在 `references/core.md`；只有带校准记录佐证的模型特异性差异才写进对应 overlay。**禁止凭想象新增规则**：每条规则必须能追溯到一次"AI 输出 vs 真人朗读 ASR 转写"的真实差异（见根目录 `AGENTS.md`）。
- 每次迭代开头报版本号：规则文件名 + 版本 + 日期（如"core，v1.1，2026-09-20"）。
- 归因日志统一记在 `CHANGELOG.md`，条目里注明改了哪个文件、源自哪次校准记录。
- 完整迭代流程（校准 → 归因 → 写回 → 回归 → 差异率）见根目录 `AGENTS.md` 与 `docs/methodology.md`。
