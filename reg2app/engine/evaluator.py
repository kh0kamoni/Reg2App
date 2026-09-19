from typing import List, Dict, Any
from reg2app.ontology.models import (
    StatutoryRegulation,
    StatutoryClause,
    TechnicalMappingItem,
    NormalizedEvidence,
    ComplianceState,
    RequirementAssessment,
    ObservabilityLevel
)
from reg2app.ontology.loader import get_paired_ontology
from reg2app.evidence.graph import EvidenceGraph

class ComplianceEvaluator:
    def __init__(self, ontology=None):
        self.ontology = ontology or get_paired_ontology()

    def evaluate(
        self,
        evidences: List[NormalizedEvidence],
        app_package: str = "com.example.app",
        app_sector: str = "MFS"
    ) -> Dict[str, Any]:
        graph = EvidenceGraph()
        assessments: List[RequirementAssessment] = []
        
        # Index evidences by rule_id
        evidences_by_rule: Dict[str, List[NormalizedEvidence]] = {}
        for ev in evidences:
            evidences_by_rule.setdefault(ev.rule_id, []).append(ev)

        state_counts = {s.value: 0 for s in ComplianceState}

        for reg, clause, mapping in self.ontology:
            rule_id = mapping.evidence_rule.rule_id
            obs_level = mapping.observability.level
            matching_evidences = evidences_by_rule.get(rule_id, [])

            # Check 1: Observability
            if obs_level == ObservabilityLevel.NONE:
                state = ComplianceState.NotObservable
                rationale = f"Requirement is organizational or legal and cannot be technically observed from Android artifacts ({mapping.observability.limitations_rationale})."
            
            # Check 2: Sector applicability (e.g. Bangladesh Bank requirements apply to financial entities)
            elif reg.regulation_id == "BB-CSF-V1-2026" and app_sector not in ["MFS", "BANKING", "FINTECH"]:
                state = ComplianceState.NotApplicable
                rationale = f"Bangladesh Bank Cybersecurity Framework does not apply to non-financial sector '{app_sector}'."

            # Check 3: Evidence-based state determination
            elif not matching_evidences:
                state = ComplianceState.InsufficientEvidence
                rationale = "No static or dynamic program evidence was observed for this technical property."
            
            else:
                # Check for violations
                violations = [e for e in matching_evidences if e.is_violation]
                supports = [e for e in matching_evidences if not e.is_violation]

                if violations:
                    state = ComplianceState.PotentialNonConformance
                    v_desc = "; ".join(v.description for v in violations[:2])
                    rationale = f"Observed technical behaviors contradict control {mapping.technical_control.control_id}: {v_desc}"
                    for v in violations:
                        graph.add_finding_provenance(reg, clause, mapping, v)
                elif supports:
                    state = ComplianceState.Supported
                    s_desc = "; ".join(s.description for s in supports[:2])
                    rationale = f"Technical safeguards conform to control {mapping.technical_control.control_id}: {s_desc}"
                    for s in supports:
                        graph.add_finding_provenance(reg, clause, mapping, s)
                else:
                    state = ComplianceState.InsufficientEvidence
                    rationale = "Available evidence is inconclusive or exhibits low evidentiary confidence."

            state_counts[state.value] += 1
            assessments.append(RequirementAssessment(
                requirement_id=clause.clause_id,
                regulation_id=reg.regulation_id,
                clause=clause,
                mapping=mapping,
                state=state,
                evidence_items=matching_evidences,
                assessment_rationale=rationale
            ))

        # Scientific Metrics
        total_reqs = len(assessments)
        applicable_count = total_reqs - state_counts[ComplianceState.NotApplicable.value]
        observable_count = applicable_count - state_counts[ComplianceState.NotObservable.value]
        assessed_count = state_counts[ComplianceState.Supported.value] + state_counts[ComplianceState.PotentialNonConformance.value]

        coverage = assessed_count / observable_count if observable_count > 0 else 0.0
        supported_ratio = (
            state_counts[ComplianceState.Supported.value] / assessed_count
            if assessed_count > 0 else 0.0
        )

        return {
            "application": {
                "package_name": app_package,
                "sector": app_sector,
                "total_regulations_evaluated": len(set(r.regulation_id for r, _, _ in self.ontology))
            },
            "summary_profile": {
                "Supported": state_counts[ComplianceState.Supported.value],
                "PotentialNonConformance": state_counts[ComplianceState.PotentialNonConformance.value],
                "InsufficientEvidence": state_counts[ComplianceState.InsufficientEvidence.value],
                "NotObservable": state_counts[ComplianceState.NotObservable.value],
                "NotApplicable": state_counts[ComplianceState.NotApplicable.value],
                "TotalRequirements": total_reqs
            },
            "metrics": {
                "EvidenceCoverage": round(coverage, 4),
                "EvidenceSupportedCompliance": round(supported_ratio, 4)
            },
            "provenance_records": graph.get_all_provenance_records(),
            "assessments": [a.model_dump() for a in assessments]
        }
