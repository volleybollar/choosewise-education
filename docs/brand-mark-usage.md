# Choosewise-märket — så används det

**Källan:** `assets/images/brand/mark-on-dark.svg` och `mark-on-light.svg`.
Allt annat genereras ur dem av `scripts/build-brand-assets.py`. Rita aldrig
märket på nytt i en enskild fil — vakten i `scripts/tests/test_brand_mark.py`
jämför banddata och blir röd.

## Geometri — bindande

Allt i en 64×64-ruta. Måtten valdes efter mätning vid 16 och 32 pixlar.

| Element | Värde |
|---|---|
| Ring | centrum 32,32 · radie 21 · linjebredd 2,5 · `fill="none"` |
| Nål, norr | `M32 6 L37.5 32 L26.5 32 Z` |
| Nål, söder | `M32 58 L37.5 32 L26.5 32 Z` |
| Nålsöga | centrum 32,32 · radie 2,6 · **bottnens färg** |

Nålsögat är ett hål i nålen, inte en prick ovanpå.

## Två färglägen, inga fler

| | Mot mörkt | Mot ljust |
|---|---|---|
| Ring | `#FBFAF8` | `#0B3A6F` |
| Nål, norr | `#E8C9A8` | `#C2793A` |
| Nål, söder | `#FBFAF8` | `#0B3A6F` |
| Nålsöga | `#0B3A6F` | `#FBFAF8` |

Kopparn mot blått är `#E8C9A8`. `#C2793A` når bara 3,0:1 mot `#0B3A6F`
och slocknar i små storlekar.

## Regler

- Minsta storlek **16 px**. Under det används märket inte alls.
- Frizon **11 enheter** i 64-rutan, alltså 17 % av bredden, runt om.
- Aldrig omfärgat utanför de två lägena, roterat, lutat, med skugga eller
  kontur, ihoptryckt, eller mot en botten som varken är papper eller
  varumärkesblå.
- Sajtens header bär inget märke. Ordmärket står som ren text.

## Guidomslag — regeln våg 2a tillämpar

Märket sitter **uppe till vänster**, 34 enheter brett på ett A4 (210×297),
med 24 enheters marginal från vänsterkant och topp. Mörkt omslag tar det
mörka läget, ljust omslag det ljusa.

Märket är litet med flit: på ett guidomslag är titeln avsändaren och
märket bara signaturen. Under titeln går kopparlinjen, och under den
`CHOOSEWISE.EDUCATION` spärrat — i `#E8C9A8` mot mörkt, `#9C5A24` mot
ljust.
