/* علمِ تجوید — مشترکہ اسکرپٹ: تھیم، فونٹ، مینو، تلاش */
(function () {
  'use strict';
  var root = document.documentElement;
  var $ = function (s) { return document.querySelector(s); };
  var safe = function (fn) { try { return fn(); } catch (e) {} };

  /* تھیم */
  $('#themeBtn').addEventListener('click', function () {
    var cur = root.getAttribute('data-theme');
    if (!cur) cur = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    var next = cur === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    safe(function () { localStorage.setItem('theme', next); });
  });

  /* فونٹ سائز */
  function setFs(delta) {
    var cur = parseFloat(getComputedStyle(root).getPropertyValue('--fs')) || 19;
    var n = Math.min(28, Math.max(14, cur + delta));
    root.style.setProperty('--fs', n + 'px');
    safe(function () { localStorage.setItem('fs', n); });
  }
  $('#fsUp').addEventListener('click', function () { setFs(1.5); });
  $('#fsDown').addEventListener('click', function () { setFs(-1.5); });

  /* مینو (موبائل) */
  var menuBtn = $('#menuBtn'), scrim = $('#scrim');
  function nav(open) {
    document.body.classList.toggle('nav-open', open);
    scrim.hidden = !open;
    menuBtn.setAttribute('aria-expanded', open);
  }
  menuBtn.addEventListener('click', function () { nav(!document.body.classList.contains('nav-open')); });
  scrim.addEventListener('click', function () { nav(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { nav(false); hideResults(); } });
  var active = document.querySelector('.sidebar a.active');
  if (active && active.scrollIntoView) safe(function () { active.scrollIntoView({ block: 'center' }); });

  /* تلاش */
  var DIAC = /[ؐ-ًؚ-ٰٟۖ-ۭـ]/g;
  function norm(s) {
    return s.replace(DIAC, '').replace(/[أإآٱ]/g, 'ا').replace(/[يىې]/g, 'ی').replace(/ك/g, 'ک')
      .replace(/[ہۃة]/g, 'ه').toLowerCase();
  }
  var q = $('#q'), box = $('#results'), idx = null, loading = false;
  function hideResults() { box.hidden = true; }
  function load(cb) {
    if (idx) return cb();
    if (loading) return;
    loading = true;
    fetch('assets/search-index.json').then(function (r) { return r.json(); }).then(function (d) { idx = d; cb(); })
      .catch(function () { box.hidden = false; box.innerHTML = '<a>تلاش کی فہرست لوڈ نہیں ہو سکی۔</a>'; loading = false; });
  }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function run() {
    var term = norm(q.value.trim());
    if (term.length < 2 && !/^[؀-ۿ]$/.test(term)) { hideResults(); return; }
    if (!term) { hideResults(); return; }
    var words = term.split(/\s+/);
    var hits = [];
    idx.forEach(function (p) {
      var score = 0, hay = norm(p.t) + ' ' + p.x;
      for (var i = 0; i < words.length; i++) {
        var w = words[i];
        if (!hay.includes(w)) { score = -1; break; }
        if (norm(p.t).includes(w)) score += 10;
        score += Math.min(5, hay.split(w).length - 1);
      }
      if (score > 0) hits.push({ p: p, s: score });
    });
    hits.sort(function (a, b) { return b.s - a.s; });
    box.hidden = false;
    if (!hits.length) { box.innerHTML = '<a>کوئی نتیجہ نہیں ملا</a>'; return; }
    box.innerHTML = hits.slice(0, 8).map(function (h) {
      var plain = h.p.r, n = norm(plain), at = n.indexOf(words[0]);
      var snip = at > 40 ? '…' + plain.slice(Math.max(0, at - 30), at + 110) : plain.slice(0, 140);
      return '<a href="' + h.p.u + '"><b>' + esc(h.p.t) + '</b><small>' + esc(snip) + '</small></a>';
    }).join('');
  }
  q.addEventListener('input', function () { load(run); });
  q.addEventListener('focus', function () { if (q.value) load(run); });
  document.addEventListener('click', function (e) { if (!e.target.closest('.search')) hideResults(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) { e.preventDefault(); q.focus(); }
  });
})();
