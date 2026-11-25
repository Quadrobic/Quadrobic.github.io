/* Extra offline menu entry; the bonus also links directly to the story. */
(function () {
  "use strict";
  const english = document.documentElement.lang === "en";
  const title = english ? "The Person Who Cannot Be Seen" : "Человек, которого не видно";
  const destination = new URL(english ? "../yard.en.html" : "../yard.html", document.currentScript.src).href;
  document.addEventListener("DOMContentLoaded", () => {
    if (/\/yard(?:\.en)?\.html$/.test(location.pathname)) return;
    const continuation = document.getElementById("yard-link");
    const navigation = document.getElementById("side-nav");
    if (continuation && navigation) {
      // Move the bonus page's floating shortcut into its chapter menu. The
      // footer link remains available, and this page needs no secret duplicate.
      const title = continuation.textContent.trim();
      continuation.removeAttribute("id");
      continuation.className = "nav-dot offline-continuation";
      continuation.title = title;
      continuation.setAttribute("aria-label", title);
      continuation.lang = english ? "en" : "ru";
      const glyph = document.createElement("span");
      glyph.className = "nav-glyph";
      glyph.textContent = "✦";
      glyph.setAttribute("aria-hidden", "true");
      const label = document.createElement("span");
      label.className = "nav-label";
      label.textContent = title;
      continuation.replaceChildren(glyph, label);
      navigation.append(continuation);
      return;
    }
    const button = document.getElementById("mobile-menu-btn");
    const container = document.getElementById("controls-row")
      || document.querySelector("footer") || document.querySelector("main nav");
    if (!container) return;
    const entry = document.createElement("a");
    entry.className = "offline-yard-entry";
    entry.lang = english ? "en" : "ru";
    entry.href = destination;
    entry.setAttribute("aria-label", title);
    entry.title = title;
    const icon = document.createElement("span");
    icon.textContent = "✦";
    icon.setAttribute("aria-hidden", "true");
    const label = document.createElement("span");
    label.className = "offline-yard-label";
    label.textContent = title;
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
