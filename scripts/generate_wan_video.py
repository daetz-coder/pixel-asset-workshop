"""Run the Wan Prime client bundled with the skill."""
from pathlib import Path
import runpy

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parents[1] / "skills"
                       / "wan-prime-video" / "scripts" / "generate_wan_video.py"),
                   run_name="__main__")
