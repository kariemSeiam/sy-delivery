#!/usr/bin/env python3
"""Assemble proposal chapters into a single self-contained HTML file."""
import re, pathlib

BASE = pathlib.Path(__file__).parent
CH = BASE / "ch"

# chapter files in document order
ORDER = ["01-05.html", "03-04.html", "05.html", "06-demo.html", "16-cost.html"]

# canonical TOC: (id, title, written?)
TOC = [
    ("ch01", "الملخّص التنفيذي", True),
    ("ch02", "مين إحنا، وإيه اللي بنيناه", True),
    ("ch03", "الفكرة: إيه اللي بنبيعه فعلاً", True),
    ("ch04", "السوق: مش فاضي، ومتسابق", True),
    ("ch05", "الأرض السورية: اللي بيكسر الافتراضات", True),
    ("ch06", "الشاشات — تشريح بقراره", True),
    ("ch07", "الأركتكتشر: مضيف الأصداف", False),
    ("ch08", "العمود الفقري للتصنيف", False),
    ("ch09", "الأسطح: إيه اللي بيتبني", False),
    ("ch10", "الفشل هو المنتج", False),
    ("ch11", "الهوية والدخول", False),
    ("ch12", "الفلوس: الليدجر والعملة", False),
    ("ch13", "التوزيع: إزاي التطبيق يوصل", False),
    ("ch14", "الإطلاق: أول ٢٠ تاجر", False),
    ("ch15", "المراحل والبوابات", False),
    ("ch16", "التكلفة التشغيلية", True),
    ("ch17", "القانون والكيان", False),
    ("ch18", "المخاطر بصراحة", False),
    ("ch19", "التعاقد", False),
    ("ch20", "الملاحق والمصادر", False),
]


def build():
    shell = (BASE / "index.html").read_text(encoding="utf-8")
    css = (BASE / "system.css").read_text(encoding="utf-8")

    # inline CSS so the file is fully self-contained
    shell = shell.replace(
        '<link rel="stylesheet" href="system.css">',
        f"<style>\n{css}\n</style>",
    )

    # assemble chapters
    parts = []
    for name in ORDER:
        p = CH / name
        if p.exists():
            parts.append(p.read_text(encoding="utf-8").strip())
    body = "\n\n".join(parts)

    # honest TOC — unwritten chapters render as disabled
    nav = []
    for cid, title, written in TOC:
        num = cid.replace("ch", "")
        if written:
            nav.append(f'      <a href="#{cid}"><i>{num}</i><span>{title}</span></a>')
        else:
            nav.append(
                f'      <span class="soon"><i>{num}</i><span>{title}</span></span>'
            )
    nav_html = "\n".join(nav)

    shell = re.sub(
        r'<nav id="toc"[^>]*>.*?</nav>',
        f'<nav id="toc" aria-label="فهرس المستند">\n{nav_html}\n    </nav>',
        shell,
        flags=re.S,
    )

    # style for not-yet-written entries
    shell = shell.replace(
        "</style>",
        """
.side nav .soon{display:grid;grid-template-columns:26px 1fr;gap:var(--s3);
  align-items:baseline;padding:var(--s2) var(--s3);font-size:14.5px;
  line-height:1.5;color:rgba(255,255,255,.3);cursor:default}
.side nav .soon i{font-style:normal;font-family:var(--mono);font-size:11.5px;
  color:rgba(255,255,255,.18)}
.side nav .soon span::after{content:" ·";opacity:.5}
.draft{background:var(--sand-tint);border:1px solid #F0E0C4;border-radius:var(--r-ui);
  padding:var(--s5) var(--s6);margin:var(--s7) 0 0;font-size:15.5px;color:var(--sand-deep)}
.draft b{display:block;font-family:var(--display);font-weight:800;margin-bottom:var(--s2)}
</style>""",
    )

    written_n = sum(1 for _, _, w in TOC if w)
    notice = f"""
      <div class="draft">
        <b>مسودة قيد الكتابة — {written_n} من {len(TOC)} فصول</b>
        الفصول المكتوبة كاملة ومراجَعة. الباقي (الرمادي في الفهرس) لسه بيتكتب.
        كل رقم في المكتوب له مصدر وتاريخ فحص، واللي مش مؤكَّد مكتوب جنبه بالنص.
      </div>"""

    shell = shell.replace("<!--CHAPTERS-->", notice + "\n\n" + body)

    out = BASE / "dist" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(shell, encoding="utf-8")
    print(f"built {out}  ({out.stat().st_size:,} bytes)")
    print(f"chapters: {len(parts)} files, {written_n}/{len(TOC)} written")
    return out


if __name__ == "__main__":
    build()
