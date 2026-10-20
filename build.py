#!/usr/bin/env python3
"""
علمِ تجوید — جامع اردو ویب سائٹ کا اسٹیٹک جنریٹر
استعمال:  python3 build.py       (نتیجہ docs/ فولڈر میں بنتا ہے)

content/ کی ہر فائل ایک صفحہ ہے۔ ترتیب اور عنوان نیچے PAGES میں درج ہیں۔
"""
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
ASSETS = ROOT / "assets"
OUT = ROOT / "docs"

SITE_TITLE = "علمِ تجوید"
SITE_TAGLINE = "قرآنِ کریم کو درست پڑھنے کا جامع اردو مرکز"

# (فائل، عنوان، مختصر تعارف، گروہ)
PAGES = [
    ("index", "صفحۂ اوّل", "", None),
    # ابتدائی
    ("01-taaruf", "تجوید کا تعارف", "تعریف، موضوع، غرض، حکم اور فضیلت", "بنیادی باتیں"),
    ("02-sabut", "تجوید کا ثبوت", "قرآن، حدیث، اقوالِ ائمہ اور مقدمۂ جزریہ کی روشنی میں", "بنیادی باتیں"),
    ("03-lahn", "لحن: جلی و خفی", "تلاوت کی غلطیوں کی اقسام اور ان کا حکم", "بنیادی باتیں"),
    ("04-adab", "آدابِ تلاوت اور رفتار", "استعاذہ، بسملہ، ترتیل، تدویر، حدر", "بنیادی باتیں"),
    # حروف
    ("05-makharij", "مخارجِ حروف", "سترہ مخارج، پانچ مقامات، پہچاننے کا طریقہ", "حروف"),
    ("06-sifat", "صفاتِ حروف", "لازمہ، متضادہ، غیر متضادہ، ممیزہ، عارضہ", "حروف"),
    ("07-tafkhim", "تفخیم و ترقیق", "پُر اور باریک حروف، لامِ جلالہ، راء کے احکام", "حروف"),
    # احکام
    ("08-noon", "نون ساکن اور تنوین", "اظہار، ادغام، قلب، اخفاء", "احکام"),
    ("09-meem", "میمِ ساکن، غنہ اور مشدّد", "اخفائے شفوی، ادغامِ شفوی، اظہارِ شفوی", "احکام"),
    ("10-madd", "مد کے احکام", "حروفِ مد و لین، مدِ اصلی و فرعی، مقدار", "احکام"),
    ("11-idgham", "ادغام اور لامِ تعریف", "صغیر و کبیر، مثلین، متجانسین، متقاربین", "احکام"),
    ("12-hamza", "ہمزہ: قطع و وصل", "ہمزۂ قطع و وصل، ابتدا کی حرکت، ہمزۂ استفہام", "احکام"),
    ("13-sakinain", "اجتماعِ ساکنین", "دو ساکنوں کا ملنا اور اس کے احکام", "احکام"),
    # وقف و رسم
    ("14-waqf", "وقف و ابتدا", "اقسامِ وقف، علاماتِ اوقاف، ابتدا", "وقف و رسم"),
    ("15-rasm", "رسمِ مصحف: مقطوع، موصول اور تاءات", "جزریہ کے ابیات کی روشنی میں", "وقف و رسم"),
    ("16-qirat", "قراءات اور روایتِ حفص", "عشرہ ائمہ و رواۃ، امام عاصم، حفص، شاطبی و جزری", "وقف و رسم"),
    # اوزار
    ("letters", "حروف کا مطالعہ (انٹرایکٹو)", "کسی بھی حرف پر کلک کریں: مخرج اور تمام صفات دیکھیں", "اوزار اور مشق"),
    ("quiz", "امتحان و مشق", "سوالات کے ذریعے اپنی تیاری جانچیں", "اوزار اور مشق"),
    ("cheatsheet", "خلاصہ و جداول", "ایک نظر میں تمام قواعد", "اوزار اور مشق"),
    ("jazariyya", "المقدمۃ الجزریہ (متن)", "۱۰۷ ابیات، حفظ کے لیے چھپانے کی سہولت کے ساتھ", "اوزار اور مشق"),
    ("glossary", "اصطلاحات کی فرہنگ", "تجوید کی اصطلاحات کا مختصر لغت", "اوزار اور مشق"),
    ("sources", "مصادر و حوالہ جات", "ماخذ کتب اور استعمال کی وضاحت", "اوزار اور مشق"),
]

# صفحہ مخصوص اسکرپٹس
PAGE_SCRIPTS = {
    "letters": ["letters-data.js", "letters.js"],
    "quiz": ["quiz-data.js", "quiz.js"],
    "jazariyya": ["jazariyya.js"],
}

