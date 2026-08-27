/*
  Visual codes page: loads codes-en.json, renders one section per category
  with a before/after slider per code, and wires up the slider interaction.

  The copy buttons need no code here — they use data-copy, which the shared
  /assets/js/copy-to-clipboard.js already listens for on the whole document.

  Slider model: each .vc-compare element has a CSS custom property --pos
  (0–100%). CSS derives everything (clip, handle position) from it, so the
  JS only has to compute a percentage from the pointer and set the property.
*/

/* Same HTML-escaping helper as the site's render-grid.js — JSON content is
   our own, but escaping keeps any future edit safe. */
function vcEscape(s = '') {
  return String(s).replace(/[&<>"']/g, c => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));
}

/* Every generated .webp exists in two widths: name.webp (1168w) and
   name-584w.webp (half size). This builds the srcset/sizes attributes so
   the browser picks the smaller file on 1x screens — same load-time
   optimization as the Infographic styles page. SVG placeholders have no
   size variants, so they get a plain src. */
function vcImgAttrs(path) {
  if (!path.endsWith('.webp')) return `src="${path}"`;
  const half = path.replace(/\.webp$/, '-584w.webp');
  return `src="${path}" srcset="${half} 584w, ${path} 1168w" sizes="(min-width: 900px) 540px, 92vw"`;
}

/* Build the markup for one code card. Codes without a generated image pair
   fall back to the neutral placeholder images. */
function vcCardHtml(item) {
  const before = item.before || 'images/placeholder-before.svg';
  const after  = item.after  || 'images/placeholder-after.svg';
  const code   = vcEscape(item.code);
  /* Codes with an `addition` were generated with the codeword PLUS that text,
     so the copy button hands over the whole prompt — otherwise the copied
     text would not reproduce the image shown right below it. */
  const copyText = vcEscape(item.addition ? `${item.code} ${item.addition}` : item.code);
  return `
  <article class="vc-card">
    <div class="vc-card__head">
      <button class="vc-card__code" data-copy="${copyText}" aria-label="Copy ${code}${item.addition ? ' and its addition' : ''} to the clipboard">${code}</button>
      <span class="copy-toast">Copied!</span>
      <span class="vc-card__hint">${item.addition ? 'Click to copy both' : 'Click to copy'}</span>
    </div>
    <p class="vc-card__desc">${vcEscape(item.description)}</p>
    ${item.addition ? `<p class="vc-card__addition"><span class="vc-card__addition-label">Add</span> ${vcEscape(item.addition)}</p>` : ''}
    <div class="vc-compare">
      <img ${vcImgAttrs(after)} alt="Result after sending ${code} to ChatGPT" loading="lazy" decoding="async">
      <span class="vc-compare__chip vc-compare__chip--after">${code}</span>
      <div class="vc-compare__before">
        <img ${vcImgAttrs(before)} alt="Original photo before ${code}" loading="lazy" decoding="async">
        <span class="vc-compare__chip vc-compare__chip--before">Original</span>
      </div>
      <button class="vc-compare__handle" role="slider" aria-label="Compare original and ${code} result"
              aria-valuemin="0" aria-valuemax="100" aria-valuenow="50" aria-valuetext="50% original">
        <span class="vc-compare__grip" aria-hidden="true">&#9664;&#9654;</span>
      </button>
    </div>
    ${item.note ? `<p class="vc-card__note">${vcEscape(item.note)}</p>` : ''}
  </article>`;
}

/* Make one slider interactive: drag with mouse/touch, arrow keys on the handle. */
function vcInitCompare(el) {
  const handle = el.querySelector('.vc-compare__handle');

  /* Move the divider to `percent` and keep the accessibility values in sync. */
  function setPos(percent) {
    const p = Math.max(0, Math.min(100, percent));
    el.style.setProperty('--pos', p + '%');
    handle.setAttribute('aria-valuenow', Math.round(p));
    handle.setAttribute('aria-valuetext', Math.round(p) + '% original');
  }

  /* Translate a pointer's x-coordinate into a percentage of the frame width. */
  function posFromEvent(e) {
    const rect = el.getBoundingClientRect();
    return ((e.clientX - rect.left) / rect.width) * 100;
  }

  /* Pointer events cover mouse, touch and pen with one API.
     `dragging` is our own state rather than hasPointerCapture(), so a drag
     still works if capture is unavailable — on iPadOS capture can be refused
     or handed back mid-gesture, and relying on it alone left the slider dead. */
  let dragging = false;

  el.addEventListener('pointerdown', (e) => {
    dragging = true;
    setPos(posFromEvent(e));
    /* Capture is still worth having: it keeps delivering pointermove when the
       finger or cursor strays outside the frame. Failure here is not fatal. */
    try { el.setPointerCapture(e.pointerId); } catch (_) { /* noop */ }
  });
  el.addEventListener('pointermove', (e) => {
    if (dragging) setPos(posFromEvent(e));
  });
  /* pointercancel fires when the browser takes the gesture over — on touch
     that means the reader started scrolling vertically, so let go cleanly. */
  ['pointerup', 'pointercancel', 'lostpointercapture'].forEach((evt) =>
    el.addEventListener(evt, () => { dragging = false; }));

  /* Keyboard support: arrows nudge 5%, Home/End jump to the extremes. */
  handle.addEventListener('keydown', (e) => {
    const now = Number(handle.getAttribute('aria-valuenow'));
    const step = { ArrowLeft: -5, ArrowRight: 5 }[e.key];
    if (step !== undefined) { setPos(now + step); e.preventDefault(); }
    else if (e.key === 'Home') { setPos(0); e.preventDefault(); }
    else if (e.key === 'End')  { setPos(100); e.preventDefault(); }
  });
}

/* Fetch the data and build every category section. */
async function vcRender() {
  const root = document.getElementById('vc-root');
  if (!root) return;
  try {
    const res = await fetch('codes-en.json');
    if (!res.ok) throw new Error(res.status);
    const data = await res.json();

    root.innerHTML = data.categories.map(cat => `
      <section class="container vc-category" id="${vcEscape(cat.id)}">
        <h2>${vcEscape(cat.title)}</h2>
        <p>${vcEscape(cat.intro)}</p>
        <div class="vc-grid">${cat.codes.map(vcCardHtml).join('')}</div>
      </section>`).join('');

    /* Whole document, not just root: the two hero examples sit in the page's
       own HTML, above the rendered categories. */
    document.querySelectorAll('.vc-compare').forEach(vcInitCompare);
  } catch (err) {
    console.error('[visual-codes] failed to load codes-en.json:', err);
    root.innerHTML = '<p class="container error">Failed to load the codes. Please refresh.</p>';
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', vcRender);
} else {
  vcRender();
}
