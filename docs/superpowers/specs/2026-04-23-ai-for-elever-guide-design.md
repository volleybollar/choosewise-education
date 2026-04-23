# AI för elever på lektionstid — guide design

**Status:** Approved via chat brainstorming 2026-04-23
**Tool target:** Johan's Swedish ed-tech consulting site (JLSU → choosewise.education)
**Language:** Svenska först, engelsk version efter

---

## Thesis

Att låta elever använda AI på lektionstid är ett **pedagogiskt beslut**, inte ett tekniskt. RÄTT-modellen är beslutsramverket. Guiden väger möjligheter (AI som utmanar tänkandet) mot faror (AI som ersätter tänkandet) och ger läraren en lektionsnivå-checklista. Två premisser genomsyrar hela texten: **(a)** utan lärares AI-litteracitet sker saker som inte borde hända; **(b)** de flesta AI-verktyg saknar lärarinsyn i vad eleverna frågar.

## Placering & filstruktur

- **SV:** `sv/guider/ai-for-elever/index.html` + `styles.css` + `script.js`
- **EN:** `guides/ai-for-students/index.html` + `styles.css` + `script.js` *(senare)*
- **PDF-källa:** `exports/guides/ai-for-elever-sv.html` → `assets/pdfs/guides/ai-for-elever-sv.pdf`
- **Index-uppdatering:** lägg till posten i `sv/guider/guides-sv.json` och `guides/guides-en.json`
- **Omslagsbild:** `assets/images/guide-covers/ai-for-elever.svg`
- **Slug:** `ai-for-elever` (SV) / `ai-for-students` (EN)

## Struktur (5 delar, ~15-20 PDF-sidor)

**Del 1 — Syftet är lärandet** *(~3-4 sidor)*
- Tes: skola = lärande; verktyg bedöms på lärandeimpact
- RÄTT-modellen introduceras som beslutsramverket (länk till `/sv/ratt/`)
- Outsourcad kognition vs utmanad kognition — nyckeldistinktion
- *"Kortsiktig prestation kan förbättras, men långsiktig kognitiv arkitektur försämras"* — den hederliga nyansen

**Del 2 — Förutsättningar innan AI hamnar på lektionen** *(~4-5 sidor)*
- Lärarens AI-litteracitet som förutsättning
- Källkritik, bias, hallucinationer i AI-eran
- Myten om teknisk överlägsenhet — läraren behöver inte kunna tekniken bättre, man lär sig tillsammans
- UNESCO AI Competency Framework for Teachers (2024) som normativ referens

**Del 3 — På lektionsgolvet** *(~4-5 sidor)*
- Historisk parallell: dator-eran, PISA 2015 digital paradox, West Point RCT
- Reframing: **inte** "datorer är dåliga" utan "datorer utan lärarinsyn/pedagogisk inramning är dåliga"
- Managering av digitala miljöer förespråkas
- **Insyn-gapet:** Gemini/ChatGPT/Copilot ger inte klassaggregerad insyn. Svenska K-12-alternativen Skolup och Pladdra gör det inte heller publikt. (EN-version nämner SchoolAI som undantag.)
- Vad läraren bör kräva: aggregerad insyn per klass för att kunna lyfta mönster till helklassdialog

**Del 4 — Checklista: Ska eleverna använda AI på den här lektionen?** *(~2-3 sidor)*
12 frågor i 4 kategorier: Pedagogik (4) / Förutsättningar (3) / Kontroll (3) / Uppföljning (2).

**Del 5 — FAQ + nedladdning** *(~1-2 sidor)*
4-6 frågor. Konkret: "Jag kan inte AI själv — ska jag avstå?", "Vad kräver jag av leverantören?", "Vad gör jag om skolan saknar manageringsverktyg?"

## Checklistans innehåll (12 frågor)

**Pedagogik**
1. Vilket lärande ska lektionen producera? Ökar AI lärandet eller ersätter det?
2. Utmanar AI tänkandet (*"förklara varför mitt svar är fel"*) eller ersätter det (*"skriv min uppsats"*)?
3. Hade samma lärandemål uppnåtts lika bra utan AI?
4. Passar AI ämnet och momentet? (Ä i RÄTT)

