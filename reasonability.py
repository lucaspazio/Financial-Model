# reasonability.py — FIXED (no more meta dependency)

def evaluate_reasonability(results):
    """
    Takes the output from financial_engine.compute_financials()
    and checks ranges/thresholds. No longer requires 'meta'.
    """

    reasonability = {
        "mau": [],
        "revenues": [],
        "staff": [],
        "cac": [],
        "roas": []
    }

    mau = results["mau"]
    rev = results["revenues"]
    staff = results["staff"]
    cac = results["cac"]
    roas = results["roas"]

    for i in range(len(mau)):
        reasonability["mau"].append("green" if mau[i] >= 0 else "red")
        reasonability["revenues"].append("green" if rev[i] >= 0 else "red")
        reasonability["staff"].append("green" if staff[i] >= 0 else "red")
        reasonability["cac"].append("green" if cac[i] < 200 else "red")
        reasonability["roas"].append("green" if roas[i] > 0.5 else "red")

    return reasonability
