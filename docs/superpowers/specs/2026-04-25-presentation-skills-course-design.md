# Presentationsteknik — interaktiv kurs design

**Status:** Approved via chat brainstorming 2026-04-25
**Tool target:** Johan's Swedish ed-tech consulting site (choosewise.education)
**Language sequence:** SV-kurs → SV-PDF → EN-kurs → EN-PDF

---

## Thesis

En interaktiv online-kurs i presentationsteknik som flyttar Johans befintliga halvdagsworkshop från Keynote till webben. Kursen är **pedagogiskt uppbyggd** — moduler bygger på varandra — men varje del fungerar fristående så besökaren kan hoppa direkt in. Huvudmålgrupp är **lärare, rektorer och annan skolpersonal**, men kursen ska kännas relevant och attraktiv även för andra som håller presentationer (säljare, ledare, talare). Exempel balanserar därför skolscenarier med bredare scenarier.

Kursens roll i Johans positionering: en gratis, högkvalitativ resurs som visar Johans pedagogiska tyngd och drar in skolpersonal till resten av sajten. Den är inte en intäktsprodukt — den är en demonstration av kompetens som öppnar dörren för konsultuppdrag och föredrag.

## Placering & filstruktur

- **SV-kurs:**
  - `sv/presentationsteknik/index.html` — översiktsvy (grid)
  - `sv/presentationsteknik/modul-1/index.html` — Varför presentationsteknik?
  - `sv/presentationsteknik/modul-2/index.html` — Designa diabilder — grunderna
  - `sv/presentationsteknik/modul-2/fordjupning/index.html`
  - `sv/presentationsteknik/modul-3/index.html` — När diabilden krockar med dig
  - `sv/presentationsteknik/modul-3/fordjupning/index.html`
  - `sv/presentationsteknik/modul-4/index.html` — Framförandet — närvaro i rummet
  - `sv/presentationsteknik/modul-4/fordjupning/index.html`
  - `sv/presentationsteknik/modul-5/index.html` — Digitala presentationer
  - `sv/presentationsteknik/modul-5/fordjupning/index.html`
  - `sv/presentationsteknik/modul-6/index.html` — Röst, kropp och språk
  - `sv/presentationsteknik/modul-6/fordjupning/index.html`
  - `sv/presentationsteknik/modul-7/index.html` — Din checklista
- **EN-kurs (steg 3):**
  - `presentation-skills/index.html` (placeholdern ersätts)
  - `presentation-skills/module-1/index.html` ... `module-7/index.html`
  - `presentation-skills/module-N/deep-dive/index.html` (för 2–6)
- **PDF-källor (steg 2 och 4):**
  - `exports/presentation-skills/sv/handout.html` → `assets/pdfs/presentationsteknik-sammanfattning.pdf`
  - `exports/presentation-skills/en/handout.html` → `assets/pdfs/presentation-skills-summary.pdf`
- **Slide-bilder (käll-tillgångar):**
  - `assets/images/presentation-skills/slides/` — utvalda slide-PNGs från Johans Keynote (ca 25–40 st)
- **Sitemap:** uppdatera `sitemap.xml` med alla nya URL:er när de produceras

## Modulstruktur (7 moduler, ~58 min totalt)

### Modul 1 — Varför presentationsteknik? *(~5 min, ingen fördjupning)*

- Definition: konst, skicklighet, hantverk → praktisk tillämpning
- Memory-övning: tänk på ett möte 4–8 veckor sedan — vad minns du?
- Sineks Golden Circle introduceras
- Logik vs känslor — vad driver beslut?
- **Övning:** Skriv ditt varför (textarea, sparas i localStorage)
- **Slides används:** intro-illustration (slide 1, omdesignad utan Advania-branding) + Sineks cirkel

### Modul 2 — Designa diabilder, grunderna *(~10 min, fördjupning ja)*

- Ett budskap per slide
- Max 6 objekt per slide (Gestalt: prickar-övning, slide 40)
- Färg och kontrast (slides 64–84: de fyra kontrastexemplen)
- Typografi: serif vs sans-serif, storlek, hierarki
- Använd färg för att styra blicken (slide 199)
- **Övning:** Klicka för att avslöja "fel slide → rätt slide" (reveal-on-click)
- **Slides används direkt:** kontrast-fyrling, "ett budskap"-progression, gestalt-prickar
- **Fördjupning:** Färgteori för presentatörer + typografi-djupare (best practice från web)

