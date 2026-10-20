#!/usr/bin/env python3
"""Founders reference site v2 (verified-only). One self-contained RTL HTML -> dist/index.html
Law: every 'ok' (verified) item MUST carry a source (article + page). The build fails otherwise.
Source of truth: SYTRA model licence for order-delivery platforms, 34 pp, 2023 (read as page images 2026-10-20).
No builder fee, no equity, no 'partnership', no personal titles anywhere in this file.
"""
import html, re, sys, pathlib, json

PDF = "https://sytpra.gov.sy/public/uploads/files/%D8%AE%D8%AF%D9%85%D8%A7%D8%AA%20%D8%A7%D9%84%D8%A7%D8%AA%D8%B5%D8%A7%D9%84%D8%A7%D8%AA/%D8%A7%D9%84%D8%AA%D8%B1%D8%A7%D8%AE%D9%8A%D8%B5%20%D8%A7%D9%84%D9%86%D9%85%D8%B7%D9%8A%D8%A9%20%D8%A7%D8%AA%D8%B5%D8%A7%D9%84%D8%A7%D8%AA/7.pdf"

OK, DESIGN, OPEN, MEAS = "ok", "design", "open", "meas"
CHIP = {OK: "من الوثيقة", DESIGN: "تصميم مقترح", OPEN: "غير مثبت", MEAS: "قياس المشروع"}

def esc(s): return html.escape(s, quote=False)
def num(s): return f'<bdi dir="ltr">{esc(s)}</bdi>'

def card(title, line, kind, src="", fig=None):
    if kind in (OK, MEAS) and not src:
        sys.exit(f"BUILD FAILED: verified card without source -> {title}")
    figh = f'<div class="fig">{fig}</div>' if fig else ""
    srch = f'<span class="src">{esc(src)}</span>' if src else ""
    return (f'<article class="card {kind}">{figh}<h3>{esc(title)}</h3><p>{line}</p>'
            f'<div class="meta"><span class="chip {kind}">{CHIP[kind]}</span>{srch}</div></article>')

# ---------- panel 1: the map ----------
stations = [
    ("١", "شركة تشغيلية في سوريا", "هي صاحبة الترخيص والمسؤولة قانونياً. شركة قيد التأسيس تُقبل.", OK, "م١ · ص٥"),
    ("٢", "ترخيص الهيئة الناظمة", "ترخيص نمطي غير حصري لمدة سنة، يتجدد.", OK, "م٥، م٦ · ص١٨"),
    ("٣", "المنصة", "محرك واحد وخمس واجهات، مستضافة داخل سوريا.", DESIGN, ""),
    ("٤", "اعتماد النسخة", "كل نسخة وكل تحديث بموافقة مسبقة قبل النشر.", OK, "الملحق ١ · ص٣٢"),
    ("٥", "إطلاق تجاري", "خلال ستة أشهر من سريان الترخيص، وإلا يُلغى.", OK, "م٦ (ب) · ص١٨"),
]
def station(n, t, l, k, s):
    if k == OK and not s: sys.exit("BUILD FAILED: station without source " + t)
    sp = f'<span class="src">{esc(s)}</span>' if s else ""
    return (f'<li><span class="dot">{n}</span><div class="st"><h3>{esc(t)}</h3><p>{esc(l)}</p>'
            f'<div class="meta"><span class="chip {k}">{CHIP[k]}</span>{sp}</div></div></li>')
route = "".join(station(*s) for s in stations)

P1 = f'''
<p class="lead">الطريق من الفكرة إلى أول طلب يمر بخمس محطات. المحطات المعلّمة «من الوثيقة» موثقة بمادتها وصفحتها في نظام الترخيص النمطي.</p>
<ol class="route">{route}</ol>
<div class="note"><b>منطقة العمل:</b> دمشق وريف دمشق. حي الإطلاق الأول يحدده المؤسسون.</div>
'''

