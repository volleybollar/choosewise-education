/*
  Flawed Answer — promptbyggaren på /flawed-answer/.

  Läser flawed-answer/flaws-en.json, fyller listan med feltyper och bygger
  prompten medan läraren skriver. Allt sker i webbläsaren: inget sparas och
  inget skickas någonstans. Användarens text sätts bara som .value och
  attribut, aldrig som HTML.

  Själva kopieringen sköts av copy-to-clipboard.js, som läser data-copy på
  knappen — därför hålls data-copy alltid lika med prompten.
*/
(function () {
  'use strict';

  var DATA_URL = '/flawed-answer/flaws-en.json';
  var HINT_EMPTY = 'Choose a flaw type and fill in subject and topic to see your prompt.';
  var HINT_FAILED = "Couldn't load the flaw types — reload the page.";
  var NOTE_EASIER_ONLY = 'This flaw type is offered at "Easier to spot" only: AI tools could not plant it reliably at the harder level.';

  /* Bygger prompten. Ren funktion: samma indata ger alltid samma text.
     Texten är fastställd i planen (Task 5) — ändra den bara tillsammans
     med PDF:ens luckprompt (exports/build-flawed-answer-pdf.py). */
  function buildPrompt(input) {
    var flaw = input.flaw;
    var level = input.level;
    var lines = [
      'Do not include student names or student work in this conversation.',
      '',
      'You are helping a Grade ' + input.grade + ' ' + input.subject +
        ' teacher prepare a fifteen-minute "Flawed Answer" task. Students will be told that an AI wrote the answer, and their job is to find the error in its reasoning.',
      '',
      'Lesson topic: ' + input.topic
    ];
    if (input.prior) lines.push('Students already know: ' + input.prior);
    lines.push(
      '',
      'Flaw type: ' + flaw.name + '. ' + flaw.one_liner,
      'How to plant it: ' + flaw.prompt_brief,
      'Difficulty: ' + level.name + '. ' + level.instruction,
      '',
      'Rules: the answer contains exactly one error. It is an error of reasoning of the type above, not a factual slip or a typo. The flawed sentence makes one claim only. Every other sentence is correct in general, not just in typical cases, and no other sentence states or hints at the correct reasoning. Use "always", "never" or "all" only if the flaw type is Overgeneralisation. Do not invent studies, measurements or sources. Write in a confident, fluent style, as an AI assistant would.',
      '',
      'Reply in plain text, no tables, with exactly these nine parts:',
      'QUESTION: the question the answer responds to, in one sentence, without hinting at the flaw',
      'ANSWER: start with the line "AI-generated answer", then the answer',
      'THE FLAW: quote the flawed sentence exactly, then say what is wrong in at most two sentences',
      'FIX: the corrected sentence or step',
      'WHY IT CONVINCES: the true-sounding idea or common misconception that makes the flaw believable',
      'TEST IT: one way students could check this in class or at home',
      'PROBE: one follow-up question that pushes past the first answer',
      'THINK BACK: one sentence starter about how they thought, not what they found',
      'CHECK: every fact, figure, date, general rule or source in ANSWER or THE FLAW that the teacher should verify, quoted or closely paraphrased as it appears there, one per line, starting with the claims you are least sure of. Do not add claims from FIX or TEST IT. Write "None" only if ANSWER contains no checkable claim.'
    );
    return lines.join('\n');
  }

  window.FlawedAnswer = { buildPrompt: buildPrompt };

  var els = {};
  var flawsById = {};
  var levelsById = {};

  function value(id) { return els[id].value.trim(); }

  function radio(levelId) {
    return els.form.querySelector('input[name="fa-level"][value="' + levelId + '"]');
  }

  /* Decision A: en feltyp med harder_ok: false erbjuder bara "Easier to spot".
     Byter man till en sådan typ efter att ha valt "Harder" faller nivån
     tillbaka, och raden under valet säger varför. */
  function syncLevels(flaw) {
    var harder = radio('harder');
    var easierOnly = flaw && !flaw.harder_ok;
    harder.disabled = !!easierOnly;
    if (easierOnly && harder.checked) radio('easier').checked = true;
    els.levelNote.textContent = easierOnly ? NOTE_EASIER_ONLY : '';
  }

  function update() {
    var flaw = flawsById[els.flaw.value];
    syncLevels(flaw);
    var checked = els.form.querySelector('input[name="fa-level"]:checked');
    var level = levelsById[checked ? checked.value : 'easier'];
    var subject = value('subject');
    var topic = value('topic');
    if (!flaw || !level || !subject || !topic) {
      els.prompt.value = '';
      els.copy.disabled = true;
      els.copy.setAttribute('data-copy', '');
      els.hint.textContent = HINT_EMPTY;
      return;
    }
    var text = buildPrompt({
      flaw: flaw, level: level, subject: subject, topic: topic,
      grade: els.grade.value, prior: value('prior')
    });
    els.prompt.value = text;
    els.copy.disabled = false;
    els.copy.setAttribute('data-copy', text);
    els.hint.textContent = '';
  }

  function selectFlaw(id) {
    if (!flawsById[id]) return;
    els.flaw.value = id;
    update();
  }

  function init(data) {
    data.levels.forEach(function (lv) { levelsById[lv.id] = lv; });
    data.flaws.forEach(function (f) {
      flawsById[f.id] = f;
      var opt = document.createElement('option');
      opt.value = f.id;
      opt.textContent = f.number + '. ' + f.name;
      els.flaw.appendChild(opt);
    });
    var wanted = new URLSearchParams(window.location.search).get('flaw');
    if (wanted && flawsById[wanted]) els.flaw.value = wanted;

    /* Alla fält och nivåknapparna bygger om prompten när de ändras. */
    els.form.addEventListener('input', update);
    els.form.addEventListener('change', update);

    /* "Use this flaw" på korten väljer feltypen och hoppar till byggaren
       utan att ladda om sidan. */
    document.addEventListener('click', function (e) {
      var link = e.target.closest('[data-use-flaw]');
      if (!link) return;
      e.preventDefault();
      selectFlaw(link.getAttribute('data-use-flaw'));
      document.getElementById('fa-builder').scrollIntoView({ behavior: 'smooth' });
      els.subject.focus({ preventScroll: true });
    });
    update();
  }

  document.addEventListener('DOMContentLoaded', function () {
    ['form', 'flaw', 'subject', 'grade', 'topic', 'prior', 'prompt', 'copy', 'hint'].forEach(function (id) {
      els[id] = document.getElementById('fa-' + id);
    });
    els.levelNote = document.getElementById('fa-level-note');
    fetch(DATA_URL)
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(init)
      .catch(function (err) {
        console.error('[flawed-answer] could not load flaw types:', err);
        els.hint.textContent = HINT_FAILED;
        els.copy.disabled = true;
      });
  });
})();
