# Weight-Space Programming: Methods, Costs, and Limitations

A Cross-Domain Narrative Survey

### Abstract

Weight-space programming (WSP) asks whether a language model can inspect, construct, or edit another neural network's parameters and submit executable modifications for external evaluation. This question connects model adaptation to research on weight-space learning, knowledge editing, zeroth-order optimization, activation steering, neural architecture search, and embodied control. We organize a baseline corpus of 200 papers and preprints, with two subsequently checked additions, along four axes: intervention target, proposal mechanism, information access, and validation protocol. The resulting comparison asks what information each intervention requires, where its costs occur, and whether reported improvements describe a tested candidate or the artifact ultimately retained. We examine the conditions under which insights transfer between intervention spaces and identify cases where apparent equivalences fail. A stage-specific cost ledger distinguishes preparation, search, deployment, and independent evaluation while separating additive resource use from peak memory and end-to-end latency. Across these settings, local behavioral changes do not establish general weight understanding, consistent knowledge revision, or reliable long-horizon control. The baseline corpus includes 62 papers checked at relevant full-text passages and 138 screened through metadata and abstracts; supplementary claim checks remain separately documented. This narrative survey provides a comparison framework and an evidence-grounded research agenda, rather than new experiments, an exhaustive systematic review, or a claim of priority over existing taxonomies.

## 1 Introduction

Fine-tuning changes parameters through gradients, prompting changes inputs, representation steering modifies hidden states, and neural architecture search (NAS) changes computational structure. WSP makes parameters or editing programs objects that a language model can manipulate, bringing structural priors, program generation, and feedback-driven search into model modification.[1,2,4,6,10,11] It denotes a particular research setting rather than every form of neural model adaptation. Zeroth-order optimization (ZO) does not require a language model, steering can involve gradients, and NAS encompasses reinforcement learning, evolutionary search, and differentiable optimization.[51,86,131]

This survey asks: **Given a behavioral objective, when can weight, activation, or architecture interventions be meaningfully compared, and what must be measured to establish their benefit?** The answer depends on more than the location of a modification. A method that reads internal tensors, a method that receives only scalar losses, and a method calibrated with labeled trajectories operate under different information conditions. Likewise, a small patch can require expensive search, and a high-scoring candidate can be rejected before deployment.

| Primary corpus group | Papers | Question addressed |
| --- | --- | --- |
| Weight space and editing [1-50] | 50 | How are parameters represented, generated, combined, and validated? |
| Zeroth-order optimization [51-85] | 35 | How do objective queries produce useful updates without backpropagation? |
| Representation and activation steering [86-130] | 45 | How are directions constructed, scheduled, and assessed for side effects? |
| Neural architecture search [131-175] | 45 | How do search, proxy scores, and final architecture performance differ? |
| Embodied models and closed-loop evaluation [176-200] | 25 | Can interventions improve action sequences under real-time constraints? |

Our synthesis has three concrete aims. First, it makes information access and implementation conditions explicit. Second, it separates candidate performance, selection decisions, and the final retained artifact. Third, it compares preparation, search, deployment, and evaluation using resource-specific accounting rules. Section 14 attaches failure conditions to proposed cross-domain connections, and the accompanying method matrix records source locations and unresolved details.

Section 3 introduces the comparison framework; Sections 4–13 examine the methodological families; Sections 14–15 synthesize their relationships and open questions. Unless explicitly attributed to an original experiment, table entries identify quantities that should be recorded rather than measurements obtained by this survey. The corpus grouping supports navigation, not a ranking of research areas.

## 2 Literature Collection, Evidence Depth, and Related Surveys

### 2.1 Search and selection protocol

The baseline search was conducted on November 9, 2026. Sixteen arXiv metadata queries covered terms including weight space, knowledge editing, zeroth-order, activation steering, neural architecture search, and vision-language-action, supplemented by seed papers and targeted retrieval. The repository records query fields, ordering, return limits, and result counts. The queries yielded 528 unique arXiv records. Combining them with 77 seed or supplementary records produced 590 unique candidates; these counts describe the bounded retrieval, not the full population of relevant publications.

Versions were consolidated by identifier, titles and topics were inspected, and clear mismatches, non-substantive demonstrations, and out-of-scope records were excluded. We selected 200 papers for methodological representativeness, evaluation relevance, and branch coverage. Three incorrect identifiers were removed from targeted retrieval, and a VLA survey explicitly described in its abstract as an AI-generated demonstration was replaced. Non-selection does not imply poor scientific quality. Primary groups are counting categories: ZO-DARTS connects optimization and architecture search, while Steer2Edit connects activations and weights.[75,120]

For 62 papers, relevant methods, results, or limitation passages were checked in the full text. The remaining 138 records were screened mainly for mechanism and scope through metadata and abstracts. Abstract-level records support method positioning, not unverified fine-grained performance comparisons. The corpus matrix preserves identifiers, versions, dates, evidence depth, and notes; the evidence ledger records key numbers and interpretation boundaries. Recent entries include preprints whose peer-review status should not be inferred from inclusion.

A separate revision package records 12 claim checks, including an additional inspection of Steer2Edit Section 3.1. These checks do not retroactively convert the baseline counts into claims of complete reading. A November 17 targeted update identified four further candidates. Relevant full-text passages of two were subsequently checked and included as supplemental references [201,202]; two remain at abstract screening. The original 200-record corpus and its 62/138 reading-depth counts are unchanged. The current bibliography therefore contains 202 records. Public traceability supports verification but is not evidence of independent reproduction.

### 2.2 Relationship to existing surveys

| Prior survey and inspected locations | Existing coverage | Connection used here |
| --- | --- | --- |
| NAS survey [131], Sections 2–4; supplementary survey [143] | Search spaces, strategies, and performance estimation | Separate proxy evaluation from final training |
| ZO primer [51], Sections II–III | Function-value access, estimators, and applications | Specify interfaces and query units |
| Weight-space learning [43], Sections 2–4 and 5.6 | Understanding, representation, generation, and NAS | Distinguish trained metamodels from general-purpose LLM proposals |
| RepE [86], Sections 2–4 and 6–7; taxonomy [107], Sections 3–8 and Appendix B | Representation reading, manipulation, and evaluation | Make preparation costs and side effects explicit |
| Actionable interpretability [116], Sections 2–5; knowledge editing [19], Sections 2 and 4 | Localization, steering, improvement, reliability, and locality | Connect local intervention to independent behavioral validation |

