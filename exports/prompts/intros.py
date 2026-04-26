"""Unique per-pack P3 intro sentences (Option B from the plan).

Used by generate-pages.py to render a 4-paragraph hero on each prompt-pack
landing page:

  P1 — dynamic lede (template, language-shared)
  P2 — bio (shared, identical on every pack)
  P3 — UNIQUE PER PACK ← this file
  P4 — "for whom" (shared, identical on every pack)

The unique sentence is 1–2 sentences, ~30–50 words. It references what
makes THIS pack relevant for THIS audience without keyword-stuffing or
promotional language. Tone: empathetic + practical, not vendor copy.

Keys are slug_sv (SV) and slug_en (EN). Megaprompt packs intentionally have
no entry — they use a separate template. SV-only packs have only an SV entry.
"""

INTROS_SV = {
    # — Generalist roles + theme —
    "larare": "Som lärare är pedagogiken alltid det viktigaste, inte verktyget. De här promptarna täcker det breda läraruppdraget — från planering och feedback till kollegial reflektion — alla skrivna med utgångspunkt i hur lärararbetet faktiskt ser ut, inte hur det ser ut i teorin.",
    "lar-dig-nya-saker": "Det här paketet är inte avgränsat till skolan utan riktar sig till alla som vill bli bättre på att lära sig något nytt. Promptarna utgår från evidensbaserade studietekniker — Feynman, spaced repetition, chunking, dual coding — och hjälper dig sätta dem i praktik.",
    "rektorer": "Som rektor jonglerar du beslut som spänner över pedagogik, ekonomi och personal samtidigt. Promptarna i det här paketet är skrivna för just den verkligheten — ofta i situationer där du behöver formulera dig snabbt utan att kompromissa med precisionen.",
    "skolchefer": "Skolchefsuppdraget handlar mycket om att översätta strategi till skolverklighet och tillbaka igen. Promptarna här fokuserar på de samtal du faktiskt sitter i — med politiker, rektorer och förvaltning — där tonen och formuleringen ofta är lika viktig som innehållet.",
    "forskola": "Förskolepedagogiken är lekfull, närvarande och vilar på relationer. Promptarna här hjälper dig planera tematiskt arbete, dokumentera lärande och formulera dig i samtal med vårdnadshavare — utan att tappa det som är förskolans signum.",
    "forskoleklass": "I förskoleklassen ska du möta varje barn där det är, samtidigt som du börjar lägga grunden för läs- och skrivinlärning. Promptarna här riktar sig särskilt till den övergången — mellan lek och struktur — och de balansgångar som hör till.",

    # — Subject teachers, compulsory school —
    "bild": "Bildämnet handlar om att tänka visuellt — och om att hjälpa eleverna våga göra det. Promptarna här kombinerar konkret undervisningsplanering med stöd för hur du kan tala om elevens uttryck utan att stänga in det i rätt eller fel.",
    "biologi": "Biologin är experimentell, etisk och systemtänkande på samma gång. Promptarna här hjälper dig med allt från fältstudier och labbinstruktioner till samtal om hållbarhet och evolution — på ett sätt som rör vid både fakta och värderingar.",
    "engelska": "Engelskan har dragit nytta av AI tidigare än de flesta ämnen — eleverna pratar redan med chattbotar på engelska. Promptarna här hjälper dig lyfta nivån från enkel översättning till verklig språkutveckling: nyans, register och strategier för att förstå.",
    "fysik": "Fysiken kräver att eleverna både kan räkna och tänka modellerande. Promptarna här fokuserar på det andra — hur du formulerar tankefrågor, designar kvalitativa uppgifter och pratar om hur naturen faktiskt fungerar, inte bara vad formeln säger.",
    "geografi": "Geografi är ett ämne som rör sig snabbt — kartan ritas om hela tiden av klimat, migration och politik. Promptarna här hjälper dig hålla undervisningen aktuell och knyta samman det fysiska, det sociala och det globala.",
    "hkk": "HKK kombinerar matlagning, ekonomi, miljö och hälsa i ett konkret klassrum. Promptarna här hjälper dig med sådant som veckomenyer för olika dieter, budgetövningar med riktiga siffror och samtal om hållbarhet utan att det blir moralism.",
    "historia": "Historieundervisningen handlar om att se sammanhang över tid och om att skilja det belagda från det berättade. Promptarna här stöttar både källkritiken och det narrativa — för att eleverna ska kunna analysera utan att tappa engagemanget.",
    "idh": "Idrott och hälsa rymmer både motorik, hälsa och samtal om kropp och välmående. Promptarna här hjälper dig planera lektioner med differentiering, formulera samtal kring känsliga ämnen och skapa bedömningsstöd för det som är svårt att betygsätta.",
    "kemi": "Kemi blir levande när eleven förstår varför reaktionen sker, inte bara att den gör det. Promptarna här hjälper dig hitta vardagsanknytningar, planera säkra labbar och förklara abstrakta begrepp på sätt som fastnar.",
    "matematik": "Matematiken kräver både precision och fantasi — eleverna ska kunna räkna, men också resonera. Promptarna här balanserar de två: rena färdighetsövningar, problemlösning och samtal om matematiskt tänkande som mer än beräkning.",
    "lara-sig-rakna": "Tidig matematikinlärning är där grunden läggs för hela skolgångens matematik. Promptarna här stöttar konkret det visuella, taktila och språkliga — det som händer innan formlerna kommer in — och som påverkar elevens självbild som mattetänkande person.",
    "moderna-sprak": "Moderna språk är ofta sårbara i timplanen och kräver kreativa lösningar. Promptarna här hjälper dig hålla språket levande — kulturellt sammanhang, autentiska texter, varierad muntlig övning — också när tiden och resurserna är begränsade.",
    "musik": "Musikämnet är där elever möter både kunskapsteori och eget skapande. Promptarna här hjälper dig planera moment som rymmer båda — från gehörsövningar och musikteori till bandklassrum och stora projekt — utan att kreativiteten kvävs av strukturen.",
    "naturkunskap": "Naturkunskap är gymnasiets bredbandämne — biologi, kemi, fysik och samhälle i samma kursplan. Promptarna här hjälper dig hitta de stora frågorna som skär tvärs över: klimat, hälsa, energi, etik — där eleverna ska kunna ta ställning grundat i vetenskap.",
    "no": "NO-lärare hanterar tre ämnen — biologi, fysik och kemi — ibland samtidigt. Promptarna här stöttar dig i den ämnesövergripande verkligheten: planering där labb, säkerhet och progression hänger ihop över ämnesgränser.",
    "religion": "Religion är ett ämne där eleverna ska analysera utan att fördöma och förstå utan att överta. Promptarna här hjälper dig formulera lektioner som öppnar samtal om tro, etik och världsbild — också i klasser där åsikterna är starka och skilda.",
    "samhallskunskap": "Samhällskunskapen ska göra eleverna till medborgare som tänker själva. Promptarna här hjälper dig hantera dagspolitiken i klassrummet utan att ta sida, träna källkritik och formulera uppgifter där eleverna ska argumentera grundat i fakta.",
    "slojd": "Slöjden är ett av de ämnen där hand och hjärna verkligen jobbar tillsammans. Promptarna här fokuserar på det som händer runt slöjden — planering, dokumentation, bedömning av processen och samtal om hantverkskvalitet — så att verkstadstiden får vara verkstadstid.",
    "so": "SO-lärare jonglerar fyra ämnen: historia, geografi, samhällskunskap och religion — ibland med samma elever. Promptarna här hjälper dig med planering och progression över ämnesgränserna, så att helheten i SO-uppdraget håller ihop.",
    "teknik": "Teknikämnet ändrar form snabbt — vad som var nytt för fem år sedan är ofta vardag idag. Promptarna här hjälper dig hålla undervisningen relevant utan att jaga trender, och formulera tekniska resonemang så att eleverna kan tänka som ingenjörer.",

    # — Subject teachers, upper secondary —
    "engelska-gymnasiet": "På gymnasiet ska eleverna kunna mer än kommunicera — de ska analysera språk, kultur och text. Promptarna här stöttar det avancerade arbetet: litteraturanalys, akademiskt skrivande och samtal om engelskan som global lingua franca.",
    "historia-gymnasiet": "Gymnasiehistorien fördjupar sig i metod och historiebruk — eleverna ska kunna värdera källor och se hur historien används idag. Promptarna här stöttar både den akademiska analysen och de stora samtalen om varför historien betyder något.",
    "idh-gymnasiet": "På gymnasiet möter du elever med vitt skilda relationer till idrott — från elitsatsande till motvilliga. Promptarna här hjälper dig differentiera utan att förlora ämnets själ, och föra samtal om hälsa som rör vid både kropp och självbild.",
    "matematik-gymnasiet": "Gymnasiematematiken kräver både stringens och förståelse på djupet. Promptarna här stöttar det abstrakta — bevis, modellering, problemlösning på högre nivå — och hjälper dig formulera uppgifter där eleven måste resonera, inte bara räkna.",
    "moderna-sprak-gymnasiet": "På gymnasiet möter eleverna språket på avancerad nivå — autentiska texter, kulturella nyanser, akademiskt skrivande. Promptarna här hjälper dig planera ett innehåll som motsvarar det språk de faktiskt kommer behöva utanför klassrummet.",
    "religion-gymnasiet": "Gymnasieelevens religionsanalys kräver verktyg från flera akademiska traditioner. Promptarna här hjälper dig planera ämnet på den nivå där eleverna ska kunna jämföra världsåskådningar systematiskt och formulera egna resonemang utan att tappa nyans.",
    "samhallskunskap-gymnasiet": "Gymnasiesamhällskunskapen lyfter politik, ekonomi och statsvetenskap till en analytisk nivå. Promptarna här hjälper dig konstruera uppgifter där eleverna måste tillämpa teori på verkligheten — inte bara reproducera definitioner från läroboken.",

    # — Swedish-only subject packs —
    "modersmal": "Modersmålsläraruppdraget är unikt — du undervisar i ett ämne där eleverna ofta är dina enda klasskamrater. Promptarna här hjälper dig planera språk- och kulturarbete på flera nivåer samtidigt, och formulera samtal med skolan om elevens hela språkliga vardag.",
    "svenska": "Svenskan är ämnet där eleverna lär sig att läsa, skriva och tänka i text. Promptarna här hjälper dig med allt från grammatikgenomgångar och läsförståelseövningar till litteratursamtal och skrivprojekt — för olika åldrar och förkunskapsnivåer.",
    "las-och-skrivinlarning": "Läs- och skrivinlärningen är där elevens hela skolresa börjar — det som händer här påverkar resten. Promptarna här stöttar det medvetna arbetet med fonologi, ordigenkänning, läsförståelse och skrivutveckling, gärna i samspel med specialpedagog.",
    "svenska-gymnasiet": "Gymnasiesvenskan kräver att eleverna kan läsa, analysera och skriva på akademisk nivå. Promptarna här stöttar det avancerade arbetet — litteraturhistoria, retorik, vetenskapligt skrivande — och formulerar samtal om språket som något mer än bara verktyg.",
    "sva": "SVA-läraren möter elever som lär sig svenska samtidigt som de ska klara hela skolans kunskapskrav. Promptarna här fokuserar på det dubbla uppdraget — språkutveckling som går hand i hand med ämneskunskap — och stödet i det vardagliga klassrumsarbetet.",
    "sva-gymnasiet": "På gymnasiet ska SVA-eleven nå akademisk svenska samtidigt som hen ofta nyligen kommit till landet. Promptarna här hjälper dig planera språkutvecklingen så att den bär eleven mot studier och arbete — utan att kompromissa med ämnesinnehållet.",

    # — Other teaching roles —
    "ikt-pedagoger": "IKT-pedagoger sitter ofta i skärningen mellan teknik, pedagogik och förändringsarbete. Promptarna i det här paketet stöttar både konkret klassrumsanvändning och de strategiska samtalen med kollegium och ledning.",
    "forstelarare": "Förstelärarrollen kräver både ämnesexpertis och förmågan att leda kollegor som inte är dina underställda. Promptarna här hjälper dig formulera kollegial återkoppling, leda ämnesutveckling och översätta forskning till sådant som faktiskt händer i klassrummen.",

    # — Support staff —
    "fritids": "Fritids ska komplettera det skolan gör utan att bli en kopia av det. Promptarna här hjälper dig planera meningsfull verksamhet, dokumentera lärande genom lek och samtala med vårdnadshavare om barnets hela dag — också den del som inte sätter betyg.",
    "speciallarare": "Specialläraren arbetar oftast individuellt eller i mindre grupp, där varje elev har en unik utgångspunkt. Promptarna här hjälper dig anpassa material, formulera mål som är konkreta nog att utvärdera, och dokumentera framsteg som annars kan vara svåra att se.",
    "elevassistenter": "Elevassistenten arbetar nära enskild elev men inom klassens helhet — en balans som kräver mycket pedagogiskt omdöme. Promptarna här hjälper dig formulera anpassningar, kommunicera med läraren om eleven, och hitta sätt att stötta utan att överta.",
    "syv": "SYV-uppdraget handlar om att möta unga som ska forma sin framtid på en arbetsmarknad som ändras snabbare än läroplanen. Promptarna här stöttar dig i samtalen, planeringen och dokumentationen — så att vägledningen håller även för en 14-åring som inte vet vad hen vill.",
    "specialpedagoger": "Specialpedagogen arbetar både med enskilda elever, lärare och hela skolans pedagogiska struktur. Promptarna här stöttar det strategiska — pedagogiska kartläggningar, åtgärdsprogram, handledning av kollegor — där formuleringen ofta är avgörande för vad som faktiskt händer.",
    "skolskoterskor": "Skolsköterskan möter elever i frågor som spänner över hälsa, identitet, utsatthet och pedagogik. Promptarna här hjälper dig med dokumentation, samtalsstrukturer och kommunikation med vårdnadshavare och skola — på sätt som klarar både GDPR och elevens förtroende.",
    "kuratorer": "Skolkuratorn arbetar i en värld där elevärendena ofta är akuta och resurserna ändliga. Promptarna här fokuserar på det som omger samtalen — dokumentation, samverkan, strukturerade kartläggningar — så att tiden i samtalsrummet kan handla om eleven.",
    "skolpsykologer": "Skolpsykologen ska göra avancerade utredningar och bidra till elevhälsans helhet — ofta på begränsad tid. Promptarna här stöttar dig i det skriftliga arbetet, från utredningstexter till handledningsförberedelser, så att du kan lägga mer tid på det kliniska.",
    "skolvaktmastare": "Skolvaktmästaren ser allt — från trasiga lås och kaffemaskiner till elever som har en dålig dag. Promptarna här hjälper dig formulera underhållsplaner, säkerhetsrutiner och kommunikation med leverantörer — för det administrativa som tar tid från det praktiska.",
    "skolmaltidspersonal": "Köket levererar ofta hundratals måltider om dagen, ska följa specialkoster och samtidigt vara pedagogiskt. Promptarna här hjälper dig med veckomenyer, kommunikation med vårdnadshavare om allergier och samtal i matsalen som gör måltiden mer än bara mat.",
    "it-ansvariga-skola": "IT-ansvariga på skolnivå möter både GDPR, lärares stress och elevers innovativa sätt att kringgå spärrar. Promptarna här hjälper dig formulera tydliga rutiner, kommunicera tekniskt utan jargong och fatta bra beslut när tiden är knapp.",
    "it-ansvariga-central": "På central IT-nivå handlar besluten om hela huvudmannens elevpopulation och fleråriga avtal. Promptarna här stöttar det strategiska arbetet — upphandlingsunderlag, säkerhetsanalyser, kommunikation med ledning — där en formulering kan styra miljonbelopp.",
    "skolbibliotekarier": "Skolbiblioteket är en av skolans viktigaste pedagogiska resurser — och en av de mest underutnyttjade. Promptarna här hjälper dig planera samarbeten med lärare, formulera bokpresentationer och leda informationssökningssamtal som bygger källkritik.",
    "strateger": "Skolstrategens uppdrag är att översätta verksamhet till strategi och tillbaka igen — ofta med ett helt huvudmannaperspektiv. Promptarna här stöttar de skriftliga delarna: analyser, beslutsunderlag, kommunikation med ledning och politik — där tonen avgör om budskapet går fram.",
    "administratorer": "Skoladministratören är den som håller skolans administrativa motor i gång — schemaläggning, frånvaro, kommunikation med vårdnadshavare. Promptarna här hjälper dig formulera tydliga meddelanden och dokumentera rutiner så att verksamheten flyter när läraren är frånvarande.",
    "admin-central": "Den centrala administrationen håller ihop ekonomi, statistik och rapportering för en hel huvudman. Promptarna här stöttar det strikt formaliserade arbetet — protokoll, rapporter, budgettexter — där en exakt formulering kan rädda eller bränna timmar i efterspelet.",

    # — Thematic —
    "digitala-verktyg": "Digitalisering i skolan är inte ett mål i sig — det är ett medel som ibland passar och ibland inte. Promptarna här hjälper dig välja, utvärdera och använda digitala verktyg där de faktiskt tillför något, och avstå där de bara skapar friktion.",
    "amnesovergripande": "Ämnesövergripande arbete ger eleverna chansen att se hur kunskap hänger ihop — men kräver också mer planering än ett vanligt ämnesmoment. Promptarna här stöttar det organisatoriska arbetet, så att samarbetet mellan lärare blir produktivt istället för komplicerat.",
    "utomhuspedagogik": "Utomhuspedagogiken sätter undervisningen i en miljö där kropp och sinnen är med på riktigt. Promptarna här hjälper dig planera lektioner som tar tillvara platsens möjligheter, formulera mål som hänger ihop med läroplanen, och hantera det praktiska runtomkring.",
    "studier-om-larande": "Forskning om lärande gör skillnad i klassrummet bara om den översätts till konkret undervisning. Promptarna här hjälper dig ta evidensbaserade slutsatser — om återkoppling, kognitiv belastning, retrieval practice — och förvandla dem till lektionsstrukturer och uppgifter som faktiskt fungerar.",
    "tidsutnyttjande": "Tidsbristen är något jag mött både som lärare och som skolledare. Promptarna här handlar om att vinna tillbaka timmar på rättning, planering och möten — utan att tappa kvalitet.",
}


