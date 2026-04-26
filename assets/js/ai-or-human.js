// ai-or-human.js
// Drives the three tests on /ai-or-human/ and /sv/ai-eller-manniska/.
//
// Tests are independent and discovered via [data-test="text|image|video"]
// containers. Each test reads its facit from data-attributes on the container
// or its cards. JS strings are taken from data-attributes so all user-facing
// copy stays in the per-language HTML.
//
// Telemetry: optional 1–6 difficulty rating per test. POSTs to a Google
// Apps Script Web App URL set in TELEMETRY_URL. Empty URL = no network call.

(function () {
  'use strict';

  // ───── Telemetry endpoint ─────
  // Set this to the Apps Script deployment URL once Johan creates the Sheet.
  // Empty string = telemetry disabled (UI still shows "Tack!" confirmation).
  const TELEMETRY_URL = '';

  // ───── Utilities ─────

  function shuffleInPlace(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  function flipCard(cardEl, toState) {
    if (toState === 'flipped') cardEl.classList.add('is-flipped');
    else if (toState === 'front') cardEl.classList.remove('is-flipped');
    else cardEl.classList.toggle('is-flipped');
  }

  // ───── Test 1: Texts ─────

  function initTextTest(rootEl) {
    const pairs = Array.from(rootEl.querySelectorAll('[data-quiz-pair]'));
    if (!pairs.length) return;

    const submitBtn = rootEl.querySelector('[data-quiz-submit]');
    const resetBtn = rootEl.querySelector('[data-quiz-reset]');
    const feedback = rootEl.querySelector('[data-quiz-feedback]');
    const tmpl = rootEl.dataset.feedbackTemplate || 'Score: {score}/2';

    let phase = 'select'; // 'select' | 'revealed'

    function getAllCards() {
      return Array.from(rootEl.querySelectorAll('.flipcard'));
    }

    function getChoiceCheckboxes() {
      return Array.from(rootEl.querySelectorAll('[data-quiz-choice]'));
    }

    // Shuffle within each topic-pair grid; then label cards "Text 1..4" in DOM order.
    function shuffleAndLabel() {
      pairs.forEach(pair => {
        const grid = pair.querySelector('[data-quiz-cards]');
        const cards = Array.from(grid.querySelectorAll('.flipcard'));
        shuffleInPlace(cards);
        grid.innerHTML = '';
        cards.forEach(c => grid.appendChild(c));
      });
      // Number labels left-to-right, top-to-bottom across both pair grids.
      const labels = Array.from(rootEl.querySelectorAll('[data-quiz-label]'));
      labels.forEach((el, i) => { el.textContent = 'Text ' + (i + 1); });
    }

    function getCheckedCount() {
      return getChoiceCheckboxes().filter(cb => cb.checked).length;
    }

    function syncSubmitState() {
      submitBtn.disabled = getCheckedCount() !== 2;
    }

    // Cap selection at 2: if user checks a 3rd, deselect oldest.
    let selectionOrder = [];
    function onChoiceChange(e) {
      if (phase !== 'select') return;
      const cb = e.target;
      if (!cb.matches('[data-quiz-choice]')) return;
      if (cb.checked) {
        selectionOrder.push(cb);
        if (selectionOrder.length > 2) {
          const oldest = selectionOrder.shift();
          oldest.checked = false;
        }
      } else {
        selectionOrder = selectionOrder.filter(x => x !== cb);
      }
      syncSubmitState();
    }

    function onCardClick(e) {
      if (phase !== 'revealed') return;
      // Don't intercept clicks on the checkbox or its label.
      if (e.target.closest('.flipcard__choice')) return;
      const card = e.target.closest('.flipcard');
      if (card) flipCard(card);
    }

    function onSubmit() {
      if (getCheckedCount() !== 2) return;
      // Score: count correct guesses. A "correct" guess is a checkbox checked
      // on a card whose data-truth === "ai".
      let score = 0;
      getChoiceCheckboxes().forEach(cb => {
        const card = cb.closest('.flipcard');
        const isAI = card.dataset.truth === 'ai';
        if (cb.checked && isAI) score += 1;
      });
      // Lock checkboxes, enable flipping.
      getChoiceCheckboxes().forEach(cb => { cb.disabled = true; });
      phase = 'revealed';
      feedback.textContent = tmpl.replace('{score}', String(score));
      feedback.hidden = false;
      submitBtn.disabled = true;
      // Reveal the rating widget for this test.
      revealRating(rootEl);
    }

    function onReset() {
      selectionOrder = [];
      shuffleAndLabel();
      getChoiceCheckboxes().forEach(cb => {
        cb.checked = false;
        cb.disabled = false;
      });
      getAllCards().forEach(c => flipCard(c, 'front'));
      feedback.hidden = true;
      feedback.textContent = '';
      phase = 'select';
      syncSubmitState();
    }

    // Wire up.
    shuffleAndLabel();
    pairs.forEach(pair => {
      pair.addEventListener('change', onChoiceChange);
      pair.addEventListener('click', onCardClick);
    });
    submitBtn.addEventListener('click', onSubmit);
    resetBtn.addEventListener('click', onReset);
    syncSubmitState();
  }

  // ───── Test 2: Images ─────

  function initImageTest(rootEl) {
    const checks = Array.from(rootEl.querySelectorAll('[data-quiz-checkboxes] input[type="checkbox"]'));
    const submitBtn = rootEl.querySelector('[data-quiz-submit]');
    const resetBtn = rootEl.querySelector('[data-quiz-reset]');
    const feedback = rootEl.querySelector('[data-quiz-feedback]');
    const hints = Array.from(rootEl.querySelectorAll('[data-quiz-hint]'));
    const tmpl = rootEl.dataset.feedbackTemplate || 'Score: {score}/9';

    // Truth set: numbers (as strings) that are NOT AI.
    const notAI = new Set(
      (rootEl.dataset.correctNotAi || '').split(',').map(s => s.trim()).filter(Boolean)
    );

    function onSubmit() {
      let score = 0;
      checks.forEach(cb => {
        const isNotAI = notAI.has(cb.value);
        const userSaysAI = cb.checked;
        // Correct if (userSaysAI && !isNotAI) or (!userSaysAI && isNotAI).
        if (userSaysAI !== isNotAI) score += 1;
      });
      feedback.textContent = tmpl.replace('{score}', String(score));
      feedback.hidden = false;
      revealRating(rootEl);
    }

    function onReset() {
      checks.forEach(cb => { cb.checked = false; });
      feedback.hidden = true;
      feedback.textContent = '';
      hints.forEach(h => { h.open = false; });
    }

    submitBtn.addEventListener('click', onSubmit);
    resetBtn.addEventListener('click', onReset);
  }

  // ───── Test 3: Videos ─────

  function initVideoTest(rootEl) {
    const radios = Array.from(rootEl.querySelectorAll('[data-quiz-radios] input[type="radio"]'));
    const submitBtn = rootEl.querySelector('[data-quiz-submit]');
    const resetBtn = rootEl.querySelector('[data-quiz-reset]');
    const feedback = rootEl.querySelector('[data-quiz-feedback]');
    const correct = parseInt(rootEl.dataset.correctVideo || '0', 10);
    const tmplCorrect = rootEl.dataset.feedbackCorrect || 'Correct!';
    const tmplWrong = rootEl.dataset.feedbackWrong || 'Wrong — it was video {correct}.';

    // Wire video src from data-src.
    rootEl.querySelectorAll('video[data-src]').forEach(v => {
      if (v.dataset.src) v.src = v.dataset.src;
    });

    function onRadioChange() {
      submitBtn.disabled = !radios.some(r => r.checked);
    }

    function onSubmit() {
      const picked = radios.find(r => r.checked);
      if (!picked) return;
      if (parseInt(picked.value, 10) === correct) {
        feedback.textContent = tmplCorrect;
      } else {
        feedback.textContent = tmplWrong.replace('{correct}', String(correct));
      }
      feedback.hidden = false;
      revealRating(rootEl);
    }

    function onReset() {
      radios.forEach(r => { r.checked = false; });
      feedback.hidden = true;
      feedback.textContent = '';
      submitBtn.disabled = true;
    }

    radios.forEach(r => r.addEventListener('change', onRadioChange));
    submitBtn.addEventListener('click', onSubmit);
    resetBtn.addEventListener('click', onReset);
  }

  // ───── Rating placeholder (filled in Phase F) ─────
  function revealRating(_rootEl) {
    // Filled in Phase F. No-op for now.
  }

  // ───── Bootstrap ─────
  function bootstrap() {
    document.querySelectorAll('[data-test="text"]').forEach(initTextTest);
    document.querySelectorAll('[data-test="image"]').forEach(initImageTest);
    document.querySelectorAll('[data-test="video"]').forEach(initVideoTest);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootstrap);
  } else {
    bootstrap();
  }
})();
