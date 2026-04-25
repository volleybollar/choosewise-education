// course-exercises.js
// Auto-saves any <form data-exercise="<key>"> textarea answer to localStorage.
// Auto-saves any <form data-checklist="<key>"> checkbox state to localStorage.
//
// Markup expected (textarea reflektion):
//   <form data-exercise="modul-1-varfor" class="exercise__form">
//     <textarea class="exercise__textarea" name="answer" required></textarea>
//     <button type="submit" class="btn btn--primary">Spara</button>
//     <p class="exercise__feedback" aria-live="polite"></p>
//   </form>
//
// Markup expected (checklista):
//   <form data-checklist="modul-5-rum" class="exercise__form">
//     <label><input type="checkbox" name="check-1"> Etikett 1</label>
//     <label><input type="checkbox" name="check-2"> Etikett 2</label>
//     ...
//     <p class="exercise__feedback" aria-live="polite"></p>
//   </form>
//
// Behavior:
//   - On load: textarea pre-filled / checkboxes restored from localStorage.
//   - On textarea submit: persist value, show "Sparat ✓" for 4s.
//   - On checkbox change: auto-persist; show count of checked items in feedback.
//   - storage keys:
//     `presentationsteknik-${lang}-exercise-${key}` (textarea)
//     `presentationsteknik-${lang}-checklist-${key}` (checklist; JSON object)

(function (global) {
  function getLang() {
    return (document.documentElement.lang || 'sv').slice(0, 2);
  }

  function exerciseKeyFor(k) {
    return `presentationsteknik-${getLang()}-exercise-${k}`;
  }

  function checklistKeyFor(k) {
    return `presentationsteknik-${getLang()}-checklist-${k}`;
  }

  function initExercises() {
    const forms = document.querySelectorAll('form[data-exercise]');
    forms.forEach((form) => {
      const key = form.dataset.exercise;
      const textarea = form.querySelector('textarea');
      const feedback = form.querySelector('.exercise__feedback');
      if (!textarea) return;

      try {
        const saved = localStorage.getItem(exerciseKeyFor(key));
        if (saved) textarea.value = saved;
      } catch { }

      form.addEventListener('submit', (e) => {
        e.preventDefault();
        try {
          localStorage.setItem(exerciseKeyFor(key), textarea.value);
          if (feedback) {
            feedback.textContent = 'Sparat ✓';
            setTimeout(() => { feedback.textContent = ''; }, 4000);
          }
        } catch {
          if (feedback) feedback.textContent = 'Kunde inte spara (localStorage avstängd)';
        }
      });
    });
  }

  function initChecklists() {
    const forms = document.querySelectorAll('form[data-checklist]');
    forms.forEach((form) => {
      const key = form.dataset.checklist;
      const checkboxes = form.querySelectorAll('input[type="checkbox"]');
      const feedback = form.querySelector('.exercise__feedback');
      const storageKey = checklistKeyFor(key);

      // Restore from storage
      try {
        const saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
        checkboxes.forEach((cb) => { cb.checked = !!saved[cb.name]; });
      } catch { }

      function updateFeedback() {
        if (!feedback) return;
        const checked = [...checkboxes].filter(c => c.checked).length;
        feedback.textContent = `${checked} av ${checkboxes.length} avbockade`;
      }
      updateFeedback();

      checkboxes.forEach((cb) => {
        cb.addEventListener('change', () => {
          const state = {};
          checkboxes.forEach((c) => { state[c.name] = c.checked; });
          try { localStorage.setItem(storageKey, JSON.stringify(state)); } catch { }
          updateFeedback();
        });
      });
    });
  }

  function init() {
    initExercises();
    initChecklists();
  }

  // Auto-init when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  global.CourseExercises = { init };
})(window);
