#!/usr/bin/env python3
"""OpenAI gpt-image-1 text-to-image 调用脚本（3 次指数退避重试）。

用法：
    python3 generate_image_openai.py \
        --prompt "the image prompt" \
        --size "1536x1024" \
        --quality "high" \
        --output "/path/to/output.png"

API Key 从环境变量 OPENAI_API_KEY 读取。

设计要点：
  - 无 --style 参数（OpenAI gpt-image-1 没有 style 预设，风格通过 prompt 描述）
  - size 用具体像素值（1024x1024 / 1024x1536 / 1536x1024 / auto）
  - quality 显式选 low / medium / high / auto（high 是品牌封面主力品质）
  - 返回 base64 数据，本地解码写盘
  - 3 次指数退避（2/4/8s），重试 5xx + 429 + 网络错误
"""

import argparse
import base64
import json
import os
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


RETRIES = 3
BACKOFF = [2, 4, 8]  # seconds
RETRYABLE_STATUS = {429, 500, 502, 503, 504}
OPENAI_ENDPOINT = "https://api.openai.com/v1/images/generations"

VALID_SIZES = {"1024x1024", "1024x1536", "1536x1024", "auto"}
VALID_QUALITIES = {"low", "medium", "high", "auto"}
VALID_FORMATS = {"png", "jpeg", "webp"}


def call_openai(payload: dict, api_key: str) -> dict:
    """Single HTTP call to OpenAI image API. Returns parsed JSON or raises."""
    req = Request(
        OPENAI_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    # high quality 可能要 30-60 秒
    with urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def generate_with_retry(payload: dict, api_key: str) -> dict:
    """Call OpenAI with 3-attempt exponential backoff."""
    last_err = None
    for attempt in range(RETRIES):
        try:
            return call_openai(payload, api_key)
        except HTTPError as e:
            try:
                err_body = e.read().decode("utf-8")[:300]
            except Exception:
                err_body = ""
            last_err = f"HTTP {e.code}: {e.reason} | body: {err_body}"
            if e.code in RETRYABLE_STATUS and attempt < RETRIES - 1:
                wait = BACKOFF[attempt]
                print(
                    f"⚠️  attempt {attempt + 1}/{RETRIES} failed ({last_err}), retry in {wait}s...",
                    file=sys.stderr,
                )
                time.sleep(wait)
                continue
            raise RuntimeError(f"Non-retryable HTTP error: {last_err}") from e
        except (URLError, TimeoutError, json.JSONDecodeError) as e:
            last_err = f"{type(e).__name__}: {e}"
            if attempt < RETRIES - 1:
                wait = BACKOFF[attempt]
                print(
                    f"⚠️  attempt {attempt + 1}/{RETRIES} failed ({last_err}), retry in {wait}s...",
                    file=sys.stderr,
                )
                time.sleep(wait)
                continue
            raise RuntimeError(f"Network error after {RETRIES} attempts: {last_err}") from e
    raise RuntimeError(f"All {RETRIES} attempts failed. Last error: {last_err}")


def generate_image(prompt: str, size: str, quality: str, output_format: str, output_path: str, api_key: str) -> str:
    payload = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": quality,
        "output_format": output_format,
    }

    result = generate_with_retry(payload, api_key)
    b64_data = result["data"][0]["b64_json"]
    img_bytes = base64.b64decode(b64_data)

    # Ensure output extension matches the actual output_format
    base, requested_ext = os.path.splitext(output_path)
    requested_ext = requested_ext.lower().lstrip(".")
    if requested_ext != output_format:
        output_path = f"{base}.{output_format}"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(img_bytes)

    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate image via OpenAI gpt-image-1 (with retry)")
    parser.add_argument("--prompt", required=True, help="Image generation prompt (English)")
    parser.add_argument(
        "--size",
        default="1536x1024",
        choices=sorted(VALID_SIZES),
        help="Image size: 1024x1024 (square) / 1536x1024 (landscape 3:2) / 1024x1536 (portrait 2:3) / auto",
    )
    parser.add_argument(
        "--quality",
        default="high",
        choices=sorted(VALID_QUALITIES),
        help="Image quality tier: low / medium / high / auto. Cost scales (high ~$0.17/image)",
    )
    parser.add_argument(
        "--output-format",
        default="png",
        choices=sorted(VALID_FORMATS),
        help="Output format: png (default) / jpeg / webp",
    )
    parser.add_argument("--output", required=True, help="Output file path (absolute)")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable not set.", file=sys.stderr)
        print('Add to ~/.zshrc: export OPENAI_API_KEY="your-key"', file=sys.stderr)
        return 1

    try:
        path = generate_image(
            prompt=args.prompt,
            size=args.size,
            quality=args.quality,
            output_format=args.output_format,
            output_path=args.output,
            api_key=api_key,
        )
        print(f"OK: {path}")
        return 0
    except Exception as exc:
        truncated_prompt = (args.prompt[:80] + "...") if len(args.prompt) > 80 else args.prompt
        print("ERROR: 生成失败", file=sys.stderr)
        print(f"  prompt: {truncated_prompt}", file=sys.stderr)
        print(f"  size: {args.size}", file=sys.stderr)
        print(f"  quality: {args.quality}", file=sys.stderr)
        print(f"  attempts: {RETRIES}", file=sys.stderr)
        print(f"  last_error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
