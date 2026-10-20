/*
  Client-side HTML includes.
  Usage in any page:
    <div data-include="/assets/partials/header-en.html"></div>
    <script src="/assets/js/include.js"></script>
*/

// Remember where this visit came from (?src=yt, ig …) so the email gate can
// record it even when the download happens on a later page. Same rule as in
// mailerlite-gate.js: short lowercase slugs only. Storage may be blocked — ignore.
(function rememberSource() {
  const src = (new URLSearchParams(location.search).get('src') || '').toLowerCase();
  if (!/^[a-z0-9-]{1,20}$/.test(src)) return;
  try { sessionStorage.setItem('cw-src', src); } catch (e) { /* ignore */ }
})();

(async function includePartials() {
  const slots = document.querySelectorAll('[data-include]');
  await Promise.all([...slots].map(async (el) => {
    const url = el.getAttribute('data-include');
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
      el.outerHTML = await res.text();
    } catch (err) {
      console.error(`[include] failed for ${url}:`, err);
      el.outerHTML = '';
    }
  }));
  document.dispatchEvent(new CustomEvent('includes:loaded'));
})();
