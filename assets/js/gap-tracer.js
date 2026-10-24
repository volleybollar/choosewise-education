/*
  Gap Tracer (/gap-tracer/).

  Everything runs in the visitor's browser. The page loads the skills and
  their prerequisites from gap-tracer/data/skills.json, and the practice
  activities for one skill at a time from gap-tracer/data/activities/<id>.json.
  The child's name is only used to fill the check questions: it is never
  stored and never sent anywhere.

  Text from the data is always written with textContent, never innerHTML,
  so a name like "<b>Sam</b>" shows as text.
*/
(function () {
  'use strict';

  const DATA = '/gap-tracer/data/';
  const NO_ACTIVITIES = 'No practice activities for this skill yet — activities currently exist only in Mathematics and Science.';
  const FETCH_FAILED = "Couldn't load the practice activities — check your connection and try again.";
  const ANSWERS = [['yes', 'Yes, secure'], ['unsure', 'Not sure'], ['no', 'No']];
  const MAX_RESULTS = 20;

  const skillsById = new Map();
  // answers: id → "yes" | "unsure" | "no". expanded: ids whose earlier layer is open.
  const state = { targetId: null, answers: new Map(), expanded: new Set() };
  const activityCache = new Map();  // id → Promise of the activity list

  const $ = (sel) => document.querySelector(sel);

  // Small helper: create an element with a class and text.
  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  // Replace {{name}} with the child's name, or "the child" when no name is given.
  function fillName(check, name) {
    const n = (name || '').trim();
    return check.replace(/\{\{name\}\}/g, (_, offset) => n || (offset === 0 ? 'The child' : 'the child'));
  }

  function currentName() {
    return $('#gt-name').value;
  }

  // Order the plan: depth-first from the target, so every prerequisite comes
  // before the skills that build on it. Shared prerequisites appear once.
  function orderPlan(targetId, gaps, skills) {
    const seen = new Set();
    const order = [];
    (function visit(id) {
      if (seen.has(id)) return;
      seen.add(id);
      const skill = skills.get(id);
      (skill ? skill.prereqs : []).forEach((p) => visit(p.id));
      order.push(id);
    })(targetId);
    return order.filter((id) => id !== targetId && gaps.has(id)).concat(targetId);
  }

  // Skills answered "Not sure" or "No" that are still on the path from the
  // target. A layer only counts while the skill above it is open and not
  // "Yes, secure": if halves are secure, what lies under halves isn't a gap.
  function gapIds() {
    const gaps = new Set();
    const target = skillsById.get(state.targetId);
    (function walk(edges) {
      edges.forEach(({ id }) => {
        const answer = state.answers.get(id);
        if (answer !== 'no' && answer !== 'unsure') return;
        if (gaps.has(id)) return;
        gaps.add(id);
        if (state.expanded.has(id)) walk(skillsById.get(id).prereqs);
      });
    })(target ? target.prereqs : []);
    return gaps;
  }

  // ───── Step 1: search ─────

  // Every word must appear in the name or a curriculum label. Name matches rank first.
  function search(query) {
    const words = query.trim().toLowerCase().split(/\s+/).filter(Boolean);
    if (!words.length) return [];
    const hits = [];
    skillsById.forEach((s) => {
      const name = s.name.toLowerCase();
      const all = name + ' ' + s.standards.join(' ').toLowerCase();
      if (words.every((w) => all.includes(w))) {
        hits.push({ s, rank: name.startsWith(words[0]) ? 0 : words.every((w) => name.includes(w)) ? 1 : 2 });
      }
    });
    hits.sort((a, b) => a.rank - b.rank || a.s.name.localeCompare(b.s.name));
    return hits.slice(0, MAX_RESULTS).map((h) => h.s);
  }

  function renderResults() {
    const query = $('#gt-search').value;
    const list = $('#gt-results');
    list.replaceChildren();
    if (!query.trim()) return;
    const hits = search(query);
    if (!hits.length) {
      list.append(el('li', 'gt-empty', `No skills match “${query.trim()}”. Try a shorter word or a curriculum code.`));
      return;
    }
    const q = query.trim().toLowerCase();
    hits.forEach((s) => {
      const button = el('button', 'gt-result');
      button.type = 'button';
      button.dataset.id = s.id;
      button.setAttribute('aria-pressed', String(s.id === state.targetId));
      button.append(el('span', 'gt-result__name', s.name));
      button.append(el('span', 'gt-result__meta', `${s.subject} · age ${s.ageStart}–${s.ageEnd}`));
      // Show the labels that match the search first, so a code search shows the code.
      const labels = [...s.standards].sort((a, b) => b.toLowerCase().includes(q) - a.toLowerCase().includes(q));
      if (labels.length) button.append(el('span', 'gt-result__standards', labels.slice(0, 4).join(' · ')));
      button.append(el('span', 'gt-badge' + (s.hasActivities ? ' gt-badge--yes' : ''),
        s.hasActivities ? 'Practice activities' : 'No practice activities yet'));
      button.addEventListener('click', () => selectTarget(s.id));
      const item = el('li');
      item.append(button);
      list.append(item);
    });
  }

  function selectTarget(id) {
    state.targetId = id;
    state.answers.clear();
    state.expanded.clear();
    document.querySelectorAll('.gt-result').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.id === id)));
    $('#gt-step-2').hidden = false;
    $('#gt-plan').hidden = false;
    renderCheck();
    renderPlan();
    // On a phone step 2 opens far below the results: take her there.
    $('#gt-step-2').scrollIntoView({ block: 'start' });
    $('#gt-step-2-title').focus({ preventScroll: true });
  }

  // ───── Step 2: the building blocks ─────

  function renderCheck() {
    const box = $('#gt-check');
    box.replaceChildren();
    const target = skillsById.get(state.targetId);
    box.append(el('p', 'section__lede', `Before “${target.name}”, the child needs these. Answer one quick question for each.`));
    if (!target.prereqs.length) {
      box.append(el('p', 'gt-empty', 'This skill has no earlier building blocks in the map.'));
      return;
    }
    box.append(blockList(target.prereqs));
  }

  function blockList(edges) {
    const list = el('ul', 'gt-check__list');
    edges.forEach((edge) => list.append(blockItem(edge)));
    return list;
  }

  // One building block: name, check question, evidence and the three answers.
  function blockItem(edge) {
    const skill = skillsById.get(edge.id);
    const item = el('li', 'gt-block');
    item.dataset.id = skill.id;

    const head = el('p');
    head.append(el('span', 'gt-block__name', skill.name));
    head.append(el('span', 'gt-block__strength', edge.strength === 'hard' ? 'Essential' : 'Helpful'));
    item.append(head);

    const question = el('p', 'gt-block__question', fillName(skill.check, currentName()));
    question.dataset.check = '';
    item.append(question);

    const details = el('details');
    details.append(el('summary', '', 'Signs it is secure'));
    const signs = el('ul');
    skill.evidence.forEach((e) => signs.append(el('li', '', e)));
    details.append(signs);
    item.append(details);

    const answers = el('div', 'gt-answers');
    ANSWERS.forEach(([value, label]) => {
      const b = el('button', 'btn btn--secondary gt-answer', label);
      b.type = 'button';
      b.dataset.answer = value;
      b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', () => setAnswer(skill.id, value));
      answers.append(b);
    });
    item.append(answers);

    // "Not sure" and "No" offer one more layer back — only when there is one.
    if (skill.prereqs.length) {
      const deeper = el('button', 'btn btn--ghost gt-deeper', 'Check what comes before');
      deeper.type = 'button';
      deeper.hidden = true;
      deeper.addEventListener('click', () => {
        deeper.remove();
        state.expanded.add(skill.id);
        const layer = blockList(skill.prereqs);
        item.append(layer);
        layer.querySelector('.gt-answer').focus();  // keep keyboard users in place
        renderPlan();
      });
      item.append(deeper);
    }
    syncBlock(item);
    return item;
  }

  // A skill can appear in several places. Its answer is stored once and shown everywhere.
  function syncBlock(item) {
    const answer = state.answers.get(item.dataset.id);
    item.querySelectorAll(':scope > .gt-answers .gt-answer').forEach((b) =>
      b.setAttribute('aria-pressed', String(b.dataset.answer === answer)));
    const deeper = item.querySelector(':scope > .gt-deeper');
    if (deeper) deeper.hidden = !(answer === 'no' || answer === 'unsure');
    // An open layer hides while the skill is "Yes, secure"; its answers are kept.
    const layer = item.querySelector(':scope > .gt-check__list');
    if (layer) layer.hidden = answer === 'yes';
  }

  function setAnswer(id, value) {
    state.answers.set(id, value);
    document.querySelectorAll(`.gt-block[data-id="${CSS.escape(id)}"]`).forEach(syncBlock);
    renderPlan();
  }

  function refreshQuestions() {
    document.querySelectorAll('.gt-block').forEach((item) => {
      item.querySelector(':scope > [data-check]').textContent =
        fillName(skillsById.get(item.dataset.id).check, currentName());
    });
  }

  // ───── Step 3: the plan ─────

  function loadActivities(id) {
    if (!activityCache.has(id)) {
      const request = fetch(`${DATA}activities/${id}.json`)
        .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then((d) => d.activities);
      request.catch(() => activityCache.delete(id));  // let a later render try again
      activityCache.set(id, request);
    }
    return activityCache.get(id);
  }

  function renderActivity(a) {
    const box = el('div', 'gt-activity');
    box.append(el('p', 'gt-activity__title', a.title));
    const steps = el('ul');
    a.learnerActions.forEach((s) => steps.append(el('li', '', s)));
    box.append(steps);
    const shows = el('p');
    shows.append(el('strong', '', 'What it shows: '), a.intendedInsight);
    box.append(shows);
    if (a.feedback.length) {
      const label = el('p');
      label.append(el('strong', '', 'If they…'));
      box.append(label);
      const tips = el('ul');
      a.feedback.forEach((f) => tips.append(el('li', '', f)));
      box.append(tips);
    }
    return box;
  }

  function renderPlan() {
    const list = $('#gt-plan-items');
    list.replaceChildren();
    orderPlan(state.targetId, gapIds(), skillsById).forEach((id) => {
      const skill = skillsById.get(id);
      const item = el('li', 'gt-plan__item');
      item.dataset.id = id;
      item.append(el('h3', '', skill.name));
      if (id === state.targetId) item.append(el('p', 'gt-plan__target', 'The skill the child was stuck on'));
      item.append(el('p', '', skill.description));
      item.append(el('h4', '', "You'll know it's working when:"));
      const signs = el('ul');
      skill.evidence.forEach((e) => signs.append(el('li', '', e)));
      item.append(signs);

      if (!skill.hasActivities) {
        item.append(el('p', 'gt-none', NO_ACTIVITIES));
      } else {
        item.append(el('h4', '', 'Try this:'));
        const box = el('div');
        item.append(box);
        loadActivities(id)
          .then((acts) => acts.slice(0, 2).forEach((a) => box.append(renderActivity(a))))
          .catch(() => {
            const error = el('p', 'gt-error', FETCH_FAILED + ' ');
            const retry = el('button', 'btn btn--secondary gt-retry', 'Try again');
            retry.type = 'button';
            retry.addEventListener('click', renderPlan);
            error.append(retry);
            box.append(error);
          });
      }
      list.append(item);
    });
  }

  // ───── Meta: counts and dates from meta.json, never typed by hand ─────

  function fillMeta(meta) {
    document.querySelectorAll('[data-meta]').forEach((node) => {
      const value = node.dataset.meta.split('.').reduce((o, k) => (o == null ? o : o[k]), meta);
      node.textContent = value == null ? '' : String(value);
    });
  }

  // ───── Feedback: yes or no, sent anonymously ─────

  // Same transport as ai-or-human.js. An empty data-telemetry-url means no
  // request at all. The child's name is never part of the payload.
  function postFeedback(answer) {
    const box = $('#gt-feedback');
    const url = box.dataset.telemetryUrl;
    if (url) {
      fetch(url, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'text/plain;charset=utf-8' },
        body: JSON.stringify({
          answer,
          skillId: state.targetId,
          gapCount: gapIds().size,
          timestamp: new Date().toISOString(),
        }),
      }).catch(() => { /* fire-and-forget */ });
    }
    box.querySelector('.gt-feedback__buttons').hidden = true;
    box.querySelector('.gt-feedback__thanks').hidden = false;
  }

  // ───── Start ─────

  function init() {
    fetch(`${DATA}meta.json`).then((r) => r.json()).then(fillMeta).catch(() => {});
    fetch(`${DATA}skills.json`)
      .then((r) => r.json())
      .then((d) => {
        d.skills.forEach((s) => skillsById.set(s.id, s));
        $('#gt-search').addEventListener('input', renderResults);
        renderResults();
      })
      .catch(() => $('#gt-results').append(el('li', 'gt-error', "Couldn't load the skills — check your connection and reload the page.")));
    $('#gt-name').addEventListener('input', refreshQuestions);
    $('#gt-print').addEventListener('click', () => window.print());
    document.querySelectorAll('#gt-feedback [data-feedback]').forEach((b) =>
      b.addEventListener('click', () => postFeedback(b.dataset.feedback)));
  }

  window.GapTracer = { fillName, orderPlan, gapIds, state, skillsById };
  init();
})();
