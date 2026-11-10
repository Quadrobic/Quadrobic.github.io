/* Definitions come from the same README glossary used by the print edition.
   One occurrence per paragraph gets a quiet underline; the prose stays intact. */
(function () {
  "use strict";
  const data = document.getElementById("glossary-data");
  if (!data) return;
  const entries = JSON.parse(data.textContent);
  if (!entries.length) return;

  const lang = document.documentElement.lang || "ru";
  const labels = { ru: "Определение", en: "Definition", th: "ความหมาย" };
  const forms = new Map();
  const lower = (s) => s.toLocaleLowerCase(lang);
  for (let i = 0; i < entries.length; i++) {
    for (const form of entries[i].forms) forms.set(lower(form), i);
  }
  const escaped = [...forms.keys()].sort((a, b) => b.length - a.length)
    .map((s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  const matcher = new RegExp(escaped.join("|"), "giu");
  const word = /[\p{L}\p{M}\p{N}_]/u;

  const blocks = document.querySelectorAll(
    ".preamble p, .passage p, .passage-list li, .conclusion p, .axioms-list .axiom"
  );
  for (const block of blocks) {
    const used = new Set();
    const walker = document.createTreeWalker(block, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        return node.parentElement.closest("a, button, .gloss-term, code, script, style")
          ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      },
    });
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    for (const node of nodes) {
      const text = node.textContent;
      matcher.lastIndex = 0;
      const fragment = document.createDocumentFragment();
      let cursor = 0;
      for (const match of text.matchAll(matcher)) {
        const start = match.index, end = start + match[0].length;
        // Thai doesn't separate words with spaces. Its glossary names
        // are matched longest-first; alphabetic languages need boundaries.
        if (lang !== "th" && (word.test(text[start - 1] || "") || word.test(text[end] || ""))) continue;
        const index = forms.get(lower(match[0]));
        if (used.has(index)) continue;
        used.add(index);
        fragment.append(document.createTextNode(text.slice(cursor, start)));
        const term = document.createElement("span");
        term.className = "gloss-term";
        term.dataset.term = index;
        term.tabIndex = 0;
        term.setAttribute("role", "button");
        term.setAttribute("aria-label", `${labels[lang] || labels.en}: ${entries[index].title}`);
        term.setAttribute("aria-expanded", "false");
        term.setAttribute("aria-controls", "term-tooltip");
        term.textContent = match[0];
        fragment.append(term);
        cursor = end;
      }
      if (cursor) {
        fragment.append(document.createTextNode(text.slice(cursor)));
        node.replaceWith(fragment);
      }
    }
  }

  const tip = document.createElement("div");
  tip.id = "term-tooltip";
  tip.setAttribute("role", "tooltip");
  tip.hidden = true;
  const title = document.createElement("strong");
  title.className = "term-tooltip-title";
  const definition = document.createElement("p");
  tip.append(title, definition);
  document.body.append(tip);
  let active = null, pinned = false, timer = 0;

  const trigger = (node) => node instanceof Element ? node.closest(".gloss-term") : null;
  const clearTimer = () => window.clearTimeout(timer);

  function hide() {
    clearTimer();
    if (active) {
      active.setAttribute("aria-expanded", "false");
      active.removeAttribute("aria-describedby");
    }
    tip.hidden = true;
    active = null;
    pinned = false;
  }

  function position() {
    const rect = active.getBoundingClientRect();
    const column = active.closest(".passage, .book-body, .preamble, .axioms-list");
    const edge = column ? column.getBoundingClientRect().right : rect.right;
    const w = tip.offsetWidth, h = tip.offsetHeight;
    const gap = 14;
    let left, top;
    if (edge + 18 + w <= window.innerWidth - 54) {
      left = edge + 18;
      top = rect.top;
    } else {
      left = Math.max(gap, Math.min(rect.left, window.innerWidth - w - gap));
      top = rect.bottom + 10 + h <= window.innerHeight - gap
        ? rect.bottom + 10 : rect.top - h - 10;
    }
    top = Math.max(gap, Math.min(top, window.innerHeight - h - gap));
    tip.style.left = `${left}px`;
    tip.style.top = `${top}px`;
  }

  function show(term, pin = false) {
    clearTimer();
    if (active && active !== term) hide();
    active = term;
    pinned = pin;
    const entry = entries[Number(term.dataset.term)];
    title.textContent = entry.title;
    definition.textContent = entry.definition;
    term.setAttribute("aria-expanded", "true");
    term.setAttribute("aria-describedby", tip.id);
    tip.hidden = false;
    position();
  }

  function toggle(term) {
    if (active === term && pinned) hide();
    else show(term, true);
  }

  function closeSoon() {
    clearTimer();
    timer = window.setTimeout(() => {
      if (pinned || tip.matches(":hover") || active === document.activeElement || active?.matches(":hover")) return;
      hide();
    }, 180);
  }

  document.addEventListener("pointerover", (e) => {
    if (e.pointerType === "touch") return;
    const term = trigger(e.target);
    if (!term || active === term) return;
    clearTimer();
    timer = window.setTimeout(() => show(term), 140);
  });
  document.addEventListener("pointerout", (e) => {
    const term = trigger(e.target);
    if (term && !term.contains(e.relatedTarget)) closeSoon();
  });
  tip.addEventListener("pointerenter", clearTimer);
  tip.addEventListener("pointerleave", closeSoon);
  document.addEventListener("focusin", (e) => {
    const term = trigger(e.target);
    if (term) show(term);
  });
  document.addEventListener("focusout", (e) => {
    if (trigger(e.target)) closeSoon();
  });
  document.addEventListener("click", (e) => {
    const term = trigger(e.target);
    if (term) toggle(term);
    else if (!tip.contains(e.target)) hide();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") hide();
    const term = trigger(e.target);
    if (term && (e.key === "Enter" || e.key === " ")) {
      e.preventDefault();
      toggle(term);
    }
  });
  window.addEventListener("scroll", (e) => {
    if (!(e.target instanceof Node) || !tip.contains(e.target)) hide();
  }, { passive: true, capture: true });
  window.addEventListener("resize", hide, { passive: true });
})();
