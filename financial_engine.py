# financial_engine.py — Clean, minimal, Codespaces‑safe version
# (Replaces the broken file entirely — no exotic unicode chars, no invalid type hints)

import numpy as np

# --------------------------------------------------------
# Helper: apply scaling factors
# --------------------------------------------------------
def apply_scale(base_array, scale):
    return [v * scale for v in base_array]

# --------------------------------------------------------
# Core Financial Model
# --------------------------------------------------------
def compute_financials(params: dict):
    """
    params = {
        'mau_scale': float,
        'game_conv_scale': float,
        'course_conv_scale': float,
        'marketing_scale': float,
        'event_yield_scale': float,
        'content_cost_scale': float,
        'staff_scale': float,
        'srv_hw_scale': float
    }
    Returns: dictionary containing full financial arrays.
    """

    years = list(range(1, 15))

    # ----------------------------------------------------
    # Example base curves — replace later with spreadsheet logic
    # ----------------------------------------------------
    base_mau = [0, 60000, 300000, 600000, 1200000, 1600000, 2000000,
                2000000, 2000000, 2000000, 2000000, 2000000, 2000000, 2000000]

    base_revenues = [0, 1.3e6, 8.8e6, 24.6e6, 58.4e6, 96e6, 134e6,
                     148e6, 163e6, 177e6, 177e6, 177e6, 177e6, 177e6]

    base_costs = [5.6e6, 8.9e6, 16.6e6, 32.7e6, 52.4e6, 67e6, 87e6,
                  87e6, 88e6, 88e6, 88e6, 88e6, 88e6, 88e6]

    base_staff = [14, 23, 39, 54, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70]

    # ----------------------------------------------------
    # Apply user scaling
    # ----------------------------------------------------
    mau = apply_scale(base_mau, params.get('mau_scale', 1))

    revenues = apply_scale(base_revenues,
                           params.get('game_conv_scale', 1)
                           * params.get('course_conv_scale', 1))

    costs = apply_scale(base_costs,
                        params.get('staff_scale', 1)
                        * params.get('srv_hw_scale', 1))

    staff = apply_scale(base_staff, params.get('staff_scale', 1))

    profit = [r - c for r, c in zip(revenues, costs)]

    # CAC + ROAS (placeholder logic)
    cac = [max(1, c / max(m, 1)) for c, m in zip(costs, mau)]
    roas = [r / max(c, 1) for r, c in zip(revenues, costs)]

    # ----------------------------------------------------
    # Reasonability — placeholder: normal ranges
    # ----------------------------------------------------
    reasonability = {
        "mau": ["green" if m > 0 else "red" for m in mau],
        "revenues": ["green" if r > 0 else "red" for r in revenues],
        "staff": ["green" if s > 0 else "red" for s in staff],
        "cac": ["green" if x < 200 else "red" for x in cac],
        "roas": ["green" if x > 0.5 else "red" for x in roas]
    }

    return {
        "years": years,
        "mau": mau,
        "revenues": revenues,
        "costs": costs,
        "profit": profit,
        "staff": staff,
        "cac": cac,
        "roas": roas,
        "reasonability": reasonability,
    }
