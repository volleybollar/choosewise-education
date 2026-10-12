"Software is over." That was the line doing the rounds in the first week of October, and most of the coverage agreed with it.

Here is what actually happened. A developer called Brandon Thomas published seven applications on GitHub: PhotoCraft, FilmCraft, LightCraft, PDFCraft, VectorCraft, EffectCraft and DesignCraft, each aimed at an Adobe product that millions of people pay for every month. All free, all open source under MIT and Apache-2.0, all written from scratch in Rust. He didn't write them by hand. He ran eight Claude Opus 5.5 agents in parallel and says he "one-shotted Photoshop". Within days the repositories had collected tens of thousands of stars, PhotoCraft alone sitting at roughly 50,000 as I write this.

If you sell software for a living, that is the story you have been told to be frightened of. Adobe's share price has a different opinion, and the distance between those two readings is where this gets interesting.

## What the share price actually did

An extinction event should be visible in the market. Here is Adobe's closing price for the week the story broke:

<figure class="data-table">
  <table class="adbe-table">
    <caption>Adobe (ADBE), daily close, 1–9 October 2026</caption>
    <thead>
      <tr>
        <th scope="col">Date</th>
        <th scope="col" class="num">Close</th>
        <th scope="col" class="num">Change</th>
      </tr>
    </thead>
    <tbody>
      <tr><th scope="row">1 Oct</th><td class="num">$241.28</td><td class="num">+0.56%</td></tr>
      <tr><th scope="row">2 Oct</th><td class="num">$237.69</td><td class="num">−1.49%</td></tr>
      <tr><th scope="row">5 Oct</th><td class="num">$238.79</td><td class="num">+0.46%</td></tr>
      <tr><th scope="row">6 Oct</th><td class="num">$238.12</td><td class="num">−0.28%</td></tr>
      <tr class="is-marked"><th scope="row">7 Oct</th><td class="num">$232.77</td><td class="num">−2.25%</td></tr>
      <tr><th scope="row">8 Oct</th><td class="num">$241.05</td><td class="num">+3.56%</td></tr>
      <tr><th scope="row">9 Oct</th><td class="num">$242.27</td><td class="num">+0.51%</td></tr>
    </tbody>
  </table>
  <p class="data-table__source">Highlighted row: the day the clone story reached the technology press at scale. Source: closing prices via stockanalysis.com.</p>
</figure>

<style>
.adbe-table { width: 100%; border-collapse: collapse; font-size: 0.95rem; margin: 1.2rem 0 0.6rem; }
.adbe-table caption { caption-side: top; text-align: left; font-weight: 600; padding-bottom: 0.6rem; }
.adbe-table thead th { background: var(--color-text); color: var(--color-bg-alt); text-align: left; padding: 0.55rem 0.7rem; font-weight: 600; }
.adbe-table thead th.num { text-align: right; }
.adbe-table tbody th { text-align: left; font-weight: 400; padding: 0.45rem 0.7rem; border-bottom: 1px solid var(--color-border); }
.adbe-table tbody td { text-align: right; padding: 0.45rem 0.7rem; border-bottom: 1px solid var(--color-border); font-variant-numeric: tabular-nums; }
.adbe-table tbody tr.is-marked th, .adbe-table tbody tr.is-marked td { background: var(--color-bg-alt); color: var(--color-highlight-ink); font-weight: 500; }
.data-table__source { font-size: 0.85rem; color: var(--color-text-soft); margin-top: 0.4rem; }
</style>

There's a 2.25% dip on 7 October, the day the story reached the technology press at scale. It was gone by the next afternoon, and the week closed higher than it opened. The context matters more than the week does: Adobe closed at $286.08 on 1 September, and against the 52-week high of $363.70 about a third of the company's market value is gone.

That repricing happened before seven free clones existed. The market had already concluded that generative AI undermines the business of renting out creative tools, so the clones didn't deliver the verdict. They illustrated it. The threat was never that somebody would rebuild Photoshop; it's that the answer to "what am I paying for?" has become harder to give.

