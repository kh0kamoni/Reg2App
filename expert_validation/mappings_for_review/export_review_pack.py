import os
import glob
import json
import yaml

def export_pack():
    kb_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "knowledge_base"))
    regs_dir = os.path.join(kb_dir, "regulations")
    maps_dir = os.path.join(kb_dir, "mappings")
    out_path = os.path.join(os.path.dirname(__file__), "review_pack.json")

    # Load all regulations into lookup table
    clauses_lookup = {}
    for rf in glob.glob(os.path.join(regs_dir, "*.yaml")):
        with open(rf, "r", encoding="utf-8") as f:
            rdata = yaml.safe_load(f)
        reg_title = rdata.get("title", "")
        for c in rdata.get("clauses", []):
            clauses_lookup[c["clause_id"]] = {
                "regulation_id": rdata.get("regulation_id"),
                "regulation_title": reg_title,
                "clause_id": c["clause_id"],
                "section": c["section"],
                "section_title": c.get("section_title", ""),
                "statutory_text_en": c.get("text_en", ""),
                "statutory_text_bn": c.get("text_bn", ""),
                "statutory_category": c.get("statutory_category", "")
            }

    # Build review pack
    review_items = []
    for mf in glob.glob(os.path.join(maps_dir, "*.yaml")):
        with open(mf, "r", encoding="utf-8") as f:
            mdata = yaml.safe_load(f)
        
        for idx, item in enumerate(mdata.get("mappings", [])):
            req_ref = item["requirement_ref"]
            clause_info = clauses_lookup.get(req_ref, {})
            
            review_item = {
                "item_id": f"REV-{mdata.get('regulation_id')}-{idx+1:02d}",
                "statutory_reference": clause_info,
                "technical_mapping": {
                    "obligation": item.get("obligation", {}),
                    "technical_control": item.get("technical_control", {}),
                    "program_property": item.get("program_property", {}),
                    "observability": item.get("observability", {}),
                    "evidence_rule": item.get("evidence_rule", {}),
                    "authors_rationale": item.get("validation", {}).get("rationale", "")
                },
                "expert_evaluation_form": {
                    "D1_statutory_faithfulness_likert_1_to_5": None,
                    "D2_property_validity_likert_1_to_5": None,
                    "D3_observability_calibration": None,
                    "D4_assessment_strength_defensibility": None,
                    "expert_comments": ""
                }
            }
            review_items.append(review_item)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_items": len(review_items),
            "protocol_version": "1.0",
            "items": review_items
        }, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Exported {len(review_items)} review items to {out_path}")

if __name__ == "__main__":
    export_pack()
