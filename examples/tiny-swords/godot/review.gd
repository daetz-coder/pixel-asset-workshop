extends Node2D

const ReviewFrames := preload("res://review_frames.gd")
const NAMES := ["Warhammer Infantry", "Grenadier", "Standard Bearer",
	"Axe Infantry", "Crossbow Infantry", "Tower Shield Infantry"]
const INK := Color("#e4e9d9")
const MUTED := Color("#a3b0a0")
const RULE := Color("#43534a")
const PAPER := Color("#192620")
const FLOOR := Color("#26372d")

var font: Font = ThemeDB.fallback_font
var sequences := ReviewFrames.new()
var elapsed := 0.0
var paused := false


func _ready() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	if not ReviewFrames.argument("pack").is_empty():
		get_tree().change_scene_to_file.call_deferred("res://comparison.tscn")
		return
	sequences.load_sequences()


func _process(delta: float) -> void:
	if not paused and sequences.error.is_empty():
		elapsed += delta
		queue_redraw()


func _unhandled_key_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_accept"):
		paused = not paused


func _draw() -> void:
	draw_rect(Rect2(0, 0, 880, 560), PAPER)
	draw_string(font, Vector2(32, 43), "PIXEL ASSET WORKSHOP", HORIZONTAL_ALIGNMENT_LEFT, -1, 16, MUTED)
	draw_string(font, Vector2(32, 85), "Generated sprite playback", HORIZONTAL_ALIGNMENT_LEFT, -1, 31, INK)
	if not sequences.error.is_empty():
		draw_string(font, Vector2(32, 134), sequences.error, HORIZONTAL_ALIGNMENT_LEFT, -1, 18, INK)
		return

	for i in range(mini(sequences.regions.size(), NAMES.size())):
		var x := 32 + (i % 3) * 276
		var y := 110 + floori(i / 3.0) * 199
		var at := Vector2(x + 132, y + 147)
		var tile := Rect2(x, y, 264, 188)
		draw_rect(tile, FLOOR)
		draw_line(Vector2(x + 13, at.y), Vector2(tile.end.x - 13, at.y), RULE)
		draw_string(font, Vector2(x + 13, tile.end.y - 13), NAMES[i], HORIZONTAL_ALIGNMENT_LEFT, -1, 16, INK)
		var region: Dictionary = sequences.regions[i]
		var frames: Array[ImageTexture] = region.frames
		var image := frames[floori(elapsed * sequences.fps) % frames.size()]
		draw_texture_rect(image, Rect2(at - region.anchor, image.get_size()), false)

	if not sequences.regions.is_empty():
		var caption := "Godot  •  %s fps extraction  •  Nearest-neighbor sampling" % sequences.fps
		draw_string(font, Vector2(32, 535), caption, HORIZONTAL_ALIGNMENT_LEFT, -1, 16, MUTED)
