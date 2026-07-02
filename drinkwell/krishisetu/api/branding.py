# Copyright (c) 2024, 10x Impact
# Replaces default/drinkwell branding with KrishiSetu across desk, login and website.
import frappe

MARK = "/assets/drinkwell/images/mark.svg"


def _set(doctype, field, value):
    try:
        frappe.db.set_single_value(doctype, field, value)
    except Exception as e:
        print(f"branding: skipped {doctype}.{field} -> {e}")


def apply_branding():
    # Desk navbar — no logo, name only
    _set("Navbar Settings", "app_logo", "")

    # Website brand / login page / favicon
    _set("Website Settings", "app_name", "KrishiSetu")
    _set("Website Settings", "app_logo", "")
    _set("Website Settings", "banner_image", "")
    _set("Website Settings", "brand_html", "KrishiSetu")
    _set("Website Settings", "favicon", MARK)
    _set("Website Settings", "splash_image", MARK)
    _set("Website Settings", "home_page", "index")
    _set("Website Settings", "footer_powered", " ")

    # System-wide app name (drives "Login to <app>" and desk title)
    _set("System Settings", "app_name", "KrishiSetu")

    frappe.db.commit()
    print("KrishiSetu branding applied.")
