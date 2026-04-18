/*
  Attaches to any <button data-copy="text">.
  On click: copies the text, shows an animated toast for 2 seconds.
  Also handles flipcard toggle: clicking a .flipcard (but not the copy button) flips it.
*/

document.addEventListener('click', async (e) => {
  const btn = e.target.closest('[data-copy]');
  if (!btn) return;
  const text = btn.getAttribute('data-copy');
  try {
    await navigator.clipboard.writeText(text);
    const toast = btn.parentElement.querySelector('.copy-toast');
    if (toast) {
      toast.classList.add('copy-toast--visible');
      setTimeout(() => toast.classList.remove('copy-toast--visible'), 2000);
    }
  } catch (err) {
    console.error('[copy] clipboard write failed:', err);
    alert('Copy failed. Please select and copy manually.');
  }
});

/* Flipcard toggle: clicking anywhere on a flipcard (except the copy button) flips it */
document.addEventListener('click', (e) => {
  const card = e.target.closest('.flipcard');
  if (!card) return;
  if (e.target.closest('.copy-btn')) return;
  card.classList.toggle('is-flipped');
});
