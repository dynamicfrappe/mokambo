
from dataclasses import fields
import frappe
from frappe import _


def _get_address(**kwargs):
	"""Fetch a list of Zones"""
	try:
		if not kwargs.get('customer'):
			# Fetch all zones
			zones = frappe.get_list(
				'Territory',
				fields=['name'],
				filters = {'parent_territory': ['!=', '']},
				ignore_permissions=True
			)
			frappe.local.response["http_status_code"] = 200
			frappe.local.response['data'] = zones
			# frappe.local.response["message"] = _('Zones fetched successfully')
   
			# frappe.local.response["http_status_code"] = 400
			# frappe.local.response["message"] = _('Customer is required')
			return

		# Fetch address
		address_list = frappe.get_all(
			'Address',
			fields=['name', 'address_title', 'address_line1', 'city', 'phone'],
			filters={'address_title': kwargs.get('customer')},
			ignore_permissions=True
		)

		
		# Success Response
		frappe.local.response['http_status_code'] = 200  # HTTP 200 OK
		frappe.local.response['data'] = address_list
	except Exception as e:
		# Generic error handling
		frappe.local.response['http_status_code'] = 500  # HTTP 500 Internal Server Error
		frappe.local.response['message'] = _("Unable to fetch zones: {0}").format(str(e))

def _create_address(**kwargs):
	"""Create a new address"""
	try:
		if kwargs.get('customer'):
			# Create new address
			address = frappe.get_doc({
				'doctype': 'Address',
   			 	'address_title': kwargs.get('customer'),
				'address_type': "Shipping",
				'address_line1': kwargs.get('address'),
				'city': kwargs.get('zone'),
				'territory': kwargs.get('zone'),
				'country': "Egypt",
				'phone': kwargs.get('mobile_no'),
			}).insert(ignore_permissions=True)
			address.save()
			frappe.db.commit()
			# Fetch address
			address_list = frappe.get_all(
				'Address',
				fields=['address_title', 'address_line1', 'city', 'phone'],
				filters={'address_title': kwargs.get('customer')},
				ignore_permissions=True
			)

			# Success Response
			frappe.local.response['http_status_code'] = 201  # HTTP 200 OK
			frappe.local.response['data'] = address_list
			frappe.local.response['message'] = _("Address is creadted successfully.")
		else:
			frappe.local.response['http_status_code'] = 400  # Bad Request	
			frappe.local.response['message'] = _("Customer is required.")
   
	except Exception as e:	
		# Generic error handling
		frappe.local.response['http_status_code'] = 500  # HTTP 500 Internal Server Error
		frappe.local.response['message'] = _("Unable to create address: {0}").format(str(e))
  
class AddressAPI:
	@staticmethod
	def get(**kwargs):
		_get_address(**kwargs)
	@staticmethod
	def post(**kwargs):
		_create_address(**kwargs)

