# Våg 2b — Claude-guidens innehåll

**Datum:** 2026-10-08
**Status:** spec, väntar granskning
**Hör till:** Blueprint-programmet. Överordnad spec: `2026-10-05-choosewise-visual-identity-design.md` §8, steg 2b.
**Omfattar:** Claude-guiden, EN + SV. De fyra opublicerade guiderna följer i egna rundor på samma mönster.

---

## 1. Varför

Guiden skrevs i april 2026 och bär det datumet på fyra ställen. Den beskriver planer, priser, modellnamn och gränssnitt som har rört sig sedan dess. Den ligger publicerad på sajten i två språk och ska ligga som nedladdning i Skool — alltså läses den av någon som registrerat sig, och den är ett av få ställen där sajtens och communityts formspråk möts i samma dokument. Ett felaktigt pris i ett medlemsvärde är dyrare än ett felaktigt pris i en annons.

Våg 2a gav guiderna en gemensam tryckmall och lämnade innehållet orört med avsikt. Den här rundan tar innehållet.

## 2. Vad som ska vara sant när vi är klara

1. Varje volatilt faktapåstående i guiden är kontrollerat mot en namngiven källa med datum, eller omskrivet så att det inte längre hänger på ett faktum vi inte kan belägga.
2. De fyra ytorna säger samma sak. Inget påstående är rättat på tre ställen av fyra.
3. Det som tillkommit sedan april 2026 och som en lärare faktiskt behöver finns i guiden.
4. Den svenska texten läses som svenska. Inga anglicismer, inga genusfel ur engelskan, ingen översatt rytm.
5. Guiden är andra upplagan, oktober 2026, på varje ställe som bär upplaga eller datum.
6. Alla fyra PDF:er är omrenderade, och fixturerna är omfångade för exakt de fyra — inte för de övriga arton.
7. Ett femte vaktlager påstår att webbytan och printytan är överens.

## 3. Ytorna

Varje faktapåstående i Claude-guiden finns på fyra ställen. De är inte speglar: av 435 meningar är 260 identiska mellan webb och print, resten har egen formulering per yta. Varje yta redigeras på sina egna villkor.

| Yta | Fil | Ord |
|---|---|---|
| EN webb | `guides/claude/index.html` | 8 726 |
| SV webb | `sv/guider/claude/index.html` | 8 642 |
| EN print → PDF | `exports/claude-print-a4-en.html` | 10 800 |
| SV print → PDF | `exports/claude-print-a4-sv.html` | 10 662 |

`build-claude-pdf.py` renderar ur print-filen, inte ur webbsidan. Ingen av våg 2a:s fyra vakter ser skillnaden mellan de två ytorna.

**Följeslagare som bär datum eller lättare fakta:**

| Fil | Vad den bär |
|---|---|
| `exports/claude-quick-start-{en,sv}.html` | inga pris- eller modellpåståenden; påståenden om inloggning och gratiskonto |
| `exports/claude-guide-license-{en,sv}.html` | "choosewise.education · April 2026" — upplagedatum |

**PDF:er som renderas om:** `assets/pdfs/guides/claude-guide-{en,sv}.pdf`, `assets/pdfs/guides/claude-quick-start-{en,sv}.pdf`.

### Rörs inte

De fyra opublicerade guiderna och deras fjorton PDF:er. Presentationsteknik-guiderna. Visual Codes. Diagram- och social-exporterna. `build-nlm-prompts-en.py` — den är trasig och är ett eget jobb. Sidstruktur, URL:er och navigation. Paletten och typografin, som är våg 1:s och 2a:s.

## 4. Angreppssätt: inventeringen som ryggrad

Arbetet hänger på en numrerad inventering av varje volatilt påstående, i `docs/guide-facts-claude.md`.

En post per påstående, med:

