/*
  Pinned scroll-driven animation for the WISE framework signature section.
  - Each letter (W, I, S, E) scales from 0.4 → 1 and fades in as user scrolls
  - Matching panel on the right fades in, stays, then fades out to 25%
  - Respects prefers-reduced-motion (shows all letters and first panel instantly)
  - Falls back cleanly on small screens (no pinning; CSS layout stacks panels)
*/

(function initWiseSignature() {
  if (!window.gsap || !window.ScrollTrigger) return;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const letters = document.querySelectorAll('.wise-letter');
  const panels  = document.querySelectorAll('.wise-panel');
  if (letters.length === 0) return;

  // On narrow viewports, CSS shows everything in stacked layout — don't animate.
  const narrow = window.matchMedia('(max-width: 900px)').matches;

  if (reduced || narrow) {
    letters.forEach(l => { l.style.opacity = '1'; });
    panels.forEach((p, i) => {
      p.classList.add('is-visible');
      if (!narrow && i > 0) p.style.opacity = '0.25';
    });
    return;
  }

  gsap.registerPlugin(ScrollTrigger);

  // Initial state
  gsap.set(letters, { opacity: 0, scale: 0.4, transformOrigin: '50% 50%' });
  gsap.set(panels,  { opacity: 0, y: 30 });

  const tl = gsap.timeline({
    scrollTrigger: {
      trigger: '#wise-signature',
      start: 'top top',
      end: '+=2000',
      pin: true,
      scrub: 0.5,
    },
  });

  ['W','I','S','E'].forEach((letter, idx) => {
    const sel = `[data-letter="${letter}"]`;
    tl.to(`.wise-letter${sel}`, { opacity: 1, scale: 1, duration: 0.5 }, idx)
      .to(`.wise-panel${sel}`,  { opacity: 1, y: 0,  duration: 0.5 }, idx)
      .to(`.wise-panel${sel}`,  { opacity: 0.25, y: -20, duration: 0.5 }, idx + 0.7);
  });
})();
