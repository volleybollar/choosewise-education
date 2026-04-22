#!/usr/bin/env python3
"""Generate choosewise.education prompt HTML pages from JSON pack data.

Builds both Swedish (always) and English (if {slug}-en.json exists and the
pack is not SV-only) HTML files for every pack in the manifest.

The templates below mirror the pilot at 01-larare-sv.html / 01-teachers-en.html
one-to-one. The shared boilerplate (glossary, framework, chatbots, usage
callout, back cover) lives inline here so it's a single source of truth.

Output: exports/prompts/{slug}-sv.html, {slug}-en.html
The downstream build-prompts-pdf.py script then renders these to A4 PDFs.

Run:
  python3 exports/prompts/generate-html.py            # all packs, both languages
  python3 exports/prompts/generate-html.py larare     # single pack, both languages
  python3 exports/prompts/generate-html.py larare sv  # single pack, one language
"""
import json
import html as _html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from manifest import PACKS

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"


# ══════════════════════════════════════════════════════════════════════
# SHARED BOILERPLATE — identical across every pack in the same language
# ══════════════════════════════════════════════════════════════════════

BOILERPLATE_SV = """
<section class="section-opener">
  <div class="section-opener__eyebrow">Del 0 · Att komma igång</div>
  <h2>Ordlista</h2>
  <p>Några begrepp som återkommer i den här guiden. Känner du redan till dem, hoppa vidare till ramverket på nästa sida.</p>
</section>

<dl class="glossary">
  <dt>AI — Artificiell Intelligens</dt>
  <dd>Ett sätt att försöka få maskiner att efterlikna hjärnans funktioner, det vill säga att kunna "tänka" och lära ungefär så som människor gör. Vi förstår inte hur hjärnan fungerar, men de delar vi förstår kan vi försöka härma.</dd>
  <dt>Prompt</dt>
  <dd>En instruktion till chattbotten för att få ett önskat svar eller en önskad uppgift utförd. Vissa chattbottar går att prata med, men än så länge är det många som skriver textkommandon till dem.</dd>
  <dt>Iterera</dt>
  <dd>När du fått ett svar från en chattbot justerar och förtydligar du vilka delar av svaret som du inte är nöjd med — du förfinar svaret så det blir bättre och bättre tills du är nöjd. Ju bättre prompt du har från början, desto färre iterationer behövs.</dd>
  <dt>Chattbot</dt>
  <dd>En chattbot har tränats på att hitta mönster i de texter som den tränats på. Dessa mönster använder den för att skapa text som svar på din prompt. Texten du får som svar genereras i realtid.</dd>
  <dt>GPT</dt>
  <dd>Själva modellen (Generative Pre-trained Transformer) som en chattbot använder sig av. Samma GPT kan användas av olika chattbottar — till exempel använder både Copilot och ChatGPT OpenAIs GPT.</dd>
  <dt>Generativ AI</dt>
  <dd>AI som skapar (genererar) text, bilder, video eller ljud i realtid när den tillfrågas om att göra det.</dd>
  <dt>Bias</dt>
  <dd>Svar som AI ger är snedvridna eller partiska, vilket beror på den data som AI tränats på och vilka bias som finns i den datan. För en chattbot är det svårt att synliggöra dessa bias, men för en AI som genererar bilder är det lättare.</dd>
  <dt>Hallucination</dt>
  <dd>Texten du får som svar av en chattbot baseras på mönster i data som den tränats på, men det finns även en slumpmässighet i vilka ord som genereras — det innebär att ord kan skapa en innebörd som inte är sann.</dd>
</dl>

<div class="framework-box">
  <h3>Ett ramverk för att skriva egna promptar</h3>
  <dl>
    <dt>Roll:</dt><dd>Agera som en erfaren lärare i fysik.</dd>
    <dt>Uppgift:</dt><dd>Skapa en lektionsplanering som introducerar elever i år 8 till området optik.</dd>
    <dt>Kontext:</dt><dd>Jag jobbar på en högstadieskola i Sverige, har 25 elever i klassen och lektionen är 60 minuter lång.</dd>
    <dt>Format:</dt><dd>Koppla ihop innehåll och aktiviteter med läroplanen i fysik och ge mig en planering som i detalj beskriver lektionens olika delar och material som behövs.</dd>
    <dt>Ton:</dt><dd>Använd en formell men vänlig ton.</dd>
  </dl>
</div>

<h3 style="margin-top: 10mm; margin-bottom: 3mm;">Exempel på chattbottar</h3>
<p style="font-size: 9.5pt; color: var(--color-text-soft); margin-bottom: 4mm;">AI kan även skapa bilder och göra annat, men här fokuserar vi på chattfunktionerna.</p>

<ul class="chatbot-list">
  <li><strong>ChatGPT</strong> — Open AIs chattbot</li>
  <li><strong>Gemini</strong> — Googles chattbot</li>
  <li><strong>NotebookLM</strong> — Googles verktyg som bland annat kan skapa podd med två röster</li>
  <li><strong>Copilot</strong> — Microsofts chattbot</li>
  <li><strong>Claude</strong> — En chattbot från Anthropic</li>
  <li><strong>Perplexity</strong> — Från San Francisco, använde tidigt länkar till källor</li>
  <li><strong>Duck AI</strong> — DuckDuckGo's chattbot, olika GPT:er att välja</li>
  <li><strong>Mistral AI</strong> — En chattbot från Frankrike</li>
</ul>
<p style="font-size: 9pt; color: var(--color-text-soft); margin-top: 3mm;">De flesta chattbottar har åldersgränser.</p>

<section class="section-opener" style="page-break-before: always;">
  <div class="section-opener__eyebrow">Innan du börjar</div>
  <h2>Hur du använder promptarna</h2>
  <p>Alla promptar är framtagna som exempel för att komma igång. Ändra dem gärna så att de passar ditt sammanhang.</p>
</section>

<p>När du använt en chattbot ett tag lär du dig vilken typ av promptar som fungerar bättre respektive sämre. Testa samma prompt två gånger — först som den står, sedan med tillägget "Agera som en erfaren expertlärare i [ämne]" — för att se om svaret förbättras. Får du bra svar är prompten bra. Får du inte bra svar behöver du ändra prompten eller ge mer kontext. Vissa chattbottar är bättre än andra på vissa typer av svar, så om du inte är nöjd med svaren du får trots olika justeringar — testa en annan chattbot.</p>

<div class="callout callout--warning">
  <h3>Hakparenteser och integritet</h3>
  <p style="margin-bottom: 2mm;">Du skriver in texten från prompten i chattbottens promptfönster. När det finns hakparenteser <span class="bracket">[så här]</span> byter du ut texten mot det som passar för ditt sammanhang.</p>
  <p style="margin-bottom: 2mm;"><strong>Dubbelkolla alltid svaren</strong> — det är inte säkert att det chattbotten skriver är sant.</p>
  <p style="margin: 0;"><strong>OBS!</strong> Tänk efter om du laddar upp texter eller dokument. Ladda inte upp personuppgifter eller känslig information. Tänk på GDPR.</p>
</div>
"""

