# demo/ — 可听对比样本

三段音频（同一音色、同一语速，只有文本不同）：

| 文件 | 内容 |
|------|------|
| `A-原始书面语.mp3` | `A-原始书面语.txt` 直接喂 TTS |
| `B-oralizer输出.mp3` | `B-oralizer输出.txt`（经 `references/core.md` 规则改写）喂 TTS |
| `C-真人朗读.mp3` | 真人自然朗读 B 的录音（可选但强烈建议），配 `C-真人朗读-ASR转写.txt` 作为 ground truth 实物证据 |

## 重新生成

音频不进 git 默认忽略列表（`lab/demo/*.mp3` 已放行提交）。生成方式：

```bash
# key 放在项目目录的上一级，如 ../.env 里写 MINIMAX_API_KEY=...
# 可选：先克隆自己的音色（10 秒–5 分钟参考音频，只需做一次，voice_id 可复用）
python lab/scripts/clone_voice.py ../voice-sample.mp3 --voice-id oralizer-owner
# 生成对比样本（--voice 不传则用默认预制音色）
python lab/scripts/tts.py "lab/demo/A-原始书面语.txt" -o "lab/demo/A-原始书面语.mp3" --voice oralizer-owner
python lab/scripts/tts.py "lab/demo/B-oralizer输出.txt" -o "lab/demo/B-oralizer输出.mp3" --voice oralizer-owner
```

C 段需要人参与：自然朗读 B 文本并录音（允许即兴修改，改得顺嘴就是对），录音转 mp3 后放入本目录；若做了 ASR 转写，把转写稿存为 `C-真人朗读-ASR转写.txt`，它可以直接作为一轮校准的输入（见 `AGENTS.md` 迭代流程）。
