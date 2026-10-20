import asyncio,base64,pathlib
from playwright.async_api import async_playwright
H=pathlib.Path(__file__).resolve().parent.parent / 'fonts'
def face(fam,w,f): return f"@font-face{{font-family:{fam};font-weight:{w};src:url(data:font/woff2;base64,{base64.b64encode((H/f).read_bytes()).decode()})}}"
html=f'''<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8"><style>
{face('Amiri',700,'Amiri-700.woff2')}{face('PlexAr',400,'IBMPlex-400.woff2')}{face('PlexAr',700,'IBMPlex-700.woff2')}
*{{box-sizing:border-box;margin:0}}
body{{width:1200px;height:630px;background:#f3efe4;color:#1b2330;font-family:PlexAr;position:relative;overflow:hidden}}
.bar{{position:absolute;inset-inline:0;top:0;height:14px;background:#1f3b64}}
.rule{{position:absolute;inset-inline:80px;top:96px;height:2px;background:#a8843a}}
.k{{position:absolute;inset-inline:80px;top:42px;font-size:30px;color:#555d6b;font-weight:700}}
h1{{position:absolute;inset-inline:80px;top:140px;font-family:Amiri;font-weight:700;font-size:104px;line-height:1.3}}
.s{{position:absolute;inset-inline:80px;top:300px;font-size:42px;line-height:1.6;color:#2b3340;max-width:900px}}
.row{{position:absolute;inset-inline:80px;bottom:60px;display:flex;gap:56px;align-items:flex-end}}
.f b{{display:block;font-family:Amiri;font-size:78px;line-height:1;color:#1f3b64}}
.f span{{font-size:26px;color:#555d6b}}
.u{{position:absolute;inset-inline-start:80px;bottom:18px;font-size:22px;color:#555d6b;direction:ltr}}
</style><body><div class="bar"></div><div class="k">وثيقة مرجعية للمؤسسين</div><div class="rule"></div>
<h1>منصة توصيل الطلبات</h1>
<div class="s">الأساس القانوني والتقني للإطلاق في دمشق وريفها. كل رقم بمادته وصفحته.</div>
<div class="row"><div class="f"><b>٤٥</b><span>يوماً مهلة البتّ</span></div><div class="f"><b>٦</b><span>أشهر للإطلاق</span></div><div class="f"><b>١٣</b><span>سؤالاً مفتوحاً</span></div></div>
<div class="u">syria.kariem.dev</div></body></html>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await (await b.new_context(viewport={'width':1200,'height':630})).new_page()
        await pg.set_content(html); await pg.wait_for_timeout(600)
        await pg.screenshot(path=str(pathlib.Path(__file__).resolve().parent / 'og_raw.png')); await b.close()
asyncio.run(main())
