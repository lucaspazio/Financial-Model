from typing import Dict, Any, List

YEARS: List[int] = list(range(1, 15))

# === Baseline vectors taken from "Hyp Financials" sheet (rows indicated) ===

BASE_MAU = [  # row 5 - Average MAU
    0,
    60000,
    300000,
    600000,
    1200000,
    1600000,
    2000000,
    2000000,
    2000000,
    2000000,
    2000000.0,
    2000000.0,
    2000000.0,
    2000000.0,
]

BASE_CONV_GAME = [  # row 12 - In-game conversion ratio
    0.01,
    0.01,
    0.01,
    0.02,
    0.02,
    0.03,
    0.03,
    0.03,
    0.03,
    0.03,
    0.03,
    0.03,
    0.03,
    0.03,
]

BASE_CONV_PREMIUM = [  # row 16 - Premium conversion ratio
    0.01,
    0.01,
    0.01,
    0.02,
    0.02,
    0.03,
    0.03,
    0.03,
    0.03,
    0.03,
    0.03,
    0.03,
    0.03,
    0.03,
]

BASE_CONV_SMALL = [  # row 33 - Small courses conversion ratio
    0.001,
    0.001,
    0.0015,
    0.002,
    0.0025,
    0.003,
    0.0035,
    0.004,
    0.0045,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
]

BASE_CONV_CERT = [  # row 36 - Certifying path conversion ratio
    0.001,
    0.001,
    0.0015,
    0.002,
    0.0025,
    0.003,
    0.0035,
    0.004,
    0.0045,
    0.005,
    0.005,
    0.005,
    0.005,
    0.005,
]

BASE_REV_GAME = [  # row 11 - "Game" revenues (in-game + ads + premium)
    0,
    447129,
    2235645,
    6971580,
    13943160,
    25258320,
    31572900,
    31572900,
    31572900,
    31572900,
    31572900.0,
    31572900.0,
    31572900.0,
    31572900.0,
]

BASE_REV_FORMATION = [  # row 32 - "Formation" revenues (courses + cert)
    0,
    862560,
    6469200,
    17251200,
    43128000,
    69004800,
    100632000,
    115008000,
    129384000,
    143760000,
    143760000.0,
    143760000.0,
    143760000.0,
    143760000.0,
]

BASE_REV_XR = [  # row 40 - XR + D events revenues
    0,
    10000,
    94000,
    382000,
    1340000,
    1820000,
    2240000,
    2240000,
    2240000,
    2240000,
    2240000.0,
    2240000.0,
    2240000.0,
    2240000.0,
]

BASE_SALARIES = [  # row 66
    1193500,
    1819000,
    2793000,
    4225000,
    5445000,
    5445000,
    5445000,
    5445000,
    5445000,
    5445000,
    5445000.0,
    5445000.0,
    5445000.0,
    5445000.0,
]

BASE_STAFF_COUNT = [  # row 79
    14.25,
    23,
    39,
    54,
    70,
    70,
    70,
    70,
    70,
    70,
    70.0,
    70.0,
    70.0,
    70.0,
]

BASE_SRV_HW_COEFF = [  # row 82 (not directly used yet, kept for future)
    3,
    2.5,
    2,
    2,
    1.5,
    1.5,
    1.5,
    1.5,
    1.5,
    1.5,
    1.5,
    1.5,
    1.5,
    1.5,
]

BASE_COST_HW = [  # row 81 - Services & HW cost as in Excel
    3580500,
    4547500,
    5586000,
    8450000,
    8167500,
    8167500,
    8167500,
    8167500,
    8167500,
    8167500,
    8167500.0,
    8167500.0,
    8167500.0,
    8167500.0,
]

BASE_COST_WEB3 = [  # row 97
    0,
    0,
    550000,
    550000,
    750000,
    750000,
    750000,
    750000,
    750000,
    750000,
    750000.0,
    750000.0,
    750000.0,
    750000.0,
]

