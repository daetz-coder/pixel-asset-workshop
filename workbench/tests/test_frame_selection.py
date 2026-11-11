import json
import shutil
import tempfile
import unittest
from http.client import HTTPConnection
from http.server import HTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import unquote
from unittest.mock import patch

import server
from sprite_gen.curate.curation import empty_curation, state_plan, write_curation_atomic
from sprite_gen.serve import serve_curation
from sprite_gen.spec.runio import publish_guard


class FrameSelectionTests(unittest.TestCase):
    def test_download_header_preserves_unicode_filename(self):
        filename = "curation-run-01_战锤兵.gif"
        gif = b"GIF89a"
        with (
            patch.object(serve_curation, "maybe_heal", return_value=False),
            patch.object(serve_curation, "build_download", return_value=(gif, filename)),
            HTTPServer(("127.0.0.1", 0), serve_curation.CurationHandler) as httpd,
        ):
            httpd.timeout = 2
            worker = Thread(target=httpd.handle_request, daemon=True)
            worker.start()
            connection = HTTPConnection("127.0.0.1", httpd.server_port, timeout=2)
            try:
                connection.request("GET", "/download/gif")
                response = connection.getresponse()
                self.assertEqual(response.status, 200)
                self.assertTrue(response.getheader("X-Filename").isascii())
                disposition = response.getheader("Content-Disposition")
                self.assertEqual(unquote(disposition.split("filename*=UTF-8''", 1)[1]), filename)
                self.assertEqual(response.read(), gif)
            finally:
                connection.close()
                worker.join(2)

    def test_empty_explicit_selection_and_legacy_default(self):
        legacy = {"states": {"idle": {"selected": []}}}
        explicit = {"states": {"idle": {"selected": [], "selection_explicit": True}}}
        self.assertEqual(state_plan(legacy, "idle", 4)[0], [0, 1, 2, 3])
        self.assertEqual(state_plan(explicit, "idle", 4)[0], [])

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg required")
    def test_native_vfr_range_and_curated_export_order(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            source = folder / "source.mkv"
            server.command([
                "ffmpeg", "-nostdin", "-v", "error", "-y",
                "-f", "lavfi", "-i", "color=c=magenta:s=64x64:r=25:d=0.6",
                "-vf", "drawbox=x=24:y=20:w=16:h=24:color=blue:t=fill,"
                "select='eq(n,0)+eq(n,1)+eq(n,5)+eq(n,7)+eq(n,12)'",
                "-fps_mode", "passthrough", "-c:v", "ffv1", str(source),
            ])
            params = {
                "kind": "video", "key": "magenta", "fps": 10,
                "samplingMode": "native", "start": 0.03, "end": 0.5,
                "width": 64, "height": 64,
                "regions": [{"name": "idle", "x": 0, "y": 0, "w": 64, "h": 64}],
            }
            job = {}
            server.run_job(job, params, source)
            self.assertEqual(job["state"], "done", job.get("message"))
            result = Path(job["result_dir"])
            info = json.loads((result / "manifest.json").read_text())
            self.assertEqual(info["regions"][0]["frames"], 4)
            self.assertEqual(info["sampling"]["mode"], "native")
            self.assertIsNone(info["sampling"]["fps"])

            run = folder / "curation-run"
            server.prepare_curation(job, run)
            state = "01_idle"
            initial = json.loads((run / "curation.json").read_text())
            self.assertEqual(state_plan(initial, state, 4)[0], [])
            request = json.loads((run / "sprite-request.json").read_text())
            self.assertEqual(request["states"][state]["fps"], 10)

            curation = empty_curation()
            curation["states"][state] = {"selected": [3, 0], "selection_explicit": True}
            with publish_guard(run):
                write_curation_atomic(run, curation)
            exported = json.loads(server.command([
                str(server.PYTHON), "-m", "sprite_gen.cli", "export-pngs",
                "--run-dir", str(run), "--out-dir", str(folder / "export"), "--selected-only",
            ]))
            self.assertEqual(exported["count"], 2)
            animation = exported["animations"][0]
            self.assertEqual([frame["sourceIndex"] for frame in animation["frames"]], [3, 0])
            self.assertEqual([frame["file"] for frame in animation["frames"]], ["0003.png", "0000.png"])
            self.assertEqual(animation["fps"], 10)
            self.assertTrue(all(frame["durationMs"] == 100 for frame in animation["frames"]))

            curation["states"][state]["selected"] = []
            with publish_guard(run):
                write_curation_atomic(run, curation)
            empty = json.loads(server.command([
                str(server.PYTHON), "-m", "sprite_gen.cli", "export-pngs",
                "--run-dir", str(run), "--out-dir", str(folder / "empty"), "--selected-only",
            ]))
            self.assertEqual(empty["count"], 0)

            for name, start, end, limit, message in (
                ("empty-range", 0.06, 0.12, 10_000, "所选时间范围内没有视频帧"),
                ("frame-limit", 0.03, 0.5, 3, "单次最多导出 10000 张图"),
            ):
                with self.subTest(name=name):
                    case_folder = folder / name
                    case_folder.mkdir()
                    case_source = case_folder / source.name
                    shutil.copy2(source, case_source)
                    case_params = dict(params, start=start, end=end)
                    failed = {}
                    with patch.object(server, "MAX_FRAMES", limit):
                        server.run_job(failed, case_params, case_source)
                    self.assertEqual(failed["state"], "error")
                    self.assertIn(message, failed["message"])


if __name__ == "__main__":
    unittest.main()
