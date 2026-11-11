(() => {
  'use strict';

  // ---- theme toggle (persists per viewer; falls back silently) ----
  const root = document.documentElement;
  const themeBtn = document.getElementById('theme-toggle');
  const stored = (() => { try { return localStorage.getItem('crj-theme'); } catch { return null; } })();
  if (stored === 'light' || stored === 'dark') root.setAttribute('data-theme', stored);

  function syncThemeLabel() {
    if (!themeBtn) return;
    const dark = root.getAttribute('data-theme') === 'dark' ||
      (!root.getAttribute('data-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
    themeBtn.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
    themeBtn.textContent = dark ? '☀' : '☾';
  }
  syncThemeLabel();
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const dark = root.getAttribute('data-theme') === 'dark' ||
        (!root.getAttribute('data-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
      const next = dark ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('crj-theme', next); } catch { /* ignore */ }
      syncThemeLabel();
    });
  }

  // ---- mobile nav ----
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.getElementById('nav-links');
  if (toggle && nav) {
    const close = () => { toggle.setAttribute('aria-expanded', 'false'); nav.classList.remove('open'); };
    const open = () => { toggle.setAttribute('aria-expanded', 'true'); nav.classList.add('open'); };
    toggle.addEventListener('click', () =>
      (toggle.getAttribute('aria-expanded') === 'true' ? close() : open()));
    nav.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && nav.classList.contains('open')) { close(); toggle.focus(); }
    });
    document.addEventListener('click', e => {
      if (nav.classList.contains('open') && !nav.contains(e.target) && !toggle.contains(e.target)) close();
    });
  }

  // ---- copy BibTeX (status announced via a dedicated live region) ----
  const copyBtn = document.getElementById('copy-bib');
  const bib = document.getElementById('bibtex');
  const live = document.getElementById('copy-status');
  if (copyBtn && bib) {
    let timer;
    const say = msg => { if (live) live.textContent = msg; };
    copyBtn.addEventListener('click', async () => {
      const text = bib.textContent.trim();
      try {
        await navigator.clipboard.writeText(text);
        say('BibTeX copied to clipboard');
        copyBtn.dataset.state = 'done';
        const label = copyBtn.querySelector('span');
        if (label) label.textContent = 'Copied';
        clearTimeout(timer);
        timer = setTimeout(() => { if (label) label.textContent = 'Copy BibTeX'; delete copyBtn.dataset.state; }, 2500);
      } catch {
        const r = document.createRange();
        r.selectNodeContents(bib);
        const sel = window.getSelection();
        sel.removeAllRanges(); sel.addRange(r);
        say('Select-all applied; press Ctrl or Cmd + C to copy');
      }
    });
  }
})();
