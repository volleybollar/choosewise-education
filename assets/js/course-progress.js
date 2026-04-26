// course-progress.js
// Manages course progression state (presentationsteknik).
//
// localStorage keys (one set per language):
//   presentationsteknik-sv-progress       → JSON array of 7 statuses
//                                           ("done" | "current" | "not-started")
//   presentationsteknik-sv-mod{N}-{slug}  → individual exercise answers
//                                           (handled by course-exercises.js)
//
// API:
//   CourseProgress.init(lang)
//   CourseProgress.getStatus(modIndex)         → "done"|"current"|"not-started"
//   CourseProgress.setCurrent(modIndex)        → marks others "done" up to N-1
//   CourseProgress.markDone(modIndex)
//   CourseProgress.reset()
//   CourseProgress.renderTopbar(containerEl, currentMod)
//   CourseProgress.renderOverview(containerEl)

(function (global) {
  const TOTAL_MODULES = 7;
  let LANG = 'sv';
  let STORAGE_KEY = 'presentationsteknik-sv-progress';

  const MODULE_TITLES = {
    sv: [
      'Varför presentationsteknik?',
      'Designa diabilder — grunderna',
      'När diabilden krockar med dig',
      'Framförandet — närvaro i rummet',
      'Digitala presentationer',
      'Röst, kropp och språk',
      'Din checklista',
    ],
    en: [
      'Why presentation skills?',
      'Designing slides — the basics',
      'When the slide gets in your way',
      'Delivery — presence in the room',
      'Digital presentations',
      'Voice, body and language',
      'Your checklist',
    ],
  };

  const MODULE_URLS = {
    sv: [
      '/sv/presentationsteknik/modul-1/',
      '/sv/presentationsteknik/modul-2/',
      '/sv/presentationsteknik/modul-3/',
      '/sv/presentationsteknik/modul-4/',
      '/sv/presentationsteknik/modul-5/',
      '/sv/presentationsteknik/modul-6/',
      '/sv/presentationsteknik/modul-7/',
    ],
    en: [
      '/presentation-skills/module-1/',
      '/presentation-skills/module-2/',
      '/presentation-skills/module-3/',
      '/presentation-skills/module-4/',
      '/presentation-skills/module-5/',
      '/presentation-skills/module-6/',
      '/presentation-skills/module-7/',
    ],
  };

  function defaultProgress() {
    return Array(TOTAL_MODULES).fill('not-started');
  }

  function load() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return defaultProgress();
      const parsed = JSON.parse(raw);
      if (!Array.isArray(parsed) || parsed.length !== TOTAL_MODULES) {
        return defaultProgress();
      }
      return parsed;
    } catch {
      return defaultProgress();
    }
  }

  function save(state) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch { /* localStorage might be disabled — silently no-op */ }
  }

  const CourseProgress = {
    init(lang) {
      LANG = lang || 'sv';
      STORAGE_KEY = `presentationsteknik-${LANG}-progress`;
    },

    // Returns a fresh array each call (callers cannot mutate stored state).
    getState() { return load(); },

    getStatus(modIndex) {
      const state = load();
      return state[modIndex - 1] || 'not-started';
    },

    setCurrent(modIndex) {
      const state = load();
      // If the target is already marked done, don't downgrade it.
      if (state[modIndex - 1] === 'done') return;
      // Mark all earlier modules done (if they weren't already) so the
      // progressionsbar renders consistently — but never touch modules
      // *after* the target. A user revisiting an earlier module shouldn't
      // lose their forward progress.
      for (let i = 0; i < modIndex - 1; i++) {
        if (state[i] !== 'done') state[i] = 'done';
      }
      state[modIndex - 1] = 'current';
      save(state);
    },

    markDone(modIndex) {
      const state = load();
      state[modIndex - 1] = 'done';
      save(state);
    },

    reset() {
      try { localStorage.removeItem(STORAGE_KEY); } catch { }
    },

    /* Renders inside an element with class "module-topbar__progress".
       currentMod = which module is "you are here" on this page. */
    renderTopbar(containerEl, currentMod) {
      const state = load();
      // Side effect: visiting a module page implicitly marks it as "current"
      // in storage so the översiktsvyn (and other pages' topbars) reflect
      // where the user is. Don't downgrade modules that are already "done".
      if (state[currentMod - 1] !== 'done') {
        state[currentMod - 1] = 'current';
        save(state);
      }
      const titles = MODULE_TITLES[LANG];
      const urls = MODULE_URLS[LANG];
      containerEl.innerHTML = '';
      for (let i = 0; i < TOTAL_MODULES; i++) {
        const mod = i + 1;
        const status = (mod === currentMod) ? 'current' : state[i];
        const dot = document.createElement('a');
        dot.className = 'module-topbar__progress-dot';
        if (status === 'done') dot.classList.add('module-topbar__progress-dot--done');
        if (status === 'current') {
          dot.classList.add('module-topbar__progress-dot--current');
          dot.setAttribute('aria-current', 'page');
        }
        dot.href = urls[i];
        dot.title = `Modul ${mod} — ${titles[i]}`;
        dot.setAttribute('aria-label', `Modul ${mod}: ${titles[i]}`);
        dot.textContent = mod;
        containerEl.appendChild(dot);

        if (i < TOTAL_MODULES - 1) {
          // Connector line lights up green ("done") when its left-side dot is
          // done. This gives the visual sense of progression flowing left to
          // right through completed material.
          const line = document.createElement('span');
          line.className = 'module-topbar__progress-line';
          if (status === 'done') line.classList.add('module-topbar__progress-line--done');
          containerEl.appendChild(line);
        }
      }
    },

    /* Renders the bigger 28px progressionsstege on översiktsvyn.
       containerEl has class "course-progress". */
    renderOverview(containerEl) {
      const state = load();
      const titles = MODULE_TITLES[LANG];
      const urls = MODULE_URLS[LANG];
      containerEl.innerHTML = '';
      for (let i = 0; i < TOTAL_MODULES; i++) {
        const mod = i + 1;
        const status = state[i];

        const step = document.createElement('div');
        step.className = 'course-progress__step';

        const dot = document.createElement('a');
        dot.className = 'course-progress__dot';
        if (status === 'done') dot.classList.add('course-progress__dot--done');
        if (status === 'current') dot.classList.add('course-progress__dot--current');
        dot.href = urls[i];
        dot.title = `Modul ${mod} — ${titles[i]}`;
        dot.setAttribute('aria-label', `Modul ${mod}: ${titles[i]}`);
        dot.textContent = mod;
        step.appendChild(dot);
        containerEl.appendChild(step);

        if (i < TOTAL_MODULES - 1) {
          const line = document.createElement('span');
          line.className = 'course-progress__line';
          if (status === 'done') line.classList.add('course-progress__line--done');
          containerEl.appendChild(line);
        }
      }
    },
  };

  global.CourseProgress = CourseProgress;
})(window);
