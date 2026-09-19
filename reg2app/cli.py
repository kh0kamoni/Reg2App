import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import argparse
import json
from reg2app.engine.evaluator import ComplianceEvaluator
from reg2app.analyzers.manifest_analyzer import ManifestAnalyzer
from reg2app.analyzers.crypto_analyzer import CryptoAnalyzer
from reg2app.analyzers.storage_analyzer import StorageAnalyzer
from reg2app.analyzers.network_analyzer import NetworkAnalyzer
from reg2app.analyzers.sdk_analyzer import SDKAnalyzer
from reg2app.analyzers.dataflow_engine import DataflowEngine
from reg2app.analyzers.apk_extractor import APKExtractor
from reg2app.reporting.localized_reporter import LocalizedReporter

def run_audit(context: dict, package_name="com.example.bank", sector="MFS"):
    manifest_an = ManifestAnalyzer(package_name, "mock_sha256")
    crypto_an = CryptoAnalyzer(package_name, "mock_sha256")
    storage_an = StorageAnalyzer(package_name, "mock_sha256")
    network_an = NetworkAnalyzer(package_name, "mock_sha256")
    sdk_an = SDKAnalyzer(package_name, "mock_sha256")
    dataflow_an = DataflowEngine(package_name, "mock_sha256")

    evidences = []
    if "manifest" in context:
        evidences.extend(manifest_an.analyze(context["manifest"]))
    if "dex" in context:
        evidences.extend(crypto_an.analyze(context["dex"]))
    if "storage" in context:
        evidences.extend(storage_an.analyze(context["storage"]))
    if "network" in context:
        evidences.extend(network_an.analyze(context["network"]))
    if "sdk" in context:
        evidences.extend(sdk_an.analyze(context["sdk"]))
    if "dataflow" in context:
        evidences.extend(dataflow_an.analyze(context["dataflow"]))

    evaluator = ComplianceEvaluator()
    result = evaluator.evaluate(evidences, app_package=package_name, app_sector=sector)
    return result

def audit_apk(apk_path: str, sector: str = "MFS"):
    extractor = APKExtractor(apk_path)
    ctx = extractor.build_full_context()
    ctx["manifest"]["declared_category"] = sector
    return run_audit(ctx, package_name=ctx["package_name"], sector=sector)

def main():
    parser = argparse.ArgumentParser(description="Reg2App: Evidence-Based Regulatory Compliance Analyzer")
    parser.add_argument("--apk", help="Path to real Android application (.apk or .apks)")
    parser.add_argument("--package", default="com.bd.fintech.app", help="Application package name")
    parser.add_argument("--sector", default="MFS", help="Application sector (MFS, BANKING, GENERAL)")
    parser.add_argument("--format", default="summary", choices=["summary", "json", "report-en", "report-bn"], help="Output format")
    args = parser.parse_args()

    if args.apk:
        result = audit_apk(args.apk, sector=args.sector)
    else:
        sample_context = {
            "manifest": {
                "application": {"usesCleartextTraffic": False, "allowBackup": False, "debuggable": False},
                "permissions": ["android.permission.INTERNET", "android.permission.READ_PHONE_STATE"],
                "declared_category": args.sector,
                "exported_components": []
            },
            "dex": {
                "ciphers": [{"transformation": "AES/GCM/NoPadding", "class_name": "CryptoUtil.dex"}],
                "hashes": [{"algorithm": "SHA-256", "class_name": "HashUtil.dex"}],
                "keystore_usage": True
            },
            "storage": {"encrypted_shared_preferences_used": True},
            "network": {"network_security_config": {"cleartextTrafficPermitted": False}},
            "sdk": {"third_party_packages": []},
            "dataflow": {"safe_network_transmission": True, "clean_logging": True}
        }
        result = run_audit(sample_context, package_name=args.package, sector=args.sector)

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.format == "report-en":
        print(LocalizedReporter.generate_report(result, condition="B"))
    elif args.format == "report-bn":
        print(LocalizedReporter.generate_report(result, condition="C"))
    else:
        print("=== Reg2App Compliance Assessment ===")
        print(f"Package: {result['application']['package_name']} (Sector: {result['application']['sector']})")
        print("Profile:", result["summary_profile"])
        print("Metrics:", result["metrics"])

if __name__ == "__main__":
    main()
