# Copyright (c) 2024, 10x Impact
# Replaces default/drinkwell branding with KrishiSetu across desk, login and website.
import frappe

MARK = "/assets/drinkwell/images/mark.svg"


def apply_branding():
    # Desk navbar — clear logo via both ORM and direct SQL to ensure it's gone
    frappe.db.set_single_value("Navbar Settings", "app_logo", None)
    frappe.db.sql(
        "UPDATE `tabSingles` SET `value`=NULL WHERE `doctype`='Navbar Settings' AND `field`='app_logo'"
    )
    frappe.db.set_default("_default_app_logo_url", "")

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
