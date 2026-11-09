# Weight-Space Programming — Survey Project

Status: scope confirmed; planning and seed literature only. This repository does not yet contain a completed survey or verified novelty claim.

Project name: **weight-space-programming-survey**. Final manuscript title remains undecided; coverage includes weight-space programming, zeroth-order optimization, steering, and NAS.

## Confirmed scope

On 2026-11-08 the authors confirmed coverage of weight-space programming, zeroth-order optimization, steering, and neural architecture search (NAS), with embodied/robotics examples retained. The target is a 20–30 page survey hosted on GitHub.

The user clarified that the intended term is **weight-space programming**, not the assistant-created umbrella “neural-model-programming”. The prior name was a local project label and is withdrawn.

## User-specified starting works

- [Exploring Weight-Space Programming: Capabilities, Generalization, and Limitations](https://arxiv.org/abs/2611.09382) — the paper in the supplied screenshot.
- [Sparks of Weight-Space Programming](https://rikiyat.github.io/blog/weight-space-programming/) — the original author blog discussed earlier.
- [SteerAct: Unlocking Action Models through Few-Shot Temporal Steering](https://arxiv.org/abs/2610.25632) — the intended steering anchor, with Li Fei-Fei among the authors.

SteerScope remains supporting evaluation literature, not a replacement for SteerAct. The previously confirmed zeroth-order and NAS coverage and 20–30 page/GitHub targets remain in scope.

## Proposed organizing principle

Distinguish **intervention/search space** (activations, weights, architecture), **proposal/search mechanism** (statistical construction, gradient methods, zeroth-order queries, evolutionary or other search, LLM-generated proposals), **available information**, and **evaluation protocol**. These axes overlap; a method can receive multiple labels. Steering is not synonymous with zeroth-order optimization, and NAS is not necessarily gradient-free.

Language and embodied models are application domains, not additional optimization algorithms. Prompting and ordinary fine-tuning serve as boundary comparisons and baselines rather than exhaustive survey topics.

## Project files

- [Scope, boundaries, and candidate contributions](docs/SCOPE.md)
- [Proposed 28-page outline](docs/OUTLINE.md)
- [Literature protocol and execution plan](docs/PLAN.md)
- [Seed literature and verification status](literature/seed-papers.csv)

## Deliverables

1. A 20–30 page manuscript with traceable references and explicit limitations.
2. A curated literature matrix and a comparison against existing surveys.
3. Editable figures/tables and, when available, manuscript sources and a compiled PDF.
4. Versioned GitHub releases; include reproduction scripts only if experiments are actually conducted.

## Current limits

The outline, English manuscript language, and page accounting are working assumptions. No venue, author list, license, or publication-readiness claim has been set. No third-party PDFs or private chat screenshots are redistributed. The user authorized a public repository at https://github.com/emecii/weight-space-programming-survey on 2026-11-08.
