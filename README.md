# Weight-Space Programming Survey

**Current manuscript: _Weight-Space Programming: Methods, Costs, and Limitations_ — an English narrative survey of 200 papers and preprints.** The English edition has 30 pages (20 pages of text, tables, figures, and transparency statements; 10 pages of references).

- [Open the Overleaf project](https://www.overleaf.com/project/6afd33eb5393573dd5c55652)
- [Read the English PDF](overleaf/main.pdf)
- [Edit the English Markdown](manuscript/survey-en.md)
- [LaTeX sources and build instructions](overleaf/README.md)
- [Download the Overleaf source package](overleaf/weight-space-programming-survey.zip)

## Scope and contribution

The survey starts from **weight-space programming** and connects weight-space learning, knowledge editing and merging, zeroth-order optimization, representation steering, neural architecture search, and embodied control. It separates intervention targets from proposal mechanisms, information access, and validation protocols.

The synthesis distinguishes evaluated candidates from retained artifacts, identifies conditions for cross-space conversion, and accounts separately for preparation, search, deployment, and independent evaluation. Additive resource use, peak memory, and end-to-end latency use different aggregation rules. Cross-domain coverage alone is not presented as a novelty claim.

## Corpus and evidence

The November 9 baseline contains 200 selected papers from 590 unique candidates. Relevant full-text passages were checked for 62 papers; 138 were screened through metadata and abstracts. These are bounded reading scopes, not claims of complete reading or independent replication. A supplementary 12-claim audit is recorded separately. Four candidates from the November 17 targeted scan await full-text assessment and are not included in the baseline count.

- [Corpus and per-paper notes](literature/corpus-200.csv)
- [Bibliography](literature/references-200.bib) and [structured metadata](literature/references-200.json)
- [Search log](literature/search-log.csv), [screening log](literature/screening-log.csv), and [evidence ledger](literature/evidence-ledger.csv)
- [Core-method comparison](literature/core-method-comparison.csv)
- [Prior-survey comparison and supplementary audit](docs/revisions/2026-11-09/README.md)
- [Incremental candidate scan](literature/update-scan-2026-11-17.md)
- [Remaining work](docs/PROGRESS.md)

The supporting research notes retain their original language. The primary manuscript, tables, figures, captions, and Overleaf compilation are English. Earlier Chinese manuscripts remain as historical working artifacts.

## Rebuild and collaborate

Run `python3 manuscript/export_overleaf.py` to export the English Markdown and bibliography metadata to `overleaf/`. Compile `overleaf/main.tex` with XeLaTeX or run `tectonic -k --keep-logs overleaf/main.tex`.

After collaborators begin editing on Overleaf, download and reconcile their changes before regenerating files. GitHub and Overleaf are not automatically synchronized. The rendered PDF should be reviewed after each substantive change; citation and layout checks do not constitute full scientific review.

## Starting sources

- [Exploring Weight-Space Programming](https://arxiv.org/abs/2611.09382v1), reference [1].
- [SteerAct](https://arxiv.org/abs/2610.25632v1), reference [176]; SteerScope supplies complementary evaluation evidence.
- [Sparks of Weight-Space Programming](https://rikiyat.github.io/blog/weight-space-programming/), background blog, outside the 200-paper corpus.

No new experiments are reported. Author order, affiliations, venue, declarations, and license remain to be supplied by the team. The repository distributes project text, code, original diagrams, metadata, and source links, not third-party paper PDFs or fonts.
