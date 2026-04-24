# Bildpromptar för guiderna på choosewise.education

**Syfte:** Skapa AI-genererade bilder till de återstående guiderna i samma editoriella foto-stil som Claude-guiden, så att de inte längre känns texttunga och kan återanvändas på respektive ämnessida (jlsu.se / choosewise.education) samt i PDF-versionerna.

---

## Sammanställning — vad som finns och vad som saknas

| Guide | Cover (PDF) | Part-openers | Status |
|---|---|---|---|
| Claude | ✅ foto | ✅ 3 st | Klar |
| Gemini · NotebookLM | ✅ SVG-diagram (behålls) | ✅ 4 st finns på disk, inte invirade i PDF | **0 nya bilder — bara wiring kvar** |
| Microsoft Copilot | ❌ | ❌ | **Saknar 1 cover + 3 part-openers** |
| Apple Intelligence | ❌ | ❌ | **Saknar 1 cover + 3 part-openers** |
| AI for Students / AI för elever | ❌ | ❌ | **Saknar 1 cover + 4 part-openers** |

**Bilder att generera totalt:** 3 covers + 10 part-openers = **13 bilder**.

> **Anmärkning om skärmdumpar:** Varje guide använder också riktiga produktskärmdumpar (t.ex. "screenshot-projects-sidebar.png" i Claude). De ska du fortfarande ta själv från respektive verktyg — de ska *inte* AI-genereras eftersom de visar verklig UI som läsaren behöver känna igen.

> **Om Gemini-PDF:en specifikt:** Coversidan behåller den befintliga SVG-diagrammen (Gemini ↔ NotebookLM). De 4 befintliga delaröppnar-foton i `guides/gemini-notebooklm/assets/` ska wires in i `exports/gemini-notebooklm-print-a4-{en,sv}.html`. Det är ett separat kodjobb — inga nya bilder att generera för Gemini.

---

## Visuell riktning (gäller alla bilder)

För att alla 13 nya bilder ska bli en sammanhållen serie tillsammans med de befintliga Claude- och Gemini-bilderna, bygger varje prompt på samma "style block":

> *"Editorial documentary photography. Warm natural daylight from a side window. Muted, slightly desaturated palette of cream, oak, sage, and wheat. Honest, unposed, contemplative atmosphere. Shot on a 35mm full-frame camera with a 50mm prime lens, f/2.8, soft natural shadows, shallow depth of field, clean composition with breathing room. No visible brand logos. No AI-stylized look — feels like a quiet magazine spread, not a tech ad."*

**Konsekvens-anchors att återanvända:**
- Trämöbler (ek, valnöt) eller kalkstensgolv — aldrig glas/krom
- Hand-skrivna anteckningsblock, böcker, pappersbuntar
- Stengods-mugg (gärna med ångande kaffe/te)
- Linnegardiner eller vita persienner som filtrerar ljuset
- Personer (när de finns med) i åldern 35–55, naturligt klädda i ull, linne, bomull — inte business-suits
- Skärmar antingen mörka, vinklade bort, eller visar generisk text utan logotyper

**Format:**
- **Covers:** 4:5 portrait (1024×1280 eller 2048×2560)
- **Part openers:** 16:9 widescreen (1920×1080 eller 2560×1440)

---

## DEL 1 — Microsoft Copilot (saknar 4 bilder)

### `guides/copilot/assets/cover.jpg` (4:5 portrait)

> A calm Scandinavian-style workplace vignette by a window in soft late-afternoon light. A modern laptop, slightly closed, sits on a pale ash-wood desk; a leather-bound A5 notebook rests beside it, open to a clean page with one neat blue-ink line of handwriting. A black ceramic mug of tea with a thin wisp of steam, a slim silver pen across the notebook, and a printed one-page document with a corner clipped. In the soft background: a single shelf with three thick policy binders and a glass jar of pencils. Muted cream, ash, and slate-blue palette. Editorial documentary photography, 35mm, 50mm lens, f/2.8. Quiet, professional, considered — *the workspace of a school administrator who plans before they act*. No logos visible, no UI, no people in frame.

