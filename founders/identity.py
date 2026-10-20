"""Visual identity for the founders site: one place for type, palette and the star.

Idea: quiet authority. One ink-blue, one hairline brass rule under the masthead, terracotta only
for what is not settled. Amiri carries titles and big numbers, IBM Plex carries every sentence.
No mark, no pattern: the navigator compass (from me.kariem.dev) is the only drawn object.
"""
import base64, pathlib

HERE = pathlib.Path(__file__).parent

def _face(family, weight, fname):
    b = base64.b64encode((HERE / "fonts" / fname).read_bytes()).decode()
    return (f"@font-face{{font-family:{family};font-weight:{weight};font-style:normal;font-display:swap;"
            f"src:url(data:font/woff2;base64,{b}) format('woff2')}}")

FONTS = "".join([_face("Amiri", 700, "Amiri-700.woff2"),
                 _face("PlexAr", 400, "IBMPlex-400.woff2"),
                 _face("PlexAr", 700, "IBMPlex-700.woff2")])

STAR = ('<svg class="star" viewBox="0 0 32 32" aria-hidden="true"><path d="M16 2 L19.5 12.5 L30 16 L19.5 19.5 L16 30 L12.5 19.5 L2 16 L12.5 12.5 Z" fill="currentColor"/></svg>')
# eight points = two squares; this is the drawn one, a true octagram
STAR8 = ('<svg class="seal" viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="18.5" fill="none" stroke="currentColor" stroke-width="1.2"/>'
         '<circle cx="20" cy="20" r="15.6" fill="none" stroke="currentColor" stroke-width=".6"/>'
         '<g fill="currentColor"><rect x="10.5" y="10.5" width="19" height="19"/><rect x="10.5" y="10.5" width="19" height="19" transform="rotate(45 20 20)"/></g>'
         '<circle cx="20" cy="20" r="4.1" fill="var(--paper)"/><circle cx="20" cy="20" r="1.7" fill="currentColor"/></svg>')

PALETTE = {  # old hard-coded value -> new
    "#14532d": "#1f3b64", "#e8f1ea": "#e3e8f1", "#8a5a00": "#8f4a14", "#6b4600": "#6a3410",
    "#e1c98e": "#e0bd98", "#efe9db": "#e8dfca", "#1e3a8a": "#2e6a58", "#fbf1dc": "#f7e9d6",
    "#e6d3a3": "#e0bd98", "#f3efe6": "#f1ecdf", "#fbf9f4": "#faf7ef", "#17202a": "#1b2330",
    "#d9d2c3": "#d8cfb9", "#5d6670": "#5b6270", "#2b3641": "#27303c", "#2b3640": "#27303c",
}

