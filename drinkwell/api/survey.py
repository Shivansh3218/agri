# Copyright (c) 2024, 10x Impact and contributors
# Public + internal API for the KrishiSetu farmer platform.

import frappe
from frappe import _
from collections import Counter

DOCTYPE = "Farmer Survey Response"

SURVEY_FIELDS = [
    "farmer_name", "region", "block", "village", "age", "gender",
    "education_level", "total_family_members", "land_size", "primary_crop",
    "source_of_irrigation", "avg_input_cost_per_acre", "source_of_seeds",
    "market_access_point", "primary_source_of_money", "fertilizer_usage",
    "adaptation_to_climate", "msp_awareness_level", "crop_loss_frequency",
    "major_challenges", "perceived_price_fairness", "govt_support_satisfaction",
    "satisfied_with_yield", "income_sufficient", "seed_fertilizer_challenges",
    "input_costs_burden", "access_to_subsidies", "heard_of_pmfby", "availed_pmfby",
    "sells_at_msp", "relies_on_middlemen", "crop_loss_climate", "groundwater_depletion",
    "borrows_money", "loan_default", "practices_organic", "wishes_to_shift_away",
    "biggest_challenge", "coping_with_losses", "govt_support_suggestions",
    "climate_change_observation", "preferred_future_farming",
]


@frappe.whitelist(allow_guest=True)
def submit_survey(**kwargs):
    """Create a Farmer Survey Response from the public form."""
    data = frappe.parse_json(kwargs.get("payload")) if kwargs.get("payload") else kwargs

    count = frappe.db.count(DOCTYPE)
    rid = f"WEB-{count + 1:05d}"

    doc = frappe.new_doc(DOCTYPE)
    doc.respondent_id = rid
    for f in SURVEY_FIELDS:
        val = data.get(f)
        if val not in (None, ""):
            doc.set(f, val)
    if not doc.farmer_name:
        doc.farmer_name = f"Farmer {rid}"

    doc.flags.ignore_permissions = True
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "ok": True,
        "respondent_id": doc.respondent_id,
        "vulnerability_score": doc.vulnerability_score,
        "vulnerability_band": doc.vulnerability_band,
    }


def _all(fields):
    return frappe.get_all(DOCTYPE, fields=fields, limit_page_length=0)


@frappe.whitelist(allow_guest=True)
def dashboard_stats():
    rows = _all([
        "region", "vulnerability_band", "vulnerability_score", "education_level",
        "primary_crop", "market_access_point", "govt_support_satisfaction",
        "income_sufficient", "sells_at_msp", "relies_on_middlemen", "groundwater_depletion",
        "borrows_money", "practices_organic", "heard_of_pmfby", "availed_pmfby",
        "input_costs_burden", "satisfied_with_yield", "wishes_to_shift_away",
        "fertilizer_usage", "gender",
    ])
    total = len(rows) or 1

    def dist(key, top=None):
        c = Counter((r.get(key) or "Unknown") for r in rows)
        items = c.most_common(top) if top else sorted(c.items(), key=lambda x: -x[1])
        return [{"label": k, "value": v} for k, v in items]

    def yes_pct(key):
        y = sum(1 for r in rows if r.get(key) == "Yes")
        return round(100.0 * y / total, 1)

    avg_score = round(sum((r.get("vulnerability_score") or 0) for r in rows) / total, 1)

    band_order = ["Low", "Moderate", "High", "Severe"]
    regions = sorted({(r.get("region") or "Unknown") for r in rows})
    matrix = {reg: {b: 0 for b in band_order} for reg in regions}
    for r in rows:
        reg = r.get("region") or "Unknown"
        b = r.get("vulnerability_band") or "Low"
        matrix.setdefault(reg, {b2: 0 for b2 in band_order})
        matrix[reg][b] = matrix[reg].get(b, 0) + 1

    return {
        "total": len(rows),
        "avg_vulnerability": avg_score,
        "regions": dist("region"),
        "bands": [{"label": b, "value": sum(1 for r in rows if r.get("vulnerability_band") == b)} for b in band_order],
        "education": dist("education_level"),
        "crops": dist("primary_crop", 6),
        "market_access": dist("market_access_point"),
        "govt_satisfaction": dist("govt_support_satisfaction"),
        "fertilizer": dist("fertilizer_usage"),
        "indicators": [
            {"label": "Income not sufficient", "value": round(100 - yes_pct("income_sufficient"), 1)},
            {"label": "Input costs a burden", "value": yes_pct("input_costs_burden")},
            {"label": "Do NOT sell at MSP", "value": round(100 - yes_pct("sells_at_msp"), 1)},
            {"label": "Rely on middlemen", "value": yes_pct("relies_on_middlemen")},
            {"label": "Groundwater depletion", "value": yes_pct("groundwater_depletion")},
            {"label": "Borrow money", "value": yes_pct("borrows_money")},
            {"label": "Wish to quit farming", "value": yes_pct("wishes_to_shift_away")},
            {"label": "Heard of PMFBY", "value": yes_pct("heard_of_pmfby")},
            {"label": "Availed PMFBY", "value": yes_pct("availed_pmfby")},
            {"label": "Practice organic", "value": yes_pct("practices_organic")},
        ],
        "region_band_matrix": {"band_order": band_order, "regions": regions, "matrix": matrix},
    }


@frappe.whitelist(allow_guest=True)
def list_farmers(region=None, band=None, search=None, start=0, page_length=24):
    filters = {}
    if region:
        filters["region"] = region
    if band:
        filters["vulnerability_band"] = band
    or_filters = None
    if search:
        or_filters = [
            [DOCTYPE, "farmer_name", "like", f"%{search}%"],
            [DOCTYPE, "village", "like", f"%{search}%"],
            [DOCTYPE, "respondent_id", "like", f"%{search}%"],
        ]
    rows = frappe.get_all(
        DOCTYPE, filters=filters, or_filters=or_filters,
        fields=["respondent_id", "farmer_name", "region", "block", "village", "age",
                "gender", "primary_crop", "land_size", "vulnerability_score", "vulnerability_band"],
        start=int(start), page_length=int(page_length), order_by="vulnerability_score desc",
    )
    total = frappe.db.count(DOCTYPE, filters=filters)
    return {"rows": rows, "total": total}


@frappe.whitelist(allow_guest=True)
def farmer_report(respondent_id):
    if not frappe.db.exists(DOCTYPE, respondent_id):
        frappe.throw(_("Farmer record not found"), frappe.DoesNotExistError)
    doc = frappe.get_doc(DOCTYPE, respondent_id)
    d = doc.as_dict()
    avg = frappe.db.sql("select avg(vulnerability_score) from `tabFarmer Survey Response`")[0][0] or 0
    d["peer_avg_score"] = round(avg, 1)
    return d
