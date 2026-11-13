/* Text references are edges, not proof dependencies. Selection never hides nodes. */
(function () {
  "use strict";
  const panels = [...document.querySelectorAll("[data-map-detail]")];
  if (!panels.length) return;
  document.documentElement.classList.add("map-enhanced");
  const nodes = [...document.querySelectorAll("[data-map-node]")];
  const edges = [...document.querySelectorAll("[data-from][data-to]")];
  function select(number, focus = false) {
    if (!panels.some(p => p.dataset.mapDetail === number)) number = "1";
    const related = new Set();
    for (const edge of edges) {
      const out = edge.dataset.from === number, incoming = edge.dataset.to === number;
      edge.classList.toggle("is-outgoing", out);
      edge.classList.toggle("is-incoming", incoming);
      if (out) related.add(edge.dataset.to);
      if (incoming) related.add(edge.dataset.from);
    }
    for (const node of nodes) {
      if (node.dataset.mapNode === number) node.setAttribute("aria-current", "true");
      else node.removeAttribute("aria-current");
      node.classList.toggle("is-related", related.has(node.dataset.mapNode));
    }
    for (const panel of panels) panel.classList.toggle("is-selected", panel.dataset.mapDetail === number);
    document.querySelectorAll("[data-map-lang]").forEach(a => { a.hash = `map-p${number}`; });
    const panel = panels.find(p => p.dataset.mapDetail === number);
    if (focus) {
      panel.querySelector("h2").focus({ preventScroll: true });
      if (matchMedia("(max-width: 900px)").matches) panel.scrollIntoView({ block: "start", behavior: "instant" });
    }
    history.replaceState(null, "", `#map-p${number}`);
  }
  document.addEventListener("click", event => {
    if (event.target.closest('.map-read, .map-nav > a')) {
      try { localStorage.setItem("iqj-lang", document.documentElement.lang); } catch (_) {}
    }
    const link = event.target.closest("[data-map-node], [data-map-select]");
    if (!link || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    select(link.dataset.mapNode || link.dataset.mapSelect, true);
  });
  addEventListener("hashchange", () => select(location.hash.replace("#map-p", "")));
  document.querySelectorAll("[data-map-lang]").forEach(link => link.addEventListener("click", () => {
    try { localStorage.setItem("iqj-lang", link.dataset.mapLang); } catch (_) {}
  }));
  select(location.hash.replace("#map-p", ""));
})();
