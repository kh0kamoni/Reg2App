# Scope, Threat Model, and Methodological Boundaries

## 1. Scope of the Research Framework

### In-Scope
1. **Target Artifacts**: Production Android Application Packages (APK) and Android App Bundles (AAB) distributed for use within the territory of Bangladesh.
2. **Regulatory Regimes (Bangladesh Proving Ground)**:
   - **Personal Data Protection Act, 2026 (PDPA)**: Focus on Chapter 2 (Principles), Chapter 3 (Data Subject Rights), Chapter 4 (Fiduciary Obligations / Security), and Chapter 5 (Cross-Border Transfer).
   - **Bangladesh Bank Cybersecurity Framework v1.0 (BB-CSF, Feb 2025/2026)**: Focus on Section 4 (Protect: IAM, Application Security, Cryptography, Data Security) and Section 5 (Detect: Logging & Tamper Resistance).
   - **Cyber Security Act, 2026 (CSA, Act 81 of 2026)**: Focus on provisions concerning computer system integrity, unauthorized access prevention, and Critical Information Infrastructure (CII) touchpoints.
3. **Analysis Modalities**: Deterministic static analysis of Android manifests, bytecode, resources, alongside instrumented dynamic tracing.

### Out-of-Scope
1. **Legal Determinations**: Reg2App does NOT provide legal advice or legal compliance certifications.
2. **Server-Side Architecture**: Remote server storage configurations, database encryption-at-rest, and cloud provider security controls cannot be directly audited from client APKs.
3. **Organizational Policies**: Human resource policies, physical security, vendor management contracts, and incident response governance.

---

## 2. Three-Layer Claim Boundary

To prevent reviewer overreach and maintain scientific validity, Reg2App operates strictly across three demarcated layers:

```
???????????????????????????????????????????????????????????????
? Layer 1: Program Analysis Facts (PROVEN EMPIRICALLY)        ?
? "Method M transmits IMEI to http://api.tracker.com"         ?
???????????????????????????????????????????????????????????????
? Layer 2: Technical Regulatory Evidence (FORMALIZED MAPPING)  ?
? "This flow is technical evidence of potential               ?
? non-conformance with PDPA Section 15 (Security Safeguards)" ?
???????????????????????????????????????????????????????????????
? Layer 3: Legal Compliance Verdict (EXPLICITLY DISCLAIMED)   ?
? "The publisher has violated Bangladesh law"                 ?
? ??? NEVER CLAIMED OR OUTPUT BY REG2APP ???                  ?
???????????????????????????????????????????????????????????????
```

---

## 3. Threat Model & Analysis Limitations

### A. Android Platform Realities
- **Dynamic Class Loading & Reflection**: Obfuscated or reflective invocations may obscure source-sink flows statically.
- **Native Code (JNI / C++)**: Sensitive operations executed in `.so` shared libraries are partially opaque to Dalvik static taint tracking.
- **Third-Party SDK Updates**: SDKs may alter behavior via server-side feature flags without APK binary modification.

### B. Evidentiary Safeguards
- When static analysis cannot definitively prove path reachability, findings are classified as `InsufficientEvidence` rather than `PotentialNonConformance`.
- All rules preserve raw execution traces and AST coordinates for human expert re-verification.
