# Apple Intelligence Guide — Design Spec

**Date:** 2026-04-19
**Author:** Johan Lindström + Claude
**Status:** Ready for implementation

## 1. Purpose

A guide that helps Swedish school staff (teachers, principals, school administrators) understand Apple Intelligence from a **pedagogically transparent, privacy-informed** perspective — with emphasis on what makes the tool distinctive in a school context: **most processing happens on the device, which matters under GDPR**.

The guide sits alongside the existing Claude and Gemini/NotebookLM guides in the `choosewise.education` series and uses the same IA pattern (3-part structure instead of 4 — shorter, more focused).

## 2. Positioning

**"Privat AI på dina egna enheter."** Apple Intelligence is the privacy-differentiated counterpart to cloud-first LLMs (Claude, Gemini, Copilot). The guide explains *why that matters* under GDPR and *how to verify* when the privacy claim holds and when it does not.

**Tone:** Pedagogically transparent. Not confrontational. Not marketing material. When a feature is good, describe it as it is. When data leaves the device (Private Cloud Compute, ChatGPT integration), clarify this explicitly so readers understand the mechanics rather than trust a slogan.

## 3. Audience + Device Priority

- **Primary audience:** Swedish school staff with access to iPad 1:1 programs or personal Apple devices
- **Secondary audience:** School IT leads evaluating Apple Intelligence for policy purposes
- **Device order:** iPad → Mac → iPhone
  - Every feature example leads with iPad where possible
  - Mac variants called out in side-notes when genuinely different
  - iPhone mentioned when relevant but never the lead device

## 4. Scope — Features Covered

### Core (Part 2 — full sections)
1. **Writing Tools** — rewrite, proofread, summarize
2. **Siri 2.0** — on-device requests, schema-awareness
3. **Mail categorization + Priority** — sorting parent and colleague mail
4. **Notification summaries** — handling 50+ daily notifications
5. **Notes + Image Wand** — sketch-to-image for whiteboard/handouts
6. **Visual Intelligence** — camera as context (text, documents, objects)

### Mentioned briefly ("värt att veta"-ruta in Part 1)
- Image Playground
- Genmoji
- Clean Up in Photos

### Explicitly out of scope
- Code generation on Mac (not classroom-relevant)
- Deep developer tooling
- Features not yet available in EU/Swedish

## 5. Structure — 3 Parts

### Del 1 — Kom igång (~8 sidor PDF)
- Vilka enheter kör Apple Intelligence (iPad M1+, Mac M-serien, iPhone 15 Pro+)
- Språkstöd (engelska + svenska, uppdaterat 2025/2026)
- Första inställningarna (iPad-first screenshot-flow)
- **Private Cloud Compute — så fungerar det i praktiken** (2 sidor, signatur-sektion)
- "Värt att veta"-ruta: Image Playground, Genmoji, Clean Up

### Del 2 — Arbeta smartare (~12 sidor PDF)
One section per core feature. Each section follows the pattern:
- Vad det gör (1 stycke)
- Pedagogiska exempel (3-5 scenarios, iPad-first)
- **Var händer beräkningen?** (on-device / Private Cloud Compute / ChatGPT-opt-in)
- Kom igång-steg (numrerad lista)
- Mac/iPhone-skillnader (sidruta när relevant)

### Del 3 — GDPR-fördelen i praktiken (~5 sidor PDF)
- Vad stannar på enheten (typiska Writing Tools-operationer, enklare Siri-frågor)
- När används Private Cloud Compute (komplexa/längre uppgifter, bildgenerering ovanför viss tröskel)
- **ChatGPT-integrationens opt-in — undantaget som bryter löftet**
- Vad detta betyder för elevdata i praktiken
- Policybeslut för skolan: DPIA-input, personal-riktlinjer, vad får/får inte skrivas in

## 6. Deliverables

| Artefakt | Sökväg | Ungefärlig storlek |
|---|---|---|
| Web guide EN | `/guides/apple-intelligence/` | ~900 rader HTML + 300 rader ny CSS |
| Web guide SV | `/sv/guider/apple-intelligence/` | ~900 rader HTML + 300 rader ny CSS |
| Full PDF EN | `assets/pdfs/guides/apple-intelligence-guide-en.pdf` | ~25 sidor, genereras från `exports/apple-intelligence-print-a4-en.html` |
| Full PDF SV | `assets/pdfs/guides/apple-intelligence-guide-sv.pdf` | ~25 sidor, genereras från `exports/apple-intelligence-print-a4-sv.html` |
| Quick Start PDF EN | `assets/pdfs/guides/apple-intelligence-quick-start-en.pdf` | 2 sidor, från `exports/apple-intelligence-quick-start-en.html` |
| Quick Start PDF SV | `assets/pdfs/guides/apple-intelligence-quick-start-sv.pdf` | 2 sidor, från `exports/apple-intelligence-quick-start-sv.html` |
| Build script | `exports/build-apple-intelligence-pdf.py` | ~65 rader (modellerad på `build-gemini-notebooklm-pdf.py`) |
| Build script Quick Start | `exports/build-apple-intelligence-quickstart-pdf.py` | ~25 rader |
| Guide-card SVG (cover) | `assets/images/guide-covers/apple.svg` | ~4 KB, matchar befintliga guide-covers |

