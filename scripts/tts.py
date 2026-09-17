#!/usr/bin/env python3
"""MiniMax TTS 命令行工具：把文本转成中文语音 mp3。

用法：
    python scripts/tts.py input.txt -o out.mp3
    python scripts/tts.py input.txt -o out.mp3 --model speech-2.8-hd --voice male-qn-qingse --speed 1.0
    python scripts/tts.py demo/*.txt -o demo/          # 批量，输出目录

Key 读取顺序：环境变量 MINIMAX_API_KEY → ../.env → ../.env.local → ../keys/minimax.env
（key 放在项目目录的上一级，不进仓库。）

注意：本脚本只是辅助工具（生成样本、快速筛查），不在 skill 的依赖链上；
Skill 本身是纯 Markdown，不需要任何 key。
"""

import argparse
import os
import sys

try:
    import requests
except ImportError:
    sys.exit("缺少依赖 requests，请先运行：pip install requests")

ENDPOINTS = {
    "cn": "https://api.minimaxi.com/v1/t2a_v2",
    "intl": "https://api.minimax.io/v1/t2a_v2",
}

# 不同订阅计划支持的模型不同，按序自动回退
MODEL_CANDIDATES = ["speech-2.8-hd", "speech-2.8-turbo", "speech-2.6-hd", "speech-2.6-turbo"]

DEFAULT_VOICE = "male-qn-qingse"


def find_api_key():
    """按约定顺序查找 API key，返回 (key, source)；找不到返回 (None, None)。"""
    key = os.environ.get("MINIMAX_API_KEY")
    if key:
        return key.strip(), "环境变量 MINIMAX_API_KEY"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    parent_dir = os.path.dirname(project_dir)
    for rel in (".env", ".env.local", os.path.join("keys", "minimax.env")):
        path = os.path.join(parent_dir, rel)
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("MINIMAX_API_KEY="):
                    value = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if value:
                        return value, path
    return None, None


def key_help_message():
    return (
        "找不到 MiniMax API key。请按以下任一方式配置：\n"
        "  1. 设置环境变量 MINIMAX_API_KEY\n"
        "  2. 在本项目目录的上一级创建 .env，写入一行：MINIMAX_API_KEY=你的key\n"
        "     （也可以是上一级的 .env.local 或 keys/minimax.env）\n"
        "key 申请地址：https://www.minimaxi.com/ （平台 → 接口密钥）\n"
        "注意：key 放在项目目录的上一级，不要放进本仓库。"
    )


def synthesize(text, api_key, model, voice, speed, endpoint):
    payload = {
        "model": model,
        "text": text,
        "stream": False,
        "output_format": "hex",
        "voice_setting": {
            "voice_id": voice,
            "speed": speed,
            "vol": 1.0,
            "pitch": 0,
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1,
        },
    }
    resp = requests.post(
        endpoint,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    base = data.get("base_resp", {})
    if base.get("status_code", 0) != 0:
        raise RuntimeError(f"API 返回错误 [{base.get('status_code')}] {base.get('status_msg')}")
    audio_hex = data.get("data", {}).get("audio")
    if not audio_hex:
        raise RuntimeError("API 响应中没有音频数据：" + str(data)[:500])
    return bytes.fromhex(audio_hex)


def synthesize_with_fallback(text, api_key, model, voice, speed, endpoint):
    """遇到 'token plan not support model' 时按候选列表自动回退。"""
    models = [model] if model else MODEL_CANDIDATES
    last_err = None
    for i, m in enumerate(models):
        try:
            audio = synthesize(text, api_key, m, voice, speed, endpoint)
            if i > 0:
                print(f"  （已自动切换到模型 {m}）", file=sys.stderr)
            return audio, m
        except RuntimeError as e:
            last_err = e
            if "not support model" in str(e) and not model:
                print(f"  模型 {m} 不可用（{e}），尝试下一个……", file=sys.stderr)
                continue
            raise
    raise last_err


def main():
    parser = argparse.ArgumentParser(description="MiniMax TTS：文本转中文语音 mp3")
    parser.add_argument("inputs", nargs="+", help="输入文本文件（可多个）")
    parser.add_argument("-o", "--output", required=True,
                        help="输出 mp3 路径；多个输入时为输出目录")
    parser.add_argument("--model", default=None,
                        help=f"TTS 模型名（默认按候选列表自动探测：{', '.join(MODEL_CANDIDATES)}）")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help=f"音色（默认 {DEFAULT_VOICE}）")
    parser.add_argument("--speed", type=float, default=1.0, help="语速（默认 1.0）")
    parser.add_argument("--endpoint", choices=sorted(ENDPOINTS), default="cn",
                        help="接口端点：cn 国内（默认）/ intl 国际")
    args = parser.parse_args()

    api_key, source = find_api_key()
    if not api_key:
        sys.exit(key_help_message())
    print(f"使用 key 来源：{source}", file=sys.stderr)

    multi = len(args.inputs) > 1
    if multi:
        os.makedirs(args.output, exist_ok=True)

    for input_path in args.inputs:
        with open(input_path, encoding="utf-8") as f:
            text = f.read().strip()
        if not text:
            print(f"跳过空文件：{input_path}", file=sys.stderr)
            continue
        if multi:
            out_path = os.path.join(
                args.output, os.path.splitext(os.path.basename(input_path))[0] + ".mp3")
        else:
            out_path = args.output
        try:
            audio, used_model = synthesize_with_fallback(
                text, api_key, args.model, args.voice, args.speed, ENDPOINTS[args.endpoint])
        except RuntimeError as e:
            sys.exit(f"合成失败（{input_path}）：{e}\n"
                     f"提示：模型名可用 --model 指定，当前候选 {MODEL_CANDIDATES}")
        with open(out_path, "wb") as f:
            f.write(audio)
        print(f"已生成 {out_path}（模型 {used_model}，{len(audio)} 字节）")


if __name__ == "__main__":
    main()
