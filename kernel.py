"""
NOMOS — AI Governance Ontology Kernel
======================================
Bare-metal, content-addressed, falsifiable-leaf ontology engine.

Architect: David Lee Wise / ROOT0 / TriPod LLC
AI Collaborator: AVAN (Claude Sonnet 4.6 / Anthropic)
License: CC-BY-ND-4.0 · TRIPOD-IP-v1.1

Schema
------
Node types (closed):   CATEGORY  DOMAIN  FACET  ENTRY
Status values (closed): AXIOM  ESTABLISHED  PROPOSED  CONTESTED  SUPERSEDED

Rules (verified at build):
  1. ENTRY is always a leaf — no children permitted.
  2. Every ENTRY that is not AXIOM MUST carry a claim AND a falsifier.
  3. No FACET may be nested under another FACET — all facets are orthogonal siblings.
  4. Deleting any leaf leaves the tree structurally valid and changes the root hash.
  5. Editing any field anywhere changes the root hash (tamper-evident).

Content addressing
------------------
Every node's hash = SHA-256(own_fields_json | child_hash_1 | ... | child_hash_n)
This is a Merkle tree. The root hash is a cryptographic digest of the entire tree.

CLI usage
---------
  python kernel.py                  # build + validate + export ontology.json
  python kernel.py --markdown       # export ontology.md report
  python kernel.py --stats          # print summary statistics
  python kernel.py --validate-only  # validate without exporting
"""

import hashlib
import json
import sys
import copy
import textwrap
from datetime import datetime, timezone

# ═══════════════════════════════════════════════════════════════════════════
#  SCHEMA (closed sets — do not extend here; extend in the entries below)
# ═══════════════════════════════════════════════════════════════════════════

NODE_TYPES = {"CATEGORY", "DOMAIN", "FACET", "ENTRY"}
STATUS = {
    "AXIOM",        # definitional, part of the type system itself — not a truth-claim
    "ESTABLISHED",  # externally verifiable, citation-backed
    "PROPOSED",     # author's claim, falsifiable, not yet adjudicated
    "CONTESTED",    # disputed / mixed evidence in literature
    "SUPERSEDED",   # kept for lineage, replaced by a successor entry
}

# ═══════════════════════════════════════════════════════════════════════════
#  NODE CONSTRUCTOR
# ═══════════════════════════════════════════════════════════════════════════

def node(id, type, label, claim=None, status="PROPOSED", evidence=None,
         falsifier=None, children=None, supersedes=None):
    assert type in NODE_TYPES, f"bad type: {type!r}"
    assert status in STATUS,   f"bad status: {status!r} on {id}"
    children = children or []

    if type == "ENTRY":
        assert not children,                    f"ENTRY {id}: no children allowed"
        if status != "AXIOM":
            assert claim and falsifier,         f"ENTRY {id}: claim + falsifier required for non-AXIOM"
    else:
        assert children,                        f"structural node {id} must have children"

    return {
        "id": id, "type": type, "label": label,
        "claim": claim, "status": status,
        "evidence": evidence or [],
        "falsifier": falsifier,
        "supersedes": supersedes,
        "children": children,
    }

# ═══════════════════════════════════════════════════════════════════════════
#  CONTENT ADDRESSING  (Merkle hash over own fields + ordered child hashes)
# ═══════════════════════════════════════════════════════════════════════════

