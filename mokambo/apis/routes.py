import frappe
from frappe import _

from mokambo.apis.customer import CustomerAPI
from mokambo.apis.jwt_decorator import jwt_required
from mokambo.apis.item import ItemAPI
from mokambo.apis.item_group import ItemGroupAPI
from mokambo.apis.pos_profiles import POSProfileAPI
from mokambo.apis.sales_invoice import SalesInvoiceAPI


def _routes_api(cls, **kwargs):
	method = frappe.request.method
	record_id = kwargs.get('id')
	if method == 'GET':
		try:
			if id:
				return cls.get(record_id, **kwargs)  # Get a single sales invoice
			else:
				return cls.get(**kwargs)  # Get all sales invoices
		except AttributeError as e:
			frappe.local.response['http_status_code'] = 405  # HTTP 405 Method Not Allowed
			frappe.local.response['message'] = (_("Method not allowed."))
	elif method == 'POST':
		try:
			return cls.post(**kwargs)  # Create a new sales invoice
		except AttributeError as e:
			frappe.local.response['http_status_code'] = 405  # HTTP 405 Method Not Allowed
			frappe.local.response['message'] = (_("Method not allowed."))
	elif method == 'PUT':
		try:
			return cls.put(record_id, **kwargs)  # Update an existing sales invoice
		except AttributeError as e:
			frappe.local.response['http_status_code'] = 405  # HTTP 405 Method Not Allowed
			frappe.local.response['message'] = (_("Method not allowed."))
	elif method == 'DELETE':
		try:
			return cls.delete(record_id, **kwargs)  # Delete an existing sales invoice
		except AttributeError as e:
			frappe.local.response['http_status_code'] = 405  # HTTP 405 Method Not Allowed
			frappe.local.response['message'] = (_("Method not allowed."))
	else:
		frappe.local.response['http_status_code'] = 405  # HTTP 405 Method Not Allowed
		frappe.local.response['message'] = (_("Method not allowed."))


@frappe.whitelist(allow_guest=True)
@jwt_required
def item_api(**kwargs):
	_routes_api(ItemAPI, **kwargs)


@frappe.whitelist(allow_guest=True)
@jwt_required
def item_group_api(**kwargs):
	_routes_api(ItemGroupAPI, **kwargs)


@frappe.whitelist(allow_guest=True)
@jwt_required
def sales_invoice_api(**kwargs):
	_routes_api(SalesInvoiceAPI, **kwargs)


@frappe.whitelist(allow_guest=True)
@jwt_required
def pos_profiles_api(**kwargs):
	_routes_api(POSProfileAPI, **kwargs)


@frappe.whitelist(allow_guest=True)
@jwt_required
def customers_api(**kwargs):
	_routes_api(CustomerAPI, **kwargs)
