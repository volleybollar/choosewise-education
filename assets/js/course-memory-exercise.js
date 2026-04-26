// course-memory-exercise.js
// Tre-fas minnesövning: intro → 10 bilder à 2 sek → 10 par-test → resultat.
//
// Markup expected:
//   <div data-memory-exercise
//        data-images="/path/01.jpg,/path/02.jpg,...,/path/10.jpg"
//        data-pairs="/path/par-01.jpg,/path/par-02.jpg,...,/path/par-10.jpg"
//        data-answers="L,L,R,R,R,R,L,L,L,R">
//   </div>
//
// Beteendet:
//   - Bilder förladdas innan fas 1 startar (annars knycker timing).
//   - Fas 1: varje bild visas 2 s, ingen UI-kontroll.
//   - Fas 2: parslide visas, två knappar "Vänster" / "Höger".
//   - Resultat: poäng + pedagogisk text + "Gör om"-knapp.
//   - Bästa resultat sparas i localStorage (informativt; ingen gating).

(function () {
  function getLang() {
    return (document.documentElement.lang || 'sv').slice(0, 2);
  }

  const STRINGS = {
    sv: {
      initError: 'Minnesövning kunde inte initieras (data-attribut saknas).',
      intro1: (n) => `Du kommer att få se ${n} bilder i följd. Varje bild visas i 2 sekunder. Försök att ta in dem — utan att stressa.`,
      intro2: (n) => `En liten stund efter att du sett bilderna får du se ${n} bildpar. I varje par finns en bild du sett och en du inte sett. Markera den bild som du tror du har sett.`,
      bestSoFar: (b, total) => `Ditt bästa resultat hittills: <strong>${b}/${total}</strong>`,
      start: 'Starta minnesövningen',
      countLabel: (n, total) => `Bild <span class="memory__count-current">${n}</span> av ${total}`,
      interstitial1: (n) => `Du kommer om en liten stund att få se ${n} nya bilder.`,
      interstitial2: 'Varje bild innehåller en bild som du sett tidigare och en som du inte sett tidigare.',
      interstitial3: 'Välj under bilderna den du känner igen.',
      pairLabel: (num, total) => `Par ${num} av ${total}`,
      pairAlt: (num) => `Par ${num}: två bilder sida vid sida`,
      pairPrompt: 'Vilken av bilderna har du sett tidigare?',
      leftImg: 'Vänster bild',
      rightImg: 'Höger bild',
      correct: 'Rätt!',
      wrong: (side) => `Fel — den sedda bilden var ${side === 'L' ? 'vänster' : 'höger'}.`,
      verdictExcellent: 'Imponerande — men tänk på att du gick in i övningen vakande, koncentrerad och förvarnad. Din publik gör inte det.',
      verdictGood: 'Bra — och ändå långt från perfekt. Lägg märke till att du var fokuserad och förvarnad. Din publik är det inte.',
      verdictMid: 'Det är just det som är poängen. Vi minns helheter, inte detaljer — och övningen är gjord för att avslöja det.',
      verdictLow: 'Och du var ändå förvarnad och uppmärksam. Det säger något om hur lite åhörare faktiskt minns från en presentation.',
      best: (b, total) => `Ditt bästa: <strong>${b}/${total}</strong>`,
      restart: 'Gör om övningen',
    },
    en: {
      initError: "The memory exercise couldn't be initialised (missing data attributes).",
      intro1: (n) => `You'll see ${n} images in succession. Each image is shown for 2 seconds. Try to take them in — without rushing.`,
      intro2: (n) => `A short while after you've seen the images, you'll see ${n} image pairs. In each pair, one image is one you've already seen and one you haven't. Mark the one you think you've seen.`,
      bestSoFar: (b, total) => `Your best result so far: <strong>${b}/${total}</strong>`,
      start: 'Start the memory exercise',
      countLabel: (n, total) => `Image <span class="memory__count-current">${n}</span> of ${total}`,
      interstitial1: (n) => `In a moment you'll see ${n} new images.`,
      interstitial2: "Each image contains one you've seen before and one you haven't.",
      interstitial3: 'Pick the one you recognise from below.',
      pairLabel: (num, total) => `Pair ${num} of ${total}`,
      pairAlt: (num) => `Pair ${num}: two images side by side`,
      pairPrompt: "Which of these images have you seen before?",
      leftImg: 'Left image',
      rightImg: 'Right image',
      correct: 'Correct!',
      wrong: (side) => `Wrong — the image you saw was on the ${side === 'L' ? 'left' : 'right'}.`,
      verdictExcellent: "Impressive — but bear in mind you went into this exercise alert, focused and warned. Your audience doesn't.",
      verdictGood: "Good — and yet far from perfect. Notice that you were focused and warned. Your audience isn't.",
      verdictMid: "That's exactly the point. We remember the whole, not the details — and the exercise is built to reveal that.",
      verdictLow: 'And you were still warned and attentive. That says something about how little an audience actually remembers from a presentation.',
      best: (b, total) => `Your best: <strong>${b}/${total}</strong>`,
      restart: 'Try again',
    },
  };
  function t() { return STRINGS[getLang()] || STRINGS.sv; }

  function bestKey() {
    return `presentationsteknik-${getLang()}-memory-best`;
  }

  function preload(urls) {
    return Promise.all(urls.map((u) => new Promise((res) => {
      const img = new Image();
      img.onload = img.onerror = () => res();
      img.src = u;
    })));
  }

  function init(host) {
    const images = (host.dataset.images || '').split(',').map((s) => s.trim()).filter(Boolean);
    const pairs = (host.dataset.pairs || '').split(',').map((s) => s.trim()).filter(Boolean);
    const answers = (host.dataset.answers || '').split(',').map((s) => s.trim().toUpperCase());
    if (images.length === 0 || pairs.length !== images.length || answers.length !== pairs.length) {
      host.innerHTML = `<p style="color:#c00">${t().initError}</p>`;
      return;
    }

    const total = images.length;
    let score = 0;
    let pairIndex = 0;

    function renderIntro() {
      const best = (() => { try { return localStorage.getItem(bestKey()); } catch { return null; } })();
      host.innerHTML = `
        <div class="memory__intro">
          <p class="memory__intro-text">${t().intro1(total)}</p>
          <p class="memory__intro-text">${t().intro2(total)}</p>
          ${best ? `<p class="memory__intro-best">${t().bestSoFar(best, total)}</p>` : ''}
          <button type="button" class="btn btn--primary memory__start">${t().start}</button>
        </div>
      `;
      host.querySelector('.memory__start').addEventListener('click', startViewing);
    }

    async function startViewing() {
      host.innerHTML = `
        <div class="memory__viewer" aria-live="polite">
          <div class="memory__progress" aria-hidden="true">
            <div class="memory__progress-bar"></div>
          </div>
          <div class="memory__count">${t().countLabel(1, total)}</div>
          <div class="memory__stage">
            <img class="memory__img" alt="">
          </div>
        </div>
      `;
      const imgEl = host.querySelector('.memory__img');
      const bar = host.querySelector('.memory__progress-bar');
      const counter = host.querySelector('.memory__count-current');

      await preload(images.concat(pairs));

      let i = 0;
      function show() {
        if (i >= total) {
          showInterstitial();
          return;
        }
        imgEl.src = images[i];
        counter.textContent = String(i + 1);
        bar.style.width = `${((i + 1) / total) * 100}%`;
        i += 1;
        setTimeout(show, 2000);
      }
      show();
    }

    function showInterstitial() {
      const seconds = 20;
      host.innerHTML = `
        <div class="memory__interstitial">
          <p class="memory__interstitial-text">${t().interstitial1(total)}</p>
          <p class="memory__interstitial-text">${t().interstitial2}</p>
          <p class="memory__interstitial-text"><strong>${t().interstitial3}</strong></p>
          <div class="memory__interstitial-countdown" aria-live="polite">${seconds}</div>
        </div>
      `;
      const countdownEl = host.querySelector('.memory__interstitial-countdown');
      let remaining = seconds;
      const tick = setInterval(() => {
        remaining -= 1;
        if (remaining <= 0) {
          clearInterval(tick);
          startTesting();
        } else {
          countdownEl.textContent = String(remaining);
        }
      }, 1000);
    }

    function startTesting() {
      pairIndex = 0;
      score = 0;
      renderPair();
    }

    function renderPair() {
      const pairImg = pairs[pairIndex];
      const num = pairIndex + 1;
      host.innerHTML = `
        <div class="memory__test">
          <div class="memory__count">${t().pairLabel(num, total)}</div>
          <img class="memory__pair" src="${pairImg}" alt="${t().pairAlt(num)}">
          <p class="memory__prompt">${t().pairPrompt}</p>
          <div class="memory__choices">
            <button type="button" class="btn btn--ghost memory__choice memory__choice--left" data-side="L">
              <span class="memory__arrow memory__arrow--left">«</span>
              <span class="memory__choice-label">${t().leftImg}</span>
            </button>
            <button type="button" class="btn btn--ghost memory__choice memory__choice--right" data-side="R">
              <span class="memory__choice-label">${t().rightImg}</span>
              <span class="memory__arrow memory__arrow--right">»</span>
            </button>
          </div>
          <p class="memory__feedback" aria-live="polite"></p>
        </div>
      `;
      host.querySelectorAll('.memory__choice').forEach((btn) => {
        btn.addEventListener('click', () => answerPair(btn.dataset.side, btn));
      });
    }

    function answerPair(side, clicked) {
      const correct = answers[pairIndex];
      const fb = host.querySelector('.memory__feedback');
      host.querySelectorAll('.memory__choice').forEach((b) => { b.disabled = true; });
      if (side === correct) {
        score += 1;
        clicked.classList.add('memory__choice--correct');
        fb.textContent = t().correct;
      } else {
        clicked.classList.add('memory__choice--wrong');
        const correctBtn = host.querySelector(`.memory__choice[data-side="${correct}"]`);
        if (correctBtn) correctBtn.classList.add('memory__choice--correct');
        fb.textContent = t().wrong(correct);
      }
      setTimeout(() => {
        pairIndex += 1;
        if (pairIndex >= total) {
          renderResult();
        } else {
          renderPair();
        }
      }, 1200);
    }

    function renderResult() {
      let best = null;
      try {
        const prev = parseInt(localStorage.getItem(bestKey()) || '0', 10);
        if (score > prev) {
          localStorage.setItem(bestKey(), String(score));
          best = score;
        } else {
          best = prev;
        }
      } catch { /* ignore */ }

      const s = t();
      const verdict = score >= 9
        ? s.verdictExcellent
        : score >= 6
          ? s.verdictGood
          : score >= 3
            ? s.verdictMid
            : s.verdictLow;

      host.innerHTML = `
        <div class="memory__result">
          <div class="memory__score">${score} / ${total}</div>
          <p class="memory__verdict">${verdict}</p>
          ${best != null ? `<p class="memory__best">${s.best(best, total)}</p>` : ''}
          <button type="button" class="btn btn--primary memory__restart">${s.restart}</button>
        </div>
      `;
      host.querySelector('.memory__restart').addEventListener('click', renderIntro);
    }

    renderIntro();
  }

  function initAll() {
    document.querySelectorAll('[data-memory-exercise]').forEach(init);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }
})();