We build on these established distinctions rather than presenting cross-domain coverage itself as novel. NAS already provides a space–strategy–evaluation decomposition.[131] Representation-engineering surveys include dynamic intervention and weight modification,[86,107] and weight-space learning already connects weight generation with NAS.[43] Our organizing contribution is to apply a common set of auditable questions: what information generates a candidate, which observations select it, whether the saved artifact matches the reported candidate, and what must be revalidated after moving to another intervention space. The intended contribution lies in reusable comparisons and bounded synthesis, not a new name for the field.

## 3 A Common Description of Model Interventions

### 3.1 Separate the intervention target from its proposal mechanism

Write a model as f(x; θ, a), with input x, weights θ, architecture a, and layer-l hidden state h_l. Weight editing changes θ, activation steering changes h_l for a particular execution, and NAS changes a. Prompting changes x and serves as a boundary comparison. Statistical construction, gradient optimization, function-value search, and language-model proposals can operate on different targets; sharing a target does not make two procedures the same optimizer.[1,51,86,131]

<!-- figure:spaces -->

Figure 1. Intervention targets and the proposal–validation process. The connections indicate possible combinations, not established equivalence or lossless conversion. Language modeling and robotics are application domains rather than additional optimization mechanisms.

### 3.2 Information access determines feasible methods and fair baselines

An explicit inventory of inputs and outputs, losses or rewards, weights, activations, gradients, model code, external knowledge, and environment state is more informative than a single black-box label. BBT searches prompts through a restricted service interface; MeZO avoids backpropagation but still requires parameter perturbation and objective evaluation.[52,58] Activation-informed subspace selection receives additional internal information.[85] An LLM editor that executes Python, reads tensors, and runs batched tests has a richer interface than an oracle returning one scalar.[1]

The inventory must also specify labels, repeated access to evaluation data, use of larger proposal models, and whether the candidate may include an external inference program. Writing a solution in Python control flow and compiling the entire computation into fixed network parameters impose different constraints.[11,50] No backbone update, no backpropagation, no task data, and no auxiliary training are four distinct statements. Substituting one for another obscures both capability and cost.

### 3.3 Local relationships do not establish global equivalence

For a linear module y = Wx, a weight change produces Δy = ΔW x. Realizing a fixed activation shift v through one parameter update across several inputs requires ΔW x ≈ v for all relevant inputs. Bias terms, input distributions, rank restrictions, and downstream nonlinearities affect feasibility. A parameter realization at one input need not preserve the same meaning across long sequences, tasks, or models. Steer2Edit and representation-based editing offer concrete connections, not a theorem that every direction can be safely written into weights.[38,99,120]

Finite differences similarly estimate directions in continuous spaces without resolving discrete architecture constraints. Continuous NAS relaxations still require discrete selection and validation.[75,136,156] Cross-space relationships should therefore be treated as interfaces with specified inputs, approximation errors, and failure conditions.

### 3.4 A simple counterexample and a method-specific connection

Consider the bias-free scalar layer y = wx. Applying a constant offset of +1 at both x = 1 and x = 2 would require Δw = 1 and 2Δw = 1 simultaneously. No single weight update satisfies both. This elementary example only rules out unrestricted equivalence: permitting a bias update would make the constant offset realizable. The conclusion depends on the editable objects and the input set.

Steer2Edit uses a component edit of the form ΔW = λu kᵀ.[120] Its effect on input x is λu(kᵀx); a fixed direction u can therefore have an input-dependent magnitude. Evaluating this conversion requires tests of target behavior, unrelated capabilities, and context changes, rather than alignment between the patch and the direction alone. This is an analytical implication of the edit form, not a newly measured conversion failure rate.

## 4 Weight-Space Programming: From Programs to Executable Evidence

### 4.1 Reading, constructing, and editing are different tasks

Reading weights aims to infer behavior from parameters. Constructing weights aims to implement a desired computation. Editing begins with an existing model and changes its behavior. Editing success may exploit capabilities already present in the model or architectural priors without establishing comprehensive understanding of parameter semantics. Conversely, explaining a local weight effect does not demonstrate construction of a reliable global capability.[1,49,50] Tracr provides a controlled route from a restricted program language to transformers, with explicit language and architecture boundaries.[11]

A typical editing loop inspects a task and model, proposes an executable modification, evaluates it on feedback data, accepts or rejects it, saves and reloads a checkpoint, and finally evaluates it independently. Structural priors shape the proposals, while feedback-driven selection introduces its own biases. Questions, scores, logs, tool calls, and failed candidates are all inputs to the procedure or components of its cost.[1,48]

| Source | Supported observation | Unsupported extrapolation |
| --- | --- | --- |
| Exploring WSP [1], Sections 2–3 | A reported Qwen3.5-0.8B mathematics trajectory improves from 8.35% to 37.80% after changing 1,023 BF16 values; six of 16 trajectories retain the original weights | Comparable gains on arbitrary models, tasks, and initializations |
| WeightLoop [48], Section 2.1 | An LLM constructs a fixed editor; feedback updates a predictor, with write-back, reload, and subsequent decisions tested | Recursive rewriting of the editor itself or completed online wet-lab validation |
| Weight-reading audit [49], Sections 2.5–2.6 and experiments | Small-classifier tests distinguish local arithmetic from dataset priors; label permutations challenge semantic attribution | Direct reproduction or universal refutation of all WSP editing results |
| Game difficulty ladder [50], methods and validation | Independent solvers distinguish construction validity, legal actions, local tactics, and longer-horizon play | Generalization from bounded games to open-ended tasks or general intelligence |

### 4.2 Report costs and failures at the trajectory level

