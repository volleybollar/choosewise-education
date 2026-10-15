/*
  Interaktiv graf till inlägget "Huset som kostade fem kronor".

  Modellen: ett hus för 5 000 000 kr vars pris faller med faktor 13 per år —
  samma takt som Epoch AI har mätt för kostnaden att nå en given
  prestationsnivå med AI.

  Skriptet ritar om hela SVG:n vid varje ändring. Det är billigt nog här
  (ett par hundra punkter) och gör koden lätt att följa: en funktion som
  räknar, en som ritar, en som uppdaterar texten.
*/
(function () {
  'use strict';

  var root = document.querySelector('.prisfall');
  if (!root) { return; }

  var START = 5000000;   // utgångspris i kronor
  var RATE = 13;         // gånger billigare per år
  var T_MAX = 6;         // reglagets längd i år

  function price(t) { return START / Math.pow(RATE, t); }

  // Vardagsjämförelser, dyrast först. Första träffen vinner.
  var EQUIVALENTS = [
    [2000000, 'ungefär ett hus'],
    [300000, 'ungefär en ny bil'],
    [80000, 'ungefär en begagnad bil'],
    [20000, 'ungefär en elcykel'],
    [6000, 'ungefär en soffa'],
    [1500, 'ungefär ett par dyra skor'],
    [600, 'ungefär en middag för två'],
    [120, 'ungefär en pizza'],
    [30, 'ungefär en kopp kaffe'],
    [8, 'ungefär en liter mjölk'],
    [2, 'ungefär en femkrona'],
    [0, 'mindre än en krona']
  ];

  function equivalent(v) {
    for (var i = 0; i < EQUIVALENTS.length; i++) {
      if (v >= EQUIVALENTS[i][0]) { return EQUIVALENTS[i][1]; }
    }
    return '';
  }

  // Svensk talformatering: tusenmellanslag, två decimaler under tio kronor.
  var nf0 = new Intl.NumberFormat('sv-SE', { maximumFractionDigits: 0 });
  var nf2 = new Intl.NumberFormat('sv-SE', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  function kr(v) {
    return (v >= 10 ? nf0.format(Math.round(v)) : nf2.format(v)) + ' kr';
  }

  // ── Diagramgeometri ──
  // Marginalerna lämnar plats åt etiketterna så att inget hamnar utanför viewBox.
  var W = 760, H = 420, ML = 86, MR = 22, MT = 18, MB = 44;
  var PW = W - ML - MR, PH = H - MT - MB;

  function xAt(t) { return ML + PW * (t / T_MAX); }

  // Log-skalan går från 1 kr (10^0) till 10 Mkr (10^7).
  function yAt(v, log) {
    if (log) {
      return MT + PH * (1 - Math.log(Math.max(v, 1)) / Math.LN10 / 7);
    }
    return MT + PH * (1 - v / START);
  }

  var LIN_TICKS = [[5e6, '5 Mkr'], [4e6, '4 Mkr'], [3e6, '3 Mkr'],
                   [2e6, '2 Mkr'], [1e6, '1 Mkr'], [0, '0']];
  var LOG_TICKS = [[1e7, '10 Mkr'], [1e6, '1 Mkr'], [1e5, '100 000 kr'],
                   [1e4, '10 000 kr'], [1e3, '1 000 kr'], [100, '100 kr'],
                   [10, '10 kr'], [1, '1 kr']];

  var chart = root.querySelector('.prisfall__chart');
  var slider = root.querySelector('#prisfall-year');
  var btnLog = root.querySelector('#prisfall-log');
  var btnLin = root.querySelector('#prisfall-lin');
  var elPrice = root.querySelector('.prisfall__price');
  var elEquiv = root.querySelector('.prisfall__equiv');
  var elWhen = root.querySelector('.prisfall__when');

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

    // Vågräta stödlinjer med värdeetikett till vänster.
    for (i = 0; i < ticks.length; i++) {
      y = yAt(ticks[i][0], useLog).toFixed(1);
      svg += line('gridline', ML, y, ML + PW, y);
      svg += text('ax', ML - 12, (Number(y) + 4).toFixed(1), 'end', ticks[i][1]);
    }

    // X-axel med ett streck per år.
    svg += line('axisline', ML, MT + PH, ML + PW, MT + PH);
    for (i = 0; i <= T_MAX; i++) {
      x = xAt(i).toFixed(1);
      svg += line('axisline', x, MT + PH, x, MT + PH + 6);
      svg += text('ax', x, MT + PH + 26, 'middle', i === 0 ? 'i dag' : i + ' år');
    }

    // Kurvan. På log-skalan blir den rak, men vi samplar ändå så att
    // båda skalorna delar samma kod.
    var pts = [];
    for (i = 0; i <= 240; i++) {
      var tt = T_MAX * i / 240;
      pts.push(xAt(tt).toFixed(2) + ' ' + yAt(price(tt), useLog).toFixed(2));
    }
    svg += '<path class="series" d="M ' + pts.join(' L ') + '"/>';

    // Markören för vald tidpunkt, med lodrät ledarlinje ned till axeln.
    x = xAt(t).toFixed(1);
    y = yAt(price(t), useLog).toFixed(1);
    svg += line('guide', x, y, x, MT + PH);
    svg += '<circle class="dot" cx="' + x + '" cy="' + y + '" r="7"/>';

    // På den linjära skalan är hela poängen att kurvan ser död ut.
    if (!useLog) {
      svg += text('hint', ML + PW, MT + 112, 'end', 'Efter år 1 ser kurvan ut att ligga på noll.');
      svg += text('hint', ML + PW, MT + 134, 'end', 'Byt skala — fallet pågår fortfarande.');
    }

    chart.innerHTML = svg;
  }

  function render() {
    var t = parseFloat(slider.value);
    var v = price(t);

    elPrice.textContent = kr(v);
    elEquiv.textContent = equivalent(v);

    // Avrundningen kan ge 12 månader — då är det ett år till.
    var years = Math.floor(t);
    var months = Math.round((t - years) * 12);
    if (months === 12) { years += 1; months = 0; }
    var m = months + (months === 1 ? ' månad' : ' månader');

    if (t === 0) {
      elWhen.textContent = 'i dag';
    } else if (years === 0) {
      elWhen.textContent = 'efter ' + m;
    } else if (months === 0) {
      elWhen.textContent = 'efter ' + years + ' år';
    } else {
      elWhen.textContent = 'efter ' + years + ' år och ' + m;
    }

    btnLog.setAttribute('aria-pressed', String(useLog));
    btnLin.setAttribute('aria-pressed', String(!useLog));

    drawChart(t);
  }

  slider.addEventListener('input', render);
  btnLog.addEventListener('click', function () { useLog = true; render(); });
  btnLin.addEventListener('click', function () { useLog = false; render(); });

  // Man ska också kunna dra direkt i diagrammet.
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
