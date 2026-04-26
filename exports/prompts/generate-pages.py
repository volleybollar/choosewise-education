#!/usr/bin/env python3
"""Generate web landing pages + library-index pages for all prompt packs.

For every pack writes:
  /sv/promptar/<slug_sv>/index.html      — individual SV landing page
  /prompts/<slug_en>/index.html          — individual EN landing page (if translatable)

And rebuilds both library index pages:
  /sv/promptar/index.html
  /prompts/index.html

Inputs:
  exports/prompts/data/<slug>.json       — extracted SV prompts (mandatory)
  exports/prompts/data/<slug_en>-en.json — translated EN prompts (optional — if
                                           missing, the EN landing page and the
                                           "EN" badge on the library card are skipped)

Run:
  python3 exports/prompts/generate-pages.py
"""
import json
import html as _html
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from manifest import PACKS, CATEGORIES
from intros import INTROS_SV, INTROS_EN, SHARED_P2, SHARED_P4

ROOT = Path(__file__).parent.parent.parent
DATA_DIR = Path(__file__).parent / "data"


# ── Category assignment for the landing-page "More prompt sets" section ──
def related_packs(current: dict, lang: str) -> list[dict]:
    """Up to 3 other packs in the same category, in manifest order."""
    same = [p for p in PACKS
            if p["category"] == current["category"]
            and p["folder"] != current["folder"]
            and (lang == "sv" or not p.get("sv_only"))]
    return same[:3]


# ══════════════════════════════════════════════════════════════════════
# INDIVIDUAL LANDING PAGES
# ══════════════════════════════════════════════════════════════════════

LANDING_SV = """<!DOCTYPE html>
<html lang="sv">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — choosewise.education</title>
  <meta name="description" content="{count} färdiga AI-chattpromptar. {subtitle} Fri nedladdningsbar PDF.">
  <meta property="og:title" content="{title} — choosewise.education">
  <meta property="og:description" content="{count} färdiga AI-chattpromptar {audience_lower}.">
  <meta property="og:image" content="/assets/images/brand/og-default.svg">
  <link rel="stylesheet" href="/assets/css/fonts.css">
  <link rel="stylesheet" href="/assets/css/tokens.css">
  <link rel="stylesheet" href="/assets/css/base.css">
  <link rel="stylesheet" href="/assets/css/components.css">
  <link rel="stylesheet" href="/assets/css/pages.css">
</head>
<body>
  <div data-include="/assets/partials/header-sv.html"></div>

  <main>
    <section class="page-hero container">
      <span class="eyebrow" data-reveal>Prompt Library · Vol. {vol}</span>
      <h1 data-reveal>{title}</h1>
      <p class="lede" data-reveal>{count} färdiga AI-chattpromptar {audience_lower} — fria att ladda ner, anpassa och dela.</p>
      <p class="prose" data-reveal>{shared_p2}</p>
      <p class="prose" data-reveal>{unique_p3}</p>
      <p class="prose" data-reveal>{shared_p4}</p>
    </section>

    <section class="section section--alt" data-reveal>
      <div class="container download-section">
        <div>
          <h2>Ladda ner PDF</h2>
          <p>A4 · {count} numrerade promptar med ordlista och promptramverk</p>
        </div>
        <a class="btn btn--primary" href="/assets/pdfs/prompts/{slug_sv}-sv.pdf" download>
          Ladda ner PDF
        </a>
      </div>
    </section>
{parts_summary}
    <section class="section container" data-reveal>
      <h2 class="section__title">Så här använder du dem</h2>
      <p class="prose">Klistra in prompten i en chattbot. Där du ser <em>[hakparenteser]</em>, byt ut texten mot det som passar din situation. Dubbelkolla alltid svaren — och ladda aldrig upp personuppgifter eller känslig information.</p>
      <p class="prose">Promptarna fungerar naturligt tillsammans med <a href="/sv/ratt/">RÄTT-modellen</a>: modellen hjälper dig avgöra <em>om</em> ett AI-verktyg hör hemma i klassrummet; promptarna hjälper dig använda det väl när svaret är ja.</p>
    </section>

{related_section}
  </main>

  <div data-include="/assets/partials/footer-sv.html"></div>

  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" integrity="sha384-g4NTh/Iv5PPU4xPyhEWqPcwtNXOvdaDI8LLnyYfyNZOjKJeYQyjzQ9X5275eBjpt" crossorigin="anonymous"></script>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" integrity="sha384-Z3REaz79l2IaAZqJsSABtTbhjgOUYyV3p90XNnAPCSHg3EMTz1fouunq9WZRtj3d" crossorigin="anonymous"></script>
  <script defer src="/assets/js/include.js"></script>
  <script defer src="/assets/js/scroll-reveals.js"></script>
</body>
</html>
"""

