from typing import Dict, Any, List


def evaluate_reasonability(results: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Assegna colori green / yellow / red per:
      - MAU (curve di adozione tipo gaming/edtech)
      - CAC (per paying customer, se disponibile)
      - ROAS
      - Revenues (stabilità / crescita)
      - Staff (MAU per FTE)
    """

    years: List[int] = results.get("years", [])
    n = len(years)

    mau: List[float] = results.get("mau", [0.0] * n)
    revenues: List[float] = results.get("revenues", [0.0] * n)
    roas: List[float] = results.get("roas", [0.0] * n)

    # Preferisce CAC per paying customers se disponibile
    cac_paying: List[float] = results.get(
        "cac_paying",
        results.get("cac", [0.0] * n),
    )

    staff: List[float] = results.get("staff", [0.0] * n)

    colors_mau: List[str] = []
    colors_cac: List[str] = []
    colors_roas: List[str] = []
    colors_revenues: List[str] = []
    colors_staff: List[str] = []

    for i in range(n):
        y = years[i] if i < len(years) else i + 1
        m = float(mau[i]) if i < len(mau) else 0.0
        r = float(roas[i]) if i < len(roas) else 0.0
        rev = float(revenues[i]) if i < len(revenues) else 0.0
        cac_val = float(cac_paying[i]) if i < len(cac_paying) else 0.0
        st = float(staff[i]) if i < len(staff) else 0.0

        # --- MAU (industry-like adoption curves) ---
        if y <= 3:
            # Early: 50k–500k green
            if 50_000 <= m <= 500_000:
                cm = "green"
            elif 10_000 <= m < 50_000 or 500_000 < m <= 1_000_000:
                cm = "yellow"
            else:
                cm = "red"
        elif 4 <= y <= 6:
            # Mid: 300k–2M green
            if 300_000 <= m <= 2_000_000:
                cm = "green"
            elif 200_000 <= m < 300_000 or 2_000_000 < m <= 4_000_000:
                cm = "yellow"
            else:
                cm = "red"
        else:
            # Mature: 1–3M green
            if 1_000_000 <= m <= 3_000_000:
                cm = "green"
            elif 600_000 <= m < 1_000_000 or 3_000_000 < m <= 5_000_000:
                cm = "yellow"
            else:
                cm = "red"
        colors_mau.append(cm)

        # --- CAC per paying customer (€/user) ---
        # Green: 5–25 ; Yellow: 25–50 ; Red: otherwise
        if cac_val <= 0:
            cc = "red"
        elif 5 <= cac_val <= 25:
            cc = "green"
        elif 25 < cac_val <= 50:
            cc = "yellow"
        else:
            cc = "red"
        colors_cac.append(cc)

        # --- ROAS ---
        # Green: ≥1.5 ; Yellow: 1.0–1.5 ; Red: <1.0
        if r >= 1.5:
            cr = "green"
        elif 1.0 <= r < 1.5:
            cr = "yellow"
        else:
            cr = "red"
        colors_roas.append(cr)

        # --- Revenues ---
        # Red se <=0, Yellow se calano >20% anno su anno, Green altrimenti
        if rev <= 0:
            crv = "red"
        else:
            if i > 0:
                prev_rev = float(revenues[i - 1])
                if prev_rev > 0 and rev < prev_rev * 0.8:
                    crv = "yellow"
                else:
                    crv = "green"
            else:
                crv = "green"
        colors_revenues.append(crv)

        # --- Staff: MAU per FTE ---
        # Green: 20k–50k users per FTE ; Yellow: 10k–20k o 50k–80k ; Red: resto
        if st <= 0:
            cs = "red"
        else:
            ratio = m / st
            if 20_000 <= ratio <= 50_000:
                cs = "green"
            elif 10_000 <= ratio < 20_000 or 50_000 < ratio <= 80_000:
                cs = "yellow"
            else:
                cs = "red"
        colors_staff.append(cs)

    return {
        "mau": colors_mau,
        "cac": colors_cac,
        "roas": colors_roas,
        "revenues": colors_revenues,
        "staff": colors_staff,
    }
