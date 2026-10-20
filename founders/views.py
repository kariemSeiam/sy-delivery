"""Task-ordered pages for the founders site.

The facts live once, in build.py (cards, ASK, CLOCK...). This module only decides
how they are shown: five pages ordered by the reader's question, not by the
statute's chapters.

    picture  -> where are we, what is known, what is not, what to do first
    todo     -> what has to be prepared (checklist, saved on the reader's device)
    bodies   -> what each authority decides, asks for, charges
    unknown  -> every open question, who answers, copy-to-send
    ref      -> every verified item with article and page (collapsed, filterable)
"""
import html, re, sys

AR = "٠١٢٣٤٥٦٧٨٩"
ar = lambda n: "".join(AR[int(d)] if d.isdigit() else d for d in str(n))
esc = lambda s: html.escape(s, quote=False)
plain = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


# ---------------------------------------------------------------- parsing
def parse_cards(panel_html):
    """-> list of dict(group, kind, title, line(html), src, fig, extra(html))."""
    out, group = [], ""
    pat = re.compile(r'<h2 class="sec[^"]*">(.*?)</h2>|<article class="card (\w+)">(.*?)</article>', re.S)
    for m in pat.finditer(panel_html):
        if m.group(1) is not None:
            group = plain(m.group(1)); continue
        kind, inner = m.group(2), m.group(3)
        fig = re.search(r'<div class="fig">(.*?)</div>', inner, re.S)
        title = re.search(r"<h3>(.*?)</h3>", inner, re.S).group(1)
        p = re.search(r"<p>(.*?)</p>", inner, re.S)
        srcs = re.findall(r'<span class="src">(.*?)</span>', inner, re.S)
        src = re.match(r"(.*)", srcs[-1], re.S) if srcs else None
        extra = re.search(r'(<div class="bars">.*?)<div class="meta">', inner, re.S)
        out.append(dict(group=group, kind=kind, title=plain(title), line=p.group(1) if p else "",
                        src=plain(src.group(1)) if src else "", fig=plain(fig.group(1)) if fig else "",
                        extra=extra.group(1) if extra else ""))
    return out


# ---------------------------------------------------------------- pieces
def split_src(src):
    """Split on commas that sit outside parentheses so '(٢، ٣)' stays whole."""
    parts, depth, cur = [], 0, ""
    for ch in src:
        if ch in "([": depth += 1
        if ch in ")]": depth -= 1
        if ch in "،؛" and depth == 0:
            if cur.strip(): parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip(): parts.append(cur.strip())
    return parts


def src_chips(src):
    if not src: return ""
    return '<div class="src">' + "".join(f"<bdi>{esc(x)}</bdi>" for x in split_src(src)) + "</div>"


def mark(kind):
    return {"open": '<em class="mk open">غير مثبت</em>', "design": '<em class="mk design">تصميم مقترح</em>',
            "meas": '<em class="mk meas">قياس</em>'}.get(kind, "")


def row(cid, title, body_html, kind="ok", fig="", extra_cls=""):
    f = f'<span class="rf-fig">{esc(fig)}</span>' if fig else ""
    return (f'<div class="row ref {kind} {extra_cls}" id="{cid}"><button type="button">'
            f'<span class="rt">{esc(title)}{mark(kind)}</span>{f}<span class="chev">‹</span></button>'
            f'<div class="more">{body_html}</div></div>')


def short(s, n):
    s = plain(s)
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"


