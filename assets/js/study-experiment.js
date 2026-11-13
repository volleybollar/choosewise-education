/*
  Study Experiment — promptbyggaren på /study-experiment/.

  Läraren fyller i ämne, årskurs, område och språk, och prompten byggs medan
  man skriver. Prompten ber en AI skriva två texter och ett quiz med tolv
  frågor till experimentet. Allt sker i webbläsaren: inget sparas och inget
  skickas någonstans, och ingen datafil hämtas, eftersom prompten är fast
  text med fyra luckor. Användarens text sätts bara som .value och attribut,
  aldrig som HTML.

  Själva kopieringen sköts av copy-to-clipboard.js, som läser data-copy på
  knappen — därför hålls data-copy alltid lika med prompten.

  Filen har fyra delar: promptbyggaren, räknefunktionerna för resultatet,
  kopplingen till promptformuläret och resultatvyn. Resultatvyn räknar och ritar
  om allt vid varje tangenttryckning och sätter all text med textContent.
*/
(function () {
  'use strict';

  var HINT_EMPTY = 'Fill in subject and topic area to see your prompt.';
  /* Språket på texterna och quizet när fältet lämnas tomt. */
  var DEFAULT_LANGUAGE = 'English';

  /* ---------- Promptbyggaren ---------- */

  /* Lärarens prompt, rad för rad. Texten är fastställd ordagrant i specen
     (avsnittet Prompt builder). Ändra den bara tillsammans med PDF:ens
     luckprompt (exports/build-study-experiment-pdf.py) och testerna.
     Luckorna är årskurs (två gånger), ämne, område och språk. */
  function teacherLines(input, language) {
    return [
      'Do not include student names or student work in this conversation.',
      '',
      'You are helping a Grade ' + input.grade + ' ' + input.subject +
        ' teacher run a classroom experiment on two study methods. Students will study two short texts: one by reading it twice, the other by reading it once, writing down everything they remember and then checking it against the text. A week later they take a surprise quiz on both texts.',
      '',
      'Topic area: ' + input.topic,
      'Write everything in ' + language + '.',
      '',
      'Write two texts, TEXT A and TEXT B, each on a different part of this topic area that students have not been taught yet.',
      '- Make each text about 250 words, and keep the two texts within 20 words of each other in length.',
      '- Make them equally hard: ten key facts each, similar sentence length and similar words, at a reading level for Grade ' + input.grade + '.',
      '- Spread the key facts evenly through each text. No headings or lists inside the texts.',
      '- Use only facts that are well established and easy to check.',
      '',
      'Then write a quiz: Q1 to Q6 on Text A and Q7 to Q12 on Text B.',
      '- Each question tests a different key point of the text, the kind of thing a student would write down when recalling it. The answer is a word, a number or a short phrase from the text.',
      '- Ask about what this text says, so that a student who has not read it cannot answer from general knowledge. Do not ask what a word means.',
      '- Spread the questions over the whole text, and do not give away one answer in another question.',
      '',
      'Reply in plain text, no tables, with exactly these five parts:',
      'TEXT A: a short title, then the text.',
      'TEXT B: a short title, then the text.',
      'QUIZ: the twelve questions, numbered Q1: to Q12:, ready to print.',
      'ANSWERS: the answers, numbered Q1: to Q12: to match, with other answers that should also count as right.',
      'CHECK: every fact, figure, date or name in the texts that the teacher should verify, one per line.'
    ];
  }

  /* Bygger prompten. Ren funktion: samma indata ger alltid samma text.
     input = { subject, grade, topic, language }. Ett tomt språk blir engelska. */
  function buildPrompt(input) {
    var language = String(input.language || '').trim() || DEFAULT_LANGUAGE;
    return teacherLines(input, language).join('\n');
  }

  /* ---------- Räkna på resultatet ---------- */

  /* En rad per lapp: poängen för texten som lästes två gånger, sedan för texten
     man testade sig på. Mellan talen går ett mellanslag, tabb, komma, snedstreck
     eller semikolon. */
  var SCORE_LINE = /^\s*(\d+)\s*(?:[,/;]\s*|\s+)(\d+)\s*$/;

  /* Läser poängen. Ren funktion. Returnerar giltiga par [lästTvå, testad] och
     radnumren (från 1) på rader som inte är två heltal från 0 till max. Tomma
     rader hoppas över, men räknas med i radnumren. */
  function parseScores(text, max) {
    var pairs = [];
    var bad = [];
    String(text).split(/\r\n|\r|\n/).forEach(function (line, i) {
      if (!line.trim()) { return; }
      var m = SCORE_LINE.exec(line);
      var twice = m ? parseInt(m[1], 10) : -1;
      var tested = m ? parseInt(m[2], 10) : -1;
      if (twice < 0 || tested < 0 || twice > max || tested > max) {
        bad.push(i + 1);
      } else {
        pairs.push([twice, tested]);
      }
    });
    return { pairs: pairs, bad: bad };
  }

  /* Räknar ihop klassens resultat. Ren funktion. predicted = { twice, tested,
     same }: hur många som tippade vad. Medelvärdena är null när det inte finns
     några lappar, så att ingen kan dela med noll. Heltalssummorna följer med,
     eftersom visningen avrundar utifrån dem (se tenths). */
  function summarize(pairs, predicted) {
    var n = pairs.length;
    var sumTwice = 0;
    var sumTested = 0;
    var better = { twice: 0, tested: 0, same: 0 };
    pairs.forEach(function (pair) {
      sumTwice += pair[0];
      sumTested += pair[1];
      if (pair[0] > pair[1]) { better.twice += 1; }
      else if (pair[1] > pair[0]) { better.tested += 1; }
      else { better.same += 1; }
    });
    return {
      n: n,
      sumTwice: sumTwice,
      sumTested: sumTested,
      avgTwice: n ? sumTwice / n : null,
      avgTested: n ? sumTested / n : null,
      better: better,
      predicted: predicted,
      predictedTotal: predicted.twice + predicted.tested + predicted.same
    };
  }

  /* Medelvärdet i hela tiondelar, räknat på heltalssumman: 87 poäng på 20 lappar
     blir 44 (4,4). Math.round avrundar hälften uppåt, som en lärare gör, och
     ett exakt .5 kan flyttal visa exakt, så avrundningen blir inte fel. Både
     visningen och jämförelsen för "jämnt resultat" använder tiondelarna, så att
     "4,3 mot 4,3" aldrig ser ut som en skillnad. */
  function tenths(sum, n) {
    return Math.round(sum * 10 / n);
  }

  /* Det som andra delar av sidan (och testerna) kan använda. */
  window.StudyExperiment = {
    buildPrompt: buildPrompt,
    parseScores: parseScores,
    summarize: summarize
  };

  /* ---------- Formuläret med promptbyggaren ---------- */

  var els = {};

  function value(id) { return els[id].value.trim(); }

  /* Fyller i prompten och knappen. Saknas ämne eller område byggs ingen
     prompt: rutan töms, knappen blir grå och ledtråden visas bredvid den. */
  function update() {
    var subject = value('subject');
    var topic = value('topic');
    if (!subject || !topic) {
      els.prompt.value = '';
      els.copy.disabled = true;
      els.copy.setAttribute('data-copy', '');
      els.hint.textContent = HINT_EMPTY;
      return;
    }
    var text = buildPrompt({
      subject: subject, grade: els.grade.value, topic: topic, language: value('language')
    });
    els.prompt.value = text;
    els.copy.disabled = false;
    els.copy.setAttribute('data-copy', text);
    els.hint.textContent = '';
  }

  function initBuilder() {
    ['subject', 'grade', 'topic', 'language', 'prompt', 'copy', 'hint'].forEach(function (id) {
      els[id] = document.getElementById('se-' + id);
    });
    ['subject', 'grade', 'topic', 'language'].forEach(function (id) {
      els[id].addEventListener('input', update);
      els[id].addEventListener('change', update);
    });
    update();
  }

  /* ---------- Resultatvyn ---------- */

  var DEFAULT_MAX = 6;
  var MAX_LIMIT = 20;
  var MSG_NO_SLIPS = 'Type the scores from the slips to see your class\'s result.';
  /* Raderna i diagrammet, i samma ordning i båda grupperna. */
  var CHART_ROWS = [
    { key: 'twice', label: 'Read twice' },
    { key: 'tested', label: 'Tested myself' },
    { key: 'same', label: 'About the same' }
  ];

  /* Hela tal i fältet, annars ersättningsvärdet. */
  function wholeNumber(id, fallback) {
    var raw = value(id);
    return /^\d+$/.test(raw) ? parseInt(raw, 10) : fallback;
  }

  /* Antal frågor per text: 1 till 20, annars 6. */
  function readMax() {
    var n = wholeNumber('max', DEFAULT_MAX);
    return n >= 1 && n <= MAX_LIMIT ? n : DEFAULT_MAX;
  }

  /* Ett element med klass och text. Texten sätts alltid med textContent. */
  function make(tag, className, text) {
    var node = document.createElement(tag);
    if (className) { node.className = className; }
    if (text !== undefined) { node.textContent = text; }
    return node;
  }

  function percent(count, total) {
    return Math.round(count / total * 100);
  }

  /* En grupp med tre rader: etikett, stapel och "antal (andel %)". Antalet
     står utanför stapeln, så en rad på 0 % går ändå att läsa, och etiketten
     skiljer raderna åt utan hjälp av färg. */
  function chartGroup(title, caption, counts, total, barClass) {
    var group = make('div', 'se-chart__group');
    group.appendChild(make('h3', 'se-chart__title', title));
    /* En rad under rubriken som säger vad staplarna visar. */
    group.appendChild(make('p', 'se-chart__caption', caption));
    var list = make('ul', 'se-chart__rows');
    CHART_ROWS.forEach(function (row) {
      var count = counts[row.key];
      var share = percent(count, total);
      var item = make('li', 'se-chart__row');
      item.appendChild(make('span', 'se-chart__label', row.label));
      /* Stapeln är bara dekoration; siffrorna bär informationen. */
      var track = make('div', 'se-chart__track');
      track.setAttribute('aria-hidden', 'true');
      var bar = make('div', 'se-chart__bar ' + barClass);
      bar.style.width = share + '%';
      if (count > 0) { bar.style.minWidth = '2px'; }
      track.appendChild(bar);
      item.appendChild(track);
      item.appendChild(make('span', 'se-chart__count', count + ' (' + share + ' %)'));
      list.appendChild(item);
    });
    group.appendChild(list);
    return group;
  }

  /* Räknar om och ritar om hela resultatvyn utifrån fälten. */
  function renderResults() {
    var max = readMax();
    var parsed = parseScores(els.scores.value, max);
    var s = summarize(parsed.pairs, {
      twice: wholeNumber('pred-twice', 0),
      tested: wholeNumber('pred-tested', 0),
      same: wholeNumber('pred-same', 0)
    });

    /* Felen: en mening per rad som lämnas utanför. Området är aria-live, så
       texten sätts bara när den har ändrats: annars läses samma fel upp på
       nytt vid varje tangenttryckning. */
    var errors = parsed.bad.map(function (line) {
      return 'Line ' + line + ' is not two scores between 0 and ' + max + ', so it is left out.';
    }).join('\n');
    if (els.errors.textContent !== errors) { els.errors.textContent = errors; }

    var shownTwice = s.n ? tenths(s.sumTwice, s.n) : 0;
    var shownTested = s.n ? tenths(s.sumTested, s.n) : 0;

    els.summary.textContent = '';
    if (s.n === 0) {
      els.summary.appendChild(make('p', '', MSG_NO_SLIPS));
    } else {
      els.summary.appendChild(make('p', '', s.n + (s.n === 1 ? ' slip.' : ' slips.')));
      els.summary.appendChild(make('p', '',
        'Text read twice: ' + (shownTwice / 10).toFixed(1) + ' of ' + max + ' on average. ' +
        'Text tested: ' + (shownTested / 10).toFixed(1) + ' of ' + max + ' on average.'));
      els.summary.appendChild(make('p', '',
        s.better.tested + ' scored higher on the text they tested themselves on, ' +
        s.better.twice + ' on the text they read twice, and ' +
        s.better.same + ' the same.'));
      if (s.predictedTotal > 0) {
        els.summary.appendChild(make('p', '',
          'Before the quiz, ' + s.predicted.twice + ' of ' + s.predictedTotal +
          ' predicted the text they read twice would stick better.'));
      }
    }

    els.chart.textContent = '';
    if (s.predictedTotal > 0) {
      els.chart.appendChild(chartGroup('What you predicted', 'Which text students expected to remember better.',
        s.predicted, s.predictedTotal, 'se-chart__bar--predicted'));
    }
    if (s.n > 0) {
      els.chart.appendChild(chartGroup('What happened', 'Which text each student remembered better.',
        s.better, s.n, 'se-chart__bar--happened'));
    }

    /* Noten om ett jämnt eller omvänt resultat: när det visade medelvärdet för
       testningen inte är högre än det för omläsningen. */
    els.even.hidden = !(s.n > 0 && shownTested <= shownTwice);
  }

  function initResults() {
    ['max', 'pred-twice', 'pred-tested', 'pred-same', 'scores', 'errors', 'summary', 'chart', 'even', 'results'].forEach(function (id) {
      els[id] = document.getElementById('se-' + id);
    });
    els.results.addEventListener('input', renderResults);
    renderResults();
  }

  document.addEventListener('DOMContentLoaded', function () {
    initBuilder();
    initResults();
  });
})();
