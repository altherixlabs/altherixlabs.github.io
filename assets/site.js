/* Altherix — shared behaviour. Small, dependency-free, every block defensive. */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  root.classList.remove('no-js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Sticky nav: compact + blurred after scrolling */
  var nav = d.querySelector('.nav');
  if (nav) {
    var onScroll = function () { nav.classList.toggle('scrolled', window.scrollY > 24); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* Mobile menu */
  var btn = d.querySelector('.menu-btn'), menu = d.getElementById('mobile-menu');
  if (btn && menu) {
    var setOpen = function (open) {
      d.body.classList.toggle('menu-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      menu.toggleAttribute('inert', !open);
      if (open) { var f = menu.querySelector('a'); if (f) f.focus(); }
    };
    menu.setAttribute('inert', '');
    btn.addEventListener('click', function () { setOpen(!d.body.classList.contains('menu-open')); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    d.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && d.body.classList.contains('menu-open')) { setOpen(false); btn.focus(); }
    });
    window.matchMedia('(min-width:1080px)').addEventListener('change', function (m) { if (m.matches) setOpen(false); });
  }

  /* Reveal on scroll */
  var items = d.querySelectorAll('.rv');
  if (reduce || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    items.forEach(function (el) { io.observe(el); });
  }

  /* Pause SVG animation when hero is off-screen (saves battery on phones) */
  var viz = d.querySelector('.hero-viz svg');
  if (viz && 'IntersectionObserver' in window && viz.pauseAnimations) {
    new IntersectionObserver(function (e) {
      e[0].isIntersecting ? viz.unpauseAnimations() : viz.pauseAnimations();
    }).observe(viz);
  }

  /* Contact form → opens the visitor's mail client, addressed to contact@altherix.in */
  var form = d.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var v = function (n) { return (form.elements[n] && form.elements[n].value || '').trim(); };
      var subject = 'Project enquiry' + (v('topic') ? ' — ' + v('topic') : '') + (v('company') ? ' (' + v('company') + ')' : '');
      var body = 'Name: ' + v('name') + '\nEmail: ' + v('email') + (v('company') ? '\nCompany: ' + v('company') : '') +
                 (v('topic') ? '\nArea: ' + v('topic') : '') + '\n\n' + v('message');
      window.location.href = 'mailto:contact@altherix.in?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      var ok = d.getElementById('form-ok');
      if (ok) ok.textContent = 'Your email app should open with the message ready to send. If it doesn’t, write to contact@altherix.in.';
    });
  }

  /* Year */
  d.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