LANDING_EN = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — choosewise.education</title>
  <meta name="description" content="{count} ready-to-use AI chat prompts. {subtitle} Free downloadable PDF.">
  <meta property="og:title" content="{title} — choosewise.education">
  <meta property="og:description" content="{count} ready-to-use AI chat prompts {audience_lower}.">
  <meta property="og:image" content="/assets/images/brand/og-default.svg">
  <link rel="stylesheet" href="/assets/css/fonts.css">
  <link rel="stylesheet" href="/assets/css/tokens.css">
  <link rel="stylesheet" href="/assets/css/base.css">
  <link rel="stylesheet" href="/assets/css/components.css">
  <link rel="stylesheet" href="/assets/css/pages.css">
</head>
<body>
  <div data-include="/assets/partials/header-en.html"></div>

  <main>
    <section class="page-hero container">
      <span class="eyebrow" data-reveal>Prompt Library · Vol. {vol}</span>
      <h1 data-reveal>{title}</h1>
      <p class="lede" data-reveal>{count} ready-to-use AI chat prompts {audience_lower} — free to download, adapt, and share.</p>
      <p class="prose" data-reveal>{shared_p2}</p>
      <p class="prose" data-reveal>{unique_p3}</p>
      <p class="prose" data-reveal>{shared_p4}</p>
    </section>

    <section class="section section--alt" data-reveal>
      <div class="container download-section">
        <div>
          <h2>Download the PDF</h2>
          <p>A4 · {count} numbered prompts with glossary and prompt framework</p>
        </div>
        <a class="btn btn--primary" href="/assets/pdfs/prompts/{slug_en}-en.pdf" download>
          Download PDF
        </a>
      </div>
    </section>
{parts_summary}
    <section class="section container" data-reveal>
      <h2 class="section__title">How to use them</h2>
      <p class="prose">Paste the prompt into a chatbot. Where you see <em>[bracketed text]</em>, replace it with what fits your situation. Always double-check output for accuracy — and never upload personal or sensitive data.</p>
      <p class="prose">All prompts were originally developed in a Swedish school context. This means that some prompts may need to be adapted to the curriculum and context in your country.</p>
      <p class="prose">These prompts pair with the <a href="/wise/">WISE Framework for Education</a>: the framework helps you decide <em>whether</em> to use an AI tool; the prompts help you use it well once you do.</p>
    </section>

{related_section}
  </main>

  <div data-include="/assets/partials/footer-en.html"></div>

  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" integrity="sha384-g4NTh/Iv5PPU4xPyhEWqPcwtNXOvdaDI8LLnyYfyNZOjKJeYQyjzQ9X5275eBjpt" crossorigin="anonymous"></script>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" integrity="sha384-Z3REaz79l2IaAZqJsSABtTbhjgOUYyV3p90XNnAPCSHg3EMTz1fouunq9WZRtj3d" crossorigin="anonymous"></script>
  <script defer src="/assets/js/include.js"></script>
  <script defer src="/assets/js/scroll-reveals.js"></script>