- **id** — löpnummer, så planen och commits kan hänvisa
- **påståendet** som det står idag
- **alla fyra förekomster** med fil och radnummer, och vilka av dem som har egen formulering
- **typ** — pris, nivå, modellnamn, funktionsnamn, gränssnitt, regelverk, konkurrent, datum, **härlett värde**
- **omfång** — gäller påståendet båda språken, eller bara ett? Ett pris i kronor är inte samma värde som ett pris i dollar
- **hur det avgörs** — officiell källa, eller "kräver inloggning"
- **källa och datum** när det är kontrollerat
- **utfall** — stämmer / ändrat till X / omskrivet / borttaget
- **bockat per yta**, fyra bockar

Inventeringen är tre saker på en gång: den källlogg specen §8 kräver, det enda som täpper fyrdubbleringen, och ett underlag som gör rundan återupptagbar över flera sessioner. Den blir också mallen för de fyra guider som följer.

**Ordningen är: inventera allt → kontrollera allt → redigera.** Inte påstående för påstående hela vägen. Skälet är att kontrollarbetet omfördelar sig självt — när Cowork visar sig ha ändrats faller flera andra poster ut som följdfrågor, och det vill man veta innan en enda rad är redigerad.

## 5. Faktakontrollens metod

Officiella källor: anthropic.com, prissidan, dokumentationen, supportartiklarna. Varje post får källa och kontrolldatum. Sekundärkällor duger inte för pris, nivå eller modellnamn.

**Det som bara syns inloggat** samlas i en egen kort lista i inventeringen, som Johan betar av — gärna med skärmbild. Guiden påstår saker om gränssnittet som ingen dokumentation svarar på: var en inställning ligger, vad gratisnivån faktiskt visar, om en funktion finns där guiden säger. Listan hålls kort och ställs som ja/nej-frågor, inte som utredningsuppdrag.

### Kronorna

Den svenska guiden prissätter i kronor — "ca 200 kr / mån", "ca 1 000 kr+ / mån" — och fotnoten säger att de är "omräknade från Anthropics dollarpriser". Svenska priser hänger alltså på två fakta: dollarpriset och kursen. Två poster i inventeringen, inte en.

Om Anthropic numera säljer i kronor till ett satt pris är dessutom hela ramen fel, inte bara siffran, och fotnoten ska skrivas om. Det avgörs som en egen post innan prisposterna rättas.

Ett påstående som varken dokumentation eller Johan kan belägga skrivs om så att det inte längre hänger på faktumet, eller tas bort. Det gissas inte.

### Cowork-grinden

Cowork har 24 omnämnanden och två egna sektioner, och beskrivs som "agentic mode inside Claude Desktop (paid)". **Cowork kontrolleras först av allt, före resten av inventeringen.** Har namnet, ytan eller nivåplaceringen ändrats väsentligt är det inte en rättning utan en omskrivning av två sektioner i fyra filer — och då går omfånget tillbaka till Johan innan planen skrivs. Posten är alltså en grind, inte en rad.

## 6. Det svenska språkpasset

Hela den svenska guiden granskas, inte bara de stycken som ändras av faktaskäl. Ribban är CLAUDE.md §3: skulle en svensk skolchef märka att texten är översatt?

Belagt i nuläget, som exempel på vad som söks:

| Ställe | Felet |
|---|---|
| `sv/guider/claude/index.html:292` | "när det körs **inne i en**" — genusfel ur engelskans "inside one"; det ska vara *inne i ett* (ett Projekt). Samma rad: "kompetent-men-blekt", engelsk sammansättning. |
| `:748`, `:794` | "problemet policyn **adresserar**", "Policyn ska **adressera**" — anglicismen CLAUDE.md §3 tar som exempel, och båda står i promptbiblioteket, i text lärare kopierar. |
| `:62`, `:77`, `:292` | negativ parallellism tre gånger — översatt engelsk rytm och ett AI-tell. |

Passet är ett eget steg efter faktaredigeringen, inte invävt i den. Skälet: rytmfel syns bara när guiden läses som en sammanhängande svensk text, och det går inte att göra stycke för stycke mellan faktakontroller.

Promptbiblioteket prioriteras i passet. Det är den text som lämnar guiden och hamnar i någon annans chattfönster.

## 7. Andra upplagan

Upplagan blir **andra upplagan, oktober 2026**. Varje ställe som bär upplaga eller datum ändras:

Sex filer, fjorton förekomster. Quick start-filerna bär inget datum.

