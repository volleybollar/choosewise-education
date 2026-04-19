# Microsoft Copilot Guide — Content Design Spec

Date: 2026-04-19
Target audience: Teachers and school leaders in Sweden (primary) + international readers (secondary).
Canonical URLs: `/guides/copilot/` (EN), `/sv/guider/copilot/` (SV).

## Positioning

Microsoft Copilot is the **enterprise-integrated option** — the AI already running inside the Microsoft 365 tenant most Swedish schools already use. Its genuine differentiator is **Commercial Data Protection (CDP)**: when a user is signed in with a work or school account, prompts and responses are bounded to the tenant, are not used to train Microsoft's foundation models, and inherit the school's existing data-processing agreement.

The guide's voice is the same as the rest of choosewise.education:
- Calm analytical adult voice, not vendor hype
- Honest where the story breaks (licensing confusion is worth naming up front)
- Practical — teachers can try the five features within a normal workday

**Voice test:** if a sentence could appear in Microsoft's own marketing brochure unchanged, rewrite it.

## The honest licensing problem (set up in Part 1, returned to in Part 3)

Microsoft's naming is the single most confusing thing about this product. Four distinct SKUs share the word "Copilot":

| Name | Who it's for | CDP? | Cost |
|---|---|---|---|
| Copilot (free web) at copilot.microsoft.com | Anyone with a Microsoft Account (MSA) | **No** — consumer terms | Free |
| Copilot Chat with work/school account | Signed-in M365 users | **Yes** — CDP enabled | Free with M365 |
| Copilot Pro | Individuals upgrading consumer Copilot | No — still consumer | Paid |
| Microsoft 365 Copilot | Tenant-licensed seats (teachers/admins) | **Yes** — inside tenant | Paid add-on, ~kr 350/user/mo |

The practical rule for schools: **sign in with the work/school account** every time. That single behavior is the difference between a teacher's prompt staying inside your M365 tenant and a teacher's prompt flowing into a consumer product covered by different terms.

## Structure (copy Apple pattern exactly)

1. Hero (banner title "Microsoft Copilot", subtitle "Chat · Write · Summarise")
2. Anchor nav: Get started · Work smarter · Compliance & licensing · FAQ · Download PDF
3. Part 1 — Get started (01)
4. Part 2 — Work smarter (02)
5. Part 3 — The compliance story (03)
6. FAQ (9–10 items)
7. Dark CTA band
8. License band (CC BY-NC-SA 4.0)
9. Footer

## Part 1 — Get started

Three sub-sections:

**1.1 Which product are you actually using?**
Name the four SKUs plainly. The CDP boundary depends on which one is open. Practical rule: at school, sign in with the work/school account. Anywhere you see the Microsoft 365 Copilot icon inside Word/Excel/PowerPoint/Outlook, CDP is already in effect because you are logged into the tenant.

**1.2 Turning it on (teacher-first)**
- M365 apps (Word, Excel, PowerPoint, Outlook, OneNote, Teams) on macOS and iPadOS: the Copilot icon appears in the ribbon / right-hand pane after the admin grants a M365 Copilot license. No user-side install; it's a server-side flip by the tenant admin.
- Copilot Chat (free with work/school): go to `copilot.cloud.microsoft` or click the Copilot icon in Teams/Edge sidebar. Sign in with work account. CDP is on by default for this path.
- On a personal Mac, download **Microsoft 365 Copilot app** from the Mac App Store for a standalone chat surface that still uses your work login.

**1.3 The commercial data protection boundary — what it actually is**
Explainer box covering:
1. What "commercial data protection" means: prompts/responses not used for training, tenant-bounded, logged under M365 audit and retention rules
2. What it does NOT mean: doesn't eliminate cloud processing, doesn't change the legal basis for processing student data, doesn't cover third-party connectors you approve
3. **EU Data Boundary**: Microsoft's commitment to store and process EU customer data in EU regions — applies to most Copilot operations but not all; verify with procurement contact
4. **Schrems II caveat**: Microsoft is a US-based controller; SCCs + supplementary measures required for EU→US transfers, and the EU Data Boundary reduces but does not eliminate this exposure

Side-note: worth knowing (outside scope):
- Copilot Studio (build custom agents — IT-department scope, not every-teacher)
- Copilot Pro consumer (for personal use — not relevant for school-issued work)

