# Task 10 — rapport: checklistan och FAQ:n, sidorna 17–21

**Filer ändrade:** `_unpublished/exports/ai-for-students-print-a4-en.html` (EP),
`_unpublished/guides/ai-for-students/index.html` (EW), `docs/guide-facts-ai-for-students.md`.
Inget i `scripts/`, ingen PDF, inget omslag, ingen byggare, inga sidor 2–16, och webbytans
Gerlich-mening (sidan 6) är orörd. Sidan 17 (Part 4-avdelaren) är orörd.

**Svit:** 860 passed / 1 skipped / 0 failed. Ytkontrollen: 47 passed. Kolumnkontrollen:
37 postrader, 0 avvikande (oförändrat antal poster — inga nya S-id:n, bara befintliga
celler kompletterade).

**Ändringar gjorda, bara två, båda på sidan 21:**
1. FAQ "What does the EU AI Act mean for my classroom — the short answer?": `minimal-risk`
   (hyfenerat) → `<em>Minimal or no risk</em>` — en andra, osynkroniserad förekomst av
   samma fel Task 8 redan rättade på sidan 11.
2. FAQ "Do we need a Data Protection Impact Assessment (DPIA)?": en ny mening tillagd om
   AI Act:s egen, separata artikel 27-bedömning — Tråd 1, stängd.

Sidorna 17, 18, 19 och 20: **lästa, inget ändrat.**

---

## 1. Varje checklistfråga och FAQ-svar, läst mot rundans faktiska text

### Sida 17 — Part 4-avdelaren
Rörs inte (brevets egen rad). Inte läst mot några sakpåståenden.

### Sida 18 — checklistan: Pedagogik + Förutsättningar (4 ändrade sidor i Del 1–2 bakom den)

| # | fråga | läst mot | bedömning |
|---|---|---|---|
| 1 | "What learning should this lesson produce... elevate... or replace?" | Part 1:s kärnram (elevate/replace), orörd av Task 7 | Håller. Ingen ändring i Del 1:s grundbegrepp — bara forskningscitaten på sidorna 4/6 ändrades, inte ramverket. |
| 2 | "Does AI challenge the student's thinking, or replace it?" | samma ram | Håller, ingen ändring. |
| 3 | "Would the same learning outcome be reached equally well or better without AI?" | samma ram | Håller, ingen ändring. |
| 4 | "Does AI use fit the subject and topic? (I in WISE...)" | WISE-ramverket, sidan 5, orörd | Håller. |
| 5 | "Do I as the teacher have enough AI literacy to evaluate students' AI responses and catch bias and hallucinations?" | Del 2:s lärarkunskaps-avsnitt, sidorna 9–10, orörda av Task 8 (som bara rörde sidorna 11–12) | Håller, ingen ändring. |
| 6 | "Have students practised source criticism of AI answers?" | samma avsnitt | Håller. |
| 7 | "Is the tool compliant with your jurisdiction's data protection rules and approved by your school authority?" | regleringsavsnittet, sidorna 11–12 | Generisk ("din jurisdiktions regler"), gör inget tidsbundet eller risknivå-specifikt påstående som S28/S29/S30:s rättelser skulle underminera. Håller orört. |

**Inget ändrat på sidan 18.**

### Sida 19 — checklistan: Tillsyn + Uppföljning (visibility-premissen)

| # | fråga | läst mot | bedömning |
|---|---|---|---|
| 8 | "Do I have visibility into what students are asking the AI during the lesson — at least at the aggregated class level?" | sidan 15:s nya text (Task 9: majoriteten saknar vyn, Khanmigo OCH SchoolAI annonserar den) | **Brevets eget citat av den "nuvarande" frågan — "...at least afterwards?" — matchar INTE den faktiska filen.** Arbetsträdets fråga lyder redan "...at least at the aggregated class level?" (bekräftat med `grep` mot båda ytorna innan jag ändrade något). Frågan är en **självutvärdering för läraren** ("do I have"), inte ett påstående om marknaden — den gör inget uttalande om huruvida LEVERANTÖREN erbjuder vyn, bara om just den här läraren har den. Uppföljningssatsen ("If not, the lesson depends on you moving around...") är villkorad på "if not" och håller oavsett om noll, en eller två leverantörer erbjuder funktionen. Sidan 15:s nya premiss (två namngivna leverantörer gör det) GÖR frågan mer relevant att svara "ja" på för en skola som valt rätt verktyg, men ändrar inget i frågans eget sanningsvärde eller lydelse. **Lämnat orört, med skälet ovan.** |
| 9 | "Does the school's management tool or clear rules prevent students from leaving the assigned task?" | sidan 16 (enhetsstyrning), en annan dimension än frågeinnehåll-vyn, orörd av Task 9 (se dess rapport §4) | Håller, ingen ändring. |
| 10 | "Can I interrupt and hold a short whole-class discussion..." | ingen koppling till visibility-premissen | Håller. |
| 11 | "How will I assess whether students actually learned more or less... (E in WISE)" | WISE, orörd | Håller. |
| 12 | "What signs of cognitive outsourcing should I be looking for?" | ingen koppling | Håller. |

