/*
  Blog post renderer. Loads a .md file from blog/posts/ (or /sv/blog/posts/),
  parses with marked.js, injects into DOM.
  URL pattern: /blog/post.html?slug=<slug>  (EN)  or  /sv/blog/post.html?slug=<slug>  (SV)
*/

(async function loadPost() {
  const params = new URLSearchParams(location.search);
  const slug = params.get('slug');
  const target = document.getElementById('post-body');
  const metaEl = document.getElementById('post-meta');

  const isSv = location.pathname.startsWith('/sv/');
  const postsDir    = isSv ? '/sv/blog/posts/' : '/blog/posts/';
  const manifestUrl = isSv ? '/sv/blog/posts-sv.json' : '/blog/posts-en.json';

  if (!slug) {
    target.innerHTML = '<p>Missing post slug.</p>';
    return;
  }

  try {
    const [mdRes, listRes] = await Promise.all([
      fetch(`${postsDir}${slug}.md`),
      fetch(manifestUrl),
    ]);
    if (!mdRes.ok) throw new Error(`post not found: ${slug}`);
    const md = await mdRes.text();
    const list = await listRes.json();
    const meta = list.find(p => p.slug === slug);

    if (!window.marked) throw new Error('marked.js not loaded');
    target.innerHTML = window.marked.parse(md);

    if (meta) {
      document.title = `${meta.title} — choosewise.education`;
      const readingTime = meta.reading_time ? ` · ${meta.reading_time}` : '';
      metaEl.innerHTML = `<h1>${escapeHtml(meta.title)}</h1><span class="eyebrow">${escapeHtml(meta.date)}${readingTime}</span>`;
    }
  } catch (err) {
    console.error('[blog]', err);
    target.innerHTML = `<p>Sorry, couldn't load this post. <a href="${isSv ? '/sv/blog/' : '/blog/'}">Back to blog</a></p>`;
  }

  function escapeHtml(s = '') {
    return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }
})();
