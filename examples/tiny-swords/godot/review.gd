extends Node2D

const NAMES := ["Warhammer Infantry", "Grenadier", "Standard Bearer",
	"Axe Infantry", "Crossbow Infantry", "Tower Shield Infantry"]
const ARCHER := "Units/Blue Units/Archer/Archer_Idle.png"
const INK := Color("#e4e9d9")
const MUTED := Color("#a3b0a0")
const RULE := Color("#43534a")
const PAPER := Color("#192620")
const FLOOR := Color("#26372d")

var font: Font = ThemeDB.fallback_font
var regions: Array[Dictionary] = []
var original: Array[ImageTexture] = []
var fps := 10.0
var elapsed := 0.0
var paused := false
var message := ""

func _ready() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	var root := ProjectSettings.globalize_path("res://").path_join("../../..").simplify_path()
	var directory := root.path_join("work/tiny-swords/frames")
	var pack := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--frames="):
			directory = arg.trim_prefix("--frames=")
		if arg.begins_with("--pack="):
			pack = arg.trim_prefix("--pack=")
	if not FileAccess.file_exists(directory.path_join("manifest.json")):
		message = "Run the frame extraction command in the README first."
		return
	var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(
		directory.path_join("manifest.json")))
	fps = float(manifest.sampling.fps)
	for item: Dictionary in manifest.regions:
		var frames: Array[ImageTexture] = []
		for i in range(int(item.frames)):
			var path := directory.path_join(item.directory).path_join("%04d.png" % i)
			var image := Image.load_from_file(path)
			if image == null or image.is_empty():
				message = "Unable to load frame %s" % path.get_file()
				return
			frames.append(ImageTexture.create_from_image(image))
		regions.append({"frames": frames, "anchor": Vector2(item.anchor_xy[0], item.anchor_xy[1])})
	if not pack.is_empty():
		var sheet := Image.load_from_file(pack.path_join(ARCHER))
		if sheet == null or sheet.get_width() != 1152 or sheet.get_height() != 192:
			message = "Use the Tiny Swords Free Pack with a 1152 × 192 Blue Archer idle sheet."
			return
		for i in range(6):
			var frame := sheet.get_region(Rect2i(i * 192, 0, 192, 192))
			original.append(ImageTexture.create_from_image(frame))

func _process(delta: float) -> void:
	if not paused:
		elapsed += delta
		queue_redraw()

func _unhandled_key_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_accept"):
		paused = not paused

func _draw() -> void:
	draw_rect(Rect2(0, 0, 880, 560), PAPER)
	draw_string(font, Vector2(32, 43), "PIXEL ASSET WORKSHOP", HORIZONTAL_ALIGNMENT_LEFT, -1, 16, MUTED)
	var title := "Generated sprite playback" if original.is_empty() else "Original and generated in Godot"
	draw_string(font, Vector2(32, 85), title, HORIZONTAL_ALIGNMENT_LEFT, -1, 31, INK)
	if not message.is_empty():
		draw_string(font, Vector2(32, 134), message, HORIZONTAL_ALIGNMENT_LEFT, -1, 18, INK)
		return
	if regions.is_empty():
		return
	if original.is_empty():
		for i in range(regions.size()):
			var x := 32 + (i % 3) * 276
			var y := 110 + floori(i / 3.0) * 199
			draw_tile(Rect2(x, y, 264, 188), NAMES[i], Vector2(x + 132, y + 147))
			draw_generated(i, Vector2(x + 132, y + 147), 1.0)
		draw_string(font, Vector2(32, 535), "Godot  •  10 fps extraction  •  Nearest-neighbor sampling", HORIZONTAL_ALIGNMENT_LEFT, -1, 16, MUTED)
	else:
		var left := Vector2(236, 365)
		var right := Vector2(644, 365)
		draw_tile(Rect2(32, 112, 400, 342), "Tiny Swords / Blue Archer", left)
		draw_tile(Rect2(448, 112, 400, 342), "Generated / Warhammer Infantry", right)
		var frame := original[floori(elapsed * 10) % original.size()]
		draw_sprite_at(frame, Vector2(94, 129), left, 2.0)
		draw_generated(0, right, 1.0)
		draw_string(font, Vector2(32, 490), "Original idle · 6 frames", HORIZONTAL_ALIGNMENT_LEFT, -1, 17, MUTED)
		draw_string(font, Vector2(448, 490), "Mixed generated clip · 50 sampled frames", HORIZONTAL_ALIGNMENT_LEFT, -1, 17, MUTED)
		draw_string(font, Vector2(32, 535), "Shared foot line  •  Archer 2× / Warhammer 1×  •  Enter or Space to pause", HORIZONTAL_ALIGNMENT_LEFT, -1, 16, MUTED)

func draw_tile(rect: Rect2, label: String, anchor: Vector2) -> void:
	draw_rect(rect, FLOOR)
	draw_line(Vector2(rect.position.x + 13, anchor.y), Vector2(rect.end.x - 13, anchor.y), RULE)
	draw_string(font, Vector2(rect.position.x + 13, rect.end.y - 13), label, HORIZONTAL_ALIGNMENT_LEFT, -1, 16, INK)

func draw_generated(index: int, at: Vector2, zoom: float) -> void:
	var region := regions[index]
	var frames: Array[ImageTexture] = region.frames
	var image := frames[floori(elapsed * fps) % frames.size()]
	draw_sprite_at(image, region.anchor, at, zoom)

func draw_sprite_at(image: Texture2D, anchor: Vector2, at: Vector2, zoom: float) -> void:
	draw_texture_rect(image, Rect2(at - anchor * zoom, image.get_size() * zoom), false)
