/* حروف کا مطالعہ: گرڈ، صفت کے فلٹر، تفصیل اور تصدیقی گنتی */
(function () {
  'use strict';
  var T = window.TAJ;
  var $ = function (s) { return document.getElementById(s); };
  var esc = function (s) { return String(s).replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); };

  var FILTERS = [
    ['ہمس', 'hams'], ['شدت', 'shiddah'], ['توسط', 'tawassut'], ['استعلاء', 'istila'],
    ['اطباق', 'itbaq'], ['اذلاق', 'izlaq'], ['قلقلہ', 'qalqala'], ['صفیر', 'safir'],
    ['لین', 'lin'], ['انحراف', 'inhiraf'], ['تکرار', 'takrir'], ['تفشی', 'tafashshi'],
    ['استطالت', 'istitala'], ['غنہ', 'ghunna']
  ];
  var current = null, sel = null;

  function inSet(key, ch) { return T.SETS[key].indexOf(ch) !== -1; }

  var grid = $('grid');
  T.LETTERS.forEach(function (l) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'btn-sm'; b.dataset.ch = l[0];
    b.style.cssText = 'font-size:1.9rem;min-width:3.2rem;padding:4px 10px;font-family:var(--ar,inherit)';
    b.textContent = l[0];
    b.setAttribute('aria-label', l[1]);
    b.addEventListener('click', function () { show(l); });
    grid.appendChild(b);
  });

  var fbox = $('filters');
  FILTERS.forEach(function (f) {
    var b = document.createElement('button');
    b.type = "button"; b.style.fontSize = ".95rem"; b.className = "chip"; b.textContent = f[0];
    b.addEventListener('click', function () {
      current = current === f[1] ? null : f[1];
      Array.prototype.forEach.call(fbox.children, function (c) { c.classList.remove('gold'); });
      if (current) b.classList.add('gold');
      applyFilter(f);
    });
    fbox.appendChild(b);
  });

  function applyFilter(f) {
    var note = $('filterNote'), n = 0;
    Array.prototype.forEach.call(grid.children, function (b) {
      var on = !current || inSet(current, b.dataset.ch);
      b.style.opacity = on ? '1' : '.25';
      if (current && on) { b.style.borderColor = 'var(--gold)'; b.style.background = 'var(--gold-soft)'; n++; }
      else { b.style.borderColor = ''; b.style.background = ''; }
    });
    if (!current) { note.style.display = 'none'; return; }
    var m = T.MNEMONIC[f[0]];
    note.style.display = 'block';
    note.innerHTML = '<b>' + esc(f[0]) + '</b>: ' + n + ' حروف' + (m ? ' — یادداشت: <span class="ar">' + esc(m) + '</span>' : '');
  }

  function show(l) {
    var ch = l[0], mk = T.MAKHARIJ[l[2]], s = T.sifat(ch);
    Array.prototype.forEach.call(grid.children, function (b) { b.style.outline = b.dataset.ch === ch ? '2px solid var(--green)' : ''; });
    var h = '<div style="display:flex;gap:18px;align-items:center;flex-wrap:wrap">' +
      '<span class="ar-lg" style="font-size:4rem;color:var(--green)">' + esc(ch) + '</span>' +
      '<div><b style="font-size:1.2em">' + esc(l[1]) + '</b><br>مخرج نمبر ' + l[2] + ': ' + esc(mk.name) + ' <span class="tag">' + esc(mk.maqam) + '</span></div></div>' +
      '<p>' + esc(mk.desc) + '</p><p><b>ضدّی صفات:</b> ' +
      s.main.map(function (x) { return '<span class="tag ' + (T.QAWI.indexOf(x) !== -1 ? 't-strong' : 't-weak') + '">' + esc(x) + '</span>'; }).join('') + '</p>';
    if (s.extra.length) h += '<p><b>غیر ضدّی صفات:</b> ' + s.extra.map(function (x) { return '<span class="tag t-sp">' + esc(x) + '</span>'; }).join('') + '</p>';
    if (T.TIPS[ch]) h += '<div class="tip">' + esc(T.TIPS[ch]) + '</div>';
    $('detail').innerHTML = h;
  }

  /* تصدیقی گنتی (کتب کے مطابق) */
  var c = T.counts();
  var want = { hams: 10, jahr: 19, shiddah: 8, tawassut: 5, rakhawa: 16, istila: 7, istifal: 22, itbaq: 4, infitah: 25, izlaq: 6, ismat: 23 };
  var names = { hams: 'ہمس', jahr: 'جہر', shiddah: 'شدت', tawassut: 'توسط', rakhawa: 'رخاوت', istila: 'استعلاء', istifal: 'استفال', itbaq: 'اطباق', infitah: 'انفتاح', izlaq: 'اذلاق', ismat: 'اصمات' };
  var out = '<table><tr><th>صفت</th><th>شمار شدہ</th><th>کتب میں</th><th></th></tr>';
  Object.keys(want).forEach(function (k) {
    var ok = c[k] === want[k];
    out += '<tr><td>' + names[k] + '</td><td>' + c[k] + '</td><td>' + want[k] + '</td><td>' + (ok ? '✔' : '✘') + '</td></tr>';
  });
  $('counts').innerHTML = out + '</table>';
})();
