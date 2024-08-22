import frappe

from mokambo.apis.core.users.jwt_decorator import jwt_required


@frappe.whitelist()
@jwt_required
def get_stock_items():
	# Get the token from the request headers
	# return 'get_stock_items'
	user = frappe.local.user
	cashier = frappe.get_doc('User', user)

	items = frappe.get_all('Item', fields=[
		'item_code', 'item_name', 'description', 'stock_uom', 'standard_rate'
	])
	print(items)
	return items