## Part 2 — Work smarter (SIX features)

Each feature gets: what it is, 5 classroom examples, "Where it runs" callout, "How to start", Mac note if relevant.

### 1. Copilot Chat (with your work data)
General-purpose chat with tenant-bounded CDP. Can reference your own files if you grant it (type `/` to anchor in OneDrive/SharePoint docs, with M365 Copilot license). Classroom examples: drafting lesson plans from last year's OneNote, extracting action items from a long meeting transcript, summarising a curriculum document, tone-rewriting a parent email, scaffolding differentiation ideas for mixed-ability groups. Where it runs: Microsoft cloud; CDP enabled when signed in with work account. How to start: open `copilot.cloud.microsoft` or the Copilot icon in Teams.

### 2. Copilot in Word
Draft-from-prompt, rewrite selection, summarise document. Classroom examples: turn a two-bullet outline into a full parent newsletter draft, rewrite a terse report in a warmer register, generate a one-paragraph summary of a 12-page research article, extract a bullet list of key points for staff briefing, produce a Swedish-English parallel version for EAL parents. Where it runs: Microsoft cloud, CDP. How to start: click the Copilot icon in Word's Home ribbon.

### 3. Copilot in Outlook
Summarise long threads, draft replies in a tone, coach-your-writing before send. Classroom examples: triage a morning of parent replies, catch up on a 40-message thread between department heads, soften a too-direct draft before sending to a parent, extract a "what actions do I owe?" list from the last week's inbox, draft a follow-up to yesterday's parent-teacher meeting based on notes in the thread. Where it runs: Microsoft cloud, CDP. How to start: Copilot button in the Outlook ribbon or the sparkle icon in the compose window.

### 4. Copilot in Teams (meeting recap + in-chat help)
Real-time meeting transcript, post-meeting recap with action items, in-chat question answering about what just happened. Classroom examples: generate action items from a department meeting, let a colleague who missed the staff meeting catch up in three minutes, summarise the key decisions from a parent-teacher conference, extract what you personally committed to do, create a shared recap for the staff wiki. Where it runs: Microsoft cloud, CDP. Teachers must explicitly enable recording/transcript — that is a school-policy decision, not a default. How to start: in a Teams meeting, open the Copilot pane on the right.

### 5. Copilot in PowerPoint
Generate slides from a Word doc or an outline, rewrite slide copy, suggest speaker notes. Classroom examples: turn a lesson plan into a 12-slide pack in two minutes, generate speaker notes for a guest-teacher deck, rewrite jargon-heavy slides in student-accessible Swedish, suggest image ideas for each slide topic, tidy existing slide decks for consistency. Where it runs: Microsoft cloud, CDP. How to start: Copilot icon in the Home ribbon of PowerPoint.

### 6. Copilot Pages (shared canvas)
A multiplayer AI-native canvas that sits between chat and document. Classroom examples: draft a unit outline collaboratively with a teaching partner, build a shared resource bank with students (appropriate-age-gated), visualise a decision with pros/cons in a persistent artifact rather than a disposable chat, prep a presentation brief that your teaching assistant can refine, keep a running project notebook for a school improvement working group. Where it runs: Microsoft cloud, CDP. How to start: from a Copilot Chat response, click the "Edit in Pages" option.

## Part 3 — Compliance & licensing in practice

Six sub-sections:

**3.1 What CDP actually gives you**
Bound to tenant, not used for training, inherits DPA and audit/retention. Not magic — it does not change your obligations as controller. Reference the Microsoft Products and Services DPA and Volume Licensing terms. Translate legalese into 3 clear claims: (a) prompts/responses aren't training data, (b) data stays within your tenant's trust boundary, (c) Microsoft acts as processor under your existing DPA.

**3.2 Sign-in = compliance**
Single biggest point of failure: a teacher using consumer Copilot by accident. Show the visual cues: work/school account shield icon at top-right of copilot.cloud.microsoft; the "Protected" badge. Policy: require signed-in use, block consumer Copilot via tenant controls if possible.

