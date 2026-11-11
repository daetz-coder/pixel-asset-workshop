"""Generate one Wan3.0-Video-Prime MP4 from a local first frame."""

import argparse
import base64
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from uuid import UUID


MODEL = "wan3.0-video-prime"
DEFAULT_REGION = "cn-beijing"
SUBMIT_PATH = "/services/aigc/video-generation/video-synthesis"


def connection():
    workspace = os.environ.get("DASHSCOPE_WORKSPACE", "").strip()
    if not workspace:
        raise ValueError("Set DASHSCOPE_WORKSPACE to your Model Studio workspace ID.")
    region = os.environ.get("DASHSCOPE_REGION", DEFAULT_REGION)
    if not re.fullmatch(r"ws-[a-z0-9]+", workspace) or not re.fullmatch(r"[a-z0-9-]+", region):
        raise ValueError("Invalid DashScope workspace or region.")
    base_url = f"https://{workspace}.{region}.maas.aliyuncs.com/api/v1"

    api_key = os.environ.get("DASHSCOPE_API_KEY", "").strip()
    if not api_key and sys.platform == "darwin":
        credential = subprocess.run(
            ["/usr/bin/security", "find-generic-password", "-a", "codex",
             "-s", f"codex.wan-prime-video.{workspace}", "-w"],
            capture_output=True, text=True, timeout=15,
        )
        if credential.returncode == 0:
            api_key = credential.stdout.strip()
    if not api_key:
        raise RuntimeError("Set DASHSCOPE_API_KEY or configure the workspace's macOS Keychain entry.")
    return base_url, api_key


def call_api(base_url, path, api_key, payload=None):
    headers = {}
    body = None
    if payload is not None:
        headers = {"Content-Type": "application/json", "X-DashScope-Async": "enable"}
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = Request(base_url + path, data=body, headers=headers)
    request.add_unredirected_header("Authorization", f"Bearer {api_key}")
    try:
        with urlopen(request, timeout=60) as response:
            return json.load(response)
    except HTTPError as exc:
        try:
            error = json.load(exc)
        except ValueError:
            error = {}
        raise RuntimeError(f"HTTP {exc.code}: {api_error(error, api_key)}") from None


def api_error(error, api_key):
    message = f"{error.get('code', '')} {error.get('message', '')}".strip()
    message = message.replace(api_key, "[redacted]")
    return f"{message[:400]} (request {error.get('request_id', 'unknown')})"


