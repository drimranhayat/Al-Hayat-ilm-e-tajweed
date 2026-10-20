from dg_common import *

# ---------- ۱۔ پانچ مقامات اور سترہ مخارج ----------
def maqamat():
    W, H = 900, 520
    b = [text(450, 28, "پانچ مقامات اور سترہ مخارج", "dg-t")]
    b.append(box(350, 44, 200, 46, ["۱۷ مخارج"], "g", "dg-t"))
    # دائیں سے بائیں: جوف، حلق، لسان، شفتان، خیشوم
    cols = [  # (عنوان, تعداد, بایاں کنارہ x, چوڑائی, قطاریں)
        ("جوف", "۱ مخرج", 780, 100, [("ا  و  ی", 1)]),
        ("حلق", "۳ مخارج", 650, 110, [("ء  ہ", 2), ("ع  ح", 3), ("غ  خ", 4)]),
        ("لسان", "۱۰ مخارج", 270, 360, [("ق", 5), ("ک", 6), ("ج ش ی", 7), ("ض", 8), ("ل", 9), ("ن", 10), ("ر", 11), ("ط د ت", 12), ("ص ز س", 13), ("ظ ذ ث", 14)]),
        ("شفتان", "۲ مخرج", 140, 110, [("ف", 15), ("ب م و", 16)]),
        ("خیشوم", "۱ مخرج", 20, 100, [("غنہ", 17)]),
    ]
    for name, cnt, x, w, rows in cols:
        b.append(arrow(450, 90, x + w/2, 128))
        b.append(box(x, 130, w, 56, [name, (cnt, "dg-s")], "y"))
        if name == "لسان":
            cw = (w - 12) / 2
            for i, (l, n) in enumerate(rows):
                col, row = divmod(i, 5)
                bx = x + w - cw*(col+1) - 12*col
                by = 210 + row*54
                b.append(f'<rect class="dg-box" x="{bx}" y="{by}" width="{cw}" height="46" rx="10"/>')
                b.append(num(n, bx+cw-18, by+23, "", r=11))
                b.append(ar(bx+(cw-30)/2, by+33, l, cls="dg-ar-s"))
        else:
            for i, (l, n) in enumerate(rows):
                by = 210 + i*54
                b.append(f'<rect class="dg-box" x="{x}" y="{by}" width="{w}" height="46" rx="10"/>')
                b.append(num(n, x+w-18, by+23, "", r=11))
                b.append(ar(x+(w-30)/2, by+33, l, cls="dg-ar-s"))
    b.append(text(450, 500, "حساب: ۱ + ۳ + ۱۰ + ۲ + ۱ = ۱۷   (مآخذ: ابنِ جزری، النشر؛ خلیل بن احمد کا قول)", "dg-s"))
    write("maqamat", svg(W, H, "".join(b), "پانچ مقامات اور سترہ مخارج"))
maqamat()

# ---------- ۲۔ شدت، توسط، رخاوت ----------
def shidda():
    W, H = 900, 330
    b = [text(450, 28, "شدت — توسط — رخاوت: آواز مخرج پر کتنی رکتی ہے", "dg-t")]
    zones = [
      ("شدت", "آواز رک جاتی ہے", "أجد قط بكت", "ء  ج  د  ق  ط  ب  ک  ت", "۸ حروف", "r", 600, 280),
      ("توسط", "نہ پوری رکتی، نہ پوری جاری", "لن عمر", "ل  ن  ع  م  ر", "۵ حروف", "y", 400, 190),
      ("رخاوت", "آواز جاری رہتی ہے", "باقی حروف", "ا ث ح خ ذ ز س ش ص ض ظ غ ف ہ و ی", "۱۶ حروف", "b", 120, 260),
    ]
    xs = (620, 400, 40)
    ws = (240, 200, 340)
    b.append('<defs><linearGradient id="gSh" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="var(--red)"/><stop offset=".5" stop-color="var(--gold)"/><stop offset="1" stop-color="var(--blue)"/></linearGradient></defs>')
    b.append('<rect x="40" y="52" width="820" height="16" rx="8" fill="url(#gSh)" opacity=".85"/>')
    b.append(text(850, 90, "بند", "dg-s")); b.append(text(50, 90, "جاری", "dg-s"))
    for (name, d, mn, letters, cnt, cls, _, _), x, w in zip(zones, xs, ws):
        b.append(box(x, 108, w, 190, [], cls))
        b.append(text(x+w/2, 138, name, "dg-t"))
        b.append(text(x+w/2, 162, d, "dg-s"))
        b.append(ar(x+w/2, 200, mn if mn != "باقی حروف" else "", cls="dg-ar-s"))
        b.append(ar(x+w/2, 252, letters, cls="dg-ar-s"))
        b.append(text(x+w/2, 282, cnt, "dg-s"))
    b.append(text(450, 322, "۸ + ۵ + ۱۶ = ۲۹ حروف", "dg-s"))
    write("shidda-spectrum", svg(W, H, "".join(b), "شدت، توسط اور رخاوت"))
