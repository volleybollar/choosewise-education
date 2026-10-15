Debatten om AI i skolan handlar nästan alltid om tillgång. Ska mobilerna låsas in, ska skärmtiden ned, ska läromedlen tillbaka till papper? Det är rimliga frågor på klassrumsnivå, och jag avfärdar dem inte. Men de vilar alla på samma antagande: att tillgången till AI är något skolan kan reglera.

Det finns en siffra som gör det antagandet svårt att försvara.

## En faktor 13 om året

Epoch AI publicerade i september 2026 en genomgång av vad det kostar att nå en *given* prestationsnivå med AI ([The Plunging Price of Thought](https://epoch.ai/publications/the-plunging-price-of-thought)). Slutsatsen: kostnaden har fallit med ca 47 procent per kvartal sedan 2023 — d v s med en faktor på ca 13 per år.

Lägg märke till vad som mäts. Inte priset per token, och inte priset på "AI" i allmänhet. Det som mäts är vad det kostar att komma upp i en bestämd kvalitetsnivå, över fem olika uppgiftstyper (bl a avancerade matematikproblem, naturvetenskapliga frågor på doktorandnivå och schackpussel). Samma uppgift, samma resultat — till en bråkdel av kostnaden.

Ett exempel ur rapporten: på testet GPQA Diamond, som består av naturvetenskapliga frågor på expertnivå, föll kostnaden för 75 procents träffsäkerhet från ca 30 cent till fyra tiotusendelar av en dollar per fråga. På arton månader. Drygt 700 gånger billigare, för samma svar.

Författarna jämför takten med andra teknikskiften: fyra gånger snabbare än DNA-sekvensering, sex gånger snabbare än datorkraft, och drygt 50 gånger snabbare än elektricitet gjorde under perioden 1892–1973.

## Räkneexempel: ditt hus

Problemet med den sortens siffror är att de inte säger oss någonting. Vi hör "en faktor 13 per år" och nickar. Så låt oss byta ut AI mot något vi faktiskt har en känsla för.

Tänk ett hus som kostar 5 miljoner kronor. Tänk att priset — samma hus, samma läge, samma skick — faller i exakt den takt Epoch har mätt.

<figure class="module-figure">
  <img src="/sv/blog/posts/assets/huset-trappan.webp" alt="Trappdiagram: huspriset faller från 5 000 000 kr i dag till 5 kr efter 5,39 år, ett steg per år." loading="lazy" decoding="async">
  <figcaption>Varje steg neråt är ett år — och en trettondel av priset.</figcaption>
</figure>

<figure class="data-table">
  <table>
    <caption>Huspriset år för år, vid ett fall med en faktor 13 per år</caption>
    <thead>
      <tr>
        <th scope="col">Tid</th>
        <th scope="col">Pris</th>
        <th scope="col">Motsvarar ungefär</th>
      </tr>
    </thead>
    <tbody>
      <tr><th scope="row">I dag</th><td>5 000 000 kr</td><td>ett hus</td></tr>
      <tr><th scope="row">Efter 1 år</th><td>384 600 kr</td><td>en ny bil</td></tr>
      <tr><th scope="row">Efter 2 år</th><td>29 600 kr</td><td>en elcykel</td></tr>
      <tr><th scope="row">Efter 3 år</th><td>2 276 kr</td><td>ett par dyra skor</td></tr>
      <tr><th scope="row">Efter 4 år</th><td>175 kr</td><td>en pizza</td></tr>
      <tr><th scope="row">Efter 5 år</th><td>13,47 kr</td><td>en liter mjölk</td></tr>
      <tr><th scope="row">Efter 5,39 år</th><td>5 kr</td><td>en femkrona</td></tr>
    </tbody>
  </table>
</figure>

Efter fem år och fem månader kostar huset fem kronor. En miljondel av utgångspriset.

> Priset halveras var tredje månad.

(Varje kvartal du väntar får du alltså dubbelt så mycket hus för pengarna — vilket förstås också betyder att den som köpte i går betalade dubbelt för mycket.)

## Varför ser vi det inte komma?

Vi är byggda för att tänka linjärt. Har något blivit lite billigare i år antar vi att det blir lite billigare nästa år också. Exponentiell utveckling fungerar inte så, och det syns tydligast om man ritar upp den.

<figure class="module-figure">
  <img src="/sv/blog/posts/assets/huset-linjar-skala.webp" alt="Linjediagram på linjär skala: kurvan störtdyker under år 1 och ligger sedan platt längs botten." loading="lazy" decoding="async">
  <figcaption>På en vanlig skala ser fallet ut som ett stup följt av ingenting.</figcaption>
</figure>

Efter år 1 ligger linjen praktiskt taget på noll, och resten av diagrammet är en rak linje längs botten. Det är där vår intuition stannar: nu är det billigt, klart.

<figure class="module-figure">
  <img src="/sv/blog/posts/assets/huset-logaritmisk-skala.webp" alt="Samma data på logaritmisk skala: en rak, nedåtlutande linje från 5 000 000 kr till 5 kr." loading="lazy" decoding="async">
  <figcaption>Samma siffror, logaritmisk skala. Fallet pågår hela vägen ned.</figcaption>
</figure>

Samma siffror på en logaritmisk skala blir en rak, nedåtlutande linje som fortsätter i oförändrad takt långt efter att det första diagrammet gav upp. Skillnaden mellan 175 kronor och 5 kronor syns inte alls i det första diagrammet. I praktiken är det skillnaden mellan "dyrt för de flesta" och "gratis för alla".

Där ligger poängen. När något har fallit så mycket att vi uppfattar det som gratis fortsätter det ändå att falla — och det är i det skedet tillgången slutar vara en fråga om pengar.

<section class="prisfall" id="prisfall">
  <link rel="stylesheet" href="/sv/blog/posts/assets/huset-prisfall.css">
  <h2 class="prisfall__title">Dra i siffrorna själv</h2>
  <p class="prisfall__intro">Flytta reglaget, eller dra direkt i diagrammet, och växla mellan de två skalorna.</p>
  <div class="prisfall__readout">
    <span class="prisfall__price">2 276 kr</span>
    <span class="prisfall__equiv">ungefär ett par dyra skor</span>
    <span class="prisfall__when">efter 3 år</span>
  </div>
  <div class="prisfall__controls">
    <div class="prisfall__slider">
      <label class="prisfall__cap" for="prisfall-year">Tid från i dag</label>
      <input type="range" id="prisfall-year" min="0" max="6" step="0.01" value="3">
    </div>
    <fieldset>
      <legend class="prisfall__cap">Skala på y-axeln</legend>
      <div class="prisfall__segmented" role="group" aria-label="Välj skala">
        <button type="button" id="prisfall-lin" aria-pressed="false">Linjär</button>
        <button type="button" id="prisfall-log" aria-pressed="true">Logaritmisk</button>
      </div>
    </fieldset>
  </div>
  <svg class="prisfall__chart" viewBox="0 0 760 420" role="img" aria-label="Diagram över huspriset som faller med en faktor 13 per år"></svg>
</section>
<script defer src="/sv/blog/posts/assets/huset-prisfall.js"></script>

## Vad betyder det för utbildningssystemet?

Om riktningen håller, även bara halvvägs, är det detta vi har att förhålla oss till: intelligens — den artificiella sorten — kommer i praktiken att vara fritt tillgänglig för varje elev, oberoende av om skolan har bestämt sig eller inte. Inte som en post i en it-budget, utan som något som ligger i telefonen, i webbläsaren och i ordbehandlaren utan att någon aktivt har valt det.

Då faller förbudslinjen på sin egen logik. Ett förbud är ett styrmedel som förutsätter kontroll över tillgången. Som ordningsregel i ett klassrum kan det fungera, och ibland är det rätt beslut just där. Men som strategi för ett utbildningssystem vilar det på en förutsättning som kurvan håller på att ta bort.

Frågan är alltså inte hur vi håller AI utanför. Den är: vad ska en elev kunna i en värld där svaret alltid är gratis och omedelbart? Vilka förmågor blir mer värda, inte mindre, när textproduktion kostar noll?

## Förbehållen

Jag ska inte överdriva säkerheten i siffran. Epochs egna invändningar är rimliga:

- Dataserien är bara tre år lång.
- Modellerna kan vara optimerade för just de test som mäts, vilket troligen överskattar den allmänna förmågan.
- Vanliga användare byter inte modell så fort en billigare dyker upp, så den besparing en enskild användare gör är mindre än den som mäts vid fronten.
- Författarna är själva tydliga med att siffrorna är representativa, inte exakta.

Takten kan alltså visa sig bli en faktor 5 per år i stället för 13. Det är ingen tröst. Då tar huset åtta år i stället för fem.

## Slutsats

Vi diskuterar skärmar därför att skärmar är synliga och går att reglera. Priset på att tänka är osynligt och går inte att reglera. Av de två är det andra det som kommer att avgöra hur svensk skola ser ut i framtiden.

Så här skulle jag vilja vända på frågan nästa gång den kommer upp i en ledningsgrupp: om vi utgår från att varje elev om tre år har tillgång till den förmåga som i dag kostar en förmögenhet — vad behöver vi då börja göra i dag?

---

*Källa: Luke Emberson & David Roodman, ["The Plunging Price of Thought"](https://epoch.ai/publications/the-plunging-price-of-thought), Epoch AI, 22 september 2026. Huset är ett räkneexempel som illustrerar takten i Epochs mätning — inte en prognos om bostadsmarknaden.*