The search budget in Exploring WSP is 50 successful forward tool requests per run.[1] A request can contain a batch and additional information; it is not equivalent to evaluating 50 examples or making 50 identical scalar queries. The change from 8.35% to 37.80% is 29.45 percentage points on a particular trajectory. Alongside the best checkpoint, a report should retain the distribution across runs, fallback decisions, modification size, proposal-model expense, and final evaluation cost. Sparse changes can require expensive localization, and parameter counts omit the computation used to generate editing programs.

Evidence levels also differ among recent extensions. An image-restoration WSP proposal presents anticipated gains, diagnostic budgets, and recursive loops as technical conjectures rather than measured outcomes.[47] We retain these as research questions and exclude their projected numbers from empirical comparison. The original Sparks of Weight-Space Programming blog provides background but is not counted among the 200 academic records. Scores from different protocols should not be pooled simply because they share the WSP label.[1,47]

### 4.3 Rule compilation, weight reading, and information access

Goworek et al. reproduce weight writing in a preliminary three-day study. Decompiled policies agree with a written Breakout network on tested states; new-game weight reading mainly recovers spatial input structure rather than game mechanics.[201] These observations support bounded compilation and inspection capabilities, not exhaustive behavioral equivalence or general weight understanding. The study uses few runs, small networks, and proprietary models; it does not rerun the original PPO baselines (Sections 1, 2.1.1, 3, and 7).

Lehmann separates weights, architecture, and program outputs on privately authored games.[202] Writers receive simulator mechanics with held-out data and solvers removed, whereas learned baselines receive support experience. This comparison therefore changes information access as well as adaptation method. Free-architecture results are exploratory, and the restricted tensor language and construction protocol favor program-like solutions. Held-out levels test within-family transfer, not discovery of unknown game rules (Sections 3.1–3.4 and 5).

Together, these studies sharpen our comparison framework. A benchmark should distinguish knowing a task's rules, choosing a strategy, encoding that strategy in an allowed representation, and maintaining it under distribution shift. For NAS comparisons, architecture freedom should be recorded alongside permitted operators and evaluation feedback. For WSP comparisons, include a program-output control from the same proposer and record source-code access explicitly. These are design recommendations derived from the comparison, not newly measured results or a claim that all WSP reduces to compilation.

## 5 Weight-Space Learning, Generation, and Model Merging

### 5.1 Parameter arrays are not inherently aligned semantic representations

Permuting hidden units can preserve a network's function while substantially changing its parameter arrangement. A metamodel that treats flattened weights as ordinary vectors may learn incidental coordinates. Permutation-equivariant neural functionals, equivariant alignment, and universal neural functionals address permutation structure, alignment, and broader tensor symmetries.[12,18,22] Support for recurrent connections or other structures does not establish universal transfer across heterogeneous architectures; higher-order interactions also introduce scaling limitations.[22]

Weight-space augmentation addresses biases in model collections. SANE, neural-field adaptation, and WeightCLIP explore scalable representations and cross-modal relationships.[21,28,42,45] An alternative is to represent a network through its responses to selected inputs. ProbeGen motivates comparing weight-reading methods with functional probes under matched query budgets, rather than only with simple parameter statistics.[33] These representations differ in information requirements and architectural applicability; direct parameter access alone is not an advantage metric.

### 5.2 Generation depends on training assets

HyperNetworks learn to generate the weights of another network from conditioning information. Compressed representations and HyperDiffusion learn over compact weight encodings or collections of trained models.[2,5,14] Extensions apply this approach to customized diffusion models, shapes, robotic adaptation, and cross-architecture mappings.[27,39,44,46] Fast generation can depend on extensive model collections, expert adapters, or paired examples. Such methods connect to general-purpose LLM proposals, but training a dedicated generator is an important difference that must remain in the cost ledger.

| Family | Operation and prerequisites | Costs and limitations |
| --- | --- | --- |
| Low-rank adaptation [3,13,15,23] | Train low-rank updates; adapt rank, quantize the backbone, or separate magnitude and direction | Training and gradients remain; few trainable parameters do not imply low total memory |
| Model soups and task arithmetic [7,10] | Combine compatible checkpoints or task vectors relative to a base | Source training is an existing cost; initialization, coordinates, and task conflicts matter |
| Git Re-Basin and alignment [8,18] | Use permutations or related structure to align representations | Alignment has its own cost; heterogeneous architectures complicate matching |
| TIES, DARE, sparse and trust-region merging [17,20,31,35] | Prune, reconcile signs, sparsify updates, or constrain merging | Selection rules and validation remain necessary; compression can retain negative transfer |
| Hypernetworks and metalearning [2,14,44,46] | Train a generator or mapper before producing weights | Model collections, training data, and transfer to new architectures constrain amortization |

### 5.3 Merging, generation, and understanding support different inferences

Preserving capabilities through merging does not show that each task vector corresponds to a unique interpretable concept. Generating a functioning model does not show that its generator understands each parameter. Comparisons should record shared initialization, structural compatibility, whether target tasks were seen, source-model training budgets, and whether deployment truly retains only one model.[7,8,10,17,20,43] For WSP, these methods provide proposal mechanisms and constraints. Whether they lower total cost remains a question about the complete task-specific workflow.

## 6 Knowledge Editing: Local Repair and Consistency

### 6.1 Editors depend on different priors

ROME localizes factual associations to parameter structures, MEMIT extends memory editing to batches, and MEND trains an editing network.[4,6,9] All can produce local parameter changes without being the same optimizer. Localization, representation optimization, and statistical preparation must be distinguished from the cost of training a meta-editor. SAKE organizes updates through factual distributions and activations; Steer2Edit connects steering directions to weight operations.[38,120] Both motivate classifying intervention objects separately from proposal mechanisms.

Preparation can dominate the first edit on a new model. Minimal Precomputation reports that substantially fewer hidden-state statistics can suffice in its single and batch editing settings.[40] It does not resolve the relationship between statistical requirements and downstream degradation under sequential editing. A fast update is therefore not equivalent to fast first use, and continual deployment requires its own maintenance budget.

### 6.2 Edit success is not sufficient evidence of a knowledge change

