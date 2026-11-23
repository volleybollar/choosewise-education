"""Vakter för de sex Word-mallarna på sidan Paperwork Pack.

Mallarna byggs av exports/build-paperwork-pack-docx.py från
paperwork-pack-f388fd9f/paperwork-en.json. Texten kommer från template_text() i
scripts/build-paperwork-pack.py, samma funktion som kopieringsknapparna på sidan
använder, så sidan och filerna kan inte glida isär.
"""
import importlib.util
import json
import re
import zipfile
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

import pytest
from docx import Document

ROOT = Path(__file__).resolve().parents[2]
SLUG = "paperwork-pack-f388fd9f"
DIR = ROOT / SLUG
DATA = DIR / "paperwork-en.json"
PAGE = DIR / "index.html"
BUILDER = ROOT / "exports/build-paperwork-pack-docx.py"
PAGE_BUILDER = ROOT / "scripts/build-paperwork-pack.py"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
TBLPR_ORDER = ["tblStyle", "tblW", "tblBorders", "tblLayout", "tblLook"]

FILES = [
    "meeting-protocol.docx",
    "information-note.docx",
    "skill-pairing.docx",
    "cut-first-checklist.docx",
    "letter-template.docx",
    "messages-home.docx",
]


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_builder():
    return _load(BUILDER, "build_pp_docx")


def page_helpers():
    return _load(PAGE_BUILDER, "build_pp_page")


def templates():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    return {t["file"]: t for s in data["sections"] for t in s["templates"]}


def doc_lines(path):
    """Dokumentets text rad för rad, i dokumentets ordning, utan tomma rader.

    En tabells rubrikrad blir en rad med cellerna sammanfogade med " | ", precis som
    template_text() skriver en tabellblock. Tomma celler (rutor, tomma tabellrader) räknas inte."""
    doc = Document(str(path))
    out = []
    for child in doc.element.body.iterchildren():
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "p":
            out.append("".join(t.text or "" for t in child.iter(W + "t")))
        elif tag == "tbl":
            first = child.find(W + "tr")
            cells = ["".join(t.text or "" for t in tc.iter(W + "t")) for tc in first.iter(W + "tc")]
            if any(cells):
                out.append(" | ".join(cells))
    return [x for x in out if x.strip()]


def doc_text(path):
    return "\n".join(doc_lines(path))


class _PageCopy(HTMLParser):
    """Läser sidan med en riktig HTML-tolkare: data-copy-texten och .docx-länken för varje mall."""

    def __init__(self):
        super().__init__()
        self.copy = None
        self.pairs = {}
        self.links = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "article" and "pp-template" in (a.get("class") or "").split():
            self.copy = None
        if tag == "button" and "data-copy" in a and a["data-copy"].count("\n") > 1:
            self.copy = a["data-copy"]
        if tag == "a" and (a.get("href") or "").endswith(".docx"):
            self.links.append(a["href"])
            self.pairs[a["href"]] = self.copy


def page_copy():
    p = _PageCopy()
    p.feed(PAGE.read_text(encoding="utf-8"))
    return p


def placeholders(text):
    return Counter(re.findall(r"\[[^\]]+\]", text))


@pytest.mark.parametrize("name", FILES)
def test_files_exist(name):
    assert (DIR / name).is_file(), name


def test_every_linked_docx_exists():
    """Varje .docx som sidan länkar till finns, och varje fil har en länk."""
    links = page_copy().links
    assert sorted(links) == sorted(FILES)
    for link in links:
        assert (DIR / link).is_file(), link


@pytest.mark.parametrize("name", FILES)
def test_text_matches_json(name):
    """Varje icke-tom rad i template_text() finns i filen, i samma ordning."""
    expected = [x for x in page_helpers().template_text(templates()[name]).split("\n") if x.strip()]
    actual = doc_lines(DIR / name)
    pos = 0
    for line in expected:
        assert line in actual[pos:], (name, line)
        pos = actual.index(line, pos) + 1


@pytest.mark.parametrize("name", FILES)
def test_placeholders_identical_page_and_docx(name):
    """[Platshållarna] är samma uppsättning i kopieringstexten på sidan och i .docx-filen."""
    copy = page_copy().pairs[name]
    assert copy, name
    assert placeholders(copy) == placeholders(doc_text(DIR / name)), name