BOILERPLATE_EN = """
<section class="section-opener">
  <div class="section-opener__eyebrow">Part 0 · Getting Started</div>
  <h2>Glossary</h2>
  <p>A few terms that recur throughout this guide. If you already know them, skip ahead to the framework on the next page.</p>
</section>

<dl class="glossary">
  <dt>AI — Artificial Intelligence</dt>
  <dd>An attempt to make machines mimic brain functions — to "think" and learn roughly the way humans do. We don't fully understand how the brain works, but we can try to replicate the parts we do understand.</dd>
  <dt>Prompt</dt>
  <dd>An instruction given to a chatbot to get a desired response or task performed. Some chatbots can be spoken to, but most are still driven by written text commands.</dd>
  <dt>Iterate</dt>
  <dd>After receiving a response from a chatbot, you refine and clarify the parts you're not satisfied with — sharpening the answer until it's what you want. The better your starting prompt, the fewer iterations you'll need.</dd>
  <dt>Chatbot</dt>
  <dd>A chatbot has been trained to find patterns in large amounts of text. It uses those patterns to generate a response to your prompt. The answer is produced in real time.</dd>
  <dt>GPT</dt>
  <dd>The underlying model (Generative Pre-trained Transformer) that a chatbot uses. The same GPT can power different chatbots — for example, Copilot and ChatGPT have both used OpenAI's GPT.</dd>
  <dt>Generative AI</dt>
  <dd>AI that creates (generates) text, images, video, or sound in real time when prompted to do so.</dd>
  <dt>Bias</dt>
  <dd>AI responses can be skewed or partial, depending on the data the AI was trained on and the biases present in that data. These biases are harder to spot in chatbots than in image-generating AI.</dd>
  <dt>Hallucination</dt>
  <dd>The text you receive from a chatbot is based on patterns in its training data, but word generation also involves randomness — meaning generated words can sometimes create a meaning that simply isn't true.</dd>
</dl>

<div class="framework-box">
  <h3>A framework for writing your own prompts</h3>
  <dl>
    <dt>Role:</dt><dd>Act as an experienced physics teacher.</dd>
    <dt>Task:</dt><dd>Create a lesson plan that introduces year 8 students to optics.</dd>
    <dt>Context:</dt><dd>I teach at a middle school, have 25 students in my class, and the lesson is 60 minutes long.</dd>
    <dt>Format:</dt><dd>Link content and activities to the physics curriculum and give me a plan that describes each part of the lesson and the materials required.</dd>
    <dt>Tone:</dt><dd>Use a formal but friendly tone.</dd>
  </dl>
</div>

<h3 style="margin-top: 10mm; margin-bottom: 3mm;">A few chatbots to know</h3>
<p style="font-size: 9.5pt; color: var(--color-text-soft); margin-bottom: 4mm;">AI can also generate images and more, but we focus here on chat capabilities.</p>

<ul class="chatbot-list">
  <li><strong>ChatGPT</strong> — OpenAI's chatbot</li>
  <li><strong>Gemini</strong> — Google's chatbot</li>
  <li><strong>NotebookLM</strong> — Google's tool that can, among other things, generate a two-voice podcast</li>
  <li><strong>Copilot</strong> — Microsoft's chatbot</li>
  <li><strong>Claude</strong> — Anthropic's chatbot</li>
  <li><strong>Perplexity</strong> — From San Francisco, was early to include source links</li>
  <li><strong>Duck AI</strong> — DuckDuckGo's chatbot, lets you pick among several GPTs</li>
  <li><strong>Mistral AI</strong> — A chatbot from France</li>
</ul>
<p style="font-size: 9pt; color: var(--color-text-soft); margin-top: 3mm;">Most chatbots have age restrictions.</p>

<section class="section-opener" style="page-break-before: always;">
  <div class="section-opener__eyebrow">Before you start</div>
  <h2>How to use the prompts</h2>
  <p>All the prompts are starting points — examples to get you going. Adapt them to fit your context.</p>
</section>

<p>After using a chatbot for a while, you'll learn what kinds of prompts work better or worse. Try the same prompt twice — first as-is, then with the prefix "Act as an experienced expert teacher in [subject]" — and see whether the quality of the response improves. A good response means a good prompt. A poor response means the prompt needs more context or adjustment. Some chatbots are better than others at certain tasks, so if you're not satisfied despite multiple tries, consider switching chatbot.</p>

<div class="callout callout--warning">
  <h3>Brackets and privacy</h3>
  <p style="margin-bottom: 2mm;">You paste the prompt text into the chatbot's input field. Wherever brackets <span class="bracket">[like this]</span> appear, replace the text inside with whatever fits your context.</p>
  <p style="margin-bottom: 2mm;"><strong>Always double-check the responses</strong> — chatbot output is not guaranteed to be accurate.</p>
  <p style="margin: 0;"><strong>Note:</strong> Think carefully before uploading texts or documents. Never upload personal data or sensitive information. Mind GDPR.</p>
</div>
"""


