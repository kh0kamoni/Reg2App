# User Study Protocol: Multilingual Usable-Security Evaluation (RQ8)

## 1. Objective & Hypothesis
Investigate whether evidence-grounded multilingual explanations (Bengali vs. English vs. Raw Diagnostics) significantly enhance risk identification, comprehension, and developer remediation accuracy.

- **$H_1$**: Evidence-grounded Bengali explanations (Condition C) result in significantly higher comprehension and lower cognitive load (NASA-TLX) for native Bengali users than raw outputs (Condition A).
- **$H_2$**: Structured English provenance reports (Condition B) and Bengali reports (Condition C) yield significantly higher developer remediation accuracy than raw scanner traces (Condition A).

---

## 2. Experimental Design
- **Design**: $3 	imes 3$ Within-Subjects Latin Square counterbalanced design.
- **Participants**: $N = 60$
  - Cohort 1: 30 Professional Android / Software Engineers in Bangladesh.
  - Cohort 2: 30 General Smartphone Users (Consumers of MFS/Banking apps).
- **Conditions**:
  - **Condition A**: Raw tool diagnostic trace (MobSF-style).
  - **Condition B**: Structured Evidence-Grounded English Report.
  - **Condition C**: Localized Evidence-Grounded Bengali (?????) Report.

---

## 3. Dependent Measures
1. **Risk Identification Accuracy**: Score on 10 objective questions regarding application safety (0?100%).
2. **Developer Remediation Precision**: Identification of correct code-level remediation actions (0?100%).
3. **Task Completion Time**: Recorded in seconds per evaluation scenario.
4. **Cognitive Load**: Evaluated via the NASA-TLX 6-dimensional index (0?100).
5. **System Usability Scale (SUS)**: Standard 10-item instrument (0?100).
