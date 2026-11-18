/* A native-keyboard-friendly disclosure for the two download formats. */
(function () {
  "use strict";
  const box = document.getElementById("download-controls");
  const toggle = document.getElementById("download-toggle");
  const panel = document.getElementById("download-panel");
  if (!box || !toggle || !panel) return;
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
