"""tools/data/jazariyya_raw.txt سے content/jazariyya.html بناتا ہے۔"""
import html, re
from pathlib import Path
R = Path(__file__).parent.parent
rows, out, n = [], [], 0
for line in (R/"tools/data/jazariyya_raw.txt").read_text(encoding="utf-8").splitlines():
    if line.startswith("## "):
        out.append(f'<div class="bab">{html.escape(line[3:])}</div>')
        continue
    m = re.match(r"(\d+) - (.+?) … (.+)$", line)
    assert m, line
    no, a, b = int(m[1]), m[2], m[3]
    n += 1; assert no == n, (no, n)
    out.append(f'<div class="verse" data-n="{no}"><span class="no">{no}</span>'
               f'<span class="h ar">{html.escape(a)}</span><span class="h ar">{html.escape(b)}</span></div>')
assert n == 107
head = '''<h1>المقدمۃ الجزریہ (متن)</h1>
<p class="lead">امام ابنِ الجزریؒ (م ۸۳۳ھ) کی مشہور منظومہ «المقدمۃ فیما علی قارئ القرآن أن یعلمہ» کے ۱۰۷ ابیات۔ حفظ اور دہرائی کے لیے نیچے سے مصرعے چھپائے جا سکتے ہیں۔</p>
<div class="panel" id="jzTools" style="font-size:.9rem">
  <button type="button" class="btn-sm" data-mode="all">سب دکھائیں</button>
  <button type="button" class="btn-sm" data-mode="second">دوسرا مصرع چھپائیں</button>
  <button type="button" class="btn-sm" data-mode="both">دونوں چھپائیں</button>
  <span class="note" style="margin:8px 0 0;display:block">کسی مصرع پر کلک کر کے اسے دکھائیں/چھپائیں۔</span>
</div>
<noscript><div class="note">چھپانے کی سہولت کے لیے جاوا اسکرپٹ درکار ہے؛ متن اس کے بغیر بھی پڑھا جا سکتا ہے۔</div></noscript>
<div id="jzText">
'''
tail = '''</div>
<div class="note"><b>متن کے بارے میں:</b> یہ متن شاملہ پر موجود د. عبدالمحسن القاسم کی تحقیق (مخطوطات پر مبنی، مصنف پر پڑھے گئے نسخوں کے ساتھ) سے لیا گیا ہے۔ چند کلمات میں نسخوں کا معمولی اختلاف ہے (مثلاً بیت ۲۷ میں «یصحح»، بیت ۷۸ میں «وَجَبْ»)؛ مثبت صورت محقق کی ترجیح کے مطابق ہے۔ بیت ۱ سے ۱۰۷ تک کی تقسیم اور عنوانات بھی اسی نسخے کے مطابق ہیں (۱۰۴–۱۰۵ اور ۱۰۶–۱۰۷ کے عنوانات محقق نے شامل کیے ہیں)۔</div>
<div class="src"><b>ماخذ:</b> المقدمۃ الجزریۃ، تحقیق: د. عبدالمحسن بن محمد القاسم (متونِ طالب العلم، المتون الإضافیۃ ۳)، المکتبۃ الشاملہ۔</div>
'''
(R/"content/jazariyya.html").write_text(head + "\n".join(out) + "\n" + tail, encoding="utf-8")
print("ok", n)
