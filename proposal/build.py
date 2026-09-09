#!/usr/bin/env python3
"""Assemble proposal chapters into a single self-contained HTML file.

Structure: a short preface (the whole pitch, compressed), then three acts —
السوق / الحل / الاتفاق (market / solution / deal) — each opened by a full
divider that states its one line before the chapters prove it.
"""
import re, pathlib

BASE = pathlib.Path(__file__).parent
CH = BASE / "ch"

# each act: id, roman numeral, label, one-line thesis, supporting line,
# then its chapters as (chapter-id, file, title, written?)
ACTS = [
    {
        "id": "preface",
        "num": "٠",
        "label": "مقدّمة",
        "chapters": [
            ("ch01", "01-02.html", "الملخّص التنفيذي", True),
            ("ch02", None, "مين إحنا، وإيه اللي بنيناه", True),
        ],
    },
    {
        "id": "act1",
        "num": "I",
        "label": "السوق",
        "tag": "دي السوق.",
        "line": "مش فاضي، ومتسابق — بس فيه ثغرة ثقة محدش قافلها لسه.",
        "mood": "market",
        "chapters": [
            ("ch03", "03-04.html", "الفكرة: إيه اللي بنبيعه فعلاً", True),
            ("ch04", None, "السوق: مش فاضي، ومتسابق", True),
            ("ch05", "05.html", "الأرض السورية: اللي بيكسر الافتراضات", True),
        ],
    },
    {
        "id": "act2",
        "num": "II",
        "label": "الحل",
        "tag": "ده الحل.",
        "line": "مش تطبيق. مضيف أصداف بيتصمّم على الفشل، مش على العرض.",
        "mood": "solution",
        "chapters": [
            ("ch06", "06-demo.html", "الشاشات — تشريح بقراره", True),
            ("ch07", "07-08.html", "الأركتكتشر: مضيف الأصداف", True),
            ("ch08", None, "العمود الفقري للتصنيف", True),
            ("ch09", "09.html", "الأسطح: إيه اللي بيتبني", True),
            ("ch10", "10.html", "الفشل هو المنتج", True),
            ("ch11", "11.html", "الهوية والدخول", True),
            ("ch12", "12.html", "الفلوس: الليدجر والعملة", True),
            ("ch13", "13.html", "التوزيع: إزاي التطبيق يوصل", True),
            ("ch14", "14.html", "الإطلاق: أول ٢٠ تاجر", True),
        ],
    },
    {
        "id": "act3",
        "num": "III",
        "label": "الاتفاق",
        "tag": "ده الاتفاق.",
        "line": "مش شهري. بوابات — كل مرحلة بيفتحها حدث حقيقي، مش تاريخ.",
        "mood": "deal",
        "chapters": [
            ("ch15", "15.html", "المراحل والبوابات", True),
            ("ch16", "16-cost.html", "التكلفة التشغيلية", True),
            ("ch17", "17.html", "القانون والكيان", True),
            ("ch18", "18.html", "المخاطر بصراحة", True),
            ("ch19", None, "التعاقد", False),
            ("ch20", "20.html", "الملاحق والمصادر", True),
        ],
    },
]


def actbreak_html(act):
    return f"""
    <section class="actbreak actbreak--{act['mood']}" id="{act['id']}"
      data-act="{act['id']}" data-act-num="{act['num']}" data-act-label="{act['label']}"
      data-title="{act['tag']}">
      <p class="actbreak__eyebrow">الجزء {act['num']} · {act['label']}</p>
      <h2 class="actbreak__tag">{act['tag']}</h2>
      <p class="actbreak__line">{act['line']}</p>
    </section>"""


def nav_link(cid, title, act_id, written):
    num = cid.replace("ch", "")
    if written:
        return f'<a href="#{cid}" data-act="{act_id}"><i>{num}</i><span>{title}</span></a>'
    return f'<span class="soon"><i>{num}</i><span>{title}</span></span>'


def read_chapter_file(fname, act):
    """Read a chapter file and tag every <section id="chNN"> inside it with
    the act it belongs to — a single combined file (e.g. 03-04.html) only
    ever holds chapters from one act, so one tag pass covers all of them.
    Used by the mobile top bar / peek sheet to know "where am I" live."""
    content = (CH / fname).read_text(encoding="utf-8").strip()
    return re.sub(
        r'id="(ch\d+)"',
        lambda m: (
            f'id="{m.group(1)}" data-act="{act["id"]}" '
            f'data-act-num="{act.get("num","")}" data-act-label="{act.get("label","")}"'
        ),
        content,
    )


def build():
    shell = (BASE / "index.html").read_text(encoding="utf-8")
    css = (BASE / "system.css").read_text(encoding="utf-8")

    # inline CSS so the file is fully self-contained
    shell = shell.replace(
        '<link rel="stylesheet" href="system.css">',
        f"<style>\n{css}\n</style>",
    )

    # ---- assemble body: preface, then per-act divider + its chapters ----
    body_parts = []
    nav_parts = []
    written_n = 0
    total_n = 0

    for act in ACTS:
        if act["id"] == "preface":
            group = ['<div class="toc-group">']
            for cid, fname, title, written in act["chapters"]:
                total_n += 1
                if written:
                    written_n += 1
                    if fname:
                        p = CH / fname
                        if p.exists():
                            body_parts.append(read_chapter_file(fname, act))
                group.append("      " + nav_link(cid, title, "preface", written))
            group.append("    </div>")
            nav_parts.append("\n".join(group))
            continue

        body_parts.append(actbreak_html(act))

        links = []
        for cid, fname, title, written in act["chapters"]:
            total_n += 1
            if written:
                written_n += 1
                if fname:
                    p = CH / fname
                    if p.exists():
                        body_parts.append(read_chapter_file(fname, act))
            links.append("        " + nav_link(cid, title, act["id"], written))
        links_html = "\n".join(links)

        nav_parts.append(
            f'''<details class="toc-act" data-act="{act['id']}"{' open' if act['id']=='act1' else ''}>
      <summary><span class="toc-act__num">{act['num']}</span><span>{act['label']}</span></summary>
      <div class="toc-act__body">
{links_html}
      </div>
    </details>'''
        )

    body = "\n\n".join(body_parts)
    nav_html = "\n    ".join(nav_parts)

    shell = re.sub(
        r'<nav id="toc"[^>]*>.*?</nav>',
        f'<nav id="toc" aria-label="فهرس المستند">\n    {nav_html}\n    </nav>',
        shell,
        flags=re.S,
    )

    # style for not-yet-written entries + accordion groups
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

    notice = f"""
      <div class="draft">
        <b>مسودة قيد الكتابة — {written_n} من {total_n} فصول</b>
        الفصول المكتوبة كاملة ومراجَعة. الباقي (الرمادي في الفهرس) لسه بيتكتب.
        كل رقم في المكتوب له مصدر وتاريخ فحص، واللي مش مؤكَّد مكتوب جنبه بالنص.
      </div>"""

    shell = shell.replace("<!--CHAPTERS-->", notice + "\n\n" + body)

    out = BASE / "dist" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(shell, encoding="utf-8")
    print(f"built {out}  ({out.stat().st_size:,} bytes)")
    print(f"chapters: {written_n}/{total_n} written · 3 acts + preface")
    return out


if __name__ == "__main__":
    build()
