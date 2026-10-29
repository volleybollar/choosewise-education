/*
  Gated download flow.
  On any element with data-gate="<resource-id>" data-gate-pdf="<pdf-url>"
  (optional data-gate-title="<modal heading>"):
    - Opens a modal with an email field and an optional role select
    - On submit: POST to MailerLite (if configured) with the resource id, the
      absolute PDF URL, the traffic source and the role
    - Then always shows "Download PDF" with a direct link, even if the POST failed
    - Remembers (flag only, never the address) that this browser has signed up,
      so the next gated PDF downloads straight away without the modal

  Gates are plain <a href="<pdf>"> links, so without JavaScript the PDF just downloads.

  Note: MailerLite's jsonp endpoint uses mode: 'no-cors', so we can't read the response.
  We assume success after the POST resolves.
*/

import { MAILERLITE } from './mailerlite-config.js';

const SUBSCRIBED_KEY = 'cw-subscribed';
const SOURCE_KEY = 'cw-src';
const LIVE_ORIGIN = 'https://choosewise.education';

// Storage can be blocked (private windows, strict settings) — never let that break the gate.
function store(kind, key, value) {
  try { window[kind].setItem(key, value); } catch (e) { /* ignore */ }
}
function load(kind, key) {
  try { return window[kind].getItem(key); } catch (e) { return null; }
}

// Traffic source: ?src= on this page wins, then what an earlier page in this
// visit saw (include.js stores it on every page), else "site".
// Only short lowercase slugs are accepted.
function readSource() {
  const raw = (new URLSearchParams(location.search).get('src') || '').toLowerCase();
  if (/^[a-z0-9-]{1,20}$/.test(raw)) {
    store('sessionStorage', SOURCE_KEY, raw);
    return raw;
  }
  return load('sessionStorage', SOURCE_KEY) || 'site';
}
const SOURCE = readSource();

// The delivery email needs a full URL. On localhost/previews, point at the live site.
function absolutePdfUrl(pdf) {
  const url = new URL(pdf, location.origin);
  return /^(localhost|127\.0\.0\.1)$/.test(url.hostname) ? LIVE_ORIGIN + url.pathname : url.href;
}

const MODAL_HTML = `
  <div class="modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="gate-title">
    <div class="modal">
      <button class="modal__close" aria-label="Close">&times;</button>
      <h3 id="gate-title">Get the PDF</h3>
      <p class="modal__desc">Enter your email and I'll send you this and future free resources for educators. Unsubscribe anytime.</p>
      <form class="modal__form" novalidate>
        <label class="visually-hidden" for="gate-email">Email</label>
        <input class="input" type="email" id="gate-email" name="email" placeholder="you@school.edu" required autocomplete="email">
        <label class="modal__label" for="gate-role">I am a… (optional)</label>
        <select class="input" id="gate-role" name="role">
          <option value=""></option>
          <option value="teacher">Teacher</option>
          <option value="school-leader">School leader</option>
          <option value="other">Other</option>
        </select>
        <input type="hidden" name="guide" value="">
        <button class="btn btn--primary modal__submit" type="submit">Send it to me</button>
      </form>
      <div class="modal__success">
        <h3>Your download is ready</h3>
        <p class="modal__desc">If you're new here, look for a confirmation email from me. Confirm it, and new resources will reach you as they're published.</p>
        <a class="btn btn--secondary" href="" download>Download PDF</a>
      </div>
    </div>
  </div>
`;

function ensureModal() {
  if (document.querySelector('.modal-backdrop')) return;
  document.body.insertAdjacentHTML('beforeend', MODAL_HTML);

  const backdrop = document.querySelector('.modal-backdrop');

  // Close on backdrop click OR close button
  backdrop.addEventListener('click', (e) => {
    if (e.target === backdrop || e.target.classList.contains('modal__close')) {
      backdrop.classList.remove('modal-backdrop--open');
    }
  });

  // Close on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && backdrop.classList.contains('modal-backdrop--open')) {
      backdrop.classList.remove('modal-backdrop--open');
    }
  });

  // Submit handler
  backdrop.querySelector('form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const email = form.email.value.trim();
    if (!email || !email.includes('@')) {
      alert('Please enter a valid email.');
      return;
    }

    if (MAILERLITE.configured) {
      try {
        const data = new URLSearchParams();
        data.set(MAILERLITE.fields.email, email);
        data.set(MAILERLITE.fields.guide, form.guide.value);
        data.set(MAILERLITE.fields.pdf, absolutePdfUrl(backdrop.dataset.pdfUrl));
        data.set(MAILERLITE.fields.source, SOURCE);
        data.set(MAILERLITE.fields.role, form.role.value);
        data.set('anticsrf', 'true');
        await fetch(MAILERLITE.formAction, { method: 'POST', mode: 'no-cors', body: data });
        // Only remember the sign-up when the request actually went out. If an ad
        // blocker or the network stopped it, the visitor is asked again next time.
        store('localStorage', SUBSCRIBED_KEY, '1');
      } catch (err) {
        console.error('[gate] MailerLite submit failed:', err);
        // Continue to success screen anyway — user still gets the PDF
      }
    } else {
      console.info('[gate] MailerLite not configured — skipping email capture, offering direct download');
    }

    // Always reveal the download regardless of email submission outcome
    form.style.display = 'none';
    const success = backdrop.querySelector('.modal__success');
    success.classList.add('modal__success--visible');
    success.querySelector('a').href = backdrop.dataset.pdfUrl;
  });
}

document.addEventListener('click', (e) => {
  const trigger = e.target.closest('[data-gate]');
  if (!trigger) return;
  e.preventDefault();
  const pdf = trigger.getAttribute('data-gate-pdf');

  // Already signed up in this browser: no second form, just the PDF.
  if (load('localStorage', SUBSCRIBED_KEY) === '1') {
    // Räkna nedladdningen anonymt (pdf-count.js, laddas av include.js).
    // Nya besökare räknas i stället när de klickar på länken i rutan:
    // den är en vanlig PDF-länk, så pdf-count.js fångar klicket själv.
    if (window.cwCountPdf) window.cwCountPdf(pdf);
    location.href = pdf;
    return;
  }

  ensureModal();
  const backdrop = document.querySelector('.modal-backdrop');
  backdrop.dataset.pdfUrl = pdf;
  backdrop.querySelector('#gate-title').textContent = trigger.getAttribute('data-gate-title') || 'Get the PDF';
  backdrop.querySelector('input[name="guide"]').value = trigger.getAttribute('data-gate');
  backdrop.querySelector('.modal__form').style.display = '';
  backdrop.querySelector('.modal__success').classList.remove('modal__success--visible');
  backdrop.classList.add('modal-backdrop--open');
  // Focus the email input after the transition settles
  setTimeout(() => backdrop.querySelector('#gate-email').focus(), 50);
});
