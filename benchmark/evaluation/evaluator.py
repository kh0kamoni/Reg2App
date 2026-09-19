import json
import os

def evaluate_predictions(predictions, ground_truth_path=None):
    """
    predictions: dict of { benchmark_id: { rule_id: detected_non_conformance (bool) } }
    ground_truth_path: path to ground_truth.json
    """
    if ground_truth_path is None:
        ground_truth_path = os.path.join(os.path.dirname(__file__), "..", "ground_truth", "ground_truth.json")
    
    with open(ground_truth_path, "r", encoding="utf-8") as f:
        gt_data = json.load(f)
    
    matrix = gt_data["matrix"]
    all_rules = gt_data["rules"]

    rule_stats = {r: {"TP": 0, "FP": 0, "TN": 0, "FN": 0} for r in all_rules}
    global_stats = {"TP": 0, "FP": 0, "TN": 0, "FN": 0}

    for b_id, b_info in matrix.items():
        pred_b = predictions.get(b_id, {})
        for r_id, r_info in b_info["rules"].items():
            expected_flag = r_info["should_trigger_non_conformance"]
            predicted_flag = pred_b.get(r_id, False)

            if expected_flag and predicted_flag:
                rule_stats[r_id]["TP"] += 1
                global_stats["TP"] += 1
            elif not expected_flag and predicted_flag:
                rule_stats[r_id]["FP"] += 1
                global_stats["FP"] += 1
            elif expected_flag and not predicted_flag:
                rule_stats[r_id]["FN"] += 1
                global_stats["FN"] += 1
            else:
                rule_stats[r_id]["TN"] += 1
                global_stats["TN"] += 1

    def calc_metrics(stats):
        tp, fp, tn, fn = stats["TP"], stats["FP"], stats["TN"], stats["FN"]
        prec = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        fnr = fn / (fn + tp) if (fn + tp) > 0 else 0.0
        return {
            "TP": tp, "FP": fp, "TN": tn, "FN": fn,
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1": round(f1, 4),
            "FPR": round(fpr, 4),
            "FNR": round(fnr, 4)
        }

    per_rule_results = {r: calc_metrics(s) for r, s in rule_stats.items()}
    summary = calc_metrics(global_stats)

    return {
        "global_metrics": summary,
        "per_rule_metrics": per_rule_results
    }

if __name__ == "__main__":
    # Smoke test with perfect oracle predictions
    gt_file = os.path.join(os.path.dirname(__file__), "..", "ground_truth", "ground_truth.json")
    with open(gt_file, "r", encoding="utf-8") as f:
        gt = json.load(f)
    oracle_preds = {}
    for bid, binfo in gt["matrix"].items():
        oracle_preds[bid] = {rid: rinfo["should_trigger_non_conformance"] for rid, rinfo in binfo["rules"].items()}
    res = evaluate_predictions(oracle_preds, gt_file)
    print("Oracle Benchmark Evaluation:", json.dumps(res["global_metrics"], indent=2))
