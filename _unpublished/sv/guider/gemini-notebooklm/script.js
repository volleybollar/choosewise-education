/* ─────────────────────────────────────────────────────────
   The Educator's Guide to Claude — page interactions
   Vanilla JavaScript, no dependencies, no build step.
   ───────────────────────────────────────────────────────── */

(function () {
  'use strict';

  // ─── 1. Sticky anchor nav appears once the hero scrolls past ───
  const nav = document.getElementById('anchorNav');
  const hero = document.querySelector('.hero');

  if (nav && hero) {
    const updateNavVisibility = () => {
      const heroBottom = hero.getBoundingClientRect().bottom;
      if (heroBottom < 60) {
        nav.classList.add('is-visible');
      } else {
        nav.classList.remove('is-visible');
      }
    };
    window.addEventListener('scroll', updateNavVisibility, { passive: true });
    updateNavVisibility();
  }

  // ─── 2. Active section highlighting in nav ───
  const sectionIds = ['part-1', 'part-2', 'part-3', 'prompts', 'download'];
  const sections = sectionIds
    .map(id => document.getElementById(id))
    .filter(Boolean);
  const navLinks = nav ? nav.querySelectorAll('a[href^="#"]') : [];

  if (sections.length && navLinks.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          navLinks.forEach(link => link.classList.remove('is-active'));
          const match = nav.querySelector(`a[href="#${entry.target.id}"]`);
          if (match) match.classList.add('is-active');
        }
      });
    }, { rootMargin: '-30% 0px -55% 0px' });
    sections.forEach(section => observer.observe(section));
  }

  // ─── 3. Smooth scroll for all anchor links ───
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (event) => {
      const id = anchor.getAttribute('href').slice(1);
      if (!id) return;
      const target = document.getElementById(id);
      if (target) {
        event.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        // Update the URL hash without causing another jump.
        if (history && history.pushState) {
          history.pushState(null, '', `#${id}`);
        }
      }
    });
  });

  // ─── 4. Expandable prompt cards ───
  document.querySelectorAll('.prompt-card').forEach(card => {
    const title = card.querySelector('.prompt-card__title');
    if (!title) return;
    title.setAttribute('role', 'button');
    title.setAttribute('tabindex', '0');
    title.setAttribute('aria-expanded', 'false');

    const toggle = () => {
      const nowOpen = card.classList.toggle('is-open');
      title.setAttribute('aria-expanded', String(nowOpen));
    };

    title.addEventListener('click', toggle);
    title.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggle();
      }
    });
  });

  // ─── 5. Click-to-copy on prompt cards ───
  document.querySelectorAll('[data-copy]').forEach(button => {
    button.addEventListener('click', (event) => {
      event.stopPropagation();
      const card = button.closest('.prompt-card');
      const text = card ? card.querySelector('.prompt-card__text') : null;
      if (!text) return;

      const copyText = text.textContent.trim();

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(copyText).then(() => {
          showCopiedState(button);
        }).catch(() => {
          fallbackCopy(copyText);
          showCopiedState(button);
        });
      } else {
        fallbackCopy(copyText);
        showCopiedState(button);
      }
    });
  });

  function showCopiedState(button) {
    const originalText = button.textContent;
    button.textContent = 'Copied ✓';
    button.classList.add('is-copied');
    setTimeout(() => {
      button.textContent = originalText;
      button.classList.remove('is-copied');
    }, 1600);
  }

  function fallbackCopy(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand('copy');
    } catch (e) {
      /* no-op */
    }
    document.body.removeChild(textarea);
  }

  // ─── 6. Auto-open FAQ item if linked via hash ───
  if (location.hash.startsWith('#faq-')) {
    const target = document.getElementById(location.hash.slice(1));
    if (target && target.tagName.toLowerCase() === 'details') {
      target.setAttribute('open', 'open');
    }
  }
})();
