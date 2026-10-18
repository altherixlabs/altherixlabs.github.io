/* Altherix — shared behaviour. Small, dependency-free, every block defensive. */
(function () {
  'use strict';
  var d = document, root = d.documentElement, w = window;
  var reduce = w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var EASE = 'cubic-bezier(.2,.7,.2,1)';

  /* iOS Safari only applies :active (press feedback) when a touch listener exists. */
  d.addEventListener('touchstart', function () {}, { passive: true });

  /* ── Reveal on scroll ─────────────────────────────────────────────
     Anything already on screen is shown immediately (no fade, no flash).
     After an in-page jump, the destination appears instantly too —
     only content you scroll into naturally fades up. */
  /* Lists reveal item by item: move the reveal from the container to its
     children, and give each child a sequence index (capped so long lists
     don't drag). The architecture list keeps its container reveal so its
     connecting line can draw. */
  ['.outcomes', '.grid2', '.layers', '.steps', '.kv', '.metrics', '.facts-dl', '.cols4',
   '.ind-grid', '.rows', '.cs-list', '.roles', '.plist', '.arch-flow', '.fit-grid'].forEach(function (sel) {
    d.querySelectorAll(sel).forEach(function (g) {
      if (g.closest('.page-hero') || g.closest('.hero')) return;
      var kids = [].slice.call(g.children);
      if (g.classList.contains('rv')) {
        if (!g.classList.contains('layers')) g.classList.remove('rv');
        kids.forEach(function (c) { c.classList.add('rv'); });
      }
      kids.filter(function (c) { return c.classList.contains('rv'); })
          .forEach(function (c, i) { c.style.setProperty('--i', Math.min(i, 6)); });
    });
  });

  var items = [].slice.call(d.querySelectorAll('.rv'));
  var jumping = !!location.hash, jumpTimer;
  function markJump() {
    jumping = true; clearTimeout(jumpTimer);
    jumpTimer = setTimeout(function () { jumping = false; }, 1200);
  }
  if (jumping) markJump();
  d.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href*="#"]');
    if (a && a.pathname === location.pathname && a.hash) markJump();
  });
  w.addEventListener('hashchange', markJump);

  function inView(el) {
    var r = el.getBoundingClientRect();
    return r.top < w.innerHeight && r.bottom > 0;
  }
  if (reduce || !('IntersectionObserver' in w)) {
    items.forEach(function (el) { el.classList.add('in', 'instant'); });
  } else {
    items.forEach(function (el) { if (inView(el)) el.classList.add('in', 'instant'); });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        if (jumping) en.target.classList.add('instant');
        en.target.classList.add('in');
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.04 });
    items.forEach(function (el) { if (!el.classList.contains('in')) io.observe(el); });
  }
  root.classList.remove('no-js');
  root.classList.add('js');

  /* ── Figures count up once when they come into view ── */
  var figs = [].slice.call(d.querySelectorAll('.outcome .n, .cs-big, .metrics b, .cs-sub b'));
  if (!reduce && 'IntersectionObserver' in w && w.requestAnimationFrame) {
    var countUp = function (el) {
      var text = el.textContent.trim(), m = text.match(/^(\d+)(\D*)$/);
      if (!m || +m[1] < 2) return;
      var end = +m[1], start = null, dur = 1100;
      el.setAttribute('aria-label', text);
      var step = function (now) {
        if (start === null) start = now;
        var p = Math.min(1, (now - start) / dur), e = 1 - Math.pow(2, -10 * p); // ease-out-expo
        el.textContent = (p < 1 ? Math.round(end * e) : end) + m[2];
        if (p < 1) w.requestAnimationFrame(step); else el.removeAttribute('aria-label');
      };
      el.textContent = '0' + m[2];
      w.requestAnimationFrame(step);
    };
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        cio.unobserve(en.target);
        if (!jumping) countUp(en.target);
      });
    }, { threshold: 0.6 });
    figs.forEach(function (el) { cio.observe(el); });
  }

  /* ── Sticky nav: material appears once you scroll ── */
  var nav = d.querySelector('.nav');
  if (nav) {
    var ticking = false;
    var onScroll = function () {
      if (ticking) return; ticking = true;
      w.requestAnimationFrame(function () { nav.classList.toggle('scrolled', w.scrollY > 24); ticking = false; });
    };
    w.addEventListener('scroll', onScroll, { passive: true });
    nav.classList.toggle('scrolled', w.scrollY > 24);
  }

  /* ── Mobile menu ── */
  var btn = d.querySelector('.menu-btn'), menu = d.getElementById('mobile-menu');
  if (btn && menu) {
    var setOpen = function (open) {
      d.body.classList.toggle('menu-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      menu.toggleAttribute('inert', !open);
      if (open) { var f = menu.querySelector('a'); if (f) f.focus({ preventScroll: true }); }
    };
    menu.setAttribute('inert', '');
    btn.addEventListener('click', function () { setOpen(!d.body.classList.contains('menu-open')); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    d.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && d.body.classList.contains('menu-open')) { setOpen(false); btn.focus(); }
    });
    w.matchMedia('(min-width:1080px)').addEventListener('change', function (m) { if (m.matches) setOpen(false); });
  }

  /* ── Homepage scroll-spy: highlight the section you're reading ── */
  var spyLinks = [].slice.call(d.querySelectorAll('.nav-links a[href^="/#"]'));
  if (location.pathname === '/' && spyLinks.length && 'IntersectionObserver' in w) {
    var byId = {};
    spyLinks.forEach(function (a) { byId[a.hash.slice(1)] = a; });
    var visible = {};
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { visible[en.target.id] = en.isIntersecting; });
      var current = null;
      Object.keys(byId).forEach(function (id) { if (visible[id] && !current) current = id; });
      spyLinks.forEach(function (a) {
        var on = a.hash.slice(1) === current;
        a.classList.toggle('is-current', on);
        if (on) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current');
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(byId).forEach(function (id) { var s = d.getElementById(id); if (s) spy.observe(s); });
  }

  /* ── Pause looping animations while off-screen ── */
  if ('IntersectionObserver' in w) {
    d.querySelectorAll('.hero-viz').forEach(function (el) {
      new IntersectionObserver(function (e) { el.classList.toggle('paused', !e[0].isIntersecting); }).observe(el);
    });
  }

  /* ── Job listings: open and close smoothly; interruptible mid-way ── */
  d.querySelectorAll('details.role').forEach(function (det) {
    var summary = det.querySelector('summary'), body = det.querySelector('.role-body'), anim = null;
    if (!summary || !body || !body.animate) return;
    summary.addEventListener('click', function (e) {
      e.preventDefault();
      var opening = !det.open || det.dataset.closing === '1';
      // start from what's on screen now (a closed <details> reports its hidden content's size, so use 0)
      var from = det.open ? body.getBoundingClientRect().height : 0;
      if (anim) anim.cancel();
      if (opening) {
        det.dataset.closing = '';
        det.open = true;
        var to = body.scrollHeight;
        if (reduce) return;
        anim = body.animate([{ height: from + 'px', opacity: from ? 1 : 0 }, { height: to + 'px', opacity: 1 }],
                            { duration: 280, easing: EASE });
        anim.onfinish = function () { anim = null; };
      } else {
        if (reduce) { det.open = false; return; }
        det.dataset.closing = '1';
        anim = body.animate([{ height: from + 'px', opacity: 1 }, { height: '0px', opacity: 0 }],
                            { duration: 220, easing: EASE });
        anim.onfinish = function () { det.open = false; det.dataset.closing = ''; anim = null; };
      }
    });
  });

  /* ── Contact form: inline validation, pressed state, and a fallback ── */
  var form = d.getElementById('contact-form');
  if (form) {
    var msgs = {
      name: 'Please enter your name.',
      email: 'Please enter a valid email address.',
      message: 'Tell us a little about what you’re working on.'
    };
    var fields = ['name', 'email', 'message'].map(function (n) { return form.elements[n]; }).filter(Boolean);
    fields.forEach(function (f) {
      var err = d.createElement('p');
      err.className = 'field-err'; err.id = f.id + '-err'; err.setAttribute('aria-live', 'polite');
      f.insertAdjacentElement('afterend', err);
      f.setAttribute('aria-describedby', ((f.getAttribute('aria-describedby') || '') + ' ' + err.id).trim());
      f.addEventListener('blur', function () { if (f.value.trim() || f.dataset.touched) check(f); f.dataset.touched = '1'; });
      f.addEventListener('input', function () { if (f.getAttribute('aria-invalid') === 'true') check(f); });
    });
    function check(f) {
      var bad = !f.value.trim() || !f.checkValidity();
      f.setAttribute('aria-invalid', bad ? 'true' : 'false');
      d.getElementById(f.id + '-err').textContent = bad ? msgs[f.name] : '';
      return !bad;
    }

    var submit = form.querySelector('button[type="submit"]');
    var label = submit ? submit.textContent : '';
    var ok = d.getElementById('form-ok');
    var fb = d.createElement('div');
    fb.className = 'form-fallback'; fb.hidden = true;
    fb.innerHTML = '<p class="meta">No email app opened? Copy your message and send it to <a href="mailto:contact@altherix.in">contact@altherix.in</a>.</p>' +
                   '<div class="btns"><button type="button" class="btn btn-s" data-copy>Copy message</button></div>';
    form.appendChild(fb);
    var composed = '';
    fb.querySelector('[data-copy]').addEventListener('click', function (e) {
      var b = e.currentTarget;
      var done = function (t) { b.textContent = t; setTimeout(function () { b.textContent = 'Copy message'; }, 2000); };
      if (navigator.clipboard) navigator.clipboard.writeText(composed).then(function () { done('Copied'); }, function () { done('Copy failed — select and copy manually'); });
      else done('Copy not supported');
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var firstBad = null;
      fields.forEach(function (f) { f.dataset.touched = '1'; if (!check(f) && !firstBad) firstBad = f; });
      if (firstBad) { firstBad.focus(); return; }
      var v = function (n) { return (form.elements[n] && form.elements[n].value || '').trim(); };
      var subject = 'Project enquiry' + (v('topic') ? ' — ' + v('topic') : '') + (v('company') ? ' (' + v('company') + ')' : '');
      var bodyText = 'Name: ' + v('name') + '\nEmail: ' + v('email') + (v('company') ? '\nCompany: ' + v('company') : '') +
                     (v('topic') ? '\nArea: ' + v('topic') : '') + '\n\n' + v('message');
      composed = 'To: contact@altherix.in\nSubject: ' + subject + '\n\n' + bodyText;
      if (submit) { submit.setAttribute('aria-busy', 'true'); submit.textContent = 'Opening your email app…'; }
      w.location.href = 'mailto:contact@altherix.in?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(bodyText);
      setTimeout(function () {
        if (submit) { submit.removeAttribute('aria-busy'); submit.textContent = label; }
        if (ok) ok.textContent = 'Your message is ready in your email app — press send there.';
        fb.hidden = false;
      }, 900);
    });
  }

  /* ── Footer line draws in when the footer is reached ── */
  var foot = d.querySelector('.foot');
  if (foot) {
    if (reduce || !('IntersectionObserver' in w)) foot.classList.add('in');
    else {
      var fio = new IntersectionObserver(function (e) { if (e[0].isIntersecting) { foot.classList.add('in'); fio.disconnect(); } }, { threshold: 0.2 });
      fio.observe(foot);
    }
  }

  /* ── Hero glow follows the pointer (desktop, motion allowed) ── */
  var hero = d.querySelector('.hero');
  if (hero && !reduce && w.matchMedia('(hover:hover) and (pointer:fine)').matches) {
    var raf = 0, gx = 0, gy = 0;
    hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect();
      gx = e.clientX - r.left; gy = e.clientY - r.top;
      if (!raf) raf = w.requestAnimationFrame(function () {
        hero.style.setProperty('--gx', gx + 'px'); hero.style.setProperty('--gy', gy + 'px'); raf = 0;
      });
      hero.classList.add('glow-on');
    });
    hero.addEventListener('pointerleave', function () { hero.classList.remove('glow-on'); });
  }

  /* ── Case studies: reading progress and live table of contents ── */
  var bar = d.querySelector('.read-progress'), article = d.querySelector('.article');
  if (bar && article) {
    var pticking = false;
    var progress = function () {
      var r = article.getBoundingClientRect(), total = r.height - w.innerHeight * 0.6;
      var p = Math.max(0, Math.min(1, -r.top / Math.max(1, total)));
      bar.style.setProperty('--p', p.toFixed(4)); pticking = false;
    };
    w.addEventListener('scroll', function () { if (!pticking) { pticking = true; w.requestAnimationFrame(progress); } }, { passive: true });
    progress();
  }
  var tocLinks = [].slice.call(d.querySelectorAll('.toc a'));
  if (tocLinks.length && 'IntersectionObserver' in w) {
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        tocLinks.forEach(function (a) {
          var on = a.hash.slice(1) === en.target.id;
          a.classList.toggle('is-current', on);
          if (on) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    tocLinks.forEach(function (a) { var t = d.getElementById(a.hash.slice(1)); if (t) tio.observe(t); });
  }

  /* ── Year ── */
  d.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
