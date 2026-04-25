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
//   CourseProgress.renderOverview(containerEl, currentMod)

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

    getState() { return load(); },

    getStatus(modIndex) {
      const state = load();
      return state[modIndex - 1] || 'not-started';
    },

    setCurrent(modIndex) {
      const state = defaultProgress();
      for (let i = 0; i < modIndex - 1; i++) state[i] = 'done';
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
      // mark currentMod as current in storage if not already
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
        dot.textContent = mod;
        containerEl.appendChild(dot);

        if (i < TOTAL_MODULES - 1) {
          const line = document.createElement('span');
          line.className = 'module-topbar__progress-line';
          if (status === 'done') line.classList.add('module-topbar__progress-line--done');
          containerEl.appendChild(line);
        }
      }
    },

    /* Renders the bigger 28px progressionsstege on översiktsvyn.
       containerEl has class "course-progress". */
    renderOverview(containerEl, currentMod) {
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