</body>
</html>
"""


def _parts_summary_sv(data: dict) -> str:
    """'Så är det uppbyggt' section — adapts to regular packs vs. megaprompts."""
    if "megaprompts" in data:
        return _megaprompts_summary_sv(data["megaprompts"])
    parts = data.get("parts", [])
    if not parts or (len(parts) == 1 and not parts[0].get("title")):
        return ""
    blocks = []
    for p in parts:
        t = p.get("title") or "Promptar"
        c = len(p["prompts"])
        blocks.append(f'''
        <article class="prompt-part">
          <span class="prompt-part__count">Del {p["number"]} · {c} promptar</span>
          <h3>{_html.escape(t)}</h3>
        </article>''')
    return f'''
    <section class="section container" data-reveal>
      <h2 class="section__title">Så är det uppbyggt</h2>
      <p class="prose">Varje prompt är en mall med hakparenteser <em>[så här]</em> som du byter ut mot din egen kontext.</p>
      <div class="prompt-parts">{"".join(blocks)}
      </div>
    </section>
'''


def _megaprompts_summary_sv(megaprompts: list) -> str:
    blocks = []
    for mp in megaprompts:
        blocks.append(f'''
        <article class="prompt-part">
          <span class="prompt-part__count">Megaprompt #{mp["number"]}</span>
          <h3>{_html.escape(mp["title"])}</h3>
        </article>''')
    return f'''
    <section class="section container" data-reveal>
      <h2 class="section__title">Så är det uppbyggt</h2>
      <p class="prose">Varje megaprompt är en längre, strukturerad prompt uppdelad i sektioner — sammanhang, mål, svarsriktlinjer, informationskrav och output. Tänkt för uppgifter där du vill ha ett mer genomarbetat resultat än vad en kortare prompt ger.</p>
      <div class="prompt-parts">{"".join(blocks)}
      </div>
    </section>
'''


def _parts_summary_en(data: dict) -> str:
    if "megaprompts" in data:
        return _megaprompts_summary_en(data["megaprompts"])
    parts = data.get("parts", [])
    if not parts or (len(parts) == 1 and not parts[0].get("title")):
        return ""
    blocks = []
    for p in parts:
        t = p.get("title_en") or p.get("title") or "Prompts"
        c = len(p["prompts"])
        blocks.append(f'''
        <article class="prompt-part">
          <span class="prompt-part__count">Part {p["number"]} · {c} prompts</span>
          <h3>{_html.escape(t)}</h3>
        </article>''')
    return f'''
    <section class="section container" data-reveal>
      <h2 class="section__title">What's inside</h2>
      <p class="prose">Every prompt is written as a template with bracketed placeholders <em>[like this]</em> for you to swap in your own context.</p>
      <div class="prompt-parts">{"".join(blocks)}
      </div>
    </section>
'''


def _megaprompts_summary_en(megaprompts: list) -> str:
    blocks = []
    for mp in megaprompts:
        title = mp.get("title_en") or mp["title"]
        blocks.append(f'''
        <article class="prompt-part">
          <span class="prompt-part__count">Megaprompt #{mp["number"]}</span>
          <h3>{_html.escape(title)}</h3>
        </article>''')
    return f'''
    <section class="section container" data-reveal>
      <h2 class="section__title">What's inside</h2>
      <p class="prose">Each megaprompt is a longer, structured prompt split into sections — context, goal, response guidelines, information requirements and output. Intended for tasks where you want a more considered result than a short prompt provides.</p>
      <div class="prompt-parts">{"".join(blocks)}
      </div>
    </section>
'''


def _related_sv(current: dict) -> str:
    related = related_packs(current, "sv")
    if not related:
        return ''
    cards = "\n".join(
        f'        <a class="prompt-card" href="/sv/promptar/{p["slug_sv"]}/">\n'
        f'          <span class="prompt-card__eyebrow">{_html.escape(p["eyebrow_sv"])}</span>\n'
        f'          <h3 class="prompt-card__title">{_html.escape(p["title_sv"].rstrip("."))}</h3>\n'
        f'        </a>'
        for p in related
    )
    return f'''
    <section class="section section--alt" data-reveal>
      <div class="container">
        <h2 class="section__title">Relaterade paket</h2>
        <div class="prompt-grid">
{cards}
        </div>
        <a class="btn btn--ghost" href="/sv/promptar/" style="margin-top: var(--space-5);">Alla promptar</a>
      </div>
    </section>
'''


def _related_en(current: dict) -> str:
    related = related_packs(current, "en")
    if not related:
        return ''
    cards = "\n".join(
        f'        <a class="prompt-card" href="/prompts/{p["slug_en"]}/">\n'
        f'          <span class="prompt-card__eyebrow">{_html.escape(p["eyebrow_en"])}</span>\n'
        f'          <h3 class="prompt-card__title">{_html.escape(p["title_en"].rstrip("."))}</h3>\n'
        f'        </a>'
        for p in related
    )
    return f'''
    <section class="section section--alt" data-reveal>
      <div class="container">
        <h2 class="section__title">Related sets</h2>
        <div class="prompt-grid">
{cards}
        </div>
        <a class="btn btn--ghost" href="/prompts/" style="margin-top: var(--space-5);">All prompts</a>
      </div>
    </section>
'''


def _vol(pack: dict) -> str:
    for i, p in enumerate(PACKS):
        if p["folder"] == pack["folder"]:
            return f"{i + 1:02d}"
    return "??"


def generate_landing_sv(pack: dict, data: dict) -> str:
    audience = pack["eyebrow_sv"]
    audience_lower = audience[0].lower() + audience[1:] if audience else ""
    is_mega = pack.get("special") and "megaprompts" in data
    if is_mega:
        n = len(data["megaprompts"])
        template = MEGA_LANDING_SV
        return template.format(
            title=_html.escape(pack["title_sv"].rstrip(".")),
            count=n,
            slug_sv=pack["slug_sv"],
            vol=_vol(pack),
            parts_summary=_parts_summary_sv(data),
            related_section=_related_sv(pack),
        )
    unique_p3 = INTROS_SV.get(pack["slug_sv"], "")
    if not unique_p3:
        print(f"  WARN: no SV intro for {pack['slug_sv']}")
    return LANDING_SV.format(
        title=_html.escape(pack["title_sv"].rstrip(".")),
        subtitle=_html.escape(pack.get("subtitle_sv") or "Färdiga promptar att utgå från i planering, undervisning och reflektion."),
        audience_lower=_html.escape(audience_lower),
        count=data["total_prompts"],
        slug_sv=pack["slug_sv"],
        vol=_vol(pack),
        parts_summary=_parts_summary_sv(data),
        related_section=_related_sv(pack),
        shared_p2=SHARED_P2["sv"],
        unique_p3=unique_p3,
        shared_p4=SHARED_P4["sv"],
    )


def generate_landing_en(pack: dict, data: dict) -> str:
    audience = pack["eyebrow_en"]
    audience_lower = audience[0].lower() + audience[1:] if audience else ""
    is_mega = pack.get("special") and "megaprompts" in data
    if is_mega:
        n = len(data["megaprompts"])
        return MEGA_LANDING_EN.format(
            title=_html.escape(pack["title_en"].rstrip(".")),
            count=n,
            slug_en=pack["slug_en"],
            vol=_vol(pack),
            parts_summary=_parts_summary_en(data),
            related_section=_related_en(pack),
        )
    unique_p3 = INTROS_EN.get(pack["slug_en"], "")
    if not unique_p3:
        print(f"  WARN: no EN intro for {pack['slug_en']}")
    return LANDING_EN.format(
        title=_html.escape(pack["title_en"].rstrip(".")),
        subtitle=_html.escape(pack.get("subtitle_en") or "Ready-to-use prompts for planning, teaching and reflection."),
        audience_lower=_html.escape(audience_lower),
        count=data["total_prompts"],
        slug_en=pack["slug_en"],
        vol=_vol(pack),
        parts_summary=_parts_summary_en(data),
        related_section=_related_en(pack),
        shared_p2=SHARED_P2["en"],
        unique_p3=unique_p3,
        shared_p4=SHARED_P4["en"],
    )


# Megapromptar-specific landing page template — different framing on the lede
# (deep-dive, for when basic prompts feel too simple) and download copy.
MEGA_LANDING_SV = """<!DOCTYPE html>
<html lang="sv">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — choosewise.education</title>
  <meta name="description" content="{count} megapromptar — längre, strukturerade promptar för fördjupning. Fri nedladdningsbar PDF.">
  <meta property="og:title" content="{title} — choosewise.education">
  <meta property="og:description" content="{count} megapromptar — fördjupning för den som tycker att de vanliga promptarna är för enkla.">
  <meta property="og:image" content="/assets/images/brand/og-default.svg">
  <link rel="stylesheet" href="/assets/css/fonts.css">
  <link rel="stylesheet" href="/assets/css/tokens.css">
  <link rel="stylesheet" href="/assets/css/base.css">
  <link rel="stylesheet" href="/assets/css/components.css">
  <link rel="stylesheet" href="/assets/css/pages.css">