| Fil | Rad | Vad som står |
|---|---|---|
| `exports/claude-print-a4-en.html` | 690 | "Edition: First edition, April 2026" |
| | 701 | "Pricing and features are accurate as of April 2026" |
| | 848 | "Pricing accurate as of April 2026" |
| | 1577 | "First edition · April 2026 · © Johan Lindström" |
| `exports/claude-print-a4-sv.html` | — | motsvarande fyra |
| `guides/claude/index.html` | 159 | "Pricing accurate as of April 2026" |
| | 1057 | "Updated April 2026." |
| `sv/guider/claude/index.html` | 159 | "Priserna stämmer per april 2026 och är omräknade från Anthropics dollarpriser" |
| | 1057 | "Uppdaterad april 2026." |
| `exports/claude-guide-license-en.html` | — | "choosewise.education · April 2026" |
| `exports/claude-guide-license-sv.html` | — | motsvarande |

Datumet sätts en gång, i inventeringen, och alla förekomster hänvisar till den posten. Det får inte stå tre olika månader i samma dokument.

## 8. Det femte vaktlagret

Våg 2a:s fyra lager vaktar varje PDF mot den HTML den byggdes ur. Ingen vaktar webbytan mot printytan. Ett pris rättat på webben men inte i print ger en guide som motsäger sig själv mellan sajt och nedladdning, tyst, och ingen befintlig vakt blir röd.

Leveransen innehåller därför `scripts/tests/test_guide_surface_consistency.py`.

**Konsistensen är per språk.** EN webb mot EN print, SV webb mot SV print. Inte mellan språken — den svenska guiden prissätter i kronor med avsikt, och en vakt som krävde samma värde över språkgränsen vore röd från första dagen.

**Testet läser inventeringen som indata**, så det inte blir en andra lista att hålla i synk. Det kräver ett maskinläsbart format, och ett markdown-dokument som parsas på fri text är sprött. Inventeringen bär därför ett avgränsat kodblock med en rad per bevakat värde, i ett fast format: `id | språk | det exakta värdet`. Resten av inventeringen är prosa och tabeller för människor; blocket är det enda testet läser, och det ligger i samma fil som allt annat.

Vakten byggs mot de volatila påståendena, inte mot hela texten. Ytorna skiljer sig 40 % i formulering med avsikt, och en vakt som krävde ordagrann likhet skulle vara röd från första dagen och alltså värdelös.

**Vakten ska bevisas kunna fallera.** Ändra ett pris på en yta och se testet bli rött innan det litas på. Det är fälla 2 i överlämningen.

## 9. Fixturerna

`scripts/tests/fixtures/capture_guide_baseline.py` fångar alla 22 PDF:er i en dict och vägrar skriva över utan `--force`. Dess egen docstring säger varför: en omkörning med `--force` efter en ändring *är* att slå av paritetsvakten.

Våg 2b rör fyra av de 22 nycklarna. Körs `--force` omfångas tyst även de fjorton opublicerade och de fyra presentationsteknik-PDF:erna, och paritetsvakten slutar betyda något för arton filer som den här rundan inte ens öppnat.

**Leveransen innehåller därför selektiv omfångning:** `capture_guide_baseline.py` får ett `--only <sökväg>`-argument som skriver om enbart de angivna nycklarna och lämnar resten orörda. Efter omfångningen verifieras att diffen på `guide-pdf-baseline.json` och `guide-pdf-body-baseline.json` rör exakt de fyra Claude-nycklarna och inget annat.

## 10. Sekvens och gren

2b måste stå ovanpå 2a — den behöver den delade `_guide-print.css`. PR #30 är inte mergad.

| Steg | Grind |
|---|---|
| Spec, inventering, hela faktakontrollen, Johans inloggade lista | görs nu. **Ingen av guidens ytor rörs** — inventeringen är en ny fil under `docs/` och kan inte konflikta med PR #30 |
| Redigering av de fyra ytorna och följeslagarna | **släpps först när Johan mergat PR #30** |
| Omrendering, fixturer, femte vakten | efter redigeringen |

