# oralizer

[English README](README_EN.md)

把书面语改写成**读出来像人说话**的文字。不是"读起来通顺"，是有自然的停顿、语气、节奏，没有书面语的生硬感——一个纯 Markdown、零依赖的 Agent Skill。

## 安装

```bash
# 装到当前项目（团队共享、跟着项目走）
npx skills add leaveWhite9088/oralizer

# 或装到全局（所有项目都能用）
npx skills add leaveWhite9088/oralizer --global
```

也可以手动安装：`git clone https://github.com/leaveWhite9088/oralizer` 到你的 agent 的 skills 目录（项目级 `.agents/skills/` 或全局 `~/.agents/skills/`）。

## 听一下差别

同一段文字，同一音色同一语速，只有文本不同。先听后看，或者边看边听：

**A · 原始书面语**（[下载 mp3](lab/demo/A-原始书面语.mp3)）



https://github.com/user-attachments/assets/e14cf8aa-4bf2-4545-8a4c-8bedea4720f7



> 在数字化转型的浪潮中，知识管理工具已成为现代人不可或缺的效率利器。然而值得注意的是，大多数用户仅仅使用了这些工具不到百分之十的功能。本文将深入探讨如何充分发挥知识管理工具的潜力，首先介绍核心理念，其次讲解实践方法，最后给出行动建议，希望能帮助你构建属于自己的第二大脑。

**B · oralizer 改写后**（[下载 mp3](lab/demo/B-oralizer输出.mp3)）



https://github.com/user-attachments/assets/9fdef488-17bd-4cef-83b0-d319aadfcf83



> 知识管理工具现在基本人手一个，但大多数人用它，用到的功能连 10% 都不到。那怎么才能把它的潜力用出来呢？这篇分三块来讲，核心理念，实践方法，还有几条能直接照做的建议，目标就是帮你搭一个自己的第二大脑。第二大脑听着玄，说白了就是在脑子外面，再给自己攒一个知识库。

## 用法

装好后对 agent 说：

```
/oralizer 把这篇文章改写成适合朗读的口播稿：<粘贴文本>
```

 Skill 零依赖、不需要任何 API key。`lab/scripts/tts.py` 是可选的辅助工具（用 MiniMax TTS 把文本转成音频，生成样本、快速筛查用），不在 Skill 依赖链上；key 放在项目目录的上一级（`../.env`），详见 [lab/demo/README.md](lab/demo/README.md)。

## 为什么它有效

规则不是拍脑袋写的，是拿真人朗读**校准**出来的：AI 改写 → 真人自然朗读、用手机语音转文字记下实际读出来的样子 → 逐条对比"AI 写的 vs 人实际读的" → 把差异归因成规则。每条规则都能追溯到一次真实差异（见 [CHANGELOG.md](CHANGELOG.md) 和 [lab/calibration/](lab/calibration/)）。ASR 转写稿是外部客观锚点，不是"用 AI 审 AI"。完整的校准循环、测试方法和收敛标准见 [lab/docs/methodology.md](lab/docs/methodology.md)。

## 定制你自己的 profile

共性规则在 `references/core.md`，所有人共享；个人偏好（句长、口头禅、停顿节奏、数字写法）放在 `profiles/<name>.md`，几行到几十行就够。从 [profiles/default.md](profiles/default.md) 复制一份改起。

想让自己的 profile 真正贴合你的嘴，最准的输入是**一段你自己朗读的语音转文字稿**：随便挑一段文字，打开手机便签或输入法的语音输入，自然地读出来让它实时转写，再和你的原文对比，你顺口改掉的地方就是你的个人口语特征，写进 profile。这比给文字样本更准——文字样本只能看出你怎么写，转写稿能看出你怎么说。

## 如何贡献

最缺的不是代码，是校准数据。你可以：

1. 装上 Skill，用它改写你的内容，把"读着还是别扭"的句子发成 issue；
2. 按[校准循环](lab/docs/methodology.md)跑一轮（朗读 + ASR + diff），把记录按 `lab/calibration/TEMPLATE.md` 提交；
3. 提交的规则改动必须能追溯到真实差异，详见 `AGENTS.md` 的守则。

当前为 v0.x，持续校准中——规则每天都在变厚，欢迎来玩。