**3.3 EU Data Boundary and Schrems II**
Microsoft's EU Data Boundary: covers most Copilot data storage and processing in EU regions. Caveats: some sub-processors still US-based; limited telemetry may cross. Schrems II: SCCs, supplementary measures, and Microsoft's own Data Privacy Framework certification. The honest sentence: this is among the best positions of any major cloud AI product, and it is still a transfer to a US-headquartered processor that should sit in the DPIA.

**3.4 Licensing — which seat does what**
The four SKUs table (copy from Part 1 with added detail on feature access: consumer Copilot = web chat only, Pro = image/video add-ons, M365 Copilot = integration into Word/Excel/PowerPoint/Outlook/Teams + tenant-grounded answers). The cost sentence: M365 Copilot is roughly kr 350/teacher/month — verify current list price. Talk about phased rollouts (start with leadership + subject leads, not full staff).

**3.5 Student access and age limits**
Microsoft's own age floor: 13+ for Copilot with work/school account (aligned with M365 Education terms). Students under 13: cannot be given direct Copilot access; teachers should use it on their own accounts to prepare materials. Above 13: admin gates which features. One concrete recommendation: most schools should start with teacher-only access for a term before enabling student access, even if license permits it. Reader-responsibility note here: verify your country's national rules.

**3.6 Five policy decisions for your school**
1. Require signed-in work/school account for all Copilot use; block consumer Copilot via tenant conditional access if possible.
2. Document Copilot paths in the school DPIA: M365 Copilot, Copilot Chat with work account, and (if allowed) any consumer use by staff on personal devices for adult-only tasks. Cite Microsoft DPA + EU Data Boundary as mitigations.
3. Produce a one-page "what to paste, what to avoid" staff guideline with three accept/three avoid examples tailored to your school. Pin it to the shared staff wiki.
4. Phase the rollout: leadership + subject leads in term 1, broader staff in term 2, student access (if permitted at all) only after the policy is stable. This is specifically Microsoft-tailored: the tenant admin flip is instant but organisational readiness is not.
5. Termly review: Microsoft ships monthly. A 30-minute standing entry each term to skim release notes and update the staff guide is enough to prevent drift.

Reader-responsibility note: readers outside Sweden should verify their own national regulations. AI in education is evolving quickly and country rules differ significantly. Sweden in particular lacks national AI-in-school guidance (April 2026) — Skolverket and IMY are working on joint guidance, date unknown. Countries like the UK, France, Germany, and the Netherlands have already published national guides.

## FAQ (9 items)

1. Which version of Copilot should my school actually use?
2. Do my prompts train Microsoft's AI?
3. Is Copilot available in Swedish?
4. Can I use Copilot with student data?
5. How does Copilot compare to Claude or Gemini?
6. What about Copilot on my personal computer?
7. Is Copilot covered by my school's Microsoft Data Processing Agreement?
8. Can I turn off specific Copilot features for certain staff groups?
9. Where do I get help if something goes wrong?

(Full answers to be authored — same length and voice as Apple FAQ)

## Six Quick Start features (for 2-page PDF)

Same six as Part 2, compressed to one-liner + subtitle in the grid. Five "Try it today" tasks:
1. Rewrite a parent email in three tones in Outlook
2. Summarise a long thread in Outlook
3. Generate a Teams meeting recap with action items
4. Turn a Word outline into PowerPoint slides
5. Draft a differentiation plan in Copilot Chat

Watch-out line: "Sign in with your work/school account. Consumer Copilot is a different product under different terms. De-identify student data before any prompt. Verify your country's rules."

## Cover SVG

Already exists at `/assets/images/guide-covers/copilot.svg` — graphite → forest green gradient with "Copilot" text. Keep as-is.

## Translation notes for SV mirror

- "School leaders" → "skolledare"
- "Teachers" → "lärare"
- "Tenant" → use the English term "tenant" (common M365 parlance in Sweden) on first use, introduce with "tenanten (organisationens Microsoft 365-miljö)"
- "Commercial Data Protection" → "Kommersiellt dataskydd (CDP)" on first use
- "Sign-in" → "inloggning"
- "Work or school account" → "arbets- eller skolkonto"
- "EU Data Boundary" → keep English term on first use, gloss as "EU-datagräns"
- "School's DPIA" → "skolans konsekvensbedömning (DPIA)"
- "School Policy" → "skolans policy"

Keep Swedish-specific references: Skolverket, IMY, rektor, huvudman, Lgr22.
