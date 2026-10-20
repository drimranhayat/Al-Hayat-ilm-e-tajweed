"""خاکوں کے مشترک اوزار (SVG بنانے کے لیے)"""
from pathlib import Path
OUT = Path(__file__).parent.parent / "diagrams"
OUT.mkdir(exist_ok=True)

DEFS = '''<defs><marker id="dgArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor" style="color:var(--muted)"/></marker></defs>'''

def svg(w, h, body, title, desc=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{title}" direction="rtl">'
            f'<title>{title}</title>' + (f'<desc>{desc}</desc>' if desc else '') + DEFS + body + '</svg>')

def num(n, x, y, cls="", r=13):
    s = str(n)
    ur = "".join("۰۱۲۳۴۵۶۷۸۹"[int(c)] for c in s)
    return (f'<circle class="dg-dot {cls}" cx="{x}" cy="{y}" r="{r}"/>'
            f'<text class="dg-n" x="{x}" y="{y+5}" text-anchor="middle" style="font-family:var(--ur);font-size:14px">{ur}</text>')

def lead(x1, y1, x2, y2, cls="dg-lead"):
    return (f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'
            f'<circle cx="{x2}" cy="{y2}" r="3.6" fill="var(--ink)"/>')

def text(x, y, s, cls="dg-t", anchor="middle"):
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{s}</text>'

def write(name, content):
    (OUT / f"{name}.svg").write_text(content, encoding="utf-8")
    print("✔", name)

def box(x, y, w, h, lines, cls="", tcls="dg-t", r=12):
    """x,y مرکز کے نہیں، اوپر بائیں کونے ہیں"""
    if isinstance(lines, str): lines = [lines]
    out = f'<rect class="dg-box {cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/>'
    n = len(lines)
    lh = 22
    y0 = y + h/2 - (n-1)*lh/2 + 5
    for i, l in enumerate(lines):
        c = tcls
        if isinstance(l, tuple): l, c = l
        out += f'<text class="{c}" x="{x+w/2}" y="{y0+i*lh}" text-anchor="middle">{l}</text>'
    return out

def arrow(x1, y1, x2, y2, label="", lx=None, ly=None):
    out = f'<path class="dg-arrow" d="M{x1} {y1} L{x2} {y2}" style="color:var(--muted)"/>'
    if label:
        lx = lx if lx is not None else (x1+x2)/2 + 6
        ly = ly if ly is not None else (y1+y2)/2
        out += f'<text class="dg-s" x="{lx}" y="{ly}" text-anchor="middle" style="fill:var(--green);font-weight:700">{label}</text>'
    return out

def ar(x, y, s, anchor="middle", cls="dg-ar"):
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{s}</text>'
