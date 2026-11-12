/*
  Study Moves — promptbyggaren på /study-moves/.

  Läser study-moves/moves-en.json, fyller listan med drag och bygger
  prompten medan man skriver. Två versioner: läraren förbereder material
  med AI, eller eleven (13+) studerar med AI som studiekamrat. Allt sker i
  webbläsaren: inget sparas och inget skickas någonstans. Användarens text
  sätts bara som .value, textContent och attribut, aldrig som HTML.

  Själva kopieringen sköts av copy-to-clipboard.js, som läser data-copy på
  knappen — därför hålls data-copy alltid lika med prompten.
*/
(function () {
  'use strict';

  var DATA_URL = '/study-moves/moves-en.json';
  var HINT_EMPTY = 'Fill in subject and topic to see your prompt.';
  var HINT_FAILED = "Couldn't load the moves — reload the page.";

  /* Fältens rubriker och integritetsraden för läraren och för eleven.
     Integritetsraden är två delar: den första står i fetstil. */
  var TEXTS = {
    teacher: {
      topic: 'What is the topic?',
      prior: 'What do students already know? (optional)',
      privacy: ['Do not include student names or student work.',
                'The prompt only needs your subject, grade and topic.']
    },
    student: {
      topic: 'What are you studying?',
      prior: 'What do you already know? (optional)',
      privacy: ['Do not include your name or other personal details.',
                'Check that you are old enough for your AI tool and that your school allows it.']
    }
  };

  /* Lärarens prompt, rad för rad. Texten är fastställd ordagrant i specen
     (avsnittet Prompt builder). Ändra den bara tillsammans med PDF:ens
     luckprompt (exports/build-study-moves-pdf.py) och testerna. */
  function teacherLines(input) {
    var lines = [
      'Do not include student names or student work in this conversation.',
      '',
      'You are helping a Grade ' + input.grade + ' ' + input.subject +
        ' teacher prepare study material that students will use on their own, on paper and without AI.',
      '',
      'Study move: ' + input.move.name + '. ' + input.move.one_liner,
      'What to make: ' + input.move.teacher_ai.brief,
      '',
      'Topic: ' + input.topic
    ];
    if (input.prior) lines.push('Students already know: ' + input.prior);
    lines.push(
      '',
      "Use only this topic's content. Do not repeat a question. If you write multiple-choice questions, make all options about the same length.",
      '',
      'Reply in plain text, no tables, with exactly these four parts:',
      "MOVE: the move's name and one sentence, written to students, on why it works.",
      'FOR STUDENTS: the material, written to the students and ready to print.',
      'ANSWERS: the answers or a checklist students use to check their own work, numbered Q1:, Q2: and so on to match.',
      'CHECK: every fact, figure, date or source in FOR STUDENTS or ANSWERS that the teacher should verify, one per line. Write "None" if there are none.'
    );
    return lines;
  }

  /* Elevens prompt, rad för rad. Reglerna gör att AI:n frågar i stället
     för att svara, och aldrig skriver elevens läxa (specens antimål). */
  function studentLines(input) {
    var lines = [
      'Do not include your name or other personal details in this conversation.',
      '',
      'You are my study partner. I am a Grade ' + input.grade + ' student studying ' + input.subject + '.',
      'Topic: ' + input.topic
    ];
    if (input.prior) lines.push('What I already know: ' + input.prior);
    lines.push(
      '',
      'Study move: ' + input.move.name + '. ' + input.move.one_liner,
      'Your role: ' + input.move.student_ai.brief,
      '',
      'Rules for the whole conversation:',
      '- Give me one question or task at a time, then wait for my answer.',
      '- Never give me the answer to a question before I have tried it. If I am stuck, give a small hint first.',
      '- Keep every message short.',
      '- Do not write my homework, essays or answers for me, even if I ask.',
      '- If you are not sure a fact is right, say so. I will check facts in my textbook or notes.',
      '',
      'Start now.'
    );
    return lines;
  }

  /* Bygger prompten. Ren funktion: samma indata ger alltid samma text.
     input.who är 'teacher' eller 'student'; prior får vara tom. */
  function buildPrompt(input) {
    var lines = input.who === 'student' ? studentLines(input) : teacherLines(input);
    return lines.join('\n');
  }

  window.StudyMoves = { buildPrompt: buildPrompt };

  var els = {};
  // Utan prototyp: ?move=constructor ska inte hitta något.
  var movesById = Object.create(null);
  var loaded = false;

  function value(id) { return els[id].value.trim(); }

  /* Vem som använder AI läses alltid från den valda radioknappen. */
  function currentWho() {
    return els.whoStudent.checked ? 'student' : 'teacher';
  }

  function setWho(who) {
    (who === 'student' ? els.whoStudent : els.whoTeacher).checked = true;
  }

  /* Rubrikerna och integritetsraden följer valet Teacher/Student.
     Fetstilen byggs med createElement, så ingen text tolkas som HTML. */
  function applyTexts(who) {
    var t = TEXTS[who];
    els.topicLabel.textContent = t.topic;
    els.priorLabel.textContent = t.prior;
    var strong = document.createElement('strong');
    strong.textContent = t.privacy[0];
    els.privacy.textContent = '';
    els.privacy.appendChild(strong);
    els.privacy.appendChild(document.createTextNode(' ' + t.privacy[1]));
  }

  function update() {
    var who = currentWho();
    applyTexts(who);
    // Utan data kan ingen prompt byggas, och felmeddelandet ska stå kvar.
    if (!loaded) return;
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
      who: who, move: move, subject: subject, grade: els.grade.value,
      topic: topic, prior: value('prior')
    });
    els.prompt.value = text;
    els.copy.disabled = false;
    els.copy.setAttribute('data-copy', text);
    els.hint.textContent = '';
  }

  function init(data) {
    data.moves.forEach(function (m) {
      movesById[m.id] = m;
      var opt = document.createElement('option');
      opt.value = m.id;
      opt.textContent = m.number + '. ' + m.name;
      els.move.appendChild(opt);
    });
    /* Startdraget och läraren, om inte en länk (?move=, ?for=) har valt
       något annat. Okända värden ignoreras. */
    var params = new URLSearchParams(window.location.search);
    var wanted = params.get('move');
    els.move.value = movesById[wanted] ? wanted : data.default_move;
    var forWho = params.get('for');
    setWho(forWho === 'student' || forWho === 'teacher' ? forWho : 'teacher');
    loaded = true;

    ['move', 'subject', 'grade', 'topic', 'prior'].forEach(function (id) {
      els[id].addEventListener('input', update);
      els[id].addEventListener('change', update);
    });

    /* Länkarna på korten väljer draget och vem som använder AI, och hoppar
       till byggaren utan att ladda om sidan. */
    document.addEventListener('click', function (e) {
      var link = e.target.closest('[data-use-move]');
      if (!link) return;
      e.preventDefault();
      var id = link.getAttribute('data-use-move');
      if (!movesById[id]) return;
      els.move.value = id;
      var forWho = link.getAttribute('data-use-for');
      if (forWho === 'student' || forWho === 'teacher') setWho(forWho);
      update();
      document.getElementById('sm-builder').scrollIntoView({ behavior: 'smooth' });
      els.subject.focus({ preventScroll: true });
    });
    update();
  }

  document.addEventListener('DOMContentLoaded', function () {
    ['move', 'subject', 'grade', 'topic', 'prior', 'prompt', 'copy', 'hint', 'privacy'].forEach(function (id) {
      els[id] = document.getElementById('sm-' + id);
    });
    els.whoTeacher = document.getElementById('sm-who-teacher');
    els.whoStudent = document.getElementById('sm-who-student');
    els.topicLabel = document.getElementById('sm-topic-label');
    els.priorLabel = document.getElementById('sm-prior-label');
    /* Valet Teacher/Student byter rubrikerna även om datafilen inte laddas. */
    [els.whoTeacher, els.whoStudent].forEach(function (radio) {
      radio.addEventListener('change', update);
    });
    fetch(DATA_URL)
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(init)
      .catch(function (err) {
        console.error('[study-moves] could not load moves:', err);
        els.hint.textContent = HINT_FAILED;
        els.copy.disabled = true;
      });
  });
})();
