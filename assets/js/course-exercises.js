// course-exercises.js
// Auto-saves any <form data-exercise="<key>"> textarea answer to localStorage.
//
// Markup expected:
//   <form data-exercise="modul-1-varfor" class="exercise__form">
//     <textarea class="exercise__textarea" name="answer" required></textarea>
//     <button type="submit" class="btn btn--primary">Spara</button>
//     <p class="exercise__feedback" aria-live="polite"></p>
//   </form>
//
// Behavior:
//   - On load: textarea pre-filled if a saved value exists in localStorage.
//   - On submit: persist value, show "Sparat ✓" in __feedback for 4s.
//   - storage key: `presentationsteknik-${lang}-exercise-${key}`
//                  (lang detected from <html lang> attribute)

(function (global) {
  function getLang() {
    return (document.documentElement.lang || 'sv').slice(0, 2);
  }

  function storageKeyFor(exerciseKey) {
    return `presentationsteknik-${getLang()}-exercise-${exerciseKey}`;
  }

  function init() {
    const forms = document.querySelectorAll('form[data-exercise]');
    forms.forEach((form) => {
      const key = form.dataset.exercise;
      const textarea = form.querySelector('textarea');
      const feedback = form.querySelector('.exercise__feedback');
      if (!textarea) return;

      // Load existing answer
      try {
        const saved = localStorage.getItem(storageKeyFor(key));
        if (saved) textarea.value = saved;
      } catch { /* localStorage disabled */ }

      form.addEventListener('submit', (e) => {
        e.preventDefault();
        try {
          localStorage.setItem(storageKeyFor(key), textarea.value);
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

  // Auto-init when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  global.CourseExercises = { init };
})(window);
