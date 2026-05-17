/* Evidence Toolkit — client-side behaviour.
 *
 * Responsibilities:
 *   1. Build the prompt-builder modal output for both per-card and free-text inputs.
 *   2. Open / close the modal and copy the prompt to clipboard.
 *   3. Filter, sort, and search the card grid (on /evidence/<domain>/ pages only).
 *   4. Render the tag-filter pills from the data file.
 *
 * Data: window.ET_DATA_URL points to the domain JSON file. On the hub page it is null
 * (no card grid, no per-skill modal), only the free-text prompt builder is active.
 */
(function () {
  "use strict";

  const PROMPT_TEMPLATE = (claim, source) => `// Context
You are a research-literate education advisor speaking with a working
teacher. Your job is to help them think critically, not to give them a
pre-baked answer.

// The claim being checked
"${claim}"${source ? `\nSource on the page: ${source}.` : ""}

// What I need you to do
1. Walk through the published research on this claim — what has actually
   been studied, by whom, and how rigorously the studies were designed.
2. Separate well-replicated findings from solid designs from one-off
   studies, underpowered samples, or contested results.
3. Name the conditions that weaken the evidence — narrow populations,
   short follow-ups, measurement quirks, missing replications.
4. Call out the gap between what the research actually shows and how the
   intervention is typically marketed, simplified, or oversold in CPD
   sessions, books, or social media.
5. Land on a practical takeaway a thoughtful teacher could defend in a
   staff meeting — neither a hype line nor a defensive hedge.
6. Cite specific, named meta-analyses or systematic reviews — by author,
   year, and journal. If you don't have a real citation, say so
   explicitly rather than inventing one.
7. Note any boundary conditions: subject, age group, country, school
   type, or context where the intervention works much better or much
   worse.
8. Distinguish the construct from the label — explain what the term
   actually means in the research vs. how it's used in popular
   discourse.
9. Flag publication bias, conflict-of-interest concerns, or vendor-funded
   research where relevant.
10. Suggest one or two stronger or comparable alternatives the teacher
    could also consider.
11. Discuss cost-effectiveness — both monetary (where data exists) and
    implementation cost (teacher time, training, structural change). Note
    where the intervention is most or least cost-effective.
12. End with a concrete picture of what this would look like in a real
    classroom next Monday — and what would NOT count as this intervention
    even if it's labelled that way.

// Output format
Use a structured response that is easy for a busy teacher to scan.
Specifically:

**Bottom line** (one sentence)
**Evidence strength** (with named sources)
**What the research actually supports**
**What it does NOT support**
**Boundary conditions**
**Common myths or exaggerations**
**Cost & implementation reality**
**On Monday in the classroom**
**Alternatives worth considering**
**Suggested follow-up reading**

// Tone
Plain professional English. Define jargon when first used. Speak to an
experienced teacher, not a researcher. If you are uncertain, say so.

// Reasoning
If you can use extended thinking or step-by-step reasoning mode for
this analysis, please do so. The questions above require careful
evaluation, not a fast first-pass answer.`;

  let SKILLS_BY_ID = {};
  let ALL_SKILLS = [];
  let LAST_FOCUS = null;

  // ----- Modal -----
  function openModal(promptText) {
    const modal = document.getElementById("et-modal");
    const out = document.getElementById("et-prompt-output");
    if (!modal || !out) return;
    LAST_FOCUS = document.activeElement;
    out.value = promptText;
    modal.classList.add("is-open");
    document.body.style.overflow = "hidden";
    // Move focus to the close button so screen readers and keyboard users land inside the dialog
    const closeBtn = modal.querySelector('[data-action="close-modal"]');
    if (closeBtn) closeBtn.focus();
  }

  function closeModal() {
    const modal = document.getElementById("et-modal");
    if (!modal) return;
    modal.classList.remove("is-open");
    document.body.style.overflow = "";
    if (LAST_FOCUS && typeof LAST_FOCUS.focus === "function") {
      LAST_FOCUS.focus();
      LAST_FOCUS = null;
    }
  }

  function buildPromptFromSkill(skill) {
    const months = skill.effect_months !== null ? `+${skill.effect_months} months progress` : null;
    const d = skill.effect_d !== null ? `d = ${skill.effect_d.toFixed(2)}` : null;
    const sizeBits = [months, d].filter(Boolean).join(" / ");
    const claim = sizeBits
      ? `${skill.display_title} has an evidence-based effect of ${sizeBits} on learning.`
      : `${skill.display_title} is an evidence-based teaching intervention with a meaningful effect on learning.`;
    const sourceBits = [];
    if (skill.effect_d_source) {
      const yr = skill.effect_d_year ? ` (${skill.effect_d_year})` : "";
      sourceBits.push(`${skill.effect_d_source}${yr}, ${skill.effect_d_journal || ""}`.trim().replace(/,\s*$/, ""));
    }
    if (skill.effect_months_source) {
      sourceBits.push(skill.effect_months_source);
    }
    return PROMPT_TEMPLATE(claim, sourceBits.join("; "));
  }

  function buildPromptFromClaim(claim) {
    return PROMPT_TEMPLATE(claim, null);
  }

  // ----- Copy to clipboard -----
  function copyPrompt() {
    const out = document.getElementById("et-prompt-output");
    if (!out) return;
    out.select();
    navigator.clipboard.writeText(out.value).then(function () {
      const fb = document.getElementById("et-copy-feedback");
      if (!fb) return;
      fb.classList.add("is-visible");
      setTimeout(() => fb.classList.remove("is-visible"), 1800);
    });
  }

  // ----- Card grid: filter, sort, search -----
  function getCards() {
    return Array.from(document.querySelectorAll("#et-card-grid .skill-card"));
  }

  function applyFilters() {
    const search = (document.getElementById("et-search")?.value || "").toLowerCase().trim();
    const activeTagBtn = document.querySelector("#et-tags .et-tag-pill.is-active");
    const activeTag = activeTagBtn?.dataset.tag || "all";

    let visible = 0;
    getCards().forEach(function (card) {
      const id = card.dataset.skillId;
      const skill = SKILLS_BY_ID[id];
      if (!skill) return;
      const haystack = [
        skill.display_title,
        skill.description,
        ...(skill.tags || []),
      ].join(" ").toLowerCase();
      const matchSearch = !search || haystack.includes(search);
      const matchTag = activeTag === "all" || (skill.tags || []).includes(activeTag);
      const show = matchSearch && matchTag;
      card.classList.toggle("is-hidden", !show);
      if (show) visible++;
    });
    const counter = document.getElementById("et-count");
    if (counter) counter.textContent = `${visible} interventions`;
  }

  function applySort() {
    const select = document.getElementById("et-sort");
    const grid = document.getElementById("et-card-grid");
    if (!select || !grid) return;
    const mode = select.value;

    function score(skill) {
      // Combined score: prefer months when present, otherwise d-derived months estimate
      if (skill.effect_months !== null && skill.effect_months !== undefined) return skill.effect_months;
      if (skill.effect_d !== null && skill.effect_d !== undefined) return skill.effect_d * 8; // rough d→months scale
      return -1;
    }

    const cards = getCards();
    cards.sort(function (a, b) {
      const sa = SKILLS_BY_ID[a.dataset.skillId];
      const sb = SKILLS_BY_ID[b.dataset.skillId];
      if (!sa || !sb) return 0;
      if (mode === "alpha") {
        return sa.display_title.localeCompare(sb.display_title);
      }
      const diff = score(sb) - score(sa);
      return mode === "effect-asc" ? -diff : diff;
    });
    cards.forEach(c => grid.appendChild(c));
  }

  function renderTagPills() {
    const container = document.getElementById("et-tags");
    if (!container) return;
    const tagSet = new Set();
    ALL_SKILLS.forEach(s => (s.tags || []).forEach(t => tagSet.add(t)));
    const tags = Array.from(tagSet).sort();

    const html = [`<button class="et-tag-pill is-active" data-tag="all" type="button">All</button>`]
      .concat(tags.map(t => `<button class="et-tag-pill" data-tag="${t}" type="button">${t}</button>`))
      .join("");
    container.innerHTML = html;

    container.addEventListener("click", function (e) {
      const btn = e.target.closest(".et-tag-pill");
      if (!btn) return;
      container.querySelectorAll(".et-tag-pill").forEach(b => b.classList.remove("is-active"));
      btn.classList.add("is-active");
      applyFilters();
    });
  }

  // ----- Bootstrap -----
  function bindGlobalEvents() {
    document.addEventListener("click", function (e) {
      // Per-card interrogate
      const interrogateBtn = e.target.closest('[data-action="interrogate"]');
      if (interrogateBtn) {
        const id = interrogateBtn.dataset.skillId;
        const skill = SKILLS_BY_ID[id];
        if (skill) openModal(buildPromptFromSkill(skill));
        return;
      }
      // Close
      if (e.target.closest('[data-action="close-modal"]')) {
        closeModal();
        return;
      }
      // Close on background click
      if (e.target.id === "et-modal") {
        closeModal();
      }
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeModal();
    });

    document.getElementById("et-copy")?.addEventListener("click", copyPrompt);

    document.getElementById("et-free-build")?.addEventListener("click", function () {
      const claim = (document.getElementById("et-free-claim")?.value || "").trim();
      const err = document.getElementById("et-free-error");
      if (!claim) {
        if (err) err.classList.add("is-visible");
        document.getElementById("et-free-claim")?.focus();
        return;
      }
      if (err) err.classList.remove("is-visible");
      openModal(buildPromptFromClaim(claim));
    });

    document.getElementById("et-free-claim")?.addEventListener("input", function () {
      document.getElementById("et-free-error")?.classList.remove("is-visible");
    });

    document.getElementById("et-search")?.addEventListener("input", applyFilters);
    document.getElementById("et-sort")?.addEventListener("change", function () {
      applySort();
      applyFilters();
    });
  }

  async function loadSkillData() {
    if (!window.ET_DATA_URL) return;
    try {
      const res = await fetch(window.ET_DATA_URL);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      ALL_SKILLS = data.skills || [];
      SKILLS_BY_ID = Object.fromEntries(ALL_SKILLS.map(s => [s.id, s]));
      renderTagPills();
      applySort();
      applyFilters();
    } catch (err) {
      console.error("Evidence Toolkit: failed to load skill data", err);
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    bindGlobalEvents();
    loadSkillData();
  });
})();