BACK_COVER_SV = """
<section class="page--back">
  <div>
    <div class="back__eyebrow">Fortsätt på webben</div>
    <h1>Rätt verktyg<br>vid rätt tillfälle.</h1>
    <p>Den här samlingen är en del av ett bibliotek med AI-promptar för alla yrkesroller i skolan — fritt att använda, anpassa och dela vidare.</p>
  </div>

  <ul class="back__cta-list">
    <li>
      <strong>Fler promptpaket</strong>
      Hitta promptar för rektorer, ämneslärare, skolledare, stödpersonal med flera på <a href="https://choosewise.education/sv/promptar/">choosewise.education/sv/promptar</a>
    </li>
    <li>
      <strong>RÄTT-modellen</strong>
      Fyra frågor som gör beslutet om AI-verktyg i klassrummet strukturerat — <a href="https://choosewise.education/sv/ratt/">choosewise.education/sv/ratt</a>
    </li>
    <li>
      <strong>Följ Johan Lindström på LinkedIn</strong>
      För nya promptar, guider och reflektioner om AI i skolan — sök på <em>Johan Lindström</em>
    </li>
  </ul>

  <div class="back__bottom">
    <span>choosewise.education · Prompt Library</span>
    <span class="back__brand">The right tool at the right time.</span>
  </div>
</section>
"""