TEMPLATE = (ROOT / "template.html").read_text(encoding="utf-8")

DIACRITICS = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭـ]")


def strip_tags(s: str) -> str:
    s = re.sub(r"<svg.*?</svg>", " ", s, flags=re.S)
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S)
    s = re.sub(r"<style.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def norm(s: str) -> str:
    s = DIACRITICS.sub("", s)
    s = s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ٱ", "ا")
    s = s.replace("ي", "ی").replace("ى", "ی").replace("ې", "ی").replace("ك", "ک").replace("ہ", "ه").replace("ۃ", "ه").replace("ة", "ه")
    return s


DIAGRAMS = ROOT / "diagrams"


def inline_diagrams(body: str) -> str:
    """<!--diagram:نام|کیپشن--> کو diagrams/نام.svg کے inline SVG سے بدلتا ہے۔"""
    def rep(m):
        name, _, cap = m.group(1).partition("|")
        f = DIAGRAMS / f"{name.strip()}.svg"
        if not f.exists():
            print("⚠️  خاکہ غائب:", f.name)
            return ""
        svg = f.read_text(encoding="utf-8")
        cap_html = f"<figcaption>{cap.strip()}</figcaption>" if cap.strip() else ""
        return f'<figure class="diagram">{svg}{cap_html}</figure>'
    return re.sub(r"<!--diagram:(.*?)-->", rep, body)


def nav_html(current: str) -> str:
    out = []
    last_group = None
    gorder = []
    for slug, title, _, group in PAGES:
        if slug == "index":
            cls = ' class="active"' if current == slug else ""
            out.append(f'<a href="index.html"{cls}>🏠 {title}</a>')
            continue
        if group != last_group:
            if last_group is not None:
                out.append("</div>")
            if group not in gorder:
                gorder.append(group)
            out.append(f'<div class="nav-group g{gorder.index(group) + 1}"><h4>{group}</h4>')
            last_group = group
        cls = ' class="active"' if current == slug else ""
        out.append(f'<a href="{slug}.html"{cls}>{title}</a>')
    out.append("</div>")
    return "\n".join(out)


def prev_next(slug: str) -> str:
    slugs = [p for p in PAGES if p[0] != "index"]
    idx = next((i for i, p in enumerate(slugs) if p[0] == slug), None)
    if idx is None:
        return ""
    parts = ['<nav class="pager" aria-label="صفحات">']
    if idx + 1 < len(slugs):  # RTL: اگلا بائیں طرف
        n = slugs[idx + 1]
        parts.append(f'<a class="next" href="{n[0]}.html"><small>اگلا ←</small><b>{n[1]}</b></a>')
    else:
        parts.append("<span></span>")
    if idx > 0:
        p = slugs[idx - 1]
        parts.append(f'<a class="prev" href="{p[0]}.html"><small>→ پچھلا</small><b>{p[1]}</b></a>')
    parts.append("</nav>")
    return "".join(parts)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(ASSETS, OUT / "assets")
    (OUT / ".nojekyll").write_text("")

    index = []
    for slug, title, summary, group in PAGES:
        src = CONTENT / f"{slug}.html"
        if not src.exists():
            print("⚠️  غائب:", src.name)
            continue
        body = inline_diagrams(src.read_text(encoding="utf-8"))
        scripts = "".join(
            f'<script src="assets/{s}" defer></script>' for s in PAGE_SCRIPTS.get(slug, [])
        )
        is_home = slug == "index"
        page_title = SITE_TITLE if is_home else f"{title} — {SITE_TITLE}"
        desc = SITE_TAGLINE if is_home else (summary or title)
        page = (
            TEMPLATE.replace("{{TITLE}}", html.escape(page_title))
            .replace("{{DESC}}", html.escape(desc))
            .replace("{{NAV}}", nav_html(slug))
            .replace("{{BODY}}", body)
            .replace("{{PAGER}}", "" if is_home else prev_next(slug))
            .replace("{{SCRIPTS}}", scripts)
            .replace("{{BODYCLASS}}", "home" if is_home else "page")
        )
        (OUT / f"{slug}.html").write_text(page, encoding="utf-8")
        text = strip_tags(body)
        index.append({"u": f"{slug}.html", "t": title, "s": summary, "x": norm(text), "r": text[:400]})

    (OUT / "assets" / "search-index.json").write_text(
        json.dumps(index, ensure_ascii=False), encoding="utf-8"
    )
    print(f"✔ {len(index)} صفحات docs/ میں بن گئے")


if __name__ == "__main__":
    main()
