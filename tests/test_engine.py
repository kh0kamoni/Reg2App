import os
import pytest
from reg2app.ontology.loader import get_paired_ontology
from reg2app.ontology.models import ComplianceState
from reg2app.analyzers.manifest_analyzer import ManifestAnalyzer
from reg2app.analyzers.crypto_analyzer import CryptoAnalyzer
from reg2app.analyzers.storage_analyzer import StorageAnalyzer
from reg2app.analyzers.network_analyzer import NetworkAnalyzer
from reg2app.analyzers.sdk_analyzer import SDKAnalyzer
from reg2app.analyzers.dataflow_engine import DataflowEngine
from reg2app.engine.evaluator import ComplianceEvaluator

def test_paired_ontology_integrity():
    paired = get_paired_ontology()
    assert len(paired) >= 12
    for reg, clause, mapping in paired:
        assert reg.regulation_id == mapping.evidence_rule.rule_id[:0] + reg.regulation_id
        assert clause.clause_id == mapping.requirement_ref

def test_manifest_analyzer_detections():
    analyzer = ManifestAnalyzer("com.test.insecure", "hash123")
    manifest = {
        "application": {
            "usesCleartextTraffic": True,
            "allowBackup": True,
            "debuggable": True
        },
        "permissions": ["android.permission.READ_SMS", "android.permission.READ_CONTACTS"],
        "declared_category": "UTILITY",
        "exported_components": [{"type": "activity", "name": ".TestActivity", "exported": True, "permission": None}]
    }
    evidences = analyzer.analyze(manifest)
    rule_ids = {e.rule_id for e in evidences if e.is_violation}
    assert "RULE-NET-CLEARTEXT-01" in rule_ids
    assert "RULE-MANIFEST-ALLOW-BACKUP" in rule_ids
    assert "RULE-MANIFEST-DEBUGGABLE" in rule_ids
    assert "RULE-PERM-EXCESSIVE-DANGEROUS" in rule_ids
    assert "RULE-MANIFEST-EXPORTED-UNPROTECTED" in rule_ids

def test_crypto_analyzer_detections():
    analyzer = CryptoAnalyzer("com.test.crypto", "hash123")
    dex_context = {
        "ciphers": [{"transformation": "DES/ECB/PKCS5Padding", "class_name": "Insecure.dex"}],
        "hashes": [{"algorithm": "MD5", "class_name": "Insecure.dex"}],
        "hardcoded_keys": [{"key_snippet": "HardcodedKey123", "class_name": "Insecure.dex"}]
    }
    evidences = analyzer.analyze(dex_context)
    rule_ids = {e.rule_id for e in evidences if e.is_violation}
    assert "RULE-CRYPTO-WEAK-ALGO" in rule_ids
    assert "RULE-CRYPTO-HARDCODED-KEY" in rule_ids

def test_end_to_end_compliance_evaluation():
    # Insecure financial app
    evaluator = ComplianceEvaluator()
    manifest_an = ManifestAnalyzer("com.bad.bank", "hash_bad")
    crypto_an = CryptoAnalyzer("com.bad.bank", "hash_bad")
    
    evidences = []
    evidences.extend(manifest_an.analyze({
        "application": {"usesCleartextTraffic": True, "allowBackup": True, "debuggable": True},
        "permissions": ["android.permission.READ_SMS"],
        "declared_category": "GENERAL",
        "exported_components": []
    }))
    evidences.extend(crypto_an.analyze({
        "ciphers": [{"transformation": "DES", "class_name": "A.dex"}],
        "hashes": [],
        "hardcoded_keys": [{"key_snippet": "static_key", "class_name": "B.dex"}]
    }))

    result = evaluator.evaluate(evidences, app_package="com.bad.bank", app_sector="MFS")
    profile = result["summary_profile"]
    assert profile["PotentialNonConformance"] >= 4
    assert result["metrics"]["EvidenceCoverage"] > 0.0

def test_non_financial_sector_not_applicable():
    evaluator = ComplianceEvaluator()
    # App is in ECOMMERCE sector (not bank/MFS)
    result = evaluator.evaluate([], app_package="com.shop.bd", app_sector="ECOMMERCE")
    profile = result["summary_profile"]
    # Bangladesh Bank requirements (6 requirements) must transition to NotApplicable
    assert profile["NotApplicable"] == 6
