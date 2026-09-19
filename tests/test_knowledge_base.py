import os
import glob
import json
import yaml
import pytest
from jsonschema import validate, Draft7Validator

KB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "knowledge_base"))
SCHEMA_DIR = os.path.join(KB_DIR, "schema")
REGS_DIR = os.path.join(KB_DIR, "regulations")
MAPS_DIR = os.path.join(KB_DIR, "mappings")

def test_json_schemas_are_valid():
    schema_files = glob.glob(os.path.join(SCHEMA_DIR, "*.json"))
    assert len(schema_files) >= 3, "Expected at least 3 schema files"
    for sf in schema_files:
        with open(sf, "r", encoding="utf-8") as f:
            data = json.load(f)
        Draft7Validator.check_schema(data)

def test_regulations_conform_to_schema():
    with open(os.path.join(SCHEMA_DIR, "regulation.schema.json"), "r", encoding="utf-8") as f:
        reg_schema = json.load(f)
    
    reg_files = glob.glob(os.path.join(REGS_DIR, "*.yaml"))
    assert len(reg_files) >= 3, "Expected at least 3 regulation files"
    
    for rf in reg_files:
        with open(rf, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        validate(instance=data, schema=reg_schema)
        assert "clauses" in data
        assert len(data["clauses"]) > 0

def test_mappings_conform_to_schema():
    with open(os.path.join(SCHEMA_DIR, "mapping.schema.json"), "r", encoding="utf-8") as f:
        map_schema = json.load(f)
    
    map_files = glob.glob(os.path.join(MAPS_DIR, "*.yaml"))
    assert len(map_files) >= 3, "Expected at least 3 mapping files"
    
    for mf in map_files:
        with open(mf, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        validate(instance=data, schema=map_schema)
        assert "mappings" in data
        assert len(data["mappings"]) > 0

def test_cross_reference_integrity():
    # Load all valid clause IDs from regulations
    valid_clauses = {}
    for rf in glob.glob(os.path.join(REGS_DIR, "*.yaml")):
        with open(rf, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        reg_id = data["regulation_id"]
        valid_clauses[reg_id] = {c["clause_id"] for c in data["clauses"]}

    # Verify each mapping references an existing clause
    for mf in glob.glob(os.path.join(MAPS_DIR, "*.yaml")):
        with open(mf, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        reg_id = data["regulation_id"]
        assert reg_id in valid_clauses, f"Mapping {mf} references unknown regulation {reg_id}"
        
        for m in data["mappings"]:
            req_ref = m["requirement_ref"]
            assert req_ref in valid_clauses[reg_id], (
                f"Mapping in {mf} references non-existent clause {req_ref} in {reg_id}"
            )

def test_observability_completeness():
    for mf in glob.glob(os.path.join(MAPS_DIR, "*.yaml")):
        with open(mf, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        for m in data["mappings"]:
            obs = m["observability"]
            assert obs["level"] in ["FULL", "PARTIAL", "NONE"]
            assert len(obs["modalities"]) > 0
            for mod in obs["modalities"]:
                assert mod in ["STATIC", "DYNAMIC", "HYBRID", "BACKEND", "ORGANIZATIONAL", "LEGAL"]
            assert len(obs["limitations_rationale"].strip()) > 10