@pytest.mark.parametrize("name", FILES)
def test_headings_use_real_styles(name):
    """Titeln är "Heading 1", blockrubrikerna "Heading 2", så att Words navigeringsruta fungerar."""
    t = templates()[name]
    doc = Document(str(DIR / name))
    h1 = [p.text for p in doc.paragraphs if p.style.name == "Heading 1"]
    h2 = [p.text for p in doc.paragraphs if p.style.name == "Heading 2"]
    assert h1 == [t["title"]], name
    assert h2 == [b["heading"] for b in t["blocks"]], name
    for style in ("Heading 1", "Heading 2"):
        st = doc.styles[style]
        assert st.font.name == "Arial", (name, style)
        assert st.font.bold is True, (name, style)
        assert st.font.color.rgb is not None
    assert doc.styles["Heading 1"].font.size.pt == 20
    assert doc.styles["Heading 2"].font.size.pt == 13
    # Temateckensnittet får inte slå ut Arial i rubrikstilarna.
    for style in ("Heading 1", "Heading 2"):
        fonts = doc.styles[style].element.rPr.find(W + "rFonts")
        assert not [k for k in fonts.attrib if "theme" in k.lower()], (name, style)   # även cstheme


@pytest.mark.parametrize("name", FILES)
def test_core_properties(name):
    props = Document(str(DIR / name)).core_properties
    assert props.author == "Choosewise.education"
    assert props.last_modified_by == "Choosewise.education"
    assert props.title == templates()[name]["title"]


@pytest.mark.parametrize("name", FILES)
def test_no_stale_metadata(name):
    """Inget "python-docx" i dokumentegenskaperna, fasta datum, ingen kommentar."""
    props = Document(str(DIR / name)).core_properties
    assert props.created.date().isoformat() == "2026-11-23"
    assert props.modified.date().isoformat() == "2026-11-23"
    assert props.comments == ""
    with zipfile.ZipFile(DIR / name) as z:
        for part in ("docProps/core.xml", "docProps/app.xml"):
            if part in z.namelist():
                assert "python-docx" not in z.read(part).decode("utf-8").lower(), part


@pytest.mark.parametrize("name", FILES)
def test_body_font_is_arial(name):
    doc = Document(str(DIR / name))
    assert doc.styles["Normal"].font.name == "Arial"
    with zipfile.ZipFile(DIR / name) as z:
        assert "Calibri" not in z.read("word/document.xml").decode("utf-8")


def test_fresh_build_matches_committed_text(tmp_path):
    built = load_builder().build_docx(tmp_path)
    assert sorted(p.name for p in built) == sorted(FILES)
    for p in built:
        assert doc_text(p) == doc_text(DIR / p.name), p.name


def _body(name):
    return Document(str(DIR / name)).element.body


def _children(el):
    return [c.tag.rsplit("}", 1)[-1] for c in el]


@pytest.mark.parametrize("name", FILES)
def test_xml_children_in_schema_order(name):
    for tblpr in _body(name).iter(W + "tblPr"):
        kids = _children(tblpr)
        assert kids == [k for k in TBLPR_ORDER if k in kids], (name, kids)
        assert {"tblW", "tblBorders", "tblLayout", "tblLook"} <= set(kids), (name, kids)


@pytest.mark.parametrize("name", FILES)
def test_tables_are_full_text_width_and_fixed(name):
    """17 cm, fast layout, kolumnerna summerar till 9638 dxa i alla tabeller."""
    for tbl in _body(name).iter(W + "tbl"):
        w = tbl.find(W + "tblPr").find(W + "tblW")
        assert (w.get(W + "type"), w.get(W + "w")) == ("dxa", "9638"), name
        assert tbl.find(W + "tblPr").find(W + "tblLayout").get(W + "type") == "fixed"
        grid = [int(g.get(W + "w")) for g in tbl.find(W + "tblGrid").findall(W + "gridCol")]
        assert sum(grid) == 9638, (name, grid)
        for tr in tbl.findall(W + "tr"):
            tcw = [int(tc.find(W + "tcPr").find(W + "tcW").get(W + "w")) for tc in tr.findall(W + "tc")]
            assert tcw == grid, (name, tcw, grid)