### Modul 3 — När diabilden krockar med dig *(~8 min, fördjupning ja)*

- Texttunga slides (läroplans-textmuren, slide 60)
- Punktlistans dilemma (apelsiner/citroner-slide)
- Tabeller — bra och dåliga (HP/Lenovo, slide 213)
- Komplexa/röriga slides
- Skippa mallarna
- Tvådiabildsprincipen
- Bildkvalitet (Tiger-exemplet)
- Animeringar
- **Övning:** Reflektera över din senast tex-tunga slide (textarea)
- **Slides används direkt:** läroplanstexten, punktlistorna, tabellerna, Tiger
- **Fördjupning:** 12 makeover-exempel (före/efter, från Johans erfarenhet och scrapad best practice)

### Modul 4 — Framförandet, närvaro i rummet *(~10 min, fördjupning ja)*

- Testa tekniken innan
- Belysning på, syns du?
- Stå upp
- Titta på publiken — inte slides
- "Öööööh…" — utfyllnadsljud
- Pauser — var inte rädd
- Interagera
- Undvik att läsa från slidet
- Props, blädderblock, whiteboard
- Berättelser
- **Övning:** "Räkna utfyllnadsljud" — 60 sek tystet ljudklipp av en presentatör (eller skärmtest), användaren räknar och jämför
- **Fördjupning:** Närvaro och scenrutiner — best practice från talartränare (web research)

### Modul 5 — Digitala presentationer *(~8 min, fördjupning ja)*

- Vad skiljer från fysiska? (i samma rum vs digitalt)
- Upplägg A vs B
- Fungerande teknik — testa innan
- Häng vid kaffemaskinen — digital ekvivalent
- Mötet börjar 9.10, inte 9.00
- Hälsa välkomna individuellt
- Digital ögonkontakt — kameran, inte skärmen
- Belysning, ståbord, händerna
- Pauser mellan möten
- Interaktion digitalt
- Berättelser i digitalt format
- **Övning:** Checklista "Ditt digitala presentationsrum" — kryssa av (sparas)
- **Fördjupning:** Kamera- och ljud-setup för kontorspresentation, plattformsspecifika tips (Teams, Zoom, Meet)

### Modul 6 — Röst, kropp och språk *(~12 min, fördjupning ja, stor)*

- Träningsmetafor: "Gör vi det inte på träning..." — du måste öva i kontrollerad miljö först
- Kort tur genom de fyra delområdena med 1–2 kärntekniker per område:
  - **Kropp:** sway (1), neutral position (34)
  - **Röst:** pauser (19+21), tempo (8–10)
  - **Ögon/ansikte:** ögonkontakt med publik (72)
  - **Språk:** trikolon (95)
- **Övning:** Spela in 30 sek av dig själv, lyssna på utfyllnadsljud (kameraåtkomst eller ljudfil-upload)
- **Fördjupning:** Vanliga svaga punkter — 19 kurerade tekniker (se nedan)

### Modul 7 — Din checklista *(~5 min, ingen fördjupning)*

- Sammanfattning: principer i en mening per modul
- Reflektion: "Vad är det första du ändrar inför nästa presentation?" (textarea)
- Ladda ner PDF
- Tipsa om relaterade resurser på sajten (RÄTT-modellen, AI-guider)

## Modul 6 fördjupning — kurerade tekniker

19 tekniker, valda som de vanligaste svaga punkterna. Varje teknik blir ett kort med titel, beskrivning, vanlig fallgrop, kort tip (~80–120 ord styck).

**Kropp (3):**
- 1. Gunga (sway) — undermedveten viktöverflyttning
- 4. Fidget — pillar på ringar, pennor, fickor
- 5. Flykt/frys — kaninen-i-strålkastarljus

**Röst (4):**
- 8–10. Tempo — talar för fort, behöver variera
- 19+21. Pauser — ofunktionella vs strategiska
- 25. Utfyllnadsljud — öh, ehm, liksom
- 28. Artikulation — sluddrar slutet av meningar

