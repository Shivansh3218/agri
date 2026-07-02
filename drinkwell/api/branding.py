# Copyright (c) 2024, 10x Impact
# Replaces default/drinkwell branding with KrishiSetu across desk, login and website.
import frappe

MARK = "/assets/drinkwell/images/mark.svg"


def apply_branding():
    # Desk navbar — clear logo so only the app name text shows
    frappe.db.set_single_value("Navbar Settings", "app_logo", None)

    # Website brand / login page / favicon
    frappe.db.set_single_value("Website Settings", "app_name", "KrishiSetu")
    frappe.db.set_single_value("Website Settings", "brand_html", "KrishiSetu")
    frappe.db.set_single_value("Website Settings", "banner_image", None)
    frappe.db.set_single_value("Website Settings", "favicon", MARK)
    frappe.db.set_single_value("Website Settings", "splash_image", MARK)
    frappe.db.set_single_value("Website Settings", "home_page", "index")
    # System-wide app name (drives "Login to <app>")
    try:
        frappe.db.set_single_value("System Settings", "app_name", "KrishiSetu")
    except Exception:
        pass
    frappe.db.commit()
    print("KrishiSetu branding applied.")