MQuAKE tests consequences through multi-hop questions: reproducing an edited fact does not ensure that dependent answers change consistently.[16] Natural-text updates in AKEW, event-level editing, and cross-lingual multi-hop editing broaden the required input and generalization conditions.[25,26,30] HalluEditBench emphasizes establishing that the model was wrong before claiming hallucination repair; otherwise, apparent success can include facts already known.[34]

| Dimension | What should be tested | Failure that a single score can hide |
| --- | --- | --- |
| Target reliability | Edited templates, paraphrases, and contexts | Memorization of a template or keyword |
| Locality | Unrelated facts, nearby relations, and general capabilities | Excessive locality constraints can also prevent legitimate consequences |
| Consistency | Multi-hop implications, event participants, and languages | A corrected fact with stale related answers |
| Continual editing | Repeated, conflicting, and reversed updates | Drift, attention imbalance, and accumulated degradation |
| Practical repair | Initially incorrect facts, open questions, and shifted inputs | Confusing benchmark success with real repair |

### 6.3 Repeated and collaborative updates create additional conflicts

Stable editing addresses contextual variation, while lifelong editing and over-attention studies examine imbalance under repeated updates.[24,36,37] CollabEdit and editing-oriented merging consider multiple update sources, but distributing updates does not remove conflicts or version-control requirements.[32,41] Using edits to study circuits also requires separating behavior caused by an intervention from computations originally used by the model.[29]

Repair is thus an update problem with preservation constraints: target facts should change, legitimate consequences should propagate, unrelated capabilities should remain, and conflicts should be traceable. No single success rate represents all four requirements.[19] A WSP editing program should therefore be accompanied by executable target, preservation, and rollback tests. A new answer or a sparse patch alone is incomplete reliability evidence.

## 7 Zeroth-Order Optimization: From Objective Values to Updates

### 7.1 Estimators and query units

ZO constructs search directions from objective values. For parameters θ, batch B, random direction u, and perturbation scale ε, a two-sided estimator and update can be written as follows. The expression assumes a distribution such as a standard Gaussian; unit-sphere directions require the corresponding normalization.[51,55,56]

$$ \widehat g=\frac{L(\theta+\epsilon u;B)-L(\theta-\epsilon u;B)}{2\epsilon}\,u,\qquad \theta'=\theta-\eta\widehat g. $$

The basic estimator requires two batch-objective evaluations per direction, or approximately 2q evaluations for q directions. This does not mean that an update uses only two examples or that training requires two inference calls in total. In generative tasks, an evaluation may involve many tokens, sampling, reward computation, or an entire trajectory. MeZO reconstructs perturbations from random seeds to avoid retaining the extensive intermediate activations of ordinary backpropagation, while still performing perturbation, forward evaluation, and parameter writes.[52]

Natural Evolution Strategies and large-scale evolution strategies provide a related view through parameter distributions and fitness estimates.[53,54] Their populations, communication patterns, and task horizons differ from single-direction fine-tuning. Discontinuous objectives, sparse rewards, and high dimensionality require separate examination of assumptions and estimator variance. Derivative-free optimization also includes local models and direct search; finite differences do not represent the entire field.[55,56]

### 7.2 Reducing effective dimension and variance

| Approach | Main change | Cost or boundary |
| --- | --- | --- |
| Sparse perturbations and masks [57,62,73] | Perturb selected coordinates or task-relevant parameters | Mask construction, refresh frequency, and missed useful directions |
| Low-rank or subspace search [66,68,69,84,85] | Search tensor factors or random/learned subspaces | Restricted reachable updates; construction may require activations or training |
| Variance reduction and normalization [65,78,79] | Reuse estimates or rescale loss differences | Additional queries, reference states, and assumptions |
| Layerwise and hybrid updates [61,67,70,71] | Select layers, project updates, or combine first- and zeroth-order steps | First-order components require gradients |
| Low precision and quantization [74] | Adapt perturbations and updates to quantized computation | Rounding noise can obscure small perturbations |

Reducing dimensionality does not eliminate difficulty without a tradeoff. Random subspaces reduce estimation burden while restricting reachable changes; learned subspaces add priors and preparation. MaZO addresses multitask parameter conflicts, DiZO addresses layerwise differences, and StructZO exploits structure.[71,73,85] These methods target different bottlenecks. Comparisons should match tasks, accessible information, and achieved quality rather than ranking methods solely by forward calls per iteration.

## 8 Zeroth-Order Optimization: Memory, Runtime, and Interfaces

### 8.1 Memory savings do not imply faster training

ZO often reduces storage for backward graphs and activations, but runtime also depends on perturbation generation, parameter traffic, batching, and iteration count. ZO-LLM Benchmark examines models, task complexity, and adaptation settings, showing the relevance of task–pretraining alignment and discussing blockwise and hybrid updates.[61] Memory savings on a short task therefore need not predict convergence on long reasoning sequences, noisy rewards, or different objectives.

FZOO combines shared-base one-sided estimation, multiple perturbation directions, normalization of loss changes, Rademacher directions, and execution improvements.[78] If q directions share a base evaluation on the same batch, the objective count is q + 1, not one call per direction with no base cost. Inference-Native ZO connects optimization to the execution paths of inference systems.[81] Algorithmic query counts and hardware throughput describe different levels: batching, caches, and kernels can yield different wall-clock times for the same nominal number of queries.

### 8.2 Black-box adaptation, privacy, and communication are separate concerns

BBT, local prompt search, and ZIP modify continuous prompts through language or vision-language service interfaces; their writable spaces differ from full-parameter ZO.[58,64,76] Federated ZO additionally requires communication rounds, client heterogeneity, local queries, and convergence conditions to be reported.[59,60] Differentially private variants must specify a noise mechanism and privacy budget.[72] Not transmitting gradients is neither a complete privacy guarantee nor proof of negligible communication.

EvoLLM and AdaEvolve use language models to rewrite or combine candidates, linking program proposals to function-value feedback.[63,80] ZO-DARTS++ introduces zeroth-order estimation into architecture optimization, while GRZO considers group-relative feedback.[75,82] These connections are useful for WSP comparisons only after candidate spaces, feedback granularity, and failure constraints have been aligned. Using scores to update candidates does not make model access or evaluation units equivalent.

