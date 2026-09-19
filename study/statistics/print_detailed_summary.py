import json
import numpy as np

with open('study/results/real_apks/audit_summary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

mfs = [d for d in data if d['sector'] == 'MFS']
mfs.sort(key=lambda x: (-x['structural_conformance_index_SCI'], -x['evidence_coverage_EC'], x['app_name']))

print("=== ALL 14 MFS APPLICATIONS ===")
print(f"{'Application':16s} & {'Package Identifier':32s} & {'Distribution':18s} & S & P & I & EC(\\%) & ESC(\\%) & SCI \\\\")
print("-" * 110)
for m in mfs:
    dist = "Multi-Split APKS" if "Multi-Split" in m["distribution"] else "Monolithic APK"
    ec = m["evidence_coverage_EC"] * 100
    esc = m["evidence_supported_compliance_ESC"] * 100
    sci = m["structural_conformance_index_SCI"]
    print(f"\\textbf{{{m['app_name']}}} & \\texttt{{{m['package_name']}}} & {dist} & {m['supported_S']} & {m['non_conformance_P']} & {m['insufficient_I']} & {ec:.1f}\\% & {esc:.1f}\\% & {sci:.3f} \\\\")

S_mfs = [m['supported_S'] for m in mfs]
P_mfs = [m['non_conformance_P'] for m in mfs]
I_mfs = [m['insufficient_I'] for m in mfs]
EC_mfs = [m['evidence_coverage_EC'] * 100 for m in mfs]
ESC_mfs = [m['evidence_supported_compliance_ESC'] * 100 for m in mfs]
SCI_mfs = [m['structural_conformance_index_SCI'] for m in mfs]
print("-" * 110)
print(f"\\textbf{{MFS Sector Mean}} & --- & --- & $\\mathbf{{{np.mean(S_mfs):.2f} \\pm {np.std(S_mfs, ddof=1):.2f}}}$ & $\\mathbf{{{np.mean(P_mfs):.2f} \\pm {np.std(P_mfs, ddof=1):.2f}}}$ & $\\mathbf{{{np.mean(I_mfs):.2f} \\pm {np.std(I_mfs, ddof=1):.2f}}}$ & $\\mathbf{{{np.mean(EC_mfs):.1f}\\% \\pm {np.std(EC_mfs, ddof=1):.1f}}}$ & $\\mathbf{{{np.mean(ESC_mfs):.1f}\\% \\pm {np.std(ESC_mfs, ddof=1):.1f}}}$ & $\\mathbf{{{np.mean(SCI_mfs):.3f} \\pm {np.std(SCI_mfs, ddof=1):.3f}}}$ \\\\")
print(f"MFS Column Sums: S={sum(S_mfs)}, P={sum(P_mfs)}, I={sum(I_mfs)}, Total={sum(S_mfs)+sum(P_mfs)+sum(I_mfs)}")
print(f"Sum of means: {np.mean(S_mfs) + np.mean(P_mfs) + np.mean(I_mfs):.2f}")

print("\n=== ALL 25 BANKING APPLICATIONS ===")
banking = [d for d in data if d['sector'] == 'BANKING']
banking.sort(key=lambda x: (x['subcategory'], -x['structural_conformance_index_SCI'], x['app_name']))

for b in banking:
    dist = "Multi-Split APKS" if "Multi-Split" in b["distribution"] else "Monolithic APK"
    ec = b["evidence_coverage_EC"] * 100
    esc = b["evidence_supported_compliance_ESC"] * 100
    sci = b["structural_conformance_index_SCI"]
    print(f"\\textbf{{{b['app_name']}}} ({b['subcategory']}) & \\texttt{{{b['package_name']}}} & {dist} & {b['supported_S']} & {b['non_conformance_P']} & {b['insufficient_I']} & {ec:.1f}\\% & {esc:.1f}\\% & {sci:.3f} \\\\")

S_b = [m['supported_S'] for m in banking]
P_b = [m['non_conformance_P'] for m in banking]
I_b = [m['insufficient_I'] for m in banking]
EC_b = [m['evidence_coverage_EC'] * 100 for m in banking]
ESC_b = [m['evidence_supported_compliance_ESC'] * 100 for m in banking]
SCI_b = [m['structural_conformance_index_SCI'] for m in banking]
print("-" * 110)
print(f"\\textbf{{Banking Sector Mean}} & --- & --- & $\\mathbf{{{np.mean(S_b):.2f} \\pm {np.std(S_b, ddof=1):.2f}}}$ & $\\mathbf{{{np.mean(P_b):.2f} \\pm {np.std(P_b, ddof=1):.2f}}}$ & $\\mathbf{{{np.mean(I_b):.2f} \\pm {np.std(I_b, ddof=1):.2f}}}$ & $\\mathbf{{{np.mean(EC_b):.1f}\\% \\pm {np.std(EC_b, ddof=1):.1f}}}$ & $\\mathbf{{{np.mean(ESC_b):.1f}\\% \\pm {np.std(ESC_b, ddof=1):.1f}}}$ & $\\mathbf{{{np.mean(SCI_b):.3f} \\pm {np.std(SCI_b, ddof=1):.3f}}}$ \\\\")
print(f"Banking Column Sums: S={sum(S_b)}, P={sum(P_b)}, I={sum(I_b)}, Total={sum(S_b)+sum(P_b)+sum(I_b)}")
print(f"Sum of means: {np.mean(S_b) + np.mean(P_b) + np.mean(I_b):.2f}")

print("\n=== COMBINED FINANCIAL CORPUS (N=39) ===")
fin = mfs + banking
S_f = [m['supported_S'] for m in fin]
P_f = [m['non_conformance_P'] for m in fin]
I_f = [m['insufficient_I'] for m in fin]
EC_f = [m['evidence_coverage_EC'] * 100 for m in fin]
ESC_f = [m['evidence_supported_compliance_ESC'] * 100 for m in fin]
SCI_f = [m['structural_conformance_index_SCI'] for m in fin]
print(f"\\textbf{{Combined Financial Mean}} & --- & --- & $\\mathbf{{{np.mean(S_f):.2f} \\pm {np.std(S_f, ddof=1):.2f}}}$ & $\\mathbf{{{np.mean(P_f):.2f} \\pm {np.std(P_f, ddof=1):.2f}}}$ & $\\mathbf{{{np.mean(I_f):.2f} \\pm {np.std(I_f, ddof=1):.2f}}}$ & $\\mathbf{{{np.mean(EC_f):.1f}\\% \\pm {np.std(EC_f, ddof=1):.1f}}}$ & $\\mathbf{{{np.mean(ESC_f):.1f}\\% \\pm {np.std(ESC_f, ddof=1):.1f}}}$ & $\\mathbf{{{np.mean(SCI_f):.3f} \\pm {np.std(SCI_f, ddof=1):.3f}}}$ \\\\")
print(f"Combined Column Sums: S={sum(S_f)}, P={sum(P_f)}, I={sum(I_f)}, Total={sum(S_f)+sum(P_f)+sum(I_f)}")
print(f"Sum of means: {np.mean(S_f) + np.mean(P_f) + np.mean(I_f):.2f}")
