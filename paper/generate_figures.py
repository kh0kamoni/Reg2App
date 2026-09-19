import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# ----------------------------------------------------------------------------
# Publication Style Configuration
# ----------------------------------------------------------------------------
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 10,
    'axes.labelsize': 10.5,
    'axes.titlesize': 11.5,
    'xtick.labelsize': 9.5,
    'ytick.labelsize': 9.5,
    'legend.fontsize': 9,
    'figure.titlesize': 12.5,
    'axes.linewidth': 0.8,
    'grid.linewidth': 0.6,
    'grid.color': '#e2e8f0',
    'grid.alpha': 0.7,
    'pdf.fonttype': 42,
    'ps.fonttype': 42
})

out_dir = r"C:\Users\Khoka Moni\Downloads\research_all\bb_comp\paper\figures"
os.makedirs(out_dir, exist_ok=True)

# ============================================================================
# Figure 1: Conceptual Architecture & Comparison
# ============================================================================
def generate_fig1():
    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Background column cards
    card_conv = FancyBboxPatch((0.03, 0.05), 0.44, 0.90, boxstyle="round,pad=0.015,rounding_size=0.02",
                               facecolor='#fff5f5', edgecolor='#fca5a5', lw=1.2)
    card_reg = FancyBboxPatch((0.53, 0.05), 0.44, 0.90, boxstyle="round,pad=0.015,rounding_size=0.02",
                              facecolor='#f0fdf4', edgecolor='#86efac', lw=1.2)
    ax.add_patch(card_conv)
    ax.add_patch(card_reg)

    # Column Headers
    ax.text(0.25, 0.91, "Conventional Vulnerability Scanners\n(e.g., MobSF, Androguard)",
            ha='center', va='center', weight='bold', fontsize=10.5, color='#991b1b')
    ax.text(0.75, 0.91, "The Reg2App Verification Framework\n(Epistemic & Evidence-Based)",
            ha='center', va='center', weight='bold', fontsize=10.5, color='#166534')

    # Step cards styling
    conv_box = dict(boxstyle='round,pad=0.4,rounding_size=0.015', facecolor='#ffffff', edgecolor='#f87171', lw=1.0)
    reg_box = dict(boxstyle='round,pad=0.4,rounding_size=0.015', facecolor='#ffffff', edgecolor='#4ade80', lw=1.0)
    arrow_props = dict(arrowstyle='-|>', lw=1.2, color='#64748b', mutation_scale=12)

    # Left steps
    ax.text(0.25, 0.77, "1. Input: Unprocessed Client APK Only\nNo statutory grounding or legal models",
            ha='center', va='center', bbox=conv_box, fontsize=8.8)
    ax.annotate('', xy=(0.25, 0.67), xytext=(0.25, 0.72), arrowprops=arrow_props)

    ax.text(0.25, 0.61, "2. Analysis: Generic CWE Pattern Matching\nTreats client APK as entire system",
            ha='center', va='center', bbox=conv_box, fontsize=8.8)
    ax.annotate('', xy=(0.25, 0.51), xytext=(0.25, 0.56), arrowprops=arrow_props)

    ax.text(0.25, 0.45, "3. Epistemic Flaw: Unbounded Extrapolation\nHallucinates compliance on unobservables\n(e.g., backend encryption, policies, training)",
            ha='center', va='center', bbox=conv_box, fontsize=8.5)
    ax.annotate('', xy=(0.25, 0.33), xytext=(0.25, 0.38), arrowprops=arrow_props)

    ax.text(0.25, 0.23, "4. Output: Fictitious Scalar Percentage\n'70% Compliant (Grade B)'\n[Legally Invalid & Scientifically Unsound]",
            ha='center', va='center', bbox=conv_box, fontsize=8.8, weight='bold', color='#991b1b')

    # Right steps
    ax.text(0.75, 0.77, "1. Input: Decompiled APK + Legal Corpus\nFormally encoded YAML regulation knowledge base",
            ha='center', va='center', bbox=reg_box, fontsize=8.8)
    ax.annotate('', xy=(0.75, 0.67), xytext=(0.75, 0.72), arrowprops=arrow_props)

    ax.text(0.75, 0.61, "2. Formal Mapping & Observability\n7-tuple model & 2D operator Ω(R)\nPartitions client-side vs. backend obligations",
            ha='center', va='center', bbox=reg_box, fontsize=8.8)
    ax.annotate('', xy=(0.75, 0.51), xytext=(0.75, 0.56), arrowprops=arrow_props)

    ax.text(0.75, 0.45, "3. Provenance Graph DAG G = (V, E)\nRigorous chain linking legal clauses to\nverifiable Dalvik & manifest bytecode witnesses",
            ha='center', va='center', bbox=reg_box, fontsize=8.5)
    ax.annotate('', xy=(0.75, 0.33), xytext=(0.75, 0.38), arrowprops=arrow_props)

    ax.text(0.75, 0.23, "4. Output: 5-State Epistemic Space\nState space {S, P, I, O, A} & Coverage EC/ESC\n+ Actionable Bilingual Reports (EN/Bengali)",
            ha='center', va='center', bbox=reg_box, fontsize=8.8, weight='bold', color='#166534')

    # Central divider badge
    ax.text(0.5, 0.50, "VS", ha='center', va='center', weight='bold', fontsize=11, color='#475569',
            bbox=dict(boxstyle='circle,pad=0.3', facecolor='#f1f5f9', edgecolor='#cbd5e1', lw=1.2))

    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "fig1_motivating_comparison.pdf"), bbox_inches='tight')
    plt.savefig(os.path.join(out_dir, "fig1_motivating_comparison.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved fig1")

# ============================================================================
# Figure 2: End-to-End System Architecture (Professional Redesign)
# ============================================================================
def generate_fig2():
    fig, ax = plt.subplots(figsize=(9.4, 4.4), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)

    # 5 Main Process Blocks (Stage 1 to 5)
    stages = [
        {"name": "Stage 1: Ingestion", "x": 1, "y": 3, "w": 17, "h": 44, "bg": "#f8fafc", "border": "#3b82f6", "title_col": "#1d4ed8"},
        {"name": "Stage 2: Extraction", "x": 20, "y": 3, "w": 17, "h": 44, "bg": "#f8fafc", "border": "#0284c7", "title_col": "#0369a1"},
        {"name": "Stage 3: Analysis Engine", "x": 39, "y": 3, "w": 23, "h": 44, "bg": "#f8fafc", "border": "#d97706", "title_col": "#b45309"},
        {"name": "Stage 4: Epistemic Core", "x": 64, "y": 3, "w": 17, "h": 44, "bg": "#f8fafc", "border": "#059669", "title_col": "#047857"},
        {"name": "Stage 5: Remediation", "x": 83, "y": 3, "w": 16, "h": 44, "bg": "#f8fafc", "border": "#7c3aed", "title_col": "#6d28d9"}
    ]

    for s in stages:
        patch = FancyBboxPatch((s['x'], s['y']), s['w'], s['h'], boxstyle="round,pad=0.3,rounding_size=1.2",
                               facecolor=s['bg'], edgecolor=s['border'], lw=1.2)
        ax.add_patch(patch)
        ax.text(s['x'] + s['w']/2, 44.5, s['name'], ha='center', va='center',
                weight='bold', fontsize=8.8, color=s['title_col'])

    # Stage 1 Sub-cards (No bullets)
    box_sub = dict(boxstyle='round,pad=0.3,rounding_size=0.8', facecolor='#ffffff', edgecolor='#cbd5e1', lw=0.9)
    ax.text(9.5, 33, "Mobile Artifacts\nTarget APK / APKS\nMulti-Split Packages\nAsset Bundles",
            ha='center', va='center', bbox=box_sub, fontsize=7.6)
    ax.text(9.5, 15, "Statutory Corpus\nBB-CSF v1.0 (BRPD)\nDraft BD-PDPA\nBD-CSA 2023",
            ha='center', va='center', bbox=box_sub, fontsize=7.6)

    # Stage 2 Sub-cards (No bullets)
    ax.text(28.5, 33, "Decompiler Pipeline\nAPKS Resolver\nDalvik .dex Parser\nAXML Decoder",
            ha='center', va='center', bbox=box_sub, fontsize=7.6)
    ax.text(28.5, 15, "Regulation Engine\n7-Tuple Parser\n2D Observability Ω\nExpert Provenance",
            ha='center', va='center', bbox=box_sub, fontsize=7.6)

    # Stage 3 Analyzers (Modular Engine)
    analyzers = [
        "1. Manifest Security Flags",
        "2. Keystore & Crypto Audit",
        "3. Local Database & Prefs",
        "4. Network & TLS Pinning",
        "5. Third-Party Tracker SDKs",
        "6. Dataflow Taint Propagation"
    ]
    for i, a in enumerate(analyzers):
        y_pos = 38 - i * 5.8
        ax.text(50.5, y_pos, a, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.25,rounding_size=0.5', facecolor='#ffffff', edgecolor='#fde68a', lw=0.9),
                fontsize=7.8, weight='medium')

    # Stage 4 Sub-cards (No bullets)
    ax.text(72.5, 33, "Evidence DAG G=(V,E)\nStatute Nodes\nTechnical Controls\nBytecode Witnesses",
            ha='center', va='center', bbox=box_sub, fontsize=7.6)
    ax.text(72.5, 15, "5-State Epistemic Core\nStates: {S, P, I, O, A}\nObservability Gate\nMetrics: EC, ESC, SCI",
            ha='center', va='center', bbox=box_sub, fontsize=7.6)

    # Stage 5 Sub-cards (No bullets)
    ax.text(91.0, 33, "Bilingual Reports\nExecutive Summary\nEnglish Diagnostics\nBengali Diagnostics",
            ha='center', va='center', bbox=box_sub, fontsize=7.6)
    ax.text(91.0, 15, "Developer Tools\nBytecode Offsets\nConcrete Code Diffs\nCI/CD Gating Rules",
            ha='center', va='center', bbox=box_sub, fontsize=7.6)

    # Inter-stage connector arrows
    arrow_style = dict(arrowstyle='-|>', lw=1.3, color='#475569', mutation_scale=11)
    ax.annotate('', xy=(20, 33), xytext=(18, 33), arrowprops=arrow_style)
    ax.annotate('', xy=(20, 15), xytext=(18, 15), arrowprops=arrow_style)
    ax.annotate('', xy=(39, 33), xytext=(37, 33), arrowprops=arrow_style)
    ax.annotate('', xy=(39, 15), xytext=(37, 15), arrowprops=arrow_style)
    ax.annotate('', xy=(64, 33), xytext=(62, 33), arrowprops=arrow_style)
    ax.annotate('', xy=(64, 15), xytext=(62, 15), arrowprops=arrow_style)
    ax.annotate('', xy=(83, 33), xytext=(81, 33), arrowprops=arrow_style)
    ax.annotate('', xy=(83, 15), xytext=(81, 15), arrowprops=arrow_style)

    # Intra-stage feedback/links
    ax.annotate('', xy=(72.5, 23), xytext=(72.5, 27), arrowprops=dict(arrowstyle='<|-|>', lw=1.1, color='#059669', mutation_scale=9))

    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "fig2_system_architecture.pdf"), bbox_inches='tight')
    plt.savefig(os.path.join(out_dir, "fig2_system_architecture.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved fig2")

# ============================================================================
# Figure 3: Cross-Sectoral Compliance Disparity (Data Plot)
# ============================================================================
def generate_fig3():
    fig, ax = plt.subplots(figsize=(8.6, 4.4), dpi=300)

    sectors = [
        'MFS Wallets\n(14 Apps)', 'Commercial Banks\n(25 Apps)',
        'Government\n(e-Gov, 4)', 'Transit\n(Ride-Share, 2)',
        'Telecom\n(Utilities, 2)', 'Healthcare\n(Digital, 1)',
        'Media\n(News, 1)', 'E-Commerce\n(Retail, 4)'
    ]
    esc_scores = [0.509, 0.498, 0.750, 0.750, 0.750, 0.667, 0.500, 0.000]
    ec_scores = [0.720, 0.733, 0.667, 0.667, 0.667, 0.667, 0.667, 0.833]

    x = np.arange(len(sectors))
    width = 0.35

    # Modern elegant colors: Deep Navy / Royal Blue & Sky / Cyan Blue
    rects1 = ax.bar(x - width/2, [s * 100 for s in esc_scores], width,
                    label='Evidence-Supported Compliance (ESC %)', color='#1e40af', edgecolor='none', zorder=3)
    rects2 = ax.bar(x + width/2, [c * 100 for c in ec_scores], width,
                    label='Evidence Coverage (EC %)', color='#60a5fa', edgecolor='none', zorder=3)

    ax.set_ylabel('Score Percentage (%)', weight='bold')
    ax.set_title('Cross-Sectoral Regulatory Compliance and Observability Metrics (N = 53 Applications)',
                 weight='bold', pad=30)
    ax.set_xticks(x)
    ax.set_xticklabels(sectors, fontsize=8.2)
    ax.set_ylim(0, 132)

    # Spines & Grid
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#94a3b8')
    ax.spines['bottom'].set_color('#94a3b8')
    ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)

    # Vertical dividing line between Financial and Non-Financial
    ax.axvline(1.5, color='#cbd5e1', linestyle='--', lw=1.2, zorder=2)

    # Sector cohort header brackets (clean, publication style)
    # Financial cohort bracket spanning 0 to 1
    ax.plot([0 - width, 1 + width], [116, 116], color='#15803d', lw=1.5, clip_on=False)
    ax.plot([0 - width, 0 - width], [113, 116], color='#15803d', lw=1.5, clip_on=False)
    ax.plot([1 + width, 1 + width], [113, 116], color='#15803d', lw=1.5, clip_on=False)
    ax.text(0.5, 119, "Regulated Financial Sector (N = 39)\nMean ESC = 50.2% | Hardware Keystore = 82.1%",
            ha='center', va='bottom', fontsize=7.6, color='#15803d', weight='bold')

    # Non-financial cohort bracket spanning 2 to 7
    ax.plot([2 - width, 7 + width], [116, 116], color='#b91c1c', lw=1.5, clip_on=False)
    ax.plot([2 - width, 2 - width], [113, 116], color='#b91c1c', lw=1.5, clip_on=False)
    ax.plot([7 + width, 7 + width], [113, 116], color='#b91c1c', lw=1.5, clip_on=False)
    ax.text(4.5, 119, "Non-Financial Commercial Sectors (N = 14)\nMann-Whitney U = 156.0, p < 0.001 | Retail ESC = 0.0%",
            ha='center', va='bottom', fontsize=7.6, color='#b91c1c', weight='bold')

    # Value annotations on bars
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 2), textcoords="offset points", ha='center', va='bottom',
                    fontsize=7.3, weight='bold', color='#1e3a8a')

    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 2), textcoords="offset points", ha='center', va='bottom',
                    fontsize=7.0, color='#2563eb')

    ax.legend(loc='upper right', frameon=True, facecolor='#ffffff', edgecolor='#e2e8f0', fontsize=8.2)

    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "fig3_sectoral_disparity.pdf"), bbox_inches='tight')
    plt.savefig(os.path.join(out_dir, "fig3_sectoral_disparity.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved fig3")

# ============================================================================
# Figure 4: Live Production MFS Audit Breakdown (N = 14)
# ============================================================================
def generate_fig4():
    fig, ax = plt.subplots(figsize=(9.2, 4.3), dpi=300)

    apps = ['MFS-01', 'MFS-02', 'MFS-03', 'MFS-04', 'MFS-05', 'MFS-06', 'MFS-07',
            'MFS-08', 'MFS-09', 'MFS-10', 'MFS-11', 'MFS-12', 'MFS-13', 'MFS-14']
    supported = [6, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 3, 3]
    non_conf =  [4, 5, 4, 4, 4, 4, 4, 5, 5, 4, 4, 4, 4, 4]
    insuff =    [2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 5, 5]

    x = np.arange(len(apps))
    w = 0.58

    # Professional palette: Emerald (#059669), Coral Red (#e11d48), Amber (#d97706)
    p1 = ax.bar(x, supported, w, label='Supported (S) [Compliant Evidence]', color='#059669', zorder=3)
    p2 = ax.bar(x, non_conf, w, bottom=supported, label='Potential Non-Conformance (P) [Defect Witness]', color='#e11d48', zorder=3)
    p3 = ax.bar(x, insuff, w, bottom=np.array(supported) + np.array(non_conf), label='Insufficient Evidence (I) [Native/Obfuscated]', color='#d97706', zorder=3)

    ax.set_ylabel('Statutory Requirements (Total = 12)', weight='bold', labelpad=10)
    ax.set_title('Empirical Audit Across All 14 Operational Bangladesh MFS Applications (RQ3)', weight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(apps, rotation=35, ha='right', fontsize=8.5)
    ax.set_ylim(0, 14.8)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#94a3b8')
    ax.spines['bottom'].set_color('#94a3b8')
    ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)

    # Clean centered numeric labels inside each bar segment
    for i in range(len(apps)):
        # S segment
        ax.text(x[i], supported[i] / 2, str(supported[i]), ha='center', va='center',
                color='white', weight='bold', fontsize=8)
        # P segment
        ax.text(x[i], supported[i] + non_conf[i] / 2, str(non_conf[i]), ha='center', va='center',
                color='white', weight='bold', fontsize=8)
        # I segment
        ax.text(x[i], supported[i] + non_conf[i] + insuff[i] / 2, str(insuff[i]), ha='center', va='center',
                color='white', weight='bold', fontsize=8)

    ax.legend(loc='upper right', ncol=3, frameon=True, facecolor='#ffffff', edgecolor='#e2e8f0', fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "fig4_mfs_audit_breakdown.pdf"), bbox_inches='tight')
    plt.savefig(os.path.join(out_dir, "fig4_mfs_audit_breakdown.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved fig4")

# ============================================================================
# Figure 5: Human-Subjects Usable Security Evaluation (N = 60)
# ============================================================================
def generate_fig5():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 4.0), dpi=300)

    conditions = ['Condition A\n(Raw Diagnostic)', 'Condition B\n(Structured EN)', 'Condition C\n(Localized BN)']
    accuracy = [53.6, 70.7, 82.9]
    sus = [47.0, 65.7, 76.8]
    tlx = [65.5, 47.2, 36.9]
    time_min = [39.7, 28.6, 19.0]

    # Panel (a): Cognitive & Usability Metrics
    x = np.arange(len(conditions))
    w = 0.24
    b1 = ax1.bar(x - w, accuracy, w, label='Comprehension Acc. (%)', color='#2563eb', zorder=3)
    b2 = ax1.bar(x, sus, w, label='System Usability (SUS)', color='#059669', zorder=3)
    b3 = ax1.bar(x + w, tlx, w, label='Cognitive Load (NASA-TLX)', color='#d97706', zorder=3)

    ax1.set_ylabel('Metric Score (Scale: 0 - 100)', weight='bold')
    ax1.set_title('(a) Cognitive & Usability Metrics (N = 60)', weight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(conditions, fontsize=8.5)
    ax1.set_ylim(0, 115)

    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color('#94a3b8')
    ax1.spines['bottom'].set_color('#94a3b8')
    ax1.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)

    for bar in b1:
        h = bar.get_height()
        ax1.annotate(f'{h:.1f}%', xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 2),
                     textcoords="offset points", ha='center', va='bottom', fontsize=7.2, weight='bold', color='#1e3a8a')
    for bar in b2:
        h = bar.get_height()
        ax1.annotate(f'{h:.1f}', xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 2),
                     textcoords="offset points", ha='center', va='bottom', fontsize=7.2, weight='bold', color='#065f46')
    for bar in b3:
        h = bar.get_height()
        ax1.annotate(f'{h:.1f}', xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 2),
                     textcoords="offset points", ha='center', va='bottom', fontsize=7.2, weight='bold', color='#92400e')

    ax1.legend(loc='upper right', frameon=True, facecolor='#ffffff', edgecolor='#e2e8f0', fontsize=7.8)

    # Panel (b): Developer Remediation Time
    bars = ax2.bar(conditions, time_min, color=['#f43f5e', '#3b82f6', '#10b981'], width=0.48, zorder=3)
    ax2.set_ylabel('Mean Remediation Time (Minutes)', weight='bold')
    ax2.set_title('(b) Developer Defect Repair Time (n = 30)', weight='bold')
    ax2.set_ylim(0, 58)

    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color('#94a3b8')
    ax2.spines['bottom'].set_color('#94a3b8')
    ax2.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)

    for bar in bars:
        h = bar.get_height()
        ax2.annotate(f'{h:.1f} m', xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 2),
                     textcoords="offset points", ha='center', va='bottom', fontsize=8.5, weight='bold')

    # Curved arrow annotation without collisions
    ax2.annotate('52.1% Speedup\n(p < 0.0001, d = 2.45)',
                 xy=(2, 20.5), xytext=(1.05, 42),
                 arrowprops=dict(facecolor='#065f46', edgecolor='#065f46', arrowstyle='-|>',
                                 connectionstyle='arc3,rad=-0.2', lw=1.3),
                 fontsize=8.5, weight='bold', color='#065f46',
                 bbox=dict(boxstyle='round,pad=0.25', facecolor='#ecfdf5', edgecolor='#a7f3d0', lw=0.9))

    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "fig5_usable_security_results.pdf"), bbox_inches='tight')
    plt.savefig(os.path.join(out_dir, "fig5_usable_security_results.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved fig5")

# ============================================================================
# Figure 6: Third-Party Tracker Telemetry Density (RQ3)
# ============================================================================
def generate_fig6():
    fig, ax = plt.subplots(figsize=(7.6, 4.0), dpi=300)

    sectors = [
        'E-Commerce (Retail, n=4)',
        'Media / Publishing (n=1)',
        'Ride-Sharing / Transit (n=2)',
        'Digital Healthcare (n=1)',
        'Government (e-Gov, n=4)',
        'Telecom / Utilities (n=2)',
        'MFS Wallets (Live, n=14)',
        'Commercial Banking (Live, n=25)'
    ]
    trackers_per_app = [4.75, 4.00, 4.00, 3.00, 2.50, 2.50, 0.71, 0.64]

    colors = ['#7c3aed', '#8b5cf6', '#8b5cf6', '#a78bfa', '#a78bfa', '#c4b5fd', '#059669', '#059669']
    bars = ax.barh(sectors, trackers_per_app, color=colors, height=0.55, zorder=3)

    ax.set_xlabel('Mean Integrated Tracking & Analytics SDKs per Application', weight='bold')
    ax.set_title('Third-Party Telemetry Density Across Economic Sectors (RQ3, Total = 75 Trackers)', weight='bold')
    ax.set_xlim(0, 5.5)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#94a3b8')
    ax.spines['bottom'].set_color('#94a3b8')
    ax.grid(axis='x', linestyle='--', alpha=0.5, zorder=0)

    for bar in bars:
        w = bar.get_width()
        ax.annotate(f'{w:.2f}', xy=(w, bar.get_y() + bar.get_height()/2),
                    xytext=(5, 0), textcoords="offset points", ha='left', va='center',
                    fontsize=8.5, weight='bold', color='#334155')

    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "fig6_telemetry_density.pdf"), bbox_inches='tight')
    plt.savefig(os.path.join(out_dir, "fig6_telemetry_density.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved fig6")

if __name__ == '__main__':
    generate_fig1()
    generate_fig2()
    generate_fig3()
    generate_fig4()
    generate_fig5()
    generate_fig6()
    print("All 6 publication figures generated successfully!")

