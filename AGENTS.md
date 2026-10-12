# Repository memory

## What this project is
Build a single exam-ready DBMS textbook PDF from the supplied course material.

- `dbms_raw.pdf` — source. It is **plain text**, not a real PDF (109 "pages" = 109 text
  chunks). Read it with `open(..., encoding='utf-8', errors='ignore')`.
- `Hashing_in_Data_Structures_Cpp.pdf` — 165-page reference used only as the visual /
  structural design template (palette, part dividers, callouts, worked dry runs).
- `DBMS_Complete_Exam_Ready_Notes.{html,pdf}` — the deliverable.

## Build
```
python3 src/build.py
```
`src/build.py` reads `src/front.html`, the `src/content_part*.html` files in manifest
order, and `src/book.css`; it inlines the CSS and writes a self-contained HTML, then
renders the PDF with WeasyPrint (v70, SVG + `target-counter` TOC supported).

- The TOC is generated from the `TOC` list in `build.py` (level, title, anchor).
  Page numbers come from `target-counter(attr(href), page)`.
- Running headers: `@top-left` is a literal title string; `@top-right` uses
  `string(partname)`, which is never set, so it renders empty. Part dividers and the
  cover use named pages that suppress the header/footer.
- Printed page numbers run 1–180 and skip the cover plus the 8 part-divider pages;
  front matter is roman (i, ii). The TOC carries a note explaining this.

## QA recipe
```python
import pymupdf
d = pymupdf.open('DBMS_Complete_Exam_Ready_Notes.pdf')
```
- **Overflow**: no text span with `x0 < 8`, `x1 > W-8`, or `y1 > H-8`.
- **Overlaps**: pairwise span-bbox intersection > ~2.5pt on both axes (catches SVG
  label collisions that otherwise look like text drawn on text).
- **Blank/sparse**: any page under ~140 chars of text.
- **TOC**: parse the Contents pages, then confirm each title's first words appear on the
  printed page it points at.
- **Figures**: every page carrying a `Figure n.m` caption should have >3 vector drawings
  (`get_drawings()`), confirming the SVG rasterised as vectors.

## Conventions
- Diagram text labels inside an SVG must stay within its `viewBox`, and adjacent labels
  must not overlap; the collision check above catches both.
- Long reference tables use `class="qbank"` / `class="rel"` so they flow across pages
  with a repeating `thead` instead of being pushed whole onto the next page.
- Preserve Chandigarh University / UIE / CSE UNIT 2 identification from the source;
  do not invent institutional details.
- Do not fabricate chapters for topics the source only mentions (transactions, recovery,
  triggers, procedures, packages) — they are listed as coverage limits in Chapter 36.