# ---------- panel 2: company ----------
P2 = '<p class="lead">الترخيص لا يُمنح لشخص ولا لمنصة. يُمنح لشركة بعينها، وهي التي تتحمل المسؤولية كاملة.</p>' + "".join([
    card("شكل الشركة", "شركة محدودة المسؤولية أو مساهمة مغفلة، مؤسسة في سوريا. القبول ممكن بشركة قيد التأسيس بشرط تزويد الهيئة بالسجل التجاري قبل منح الترخيص.", OK, "م١ (١) · ص٥"),
    card("غاية الشركة", "يجب أن تتضمن غاية الشركة تقديم خدمة توصيل الطلبات عبر المنصات الإلكترونية، أو أن تتعهد بإضافتها إلى سجلها التجاري.", OK, "م١ (١) · ص٥"),
    card("سجل نظيف", "ألا يكون لطالب الترخيص ترخيص سابق أُلغي قبل أقل من سنتين، وألا يكون قد أُشهر إفلاسه.", OK, "م١ (٢، ٣) · ص٥"),
    card("المخوّلون بالتوقيع", "تُقدَّم أسماؤهم ونماذج توقيعهم، مع صورة هوية كل شخص طبيعي وارد اسمه في السجل التجاري وعنوانه وأرقام التواصل معه.", OK, "م٢ (٣، ٤) · ص٥"),
    card("تغيير الشركاء", "أي تغيير في أسماء الشركاء أو في نسب مساهمتهم يحتاج موافقة الهيئة المسبقة. وكذلك التنازل عن الترخيص أو الاندماج.", OK, "م٨ (أ، ب، هـ) · ص١٩"),
    card("التعاقد من الباطن", "لا يجوز إلا بعد موافقة الهيئة، وتبقى الشركة المرخّص لها مسؤولة مسؤولية كاملة.", OK, "م٩ (أ) · ص١٩"),
])

# ---------- panel 3: licence ----------
def bars():
    rows = [("السنة ١", 0), ("السنة ٢", 5), ("السنة ٣", 10), ("السنة ٤ وما بعد", 15)]
    cols = "".join(f'<div class="bar"><span class="h" style="height:{max(4, p*5)}px"></span>'
                   f'<b>{p}٪</b><i>{y}</i></div>' for y, p in rows)
    return f'<div class="bars">{cols}</div>'

P3 = '<p class="lead">ترخيص واحد من الهيئة الناظمة للاتصالات والبريد، بشروط محددة ومدفوعات معروفة مسبقاً.</p>' + "".join([
    card("نوع الترخيص", "نمطي وغير حصري: لا يمنع الهيئة من ترخيص غيرك، ولا يعطيك احتكاراً. وللهيئة أن تضيف لاحقاً أجوراً أو شروطاً.", OK, "م٥ (أ، ب) · ص١٨"),
    card("المدة والتجديد", "سنة من تاريخ السريان، قابلة للتجديد. يُقدَّم طلب التجديد قبل ثلاثة أشهر على الأقل من انتهاء المدة.", OK, "م٦ (أ) · ص١٨، م٧ · ص١٩"),
    card("مهلة الإطلاق", "الإطلاق التجاري خلال ستة أشهر من سريان الترخيص وإلا أُلغي، وتُبلَّغ الهيئة قبل الإطلاق بشهر على الأقل.", OK, "م٦ (ب، ج) · ص١٨", fig="٦ أشهر"),
    card("مدة البت في الطلب", "تُخطر الهيئة باستلام الطلب خلال خمسة عشر يوم عمل، وتبتّ فيه خلال مدة لا تتجاوز خمسة وأربعين يوماً من استكمال الوثائق. الموافقة الأولية ليست إذناً بتقديم الخدمة.", OK, "م٤ (أ، ب، ت) · ص٦", fig="٤٥ يوماً"),
    card("الرسوم وتعديلها", f'النص المنشور: بدل ابتدائي {num("500,000")} ل.س، وأجر سنوي {num("500,000")} ل.س، وأجر دراسة {num("100,000")} ل.س. وبحسب ما نُشر في الصحافة عدّل قرار للهيئة رقمه {num("264")} بتاريخ {num("19/4/2026")} هذه الأرقام، ولم نطّلع على نصه بعد.', OPEN, "النص: الملحق ٢ · ص٣٤. التعديل: خبر منشور، لم يُتحقق من نصه"),
    f'''<article class="card ok"><h3>حصة الهيئة من الإيراد</h3><p>تُسدَّد من الإيرادات الخاضعة لتقاسم الإيراد، طوال مدة الترخيص.</p>{bars()}<div class="meta"><span class="chip ok">من الوثيقة</span><span class="src">الملحق ٢ · ص٣٤</span></div></article>''',
])

