/* Extra offline menu entry; the bonus also links directly to the story. */
(function () {
  "use strict";
  const destination = new URL("../yard.html", document.currentScript.src).href;
  document.addEventListener("DOMContentLoaded", () => {
    if (/\/yard\.html$/.test(location.pathname)) return;
    const button = document.getElementById("mobile-menu-btn");
    const container = document.getElementById("controls-row")
      || document.querySelector("footer") || document.querySelector("main nav");
    if (!container) return;
    const entry = document.createElement("a");
    entry.className = "offline-yard-entry";
    entry.lang = "ru";
    entry.href = destination;
    entry.setAttribute("aria-label", "Человек, которого не видно · RU");
    entry.title = "Человек, которого не видно · RU";
    const icon = document.createElement("span");
    icon.textContent = "✦";
    icon.setAttribute("aria-hidden", "true");
    const label = document.createElement("span");
    label.className = "offline-yard-label";
    label.textContent = "Человек, которого не видно · RU";
    entry.append(icon, label);
    entry.hidden = true;
    try { entry.hidden = sessionStorage.getItem("iqj-yard-menu") !== "yes"; } catch (_) {}
    container.append(entry);
    let taps = 0, started = 0;
    function tap() {
      if (!entry.hidden) return;
      const now = performance.now();
      if (!taps || now - started > 4000) { taps = 0; started = now; }
      if (++taps < 5) return;
      entry.hidden = false;
      try { sessionStorage.setItem("iqj-yard-menu", "yes"); } catch (_) {}
      if (button && getComputedStyle(button).display !== "none") {
        if (button.getAttribute("aria-expanded") !== "true") button.click();
        const sheet = document.getElementById("mobile-sheet");
        if (sheet) sheet.scrollTop = sheet.scrollHeight;
      }
    }
    // DOMContentLoaded runs after main.js has installed the normal menu toggle.
    button?.addEventListener("click", tap);
    // Build-number taps also work on tablets without the compact menu button.
    document.querySelectorAll("[data-offline-version]").forEach(version => {
      version.tabIndex = 0;
      version.setAttribute("role", "button");
      version.addEventListener("click", tap);
      version.addEventListener("keydown", event => {
        if (!event.repeat && (event.key === "Enter" || event.key === " ")) {
          event.preventDefault();
          tap();
        }
      });
    });
  }, { once: true });
})();
