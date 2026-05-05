#!/usr/bin/env python3
"""fal.ai Recraft V3 text-to-image 调用脚本（V2：3 次指数退避重试）。

用法：
    python3 generate_image.py \
        --prompt "the image prompt" \
        --style "digital_illustration" \
        --image-size "landscape_4_3" \
        --output "/path/to/output.png"

API Key 从环境变量 FAL_API_KEY 读取。
"""

import argparse
import json
import os
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen, urlretrieve


KNOWN_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif"}


RETRIES = 3
BACKOFF = [2, 4, 8]  # seconds
RETRYABLE_STATUS = {429, 500, 502, 503, 504}
FAL_ENDPOINT = "https://fal.run/fal-ai/recraft/v3/text-to-image"


def call_fal(payload: dict, api_key: str) -> dict:
    """Single HTTP call to fal.ai. Returns parsed JSON or raises."""
    req = Request(
        FAL_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def generate_with_retry(payload: dict, api_key: str) -> dict:
    """Call fal.ai with 3-attempt exponential backoff.

    Retries on: HTTP 429/5xx, URLError, TimeoutError, JSONDecodeError.
    Fails fast on: 4xx (non-429).
    """
    last_err = None
    for attempt in range(RETRIES):
        try:
            return call_fal(payload, api_key)
        except HTTPError as e:
            last_err = f"HTTP {e.code}: {e.reason}"
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


def generate_image(prompt: str, style: str, image_size: str, output_path: str, api_key: str) -> str:
    payload = {
        "prompt": prompt,
        "style": style,
        "image_size": image_size,
        "num_images": 1,
        "enable_safety_checker": True,
    }

    result = generate_with_retry(payload, api_key)
    image_url = result["images"][0]["url"]

    url_ext = os.path.splitext(urlparse(image_url).path)[1].lower()
    requested_ext = os.path.splitext(output_path)[1].lower()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 按 URL 真实扩展名改写 output（API 有时返回 WebP 而调用方传的是 .png）
    if url_ext in KNOWN_EXTS and url_ext != requested_ext:
        base, _ = os.path.splitext(output_path)
        output_path = base + url_ext
    urlretrieve(image_url, output_path)
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate image via fal.ai Recraft V3 (with retry)")
    parser.add_argument("--prompt", required=True, help="Image generation prompt (English)")
    parser.add_argument(
        "--style",
        default="digital_illustration",
        help="Recraft V3 style parameter (see references/style-options.md, e.g. digital_illustration, digital_illustration/hand_drawn, realistic_image/natural_light)",
    )
    parser.add_argument(
        "--image-size",
        default="landscape_4_3",
        help="Image size (e.g., landscape_4_3, square_hd, portrait_4_3)",
    )
    parser.add_argument("--output", required=True, help="Output file path (absolute)")
    args = parser.parse_args()

    api_key = os.environ.get("FAL_API_KEY", "")
    if not api_key:
        print("ERROR: FAL_API_KEY environment variable not set.", file=sys.stderr)
        print("Add to ~/.zshrc: export FAL_API_KEY=\"your-key\"", file=sys.stderr)
        return 1

    try:
        path = generate_image(
            prompt=args.prompt,
            style=args.style,
            image_size=args.image_size,
            output_path=args.output,
            api_key=api_key,
        )
        print(f"OK: {path}")
        return 0
    except Exception as exc:
        truncated_prompt = (args.prompt[:50] + "...") if len(args.prompt) > 50 else args.prompt
        print("ERROR: 生成失败", file=sys.stderr)
        print(f"  prompt: {truncated_prompt}", file=sys.stderr)
        print(f"  style: {args.style}", file=sys.stderr)
        print(f"  attempts: {RETRIES}", file=sys.stderr)
        print(f"  last_error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
