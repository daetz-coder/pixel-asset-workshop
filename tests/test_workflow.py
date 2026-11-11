"""Offline integration tests on the actual saved Wan clip and the example sprite batch."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def run(script, *args):
    return subprocess.run([sys.executable, script, *map(str, args)], cwd=ROOT,
                          capture_output=True, text=True, check=True)


class TinySwordsWorkflow(unittest.TestCase):
    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg required")
    def test_real_wan_clip_extracts_six_aligned_transparent_sequences(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "frames"
            run("scripts/extract_frames.py", "--video",
                "assets/video-inputs/blue-units-3x2-wan-prime-480p.mp4", "--layout",
                "examples/tiny-swords/wan-layout.json", "--out", target)
            manifest = json.loads((target / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["source_size"], [854, 480])
            self.assertEqual(manifest["status"], "unreviewed")
            self.assertEqual(len(manifest["regions"]), 6)
            for region in manifest["regions"]:
                row, col = region["row"], region["col"]
                self.assertEqual(region["crop_xywh"],
                                 [[0, 285, 569][col], 240 * row, [285, 284, 285][col], 240])
                self.assertEqual(region["anchor_xy"], [[142, 142, 143][col], 167])
                self.assertEqual(region["empty_frames"], [])
                folder = target / region["directory"]
                frames = sorted(folder.glob("*.png"))
                self.assertEqual(len(frames), 50)
                self.assertEqual(frames[-1].name, "0049.png")
                for path in (frames[0], frames[-1]):
                    with Image.open(path) as frame:
                        self.assertEqual(frame.size, tuple(region["crop_xywh"][2:]))
                        self.assertEqual(frame.mode, "RGBA")
                        self.assertEqual(frame.getchannel("A").getextrema(), (0, 255))

    @unittest.skipUnless(shutil.which("magick"), "ImageMagick 7 required")
    def test_composed_walk_board_and_wan_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            reference = folder / "walk.png"
            run("skills/wan-prime-video/scripts/compose_reference.py", "--config",
                "examples/tiny-swords/batch-walk.json", "--output", reference)
            layout = json.loads((folder / "walk-layout.json").read_text(encoding="utf-8"))
            self.assertEqual((layout["cols"], layout["rows"], layout["action"]), (3, 2, "walk"))
            self.assertEqual([c["name"] for c in layout["cells"]],
                             ["战锤兵", "投弹兵", "旗手", "战斧兵", "弩兵", "塔盾兵"])
            with Image.open(reference) as image:
                self.assertEqual(image.size, (1280, 720))
                self.assertEqual(image.getpixel((0, 0)), (255, 0, 255))
            prompt = folder / "walk-prompt.txt"
            self.assertIn("Row 2, column 3 · 塔盾兵", prompt.read_text(encoding="utf-8"))
            result = run("scripts/generate_wan_video.py", "--image", reference, "--prompt-file",
                         prompt, "--ratio", "adaptive", "--output", folder / "walk.mp4", "--dry-run")
            self.assertIn("No task submitted", result.stdout)
            self.assertFalse((folder / "walk.mp4").exists())


if __name__ == "__main__":
    unittest.main()