**Förutsättningar**
5. Har jag tillräcklig AI-litteracitet för att bedöma elevernas AI-svar?
6. Har eleverna tränat på källkritik av AI-svar?
7. Är verktyget GDPR-kompatibelt och godkänt av huvudmannen?

**Kontroll**
8. Har jag insyn i vad eleverna frågar AI — minst på aggregerad klassnivå?
9. Hindrar skolans manageringsverktyg/regler eleverna från att lämna uppgiften?
10. Kan jag avbryta och hålla en kort genomgång om klassen fastnar?

**Uppföljning**
11. Hur ska jag bedöma om eleverna lärde sig *mer* eller *mindre* än utan AI? (T i RÄTT)
12. Vilka tecken på outsourcad kognition ska jag leta efter?

## Källor (8-10 i texten)

| Del | Källa | Användning |
|---|---|---|
| 1 | OECD *Unlocking High-Quality Teaching* (Houldsworth & Pons, 2025) | Auktoritet för "skola = lärande" + varning mot teknik-solutionism (s. 8, p. 3) |
| 1 | Kosmyna et al. MIT *Your Brain on ChatGPT* (2025) | 55% lägre hjärnkonnektivitet — outsourcad kognition konkret |
| 1 | Wang & Fan meta-analys (2025) *Computers & Education* | Ärlig komplikation: kortsiktig prestation förbättras |
| 1 | Lee et al. Microsoft (CHI 2025) | Effort-förflyttning från generera→verifiera |
| 2 | UNESCO AI Competency Framework for Teachers (2024) | 15 kompetenser, 5 dimensioner — normativ referens |
| 2 | Yilmaz et al. *Scientific Reports* (2025) | Lärar-beroende → sämre undervisningskvalitet |
| 3 | **Unos Uno / Grönlund m.fl. (Örebro universitet, 2011-2014)** | **Svensk empirisk anchor:** skolor som LYCKADES med 1:1 hade MER lärarledd tid. Ensamarbete vid skärmen ökade men sänkte lärandet. |
| 3 | OECD PISA 2015 *Students, Computers and Learning* (Schleicher) | Digital paradox — internationell spegel till Unos Uno |
| 3 | Zheng meta *Review of Educational Research* (2016) | Nyckel: effekten beror på lärarintegration |
| 3 | Skolverkets råd om AI-chattbottar | Svensk kontext |
| 3 (EN) | SchoolAI dokumentation + Bloomberg-investigation 2025 | EN-version: insyn-gapet konkret |

## Tonalitet & röst

Följer Johans röst-DNA från jlsu.se-analys (voice-skill ska invokeras innan skrivande):
- Auktoritativ men pragmatisk
- Utmanande men konstruktiv
- Provocera till eftertanke utan att raljera
- Praktisk — varje princip måste översättas till lärarbeslut
- Undvik teknik-hajp och teknik-rädsla i lika mån

## Implementation — filer att skapa

1. `docs/superpowers/specs/2026-04-23-ai-for-elever-guide-design.md` (detta dokument)
2. `sv/guider/ai-for-elever/index.html` (~700-900 rader baserat på befintliga guider)
3. `sv/guider/ai-for-elever/styles.css` (återanvänder guide-CSS-mönster)
4. `sv/guider/ai-for-elever/script.js` (anchor-nav-scroll, återanvänder mönster)
5. `exports/guides/ai-for-elever-sv.html` (PDF-källa) — A4-format, egen CSS
6. `assets/pdfs/guides/ai-for-elever-sv.pdf` (renderas via Playwright)
7. `assets/images/guide-covers/ai-for-elever.svg` (omslagsbild i stil med övriga)
8. Uppdatera `sv/guider/guides-sv.json`
9. Uppdatera `sv/guider/index.html` (läggs till av eventuell regenerator, annars manuellt)

EN-version görs i separat pass efter SV är godkänd.

## Godkännande

Design + checklist + källor godkända i chatt 2026-04-23. Tes-justering för kortsiktig vs långsiktig kognition godkänd. Skolup-stavning (inte Skollup) och svensk-specifika verktyg noterade. Auto mode — "kör igång".