</head>
<body>
  <div data-include="/assets/partials/header-sv.html"></div>

  <main>
    <section class="page-hero container">
      <span class="eyebrow" data-reveal>Prompt Library · Vol. {vol} · Fördjupning</span>
      <h1 data-reveal>{title}</h1>
      <p class="lede" data-reveal>{count} megapromptar — längre, strukturerade promptar för när de vanliga känns för enkla. Varje megaprompt är uppdelad i sektioner (sammanhang, mål, svarsriktlinjer) och fungerar som en färdig mall du kan kopiera, fylla i och iterera med.</p>
    </section>

    <section class="section section--alt" data-reveal>
      <div class="container download-section">
        <div>
          <h2>Ladda ner PDF</h2>
          <p>A4 · {count} strukturerade megapromptar med ordlista och promptramverk</p>
        </div>
        <a class="btn btn--primary" href="/assets/pdfs/prompts/{slug_sv}-sv.pdf" download>
          Ladda ner PDF
        </a>
      </div>
    </section>
{parts_summary}
    <section class="section container" data-reveal>
      <h2 class="section__title">Så här använder du dem</h2>
      <p class="prose">Kopiera hela megaprompten, klistra in i chattbotten, byt ut <em>[HAKPARENTESER]</em> mot din kontext (målgrupp, ämne, nyckelbegrepp osv), och iterera sedan som vanligt tills du är nöjd. Megapromptar ger långa svar — dubbelkolla detaljerna.</p>
      <p class="prose">Vill du komma igång enklare, börja med <a href="/sv/promptar/">promptpaketen för din roll</a> först. Megapromptarna är tänkta som ett steg djupare.</p>
    </section>

