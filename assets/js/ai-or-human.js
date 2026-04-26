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

  // ───── Rating widget + telemetry ─────

  function getTestKey(rootEl) {
    return rootEl.dataset.test; // "text" | "image" | "video"
  }

  function getLastScore(rootEl) {
    // Pull score from rendered feedback text (the test functions already updated it).
    // Match patterns like "X of Y" / "X av Y" or "Correct!"/"Rätt!" / "Wrong"/"Fel".
    const fb = rootEl.querySelector('[data-quiz-feedback]');
    if (!fb || fb.hidden) return { user: null, total: null };
    const text = fb.textContent || '';
    const m = text.match(/(\d+)\s*(?:of|av)\s*(\d+)/i);
    if (m) return { user: parseInt(m[1], 10), total: parseInt(m[2], 10) };
    if (/correct|rätt(?!\s*var)/i.test(text)) return { user: 1, total: 1 };
    if (/wrong|fel/i.test(text)) return { user: 0, total: 1 };
    return { user: null, total: null };
  }

  function postTelemetry(payload) {
    if (!TELEMETRY_URL) return;
    // Use text/plain body to avoid CORS preflight on Apps Script.
    fetch(TELEMETRY_URL, {
      method: 'POST',
      mode: 'no-cors',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(payload)
    }).catch(() => { /* fire-and-forget */ });
  }

  // No-op: kept for backwards compatibility with the test functions that
  // still call revealRating(rootEl) on submit. The rating UI is always
  // visible at the bottom of the page (see initRatingSummary) so this
  // call is a no-op now.
  function revealRating(_rootEl) { /* no-op */ }

  function initRatingSummary() {
    const rows = Array.from(document.querySelectorAll('[data-rating-for]'));
    const lang = (document.documentElement.lang || 'en').slice(0, 2);

    rows.forEach(row => {
      const key = row.dataset.ratingFor;
      const buttons = Array.from(row.querySelectorAll('[data-rating-btn]'));
      const thanksEl = row.querySelector('[data-rating-thanks]');

      // If already rated this session, restore the rated state.
      let storedRating = null;
      try { storedRating = sessionStorage.getItem('aiOrHuman.rated.' + key); } catch (_) {}
      if (storedRating) {
        buttons.forEach(b => {
          b.disabled = true;
          b.setAttribute('aria-pressed', b.dataset.ratingBtn === storedRating ? 'true' : 'false');
        });
        if (thanksEl) thanksEl.hidden = false;
        return;
      }

      buttons.forEach(btn => {
        btn.addEventListener('click', () => {
          const rating = parseInt(btn.dataset.ratingBtn, 10);
          buttons.forEach(b => {
            b.disabled = true;
            b.setAttribute('aria-pressed', b === btn ? 'true' : 'false');
          });
          if (thanksEl) thanksEl.hidden = false;
          try { sessionStorage.setItem('aiOrHuman.rated.' + key, String(rating)); } catch (_) {}

          // Pull the user's score for this test (if they completed it).
          const testSection = document.querySelector('[data-test="' + key + '"]');
          const score = testSection ? getLastScore(testSection) : { user: null, total: null };

          postTelemetry({
            ts: new Date().toISOString(),
            lang: lang,
            test: key,
            rating: rating,
            userScore: score.user,
            totalScore: score.total
          });
        });
      });
    });
  }

  // ───── Bootstrap ─────
  function bootstrap() {
    document.querySelectorAll('[data-test="text"]').forEach(initTextTest);
    document.querySelectorAll('[data-test="image"]').forEach(initImageTest);
    document.querySelectorAll('[data-test="video"]').forEach(initVideoTest);
    initRatingSummary();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootstrap);
  } else {
    bootstrap();
  }
})();
