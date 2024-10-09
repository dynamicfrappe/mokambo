from dataclasses import fields

import frappe
from frappe import _


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
			fields=['name', 'customer_name', 'mobile_no'],
			filters=filters,
			ignore_permissions=True
		)

		# Success Response
		frappe.local.response['http_status_code'] = 200  # HTTP 200 OK
		frappe.local.response['data'] = customers
	except Exception as e:
		# Generic error handling
		frappe.local.response['http_status_code'] = 500  # HTTP 500 Internal Server Error
		frappe.local.response['message'] = _("Unable to fetch POS Profiles: {0}").format(str(e))


class CustomerAPI:
	@staticmethod
	def get(**kwargs):
		_get_customers(**kwargs)
