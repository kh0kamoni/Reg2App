import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from reg2app.ontology.models import (
    NormalizedEvidence,
    EvidenceModality,
    EvidenceStrength,
    EvidenceLocation
)

class BaseAnalyzer:
    def __init__(self, target_package: str, apk_hash: str):
        self.target_package = target_package
        self.apk_hash = apk_hash

    def create_evidence(
        self,
        rule_id: str,
        modality: EvidenceModality,
        component_type: str,
        file_path: str,
        description: str,
        evidence_strength: EvidenceStrength = EvidenceStrength.HIGH,
        class_name: Optional[str] = None,
        method_name: Optional[str] = None,
        line_number: Optional[int] = None,
        dataflow: Optional[Dict[str, Any]] = None,
        extracted_value: Optional[str] = None,
        is_violation: bool = True
    ) -> NormalizedEvidence:
        return NormalizedEvidence(
            finding_id=f"EV-{uuid.uuid4().hex[:10].upper()}",
            rule_id=rule_id,
            target_package=self.target_package,
            apk_hash_sha256=self.apk_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
            modality=modality,
            location=EvidenceLocation(
                component_type=component_type,
                file_path=file_path,
                class_name=class_name,
                method_name=method_name,
                line_number=line_number
            ),
            dataflow=dataflow,
            extracted_value=extracted_value,
            evidence_strength=evidence_strength,
            description=description,
            is_violation=is_violation
        )

    def analyze(self, parsed_context: Any) -> List[NormalizedEvidence]:
        raise NotImplementedError
