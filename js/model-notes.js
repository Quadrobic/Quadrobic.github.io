/* One claim inspector, shared by all numbered sections. No prose is replaced. */
(function () {
  "use strict";
  const dataNode = document.getElementById("model-notes-data");
  const panel = document.getElementById("model-panel");
  if (!dataNode || !panel) return;
  const data = JSON.parse(dataNode.textContent);
  const wide = matchMedia("(min-width: 1380px)");
  const hover = matchMedia("(hover: hover) and (pointer: fine)");
  let active = null, pinned = false, timer = 0, restoring = false;
  const cancel = () => clearTimeout(timer);
  const inside = (node) => node instanceof Node && panel.contains(node);
  const inContext = (node) => inside(node) || (active && node instanceof Node && active.closest(".passage").contains(node));
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
    const article = active.closest(".passage");
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
  function open(button, pin = false) {
    cancel();
    if (active === button) { pinned ||= pin; return; }
    close();
    active = button; pinned = pin;
    const section = data.sections[button.dataset.modelSection];
    panel.querySelector("#model-panel-title").textContent = section.title;
    panel.querySelector(".model-panel-content").innerHTML = section.html;
    panel.querySelector("[data-model-map]").href = `${data.map}#map-p${button.dataset.modelSection}`;
    panel.hidden = false;
    button.setAttribute("aria-expanded", "true");
    place();
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
  panel.addEventListener("toggle", place, true);
  addEventListener("resize", () => { if (active) place(); });
  addEventListener("scroll", () => {
    if (!active || panel.classList.contains("is-inline")) return;
    const rect = active.getBoundingClientRect();
    if (rect.bottom < 70 || rect.top > innerHeight - 40) close();
    else place();
  }, { passive: true });
})();
