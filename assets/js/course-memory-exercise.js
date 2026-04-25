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
      host.innerHTML = '<p style="color:#c00">Minnesövning kunde inte initieras (data-attribut saknas).</p>';
      return;
    }

    const total = images.length;
    let score = 0;
    let pairIndex = 0;

    function renderIntro() {
      const best = (() => { try { return localStorage.getItem(bestKey()); } catch { return null; } })();
      host.innerHTML = `
        <div class="memory__intro">
          <p class="memory__intro-text">Du kommer att få se ${total} bilder i följd. Varje bild visas i 2 sekunder. Försök att ta in dem — utan att stressa.</p>
          <p class="memory__intro-text">Direkt efter visningen får du se ${total} par av bilder. I varje par finns en bild du sett och en du inte sett. Klicka på den du tror du har sett.</p>
          ${best ? `<p class="memory__intro-best">Ditt bästa resultat hittills: <strong>${best}/${total}</strong></p>` : ''}
          <button type="button" class="btn btn--primary memory__start">Starta minnesövningen</button>
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
          <div class="memory__count">Bild <span class="memory__count-current">1</span> av ${total}</div>
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
          <p class="memory__interstitial-text">Du kommer om en liten stund att få se ${total} nya bilder.</p>
          <p class="memory__interstitial-text">Varje bild innehåller en bild som du sett tidigare och en som du inte sett tidigare.</p>
          <p class="memory__interstitial-text"><strong>Välj under bilderna den du känner igen.</strong></p>
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
          <div class="memory__count">Par ${num} av ${total}</div>
          <img class="memory__pair" src="${pairImg}" alt="Par ${num}: två bilder sida vid sida">
          <p class="memory__prompt">Vilken av bilderna har du sett tidigare?</p>
          <div class="memory__choices">
            <button type="button" class="btn btn--ghost memory__choice memory__choice--left" data-side="L">
              <span class="memory__arrow memory__arrow--left">«</span>
              <span class="memory__choice-label">Vänster bild</span>
            </button>
            <button type="button" class="btn btn--ghost memory__choice memory__choice--right" data-side="R">
              <span class="memory__choice-label">Höger bild</span>
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
        fb.textContent = 'Rätt!';
      } else {
        clicked.classList.add('memory__choice--wrong');
        const correctBtn = host.querySelector(`.memory__choice[data-side="${correct}"]`);
        if (correctBtn) correctBtn.classList.add('memory__choice--correct');
        fb.textContent = `Fel — den sedda bilden var ${correct === 'L' ? 'vänster' : 'höger'}.`;
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

      const verdict = score >= 9
        ? 'Imponerande — men tänk på att du gick in i övningen vakande, koncentrerad och förvarnad. Din publik gör inte det.'
        : score >= 6
          ? 'Bra — och ändå långt från perfekt. Lägg märke till att du var fokuserad och förvarnad. Din publik är det inte.'
          : score >= 3
            ? 'Det är just det som är poängen. Vi minns helheter, inte detaljer — och övningen är gjord för att avslöja det.'
            : 'Och du var ändå förvarnad och uppmärksam. Det säger något om hur lite åhörare faktiskt minns från en presentation.';

      host.innerHTML = `
        <div class="memory__result">
          <div class="memory__score">${score} / ${total}</div>
          <p class="memory__verdict">${verdict}</p>
          ${best != null ? `<p class="memory__best">Ditt bästa: <strong>${best}/${total}</strong></p>` : ''}
          <button type="button" class="btn btn--primary memory__restart">Gör om övningen</button>
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