shidda()

# ---------- ۳۔ پانچ ضدّی جوڑے ----------
def pairs():
    W, H = 900, 460
    b = [text(450, 28, "پانچ ضدّی جوڑے: ہر حرف میں ہر جوڑے کی ایک صفت ضرور ہے", "dg-t")]
    rows = [
      ("ہمس", "فحثه شخص سكت", "۱۰", "جہر", "باقی", "۱۹"),
      ("شدت", "أجد قط بكت", "۸", "رخاوت", "باقی (توسط کے سوا)", "۱۶"),
      ("استعلاء", "خص ضغط قظ", "۷", "استفال", "باقی", "۲۲"),
      ("اطباق", "ص ض ط ظ", "۴", "انفتاح", "باقی", "۲۵"),
      ("اذلاق", "فر من لب", "۶", "اصمات", "باقی", "۲۳"),
    ]
    for i, (a, am, ac, d, dm, dc) in enumerate(rows):
        y = 50 + i*78
        b.append(box(480, y, 380, 64, [], "g"))
        b.append(text(700, y+26, f"{a}  ({ac})", "dg-t"))
        b.append(ar(700, y+54, am, cls="dg-ar-s"))
        b.append(box(40, y, 380, 64, [], "b"))
        b.append(text(230, y+26, f"{d}  ({dc})", "dg-t"))
        b.append(text(230, y+52, dm, "dg-s"))
        b.append(f'<text class="dg-t" x="450" y="{y+38}" text-anchor="middle" style="fill:var(--gold)">⇄</text>')
    b.append(text(450, 448, "توسط (۵: لن عمر) شدت اور رخاوت کے بیچ ہے؛ اس لیے رخاوت کے ۱۶ حروف = ۲۹ − ۸ − ۵", "dg-s"))
    write("sifat-pairs", svg(W, H, "".join(b), "پانچ ضدّی جوڑے"))
pairs()

