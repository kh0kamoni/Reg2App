# Research Questions & Evaluation Framework

## Project: Reg2App (Bangladesh Regulatory Assessment Proving Ground)

### Central Thesis
> **Can natural-language regulatory requirements be systematically transformed into machine-observable Android program properties, and can static and dynamic program analysis reliably produce evidence for assessing those requirements under conditions of partial observability at ecosystem scale?**

---

### Research Questions (RQ1 ? RQ8)

#### **RQ1: Regulatory Formalization & Transformation**
- **Question**: How can unstructured, natural-language statutory requirements (e.g., PDPA 2026, Bangladesh Bank CSF v1.0, CSA 2026) be systematically transformed into machine-observable, formally specified Android security properties without loss of statutory intent?
- **Formal Target**: Formulation of the 7-tuple mapping:
  $$M_i = (R_i, O_i, C_i, P_i, E_i, A_i, V_i)$$
- **Measurement**: Ontological completeness, unambiguous source-sink mapping, and formal grammar coverage.

#### **RQ2: The Observability Boundary**
- **Question**: What proportion of national data-protection and financial cybersecurity obligations can be assessed through client-side Android artifacts (static bytecode, manifest, runtime execution) versus requirements that depend on backend architecture, organizational process, or legal intent?
- **Formal Target**: Empirical distribution across the 6-modality taxonomy:
  $$\mathcal{M} = \{\text{STATIC}, \text{DYNAMIC}, \text{HYBRID}, \text{BACKEND}, \text{ORGANIZATIONAL}, \text{LEGAL}\}$$
  and Observability Levels $\{\text{FULL}, \text{PARTIAL}, \text{NONE}\}$.
- **Measurement**: Observability ratio $OR = \frac{|\mathcal{R}_{\text{observable}}|}{|\mathcal{R}_{\text{total}}|}$ across statutory regimes.

#### **RQ3: Detection Accuracy on Controlled Ground-Truth**
- **Question**: How accurately does the proposed evidence-based regulatory analysis engine detect targeted program properties and data flows on a controlled, synthetic Android benchmark?
- **Formal Target**: Evaluation across a benchmark suite of $N \ge 50$ micro-applications exhibiting known compliant and non-conforming behaviors.
- **Measurement**: Precision, Recall, $F_1$-score, False Positive Rate (FPR), False Negative Rate (FNR) per technical property rule.

#### **RQ4: Ecosystem-Scale Prevalence of Technical Non-Conformance**
- **Question**: What is the prevalence and distribution of regulatory-relevant security weaknesses and privacy risks across Bangladesh's production Android application ecosystem?
- **Formal Target**: Static and dynamic measurement across $N = 500\text{--}1,000$ applications distributed in Bangladesh.
- **Measurement**: Frequency of potential non-conformance by requirement domain, severity, and evidence strength.

#### **RQ5: Cross-Sectoral Compliance Disparity**
- **Question**: Do Mobile Financial Services (MFS) and banking applications governed by Bangladesh Bank regulations exhibit significantly stronger technical compliance evidence than non-financial sectors (e.g., e-commerce, government services, transportation, utilities)?
- **Formal Target**: Hypothesis testing ($H_0$: no difference in compliance profiles across sectors vs. $H_1$: financial apps have higher Evidence-Supported Compliance ($ESC$)).
- **Measurement**: Kruskal-Wallis / Mann-Whitney U test on sectoral evidence scores.

#### **RQ6: Third-Party SDK Ecosystem Exposure**
- **Question**: To what extent do third-party Software Development Kits (advertising, analytics, social, crash trackers) participate in the extraction, transmission, or exfiltration of sensitive Bangladeshi user data?
- **Formal Target**: SDK dependency attribution and data-flow reachability analysis.
- **Measurement**: Number and category of third-party SDKs receiving sensitive PII (IMEI, phone, IMSI, location, clipboard) without application-level encryption.

#### **RQ7: Temporal Stability & Regulatory Decoupling**
- **Question**: How stable is the framework when regulatory specifications evolve, and can updates to the Regulation-as-Code knowledge base be applied without modifying the underlying program analysis engines?
- **Formal Target**: Longitudinal evaluation across application version histories ($v_{1}, v_{2}, \dots$) and simulated regulatory version revisions ($v_{\text{draft}} \to v_{\text{gazette}}$).
- **Measurement**: Maintenance effort, rule portability, delta diffs in compliance profiles across software releases.

#### **RQ8: Usability of Evidence-Grounded Multi-Lingual Explanations**
- **Question**: Does evidence-grounded, provenance-preserving reporting in Bengali and English significantly improve comprehension, risk identification, and developer remediation accuracy compared to raw technical scanning outputs?
- **Formal Target**: Controlled human-subjects experiment (Condition A: Raw tool output, Condition B: English structured explanation, Condition C: Localized Bengali evidence summary).
- **Measurement**: Task completion accuracy, comprehension rating, System Usability Scale (SUS), cognitive load (NASA-TLX).
