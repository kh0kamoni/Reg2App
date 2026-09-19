import json
from typing import List, Dict, Any
from reg2app.analyzers.base import BaseAnalyzer
from reg2app.ontology.models import NormalizedEvidence, EvidenceModality, EvidenceStrength

class ManifestAnalyzer(BaseAnalyzer):
    DANGEROUS_PERMISSIONS = {
        "android.permission.READ_SMS": "Reads incoming and stored SMS messages containing OTPs and personal communications",
        "android.permission.SEND_SMS": "Sends arbitrary SMS messages potentially incurring charges",
        "android.permission.READ_CONTACTS": "Accesses address book and personal social graphs",
        "android.permission.READ_CALL_LOG": "Accesses telephony call history",
        "android.permission.ACCESS_FINE_LOCATION": "Harvests precise physical GPS coordinates",
        "android.permission.RECORD_AUDIO": "Records ambient microphone audio",
        "android.permission.CAMERA": "Captures raw camera video and photos",
        "android.permission.READ_PHONE_STATE": "Reads sensitive subscriber identifiers (IMEI, IMSI, SIM serial)"
    }

    def analyze(self, manifest_data: Dict[str, Any]) -> List[NormalizedEvidence]:
        evidences = []
        app_info = manifest_data.get("application", {})
        
        # 1. Cleartext Traffic Flag (RULE-NET-CLEARTEXT-01)
        uses_cleartext = app_info.get("usesCleartextTraffic")
        if uses_cleartext is True or uses_cleartext == "true":
            evidences.append(self.create_evidence(
                rule_id="RULE-NET-CLEARTEXT-01",
                modality=EvidenceModality.STATIC,
                component_type="MANIFEST",
                file_path="AndroidManifest.xml",
                description="Manifest explicitly enables cleartext network traffic (android:usesCleartextTraffic='true').",
                evidence_strength=EvidenceStrength.HIGH,
                extracted_value="android:usesCleartextTraffic='true'",
                is_violation=True
            ))
        elif uses_cleartext is False or uses_cleartext == "false":
            evidences.append(self.create_evidence(
                rule_id="RULE-NET-CLEARTEXT-01",
                modality=EvidenceModality.STATIC,
                component_type="MANIFEST",
                file_path="AndroidManifest.xml",
                description="Manifest explicitly prohibits cleartext network traffic (android:usesCleartextTraffic='false').",
                evidence_strength=EvidenceStrength.HIGH,
                extracted_value="android:usesCleartextTraffic='false'",
                is_violation=False
            ))

        # 2. AllowBackup Flag (RULE-MANIFEST-ALLOW-BACKUP)
        allow_backup = app_info.get("allowBackup")
        if allow_backup is True or allow_backup == "true" or allow_backup is None:
            evidences.append(self.create_evidence(
                rule_id="RULE-MANIFEST-ALLOW-BACKUP",
                modality=EvidenceModality.STATIC,
                component_type="MANIFEST",
                file_path="AndroidManifest.xml",
                description="Application allows ADB data backup extraction (android:allowBackup is true or omitted).",
                evidence_strength=EvidenceStrength.HIGH,
                extracted_value=f"android:allowBackup='{allow_backup}'",
                is_violation=True
            ))
        else:
            evidences.append(self.create_evidence(
                rule_id="RULE-MANIFEST-ALLOW-BACKUP",
                modality=EvidenceModality.STATIC,
                component_type="MANIFEST",
                file_path="AndroidManifest.xml",
                description="Application explicitly disables ADB data backup extraction (android:allowBackup='false').",
                evidence_strength=EvidenceStrength.HIGH,
                extracted_value="android:allowBackup='false'",
                is_violation=False
            ))

        # 3. Debuggable Flag (RULE-MANIFEST-DEBUGGABLE)
        debuggable = app_info.get("debuggable")
        if debuggable is True or debuggable == "true":
            evidences.append(self.create_evidence(
                rule_id="RULE-MANIFEST-DEBUGGABLE",
                modality=EvidenceModality.STATIC,
                component_type="MANIFEST",
                file_path="AndroidManifest.xml",
                description="Production APK is compiled with debugging enabled (android:debuggable='true').",
                evidence_strength=EvidenceStrength.HIGH,
                extracted_value="android:debuggable='true'",
                is_violation=True
            ))
        else:
            evidences.append(self.create_evidence(
                rule_id="RULE-MANIFEST-DEBUGGABLE",
                modality=EvidenceModality.STATIC,
                component_type="MANIFEST",
                file_path="AndroidManifest.xml",
                description="Application is compiled with debugging disabled (android:debuggable='false' or omitted).",
                evidence_strength=EvidenceStrength.HIGH,
                extracted_value="android:debuggable='false'",
                is_violation=False
            ))

        # 4. Dangerous Permissions (RULE-PERM-EXCESSIVE-DANGEROUS)
        permissions = manifest_data.get("permissions", [])
        category = manifest_data.get("declared_category", "GENERAL")
        
        # Sectoral whitelists (e.g. MFS may legitimately use SMS for OTP, but Calculator should not)
        allowed_by_category = {
            "MFS": {"android.permission.RECEIVE_SMS", "android.permission.READ_PHONE_STATE"},
            "BANKING": {"android.permission.RECEIVE_SMS", "android.permission.READ_PHONE_STATE"},
            "MAPS": {"android.permission.ACCESS_FINE_LOCATION", "android.permission.ACCESS_COARSE_LOCATION"},
            "GENERAL": set()
        }
        allowed = allowed_by_category.get(category, set())

        excessive_perms = []
        for p in permissions:
            if p in self.DANGEROUS_PERMISSIONS and p not in allowed:
                excessive_perms.append(p)

        if excessive_perms:
            evidences.append(self.create_evidence(
                rule_id="RULE-PERM-EXCESSIVE-DANGEROUS",
                modality=EvidenceModality.STATIC,
                component_type="MANIFEST",
                file_path="AndroidManifest.xml",
                description=f"Application requests dangerous permissions without sectoral justification: {', '.join(excessive_perms)}",
                evidence_strength=EvidenceStrength.HIGH,
                extracted_value=json.dumps(excessive_perms),
                is_violation=True
            ))
        else:
            evidences.append(self.create_evidence(
                rule_id="RULE-PERM-EXCESSIVE-DANGEROUS",
                modality=EvidenceModality.STATIC,
                component_type="MANIFEST",
                file_path="AndroidManifest.xml",
                description="Application permission requests strictly align with declared sectoral baseline.",
                evidence_strength=EvidenceStrength.HIGH,
                extracted_value="Zero excessive permissions",
                is_violation=False
            ))

        # 5. Exported Components (RULE-MANIFEST-EXPORTED-UNPROTECTED)
        components = manifest_data.get("exported_components", [])
        unprotected = [c for c in components if c.get("exported") and not c.get("permission")]
        if unprotected:
            comp_names = [f"{c.get('type')}:{c.get('name')}" for c in unprotected[:5]]
            evidences.append(self.create_evidence(
                rule_id="RULE-MANIFEST-EXPORTED-UNPROTECTED",
                modality=EvidenceModality.STATIC,
                component_type="MANIFEST",
                file_path="AndroidManifest.xml",
                description=f"Application exposes unprotected exported components without permissions: {', '.join(comp_names)}",
                evidence_strength=EvidenceStrength.HIGH,
                extracted_value=json.dumps(comp_names),
                is_violation=True
            ))
        elif components:
            evidences.append(self.create_evidence(
                rule_id="RULE-MANIFEST-EXPORTED-UNPROTECTED",
                modality=EvidenceModality.STATIC,
                component_type="MANIFEST",
                file_path="AndroidManifest.xml",
                description="All exported components are properly guarded by explicit permissions.",
                evidence_strength=EvidenceStrength.HIGH,
                extracted_value="Protected exported components",
                is_violation=False
            ))

        return evidences
