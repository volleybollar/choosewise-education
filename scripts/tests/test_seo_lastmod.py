"""Stämpeln får inte läsa sig själv som en innehållsändring.

`git_lastmod()` härleder "senast uppdaterad" ur senaste commit som rörde
filen — men att skriva stämpeln ÄR en sådan commit. Utan en spärr läser
nästa körning alltså sitt eget förra utdata och skriver dagens datum på en
sida som inte ändrats sedan i våras. Mätt i verkligheten: commit `9c6390c`
ändrade `about/index.html` på fyra rader, och alla fyra bar ett datumfält.

Vakten konstruerar det fallet i riktiga git-repon i temporära kataloger.

Två saker i den här filen är inte stil utan bärande konstruktion:

1. **Sidorna byggs av skriptets EGNA generatorer**, aldrig av handskrivna
   radformer. `_GENERATED_LINES` är ankrade helradsmönster, och en fixtur
   som skriver sin egen variant av en rad kan matcha masken samtidigt som
   den verkliga raden slutat göra det. Granskaren visade det: en mask
   smalnad till `<aside class="page-last-updated"><time.*</aside>$`
   matchar en handskriven fixtur men inte skriptets aside, som bär
   `aria-label` — fem gröna tester och buggen helt tillbaka. Härleds
   fixturen ur generatorn kan masken och fixturen inte glida isär.

2. **Inget förväntat datum får vara dagens, och filens mtime sätts till
   `MTIME_SENTINEL`.** Faller `git_lastmod` igenom till mtime-ledet ska
   svaret bli omöjligt att förväxla med ett commitdatum. Utan det blev två
   av testerna gröna under sabotage: allt hoppades över, mtime var dagens
   datum, och det var precis vad de assertade.
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PAGE = "about/index.html"

# Ett datum ingen commit i testerna bär och som aldrig kan vara "i dag".
MTIME_SENTINEL = datetime(1999, 1, 1, 12, tzinfo=timezone.utc)
MTIME_SENTINEL_DATE = "1999-01-01"

# Commitdatum. Inget av dem är dagens datum — se punkt 2 i modulens
# docstring. INNEHALL är den äldre, riktiga innehållsändringen; TOPP är
# commiten ovanpå den som testerna varierar.
INNEHALL = "2026-10-07T13:57:55+02:00"
INNEHALL_DATE = "2026-10-07"
# Det föräldralösa blockets frusna datum, som 2026-04-24 i verkligheten.
FORALDRALOST_DATE = "2026-04-24"
TOPP = "2026-10-11T09:14:02+02:00"
TOPP_DATE = "2026-10-11"

_IDENTITY = {
    "GIT_AUTHOR_NAME": "Vakt", "GIT_AUTHOR_EMAIL": "vakt@example.invalid",
    "GIT_COMMITTER_NAME": "Vakt", "GIT_COMMITTER_EMAIL": "vakt@example.invalid",
}


def _seo_module():
    spec = importlib.util.spec_from_file_location(
        "build_seo_meta", ROOT / "scripts/build-seo-meta.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _git(repo: Path, *args: str, date: str | None = None) -> None:
    import os
    env = {**os.environ, **_IDENTITY}
    if date:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = date
    subprocess.run(["git", *args], cwd=repo, env=env,
                   check=True, capture_output=True, text=True)


def _page(seo, body: str, date: str, stamped: bool = True) -> str:
    """En sida byggd av SKRIPTETS EGNA generatorer, inte för hand.

    `stamped=False` ger sidan som den ser ut innan den blev section
    landing: seo-blocket byggs då för en kanonisk sökväg som inte står i
    `SECTION_LANDINGS`, så JSON-LD:n saknar både sidentitet och
    `dateModified` och inget last-updated-block injiceras — precis så
    `infographic-styles/index.html` såg ut före 2026-10-13.

    Att `build_seo_block()` och `build_last_updated_block()` anropas i
    stället för att radformerna skrivs av är det som binder `_GENERATED_LINES`
    till verkligheten. Ändrar en generator sin rad följer fixturen med, och
    en mask som slutat matcha blir röd här.
    """
    html = (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n</head>\n<body>\n'
        "<main>\n"
        f"<p>{body}</p>\n"
        "</main>\n</body>\n</html>\n"
    )
    canonical = seo.path_to_canonical(PAGE)
    assert canonical in seo.SECTION_LANDINGS, (
        f"{canonical} står inte längre i SECTION_LANDINGS — fixturen bygger "
        "inte det läge den påstår")
    if stamped:
        html = seo.inject_head(
            html, seo.build_seo_block(canonical, "en", html, date))
        return seo.inject_last_updated(
            html, seo.build_last_updated_block("en", date))

    # Samma kanoniska sökväg, bara utan att vara section landing — exakt
    # den skillnad som skildes 2026-10-13. Byts sökvägen i stället ändras
    # canonical- och hreflang-raderna med, och diffen bär då en skillnad
    # som det verkliga fallet aldrig hade.
    #
    # Last-updated-blocket står kvar, med sitt gamla datum. Det är poängen:
    # `infographic-styles/index.html` BAR ett föräldralöst block fruset på
    # 2026-04-24 medan JSON-LD:n saknade `dateModified` helt. Byggs sidan
    # utan blocket blir markörraderna tillagda i diffen, och fixturen
    # skildrar en förstagångsinjektion i stället för regressionen.
    saved = seo.SECTION_LANDINGS.pop(canonical)
    try:
        html = seo.inject_head(
            html, seo.build_seo_block(canonical, "en", html, date))
    finally:
        seo.SECTION_LANDINGS[canonical] = saved
    return seo.inject_last_updated(
        html, seo.build_last_updated_block("en", FORALDRALOST_DATE))


def _set_sentinel_mtime(repo: Path) -> None:
    """Gör mtime-ledet omöjligt att förväxla med ett commitdatum."""
    stamp = MTIME_SENTINEL.timestamp()
    os.utime(repo / PAGE, (stamp, stamp))


def _repo(tmp_path: Path, second: str, second_date: str = TOPP,
          first: str | None = None, seo=None) -> Path:
    """Ett repo med en innehållscommit 2026-10-07 och en commit ovanpå den."""
    seo = seo or _seo_module()
    repo = tmp_path / "repo"
    (repo / "about").mkdir(parents=True)
    _git(repo.parent, "init", "-q", "-b", "main", "repo")

    (repo / PAGE).write_text(
        first if first is not None
        else _page(seo, "Det riktiga innehållet.", INNEHALL_DATE),
        encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "innehållscommit", date=INNEHALL)

    (repo / PAGE).write_text(second, encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "commit ovanpå", date=second_date)
    _set_sentinel_mtime(repo)
    return repo


def test_a_date_only_commit_is_not_a_content_change(tmp_path):
    """Självreferensen stängd: toppcommiten flyttar bara datumen, så svaret
    ska vara innehållscommitens datum — inte dagens."""
    seo = _seo_module()
    repo = _repo(tmp_path,
                 _page(seo, "Det riktiga innehållet.", TOPP_DATE), seo=seo)
    seo.ROOT = repo
    assert seo.git_lastmod(PAGE) == INNEHALL_DATE


def test_a_commit_that_only_adds_a_date_FIELD_is_not_a_content_change(tmp_path):
    """Formfallet, och regressionen som kostade en granskningsrunda.

    Spärrens första version krävde att VARJE ändrad rad bar en datummarkör.
    Det håller bara när utdatat ändrar ett datum*värde* — båda raderna bär
    då markören. Ändrar utdatat *form* bär den borttagna raden ingen
    markör alls, för fältet fanns inte innan, och `all(...)` föll.

    Verkligt fall: när `/infographic-styles/` lades i `SECTION_LANDINGS`
    2026-10-13 fick dess JSON-LD en helt ny `CollectionPage`-entitet med
    `dateModified`. Den commiten räknades som en innehållsändring, och
    nästa körning hade stämplat om sidan till körningens datum — exakt den
    bugg jobb 1 tog bort, återskapad på två publicerade sidor.
    """
    seo = _seo_module()
    repo = _repo(tmp_path,
                 _page(seo, "Det riktiga innehållet.", INNEHALL_DATE),
                 first=_page(seo, "Det riktiga innehållet.", INNEHALL_DATE,
                             stamped=False),
                 seo=seo)
    seo.ROOT = repo
    assert seo.git_lastmod(PAGE) == INNEHALL_DATE


def test_a_commit_that_also_changes_content_still_counts(tmp_path):
    """Motprovet, och det som gör spärren värd något: spärren får inte
    hoppa över toppcommiten bara för att den råkar bära ett datumfält.
    Ändras innehållet i samma commit är datumet toppcommitens."""
    seo = _seo_module()
    repo = _repo(tmp_path,
                 _page(seo, "Innehållet är omskrivet.", TOPP_DATE), seo=seo)
    seo.ROOT = repo
    assert seo.git_lastmod(PAGE) == TOPP_DATE
    assert seo.git_lastmod(PAGE) != MTIME_SENTINEL_DATE, \
        "svaret kom från mtime-ledet — testet bevisar då ingenting"


def test_a_commit_that_adds_a_date_field_AND_changes_content_still_counts(tmp_path):
    """Över-hoppningsprovet för formfallet.

    Spärren sorterar bort skriptets egna rader och jämför resten. Sorterar
    den bort för mycket — t ex hela diffen så fort ett datumfält tillkommit
    — blir den grön av fel skäl och varje stämpel fryser för evigt. Här
    tillkommer `dateModified` i samma commit som stycket skrivs om, och
    svaret ska vara toppcommitens datum.
    """
    seo = _seo_module()
    repo = _repo(tmp_path,
                 _page(seo, "Innehållet är omskrivet.", TOPP_DATE),
                 first=_page(seo, "Det riktiga innehållet.", INNEHALL_DATE,
                             stamped=False),
                 seo=seo)
    seo.ROOT = repo
    assert seo.git_lastmod(PAGE) == TOPP_DATE
    assert seo.git_lastmod(PAGE) != MTIME_SENTINEL_DATE, \
        "svaret kom från mtime-ledet — testet bevisar då ingenting"


def test_a_file_outside_git_still_falls_back_to_its_mtime(tmp_path):
    """Fallbacken ska finnas kvar. En helt ny fil har ingen commit alls, och
    då är filens mtime det bästa svaret — aldrig ett undantag."""
    seo = _seo_module()
    repo = tmp_path / "tom"
    (repo / "about").mkdir(parents=True)
    _git(repo.parent, "init", "-q", "-b", "main", "tom")
    (repo / PAGE).write_text(
        _page(seo, "Aldrig committad.", INNEHALL_DATE), encoding="utf-8")
    _set_sentinel_mtime(repo)

    seo.ROOT = repo
    assert seo.git_lastmod(PAGE) == MTIME_SENTINEL_DATE


def test_running_the_script_twice_changes_nothing_the_second_time(tmp_path):
    """Hela kedjan, och den vakt som inte kan luras av att masken och
    fixturen glider i takt.

    De fyra testerna ovan matar `git_lastmod()` med konstruerade diffar.
    Går `_GENERATED_LINES` isär från vad generatorerna faktiskt skriver —
    ett nytt attribut, en radbrytning, ett nytt datumbärande fält — kan de
    fortsätta vara gröna medan skriptet stämplar om sidor i drift.
    Granskaren visade det: en mask smalnad så att den matchar en
    handskriven fixtur men inte skriptets verkliga aside gav fem gröna
    tester och buggen helt tillbaka.

    Det här testet rör ingen mask och ingen radform. Det spelar upp jobb
    3:s regression i sin helhet — en sida som BLIR section landing, körs,
    commitas, och körs igen — och kräver att andra körningen skriver noll.
    Skriver den något har skriptet läst sitt eget förra utdata som en
    innehållsändring, oavsett var i kedjan felet sitter.
    """
    seo = _seo_module()
    repo = tmp_path / "repo"
    (repo / "about").mkdir(parents=True)
    _git(repo.parent, "init", "-q", "-b", "main", "repo")

    # main() läser FAVICON_ONLY_PATHS direkt från disk.
    for rel in seo.FAVICON_ONLY_PATHS:
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('<!DOCTYPE html>\n<html lang="en">\n<head>\n'
                        "</head>\n<body></body>\n</html>\n", encoding="utf-8")

    # Utgångsläget: sidan är ÄNNU INTE section landing och bär ett
    # föräldralöst last-updated-block — precis infographic-styles 2026-10-12.
    page = repo / PAGE
    page.write_text(_page(seo, "Det riktiga innehållet.", INNEHALL_DATE,
                          stamped=False), encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "innehållscommit", date=INNEHALL)

    # Sidan blir section landing: JSON-LD:n får en entitet med
    # `dateModified` och det föräldralösa blocket adopteras.
    seo.ROOT = repo
    seo.main()
    first = page.read_text(encoding="utf-8")
    assert '"dateModified"' in first, \
        "första körningen la ingen dateModified — testet vaktar då ingenting"
    assert FORALDRALOST_DATE not in first, \
        "det föräldralösa datumet står kvar — blocket adopterades inte"
    assert INNEHALL_DATE in first, \
        "första körningen satte inte innehållscommitens datum"

    # Stämpeln commitas, precis som en människa gör. Det är den commiten
    # nästa körning annars läser som en innehållsändring.
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "stämpla sidan", date=TOPP)

    seo.main()
    assert page.read_text(encoding="utf-8") == first, (
        "andra körningen skrev om sidan — skriptet läser sitt eget utdata "
        "som en innehållsändring")
