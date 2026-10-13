# Native reconstruction examples

From the repository root, run `law eval reconstruction/examples/<name>`.
Install `@arxo/cli@0.2.4` through npm first. Every directory contains its exact
request, case, query and recorded native result. CLI output keeps both evaluation
status and truth status; argumentation answers also keep their acceptance class.

| Example | Observed answer | What it exposes |
|---|---|---|
| [intended-death-objection](intended-death-objection) | `SKEPTICALLY_ACCEPTED` | Intended death supports the scoped objection |
| [incidental-death-reply](incidental-death-reply) | `REJECTED` | Explicit non-intention defeats that objection |
| [conditional-defense](conditional-defense) | `COMPUTED / TRUE_ONLY` | Permission under declared premises and adjudicated proportionality |
| [defense-awaits-judgment](defense-awaits-judgment) | `REQUIRES_JUDGMENT / NEITHER` | Missing practical assessment remains a request |
| [conflicting-proportionality](conflicting-proportionality) | `COMPUTED / BOTH` | Conflicting findings remain visible |
| [conflict-blocks-permission](conflict-blocks-permission) | `COMPUTED / NEITHER` | Conservative dependent conclusion is not established |
| [clerical-irregularity](clerical-irregularity) | `COMPUTED / TRUE_ONLY` | Irregularity is separate from moral culpability |
| [common-happiness-with-bridge](common-happiness-with-bridge) | `COMPUTED / TRUE_ONLY` | The common-happiness route uses an explicit bridge |
| [common-happiness-without-bridge](common-happiness-without-bridge) | `COMPUTED / NEITHER` | Removing the bridge blocks its dependent conclusion |
| [canonical-authority-category](canonical-authority-category) | `COMPUTED / TRUE_ONLY` | A supplied source classification retains its category |
| [finite-actualization](finite-actualization) | `COMPUTED / TRUE_ONLY` | A target-state witness under declared principles |
| [first-mover-not-established](first-mover-not-established) | `COMPUTED / NEITHER` | That witness does not establish a first mover |
| [self-cause-order-conflict](self-cause-order-conflict) | `COMPUTED / BOTH` | Self-cause conflicts with stipulated order irreflexivity |

The results are finite model consequences. They do not certify theological
premises, universal regress termination or complete article formalization.
Original native proof `sourceAnchors` may be empty; use the pinned Latin excerpts,
model annotations and per-article reconstruction ledger for provenance.
