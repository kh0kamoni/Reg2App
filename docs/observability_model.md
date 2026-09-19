# Observability Model & Evidence Modality Taxonomy

## 1. Motivation
A common methodological flaw in software compliance research is treating all regulatory requirements as uniformly verifiable through client-side binary analysis. In reality, an APK scanner has only partial visibility into an organization's security posture. 

To address this, **Reg2App** introduces an explicit two-dimensional epistemic boundary:
1. **Observability Level** ($L$): How completely an Android artifact can decide conformance.
2. **Evidence Modality** ($M$): The technical or operational environment where evidence must be gathered.

---

## 2. Observability Levels

For any regulatory requirement $R_i$, its observability level $L(R_i)$ is defined over the domain:
$$\mathcal{L} = \{\text{FULL}, \text{PARTIAL}, \text{NONE}\}$$

| Level | Definition | Example Regulatory Clause | Machine-Observable Interpretation |
| :--- | :--- | :--- | :--- |
| **FULL** | Client-side artifacts are necessary and sufficient to determine conformance. | Cleartext network communications are prohibited (BB-CSF 4.1.3.12) | Manifest `android:usesCleartextTraffic="false"` and network security config without cleartext permits. |
| **PARTIAL** | Client-side behavior provides necessary technical evidence, but external context (user consent, backend safeguards, contracts) is required for complete determination. | Sensitive personal data shall not be shared with third parties without consent (PDPA Section 6) | Data-flow reachability from sensitive PII sources (`getDeviceId()`) to third-party ad SDK network endpoints. |
| **NONE** | Requirement is purely governance, physical, operational, or legal, completely unobservable from mobile artifacts. | The Organization shall ensure visitors are escorted at all times in active port areas (BB-CSF 4.1.3.23) | Out-of-scope for programmatic bytecode/runtime verification. |

---

## 3. Evidence Modality Taxonomy

The evidence modality indicates the instrumentation surface required to substantiate or refute technical conformance:

$$\mathcal{M} = \{\text{STATIC}, \text{DYNAMIC}, \text{HYBRID}, \text{BACKEND}, \text{ORGANIZATIONAL}, \text{LEGAL}\}$$

### A. Technically Observable Modalities (Automated by Reg2App)
1. **STATIC ($	ext{STATIC}$)**: Observable via inspection of AndroidManifest.xml, Dalvik bytecode (DEX), native libraries (`.so`), resources, and network security configuration.
   - *Techniques*: AST parsing, manifest inspection, cryptographic API pattern matching, Call Graph (CG) analysis, Intra-procedural / Inter-procedural Taint Analysis.
2. **DYNAMIC ($	ext{DYNAMIC}$)**: Observable only during active execution on an Android device or instrumented emulator.
   - *Techniques*: Dynamic binary instrumentation (Frida), network TLS inspection / mitmproxy, runtime permission requests, memory scraping.
3. **HYBRID ($	ext{HYBRID}$)**: Requires static reachability identification corroborated by runtime traffic or dynamic activation.
   - *Example*: Static identification of an unpinned TLS client corroborated by dynamic interception of intercepted sessions.

### B. Out-of-Scope / Non-Programmatic Modalities (Explicitly Partitioned)
4. **BACKEND ($	ext{BACKEND}$)**: Properties governing remote server-side storage, database encryption, server TLS configurations, or microservice isolation.
5. **ORGANIZATIONAL ($	ext{ORGANIZATIONAL}$)**: Internal administrative policies, personnel screening, vendor contracts, disaster recovery drills, incident response team drills.
6. **LEGAL ($	ext{LEGAL}$)**: Sovereign authority requests, statutory exemptions, legitimate interest balancing tests, legal entity registrations.

---

## 4. Formal Observability Tuple

Every regulatory requirement $R_i$ is mapped through an observability operator:
$$\Omega(R_i) = (L_i, \mathcal{M}_i, \Phi_i)$$
where:
- $L_i \in \{\text{FULL}, \text{PARTIAL}, \text{NONE}\}$ is the observability level.
- $\mathcal{M}_i \subseteq \mathcal{M}$ is the set of applicable modalities.
- $\Phi_i$ is the methodological limitation rationale, documenting why full observability cannot be attained.
