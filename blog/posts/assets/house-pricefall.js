/*
  Interactive chart for the post "The house that cost one dollar".

  The model: a house costing $1,000,000 whose price falls by a factor of 13
  per year — the same pace Epoch AI has measured for the cost of reaching a
  given level of performance with AI.

  The script redraws the whole SVG on every change. That is cheap enough here
  (a couple of hundred points) and keeps the code easy to follow: one function
  that calculates, one that draws, one that updates the text.
*/
(function () {
  'use strict';

  var root = document.querySelector('.pricefall');
  if (!root) { return; }

  var START = 1000000;   // starting price in dollars
  var RATE = 13;         // times cheaper per year
  var T_MAX = 6;         // length of the slider, in years

  function price(t) { return START / Math.pow(RATE, t); }

  // Everyday comparisons, dearest first. The first match wins.
  var EQUIVALENTS = [
    [400000, 'roughly a house'],
    [60000, 'roughly a new car'],
    [15000, 'roughly a second-hand car'],
    [3000, 'roughly an e-bike'],
    [1000, 'roughly a sofa'],
    [300, 'roughly a pair of expensive shoes'],
    [120, 'roughly dinner for two'],
    [25, 'roughly a pizza'],
    [6, 'roughly a cinema ticket'],
    [1.5, 'roughly a cup of coffee'],
    [0.5, 'roughly a dollar bill'],
    [0, 'less than a dollar']
  ];

  function equivalent(v) {
    for (var i = 0; i < EQUIVALENTS.length; i++) {
      if (v >= EQUIVALENTS[i][0]) { return EQUIVALENTS[i][1]; }
    }
    return '';
  }

  // Number formatting: thousands separators, and cents below ten dollars.
  var nf0 = new Intl.NumberFormat('en-US', { maximumFractionDigits: 0 });
  var nf2 = new Intl.NumberFormat('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  function usd(v) {
    return '$' + (v >= 10 ? nf0.format(Math.round(v)) : nf2.format(v));
  }

  // ── Chart geometry ──
  // The margins leave room for the labels so that nothing lands outside the viewBox.
  var W = 760, H = 420, ML = 86, MR = 22, MT = 18, MB = 44;
  var PW = W - ML - MR, PH = H - MT - MB;

  function xAt(t) { return ML + PW * (t / T_MAX); }

  // The log scale runs from $0.10 (10^-1) to $10M (10^7): eight decades, which
  // leaves the curve clear of both the top and the bottom of the plot.
  var LOG_MIN = 0.1, LOG_DECADES = 8;

  function yAt(v, log) {
    if (log) {
      return MT + PH * (1 - (Math.log(Math.max(v, LOG_MIN)) / Math.LN10 + 1) / LOG_DECADES);
    }
    return MT + PH * (1 - v / START);
  }

  var LIN_TICKS = [[1e6, '$1M'], [8e5, '$800k'], [6e5, '$600k'],
                   [4e5, '$400k'], [2e5, '$200k'], [0, '0']];
  var LOG_TICKS = [[1e7, '$10M'], [1e6, '$1M'], [1e5, '$100k'], [1e4, '$10k'],
                   [1e3, '$1,000'], [100, '$100'], [10, '$10'], [1, '$1'],
                   [0.1, '$0.10']];

  var chart = root.querySelector('.pricefall__chart');
  var slider = root.querySelector('#pricefall-year');
  var btnLog = root.querySelector('#pricefall-log');
  var btnLin = root.querySelector('#pricefall-lin');
  var elPrice = root.querySelector('.pricefall__price');
  var elEquiv = root.querySelector('.pricefall__equiv');
  var elWhen = root.querySelector('.pricefall__when');

  var useLog = true;

  function line(cls, x1, y1, x2, y2) {
    return '<line class="' + cls + '" x1="' + x1 + '" y1="' + y1 +
           '" x2="' + x2 + '" y2="' + y2 + '"/>';
  }

  function text(cls, x, y, anchor, body) {
    return '<text class="' + cls + '" x="' + x + '" y="' + y +
           '" text-anchor="' + anchor + '">' + body + '</text>';
  }

  function drawChart(t) {
    var ticks = useLog ? LOG_TICKS : LIN_TICKS;
    var svg = '';
    var i, y, x;

    // Horizontal gridlines with a value label to the left.
    for (i = 0; i < ticks.length; i++) {
      y = yAt(ticks[i][0], useLog).toFixed(1);
      svg += line('gridline', ML, y, ML + PW, y);
      svg += text('ax', ML - 12, (Number(y) + 4).toFixed(1), 'end', ticks[i][1]);
    }

    // The x-axis, one tick per year.
    svg += line('axisline', ML, MT + PH, ML + PW, MT + PH);
    for (i = 0; i <= T_MAX; i++) {
      x = xAt(i).toFixed(1);
      svg += line('axisline', x, MT + PH, x, MT + PH + 6);
      svg += text('ax', x, MT + PH + 26, 'middle',
                  i === 0 ? 'today' : i + (i === 1 ? ' year' : ' years'));
    }

    // The curve. On the log scale it comes out straight, but we sample it
    // anyway so that both scales share the same code.
    var pts = [];
    for (i = 0; i <= 240; i++) {
      var tt = T_MAX * i / 240;
      pts.push(xAt(tt).toFixed(2) + ' ' + yAt(price(tt), useLog).toFixed(2));
    }
    svg += '<path class="series" d="M ' + pts.join(' L ') + '"/>';

    // The marker for the chosen point in time, with a vertical guide down to the axis.
    x = xAt(t).toFixed(1);
    y = yAt(price(t), useLog).toFixed(1);
    svg += line('guide', x, y, x, MT + PH);
    svg += '<circle class="dot" cx="' + x + '" cy="' + y + '" r="7"/>';

    // On the linear scale the whole point is that the curve looks dead.
    if (!useLog) {
      svg += text('hint', ML + PW, MT + 112, 'end', 'After year 1 the curve looks like it sits at zero.');
      svg += text('hint', ML + PW, MT + 134, 'end', 'Switch the scale — the fall is still going.');
    }

    chart.innerHTML = svg;
  }

  function render() {
    var t = parseFloat(slider.value);
    var v = price(t);

    elPrice.textContent = usd(v);
    elEquiv.textContent = equivalent(v);

    // Rounding can produce 12 months — in which case it is another year.
    var years = Math.floor(t);
    var months = Math.round((t - years) * 12);
    if (months === 12) { years += 1; months = 0; }
    var m = months + (months === 1 ? ' month' : ' months');
    var y = years + (years === 1 ? ' year' : ' years');

    if (t === 0) {
      elWhen.textContent = 'today';
    } else if (years === 0) {
      elWhen.textContent = 'after ' + m;
    } else if (months === 0) {
      elWhen.textContent = 'after ' + y;
    } else {
      elWhen.textContent = 'after ' + y + ' and ' + m;
    }

    btnLog.setAttribute('aria-pressed', String(useLog));
    btnLin.setAttribute('aria-pressed', String(!useLog));

    drawChart(t);
  }

  slider.addEventListener('input', render);
  btnLog.addEventListener('click', function () { useLog = true; render(); });
  btnLin.addEventListener('click', function () { useLog = false; render(); });

  // It should also be possible to drag directly in the chart.
  function scrub(ev) {
    if (ev.type === 'pointermove' && ev.buttons === 0) { return; }
    var box = chart.getBoundingClientRect();
    var frac = ((ev.clientX - box.left) / box.width * W - ML) / PW;
    var t = frac * T_MAX;
    if (t < 0) { t = 0; }
    if (t > T_MAX) { t = T_MAX; }
    slider.value = t.toFixed(2);
    render();
  }

  chart.addEventListener('pointerdown', function (ev) {
    chart.setPointerCapture(ev.pointerId);
    scrub(ev);
  });
  chart.addEventListener('pointermove', scrub);

  render();
}());