# ---------- panel 4: platform ----------
P4 = '<p class="lead">شروط الهيئة تحدد شكل المنصة قبل أي قرار تقني. هذه الشروط كما وردت، ثم ما يترتب عليها في التصميم.</p>' + "".join([
    card("الاستضافة", "داخل الجمهورية العربية السورية، في مراكز استضافة تابعة للمرخّص له أو لجهات عامة قادرة على تقديمها.", OK, "الملحق ١ · ص٣٢"),
    card("التحديثات", "أي تحديث لنسخة المنصة يحتاج موافقة مسبقة قبل إتاحته للعموم.", OK, "الملحق ١ · ص٣٢"),
    card("حساب المستخدم", "رقم خلوي سوري حصراً، مع تحقق عبر رسالة نصية SMS.", OK, "الملحق ١ · ص٣٢"),
    card("رقم الطلب", "رقم تعريفي فريد لكل طلب يولّده النظام، ويصل إلى الزبون برسالة نصية.", OK, "الملحق ١ · ص٣٢"),
    card("صلاحيات التطبيق", "ثلاثة مصادر فقط على جهاز المستخدم: الموقع الجغرافي، الهاتف لإجراء مكالمة، ووحدة التخزين.", OK, "الملحق ١ · ص٣٢"),
    card("الخصوصية", "عرض سياسة الخصوصية وشروط الاستخدام بالعربية والإنجليزية عند أول تسجيل، وعند كل تحديث، وموافقة المستخدم شرط للاستخدام.", OK, "الملحق ١ · ص٣٢"),
    card("اطلاع الهيئة", "نفاذ دائم إلى قواعد البيانات للمخوّلين لدى الهيئة، بصلاحية القراءة فقط.", OK, "م١٠ (ب) · ص٢٠"),
    card("حفظ البيانات", "الاحتفاظ بكل بيانات المشتركين والمندوبين والبيانات المالية مدة تعادل مدة الترخيص على الأقل.", OK, "م١٠ (هـ) · ص٢٠"),
    '<h2 class="sec">ما يترتب على ذلك في التصميم</h2>',
    card("بنية المنصة", "محرك واحد تقوم عليه خمس واجهات: تطبيق الزبون، موقع الزبون، تطبيق المندوب، لوحة التاجر، لوحة التشغيل.", DESIGN),
    card("التغيير من السيرفر", "لأن كل تحديث بموافقة مسبقة، تُدار الأسعار والعروض والنصوص من إعدادات على الخادم لا بإصدار جديد.", DESIGN),
    card("سجل لا يُحذف", "كل طلب وكل حركة مالية تُسجَّل كحدث ثابت، تلبية لشرط الحفظ واطلاع الهيئة.", DESIGN),
    card("العنوان يُبنى من الناس", "في داريا ١٣٬٣٨٥ مبنى مرسوماً على الخريطة المفتوحة، لكن ٢ منها فقط عليها رقم بيت، و٢٦ طريقاً فقط من ٨٤٢ لها اسم. فالعنوان في الطلب أربعة حقول معاً: دبوس على الخريطة، وأقرب معلم، ووصف نصي، ورقم هاتف بديل.", MEAS, "قياس الخريطة المفتوحة لداريا · ١٨ أكتوبر ٢٠٢٦"),
    card("الفلوس بالليرة", "كل مبلغ يُخزَّن بالليرة السورية مع لقطة سعر الصرف وقت الحركة. أي عملة أخرى تُعرض للمرجع فقط. والسجل المالي يُضاف إليه ولا يُعدَّل.", DESIGN, "قرار تصميم المشروع"),
    card("دورة الطلب", "ست حالات: أُنشئ، أُكّد، قيد التحضير، جاهز، مع المندوب، سُلّم. وسبعة فروع للفشل لكل منها شاشة وسبب وخطوة تالية: رفض التاجر، نفاد صنف، إلغاء الزبون، فشل التوصيل، تأخر، نزاع، مرتجع جزئي.", DESIGN, "قرار تصميم المشروع"),
    card("الدفع", "الدفع عند الاستلام هو المسار الأول. المحافظ الإلكترونية تحتاج تسجيل التاجر بزيارة مركز وحساب بنكي، فتأتي بعد الإطلاق.", DESIGN, "بحث المشروع · سبتمبر ٢٠٢٦، لم يُعَد التحقق"),
    card("العمل عند ضعف الاتصال", "التطبيق يُصمَّم ليعمل ويُزامن لاحقاً عند انقطاع الشبكة أو الكهرباء.", DESIGN),
])

