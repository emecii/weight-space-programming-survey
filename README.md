# Neural Model Programming and Search — Survey Project

Status: scope confirmed; planning and seed literature only. This repository does not yet contain a completed survey or verified novelty claim.

Working title: **Programming and Searching Neural Models: A Survey of Activation Steering, Weight-Space Programming, Zeroth-Order Optimization, and Architecture Search**.

## Confirmed scope

On 2026-11-08 the authors confirmed coverage of space programming, zeroth-order optimization, steering, and neural architecture search (NAS), with embodied/robotics examples retained. The target is a 20–30 page survey hosted on GitHub.

“Space programming” is provisionally interpreted from the preceding discussion as weight-space programming and its connections to activation and architecture interventions. It is not asserted to be a universally established umbrella term.

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

The outline, English manuscript language, and page accounting are working assumptions. No venue, author list, license, or publication-readiness claim has been set. No third-party PDFs or private chat screenshots are redistributed. GitHub destination and visibility are pending the repository owner's choice.
