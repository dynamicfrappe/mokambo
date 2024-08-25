import frappe

from mokambo.apis.core.users.jwt_decorator import jwt_required


@frappe.whitelist(allow_guest=True)
@jwt_required
def get_stock_items(item_group=None):
	if item_group:
		items = frappe.get_all('Item', fields=[
			'name', 'item_code', 'item_name', 'item_group', 'image', 'stock_uom', 'standard_rate'
		], filters={'item_group': item_group})
	else:
		items = frappe.get_all('Item', fields=[
			'name', 'item_code', 'item_name', 'item_group', 'description', 'stock_uom', 'standard_rate'
		])
	frappe.local.response['data'] = items
