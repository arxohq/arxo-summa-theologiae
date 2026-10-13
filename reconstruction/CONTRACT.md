# Summa argument reconstruction on the existing runtime

This experimental layer is owned by the corpus repository. It does not change
the published structural models, their registries, or the engine. The seven
articles and the held-out criterion were pinned before model implementation in
`suite.json` and `source-pin.json`. The six initial articles include II–II q.64
a.7 once. I q.2 a.3 is a seventh, contrasting control, not a prescribed failure.

## Deliverables per article

Each `articles/<id>/` contains immutable `source.txt` and `source.json`, a
standalone `model/` with a `00-package.law`, declared scenarios in `tests/`,
`reconstruction.json`, and an English `README.md`. No imports from the old
argument graphs: their directly asserted theses and opaque premises would
contaminate the new trust base. Do not assert the conclusion under test.

`reconstruction.json` has this project-specific shape:

```json
{
  "format": "arxo.summa-argument-reconstruction/0.1",
  "articleId": "ii-ii-q64-a7",
  "modelSpec": "la.aquinas.reconstruct.ii_ii_q64_a7@0.1.0",
  "sourceSections": [{"section": "arg. 1", "obligations": ["ad1-scope"]}],
  "premises": [{"id": "p1", "kind": "source_principle", "sections": ["co."], "statement": "...", "formalSymbols": ["..."]}],
  "obligations": [{"id": "ad1-scope", "statement": "...", "sections": ["arg. 1", "ad 1"], "status": "CONDITIONAL", "reason": "...", "formalSymbols": ["..."], "tests": ["01-example.lawtest"], "dependsOn": []}],
  "replyTargets": [{"reply": "ad 1", "objection": "arg. 1", "target": "...", "mechanism": "...", "obligations": ["ad1-scope"]}],
  "protectedConclusions": ["..."],
  "limitations": ["..."],
  "fullArticleVerified": false
}
```

All source sections must be accounted for, including sed contra, every
objection and reply, and every one of the Five Ways in the control. Section
mapping is a source inventory, not a claim that a transition was verified.
Premise kinds: `source_principle`, `conservative_definition`, `verified_lemma`,
`reconstructed_bridge`, `case_fact`, `external_judgment`. A verified lemma must
identify its checked evidence and trust closure; none is assumed in advance.

Obligation statuses: `VERIFIED_IN_PROFILE`, `CONDITIONAL`, `RECONSTRUCTED`,
`UNSUPPORTED`, `NOT_VERIFIED`, `INVALID_IN_PROFILE`. Authors may initially use
`NOT_VERIFIED` for runnable obligations; the coordinator only promotes these
after execution and semantic review. A conditional obligation remains
conditional when its runtime scenario passes. `INVALID_IN_PROFILE` requires a
checked counterexample to the exact reconstruction, not a failure to express it.

## Execution and acceptance

Use named, substantive relations, explicit negative facts, intermediate
conclusions, and source-anchored rules. Unknown is not false. External practical
judgment keeps `adjudicated` provenance. Separate runs with different accepted
premises demonstrate conditional dependence; they do not implement hypothesis
discharge. A finite causal chain does not prove a universal no-regress principle.
No `proof_valid`, `reply_successful`, `no_infinite_regress`, or equivalent
conclusion-shaped fact may close an unsupported obligation.

Baseline truth, argumentation acceptance, and properties certified by a checker
are distinct claims. For argumentation v1, inspect and retain `skippedRules`;
essential skipped rules and resource refusals block acceptance. Do not engineer
priorities simply to make replies win. Source-attested principles are still
declared philosophical premises, not independently established truths.

Every implemented branch needs a positive scenario and a meaningful removal,
negative, conflict, or scope mutation. Test a particular branch's disappearance
when an alternative proof survives. Record proof rules and source anchors when
available, deterministic canonical documents, and repeated result hashes. The
runner marshals inputs and inspects runtime results; it must not implement a
second subject evaluator or use a Boolean oracle copied from the model.

Full article acceptance requires all predeclared necessary obligations to be
closed, with no hidden bridge premises. An open obligation blocks that claim and
all dependent claims, but independent checks continue. A passed test is evidence
of current-runtime behavior, not a proof of Aquinas's theological assumptions or
a certificate of the entire engine. Tests remain article-local. The full corpus
stays `not_checked`; this work is not a public release.
