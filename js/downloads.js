/* A native-keyboard-friendly disclosure for the two download formats. */
(function () {
  "use strict";
  const box = document.getElementById("download-controls");
  const toggle = document.getElementById("download-toggle");
  const panel = document.getElementById("download-panel");
  if (!box || !toggle || !panel) return;
  // Resolve versioned asset names only when Android is requested.
  // A failed API request falls back to GitHub's always-current release page.
  const android = document.getElementById("android-download");
  const releaseRoot = "https://github.com/Quadrobic/Quadrobic.github.io/releases/";
  if (android) android.href = releaseRoot + "latest";
  let pending = false;
  if (android) android.addEventListener("click", async (event) => {
    // Preserve native open-in-new-tab/window and download gestures.
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    if (pending) return;
    pending = true;
    android.setAttribute("aria-busy", "true");
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);
    let destination = releaseRoot + "latest";
    try {
      const response = await fetch(
        "https://api.github.com/repos/Quadrobic/Quadrobic.github.io/releases/latest",
        { signal: controller.signal, headers: { Accept: "application/vnd.github+json" } }
      );
      if (!response.ok) throw new Error("Release lookup failed");
      const release = await response.json();
      const assets = (release.assets || []).filter((asset) =>
        /^quadrobic-.*\.apk$/i.test(asset.name || "") &&
        typeof asset.browser_download_url === "string" &&
        asset.browser_download_url.startsWith(releaseRoot + "download/")
      );
      const apk = assets.find((asset) => asset.name === `quadrobic-${release.tag_name}.apk`) ||
                  (assets.length === 1 ? assets[0] : null);
      if (apk) destination = apk.browser_download_url;
    } catch (_) {
      // Includes offline access, API rate limits and network timeout.
    } finally {
      clearTimeout(timeout);
      pending = false;
      android.removeAttribute("aria-busy");
    }
    window.location.assign(destination);
  });
  function close(restoreFocus) {
    panel.hidden = true;
    toggle.setAttribute("aria-expanded", "false");
    if (restoreFocus) toggle.focus();
  }
  toggle.addEventListener("click", () => {
    const opening = panel.hidden;
    panel.hidden = !opening;
    toggle.setAttribute("aria-expanded", String(opening));
  });
  toggle.addEventListener("keydown", (event) => {
    if (event.key !== "ArrowDown") return;
    event.preventDefault();
    panel.hidden = false;
    toggle.setAttribute("aria-expanded", "true");
    panel.querySelector("a").focus();
  });
  panel.addEventListener("click", (event) => {
    if (event.target.closest("a")) close(true);
  });
  document.addEventListener("pointerdown", (event) => {
    if (!box.contains(event.target)) close(false);
  });
  box.addEventListener("focusout", (event) => {
    if (!box.contains(event.relatedTarget)) close(false);
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !panel.hidden) {
      event.preventDefault();
      event.stopImmediatePropagation();
      close(true);
    }
  }, true);
})();
