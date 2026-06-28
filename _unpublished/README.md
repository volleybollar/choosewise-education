# Unpublished pages

Pages parked here are **not served** by GitHub Pages: the live site is built with
Jekyll (no `.nojekyll` file), and Jekyll ignores any folder whose name starts with
`_`. So everything under `_unpublished/` returns 404 on the live site, while the
files stay safely in the repo at their original relative paths.

Parked on 2026-06-28: all AI guides **except Claude** (English + Swedish) — the
guide pages AND their downloadable artifacts (PDFs under
`assets/pdfs/guides/`, print-A4 + quick-start HTML under `exports/`).
Claude stays published at `/guides/claude/` and `/sv/guider/claude/`, and its
PDFs/exports stay live too. The `.py` PDF build scripts in `exports/` were left
in place (build tooling, not published content).

`/ai-or-human/` and `/sv/ai-eller-manniska/` were intentionally left published.

## How to republish a page (same URL as before)

For each page, do two things:

### 1. Move the folder back to its original location

```sh
# English examples — run from the repo root:
git mv _unpublished/guides/copilot            guides/copilot
git mv _unpublished/guides/gemini-notebooklm  guides/gemini-notebooklm
git mv _unpublished/guides/apple-intelligence guides/apple-intelligence
git mv _unpublished/guides/ai-for-students    guides/ai-for-students

# Swedish:
git mv _unpublished/sv/guider/copilot            sv/guider/copilot
git mv _unpublished/sv/guider/gemini-notebooklm  sv/guider/gemini-notebooklm
git mv _unpublished/sv/guider/apple-intelligence sv/guider/apple-intelligence
git mv _unpublished/sv/guider/ai-for-elever      sv/guider/ai-for-elever
```

### 2. Add the guide's card back to the index JSON

The card was removed from the guides index so it would not show a dead link.
Add the matching object back into the array in:

- English: `guides/guides-en.json`
- Swedish: `sv/guider/guides-sv.json`

Then commit and push to `main`. The page is live again on its original URL within
a few minutes (GitHub Pages rebuild).

To republish **everything at once**, you can instead revert the single unpublish
commit: `git revert <commit>` (or ask Claude to do it).

---

## Removed index-card entries (verbatim, for copy-paste restore)

### English — add into `guides/guides-en.json`

```json
  {
    "id": "gemini-notebooklm",
    "title": "Gemini & NotebookLM for teachers and school leaders",
    "tool": "Gemini / NotebookLM",
    "status": "available",
    "url": "/guides/gemini-notebooklm/",
    "cover_image": "/assets/images/guide-covers/gemini.svg"
  },
  {
    "id": "apple-intelligence",
    "title": "Apple Intelligence for teachers and school leaders",
    "tool": "Apple Intelligence",
    "status": "available",
    "url": "/guides/apple-intelligence/",
    "cover_image": "/assets/images/guide-covers/apple.svg"
  },
  {
    "id": "copilot",
    "title": "Microsoft Copilot for teachers and school leaders",
    "tool": "Copilot",
    "status": "available",
    "url": "/guides/copilot/",
    "cover_image": "/assets/images/guide-covers/copilot.svg"
  },
  {
    "id": "ai-for-students",
    "title": "Should students use AI in class?",
    "tool": "Pedagogical decision guide",
    "status": "available",
    "url": "/guides/ai-for-students/",
    "cover_image": "/assets/images/guide-covers/ai-for-students.svg"
  }
```

### Swedish — add into `sv/guider/guides-sv.json`

```json
  {
    "id": "gemini-notebooklm",
    "title": "Gemini & NotebookLM för lärare och skolledare",
    "tool": "Gemini / NotebookLM",
    "status": "available",
    "url": "/sv/guider/gemini-notebooklm/",
    "cover_image": "/assets/images/guide-covers/gemini.svg"
  },
  {
    "id": "apple-intelligence",
    "title": "Apple Intelligence för lärare och skolledare",
    "tool": "Apple Intelligence",
    "status": "available",
    "url": "/sv/guider/apple-intelligence/",
    "cover_image": "/assets/images/guide-covers/apple.svg"
  },
  {
    "id": "copilot",
    "title": "Microsoft Copilot för lärare och skolledare",
    "tool": "Copilot",
    "status": "available",
    "url": "/sv/guider/copilot/",
    "cover_image": "/assets/images/guide-covers/copilot.svg"
  },
  {
    "id": "ai-for-elever",
    "title": "Ska eleverna använda AI på lektionstid?",
    "tool": "Pedagogisk beslutsguide",
    "status": "available",
    "url": "/sv/guider/ai-for-elever/",
    "cover_image": "/assets/images/guide-covers/ai-for-elever.svg"
  }
```

## Parked PDFs and export HTML (restore = move back to original path)

The downloadable PDFs and their print/quick-start HTML were parked too, under the
same mirrored paths. To republish a guide's downloads, move them back:

```sh
# PDFs (example: Copilot) — run from repo root:
git mv _unpublished/assets/pdfs/guides/copilot-guide-en.pdf       assets/pdfs/guides/copilot-guide-en.pdf
git mv _unpublished/assets/pdfs/guides/copilot-guide-sv.pdf       assets/pdfs/guides/copilot-guide-sv.pdf
git mv _unpublished/assets/pdfs/guides/copilot-quick-start-en.pdf assets/pdfs/guides/copilot-quick-start-en.pdf
git mv _unpublished/assets/pdfs/guides/copilot-quick-start-sv.pdf assets/pdfs/guides/copilot-quick-start-sv.pdf

# Export HTML (example: Copilot):
git mv _unpublished/exports/copilot-print-a4-en.html   exports/copilot-print-a4-en.html
git mv _unpublished/exports/copilot-print-a4-sv.html   exports/copilot-print-a4-sv.html
git mv _unpublished/exports/copilot-quick-start-en.html exports/copilot-quick-start-en.html
git mv _unpublished/exports/copilot-quick-start-sv.html exports/copilot-quick-start-sv.html
```

The other guides (gemini-notebooklm, apple-intelligence, ai-for-students /
ai-for-elever) follow the exact same pattern — see `_unpublished/assets/pdfs/guides/`
and `_unpublished/exports/` for the full list. The `.py` build scripts that
generate these PDFs are still in `exports/` if you ever need to regenerate them.
