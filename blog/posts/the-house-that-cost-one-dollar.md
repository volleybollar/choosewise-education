The debate about AI in schools is almost always a debate about access. Should the phones be locked away, should screen time come down, should the textbooks go back to paper? Those are reasonable questions at classroom level, and I am not dismissing them. But they all rest on the same assumption: that access to AI is something a school can regulate.

There is one number that makes that assumption hard to defend.

## A factor of 13 a year

In September 2026 Epoch AI published an analysis of what it costs to reach a *given* level of performance with AI ([The Plunging Price of Thought](https://epoch.ai/publications/the-plunging-price-of-thought)). The conclusion: the cost has fallen by roughly 47 per cent per quarter since 2023 — that is, by a factor of about 13 per year.

Note what is being measured. Not the price per token, and not the price of "AI" in general. What is measured is what it costs to reach a fixed level of quality, across five different task types (among them advanced mathematics problems, science questions at doctoral level and chess puzzles). Same task, same result — at a fraction of the cost.

One example from the report: on GPQA Diamond, a set of expert-level science questions, the cost of reaching 75 per cent accuracy fell from about 30 cents to four ten-thousandths of a dollar per question. In eighteen months. Something over 700 times cheaper, for the same answer.

The authors compare the pace to other technology shifts: four times faster than DNA sequencing, six times faster than computing power, and some 50 times faster than electricity managed over the period 1892–1973.

## A worked example: your house

The trouble with numbers of that kind is that they tell us nothing. We hear "a factor of 13 per year" and nod. So let us swap AI for something we actually have a feel for.

Picture a house that costs a million dollars. Picture the price — same house, same street, same condition — falling at exactly the rate Epoch has measured.

<figure class="module-figure">
  <img src="/blog/posts/assets/house-staircase.webp" alt="Staircase chart: the price of the house falls from $1,000,000 today to $1 after 5.39 years, one step per year." loading="lazy" decoding="async">
  <figcaption>Every step down is one year — and one thirteenth of the price.</figcaption>
</figure>

<figure class="data-table">
  <table>
    <caption>The price of the house year by year, falling by a factor of 13 per year</caption>
    <thead>
      <tr>
        <th scope="col">Time</th>
        <th scope="col">Price</th>
        <th scope="col">Roughly equivalent to</th>
      </tr>
    </thead>
    <tbody>
      <tr><th scope="row">Today</th><td>$1,000,000</td><td>a house</td></tr>
      <tr><th scope="row">After 1 year</th><td>$76,900</td><td>a new car</td></tr>
      <tr><th scope="row">After 2 years</th><td>$5,920</td><td>an e-bike</td></tr>
      <tr><th scope="row">After 3 years</th><td>$455</td><td>a pair of expensive shoes</td></tr>
      <tr><th scope="row">After 4 years</th><td>$35</td><td>a pizza</td></tr>
      <tr><th scope="row">After 5 years</th><td>$2.69</td><td>a cup of coffee</td></tr>
      <tr><th scope="row">After 5.39 years</th><td>$1</td><td>a dollar bill</td></tr>
    </tbody>
  </table>
</figure>

After five years and five months the house costs one dollar. One millionth of the starting price.

> The price halves every three months.

(Every quarter you wait buys you twice as much house for the money — which of course also means that whoever bought yesterday paid twice too much.)

## Why don't we see it coming?

We are built to think in straight lines. If something got a little cheaper this year, we assume it will be a little cheaper next year too. Exponential change doesn't work that way, and that shows most clearly if you draw it.

<figure class="module-figure">
  <img src="/blog/posts/assets/house-linear-scale.webp" alt="Line chart on a linear scale: the curve plunges during year 1 and then lies flat along the bottom." loading="lazy" decoding="async">
  <figcaption>On an ordinary scale the fall looks like a cliff followed by nothing.</figcaption>
</figure>

After year 1 the line sits practically at zero, and the rest of the chart is a straight line along the bottom. That is where our intuition stops: it's cheap now, done.

<figure class="module-figure">
  <img src="/blog/posts/assets/house-log-scale.webp" alt="The same data on a logarithmic scale: a straight, descending line from $1,000,000 to $1." loading="lazy" decoding="async">
  <figcaption>The same numbers, logarithmic scale. The fall continues all the way down.</figcaption>
</figure>

The same numbers on a logarithmic scale become a straight, descending line that carries on at an unchanged pace long after the first chart gave up. The difference between $35 and $1 is invisible in the first chart. In practice it is the difference between "expensive for most people" and "free for everyone".

That is where the point lies. When something has fallen so far that we perceive it as free, it carries on falling anyway — and that is the stage at which access stops being a question of money.

<section class="pricefall" id="pricefall">
  <link rel="stylesheet" href="/blog/posts/assets/house-pricefall.css">
  <h2 class="pricefall__title">Pull the numbers around yourself</h2>
  <p class="pricefall__intro">Move the slider, or drag directly in the chart, and switch between the two scales.</p>
  <div class="pricefall__readout">
    <span class="pricefall__price">$455</span>
    <span class="pricefall__equiv">roughly a pair of expensive shoes</span>
    <span class="pricefall__when">after 3 years</span>
  </div>
  <div class="pricefall__controls">
    <div class="pricefall__slider">
      <label class="pricefall__cap" for="pricefall-year">Time from today</label>
      <input type="range" id="pricefall-year" min="0" max="6" step="0.01" value="3">
    </div>
    <fieldset>
      <legend class="pricefall__cap">Scale on the y-axis</legend>
      <div class="pricefall__segmented" role="group" aria-label="Choose scale">
        <button type="button" id="pricefall-lin" aria-pressed="false">Linear</button>
        <button type="button" id="pricefall-log" aria-pressed="true">Logarithmic</button>
      </div>
    </fieldset>
  </div>
  <svg class="pricefall__chart" viewBox="0 0 760 420" role="img" aria-label="Chart of the house price falling by a factor of 13 per year"></svg>
</section>
<script defer src="/blog/posts/assets/house-pricefall.js"></script>

## What does that mean for an education system?

If the direction holds, even halfway, this is what we have to work with: intelligence — the artificial kind — will in practice be freely available to every student, independent of whether the school has made up its mind or not. Not as a line in an IT budget, but as something sitting in the phone, in the browser and in the word processor without anyone having actively chosen it.

The ban position then collapses under its own logic. A ban is an instrument that presupposes control over access. As a classroom rule it can work, and sometimes it is the right decision precisely there. But as a strategy for an education system it rests on a precondition that the curve is in the process of removing.

So the question is not how we keep AI out. It is: what should a student be able to do in a world where the answer is always free and immediate? Which abilities become worth more, not less, when producing text costs nothing?

## The caveats

I am not going to overstate the certainty of the figure. Epoch's own objections are reasonable:

- The data series is only three years long.
- The models may be optimised for the very tests being measured, which probably overstates general capability.
- Ordinary users don't switch model the moment a cheaper one appears, so the saving an individual user makes is smaller than the one measured at the frontier.
- The authors are themselves clear that the figures are representative, not exact.

The pace may therefore turn out to be a factor of 5 a year rather than 13. That is no comfort. It simply means the house takes eight years instead of five.

## In conclusion

We discuss screens because screens are visible and can be regulated. The price of thinking is invisible and cannot be regulated. Of the two, the second is the one that will decide what school looks like in the years ahead.

This is how I would turn the question around the next time it comes up in a leadership team: if we assume that in three years every student has access to the capability that today costs a fortune — what do we need to start doing today?

---

*Source: Luke Emberson & David Roodman, ["The Plunging Price of Thought"](https://epoch.ai/publications/the-plunging-price-of-thought), Epoch AI, 22 September 2026. The house is a worked example to illustrate the pace of Epoch's measurement — not a forecast about the housing market.*
