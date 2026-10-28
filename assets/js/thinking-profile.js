/*
  Thinking Profile — planeringsbyggaren på /thinking-profile/.

  Läser fyra JSON-filer (stegar, tankeförflyttningar, felsorter, partyper),
  sätter ihop uppgiftslistan och bygger prompten medan läraren skriver.
  Allt sker i webbläsaren: inget sparas och inget skickas någonstans.
  Användarens text sätts bara som .value och attribut, aldrig som HTML.

  Själva kopieringen sköts av copy-to-clipboard.js, som läser data-copy på
  knappen — därför hålls data-copy alltid lika med prompten.
*/
(function () {
  'use strict';

  var LADDERS_URL = '/thinking-profile/ladders-en.json';
  var MOVES_URL = '/thinking-moves/moves-en.json';
  var FLAWS_URL = '/flawed-answer/flaws-en.json';
  var PAIRS_URL = '/side-by-side/pairs-en.json';
  var SITE = 'https://choosewise.education';
  var HINT_EMPTY = 'Choose a thinking cluster, then fill in subject and topic.';
  var HINT_FAILED = "Couldn't load the ladders — reload the page.";

  /* Veckor: 3–8. Tomt eller inte ett tal ger 6. */
  function clampWeeks(raw) {
    var n = parseInt(raw, 10);
    if (isNaN(n)) return 6;
    return Math.min(8, Math.max(3, n));
  }

  function taskLine(t) {
    return '- ' + t.name + ' (' + t.tool + '): ' + t.one_liner + ' ' + t.url;
  }

  /* Bygger prompten. Ren funktion: samma indata ger alltid samma text.
     Ändra texten bara tillsammans med PDF:ens promptkort — ett test vaktar
     att svarsformatet är lika. Svarsformatets rader står som egna strängar,
     en per rad, så att testet kan läsa ut dem. */
  function buildPrompt(input) {
    var cluster = input.cluster;
    var ladder = input.ladder;
    /* Regulating har en egen regeluppsättning: Think back avslutar varje
       uppgift, så de vanliga reglerna om föredragna uppgifter och om
       stegen på uppgiftssvaret skulle motsäga den. */
    var rules = input.rules.join(' ');
    var lines = [
      'Do not include student names or student work in this conversation.',
      '',
      'You are helping a Grade ' + input.grade + ' ' + input.subject + ' teacher plan a ' + input.weeks +
        '-week unit so that students practise one kind of thinking all the way through it, instead of handing their thinking to AI. Students do the tasks on paper, without AI. After each task they mark which step of a four-step ladder their answer reached. The ladder is for students\' own self-check. It is never graded.',
      '',
      'Unit topic: ' + input.topic
    ];
    if (input.overview) lines.push('Unit outline: ' + input.overview);
    lines.push(
      '',
      'Thinking to follow: ' + cluster.name + '. ' + cluster.description,
      'The ladder:'
    );
    ladder.steps.forEach(function (s, i) { lines.push((i + 1) + '. ' + s.text); });
    lines.push(
      '',
      'Each task below is made in its own free builder on choosewise.education; the teacher types in the inputs you give, and the builder makes the task sheet students answer on paper.',
      'Builder fields. All three: Subject, Grade, What is the lesson about? (at most 400 characters), What do students already know? (optional). Thinking Moves also has Thinking move (the task name); grades 8 to 12. Flawed Answer also has Flaw type and How hard should the flaw be to spot? (Easier to spot or Harder to spot); grades 8 to 12. Side by Side also has Pair type and How hard should the difference be to see? (Easier to see or Harder to see); grades 7 to 12. If the unit grade is not offered, use the nearest. The builder writes the task itself, so put the case, numbers or text for students into What is the lesson about?',
      'Preferred tasks, because they train ' + cluster.name + ':'
    );
    input.preferred.forEach(function (t) { lines.push(taskLine(t)); });
    lines.push('Other tasks you may borrow:');
    input.others.forEach(function (t) { lines.push(taskLine(t)); });
    lines.push(
      '',
      'Rules: ' + rules + ' Do not invent studies or sources.',
      '',
      'Reply in plain text, no tables, in this order:',
      'THE THINKING THREAD: one or two sentences on what kind of thinking this unit trains and why it fits the topic',
      'PLAN: four to six tasks spread across the weeks. For each task write',
      'WEEK:',
      'TASK: the task name and the tool',
      'WHAT STUDENTS DO: one sentence',
      'ROOM FOR STEP: the highest step this task gives room for',
      'BUILDER INPUTS: one Field: value line per field of that builder, as listed above',
      'LINK: the builder link',
      'TELL STUDENTS: three or four sentences the teacher reads at the start of the unit, introducing the ladder and saying it is never graded',
      'CHECK: facts or claims in the plan that could be wrong, one per line, at most four lines. Write "None" if there are none.'
    );
    return lines.join('\n');
  }

  window.ThinkingProfile = { buildPrompt: buildPrompt };

  var els = {};
  var data = {};

  function value(id) { return els[id].value.trim(); }

  /* Sätter ihop alla 14 uppgifter: tolv tankeförflyttningar plus Flawed
     Answer och Side by Side. Varje uppgift får en nyckel som stegarna i
     ladders-en.json pekar på. */
  function assembleTasks(moves, flaws, pairs) {
    var all = moves.moves.map(function (m) {
      return {
        key: 'thinking-moves:' + m.id,
        name: m.name, tool: 'Thinking Moves', one_liner: m.one_liner,
        url: SITE + '/thinking-moves/?move=' + m.id
      };
    });
    all.push({
      key: 'flawed-answer', name: 'Flawed Answer', tool: 'Flawed Answer',
      one_liner: 'Students find and explain the flaw in an answer that looks right. Flaw types: ' +
        flaws.flaws.map(function (f) { return f.name; }).join(', ') + '.',
      url: SITE + '/flawed-answer/'
    });
    all.push({
      key: 'side-by-side', name: 'Side by Side', tool: 'Side by Side',
      one_liner: 'Students compare two items placed next to each other, write the rule they find and try it on a new case. Pair types: ' +
        pairs.pairs.map(function (p) { return p.name; }).join(', ') + '.',
      url: SITE + '/side-by-side/'
    });
    return all;
  }

  function update() {
    var cluster = data.clusters[els.cluster.value];
    var ladder = data.ladders[els.cluster.value];
    var subject = value('subject');
    var topic = value('topic');
    if (!cluster || !ladder || !subject || !topic) {
      els.prompt.value = '';
      els.copy.disabled = true;
      els.copy.setAttribute('data-copy', '');
      els.hint.textContent = HINT_EMPTY;
      return;
    }
    var keys = ladder.tasks.map(function (t) {
      return t.id ? t.tool + ':' + t.id : t.tool;
    });
    var preferred = keys.map(function (k) { return data.tasksByKey[k]; }).filter(Boolean);
    var others = data.tasks.filter(function (t) { return keys.indexOf(t.key) === -1; });
    var text = buildPrompt({
      cluster: cluster, ladder: ladder, preferred: preferred, others: others,
      rules: els.cluster.value === 'regulating' ? data.rulesRegulating : data.rules,
      subject: subject, grade: els.grade.value, weeks: clampWeeks(els.weeks.value),
      topic: topic, overview: value('overview')
    });
    els.prompt.value = text;
    els.copy.disabled = false;
    els.copy.setAttribute('data-copy', text);
    els.hint.textContent = '';
  }

  function selectCluster(id) {
    if (!data.clusters[id]) return;
    els.cluster.value = id;
    update();
  }

  function init(res) {
    var ladders = res[0], moves = res[1], flaws = res[2], pairs = res[3];
    data.clusters = {};
    moves.clusters.forEach(function (c) { data.clusters[c.id] = c; });
    data.ladders = {};
    ladders.ladders.forEach(function (l) { data.ladders[l.cluster] = l; });
    data.rules = ladders.rules;
    data.rulesRegulating = ladders.rules_regulating;
    data.tasks = assembleTasks(moves, flaws, pairs);
    data.tasksByKey = {};
    data.tasks.forEach(function (t) { data.tasksByKey[t.key] = t; });

    var wanted = new URLSearchParams(window.location.search).get('cluster');
    if (wanted && data.clusters[wanted]) els.cluster.value = wanted;

    /* Alla fält bygger om prompten när de ändras. */
    els.form.addEventListener('input', update);
    els.form.addEventListener('change', update);

    /* "Plan with this ladder" på korten väljer stegen och hoppar till
       byggaren utan att ladda om sidan. */
    document.addEventListener('click', function (e) {
      var link = e.target.closest('[data-use-cluster]');
      if (!link) return;
      e.preventDefault();
      selectCluster(link.getAttribute('data-use-cluster'));
      document.getElementById('tp-builder').scrollIntoView({ behavior: 'smooth' });
      els.subject.focus({ preventScroll: true });
    });
    update();
  }

  function load(url) {
    return fetch(url).then(function (res) {
      if (!res.ok) throw new Error('HTTP ' + res.status + ' ' + url);
      return res.json();
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    ['form', 'cluster', 'subject', 'grade', 'weeks', 'topic', 'overview', 'prompt', 'copy', 'hint'].forEach(function (id) {
      els[id] = document.getElementById('tp-' + id);
    });
    Promise.all([load(LADDERS_URL), load(MOVES_URL), load(FLAWS_URL), load(PAIRS_URL)])
      .then(init)
      .catch(function (err) {
        console.error('[thinking-profile] could not load the ladders:', err);
        els.hint.textContent = HINT_FAILED;
        els.copy.disabled = true;
      });
  });
})();