{related_section}
  </main>

  <div data-include="/assets/partials/footer-sv.html"></div>

  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" integrity="sha384-g4NTh/Iv5PPU4xPyhEWqPcwtNXOvdaDI8LLnyYfyNZOjKJeYQyjzQ9X5275eBjpt" crossorigin="anonymous"></script>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" integrity="sha384-Z3REaz79l2IaAZqJsSABtTbhjgOUYyV3p90XNnAPCSHg3EMTz1fouunq9WZRtj3d" crossorigin="anonymous"></script>
  <script defer src="/assets/js/include.js"></script>
  <script defer src="/assets/js/scroll-reveals.js"></script>
</body>
</html>
"""

MEGA_LANDING_EN = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — choosewise.education</title>
  <meta name="description" content="{count} megaprompts — longer, structured prompts for deep-dive use. Free downloadable PDF.">
  <meta property="og:title" content="{title} — choosewise.education">
  <meta property="og:description" content="{count} megaprompts — a deep dive for when the basic prompts feel too simple.">
  <meta property="og:image" content="/assets/images/brand/og-default.svg">
  <link rel="stylesheet" href="/assets/css/fonts.css">
  <link rel="stylesheet" href="/assets/css/tokens.css">
  <link rel="stylesheet" href="/assets/css/base.css">
  <link rel="stylesheet" href="/assets/css/components.css">
  <link rel="stylesheet" href="/assets/css/pages.css">
</head>
<body>
  <div data-include="/assets/partials/header-en.html"></div>

  <main>
    <section class="page-hero container">
      <span class="eyebrow" data-reveal>Prompt Library · Vol. {vol} · Deep Dive</span>
      <h1 data-reveal>{title}</h1>
      <p class="lede" data-reveal>{count} megaprompts — longer, structured prompts for when the basic ones feel too simple. Each megaprompt is split into labelled sections (context, goal, response guidelines) and works as a ready-to-use template you can copy, fill in, and iterate on.</p>
    </section>

    <section class="section section--alt" data-reveal>
      <div class="container download-section">
        <div>
          <h2>Download the PDF</h2>
          <p>A4 · {count} structured megaprompts with glossary and prompt framework</p>
        </div>
        <a class="btn btn--primary" href="/assets/pdfs/prompts/{slug_en}-en.pdf" download>
          Download PDF
        </a>
      </div>
    </section>
{parts_summary}
    <section class="section container" data-reveal>
      <h2 class="section__title">How to use them</h2>
      <p class="prose">Copy the whole megaprompt, paste it into the chatbot, replace the <em>[BRACKETS]</em> with your own context (audience, subject, key concepts, etc.), and iterate as usual until you're happy. Megaprompts produce long responses — double-check the details.</p>
      <p class="prose">All prompts were originally developed in a Swedish school context. This means that some prompts may need to be adapted to the curriculum and context in your country.</p>
      <p class="prose">If you'd rather ease in, start with a <a href="/prompts/">role-specific prompt set</a> first. The megaprompts are designed as a step deeper.</p>
    </section>

{related_section}
  </main>

  <div data-include="/assets/partials/footer-en.html"></div>

  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" integrity="sha384-g4NTh/Iv5PPU4xPyhEWqPcwtNXOvdaDI8LLnyYfyNZOjKJeYQyjzQ9X5275eBjpt" crossorigin="anonymous"></script>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" integrity="sha384-Z3REaz79l2IaAZqJsSABtTbhjgOUYyV3p90XNnAPCSHg3EMTz1fouunq9WZRtj3d" crossorigin="anonymous"></script>
  <script defer src="/assets/js/include.js"></script>
  <script defer src="/assets/js/scroll-reveals.js"></script>
</body>
</html>
"""


# ══════════════════════════════════════════════════════════════════════
# LIBRARY INDEX
# ══════════════════════════════════════════════════════════════════════

