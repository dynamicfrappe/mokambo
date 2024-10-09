app_name = "mokambo"
app_title = "Mokambo"
app_publisher = "Ameer Abdulaziz"
app_description = "This is a Mokambo app."
app_email = "ameer.abdulaziz93@gmail.com"
app_license = "mit"

fixtures = ["Custom Field"]
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/mokambo/css/mokambo.css"
# app_include_js = "/assets/mokambo/js/mokambo.js"

# include js, css files in header of web template
# web_include_css = "/assets/mokambo/css/mokambo.css"
# web_include_js = "/assets/mokambo/js/mokambo.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "mokambo/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "mokambo/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "mokambo.utils.jinja_methods",
# 	"filters": "mokambo.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "mokambo.install.before_install"
# after_install = "mokambo.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "mokambo.uninstall.before_uninstall"
# after_uninstall = "mokambo.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "mokambo.utils.before_app_install"
# after_app_install = "mokambo.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "mokambo.utils.before_app_uninstall"
# after_app_uninstall = "mokambo.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mokambo.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Sales Order": "mokambo.overrides.sales_order.CustomSalesOrder",
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	"cron": {
		"* * * * *": [
			"mokambo.overrides.sales_order.update_days_of_delivery"
		]
	}
# 	"all": [
# 		"mokambo.tasks.all"
# 	],
# 	"daily": [
# 		"mokambo.tasks.daily"
# 	],
# 	"hourly": [
# 		"mokambo.tasks.hourly"
# 	],
# 	"weekly": [
# 		"mokambo.tasks.weekly"
# 	],
# 	"monthly": [
# 		"mokambo.tasks.monthly"
# 	],
}

# Testing
# -------

# before_tests = "mokambo.install.before_tests"

# Overriding Methods
# ------------------------------
override_whitelisted_methods = {
	"login-user": "mokambo.apis.auth.login_user",
	"products": "mokambo.apis.routes.item_api",
	"categories": "mokambo.apis.routes.item_group_api",
	"sales-invoices": "mokambo.apis.routes.sales_invoice_api",
	"pos-profiles": "mokambo.apis.routes.pos_profiles_api",
	"customers": "mokambo.apis.routes.customers_api",
	"payment-methods": "mokambo.apis.routes.payment_methods_api",
	'pos-invoices': "mokambo.apis.routes.pos_invoices_api",
}

# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "mokambo.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["mokambo.utils.before_request"]
# after_request = ["mokambo.utils.after_request"]

# Job Events
# ----------
# before_job = ["mokambo.utils.before_job"]
# after_job = ["mokambo.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"mokambo.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# app_include_urls = "mokambo.apis.stock.items.get_stock_items"
#
# routes = [
#     {
# 		"from_route": "/api/method/mokambo/apis/stock/items/get_stock_items",
# 	 	"to_route": "mokambo.apis.stock.items.get_stock_items"
# 	}
# ]
