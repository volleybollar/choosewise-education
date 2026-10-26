/*
  Visual codes for studying: loads codes-study-en.json and renders one
  section per category with a card per code.

  Part 1 sections go into #vcs-part1, Part 2 into #vcs-part2 — the static
  "What went wrong" box in index.html sits between them.

  Copy buttons need no code here: they use data-copy, which the shared
  /assets/js/copy-to-clipboard.js already listens for on the whole document.

  Image paths are built from each code's slug only:
  images/<slug>-512w.webp on the card, images/<slug>.webp when clicked.
*/

/* Same HTML-escaping helper as the image and video pages */
function vcsEscape(s = '') {
  return String(s).replace(/[&<>"']/g, c => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));
}

/* Labels for the use chips and for the status badges. 'works' gets no
   badge — that is the normal case. */
const VCS_USES = { print: 'Print', wall: 'Wall', digital: 'Digital' };
const VCS_STATUS = { partial: 'Check the result', fails: "Doesn't work yet" };

/* The text the copy button hands over: the same shape as the prompt we sent
   in testing, with [your topic] where the topic went. */
function vcsPrompt(item) {
  return `${item.code} [your topic]. Make it an image.${item.addition ? ' ' + item.addition : ''}`;
}

/* Build one card. Every card has the same six parts in the same order — an
   empty .vcv-slot stands in for a missing part — so the CSS subgrid can line
   them up with the cards next to it (the video page uses the same trick).
   The third part is the Add line on practise cards and the "Make it active"
   line on reading cards. */
function vcsCardHtml(item) {
  const code = vcsEscape(item.code);
  const slug = vcsEscape(item.slug);

  let line = '<div class="vcv-slot"></div>';
  if (item.addition) {
    line = `<p class="vc-card__addition"><span class="vc-card__addition-label">Add</span> ${vcsEscape(item.addition)}</p>`;
  } else if (item.active) {
    line = `<p class="vcs-active"><span class="vcs-active__label">Make it active</span> ${vcsEscape(item.active)}</p>`;
  }

  const chips = [
    ...item.uses.map(u => `<span class="vcs-use">${VCS_USES[u]}</span>`),
    VCS_STATUS[item.status] ? `<span class="vcv-badge vcv-badge--${item.status}">${VCS_STATUS[item.status]}</span>` : '',
    item.spot_the_error ? '<span class="vcv-badge vcv-badge--spot">Spot the error</span>' : '',
  ].join('');

  return `
  <article class="vc-card vcs-card" data-slug="${slug}" data-status="${vcsEscape(item.status)}">
    <div class="vc-card__head">
      <button class="vc-card__code" data-copy="${vcsEscape(vcsPrompt(item))}" aria-label="Copy the prompt for ${code} to the clipboard">${code}</button>
      <span class="copy-toast">Copied!</span>
      <span class="vc-card__hint">Click to copy</span>
    </div>
    <p class="vc-card__desc">${vcsEscape(item.description)}</p>
    ${line}
    ${chips ? `<div class="vcv-badges">${chips}</div>` : '<div class="vcv-slot"></div>'}
    <figure class="vcs-figure">
      <a href="images/${slug}.webp" target="_blank" rel="noopener" aria-label="Open the full-size image for ${code}">
        <img src="images/${slug}-512w.webp"
             srcset="images/${slug}-512w.webp 512w, images/${slug}.webp 1024w"
             sizes="(min-width: 1100px) 340px, (min-width: 700px) 45vw, 92vw"
             width="512" height="768" loading="lazy" decoding="async"
             alt="Image made with ${code} on ${vcsEscape(item.subject)}">
      </a>
      <figcaption>Tested on ${vcsEscape(item.subject)} · click to enlarge</figcaption>
    </figure>
    ${item.note ? `<p class="vc-card__note">${vcsEscape(item.note)}</p>` : '<div class="vcv-slot"></div>'}
  </article>`;
}

function vcsSectionHtml(section) {
  const box = section.id === 'doesnt-work-yet' ? ' vcv-box' : '';
  return `
  <section class="container vc-category${box}" id="${vcsEscape(section.id)}">
    <h3>${vcsEscape(section.title)}</h3>
    <p>${vcsEscape(section.intro)}</p>
    <div class="vc-grid">${section.codes.map(vcsCardHtml).join('')}</div>
  </section>`;
}

/* Fetch the data and build both parts */
async function vcsRender() {
  const part1 = document.getElementById('vcs-part1');
  const part2 = document.getElementById('vcs-part2');
  if (!part1 || !part2) return;
  try {
    const res = await fetch('codes-study-en.json');
    if (!res.ok) throw new Error(res.status);
    const data = await res.json();
    part1.innerHTML = data.sections.filter(s => s.part === 1).map(vcsSectionHtml).join('');
    part2.innerHTML = data.sections.filter(s => s.part === 2).map(vcsSectionHtml).join('');
  } catch (err) {
    console.error('[study-codes] failed to load codes-study-en.json:', err);
    part1.innerHTML = '<p class="container error">Failed to load the codes. Please refresh.</p>';
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', vcsRender);
} else {
  vcsRender();
}
