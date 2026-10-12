# Gemini- och NotebookLM-guiden, aktuell och internationell: implementationsplan

> **För agentiska arbetare:** OBLIGATORISK SUB-SKILL: använd superpowers:subagent-driven-development (rekommenderad) eller superpowers:executing-plans för att genomföra planen uppgift för uppgift. Stegen är kryssrutor (`- [ ]`) för spårning.

**Mål:** De två engelska Gemini/NotebookLM-PDF:erna levereras till Skool-communityt, faktamässigt sanna per oktober 2026 och skrivna för en engelskspråkig skolvärld i stället för en svensk — utan att något publiceras på sajten.

**Arkitektur:** Samma ryggrad som Copilot-rundan. En numrerad påståendeinventering (`docs/guide-facts-gemini.md`) upprättas och faktakontrolleras **innan** en enda guideyta rörs. Rundans kodarbete är att generalisera de två vakter som Copilot-rundan lämnade guidespecifika — TOC-vakten och leveransvakten — i stället för att kopiera dem. Därefter redigeras de två engelska ytorna parvis, aldrig en i taget, PDF:erna renderas om, innehållsförteckningens tio sidnummer räknas om mot den renderade filen, och facit omfångas selektivt med `--only`.

**Teknikstack:** `/usr/bin/python3` (3.9.6 — enda interpretern med pytest, playwright och Pillow), pytest, Playwright för PDF-rendering, `pdftotext`/`pdfinfo` (poppler) för textextraktion och sidräkning.

**Spec:** `docs/superpowers/specs/2026-10-12-gemini-guide-international-design.md`