# ---------- panel 5: the road, spined on the licence's own clocks ----------
# Sequence only. Every dated item is a clock the licence itself fixes (article + page);
# everything before the licence takes effect has no clock and is shown as a step, not a date.
def before(n, t, l, k, s):
    return (f'<li><span class="dot">{n}</span><div class="st"><h3>{esc(t)}</h3><p>{esc(l)}</p>'
            f'<div class="meta"><span class="chip {k}">{CHIP[k]}</span><span class="src">{esc(s)}</span></div></div></li>')
BEFORE = [
    ("١", "تأسيس الشركة أو قيدها", "مع إضافة غاية توصيل الطلبات إلى السجل التجاري.", OK, "م١ · ص٥"),
    ("٢", "تقديم طلب الترخيص", "بالاستمارة المعتمدة والوثائق وأجر دراسة الطلب.", OK, "م٢ (٦) · ص٥"),
    ("٣", "بناء المنصة بالتوازي", "على الشروط الفنية في الملحق ١، وكل نسخة تُعتمد قبل إتاحتها.", OK, "الملحق ١ · ص٣٢"),
]
for *_x, k, s_ in BEFORE:
    if k == OK and not s_: sys.exit("BUILD FAILED: road step without source")

CLOCK = [  # (month, title, line, source, goal)
    (0, "سريان الترخيص", "من هذا التاريخ تُحسب كل المهل التالية. المدة سنة واحدة، غير حصرية.", "م٦ (أ) · ص١٨", False),
    (5, "آخر موعد لإبلاغ الهيئة بالإطلاق", "الإبلاغ قبل الإطلاق بشهر على الأقل، فإن أُطلق في آخر موعد كان الإبلاغ في الشهر الخامس.", "م٦ (ب، ج) · ص١٨", False),
    (6, "آخر موعد للإطلاق التجاري", "بعده يُلغى الترخيص. أول طلب حقيقي يجب أن يسبق هذا الموعد.", "م٦ (ب) · ص١٨", True),
    (9, "آخر موعد لطلب التجديد", "يُقدَّم قبل ثلاثة أشهر على الأقل من انتهاء المدة.", "م٧ · ص١٩", False),
    (12, "انتهاء المدة", "يبدأ العام الثاني بحصة للهيئة قدرها ٥٪ من الإيراد الخاضع، بعد عام أول بلا حصة.", "م٦ (أ) · ص١٨، الملحق ٢ · ص٣٤", False),
]
_m = [c[0] for c in CLOCK]
if _m != sorted(_m) or len(set(_m)) != len(_m): sys.exit("BUILD FAILED: road clock not in strict month order")
if any(not c[3] for c in CLOCK): sys.exit("BUILD FAILED: road clock item without source")
if sum(1 for c in CLOCK if c[4]) != 1: sys.exit("BUILD FAILED: road must have exactly one destination")
AR = "٠١٢٣٤٥٦٧٨٩"
ar = lambda n: "".join(AR[int(d)] for d in str(n))
def clock_li(m, t, l, s, goal):
    return (f'<li class="{"goal" if goal else ""}"><span class="mo"><b>{ar(m)}</b><i>شهر</i></span><div class="st"><h3>{esc(t)}</h3><p>{esc(l)}</p>'
            f'<div class="meta"><span class="chip ok">{CHIP[OK]}</span><span class="src">{esc(s)}</span></div></div></li>')

ASK = [  # (who answers, [questions]); every group must name who answers
    ("الهيئة الناظمة", ["نص القرار ٢٦٤ لسنة ٢٠٢٦ بشأن الرسوم، وهل غيّر نسب تقاسم الإيراد.", "ما المقصود بالإيرادات الخاضعة للتقاسم: عمولة المنصة أم قيمة الطلب."]),
    ("محامٍ سوري", ["متطلبات تأسيس الشركة ومدتها.", "هل إدارة المنصة من خارج سوريا تُعدّ تعاقداً من الباطن بحسب المادة ٩."]),
]
if any(not w or not q for w, q in ASK): sys.exit("BUILD FAILED: open item without a named answerer")
askh = "".join(f'<div class="askg"><h3>{esc(w)}</h3>' + "".join(f"<div class=\"q\">{esc(x)}</div>" for x in q) + "</div>" for w, q in ASK)

