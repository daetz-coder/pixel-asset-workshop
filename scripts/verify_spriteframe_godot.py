"""Exercise the video pipeline and exported resources in a supplied Godot binary.

All inputs and approvals belong to a synthetic test fixture, never production art.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw


GDSCRIPT = '''extends SceneTree
var failures: Array[String] = []
var finished := false
var looped := false

func expect(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)

func _initialize() -> void:
    call_deferred("verify")

func verify() -> void:
    var frames = load("res://sprites/attack/animation.tres") as SpriteFrames
    if frames == null:
        push_error("SpriteFrames failed to load")
        quit(1)
        return
    expect(frames.has_animation("attack"), "attack animation missing")
    expect(frames.get_frame_count("attack") == 8, "frame count")
    expect(is_equal_approx(frames.get_animation_speed("attack"), 8.0), "fps")
    expect(not frames.get_animation_loop("attack"), "attack should finish")
    for i in range(frames.get_frame_count("attack")):
        var texture = frames.get_frame_texture("attack", i)
        expect(texture != null and texture.get_size() == Vector2(64, 64), "texture dimensions")
        if texture != null:
            expect(texture.get_image().get_pixel(0, 0).a == 0.0, "transparent corner")
    # A second state tests the engine's playback and transition plumbing.
    # This does not prove shared scaling or alignment across generated actions.
    frames.add_animation("idle")
    frames.set_animation_speed("idle", 8.0)
    frames.set_animation_loop("idle", true)
    for i in range(2):
        frames.add_frame("idle", frames.get_frame_texture("attack", i))
    var sprite := AnimatedSprite2D.new()
    sprite.sprite_frames = frames
    sprite.position = Vector2(100, 100)
    sprite.centered = false
    sprite.offset = Vector2(-32, -56)
    root.add_child(sprite)
    sprite.animation_finished.connect(func(): finished = true)
    sprite.animation_looped.connect(func(): looped = true)
    sprite.play("attack")
    await create_timer(0.3).timeout
    expect(sprite.frame > 0, "playback did not advance")
    await create_timer(0.9).timeout
    expect(finished and not sprite.is_playing(), "one-shot did not finish")
    expect(sprite.frame == 7, "one-shot final frame")
    sprite.play("idle")
    await create_timer(0.6).timeout
    expect(looped and sprite.is_playing(), "idle did not loop")
    expect(sprite.position == Vector2(100, 100), "position changed on transition")
    expect(sprite.offset == Vector2(-32, -56), "anchor offset changed")
    print("SPRITEFRAME_RESULT=" + JSON.stringify({"passed": failures.is_empty(), "failures": failures}))
    quit(0 if failures.is_empty() else 1)
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--godot', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    if out.exists():
        parser.error('Output must be a new directory')
    if not args.godot.is_file():
        parser.error('Godot executable not found')
    out.mkdir(parents=True)
    cli = Path(__file__).resolve().parents[1] / 'skills/spriteframe/scripts/spriteframe.py'

    def run(name, command):
        result = subprocess.run(list(map(str, command)), capture_output=True, text=True,
                                encoding='utf-8', errors='replace', timeout=60)
        (out/f'{name}.log').write_text(result.stdout + result.stderr, encoding='utf-8')
        if result.returncode:
            raise RuntimeError(f'{name} failed; see {out/name}.log')
        return result.stdout

    version = run('version', [args.godot, '--version']).strip()
    source = out/'source'
    source.mkdir()
    for i in range(8):
        im = Image.new('RGB', (96, 96), '#00ff00')
        ImageDraw.Draw(im).rectangle((35+i, 20, 55+i, 80), fill='#d02525')
        im.save(source/f'{i:04}.png')
    video = out/'synthetic.mp4'
    run('encode', ['ffmpeg', '-loglevel', 'error', '-framerate', '8',
                   '-i', source/'%04d.png', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video])
    job = out/'job'
    run('process', [sys.executable, cli, 'process', '--video', video, '--out', job,
                    '--duration', '1', '--fps', '8', '--size', '64x64', '--anchor', '32,56',
                    '--key', '00ff00', '--tolerance', '80', '--source-accepted'])
    run('fixture-approval', [sys.executable, cli, 'approve', '--job', job,
                             '--reviewer', 'SYNTHETIC AUTOMATED TEST ONLY'])
    project = out/'project'
    project.mkdir()
    (project/'project.godot').write_text('config_version=5\n[application]\nconfig/name="SpriteFrame Test"\n', encoding='utf-8')
    run('export', [sys.executable, cli, 'export-godot', '--job', job, '--out', project/'sprites/attack',
                   '--name', 'attack', '--res-path', 'res://sprites/attack'])
    (project/'verify.gd').write_text(GDSCRIPT, encoding='utf-8')
    run('import', [args.godot, '--headless', '--path', project, '--editor', '--import'])
    result = run('playback', [args.godot, '--headless', '--path', project, '--script', 'res://verify.gd'])
    marker = next((line for line in result.splitlines() if line.startswith('SPRITEFRAME_RESULT=')), None)
    if marker is None:
        raise RuntimeError('Godot did not report test completion; inspect playback.log')
    report = json.loads(marker.split('=', 1)[1])
    if not report['passed']:
        raise RuntimeError(str(report))
    report.update({'godot_version': version, 'fixture': 'synthetic, not production art',
                   'checks': ['resource load', '8 textures and alpha', '8 FPS', 'frame progression',
                              'one-shot finish', 'loop playback', 'node position and anchor on transition'],
                   'limits': 'No rendered visual QA, real character art, or cross-action alignment validation.'})
    (out/'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
