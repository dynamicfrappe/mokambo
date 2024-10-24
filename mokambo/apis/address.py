
from dataclasses import fields
import frappe
from frappe import _

def get_address_list(**kwargs):
	"""Fetch a list of Addresses"""
	return frappe.get_all(
			'Address',
			fields=['name', 'address_title', 'address_line1', 'city', 'phone'],
			filters={'address_title': kwargs.get('customer')},
			ignore_permissions=True
		)

def _get_address(**kwargs):
	"""Fetch a list of Zones"""
	try:
		if not kwargs.get('customer'):
			frappe.local.response["http_status_code"] = 400
			frappe.local.response["message"] = _('Customer is required')
			return
		
		address_list = get_address_list(**kwargs)
  
		# Success Response
		frappe.local.response['http_status_code'] = 200  # HTTP 200 OK
		frappe.local.response['data'] = address_list
	except Exception as e:
		# Generic error handling
		frappe.local.response['http_status_code'] = 500  # HTTP 500 Internal Server Error
		frappe.local.response['message'] = _("Unable to fetch Customer addresses: {0}").format(str(e))

def _create_address(**kwargs):
	"""Create a new address"""
	try:
		if not kwargs.get('customer'):
			frappe.local.response['http_status_code'] = 400  # Bad Request	
			frappe.local.response['message'] = _("Customer is required.")
			return

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
  
		# Fetch addresses after commited
		address_list = get_address_list(**kwargs)

		# Success Response
		frappe.local.response['http_status_code'] = 201
		frappe.local.response['data'] = address_list
		frappe.local.response['message'] = _("Address is created successfully.")
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

