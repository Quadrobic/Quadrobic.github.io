/* Native scrolling and sealed targets for the unlisted edition; no runtime library. */
(function () {
  "use strict";
  // Only the final link requests music on the next document.
  document.querySelector('.yard-treatise-button')?.addEventListener('click', event => {
    if (event.defaultPrevented || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    const target = new URL(event.currentTarget.href);
    try {
      sessionStorage.setItem('iqj-yard-music', JSON.stringify({ path: target.pathname, at: Date.now() }));
    } catch (_) {}
  });
  function sealedTarget(hash) {
    if (!document.documentElement.classList.contains("star-sealed")) return null;
    let target;
    try { target = document.getElementById(decodeURIComponent(hash.slice(1))); }
    catch (_) { return null; }
    return target?.closest("[data-yard-after-star]")
      ? document.querySelector(".star-return") : null;
  }
  function visitSealed(hash) {
    const target = sealedTarget(hash);
    if (!target) return false;
    target.scrollIntoView({ block: "center" });
    target.focus({ preventScroll: true });
    return true;
  }
  function updateLanguageLinks() {
    document.querySelectorAll("[data-yard-language]").forEach(link => {
      link.hash = location.hash;
    });
  }
  updateLanguageLinks();
  addEventListener("hashchange", updateLanguageLinks);
  document.querySelector(".yard-index").addEventListener("click", event => {
    const link = event.target.closest('a[href^="#"]');
    if (!link) return;
    document.querySelector(".yard-index").open = false;
    if (visitSealed(link.hash)) event.preventDefault();
  });
  addEventListener("hashchange", () => visitSealed(location.hash));
  addEventListener("load", () => visitSealed(location.hash));
})();
