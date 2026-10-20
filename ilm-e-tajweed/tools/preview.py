import sys, asyncio
from pathlib import Path
from playwright.sync_api import sync_playwright
root = Path(__file__).parent.parent
names = sys.argv[1:]
css = (root/"assets/style.css").read_text(encoding="utf-8")
with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
    for n in names:
        svg = (root/"diagrams"/f"{n}.svg").read_text(encoding="utf-8")
        html = f'<html dir="rtl"><head><meta charset="utf-8"><style>{css}</style></head><body style="padding:10px"><figure class="diagram">{svg}</figure></body></html>'
        pg = br.new_page(viewport={"width":960,"height":800})
        pg.set_content(html)
        pg.wait_for_timeout(300)
        out = f"/tmp/claude-0/-home-claude/5c6dcef8-9dc4-599c-9b55-68519ca45f08/scratchpad/{n}.png"
        pg.locator("figure").screenshot(path=out)
        print(out)
    br.close()
