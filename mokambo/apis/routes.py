import frappe
from frappe import _

from mokambo.apis.customer import CustomerAPI
from mokambo.apis.jwt_decorator import jwt_required
from mokambo.apis.item import ItemAPI
from mokambo.apis.item_group import ItemGroupAPI
from mokambo.apis.payment_method import PaymentMethodAPI
from mokambo.apis.pos_invoice import POSInvoiceAPI
from mokambo.apis.pos_profiles import POSProfileAPI
from mokambo.apis.shift import ShiftAPI
from mokambo.apis.address import AddressAPI
from mokambo.apis.delivery import DeliveryAPI
from mokambo.apis.global_endpoints import GlobalEndpointsAPI
from mokambo.apis.zone import ZoneAPI


def _check_and_get_method(cls: type, method: str):
	"""
	Check if the method exists in the class and return the method.

	Args:
		cls (type): The class to check.
		method (str): The HTTP method (GET, POST, etc.).

	Returns:
		callable: The class method if it exists, otherwise None.
	"""
	method_name = method.lower()
	if hasattr(cls, method_name):
		return getattr(cls, method_name)

	frappe.local.response['http_status_code'] = 405  # HTTP 405 Method Not Allowed
	frappe.local.response['message'] = _("Method not allowed.")
	return None


def _routes_api(cls, **kwargs):
	method = frappe.request.method
	record_id = kwargs.get('id')

	# Create an instance of the class if methods are instance methods
	instance = cls()

	# Define the method mappings
	method_map = {
		'GET': lambda: instance.get(**kwargs) if record_id else instance.get(**kwargs),
		'POST': lambda: instance.post(**kwargs),
		'PUT': lambda: instance.put(**kwargs),
		'DELETE': lambda: instance.delete(**kwargs)
	}

	# Check if the method is allowed and exists
	api_method = _check_and_get_method(cls, method)
	if api_method:
		return method_map[method]()  # Execute the appropriate method
	else:
		return None


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
def pos_profiles_api(**kwargs):
	_routes_api(POSProfileAPI, **kwargs)


@frappe.whitelist(allow_guest=True)
@jwt_required
def customers_api(**kwargs):
	_routes_api(CustomerAPI, **kwargs)


@frappe.whitelist(allow_guest=True)
@jwt_required
def payment_methods_api(**kwargs):
	_routes_api(PaymentMethodAPI, **kwargs)


@frappe.whitelist(allow_guest=True)
@jwt_required
def pos_invoices_api(**kwargs):
	_routes_api(POSInvoiceAPI, **kwargs)

@frappe.whitelist(allow_guest=True)
@jwt_required
def shift_api(**kwargs):
	_routes_api(ShiftAPI, **kwargs)

@frappe.whitelist(allow_guest=True)
@jwt_required
def address_api(**kwargs):
	_routes_api(AddressAPI, **kwargs)

@frappe.whitelist(allow_guest=True)
@jwt_required
def global_api(**kwargs):
	_routes_api(GlobalEndpointsAPI, **kwargs)
	
@frappe.whitelist(allow_guest=True)
@jwt_required
def delivery_api(**kwargs):
	_routes_api(DeliveryAPI, **kwargs)
 
@frappe.whitelist(allow_guest=True)
@jwt_required
def zone_api(**kwargs):
	_routes_api(ZoneAPI, **kwargs)
	