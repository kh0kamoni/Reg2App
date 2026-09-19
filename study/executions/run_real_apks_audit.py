import os
import sys
import glob
import json
import csv
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from reg2app.analyzers.apk_extractor import APKExtractor
from reg2app.cli import run_audit

# Canonical metadata mapping for the 41 unique Google Play applications
APP_METADATA = {
    # MFS Applications (14 apps)
    "com.bKash.customerapp": {"app_name": "bKash", "sector": "MFS", "subcategory": "MFS"},
    "com.konasl.nagad": {"app_name": "Nagad", "sector": "MFS", "subcategory": "MFS"},
    "com.dbbl.mbs.apps.main": {"app_name": "Rocket", "sector": "MFS", "subcategory": "MFS"},
    "bd.com.upay.customer": {"app_name": "upay", "sector": "MFS", "subcategory": "MFS"},
    "com.ibbl.cellfin": {"app_name": "CellFin", "sector": "MFS", "subcategory": "MFS"},
    "com.dbbl.nexus.pay": {"app_name": "NexusPay", "sector": "MFS", "subcategory": "MFS"},
    "com.ibbl.mcashcustomer": {"app_name": "mCash", "sector": "MFS", "subcategory": "MFS"},
    "com.modefin.meghnaui": {"app_name": "MeghnaPay", "sector": "MFS", "subcategory": "MFS"},
    "com.mycash": {"app_name": "MYCash", "sector": "MFS", "subcategory": "MFS"},
    "com.fsiblbd.customer": {"app_name": "FirstCash", "sector": "MFS", "subcategory": "MFS"},
    "com.iw.app": {"app_name": "Islamic Wallet", "sector": "MFS", "subcategory": "MFS"},
    "com.reddot.lenden.customerapp": {"app_name": "LENDEN", "sector": "MFS", "subcategory": "MFS"},
    "com.reddot.telecash.mobile": {"app_name": "TeleCash", "sector": "MFS", "subcategory": "MFS"},
    "com.trustandpay.customer": {"app_name": "Trust And Pay", "sector": "MFS", "subcategory": "MFS"},

    # Commercial & State-Owned Banks (25 apps)
    # State-Owned Commercial Banks (SOCBs) & Specialized
    "bd.com.sonalibank.sw": {"app_name": "Sonali e-Wallet", "sector": "BANKING", "subcategory": "SOCB"},
    "bd.com.sonalibank.ss": {"app_name": "Sonali eSheba", "sector": "BANKING", "subcategory": "SOCB"},
    "net.celloscope.ib_mobile_app": {"app_name": "Agrani Smart App", "sector": "BANKING", "subcategory": "SOCB"},
    "com.jb.ejanata": {"app_name": "eJanata", "sector": "BANKING", "subcategory": "SOCB"},
    "com.rbplc.rupaliebank": {"app_name": "Rupali eBank", "sector": "BANKING", "subcategory": "SOCB"},
    "eraapps.bdbl.bdinternetbanking.apps": {"app_name": "BDBL Digital Bank", "sector": "BANKING", "subcategory": "SOCB"},

    # Private Commercial Banks (PCBs) Conventional
    "com.bracbank.astha": {"app_name": "BRAC Bank Astha", "sector": "BANKING", "subcategory": "PCB_CONVENTIONAL"},
    "com.thecitybank.citytouch": {"app_name": "Citytouch", "sector": "BANKING", "subcategory": "PCB_CONVENTIONAL"},
    "com.ebl.skybanking": {"app_name": "EBL Skybanking", "sector": "BANKING", "subcategory": "PCB_CONVENTIONAL"},
    "eraapps.bankasia.bdinternetbanking.apps": {"app_name": "Bank Asia Zen", "sector": "BANKING", "subcategory": "PCB_CONVENTIONAL"},
    "com.dbl.goplus": {"app_name": "DBL Go Plus", "sector": "BANKING", "subcategory": "PCB_CONVENTIONAL"},
    "com.ific.mobile": {"app_name": "IFIC Aamar Bank", "sector": "BANKING", "subcategory": "PCB_CONVENTIONAL"},
    "com.konasl.mercantile": {"app_name": "MBL Rainbow", "sector": "BANKING", "subcategory": "PCB_CONVENTIONAL"},
    "bd.com.primebank.pib.altitudemobile": {"app_name": "MyPrime", "sector": "BANKING", "subcategory": "PCB_CONVENTIONAL"},
    "com.pubali.internet.banking": {"app_name": "PI Banking", "sector": "BANKING", "subcategory": "PCB_CONVENTIONAL"},
    "com.seblit.ssa": {"app_name": "Southeast Bank PLC", "sector": "BANKING", "subcategory": "PCB_CONVENTIONAL"},
    "bd.com.ucb.unet": {"app_name": "UCB One", "sector": "BANKING", "subcategory": "PCB_CONVENTIONAL"},

    # Private Commercial Banks (PCBs) Islamic
    "com.ionicframework.icellular894076": {"app_name": "IBBL iSmart", "sector": "BANKING", "subcategory": "PCB_ISLAMIC"},
    "com.bd.aibl.ibapps": {"app_name": "aibl i-Banking", "sector": "BANKING", "subcategory": "PCB_ISLAMIC"},
    "com.eximbankbd.eWallet": {"app_name": "EXIM aiser", "sector": "BANKING", "subcategory": "PCB_ISLAMIC"},
    "com.mislbd.sibl.now": {"app_name": "SIBL NOW", "sector": "BANKING", "subcategory": "PCB_ISLAMIC"},
    "com.cibl.sblmobilebanking": {"app_name": "SBL DigiBanking", "sector": "BANKING", "subcategory": "PCB_ISLAMIC"},
    "com.cibl.app.shahjalalbankapp": {"app_name": "TouchPay", "sector": "BANKING", "subcategory": "PCB_ISLAMIC"},

    # Foreign Commercial Banks (FCB)
    "com.sc.mobilebanking.bd": {"app_name": "SC Mobile", "sector": "BANKING", "subcategory": "FCB"},
    "com.citi.mobile.cdbe": {"app_name": "CitiDirect", "sector": "BANKING", "subcategory": "FCB"},

    # Non-Financial Controls (2 apps)
    "com.hellotalk": {"app_name": "HelloTalk", "sector": "GENERAL", "subcategory": "CONTROL"},
    "com.idea.backup.smscontacts": {"app_name": "Super Backup", "sector": "GENERAL", "subcategory": "CONTROL"},
}

