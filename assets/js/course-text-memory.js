// course-text-memory.js
// Övning: visa en kort text i N sekunder, sen får användaren skriva ner
// så många av orden hen minns som möjligt.
// +1 poäng för varje unikt ord som finns i texten.
// −1 poäng för varje unikt ord som inte finns i texten.
//
// Markup expected:
//   <div data-text-memory data-duration="8"
//        data-text="Pappan hade en inköpslista. På den stod det: …"></div>

(function () {
  function getLang() {
    return (document.documentElement.lang || 'sv').slice(0, 2);
  }

  const STRINGS = {
    sv: {
      intro: (d) => `Texten visas i ${d} sekunder. Försök komma ihåg så många av orden som möjligt — sen får du skriva ner det du minns.`,
      showText: 'Visa texten',
      askPrompt: 'Vilka ord minns du? Skriv dem fritt — separera med mellanslag, kommatecken eller radbrytning. Ord som inte fanns med ger minuspoäng.',
      placeholder: 'Skriv dina svar här',
      check: 'Kontrollera',
      verdictExcellent: 'Riktigt bra. Men lägg märke till hur mycket koncentration det krävde — i en presentation har publiken inte alls den fokusen.',
      verdictGood: 'Hyfsat — men minnet av en text är skört. I en presentation där publiken inte är förvarnad blir resultatet sällan så här bra.',
      verdictMid: 'Inte konstigt. Vi minns inte text som vi minns bilder. Det är just därför textmurar på slides sällan når fram.',
      verdictLow: 'Och det är poängen — text som visas kort tid är extremt svårt att minnas, även när du är förvarnad och fokuserad.',
      correctLabel: 'Rätta ord (+1 vardera)',
      wrongLabel: 'Fel ord (−1 vardera)',
      originalLabel: 'Originaltexten',
      restart: 'Gör om övningen',
    },
    en: {
      intro: (d) => `The text shows for ${d} seconds. Try to remember as many of the words as you can — then write down what you recall.`,
      showText: 'Show the text',
      askPrompt: 'Which words do you remember? Write them freely — separate with spaces, commas or line breaks. Words that weren\'t in the text count as minus points.',
      placeholder: 'Your answers here',
      check: 'Check',
      verdictExcellent: 'Really good. But notice how much concentration that required — in a presentation, the audience is nowhere near that focused.',
      verdictGood: "Decent — but text memory is fragile. In a presentation where the audience hasn't been warned, results are rarely this good.",
      verdictMid: "No surprise. We don't remember text the way we remember images. That's exactly why walls of text on slides rarely land.",
      verdictLow: "And that's the point — text shown briefly is extremely hard to remember, even when you're warned and focused.",
      correctLabel: 'Correct words (+1 each)',
      wrongLabel: 'Wrong words (−1 each)',
      originalLabel: 'Original text',
      restart: 'Try again',
    },
  };
  function t() { return STRINGS[getLang()] || STRINGS.sv; }

  // Tokenize a string into lowercase word tokens. Strips punctuation,
  // keeps Swedish letters (åäö).
  function tokens(s) {
    return (s.toLowerCase().match(/[a-zåäöéü]+/gi) || []).map((t) => t.toLowerCase());
  }

  function init(host) {
    const text = host.dataset.text || '';
    const duration = parseInt(host.dataset.duration || '8', 10);
    const valid = new Set(tokens(text));

    function renderIntro() {
      host.innerHTML = `
        <div class="text-memory__intro">
          <p class="text-memory__intro-text">${t().intro(duration)}</p>
          <button type="button" class="btn btn--primary text-memory__start">${t().showText}</button>
        </div>
      `;
      host.querySelector('.text-memory__start').addEventListener('click', show);
    }

    function show() {
      host.innerHTML = `
        <div class="text-memory__viewer" aria-live="polite">
          <div class="text-memory__progress" aria-hidden="true">
            <div class="text-memory__progress-bar"></div>
          </div>
          <div class="text-memory__text">${text}</div>
        </div>
      `;
      const bar = host.querySelector('.text-memory__progress-bar');
      requestAnimationFrame(() => {
        bar.style.transition = `width ${duration}s linear`;
        bar.style.width = '0%';
      });
      setTimeout(askInput, duration * 1000);
    }

    function askInput() {
      host.innerHTML = `
        <div class="text-memory__input">
          <p class="text-memory__prompt">${t().askPrompt}</p>
          <textarea class="text-memory__textarea"
                    placeholder="${t().placeholder}"
                    autocomplete="off"
                    spellcheck="false"></textarea>
          <button type="button" class="btn btn--primary text-memory__check">${t().check}</button>
        </div>
      `;
      const ta = host.querySelector('.text-memory__textarea');
      ta.focus();
      host.querySelector('.text-memory__check').addEventListener('click', () => grade(ta.value));
    }

    function grade(guess) {
      const guessed = [...new Set(tokens(guess))];
      const correct = [];
      const wrong = [];
      for (const t of guessed) {
        if (valid.has(t)) correct.push(t);
        else wrong.push(t);
      }
      const score = correct.length - wrong.length;
      const s = t();
      const verdict = score >= 9
        ? s.verdictExcellent
        : score >= 6
          ? s.verdictGood
          : score >= 3
            ? s.verdictMid
            : s.verdictLow;

      host.innerHTML = `
        <div class="text-memory__result">
          <div class="text-memory__score">${score}</div>
          <p class="text-memory__verdict">${verdict}</p>
          <dl class="text-memory__compare">
            <dt>${s.correctLabel}</dt>
            <dd>${correct.length ? correct.join(', ') : '—'}</dd>
            <dt>${s.wrongLabel}</dt>
            <dd>${wrong.length ? wrong.join(', ') : '—'}</dd>
            <dt>${s.originalLabel}</dt>
            <dd class="text-memory__original">${text}</dd>
          </dl>
          <button type="button" class="btn btn--primary text-memory__restart">${s.restart}</button>
        </div>
      `;
      host.querySelector('.text-memory__restart').addEventListener('click', renderIntro);
    }

    renderIntro();
  }

  function initAll() {
    document.querySelectorAll('[data-text-memory]').forEach(init);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }
})();
