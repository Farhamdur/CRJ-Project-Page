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

  // ---- Copy BibTeX without selecting the visible code block ----
  const copyBtn = document.getElementById('copy-bib');
  const bib = document.getElementById('bibtex');
  const live = document.getElementById('copy-status');
  if (copyBtn && bib) {
    const label = copyBtn.querySelector('span');
    let timer;
    const say = (message) => { if (live) live.textContent = message; };

    async function copyBibTeX(text) {
      // Clipboard API works when the page is served over HTTPS or localhost.
      if (navigator.clipboard && window.isSecureContext) {
        try {
          await navigator.clipboard.writeText(text);
          return true;
        } catch { /* Try the legacy fallback below. */ }
      }

      // A hidden textarea prevents visible <pre> lines being selected.
      const field = document.createElement('textarea');
      field.value = text;
      field.setAttribute('readonly', '');
      field.style.cssText =
        'position:fixed;top:0;left:-9999px;width:1px;height:1px;opacity:0;';
      document.body.appendChild(field);
      field.focus();
      field.select();
      let copied = false;
      try { copied = document.execCommand('copy'); }
      catch { copied = false; }
      finally { field.remove(); }
      return copied;
    }

    copyBtn.addEventListener('click', async () => {
      // A leftover selection may be from the previous fallback implementation.
      const selection = window.getSelection();
      if (selection) selection.removeAllRanges();
      const text = bib.textContent.trim();
      const copied = await copyBibTeX(text);
      clearTimeout(timer);
      if (copied) {
        if (label) label.textContent = 'Copied!';
        say('BibTeX copied to clipboard.');
      } else {
        if (label) label.textContent = 'Copy unavailable';
        say('Automatic copying is unavailable. You can select the BibTeX manually.');
      }
      timer = setTimeout(() => {
        if (label) label.textContent = 'Copy BibTeX';
      }, 2500);
    });
  }
})();
