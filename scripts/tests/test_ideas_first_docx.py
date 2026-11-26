"""Vakter för Word-bladet på sidan Ideas first (team-idea-sheet.docx).

Filen byggs av exports/build-ideas-first-docx.py från team.sheet i
ideas-first-778ba230/ideas-en.json. Texten kommer från sheet_text() i
scripts/build-ideas-first.py, samma funktion som sidan använder.
"""
import importlib.util
import json
import re
import zipfile
from html.parser import HTMLParser
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parents[2]
SLUG = "ideas-first-778ba230"
DIR = ROOT / SLUG
NAME = "team-idea-sheet.docx"
FILE = DIR / NAME
DATA = DIR / "ideas-en.json"
PAGE = DIR / "index.html"
BUILDER = ROOT / "exports/build-ideas-first-docx.py"
PAGE_BUILDER = ROOT / "scripts/build-ideas-first.py"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
TBLPR_ORDER = ["tblStyle", "tblW", "tblBorders", "tblLayout", "tblLook"]
BRITISH = re.compile(r"\b(behaviour\w*|colour\w*|programme|practis\w*|organis\w*|recognis\w*"
                     r"|labelled|centre|pupils?|maths)\b", re.IGNORECASE)
QUOTED = re.compile(r'"[^"]*"|“[^”]*”')


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_builder():
    return _load(BUILDER, "build_if_docx")


def sheet():
    return json.loads(DATA.read_text(encoding="utf-8"))["team"]["sheet"]


def expected_text():
    return _load(PAGE_BUILDER, "build_if_page").sheet_text(sheet())


def _cells(tr):
    return ["".join(t.text or "" for t in tc.iter(W + "t")) for tc in tr.findall(W + "tc")]


def _p_text(p):
    return "".join(t.text or "" for t in p.iter(W + "t"))


def doc_lines(path):
    """Brödtexten i dokumentordning, utan tomma rader: stycken, och för varje tabell
    cellerna i första raden som egna rader."""
    out = []
    for child in Document(str(path)).element.body.iterchildren():
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "p":
            out.append(_p_text(child))
        elif tag == "tbl":
            out.extend(_cells(child.find(W + "tr")))
    return [x for x in out if x.strip()]


def doc_text(path):
    return "\n".join(doc_lines(path))


def _body(path=FILE):
    return Document(str(path)).element.body


def _tables(path=FILE):
    return list(_body(path).iter(W + "tbl"))


class _Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        href = dict(attrs).get("href") or ""
        if tag == "a" and href.endswith(".docx"):
            self.links.append(href)


def test_file_exists():
    assert FILE.is_file()


def test_every_linked_docx_exists():
    p = _Links()
    p.feed(PAGE.read_text(encoding="utf-8"))
    assert p.links == [NAME]
    assert (DIR / NAME).is_file()


def test_text_matches_json():
    expected = [x for x in expected_text().split("\n") if x.strip()]
    actual = doc_lines(FILE)
    assert actual == expected


def test_headings_use_real_styles():
    doc = Document(str(FILE))
    s = sheet()
    h1 = [p.text for p in doc.paragraphs if p.style.name == "Heading 1"]
    h2 = [p.text for p in doc.paragraphs if p.style.name == "Heading 2"]
    assert h1 == [s["title"]]
    assert h2 == [s["routine_heading"], s["before_ai"]["heading"],
                  s["from_ai"]["heading"], s["chose"]["heading"]]
    for style in ("Heading 1", "Heading 2"):
        st = doc.styles[style]
        assert st.font.name == "Arial" and st.font.bold is True, style
        fonts = st.element.rPr.find(W + "rFonts")
        assert not [k for k in fonts.attrib if "theme" in k.lower()], style
    assert doc.styles["Heading 1"].font.size.pt == 20
    assert doc.styles["Heading 2"].font.size.pt == 13


def test_core_properties():
    props = Document(str(FILE)).core_properties
    assert props.author == "Choosewise.education"
    assert props.last_modified_by == "Choosewise.education"
    assert props.title == "Ideas first: team sheet"


def test_no_stale_metadata():
    props = Document(str(FILE)).core_properties
    assert props.created.date().isoformat() == "2026-11-26"
    assert props.modified.date().isoformat() == "2026-11-26"
    assert props.comments == ""
    with zipfile.ZipFile(FILE) as z:
        for part in ("docProps/core.xml", "docProps/app.xml"):
            if part in z.namelist():
                assert "python-docx" not in z.read(part).decode("utf-8").lower(), part


