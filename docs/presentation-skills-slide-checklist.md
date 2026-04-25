# Presentationsteknik — slide-leveransspec

**Plats där bilderna ska in:** `Ny JLSU hemsida/assets/images/presentation-skills/slides/`

## Format

| Spec | Värde |
|---|---|
| Filformat | **JPG** (Keynote: Arkiv → Exportera till → Bilder → JPG, kvalitet "Bra" eller "Bästa") |
| Upplösning | **1920 × 1080 px** (Keynotes 16:9-standard) |
| Branding | **Inga Advania-loggor**, inga sidnummer från mallar, inga datum-/footer-element |
| Filnamn | **Exakt** enligt listan nedan (case-sensitive, bindestreck, inga mellanslag) |

Förslag på arbetsflöde: skapa en ny Keynote-fil (kalla den `presentationsteknik-webslides.key`) — kopiera in originalslidesen som ska användas, skapa nya för makeover-paren, ta bort allt Advania-chrome, och exportera hela presentationen i ett svep. Då blir filnamnen sekventiella och du döper bara om dem efter exporten.

## Bilder som behövs (19 stycken)

### A. Direktöverförda slides från Keynote del 1 *(5 st — du har dem redan, ta bara bort Advania-loggan)*

| Filnamn | Original (slide #) | Beskrivning |
|---|---|---|
| `slide-040-prickar.jpg` | Del 1, slide ~40 | 11 utspridda turkosa prickar på svart bakgrund — Gestalt-övning, "räkna prickarna" |
| `slide-060-laroplan-textmur.jpg` | Del 1, slide 60 | Hela paragrafen om "En likvärdig utbildning" från läroplanen, vit text på svart bakgrund |
| `slide-080-punktlistor.jpg` | Del 1, slide ~80 | Bullet-list "Kort text om apelsiner / citroner / äpplen / ananas" — exempel på meningslös punktlista |
| `slide-200-hp-lenovo.jpg` | Del 1, slide ~200 | Tabellen med HP / Lenovo / Acer / Asus och prissiffror för fyra modeller |
| `slide-269-tiger.jpg` | Del 1, slide ~269 | Lågupplöst, pixlig tiger-bild — exempel på dålig bildkvalitet |

### B. Modul 2:s "reveal-on-click"-övning *(2 st — nya slides du designar)*

Två slides som visar samma innehåll men i olika kvalitet. Användaren klickar för att toggla mellan dem.

| Filnamn | Beskrivning |
|---|---|
| `slide-modul2-fore.jpg` | "Före": en typisk dålig slide — fyra bullet-punkter under en rubrik, kanske något i stil med fyra punkter om "AI i undervisningen" eller liknande tema |
| `slide-modul2-efter.jpg` | "Efter": samma budskap men byggt om till **ett enda kärnbudskap** som tar fokus — t ex en stor mening i mitten av sliden eller ett enda nyckelord i versaler |

Tänk på det som en läroexempel — det "efter"-slidet ska ha en tydligt synlig poäng som blir minnesvärd inom 3 sekunder.

### C. Makeover-galleri (modul 3 fördjupning) *(12 st — nya composite-slides)*

Varje makeover är **en slide som visar både "före" och "efter" sida vid sida** (vänster halva = före, höger halva = efter, med ett "→" eller liknande visuell separator). Användaren ser hela paret på en gång.

Spec per slide: 1920×1080, två "halv-slides" inuti vilket gör varje halva ca 900×900 px med marginal mellan dem. Lägg gärna en liten textetikett ("FÖRE" / "EFTER") i ett hörn.

| Filnamn | Före | Efter |
|---|---|---|
| `makeover-01-fore-efter.jpg` | En hel paragraf läroplanstext täcker hela sliden | En enda nyckelmening centrerad, med en hänvisning till källan i mindre text längst ned |
| `makeover-02-fore-efter.jpg` | Åtta punkter på en sida i Arial 18pt | En enda mening som tar upp halva sliden, med en relevant ikon till vänster |
| `makeover-03-fore-efter.jpg` | En tabell med 9 kolumner och 6 rader, alla siffror i samma storlek | Tre stora siffror centrerade på sliden med en kort beskrivning under varje |
| `makeover-04-fore-efter.jpg` | Slide med logotyp uppe till vänster, datum uppe till höger, sidnummer nere, footer med organisationsnamn — innehållet trängs i en liten ruta i mitten | Enbart innehållet, fullt utnyttjande av sliden |
| `makeover-05-fore-efter.jpg` | Tre stockfoton i rad med korta etiketter (folk skakar hand, glödlampa, uppåtgående pil) | En enda fotografisk bild som täcker hälften av sliden, med ett kort textstycke bredvid |
| `makeover-06-fore-efter.jpg` | Bullet-text med "Bounce"-animation från höger (visa med rörelseslinjor eller "(animering)") | Samma bullet-text, men med en lugn cross-fade (visa med subtil överlapp) |
| `makeover-07-fore-efter.jpg` | Komplext diagram med tre olika Y-axlar och fem linjer | Enkelt linjediagram med en linje och en Y-axel, med själva poängen markerad |
| `makeover-08-fore-efter.jpg` | Tre färgglada ikoner i triangelformation med pilar mellan, ingen tydlig struktur | Ett enkelt diagram med tre noder och linjer som visar ett konkret förhållande |
| `makeover-09-fore-efter.jpg` | En slide med en kort bullet-lista överst, en bild i mitten och ett citat nederst | Två slides istället för en — en med bilden + citatet, en med bullet-listan (visa båda i "efter"-halvan) |
| `makeover-10-fore-efter.jpg` | Block med 12pt-text — oläsbart från avstånd | Ett enda nyckelord i 72pt som tar fokus |
| `makeover-11-fore-efter.jpg` | Slide med Times New Roman som rubrik, Arial som brödtext och Comic Sans i en faktaruta | Samma slide men med endast en typsnittsfamilj (t ex Inter), regular för brödtext och bold för rubrik |
| `makeover-12-fore-efter.jpg` | Rubriken **"Inflation, ekonomi, kostnader"** ovanför en graf | Rubriken **"Maten kostar 23 % mer än 2021"** ovanför samma graf |

## Ljudfil för modul 4 *(1 st)*

| Filnamn | Plats | Beskrivning |
|---|---|---|
| `modul-4-utfyllnadsljud.mp3` | `Ny JLSU hemsida/assets/audio/` *(skapa mappen)* | 60 sekunders ljudklipp där en presentatör (du själv eller någon annan) gör medvetna utfyllnadsljud — "öh", "ehm", "liksom", "alltså". Räkna själv — säg till mig hur många och jag uppdaterar "Rätt antal: 14" i modul 4 till ditt korrekta tal. |

## Sammanfattning

- **5** "lätta" slides — bara ta bort Advania-loggan från befintliga
- **2** "reveal"-slides — nydesign av övningsslide för modul 2
- **12** makeover-paren — nydesign för fördjupning i modul 3
- **1** ljudfil för modul 4

Total: **19 bilder + 1 ljudfil**.

När du är klar: lägg dem i mapparna ovan, säg till så commits jag in dem och uppdaterar siffran i modul 4.
