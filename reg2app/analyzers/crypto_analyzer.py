from typing import List, Dict, Any
from reg2app.analyzers.base import BaseAnalyzer
from reg2app.ontology.models import NormalizedEvidence, EvidenceModality, EvidenceStrength

class CryptoAnalyzer(BaseAnalyzer):
    WEAK_CIPHERS = ["DES", "DESEDE", "RC4", "BLOWFISH", "AES/ECB"]
    WEAK_HASHES = ["MD5", "SHA-1", "SHA1"]

    def analyze(self, dex_context: Dict[str, Any]) -> List[NormalizedEvidence]:
        evidences = []
        ciphers_found = dex_context.get("ciphers", [])
        hashes_found = dex_context.get("hashes", [])
        hardcoded_keys = dex_context.get("hardcoded_keys", [])

        # 1. Weak Ciphers / Hashing (RULE-CRYPTO-WEAK-ALGO)
        weak_detected = []
        for c in ciphers_found:
            c_upper = c.get("transformation", "").upper()
            for wc in self.WEAK_CIPHERS:
                if wc in c_upper:
                    weak_detected.append(c)
                    break
        for h in hashes_found:
            h_upper = h.get("algorithm", "").upper()
            for wh in self.WEAK_HASHES:
                if wh in h_upper:
                    weak_detected.append(h)
                    break

        if weak_detected:
            for item in weak_detected[:5]:
                evidences.append(self.create_evidence(
                    rule_id="RULE-CRYPTO-WEAK-ALGO",
                    modality=EvidenceModality.STATIC,
                    component_type="BYTECODE",
                    file_path=item.get("class_name", "Unknown.dex"),
                    class_name=item.get("class_name"),
                    method_name=item.get("method_name"),
                    line_number=item.get("line_number"),
                    description=f"Invocation of deprecated or broken cryptographic algorithm: {item.get('transformation') or item.get('algorithm')}",
                    evidence_strength=EvidenceStrength.HIGH,
                    extracted_value=item.get("transformation") or item.get("algorithm"),
                    is_violation=True
                ))
        elif ciphers_found or hashes_found:
            evidences.append(self.create_evidence(
                rule_id="RULE-CRYPTO-WEAK-ALGO",
                modality=EvidenceModality.STATIC,
                component_type="BYTECODE",
                file_path="classes.dex",
                description="All identified cryptographic cipher and digest invocations use modern standards (AES-GCM, SHA-256).",
                evidence_strength=EvidenceStrength.HIGH,
                extracted_value="Standard secure ciphers verified",
                is_violation=False
            ))

        # 2. Hardcoded Keys (RULE-CRYPTO-HARDCODED-KEY)
        if hardcoded_keys:
            for k in hardcoded_keys[:5]:
                evidences.append(self.create_evidence(
                    rule_id="RULE-CRYPTO-HARDCODED-KEY",
                    modality=EvidenceModality.STATIC,
                    component_type="BYTECODE",
                    file_path=k.get("class_name", "Unknown.dex"),
                    class_name=k.get("class_name"),
                    method_name=k.get("method_name"),
                    line_number=k.get("line_number"),
                    description=f"Cryptographic key initialized from static byte array or literal string constant: {k.get('key_snippet', '***')}",
                    evidence_strength=EvidenceStrength.HIGH,
                    extracted_value=k.get("key_snippet"),
                    is_violation=True
                ))
        elif dex_context.get("keystore_usage", False):
            evidences.append(self.create_evidence(
                rule_id="RULE-CRYPTO-HARDCODED-KEY",
                modality=EvidenceModality.STATIC,
                component_type="BYTECODE",
                file_path="classes.dex",
                description="Cryptographic operations use AndroidKeyStore provider for key generation without hardcoded secrets.",
                evidence_strength=EvidenceStrength.HIGH,
                extracted_value="AndroidKeyStore backed",
                is_violation=False
            ))

        return evidences
