import frappe

def get_context(context):
    context.no_cache = 1
    try:
        context.schemes = frappe.get_all("Government Scheme",
            filters={"is_active": 1},
            fields=["scheme_name","short_code","category","benefit_summary","description","eligibility","how_to_apply","official_url"],
            order_by="category asc")
    except Exception:
        context.schemes = []
    return context
