# Elevguiden, riktad till educators på engelska — implementationsplan

> **För agentiska arbetare:** OBLIGATORISK SUB-SKILL: använd
> `superpowers:subagent-driven-development` (rekommenderas) eller
> `superpowers:executing-plans` för att köra planen uppgift för uppgift. Stegen använder
> checkbox-syntax (`- [ ]`).

**Mål:** Gör `ai-for-students` sann mot oktober 2026 och uttalat riktad till educators med
engelska som språk, och leverera **en** omrenderad engelsk PDF — ingen quick-start, svenska
ytorna frysta.

**Arkitektur:** Guiden har ingen påståendeinventering i dag. Rundan bygger den först
(`docs/guide-facts-ai-for-students.md`), verifierar den mot primärkällor i fyra
mätuppgifter, och **grindar** mot Johan innan en enda mening skrivs om. Sedan rättar
innehållsuppgifterna sin del av guiden **på båda engelska ytorna** och uppdaterar **sina egna
inventeringsrader i samma commit**. Kartorna fylls, omrenderingen stänger rundan, och
`UNMAPPED_GUIDE_SURFACES` stryks sist.

**Teknikstack:** Python 3.9.6 via `/usr/bin/python3` — **enda interpretern** med pytest,
playwright och Pillow. `pdftotext` (poppler) för PDF-text. Inga nya beroenden.

**Spec:** `docs/superpowers/specs/2026-10-14-ai-for-students-educators-design.md` — **läs
amendemanget först i §1.** Det rättar specens sidantal (22, inte 16) och bär sidkartan som
hela den här planen äger sina sidor ur.

---

## Globala villkor

- **Varje innehållsändring görs på BÅDA engelska ytorna.** `EP` =
  `_unpublished/exports/ai-for-students-print-a4-en.html` (print, 22 renderade sidor), `EW` =
  `_unpublished/guides/ai-for-students/index.html` (webb). Ytorna bär i allt väsentligt samma
  text, men **de divergerar redan**: printytans rubrik *"GDPR in practice (EU) / equivalent
  data protection rules elsewhere"* finns inte på webbytan. Leta upp motsvarande passage;
  skriv aldrig över den ena ytan med den andras text.
- **De exakta värdena står i inventeringen, ordagrant citerade ur primärkällan.** Hämta dem
  därifrån — härled dem inte på nytt, och hitta aldrig på ett värde.
- **Ett tal som inte går att läsa ordagrant ur primärkällan TAS BORT.** Det skrivs inte om
  till ett annat tal, och det hedgas inte. Samma regel för en attribution: ett citat som inte
  går att belägga lämnar guiden — **borttaget, inte omskrivet.** Specen §6 klass 1.
- **Johans fem beslut (spec §1 och §4):** målgruppen är `educators` med engelska som språk;
  **ingen quick-start byggs**; titeln får avvika och behålls som frågan `Should students use
  AI in class?`; underrubriken bär läsaren (`for educators`); **ingen innehållsförteckning**.
- **`ai-for-elever-sv.pdf` och den svenska printytan ska komma ut byte-identiska.**
  `build-ai-for-elever-pdf.py` renderar EN och SV i samma körning utan språkargument. Kopiera
  undan den svenska filen och återställ med `cp` — **aldrig** `git checkout --` på en katalog
  (det har kostat två av Johans filer en gång).
- **Interpretern är `/usr/bin/python3`.** Hela sviten:
  `/usr/bin/python3 -m pytest scripts/tests -q`
  Utgångsläge på `main` `9c51cab`: **854 passed / 1 skipped / 0 failed**. Den skippade raden
  är avsiktlig (`NO_PAGE_CLAIM` är tom — rör den inte). Talet ska aldrig sjunka utan att
  uppgiften säger varför, och noll failed är kravet. Faller elva tester i
  `test_prompt_pdf_parity.py` är facitkatalogen `/tmp/pdf-parity-before/` tom — återskapa den
  enligt testets egen felutskrift, det är inte rundans fel.
- **`docs/` är gitignorerad.** Inventeringen och specen committas med `git add -f`.
- **`git add -A` används aldrig.** Repot bär normalt ocommittade filer som tillhör Johan.
- **Ingenting publiceras.** Bara `_unpublished/`, `docs/` och `scripts/` får ändras.

## Granskningsfokus

Fem fel som specen förutsätter borta men som ingen enskild uppgifts test fångar av sig själv.
Var och en är pinnad i den uppgift som äger koden.

1. **En rättelse som bara träffar en yta.** Ytkonsistensvakten läser bara de värden
   inventeringen pekar på, så en rättelse som missar EW blir röd först om posten har en
   `aktiv`-rad — och tyst annars. *Pinnad i varje innehållsuppgift (Task 6–11): sista steget
   kör ytkontrollen över båda ytorna.*
2. **Ett tal som skrivs om i stället för att tas bort.** Den farligaste frestelsen i den här
   guiden: `55 percent` går inte att belägga, och att skriva `omkring hälften` är samma fel
   med mjukare ord. *Pinnad i Task 2 och 3: varje tal får antingen en källcell med ordagrant
   citat, eller verdiktet `struket`.*
3. **En `aktiv`-rad ankrad på en lång mening i stället för på värdet.** En legitim
   omformulering fäller då vakten, och den som lagar det tar bort raden. *Pinnad i Task 1:
   inventeringens huvud bär regeln, och i varje innehållsuppgift: ankaret är värdet, inte
   satsen.*
4. **Avdelningssidorna fälls av stoppvillkoret.** Tre av dem ligger redan under 400 tecken
   och är korta med avsikt. *Pinnad i Task 14: villkoret undantar omslaget och de fyra
   avdelningssidorna, och mäts med kollapsade blanktecken — aldrig borttagna.*
5. **Två tester försvinner med avsikt och ser ut som ett tapp.** Rundan stryker
   `UNMAPPED_GUIDE_SURFACES` och dess två vakter. *Pinnad i Task 15: insamlade test-id:n
   jämförs mot `main`, och diffen ska vara exakt de två borttagna plus de nya
   parametriseringarna.*

---

## Sidkartan och vem som äger vad

Varje sida i den renderade PDF:en har en ägande uppgift. Det är planens egen vakt mot
lärdomen från Apple-rundan: fillistor skrivna per avsnitt lämnade fyra sidor oägda.

| sida | innehåll | mäts av | skrivs av |
|---|---|---|---|
| 1 | omslaget | — | **T11** (titel, läsaretiketten, stämpeln — hela omslaget) |
| 2 | Introduction | — | **T7** |
| 3 | Part 1-avdelare | — | **T7** |
| 4 | OECD *Unlocking High-Quality Teaching* | **T2** | **T7** |
| 5 | WISE-ramverket | — | **T7** |
| 6 | Wang & Fan, Kosmyna, Lee | **T2** | **T7** |
| 7 | Part 2-avdelare | — | **T8** |
| 8 | UNESCO-ramverket | **T3** | **T8** |
| 9 | källkritik, bias, hallucinationer | — | **T8** |
| 10 | "Teachers don't need to know the tech better" | — | **T8** |
| 11 | GDPR och AI Act | **T5** | **T8** |
| 12 | GDPR i praktiken | **T5** | **T8** |
| 13 | Part 3-avdelare | — | **T9** |
| 14 | PISA 2015, Carter 2017, Zheng 2016, Unos Uno | **T3** | **T9** |
| 15 | The visibility gap — produktlandskapet | **T4** | **T9** |
| 16 | klassrumshantering | — | **T9** |
| 17 | Part 4-avdelare | — | **T10** |
| 18 | checklistan: pedagogik, förutsättningar | — | **T10** |
| 19 | checklistan: tillsyn, uppföljning | — | **T10** |
| 20 | FAQ, första halvan | — | **T10** |
| 21 | FAQ, andra halvan (AI Act, DPIA) | **T5** | **T10** |
| 22 | slutcitatet och licensbandet | — | **T11** |

---

### Task 1: Inventeringens skelett och påståendecensusen

Rundans arbetsorder. Ingen annan uppgift får skriva en mening förrän den här filen finns.

**Filer:**
- Skapa: `docs/guide-facts-ai-for-students.md`

**Gränssnitt:**
- Konsumerar: inget.
- Producerar: postrader `S01…Snn` med kolumnerna `| id | påstående i guiden | EW | EP |
  primärkälla + hämtdatum | verdikt |`, och ett `## Vaktblocket` med rader på formen
  `Snn | en | <sträng> | aktiv|borttaget`. Varje senare uppgift läser sina poster härifrån.

**Formen ärvs ordagrant från `docs/guide-facts-apple-intelligence.md`** — den mest utvecklade
av de fyra. Kopiera dess struktur, inte dess innehåll: huvudet, verdikttaxonomin,
utfallsräkningen och vaktblockets kommenterade huvud. **Tre skillnader mot syskonen, och de
ska stå i huvudet:** guiden har **ingen QS-kolumn** (ingen quick-start finns och ingen ska
byggas), de **svenska ytorna är frysta och har inga poster**, och **ingen innehållsförteckning
finns** så ingen post kan hänga på ett TOC-nummer.

