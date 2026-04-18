/*
  Gated download flow.
  On any <button data-gate="<guide-id>" data-gate-pdf="<pdf-url>">:
    - Opens a modal with an email form
    - On submit: POST to MailerLite (if configured)
    - On success OR if MailerLite not yet configured: show "Download your copy" with a direct link

  Note: MailerLite's jsonp endpoint uses mode: 'no-cors', so we can't read the response.
  We assume success after the POST resolves. The direct download link is always offered as
  a safety net.
*/

import { MAILERLITE } from './mailerlite-config.js';

const MODAL_HTML = `
  <div class="modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="gate-title">
    <div class="modal">
      <button class="modal__close" aria-label="Close">&times;</button>
      <h3 id="gate-title">Get the guide</h3>
      <p class="modal__desc">Enter your email and we'll send you the PDF. Unsubscribe anytime. No spam, ever.</p>
      <form class="modal__form" novalidate>
        <label class="visually-hidden" for="gate-email">Email</label>
        <input class="input" type="email" id="gate-email" name="email" placeholder="you@school.edu" required autocomplete="email">
        <input type="hidden" name="guide" value="">
        <button class="btn btn--primary modal__submit" type="submit">Send it to me</button>
      </form>
      <div class="modal__success">
        <h3>Check your inbox ✓</h3>
        <p class="modal__desc">We've sent the PDF to your email. You can also download it directly here:</p>
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
    const guide = form.guide.value;
    if (!email || !email.includes('@')) {
      alert('Please enter a valid email.');
      return;
    }

    if (MAILERLITE.configured) {
      try {
        const data = new URLSearchParams();
        data.set(MAILERLITE.fields.email, email);
        data.set(MAILERLITE.fields.guide, guide);
        data.set('anticsrf', 'true');
        await fetch(MAILERLITE.formAction, { method: 'POST', mode: 'no-cors', body: data });
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
  ensureModal();
  const backdrop = document.querySelector('.modal-backdrop');
  backdrop.dataset.pdfUrl = trigger.getAttribute('data-gate-pdf');
  backdrop.querySelector('input[name="guide"]').value = trigger.getAttribute('data-gate');
  backdrop.querySelector('.modal__form').style.display = '';
  backdrop.querySelector('.modal__success').classList.remove('modal__success--visible');
  backdrop.classList.add('modal-backdrop--open');
  // Focus the email input after the transition settles
  setTimeout(() => backdrop.querySelector('#gate-email').focus(), 50);
});
