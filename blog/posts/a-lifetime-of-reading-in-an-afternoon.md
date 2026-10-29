Picture a genuinely keen reader: someone who reads fiction for an hour every day, all year round, for fifty years.

Over those fifty years they get through a remarkable amount of literature:

- 3,650 books (73 a year)
- about 1.1 million pages
- roughly 274 million words
- 18,250 hours of reading

That is more than two years of uninterrupted reading, day and night, without sleep.

I recently worked through the numbers on how long a modern AI model would need to process the same pile of text. The answer says less about books than it does about the choices in front of us in education.

## Reading: 18,250 hours against about four

AI models do not read words. They process tokens (whole words, parts of words and punctuation). OpenAI's own rule of thumb is that 100 tokens correspond to about 75 English words, which turns our 274 million words into roughly 365 million tokens, or about 100,000 tokens per novel.

Two current OpenAI models make a useful comparison: GPT-6 Astra, one of the most capable (and expensive) models available, and GPT-6 Luna, a far cheaper model built for speed and volume. Both can take in an entire novel in a single request.

In September 2026 Epoch AI published measurements of how quickly frontier models process long inputs ([Latency scaling differences for GPT and Claude models](https://epoch.ai/publications/long-context-latency-scaling-gpt-vs-claude)). Based on their figures, GPT-6 Astra needs about 3.6 seconds to take in a full novel. There is no comparable published measurement for Luna, so I have assumed 3 seconds per book (a cautious figure, since Epoch measured a similar budget model at about 1.3 seconds).

Fed one book at a time, the result looks like this:

<figure class="module-figure">
  <img src="/blog/posts/assets/reading-time.webp" alt="Bar chart on one scale: a keen reader spends 18,250 hours on 3,650 novels over 50 years. GPT-6 Astra processes the same text in about 3.7 hours and GPT-6 Luna in about 3 hours, bars so short they are barely visible." loading="lazy" decoding="async">
  <figcaption>Same books, same scale. The AI bars are 0.02 per cent as long as the human one.</figcaption>
</figure>

To keep the comparison honest, I am comparing actual reading time with processing time, not fifty calendar years with an afternoon. So: 18,250 hours for the human reader against about 4 hours for the AI. That is still a factor of around 5,000. If the human's reading were a 100-metre running track, the AI would be finished after two centimetres.

## Reading on its own is worth nothing

Passing text through a model creates no value by itself. The interesting question is how much time it takes to actually do something with what has been read. So I added a task: for every single book, write a structured analysis of about 1,000 words covering plot, characters, themes and the main conclusions.

That adds two things. The first is thinking time, which I have set at 10 extra seconds of reasoning per book (a deliberate simplification). The second is writing time, which can be measured: [Artificial Analysis](https://artificialanalysis.ai/) clocks GPT-6 Astra at roughly 55 tokens per second and Luna at roughly 115.

<figure class="module-figure">
  <img src="/blog/posts/assets/reading-and-analysis.webp" alt="Stacked bar chart: GPT-6 Astra needs about 41 hours to read all 3,650 novels and write an analysis of each, of which about 4 hours are reading. GPT-6 Luna needs about 26 hours, of which about 3 hours are reading." loading="lazy" decoding="async">
  <figcaption>Zoomed in on the AI: most of the time goes on the analysis, not the reading.</figcaption>
</figure>

Reading plus a structured analysis of all 3,650 books comes to:

- **GPT-6 Astra:** about 41 hours, i.e. under two days
- **GPT-6 Luna:** about 26 hours, i.e. just over a day

Note one counter-intuitive detail: the expensive model is the slower one here, because it writes at half the speed. Higher capability does not automatically mean higher speed. It may well mean a better analysis, but that is a separate question.

Fifty years of reading, with an analysis of every book, in one to two days.

## Cost and pace: the part that should make us stop

At OpenAI's list prices ($10 per million input tokens for Astra, $0.10 for Luna), reading and analysing all 3,650 books costs around $4,000 with Astra and around $40 with Luna.

Forty dollars.

And it will not stay at forty. Epoch AI has measured the cost of reaching a given level of AI performance falling by about 13 times a year. If that pace continues, the same job will cost around three dollars a year from now and about 25 cents in two years. Even at a more cautious five times a year, it drops below two dollars within two years. I have written more about what that kind of curve means in [The house that cost one dollar](/blog/posts/the-house-that-cost-one-dollar.html).

And this, I think, is what matters most. When GPT-4 was launched in March 2023 it cost $30 per million input tokens and could hold about 8,000 tokens at a time. It could not even take in one novel: 8,000 tokens is about 8 per cent of a book. Even if the text had been cut into pieces, the input alone would have cost around $11,000. Three and a half years later, a budget model takes in the whole novel in one go, and the input cost for fifty years of reading has fallen to under $40.

<figure class="module-figure">
  <img src="/blog/posts/assets/reading-cost.webp" alt="Bar chart of the input cost for 365 million tokens: GPT-4 in March 2023 $10,950, GPT-6 Astra in October 2026 $3,650, GPT-6 Luna in October 2026 $36.50." loading="lazy" decoding="async">
  <figcaption>The same pile of text, three and a half years apart.</figcaption>
</figure>

That is what exponential development looks like in practice. Not a slightly better tool every year, but things that were impossible becoming routine and cheap within the lifetime of a single school strategy.

## Processing is not understanding

There is a fair objection here. The AI has not experienced 3,650 books. It has not been moved by them, and it does not carry fifty years of reading with it the way a person does. Each book is processed separately, and drawing conclusions across all of them requires further steps.

All true. But it is not my point. My point is the capacity: the sheer volume of information that can now be processed, analysed and summarised, quickly and cheaply. And the question that every school leader, education authority and ministry should be asking is where in education that capacity could create real value.

## Where it gets interesting for schools

Here is one idea I keep coming back to.

A teacher who stays in the profession for 40 years teaches roughly 30,000 lessons. That is an approximate figure: in Sweden a full-time teacher's starting point is around 18.5 hours of teaching a week, many lower-secondary teachers teach more than that, and lesson length varies with subject and with the age of the pupils. Whether the true figure is 10 per cent higher or lower makes no real difference, as the reasoning holds either way. Everything that teacher learns about what works (which explanations land, which tasks lift which pupils, which approaches quietly fail) comes from that one sample. A large sample by human standards. A tiny one by the standards of a school system.

In Sweden, with around 141,000 full-time teaching posts (2024/25), far more lessons than that are taught every ordinary school morning.

<figure class="module-figure">
  <img src="/blog/posts/assets/reading-lessons.webp" alt="Bar chart: one teacher teaches about 30,000 lessons over a 40-year career, while Sweden's teachers teach at least 141,000 lessons in a single school morning." loading="lazy" decoding="async">
  <figcaption>A whole career's worth of lessons is less than a quarter of one Swedish school morning.</figcaption>
</figure>

Today almost all of that experience disappears when the bell rings. The knowledge that does reach teachers systematically comes through research: trials, evaluations and meta-analyses that take years to produce and even longer to reach the classroom (and often arrive in a form that is hard to turn into Monday's lesson).

Now imagine that we broke teaching down into its components and continuously collected data on which ways of teaching lead to which learning, for which pupils. That data could be analysed at the scale we have just seen, compiled into something a teacher can actually use, and sent out to every teacher in the country.

A newly qualified teacher would then start their career with a knowledge bank weightier than anything a single teacher could build up over a whole working life.

I believe that could improve a country's school system more than anything else we know of today.

## The problems are real. So is the cost of not starting.

There are hard problems to solve along the way, and I have no wish to play them down:

- **Data:** how do we collect, store and protect data about pupils and teachers in a way that is lawful, secure and trusted?
- **Breaking down teaching:** what are the meaningful units of a lesson, and how do we capture them without reducing teaching to a checklist?
- **Linking teaching to learning:** how do we connect what happened in the classroom to what pupils actually learned, not just what they scored on the next test?
- **Trust:** how do we build this as professional support for teachers rather than a surveillance system?

None of these is trivial. But they are problems to investigate, not reasons to stand still. If we never begin to explore what this new capacity makes possible, we will never get there.

The books are only an illustration. There are surely many more places in education where this kind of capacity could add real value for teachers and for pupils' learning.

Where would you start? What do you think?

## How I calculated

- **Reading speed:** 250 words per minute, rounded down from 260 for fiction in Brysbaert's 2019 meta-analysis of 190 studies (*Journal of Memory and Language*).
- **A novel:** 300 pages × 250 words = 75,000 words (my estimate). One hour a day gives one book every five days.
- **Tokens:** 1 token ≈ 0.75 English words (OpenAI's rule of thumb).
- **Input processing:** GPT-6 Astra from Epoch AI's latency measurements (September 2026). GPT-6 Luna: my assumption of 3 seconds per book, as no measurement has been published.
- **Writing speed:** Artificial Analysis, October 2026 (Astra about 55 tokens per second, Luna about 115).
- **Analysis:** 1,500 output tokens (about 1,000 words) plus 10 seconds of reasoning per book (my assumption).
- **Prices:** OpenAI list prices, October 2026. GPT-4 at its March 2023 launch price.
- **Lessons:** about 18.5 hours of teaching a week (the Swedish starting point for a full-time teacher), roughly one hour per lesson, 38 weeks a year, 40 years. That gives about 28,000, rounded up to 30,000 since many teachers teach more. The figure is approximate, and 10 per cent either way does not change the argument. Around 141,000 full-time teaching posts in Sweden in 2024/25.
- All AI times assume one book per request, processed one after another, with no rate limits. They are calculations, not measured end-to-end runs. Not every detail will be exact, but the size of the gap holds even with generous margins.
