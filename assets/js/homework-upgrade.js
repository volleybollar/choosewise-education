/*
  Homework Upgrade — promptbyggaren på den dolda sidan för Skool-medlemmar.

  Läser de tolv mönstren ur JSON-blocket #hu-data (som scripts/build-homework-upgrade.py
  skriver in i sidan) och bygger prompten medan läraren skriver. Allt sker i
  webbläsaren: inget sparas och inget skickas någonstans. Användarens text
  sätts bara som .value och attribut, aldrig som HTML.

  Själva kopieringen sköts av copy-to-clipboard.js, som läser data-copy på
  knappen — därför hålls data-copy alltid lika med prompten.
*/
(function () {
  'use strict';

  var HINT_EMPTY = 'Fill in subject and the homework to see your prompt.';

  /* Raden för mönstret när läraren inte har valt något ("Let the AI choose"). */
  var PATTERN_ANY = 'Pattern: choose the one that fits this homework best, for example answering from memory before opening the book, writing down everything students remember after reading, self-test cards, a solved example followed by a similar problem, a mixed problem set, or explaining or drawing from memory.';

  /* Reglerna och svarsformatet. Texten är fastställd i specen (avsnittet
     "The prompt builder") — ändra den bara tillsammans med specen. Raderna
     med årskurs byggs i buildPrompt, eftersom de beror på indata. */
  var RULES_BEFORE_GRADE = [
    'Rules for the upgraded homework:',
    '- Unless the pattern says otherwise, students do the main part with the book and notes closed, then open them to check, correct and add what was missing in a different colour.',
    '- If students are likely to remember very little, give them headings or a few prompts to recall from.',
    '- It needs only paper, a pen and material students already have: no AI, no apps, nothing to print at home.',
    '- It practises the content of the original task, nothing new. It takes no longer than the original task and fits in the time above.',
    '- If you write new questions or problems, put their answers at the end of the homework, so students can check their own work.',
    '- It ends by telling students that the next lesson starts with three short questions on it, with books closed.'
  ];
  var FORMAT = [
    'Reply in plain text, no tables, with exactly these four parts:',
    'KEEP: one or two lines on what already works in the task and why, for example a clear purpose or a link to the lesson.',
    'UPGRADE: the new homework written to the student, ready to hand out: numbered steps, then any questions or problems in their own numbered list.',
    'AI RISK: one line on how easily a chatbot could do the original task, and one line on what a student would lose by letting a chatbot do the upgraded one and how the check below would show it. Do not call any version AI-proof.',
    'CHECK: three short questions for the start of the next lesson, on what the homework practised and in the same kind of task, answered on paper with books closed in about four minutes, numbered Q1:, Q2: and Q3:. At least one asks students to use the content, not only repeat it. Then the answers, numbered A1:, A2: and A3:. The check is not graded: students mark their own answers. End with one line on what to do if many students miss the same question.'
  ];

  /* Bygger prompten. Ren funktion: samma indata ger alltid samma text.
     input.pattern är null eller { name, brief }. Ämne, läxa och mål ska vara
     trimmade av anroparen och sätts in precis som de är skrivna; språket
     trimmas här, och tomt eller "english" (oavsett versaler) räknas som engelska. */
  function buildPrompt(input) {
    var language = (input.language || '').trim();
    var english = language === '' || language.toLowerCase() === 'english';
    var lines = [
      'Do not include student names or student work in this conversation.',
      '',
      'You are helping a Grade ' + input.grade + ' ' + input.subject +
        " teacher upgrade a homework task they have already set. Students do it at home on their own, and most of them can reach a chatbot. Keep the teacher's content and purpose. Change how students work, so that they practise from memory and the next lesson shows what each student can do alone.",
      '',
      'The homework as set:',
      input.homework,
      ''
    ];
    // Målraden finns bara när läraren har fyllt i ett mål.
    if (input.goal) lines.push('What students should be able to do afterwards: ' + input.goal);
    lines.push(
      'Time at home: about ' + input.minutes + ' minutes.',
      '',
      input.pattern ? 'Pattern: ' + input.pattern.name + '. ' + input.pattern.brief : PATTERN_ANY,
      ''
    );
    lines = lines.concat(RULES_BEFORE_GRADE, [
      '- Write it to the student, in plain words a Grade ' + input.grade + ' student can follow alone.',
      '',
      english
        ? 'Write everything in English.'
        : 'Write everything in ' + language + ', but keep the four headings in English.',
      ''
    ], FORMAT);
    return lines.join('\n');
  }

  window.HomeworkUpgrade = { buildPrompt: buildPrompt };

  var els = {};
  // Utan prototyp: ?pattern=constructor ska inte hitta något.
  var patternsById = Object.create(null);

  function update() {
    var subject = els.subject.value.trim();
    var homework = els.homework.value.trim();
    if (!subject || !homework) {
      els.prompt.value = '';
      els.copy.disabled = true;
      els.copy.setAttribute('data-copy', '');
      els.hint.textContent = HINT_EMPTY;
      return;
    }
    var text = buildPrompt({
      pattern: patternsById[els.pattern.value] || null,
      subject: subject, grade: els.grade.value,
      homework: homework, goal: els.goal.value.trim(),
      minutes: els.minutes.value, language: els.language.value
    });
    els.prompt.value = text;
    els.copy.disabled = false;
    els.copy.setAttribute('data-copy', text);
    els.hint.textContent = '';
  }

  document.addEventListener('DOMContentLoaded', function () {
    ['pattern', 'subject', 'grade', 'homework', 'goal', 'minutes', 'language', 'prompt', 'copy', 'hint'].forEach(function (id) {
      els[id] = document.getElementById('hu-' + id);
    });

    // Mönstren ligger i sidan, så inget behöver hämtas.
    JSON.parse(document.getElementById('hu-data').textContent).patterns.forEach(function (p) {
      patternsById[p.id] = p;
    });

    /* Förvalt mönster från länken (?pattern=). Ett okänt id lämnar
       "Let the AI choose". */
    var wanted = new URLSearchParams(window.location.search).get('pattern');
    if (wanted && patternsById[wanted]) els.pattern.value = wanted;

    ['pattern', 'subject', 'grade', 'homework', 'goal', 'minutes', 'language'].forEach(function (id) {
      els[id].addEventListener('input', update);
      els[id].addEventListener('change', update);
    });

    /* "Use this pattern" på korten väljer mönstret och hoppar till byggaren
       utan att ladda om sidan, så text som läraren redan skrivit finns kvar. */
    document.addEventListener('click', function (e) {
      var link = e.target.closest('[data-use-pattern]');
      if (!link) return;
      e.preventDefault();
      var id = link.getAttribute('data-use-pattern');
      if (!patternsById[id]) return;
      els.pattern.value = id;
      update();
      document.getElementById('hu-builder').scrollIntoView({ behavior: 'smooth' });
      els.subject.focus({ preventScroll: true });
    });
    update();
  });
})();