BACK_COVER_EN = """
<section class="page--back">
  <div>
    <div class="back__eyebrow">Continue on the web</div>
    <h1>The right tool<br>at the right time.</h1>
    <p>This collection is part of a library of AI prompts for every role in the school — free to use, adapt, and share.</p>
  </div>

  <ul class="back__cta-list">
    <li>
      <strong>More prompt sets</strong>
      Find prompts for principals, subject teachers, school leaders, support staff and more at <a href="https://choosewise.education/prompts/">choosewise.education/prompts</a>
    </li>
    <li>
      <strong>The WISE framework</strong>
      Four questions that turn any "should we use this AI tool?" conversation into a structured decision — <a href="https://choosewise.education/wise/">choosewise.education/wise</a>
    </li>
    <li>
      <strong>Follow Johan Lindström on LinkedIn</strong>
      For new prompts, guides and reflections on AI in education — search for <em>Johan Lindström</em>
    </li>
  </ul>

  <div class="back__bottom">
    <span>choosewise.education · Prompt Library</span>
    <span class="back__brand">The right tool at the right time.</span>
  </div>
</section>
"""

SCRIPT_SNIPPET = """
<script>
  document.querySelectorAll('.prompts > li, .callout p, .framework-box dd').forEach(el => {
    el.innerHTML = el.innerHTML.replace(/\\[([^\\]]+)\\]/g, '<span class="bracket">[$1]</span>');
  });
</script>
"""

# ══════════════════════════════════════════════════════════════════════
# PAGE ASSEMBLY
# ══════════════════════════════════════════════════════════════════════

def _volume_number(pack: dict) -> str:
    """Sequential volume number based on pack's position in PACKS."""
    for i, p in enumerate(PACKS):
        if p["folder"] == pack["folder"]:
            return f"{i + 1:02d}"
    return "??"


def cover_sv(pack: dict, total_prompts: int) -> str:
    subtitle = pack.get("subtitle_sv") or "Färdiga promptar att utgå från i planering, undervisning och reflektion."
    count_label = f"{total_prompts} chattpromptar" if total_prompts else "Chattpromptar"
    vol = _volume_number(pack)
    return f'''
<section class="page--cover">
  <div class="cover__top">
    <span class="cover__brand">choosewise.education</span>
    <span>Prompt Library · Vol. {vol}</span>
  </div>

  <div class="cover__middle">
    <div class="cover__eyebrow">{_html.escape(pack["eyebrow_sv"])}</div>
    <div class="cover__count">{_html.escape(count_label)}</div>
    <h1 class="cover__title">{_html.escape(pack["title_sv"])}</h1>
    <p class="cover__subtitle">{_html.escape(subtitle)}</p>
  </div>

  <div class="cover__bottom">
    <div class="cover__tagline">
      Rätt verktyg vid rätt tillfälle.<br>
      En del av RÄTT-modellen på choosewise.education.
    </div>
    <div class="cover__volume">
      <span class="cover__volume__label">Vol.</span>
      <span class="cover__volume__number">{vol}</span>
    </div>
  </div>
</section>'''


def cover_en(pack: dict, total_prompts: int) -> str:
    subtitle = pack.get("subtitle_en") or "Ready-to-use prompts for planning, teaching and reflection."
    count_label = f"{total_prompts} chat prompts" if total_prompts else "Chat prompts"
    vol = _volume_number(pack)
    return f'''
<section class="page--cover">
  <div class="cover__top">
    <span class="cover__brand">choosewise.education</span>
    <span>Prompt Library · Vol. {vol}</span>
  </div>

  <div class="cover__middle">
    <div class="cover__eyebrow">{_html.escape(pack["eyebrow_en"])}</div>
    <div class="cover__count">{_html.escape(count_label)}</div>
    <h1 class="cover__title">{_html.escape(pack["title_en"])}</h1>
    <p class="cover__subtitle">{_html.escape(subtitle)}</p>
  </div>

  <div class="cover__bottom">
    <div class="cover__tagline">
      The right tool at the right time.<br>
      Part of the WISE framework at choosewise.education.
    </div>
    <div class="cover__volume">
      <span class="cover__volume__label">Vol.</span>
      <span class="cover__volume__number">{vol}</span>
    </div>
  </div>
</section>'''


