/*
  Pedagogy Compass — promptbyggaren på den dolda sidan för Skool-medlemmar.

  Läser problemen och modellerna ur JSON-blocket #pc-data (som
  scripts/build-pedagogy-compass.py skriver in i sidan) och bygger prompten
  medan läraren skriver. Allt sker i webbläsaren: inget sparas och inget
  skickas någonstans. Användarens text sätts bara som .value, .textContent
  och attribut, aldrig som HTML.

  Kopieringen sköts av copy-to-clipboard.js, som läser data-copy på knappen —
  därför hålls data-copy alltid lika med prompten.
*/
(function () {
  'use strict';

  var HINT_EMPTY = 'Choose a problem and fill in your subject to see your prompt.';
  // Läses upp av skärmläsare (aria-live) när prompten är klar.
  var HINT_READY = 'Your prompt is ready.';
  var OWN = 'own';

  /* Texten är fastställd i planen — ändra den bara tillsammans med
     affischens baksida (exports/build-pedagogy-compass-pdf.py). */
  var FORMAT = [
    'Reply in plain text, no tables, in exactly this format:',
    'BEST FIRST STEP: which approach to try first and why, given what the teacher sees',
    'NEXT LESSON: what it looks like in one concrete lesson in this subject, with minutes',
    'WATCH FOR: how the teacher will know within two weeks whether it is working',
    'AI: one way AI could help the teacher with this, and one way students\' use of AI could make the problem worse',
    'HONEST NOTE: what the evidence label means for this approach, in one or two lines'
  ];
  /* Utan valda modeller hittade AI:n på egna etiketter i testkörningen, så
     prompten ger den sajtens tre. */
  var NO_MODELS = 'The teacher has not chosen any approaches yet. Suggest two or three research-based approaches that fit this problem, strongest evidence first, and give each one of these labels: Strong (meta-analyses of classroom studies), Promising (controlled studies, but mixed or dependent on context) or Framework (useful for planning, not tested as a method).';

  /* Bygger prompten. Ren funktion: samma indata ger alltid samma text.
     models: [{name, label, one_liner}], starkast evidens först. */
  function buildPrompt(d) {
    var block = d.models.length
      ? 'The teacher is looking at these approaches, strongest evidence first:\n' + d.models.map(function (m) {
          return '- ' + m.name + ' (' + m.label + '): ' + m.one_liner;
        }).join('\n')
      : NO_MODELS;
    return [
      'Do not include student names or student results in this conversation.',
      '',
      'You are helping a Grade ' + d.grade + ' ' + d.subject + ' teacher with a problem in class: ' + d.problem,
      'What the teacher sees: ' + (d.situation || 'Nothing more described.'),
      '',
      block,
      ''
    ].concat(FORMAT).join('\n');
  }

  window.PedagogyCompass = { buildPrompt: buildPrompt };

  var els = {};
  // Utan prototyp: ?problem=constructor ska inte hitta något.
  var problems = Object.create(null);
  var models = Object.create(null);
  var order = [];

  /* Kryssrutorna för valt problem, alla ikryssade, i evidensordning. */
  function renderModels() {
    els.models.textContent = '';
    var p = problems[els.problem.value];
    (p ? p.model_ids : []).forEach(function (id) {
      var m = models[id];
      var li = document.createElement('li');
      var label = document.createElement('label');
      var box = document.createElement('input');
      box.type = 'checkbox';
      box.checked = true;
      box.value = id;
      box.addEventListener('change', update);
      label.append(box, document.createTextNode(' ' + m.name + ' (' + m.label + ')'));
      li.appendChild(label);
      els.models.appendChild(li);
    });
  }

  function update() {
    var own = els.problem.value === OWN;
    els['own-field'].hidden = !own;
    var problem = own ? els.own.value.trim() : (problems[els.problem.value] || {}).name;
    var subject = els.subject.value.trim();
    var text = '';
    if (problem && subject) {
      var picked = Array.prototype.filter.call(els.models.querySelectorAll('input'), function (b) { return b.checked; })
        .map(function (b) { return models[b.value]; });
      text = buildPrompt({
        problem: problem, subject: subject, grade: els.grade.value,
        situation: els.situation.value.trim(), models: picked
      });
    }
    els.prompt.value = text;
    els.copy.disabled = !text;
    els.copy.setAttribute('data-copy', text);
    els.hint.textContent = text ? HINT_READY : HINT_EMPTY;
  }

  function chooseProblem(id) {
    els.problem.value = id;
    renderModels();
    update();
  }

  document.addEventListener('DOMContentLoaded', function () {
    ['problem', 'own', 'own-field', 'subject', 'grade', 'situation', 'models', 'prompt', 'copy', 'hint'].forEach(function (id) {
      els[id] = document.getElementById('pc-' + id);
    });
    var data = JSON.parse(document.getElementById('pc-data').textContent);
    data.models.forEach(function (m) { models[m.id] = m; });
    data.problems.forEach(function (p) {
      problems[p.id] = p;
      order.push(p.id);
      var opt = document.createElement('option');
      opt.value = p.id;
      opt.textContent = p.name;
      els.problem.appendChild(opt);
    });
    var own = document.createElement('option');
    own.value = OWN;
    own.textContent = 'My own problem';
    els.problem.appendChild(own);

    /* ?problem=<id> väljer problemet; allt annat ger det första. */
    var wanted = new URLSearchParams(window.location.search).get('problem');
    chooseProblem(problems[wanted] || wanted === OWN ? wanted : order[0]);

    els.problem.addEventListener('change', function () { chooseProblem(els.problem.value); });
    ['own', 'subject', 'grade', 'situation'].forEach(function (id) {
      els[id].addEventListener('input', update);
      els[id].addEventListener('change', update);
    });

    /* "Use in the prompt" på problemkorten väljer problemet utan omladdning. */
    document.addEventListener('click', function (e) {
      var link = e.target.closest('[data-use-problem]');
      if (!link) return;
      e.preventDefault();
      var id = link.getAttribute('data-use-problem');
      if (!problems[id]) return;
      chooseProblem(id);
      document.getElementById('pc-builder').scrollIntoView({ behavior: 'smooth' });
      els.subject.focus({ preventScroll: true });
    });
  });
})();