LIBRARY_INDEX_SV = """<!DOCTYPE html>
<html lang="sv">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Promptbibliotek — choosewise.education</title>
  <meta name="description" content="Ett fritt bibliotek av AI-chattpromptar för alla yrkesroller i skolan — lärare, rektorer, ämneslärare, stödpersonal. Nedladdningsbara PDF:er.">
  <meta property="og:title" content="Promptbibliotek — choosewise.education">
  <meta property="og:description" content="Ett fritt bibliotek av AI-chattpromptar för alla yrkesroller i skolan.">
  <meta property="og:image" content="/assets/images/brand/og/prompts-sv.svg">
  <link rel="stylesheet" href="/assets/css/fonts.css">
  <link rel="stylesheet" href="/assets/css/tokens.css">
  <link rel="stylesheet" href="/assets/css/base.css">
  <link rel="stylesheet" href="/assets/css/components.css">
  <link rel="stylesheet" href="/assets/css/pages.css">
</head>
<body>
  <div data-include="/assets/partials/header-sv.html"></div>

  <main>
    <section class="page-hero container">
      <span class="eyebrow" data-reveal>Promptbibliotek</span>
      <h1 data-reveal>Promptar för alla som jobbar i skolan.</h1>
      <p class="lede" data-reveal>{total_packs} promptpaket för lärare, ämneslärare, skolledare och stödpersonal — {total_prompts} promptar totalt, grundade i pedagogik. Varje paket är en nedladdningsbar PDF.</p>
    </section>

    <!-- Svarsblock för "vilket promptpaket ska jag ladda ner?" -->
    <section class="seo-answer" data-reveal>
      <h2 class="seo-answer__question">Vilket promptpaket ska jag ladda ner?</h2>
      <p class="seo-answer__capsule">Fria promptpaket som täcker {total_packs} roller och ämnen i skolan — klasslärare, ämneslärare från biologi till hem- och konsumentkunskap, både grundskola och gymnasium, skolledare (rektorer, skolchefer, central administration) och stödpersonal (kuratorer, bibliotekarier, IT, specialpedagogik). Varje paket är en nedladdningsbar PDF, framtagen i svensk skolkontext men möjlig att anpassa till andra läroplaner. Välj det paket som ligger närmast din roll; ämneslärare kan också börja i det ämnesövergripande paketet.</p>
    </section>

    <section class="section container" data-reveal>
      <div class="prompt-filters" role="group" aria-label="Filtrera promptpaket">
        <span class="prompt-filters__group-label">Filtrera</span>
        <button type="button" class="prompt-filter is-active" data-filter="all">Alla</button>
{filter_buttons_sv}
      </div>

      <div class="prompt-grid">
{cards}
      </div>
    </section>

    <section class="section section--alt" data-reveal>
      <div class="container">
        <h2 class="section__title">Om biblioteket</h2>
        <p class="prose">Varje promptpaket är fritt att ladda ner, använda, anpassa och dela. Designen är avsiktligt konsekvent mellan alla volymer — samma omslag, samma typografi, samma struktur — så biblioteket känns som en sammanhållen samling istället för spridda handouts.</p>
        <p class="prose">Promptarna fungerar naturligt tillsammans med <a href="/sv/ratt/">RÄTT-modellen</a>: modellen hjälper dig avgöra <em>om</em> ett AI-verktyg hör hemma i klassrummet; promptarna hjälper dig använda det väl när svaret är ja.</p>
      </div>
    </section>
  </main>

  <div data-include="/assets/partials/footer-sv.html"></div>

  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" integrity="sha384-g4NTh/Iv5PPU4xPyhEWqPcwtNXOvdaDI8LLnyYfyNZOjKJeYQyjzQ9X5275eBjpt" crossorigin="anonymous"></script>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" integrity="sha384-Z3REaz79l2IaAZqJsSABtTbhjgOUYyV3p90XNnAPCSHg3EMTz1fouunq9WZRtj3d" crossorigin="anonymous"></script>
  <script defer src="/assets/js/include.js"></script>
  <script defer src="/assets/js/scroll-reveals.js"></script>

  <script>
    document.querySelectorAll('.prompt-filter').forEach(btn => {{
      btn.addEventListener('click', () => {{
        const filter = btn.dataset.filter;
        document.querySelectorAll('.prompt-filter').forEach(b => b.classList.toggle('is-active', b === btn));
        document.querySelectorAll('.prompt-card').forEach(card => {{
          const cat = card.dataset.category;
          card.style.display = (filter === 'all' || cat === filter) ? '' : 'none';
        }});
      }});
    }});
  </script>
</body>
</html>
"""

LIBRARY_INDEX_EN = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Prompt Library — choosewise.education</title>
  <meta name="description" content="A free library of AI chat prompts for every role in the school — teachers, principals, subject specialists, support staff. Downloadable PDFs.">
  <meta property="og:title" content="Prompt Library — choosewise.education">
  <meta property="og:description" content="A free library of AI chat prompts for every role in the school.">
  <meta property="og:image" content="/assets/images/brand/og/prompts-en.svg">
  <link rel="stylesheet" href="/assets/css/fonts.css">
  <link rel="stylesheet" href="/assets/css/tokens.css">
  <link rel="stylesheet" href="/assets/css/base.css">
  <link rel="stylesheet" href="/assets/css/components.css">
  <link rel="stylesheet" href="/assets/css/pages.css">
