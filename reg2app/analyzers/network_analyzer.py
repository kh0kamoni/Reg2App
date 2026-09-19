from typing import List, Dict, Any
from reg2app.analyzers.base import BaseAnalyzer
from reg2app.ontology.models import NormalizedEvidence, EvidenceModality, EvidenceStrength

class NetworkAnalyzer(BaseAnalyzer):
    def analyze(self, network_context: Dict[str, Any]) -> List[NormalizedEvidence]:
        evidences = []
        nsc = network_context.get("network_security_config", {})
        cleartext_urls = network_context.get("cleartext_http_urls", [])

        # 1. Cleartext HTTP URLs in Bytecode (RULE-NET-CLEARTEXT-01)
        if cleartext_urls:
            for u in cleartext_urls[:5]:
                evidences.append(self.create_evidence(
                    rule_id="RULE-NET-CLEARTEXT-01",
                    modality=EvidenceModality.STATIC,
                    component_type="BYTECODE",
                    file_path=u.get("class_name", "classes.dex"),
                    class_name=u.get("class_name"),
                    method_name=u.get("method_name"),
                    description=f"Unencrypted cleartext HTTP endpoint found in bytecode invocation: {u.get('url')}",
                    evidence_strength=EvidenceStrength.HIGH,
                    extracted_value=u.get("url"),
                    is_violation=True
                ))

        # 2. Network Security Config Permitting Cleartext
        if nsc.get("cleartextTrafficPermitted") is True:
            evidences.append(self.create_evidence(
                rule_id="RULE-NET-CLEARTEXT-01",
                modality=EvidenceModality.STATIC,
                component_type="RESOURCE",
                file_path="res/xml/network_security_config.xml",
                description="Network security config explicitly permits cleartext HTTP communications.",
                evidence_strength=EvidenceStrength.HIGH,
                extracted_value="cleartextTrafficPermitted='true'",
                is_violation=True
            ))
        elif nsc.get("cleartextTrafficPermitted") is False and not cleartext_urls:
            evidences.append(self.create_evidence(
                rule_id="RULE-NET-CLEARTEXT-01",
                modality=EvidenceModality.STATIC,
                component_type="RESOURCE",
                file_path="res/xml/network_security_config.xml",
                description="Network security config strictly enforces HTTPS and forbids cleartext traffic.",
                evidence_strength=EvidenceStrength.HIGH,
                extracted_value="cleartextTrafficPermitted='false'",
                is_violation=False
            ))

        return evidences