## The short run, for the individual and the school

For someone who needs to crop a photograph, redact a PDF or cut a two-minute video, the arithmetic is attractive. No licence, no account, no renewal, and no cancellation fee (the specific grievance Thomas has said set him off in the first place).

But free at the point of download isn't the same thing as free. PhotoCraft had 792 open issues on 12 October, a week after launch, and reviewers call the apps capable and glitchy at once, an early alpha that feels startlingly close to the real thing until it doesn't. None of that is scandalous for a one-week-old project. It is, however, the part of the cost that never appears on an invoice, and in a school the person absorbing it is usually an IT coordinator who didn't choose the tool and a teacher who loses the lesson.

So "free" changes the procurement conversation, and it should. But the question to put to a free alternative is the one you should already be putting to a paid one: what does this cost over five years including support, migration, patching and data protection, and who carries it when it breaks at eight on a Tuesday morning? Sometimes the free tool wins outright. Sometimes the subscription was never really about the software, and I've sat on the buying side often enough to know the second case is more common than the invoice suggests.

A file format is also a promise about the future, and a free tool with one sponsor is a weaker promise than a subscription you resent paying. Don't ask whether a free replacement opens your files today. Ask who will be fixing it in three years, and what becomes of the school's archive if the answer is nobody.

## The short run, for the company

Adobe's problem isn't that PhotoCraft has layers and masks. It's that the clones make the price visible. Once a credible free alternative exists, every renewal turns into a decision rather than a default, and a business built on defaults feels that immediately, as churn at the bottom of the market, long before anything shows up in enterprise revenue. The clones also put a number on something Adobe's competitors can now reason about: if seven applications can be approximated in a week by one person with agent time, the wall that protected the category was never as high as the engineer-years suggested. That wall was never patented. It was simply expensive.

## The long run: does anyone keep building?

Kenneth Arrow set up the problem in 1962: an innovator invests only if the returns can be captured, and information is unusually hard to capture because it is cheap to copy. The empirical anchor came in Mansfield, Schwartz and Wagner's 1981 study in *The Economic Journal*, which found that around 60% of patented innovations were imitated within four years, at a cost of somewhere between 40% and 90% of the original development.

That ratio decides everything. At 0.9, copying barely pays. At 0.1, the innovator's payback window shuts before it opens. What AI agents do is push the ratio down hard for one class of product: software whose behaviour is fully observable from the outside. Nobody needs Adobe's source code to rebuild a gradient tool; they need to watch what it does. That is why these are *clean-room* reimplementations and why they are probably lawful, since functionality isn't what copyright protects and *Google v. Oracle* (2021) established that even verbatim copying of interface code can be fair use.

The pessimistic reading is that nobody will fund the next Photoshop. I think that's probably wrong, for a reason David Teece set out in 1986: when imitation is easy, the returns flow to whoever controls the complementary assets, meaning distribution, brand, installed base, service and data. Innovation carries on; it just changes address.

We have watched this before. In 1984 Phoenix Technologies clean-room reverse-engineered IBM's PC BIOS and licensed it to all comers. IBM lost the platform it had invented, the market exploded rather than shrank, and the value migrated to the two layers nobody had cloned: Microsoft's operating system and Intel's instruction set.

If that pattern holds, cheap copying gives us not a smaller software industry but a differently shaped one, with the value pooling in whatever stays expensive: proprietary data, network effects, regulatory trust, integration into workflows people can't leave. Large incumbents own most of that, which leads somewhere less comforting than "innovation survives". The firm most exposed is not Adobe, with its enterprise contracts and its balance sheet, but the small independent developer selling a good $49 utility into a niche and owning no complementary assets whatsoever. Cheap imitation doesn't flatten an industry evenly. It hollows out the middle.

## The asymmetry nobody is pricing

