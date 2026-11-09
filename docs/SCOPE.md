# Scope and contribution brief

Date: 2026-11-08. Confirmed: the four subject areas, 20–30 pages, GitHub delivery, and inclusion of embodied work. The following synthesis and boundaries are proposed implementation choices.

## Central question

How do methods design or search modifications in activation, weight, and architecture spaces, and how do their information requirements, proposal mechanisms, and evaluation protocols determine what comparisons and conclusions are justified?

## Coverage

| Area | Core coverage | Boundary |
|---|---|---|
| Activation/representation steering | Direction, subspace, SAE features, layer/site, strength, timing, static and feedback interventions | Not every interpretability technique; include localization when it enables intervention |
| Weight-space programming | Direct construction/editing of weights, LLM-proposed edits, relevant model-editing and weight-generation foundations | Not all pretraining, fine-tuning, merging, or weight-space learning |
| Zeroth-order optimization | Function-evaluation-based optimization relevant to neural weights and intervention parameters; finite differences, query budgets, noise, dimension and subspace effects | Not an exhaustive survey of all numerical optimization; distinguish derivative-free families where definitions differ |
| NAS | Search-space design, architecture proposals, evaluation, discrete/continuous search, gradient/evolutionary/LLM-guided approaches | Not all AutoML, training infrastructure, or architecture history |
| Embodied models | Action-model steering, temporal feedback, rollout budgets, outcome and safety evaluation | Explicitly covered, not claimed comparable to language benchmarks on a shared score |

## Proposed common record

For each method record: intervention object; representation/parameterization; allowed changes; information access (weights, activations, gradients, objective values, trajectories); proposal mechanism; objective/proxy; constraints; offline preparation; online policy; evaluation budget; baseline; held-out protocol; side effects; transfer; implementation availability; evidence status.

Access and use must be separated: a white-box model can be optimized without gradients. Frozen backbone does not mean no auxiliary training. A fixed steering vector need not be the result of optimization. LLM-proposed edits can use rich internal diagnostics and need not be scalar-oracle zeroth-order optimization.

## Candidate contributions — not established novelty

1. An operational cross-domain taxonomy with explicit information access and decision timing, beyond placing four literatures next to each other.
2. A budget/evidence comparison separating search, auxiliary training, inference, and final validation costs. A tool call, full sequence generation, forward pass, rollout, and architecture-training run are different units.
3. A synthesis of when target gains coexist with regressions, and which transfer or reliability claims are actually supported.

Each candidate must be checked against existing representation-engineering, actionable-interpretability, weight-space-learning, zeroth-order, and NAS surveys. Search space / strategy / evaluation is already a NAS taxonomy and cannot itself be claimed as new.

## Falsification checks for the survey contribution

- If existing surveys already provide the same synthesis, revise the contribution rather than relabel it.
- If common metrics do not exist, compare protocols and assumptions, not raw scores.
- If the new weight-space-programming corpus is small, present it as an emerging bridge with appropriately limited conclusions.
- If the corpus cannot sustain a claimed trend, mark a hypothesis or evidence gap.

## Decisions still open

Repository owner and visibility; final title; venue/template; author list; whether 20–30 pages includes references; whether optional experiments materially improve the survey. No new experiment is mandatory at this stage.
