#!/usr/bin/env python3
"""Article-local reproducibility runner for the Summa reconstruction pilot.

This tool orchestrates the published law CLI and inspects its documents. It
does not evaluate argument semantics itself.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPOSITORY = ROOT.parent
SUITE_PATH = ROOT / "suite.json"
PIN_PATH = ROOT / "source-pin.json"
TOOLCHAIN_PATH = REPOSITORY / "toolchain.lock.json"
EXPECTED_RUNTIME = "law.core/0.2.11"
EXPECTED_CLI_VERSION = "0.2.4"
EXPECTED_PLATFORM_PINS = {
    "@arxo/cli-darwin-arm64@0.2.4": "f92d66559467a23091c58e4d7cdf66666363e713c9b1b3b183e31ceff3c54433",
    "@arxo/cli-linux-x64@0.2.4": "cddf99123af2a8e85b886820b243636ed1eba8df8e64042617c173637f14c262",
}
STATUSES = {
    "VERIFIED_IN_PROFILE", "CONDITIONAL", "RECONSTRUCTED", "UNSUPPORTED",
    "NOT_VERIFIED", "INVALID_IN_PROFILE",
}
PREMISE_KINDS = {
    "source_principle", "conservative_definition", "verified_lemma",
    "reconstructed_bridge", "case_fact", "external_judgment",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_hash(value: Any) -> str:
    return sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                              separators=(",", ":")).encode("utf-8"))


def version_matches(command: dict[str, Any] | None, expected_hash: str) -> bool:
    if not isinstance(command, dict) or command.get("exitCode") != 0:
        return False
    try:
        value = json.loads(command.get("stdout", ""))
    except (TypeError, ValueError):
        return False
    if not isinstance(value, dict):
        return False
    binary_hash = value.get("binaryHash")
    return (value.get("tool") == EXPECTED_CLI_VERSION
            and binary_hash in {expected_hash, "sha256:" + expected_hash})


def platform_pins(lock: dict[str, Any]) -> dict[str, str]:
    """Return only exact, expected native package pins from the public lock."""
    if lock.get("tool") != EXPECTED_CLI_VERSION or lock.get("semantics") != EXPECTED_RUNTIME:
        raise ValueError("toolchain.lock.json tool or semantics version mismatch")
    found: dict[str, str] = {}
    for package in lock.get("packages", []):
        if not isinstance(package, dict):
            continue
        name, version, digest = package.get("name"), package.get("version"), package.get("binarySha256")
        key = f"{name}@{version}"
        if key in EXPECTED_PLATFORM_PINS:
            if digest != EXPECTED_PLATFORM_PINS[key]:
                raise ValueError(f"toolchain.lock.json digest mismatch for {key}")
            found[key] = digest
    if found != EXPECTED_PLATFORM_PINS:
        raise ValueError("toolchain.lock.json must pin both supported native CLI packages")
    return found


def values_for_key(value: Any, wanted: set[str]):
    if isinstance(value, dict):
        for key, child in value.items():
            if key in wanted:
                yield child
            yield from values_for_key(child, wanted)
    elif isinstance(value, list):
        for child in value:
            yield from values_for_key(child, wanted)


def run_command(law: Path, args: list[str], cwd: Path, timeout: int = 120,
                stdin_path: Path | None = None) -> dict[str, Any]:
    command = [str(law), *args]
    try:
        if stdin_path is None:
            p = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, timeout=timeout, check=False)
        else:
            with stdin_path.open("r", encoding="utf-8") as source:
                p = subprocess.run(command, cwd=cwd, stdin=source, text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   timeout=timeout, check=False)
        result = {"argv": command, "cwd": str(cwd), "exitCode": p.returncode,
                  "stdout": p.stdout, "stderr": p.stderr}
        if stdin_path is not None:
            result["stdinPath"] = str(stdin_path)
            result["stdinSha256"] = sha256(stdin_path.read_bytes())
        return result
    except subprocess.TimeoutExpired as e:
        return {"argv": command, "cwd": str(cwd), "exitCode": None,
                "stdout": e.stdout or "", "stderr": e.stderr or "",
                "error": f"timed out after {timeout}s"}
    except OSError as e:
        return {"argv": command, "cwd": str(cwd), "exitCode": None,
                "stdout": "", "stderr": "", "error": str(e)}


def command_json(record: dict[str, Any]) -> Any:
    try:
        return json.loads(record.get("stdout", ""))
    except (json.JSONDecodeError, TypeError):
        lines = [line for line in record.get("stdout", "").splitlines() if line.strip()]
        if not lines:
            return None
        try:
            return [json.loads(line) for line in lines]
        except (json.JSONDecodeError, TypeError):
            return None


def source_checks(article: str, source_json: Path, source_txt: Path,
                  pin: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {"ok": False, "errors": []}
    try:
        meta = json_read(source_json)
        raw = source_txt.read_bytes()
    except (OSError, ValueError) as e:
        result["errors"].append(str(e))
        return result
    pin_row = next((x for x in pin.get("inputs", []) if x.get("articleId") == article), None)
    section_text = "".join(s.get("text", "") for s in meta.get("sections", [])).encode("utf-8")
    checks = {
        "articleId": meta.get("articleId") == article,
        "pinnedEntryExists": pin_row is not None,
        "sourceFileMatchesPin": bool(pin_row) and meta.get("sourceFile") == pin_row.get("sourceFile"),
        "sourceProvenanceHashMatchesPin": bool(pin_row) and meta.get("sourceFileSha256") == pin_row.get("sha256"),
        "excerptBytesMatchSourceJson": raw == section_text,
        "excerptHashMatchesPin": bool(pin_row) and sha256(raw) == pin_row.get("excerptSha256"),
        "sectionHashesMatch": all(sha256(s.get("text", "").encode("utf-8")) == s.get("sha256")
                                   for s in meta.get("sections", [])),
    }
    result.update({"ok": all(checks.values()), "checks": checks,
                   "excerptBytes": len(raw), "excerptSha256": sha256(raw),
                   "fullSourceFileVerified": False, "fullSourceIntegrity": "PROVENANCE_ONLY",
                   "sourceSections": [s.get("id") for s in meta.get("sections", [])]})
    if not result["ok"]:
        result["errors"].append("One or more pinned excerpt checks failed")
    return result


def reconstruction_checks(article: str, base: Path, source_sections: list[str]) -> dict[str, Any]:
    rp = base / "reconstruction.json"
    result: dict[str, Any] = {"present": rp.is_file(), "ok": False, "errors": []}
    if not rp.is_file():
        result["errors"].append("reconstruction.json is not ready")
        return result
    try:
        data = json_read(rp)
    except (OSError, ValueError) as e:
        result["errors"].append(str(e))
        return result
    errs: list[str] = []
    if data.get("format") != "arxo.summa-argument-reconstruction/0.1": errs.append("unsupported format")
    if data.get("articleId") != article: errs.append("articleId mismatch")
    if not isinstance(data.get("modelSpec"), str) or not data["modelSpec"].strip(): errs.append("missing modelSpec")
    mapped: list[str] = []
    for entry in data.get("sourceSections", []):
        if not isinstance(entry, dict) or not isinstance(entry.get("section"), str):
            errs.append("invalid sourceSections entry")
            continue
        mapped.append(entry["section"])
        if not isinstance(entry.get("obligations"), list): errs.append(f"{entry['section']}: obligations must be a list")
    missing = sorted(set(source_sections) - set(mapped))
    unknown_sections = sorted(set(mapped) - set(source_sections))
    duplicates = sorted(x for x in set(mapped) if mapped.count(x) > 1)
    if missing: errs.append("unmapped source sections: " + ", ".join(missing))
    if unknown_sections: errs.append("unknown source sections: " + ", ".join(unknown_sections))
    if duplicates: errs.append("duplicate source sections: " + ", ".join(duplicates))
    ids: set[str] = set()
    obligations = data.get("obligations", [])
    if not isinstance(obligations, list): obligations = []; errs.append("obligations must be a list")
    for item in obligations:
        if not isinstance(item, dict): errs.append("invalid obligation entry"); continue
        oid = item.get("id")
        if not isinstance(oid, str) or not oid: errs.append("obligation missing id")
        elif oid in ids: errs.append(f"duplicate obligation id: {oid}")
        else: ids.add(oid)
        if item.get("status") not in STATUSES: errs.append(f"{oid or '?'}: invalid status")
        if not isinstance(item.get("statement"), str) or not item["statement"].strip(): errs.append(f"{oid or '?'}: missing statement")
        for field in ("sections", "tests", "dependsOn"):
            if not isinstance(item.get(field, []), list): errs.append(f"{oid or '?'}: {field} must be a list")
    for item in obligations:
        if isinstance(item, dict):
            for dep in item.get("dependsOn", []) if isinstance(item.get("dependsOn", []), list) else []:
                if dep not in ids: errs.append(f"{item.get('id', '?')}: unknown dependsOn id {dep}")
            for section in item.get("sections", []) if isinstance(item.get("sections", []), list) else []:
                if section not in source_sections: errs.append(f"{item.get('id', '?')}: unknown source section {section}")
    test_names = {p.name for p in (base / "tests").rglob("*.lawtest")} if (base / "tests").is_dir() else set()
    for entry in data.get("sourceSections", []):
        if isinstance(entry, dict):
            for oid in entry.get("obligations", []) if isinstance(entry.get("obligations", []), list) else []:
                if oid not in ids: errs.append(f"source section {entry.get('section')}: unknown obligation {oid}")
    for item in obligations:
        if isinstance(item, dict):
            for test in item.get("tests", []) if isinstance(item.get("tests", []), list) else []:
                if test not in test_names: errs.append(f"{item.get('id', '?')}: unknown test fixture {test}")
    premises = data.get("premises", [])
    premise_ids: set[str] = set()
    if not isinstance(premises, list): premises = []; errs.append("premises must be a list")
    for item in premises:
        if not isinstance(item, dict): errs.append("invalid premise entry"); continue
        pid = item.get("id")
        if not isinstance(pid, str) or not pid: errs.append("premise missing id")
        elif pid in premise_ids: errs.append(f"duplicate premise id: {pid}")
        else: premise_ids.add(pid)
        if item.get("kind") not in PREMISE_KINDS: errs.append(f"{pid or '?'}: invalid premise kind")
        for section in item.get("sections", []) if isinstance(item.get("sections", []), list) else []:
            if section not in source_sections: errs.append(f"{pid or '?'}: unknown source section {section}")
    replies = data.get("replyTargets", [])
    if not isinstance(replies, list): replies = []; errs.append("replyTargets must be a list")
    for item in replies:
        if not isinstance(item, dict): errs.append("invalid replyTargets entry"); continue
        if item.get("objection") not in source_sections: errs.append(f"reply {item.get('reply')}: unknown objection source section")
        if item.get("reply") not in source_sections: errs.append(f"unknown reply source section: {item.get('reply')}")
        for oid in item.get("obligations", []) if isinstance(item.get("obligations", []), list) else []:
            if oid not in ids: errs.append(f"reply {item.get('reply')}: unknown obligation {oid}")
    if not isinstance(data.get("protectedConclusions", []), list): errs.append("protectedConclusions must be a list")
    if not isinstance(data.get("limitations", []), list): errs.append("limitations must be a list")
    result.update({"ok": not errs, "errors": errs, "data": data,
                   "sectionCoverage": {"source": len(source_sections), "mapped": len(mapped),
                                       "missing": missing, "unknown": unknown_sections},
                   "obligationCount": len(obligations), "premiseCount": len(premises),
                   "openObligations": [x.get("id") for x in obligations if isinstance(x, dict)
                                       and x.get("status") in {"CONDITIONAL", "RECONSTRUCTED", "UNSUPPORTED", "NOT_VERIFIED", "INVALID_IN_PROFILE"}]})
    return result


def model_inputs(article_dir: Path) -> tuple[Path | None, list[Path]]:
    model_dir = article_dir / "model"
    law_files = sorted(model_dir.rglob("*.law")) if model_dir.is_dir() else []
    tests_dir = article_dir / "tests"
    fixtures = sorted(tests_dir.rglob("*.lawtest")) if tests_dir.is_dir() else []
    return (law_files[0] if law_files else None, fixtures)


def protected_relation_ids(conclusions: Any, ir: Any) -> dict[str, Any]:
    declarations = [n for n in ir.get("nodes", []) if isinstance(n, dict)
                    and n.get("kind") == "symbol_decl" and n.get("symbolKind") == "relation"] if isinstance(ir, dict) else []
    by_name: dict[str, list[str]] = {}
    ids = set()
    for declaration in declarations:
        symbol_id, name = declaration.get("id"), declaration.get("name")
        if isinstance(symbol_id, str): ids.add(symbol_id)
        if isinstance(symbol_id, str) and isinstance(name, str): by_name.setdefault(name, []).append(symbol_id)
    resolved: list[str] = []
    errors: list[str] = []
    if not isinstance(conclusions, list) or not conclusions:
        errors.append("protectedConclusions must be a non-empty list of relation symbols")
    else:
        for item in conclusions:
            if not isinstance(item, str) or not item.strip():
                errors.append(f"invalid protected conclusion entry: {item!r}")
            elif item in ids:
                resolved.append(item)
            elif item in by_name and len(by_name[item]) == 1:
                resolved.append(by_name[item][0])
            else:
                errors.append(f"protected conclusion {item!r} does not resolve to one declared relation symbol")
    return {"resolvedRelationIds": resolved, "metadataErrors": errors, "ok": not errors}


def assertion_literals(ir: Any, lowered_rows: list[Any]) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(ir, dict):
        for node in ir.get("nodes", []):
            if isinstance(node, dict) and node.get("kind") == "assertion" and isinstance(node.get("literal"), dict):
                found.append({"context": "compiled package assertion", "literal": node["literal"],
                              "assertionId": node.get("id")})
    for row in lowered_rows:
        if not isinstance(row, dict) or not isinstance(row.get("document"), dict): continue
        document = row["document"]
        for test in document.get("tests", []) if isinstance(document.get("tests"), list) else []:
            case = test.get("case", {}) if isinstance(test, dict) else {}
            for assertion in case.get("assertions", []) if isinstance(case, dict) and isinstance(case.get("assertions"), list) else []:
                if isinstance(assertion, dict) and isinstance(assertion.get("literal"), dict):
                    found.append({"context": "lowered test case assertion", "fixture": row.get("path"),
                                  "test": test.get("title"), "assertionId": assertion.get("id"),
                                  "literal": assertion["literal"]})
    return found


def inspect_protected(conclusions: Any, ir: Any, lowered_rows: list[Any]) -> dict[str, Any]:
    resolved = protected_relation_ids(conclusions, ir)
    protected = set(resolved["resolvedRelationIds"])
    hits = [entry for entry in assertion_literals(ir, lowered_rows)
            if entry["literal"].get("predicate") in protected]
    return {**resolved, "assertionCountInspected": len(assertion_literals(ir, lowered_rows)),
            "matches": hits, "ok": resolved["ok"] and not hits,
            "scope": "Only compiled package assertion nodes and lowered test case assertions; declarations, rule heads and query targets are excluded."}


def file_inventory(paths: list[Path], root: Path) -> list[dict[str, Any]]:
    return [{"path": p.relative_to(root).as_posix(), "sha256": sha256(p.read_bytes()), "bytes": p.stat().st_size}
            for p in paths]


def article_run(article: str, law: Path, out_dir: Path, pin: dict[str, Any]) -> dict[str, Any]:
    article_dir = ROOT / "articles" / article
    source = source_checks(article, article_dir / "source.json", article_dir / "source.txt", pin)
    rc = reconstruction_checks(article, article_dir, source.get("sourceSections", []))
    base: dict[str, Any] = {"articleId": article, "source": {k: v for k, v in source.items() if k != "sourceSections"},
                            "reconstruction": {k: v for k, v in rc.items() if k != "data"},
                            "commands": [], "status": "NOT_READY"}
    if not source.get("ok") or not rc.get("ok"):
        base["readinessErrors"] = source.get("errors", []) + rc.get("errors", [])
        return base
    data = rc["data"]
    model_dir = article_dir / "model"
    _, fixtures = model_inputs(article_dir)
    base["readiness"] = {"model": model_dir.is_dir(), "fixtures": len(fixtures)}
    if not model_dir.is_dir() or not list(model_dir.rglob("*.law")) or not fixtures:
        base["status"] = "NOT_READY"
        base["readinessErrors"] = (["model package is missing"] if not list(model_dir.rglob("*.law")) else []) + (["zero .lawtest fixtures"] if not fixtures else [])
        return base

    article_out = out_dir / article
    article_out.mkdir(parents=True, exist_ok=True)
    base["modelFiles"] = file_inventory(sorted(model_dir.rglob("*.law")), article_dir)
    base["testFiles"] = file_inventory(fixtures, article_dir)
    fixture_manifest = article_out / "test-files.json"
    fixture_manifest.write_text(json.dumps([str(p.resolve()) for p in fixtures], indent=2) + "\n", encoding="utf-8")
    base["artifacts"] = {"testFileList": {"path": str(fixture_manifest), "sha256": sha256(fixture_manifest.read_bytes())}}

    check = run_command(law, ["engine", "check", str(model_dir), "--json"], REPOSITORY)
    base["commands"].append(check)
    base["check"] = command_json(check)
    lower = run_command(law, ["engine", "lower", str(model_dir), "--exact-release", EXPECTED_RUNTIME], REPOSITORY)
    base["commands"].append(lower)
    ir: Any = None
    ir_path = article_out / "compiled-ir.json"
    try:
        if lower.get("exitCode") == 0:
            ir = json.loads(lower.get("stdout", ""))
            ir_path.write_text(json.dumps(ir, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    except (ValueError, OSError) as e:
        base["lowerParseError"] = str(e)
    base["lower"] = {"exitCode": lower.get("exitCode"), "stderr": lower.get("stderr", "")}
    if ir is not None:
        base["compiledIR"] = {"path": str(ir_path), "sha256": sha256(ir_path.read_bytes()), "bytes": ir_path.stat().st_size,
                              "semanticVersion": ir.get("semanticVersion")}

    deps = run_command(law, ["engine", "deps", str(model_dir), "--json", "--files", "--symbols", "--why"], REPOSITORY)
    base["commands"].append(deps)
    base["trustClosure"] = command_json(deps)
    if ir is None:
        base["status"] = "FAILED"
        base["failures"] = ["compiled IR unavailable"]
        return base

    lower_tests = run_command(law, ["engine", "lower-test", str(fixture_manifest), "--lawtest-list",
                                    "--program", str(ir_path)], REPOSITORY)
    base["commands"].append(lower_tests)
    lowered_rows = command_json(lower_tests)
    if not isinstance(lowered_rows, list): lowered_rows = []
    lowered_path = article_out / "lowered-tests.jsonl"
    lowered_path.write_text(lower_tests.get("stdout", ""), encoding="utf-8")
    base["artifacts"]["loweredTests"] = {"path": str(lowered_path), "sha256": sha256(lowered_path.read_bytes())}
    base["fixtureLowerings"] = [{"path": row.get("path"), "ok": isinstance(row.get("document"), dict),
                                  "error": row.get("error"), "document": row.get("document")}
                                 for row in lowered_rows if isinstance(row, dict)]
    lower_test_rows_ok = (lower_tests.get("exitCode") == 0 and len(lowered_rows) == len(fixtures)
                          and all(isinstance(row, dict) and isinstance(row.get("document"), dict)
                                  for row in lowered_rows))
    fixture_test_count = sum(len(row.get("document", {}).get("tests", [])) for row in lowered_rows
                             if isinstance(row, dict) and isinstance(row.get("document"), dict)
                             and isinstance(row.get("document", {}).get("tests"), list))

    tested = run_command(law, ["engine", "test", str(fixture_manifest), "--lawtest-list",
                               "--program", str(ir_path), "--json"], REPOSITORY)
    base["commands"].append(tested)
    test_summary = command_json(tested)
    base["testSummary"] = test_summary
    test_items = test_summary.get("tests", []) if isinstance(test_summary, dict) else []
    native_test_counts = {"total": test_summary.get("total") if isinstance(test_summary, dict) else None,
                          "passed": test_summary.get("passed") if isinstance(test_summary, dict) else None,
                          "failed": test_summary.get("failed") if isinstance(test_summary, dict) else None,
                          "loweredTests": fixture_test_count, "summaryItems": len(test_items) if isinstance(test_items, list) else 0}

    protection = inspect_protected(data.get("protectedConclusions"), ir, lowered_rows)
    base["protectedConclusionInspection"] = protection

    requests: list[dict[str, Any]] = []
    request_index: list[dict[str, Any]] = []
    for row in lowered_rows:
        if not isinstance(row, dict) or not isinstance(row.get("document"), dict): continue
        doc = row["document"]
        for ix, test in enumerate(doc.get("tests", []) if isinstance(doc.get("tests"), list) else []):
            if not isinstance(test, dict) or not isinstance(test.get("case"), dict) or not isinstance(test.get("query"), dict):
                continue
            steps = test.get("steps") if isinstance(test.get("steps"), list) else []
            if not steps:
                steps = [{"query": test["query"], "expectations": test.get("expectations", [])}]
            for step_index, step in enumerate(steps):
                query = step.get("query") if isinstance(step, dict) else None
                if not isinstance(query, dict): continue
                request = {"schemaVersion": "law.core.evaluation-request/0.2", "semanticVersion": ir.get("semanticVersion"),
                           "ir": ir, "case": test["case"], "query": query}
                requests.append(request)
                request_index.append({"fixture": row.get("path"), "testIndex": ix, "stepIndex": step_index,
                                      "title": test.get("title"), "queryId": query.get("queryId"),
                                      "expectations": step.get("expectations", []) if isinstance(step, dict) else []})
    request_path = article_out / "evaluation-requests.jsonl"
    request_path.write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in requests), encoding="utf-8")
    base["artifacts"]["evaluationRequests"] = {"path": str(request_path), "sha256": sha256(request_path.read_bytes()),
                                               "count": len(requests), "index": request_index}

    eval_runs = []
    for run_number in (1, 2):
        record = run_command(law, ["engine", "eval-batch"], REPOSITORY, stdin_path=request_path)
        base["commands"].append(record)
        docs = command_json(record)
        if isinstance(docs, dict): docs = [docs]
        if not isinstance(docs, list): docs = []
        docs_path = article_out / f"evaluations-run-{run_number}.jsonl"
        docs_path.write_text(record.get("stdout", ""), encoding="utf-8")
        run_docs = []
        for ix, doc in enumerate(docs):
            if not isinstance(doc, dict):
                run_docs.append({"document": doc, "measurement": "NOT_MEASURED", "reason": "not a JSON object"})
                continue
            has_result_hash = isinstance(doc.get("resultHash"), str) and bool(doc.get("resultHash"))
            run_docs.append({"document": doc, "resultHash": doc.get("resultHash"),
                             "outcomeHash": doc.get("outcomeHash"), "canonicalDocumentSha256": canonical_hash(doc),
                             "measurement": "MEASURED" if has_result_hash else "NOT_MEASURED",
                             "reason": None if has_result_hash else "canonical evaluation resultHash absent"})
        eval_runs.append({"run": run_number, "exitCode": record.get("exitCode"), "path": str(docs_path),
                          "rawOutputSha256": sha256(docs_path.read_bytes()), "documents": run_docs,
                          "documentCount": len(docs)})
    base["canonicalEvaluations"] = eval_runs
    deterministic = len(eval_runs) == 2 and len(requests) > 0 and all(
        r.get("exitCode") == 0 and len(r["documents"]) == len(requests)
        and all(x.get("measurement") == "MEASURED" for x in r["documents"])
        for r in eval_runs)
    comparison = []
    if deterministic:
        for ix, (first, second) in enumerate(zip(eval_runs[0]["documents"], eval_runs[1]["documents"])):
            outcome_hash_present = (isinstance(first.get("outcomeHash"), str) and bool(first.get("outcomeHash"))
                                    and isinstance(second.get("outcomeHash"), str) and bool(second.get("outcomeHash")))
            outcome_hash_match = (first.get("outcomeHash") == second.get("outcomeHash")) if outcome_hash_present else None
            same_result_hash = (isinstance(first.get("resultHash"), str) and bool(first.get("resultHash"))
                                and first.get("resultHash") == second.get("resultHash"))
            same_document_hash = (isinstance(first.get("canonicalDocumentSha256"), str)
                                  and bool(first.get("canonicalDocumentSha256"))
                                  and first.get("canonicalDocumentSha256") == second.get("canonicalDocumentSha256"))
            same = same_result_hash and same_document_hash and outcome_hash_match is not False
            comparison.append({**request_index[ix], "firstResultHash": first.get("resultHash"),
                               "secondResultHash": second.get("resultHash"), "firstOutcomeHash": first.get("outcomeHash"),
                               "secondOutcomeHash": second.get("outcomeHash"),
                               "outcomeHashComparison": "MATCH" if outcome_hash_match is True else "NOT_PROVIDED" if outcome_hash_match is None else "MISMATCH",
                               "firstCanonicalDocumentSha256": first.get("canonicalDocumentSha256"),
                               "secondCanonicalDocumentSha256": second.get("canonicalDocumentSha256"), "match": same})
    base["repeatedResultComparison"] = {"status": "MEASURED" if deterministic else "NOT_MEASURED",
                                        "allMatch": bool(comparison) and all(x["match"] for x in comparison),
                                        "items": comparison,
                                        "limitation": None if deterministic else "One or more native canonical evaluation documents or resultHash values were unavailable."}

    evaluation_docs = [item.get("document") for run in eval_runs for item in run.get("documents", [])
                       if isinstance(item.get("document"), dict)]
    proof_graphs = [doc.get("proofGraph") for doc in evaluation_docs if isinstance(doc.get("proofGraph"), dict)]
    skipped_rules = [item for doc in evaluation_docs for value in values_for_key(doc, {"skippedRules"})
                     for item in (value if isinstance(value, list) else [])]
    anchors = [item for graph in proof_graphs for node in graph.get("nodes", []) if isinstance(node, dict)
               for item in (node.get("sourceAnchors", []) if isinstance(node.get("sourceAnchors"), list) else [])]
    surfaced_faults = [item for doc in evaluation_docs for value in values_for_key(doc, {"faults", "errors", "issues", "resourceRefusals"})
                       for item in (value if isinstance(value, list) else [])]
    base["evidenceInspection"] = {"ruleNodes": [node for graph in proof_graphs for node in graph.get("nodes", [])
                                                  if isinstance(node, dict) and node.get("kind") == "rule_application"],
                                  "sourceAnchors": anchors, "skippedRules": skipped_rules,
                                  "proofGraphs": proof_graphs, "surfacedFaults": surfaced_faults,
                                  "note": "These fields are retained from native canonical evaluation documents, never inferred from test summaries."}

    test_summary_ok = (tested.get("exitCode") == 0 and isinstance(test_summary, dict)
                       and test_summary.get("ok") is True and test_summary.get("failed") == 0
                       and test_summary.get("total") == fixture_test_count
                       and test_summary.get("passed") == fixture_test_count and fixture_test_count > 0)
    check_ok = check.get("exitCode") == 0 and isinstance(base.get("check"), dict) and base["check"].get("ok") is True
    checks = {"check": check_ok,
              "lower": lower.get("exitCode") == 0 and ir is not None,
              "dependencyInventory": deps.get("exitCode") == 0,
              "lowerTests": lower_test_rows_ok and fixture_test_count > 0,
              "testExpectations": test_summary_ok,
              "canonicalEvaluationMeasurements": deterministic,
              "canonicalRepeatedHashesMatch": bool(comparison) and all(x["match"] for x in comparison),
              "protectedConclusionGuard": protection.get("ok") is True,
              "noSkippedRules": not skipped_rules}
    failures = [name for name, passed in checks.items() if not passed]
    base["counts"] = {"modelFiles": len(base["modelFiles"]), "testFixtures": len(fixtures),
                      "scenariosLowered": fixture_test_count, "queryStepsEvaluated": len(requests),
                      "scenariosPassed": native_test_counts["passed"],
                      "scenariosFailed": native_test_counts["failed"], "nativeEvaluationDocuments": len(eval_runs[0]["documents"]),
                      "checkExitCode": check.get("exitCode"), "testSummary": native_test_counts}
    base["observedChecks"] = {**checks, "necessaryOpenObligations": rc.get("openObligations", []),
                              "authorDeclaredFullArticleVerified": bool(data.get("fullArticleVerified", False)),
                              "fullArticleVerified": False, "promotionApplied": False}
    base["failures"] = failures
    base["status"] = "EXECUTED" if not failures else "FAILED"
    return base


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--article", action="append", help="article ID; repeatable")
    parser.add_argument("--all-selected", action="store_true", help="run the seven articles pinned in suite.json")
    parser.add_argument("--law-bin", required=True, help="absolute path to the exact published law CLI")
    parser.add_argument("--out", required=True, help="absolute output directory outside this public repository")
    parser.add_argument("--readiness-only", action="store_true", help="allow exit zero when selected article inputs are not ready")
    args = parser.parse_args()
    if bool(args.article) == bool(args.all_selected):
        parser.error("choose repeated --article or --all-selected")
    out_arg = Path(args.out)
    law_arg = Path(args.law_bin)
    if not out_arg.is_absolute() or not law_arg.is_absolute(): parser.error("--out and --law-bin must be absolute paths")
    out = out_arg.resolve()
    law = law_arg.resolve()
    if out == REPOSITORY or REPOSITORY in out.parents: parser.error("--out must be outside the public repository")
    try:
        suite = json_read(SUITE_PATH)
        pin = json_read(PIN_PATH)
        lock = json_read(TOOLCHAIN_PATH)
        public_pins = platform_pins(lock)
    except (OSError, ValueError) as e:
        parser.error(f"cannot read or validate public pins: {e}")
    allowed = suite.get("order", [])
    if not isinstance(allowed, list) or len(allowed) != 7 or len(set(allowed)) != 7:
        parser.error("suite.json must pin exactly seven distinct articles")
    selected = allowed if args.all_selected else args.article
    unknown = [x for x in selected if x not in allowed]
    if unknown: parser.error("article ID outside pinned seven-article suite: " + ", ".join(unknown))
    selected = list(dict.fromkeys(selected))
    out.mkdir(parents=True, exist_ok=True)
    cli_hash = sha256(law.read_bytes()) if law.is_file() else None
    selected_platform = next((name for name, digest in public_pins.items() if cli_hash == digest), None)
    pinned_cli_hash = public_pins.get(selected_platform) if selected_platform else None
    cli_pin_matches = selected_platform is not None
    # Verify executable bytes before invoking even the informational version command.
    version = run_command(law, ["version", "--json"], REPOSITORY) if cli_pin_matches else None
    cli_version_matches = version_matches(version, pinned_cli_hash) if cli_pin_matches else False
    report = {
        "format": "arxo.summa-reconstruction-run/0.1",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "suite": str(SUITE_PATH.relative_to(REPOSITORY)),
        "selectedArticles": selected,
        "runtime": {"selection": "published CLI explicitly supplied", "cliPath": str(law),
                    "cliSha256": cli_hash, "expectedCliSha256": pinned_cli_hash,
                    "cliPinMatches": cli_pin_matches,
                    "cliVersionMatches": cli_version_matches,
                    "platformPackage": selected_platform,
                    "platformPinSource": "public toolchain.lock.json",
                    "publicRuntimeProvenance": "UNPINNED_FROM_CORPUS_LOCKSET",
                    "historicalOriginPin": pin.get("toolchain", {}).get("platformPackage"),
                    "launcherSha256RecordedOnly": pin.get("toolchain", {}).get("launcherSha256"),
                    "versionCommand": version, "expectedExactRelease": EXPECTED_RUNTIME,
                    "corpusLocksetStatus": "UNPINNED_FROM_CORPUS_LOCKSET",
                    "cargoFallback": False},
        "scope": {"coreChanges": False, "fullCorpus": "not_checked", "published": False,
                  "releaseVerified": False, "typeSystemAcceptance": "not_claimed"},
        "articles": [],
    }
    for article in selected:
        if not cli_pin_matches:
            report["articles"].append({"articleId": article, "status": "CLI_PIN_MISMATCH",
                                       "commands": [], "failures": ["CLI hash mismatch; no CLI command was executed."]})
        elif not cli_version_matches:
            report["articles"].append({"articleId": article, "status": "CLI_VERSION_MISMATCH",
                                       "commands": [], "failures": ["Pinned executable did not report the pinned CLI version and binaryHash; no article command was executed."]})
        else:
            report["articles"].append(article_run(article, law, out, pin))
    report_path = out / "report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(report_path), "selected": selected,
                      "statuses": {x["articleId"]: x["status"] for x in report["articles"]},
                      "cliPinMatches": report["runtime"]["cliPinMatches"],
                      "cliVersionMatches": report["runtime"]["cliVersionMatches"]}, ensure_ascii=False))
    statuses = {x["status"] for x in report["articles"]}
    if statuses == {"EXECUTED"}:
        return 0
    readiness_statuses = {"NOT_READY", "MODEL_NOT_READY"}
    if args.readiness_only and statuses and statuses <= readiness_statuses:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
