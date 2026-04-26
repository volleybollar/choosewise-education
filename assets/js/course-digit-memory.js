// course-digit-memory.js
// Övning: visa 15 slumpmässiga siffror i 5 sek, sen får användaren skriva
// ner det hen kommer ihåg. Feedback = antal rätt i rad från början.
//
// Markup expected:
//   <div data-digit-memory data-count="15" data-duration="5"></div>
//
// Beteende:
//   - Knapp "Visa siffror" → siffrorna renderas i stort typsnitt med
//     en progress-bar som krymper ner i 5 sek
//   - När tiden är ute försvinner siffrorna och en textarea visas
//   - Användaren skriver in det hen minns och klickar "Kontrollera"
//   - Resultat: "Du fick X siffror rätt i rad från början" + visa facit
//   - Bästa resultat sparas i localStorage

(function () {
  function getLang() {
    return (document.documentElement.lang || 'sv').slice(0, 2);
  }

  const STRINGS = {
    sv: {
      intro: (n, d) => `Du kommer att få se ${n} slumpmässiga siffror i ${d} sekunder. Försök att lägga dem på minnet i den ordning de står — sen får du skriva ner det du kommer ihåg.`,
      bestSoFar: (b, total) => `Ditt bästa hittills: <strong>${b}/${total}</strong> rätt i rad från början`,
      showDigits: 'Visa siffrorna',
      askPrompt: 'Vilka siffror minns du? Skriv dem i den ordning du såg dem (mellanslag och bindestreck ignoreras).',
      placeholder: 'Skriv dina svar här',
      check: 'Kontrollera',
      verdictExcellent: 'Imponerande — och ändå tappar de flesta efter sju siffror i en presentation där publiken inte är förvarnad.',
      verdictGood: 'Du landar runt de 7 ± 2 siffror som korttidsminnet brukar klara. Det är inte mer än så.',
      verdictMid: 'Det är inte konstigt — siffror utan mening är svåra att hålla i minnet. Det är just därför slides med massor av siffror sällan fastnar.',
      verdictLow: 'Och det är poängen — siffror utan kontext är extremt svåra att minnas, även när du är förvarnad och fokuserad.',
      answerLabel: 'Facit',
      youWroteLabel: 'Du skrev',
      nothingWritten: '(inget skrivet)',
      bestNow: (b, total) => `Ditt bästa hittills: <strong>${b}/${total}</strong>`,
      restart: 'Gör om övningen',
    },
    en: {
      intro: (n, d) => `You'll see ${n} random digits for ${d} seconds. Try to commit them to memory in the order shown — then write down what you remember.`,
      bestSoFar: (b, total) => `Your best so far: <strong>${b}/${total}</strong> correct in a row from the start`,
      showDigits: 'Show the digits',
      askPrompt: 'Which digits do you remember? Write them in the order you saw them (spaces and dashes are ignored).',
      placeholder: 'Your answers here',
      check: 'Check',
      verdictExcellent: "Impressive — and yet most people lose track after seven digits in a presentation where the audience hasn't been warned.",
      verdictGood: "You land around the 7 ± 2 digits that short-term memory tends to handle. That's about it.",
      verdictMid: "No surprise — digits without meaning are hard to hold in memory. That's exactly why slides packed with numbers rarely stick.",
      verdictLow: "And that's the point — digits without context are extremely hard to remember, even when you're warned and focused.",
      answerLabel: 'Correct answer',
      youWroteLabel: 'You wrote',
      nothingWritten: '(nothing written)',
      bestNow: (b, total) => `Your best so far: <strong>${b}/${total}</strong>`,
      restart: 'Try again',
    },
  };
  function t() { return STRINGS[getLang()] || STRINGS.sv; }

  function bestKey() {
    return `presentationsteknik-${getLang()}-digit-memory-best`;
  }

  function generateDigits(count) {
    let s = '';
    for (let i = 0; i < count; i += 1) s += String(Math.floor(Math.random() * 10));
    return s;
  }

  function countLeadingMatches(actual, guess) {
    const a = actual.replace(/\D/g, '');
    const g = guess.replace(/\D/g, '');
    let n = 0;
    while (n < a.length && n < g.length && a[n] === g[n]) n += 1;
    return n;
  }

  function init(host) {
    const total = parseInt(host.dataset.count || '15', 10);
    const duration = parseInt(host.dataset.duration || '5', 10);
    let digits = '';

    function renderIntro() {
      const best = (() => { try { return localStorage.getItem(bestKey()); } catch { return null; } })();
      host.innerHTML = `
        <div class="digit-memory__intro">
          <p class="digit-memory__intro-text">${t().intro(total, duration)}</p>
          ${best ? `<p class="digit-memory__best">${t().bestSoFar(best, total)}</p>` : ''}
          <button type="button" class="btn btn--primary digit-memory__start">${t().showDigits}</button>
        </div>
      `;
      host.querySelector('.digit-memory__start').addEventListener('click', show);
    }

    function show() {
      digits = generateDigits(total);
      const spaced = digits.split('').join(' ');
      host.innerHTML = `
        <div class="digit-memory__viewer" aria-live="polite">
          <div class="digit-memory__progress" aria-hidden="true">
            <div class="digit-memory__progress-bar"></div>
          </div>
          <div class="digit-memory__digits">${spaced}</div>
        </div>
      `;
      const bar = host.querySelector('.digit-memory__progress-bar');
      // animate width: 100% → 0% over duration
      requestAnimationFrame(() => {
        bar.style.transition = `width ${duration}s linear`;
        bar.style.width = '0%';
      });
      setTimeout(askInput, duration * 1000);
    }

    function askInput() {
      host.innerHTML = `
        <div class="digit-memory__input">
          <p class="digit-memory__prompt">${t().askPrompt}</p>
          <textarea class="digit-memory__textarea"
                    placeholder="${t().placeholder}"
                    autocomplete="off"
                    spellcheck="false"></textarea>
          <button type="button" class="btn btn--primary digit-memory__check">${t().check}</button>
        </div>
      `;
      const ta = host.querySelector('.digit-memory__textarea');
      ta.focus();
      host.querySelector('.digit-memory__check').addEventListener('click', () => grade(ta.value));
    }

    function grade(guess) {
      const score = countLeadingMatches(digits, guess);
      let best = score;
      try {
        const prev = parseInt(localStorage.getItem(bestKey()) || '0', 10);
        if (score > prev) {
          localStorage.setItem(bestKey(), String(score));
        } else {
          best = prev;
        }
      } catch { /* ignore */ }

      const s = t();
      const verdict = score >= 12
        ? s.verdictExcellent
        : score >= 7
          ? s.verdictGood
          : score >= 3
            ? s.verdictMid
            : s.verdictLow;

      const facit = digits.split('').join(' ');
      const guessClean = guess.replace(/\D/g, '');
      const guessSpaced = guessClean ? guessClean.split('').join(' ') : s.nothingWritten;

      host.innerHTML = `
        <div class="digit-memory__result">
          <div class="digit-memory__score">${score} / ${total}</div>
          <p class="digit-memory__verdict">${verdict}</p>
          <dl class="digit-memory__compare">
            <dt>${s.answerLabel}</dt>
            <dd class="digit-memory__digits-small">${facit}</dd>
            <dt>${s.youWroteLabel}</dt>
            <dd class="digit-memory__digits-small">${guessSpaced}</dd>
          </dl>
          ${best > score ? `<p class="digit-memory__best">${s.bestNow(best, total)}</p>` : ''}
          <button type="button" class="btn btn--primary digit-memory__restart">${s.restart}</button>
        </div>
      `;
      host.querySelector('.digit-memory__restart').addEventListener('click', renderIntro);
    }

    renderIntro();
  }

  function initAll() {
    document.querySelectorAll('[data-digit-memory]').forEach(init);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }
})();
