/*
  Räknar PDF-nedladdningar som anonyma händelser i GoatCounter.

  Varje nedladdning skickas som en händelse med
    path:  "pdf/<sökvägen under /assets/pdfs/ utan .pdf>"  t.ex. "pdf/free/visual-codes-50-en"
    title: filnamnet                                       t.ex. "visual-codes-50-en.pdf"
  Dashboarden i AI OS läser exakt det formatet, så ändra det inte här utan att ändra där.

  Filen laddas av include.js på varje sida, och direkt av /dl/.
  Andra skript (e-postgrinden, /dl/) räknar via window.cwCountPdf(href).
  Ingenting här får kasta fel: blir räkningen fel ska PDF:en ändå öppnas.
*/
(function () {
  // Laddas filen två gånger (include.js + /dl/) räcker det med den första.
  if (window.cwCountPdf) return;

  const PDF_DIR = '/assets/pdfs/';
  const LIVE_HOST = 'choosewise.education';

  // Anrop som väntar på att GoatCounters skript ska bli klart (eller blockeras).
  const queue = [];
  let timer = null;
  let waited = 0;

  // Gör om en länk till GoatCounter-händelsen ovan. Ger null för allt som
  // inte är en PDF under /assets/pdfs/ på den här sajten — sådant räknas inte.
  function eventFor(href) {
    let url;
    try { url = new URL(href, location.href); } catch (e) { return null; }
    // Samma sajt: antingen samma ursprung som sidan, eller den publicerade
    // adressen (en absolut länk till choosewise.education vid lokal förhandsvisning).
    if (url.origin !== location.origin && url.hostname !== LIVE_HOST) return null;
    const path = url.pathname;
    if (!path.startsWith(PDF_DIR) || !path.endsWith('.pdf')) return null;
    const name = path.slice(PDF_DIR.length, -'.pdf'.length);
    if (!name) return null;
    return { path: 'pdf/' + name, title: path.split('/').pop(), event: true };
  }

  // Är GoatCounters skript laddat och redo att ta emot anrop?
  function ready() {
    return !!(window.goatcounter && typeof window.goatcounter.count === 'function');
  }

  // Skickar allt som står i kön, om GoatCounter är redo. Sant när kön är tom.
  function flush() {
    while (queue.length && ready()) {
      const item = queue.shift();
      try { window.goatcounter.count(item); } catch (e) { /* räkningen får aldrig stoppa nedladdningen */ }
    }
    return queue.length === 0;
  }

  // Tittar efter GoatCounter var 100:e millisekund tills kön är tom.
  // Efter 10 sekunder ger vi upp: då är skriptet troligen blockerat.
  function keepTrying() {
    if (timer) return;
    waited = 0;
    timer = setInterval(function () {
      waited += 100;
      if (flush() || waited >= 10000) {
        clearInterval(timer);
        timer = null;
      }
    }, 100);
  }

  // Det enda andra skript behöver: räkna en nedladdning av den här länken.
  function countPdf(href) {
    const item = eventFor(href);
    if (!item) return;
    queue.push(item);
    if (!flush()) keepTrying();
  }

  // För /dl/: vänta tills kön är tömd, men högst maxMs millisekunder.
  countPdf.settled = function (maxMs) {
    return new Promise(function (resolve) {
      const start = Date.now();
      (function check() {
        if (flush() || Date.now() - start >= maxMs) resolve();
        else setTimeout(check, 50);
      })();
    });
  };

  window.cwCountPdf = countPdf;

  // Ett enda lyssnare för hela sidan fångar klick på alla PDF-länkar,
  // även länkar som läggs till senare (t.ex. i e-postgrindens ruta).
  // Grindknappar (data-gate) hoppas över: att klicka på dem öppnar oftast bara
  // rutan för e-post, så mailerlite-gate.js räknar själv när PDF:en faktiskt öppnas.
  document.addEventListener('click', function (e) {
    const link = e.target.closest && e.target.closest('a[href]');
    if (!link || link.closest('[data-gate]')) return;
    countPdf(link.href);
  });
})();