BASE_COST_GAME_DEV = [  # row 102
    200000,
    350000,
    450000,
    350000,
    350000,
    350000,
    350000,
    350000,
    350000,
    350000,
    350000.0,
    350000.0,
    350000.0,
    350000.0,
]

BASE_COST_FORMATION = [  # row 104
    60000,
    700000,
    1700000,
    3500000,
    7000000,
    7000000,
    7000000,
    7000000,
    7000000,
    7000000,
    7000000.0,
    7000000.0,
    7000000.0,
    7000000.0,
]

BASE_COST_SPACE_SYSTEM = [  # row 110
    0,
    0,
    0,
    0,
    5000000,
    10000000,
    30000000,
    30000000,
    30000000,
    30000000,
    30000000.0,
    30000000.0,
    30000000.0,
    30000000.0,
]

BASE_COST_SPACE_OPS = [  # row 111
    0,
    0,
    0,
    0,
    0,
    0,
    500000,
    500000,
    1000000,
    1000000,
    1000000.0,
    1000000.0,
    1000000.0,
    1000000.0,
]

BASE_COST_PRICES = [  # row 113 - tournament prices
    0,
    2000,
    40000,
    120000,
    210000,
    210000,
    210000,
    210000,
    210000,
    210000,
    210000.0,
    210000.0,
    210000.0,
    210000.0,
]

BASE_MARKETING_COMPONENTS = {  # rows 122–125
    "events": [
        20000,
        20000,
        20000,
        20000,
        20000,
        20000,
        20000,
        20000,
        20000,
        20000,
        20000.0,
        20000.0,
        20000.0,
        20000.0,
    ],
    "sponsors": [
        500000,
        500000,
        500000,
        500000,
        500000,
        500000,
        500000,
        500000,
        500000,
        500000,
        500000.0,
        500000.0,
        500000.0,
        500000.0,
    ],
    "travels": [
        50000,
        50000,
        50000,
        50000,
        50000,
        50000,
        50000,
        50000,
        50000,
        50000,
        50000.0,
        50000.0,
        50000.0,
        50000.0,
    ],
    "publicity": [
        50000,
        1000000,
        5000000,
        15000000,
        25000000,
        35000000,
        35000000,
        35000000,
        35000000,
        35000000,
        35000000.0,
        35000000.0,
        35000000.0,
        35000000.0,
    ],
}


def _get_scale(params: Dict[str, Any], key: str, default: float = 1.0) -> float:
    try:
        val = float(params.get(key, default))
    except (TypeError, ValueError):
        val = default
    return max(val, 0.0)


