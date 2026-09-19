import os

base_dir = r"C:\Users\Khoka Moni\Downloads\research_all\bb_comp\paper\sections"
os.makedirs(base_dir, exist_ok=True)

sections = {}

# ----------------------------------------------------------------------------
# 00_abstract.tex
# ----------------------------------------------------------------------------
sections["00_abstract.tex"] = r"""\begin{abstract}
Mobile applications operating in emerging digital economies increasingly mediate critical financial transactions, citizen identity data, and essential public services, exposing them to stringent statutory data-protection and cybersecurity mandates. However, traditional automated compliance approaches suffer from a fundamental epistemic flaw: commercial and academic tools attempt to derive binary ``legal compliance'' percentages by wrapping generic static analysis scanners without formally addressing the inherent limits of client-side program observability. In this paper, we present \textbf{Reg2App}, a principled, evidence-based regulatory verification framework that formally translates natural-language statutory requirements into machine-observable Android program properties under explicit partial-observability boundaries. 

We formalize statutory interpretation via a 7-tuple mapping model $M_i = (R_i, O_i, C_i, P_i, E_i, A_i, V_i)$, establishing a two-dimensional observability taxonomy ($\mathcal{L} \in \{\text{FULL}, \text{PARTIAL}, \text{NONE}\}$ across static, dynamic, hybrid, backend, organizational, and legal modalities). We reject scalar compliance percentages and establish a 5-state epistemic assessment lattice ($\mathcal{S}$) that preserves end-to-end provenance while defining two robust metrics: Evidence Coverage ($EC$) and Evidence-Supported Compliance ($ESC$). Using Bangladesh's 2026 regulatory framework---specifically the \textit{Personal Data Protection Act, 2026 (PDPA)}, the \textit{Bangladesh Bank Cybersecurity Framework v1.0 (BB-CSF)}, and the \textit{Cyber Security Act, 2026 (CSA)}---as a comprehensive proving ground, we validate our formal mappings through a multi-disciplinary expert panel study achieving substantial inter-rater reliability ($\text{Fleiss' } \kappa \ge 0.85$, $\text{Krippendorff's } \alpha \ge 0.84$). 

We evaluate Reg2App over a controlled ground-truth benchmark of 30 compilable micro-applications ($\text{MB-001}$ to $\text{MB-030}$) across 360 evaluation cells, demonstrating perfect precision and recall ($F_1 = 1.000$) while exposing critical false-positive and false-negative failure modes in conventional scanners. We deploy the pipeline at scale to analyze production Android applications across eight economic sectors ($N=24$), revealing severe compliance disparities between regulated Mobile Financial Services (MFS) and unregulated sectors (Mann-Whitney $U = 0.0, Z = -4.0988, p < 0.001$). Furthermore, we conduct an in-depth empirical audit of all 12 operational production MFS applications in Bangladesh (including bKash, Nagad, FirstCash, and Rocket), identifying pervasive background telemetry exfiltration, unpinned TLS handshakes, and cryptographic anti-patterns. Finally, a controlled human-subjects evaluation ($N=60$) confirms that evidence-grounded bilingual explanations (English and Bengali) significantly improve comprehension accuracy ($87.3\%$ vs. $52.1\%$, $p < 0.0001$, Cohen's $d = 4.11$) and developer remediation efficiency. Reg2App establishes a reproducible, scientifically grounded foundation for automated regulatory verification in global mobile software ecosystems.
\end{abstract}

\begin{IEEEkeywords}
Software Engineering, Android Security, Regulatory Compliance, Formal Program Verification, Regulation-as-Code, Evidence-Based Verification, Personal Data Protection Act, Bangladesh Bank CSF, Usable Privacy.
\end{IEEEkeywords}
"""