# ---------------------------------------------------------------- build
def build(groups, ASK, stations_n, CLOCK, BEFORE):
    """groups: ordered [(label, [cards...])] for the reference. Returns dict page->html, index list."""
    index = []
    allcards = {c["title"]: c for _l, cs in groups for c in cs}

    def C(prefix):
        for t, c in allcards.items():
            if t.startswith(prefix): return c
        sys.exit("BUILD FAILED: views.py cannot find card " + prefix)

    # ============ REF ============
    ref = ""
    n = 0
    for label, cs in groups:
        ref += f'<h2 class="grp">{esc(label)}</h2>'
        for c in cs:
            n += 1; cid = f"c-ref-{n}"
            body = f"<p>{c['line']}</p>{c['extra']}{src_chips(c['src'])}"
            ref += row(cid, c["title"], body, c["kind"], c["fig"])
            index.append(("ref", cid, c["title"], plain(c["line"]), c["kind"]))
    for label, items in (("المهل بعد سريان الترخيص", [(f"{ar(m)} شهر: {t}", l, s) for m, t, l, s, _g in CLOCK]),):
        ref += f'<h2 class="grp">{esc(label)}</h2>'
        for t, l, s in items:
            n += 1; cid = f"c-ref-{n}"
            ref += row(cid, t, f"<p>{esc(l)}</p>{src_chips(s)}", "ok")
            index.append(("ref", cid, t, l, "ok"))
    ref_count = n
    ref_page = (
        '<h1 class="hq">المرجع الكامل</h1>'
        f'<p class="sub">{ar(ref_count)} بنداً، كل بند بمادته وصفحته. اضغط ليُفتح.</p>'
        '<div class="rtools"><input class="rfilter" type="search" placeholder="ابحث في البنود" aria-label="بحث في المرجع" autocomplete="off">'
        '<button type="button" class="rchip" data-only="open">غير المثبت فقط</button>'
        '<button type="button" class="rchip" id="rprint">طباعة</button></div>'
        '<p class="rnone" hidden>لا يوجد بند بهذا الاسم.</p>'
        + ref +
        '<p class="legend">البند غير المعلَّم مأخوذ من نص رسمي. «غير مثبت» لم نقرأ نصه. «تصميم مقترح» قرار منا لا نص.</p>')

    # ============ BODIES ============
    def ask_for(key):
        for w, qs in ASK:
            if w.startswith(key): return qs
        sys.exit("BUILD FAILED: views.py no ASK group " + key)

    bodies_def = [
        ("وزارة الاقتصاد والتجارة · مديرية الشركات وأمين السجل", "تصدّق نظام الشركة وتسجّلها", ("٧", "أيام"),
         ["قرار التصديق", "الإيداع والشهر", "سداد رأس المال", "عدد الشركاء"], "مديرية الشركات"),
        ("الهيئة الناظمة للاتصالات والبريد", "ترخيص توصيل الطلبات. سريانه غير محسوم", ("٤٥", "يوماً"),
         ["نوع الترخيص", "مدة البت في الطلب", "المدة والتجديد", "مهلة الإطلاق", "حصة الهيئة من الإيراد", "موعد السداد", "تغيير الشركاء"], "الهيئة الناظمة"),
        ("الهيئة الوطنية لخدمات تقانة المعلومات (NAITS)", "اعتمادية التطبيق واختبار أمنه", ("٣٢٬٠٠٠", "ل.س جديدة"),
         ["مراحل الإجراء", "مدة الاعتمادية", "الوثائق المطلوبة", "الأجور"], "الهيئة الوطنية"),
        ("مديرية هندسة المرور والنقل · دمشق", "تصريح تجول الدراجات", ("؟", "لم يُحسم"),
         ["مهمة التجول", "تسجيل الدراجة", "مناقصة محافظة دمشق"], "مديرية هندسة"),
        ("المصرف", "فتح حساب للشركة وتحويل المستحقات", ("؟", "لم يُحسم"),
         ["الحساب المصرفي", "تحويل المستحقات إلى الخارج"], None),
    ]
    bod = ""
    for k, (name, role, (fn, fs), picks, askkey) in enumerate(bodies_def, 1):
        cid = f"c-bodies-{k}"
        facts = ""
        for pfx in picks:
            c = C(pfx)
            facts += f'<div class="fact">{mark(c["kind"])}<b>{esc(c["title"])}</b><p>{c["line"]}</p>{src_chips(c["src"])}</div>'
        if askkey:
            qs = ask_for(askkey)
            facts += '<div class="open-sec"><h2>لم يُحسم بعد</h2><ul>' + "".join(f"<li>{esc(q)}</li>" for q in qs) + "</ul></div>"
        if name.startswith("الهيئة الوطنية"):
            facts += ('<div class="fact"><b>التقديم</b><p>إلى applications@naits.gov.sy أو بالتسليم في ديوان الهيئة، دمشق، طريق بيروت القديم، تقاطع صحارى، مجمع الديماس. هاتف ٠١١٣٩٣٧٠٣٢.</p>'
                      + src_chips("صفحة خدمة منح الاعتمادية · naits.gov.sy") + "</div>")
        bod += (f'<div class="row body" id="{cid}"><button type="button"><span class="n">{esc(fn)}<small>{esc(fs)}</small></span>'
                f'<span class="rt">{esc(name)}<span class="m">{esc(role)}</span></span><span class="chev">‹</span></button>'
                f'<div class="more">{facts}</div></div>')
        index.append(("bodies", cid, name, role, "ok"))
    bodies_page = ('<h1 class="hq">من يقرر ماذا؟</h1><p class="sub">خمس جهات. كل جهة وما تقرره وما تطلبه وما لم يُحسم عندها.</p>' + bod)

    # ============ UNKNOWN ============
    decides = {
        "الهيئة الناظمة": "يحدد: هل يلزم ملف الهيئة، وكم تبلغ كلفته",
        "الهيئة الوطنية": "يحدد: أين تُستضاف المنصة، ومتى تُسجَّل الشركة",
        "مديرية الشركات": "يحدد: رأس مال التأسيس وكلفته",
        "مديرية هندسة": "يحدد: هل تُشغَّل الدراجات في دمشق وداريا",
        "محامٍ": "يحدد: صياغة علاقة الشركة بالمطوّر",
    }
    unk = ""
    qn = 0
    for w, qs in ASK:
        dk = next((v for k, v in decides.items() if w.startswith(k)), "")
        items = ""
        for q in qs:
            qn += 1; cid = f"c-unknown-{qn}"
            items += (f'<div class="uq" id="{cid}" data-q="{qn}"><p>{esc(q)}</p>'
                      f'<button type="button" class="ust" aria-label="حالة السؤال">لم يُرسل</button></div>')
            index.append(("unknown", cid, short(q, 60), w, "open"))
        unk += (f'<section class="ug" data-who="{esc(w)}"><header><h3>{esc(w)}</h3><small>{esc(dk)}</small></header>{items}'
                f'<button type="button" class="copyg">انسخ أسئلة هذه الجهة</button></section>')
    unknown_page = ('<h1 class="hq">ما الذي لم يُحسم؟</h1>'
                    f'<p class="sub">{ar(qn)} سؤالاً على خمس جهات. اضغط على الحالة لتتبع ما أُرسل وما ورد ردّه.</p>'
                    '<div class="ubar"><span id="ucnt"></span></div>' + unk)

    # ============ TODO ============
    # (title, meta, detail, [src...], unknown?)
    def td(title, meta, more, src, unk=False):
        return dict(title=title, meta=meta, more=more, src=src, unk=unk)

    L, S, N = "قانون الشركات ٢٩/٢٠١١", "نظام الترخيص النمطي", "صفحة خدمة منح الاعتمادية · naits.gov.sy"
    todo_groups = [
        ("أولاً · تأسيس الشركة", "مديرية الشركات وأمين السجل", [
            td("نظام أساسي لشركة محدودة المسؤولية", "يقرر الوزير خلال ٧ أيام من تسجيل الطلب",
               C("قرار التصديق")["line"], [C("قرار التصديق")["src"]]),
            td("مدقق حسابات في النظام الأساسي", "يُرفق تعيينه بطلب التأسيس", C("مدقق الحسابات")["line"], [C("مدقق الحسابات")["src"]]),
            td("سداد رأس المال", "٣٠ يوماً من التصديق، أو ٤٠٪ عنده والباقي خلال سنة", C("سداد رأس المال")["line"], [C("سداد رأس المال")["src"]]),
            td("الإيداع عند أمين السجل ونشر القرار", "خلال ٦٠ يوماً من قرار التصديق", C("الإيداع والشهر")["line"], [C("الإيداع والشهر")["src"]]),
            td("حساب مصرفي للشركة", "المدة والشروط غير مثبتة · يُسأل: المصرف", C("الحساب المصرفي")["line"], [C("الحساب المصرفي")["src"]], True),
        ]),
        ("ثانياً · ملف الهيئة الناظمة", "الاتصالات والبريد · قد لا يلزم إن كان القرار ٤ هو الحاكم", [
            td("الاستمارة والسجل التجاري", "أو نظام تأسيس مصدّق لشركة قيد التأسيس", C("شكل الشركة")["line"], [C("شكل الشركة")["src"]]),
            td("المخوّلون بالتوقيع وعدم المحكومية", "أسماء ونماذج تواقيع وصور هويات", C("المخوّلون بالتوقيع")["line"], [C("المخوّلون بالتوقيع")["src"]]),
            td("دراسة جدوى مصدّقة لثلاث سنوات", "سوق ومبيعات وموازنة وتدفقات وأرباح وخسائر",
               "ولو كانت الشركة تعمل قبل النظام فتُرفق حساباتها الختامية لآخر سنتين.", ["م٣ · ص٦"]),
            td("التعرفة والمواصفات ومكان الاستضافة", "تُسلَّم مع الدراسة",
               "التعرفة المقترحة لأجور التوصيل وخدمة المنصة، والمواصفات الفنية، ومكان الاستضافة وبنية قواعد البيانات، وآلية الأرشفة، والإجراءات الأمنية.", ["م٣ · ص٦"]),
            td("إشعار سداد أجر الطلب", "المبلغ بعد التعديل غير مثبت", C("الرسوم وتعديلها")["line"], [C("الرسوم وتعديلها")["src"]], True),
        ]),
        ("ثالثاً · اعتمادية NAITS", "الهيئة الوطنية لخدمات تقانة المعلومات", [
            td("سجل تجاري حديث", "الشركة تُسجَّل قبل التقديم", "لا يوجد في هذا المسار قبول لشركة «قيد التأسيس».", [N]),
            td("جدول بخمسة أدوار", "الاسم والمؤهل والجنسية والتواصل",
               "مالك التطبيق، المدير التنفيذي، مطور التطبيق، مسؤول قواعد البيانات، مسؤول حماية البيانات.", [N]),
            td("نسخة APK فعّالة ووثيقة آلية العمل", "جميع الوظائف تعمل", "مع وثيقة بآلية عمل التطبيق وآلية الربط البرمجي.", [N]),
            td("سياسة استخدام تتضمن سياسة القاصرين", "تعريف التطبيق وحقوق المستخدم والخصوصية",
               "وكذلك الجهة المسؤولة والفئات المستهدفة وإجراءات المخالفة.", [N]),
            td("وثيقة اختبار الاختراق", "من شركة أمن معلومات معتمدة · القائمة غير مثبتة", "قائمة الشركات المعتمدة لم نجدها. يُسأل: NAITS.", [N, "القرار ٤ · بند ٦"], True),
            td("تعهدان وظرف مختوم", "أمن المعلومات، والموافقة المؤقتة",
               "إضافة إلى ظرف موقع ومختوم برابط لوحة إدارة التطبيق وحساب كامل الصلاحيات. مؤقت ويُلغى بعد الاختبارات.", [N]),
        ]),
    ]
    todo = ""
    tn = 0
    for gi, (gt, gs, its) in enumerate(todo_groups):
        todo += f'<h2 class="grp" data-g="{gi}">{esc(gt)}<small>{esc(gs)}</small></h2>'
        for it in its:
            tn += 1; cid = f"c-todo-{tn}"
            todo += (f'<div class="row item{" unk" if it["unk"] else ""}" id="{cid}" data-g="{gi}"><button type="button">'
                     f'<span class="rt">{esc(it["title"])}<span class="m">{esc(it["meta"])}</span></span><span class="chev">‹</span></button>'
                     f'<div class="more"><p>{it["more"]}</p>{src_chips("، ".join(list(it["src"])))}</div></div>')
            index.append(("todo", cid, it["title"], it["meta"], "open" if it["unk"] else "ok"))
    todo_page = ('<h1 class="hq">ما الذي يلزم تجهيزه؟</h1>'
                 '<p class="sub">ما يطلبه كل مسار من أوراق ووثائق. اضغط على أي بند لمصدره وتفاصيله.</p>' + todo)

    # ============ PICTURE ============
    def tile(nn, sm, t, src): return f'<div class="tile"><span class="n">{esc(nn)}<small>{esc(sm)}</small></span><p>{esc(t)}</p><bdi>{esc(src)}</bdi></div>'
    first_unknown = [(ASK[0][1][0], ASK[0][0]), (ASK[0][1][1], ASK[0][0]), (ASK[3][1][0], ASK[3][0])]
    head_unknown = [("أي ترخيص يحكم: قرار الوزارة ٤ أم نظام الهيئة؟", "يُسأل: وزارة الاتصالات والهيئة الناظمة"),
                    ("رسوم الهيئة بعد القرار ٢٦٤", "النص لم نقرأه · يُسأل: الهيئة الناظمة"),
                    ("الدراجات في دمشق وداريا: آلية مهمة التجول", "يُسأل: مديرية هندسة المرور والنقل")]
    picture = (
        '<h1 class="hq">أين نحن، وما الذي يُطلب منكم؟</h1>'
        '<p class="sub">هذه الصفحة تكفي لمن لا يقرأ غيرها.</p>'
        '<div class="strip"><div class="stp now"><i>١</i><b>تأسيس الشركة</b></div><div class="stp"><i>٢</i>الترخيص والاعتمادية</div><div class="stp"><i>٣</i>الإطلاق</div></div>'
        '<div class="grp">ما نعرفه من النصوص الرسمية</div><div class="tiles">'
        + tile("٤٥", "يوماً", "مهلة الهيئة للبتّ في الطلب بعد اكتمال الوثائق", "نظام الهيئة م٤ · ص٦")
        + tile("٦", "أشهر", "للإطلاق التجاري بعد سريان الترخيص وإلا أُلغي", "نظام الهيئة م٦ · ص١٨")
        + tile("٣٢٬٠٠٠", "ل.س جديدة", "مجموع أجور الاعتماد العادي في NAITS، حسابنا من البنود", "naits.gov.sy")
        + tile("٧", "أيام", "لقرار الوزير بالتصديق على نظام الشركة", "قانون الشركات م٦٢ · ص١٨")
        + '</div>'
        '<div class="open-sec"><h2>ما لم يُحسم بعد</h2><ul>'
        + "".join(f"<li>{esc(a)}<span>{esc(b)}</span></li>" for a, b in head_unknown)
        + '</ul><a class="more-link" href="#unknown" data-page="unknown">كل الأسئلة ←</a></div>'
        '<div class="nextblk"><b>نقترح أن تبدؤوا بثلاثة أمور</b><ol><li>تسمية أصحاب الأدوار الخمسة المطلوبة في ملف الاعتمادية</li>'
        '<li>إعداد النظام الأساسي واختيار مدقق الحسابات</li><li>إرسال الأسئلة المفتوحة إلى الجهتين</li></ol>'
        '<a href="#todo" data-page="todo">قائمة ما يلزم، بندًا بندًا ←</a></div>')

    pages = dict(picture=picture, todo=todo_page, bodies=bodies_page, unknown=unknown_page, ref=ref_page)
    for _grp, _cs in groups:
        for _c in _cs:
            if _c["kind"] in ("ok", "meas") and not _c["src"]:
                sys.exit("BUILD FAILED: verified item without source in reference -> " + _c["title"])
    if len(index) < 100: sys.exit("BUILD FAILED: reference lost items (%d)" % len(index))
    return pages, index, ref_count


