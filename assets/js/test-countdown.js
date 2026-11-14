/*
  Test Countdown — planeraren på /test-countdown/.

  Eleven anger provdagen och vad provet täcker, och planen byggs av en handfull
  rena funktioner: samma indata ger alltid samma plan. Allt sker i webbläsaren:
  inget sparas och inget skickas någonstans. Planen lever i adressen (?test=…),
  så en bokmärkt länk är hela "sparfilen".

  Datum är texter på formen YYYY-MM-DD och räknas bara med Date.UTC och
  getUTC…: då kan ingen sommartid i någon tidszon flytta en dag. Veckodagar och
  månader kommer från fasta engelska listor, aldrig från webbläsarens språk.
  Det enda som använder lokal tid är "idag" i formuläret.

  Filen har fyra delar: datumfunktionerna, planreglerna med texterna, länken
  (adressfältet) och lärarens quizprompt. Alla funktioner exporteras först på
  window.TestCountdown; sist kommer kopplingen till sidan.

  Reglerna är fastställda i specen (avsnittet The planner). Tidsfönstret på 21
  dagar, övningsprovet två dagar före och passens längd är konventioner, inte
  forskningsfynd, och sidan presenterar dem aldrig som fynd.
*/
(function () {
  'use strict';

  var MS_PER_DAY = 24 * 60 * 60 * 1000;
  /* Planen ser högst så här många dagar framåt från provet. */
  var LOOKAHEAD_DAYS = 21;
  var MAX_AREAS = 6;
  var MAX_AREA_LENGTH = 60;
  /* Längsta passet på sista kvällen. */
  var LAST_EVENING_MINUTES = 15;
  /* Byggpassen blir aldrig fler än så här; med övningsprovet och sista kvällen
     blir planen högst nio pass. */
  var MAX_BUILD_SESSIONS = 7;
  var MINUTE_CHOICES = ['15', '20', '30', '45'];

  var WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  var MSG_NO_TEST = 'Pick your test date to see your plan.';
  var MSG_NO_AREA = 'Type at least one area the test covers.';
  var MSG_TOO_MANY = 'Use at most six areas. Combine some, for example by chapter.';
  var MSG_NO_START = 'Pick a start date.';
  var MSG_NOT_AFTER = 'The test date must be after the start date.';
  var MSG_NO_DAY = 'Tick at least one day you can study.';
  var MSG_NO_STUDY_DAY = 'There are no study days before the test. Tick more days or start earlier.';

  /* ---------- Datum ---------- */

  /* Gör om YYYY-MM-DD till millisekunder i UTC (midnatt det dygnet). Ger null om
     texten inte är ett riktigt datum: 2026-02-30 och 2026-1-5 är båda ogiltiga.
     Kontrollen går i en rundtur: ett datum som Date.UTC "rättar" till nästa
     månad kommer inte tillbaka som samma år, månad och dag. */
  function parseDate(iso) {
    var match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(iso));
    if (!match) { return null; }
    var year = Number(match[1]);
    var month = Number(match[2]);
    var day = Number(match[3]);
    var ms = Date.UTC(year, month - 1, day);
    var back = new Date(ms);
    if (back.getUTCFullYear() !== year || back.getUTCMonth() !== month - 1 || back.getUTCDate() !== day) {
      return null;
    }
    return ms;
  }

  function pad2(number) {
    return (number < 10 ? '0' : '') + number;
  }

  /* Det omvända: millisekunder i UTC till YYYY-MM-DD. */
  function toIso(ms) {
    var d = new Date(ms);
    return d.getUTCFullYear() + '-' + pad2(d.getUTCMonth() + 1) + '-' + pad2(d.getUTCDate());
  }

  /* ISO-veckodag: 1 = måndag … 7 = söndag (getUTCDay ger 0 för söndag). */
  function isoWeekday(ms) {
    return new Date(ms).getUTCDay() || 7;
  }

  /* "2026-11-09" blir "Mon 9 Nov". Fasta engelska namn, aldrig webbläsarens språk. */
  function formatDate(iso) {
    var d = new Date(parseDate(iso));
    return WEEKDAYS[d.getUTCDay()] + ' ' + d.getUTCDate() + ' ' + MONTHS[d.getUTCMonth()];
  }

  /* ["A"] blir "A", ["A", "B"] blir "A and B", ["A", "B", "C"] blir "A, B and C". */
  function joinList(items) {
    if (items.length <= 1) { return items.join(''); }
    return items.slice(0, -1).join(', ') + ' and ' + items[items.length - 1];
  }

  /* ---------- Områden ---------- */

  /* Textrutan: ett område per rad. Raderna trimmas, tomma rader hoppas över och
     varje område kapas vid 60 tecken. Efter kapningen trimmas området igen, så
     att ett område som klipps mitt i ett mellanrum inte slutar på ett mellanslag.
     Antalet begränsas inte här; det är buildPlan som säger ifrån vid fler än sex. */
  function parseAreas(text) {
    var areas = [];
    String(text).split('\n').forEach(function (line) {
      var area = line.trim();
      if (area) { areas.push(area.slice(0, MAX_AREA_LENGTH).trim()); }
    });
    return areas;
  }

  /* ---------- Planreglerna ---------- */

  function fail(error) {
    return { ok: false, error: error };
  }

  /* Ett pass i planen. För "new" är areas den nya gruppen och earlier alla
     tidigare områden; för övriga slag är areas alla områden och earlier tom. */
  function makeSession(ms, kind, areas, earlier, minutes) {
    return { date: toIso(ms), kind: kind, areas: areas, earlier: earlier, minutes: minutes };
  }

  /* Vilka dagar (index i L) som byggpassen läggs på: b stycken jämnt utspridda
     bland de m byggdagarna. Första passet ligger alltid på första lediga dagen,
     och b = 1 ger bara index 0. */
  function buildDayIndexes(m, b) {
    var indexes = [];
    for (var i = 0; i < b; i++) {
      /* Math.round avrundar halvor uppåt (1,5 blir 2): lika långt mellan två dagar tar den senare. */
      indexes.push(b === 1 ? 0 : Math.round(i * (m - 1) / (b - 1)));
    }
    return indexes;
  }

  /* Delar områdena i ordning på b grupper så jämnt som möjligt; tidigare
     grupper tar det som blir över. Används när områdena är fler än byggpassen. */
  function splitAreas(areas, b) {
    var groups = [];
    var size = Math.floor(areas.length / b);
    var extra = areas.length % b;
    var at = 0;
    for (var g = 0; g < b; g++) {
      var take = size + (g < extra ? 1 : 0);
      groups.push(areas.slice(at, at + take));
      at += take;
    }
    return groups;
  }

  /* Byggpassen (alla utom övningsprovet och sista kvällen). dayIndexes pekar ut
     vilka lediga dagar de läggs på. Är passen minst lika många som områdena
     tar varje pass ett nytt område och de som blir över är blandade repetitioner.
     Är de färre delar områdena upp sig på passen. */
  function buildSessions(L, dayIndexes, areas, minutes) {
    var b = dayIndexes.length;
    var n = areas.length;
    var sessions = [];
    var groups;
    var i;
    if (b >= n) {
      for (i = 0; i < b; i++) {
        if (i < n) {
          sessions.push(makeSession(L[dayIndexes[i]], 'new', [areas[i]], areas.slice(0, i), minutes));
        } else {
          sessions.push(makeSession(L[dayIndexes[i]], 'mixed', areas.slice(), [], minutes));
        }
      }
      return sessions;
    }
    groups = splitAreas(areas, b);
    var seen = 0;
    for (i = 0; i < b; i++) {
      sessions.push(makeSession(L[dayIndexes[i]], 'new', groups[i], areas.slice(0, seen), minutes));
      seen += groups[i].length;
    }
    return sessions;
  }

  /* Bygger planen. Ren funktion.
     input = { test, start, areas, minutes, days } där days är ISO-veckodagar
     (1 = måndag … 7 = söndag) och areas redan går genom parseAreas.
     Ger { ok: true, test, areas, sessions, short, capped } eller
     { ok: false, error } med meddelandet som sidan visar i stället för en plan.
     Felen kommer i fast ordning: provdag, område, för många områden, startdag,
     provdag efter start, ingen vald dag, ingen ledig dag. */
  function buildPlan(input) {
    var test = parseDate(input.test);
    if (test === null) { return fail(MSG_NO_TEST); }
    var areas = input.areas || [];
    if (areas.length === 0) { return fail(MSG_NO_AREA); }
    if (areas.length > MAX_AREAS) { return fail(MSG_TOO_MANY); }
    var start = parseDate(input.start);
    if (start === null) { return fail(MSG_NO_START); }
    if (test <= start) { return fail(MSG_NOT_AFTER); }
    /* Dagarna kan komma som texter ("1") ur ett formulär: gör om dem till tal
       så att de går att jämföra med isoWeekday. */
    var days = (input.days || []).map(Number);
    if (days.length === 0) { return fail(MSG_NO_DAY); }

    /* Fönstret: från startdagen, dock högst 21 dagar före provet, till och med
       dagen före provet. Är starten längre bort än så visas noten om kapning. */
    var lookahead = LOOKAHEAD_DAYS * MS_PER_DAY;
    var capped = test - start > lookahead;
    var L = [];
    for (var ms = Math.max(start, test - lookahead); ms < test; ms += MS_PER_DAY) {
      if (days.indexOf(isoWeekday(ms)) !== -1) { L.push(ms); }
    }
    var k = L.length;
    if (k === 0) { return fail(MSG_NO_STUDY_DAY); }

    var n = areas.length;
    /* Minuterna kan också vara en text ("20"): som tal läggs de ihop rätt i planTotal. */
    var minutes = Number(input.minutes);
    var lastMinutes = Math.min(minutes, LAST_EVENING_MINUTES);
    var sessions;

    if (k === 1) {
      /* En enda dag: de viktigaste idéerna i alla områden. */
      sessions = [makeSession(L[0], 'single', areas.slice(), [], minutes)];
    } else if (k === 2) {
      /* Två dagar: ett kärnquiz på alla områden och sedan sista kvällen. */
      sessions = [
        makeSession(L[0], 'new', areas.slice(), [], minutes),
        makeSession(L[1], 'last', areas.slice(), [], lastMinutes)
      ];
    } else {
      /* Tre dagar eller fler: sista kvällen på L[k-1], övningsprovet på L[k-2]
         och byggdagarna L[0..k-3] däremellan. */
      var m = k - 2;
      var b = Math.min(m, MAX_BUILD_SESSIONS, Math.max(n + 1, Math.ceil(m / 2)));
      sessions = buildSessions(L, buildDayIndexes(m, b), areas, minutes);
      sessions.push(makeSession(L[k - 2], 'practice', areas.slice(), [], minutes));
      sessions.push(makeSession(L[k - 1], 'last', areas.slice(), [], lastMinutes));
    }

    return {
      ok: true,
      test: toIso(test),
      areas: areas.slice(),
      sessions: sessions,
      /* Kort om tid: högst tre dagar, eller så få byggdagar att områdena måste dela pass. */
      short: k <= 3 || k - 2 < n,
      capped: capped
    };
  }

  /* ---------- Texterna ---------- */

  /* Raden för ett pass: { label, text }. Texterna är fastställda ordagrant i
     specen. Områdena sätts in som ren text; sidan sätter dem med textContent.
     Planen behövs för tre saker: kort plan ger "the most important ideas",
     ett enda område ger andra formuleringar, och sista kvällen säger olika
     saker beroende på om planen har ett övningsprov. */
  function sessionText(session, plan) {
    var single = plan.areas.length === 1;
    var hasPractice = plan.sessions.some(function (s) { return s.kind === 'practice'; });
    switch (session.kind) {
      case 'new':
        var what = 'Quiz yourself on ' + (plan.short ? 'the most important ideas in ' : '') + joinList(session.areas);
        if (session.earlier.length > 0) {
          what += ', then a few questions on ' + joinList(session.earlier);
        }
        return {
          label: 'Quiz',
          text: what + '. Then check your notes and try the ones you missed again until you get them right.'
        };
      case 'mixed':
        if (single) {
          return {
            label: 'Quiz again',
            text: 'Quiz yourself on ' + session.areas[0] + ' again, starting with what you missed last time. Then explain one idea out loud without your notes.'
          };
        }
        return {
          label: 'Mixed quiz',
          text: 'Mixed quiz on all areas, starting with what you missed last time. Then explain one idea out loud without your notes.'
        };
      case 'practice':
        return {
          label: 'Practice test',
          text: 'Practice test on ' + (single ? plan.areas[0] : 'all areas') + ': no notes, timed, in the same format as the real test. Then check your answers and try the ones you got wrong again.'
        };
      case 'last':
        if (hasPractice) {
          return {
            label: 'Last evening',
            text: 'Only what you got wrong on the practice test. Keep it short, then get a good night\'s sleep.'
          };
        }
        return {
          label: 'Last evening',
          text: 'Quiz yourself again on what you missed, then one quick round of the most important ideas. Keep it short, then get a good night\'s sleep.'
        };
      case 'single':
        /* Den enda studiedagen före provet. */
        return {
          label: 'Quiz',
          text: 'Quiz yourself on the most important ideas in ' + joinList(session.areas) + '. Check your notes, try the ones you missed again, and finish in time for your normal bedtime.'
        };
    }
  }

  /* Den sista raden i planen, på provdagen. Inga minuter. */
  function testRow() {
    return { label: 'Test', text: 'Test day. You have practised for it.' };
  }

  /* Rubriken över planen: "Your plan: 6 sessions before the test on Fri 20 Nov". */
  function planTitle(plan) {
    var count = plan.sessions.length;
    return 'Your plan: ' + count + (count === 1 ? ' session' : ' sessions') +
      ' before the test on ' + formatDate(plan.test);
  }

  /* Raden under rubriken: summan av passens minuter och spännvidden i dagar,
     räknad från första passet till provdagen. Ett enda pass har ingen spännvidd. */
  function planTotal(plan) {
    var total = 0;
    plan.sessions.forEach(function (s) { total += s.minutes; });
    if (plan.sessions.length === 1) { return total + ' minutes in all.'; }
    var span = Math.round((parseDate(plan.test) - parseDate(plan.sessions[0].date)) / MS_PER_DAY);
    return total + ' minutes in all, spread over ' + span + ' days.';
  }

  /* ---------- Länken (adressfältet) ---------- */

  /* Planens indata som en adress-sträng, utan inledande "?":
     test=…&start=…&min=…&days=…&area=…&area=…  (i just den ordningen).
     days skrivs som sorterade siffror, till exempel 12345. URLSearchParams
     sköter kodningen av mellanslag, &, = och icke-ASCII-tecken. */
  function toQuery(input) {
    var params = new URLSearchParams();
    params.append('test', input.test);
    params.append('start', input.start);
    params.append('min', input.minutes);
    params.append('days', input.days.slice().sort(function (a, b) { return a - b; }).join(''));
    input.areas.forEach(function (area) { params.append('area', area); });
    return params.toString();
  }

  /* Läser en adress (med eller utan "?"). Ger bara de delar som är giltiga:
     riktiga datum, min 15/20/30/45, days som en icke-tom text av siffror 1–7
     (dubbletter slås ihop) och högst sex områden genom samma regler som
     textrutan. Allt annat hoppas över så att formulärets standardvärde står
     kvar, och inget kastar fel på en gammal eller handredigerad länk. */
  function fromQuery(search) {
    var params = new URLSearchParams(search);
    var result = {};

    ['test', 'start'].forEach(function (key) {
      var value = params.get(key);
      if (value !== null && parseDate(value) !== null) { result[key] = value; }
    });

    var minutes = params.get('min');
    if (minutes !== null && MINUTE_CHOICES.indexOf(minutes) !== -1) {
      result.minutes = Number(minutes);
    }

    var days = params.get('days');
    if (days !== null && /^[1-7]+$/.test(days)) {
      var chosen = [];
      for (var d = 1; d <= 7; d++) {
        if (days.indexOf(String(d)) !== -1) { chosen.push(d); }
      }
      result.days = chosen;
    }

    var areas = parseAreas(params.getAll('area').join('\n')).slice(0, MAX_AREAS);
    if (areas.length > 0) { result.areas = areas; }

    return result;
  }

  /* ---------- Lärarens quizprompt ---------- */

  var BUILDER_HINT = 'Make a plan above, then fill in your subject.';

  /* Det som står efter "Session {i}: " för ett pass, utan slutpunkten (den sätter
     buildPrompt dit). Texterna är fastställda ordagrant i specen (avsnittet Quiz
     prompt). Antalet frågor och formuleringen följer passets slag; kort plan och
     ett enda område ger andra ord, precis som i sessionText. */
  function quizLine(session, plan) {
    var single = plan.areas.length === 1;
    var line;
    switch (session.kind) {
      case 'new':
        line = 'five questions on ' + (plan.short ? 'the most important ideas in ' : '') + joinList(session.areas);
        if (session.earlier.length > 0) { line += ', and three on ' + joinList(session.earlier); }
        return line;
      case 'mixed':
        return single ? 'eight new questions on ' + session.areas[0] : 'eight questions mixing all areas';
      case 'practice':
        return 'a practice test of twelve questions on ' + (single ? plan.areas[0] : 'all areas') +
          ', in the same format as the real test';
      case 'single':
        return 'ten questions on the most important ideas in ' + joinList(session.areas);
    }
  }

  /* Bygger lärarens prompt. Ren funktion: samma plan och indata ger alltid samma
     text. options = { subject, grade, language }. Ämnet och språket trimmas, och
     ett tomt språk blir engelska. Passen numreras utan sista kvällen, som inte
     får något quiz; meningen om sista passet kommer bara när planen har en sista
     kväll, och den säger olika saker med och utan övningsprov. */
  function buildPrompt(plan, options) {
    var subject = String(options.subject).trim();
    var language = String(options.language).trim() || 'English';
    var areasSentence = plan.areas.length === 1
      ? 'The class has a test on ' + plan.areas[0] + '.'
      : 'The class has a test on these areas: ' + plan.areas.join('; ') + '.';
    var lines = [
      'Do not include student names or student work in this conversation.',
      '',
      'You are helping a Grade ' + options.grade + ' ' + subject + ' teacher. ' + areasSentence +
        ' Students will prepare with short study sessions on different days. Each session starts with a quiz that students answer on paper with their notes closed, and then check against the answers.',
      '',
      'Write everything in ' + language + '.',
      '',
      'Write one quiz for each of these sessions:'
    ];
    var number = 0;
    var hasPractice = false;
    var hasLast = false;
    plan.sessions.forEach(function (session) {
      if (session.kind === 'last') {
        hasLast = true;
        return;
      }
      if (session.kind === 'practice') { hasPractice = true; }
      number += 1;
      lines.push('Session ' + number + ': ' + quizLine(session, plan) + '.');
    });
    if (hasLast) {
      lines.push(hasPractice
        ? 'The last session works on the mistakes from the practice test, so it needs no quiz.'
        : 'The last session goes back over the first quiz, so it needs no quiz of its own.');
    }
    lines.push(
      '',
      '- Ask about the most important content in each area: what the test is most likely to ask. If I paste my own teaching material or an old test after this prompt, base the questions on that material and make the practice test look like the old test.',
      '- Each question asks one thing. Most answers are a word, a number or a short phrase; add a few "explain why" questions.',
      '- When a session comes back to an earlier area, ask in a new way, not the same question again.',
      '- Do not give away one answer in another question.',
      '',
      'Reply in plain text, no tables. For each session, write SESSION 1:, SESSION 2: and so on, with the questions numbered Q1:, Q2: and so on, ready to print. Then write ANSWERS, with the answers for each session numbered to match. End with CHECK: every fact, figure, date or name in the answers that I should verify, one per line.'
    );
    return lines.join('\n');
  }

  window.TestCountdown = {
    parseAreas: parseAreas,
    buildPlan: buildPlan,
    sessionText: sessionText,
    testRow: testRow,
    formatDate: formatDate,
    joinList: joinList,
    planTitle: planTitle,
    planTotal: planTotal,
    toQuery: toQuery,
    fromQuery: fromQuery,
    buildPrompt: buildPrompt
  };

  /* ---------- Kopplingen till sidan ---------- */

  /* Dagens datum som YYYY-MM-DD, i webbläsarens lokala tid. Det är det enda
     stället som använder lokal tid: ett datum "idag" är den dag eleven ser på
     sin klocka, inte den dag det är i UTC. */
  function todayLocal() {
    var now = new Date();
    return now.getFullYear() + '-' + pad2(now.getMonth() + 1) + '-' + pad2(now.getDate());
  }

  /* Ett element med klass och text. Texten sätts alltid med textContent, så
     inget som eleven skrivit kan bli HTML. */
  function make(tag, className, text) {
    var node = document.createElement(tag);
    if (className) { node.className = className; }
    if (text !== undefined) { node.textContent = text; }
    return node;
  }

  /* En rad i planen: datum, etikett och text, och sist minuterna (utom på
     provdagen, som skickar null). Markuppen följer test-countdown.css. */
  function makeRow(kind, date, label, text, minutes) {
    var row = make('li', 'tc-row tc-row--' + kind);
    row.appendChild(make('span', 'tc-row__date', formatDate(date)));
    var main = make('div', 'tc-row__main');
    main.appendChild(make('span', 'tc-row__label', label));
    main.appendChild(make('p', 'tc-row__text', text));
    row.appendChild(main);
    if (minutes !== null) { row.appendChild(make('span', 'tc-row__minutes', minutes + ' min')); }
    return row;
  }

  /* Sidans formulär kopplas här. Finns inget #tc-form (filen läses in på en
     annan sida) görs ingenting alls. */
  function init() {
    var form = document.getElementById('tc-form');
    if (!form) { return; }

    var els = {
      test: document.getElementById('tc-test'),
      start: document.getElementById('tc-start'),
      minutes: document.getElementById('tc-minutes'),
      areas: document.getElementById('tc-areas'),
      days: form.querySelectorAll('#tc-days input[name="day"]'),
      hint: document.getElementById('tc-hint'),
      plan: document.getElementById('tc-plan'),
      title: document.getElementById('tc-plan-title'),
      total: document.getElementById('tc-plan-total'),
      list: document.getElementById('tc-plan-list'),
      short: document.getElementById('tc-short'),
      capped: document.getElementById('tc-capped'),
      link: document.getElementById('tc-link'),
      print: document.getElementById('tc-print')
    };

    /* Adressen skrivs bara om när eleven har ändrat något eller när sidan
       öppnades med en länk som hade minst en giltig del. En vanlig sidladdning
       och en adress med bara andra parametrar (till exempel ?utm_source=mail)
       lämnas orörda tills eleven ändrar något. */
    var saved = fromQuery(location.search);
    var opened = Object.keys(saved).length > 0;
    var edited = false;

    /* Formuläret som indata till buildPlan och toQuery. Minuter och veckodagar
       är tal, inte de texter fälten innehåller. */
    function readState() {
      var days = [];
      Array.prototype.forEach.call(els.days, function (box) {
        if (box.checked) { days.push(Number(box.value)); }
      });
      return {
        test: els.test.value,
        start: els.start.value,
        minutes: Number(els.minutes.value),
        areas: parseAreas(els.areas.value),
        days: days
      };
    }

    /* Länken i adressen fyller i formuläret. Det som saknas eller är ogiltigt
       lämnas som det står i HTML:en (20 minuter, alla dagar ikryssade). */
    function fillForm(saved) {
      if (saved.test) { els.test.value = saved.test; }
      if (saved.start) { els.start.value = saved.start; }
      if (saved.minutes) { els.minutes.value = String(saved.minutes); }
      if (saved.areas) { els.areas.value = saved.areas.join('\n'); }
      if (saved.days) {
        Array.prototype.forEach.call(els.days, function (box) {
          box.checked = saved.days.indexOf(Number(box.value)) !== -1;
        });
      }
    }

    /* Rubrik, summering, noter och rader. Raderna byggs om varje gång. */
    function showPlan(plan) {
      els.title.textContent = planTitle(plan);
      els.total.textContent = planTotal(plan);
      els.short.hidden = !plan.short;
      els.capped.hidden = !plan.capped;
      var rows = document.createDocumentFragment();
      plan.sessions.forEach(function (session) {
        var shown = sessionText(session, plan);
        rows.appendChild(makeRow(session.kind, session.date, shown.label, shown.text, session.minutes));
      });
      var test = testRow();
      rows.appendChild(makeRow('test', plan.test, test.label, test.text, null));
      els.list.textContent = '';
      els.list.appendChild(rows);
    }

    /* Skriver formulärets läge i adressfältet utan att lägga till något i
       historiken. Misslyckas det (Safari tillåter bara ett hundratal ändringar
       på 30 sekunder, och snabb skrivning kan nå dit) ska planen ändå visas. */
    function updateAddress(input) {
      try {
        history.replaceState(null, '', location.pathname + '?' + toQuery(input) + location.hash);
      } catch (e) { /* adressen blir kvar som den var */ }
    }

    /* En omräkning: läs formuläret, bygg planen, visa den eller ledtråden,
       uppdatera adressen och länkknappen och berätta för andra delar av sidan
       (promptbyggaren lyssnar på tc:plan; detail är planen eller null). */
    function replan() {
      var input = readState();
      var plan = buildPlan(input);
      var message = plan.ok ? '' : plan.error;
      /* Ledtråden är aria-live: skrivs samma text om läser en skärmläsare upp
         den för varje tangenttryckning. Därför skrivs den bara när den ändras. */
      if (els.hint.textContent !== message) { els.hint.textContent = message; }
      els.plan.hidden = !plan.ok;
      if (plan.ok) { showPlan(plan); }
      if (edited || opened) { updateAddress(input); }
      els.link.setAttribute('data-copy', location.href);
      document.dispatchEvent(new CustomEvent('tc:plan', { detail: plan.ok ? plan : null }));
    }

    function onEdit() {
      edited = true;
      replan();
    }

    fillForm(saved);
    /* Tomt startdatum blir dagens datum. */
    if (!els.start.value) { els.start.value = todayLocal(); }
    form.addEventListener('input', onEdit);
    form.addEventListener('change', onEdit);
    els.print.addEventListener('click', function () { window.print(); });
    replan();
  }

  /* Promptbyggaren på sidan. Den lyssnar på tc:plan från planeraren och på
     sina egna fält. Senaste planen sparas i en variabel (null när det inte finns
     någon), och prompten byggs om från den varje gång något ändras. Det gör
     lyssnaren idempotent: planeraren kan skicka tc:plan två gånger per ändring
     (input och change), och samma plan igen ger exakt samma läge. */
  function initBuilder() {
    var form = document.getElementById('tc-builder-form');
    if (!form) { return; }

    var els = {
      subject: document.getElementById('tc-subject'),
      grade: document.getElementById('tc-grade'),
      language: document.getElementById('tc-language'),
      prompt: document.getElementById('tc-prompt'),
      copy: document.getElementById('tc-copy'),
      hint: document.getElementById('tc-prompt-hint')
    };
    var latestPlan = null;

    /* Klar = en plan och ett ämne. Då står prompten i rutan och i knappens
       data-copy, som copy-to-clipboard.js kopierar vid klick; annars är rutan
       tom, knappen grå och ledtråden säger vad som saknas. Ledtråden är
       aria-live och skrivs därför bara när texten ändras. */
    function refresh() {
      var subject = els.subject.value.trim();
      var text = '';
      if (latestPlan && subject) {
        text = buildPrompt(latestPlan, {
          subject: subject,
          grade: els.grade.value,
          language: els.language.value
        });
      }
      var message = text ? '' : BUILDER_HINT;
      els.prompt.value = text;
      els.copy.disabled = text === '';
      els.copy.setAttribute('data-copy', text);
      if (els.hint.textContent !== message) { els.hint.textContent = message; }
    }

    document.addEventListener('tc:plan', function (event) {
      latestPlan = event.detail || null;
      refresh();
    });
    form.addEventListener('input', refresh);
    form.addEventListener('change', refresh);
    refresh();
  }

  /* initBuilder registreras före init: planeraren skickar sin första tc:plan
     redan i init, och då måste promptbyggaren redan lyssna. Lyssnarna på
     DOMContentLoaded körs i den ordning de lades till. */
  document.addEventListener('DOMContentLoaded', initBuilder);
  document.addEventListener('DOMContentLoaded', init);
})();