**Inget ändrat på sidan 19.**

### Sida 20 — FAQ, första halvan

| fråga | läst mot | bedömning |
|---|---|---|
| "I don't know AI myself — should I wait...?" | UNESCO/OECD-rekommendationen, sidan 8 (orörd av Task 8, men S11:s cell nu kompletterad, se Tråd 2 nedan) | Håller, ingen ändring i guidetexten. |
| "What should I require from a vendor...?" | sidan 15:s visibility-premiss | "teacher visibility — at least at the aggregated class level" är köpråd ("require detta av din leverantör"), konsekvent med att MAJORITETEN saknar funktionen men den är görbar (precis det Khanmigo/SchoolAI bevisar). Håller, ingen ändring. |
| "What do I do if the school doesn't have a device management tool?" | sidan 16 | Ingen koppling till någon av de fyra rättelserna. Håller. |
| "How do I tell if a student has outsourced the work to AI?" | ingen koppling | Håller. |

**Inget ändrat på sidan 20.**

### Sida 21 — FAQ, andra halvan (AI Act-svaret, DPIA-svaret)

| fråga | läst mot | bedömning |
|---|---|---|
| "What does the EU AI Act mean for my classroom — the short answer?" | sidan 11:s rättade text (S28/S29), risknivånamnet | **Fel funnet och rättat** — se §2 nedan. |
| "Do we need a Data Protection Impact Assessment (DPIA)?" | S30, tråden Task 8 lämnade öppen | **Tråden stängd** — se §3 nedan. |
| "Is AI good or bad for student learning?" | ingen koppling till någon regleringsrättelse eller forskningscitat | Håller, ingen ändring. |
| "Where do I get help with AI policy for my school?" | ingen koppling | Håller, ingen ändring. |

---

## 2. Fyndet: en andra, osynkroniserad förekomst av "minimal risk"-felet

Sidan 21:s AI Act-svar löd (identiskt på båda ytorna, före ändring):

> "...very little. You're in the minimal-risk category and normal data discipline is
> enough..."

Detta är samma sakfel S29 redan rättade på sidan 11 (Aktens fjärde risknivå heter
"Minimal or no risk", inte "minimal risk") — men i **hyfenerad** form (`minimal-risk`,
inte `minimal risk` med mellanslag). Task 8:s `borttaget`-vaktrad för S29 ankrar på
`minimal risk` (mellanslag); `surfacecheck.normalise()` slår bara om Unicode-
bindestreckvarianter till ASCII-hyphen, den slår **aldrig** om hyphen till mellanslag
eller tvärtom (se `scripts/tests/surfacecheck.py`, `_DASHES`/`normalise()`). Den
hyfenerade stale-frasen hade alltså överlevt Task 8:s rättelse helt osynlig för vakten
— exakt den typ av tyst kvarlevande fel brevet varnade för, bara upptäckt genom att
läsa filen i stället för att lita på att en tidigare rättelse redan täckte allt.

**Rättat, identiskt på båda ytorna:**

> "...very little. You're in the *Minimal or no risk* category and normal data
> discipline is enough..."

**Vaktrader:** ny `borttaget`-rad `S29 | en | minimal-risk | borttaget`, skild från den
befintliga mellanslags-raden eftersom de är olika strängar för `normalise()`. Ingen ny
`aktiv`-rad behövdes — `Minimal or no risk` är redan `aktiv` sedan Task 8 och täcker nu
båda förekomsterna (sidan 11 och sidan 21).

---

## 3. Tråd 1 stängd — artikel 27 i DPIA-svaret