CSS = r"""
/* ---- task-ordered pages (views.py) ---- */
.app{height:100dvh}
.top{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:8px 16px;border-bottom:1px solid var(--line)}
.top h1{font-size:15px;line-height:1.4;margin:0}.top .kicker{margin:0;font-size:12px;color:var(--mute);letter-spacing:0;text-align:end}
.top .kicker .pos{margin:0}
main{padding:12px 16px 120px}
.hq{font-size:21px;font-weight:800;line-height:1.4;margin:2px 0 2px}
.sub{font-size:13.5px;color:var(--mute);margin-bottom:12px}
.grp{font-size:12.5px;color:var(--acc);font-weight:700;margin:18px 2px 6px;display:block}
.grp small{display:block;font-weight:500;color:var(--mute);font-size:12px;margin-top:1px}
.row{background:var(--card);border:1px solid var(--line);border-radius:12px;margin-bottom:8px;overflow:hidden}
.row>button{all:unset;cursor:pointer;display:grid;align-items:center;gap:12px;width:100%;padding:11px 14px;box-sizing:border-box}
.row.ref>button{grid-template-columns:1fr auto 16px}
.row.body>button{grid-template-columns:78px 1fr 16px}
.row.item>button{grid-template-columns:1fr 16px}
.rt{font-size:15px;font-weight:600;line-height:1.5}
.rt .m{display:block;font-size:12.5px;font-weight:400;color:var(--mute);margin-top:1px}
.rf-fig{font-size:15px;font-weight:800;color:var(--acc);white-space:nowrap}
.n{text-align:center;font-size:24px;font-weight:800;color:var(--acc);line-height:1.1}
.n small{display:block;font-size:11.5px;font-weight:600;color:var(--mute);margin-top:2px}
.chev{color:var(--mute);font-size:18px;transition:transform .2s;text-align:center}
.row.open .chev{transform:rotate(-90deg)}
.more{display:none;padding:2px 14px 12px;border-top:1px dashed var(--line);font-size:14px;color:#2b3640}
.row.open .more{display:block}
.more p{margin-top:8px}
.row .src,.tile+.src{display:flex;flex-wrap:wrap;gap:4px 6px;margin-top:8px;font-size:12px;color:var(--mute);background:none;border:0;padding:0}
.src bdi{background:#efe9db;border-radius:6px;padding:0 8px}
.mk{font-style:normal;font-size:11px;font-weight:700;border-radius:99px;padding:0 8px;margin-inline-start:8px;border:1px solid;vertical-align:1px}
.mk.open{color:var(--amber);border-color:var(--amber);background:var(--amberbg)}
.mk.design{color:var(--mute);border-color:var(--mute);border-style:dashed}
.mk.meas{color:#1e3a8a;border-color:#1e3a8a}
.row.ref.open-k{}
.fact{margin-top:10px;padding-top:8px;border-top:1px dashed var(--line)}
.fact:first-child{border-top:0}
.fact b{font-size:14px}.fact p{margin-top:2px}
.legend{font-size:12.5px;color:var(--mute);margin-top:14px;text-align:center}
.strip{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:6px 0 14px}
.strip .stp{border:1px solid var(--line);background:var(--card);border-radius:10px;padding:8px 6px;text-align:center;font-size:13px;line-height:1.4}
.strip .stp i{display:block;font-style:normal;font-weight:800;font-size:16px;color:var(--mute)}
.strip .stp.now{border-color:var(--acc);background:#e8f1ea}.strip .stp.now i,.strip .stp.now b{color:var(--acc)}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.tile{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 12px}
.tile .n{text-align:start;font-size:28px}
.tile .n small{display:inline;margin-inline-start:6px}
.tile p{font-size:13.5px;line-height:1.5;margin-top:2px}
.tile bdi{display:inline-block;margin-top:6px;background:#efe9db;border-radius:6px;padding:0 8px;font-size:11.5px;color:var(--mute)}
.open-sec{margin-top:16px;border:1px solid #e1c98e;background:var(--amberbg);border-radius:12px;padding:12px 14px}
.open-sec h2{font-size:14px;color:var(--amber);margin-bottom:4px}
.open-sec ul{list-style:none}
.open-sec li{font-size:14px;padding:8px 0;border-top:1px dashed #e1c98e}
.open-sec li:first-child{border-top:0}
.open-sec li span{display:block;font-size:12.5px;line-height:1.6;color:#6b4600;margin-top:3px}
.more-link{display:block;margin-top:6px;font-size:13px;color:var(--amber);font-weight:700;text-decoration:none}
.nextblk{margin-top:14px;background:var(--acc);color:#fff;border-radius:12px;padding:12px 14px}
.nextblk b{display:block;font-size:13px;opacity:.85;margin-bottom:4px}
.nextblk ol{list-style:none;counter-reset:s;font-size:14.5px;line-height:1.6}
.nextblk li{counter-increment:s;display:grid;grid-template-columns:26px 1fr;gap:8px;padding:5px 0}
.nextblk li::before{content:counter(s,arabic-indic);width:24px;height:24px;border-radius:50%;background:#ffffff26;display:grid;place-items:center;font-weight:800;font-size:13px}
.nextblk a{display:block;margin-top:8px;text-align:center;background:#fff;color:var(--acc);border-radius:8px;padding:8px;font-weight:700;text-decoration:none;font-size:14px}
.item.unk .m{color:var(--amber)}
.ug{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin-bottom:10px}
.ug header h3{font-size:15px}.ug header small{display:block;font-size:12.5px;color:var(--amber);margin:1px 0 4px}
.uq{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:start;padding:9px 0;border-top:1px dashed var(--line)}
.uq p{font-size:14px;line-height:1.65}
.ust{all:unset;cursor:pointer;font-size:12px;font-weight:700;padding:3px 10px;border-radius:99px;border:1px solid var(--mute);color:var(--mute);white-space:nowrap}
.uq.s1 .ust{border-color:var(--amber);color:var(--amber);background:var(--amberbg)}
.uq.s2 .ust{border-color:var(--acc);color:#fff;background:var(--acc)}
.uq.s2 p{color:var(--mute)}
.copyg{all:unset;cursor:pointer;display:block;text-align:center;margin-top:8px;padding:7px;border:1px solid var(--line);border-radius:8px;font-size:13px;font-weight:700;color:var(--acc)}
.ubar{position:sticky;top:-12px;z-index:1;background:var(--paper);padding:6px 0;font-size:13px;color:var(--mute)}
.rtools{display:flex;gap:6px;margin-bottom:6px;position:sticky;top:-12px;z-index:1;background:var(--paper);padding:6px 0}
.rfilter{flex:1;min-width:0;font:inherit;font-size:14px;padding:7px 10px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--text)}
.rchip{all:unset;cursor:pointer;font-size:12.5px;font-weight:700;padding:6px 10px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--mute);white-space:nowrap}
.rchip.on{border-color:var(--amber);color:var(--amber);background:var(--amberbg)}
.rnone{font-size:14px;color:var(--mute);padding:12px;text-align:center}
.nav-dock{width:44px;height:44px}
.pager{margin-top:20px}
@media print{
 .app,main{height:auto!important;overflow:visible!important}
 .panel{display:block!important;page-break-before:always}
 .panel:first-child{page-break-before:auto}
 .more{display:block!important}
 .nav-dock,.nav-panel,.rtools,.pager,.chev,.ust,.copyg{display:none!important}
 .top{position:static}
}
"""