# ---------- ۴۔ مد کی اقسام: فیصلہ چارٹ ----------
def madd_flow():
    W, H = 900, 640
    b = [text(450, 26, "مد کی قسم کیسے پہچانیں؟", "dg-t")]
    b.append(box(330, 44, 240, 50, ["حرفِ مد (ا / و / ی) موجود ہے"], "g"))
    b.append(arrow(450, 94, 450, 126))
    b.append(box(330, 126, 240, 50, ["اس کے بعد ہمزہ ہے؟"], "y"))
    # ہاں: بائیں؟ RTL میں ہاں دائیں
    b.append(arrow(570, 151, 700, 151, "ہاں", ly=140))
    b.append(box(650, 126, 220, 50, ["ایک ہی کلمے میں؟"], "y"))
    b.append(arrow(760, 176, 760, 216, "ہاں", lx=780))
    b.append(box(660, 216, 200, 74, ["مدِ متصل", ("واجب — ۴ یا ۵ حرکات", "dg-s")], "g"))
    b.append(arrow(650, 151, 560, 250, "نہیں", lx=600, ly=185))
    b.append(box(470, 216, 190, 74, ["مدِ منفصل", ("جائز — ۴ یا ۵ حرکات", "dg-s")], "g"))
    # نہیں: بائیں
    b.append(arrow(330, 151, 200, 151, "نہیں", ly=140))
    b.append(box(40, 126, 220, 50, ["اس کے بعد سکون ہے؟"], "y"))
    b.append(arrow(150, 176, 150, 216, "نہیں", lx=130))
    b.append(box(40, 216, 220, 74, ["مدِ طبعی (اصلی)", ("۲ حرکات", "dg-s")], "b"))
    b.append(arrow(260, 151, 330, 330, "ہاں", lx=330, ly=250))
    b.append(box(300, 330, 300, 50, ["سکون اصلی ہے یا وقف کی وجہ سے؟"], "y"))
    b.append(arrow(570, 380, 690, 430, "اصلی", lx=650, ly=395))
    b.append(box(590, 430, 270, 90, ["مدِ لازم", ("۶ حرکات", "dg-s"), ("(مشدد/ساکن: الضّالین، آلآن، الم)", "dg-s")], "r"))
    b.append(arrow(330, 380, 210, 430, "وقفی", lx=240, ly=395))
    b.append(box(40, 430, 270, 90, ["مدِ عارض للسکون", ("۲ یا ۴ یا ۶ حرکات", "dg-s"), ("(العالمین پر وقف)", "dg-s")], "r"))
    b.append(box(330, 560, 300, 60, [("خاص: ہمزہ مد سے پہلے ہو (آمنوا) ← مدِ بدل: ۲ حرکات", "dg-s"), ("واؤ/یاء ساکن، ماقبل زبر، وقف ← مدِ لین", "dg-s")], ""))
    write("madd-flow", svg(W, H, "".join(b), "مد کی اقسام کا فیصلہ چارٹ"))
madd_flow()

# ---------- ۵۔ مد کی مقداریں ----------
def madd_len():
    W, H = 900, 420
    b = [text(450, 26, "مد کی مقداریں (حرکات میں): ایک حرکت ≈ ایک انگلی کھولنے یا بند کرنے کا وقت", "dg-t")]
    unit = 100
    x0 = 800   # دائیں سے بائیں
    for k in range(0, 7):
        x = x0 - k*unit
        b.append(f'<line class="dg-lead" x1="{x}" y1="52" x2="{x}" y2="372"/>')
        b.append(text(x, 392, "۰۱۲۳۴۵۶"[k], "dg-s"))
    rows = [
      ("طبعی، بدل، عوض، صلہ صغریٰ", [(2, 2, "g")]),
      ("متصل، منفصل، صلہ کبریٰ", [(4, 5, "y")]),
      ("عارض للسکون، لین", [(2, 2, "b"), (4, 4, "b"), (6, 6, "b")]),
      ("لازم", [(6, 6, "r")]),
    ]
    for i, (nm, bars) in enumerate(rows):
        y = 70 + i*78
        b.append(text(x0+60, y+6, "", "dg-s"))
        for lo, hi, c in bars:
            col = {"g": "var(--green)", "y": "var(--gold)", "b": "var(--blue)", "r": "var(--red)"}[c]
            if lo == hi and nm.startswith("عارض"):
                yy = y + 18 + (hi//2 - 1) * 12
                b.append(f'<rect x="{x0-hi*unit}" y="{yy}" width="{hi*unit}" height="9" rx="4" fill="{col}" opacity="{0.9 - 0.2*(hi//2 - 1)}"/>')
            elif lo == hi:
                b.append(f'<rect x="{x0-hi*unit}" y="{y+22}" width="{hi*unit}" height="22" rx="8" fill="{col}" opacity=".85"/>')
            else:
                b.append(f'<rect x="{x0-lo*unit}" y="{y+22}" width="{lo*unit}" height="22" rx="8" fill="{col}" opacity=".85"/>')
                b.append(f'<rect x="{x0-hi*unit}" y="{y+22}" width="{(hi-lo)*unit}" height="22" fill="{col}" opacity=".45"/>')
        b.append(text(x0-10, y+12, nm, "dg-t", "end") if False else f'<text class="dg-t" x="{x0}" y="{y+12}" text-anchor="start">{nm}</text>')
    b.append(text(450, 412, "(عارض و لین میں ۲، ۴، ۶ میں سے کوئی ایک مقدار؛ پوری تلاوت میں یکساں رکھیں)", "dg-s"))
    write("madd-lengths", svg(W, H, "".join(b), "مد کی مقداریں"))
madd_len()
