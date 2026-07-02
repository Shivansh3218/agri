app_name = "drinkwell"
app_title = "KrishiSetu"
app_publisher = "10x Impact"
app_description = "KrishiSetu — Farmer Insights & Survey Platform"
app_email = "shivansh@10ximpact.in"
app_license = "MIT"
app_version = "1.0.0"

# Theme + interactions loaded on every website page (login included)
web_include_css = "/assets/drinkwell/css/krishisetu.css?v=5"
web_include_js = "/assets/drinkwell/js/ks.js?v=5"

website_context = {
    "favicon": "/assets/drinkwell/images/mark.svg",
    "splash_image": "/assets/drinkwell/images/mark.svg",
}

home_page = "index"

# Re-apply KrishiSetu branding (desk logo, login, favicon) after every migrate
after_migrate = ["drinkwell.api.branding.apply_branding"]
