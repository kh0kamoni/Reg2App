import os
import json
import pytest
from expert_validation.agreement.calculate_agreement import (
    compute_percent_agreement,
    compute_fleiss_kappa,
    compute_krippendorff_alpha_interval
)

def test_review_pack_exists_and_valid():
    pack_path = os.path.join(
        os.path.dirname(__file__), "..", "expert_validation", "mappings_for_review", "review_pack.json"
    )
    assert os.path.exists(pack_path), "review_pack.json must exist"
    with open(pack_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "total_items" in data
    assert data["total_items"] >= 12
    assert len(data["items"]) == data["total_items"]
    
    for item in data["items"]:
        assert "item_id" in item
        assert "statutory_reference" in item
        assert "technical_mapping" in item
        assert "expert_evaluation_form" in item

def test_fleiss_kappa_perfect_agreement():
    matrix = [
        ["Accurate", "Accurate", "Accurate"],
        ["Overreach", "Overreach", "Overreach"],
        ["Accurate", "Accurate", "Accurate"]
    ]
    categories = ["Accurate", "Overreach", "Underreach"]
    kappa = compute_fleiss_kappa(matrix, categories)
    assert kappa == pytest.approx(1.0, rel=1e-3)

def test_krippendorff_alpha_perfect_agreement():
    matrix = [
        [5, 5, 5],
        [4, 4, 4],
        [3, 3, 3]
    ]
    alpha = compute_krippendorff_alpha_interval(matrix)
    assert alpha == pytest.approx(1.0, rel=1e-3)

def test_percent_agreement_calculation():
    matrix = [
        ["A", "A", "A"], # 3 pairs: (0,1), (0,2), (1,2) -> 3 agree
        ["A", "B", "A"]  # 3 pairs: (0,1) diff, (0,2) agree, (1,2) diff -> 1 agree
    ]
    # Total pairs = 6, agreed = 4 -> 4/6 = 0.6667
    pa = compute_percent_agreement(matrix)
    assert pa == pytest.approx(4/6, rel=1e-3)
