/* Ambient audio and text size; usable independently of scroll animations. */
(function () {
  "use strict";

  /* ---------------- ambient sound toggle ---------------- */
  /* A generated drone + filtered noise for the riverbed. After §38's
     Return button, the same sound control pauses/resumes alquadro.mp3.
     Music starts on Return or a one-time request from the final story link. */

  (function setupSound() {
    const btn = document.getElementById("sound-toggle");
    if (!btn) return;
    let ctx = null;
    let nodes = null;
    let on = false;
    const music = document.getElementById("return-music");
    let musicMode = false;
    const originalTitle = btn.title;
    const originalLabel = btn.getAttribute("aria-label");
    const musicLabels = {
      ru: ["Продолжить музыку", "Приостановить музыку"],
      en: ["Resume music", "Pause music"],
      th: ["เล่นเพลงต่อ", "หยุดเพลงชั่วคราว"],
    }[document.documentElement.lang] || ["Resume music", "Pause music"];

    function setSoundState(playing) {
      btn.classList.toggle("on", playing);
      btn.setAttribute("aria-pressed", String(playing));
      btn.title = musicMode ? musicLabels[playing ? 1 : 0] : originalTitle;
      btn.setAttribute("aria-label", musicMode ? btn.title : originalLabel);
    }

    function fadeAmbient(target) {
      if (!ctx || !nodes) return;
      nodes.master.gain.cancelScheduledValues(ctx.currentTime);
      nodes.master.gain.linearRampToValueAtTime(target, ctx.currentTime + 1.2);
    }

    function playMusic() {
      if (music.ended) music.currentTime = 0;
      const attempt = music.play();
      if (attempt) attempt.catch(() => setSoundState(false));
    }

    if (music) {
      music.volume = 0.65;
      music.addEventListener("play", () => { if (musicMode) setSoundState(true); });
      music.addEventListener("pause", () => { if (musicMode) setSoundState(false); });
      music.addEventListener("error", () => { if (musicMode) setSoundState(false); });
      music.addEventListener("ended", () => {
        musicMode = false;
        setSoundState(false);
      });
      window.addEventListener("reading:return", () => {
        if (music.getAttribute("src") !== "audio/alquadro.mp3") music.src = "audio/alquadro.mp3";
        musicMode = true;
        on = false;
        fadeAmbient(0);
        // Repeated returns use this same player; no overlapping copies.
        playMusic();
      });
    }

    // Consume a short-lived, per-tab request from the story's final link.
    if (music && /\/index(?:\.(?:en|th))?\.html$/.test(location.pathname)) {
      let request;
      try {
        request = JSON.parse(sessionStorage.getItem('iqj-yard-music') || 'null');
        sessionStorage.removeItem('iqj-yard-music');
      } catch (_) {}
      if (request && request.path === location.pathname &&
          Date.now() >= request.at && Date.now() - request.at < 30000) {
        music.src = 'audio/sap.mp3';
        musicMode = true;
        playMusic();
      }

    }

    function build() {
      ctx = new (window.AudioContext || window.webkitAudioContext)();
      const master = ctx.createGain();
      master.gain.value = 0;
      master.connect(ctx.destination);

      // low drone
      const osc1 = ctx.createOscillator();
      osc1.type = "sine";
      osc1.frequency.value = 55;
      const osc2 = ctx.createOscillator();
      osc2.type = "sine";
      osc2.frequency.value = 82.5;
      const droneGain = ctx.createGain();
      droneGain.gain.value = 0.25;
      osc1.connect(droneGain);
      osc2.connect(droneGain);

      // filtered noise (river texture)
      const bufferSize = 2 * ctx.sampleRate;
      const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) data[i] = Math.random() * 2 - 1;
      const noise = ctx.createBufferSource();
      noise.buffer = buffer;
      noise.loop = true;
      const noiseFilter = ctx.createBiquadFilter();
      noiseFilter.type = "bandpass";
      noiseFilter.frequency.value = 700;
      noiseFilter.Q.value = 0.6;
      const noiseGain = ctx.createGain();
      noiseGain.gain.value = 0.06;
      noise.connect(noiseFilter).connect(noiseGain);

      // slow LFO breathing the filter
      const lfo = ctx.createOscillator();
      lfo.type = "sine";
      lfo.frequency.value = 0.06;
      const lfoGain = ctx.createGain();
      lfoGain.gain.value = 260;
      lfo.connect(lfoGain).connect(noiseFilter.frequency);

      droneGain.connect(master);
      noiseGain.connect(master);

      osc1.start();
      osc2.start();
      noise.start();
      lfo.start();

      nodes = { master };
    }

    btn.addEventListener("click", () => {
      if (musicMode) {
        if (music.paused) playMusic();
        else music.pause();
        return;
      }
      if (!ctx) build();
      on = !on;
      setSoundState(on);
      fadeAmbient(on ? 0.55 : 0);
      if (ctx.state === "suspended") ctx.resume();
    });
  })();

  /* ---------------- text size: reading comfort (A- / A+) ---------------- */

  (function setupTextScale() {
    const dec = document.getElementById("text-size-dec");
    const inc = document.getElementById("text-size-inc");
    if (!dec || !inc) return;

    const KEY = "iqj-text-scale";
    const MIN = 0.85;
    const MAX = 1.4;
    const STEP = 0.1;
    const root = document.documentElement;

    let scale = parseFloat(localStorage.getItem(KEY));
    if (!scale || isNaN(scale)) scale = 1;
    scale = Math.min(MAX, Math.max(MIN, scale));

    function apply() {
      root.style.setProperty("--text-scale", scale.toFixed(2));
      dec.disabled = scale <= MIN + 1e-9;
      inc.disabled = scale >= MAX - 1e-9;
      try { localStorage.setItem(KEY, scale.toFixed(2)); } catch (e) {}
      // layout heights shift with font size, so scroll-triggered reveals
      // need to recompute against the new geometry
      requestAnimationFrame(() => window.ScrollTrigger?.refresh());
    }

    dec.addEventListener("click", () => {
      window.dispatchEvent(new Event("reading:jump"));
      scale = Math.max(MIN, Math.round((scale - STEP) * 100) / 100);
      apply();
    });
    inc.addEventListener("click", () => {
      window.dispatchEvent(new Event("reading:jump"));
      scale = Math.min(MAX, Math.round((scale + STEP) * 100) / 100);
      apply();
    });

    apply();
  })();

})();
