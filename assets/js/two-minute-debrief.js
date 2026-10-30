/*
  Two-Minute Debrief — debriefen på /two-minute-debrief/.

  Bygger promptarna medan läraren skriver: debriefen, kvällsprompten för
  dagens sparade debriefer, veckosammanställningen och hinge-frågan. Allt sker
  i webbläsaren och inget skickas någonstans. Användarens text sätts bara som
  .value, .textContent och attribut, aldrig som HTML.

  Själva kopieringen sköts av copy-to-clipboard.js, som läser data-copy på
  knappen — därför hålls data-copy alltid lika med prompten.
*/
(function () {
  'use strict';

  var HINT_EMPTY = 'Fill in group, goal, evidence and next to see your prompt.';
  // Läses upp av skärmläsare (aria-live) när prompten är klar.
  var HINT_READY = 'Your prompt is ready.';

  var PRIVACY = 'Do not include student names or student results in this conversation.';

  /* Svarsformatet för en debrief. Texten är fastställd i planen — ändra den
     bara tillsammans med PDF:ens luckprompt (exports/build-two-minute-debrief-pdf.py). */
  var DEBRIEF_FORMAT = [
    'LIKELY CAUSES: two possible explanations, numbered 1 and 2, each tied to this lesson\'s content, and what would tell them apart. Look beyond the first explanation: missing prior knowledge, too much new at once, a common misconception, a task that did not make students think about the goal, or too little practice.',
    'NEXT LESSON: one concrete move aimed at the more likely cause, with minutes. Not "re-teach".',
    'CHECK FIRST: one quick question or task, written exactly as students will see it, and when to move on, for example "Move on if about 4 in 5 get it right". If the evidence is only a feeling, also say what to look at to turn the feeling into evidence.',
    'ONE QUESTION: one question back to the teacher, to think further.'
  ];

  /* De fyra svaren, med "None given" när överraskningen är tom. */
  function answers(d) {
    return [
      'Goal: ' + d.goal,
      'Evidence: ' + d.evidence,
      'Surprise: ' + (d.surprise && d.surprise.trim() ? d.surprise : 'None given'),
      'Next: ' + d.next
    ];
  }

  /* En debrief. Ren funktion: samma indata ger alltid samma text. */
  function buildDebriefPrompt(d) {
    return [
      PRIVACY,
      '',
      'You are helping a Grade ' + d.grade + ' teacher think through a lesson with ' + d.group +
        ' that did not go as planned. Base everything on what the teacher writes below, and tie every point to this lesson\'s content.',
      ''
    ].concat(answers(d), [
      '',
      'Reply in plain text, no tables, in exactly this format:'
    ], DEBRIEF_FORMAT).join('\n');
  }

  /* Flera debriefer i slutet av dagen, var och en med sin grupp som rubrik. */
  function buildBatchPrompt(list) {
    var lines = [
      PRIVACY,
      '',
      'You are helping a teacher think through ' + list.length +
        ' lessons from today that did not go as planned. Treat each debrief on its own. Base everything on what the teacher writes, and tie every point to that lesson\'s content.',
      ''
    ];
    list.forEach(function (d, i) {
      lines.push('DEBRIEF ' + (i + 1) + ': ' + d.group + ', Grade ' + d.grade);
      lines = lines.concat(answers(d));
      lines.push('');
    });
    lines.push('Reply in plain text, no tables. For each debrief, write its number and group as a heading, then exactly this format:');
    return lines.concat(DEBRIEF_FORMAT).join('\n');
  }

  /* Veckosammanställningen. Texten är fastställd i planen, som debriefen. */
  function buildRollupPrompt(text) {
    return [
      PRIVACY,
      '',
      'You are helping a teacher look back on a week of lesson debriefs. Each debrief has a date, a group, a goal, evidence, a surprise and a next step. Some evidence starts with the result of a check from an earlier lesson.',
      '',
      'Debriefs:',
      text,
      '',
      'Reply in plain text, no tables, in exactly this format:',
      'PATTERNS: up to three patterns across the week that one lesson would not show. After each, name the debriefs it comes from by date and group.',
      'WHAT WORKED: any change whose later check showed improvement. If there are no check results yet, write "Not enough check results yet".',
      'ONE CHANGE FOR NEXT WEEK: one concrete change to the teacher\'s routine.',
      'ONE QUESTION: one question back to the teacher.'
    ].join('\n');
  }

  /* En hinge-fråga för lärarens eget mål. */
  function buildHingePrompt(d) {
    return [
      PRIVACY,
      '',
      'Write one hinge question for a Grade ' + d.grade + ' lesson with ' + d.group + '. The goal of the lesson: ' + d.goal,
      'Give four options, A to D, of about the same length. Exactly one is correct. Each wrong option shows a common misconception about this goal.',
      '',
      'Reply in plain text, no tables:',
      'QUESTION: the question and options exactly as students will see them',
      'KEY: the correct letter, and for each wrong option the misconception it shows'
    ].join('\n');
  }

  /* En flik eller radbrytning i ett svar skulle dela raden i fel kolumner
     när den klistras in i journalen, så de blir mellanslag. */
  function cell(s) { return String(s || '').replace(/[\t\r\n]+/g, ' ').trim(); }

  /* En rad till enhetsjournalen: åtta kolumner, de två sista tomma
     (Change I made och Check result fyller läraren i själv). */
  function journalRow(s) {
    return [s.date, 'Grade ' + s.grade + ' · ' + s.group, s.goal, s.evidence, s.surprise, s.next, '', '']
      .map(cell).join('\t');
  }

  /* Gruppnamn jämförs utan hänsyn till versaler och extra mellanslag. */
  function normalizeGroup(s) { return String(s || '').toLowerCase().replace(/\s+/g, ' ').trim(); }

  window.TwoMinuteDebrief = {
    buildDebriefPrompt: buildDebriefPrompt,
    buildBatchPrompt: buildBatchPrompt,
    buildRollupPrompt: buildRollupPrompt,
    buildHingePrompt: buildHingePrompt,
    journalRow: journalRow,
    normalizeGroup: normalizeGroup
  };

  var els = {};

  function value(id) { return els[id].value.trim(); }

  /* Debriefen som den står i formuläret just nu. */
  function current() {
    return {
      group: value('group'), grade: els.grade.value, goal: value('goal'),
      evidence: value('evidence'), surprise: value('surprise'), next: value('next')
    };
  }

  function complete(d) { return d.group && d.goal && d.evidence && d.next; }

  /* Sätter en promptruta och dess kopieringsknapp i ett svep, så att
     data-copy aldrig skiljer sig från det som syns. */
  function setPrompt(box, button, text) {
    box.value = text;
    button.disabled = !text;
    button.setAttribute('data-copy', text);
  }

  function update() {
    var d = current();
    var ready = complete(d);
    setPrompt(els.prompt, els.copy, ready ? buildDebriefPrompt(d) : '');
    els.hint.textContent = ready ? HINT_READY : HINT_EMPTY;
    setPrompt(els['hinge-prompt'], els['hinge-copy'], d.group && d.goal ? buildHingePrompt(d) : '');
  }

  document.addEventListener('DOMContentLoaded', function () {
    ['group', 'grade', 'goal', 'evidence', 'surprise', 'next', 'prompt', 'copy', 'hint',
     'hinge-prompt', 'hinge-copy'].forEach(function (id) {
      els[id] = document.getElementById('td-' + id);
    });
    ['group', 'grade', 'goal', 'evidence', 'surprise', 'next'].forEach(function (id) {
      els[id].addEventListener('input', update);
      els[id].addEventListener('change', update);
    });
    update();
  });
})();
