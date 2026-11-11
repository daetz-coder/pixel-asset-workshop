// SPDX-License-Identifier: Apache-2.0
// SpriteFrame's initial frame selection for the embedded curator.

async function summarizePose(frame, context, size) {
  const image = img(frame.url);
  if (!image.complete || !image.naturalWidth) await image.decode();
  context.clearRect(0, 0, size, size);
  context.drawImage(image, 0, 0, size, size);
  const { data } = context.getImageData(0, 0, size, size);
  let coverage = 0;
  let touchesEdge = false;
  for (let pixel = 0; pixel < size * size; pixel++) {
    const offset = pixel * 4;
    const alpha = data[offset + 3];
    coverage += alpha;
    for (let channel = 0; channel < 3; channel++) data[offset + channel] *= alpha / 255;
    const x = pixel % size;
    if (alpha >= 128 && (pixel < size || x === 0 || x === size - 1)) touchesEdge = true;
  }
  return { index: frame.index, data, coverage, touchesEdge };
}

function poseDifference(a, b) {
  let difference = 0;
  for (let i = 0; i < a.data.length; i++) difference += Math.abs(a.data[i] - b.data[i]);
  return difference / (4 * Math.max(a.coverage, b.coverage));
}

async function suggestFrames(state) {
  const entry = entries[state.name];
  const available = new Set(entry.order);
  const frames = state.frames.filter(frame => frame.present && available.has(frame.index));
  if (frames.length < 2) return frames.map(frame => frame.index);

  const duration = Number(pageQuery.get("sourceSeconds"));
  const seconds = duration > 0 && Number.isFinite(duration) ? duration : frames.length / 30;
  const target = Math.min(frames.length, Math.max(1, Math.ceil(seconds * state.fps)));
  const size = 40;
  const thumbnail = document.createElement("canvas");
  thumbnail.width = thumbnail.height = size;
  const context = thumbnail.getContext("2d", { willReadFrequently: true });
  const duplicateDistance = 0.035;
  const selected = [];
  let previous = null;
  let lastVisible = null;

  // Walk chronological buckets at the target playback rate. A strong pose
  // inside a bucket can survive even if it falls between regular samples.
  for (let bucket = 0; bucket < target; bucket++) {
    const first = Math.floor(bucket * frames.length / target);
    const end = Math.floor((bucket + 1) * frames.length / target);
    let best = null;
    let bestScore = -Infinity;
    for (let i = first; i < end; i++) {
      const pose = await summarizePose(frames[i], context, size);
      if (!pose.coverage) continue;
      lastVisible = pose;
      if (!previous) {
        selected.push(pose.index);
        previous = pose;
        continue;
      }
      const change = poseDifference(previous, pose);
      if (change < duplicateDistance) continue;
      const score = change - (pose.touchesEdge ? 0.04 : 0);
      if (score > bestScore) {
        best = pose;
        bestScore = score;
      }
    }
    if (best) {
      selected.push(best.index);
      previous = best;
    }
  }
  if (lastVisible && poseDifference(previous, lastVisible) >= duplicateDistance) {
    selected.push(lastVisible.index);
  }
  return selected.length ? selected : [frames[0].index];
}

function applySuggestedFrames(state, indices) {
  const entry = entries[state.name];
  entry.sel = new Set(indices);
  entry.order = [...indices, ...entry.order.filter(index => !entry.sel.has(index))];
}

async function seedSuggestedFrames() {
  if (!embedded) return true;
  const fresh = run.states.filter(state => {
    const saved = run.curation?.states?.[state.name];
    return saved?.selection_explicit === true && saved.selected?.length === 0 && !saved.order;
  });
  if (!fresh.length) return true;
  setStatus(t("autoSelecting"));
  const results = await Promise.allSettled(fresh.map(async state => {
    applySuggestedFrames(state, await suggestFrames(state));
  }));
  return results.every(result => result.status === "fulfilled");
}
