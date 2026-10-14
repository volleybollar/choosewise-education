# Helgranskningens fixvåg — slutrapport

**Datum:** 2026-10-14 · **Gren:** `feat/apple-guide-round-2` · **Utgångs-HEAD:** `42f88bb`
**Merge-bas mot `main`:** `1fea250`
**Omfång:** sex Important + fem Minor ur helgranskningen. Sista ändringen före leverans.
**Interpreter:** `/usr/bin/python3`

Ytbeteckningar: **EP** = `_unpublished/exports/apple-intelligence-print-a4-en.html`,
**EW** = `_unpublished/guides/apple-intelligence/index.html`,
**QS-en/QS-sv** = `_unpublished/exports/apple-intelligence-quick-start-{en,sv}.html`.

---

## IMPORTANT 1 — Den svenska quick-starten levererade två falska värden

Fil: `_unpublished/exports/apple-intelligence-quick-start-sv.html`. Tre åtgärder enligt
kontrollerns ruling, inget annat rört i filen.

### 1a. Åldersgränsen (källa: **A16**)

Före (Tänk på-rutan):

> Vissa funktioner är 18+; kontrollera nationella regler för elev-användning.

Efter, ordagrant:

> ChatGPT-vägen kräver att användaren är minst 13 år, eller den minimiålder som gäller i
> landet; kontrollera nationella regler för elev-användning.

**Källcell:** A16. `support.apple.com/guide/iphone/use-chatgpt-with-apple-intelligence-iph00fd3c8c2/ios`
→ 200, ordagrant 2026-10-14: *"You must be at least 13 years old or the minimum age required
in your country to consent to use ChatGPT."* Samma mening i den arkiverade primärkällan
(Wayback-capture 2026-04-17) — värdet var falskt redan i april, inte föråldrat.

