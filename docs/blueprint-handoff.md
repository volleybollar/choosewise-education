# Blueprint — överlämning

**Datum:** 2026-10-05
**Status:** PR #28 **MERGAD 2026-10-05** som merge-commit `851c9f5`. 41 commits från `feat/visual-identity-blueprint` ligger i `main` och Blueprint är live på choosewise.education (Pages-bygget grönt, live-CSS verifierad). Svit 110/110 både före och efter mergen. Grenen är inte raderad.
**LÄS FÖRST** vid fortsättning. Specen är den bindande auktoriteten, planen argumenterar från den.

---

## Vad som är gjort

Choosewise.educations grafiska uttryck är bytt till **Blueprint**: djupblått som varumärkesfärg, koppar som enda varma ton, Hanken Grotesk som enda typsnitt med Instrument Serif enbart i citat. Innehållet är oförändrat — inte ett ord, en rubrik, en URL eller ett filnamn.

- PR: https://github.com/volleybollar/choosewise-education/pull/28
- Spec: `docs/superpowers/specs/2026-10-05-choosewise-visual-identity-design.md`
- Plan: `docs/superpowers/plans/2026-10-05-visual-identity-wave-1.md`
- Loggbok med alla 44 besluten: `.superpowers/sdd/2026-10-05-visual-identity-wave-1/progress.md`
- Skärmbilder och rapporter: `~/Desktop/choosewise-blueprint-granskning/`

Testsviten gick från 0 till **110 tester** och vaktar nu paletten, kontrastvärdena, typsnitten, tokendisciplinen, viktskalan, hela filkorpusen och de 124 prompt-PDF:ernas innehåll per sida.

## Paletten

| Token | Värde | Roll |
|---|---|---|
| `--color-bg` | `#FBFAF8` | papper |
| `--color-bg-alt` | `#EFF2F6` | svalt sektionsband |
| `--color-text` | `#0C1A2E` | bläck |
| `--color-text-soft` | `#4E5A68` | brödtext |
| `--color-text-muted` | `#656F7B` | metadata |
| `--color-border` | `#DDE3EA` | hårlinje |
| `--color-accent` | `#0B3A6F` | varumärkesblå, **samma värde som `--color-dark-bg`** |
| `--color-deep` | `#07284D` | footer, djupare band |
| `--color-highlight` | `#C2793A` | koppar i **ytor och grafik, aldrig text** |
| `--color-highlight-ink` | `#9C5A24` | koppar i **text på ljust** |
| `--color-highlight-on-dark` | `#E8C9A8` | koppar i **text på mörkt** |

Vikter: display 300, rubrik 400, brödtext 400, betoning 500. **Inget utanför skalan.**

## Vad som ÅTERSTÅR att besluta

Inget av det blockerar en merge.

1. **Evidence Toolkit — banden.** "Kring" och "över" typisk skoleffekt skiljer bara **1,54:1**. Pillren visar bara siffran, aldrig bandets namn, så färgen är enda ledtråden. Det är ett **palettak**, inte ett förbiseende: `--color-accent` är redan så mörk att inget mörkare kan nå högre mot den. Vägen till 8–10:1 är att göra "över" **ljusare** än blå. Under det ligger en större fråga: färg ensam som informationsbärare är WCAG 1.4.1, och det var sant före det här arbetet.

2. **Bloggkortens understrykningar.** Datum, rubrik och ingress är alla understrukna — hela kortet är en länk och understrykningen ärvs. **Preexisterande**, verifierat: varken `render-blog.js`, `posts-*.json` eller `text-decoration`-reglerna rördes av den här grenen.

3. **Paletten saknar en larmfärg.** Det har tvingat fram kompromisser två gånger: EU AI Act-pyramidens "Unacceptable" fick samma koppar som allt annat, och "Watch Out"-rutan fick lösas med form i stället för färg. Ett enda nytt token skulle lösa båda.

## Vad som INTE ingick — våg 2 och spår A

- **Våg 2:** de 23 export-mallarna i `exports/` bryts ut till en delad `_guide-print.css`, guide-PDF:erna renderas om, och **sedan** uppdateras guidernas innehåll. Två steg, inte ett — om en PDF går sönder ska det gå att se om det var mallen eller texten. Nio av mallarna kör fortfarande Crestioras navy/mässing/Playfair. Visual Codes Vol. 1–3 utanför repot har en tredje kopia av paletten.
- **Spår A:** märke, favicon och Skool-tillgångar. Sajten har **ingen logotyp och ingen favicon** — bara ett textordmärke. Skool kräver logotyp, favicon och omslag 1400×790, och det är de enda ytorna Skool låter en styra.

## Fällor som kostade tid — läs dessa innan nästa ändring

1. **Fokusringar mäts med Tab, aldrig med `.focus()`.** Chromium svarar `true` på `matches(':focus-visible')` utan att tillämpa stilen vid programmatiskt fokus. Tre separata verifieringar i det här arbetet var osunda av det skälet. Läs dessutom av värdet **minst 180 ms** efter tangenttrycket — `.btn` har en övergång på 150 ms och en tidigare avläsning fångar värdet mitt i.

2. **Fyra tester kunde inte fallera på det de påstod sig vakta.** Ett token som fanns men aldrig användes. Ett paritetsbevis som bevisade en annan funktion än grinden. En typsnittsvakt som inte täckte sitt eget motiverande fall. En viktvakt som kontrollerade att strängar förekom *någonstans*. Mönstret: testet mätte färgen i burken, inte färgen på väggen. **Fråga alltid: skulle det här bli rött om felet kom tillbaka?**

3. **Använd `brandguard.published_files()`, aldrig ad hoc-grep**, för frågor om vad som är publicerat. Egna grep-kommandon gav fel svar tre gånger: skiftlägeskänslighet missade två filer, och ett trasigt exkluderingsmönster rapporterade 27 falska träffar i `exports/`.

4. **Sajten undervisar om design.** `presentation-skills/module-2` skriver "Fraunces, Times) can feel heavier…" i brödtext. En varumärkesvakt som matchar på typsnittsnamn utan `font-family`-kontext slår larm på din egen undervisning.

5. **Helsidesbilder ljuger om sidor med scroll-animation.** WISE-sidan ser ut som att avsnitten hamnat mitt på sidan — det är verktyget som rullar ut hela scrollsträckan och klistrar in den klibbiga menyn. Fönsterstora bilder vid olika scrollägen visar sanningen.

6. **`build-seo-meta.py` bumpar "Last updated"** ur git-commitdatum på varje sida vid en sajtbred commit. Kontrollera vad skriptet rör och återställ orelaterade sidor före push.

7. **Förhandsvisning körs alltid på ny port** — `include.js` hämtar `header-*.html` separat och Safari cachar hårt.

8. **`git add -A` används aldrig.** Repot har ~18 ocommittade ändringar som hör till Johan och inte till det här arbetet.

## Interpretern

`/usr/bin/python3` (3.9.6) är den **enda** som har `pytest` och `playwright`. Homebrews `python3` (3.14) saknar båda.
