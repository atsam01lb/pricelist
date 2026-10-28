/* SKNFORCE price list — tiny helper script: tab highlighting, share, reveal. */
(function () {
  'use strict';

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

  if ('IntersectionObserver' in window) {
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
  function copyFallback(url) {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(url).then(function () { say('Link copied'); },
        function () { say(legacyCopy(url) ? 'Link copied' : url); });
    } else {
      say(legacyCopy(url) ? 'Link copied' : url);
    }
  }

  // ---- Minimal reveal-on-scroll (progressive: content is visible without JS) ----
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    document.documentElement.classList.add('js');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    items.forEach(function (el) { io.observe(el); });
  }
})();
