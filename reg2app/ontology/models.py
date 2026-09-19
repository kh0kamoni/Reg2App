from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class StatutoryCategory(str, Enum):
    GOVERNANCE = "GOVERNANCE"
    DATA_PROTECTION = "DATA_PROTECTION"
    APPLICATION_SECURITY = "APPLICATION_SECURITY"
    INFRASTRUCTURE_SECURITY = "INFRASTRUCTURE_SECURITY"
    CRYPTOGRAPHY = "CRYPTOGRAPHY"
    AUDIT_LOGGING = "AUDIT_LOGGING"
    INCIDENT_RESPONSE = "INCIDENT_RESPONSE"
    PENAL_SANCTIONS = "PENAL_SANCTIONS"

class PrimaryEntity(str, Enum):
    DATA_CONTROLLER = "DATA_CONTROLLER"
    DATA_PROCESSOR = "DATA_PROCESSOR"
    BANK = "BANK"
    MFS_PROVIDER = "MFS_PROVIDER"
    PAYMENT_OPERATOR = "PAYMENT_OPERATOR"
    ALL_ORGANIZATIONS = "ALL_ORGANIZATIONS"
    GENERAL_CITIZEN = "GENERAL_CITIZEN"

class StatutoryClause(BaseModel):
    clause_id: str
    chapter: str
    chapter_title: str
    section: str
    section_title: Optional[str] = None
    text_bn: Optional[str] = None
    text_en: str
    statutory_category: StatutoryCategory
    primary_entity: PrimaryEntity

class StatutoryRegulation(BaseModel):
    regulation_id: str
    title: str
    short_title: str
    jurisdiction: str
    enacting_authority: str
    act_number: Optional[str] = None
    gazette_date: Optional[str] = None
    effective_date: Optional[str] = None
    version: str
    official_language: str
    source_file: Optional[str] = None
    clauses: List[StatutoryClause]

class ObservabilityLevel(str, Enum):
    FULL = "FULL"
    PARTIAL = "PARTIAL"
    NONE = "NONE"

class EvidenceModality(str, Enum):
    STATIC = "STATIC"
    DYNAMIC = "DYNAMIC"
    HYBRID = "HYBRID"
    BACKEND = "BACKEND"
    ORGANIZATIONAL = "ORGANIZATIONAL"
    LEGAL = "LEGAL"

class Obligation(BaseModel):
    category: str
    description: str

class TechnicalControl(BaseModel):
    control_id: str
    name: str
    description: str

class ProgramProperty(BaseModel):
    property_id: str
    name: str
    target_platform: str = "Android"
    formal_specification: str

class Observability(BaseModel):
    level: ObservabilityLevel
    modalities: List[EvidenceModality]
    limitations_rationale: str

class EvidenceRule(BaseModel):
    rule_id: str
    analysis_type: str
    sources: Optional[List[str]] = None
    sinks: Optional[List[str]] = None
    conditions: Optional[List[str]] = None
    supported_criteria: str
    non_conformance_criteria: str
    insufficient_evidence_criteria: str

class ValidationInfo(BaseModel):
    status: str
    expert_raters: Optional[int] = None
    inter_rater_agreement: Optional[float] = None
    rationale: str

class TechnicalMappingItem(BaseModel):
    requirement_ref: str
    obligation: Obligation
    technical_control: TechnicalControl
    program_property: ProgramProperty
    observability: Observability
    evidence_rule: EvidenceRule
    validation: ValidationInfo

class TechnicalMapping(BaseModel):
    mapping_id: str
    regulation_id: str
    version: str
    mappings: List[TechnicalMappingItem]

class EvidenceStrength(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CONFIRMED = "CONFIRMED"

class EvidenceLocation(BaseModel):
    component_type: str
    file_path: str
    class_name: Optional[str] = None
    method_name: Optional[str] = None
    line_number: Optional[int] = None

class NormalizedEvidence(BaseModel):
    finding_id: str
    rule_id: str
    target_package: str
    apk_hash_sha256: str
    timestamp: str
    modality: EvidenceModality
    location: EvidenceLocation
    dataflow: Optional[Dict[str, Any]] = None
    extracted_value: Optional[str] = None
    evidence_strength: EvidenceStrength
    description: str
    is_violation: bool = True
    raw_artifact_ref: Optional[str] = None

class ComplianceState(str, Enum):
    Supported = "Supported"
    PotentialNonConformance = "PotentialNonConformance"
    InsufficientEvidence = "InsufficientEvidence"
    NotObservable = "NotObservable"
    NotApplicable = "NotApplicable"

class RequirementAssessment(BaseModel):
    requirement_id: str
    regulation_id: str
    clause: StatutoryClause
    mapping: TechnicalMappingItem
    state: ComplianceState
    evidence_items: List[NormalizedEvidence] = []
    assessment_rationale: str
