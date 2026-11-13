/* §38: a temporary night, never a scroll lock. Return restores the page. */
(function () {
  "use strict";
  const section = document.querySelector("[data-star-reading]");
  if (!section) return;
  const root = document.documentElement;
  const motion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const phases = [...section.querySelectorAll("[data-star-phase]")];
  const lines = [...section.querySelectorAll(".star-line")];
  const button = section.querySelector(".star-return");
  const heading = section.querySelector("h3");
  const conclusion = document.getElementById("conclusion");
  let active = false, dismissed = false, released = false;
  let returning = false;
  let scheduled = false, previousY = window.scrollY;
  let cancelBurst = null;
  window.deathStarActive = false;

  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      entry.target.classList.toggle("star-in-view", entry.isIntersecting);
    }
  }, { rootMargin: "0px", threshold: 0.05 });
  lines.forEach((line) => observer.observe(line));

  function setActive(value) {
    if (active === value) return;
    active = value;
    window.deathStarActive = value;
    root.classList.toggle("death-star-mode", value);
    if (value) {
      released = false;
      section.classList.remove("star-released");
    } else {
      root.classList.remove("star-at-threshold");
      if (cancelBurst) cancelBurst();
      root.removeAttribute("data-star-phase");
    }
    window.dispatchEvent(new CustomEvent("reading:star-mode", { detail: { active: value } }));
  }

  function burst() {
    released = true;
    section.classList.add("star-released");
    if (motion.matches) return;

    // Only words presently on screen move. Original text nodes and glossary
    // controls return after the gesture; there is no duplicate visual text.
    const visible = lines.filter((line) => {
      const rect = line.getBoundingClientRect();
      return rect.bottom > window.innerHeight * 0.15 && rect.top < window.innerHeight * 0.9;
    }).slice(-2);
    const wrappers = [], controls = [], fragments = [];
    for (const line of visible) {
      const voice = line.querySelector(".star-voice");
      const walker = document.createTreeWalker(voice, NodeFilter.SHOW_TEXT, {
        acceptNode(node) {
          return node.parentElement.closest(".gloss-term, .ref, a")
            ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
        },
      });
      const nodes = [];
      while (walker.nextNode()) nodes.push(walker.currentNode);
      for (const node of nodes) {
        const fragment = document.createDocumentFragment();
        for (const word of node.textContent.match(/\s+|\S+/gu) || []) {
          if (/^\s+$/u.test(word)) fragment.append(document.createTextNode(word));
          else {
            const span = document.createElement("span");
            span.className = "star-fragment";
            span.textContent = word;
            wrappers.push(span);
            fragments.push(span);
            fragment.append(span);
          }
        }
        node.replaceWith(fragment);
      }
      for (const term of voice.querySelectorAll(".gloss-term, .ref, a")) {
        term.classList.add("star-fragment");
        controls.push(term);
        fragments.push(term);
      }
    }

    // Read all geometry before starting animations to avoid layout thrashing.
    const positions = fragments.map((el, i) => {
      const r = el.getBoundingClientRect();
      const dx = Math.max(-22, Math.min(22,
        (r.left + r.width / 2 - window.innerWidth / 2) * 0.055 + Math.sin(i * 2.4) * 6));
      const dy = Math.max(-15, Math.min(15,
        (r.top + r.height / 2 - window.innerHeight / 2) * 0.03 + Math.cos(i * 1.7) * 5));
      return { el, dx, dy };
    });
    const animations = positions.map(({ el, dx, dy }, i) => el.animate([
      { left: "0px", top: "0px", opacity: 1 },
      { left: `${dx}px`, top: `${dy}px`, opacity: 0.4, offset: 0.35 },
      { left: "0px", top: "0px", opacity: 1 },
    ], { duration: 720, delay: (i % 7) * 9, easing: "cubic-bezier(.2,.6,.3,1)" }));

    let cleaned = false;
    function cleanup() {
      if (cleaned) return;
      cleaned = true;
      for (const el of wrappers) el.replaceWith(document.createTextNode(el.textContent));
      for (const el of controls) el.classList.remove("star-fragment");
      for (const line of visible) line.querySelector(".star-voice").normalize();
      cancelBurst = null;
    }
    cancelBurst = () => {
      animations.forEach((animation) => animation.cancel());
      cleanup();
    };
    Promise.all(animations.map((animation) => animation.finished.catch(() => {}))).then(cleanup);
  }

  function update() {
    scheduled = false;
    if (returning) return;
    const height = window.innerHeight;
    const rect = section.getBoundingClientRect();
    const buttonRect = button.getBoundingClientRect();
    const atThreshold = buttonRect.top < height * 0.95 && buttonRect.bottom > 0;
    const inside = rect.top < height * 0.65 && rect.bottom > height * 0.25;
    if (!inside) dismissed = false;
    if (atThreshold && window.scrollY > previousY) dismissed = false;
    const entering = !active && inside && !dismissed;
    setActive(inside && !dismissed);
    root.classList.toggle("star-at-threshold", active && atThreshold);
    if (active) {
      let next = "gather";
      for (const group of phases) {
        if (group.getBoundingClientRect().top < height * 0.65) next = group.dataset.starPhase;
      }
      if (entering && next === "after") {
        released = true;
        section.classList.add("star-released");
      }
      root.dataset.starPhase = next;
      if (next === "choice" && !released && window.scrollY >= previousY) burst();
    }
    previousY = window.scrollY;
  }

  function schedule() {
    if (!scheduled) {
      scheduled = true;
      requestAnimationFrame(update);
    }
  }

  function returnToPage() {
    dismissed = true;
    setActive(false);
    window.dispatchEvent(new Event("reading:jump"));
    if (window.__lenis && !motion.matches) {
      window.__lenis.scrollTo(section, { offset: -80, duration: 1.2 });
    } else {
      window.scrollTo({ top: window.scrollY + section.getBoundingClientRect().top - 80,
        behavior: "instant" });
    }
    heading.tabIndex = -1;
    heading.focus({ preventScroll: true });
  }

  async function leaveStar() {
    if (returning || !conclusion) return;
    returning = true;
    button.disabled = true;
    // Playback stays inside the click's user activation, including on mobile.
    window.dispatchEvent(new Event("reading:return"));
    let explosion = null;
    let animations = [];
    if (!motion.matches) {
      explosion = document.createElement("div");
      explosion.className = "star-explosion";
      explosion.setAttribute("aria-hidden", "true");
      const core = document.createElement("div");
      core.className = "star-explosion-core";
      explosion.append(core);
      for (let i = 0; i < 48; i++) {
        const spark = document.createElement("i");
        const angle = i * Math.PI * 2 / 48;
        const distance = Math.max(innerWidth, innerHeight) * (0.45 + (i % 5) * 0.08);
        spark.className = "star-explosion-spark";
        explosion.append(spark);
        animations.push(spark.animate([
          { transform: "translate(-50%, -50%) scale(0)", opacity: 0 },
          { opacity: 0.9, offset: 0.18 },
          { transform: `translate(calc(-50% + ${Math.cos(angle) * distance}px), calc(-50% + ${Math.sin(angle) * distance}px)) scale(0.2)`, opacity: 0 },
        ], { duration: 1200, easing: "cubic-bezier(.12,.65,.25,1)", fill: "forwards" }));
      }
      document.body.append(explosion);
      animations.push(core.animate([
        { transform: "scale(0.015)", opacity: 0 },
        { opacity: 1, offset: 0.3 },
        { transform: "scale(1)", opacity: 1, offset: 0.45 },
        { transform: "scale(1.15)", opacity: 0 },
      ], { duration: 1400, easing: "ease-out", fill: "forwards" }));
      // Cross to the conclusion behind the expanding light, then let it clear.
      await new Promise((resolve) => setTimeout(resolve, 520));
    }
    dismissed = true;
    setActive(false);
    root.classList.remove("star-sealed");
    window.__lenis?.resize();
    window.ScrollTrigger?.refresh();
    window.dispatchEvent(new Event("reading:jump"));
    if (window.__lenis) window.__lenis.scrollTo(conclusion, { offset: -40, immediate: true });
    else window.scrollTo({ top: scrollY + conclusion.getBoundingClientRect().top - 40, behavior: "instant" });
    const title = conclusion.querySelector("h2") || conclusion;
    title.tabIndex = -1;
    title.focus({ preventScroll: true });
    await Promise.all(animations.map((animation) => animation.finished.catch(() => {})));
    explosion?.remove();
    button.disabled = false;
    returning = false;
    schedule();
  }

  button.addEventListener("click", () => {
    leaveStar();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape" || !active || returning) return;
    // Let a definition, mobile menu or voice panel consume its own Escape.
    if (document.querySelector('#term-tooltip:not([hidden]), [data-model-panel]:not([hidden]), #mobile-sheet.open, #tts-voice-panel.open')) return;
    e.preventDefault();
    returnToPage();
  }, true);
  window.addEventListener("scroll", schedule, { passive: true });
  window.addEventListener("resize", schedule, { passive: true });
  window.addEventListener("load", schedule);
  motion.addEventListener("change", () => {
    if (motion.matches && cancelBurst) cancelBurst();
  });
  schedule();
})();