def run_real_apks_batch():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    apks_dir = os.path.join(base_dir, "apks")
    out_dir = os.path.join(base_dir, "study", "results", "real_apks")
    os.makedirs(out_dir, exist_ok=True)

    apk_files = sorted(glob.glob(os.path.join(apks_dir, "*.*")))
    print(f"Discovered {len(apk_files)} files in {apks_dir}.")

    processed_packages = set()
    summary_records = []

    for apk_path in apk_files:
        base_name = os.path.basename(apk_path)
        # Skip duplicate download
        if "(1)" in base_name:
            print(f"Skipping duplicate file: {base_name}")
            continue

        try:
            extractor = APKExtractor(apk_path)
            pkg = extractor.package_name
            if pkg in processed_packages:
                print(f"Package {pkg} already processed; skipping {base_name}")
                continue
            processed_packages.add(pkg)

            meta = APP_METADATA.get(pkg, {
                "app_name": base_name.split("_")[0],
                "sector": "MFS" if "mfs" in base_name.lower() else "BANKING",
                "subcategory": "GENERAL"
            })

            dist_type = "Multi-Split APKS" if apk_path.endswith(".apks") else "Monolithic APK"
            print(f"Analyzing [{meta['sector']}/{meta['subcategory']}] {meta['app_name']} ({pkg}) from {dist_type}...")

            ctx = extractor.build_full_context()
            ctx["manifest"]["declared_category"] = meta["sector"]

            # Run compliance audit
            audit_result = run_audit(ctx, package_name=pkg, sector=meta["sector"])

            # Save detailed per-app audit JSON
            json_file = os.path.join(out_dir, f"{pkg}.json")
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(audit_result, f, indent=2, ensure_ascii=False)

            prof = audit_result["summary_profile"]
            metrics = audit_result["metrics"]
            ec = metrics["EvidenceCoverage"]
            esc = metrics["EvidenceSupportedCompliance"]
            sci = round(ec * esc, 4)

            app_info = ctx.get("manifest", {}).get("application", {})
            allow_backup = app_info.get("allowBackup")
            uses_cleartext = app_info.get("usesCleartextTraffic")
            debuggable = app_info.get("debuggable")
            keystore = ctx.get("dex", {}).get("keystore_usage", False)
            enc_prefs = ctx.get("storage", {}).get("encrypted_shared_preferences_used", False)
            trackers = ctx.get("sdk", {}).get("third_party_packages", [])
            ciphers = [c.get("transformation") for c in ctx.get("dex", {}).get("ciphers", [])]
            urls = [u.get("url") for u in ctx.get("network", {}).get("cleartext_http_urls", [])]

            rec = {
                "app_name": meta["app_name"],
                "package_name": pkg,
                "sector": meta["sector"],
                "subcategory": meta["subcategory"],
                "distribution": dist_type,
                "supported_S": prof["Supported"],
                "non_conformance_P": prof["PotentialNonConformance"],
                "insufficient_I": prof["InsufficientEvidence"],
                "not_observable_O": prof["NotObservable"],
                "not_applicable_A": prof["NotApplicable"],
                "evidence_coverage_EC": ec,
                "evidence_supported_compliance_ESC": esc,
                "structural_conformance_index_SCI": sci,
                "allow_backup": allow_backup,
                "uses_cleartext_traffic": uses_cleartext,
                "debuggable": debuggable,
                "keystore_usage": keystore,
                "encrypted_prefs": enc_prefs,
                "trackers_count": len(trackers),
                "trackers": ";".join(trackers),
                "ciphers": ";".join(ciphers[:4]),
                "cleartext_urls_count": len(urls)
            }
            summary_records.append(rec)

        except Exception as e:
            print(f"ERROR analyzing {base_name}: {e}")

    # Write summary CSV
    csv_file = os.path.join(out_dir, "audit_summary.csv")
    if summary_records:
        keys = summary_records[0].keys()
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(summary_records)

    # Write summary JSON
    json_summary_file = os.path.join(out_dir, "audit_summary.json")
    with open(json_summary_file, "w", encoding="utf-8") as f:
        json.dump(summary_records, f, indent=2, ensure_ascii=False)

    print(f"\nSuccessfully audited {len(summary_records)} unique production applications!")
    print(f"Summary CSV: {csv_file}")
    print(f"Summary JSON: {json_summary_file}")
    return summary_records

if __name__ == "__main__":
    run_real_apks_batch()
