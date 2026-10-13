#!/usr/bin/env python3
"""Check the exported reconstruction kit and its native reader examples only."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "reconstruction"


def run(law, *args):
    process = subprocess.run([law, *map(str, args)], capture_output=True, text=True, check=True)
    return json.loads(process.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--law", default="law")
    parser.add_argument("--evidence", type=Path, help="fresh seven-article runner output directory")
    args = parser.parse_args()
    version = run(args.law, "version", "--json")
    pin = json.loads((ROOT / "toolchain.lock.json").read_text())
    assert version["tool"] == pin["tool"]
    admitted = {"sha256:" + p["binarySha256"] for p in pin["packages"] if "binarySha256" in p}
    assert version["binaryHash"] in admitted
    models = json.loads((KIT / "models.json").read_text())
    assert len(models) == 7
    by_article = {}
    for model in models:
        raw = (KIT / model["program"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == model["programSha256"]
        program = json.loads(raw)
        assert program["package"]["name"] + "@" + program["package"]["version"] == model["spec"]
        assert program["semanticVersion"] == "0.2.11" and not program.get("imports")
        for file in model["modelSources"] + model["fixtures"]:
            source = KIT / "articles" / model["articleId"] / file["path"]
            assert hashlib.sha256(source.read_bytes()).hexdigest() == file["sha256"]
        by_article[model["articleId"]] = program
    if args.evidence:
        evidence = json.loads((args.evidence / "report.json").read_text())
        assert set(evidence["selectedArticles"]) == set(by_article)
        assert len(evidence["articles"]) == 7
        model_rows = {m["articleId"]: m for m in models}
        for article in evidence["articles"]:
            assert article["status"] == "EXECUTED" and not article["failures"]
            assert article["counts"]["scenariosFailed"] == 0
            assert article["repeatedResultComparison"]["allMatch"]
            assert article["protectedConclusionInspection"]["ok"]
            assert article["compiledIR"]["sha256"] == model_rows[article["articleId"]]["programSha256"]
        assert sum(a["counts"]["scenariosPassed"] for a in evidence["articles"]) == 73
        assert sum(a["counts"]["nativeEvaluationDocuments"] for a in evidence["articles"]) == 132
    examples = json.loads((KIT / "examples/index.json").read_text())
    for example in examples:
        folder = KIT / "examples" / example["name"]
        request = json.loads((folder / "request.json").read_text())
        expected = json.loads((folder / "result.json").read_text())
        assert request["ir"] == by_article[example["articleId"]]
        assert request["case"] == json.loads((folder / "case.json").read_text())
        assert request["query"] == json.loads((folder / "query.json").read_text())
        assert expected["resultHash"] == example["resultHash"]
        assert run(args.law, "eval", folder) == expected, example["name"]
        print("RECONSTRUCTION REPLAY PASS", example["name"], expected["resultHash"])
    acceptance = json.loads((KIT / "reports/acceptance.json").read_text())
    assert acceptance["scope"]["fullArticlesVerified"] == 0
    assert acceptance["obligationTotals"] == {"VERIFIED_IN_PROFILE": 21, "CONDITIONAL": 22,
                                             "RECONSTRUCTED": 32, "UNSUPPORTED": 15}
    assert all(not a["fullArticleVerified"] for a in acceptance["articles"])
    print("PUBLIC RECONSTRUCTION PASS; models", len(models), "examples", len(examples))


if __name__ == "__main__":
    main()
