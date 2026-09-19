from typing import List, Dict, Any
from reg2app.analyzers.base import BaseAnalyzer
from reg2app.ontology.models import NormalizedEvidence, EvidenceModality, EvidenceStrength

class DataflowEngine(BaseAnalyzer):
    def analyze(self, dataflow_context: Dict[str, Any]) -> List[NormalizedEvidence]:
        evidences = []
        pii_network_flows = dataflow_context.get("pii_to_insecure_network", [])
        pii_log_flows = dataflow_context.get("pii_to_logcat", [])
        obfuscation_info = dataflow_context.get("obfuscation", {})

        # 1. PII to insecure network (RULE-DATAFLOW-PII-TO-HTTP)
        if pii_network_flows:
            for flow in pii_network_flows[:5]:
                evidences.append(self.create_evidence(
                    rule_id="RULE-DATAFLOW-PII-TO-HTTP",
                    modality=EvidenceModality.STATIC,
                    component_type="BYTECODE",
                    file_path=flow.get("class_name", "classes.dex"),
                    class_name=flow.get("class_name"),
                    method_name=flow.get("method_name"),
                    line_number=flow.get("line_number"),
                    dataflow={
                        "source": flow.get("source"),
                        "sink": flow.get("sink"),
                        "intermediate_hops": flow.get("hops", [])
                    },
                    description=f"Taint flow path detected: personal identifier ({flow.get('source')}) reaches unencrypted network sink ({flow.get('sink')}).",
                    evidence_strength=EvidenceStrength.HIGH,
                    extracted_value=f"{flow.get('source')} -> {flow.get('sink')}",
                    is_violation=True
                ))
        elif dataflow_context.get("safe_network_transmission", False):
            evidences.append(self.create_evidence(
                rule_id="RULE-DATAFLOW-PII-TO-HTTP",
                modality=EvidenceModality.STATIC,
                component_type="BYTECODE",
                file_path="classes.dex",
                description="Personal identifiers transmitted strictly via authenticated, encrypted TLS channels.",
                evidence_strength=EvidenceStrength.HIGH,
                extracted_value="Secure TLS transmission verified",
                is_violation=False
            ))

        # 2. PII to Logcat (RULE-DATAFLOW-PII-TO-LOG)
        if pii_log_flows:
            for log_flow in pii_log_flows[:5]:
                evidences.append(self.create_evidence(
                    rule_id="RULE-DATAFLOW-PII-TO-LOG",
                    modality=EvidenceModality.STATIC,
                    component_type="BYTECODE",
                    file_path=log_flow.get("class_name", "classes.dex"),
                    class_name=log_flow.get("class_name"),
                    method_name=log_flow.get("method_name"),
                    line_number=log_flow.get("line_number"),
                    description=f"Personal data or credential field ({log_flow.get('field')}) emitted to Android Logcat sink ({log_flow.get('sink')}).",
                    evidence_strength=EvidenceStrength.HIGH,
                    extracted_value=f"{log_flow.get('field')} in Logcat",
                    is_violation=True
                ))
        elif dataflow_context.get("clean_logging", False):
            evidences.append(self.create_evidence(
                rule_id="RULE-DATAFLOW-PII-TO-LOG",
                modality=EvidenceModality.STATIC,
                component_type="BYTECODE",
                file_path="classes.dex",
                description="Zero customer credentials or PII fields detected in logging statements.",
                evidence_strength=EvidenceStrength.HIGH,
                extracted_value="Sanitized logging verified",
                is_violation=False
            ))

        # 3. Obfuscation check (RULE-CODE-OBFUSCATION-CHECK)
        if obfuscation_info:
            ratio = obfuscation_info.get("ratio", 0.0)
            is_obfuscated = ratio >= 0.60
            evidences.append(self.create_evidence(
                rule_id="RULE-CODE-OBFUSCATION-CHECK",
                modality=EvidenceModality.STATIC,
                component_type="BYTECODE",
                file_path="classes.dex",
                description=f"Bytecode symbol obfuscation ratio: {ratio*100:.1f}% (threshold = 60.0%).",
                evidence_strength=EvidenceStrength.MEDIUM,
                extracted_value=f"Obfuscation ratio: {ratio:.2f}",
                is_violation=(not is_obfuscated)
            ))

        return evidences