def compute_financials(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Core financial engine.

    params comes from the frontend and typically contains:
      - mau_scale
      - conv_game_scale
      - conv_course_scale
      - marketing_scale
      - event_yield_scale
      - content_cost_scale
      - staff_scale
      - srv_hw_scale
    """

    mau_scale = _get_scale(params, "mau_scale", 1.0)
    conv_game_scale = _get_scale(params, "conv_game_scale", 1.0)
    conv_course_scale = _get_scale(params, "conv_course_scale", 1.0)
    marketing_scale = _get_scale(params, "marketing_scale", 1.0)
    event_yield_scale = _get_scale(params, "event_yield_scale", 1.0)
    content_cost_scale = _get_scale(params, "content_cost_scale", 1.0)
    staff_scale = _get_scale(params, "staff_scale", 1.0)
    srv_hw_scale = _get_scale(params, "srv_hw_scale", 1.0)

    # === 1) Scale core drivers ===

    mau = [base * mau_scale for base in BASE_MAU]

    # Game conversion & course conversion — we just scale ratios
    conv_game = [c * conv_game_scale for c in BASE_CONV_GAME]
    conv_premium = BASE_CONV_PREMIUM  # kept as-is, used in CAC paying
    conv_small = [c * conv_course_scale for c in BASE_CONV_SMALL]
    conv_cert = [c * conv_course_scale for c in BASE_CONV_CERT]

    # Marketing components
    mkt_events = [v * marketing_scale for v in BASE_MARKETING_COMPONENTS["events"]]
    mkt_sponsors = [v * marketing_scale for v in BASE_MARKETING_COMPONENTS["sponsors"]]
    mkt_travels = [v * marketing_scale for v in BASE_MARKETING_COMPONENTS["travels"]]
    mkt_publicity = [v * marketing_scale for v in BASE_MARKETING_COMPONENTS["publicity"]]

    marketing_total = [
        mkt_events[i]
        + mkt_sponsors[i]
        + mkt_travels[i]
        + mkt_publicity[i]
        for i in range(len(YEARS))
    ]

    # Event yields (XR + D revenues)
    rev_xr = [BASE_REV_XR[i] * event_yield_scale for i in range(len(YEARS))]

    # Formation/content costs
    cost_formation = [BASE_COST_FORMATION[i] * content_cost_scale for i in range(len(YEARS))]

    # Salaries & staff
    staff = [BASE_STAFF_COUNT[i] * staff_scale for i in range(len(YEARS))]
    cost_salaries = [BASE_SALARIES[i] * staff_scale for i in range(len(YEARS))]

    # Services & HW: derived from base HW cost, scaled by both staff & srv_hw scale
    cost_hw = [
        BASE_COST_HW[i] * staff_scale * srv_hw_scale for i in range(len(YEARS))
    ]

    # Web3 costs, game dev (kept fixed except content scaling could be added later)
    cost_web3 = BASE_COST_WEB3[:]
    cost_game_dev = BASE_COST_GAME_DEV[:]

    # === 2) Revenues, calibrated to keep Excel numbers at 1x ===

    game_rev: List[float] = []
    formation_rev: List[float] = []

    for i in range(len(YEARS)):
        base_m = BASE_MAU[i]
        base_g = BASE_REV_GAME[i]
        base_f = BASE_REV_FORMATION[i]

        if base_m > 0:
            # Effective revenue per MAU at baseline
            rev_per_m_game = base_g / base_m
            rev_per_m_form = base_f / base_m

            # Scale with both MAU and the respective conversion sliders
            game_rev.append(mau[i] * rev_per_m_game * conv_game_scale)
            formation_rev.append(mau[i] * rev_per_m_form * conv_course_scale)
        else:
            game_rev.append(0.0)
            formation_rev.append(0.0)

    revenues = [
        game_rev[i] + formation_rev[i] + rev_xr[i]
        for i in range(len(YEARS))
    ]

    # === 3) Space system costs driven by profitability (≥ 5M rule) ===

    SPACE_MIN_PROFIT = 5_000_000.0
    space_cost_used: List[float] = []
    profit_before_space: List[float] = []
    total_costs: List[float] = []
    profit: List[float] = []

    for i in range(len(YEARS)):
        # Costs that do NOT depend on the profit rule
        cost_marketing_i = marketing_total[i]
        cost_salaries_i = cost_salaries[i]
        cost_hw_i = cost_hw[i]
        cost_web3_i = cost_web3[i]
        cost_game_dev_i = cost_game_dev[i]
        cost_formation_i = cost_formation[i]
        cost_prices_i = BASE_COST_PRICES[i]

        # Sum partial costs (without space system & ops)
        partial_costs = (
            cost_marketing_i
            + cost_salaries_i
            + cost_hw_i
            + cost_web3_i
            + cost_game_dev_i
            + cost_formation_i
            + cost_prices_i
        )

        profit_before = revenues[i] - partial_costs

        # Planned space system + ops cost from Excel
        planned_space = BASE_COST_SPACE_SYSTEM[i] + BASE_COST_SPACE_OPS[i]

        if profit_before <= SPACE_MIN_PROFIT:
            # Not enough margin to sustain space system: invest 0 that year
            space_used = 0.0
        else:
            # Invest up to what keeps profit >= 5M
            max_affordable = profit_before - SPACE_MIN_PROFIT
            space_used = min(planned_space, max_affordable)

        total_cost_i = partial_costs + space_used
        profit_i = revenues[i] - total_cost_i

        profit_before_space.append(profit_before)
        space_cost_used.append(space_used)
        total_costs.append(total_cost_i)
        profit.append(profit_i)

    # === 4) CAC metrics (total & paying) ===

    RECURRENCY = 0.4  # 40% monthly recurrency as in F126

    new_users_raw: List[float] = []
    new_paying_users: List[float] = []
    cac_total: List[float] = []
    cac_paying: List[float] = []

    for i in range(len(YEARS)):
        if i == 0:
            prev_mau = 0.0
        else:
            prev_mau = mau[i - 1]

        # New users after accounting for recurrency (simplified adaptation of row 126)
        new_users = max(mau[i] - prev_mau * RECURRENCY, 0.0)
        new_users_raw.append(new_users)

        # Rough paying ratio = sum of the 4 conversion types
        paying_ratio = conv_game[i] + conv_premium[i] + conv_small[i] + conv_cert[i]
        paying_ratio = min(max(paying_ratio, 0.0), 1.0)

        new_paying = new_users * paying_ratio
        new_paying_users.append(new_paying)

        # Acquisition spend: we tie CAC to marketing budget
        acq_spend = marketing_total[i]

        if new_users > 0:
            cac_total.append(acq_spend / new_users)
        else:
            cac_total.append(0.0)

        if new_paying > 0:
            cac_paying.append(acq_spend / new_paying)
        else:
            cac_paying.append(0.0)

    # For reasonability & charts we expose "cac" as CAC per paying customer
    cac_for_charts = cac_paying

    # === 5) ROAS ===

    roas: List[float] = []
    for i in range(len(YEARS)):
        mkt = marketing_total[i]
        if mkt > 0:
            roas.append(revenues[i] / mkt)
        else:
            roas.append(0.0)

    # === 6) Build debug table (one row per year) ===

    debug_table: List[Dict[str, float]] = []
    for idx, year in enumerate(YEARS):
        debug_table.append(
            {
                "year": year,
                "mau": mau[idx],
                "game_revenue": game_rev[idx],
                "formation_revenue": formation_rev[idx],
                "xr_revenue": rev_xr[idx],
                "total_revenue": revenues[idx],
                "marketing_total": marketing_total[idx],
                "salaries": cost_salaries[idx],
                "services_hw": cost_hw[idx],
                "web3_cost": cost_web3[idx],
                "game_dev_cost": cost_game_dev[idx],
                "formation_cost": cost_formation[idx],
                "prices_cost": BASE_COST_PRICES[idx],
                "space_cost_used": space_cost_used[idx],
                "total_cost": total_costs[idx],
                "profit_before_space": profit_before_space[idx],
                "profit": profit[idx],
                "new_users": new_users_raw[idx],
                "new_paying_users": new_paying_users[idx],
                "cac_total": cac_total[idx],
                "cac_paying": cac_paying[idx],
                "roas": roas[idx],
                "staff": staff[idx],
            }
        )

    # === 7) Final results payload ===

    return {
        "years": YEARS,
        "mau": mau,
        "revenues": revenues,
        "costs": total_costs,
        "profit": profit,
        "staff": staff,
        "roas": roas,
        "cac": cac_for_charts,          # CAC per paying customer
        "cac_total": cac_total,         # CAC per new user
        "cac_paying": cac_paying,       # explicit alias
        "game_revenue": game_rev,
        "formation_revenue": formation_rev,
        "xr_revenue": rev_xr,
        "marketing_total": marketing_total,
        "space_cost_used": space_cost_used,
        "profit_before_space": profit_before_space,
        "debug_table": debug_table,
    }
