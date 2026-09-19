from typing import List, Dict, Any
from reg2app.ontology.models import NormalizedEvidence, TechnicalMappingItem, StatutoryClause, StatutoryRegulation

class EvidenceGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_finding_provenance(
        self,
        regulation: StatutoryRegulation,
        clause: StatutoryClause,
        mapping: TechnicalMappingItem,
        evidence: NormalizedEvidence
    ):
        finding_id = evidence.finding_id
        clause_id = clause.clause_id
        control_id = mapping.technical_control.control_id
        rule_id = mapping.evidence_rule.rule_id

        # Record provenance record
        provenance = {
            "finding_id": finding_id,
            "regulation_id": regulation.regulation_id,
            "regulation_title": regulation.title,
            "clause_id": clause_id,
            "statutory_category": clause.statutory_category.value,
            "statutory_text": clause.text_en,
            "obligation": mapping.obligation.category,
            "control_id": control_id,
            "control_name": mapping.technical_control.name,
            "property_id": mapping.program_property.property_id,
            "property_name": mapping.program_property.name,
            "rule_id": rule_id,
            "evidence": {
                "modality": evidence.modality.value,
                "component_type": evidence.location.component_type,
                "file_path": evidence.location.file_path,
                "class_name": evidence.location.class_name,
                "method_name": evidence.location.method_name,
                "line_number": evidence.location.line_number,
                "extracted_value": evidence.extracted_value,
                "strength": evidence.evidence_strength.value,
                "is_violation": evidence.is_violation,
                "description": evidence.description
            }
        }
        self.nodes[finding_id] = provenance
        return provenance

    def get_audit_trail(self, finding_id: str) -> Dict[str, Any]:
        return self.nodes.get(finding_id, {})

    def get_all_provenance_records(self) -> List[Dict[str, Any]]:
        return list(self.nodes.values())
