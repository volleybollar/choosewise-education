"""Manifest: single source of truth for the prompt-library batch.

Encodes every decision made during the pilot, so that downstream scripts
(extract → translate → generate HTML → render PDF) can act on consistent
metadata. If you change a translation, a category, or a URL slug, do it
here — not inline in the scripts.

The scripts scan ~/Desktop/Promptar för rebranding/Del 1-63/ for folders
and look each up by the folder's display name (without the leading number).
Folders not listed here are skipped with a warning.
"""
from pathlib import Path

SOURCE_DIR = Path.home() / "Desktop" / "Promptar för rebranding" / "Del 1-63"

# ───────────────────────────────────────────────────────────────
# Category taxonomy (matches the library-index filter pills)
# ───────────────────────────────────────────────────────────────
CATEGORIES = {
    "teachers":  "Classroom teachers",   # generalist teachers / role-based
    "subject":   "Subject specialists",  # subject-teacher packs
    "leaders":   "School leaders",       # principals, head office
    "support":   "Support staff",        # counselors, nurses, admin, IT, etc.
    "themes":    "Thematic",             # topic-based (not role-based)
}

# ───────────────────────────────────────────────────────────────
# Per-pack metadata
#
#   folder:  folder name inside Del 1-63/ (Swedish, as on disk)
#   slug_en: URL slug for English page (lowercased, hyphenated)
#   slug_sv: URL slug for Swedish page
#   title_en: English cover title ("Prompts for X Teachers.")
#   title_sv: Swedish cover title
#   eyebrow_en: Small label above cover title (e.g. "For Teachers")
#   eyebrow_sv: Same in Swedish
#   category: one of CATEGORIES
#   sv_only: True if no English translation should be generated
#   special: True for megapromptar that need custom layout (handle later)
# ───────────────────────────────────────────────────────────────
PACKS = [
    # Role-based / general
    {"folder": "1 Lärare", "slug_en": "teachers", "slug_sv": "larare",
     "title_en": "Prompts for Teachers.", "title_sv": "Promptar för lärare.",
     "eyebrow_en": "For Teachers", "eyebrow_sv": "För lärare",
     "category": "teachers"},
    {"folder": "2 Lär dig nya saker", "slug_en": "learning-new-skills", "slug_sv": "lar-dig-nya-saker",
     "title_en": "Prompts for Learning New Skills.", "title_sv": "Promptar för att lära dig nya saker.",
     "eyebrow_en": "For Anyone Learning", "eyebrow_sv": "För den som vill lära sig nya saker",
     "category": "themes"},
    {"folder": "3 Rektorer", "slug_en": "principals", "slug_sv": "rektorer",
     "title_en": "Prompts for Principals.", "title_sv": "Promptar för rektorer.",
     "eyebrow_en": "For Principals", "eyebrow_sv": "För rektorer",
     "category": "leaders"},
    {"folder": "4 Skolchefer", "slug_en": "superintendents", "slug_sv": "skolchefer",
     "title_en": "Prompts for Superintendents.", "title_sv": "Promptar för skolchefer.",
     "eyebrow_en": "For Superintendents", "eyebrow_sv": "För skolchefer",
     "category": "leaders"},
    {"folder": "5 Förskola", "slug_en": "preschool", "slug_sv": "forskola",
     "title_en": "Prompts for Preschool Teachers.", "title_sv": "Promptar för förskolan.",
     "eyebrow_en": "For Preschool Teachers", "eyebrow_sv": "För förskolan",
     "category": "teachers"},
    {"folder": "6 Förskoleklass", "slug_en": "reception", "slug_sv": "forskoleklass",
     "title_en": "Prompts for Reception Teachers.", "title_sv": "Promptar för förskoleklass.",
     "eyebrow_en": "For Reception Teachers · Ages 6–7", "eyebrow_sv": "För förskoleklass",
     "category": "teachers"},

    # Subject teachers — compulsory school
    {"folder": "7 Bildlärare", "slug_en": "art", "slug_sv": "bild",
     "title_en": "Prompts for Art Teachers.", "title_sv": "Promptar för bildlärare.",
     "eyebrow_en": "For Art Teachers", "eyebrow_sv": "För bildlärare",
     "category": "subject"},
    {"folder": "8 Biologi", "slug_en": "biology", "slug_sv": "biologi",
     "title_en": "Prompts for Biology Teachers.", "title_sv": "Promptar för biologilärare.",
     "eyebrow_en": "For Biology Teachers", "eyebrow_sv": "För biologilärare",
     "category": "subject"},
    {"folder": "9 Lärare Engelska", "slug_en": "english", "slug_sv": "engelska",
     "title_en": "Prompts for English Teachers.", "title_sv": "Promptar för engelsklärare.",
     "eyebrow_en": "For English Teachers", "eyebrow_sv": "För engelsklärare",
     "category": "subject"},
    {"folder": "11 Fysik", "slug_en": "physics", "slug_sv": "fysik",
     "title_en": "Prompts for Physics Teachers.", "title_sv": "Promptar för fysiklärare.",
     "eyebrow_en": "For Physics Teachers", "eyebrow_sv": "För fysiklärare",
     "category": "subject"},
    {"folder": "12 Geografi", "slug_en": "geography", "slug_sv": "geografi",
     "title_en": "Prompts for Geography Teachers.", "title_sv": "Promptar för geografilärare.",
     "eyebrow_en": "For Geography Teachers", "eyebrow_sv": "För geografilärare",
     "category": "subject"},
    {"folder": "13 HKK", "slug_en": "home-economics", "slug_sv": "hkk",
     "title_en": "Prompts for Home Economics Teachers.", "title_sv": "Promptar för HKK-lärare.",
     "eyebrow_en": "For Home Economics Teachers", "eyebrow_sv": "För HKK-lärare",
     "category": "subject"},
    {"folder": "14 Historia", "slug_en": "history", "slug_sv": "historia",
     "title_en": "Prompts for History Teachers.", "title_sv": "Promptar för historielärare.",
     "eyebrow_en": "For History Teachers", "eyebrow_sv": "För historielärare",
     "category": "subject"},
    {"folder": "16 IDH", "slug_en": "physical-education", "slug_sv": "idh",
     "title_en": "Prompts for PE Teachers.", "title_sv": "Promptar för IDH-lärare.",
     "eyebrow_en": "For PE Teachers", "eyebrow_sv": "För IDH-lärare",
     "category": "subject"},
    {"folder": "18 Kemi", "slug_en": "chemistry", "slug_sv": "kemi",
     "title_en": "Prompts for Chemistry Teachers.", "title_sv": "Promptar för kemilärare.",
     "eyebrow_en": "For Chemistry Teachers", "eyebrow_sv": "För kemilärare",
     "category": "subject"},
    {"folder": "19 Matematiklärare", "slug_en": "mathematics", "slug_sv": "matematik",
     "title_en": "Prompts for Mathematics Teachers.", "title_sv": "Promptar för matematiklärare.",
     "eyebrow_en": "For Mathematics Teachers", "eyebrow_sv": "För matematiklärare",
     "category": "subject"},
    {"folder": "20 Lära sig räkna", "slug_en": "early-numeracy", "slug_sv": "lara-sig-rakna",
     "title_en": "Prompts for Early Numeracy.", "title_sv": "Promptar för tidig matematikinlärning.",
     "eyebrow_en": "For Early-Numeracy Teachers", "eyebrow_sv": "För tidig räkneinlärning",
     "category": "subject"},
    {"folder": "22 Moderna språk", "slug_en": "modern-languages", "slug_sv": "moderna-sprak",
     "title_en": "Prompts for Modern Languages Teachers.", "title_sv": "Promptar för lärare i moderna språk.",
     "eyebrow_en": "For Modern Languages Teachers", "eyebrow_sv": "För lärare i moderna språk",
     "category": "subject"},
    {"folder": "24 Musiklärare", "slug_en": "music", "slug_sv": "musik",
     "title_en": "Prompts for Music Teachers.", "title_sv": "Promptar för musiklärare.",
     "eyebrow_en": "For Music Teachers", "eyebrow_sv": "För musiklärare",
     "category": "subject"},
    {"folder": "25 Naturkunskap", "slug_en": "science", "slug_sv": "naturkunskap",
     "title_en": "Prompts for Science Teachers.", "title_sv": "Promptar för lärare i naturkunskap.",
     "eyebrow_en": "For Science Teachers", "eyebrow_sv": "För lärare i naturkunskap",
     "category": "subject"},
    {"folder": "26 NO-lärare", "slug_en": "science-general", "slug_sv": "no",
     "title_en": "Prompts for Science Teachers (General).", "title_sv": "Promptar för NO-lärare.",
     "eyebrow_en": "For Science Teachers (Biology · Physics · Chemistry)", "eyebrow_sv": "För NO-lärare",
     "category": "subject"},
    {"folder": "27 Religion", "slug_en": "religious-studies", "slug_sv": "religion",
     "title_en": "Prompts for Religious Studies Teachers.", "title_sv": "Promptar för religionslärare.",
     "eyebrow_en": "For Religious Studies Teachers", "eyebrow_sv": "För religionslärare",
     "category": "subject"},
    {"folder": "29 Samhällskunskap", "slug_en": "social-studies", "slug_sv": "samhallskunskap",
     "title_en": "Prompts for Social Studies Teachers.", "title_sv": "Promptar för SH-lärare.",
     "eyebrow_en": "For Social Studies Teachers", "eyebrow_sv": "För samhällskunskapslärare",
     "category": "subject"},
    {"folder": "31 Slöjdlärare", "slug_en": "crafts", "slug_sv": "slojd",
     "title_en": "Prompts for Crafts Teachers.", "title_sv": "Promptar för slöjdlärare.",
     "eyebrow_en": "For Crafts Teachers", "eyebrow_sv": "För slöjdlärare",
     "category": "subject"},
    {"folder": "32 SO-lärare", "slug_en": "social-studies-general", "slug_sv": "so",
     "title_en": "Prompts for Social Studies Teachers (General).", "title_sv": "Promptar för SO-lärare.",
     "eyebrow_en": "For Social Studies Teachers (History · Geography · Civics · Religion)",
     "eyebrow_sv": "För SO-lärare",
     "category": "subject"},
    {"folder": "38 Tekniklärare", "slug_en": "technology", "slug_sv": "teknik",
     "title_en": "Prompts for Technology Teachers.", "title_sv": "Promptar för tekniklärare.",
     "eyebrow_en": "For Technology Teachers", "eyebrow_sv": "För tekniklärare",
     "category": "subject"},

    # Subject teachers — upper secondary (gymnasium)
    {"folder": "10 Engelska gymnasiet", "slug_en": "english-upper-secondary", "slug_sv": "engelska-gymnasiet",
     "title_en": "Prompts for English Teachers · Upper Secondary.",
     "title_sv": "Promptar för engelsklärare på gymnasiet.",
     "eyebrow_en": "For Teachers · Ages 16–19", "eyebrow_sv": "För engelsklärare på gymnasiet",
     "category": "subject"},
    {"folder": "15 Historia Gymnasiet", "slug_en": "history-upper-secondary", "slug_sv": "historia-gymnasiet",
     "title_en": "Prompts for History Teachers · Upper Secondary.",
     "title_sv": "Promptar för historielärare på gymnasiet.",
     "eyebrow_en": "For Teachers · Ages 16–19", "eyebrow_sv": "För historielärare på gymnasiet",
     "category": "subject"},
    {"folder": "17 IDH gymnasiet", "slug_en": "physical-education-upper-secondary", "slug_sv": "idh-gymnasiet",
     "title_en": "Prompts for PE Teachers · Upper Secondary.",
     "title_sv": "Promptar för IDH-lärare på gymnasiet.",
     "eyebrow_en": "For Teachers · Ages 16–19", "eyebrow_sv": "För IDH-lärare på gymnasiet",
     "category": "subject"},
    {"folder": "21 Matematik gymnasiet", "slug_en": "mathematics-upper-secondary", "slug_sv": "matematik-gymnasiet",
     "title_en": "Prompts for Mathematics Teachers · Upper Secondary.",
     "title_sv": "Promptar för matematiklärare på gymnasiet.",
     "eyebrow_en": "For Teachers · Ages 16–19", "eyebrow_sv": "För matematiklärare på gymnasiet",
     "category": "subject"},
    {"folder": "23 Moderna språk gymnasiet", "slug_en": "modern-languages-upper-secondary", "slug_sv": "moderna-sprak-gymnasiet",
     "title_en": "Prompts for Modern Languages Teachers · Upper Secondary.",
     "title_sv": "Promptar för lärare i moderna språk på gymnasiet.",
     "eyebrow_en": "For Teachers · Ages 16–19", "eyebrow_sv": "För moderna språk på gymnasiet",
     "category": "subject"},
    {"folder": "28 Religion gymnasiet", "slug_en": "religious-studies-upper-secondary", "slug_sv": "religion-gymnasiet",
     "title_en": "Prompts for Religious Studies Teachers · Upper Secondary.",
     "title_sv": "Promptar för religionslärare på gymnasiet.",
     "eyebrow_en": "For Teachers · Ages 16–19", "eyebrow_sv": "För religionslärare på gymnasiet",
     "category": "subject"},
    {"folder": "30 Samhällskunskap gymnasiet", "slug_en": "social-studies-upper-secondary", "slug_sv": "samhallskunskap-gymnasiet",
     "title_en": "Prompts for Social Studies Teachers · Upper Secondary.",
     "title_sv": "Promptar för SH-lärare på gymnasiet.",
     "eyebrow_en": "For Teachers · Ages 16–19", "eyebrow_sv": "För samhällskunskapslärare på gymnasiet",
     "category": "subject"},

    # Swedish-only subjects (no English translation)
    {"folder": "24 Modersmål", "slug_sv": "modersmal", "title_sv": "Promptar för modersmålslärare.",
     "eyebrow_sv": "För modersmålslärare", "category": "subject", "sv_only": True},
    {"folder": "33 Svenska", "slug_sv": "svenska", "title_sv": "Promptar för svensklärare.",
     "eyebrow_sv": "För svensklärare", "category": "subject", "sv_only": True},
    {"folder": "34 Läs- och skrivinlärning", "slug_sv": "las-och-skrivinlarning",
     "title_sv": "Promptar för läs- och skrivinlärning.",
     "eyebrow_sv": "För läs- och skrivinlärning", "category": "subject", "sv_only": True},
    {"folder": "35 Svenska gymnasiet", "slug_sv": "svenska-gymnasiet",
     "title_sv": "Promptar för svensklärare på gymnasiet.",
     "eyebrow_sv": "För svensklärare på gymnasiet", "category": "subject", "sv_only": True},
    {"folder": "36 SVA", "slug_sv": "sva", "title_sv": "Promptar för SVA-lärare.",
     "eyebrow_sv": "För SVA-lärare", "category": "subject", "sv_only": True},
    {"folder": "37 SVA Gymnasiet", "slug_sv": "sva-gymnasiet",
     "title_sv": "Promptar för SVA-lärare på gymnasiet.",
     "eyebrow_sv": "För SVA-lärare på gymnasiet", "category": "subject", "sv_only": True},

    # Other teacher roles
    {"folder": "39 IKT-pedagoger", "slug_en": "edtech-coaches", "slug_sv": "ikt-pedagoger",
     "title_en": "Prompts for EdTech Coaches.", "title_sv": "Promptar för IKT-pedagoger.",
     "eyebrow_en": "For EdTech Coaches", "eyebrow_sv": "För IKT-pedagoger",
     "category": "teachers"},
    {"folder": "40 Förstelärare", "slug_en": "lead-teachers", "slug_sv": "forstelarare",
     "title_en": "Prompts for Lead Teachers.", "title_sv": "Promptar för förstelärare.",
     "eyebrow_en": "For Lead Teachers", "eyebrow_sv": "För förstelärare",
     "category": "teachers"},

    # Support staff
    {"folder": "41 Fritids", "slug_en": "after-school-care", "slug_sv": "fritids",
     "title_en": "Prompts for After-School Care Staff.", "title_sv": "Promptar för personal på fritids.",
     "eyebrow_en": "For After-School Care Staff", "eyebrow_sv": "För personal på fritids",
     "category": "support"},
    {"folder": "42 speciallärare", "slug_en": "special-education-teachers", "slug_sv": "speciallarare",
     "title_en": "Prompts for Special Education Teachers.", "title_sv": "Promptar för speciallärare.",
     "eyebrow_en": "For Special Education Teachers", "eyebrow_sv": "För speciallärare",
     "category": "support"},
    {"folder": "43 Elevassistenter", "slug_en": "student-assistants", "slug_sv": "elevassistenter",
     "title_en": "Prompts for Student Assistants.", "title_sv": "Promptar för elevassistenter.",
     "eyebrow_en": "For Student Assistants", "eyebrow_sv": "För elevassistenter",
     "category": "support"},
    {"folder": "44 SYV", "slug_en": "career-counselors", "slug_sv": "syv",
     "title_en": "Prompts for Career Counselors.", "title_sv": "Promptar för SYV.",
     "eyebrow_en": "For Career Counselors", "eyebrow_sv": "För studie- och yrkesvägledare",
     "category": "support"},
    {"folder": "44 Specialpedagoger", "slug_en": "special-education-specialists", "slug_sv": "specialpedagoger",
     "title_en": "Prompts for Special Education Specialists.", "title_sv": "Promptar för specialpedagoger.",
     "eyebrow_en": "For Special Education Specialists", "eyebrow_sv": "För specialpedagoger",
     "category": "support"},
    {"folder": "45 skolsköterskor", "slug_en": "school-nurses", "slug_sv": "skolskoterskor",
     "title_en": "Prompts for School Nurses.", "title_sv": "Promptar för skolsköterskor.",
     "eyebrow_en": "For School Nurses", "eyebrow_sv": "För skolsköterskor",
     "category": "support"},
    {"folder": "46 Kuratorer", "slug_en": "school-counselors", "slug_sv": "kuratorer",
     "title_en": "Prompts for School Counselors.", "title_sv": "Promptar för kuratorer.",
     "eyebrow_en": "For School Counselors", "eyebrow_sv": "För kuratorer",
     "category": "support"},
    {"folder": "47 skolpsykologer", "slug_en": "school-psychologists", "slug_sv": "skolpsykologer",
     "title_en": "Prompts for School Psychologists.", "title_sv": "Promptar för skolpsykologer.",
     "eyebrow_en": "For School Psychologists", "eyebrow_sv": "För skolpsykologer",
     "category": "support"},
    {"folder": "48 skolvaktmästare", "slug_en": "school-caretakers", "slug_sv": "skolvaktmastare",
     "title_en": "Prompts for School Caretakers.", "title_sv": "Promptar för skolvaktmästare.",
     "eyebrow_en": "For School Caretakers", "eyebrow_sv": "För skolvaktmästare",
     "category": "support"},
    {"folder": "49 Skolmåltidspersonal", "slug_en": "school-catering-staff", "slug_sv": "skolmaltidspersonal",
     "title_en": "Prompts for School Catering Staff.", "title_sv": "Promptar för skolmåltidspersonal.",
     "eyebrow_en": "For School Catering Staff", "eyebrow_sv": "För skolmåltidspersonal",
     "category": "support"},
    {"folder": "50 it-ansvariga skola", "slug_en": "school-it-managers", "slug_sv": "it-ansvariga-skola",
     "title_en": "Prompts for School IT Managers.", "title_sv": "Promptar för IT-ansvariga på skolan.",
     "eyebrow_en": "For School IT Managers", "eyebrow_sv": "För IT-ansvariga på skolan",
     "category": "support"},
    {"folder": "51 it-ansvariga central nivå", "slug_en": "district-it-managers", "slug_sv": "it-ansvariga-central",
     "title_en": "Prompts for District IT Managers.", "title_sv": "Promptar för IT-ansvariga på central nivå.",
     "eyebrow_en": "For District IT Managers", "eyebrow_sv": "För IT-ansvariga på central nivå",
     "category": "support"},
    {"folder": "52 Skolbibliotekarier", "slug_en": "school-librarians", "slug_sv": "skolbibliotekarier",
     "title_en": "Prompts for School Librarians.", "title_sv": "Promptar för skolbibliotekarier.",
     "eyebrow_en": "For School Librarians", "eyebrow_sv": "För skolbibliotekarier",
     "category": "support"},
    {"folder": "52 strateger", "slug_en": "education-strategists", "slug_sv": "strateger",
     "title_en": "Prompts for Education Strategists.", "title_sv": "Promptar för strateger.",
     "eyebrow_en": "For Education Strategists", "eyebrow_sv": "För strateger",
     "category": "leaders"},
    {"folder": "53 Administratörer", "slug_en": "school-administrators", "slug_sv": "administratorer",
     "title_en": "Prompts for School Administrators.", "title_sv": "Promptar för skoladministratörer.",
     "eyebrow_en": "For School Administrators", "eyebrow_sv": "För skoladministratörer",
     "category": "support"},
    {"folder": "54 Admin central nivå", "slug_en": "district-administrators", "slug_sv": "admin-central",
     "title_en": "Prompts for District Administrators.", "title_sv": "Promptar för administratörer på central nivå.",
     "eyebrow_en": "For District Administrators", "eyebrow_sv": "För administratörer på central nivå",
     "category": "support"},

    # Thematic
    {"folder": "55 Digitala verktyg", "slug_en": "digital-tools", "slug_sv": "digitala-verktyg",
     "title_en": "Prompts for Digital Tools in Education.", "title_sv": "Promptar om digitala verktyg i skolan.",
     "eyebrow_en": "Thematic · Digital Tools", "eyebrow_sv": "Tematiskt · Digitala verktyg",
     "category": "themes"},
    # 56 AI i undervisningen — source has only a .pages template, no finished PDF.
    # Excluded by the user from this batch.
    {"folder": "57 Ämnesövergripande arbete", "slug_en": "cross-curricular", "slug_sv": "amnesovergripande",
     "title_en": "Prompts for Cross-Curricular Work.", "title_sv": "Promptar om ämnesövergripande arbete.",
     "eyebrow_en": "Thematic · Cross-Curricular", "eyebrow_sv": "Tematiskt · Ämnesövergripande",
     "category": "themes"},
    {"folder": "58 Utomhuspedagogik", "slug_en": "outdoor-education", "slug_sv": "utomhuspedagogik",
     "title_en": "Prompts for Outdoor Education.", "title_sv": "Promptar om utomhuspedagogik.",
     "eyebrow_en": "Thematic · Outdoor Education", "eyebrow_sv": "Tematiskt · Utomhuspedagogik",
     "category": "themes"},
    {"folder": "59 Studier om lärande", "slug_en": "research-on-learning", "slug_sv": "studier-om-larande",
     "title_en": "Prompts Grounded in Research on Learning.", "title_sv": "Promptar grundade i forskning om lärande.",
     "eyebrow_en": "Thematic · Research on Learning", "eyebrow_sv": "Tematiskt · Studier om lärande",
     "category": "themes"},
    {"folder": "60 Effektivt tidsutnyttjande", "slug_en": "time-management", "slug_sv": "tidsutnyttjande",
     "title_en": "Prompts for Effective Time Use.", "title_sv": "Promptar för effektivt tidsutnyttjande.",
     "eyebrow_en": "Thematic · Time Management", "eyebrow_sv": "Tematiskt · Tidsutnyttjande",
     "category": "themes"},

    # Megapromptar — structurally different, handled as special cases
    {"folder": "61 Megapromptar 1", "slug_en": "megaprompts-1", "slug_sv": "megapromptar-1",
     "title_en": "Megaprompts #1.", "title_sv": "Megapromptar #1.",
     "eyebrow_en": "Megaprompts · Vol. 1", "eyebrow_sv": "Megapromptar · Vol. 1",
     "category": "themes", "special": True},
    {"folder": "62 Megapromptar 2", "slug_en": "megaprompts-2", "slug_sv": "megapromptar-2",
     "title_en": "Megaprompts #2.", "title_sv": "Megapromptar #2.",
     "eyebrow_en": "Megaprompts · Vol. 2", "eyebrow_sv": "Megapromptar · Vol. 2",
     "category": "themes", "special": True},
    {"folder": "63 Megapromptar 3", "slug_en": "megaprompts-3", "slug_sv": "megapromptar-3",
     "title_en": "Megaprompts #3.", "title_sv": "Megapromptar #3.",
     "eyebrow_en": "Megaprompts · Vol. 3", "eyebrow_sv": "Megapromptar · Vol. 3",
     "category": "themes", "special": True},
]