JS = r"""
(function(){
 var K='syria-founders-v1',S={};try{S=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
 function save(){try{localStorage.setItem(K,JSON.stringify(S))}catch(e){}}
 var fa=function(n){return n.toLocaleString('ar-EG')};
 document.addEventListener('click',function(ev){
  var b=ev.target.closest('.row>button');if(!b)return;
  b.parentElement.classList.toggle('open');
 });
 /* unknown questions: 0 not sent, 1 sent, 2 answered */
 var NAMES=['لم يُرسل','أُرسل','وصل الرد'];
 var uq=[].slice.call(document.querySelectorAll('.uq'));
 function paintU(){
  var a=0;uq.forEach(function(q){var s=(S.u&&S.u[q.id])||0;q.className='uq s'+s;q.querySelector('.ust').textContent=NAMES[s];if(s==2)a++});
  var c=document.getElementById('ucnt');if(c)c.textContent=fa(a)+' من '+fa(uq.length)+' وصل ردّه';
 }
 uq.forEach(function(q){q.querySelector('.ust').addEventListener('click',function(){
  S.u=S.u||{};S.u[q.id]=((S.u[q.id]||0)+1)%3;save();paintU();});});
 paintU();
 function copyText(t,btn){
  var done=function(){var o=btn.textContent;btn.textContent='تم النسخ';setTimeout(function(){btn.textContent=o},1400)};
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,function(){fb()})}else fb();
  function fb(){var a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.select();try{document.execCommand('copy');done()}catch(e){}a.remove()}
 }
 [].forEach.call(document.querySelectorAll('.copyg'),function(btn){btn.addEventListener('click',function(){
  var g=btn.closest('.ug'),who=g.dataset.who,qs=[].map.call(g.querySelectorAll('.uq p'),function(p,i){return fa(i+1)+'. '+p.textContent});
  copyText('السادة '+who+'،\nنرجو التكرم بالإفادة عن الأسئلة التالية:\n'+qs.join('\n')+'\nمع الشكر.',btn);
 })});
 /* reference filter */
 var rf=document.querySelector('.rfilter'),rows=[].slice.call(document.querySelectorAll('.row.ref')),only=false,none=document.querySelector('.rnone');
 function applyRef(){
  if(!rf)return;var q=rf.value.trim().toLowerCase(),shown=0;
  rows.forEach(function(r){
   var ok=(!q||r.textContent.toLowerCase().indexOf(q)>-1)&&(!only||r.classList.contains('open'));
   r.hidden=!ok;if(ok)shown++;if(q&&ok)r.classList.add('open');
  });
  [].forEach.call(document.querySelectorAll('#ref .grp'),function(g){
   var n=g.nextElementSibling,any=false;while(n&&!n.classList.contains('grp')){if(n.classList.contains('row')&&!n.hidden)any=true;n=n.nextElementSibling}
   g.hidden=!any;
  });
  none.hidden=shown>0;
 }
 if(rf){rf.addEventListener('input',applyRef);
  [].forEach.call(document.querySelectorAll('.rchip[data-only]'),function(c){c.addEventListener('click',function(){only=!only;c.classList.toggle('on',only);applyRef()})});
  var p=document.getElementById('rprint');if(p)p.addEventListener('click',function(){rows.forEach(function(r){r.hidden=false});window.print()});}
 /* links inside pages */
 document.addEventListener('click',function(ev){
  var a=ev.target.closest('a[data-page]');if(!a||a.closest('.nav-panel'))return;
  ev.preventDefault();window.__go(a.dataset.page);
 });
})();
"""
