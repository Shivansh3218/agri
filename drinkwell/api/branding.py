# Copyright (c) 2024, 10x Impact
# Replaces default/drinkwell branding with KrishiSetu across desk, login and website.
import frappe

MARK = "/assets/drinkwell/images/mark.svg"


def apply_branding():
    # Desk navbar — no logo, name only
    try:
        nb = frappe.get_single("Navbar Settings")
        nb.app_logo = ""
        nb.save(ignore_permissions=True)
    except Exception:
        pass
    # Website brand / login page / favicon
    try:
        ws = frappe.get_single("Website Settings")
        ws.app_name = "KrishiSetu"
        ws.brand_html = "KrishiSetu"
        ws.banner_image = ""
        ws.favicon = MARK
        ws.splash_image = MARK
        ws.home_page = "index"
        ws.save(ignore_permissions=True)
    except Exception:
        pass
    # System-wide app name (drives "Login to <app>")
    try:
        frappe.db.set_single_value("System Settings", "app_name", "KrishiSetu")
    except Exception:
        pass
    frappe.db.commit()
    print("KrishiSetu branding applied.")
