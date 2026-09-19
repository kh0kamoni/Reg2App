import os
import csv
import json
import pytest
from study.executions.batch_runner import execute_batch_study
from study.statistics.analyze_results import run_statistical_analysis
from reg2app.reporting.localized_reporter import LocalizedReporter
from user_study.analysis.evaluate_user_study import simulate_and_evaluate_user_study

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def test_seed_manifest_and_sectors():
    manifest_path = os.path.join(BASE_DIR, "study", "manifests", "seed_manifest.csv")
    assert os.path.exists(manifest_path)
    with open(manifest_path, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    assert len(reader) >= 20
    sectors = {r["sector"] for r in reader}
    assert "MFS" in sectors
    assert "BANKING" in sectors
    assert "ECOMMERCE" in sectors
    assert "GOVERNMENT" in sectors

def test_batch_runner_and_statistics():
    index_path = os.path.join(BASE_DIR, "study", "results", "study_execution_index.json")
    if not os.path.exists(index_path):
        execute_batch_study()
    assert os.path.exists(index_path)

    stats = run_statistical_analysis(index_path)
    assert stats["dataset_summary"]["total_applications_analyzed"] >= 20
    assert "rq5_sectoral_disparity" in stats
    assert stats["rq5_sectoral_disparity"]["statistically_significant"] is True

def test_localized_reporter_conditions():
    sample_audit = {
        "application": {"package_name": "com.test.app", "sector": "MFS"},
        "summary_profile": {"Supported": 8, "PotentialNonConformance": 2, "InsufficientEvidence": 1, "NotObservable": 0, "NotApplicable": 0},
        "metrics": {"EvidenceCoverage": 0.90, "EvidenceSupportedCompliance": 0.80},
        "provenance_records": [
            {
                "rule_id": "RULE-NET-CLEARTEXT-01",
                "regulation_title": "Bangladesh Bank CSF v1.0",
                "clause_id": "BB-CSF-4.1.3.12",
                "control_name": "Mandatory TLS",
                "obligation": "Network Security",
                "property_name": "No Cleartext HTTP",
                "evidence": {
                    "is_violation": True,
                    "component_type": "MANIFEST",
                    "file_path": "AndroidManifest.xml",
                    "extracted_value": "usesCleartextTraffic='true'",
                    "strength": "HIGH",
                    "description": "Cleartext traffic permitted"
                }
            }
        ]
    }
    # Condition A
    report_a = LocalizedReporter.generate_report(sample_audit, condition="A")
    assert "RAW_DIAGNOSTIC_TRACE" in report_a
    assert "RULE-NET-CLEARTEXT-01" in report_a

    # Condition B
    report_b = LocalizedReporter.generate_report(sample_audit, condition="B")
    assert "Reg2App Technical Regulatory Compliance Report" in report_b
    assert "Evidence Coverage" in report_b
    assert "Finding 1: Mandatory TLS" in report_b

    # Condition C
    report_c = LocalizedReporter.generate_report(sample_audit, condition="C")
    assert "?????????" in report_c
    assert "????? ????????????" in report_c
    assert "??????? ????????? ???????" in report_c

def test_user_study_evaluation():
    res = simulate_and_evaluate_user_study()
    assert res["participants"] == 60
    assert res["hypothesis_testing_C_vs_A"]["supported"] is True
    assert res["hypothesis_testing_C_vs_A"]["t_statistic"] > 5.0
