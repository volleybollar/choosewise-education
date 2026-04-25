# Presentationsteknik — slide-leveransstatus

**Plats:** `Ny JLSU hemsida/assets/images/presentation-skills/slides/`

> **Status 2026-04-25:** Johan levererade 40 slides från egen Keynote (`Presentationsteknik-webslides.001-040.jpeg`). 38 av dessa har integrerats i kursen. Två "ÖVNING"-divider-slides (003, 010) hoppades medvetet över — de fyller ingen funktion på webben där varje övning redan har egen styling.

## Var bilderna används

### Modul 1 — Varför presentationsteknik?
**Minnesövning** (10 + 10 par)

| Filnamn | Källa | Roll |
|---|---|---|
| `slide-minne-bild-01.jpg` … `-10.jpg` | Keynote 019–028 | 10 bilder som visas 2 sek per styck (fas 1) |
| `slide-minne-par-01.jpg` … `-10.jpg` | Keynote 029–038 | 10 par-bilder, en sedd + en ej sedd (fas 2) |

Svarsnyckeln (vilken sida i varje par är sedd) ligger inbakad i HTML:en på modul 1: `data-answers="L,L,R,R,R,R,L,L,L,R"`. Om du byter ut bilderna måste nyckeln uppdateras därefter.

### Modul 2 — Designa diabilder
| Filnamn | Källa | Var i modulen |
|---|---|---|
| `slide-bakgrund-1.jpg`–`-4.jpg` | Keynote 004–007 | Sektion "Färg och kontrast" — 2×2-grid av bakgrundsval |
| `slide-projektor.jpg` | Keynote 008 | Sektion "Färg och kontrast" — vit bg "tar bort fokus" |
| `slide-langd.jpg` | Keynote 009 | Sektion "Färg och kontrast" — svart bg "fokus på dig" |
| `slide-dalig-kontrast.jpg` | Keynote 013 | Sektion "Färg och kontrast" — split mörkblå/vit på svart |
| `slide-rubrik-storlek.jpg` | Keynote 012 | Sektion "Typografi" — rubriken behöver inte vara störst |
| `slide-font-serif.jpg` | Keynote 040 | Sektion "Typografi" — serif vs sans |
| `slide-styra-blicken.jpg` | Keynote 039 | Sektion "Styr blicken med färg" — luftballong i färg |
| `slide-textmur-fore.jpg` | Keynote 001 | Övning (reveal-on-click) — också i modul 3 |
| `slide-textmur-efter.jpg` | Keynote 002 | Övning (reveal-on-click) — också i modul 3 |

### Modul 3 — När diabilden krockar med dig
| Filnamn | Källa | Var i modulen |
|---|---|---|
| `slide-prickar.jpg` | Keynote 011 | Sektion "Räkna prickarna" — Gestalt-demo |
| `slide-textmur-fore.jpg` | Keynote 001 | Sektion "Textmuren" — ohighlightad |
| `slide-textmur-efter.jpg` | Keynote 002 | Sektion "Textmuren" — highlightad |
| `slide-bilder-vs-bullets.jpg` | Keynote 014 | Sektion "Punktlistans dilemma" — frukt-grid |
| `slide-tabell-full.jpg` | Keynote 015 | Sektion "Tabeller" — full kontrast på allt |
| `slide-tabell-tonad.jpg` | Keynote 016 | Sektion "Tabeller" — fokus på en kolumn, resten dimmade |
| `slide-skrikig.jpg` | Keynote 018 | Sektion "Mallar, animeringar" — överbelastat extremfall |
| `slide-bildkvalitet.jpg` | Keynote 017 | Sektion "Bildkvalitet" — skarp vs suddig blomma |

## Format

| Spec | Värde |
|---|---|
| Filformat | JPG (Keynote-export, kvalitet "Bra"/"Bästa") |
| Upplösning | ~1920×1080 (Keynote 16:9) |
| Branding | Inga Advania-loggor, inga sidnummer, inga datum/footer |
| Filnamn | Exakt enligt listorna ovan (case-sensitive, bindestreck, inga mellanslag) |

## Kvarvarande leveranser

### Modul 4 — ljudfil
| Filnamn | Plats | Beskrivning |
|---|---|---|
| `modul-4-utfyllnadsljud.mp3` | `Ny JLSU hemsida/assets/audio/` *(skapa mappen)* | 60 sek där en presentatör (du själv eller någon annan) gör medvetna utfyllnadsljud — "öh", "ehm", "liksom", "alltså". Räkna själv hur många ljud du la in; säg numret till mig så uppdaterar jag "Rätt antal: 14" i `sv/presentationsteknik/modul-4/index.html`. |

## Vad som inte längre behövs

Den ursprungliga 19-bilders-specen (`slide-040-prickar.jpg`, `slide-060-laroplan-textmur.jpg`, `slide-080-punktlistor.jpg`, `slide-200-hp-lenovo.jpg`, `slide-269-tiger.jpg`, `slide-modul2-fore.jpg`, `slide-modul2-efter.jpg`, samt 12 makeover-paren `makeover-01-fore-efter.jpg`–`makeover-12-fore-efter.jpg`) är ersatt av de 38 slides Johan faktiskt levererade. Modul-3-fördjupningen är omskriven från visuellt galleri till textbaserade principer (12 stycken) — bilder behövs inte där längre.