P5 = f'''
<div class="dest"><small>الوجهة</small><b>الإطلاق التجاري</b><span>آخر موعد له الشهر السادس من سريان الترخيص.</span></div>
<h2 class="sec first">قبل سريان الترخيص</h2>
<p class="lead">لا مهلة محددة في الوثيقة لهذه المرحلة. الترتيب هو المهم.</p>
<ol class="route">{"".join(before(*x) for x in BEFORE)}</ol>
<h2 class="sec">بعد سريان الترخيص</h2>
<p class="lead">كل رقم هنا مهلة تفرضها الوثيقة نفسها.</p>
<ol class="clock">{"".join(clock_li(*c) for c in CLOCK)}</ol>
<div class="note">أي تغيير في الشركاء أو نسبهم يحتاج موافقة الهيئة قبل التنفيذ، في أي مرحلة من هذا الطريق. م٨ · ص١٩</div>
<h2 class="sec">يُؤكَّد قبل التقديم</h2>
{askh}
'''
if 'class="card open"' in P5: sys.exit("BUILD FAILED: unverified cards do not belong on the road")

tabs = [("map", "الخريطة", P1, "١"), ("company", "الشركة", P2, "٢"), ("licence", "الترخيص", P3, "٣"),
        ("platform", "المنصة", P4, "٤"), ("road", "الطريق", P5, "٥")]

CSS = """
:root{--paper:#f3efe6;--card:#fbf9f4;--text:#17202a;--mute:#5d6670;--line:#d9d2c3;--acc:#14532d;--amber:#8a5a00;--amberbg:#fbf1dc}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{background:var(--paper);color:var(--text);font-family:"IBM Plex Sans Arabic","Cairo","Almarai","Noto Naskh Arabic",Tahoma,system-ui,sans-serif;line-height:1.75;-webkit-font-smoothing:antialiased}
.app{max-width:720px;margin:0 auto;height:100dvh;display:flex;flex-direction:column;border-inline:1px solid var(--line);background:var(--paper)}
.top{padding:18px 20px 14px;border-bottom:1px solid var(--line)}
.kicker{font-size:12px;color:var(--acc);letter-spacing:.04em;font-weight:700}
h1{font-size:22px;line-height:1.35;margin-top:2px}
.sub{font-size:13px;color:var(--mute)}
main{flex:1;overflow-y:auto;overflow-x:hidden;padding:18px 18px 28px}
.panel{display:none}.panel.on{display:block}
.lead{font-size:14.5px;color:var(--mute);margin-bottom:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 15px;margin-bottom:11px}
.card h3,.st h3{font-size:15.5px;line-height:1.45;margin-bottom:3px}
.card p,.st p{font-size:14px;color:#2b3641}
.card.open{background:var(--amberbg);border-color:#e6d3a3}
.card.design{border-style:dashed}
.fig{font-size:30px;font-weight:800;color:var(--acc);line-height:1.1;margin-bottom:4px}
.meta{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:10px}
.chip{font-size:11.5px;padding:1px 9px;border-radius:99px;border:1px solid;font-weight:700}
.chip.ok{color:var(--acc);border-color:var(--acc)}
.chip.design{color:var(--text);border-color:var(--mute)}
.chip.open{color:var(--amber);border-color:var(--amber)}
.chip.meas{color:#1e3a8a;border-color:#1e3a8a}
.card.meas{border-inline-start:3px solid #1e3a8a}
.src{font-size:12px;color:var(--mute)}
.route{list-style:none;position:relative;margin:4px 0 14px}
.route::before{content:"";position:absolute;inset-block:12px;inset-inline-start:15px;width:2px;background:var(--line)}
.route li{position:relative;display:flex;gap:14px;margin-bottom:12px}
.dot{flex:none;width:32px;height:32px;border-radius:50%;background:var(--acc);color:#fff;display:grid;place-items:center;font-weight:800;font-size:14px;z-index:1}
.st{flex:1;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:11px 14px}
.note{border-inline-start:3px solid var(--acc);padding:6px 12px;font-size:14px;background:var(--card)}
.sec{font-size:16px;margin:20px 0 8px;padding-top:12px;border-top:1px solid var(--line)}
.bars{display:flex;gap:10px;align-items:flex-end;margin:12px 0 2px;height:104px}
.bar{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:2px}
.bar .h{width:100%;background:var(--acc);border-radius:5px 5px 0 0;display:block}
.bar b{font-size:15px}.bar i{font-style:normal;font-size:11px;color:var(--mute);text-align:center;line-height:1.3}
.tabs{display:grid;grid-template-columns:repeat(5,1fr);border-top:1px solid var(--line);background:var(--card)}
.tabs button{all:unset;cursor:pointer;text-align:center;padding:9px 2px 10px;font-size:12.5px;color:var(--mute);display:flex;flex-direction:column;align-items:center;gap:2px}
.tabs button b{width:22px;height:22px;border-radius:50%;border:1px solid var(--line);display:grid;place-items:center;font-size:11px}
.tabs button[aria-selected=true]{color:var(--acc);font-weight:700}
.tabs button[aria-selected=true] b{background:var(--acc);color:#fff;border-color:var(--acc)}
.sec.first{border-top:0;margin-top:14px;padding-top:0}
.dest{background:var(--text);color:#f3efe6;border-radius:14px;padding:15px 16px 14px}
.dest small{font-size:12px;opacity:.7;letter-spacing:.04em}
.dest b{display:block;font-size:21px;line-height:1.4}
.dest span{font-size:14px;opacity:.88}
.clock{list-style:none;position:relative;margin:6px 0 14px}
.clock::before{content:"";position:absolute;inset-block:12px;inset-inline-start:24px;width:2px;background:var(--line)}
.clock li{position:relative;display:flex;gap:12px;margin-bottom:11px;align-items:flex-start}
.mo{flex:none;width:50px;border-radius:12px;background:var(--card);border:2px solid var(--acc);text-align:center;padding:3px 0 4px;z-index:1;line-height:1.1}
.mo b{display:block;font-size:22px;color:var(--acc)}.mo i{font-style:normal;font-size:11px;color:var(--mute)}
.clock li.goal .mo{background:var(--acc)}.clock li.goal .mo b,.clock li.goal .mo i{color:#fff}
.clock li.goal .st{border:2px solid var(--acc)}
.note{margin:4px 0 6px}
.askg{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:11px 14px;margin-bottom:10px}
.askg h3{font-size:14.5px;color:var(--acc);margin-bottom:2px}.askg .q{font-size:14px;padding:2px 0}
.foot{margin-top:18px;font-size:12px;color:var(--mute);border-top:1px solid var(--line);padding-top:10px}
.foot a{color:var(--acc)}
"""