def first_frame(image, ratio, background):
    if image.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".bmp"}:
        raise ValueError("Use a local PNG, JPEG, WebP, or BMP first frame.")
    if not image.is_file():
        raise ValueError(f"Image does not exist: {image}")
    magick = shutil.which("magick")
    if not magick:
        raise RuntimeError("ImageMagick (magick) is required to prepare the first frame.")

    source = [magick, f"{image.resolve()}[0]", "-auto-orient"]
    dimensions = subprocess.check_output(source + ["-format", "%w %h", "info:"])
    width, height = map(int, dimensions.split())
    transform = []
    if ratio != "adaptive":
        horizontal, vertical = map(int, ratio.split(":"))
        units = math.ceil(max(width / horizontal, height / vertical, 240 / horizontal, 240 / vertical))
        units = min(units, 8000 // max(horizontal, vertical))
        width, height = horizontal * units, vertical * units
        geometry = f"{width}x{height}"
        transform = ["-filter", "point", "-resize", f"{geometry}>",
                     "-gravity", "center", "-extent", geometry]
    if min(width, height) < 240 or max(width, height) > 8000 or max(width, height) > 8 * min(width, height):
        raise ValueError("First frame must be 240–8000 pixels per side with an aspect ratio within 8:1.")

    frame = subprocess.check_output(
        source + ["-background", background, "-alpha", "remove", "-alpha", "off"]
        + transform + ["-strip", "PNG24:-"]
    )
    if len(frame) > 20_000_000:
        raise ValueError("Prepared first frame exceeds 20 MB. Use a smaller input image.")
    return f"data:image/png;base64,{base64.b64encode(frame).decode('ascii')}"


def download_video(url, destination):
    if not url.startswith("https://"):
        raise RuntimeError("Wan did not return an HTTPS video URL.")
    with tempfile.NamedTemporaryFile(mode="w+b", dir=destination.parent) as temporary:
        with urlopen(url, timeout=120) as response:
            shutil.copyfileobj(response, temporary)
        temporary.flush()
        temporary.seek(0)
        if temporary.read(8)[4:8] != b"ftyp":
            raise RuntimeError("The downloaded response is not an MP4.")
        os.link(temporary.name, destination)


def wait_for_video(base_url, api_key, task_id, destination):
    last_status = None
    deadline = time.monotonic() + 900
    while time.monotonic() < deadline:
        result = call_api(base_url, f"/tasks/{task_id}", api_key)
        output = result["output"]
        status = output["task_status"]
        if status != last_status:
            print(f"{task_id}: {status}", flush=True)
            last_status = status
        if status == "SUCCEEDED":
            download_video(output["video_url"], destination)
            print(f"Saved {destination}", flush=True)
            return
        if status not in {"PENDING", "RUNNING"}:
            error = dict(output, request_id=result.get("request_id", "unknown"))
            raise RuntimeError(f"{status}: {api_error(error, api_key)}")
        time.sleep(10)
    raise RuntimeError("Polling timed out.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", type=Path, help="Local first-frame image")
    prompts = parser.add_mutually_exclusive_group()
    prompts.add_argument("--prompt", help="Prompt text")
    prompts.add_argument("--prompt-file", type=Path, help="UTF-8 plain-text prompt")
    parser.add_argument("--output", type=Path, help="Destination MP4")
    parser.add_argument("--resolution", type=str.upper, choices=["480P", "720P", "1080P"], default="480P")
    parser.add_argument("--ratio", choices=["16:9", "21:9", "4:3", "1:1", "3:4", "9:16", "adaptive"], default="16:9")
    parser.add_argument("--duration", type=int, default=5, help="Video duration in whole seconds (2–30)")
    parser.add_argument("--background", default="#FF00FF", help="RGB hex fill for transparency and padding")
    parser.add_argument("--audio", action="store_true")
    parser.add_argument("--prompt-extend", action="store_true", help="Allow Wan to rewrite the prompt")
    parser.add_argument("--task-id", type=UUID, help="Resume a task without submitting again")
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs locally without submitting")
    args = parser.parse_args()

    if args.task_id and (args.image or args.prompt is not None or args.prompt_file):
        parser.error("Use --task-id without --image or a prompt.")
    if args.task_id and args.dry_run:
        parser.error("Use --dry-run with a first frame and prompt, not --task-id.")
    if args.task_id is None and (args.image is None or (args.prompt is None and args.prompt_file is None)):
        parser.error("Provide --image and either --prompt or --prompt-file.")
    if not 2 <= args.duration <= 30:
        parser.error("--duration must be an integer from 2 to 30.")
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", args.background):
        parser.error("--background must be a six-digit RGB hex color such as '#FF00FF'.")

    label = args.image.stem if args.image else str(args.task_id)
    destination = (args.output or Path(f"{label}-wan-prime.mp4")).resolve()
    if destination.suffix.lower() != ".mp4":
        parser.error("--output must end in .mp4.")
    if destination.exists():
        parser.error(f"Output already exists: {destination}")

    task_id = args.task_id
    if task_id is None:
        prompt = (args.prompt_file.read_text(encoding="utf-8") if args.prompt_file else args.prompt).strip()
        if not 1 <= len(prompt) <= 20_000:
            parser.error("Prompt must contain 1–20,000 characters.")
        frame = first_frame(args.image, args.ratio, args.background)
        payload = {
            "model": MODEL,
            "input": {"prompt": prompt, "media": [{"type": "first_frame", "url": frame}]},
            "parameters": {
                "resolution": args.resolution,
                "ratio": args.ratio,
                "duration": args.duration,
                "audio": args.audio,
                "prompt_extend": args.prompt_extend,
                "watermark": False,
            },
        }
        if args.dry_run:
            print(f"Validated first frame and prompt for {MODEL}: "
                  f"{args.duration}s, {args.resolution}, {args.ratio}. No task submitted.")
            return

    destination.parent.mkdir(parents=True, exist_ok=True)
    base_url, api_key = connection()
    if task_id is None:
        try:
            result = call_api(base_url, SUBMIT_PATH, api_key, payload)
            task_id = UUID(result["output"]["task_id"])
        except (URLError, TimeoutError, KeyError, ValueError) as exc:
            raise RuntimeError("Submission status is uncertain. Check Model Studio for the task before resubmitting.") from exc
        print(f"Submitted {task_id} (request {result.get('request_id', 'unknown')})", flush=True)
    try:
        wait_for_video(base_url, api_key, task_id, destination)
    except (URLError, TimeoutError, KeyError, OSError, RuntimeError, ValueError, KeyboardInterrupt) as exc:
        details = type(exc).__name__ if isinstance(exc, URLError) else str(exc)
        raise RuntimeError(f"{details}\nResume with --task-id {task_id} and the same --output.") from None


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError, subprocess.SubprocessError) as exc:
        sys.exit(str(exc))