Task 8 skrev in artikel 27 på sidan 11 (i S28:s rättade mening) men avgränsade sig
uttryckligen från sidan 21, eftersom FAQ:n stod listad som Task 10:s egen rad. DPIA-
svaret bar därför fortfarande bara GDPR artikel 35 — en läsare som bara läser FAQ:n
missade att AI Act har en egen, separat konsekvensbedömning för samma högrisksystem.

**Tillagd mening, identisk på båda ytorna** (efter "Consult your data protection
officer."):

> "The AI Act adds a separate requirement for the same high-risk systems, education
> included: Article 27's fundamental-rights impact assessment before first use,
> whether the school is publicly run or an independent provider of a public service —
> a GDPR DPIA does not cover it."

Ordalydelsen för "whether... public service"-ledet är densamma som A38/G51/S28 redan
låste fast (inte "a body governed by public law", som är sant för en kommunal skola
och falskt för en friskola). Källa: `docs/guide-facts-apple-intelligence.md` A38,
`docs/guide-facts-gemini.md` G51 (artificialintelligenceact.eu, hämtad 2026-10-13).

EW:s befintliga extra sista mening ("In the EU, national DPAs publish guidance...")
är orörd och står nu sist, efter den nya meningen — en känd, redan existerande
EW/EP-divergens (EW har en sista sats EP saknar) som jag inte skapade och inte stänger.

**Vaktrad:** `S30 | en | a GDPR DPIA does not cover it | aktiv` — kort, unikt för den
nya FAQ-meningen, skild från S28:s identiska "Article 27"-fras på sidan 11 (så en
framtida strykning av endera meningen slår rött oberoende av den andra).

Mätt, båda ytorna, ordagrant identiskt: `grep -o` bekräftar exakt samma 274-teckens
mening på EP och EW (se körningen nedan).

---

## 4. Tråd 2 stängd — UNESCO-citeringsluckan (S11)

Guiden skriver på sidan 8: "15 competencies across five dimensions" om UNESCO:s
ramverk. S11:s källcell belade bara titel, upphovsmän och år — inte den detaljen.
Komplettering (samma URL cellen redan citerade, unesco.org/en/articles/
ai-competency-framework-teachers), hämtad på nytt 2026-10-15: ordagrant **"the
publication outlines 15 competencies across five dimensions."** Talen är alltså
sanna. **Ingen guidetext ändrad** — bara S11:s källcell och dess verdiktcell i
`docs/guide-facts-ai-for-students.md` kompletterade med citatet, enligt tråd 2:s
egen instruktion.

---

## 5. Vaktraderna, nya i den här uppgiften

```guard
S29 | en | minimal-risk | borttaget
S30 | en | a GDPR DPIA does not cover it | aktiv
```

**Mätning, före och efter, båda ytorna:**

```
$ grep -o "minimal-risk" <båda ytorna>          → 0 / 0  (efter; var 1 / 1 före)
$ grep -o "Minimal or no risk" <båda ytorna>    → 2 / 2  (efter; var 1 / 1 före — sidan 11 + sidan 21)
$ grep -o "a GDPR DPIA does not cover it" <båda ytorna> → 1 / 1
```

Den nya DPIA-meningen är verifierad ordagrant identisk på EP och EW med `grep -o`
(samma 274-teckenssträng, tecken för tecken).

---

## 6. Sidornas teckenantal, före och efter

Baslinjen (sidkartan, mätt ur den ännu orenderade PDF:en — oförändrad, ingen tidigare
uppgift rörde sidorna 17–21, och jag renderar inte om, enligt brevets instruktion):

```
18  951 tecken (orörd)
19 1330 tecken (orörd)
20 2270 tecken (orörd)
21 2140 tecken
```

Sidorna 18, 19 och 20 är inte rörda — inget att mäta om. Sidan 21:s delta mätt direkt
på den faktiska teckenskillnaden i det ändrade HTML-stycket (text, taggar borträknade,
samma metod som Task 7–9):

```
"minimal-risk" (12 tecken) → "Minimal or no risk" (18 tecken): +6
ny DPIA-mening tillagd: +274
Total delta sidan 21: +280 tecken
```

Verifierat maskinellt genom att extrahera hela sidan-21-blocket ur EP före och efter
(ren text, taggar och entiteter normaliserade): 2099 → 2379 tecken i den extraherade
blocktexten, delta **+280**, exakt samma tal som handräkningen.

| sida | före | efter (uppskattat) |
|---|---|---|
| 18 | 951 | 951 (orörd) |
| 19 | 1330 | 1330 (orörd) |
| 20 | 2270 | 2270 (orörd) |
| 21 | 2140 | **≈2420** (+280, ~13 %) |

**+13 % är mindre än de två tidigare växande sidorna i rundan** (sidan 11 ~+16 %,
sidan 15 ~+26 %), och är den minsta ändring jag kunde göra som fortfarande stänger
båda trådarna fullt ut — jag övervägde en kortare version av DPIA-meningen (bara
"Article 27 also applies" utan att skriva ut vem bedömningen gäller eller att en
GDPR-DPIA inte räcker) men det hade återinfört exakt den typ av ofullständighet
S28/S30 redan en gång rättade (en artikelhänvisning utan att säga vad den kräver
eller av vem). Jag har INTE renderat om PDF:en — det äger en senare uppgift (Task 14).

---

## 7. Verifiering

```
$ /usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
47 passed in 3.79s

$ /usr/bin/python3 -m pytest scripts/tests -q
860 passed, 1 skipped in 65.15s

$ kolumnkontroll (7 oescapade pipes per postrad)
37 postrader, {7: 37} → 0 avvikande
```

---

## 8. Det jag läste men lämnade orört, med skäl (så nästa runda inte läser om samma sidor)

- **Checklistfråga 1–7 (sidan 18):** inget innehåll som rör någon av rundans fyra
  rättelser (visibility-premissen, de struckna/ersatta forskningscitaten, AI Act-
  distinktionen, risknivånamnet). Se tabellen i §1.
- **Checklistfråga 8 (sidan 19, tillsynsfrågan):** brevets eget citat av "nuvarande"
  lydelse matchade INTE den faktiska filen (se §1, sida 19, rad 8) — frågan var redan
  "at least at the aggregated class level", inte "at least afterwards". Frågan är en
  självutvärdering, inte ett marknadspåstående, och håller oförändrad oavsett hur många
  leverantörer som annonserar funktionen.
- **Checklistfråga 9–12 (sidan 19):** ingen koppling till visibility-premissen eller
  någon av de fyra rättelserna.
- **FAQ, sidan 20, alla fyra frågorna:** ingen koppling till rundans rättelser.
- **FAQ, sidan 21, "Is AI good or bad" och "Where do I get help":** ingen koppling.
- **EW:s extra sista mening i DPIA-svaret** ("In the EU, national DPAs publish
  guidance...") och EW:s extra länk i AI Act-svaret ("See Part 2 · Regulation above"):
  kända, redan existerande EP/EW-divergenser, inte skapade av mig och inte en del av
  uppdraget att harmonisera — lämnade orörda, nu placerade efter mina tillägg i
  flödet.
- **S11:s detalj "15 competencies across five dimensions":** var tidigare omärkt som
  overifierad (Task 8:s not); nu belagd (Tråd 2, §4). Ingen guidetext ändrad, bara
  inventeringscellen.

---

## Mina farhågor

- **Brevets citat av checklistfråga 8 ("at least afterwards") matchar inte filen.**
  Jag har följt uppdragets egen huvudregel ("läs mot vad rundan faktiskt skrev, inte
  mot vad planen sa") och agerat på den faktiska texten, men flaggar discrepansen
  eftersom den kan betyda att brevets författare hade en annan version av filen i
  åtanke, eller blandat ihop den med en syskonguide. Om Johan avsåg en specifik
  ändring till frågans lydelse som jag inte kan härleda ur den faktiska texten eller
  ur Task 7–9:s rapporter, är den ogjord.
- **Sidan 21 växer ~13 %** (2140 → ≈2420 tecken), den tredje sidan i rundan som växer
  märkbart (efter sidan 11:s ~16 % och sidan 15:s ~26 %). Jag har inte renderat om för
  att verifiera en faktisk ompaginering — Task 14 bör mäta om sidan 21 (och eventuellt
  22, om sidan 21 svämmar över) med en färsk `pdftotext`-körning.
- **Jag skrev en ny mening snarare än att bara infoga ordet "Article 27"** i DPIA-
  svaret, efter avvägningen i §6 — en kortare insättning hade återinfört den typ av
  ofullständighet (artikelnummer utan vem/vad) som S28/S30 redan en gång rättade. Om
  Johan ville ha en minimal, enda-ords-insättning i stället, är det en annan avvägning
  än den jag gjorde.
