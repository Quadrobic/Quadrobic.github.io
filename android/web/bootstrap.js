/* Offline-only bootstrap: no geolocation, persistent language and reading place. */
(function () {
  "use strict";
  const isTreatise = /\/index(?:\.(?:en|th))?\.html$/.test(location.pathname);
  const isYard = /\/yard\.html$/.test(location.pathname);
  const hasStar = isTreatise || isYard;
  const returnKey = isYard ? "iqj-offline-returned:yard" : "iqj-offline-returned";
  const language = document.documentElement.lang || "ru";
  const progressKey = "iqj-offline-progress:" + location.pathname;
  let interacted = false, restoring = true, saveTimer;
  // The native host retains the old frame until this document is ready to paint.
  window.iqjOfflineReady = false;
  if (hasStar) document.documentElement.classList.add("star-sealed");
  try {
    // The Activity remembers the last document. Honor explicit URLs (and Back)
    // instead of redirecting a Russian history entry to the saved language.
    if (isTreatise) localStorage.setItem("iqj-lang", language);
  } catch (_) {}

  const anchors = () => [...document.querySelectorAll(".passage[id], .proof-stage[id]")];
  function save() {
    if (restoring) return;
    let anchor = null;
    for (const item of anchors()) {
      if (item.getBoundingClientRect().top <= 100) anchor = item;
    }
    try {
      localStorage.setItem(progressKey, JSON.stringify({
        y: scrollY, anchor: anchor?.id || null,
        offset: anchor ? -anchor.getBoundingClientRect().top : 0,
      }));
    } catch (_) {}
  }
  function scheduleSave() {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(save, 250);
  }
  async function restore(force = false) {
    try {
      if (hasStar && localStorage.getItem(returnKey) === "yes") {
        document.documentElement.classList.remove("star-sealed");
      }
      await document.fonts.ready;
      await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
      window.__lenis?.resize();
      window.ScrollTrigger?.refresh();
      if ((interacted || location.hash) && !force) return;
      const saved = JSON.parse(localStorage.getItem(progressKey) || "null");
      if (saved) {
        const anchor = saved.anchor && document.getElementById(saved.anchor);
        const y = anchor ? scrollY + anchor.getBoundingClientRect().top + saved.offset : saved.y;
        window.dispatchEvent(new Event("reading:jump"));
        if (window.__lenis) window.__lenis.scrollTo(Math.max(0, y), { immediate: true });
        else scrollTo(0, Math.max(0, y));
      }
    } catch (_) {
      // A missing saved position must not prevent the new page becoming visible.
    } finally {
      restoring = false;
      window.iqjOfflineReady = true;
    }
  }
  for (const type of ["pointerdown", "touchstart", "wheel", "keydown"]) {
    addEventListener(type, () => { interacted = true; }, { passive: true, once: true });
  }
  addEventListener("load", () => setTimeout(() => restore(), 120));
  addEventListener("iqj:resume", () => restore(true));
  addEventListener("scroll", scheduleSave, { passive: true });
  addEventListener("iqj:save", save);
  addEventListener("pagehide", save);
  document.addEventListener("visibilitychange", () => { if (document.hidden) save(); });
  addEventListener("reading:return", () => {
    try { if (hasStar) localStorage.setItem(returnKey, "yes"); } catch (_) {}
    setTimeout(save, 1800);
  });
})();