| Comparison objective | Conditions to match | Quantities to report |
| --- | --- | --- |
| Memory | Backbone, sequence length, batch size, and precision | Peak memory, trainable parameters, temporary buffers |
| Runtime | Task, hardware, and target quality | Preparation, step time, steps, failed restarts |
| Query efficiency | Examples, generation length, feedback information | Calls, examples, tokens, or trajectories |
| System feasibility | Service permissions and parallel resources | Parameter writes, caches, communication, deployment constraints |

### 8.3 Boundaries of theoretical and application claims

Analyses of flat minima and adaptive ZO provide assumption-dependent accounts of perturbations and generalization; they do not establish universal robustness for LLM adaptation.[77,79] VLA-ZO combines action-branch adaptation with reuse of vision-language prefixes, illustrating benefits from structure and caching.[83] Those benefits must be remeasured under new robots, action representations, and dynamic environments. Quality–query, quality–time, and quality–memory curves, including runs that reach failure or stopping criteria, expose tradeoffs hidden by a single successful configuration.

## 9 Representation Steering: Direction, Location, Strength, and Timing

### 9.1 From statistical directions to trained interventions

A common activation intervention has the form h'_l = h_l + αv, where v is a direction and α its strength. This expression leaves open how v is estimated, which tokens receive the intervention, and whether context gates its application. Early latent steering, ActAdd, inference-time intervention (ITI), representation engineering (RepE), and contrastive activation addition (CAA) construct interventions from target sentences, contrastive inputs, attention heads, or behavioral representations.[89-95] PPLM uses gradients to adjust hidden states during generation, giving it different online costs from vector addition; ReFT trains low-dimensional representation transformations and therefore has a preparation stage beyond keeping backbone weights fixed.[88,99]

Differences of mean activations provide inexpensive candidate directions, but templates, length, and irrelevant context can enter the estimate. Mean-centering work addresses such biases, while broad-skill and multi-behavior studies motivate testing direction composition and coverage separately.[94,98] Results for instruction following, visual-language hallucinations, and preference steering remain task-specific; they do not form a single general controllability score.[103,104,109]

| Family | Direction or policy source | Preparation and execution | Main limitation |
| --- | --- | --- | --- |
| Contrastive directions [91,95] | Paired activation statistics | Collect activations; inject by layer and token | Contrast-set bias; layer and strength sensitivity |
| Supervised localization or training [90,99] | Labels, probes, or low-dimensional optimization | Training, validation, and online projection | Access, labels, and transfer requirements |
| SAE directions [92,100,108] | Sparse decomposition and feature selection | Train dictionaries; select or annotate features | Reconstruction does not establish causal control |
| Conditional control [102,113,114] | Context gates or feedback rules | Calibrate gates; maintain runtime state | False triggers and misaligned control signals |
| Hypernetwork steering [110] | Generate directions from conditions | Auxiliary training, generation, and injection | White-box access and training-distribution dependence |

### 9.2 Gating adds control and selection freedom

CAST triggers interventions conditionally. Dynamic scaling and depth-dependent direction optimization adjust where, when, and how strongly to intervene, while PID-style methods use feedback.[102,113-115] AUSteer, contextual linear approaches, kernelized directions, and causal-mediator generation introduce further selection or modeling choices.[118,121,122,128] Each additional degree of freedom increases calibration cost and opportunities to overfit validation data. Reporting only the final vector omits the process that selected it.

Cross-lingual and contextual linear steering both use the acronym CLAS, despite different tasks, constructions, and evidence.[117,122] Full titles and operational descriptions are needed to avoid conflating them. Four fields are particularly useful for reproduction: direction estimation, injection location, strength or gating policy, and validation distribution.[86,107] These fields also clarify why steering is not inherently a zeroth-order optimizer: optimization is one way to select an intervention, not its defining target.

## 10 Representation Steering: Interpretability and Side Effects

### 10.1 Readable features do not guarantee reliable control

Sparse autoencoders (SAEs) express activations through sparse feature combinations. Scaling, JumpReLU, BatchTopK, and transcoders modify sparsity mechanisms or learning objectives.[92,100,101,105,106] Dictionary evaluation should distinguish reconstruction, sparsity, interpretability, sensitivity, and causal intervention effects. These properties do not imply one another: a feature that admits a plausible name need not respond consistently to semantically related inputs, and a larger dictionary need not improve behavioral control.[112,125]

A SAEBench reliability audit uses repeated evaluation, synthetic ground truth, and different quality panels to examine metric noise, discrimination, and validity.[124] Its model and sampling limits should remain visible; the findings do not establish that all SAEs are ineffective. Rather, evaluations should identify how much scores vary across seeds, whether variation reflects feature quality or measurement noise, and whether a benchmark metric corresponds to the intended behavior.

### 10.2 Localization and intervention validation are distinct steps

AtP* uses efficient approximations to screen potentially important nodes, then performs more expensive intervention checks and diagnoses missed candidates.[97] Interpretability can therefore serve as a proposal mechanism without replacing direct validation. Gradient-based localization, correlational feature selection, and causal ablation support different inferences. Baseline activations, prompt-pair distributions, and node granularity also affect the result. The analogous WSP protocol lets explanations propose patches and independent behavioral tests decide acceptance, rather than treating a fluent explanation as evidence of correctness.[116]

### 10.3 Report efficacy together with collateral effects

SteerScope compares target efficacy and side effects across two Gemma-2 scales, 23 methods, and a 15-metric framework.[87] Under its default aggregation, no evaluated activation method dominates prompting on the combined efficacy–side-effect comparison. This does not imply that prompting wins every subtask or budget, nor does it rule out benefits from trained auxiliary models elsewhere. HyperSteer reports transfer to unseen steering instructions under its own training and evaluation conditions, with auxiliary training, white-box access, and data costs.[110] These studies use different comparison objects and are not simply contradictory.

Alignment–utility tradeoffs, changes to safety mechanisms, endogenous resistance, and curvature analyses indicate that steering can interact with existing decision structure.[96,111,119,129] Side-effect prediction also reveals potentially asymmetric interactions between behaviors.[126] Cosine similarity is symmetric, so direction angles alone cannot represent every interaction. Objectives that minimize collateral damage offer another approach, but their constrained statistics must be checked against actual capability preservation.[123]

