"""The compass dial as inline SVG. A line-for-line port of the geometry in
me.kariem.dev src/components/navigator/Compass.astro (same 64-unit viewBox,
same radii, same kite). Drawn here in Python because this site has no bundler.

needle -> which page you are in (bearing)
ring   -> how deep you are in it (scroll progress)
"""
import math

C = 32
RING_R = 24.6
RING_C = round(2 * math.pi * RING_R, 2)


def f(n):
    return round(n, 2)


def at(r, deg):
    a = math.radians(deg)
    return f(C + r * math.sin(a)), f(C - r * math.cos(a))


def arc(r, a0, a1):
    x0, y0 = at(r, a0)
    x1, y1 = at(r, a1)
    large = 1 if a1 - a0 > 180 else 0
    return f"M{x0} {y0}A{r} {r} 0 {large} 1 {x1} {y1}"


def graduations():
    g = {"minor": "", "quarter": "", "north": ""}
    for deg in range(0, 360, 10):
        quarter = deg % 90 == 0
        x0, y0 = at(26.9 if quarter else 28.1, deg)
        x1, y1 = at(30.2, deg)
        key = "north" if deg == 0 else ("quarter" if quarter else "minor")
        g[key] += f"M{x0} {y0}L{x1} {y1}"
    return g


def cardinals():
    out = ""
    for deg in (0, 90, 180, 270):
        x0, y0 = at(17.9, deg)
        x1, y1 = at(20.1, deg)
        out += f"M{x0} {y0}L{x1} {y1}"
    return out


def dial_svg():
    g = graduations()
    tip, tail, w = C - 16.2, C + 12, 3.9
    kite = f"{C},{tip} {C + w},{C} {C},{tail} {C - w},{C}"
    return f'''<svg class="nav-dial" viewBox="0 0 64 64" aria-hidden="true" focusable="false">
<defs>
<radialGradient id="nav-face-fill" cx="0.36" cy="0.3" r="0.95"><stop offset="0" class="nav-face-a"/><stop offset="1" class="nav-face-b"/></radialGradient>
<radialGradient id="nav-sheen-fill" cx="0.3" cy="0.22" r="0.75"><stop offset="0" class="nav-sheen-a"/><stop offset="1" class="nav-sheen-b"/></radialGradient>
<radialGradient id="nav-jewel-fill" cx="0.36" cy="0.3" r="0.85"><stop offset="0" class="nav-jewel-a"/><stop offset="0.55" class="nav-jewel-b"/><stop offset="1" class="nav-jewel-c"/></radialGradient>
<linearGradient id="nav-glint-fill" gradientUnits="userSpaceOnUse" x1="11.3" y1="32" x2="32" y2="11.3"><stop offset="0" stop-color="rgb(255 255 255)" stop-opacity="0"/><stop offset="0.5" stop-color="rgb(255 255 255)" stop-opacity="1"/><stop offset="1" stop-color="rgb(255 255 255)" stop-opacity="0"/></linearGradient>
<filter id="nav-cast-blur" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="0.8"/></filter>
</defs>
<circle class="nav-bezel" cx="{C}" cy="{C}" r="31.3"/>
<path class="nav-bezel-glint" d="{arc(30.7, 282, 352)}"/>
<path class="nav-bezel-shade" d="{arc(30.7, 108, 172)}"/>
<path class="nav-grad" d="{g["minor"]}"/>
<path class="nav-grad quarter" d="{g["quarter"]}"/>
<path class="nav-grad north" d="{g["north"]}"/>
<circle class="nav-ring-track" cx="{C}" cy="{C}" r="{RING_R}"/>
<circle class="nav-face" cx="{C}" cy="{C}" r="22.3"/>
<path class="nav-dish" d="{arc(21.2, 250, 30)}" filter="url(#nav-cast-blur)"/>
<circle class="nav-sheen" cx="{C}" cy="{C}" r="22.3"/>
<path class="nav-cardinals" d="{cardinals()}"/>
<path class="nav-glint" d="{arc(20.7, 266, 352)}"/>
<path class="nav-rim" d="{arc(20.7, 106, 160)}"/>
<g transform="translate(0.9 1.5)" class="nav-cast"><g class="nav-needle" filter="url(#nav-cast-blur)"><polygon points="{kite}"/></g></g>
<g class="nav-needle">
<polygon class="nav-point-lit" points="{C},{tip} {C - w},{C} {C},{C}"/>
<polygon class="nav-point-shade" points="{C},{tip} {C + w},{C} {C},{C}"/>
<polygon class="nav-tail-lit" points="{C},{tail} {C - w},{C} {C},{C}"/>
<polygon class="nav-tail-shade" points="{C},{tail} {C + w},{C} {C},{C}"/>
</g>
<circle class="nav-hub" cx="{C}" cy="{C}" r="4.3"/>
<circle class="nav-jewel" cx="{C}" cy="{C}" r="2.5"/>
<circle class="nav-jewel-glint" cx="31.2" cy="31.1" r="0.7"/>
</svg>
<svg class="nav-gauge" viewBox="0 0 64 64" aria-hidden="true" focusable="false">
<g class="nav-depth"><circle class="nav-ring-fill" cx="{C}" cy="{C}" r="{RING_R}"/><circle class="nav-bead-halo" cx="{C}" cy="{C}" r="{RING_R}"/><circle class="nav-bead" cx="{C}" cy="{C}" r="{RING_R}"/></g>
</svg>'''
