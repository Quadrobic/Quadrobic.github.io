/* Native navigation and Agda's own semantic links; no highlighting heuristics. */
(function () {
  "use strict";
  const lang = document.documentElement.lang;
  const languageLinks = document.querySelectorAll("#lang-switch [data-lang]");
  languageLinks.forEach((link) => {
    link.classList.toggle("active", link.dataset.lang === lang);
    if (link.dataset.lang === lang) link.setAttribute("aria-current", "page");
    // Keep the stage when changing the language of the reading page.
    link.addEventListener("click", () => {
      if (location.hash) link.hash = location.hash;
      try { localStorage.setItem("iqj-lang", link.dataset.lang); } catch (_) {}
    });
  });
  if (languageLinks.length) {
    try { localStorage.setItem("iqj-lang", lang); } catch (_) {}
  }

  const occurrences = new Map();
  document.querySelectorAll(".Agda a[href]").forEach((link) => {
    const key = link.href;
    if (!occurrences.has(key)) occurrences.set(key, []);
    occurrences.get(key).push(link);
    for (const [event, highlighted] of [["mouseenter", true], ["mouseleave", false], ["focus", true], ["blur", false]]) {
      link.addEventListener(event, () => {
        occurrences.get(key).forEach((other) => other.classList.toggle("symbol-highlight", highlighted));
      });
    }
  });

  const status = document.querySelector(".copy-status");
  let statusTimer;
  document.querySelectorAll("[data-copy]").forEach((button) => {
    button.addEventListener("click", async () => {
      const pre = button.closest("figure").querySelector("pre");
      let message = document.body.dataset.copyDone || "Copied";
      try {
        await navigator.clipboard.writeText(pre.textContent);
      } catch (_) {
        const range = document.createRange();
        range.selectNodeContents(pre);
        const selection = getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        message = document.body.dataset.copySelect || "Code selected";
      }
      if (status) {
        status.textContent = message;
        clearTimeout(statusTimer);
        statusTimer = setTimeout(() => { status.textContent = ""; }, 2200);
      }
    });
  });
})();