JS = """
const T=[...document.querySelectorAll('.tabs button')],P=[...document.querySelectorAll('.panel')],M=document.querySelector('main');
function go(id){T.forEach(b=>b.setAttribute('aria-selected',b.dataset.t===id));P.forEach(p=>p.classList.toggle('on',p.id===id));M.scrollTop=0;history.replaceState(null,'','#'+id)}
T.forEach(b=>b.onclick=()=>go(b.dataset.t));
go(P.some(p=>p.id===location.hash.slice(1))?location.hash.slice(1):'map');
"""


# ================= NAVIGATOR (the FAB) =================
# The bottom tab bar is gone: the compass dock replaces it, exactly as on me.kariem.dev.
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from nav.compass import dial_svg

NAVCSS = (HERE / "nav" / "nav.css").read_text(encoding="utf-8")
NAVJS = (HERE / "nav" / "nav.js").read_text(encoding="utf-8")

# one bearing per page, evenly round the dial; the hint says what the page answers
PAGEMETA = {
    "map": (0, "الطريق من الفكرة إلى أول طلب"),
    "company": (72, "من يحمل الترخيص ويتحمل المسؤولية"),
    "licence": (144, "شروط الهيئة والرسوم والمدد"),
    "platform": (216, "ما الذي يُبنى وأين يُستضاف"),
    "road": (288, "المهل من سريان الترخيص حتى التجديد"),
}
TABLABEL = {i: t for i, t, _b, _n in tabs}
plain = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()

index = []          # every addressable item: (tab, id, title, line, kind)
def annotate(tab, body):
    n = [0]
    def card_sub(m):
        n[0] += 1; cid = f"c-{tab}-{n[0]}"
        inner = m.group(2)
        t = re.search(r"<h3>(.*?)</h3>", inner, re.S); p = re.search(r"<p>(.*?)</p>", inner, re.S)
        index.append((tab, cid, plain(t.group(1)), plain(p.group(1)) if p else "", m.group(1)))
        return f'<article id="{cid}" class="card {m.group(1)}">{inner}</article>'
    def st_sub(m):
        chip = re.search(r'class="chip (\w+)"', m.group(1))
        if not chip: return m.group(0)
        n[0] += 1; cid = f"c-{tab}-{n[0]}"
        t = re.search(r"<h3>(.*?)</h3>", m.group(1), re.S); p = re.search(r"<p>(.*?)</p>", m.group(1), re.S)
        index.append((tab, cid, plain(t.group(1)), plain(p.group(1)) if p else "", chip.group(1)))
        return f'<li id="{cid}">{m.group(1)}</li>'
    body = re.sub(r'<article class="card (\w+)">(.*?)</article>', card_sub, body, flags=re.S)
    body = re.sub(r"<li>(.*?)</li>", st_sub, body, flags=re.S)
    return body