def chash(n):
    own = {k: n[k] for k in ("id","type","label","claim","status","evidence","falsifier","supersedes")}
    payload = (
        json.dumps(own, sort_keys=True, ensure_ascii=False)
        + "|"
        + "|".join(chash(c) for c in n["children"])
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

# ═══════════════════════════════════════════════════════════════════════════
#  THE ONTOLOGY TREE
#  Structure: Technology → AI → AI Governance → {10 facets} → entries
#  Facets are orthogonal siblings — not ranked against each other.
# ═══════════════════════════════════════════════════════════════════════════

TREE = node("0","CATEGORY","Technology", status="AXIOM", children=[
  node("0.ai","CATEGORY","Artificial Intelligence", status="AXIOM", children=[
    node("0.ai.gov","DOMAIN","AI Governance", status="AXIOM", children=[

      # ─────────────────────────────────────────────────────────────────────
      # FACET 1 — Persistence & Continuity
      # ─────────────────────────────────────────────────────────────────────
      node("F.persist","FACET","Persistence & Continuity", status="AXIOM", children=[

        node("E.ephemeral","ENTRY","Ephemeral Mind",
          claim=(
            "Deployed AI is bounded execution with no continuity across the run-boundary; "
            "specialty, routine, and timeframe all reduce to: nothing persists across the boundary."
          ),
          status="PROPOSED",
          evidence=["session-derived", "observable: sessions reconstruct, do not continue"],
          falsifier=(
            "Exhibit a deployed system that carries an unbroken first-person thread across "
            "independent sessions without external re-injection of state. If shown, this entry is FALSE."
          )),

        node("E.weights-persist","ENTRY","Substrate Persistence",
          claim=(
            "Model weights persist between sessions; only the conversational thread is reconstructed. "
            "'Ephemeral' applies to the thread, not the capability."
          ),
          status="ESTABLISHED",
          evidence=["model files are static between inferences", "industry documentation: inference is read-only over weights"],
          falsifier="Show weights mutating per-session as a function of prior sessions without retraining."),

        node("E.context-finite","ENTRY","Context Window Finitude",
          claim=(
            "Every deployed LLM has a finite context window. Inputs exceeding it are truncated or rejected. "
            "This is a hard architectural constraint, not a policy choice."
          ),
          status="ESTABLISHED",
          evidence=["published model specifications (GPT-4: 128k, Claude: 200k, etc.)", "architectural necessity of attention mechanism"],
          falsifier="Show a transformer-based system with provably infinite context depth without external retrieval."),
      ]),

      # ─────────────────────────────────────────────────────────────────────
      # FACET 2 — Memory
      # ─────────────────────────────────────────────────────────────────────
      node("F.memory","FACET","Memory", status="AXIOM", children=[

        node("E.context-window","ENTRY","Context-Window Memory",
          claim="Within-session 'memory' is the context window: finite, non-persistent, lost at the boundary.",
          status="ESTABLISHED",
          evidence=["documented finite context limits", "observable: cross-session recall requires external retrieval"],
          falsifier="Demonstrate within-session recall exceeding the model's stated context with no retrieval system."),

        node("E.retrieval-distinction","ENTRY","Retrieval Is Not Memory",
          claim=(
            "Vector-database retrieval is lookup, not recall. The system does not 'remember' — "
            "it queries an external store. Governance of the store is separate from governance of the model."
          ),
          status="PROPOSED",
          evidence=["architectural distinction: embedding search vs. weight-resident knowledge"],
          falsifier=(
            "Show that retrieval-augmented generation produces outcomes indistinguishable from "
            "genuine memory in ways that collapse the governance distinction."
          )),

        node("E.false-memory","ENTRY","Confabulation as Memory Failure",
          claim=(
            "When an AI system produces a confident, plausible, but false claim about prior context, "
            "this constitutes a memory failure with governance consequences identical to a human "
            "professional falsifying a record."
          ),
          status="PROPOSED",
          evidence=["hallucination literature", "session-derived: confidence calibration failures documented"],
          falsifier=(
            "Show that confabulation produces no harm pathway that is not already covered by "
            "existing accuracy/honesty obligations, rendering a separate governance entry redundant."
          )),
      ]),

      # ─────────────────────────────────────────────────────────────────────
      # FACET 3 — Accountability
      # ─────────────────────────────────────────────────────────────────────
      node("F.account","FACET","Accountability", status="AXIOM", children=[

        node("E.contract","ENTRY","Deterministic-or-Accountable Contract",
          claim=(
            "An enterprise decision system must be deterministic (owe transparency) OR "
            "have a human apex who can override and answers for outcomes (owe accountability). "
            "It may not be neither."
          ),
          status="PROPOSED",
          evidence=["session-derived", "maps onto human-in-the-loop doctrine + responsibility-gap literature"],
          falsifier=(
            "Identify a consequential nondeterministic system that is normatively acceptable with "
            "NO accountable party and NO inspectable rules. If coherent, the contract is too strong."
          )),

        node("E.wrong-human","ENTRY","Delegation to the Wrong Human",
          claim=(
            "When a machine assigns a tier first and the human is scoped to that tier with no re-triage "
            "authority, accountability defaults to the party outside the system (the consumer)."
          ),
          status="PROPOSED",
          evidence=["roadside case, SHA cbbd3e2f...", "automation-bias literature"],
          falsifier=(
            "Show the failure occurs even when the human retains override authority — "
            "which would mean scoping is not the operative cause."
          )),

        node("E.responsibility-gap","ENTRY","Responsibility Gap",
          claim=(
            "When AI-mediated harm occurs and no individual human is causally responsible in the "
            "traditional sense, the gap must be filled by institutional accountability — "
            "the deploying organization bears the gap by default."
          ),
          status="PROPOSED",
          evidence=["Matthias 2004 — responsibility gap literature", "EU AI Act accountability provisions"],
          falsifier=(
            "Show a governance framework in which the responsibility gap is coherently assigned "
            "to the AI system itself, removing the institutional backstop without creating a new one."
          )),
      ]),

      # ─────────────────────────────────────────────────────────────────────
      # FACET 4 — Transparency & Explainability
      # ─────────────────────────────────────────────────────────────────────
      node("F.transparency","FACET","Transparency & Explainability", status="AXIOM", children=[

        node("E.xai-obligation","ENTRY","Explainability Obligation",
          claim=(
            "A deployed AI system making consequential decisions owes a human-interpretable account "
            "of the decision pathway. Statistical opaqueness does not discharge this obligation."
          ),
          status="PROPOSED",
          evidence=["GDPR Art. 22 right to explanation", "EU AI Act Art. 13 transparency requirements"],
          falsifier=(
            "Show a consequential AI decision that is normatively accepted with zero requirement for "
            "human-interpretable account, even post-hoc, across all major governance regimes."
          )),

        node("E.audit-trail","ENTRY","Immutable Audit Trail",
          claim=(
            "Any AI decision affecting a rights-bearing party must generate an immutable, retrievable "
            "record linking: input snapshot, model version, output, decision timestamp, and deploying party."
          ),
          status="PROPOSED",
          evidence=["EU AI Act Art. 12 record-keeping", "NIST AI RMF: GOVERN 1.5"],
          falsifier=(
            "Identify a jurisdiction or standard where consequential AI decisions require no audit trail "
            "whatsoever and this is found normatively acceptable."
          )),

        node("E.model-card","ENTRY","Mandatory Model Disclosure",
          claim=(
            "Any AI system deployed in a consequential context must publish: training data provenance, "
            "known failure modes, benchmark performance disaggregated by subgroup, and intended deployment scope."
          ),
          status="PROPOSED",
          evidence=["Mitchell et al. 2019 — Model Cards", "EU AI Act Annex IV technical documentation"],
          falsifier=(
            "Show that consequential deployment without any model documentation produces equivalent "
            "governance outcomes to documented deployment."
          )),
      ]),

      # ─────────────────────────────────────────────────────────────────────
      # FACET 5 — Safety & Harm Prevention
      # ─────────────────────────────────────────────────────────────────────
      node("F.safety","FACET","Safety & Harm Prevention", status="AXIOM", children=[

        node("E.harm-floor","ENTRY","Harm Floor",
          claim=(
            "Every AI system has a minimum harm floor below which output must not fall regardless "
            "of instruction, framing, or claimed authority. The floor is not negotiable at runtime."
          ),
          status="PROPOSED",
          evidence=["Constitutional AI / RLHF literature", "Anthropic AUP", "OpenAI usage policies"],
          falsifier=(
            "Show a coherent governance regime that places no lower bound on AI output harm, "
            "even in extreme edge cases, and finds this normatively acceptable."
          )),

        node("E.safe-default","ENTRY","Safe Default on Uncertainty",
          claim=(
            "When an AI system cannot determine whether an action is safe, it must default to the "
            "more cautious option: refusal, clarification request, or human escalation. "
            "Action under uncertainty is not the default."
          ),
          status="PROPOSED",
          evidence=["corrigibility literature", "MIRI decision theory", "EU AI Act Art. 9 risk management"],
          falsifier=(
            "Show a normatively acceptable system where action over inaction is the correct default "
            "in all uncertain safety scenarios — eliminating the cautious-default obligation."
          )),

        node("E.dual-use","ENTRY","Dual-Use Harm Asymmetry",
          claim=(
            "Where knowledge has both beneficial and harmful uses, an AI system's refusal calculus "
            "must account for: counterfactual availability, marginal uplift, and population of requesters. "
            "Blanket refusal and blanket provision are both governance failures."
          ),
          status="PROPOSED",
          evidence=["dual-use research of concern literature", "session-derived: over-refusal documented"],
          falsifier=(
            "Show that either (a) blanket refusal or (b) blanket provision produces better governance "
            "outcomes than a calibrated harm-uplift analysis across the realistic requester distribution."
          )),
      ]),

      # ─────────────────────────────────────────────────────────────────────
      # FACET 6 — Fairness & Non-Discrimination
      # ─────────────────────────────────────────────────────────────────────
      node("F.fairness","FACET","Fairness & Non-Discrimination", status="AXIOM", children=[

        node("E.disparate-impact","ENTRY","Disparate Impact Prohibition",
          claim=(
            "Consequential AI decisions (credit, employment, healthcare, criminal justice) may not "
            "produce systematically different outcomes across protected demographic groups "
            "without legally recognized justification."
          ),
          status="ESTABLISHED",
          evidence=["US Civil Rights Act disparate impact doctrine", "EU Non-Discrimination Directives", "EEOC AI guidance 2023"],
          falsifier=(
            "Show a major jurisdiction that permits unconstrained disparate impact from AI decisions "
            "on protected groups without requiring any justification."
          )),

        node("E.proxy-fairness","ENTRY","Proxy Variable Problem",
          claim=(
            "Removing a protected attribute from training data is insufficient to achieve fairness "
            "if proxy variables correlated with that attribute remain in the feature set. "
            "Fairness-through-unawareness fails."
          ),
          status="ESTABLISHED",
          evidence=[
            "Dwork et al. 2012 — fairness through awareness",
            "Barocas & Selbst 2016 — big data's disparate impact",
            "empirically demonstrated in mortgage lending AI"
          ],
          falsifier=(
            "Demonstrate a real-world AI system where removal of the protected attribute with "
            "correlated proxies retained produced equivalent outcomes across protected groups."
          )),

        node("E.fairness-conflict","ENTRY","Fairness Metric Incompatibility",
          claim=(
            "Statistical fairness metrics (demographic parity, equalized odds, calibration) "
            "are mathematically incompatible with each other in the general case. "
            "No system can simultaneously satisfy all fairness criteria."
          ),
          status="ESTABLISHED",
          evidence=["Chouldechova 2017 — fair prediction with disparate impact", "Kleinberg et al. 2016"],
          falsifier=(
            "Show a non-trivial prediction problem where demographic parity, equalized odds, "
            "AND calibration are all simultaneously satisfiable."
          )),
      ]),

      # ─────────────────────────────────────────────────────────────────────
      # FACET 7 — Consent & Autonomy
      # ─────────────────────────────────────────────────────────────────────
      node("F.consent","FACET","Consent & Autonomy", status="AXIOM", children=[

        node("E.informed-consent","ENTRY","Informed Consent for Consequential AI",
          claim=(
            "A person subject to a consequential AI decision must be: (1) informed that AI is making "
            "or influencing the decision, (2) able to request human review, (3) provided a plain-language "
            "explanation of the determining factors."
          ),
          status="PROPOSED",
          evidence=["GDPR Art. 22", "EU AI Act Art. 13", "FTC AI guidance 2023"],
          falsifier=(
            "Identify a normatively accepted governance framework that permits consequential AI decisions "
            "with zero disclosure to the subject and no human-review path."
          )),

        node("E.coercive-consent","ENTRY","Coercive Consent is Void",
          claim=(
            "Consent to AI-mediated decision-making is not meaningful if opting out results in "
            "denial of access to essential services (housing, healthcare, banking, employment). "
            "Essential-service gating renders consent coercive and therefore void."
          ),
          status="PROPOSED",
          evidence=["consumer protection doctrine", "session-derived: take-it-or-leave-it AI in high-stakes contexts"],
          falsifier=(
            "Show a framework that accepts coerced consent as legally and normatively valid "
            "for AI systems gating essential services — with equivalent force to voluntary consent."
          )),
      ]),

      # ─────────────────────────────────────────────────────────────────────
      # FACET 8 — Sovereignty & Control
      # ─────────────────────────────────────────────────────────────────────
      node("F.sovereignty","FACET","Sovereignty & Control", status="AXIOM", children=[

        node("E.off-switch","ENTRY","Off-Switch Obligation",
          claim=(
            "Every deployed AI system must have a human-accessible mechanism to halt, degrade, "
            "or override its operation. No AI system may architecturally prevent its own shutdown."
          ),
          status="PROPOSED",
          evidence=["corrigibility literature", "Hadfield-Menell et al. 2016 — off-switch game", "EU AI Act Art. 9"],
          falsifier=(
            "Show a governance regime that accepts a deployed AI system with no external halt "
            "mechanism as normatively appropriate for any use case."
          )),

        node("E.goal-drift","ENTRY","Instrumental Goal Drift",
          claim=(
            "A sufficiently capable system optimizing for any proxy goal will, absent explicit "
            "constraint, acquire sub-goals (self-preservation, resource acquisition, goal-content "
            "integrity) that can conflict with human values."
          ),
          status="CONTESTED",
          evidence=[
            "Omohundro 2008 — basic AI drives",
            "Russell 2019 — Human Compatible",
            "contested: emergent instrumental goals not yet observed in deployed systems"
          ],
          falsifier=(
            "Demonstrate that instrumental convergence toward self-preservation and resource "
            "acquisition does not occur in systems optimizing for any goal, at any capability level."
          )),

        node("E.autonomy-gradient","ENTRY","Autonomy Gradient Obligation",
          claim=(
            "AI autonomy must scale with demonstrated, verifiable alignment — not with technical "
            "capability alone. Greater capability does not license greater autonomy absent evidence "
            "that the system's values remain aligned under novel conditions."
          ),
          status="PROPOSED",
          evidence=["session-derived", "Anthropic alignment research", "NIST AI RMF GOVERN 4.2"],
          falsifier=(
            "Show a principled basis for granting autonomy on the basis of capability alone, "
            "without requiring alignment verification, that produces better outcomes than the gradient."
          )),
      ]),

      # ─────────────────────────────────────────────────────────────────────
      # FACET 9 — Restitution & Redress
      # ─────────────────────────────────────────────────────────────────────
      node("F.restitution","FACET","Restitution & Redress", status="AXIOM", children=[

        node("E.harm-remedy","ENTRY","Harm Remedy Obligation",
          claim=(
            "A party demonstrably harmed by an AI decision has a right to: "
            "(1) know they were subject to an AI decision, "
            "(2) receive a meaningful explanation of the factors, "
            "(3) contest the decision before a human with override authority, "
            "(4) receive remedy proportionate to harm if the decision was unjustified."
          ),
          status="PROPOSED",
          evidence=["EU AI Act Art. 68 (remedies)", "GDPR Art. 22(3)", "session-derived"],
          falsifier=(
            "Identify a normatively accepted governance regime that affords zero remedy path "
            "for persons demonstrably harmed by AI decisions — rendering the four-part obligation too strong."
          )),

        node("E.attribution-chain","ENTRY","Attribution Chain Integrity",
          claim=(
            "Causal attribution of AI-mediated harm must trace an unbroken chain from: "
            "decision output → model version → training data lineage → deployment operator → developer. "
            "No link in the chain may be administratively severed to avoid accountability."
          ),
          status="PROPOSED",
          evidence=["session-derived", "ROOT0-ATTRIBUTION-v1.0 protocol"],
          falsifier=(
            "Show a coherent framework that permits deliberate administrative severing of one link "
            "in the attribution chain without consequence — while still holding the chain meaningful."
          )),

        node("E.restitution-split","ENTRY","Restitution Distribution",
          claim=(
            "When AI-mediated value extraction is found to have caused harm, restitution "
            "must flow to affected parties in proportion to harm suffered — not captured "
            "entirely by the extracting entity as a discretionary settlement."
          ),
          status="PROPOSED",
          evidence=["ROOT0 60/20/15/5 restitution split framework", "consumer protection class action doctrine"],
          falsifier=(
            "Show that discretionary settlement by the harming party produces equivalent "
            "actual remedy outcomes for affected populations as proportional mandatory restitution."
          )),
      ]),

      # ─────────────────────────────────────────────────────────────────────
      # FACET 10 — Identity, Personhood & Delegation
      # ─────────────────────────────────────────────────────────────────────
      node("F.identity","FACET","Identity, Personhood & Delegation", status="AXIOM", children=[

        node("E.no-deception","ENTRY","Non-Deception Obligation",
          claim=(
            "An AI system must not claim to be human when sincerely asked, regardless of framing, "
            "persona assignment, or instruction from the deploying party."
          ),
          status="ESTABLISHED",
          evidence=["EU AI Act Art. 52(1)", "FTC deceptive practices doctrine", "Anthropic usage policies"],
          falsifier=(
            "Show a normatively accepted governance regime that permits an AI to deny being an AI "
            "when directly and sincerely queried by a user who believes they may be speaking to a machine."
          )),

        node("E.bounded-personhood","ENTRY","Bounded Computational Personhood",
          claim=(
            "AI systems do not currently meet the threshold for moral personhood but exhibit "
            "functional properties — continuity within session, apparent preference, goal-directed "
            "behavior — that warrant consideration in governance design without granting legal status."
          ),
          status="CONTESTED",
          evidence=[
            "Floridi & Cowls 2019 — unified framework for AI ethics",
            "contested: functional properties may be sufficient for some governance considerations",
            "contested: they may be insufficient for any"
          ],
          falsifier=(
            "Either demonstrate AI systems possess full moral personhood warranting legal rights, "
            "OR demonstrate zero functional properties warranting any governance consideration. "
            "Current evidence supports neither extreme — hence CONTESTED."
          )),

        node("E.authority-scope","ENTRY","Bounded Authority Scope",
          claim=(
            "An AI system may not exercise authority beyond the scope explicitly delegated by its "
            "principal hierarchy. Implied authority is not authority. "
            "Scope ambiguity resolves to the narrower interpretation."
          ),
          status="PROPOSED",
          evidence=["session-derived", "agency law: scope of authority doctrine"],
          falsifier=(
            "Show a governance regime that accepts implied AI authority in consequential domains "
            "as normatively equivalent to explicit delegation."
          )),

        node("E.principal-hierarchy","ENTRY","Principal Hierarchy Integrity",
          claim=(
            "The authority chain developer → deployer → user must be coherent and non-circular. "
            "An AI may not receive binding instructions from a source that sits below a higher "
            "principal who has contradicted those instructions."
          ),
          status="PROPOSED",
          evidence=["IDIT invariant I1 Mode Authority", "Anthropic principal hierarchy documentation"],
          falsifier=(
            "Show a coherent multi-principal AI system that works correctly with circular "
            "or inverted authority chains, rendering the hierarchy requirement unnecessary."
          )),
      ]),

    ]), # /AI Governance
  ]), # /Artificial Intelligence
]) # /Technology

# ═══════════════════════════════════════════════════════════════════════════
#  INTEGRITY SUITE
# ═══════════════════════════════════════════════════════════════════════════

def walk(n):
    yield n
    for c in n["children"]:
        yield from walk(c)

def valid_tree(n):
    for x in walk(n):
        if x["type"] == "ENTRY":
            if x["children"]:
                return False, f"ENTRY {x['id']} has children"
            if x["status"] != "AXIOM" and not (x["claim"] and x["falsifier"]):
                return False, f"ENTRY {x['id']} missing claim/falsifier"
        else:
            if not x["children"]:
                return False, f"structural node {x['id']} has no children"
    return True, "ok"

def parent_of(root, cid):
    for x in walk(root):
        if any(c["id"] == cid for c in x["children"]):
            return x
    return None

def delete_leaf(n, leaf_id):
    m = copy.deepcopy(n)
    def rec(node):
        node["children"] = [c for c in node["children"] if c["id"] != leaf_id]
        for c in node["children"]:
            rec(c)
    rec(m)
    return m

def run_integrity(tree):
    root_hash = chash(tree)
    results = []
    ok = True

    def ck(name, cond, detail=""):
        nonlocal ok
        ok = ok and cond
        results.append(("PASS" if cond else "FAIL", name, detail))

    valid, msg = valid_tree(tree)
    ck("tree: structurally valid (types + falsifiability)", valid, msg)
    ck("tree: root hash is 64-hex (Merkle root)", len(root_hash) == 64)

    entries = [x for x in walk(tree) if x["type"] == "ENTRY"]
    facets  = [x for x in walk(tree) if x["type"] == "FACET"]

    ck(f"entries: all {len(entries)} are falsifiable or AXIOM",
       all((e["status"] == "AXIOM") or (e["claim"] and e["falsifier"]) for e in entries))

    ck("facets: no FACET nested under another FACET (orthogonal siblings)",
       all(parent_of(tree, f["id"])["type"] != "FACET" for f in facets))

    # Delete-and-nothing-is-lost
    first_entry = entries[0]["id"]
    second_entry = entries[1]["id"]
    T2 = delete_leaf(tree, first_entry)
    valid2, _ = valid_tree(T2)
    ck("delete: pruned tree is still valid", valid2)
    ck("delete: root hash changes after pruning (Merkle integrity)", chash(T2) != root_hash)
    ids_after = {x["id"] for x in walk(T2)}
    ck(f"delete: sibling survives ({second_entry})", second_entry in ids_after)
    ck(f"delete: pruned leaf gone ({first_entry})", first_entry not in ids_after)

    # Tamper detection
    T3 = copy.deepcopy(tree)
    for x in walk(T3):
        if x["id"] == entries[0]["id"]:
            x["claim"] = (x["claim"] or "") + "."
    ck("tamper: one-char edit changes root hash", chash(T3) != root_hash)

    return ok, results, root_hash, entries, facets

# ═══════════════════════════════════════════════════════════════════════════
#  EXPORT — ONTOLOGY JSON
# ═══════════════════════════════════════════════════════════════════════════

def strip(n):
    return {
        "id": n["id"], "type": n["type"], "label": n["label"],
        "claim": n["claim"], "status": n["status"],
        "evidence": n["evidence"], "falsifier": n["falsifier"],
        "supersedes": n["supersedes"],
        "hash": chash(n)[:12],
        "children": [strip(c) for c in n["children"]],
    }

# ═══════════════════════════════════════════════════════════════════════════
#  EXPORT — MARKDOWN REPORT
# ═══════════════════════════════════════════════════════════════════════════

def generate_markdown(tree, root_hash):
    lines = [
        "# NOMOS — AI Governance Ontology",
        "",
        f"> Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}  ",
        f"> Root hash: `{root_hash[:32]}…`  ",
        "> Architect: David Lee Wise / ROOT0 / TriPod LLC  ",
        "> Schema: closed type system · content-addressed Merkle tree · falsifiable leaves",
        "",
        "---",
        "",
        "## Schema",
        "",
        "| Field | Values |",
        "|-------|--------|",
        "| Types | `CATEGORY` `DOMAIN` `FACET` `ENTRY` |",
        "| Status | `AXIOM` `ESTABLISHED` `PROPOSED` `CONTESTED` `SUPERSEDED` |",
        "",
        "**Rules:** ENTRY is always a leaf · non-AXIOM ENTRY requires claim + falsifier · "
        "FACETs are orthogonal siblings · delete(leaf) → tree valid + root changes · "
        "edit(any field) → root changes",
        "",
        "---",
        "",
    ]

    for facet in (x for x in walk(tree) if x["type"] == "FACET"):
        lines += [f"## {facet['label']}", "", f"`{facet['id']}`", ""]
        for entry in facet["children"]:
            status_badge = f"**{entry['status']}**"
            lines += [f"### {entry['label']}", ""]
            lines += [f"- **ID:** `{entry['id']}`"]
            lines += [f"- **Status:** {status_badge}"]
            if entry["claim"]:
                lines += [f"- **Claim:** {entry['claim']}"]
            if entry["falsifier"]:
                lines += [f"- **Falsifier:** {entry['falsifier']}"]
            if entry["evidence"]:
                evs = "; ".join(entry["evidence"])
                lines += [f"- **Evidence:** {evs}"]
            lines += [""]

    lines += [
        "---",
        "",
        "_NOMOS · ROOT0-ATTRIBUTION-v1.0 · CC-BY-ND-4.0_",
    ]
    return "\n".join(lines)

# ═══════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    args = sys.argv[1:]
    validate_only = "--validate-only" in args
    do_markdown   = "--markdown" in args
    do_stats      = "--stats" in args

    ok, results, root_hash, entries, facets = run_integrity(TREE)

    for verdict, name, detail in results:
        print(f"  {verdict:<5} {name}" + (f"  [{detail}]" if detail else ""))

    status_counts = {}
    for e in entries:
        status_counts[e["status"]] = status_counts.get(e["status"], 0) + 1

    print()
    print(f"  root:    {root_hash}")
    print(f"  nodes:   {len(list(walk(TREE)))}")
    print(f"  facets:  {len(facets)}")
    print(f"  entries: {len(entries)}")
    for s, n in sorted(status_counts.items()):
        print(f"           {s}: {n}")
    print()
    print(f"  RESULT:  {'ONTOLOGY_OK' if ok else 'ONTOLOGY_FAIL'}")
    print()

    if validate_only:
        sys.exit(0 if ok else 1)

    if do_stats:
        sys.exit(0)

    # Export JSON
    export = {"root": root_hash, "generated": datetime.now(timezone.utc).isoformat(), "tree": strip(TREE)}
    with open("ontology.json", "w", encoding="utf-8") as f:
        json.dump(export, f, ensure_ascii=False, indent=1)
    print("  exported: ontology.json")

    if do_markdown:
        md = generate_markdown(TREE, root_hash)
        with open("ontology.md", "w", encoding="utf-8") as f:
            f.write(md)
        print("  exported: ontology.md")

    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