**Taxonomin ärvs som den står efter omklassificeringen 2026-10-14**, `struket` inkluderat:
`står`, `föråldrat`, `falskt`, `obelagt`, `struket`, `rättat`, `lagt till`.

**Två regler skrivs in i huvudet, ordagrant:**
1. **En faktamening utan post i inventeringen får inte skrivas.**
2. **Ett fynd som inte behöver ändras stryks aldrig tyst** — det står kvar med en motivering.

**Och en tredje, som är den här rundans egen** (granskningsfokus 3): *ett `aktiv`-ankare är
det kortaste värde som bär påståendet — ett tal, ett namn, en tidskriftstitel — aldrig hela
satsen. På `borttaget`-sidan gäller motsatsen: en lång sträng som innehåller en kort förbjuden
är strikt svagare än den korta, eftersom en återinföring träffar den korta först.*

- [ ] **Steg 1: Mät varje kandidats förekomster per yta**

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
EP=_unpublished/exports/ai-for-students-print-a4-en.html
EW=_unpublished/guides/ai-for-students/index.html
for s in "Unlocking High-Quality Teaching" "150 classrooms" "Wang &amp; Fan" "69 studies" \
         "Kosmyna" "55 percent" "Lee et al" "319 knowledge workers" \
         "AI Competency Framework" "Students, Computers and Learning" "digital paradox" \
         "Carter, Greenberg" "0.18 standard deviations" "Zheng et al" "Unos Uno" \
         "11 municipalities" "largest chatbots" "Copilot is built on" "Khanmigo" \
         "MagicSchool" "ChatGPT for Teachers" "aggregated view" "back in 2014" \
         "teachers and school leaders" "Updated April 2026"; do
  printf '%-34s EW:%s EP:%s\n' "$s" "$(grep -c "$s" $EW)" "$(grep -c "$s" $EP)"