</head>
<body>
  <div data-include="/assets/partials/header-en.html"></div>

  <main>
    <section class="page-hero container">
      <span class="eyebrow" data-reveal>Prompt Library</span>
      <h1 data-reveal>Prompts about teaching, learning and education.</h1>
      <p class="lede" data-reveal>{total_packs} prompt sets for teachers, subject specialists, school leaders and support staff — {total_prompts} prompts in total, grounded in pedagogy. Every set is a downloadable PDF.</p>
    </section>

    <!-- Answer capsule for "which prompt pack should I download?" -->
    <section class="seo-answer" data-reveal>
      <h2 class="seo-answer__question">Which prompt pack should I download?</h2>
      <p class="seo-answer__capsule">Free prompt packs covering {total_packs} roles and subjects in education — classroom teachers, subject specialists from biology to home economics across compulsory and upper-secondary, school leaders (principals, superintendents, district administrators), and support staff (counselors, librarians, IT, special education). Every pack is a downloadable PDF, originally written in a Swedish school context but adaptable to other curricula. Pick the pack closest to your role; subject teachers can also start from the cross-curricular pack.</p>
    </section>

    <section class="section container" data-reveal>
      <div class="prompt-filters" role="group" aria-label="Filter prompt sets">
        <span class="prompt-filters__group-label">Filter</span>
        <button type="button" class="prompt-filter is-active" data-filter="all">All</button>
{filter_buttons_en}
      </div>

      <div class="prompt-grid">
{cards}
      </div>
    </section>

    <section class="section section--alt" data-reveal>
      <div class="container">
        <h2 class="section__title">About the library</h2>
        <p class="prose">Every prompt set is free to download, use, adapt, and share. The design is intentionally consistent across all volumes — same cover, same typography, same structure — so the library feels like one collection rather than scattered handouts.</p>
        <p class="prose">All prompts were originally developed in a Swedish school context. This means that some prompts may need to be adapted to the curriculum and context in your country.</p>
        <p class="prose">These prompts pair with the <a href="/wise/">WISE Framework for Education</a>: the framework helps you decide <em>whether</em> a given AI tool belongs in the classroom; the prompts help you use it well once the answer is yes.</p>
      </div>
    </section>
  </main>

  <div data-include="/assets/partials/footer-en.html"></div>

  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" integrity="sha384-g4NTh/Iv5PPU4xPyhEWqPcwtNXOvdaDI8LLnyYfyNZOjKJeYQyjzQ9X5275eBjpt" crossorigin="anonymous"></script>
  <script defer src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" integrity="sha384-Z3REaz79l2IaAZqJsSABtTbhjgOUYyV3p90XNnAPCSHg3EMTz1fouunq9WZRtj3d" crossorigin="anonymous"></script>
  <script defer src="/assets/js/include.js"></script>
  <script defer src="/assets/js/scroll-reveals.js"></script>

  <script>
    document.querySelectorAll('.prompt-filter').forEach(btn => {{
      btn.addEventListener('click', () => {{
        const filter = btn.dataset.filter;
        document.querySelectorAll('.prompt-filter').forEach(b => b.classList.toggle('is-active', b === btn));
        document.querySelectorAll('.prompt-card').forEach(card => {{
          const cat = card.dataset.category;
          card.style.display = (filter === 'all' || cat === filter) ? '' : 'none';
        }});
      }});
    }});
  </script>
