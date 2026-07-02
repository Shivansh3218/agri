# Copyright (c) 2024, 10x Impact and contributors
# Seed the KrishiSetu platform with survey data, crop & scheme masters.

import json
import os
import frappe

FSR = "Farmer Survey Response"


def _data_path(name):
    return os.path.join(os.path.dirname(__file__), "..", "data", name)


def ensure_role():
    if not frappe.db.exists("Role", "Agriculture Officer"):
        frappe.get_doc({"doctype": "Role", "role_name": "Agriculture Officer",
                        "desk_access": 1}).insert(ignore_permissions=True)


CROPS = [
    ("Wheat", "Rabi", "Cereal", "Primary rabi cereal across all surveyed regions."),
    ("Rice", "Kharif", "Cereal", "Staple kharif crop, water intensive."),
    ("Sugarcane", "Perennial", "Cash Crop", "Long-duration cash crop common in Amroha."),
    ("Mustard", "Rabi", "Oilseed", "Oilseed grown in rotation with wheat."),
    ("Bajra", "Kharif", "Cereal", "Drought-tolerant millet."),
    ("Pulses", "Rabi", "Pulse", "Nitrogen-fixing rotation crop."),
]

SCHEMES = [
    ("Pradhan Mantri Fasal Bima Yojana", "PMFBY", "Insurance",
     "Crop insurance scheme providing financial support to farmers suffering crop loss due to natural calamities, pests and diseases.",
     "All farmers growing notified crops in notified areas, including sharecroppers and tenant farmers.",
     "Apply through banks, CSCs, insurance agents or the National Crop Insurance Portal before the cut-off date.",
     "https://pmfby.gov.in", "Up to full sum-insured payout on verified crop loss."),
    ("PM Kisan Samman Nidhi", "PM-KISAN", "Subsidy",
     "Income support of Rs 6,000 per year paid in three equal instalments to eligible landholding farmer families.",
     "Small and marginal landholding farmer families with cultivable land.",
     "Register at pmkisan.gov.in or via local revenue / agriculture office with Aadhaar and land records.",
     "https://pmkisan.gov.in", "Rs 6,000 / year direct benefit transfer."),
    ("Kisan Credit Card", "KCC", "Credit",
     "Provides farmers timely access to short-term credit for cultivation and allied activities at subsidised interest.",
     "All farmers, tenant farmers, sharecroppers and self-help groups.",
     "Apply at any commercial bank, cooperative bank or RRB with land and identity documents.",
     "https://www.myscheme.gov.in", "Collateral-free credit up to Rs 1.6 lakh at 4% effective interest."),
    ("Pradhan Mantri Krishi Sinchayee Yojana", "PMKSY", "Irrigation",
     "Aims to expand cultivated area under assured irrigation and improve on-farm water use efficiency (per drop more crop).",
     "Farmers seeking micro-irrigation and water conservation support.",
     "Apply through the state agriculture / horticulture department.",
     "https://pmksy.gov.in", "Subsidy on drip / sprinkler irrigation systems."),
    ("National Agriculture Market", "e-NAM", "Market Support",
     "Online trading platform networking APMC mandis to enable better price discovery and transparent auctions.",
     "Registered farmers and traders in linked mandis.",
     "Register at enam.gov.in or via your nearest linked mandi.",
     "https://enam.gov.in", "Wider market access and transparent price discovery."),
    ("Soil Health Card Scheme", "SHC", "Other",
     "Provides farmers a card with crop-wise recommendations of nutrients and fertilizers to improve productivity.",
     "All farmers.",
     "Request through the local agriculture department or soil testing lab.",
     "https://soilhealth.dac.gov.in", "Tailored fertilizer recommendations, lower input waste."),
]


def seed_masters():
    for name, season, cat, desc in CROPS:
        if not frappe.db.exists("Crop", name):
            frappe.get_doc({"doctype": "Crop", "crop_name": name, "season": season,
                            "category": cat, "description": desc}).insert(ignore_permissions=True)
    for nm, code, cat, desc, elig, how, url, benefit in SCHEMES:
        if not frappe.db.exists("Government Scheme", nm):
            frappe.get_doc({"doctype": "Government Scheme", "scheme_name": nm, "short_code": code,
                            "category": cat, "is_active": 1, "benefit_summary": benefit,
                            "description": desc, "eligibility": elig, "how_to_apply": how,
                            "official_url": url}).insert(ignore_permissions=True)


def seed_responses():
    records = json.load(open(_data_path("farmer_data.json"), encoding="utf-8"))
    created = 0
    for rec in records:
        rid = rec.get("respondent_id")
        if not rid or frappe.db.exists(FSR, rid):
            continue
        doc = frappe.new_doc(FSR)
        for k, v in rec.items():
            if v is not None and k not in ("vulnerability_score", "vulnerability_band"):
                doc.set(k, v)
        doc.insert(ignore_permissions=True)
        created += 1
        if created % 100 == 0:
            frappe.db.commit()
    frappe.db.commit()
    return created


def seed_farmers():
    """Create/refresh Farmer master rows from survey responses."""
    created = 0
    for r in frappe.get_all(FSR, fields=["respondent_id", "farmer_name", "region", "village",
                                         "age", "gender", "primary_crop", "land_size",
                                         "vulnerability_band"], limit_page_length=0):
        if frappe.db.exists("Farmer", r.farmer_name):
            continue
        frappe.get_doc({"doctype": "Farmer", "farmer_name": r.farmer_name, "region": r.region,
                        "village": r.village, "age": r.age, "gender": r.gender,
                        "primary_crop": r.primary_crop, "land_size": r.land_size,
                        "latest_survey": r.respondent_id,
                        "vulnerability_band": r.vulnerability_band}).insert(ignore_permissions=True)
        created += 1
        if created % 100 == 0:
            frappe.db.commit()
    frappe.db.commit()
    return created


@frappe.whitelist()
def seed_data():
    """One-shot idempotent seeding. Run: bench --site <site> execute drinkwell.api.seed.seed_data"""
    ensure_role()
    seed_masters()
    n = seed_responses()
    f = seed_farmers()
    frappe.db.commit()
    msg = f"Seeded: {n} survey responses, {f} farmers, {len(CROPS)} crops, {len(SCHEMES)} schemes."
    print(msg)
    return msg