done
```
Skriv talen i kolumnerna **som de mäts**, inte som planen gissar dem. En kandidat med 0/0 har
ingen post; en med träff på bara en yta får sin divergens skriven i prosan och **ingen
`aktiv`-rad** (den hade varit `saknas_på_en_yta` från första sekunden — samma skäl som
Apples `IMY`).

- [ ] **Steg 2: Skriv skelettet med alla poster, verdiktkolumnen tom**

En rad per kandidat ovan som har minst en förekomst, grupperad i tre block med egna rubriker
i prosan: **forskningscitaten** (spec §6 klass 1), **produktlandskapet** (klass 2),
**regleringen** (klass 3). Källkolumnen lämnas tom — Task 2–5 fyller den.

- [ ] **Steg 3: Skriv sidkartan i huvudet**

Kopiera specens amendemang-tabell (22 sidor med teckenantal). Den är rundans referens för
ompaginering, och Task 14 mäter mot den.

- [ ] **Steg 4: Verifiera att filen parsar innan den committas**

```bash
/usr/bin/python3 -c "
import sys; sys.path.insert(0,'scripts')
from tests import factinventory
rows = factinventory.parse_guard_block(open('docs/guide-facts-ai-for-students.md').read())
print(len(rows), 'vaktrader parsade')"
```
Heter funktionen något annat i `factinventory.py` — läs modulen och använd dess eget namn.
Förväntat i det här läget: **0 rader** (vaktblocket är tomt tills innehållsuppgifterna
skriver sina), och **ingen traceback**. En traceback betyder trasig tabellsyntax.

- [ ] **Steg 5: Committa**

```bash
git add -f docs/guide-facts-ai-for-students.md
git commit -m "docs(students): inventeringens skelett och påståendecensusen"
```

---

### Task 2: Klass 1a — de fyra AI-forskningscitaten verifierade (sidorna 4 och 6)

**Filer:**
- Ändra: `docs/guide-facts-ai-for-students.md` (källkolumn och verdikt för fyra poster)

**Gränssnitt:**
- Konsumerar: Task 1:s postrader.
- Producerar: verdikt och ordagranna källcitat för OECD *Unlocking*, Wang & Fan, Kosmyna et
  al. och Lee et al. Task 7 skriver texten utifrån dem.

**De fyra posterna, med exakt vad som ska beläggas:**

| post | som guiden skriver det | vad som måste läsas ordagrant ur källan |
|---|---|---|
| OECD *Unlocking High-Quality Teaching* | "In April 2025 the OECD published …", "grounded in 150 classrooms across 40 countries", plus ett ordagrant citat och påståendet att rapporten drar slutsatsen att inget skolinternt påverkar elevresultat mer än undervisningens kvalitet | att rapporten finns och utgivningsmånaden; **talen 150 och 40**; **citatet tecken för tecken**; och att slutsatsen är rapportens egen och inte guidens tolkning |
| Wang & Fan, *Computers & Education*, 2025 | "A substantial 2025 meta-analysis (Wang & Fan, *Computers & Education*, 69 studies) shows that ChatGPT in controlled experiments tends to improve students' performance, motivation and higher-order thinking in the short term" | tidskrift, år, **talet 69**, och att de tre utfallen är metaanalysens egna — inte tre guiden har lagt till |
| Kosmyna et al., MIT Media Lab 2025 | "An EEG study … measured brain connectivity while participants wrote essays with or without LLM help — the LLM group had up to 55 percent lower brain connectivity" | **talet 55 procent**, vad måttet faktiskt är, och studiens egna förbehåll om urval och varaktighet |
| Lee et al., Microsoft Research, CHI 2025 | "A parallel study … of 319 knowledge workers showed that high confidence in AI goes hand in hand with less critical thinking" | **talet 319**, att det är CHI 2025, och riktningen i slutsatsen |

- [ ] **Steg 1: Hämta varje källa rå och läs den lokalt**

```bash
mkdir -p /tmp/students-sources
curl -sSL -o /tmp/students-sources/oecd-unlocking.html "<URL>"
/usr/bin/python3 -c "
import re,sys,html
t=open('/tmp/students-sources/oecd-unlocking.html',encoding='utf-8',errors='replace').read()
t=html.unescape(re.sub(r'<[^>]*>',' ',t)); print(' '.join(t.split())[:4000])"
```
Samma mönster per källa. **En sammanfattning är aldrig källa till ett värde** — inte en
nyhetsartikel om studien, inte ett pressmeddelande, inte en annan sidas referat. Svarar
källan 403 eller ligger bakom betalvägg: försök förlagets DOI-sida och arXiv/preprint, och
**lyckas ingen hämtning blir posten `obelagt`.**

- [ ] **Steg 2: Skriv källcellen med ordagrant citat och hämtdatum**

Formen är Apple-inventeringens: `<url> → **200**, ordagrant 2026-10-NN: "<citat>"`. Citatet
ska innehålla det tal posten hänger på. Bär källan inte talet — skriv det i cellen: *"källan
bär inte talet"*.

- [ ] **Steg 3: Sätt verdikt, och använd `struket` när det är rätt ord**

`står` om värdet är belagt ordagrant. `falskt` om källan säger något annat. `obelagt` om
ingen primärkälla går att hämta. **Går talet inte att belägga blir posten `obelagt` nu, och
Task 7 stryker talet ur guiden — varefter posten blir `struket`.** Skriv aldrig ett nytt tal.

- [ ] **Steg 4: Committa**

```bash
git add -f docs/guide-facts-ai-for-students.md
git commit -m "docs(students): de fyra AI-forskningscitaten verifierade mot primärkälla"
```

---

### Task 3: Klass 1b — UNESCO-ramverket och de fyra 1:1-citaten (sidorna 8 och 14)

**Filer:**
- Ändra: `docs/guide-facts-ai-for-students.md` (fem poster)

**Gränssnitt:**
- Konsumerar: Task 1:s postrader.
- Producerar: verdikt och källceller för UNESCO-ramverket, PISA 2015, Carter 2017, Zheng 2016
  och Unos Uno. Task 8 och 9 skriver texten utifrån dem.

| post | som guiden skriver det | vad som måste beläggas |
|---|---|---|
| UNESCO, *AI Competency Framework for Teachers* | "In 2024 UNESCO published its AI Competency Framework for Teachers" | titeln ordagrant och året |
| OECD PISA, *Students, Computers and Learning* (2015) | "found what became known as the 'digital paradox': students who used computers frequently at school performed worse on PISA, even after controlling for socioeconomic background" | rapportens titel och år, **att kontrollen för socioekonomi är rapportens egen**, och om `digital paradox` är rapportens term eller en sekundärkällas etikett (guiden hedgar redan med "became known as" — kontrollera att hedgen räcker) |
| Carter, Greenberg & Walker (2017) | "ran a randomised controlled trial at the US Military Academy and found that classes where laptops were permitted had **0.18 standard deviations** lower scores" | effektstorleken, att designen är en RCT, och vad utfallsmåttet var |
| Zheng et al., *Review of Educational Research* (2016) | metaanalys av 1:1-program: "positive effects existed — but only where teachers integrated the devices pedagogically" | tidskrift, år, och **villkoret** — det är den halva guidens argument vilar på |
| Grönlund et al., Unos Uno, Örebro 2011–2014 | "the most cited Nordic longitudinal study … covering roughly **20 schools in 11 municipalities**", plus att ensamarbetet ökade och att sociala medier distraherade en betydande andel elever | talen, åren, och de två utfallen |

**Unos Uno är svensk, och det är inte ett problem.** Guiden ramar den redan som "Nordic
longitudinal study" — en internationellt citerbar beskrivning utan svensk läsarkontext. Den
står kvar. Det här är ett medvetet beslut och inte ett förbiseende: skriv motiveringen i
cellen, så att nästa runda inte tar bort den som en nationell referens.

- [ ] **Steg 1: Hämta och läs varje källa rått, samma mönster som Task 2 steg 1**

Unos Uno-rapporterna ligger på Örebro universitets DiVA. PISA 2015 ligger på
`oecd.org`/`oecd-ilibrary.org`. Carter m fl är publicerad i *Economics of Education Review*;
läs den publicerade versionen, inte ett arbetspapper med annan effektstorlek — **ett
arbetspapper och en publicerad artikel kan bära olika tal, och det är precis så ett fel i den
här klassen uppstår.**

- [ ] **Steg 2: Skriv källceller med ordagranna citat och hämtdatum**

- [ ] **Steg 3: Sätt verdikt. Samma regel som Task 2: inget nytt tal, någonsin**

- [ ] **Steg 4: Committa**

```bash
git add -f docs/guide-facts-ai-for-students.md
git commit -m "docs(students): UNESCO-ramverket och 1:1-erans fyra citat verifierade"
```

---

### Task 4: Klass 2 — produktlandskapet på sidan 15

Rundans känsligaste mätning. **Uppgiften skriver ingen guidetext.** Den mäter och rapporterar.

**Filer:**
- Ändra: `docs/guide-facts-ai-for-students.md` (sex poster)
- Läsa: `docs/guide-facts-apple-intelligence.md`, `docs/guide-facts-gemini.md`,
  `docs/guide-facts-copilot.md`

**Gränssnitt:**
- Konsumerar: Task 1:s postrader.
- Producerar: verdikt för sex produktpåståenden, och **ett beslutsunderlag till Johan** om den
  bärande utsagan faller.

| post | som guiden skriver det | hur den mäts |
|---|---|---|
| marknadsledarna | "The largest chatbots in K-12 classrooms today are Gemini (Google) and ChatGPT (OpenAI)" | en marknadsandelsutsaga utan källa. Finns ingen hämtbar primärkälla på K-12-andelar — och det gör det sannolikt inte — blir den `obelagt` och **omformuleras utan rangordning** |
| Copilots modell | "Copilot is built on ChatGPT" | **korsref** `guide-facts-copilot.md`. Var en förenkling redan i april och är sannolikt fel nu |
| Apple-vägen | "Apple Intelligence uses ChatGPT for the functions that go beyond the device" | **korsref A11/A12** i Apple-inventeringen, verdikt `står`, verifierat 2026-10-14. Korsref får bara användas mot poster vars verdikt är `står` eller `rättat` |
| K-12-produkterna | "Khanmigo, MagicSchool, and ChatGPT for Teachers" | tre produktnamn, var för sig mot leverantörens egen sida: finns produkten, och heter den så i dag |
| **den bärande utsagan** | "What the majority of these tools share, according to what's publicly advertised, is that they do not give teachers a clear aggregated view of which questions students in a class have asked the AI during a lesson" | mät mot varje namngiven leverantörs **egna** sidor om lärar-/administratörsvyer. Hedgen "according to what's publicly advertised" sätter mätningens ribba: det som är publikt annonserat |
| slutklämmen | "teachers suddenly have the instruments the 1:1 researchers were calling for back in 2014" | hänger på föregående; faller den faller den här |

- [ ] **Steg 1: Hämta varje leverantörs egen sida om lärarvyer, och läs den rått**

Minst: Google (Gemini for Education / Workspace for Education admin), OpenAI (ChatGPT Edu,
ChatGPT for Teachers), Microsoft (Copilot for Education), Khan Academy (Khanmigo Teacher
Tools), MagicSchool. Samma `curl` + lokal textextraktion som Task 2.

- [ ] **Steg 2: Skriv per leverantör vad som är publikt annonserat om aggregerad klassvy**

En rad per leverantör i postens källcell, med URL, hämtdatum och ordagrant citat. **Det här
är den mätning hela avsnittets slutsats vilar på — den ska gå att läsa om av en granskare utan
att hämta något själv.**

- [ ] **Steg 3: Sätt verdikt på de sex posterna**

- [ ] **Steg 4: GRIND — rapportera till Johan, skriv inget**

Rapporten ska svara på en fråga: **ger de stora verktygen i dag läraren en aggregerad vy över
vad klassen frågat?**

- **Nej, fortfarande inte:** avsnittet står i sak, posterna får `står`, och Task 9 rättar bara
  de enskilda produktpåståendena runt det.
- **Ja, minst några gör det:** då faller avsnittets slutsats, och **det är ett innehållsbeslut
  för Johan, inte en formulering för en uppgift.** Lägg fram vad som mätts per leverantör,
  vad som faller och vad som står kvar, och **invänta hans beslut.** Fortsätt inte till Task 5.

- [ ] **Steg 5: Committa mätningen**

```bash
git add -f docs/guide-facts-ai-for-students.md
git commit -m "docs(students): produktlandskapet mätt per leverantör, utan guidetext rörd"
```

---

### Task 5: Klass 3 — regleringen mätt mot A33–A39 (sidorna 11, 12 och 21)

**Filer:**
- Ändra: `docs/guide-facts-ai-for-students.md` (regleringsposterna)
- Läsa: `docs/guide-facts-apple-intelligence.md` (A33–A39 och deras vaktblock)

**Gränssnitt:**
- Konsumerar: Task 1:s postrader.
- Producerar: verdikt för regleringsposterna, med `korsref A33`…`A39` som källa där posten är
  densamma. Task 8 och 10 skriver texten utifrån dem.

**Mät mot de färdiga posterna, hämta inte om.** Apple-inventeringen bär, verifierade
2026-10-14 och med verdikt `står`/`rättat`/`lagt till`: AI Act:s tillämplighetsdatum
**2 augusti 2026**, de fyra risknivåerna, **artikel 4:s AI-kunnighetsplikt som gäller sedan
2 februari 2025**, artikel 16 som **leverantörens** plikter, artikel 26 som
**driftsättarens** fem plikter, artikel 27:s konsekvensbedömning, och Annex III-tidpunkten
**2 december 2027** efter AI Omnibus.

**Den kända felklassen ska letas aktivt, inte väntas på.** Att framställa
högriskskyldigheter som bindande i dag, eller att lägga leverantörens förhandsplikter på
skolan, har nu fällts i tre dokument: G48 i Gemini-rundan, Geminis bonuskapitels
`pre-market obligations` (fortfarande öppet) och Apples A36/A37.

**Meningen som bär risken, och som mäts först:** *"Both apply, both are the teacher's and the
school authority's responsibility, and neither can be postponed."* Den säger att allt gäller
nu. Artikel 4 gäller nu; Annex III-högrisk gör det inte förrän 2 december 2027. Mät om
meningen läses som det senare.

- [ ] **Steg 1: Läs A33–A39 och deras vaktblock**

```bash
grep -nE '^\| A3[3-9] ' docs/guide-facts-apple-intelligence.md
grep -nE '^A3[3-9] \| ' docs/guide-facts-apple-intelligence.md
```

- [ ] **Steg 2: Läs guidens tre regleringspassager rått**

```bash
/usr/bin/python3 -c "
import re,pathlib
t=' '.join(re.sub(r'<[^>]*>',' ',pathlib.Path('_unpublished/exports/ai-for-students-print-a4-en.html').read_text()).split())
for key in ['GDPR and the EU AI Act','GDPR in practice','What does the EU AI Act mean','Data Protection Impact Assessment']:
    i=t.find(key); print('---',key,'---'); print(t[i:i+1200],'\n')"
```

- [ ] **Steg 3: Skriv poster med `korsref`, och verdikt**

Där guidens påstående är samma som en Apple-post: `korsref A3N` plus den postens källa och
hämtdatum. Där guiden säger något Apple-inventeringen inte täcker (FERPA, delstatsregler, UK
GDPR): **egen hämtning, egen källcell** — eller `obelagt`.

- [ ] **Steg 4: Committa**

```bash
git add -f docs/guide-facts-ai-for-students.md
git commit -m "docs(students): regleringen mätt mot Apple-inventeringens A33-A39"
```

---

## GRINDEN — hela inventeringen rapporteras till Johan innan en mening skrivs om

**Stanna här.** Task 1–5 har mätt; Task 6–11 skriver. Mellan dem ligger en grind, av samma
skäl som Apple-rundan hade en efter uppgift 6: **de värden som faller är innehållsbeslut,
inte formuleringar.**

Rapporten till Johan innehåller:

1. **Utfallsräkningen**, räknad maskinellt ur postradernas inledande token — aldrig förd
   efter en lista:
```bash
/usr/bin/python3 - <<'PY'
import re, collections, pathlib
TOK = ["står","föråldrat","falskt","obelagt","struket","rättat","lagt till"]
c = collections.Counter()
for line in pathlib.Path("docs/guide-facts-ai-for-students.md").read_text().splitlines():
    if not re.match(r"^\| S\d+ \|", line): continue
    lead = [x.strip() for x in line.strip().strip("|").split("|")][-1].lstrip("*")
    c[next((t for t in TOK if lead.startswith(t)), "OKÄND")] += 1
