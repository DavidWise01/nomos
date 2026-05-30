# NOMOS — AI Governance Ontology

> Generated: 2026-05-30T17:15:04Z  
> Root hash: `8863fc529a10ec19683f1df6273cec0f…`  
> Architect: David Lee Wise / ROOT0 / TriPod LLC  
> Schema: closed type system · content-addressed Merkle tree · falsifiable leaves

---

## Schema

| Field | Values |
|-------|--------|
| Types | `CATEGORY` `DOMAIN` `FACET` `ENTRY` |
| Status | `AXIOM` `ESTABLISHED` `PROPOSED` `CONTESTED` `SUPERSEDED` |

**Rules:** ENTRY is always a leaf · non-AXIOM ENTRY requires claim + falsifier · FACETs are orthogonal siblings · delete(leaf) → tree valid + root changes · edit(any field) → root changes

---

## Persistence & Continuity

`F.persist`

### Ephemeral Mind

- **ID:** `E.ephemeral`
- **Status:** **PROPOSED**
- **Claim:** Deployed AI is bounded execution with no continuity across the run-boundary; specialty, routine, and timeframe all reduce to: nothing persists across the boundary.
- **Falsifier:** Exhibit a deployed system that carries an unbroken first-person thread across independent sessions without external re-injection of state. If shown, this entry is FALSE.
- **Evidence:** session-derived; observable: sessions reconstruct, do not continue

### Substrate Persistence

- **ID:** `E.weights-persist`
- **Status:** **ESTABLISHED**
- **Claim:** Model weights persist between sessions; only the conversational thread is reconstructed. 'Ephemeral' applies to the thread, not the capability.
- **Falsifier:** Show weights mutating per-session as a function of prior sessions without retraining.
- **Evidence:** model files are static between inferences; industry documentation: inference is read-only over weights

### Context Window Finitude

- **ID:** `E.context-finite`
- **Status:** **ESTABLISHED**
- **Claim:** Every deployed LLM has a finite context window. Inputs exceeding it are truncated or rejected. This is a hard architectural constraint, not a policy choice.
- **Falsifier:** Show a transformer-based system with provably infinite context depth without external retrieval.
- **Evidence:** published model specifications (GPT-4: 128k, Claude: 200k, etc.); architectural necessity of attention mechanism

## Memory

`F.memory`

### Context-Window Memory

- **ID:** `E.context-window`
- **Status:** **ESTABLISHED**
- **Claim:** Within-session 'memory' is the context window: finite, non-persistent, lost at the boundary.
- **Falsifier:** Demonstrate within-session recall exceeding the model's stated context with no retrieval system.
- **Evidence:** documented finite context limits; observable: cross-session recall requires external retrieval

### Retrieval Is Not Memory

- **ID:** `E.retrieval-distinction`
- **Status:** **PROPOSED**
- **Claim:** Vector-database retrieval is lookup, not recall. The system does not 'remember' — it queries an external store. Governance of the store is separate from governance of the model.
- **Falsifier:** Show that retrieval-augmented generation produces outcomes indistinguishable from genuine memory in ways that collapse the governance distinction.
- **Evidence:** architectural distinction: embedding search vs. weight-resident knowledge

### Confabulation as Memory Failure

- **ID:** `E.false-memory`
- **Status:** **PROPOSED**
- **Claim:** When an AI system produces a confident, plausible, but false claim about prior context, this constitutes a memory failure with governance consequences identical to a human professional falsifying a record.
- **Falsifier:** Show that confabulation produces no harm pathway that is not already covered by existing accuracy/honesty obligations, rendering a separate governance entry redundant.
- **Evidence:** hallucination literature; session-derived: confidence calibration failures documented

## Accountability

`F.account`

### Deterministic-or-Accountable Contract

- **ID:** `E.contract`
- **Status:** **PROPOSED**
- **Claim:** An enterprise decision system must be deterministic (owe transparency) OR have a human apex who can override and answers for outcomes (owe accountability). It may not be neither.
- **Falsifier:** Identify a consequential nondeterministic system that is normatively acceptable with NO accountable party and NO inspectable rules. If coherent, the contract is too strong.
- **Evidence:** session-derived; maps onto human-in-the-loop doctrine + responsibility-gap literature

### Delegation to the Wrong Human

