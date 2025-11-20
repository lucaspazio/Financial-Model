from flask import Flask, request, jsonify, make_response
import json
import math

app = Flask(__name__)

# -------------- FINANCIAL ENGINE ---------------- #

def compute_model(params: dict):
    """
    Compute a 14-year financial model replicating the Excel structure.

    Years index: 0..13  (corresponds to columns G..T, i.e. Year1..Year14)
    """

    n = 14
    idx = range(n)

    # ---- multipliers from front-end (stress test controls) ----
    mau_scale           = float(params.get("mau_scale", 1.0))
    conv_game_scale     = float(params.get("conv_game_scale", 1.0))
    conv_course_scale   = float(params.get("conv_course_scale", 1.0))
    marketing_scale     = float(params.get("marketing_scale", 1.0))
    content_cost_scale  = float(params.get("content_cost_scale", 1.0))
    event_yield_scale   = float(params.get("event_yield_scale", 1.0))

    # ========= INPUT LINES FROM EXCEL ========= #

    # Row 5: Average MAU (G..T)
    mau_base = [
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
        2000000,
        2000000,
        2000000,
        2000000,
    ][0:n]

    mau = [m * mau_scale for m in mau_base]

    # ---- Game monetisation ---- #
    # Row 12: converting ratio in-game
    conv_in_game_base = [0.01, 0.01, 0.01, 0.02, 0.02, 0.03, 0.03, 0.03,
                         0.03, 0.03, 0.03, 0.03, 0.03, 0.03][0:n]
    conv_in_game = [c * conv_game_scale for c in conv_in_game_base]

    # Row 16: converting ratio premium
    conv_premium_base = [0.01, 0.01, 0.01, 0.02, 0.02, 0.03, 0.03, 0.03,
                         0.03, 0.03, 0.03, 0.03, 0.03, 0.03][0:n]
    conv_premium = [c * conv_game_scale for c in conv_premium_base]

    # Prices
    price_in_game = 20.0   # F14
    price_premium = 15.0   # F18
    ad_ecpm       = 30.0   # F15, € per 1000 impressions
    ads_per_day_per_user = 0.3  # from Excel: *0.3

    # ---- Formation (courses) ---- #
    conv_small_course_base = [
        0.001, 0.001, 0.0015, 0.002, 0.0025, 0.003, 0.0035, 0.004,
        0.0045, 0.005, 0.005, 0.005, 0.005, 0.005
    ][0:n]
    conv_small_course = [c * conv_course_scale for c in conv_small_course_base]

    conv_cert_path_base = conv_small_course_base[:]   # row 36 identical
    conv_cert_path = [c * conv_course_scale for c in conv_cert_path_base]

    price_small_course = 199.0   # F35
    price_cert_path    = 999.0   # F38

    # ---- XR Events ---- #
    d_events = [0,1,2,6,12,12,12,12,12,12,12,12,12,12][0:n]        # row 41
    xr_events = [0,1,2,2,2,2,2,2,2,2,2,2,2,2][0:n]                  # row 42

    comp_d_per_event  = [0,50,100,200,500,1000,1000,1000,1000,1000,1000,1000,1000,1000][0:n]  # row 43
    comp_xr_per_event = [0,5,10,50,100,100,100,100,100,100,100,100,100,100][0:n]             # row 45

    reg_fee_d  = 10.0   # F47
    reg_fee_xr = 100.0  # F48
    ticket_conv_ratio = [0,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01][0:n]  # row 49
    ticket_price = 5.0  # F52

    # ---- Salaries ---- #
    # salary per FTE (row 67..75, 77..78)
    sal_mgmt       = 150000
    sal_blockchain = 120000
    sal_ai         = 120000
    sal_it         = 90000
    sal_content    = 90000
    sal_gamif      = 120000
    sal_mkt        = 100000
    sal_analyst    = 100000
    sal_space      = 120000
    sal_intern     = 6000
    sal_phd        = 35000

    # headcount per year (rows 67..75, 77..78; G..T)
    hc_mgmt       = [2,3,3,4,5,5,5,5,5,5,5,5,5,5][0:n]
    hc_blockchain = [2,2,3,4,6,6,6,6,6,6,6,6,6,6][0:n]
    hc_ai         = [1,2,3,4,5,5,5,5,5,5,5,5,5,5][0:n]
    hc_it         = [2,3,6,9,12,12,12,12,12,12,12,12,12,12][0:n]
    hc_content    = [1,1,2,2,3,3,3,3,3,3,3,3,3,3][0:n]
    hc_gamif      = [2,3,5,8,10,10,10,10,10,10,10,10,10,10][0:n]
    hc_mkt        = [1,2,4,8,10,10,10,10,10,10,10,10,10,10][0:n]
    hc_analyst    = [1,1,2,2,4,4,4,4,4,4,4,4,4,4][0:n]
    hc_space      = [0,1,2,2,4,4,4,4,4,4,4,4,4,4][0:n]
    hc_intern     = [9/4,4,8,10,10,10,10,10,10,10,10,10,10,10][0:n]
    hc_phd        = [0,1,1,1,1,1,1,1,1,1,1,1,1,1][0:n]

    # ---- Services & HW ---- #
    coeff_srv_hw = [3,2.5,2,2,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5][0:n]

    # ---- Web3 costs ---- #
    market_making = [0,0,200000,300000,500000,500000,500000,500000,500000,500000,500000,500000,500000,500000][0:n]
    exch_list     = [0,0,100000,0,0,0,0,0,0,0,0,0,0,0][0:n]
    web3_legal    = [0,0,250000,250000,250000,250000,250000,250000,250000,250000,250000,250000,250000,250000][0:n]

    # ---- Games & Platform Dev ---- #
    game_platform_dev = [350000,450000,350000,350000,350000,350000,350000,350000,
                         350000,350000,350000,350000,350000,350000][0:n]
    # Year 0 200k ignored in 14-year columns.

    # ---- Formation cost ---- #
    small_courses_count = [2,20,50,100,200,200,200,200,200,200,200,200,200,200][0:n]
    cert_paths_count    = [1,2,5,10,10,10,10,10,10,10,10,10,10,10][0:n]

    cost_small_course_per = 30000 * content_cost_scale  # F106
    cost_cert_per         = 100000 * content_cost_scale # F108

    # ---- Space System ---- #
    space_system_cost = [0,0,0,0,5000000,10000000,30000000,30000000,30000000,
                         30000000,30000000,30000000,30000000,30000000][0:n]
    space_ops_cost    = [0,0,0,0,0,0,500000,500000,1000000,1000000,1000000,1000000,1000000,1000000][0:n]

    # ---- Tournament prices (events pricing, separate from tickets) ---- #
    price_per_d_tourn  = [0,1000,10000,15000,15000,15000,15000,15000,15000,15000,15000,15000,15000,15000][0:n]
    price_per_xr_tourn = [0,1000,10000,15000,15000,15000,15000,15000,15000,15000,15000,15000,15000,15000][0:n]

    # ---- Marketing block ---- #
    events_cost   = [20000]*n                # row 122
    sponsors_cost = [500000]*n               # row 123
    travel_cost   = [50000]*n                # row 124
    publicity_base = [
        50000,1000000,5000000,15000000,25000000,
        35000000,35000000,35000000,35000000,35000000,
        35000000,35000000,35000000,35000000
    ][0:n]

    publicity = [p * marketing_scale for p in publicity_base]

    # ================== CALCULATIONS =================== #

    # ---- Game segment ---- #
    converted_in_game = [mau[i] * conv_in_game[i] for i in idx]
    in_game_sales = [converted_in_game[i] * price_in_game * 12 for i in idx]

    # Premium
    converted_premium = [mau[i] * conv_premium[i] for i in idx]
    premium_fee = [converted_premium[i] * price_premium * 12 for i in idx]

    # Ads
    paid_ads = [
        ad_ecpm * 365 * mau[i]/1000.0 * ads_per_day_per_user * (1.0 - conv_premium[i])
        for i in idx
    ]

    # Game total (row 11)
    game_total = [in_game_sales[i] + premium_fee[i] + paid_ads[i] for i in idx]

    # ---- Formation revenue ---- #
    conv_small_users = [conv_small_course[i]*mau[i] for i in idx]
    conv_cert_users  = [conv_cert_path[i]*mau[i]   for i in idx]

    small_course_sales = [conv_small_users[i] * price_small_course * 12 for i in idx]
    cert_path_sales    = [conv_cert_users[i]  * price_cert_path    * 12 for i in idx]

    formation_total = [small_course_sales[i] + cert_path_sales[i] for i in idx]

    # ---- Marketplace & Serious (currently 0 in your sheet) ---- #
    tokens_total = [0.0]*n
    marketplace_total = [0.0]*n
    serious_total = [0.0]*n

    # ---- XR game revenue ---- #
    overall_comp_d  = [comp_d_per_event[i]*d_events[i] for i in idx]
    overall_comp_xr = [comp_xr_per_event[i]*xr_events[i] for i in idx]

    tourn_reg_d  = [overall_comp_d[i]  * reg_fee_d  for i in idx]
    tourn_reg_xr = [overall_comp_xr[i] * reg_fee_xr for i in idx]

    tickets_per_event = [ticket_conv_ratio[i]*mau[i] for i in idx]
    total_ticket_units = [
        tickets_per_event[i]*(d_events[i]+xr_events[i]) for i in idx
    ]
    tickets_revenue = [total_ticket_units[i]*ticket_price for i in idx]

    # Sponsors revenue row 53: 2x in first year, then 0.5x
    sponsors_revenue = []
    for i in idx:
        if i == 0:
            sponsors_revenue.append(2.0 * tickets_revenue[i])
        else:
            sponsors_revenue.append(0.5 * tickets_revenue[i])
    # Apply event_yield_scale to all XR-related revenues
    tourn_reg_d  = [x * event_yield_scale for x in tourn_reg_d]
    tourn_reg_xr = [x * event_yield_scale for x in tourn_reg_xr]
    tickets_revenue = [x * event_yield_scale for x in tickets_revenue]
    sponsors_revenue = [x * event_yield_scale for x in sponsors_revenue]

    xr_total = [
        tourn_reg_d[i] + tourn_reg_xr[i] + tickets_revenue[i] + sponsors_revenue[i]
        for i in idx
    ]

    # ---- Revenues total (row 55) ---- #
    revenues = [
        tokens_total[i] + game_total[i] + serious_total[i] + xr_total[i] +
        formation_total[i] + marketplace_total[i]
        for i in idx
    ]

    # ---- Salaries (row 66) ---- #
    salaries = []
    for i in idx:
        total_sal = (
            hc_mgmt[i]       * sal_mgmt +
            hc_blockchain[i] * sal_blockchain +
            hc_ai[i]         * sal_ai +
            hc_it[i]         * sal_it +
            hc_content[i]    * sal_content +
            hc_gamif[i]      * sal_gamif +
            hc_mkt[i]        * sal_mkt +
            hc_analyst[i]    * sal_analyst +
            hc_space[i]      * sal_space +
            hc_intern[i]     * sal_intern +
            hc_phd[i]        * sal_phd
        )
        salaries.append(total_sal)

    # ---- Services & HW (row 81) ---- #
    services_hw = [salaries[i]*coeff_srv_hw[i] for i in idx]

    # ---- Web3 costs (row 97) ---- #
    web3_costs = [
        market_making[i] + exch_list[i] + web3_legal[i]
        for i in idx
    ]

    # ---- Formation cost (row 104) ---- #
    cost_small_courses = [cost_small_course_per * small_courses_count[i] for i in idx]
    cost_cert_paths    = [cost_cert_per         * cert_paths_count[i]    for i in idx]
    formation_cost = [
        cost_small_courses[i] + cost_cert_paths[i] for i in idx
    ]

    # ---- Tournament prices/fees (row 113) ---- #
    d_tourn_prices  = [price_per_d_tourn[i]*d_events[i]  for i in idx]
    xr_tourn_prices = [price_per_xr_tourn[i]*xr_events[i] for i in idx]
    prices_total = [d_tourn_prices[i] + xr_tourn_prices[i] for i in idx]

    # ---- Marketing costs (row 119) ---- #
    events_cost_scaled   = [e * marketing_scale for e in events_cost]
    sponsors_cost_scaled = [s * marketing_scale for s in sponsors_cost]
    travel_cost_scaled   = [t * marketing_scale for t in travel_cost]

    marketing_total = [
        events_cost_scaled[i] + sponsors_cost_scaled[i] +
        travel_cost_scaled[i] + publicity[i]
        for i in idx
    ]

    # ---- New Paying Users (row 126) + Acquisition cost (127) ---- #
    monthly_recurrency = 0.4
    new_paying_users = [0.0]*n
    # Row126 formulas use differences & recurrency; approximate cleanly:
    for i in idx:
        if i == 0:
            new_paying_users[i] = max(mau[i] * (1.0-monthly_recurrency), 0)
        else:
            delta = mau[i] - mau[i-1]*monthly_recurrency
            new_paying_users[i] = max(delta, 0)

    new_user_acq_cost = []
    for i in idx:
        # Excel distributes some cost buckets over new paying users.
        num = prices_total[i] + marketing_total[i] + hc_mkt[i]*sal_mkt
        denom = new_paying_users[i]
        if denom <= 0:
            new_user_acq_cost.append(0.0)
        else:
            new_user_acq_cost.append(num/denom)

    # ---- Total Costs (row 129) ---- #
    costs = []
    for i in idx:
        total_cost = (
            marketing_total[i] +
            new_user_acq_cost[i] +
            game_platform_dev[i] +
            services_hw[i] +
            salaries[i] +
            space_system_cost[i] +
            space_ops_cost[i] +
            prices_total[i] +
            formation_cost[i] +
            web3_costs[i]
        )
        costs.append(total_cost)

    # ---- Profit (row 131) + Overall cumulative (row 133) ---- #
    profit = [revenues[i] - costs[i] for i in idx]

    overall = []
    cumulative = 0.0
    for i in idx:
        cumulative += profit[i]
        overall.append(cumulative)

    # aggregate breakdown to feed charts
    result = {
        "years": [i+1 for i in idx],
        "mau": mau,
        "revenues": revenues,
        "costs": costs,
        "profit": profit,
        "overall": overall,
        "segments": {
            "game": game_total,
            "formation": formation_total,
            "xr": xr_total,
            "tokens": tokens_total,
            "marketplace": marketplace_total,
            "serious": serious_total
        },
        "cost_breakdown": {
            "salaries": salaries,
            "services_hw": services_hw,
            "web3": web3_costs,
            "game_platform": game_platform_dev,
            "formation_cost": formation_cost,
            "space_system": space_system_cost,
            "space_ops": space_ops_cost,
            "prices": prices_total,
            "marketing": marketing_total,
            "new_user_acq": new_user_acq_cost
        }
    }
    return result


