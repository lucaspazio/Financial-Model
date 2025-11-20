// app.js — Updated to match REAL HTML IDs exactly
// Includes full debug logs

console.log("SpArks Financial Dashboard Loaded 🚀");

//--------------------------------------------------------------
// 1. Utility: Get slider values (IDs now match index.html)
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
// 2. Update readout text for sliders
//--------------------------------------------------------------
function bindSlider(id) {
    const s = document.getElementById(id);
    const r = document.getElementById(id + "_value");

    if (!s) {
        console.error("❌ Missing slider ID:", id);
        return;
    }
    if (r) r.innerText = s.value;

    s.addEventListener("input", () => {
        if (r) r.innerText = s.value;
    });
}

// IDs EXACTLY as in index.html
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
// 3. Run Model - POST to Flask
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

        const result = await response.json();
        console.log("📊 Model output received:", result);

        renderCharts(result);
        fillReasonability(result.reasonability);

    } catch (err) {
        console.error("❌ Error running model:", err);
        alert("Model error: " + err.message);
    }
}

//--------------------------------------------------------------
// 4. Render Plotly Charts
//--------------------------------------------------------------
function renderCharts(data) {
    const r = data.results; // shorthand

    Plotly.newPlot("chart_revcost", [
        { x: r.years, y: r.revenues, name: "Revenues", mode: "lines+markers" },
        { x: r.years, y: r.costs, name: "Costs", mode: "lines+markers" }
    ], {
        title: "Revenues vs Costs",
        paper_bgcolor: "#020617",
        plot_bgcolor: "#020617",
        font: { color: "white" }
    });

    Plotly.newPlot("chart_profit", [
        { x: r.years, y: r.profit, name: "Profit", mode: "lines+markers" }
    ], {
        title: "Profit",
        paper_bgcolor: "#020617",
        plot_bgcolor: "#020617",
        font: { color: "white" }
    });

    Plotly.newPlot("chart_mau", [
        { x: r.years, y: r.mau, name: "MAU", mode: "lines+markers" }
    ], {
        title: "MAU Growth",
        paper_bgcolor: "#020617",
        plot_bgcolor: "#020617",
        font: { color: "white" }
    });

    Plotly.newPlot("chart_cac", [
        { x: r.years, y: r.cac, name: "CAC", mode: "lines+markers" }
    ], {
        title: "CAC",
        paper_bgcolor: "#020617",
        plot_bgcolor: "#020617",
        font: { color: "white" }
    });

    Plotly.newPlot("chart_roas", [
        { x: r.years, y: r.roas, name: "ROAS", mode: "lines+markers" }
    ], {
        title: "ROAS",
        paper_bgcolor: "#020617",
        plot_bgcolor: "#020617",
        font: { color: "white" }
    });

    Plotly.newPlot("chart_staff", [
        { x: r.years, y: r.staff, name: "Staff Count", mode: "lines+markers" }
    ], {
        title: "Staff",
        paper_bgcolor: "#020617",
        plot_bgcolor: "#020617",
        font: { color: "white" }
    });
}


//--------------------------------------------------------------
// 5. Reasonability indicators (green/red)
//--------------------------------------------------------------
function fillReasonability(res) {
    console.log("🟢 Checking reasonability...", res);

    for (const [key, arr] of Object.entries(res)) {
        const container = document.getElementById("reason_" + key);
        if (!container) continue;
        container.innerHTML = "";
        arr.forEach(state => {
            const dot = document.createElement("span");
            dot.style.height = "14px";
            dot.style.width = "14px";
            dot.style.display = "inline-block";
            dot.style.borderRadius = "50%";
            dot.style.marginRight = "4px";
            dot.style.backgroundColor = state === "green" ? "#22c55e" : "#ef4444";
            container.appendChild(dot);
        });
    }
}

//--------------------------------------------------------------
// 6. Save Scenario
//--------------------------------------------------------------
async function saveScenario() {
    const name = document.getElementById("scenario_name").value;
    const payload = getInputs();

    console.log("💾 Saving scenario:", name, payload);

    const response = await fetch(`/save_scenario/${name}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    alert("Scenario saved: " + name);
}

//--------------------------------------------------------------
// 7. Load Scenario
//--------------------------------------------------------------
async function loadScenario() {
    const name = document.getElementById("scenario_list").value;
    console.log("📂 Loading scenario:", name);

    const response = await fetch(`/data/scenario/${name}`);
    const data = await response.json();

    console.log("Scenario loaded:", data);

    for (const [key, value] of Object.entries(data)) {
        const el = document.getElementById(key);
        if (el) el.value = value;
    }

    alert("Scenario loaded.");
}

//--------------------------------------------------------------
console.log("SpArks app.js fully initialized 🛸");