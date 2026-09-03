<div align="center">

# 🧭 Latakia Super-App — Strategy Brain

### A shell-host architecture for a hyperlocal delivery super-app in Latakia, Syria — built against 8 competitors' documented failures, not a blank page

![Status](https://img.shields.io/badge/status-strategy%20phase-1f6feb)
![License](https://img.shields.io/badge/license-proprietary-red)
![Docs](https://img.shields.io/badge/docs-Arabic--first-2ea44f)
![Visibility](https://img.shields.io/badge/visibility-private-lightgrey)

**[The Bet](#-the-bet) · [The Model](#-the-model) · [Decisions](#-decisions) · [Competitive Intel](#-competitive-intel) · [Navigate the Brain](#-navigate-the-brain) · [Constraints](#-constraints) · [Structure](#-repo-structure)**

</div>

---

## ⚡ What this is

This is not the product. It's the brain that makes the product buildable without anyone — a new
developer, an AI agent, or us in two months — having to re-derive the reasoning from scratch.

Executed by **Bosla** · started **2026-08-31** · client name and the folder name (`sy-delivery`) are
placeholders until the brand decision locks (`REGISTER.md` → E1) — deliberately deferred, not an
oversight. Naming it now, before positioning is known, would be a name chosen with incomplete
information.

---

## 🎯 The bet

We're not entering an empty market. **8+ competitors already operate in Syria**, the oldest since 2016,
one (Talabatey) headquartered in Latakia itself. The fight isn't first-mover — it's **trust**.

Real complaints, pulled verbatim from the market leader's own reviews:

> *"Delivery fees are so high they add up to the price of the food itself."*
> *"The courier's photo in the app isn't who actually shows up."*

Neither complaint is really about price or the photo. Both are about the same thing: **being
surprised.** Surprised by the bill after building a full cart. Surprised by a stranger at the door.

And this is a country where everything else got redrawn in two years — the government changed, the
currency was redenominated (two zeros dropped, January 2026), electricity comes and goes at a shifting
price, and the internet went dark for 75% of the country in a single day from a February cyberattack.

**So what's being sold isn't food. It's one moment a day that goes exactly as promised.**

Every constraint in the brain — fees shown before entry, silence treated as a lie, real courier photos,
computed time windows, one currency format — is that same sentence written six ways. Full reasoning in
[`brain/intent.md`](brain/intent.md).

---

## 🏗 The model

Not an app with sections. A **host that loads shells** — one identity / session / address / payment /
ledger layer, wearing a different product on top depending on city, vertical, and merchant config.
Proven live, not theorized: Talabatey Iraq ships exactly this pattern across 3 countries
([teardown](brain/teardown/talabatey-iq.md)).

```
                         ┌───────────────────────────┐
                         │            HOST              │
                         │  identity · session · geo     │
                         │  address · cart · payment       │
                         │            · ledger               │
                         └──────────────┬─────────────────┘
                                        │ loads a shell by: city + vertical + merchant config
              ┌─────────────────────────┼─────────────────────────┐
              ▼                         ▼                         ▼
      DELIVERY SHELL              MARKETPLACE SHELL           ERRAND SHELL ("hatly")
      restaurants / meals          SKU · weight · stock         no catalog at all
      3 tabs, instant              stock filters, multi-cart     free text → quote → fulfil
```

A 4th shell (fashion/electronics commerce) was in the original model — **cancelled 2026-09-02**,
Kariem's direct call, not a research finding. Current scope is these 3. Full ownership rules and the
open conflict with the business model (D1) in
[`brain/decisions/0004-shell-host.md`](brain/decisions/0004-shell-host.md).

---

## 📊 Decisions

65 rows tracked. 1 (**E1** — brand identity) is deliberately deferred and excluded from the denominator
by design. **64 counted decisions:**

| | Count | Share |
|---|---:|---:|
| 🔒 Locked (agreed — won't reopen without a written reason) | 3 | ≈4.7% |
| 📝 Draft (strong opinion, needs confirmation) | 34 | ≈53.1% *(counted at half-credit)* |
| ⬜ Empty (not even an opinion yet) | 27 | — |
| **Effective coverage** | | **≈31.3%** |

Source of truth: [`brain/REGISTER.md`](brain/REGISTER.md) — this is a point-in-time snapshot, not
synced automatically. Any coverage number elsewhere in this repo is stale by definition.

The one locked decision that matters most — **A1: first city is Latakia.** Delegated to research
(606k population, 2026, sourced): a tight market, not a huge one, with less named competition than
Aleppo or Damascus and a real timing window before better-funded rivals arrive.

**Open and blocking — needs Kariem's word, not more research:**

1. **D1 — ownership conflict.** "One shared infrastructure, one dashboard for everything" (multi-tenant)
   and "fully client-owned" (single-tenant) can't both be true. 3 resolutions ranked in
   [`0014-ownership-models.md`](brain/decisions/0014-ownership-models.md) — likely hybrid: the client's
   data and branding are fully theirs, the shared infrastructure stays Bosla's.
2. **Q6/Q7** — contracted merchants? Budget and timing? Blocks B1, B4, F1–F3 — not researchable, only
   answerable.
3. **D8/G2** — courier employment model (employee vs. freelance), needed before the dispatch engine
   can lock.

<details>
<summary><b>All 14 architecture decisions (ADRs)</b></summary>
<br>

| # | Decision | Status |
|---|---|---|
| [0001](brain/decisions/0001-surfaces.md) | Surfaces — now 5, after 0009 | Draft |
| [0002](brain/decisions/0002-order-lifecycle.md) | Order lifecycle + 7 failure branches | Draft |
| [0003](brain/decisions/0003-dual-currency.md) | Dual currency as a UX pattern | Draft |
| [0004](brain/decisions/0004-shell-host.md) | **Shell-host architecture** — conflicts with D1 | Draft ⚠️ |
| [0005](brain/decisions/0005-guest-first.md) | Guest journey — wall only at payment | Draft |
| [0006](brain/decisions/0006-address-model.md) | Address model — store both forms | Draft |
| [0007](brain/decisions/0007-home-anatomy.md) | Home screen anatomy | Draft |
| [0008](brain/decisions/0008-category-spine.md) | Category spine — the secret | Draft |
| [0009](brain/decisions/0009-web-and-brand-layers.md) | Web + storefront pages + brand layers | Draft |
| [0010](brain/decisions/0010-offline-sync.md) | Offline sync — outbox + conflict matrix | Draft |
| [0011](brain/decisions/0011-catalog-shapes.md) | Catalog shapes — one polymorphic table | Draft |
| [0012](brain/decisions/0012-city-partition.md) | City partitioning — zone as pricing unit | Draft |
| [0013](brain/decisions/0013-launch-playbook.md) | Latakia launch playbook | Draft |
| [0014](brain/decisions/0014-ownership-models.md) | 3 ownership models — resolves D1 | Draft, open |

</details>

---

## 🔍 Competitive intel

The real threat circle for Latakia, narrowed from 9 competitors scanned for actual download numbers
([scan](brain/teardown/competitor-scale-scan.md)):

| Competitor | What's confirmed |
|---|---|
| 🔴 **BeeOrder** | Confirmed breach of the "no silence" and "real courier" rules. 462k downloads, 4.0★. [teardown](brain/teardown/beeorder.md) |
| 🔴 **Movo** | The only one genuinely popular — 100k+ downloads, 2,516 reviews, 4.2–4.7★. The single worst trust breach found across the whole scan: a real, readable App Store review reporting an account ban *after* the user contacted support about a problem the app itself caused. [teardown](brain/teardown/movo.md) |
| 🟡 **Labby** | Best-funded by far — $10M raised from Saudi/UAE investors, July 2026, the first institutional foreign funding any Syrian tech startup has received. Damascus-only today, Aleppo next, Latakia after — a real timing window, not a false one. |
| ⚪ **Talabatey** | Weakest of the confirmed four locally — but its Iraqi sibling is the architecture reference for the shell-host model. [teardown](brain/teardown/talabatey-iq.md) |
| ⚪ **Wee-Sy** | Closest philosophical model on paper, but the shipped app is transport-only with "0+" downloads — worth watching, not chasing. [teardown](brain/teardown/wee-sy.md) |

---

## 🗺 Navigate the brain

| Start here | Why |
|---|---|
| [`brain/INDEX.md`](brain/INDEX.md) | The only entry point — everything else is linked from here |
| [`brain/REGISTER.md`](brain/REGISTER.md) | ⭐ Single source of truth for decision state |
| [`brain/intent.md`](brain/intent.md) | ⭐ Why the product exists at all — read before anything else |
| [`brain/constraints.md`](brain/constraints.md) | C1–C12, each earned by a documented failure |
| [`brain/sequence.md`](brain/sequence.md) | What gets built when, and behind which gate |
| [`brain/flows/`](brain/flows/README.md) | The four journeys — [first order](brain/flows/first-order.md) in full |
| [`brain/decisions/`](brain/decisions/) | Numbered architecture decision records |
| [`brain/teardown/`](brain/teardown/) | Competitor and reference teardowns |
| [`brain/research/`](brain/research/) | Sourced market scans |
| [`brain/OPEN.md`](brain/OPEN.md) | Client questions, research queues, running assumptions |
| [`pitch/latakia-file.html`](pitch/latakia-file.html) | The pitch deck |

---

## 📐 Constraints

12 rules, each earned by a documented failure — not a nice-sounding principle. Every one is written
with the failure it prevents, so it can be argued with evidence instead of treated as scripture.

| # | Rule | Earned by |
|---|---|---|
| C1 | Delivery fee shown on the merchant card, before entry | BeeOrder reviews (4.0★, 462k downloads): *"delivery fees so high they add up to the food price"* |
| C2 | Silence is a lie — every failure state gets a screen | Same review pattern across the leading competitors |
| C3 | The courier photo shown must be the courier who shows up | Confirmed breach in BeeOrder specifically |

Full 12, each with its source and a testability note, in [`brain/constraints.md`](brain/constraints.md).

---

## 📁 Repo structure

```
brain/
  INDEX.md            ← entry point
  REGISTER.md          ← 65-decision register + lock log
  intent.md             ← why the product exists
  constraints.md          ← C1–C12
  sequence.md               ← build order
  flows/                     ← the 4 journeys
  decisions/                  ← numbered ADRs
  teardown/                    ← competitor teardowns
  research/                     ← sourced market scans
pitch/
  latakia-file.html            ← pitch deck
.venom/                          ← session memory (resume state, learned patterns)
```

---

<div align="center">

**Proprietary and confidential.** Strategy and market research prepared by **Bosla** — not licensed for
reproduction or use outside its intended engagement. See [`LICENSE`](LICENSE).

</div>