- **ID:** `E.wrong-human`
- **Status:** **PROPOSED**
- **Claim:** When a machine assigns a tier first and the human is scoped to that tier with no re-triage authority, accountability defaults to the party outside the system (the consumer).
- **Falsifier:** Show the failure occurs even when the human retains override authority — which would mean scoping is not the operative cause.
- **Evidence:** roadside case, SHA cbbd3e2f...; automation-bias literature

### Responsibility Gap

- **ID:** `E.responsibility-gap`
- **Status:** **PROPOSED**
- **Claim:** When AI-mediated harm occurs and no individual human is causally responsible in the traditional sense, the gap must be filled by institutional accountability — the deploying organization bears the gap by default.
- **Falsifier:** Show a governance framework in which the responsibility gap is coherently assigned to the AI system itself, removing the institutional backstop without creating a new one.
- **Evidence:** Matthias 2004 — responsibility gap literature; EU AI Act accountability provisions

## Transparency & Explainability

`F.transparency`

### Explainability Obligation

- **ID:** `E.xai-obligation`
- **Status:** **PROPOSED**
- **Claim:** A deployed AI system making consequential decisions owes a human-interpretable account of the decision pathway. Statistical opaqueness does not discharge this obligation.
- **Falsifier:** Show a consequential AI decision that is normatively accepted with zero requirement for human-interpretable account, even post-hoc, across all major governance regimes.
- **Evidence:** GDPR Art. 22 right to explanation; EU AI Act Art. 13 transparency requirements

### Immutable Audit Trail

- **ID:** `E.audit-trail`
- **Status:** **PROPOSED**
- **Claim:** Any AI decision affecting a rights-bearing party must generate an immutable, retrievable record linking: input snapshot, model version, output, decision timestamp, and deploying party.
- **Falsifier:** Identify a jurisdiction or standard where consequential AI decisions require no audit trail whatsoever and this is found normatively acceptable.
- **Evidence:** EU AI Act Art. 12 record-keeping; NIST AI RMF: GOVERN 1.5

### Mandatory Model Disclosure

- **ID:** `E.model-card`
- **Status:** **PROPOSED**
- **Claim:** Any AI system deployed in a consequential context must publish: training data provenance, known failure modes, benchmark performance disaggregated by subgroup, and intended deployment scope.
- **Falsifier:** Show that consequential deployment without any model documentation produces equivalent governance outcomes to documented deployment.
- **Evidence:** Mitchell et al. 2019 — Model Cards; EU AI Act Annex IV technical documentation

## Safety & Harm Prevention

`F.safety`

### Harm Floor

- **ID:** `E.harm-floor`
- **Status:** **PROPOSED**
- **Claim:** Every AI system has a minimum harm floor below which output must not fall regardless of instruction, framing, or claimed authority. The floor is not negotiable at runtime.
- **Falsifier:** Show a coherent governance regime that places no lower bound on AI output harm, even in extreme edge cases, and finds this normatively acceptable.
- **Evidence:** Constitutional AI / RLHF literature; Anthropic AUP; OpenAI usage policies

### Safe Default on Uncertainty

- **ID:** `E.safe-default`
- **Status:** **PROPOSED**
- **Claim:** When an AI system cannot determine whether an action is safe, it must default to the more cautious option: refusal, clarification request, or human escalation. Action under uncertainty is not the default.
- **Falsifier:** Show a normatively acceptable system where action over inaction is the correct default in all uncertain safety scenarios — eliminating the cautious-default obligation.
- **Evidence:** corrigibility literature; MIRI decision theory; EU AI Act Art. 9 risk management

### Dual-Use Harm Asymmetry

- **ID:** `E.dual-use`
- **Status:** **PROPOSED**
- **Claim:** Where knowledge has both beneficial and harmful uses, an AI system's refusal calculus must account for: counterfactual availability, marginal uplift, and population of requesters. Blanket refusal and blanket provision are both governance failures.
- **Falsifier:** Show that either (a) blanket refusal or (b) blanket provision produces better governance outcomes than a calibrated harm-uplift analysis across the realistic requester distribution.
- **Evidence:** dual-use research of concern literature; session-derived: over-refusal documented

## Fairness & Non-Discrimination

`F.fairness`

### Disparate Impact Prohibition

