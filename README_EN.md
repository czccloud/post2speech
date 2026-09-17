# oralizer

[中文版 README](README.md)

**oralizer** rewrites written Chinese into text that *sounds like a real person talking* when read aloud — natural pauses, tone particles, uneven sentence rhythm, no AI-flavored formality. It is a pure-Markdown, zero-dependency agent skill.

## Install

```bash
# Into the current project (shared with the team, travels with the repo)
npx skills add leaveWhite9088/oralizer

# Or globally (available in every project)
npx skills add leaveWhite9088/oralizer --global
```

Or manually: `git clone https://github.com/leaveWhite9088/oralizer` into your agent's skills directory (project-level `.agents/skills/` or global `~/.agents/skills/`).

## Hear the difference

Same passage, same TTS voice and speed — only the text differs:

- **A · Original written Chinese** — [▶ listen](demo/A-原始书面语.mp3) ([text](demo/A-原始书面语.txt))
- **B · Rewritten by oralizer** — [▶ listen](demo/B-oralizer输出.mp3) ([text](demo/B-oralizer输出.txt))

## Usage

```
/oralizer rewrite this article into a speakable script: <paste text>
```

The skill itself is pure Markdown and needs no API key. `scripts/tts.py` is an optional helper (MiniMax TTS) for generating samples and quick screening — it is not in the skill's dependency chain.

## Why it works

The rules aren't invented — they're **calibrated against real human read-aloud recordings**: AI rewrites a passage → a human reads it aloud naturally (recording) → ASR transcribes what's actually said → every diff between "what the AI wrote" and "what the human said" is attributed to a missing rule. Each rule traces back to a real recorded difference (see [CHANGELOG.md](CHANGELOG.md) and [calibration/](calibration/)). The ASR transcript is an external objective anchor — not "an AI judging another AI". Full methodology: [docs/methodology.md](docs/methodology.md).

Most "de-AI" tools target English fingerprints (em dashes, triads) and validate with LLM self-review. Chinese AI-flavored writing is a different beast, and oralizer is built for it.

## Personalization

Shared rules live in `references/core.md`. Personal preferences (sentence length, verbal tics, pause rhythm, number style) go in `profiles/<name>.md` — a few lines to a few dozen. Start from [profiles/default.md](profiles/default.md). The best calibration input is an ASR transcript of *your own* read-aloud: it captures how you actually speak, not how you write.

## Contributing

Calibration data is what we need most:

1. Install the skill, rewrite your content, and file issues with sentences that still read awkwardly aloud;
2. Run one calibration round (read aloud + ASR + diff) and submit per `calibration/TEMPLATE.md`;
3. Every rule change must trace to a real recorded difference — see `AGENTS.md`.

Currently v0.x, under continuous calibration.
