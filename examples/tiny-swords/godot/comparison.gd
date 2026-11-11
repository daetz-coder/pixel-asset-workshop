extends Node2D

const ReviewFrames := preload("res://review_frames.gd")
const PACK := "assets/references/tiny-swords/Tiny Swords (Free Pack)"
const TILESET := "Terrain/Tileset/"
const ORIGINAL_FPS := 10.0
const GENERATED_SCALE := 0.5
const ORIGINAL_Y := 235
const GENERATED_Y := 393
const LABELS := [
	["Hammer Pawn", "Warhammer Infantry"],
	["Lancer", "Grenadier"],
	["Monk", "Standard Bearer"],
	["Axe Pawn", "Axe Infantry"],
	["Archer", "Crossbow Infantry"],
	["Warrior", "Tower Shield Infantry"],
]
# The idle sheet frame size and a foot anchor for each original unit.
const ORIGINALS := [
	["Pawn/Pawn_Idle Hammer.png", 192, Vector2(94, 129)],
	["Lancer/Lancer_Idle.png", 320, Vector2(156, 192)],
	["Monk/Idle.png", 192, Vector2(96, 129)],
	["Pawn/Pawn_Idle Axe.png", 192, Vector2(97, 129)],
	["Archer/Archer_Idle.png", 192, Vector2(94, 129)],
	["Warrior/Warrior_Idle.png", 192, Vector2(97, 131)],
]
const INK := Color("#1d3329")
const MUTED := Color("#4b6257")
const PAPER := Color.WHITE

@onready var water: TileMapLayer = $Water
@onready var island: TileMapLayer = $Island
@onready var scenery: Node2D = $Scenery
@onready var originals: Node2D = $Originals
@onready var generated: Node2D = $Generated
@onready var overlay: Node2D = $Overlay

var font: Font = ThemeDB.fallback_font
var sequences := ReviewFrames.new()
var original_units: Array[AnimatedSprite2D] = []
var generated_units: Array[AnimatedSprite2D] = []
var pack: String
var message := ""
var elapsed := 0.0
var frame_count := 0
var current_frame := 0
var paused := false


func _ready() -> void:
	overlay.draw.connect(_draw_overlay)
	pack = ReviewFrames.argument("pack", ReviewFrames.repository_root().path_join(PACK))
	if not FileAccess.file_exists(pack.path_join(TILESET + "Tilemap_color1.png")):
		message = "Set --pack to the extracted Tiny Swords Free Pack directory."
		return
	if not sequences.load_sequences():
		message = sequences.error
		return
	var by_name := {}
	for region: Dictionary in sequences.regions:
		by_name[region.name] = region
	for pair: Array in LABELS:
		if not by_name.has(pair[1]):
			message = "The comparison needs the six-unit sample frame manifest. Missing: " + pair[1]
			return

	if not _build_ground():
		return
	_add_scenery()
	for i in range(ORIGINALS.size()):
		var unit: Array = ORIGINALS[i]
		var idle_frames := _load_idle(unit[0], unit[1])
		if idle_frames.is_empty():
			return
		original_units.append(_add_unit(originals, LABELS[i][0], idle_frames,
			unit[2], Vector2(_column(i), ORIGINAL_Y), 1.0))

		var region: Dictionary = by_name[LABELS[i][1]]
		var frames: Array[ImageTexture] = region.frames
		frame_count = maxi(frame_count, frames.size())
		generated_units.append(_add_unit(generated, LABELS[i][1], frames,
			region.anchor, Vector2(_column(i), GENERATED_Y), GENERATED_SCALE))
	_update_playback()


