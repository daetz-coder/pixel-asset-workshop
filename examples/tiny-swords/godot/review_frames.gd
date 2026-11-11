extends RefCounted

var regions: Array[Dictionary] = []
var fps := 10.0
var error := ""


static func repository_root() -> String:
	return ProjectSettings.globalize_path("res://").path_join("../../..").simplify_path()


static func argument(key: String, fallback: String = "") -> String:
	var prefix := "--" + key + "="
	for value in OS.get_cmdline_user_args():
		if value.begins_with(prefix):
			return value.trim_prefix(prefix)
	return fallback


func load_sequences() -> bool:
	var directory := argument("frames", repository_root().path_join("work/tiny-swords/frames"))
	var path := directory.path_join("manifest.json")
	if not FileAccess.file_exists(path):
		error = "Run the frame extraction command in the README first."
		return false

	var manifest: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not manifest is Dictionary or not manifest.get("regions") is Array:
		error = "Invalid frame manifest: " + path
		return false
	fps = float(manifest.get("sampling", {}).get("fps", 10.0))
	if fps <= 0.0 or manifest.regions.is_empty():
		error = "The frame manifest needs a positive sampling rate and at least one sequence."
		return false

	for item: Dictionary in manifest.regions:
		var frames: Array[ImageTexture] = []
		for i in range(int(item.frames)):
			var frame_path := directory.path_join(item.directory).path_join("%04d.png" % i)
			var image := Image.load_from_file(frame_path)
			if image == null or image.is_empty():
				error = "Unable to load frame: " + frame_path
				return false
			frames.append(ImageTexture.create_from_image(image))
		if frames.is_empty():
			error = "Empty sequence: " + str(item.directory)
			return false
		regions.append({
			"name": str(item.get("name", "")),
			"frames": frames,
			"anchor": Vector2(item.anchor_xy[0], item.anchor_xy[1]),
		})
	return true
