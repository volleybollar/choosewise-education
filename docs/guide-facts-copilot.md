# Påståendeinventering — Copilot-guiden

**Rundan:** Copilot-guiden, internationell omriktning. Spec: `docs/superpowers/specs/2026-10-09-copilot-guide-international-design.md`
**Upprättad:** 2026-10-09
**Faktakontrollerad:** (Task 4)

Varje volatilt faktapåstående i de **engelska** ytorna, med alla sina
förekomster. De svenska ytorna ingår inte i rundan (spec §5) och har därför
inga poster.

Ytorna: **EW** `_unpublished/guides/copilot/index.html` · **EP**
`_unpublished/exports/copilot-print-a4-en.html` · **QS**
`_unpublished/exports/copilot-quick-start-en.html`

**QS står utanför ytkonsistensvakten** — avsiktligt, spec §7: quick-starten är
en tredje yta med egen, kortare formulering, och kravet "ordagrant på alla
ytor" vore rött från dag ett och därmed värdelöst. Den bevakas i stället av
förekomstkolumnen här, av PDF-facit, och av leveransvakten
(`scripts/tests/test_copilot_delivery.py`).

## Hur källorna läses

Varje sida hämtas som rå HTML och läses ordagrant; texten extraheras lokalt ur
markupen. Ingen sida sammanfattas av ett annat modellanrop, och en
sammanfattning är aldrig källa till ett värde. Där källor går emot varandra
står båda, och den nyare vinner — med noteringen att de skiljer sig.

## Poster

(Task 3 fyller tabellen, Task 4 kolumnerna källa och utfall.)

| id | påstående idag | typ | EW | EP | QS | källa + datum | utfall |
|---|---|---|---|---|---|---|---|

## Observationer utanför posterna

(Task 4.)

## Vaktblock

Semantiken är den som gäller sedan 2026-10-09: `aktiv` kräver att strängen
står ordagrant på **båda** de engelska guideytorna (EW + EP), `borttaget` att
den **inte** står på någon av dem. Varje påstående rundan stryker eller rättar
får en `borttaget`-rad — den är det enda som hindrar att rättningen tas
tillbaka.

```guard
# Fylls i Task 10. Tills blocket har rader hoppar de parametriserade
# vakterna över copilot, och Task 13 kräver 0 skipped i sviten — så ett
# tomt block kan inte överleva rundan.
```
