/*
  Visual codes for video: loads codes-video-en.json, renders one section per
  category with a card per code, and starts/stops the clips as they scroll.

  Part 1 sections go into #vcv-part1, Part 2 into #vcv-part2 — the static
  "Spot the error" box in index.html sits between them.

  Copy buttons need no code here: they use data-copy, which the shared
  /assets/js/copy-to-clipboard.js already listens for on the whole document.

  Media paths are built from each code's slug only:
  media/<slug>.mp4, media/<slug>-poster.webp, media/<slug>-start.webp
*/

/* Same HTML-escaping helper as the image page's visual-codes.js — the JSON
   is our own, but escaping keeps any future edit safe. */
function vcvEscape(s = '') {
  return String(s).replace(/[&<>"']/g, c => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));
}

/* The labels a card can carry. 'works' gets none — that is the normal case. */
const VCV_STATUS = { partial: 'Partly works', fails: "Doesn't work yet" };

/* Build one card. The prompt is the exact text that was sent, so the copy
   button hands over all of it, and the Add line shows what follows the code.
   Every card has the same six parts in the same order — an empty
   .vcv-slot stands in for a missing Add line, badge row or note — so the
   CSS subgrid can line them up with the card next to it. */
function vcvCardHtml(item) {
  const code = vcvEscape(item.code);
  const slug = vcvEscape(item.slug);
  const addition = item.prompt.slice(item.code.length).trim();
  const badges = [
    VCV_STATUS[item.status] ? `<span class="vcv-badge vcv-badge--${item.status}">${VCV_STATUS[item.status]}</span>` : '',
    item.spot_the_error ? '<span class="vcv-badge vcv-badge--spot">Spot the error</span>' : '',
  ].join('');
  return `
  <article class="vc-card vcv-card" data-slug="${slug}" data-status="${vcvEscape(item.status)}">
    <div class="vc-card__head">
      <button class="vc-card__code" data-copy="${vcvEscape(item.prompt)}" aria-label="Copy the prompt for ${code} to the clipboard">${code}</button>
      <span class="copy-toast">Copied!</span>
      <span class="vc-card__hint">${addition ? 'Click to copy both' : 'Click to copy'}</span>
    </div>
    <p class="vc-card__desc">${vcvEscape(item.description)}</p>
    ${addition ? `<p class="vc-card__addition"><span class="vc-card__addition-label">Add</span> ${vcvEscape(addition)}</p>` : '<div class="vcv-slot"></div>'}
    ${badges ? `<div class="vcv-badges">${badges}</div>` : '<div class="vcv-slot"></div>'}
    <div class="vcv-media">
      <video class="vcv-video" src="media/${slug}.mp4" poster="media/${slug}-poster.webp"
             muted loop playsinline preload="none" tabindex="0"
             aria-label="Clip made with ${code}. Press to pause or play."></video>
      <span class="vcv-play" aria-hidden="true"></span>
      <span class="vc-compare__chip vc-compare__chip--after">${code}</span>
      <figure class="vcv-start">
        <img src="media/${slug}-start.webp" alt="Start image sent with ${code}" loading="lazy" decoding="async">
        <figcaption>Start image</figcaption>
      </figure>
    </div>
    ${item.note ? `<p class="vc-card__note">${vcvEscape(item.note)}</p>` : '<div class="vcv-slot"></div>'}
  </article>`;
}

/* Visitors who ask the system for less motion get no autoplay — the poster
   shows, and the clip plays only when they start it. */
const vcvReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* One shared observer: a clip plays while at least half of it is on screen
   and pauses when it leaves, so ~45 videos never run at the same time.
   A clip the visitor paused themselves stays paused. */
const vcvObserver = 'IntersectionObserver' in window
  ? new IntersectionObserver(entries => entries.forEach(({ target, isIntersecting }) => {
      if (isIntersecting && !vcvReducedMotion && !target.dataset.userPaused) {
        target.play().catch(() => { /* autoplay refused — the poster stays */ });
      } else {
        target.pause();
      }
    }), { threshold: 0.5 })
  : null;

/* Click, Enter or Space toggles a clip — the keyboard route matters because
   reduced-motion visitors start every clip themselves. */
function vcvInitVideo(video) {
  const toggle = () => {
    if (video.paused) {
      delete video.dataset.userPaused;
      video.play().catch(() => {});
    } else {
      video.dataset.userPaused = 'true';
      video.pause();
    }
  };
  /* The play cue shows whenever the clip is not running — otherwise a paused
     poster looks like a still photo and nobody knows it is a clip. Driven by
     the video's own play/pause events, so it is right however playback
     started or stopped (observer, click, keyboard, or the browser itself). */
  const media = video.closest('.vcv-media');
  const sync = () => media && media.classList.toggle('is-paused', video.paused);
  video.addEventListener('play', sync);
  video.addEventListener('pause', sync);
  sync();
  video.addEventListener('click', toggle);
  video.addEventListener('keydown', (e) => {
    if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); toggle(); }
  });
  if (vcvObserver) vcvObserver.observe(video);
}

function vcvSectionHtml(section) {
  const box = section.id === 'doesnt-work-yet' ? ' vcv-box' : '';
  return `
  <section class="container vc-category${box}" id="${vcvEscape(section.id)}">
    <h3>${vcvEscape(section.title)}</h3>
    <p>${vcvEscape(section.intro)}</p>
    <div class="vc-grid">${section.codes.map(vcvCardHtml).join('')}</div>
  </section>`;
}

/* Fetch the data, build both parts, then wire up every clip on the page
   (including the two hand-written hero clips). */
async function vcvRender() {
  const part1 = document.getElementById('vcv-part1');
  const part2 = document.getElementById('vcv-part2');
  if (!part1 || !part2) return;
  try {
    const res = await fetch('codes-video-en.json');
    if (!res.ok) throw new Error(res.status);
    const data = await res.json();
    part1.innerHTML = data.sections.filter(s => s.part === 1).map(vcvSectionHtml).join('');
    part2.innerHTML = data.sections.filter(s => s.part === 2).map(vcvSectionHtml).join('');
  } catch (err) {
    console.error('[video-codes] failed to load codes-video-en.json:', err);
    part1.innerHTML = '<p class="container error">Failed to load the codes. Please refresh.</p>';
  }
  document.querySelectorAll('.vcv-video').forEach(vcvInitVideo);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', vcvRender);
} else {
  vcvRender();
}