Formuleringen är skriven som svensk prosa, inte översatt från den engelska tvillingen.
Systerguidernas svenska quick-starter lästes först som register-referens
(`gemini-notebooklm-quick-start-sv.html`: *"NotebookLM är 13+ i webbläsaren med strängare
regler under 18."*, `copilot-quick-start-sv.html`). Två saker togs därifrån: åldern knyts
till **vägen** (ChatGPT), inte till "funktioner" i allmänhet, och semikolonledet om
nationella regler står kvar oförändrat eftersom det redan var rätt.

### 1b. Funktion 2 — namnet och EU-spärren (källor: **A10** + **A15**)

Före:

> **Siri 2.0** — Kontextmedveten schemaläggning, hämta saker mellan appar. Nästan allt på
> enheten.

Efter, ordagrant:

> **Siri AI** — Kontextmedveten schemaläggning, hämta saker mellan appar. Nästan allt på
> enheten. Spärrad i EU på iPhone och iPad — Apple anger DMA som skäl, och ger ingen tidplan.

**Källceller:** A10 för namnet (fyra hämtade Apple-sidor namnger assistenten `Siri AI`;
`grep -i "Siri 2.0"` ger **noll** träffar i den hämtade HTML:en från alla fyra — Apple har
aldrig haft en produkt som heter `Siri 2.0`). A15 för de tre sakuppgifterna:

- **spärrad i EU på iPhone och iPad** — `apple.com/newsroom/2026/06/due-to-dma-siri-ai-delayed-in-eu-for-ios-27-and-ipados-27/`,
  ordagrant: *"users in the EU will not have access to Siri AI"* på *"iOS 27 and iPadOS 27"*;
- **DMA som Apples angivna skäl** — samma sida (DMA är sidans hela premiss);
- **ingen tidplan** — samma sida, ordagrant: *"there is currently no timeline for Siri AI's
  availability in the EU on iOS and iPadOS"*.

Ingen tidplan påstås, och ordet "senare" förekommer inte. Formuleringen följer den engelska
tvillingens struktur (*"Blocked in the EU on iPhone and iPad — Apple cites the DMA, no
timeline."*) men är skriven på svenska, inte översatt ord för ord.

### 1c. Inget annat rört

QS-sv:s punkt 3 på sida 2 (*"Fråga Siri om torsdagens schema"*) har **inte** fått den
EU-notis den engelska tvillingen bär. Det låg utanför rulingens tre punkter
("Rör ingenting annat i filen"). Se Farhågor nedan.

### 1d. Omrendering och omfångning

```
/usr/bin/python3 exports/build-apple-intelligence-quickstart-pdf.py
```

Byggaren renderar EN *och* SV i samma körning. Den **engelska** quick-starten är ändrad med
avsikt i den här vågen (Important 6) och återställdes därför inte — kravet i briefen gäller
byggarens icke-determinism, inte en avsiktlig ändring. Omfångning per ändrad PDF med
`--only`; **`--force` användes aldrig.**

### 1e. Vakthålet dokumenterat

Ny kommentar i `scripts/tests/test_guide_delivery.py`, i
`GUIDE_DELIVERY["apple-intelligence"]`, direkt efter `forbidden`-tupeln. Den säger de tre
sakerna briefen krävde:

1. **De svenska filerna läses inte av förbudslistan** — `pdfs` är de två engelska PDF:erna,
   och förbudsvakten läser bara dem. Varje sträng i listan (`Siri 2.0`, `18 or over`,
   `April 2026`, …) mäts alltså aldrig mot de svenska PDF:erna.
2. **Quick-starten rättades manuellt i den här fixvågen** — filen ligger inte i `pdfs` och
   dess PDF stod i `untouched` fram till Task 1, så ingen vakt läste den. En framtida runda
   som rättar ett engelskt värde måste själv fråga om QS-sv bär samma värde.
3. **Guide-sv:s prosa är fryst med avsikt och bär fortfarande `Siri 2.0`** — både
   `_unpublished/sv/guider/apple-intelligence/index.html` och
   `_unpublished/exports/apple-intelligence-print-a4-sv.html`. Att `Siri 2.0` står på
   förbudslistan betyder alltså **inte** att strängen är borta ur guiden; den är borta ur de
   två engelska PDF:erna. Kommentaren säger också vad som händer den dag de svenska PDF:erna
   tas in i `pdfs` utan att prosan först rättas (listan blir röd, vilket är rätt beteende).

Samma hål är beskrivet från inventeringshållet i vaktblockets nya avsnitt.

---

## IMPORTANT 2 — FAQ-fråga 9 bar aprilvägen

Fil: EP, FAQ-svaret *"Can I turn off specific features while keeping Writing Tools?"*.

Före:

> ChatGPT Extension has its own setting under Siri &amp; Apple Intelligence.

Efter, ordagrant:

> The ChatGPT path has its own setting under Settings → Siri → ChatGPT Extension.

**Källcell:** A30. `support.apple.com` ChatGPT-guiden → 200, nuvarande väg ordagrant:
*"Go to the Settings app on your iPhone. Tap Siri. Tap ChatGPT, tap Set Up …"* Den arkiverade
primärkällan (Wayback 2026-04-17) ger aprilvägen: *"Tap Apple Intelligence & Siri. Below
Extensions, tap ChatGPT, then tap Set Up."* EP bar alltså aprilvägen, ordvänd. Ordet
`Extensions` är Apples eget och behålls.

Vägen är nu densamma som EP:s egen sida 21 (*"Confirm Requests under Settings → Siri →
ChatGPT"*) och som EW:s FAQ-svar redan bar.

### Mätningen före beslutet om inventeringsrad

Mätt efter rättelsen med `surfacecheck.read_surfaces` + `normalise` (vaktens egen
normalisering, inte rå HTML):

| sträng | EW | EP |
|---|---|---|
| `Settings → Siri → ChatGPT Extension` | **1** | **1** |
| `Settings → Siri → ChatGPT` | 2 | 2 |
| `Siri & Apple Intelligence → ChatGPT Extension` (aprilvägen) | 0 | 0 |

### Valet, och varför

**Vald: `A30 | en | Settings → Siri → ChatGPT Extension | aktiv`.**

A30 var deklarerad EW-exklusiv av Task 7, och skälet var riktigt *då*: EP bar ingen
motsvarande instruktion alls, bara aprilvägen, så en rad som kräver ordagrann träff på båda
ytorna hade varit `saknas_på_en_yta` från första sekunden. Efter den här rättelsen står
strängen 1/1, och posten kan därför få sin första `aktiv`-rad.

Det **förkastade** alternativet var ett ankare på bara `Settings → Siri → ChatGPT`. Det var
redan 2/2 **före** rättelsen — A18:s två passager (EP:1096, EW:399) bär den strängen — alltså
hade en sådan rad varit grön även med aprilvägen kvar i FAQ:n. Den hade vaktat ingenting av
just det hålet granskningen fann. Den längre strängen är den som faktiskt blev sann av
rättelsen, och den enda som bryts om FAQ-svaret faller tillbaka.

EP-formuleringen ändrades från *"ChatGPT Extension has its own setting under …"* till
*"The ChatGPT path has its own setting under …"* för att undvika stammandet
"ChatGPT Extension … ChatGPT Extension" i samma mening, utan att röra vaktsträngen.

Följdändringar i inventeringen, så att dokumentet inte bär ett påstående som nu är falskt
(samma defektklass som Important 5):

- A30:s postrad: verdiktcellen inleds nu *"föråldrat — rättat, och sedan helgranskningens
  fixvåg inte längre EW-exklusivt"*, med förekomsten `1 / 0` uttryckligen märkt som runda 1:s
  mätning av den gamla strängen.
- Vaktblockets inledande kommentar: *"Samma skäl gällde A30 … **A30 är inte längre
  enytig**"*.
- Ytdivergenstabellens A30-rad: `**Löst:**`-not, raden står kvar som historik (samma mönster
  som IMY-raderna).
- Observation 6: *"Tre poster saknar vaktrad med avsikt"* → **två** (A31 + IMY), med A30
  utbruten i parentes enligt A32:s redan etablerade precedens i samma stycke.

---

## IMPORTANT 3 — A19:s inramning följde inte värdet

Filer: EP sida 4 och EW `#p1-setup`. Ordagrant samma stycke på båda ytorna före och efter.

Före:

> On a compatible iPad, the setup is short but the download is not. You toggle the feature on,
> and your iPad then pulls down on-device storage in the background: **up to 8 GB** on most
> supported iPads, or **up to 14 GB** on iPad models with M4 or later and at least 12 GB of
> unified memory. On decent school WiFi this takes thirty to sixty minutes. The settings panel
> will read "Preparing" during that window; you can keep using the iPad normally while it works.

Efter, ordagrant:

> On a compatible iPad, the setup is a single toggle, and the iPad then downloads its
> on-device models in the background. What Apple publishes is the storage the feature
> requires, not the size of that download: you need **up to 8 GB** on most supported iPads,
> or **up to 14 GB** on iPad models with M4 or later and at least 12 GB of unified memory.
> Apple gives no figure for how long the download takes, so plan around free space rather
> than a clock. The settings panel will read "Preparing" while it works; you can keep using
> the iPad normally.

**Källcell:** A19. `support.apple.com/en-us/121115` → 200, ordagrant: *"**Up to 14 GB of
storage on device** for iPhone 17 Pro, …"* och *"**Up to 8 GB of storage** for other Apple
Intelligence-enabled iPhone, iPad, Mac, and Apple Vision Pro models"*. Källan talar om
**diskutrymme**, inte om nedladdningens storlek — A19:s verdiktcell säger det själv och
noterar uttryckligen att guiden *"byggde en praktisk instruktion på den"*.

Två led, båda lagade:

1. **"pulls down on-device storage"** läste som att hela utrymmet laddas ned. Meningen skiljer
   nu uttryckligen *vad som laddas ned* (*"downloads its on-device models"*) från *vad som
   krävs i utrymme* (*"the storage the feature requires, not the size of that download"*).
2. **Tidsuppskattningen är borttagen utan ersättning.** `thirty to sixty minutes` var
   kalibrerad för den gamla 4 GB-siffran och stod nu intill Apples 8–14 GB-tak. **Ingen källa
   i inventeringen bär en nedladdningstid**, så inget nytt tal är skrivet in; i stället står
   frånvaron uttryckligen (*"Apple gives no figure for how long the download takes"*) med en
   användbar ersättning för läsaren (*"plan around free space rather than a clock"*). Även
   det inledande ledet *"the setup is short but the download is not"* föll — det var ett
   implicit varaktighetspåstående ur samma obelagda uppskattning.

De tre `aktiv`-raderna med Apples två tak är **orörda** och mätta 1/1 var efter ändringen.
Mac- och iPhone-stycket var redan rätt inramat (*"free disk space"*) och är orört.

A19:s postrad i inventeringen har fått en avslutande not om fixvågen, så att verdiktcellen
inte längre beskriver en instruktion guiden inte bär.

---

## IMPORTANT 4 — Uppstartssteget lovade en funktion EU-läsaren inte får

Filer: EP sida 4 och EW `#p1-setup`, steg 5 i `<ol class="steps">`. Identiskt på båda ytorna.

Före:

> When "Preparing" disappears, Writing Tools, the new Siri, and Mail categorisation are live.

Efter, ordagrant:

> When "Preparing" disappears, Writing Tools is live. Siri AI is not, on an EU iPad — Apple
> blocks it there. And Mail categorisation is a separate matter: Apple's own documentation
> never ties it to Apple Intelligence at all. Part 2 takes up both.

**Källceller:**

- **Siri-ledet: A15.** Spärren är EU-bred på iPhone och iPad
  (`apple.com/newsroom/2026/06/due-to-dma-…`, ordagrant *"users in the EU will not have access
  to Siri AI"*), och guidens egen callout på sidan 10 säger samma sak. Steget **pekar** till
  Del 2 i stället för att upprepa hela förbehållet — ingen ny sakuppgift införs, och A15:s
  ankare `the EU's Digital Markets Act` ligger kvar där det redan var ankrat. Namnet är
  `Siri AI`, inte `the new Siri`.
- **Mail-ledet: A07.** Apples sida
  (`support.apple.com/guide/iphone/use-categories-iphfe4a36baf/ios`) *"säger ingenting om var
  kategoriseringen körs, och nämner inte Apple Intelligence som krav"*. Guidens egen rättade
  hållning står på EW:262 (*"its support page never ties the feature to Apple Intelligence at
  all"*) och EP:863 (*"or that Apple Intelligence is required to use it"*).

**Medvetet val i formuleringen:** ett första utkast skrev *"Mail categorisation never depended
on this switch: Apple does not tie it to Apple Intelligence."* Det bytte ett obelagt påstående
mot ett annat — att huvudreglaget mekaniskt inte styr kategoriseringen är en slutsats ingen
hämtad källa bär. Den levererade texten **rapporterar** i stället vad Apples dokumentation
inte säger, vilket är exakt A07:s verdikt. Ingen ny vaktrad: steget påstår inget nytt
sakvärde.

---

## IMPORTANT 5 — Inventeringens utfallsräkning var föråldrad

Fil: `docs/guide-facts-apple-intelligence.md`, `## Utfallsräkningen`. Tre rättelser.

### 5a. Sektionens inledning (överclaimen)

Före:

> … Efter runda 2:s Task 2–11 beskriver samtliga 39 **den omskrivna guiden**: verdiktkolumnen
> bär klassificeringen och, för varje post runda 2 har rört, vad som gjordes med den.

Efter, ordagrant:

> … Samtliga 39 beskriver **inte** den omskrivna guiden, och får inte läsas så — dokumentets
> huvud säger samma sak: i de flesta cellerna står verdiktet kvar som runda 1 klassificerade
> det, och bara en del av cellerna är uppdaterade med vad runda 2 gjorde. **Vaktblocket är den
> auktoritativa källan** för vad som faktiskt ändrades.

Detta är exakt den överclaim Task 12:s fixrunda rättade i dokumentets huvud (rad 20–38:
*"var inte en beskrivning av den omskrivna guiden … i de allra flesta cellerna är det
verdiktet fortfarande runda 1:s ursprungliga klassificering"*). Sektionen sa motsatsen.

### 5b + 5c. De två falska påståendena om A06 och A07

Före:

> **Två av kvalifikatorerna är spärrar, inte dekoration.** `står (delvis obelagt)` på **A07**
> får inte läsas som att Mail-kategoriseringens on-device-påstående är belagt — det är det
> inte, och det står i DPIA-kapitlet. `står (EU-förbehåll saknas)` på **A06** får inte läsas
> som att Visual Intelligence-avsnittet är klart — Apple har skrivit ut EU-svaret och guiden
> bär det inte.

Efter, ordagrant:

> **Två av kvalifikatorerna var spärrar, inte dekoration — och båda är åtgärdade i runda 2.**
> `står (delvis obelagt)` på **A07** gällde att Mail-kategoriseringens on-device-påstående
> inte var belagt, i DPIA-kapitlet. Påståendet **står inte längre någonstans i guiden**: Task 6
> strök rutans två superlativfraser och Task 7:s Fixrunda 1 de två bredare påståendena i Del 1
> och Del 3 — fyra `borttaget`-rader i vaktblocket. `står (EU-förbehåll saknas)` på **A06**
> gällde att Apple hade skrivit ut EU-svaret utan att guiden bar det. **Guiden bär det nu:**
> callouten `The expanded layer is blocked in the EU` (sidan 15), ankrad som
> `an expanded Visual Intelligence experience`. Kvalifikatorerna står kvar i cellerna därför
> att de redovisar runda 1:s mätning — läs dem som historik över vad som behövde göras, inte
> som öppna brister.

Belägg för de två: A07:s fyra `borttaget`-rader i vaktblocket (`no email content is sent to
Apple servers`, `cleanest privacy profile in the entire Apple Intelligence suite`, `Mail
categorisation and notification summaries are entirely on-device`, `Mail categorisation, and
Notification summaries. Nothing leaves the device.`) — alla gröna, alltså frånvarande på båda
ytorna. A06:s callout mätt på plats: EP:957–958 och EW:339, ankaret `an expanded Visual
Intelligence experience` 1/1.

Kvalifikatorerna i postcellerna (`står (öppen EU-fråga)` etc.) är **inte** omklassificerade —
omklassificering är uttalat utanför den här vågens omfång, och tokentabellens summa
(13 + 5 + 5 + 3 + 5 + 8 = 39) är oförändrad.

---

## IMPORTANT 6 — Engelska quick-starten saknade två förbehåll

Fil: `_unpublished/exports/apple-intelligence-quick-start-en.html`. Styrkan är satt **per
post**, inte lika — det var hela poängen i fyndet.

### Funktion 1 · Writing Tools (**A05** = `står (öppen EU-fråga)`)

Efter, ordagrant (tillägget är den sista meningen):

> Rewrite, proofread, summarise. Grading comments, parent emails, lesson plans. Most
> on-device. EU status unconfirmed: Apple's DMA notice blocks "integrated tools for writing"
> without saying whether that means Writing Tools.

**Källcell:** A05/A06 delar Apple-meningen: `apple.com/newsroom/2026/06/due-to-dma-siri-ai-delayed-in-eu-for-ios-27-and-ipados-27/`
→ 200 (curl), ordagrant *"…including the new dedicated app to revisit conversations, an
expanded Visual Intelligence experience, **integrated tools for writing**, Siri mode in Camera
on iOS, and other Siri AI capabilities…"*. A05:s cell säger att frågan **går inte att avgöra
ur den hämtade texten**.

Status är **obekräftad**, inte spärrad, och **ingen av tolkningarna påstås** (varken att det
är guidens `Writing Tools` eller att det bara är Siri AI:s egen skrivintegration).
Komprimering av guidens egen callout på sidan 9 (EP:761–762, *"Possibly affected by the EU
restriction"* / *"treat Writing Tools' status on an EU iPad as unconfirmed rather than
assuming it works"*). Inget uppfunnet.

### Funktion 6 · Visual Intelligence (**A06** = `står (EU-förbehåll saknas)`)

Efter, ordagrant (tillägget är den sista meningen):

> Point the camera at text or objects for translation, summaries, context. Apple's DMA notice
> blocks the "expanded" layer in the EU and says nothing about the basic one — verify locally
> before building a lesson on it.

**Källcell:** A06, samma Apple-mening, ordagrant *"an expanded Visual Intelligence
experience"*. Det **utvidgade** lagret är spärrat; det **grundläggande** är inte omnämnt av
Apple. Komprimering av guidens callout på sidan 15 (EP:957–958, *"The expanded layer is
blocked in the EU"* / *"Apple does not say how much of the basic recognition and translation
below survives … verify locally before building a lesson around them"*).

Typografi: de två tilläggen skrevs först med typografiska citattecken och är normaliserade
till **raka** citattecken — de var de enda två krokiga i hela Apple-korpusen (EP 0, EW 0,
QS-en nu 0).

---

## FEM MINOR

### Minor 1 — `Siri itself` på sidan 5 (båda ytorna)

Före:

> One clarification before the three: Apple has said Siri itself is built "in collaboration
> with Google and its Gemini models" — that partnership runs through the first two tiers below,
> not as a fourth path alongside them.

Efter, ordagrant:

> One clarification before the three: Apple has said Siri AI is built "in collaboration with
> Google and its Gemini models" — Apple does not say where that partnership sits, and the most
> likely reading is that it runs through the first two tiers below rather than as a fourth path
> alongside them.

Två saker: ordet `Siri itself` generaliserade Apples uttalande om **Siri AI** till Siri i
allmänhet — alltså även till den klassiska Siri som är det enda en EU-läsare har — och ledet
om de två nivåerna påstod inventeringens egen slutledning som faktum. Det är nu hedgat.

**Källcell:** A17 (och huvudets lead 2), Apple Newsroom ordagrant: *"custom-built in
collaboration with Google and its Gemini models"*. A17:s vaktsträng `in collaboration with
Google and its Gemini models` står ordagrant kvar, mätt 1/1 efter ändringen.

### Minor 2 — `remains blocked` → `is blocked` (EP sida 17)

> … Siri AI finds last term's lesson plan without you scrolling through Notes — not on an EU
> iPad, where Siri AI **is** blocked (see the Siri AI entry earlier in this Part).

Matchar nu sidan 10:s register. Det var det sista hedge-ordet i hela PDF:en. EP-ensam passage
(EW har ingen motsvarande sammanfattande sida) — ingen vaktrad möjlig, samma skäl som
IMY/A31.

### Minor 3 — EW påstod utgångsläget baklänges

Före: `… and switch it on — there's no default to rely on here.`
Efter, ordagrant: `… and switch it on.`

**Källcell:** A29, verdikt `obelagt`: *"ingen hämtad sida säger att sammanfattningar är på som
standard"* och *"ingen hämtbar sida uttalar sig om defaulten"*. Planens instruktion är att
inte påstå utgångsläget. EP gjorde det redan rätt (*"and turn the feature on"*). A29 har med
avsikt ingen ersättande `aktiv`-rad — kapitlet pekar bara till var inställningen bor.

### Minor 4 — EW:s Siri-callout tappade EP:s villkor

Efter, ordagrant (ny inledning på sista meningen):

> Apple has blocked Siri AI in the EU on iPhone and iPad. The stated reason is the EU's
> Digital Markets Act, and Apple has not published a timeline. **If your school's iPads are in
> the EU,** the classroom examples below describe a feature you cannot use.

Villkoret är EP:803:s ordagranna formulering. Rutan är inte längre obetingad.

### Minor 5 — Död referens

`scripts/tests/test_guide_delivery.py`, docstringen i
`test_the_no_page_claim_list_cannot_rot`. `MEASURE_ONLY_INVENTORIES` ströks i rundans andra
uppgift (verifierat: enda kvarvarande förekomsten i kod är den här docstringen; i övrigt bara
historiknoten i `test_guide_surface_consistency.py:264` och planfilerna). Rättad till den
levande syskondeklarationen, med namnets historik bevarad:

> … Samma form som UNMAPPED_GUIDE_SURFACES i test_guide_surface_consistency.py
> (MEASURE_ONLY_INVENTORIES, som stod här som andra exempel, ströks i runda 2 Task 2 — se den
> filens historiknot).

### Lämnat orört enligt instruktion

- `skolchef`/`rektor` på EP — ägarens redaktionella pass. Diffen visar fyra ändrade rader i
  EP, ingen av dem i de passagerna.
- Task 15:s `worth`-räkning — en rapportsiffra, ingen fil rörd.
- De svenska **guideytornas** prosa — orörd; `apple-intelligence-guide-sv.pdf` är
  byte-identisk (se nedan).

---

## Omrendering, återställning, omfångning

```
/usr/bin/python3 exports/build-apple-intelligence-pdf.py
/usr/bin/python3 exports/build-apple-intelligence-quickstart-pdf.py
```

Kördes om efter varje textjustering; sista körningen är den som räknas.

**`apple-intelligence-guide-sv.pdf` — byte-status.** Byggaren skriver den varje körning
(rapporterar "5865 KB"), men filen kom ut **byte-identisk varje gång**. SHA-256 på disk:
`6506ec78539cd840deca19b7cad66eb801ee70c6d7487853e7d2d80765a56c78`, identisk med
`git show 1fea250:_unpublished/assets/pdfs/guides/apple-intelligence-guide-sv.pdf | shasum -a 256`
(merge-basen) och med utgångsläget. `git status --short` visade den aldrig som ändrad. **Ingen
`git checkout --` behövdes**, och `untouched`-vakten passerar.

**Omfångning, per ändrad PDF, med `--only`. `--force` användes aldrig.**

```
/usr/bin/python3 scripts/tests/fixtures/capture_guide_baseline.py \
  --only _unpublished/assets/pdfs/guides/apple-intelligence-guide-en.pdf \
  --only _unpublished/assets/pdfs/guides/apple-intelligence-quick-start-en.pdf \
  --only _unpublished/assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf
```

**`RECAPTURED_THIS_ROUND` — kontrollerad, oförändrad, och exakt rätt.** Listan bär tre
poster:

| post | renderad om i rundan? |
|---|---|
| `apple-intelligence-quick-start-sv.pdf` | ja (Task 1, och igen i den här vågen) |
| `apple-intelligence-guide-en.pdf` | ja (Task 13, och igen i den här vågen) |
| `apple-intelligence-quick-start-en.pdf` | ja (Task 13, och igen i den här vågen) |

Vågen renderade om exakt dessa tre. Den fjärde Apple-PDF:en, `apple-intelligence-guide-sv.pdf`,
står med rätta i `untouched` och **inte** i `RECAPTURED_THIS_ROUND` — den är byte-identisk mot
merge-basen. Ingen rad lagd till, ingen tagen bort.

---

## De fyra mätningarna

Mätta mot den slutligt renderade PDF:en med vaktens egna moduler
(`pdf_fingerprint`, `surfacecheck.normalise`), sista tomma formfeed-posten bortstruken.

### 1. Sidantal och tunna sidor

**26 sidor** — oförändrat mot Task 13. **Ingen sida ligger under 400 tecken.** Omslaget
(sida 1) är 445 tecken. De tre tunnaste icke-omslagssidorna:

| sida | tecken | vad det är |
|---|---|---|
| 26 | **802** | "About this guide" — licens-/attributionssidan, tunn med rätta |
| 2 | 1 415 | innehållsförteckningen, tunn med rätta (en lista) |
| 18 | 1 770 | "Before you read Part 3" |

Stoppvillkoret utlöses inte. Sidorna 4 och 5 växte av Important 3 och 4 (sida 4: 2 581 → 2 809
tecken, sida 5: 2 441 → 2 520) utan att brytningen flyttade — ingen sida sköts över till en
ny, och sidantalet står still.

Quick-starterna: **QS-en 2 sidor** (2 420 / 1 958 tecken), **QS-sv 2 sidor**
(2 014 / 2 050 tecken). Inget kort klipptes av tilläggen; båda renderade uppslagen lästes
igenom i utskriftsform.

### 2. TOC:ns fem ankare

| rad i mallen | nummer i mallen | faktisk startsida | unik träff |
|---|---|---|---|
| Part 1 · Get started | 3 | **3** | ja |
| Part 2 · Work smarter | 9 | **9** | ja |
| Part 3 · The GDPR angle | 19 | **19** | ja |
| FAQ | 25 | **25** | ja |
| About this guide | 26 | **26** | ja |

**Alla fem träffar, var och en på exakt en sida, och alla fem nummer stämmer redan.** Inget
nummer rättat i mallen, inget ankare bytt. Inget ankare bär produktnamn, pris eller datum
(oförändrat).

Bikontroll: EP:1050:s *"Part 3 is six pages."* står kvar sann — Del 3 är sidorna 19–24 =
sex sidor. (Rubriksökningen träffar även sida 18, som bär eyebrown "Part 2 · Before you read
Part 3"; den är en Del 2-sida.)

### 3. De 20 förbudsstängarna

**Samtliga 20 mäter noll i båda engelska PDF:erna.** Summa träffar: guide **0**,
quick-start **0**. Icke-noll: inga. Mätt i `_flat()`-form, alltså samma normalisering vakten
själv använder, direkt i de levererade PDF:erna.

Värt att notera för nästa runda: `Siri 2.0` mäter noll i de två engelska PDF:erna, men står
kvar i de svenska **guideytorna** (fryst prosa). Hålet är nu dokumenterat i
`GUIDE_DELIVERY`-kommentaren.

### 4. `[PAGE_COUNT]`

| PDF | träffar |
|---|---|
| `apple-intelligence-guide-en.pdf` | **0** |
| `apple-intelligence-guide-sv.pdf` | **0** |
| `apple-intelligence-quick-start-en.pdf` | **0** |
| `apple-intelligence-quick-start-sv.pdf` | **0** |

Markören finns inte i någon renderad PDF. Quick-startens avslutning bär det äkta talet
(*"The full 26-page Apple Intelligence Guide comes with this quick start in the
community."*), vilket matchar det uppmätta sidantalet.

---

## Svitens tal

```
/usr/bin/python3 -m pytest scripts/tests -q --ignore=scripts/tests/test_prompt_pdf_parity.py
```

| körning | utfall |
|---|---|
| utgångsläget (`42f88bb`, före ändringar) | 837 passed, 1 skipped, **0 failed** |
| efter textändringarna, före omrendering | 837 passed, 1 skipped, **0 failed** |
| efter omrendering + omfångning (slutligt) | **837 passed, 1 skipped, 0 failed** |

Den enda `skipped` är den dokumenterade tomma parametriseringen:
`SKIPPED [1] scripts/tests/test_guide_delivery.py:449: got empty parameter set for (guide)` —
`NO_PAGE_CLAIM` står tom, vilket är ett giltigt återkommande tillstånd enligt modulens egen
kommentar.

Inventeringen efter vågen: **77 vaktrader** (76 + A30:s nya). `surfacecheck.check` mot båda
engelska ytorna ger **noll problem** — ingen `saknas_på_en_yta`, ingen `finns_ingenstans`,
ingen `återinfört`.

---

## Ändrade filer

| fil | vad |
|---|---|
| `_unpublished/exports/apple-intelligence-print-a4-en.html` | Important 2, 3, 4 + Minor 1, 2 (4 rader) |
| `_unpublished/guides/apple-intelligence/index.html` | Important 3, 4 + Minor 1, 3, 4 (5 rader) |
| `_unpublished/exports/apple-intelligence-quick-start-en.html` | Important 6 (2 rader) |
| `_unpublished/exports/apple-intelligence-quick-start-sv.html` | Important 1 (3 rader) |
| `docs/guide-facts-apple-intelligence.md` | Important 5; A30:s postrad, ytdivergensraden, observation 6, A19:s not; nytt vaktblocksavsnitt med `A30`-raden |
| `scripts/tests/test_guide_delivery.py` | Important 1:s `GUIDE_DELIVERY`-kommentar + Minor 5 |
| `_unpublished/assets/pdfs/guides/apple-intelligence-guide-en.pdf` | omrenderad |
| `_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-en.pdf` | omrenderad |
| `_unpublished/assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf` | omrenderad |
| `scripts/tests/fixtures/guide-pdf-baseline.json` | omfångad, `--only`, 3 nycklar |
| `scripts/tests/fixtures/guide-pdf-body-baseline.json` | omfångad, `--only`, 3 nycklar |

`docs/` är gitignorerad — inventeringen committas med `git add -f`.

Inte ändrade: `apple-intelligence-guide-sv.pdf` (byte-identisk), de svenska guideytornas
HTML, `exports/build-apple-intelligence-*.py`, `RECAPTURED_THIS_ROUND`,
`XFAIL_UNTIL_RECOUNTED`, `XFAIL_UNTIL_RERENDERED`, TOC-mallens sidnummer och ankare.

---

## Självgranskningens fynd

Fynd jag gjorde på mig själv under vågen och åtgärdade innan leverans:

1. **Mail-ledet i steg 5 bytte ett obelagt påstående mot ett annat.** Första utkastet skrev
   *"Mail categorisation never depended on this switch"* — en mekanisk slutsats ingen hämtad
   källa bär. Omskrivet till en rapport om vad Apples dokumentation inte säger. Det är precis
   samma defektmönster som A18:s Critical i Fixrunda 1 (en halv sanning skriven som hel), och
   jag höll nära på att upprepa det.
2. **A19-stycket bar ett tredje tidspåstående jag först missade.** Granskarens fynd pekade på
   `thirty to sixty minutes`, men den inledande satsen *"the setup is short but the download
   is not"* är också en varaktighetsutsaga ur samma obelagda uppskattning. Den föll med.
3. **Typografin i QS-en-tilläggen.** Jag skrev typografiska citattecken; hela Apple-korpusen
   använder raka (EP 0, EW 0 krokiga före min ändring). Normaliserat och quick-starten
   renderad om.
4. **Dubbelt "(see Part 2)" i samma listpunkt.** Fångat i genomläsningen av den renderade
   sidan 4, inte i källkoden. Ett ledigt pekarled togs bort.
5. **Fyra följdpåståenden i inventeringen som blev falska av min egen A30-rättelse.**
   Vaktblockets inledande kommentar, A30:s postrad, ytdivergenstabellen och observation 6 sa
   alla att A30 är EW-exklusiv och saknar vaktrad. Att lämna dem hade varit att skapa en ny
   instans av exakt den defekt Important 5 handlar om. Alla fyra uppdaterade.
6. **Vaktblockets citat av steg 5 hade hunnit bli föråldrat** mot den slutliga texten efter
   punkt 1 och 4. Synkat ordagrant.

---

## Farhågor

1. **QS-sv:s punkt 3 bär fortfarande ingen EU-notis.** *"Fråga Siri om torsdagens schema"*
   ber en svensk lärare testa Siri AI, som hen inte kan få. Den engelska tvillingen fick sin
   notis i Task 11 (*"Not on an EU iPad — Siri AI is blocked there."*). Rulingen i Important 1
   gav tre punkter och sa uttryckligen "Rör ingenting annat i filen", så jag lämnade den.
   Mildrande: funktion 2 på samma dokuments **sida 1** bär nu hela spärren, så läsaren möter
   uppgiften innan punkt 3. **Jag rekommenderar att ägaren eller nästa runda lägger notisen.**
   Det är en mening, ordagrant tillgänglig i den engelska tvillingen.
2. **De svenska guideytorna är internt motsägelsefulla mot quick-starten nu.** QS-sv säger
   `Siri AI` och spärrad i EU; `apple-intelligence-print-a4-sv.html` och
   `sv/guider/apple-intelligence/index.html` säger `Siri 2.0` och lovar fortfarande att
   svensk Siri *"fortsätter förbättras genom 2026"*. Det är den frysta prosan, alltså enligt
   beslut — men en läsare som får båda dokumenten ser skillnaden. Hålet är dokumenterat på två
   ställen (`GUIDE_DELIVERY`-kommentaren och vaktblocket), men **dokumentation är inte en
   vakt**: inget test fäller de svenska ytorna.
3. **A30:s nya `aktiv`-rad binder EP:s FAQ-formulering.** Raden kräver `Settings → Siri →
   ChatGPT Extension` ordagrant på båda ytorna. En framtida runda som skriver om EP:s FAQ i
   det kortare registret (t.ex. till *"under Settings → Siri → ChatGPT"*, som sidan 21 skriver)
   gör vakten röd. Det är avsiktligt — det är samma formulering som den rad vakten finns för
   att skydda — men den som rör FAQ-svaret behöver veta det.
4. **Kvalifikatorerna i A05/A06/A07:s postceller är fortfarande runda 1:s.** Jag rättade
   *påståendena om* dem i Utfallsräkningen, men cellerna själva bär kvar `står (öppen
   EU-fråga)`, `står (EU-förbehåll saknas)` och `står (delvis obelagt)`, och
   kvalifikatortabellens åtgärdskolumn står i imperativ ("lägg till förbehållet"). Dokumentet
   säger nu uttryckligen att de ska läsas som historik, men **omklassificeringen är fortsatt
   utestående** — den är uttalat utanför den här vågens omfång och kräver ett beslut om
   taxonomin (bl.a. ordet som saknas för "obelagt påstående struket, inget ersatt", A25/A27/A29).
5. **Sidbrytningen på sidorna 4–5 har mindre marginal än förut.** Sida 4 gick från 2 581 till
   2 809 tecken. Taket i korpusen är sida 15 på 3 013 tecken, så det finns utrymme, men nästa
   runda som lägger text på Del 1:s setup-sida bör räkna sidantalet igen innan den litar på
   26.
6. **`Part 3 is six pages` är hårdkodad och ovaktad.** Den stämmer i dag (19–24), men ingen
   vakt läser den. Den bryts tyst av varje framtida sida som läggs i eller tas ur Del 3. Känt
   sedan Task 13; oförändrat av den här vågen.