CSS = r"""
/* ---- identity.py: quiet authority ---- */
:root{--paper:#f3efe4;--card:#fbf9f2;--text:#1b2330;--mute:#555d6b;--line:#dcd3be;--acc:#1f3b64;--amber:#8f4a14;--amberbg:#f8ecda;--brass:#a8843a;
 --accent:31 59 100;--ink:27 35 48;--canvas:243 239 228;--canvas-secondary:251 249 242;--canvas-tertiary:234 226 207;--border:220 211 190;--border-secondary:228 221 202;--ink-secondary:85 93 107;--ink-tertiary:125 130 141;
 --serif:Amiri,"Noto Naskh Arabic",serif;--sans:PlexAr,"IBM Plex Sans Arabic",Cairo,Tahoma,system-ui,sans-serif}
body{font-family:var(--sans);font-feature-settings:"kern","liga";background:var(--paper)}
.app{background:var(--paper)}
/* masthead: text only, one brass hairline */
.top{padding:11px 18px 10px;border-bottom:1px solid var(--brass);background:var(--paper);position:relative}
.top .mast{display:flex;flex-direction:column}
.top h1{font-family:var(--serif);font-weight:700;font-size:21px;line-height:1.3;color:var(--text)}
.top .kicker{font-size:12.5px;color:var(--mute);display:flex;gap:8px;align-items:center}
.kicker .kn{font-weight:700;color:var(--acc)}
.kicker .kp{border:0;background:none;padding:0;color:var(--mute);font-size:12.5px}
.kicker .kp::before{content:"\00B7";margin-inline-end:8px;color:var(--brass);font-weight:700}
/* type: serif only for titles + big numerals; floor of 13px elsewhere */
.hq{font-family:var(--serif);font-weight:700;font-size:26px;line-height:1.4;margin:6px 0 4px}
.n,.rf-fig,.tile .n{font-family:var(--serif);font-weight:700;color:var(--acc)}
.n{font-size:26px;white-space:nowrap}.row>button .n{font-size:25px}.row>button .n.long{font-size:19px}.tile .n{font-size:38px;line-height:1.05}
.n small,.rt .m,.grp small,.tile bdi,.src,.chip{font-size:13px}
.grp{font-family:var(--serif);font-size:17px;font-weight:700;color:var(--text);margin:22px 2px 8px}
.rt{font-weight:700}
.legend,.foot{font-size:13px}
/* surfaces: paper + hairline, no shadow */
.row,.tile,.stp,.ug{background:var(--card);border-color:var(--line);border-radius:10px}
.row.open{border-color:#b7aa8b}.row.open>button{background:#f4efe1}
.tile bdi{background:#ebe3cf;color:var(--mute);display:block;width:fit-content;max-width:100%;text-wrap:balance;line-height:1.55;padding:2px 8px}
.strip .stp.now{background:var(--acc);border-color:var(--acc)}
.strip .stp.now i,.strip .stp.now b{color:#fff}
.strip .stp i{font-family:var(--serif);font-size:19px}
/* not settled: terracotta, with a stamped heading */
.open-sec{background:var(--amberbg);border:1px solid #e0bd98;border-radius:10px}
.open-sec h2{display:inline-block;font-family:var(--serif);font-size:16px;border:1.5px solid var(--amber);border-radius:6px;padding:0 10px;margin-bottom:6px}
.open-sec li span{color:#7a4115;font-size:13px}
.mk.open{background:var(--amberbg)}
.more-link{color:var(--amber)}
.nextblk{background:var(--acc);border-radius:10px;border-top:3px solid var(--brass)}
.nextblk b{font-family:var(--serif);font-size:17px;opacity:1;color:#f3efe4}
.nextblk a{background:#f3efe4;color:var(--acc);min-height:44px;display:flex;align-items:center;justify-content:center}
.pager .pg-ar{background:#e3e8f1;color:var(--acc)}
.pager .pg-t{font-family:var(--serif);font-size:17px}
.pager a{min-height:56px}
/* touch targets >= 44px */
.ug header h3{font-family:var(--serif);font-size:17px}
.uq{min-height:44px}
.ust{min-height:34px;display:inline-flex!important;align-items:center;padding:4px 12px!important;font-size:13px!important;position:relative}
.ust::after{content:"";position:absolute;inset:-6px -4px}
.copyg{min-height:44px;display:flex!important;align-items:center;justify-content:center;font-size:14px!important}
.rcount{margin:6px 2px 0;font-size:13.5px;color:var(--mute);min-height:1.2em}
.rchip{min-height:44px;display:inline-flex!important;align-items:center;font-size:13.5px!important}
.rsearch input,.rsearch{min-height:44px}
.row>button{min-height:48px}
.uq.s2 .ust{background:var(--acc);border-color:var(--acc)}
/* three stages on the first page */
.strip{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:10px 0 4px}
.strip .stp{display:flex;flex-direction:column;align-items:center;gap:2px;padding:9px 4px;text-align:center;font-size:13px;line-height:1.35}
.strip .stp small{font-size:13px;color:var(--mute);font-weight:400}
.strip .stp.now small{color:#d8e0ee}
.stage{margin-top:4px}
.stage .grp{display:flex;align-items:baseline;flex-wrap:wrap;gap:4px 8px;margin:20px 2px 8px}
.stage .grp .sn{display:inline-grid;place-items:center;width:26px;height:26px;border-radius:50%;background:var(--acc);color:#fff;font-size:15px;line-height:1;flex:none;align-self:center}
.stage .grp small{flex-basis:100%;margin-inline-start:34px;margin-top:-2px;color:var(--mute);font-family:var(--sans);font-weight:400;font-size:13px}
.kn,.kp,.nav-dock-place,.nav-item-hint,.nav-item-meta,.nav-sheet h2,.nav-foot span{font-size:13px!important}
kbd{font-size:12px}
.row .more i{font-size:13px!important}
.tile .tsrc{display:flex;flex-wrap:wrap;gap:4px;margin-top:8px}
.tile .tsrc bdi{margin-top:0;unicode-bidi:isolate;white-space:nowrap}
.tile.quiet{background:var(--amberbg);border:1px dashed #d9b48a}
.tile.quiet .n{color:var(--amber)}
.tile.quiet bdi{background:#f0d8bb;color:#6f3a10}
/* per-item share link */
.share{all:unset;cursor:pointer;display:inline-flex;align-items:center;gap:6px;margin-top:10px;min-height:44px;padding:0 4px;color:var(--acc);font-size:13.5px;font-weight:700}
.share svg{width:16px;height:16px}
.share.ok{color:#2e6a58}
.pager .pg-k,.mk,.ug header small,.uq small,.open-sec li span,.row .more small,.row .more .src,.row .more p,.src bdi,.meta{font-size:13px}
.mk{padding:0 7px}
.src bdi{font-size:13px}
.more-link{display:inline-flex;align-items:center;min-height:44px;font-size:14px}
.foot a{display:inline-block;padding:6px 0;min-height:44px;line-height:1.6}
"""
