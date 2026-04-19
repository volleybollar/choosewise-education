/*
  Pinned scroll-driven animation for the WISE framework signature section.
  - Each letter (W, I, S, E) scales from 0.4 → 1 and fades in as user scrolls
  - Matching panel fades in, stays, then fades completely out before the next panel appears
    (so only one panel is readable at a time — no ghost-text overlap)
  - Last panel stays visible at the end of the timeline
  - Respects prefers-reduced-motion (shows all letters and first panel instantly)
  - Falls back cleanly on small screens (no pinning; CSS layout stacks panels)
*/

(function initWiseSignature() {
  if (!window.gsap || !window.ScrollTrigger) return;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const letters = document.querySelectorAll('.wise-letter');
  const panels  = document.querySelectorAll('.wise-panel');
  if (letters.length === 0) return;

  // On narrow viewports, CSS shows everything in stacked layout — the pinned
  // scroll-driven timeline is skipped. We still want a sense of motion though,
  // so we fade letters + panels in as they reach the viewport.
  const narrow = window.matchMedia('(max-width: 900px)').matches;

  if (reduced) {
    letters.forEach(l => { l.style.opacity = '1'; });
    panels.forEach((p) => {
      p.classList.add('is-visible');
      p.style.opacity = '1';
    });
    return;
  }

  gsap.registerPlugin(ScrollTrigger);

  if (narrow) {
    // Mobile fallback: fade in the whole diagram when it enters the viewport,
    // then fade each panel in as it scrolls into view below it. We animate the
    // diagram as a single CSS container (not per-letter SVG transforms) because
    // iOS Safari is unreliable with GSAP scale on SVG <g> elements.
    const diagram = document.querySelector('.wise-signature__diagram');
    if (diagram) {
      gsap.set(diagram, { opacity: 0, y: 12 });
      gsap.to(diagram, {
        opacity: 1, y: 0, duration: 0.7, ease: 'power2.out',
        scrollTrigger: { trigger: diagram, start: 'top 90%', toggleActions: 'play none none none' },
      });
    }
    letters.forEach(l => { l.style.opacity = '1'; });
    panels.forEach((p) => {
      gsap.set(p, { opacity: 0, y: 20 });
      gsap.to(p, {
        opacity: 1, y: 0, duration: 0.5, ease: 'power2.out',
        onStart: () => p.classList.add('is-visible'),
        scrollTrigger: { trigger: p, start: 'top 90%', toggleActions: 'play none none none' },
      });
    });
    // iOS Safari sometimes computes ScrollTrigger start positions before layout
    // settles — refresh once the page is fully loaded + after 400ms as a backstop.
    window.addEventListener('load', () => ScrollTrigger.refresh());
    setTimeout(() => ScrollTrigger.refresh(), 400);
    return;
  }

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

  // Detect which letters this page uses by reading data-letter attributes.
  // Timeline uses unit=1 per letter. Within each slot:
  //   - Letter scales + fades in at t = idx (stays visible through the rest of the timeline)
  //   - Panel fades in at t = idx
  //   - Panel fades out at t = idx + 0.7 (so the next panel at t = idx+1 appears clean)
  //   - Last panel does NOT fade out — it remains visible at the end of the timeline
  const letterOrder = Array.from(letters).map(el => el.dataset.letter);
  const lastIdx = letterOrder.length - 1;
  letterOrder.forEach((letter, idx) => {
    const sel = `[data-letter="${letter}"]`;
    tl.to(`.wise-letter${sel}`, { opacity: 1, scale: 1, duration: 0.4 }, idx)
      .to(`.wise-panel${sel}`,  { opacity: 1, y: 0, duration: 0.3 }, idx);
    if (idx < lastIdx) {
      tl.to(`.wise-panel${sel}`, { opacity: 0, y: -20, duration: 0.3 }, idx + 0.7);
    }
  });
})();
