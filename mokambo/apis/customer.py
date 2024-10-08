import frappe
from frappe import _


def _get_customers(**kwargs):
	"""Fetch a list of Customers"""
	try:
		# Fetch all POS Profile documents with necessary fields
		customers = frappe.get_list('Customer', pluck='name')

		# Success Response
		frappe.local.response['http_status_code'] = 200  # HTTP 200 OK
		frappe.local.response['data'] = customers
	except Exception as e:
		# Generic error handling
		frappe.local.response['http_status_code'] = 500  # HTTP 500 Internal Server Error
		frappe.local.response['message'] = _("Unable to fetch POS Profiles: {0}").format(str(e))


class CustomerAPI:
	@staticmethod
	def get(cls, **kwargs):
		_get_customers(**kwargs)
