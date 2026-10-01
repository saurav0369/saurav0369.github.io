(() => {
  const d = document, root = d.documentElement;
  root.classList.add('js');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (reduce) d.querySelectorAll('svg animate, svg animateMotion').forEach(a => a.remove());

  d.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());

  // theme
  const tbtn = d.querySelector('[data-theme-toggle]');
  if (tbtn) tbtn.addEventListener('click', () => {
    const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('theme', next); } catch (e) {}
    tbtn.setAttribute('aria-pressed', String(next === 'dark'));
  });

  // mobile menu
  const header = d.querySelector('.site-header');
  const mbtn = d.querySelector('[data-menu]');
  if (mbtn) {
    mbtn.addEventListener('click', () => {
      const open = header.classList.toggle('nav-open');
      mbtn.setAttribute('aria-expanded', String(open));
    });
    d.addEventListener('keydown', e => { if (e.key === 'Escape' && header.classList.contains('nav-open')) { header.classList.remove('nav-open'); mbtn.setAttribute('aria-expanded', 'false'); mbtn.focus(); } });
  }

  // scroll progress + header state
  const bar = d.querySelector('.progress');
  let ticking = false;
  const onScroll = () => {
    const h = root.scrollHeight - innerHeight;
    if (bar) bar.style.setProperty('--p', h > 0 ? (scrollY / h).toFixed(4) : 0);
    if (header) header.classList.toggle('scrolled', scrollY > 8);
    ticking = false;
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  // split headline words
  d.querySelectorAll('[data-split]').forEach(el => {
    let i = 0;
    const walk = node => {
      [...node.childNodes].forEach(n => {
        if (n.nodeType === 3) {
          const frag = d.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(part => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(d.createTextNode(part)); return; }
            const w = d.createElement('span'); w.className = 'w';
            const s = d.createElement('span'); s.textContent = part; s.style.setProperty('--i', i++);
            w.appendChild(s); frag.appendChild(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1) walk(n);
      });
    };
    walk(el);
    el.classList.add('split');
    if (!el.hasAttribute('data-reveal')) el.setAttribute('data-reveal', '');
  });

  // dot marks: data-dots="14/20"
  d.querySelectorAll('[data-dots]').forEach(el => {
    const [n, total] = el.dataset.dots.split('/').map(Number);
    el.style.setProperty('--cols', el.dataset.cols || Math.min(total, 20));
    el.setAttribute('role', 'img');
    el.setAttribute('aria-label', `${n} of ${total}`);
    for (let k = 0; k < total; k++) { const i = d.createElement('i'); i.dataset.k = k; el.appendChild(i); }
    el._fill = () => {
      const cells = el.querySelectorAll('i');
      cells.forEach((c, k) => { if (k < n) { if (reduce) c.classList.add('on'); else setTimeout(() => c.classList.add('on'), 200 + k * 45); } });
    };
  });

  // count-up
  const fmt = (v, dec) => v.toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  const countUp = el => {
    const target = parseFloat(el.dataset.count), dec = (el.dataset.count.split('.')[1] || '').length;
    if (reduce || target === 0) return;
    const dur = 1400, t0 = performance.now();
    const step = t => {
      const p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 4);
      el.textContent = fmt(target * e, dec);
      if (p < 1) requestAnimationFrame(step); else el.textContent = fmt(target, dec);
    };
    el.textContent = fmt(0, dec);
    requestAnimationFrame(step);
  };

  // reveal
  const io = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (!en.isIntersecting) return;
      const el = en.target;
      el.classList.add('in');
      el.querySelectorAll('[data-count]').forEach(countUp);
      el.querySelectorAll('[data-dots]').forEach(x => x._fill && x._fill());
      if (el.matches('[data-dots]') && el._fill) el._fill();
      io.unobserve(el);
    });
  }, { threshold: 0.18, rootMargin: '0px 0px -6% 0px' });
  d.querySelectorAll('[data-reveal], .figure, .evidence, .timeline, .pipeline-wrap').forEach(el => io.observe(el));

  // pause looping figures offscreen
  const po = new IntersectionObserver(es => es.forEach(e => { e.target.classList.toggle('paused', !e.isIntersecting); e.target.querySelectorAll('svg').forEach(s => { try { e.isIntersecting ? s.unpauseAnimations() : s.pauseAnimations(); } catch (_) {} }); }), { threshold: 0 });
  d.querySelectorAll('.figure').forEach(f => po.observe(f));

  // toc active state
  const toc = d.querySelectorAll('.toc a');
  if (toc.length) {
    const map = new Map([...toc].map(a => [a.getAttribute('href').slice(1), a]));
    const so = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { toc.forEach(a => a.classList.remove('active')); const a = map.get(e.target.id); if (a) a.classList.add('active'); }
    }), { rootMargin: '-30% 0px -60% 0px' });
    map.forEach((_, id) => { const s = d.getElementById(id); if (s) so.observe(s); });
  }
})();
