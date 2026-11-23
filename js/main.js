/*
 * Scroll orchestration: Lenis (smooth momentum scroll) driving GSAP's
 * ticker, ScrollTrigger firing the reveal / mood / nav work off that same
 * clock. Audio/text controls live in reader-controls.js; speech in speech.js.
 * Script order is declared in template.html and bird_template.html.
 */
(function () {
  "use strict";

  const reduceMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  // Lenis owns scroll position; the browser's own jump-to-#hash on load
  // races it and used to leave the page blank at a deep link. Take manual
  // control and replay the jump ourselves once everything below is ready.
  if ("scrollRestoration" in history) history.scrollRestoration = "manual";
  const initialHash = location.hash ? location.hash.slice(1) : null;
  window.scrollTo(0, 0);

  /* ---------------- language switch ---------------- */
  /* The head bootstrap script (template.html) handles geolocation and
     redirecting; this just highlights the current language and remembers
     an explicit click so it sticks on the next visit. */
  (function setupLangSwitch() {
    const nav = document.getElementById("lang-switch");
    if (!nav) return;
    const current = document.documentElement.lang || "ru";
    nav.querySelectorAll("a").forEach((a) => {
      a.classList.toggle("active", a.dataset.lang === current);
      a.addEventListener("click", () => {
        try { localStorage.setItem("iqj-lang", a.dataset.lang); } catch (e) {}
      });
    });
  })();

  /* ---------------- mobile menu sheet ---------------- */
  /* Below the 720px breakpoint, style.css turns the side nav and the four
     utility buttons from individually fixed elements into normal content
     inside #mobile-sheet - this just drives opening and closing it. The
     nav links and buttons inside keep working exactly as they already
     did (their own listeners are set up elsewhere in this file and don't
     care where in the DOM their element currently sits). */
  (function setupMobileSheet() {
    const menuBtn = document.getElementById("mobile-menu-btn");
    const sheet = document.getElementById("mobile-sheet");
    const backdrop = document.getElementById("mobile-sheet-backdrop");
    if (!menuBtn || !sheet || !backdrop) return;

    function isOpen() {
      return sheet.classList.contains("open");
    }
    function open() {
      sheet.classList.add("open");
      backdrop.classList.add("open");
      menuBtn.setAttribute("aria-expanded", "true");
      document.addEventListener("keydown", onEsc);
    }
    function close() {
      sheet.classList.remove("open");
      backdrop.classList.remove("open");
      menuBtn.setAttribute("aria-expanded", "false");
      document.removeEventListener("keydown", onEsc);
    }
    function onEsc(e) {
      if (e.key === "Escape") close();
    }

    menuBtn.addEventListener("click", () => (isOpen() ? close() : open()));
    backdrop.addEventListener("click", close);

    // Picking a book from the list is a "navigate away" action - closing
    // the sheet so the reader actually sees the section scroll into view.
    // The utility buttons (sound/voice/pdf/text size) stay open on click:
    // those are often pressed more than once in a row (A- / A+ especially),
    // and closing on every tap would mean reopening the sheet each time.
    sheet.addEventListener("click", (e) => {
      if (e.target.closest(".nav-dot")) close();
    });

    // A rotation or a resize across the 720px breakpoint shouldn't leave
    // the sheet stuck open underneath the now-desktop layout.
    window.addEventListener("resize", () => {
      if (isOpen() && window.innerWidth > 720) close();
    });
  })();

  gsap.registerPlugin(ScrollTrigger);

  /* ---------------- Lenis smooth scroll ---------------- */

  let lenis = null;
  if (!reduceMotion) {
    lenis = new Lenis({
      duration: 1.1,
      easing: (t) => 1 - Math.pow(1 - t, 3),
      smoothWheel: true,
    });
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add((time) => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);
  }

  window.__lenis = lenis;

  function scrollToTarget(id) {
    const sealed = document.documentElement.classList.contains("star-sealed");
    const el = sealed && (id === "conclusion" || id === "practices" || id === "p39" || id === "afterword")
      ? document.querySelector(".star-return") : document.getElementById(id);
    if (!el) return;
    window.dispatchEvent(new Event("reading:jump"));
    if (lenis) lenis.scrollTo(el, { offset: 0, duration: 1.3 });
    else el.scrollIntoView({ behavior: "smooth" });
  }

  /* ---------------- paragraph / list reveals ---------------- */

  gsap.utils.toArray(".reveal").forEach((el) => {
    const inStar = !!el.closest("[data-star-reading]");
    if (reduceMotion) {
      el.style.opacity = 1;
      el.style.transform = "none";
      return;
    }
    gsap.fromTo(
      el,
      { opacity: 0, y: 28 },
      {
        opacity: 1,
        y: 0,
        duration: inStar ? 2.1 : 0.9,
        ease: "power2.out",
        scrollTrigger: {
          trigger: el,
          start: "top 88%",
          toggleActions: "play none none reverse",
        },
      }
    );
  });

  /* ---------------- chapter dividers ---------------- */

  gsap.utils.toArray(".book-divider").forEach((div) => {
    const roman = div.querySelector(".book-roman");
    const title = div.querySelector(".reveal-title");
    // Not every divider has a roman numeral (Заключение, Садхана,
    // Аксиоматика, Словарь aren't numbered "books"), but the title must
    // still be animated in - otherwise it stays at the CSS default
    // opacity:0 for .reveal-title forever.
    if (!title) return;

    if (roman) gsap.set(roman, { opacity: 0, y: 24 });
    gsap.set(title, { opacity: 0, scale: 0.92, y: 16 });

    if (reduceMotion) {
      gsap.set([roman, title].filter(Boolean), { opacity: 1, y: 0, scale: 1 });
      return;
    }

    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: div,
        start: "top 65%",
        toggleActions: "play none none reverse",
      },
    });
    if (roman) {
      tl.to(roman, { opacity: 1, y: 0, duration: 1.0, ease: "power2.out" }).to(
        title,
        { opacity: 1, scale: 1, y: 0, duration: 1.1, ease: "power3.out" },
        "-=0.55"
      );
    } else {
      tl.to(title, { opacity: 1, scale: 1, y: 0, duration: 1.1, ease: "power3.out" });
    }
  });

  /* ---------------- mood-driven background ---------------- */

  gsap.utils.toArray("[data-mood]").forEach((section) => {
    const mood = section.dataset.mood;
    ScrollTrigger.create({
      trigger: section,
      start: "top 55%",
      end: "bottom 45%",
      onEnter: () => window.setInkMood && window.setInkMood(mood),
      onEnterBack: () => window.setInkMood && window.setInkMood(mood),
    });
  });

  /* ---------------- progress rail ---------------- */

  gsap.to("#progress-fill", {
    width: "100%",
    ease: "none",
    scrollTrigger: {
      trigger: document.body,
      start: "top top",
      end: "bottom bottom",
      scrub: 0.3,
    },
  });

  /* ---------------- side nav: click-to-scroll + active state ---------------- */

  const navDots = gsap.utils.toArray(".nav-dot");
  navDots.forEach((a) => {
    a.addEventListener("click", (e) => {
      e.preventDefault();
      scrollToTarget(a.dataset.target);
    });
  });

  navDots.forEach((a) => {
    const target = document.getElementById(a.dataset.target);
    if (!target) return;
    ScrollTrigger.create({
      trigger: target,
      start: "top 60%",
      end: "bottom 40%",
      onEnter: () => setActiveDot(a),
      onEnterBack: () => setActiveDot(a),
    });
  });

  function setActiveDot(active) {
    navDots.forEach((d) => d.classList.toggle("active", d === active));
  }

  /* ---------------- refresh on load & resize ---------------- */

  window.addEventListener("load", () => {
    ScrollTrigger.refresh();
    if (initialHash) {
      // let one frame pass so ScrollTrigger has real geometry to jump to
      requestAnimationFrame(() => scrollToTarget(initialHash));
    }
  });
})();
