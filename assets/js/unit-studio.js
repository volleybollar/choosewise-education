/*
  Unit Studio — promptbyggaren på den dolda sidan för Skool-medlemmar.

  Läser stegen ur JSON-blocket #us-data (som scripts/build-unit-studio.py
  skriver in i sidan) och bygger prompten medan läraren skriver. Allt sker i
  webbläsaren: inget sparas och inget skickas någonstans. Användarens text
  sätts bara som .value och attribut, aldrig som HTML.

  Kopieringen sköts av copy-to-clipboard.js, som läser data-copy på knappen —
  därför hålls data-copy alltid lika med prompten.
*/
(function () {
  'use strict';

  var HINT_EMPTY = 'Fill in subject and your unit to see your prompt.';
  // Läses upp av skärmläsare (aria-live) när prompten är klar.
  var HINT_READY = 'Your prompt is ready.';
  var PRIVACY = 'Do not include student names or student results in this conversation.';
  var LABEL_IMPROVE = 'The unit as you have planned it';
  var LABEL_NEW = 'The topic and goals of the new unit';

  /* Texten är fastställd i planen — ändra den bara tillsammans med
     metodkortets luckprompt (exports/build-unit-studio-pdf.py). */
  var STEP_FORMAT = [
    'Reply in plain text, no tables, in exactly this format:',
    'KEEP: what already works for this step, in one or two lines. For a new unit, what in the topic and goals is already clear.',
    'SUGGEST: at most three changes for this step, numbered, each tied to this unit\'s content, each with one line on why it helps students learn.',
    'QUESTION: one question back to the teacher before the next step.',
    'AI CAN ALSO: one other way an AI tool could help with this step, written as a short prompt the teacher can copy.'
  ];
  var FINAL_FORMAT = [
    'Reply in plain text, no tables, in exactly this format:',
    'GOAL AND EVIDENCE: what students should be able to do by the end, and how the teacher will see it',
    'PRIOR KNOWLEDGE: what students need first, and how to check it in the first lesson',
    'LESSONS: one line per lesson, numbered, with what students do and roughly how long',
    'RETRIEVAL: which earlier content returns in which lessons',
    'CHECKPOINTS: where in the unit to check understanding, how, and what to do if fewer than about 4 in 5 get it',
    'AI USE: where students use AI in this unit, where they do not, and why',
    'CHANGES: what is different from the original plan, one line each, or "New unit"',
    'CHECK: anything the teacher should verify before teaching, one per line, or "None"'
  ];

  /* Enheten, med en inledning som beror på läget. */
  function unitBlock(d) {
    return (d.mode === 'new'
      ? 'The teacher is planning a new unit. Topic and goals:\n'
      : 'The unit as the teacher has planned it:\n') + d.unit;
  }

  function about(d) {
    return 'a unit of ' + d.weeks + ' weeks with ' + d.lessons + ' lessons a week';
  }

  /* Ett av de fem stegen. Ren funktion: samma indata ger alltid samma text. */
  function buildStepPrompt(d) {
    return [
      PRIVACY,
      '',
      'You are helping a Grade ' + d.grade + ' ' + d.subject + ' teacher improve ' + about(d) +
        '. We work through five steps, one at a time. This is step ' + d.step.num + ' of 5: ' + d.step.name + '.',
      '',
      unitBlock(d),
      '',
      'Decisions so far: ' + (d.decisions || 'None yet. If earlier steps are in this conversation, build on what the teacher decided there.'),
      '',
      d.step.brief,
      ''
    ].concat(STEP_FORMAT).join('\n');
  }

  /* Slutsteget: AI:n skriver den förbättrade planen, läraren granskar. */
  function buildFinalPrompt(d) {
    return [
      PRIVACY,
      '',
      'You are helping a Grade ' + d.grade + ' ' + d.subject + ' teacher write the improved plan for ' + about(d) +
        '. Use the unit and the decisions below. Where the teacher has not decided something, choose what the research behind the five steps supports, and say so.',
      '',
      unitBlock(d),
      '',
      'Decisions from the five steps: ' + (d.decisions || 'See the earlier steps in this conversation.'),
      ''
    ].concat(FINAL_FORMAT).join('\n');
  }

  window.UnitStudio = { buildStepPrompt: buildStepPrompt, buildFinalPrompt: buildFinalPrompt };

  var els = {};
  // Utan prototyp: ?step=constructor ska inte hitta något.
  var stepsByNum = Object.create(null);

  function mode() { return els['mode-new'].checked ? 'new' : 'improve'; }

  function update() {
    els['unit-label'].textContent = mode() === 'new' ? LABEL_NEW : LABEL_IMPROVE;
    var d = {
      mode: mode(), subject: els.subject.value.trim(), grade: els.grade.value, weeks: els.weeks.value,
      lessons: els.lessons.value, unit: els.unit.value.trim(), decisions: els.decisions.value.trim()
    };
    var text = '';
    if (d.subject && d.unit) {
      if (els.step.value === 'final') {
        text = buildFinalPrompt(d);
      } else {
        d.step = stepsByNum[els.step.value];
        text = buildStepPrompt(d);
      }
    }
    els.prompt.value = text;
    els.copy.disabled = !text;
    els.copy.setAttribute('data-copy', text);
    els.hint.textContent = text ? HINT_READY : HINT_EMPTY;
  }

  document.addEventListener('DOMContentLoaded', function () {
    ['mode-improve', 'mode-new', 'subject', 'grade', 'weeks', 'lessons', 'unit', 'unit-label', 'step',
     'decisions', 'prompt', 'copy', 'hint'].forEach(function (id) {
      els[id] = document.getElementById('us-' + id);
    });
    JSON.parse(document.getElementById('us-data').textContent).steps.forEach(function (s) {
      stepsByNum[String(s.num)] = s;
    });

    /* ?step=3 eller ?step=final väljer steget; allt annat ger steg 1. */
    var wanted = new URLSearchParams(window.location.search).get('step');
    els.step.value = (wanted === 'final' || stepsByNum[wanted]) ? wanted : '1';

    ['mode-improve', 'mode-new', 'subject', 'grade', 'weeks', 'lessons', 'unit', 'step', 'decisions'].forEach(function (id) {
      els[id].addEventListener('input', update);
      els[id].addEventListener('change', update);
    });

    /* "Use this step" på korten väljer steget utan att ladda om sidan. */
    document.addEventListener('click', function (e) {
      var link = e.target.closest('[data-use-step]');
      if (!link) return;
      e.preventDefault();
      els.step.value = link.getAttribute('data-use-step');
      update();
      document.getElementById('us-builder').scrollIntoView({ behavior: 'smooth' });
    });
    update();
  });
})();
