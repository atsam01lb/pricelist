/* SKNFORCE price list — tab highlighting, share, scroll animation, price count-up. */
(function () {
  'use strict';

  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;

  // ---- Tabs: highlight the category in view ----
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.tab'));
  var byId = {};
  tabs.forEach(function (t) { byId[t.getAttribute('data-target')] = t; });

  function setActive(id) {
    tabs.forEach(function (t) {
      var on = t.getAttribute('data-target') === id;
      t.classList.toggle('is-active', on);
      if (on) t.setAttribute('aria-current', 'true'); else t.removeAttribute('aria-current');
    });
    var active = byId[id];
    var strip = active && active.parentNode;
    if (strip && strip.scrollWidth > strip.clientWidth) {
      strip.scrollTo({ left: active.offsetLeft - 20, behavior: 'smooth' });
    }
  }

  if (hasIO) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) setActive(en.target.id); });
    }, { rootMargin: '-30% 0px -60% 0px' });
    document.querySelectorAll('.cat').forEach(function (s) { spy.observe(s); });
  }

  // ---- Share: Web Share API, copy-link fallback ----
  var toast = document.getElementById('toast');
  var toastTimer;
  function say(msg) {
    toast.textContent = msg;
    toast.classList.add('is-on');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.classList.remove('is-on'); }, 2400);
  }
  function legacyCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly', '');
    ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
    return ok;
  }
  function copyFallback(url) {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(url).then(function () { say('Link copied'); },
        function () { say(legacyCopy(url) ? 'Link copied' : url); });
    } else {
      say(legacyCopy(url) ? 'Link copied' : url);
    }
  }
  var shareBtn = document.getElementById('shareBtn');
  if (shareBtn) {
    shareBtn.addEventListener('click', function () {
      var canonical = document.querySelector('link[rel="canonical"]');
      var url = canonical ? canonical.href : location.href;
      var data = {
        title: 'SKNFORCE | Home & Hotel Grooming Services',
        text: 'SKNFORCE price list: home & hotel grooming services.',
        url: url
      };
      if (navigator.share) {
        navigator.share(data).catch(function (err) {
          if (err && err.name === 'AbortError') return; // user closed the sheet
          copyFallback(url);
        });
      } else {
        copyFallback(url);
      }
    });
  }

  // ---- Scroll progress bar ----
  var bar = document.getElementById('progress');
  if (bar && !reduce) {
    var ticking = false;
    var update = function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(window.scrollY / h, 1) : 0) + ')';
      ticking = false;
    };
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  // ---- Price count-up (final text stays in the HTML for SEO; animation is cosmetic) ----
  function countUp(el) {
    var final = el.textContent;
    var target = parseFloat(final.replace(/[^0-9.]/g, ''));
    if (!isFinite(target)) return;
    var dur = 1100, start = null;
    el.classList.add('is-counting');
    function frame(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = '$' + (target * eased).toFixed(2);
      if (p < 1) requestAnimationFrame(frame);
      else { el.textContent = final; el.classList.remove('is-counting'); }
    }
    requestAnimationFrame(frame);
  }

  // ---- Reveal on scroll (progressive: everything is visible without JS) ----
  if (!hasIO || reduce) return;
  document.documentElement.classList.add('js');

  document.querySelectorAll('.cat').forEach(function (cat) {
    cat.querySelectorAll('.row').forEach(function (row, i) { row.style.setProperty('--i', i); });
  });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      var el = en.target;
      el.classList.add('is-in');
      io.unobserve(el);
      if (el.classList.contains('cat')) {
        el.querySelectorAll('.row').forEach(function (row, i) {
          setTimeout(function () { countUp(row.querySelector('.price')); }, 350 + i * 70);
        });
      }
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });

  document.querySelectorAll('.cat, .book-card, .site-footer').forEach(function (el) { io.observe(el); });
})();
