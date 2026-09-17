# 传播物料

## Elevator pitch（30 秒）

**中文版**

oralizer 是一个把书面语改写成"读出来像人说话"的 Agent Skill。市面上的"去 AI 味"工具清的是英文指纹，规则来自模型自查；oralizer 专攻中文，而且规则不是拍脑袋写的——每一条都校准自真人朗读：让人把 AI 的改写稿自然读出来、录音、ASR 转写，逐条对比"AI 写的 vs 人实际读的"，差异归因成规则。纯 Markdown 零依赖，`npx skills add leaveWhite9088/oralizer` 装上就能用。

**English version**

oralizer is an agent skill that rewrites written Chinese into text that sounds like a real person talking when read aloud. Most "de-AI" tools target English fingerprints and validate with LLM self-review. oralizer is built for Chinese, and every rule is calibrated against real human read-aloud recordings: people read the AI's rewrite naturally, we transcribe with ASR, diff "what the AI wrote vs. what the human actually said", and turn each diff into a rule. Pure Markdown, zero dependencies — `npx skills add leaveWhite9088/oralizer` and it works.

## Before / After 文本对照

**原文（典型 AI 书面腔）**

> 在数字化转型的浪潮中，知识管理工具已成为现代人不可或缺的效率利器。然而值得注意的是，大多数用户仅仅使用了这些工具不到百分之十的功能。本文将深入探讨如何充分发挥知识管理工具的潜力，首先介绍核心理念，其次讲解实践方法，最后给出行动建议，希望能帮助你构建属于自己的第二大脑。

**oralizer 改写后**

> 知识管理工具现在基本人手一个，但大多数人用它，用到的功能连 10% 都不到。那怎么才能把它的潜力用出来呢？这篇分三块来讲，核心理念，实践方法，还有几条能直接照做的建议，目标就是帮你搭一个自己的第二大脑。第二大脑听着玄，说白了就是在脑子外面，再给自己攒一个知识库。

看出来的差异只是表面，读出来才是本体：原版"在数字化转型的浪潮中"一开口就是稿子腔，"首先、其次、最后"念着像念提纲；改写版先把扎眼的事实扔出来，三块内容顺着嘴报完，黑话"第二大脑"按住了用大白话解释——而且事实和数字一个没动（原文说"不到 10% 的功能"，改写版不会说成"不到一成的用户"）。真人照着念改写版，几乎不用改口。可听对照见 [lab/demo/](lab/demo/)。

## 短文选题（备写）

- 《为什么"去 AI 味"的工具都搞不定中文》：英文指纹（em dash、三连排比）在中文里根本不出现，中文的 AI 味是另一套——提纲腔、名词化、句句工整。而验证"像不像人话"，最硬的锚点不是再找一个 AI 来评，是让人读出来、用 ASR 记下来。
- 《用录音校准一个写作 Skill》：朗读校准循环的完整方法——生成、朗读、ASR、diff 归因、回写规则、回归，以及为什么"一个人校准出来的 Skill 只适合自己"。