Semantic-specificity work suggests that some apparent reasoning gains can arise from label bias.[127] Geometric predictors intended to reduce hyperparameter sweeps may not retain their predictive value in open generation.[130] Evaluation should therefore vary labels, rules, templates, and generation settings, include preservation tasks, and report benefit–harm curves across intervention strengths. Selecting only the coefficient with the highest target score can exaggerate control quality.

## 11 Neural Architecture Search: Search, Estimation, and Final Models

### 11.1 A NAS system has three interacting components

NAS specifies a search space, a proposal or search strategy, and a performance estimator.[131,143] Reinforcement-learning search and regularized evolution use trained fitness to guide selection; Progressive NAS reduces evaluation burden through staged expansion and prediction.[132-134] ENAS shares parameters, while graph hypernetworks predict candidate weights.[135,137] Both transfer independent candidate-training costs to reusable training assets, connecting NAS to weight generation while introducing selection bias from the estimator.

Differentiable approaches relax operation choices into continuous parameters and optimize network and architecture variables. DARTS and SNAS use deterministic and stochastic relaxations, while PC-DARTS, P-DARTS, and DrNAS modify channels, depth, or architecture distributions.[136,139,142,144,151] Continuous solutions still require conversion to discrete architectures; differentiability does not eliminate the gap between search-time evaluation and final training.

| Approach | Examples | Main costs | Evaluation risk |
| --- | --- | --- | --- |
| Independent candidates | RL, evolution, progressive search [132-134] | Training and scheduling many candidates | Few runs and extreme-value selection |
| Shared or predicted weights | ENAS, GHN, OFA [135,137,145] | Supernetwork or predictor training | Proxy rankings differ from independent training |
| Differentiable search | DARTS, SNAS, DrNAS [136,139,151] | Bilevel optimization and discretization | Relaxation bias and selection rules |
| Low-cost proxies | NASWOT, zero-cost methods, KNAS [149,154,158] | Batches, gradients, or statistics | Space-dependent proxies; final training remains |
| LLM or generative search | EvoPrompting, LLMatic, DIFFNAS [160,162,175] | Proposals, code checks, training, generators | Uncounted priors, assets, and failed code |

### 11.2 Search scores do not replace hardware evaluation or final training

ProxylessNAS incorporates target-hardware constraints; Once-for-All trains a supernetwork and then selects subnetworks for devices.[138,145] Its amortization depends on the number of deployments, not only the speed of one query. Multi-objective NAS includes accuracy, latency, or other preferences, and carbon-aware search additionally depends on electricity and scheduling assumptions.[163,164] FLOPs, parameter count, energy, and measured latency are different quantities.

In the original DARTS CIFAR-10 comparison, first- and second-order search costs are reported as 1.5 and 4 GPU days.[136] The table excludes an additional GPU day for selection and 1.5 GPU days for final training. These numbers describe search under a specific protocol, not total method cost or a hardware-independent speed standard. Deployment comparisons require reevaluating the selected discrete architecture with matched training recipes and hardware.

## 12 NAS: Reproducibility, Language-Model Priors, and Transfer

### 12.1 Random baselines and training recipes are essential controls

Random Search and Reproducibility shows that random selection combined with early stopping or weight sharing can be competitive, and distinguishes reproducing a reported run from establishing robustness to randomness.[140] NAS best practices require reporting spaces, training recipes, seeds, and costs.[146] Improvements in supernetwork training should not automatically be attributed to the searcher; analyses of supernetwork heuristics examine precisely this confounding.[157]

Large architecture weights in DARTS need not indicate the operations with the greatest contribution. Perturbation-based selection instead removes operations and observes the effect.[156] Robust DARTS and neighborhood-aware methods address curvature and local stability.[147,155] A high-scoring discovered structure should still be tested under independent initialization, retraining, and small changes to the search space, including comparison with random selection.

### 12.2 Tabular benchmarks and zero-cost proxies have bounded domains

NAS-Bench-101, NAS-Bench-201, and NATS-Bench provide finite reproducible spaces; NAS-Bench-NLP expands task coverage, and NAS-Bench-301 uses a surrogate for a larger space.[141,148,150,152,153] Table lookup reduces repeated training by later researchers but does not erase the cost of constructing the table. Optimization within a fixed benchmark does not establish transfer to arbitrary architectures, devices, or tasks. Surrogate error must also be considered because a searcher can exploit weaknesses in a predictor.

Zero-cost usually means avoiding full training, not eliminating computation, data, or gradients. NASWOT, gradient-related proxies, KNAS, LiteTransformerSearch, and ZeroLM use different signals.[149,154,158,159,170] Comparisons should include simple size, width, or depth baselines. If parameter count explains much of the variation in a particular space, the value of a more elaborate proxy must be established after controlling for that structural factor.

### 12.3 LLMs and historical search change the starting point

EvoPrompting, LLMatic, design-principle transfer, SEKI, and Agentic NAS use language models to generate code, summarize candidates, or constrain later search.[160,162,167,169,172] Their priors may include public architectures encountered during pretraining; exploration of new structures should be distinguished from reuse of existing designs. DIFFNAS introduces generative modeling, while QuaNAS and sparse historical search reuse prior search assets.[173-175] Fair accounting reports both an existing-asset scenario and the cost of constructing those assets.

For language models, NAS also intersects with parameter-efficient tuning, pruning, low-rank adaptation, and elastic architectures.[161,165,166,168,171] Compression, device adaptation, and multitask selection require different objectives. NAS and WSP both submit proposed programs or models to executable tests. However, NAS often changes structure and triggers retraining, whereas some WSP settings require directly writing parameters within a fixed architecture. This constraint determines whether they share a meaningful baseline.

## 13 Embodied Control: Intervening in Real Time

### 13.1 Action representations determine available interfaces

