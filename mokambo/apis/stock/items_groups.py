import frappe

from mokambo.apis.core.users.jwt_decorator import jwt_required


@frappe.whitelist(allow_guest=True)
@jwt_required
def get_stock_items_groups():
	# Get the token from the request headers
    # return 'get_stock_items'
	user = frappe.local.user
	cashier = frappe.get_doc('User', user)

	items_groups = frappe.get_all('Item Group', fields=[
		'name', 'item_group_name',
	])
	frappe.local.response['data'] = items_groups
