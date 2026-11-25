/*
  Barrier Planner — de två promptbyggarna på den dolda sidan för Skool-medlemmar.

  "Plan for a barrier" bygger en prompt av lärarens uppgift, hinder och vad hen
  ser, med dragen från hinderkortet. "Adapt a text" bygger en prompt som
  utvidgar en text utan att förenkla den. Allt sker i webbläsaren: inget
  sparas och inget skickas någonstans. Lärarens text sätts bara som .value och
  attribut, aldrig som HTML.

  Korten läses en gång ur JSON-blocket #bp-data. Själva kopieringen sköts av
  copy-to-clipboard.js, som läser data-copy på knappen — därför hålls
  data-copy alltid lika med prompten.
*/
(function () {
  'use strict';

  var PRIVACY = 'Do not include student names or student work in this conversation.';
  var HINT_PLAN = 'Fill in subject, the task and the barrier to see your prompt.';
  var HINT_ADAPT = 'Fill in subject and paste the text to see your prompt.';

  /* Mallarna är fastställda i specen (avsnitt B5 och B6) — ändra dem bara
     tillsammans med specen. Rader som beror på indata byggs i funktionerna. */
  var PLAN_INTRO = 'You are helping a Grade {grade} {subject} teacher plan support for a barrier that some students in the class meet in one task. Plan for the task and the barrier, not for any one student. Do not ask about students, and do not ask for or use any diagnosis.';
  var GOAL_EMPTY = 'The learning goal: the goal of the task as it is, the same for every student.';
  var MOVES_HEAD = 'Start from these moves and fit them to this task:';
  var FIVE_STRATEGIES = 'Start from these five strategies for the whole class and fit them to this task: flexible grouping, cognitive and metacognitive strategies, explicit instruction, technology, and scaffolding.';
  var PLAN_RULES = [
    'Rules:',
    '- Keep the task and the learning goal the same for everyone. Change the route to the goal, not the goal.',
    '- Do not suggest colored overlays, dyslexia fonts, fidget spinners, extra time in lessons, a separate easier worksheet, or less work as the default.',
    '- Every support can be taken away later.',
    '- If a move needs something the teacher must prepare, say what in one line.'
  ];
  var PLAN_FORMAT = [
    'Reply in plain text, no tables, with exactly these parts. Keep each part under 70 words, so the whole reply stays under 300 words:',
    'FOR THE WHOLE CLASS: two or three moves written for this task: what you do and what students see.',
    'TARGETED: one or two supports for the students who still meet the barrier, and how you will notice during the lesson who they are.',
    'TAKE IT AWAY: which support goes first, and what tells you it is time.',
    'REVIEW: one question to answer in {review}, and what you will look for then.'
  ];
  var ADAPT_TAIL = [
    '',
    'Keep every original sentence. Do not simplify the text or remove anything.',
    '',
    'Reply in plain text, in the language of the text, with the headings in English and exactly these parts:',
    'ADAPTED TEXT: the whole text in short sections, each with one guiding question. After hard words and phrases, add a short explanation or example in brackets.',
    'GLOSSARY: the {n} key words, each with a plain definition and an example sentence.',
    'PICTURE: one picture or diagram that shows the main idea: what it shows and where it goes.',
    'TAKE IT AWAY: which addition to remove first as students manage without it, and which last.'
  ];

  /* Trimmar ett textvärde; saknat värde blir tom sträng. */
  function clean(value) {
    return String(value == null ? '' : value).trim();
  }

  /* Byter ut {namn} i en fast textrad. Används bara på de fasta raderna,
     aldrig på det läraren har skrivit. */
  function fill(line, values) {
    return line.replace(/\{(\w+)\}/g, function (m, key) {
      return Object.prototype.hasOwnProperty.call(values, key) ? values[key] : m;
    });
  }

  /* Bygger planprompten. Ren funktion: samma indata ger alltid samma text.
     input = { subject, grade, task, barrier: id | "other", other, seen, goal,
     review, language }; data = innehållet i #bp-data. Alla textvärden trimmas
     här och sätts sedan in precis som de är skrivna. */
  function buildPlanPrompt(input, data) {
    var subject = clean(input.subject);
    var grade = clean(input.grade);
    var task = clean(input.task);
    var goal = clean(input.goal);
    var seen = clean(input.seen);
    var language = clean(input.language);
    var english = language === '' || language.toLowerCase() === 'english';
    var card = null;
    if (input.barrier !== 'other') {
      ((data && data.cards) || []).forEach(function (c) { if (c.id === input.barrier) card = c; });
    }

    var lines = [
      PRIVACY,
      '',
      fill(PLAN_INTRO, { grade: grade, subject: subject }),
      '',
      'The task as students get it:',
      task,
      '',
      goal ? 'The learning goal, the same for every student: ' + goal : GOAL_EMPTY,
      'The barrier: ' + (card ? card.barrier : clean(input.other))
    ];
    if (seen) lines.push('What the teacher sees: ' + seen);
    lines.push('');

    // Kortets drag (de korta formerna i #bp-data), eller de fem strategierna för eget hinder.
    if (card) {
      lines.push(
        MOVES_HEAD,
        'For the whole class: ' + card.whole_class.join('; '),
        'Targeted: ' + card.targeted.join('; ')
      );
    } else {
      lines.push(FIVE_STRATEGIES);
    }

    lines = lines.concat(
      [''],
      PLAN_RULES,
      [
        '',
        english
          ? 'Write everything in English.'
          : 'Write everything in ' + language + ', but keep the headings in English.',
        ''
      ],
      PLAN_FORMAT.map(function (line) { return fill(line, { review: clean(input.review) }); })
    );
    return lines.join('\n');
  }

  /* Bygger textanpassningsprompten. Ren funktion.
     input = { subject, grade, barrier: "" | alternativets text, words, text }.
     Hinderraden finns bara när ett hinder är valt, med första bokstaven gemen. */
  function buildAdaptPrompt(input) {
    var barrier = clean(input.barrier);
    var line = 'Here is a text I use with Grade ' + clean(input.grade) + ' students in ' + clean(input.subject) + '.';
    if (barrier) {
      line += ' Some students find it hard: ' + barrier.charAt(0).toLowerCase() + barrier.slice(1) + '.';
    }
    return [PRIVACY, '', line, '', 'TEXT:', clean(input.text)]
      .concat(ADAPT_TAIL.map(function (l) { return fill(l, { n: clean(input.words) }); }))
      .join('\n');
  }

  window.BarrierPlanner = { buildPlanPrompt: buildPlanPrompt, buildAdaptPrompt: buildAdaptPrompt };

  /* Visar en färdig prompt, eller tomt läge med ledtråd. */
  function show(out, text, hintText) {
    out.prompt.value = text;
    out.copy.disabled = text === '';
    out.copy.setAttribute('data-copy', text);
    out.hint.textContent = text === '' ? hintText : '';
    out.hint.hidden = text !== '';
  }

  document.addEventListener('DOMContentLoaded', function () {
    var byId = function (id) { return document.getElementById(id); };
    var data = { cards: [] };
    try {
      data = JSON.parse(byId('bp-data').textContent);
    } catch (e) { /* utan kort faller planprompten tillbaka på tomt läge */ }

    var plan = {
      subject: byId('bp-subject'), grade: byId('bp-grade'), task: byId('bp-task'),
      barrier: byId('bp-barrier'), other: byId('bp-barrier-other'),
      otherField: byId('bp-other-field'), link: byId('bp-card-link'),
      seen: byId('bp-seen'), goal: byId('bp-goal'), review: byId('bp-review'),
      language: byId('bp-language'),
      prompt: byId('bp-prompt'), copy: byId('bp-copy'), hint: byId('bp-hint')
    };
    var adaptEls = {
      subject: byId('bp-a-subject'), grade: byId('bp-a-grade'),
      barrier: byId('bp-a-barrier'), words: byId('bp-a-words'), text: byId('bp-a-text'),
      prompt: byId('bp-a-prompt'), copy: byId('bp-a-copy'), hint: byId('bp-a-hint')
    };

    function updatePlan() {
      var choice = plan.barrier.value;
      var isOther = choice === 'other';
      // Fältet "Something else" och länken till kortet följer valet. Det
      // skrivna värdet i fältet behålls när det göms.
      plan.otherField.hidden = !isOther;
      plan.other.required = isOther;
      plan.link.hidden = choice === '' || isOther;
      if (!plan.link.hidden) plan.link.setAttribute('href', '#bp-barrier-' + choice);

      var ready = clean(plan.subject.value) && clean(plan.task.value) && choice &&
        (!isOther || clean(plan.other.value)) &&
        (isOther || data.cards.some(function (c) { return c.id === choice; }));
      show(plan, ready ? buildPlanPrompt({
        subject: plan.subject.value, grade: plan.grade.value, task: plan.task.value,
        barrier: choice, other: plan.other.value, seen: plan.seen.value,
        goal: plan.goal.value, review: plan.review.value, language: plan.language.value
      }, data) : '', HINT_PLAN);
    }

    function updateAdapt() {
      var ready = clean(adaptEls.subject.value) && clean(adaptEls.text.value);
      var opt = adaptEls.barrier.options[adaptEls.barrier.selectedIndex];
      show(adaptEls, ready ? buildAdaptPrompt({
        subject: adaptEls.subject.value, grade: adaptEls.grade.value,
        barrier: adaptEls.barrier.value === '' ? '' : opt.textContent,
        words: adaptEls.words.value, text: adaptEls.text.value
      }) : '', HINT_ADAPT);
    }

    // Textfält ger "input", väljare ger "change"; båda lyssnas på överallt.
    [[plan, updatePlan, ['subject', 'grade', 'task', 'barrier', 'other', 'seen', 'goal', 'review', 'language']],
     [adaptEls, updateAdapt, ['subject', 'grade', 'barrier', 'words', 'text']]].forEach(function (g) {
      g[2].forEach(function (k) {
        g[0][k].addEventListener('input', g[1]);
        g[0][k].addEventListener('change', g[1]);
      });
      g[1]();
    });
  });
})();
