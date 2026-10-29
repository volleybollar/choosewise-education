/*
  Lesson Lens — promptbyggaren på /lesson-lens/.

  Läser lesson-lens/lenses-en.json, fyller listorna med linser och bygger
  prompten medan läraren skriver. Allt sker i webbläsaren: inget sparas och
  inget skickas någonstans. Användarens text sätts bara som .value och
  attribut, aldrig som HTML.

  Själva kopieringen sköts av copy-to-clipboard.js, som läser data-copy på
  knappen — därför hålls data-copy alltid lika med prompten.
*/
(function () {
  'use strict';

  var DATA_URL = '/lesson-lens/lenses-en.json';
  var HINT_EMPTY = 'Fill in subject and your lesson to see your prompt.';
  var HINT_FAILED = "Couldn't load the lenses — reload the page.";

  /* Bygger prompten. Ren funktion: samma indata ger alltid samma text.
     input.lenses är en eller två linser, utan dubbletter.
     Texten är fastställd i planen (Task 4) — ändra den bara tillsammans
     med PDF:ens luckprompt (exports/build-lesson-lens-pdf.py). */
  function buildPrompt(input) {
    var first = input.lenses[0];
    var second = input.lenses[1];
    var lines = [
      'Do not include student names or student work in this conversation.',
      '',
      'You are helping a Grade ' + input.grade + ' ' + input.subject +
        ' teacher improve a lesson they have already planned. Keep their lesson and their way of teaching. Do not rewrite the lesson.',
      '',
      'Lens: ' + first.name + '. ' + first.one_liner,
      'How to apply it: ' + first.prompt_brief
    ];
    if (second) {
      lines.push(
        '',
        'Second lens: ' + second.name + '. ' + second.one_liner,
        'How to apply it: ' + second.prompt_brief
      );
    }
    lines.push('', 'The lesson as planned:', input.lesson);
    if (input.prior) lines.push('', 'Students already know: ' + input.prior);
    lines.push(
      '',
      'Reply in plain text, no tables, with exactly these four parts:',
      'KEEP: one or two lines on what already works in this lesson and why.',
      "UPGRADE: at most two changes in total, numbered. Each must use this lesson's own content and be small enough to make this evening.",
      'NUDGE: one question, only if the research behind the lens (or lenses) points to a clearly stronger option than what is planned. Otherwise write "None".',
      'CHECK: what the teacher should look for in class to see whether it worked.'
    );
    return lines.join('\n');
  }

  window.LessonLens = { buildPrompt: buildPrompt };

  var els = {};
  // Utan prototyp: ?lens=constructor ska inte hitta något.
  var lensesById = Object.create(null);

  function value(id) { return els[id].value.trim(); }

  function update() {
    var first = lensesById[els.lens.value];
    var second = lensesById[els.lens2.value];
    /* Samma lins två gånger räknas som en, och den andra listan nollställs
       så att läraren ser det. */
    if (second && second === first) {
      els.lens2.value = '';
      second = null;
    }
    var subject = value('subject');
    var lesson = value('lesson');
    if (!first || !subject || !lesson) {
      els.prompt.value = '';
      els.copy.disabled = true;
      els.copy.setAttribute('data-copy', '');
      els.hint.textContent = HINT_EMPTY;
      return;
    }
    var text = buildPrompt({
      lenses: second ? [first, second] : [first],
      subject: subject, grade: els.grade.value,
      lesson: lesson, prior: value('prior')
    });
    els.prompt.value = text;
    els.copy.disabled = false;
    els.copy.setAttribute('data-copy', text);
    els.hint.textContent = '';
  }

  function addOption(select, lens) {
    var opt = document.createElement('option');
    opt.value = lens.id;
    opt.textContent = lens.number + '. ' + lens.name;
    select.appendChild(opt);
  }

  function init(data) {
    data.lenses.forEach(function (l) {
      lensesById[l.id] = l;
      addOption(els.lens, l);
      addOption(els.lens2, l);
    });
    /* Startlinsen, om inte en länk (?lens=) har valt en annan. */
    var wanted = new URLSearchParams(window.location.search).get('lens');
    els.lens.value = lensesById[wanted] ? wanted : data.default_lens;

    ['lens', 'lens2', 'subject', 'grade', 'lesson', 'prior'].forEach(function (id) {
      els[id].addEventListener('input', update);
      els[id].addEventListener('change', update);
    });

    /* "Use this lens" på korten väljer linsen och hoppar till byggaren
       utan att ladda om sidan. */
    document.addEventListener('click', function (e) {
      var link = e.target.closest('[data-use-lens]');
      if (!link) return;
      e.preventDefault();
      var id = link.getAttribute('data-use-lens');
      if (!lensesById[id]) return;
      els.lens.value = id;
      update();
      document.getElementById('ll-builder').scrollIntoView({ behavior: 'smooth' });
      els.subject.focus({ preventScroll: true });
    });
    update();
  }

  document.addEventListener('DOMContentLoaded', function () {
    ['lens', 'lens2', 'subject', 'grade', 'lesson', 'prior', 'prompt', 'copy', 'hint'].forEach(function (id) {
      els[id] = document.getElementById('ll-' + id);
    });
    fetch(DATA_URL)
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(init)
      .catch(function (err) {
        console.error('[lesson-lens] could not load lenses:', err);
        els.hint.textContent = HINT_FAILED;
        els.copy.disabled = true;
      });
  });
})();
