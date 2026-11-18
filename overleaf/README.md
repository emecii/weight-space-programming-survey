# Weight-Space Programming Survey — 中文整合稿 v2

Overleaf: select XeLaTeX, main document `main.tex`, then Recompile.

Edit `body.tex` for manuscript text; `references.tex` preserves existing [1]–[200] numbering. `references-200.bib` is supplied for future venue conversion; the current build uses references.tex, not BibTeX.

Source of truth before collaborative editing: manuscript/survey-zh-200.md and literature/references-200.json in GitHub. Run `python3 manuscript/export_overleaf.py` to regenerate this folder. Once editing on Overleaf starts, export and reconcile those edits before regenerating; do not overwrite collaborators' changes.

Author order, affiliations, funding, conflict-of-interest and author contribution declarations require team input. This is a narrative review with no new experiments. The baseline search date remains 2026-11-09. AI assistance was used for drafting, source cross-checking and formatting; authors must review the final text and venue-specific disclosure requirements.

Overleaf 项目：https://www.overleaf.com/project/6afd33eb5393573dd5c55652

Current local XeLaTeX-compatible PDF: 23 pages (14 body + 9 references). The alternative ReportLab PDF has 22 pages (17 body + 5 references); both derive from the same Markdown and reference metadata.
