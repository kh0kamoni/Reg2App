# Reg2App: Evidence-Based Privacy and Cybersecurity Compliance Verification of the Android Application Ecosystem

[![pytest](https://img.shields.io/badge/pytest-21%20passed-brightgreen.svg)](tests/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Official reproducibility artifact repository for the research paper:
> **"From Regulation to Bytecode: Evidence-Based Privacy and Cybersecurity Compliance Verification of the Android Application Ecosystem"**  
> Authors: [Khoka Moni](https://orcid.org/0009-0000-3573-714X) (Mymensingh Engineering College) & [Maria Akter](https://orcid.org/0009-0005-7038-9490) (Southeast University).  
> Target Venue: *Elsevier Journal of Systems and Software (JSS)*.

---

## Overview

**Reg2App** is a formally specified, provenance-preserving static analysis framework that operationalizes legal statutes into verifiable Android program properties. Rather than collapsing compliance into speculative percentage scores, Reg2App partitions requirements across an explicit epistemic boundary:

1. **7-Tuple Mapping Model ($M_i$)**: Formalizes legal obligations $(R_i, O_i, C_i, P_i, E_i, A_i, V_i)$ into machine-evaluable AST predicates $\phi \in \mathcal{L}_{\text{pred}}$.
2. **Two-Dimensional Observability Operator ($\Omega(R_i)$)**: Partitions requirements across observability levels ($\mathbf{FULL}, \mathbf{PARTIAL}, \mathbf{NONE}$) and operational modalities ($\mathbb{M}$), preventing compliance hallucinations on unobservable backend obligations.
3. **5-State Epistemic Space ($\mathcal{S}$)**: Evaluates targets into $\{\mathbf{Conforming}, \mathbf{PotentialNonConformance}, \mathbf{InsufficientEvidence}, \mathbf{NotObservable}, \mathbf{NotApplicable}\}$ with objective Evidence Coverage ($EC$) and Evidence-Supported Compliance ($ESC$) metrics.
4. **Evidence Provenance Graph ($G = (V, E)$)**: Graph-structured audit trail connecting statutory clauses to bytecode offsets, method invocations, and manifest declarations.
5. **Usable Multilingual Reporting**: Generates evidence-grounded bilingual (English and Bengali) developer reports with concrete remediation diffs.

---

## Repository Structure

```text
.
├── benchmark/               # 30 compilable micro-applications (MB-001 .. MB-030)
│   ├── apps/                # Synthetic APK source projects
│   ├── ground_truth.json    # 360-cell ground-truth evaluation matrix
│   └── evaluate_benchmark.py# Automated benchmark verification runner
├── knowledge_base/          # Declarative YAML statutory ontologies
│   ├── regulations/         # BB-CSF v1.0, Draft BD-PDPA, and BD-CSA 2023 schemas
│   ├── mappings/            # Formal 7-tuple mapping specifications
│   └── schemas/             # JSON Schema definitions for mapping validation
├── reg2app/                 # Core static program analysis engine
│   ├── analyzers/           # Manifest, Crypto, Storage, Network, and Telemetry analyzers
│   ├── assessment/          # Epistemic assessment evaluator and metric engine
│   ├── provenance/          # Provenance graph constructor (NetworkX / JSON)
│   └── reporting/           # Bilingual localized reporting generator (En/Bn)
├── expert_validation/       # Expert elicitation instruments & Delphi protocol data
│   ├── review_pack.json     # Blinded 12-item expert review pack
│   └── inter_rater_reliability.py # Fleiss' kappa and Krippendorff's alpha calculators
├── study/                   # Empirical ecosystem audit data (53 production apps)
│   ├── batch_runner.py      # Automated sectoral batch analysis engine
│   ├── sector_manifest.json # Application metadata across 8 economic sectors
│   └── outputs/             # Anonymized structured audit reports
├── user_study/              # Usable security developer study (N=60)
│   ├── human_study_n60_raw.csv # Counterbalanced experimental trial data
│   └── analyze_user_study.py   # Statistical evaluation script (McNemar, Wilcoxon, ANOVA)
└── tests/                   # 21 comprehensive unit tests
```

---

## Quick Start & Reproduction

### 1. Environment Setup

```bash
git clone https://github.com/kh0kamoni/Reg2App.git
cd Reg2App
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -e .
```

### 2. Running Unit Tests

Execute the 21-test verification suite:

```bash
pytest tests/ -v
```

### 3. Evaluating the Micro-Benchmark Suite (RQ2)

Verify the analyzer against the 360-cell ground-truth matrix across 30 micro-applications:

```bash
python benchmark/evaluate_benchmark.py
```

### 4. Running Expert Elicitation Reliability Analysis (RQ1)

Compute pre-reconciliation inter-rater reliability metrics ($\text{Fleiss' } \kappa, \text{Krippendorff's } \alpha$):

```bash
python expert_validation/inter_rater_reliability.py
```

### 5. Running User Study Statistical Analysis (RQ4)

Reproduce the paired McNemar exact tests, Wilcoxon signed-rank tests, and task completion times:

```bash
python user_study/analyze_user_study.py
```

---

## Ethical Considerations and Responsible Reporting

All empirical audits were conducted strictly in accordance with ACM and IEEE ethical research guidelines. All analyses were performed entirely offline on publicly available application packages downloaded from Google Play. At no point were live production services, payment gateways, banking backends, or customer accounts probed, scanned, or attacked. Zero exploits were constructed. To eliminate operational risks to production infrastructure and prevent targeted attacks, all institutional identities, organization names, and package namespaces are strictly pseudonymized, and vulnerability details are restricted to high-level technical observation categories. Detailed bytecode offsets and call graphs that could facilitate weaponization are deliberately omitted from public artifacts.

---

## Citation

```bibtex
@article{moni2026reg2app,
  title={From Regulation to Bytecode: Evidence-Based Privacy and Cybersecurity Compliance Verification of the Android Application Ecosystem},
  author={Moni, Khoka and Akter, Maria},
  journal={Journal of Systems and Software},
  year={2026},
  publisher={Elsevier}
}
```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