@pytest.mark.parametrize("name", FILES)
def test_no_filler_paragraphs(name):
    """Inga stycken som bara är hårda blanksteg, och varje cell har exakt ett stycke.

    Enda undantaget är det tomma stycke på 1 pt som får stå sist efter en avslutande tabell
    (se test_document_ending_in_a_table_closes_with_a_1pt_paragraph); inga andra tomma stycken
    på toppnivå."""
    body = _body(name)
    for p in body.iter(W + "p"):
        text = "".join(t.text or "" for t in p.iter(W + "t"))
        assert not (text and not text.replace(" ", "").strip()), (name, repr(text[:20]))
    top = [c for c in body.iterchildren() if not c.tag.endswith("}sectPr")]
    for k, c in enumerate(top):
        if c.tag == W + "p" and not "".join(x.text or "" for x in c.iter(W + "t")):
            assert k == len(top) - 1 and top[k - 1].tag == W + "tbl", (name, k)
    for tc in body.iter(W + "tc"):
        assert len(tc.findall(W + "p")) == 1, name


@pytest.mark.parametrize("name", FILES)
def test_document_ending_in_a_table_closes_with_a_1pt_paragraph(name):
    """Word lägger annars till ett stycke på 11 pt efter en sista tabell, vilket kan ge en tom sida 2."""
    top = [c for c in _body(name).iterchildren() if not c.tag.endswith("}sectPr")]
    assert top[-1].tag == W + "p", f"{name}: slutar på en tabell utan avslutande stycke"
    if top[-2].tag == W + "tbl":
        last = top[-1]
        ppr = last.find(W + "pPr")
        assert ppr.find(W + "rPr").find(W + "sz").get(W + "val") == "2", name   # 1 pt
        spacing = ppr.find(W + "spacing")
        assert (spacing.get(W + "before"), spacing.get(W + "after")) == ("0", "0"), name
        assert not "".join(x.text or "" for x in last.iter(W + "t")), name


@pytest.mark.parametrize("name", FILES)
def test_fits_one_page_proxy(name):
    """Spärr, inte mätning: den riktiga sidkontrollen är visuell."""
    assert len(doc_text(DIR / name).split()) <= 450, name


@pytest.mark.parametrize("name", FILES)
def test_box_blocks_have_a_box(name):
    """Varje block med box: true följs av en ruta (en tabell med en cell och ram), och bara de."""
    t = templates()[name]
    # sectPr (sidinställningarna) ligger sist i body och hör inte till något block.
    body = [c for c in _body(name).iterchildren() if not c.tag.endswith("}sectPr")]
    # Det avslutande 1 pt-stycket efter en sista tabell hör inte till något block.
    if body[-1].tag == W + "p" and not "".join(x.text or "" for x in body[-1].iter(W + "t")):
        body = body[:-1]
    kinds = [c.tag.rsplit("}", 1)[-1] for c in body]
    for b in t["blocks"]:
        # Hitta blockets rubrik (Heading 2) och följ med fram till nästa rubrik.
        start = next(i for i, c in enumerate(body)
                     if kinds[i] == "p" and "".join(x.text or "" for x in c.iter(W + "t")) == b["heading"]
                     and c.find(W + "pPr").find(W + "pStyle").get(W + "val") == "Heading2")
        end = next((i for i in range(start + 1, len(body))
                    if kinds[i] == "p" and body[i].find(W + "pPr") is not None
                    and body[i].find(W + "pPr").find(W + "pStyle") is not None
                    and body[i].find(W + "pPr").find(W + "pStyle").get(W + "val") == "Heading2"), len(body))
        tbls = [c for c, k in zip(body[start + 1:end], kinds[start + 1:end]) if k == "tbl"]
        if "columns" in b:
            assert len(tbls) == 1 and len(tbls[0].findall(W + "tr")) == b["rows"] + 1, (name, b["heading"])
        elif b["box"]:
            assert len(tbls) == 1, (name, b["heading"])
            tbl = tbls[0]
            assert len(tbl.findall(W + "tr")) == 1 and len(tbl.findall(".//" + W + "tc")) == 1
            borders = tbl.find(W + "tblPr").find(W + "tblBorders")
            assert {"top", "left", "bottom", "right"} <= {c.tag.rsplit("}", 1)[-1] for c in borders}
            # Rutan ligger efter raderna, sist i blocket.
            assert body[start + 1:end][-1] is tbl, (name, b["heading"])
        else:
            assert not tbls, (name, b["heading"])
