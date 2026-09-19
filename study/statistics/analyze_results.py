import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import os
import json
import math
from collections import defaultdict

def run_statistical_analysis(index_json_path=None):
    if index_json_path is None:
        index_json_path = os.path.join(os.path.dirname(__file__), "..", "results", "study_execution_index.json")
    
    with open(index_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_apps = len(data)
    sector_esc = defaultdict(list)
    sector_ec = defaultdict(list)
    sector_violations = defaultdict(list)

    # 1. Sectoral aggregation (RQ5)
    financial_esc = []
    non_financial_esc = []

    for app in data:
        sec = app["sector"]
        esc = app["metrics"]["EvidenceSupportedCompliance"]
        ec = app["metrics"]["EvidenceCoverage"]
        viols = app["summary"]["PotentialNonConformance"]

        sector_esc[sec].append(esc)
        sector_ec[sec].append(ec)
        sector_violations[sec].append(viols)

        if app["is_regulated_financial"]:
            financial_esc.append(esc)
        else:
            non_financial_esc.append(esc)

    # 2. Compute Mann-Whitney U test statistic between Financial vs Non-Financial
    # Mann-Whitney U on ESC
    n1 = len(financial_esc)
    n2 = len(non_financial_esc)
    
    # Rank all values
    combined = [(v, 1) for v in financial_esc] + [(v, 2) for v in non_financial_esc]
    combined.sort(key=lambda x: x[0])
    
    ranks_group1 = 0
    for rank, (val, grp) in enumerate(combined, start=1):
        if grp == 1:
            ranks_group1 += rank
            
    U1 = ranks_group1 - (n1 * (n1 + 1)) / 2
    U2 = (n1 * n2) - U1
    U = min(U1, U2)
    
    mean_u = (n1 * n2) / 2
    sigma_u = math.sqrt((n1 * n2 * (n1 + n2 + 1)) / 12)
    z_score = (U - mean_u) / sigma_u if sigma_u > 0 else 0.0

    # Sector summary
    sector_summary = {}
    for sec in sector_esc:
        escs = sector_esc[sec]
        mean_esc = sum(escs) / len(escs) if escs else 0.0
        mean_ec = sum(sector_ec[sec]) / len(sector_ec[sec]) if sector_ec[sec] else 0.0
        avg_viols = sum(sector_violations[sec]) / len(sector_violations[sec]) if sector_violations[sec] else 0.0
        sector_summary[sec] = {
            "app_count": len(escs),
            "mean_ESC": round(mean_esc, 4),
            "mean_EC": round(mean_ec, 4),
            "avg_potential_violations": round(avg_viols, 2)
        }

    report = {
        "dataset_summary": {
            "total_applications_analyzed": total_apps,
            "financial_apps": n1,
            "non_financial_apps": n2
        },
        "rq5_sectoral_disparity": {
            "mean_ESC_financial": round(sum(financial_esc)/n1, 4) if n1 else 0,
            "mean_ESC_non_financial": round(sum(non_financial_esc)/n2, 4) if n2 else 0,
            "mann_whitney_u": round(U, 2),
            "z_score": round(z_score, 4),
            "statistically_significant": abs(z_score) > 1.96,
            "p_value_approx": "< 0.001" if abs(z_score) > 3.29 else ("< 0.05" if abs(z_score) > 1.96 else ">= 0.05")
        },
        "sector_breakdown": sector_summary
    }

    out_stat_path = os.path.join(os.path.dirname(__file__), "sectoral_statistics.json")
    with open(out_stat_path, "w", encoding="utf-8") as out_f:
        json.dump(report, out_f, indent=2, ensure_ascii=False)

    print("[OK] Statistical Analysis Report:")
    print(f"  Total Applications: {total_apps}")
    print(f"  Financial ESC Mean: {report['rq5_sectoral_disparity']['mean_ESC_financial']}")
    print(f"  Non-Financial ESC Mean: {report['rq5_sectoral_disparity']['mean_ESC_non_financial']}")
    print(f"  Z-Score: {report['rq5_sectoral_disparity']['z_score']} (p-val: {report['rq5_sectoral_disparity']['p_value_approx']})")
    return report

if __name__ == "__main__":
    run_statistical_analysis()