**Gren:** `feat/gemini-guide-international`, från `main` (HEAD **`e2282b7`** — `main` flyttade sig under planeringen, PR #40 mergade ett blogginlägg; planens första utkast sa `26c661a`). Grenen bär också en merge av `origin/docs/gemini-guide-spec` (PR #39), eftersom `docs/` är gitignorerad och specen annars inte vore läsbar i worktreen.

**Baslinjen, mätt i worktreen på `e2282b7`:** **757 passed, 1 failed** med `scripts/tests/test_prompt_pdf_parity.py` exkluderad; med den filen inne tillkommer dess **elva miljöberoende fel** (spec §8, `/tmp/pdf-parity-before/` töms av macOS vid dygnsskifte).

**Det enda felet är PREEXISTERANDE och tillhör inte den här rundan:** `test_brand_mark.py::test_the_page_count_is_what_we_think` hävdar 198 sidor, och blogg-mergen gjorde dem 199 (`scripts/tests/test_brand_mark.py:176`). **Rundan rör det inte** — det är blogg-rundans regression och en rättning här skulle blanda två rundor. Varje uppgifts förväntade utfall ska alltså läsas som "757 + mina gröna, och det här ena röda kvar". **Är felen fler än ett, eller ett annat, är det rundans eget och ska lagas.**

---

## Globala villkor

- **`git add -A` används aldrig.** Repot har 26 ocommittade filer under `exports/` och `assets/pdfs/wise/` som tillhör Johan. Namnge varje fil i varje `git add`.
- **`git checkout --` körs aldrig på en katalog.** Det raderade två av Johans filer i våg 2a. På **namngiven fil** är det tillåtet; de svenska PDF:erna återställs ändå med `cp` från en kopia (Task 13), inte med git.
- **`docs/` är gitignorerad.** Inventeringen, planen och överlämningen committas med `git add -f`.
- **Interpretern är `/usr/bin/python3`** (3.9.6). Ingen `dict | dict`; använd `{**a, **b}`. `list[str]` i annoteringar kräver `from __future__ import annotations`.
- **Ingenting publiceras.** Inga poster i `guides-en.json`, ingen PAIR_MAP, ingen sitemap, inga og-kort, landningssidans uppräkning rörs inte. Allt arbete ligger under `_unpublished/`, plus testfiler, inventeringen och överlämningen.
- **De svenska ytorna rörs inte.** `_unpublished/exports/gemini-notebooklm-print-a4-sv.html`, `gemini-notebooklm-quick-start-sv.html` och `_unpublished/sv/guider/gemini-notebooklm/` lämnas som de står, och deras PDF:er ska vara **byte-identiska** när rundan är klar. Task 2 bygger vakten som säger det.
- **Layouten rörs inte.** Omslaget behåller sitt format och sin SVG, sidfoten sin form, de åtta stilbilderna sina platser. Jurisdiktionsrutan använder guidens **befintliga** `callout callout--watch`-komponent (sex förekomster i print redan) — ingen ny stil tillkommer.
- **Paletten och typografin rörs inte.** Enda typografiändringen är att webbytans Google Fonts-rader, dess tre `--font-*`-överskrivningar och dess sjutton inline-`font-family`-attribut tas bort, så att sidan ärver Blueprints `tokens.css`.
- **En faktamening utan post i inventeringen får inte skrivas.** Ärvs från Copilot-rundan, gäller utan undantag.
- **Ett fynd som inte behöver ändras stryks aldrig tyst.** Det står kvar i tabellen med en motivering.
- **Varje post bär källa, hämtdatum och vilken källa.** Rå HTML och lokal textextraktion; en sammanfattning är aldrig källa till ett värde. Googles sidor kan svara 403 mot `curl` precis som Microsofts marknadsföringssidor gjorde — ett påstående utan hämtbar källa blir `obelagt` och skrivs om utan siffra.
- **AI Act stannar, GDPR på artikelnivå går.** Spec §3, Johans beslut 2026-10-12. AI Act är det enda regelverk som får namnges i de engelska ytorna, och bara med de värden `docs/guide-facts-claude.md` post **P13** redan belägger. GDPR, Article 6(1)(e), Article 30, "national data protection authority", "every EU member state has one" och medlemsstatsjämförelserna ut. **Undantag:** dataresidens är **produktfakta** — var data lagras och behandlas får stå där meningen säger just det, aldrig som rättslig analys, och varje förekomst får en egen post med motiveringen utskriven. "Data controller" används som allmän yrkesterm, inte som hänvisning till en namngiven förordning.
- **Vaktblockets sekvens är inte Copilots.** Copilot-rundan skapade inventeringen med ett **tomt** vaktblock i Task 1 och lät de parametriserade vakterna `skip` på tomma block. Den skip:en finns inte längre: slutfixvågen lade `test_every_guides_guard_block_is_not_empty`, som kräver både `aktiv`- och `borttaget`-rader per guide i ytkartan. Därför läggs **`gemini` till i `surfacecheck.GUIDE_SURFACES` och `factinventory.INVENTORIES` först i Task 12**, i samma commit som vaktraderna skrivs. Fram till dess är inventeringen en ren människotext med ett tomt block, och varje commit är grön.
- **Radnumren i uppgifterna är mätta 2026-10-12, före rundans första ändring.** Task 5 tar bort tre `<link>`-rader ur `_unpublished/guides/gemini-notebooklm/index.html`, så **varje webb-radnummer i Task 6–11 ligger tre rader lägre efter Task 5**, och printytans numrering flyttar sig när Task 6–7 kortar juridiken. Behandla numren som en karta till rätt stycke, aldrig som adress: lokalisera med `grep -n "<sträng>"` före varje ändring. Står strängen inte där numret säger är numret gammalt, inte texten fel.
- **Sifferutfallen i stegen är räknade, inte mätta.** De utgår från baslinjens 757 och de tester planen lägger till; lägger du till ett test till räknar du om. Det som är bindande är **0 skipped och 0 xfailed i Task 17**, och att inget test-id från `main` har försvunnit **utom** de sex i `test_copilot_toc.py` och de tre i `test_copilot_delivery.py`, som byter nodeid när filerna döps om i Task 1 och 2 (se respektive uppgift).
- **Prosa som beror på en källa skrivs inte i planen.** Där formuleringen är avgjord — omslaget, avslutningen, jurisdiktionsrutan, bonuskapitlets skylt — står den ordagrant här. Där meningen bär ett faktavärde står i stället vad den ska säga och vilken post som belägger den, eftersom en förskriven faktamening vore ett värde utan källa.
- **Grindens tre beslut, Johan 2026-10-12, är inte längre antaganden.** (1) **Namnbytet omfattar allt, även filnamnen** — Task 4B och 4C äger det, och varje uppgift från Task 5 och framåt är skriven med de nya sökvägarna. (2) **Fristadsskolan-exemplet stannar** (Task 8), vilket är skälet att varken vaktblocket eller leveransvakten kan bära ett bart `Sweden`. (3) **Emotion recognition och examinationshögrisken tas in i bonuskapitlet; förbud 9 om nudification-appar tas inte in** — kapitlet stannar vid vad som gäller guidens egna verktyg och läsarens skola.
- **Fyra ord kan aldrig bli bara förbudsrader i den här guiden**, eftersom legitimt innehåll bär dem: `Sweden`/`Swedish` (G21:s källbelagda exempel), `GDPR` (G30:s promptplatshållare), `April 2026` (G03:s daterade produktpåståenden) och `NotebookLM` (citaten och källtitlarna). Varje vakt som vill fånga dem måste fånga en **fras ur guidens egen röst**, inte ordet.
- **Tio av 22 PDF:er är inte byte-identiska vid omrendering.** Skillnaden är Chromiums `CreationDate`/`ModDate`. En omrendering visar alltid ändrade filer även när innehållet är oförändrat — det är inte ett fynd.
- **En vakt som inte setts bli röd vaktar ingenting.** Bryt varje ny vakt med flit och se den fallera på det den vaktar. **En HTML-kommentar duger inte som brytning** — `surfacecheck._TAG` slukar den.

---

## Rättelser och tillägg till specen, inskrivna med avsikt

Fem saker mätningen 2026-10-12 visar som specen inte bär. Ingen av dem ändrar den valda vägen; alla fem ändrar vad en uppgift måste göra.

**1. Webbytans typsnittsfel är tre gånger större än specen säger.** Spec §2 räknar tre `<link>`-rader och tre `--font-*`-överskrivningar. Utöver dem bär `_unpublished/guides/gemini-notebooklm/index.html` **sjutton inline-`font-family`-attribut** i SVG-`<text>`-element: sex `Playfair Display` (rad 106, 114, 551, 556, 561, 566) och elva `Inter`. Tas bara de sex raderna bort står diagrammens text kvar i Crestiora-typsnitt — och eftersom ett inline-attribut vinner över varje `:root`-token går felet inte att se i en CSS-granskning. Copilots båda ytor hade **noll** sådana attribut, så fällan är ny för den här rundan. Printytan har noll (`grep -c Playfair` = 0) och är alltså redan ren. Task 5 äger alla tjugotre förekomsterna, och review-fokus 4 är testet som gör ett återfall rött.

**2. "AI Act stannar" betyder inte "AI Act är orörd".** Spec §3 säger att AI Act-fakta *redan är belagda* i Claude-guidens post P13. Det stämmer — och tre av dem är **belagda som felaktiga**, med rättningen redan skriven och redan levererad i den publicerade Claude-guiden. Gemini-guiden bär fortfarande förvärdena:

| Står i Gemini-guiden | P13:s belagda värde | Rad i EP |
|---|---|---|
| "phases in through 2026 and beyond" | blev tillämplig **2 augusti 2026** | 1028 |
| "Limited risk" | **Transparency risk** | 1042 (pyramiden), 1062 (brödtext) |
| "Minimal risk" | **Minimal or no risk** | 1037 (pyramiden), 1061 (brödtext) |

Den publicerade `exports/claude-print-a4-en.html` använder **Unacceptable / High risk / Transparency risk / Minimal or no risk** (rad 1276–1306). Gemini-guidens fjärde nivå heter "Prohibited" och ska bli "Unacceptable risk" av samma skäl. Task 7 äger detta, och det kostar en korsreferens till P13 — ingen ny källdomän.

**3. Den svenska inramningen innehåller ett namngivet svenskt klassrumsexempel.** Spec §2 räknar "Swedish"/"Sweden" till 2/3 utan att säga vad förekomsterna är. Två av dem är ett **källbelagt praktikexempel**: Viktor Säfström och David Folkebrant, Fristadsskolan i Eskilstuna, publicerat på Pedagog Eskilstuna — EP rad 831 och 896, EW rad 333 och 405. Det är guidens enda konkreta, namngivna skolexempel på 42 sidor. **Antagande som Johan får korrigera när han läser planen: exemplet stannar**, med en post och en utskriven motivering, eftersom spec §9 uttryckligen tillåter "ett medvetet, motiverat exempel med en post i inventeringen" och ett sourcat praktikfall är innehåll, inte inramning. Det som går är de två ställen där Sverige används som **jurisdiktionsexempel** (EP 979, EP 1031) och språkexemplet "including Swedish and other EU languages" (EP 831). Följden för koden står i review-fokus 1: Gemini-guidens förbudslista kan därför **inte** innehålla ett bart "Sweden" eller "Swedish", som Copilots gör.

**4. Ett påstående om Johan själv är inte längre sant.** EP rad 1611 och EW rad 1209: *"I have a full-time job and run this work alongside it"*. Johan lämnade Advania i augusti 2026 och är sedan dess egen konsult (CLAUDE.md §1). Meningen står **inte** i Claude- eller Copilot-guidens engelska ytor — den är Gemini-guidens egen. Specens postklasser täcker produkt, pris, licens, funktion och regelverk, inte författaren; posten skapas ändå, eftersom påståendet är volatilt och falskt. Task 10 äger det.

**5. Produktnamnens antal skiljer sig mellan de två engelska ytorna.** Spec §6 listar misstänkta namn med ett antal var. Mätt per yta 2026-10-12 är tre av dem **asymmetriska**: `Gems` EP 25 / EW 24, `Audio Overview` EP 10 / EW 11, `AI Ultra` EP 5 / EW 6. Antalet i sig är ingen fälla — asymmetrin är det, eftersom den betyder att ytorna redan säger olika saker om samma produkt. Task 9 läser varje asymmetri och avgör om den är en formuleringsskillnad eller en saklig divergens; det senare rättas på båda ytorna.

---

## Granskningsfokus

Fem fel som specen förutsätter men som ingen uppgifts tester annars skulle fånga. Varje rad har fått sitt test inlagt i den uppgift som äger koden.

1. **En kopierad förbudslista förbjuder rätt innehåll.** Copilots leveransvakt förbjuder "Sweden" och "Swedish" rakt av. Generaliseras den med en delad lista blir Gemini-guiden röd för det källbelagda Fristadsskolan-exemplet — och den billigaste vägen till grönt är då att stryka exemplet, alltså att vakten styr innehållet i stället för att vakta det. → Task 2, `test_each_guides_forbidden_list_is_its_own` och `test_geminis_forbidden_list_does_not_ban_what_the_spec_keeps`.
2. **En guide utan ankare i TOC-kartan ger en tyst grön vakt.** Parametriseras vakten över en karta vars `anchors` är tom för en guide samlas noll tester in för den — och en tom parametrisering är grön. → Task 1, `test_every_guide_in_the_toc_map_has_anchors_for_every_row`.
3. **TOC-ankaret är hämtat ur en mening rundan själv skriver om.** Bonuskapitlets ankare står i den ingress som namnger GDPR, och Task 7 skriver om just den meningen. Skrivs den om utan ankarledet kan vakten aldrig hitta kapitlets startsida igen — och felmeddelandet säger "ankaret står inte på någon sida", vilket läser som ett vaktfel, inte ett innehållsfel. Det som biter är `assert actual is not None` i `test_every_toc_page_number_matches_the_rendered_pdf` — den blir röd, men med ett meddelande som pekar på vakten. → Task 7 bevarar ledet ordagrant, Task 14 steg 1 verifierar om alla tio ankaren mot den nya utskriften **innan** numren skrivs in.
4. **Inline-`font-family` överlever varje CSS-rättning.** De sjutton attributen i webbytans SVG:er vinner över `tokens.css` och syns inte i någon av våg 1:s CSS-vakter. → Task 5, `test_the_guide_web_surfaces_have_no_crestiora_fonts`.
5. **De svenska PDF:erna skrivs om varje gång de engelska renderas.** Båda byggarna renderar EN *och* SV utan språkargument. Återställs de svenska slarvigt är facit för deras nycklar oförändrat — innehållsfingeravtrycket är ju detsamma — och hela sviten går grön medan två filer ligger ändrade i arbetsträdet. → Task 2, `test_the_swedish_gemini_pdfs_are_untouched_since_the_merge_base`.

---

## Filstruktur

| Fil | Ansvar | Uppgift |
|---|---|---|
| `scripts/tests/test_guide_toc.py` | **ny** (ersätter `test_copilot_toc.py`) — TOC-vakten, karta per guide | Task 1, 14 |
| `scripts/tests/test_copilot_toc.py` | **tas bort** — innehållet flyttas oförändrat in i kartan | Task 1 |
| `scripts/tests/test_guide_delivery.py` | **ny** (ersätter `test_copilot_delivery.py`) — leveransvakten, förbudslista per guide, plus de svenska PDF:ernas byte-identitet | Task 2, 13 |
| `scripts/tests/test_copilot_delivery.py` | **tas bort** | Task 2 |
| `scripts/tests/test_fonts.py` | webbytans typsnitt, nu även inline-attributen | Task 5 |
| `scripts/tests/surfacecheck.py` | ytkartan — en rad för `gemini` | Task 12 |
| `scripts/tests/factinventory.py` | inventeringssökvägarna — en rad för `gemini` | Task 12 |
| `scripts/tests/test_capture_guide_baseline.py` | `RECAPTURED_THIS_ROUND` töms och fylls om | Task 15 |
| `docs/guide-facts-gemini.md` | **ny** — påståendeinventeringen med vaktblocket | Task 3 (skelett + poster), 4 (fakta), 12 (vaktrader) |
| `_unpublished/exports/gemini-notebooklm-print-a4-en.html` | källan till huvud-PDF:en — den egentliga leveransen | Task 5–10, 13, 14 |
| `_unpublished/guides/gemini-notebooklm/index.html` | webbytan, hålls i sak synkad med printytan | Task 5–10 |
| `_unpublished/guides/gemini-notebooklm/styles.css` | de tre typsnittsöverskrivningarna tas bort | Task 5 |
| `_unpublished/exports/gemini-notebooklm-quick-start-en.html` | källan till quick-start-PDF:en, går också till Skool | Task 11 |
| `_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf` | leverans | Task 13, 14 |
| `_unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-en.pdf` | leverans | Task 13 |
| `scripts/tests/fixtures/guide-pdf-baseline.json` | facit per sida, två nycklar omfångas | Task 15 |
| `scripts/tests/fixtures/guide-pdf-body-baseline.json` | facit per dokument, två nycklar omfångas | Task 15 |
| `docs/blueprint-handoff.md` | programöverlämningen, inklusive det svenska divergensläget | Task 17 |

---

# FÖRE GRINDEN — ingen guideyta rörs

## Task 1: TOC-vakten blir guide-agnostisk

**Filer:**
- Skapa: `scripts/tests/test_guide_toc.py`
- Ta bort: `scripts/tests/test_copilot_toc.py`
- Test: `scripts/tests/test_guide_toc.py`

**Gränssnitt:**
- Förbrukar: `pdf_fingerprint.extract(path) -> str`, `pdf_fingerprint.pages(text) -> list[str]`, `pdf_fingerprint.ROOT`, `surfacecheck.normalise(text) -> str`.
- Producerar:
  - `GUIDE_TOC: dict[str, dict]` — nyckel guide, värde `{"template": str, "pdf": str, "toc_page": int, "anchors": dict[str, str]}`.
  - `config_for(guide: str) -> dict` — höjer `KeyError` med kända guider namngivna.
  - `toc_rows(guide: str) -> list[tuple[str, int]]`.
  - `XFAIL_UNTIL_RECOUNTED: set[tuple[str, str]]` — `(guide, förteckningsrubrik)` för de rader vars nummer är fel i utgångsläget och rättas i Task 14.

**Varför en ny fil och inte en kopia.** `test_copilot_toc.py` bär guidens namn i filnamnet, i `TEMPLATE`, i `PDF` och i `ANCHORS`. En kopia till `test_gemini_toc.py` ger två filer med samma logik och två ställen att laga — samma fel som `CLAUDE`-listan var, och den kostade en eskalering i våg 2b (spec §7). Copilots sex ankare flyttas in **oförändrade**.

**Test-id:n som försvinner, med avsikt.** De sex `test_copilot_toc.py::test_every_toc_page_number_matches_the_rendered_pdf[…]` och `test_the_toc_has_the_six_rows_we_think_it_has` byter nodeid när filen döps om. Det är den enda tillåtna id-förlusten i den här uppgiften; jämför den insamlade mängden mot `main` i steg 5 och kontrollera att varje borttaget id har en motsvarighet i den nya filen.

- [ ] **Steg 1: Skriv den nya filen**

```python
# scripts/tests/test_guide_toc.py
"""Innehållsförteckningens sidnummer mot den renderade PDF:en.

Våg 2b:s dyraste fel: 13 av 15 hårdkodade sidnummer i Claude-guidens
förteckning var fel, och ingen vakt såg det — texten granskades sexton
gånger utan att någon öppnade dokumentet. Copilot-rundan byggde vakten
men band den till en guide; den här rundan gör den guide-agnostisk
(spec §7).

Vakten läser numren ur mallen och letar upp varje avsnitts faktiska
startsida i den renderade PDF:en. Ankarsträngarna är valda ur
`pdftotext`-utskriften, inte ur HTML:en: extraktionen spärrar versaler
oförutsägbart ("PA R T 1"), så en spärrad etikett vore ett ankare som
aldrig matchar. Sökningen börjar på sidan efter förteckningen själv —
annars matchar varje ankare förteckningens egen rad.

Claude-guiden står UTANFÖR kartan, med avsikt. Dess förteckning
använder `toc-title`/`toc-page-num` i stället för `toc__title`/
`toc__page`, numren är nollutfyllda ("04"), och arton rader delar sidor
mellan delrubrik och underrad, vilket gör ankarvalet tvetydigt. Att ta
in den kräver en andra radregex och arton ankare verifierade mot en PDF
den här rundan inte renderar om. Att Claudes femton nummer står
ovaktade sedan våg 2b är en känd lucka och står i överlämningen.
"""
from __future__ import annotations

import re

import pytest

from . import pdf_fingerprint as fp
from . import surfacecheck

GUIDE_TOC = {
    # Copilots sex ankare, flyttade oförändrade ur test_copilot_toc.py.
    # Två av dem byttes under Copilot-rundan efter kontroll mot
    # pdftotext-utskriften: Part 3:s ankare sa "CDP" (texten säger "EDP"),
    # och "About this guide" matchade även sidan 3.
    "copilot": {
        "template": "_unpublished/exports/copilot-print-a4-en.html",
        "pdf": "_unpublished/assets/pdfs/guides/copilot-guide-en.pdf",
        "toc_page": 2,
        "anchors": {
            "Why this guide exists": "Why this guide exists",
            "Part 1 · Get started": "Which product are you actually using?",
            "Part 2 · Work smarter": "Copilot Chat (with your work data)",
            "Part 3 · Compliance & licensing": "What EDP actually gives you",
            "FAQ": "Questions teachers ask",
            "About this guide": "Johan Lindström, October 2026",
        },
    },
    # Gemini: tio rader, tio ankare, alla verifierade mot den renderade
    # PDF:en 2026-10-12 — varje ankare träffar först på den sida
    # avsnittet faktiskt börjar på. Inget ankare är hämtat ur en spärrad
    # etikett; openarna står som "PA R T 1", "O R I E N TAT I O N",
    # "BONUS CHAPTER" och "PROMPTS" i utskriften.
    "gemini": {
        "template": "_unpublished/exports/gemini-notebooklm-print-a4-en.html",
        "pdf": "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf",
        "toc_page": 2,
        "anchors": {
            "Introduction":
                "Before the how, a word on the why",
            "Understanding Gemini and NotebookLM":
                "two complementary views onto a single Google account",
            "Part 1 · Getting Started":
                "If you have never opened Gemini or NotebookLM, start here",
            "Part 2 · Working Smarter":
                "returning to Gemini or NotebookLM for the same kind of task",
            "Part 3 · Scale & Lead":
                "for educators who want to do more than save personal time",
            "Part 4 · Google Workspace for Education":
                "Many schools run Google Workspace for Education",
            # Ankaret står i den ingress Task 7 skriver om. Ledet
            # "If you teach or lead a school in an EU member state"
            # bevaras ordagrant där; resten av meningen byts.
            "Bonus Chapter · For EU readers":
                "If you teach or lead a school in an EU member state",
            "The Styles Library":
                "The same notebook and the same prompt will produce very different outputs",
            "Prompts":
                "Copy these prompts, adapt them to your context, run them",
            "FAQ":
                "Is the free tier enough?",
        },
    },
}

# De åtta av Geminis tio nummer som är FEL i utgångsläget, mätta mot den
# renderade PDF:en 2026-10-12. Driften växer från −1 till −4, alltså en
# förteckning som aldrig räknats om sedan kapitel växte:
#
#   Part 1 · Getting Started            säger  8, börjar på  7   (−1)
#   Part 2 · Working Smarter            säger 13, börjar på 12   (−1)
#   Part 3 · Scale & Lead               säger 20, börjar på 19   (−1)
#   Part 4 · Google Workspace…          säger 24, börjar på 22   (−2)
#   Bonus Chapter · For EU readers      säger 28, börjar på 25   (−3)
#   The Styles Library                  säger 32, börjar på 28   (−4)
#   Prompts                             säger 34, börjar på 30   (−4)
#   FAQ                                 säger 40, börjar på 39   (−1)
#
# Introduction (3) och Understanding (5) stämmer redan och står därför
# INTE här — en xfail på dem skulle bli xpassed, och `strict=True` gör
# xpassed rött. Markeringarna tas bort i Task 14, efter att numren
# räknats om mot den OMRENDERADE filen; sidorna flyttar sig när Task 6–7
# kortar juridiken, så dagens åttasiffriga drift är inte slutvärdet.
XFAIL_UNTIL_RECOUNTED = {
    ("gemini", "Part 1 · Getting Started"),
    ("gemini", "Part 2 · Working Smarter"),
    ("gemini", "Part 3 · Scale & Lead"),
    ("gemini", "Part 4 · Google Workspace for Education"),
    ("gemini", "Bonus Chapter · For EU readers"),
    ("gemini", "The Styles Library"),
    ("gemini", "Prompts"),
    ("gemini", "FAQ"),
}

GUIDES = tuple(GUIDE_TOC)

_TOC_ROW = re.compile(
    r'<span class="toc__title">(?P<title>.*?)(?:<span class="toc__sub">.*?</span>)?'
    r'\s*</span>.*?<span class="toc__page">(?P<page>\d+)</span>',
    re.S)


def config_for(guide: str) -> dict:
    try:
        return GUIDE_TOC[guide]
    except KeyError:
        raise KeyError(
            f"okänd guide {guide!r}, kända: {sorted(GUIDE_TOC)}"
        ) from None


def toc_rows(guide: str) -> list:
    """surfacecheck.normalise gör entiteterna till tecken, så nyckeln
    `Part 3 · Scale & Lead` matchar markupens `&amp;`."""
    html = (fp.ROOT / config_for(guide)["template"]).read_text(encoding="utf-8")
    return [(surfacecheck.normalise(re.sub(r"<[^>]+>", " ", m.group("title"))),
             int(m.group("page")))
            for m in _TOC_ROW.finditer(html)]


def _cases():
    for guide, cfg in GUIDE_TOC.items():
        for title in cfg["anchors"]:
            marks = ([pytest.mark.xfail(
                        strict=True,
                        reason="numret är fel i utgångsläget, räknas om i Task 14")]
                     if (guide, title) in XFAIL_UNTIL_RECOUNTED else [])
            yield pytest.param(guide, title, marks=marks, id=f"{guide}:{title}")


def test_an_unknown_guide_is_a_loud_error():
    """En guide som inte finns i kartan får inte ge en tom konfiguration
    — då vaktar vakten ingenting och är grön för det."""
    with pytest.raises(KeyError) as exc:
        config_for("apple-intelligence")
    assert "copilot" in str(exc.value) and "gemini" in str(exc.value)


@pytest.mark.parametrize("guide", GUIDES)
def test_every_guide_in_the_toc_map_has_anchors_for_every_row(guide):
    """Granskningsfokus 2: en guide med tom ankarlista samlar in noll
    parametriseringar, och en tom parametrisering är grön utan att vakta
    något. Den här raden är det som gör en tom lista röd."""
    cfg = config_for(guide)
    assert cfg["anchors"], f"{guide}: ankarlistan är tom"
    assert len(cfg["anchors"]) == len(toc_rows(guide))


@pytest.mark.parametrize("guide", GUIDES)
def test_the_toc_has_the_rows_we_think_it_has(guide):
    """Går regexen sönder blir listan tom, och en tom lista är en grön
    vakt som vaktar ingenting."""
    rows = toc_rows(guide)
    assert [title for title, _ in rows] == list(config_for(guide)["anchors"]), rows


@pytest.mark.parametrize("guide,title", list(_cases()))
def test_every_toc_page_number_matches_the_rendered_pdf(guide, title):
    cfg = config_for(guide)
    claimed = dict(toc_rows(guide))[title]
    anchor = surfacecheck.normalise(cfg["anchors"][title])
    pages = [surfacecheck.normalise(page)
             for page in fp.pages(fp.extract(fp.ROOT / cfg["pdf"]))]
    actual = next((i + 1 for i, page in enumerate(pages)
                   if i + 1 > cfg["toc_page"] and anchor in page), None)
    assert actual is not None, (
        f"ankaret {anchor!r} står inte på någon sida efter {cfg['toc_page']} — "
        "välj ett ankare ur pdftotext-utskriften, inte ur HTML:en")
    assert actual == claimed, (
        f"{guide} {title!r}: förteckningen säger {claimed}, "
        f"avsnittet börjar på {actual}")
```

- [ ] **Steg 2: Kör den nya filen och läs utfallet rad för rad**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_guide_toc.py -v`

Förväntat: **1 + 2 + 2 + 16 tester**, varav Copilots sex PASS, Geminis två korrekta (Introduction, Understanding) PASS och Geminis åtta XFAIL. **Noll XPASS.** Ett xpassed betyder att numret redan stämmer och att raden ska ut ur `XFAIL_UNTIL_RECOUNTED`, inte att markeringen ska bli icke-strikt. Ett FAIL på "ankaret står inte på någon sida" betyder att ett ankare är felskrivet — jämför mot utskriften i steg 3.

- [ ] **Steg 3: Se att de åtta xfail:en faller på rätt sak**

Kör:
```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_toc.py -v --runxfail 2>&1 | grep -E "förteckningen säger|står inte på någon sida"
```
Förväntat: åtta rader av formen `gemini 'Part 1 · Getting Started': förteckningen säger 8, avsnittet börjar på 7` — alltså **innehållsfel, inte ankarfel**. Står det "står inte på någon sida" någonstans är det ankaret som är fel, och det måste lagas här, inte i Task 14.

- [ ] **Steg 4: Ta bort den gamla filen**

```bash
git rm scripts/tests/test_copilot_toc.py
```

- [ ] **Steg 5: Jämför de insamlade test-id:na mot `main`**

```bash
WS=.superpowers/sdd/2026-10-12-gemini-guide-international
/usr/bin/python3 -m pytest scripts/tests/ -q --collect-only 2>/dev/null | grep "::" | sort > "$WS/ids-task1.txt"
diff "$WS/ids-main.txt" "$WS/ids-task1.txt"
```
Förväntat: exakt sju borttagna id:n, alla ur `test_copilot_toc.py`, och deras motsvarigheter tillagda under `test_guide_toc.py` plus Geminis sexton. Försvinner något annat id är en parametrisering trasig.

**`$WS/ids-main.txt` är insamlad i förväg** (775 id:n på `e2282b7`, innan grenens första ändring) och ligger i rundans arbetskatalog. **Använd ALDRIG `git stash` för att jämföra mot `main`:** stashstacken delas mellan worktreen och Johans huvudkopia, där 31 ocommittade filer ligger — en `git stash pop` i fel ordning kan ta hans ändringar. Behöver du mäta om `main` skapar du en engångs-worktree (`git worktree add --detach ../ids-main main`) och tar bort den efteråt.

- [ ] **Steg 6: Hela sviten och commit**

Kör: `/usr/bin/python3 -m pytest scripts/tests/ -q --ignore=scripts/tests/test_prompt_pdf_parity.py`
Förväntat: **763 passed, 8 xfailed, 0 skipped.** Räkningen: baslinjens 757 minus de sju borttagna Copilot-id:na, plus trettonde gröna av filens tjugoen.

```bash
git add scripts/tests/test_guide_toc.py
git commit -m "test(gemini): TOC-vakten blir guide-agnostisk, Geminis tio ankare inlagda"
```

---

## Task 2: Leveransvakten blir guide-agnostisk, och de svenska PDF:erna får sin byte-vakt

**Filer:**
- Skapa: `scripts/tests/test_guide_delivery.py`
- Ta bort: `scripts/tests/test_copilot_delivery.py`
- Test: `scripts/tests/test_guide_delivery.py`

**Gränssnitt:**
- Förbrukar: `pdf_fingerprint.extract(path) -> str`, `pdf_fingerprint.ROOT`, `pdf_fingerprint.UNPUBLISHED_GUIDE_PDFS`.
- Producerar: `GUIDE_DELIVERY: dict[str, dict]` med nycklarna `pdfs`, `forbidden`, `untouched`; `delivery_for(guide) -> dict`.

**Förbudslistan är per guide, inte delad.** Copilots lista förbjuder `"Sweden"`, `"Swedish"` och `"GDPR"` rakt av. Delas den med Gemini blir vakten röd för **två saker som ska stå kvar**: det källbelagda Fristadsskolan-exemplet (rättelse 3 ovan) och promptmallens platshållare `[e.g. GDPR + EU AI Act + your national school-governance law]`, som spec §3 uttryckligen låter stanna eftersom den visar formen på läsarens eget svar. En delad lista skulle alltså göra den billigaste vägen till grönt att stryka innehåll vakten inte har någon åsikt om. Geminis lista förbjuder i stället **inramningen och den artikelnivå-GDPR som väljs bort**, sträng för sträng.

- [ ] **Steg 1: Skriv den nya filen**

```python
# scripts/tests/test_guide_delivery.py
"""Leveransen är de engelska PDF:erna, inte HTML:en de renderas ur.

Varje annan vakt i rundan läser HTML. Rättas HTML:en utan att PDF:erna
renderas om går hela sviten grön medan filen som går till Skool
fortfarande bär den svenska inramningen. Den här vakten läser det som
levereras.

Den täcker också quick-starten, som med avsikt står utanför
ytkonsistensvakten (spec §5) och annars inte bevakas av något som läser
dess innehåll.

Förbudslistan är PER GUIDE. Copilot-rundan valde väg A rakt av och kan
därför förbjuda "Sweden", "Swedish" och "GDPR" bart. Gemini-rundan kan
inte: ett källbelagt svenskt praktikexempel stannar (spec §9 tillåter
det uttryckligen), och en promptmall innehåller ordet GDPR som
platshållare läsaren själv fyller i. En delad lista vore en vakt som
styr innehållet i stället för att vakta det.
"""
from __future__ import annotations

import hashlib
import re
import subprocess

import pytest

from . import pdf_fingerprint as fp

GUIDE_DELIVERY = {
    "copilot": {
        "pdfs": (
            "_unpublished/assets/pdfs/guides/copilot-guide-en.pdf",
            "_unpublished/assets/pdfs/guides/copilot-quick-start-en.pdf",
        ),
        # Oförändrad ur test_copilot_delivery.py.
        "forbidden": (
            "Swedish", "Sweden", "Skolverket", "IMY", "Schrems", "GDPR",
            "April 2026", "kr 350",
        ),
        "untouched": (),
    },
    "gemini": {
        "pdfs": (
            "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf",
            "_unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-en.pdf",
        ),
        # Inramningen och den artikelnivå-GDPR spec §3 väljer bort, sträng
        # för sträng. Inget bart "Sweden"/"Swedish" och inget bart "GDPR":
        # se modulens docstring. Och inget bart "April 2026" — sju
        # meningar bär datumet som ett DATERAT PRODUKTPÅSTÅENDE ("Since 8
        # April 2026 the two tools sync bidirectionally"), och de står
        # eller faller på sin källa, inte på rundans datumstämpel. De två
        # STÄMPLARNA bevakas i stället var och en på sin plats, av
        # test_geminis_cover_and_closing_carry_the_rounds_date nedan.
        "forbidden": (
            "Skolverket", "IMY", "Schrems",
            "Swedish schools",
            "Swedish and other EU languages",
            "Sweden, as of April 2026",
            "Sweden is a notable example",
            "GDPR fundamentals",
            "Standard GDPR discipline",
            "carrying GDPR risk",
            "the GDPR and the EU AI Act",
            "Article 6(1)(e)",
            "Article 30",
            "national data protection authority",
            "Every EU member state has one",
            "phases in through 2026 and beyond",
            "Limited risk",
            "I have a full-time job",
        ),
        # Spec §1: de svenska ytorna ska komma ut byte-identiska. Båda
        # byggarna renderar EN *och* SV i samma körning, så de skrivs
        # varje gång de engelska renderas om.
        "untouched": (
            "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-sv.pdf",
            "_unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-sv.pdf",
        ),
    },
}

GUIDES = tuple(GUIDE_DELIVERY)

# Röd till Task 13 har renderat om PDF:erna. Mängden är PER PDF, inte per
# guide: quick-starten bär INGEN av de arton förbudssträngarna redan i dag
# (mätt 2026-10-12 — den har varken svensk inramning eller juridisk text),
# så en xfail på den vore en strikt XPASS, alltså röd av fel skäl. Samma
# form som XFAIL_UNTIL_RECOUNTED i test_guide_toc.py: (guide, identitet).
XFAIL_UNTIL_RERENDERED = {
    ("gemini", "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf"),
}


def delivery_for(guide: str) -> dict:
    try:
        return GUIDE_DELIVERY[guide]
    except KeyError:
        raise KeyError(
            f"okänd guide {guide!r}, kända: {sorted(GUIDE_DELIVERY)}"
        ) from None


def _flat(rel: str) -> str:
    """pdftotext -layout bryter rader mitt i meningar; en sträng som
    'Swedish schools' står med radbrytning emellan i den renderade
    filen. Platta till allt blankt till ett mellanslag innan sökning."""
    return re.sub(r"\s+", " ", fp.extract(fp.ROOT / rel))


def _merge_base() -> str:
    """Grenens avstamp från `main`. Jämförelsepunkten måste ligga före
    rundan: på `HEAD` vore vakten en snubbeltråd i arbetsträdet, och en
    gång committad skada skulle passera för alltid."""
    return subprocess.run(
        ["git", "merge-base", "main", "HEAD"],
        capture_output=True, text=True, check=True, cwd=fp.ROOT).stdout.strip()


def _delivery_cases():
    for guide, cfg in GUIDE_DELIVERY.items():
        for rel in cfg["pdfs"]:
            marks = ([pytest.mark.xfail(
                        strict=True,
                        reason="röd till Task 13 har renderat om PDF:erna")]
                     if (guide, rel) in XFAIL_UNTIL_RERENDERED else [])
            yield pytest.param(guide, rel, marks=marks, id=f"{guide}:{rel.rsplit('/', 1)[-1]}")


@pytest.mark.parametrize("guide,rel", list(_delivery_cases()))
def test_the_delivered_pdfs_carry_no_abandoned_claim(guide, rel):
    flat = _flat(rel)
    found = [needle for needle in delivery_for(guide)["forbidden"] if needle in flat]
    assert found == [], f"{rel} bär kvar: {found}"


@pytest.mark.parametrize("guide", GUIDES)
def test_the_quick_start_pdf_is_part_of_the_delivery_guard(guide):
    """Quick-starten står utanför ytvakten med avsikt. Faller den också
    ur den här vakten bevakas dess innehåll av ingenting alls."""
    pdfs = delivery_for(guide)["pdfs"]
    assert any("quick-start" in rel for rel in pdfs), guide
    for rel in pdfs:
        assert rel in fp.UNPUBLISHED_GUIDE_PDFS, f"{rel} står inte i facitlistan"


@pytest.mark.parametrize("guide", GUIDES)
def test_each_guides_forbidden_list_is_its_own(guide):
    """Granskningsfokus 1: listan får inte bli delad igen. En guide utan
    egna strängar är en guide vars vakt någon har slagit ihop."""
    cfg = delivery_for(guide)
    assert cfg["forbidden"], f"{guide}: tom förbudslista"
    others = {needle for other, c in GUIDE_DELIVERY.items() if other != guide
              for needle in c["forbidden"]}
    assert set(cfg["forbidden"]) - others, (
        f"{guide}: varje förbjuden sträng delas med en annan guide — "
        "listan har slagits ihop och vaktar inte den här guidens beslut")


def test_geminis_forbidden_list_does_not_ban_what_the_spec_keeps():
    """Granskningsfokus 1, andra halvan. Två saker STANNAR i Gemini-
    guiden och en kopierad Copilot-lista hade förbjudit båda: det
    källbelagda Fristadsskolan-exemplet (spec §9: medvetet, motiverat
    exempel med en post) och promptmallens GDPR-platshållare (spec §3).
    En bar sträng här skulle göra vakten röd för rätt innehåll."""
    forbidden = delivery_for("gemini")["forbidden"]
    for kept in ("Sweden", "Swedish", "GDPR", "EU AI Act", "Article 4"):
        assert kept not in forbidden, (
            f"{kept!r} är en bar sträng i Geminis förbudslista — "
            "den träffar innehåll rundan har beslutat att behålla")


@pytest.mark.xfail(strict=True, reason="röd till Task 13 har renderat om PDF:erna")
def test_geminis_cover_and_closing_carry_the_rounds_date():
    """Datumstämplarna, var och en på sin plats.

    En bar förbudsrad på "April 2026" går inte för den här guiden (se
    kommentaren i kartan), så omslaget kontrolleras som SIDA 1 och
    avslutningen genom signaturens hela sträng. Det är de två ställen där
    datumet är en stämpel på dokumentet och inte ett påstående om en
    produkt.
    """
    main = "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf"
    cover = re.sub(r"\s+", " ", fp.pages(fp.extract(fp.ROOT / main))[0])
    assert "October 2026" in cover, "omslaget bär inte rundans datum"
    assert "April 2026" not in cover, "omslaget bär kvar den gamla stämpeln"
    flat = _flat(main)
    assert "Johan Lindström, October 2026" in flat
    assert "Johan Lindström, April 2026" not in flat


@pytest.mark.parametrize(
    "rel", GUIDE_DELIVERY["gemini"]["untouched"],
    ids=lambda rel: rel.rsplit("/", 1)[-1])
def test_the_swedish_gemini_pdfs_are_untouched_since_the_merge_base(rel):
    """Granskningsfokus 5: båda byggarna renderar EN *och* SV utan
    språkargument, så de svenska filerna skrivs varje gång de engelska
    renderas om. Återställs de slarvigt är INNEHÅLLSfacit ändå
    oförändrat — fingeravtrycket är detsamma, bara `CreationDate` har
    rört sig — och hela sviten går grön medan två filer ligger ändrade.
    Den här vakten jämför bytes mot bascommiten, inte innehåll."""
    committed = subprocess.run(
        ["git", "show", f"{_merge_base()}:{rel}"],
        capture_output=True, check=True, cwd=fp.ROOT).stdout
    assert hashlib.sha256(committed).hexdigest() == \
           hashlib.sha256((fp.ROOT / rel).read_bytes()).hexdigest(), \
           f"{rel} är inte byte-identisk med bascommiten — spec §1"
```

- [ ] **Steg 2: Kör den och läs utfallet**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_guide_delivery.py -v`
Förväntat: Copilots två PASS, Geminis **huvudguide XFAIL**, Geminis **quick-start PASS**, de övriga sju PASS. **Noll XPASS.** Att quick-starten är grön från början är mätt, inte antaget: den bär noll av de arton strängarna. Ett xpassed på huvudguiden skulle däremot betyda att den redan är ren, vilket den inte är — `grep` i steg 3 visar vilka femton strängar som står kvar.

- [ ] **Steg 3: Se att xfail:en faller på innehåll och inte på en felskriven sträng**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_delivery.py -v --runxfail 2>&1 | grep "bär kvar"
```
Förväntat: två rader som räknar upp strängarna. Huvud-PDF:en ska bära `GDPR fundamentals`, `Standard GDPR discipline`, `carrying GDPR risk`, `the GDPR and the EU AI Act`, `Article 6(1)(e)`, `Article 30`, `national data protection authority`, `Every EU member state has one`, `phases in through 2026 and beyond`, `Limited risk`, `I have a full-time job`, `Swedish schools`, `Sweden, as of April 2026`, `Sweden is a notable example` och `Swedish and other EU languages`. **`Skolverket`, `IMY` och `Schrems` står inte i guiden alls** (spec §2: 0/0/0) — de står i listan som spärr mot att de smyger in, och de ska alltså *inte* dyka upp i utskriften. **En sträng som INTE står kvar i utgångsläget är ett stavfel i listan, inte ett löst problem:** kontrollera varje sådan mot HTML-källan med `grep -n` innan du går vidare. Strängen `Swedish schools` står på EP rad 1031 (inuti AI Act-stycket) men inte i quick-starten — att den bara faller på en av de två PDF:erna är alltså korrekt.

- [ ] **Steg 4: Bryt byte-vakten med flit**

```bash
cp _unpublished/assets/pdfs/guides/gemini-notebooklm-guide-sv.pdf /tmp/gemini-sv-backup.pdf
printf '%% rör' >> _unpublished/assets/pdfs/guides/gemini-notebooklm-guide-sv.pdf
/usr/bin/python3 -m pytest scripts/tests/test_guide_delivery.py -k untouched -v 2>&1 | tail -8
cp /tmp/gemini-sv-backup.pdf _unpublished/assets/pdfs/guides/gemini-notebooklm-guide-sv.pdf
git status --short -- _unpublished/assets/pdfs/guides/
```
Förväntat: `gemini-notebooklm-guide-sv.pdf är inte byte-identisk med bascommiten`, och efter återställningen en **tom** `git status`. Blir vakten inte röd vaktar den ingenting.

- [ ] **Steg 5: Ta bort den gamla filen, kör sviten, commit**

```bash
git rm scripts/tests/test_copilot_delivery.py
/usr/bin/python3 -m pytest scripts/tests/ -q --ignore=scripts/tests/test_prompt_pdf_parity.py
```
Förväntat: **769 passed, 11 xfailed, 0 skipped.** Räkningen: Task 1:s 763 minus de tre borttagna Copilot-id:na, plus nio gröna av filens tolv.

```bash
git add scripts/tests/test_guide_delivery.py
git commit -m "test(gemini): leveransvakten blir guide-agnostisk, svenska PDF:erna får sin byte-vakt"
```

---

## Task 3: Inventera varje volatilt påstående

**Filer:**
- Skapa: `docs/guide-facts-gemini.md`

Ingen källa läses här och ingen yta redigeras. Uppgiften är att hitta och lokalisera varje påstående som kan ha åldrats, som bär svensk inramning eller som faller under omriktningen — med radnummer per yta. **Ett påstående som inte står i tabellen får inte skrivas om senare.** Rundan väntas bli ungefär dubbelt så stor som Copilots 27 poster: guiden är 42 sidor och täcker två produkter.

- [ ] **Steg 1: Skapa skelettet**

```bash
cat > docs/guide-facts-gemini.md <<'DOCEOF'
# Påståendeinventering — Gemini- och NotebookLM-guiden

**Rundan:** Gemini/NotebookLM-guiden, internationell omriktning. Spec: `docs/superpowers/specs/2026-10-12-gemini-guide-international-design.md`
**Upprättad:** 2026-10-12
**Faktakontrollerad:** (Task 4)

Varje volatilt faktapåstående i de **engelska** ytorna, med alla sina
förekomster. De svenska ytorna ingår inte i rundan (spec §1) och har därför
inga poster.

Ytorna: **EW** `_unpublished/guides/gemini-notebooklm/index.html` · **EP**
`_unpublished/exports/gemini-notebooklm-print-a4-en.html` · **QS**
`_unpublished/exports/gemini-notebooklm-quick-start-en.html`

**QS står utanför ytkonsistensvakten** — avsiktligt, spec §5: quick-starten är
en tredje yta med egen, kortare formulering, och kravet "ordagrant på alla
ytor" vore rött från dag ett och därmed värdelöst. Den bevakas i stället av
förekomstkolumnen här, av PDF-facit, och av leveransvakten
(`scripts/tests/test_guide_delivery.py`).

## Hur källorna läses

Varje sida hämtas som rå HTML och läses ordagrant; texten extraheras lokalt ur
markupen. Ingen sida sammanfattas av ett annat modellanrop, och en
sammanfattning är aldrig källa till ett värde. Där källor går emot varandra
står båda, och den nyare vinner — med noteringen att de skiljer sig.

**Googles sidor kan svara 403 mot `curl`**, precis som Microsofts
marknadsföringssidor gjorde i förra rundan. Ett påstående utan hämtbar källa
blir `obelagt` och skrivs om utan siffra — det får inte bli `stämmer` på en
sida ingen kunde läsa.

**Två poster hämtar sitt belägg ur en annan inventering.** AI Act-fakta är
redan verifierade i `docs/guide-facts-claude.md` post **P13** (källa:
Europeiska kommissionen, `digital-strategy.ec.europa.eu`, läst 2026-10-08).
Där P13 räcker står `korsref P13` i källkolumnen och ingen ny hämtning görs —
det var hela skälet att AI Act fick stanna (spec §3).

## Poster

Utfallen är `stämmer`, `fel: <rätt värde>` och `obelagt: <vad källan säger i
stället>`. **Varje utfallscell inleds med sin token**, så att kolumnen går att
skanna utan att läsa resonemanget.

`fel` har två betydelser, ärvda från Copilot-inventeringen och de får inte
läsas som samma sak. `fel: <rätt värde>` betyder att en hämtad källa säger
något annat än ytan. `fel (omfång)` betyder att påståendet inte är sakligt
osant men ligger utanför det omfång rundan valde (spec §3) — **ingen källa
motsäger det, och den som letar efter en sådan letar förgäves.**

| id | påstående idag | typ | EW | EP | QS | källa + datum | utfall |
|---|---|---|---|---|---|---|---|

## Observationer utanför posterna

## Vaktblock

```guard
# Fylls i Task 12, i samma commit som `gemini` läggs till i
# surfacecheck.GUIDE_SURFACES och factinventory.INVENTORIES.
# Till dess är blocket tomt MED AVSIKT: `test_every_guides_guard_block_is_not_empty`
# kräver både aktiv- och borttaget-rader för varje guide i ytkartan, så
# ett tomt block kan inte samexistera med en ifylld ytkarta.
```
DOCEOF
```

- [ ] **Steg 2: Mät inramningen och juridiken**

```bash
# kör från repots rot — i den här rundan är det worktreen, inte huvudkopian
for f in _unpublished/guides/gemini-notebooklm/index.html \
         _unpublished/exports/gemini-notebooklm-print-a4-en.html \
         _unpublished/exports/gemini-notebooklm-quick-start-en.html; do
  echo "=== $f"
  grep -nE "Swedish|Sweden|Skolverket|IMY|GDPR|Schrems|DPIA|Article [0-9]|data protection authority|supervisory|member state|April 2026" "$f" | cut -c1-130
done
```
Varje träff hör till antingen en post (ett påstående som ska rättas) eller en omriktning (en formulering som ska skrivas om). Båda listas. **Noll träffar i QS är det förväntade** — quick-starten är redan fri från både inramning och juridik, till skillnad från Copilots, som pekade läsare till en 404.

- [ ] **Steg 3: Mät produktfakta**

Särskilt misstänkta enligt spec §6, eftersom Google döper om och paketerar om ofta. Antalen i tabellen nedan är mätta per yta 2026-10-12; **avvikelser mellan EP och EW är det som ska läsas, inte antalet i sig.**

```bash
EP=_unpublished/exports/gemini-notebooklm-print-a4-en.html
EW=_unpublished/guides/gemini-notebooklm/index.html
QS=_unpublished/exports/gemini-notebooklm-quick-start-en.html
for n in "Workspace for Education" "Gems" "Canvas" "Deep Research" \
         "Audio Overview" "Video Overview" "Education Plus" \
         "NotebookLM Enterprise" "Gemini for Education" "AI Pro" "AI Ultra" \
         "Teaching & Learning" "Studio" "13+" "18+"; do
  printf "%-26s EP:%-4s EW:%-4s QS:%s\n" "$n" \
    "$(grep -o "$n" $EP | wc -l | tr -d ' ')" \
    "$(grep -o "$n" $EW | wc -l | tr -d ' ')" \
    "$(grep -o "$n" $QS | wc -l | tr -d ' ')"
done
```

| namn | EP | EW | QS |
|---|---|---|---|
| Workspace for Education | 24 | 24 | 1 |
| Gems | **25** | **24** | 0 |
| Canvas | 19 | 19 | 0 |
| Deep Research | 13 | 13 | 1 |
| Audio Overview | **10** | **11** | 4 |
| Video Overview | 8 | 8 | 1 |
| Education Plus | 7 | 7 | 0 |
| AI Ultra | **5** | **6** | 0 |
| AI Pro | 3 | 3 | 0 |
| NotebookLM Enterprise | 2 | 2 | 0 |
| Gemini for Education | 2 | 2 | 0 |

De tre fetmarkerade asymmetrierna är rättelse 5 i planens inledning. Var och en läses i sitt sammanhang och avgörs: formuleringsskillnad (ingen åtgärd, men en rad i "Observationer utanför posterna") eller saklig divergens (post, och rättning på båda ytorna i Task 9).

- [ ] **Steg 4: Skriv tabellen**

En rad per påstående, id `G01`, `G02`, … Kolumnerna är `id | påstående idag | typ | EW | EP | QS | källa + datum | utfall`. `typ` är en av `produktnamn`, `pris`, `licens`, `funktion`, `URL`, `åldersgräns`, `dataresidens`, `regelverk`, `inramning`, `datumstämpel`, `citat`, `författarfakta`. Platser är radnummer; `—` betyder att påståendet inte står på den ytan. Lämna `källa + datum` och `utfall` tomma — Task 4 äger dem.

Dessa är kända från mätningen och **ska** finnas med (fler tillkommer ur steg 2–3):

| id | påstående | typ | plats |
|---|---|---|---|
| G01 | Omslagets datumstämpel "April 2026" | datumstämpel | EP 486 |
| G02 | Avslutningens signatur "— Johan Lindström, April 2026" | datumstämpel | EP 1623 |
| G03 | "Since 8 April 2026 the two tools sync bidirectionally" — det daterade produktpåståendet, samt dess odaterade varianter | funktion | EP 610, 628, 640, 719, 847, 1546; EW 100, 118, 130, 351, 1144 |
| G04 | Innehållsförteckningens tio sidnummer | datumstämpel | EP 502, 509, 516, 523, 530, 537, 544, 551, 558, 565 |
| G05 | `Workspace for Education` som namn och som licensinnehåll | produktnamn | EP passim, EW passim, QS 1 |
| G06 | `Gems` — asymmetrisk EP 25 / EW 24 | produktnamn | EP passim, EW passim |
| G07 | `Canvas` som namngiven funktion | produktnamn | EP passim, EW passim |
| G08 | `Deep Research` som "multi-step agent" | funktion | EP 1416 m fl, EW passim, QS 1 |
| G09 | `Audio Overview` — asymmetrisk EP 10 / EW 11 — plus de fyra formaten och "added September 2025" | funktion | EP 831, EW 333, QS 4 |
| G10 | Interaktivt läge för Audio Overview "still in beta" | funktion | EP 831, EW 333 |
| G11 | `Video Overview` som endast NotebookLM-sidig | funktion | EP 862 m fl, EW passim, QS 1 |
| G12 | De två licensvägarna: `Education Plus` och `Teaching & Learning add-on` | licens | EP 970, EW 482 |
| G13 | `NotebookLM Enterprise` på Google Cloud med EU-residens; Workspace-versionens residens | dataresidens | EP 973, 1023; EW 485, 537 |
| G14 | `Gemini for Education` som licensnamn | produktnamn | EP 968, EW 480 |
| G15 | Utrullningsordningen "AI Ultra, Pro, and Plus subscribers; the free tier follows" | licens | EP 847, EW 351 |
| G16 | Åldersgolven: Gemini Live 18+, premium-Workspace-funktioner 18+, NotebookLM 13+ | åldersgräns | EW 138, EP (lokalisera med `grep -n "13+"`) |
| G17 | Granulära per-app-toggles "rolling out through 2026" | funktion | EP 982, EW 494 |
| G18 | Google Classroom AI-funktioner "free with all Workspace for Education accounts" | licens | EP 987, EW 499 |
| G19 | "I have built 140 such styles" + pekaren `choosewise.education/infographic-styles/` | URL | EP 1094, 1164; EW 611, 615–682 |
| G20 | Matt Miller-citatet "a personal tutor that only knows what you teach" (Ditch That Textbook, januari 2026) | citat | EP 636, 719; EW (lokalisera) |
| G21 | Säfström/Folkebrant-exemplet, Fristadsskolan i Eskilstuna, Pedagog Eskilstuna februari 2026 — **stannar**, se rättelse 3 | inramning | EP 831, 896; EW 333, 405 |
| G22 | "including Swedish and other EU languages" som språkexempel | inramning | EP 831, EW 333 |
| G23 | Huvudflödets juridikpassage "Data residency, GDPR, and national context" | regelverk | EP 972–979, EW 484–491 |
| G24 | Bonuskapitlets GDPR-halva: ingressen och hela avsnittet "GDPR fundamentals for schools using AI" | regelverk | EP 1016, 1018–1025; EW 530, 532–539 |
| G25 | AI Act-ingressens "entered into force on 1 August 2024 and phases in through 2026 and beyond" | regelverk | EP 1028, EW 542 |
| G26 | Risknivåernas fyra namn: Minimal risk / Limited risk / High risk / Prohibited | regelverk | EP 1037, 1042, 1047, 1052 (pyramiden), 1061–1064 (brödtexten); EW 551, 556, 561, 566 + brödtexten |
| G27 | Artikel 4-påståendena: "has applied since 2 February 2025", "in force since 2 February 2025" | regelverk | EP 596, 912, 940, 1029, 1075, 1430 |
| G28 | "Sweden, as of April 2026, is among the countries that have not… the dominant framework for Swedish schools" | inramning | EP 1031, EW 545 |
| G29 | "others (Sweden is a notable example, as of April 2026) have not yet" — **står bara på EP** | inramning | EP 979, EW — |
| G30 | Promptmallens platshållare "[e.g. GDPR + EU AI Act + your national school-governance law]" — **stannar**, spec §3 | regelverk | EP 1357, EW 915 |
| G31 | "I have a full-time job and run this work alongside it" | författarfakta | EP 1611, EW 1209 |
| G32 | Avslutningens CTA: "you can also reach out through my website (link in the footer)" | inramning | EP 1611, EW 1209 |
| G33 | Del 3: "Update the school's records of processing (GDPR, a European regulation — Article 30)" | regelverk | EP 921, EW 430 |
| G34 | Del 3: "You are personally carrying GDPR risk that belongs with your organisation" | regelverk | EP 934, EW 443 |

**G33 och G34 är förflygsskanningens fynd 2026-10-12:** spec §3 räknar GDPR till tre ställen utanför bonuskapitlet, men printytan har **fem**. Mät själv i steg 2 — `grep -c "Article 30"` ska ge 4 och `grep -c "national data protection authority"` 3, alltså fler än Del 4:s passage rymmer. Task 6 äger rättningen.

**G29 är i sig ett fynd:** webbytan saknar redan Sverige-parentesen som printytan bär, alltså divergerar de två engelska ytorna **i dag** på exakt en av rundans känsligaste meningar. Det hör i "Observationer utanför posterna" också, eftersom det säger något om hur de två ytorna har underhållits.

- [ ] **Steg 5: Kontrollera att varje radnummer stämmer**

```bash
/usr/bin/python3 - <<'PY'
from pathlib import Path
# Klistra in (fil, rad, en kort sträng ur påståendet) för VARJE post och se
# att strängen verkligen står på den raden. En felpekande post skickar
# Task 5–11 till fel stycke.
checks = [
    ("_unpublished/exports/gemini-notebooklm-print-a4-en.html", 486, "April 2026"),
    ("_unpublished/exports/gemini-notebooklm-print-a4-en.html", 1623, "Johan Lindström, April 2026"),
    ("_unpublished/exports/gemini-notebooklm-print-a4-en.html", 640, "Since 8 April 2026"),
    ("_unpublished/exports/gemini-notebooklm-print-a4-en.html", 1028, "phases in through 2026 and beyond"),
    ("_unpublished/exports/gemini-notebooklm-print-a4-en.html", 1042, "Limited risk"),
    ("_unpublished/exports/gemini-notebooklm-print-a4-en.html", 979, "Sweden is a notable example"),
    ("_unpublished/exports/gemini-notebooklm-print-a4-en.html", 1031, "Swedish schools"),
    ("_unpublished/exports/gemini-notebooklm-print-a4-en.html", 1357, "your national school-governance law"),
    ("_unpublished/exports/gemini-notebooklm-print-a4-en.html", 1611, "full-time job"),
    ("_unpublished/guides/gemini-notebooklm/index.html", 491, "others have not yet"),
    ("_unpublished/guides/gemini-notebooklm/index.html", 1209, "full-time job"),
]
for rel, line, needle in checks:
    text = Path(rel).read_text(encoding="utf-8").splitlines()[line - 1]
    print(("OK  " if needle in text else "FEL "), rel, line, needle)
PY
```
Förväntat: OK på varje rad. Utöka listan till samtliga poster. **Raden `index.html` 491 med `others have not yet` är G29:s belägg** — står strängen där utan Sverige-parentes är divergensen bekräftad.

- [ ] **Steg 6: Commit**

```bash
git add -f docs/guide-facts-gemini.md
git commit -m "docs(gemini): inventera guidens volatila påståenden"
```

---

## Task 4: Faktakontrollera varje post mot namngiven källa

**Filer:**
- Modifiera: `docs/guide-facts-gemini.md` (kolumnerna `källa + datum` och `utfall`, plus "Observationer utanför posterna")

Ingen yta redigeras. Varje post får en källa med hämtdatum och ett utfall: **stämmer**, **fel** (med det rätta värdet), eller **obelagt** (källan säger inte det guiden säger).

- [ ] **Steg 1: Hämta källorna som rå HTML**

Sidorna läses ordagrant, inte sammanfattade. Googles egna sidor är källan för produkt, licens, funktion och åldersgräns:

```bash
mkdir -p /tmp/gemini-sources
while read -r name url; do
  curl -sSL -A "Mozilla/5.0" -o "/tmp/gemini-sources/$name.html" -w "$name %{http_code}\n" "$url"
done <<'URLS'
workspace-ai      https://workspace.google.com/solutions/ai/
edu-plus          https://edu.google.com/workspace-for-education/editions/
gemini-edu        https://edu.google.com/workspace-for-education/gemini/
notebooklm-help   https://support.google.com/notebooklm/
gemini-help       https://support.google.com/gemini/
notebooklm-ent    https://cloud.google.com/agentspace/notebooklm-enterprise/docs/overview
URLS
```
**Ett 403 eller 404 är ett resultat, inte ett fel att kringgå.** Skriv statuskoden i källkolumnen och sätt utfallet `obelagt`. Påståendet skrivs då om utan siffra i Task 9 — det raderas inte och det behålls inte oförändrat.

- [ ] **Steg 2: Extrahera text lokalt och läs värdena**

```bash
for f in /tmp/gemini-sources/*.html; do
  echo "=== $f"
  /usr/bin/python3 - "$f" <<'PY'
import re, sys, html
raw = open(sys.argv[1], encoding="utf-8", errors="replace").read()
raw = re.sub(r"<(script|style)\b.*?</\1>", " ", raw, flags=re.S | re.I)
text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
print(re.sub(r"\s+", " ", text)[:4000])
PY
done
```

- [ ] **Steg 3: AI Act-posterna korsrefereras, de hämtas inte om**

G25, G26 och G27 belägges ur `docs/guide-facts-claude.md` post **P13**. Läs posten och skriv in de värden som gäller:

```bash
grep -n "^| P13 " docs/guide-facts-claude.md | tr '|' '\n' | sed -n '7,9p' | cut -c1-2000
```

De tre värden som rättar guiden, direkt ur P13:

| post | guiden säger | P13:s belagda värde |
|---|---|---|
| G25 | "phases in through 2026 and beyond" | förordningen **blev tillämplig 2 augusti 2026** |
| G26 | "Limited risk" | **Transparency risk** |
| G26 | "Minimal risk" | **Minimal or no risk** |
| G26 | "Prohibited" | **Unacceptable risk** |

Och de två som **stämmer** och därför inte ändras — men som enligt regel 2 aldrig stryks tyst: ikraftträdandet 1 augusti 2024, och artikel 4:s tillämpning sedan 2 februari 2025. **Den publicerade `exports/claude-print-a4-en.html` använder redan de fyra rättade nivånamnen** (rad 1276–1306); Gemini-guiden ska använda samma fyra, så att de två guiderna inte säger olika saker om samma förordning.

- [ ] **Steg 4: Citatet kontrolleras mot sin egen källa**

G20 är Matt Millers formulering, inte Googles. Den kontrolleras mot Ditch That Textbook, inte mot en Google-sida, och om citatet inte går att hitta ordagrant blir utfallet `obelagt` — ett citationstecken är ett löfte om ordalydelse.

- [ ] **Steg 5: Skriv utfallen och räkna dem**

Varje cell inleds med sin token. Skriv under tabellen: **utfallsräkningen** (hur många `stämmer`, `fel`, `obelagt`), vilka poster som bär en andra token längre in i cellen, och **varje konflikt mellan källor** — att två Google-sidor säger olika saker är i sig ett resultat och står i respektive cell.

- [ ] **Steg 6: Commit**

```bash
git add -f docs/guide-facts-gemini.md
git commit -m "docs(gemini): faktakontrollera inventeringen mot namngivna källor"
```

---

```
# ⟨ GRIND ⟩
#
# Johan läser Task 4:s utfall innan en enda mening skrivs om.
#
# Tre saker avgörs här, och de är alla hans:
#
#  1. ANTAGANDET OM FRISTADSSKOLAN-EXEMPLET (rättelse 3). Planen utgår
#     från att det stannar. Säger Johan att det går, så går också
#     "Sweden"/"Swedish" in i leveransvaktens förbudslista som bara
#     strängar, och Task 8 blir kortare.
#  2. OBELAGDA PÅSTÅENDEN. Varje post som blev `obelagt` ska skrivas om
#     utan siffra. Vilka siffror som är värda en andra källhämtning, och
#     vilka som får gå, är hans bedömning.
#  3. FÖRBUD 9 OCH DECEMBER 2026. P13 bär ett datum som ligger två
#     månader framför en guide daterad oktober 2026. Om det hör hemma i
#     den här guidens bonuskapitel är Johans beslut, inte planens.
#
# Inget efter den här raden körs före grinden.
```

---

# EFTER GRINDEN — de två engelska ytorna redigeras parvis

**Regeln för hela avsnittet:** varje saklig ändring görs på **båda** engelska ytorna i samma commit, aldrig en i taget. Ytkonsistensvakten läses in först i Task 12, så fram till dess finns ingen vakt som fångar en halvgjord ändring — bara disciplinen.

## Task 4B: Filnamnen, sökvägarna och vaktlagret

**Johans beslut vid grinden 2026-10-12: namnbytet omfattar ALLT, även filnamnen.** Google döpte om NotebookLM till **Gemini Notebook** den 16 juli 2026 (post G49, verifierad av controllern: Workspace Updates-posten svarar 200 med rubriken "NotebookLM is now Gemini Notebook", och `notebooklm.google.com`, `support.google.com/notebooklm/` och `notebooklm.google` 301-redirectar alla till de nya namnen).

**Filer:**
- Byt namn: `_unpublished/exports/gemini-notebooklm-print-a4-en.html`, `gemini-notebooklm-quick-start-en.html`, `_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf`, `gemini-notebooklm-quick-start-en.pdf`, katalogen `_unpublished/guides/gemini-notebooklm/`, dess `assets/screenshot-notebooklm-audio.png`, och `exports/build-gemini-notebooklm-pdf.py`
- Modifiera: `scripts/tests/pdf_fingerprint.py`, `pdf_body_text.py`, `test_guide_toc.py`, `test_guide_delivery.py`, `test_guide_pdf_body_text.py`, `test_guide_pdf_font_weights.py`, `test_build_scripts.py`, `test_guide_asset_paths.py`, **`test_capture_guide_baseline.py` (`RECAPTURED_THIS_ROUND` — se ruling 3)**, `exports/build-guide-pdfs.py`, `exports/build-gemini-quickstart-pdf.py`, `_unpublished/guides/gemini-notebook/index.html` (**bildreferensen OCH nedladdningslänkarna — `data-gate`, `data-gate-pdf` och `href` kring rad 1222 och 1225 pekar också på de gamla PDF-namnen**), `_unpublished/exports/gemini-notebook-quick-start-en.html` (sökvägsreferensen), `docs/guide-facts-gemini.md` (ythuvudet), och de två facit-JSON-filerna

**Sök brett innan du bockar uppgiften:** `grep -rn "gemini-notebooklm" ` över de tre engelska ytorna och den omdöpta webbkatalogen. Listan ovan är mätt, men den mätningen letade efter sökvägar i kod — en referens inne i ett HTML-attribut syns inte i den sökningen.

**Tre rulings som avgränsar uppgiften, och som du inte ska vidga:**

1. **Bara EN-filerna byter namn.** De svenska ytorna behåller `gemini-notebooklm-*` och `sv/guider/gemini-notebooklm/`, eftersom deras innehåll fortfarande säger NotebookLM — de står utanför rundan med aprilfakta (spec §1), och ett namnbyte där hade gjort filnamnet osant om innehållet. Följden är att `test_the_swedish_gemini_pdfs_are_untouched_since_the_merge_base` fungerar oförändrat: dess merge-base-uppslagning sker på sökvägar som inte rört sig.
2. **`scripts/build-seo-meta.py` rörs INTE.** Dess rader 51, 57 och 75 bär `/guides/gemini-notebooklm/` och `/sv/guider/gemini-notebooklm/`, och rad 75 är PAIR_MAP — som spec §1 uttryckligen förbjuder rundan att röra. Inkonsekvensen är avsiktligt kvarlämnad och skrivs in i överlämningen med radnummer (Task 17).
3. **Facitvakten kräver EN ändring — rättat 2026-10-12 efter att uppgiften kördes.** Planen hävdade först att vakten kunde lämnas orörd, eftersom de två EN-PDF:erna "redan står i `RECAPTURED_THIS_ROUND`". **Det var fel.** Listan bar fortfarande Copilot-rundans två nycklar, för planen lägger omfyllningen i Task 15 — så efter namnbytet slog `committed[rel]` fel på de nya nycklarna och tre tester föll. Rätt åtgärd, verifierad: fyll `RECAPTURED_THIS_ROUND` med de **två nya gemini-nycklarna** redan här, enligt filens egen konvention ("töms och fylls om i varje ny runda"). Task 15 bekräftar sedan samma två namn.

   **Kontrollera samtidigt att nyckelbytet inte smugglade in en innehållsändring** — det är vad vakten annars hade gjort åt dig:
   ```bash
   /usr/bin/python3 - <<'PY'
   import json, subprocess
   MB = subprocess.run(["git","merge-base","main","HEAD"],capture_output=True,text=True,check=True).stdout.strip()
   PAIRS = [("_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf",
             "_unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf"),
            ("_unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-en.pdf",
             "_unpublished/assets/pdfs/guides/gemini-notebook-quick-start-en.pdf")]
   for f in ("guide-pdf-baseline.json","guide-pdf-body-baseline.json"):
       rel = f"scripts/tests/fixtures/{f}"
       before = json.loads(subprocess.run(["git","show",f"{MB}:{rel}"],capture_output=True,text=True,check=True).stdout)
       after = json.loads(open(rel,encoding="utf-8").read())
       assert len(after) == 22, len(after)
       for old_k, new_k in PAIRS:
           assert before[old_k] == after[new_k], f"{f}: {new_k} fick ett ändrat värde"
       others = [k for k in after if k not in dict(PAIRS).values()]
       assert not [k for k in others if before.get(k) != after[k]], f"{f}: drift på en orörd nyckel"
       print(f"{f}: 22 nycklar, båda värdena oförändrade, noll drift")
   PY
   ```
   **En starkare variant som nästa runda kan välja i stället:** ge vakten en namnbyteskarta (`committed[gammal_nyckel]` mot `current[ny_nyckel]`) så att värdena fortsätter bevakas ända till den runda som faktiskt renderar om filerna. `RECAPTURED`-vägen når samma slutläge men lämnar de två filerna obevakade däremellan.

**Namnformen:** prefixet blir `gemini-notebook`. Alltså `gemini-notebook-print-a4-en.html`, `gemini-notebook-quick-start-en.html`, `gemini-notebook-guide-en.pdf`, `gemini-notebook-quick-start-en.pdf`, katalogen `_unpublished/guides/gemini-notebook/`, bilden `screenshot-notebook-audio.png`, byggaren `exports/build-gemini-notebook-pdf.py`. **Guidenyckeln i vaktkartorna är och förblir `"gemini"`** — den bar aldrig produktnamnet och ska inte byta.

- [ ] **Steg 1: Byt namn med `git mv`**

```bash
git mv _unpublished/exports/gemini-notebooklm-print-a4-en.html \
       _unpublished/exports/gemini-notebook-print-a4-en.html
git mv _unpublished/exports/gemini-notebooklm-quick-start-en.html \
       _unpublished/exports/gemini-notebook-quick-start-en.html
git mv _unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf \
       _unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf
git mv _unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-en.pdf \
       _unpublished/assets/pdfs/guides/gemini-notebook-quick-start-en.pdf
git mv _unpublished/guides/gemini-notebooklm _unpublished/guides/gemini-notebook
git mv _unpublished/guides/gemini-notebook/assets/screenshot-notebooklm-audio.png \
       _unpublished/guides/gemini-notebook/assets/screenshot-notebook-audio.png
git mv exports/build-gemini-notebooklm-pdf.py exports/build-gemini-notebook-pdf.py
git status --short | head -40
```
Förväntat: enbart `R`-rader. **Står en `sv`-sökväg bland dem har du flyttat för mycket** — ångra och gör om.

- [ ] **Steg 2: Lokalisera varje referens som måste följa med**

```bash
git grep -n "gemini-notebooklm" -- scripts exports _unpublished docs | grep -v "^docs/superpowers/plans/" | grep -v "sv/guider\|-sv\.\|_sv\b"
```
Varje träff som pekar på en **EN**-sökväg eller på byggarens filnamn uppdateras. Varje träff som pekar på en **SV**-sökväg lämnas. Byggaren `exports/build-gemini-notebook-pdf.py` får en kommentar i sin `jobs`-lista som säger varför EN och SV nu har olika prefix — asymmetrin är avsiktlig och ska inte "städas" av nästa läsare.

- [ ] **Steg 3: Byt de två nycklarna i varje facit, med värdet oförändrat**

Det här är ett **nyckelbyte, inte en omfångning**. Värdet får inte röras — hade det gjorts vore det en tyst omfångning av en fil rundan ännu inte renderat om.

```bash
/usr/bin/python3 - <<'PY'
import json, collections
RENAME = {
    "_unpublished/assets/pdfs/guides/gemini-notebooklm-guide-en.pdf":
        "_unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf",
    "_unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-en.pdf":
        "_unpublished/assets/pdfs/guides/gemini-notebook-quick-start-en.pdf",
}
for f in ("guide-pdf-baseline.json", "guide-pdf-body-baseline.json"):
    rel = f"scripts/tests/fixtures/{f}"
    with open(rel, encoding="utf-8") as fh:
        data = json.load(fh, object_pairs_hook=collections.OrderedDict)
    out = collections.OrderedDict(
        (RENAME.get(k, k), v) for k, v in data.items())
    assert len(out) == len(data) == 22, (len(out), len(data))
    with open(rel, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"{f}: {len(out)} nycklar, två bytta")
PY
git diff --stat -- scripts/tests/fixtures/
```
**Kontrollera formen mot `main` innan du går vidare:** `git diff -- scripts/tests/fixtures/ | grep -c "^[+-]" ` ska vara litet. Är diffen tusentals rader har `json.dump` skrivit om formateringen av hela filen — läs hur filen var formaterad (indrag, nyckelordning, radslut) och matcha den i stället. **En omformaterad facitfil går inte att granska**, och den döljer i praktiken vad som ändrats.

- [ ] **Steg 4: Kör hela sviten**

Kör: `/usr/bin/python3 -m pytest scripts/tests/ -q --ignore=scripts/tests/test_prompt_pdf_parity.py`
Förväntat: **exakt samma siffror som före uppgiften** — 770 passed, 1 failed (det preexisterande `test_brand_mark`-felet), 10 xfailed, 0 skipped. Ett namnbyte får inte ändra ett enda testutfall. Gör det det har en referens inte följt med, och felmeddelandet namnger filen.

- [ ] **Steg 5: Kontrollera att ingenting förbjudet rörts**

```bash
git status --short | grep -E "sv/guider|-sv\.|build-seo-meta" && echo "FEL: förbjuden fil rörd" || echo "OK"
git diff --name-only | sort
```
Förväntat: `OK`, och i filistan ingen `build-seo-meta.py`, ingen svensk yta, ingen `guides-en.json`, ingen `sitemap.xml`.

- [ ] **Steg 6: Commit**

```bash
git add scripts/tests/pdf_fingerprint.py scripts/tests/pdf_body_text.py \
        scripts/tests/test_guide_toc.py scripts/tests/test_guide_delivery.py \
        scripts/tests/test_guide_pdf_body_text.py scripts/tests/test_guide_pdf_font_weights.py \
        scripts/tests/test_build_scripts.py scripts/tests/test_guide_asset_paths.py \
        scripts/tests/fixtures/guide-pdf-baseline.json \
        scripts/tests/fixtures/guide-pdf-body-baseline.json \
        exports/build-guide-pdfs.py exports/build-gemini-quickstart-pdf.py
git add -A -- _unpublished/exports _unpublished/assets/pdfs/guides _unpublished/guides exports
git add -f docs/guide-facts-gemini.md
git commit -m "refactor(gemini): EN-ytorna byter namn till gemini-notebook"
```
**OBS:** `git add -A` är annars förbjudet i den här rundan, men `git add -A -- <sökväg>` på de fyra namngivna katalogerna är det sättet git registrerar en katalogflytt med alla sina filer. Johans ocommittade filer ligger i **huvudkopian**, inte i worktreen, och ingen av de fyra sökvägarna rör dem. Kontrollera ändå `git status --short` före commit.

---

## Task 4C: Produktnamnet i prosan

**205 förekomster av `NotebookLM`** över de tre engelska ytorna: 97 i print, 94 på webbytan, 14 i quick-starten — plus guidens titel och den tryckta hjälpsides-URL:en.

**Filer:**
- Modifiera: `_unpublished/exports/gemini-notebook-print-a4-en.html`, `_unpublished/guides/gemini-notebook/index.html`, `_unpublished/exports/gemini-notebook-quick-start-en.html`
- Modifiera: `docs/guide-facts-gemini.md` (G49:s förekomstkolumner och den överlevandelista steg 4 kräver)

**Den gräns som gör uppgiften svår:** guidens **egen prosa** byter namn. **Citerat och attribuerat material gör det inte** — Pedagog Eskilstunas rubrik, Ditch That Textbooks sidtitel, Kasey Bells avsnittsnamn och choosewise.educations egen styles-sida skriver fortfarande "NotebookLM", och de har inte fel: de citerar och daterar sig själva. Ett citat som "rättas" är inte längre ett citat.

- [ ] **Steg 1: Byt namnet i guidens egen prosa**

Formen är **`Gemini Notebook`** vid första omnämnandet i varje del och i varje rubrik. **Där en mening annars skulle läsa "Gemini and Gemini Notebook" får andra ledet kortas till `Notebook`** — Googles egen domän är `notebook.google.com` och hjälpcentret heter "Gemini Notebook Help", så kortformen är leverantörens egen. Välj en form per mening och håll den genom stycket; en guide som växlar mellan "Gemini Notebook" och "Notebook" i samma stycke läser som två produkter.

- [ ] **Steg 2: Titeln och den tryckta URL:en**

Titeln blir — Johans angivna standard vid grinden, som han kan byta:
```html
  <h1>Gemini &amp; Gemini Notebook for teachers and school leaders</h1>
```
Den tryckta hjälpsides-URL:en på EP ~1610 / EW ~1208 säger `support.google.com/notebooklm`. Den **301:ar** till `support.google.com/gemininotebook` (verifierat 2026-10-12) — skriv dit den pekar, inte dit den pekade.

- [ ] **Steg 3: Lämna citaten i fred**

```bash
grep -n "NotebookLM" _unpublished/exports/gemini-notebook-print-a4-en.html \
  _unpublished/guides/gemini-notebook/index.html \
  _unpublished/exports/gemini-notebook-quick-start-en.html | cut -c1-150
```
Varje kvarvarande förekomst ska vara **inuti ett citat, en källtitel eller ett avsnittsnamn**. Är den i guidens egen röst har steg 1 missat den.

- [ ] **Steg 4: Skriv den överlevandelista som ersätter en förbudsrad**

**Varför det här steget finns:** `NotebookLM` kan **inte** bli en `borttaget`-rad i vaktblocket, och inte heller en förbjuden sträng i leveransvakten — citaten bär ordet legitimt, exakt samma fälla som ordet `Sweden` (G21) och ordet `GDPR` (G30). Vakten måste därför vakta något annat: **de överlevande förekomsterna, uppräknade.**

Skriv i inventeringen under G49: varje kvarvarande förekomst med yta, radnummer och vilket citat den tillhör. Task 12 gör en `aktiv`-rad på `Gemini Notebook` och `borttaget`-rader på guidens **egna** gamla formuleringar (de fraser där guidens röst sa NotebookLM), aldrig på det bara ordet.

- [ ] **Steg 5: Räkna**

```bash
for f in _unpublished/exports/gemini-notebook-print-a4-en.html \
         _unpublished/guides/gemini-notebook/index.html \
         _unpublished/exports/gemini-notebook-quick-start-en.html; do
  printf "%-62s NotebookLM:%-4s Gemini Notebook:%s\n" "$f" \
    "$(grep -o "NotebookLM" $f | wc -l | tr -d ' ')" \
    "$(grep -o "Gemini Notebook" $f | wc -l | tr -d ' ')"
done
```
Utgångsläget är 97 / 94 / 14. Slutläget ska vara **litet och förklarat** — varje kvarvarande förekomst har sin rad i steg 4:s lista. Ett nollvärde är sannolikt fel: det betyder att ett citat också skrevs om.

- [ ] **Steg 6: Commit**

```bash
git add _unpublished/exports/gemini-notebook-print-a4-en.html \
        _unpublished/guides/gemini-notebook/index.html \
        _unpublished/exports/gemini-notebook-quick-start-en.html
git add -f docs/guide-facts-gemini.md
git commit -m "content(gemini): produktnamnet blir Gemini Notebook i guidens egen röst"
```

---

## Task 5: Datumstämplarna och typsnitten

**Filer:**
- Modifiera: `_unpublished/exports/gemini-notebook-print-a4-en.html` (rad 486, 1623)
- Modifiera: `_unpublished/guides/gemini-notebook/index.html` (rad 10–12, 1229, plus sjutton inline-attribut)
- Modifiera: `_unpublished/guides/gemini-notebook/styles.css` (rad 21–23, 776)
- Modifiera: `scripts/tests/test_fonts.py`

**Gränssnitt:**
- Producerar: `test_fonts.GUIDE_WEB_SURFACES: tuple[str, ...]` — guidewebbytorna som är städade och ska förbli det.

- [ ] **Steg 1: Skriv det misslyckade testet**

Lägg till i `scripts/tests/test_fonts.py` (de befintliga sex testerna står kvar orörda):

```python
# Guidernas webbytor ligger under guides/ respektive _unpublished/guides/.
# published_files() utesluter HELA _unpublished/ (se brandguard.py), och
# guide_templates() täcker bara _unpublished/exports/*.html — alltså
# tryckmallarna, inte webbsidorna. Guidernas webbytor har därför aldrig
# haft någon typsnittsvakt, och det är precis därför både Copilots och
# Geminis sidor kunde ligga med Google Fonts.
#
# Listan är de guider vars webbyta ÄR städad och ska förbli det. De två
# som saknas — _unpublished/guides/apple-intelligence/ och
# _unpublished/guides/ai-for-students/ — bär fortfarande Crestioras
# typsnitt och tas i sina egna rundor; var runda lägger till sin guide
# här när den städat den. En glob över alla guider vore röd för dem från
# dag ett och därmed en vakt någon slår av.
GUIDE_WEB_SURFACES = (
    "guides/claude/index.html",
    "guides/claude/styles.css",
    "_unpublished/guides/copilot/index.html",
    "_unpublished/guides/copilot/styles.css",
    "_unpublished/guides/gemini-notebook/index.html",
    "_unpublished/guides/gemini-notebook/styles.css",
)

# Crestioras två typsnitt. 'Inter' söks med citattecken och som
# attributvärde: ordet "inter" förekommer i vanlig engelska ("interact",
# "interface") och en bar delsträngsökning vore brus.
_CRESTIORA_FONTS = (
    "Playfair",
    "'Inter'",
    '"Inter"',
    'font-family="Inter',
    "fonts.googleapis.com",
    "fonts.gstatic.com",
)


@pytest.mark.parametrize("rel", GUIDE_WEB_SURFACES)
def test_the_guide_web_surfaces_have_no_crestiora_fonts(rel):
    """Granskningsfokus 4: ett inline-`font-family`-attribut i en SVG
    vinner över varje token i `tokens.css` och syns inte i någon
    CSS-vakt. Gemini-guidens sida bar sjutton sådana (sex Playfair, elva
    Inter) utöver de tre `<link>`-raderna och de tre `--font-*`-
    överskrivningarna — tas bara raderna bort står diagrammens text kvar
    i Crestiora-typsnitt och ingenting blir rött.
    """
    text = (ROOT / rel).read_text(encoding="utf-8")
    found = [needle for needle in _CRESTIORA_FONTS if needle in text]
    assert found == [], f"{rel} bär kvar: {found}"
```

- [ ] **Steg 2: Kör och se det bli rött på rätt fil**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_fonts.py -v`
Förväntat: FAIL på **två** parametriseringar — `_unpublished/guides/gemini-notebook/index.html` (`Playfair`, `'Inter'`, `font-family="Inter`, `fonts.googleapis.com`, `fonts.gstatic.com`) och `.../styles.css` (`Playfair`, `'Inter'`). Claudes och Copilots fyra ska vara **gröna redan nu** — är de röda har någon av de tidigare rundorna regredierat, och det är ett eget fynd som ska rapporteras, inte lagas här.

- [ ] **Steg 3: Rensa webbytans typsnitt**

```bash
EW=_unpublished/guides/gemini-notebook/index.html
grep -nE "fonts\.(googleapis|gstatic)" $EW          # ska vara rad 10, 11, 12
grep -nE 'font-family="(Playfair|Inter)' $EW        # ska vara sjutton rader
grep -nE "Playfair|'Inter'" _unpublished/guides/gemini-notebook/styles.css  # 21, 22, 776
```

1. **Rad 10–12 i `index.html`:** de tre `<link>`-raderna (`preconnect` ×2 + stylesheet) tas bort i sin helhet. `tokens.css` är redan länkad i samma `<head>`.
2. **Rad 21–23 i `styles.css`:** `--font-display`, `--font-body` och `--font-mono` tas bort. Alla tre sätts av Blueprints `tokens.css`; en `:root`-överskrivning i guidens egen fil vinner över den, och då faller sidan tillbaka på Georgia och systemsans.
3. **Rad 776 i `styles.css`:** `font-family: var(--font-display, 'Playfair Display', serif);` → `font-family: var(--font-display);`. Fallbacken inuti `var()` är ett andra Crestiora-värde och återinför felet om token någon gång saknas.
4. **De sjutton inline-attributen i `index.html`:** varje `font-family="Playfair Display, serif"` → `font-family="var(--font-display)"`, varje `font-family="Inter, sans-serif"` (eller motsvarande) → `font-family="var(--font-body)"`. **Printytan är redan skriven så** (`grep -c "var(--font-" ` på EP ger träffar, `grep -c Playfair` ger 0) — alltså är formen inte ny, den är den som redan används på andra sidan av samma guide.

- [ ] **Steg 4: Byt de två datumstämplarna, på båda ytorna**

| yta | rad | från | till |
|---|---|---|---|
| EP | 486 | `<span class="cover__attr">April 2026</span>` | `<span class="cover__attr">October 2026</span>` |
| EP | 1623 | `<p class="closing__signature">— Johan Lindström, April 2026</p>` | `<p class="closing__signature">— Johan Lindström, October 2026</p>` |
| EW | 1229 | `<p class="cta-fineprint">Updated April 2026.</p>` | `<p class="cta-fineprint">Updated October 2026.</p>` |

**Rör ingen annan "April 2026".** De sju återstående förekomsterna är daterade **produktpåståenden** (G03: "Since 8 April 2026 the two tools sync bidirectionally", och de odaterade varianterna), och de står eller faller på sin källa i Task 9 — inte på rundans datumstämpel. Det är också skälet att varken leveransvakten eller vaktblocket får ha ett bart "April 2026" för den här guiden.

- [ ] **Steg 5: Kör testerna och commit**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_fonts.py scripts/tests/test_css_discipline.py scripts/tests/test_guide_print_css.py -v`
Förväntat: PASS på alla sex parametriseringar av det nya testet, och inga nya fel i de två befintliga CSS-vakterna.

```bash
git add scripts/tests/test_fonts.py \
        _unpublished/guides/gemini-notebook/index.html \
        _unpublished/guides/gemini-notebook/styles.css \
        _unpublished/exports/gemini-notebook-print-a4-en.html
git commit -m "fix(gemini): datumstämplarna till oktober, webbytan ärver Blueprints typsnitt"
```

---

## Task 6: Jurisdiktionsrutan in i huvudflödet

**Filer:**
- Modifiera: `_unpublished/exports/gemini-notebook-print-a4-en.html` (rad 921, 934, 972–979)
- Modifiera: `_unpublished/guides/gemini-notebook/index.html` (rad 430, 443, 484–491, minus tre efter Task 5)
- Modifiera: `docs/guide-facts-gemini.md` (två nya poster, G33–G34)

Spec §3 pekar ut den här passagen som **det ställe rutan ska stå**: den är huvudflödets egen juridikpassage, den bär redan en svagare föregångare till rutan på rad 977 ("Readers outside the EU should verify…"), och den läses av dem som hoppar över bonuskapitlet.

Fyra stycken, fyra olika utfall:

| rad | innehåll | utfall |
|---|---|---|
| 972 | `<h4>Data residency, GDPR, and national context</h4>` | **rubriken byts** — GDPR ut ur den |
| 973 | var data lagras och behandlas (NotebookLM Enterprise EU-residens, Workspace-versionens residens) | **stannar** — produktfakta, post G13, skrivs om bara om Task 4 gav `fel` eller `obelagt` |
| 975 | "Standard GDPR discipline applies… Article 6(1)(e)… Article 9… Article 30 records of processing" | **går** — artikelnivå-GDPR, spec §3 |
| 977 | "Readers outside the EU should verify the privacy framework… (UK, Switzerland, FERPA, APPI)" | **ersätts av rutan** — det är föregångaren |
| 979 | "National supervisory authorities. Every EU member state has one… (Sweden is a notable example)" | **går** — namngiven tillsynsstruktur plus G29:s Sverige-exempel |

- [ ] **Steg 1: Byt rubriken**

```html
  <h4>Data residency, and what depends on where you are</h4>
```

- [ ] **Steg 2: Ersätt rad 975–979 med rutan**

Tre stycken blir ett inledande stycke plus guidens **befintliga** `callout callout--watch`-komponent (sex förekomster i print redan — ingen ny stil). Ordalydelsen är avgjord och står här ordagrant; den är Copilot-rutan i sak, med samma tre kategorier och utan en enda namngiven lag eller myndighet:

```html
  <p>What none of that settles is which rules you have to satisfy. Where your data is stored and processed is a product fact, and your agreement and the Admin console will tell you what it is for your domain. Which data-protection regime governs that processing, and what it asks you to write down, is set by where your school operates — not by the product. The box below names the three things to check locally.</p>

  <div class="callout callout--watch">
    <span class="callout__label">What depends on where you are</span>
    <p>Three things here are set where you work, not by the product. <strong>Your data-protection regime</strong> decides what lawful basis you need before processing student data, and what you must document. <strong>Your rules on student age and consent</strong> decide who may use Gemini and NotebookLM at all, and who signs for it — Google's own age floors are a minimum, not a permission slip. <strong>Your school's procurement and approval route</strong> decides who signs the agreement and who must be consulted first. <strong>What does not depend on where you are:</strong> your school remains the data controller for its students' data, and using Gemini or NotebookLM does not transfer that responsibility to Google. Check the three above locally before you rely on any specific rule in this part.</p>
  </div>
```

**"Data controller" är tillåtet** som allmän yrkesterm — det är inte en hänvisning till en namngiven förordning, och gränsen är ärvd ordagrant från Copilot-rundan.

- [ ] **Steg 3: Samma ändring på webbytan**

```bash
grep -n "Data residency, GDPR, and national context" _unpublished/guides/gemini-notebook/index.html
```
Webbytans fyra stycken har **samma ordalydelse** som printytans (verifierat 2026-10-12: rad 484–491 mot 972–979), **utom** att rad 491 saknar Sverige-parentesen som printytans 979 bär — det är G29. Rutan skrivs in med samma markup; webbytan använder samma `callout callout--watch`-komponent (`grep -c "callout--watch"` ger 26 träffar på hela sidan).

- [ ] **Steg 4: Kontrollera att inget artikelnivå-GDPR står kvar i passagen**

```bash
for f in _unpublished/exports/gemini-notebook-print-a4-en.html \
         _unpublished/guides/gemini-notebook/index.html; do
  echo "=== $f"
  grep -nE "Article 6\(1\)|Article 9 |Article 30|supervisory|data protection authority" "$f" | cut -c1-120
done
```
Förväntat: inga träffar i Del 4:s passage. Träffar i **bonuskapitlet** är kvar här och tas i Task 7 — läs radnumret innan du drar slutsatsen.

- [ ] **Steg 5: Del 3:s två GDPR-förekomster — luckan förflygsskanningen hittade**

**Spec §3 räknar tre GDPR-ställen utanför bonuskapitlet (print 972–979, 541, 1357). Det är fem.** Mätt i worktreen 2026-10-12: `grep -c "Article 30"` ger **4** och `grep -c "national data protection authority"` ger **3** i printytan, alltså fler än passagen ovan rymmer. De två specen missade står i **Del 3**, och ingen annan uppgift äger dem:

| rad | står i dag | utfall |
|---|---|---|
| EP 921 / EW 430 | "Update the school's records of processing (GDPR, a European regulation — Article 30) to reflect the new tools." | **artikelnivån går, rådet stannar.** Meningen gör något för läsaren — den säger att dokumentationen ska uppdateras när verktygen ändras — och det är jurisdiktionsneutralt. Skriv om så att den säger *vad* som ska uppdateras (skolans egen förteckning över vilka personuppgifter verktygen behandlar) utan att namnge förordning eller artikel. |
| EP 934 / EW 443 | "You are personally carrying GDPR risk that belongs with your organisation." | **regelverksnamnet går, varningen stannar.** "a data-protection risk that belongs with your organisation" bär samma skärpa utan rättslig analys. Hela stycket är ett av guidens viktigaste råd (konsumentkonton i skolarbete) och får inte tappa kraft. |

Båda får **egna poster** i inventeringen (`G33`, `G34`) med typ `regelverk` och motiveringen utskriven — de finns inte i Task 3:s kända lista, eftersom den byggdes på specens treställsräkning.

- [ ] **Steg 6: Commit**

```bash
git add _unpublished/exports/gemini-notebook-print-a4-en.html \
        _unpublished/guides/gemini-notebook/index.html
git commit -m "content(gemini): jurisdiktionsrutan ersätter huvudflödets GDPR-passage, Del 3:s två artikelled bort"
```

---

## Task 7: Bonuskapitlet — AI Act kvar och rättad, GDPR på artikelnivå ut, skylten skärpt

**Filer:**
- Modifiera: `_unpublished/exports/gemini-notebook-print-a4-en.html` (rad 540–541, 1015–1016, 1018–1025, 1028–1029, 1037–1052, 1061–1064, 1081)
- Modifiera: `_unpublished/guides/gemini-notebook/index.html` (rad 529–539, 542, 551–566, brödtexten, 596)
- Modifiera: `scripts/tests/test_guide_toc.py` (en nyckel i `GUIDE_TOC["gemini"]["anchors"]` och en i `XFAIL_UNTIL_RECOUNTED`)

Rundans tyngsta uppgift. Kapitlet behåller sin plats och sin överhoppbarhet; det är dess **innehåll** som ändras på tre sätt.

**FÄLLA, läs först.** Kapitlets TOC-ankare är `"If you teach or lead a school in an EU member state"` och det står i den ingress som skrivs om i steg 2. **Ledet bevaras ordagrant.** Byts det ut kan TOC-vakten inte hitta kapitlets startsida, och felmeddelandet blir "ankaret står inte på någon sida", vilket läser som ett vaktfel i stället för ett innehållsfel (granskningsfokus 3).

- [ ] **Steg 1: Skärp skylten — rubriken och förteckningens rad**

Spec §3: rubriken ska säga vad kapitlet faktiskt täcker, så att en läsare utanför EU inte tror sig missa dataskyddsvägledning som inte längre står där.

EP rad 540–541 (förteckningen):
```html
      <span class="toc__title">Bonus Chapter · The EU AI Act for schools
        <span class="toc__sub">Article 4, the four risk tiers, the dates that bind, compliance checklist</span>
      </span>
```

EP rad 1015 och EW rad 529 (kapitelrubriken; `<span class="eyebrow">Bonus Chapter</span>` står kvar oförändrad):
```html
  <h2>The EU AI Act for schools</h2>
```

**I samma commit:** byt nyckeln i `scripts/tests/test_guide_toc.py` på två ställen, från `"Bonus Chapter · For EU readers"` till `"Bonus Chapter · The EU AI Act for schools"` — en gång i `GUIDE_TOC["gemini"]["anchors"]` och en gång i `XFAIL_UNTIL_RECOUNTED`. Ankarsträngen (värdet) ändras **inte**. Görs det i en senare commit är `test_the_toc_has_the_rows_we_think_it_has` röd däremellan.

- [ ] **Steg 2: Skriv om ingressen, med ankarledet intakt**

EP 1016 / EW 530:
```html
  <p class="lede">If you teach or lead a school in an EU member state, one regulation shapes how you use Gemini and NotebookLM more than any other: the EU AI Act. This chapter is a practical primer — not legal advice.</p>
```

- [ ] **Steg 3: Ta bort GDPR-avsnittet**

EP rad 1018 (`<h3>GDPR fundamentals for schools using AI</h3>`) och de sju styckena 1019–1025 går i sin helhet, samt deras motsvarighet på webbytan (EW 532–539). Styckena bär: data controller/processor-förhållandet och DPA:n, Article 6(1)(e), dataminimering, Article 30, dataresidensen, "your country's national data protection authority", och den praktiska regeln om skoldomänkonto.

**Två av dem är inte bara juridik, och de får inte försvinna med badvattnet:**
- **Dataresidensen** (EP 1023) är produktfakta och står redan i huvudflödet på EP 973 (post G13, Task 6 lät den stanna). Samma påstående, två formuleringar — det försvinner alltså inte ur guiden, det slutar stå två gånger.
- **Den praktiska regeln** (EP 1025: "use only the school-domain Workspace account for anything touching student data… never put student-identifiable content into a consumer account") är ett **handlingsråd utan rättslig analys** och har ingen motsvarighet någon annanstans i guiden. Den **flyttas** till slutet av steg 2:s ingress eller till checklistan i EP 1066 — den stryks inte. Ett råd som inte namnger en lag faller inte under spec §3.

  **MEN: stycket flyttas utan sin sista mening.** EP 1025 slutar *"If your school routinely uses Gemini or NotebookLM, your records of processing should reflect that."* Den meningen bär G33:s term, som Task 6 tar bort ur Del 3 och Task 12 gör till en förbudsrad — flyttas den med skrivs termen tillbaka och vaktblocket blir rött. Dokumentationsrådet finns dessutom redan kvar i Del 3 efter Task 6:s omskrivning, så ingenting går förlorat. **Två meningar flyttas, tre finns i stycket.**

**Checklistan bär samma term en tredje gång.** EP 1072 / motsvarande rad på webbytan: *"Our records of processing (Article 30) reflect routine AI use across our school"*. Den punkten namnger en GDPR-artikel och går enligt steg 6 — men den räknas här, så att den inte blir en överraskning när vaktblocket läses in i Task 12.

- [ ] **Steg 4: Rätta AI Act-datumen mot P13**

EP 1028 och EW 542. Posten är G25; den publicerade `exports/claude-print-a4-en.html` rad 1269 bär samma fakta i Claude-guidens röst, och de två guiderna ska inte säga olika saker om samma förordning:

```html
  <p>The EU AI Act entered into force on 1 August 2024 and became applicable on 2 August 2026. It classifies AI use by risk level and attaches obligations to each level. Education is explicitly in scope.</p>
```

EP 1029 bär **ett fjärde fel som specen inte räknat**: *"On 2 August 2026, general applicability begins, transparency rules apply, and most high-risk obligations take effect."* P13 belägger att **bara** transparensskyldigheterna gäller sedan dess — bilaga III-högrisken, där utbildning uttryckligen ingår, är genom AI-omnibusen framflyttad till **2 december 2027**, och produktinbyggd högrisk till 2 augusti 2028. Meningen ska alltså säga att de två dateringarna 2025 och 2026 gäller, och att högriskfristen för utbildning ligger 2027. **Skriv den i Gemini-guidens egen röst, med G25:s och G27:s värden** — kopiera inte Claude-guidens mening ordagrant, de två guiderna delar fakta, inte formulering. Lägg till en rad i inventeringen för den här meningen om Task 3 inte redan gav den en.

- [ ] **Steg 5: Rätta risknivåernas fyra namn, på fyra ställen per yta**

Post G26, belagd i P13, och redan levererad i Claude-guiden (rad 1276–1306):

| gammalt | nytt |
|---|---|
| `Minimal risk` | `Minimal or no risk` |
| `Limited risk` | `Transparency risk` |
| `High risk` | `High risk` (oförändrat) |
| `Prohibited` | `Unacceptable risk` |

Ställena: EP 1037, 1042, 1047, 1052 (pyramidens `<text>`-element) och 1061–1064 (brödtextens fyra `<strong>`-led); EW 551, 556, 561, 566 och brödtextens motsvarighet. **Pyramiden är en SVG med fasta `x`/`y`** — `Unacceptable risk` är längre än `Prohibited` och `Transparency risk` längre än `Limited risk`. Kontrollera i steg 7 att ingen etikett går utanför sin `<rect>`; Claude-guidens pyramid bär samma namn i samma bredd, så måttet är redan prövat en gång, men **inte i den här SVG:ns geometri** (Geminis `viewBox` är `0 0 680 320`, Claudes en annan).

De fyra brödtextstyckena bär också **innehåll** som måste följa namnet: 1062 handlar om transparens och passar `Transparency risk` som den står; 1064 säger "banned outright", vilket passar `Unacceptable risk`. Byt leden, inte argumenten.

- [ ] **Steg 6: Ta bort kapitlets GDPR-rester**

EP 1081 / EW 596 (friskrivningen): *"Make sure the checklist harmonises with your own school's interpretation of the GDPR and the EU AI Act"* → GDPR-ledet ut, AI Act kvar. **"Readers outside the EU should verify the data-protection and AI-governance frameworks that apply in their own country"** i samma stycke stannar — det namnger ingenting och är samma sorts hänvisning som rutan i Task 6.

Checklistan (EP 1066 och framåt) och dess punkter läses igenom: varje punkt som namnger en GDPR-artikel går, varje punkt som rör Article 4 eller risknivåer stannar.

- [ ] **Steg 6B: Ta in de två skolnära AI Act-punkterna som saknas**

**Johans beslut vid grinden:** kapitlet listar i dag AI Act-datum men nämner inget av de nio förbuden utom social scoring. Två saker som rör skolan direkt saknas, och de tas in — båda belagda i P13, ingen ny källdomän:

1. **`emotion recognition in education institutions` är ett av de nio förbuden.** Det hör i stycket om den översta nivån (EP ~1064, det som efter steg 5 heter `Unacceptable risk`), intill social scoring.
2. **Kommissionen räknar uttryckligen AI som avgör tillträde till utbildning som högrisk** — "AI solutions used in education institutions, that may determine the access to education … (e.g. scoring of exams)". Det hör i högriskstycket (EP ~1063), som i dag ger exempel men inte säger att kommissionen namnger utbildning explicit.

**Förbud 9 om nudification-appar tas INTE in** — Johans beslut. Det träder i kraft i december 2026 och är relevant för en skolledare som skriver AI-policy, men det rör inte Gemini eller Gemini Notebook, och kapitlet ska stanna vid vad som gäller guidens egna verktyg. **Skriv inte in det "för fullständighetens skull".**

- [ ] **Steg 7: Kontrollera kapitlet**

```bash
EP=_unpublished/exports/gemini-notebook-print-a4-en.html
sed -n '1010,1100p' $EP | grep -nE "GDPR|Article [0-9]|supervisory|Limited risk|Minimal risk|Prohibited|phases in"
```
Förväntat: **inga träffar**. Den enda GDPR-förekomsten som får stå kvar i hela printytan efter den här uppgiften är promptmallens platshållare på rad ~1357 (post G30, spec §3) — kontrollera med `grep -c GDPR $EP`, som ska ge **1**.

- [ ] **Steg 8: Kör TOC-vakten och commit**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_guide_toc.py -v`
Förväntat: oförändrat utfall — 13 passed, 8 xfailed. **Ett FAIL på `test_the_toc_has_the_rows_we_think_it_has[gemini]` betyder att nyckeln i steg 1 inte byttes i samma commit.**

```bash
git add _unpublished/exports/gemini-notebook-print-a4-en.html \
        _unpublished/guides/gemini-notebook/index.html \
        scripts/tests/test_guide_toc.py
git commit -m "content(gemini): bonuskapitlet behåller AI Act, rättad mot P13, och tappar artikelnivå-GDPR"
```

---

## Task 8: Den svenska inramningen — två jurisdiktionsexempel går, ett praktikexempel stannar

**Filer:**
- Modifiera: `_unpublished/exports/gemini-notebook-print-a4-en.html` (rad 831, 1031)
- Modifiera: `_unpublished/guides/gemini-notebook/index.html` (rad 333, 545)

Efter Task 6 och 7 står tre svenska förekomster kvar, och de har tre olika utfall. **Johans beslut vid grinden 2026-10-12: praktikexemplet STANNAR.** Det är alltså avgjort, inte ett antagande — och det är skälet att `Sweden` och `Swedish` aldrig kan bli bara strängar i leveransvaktens lista eller i vaktblocket.

**Källan är kontrollerad och håller** (Task 4, G21): `pedagog.eskilstuna.se` svarade 200, är daterad 4 februari 2026, och bär varje led ordagrant — "Viktor Säfström", "David Folkebrant", "Fristadsskolan", "1–2 minuter", "amhariska", "Google Classroom". **En enda detalj står inte i källan:** halvsatsen "for **newly-arrived** students". Artikeln säger att elever *vill ha* amhariska eller arabiska varianter; ordet nyanländ förekommer inte. **Den halvsatsen skrivs om, och det är inte valfritt.**

| post | förekomst | utfall |
|---|---|---|
| G28 | EP 1031 / EW 545: "Sweden, as of April 2026, is among the countries that have *not* yet issued detailed national guidance — which makes the EU AI Act the dominant framework for Swedish schools" | **går** — jurisdiktionsexempel, och dessutom en datering som Task 4 inte kan belägga mot en namngiven källa |
| G22 | EP 831 / EW 333: "Output in languages beyond English — including Swedish and other EU languages — works well as of April 2026" | **generaliseras** — språkstödet är produktfakta, det namngivna språket är inramning |
| G21 | EP 831, 896 / EW 333, 405: Säfström och Folkebrant, Fristadsskolan i Eskilstuna, Pedagog Eskilstuna | **stannar**, med posten och motiveringen utskriven |

- [ ] **Steg 1: Skriv om G28:s mening utan Sverige**

Argumentet i meningen — att Aktens betydelse varierar med om landet publicerat egen vägledning — är jurisdiktionsneutralt och **stannar**. Det som går är exemplet och dateringen. Meningen behåller alltså sin första och sina två sista satser och tappar den mittersta. Formuleringen är fri; den får inte namnge ett land och den får inte bära ett datum som ingen källa belägger.

- [ ] **Steg 2: Generalisera G22**

Språkstödet stannar som påstående, exemplet blir språkneutralt: "languages beyond English" utan uppräkning. **Dateringen "as of April 2026" i samma mening** hör till G09/G22 och avgörs av Task 4:s utfall — gav källan inget datum går datumet, och meningen säger att kvaliteten varierar per språk och att man ska testa först, vilket den redan gör.

- [ ] **Steg 3: Låt G21 stå, och skriv motiveringen i inventeringen**

Ingen ändring i texten. I posten skrivs ut: att exemplet är **källbelagt** (Pedagog Eskilstuna, februari 2026), att det är guidens enda namngivna klassrumsexempel på 42 sidor, att spec §9 uttryckligen tillåter "ett medvetet, motiverat exempel med en post i inventeringen", och att **det är därför leveransvaktens lista för den här guiden inte kan innehålla ett bart `Sweden`** (granskningsfokus 1). En läsare som undrar varför Copilot-guiden förbjuder ordet och Gemini-guiden inte gör det ska hitta svaret i posten, inte i en commit-text.

- [ ] **Steg 4: Räkna om**

```bash
for f in _unpublished/exports/gemini-notebook-print-a4-en.html \
         _unpublished/guides/gemini-notebook/index.html \
         _unpublished/exports/gemini-notebook-quick-start-en.html; do
  printf "%-62s Sweden:%s Swedish:%s\n" "$f" \
    "$(grep -o "Sweden" "$f" | wc -l | tr -d ' ')" \
    "$(grep -o "Swedish" "$f" | wc -l | tr -d ' ')"
done
```
Förväntat: EP `Sweden:2 Swedish:0`, EW `Sweden:2 Swedish:0`, QS `0 0`. De två `Sweden` är G21:s två förekomster per yta (Eskilstuna-exemplet står på två ställen). **Varje annan siffra är ett fynd:** fler betyder att en förekomst missades, färre att praktikexemplet skadades.

- [ ] **Steg 5: Commit**

```bash
git add _unpublished/exports/gemini-notebook-print-a4-en.html \
        _unpublished/guides/gemini-notebook/index.html
git commit -m "content(gemini): jurisdiktionsexemplen generaliserade, praktikexemplet står kvar med sin post"
git add -f docs/guide-facts-gemini.md
git commit -m "docs(gemini): G21:s motivering — varför ordet Sweden inte kan vara en förbudsrad här"
```

---

## Task 9: Produktnamn, dateringar och de tre asymmetrierna

**Filer:**
- Modifiera: `_unpublished/exports/gemini-notebook-print-a4-en.html`
- Modifiera: `_unpublished/guides/gemini-notebook/index.html`

Varje post vars utfall i Task 4 blev `fel` eller `obelagt` rättas här, på båda ytorna i samma commit. Inga nya faktavärden skrivs som inte står i inventeringen.

- [ ] **Steg 1: De två daterade produktpåståendena (G03)**

*"Since 8 April 2026 the two tools sync bidirectionally"* står på EP 610 och 640 och 847, och i odaterad form ("since April 2026") på 628, 719 och 1546 — plus motsvarigheterna på EW. **Ett datum i brödtext är ett påstående om när något hände; källan måste bära det eller så går datumet.** Tre utfall, ett av dem gäller:
- `stämmer` → datumet står kvar på alla förekomster, och de odaterade varianterna lämnas som de är.
- `fel: <datum>` → det rätta datumet skrivs in på **alla** förekomster, inte bara de två exakta.
- `obelagt` → datumet går ur alla förekomster; funktionen beskrivs utan "since". Funktionen i sig är inte i tvivel — den har en skärmbildsplatshållare på EW 354 som säger att integrationen rullas ut gradvis.

- [ ] **Steg 2: De tre asymmetrierna (G06, G09, G15)**

```bash
EP=_unpublished/exports/gemini-notebook-print-a4-en.html
EW=_unpublished/guides/gemini-notebook/index.html
for n in "Gems" "Audio Overview" "AI Ultra"; do
  echo "=== $n"
  diff <(grep -o ".\{90\}$n.\{90\}" $EP) <(grep -o ".\{90\}$n.\{90\}" $EW) | head -20
done
```
Läs varje skillnad och avgör: **formuleringsskillnad** (ingen åtgärd, en rad i "Observationer utanför posterna") eller **saklig divergens** (rättas på båda ytorna). En divergens i sak betyder att de två ytorna i dag säger olika saker om samma produkt — det är ett fynd i sin egen rätt och ska stå i överlämningen, inte bara lagas.

- [ ] **Steg 3: Licens-, funktions- och åldersposterna**

G05, G08, G10–G18 enligt sina utfall. Två regler:
- Ett `obelagt` värde skrivs om **utan siffra**, inte med en gissning. "Four formats" blir "several formats" om källan inte räknar dem; "added September 2025" går om ingen sida bär datumet.
- Ett namn Google har bytt skrivs om på **varje** förekomst. Antalen i Task 3:s tabell är hur många det är — en rättning som lämnar 23 av 24 är inte en rättning.

- [ ] **Steg 4: URL-posten (G19)**

Spec §2 har redan mätt att `choosewise.education/infographic-styles/` och `assets/pdfs/nlm-140-prompts-en.pdf` svarar **200**. Verifiera om, eftersom mätningen är fyra dagar gammal när uppgiften körs:
```bash
for u in https://choosewise.education/infographic-styles/ \
         https://choosewise.education/assets/pdfs/nlm-140-prompts-en.pdf; do
  echo "$(curl -s -o /dev/null -w '%{http_code}' "$u") $u"
done
```
Förväntat: 200 på båda. **Ett 404 är ett eget fynd**, inte något den här uppgiften lagar: det vore samma fel som Copilots quick-start hade, och det skulle gå till överlämningen och till Johan.

- [ ] **Steg 5: Kör sviten och commit**

Kör: `/usr/bin/python3 -m pytest scripts/tests/ -q --ignore=scripts/tests/test_prompt_pdf_parity.py`
Förväntat: oförändrat mot Task 5 — inget test läser ännu guidens sakinnehåll utom typsnittsvakten.

```bash
git add _unpublished/exports/gemini-notebook-print-a4-en.html \
        _unpublished/guides/gemini-notebook/index.html
git commit -m "content(gemini): produktnamn, licensnivåer och dateringar enligt inventeringen"
```

---

## Task 10: Avslutningen, CTA:n och Johans egen rad

**Filer:**
- Modifiera: `_unpublished/exports/gemini-notebook-print-a4-en.html` (rad 1611)
- Modifiera: `_unpublished/guides/gemini-notebook/index.html` (rad 1209)

Post G31 och G32, rättelse 4 i planens inledning. Meningen *"I have a full-time job and run this work alongside it, which means I can't always handle urgent or tight-turnaround queries"* är **inte längre sann**: Johan lämnade Advania i augusti 2026 och är sedan dess egen konsult (CLAUDE.md §1). Meningen står inte i Claude- eller Copilot-guidens engelska ytor — den är den här guidens egen.

- [ ] **Steg 1: Skriv om förväntansraden**

Det meningen **gör** för läsaren är att sätta en förväntan på svarstid, och den förväntningen gäller fortfarande — det är skälet den skrivs om och inte stryks. Den nya formuleringen får inte påstå något om Johans anställning. **Johans beslut 2026-10-12, inte längre ett antagande: raden SKA skrivas om.** Han läste planens rättelse 4 och svarade "ändra påståendet om mig som inte längre är sant". Formuleringen nedan är alltså godkänd i sak: raden säger att han driver det här arbetet vid sidan av uppdrag, och att tidskritiska frågor hör till skolans egen administration, DPO eller resurserna ovan — alltså samma styrning av läsaren, utan påståendet om en heltidstjänst. Förslag att utgå från, som Johan får byta ord i:

```html
      <p>For school-specific questions — AI policy, whole-school rollout, working-group design, EU AI Act implementation — you can also reach out through my website (link in the footer). A small note on expectations: this work runs alongside my consulting, so I cannot always take on urgent or tight-turnaround queries. For anything time-critical, start with your admin, your DPO, or the resources above.</p>
```

- [ ] **Steg 2: Kontrollera CTA:ns avsändare**

Guidens engelskspråkiga hatt är **choosewise.education** (CLAUDE.md §2). `grep -n "choosewise" EP` ska visa att omslaget, sidfoten och avslutningen pekar dit; meningen "reach out through my website (link in the footer)" är redan avsändarneutral och behöver bara stå kvar. **Guiden säljer inte Johans tid** — samma antagande som Copilot-rundan körde på, och det gäller till Johan säger annat.

- [ ] **Steg 3: Kontrollera och commit**

```bash
grep -c "full-time job" _unpublished/exports/gemini-notebook-print-a4-en.html \
                        _unpublished/guides/gemini-notebook/index.html
```
Förväntat: 0 på båda.

```bash
git add _unpublished/exports/gemini-notebook-print-a4-en.html \
        _unpublished/guides/gemini-notebook/index.html
git commit -m "content(gemini): förväntansraden utan påståendet om en heltidstjänst"
```

---

## Task 11: Quick-starten

**Filer:**
- Modifiera: `_unpublished/exports/gemini-notebook-quick-start-en.html` (bara om inventeringen pekar dit)

**Den här quick-starten är ren där Copilots var trasig.** Mätt 2026-10-12: noll förekomster av "Swedish", "Sweden", "GDPR", "April 2026", och dess enda utgående pekare är `choosewise.education / guides / gemini-notebooklm` (rad 319) plus `choosewise.education` i sidfoten — inte en 404 som Copilots. Uppgiften är därför liten, men den får inte hoppas över: QS bär **sex produktpåståenden** (Workspace for Education ×1, Deep Research ×1, Audio Overview ×4, Video Overview ×1) som delar post med huvudguidens.

- [ ] **Steg 1: Stäm av QS mot inventeringens utfall**

```bash
QS=_unpublished/exports/gemini-notebook-quick-start-en.html
grep -nE "Workspace for Education|Deep Research|Audio Overview|Video Overview|Gems|Canvas" $QS | cut -c1-140
```
Varje träff vars post fick `fel` eller `obelagt` i Task 4 rättas här, med **samma** värde som huvudguiden fick i Task 9. Ett värde som rättas i huvudguiden men inte i quick-starten är exakt det fel leveransvakten finns för att fånga.

- [ ] **Steg 2: Kontrollera pekaren**

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://choosewise.education/guides/gemini-notebooklm/
```
**Ett 404 här är väntat och korrekt** — guiden är opublicerad, och spec §1 säger att ingenting publiceras i den här rundan. Pekaren är alltså en adress som blir giltig när guiden publiceras, inte ett fel. Att den står kvar är ett medvetet val och det ska skrivas i överlämningen, så att nästa runda inte "lagar" den.

- [ ] **Steg 3: Commit (hoppas över om ingenting ändrades)**

```bash
git add _unpublished/exports/gemini-notebook-quick-start-en.html
git commit -m "content(gemini): quick-starten får huvudguidens rättade värden"
```
Ändrades ingenting: skriv i inventeringens "Observationer utanför posterna" att QS kontrollerades mot varje post och inte behövde någon ändring. **Ett fynd som inte behöver ändras stryks aldrig tyst.**

---

## Task 12: Vaktblocket — `gemini` in i ytkartan, varje rättning får sin rad

**Filer:**
- Modifiera: `scripts/tests/surfacecheck.py` (`GUIDE_SURFACES`)
- Modifiera: `scripts/tests/factinventory.py` (`INVENTORIES`)
- Modifiera: `scripts/tests/test_guide_surface_consistency.py` (ett test generaliseras)
- Modifiera: `docs/guide-facts-gemini.md` (vaktblocket)

**Allt i den här uppgiften hör till samma commit.** `test_every_guides_guard_block_is_not_empty` kräver både `aktiv`- och `borttaget`-rader för varje guide i ytkartan, så en ifylld ytkarta utan vaktrader är röd — och tvärtom har vaktrader utan ytkarta ingen vakt som läser dem. Det är skälet planen väntat med båda till nu (se Globala villkor).

- [ ] **Steg 1: Lägg `gemini` i de två kartorna**

```python
# scripts/tests/surfacecheck.py — en ny nyckel i GUIDE_SURFACES
    # Gemini/NotebookLM ligger under _unpublished/ av samma skäl som
    # Copilot: GitHub Pages serverar inte kataloger som börjar med
    # understreck. De svenska ytorna står med i kartan fast rundan inte
    # rör dem — de FINNS, och en svensk vaktrad ska jämföras mot dem och
    # inte mot ingenting. Att de divergerar i sak från de engelska är ett
    # känt läge (spec §1), inte något vakten ska dölja.
    "gemini": {
        ("en", "web"):   "_unpublished/guides/gemini-notebook/index.html",
        ("en", "print"): "_unpublished/exports/gemini-notebook-print-a4-en.html",
        ("sv", "web"):   "_unpublished/sv/guider/gemini-notebooklm/index.html",
        ("sv", "print"): "_unpublished/exports/gemini-notebooklm-print-a4-sv.html",
    },
```

```python
# scripts/tests/factinventory.py — en ny rad i INVENTORIES
    "gemini":  ROOT / "docs" / "guide-facts-gemini.md",
```

- [ ] **Steg 2: Generalisera `_unpublished`-testet i stället för att kopiera det**

`test_copilot_surfaces_are_the_unpublished_ones` är guidespecifik. Två opublicerade guider nu, fyra när Apple och elevguiden kommer. Ersätt den med:

```python
# Guider vars fyra ytor ligger under _unpublished/, som Pages inte
# serverar. Claude är publicerad; de andra tre tas i sina egna rundor.
UNPUBLISHED_GUIDES = ("copilot", "gemini")


@pytest.mark.parametrize("guide", UNPUBLISHED_GUIDES)
def test_unpublished_guides_surfaces_are_under_unpublished(guide):
    """Granskningsfokus 5 i Copilot-rundan, nu för två guider: pekar
    kartan på `guides/<guide>/` läser vakten en fil som inte finns —
    eller en dag den fel."""
    rels = list(surfacecheck.surfaces_for(guide).values())
    assert len(rels) == 4
    assert all(rel.startswith("_unpublished/") for rel in rels), rels


def test_every_unpublished_guide_is_in_the_surface_map():
    """Listan ovan får inte glida ifrån ytkartan. En guide som läggs i
    kartan men inte här tappar sin sökvägsvakt tyst."""
    assert set(UNPUBLISHED_GUIDES) <= set(surfacecheck.GUIDES)
    assert "claude" not in UNPUBLISHED_GUIDES
```

Det kostar ett borttaget test-id (`test_copilot_surfaces_are_the_unpublished_ones`) och ger tre nya. Räkna det i Task 17:s id-jämförelse.

- [ ] **Steg 3: Skriv vaktraderna**

`aktiv` kräver att strängen står ordagrant på **båda** engelska guideytorna (EW + EP). `borttaget` kräver att den inte står på någon av dem. Formatet är `id | språk | värde | status`, fyra kolumner, `#` inleder kommentar.

```guard
# Engelska ytorna: EW `_unpublished/guides/gemini-notebook/index.html` (web)
# + EP `_unpublished/exports/gemini-notebook-print-a4-en.html` (print).
# QS står utanför vakten med avsikt (spec §5) och bevakas av
# scripts/tests/test_guide_delivery.py.
#
# INGEN BAR "April 2026"-RAD, och inget bart "Sweden"/"Swedish"/"GDPR".
# Sju meningar bär datumet som daterat PRODUKTpåstående (G03), ordet
# Sweden står i det källbelagda praktikexemplet (G21) och ordet GDPR i
# promptmallens platshållare (G30). En borttaget-rad på någon av de bara
# strängarna vore röd för innehåll rundan har beslutat att behålla.
# Stämplarna bevakas i stället av
# test_geminis_cover_and_closing_carry_the_rounds_date.
G01 | en | October 2026 | aktiv
G02 | en | Johan Lindström, April 2026 | borttaget
# G02 får ingen aktiv-rad: den nya signaturen står bara i PRINT
# (avslutningssidan) och har ingen motsvarighet på webbytan, så en
# aktiv-rad vore `saknas_på_en_yta` från första sekunden. Den bevakas av
# leveransvakten, som läser PDF:en.

# Task 6 — huvudflödets juridikpassage OCH Del 3:s två artikelled
G33 | en | a European regulation | borttaget
G33 | en | records of processing | borttaget
G34 | en | carrying GDPR risk | borttaget
G29 | en | Sweden is a notable example | borttaget
G23 | en | Data residency, GDPR, and national context | borttaget
G23 | en | Standard GDPR discipline | borttaget
G23 | en | Every EU member state has one | borttaget
G23 | en | Readers outside the EU should verify the privacy framework | borttaget
G23 | en | What depends on where you are | aktiv

# Task 7 — bonuskapitlet
G24 | en | GDPR fundamentals | borttaget
G24 | en | Article 6(1)(e) | borttaget
G24 | en | Article 30 | borttaget
G25 | en | phases in through 2026 and beyond | borttaget
G25 | en | became applicable on 2 August 2026 | aktiv
G26 | en | Limited risk | borttaget
G26 | en | Prohibited | borttaget
G26 | en | Transparency risk | aktiv
G26 | en | Minimal or no risk | aktiv
G26 | en | Unacceptable risk | aktiv

# Task 8 — inramningen
G22 | en | Swedish and other EU languages | borttaget
G28 | en | Swedish schools | borttaget
G28 | en | Sweden, as of April 2026 | borttaget
# G29 står under Task 6 ovan: dess mening ligger i den passage Task 6
# ersätter, inte i Task 8:s två jurisdiktionsexempel.
# G21: praktikexemplet STANNAR, och de två aktiv-raderna är det som
# hindrar ett senare städarsvep från att ta bort det utan att något
# blir rött. Motiveringen står i posten.
G21 | en | Fristadsskolan | aktiv
G21 | en | Pedagog Eskilstuna | aktiv

# Task 10
G31 | en | I have a full-time job | borttaget

# G30: promptmallens platshållare stannar (spec §3) — raden finns för
# att den inte ska städas bort av misstag.
G30 | en | your national school-governance law | aktiv
```

**Fyra fällor i just det här steget.**
1. En `aktiv`-rad vars sträng bara står på en yta ger `saknas_på_en_yta` — det betyder att Task 5–11 missade en yta, inte att raden ska skrivas om.
2. En `aktiv`-rad som inte står någonstans ger `finns_ingenstans` och är nästan alltid ett stavfel i vaktblocket.
3. **En sträng som med avsikt bara finns på en av ytorna kan aldrig bli en `aktiv`-rad** — avslutningens signatur och omslagets stämpel står bara i print. Sådant bevakas av leveransvakten.
4. `G26 | en | Prohibited | borttaget` är säker **tack vare** att `surfacecheck._TAG` slukar HTML-kommentarer: strängen står i dag tre gånger per yta, varav en i kommentaren `<!-- Prohibited -->`. Döp om kommentaren ändå i Task 7 — en kommentar som motsäger koden under sig är ett fynd i nästa granskning.

- [ ] **Steg 4: Kör vakten och läs varje problem**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -v`
Förväntat: PASS, **och ingen SKIPPED** — Geminis fyra parametriseringar ska nu köra på riktigt.

- [ ] **Steg 5: Bryt vakten med flit och se den bli röd**

```bash
cp _unpublished/exports/gemini-notebook-print-a4-en.html /tmp/gemini-print-backup.html
printf '<p>Standard GDPR discipline applies for EU schools.</p>\n' \
  >> _unpublished/exports/gemini-notebook-print-a4-en.html
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q 2>&1 | tail -20
cp /tmp/gemini-print-backup.html _unpublished/exports/gemini-notebook-print-a4-en.html
git diff --stat -- _unpublished/exports/gemini-notebook-print-a4-en.html
```
Förväntat: `G23 [en] återinfört` i utfallet, och efter återställningen en **tom** `git diff --stat`. **Blir vakten inte röd vaktar den ingenting** — då står strängen inte i vaktblocket, eller normaliseringen äter den. Återställningen sker med `cp` från kopian, aldrig med `git checkout --` på en katalog. Och brytningen är ett `<p>`-element med avsikt: en HTML-kommentar hade slukats av `_TAG` och gett ett falskt grönt.

- [ ] **Steg 6: Hela sviten och commit**

Kör: `/usr/bin/python3 -m pytest scripts/tests/ -q --ignore=scripts/tests/test_prompt_pdf_parity.py`
Förväntat: 0 skipped, 3 xfailed (leveransvaktens, kvar till Task 13) + 8 xfailed (TOC-vaktens, kvar till Task 14) = **11 xfailed**.

```bash
git add scripts/tests/surfacecheck.py scripts/tests/factinventory.py \
        scripts/tests/test_guide_surface_consistency.py
git add -f docs/guide-facts-gemini.md
git commit -m "test(gemini): ytkartan får sin guide, vaktblocket sina rader"
```

---

## Task 13: Rendera om de två engelska PDF:erna

**Filer:**
- Modifiera: `_unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf`, `_unpublished/assets/pdfs/guides/gemini-notebook-quick-start-en.pdf`
- Modifiera: `scripts/tests/test_guide_delivery.py` (de tre xfail-markeringarna tas bort)

**Båda byggarna renderar EN *och* SV.** Varken `exports/build-gemini-notebook-pdf.py` eller `exports/build-gemini-quickstart-pdf.py` tar ett språkargument, och de svenska källorna finns — så fyra filer skrivs och de två svenska måste återställas. De får inte ändras ens i `CreationDate`: spec §1 lämnar dem som de står, och en ändrad byte skulle kräva en facitomfångning rundan inte ska göra. Det är exakt det `test_the_swedish_gemini_pdfs_are_untouched_since_the_merge_base` finns för.

- [ ] **Steg 1: Kopiera undan de svenska PDF:erna**

```bash
# kör från repots rot — i den här rundan är det worktreen, inte huvudkopian
cp _unpublished/assets/pdfs/guides/gemini-notebooklm-guide-sv.pdf /tmp/gemini-guide-sv.pdf
cp _unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-sv.pdf /tmp/gemini-quick-start-sv.pdf
```

- [ ] **Steg 2: Rendera**

```bash
/usr/bin/python3 exports/build-gemini-notebook-pdf.py
/usr/bin/python3 exports/build-gemini-quickstart-pdf.py
```
Byggaren skriver ut sidantal och storlek per fil. **Utgångsläget är 42 sidor och 9,6 MB** för huvudguiden; Task 6–10 tar bort mer text än de lägger till, så 41 eller 42 sidor är väntat. **40 eller färre är ett fynd** — då har ett helt uppslag fallit bort, och det ska förstås innan uppgiften bockas.

- [ ] **Steg 3: Återställ de svenska, med `cp` från kopian**

```bash
cp /tmp/gemini-guide-sv.pdf _unpublished/assets/pdfs/guides/gemini-notebooklm-guide-sv.pdf
cp /tmp/gemini-quick-start-sv.pdf _unpublished/assets/pdfs/guides/gemini-notebooklm-quick-start-sv.pdf
git status --short -- _unpublished/assets/pdfs/
```
Förväntat: **exakt två ändrade filer**, `gemini-notebooklm-guide-en.pdf` och `gemini-notebooklm-quick-start-en.pdf`. Står en svensk fil som ändrad: återställningen misslyckades, gör om steget. Står någon annan PDF som ändrad: stanna.

- [ ] **Steg 4: Ta bort de tre xfail-markeringarna**

I `scripts/tests/test_guide_delivery.py`:
1. Töm `XFAIL_UNTIL_RERENDERED` till `set()` — behåll konstanten med en kommentar om att nästa guide fyller den igen, samma konvention som `RECAPTURED_THIS_ROUND`. Mängden innehåller efter Task 2 **ett** par, huvudguidens; quick-starten var grön från början.
2. Ta bort `@pytest.mark.xfail(...)`-raden över `test_geminis_cover_and_closing_carry_the_rounds_date`.

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_guide_delivery.py -v`
Förväntat: PASS, 12 tester, 0 xfailed (två markeringar tas bort: huvudguidens par och datumstämpeltestets dekorator). Är någon röd står en förbjuden sträng kvar i den renderade filen — felmeddelandet namnger vilken, och den ska lagas i HTML:en och renderas om, inte tas ur listan.

- [ ] **Steg 5: Räkna med fyra fel till, fram till Task 15**

Kör: `/usr/bin/python3 -m pytest scripts/tests/ -q --ignore=scripts/tests/test_prompt_pdf_parity.py`
Förväntat: **fyra fel** i `test_guide_pdf_parity.py` och `test_guide_pdf_body_text.py` — två nycklar i två facit. Det är **inneboende** (spec §8): man kan inte rendera om en PDF och behålla dess gamla fingeravtryck. De stängs i Task 15 och ingen annanstans. Är felen fler än fyra, eller rör de en annan nyckel än de två engelska Gemini-PDF:erna, är det ett fynd — läs vilken nyckel det är innan du går vidare.

- [ ] **Steg 6: Commit**

```bash
git add _unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf \
        _unpublished/assets/pdfs/guides/gemini-notebook-quick-start-en.pdf \
        scripts/tests/test_guide_delivery.py
git commit -m "build(gemini): rendera om de två engelska PDF:erna ur det rättade innehållet"
```

---

## Task 14: Innehållsförteckningens tio sidnummer

**Filer:**
- Modifiera: `_unpublished/exports/gemini-notebook-print-a4-en.html` (rad 502, 509, 516, 523, 530, 537, 544, 551, 558, 565)
- Modifiera: `scripts/tests/test_guide_toc.py` (`XFAIL_UNTIL_RECOUNTED` töms)
- Modifiera: `_unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf` (renderas om)

Rundans mest läsarnära rättning. Åtta av tio nummer var fel före rundan, med en drift som växte från −1 till −4, och efter Task 6–10 har sidorna dessutom flyttat sig igen. **Numren räknas mot den PDF Task 13 renderade, aldrig mot markupen.**

- [ ] **Steg 1: Verifiera om alla tio ankare mot den nya utskriften**

```bash
/usr/bin/python3 - <<'PY'
import sys
sys.path.insert(0, "scripts")
from tests import pdf_fingerprint as fp, surfacecheck as sc
from tests.test_guide_toc import GUIDE_TOC, toc_rows
cfg = GUIDE_TOC["gemini"]
pages = [sc.normalise(p) for p in fp.pages(fp.extract(fp.ROOT / cfg["pdf"]))]
claimed = dict(toc_rows("gemini"))
for title, anchor in cfg["anchors"].items():
    a = sc.normalise(anchor)
    hits = [i + 1 for i, p in enumerate(pages) if i + 1 > cfg["toc_page"] and a in p]
    print(f"{'OK ' if hits else 'SAKNAS'} {title:<42} säger {claimed[title]:>3}  börjar {hits[:3]}")
PY
```
Förväntat: `OK` på alla tio, och en första träff per rad. **`SAKNAS` på bonuskapitlet betyder att Task 7 inte bevarade ankarledet** — laga ingressen, rendera om, kör om. **`SAKNAS` på något annat** betyder att en rubrik eller ett stycke rundan skrev om bar ankaret; välj ett nytt ankare **ur den här utskriften**, inte ur HTML:en, och skriv in det i kartan med en kommentar om varför det byttes.

- [ ] **Steg 2: Skriv in de tio numren**

Varje `<span class="toc__page">N</span>` sätts till den sida steg 1 skrev ut. Rör inget annat på raderna.

- [ ] **Steg 3: Töm xfail-mängden och se vakten bli grön**

```python
# scripts/tests/test_guide_toc.py
# Töms i slutet av varje runda som rättat sin förtecknings nummer.
# En mängd som bara växer slutar vakta något — samma konvention som
# RECAPTURED_THIS_ROUND i test_capture_guide_baseline.py.
XFAIL_UNTIL_RECOUNTED: set = set()
```

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_guide_toc.py -v`
Förväntat: 21 passed, **0 xfailed, 0 xpassed**.

- [ ] **Steg 4: Se vakten bli röd på ett av de åtta felen**

Fälla i spec §8: en vakt som inte setts bli röd vaktar ingenting. Åtta nummer var fel; bryt ett av dem och se exakt den parametriseringen falla.

```bash
cp _unpublished/exports/gemini-notebook-print-a4-en.html /tmp/gemini-toc-backup.html
/usr/bin/python3 - <<'PY'
from pathlib import Path
p = Path("_unpublished/exports/gemini-notebook-print-a4-en.html")
lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
i = 543  # rad 544, bonuskapitlets toc__page — kontrollera numret först
assert "toc__page" in lines[i], lines[i]
lines[i] = lines[i].replace(">2", ">9")
p.write_text("".join(lines), encoding="utf-8")
PY
/usr/bin/python3 -m pytest scripts/tests/test_guide_toc.py -q 2>&1 | tail -12
cp /tmp/gemini-toc-backup.html _unpublished/exports/gemini-notebook-print-a4-en.html
git diff --stat -- _unpublished/exports/gemini-notebook-print-a4-en.html
```
Förväntat: ett FAIL av formen `gemini 'Bonus Chapter · The EU AI Act for schools': förteckningen säger 9…, avsnittet börjar på N`, och efter återställningen tom `git diff --stat`.

- [ ] **Steg 5: Rendera om och återställ de svenska igen**

Samma cp-undan-och-tillbaka som Task 13 — numren står i PDF:en, så den måste renderas om.

```bash
cp _unpublished/assets/pdfs/guides/gemini-notebooklm-guide-sv.pdf /tmp/gemini-guide-sv.pdf
/usr/bin/python3 exports/build-gemini-notebook-pdf.py
cp /tmp/gemini-guide-sv.pdf _unpublished/assets/pdfs/guides/gemini-notebooklm-guide-sv.pdf
git status --short -- _unpublished/assets/pdfs/
```
Förväntat: en ändrad fil, `gemini-notebooklm-guide-en.pdf`. **Kör sedan TOC-vakten en gång till** — numren kontrolleras mot den omrenderade filen, och ett sidnummer som ändrades av själva numrets textbredd (tiotal → ental kan korta en rad) fångas bara där.

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_guide_toc.py scripts/tests/test_guide_delivery.py -v`
Förväntat: PASS på båda, 0 xfailed.

- [ ] **Steg 6: Commit**

```bash
git add _unpublished/exports/gemini-notebook-print-a4-en.html \
        scripts/tests/test_guide_toc.py \
        _unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf
git commit -m "fix(gemini): innehållsförteckningens tio sidnummer, nu vaktade mot PDF:en"
```

---

## Task 15: Selektiv fixturomfångning

**Filer:**
- Modifiera: `scripts/tests/fixtures/guide-pdf-baseline.json`, `scripts/tests/fixtures/guide-pdf-body-baseline.json`
- Modifiera: `scripts/tests/test_capture_guide_baseline.py` (`RECAPTURED_THIS_ROUND`)

- [ ] **Steg 1: Töm och fyll om `RECAPTURED_THIS_ROUND`**

Copilots nycklar kommer ut och Geminis två in. Listan ska aldrig växa radvis; en lista som bara växer slutar vakta något, och konventionen står i en kommentar ovanför konstanten sedan förra rundan. **Liten rättelse till spec §7:** den säger "Copilots fyra kommer ut" — det är **två**, `copilot-guide-en.pdf` och `copilot-quick-start-en.pdf`. Copilot-rundan renderade bara sina två engelska filer, precis som den här gör.

```python
RECAPTURED_THIS_ROUND = [
    "_unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf",
    "_unpublished/assets/pdfs/guides/gemini-notebook-quick-start-en.pdf",
]
```

- [ ] **Steg 2: Omfånga bara de två**

```bash
/usr/bin/python3 scripts/tests/fixtures/capture_guide_baseline.py \
  --only _unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf \
  --only _unpublished/assets/pdfs/guides/gemini-notebook-quick-start-en.pdf
```

**`--force` får inte användas.** Det är liktydigt med att slå av paritetsvakten för alla 22 PDF:er (spec §8).

- [ ] **Steg 3: Verifiera att diffen rör exakt två nycklar**

```bash
/usr/bin/python3 - <<'PY'
import json, subprocess
for f in ("guide-pdf-baseline.json", "guide-pdf-body-baseline.json"):
    rel = f"scripts/tests/fixtures/{f}"
    before = json.loads(subprocess.run(["git", "show", f"HEAD:{rel}"],
        capture_output=True, text=True, check=True).stdout)
    after = json.loads(open(rel, encoding="utf-8").read())
    changed = sorted(k for k in after if before.get(k) != after[k])
    print(f"{f}: {len(changed)} ändrade nycklar")
    for k in changed:
        print("   ", k)
    assert sorted(before) == sorted(after), "nyckeluppsättningen ändrades"
    assert len(changed) == 2, "exakt två nycklar ska ha ändrats"
    assert all("gemini-notebooklm-" in k and k.endswith("-en.pdf") for k in changed)
PY
```
Förväntat: två ändrade nycklar per fil. **Har en svensk Gemini-nyckel ändrats återställdes inte SV-filerna i Task 13 eller 14** — stanna och gå tillbaka dit.

- [ ] **Steg 4: Kör paritets- och innehållsvakterna före commit**

Kör: `/usr/bin/python3 -m pytest scripts/tests/test_guide_pdf_parity.py scripts/tests/test_guide_pdf_body_text.py scripts/tests/test_capture_guide_baseline.py -v`
Förväntat: PASS. `test_force_cannot_silently_reset_unrelated_entries` jämför mot `git merge-base main HEAD` — kör den **före** commit, inte efter.

- [ ] **Steg 5: Commit**

```bash
git add scripts/tests/fixtures/guide-pdf-baseline.json \
        scripts/tests/fixtures/guide-pdf-body-baseline.json \
        scripts/tests/test_capture_guide_baseline.py
git commit -m "test(gemini): omfånga facit för de två engelska PDF:erna, de tjugo andra orörda"
```

---

## Task 16: Titta på dokumentet — åtta bilder och 42 sidor

**Filer:** inga, om granskningen inte hittar något. Hittar den något rättas det i den fil som äger felet och PDF:en renderas om som i Task 13.

Spec §8.6 och §8.7. Copilot-rundans slutgranskning hittade elva fynd i ett pass på en 25-sidig guide; den här är 42 sidor med åtta bilder mot Copilots tre.

- [ ] **Steg 1: Rendera sidbilder och titta på varje sida där text ändrats**

```bash
mkdir -p /tmp/gemini-pages
pdftoppm -png -r 110 \
  _unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf \
  /tmp/gemini-pages/p
ls /tmp/gemini-pages/ | wc -l
```
Sidorna rundan rörde: omslaget (1), förteckningen (2), Del 4 (22–24, jurisdiktionsrutan), bonuskapitlet (25–27, inklusive risknivåpyramiden), stilbiblioteket (28–29) och avslutningen (41–42). **Öppna varje bild och titta** — ingen av vakterna ser layout.

- [ ] **Steg 2: Kontrollera pyramidens fyra etiketter**

Task 7 bytte `Prohibited` → `Unacceptable risk` och `Limited risk` → `Transparency risk` i en SVG med fasta `x`/`y`. Titta på sidan med pyramiden: ingen etikett får gå utanför sin `<rect>`, och ingen får kollidera med den högerställda texten på samma rad (`text-anchor="end"` på `x="590"`). Går den utanför är rättningen att korta etiketten i **båda** riktningarna — namnen är belagda i P13 och kan inte ändras, men `font-size` på just de två `<text>`-elementen kan.

- [ ] **Steg 3: Kontrollera jurisdiktionsrutan och sidbrytningarna**

Rutan är ny text i en `callout--watch`. Kontrollera att den inte bryter över en sidgräns mitt i sin bakgrundsfärg, och att stycket före den inte blev ensamt kvar på föregående sida. Samma kontroll på bonuskapitlet, där tre stycken och ett helt avsnitt försvann.

- [ ] **Steg 4: Kontrollera de åtta stilbilderna**

De åtta `<img>`-raderna (EP 1099–1155) ligger alla i stilbiblioteket och rundan ändrade ingen av dem. Kontrollera ändå att alla åtta **renderas** — en bild som tystnar ger en tom ruta i PDF:en och ingen vakt läser bilder:
```bash
/usr/bin/python3 - <<'PY'
from pathlib import Path
import re
ep = Path("_unpublished/exports/gemini-notebook-print-a4-en.html").read_text(encoding="utf-8")
for src in re.findall(r'<img src="([^"]+)"', ep):
    p = (Path("_unpublished/exports") / src).resolve()
    print(("OK  " if p.is_file() else "SAKNAS"), src)
PY
```
Förväntat: OK på alla åtta.

- [ ] **Steg 5: Läs PDF:en från pärm till pärm**

```bash
pdftotext -layout _unpublished/assets/pdfs/guides/gemini-notebook-guide-en.pdf - | less
```
Det som letas efter är sådant ingen vakt kan se: en mening som tappat sitt subjekt när mitten ströks, en korsreferens till ett avsnitt som bytt namn ("the Bonus Chapter on GDPR"), en uppräkning som säger "three things" och räknar två, och ett stycke som nu säger samma sak två gånger eftersom dubbletten i bonuskapitlet togs bort.

```bash
grep -nE "Bonus Chapter|see (Part|the chapter)|as described (in|above)|below" \
  _unpublished/exports/gemini-notebook-print-a4-en.html | cut -c1-140
```
Varje korsreferens läses mot det den pekar på.

- [ ] **Steg 6: Commit, om något rättades**

Rättningar görs i HTML, PDF:en renderas om enligt Task 13:s steg, och facit omfångas om enligt Task 15. **Ett fynd som inte rättas skrivs i överlämningen** — det stryks aldrig tyst.

---

## Task 17: Slutkontroll, överlämning och PR

- [ ] **Steg 1: Hela sviten**

Kör: `/usr/bin/python3 -m pytest scripts/tests/ -q --ignore=scripts/tests/test_prompt_pdf_parity.py`
Förväntat: **0 skipped, 0 xfailed, 0 xpassed.** Står en skip kvar är ett vaktblock tomt; står en xfail kvar sitter en markering från Task 1, 2 eller 13 i.

Kör sedan utan `--ignore` och kontrollera att de **elva** felen i `test_prompt_pdf_parity.py` är exakt de elva som faller på `main` — inga fler, inga andra:
```bash
/usr/bin/python3 -m pytest scripts/tests/test_prompt_pdf_parity.py -q 2>&1 | tail -15
```

- [ ] **Steg 2: Jämför de insamlade test-id:na mot `main`**

```bash
WS=.superpowers/sdd/2026-10-12-gemini-guide-international
/usr/bin/python3 -m pytest scripts/tests/ -q --collect-only 2>/dev/null | grep "::" | sort > "$WS/ids-final.txt"
diff "$WS/ids-main.txt" "$WS/ids-final.txt"
```
Tillåtna förluster, och inga andra: de sju ur `test_copilot_toc.py` (Task 1), de tre ur `test_copilot_delivery.py` (Task 2) och `test_copilot_surfaces_are_the_unpublished_ones` (Task 12). Varje borttaget id ska ha en namngiven efterträdare.

- [ ] **Steg 3: Gå igenom specens §9 rad för rad**

```bash
# kör från repots rot — i den här rundan är det worktreen, inte huvudkopian
EP=_unpublished/exports/gemini-notebook-print-a4-en.html
EW=_unpublished/guides/gemini-notebook/index.html
QS=_unpublished/exports/gemini-notebook-quick-start-en.html

# Ingen namngiven myndighet, ingen artikelnivå-GDPR
grep -rncE "Skolverket|IMY|Schrems|Article 6\(1\)|Article 30|supervisory authorit|national data protection authority" $EP $EW $QS   # 0 på alla tre
# GDPR står kvar på exakt ett ställe per yta: promptmallens platshållare
grep -c "GDPR" $EP   # 1
grep -c "GDPR" $EW   # 1
# Sweden/Swedish bara i det källbelagda praktikexemplet
grep -o "Sweden" $EP | wc -l    # 2
grep -o "Swedish" $EP | wc -l   # 0
# AI Act kvar, med P13:s värden
grep -cE "became applicable on 2 August 2026" $EP            # minst 1
grep -cE "Transparency risk|Minimal or no risk|Unacceptable risk" $EP   # minst 3
grep -cE "Limited risk|phases in through 2026" $EP           # 0
# Stämplarna
grep -nE "cover__attr|closing__signature" $EP | grep -c "October 2026"  # 2
# Webbsidan fri från Google Fonts och Crestiora-typsnitten
grep -rncE "fonts\.googleapis|fonts\.gstatic|Playfair|'Inter'|font-family=\"Inter" \
  $EW _unpublished/guides/gemini-notebook/styles.css       # 0 på båda
# Två PDF:er ändrade, inga fler
git diff --name-only origin/main...HEAD -- '*.pdf' | wc -l   # 2
# Johans filer orörda
git diff --name-only origin/main...HEAD | grep -cE '^(exports/wise|exports/ratt|assets/pdfs/wise)'   # 0
# Svenska Gemini-ytor orörda
git diff --name-only origin/main...HEAD | grep -cE 'gemini.*-sv|sv/guider/gemini'                    # 0
# Inget publiceringssteg smugit in
git diff --name-only origin/main...HEAD | grep -cE 'guides-en\.json|sitemap\.xml|PAIR_MAP|build-seo-meta'  # 0
# Namnbytet: inga EN-filer med det gamla prefixet kvar
git ls-files | grep -c 'gemini-notebooklm.*-en\|guides/gemini-notebooklm/'   # 0
# De svenska filnamnen ÄR kvar, med avsikt (deras innehåll säger ännu NotebookLM)
git ls-files | grep -c 'gemini-notebooklm'                                    # 14
# NotebookLM står bara i citerat material — jämför mot Task 4C:s överlevandelista
grep -c "NotebookLM" $EP $EW $QS
```

- [ ] **Steg 4: Kontrollera att varje post bär källa och datum**

```bash
grep -cE "^\| G[0-9][0-9] " docs/guide-facts-gemini.md
grep -E "^\| G[0-9][0-9] " docs/guide-facts-gemini.md | grep -cE "2026-10-|korsref P13"
```
Förväntat: samma tal två gånger — varje post bär antingen ett hämtdatum i oktober 2026 eller en korsreferens till P13. Är det andra talet lägre står en post utan belägg, och då är dess mening skriven utan källa.

- [ ] **Steg 5: Uppdatera överlämningen**

`docs/blueprint-handoff.md`:
- Flytta Gemini-raden i statustabellen från "SPEC GODKÄND, inget byggt" till sitt nya läge, med PR-nummer, grennamn och sifferutfallet ur sviten.
- Stryk punkt 3b i "Nästa steg" och skriv in vad rundan levererade.
- **Vaktlagret** är nu guide-agnostiskt i fyra lager, inte två: ytvakten och inventeringen sedan Copilot-rundan, **TOC-vakten (`test_guide_toc.py`) och leveransvakten (`test_guide_delivery.py`) sedan den här**. Nästa guide fyller fyra kartor och skriver en inventering; den behöver inte ändra någon vakt. Skriv ut de fyra namnen och vad var och en kräver.
- **Två nya konventioner** som nästa runda ska följa: `XFAIL_UNTIL_RECOUNTED` och `XFAIL_UNTIL_RERENDERED` töms i slutet av varje runda, precis som `RECAPTURED_THIS_ROUND`, och `test_fonts.GUIDE_WEB_SURFACES` fylls med en guide när dess webbyta städats.
- **Det svenska divergensläget** som ett känt läge, inte något att upptäcka senare: `_unpublished/exports/gemini-notebooklm-print-a4-sv.html`, `gemini-notebooklm-quick-start-sv.html` och `_unpublished/sv/guider/gemini-notebooklm/` står kvar med aprilfakta och svensk inramning, deras PDF:er är byte-identiska, och de två språken divergerar nu i sak. Lägg Gemini till den befintliga punkten om Copilots svenska ytor — frågan är densamma för båda.
- **Namnbytet och dess kvarvarande skuld.** Google döpte om NotebookLM till **Gemini Notebook** 2026-07-16 (post G49). Rundan bytte namn i de engelska ytornas prosa, i titeln, i den tryckta URL:en och i **filnamnen** — Johans beslut 2026-10-12. Skriv ut: (a) att de **svenska** filnamnen med avsikt behåller `gemini-notebooklm-*`, eftersom deras innehåll fortfarande säger NotebookLM och ett namnbyte där hade gjort filnamnet osant; (b) att namnbytet lämnar **en sammanhållen skuld till publiceringsrundan, på två ställen**: `scripts/build-seo-meta.py` rad 51, 57 och 75 (rad 75 är PAIR_MAP, som spec §1 förbjuder rundan att röra) och `_unpublished/README.md` rad 26, 59, 63 och 148 — publiceringsrunbookens engelska block, vars **källsökväg på rad 26 nu är bruten** eftersom filerna flyttat. **Varför den inte lagades här:** rad 26 går inte att rätta ensam utan att runbooken blir osammanhängande ("flytta `gemini-notebook` till `guides/gemini-notebooklm`"), och att rätta hela blocket betyder att välja guidens **publicerade** sökväg och id — vilket är precis vad PAIR_MAP äger och spec §1 reserverar. De två filerna är i dag **överens** med varandra; en halv rättning hade gjort dem oense. Skulden är alltså ett jobb, inte två: publiceringsrundan byter destinationssökvägen på båda ställena plus i `guides-en.json` samtidigt. De svenska raderna (32, 96, 100) är fortfarande riktiga och ska inte röras; (c) att `NotebookLM` aldrig kan bli en förbudsrad i den här guiden, eftersom citaten bär ordet legitimt, och att vakten därför vaktar Task 4C:s uppräknade överlevande förekomster i stället.
- **Grindens tre beslut**, så att nästa guide vet att de togs och av vem: namnbytets omfång, att det svenska praktikexemplet stannar, och att bonuskapitlet tar in emotion recognition och examinationshögrisken men inte förbud 9.
- **Tre kända luckor** som rundan inte stänger och som ska stå utskrivna: (1) Claude-guidens femton TOC-nummer står ovaktade — `test_guide_toc.py` tar inte in dem, och varför står i filens docstring. (2) `_unpublished/guides/apple-intelligence/` och `_unpublished/guides/ai-for-students/` bär fortfarande Crestioras typsnitt, inklusive inline-attribut i SVG. (3) Quick-startens pekare till `choosewise.education/guides/gemini-notebooklm/` svarar 404 så länge guiden är opublicerad — medvetet, inte missat.
- **Rättelserna till specen** (planens fem) så att nästa guide mäter på rätt saker: inline-`font-family` i SVG, P13-korsreferensens verkliga omfång, praktikexemplet som skäl att inte dela förbudslistor, ett påstående om Johans anställning, och asymmetrier mellan de två engelska ytorna.

- [ ] **Steg 6: Commit och öppna PR**

```bash
git add -f docs/blueprint-handoff.md docs/superpowers/plans/2026-10-12-gemini-guide-international.md
git commit -m "docs(gemini): uppdatera överlämningen efter Gemini-rundan"
git push -u origin feat/gemini-guide-international
```

PR-texten säger: vad som levereras (två engelska PDF:er till Skool, ingenting publicerat), vilken väg som valdes och varför AI Act fick stanna, de fyra AI Act-värden P13 rättade, vad vaktlagret nu äger och vad nästa guide slipper bygga, det svenska divergensläget, de tre kända luckorna, och sifferutfallet ur sviten.

**PR #39 (specen) mergas före eller tillsammans med den här** — planen argumenterar från specen, och en mergad plan utan mergad spec lämnar en hängande korsreferens.

---

## Vad som gör rundan klar

Specens §9, med planens tillägg:

- [ ] Båda engelska PDF:erna byggda ur rättat innehåll, med Blueprint-layout.
- [ ] Inget "Sweden" eller "Swedish" kvar i de engelska ytorna annat än i det källbelagda Fristadsskolan-exemplet, som har en post och en utskriven motivering.
- [ ] GDPR på artikelnivå borta; den enda GDPR-förekomsten per yta är promptmallens platshållare.
- [ ] AI Act kvar, korsrefererad till P13, och **rättad på fyra punkter**: ikraftträdandeformuleringen, högriskfristen, och två av de fyra risknivånamnen.
- [ ] Bonuskapitlets skylt säger vad kapitlet täcker, både i rubriken och i förteckningen.
- [ ] Jurisdiktionsrutan står i huvudflödet, i guidens befintliga callout-komponent, utan namngiven lag eller myndighet.
- [ ] Varje volatilt påstående har en post i `docs/guide-facts-gemini.md` med källa och datum, eller en korsreferens till P13.
- [ ] Ytkonsistensvakten grön för Claude, Copilot och Gemini, utan skip.
- [ ] TOC-vakten guide-agnostisk, grön för båda guiderna, och sedd röd på minst ett av de åtta felaktiga numren.
- [ ] Leveransvakten guide-agnostisk med en förbudslista per guide, och sedd röd innan PDF:erna renderades om.
- [ ] De svenska PDF:erna byte-identiska mot bascommiten, och vakten som säger det har setts bli röd.
- [ ] Webbytan fri från Google Fonts, från Crestiora-typsnitten och från de sjutton inline-attributen — med en vakt som ser dem.
- [ ] PDF-facit omfångat med `--only`, de tjugo andra nycklarna orörda.
- [ ] Dokumentet granskat som dokument: åtta bilder, pyramidens nya etiketter, jurisdiktionsrutans sidbrytning, och en genomläsning pärm till pärm.
- [ ] Produktnamnet är `Gemini Notebook` i guidens egen röst på alla tre engelska ytorna, i titeln, i den tryckta URL:en och i filnamnen — och `NotebookLM` står kvar enbart i citerat material, uppräknat post för post.
- [ ] Bonuskapitlet nämner emotion recognition i utbildningsinstitutioner och kommissionens egen högriskformulering om tillträde till utbildning. Förbud 9 står inte där.
- [ ] Fristadsskolan-exemplet står kvar, med källa, och utan påståendet om nyanlända elever.
- [ ] Det svenska divergensläget, namnbytets kvarvarande skuld i `build-seo-meta.py` och de tre kända luckorna skrivna i överlämningen.