**Position & gester (3):**
- 34. Neutral position — saknar "hem"-position
- 44. Funktionella gester — slumpartade vs understrykande
- 66. Anchoring — vandrar planlöst

**Ögon & ansikte (3):**
- 72. Generell ögonkontakt — slides istället för publik
- 76. Neutralt ansiktsuttryck — frusen presentations-mask
- 83. Skratta åt sig själv — för allvarliga

**Språk & retorik (4):**
- 88. Onödiga utfyllnadsord — "lite", "kanske", "typ"
- 89. Negationer — "Jag ska inte tråka ut er..."
- 95. Trikolon — kraftfull treenighet, underutnyttjad
- 96. Repetition av ord — vågar inte upprepa

**Helhet (2):**
- 105. Intensitetsövergång — samma energinivå hela tiden
- 107. Närvarande och autentisk — läser från manus

## Övriga fördjupningar — innehållsstrategi

Modul 2–5 har vardera en fördjupning som inte primärt baseras på Johans Keynote — istället **scrapas best practice från webben** och presenteras kuraterat med Johans röst som kommentator. Förslagskällor per fördjupning:

- **Modul 2:** Smashing Magazine, Practical Typography, Material Design Color Theory, Adobe color/contrast guides
- **Modul 3:** Garr Reynolds (Presentation Zen), Edward Tufte (data presentation), McKinsey/HBR makeover-artiklar
- **Modul 4:** Toastmasters, Nancy Duarte, TED Speaker Coaching-artiklar
- **Modul 5:** Microsoft/Google/Zoom-officiella best practice-guider, plus uppdaterade artiklar om hybridmöten
- **Modul 6:** primärt Johans kuraterade lista (källan finns i Keynote)

Fördjupningstexter ska alltid skrivas i Johans röst (auktoritativ men varm, ifrågasättande), inte vara "scraped articles". Källor refereras tydligt när enskilda forskningsresultat citeras.

## Navigation & UX

### Översiktsvy (`/sv/presentationsteknik/`)

Grid med 7 modulkort (mockup A approved). Varje kort:
- Stort modulnummer (01–07)
- Statusbadge: Klar / Pågår / Ej startad
- Titel (Fraunces, 1.35rem)
- Kort beskrivning (1 mening, var-i-kursen-finns-jag)
- Fottfält med tid + fördjupningstagg
- Hover-effekt: lyfter, accent-border
- "Pågår"-kortet markeras med terrakotta-border

Ovanför griden: en kompakt progressionsstege med 7 numrerade cirklar (28px) + linjer mellan, klickbara, visar var användaren är.

### Sticky topbar på alla modulsidor

På varje modulsida + fördjupningssida finns en sticky topbar (under nav) med:
- **Vänster:** breadcrumb — "Kursöversikt · Modul N av 7"
- **Höger:** numrerad progressionsbar (24px cirklar, klickbara, koppling-linjer mellan)
- Samma färgkodning: forest green = klar, terrakotta = current, grå = ej startad
- På mobil (≤720px): linjerna döljs, cirklar krymps till 22px

Topbaren är tillgänglig (aria-current på current-modul, title-tooltip på alla cirklar).

### Fördjupningssidor

Egen URL: `/sv/presentationsteknik/modul-N/fordjupning/`. Använder samma sticky topbar (ärver modulens "current"-state). Lay-out som modul-sidor men mer utrymme för listor/galerier. "Tillbaka till modul"-länk längst upp.

### Föregående/nästa

Längst ner på varje modulsida: två-kolumns rutnät med föregående modul (vänster) och nästa modul (höger). På mobil staplas de.

## Modulsida-layout

Varje modul (`/sv/presentationsteknik/modul-N/`) har samma struktur (mockup C approved):

1. **Sticky topbar** (se ovan)
2. **Modulhero:** eyebrow ("Modul N · X min läsning") + h1 (modulrubrik) + lede (vad du lär dig)
3. **Innehållssektioner:** 3–6 sektioner per modul, varje med rubrik (h2), 1–4 stycken text, 0–3 slide-figurer, 0–1 interaktiv övning
4. **Slide-figurer:** används där bilden bär budskapet, med caption som anger källan (slide N från Keynote eller scrapad). Bilden är `<figure>` med `<figcaption>`.
5. **Övning:** distinkt sektion med vänster-kant accent, "ÖVNING · X min"-label, prompt, interaktion (textarea / klick / etc), spara-knapp. Sparar i localStorage.
6. **Fördjupnings-CTA** (om modulen har fördjupning): tydlig terrakotta-stilig länkblock i slutet, klick → separat fördjupningssida.
7. **Föregående/nästa-navigation**

