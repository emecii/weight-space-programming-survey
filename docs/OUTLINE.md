# Proposed outline and page budget

**Delivery update (2026-11-09):** the current user-requested artifact is a [one-page Chinese survey](../manuscript/survey-one-page-zh.pdf). The 28-page outline below is retained as the earlier long-form expansion plan, rather than the page target for this delivery.

## Scope clarification (2026-11-08)

Use **weight-space programming** as the user-specified term. Primary anchors: Exploring Weight-Space Programming (https://arxiv.org/abs/2611.09382), Sparks of Weight-Space Programming (https://rikiyat.github.io/blog/weight-space-programming/), and **SteerAct** (https://arxiv.org/abs/2610.25632). SteerScope is supplementary evaluation literature. Zeroth-order optimization, NAS, embodied coverage, 20–30 pages, and GitHub remain confirmed. The cross-space taxonomy below is an analytical proposal, not a new field name or an author-approved final title.

Planning target: **28 total pages**, provisionally in a two-column academic format, including references and embedded figures/tables. Actual length must be checked after typesetting. Language assumption: English manuscript, Chinese planning notes. This is an outline, not a manuscript or a venue-compliant submission.

| Section | Pages | Purpose / required evidence |
|---|---:|---|
| 1. Introduction and review methodology | 2 | Motivation, scope, inclusion rules, survey comparison, reproducible search record |
| 2. Spaces, information access, and intervention design | 3 | Definitions and mapping; distinguish intervention object from optimizer; foundational surveys |
| 3. Zeroth-order and other proposal/search mechanisms | 3 | Function-value oracles, gradient estimates, query/dimension issues; distinguish adjacent search approaches |
| 4. Activation and representation steering | 4 | Statistical/learned directions, SAE features, strength/site/time, static versus adaptive policies; SteerAct as the user-specified anchor and SteerScope as supporting evaluation evidence |
| 5. Weight-space programming and editing | 3 | Sparks and Exploring WSP as anchors; direct edits/construction, LLM proposals, diagnostic feedback, reliability and cross-task transfer |
| 6. Neural architecture search | 3 | Architecture spaces, discrete and differentiable strategies, evolutionary/LLM proposals, evaluation cost and proxies |
| 7. Embodied interventions and temporal feedback | 2 | SteerAct plus further verified action-model papers; trajectory feedback, latency, success/safety, distribution shift |
| 8. Cross-domain evidence and open problems | 3 | Costs, side effects, robustness, reproducibility; supported connections and unresolved comparisons |
| 9. Conclusion | 0.5 | Only findings established by the literature synthesis |
| References | 4.5 | Verified bibliography |
| **Total** | **28** | **23.5 body + 4.5 references** |

## Planned figures and tables

- A map of activation, weight, and architecture intervention spaces (conceptual, no implication of universal equivalence).
- A method-by-information/proposal/timing matrix.
- A comparison against existing surveys, with page/section evidence for each coverage judgement.
- A budget and evaluation-protocol table separating offline preparation, search and deployment.
- An evidence-gap map; numerical trade-off plots only when comparable data are available.

## Evidence assignment

The seed CSV assigns initial sources to branches. Detailed source-to-claim mapping remains pending. All four technical branches need original papers beyond surveys. The embodied section needs sources beyond SteerAct. No section is currently ready for final prose.

## Writing order

Build the survey-comparison and method matrices first. Draft the taxonomy alongside classification trials, then technical sections, cross-domain synthesis, and finally introduction/abstract/conclusion. Adjust page allocation based on verified evidence rather than equal coverage quotas.