print(dict(c), "summa", sum(c.values()))
PY
```
2. **Varje tal som inte gick att belägga**, med vad källan säger i stället.
3. **Varje attribution som inte gick att belägga** — och förslaget är alltid att ta bort den,
   inte skriva om den.
4. **Svaret på Task 4:s fråga**, och om den bärande utsagan faller: vad som återstår av
   avsnittet.

---

### Task 6: Läsartilltalet mätt i löptexten, och rättat där det brister

**Filer:**
- Ändra: `_unpublished/exports/ai-for-students-print-a4-en.html` (löptexten, sidorna 2–21)
- Ändra: `_unpublished/guides/ai-for-students/index.html` (motsvarande passager)
- Ändra: `docs/guide-facts-ai-for-students.md` (en post för läsartilltalet)

**Gränssnitt:**
- Konsumerar: inget från Task 2–5. Kan köras parallellt med dem, men **efter grinden**.
- Producerar: ett mätt, dokumenterat läsartilltal. Task 11 använder slutsatsen på omslaget.

**Mätt före planen, och det ändrar uppgiftens storlek:** etiketten
`teachers and school leaders` står på **en** plats i hela guiden — omslaget, som **Task 11**
äger. Löptexten talar redan till läraren rakt igenom. **Den här uppgiften är därför i första
hand en mätning**, och dess troliga utfall är "inget att rätta". Det utfallet ska **skrivas
ner**, inte hoppas över: en post i inventeringen med motivering, enligt regel 2.

- [ ] **Steg 1: Mät varje tilltal, per yta**

```bash
cd /Users/johan/Projekt/Choosewise/choosewise-education
/usr/bin/python3 - <<'PY'
import re, pathlib
for rel in ("_unpublished/exports/ai-for-students-print-a4-en.html",
            "_unpublished/guides/ai-for-students/index.html"):
    t = " ".join(re.sub(r"<[^>]*>", " ", pathlib.Path(rel).read_text(encoding="utf-8")).split())
    print("===", rel)
    for label, pat in (
        ("teachers and school leaders", r"teachers and school leaders"),
        ("educators",                   r"\beducators?\b"),
        ("du-tilltal 'you'",            r"\byou\b"),
        ("'your students'",             r"\byour students\b"),
        ("tilltalad elev ('you' + student-kontext)", r"\bif you are a student\b"),
    ):
        print(f"  {label:<44} {len(re.findall(pat, t, re.I))}")
PY
```

- [ ] **Steg 2: Läs varje `you`-förekomst i sitt sammanhang och avgör vem den talar till**

```bash
/usr/bin/python3 - <<'PY'
import re, pathlib
t = " ".join(re.sub(r"<[^>]*>", " ", pathlib.Path(
    "_unpublished/exports/ai-for-students-print-a4-en.html").read_text(encoding="utf-8")).split())
for m in re.finditer(r"[^.]{0,70}\byou\b[^.]{0,70}", t, re.I):
    print("•", " ".join(m.group(0).split()))
PY
```
En `you` som talar till en educator står. En som talar till en elev, eller till "skolan" som
abstraktion där en person behövs, skrivs om. **Lista fynden innan du ändrar något.**

- [ ] **Steg 3: Rätta det som brister, på båda ytorna**

Hittas inget: hoppa till steg 4. Hittas något: rätta det på båda ytorna, med samma
formulering där ytorna redan är samstämmiga.

- [ ] **Steg 4: Skriv posten i inventeringen, också om inget rättades**

Posten bär vad som mättes, vad utfallet blev och motiveringen. Blev utfallet "inget att
rätta" är verdiktet `står` — **och cellen säger att läsartilltalet är mätt och varför det
redan höll.** Det är den raden som gör att nästa runda inte mäter om samma sak.

- [ ] **Steg 5: Kör ytkontrollen och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
git add -f docs/guide-facts-ai-for-students.md
git add _unpublished/exports/ai-for-students-print-a4-en.html \
        _unpublished/guides/ai-for-students/index.html
git commit -m "fix(students): läsartilltalet mätt i löptexten, och dokumenterat"
```

---

### Task 7: Del 1 — sidorna 2 till 6

**Filer:**
- Ändra: `_unpublished/exports/ai-for-students-print-a4-en.html` (sidorna 2–6)
- Ändra: `_unpublished/guides/ai-for-students/index.html` (motsvarande avsnitt)
- Ändra: `docs/guide-facts-ai-for-students.md` (Task 2:s fyra poster, plus vaktrader)

**Gränssnitt:**
- Konsumerar: **Task 2:s verdikt och källceller.** Skriv inget som inte står där.
- Producerar: vaktrader för de fyra forskningscitaten i Del 1.

**Sidorna och vad som rörs:**

| sida | innehåll | vad uppgiften gör |
|---|---|---|
| 2 | Introduction | rörs bara om Task 6 eller 2 pekar dit |
| 3 | Part 1-avdelare | rörs inte |
| 4 | "If the tool elevates learning" | **OECD-citatet** enligt Task 2 |
| 5 | WISE-ramverket | rörs inte — ramverket är Johans eget och ingen volatil uppgift |
| 6 | "Challenging thinking, or replacing it" | **Wang & Fan, Kosmyna, Lee** enligt Task 2 |

- [ ] **Steg 1: Mät sidornas luft INNAN du skriver**

```bash
/usr/bin/python3 - <<'PY'
import re, subprocess
out = subprocess.run(["pdftotext","-layout",
  "_unpublished/assets/pdfs/guides/ai-for-students-en.pdf","-"],
  capture_output=True, text=True, check=True).stdout
for n in (2,4,6):
    p = out.split("\f")[n-1]
    print(n, len(re.sub(r"\s+"," ",p).strip()), "tecken")
PY
```
Jämför mot sidkartan i inventeringen (s2 2432, s4 1774, s6 2320 tecken). **Lägger du till mer
än ett stycke på en sida — mät igen efter, och säg det i committen.** Ompaginering är billig
att upptäcka nu och dyr i Task 14.

- [ ] **Steg 2: Läs Task 2:s källceller ordagrant**

```bash
grep -nE '^\| S[0-9]+ .*(Unlocking|Wang|Kosmyna|Lee et al)' docs/guide-facts-ai-for-students.md
```

- [ ] **Steg 3: Rätta de fyra citaten på båda ytorna**

Regeln ur globala villkor: **ett tal utan belagd källa tas bort, inte skrivs om.** Faller ett
helt citat är det attributionen som går — meningen får stå på egna ben eller falla. Lämna
aldrig "forskning visar" efter en struken studie: det är samma påstående utan avsändare.

- [ ] **Steg 4: Skriv vaktraderna**

```
# Elevguiden Task 7 — Del 1:s forskningscitat
S0n | en | <det belagda talet, t ex 150 classrooms across 40 countries> | aktiv
S0n | en | <det struckna talet, t ex 55 percent> | borttaget
```
Ankaret är **värdet**, inte satsen (granskningsfokus 3). Ett struket tal får en
`borttaget`-rad — det är den raden som gör det omöjligt att skriva tillbaka talet.

- [ ] **Steg 5: Kör ytkontrollen, hela sviten, och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
/usr/bin/python3 -m pytest scripts/tests -q
git add -f docs/guide-facts-ai-for-students.md
git add _unpublished/exports/ai-for-students-print-a4-en.html \
        _unpublished/guides/ai-for-students/index.html
