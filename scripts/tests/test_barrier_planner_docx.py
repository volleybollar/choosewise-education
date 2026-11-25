"""Vakter för de två Word-filerna på sidan Barrier Planner.

Filerna byggs av exports/build-barrier-planner-docx.py från
barrier-planner-1c25533d/planner-en.json. Texten kommer från record_text() och
unsupported_text() i scripts/build-barrier-planner.py, samma funktioner som
kopieringsknapparna på sidan använder, så sidan och filerna kan inte glida isär.
"""
import importlib.util
import json
import re
import zipfile
from html.parser import HTMLParser
from pathlib import Path

import pytest
from docx import Document

ROOT = Path(__file__).resolve().parents[2]
SLUG = "barrier-planner-1c25533d"
DIR = ROOT / SLUG
DATA = DIR / "planner-en.json"
PAGE = DIR / "index.html"
BUILDER = ROOT / "exports/build-barrier-planner-docx.py"
PAGE_BUILDER = ROOT / "scripts/build-barrier-planner.py"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
TBLPR_ORDER = ["tblStyle", "tblW", "tblBorders", "tblLayout", "tblLook"]
FILES = ["needs-and-measures.docx", "popular-but-unsupported.docx"]
TITLES = {"needs-and-measures.docx": "Needs and measures",
          "popular-but-unsupported.docx": "Popular but unsupported"}
BRITISH = re.compile(r"\b(behaviour\w*|colour\w*|programme|practis\w*|organis\w*|recognis\w*"
                     r"|labelled|centre|pupils?|maths)\b", re.IGNORECASE)
QUOTED = re.compile(r'"[^"]*"|“[^”]*”')


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_builder():
    return _load(BUILDER, "build_bp_docx")


def page_helpers():
    return _load(PAGE_BUILDER, "build_bp_page")


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def expected_text(name):
    mod = page_helpers()
    d = data()
    if name == "needs-and-measures.docx":
        return mod.record_text(d["record"])
    return mod.unsupported_text(d["unsupported"])


def doc_lines(path):
    """Dokumentets text rad för rad, utan tomma rader. En tabells första rad blir en rad med
    cellerna sammanfogade med " | " (som record_text() gör), utom när varje cell slutar på ":"
    (formulärhuvudet): då blir varje cell en egen rad."""
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
                if all(c.endswith(":") for c in cells):
                    out.extend(cells)
                else:
                    out.append(" | ".join(cells))
    return [x for x in out if x.strip()]


def doc_text(path):
    return "\n".join(doc_lines(path))


class _Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        href = dict(attrs).get("href") or ""
        if tag == "a" and href.endswith(".docx"):
            self.links.append(href)


def _body(name):
    return Document(str(DIR / name)).element.body


def _children(el):
    return [c.tag.rsplit("}", 1)[-1] for c in el]


def _cell_text(tc):
    return "".join(t.text or "" for t in tc.iter(W + "t"))


def _p_text(p):
    return "".join(t.text or "" for t in p.iter(W + "t"))


@pytest.mark.parametrize("name", FILES)
def test_files_exist(name):
    assert (DIR / name).is_file(), name


def test_every_linked_docx_exists():
    p = _Links()
    p.feed(PAGE.read_text(encoding="utf-8"))
    assert sorted(p.links) == sorted(FILES)
    for link in p.links:
        assert (DIR / link).is_file(), link


@pytest.mark.parametrize("name", FILES)
def test_text_matches_json(name):
    """Varje icke-tom rad i sidans kopieringstext finns i filen, i samma ordning."""
    expected = [x for x in expected_text(name).split("\n") if x.strip()]
    actual = doc_lines(DIR / name)
    pos = 0
    for line in expected:
        assert line in actual[pos:], (name, line)
        pos = actual.index(line, pos) + 1


@pytest.mark.parametrize("name", FILES)
def test_headings_use_real_styles(name):
    doc = Document(str(DIR / name))
    d = data()
    h1 = [p.text for p in doc.paragraphs if p.style.name == "Heading 1"]
    h2 = [p.text for p in doc.paragraphs if p.style.name == "Heading 2"]
    assert h1 == [TITLES[name]], name
    if name == "needs-and-measures.docx":
        mod = page_helpers()
        want = [b["heading"] for b in d["record"]["blocks"]] + [mod.REVIEW_QUESTIONS_TITLE, mod.EEF_TITLE]
    else:
        want = [i["title"] for i in d["unsupported"]["items"]]
    assert h2 == want, name
    for style in ("Heading 1", "Heading 2"):
        st = doc.styles[style]
        assert st.font.name == "Arial" and st.font.bold is True, (name, style)
        fonts = st.element.rPr.find(W + "rFonts")
        assert not [k for k in fonts.attrib if "theme" in k.lower()], (name, style)
    assert doc.styles["Heading 1"].font.size.pt == 20
    assert doc.styles["Heading 2"].font.size.pt == 13