## 7. Design System Alignment

- **Reuse** Claude guide styles as baseline (guides/claude/styles.css) — copy and adapt rather than fork base tokens
- **Accent color:** Apple brand is historically silver/white, which does not print well. Use **a new accent color** for Apple guide to differentiate from Claude (navy/brass) and Gemini (terracotta):
  - Proposal: **soft graphite** `#3E4A57` (calm, technical, matches Apple's hardware aesthetic)
  - Paired with existing cream surface `#F6F3EE` and near-black text
- **Typography:** same as Claude — Playfair Display (serif headings) + Inter (sans body) — site consistency
- **CC BY-NC-SA 4.0 license band** — already-built pattern from Claude/Gemini guides
- **MailerLite gate** on full PDF download (same pattern); Quick Start as open direct download

## 8. Sources + Research Approach

**Primary sources:**
- Apple's official Apple Intelligence documentation (developer.apple.com, support.apple.com)
- Apple Private Cloud Compute white paper (June 2024, security.apple.com)
- EU feature-availability matrix (Apple support pages, updated quarterly)

**Secondary sources (read with caution):**
- Common Sense Media — partners with Apple, flagged as possibly uncritical. Use for pedagogy ideas, not privacy claims.
- Third-party teacher blogs (verify every specific claim)

**Research discipline:**
- Every privacy claim verified against Apple's own security documentation, not marketing copy
- Every "EU-available" feature claim verified against the current Apple EU matrix
- "Last updated" note on closing page so readers know when to re-verify (Apple rolls out features monthly)

## 9. Global Content Rules (Applied)

Per `feedback_ai_content_global_rules.md`:
- Age limits for AI features stated explicitly (reader responsibility for national rules)
- No advisory "contact your data protection officer" phrasing that implies Johan's legal opinion
- Swedish versions use natural professional Swedish, not translated English

## 10. Questions Answered (Alignment Record)

| Decision | Answer |
|---|---|
| Positioning | **A** — Privat AI / GDPR-differentierad, pedagogiskt fokus |
| Feature scope | **A** — 6 core features; Image Playground/Genmoji i "värt att veta"-ruta |
| IA | **A** — 3 parts (Kom igång, Arbeta smartare, GDPR-fördelen) |
| Device priority | **iPad → Mac → iPhone** |
| Quick Start | **Yes** — 2-page handout, same pattern as Claude/Gemini |
| Bonus chapter | **No** — Del 3 covers GDPR enough; Apple EU situation volatile |
| Tone | **Pedagogically transparent** — not confrontational, not marketing; clarify data-flow mechanics |

## 11. Success Criteria

1. A Swedish school administrator can read the guide and articulate in their own words *when Apple Intelligence processes data on-device vs in Private Cloud Compute vs hands off to ChatGPT*.
2. A teacher can perform at least 3 of the 6 core features on their iPad within 10 minutes of reading Part 2, without needing to hunt through Apple's own docs.
3. The PDF version reads as a standalone document — not just a web-page export. Closing license page, polished typography, consistent with Claude/Gemini PDFs.
4. The web pages render well on iPad (1024pt portrait) without horizontal scroll or broken layouts.
5. CC BY-NC-SA 4.0 license visible on both web and PDF (band / closing page).

## 12. Out of Scope

- Integration with Apple School Manager / Managed Apple IDs (enterprise deployment — separate guide)
- Apple Classroom / Schoolwork app deep-dives (these are classroom management tools, not AI)
- Developer-focused features (Xcode AI, code generation on Mac for teaching CS)
- Comparisons to specific competitor products (Gemini-guide comparison charts — this guide has its own lens)
- Video content or animations (static HTML + PDF only)

## 13. Implementation Order

1. **EN web page** (`/guides/apple-intelligence/`) — scaffold, content, styles
2. **SV web page** (`/sv/guider/apple-intelligence/`) — translate and adapt
3. **EN print-a4 HTML** (`exports/apple-intelligence-print-a4-en.html`) + build script + PDF
4. **SV print-a4 HTML** + PDF
5. **EN Quick Start HTML** + build script + PDF
6. **SV Quick Start HTML** + PDF
7. **Guide cards + JSON updates** — update `guides/guides-en.json` + `sv/guider/guides-sv.json` to flip status from `coming-soon` to `available`, link to new pages
8. **Guide index pages** — verify cards render correctly
9. **CC BY-NC-SA 4.0** — applied to all deliverables from the start
10. **MailerLite gate** — wired to full PDFs (Quick Start is direct download, same as Claude/Gemini)

Est. total time: **3-4 hours of focused work.**
