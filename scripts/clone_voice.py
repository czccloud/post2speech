#!/usr/bin/env python3
"""MiniMax 声音克隆：上传参考音频 → 复刻音色 → 得到可复用的 voice_id。

用法：
    python scripts/clone_voice.py ../voice-sample.mp3 --voice-id my-voice
    # 之后把 my-voice 传给 tts.py 的 --voice 即可

参考音频要求：mp3 / m4a / wav，10 秒到 5 分钟，不超过 20MB。
克隆出的 voice_id 与账号绑定，可重复使用，不用每次克隆。
"""

import argparse
import os
import sys

try:
    import requests
except ImportError:
    sys.exit("缺少依赖 requests，请先运行：pip install requests")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tts import find_api_key, key_help_message  # noqa: E402

UPLOAD_PATH = "/v1/files/upload"
CLONE_PATH = "/v1/voice_clone"

ENDPOINTS = {
    "cn": "https://api.minimaxi.com",
    "intl": "https://api.minimax.io",
}


def main():
    parser = argparse.ArgumentParser(description="MiniMax 声音克隆：参考音频 → voice_id")
    parser.add_argument("audio", help="参考音频文件（mp3/m4a/wav，10 秒–5 分钟）")
    parser.add_argument("--voice-id", required=True,
                        help="给克隆音色起的名字（之后传给 tts.py --voice）")
    parser.add_argument("--endpoint", choices=sorted(ENDPOINTS), default="cn",
                        help="接口端点：cn 国内（默认）/ intl 国际")
    args = parser.parse_args()

    api_key, source = find_api_key()
    if not api_key:
        sys.exit(key_help_message())
    print(f"使用 key 来源：{source}", file=sys.stderr)

    if not os.path.isfile(args.audio):
        sys.exit(f"文件不存在：{args.audio}")
    size = os.path.getsize(args.audio)
    if size > 20 * 1024 * 1024:
        sys.exit(f"文件超过 20MB 限制：{size} 字节")
    if os.path.splitext(args.audio)[1].lower() not in (".mp3", ".m4a", ".wav"):
        sys.exit("格式不接受：克隆接口只收 mp3 / m4a / wav（aac 请先转码）")

    base = ENDPOINTS[args.endpoint]
    headers = {"Authorization": f"Bearer {api_key}"}

    print("上传参考音频……", file=sys.stderr)
    with open(args.audio, "rb") as f:
        resp = requests.post(
            base + UPLOAD_PATH,
            headers=headers,
            data={"purpose": "voice_clone"},
            files={"file": (os.path.basename(args.audio), f)},
            timeout=300,
        )
    resp.raise_for_status()
    up = resp.json()
    if up.get("base_resp", {}).get("status_code", 0) != 0:
        sys.exit(f"上传失败：{up.get('base_resp')}")
    file_id = up["file"]["file_id"]
    print(f"上传成功，file_id={file_id}", file=sys.stderr)

    print(f"复刻音色 {args.voice_id} ……", file=sys.stderr)
    resp = requests.post(
        base + CLONE_PATH,
        headers={**headers, "Content-Type": "application/json"},
        json={"file_id": file_id, "voice_id": args.voice_id},
        timeout=300,
    )
    resp.raise_for_status()
    clone = resp.json()
    base_resp = clone.get("base_resp", {})
    if base_resp.get("status_code", 0) != 0:
        sys.exit(f"克隆失败 [{base_resp.get('status_code')}] {base_resp.get('status_msg')}")

    print(f"克隆完成。voice_id：{args.voice_id}")
    print(f"试听：python scripts/tts.py demo/B-oralizer输出.txt -o /tmp/test.mp3 --voice {args.voice_id}")


if __name__ == "__main__":
    main()
