from typing import List, Dict, Any
from reg2app.analyzers.base import BaseAnalyzer
from reg2app.ontology.models import NormalizedEvidence, EvidenceModality, EvidenceStrength

class SDKAnalyzer(BaseAnalyzer):
    KNOWN_TRACKER_SDKS = {
        "com.facebook.ads": "Facebook Audience Network",
        "com.google.android.gms.ads": "Google AdMob",
        "com.appsflyer": "AppsFlyer Telemetry & Attribution",
        "com.adjust.sdk": "Adjust Attribution",
        "com.flurry": "Yahoo Flurry Analytics",
        "io.branch": "Branch.io Deep Linking & Tracking"
    }

    def analyze(self, sdk_context: Dict[str, Any]) -> List[NormalizedEvidence]:
        evidences = []
        packages_present = sdk_context.get("third_party_packages", [])
        sdk_id_flows = sdk_context.get("sdk_identifier_flows", [])

        # 1. Tracker SDK identifier exfiltration (RULE-SDK-TRACKER-PII-FLOW)
        if sdk_id_flows:
            for flow in sdk_id_flows[:5]:
                sdk_pkg = flow.get("sdk_package", "tracker_sdk")
                sdk_name = self.KNOWN_TRACKER_SDKS.get(sdk_pkg, sdk_pkg)
                evidences.append(self.create_evidence(
                    rule_id="RULE-SDK-TRACKER-PII-FLOW",
                    modality=EvidenceModality.STATIC,
                    component_type="BYTECODE",
                    file_path=flow.get("class_name", "classes.dex"),
                    class_name=flow.get("class_name"),
                    method_name=flow.get("method_name"),
                    description=f"Device/subscriber identifier passed directly to third-party tracker SDK ({sdk_name}): {flow.get('source_field')}",
                    evidence_strength=EvidenceStrength.HIGH,
                    extracted_value=f"{sdk_name} <- {flow.get('source_field')}",
                    is_violation=True
                ))
        elif not any(tp in self.KNOWN_TRACKER_SDKS for tp in packages_present):
            evidences.append(self.create_evidence(
                rule_id="RULE-SDK-TRACKER-PII-FLOW",
                modality=EvidenceModality.STATIC,
                component_type="BYTECODE",
                file_path="classes.dex",
                description="Zero third-party commercial advertising or behavioral tracking SDKs detected in application packages.",
                evidence_strength=EvidenceStrength.HIGH,
                extracted_value="Zero tracker SDKs detected",
                is_violation=False
            ))

        return evidences
