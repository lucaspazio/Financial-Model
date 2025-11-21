// app.js — nuova versione con Inputs/Results, bande verdi/rosse e slider leggibili

console.log("SpArks Financial Dashboard Loaded 🚀");

//--------------------------------------------------------------
// 1. Utility: recupero input dai cursori
//--------------------------------------------------------------
function getInputs() {
    const data = {
        mau_scale: parseFloat(document.getElementById("mau_scale").value),
        game_conv_scale: parseFloat(document.getElementById("conv_game_scale").value),
        course_conv_scale: parseFloat(document.getElementById("conv_course_scale").value),
        marketing_scale: parseFloat(document.getElementById("marketing_scale").value),
        event_yield_scale: parseFloat(document.getElementById("event_yield_scale").value),
        content_cost_scale: parseFloat(document.getElementById("content_cost_scale").value),
        staff_scale: parseFloat(document.getElementById("staff_scale").value),
        srv_hw_scale: parseFloat(document.getElementById("srv_hw_scale").value)
    };
    console.log("📥 Collected input sliders:", data);
    return data;
}

//--------------------------------------------------------------
// 2. Slider binding: mostra valore tipo "1.15×"
//--------------------------------------------------------------
function bindSlider(id) {
    const s = document.getElementById(id);
    const v = document.getElementById(id + "_value");

    if (!s) {
        console.error("❌ Missing slider:", id);
        return;
    }

    const update = () => {
        if (v) v.innerText = parseFloat(s.value).toFixed(2) + "×";
    };

    s.addEventListener("input", update);
    update();
}

// Bind all sliders
[
  "mau_scale",
  "conv_game_scale",
  "conv_course_scale",
  "marketing_scale",
  "event_yield_scale",
  "content_cost_scale",
  "staff_scale",
  "srv_hw_scale"
].forEach(bindSlider);