Kontrollarbetet är den långa delen, så grinden kostar ingen väntetid. Grenen tas från `feat/blueprint-wave-2a-guides` när grinden öppnas, eller från `main` om #30 redan är inne.

## 11. Fällor som ärvs från programmet

Dessa är inte nya — de står i `docs/blueprint-handoff.md` och gäller här.

1. **`git add -A` används aldrig.** Johan har ~26 ocommittade filer under `exports/` och `assets/pdfs/wise/` som är hans eget attributionssvep. Två av filerna som ändras i den här rundan ligger i `exports/`, alltså i samma katalog som hans arbete. Namnge varje fil.
2. **`git checkout --` på en katalog raderar andras ocommittade arbete.** Det hände i våg 2a och kostade två av Johans filer. Kopiera undan och återställ med `cp`.
3. **Tio av 22 PDF:er är inte byte-identiska vid omrendering** — Chromiums `CreationDate`/`ModDate`. `git status` visar alltid ändrade filer efter en körning även när innehållet är idempotent.
4. **`build-seo-meta.py` bumpar "Last updated" ur commitdatum.** Här är det korrekt — innehållet har faktiskt ändrats — men kör det medvetet och kontrollera att inga andra sidor fick nytt datum.
5. **Generatorer äger sina filer.** Lägg ingen ändring i en fil som skrivs av ett skript.
6. **`/usr/bin/python3` (3.9.6) är enda interpretern** med pytest, playwright och Pillow.
7. **En kontrastsiffra härledd ur deklarerad CSS är inte bevisad.** Gäller inte den här rundan direkt, men om en textändring tvingar en stilrättning: pixelmät i den renderade filen.

## 12. Verifiering

| Påstående | Hur det bevisas |
|---|---|
| Varje volatilt påstående är kontrollerat | Varje post i `docs/guide-facts-claude.md` har källa och datum, eller är märkt omskrivet/borttaget |
| De fyra ytorna är överens | `test_guide_surface_consistency.py` grön, och bevisad kunna bli röd |
| Inget innehåll har försvunnit | Våg 2a:s dokumentnivåinvariant, `test_guide_pdf_body_text.py` |
| Fixturerna rör bara Claude | Diffen på de två baseline-filerna rör exakt fyra nycklar |
| Svenskan håller | Hela svenska guiden läst i ett svep mot CLAUDE.md §3; de fem belagda ställena i §6 åtgärdade |
| Upplagan är konsekvent | `grep` på "April 2026", "april 2026" och "First edition" i de sex filerna ger noll träffar; fjorton förekomster ändrade |
| PDF:erna är byggda ur det nya innehållet | De fyra PDF:erna omrenderade, övriga arton orörda i `git status` |

## 13. Öppna beslut

- **Johans röst i den svenska texten.** Specen binder svenskan till CLAUDE.md §3:s kvalitetsribba — naturlig professionell svenska. Om Johan dessutom vill att guiden ska bära hans personliga röst enligt `voice`-skillen, eller köras genom `voice-humanizer`, är det ett eget val han får göra. CLAUDE.md §7 säger att `voice-humanizer` bara aktiveras på uttrycklig begäran, så den körs inte av sig själv.
- **Konkurrentpåståendet om ChatGPT.** Guiden påstår att Projects är enklare än custom GPTs. Ett konkurrentpåstående åldras snabbare än allt annat i guiden och är svårast att belägga med en källa som håller. Frågan är om det ska beläggas eller skrivas om till något som inte är en jämförelse. Avgörs som en post i inventeringen, men flaggas här eftersom svaret är en bedömning och inte ett faktum.
- **Om Cowork har ändrats väsentligt** går omfånget tillbaka till Johan enligt §5. Det är inte ett beslut som kan tas i förväg.

## 14. Dokument

- Överordnad spec: `docs/superpowers/specs/2026-10-05-choosewise-visual-identity-design.md` §8
- Våg 2a:s plan: `docs/superpowers/plans/2026-10-05-visual-identity-wave-2a-guides.md`
- Programmets överlämning: `docs/blueprint-handoff.md`
- Inventeringen som den här rundan bygger: `docs/guide-facts-claude.md`