### `guides/copilot/assets/part-1-opener.jpg` (16:9) — "Get started"

> Two hands of an adult resting lightly on the keyboard of a modern silver laptop on an oak desk by a window. The laptop screen is angled away from the camera, showing only a soft glow. Beside the laptop: a fresh A5 notebook open to the very first page, completely blank except for a single hand-written question mark in pencil at the top, and a stoneware mug of tea. Warm side-lighting from linen curtains. Cinematic editorial style, 35mm, 50mm lens, f/2.8, shallow depth of field. Cream, oak, and warm grey palette. Quiet, focused, beginner-energy — *the moment before someone starts learning a new tool*. No logos, no visible UI.

### `guides/copilot/assets/part-2-opener.jpg` (16:9) — "Work smarter"

> A flat-lay overhead shot of a busy but tidy oak desk in soft daylight. A modern laptop open in the lower third, screen dark. Around it, arranged in three loose clusters: (1) a printed Word-style document with handwritten edits and a fountain pen on top, (2) a small stack of three printed slide thumbnails next to a ruler, (3) a printed email-style paper with a yellow sticky note attached. A stoneware mug of coffee with a thin curl of steam in the upper right corner. Reading glasses folded beside the laptop. Editorial overhead documentary style, 35mm, slightly elevated angle. Muted cream, oak, slate-blue, and parchment palette. *Six tools, one workflow* — the visual implication is multitasking under control. No logos, no on-screen text.

### `guides/copilot/assets/part-3-opener.jpg` (16:9) — "Compliance & licensing in practice"

> A serious but warm scene on a dark walnut desk in a quiet office: a thick navy ring-binder labelled only with a discreet white spine label that reads "Policy" in small serif type, partially open, with a printed multi-page document tucked inside marked with sticky tabs in three colours. A pair of folded tortoiseshell glasses rests on top. Behind the binder, a small green banker's lamp casts a warm pool of light. A stoneware mug and a leather-bound notebook sit slightly out of focus in the background, alongside a small framed certificate-style document angled away from the viewer. Light from a tall window in the upper left, soft shadows across the wood. Editorial photography, 35mm, 50mm lens, f/2.8. Palette: walnut, navy, cream, and brass. *The mood of due diligence and quiet governance.* No logos, no readable text on the certificate.

---

## DEL 2 — Apple Intelligence (saknar 4 bilder)

### `guides/apple-intelligence/assets/cover.jpg` (4:5 portrait)

> An editorial still life on a pale ash-wood desk in a calm, modern Scandinavian study, lit by soft daylight through a tall window with sheer linen curtains. Centred: a modern thin tablet (iPad-shape, generic, no logo) lying flat with its screen completely black and reflective like dark glass. To the left, a slim folded smart-cover keyboard in oatmeal fabric. To the right, a stoneware mug of green tea and a small notebook open to a blank page with a single sentence in pencil. A small ceramic dish with a single white pebble at the upper edge for visual quietness. Muted palette of warm white, oatmeal, sage, and pale oak. Editorial documentary photography, 35mm, 50mm lens, f/2.8, shallow depth of field, soft natural shadows. No logos. *The mood is calm minimalism — design as restraint.*

### `guides/apple-intelligence/assets/part-1-opener.jpg` (16:9) — "Get started"

> An overhead, slightly angled shot of a single adult's hand gently tapping the dark glass screen of a thin modern tablet (iPad-shape, no logo) lying on a pale linen tablecloth. The screen shows nothing — just the faint reflection of soft window light. Next to the tablet: a small stoneware espresso cup, a thin silver pen, and a folded pair of round wire glasses. Warm side-lighting from a window just out of frame. Cinematic editorial style, 35mm, 50mm lens, f/2.8. Palette: warm white, linen, oak, brushed aluminium. *The first quiet moment of switching something on.* No visible UI, no logos.

### `guides/apple-intelligence/assets/part-2-opener.jpg` (16:9) — "Work smarter"

