# The 5-State Assessment Model & Provenance Engine

## 1. Epistemic Principle: Evidence, Not Legal Judgments
Reg2App never produces a simplistic percentage score (e.g., "78% Compliant") nor does it issue binding legal verdicts ("This app violates Section 15 of PDPA"). 

Instead, the framework produces an **Evidence-Based Technical Compliance Profile** evaluated over a 5-state discrete lattice:

$$\mathcal{S} = \{ \text{Supported}, \text{PotentialNonConformance}, \text{InsufficientEvidence}, \text{NotObservable}, \text{NotApplicable} \}$$

---

## 2. Assessment State Definitions

For any requirement $R_i$ applied to an application $A$:

1. **`Supported`**:
   - Technical evidence demonstrates that the concrete technical control $C_i$ required by $R_i$ is properly implemented and active.
   - *Example*: App enforces Certificate Pinning and disables plaintext HTTP in `network_security_config.xml`.

2. **`PotentialNonConformance`**:
   - Technical evidence indicates the presence of a pattern, data flow, or configuration that directly contradicts the technical control $C_i$.
   - *Example*: App transmits unencrypted NID / phone numbers to an external HTTP endpoint, or uses hardcoded DES keys.

3. **`InsufficientEvidence`**:
   - The requirement is technically observable ($L \in \{\text{FULL}, \text{PARTIAL}\}$), but available static/dynamic evidence is inconclusive (e.g., dead code paths, heavily obfuscated reflective invocations without dynamic activation, or truncated trace).
   - *Example*: Taint analysis indicates PII reaches a native JNI call whose internal sink cannot be statically verified.

4. **`NotObservable`**:
   - The requirement has observability level $L = \text{NONE}$ (governance, legal, physical, organizational).
   - *Example*: BB-CSF Requirement 4.1.6.4 (contractual agreements with employees).

5. **`NotApplicable`**:
   - The requirement applies only to specific application categories or operational contexts that do not match application $A$.
   - *Example*: Bangladesh Bank financial transaction integrity controls evaluated against a pure news reader or utility app.

---

## 3. Evidence Strength Hierarchy

Evidence items are tagged with qualitative strength categories based on evidentiary rigor:

$$\text{Strength}(e) \in \{ \text{CONFIRMED}, \text{HIGH}, \text{MEDIUM}, \text{LOW} \}$$

- **CONFIRMED**: Dual-modality verification (Static taint flow verified by dynamic packet capture or Frida hook).
- **HIGH**: High-confidence inter-procedural data flow analysis with full source-to-sink path and concrete manifest configurations.
- **MEDIUM**: Intra-procedural flow or structural detection without path feasibility proof (heuristic API match).
- **LOW**: Keyword occurrence, decompilation artifact, or unresolved reflective call.

---

## 4. The 7-Tuple Mapping Model

Every regulatory interpretation is formalized as:
$$M_i = (R_i, O_i, C_i, P_i, E_i, A_i, V_i)$$

- $R_i$: Statutory requirement identifier (e.g., `BB-CSF-4.1.3.12`, `PDPA-SEC-15`).
- $O_i$: High-level security/privacy obligation category.
- $C_i$: Concrete technical control specification.
- $P_i$: Formal program property to be verified in Dalvik/Android environment.
- $E_i$: Evidence rule (sources, sinks, conditions, inspection targets).
- $A_i$: Applicability scope and observability tuple $(L_i, \mathcal{M}_i)$.
- $V_i$: Expert validation status, rationales, and known threats to validity.

---

## 5. Provenance-Preserving Traceability

Every finding in Reg2App emits a strict provenance chain:
$$\text{Regulation Clause} \longrightarrow \text{Technical Control} \longrightarrow \text{Detection Rule} \longrightarrow \text{APK Artifact} \longrightarrow \text{Code Location (Class/Method)} \longrightarrow \text{Evidence Strength}$$
This eliminates black-box heuristics and ensures reproducibility and developer auditability.