func _build_ground() -> bool:
	var water_image := Image.load_from_file(pack.path_join(TILESET + "Water Background color.png"))
	var ground_image := Image.load_from_file(pack.path_join(TILESET + "Tilemap_color1.png"))
	if water_image == null or water_image.get_size() != Vector2i(64, 64):
		message = "The Tiny Swords water tile must be 64 × 64."
		return false
	if ground_image == null or ground_image.get_width() < 512 or ground_image.get_height() < 384:
		message = "The Tiny Swords terrain atlas is missing or incomplete."
		return false

	water.tile_set = _tile_set(water_image, Rect2i(0, 0, 1, 1))
	for y in range(1, 9):
		for x in range(14):
			water.set_cell(Vector2i(x, y), 0, Vector2i.ZERO)

	island.tile_set = _tile_set(ground_image, Rect2i(5, 0, 3, 6))
	# Cliff-backed atlas columns 5–7 are the left edge, center and right edge.
	const ROWS := [0, 1, 1, 1, 1, 2, 5]
	for y in range(ROWS.size()):
		for x in range(13):
			var atlas_x := 5 if x == 0 else (7 if x == 12 else 6)
			island.set_cell(Vector2i(x, y), 0, Vector2i(atlas_x, ROWS[y]))
	return true


func _tile_set(image: Image, tiles: Rect2i) -> TileSet:
	var atlas := TileSetAtlasSource.new()
	atlas.texture = ImageTexture.create_from_image(image)
	atlas.texture_region_size = Vector2i(64, 64)
	for y in range(tiles.position.y, tiles.end.y):
		for x in range(tiles.position.x, tiles.end.x):
			atlas.create_tile(Vector2i(x, y))
	var tileset := TileSet.new()
	tileset.tile_size = atlas.texture_region_size
	tileset.add_source(atlas, 0)
	return tileset


func _add_scenery() -> void:
	_add_prop("Buildings/Blue Buildings/Tower.png", Vector2i(128, 256), Vector2(441, 205))
	_add_prop("Terrain/Resources/Wood/Trees/Tree1.png", Vector2i(192, 256), Vector2(66, 322))
	_add_prop("Terrain/Resources/Wood/Trees/Tree2.png", Vector2i(192, 256), Vector2(815, 324))
	_add_prop("Terrain/Decorations/Rocks/Rock1.png", Vector2i(64, 64), Vector2(795, 163))
	_add_prop("Terrain/Decorations/Rocks/Rock3.png", Vector2i(64, 64), Vector2(70, 450))
	_add_prop("Terrain/Decorations/Bushes/Bushe1.png", Vector2i(128, 128), Vector2(800, 455))
	_add_prop("Terrain/Decorations/Bushes/Bushe2.png", Vector2i(128, 128), Vector2(445, 314))


func _add_prop(path: String, frame_size: Vector2i, at: Vector2) -> void:
	var full_path := pack.path_join(path)
	if not FileAccess.file_exists(full_path):
		return
	var sheet := Image.load_from_file(full_path)
	if sheet == null or sheet.get_width() < frame_size.x or sheet.get_height() < frame_size.y:
		return
	var image := sheet.get_region(Rect2i(Vector2i.ZERO, frame_size))
	var bounds := image.get_used_rect()
	if not bounds.has_area():
		return
	var prop := Sprite2D.new()
	prop.texture = ImageTexture.create_from_image(image.get_region(bounds))
	prop.position = at
	prop.centered = false
	prop.offset = Vector2(-bounds.size.x * 0.5, -bounds.size.y)
	prop.scale = Vector2.ONE * 0.5
	scenery.add_child(prop)


func _load_idle(path: String, frame_size: int) -> Array[Texture2D]:
	var frames: Array[Texture2D] = []
	var sheet := Image.load_from_file(pack.path_join("Units/Blue Units/" + path))
	if sheet == null or sheet.get_height() != frame_size or sheet.get_width() % frame_size != 0:
		message = "Unexpected Tiny Swords idle sheet: " + path
		return frames
	var atlas := ImageTexture.create_from_image(sheet)
	for x in range(0, sheet.get_width(), frame_size):
		var frame := AtlasTexture.new()
		frame.atlas = atlas
		frame.region = Rect2(x, 0, frame_size, frame_size)
		frames.append(frame)
	return frames