@pytest.mark.parametrize("name", FILES)
def test_core_properties(name):
    props = Document(str(DIR / name)).core_properties
    assert props.author == "Choosewise.education"
    assert props.last_modified_by == "Choosewise.education"
    assert props.title == TITLES[name]


@pytest.mark.parametrize("name", FILES)
def test_no_stale_metadata(name):
    props = Document(str(DIR / name)).core_properties
    assert props.created.date().isoformat() == "2026-11-25"
    assert props.modified.date().isoformat() == "2026-11-25"
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


@pytest.mark.parametrize("name", FILES)
def test_xml_children_in_schema_order(name):
    for tblpr in _body(name).iter(W + "tblPr"):
        kids = _children(tblpr)
        assert kids == [k for k in TBLPR_ORDER if k in kids], (name, kids)
        assert {"tblW", "tblBorders", "tblLayout", "tblLook"} <= set(kids), (name, kids)


@pytest.mark.parametrize("name", FILES)
def test_tables_are_full_text_width_and_fixed(name):
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
    """Inga stycken av bara blanksteg, ett stycke per cell, och inget tomt stycke på toppnivå
    utom det på 1 pt sist efter en avslutande tabell."""
    body = _body(name)
    for p in body.iter(W + "p"):
        text = _p_text(p)
        assert not (text and not text.replace(" ", "").strip()), (name, repr(text[:20]))
    top = [c for c in body.iterchildren() if not c.tag.endswith("}sectPr")]
    for k, c in enumerate(top):
        if c.tag == W + "p" and not _p_text(c):
            assert k == len(top) - 1 and top[k - 1].tag == W + "tbl", (name, k)
    for tc in body.iter(W + "tc"):
        assert len(tc.findall(W + "p")) == 1, name
    assert top[-1].tag == W + "p", name


@pytest.mark.parametrize("name", FILES)
def test_fits_one_page_proxy(name):
    assert len(doc_text(DIR / name).split()) <= 450, name


def test_warning_directly_above_form():
    body = [c for c in _body("needs-and-measures.docx").iterchildren()]
    idx = next(i for i, c in enumerate(body)
               if c.tag == W + "p" and _p_text(c).startswith("This form never goes through AI."))
    nxt = body[idx + 1]
    assert nxt.tag == W + "tbl"
    cells = [_cell_text(tc) for tc in nxt.find(W + "tr").findall(W + "tc")]
    assert len(nxt.findall(W + "tr")) == 1
    assert [c.startswith(s) for c, s in zip(cells, ["Student or class", "Date", "Who took part"])] == [True] * 3
    # Första meningen är fetstil, resten inte.
    runs = body[idx].findall(W + "r")
    assert runs[0].find(W + "rPr").find(W + "b") is not None


def test_measures_table():
    d = data()["record"]
    tables = [t for t in _body("needs-and-measures.docx").iter(W + "tbl")]
    meas = [t for t in tables
            if [_cell_text(tc) for tc in t.find(W + "tr").findall(W + "tc")] == d["measure_columns"]]
    assert len(meas) == 1
    rows = meas[0].findall(W + "tr")
    assert len(rows) == 4
    assert all(not _cell_text(tc) for tr in rows[1:] for tc in tr.findall(W + "tc"))
    out = [t for t in tables
           if [_cell_text(tc) for tc in t.find(W + "tr").findall(W + "tc")] == d["outcomes"]]
    assert len(out) == 1
    assert len(out[0].findall(W + "tr")) >= 2


def test_no_diagnosis_field():
    body = _body("needs-and-measures.docx")
    for tc in body.iter(W + "tc"):
        assert not re.search(r"diagnos|medical|health", _cell_text(tc), re.I), _cell_text(tc)
    doc = Document(str(DIR / "needs-and-measures.docx"))
    for p in doc.paragraphs:
        if p.style.name == "Heading 2":
            assert not re.search(r"diagnos|medical|health", p.text, re.I), p.text


@pytest.mark.parametrize("name", FILES)
def test_american_spelling_in_docx(name):
    assert BRITISH.findall(QUOTED.sub("", doc_text(DIR / name))) == [], name
