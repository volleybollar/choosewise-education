"""Stämpeln får inte läsa sig själv som en innehållsändring.

`git_lastmod()` härleder "senast uppdaterad" ur senaste commit som rörde
filen — men att skriva stämpeln ÄR en sådan commit. Utan en spärr läser
nästa körning alltså sitt eget förra utdata och skriver dagens datum på en
sida som inte ändrats sedan i våras. Mätt i verkligheten: commit `9c6390c`
ändrade `about/index.html` på fyra rader, och alla fyra bar ett datumfält.

Vakten konstruerar det fallet i ett riktigt git-repo i en temporär katalog:
en innehållscommit, och ovanpå den en commit som bara flyttar datumen.
"""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PAGE = "about/index.html"

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


def _page(body: str, date: str | None, stamped: bool = True) -> str:
    """En sida med ett innehållsstycke och skriptets datumutdata.

    `stamped=False` ger sidan som den ser ut INNAN den blev section landing:
    JSON-LD:n saknar då både `dateModified` och sin sidentitet, precis som
    `infographic-styles/index.html` gjorde före 2026-10-13.
    """
    if not stamped:
        json_ld = '{"@context":"https://schema.org","@graph":[{"@type":"WebSite"}]}'
        aside = ""
    else:
        json_ld = ('{"@context":"https://schema.org","@graph":[{"@type":"WebSite"},'
                   f'{{"@type":"CollectionPage","dateModified":"{date}"}}]}}')
        aside = (f'<aside class="page-last-updated"><time datetime="{date}">'
                 f"{date}</time></aside>\n")
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<body>\n"
        f"<p>{body}</p>\n"
        f'<script type="application/ld+json">{json_ld}</script>\n'
        f"{aside}</body>\n</html>\n"
    )


def _repo(tmp_path: Path, second: str, second_date: str,
          first: str | None = None) -> Path:
    """Ett repo med en innehållscommit 2026-10-07 och en commit ovanpå den."""
    repo = tmp_path / "repo"
    (repo / "about").mkdir(parents=True)
    _git(repo.parent, "init", "-q", "-b", "main", "repo")

    (repo / PAGE).write_text(
        first if first is not None else _page("Det riktiga innehållet.", "2026-10-07"),
        encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "innehållscommit",
         date="2026-10-07T13:57:55+02:00")

    (repo / PAGE).write_text(second, encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "commit ovanpå", date=second_date)
    return repo


def test_a_date_only_commit_is_not_a_content_change(tmp_path):
    """Självreferensen stängd: toppcommiten flyttar bara datumen, så svaret
    ska vara innehållscommitens datum — inte dagens."""
    repo = _repo(tmp_path,
                 _page("Det riktiga innehållet.", "2026-10-13"),
                 "2026-10-13T11:49:40+02:00")
    seo = _seo_module()
    seo.ROOT = repo
    assert seo.git_lastmod(PAGE) == "2026-10-07"


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
    repo = _repo(tmp_path,
                 _page("Det riktiga innehållet.", "2026-10-07"),
                 "2026-10-13T11:49:40+02:00",
                 first=_page("Det riktiga innehållet.", None, stamped=False))
    seo = _seo_module()
    seo.ROOT = repo
    assert seo.git_lastmod(PAGE) == "2026-10-07"


def test_a_commit_that_also_changes_content_still_counts(tmp_path):
    """Motprovet, och det som gör spärren värd något: spärren får inte
    hoppa över toppcommiten bara för att den råkar bära ett datumfält.
    Ändras innehållet i samma commit är datumet toppcommitens."""
    repo = _repo(tmp_path,
                 _page("Innehållet är omskrivet.", "2026-10-13"),
                 "2026-10-13T11:49:40+02:00")
    seo = _seo_module()
    seo.ROOT = repo
    assert seo.git_lastmod(PAGE) == "2026-10-13"


def test_a_commit_that_adds_a_date_field_AND_changes_content_still_counts(tmp_path):
    """Över-hoppningsprovet för formfallet.

    Spärren sorterar bort skriptets egna rader och jämför resten. Sorterar
    den bort för mycket — t ex hela diffen så fort ett datumfält tillkommit
    — blir den grön av fel skäl och varje stämpel fryser för evigt. Här
    tillkommer `dateModified` i samma commit som stycket skrivs om, och
    svaret ska vara toppcommitens datum.
    """
    repo = _repo(tmp_path,
                 _page("Innehållet är omskrivet.", "2026-10-07"),
                 "2026-10-13T11:49:40+02:00",
                 first=_page("Det riktiga innehållet.", None, stamped=False))
    seo = _seo_module()
    seo.ROOT = repo
    assert seo.git_lastmod(PAGE) == "2026-10-13"


def test_a_file_outside_git_still_falls_back_to_its_mtime(tmp_path):
    """Fallbacken ska finnas kvar. En helt ny fil har ingen commit alls, och
    då är filens mtime det bästa svaret — aldrig ett undantag."""
    repo = tmp_path / "tom"
    (repo / "about").mkdir(parents=True)
    _git(repo.parent, "init", "-q", "-b", "main", "tom")
    page = repo / PAGE
    page.write_text(_page("Aldrig committad.", "2026-10-07"), encoding="utf-8")
    import os
    from datetime import datetime, timezone
    stamp = datetime(2026, 10, 7, 12, tzinfo=timezone.utc).timestamp()
    os.utime(page, (stamp, stamp))

    seo = _seo_module()
    seo.ROOT = repo
    assert seo.git_lastmod(PAGE) == "2026-10-07"
