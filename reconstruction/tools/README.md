# Article-local verification runner

`verify.py` checks pinned article excerpts, validates the reconstruction
inventory, and records commands and documents returned by the explicitly
supplied published CLI. It contains no Summa subject evaluator and does not
rewrite author files or obligation statuses.

Install the published CLI and use its launcher to locate the actual native
executable. The runner accepts only the Darwin arm64 or Linux x64 executable
whose raw SHA-256 appears in the public repository's `toolchain.lock.json`.
It checks those bytes before invoking `version --json`, then checks reported
version `0.2.4` and the matching `binaryHash`. The npm JavaScript launcher is
not the measured runtime; there is no launcher substitution or Cargo fallback.

```sh
npm install -g @arxo/cli@0.2.4
LAW_RECON_BIN="$(node --input-type=module -e '
  const { locateBinary } = await import(process.argv[2]);
  const found = locateBinary();
  if (found.error) throw new Error(found.error);
  console.log(found.binary);
' -- locate-native "$(npm root -g)/@arxo/cli/bin/law.js")"
python3 reconstruction/tools/verify.py \
  --article ii-ii-q64-a7 \
  --law-bin "$LAW_RECON_BIN" \
  --out /tmp/arxo-summa-q64-evidence
```

Repeat `--article <id>` for selected articles, or use `--all-selected` to select
exactly the seven IDs in `suite.json`. `--out` and `--law-bin` must be absolute;
the output directory must be outside this public repository.

When files are ready, the runner records `engine check`, `engine lower
--exact-release law.core/0.2.11`, `engine deps`, batch `engine lower-test
--lawtest-list`, and `engine test --lawtest-list`. It evaluates each lowered
fixture case/query twice through `engine eval-batch`, retaining native
canonical evaluation documents and their `resultHash`/`outcomeHash` when
supplied. Test-summary JSON is kept for expectation counts, never used as
evaluation evidence. The report preserves stdout/stderr, exit codes, scenario
counts, compiled IR hash, trust/import inventory, proofs, source anchors,
skipped rules, and surfaced faults.

Excerpt hashes and section inventory establish local excerpt integrity. The
complete source-file byte count and digest are provenance fields; the runner
cannot claim a local full-file integrity pass. The source metadata's original
toolchain note records its corpus origin, while public execution is independently
pinned by `toolchain.lock.json` and reports
`UNPINNED_FROM_CORPUS_LOCKSET`. Protected conclusions must resolve to declared
relation symbols; the guard inspects compiled package assertions and lowered
test case assertions, excluding declarations, rule heads, and query targets.
Passing tests do not promote obligations, and this runner never asserts
full-article or full engine acceptance.
