import json
import math
from collections import Counter

def compute_percent_agreement(ratings_matrix):
    """
    ratings_matrix: List of rows, where each row is list of ratings by raters for an item.
    """
    total_pairs = 0
    agreed_pairs = 0
    for row in ratings_matrix:
        n = len(row)
        for i in range(n):
            for j in range(i + 1, n):
                total_pairs += 1
                if row[i] == row[j]:
                    agreed_pairs += 1
    return agreed_pairs / total_pairs if total_pairs > 0 else 1.0

def compute_fleiss_kappa(ratings_matrix, categories):
    """
    Computes Fleiss' Kappa for N items rated by k raters into C categories.
    ratings_matrix: List of N lists, each having k ratings.
    categories: List of unique categories.
    """
    N = len(ratings_matrix)
    if N == 0:
        return 0.0
    k = len(ratings_matrix[0])
    if k <= 1:
        return 1.0
    
    cat_to_idx = {cat: i for i, cat in enumerate(categories)}
    n_categories = len(categories)
    
    # Table of counts n_ij: item i assigned to category j
    table = [[0] * n_categories for _ in range(N)]
    for i, row in enumerate(ratings_matrix):
        for r in row:
            if r in cat_to_idx:
                table[i][cat_to_idx[r]] += 1
    
    # Proportion of all assignments to category j
    p_j = [0.0] * n_categories
    for j in range(n_categories):
        total = sum(table[i][j] for i in range(N))
        p_j[j] = total / (N * k)
    
    # P_e = sum(p_j^2)
    P_e = sum(pj ** 2 for pj in p_j)
    
    # P_i for each item
    P_i = [0.0] * N
    for i in range(N):
        sum_sq = sum(table[i][j] ** 2 for j in range(n_categories))
        P_i[i] = (sum_sq - k) / (k * (k - 1))
    
    # P_bar
    P_bar = sum(P_i) / N
    
    if abs(1.0 - P_e) < 1e-9:
        return 1.0
    
    kappa = (P_bar - P_e) / (1.0 - P_e)
    return kappa

def compute_krippendorff_alpha_interval(ratings_matrix):
    """
    Computes Krippendorff's Alpha for interval / ordinal data.
    ratings_matrix: List of items, each item is a list of numerical ratings.
    """
    # Pairwise coincidence matrix
    pairs = []
    all_values = []
    for row in ratings_matrix:
        clean_row = [float(v) for v in row if v is not None]
        all_values.extend(clean_row)
        n = len(clean_row)
        for i in range(n):
            for j in range(n):
                if i != j:
                    pairs.append((clean_row[i], clean_row[j]))
    
    if not pairs:
        return 1.0
    
    # Observed disagreement
    d_obs = sum((x - y) ** 2 for x, y in pairs) / len(pairs)
    
    # Expected disagreement
    m = len(all_values)
    if m <= 1:
        return 1.0
    d_exp = 0.0
    total_exp_pairs = 0
    for i in range(m):
        for j in range(m):
            if i != j:
                d_exp += (all_values[i] - all_values[j]) ** 2
                total_exp_pairs += 1
    
    d_exp = d_exp / total_exp_pairs if total_exp_pairs > 0 else 1.0
    
    if abs(d_exp) < 1e-9:
        return 1.0
    
    alpha = 1.0 - (d_obs / d_exp)
    return alpha

if __name__ == "__main__":
    # Smoke test sample
    sample_nominal = [
        ["Accurate", "Accurate", "Accurate"],
        ["Accurate", "Accurate", "Accurate"],
        ["Accurate", "Underestimated", "Accurate"],
        ["Accurate", "Accurate", "Accurate"]
    ]
    cats = ["Accurate", "Underestimated", "Overestimated"]
    k = compute_fleiss_kappa(sample_nominal, cats)
    print(f"Sample Fleiss Kappa: {k:.3f}")
    
    sample_likert = [
        [5, 5, 4],
        [4, 5, 5],
        [5, 4, 4],
        [5, 5, 5]
    ]
    a = compute_krippendorff_alpha_interval(sample_likert)
    print(f"Sample Krippendorff Alpha: {a:.3f}")
