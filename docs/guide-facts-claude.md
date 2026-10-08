# Påståendeinventering — Claude-guiden

**Rundan:** Blueprint våg 2b. Spec: `docs/superpowers/specs/2026-10-08-wave-2b-claude-guide-content-design.md`
**Upprättad:** 2026-10-08

Varje volatilt faktapåstående i guiden, med alla sina förekomster över de
fyra ytorna. En post är inte klar förrän alla fyra är bockade.

Ytorna: **EW** `guides/claude/index.html` · **SW** `sv/guider/claude/index.html`
· **EP** `exports/claude-print-a4-en.html` · **SP** `exports/claude-print-a4-sv.html`

## Poster

| id | påstående idag | typ | omfång | EW | SW | EP | SP | källa + datum | utfall |
|---|---|---|---|---|---|---|---|---|---|

## Frågor som kräver inloggat konto

Johan betar av. Ja/nej-frågor, inte utredningsuppdrag.

| id | frågan | svar |
|---|---|---|

## Vaktblock

Läses av `scripts/tests/test_guide_surface_consistency.py`. En rad per
bevakat värde: `id | språk | exakt sträng | status`. Status `borttaget`
hoppas över — använd den när ett påstående utgått ur guiden i stället för
att radera raden, så historiken står kvar.

```guard
```