def _norm(s: str) -> str:
    """Unicode-normalise so HFS+ NFD filenames compare equal to NFC source."""
    import unicodedata
    return unicodedata.normalize("NFC", s)


def pack_by_folder(folder_name: str):
    """Look up a pack by its folder name. Returns None if not in manifest."""
    target = _norm(folder_name)
    for p in PACKS:
        if _norm(p["folder"]) == target:
            return p
    return None


def translatable_packs():
    """Packs that should be translated to English (not sv_only, not special)."""
    return [p for p in PACKS if not p.get("sv_only") and not p.get("special")]


def sv_only_packs():
    return [p for p in PACKS if p.get("sv_only")]


def special_packs():
    return [p for p in PACKS if p.get("special")]


if __name__ == "__main__":
    # Sanity check: report pack counts and flag missing folders
    on_disk = {_norm(d.name) for d in SOURCE_DIR.iterdir() if d.is_dir()}
    in_manifest = {_norm(p["folder"]) for p in PACKS}

    missing = on_disk - in_manifest
    extra   = in_manifest - on_disk

    print(f"Packs in manifest: {len(PACKS)}")
    print(f"Folders on disk:   {len(on_disk)}")
    print(f"  Translatable:    {len(translatable_packs())}")
    print(f"  Swedish-only:    {len(sv_only_packs())}")
    print(f"  Special layout:  {len(special_packs())}")
    if missing:
        print(f"\nOn disk but NOT in manifest (will be skipped):")
        for f in sorted(missing): print(f"  · {f}")
    if extra:
        print(f"\nIn manifest but NOT on disk (typo?):")
        for f in sorted(extra): print(f"  · {f}")
