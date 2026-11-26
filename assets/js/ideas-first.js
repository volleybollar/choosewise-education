/*
  Ideas first — promptbyggaren på den dolda sidan för Skool-medlemmar.

  Bygger en prompt av lärarens ämne, mål och egna idéer, så att läraren har
  egna idéer på bordet innan AI-verktyget får svara. Allt sker i webbläsaren:
  inget sparas och inget skickas någonstans. Lärarens text sätts bara som
  .value och attribut, aldrig som HTML.

  Själva kopieringen sköts av copy-to-clipboard.js, som läser data-copy på
  knappen — därför hålls data-copy alltid lika med prompten.
*/
(function () {
  'use strict';

  var PRIVACY = 'Do not include student names or student work in this conversation.';
  var HINT = 'Write the subject, the goal and at least one idea of your own to see your prompt.';

  /* Mallen är fastställd i specen (avsnitt B4) — ändra den bara tillsammans
     med specen. En uppsättning rader per läge: "me" (en lärare) och "team". */
  var MODES = {
    me: {
      intro: 'I teach {subject} to Grade {grade}.',
      ideasHead: 'My own ideas so far:',
      ask: 'Give me eight ideas for an activity that reaches this goal, each clearly different from the others and from mine: vary the format (written, spoken, hands-on, visual), the context and the level of challenge.',
      noRank: 'Do not rank them or choose one for me.',
      label: 'Your own ideas',
      note: 'Two or three is enough.'
    },
    team: {
      intro: 'We are a team of teachers who teach {subject} to Grade {grade}.',
      ideasHead: 'Our ideas so far:',
      ask: 'Give us eight ideas for an activity that reaches this goal, each clearly different from the others and from all of ours: vary the format (written, spoken, hands-on, visual), the context and the level of challenge.',
      noRank: 'Do not rank them or choose one for us.',
      label: 'Your team\'s ideas',
      note: 'Everyone\'s ideas, one per line.'
    }
  };
  var FORMAT = 'Reply in plain text, no tables, as a numbered list of eight ideas, one or two sentences each. Start each idea with its format in parentheses, for example (hands-on). ';

  /* Trimmar ett textvärde; saknat värde blir tom sträng. */
  function clean(value) {
    return String(value == null ? '' : value).trim();
  }

  /* Byter ut {namn} i en fast textrad. Funktionen som ersättare gör att
     $&, $1 och liknande i lärarens text aldrig tolkas av replace. */
  function fill(line, values) {
    return line.replace(/\{(\w+)\}/g, function (m, key) {
      return Object.prototype.hasOwnProperty.call(values, key) ? values[key] : m;
    });
  }

  /* Delar lärarens egna idéer i rader: radbrytning med eller utan \r, trimma,
     ta bort ett inledande listtecken ("-", "•", "*", "1." eller "2)") och
     släng tomma rader. */
  function ideaLines(own) {
    return String(own == null ? '' : own).split(/\r?\n/)
      .map(function (line) { return line.trim().replace(/^(?:[-•*]|\d+[.)])\s*/, ''); })
      .filter(function (line) { return line !== ''; });
  }

  /* Bygger prompten. Ren funktion: samma indata ger alltid samma text.
     input = { who: "me" | "team", subject, grade, goal, own, fit, language }. */
  function buildIdeasPrompt(input) {
    var mode = MODES[input.who === 'team' ? 'team' : 'me'];
    var language = clean(input.language);
    var english = language === '' || language.toLowerCase() === 'english';
    var fit = clean(input.fit);

    var lines = [
      PRIVACY,
      '',
      fill(mode.intro, { subject: clean(input.subject), grade: clean(input.grade) }) +
        ' The goal of the lesson is: ' + clean(input.goal)
    ];
    // Passar-raden finns bara när något är skrivet, och ingen tom rad lämnas kvar.
    if (fit) lines.push('The ideas must fit this: ' + fit);
    lines.push('', mode.ideasHead);
    ideaLines(input.own).forEach(function (idea) { lines.push('- ' + idea); });
    lines.push(
      '',
      mode.ask,
      '',
      english ? 'Write everything in English.' : 'Write everything in ' + language + '.',
      '',
      FORMAT + mode.noRank
    );
    return lines.join('\n');
  }

  window.IdeasFirst = { buildIdeasPrompt: buildIdeasPrompt, ideaLines: ideaLines };

  document.addEventListener('DOMContentLoaded', function () {
    var byId = function (id) { return document.getElementById(id); };
    var els = {
      who: byId('if-who'), subject: byId('if-subject'), grade: byId('if-grade'),
      goal: byId('if-goal'), own: byId('if-own'), fit: byId('if-fit'),
      language: byId('if-language'),
      label: byId('if-own-label'), note: byId('if-own-note'),
      prompt: byId('if-prompt'), copy: byId('if-copy'), hint: byId('if-hint')
    };

    function update() {
      // Läget byter bara etikett och notering, aldrig textrutans innehåll.
      var mode = MODES[els.who.value === 'team' ? 'team' : 'me'];
      els.label.textContent = mode.label;
      els.note.textContent = mode.note;

      var ready = clean(els.subject.value) && clean(els.goal.value) &&
        ideaLines(els.own.value).length >= 1;
      var text = ready ? buildIdeasPrompt({
        who: els.who.value, subject: els.subject.value, grade: els.grade.value,
        goal: els.goal.value, own: els.own.value, fit: els.fit.value,
        language: els.language.value
      }) : '';

      els.prompt.value = text;
      els.copy.disabled = text === '';
      els.copy.setAttribute('data-copy', text);
      els.hint.textContent = text === '' ? HINT : '';
      els.hint.hidden = text !== '';
    }

    // Textfält ger "input", väljare ger "change"; båda lyssnas på.
    ['who', 'subject', 'grade', 'goal', 'own', 'fit', 'language'].forEach(function (k) {
      els[k].addEventListener('input', update);
      els[k].addEventListener('change', update);
    });
    update();
  });
})();
