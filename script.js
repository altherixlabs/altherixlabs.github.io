/* ═══════════════════════════════════════════════════════════
   Altherix — shared site behaviour
   Loaded by every page. Every block is defensive: if a page
   does not contain the element, the block simply no-ops.
   ═══════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer  = window.matchMedia('(hover:hover) and (pointer:fine)').matches;

  /* ── LOADER ──────────────────────────────────────────────
     Shows once per browser session. Repeat navigation within
     the session skips it, and reduced-motion skips it always. */
  (function () {
    var loader = $('#loader');
    if (!loader) return;

    var seen = false;
    try { seen = sessionStorage.getItem('ax_loaded') === '1'; } catch (e) {}

    if (reduceMotion || seen) {
      loader.parentNode.removeChild(loader);
      document.body.classList.add('loaded');
      return;
    }

    var pct  = $('#lpct');
    var line = $('#lline');
    var p = 0;
    var iv = setInterval(function () {
      p = Math.min(p + Math.random() * 18, 100);
      if (pct)  pct.textContent = Math.round(p);
      if (line) line.style.width = p + '%';
      if (p >= 100) {
        clearInterval(iv);
        setTimeout(function () {
          loader.classList.add('done');
          document.body.classList.add('loaded');
          try { sessionStorage.setItem('ax_loaded', '1'); } catch (e) {}
          setTimeout(function () {
            if (loader.parentNode) loader.parentNode.removeChild(loader);
          }, 900);
        }, 300);
      }
    }, 60);
  })();

  /* ── SCROLL PROGRESS ─────────────────────────────────── */
  (function () {
    var fill = $('#progress-fill');
    if (!fill) return;
    var ticking = false;
    function update() {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      fill.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + '%';
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  })();

  /* ── CUSTOM CURSOR ───────────────────────────────────────
     Mouse-only. Skipped on touch and under reduced motion. */
  (function () {
    var dot  = $('#cur-dot');
    var ring = $('#cur-ring');
    if (!dot || !ring) return;

    if (!finePointer || reduceMotion) {
      dot.parentNode.removeChild(dot);
      ring.parentNode.removeChild(ring);
      return;
    }

    var mx = 0, my = 0, rx = 0, ry = 0;
    document.addEventListener('mousemove', function (e) {
      mx = e.clientX; my = e.clientY;
      dot.style.left = mx + 'px'; dot.style.top = my + 'px';
    }, { passive: true });

    (function loop() {
      rx += (mx - rx) * 0.1; ry += (my - ry) * 0.1;
      ring.style.left = Math.round(rx) + 'px';
      ring.style.top  = Math.round(ry) + 'px';
      requestAnimationFrame(loop);
    })();

    document.addEventListener('mouseover', function (e) {
      if (e.target.closest('a,button,summary,.svc,.tcard,.pcard,.why,.role')) {
        dot.classList.add('h'); ring.classList.add('h');
      }
    });
    document.addEventListener('mouseout', function (e) {
      if (e.target.closest('a,button,summary,.svc,.tcard,.pcard,.why,.role')) {
        dot.classList.remove('h'); ring.classList.remove('h');
      }
    });
  })();

  /* ── NAV: shadow on scroll + active section ──────────── */
  (function () {
    var nav = $('#nav');
    if (!nav) return;

    var anchors = $$('#navlinks a[href^="#"]');
    var sections = anchors
      .map(function (a) { return document.querySelector(a.getAttribute('href')); })
      .filter(Boolean);

    function update() {
      nav.classList.toggle('s', window.scrollY > 40);
      if (!sections.length) return;
      var current = sections[0];
      sections.forEach(function (sec) {
        if (window.scrollY >= sec.offsetTop - 120) current = sec;
      });
      anchors.forEach(function (a) {
        a.classList.toggle('active', a.getAttribute('href') === '#' + current.id);
      });
    }
    window.addEventListener('scroll', update, { passive: true });
    update();
  })();

  /* ── MOBILE NAV ──────────────────────────────────────────
     Class-driven, with aria state and Escape to close. */
  (function () {
    var ham   = $('#ham');
    var links = $('#navlinks');
    if (!ham || !links) return;

    function setOpen(open) {
      links.classList.toggle('open', open);
      ham.classList.toggle('open', open);
      ham.setAttribute('aria-expanded', open ? 'true' : 'false');
    }

    ham.setAttribute('role', 'button');
    ham.setAttribute('tabindex', '0');
    ham.setAttribute('aria-controls', 'navlinks');
    ham.setAttribute('aria-expanded', 'false');
    ham.setAttribute('aria-label', 'Toggle navigation menu');

    ham.addEventListener('click', function () {
      setOpen(!links.classList.contains('open'));
    });
    ham.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        setOpen(!links.classList.contains('open'));
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && links.classList.contains('open')) {
        setOpen(false); ham.focus();
      }
    });
    $$('#navlinks a').forEach(function (a) {
      a.addEventListener('click', function () { setOpen(false); });
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 860) setOpen(false);
    });
  })();

  /* ── REVEAL ON SCROLL ────────────────────────────────── */
  (function () {
    var targets = $$('.rv,.rvl,.rvr,.pcard,.why,.step,.feat');
    if (!targets.length) return;

    if (reduceMotion || !('IntersectionObserver' in window)) {
      targets.forEach(function (el) { el.classList.add('on', 'vis'); });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('on');
        if (e.target.classList.contains('pcard')) {
          e.target.classList.add('vis');
          var bar = e.target.querySelector('.pbar');
          if (bar) setTimeout(function () { bar.style.transform = 'scaleX(1)'; }, 200);
        }
        io.unobserve(e.target);
      });
    }, { threshold: 0.12 });
    targets.forEach(function (el) { io.observe(el); });
  })();

  /* ── COUNT-UP NUMBERS ────────────────────────────────── */
  (function () {
    var hosts = $$('.hero-card,.pcard,.hstat,.feat-meta');
    if (!hosts.length) return;

    function countUp(el) {
      var target = parseInt(el.dataset.count, 10);
      if (isNaN(target)) return;
      var sfx = el.dataset.sfx || '';
      if (reduceMotion) { el.textContent = target + sfx; return; }
      var dur = 1400, start = performance.now();
      var ease = function (t) { return 1 - Math.pow(1 - t, 4); };
      (function frame(now) {
        var p = Math.min((now - start) / dur, 1);
        el.textContent = Math.round(ease(p) * target) + sfx;
        if (p < 1) requestAnimationFrame(frame);
      })(performance.now());
    }

    if (!('IntersectionObserver' in window)) {
      $$('[data-count]').forEach(countUp);
      return;
    }
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        $$('[data-count]', e.target).forEach(countUp);
        cio.unobserve(e.target);
      });
    }, { threshold: 0.3 });
    hosts.forEach(function (el) { cio.observe(el); });
  })();

  /* ── FOOTER YEAR ─────────────────────────────────────── */
  $$('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
