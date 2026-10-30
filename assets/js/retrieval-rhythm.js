/*
  Retrieval Rhythm — promptbyggaren på /retrieval-rhythm/.

  Läser retrieval-rhythm/rhythm-en.json, fyller listan med format och bygger
  prompten medan läraren skriver. Allt sker i webbläsaren: inget sparas och
  inget skickas någonstans. Användarens text sätts bara som .value och
  attribut, aldrig som HTML.

  Själva kopieringen sköts av copy-to-clipboard.js, som läser data-copy på
  knappen — därför hålls data-copy alltid lika med prompten.
*/
(function () {
  'use strict';

  var DATA_URL = '/retrieval-rhythm/rhythm-en.json';
  var HINT_EMPTY = 'Fill in subject and paste your topic log to see your prompt.';
  var HINT_FAILED = "Couldn't load the formats — reload the page.";

  /* Bygger prompten. Ren funktion: samma indata ger alltid samma text.
     Texten är fastställd i planen — ändra den bara tillsammans med
     PDF:ens luckprompt (exports/build-retrieval-rhythm-pdf.py). */
  function buildPrompt(input) {
    var lines = [
      'Do not include student names or student results in this conversation.',
      '',
      'You are helping a Grade ' + input.grade + ' ' + input.subject +
        ' teacher plan retrieval practice starters for next week. Use only content from the topic log below. Do not add new content.',
      '',
      'Format: ' + input.format.name + '. ' + input.format.prompt_brief,
      'Number of lessons: ' + input.lessons
    ];
    if (input.date) lines.push('First lesson: ' + input.date);
    lines.push(
      'Questions per starter: ' + input.questions + ' (for starter quizzes and multiple choice)',
      '',
      'Topic log (date, topic, key points):',
      input.log,
      '',
      'In starter quizzes and multiple choice, mix content from different times in the log: about two fifths from the most recent lessons, two fifths from two to four weeks earlier, and one fifth from older entries. If the log is short, spread the questions across all of it. Mix the order so students cannot tell which week a question comes from. The other formats follow their own description.',
      '',
      'Reply in plain text, no tables. For each lesson write:',
      'LESSON: the lesson number, the format, and the log entries it draws on, with their dates',
      'STARTER: the starter exactly as students will see it',
      'KEY: the answer to every question',
      'Then once, at the very end:',
      'CHECK: every answer you are not fully sure of, one per line, so the teacher can verify it. Write "None" if there are none.'
    );
    return lines.join('\n');
  }

  window.RetrievalRhythm = { buildPrompt: buildPrompt };

  var els = {};
  // Utan prototyp: ?format=constructor ska inte hitta något.
  var formatsById = Object.create(null);

  function value(id) { return els[id].value.trim(); }

  function update() {
    var format = formatsById[els.format.value];
    var subject = value('subject');
    var log = value('log');
    if (!format || !subject || !log) {
      els.prompt.value = '';
      els.copy.disabled = true;
      els.copy.setAttribute('data-copy', '');
      els.hint.textContent = HINT_EMPTY;
      return;
    }
    var text = buildPrompt({
      format: format, subject: subject, grade: els.grade.value,
      lessons: els.lessons.value, questions: els.questions.value,
      date: value('date'), log: log
    });
    els.prompt.value = text;
    els.copy.disabled = false;
    els.copy.setAttribute('data-copy', text);
    els.hint.textContent = '';
  }

  function init(data) {
    data.formats.forEach(function (f) {
      formatsById[f.id] = f;
      var opt = document.createElement('option');
      opt.value = f.id;
      opt.textContent = f.name;
      els.format.appendChild(opt);
    });
    /* Mix, om inte en länk (?format=) har valt ett annat format. */
    var wanted = new URLSearchParams(window.location.search).get('format');
    els.format.value = formatsById[wanted] ? wanted : data.default_format;

    ['format', 'subject', 'grade', 'lessons', 'questions', 'date', 'log'].forEach(function (id) {
      els[id].addEventListener('input', update);
      els[id].addEventListener('change', update);
    });

    /* "Use this format" på korten väljer formatet och hoppar till byggaren
       utan att ladda om sidan. */
    document.addEventListener('click', function (e) {
      var link = e.target.closest('[data-use-format]');
      if (!link) return;
      e.preventDefault();
      var id = link.getAttribute('data-use-format');
      if (!formatsById[id]) return;
      els.format.value = id;
      update();
      document.getElementById('rr-builder').scrollIntoView({ behavior: 'smooth' });
      els.subject.focus({ preventScroll: true });
    });
    update();
  }

  document.addEventListener('DOMContentLoaded', function () {
    ['format', 'subject', 'grade', 'lessons', 'questions', 'date', 'log', 'prompt', 'copy', 'hint'].forEach(function (id) {
      els[id] = document.getElementById('rr-' + id);
    });
    fetch(DATA_URL)
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(init)
      .catch(function (err) {
        console.error('[retrieval-rhythm] could not load formats:', err);
        els.hint.textContent = HINT_FAILED;
        els.copy.disabled = true;
      });
  });
})();
