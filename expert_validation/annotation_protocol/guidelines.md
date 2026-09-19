# Expert Validation Protocol & Annotation Guidelines

## 1. Study Objective
The objective of this expert validation study is to evaluate the scientific validity, legal faithfulness, and technical defensibility of the regulatory-to-program-property mappings formalized in **Reg2App**.

Experts are drawn from two distinct domains:
- **Cybersecurity & Android Security Researchers** ($E_{	ext{sec}}$: 3?5 experts)
- **Data Protection Lawyers & Legal Scholars** ($E_{	ext{law}}$: 2?3 experts)

---

## 2. Evaluation Dimensions

For each mapping tuple $M_i = (R_i, O_i, C_i, P_i, E_i, A_i, V_i)$, the reviewer independently answers four structured evaluation questions:

### **Dimension 1: Statutory Faithfulness (D1)**
- *Prompt*: Does the stated technical control $C_i$ faithfully capture the statutory intent and obligations of regulatory clause $R_i$?
- *Scale*: 5-point Likert scale (1 = Strongly Disagree, 2 = Disagree, 3 = Neutral, 4 = Agree, 5 = Strongly Agree).

### **Dimension 2: Program Property Validity (D2)**
- *Prompt*: Does the machine-observable Android program property $P_i$ constitute sound and valid technical evidence for the satisfaction or violation of technical control $C_i$?
- *Scale*: 5-point Likert scale (1 = Strongly Disagree, 2 = Disagree, 3 = Neutral, 4 = Agree, 5 = Strongly Agree).

### **Dimension 3: Observability Calibration (D3)**
- *Prompt*: Is the assigned Observability Level ($L_i \in \{	ext{FULL}, 	ext{PARTIAL}, 	ext{NONE}\}$) and modality set $\mathcal{M}_i$ methodologically accurate?
  - Can an Android APK/runtime artifact genuinely observe this property?
  - Does the limitation rationale properly account for platform boundaries?
- *Scale*: Nominal categorical rating (`Accurate`, `Underestimated`, `Overestimated`).

### **Dimension 4: Assessment Severity Defensibility (D4)**
- *Prompt*: When the detection rule triggers, is concluding **`PotentialNonConformance`** legally and technically defensible, or does it represent an evidentiary overreach?
- *Scale*: Categorical rating (`Defensible`, `Overreach - Should be InsufficientEvidence`, `Overreach - Should be Informational`).

---

## 3. Inter-Rater Reliability Thresholds
To claim publication-grade consensus, annotations must meet the following standard reliability metrics:
- **Fleiss' Kappa ($\kappa$)**: $\kappa \ge 0.70$ (Substantial Agreement) across categorical dimensions.
- **Krippendorff's Alpha ($lpha$)**: $lpha \ge 0.80$ across ordinal Likert dimensions.