git commit -m "fix(students): Del 1 — forskningscitaten mot primärkälla"
```

---

### Task 8: Del 2 — sidorna 7 till 12

**Filer:**
- Ändra: `_unpublished/exports/ai-for-students-print-a4-en.html` (sidorna 7–12)
- Ändra: `_unpublished/guides/ai-for-students/index.html` (motsvarande avsnitt)
- Ändra: `docs/guide-facts-ai-for-students.md` (Task 3:s UNESCO-post, Task 5:s
  regleringsposter, plus vaktrader)

**Gränssnitt:**
- Konsumerar: **Task 3:s UNESCO-post och Task 5:s regleringsposter.**
- Producerar: vaktrader för UNESCO-ramverket och regleringsavsnittets värden.

| sida | innehåll | vad uppgiften gör |
|---|---|---|
| 7 | Part 2-avdelare | rörs inte |
| 8 | "Teacher knowledge isn't a bonus" | **UNESCO-ramverket** enligt Task 3 |
| 9 | källkritik, bias, hallucinationer | rörs bara om en post pekar dit |
| 10 | "Teachers don't need to know the tech better" | rörs bara om en post pekar dit |
| 11 | **GDPR och AI Act** | regleringen enligt Task 5, och felklassen nedan |
| 12 | **GDPR i praktiken / motsvarande regler annorstädes** | regleringen enligt Task 5 |

> **AMENDEMANG 2026-10-15, efter Task 5:s mätning och granskning.** Stycket nedan pekade ut
> FEL MENING. Planen rättas här i stället för att skicka en implementerare på en sann mening.
>
> Meningen *"Both apply, both are the teacher's and the school authority's responsibility,
> and neither can be postponed"* har `both`/`neither` syftande på de **två regelverken** i den
> föregående meningen — EU AI Act och GDPR — inte på artikel 4 kontra Annex III, som inte är
> introducerade i texten vid den punkten. Båda regelverken gäller faktiskt: AI Act sedan
> 2026-08-02, GDPR sedan länge. **Meningen är sann och ska inte röras** (inventeringens S27,
> verdikt `står`, med skälet skrivet i cellen).
>
> **Felklassen finns i det FÖLJANDE högriskstycket** (inventeringens S28, verdikt `falskt`),
> som framställer Annex III-högriskens dokumentations-, transparens- och granskningsplikter
> som bindande i dag. Mellan de två ligger hela icke-EU-avsnittet, en ny underrubrik och
> minimalrisk-meningen — de står **inte** i följd.

**Felklassen som ska rättas, enligt Task 5:s mätning:** högriskstycket på sidan 11
(inventeringens **S28**) framställer Annex III-plikter som bindande i dag. Artikel 4:s
AI-kunnighetsplikt gäller sedan **2 februari 2025** och är det enda som binder en skola nu;
Annex III-högrisk gäller från **2 december 2027**. Den motsatta varianten — att lägga
**leverantörens** förhandsplikter på skolan — är samma fel i andra riktningen. **Skriv
distinktionen explicit: vad som binder skolan i dag, och vad som binder den från ett datum.**
Två lindrigare fynd hör till samma sidor: guiden skriver `minimal risk` där AI Act säger
`Minimal or no risk` (S29), och den nämner DPIA/artikel 35 men aldrig artikel 27:s FRIA (S30).

- [ ] **Steg 1: Mät sidornas luft före, samma skript som Task 7 steg 1 med sidorna 8, 11, 12**

- [ ] **Steg 2: Läs Task 3:s och Task 5:s källceller ordagrant**

- [ ] **Steg 3: Rätta på båda ytorna**

**Observera divergensen:** rubriken *"GDPR in practice (EU) / equivalent data protection
rules elsewhere"* finns bara på printytan. Rätta sakinnehållet på båda ytorna där det finns,
och **skriv divergensen i inventeringens prosa** — rundan ska inte tysta jämna ut den, och
inte heller tysta låta den växa.

- [ ] **Steg 4: Skriv vaktraderna**

Datum och artikelnummer är korta, stabila värden och är därför goda ankare:
`2 February 2025`, `2 December 2027`, `Article 4`. **Inte** hela satsen de står i.

- [ ] **Steg 5: Kör ytkontrollen, hela sviten, och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
/usr/bin/python3 -m pytest scripts/tests -q
git add -f docs/guide-facts-ai-for-students.md
git add _unpublished/exports/ai-for-students-print-a4-en.html \
        _unpublished/guides/ai-for-students/index.html
git commit -m "fix(students): Del 2 — UNESCO-ramverket och regleringen"
```

---

### Task 9: Del 3 — sidorna 13 till 16

Rundans tyngsta innehållsuppgift, och den enda vars omfång beror på ett beslut Johan tog vid
grinden.

**Filer:**
- Ändra: `_unpublished/exports/ai-for-students-print-a4-en.html` (sidorna 13–16)
- Ändra: `_unpublished/guides/ai-for-students/index.html` (motsvarande avsnitt)
- Ändra: `docs/guide-facts-ai-for-students.md` (Task 3:s fyra 1:1-poster, Task 4:s sex
  produktposter, plus vaktrader)

**Gränssnitt:**
- Konsumerar: **Task 3:s 1:1-citat, Task 4:s produktmätning, och Johans beslut vid grinden.**
- Producerar: vaktrader för 1:1-citaten och för de produktpåståenden som står kvar.

| sida | innehåll | vad uppgiften gör |
|---|---|---|
| 13 | Part 3-avdelare | rörs inte |
| 14 | 1:1-eran | **PISA 2015, Carter 2017, Zheng 2016, Unos Uno** enligt Task 3 |
| 15 | **The visibility gap** | produktpåståendena enligt Task 4 **och Johans beslut** |
| 16 | klassrumshantering | hänger på sidan 15; rättas i samma svep om slutsatsen flyttar |