## Slide-användning (hybrid B)

Cirka **25–40 av Johans 191 slides** används direkt i kursen som demonstrativa figurer. Kriteriet: **bilden bär budskapet** (kan inte rimligen skapas om i HTML).

**Slides som behålls (preliminär lista, justeras under bygge):**
- Modul 2: kontrast-fyrlingen (~slide 64–84), "ett budskap"-progression, gestalt-prickar (slide 40, 143), färgexempel (slide 199)
- Modul 3: läroplans-textmuren (slide 60), punktlist-jämförelser (slide 261–267), HP/Lenovo-tabeller (slide 200–225), Tiger-exemplet (slide 269–274), Covid-tabellen (slide 282)
- Modul 4: minst 2 illustrationer av "stå/sitta" och "blickkontakt"
- Modul 5: hybridmötes-uppställningar (slide om "i samma rum vs digitalt")
- Modul 6: positionsdiagram (kropp), ansikts-zonindelning (mun/ögon/panna)

**Slides som byggs om i HTML/CSS:**
- Slide 1 (cover): byggs om utan Advania-branding, choosewise-stil
- Övergångsslides (svarta): ersätts med pedagogisk pacing i HTML
- Bullet-tunga referensslides (110-tekniker-listan i del 2): native HTML, sökbar lista i fördjupning
- Citatslides: byggs om med Fraunces serif som citatblock

**Process att exportera slides:**
Johan exporterar nya slide-bilder utan Advania-branding (PNG, 1920×1080) eller jag skapar SVG-varianter där det är möjligt. Specifika slides som ska behållas listas i en Markdown-tabell när vi når implementation.

## Interaktivitet (nivå C)

Varje modul har **1–2 interaktiva element**. Inga quiz med rätt/fel. Allt sparas lokalt i webbläsaren (localStorage).

Typer:
- **Textarea-reflektion:** prompt + textfält + spara-knapp. Bevarar svar mellan sessioner. (Modul 1, 3, 7)
- **Reveal-on-click:** klick avslöjar nästa lager (rätt slide → fel slide → varför). (Modul 2)
- **Räkna-objekt:** användaren får 3–4 sek att titta på en slide, sedan frågas hur många objekt — instant feedback. (Modul 2, 4)
- **Checklista:** kryssa-av-frågor för "ditt digitala presentationsrum" eller "din nästa-presentation-checklista". (Modul 5, 7)
- **Inspelningsövning** (modul 6): user-medgivande för mikrofon, spela in 30 sek, spela upp, räkna utfyllnadsljud — eller, fallback: ladda upp ljudfil. **Privacy-by-default:** all bearbetning sker lokalt i webbläsaren (Web Audio API), ingen uppladdning sker.

## State (localStorage)

Alla användardata sparas i `localStorage` med namespace `presentationsteknik-sv-` (eller `-en-`). Inga konton, ingen server, ingen cookie:
- `presentationsteknik-sv-progress`: array av modulstatus `["done", "done", "current", "not-started", ...]`
- `presentationsteknik-sv-mod1-varfor`: textsvar från modul 1-övning
- `presentationsteknik-sv-mod3-textmur`: textsvar från modul 3-övning
- ... osv per modul

Återställ-funktion under "Din checklista" (modul 7): "Rensa mina svar".

## Tekniska val

- **Stack:** Plain HTML/CSS/JS (matchar resten av sajten)
- **CSS:** ny komponent `.course-progress` (sticky topbar) i `assets/css/components.css` så den kan delas mellan översiktsvy och modulsidor
- **JavaScript:**
  - `assets/js/course-progress.js` — synka progress mellan moduler, hantera "current"-markering
  - `assets/js/course-exercises.js` — generic textarea-reflektion (spara/ladda från localStorage)
  - `assets/js/course-recording.js` — Web Audio API-inspelning för modul 6
