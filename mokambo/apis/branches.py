import frappe

from mokambo.apis.jwt_decorator import jwt_required


@frappe.whitelist(allow_guest=True)
@jwt_required
def get_branches():
	branches = frappe.get_all('Branch', fields=['name', 'branch'])
	frappe.local.response['data'] = branches
