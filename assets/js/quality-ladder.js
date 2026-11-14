/*
  Quality Ladder — promptbyggaren på den dolda sidan för Skool-medlemmar.

  Bygger prompten medan läraren skriver. Sidan har inget JSON-block: all text
  som behövs finns här. Allt sker i webbläsaren: inget sparas och inget skickas
  någonstans. Användarens text sätts bara som .value och attribut, aldrig som HTML.

  Själva kopieringen sköts av copy-to-clipboard.js, som läser data-copy på
  knappen — därför hålls data-copy alltid lika med prompten.
*/
(function () {
  'use strict';

  var HINT_EMPTY = 'Fill in subject and the task to see your prompt.';

  /* Reglerna och svarsformatet. Texten är fastställd i specen (avsnitt B4,
     "The prompt builder") — ändra den bara tillsammans med specen. Rader med
     årskurs, kriterier eller språk byggs i buildPrompt, eftersom de beror på
     indata. */
  var RULES_BEFORE_MISTAKE = [
    'Rules for the samples:',
    '- Write as real Grade {grade} students would, in words they use. No names.',
    '- The three samples are about the same length. They differ in what they do against the criteria, not in how much they write.'
  ];
  // Den svagaste provtexten: med angiven vanlig miss pekar regeln på den, annars på en typisk miss.
  var WEAKEST_WITH_MISTAKE = 'the common mistake above';
  var WEAKEST_WITHOUT_MISTAKE = 'a mistake Grade {grade} students often make in this task';
  var WEAKEST_RULE = '- The weakest sample shows {mistake} and meets few of the criteria. The middle one meets some. The strongest meets all of them and is realistic for a strong Grade {grade} student, not an expert.';
  var RULE_FACTS = '- Apart from that mistake, every fact in the samples is correct.';

  var FORMAT_HEAD = 'Reply in plain text, no tables, with exactly these {count} parts:';
  var FORMAT_BEFORE_SECOND = [
    'CRITERIA: the criteria numbered, in words a Grade {grade} student understands.',
    'FOR STUDENTS: the three samples labelled Sample A, Sample B and Sample C, in mixed order so that A is not the weakest, with no levels or comments. This part is handed out as it is.',
    'TEACHER KEY: for each sample, its level (weakest, middle or strongest), one or two lines on what it does and does not do against the criteria, and ONE LEVEL UP: the one change that would lift it a level. For the strongest, say what would make it even better.'
  ];
  var FORMAT_SECOND = 'SECOND STRONG ANSWER: another strong answer that meets all the criteria in a clearly different way, so that students see there is more than one way to do it well.';
  var FORMAT_LAST = 'QUESTIONS: three questions for the class discussion after students have ranked the samples.';

  /* Byter ut {grade} i en textrad. */
  function withGrade(line, grade) {
    return line.split('{grade}').join(grade);
  }

  /* Delar kriterietexten på rader: trimmar och släpper tomma rader. */
  function parseCriteria(text) {
    return String(text || '').split('\n')
      .map(function (line) { return line.trim(); })
      .filter(function (line) { return line !== ''; });
  }

  /* Bygger prompten. Ren funktion: samma indata ger alltid samma text.
     input = { subject, grade, task, criteria[], mistake, length, second, language }.
     Ämne, uppgift, kriterier och miss ska vara trimmade av anroparen och
     sätts in precis som de är skrivna; språket trimmas här, och tomt eller
     "english" (oavsett versaler) räknas som engelska. */
  function buildPrompt(input) {
    var grade = String(input.grade);
    var language = (input.language || '').trim();
    var english = language === '' || language.toLowerCase() === 'english';
    var criteria = input.criteria || [];
    var lines = [
      'Do not include student names or student work in this conversation.',
      '',
      'You are helping a Grade ' + grade + ' ' + input.subject +
        ' teacher show students what quality looks like in one task. Write three made-up student answers to the task below, at three levels of quality, so that students can compare them with their own draft and see what would lift it one level. These are teaching samples. Do not grade, score or mark them.',
      '',
      'The task as students get it:',
      input.task,
      ''
    ];

    // Kriterieblocket: numrerade rader, eller en rad som ber AI:n skriva dem själv.
    if (criteria.length) {
      lines.push('Criteria for a strong answer:');
      criteria.forEach(function (c, i) { lines.push((i + 1) + '. ' + c); });
    } else {
      lines.push('Criteria: none given. First write three to five criteria for a strong answer to this task at Grade ' + grade + ', then use them.');
    }
    lines.push('');

    // Missraden finns bara när läraren har fyllt i en miss. Längdraden följer alltid.
    if (input.mistake) lines.push('A common mistake in this task: ' + input.mistake);
    lines.push('Length of a strong answer: ' + String(input.length).toLowerCase() + '.', '');

    var weakest = input.mistake ? WEAKEST_WITH_MISTAKE : WEAKEST_WITHOUT_MISTAKE;
    // {grade} byts bara i de fasta textraderna, aldrig i det läraren har skrivit.
    var fixed = RULES_BEFORE_MISTAKE.concat([WEAKEST_RULE.replace('{mistake}', weakest), RULE_FACTS]);
    var format = FORMAT_BEFORE_SECOND.concat(input.second ? [FORMAT_SECOND] : [], [FORMAT_LAST]);
    lines = lines.concat(
      fixed.map(function (line) { return withGrade(line, grade); }),
      [
        '',
        english
          ? 'Write everything in English.'
          : 'Write everything in ' + language + ', but keep the headings in English.',
        '',
        FORMAT_HEAD.replace('{count}', input.second ? 'five' : 'four')
      ],
      format.map(function (line) { return withGrade(line, grade); })
    );

    return lines.join('\n');
  }

  window.QualityLadder = { buildPrompt: buildPrompt, parseCriteria: parseCriteria };

  var els = {};

  function update() {
    var subject = els.subject.value.trim();
    var task = els.task.value.trim();
    if (!subject || !task) {
      els.prompt.value = '';
      els.copy.disabled = true;
      els.copy.setAttribute('data-copy', '');
      els.hint.textContent = HINT_EMPTY;
      return;
    }
    var text = buildPrompt({
      subject: subject, grade: els.grade.value, task: task,
      criteria: parseCriteria(els.criteria.value),
      mistake: els.mistake.value.trim(),
      length: els.length.value, second: els.second.checked,
      language: els.language.value
    });
    els.prompt.value = text;
    els.copy.disabled = false;
    els.copy.setAttribute('data-copy', text);
    els.hint.textContent = '';
  }

  document.addEventListener('DOMContentLoaded', function () {
    ['subject', 'grade', 'task', 'criteria', 'mistake', 'length', 'second', 'language', 'prompt', 'copy', 'hint'].forEach(function (id) {
      els[id] = document.getElementById('ql-' + id);
    });
    // Kryssrutan ger "change"; textfälten ger "input". Båda lyssnas på överallt.
    ['subject', 'grade', 'task', 'criteria', 'mistake', 'length', 'second', 'language'].forEach(function (id) {
      els[id].addEventListener('input', update);
      els[id].addEventListener('change', update);
    });
    update();
  });
})();