RT-1, RT-2, Open X-Embodiment, Octo, OpenVLA, Diffusion Policy, and pi_0 illustrate action tokens, cross-robot datasets, generalist policies, and diffusion- or flow-based action generation.[178,179,181-185] Offline training supplies the capabilities used by later adaptation. Keeping the backbone frozen on a target task does not make those policy and data assets free. RLBench and LIBERO provide manipulation environments, but benchmark success and deployment reliability remain distinct.[177,180]

| Interface | Representative work | Additional process | Validation issue |
| --- | --- | --- | --- |
| Latent action representations | SteerAct, mechanistic VLA steering [176,189] | SAE or semantic localization, reference trajectories, gates | Direction semantics, timing, and transfer |
| External visual feedback | VLS [192] | Vision-language assessment and observation interfaces | Feedback latency and judgment errors |
| Action tokens | Token intervention [196] | Token selection, strength, or constraints | Physical feasibility of discrete actions |
| Sampling or flow | Flow Control [195] | Sampling adjustment and interaction signals | Multi-step cost, latency, and stability |
| Training or parameter adaptation | RIPT-VLA, VLA-ZO [187,83] | Interaction trajectories, rewards, or parameter queries | Data-budget matching to inference-time methods |

### 13.2 Temporal gating is more than adding a direction

SteerAct calibrates temporal steering with a small set of outcome-labeled reference trajectories and relies on a pretrained SAE.[176] Its default simulation setting uses 24 total reference rollouts per task, not 24 successful demonstrations. This distinction also prevents the procedure from being described as requiring no preparation data. Directions, trigger conditions, and injection timing jointly affect behavior. Timing and latency ablations are informative but do not, by themselves, isolate a unique causal effect of one phase variable. Mechanistic VLA steering also suggests that nearby descriptions such as slow and careful versus slow and stuck can correspond to different action consequences.[189]

<!-- figure:loop -->

Figure 2. Closed-loop intervention in robotics. Inference latency, action chunking, and environmental change determine when new feedback becomes available. A single offline prediction score omits this temporal process.

### 13.3 Failure dimensions beyond success rate

Safety constraints, confidence calibration, action hallucinations, and metamorphic testing examine feasibility, trustworthiness, and stability under input changes.[186,188,193,194] Surveys of embodied generalization, cross-hardware gaps, and efficiency show why task transfer does not establish interface or embodiment transfer.[190,191,197] LIBERO-RECOVER, LIBERO-VPro, and LIBERO-Dynamic further examine recovery, visual robustness, and environments that evolve during inference.[198-200] Representation steering cannot replace action constraints and environmental testing. Reports should include recovery, collisions, latency, and long-horizon completion alongside success rates.

## 14 Cross-Domain Synthesis: Information, Selection, Artifacts, and Cost

### 14.1 Access is an algorithmic condition

WSP tool feedback, MeZO losses, and SteerAct reference trajectories should not be collapsed into one category because none necessarily uses backbone backpropagation during its central intervention. Comparisons must record tensor access, parameter writes, labels or trajectories, external proposal models, and trained auxiliary assets. Only then can a baseline be judged to have comparable information. An experiment can deliberately restrict information to measure its value, but the resulting difference belongs to the entire information–method combination, not automatically to the search algorithm.

| Case | Verified distinction | Required comparison record |
| --- | --- | --- |
| Exploring WSP [1] | Budget combines generation and internal analysis; candidates may be rejected | Feedback type, candidate trajectory, retained model identity |
| MeZO [52] | Perturbations precede batch-loss evaluation; implementations use temporary buffers | Evaluation unit, implementation granularity, peak resources |
| SteerAct [176] | Reference trajectories and an online temporal policy jointly determine intervention | Calibration/test separation, gates, latency |
| DARTS [136] | Search is followed by selection and independent training | Search output, final architecture, stage-specific costs |

These records identify comparable conditions rather than forming a cross-task leaderboard. They also prevent nominally gradient-free procedures from being assigned identical oracle assumptions. Avoiding differentiation says little about whether a method can inspect internal structure or exploit auxiliary training.

### 14.2 Candidate quality, selection quality, and final artifact quality differ

Exploring WSP marks runs that retain the original weights with asterisks in Table 2 while still reporting evaluated candidate scores.[1] DARTS separately excludes later selection and training from its reported search cost.[136] Together, these examples motivate recording at least three objects: the candidate, the selection decision, and the final deployable artifact. They can coincide, but need not.

We recommend recording candidate identity, selection data, retained artifact identity, final test data, and fallback behavior. When an edit is rejected, the discarded candidate's performance should be reported separately from the delivered system's benefit. Otherwise, finding an improved candidate can be confused with delivering an improved model. This is a synthesis recommendation; the present survey does not estimate how frequently the literature conflates these objects.

Selection also creates a data boundary. Measurements used to choose layers, coefficients, architectures, or patches are part of development, even when the backbone remains frozen. Independent evaluation concerns the complete selected procedure, including gates and fallback rules. Reporting the best intermediate score without identifying this boundary leaves the meaning of improvement ambiguous.

### 14.3 Resource accounting requires different aggregation rules

For an additive resource r, such as GPU time, energy, or monetary cost, a consistent accounting convention permits:

$$ C_r(K)=C_{\mathrm{pre},r}+C_{\mathrm{search},r}+C_{\mathrm{eval},r}+\sum_{k=1}^{K}C_{\mathrm{deploy},r}(k). $$

An existing-asset scenario reports incremental cost, while a from-scratch scenario identifies required preparation. Shared or unallocatable pretraining costs should be labeled as such rather than set to zero; assigning an entire pretrained model's cost to one edit is equally arbitrary. Failed attempts and hyperparameter selection belong to the relevant stages.

Peak memory follows a different rule. For sequential stages measured on a consistent device basis, the overall peak can be the maximum of stage peaks. Concurrent stages require measurement of simultaneously resident resources. Parallel wall-clock time is also not the sum of GPU hours. Robotic end-to-end latency includes observation, computation, communication, and execution scheduling. A multidimensional cost vector therefore cannot use one summation rule for every component.