//--------------------------------------------------------------
// 3. Run Model - chiama Flask /run_model
//--------------------------------------------------------------
async function runModel() {
    console.log("▶ Running model...");
    const payload = getInputs();

    try {
        const response = await fetch("/run_model", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error("API error " + response.status);

        const data = await response.json();
        console.log("📊 Model output received:", data);

        // data.results = numeri; data.reasonability = colori
        renderResultsCharts(data.results);
        renderInputCharts(payload, data.results);
        // Se in futuro vuoi ancora i dots, puoi usare data.reasonability

    } catch (err) {
        console.error("❌ Error running model:", err);
        alert("Model error: " + err.message);
    }
}

//--------------------------------------------------------------
// 4. Grafici INPUTS: bande verdi/rosse + linea del valore
//--------------------------------------------------------------
function makeInputChart(divId, label, years, baseline, scale, options) {
    const factor = options?.factor ?? 1;
    const unit   = options?.unit   ?? "";

    const baselinePlot = baseline.map(v => v * factor);
    const scaledPlot   = baseline.map(v => v * scale * factor);

    const traces = [
        {
            x: years,
            y: baselinePlot,
            name: "Baseline (1.00×)",
            mode: "lines",
            line: { dash: "dot" }
        },
        {
            x: years,
            y: scaledPlot,
            name: `Scaled (${scale.toFixed(2)}×)`,
            mode: "lines+markers"
        }
    ];

    const shapes = [];

    // Se abbiamo un greenMin/greenMax (in unità "raw"), disegnamo banda verde costante
    if (options?.greenMin != null && options?.greenMax != null) {
        const y0 = options.greenMin * factor;
        const y1 = options.greenMax * factor;
        shapes.push({
            type: "rect",
            x0: years[0] - 0.5,
            x1: years[years.length - 1] + 0.5,
            y0: y0,
            y1: y1,
            fillcolor: "rgba(34,197,94,0.12)",
            line: { width: 0 }
        });
    }

    Plotly.newPlot(divId, traces, {
        title: `${label}${unit ? " (" + unit + ")" : ""}`,
        paper_bgcolor: "#020617",
        plot_bgcolor: "#020617",
        font: { color: "white" },
        shapes: shapes
    });
}


function makeMauInputChart(divId, years, baseline, scale) {
    const baselinePlot = baseline;
    const scaledPlot = baseline.map(v => v * scale);

    const traces = [
        {
            x: years,
            y: baselinePlot,
            name: "Baseline MAU (1.00×)",
            mode: "lines",
            line: { dash: "dot" }
        },
        {
            x: years,
            y: scaledPlot,
            name: `Scaled MAU (${scale.toFixed(2)}×)`,
            mode: "lines+markers"
        }
    ];

    // Bande verdi "industriali" per MAU (see Option B)
    const shapes = [
        // Early years 1–3: 50k–500k
        {
            type: "rect",
            x0: 0.5,
            x1: 3.5,
            y0: 50000,
            y1: 500000,
            fillcolor: "rgba(34,197,94,0.12)",
            line: { width: 0 }
        },
        // Years 4–6: 300k–2M
        {
            type: "rect",
            x0: 3.5,
            x1: 6.5,
            y0: 300000,
            y1: 2000000,
            fillcolor: "rgba(34,197,94,0.12)",
            line: { width: 0 }
        },
        // Years 7+: 1–3M
        {
            type: "rect",
            x0: 6.5,
            x1: years[years.length - 1] + 0.5,
            y0: 1000000,
            y1: 3000000,
            fillcolor: "rgba(34,197,94,0.12)",
            line: { width: 0 }
        }
    ];

    Plotly.newPlot(divId, traces, {
        title: "MAU (green = reasonable band by phase)",
        paper_bgcolor: "#020617",
        plot_bgcolor: "#020617",
        font: { color: "white" },
        shapes: shapes
    });
}


function renderInputCharts(inputs, results) {
    const years = results.years || Array.from({ length: 14 }, (_, i) => i + 1);

    // === Baseline arrays from Excel: sheet "Hyp Financials" ===
    const base_mau = [
        0, 60000, 300000, 600000, 1200000, 1600000, 2000000,
        2000000, 2000000, 2000000, 2000000, 2000000, 2000000, 2000000
    ];

    const base_conv_game = [
        0.01, 0.01, 0.01, 0.02, 0.02, 0.03, 0.03,
        0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03
    ];

    const base_conv_course = [
        0.001, 0.001, 0.0015, 0.002, 0.0025, 0.003, 0.0035,
        0.004, 0.0045, 0.005, 0.005, 0.005, 0.005, 0.005
    ];

    const base_marketing = [
        620000,
        1570000,
        5570000,
        15570000,
        25570000,
        35570000,
        35570000,
        35570000,
        35570000,
        35570000,
        35570000,
        35570000,
        35570000,
        35570000
    ];

    const base_event_yield = [
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
        2240000,
        2240000,
        2240000,
        2240000
    ];

    const base_content_cost = [
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
        7000000,
        7000000,
        7000000,
        7000000
    ];

    const base_staff = [
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
        70,
        70,
        70,
        70
    ];

    const base_srv_hw = [
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
        1.5
    ];

    // MAU: grafico dedicato con fasce per year-range
    makeMauInputChart("chart_in_mau", years, base_mau, inputs.mau_scale);

    // Game conversion: green band 1–5%
    makeInputChart(
        "chart_in_game",
        "Game Conversion",
        years,
        base_conv_game,
        inputs.game_conv_scale,
        {
            unit: "%",
            factor: 100,
            greenMin: 0.01,
            greenMax: 0.05
        }
    );

    // Course conversion: green band 0.05–0.4%
    makeInputChart(
        "chart_in_course",
        "Course Conversion (Small)",
        years,
        base_conv_course,
        inputs.course_conv_scale,       
        {
            unit: "%",
            factor: 100,
            greenMin: 0.0005,
            greenMax: 0.004
        }
    );

    // Marketing: solo baseline vs scaled (niente banda "hard" – dipende dal modello)
    makeInputChart(
        "chart_in_marketing",
        "Marketing Spend",
        years,
        base_marketing,
        inputs.marketing_scale,
        {
            unit: "€M",
            factor: 1e-6
        }
    );

    // Event Yield: baseline vs scaled, senza banda rigida
    makeInputChart(
        "chart_in_events",
        "Event Yield (XR + D)",
        years,
        base_event_yield,
        inputs.event_yield_scale,
        {
            unit: "€M",
            factor: 1e-6
        }
    );

    // Content cost: baseline vs scaled, niente banda esplicita (dipende da corsi/dev)
    makeInputChart(
        "chart_in_content",
        "Content & Formation Cost",
        years,
        base_content_cost,
        inputs.content_cost_scale,
        {
            unit: "€M",
            factor: 1e-6
        }
    );

    // Staff: baseline vs scaled; la reasonability vera sta nel ratio MAU/staff (in backend)
    makeInputChart(
        "chart_in_staff",
        "Staff Count",
        years,
        base_staff,
        inputs.staff_scale,
        {
            unit: "FTE",
            factor: 1
        }
    );

    // Services & HW coefficient: banda verde 1.5–2.5
    makeInputChart(
        "chart_in_srv",
        "Services & HW Coefficient",
        years,
        base_srv_hw,
        inputs.srv_hw_scale,
        {
            unit: "coef",
            factor: 1,
            greenMin: 1.5,
            greenMax: 2.5
        }
    );
}



//--------------------------------------------------------------
// 5. Grafici RESULTS: P&L, Space, Revenues, Costs, MAU, CAC/ROAS, Staff
//--------------------------------------------------------------
function renderResultsCharts(r) {
    console.log("📈 Rendering results charts...");

    // 5.1 Revenues vs Costs
    Plotly.newPlot("chart_revcost", [
        { x: r.years, y: r.revenues, name: "Revenues", mode: "lines+markers" },
        { x: r.years, y: r.costs,    name: "Costs",    mode: "lines+markers" }
    ], {
        title: "Revenues vs Costs",
        paper_bgcolor: "#020617",
        plot_bgcolor: "#020617",
        font: { color: "white" }
    });

    // 5.2 Profit
    Plotly.newPlot("chart_profit", [
        { x: r.years, y: r.profit, name: "Profit", mode: "lines+markers" }
    ], {
        title: "Profit",
        paper_bgcolor: "#020617",
        plot_bgcolor: "#020617",
        font: { color: "white" }
    });

    // 5.3 Space System: Profit vs soglia 5M
    const threshold = 5000000;
    Plotly.newPlot("chart_space_profit", [
        { x: r.years, y: r.profit, name: "Profit", mode: "lines+markers" }
    ], {
        title: "Profit vs 5M€ (Space System Sustainability)",
        paper_bgcolor: "#020617",
        plot_bgcolor: "#020617",
        font: { color: "white" },
        shapes: [
            {
                type: "line",
                x0: r.years[0],
                x1: r.years[r.years.length - 1],
                y0: threshold,
                y1: threshold,
                line: { color: "green", width: 3, dash: "dot" }
            },
            {
                type: "rect",
                x0: r.years[0],
                x1: r.years[r.years.length - 1],
                y0: 0,
                y1: threshold,
                fillcolor: "rgba(239,68,68,0.10)",
                line: { width: 0 }
            },
            {
                type: "rect",
                x0: r.years[0],
                x1: r.years[r.years.length - 1],
                y0: threshold,
                y1: Math.max(...r.profit) * 1.1,
                fillcolor: "rgba(34,197,94,0.08)",
                line: { width: 0 }
            }
        ]
    });

    // 5.4 Revenue Breakdown (placeholder: 60/25/15)
    const revGames   = r.revenues.map(v => v * 0.6);
    const revCourses = r.revenues.map(v => v * 0.25);
    const revEvents  = r.revenues.map(v => v * 0.15);

    Plotly.newPlot("chart_segments", [
        { x: r.years, y: revGames,   name: "Games",   type: "bar" },
        { x: r.years, y: revCourses, name: "Courses", type: "bar" },
        { x: r.years, y: revEvents,  name: "Events",  type: "bar" }
    ], {
        barmode: "stack",
        title: "Revenues by Segment (approx.)",
        paper_bgcolor: "#020617",
        plot_bgcolor: "#020617",
        font: { color: "white" }
    });

    // 5.5 Cost Breakdown (placeholder: 40/30/20/10)
    const cStaff   = r.costs.map(v => v * 0.4);
    const cMkt     = r.costs.map(v => v * 0.3);
    const cDev     = r.costs.map(v => v * 0.2);
    const cOther   = r.costs.map(v => v * 0.1);

    Plotly.newPlot("chart_costs_seg", [
        { x: r.years, y: cStaff, name: "Staff",   type: "bar" },
        { x: r.years, y: cMkt,   name: "Marketing", type: "bar" },
        { x: r.years, y: cDev,   name: "Dev & Platform", type: "bar" },
        { x: r.years, y: cOther, name: "Other",  type: "bar" }
    ], {
        barmode: "stack",
        title: "Costs by Segment (approx.)",
        paper_bgcolor: "#020617",
        plot_bgcolor: "#020617",
        font: { color: "white" }
    });

    // 5.6 MAU
    Plotly.newPlot("chart_mau", [
        { x: r.years, y: r.mau, name: "MAU", mode: "lines+markers" }
    ], {
        title: "MAU",
        paper_bgcolor: "#020617",
        plot_bgcolor: "#020617",
        font: { color: "white" }
    });

    // 5.7 CAC
    // 5.7 CAC (per paying customer)
Plotly.newPlot("chart_cac", [
    { x: r.years, y: r.cac, name: "CAC (paying)", mode: "lines+markers" }
], {
    title: "CAC (green = €5–25, yellow = €25–50)",
    paper_bgcolor: "#020617",
    plot_bgcolor: "#020617",
    font: { color: "white" },
    shapes: [
        // green band
        {
            type: "rect",
            x0: r.years[0] - 0.5,
            x1: r.years[r.years.length - 1] + 0.5,
            y0: 5,
            y1: 25,
            fillcolor: "rgba(34,197,94,0.12)",
            line: { width: 0 }
        },
        // yellow band
        {
            type: "rect",
            x0: r.years[0] - 0.5,
            x1: r.years[r.years.length - 1] + 0.5,
            y0: 25,
            y1: 50,
            fillcolor: "rgba(234,179,8,0.10)",
            line: { width: 0 }
        }
    ]
});


    // 5.8 ROAS
    // 5.8 ROAS
Plotly.newPlot("chart_roas", [
    { x: r.years, y: r.roas, name: "ROAS", mode: "lines+markers" }
], {
    title: "ROAS (green ≥ 1.5 , yellow 1.0–1.5)",
    paper_bgcolor: "#020617",
    plot_bgcolor: "#020617",
    font: { color: "white" },
    shapes: [
        // yellow band 1.0–1.5
        {
            type: "rect",
            x0: r.years[0] - 0.5,
            x1: r.years[r.years.length - 1] + 0.5,
            y0: 1.0,
            y1: 1.5,
            fillcolor: "rgba(234,179,8,0.10)",
            line: { width: 0 }
        },
        // green band ≥ 1.5 up to 5
        {
            type: "rect",
            x0: r.years[0] - 0.5,
            x1: r.years[r.years.length - 1] + 0.5,
            y0: 1.5,
            y1: 5,
            fillcolor: "rgba(34,197,94,0.12)",
            line: { width: 0 }
        }
    ]
});


    // 5.9 Staff & Salaries
    Plotly.newPlot("chart_staff", [
        { x: r.years, y: r.staff, name: "Staff", mode: "lines+markers" }
    ], {
        title: "Staff",
        paper_bgcolor: "#020617",
        plot_bgcolor: "#020617",
        font: { color: "white" }
    });

    Plotly.newPlot("chart_salaries", [
        { x: r.years, y: r.staff.map(v => v * 60000), name: "Salaries (approx.)", mode: "lines+markers" }
    ], {
        title: "Salaries (approx.)",
        paper_bgcolor: "#020617",
        plot_bgcolor: "#020617",
        font: { color: "white" }
    });

    console.log("✨ Results charts rendered.");
}

//--------------------------------------------------------------
// 6. Save / Load Scenarios (semplice wrapper)
//--------------------------------------------------------------
async function saveScenario() {
    const name = document.getElementById("scenario_name").value || "default";
    const payload = getInputs();
    console.log("💾 Saving scenario:", name, payload);

    const response = await fetch(`/save_scenario/${name}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    if (!response.ok) {
        alert("Error saving scenario");
        return;
    }
    alert("Scenario saved: " + name);
}

async function loadScenario() {
    const name = document.getElementById("scenario_list").value
               || document.getElementById("scenario_name").value
               || "default";

    console.log("📂 Loading scenario:", name);

    const response = await fetch(`/data/scenario/${name}`);
    if (!response.ok) {
        alert("Error loading scenario");
        return;
    }

    const data = await response.json();
    console.log("Scenario loaded:", data);

    // ripristina sliders
    for (const [key, value] of Object.entries(data)) {
        const el = document.getElementById(key);
        if (el) {
            el.value = value;
            const label = document.getElementById(key + "_value");
            if (label) label.innerText = parseFloat(value).toFixed(2) + "×";
        }
    }

    alert("Scenario loaded: " + name);
}

//--------------------------------------------------------------
console.log("SpArks app.js fully initialized 🛸");
