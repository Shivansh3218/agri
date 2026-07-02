# Copyright (c) 2024, 10x Impact and contributors
import frappe
from frappe.model.document import Document


def compute_vulnerability(doc):
    score = 0
    score += 14 if doc.income_sufficient == "No" else 0
    score += 12 if doc.input_costs_burden == "Yes" else 0
    score += 12 if doc.govt_support_satisfaction == "Not satisfied" else (6 if doc.govt_support_satisfaction == "Moderately satisfied" else 0)
    score += 10 if doc.groundwater_depletion == "Yes" else 0
    score += 10 if doc.crop_loss_climate == "Yes" else 0
    score += 10 if doc.sells_at_msp == "No" else 0
    score += 8 if doc.relies_on_middlemen == "Yes" else 0
    score += 8 if doc.borrows_money == "Yes" else 0
    score += 8 if doc.loan_default == "Yes" else 0
    score += 8 if doc.satisfied_with_yield == "No" else 0
    score = min(score, 100)
    band = "Severe" if score >= 70 else "High" if score >= 50 else "Moderate" if score >= 30 else "Low"
    return score, band


class FarmerSurveyResponse(Document):
    def validate(self):
        self.vulnerability_score, self.vulnerability_band = compute_vulnerability(self)
        if not self.farmer_name and self.respondent_id:
            self.farmer_name = f"Farmer {self.respondent_id}"
