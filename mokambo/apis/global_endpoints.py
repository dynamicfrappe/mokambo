
from dataclasses import fields
import frappe
from frappe import _


def _get_request_source(**kwargs):
	"""Fetch a list of request sources"""
	try:
		sources = frappe.get_list(
			'Request Source',
			fields=['source'],
			ignore_permissions=True
		)
		# Success Response
		frappe.local.response['http_status_code'] = 200  # HTTP 200 OK
		frappe.local.response['data'] = sources
	except Exception as e:
		# Generic error handling
		frappe.local.response['http_status_code'] = 500  # HTTP 500 Internal Server Error
		frappe.local.response['message'] = _("Unable to fetch request sources: {0}").format(str(e))


class GlobalEndpointsAPI:
	@staticmethod
	def get(**kwargs):
		_get_request_source(**kwargs)