func _add_unit(parent: Node2D, unit_name: String, textures: Array, anchor: Vector2,
		at: Vector2, zoom: float) -> AnimatedSprite2D:
	var unit := AnimatedSprite2D.new()
	unit.name = unit_name
	unit.sprite_frames = SpriteFrames.new()
	for texture: Texture2D in textures:
		unit.sprite_frames.add_frame(&"default", texture)
	unit.centered = false
	unit.position = at
	unit.offset = -anchor
	unit.scale = Vector2.ONE * zoom
	parent.add_child(unit)
	return unit


func _process(delta: float) -> void:
	if not paused and frame_count > 0 and message.is_empty():
		elapsed += delta
		_update_playback()


func _unhandled_key_input(event: InputEvent) -> void:
	if frame_count == 0 or not message.is_empty():
		return
	if event.is_action_pressed("ui_accept"):
		paused = not paused
	elif event.is_action_pressed("ui_left", true):
		_seek(-1)
	elif event.is_action_pressed("ui_right", true):
		_seek(1)
	else:
		return
	overlay.queue_redraw()


func _seek(direction: int) -> void:
	paused = true
	var tick := floori(elapsed * sequences.fps) + direction
	if tick < 0:
		tick = frame_count - 1
	elapsed = (tick + 0.01) / sequences.fps
	_update_playback()


func _update_playback() -> void:
	var generated_tick := floori(elapsed * sequences.fps)
	var original_tick := floori(elapsed * ORIGINAL_FPS)
	current_frame = generated_tick % frame_count
	for unit in original_units:
		unit.frame = original_tick % unit.sprite_frames.get_frame_count(&"default")
	for unit in generated_units:
		unit.frame = generated_tick % unit.sprite_frames.get_frame_count(&"default")
	overlay.queue_redraw()


func _column(index: int) -> int:
	return 110 + index * 132


func _draw_overlay() -> void:
	overlay.draw_rect(Rect2(0, 0, 880, 82), PAPER)
	overlay.draw_rect(Rect2(0, 530, 880, 30), PAPER)
	overlay.draw_string(font, Vector2(32, 42), "Tiny Swords training ground", HORIZONTAL_ALIGNMENT_LEFT, -1, 31, INK)
	overlay.draw_string(font, Vector2(33, 67), "Blue faction   ·   Original units and generated sprites", HORIZONTAL_ALIGNMENT_LEFT, -1, 15, MUTED)
	if not message.is_empty():
		overlay.draw_rect(Rect2(0, 82, 880, 448), PAPER)
		overlay.draw_string(font, Vector2(32, 130), message, HORIZONTAL_ALIGNMENT_LEFT, -1, 16, INK)
		return

	_draw_plate(Rect2(47, 103, 155, 26), "Original · Idle", Color("#edf3d6"))
	_draw_plate(Rect2(47, 286, 208, 26), "Generated · Mixed clip", Color("#edf3d6"))
	for i in range(LABELS.size()):
		var x := _column(i) - 64
		_draw_plate(Rect2(x, 248, 128, 23), LABELS[i][0], Color("#eef3dc"))
		_draw_plate(Rect2(x, 418, 128, 23), LABELS[i][1], Color("#e6efed"), 12)

	var controls := "Space / Enter to pause   ·   ← / → to step"
	if paused:
		controls = "Space / Enter to play   ·   ← / → to step"
	overlay.draw_string(font, Vector2(32, 550), controls, HORIZONTAL_ALIGNMENT_LEFT, -1, 13, MUTED)
	var status := "%02d / %02d   ·   %s fps" % [current_frame + 1, frame_count, str(sequences.fps)]
	overlay.draw_string(font, Vector2(650, 550), status, HORIZONTAL_ALIGNMENT_RIGHT, 198, 13, MUTED)


func _draw_plate(rect: Rect2, label: String, color: Color, font_size: int = 13) -> void:
	overlay.draw_rect(rect, color)
	overlay.draw_string(font, rect.position + Vector2(0, rect.size.y - 7),
		label, HORIZONTAL_ALIGNMENT_CENTER, rect.size.x, font_size, INK)