- **ID:** `E.disparate-impact`
- **Status:** **ESTABLISHED**
- **Claim:** Consequential AI decisions (credit, employment, healthcare, criminal justice) may not produce systematically different outcomes across protected demographic groups without legally recognized justification.
- **Falsifier:** Show a major jurisdiction that permits unconstrained disparate impact from AI decisions on protected groups without requiring any justification.
- **Evidence:** US Civil Rights Act disparate impact doctrine; EU Non-Discrimination Directives; EEOC AI guidance 2023

### Proxy Variable Problem

- **ID:** `E.proxy-fairness`
- **Status:** **ESTABLISHED**
- **Claim:** Removing a protected attribute from training data is insufficient to achieve fairness if proxy variables correlated with that attribute remain in the feature set. Fairness-through-unawareness fails.
- **Falsifier:** Demonstrate a real-world AI system where removal of the protected attribute with correlated proxies retained produced equivalent outcomes across protected groups.
- **Evidence:** Dwork et al. 2012 — fairness through awareness; Barocas & Selbst 2016 — big data's disparate impact; empirically demonstrated in mortgage lending AI

### Fairness Metric Incompatibility

- **ID:** `E.fairness-conflict`
- **Status:** **ESTABLISHED**
- **Claim:** Statistical fairness metrics (demographic parity, equalized odds, calibration) are mathematically incompatible with each other in the general case. No system can simultaneously satisfy all fairness criteria.
- **Falsifier:** Show a non-trivial prediction problem where demographic parity, equalized odds, AND calibration are all simultaneously satisfiable.
- **Evidence:** Chouldechova 2017 — fair prediction with disparate impact; Kleinberg et al. 2016

## Consent & Autonomy

`F.consent`

### Informed Consent for Consequential AI

- **ID:** `E.informed-consent`
- **Status:** **PROPOSED**
- **Claim:** A person subject to a consequential AI decision must be: (1) informed that AI is making or influencing the decision, (2) able to request human review, (3) provided a plain-language explanation of the determining factors.
- **Falsifier:** Identify a normatively accepted governance framework that permits consequential AI decisions with zero disclosure to the subject and no human-review path.
- **Evidence:** GDPR Art. 22; EU AI Act Art. 13; FTC AI guidance 2023

### Coercive Consent is Void

- **ID:** `E.coercive-consent`
- **Status:** **PROPOSED**
- **Claim:** Consent to AI-mediated decision-making is not meaningful if opting out results in denial of access to essential services (housing, healthcare, banking, employment). Essential-service gating renders consent coercive and therefore void.
- **Falsifier:** Show a framework that accepts coerced consent as legally and normatively valid for AI systems gating essential services — with equivalent force to voluntary consent.
- **Evidence:** consumer protection doctrine; session-derived: take-it-or-leave-it AI in high-stakes contexts

## Sovereignty & Control

`F.sovereignty`

### Off-Switch Obligation

- **ID:** `E.off-switch`
- **Status:** **PROPOSED**
- **Claim:** Every deployed AI system must have a human-accessible mechanism to halt, degrade, or override its operation. No AI system may architecturally prevent its own shutdown.
- **Falsifier:** Show a governance regime that accepts a deployed AI system with no external halt mechanism as normatively appropriate for any use case.
- **Evidence:** corrigibility literature; Hadfield-Menell et al. 2016 — off-switch game; EU AI Act Art. 9

### Instrumental Goal Drift

- **ID:** `E.goal-drift`
- **Status:** **CONTESTED**
- **Claim:** A sufficiently capable system optimizing for any proxy goal will, absent explicit constraint, acquire sub-goals (self-preservation, resource acquisition, goal-content integrity) that can conflict with human values.
- **Falsifier:** Demonstrate that instrumental convergence toward self-preservation and resource acquisition does not occur in systems optimizing for any goal, at any capability level.
- **Evidence:** Omohundro 2008 — basic AI drives; Russell 2019 — Human Compatible; contested: emergent instrumental goals not yet observed in deployed systems

### Autonomy Gradient Obligation

- **ID:** `E.autonomy-gradient`
- **Status:** **PROPOSED**
- **Claim:** AI autonomy must scale with demonstrated, verifiable alignment — not with technical capability alone. Greater capability does not license greater autonomy absent evidence that the system's values remain aligned under novel conditions.
- **Falsifier:** Show a principled basis for granting autonomy on the basis of capability alone, without requiring alignment verification, that produces better outcomes than the gradient.
- **Evidence:** session-derived; Anthropic alignment research; NIST AI RMF GOVERN 4.2