</body>
</html>
"""

# Swedish category labels for the filter buttons
CATEGORY_SV = {
    "teachers": "Lärare",
    "subject":  "Ämneslärare",
    "leaders":  "Skolledare",
    "support":  "Stödpersonal",
    "themes":   "Tematiskt",
}


def _filter_buttons(lang: str) -> str:
    labels = CATEGORY_SV if lang == "sv" else CATEGORIES
    buttons = [
        f'        <button type="button" class="prompt-filter" data-filter="{k}">{_html.escape(v)}</button>'
        for k, v in labels.items()
    ]
    return "\n".join(buttons)


def _library_cards_sv(pack_counts: dict) -> str:
    cards = []
    for pack in PACKS:
        slug_sv = pack.get("slug_sv")
        if not slug_sv:
            continue
        count = pack_counts.get(slug_sv, 0)
        unit = "megapromptar" if pack.get("special") else "promptar"
        has_en = pack.get("slug_en") and not pack.get("sv_only")
        langs = '<span>SV</span>' + (f' <span>EN</span>' if has_en else '')
        cards.append(f'''        <a class="prompt-card" href="/sv/promptar/{slug_sv}/" data-category="{pack["category"]}">
          <span class="prompt-card__eyebrow">{_html.escape(pack["eyebrow_sv"])}</span>
          <h2 class="prompt-card__title">{_html.escape(pack["title_sv"].rstrip("."))}</h2>
          <p class="prompt-card__count">{count} {unit}</p>
          <div class="prompt-card__langs">{langs}</div>
        </a>''')
    return "\n".join(cards)


def _library_cards_en(pack_counts: dict, has_en_data: set) -> str:
    cards = []
    for pack in PACKS:
        slug_en = pack.get("slug_en")
        if not slug_en or pack.get("sv_only"):
            continue
        count = pack_counts.get(pack["slug_sv"], 0)
        unit = "megaprompts" if pack.get("special") else "prompts"
        available = slug_en in has_en_data
        # Before translation: every card still appears but with a "Coming soon" state
        if available:
            open_tag = f'<a class="prompt-card" href="/prompts/{slug_en}/" data-category="{pack["category"]}">'
            close_tag = '</a>'
            lang_line = '<span>EN</span><span>SV</span>'
        else:
            open_tag = (
                f'<div class="prompt-card" data-category="{pack["category"]}" '
                f'style="opacity: 0.55; cursor: default; background: var(--color-bg-alt); border-style: dashed;">'
            )
            close_tag = '</div>'
            lang_line = '<span>Coming soon</span>'
        cards.append(
            f'        {open_tag}\n'
            f'          <span class="prompt-card__eyebrow">{_html.escape(pack["eyebrow_en"])}</span>\n'
            f'          <h2 class="prompt-card__title">{_html.escape(pack["title_en"].rstrip("."))}</h2>\n'
            f'          <p class="prompt-card__count">{count} {unit}</p>\n'
            f'          <div class="prompt-card__langs">{lang_line}</div>\n'
            f'        {close_tag}'
        )
    return "\n".join(cards)


def main():
    pack_counts = {}
    has_en_data = set()

    # Build per-pack landing pages + collect stats
    for pack in PACKS:
        slug_sv = pack.get("slug_sv")
        slug_en = pack.get("slug_en")

        # Swedish landing — always, if data exists
        if slug_sv:
            data_path = DATA_DIR / f"{slug_sv}.json"
            if data_path.exists():
                data = json.load(open(data_path))
                pack_counts[slug_sv] = data["total_prompts"]
                out = ROOT / "sv" / "promptar" / slug_sv / "index.html"
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(generate_landing_sv(pack, data), encoding="utf-8")

        # English landing — only if EN data exists
        if slug_en and not pack.get("sv_only"):
            en_data_path = DATA_DIR / f"{slug_en}-en.json"
            if en_data_path.exists():
                data = json.load(open(en_data_path))
                has_en_data.add(slug_en)
                out = ROOT / "prompts" / slug_en / "index.html"
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(generate_landing_en(pack, data), encoding="utf-8")

    total_packs = len(pack_counts)
    total_prompts = sum(pack_counts.values())

    # Library indexes
    sv_idx = LIBRARY_INDEX_SV.format(
        total_packs=total_packs,
        total_prompts=total_prompts,
        filter_buttons_sv=_filter_buttons("sv"),
        cards=_library_cards_sv(pack_counts),
    )
    (ROOT / "sv" / "promptar" / "index.html").write_text(sv_idx, encoding="utf-8")

    en_idx = LIBRARY_INDEX_EN.format(
        total_packs=total_packs,
        total_prompts=total_prompts,
        filter_buttons_en=_filter_buttons("en"),
        cards=_library_cards_en(pack_counts, has_en_data),
    )
    (ROOT / "prompts" / "index.html").write_text(en_idx, encoding="utf-8")

    print(f"Generated:")
    print(f"  · {total_packs} SV landing pages  (total {total_prompts} prompts)")
    print(f"  · {len(has_en_data)} EN landing pages")
    print(f"  · /sv/promptar/index.html")
    print(f"  · /prompts/index.html")

    # Breakdown by category
    by_cat = defaultdict(int)
    for p in PACKS:
        if p.get("slug_sv") in pack_counts:
            by_cat[p["category"]] += 1
    print("\nBy category:")
    for cat, label in CATEGORIES.items():
        print(f"  {label:<20s} {by_cat[cat]:>3} packs")


if __name__ == "__main__":
    main()
