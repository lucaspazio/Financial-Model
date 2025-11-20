from flask import Flask, render_template, request, jsonify
import json
from financial_engine import compute_financials
from reasonability import evaluate_reasonability
import os

app = Flask(__name__)

# -----------------------------
# ROUTES
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")

# -----------------------------
# RUN MODEL
# -----------------------------
@app.route("/run_model", methods=["POST"])
def run_model():
    data = request.json

    results = compute_financials(data)
    reason = evaluate_reasonability(results)

    return jsonify({
        "results": results,
        "reasonability": reason
    })

# -----------------------------
# SAVE SCENARIO
# -----------------------------
@app.route("/save_scenario", methods=["POST"])
def save_scenario():
    scenario = request.json
    name = scenario.get("name", "scenario")

    os.makedirs("data/scenarios", exist_ok=True)
    path = f"data/scenarios/{name}.json"

    with open(path, "w") as f:
        json.dump(scenario, f, indent=4)

    return jsonify({"status": "ok", "path": path})

# -----------------------------
# LOAD SCENARIO
# -----------------------------
@app.route("/load_scenario", methods=["POST"])
def load_scenario():
    name = request.json.get("name")
    path = f"data/scenarios/{name}.json"

    if not os.path.exists(path):
        return jsonify({"error": "Scenario not found"}), 404

    with open(path, "r") as f:
        scenario = json.load(f)

    return jsonify(scenario)

# -----------------------------
# LIST SCENARIOS
# -----------------------------
@app.route("/list_scenarios", methods=["GET"])
def list_scenarios():
    os.makedirs("data/scenarios", exist_ok=True)
    files = os.listdir("data/scenarios")
    names = [f.replace(".json", "") for f in files if f.endswith(".json")]
    return jsonify(names)

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