Writing software has become dramatically cheaper. Maintaining it hasn't, and that gap is where I'd put my attention over the next few years.

GitClear's analysis of 211 million changed lines found duplicated code blocks rising sharply while refactoring, the work that keeps a codebase maintainable, fell from 25% of changed lines in 2021 to under 10% in 2024. METR's randomised trial in 2025 found experienced open-source developers working 19% *slower* with AI tools while believing they were 20% faster, though METR now says that result is outdated. Treat the direction as uncertain. We are producing code faster than we are producing evidence about what it costs to keep.

The commons all this depends on is already stretched. Hoffmann, Nagle and Zhou at Harvard Business School put the demand-side value of widely used open-source software at $8.8 trillion against a supply-side replacement cost of $4.15 billion, and that leverage rests on a small number of maintainers, most of them unpaid. Adding seven large Rust applications to the pile in a week is a gift. It is also 792 open issues looking for a volunteer.

## The thing that gets better

There is an upside here that the "software is over" framing misses entirely, and it belongs to the individual.

Every time a story like this circulates, a few thousand people go and try it. Some open the repository, read the issues and understand for the first time what an open-source project actually is. A smaller number point an agent at a problem of their own and discover that the little tool they have wanted for years, the one nobody would ever build because the market for it is eleven people, can now exist by Friday.

That is a fast and real increase in practical AI competence, distributed far more widely than the ability to write code ever was. The person who commissions software from an agent learns what no subscription ever taught them: what these systems are good at, where they fail, and how much of the work is specifying the problem rather than solving it. The 792 open issues are part of that education rather than an argument against it. Producing something that looks finished is now easy; judging whether it *is* finished is the skill that separates the people who benefit from this shift from the people who get burned by it.

## What schools should take from this

**Teaching.** If a credible clone of a professional tool can be produced in a week, tool-specific instruction depreciates faster than it used to. The durable content was never the menu structure anyway. It's the concept underneath: non-destructive editing, what a mask actually is, why colour management exists, how a timeline behaves. Teach those and the student can sit down in front of Photoshop, PhotoCraft or whatever replaces both. This is the *I — Inspect what the subject requires* step of [the WISE Framework](/wise/) doing real work.

**Careers advice.** We have spent a decade telling students that employability runs through tool proficiency. The tool is now the cheapest input in the chain. What stayed scarce is the judgment about what is worth making and whether the result is any good, which is, inconveniently for everyone designing a curriculum, also the hardest thing to assess.

## Where I land

What has changed is the cost of imitation, which moves the returns rather than destroying them: more software, worse maintained, the profit collecting in fewer firms that own something a model can't regenerate by watching it work, and a great many more people who know how to make a machine build something.

So, when the copy becomes free, what is left that you were actually paying for? Ask it about your creative suite, then about your learning platform, your assessment system and your student information system, because none of them are harder to rebuild than Photoshop.

— Johan

---

**Sources:** [ArtCraft repositories](https://github.com/storytold) · Adobe closing prices via [stockanalysis.com](https://stockanalysis.com/stocks/adbe/) · Mansfield, Schwartz & Wagner, "Imitation Costs and Patents: An Empirical Study", *The Economic Journal* 91 (1981) · Teece, "Profiting from Technological Innovation", *Research Policy* 15 (1986) · [Google LLC v. Oracle America, Inc. (2021)](https://www.eff.org/deeplinks/2021/04/victory-fair-use-supreme-court-reverses-federal-circuit-oracle-v-google) · [Hoffmann, Nagle & Zhou, "The Value of Open Source Software", HBS Working Paper 24-038](https://www.hbs.edu/ris/Publication%20Files/24-038_51f8444f-502c-4139-8bf2-56eb4b65c58a.pdf) · [GitClear, AI Copilot Code Quality 2025](https://www.gitclear.com/ai_assistant_code_quality_2025_research) · [METR, Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