INTROS_EN = {
    # — Generalist roles + theme —
    "teachers": "As a teacher, pedagogy comes first — never the tool. This pack covers the breadth of the classroom teacher's role — planning, feedback, collegial reflection — written from the inside, around how the work actually feels, not how it looks in a glossy training brochure.",
    "learning-new-skills": "This pack isn't tied to school — it's for anyone who wants to get better at learning something new. The prompts draw on evidence-based study techniques like the Feynman method, spaced repetition, chunking, and dual coding, with concrete steps for putting them into practice.",
    "principals": "As a principal you juggle decisions that span pedagogy, finance, and personnel simultaneously. The prompts in this pack are written for that reality — situations where you need to formulate yourself quickly without compromising on precision.",
    "superintendents": "The superintendent's job is largely translation — strategy into school reality and back again. These prompts focus on the conversations you actually sit in: with politicians, principals, and administration, where the tone of the message often matters as much as its content.",
    "preschool": "Preschool pedagogy is playful, present, and built on relationships. The prompts here help you plan thematic work, document learning, and communicate with parents — without losing what makes preschool work in the first place.",
    "reception": "In reception (förskoleklass / årskurs F in Sweden) you meet each child where they are while quietly laying the foundation for literacy and numeracy. The prompts here address that transition — between play and structure — and the balancing act it requires.",

    # — Subject teachers, compulsory school —
    "art": "Art is about thinking visually — and helping students dare to do the same. The prompts here combine concrete lesson planning with support for how to talk about a student's expression without locking it into right or wrong.",
    "biology": "Biology is experimental, ethical, and systems-thinking all at once. These prompts cover everything from field-study and lab instructions to conversations about sustainability and evolution — engaging both the facts and the values that surround them.",
    "english": "English benefited from AI earlier than most subjects — students are already chatting with bots in English. The prompts here help you raise the level from simple translation toward real language development: nuance, register, and strategies for genuinely understanding.",
    "physics": "Physics asks students to both calculate and think in models. These prompts focus on the second — designing reasoning questions, qualitative tasks, and conversations about how nature actually works, not just what the formula says.",
    "geography": "Geography moves fast — climate, migration, and politics keep redrawing the map. The prompts here help keep teaching current and tie together the physical, the social, and the global without losing depth.",
    "home-economics": "Home economics combines cooking, budgeting, environment, and health in a hands-on classroom. The prompts here help with weekly menus that account for different diets, budget exercises with real numbers, and sustainability conversations that aren't moralistic.",
    "history": "History teaching is about seeing connections across time and separating the documented from the merely told. The prompts here support both source criticism and the narrative side — so students can analyse without losing engagement.",
    "physical-education": "PE covers motor skills, health, and conversations about body and well-being. The prompts here help you plan differentiated lessons, formulate conversations around sensitive topics, and build assessment support for what is hard to grade.",
    "chemistry": "Chemistry comes alive when a student understands why a reaction happens, not just that it does. The prompts here help you find everyday hooks, plan safer labs, and explain abstract concepts in ways that stick.",
    "mathematics": "Mathematics requires both precision and imagination — students need to compute, but also to reason. The prompts here balance the two: pure skills practice, problem-solving, and conversations about mathematical thinking as more than calculation.",
    "early-numeracy": "Early numeracy is where the foundation for all later mathematics is laid. The prompts here support the visual, tactile, and verbal work that comes before formulas — and that shapes whether a student sees themselves as a mathematical thinker.",
    "modern-languages": "Modern languages are often squeezed for time and need creative solutions. The prompts here help keep the language alive — cultural context, authentic texts, varied speaking practice — even when time and resources are limited.",
    "music": "Music is where students meet both theory and creative making. The prompts here help you plan units that hold both — from ear training and theory to band classrooms and big projects — without smothering creativity in structure.",
    "science": "Naturkunskap is upper-secondary natural science in Sweden — biology, chemistry, physics, and society in one syllabus. The prompts here help you find the big questions that cut across: climate, health, energy, ethics — where students need to reason from science.",
    "science-general": "Compulsory-school science teachers (NO in Sweden) teach all three natural sciences — often in the same week. The prompts here support that cross-subject reality: planning where labs, safety, and progression connect across subject boundaries.",
    "religious-studies": "Religious studies asks students to analyse without condemning and understand without adopting. These prompts help you frame lessons that open conversations about belief, ethics, and worldview — even in classrooms where opinions are strong and divided.",
    "social-studies": "Social studies should make students into citizens who think for themselves. The prompts here help you handle current politics in the classroom without taking sides, train source criticism, and design tasks where students argue from evidence.",
    "crafts": "Crafts is one of the few subjects where hand and brain genuinely work together. The prompts here focus on what surrounds the workshop time — planning, documentation, process assessment, conversations about quality — so the workshop time stays workshop time.",
    "social-studies-general": "SO teachers (samhällsorienterande ämnen in Sweden) juggle four subjects — history, geography, civics, religion — often with the same students. The prompts here help with planning and progression across subject boundaries, so the SO mandate hangs together.",
    "technology": "Technology as a subject changes shape fast — what was new five years ago is often everyday now. The prompts here help keep teaching relevant without chasing trends, and frame technical reasoning so students can think like engineers.",

    # — Subject teachers, upper secondary —
    "english-upper-secondary": "At upper secondary, students need more than communication — they should analyse language, culture, and texts. The prompts here support advanced work: literary analysis, academic writing, and conversations about English as a global lingua franca.",
    "history-upper-secondary": "Upper-secondary history goes deeper into method and use of history — students should evaluate sources and see how history is invoked today. The prompts here support both the academic analysis and the larger conversations about why history matters.",
    "physical-education-upper-secondary": "At upper secondary you meet students with vastly different relationships to sport — from elite athletes to the reluctant. These prompts help you differentiate without losing what the subject is about, and run conversations on health that touch both body and self-image.",
    "mathematics-upper-secondary": "Upper-secondary mathematics demands rigour and deep understanding both. The prompts here support the abstract — proof, modelling, problem-solving at higher levels — and help you frame tasks where students must reason, not just calculate.",
    "modern-languages-upper-secondary": "At upper secondary, students meet the language at advanced level — authentic texts, cultural nuance, academic writing. The prompts here help you plan content that matches the language students will actually need beyond the classroom.",
    "religious-studies-upper-secondary": "Upper-secondary religious analysis requires tools from several academic traditions. The prompts here help you teach at the level where students can compare worldviews systematically and form their own arguments without losing nuance.",
    "social-studies-upper-secondary": "Upper-secondary social studies takes politics, economics, and political science to an analytical level. The prompts here help you build tasks where students must apply theory to reality — not just reproduce textbook definitions.",

    # — Other teaching roles —
    "edtech-coaches": "EdTech coaches sit at the intersection of technology, pedagogy, and change management. The prompts in this pack support both concrete classroom use and the strategic conversations with colleagues and leadership.",
    "lead-teachers": "The lead-teacher role asks for both subject expertise and the ability to lead colleagues who aren't your reports. The prompts here help you formulate collegial feedback, lead subject development, and translate research into things that actually happen in classrooms.",

    # — Support staff —
    "after-school-care": "After-school care should complement what school does without copying it. The prompts here help you plan meaningful activities, document learning through play, and talk to parents about the child's whole day — including the part that doesn't get a grade.",
    "special-education-teachers": "Special education teachers usually work one-to-one or in small groups, where every student starts from a unique place. The prompts here help you adapt material, formulate goals concrete enough to evaluate, and document progress that can otherwise be hard to see.",
    "student-assistants": "The student assistant works close to one student inside the class as a whole — a balance that asks for serious pedagogical judgment. These prompts help you formulate adaptations, communicate with the teacher about the student, and find ways to support without taking over.",
    "career-counselors": "Career counselling means meeting young people who are shaping a future on a labour market that changes faster than the curriculum. The prompts here support the conversations, the planning, and the documentation — so the guidance holds up even for a 14-year-old who doesn't yet know what they want.",
    "special-education-specialists": "The special education specialist works with individual students, with teachers, and with the school's pedagogical structure. The prompts here support the strategic side — pedagogical mapping, action plans, supervising colleagues — where the wording often determines what actually happens.",
    "school-nurses": "The school nurse meets students on questions that span health, identity, vulnerability, and pedagogy. These prompts help with documentation, conversation structures, and communication with parents and school — in ways that hold up to both data-protection rules and the student's trust.",
    "school-counselors": "The school counsellor works in a world where student cases are often urgent and resources finite. The prompts here focus on what surrounds the conversations — documentation, collaboration, structured intake — so that time in the conversation room can be about the student.",
    "school-psychologists": "The school psychologist runs advanced assessments and contributes to the larger student-health team — usually on limited time. The prompts here support the written work, from assessment reports to supervision prep, so you can spend more time on the clinical side.",
    "school-caretakers": "The school caretaker sees everything — from broken locks and coffee machines to a student having a bad day. The prompts here help you formulate maintenance plans, safety routines, and supplier communication — for the admin work that takes time from the practical work.",
    "school-catering-staff": "The school kitchen often serves hundreds of meals a day, follows special diets, and is meant to be educational. The prompts here help with weekly menus, communication with parents about allergies, and conversations in the dining hall that make the meal more than just food.",
    "school-it-managers": "School-level IT staff face GDPR, teachers' stress, and students' creative ways around restrictions all at once. The prompts here help you formulate clear procedures, communicate technically without jargon, and make solid decisions when time is short.",
    "district-it-managers": "At district IT level, decisions affect the whole authority's student population and multi-year contracts. The prompts here support the strategic work — procurement documents, security analyses, communication with leadership — where one phrase can steer significant budgets.",
    "school-librarians": "The school library is one of the most important pedagogical resources at the school — and one of the most underused. The prompts here help you plan teacher collaborations, formulate book introductions, and lead information-literacy conversations that build source criticism.",
    "education-strategists": "The school strategist's job is to translate operations into strategy and back — usually across the whole district. The prompts here support the written side: analyses, decision documents, communication with leadership and politics, where tone determines whether the message lands.",
    "school-administrators": "The school administrator keeps the operational engine running — scheduling, attendance, parent communication. The prompts here help you formulate clear messages and document routines so the operation flows even when a teacher is absent.",
    "district-administrators": "District-level administration holds finance, statistics, and reporting together for a whole authority. The prompts here support the highly formalised work — minutes, reports, budget texts — where an exact phrase can save or burn hours downstream.",

    # — Thematic —
    "digital-tools": "Digitalisation in school isn't a goal in itself — it's a means that sometimes fits and sometimes doesn't. The prompts here help you choose, evaluate, and use digital tools where they actually add something, and skip them where they only create friction.",
    "cross-curricular": "Cross-curricular work lets students see how knowledge connects — but it also takes more planning than a single-subject unit. The prompts here support the organisational work, so collaboration between teachers becomes productive instead of complicated.",
    "outdoor-education": "Outdoor education places teaching in a setting where body and senses are genuinely engaged. The prompts here help you plan lessons that use the place's potential, formulate goals tied to the curriculum, and handle the practical side around it.",
    "research-on-learning": "Research on learning makes a difference in the classroom only when it gets translated into concrete teaching. The prompts here help you take evidence-based conclusions — about feedback, cognitive load, retrieval practice — and turn them into lesson structures and tasks that actually work.",
    "time-management": "Time pressure is something I have met both as a teacher and as a school leader. These prompts are about winning hours back — on grading, planning, and meetings — without giving up quality.",
}