**Sidan 14 bär fyra citat på en sida.** Faller ett av dem räcker det inte att ta bort
meningen: stycket bygger en kedja ("the research record is clear and internationally
consistent"), och en kedja med ett led borta påstår fortfarande att leden är fler än de är.
**Läs hela stycket efter varje borttagning och se att det som står kvar är sant.**

**Sidan 15 har två möjliga utfall, och Johan har valt ett vid grinden:**
- **Utsagan står:** rätta bara de enskilda produktpåståendena — marknadsledarna utan
  rangordning om den är `obelagt`, Copilots modellpåstående, och produktnamnen. Avsnittets
  slutsats står.
- **Utsagan faller:** avsnittet skrivs om enligt Johans beslut vid grinden. **Hitta inte på
  en ny slutsats** — skriv den han gav.

- [ ] **Steg 1: Mät sidornas luft före, sidorna 14, 15, 16**

- [ ] **Steg 2: Läs Task 3:s och Task 4:s källceller, och Johans beslut**

- [ ] **Steg 3: Rätta sidan 14 på båda ytorna, och läs hela stycket efteråt**

- [ ] **Steg 4: Rätta sidan 15 enligt beslutet, på båda ytorna**

- [ ] **Steg 5: Läs sidan 16 mot den nya sidan 15**

Klassrumshanteringsavsnittet argumenterar utifrån visibility-utsagan. Flyttade den, flyttar
det här avsnittets premiss — läs det och rätta det som inte längre följer.

- [ ] **Steg 6: Skriv vaktraderna**

```
# Elevguiden Task 9 — Del 3: 1:1-eran och produktlandskapet
S0n | en | 0.18 standard deviations | aktiv
S0n | en | 11 municipalities | aktiv
S0n | en | Copilot is built on ChatGPT | borttaget
```
Produktnamn som står kvar får `aktiv`-rader på **namnet**, inte på meningen om det.

- [ ] **Steg 7: Kör ytkontrollen, hela sviten, och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
/usr/bin/python3 -m pytest scripts/tests -q
git add -f docs/guide-facts-ai-for-students.md
git add _unpublished/exports/ai-for-students-print-a4-en.html \
        _unpublished/guides/ai-for-students/index.html
git commit -m "fix(students): Del 3 — 1:1-citaten och produktlandskapet"
```

---

### Task 10: Checklistan och FAQ:n — sidorna 17 till 21

**Filer:**
- Ändra: `_unpublished/exports/ai-for-students-print-a4-en.html` (sidorna 17–21)
- Ändra: `_unpublished/guides/ai-for-students/index.html` (motsvarande avsnitt)
- Ändra: `docs/guide-facts-ai-for-students.md` (Task 5:s FAQ-poster, plus vaktrader)

**Gränssnitt:**
- Konsumerar: Task 5:s regleringsposter, och vad Task 8 skrev på sidorna 11–12.
- Producerar: vaktrader för FAQ:ns regleringssvar.

| sida | innehåll | vad uppgiften gör |
|---|---|---|
| 17 | Part 4-avdelare | rörs inte |
| 18 | checklistan: pedagogik, förutsättningar | läs mot Del 1–2:s nya text |
| 19 | checklistan: tillsyn, uppföljning | **tillsynsfrågan bygger på visibility-utsagan** — läs mot sidan 15 |
| 20 | FAQ, första halvan | läs mot det som ändrats |
| 21 | FAQ, andra halvan | **AI Act-svaret och DPIA-svaret** enligt Task 5 |

**Checklistan och FAQ:n är guidens två sammanfattande ytor, och därför de som tystast bär
kvar ett påstående rundan rättat någon annanstans.** Samma mönster som fällde Apple-rundan
tre gånger: en rättelse i ett kapitel, en gammal formulering kvar i FAQ:n. Läs varje
checklistfråga och varje FAQ-svar mot vad Task 7–9 faktiskt skrev — inte mot vad planen sa
att de skulle skriva.

**Sidan 19:s tillsynsfråga** lyder i dag *"Do I have visibility into what students are asking
the AI during the lesson — at least afterwards?"* Står visibility-utsagan kvar är frågan
oförändrad. Föll den, är frågan fortfarande rimlig men dess premiss är ny: läs den och rätta
det som inte följer.

- [ ] **Steg 1: Lista varje påstående i checklistan och FAQ:n som Task 7–9 rörde**

```bash
/usr/bin/python3 - <<'PY'
import re, subprocess
out = subprocess.run(["pdftotext","-layout",
  "_unpublished/assets/pdfs/guides/ai-for-students-en.pdf","-"],
  capture_output=True, text=True, check=True).stdout
pages = out.split("\f")
for n in (18,19,20,21):
    print("=== sida", n, "===")
    print(" ".join(pages[n-1].split())[:1800], "\n")
PY
```
Kör mot den **nuvarande** PDF:en, alltså före omrenderingen, och jämför mot arbetsträdets
HTML — det är skillnaden mellan dem som är rundans ändringar så här långt.

- [ ] **Steg 2: Rätta på båda ytorna**

- [ ] **Steg 3: Skriv vaktraderna för FAQ:ns regleringssvar**

- [ ] **Steg 4: Kör ytkontrollen, hela sviten, och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
/usr/bin/python3 -m pytest scripts/tests -q
git add -f docs/guide-facts-ai-for-students.md
git add _unpublished/exports/ai-for-students-print-a4-en.html \
        _unpublished/guides/ai-for-students/index.html
git commit -m "fix(students): checklistan och FAQ:n lästa mot rundans rättelser"
```

---

### Task 11: Omslaget, sidfoten och datumstämpeln — sidorna 1 och 22

**Filer:**
- Ändra: `_unpublished/exports/ai-for-students-print-a4-en.html` (omslaget rad ~295–307,
  sidfotsraden i slutet — **grepa fram raderna, lita inte på numren**)
- Ändra: `_unpublished/guides/ai-for-students/index.html` (titel, `<title>`, CTA-finprint)
- Läsa: `exports/build-ai-for-elever-pdf.py` (sidfotsmallen)
- Ändra: `docs/guide-facts-ai-for-students.md` (en post för datumstämpeln)

**Gränssnitt:**
- Konsumerar: Task 6:s slutsats om läsartilltalet.
- Producerar: guidens slutliga titel och underrubrik, som Task 13:s förbudslista ankrar mot.

**Johans beslut (spec §4), och specens förslag som han godkände:**
- **Titeln behålls som frågan** `Should students use AI in class?` — avviker avsiktligt från
  systerguidernas `… for teachers and school leaders`.
- **Eyebrow står kvar:** `Pedagogical decision guide`.
- **Underrubriken byter läsare:** `for teachers and school leaders` → `for educators`.
  **Det här är guidens enda förekomst av den gamla etiketten** (mätt: sida 1, en gång).

**Datumstämpeln står på tre ställen** (mätt): printytan två gånger — en i omslagets
`cover__footer` och en i den löpande sidfoten — och webbytan en gång, i CTA:ns finprint.

- [ ] **Steg 1: Grepa fram varje förekomst, på båda ytorna och i byggaren**

```bash
grep -n "April 2026" _unpublished/exports/ai-for-students-print-a4-en.html \
                     _unpublished/guides/ai-for-students/index.html
grep -n "April 2026\|Updated\|footer" exports/build-ai-for-elever-pdf.py | head -20
grep -n "teachers and school leaders" _unpublished/exports/ai-for-students-print-a4-en.html \
                                      _unpublished/guides/ai-for-students/index.html
```
**Byggaren är en femte yta.** Gemini-rundans sidfot bar det pensionerade produktnamnet på 43
av 44 sidor, hårdkodat i Python, och upptäcktes först när den renderade PDF:en lästes. Läs
`jobs`-listan och `cover_footer`/`standard_footer` innan du antar att sidfoten bor i HTML.

- [ ] **Steg 2: Byt underrubrikens läsare, på båda ytorna där den står**

- [ ] **Steg 3: Ersätt datumstämpeln**

Skriv **ingen** ny månad som inte är sann vid leverans. Säkraste formen är den de andra
guiderna landade på — grepa fram vad `copilot-print-a4-en.html` och
`apple-intelligence-print-a4-en.html` skriver i dag och följ det, så alla fyra guider bär
samma form.

- [ ] **Steg 4: Skriv posten för datumstämpeln, med `April 2026` som `borttaget`-rad**

- [ ] **Steg 5: Kör ytkontrollen, hela sviten, och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
/usr/bin/python3 -m pytest scripts/tests -q
git add -f docs/guide-facts-ai-for-students.md
git add _unpublished/exports/ai-for-students-print-a4-en.html \
        _unpublished/guides/ai-for-students/index.html
git commit -m "fix(students): omslaget talar till educators, och datumstämpeln är borta"
```

---

### Task 12: Webbytan — typsnitten och den döda nedladdningsknappen

Den enda uppgiften som rör design i egen rätt, och den enda vars fel bara finns på webbytan.

**Filer:**
- Ändra: `_unpublished/guides/ai-for-students/index.html` (Google Fonts-`<link>`, rad 34;
  CTA-blocket kring rad 450)
- Ändra: `_unpublished/guides/ai-for-students/styles.css` (rad 23–24,
  `--font-display` / `--font-body`)
- Läsa: `_unpublished/guides/ai-for-students/script.js` (rad 27, `sectionIds`)
- Läsa som referens: `_unpublished/guides/apple-intelligence/index.html` och dess `styles.css`

**Gränssnitt:**
- Konsumerar: inget.
- Producerar: en webbyta som kan stå i `test_fonts.GUIDE_WEB_SURFACES`, vilket Task 13 gör.

**Två fel, mätta:**

1. **Crestiora-typsnitten.** `index.html` rad 34 laddar `Playfair Display` + `Inter` från
   Google Fonts, och `styles.css` rad 23–24 sätter dem som `--font-display` respektive
   `--font-body`. Blueprint är **Hanken Grotesk** som enda typsnitt, med **Instrument Serif**
   enbart i citat. **Kopiera inte värdena ur den här planen — läs dem ur Apple-guidens
   webbyta**, som är städad och är facit.
2. **En nedladdningsknapp som inte gör något.** CTA:n lovar *"Download the portable PDF —
   same content, premium layout, perfect for offline reading or for sharing with colleagues"*
   och knappen är en `<button>` **utan href och utan handler**. PDF:en publiceras inte —
   guiden distribueras via Skool — så löftet kan inte infrias och ska bort. Samma felklass som
   Apples struckna *"download the 25-page premium PDF from the same page"*.

**Knappen sitter i en navigerad sektion.** `script.js` rad 27 listar
`['part-1','part-2','part-3','faq','download']`. Tas sektionen bort måste `download` ur
listan, annars pekar scrollspionen på ett id som inte finns.

- [ ] **Steg 1: Läs Apple-guidens webbyta och ta typsnittsraderna därifrån**

```bash
grep -n "fonts.googleapis\|font-display\|font-body\|Hanken\|Instrument" \
  _unpublished/guides/apple-intelligence/index.html \
  _unpublished/guides/apple-intelligence/styles.css | head -20
```

- [ ] **Steg 2: Byt typsnitten på webbytan**

Både `<link>`-raden och de två CSS-variablerna. Blir någon regel kvar som pekar på ett
borttaget typsnitt är sidan trasig på ett sätt ingen textvakt ser — **grepa efter `Playfair`
och `Inter` i båda filerna efteråt och kräv noll träffar.**

- [ ] **Steg 3: Ta bort CTA-sektionen, och dess id ur `script.js`**

Finprinten `Updated April 2026.` i samma block ägs av Task 11 — är den redan borta, rör den
inte; står den kvar, tar den här uppgiften bort hela blocket den satt i och säger det i
committen.

- [ ] **Steg 4: Verifiera att inget pekar på den borttagna sektionen**

```bash
grep -n "download" _unpublished/guides/ai-for-students/index.html \
                   _unpublished/guides/ai-for-students/script.js \
                   _unpublished/guides/ai-for-students/styles.css
grep -n "Playfair\|Inter" _unpublished/guides/ai-for-students/index.html \
                          _unpublished/guides/ai-for-students/styles.css
```
Förväntat: noll träffar på `Playfair`/`Inter`, och ingen kvarvarande referens till
`download`-sektionen — varken i nav, scrollspion eller CSS.

- [ ] **Steg 5: Kör sviten och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests -q
git add _unpublished/guides/ai-for-students/
git commit -m "fix(students): webbytan till Blueprint, och det tomma nedladdningslöftet bort"
```

---

### Task 13: Kartorna fylls — fyra rader som tar in guiden i vaktlagret

**Filer:**
- Ändra: `scripts/tests/surfacecheck.py` (`GUIDE_SURFACES`, kring rad 22)
- Ändra: `scripts/tests/factinventory.py` (`INVENTORIES`, kring rad 14)
- Ändra: `scripts/tests/test_guide_delivery.py` (`GUIDE_DELIVERY`, kring rad 29)
- Ändra: `scripts/tests/test_fonts.py` (`GUIDE_WEB_SURFACES`, kring rad 73)

**Gränssnitt:**
- Konsumerar: inventeringen (Task 1–11) och den städade webbytan (Task 12).
- Producerar: guiden `ai-for-students` känd av fyra vakter. Task 15 river skuldlistan först
  när det här är grönt.

**Inget nytt vaktlager byggs.** Allt är guide-agnostiskt sedan Copilot-, Gemini- och
Apple-rundorna. **Kopiera formen ur en befintlig post, inte ur den här planen.**

**Fyra saker som skiljer den här guiden från syskonen, och var och en är ett konkret val:**

1. **`GUIDE_SURFACES`: bara de två engelska ytorna, eller också de svenska?** Apples post bär
   alla fyra, med skälet skrivet i en kommentar: de svenska ytorna **finns**, och en svensk
   vaktrad ska jämföras mot dem och inte mot ingenting. Elevguidens svenska yta är **fryst och
   har inga poster** — men den finns. **Ta med den, med samma kommentar**, och lägg aldrig en
   svensk vaktrad i inventeringen.
2. **`GUIDE_DELIVERY`: `pdfs` bär EN fil.** `ai-for-students-en.pdf`. Ingen quick-start, och
   **ingen post i `NO_PAGE_CLAIM`** (dicten är tom och ska förbli det — kommentaren vid den
   förklarar varför dess `skipped`-rad är förväntad; **rör den inte**).
3. **`untouched` bär de två svenska filerna:** `ai-for-elever-sv.pdf` och den svenska
   printytan. Byggaren renderar EN och SV i samma körning, så vakten är det som fäller den som
   committar en byte-ändrad svensk fil.
4. **`forbidden` fylls med guidens egna strängar**, och var och en **mäts på noll i den
   renderade PDF:en innan den skrivs in**:

```
"Download the portable PDF", "Download the guide (PDF)",
"same content, premium layout", "April 2026",
"teachers and school leaders",
```
Plus varje tal och attribution som Task 7–9 strök. **Regeln ur Apple-rundan: en lång sträng
som innehåller en kort förbjuden är strikt svagare än den korta** — en återinföring träffar
alltid den korta först. Ankra på det korta värdet.

- [ ] **Steg 1: Fyll `INVENTORIES` och kör dess vakt**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q -k inventory
```
Förväntat: grönt. Rött med "inventeringsfil saknas" betyder felstavad sökväg.

- [ ] **Steg 2: Fyll `GUIDE_SURFACES` och kör ytvakten**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_guide_surface_consistency.py -q
```
Förväntat: grönt för alla fem guider. Rött på `saknas_på_en_yta` betyder att en `aktiv`-rad
står på bara en yta — **laga texten, inte raden.**

- [ ] **Steg 3: Mät varje förbjuden sträng i den renderade PDF:en, och fyll `GUIDE_DELIVERY`**

```bash
/usr/bin/python3 - <<'PY'
import subprocess
pdf = subprocess.run(["pdftotext","-layout",
  "_unpublished/assets/pdfs/guides/ai-for-students-en.pdf","-"],
  capture_output=True, text=True, check=True).stdout
for s in ("Download the portable PDF", "Download the guide (PDF)",
          "same content, premium layout", "April 2026",
          "teachers and school leaders"):
    print(f"{s!r}: {pdf.count(s)}")
PY
```
**Kör det här EFTER Task 14:s omrendering** om någon sträng ännu står kvar i den gamla
PDF:en — en förbudsrad som fälls av en inaktuell PDF är inte ett fel i listan.

- [ ] **Steg 4: Fyll `GUIDE_WEB_SURFACES` med webbytan och dess CSS, och kör typsnittsvakten**

```bash
/usr/bin/python3 -m pytest scripts/tests/test_fonts.py -q
```

- [ ] **Steg 5: Bryt varje ny vakt med flit**

En vakt som inte setts bli röd vaktar ingenting. Minst tre brytningar, var och en återställd
direkt:
- skriv tillbaka `Playfair Display` i `styles.css` → typsnittsvakten ska fälla;
- skriv in `April 2026` i printytan, rendera om, kör leveransvakten → förbudslistan ska fälla;
- ta bort en `aktiv`-rads sträng ur EW → ytvakten ska säga `saknas_på_en_yta`.

**En HTML-kommentar duger inte som brytning** — `_TAG`-regexen slukar den.

- [ ] **Steg 6: Kör hela sviten och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests -q
git add scripts/tests/surfacecheck.py scripts/tests/factinventory.py \
        scripts/tests/test_guide_delivery.py scripts/tests/test_fonts.py
git commit -m "test(students): guiden in i fyra kartor, förbudslistan mätt"
```

---

### Task 14: Omrenderingen, sidantalet och facit

**Filer:**
- Kör: `exports/build-ai-for-elever-pdf.py`
- Ändra: `_unpublished/assets/pdfs/guides/ai-for-students-en.pdf` (utdata)
- Ändra: `scripts/tests/test_capture_guide_baseline.py` (`RECAPTURED_THIS_ROUND`)
- Ändra: `scripts/tests/fixtures/guide-pdf-baseline.json` och
  `guide-pdf-body-baseline.json` (via omfångningsskriptet, aldrig för hand)
- Ändra: `docs/guide-facts-ai-for-students.md` (sidkartan uppdateras med nya tal)

**Gränssnitt:**
- Konsumerar: allt innehållsarbete, Task 6–12.
- Producerar: den levererade PDF:en och ett omfångat facit. Task 15 och 16 mäter mot den.

**Stoppvillkoret, rättat enligt specens amendemang:** sidantalet får röra sig, men **ingen
sida under 400 tecken utom omslaget och de fyra avdelningssidorna** (sidorna 3, 7, 13 och 17 i
dagens paginering — de ligger på 712, 257, 237 och 184 tecken och är korta med avsikt).
**Mät med kollapsade blanktecken, aldrig borttagna** — den buggen gav fel siffror två gånger i
Gemini-rundan.

- [ ] **Steg 1: Kopiera undan de svenska filerna**

```bash
cp _unpublished/assets/pdfs/guides/ai-for-elever-sv.pdf /tmp/ai-for-elever-sv.pdf.bak
```
**Aldrig `git checkout --` på en katalog.** Det har kostat två av Johans filer en gång.

- [ ] **Steg 2: Rendera om**

```bash
/usr/bin/python3 exports/build-ai-for-elever-pdf.py
```
Byggaren renderar EN **och** SV i samma körning utan språkargument.

- [ ] **Steg 3: Återställ den svenska filen och verifiera att den är byte-identisk**

```bash
cp /tmp/ai-for-elever-sv.pdf.bak _unpublished/assets/pdfs/guides/ai-for-elever-sv.pdf
git status --short _unpublished/assets/pdfs/guides/
```
Förväntat: **bara** `ai-for-students-en.pdf` ändrad.

- [ ] **Steg 4: Mät sidantal, tunna sidor och sidkartan**

```bash
/usr/bin/python3 - <<'PY'
import re, subprocess
out = subprocess.run(["pdftotext","-layout",
  "_unpublished/assets/pdfs/guides/ai-for-students-en.pdf","-"],
  capture_output=True, text=True, check=True).stdout
pages = [p for p in out.split("\f")]
real = [(i+1, len(re.sub(r"\s+"," ",p).strip())) for i,p in enumerate(pages)]
print("formfeed-sidor:", len(pages), "— varav tomma:", sum(1 for _,n in real if n==0))
for n, c in real:
    print(f"  s{n:>2} {c:>5} tkn")
PY
```
Jämför varje tal mot sidkartan i inventeringen. **Skriv in de nya talen där** — kartan är
nästa rundas utgångsläge, och en inaktuell karta är exakt den sorts siffra överlämningen
varnar för att ärva.

- [ ] **Steg 5: Töm och fyll om `RECAPTURED_THIS_ROUND`**

**Töms och fylls om — aldrig radvis tillägg.** En lista som bara växer slutar vakta något.
Den här rundan omfångar **en** fil:
```python
RECAPTURED_THIS_ROUND = [
    # Elevguidens runda 2026-10-NN: … (skriv vad som ändrades och vilka sidor)
    "_unpublished/assets/pdfs/guides/ai-for-students-en.pdf",
]
```

- [ ] **Steg 6: Omfånga facit med `--only`**

```bash
/usr/bin/python3 scripts/tests/fixtures/capture_guide_baseline.py \
  --only _unpublished/assets/pdfs/guides/ai-for-students-en.pdf
```
**`--force` är liktydigt med att slå av paritetsvakten för alla 22 nycklar.** Använd det inte.

- [ ] **Steg 7: Jämför facit före och efter — bildinventeringen ska vara identisk**

```bash
/usr/bin/python3 - <<'PY'
import json, subprocess
key = "_unpublished/assets/pdfs/guides/ai-for-students-en.pdf"
old = json.loads(subprocess.run(["git","show","HEAD:scripts/tests/fixtures/guide-pdf-baseline.json"],
      capture_output=True, text=True, check=True).stdout)[key]
new = json.load(open("scripts/tests/fixtures/guide-pdf-baseline.json"))[key]
print("sidor:", len(old["pages"]), "->", len(new["pages"]))
print("bildinventering identisk:", old["images"] == new["images"])
PY
```
Skiljer bildinventeringen sig har renderingen tappat eller bytt en bild — **fingeravtryck på
text är blinda för bilder, och en omrendering har tappat åtta fotografier en gång.** Stanna
och titta på dokumentet.

- [ ] **Steg 8: Titta på den renderade PDF:en**

Varje bild intill ändrad text, och varje sida rundan skrev på. En textkontroll kan inte se en
trasig figur.

- [ ] **Steg 9: Kör hela sviten och committa**

```bash
/usr/bin/python3 -m pytest scripts/tests -q
git add -f docs/guide-facts-ai-for-students.md
git add _unpublished/assets/pdfs/guides/ai-for-students-en.pdf \
        scripts/tests/test_capture_guide_baseline.py \
        scripts/tests/fixtures/guide-pdf-baseline.json \
        scripts/tests/fixtures/guide-pdf-body-baseline.json
git commit -m "build(students): omrendering, nytt sidantal, facit omfångat med --only"
```

---

### Task 15: Skuldlistan rivs — `UNMAPPED_GUIDE_SURFACES` och dess två vakter

Rundans sista kodarbete, och det enda som **tar bort** tester. Gör det sist, efter att Task 13
är grönt.

**Filer:**
- Ändra: `scripts/tests/test_guide_surface_consistency.py` (ta bort
  `UNMAPPED_GUIDE_SURFACES`, ta bort `test_the_debt_list_cannot_rot`, skriv om
  `test_every_unpublished_guide_web_surface_is_accounted_for`)

**Gränssnitt:**
- Konsumerar: Task 13:s ifyllda `GUIDE_SURFACES`.
- Producerar: ett vaktlager med en lista mindre att hålla aktuell.

**Strykningen är ett krav, inte en städning.** Listans eget huvud säger det: *"Är den tom ska
både listan och dess två vakter strykas — de vaktar ingenting då."* Elevguiden är dess enda
post.

**De två vakterna, och de ska behandlas olika:**
- `test_the_debt_list_cannot_rot` finns **bara** för listan → **stryks helt.**
- `test_every_unpublished_guide_web_surface_is_accounted_for` läser listan som undantag →
  **skrivs om** så att den mäter varje webbyta på disk mot `GUIDE_SURFACES` enbart. Den
  behålls: det är den vakt som gör att en ny guides webbyta syns utan att någon kommer ihåg
  att skriva upp den.

- [ ] **Steg 1: Spara test-id:n från `main` INNAN du ändrar något**

```bash
git stash list >/dev/null
/usr/bin/python3 -m pytest scripts/tests --collect-only -q > /tmp/ids-branch.txt
git stash push -u -m "tmp" >/dev/null 2>&1 || true
git switch main -q
/usr/bin/python3 -m pytest scripts/tests --collect-only -q > /tmp/ids-main.txt
git switch - -q
git stash pop >/dev/null 2>&1 || true
wc -l /tmp/ids-main.txt /tmp/ids-branch.txt
```
Går stash-dansen inte ihop: hoppa över den och jämför i stället mot
`git show main:scripts/tests/...`-körningen i en separat utcheckning. **Poängen är att ha
`main`-listan innan strykningen**, inte att göra just den här manövern.

- [ ] **Steg 2: Skriv om `test_every_unpublished_guide_web_surface_is_accounted_for`**

Den ska mäta `_guide_web_surfaces_on_disk()` mot ytorna i `GUIDE_SURFACES` — utan
undantagslista. Felmeddelandet ska säga vad man gör med en ny yta: kartlägg den i
`GUIDE_SURFACES` och skriv en inventering.

- [ ] **Steg 3: Ta bort `UNMAPPED_GUIDE_SURFACES` och `test_the_debt_list_cannot_rot`**

Blir en import eller hjälpfunktion oanvänd av strykningen — **ta bort den också.** Global
regel i det här repot.

- [ ] **Steg 4: Kör sviten och jämför test-id:n mot `main`**

```bash
/usr/bin/python3 -m pytest scripts/tests -q
/usr/bin/python3 -m pytest scripts/tests --collect-only -q > /tmp/ids-after.txt
diff /tmp/ids-main.txt /tmp/ids-after.txt
```
**Diffen ska vara exakt:** de borttagna raderna är `test_the_debt_list_cannot_rot` och
inget mer under den filen; de tillagda är de nya parametriseringarna för `ai-for-students`
(ytvakten, inventeringsvakten, leveransvakten, typsnittsvakten). **Står något annat i diffen
— stanna.** "Antalet ökade" duger inte som kontroll i en runda som tar bort tester med avsikt.

- [ ] **Steg 5: Committa**

```bash
git add scripts/tests/test_guide_surface_consistency.py
git commit -m "test: skuldlistan riven — elevguiden var dess sista post"
```

---

### Task 16: Helgranskning av grenen

**Filer:** inga ändras av den här uppgiften. Den mäter och rapporterar.

**Gränssnitt:**
- Konsumerar: hela grenen.
- Producerar: rapporten Johan läser före merge, och överlämningens nya avsnitt.

- [ ] **Steg 1: Kör sviten i en ORÖRD utcheckning, inte i arbetsträdet**

```bash
git worktree add /tmp/students-verify HEAD
cd /tmp/students-verify && /usr/bin/python3 -m pytest scripts/tests -q; cd -
git worktree remove /tmp/students-verify
```
Faller de elva i `test_prompt_pdf_parity.py`: återskapa `/tmp/pdf-parity-before/` enligt
testets egen felutskrift och kör om. **Rapportera talet med den filen inkluderad** när facit
finns — ett tal mätt med en exkluderad fil är inte sviten.

- [ ] **Steg 2: Kontrollera att inget publicerat rörts, och att inga rundartefakter smugit in**

```bash
git diff --name-only main..HEAD | grep -vE '^(_unpublished|docs|scripts)/' || echo "inget publicerat rört"
git ls-files .superpowers/ | head
```
Förväntat: tomt i båda. En implementerare har force-addat sin rapport under `.superpowers/`
en gång.

- [ ] **Steg 3: Verifiera de frysta svenska filerna mot merge-basen**

```bash
git diff --stat $(git merge-base main HEAD)..HEAD -- \
  _unpublished/assets/pdfs/guides/ai-for-elever-sv.pdf \
  _unpublished/exports/ai-for-students-print-a4-sv.html \
  _unpublished/exports/ai-for-elever-print-a4-sv.html
```
Förväntat: tomt. Allt annat är en frysning som läckt.

- [ ] **Steg 4: Räkna utfallsräkningen maskinellt och jämför mot inventeringens tabell**

Samma skript som i grinden. Står tabellen och raderna inte överens är tabellen fel —
**räkningen är aldrig fel, den är mätt.**

- [ ] **Steg 5: Läs PDF:en från pärm till pärm**

Leta tre saker: ett påstående rundan rättade på ett ställe men inte på ett annat, en figur
intill ändrad text, och en sida som blivit tunn.

- [ ] **Steg 6: Skriv rapporten**

Den ska innehålla: svitens tal i orörd utcheckning, sidantalet före och efter, utfallsräkningen,
varje tal och attribution som ströks med skälet, vad som föll vid grinden och vad Johan
beslutade, de nya vaktraderna, och **vad rundan medvetet INTE gjorde**.

- [ ] **Steg 7: Skriv överlämningens nya avsnitt**

`docs/blueprint-handoff.md` får ett avsnitt *"Elevguiden — vad rundan lämnar"* med samma form
som de tre föregående guidernas: var det står, vad som väntar på Johan, vaktläget efter
rundan, och lärdomarna för nästa runda. **Ersätt avsnittet "Elevguiden — specen skriven"**,
skriv inte ett andra avsnitt om samma guide.

```bash
git add -f docs/blueprint-handoff.md
git commit -m "docs(handoff): elevguiden — vad rundan lämnar"
```

---

## Självgranskning av planen, gjord 2026-10-14

**Specens täckning:** §1 → Task 13 (en PDF, ingen quick-start) och Task 14 (svenska frysta).
§2 → Task 1 (censusen) och sidkartan. §3 → Task 6 (läsaren), Task 7–10 (innehållet).
§4 → Task 11. §5 → globala villkor och varje innehållsuppgifts fillista. §6 klass 1 → Task 2
och 3; klass 2 → Task 4 och grinden; klass 3 → Task 5. §7 → Task 13 och 15. §8 → varje
uppgifts sista steg plus Task 16. §9 → Task 16 steg 6. **Ingen lucka hittad.**

**Varje sida har en ägare:** se sidkartan ovan. 22 av 22 sidor pekar ut en skrivande uppgift.

**Platshållare:** inga `TBD`. Tre ställen är avsiktligt öppna och det står varför: URL:erna i
Task 2 steg 1 (de ska hämtas, inte gissas), de nya vaktradernas exakta strängar (de beror på
vad mätningen visar) och datumstämpelns nya form (den ska läsas ur systerguiderna, inte ur
planen).

**Namnkonsistens:** `S01…Snn` som post-id i hela planen; `EP`/`EW` som ytbeteckningar;
`GUIDE_SURFACES`, `INVENTORIES`, `GUIDE_DELIVERY`, `GUIDE_WEB_SURFACES`,
`UNMAPPED_GUIDE_SURFACES`, `RECAPTURED_THIS_ROUND`, `NO_PAGE_CLAIM` — alla verifierade mot
koden 2026-10-14, med fil och ungefärlig rad i uppgiftens fillista.