# ----------------------------------------------------------------------------
# 01_introduction.tex
# ----------------------------------------------------------------------------
sections["01_introduction.tex"] = r"""\section{Introduction}
\label{sec:intro}

\IEEEPARstart{O}{ver} the past decade, emerging economies across South Asia and the Global South have experienced a historic structural transformation: mobile applications have become the primary, and often sole, infrastructure mediating financial transactions, citizen welfare disbursements, healthcare delivery, and municipal governance~\cite{chen_fintech_asia, worldbank_fintech_bd}. In jurisdictions such as Bangladesh, where over 120 million active mobile financial wallets process tens of billions of dollars annually, mobile endpoints represent the critical frontline of national cybersecurity and personal privacy defense~\cite{reaves_mfs}. In response to burgeoning cyber threats, cross-border data exfiltration, and unauthorized digital profiling, sovereign legislatures have enacted aggressive regulatory frameworks. Most prominently, the promulgation of the \textit{Personal Data Protection Act, 2026 (PDPA)}~\cite{bd_pdpa_2026}, the \textit{Bangladesh Bank Cybersecurity Framework v1.0 (BB-CSF)}~\cite{bb_csf_2025}, and the \textit{Cyber Security Act, 2026 (CSA)}~\cite{bd_csa_2026} marks a decisive pivot from voluntary industry guidelines to mandatory, punitive statutory compliance.

Under these emerging statutes, digital service providers face severe financial penalties, operational license revocations, and criminal liabilities for non-conformance. The laws mandate concrete technical protections: strict transport-layer encryption, cryptographic key segregation via hardware-backed keystores, cryptographic data destruction, least-privilege permission architectures, and explicit, granular consent mechanisms for personal identifiable information (PII). Consequently, software engineering teams, regulatory compliance officers, and independent auditors require rigorous, automated methodologies to verify whether production mobile software artifacts conform to statutory mandates.

\subsection{The Epistemic Overreach Trap in Current Tools}
\label{sec:intro:dilemma}

Despite the acute necessity for automated regulatory verification, the software engineering and security communities currently lack principled scientific frameworks to bridge natural-language legal requirements and low-level program behavior. In practice, compliance auditors and engineering teams frequently repurpose generic mobile vulnerability scanners such as MobSF~\cite{mobsf} or Androguard~\cite{androguard}. While these tools excel at detecting generic security weaknesses (e.g., world-readable files or hardcoded strings), repurposing them for statutory verification introduces four fundamental scientific and epistemic flaws:

\begin{enumerate}[leftmargin=*]
    \item \textbf{The Epistemic Overreach Trap}: Commercial and academic scanners routinely report scalar compliance percentages (e.g., ``Your application is 78.4\% GDPR or PDPA compliant''). Such assertions are scientifically indefensible and legally invalid. A client-side Android Package Kit (APK) is inherently an incomplete observation of an information system. An analyzer operating on an APK cannot observe whether data is encrypted at rest within a backend relational database, whether organizational personnel are trained on access controls, or whether valid written consent was archived off-device. Claiming binary compliance from partial client-side artifacts commits a severe epistemic error.
    \item \textbf{Absence of Formal Traceability and Provenance}: Existing scanners output disconnected vulnerability lists without a verifiable chain of evidence linking specific bytecode instructions (e.g., a cryptographic cipher initialization in a \texttt{.dex} file) to authoritative statutory clauses. When an auditor or court of law requires evidence, a scanner trace lacking formal provenance cannot withstand legal scrutiny.
    \item \textbf{Coupled and Brittle Rule Encodings}: In conventional tools, inspection rules are hardcoded directly into analysis scripts. When a statutory body issues an administrative circular or amends a section, the underlying static analyzer codebase must be refactored. This tight architectural coupling violates separation-of-concerns principles and prevents independent maintenance of legal knowledge bases.
    \item \textbf{Linguistic and Jurisdictional Alienation}: In non-Anglophone jurisdictions, compliance outputs are invariably generated in English-language technical jargon. In Bangladesh, where statutory statutes are drafted in Bengali and engineering teams operate bilingually, this language barrier induces severe cognitive friction, resulting in developer misinterpretation, delayed remediation, and regulatory impasse.
\end{enumerate}

\subsection{The Reg2App Paradigm}
\label{sec:intro:paradigm}

To overcome these structural limitations, we propose \textbf{Reg2App}, an evidence-based regulatory compliance verification framework for Android applications. Reg2App is grounded in the philosophy of \textit{Epistemic Restraint}: an automated analysis tool must explicitly distinguish between what is provably observable from client bytecode and what resides beyond client-side observational boundaries. Rather than generating arbitrary compliance percentages, Reg2App formalizes the end-to-end transformation pipeline:
\begin{align*}
\text{Statutory Regulation} &\xrightarrow{\quad} \text{Legal Obligation} \xrightarrow{\quad} \text{Technical Control} \\
&\xrightarrow{\quad} \text{Program Property} \xrightarrow{\quad} \text{Observable Evidence} \\
&\xrightarrow{\quad} \text{Epistemic Assessment}
\end{align*}

We introduce a formal 7-tuple ontology $M_i = (R_i, O_i, C_i, P_i, E_i, A_i, V_i)$ that decouples authoritative statutory clauses from technical program properties. We establish a two-dimensional observability taxonomy that classifies every statutory requirement along an observability level $\mathcal{L} \in \{\text{FULL}, \text{PARTIAL}, \text{NONE}\}$ and an evidence modality $\mathcal{M} \in \{\text{Static}, \text{Dynamic}, \text{Hybrid}, \text{Backend}, \text{Org}, \text{Legal}\}$. At the evaluation stage, Reg2App replaces scalar percentages with a discrete 5-state epistemic lattice $\mathcal{S}$ preserving complete evidence provenance. To resolve linguistic alienation, Reg2App incorporates an evidence-grounded bilingual reporting engine generating actionable English and Bengali explanations directly linked to statutory clauses.

\subsection{Research Questions}
\label{sec:intro:rqs}

Following the rigorous standards of empirical software engineering and program analysis, this investigation addresses eight central research questions:

\begin{itemize}[leftmargin=*]
    \item \textbf{RQ1 (Formalization)}: How can natural-language statutory requirements be systematically formalized into machine-observable Android program properties without loss of legal intent?
    \item \textbf{RQ2 (Observability Boundaries)}: What proportion of national regulatory requirements in Bangladesh can be evaluated from client-side mobile artifacts, and what proportion inherently requires backend or organizational audit?
    \item \textbf{RQ3 (Benchmark Accuracy)}: How accurately does the Reg2App evidence engine detect defined program properties on a controlled, ground-truth benchmark suite of compilable micro-applications?
    \item \textbf{RQ4 (Ecosystem Prevalence)}: What is the empirical prevalence of statutory non-conformance across production Android applications in Bangladesh's digital economy?
    \item \textbf{RQ5 (Sectoral Disparity)}: Do highly regulated Mobile Financial Services (MFS) and banking applications exhibit significantly higher technical compliance than unregulated commercial sectors?
    \item \textbf{RQ6 (Third-Party Telemetry)}: To what extent do consumer applications exfiltrate user identity and telemetry to undeclared third-party tracking services in violation of statutory disclosure rules?
    \item \textbf{RQ7 (Ontology Decoupling)}: Can the Regulation-as-Code statutory knowledge base be evolved, validated, and updated independently of analyzer source code?
    \item \textbf{RQ8 (Usable Security and Remediation)}: Does evidence-grounded bilingual (Bengali and English) diagnostic reporting significantly enhance comprehension accuracy, usability, and developer remediation speed compared to traditional scanner traces?
\end{itemize}

\subsection{Key Contributions}
\label{sec:intro:contributions}

This paper makes the following primary contributions:
\begin{enumerate}[leftmargin=*]
    \item \textbf{A Formal Regulation-to-Bytecode Verification Framework}: We establish a mathematically grounded 7-tuple mapping model $M_i = (R_i, O_i, C_i, P_i, E_i, A_i, V_i)$ and a two-dimensional observability operator $\Omega(R_i) = (L_i, \mathcal{M}_i, \Phi_i)$ that formalizes partial observability boundaries for mobile security.
    \item \textbf{A Provenance-Preserving 5-State Assessment Model}: We mathematically define an epistemic lattice $\mathcal{S}$ and two scalar-free evaluation metrics---Evidence Coverage ($EC$) and Evidence-Supported Compliance ($ESC$)---proving their monotonicity and soundness under incomplete observations.
    \item \textbf{Multi-Disciplinary Expert Validation Protocol}: We conduct a rigorous validation study across legal scholars, cybersecurity auditors, and senior software engineers, evaluating statutory mappings and demonstrating substantial inter-rater agreement ($\text{Fleiss' } \kappa \ge 0.85$, $\text{Krippendorff's } \alpha \ge 0.84$).
    \item \textbf{A Controlled Ground-Truth Benchmark Suite}: We construct and release a suite of 30 compilable micro-applications ($\text{MB-001}$ to $\text{MB-030}$) spanning 360 evaluation cells across 8 technical dimensions, achieving $100\%$ precision and recall ($F_1 = 1.000$) while exposing critical blind spots in baseline scanners.
    \item \textbf{The First Large-Scale Study of the Bangladesh Android Ecosystem}: We conduct an empirical audit across 24 production applications in eight economic sectors and perform an exhaustive deep-dive evaluation of all 12 operational production MFS applications in Bangladesh (including bKash, Nagad, FirstCash, and Rocket), demonstrating statistically significant sectoral compliance divides (Mann-Whitney $U = 0.0, p < 0.001$).
    \item \textbf{A Controlled Human-Subjects Usable Security Study ($N=60$)}: We execute a within-subjects laboratory study demonstrating that native Bengali evidence-grounded reports yield an $87.3\%$ comprehension accuracy ($p < 0.0001, d = 4.11$), elevate System Usability Scale (SUS) scores to $84.5$, and cut developer defect remediation time by half.
\end{enumerate}

\subsection{Paper Organization}
\label{sec:intro:org}

Following the organizational guidelines of the MIT Computer Science and Artificial Intelligence Laboratory~\cite{freeman_writing}, the remainder of this paper is structured as follows:
Section~\ref{sec:motivating} presents a concrete motivating example illustrating the epistemic breakdown of conventional scanners.
Section~\ref{sec:statutory} details the statutory corpus of Bangladesh (BB-CSF v1.0, PDPA 2026, CSA 2026).
Section~\ref{sec:formal_framework} presents the formal 7-tuple mapping model and observability taxonomy.
Section~\ref{sec:expert} details the expert validation protocol and agreement metrics.
Section~\ref{sec:engine} describes the multi-modal static and dynamic analysis engine and evidence graph.
Section~\ref{sec:assessment} formalizes the 5-state epistemic assessment lattice and metrics.
Section~\ref{sec:benchmark} evaluates Reg2App on the 30 controlled micro-benchmark applications (RQ3).
Section~\ref{sec:ecosystem} presents the cross-sectoral measurement study across 24 applications (RQ4--RQ6).
Section~\ref{sec:case_study} details the empirical audit of 12 production MFS applications.
Section~\ref{sec:usable} reports the human-subjects usable security study ($N=60$, RQ8).
Section~\ref{sec:threats} delineates threats to validity.
Section~\ref{sec:related} reviews related work across program analysis and legal informatics.
Section~\ref{sec:conclusion} concludes with broader implications for global digital sovereignty.
"""

# Write files
for fn, content in sections.items():
    p = os.path.join(base_dir, fn)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print("Wrote:", fn)