> A bright, airy classroom corner in a Nordic school in late morning. A thin tablet (iPad-shape, no logo) sits propped up at a slight angle on a wooden teacher's desk, screen dark and reflective. Around it: a printed lesson plan with neat handwritten annotations in pencil, a small stack of student notebooks bound with elastic, a stoneware mug of coffee, and a vase with a single sprig of dried wheat. A wide window in the soft background shows out-of-focus bare trees and a hint of a school yard. Warm natural daylight, no overhead fluorescents. Editorial documentary photography, 35mm, 50mm lens, f/2.8. Palette: warm white, oak, oatmeal, and pale green. *A teacher's preparation moment — calm, mid-week, mid-morning.* No logos, no people in frame, no readable text on screen.

### `guides/apple-intelligence/assets/part-3-opener.jpg` (16:9) — "The GDPR angle in practice"

> A composed editorial scene on a dark walnut desk in a quiet office, lit by tall window light filtered through half-closed wooden venetian blinds — soft horizontal bands of light fall across the surface. Centred: a thin tablet (iPad-shape, no logo) face-down on the desk to imply privacy, beside a closed leather-bound document folder with a slim brass clasp. A small old brass key rests on top of the folder. A stoneware mug of black tea, a fountain pen, and a single sealed cream-coloured envelope arranged with restraint around the folder. Muted palette of walnut, cream, brass, and shadowed grey. Editorial photography, 35mm, 50mm lens, f/2.8, shallow depth of field. *The mood: discretion, custodianship, careful handling of something private.* No logos, no readable text.

---

## DEL 3 — AI for Students / AI för elever (saknar 5 bilder)

> Samma bilder används i båda språkversionerna (engelska + svenska). Filerna ligger redan på samma plats per språk — du kan kopiera bilderna mellan `guides/ai-for-students/assets/` och `sv/guider/ai-for-elever/assets/`.

### `guides/ai-for-students/assets/cover.jpg` (4:5 portrait)

> A warm editorial still life on a wooden classroom desk in soft daylight from a tall window. Centred: an open spiral-bound student notebook with a half-finished hand-written sentence in pencil mid-stroke, a wooden HB pencil resting across the page, a worn paperback novel with a folded corner, and a small stack of three textbooks with cloth bookmarks. To one side, a stoneware mug of milky tea and a green apple with one small bite taken out. The faintest hint of a closed laptop in the soft background, completely de-emphasised. Light filters through the window, casting a soft golden bar across the notebook. Muted palette of cream, oak, sage, and apple green. Editorial documentary photography, 35mm, 50mm lens, f/2.8. *The mood: learning is the point, tools are secondary.* No logos.

### `guides/ai-for-students/assets/part-1-opener.jpg` (16:9) — "Learning is the point"

> A close-up, slightly low-angle shot of a young student's hands (age implied 14–16, no face visible) writing in pencil in a lined notebook on a wooden desk. The page shows a half-completed mind map with hand-drawn arrows and bubbles. Beside the notebook: a worn textbook open face-down, a wooden ruler, and a small ceramic cup of water. Soft window light from the upper-left, warm daylight, no fluorescents. Editorial documentary style, 35mm, 50mm lens, f/2.8, shallow depth of field. Palette: cream, oak, graphite grey, and pale sage. *The act of thinking, made visible.* No devices in frame, no logos, no readable text.

### `guides/ai-for-students/assets/part-2-opener.jpg` (16:9) — "Prerequisites before AI becomes part of the lesson"

> An empty classroom in soft early-morning light, just before students arrive. A teacher's wooden desk in the foreground, neatly prepared: a printed lesson plan with handwritten margin notes, a stoneware mug of coffee with a thin curl of steam, a closed thin laptop angled to one side, a small stack of student notebooks bound with an elastic, and a single book open to a marked page. The blackboard or whiteboard in the soft background is mostly out of focus, with only a faint outline of a hand-written learning objective visible. Warm side-lighting from tall windows. Editorial documentary photography, 35mm, 50mm lens, f/2.8. Palette: warm white, oak, oatmeal, and chalkboard green. *The mood: preparation, before the day begins.* No logos, no people in frame, no readable text.