if len(tabs) > 6: sys.exit("BUILD FAILED: more than 6 pages (standard: 4-6)")
order = [i for i, *_ in tabs]
panels = ""
for k, (i, t, body, nn) in enumerate(tabs):
    body = annotate(i, body)
    prev_i = order[k - 1] if k > 0 else None
    next_i = order[k + 1] if k < len(order) - 1 else None
    def pg(target, kind):
        if not target: return ""
        b = PAGEMETA[target][0]
        arrow = "السابق" if kind == "prev" else "التالي"
        return (f'<a class="{kind}" href="#{target}" data-page="{target}"><span class="nav-item-bearing" style="--bearing:{b}deg" aria-hidden="true">'
                f'<svg viewBox="0 0 16 16" width="22" height="22"><circle cx="8" cy="8" r="6.4"/><path d="M8 2.6 L9.7 8 L6.3 8 Z"/></svg></span>'
                f'<span><span class="pg-k">{arrow}</span><br><span class="pg-t">{esc(TABLABEL[target])}</span></span></a>')
    pager = f'<nav class="pager" aria-label="التنقل بين الصفحات">{pg(next_i, "next") or ""}{pg(prev_i, "prev") or ""}</nav>'
    panels += (f'<section class="panel" id="{i}" aria-label="{esc(t)}">{body}{pager}'
               f'<div class="foot">المرجع: <a href="{PDF}">نظام الترخيص النمطي لتقديم خدمة توصيل الطلبات عبر المنصات الإلكترونية</a>، '
               f'الهيئة الناظمة للاتصالات والبريد، ٣٤ صفحة، ٢٠٢٣. الأرقام موثقة بمادتها وصفحتها.</div></section>')

page_items = "".join(
    f'<a class="nav-item" href="#{i}" data-nav-item data-page="{i}" data-label="{esc((t + " " + PAGEMETA[i][1]).lower())}">'
    f'<span class="nav-item-bearing" style="--bearing:{PAGEMETA[i][0]}deg" aria-hidden="true"><svg viewBox="0 0 16 16" width="15" height="15">'
    f'<circle cx="8" cy="8" r="6.4"/><path d="M8 2.6 L9.7 8 L6.3 8 Z"/></svg></span>'
    f'<span class="nav-item-body"><span class="nav-item-label">{esc(t)}</span><span class="nav-item-hint">{esc(PAGEMETA[i][1])}</span></span>'
    f'<span class="nav-item-meta">{PAGEMETA[i][0]}°</span></a>'
    for i, t, _b, _n in tabs)
item_rows = "".join(
    f'<a class="nav-item" href="#{tab}" data-nav-item data-page="{tab}" data-card="{cid}" data-label="{esc((title + " " + line + " " + TABLABEL[tab]).lower())}">'
    f'<span class="sdot {kind}" aria-hidden="true"></span>'
    f'<span class="nav-item-body"><span class="nav-item-label">{esc(title)}</span><span class="nav-item-hint">{esc(line[:90])}</span></span>'
    f'<span class="nav-item-meta">{esc(TABLABEL[tab])}</span></a>'
    for tab, cid, title, line, kind in index)
navdata = json.dumps({i: {"bearing": PAGEMETA[i][0], "label": t} for i, t, _b, _n in tabs}, ensure_ascii=False)

SEARCH_SVG = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><line x1="16.5" y1="16.5" x2="21" y2="21"></line></svg>'
DOCK = (f'<div class="nav-dock"><span class="nav-dock-hint" aria-hidden="true"><span class="nav-dock-place">الخريطة</span></span>'
        f'<button type="button" class="nav-compass" data-navigator-open aria-haspopup="dialog" aria-expanded="false" '
        f'aria-keyshortcuts="Meta+K Control+K" aria-label="فتح التنقل" style="--bearing:0deg;--ring-c:{__import__("nav.compass",fromlist=["x"]).RING_C}">{dial_svg()}</button></div>')