# ─── Shared P2 (bio) and P4 (audience) ─────────────────────────────────
SHARED_P2 = {
    "sv": ("Promptarna är framtagna av mig, Johan Lindström. Med en gedigen "
           "bakgrund som lärare, skolledare och utbildningsansvarig vet jag "
           "vad som skiljer en allmän AI-prompt på internet från en som "
           "faktiskt fungerar i ett skolsammanhang. En generell prompt tar "
           "inte hänsyn till åldersgrupper, läroplan eller hur en lärares "
           "eller skolledares vardag ser ut. Det gör de här promptarna. "
           "Varje prompt är skriven med ett tydligt syfte — du fyller bara "
           "i hakparenteserna med din egen kontext för att maximera "
           "promptens nytta för dig."),
    "en": ("These prompts are written by me, Johan Lindström. With a solid "
           "background as a teacher, school leader, and head of education, "
           "I know what separates a generic AI prompt online from one that "
           "actually works in a school context. A generic prompt doesn't "
           "account for age groups, curriculum, or what a teacher's or "
           "school leader's day actually looks like. These do. Every "
           "prompt is written with a clear purpose — you just fill in the "
           "bracketed placeholders with your own context to maximize the "
           "prompt's usefulness for you."),
}

SHARED_P4 = {
    "sv": ("Promptarna är framför allt till för dig som ännu inte är så van "
           "vid att prompta — du får färdiga mallar att utgå från och göra "
           "till dina egna. Är du redan en van AI-användare kan du använda "
           "dem som idébank, eller analysera "
           "<a href=\"/sv/promptar/megapromptar-1/\">megapromptarna</a> för "
           "att se hur de är uppbyggda och lära dig mönstret bakom."),
    "en": ("The prompts are aimed mainly at those of you who aren't yet "
           "comfortable with prompting — you get ready-made templates to "
           "start from and adapt. If you're already an experienced AI user, "
           "treat them as an idea bank, or study the "
           "<a href=\"/prompts/megaprompts-1/\">megaprompts</a> to see how "
           "they're built and learn the structure behind them."),
}
