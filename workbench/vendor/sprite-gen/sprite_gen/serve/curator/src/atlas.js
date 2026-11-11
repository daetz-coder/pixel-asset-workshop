// SPDX-License-Identifier: Apache-2.0
// Modified for SpriteFrame’s embedded bilingual frame editor.
// curator/atlas.js — 최종 아틀라스 섹션 (시트 + manifest 뷰)
// 로드 순서 SSoT = index.html (classic script 전역 어휘 공유; 빌드 스텝 없음)

let atlasBuild = Promise.resolve();

function queueAtlasBuild(build) {
  const pending = atlasBuild.then(build);
  atlasBuild = pending.catch(() => {});
  return pending;
}

function requireAtlasFrames() {
  if (!run.states.some(state => playList(state.name).length)) {
    throw new Error(t("atlasNeedsFrames"));
  }
}

async function renderFinalAtlas(info) {
  let section = document.getElementById("final-atlas");
  if (!section) {
    section = document.createElement("div");
    section.id = "final-atlas";
    section.className = "state final-atlas";
    document.getElementById("states").appendChild(section);
  }

  let manifest = null;
  if (info?.manifestUrl) {
    try {
      const response = await fetch(info.manifestUrl);
      if (!response.ok) throw new Error(response.status);
      manifest = await response.json();
    } catch {
      // The sprite sheet remains visible when its metadata is unavailable.
    }
  }
  const layout = manifest?.frame_layout;
  const frameWidth = Number(layout?.cellWidth);
  const sheetWidth = Number(layout?.sheetWidth);
  const previewWidth = frameWidth > 0 && sheetWidth > 0
    ? Math.ceil(sheetWidth * Math.min(1, 96 / frameWidth))
    : null;
  const stamp = info ? STR[lang].atlasStamp(new Date(info.mtime * 1000).toLocaleString()) : "";
  const metadata = layout ? ` · ${layout.sheetWidth} × ${layout.sheetHeight} px` : "";
  section.innerHTML =
    `<div class="state-head"><span class="name">${t("treeAtlas")}</span>` +
    (info ? `<span class="meta">PNG${escapeHtml(metadata)} · ${escapeHtml(stamp)}</span>` : "") +
    `<button type="button" class="ghost atlas-bake-btn" title="${t("tAtlasBake")}">${t(info ? "atlasBake" : "atlasPreview")}</button>` +
    `<button type="button" class="atlas-export-btn">${t("compose")}</button></div>` +
    (info
      ? `<div class="atlas-scroll" tabindex="0" aria-label="${t("treeAtlas")}">` +
        `<a class="atlas-sheet" href="${escapeHtml(info.url)}" target="_blank" rel="noopener">` +
        `<img src="${escapeHtml(info.url)}" alt="${t("treeAtlas")}"${previewWidth ? ` width="${previewWidth}"` : ""} />` +
        `</a></div>` +
        `<div class="atlas-animation-head">${t("atlasAnimations")}</div>` +
        `<div class="atlas-animation-strip" tabindex="0" aria-label="${t("atlasAnimations")}">` +
        `<span class="atlas-animation-status" role="status">${t("atlasAnimationsLoading")}</span></div>` +
        (info.manifestUrl
          ? `<details class="atlas-doc"><summary>${t("atlasDoc")}</summary>` +
            `<pre class="atlas-doc-json">${escapeHtml(manifest ? JSON.stringify(manifest, null, 2) : t("readingManifestFailed"))}</pre></details>`
          : "")
      : `<div class="atlas-pending">${t("atlasPending")}</div>`);

  const bakeBtn = section.querySelector(".atlas-bake-btn");
  const exportBtn = section.querySelector(".atlas-export-btn");
  if (info && (atlasDirty || lastEditAt > info.mtime * 1000)) markAtlasStale();
  bakeBtn.addEventListener("click", async () => {
    bakeBtn.disabled = exportBtn.disabled = true;
    bakeBtn.textContent = t("atlasBaking");
    try {
      await queueAtlasBuild(async () => {
        requireAtlasFrames();
        if (!await flushSave()) return;
        const editTime = lastEditAt;
        const response = await fetch("/api/compose", { method: "POST" });
        const result = await response.json();
        if (!response.ok || !result.ok) throw new Error(result.error || result.stderr || response.status);
        await refreshFinalAtlas(editTime);
        setStatus(t("atlasBaked"), "ok");
      });
    } catch (error) {
      setStatus(t("atlasBakeFail") + error.message, "err");
    } finally {
      bakeBtn.disabled = exportBtn.disabled = false;
      bakeBtn.textContent = t(info ? "atlasBake" : "atlasPreview");
    }
  });
  exportBtn.addEventListener("click", async () => {
    bakeBtn.disabled = exportBtn.disabled = true;
    exportBtn.textContent = t("atlasBaking");
    try {
      await downloadArtifact("atlas", t("composeDone"));
    } catch (error) {
      setStatus(t("composeFail") + error.message, "err");
    } finally {
      bakeBtn.disabled = exportBtn.disabled = false;
      exportBtn.textContent = t("compose");
    }
  });
  if (info) {
    ensureAtlasObserver();
    renderAtlasAnimations(section.querySelector(".atlas-animation-strip"));
  }
}