### `guides/ai-for-students/assets/part-3-opener.jpg` (16:9) — "On the classroom floor"

> A documentary mid-shot inside a Nordic secondary classroom in session. A teacher in their 40s, in a soft wool cardigan, stands beside a student desk and leans down slightly to look at a student's open notebook — both faces in profile or partially turned away, no direct eye-contact with camera. The student's tablet (no logo) sits flat on the desk, screen dark. Two other students at adjacent desks work quietly with notebooks and books. Warm natural daylight pours through a large window in the background, slightly out of focus. Editorial documentary style, 35mm, 50mm lens, f/2.8, shallow depth of field. Muted palette: oak, cream, soft denim, and pale moss. *The mood: presence, oversight, a teacher in the room — not at the door.* No logos, no readable screens.

### `guides/ai-for-students/assets/part-4-opener.jpg` (16:9) — "Checklist: Should students use AI in this lesson?"

> An overhead flat-lay on a pale oak desk: a clean printed A4 checklist with twelve numbered items lies in the centre — the items are visible but blurred so they read as "checklist" without being legible. A black fountain pen rests across the page, with three of the early checkboxes ticked in confident handwritten ink. Around the page, arranged with quiet care: a stoneware mug of tea, a folded pair of tortoiseshell glasses, a small stack of student notebooks, and a wooden ruler. Soft window light from the upper-left, gentle natural shadow across the page. Editorial documentary photography, 35mm overhead, f/2.8. Palette: cream, oak, ink-black, and warm grey. *The mood: a thoughtful pause before deciding.* No logos, no readable text apart from the implication of a list.

---

## Workflow-tips när du genererar

1. **Generera 3–4 varianter per prompt** — välj den som mest stilistiskt matchar de befintliga Claude-bilderna.
2. **Kör samma prompt mot Nano Banana 2 *och* Midjourney/Imagen** — du brukar få bäst resultat genom att jämföra. Nano Banana 2 är ofta starkare på det editoriella foto-greppet, men Midjourney ger ibland bättre ljussättning.
3. **Spara originalen** i högsta upplösning innan du nedskalar för webben (nuvarande JPG-filer i Claude-guiden ligger på ca 1024 px bredd, vilket räcker både för webb och PDF-tryck).
4. **Konsistenscheck:** lägg upp alla 13 nya bilder bredvid Claude- och Gemini-bilderna och titta på paletten som helhet — om någon sticker ut för mycket (för blå, för "AI-tech-look"), kör om den.
5. **Filnamn:** använd exakt de filnamn som står i varje rubrik ovan — då fungerar både `<img src="…">`-taggarna i HTML-guiderna och referenserna i `exports/*-print-a4-*.html` direkt utan kodändringar.

---

## Vad jag *inte* gjort prompts för (med flit)

- **Produktskärmdumpar** (t.ex. `screenshot-gems.png`, `screenshot-canvas.png`, `screenshot-projects-sidebar.png`) — dessa måste vara verkliga UI-bilder som läsaren känner igen från sitt eget verktyg. AI-genererade fejk-skärmdumpar urholkar guidens trovärdighet.
- **Logotyper** för respektive AI-tjänst — de SVG-filerna i `assets/images/guide-covers/` (claude.svg, copilot.svg, gemini.svg, apple.svg, ai-for-elever.svg) finns redan och fungerar för listsidor och social-cards.
- **Hero-bannrar** på varje guidesida — de använder typografi mot färgad bakgrund, inte foto, och behöver inte AI-bilder.

Säg till om du vill att jag justerar tonen i någon prompt — t.ex. mer "klassrum", mindre "studiekammare", eller mer pojk-/flick-koderat. Och säg till om du vill ha versioner av prompterna på engelska direkt mot Nano Banana — ovan ligger redan engelska prompts (eftersom det ger bäst resultat), inramade på svenska.
