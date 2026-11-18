# WSP evidence supplement — November 17, 2026

This is a relevant-passage check, not independent reproduction or complete paper reading. Baseline: 200 records (62 relevant-passage checked, 138 abstract-screened). Additions: two checked records, numbered 201–202. Two scan candidates remain pending.

| Reference | Version and checked locations | Interpretation used in the manuscript | Remaining checks |
| --- | --- | --- | --- |
| [201] Goworek et al. | [v1 HTML](https://arxiv.org/html/2611.21449v1), §§1, 2.1.1, 3, 7 | Tested-state agreement does not prove global equivalence; spatial input cues do not establish full game understanding | Released code, independent harness validation, matched PPO reruns, broader task coverage |
| [202] Lehmann | [v1 HTML](https://arxiv.org/html/2611.16981v1), §§3.1–3.4, §5 limitations | Source access differs from learner experience; FreeArch changes the representation and is exploratory | Sandbox enforcement and cost appendix require deeper checks before numerical cost comparisons; no independent replication |

## Manuscript decisions

Added Section 4.3 with bounded claims and a separately identified synthesis. No numerical leaderboard was added. Original references keep their identifiers; supplemental metadata lives in `references-supplement.json`. No baseline record is upgraded by this check.

## Next evidence priorities

1. Inspect iWSP and medical-imaging WSP from the targeted scan, including data/label access and independent evaluation.
2. Complete Steer2Edit selection/test and construction-cost checks; its current comparison row only verifies the edit mechanism.
3. Extend the core-method matrix with consistent preparation, proposal, selection, deployment and final-test fields. Leave unreported costs unknown.
4. Compare the survey's proposed taxonomy against the closest existing surveys before making any originality claim.