def test_body_font_is_arial():
    doc = Document(str(FILE))
    assert doc.styles["Normal"].font.name == "Arial"
    with zipfile.ZipFile(FILE) as z:
        assert "Calibri" not in z.read("word/document.xml").decode("utf-8")


def test_fresh_build_matches_committed_text(tmp_path):
    built = load_builder().build_docx(tmp_path)
    assert [p.name for p in built] == [NAME]
    assert doc_text(built[0]) == doc_text(FILE)


def test_xml_children_in_schema_order():
    for tblpr in _body().iter(W + "tblPr"):
        kids = [c.tag.rsplit("}", 1)[-1] for c in tblpr]
        assert kids == [k for k in TBLPR_ORDER if k in kids], kids
        assert {"tblW", "tblBorders", "tblLayout", "tblLook"} <= set(kids), kids


def test_tables_are_full_text_width_and_fixed():
    for tbl in _tables():
        w = tbl.find(W + "tblPr").find(W + "tblW")
        assert (w.get(W + "type"), w.get(W + "w")) == ("dxa", "9638")
        assert tbl.find(W + "tblPr").find(W + "tblLayout").get(W + "type") == "fixed"
        grid = [int(g.get(W + "w")) for g in tbl.find(W + "tblGrid").findall(W + "gridCol")]
        assert sum(grid) == 9638, grid
        for tr in tbl.findall(W + "tr"):
            tcw = [int(tc.find(W + "tcPr").find(W + "tcW").get(W + "w")) for tc in tr.findall(W + "tc")]
            assert tcw == grid, (tcw, grid)


def test_no_filler_paragraphs():
    body = _body()
    for p in body.iter(W + "p"):
        text = _p_text(p)
        assert not (text and not text.replace(" ", "").strip()), repr(text[:20])
    top = [c for c in body.iterchildren() if not c.tag.endswith("}sectPr")]
    for k, c in enumerate(top):
        if c.tag == W + "p" and not _p_text(c):
            assert k == len(top) - 1 and top[k - 1].tag == W + "tbl", k
    for tc in body.iter(W + "tc"):
        assert len(tc.findall(W + "p")) == 1
    assert top[-1].tag == W + "p"


def test_fits_one_page_proxy():
    assert len(doc_text(FILE).split()) <= 450


def test_header_row():
    first = _tables()[0]
    assert len(first.findall(W + "tr")) == 1
    cells = _cells(first.find(W + "tr"))
    assert [c.startswith(s) for c, s in zip(cells, ["Subject", "Grade", "Goal", "Date"])] == [True] * 4
    assert len(cells) == 4


def _table_with_header(header):
    found = [t for t in _tables() if _cells(t.find(W + "tr")) == header]
    assert len(found) == 1, header
    return found[0]


def _empty_rows(tbl):
    rows = tbl.findall(W + "tr")[1:]
    assert all(not any(_cells(tr)) for tr in rows)
    return len(rows)


def test_before_ai_table():
    s = sheet()["before_ai"]
    assert _empty_rows(_table_with_header(s["columns"])) == s["rows"]


def test_chose_table():
    s = sheet()["chose"]
    assert _empty_rows(_table_with_header(s["columns"])) == s["rows"]


def test_note_on_the_sheet():
    assert "Only the ideas go into AI, never the names on this sheet." in doc_text(FILE)


def test_american_spelling_in_docx():
    assert BRITISH.findall(QUOTED.sub("", doc_text(FILE))) == []


def test_routine_numbers_match_text_size():
    # Listnumret tar storlek från styckets egen teckenmarkering: den ska vara lika stor som texten.
    items = [p for p in _body().iter(W + "p")
             if p.find(W + "pPr") is not None and p.find(W + "pPr").find(W + "pStyle") is not None
             and p.find(W + "pPr").find(W + "pStyle").get(W + "val") == "ListNumber"]
    assert items
    for p in items:
        mark = p.find(W + "pPr").find(W + "rPr")
        assert mark is not None and mark.find(W + "sz") is not None
        runs = {r.find(W + "rPr").find(W + "sz").get(W + "val") for r in p.findall(W + "r")}
        assert runs == {mark.find(W + "sz").get(W + "val")}
