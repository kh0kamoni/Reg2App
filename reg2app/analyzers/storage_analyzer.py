from typing import List, Dict, Any
from reg2app.analyzers.base import BaseAnalyzer
from reg2app.ontology.models import NormalizedEvidence, EvidenceModality, EvidenceStrength

class StorageAnalyzer(BaseAnalyzer):
    SENSITIVE_FIELD_NAMES = ["password", "token", "pin", "auth", "secret", "cvv", "balance", "account"]

    def analyze(self, storage_context: Dict[str, Any]) -> List[NormalizedEvidence]:
        evidences = []
        prefs_writes = storage_context.get("shared_preferences_writes", [])
        world_readable = storage_context.get("world_readable_files", [])
        encrypted_prefs_used = storage_context.get("encrypted_shared_preferences_used", False)

        # 1. Plaintext storage of sensitive keys (RULE-STORAGE-PLAINTEXT-SECRETS)
        plaintext_violations = []
        for pw in prefs_writes:
            key_name = pw.get("key", "").lower()
            if any(s in key_name for s in self.SENSITIVE_FIELD_NAMES) and not encrypted_prefs_used:
                plaintext_violations.append(pw)

        for wr in world_readable:
            plaintext_violations.append(wr)

        if plaintext_violations:
            for item in plaintext_violations[:5]:
                evidences.append(self.create_evidence(
                    rule_id="RULE-STORAGE-PLAINTEXT-SECRETS",
                    modality=EvidenceModality.STATIC,
                    component_type="BYTECODE",
                    file_path=item.get("class_name", "Storage.dex"),
                    class_name=item.get("class_name"),
                    method_name=item.get("method_name"),
                    line_number=item.get("line_number"),
                    description=f"Sensitive data written to unencrypted local storage sink: {item.get('key') or item.get('file')}",
                    evidence_strength=EvidenceStrength.HIGH,
                    extracted_value=item.get("key") or item.get("file"),
                    is_violation=True
                ))
        elif encrypted_prefs_used:
            evidences.append(self.create_evidence(
                rule_id="RULE-STORAGE-PLAINTEXT-SECRETS",
                modality=EvidenceModality.STATIC,
                component_type="BYTECODE",
                file_path="classes.dex",
                description="Application employs EncryptedSharedPreferences with hardware-backed master key for sensitive data at rest.",
                evidence_strength=EvidenceStrength.HIGH,
                extracted_value="EncryptedSharedPreferences active",
                is_violation=False
            ))

        return evidences