# -------------- API ENDPOINTS ---------------- #

@app.route("/api/compute", methods=["POST"])
def api_compute():
    params = request.json or {}
    data = compute_model(params)
    return jsonify(data)


# -------------- FRONT-END (SPACE THEME) --------------- #

INDEX_HTML = """
<!doctype html>
<html lang="en" data-bs-theme="dark">
  <head>
    <meta charset="utf-8">
    <title>SpArks Financial Simulator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap 5 -->
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
      rel="stylesheet"
    >
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

    <!-- Plotly -->
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

    <style>
      body {
        background: radial-gradient(circle at top, #1a2b4c 0, #050816 40%, #000000 100%);
        color: #e2e8f0;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }
      .navbar-brand {
        font-family: "Orbitron", system-ui, sans-serif;
        letter-spacing: 0.12em;
      }
      .glass {
        background: rgba(15, 23, 42, 0.85);
        border-radius: 1rem;
        border: 1px solid rgba(148, 163, 184, 0.3);
        box-shadow: 0 0 40px rgba(56, 189, 248, 0.25);
      }
      .neon-text {
        color: #38bdf8;
        text-shadow: 0 0 12px rgba(56, 189, 248, 0.9);
      }
      .slider-label {
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #a5b4fc;
      }
      .form-range::-webkit-slider-thumb {
        background: #38bdf8;
      }
      .tab-pane {
        padding-top: 1rem;
      }
    </style>
  </head>
  <body class="pb-4">

    <nav class="navbar navbar-dark bg-dark bg-opacity-75 mb-3 border-bottom border-info border-opacity-50">
      <div class="container-fluid">
        <span class="navbar-brand mb-0 h1">
          🌌 SpArks Financial Simulator
        </span>
        <span class="text-secondary small">Playable Space Assets • Edutainment • Web3</span>
      </div>
    </nav>

    <div class="container">

      <div class="row mb-3">
        <div class="col-lg-4 mb-3">
          <div class="glass p-3 h-100">
            <h5 class="neon-text mb-3">Stress Test Controls</h5>

            <label class="slider-label">MAU Scale (<span id="mauScaleLabel">1.0x</span>)</label>
            <input type="range" class="form-range" min="0.5" max="1.5" step="0.05" id="mauScale" value="1.0">

            <label class="slider-label mt-3">Game Conversion Scale (<span id="convGameLabel">1.0x</span>)</label>
            <input type="range" class="form-range" min="0.5" max="1.5" step="0.05" id="convGameScale" value="1.0">

            <label class="slider-label mt-3">Courses Conversion Scale (<span id="convCourseLabel">1.0x</span>)</label>
            <input type="range" class="form-range" min="0.5" max="1.5" step="0.05" id="convCourseScale" value="1.0">

            <label class="slider-label mt-3">Marketing Intensity (<span id="marketingLabel">1.0x</span>)</label>
            <input type="range" class="form-range" min="0.3" max="1.5" step="0.05" id="marketingScale" value="1.0">

            <label class="slider-label mt-3">Content Cost Scale (<span id="contentCostLabel">1.0x</span>)</label>
            <input type="range" class="form-range" min="0.5" max="1.5" step="0.05" id="contentCostScale" value="1.0">

            <label class="slider-label mt-3">Event Yield Scale (<span id="eventYieldLabel">1.0x</span>)</label>
            <input type="range" class="form-range" min="0.5" max="2.0" step="0.1" id="eventYieldScale" value="1.0">

            <button class="btn btn-outline-info w-100 mt-3" onclick="runModel()">Recompute Model</button>
          </div>
        </div>

        <div class="col-lg-8 mb-3">
          <div class="glass p-3 h-100">
            <ul class="nav nav-tabs" id="mainTabs" role="tablist">
              <li class="nav-item" role="presentation">
                <button class="nav-link active" id="overview-tab" data-bs-toggle="tab"
                        data-bs-target="#overview" type="button" role="tab">
                  Overview
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="revenue-tab" data-bs-toggle="tab"
                        data-bs-target="#revenuesTab" type="button" role="tab">
                  Revenues
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="costs-tab" data-bs-toggle="tab"
                        data-bs-target="#costsTab" type="button" role="tab">
                  Costs
                </button>
              </li>
            </ul>

            <div class="tab-content">
              <div class="tab-pane fade show active" id="overview" role="tabpanel">
                <div id="overviewChart" style="height:360px;"></div>
              </div>
              <div class="tab-pane fade" id="revenuesTab" role="tabpanel">
                <div id="revenuesChart" style="height:360px;"></div>
              </div>
              <div class="tab-pane fade" id="costsTab" role="tabpanel">
                <div id="costsChart" style="height:360px;"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-12">
          <div class="glass p-3">
            <h5 class="neon-text mb-2">Cumulative Profit</h5>
            <div id="overallChart" style="height:320px;"></div>
          </div>
        </div>
      </div>

    </div>

    <script>
      function updateLabels() {
        document.getElementById("mauScaleLabel").innerText =
          document.getElementById("mauScale").value + "x";
        document.getElementById("convGameLabel").innerText =
          document.getElementById("convGameScale").value + "x";
        document.getElementById("convCourseLabel").innerText =
          document.getElementById("convCourseScale").value + "x";
        document.getElementById("marketingLabel").innerText =
          document.getElementById("marketingScale").value + "x";
        document.getElementById("contentCostLabel").innerText =
          document.getElementById("contentCostScale").value + "x";
        document.getElementById("eventYieldLabel").innerText =
          document.getElementById("eventYieldScale").value + "x";
      }

      ["mauScale","convGameScale","convCourseScale","marketingScale",
       "contentCostScale","eventYieldScale"].forEach(id => {
          document.getElementById(id).addEventListener("input", updateLabels);
      });

      async function runModel() {
        const body = {
          mau_scale: parseFloat(document.getElementById("mauScale").value),
          conv_game_scale: parseFloat(document.getElementById("convGameScale").value),
          conv_course_scale: parseFloat(document.getElementById("convCourseScale").value),
          marketing_scale: parseFloat(document.getElementById("marketingScale").value),
          content_cost_scale: parseFloat(document.getElementById("contentCostScale").value),
          event_yield_scale: parseFloat(document.getElementById("eventYieldScale").value)
        };

        const resp = await fetch("/api/compute", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify(body)
        });
        const data = await resp.json();
        renderCharts(data);
      }

      function renderCharts(data) {
        const years = data.years;

        // Overview: revenues, costs, profit
        Plotly.newPlot("overviewChart", [
          { x: years, y: data.revenues, name: "Revenues", type: "scatter" },
          { x: years, y: data.costs,    name: "Costs",    type: "scatter" },
          { x: years, y: data.profit,   name: "Profit",   type: "bar", opacity: 0.5 }
        ], {
          margin: {t: 20},
          paper_bgcolor: "rgba(0,0,0,0)",
          plot_bgcolor: "rgba(15,23,42,0.8)",
          legend: {orientation:"h", y:-0.2}
        });

        // Revenues breakdown
        const seg = data.segments;
        Plotly.newPlot("revenuesChart", [
          { x: years, y: seg.game,       name: "Game",       type: "scatter" },
          { x: years, y: seg.formation,  name: "Formation",  type: "scatter" },
          { x: years, y: seg.xr,         name: "XR Events",  type: "scatter" },
          { x: years, y: seg.marketplace,name: "Marketplace",type: "scatter" },
          { x: years, y: seg.tokens,     name: "Tokens",     type: "scatter" },
          { x: years, y: seg.serious,    name: "Serious",    type: "scatter" }
        ], {
          margin: {t: 20},
          paper_bgcolor: "rgba(0,0,0,0)",
          plot_bgcolor: "rgba(15,23,42,0.8)",
          legend: {orientation:"h", y:-0.2}
        });

        // Costs breakdown
        const c = data.cost_breakdown;
        Plotly.newPlot("costsChart", [
          { x: years, y: c.salaries,       name: "Salaries",       type: "scatter" },
          { x: years, y: c.services_hw,    name: "Services & HW",  type: "scatter" },
          { x: years, y: c.marketing,      name: "Marketing",      type: "scatter" },
          { x: years, y: c.game_platform,  name: "Game & Platform",type: "scatter" },
          { x: years, y: c.formation_cost, name: "Formation Cost", type: "scatter" },
          { x: years, y: c.space_system,   name: "Space System",   type: "scatter" },
          { x: years, y: c.space_ops,      name: "Space Ops",      type: "scatter" },
          { x: years, y: c.web3,           name: "Web3",           type: "scatter" },
          { x: years, y: c.prices,         name: "Tournament Prices", type: "scatter" },
          { x: years, y: c.new_user_acq,   name: "New User CAC",   type: "scatter" }
        ], {
          margin: {t: 20},
          paper_bgcolor: "rgba(0,0,0,0)",
          plot_bgcolor: "rgba(15,23,42,0.8)",
          legend: {orientation:"h", y:-0.3}
        });

        // Overall cumulative
        Plotly.newPlot("overallChart", [
          { x: years, y: data.overall, name: "Cumulative Profit", type: "scatter", fill: "tozeroy" }
        ], {
          margin: {t: 20},
          paper_bgcolor: "rgba(0,0,0,0)",
          plot_bgcolor: "rgba(15,23,42,0.8)"
        });
      }

      // initial load
      updateLabels();
      runModel();
    </script>
  </body>
</html>
"""

@app.route("/")
def index():
    return make_response(INDEX_HTML)


if __name__ == "__main__":
    app.run(debug=True)
