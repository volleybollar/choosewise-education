/*
  Client-side HTML includes.
  Usage in any page:
    <div data-include="/assets/partials/header-en.html"></div>
    <script src="/assets/js/include.js"></script>
*/

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
