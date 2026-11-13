/*
  Study Experiment — promptbyggaren på /study-experiment/.

  Läraren fyller i ämne, årskurs, område och språk, och prompten byggs medan
  man skriver. Prompten ber en AI skriva två texter och ett quiz med tolv
  frågor till experimentet. Allt sker i webbläsaren: inget sparas och inget
  skickas någonstans, och ingen datafil hämtas, eftersom prompten är fast
  text med fyra luckor. Användarens text sätts bara som .value och attribut,
  aldrig som HTML.

  Själva kopieringen sköts av copy-to-clipboard.js, som läser data-copy på
  knappen — därför hålls data-copy alltid lika med prompten.

  Filen har två delar: promptbyggaren (här) och, längre ner, kopplingen till
  formuläret. Resultatvyn får egna delar i samma fil.
*/
(function () {
  'use strict';

  var HINT_EMPTY = 'Fill in subject and topic area to see your prompt.';
  /* Språket på texterna och quizet när fältet lämnas tomt. */
  var DEFAULT_LANGUAGE = 'English';

  /* ---------- Promptbyggaren ---------- */

  /* Lärarens prompt, rad för rad. Texten är fastställd ordagrant i specen
     (avsnittet Prompt builder). Ändra den bara tillsammans med PDF:ens
     luckprompt (exports/build-study-experiment-pdf.py) och testerna.
     Luckorna är årskurs (två gånger), ämne, område och språk. */
  function teacherLines(input, language) {
    return [
      'Do not include student names or student work in this conversation.',
      '',
      'You are helping a Grade ' + input.grade + ' ' + input.subject +
        ' teacher run a classroom experiment on two study methods. Students will study two short texts: one by reading it twice, the other by reading it once, writing down everything they remember and then checking it against the text. A week later they take a surprise quiz on both texts.',
      '',
      'Topic area: ' + input.topic,
      'Write everything in ' + language + '.',
      '',
      'Write two texts, TEXT A and TEXT B, each on a different part of this topic area that students have not been taught yet.',
      '- Make each text about 250 words, and keep the two texts within 20 words of each other in length.',
      '- Make them equally hard: ten key facts each, similar sentence length and similar words, at a reading level for Grade ' + input.grade + '.',
      '- Spread the key facts evenly through each text. No headings or lists inside the texts.',
      '- Use only facts that are well established and easy to check.',
      '',
      'Then write a quiz: Q1 to Q6 on Text A and Q7 to Q12 on Text B.',
      '- Each question tests a different key point of the text, the kind of thing a student would write down when recalling it. The answer is a word, a number or a short phrase from the text.',
      '- Ask about what this text says, so that a student who has not read it cannot answer from general knowledge. Do not ask what a word means.',
      '- Spread the questions over the whole text, and do not give away one answer in another question.',
      '',
      'Reply in plain text, no tables, with exactly these five parts:',
      'TEXT A: a short title, then the text.',
      'TEXT B: a short title, then the text.',
      'QUIZ: the twelve questions, numbered Q1: to Q12:, ready to print.',
      'ANSWERS: the answers, numbered Q1: to Q12: to match, with other answers that should also count as right.',
      'CHECK: every fact, figure, date or name in the texts that the teacher should verify, one per line.'
    ];
  }

  /* Bygger prompten. Ren funktion: samma indata ger alltid samma text.
     input = { subject, grade, topic, language }. Ett tomt språk blir engelska. */
  function buildPrompt(input) {
    var language = String(input.language || '').trim() || DEFAULT_LANGUAGE;
    return teacherLines(input, language).join('\n');
  }

  /* Det som andra delar av sidan (och testerna) kan använda. Fler funktioner
     läggs till här i objektet. */
  window.StudyExperiment = { buildPrompt: buildPrompt };

  /* ---------- Formuläret med promptbyggaren ---------- */

  var els = {};

  function value(id) { return els[id].value.trim(); }

  /* Fyller i prompten och knappen. Saknas ämne eller område byggs ingen
     prompt: rutan töms, knappen blir grå och ledtråden visas bredvid den. */
  function update() {
    var subject = value('subject');
    var topic = value('topic');
    if (!subject || !topic) {
      els.prompt.value = '';
      els.copy.disabled = true;
      els.copy.setAttribute('data-copy', '');
      els.hint.textContent = HINT_EMPTY;
      return;
    }
    var text = buildPrompt({
      subject: subject, grade: els.grade.value, topic: topic, language: value('language')
    });
    els.prompt.value = text;
    els.copy.disabled = false;
    els.copy.setAttribute('data-copy', text);
    els.hint.textContent = '';
  }

  function initBuilder() {
    ['subject', 'grade', 'topic', 'language', 'prompt', 'copy', 'hint'].forEach(function (id) {
      els[id] = document.getElementById('se-' + id);
    });
    ['subject', 'grade', 'topic', 'language'].forEach(function (id) {
      els[id].addEventListener('input', update);
      els[id].addEventListener('change', update);
    });
    update();
  }

  document.addEventListener('DOMContentLoaded', function () {
    initBuilder();
  });
})();
