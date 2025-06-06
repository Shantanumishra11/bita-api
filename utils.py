import pandas as pd

def generate_quarter_end_dates(start, end):
    return pd.date_range(start, end, freq='Q').strftime('%Y-%m-%d').tolist()

def apply_top_n_filter(row, n):
    return row.nlargest(n).index.tolist()

def apply_value_filter(row, p):
    return row[row > p].index.tolist()

def apply_equal_weighting(securities):
    n = len(securities)
    return {s: round(1/n, 6) for s in securities}

def apply_optimized_weighting(securities, values, lb, ub):
    sorted_securities = values[securities].sort_values(ascending=False)
    weights = {}
    remaining = 1.0
    for sec in sorted_securities.index:
        weight = min(ub, max(lb, remaining / len(sorted_securities)))
        weights[sec] = round(weight, 6)
        remaining -= weight
        if remaining <= 0:
            break
    total = sum(weights.values())
    return {k: round(v / total, 6) for k, v in weights.items()}

