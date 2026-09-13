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
            ("ch01", "01.html", "الملخّص التنفيذي", True),
        ],
    },
    {
        "id": "act1",
        "num": "I",
        "label": "السوق",
        "tag": "السوق.",
        "line": "مش فاضي، ومتسابق — بس فيه ثغرة ثقة محدش قافلها لسه.",
        "mood": "market",
        "chapters": [
            ("ch02", "02.html", "السوق: مش فاضي، ومتسابق", True),
            ("ch03", "03.html", "الأرض السورية: اللي بيكسر الحسابات", True),
        ],
    },
    {
        "id": "act2",
        "num": "II",
        "label": "الحل",
        "tag": "الحل.",
        "line": "أساس واحد بيلبس وشوش مختلفة — ومتصمّم على الفشل، مش على العرض.",
        "mood": "solution",
        "chapters": [
            ("ch04", "04.html", "الشاشات وسبب كل عنصر", True),
            ("ch05", "05.html", "إزاي هيتبني: أساس واحد، وشوش متعددة", True),
            ("ch06", "06.html", "الفشل والفلوس", True),
        ],
    },
    {
        "id": "act3",
        "num": "III",
        "label": "الاتفاق",
        "tag": "الاتفاق.",
        "line": "سعر واحد، دفعتين، والأكبر بعد ما تشوفوا المنتج شغّال.",
        "mood": "deal",
        "chapters": [
            ("ch07", "07.html", "الإطلاق والمخاطر", True),
            ("ch08", "08.html", "التعاقد", True),
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
    the act it belongs to — used by the mobile top bar / peek sheet to know
    "where am I" live."""
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
            f'''<div class="toc-act" data-act="{act['id']}">
      <p class="toc-act__head"><span class="toc-act__num">{act['num']}</span><span>{act['label']}</span></p>
{links_html}
    </div>'''
        )

    body = "\n\n".join(body_parts)
    nav_html = "\n    ".join(nav_parts)

    shell = re.sub(
        r'<nav id="toc"[^>]*>.*?</nav>',
        f'<nav id="toc" aria-label="فهرس المستند">\n    {nav_html}\n    </nav>',
        shell,
        flags=re.S,
    )

    shell = shell.replace("<!--CHAPTERS-->", body)

    out = BASE / "dist" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(shell, encoding="utf-8")

    # custom domain for GitHub Pages — must ship inside the artifact
    (out.parent / "CNAME").write_text("syria.kariem.dev\n", encoding="utf-8")
    print(f"built {out}  ({out.stat().st_size:,} bytes)")
    print(f"chapters: {written_n}/{total_n} written · 3 acts + preface")
    return out


if __name__ == "__main__":
    build()
