"""Vakter för de tre Word-mallarna på sidan Quality Ladder.

Mallarna byggs av exports/build-quality-ladder-docx.py från
quality-ladder-ec1c2f8c/ladder-en.json. Texten kommer från samma hjälpfunktioner
som kopieringsknapparna på sidan, så sidan och filerna kan inte glida isär.
Spec: docs/superpowers/specs/2026-11-14-what-teachers-do-design.md, B1, B2, B5, B6.
"""
import importlib.util
import json
import re
from pathlib import Path

import pytest
from docx import Document

ROOT = Path(__file__).resolve().parents[2]
SLUG = "quality-ladder-ec1c2f8c"
DIR = ROOT / SLUG
DATA = DIR / "ladder-en.json"
PAGE = DIR / "index.html"
BUILDER = ROOT / "exports/build-quality-ladder-docx.py"

FILES = {
    "quality-ladder-routine.docx": "Quality Ladder — student sheet",
    "whole-class-feedback.docx": "Whole-class feedback",
    "feedback-policy.docx": "Feedback policy",
}


def load_builder():
    spec = importlib.util.spec_from_file_location("build_ql_docx", BUILDER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def data():
    return json.loads(DATA.read_text(encoding="utf-8"))


def doc_text(path):
    """Alla stycken och tabellceller, i den ordning de ligger i dokumentet."""
    doc = Document(str(path))
    out = []
    for child in doc.element.body.iterchildren():
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "p":
            out.append("".join(t.text or "" for t in child.iter() if t.tag.endswith("}t")))
        elif tag == "tbl":
            for t in child.iter():
                if t.tag.endswith("}tc"):
                    out.append("".join(x.text or "" for x in t.iter() if x.tag.endswith("}t")))
    return "\n".join(out)


def expected_strings(name, d):
    if name == "quality-ladder-routine.docx":
        r = d["routine"]
        return r["steps"] + r["sheet"] + [r["younger"]]
    if name == "whole-class-feedback.docx":
        wc = d["whole_class"]
        out = [wc["intro"], wc["followup"]]
        for s in wc["sections"]:
            out += [s["heading"], s["guide"]]
        return out
    p = d["policy"]
    out = [p["intro"]] + p["placeholders"]
    for pr in p["principles"]:
        out += [pr["title"], pr["text"]]
        if pr["source"]:
            out.append(pr["source"])
    return out


@pytest.mark.parametrize("name", FILES)
def test_files_exist(name):
    assert (DIR / name).is_file(), name


def test_every_linked_docx_exists():
    """Uppskjuten fråga från granskningen av uppgift 2: varje .docx som sidan länkar till finns."""
    links = re.findall(r'<a href="([^"]+\.docx)" download>', PAGE.read_text(encoding="utf-8"))
    assert sorted(links) == sorted(FILES)
    for link in links:
        assert (DIR / link).is_file(), link


@pytest.mark.parametrize("name", FILES)
def test_text_matches_json(name):
    text = doc_text(DIR / name)
    for s in expected_strings(name, data()):
        assert s in text, (name, s)


def test_every_helper_line_is_in_the_file():
    """Hjälparna är enda källan till kopieringsknapparna och filerna: varje rad de ger finns i filen."""
    h = importlib.util.spec_from_file_location("bql", ROOT / "scripts/build-quality-ladder.py")
    mod = importlib.util.module_from_spec(h)
    h.loader.exec_module(mod)
    d = data()
    texts = {"quality-ladder-routine.docx": mod.routine_text(d["routine"]),
             "whole-class-feedback.docx": mod.whole_class_text(d["whole_class"]),
             "feedback-policy.docx": mod.policy_text(d["policy"])}
    for name, helper in texts.items():
        lines = doc_text(DIR / name).split("\n")
        for line in filter(None, helper.split("\n")):
            assert line in lines, (name, line)


@pytest.mark.parametrize("name,title", FILES.items())
def test_core_properties(name, title):
    props = Document(str(DIR / name)).core_properties
    assert props.author == "Choosewise.education"
    assert props.title == title


@pytest.mark.parametrize("name", FILES)
def test_no_stale_metadata(name):
    """Inget "python-docx" i dokumentegenskaperna, fasta datum, ingen kommentar."""
    import zipfile
    props = Document(str(DIR / name)).core_properties
    assert props.created.date().isoformat() == "2026-11-14"
    assert props.modified.date().isoformat() == "2026-11-14"
    assert props.comments == ""
    with zipfile.ZipFile(DIR / name) as z:
        for part in ("docProps/core.xml", "docProps/app.xml"):
            if part in z.namelist():
                assert "python-docx" not in z.read(part).decode("utf-8").lower(), part


@pytest.mark.parametrize("name", FILES)
def test_body_font_is_arial(name):
    doc = Document(str(DIR / name))
    assert doc.styles["Normal"].font.name == "Arial"
    with __import__("zipfile").ZipFile(DIR / name) as z:
        assert "Calibri" not in z.read("word/document.xml").decode("utf-8")


def test_fresh_build_matches_committed_text(tmp_path):
    built = load_builder().build_docx(tmp_path)
    assert sorted(p.name for p in built) == sorted(FILES)
    for p in built:
        assert doc_text(p) == doc_text(DIR / p.name), p.name


@pytest.mark.parametrize("name", FILES)
def test_fits_one_page_proxy(name):
    """Spärr, inte mätning: den riktiga sidkontrollen är visuell (uppgift 7)."""
    assert len(doc_text(DIR / name).split()) <= 450, name


def test_no_ai_student_data():
    text = doc_text(DIR / "whole-class-feedback.docx")
    assert "names on paper or in this document, never in an AI tool" in text


def _body_xml(name):
    return Document(str(DIR / name)).element.body


def _children(el):
    return [c.tag.rsplit("}", 1)[-1] for c in el]


W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
TBLPR_ORDER = ["tblStyle", "tblW", "tblBorders", "tblLayout", "tblLook"]


def test_xml_children_in_schema_order():
    """Word kräver schemaordning i tblPr: tblW, tblBorders, tblLayout, tblLook."""
    for name in ("quality-ladder-routine.docx", "whole-class-feedback.docx"):
        tbls = list(_body_xml(name).iter(W + "tblPr"))
        assert tbls, name
        for tblpr in tbls:
            kids = _children(tblpr)
            assert kids == [k for k in TBLPR_ORDER if k in kids], (name, kids)
            assert {"tblW", "tblBorders", "tblLayout", "tblLook"} <= set(kids), (name, kids)


def test_tables_are_full_text_width_and_fixed():
    """Utan uttrycklig bredd ritar Quick Look en smal ruta: 17 cm, fast layout, i alla tabeller."""
    for name in ("quality-ladder-routine.docx", "whole-class-feedback.docx"):
        body = _body_xml(name)
        tbls = list(body.iter(W + "tbl"))
        assert tbls, name
        for tbl in tbls:
            w = tbl.find(W + "tblPr").find(W + "tblW")
            assert (w.get(W + "type"), w.get(W + "w")) == ("dxa", "9638"), name
            assert tbl.find(W + "tblPr").find(W + "tblLayout").get(W + "type") == "fixed"
            assert tbl.find(W + "tblGrid").find(W + "gridCol").get(W + "w") == "9638"
            tcw = tbl.find(".//" + W + "tcW")
            assert (tcw.get(W + "type"), tcw.get(W + "w")) == ("dxa", "9638"), name


def test_routine_sheet_has_a_box_under_each_prompt():
    heights = [int(h.get(W + "val")) for h in _body_xml("quality-ladder-routine.docx").iter(W + "trHeight")]
    assert heights == [int(2 * 567), int(2 * 567), int(7 * 567)]


def test_notes_boxes_are_1_4_cm():
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    heights = {h.get(ns + "val") for h in _body_xml("whole-class-feedback.docx").iter(ns + "trHeight")}
    assert heights == {str(int(1.4 * 567))}


@pytest.mark.parametrize("name", FILES)
def test_no_filler_paragraphs(name):
    """Inga stycken som bara består av hårda blanksteg, och varje ruta har exakt ett stycke."""
    body = _body_xml(name)
    for p in body.iter(W + "p"):
        text = "".join(t.text or "" for t in p.iter(W + "t"))
        assert not (text and not text.replace("\u00a0", "").strip()), (name, repr(text[:20]))
    for tc in body.iter(W + "tc"):
        assert len(tc.findall(W + "p")) == 1, name
