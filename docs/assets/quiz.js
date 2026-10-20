(function () {
  'use strict';
  var all = window.QUIZ || [];
  var $ = function (id) { return document.getElementById(id); };
  var cat = $('qCat'), box = $('qBox');
  var cats = [];
  all.forEach(function (q) { if (cats.indexOf(q.c) === -1) cats.push(q.c); });
  cat.innerHTML = '<option value="">تمام ابواب (' + all.length + ')</option>' + cats.map(function (c) {
    return '<option>' + c + '</option>';
  }).join('');

  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }

  var list, i, score, wrong;
  function start() {
    var pool = all.filter(function (q) { return !cat.value || q.c === cat.value; });
    list = shuffle(pool); i = 0; score = 0; wrong = [];
    box.style.display = 'block';
    next();
  }
  function next() {
    if (i >= list.length) return end();
    var q = list[i];
    var opts = shuffle(q.o.map(function (t, k) { return { t: t, ok: k === q.a }; }));
    box.innerHTML = '<p class="note">سوال ' + (i + 1) + ' / ' + list.length + ' — ' + q.c + '</p><p style="font-size:1.1em"><b></b></p><div></div><div class="fb"></div>';
    box.querySelector('b').textContent = q.q;
    var wrap = box.children[2], fb = box.children[3];
    opts.forEach(function (o) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'opt'; b.textContent = o.t;
      b.addEventListener('click', function () {
        Array.prototype.forEach.call(wrap.children, function (x, k) { x.disabled = true; if (opts[k].ok) x.classList.add('ok'); });
        if (o.ok) score++; else { b.classList.add('bad'); wrong.push(q); }
        fb.innerHTML = '<div class="' + (o.ok ? 'tip' : 'warn') + '"></div><p><button type="button" class="btn-sm primary">' + (i + 1 < list.length ? 'اگلا سوال' : 'نتیجہ') + '</button></p>';
        fb.firstChild.textContent = (o.ok ? 'درست۔ ' : 'غلط۔ ') + q.e;
        fb.querySelector('button').addEventListener('click', function () { i++; next(); });
      });
      wrap.appendChild(b);
    });
  }
  function end() {
    var pct = list.length ? Math.round(score * 100 / list.length) : 0;
    box.innerHTML = '<h2>نتیجہ: ' + score + ' / ' + list.length + ' (' + pct + '٪)</h2>';
    if (wrong.length) {
      var h = '<p>یہ سوالات دوبارہ دیکھیں:</p><ul>';
      wrong.forEach(function (q) { h += '<li></li>'; });
      box.insertAdjacentHTML('beforeend', h + '</ul>');
      var lis = box.querySelectorAll('li');
      wrong.forEach(function (q, k) { lis[k].textContent = q.q + ' — ' + q.o[q.a]; });
    }
    box.insertAdjacentHTML('beforeend', '<p><button class="btn-sm primary" type="button" id="again">دوبارہ</button></p>');
    $('again').addEventListener('click', start);
  }
  $('qStart').addEventListener('click', start);
})();