async function renderAtlasAnimations(strip) {
  try {
    await queueAtlasBuild(async () => {
      if (!strip.isConnected) return;
      const response = await fetch("/api/export-gif", { method: "POST" });
      const result = await response.json();
      if (!response.ok || !result.ok) throw new Error(result.error || result.stderr || response.status);
      if (!strip.isConnected) return;

      const animations = result.gif?.exports || [];
      if (!animations.length) {
        strip.querySelector(".atlas-animation-status").textContent = t("atlasNeedsFrames");
        return;
      }
      const version = Date.now();
      const cards = animations.map(({ state }) => {
        const card = document.createElement("figure");
        card.className = "atlas-animation";
        const image = document.createElement("img");
        image.src = `/run/exports/${encodeURIComponent(state)}.gif?v=${version}`;
        image.alt = state;
        const caption = document.createElement("figcaption");
        caption.textContent = state;
        card.append(image, caption);
        return card;
      });
      strip.replaceChildren(...cards);
    });
  } catch (error) {
    const status = strip.querySelector(".atlas-animation-status");
    if (strip.isConnected && status) status.textContent = t("atlasAnimationsFailed") + error.message;
  }
}

// 다운로드가 아틀라스/manifest 를 다시 계산했을 수 있으니 섹션을 최신 파일로 갱신
// ── 레이지 자동 굽기 (maintainer 2026-07-19 "실시간 반영, 단 느린 컴퓨터 렉 걱정"):
// 편집은 dirty 만 표시하고, 아틀라스 섹션이 **화면에 보일 때만** 디바운스 굽기를
// 돌린다 — 안 보는 동안엔 비용 0, 스크롤로 내려오는 순간 최신으로 한 번에 반영.
// 디바운스는 직전 compose 실측 소요시간의 3배(최소 0.8s)로 자동 조절 — 느린
// 머신일수록 덜 자주 굽는다. 굽는 중 새 편집은 끝나고 한 번 더 (코얼레싱).
// 수동 "지금 상태로 굽기" 버튼은 즉시 실행용으로 유지.
let autoBakeTimer = null;
let autoBakeRunning = false;
let autoBakeDirty = false;
let atlasDirty = false;
let atlasVisible = false;
let atlasObserver = null;
let lastBakeMs = 100;
function noteAtlasEdit() {
  atlasDirty = true;
  if (atlasVisible) scheduleAutoBake();
}
function ensureAtlasObserver() {
  const section = document.getElementById("final-atlas");
  if (!section || atlasObserver) return;
  atlasObserver = new IntersectionObserver((ents) => {
    atlasVisible = ents.some((e) => e.isIntersecting);
    if (atlasVisible && atlasDirty) scheduleAutoBake();
  });
  atlasObserver.observe(section);
}
async function autoBakeAtlas() {
  if (autoBakeRunning) { autoBakeDirty = true; return; }
  autoBakeRunning = true;
  let failed = null;
  try {
    await queueAtlasBuild(async () => {
      if (!atlasDirty || !run.states.some(state => playList(state.name).length)) return;
      const t0 = performance.now();
      const editTime = lastEditAt;
      const res = await fetch("/api/compose", { method: "POST" });
      lastBakeMs = performance.now() - t0;
      const data = await res.json().catch(() => ({}));
      if (res.ok && data.ok) {
        await refreshFinalAtlas(editTime);
      } else if (res.status === 503) autoBakeDirty = true;
      else failed = data.error || data.stderr || String(res.status);
    });
  } catch (e) {
    failed = e.message;
  }
  autoBakeRunning = false;
  // 지속 실패(500 등)는 재시도 루프를 돌리지 않는다 — 한 번 보고하고 배지 유지,
  // 다음 편집(저장)이 오면 다시 시도 (회귀 2026-07-19: 추출 미완 상태에서
  // 500 을 0.8s 간격으로 무한 재타격).
  if (failed) setStatus(t("atlasBakeFail") + failed, "err");
  else if (autoBakeDirty) { autoBakeDirty = false; scheduleAutoBake(); }
}
function scheduleAutoBake() {
  clearTimeout(autoBakeTimer);
  autoBakeTimer = setTimeout(autoBakeAtlas, Math.max(800, lastBakeMs * 3));
}

// 편집 직후 호출 (scheduleSave) — "편집 이후 안 구움" 을 버튼 배지로 보이게 한다.
// (자동 굽기가 곧 갱신하므로 배지는 굽기 완료까지의 과도 상태 표시가 된다.)
function markAtlasStale() {
  if (!run.atlas) return;
  const btn = document.querySelector(".atlas-bake-btn");
  if (btn && !btn.disabled && !btn.classList.contains("stale")) {
    btn.classList.add("stale");
    btn.textContent = `${t("atlasBake")} · ${t("atlasStale")}`;
  }
}

async function refreshFinalAtlas(editTime) {
  atlasDirty = lastEditAt > editTime;
  const now = Date.now();
  const firstBuild = !run.atlas;
  run.atlas = {
    url: `/run/sprite-sheet-alpha.png?v=${now}`,
    mtime: now / 1000,
    manifestUrl: `/run/manifest.json?v=${now}`,
  };
  run.hasAtlas = true;
  await renderFinalAtlas(run.atlas);
  if (firstBuild) renderPipelineTree();
}
