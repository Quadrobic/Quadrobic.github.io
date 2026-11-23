/* One inspector for model claims and contextual readings. No prose is replaced. */
(function () {
  "use strict";
  const dataNode = document.getElementById("model-notes-data");
  const panel = document.getElementById("model-panel");
  if (!dataNode || !panel) return;
  const data = JSON.parse(dataNode.textContent);
  let loading = null;
  function loadNotes() {
    if (data.sections) return Promise.resolve();
    if (loading) return loading;
    loading = new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = dataNode.dataset.src;
      script.async = true;
      let finished = false;
      const timeout = setTimeout(() => finish(new Error("Notes timed out")), 10000);
      function finish(error) {
        if (finished) return;
        finished = true;
        clearTimeout(timeout);
        script.remove();
        if (error) { reject(error); return; }
        const payload = window.iqjModelNotes;
        if (!payload || payload.version !== data.version || !payload.sections) {
          reject(new Error("Notes snapshot mismatch"));
          return;
        }
        data.sections = payload.sections;
        resolve();
      }
      script.onload = () => finish();
      script.onerror = () => finish(new Error("Notes unavailable"));
      document.head.append(script);
    }).catch((error) => {
      loading = null; // A later visit to a marker can retry a failed request.
      throw error;
    });
    return loading;
  }
  const wide = matchMedia("(min-width: 1380px)");
  const hover = matchMedia("(hover: hover) and (pointer: fine)");
  let active = null, pinned = false, timer = 0, restoring = false;
  const cancel = () => clearTimeout(timer);
  const inside = (node) => node instanceof Node && panel.contains(node);
  const region = (button) => button.closest(".passage, .model-context");
  const inContext = (node) => inside(node) || (active && node instanceof Node && region(active).contains(node));
  const trigger = (node) => node instanceof Element ? node.closest(".model-marker") : null;

  function refresh() {
    window.__lenis?.resize();
    window.ScrollTrigger?.refresh();
  }
  function close(restore = false) {
    cancel();
    if (!active) return;
    const button = active;
    const inline = panel.classList.contains("is-inline");
    panel.hidden = true;
    button.setAttribute("aria-expanded", "false");
    active = null; pinned = false;
    document.body.append(panel);
    if (restore) {
      restoring = true; button.focus({ preventScroll: true }); restoring = false;
    }
    if (inline) refresh();
  }
  function place() {
    if (!active) return;
    const article = region(active);
    const rect = article.getBoundingClientRect();
    const inline = !wide.matches || rect.right + 328 > innerWidth;
    const changed = panel.classList.contains("is-inline") !== inline;
    panel.classList.toggle("is-inline", inline);
    if (inline) {
      document.getElementById(`model-slot-${active.dataset.modelSection}`).append(panel);
      if (changed) refresh();
    } else {
      document.body.append(panel);
      const marker = active.getBoundingClientRect();
      panel.style.left = `${rect.right + 14}px`;
      panel.style.top = `${Math.max(86, Math.min(marker.top, innerHeight - panel.offsetHeight - 18))}px`;
    }
  }
  async function open(button, pin = false) {
    cancel();
    if (active === button) { pinned ||= pin; return; }
    close();
    active = button; pinned = pin;
    const id = button.dataset.modelSection;
    const title = panel.querySelector("#model-panel-title");
    const content = panel.querySelector(".model-panel-content");
    const mapLink = panel.querySelector("[data-model-map]");
    title.textContent = data.ui[id] || region(button).querySelector("h3, h2")?.textContent || data.ui.status;
    panel.querySelector(".model-panel-label").textContent = data.ui.status;
    panel.querySelector(".model-panel-scope").textContent = data.ui.scope;
    content.textContent = data.ui.loading;
    panel.querySelector("footer").hidden = false;
    mapLink.href = data.map;
    panel.hidden = false;
    panel.setAttribute("aria-busy", "true");
    button.setAttribute("aria-expanded", "true");
    place();
    try {
      await loadNotes();
      if (active !== button) return; // Do not reopen a closed or replaced panel.
      const section = data.sections[id];
      title.textContent = section.title;
      panel.querySelector(".model-panel-label").textContent = section.label || data.ui.status;
      panel.querySelector(".model-panel-scope").textContent = section.scope || data.ui.scope;
      content.innerHTML = section.html;
      panel.querySelector("footer").hidden = !!section.context;
      if (section.context) mapLink.removeAttribute("href");
      else mapLink.href = `${data.map}#map-p${id}`;
    } catch (_) {
      if (active !== button) return;
      content.textContent = data.ui.load_error;
    } finally {
      if (active === button) {
        panel.removeAttribute("aria-busy");
        place();
        if (panel.classList.contains("is-inline")) refresh();
      }
    }
  }
  function delayedClose() {
    cancel();
    timer = setTimeout(() => {
      if (!pinned && !inside(document.activeElement) && document.activeElement !== active) close();
    }, 200);
  }
  document.addEventListener("pointerover", (event) => {
    if (event.pointerType !== "mouse" && !hover.matches) return;
    const button = trigger(event.target);
    if (button) open(button);
    else if (inContext(event.target)) cancel();
  });
  document.addEventListener("pointerout", (event) => {
    if (event.pointerType !== "mouse" && !hover.matches) return;
    if ((trigger(event.target) || inContext(event.target)) && !trigger(event.relatedTarget) && !inContext(event.relatedTarget)) delayedClose();
  });
  document.addEventListener("focusin", (event) => {
    if (restoring) return;
    const button = trigger(event.target);
    if (button) open(button);
    else if (active && !inside(event.target) && event.target !== active) close();
  });
  document.addEventListener("click", (event) => {
    const button = trigger(event.target);
    if (button) {
      if (active === button && pinned) close();
      else open(button, true);
    } else if (event.target.closest?.("[data-model-close]")) close(true);
    else if (active && !inside(event.target)) close();
  });
  document.addEventListener("keydown", (event) => {
    if (!active) return;
    if (event.key === "Escape") {
      event.preventDefault(); event.stopImmediatePropagation();
      close(inside(document.activeElement));
    } else if (event.key === "ArrowRight" && event.target === active) {
      pinned = true; panel.querySelector("[data-model-close]").focus();
      event.preventDefault();
    }
  }, true);
  let placementFrame = 0;
  function schedulePlace() {
    if (placementFrame) return;
    placementFrame = requestAnimationFrame(() => { placementFrame = 0; place(); });
  }
  panel.addEventListener("toggle", schedulePlace, true);
  addEventListener("resize", () => { if (active) schedulePlace(); });
  addEventListener("scroll", () => {
    if (!active || panel.classList.contains("is-inline")) return;
    const rect = active.getBoundingClientRect();
    if (rect.bottom < 70 || rect.top > innerHeight - 40) close();
    else schedulePlace();
  }, { passive: true });
})();
