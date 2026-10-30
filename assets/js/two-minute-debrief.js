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

  /* ---------- Sparade debriefer ----------
     Bara i den här webbläsaren (localStorage). Tas bort efter 14 dagar. */
  var KEY = 'choosewise.debrief.v1';
  var KEEP_MS = 14 * 24 * 3600 * 1000;
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var HINT_NO_BATCH = 'No unanalysed debriefs saved today.';
  var HINT_ROLLUP_EMPTY = 'Tick saved debriefs or paste rows from your unit journal.';
  var WEEK_MS = 7 * 24 * 3600 * 1000;
  var EVIDENCE_PLACEHOLDER = 'On the exit ticket, 11 of 27 forgot to divide the + 5.';
  var FOLLOWUP_PLACEHOLDER = 'Check: 20 of 27 right, up from 16. Most now divide the whole side.';

  /* Besökarens lokala datum. toISOString() ger UTC och skulle göra en
     debrief sparad sent på kvällen till fel dag. */
  function localDate(d) {
    function pad(n) { return (n < 10 ? '0' : '') + n; }
    return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
  }

  /* "2026-10-28" blir "28 Oct". */
  function shortDate(iso) {
    var parts = iso.split('-');
    return parseInt(parts[2], 10) + ' ' + MONTHS[parseInt(parts[1], 10) - 1];
  }

  function prune(list, nowMs) {
    return list.filter(function (s) { return nowMs - s.savedAt <= KEEP_MS; });
  }

  /* Den senast sparade debriefen för samma grupp, eller null. */
  function lastForGroup(list, group) {
    var wanted = normalizeGroup(group);
    var best = null;
    list.forEach(function (s) {
      if (wanted && normalizeGroup(s.group) === wanted && (!best || s.savedAt > best.savedAt)) best = s;
    });
    return best;
  }

  /* Bara poster som ser ut som en sparad debrief räknas; annat i lagringen
     (trasig JSON, något annat program) behandlas som tomt. */
  function isSaved(s) {
    return !!s && typeof s === 'object' && typeof s.group === 'string' && typeof s.date === 'string' &&
      /^\d{4}-\d{2}-\d{2}$/.test(s.date) && typeof s.savedAt === 'number';
  }

  /* Provar att skriva och ta bort en post. Kastar webbläsaren (privat
     fönster, blockerad lagring) finns ingen lagring. */
  function storageWorks() {
    try {
      window.localStorage.setItem(KEY + '.test', '1');
      window.localStorage.removeItem(KEY + '.test');
      return true;
    } catch (e) {
      return false;
    }
  }

  function load() {
    try {
      var list = JSON.parse(window.localStorage.getItem(KEY) || '[]');
      return Array.isArray(list) ? list.filter(isSaved) : [];
    } catch (e) {
      return [];
    }
  }

  function store(list) {
    try {
      window.localStorage.setItem(KEY, JSON.stringify(list));
    } catch (e) {
      console.error('[two-minute-debrief] could not save:', e);
    }
  }

  /* En rad per debrief till veckosammanställningen. */
  function rollupLines(list) {
    return list.map(function (s) {
      return [s.date, s.group + ', Grade ' + s.grade].concat(answers(s)).map(cell).join(' | ');
    }).join('\n');
  }

  window.TwoMinuteDebrief = {
    buildDebriefPrompt: buildDebriefPrompt,
    buildBatchPrompt: buildBatchPrompt,
    buildRollupPrompt: buildRollupPrompt,
    buildHingePrompt: buildHingePrompt,
    journalRow: journalRow,
    normalizeGroup: normalizeGroup,
    localDate: localDate,
    prune: prune,
    lastForGroup: lastForGroup,
    rollupLines: rollupLines
  };

  var els = {};
  var canSave = false;
  var saved = [];

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

  /* Visar förra debriefen för samma grupp ovanför Evidence, om det finns en.
     Inget fylls i automatiskt: läraren kan strunta i noten. */
  function updateFollowup() {
    var last = canSave ? lastForGroup(saved, value('group')) : null;
    if (last) {
      els.followup.textContent = 'Last time (' + shortDate(last.date) + '): ' + last.next + ' What did your check show?';
      els.followup.hidden = false;
      els.evidence.placeholder = FOLLOWUP_PLACEHOLDER;
    } else {
      els.followup.textContent = '';
      els.followup.hidden = true;
      els.evidence.placeholder = EVIDENCE_PLACEHOLDER;
    }
  }

  function update() {
    var d = current();
    var ready = complete(d);
    setPrompt(els.prompt, els.copy, ready ? buildDebriefPrompt(d) : '');
    els.hint.textContent = ready ? HINT_READY : HINT_EMPTY;
    els.save.disabled = !ready;
    setPrompt(els['hinge-prompt'], els['hinge-copy'], d.group && d.goal ? buildHingePrompt(d) : '');
    updateFollowup();
  }

  /* Dagens sparade debriefer som inte körts än. */
  function todaysOpen() {
    var today = localDate(new Date());
    return saved.filter(function (s) { return s.date === today && !s.analysed; });
  }

  function button(label, cls) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'btn ' + cls;
    b.textContent = label;
    return b;
  }

  /* Listan över sparade debriefer, nyast först, och kvällsprompten. */
  function renderSaved() {
    els.saved.textContent = '';
    saved.slice().sort(function (a, b) { return b.savedAt - a.savedAt; }).forEach(function (s) {
      var li = document.createElement('li');
      var label = document.createElement('span');
      label.textContent = shortDate(s.date) + ' · ' + s.group + (s.analysed ? ' (run)' : '');
      var copyRow = button('Copy journal row', 'btn--secondary');
      copyRow.setAttribute('data-copy', journalRow(s));
      var del = button('Delete', 'btn--secondary');
      del.addEventListener('click', function () {
        saved = saved.filter(function (x) { return x.id !== s.id; });
        store(saved);
        renderAll();
      });
      var toast = document.createElement('span');
      toast.className = 'copy-toast';
      toast.setAttribute('role', 'status');
      toast.textContent = 'Copied';
      li.append(label, copyRow, del, toast);
      els.saved.appendChild(li);
    });
    var open = todaysOpen();
    setPrompt(els['batch-prompt'], els['batch-copy'], open.length ? buildBatchPrompt(open) : '');
    els['batch-hint'].textContent = open.length
      ? open.length + (open.length === 1 ? ' debrief' : ' debriefs') + ' from today in this prompt.'
      : HINT_NO_BATCH;
  }

  /* Kryssrutorna i veckosammanställningen: sparade debriefer från de senaste
     7 dagarna, nyast först. Urvalet bevaras när listan ritas om. */
  var unticked = {};

  function renderRollupList() {
    els['rollup-list'].textContent = '';
    var now = Date.now();
    saved.filter(function (s) { return now - s.savedAt <= WEEK_MS; })
      .sort(function (a, b) { return b.savedAt - a.savedAt; })
      .forEach(function (s) {
        var li = document.createElement('li');
        var label = document.createElement('label');
        var box = document.createElement('input');
        box.type = 'checkbox';
        box.checked = !unticked[s.id];
        box.addEventListener('change', function () {
          unticked[s.id] = !box.checked;
          updateRollup();
        });
        var text = document.createElement('span');
        text.textContent = ' ' + shortDate(s.date) + ' · ' + s.group;
        label.append(box, text);
        li.appendChild(label);
        els['rollup-list'].appendChild(li);
      });
  }

  function updateRollup() {
    var now = Date.now();
    var picked = canSave ? saved.filter(function (s) { return now - s.savedAt <= WEEK_MS && !unticked[s.id]; })
      .sort(function (a, b) { return a.savedAt - b.savedAt; }) : [];
    var parts = [];
    if (picked.length) parts.push(rollupLines(picked));
    var pasted = els['rollup-paste'].value.trim();
    if (pasted) parts.push(pasted);
    var text = parts.length ? buildRollupPrompt(parts.join('\n')) : '';
    setPrompt(els['rollup-prompt'], els['rollup-copy'], text);
    els['rollup-hint'].textContent = text ? HINT_READY : HINT_ROLLUP_EMPTY;
  }

  function renderAll() {
    renderSaved();
    renderRollupList();
    updateRollup();
    updateFollowup();
  }

  function save() {
    var d = current();
    if (!complete(d)) return;
    var now = Date.now();
    saved.push({
      id: String(now) + '-' + saved.length, date: localDate(new Date(now)), savedAt: now,
      group: d.group, grade: d.grade, goal: d.goal, evidence: d.evidence, surprise: d.surprise,
      next: d.next, analysed: false
    });
    store(saved);
    /* Gruppen och årskursen står kvar: nästa debrief är ofta samma klass. */
    ['goal', 'evidence', 'surprise', 'next'].forEach(function (id) { els[id].value = ''; });
    renderAll();
    update();
  }

  document.addEventListener('DOMContentLoaded', function () {
    ['group', 'grade', 'goal', 'evidence', 'surprise', 'next', 'prompt', 'copy', 'hint', 'save',
     'followup', 'saved-area', 'saved', 'storage-note', 'batch-prompt', 'batch-copy', 'batch-hint',
     'delete-all', 'hinge-prompt', 'hinge-copy', 'rollup-list', 'rollup-paste', 'rollup-prompt',
     'rollup-copy', 'rollup-hint'].forEach(function (id) {
      els[id] = document.getElementById('td-' + id);
    });
    ['group', 'grade', 'goal', 'evidence', 'surprise', 'next'].forEach(function (id) {
      els[id].addEventListener('input', update);
      els[id].addEventListener('change', update);
    });

    canSave = storageWorks();
    if (canSave) {
      saved = prune(load(), Date.now());
      store(saved);
      els.save.addEventListener('click', save);
      /* Markeringen väntar ett varv, så att copy-to-clipboard.js hinner läsa
         data-copy innan prompten töms. */
      els['batch-copy'].addEventListener('click', function () {
        var ids = todaysOpen().map(function (s) { return s.id; });
        setTimeout(function () {
          saved.forEach(function (s) { if (ids.indexOf(s.id) !== -1) s.analysed = true; });
          store(saved);
          renderAll();
        }, 0);
      });
      els['delete-all'].addEventListener('click', function () {
        saved = [];
        store(saved);
        renderAll();
      });
      renderAll();
    } else {
      els.save.hidden = true;
      els['saved-area'].hidden = true;
      els['storage-note'].hidden = false;
      els['rollup-list'].parentElement.hidden = true;
    }
    els['rollup-paste'].addEventListener('input', updateRollup);
    updateRollup();
    update();
  });
})();
