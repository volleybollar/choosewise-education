A teacher hears a confident claim at a CPD session: "this approach has been shown to add seven months of progress." She goes back to school, considers reorganising her planning around it, and then pauses. *Who measured that? Across what students? When? What if it's wrong?*

She has no realistic way to find out. Not in the twenty minutes she has between lessons. And the people she could ask — consultants, publishers, leaders — are often the same people who introduced the claim in the first place.

This is the problem the [Evidence Toolkit](/evidence/) is built to solve.

## The verification gap

Education has a quiet structural problem: most teachers cannot directly interrogate the research behind the practices they're asked to adopt. Tens of thousands of studies are published every year, mostly behind paywalls, written in a register that takes training to decode. So an industry of intermediaries — consultants, books, social media accounts, framework vendors — has grown up to translate research for teachers.

That layer is mostly well-meaning. It is also where the evidence base gets simplified, repackaged, and sometimes inflated. By the time a claim reaches a CPD slide, it has often lost the caveats that made it true in the first place.

The result is what researchers call *instructional churn*: a cycle of confident fads, modest results, quiet retreat, then a new confident fad. Teachers are tired of it. They have every reason to be.

## What the toolkit does

The Evidence Toolkit is a growing reference page that lets you see — at a glance — which teaching interventions have the strongest evidence-based effect on learning, with the source for every number cited by name and year. You can filter by domain, sort by effect size, and search by tag. It launches with eight interventions in **Memory & Learning Science**, with more domains added over time.

Two things make it different from existing toolkits:

**The toolkit uses an existing open skill library as its spine, but does not trust the spine's labels.** It builds on [Gareth Manning's open-source Claude Education Skills](https://github.com/GarethManning/claude-education-skills) — 114 evidence-grounded teaching prompts. But for every skill on the toolkit, the effect size is cross-referenced to an independent peer-reviewed meta-analysis, by name, with publication year visible on the card. Where the independent evidence base is missing, the card says so openly rather than hiding the gap.

**Every card carries a prompt builder for interrogating the claim in any AI chatbot.** This is the structural answer to the verification problem. Click "Interrogate this claim" on any card, copy the generated prompt, paste it into ChatGPT, Claude, or Gemini. The prompt is engineered to ask the model to cite real meta-analyses (not fabricate them), separate strong from weak evidence, name boundary conditions, flag common exaggerations, and discuss cost-effectiveness. It even tells the model to use its reasoning or "thinking" mode for the analysis. Use it for our cards. Use it for any claim you hear anywhere. That is the point.

## What it shows you — and what it doesn't

Each card shows effect size two ways: **months of progress** (the EEF Toolkit's teacher-friendly shorthand, where available) and **Cohen's d** (the standardised academic effect size). When the two metrics disagree on band — as they do for Feedback, where d = 0.48 looks moderate and +6 months looks high — the card shows the disagreement openly. Different meta-analyses measure different things; that is itself informative.

Numbers are colour-coded using calibration bands — **below typical**, **around typical**, **above typical** — relative to Hattie's "hinge point" of about d = 0.40, which is the average effect of a year of schooling. The colours signal calibration, not value judgment. A skill in the "below typical" band is not a bad skill; it is one whose average effect is smaller than the typical schooling effect, which can still be appropriate for specific contexts the average does not capture.

Each card also carries an **implementation cost** — Low, Medium, or High — for what your school actually has to invest in teacher time, training, and structural change to run the intervention well. This is the editorial team's read of practical effort, not a monetary figure. For UK £ cost data on the interventions the EEF have priced, the toolkit links straight back to the [EEF Teaching & Learning Toolkit](https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit).

## Where this sits in the WISE Framework

Evidence Toolkit is the **S — Select the right tool** step of [the WISE Framework](/wise/). After you've weighed the learning goal (W) and inspected what the subject calls for (I), this is where you select the teaching move with the strongest evidence base for *your* context. Then you evaluate the outcome (E) — and run the cycle again.

## What's coming

Eight skills today. The next domain in the queue is **Feedback & Formative Assessment** (~13 interventions). After that: Explicit Instruction, Self-Regulated Learning, Questioning & Discussion. Domain by domain, hand-verified, in public.

Each release is small enough to read in one sitting and grounded enough that you can defend any claim on the page in a staff meeting. That's the bar. If a claim ever can't clear it, the prompt builder is there — for our claims as much as anyone else's.

Open the [Evidence Toolkit](/evidence/) — and let me know which intervention you wish was on it next.

— Johan
