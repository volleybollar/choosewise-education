/*
  Adds subtle fade-up to any element with [data-reveal].
  Respects prefers-reduced-motion.
  Depends on GSAP + ScrollTrigger loaded globally (via CDN in page HTML).
*/

(function initScrollReveals() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!window.gsap || !window.ScrollTrigger) { console.warn('[reveals] GSAP not loaded'); return; }

  gsap.registerPlugin(ScrollTrigger);

  const els = document.querySelectorAll('[data-reveal]');
  els.forEach((el) => {
    gsap.from(el, {
      y: 30,
      opacity: 0,
      duration: 0.8,
      ease: 'power2.out',
      scrollTrigger: {
        trigger: el,
        start: 'top 85%',
        toggleActions: 'play none none none',
      },
    });
  });
})();
