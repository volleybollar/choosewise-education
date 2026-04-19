/*
  Generic JSON-to-cards grid renderer.
  Consumer HTML has:
    <div id="grid" data-source="/path/to/data.json" data-template="style"></div>

  Templates: 'style' (flip card with image + prompt), 'prompt' (PDF download card), 'guide', 'blog-post'
*/

/* Language-aware strings for the style template (resolved at render time from URL path) */
const IS_SV = typeof location !== 'undefined' && location.pathname.startsWith('/sv/');
const COPY_BTN_LABEL = IS_SV ? 'Kopiera prompt – Stil' : 'Copy prompt – Style';
const COPIED_LABEL   = IS_SV ? 'Kopierat!' : 'Copied!';

const TEMPLATES = {
  /* NotebookLM style — flip card with image front, prompt back.
     `item.id` looks like "style-1" / "style-140"; we extract the number for the button label. */
  style: (item, idx) => {
    const styleNumber = String(item.id || '').replace(/^style-/, '') || String(idx + 1);
    return `
    <article class="flipcard" data-index="${idx}">
      <div class="flipcard__inner">
        <div class="flipcard__face flipcard__front">
          <img src="${item.image}" alt="${escapeHtml(item.title)}" loading="lazy" decoding="async">
          <div class="flipcard__overlay">
            <h3 class="flipcard__title">${escapeHtml(item.title)}</h3>
            ${item.description ? `<p class="flipcard__description">${escapeHtml(item.description)}</p>` : ''}
            <span class="flipcard__category">${escapeHtml(item.category || '')}</span>
          </div>
        </div>
        <div class="flipcard__face flipcard__back">
          <div class="flipcard__prompt">${escapeHtml(item.prompt)}</div>
          <button class="btn btn--primary copy-btn" data-copy="${escapeAttr(item.prompt)}">
            ${COPY_BTN_LABEL} ${escapeHtml(styleNumber)}
          </button>
          <span class="copy-toast">${COPIED_LABEL}</span>
        </div>
      </div>
    </article>`;
  },

  /* Prompt library — download card */
  prompt: (item) => `
    <article class="card card--prompt">
      ${item.cover_image ? `<div class="card__image"><img src="${item.cover_image}" alt="" loading="lazy"></div>` : ''}
      <div class="card__body">
        <span class="card__meta">${escapeHtml(item.role || '')} · ${escapeHtml(item.topic || '')}</span>
        <h3 class="card__title">${escapeHtml(item.title)}</h3>
        <p class="card__excerpt">${escapeHtml(item.description || '')}</p>
        <a class="btn btn--secondary" href="${item.pdf_url}" download>Download PDF</a>
      </div>
    </article>`,

  /* Guide landing — tool card with status */
  guide: (item) => `
    <a class="card card--guide ${item.status === 'coming-soon' ? 'card--disabled' : ''}"
       href="${item.status === 'coming-soon' ? '#' : item.url}"
       ${item.status === 'coming-soon' ? 'aria-disabled="true"' : ''}>
      ${item.cover_image ? `<div class="card__image"><img src="${item.cover_image}" alt=""></div>` : ''}
      <div class="card__body">
        <span class="card__meta">${escapeHtml(item.tool)}${item.status === 'coming-soon' ? ' · Coming soon' : ''}</span>
        <h3 class="card__title">${escapeHtml(item.title)}</h3>
      </div>
    </a>`,

  /* Blog post preview */
  'blog-post': (item) => `
    <a class="card card--post" href="/blog/post.html?slug=${encodeURIComponent(item.slug)}">
      ${item.cover_image ? `<div class="card__image"><img src="${item.cover_image}" alt="" loading="lazy"></div>` : ''}
      <div class="card__body">
        <span class="card__meta">${item.date}</span>
        <h3 class="card__title">${escapeHtml(item.title)}</h3>
        <p class="card__excerpt">${escapeHtml(item.excerpt || '')}</p>
      </div>
    </a>`,
};

function escapeHtml(s = '') {
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function escapeAttr(s = '') { return escapeHtml(s); }

async function renderAllGrids() {
  const grids = document.querySelectorAll('[data-source][data-template]');
  for (const el of grids) {
    const src = el.dataset.source;
    const tpl = TEMPLATES[el.dataset.template];
    if (!tpl) { console.error(`[grid] unknown template: ${el.dataset.template}`); continue; }
    el.innerHTML = Array.from({length: 6}).map(() => '<div class="skeleton skeleton--card"></div>').join('');
    try {
      const res = await fetch(src);
      if (!res.ok) throw new Error(`${res.status}`);
      const items = await res.json();
      el.innerHTML = items.map((item, i) => tpl(item, i)).join('');
      el.dispatchEvent(new CustomEvent('grid:rendered', { detail: { count: items.length }}));
    } catch (err) {
      console.error(`[grid] failed ${src}:`, err);
      el.innerHTML = '<p class="error">Failed to load content. Please refresh.</p>';
    }
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', renderAllGrids);
} else {
  renderAllGrids();
}
