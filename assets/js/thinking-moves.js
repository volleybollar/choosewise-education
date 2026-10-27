/*
  Thinking Moves — promptbyggaren på /thinking-moves/.

  Läser thinking-moves/moves-en.json, fyller listan med drag och bygger
  prompten medan läraren skriver. Allt sker i webbläsaren: inget sparas och
  inget skickas någonstans. Användarens text sätts bara som .value och
  attribut, aldrig som HTML.

  Själva kopieringen sköts av copy-to-clipboard.js, som läser data-copy på
  knappen — därför hålls data-copy alltid lika med prompten.
*/
(function () {
  'use strict';

  var DATA_URL = '/thinking-moves/moves-en.json';
  var HINT_EMPTY = 'Choose a move and fill in subject and topic to see your prompt.';
  var HINT_FAILED = "Couldn't load the moves — reload the page.";

  /* Bygger prompten. Ren funktion: samma indata ger alltid samma text.
     Texten är fastställd i planen (Task 5) — ändra den bara tillsammans
     med PDF:ens luckprompt. */
  function buildPrompt(input) {
    var move = input.move;
    var lines = [
      'Do not include student names or student work in this conversation.',
      '',
      'You are helping a Grade ' + input.grade + ' ' + input.subject +
        " teacher plan a five-minute thinking task for tomorrow's lesson.",
      '',
      'Thinking move: ' + move.name + '. ' + move.one_liner,
      'How to design it: ' + move.prompt_brief,
      '',
      'Lesson topic: ' + input.topic
    ];
    if (input.prior) lines.push('Students already know: ' + input.prior);
    lines.push(
      '',
      "Write the task so it can only be done by thinking about this topic's content, and so students need no devices: paper, whiteboards or talk.",
      '',
      'Reply in plain text, no tables, with exactly these six parts:',
      "MOVE: the move's name and one line on what it trains",
      'TASK: the task, written to the students',
      'LOOK FOR: what strong thinking looks like in their answers',
      'PROBE: one follow-up question that pushes past the first answer',
      'THINK BACK: one sentence starter about how they thought, not what they found',
      'CHECK: any fact in the task the teacher should verify before using it'
    );
    return lines.join('\n');
  }

  window.ThinkingMoves = { buildPrompt: buildPrompt };

  var els = {};
  var movesById = {};

  function value(id) { return els[id].value.trim(); }

  function update() {
    var move = movesById[els.move.value];
    var subject = value('subject');
    var topic = value('topic');
    if (!move || !subject || !topic) {
      els.prompt.value = '';
      els.copy.disabled = true;
      els.copy.setAttribute('data-copy', '');
      els.hint.textContent = HINT_EMPTY;
      return;
    }
    var text = buildPrompt({
      move: move, subject: subject, topic: topic,
      grade: els.grade.value, prior: value('prior')
    });
    els.prompt.value = text;
    els.copy.disabled = false;
    els.copy.setAttribute('data-copy', text);
    els.hint.textContent = '';
  }

  function selectMove(id) {
    if (!movesById[id]) return;
    els.move.value = id;
    update();
  }

  function init(data) {
    data.moves.forEach(function (m) {
      movesById[m.id] = m;
      var opt = document.createElement('option');
      opt.value = m.id;
      opt.textContent = m.number + '. ' + m.name;
      els.move.appendChild(opt);
    });
    var wanted = new URLSearchParams(window.location.search).get('move');
    if (wanted && movesById[wanted]) els.move.value = wanted;

    ['move', 'subject', 'grade', 'topic', 'prior'].forEach(function (id) {
      els[id].addEventListener('input', update);
      els[id].addEventListener('change', update);
    });

    /* "Use this move" på korten väljer draget och hoppar till byggaren
       utan att ladda om sidan. */
    document.addEventListener('click', function (e) {
      var link = e.target.closest('[data-use-move]');
      if (!link) return;
      e.preventDefault();
      selectMove(link.getAttribute('data-use-move'));
      document.getElementById('tm-builder').scrollIntoView({ behavior: 'smooth' });
      els.subject.focus({ preventScroll: true });
    });
    update();
  }

  document.addEventListener('DOMContentLoaded', function () {
    ['move', 'subject', 'grade', 'topic', 'prior', 'prompt', 'copy', 'hint'].forEach(function (id) {
      els[id] = document.getElementById('tm-' + id);
    });
    fetch(DATA_URL)
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(init)
      .catch(function (err) {
        console.error('[thinking-moves] could not load moves:', err);
        els.hint.textContent = HINT_FAILED;
        els.copy.disabled = true;
      });
  });
})();
