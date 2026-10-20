(function () {
  var tabs = [].slice.call(document.querySelectorAll('.ptab'));
  if (!tabs.length) return;
  var map = { art: 'tb-art', qa: 'tb-qa', mcq: 'tb-mcq' };
  function show(key, noHash) {
    tabs.forEach(function (t) {
      var on = t.id === map[key];
      t.setAttribute('aria-selected', on);
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
    try { if (!noHash && key !== 'art') history.replaceState(null, '', '#tab-' + key); } catch (e) {}
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { show(t.id.slice(3)); });
    t.addEventListener('keydown', function (e) {
      var d = e.key === 'ArrowLeft' ? 1 : e.key === 'ArrowRight' ? -1 : 0; // RTL
      if (!d) return;
      var n = tabs[(i + d + tabs.length) % tabs.length]; n.focus(); show(n.id.slice(3));
    });
  });
  // hash: #tab-qa / #tab-mcq, or an anchor inside the articles panel
  var h = location.hash.slice(1);
  if (h === 'tab-qa') show('qa', true); else if (h === 'tab-mcq') show('mcq', true);
  else show('art', true);
  // MCQ
  var qs = [].slice.call(document.querySelectorAll('.mcq')), done = 0, ok = 0;
  qs.forEach(function (q) {
    var a = +q.dataset.a, opts = [].slice.call(q.querySelectorAll('.opt'));
    opts.forEach(function (b) {
      b.addEventListener('click', function () {
        if (q.classList.contains('answered')) return;
        q.classList.add('answered');
        var i = +b.dataset.i; done++; if (i === a) ok++;
        opts.forEach(function (o, j) {
          o.disabled = true;
          if (j === a) { o.classList.add('right'); o.insertAdjacentHTML('beforeend', '<span class="mk">✔ درست</span>'); }
          else if (j === i) { o.classList.add('wrong'); o.insertAdjacentHTML('beforeend', '<span class="mk">✘ غلط</span>'); }
        });
        q.querySelector('.expl').hidden = false;
        if (done === qs.length) {
          var s = document.querySelector('.mcq-score');
          s.hidden = false; s.textContent = 'آپ کا نتیجہ: ' + ok + ' / ' + qs.length;
        }
      });
    });
  });
  // in-page anchors that live in the articles panel
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (a && !/^#tab-/.test(a.getAttribute('href'))) show('art', true);
  });
})();
