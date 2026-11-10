/* Haste gathers ice; an unhurried page gives it back to the current.
   Native scroll position works with Lenis, touch, keys and the scrollbar.
   Nothing here changes text metrics or takes control of scrolling. */
(function () {
  "use strict";

  const canvas = document.getElementById("frost-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  const root = document.documentElement;
  const motion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const clamp = (n, lo = 0, hi = 1) => Math.max(lo, Math.min(hi, n));
  let width = 0, height = 0, band = 0;
  let branches = [];
  let ice = 0, velocity = 0;
  let previousY = window.scrollY, previousTime = 0;
  let paintedAt = 0, published = -1, frame = 0, ignoreUntil = 0;
  window.readingIce = 0;

  // A fixed seed: crystals grow and melt along the same branches, without
  // regenerating noise or flickering while the reader holds still.
  function makeBranches() {
    let seed = 71931;
    const random = () => {
      seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
      return seed / 4294967296;
    };
    const segments = [];
    function twig(x, y, angle, length, depth, start) {
      const steps = depth ? 6 : 3;
      const step = length / steps;
      for (let i = 0; i < steps; i++) {
        const nx = x + Math.cos(angle) * step;
        const ny = y + Math.sin(angle) * step;
        const at = start + i * 0.072;
        segments.push({ x, y, nx, ny, at, thin: depth ? 0.85 : 0.5 });
        if (depth && (i === 2 || i === 4)) {
          for (const side of [-1, 1]) {
            twig(nx, ny, angle + side * Math.PI / 3,
              length * (0.24 + random() * 0.12), depth - 1, at + 0.055);
          }
        }
        x = nx; y = ny;
      }
    }
    for (let edge = 0; edge < 4; edge++) {
      const span = edge < 2 ? height : width;
      const count = Math.ceil(span / 48);
      for (let i = 0; i < count; i++) {
        const along = (i + 0.2 + random() * 0.6) * span / count;
        const x = edge === 0 ? -2 : edge === 1 ? width + 2 : along;
        const y = edge === 2 ? -2 : edge === 3 ? height + 2 : along;
        const angle = [0, Math.PI, Math.PI / 2, -Math.PI / 2][edge];
        twig(x, y, angle, band * (0.5 + random() * 0.45), 2,
          0.025 + random() * 0.2);
      }
    }
    return segments;
  }

  function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    band = clamp(width * 0.095, 32, 125);
    const density = Math.min(window.devicePixelRatio || 1, 1.5);
    canvas.width = Math.round(width * density);
    canvas.height = Math.round(height * density);
    ctx.setTransform(density, 0, 0, density, 0, 0);
    branches = makeBranches();
    previousY = window.scrollY;
    // Resizing / rotation can reflow a long chapter by several screens.
    ignoreUntil = performance.now() + 350;
    paint();
  }

  function publish() {
    window.readingIce = ice;
    if (ice === published || (Math.abs(ice - published) < 0.003 && ice !== 0)) return;
    published = ice;
    root.style.setProperty("--reading-ice", ice.toFixed(3));
    root.style.setProperty("--reading-stroke", `${(ice * 0.16).toFixed(3)}px`);
    root.style.setProperty("--reading-softness", `${((1 - ice) * 0.32).toFixed(3)}px`);
  }

  function paint() {
    ctx.clearRect(0, 0, width, height);
    publish();
    if (ice < 0.003) return;

    // Mist stays in the margins, leaving the reading column uncovered.
    for (let edge = 0; edge < 4; edge++) {
      const vertical = edge < 2;
      const depth = band * (vertical ? 1 : 0.7);
      const x = edge === 1 ? width : 0;
      const y = edge === 3 ? height : 0;
      const gradient = ctx.createLinearGradient(x, y,
        x + (vertical ? (edge === 0 ? depth : -depth) : 0),
        y + (vertical ? 0 : (edge === 2 ? depth : -depth)));
      gradient.addColorStop(0, `rgba(205, 224, 225, ${ice * 0.26})`);
      gradient.addColorStop(0.38, `rgba(189, 215, 220, ${ice * 0.09})`);
      gradient.addColorStop(1, "rgba(189, 215, 220, 0)");
      ctx.fillStyle = gradient;
      ctx.fillRect(vertical && edge === 1 ? width - depth : 0,
        !vertical && edge === 3 ? height - depth : 0,
        vertical ? depth : width, vertical ? height : depth);
    }

    ctx.lineCap = "butt";
    ctx.strokeStyle = `rgba(217, 235, 238, ${ice * 0.64})`;
    // Two batched paths rather than thousands of individual draw calls.
    for (const thin of [0.5, 0.85]) {
      ctx.lineWidth = thin;
      ctx.beginPath();
      for (const branch of branches) {
        if (branch.thin !== thin) continue;
        const grown = clamp((ice - branch.at) / 0.23);
        if (!grown) continue;
        ctx.moveTo(branch.x, branch.y);
        ctx.lineTo(branch.x + (branch.nx - branch.x) * grown,
          branch.y + (branch.ny - branch.y) * grown);
      }
      ctx.stroke();
    }
  }

  function tick(now) {
    frame = 0;
    const dt = clamp((now - previousTime) / 1000, 0.001, 0.064);
    previousTime = now;
    const y = window.scrollY;
    const distance = Math.abs(y - previousY);
    previousY = y;
    // Screens/second makes the same gesture comparable on a phone and a
    // desktop. Cap big deltas (including scrollbar drags); navigation
    // announces itself separately instead of masquerading as haste.
    const raw = now < ignoreUntil
      ? 0 : Math.min(6, distance / Math.max(height, 1) / dt);
    velocity += (raw - velocity) * (1 - Math.exp(-dt / 0.14));
    const haste = clamp((velocity - 0.55) / 2);
    ice = clamp(ice + (haste > 0.03 ? haste * 0.8 : -0.19) * dt);
    window.readingIce = ice;
    if (now - paintedAt > 32 || ice === 0) {
      paint();
      paintedAt = now;
    }
    if (ice > 0 || velocity > 0.01 || distance > 0) {
      frame = requestAnimationFrame(tick);
    }
  }

  function wake() {
    if (motion.matches || document.hidden || frame) return;
    previousTime = performance.now() - 16;
    frame = requestAnimationFrame(tick);
  }

  function reset() {
    cancelAnimationFrame(frame);
    frame = 0;
    ice = velocity = 0;
    previousY = window.scrollY;
    paint();
  }

  window.addEventListener("scroll", wake, { passive: true });
  window.addEventListener("resize", resize, { passive: true });
  window.addEventListener("reading:jump", () => {
    ignoreUntil = performance.now() + 1800;
    velocity = 0;
  });
  document.addEventListener("visibilitychange", reset);
  motion.addEventListener("change", reset);
  resize();
})();