def render_parts_sv(parts: list[dict]) -> str:
    """Emit one <section.section-opener> + <ol.prompts> per part."""
    out = []
    running_total = 0
    multi = len(parts) > 1
    for p in parts:
        count = len(p["prompts"])
        eyebrow = f"Del {p['number']} · {count} promptar" if multi else f"{count} promptar"
        title = p["title"] or "Promptar"
        out.append(f'''
<section class="section-opener">
  <div class="section-opener__eyebrow">{_html.escape(eyebrow)}</div>
  <h2>{_html.escape(title)}</h2>
</section>

<ol class="prompts"{'' if running_total == 0 else f' style="counter-reset: prompt {running_total};"'}>''')
        for prompt in p["prompts"]:
            out.append(f'  <li>{_html.escape(prompt)}</li>')
        out.append('</ol>')
        running_total += count
    return "\n".join(out)


def render_parts_en(parts: list[dict]) -> str:
    """Same shape as SV. Uses 'Part' and 'prompts' in English."""
    out = []
    running_total = 0
    multi = len(parts) > 1
    for p in parts:
        count = len(p["prompts"])
        eyebrow = f"Part {p['number']} · {count} prompts" if multi else f"{count} prompts"
        # The part title in EN data should have been translated
        title = p.get("title_en") or p["title"] or "Prompts"
        out.append(f'''
<section class="section-opener">
  <div class="section-opener__eyebrow">{_html.escape(eyebrow)}</div>
  <h2>{_html.escape(title)}</h2>
</section>

<ol class="prompts"{'' if running_total == 0 else f' style="counter-reset: prompt {running_total};"'}>''')
        for prompt in p["prompts"]:
            out.append(f'  <li>{_html.escape(prompt)}</li>')
        out.append('</ol>')
        running_total += count
    return "\n".join(out)


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<title>{title} — choosewise.education</title>
<link rel="stylesheet" href="_prompt-print.css">
</head>
<body>
{cover}
{boilerplate}
{parts}
{back}
{script}
</body>
</html>
"""


def build_sv(pack: dict, data: dict) -> str:
    return PAGE_TEMPLATE.format(
        lang="sv",
        title=_html.escape(pack["title_sv"].rstrip(".")),
        cover=cover_sv(pack, data["total_prompts"]),
        boilerplate=BOILERPLATE_SV.strip(),
        parts=render_parts_sv(data["parts"]),
        back=BACK_COVER_SV.strip(),
        script=SCRIPT_SNIPPET.strip(),
    )


def build_en(pack: dict, data: dict) -> str:
    return PAGE_TEMPLATE.format(
        lang="en",
        title=_html.escape(pack["title_en"].rstrip(".")),
        cover=cover_en(pack, data["total_prompts"]),
        boilerplate=BOILERPLATE_EN.strip(),
        parts=render_parts_en(data["parts"]),
        back=BACK_COVER_EN.strip(),
        script=SCRIPT_SNIPPET.strip(),
    )


def main():
    which_slug = sys.argv[1] if len(sys.argv) > 1 else None
    which_lang = sys.argv[2] if len(sys.argv) > 2 else None  # "sv", "en", or None

    wrote = 0
    for pack in PACKS:
        slug_sv = pack.get("slug_sv")
        slug_en = pack.get("slug_en")
        if which_slug and which_slug not in (slug_sv, slug_en):
            continue

        # SV
        if slug_sv and which_lang in (None, "sv"):
            data_path = DATA_DIR / f"{slug_sv}.json"
            if not data_path.exists():
                print(f"  ⚠ {slug_sv}: no data, skipping SV")
            else:
                data = json.load(open(data_path))
                html_out = build_sv(pack, data)
                out = SCRIPT_DIR / f"{slug_sv}-sv.html"
                out.write_text(html_out, encoding="utf-8")
                print(f"  ✓ {out.name} ({data['total_prompts']} prompts)")
                wrote += 1

        # EN — needs translated data (data-en/<slug_en>.json) AND pack not SV-only
        if slug_en and which_lang in (None, "en") and not pack.get("sv_only"):
            en_data_path = DATA_DIR / f"{slug_en}-en.json"
            if not en_data_path.exists():
                # EN data not yet translated — expected before translate-prompts runs
                continue
            data = json.load(open(en_data_path))
            html_out = build_en(pack, data)
            out = SCRIPT_DIR / f"{slug_en}-en.html"
            out.write_text(html_out, encoding="utf-8")
            print(f"  ✓ {out.name} ({data['total_prompts']} prompts)")
            wrote += 1

    print(f"\n{wrote} HTML files written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