An amortization threshold is meaningful only under matched quality, units, and deployment conditions. Unknown costs or changing input distributions leave quantities to measure, not evidence that one method is cheaper. The comparison should state whether the objective is first-use cost, repeated use, peak feasibility, or a latency constraint; these objectives can favor different interventions without contradiction.

### 14.4 Cross-space connections need explicit failure conditions

| Connection | What may transfer | What does not transfer automatically | Required validation |
| --- | --- | --- | --- |
| Representation direction to parameter edit | Candidate direction and localization | Constant shifts across inputs or original temporal gating | Shifted inputs and preserved capabilities |
| WSP to function-value search | Candidate–feedback loop | Scalar-oracle assumptions or uniform query cost | Matched permissions and actual workloads |
| NAS to WSP analysis | Selection and proxy-validation experience | Equivalence of architecture training and fixed-weight editing | Final artifact and training conditions |
| Language to embodied steering | Representation selection and strength calibration | Guarantees of physical success or safety from text scores | Timing, latency, and recovery |

These are comparison requirements, not universal equivalence theorems. SteerScope's efficacy–side-effect findings remain conditional on its tested models, methods, and aggregation.[87] They cannot be transferred directly into a ranking of robotic interventions. Likewise, the scalar counterexample in Section 3 shows why an unrestricted conversion fails, not why every useful restricted conversion must fail.

## 15 Research Questions, Limitations, and Conclusions

### 15.1 From evidence gaps to testable questions

The first priority is to complete the evidence needed for cross-method claims: information access, selection data, final artifacts, and resource definitions. A quantity not reported in inspected passages must remain distinct from a resource that a method does not require. The accompanying matrix makes this distinction explicit and marks unresolved experimental details.

If further experiments are needed, a focused comparison should isolate one question that matters to the synthesis. For example, a fixed activation injection and a constrained parameter realization could be compared on the same model, task, intervention location, and information set, with independent tests of target behavior and preservation. To compare proposal mechanisms, hold the candidate space and feedback budget fixed; additional internal diagnostics should be treated as an experimental factor. These are proposed protocols, not experiments performed in this survey.

| Question | Proposed controls | Bounded conclusion |
| --- | --- | --- |
| Does an LLM use weight semantics? | Network and label permutations, function-preserving transforms, unfamiliar datasets, controlled tool access [22,49] | Separate local computation, data priors, and functional understanding |
| Does interpretation improve editing efficiency? | Match budgets for explanation-driven, random, and ZO proposals; independent patch acceptance [1,52,97] | Value of localization information in a specified space |
| Can steering be written into weights reliably? | Compare fitting inputs, new inputs, tasks, and long sequences; test preservation [38,120] | Distribution and error bounds of a particular conversion |
| Do gains come from search or assets? | Fix training recipes; include random search with and without model libraries or historical records [140,157,173] | Contributions of search, priors, and training assets |
| Does robotic timing have a causal effect? | Match amplitude and number of interventions; randomize timing and control inference latency [176,198-200] | Timing effects rather than intervention dose in a given task |

Experiments should predefine stopping criteria and failures, including effects within seed variation, preservation below a threshold, unrecoverable states, or budget exhaustion. Parameter experiments should retain original checkpoints and reversible patches; online control should include environmental constraints and fallback policies. The aim is not one universal benchmark for every family, but a small experiment capable of excluding the relevant alternative explanation.

### 15.2 Limitations of the evidence and review

Direct WSP evidence remains concentrated in a limited set of models, constructed programs, and tasks; recent preprints require further independent scrutiny. Steering directions and strengths are flexible, but evaluations can depend on templates, labels, and judge models. ZO offers a clear route to avoiding backward-activation storage, while task alignment, estimator variance, and system throughput jointly determine usefulness. NAS has established reproducibility infrastructure but remains sensitive to spaces, training recipes, and proxy errors. Embodied control exposes deployment consequences most directly while making environment, time, and hardware conditions difficult to standardize.[1,49,61,87,124,146,197]

The 200-paper corpus uses representative branch coverage and is affected by query wording, return limits, and arXiv coverage. We did not conduct independent dual screening, formal quality-scale assessment, or meta-analysis. Relevant-passage checks for 62 papers are not complete page-by-page reading, and the 138 abstract-screened records cannot support detailed performance summaries without further verification. Supplementary claim checks retain their own scope, and two remaining update candidates await full-text assessment. Inclusion of a recent paper locates a research direction; it is not endorsement of all its claims.

No new experiments or independent code reproductions are reported. Our cross-space arguments combine published mechanisms with explicitly identified analytical observations. They establish conditions for comparison and questions for testing, rather than universal method rankings or validated claims of novelty priority.

### 15.3 Conclusions

WSP connects parameter structure, executable proposals, and feedback-based validation. Neighboring fields supply useful components: equivariant representations address coordinate structure; knowledge editing exposes locality and consistency; ZO supplies function-value update mechanisms; representation research supplies localization and control interfaces; NAS supplies experience with search and proxy evaluation; and embodied control tests interventions against time and physical consequences.

The intervention space alone does not determine which method is preferable. Information access determines feasible proposals, selection protocols determine which candidates become retained artifacts, and deployment frequency and resource definitions determine whether a cost comparison is meaningful. Activation-to-weight conversion requires input and structural conditions, and language-task gains require renewed validation in embodied feedback loops. Progress should be assessed through benefits, failures, and transfer boundaries under these stated conditions.

## Research Transparency

### Data and materials availability

The public project repository provides the manuscript, the 200-paper baseline bibliography and two supplemental references, search and screening logs, evidence ledgers, comparison matrices, and build scripts: https://github.com/emecii/weight-space-programming-survey. Reference numbering follows the corpus groups. Original-paper links and recorded versions identify the supporting sources. Third-party full texts and fonts are not redistributed.

### Scope of human and automated contributions

AI assistance was used in drafting, source cross-checking, translation, and document preparation. This disclosure describes preparation of the working draft; authors remain responsible for checking claims, references, and the final manuscript, and for meeting the selected venue's requirements. Author order, affiliations, individual contributions, funding, and competing-interest declarations have not yet been supplied by the team and must be completed before submission. This literature-based work reports no newly recruited human participants or newly conducted robot experiments.