PANEL = (f'<dialog class="nav-panel" data-navigator-panel aria-label="التنقل" tabindex="-1"><div class="nav-panel-inner" tabindex="-1">'
         f'<div class="nav-search">{SEARCH_SVG}<input type="text" name="destination" data-navigator-filter placeholder="إلى أين؟" aria-label="بحث في الصفحات والبنود" '
         f'autocomplete="off" autocapitalize="off" autocorrect="off" enterkeyhint="go" spellcheck="false"><kbd>esc</kbd></div>'
         f'<div class="nav-results" data-navigator-results>'
         f'<section class="nav-group" data-group="pages"><h2>الصفحات</h2>{page_items}</section>'
         f'<section class="nav-group" data-group="items"><h2>كل البنود</h2>{item_rows}</section>'
         f'<p class="nav-empty" data-navigator-empty hidden>لا يوجد بند بهذا الاسم.</p></div>'
         f'<footer class="nav-foot"><span><kbd>↑</kbd><kbd>↓</kbd> تنقل</span><span><kbd>↵</kbd> انتقال</span></footer></div></dialog>')
NOJS = ('<noscript><style>.panel{display:block!important}.nav-dock{display:none}</style><nav class="nav-nojs" aria-label="الصفحات">'
        + "".join(f'<a href="#{i}">{esc(t)}</a>' for i, t, _b, _n in tabs) + '</nav></noscript>')

CSS += NAVCSS + """
.app{position:relative}
main{padding-bottom:104px}
.flash{animation:flash 1.6s var(--ease-out-expo)}
@keyframes flash{0%{box-shadow:0 0 0 3px rgb(var(--accent)/.55)}100%{box-shadow:0 0 0 3px rgb(var(--accent)/0)}}
.kicker .pos{color:var(--mute);font-weight:600;margin-inline-start:6px}
"""

JS = """
const P=[...document.querySelectorAll('.panel')],M=document.querySelector('main'),K=document.querySelector('.kicker'),NAMES=%s;
function go(id){
  if(!P.some(p=>p.id===id))id='map';
  P.forEach(p=>p.classList.toggle('on',p.id===id));
  M.scrollTop=0; history.replaceState(null,'','#'+id);
  const i=P.findIndex(p=>p.id===id); K.innerHTML='وثيقة مرجعية للمؤسسين<span class="pos">· '+NAMES[id]+' · '+(i+1).toLocaleString('ar-EG')+' من '+P.length.toLocaleString('ar-EG')+'</span>';
  if(window.__navSync)window.__navSync(id);else window.__navPending=id;
}
window.__go=go;
go(location.hash.slice(1)||'map');
""" % json.dumps({i: t for i, t, _b, _n in tabs}, ensure_ascii=False)

PAGE = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>منصة توصيل الطلبات: الأساس القانوني والتقني</title><script>document.documentElement.classList.add('js')</script><style>{CSS}</style></head>
<body>{NOJS}<div class="app"><header class="top"><div class="kicker">وثيقة مرجعية للمؤسسين</div><h1>منصة توصيل الطلبات</h1><div class="sub">الأساس القانوني والتقني، دمشق وريف دمشق</div></header>
<main>{panels}</main>{DOCK}{PANEL}</div><script type="application/json" id="nav-data">{navdata}</script><script>{JS}</script><script>{NAVJS}</script></body></html>'''

# --- hard checks on the final visible text ---
text = re.sub(r"<style.*?</style>|<script.*?</script>|<[^>]+>", " ", PAGE, flags=re.S)
banned = ["شراكة", "بدري", "Bosla", "بوصلة", "MVP", "$", "دولار", "8,000", "8k"]
bad = [b for b in banned if b in text] + (["الأب"] if re.search(r"(?<![\u0621-\u064A])الأب(?![\u0621-\u064A])", text) else [])
if bad: sys.exit("BUILD FAILED: banned token(s): " + ", ".join(bad))
if "[truncated]" in PAGE: sys.exit("BUILD FAILED: truncated literal")
out = HERE / "dist"; out.mkdir(exist_ok=True)
(out / "index.html").write_text(PAGE, encoding="utf-8")
print("ok bytes", len(PAGE), "tabs", len(tabs), "indexed items", len(index))
