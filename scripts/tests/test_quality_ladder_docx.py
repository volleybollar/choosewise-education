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


def test_xml_children_in_schema_order():
    """Word kräver schemaordning: pBdr före spacing i pPr, tblBorders före tblLook i tblPr."""
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    lines = [p for p in _body_xml("quality-ladder-routine.docx").iter(ns + "pPr")
             if p.find(ns + "pBdr") is not None]
    assert lines, "inga skrivrader hittades"
    for ppr in lines:
        kids = _children(ppr)
        assert kids.index("pBdr") < kids.index("spacing"), kids
    tbls = list(_body_xml("whole-class-feedback.docx").iter(ns + "tblPr"))
    assert tbls, "inga anteckningsrutor hittades"
    for tblpr in tbls:
        kids = _children(tblpr)
        assert kids.index("tblBorders") < kids.index("tblLook"), kids


def test_notes_boxes_are_1_4_cm():
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    heights = {h.get(ns + "val") for h in _body_xml("whole-class-feedback.docx").iter(ns + "trHeight")}
    assert heights == {str(int(1.4 * 567))}
