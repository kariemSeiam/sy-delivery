# The Proposal — Build Brief

> Internal. This is the spec for `proposal/index.html`, the document that goes to the owners.
> Standard to beat: `bashra-playbook.html` (17 chapters, idea → market, Arabic-first, dense but readable).

---

## Who reads this

**Egyptian owners.** They own the idea. They are hiring Bosla to build AND operate the infrastructure.

| They already believe | They need proof of |
|---|---|
| Syria is worth entering | **We can execute it** |
| Delivery apps work | **The Syrian constraints are survivable** |
| The market has room | **The unit economics close at 122 SYP/USD** |
| — | **What it costs to keep running** |

**They have Egyptian reflexes, not Syrian ones.** They know Talabat, Breadfast, Rabbit, Elmenus.
They do NOT have instincts for: 35.8% internet penetration, daily power cuts killing phones mid-delivery,
A2P marketing SMS being illegal, OSM having real holes in the streets, **Syria not being a Play Store country**.

→ Every Syrian constraint needs an Egyptian bridge: *"this is like X in Cairo, except Y breaks."*

## What this document asks for

A **build + operate contract**. Not investment, not partnership. Pure client, Bosla is the executor.
Includes: build scope, average period, deliverables, sources, running costs (VPS + subscriptions), and the deal.

## Language

Arabic body (Egyptian dialect, as the brain already is) · **English for numbers, architecture terms, and deal terms.**

---

## The three findings that rebuild the architecture

### 1. 🔴 Syria is not a Play Store country — C12's reasoning is WRONG

The brain says: *"Google Play Console is restricted for SYRIAN entities → Bosla (Egyptian) publishes on their behalf."*

**Verified live 2026-09-08:** Syria is absent from Google Play's official 225-location distribution table
AND absent from Apple Media Services. **Egyptian ownership does not fix this.** The constraint was never
about the publisher — it's about the destination.

**Consequences:**
- Android = **self-hosted APK from day one.** Not a fallback. The primary channel.
- iOS = effectively blocked. Browsing works on mobile data (MTN/Syriatel LTE) since Feb 2026, downloads blocked on fixed-line.
- **The web app stops being surface #5 and becomes the second real surface.** PWA is not a nice-to-have.
- This *raises* the value of `0009-web-and-brand-layers` — the SSR store page was already the growth loop; now the web app is also the iOS strategy.

### 2. ✅ The sanctions blocker is gone

- US comprehensive Syria sanctions revoked **1 Jul 2025** (E.O. 14312)
- 31 CFR Part 542 deleted **25 Aug 2025**
- Caesar Act repealed **18 Dec 2025**
- **Google Maps Platform officially supports Syria** for Tiles, Geocoding, Driving & Walking Directions

→ D10 ("Google Maps availability UNCONFIRMED") is resolvable. An Egyptian entity can buy it.

### 3. 🔴 Street addresses do not exist in Latakia — C5 was righter than it knew

Measured: Latakia OSM has ~34,957 buildings but **no usable street addressing**.
Google returns **Plus Codes** (`GQ8V+82M, Latakia, Syria`), not street numbers.

**No provider at any price will turn a typed address into a rooftop pin.**

→ Pin-drop + landmark/POI search + saved locations is not a design preference. It is the only thing that works.
→ This *validates* C5 (`user_text` + `geocoded_text` both stored, landmark required) and makes it non-negotiable.
→ POI/landmark search IS the address substitute. That's why Google's POI quality matters commercially.

---

## Decisions applied in this document

| Decision | Change | Why |
|---|---|---|
| **E5** — master dashboard | ⬛ **KILLED** | Register itself said *"this is a product on its own, not a screen."* Survives as: zones · delivery pricing · manual dispatch · COD settlement |
| **D18** — heatmaps/geo analytics | ⏭️ Deferred to Phase 5 | Lost its home when E5 died. Must be explicitly deferred or it becomes scope creep |
| **C12** — publishing accounts | 🔄 **REWRITTEN** | Reasoning was wrong. New constraint: no store distribution to Syria at all |
| **D13** — Play Store availability | 🔄 **REWRITTEN** | Same. APK-first is now architectural, not a workaround |
| **D10** — maps/geo | ✅ Resolvable | Sanctions gone, Google supports Syria, but addresses don't exist → hybrid stack |
| **D1** — ownership | ⚠️ Reopened **commercially** | Egyptian owners removes the *legal* pressure; the VPS bundle adds *commercial* pressure. Needs Kariem's sentence |
| **B2** — code ownership | Stays locked | Client owns code. Bosla separately operates infra as a paid service. Must be stated out loud |
| **Manual dispatch** | ✅ Correct by design | Phase 2 wants it. Auto-dispatch before 100 real orders = optimising an imagined problem |

