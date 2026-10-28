/*
  Side by Side — promptbyggaren på /side-by-side/.

  Läser side-by-side/pairs-en.json, fyller listan med partyper och bygger
  prompten medan läraren skriver. Allt sker i webbläsaren: inget sparas och
  inget skickas någonstans. Användarens text sätts bara som .value och
  attribut, aldrig som HTML.

  Själva kopieringen sköts av copy-to-clipboard.js, som läser data-copy på
  knappen — därför hålls data-copy alltid lika med prompten.
*/
(function () {
  'use strict';

  var DATA_URL = '/side-by-side/pairs-en.json';
  var HINT_EMPTY = 'Fill in subject and topic to see your prompt.';
  var HINT_FAILED = "Couldn't load the pair types — reload the page.";
  var NOTE_EASIER_ONLY = 'This pair type is offered at "Easier to see" only: AI tools could not build it reliably at the harder level.';

  /* Bygger prompten. Ren funktion: samma indata ger alltid samma text.
     Ändra texten bara tillsammans med PDF:ens luckprompt
     (exports/build-side-by-side-pdf.py) — ett test vaktar att de är lika. */
  function buildPrompt(input) {
    var pair = input.pair;
    var level = input.level;
    var lines = [
      'Do not include student names or student work in this conversation.',
      '',
      'You are helping a Grade ' + input.grade + ' ' + input.subject +
        ' teacher prepare a fifteen-minute "Side by Side" task. Students compare two items placed next to each other: what is only in A, what is in both, and what is only in B. Then they write the rule they found and try it on a new case C. Students work on paper, without AI.',
      '',
      'Lesson topic: ' + input.topic
    ];
    if (input.prior) lines.push('Students already know: ' + input.prior);
    lines.push(
      '',
      'Pair type: ' + pair.name + '. ' + pair.one_liner,
      'How to build the pair: ' + pair.prompt_brief,
      'Difficulty: ' + level.name + '. ' + level.instruction,
      '',
      'Rules: A and B respond to the same task and are as alike as possible apart from the difference this pair type asks for. Each of A and B is at most 60 words or six short lines, so it fits half a page width. Case C can be decided with the rule. Case C is a new situation, not the same pair with new names. Do not invent studies, measurements or sources; a source written for the task must say so. Write for students in this grade.',
      '',
      'Reply in plain text, no tables, in two blocks. The first block is printed for students, so it must not contain anything from the second.',
      'FOR STUDENTS',
      'TASK: the question or task both A and B respond to',
      'A: a short label, then the first item',
      'B: a short label, then the second item',
      'CASE C: a new case the rule decides, without its answer',
      'THINK BACK: one short sentence starter with a single blank, about how they thought, not what they found',
      'TEACHER KEY',
      'ONLY A: what only A has or does',
      'BOTH: what A and B share',
      'ONLY B: what only B has or does',
      'THE RULE: the principle students should reach, in one or two sentences',
      'CASE C ANSWER: the answer, and how the rule decides it',
      'PROBE: one follow-up question that pushes past the first answer',
      'CHECK: only the facts, figures, dates or sources in TASK, A, B or CASE C that could be wrong, quoted or closely paraphrased, most doubtful first, one per line, at most six lines. Write "None" if there are none.'
    );
    return lines.join('\n');
  }

  window.SideBySide = { buildPrompt: buildPrompt };

  var els = {};
  var pairsById = {};
  var levelsById = {};

  function value(id) { return els[id].value.trim(); }

  function radio(levelId) {
    return els.form.querySelector('input[name="sb-level"][value="' + levelId + '"]');
  }

  /* En partyp med harder_ok: false erbjuder bara "Easier to see". Byter man
     till en sådan typ efter att ha valt "Harder" faller nivån tillbaka, och
     raden under valet säger varför. */
  function syncLevels(pair) {
    var harder = radio('harder');
    var easierOnly = pair && !pair.harder_ok;
    harder.disabled = !!easierOnly;
    if (easierOnly && harder.checked) radio('easier').checked = true;
    els.levelNote.textContent = easierOnly ? NOTE_EASIER_ONLY : '';
  }

  function update() {
    var pair = pairsById[els.pair.value];
    syncLevels(pair);
    var checked = els.form.querySelector('input[name="sb-level"]:checked');
    var level = levelsById[checked ? checked.value : 'easier'];
    var subject = value('subject');
    var topic = value('topic');
    if (!pair || !level || !subject || !topic) {
      els.prompt.value = '';
      els.copy.disabled = true;
      els.copy.setAttribute('data-copy', '');
      els.hint.textContent = HINT_EMPTY;
      return;
    }
    var text = buildPrompt({
      pair: pair, level: level, subject: subject, topic: topic,
      grade: els.grade.value, prior: value('prior')
    });
    els.prompt.value = text;
    els.copy.disabled = false;
    els.copy.setAttribute('data-copy', text);
    els.hint.textContent = '';
  }

  function selectPair(id) {
    if (!pairsById[id]) return;
    els.pair.value = id;
    update();
  }

  function init(data) {
    data.levels.forEach(function (lv) { levelsById[lv.id] = lv; });
    data.pairs.forEach(function (p) {
      pairsById[p.id] = p;
      var opt = document.createElement('option');
      opt.value = p.id;
      opt.textContent = p.number + '. ' + p.name;
      els.pair.appendChild(opt);
    });
    var wanted = new URLSearchParams(window.location.search).get('pair');
    if (wanted && pairsById[wanted]) els.pair.value = wanted;

    /* Alla fält och nivåknapparna bygger om prompten när de ändras. */
    els.form.addEventListener('input', update);
    els.form.addEventListener('change', update);

    /* "Use this pair" på korten väljer partypen och hoppar till byggaren
       utan att ladda om sidan. */
    document.addEventListener('click', function (e) {
      var link = e.target.closest('[data-use-pair]');
      if (!link) return;
      e.preventDefault();
      selectPair(link.getAttribute('data-use-pair'));
      document.getElementById('sb-builder').scrollIntoView({ behavior: 'smooth' });
      els.subject.focus({ preventScroll: true });
    });
    update();
  }

  document.addEventListener('DOMContentLoaded', function () {
    ['form', 'pair', 'subject', 'grade', 'topic', 'prior', 'prompt', 'copy', 'hint'].forEach(function (id) {
      els[id] = document.getElementById('sb-' + id);
    });
    els.levelNote = document.getElementById('sb-level-note');
    fetch(DATA_URL)
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(init)
      .catch(function (err) {
        console.error('[side-by-side] could not load pair types:', err);
        els.hint.textContent = HINT_FAILED;
        els.copy.disabled = true;
      });
  });
})();
