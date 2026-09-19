import os
import glob
import yaml
from typing import Dict, List, Tuple
from reg2app.ontology.models import StatutoryRegulation, TechnicalMapping, TechnicalMappingItem, StatutoryClause

def get_kb_paths(base_dir=None):
    if base_dir is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "knowledge_base"))
    return {
        "regulations": os.path.join(base_dir, "regulations"),
        "mappings": os.path.join(base_dir, "mappings"),
        "schema": os.path.join(base_dir, "schema")
    }

def load_all_regulations(regs_dir=None) -> Dict[str, StatutoryRegulation]:
    if regs_dir is None:
        regs_dir = get_kb_paths()["regulations"]
    
    regulations = {}
    for fpath in glob.glob(os.path.join(regs_dir, "*.yaml")):
        with open(fpath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        reg = StatutoryRegulation(**data)
        regulations[reg.regulation_id] = reg
    return regulations

def load_all_mappings(maps_dir=None) -> List[TechnicalMapping]:
    if maps_dir is None:
        maps_dir = get_kb_paths()["mappings"]
    
    mappings = []
    for fpath in glob.glob(os.path.join(maps_dir, "*.yaml")):
        with open(fpath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        m = TechnicalMapping(**data)
        mappings.append(m)
    return mappings

def get_paired_ontology() -> List[Tuple[StatutoryRegulation, StatutoryClause, TechnicalMappingItem]]:
    regs = load_all_regulations()
    maps = load_all_mappings()

    clauses_by_reg = {}
    for r_id, reg in regs.items():
        clauses_by_reg[r_id] = {c.clause_id: c for c in reg.clauses}

    paired = []
    for m in maps:
        reg = regs.get(m.regulation_id)
        if not reg:
            continue
        for item in m.mappings:
            clause = clauses_by_reg.get(m.regulation_id, {}).get(item.requirement_ref)
            if clause:
                paired.append((reg, clause, item))
    return paired
