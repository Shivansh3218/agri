# Copyright (c) 2024, 10x Impact
# Replaces default/drinkwell branding with KrishiSetu across desk, login and website.
import frappe

LOGO = "/assets/drinkwell/images/logo.svg"
MARK = "/assets/drinkwell/images/mark.svg"


def apply_branding():
    # Desk navbar logo
    try:
        nb = frappe.get_single("Navbar Settings")
        nb.app_logo = LOGO
        nb.save(ignore_permissions=True)
    except Exception:
        pass
    # Website brand / login page / favicon
    try:
        ws = frappe.get_single("Website Settings")
        ws.app_name = "KrishiSetu"
        ws.brand_html = '<img src="%s" style="height:26px">' % LOGO
        ws.banner_image = LOGO
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
