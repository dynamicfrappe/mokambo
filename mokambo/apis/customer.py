from dataclasses import fields

import frappe
from frappe import _


def create_contact(kwargs, customer):
	contact = frappe.new_doc('Contact')
	contact.first_name = customer.customer_name
	contact.append('phone_nos', {
		"phone": kwargs.get('mobile_no'),
		"is_primary_mobile_no": 1
	})
	contact.append('links', {
		"link_doctype": "Customer",
		"link_name": customer.name,
		"link_type": customer.customer_name,
	})
	contact.insert(ignore_permissions=True)
	return contact


def create_address(kwargs, customer):
	address = frappe.new_doc('Address')
	address.address_type ="Shipping"
	address.address_title = customer.customer_name
	address.address_line1 = kwargs.get('address')
	address.city = kwargs.get('zone')
	address.country = "Egypt"
	address.phone = kwargs.get('mobile_no')
	address.append('links', {
		"link_doctype": "Customer",
		"link_name": customer.name,
		"link_type": customer.customer_name,
	})
	address.insert(ignore_permissions=True)
	return address


def _get_customers(**kwargs):
	"""Fetch a list of Customers"""
	try:
		filters = []
		customer_name = kwargs.get('customer_name')
		mobile_no = kwargs.get('mobile_no')

		# Add filters using icontains (LIKE %value%) for case-insensitive search
		if customer_name:
			filters.append(['customer_name', 'like', f'%{customer_name}%'])
		if mobile_no:
			filters.append(['mobile_no', 'like', f'%{mobile_no}%'])

		# Fetch all POS Profile documents with necessary fields
		customers = frappe.get_list(
			'Customer',
			fields=['name', 'customer_name', 'territory'],
			filters=filters,
			ignore_permissions=True
		)
		for customer in customers:
			customer_id = frappe.get_doc("Customer", customer.get("name"))
			customer_address = frappe.get_value("Address", customer_id.customer_primary_address, 'address_line1')
			mobile_no = frappe.get_value("Address", customer_id.customer_primary_address, 'phone')
			customer['mobile_no'] = mobile_no
			customer['address'] = customer_address

		# Success Response
		frappe.local.response['http_status_code'] = 200  # HTTP 200 OK
		frappe.local.response['data'] = customers
	except Exception as e:
		# Generic error handling
		frappe.local.response['http_status_code'] = 500  # HTTP 500 Internal Server Error
		frappe.local.response['message'] = _("Unable to fetch customers list: {0}").format(str(e))


def _add_customer(**kwargs):
	"""Create New customer"""
	try:
		required_fields = ['customer', 'mobile_no', 'address', 'zone']
		for field in required_fields:
			if kwargs.get(field) == "":
				frappe.local.response['http_status_code'] = 400  # Bad Request
				frappe.local.response['message'] = _("Field '{0}' is required.").format(field)
				return

		customer_name = kwargs.get('customer')
		is_customer_existing = frappe.db.exists("Customer", customer_name)
		if is_customer_existing:
			frappe.local.response['http_status_code'] = 400  # Bad Request
			frappe.local.response['message'] = _("Customer {0} already exists.").format(customer_name)
			return

		# Create a new customer document
		customer = frappe.new_doc("Customer")
		customer.customer_name = kwargs.get('customer')
		customer.territory = kwargs.get('zone')

		customer.insert(ignore_permissions=True)

		# Create contact document
		contact = create_contact(kwargs, customer)

		# Create address document
		address = create_address(kwargs, customer)

		# Update the customer document with contact, address, and user details
		customer.customer_primary_contact = contact.name
		customer.customer_primary_address = address.name
		customer.mobile_no = address.phone
		customer.save(ignore_permissions=True)

		frappe.db.commit()

		# Success Response
		frappe.local.response['http_status_code'] = 200  # HTTP 200 OK
		frappe.local.response['message'] = f"Customer {customer_name} is created successfully."
	except Exception as e:
		# Generic error handling
		frappe.local.response['http_status_code'] = 500  # HTTP 500 Internal Server Error
		frappe.local.response['message'] = _("Unable to Create new customer: {0}").format(str(e))

class CustomerAPI:
	@staticmethod
	def get(**kwargs):
		_get_customers(**kwargs)

	@staticmethod
	def post(**kwargs):
		_add_customer(**kwargs)
