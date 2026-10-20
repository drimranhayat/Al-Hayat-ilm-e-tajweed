(function () {
  'use strict';
  var verses = document.querySelectorAll('#jzText .h');
  function mode(m) {
    Array.prototype.forEach.call(document.querySelectorAll('#jzText .verse'), function (v) {
      var hs = v.querySelectorAll('.h');
      hs[0].style.filter = m === 'both' ? 'blur(7px)' : '';
      hs[1].style.filter = (m === 'both' || m === 'second') ? 'blur(7px)' : '';
      Array.prototype.forEach.call(hs, function (h) { h.classList.remove('rev'); });
    });
  }
  Array.prototype.forEach.call(verses, function (h) {
    h.style.cursor = 'pointer';
    h.addEventListener('click', function () { h.classList.toggle('rev'); });
  });
  Array.prototype.forEach.call(document.querySelectorAll('#jzTools [data-mode]'), function (b) {
    b.addEventListener('click', function () { mode(b.getAttribute('data-mode')); });
  });
})();