- **Bilder:** WebP där möjligt, JPG/PNG fallback för fotografi/screenshots, SVG för diagram. OG-bilder per modul-grupp (en för översikten, eventuellt en per modul om vi ser värdet).
- **Tillgänglighet:**
  - Sticky topbar med `aria-label="Kursprogression"`, `aria-current="page"` på current-modul
  - Alla interaktiva element tangentbordsnavigerbara
  - Reduced-motion respekteras (puls på "current"-cirkel stängs av)
  - Slide-bilder med beskrivande alt-text
- **Performance:**
  - Inga GSAP-animationer på modulsidor (bara på översiktsvyn vid behov)
  - Bilder lazy-loaded
  - Inga externa fonts utöver befintliga Fraunces/Inter på sajten

## PDF-sammanfattning (steg 2 och 4)

Den nedladdningsbara PDF:en innehåller **det viktigaste, inte hela kursen** (Johan: explicit krav). Föreslagen struktur (~8–12 sidor A4):

1. Försättssida (Johan + JLSU + tagline)
2. Sammanfattningsöversikt — sju moduler, en mening per
3. Diabilder: 5 grundregler (modul 2+3 distillerat)
4. Framförandet: 8 vanor (modul 4 distillerat)
5. Digital presentation: checklista (från modul 5)
6. Röst, kropp, språk: 10 vanliga fallgropar (kort version av modul 6 fördjupning)
7. Din nästa presentation: 7-punkts checklista
8. "Tack" + länk till kursen + Johan-kontakt

PDF:en byggs på samma sätt som befintliga guides (`exports/.../*.html` → `assets/pdfs/*.pdf` via existerande build-process). Designmässigt: choosewise-typsnitt, A4 stående, gott om luft.

## Avgränsningar (vad som INTE ingår)

- Ingen video-inspelning av Johan i kursen (kan komma som fas 2)
- Inga quiz/test med poängsystem
- Inga konton, ingen server, ingen mailinsamling
- Ingen översättning av enskilda slides till engelska — i EN-versionen byggs slide-figurerna om eller ersätts med engelskspråkiga ekvivalenter
- Ingen integration med Johans CRM/email/marketing-verktyg
- Ingen Advania-branding någonstans (originell-keynoten är hans, men kursen är JLSU/choosewise)

## Risker & öppna frågor

1. **Kameraåtkomst i modul 6:** webbläsare blockerar/varnar för mikrofon/kamera. Måste ha tydlig fallback (ljudfil-upload) och inte göra inspelning till blocker för att gå vidare.
2. **Slide-export utan Advania-branding:** Johan behöver göra en runda exporter från Keynote utan Advania-loggan, eller jag måste städa bort den i bildbehandling.
3. **Modul 6 risk för "för stor":** med 12 min huvudmodul + 19 tekniker i fördjupning blir den dubbelt så stor som modul 1 och 7. Acceptabelt om innehållet motiverar tiden — kontrollera under bygge att det inte blir överväldigande.
4. **Best practice-fördjupningar:** webbsökning kan generera generiska eller motstridiga råd. Lösning: jag presenterar 5–8 källor och Johan väljer vilka som passar hans röst innan vi skriver.
5. **PDF-omfång:** 8–12 sidor är en gissning. Validera när modulinnehåll är skrivet — kanske blir det 6 eller 16.
6. **EN-anpassning:** "skolfolk"-exempel som funkar i SV (svenska skolan) kanske inte landar 1:1 på engelska — vi tar en runda lokalisering, inte bara översättning.

## Lansering

- **Steg 1 (SV-kurs):** Lanseras när alla 7 moduler + 5 fördjupningar är klara. Crawlbar för Google. Lägg till `/sv/presentationsteknik/` i `sitemap.xml` och länka från `/sv/`-startsidan i en ny sektion.
- **Steg 2 (SV-PDF):** Tillgänglig från modul 7 + från en "Ladda ner"-CTA i översiktsvyn.
- **Steg 3 (EN-kurs):** Ersätter den nuvarande "under construction"-placeholdern.
- **Steg 4 (EN-PDF):** Som SV.

Ingen email-gating på PDF:en initialt — den ligger fritt nedladdningsbar för att maximera räckvidd. Kan senare ändras om Johan vill bygga lista.