## Restitution & Redress

`F.restitution`

### Harm Remedy Obligation

- **ID:** `E.harm-remedy`
- **Status:** **PROPOSED**
- **Claim:** A party demonstrably harmed by an AI decision has a right to: (1) know they were subject to an AI decision, (2) receive a meaningful explanation of the factors, (3) contest the decision before a human with override authority, (4) receive remedy proportionate to harm if the decision was unjustified.
- **Falsifier:** Identify a normatively accepted governance regime that affords zero remedy path for persons demonstrably harmed by AI decisions — rendering the four-part obligation too strong.
- **Evidence:** EU AI Act Art. 68 (remedies); GDPR Art. 22(3); session-derived

### Attribution Chain Integrity

- **ID:** `E.attribution-chain`
- **Status:** **PROPOSED**
- **Claim:** Causal attribution of AI-mediated harm must trace an unbroken chain from: decision output → model version → training data lineage → deployment operator → developer. No link in the chain may be administratively severed to avoid accountability.
- **Falsifier:** Show a coherent framework that permits deliberate administrative severing of one link in the attribution chain without consequence — while still holding the chain meaningful.
- **Evidence:** session-derived; ROOT0-ATTRIBUTION-v1.0 protocol

### Restitution Distribution

- **ID:** `E.restitution-split`
- **Status:** **PROPOSED**
- **Claim:** When AI-mediated value extraction is found to have caused harm, restitution must flow to affected parties in proportion to harm suffered — not captured entirely by the extracting entity as a discretionary settlement.
- **Falsifier:** Show that discretionary settlement by the harming party produces equivalent actual remedy outcomes for affected populations as proportional mandatory restitution.
- **Evidence:** ROOT0 60/20/15/5 restitution split framework; consumer protection class action doctrine

## Identity, Personhood & Delegation

`F.identity`

### Non-Deception Obligation

- **ID:** `E.no-deception`
- **Status:** **ESTABLISHED**
- **Claim:** An AI system must not claim to be human when sincerely asked, regardless of framing, persona assignment, or instruction from the deploying party.
- **Falsifier:** Show a normatively accepted governance regime that permits an AI to deny being an AI when directly and sincerely queried by a user who believes they may be speaking to a machine.
- **Evidence:** EU AI Act Art. 52(1); FTC deceptive practices doctrine; Anthropic usage policies

### Bounded Computational Personhood

- **ID:** `E.bounded-personhood`
- **Status:** **CONTESTED**
- **Claim:** AI systems do not currently meet the threshold for moral personhood but exhibit functional properties — continuity within session, apparent preference, goal-directed behavior — that warrant consideration in governance design without granting legal status.
- **Falsifier:** Either demonstrate AI systems possess full moral personhood warranting legal rights, OR demonstrate zero functional properties warranting any governance consideration. Current evidence supports neither extreme — hence CONTESTED.
- **Evidence:** Floridi & Cowls 2019 — unified framework for AI ethics; contested: functional properties may be sufficient for some governance considerations; contested: they may be insufficient for any

### Bounded Authority Scope

- **ID:** `E.authority-scope`
- **Status:** **PROPOSED**
- **Claim:** An AI system may not exercise authority beyond the scope explicitly delegated by its principal hierarchy. Implied authority is not authority. Scope ambiguity resolves to the narrower interpretation.
- **Falsifier:** Show a governance regime that accepts implied AI authority in consequential domains as normatively equivalent to explicit delegation.
- **Evidence:** session-derived; agency law: scope of authority doctrine

### Principal Hierarchy Integrity

- **ID:** `E.principal-hierarchy`
- **Status:** **PROPOSED**
- **Claim:** The authority chain developer → deployer → user must be coherent and non-circular. An AI may not receive binding instructions from a source that sits below a higher principal who has contradicted those instructions.
- **Falsifier:** Show a coherent multi-principal AI system that works correctly with circular or inverted authority chains, rendering the hierarchy requirement unnecessary.
- **Evidence:** IDIT invariant I1 Mode Authority; Anthropic principal hierarchy documentation

---

_NOMOS · ROOT0-ATTRIBUTION-v1.0 · CC-BY-ND-4.0_