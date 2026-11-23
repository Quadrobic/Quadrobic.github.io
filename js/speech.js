/* Speech playback and voice selection. No synthesis runs until requested. */
(function () {
  "use strict";
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const lenis = window.__lenis || null;

  /* ---------------- text-to-speech: "listen to the treatise" ---------------- */
  /* Walks the content in document order, queues one SpeechSynthesisUtterance
     per block (paragraph, axiom...), highlights whichever
     one is currently being read, and gently scrolls it into view if it has
     drifted off-screen. No audio files, no server: the browser's own
     speechSynthesis API, chunked per-block so long sections don't hit the
     well-known "utterances over ~15s silently stop" bug in Chrome. */

  (function setupTTS() {
    const btn = document.getElementById("tts-toggle");
    const wrap = document.getElementById("tts-wrap");
    const voiceBtn = document.getElementById("tts-voice-btn");
    const voicePanel = document.getElementById("tts-voice-panel");
    const PAGE_LANG = document.documentElement.lang || "ru";
    // Thai speech synthesis support is bad enough across browsers/OSes
    // (missing voices, mangled pronunciation) that offering the feature
    // does more harm than leaving it off entirely on this page.
    if (!btn || !("speechSynthesis" in window) || PAGE_LANG === "th") {
      if (wrap) wrap.style.display = "none";
      return;
    }

    const SELECTOR = [
      ".hero-title",
      ".hero-subtitle",
      ".preamble p",
      ".book-divider .book-title",
      "h3",
      ".passage p",
      ".passage-list li",
      "li.axiom",
      ".book-body p",
      "p.invocation",
    ].join(", ");

    const BCP47 = { ru: "ru-RU", en: "en-US", th: "th-TH" }[PAGE_LANG] || "ru-RU";

    let items = null; // [{el, text}], built lazily on first play
    let voice = null;
    let voiceOptions = []; // every installed voice matching PAGE_LANG
    let voiceOptionsSig = ""; // cheap signature, avoids rebuilding the panel on every poll
    let idx = 0;
    let state = "idle"; // idle | reading | paused
    let currentUtterance = null; // kept referenced on purpose, see speakFrom()
    let watchdog = null;

    const VOICE_KEY = "iqj-tts-voice-" + PAGE_LANG;
    const RATE_KEY = "iqj-tts-rate";
    // Language-neutral labels (×-multiplier) so this needs no translation
    // table; 0.98 is the original hardcoded default, kept as the "normal" step.
    const RATE_OPTIONS = [
      { value: 0.8, label: "0.8×" },
      { value: 0.98, label: "1×" },
      { value: 1.15, label: "1.15×" },
      { value: 1.35, label: "1.35×" },
    ];
    const PANEL_LABELS = PAGE_LANG === "en"
      ? { speed: "Speed", voice: "Voice" }
      : { speed: "Скорость", voice: "Голос" };
    let rate = RATE_OPTIONS[1].value;
    try {
      const saved = parseFloat(localStorage.getItem(RATE_KEY));
      if (RATE_OPTIONS.some((r) => r.value === saved)) rate = saved;
    } catch (e) {}

    function pickVoice() {
      const voices = speechSynthesis.getVoices();
      voiceOptions = voices.filter((v) => v.lang && v.lang.toLowerCase().startsWith(PAGE_LANG));

      const sig = voiceOptions.map((v) => v.voiceURI).join("|");
      if (sig === voiceOptionsSig) {
        // Same voice list as last time - still make sure `voice` itself
        // points at one of today's actual Voice objects (some browsers
        // hand out fresh objects on every getVoices() call).
        if (voice) voice = voiceOptions.find((v) => v.voiceURI === voice.voiceURI) || voice;
      } else {
        voiceOptionsSig = sig;
        let saved = null;
        try { saved = localStorage.getItem(VOICE_KEY); } catch (e) {}
        voice = (saved && voiceOptions.find((v) => v.voiceURI === saved)) || voiceOptions[0] || null;
        renderVoicePanel();
      }
    }

    function renderVoicePanel() {
      if (!voiceBtn || !voicePanel) return;
      // The button now always opens at least the speed control, regardless
      // of how many voices this browser/OS happens to install.
      voiceBtn.hidden = false;
      voicePanel.innerHTML = "";

      const speedLabel = document.createElement("div");
      speedLabel.className = "tts-panel-label";
      speedLabel.textContent = PANEL_LABELS.speed;
      voicePanel.appendChild(speedLabel);

      const speedRow = document.createElement("div");
      speedRow.className = "tts-speed-row";
      RATE_OPTIONS.forEach((opt) => {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "tts-speed-option";
        b.setAttribute("role", "menuitemradio");
        b.textContent = opt.label;
        const isActive = opt.value === rate;
        b.setAttribute("aria-checked", isActive ? "true" : "false");
        b.classList.toggle("active", isActive);
        b.addEventListener("click", () => {
          rate = opt.value;
          try { localStorage.setItem(RATE_KEY, String(rate)); } catch (e) {}
          renderVoicePanel();
          // Rate only takes effect on the utterance that's about to start,
          // so restart the current block to make the change audible right away.
          if (state === "reading") speakFrom(idx);
        });
        speedRow.appendChild(b);
      });
      voicePanel.appendChild(speedRow);

      if (voiceOptions.length < 2) return;

      const voiceLabel = document.createElement("div");
      voiceLabel.className = "tts-panel-label";
      voiceLabel.textContent = PANEL_LABELS.voice;
      voicePanel.appendChild(voiceLabel);

      voiceOptions.forEach((v) => {
        const row = document.createElement("button");
        row.type = "button";
        row.className = "tts-voice-option";
        row.setAttribute("role", "menuitemradio");
        row.textContent = v.name.replace(/\s*\([^)]*\)\s*$/, ""); // trim "(ru-RU)" suffixes some browsers add
        row.title = v.name;
        const isActive = !!voice && v.voiceURI === voice.voiceURI;
        row.setAttribute("aria-checked", isActive ? "true" : "false");
        row.classList.toggle("active", isActive);
        row.addEventListener("click", () => {
          voice = v;
          try { localStorage.setItem(VOICE_KEY, v.voiceURI); } catch (e) {}
          renderVoicePanel();
          closeVoicePanel();
          // Changing voice mid-sentence isn't possible with this API; the
          // next-best thing is restarting the current block so the choice
          // is actually audible right away instead of waiting.
          if (state === "reading") speakFrom(idx);
        });
        voicePanel.appendChild(row);
      });
    }

    function openVoicePanel() {
      if (!voiceBtn || !voicePanel || voiceBtn.hidden) return;
      voicePanel.hidden = false;
      requestAnimationFrame(() => {
        voicePanel.classList.add("open");
        voiceBtn.classList.add("open");
      });
      voiceBtn.setAttribute("aria-expanded", "true");
      document.addEventListener("click", onDocClickCloseVoicePanel, true);
      document.addEventListener("keydown", onEscCloseVoicePanel);
    }

    function closeVoicePanel() {
      if (!voiceBtn || !voicePanel) return;
      voicePanel.classList.remove("open");
      voiceBtn.classList.remove("open");
      voiceBtn.setAttribute("aria-expanded", "false");
      document.removeEventListener("click", onDocClickCloseVoicePanel, true);
      document.removeEventListener("keydown", onEscCloseVoicePanel);
      setTimeout(() => {
        if (!voicePanel.classList.contains("open")) voicePanel.hidden = true;
      }, 250);
    }

    function onDocClickCloseVoicePanel(e) {
      if (wrap && !wrap.contains(e.target)) closeVoicePanel();
    }
    function onEscCloseVoicePanel(e) {
      if (e.key === "Escape") closeVoicePanel();
    }

    if (voiceBtn) {
      voiceBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        if (voicePanel.classList.contains("open")) closeVoicePanel();
        else openVoicePanel();
      });
    }

    // Render immediately so the speed control is usable right away, without
    // waiting on the (sometimes slow/async) voice list to resolve first.
    renderVoicePanel();
    pickVoice();
    if ("onvoiceschanged" in speechSynthesis) {
      speechSynthesis.onvoiceschanged = pickVoice;
    }
    // Firefox doesn't always fire onvoiceschanged even though it loads the
    // voice list asynchronously, so poll a couple of times early on too.
    [300, 1000, 2500].forEach((ms) => setTimeout(pickVoice, ms));

    function extractText(el) {
      const clone = el.cloneNode(true);
      clone.querySelectorAll("br").forEach((br) => br.replaceWith(" "));
      let text = clone.textContent.replace(/\s+/g, " ").trim();
      if (el.classList.contains("axiom")) text = text.replace(/^△\s*/, "");
      return text;
    }

    function buildItems() {
      items = Array.from(document.querySelectorAll(SELECTOR))
        .filter((el) => el.getClientRects().length > 0)
        .map((el) => ({ el, text: extractText(el) }))
        .filter((it) => it.text.length > 0);
    }

    function clearHighlight() {
      document.querySelectorAll(".tts-active").forEach((el) => el.classList.remove("tts-active"));
    }

    function revealCurrent(el) {
      if (reduceMotion) return;
      const rect = el.getBoundingClientRect();
      if (rect.top > 80 && rect.bottom < window.innerHeight - 80) return;
      window.dispatchEvent(new Event("reading:jump"));
      if (lenis) lenis.scrollTo(el, { offset: -window.innerHeight * 0.35, duration: 1.0 });
      else el.scrollIntoView({ behavior: "smooth", block: "center" });
    }

    function setBtnState(reading) {
      btn.classList.toggle("on", reading);
      btn.setAttribute("aria-pressed", reading ? "true" : "false");
    }

    function speakFrom(i) {
      if (!items || i >= items.length) {
        stop();
        return;
      }
      idx = i;
      const item = items[idx];

      pickVoice(); // re-check right before speaking, in case it just loaded
      const utter = new SpeechSynthesisUtterance(item.text);
      utter.lang = BCP47;
      if (voice) utter.voice = voice;
      utter.rate = rate;
      // Firefox is known to garbage-collect SpeechSynthesisUtterance objects
      // that nothing in JS still references, cutting speech off mid-queue.
      // Keeping this assignment alive for the duration is the standard fix.
      currentUtterance = utter;

      let started = false;
      utter.onstart = () => {
        // Highlighting/scrolling here, not before speak() is called, keeps
        // the page in sync with what's actually audible: speak() can have
        // a noticeable startup lag, and doing this eagerly made the page
        // visibly jump ahead of the voice still finishing the prior block.
        started = true;
        clearTimeout(watchdog);
        clearHighlight();
        item.el.classList.add("tts-active");
        revealCurrent(item.el);
      };
      utter.onend = () => {
        clearTimeout(watchdog);
        if (state === "reading") speakFrom(idx + 1);
      };
      utter.onerror = () => {
        clearTimeout(watchdog);
        if (state === "reading") speakFrom(idx + 1);
      };
      speechSynthesis.speak(utter);

      // Some browsers (seen on Firefox) silently drop an utterance without
      // ever firing start/end/error — missing voice, a stale voice
      // reference, or the GC issue above. Rather than hang forever on one
      // click, skip ahead if nothing happened after a few seconds.
      clearTimeout(watchdog);
      watchdog = setTimeout(() => {
        if (!started && state === "reading" && idx === i) speakFrom(i + 1);
      }, 4000);
    }

    function start() {
      if (!items) buildItems();
      if (!items.length) return;
      state = "reading";
      setBtnState(true);
      speakFrom(0);
    }

    function pause() {
      // The native speechSynthesis.pause()/resume() pair is unreliable
      // across browsers (resume() silently doing nothing is a long-known
      // issue). Pausing is done ourselves instead: cancel the current
      // utterance outright and simply remember which block we were on;
      // resume() just re-speaks that same block. Block-level granularity
      // (not mid-sentence) is the trade-off, in exchange for it actually
      // working reliably every time.
      state = "paused";
      setBtnState(false);
      clearTimeout(watchdog);
      speechSynthesis.cancel();
    }

    function resume() {
      if (!items) return;
      state = "reading";
      setBtnState(true);
      speakFrom(idx);
    }

    function stop() {
      state = "idle";
      setBtnState(false);
      clearTimeout(watchdog);
      speechSynthesis.cancel();
      currentUtterance = null;
      clearHighlight();
      idx = 0;
    }

    btn.addEventListener("click", () => {
      if (state === "idle") start();
      else if (state === "reading") pause();
      else resume();
    });

    // Deliberately no visibilitychange handler: switching tabs should not
    // stop the reading, and modern browsers keep speechSynthesis running
    // in a backgrounded tab just fine.
    window.addEventListener("beforeunload", () => speechSynthesis.cancel());
  })();

})();
