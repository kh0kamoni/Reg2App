import os
import json
import pytest
from benchmark.evaluation.evaluator import evaluate_predictions

BENCH_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "benchmark"))

def test_catalog_integrity():
    cat_path = os.path.join(BENCH_DIR, "specifications", "catalog.json")
    assert os.path.exists(cat_path), "catalog.json must exist"
    with open(cat_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["total_benchmarks"] == 30
    assert len(data["benchmarks"]) == 30
    for bm in data["benchmarks"]:
        assert bm["benchmark_id"].startswith("MB-")
        assert len(bm["name"]) > 5
        assert bm["category"] in ["NETWORK", "CRYPTO", "STORAGE", "MANIFEST", "DATAFLOW", "SDK", "HYBRID"]
        assert bm["expected_state"] in ["Supported", "PotentialNonConformance", "InsufficientEvidence", "NotApplicable"]

def test_ground_truth_consistency():
    gt_path = os.path.join(BENCH_DIR, "ground_truth", "ground_truth.json")
    cat_path = os.path.join(BENCH_DIR, "specifications", "catalog.json")
    with open(gt_path, "r", encoding="utf-8") as f:
        gt = json.load(f)
    with open(cat_path, "r", encoding="utf-8") as f:
        cat = json.load(f)
    
    assert gt["total_micro_benchmarks"] == 30
    assert len(gt["rules"]) == 12
    for bm in cat["benchmarks"]:
        b_id = bm["benchmark_id"]
        assert b_id in gt["matrix"]
        b_entry = gt["matrix"][b_id]
        assert b_entry["is_compliant"] == bm["is_compliant"]
        assert len(b_entry["rules"]) == 12
        target_rule = bm["targeted_rule"]
        assert target_rule in b_entry["rules"]
        assert b_entry["rules"][target_rule]["targeted"] is True

def test_evaluator_metric_computations():
    gt_path = os.path.join(BENCH_DIR, "ground_truth", "ground_truth.json")
    with open(gt_path, "r", encoding="utf-8") as f:
        gt = json.load(f)
    
    # 1. Oracle predictions
    oracle_preds = {}
    for bid, binfo in gt["matrix"].items():
        oracle_preds[bid] = {rid: rinfo["should_trigger_non_conformance"] for rid, rinfo in binfo["rules"].items()}
    res = evaluate_predictions(oracle_preds, gt_path)
    assert res["global_metrics"]["Precision"] == 1.0
    assert res["global_metrics"]["Recall"] == 1.0
    assert res["global_metrics"]["F1"] == 1.0

    # 2. Inject one FP and one FN
    imperfect_preds = {k: v.copy() for k, v in oracle_preds.items()}
    # MB-002 is compliant for RULE-NET-CLEARTEXT-01 (should be False). Set to True -> FP
    imperfect_preds["MB-002"]["RULE-NET-CLEARTEXT-01"] = True
    # MB-001 is non-compliant for RULE-NET-CLEARTEXT-01 (should be True). Set to False -> FN
    imperfect_preds["MB-001"]["RULE-NET-CLEARTEXT-01"] = False

    res_imp = evaluate_predictions(imperfect_preds, gt_path)
    assert res_imp["global_metrics"]["FP"] == 1
    assert res_imp["global_metrics"]["FN"] == 1
    assert res_imp["global_metrics"]["Precision"] < 1.0
    assert res_imp["global_metrics"]["Recall"] < 1.0