---

## The deal architecture — already written, never noticed

`sequence.md` has six phases, each gated on a **real-world outcome**, not a date.
That is a payment schedule that has been sitting there as engineering sequencing.

| Phase | Gate — what must actually be TRUE |
|---|---|
| 0 — Decisions, no code | D1, B1+B3, C2, D4 locked |
| 1 — Foundation that can't be fixed later | A fake order completes full lifecycle **including cancel + refund**, ledger balances |
| 2 — First real journey | **20 real orders in Latakia with real couriers.** Not a demo |
| 3 — Merchant weapon | **5 merchants shared their link unprompted** |
| 4 — Offline + full courier app | Built on actions we *watched happen* |
| 5 — Expansion | Latakia hits stable completion / complaint / repeat rates |

**Payment tied to gates, not calendar.** Most agencies bill monthly and the client absorbs slippage.
This says: *we don't get paid for Phase 2 until 20 real orders ran in Latakia.*
Honest, differentiated, and already written.

---

## Section plan — 15 current sections re-judged

Current deck sells "Syria is an opportunity." Owners already own the idea. ~27% of the deck sells them their own conviction.

| # | Section | Verdict |
|---|---|---|
| 01 | الملخّص التنفيذي | 🆕 **NEW** — what we're building, what it costs, how long, what you own |
| 02 | method + work | ⬆️ **PROMOTED to opener** — the only thing they need convincing of |
| 03 | market + competitors | ⬇️ **COMPRESSED** — 17 competitors → 3 that threaten Latakia. Reframe: opportunity → **timing risk** |
| 04 | intent | Keep, shrink. The certainty thesis is the spine |
| 05 | audience | Merge into journey |
| 06 | model (shell-host) | ✅ Keep — this is what they're buying |
| 07 | surfaces | 🔄 **REBUILT** — 6 surfaces re-counted after E5 death + APK reality |
| 08 | spine (category) | ✅ Keep — the moat |
| 09 | journey + demo | ✅ Keep + merge audience |
| 10 | lifecycle (failure branches) | ✅ Keep — failure IS the product |
| 11 | 🆕 **الأرض السورية** | **NEW** — the constraints as Egyptian bridges (no Play Store, no addresses, 35.8% internet, power cuts) |
| 12 | phases | ⬆️ **BECOMES the payment schedule** |
| 13 | 🆕 **التكلفة التشغيلية** | **NEW** — VPS, SMS, maps, stores, SaaS. The section that doesn't exist and Kariem named it |
| 14 | honesty | ✅ Keep — the trust move, genuinely rare |
| 15 | deal | 🔴 **REBUILT FROM NOTHING** — currently refuses to answer the question |

---

## Numbers that are load-bearing and must be handled honestly

| Number | Status | Handling |
|---|---|---|
| **122.00 SYP/USD** | ✅ Verified, Central Bank direct | Use everywhere. Every FX-dependent figure re-derived |
| **BeeOrder 22% implied take rate** | ⚠️ **Single low-credibility source** | Brain itself flags: *"needs a second source before B3 is built on it."* State as ASSUMPTION out loud, or verify. Quietly leaning on it undermines the whole honesty pitch |
| **BeeOrder 120k orders/month** | Rest of World (higher credibility) | Usable as market-scale anchor |
| **$15 avg order value** | Derived, raw | Mark as preliminary |
| **35.8% internet penetration** | ✅ Verified | Core constraint, drives offline-first |
| **$100-250/mo courier income** | ✅ Verified | Drives B6 |

---

## Craft standard (from bashra-playbook)

- Arabic RTL, `Almarai` display + `IBM Plex Sans Arabic` body + `IBM Plex Mono` for numbers
- Token-driven CSS, 4pt spacing scale, semantic colours
- **Real UI wireframes rendered in HTML/CSS**, not screenshots — the home screen, the store card, the failure states
- Numbered chapters with intro paragraphs
- Callouts: warn / rose / info
- Data tables with `yes`/`no` cells
- KPI blocks, timeline, flow diagrams
- Sticky sidebar TOC + scroll progress
- Self-contained single file, no build step
