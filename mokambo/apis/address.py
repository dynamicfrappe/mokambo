
from dataclasses import fields
import frappe
from frappe import _


def _get_address(**kwargs):
	"""Fetch a list of Zones"""
	try:
		if kwargs.get('customer_id'):
			# Success Response
			frappe.local.response['http_status_code'] = 200  # HTTP 200 OK

		else:
			# Fetch all zones
			zones = frappe.get_list(
				'Territory',
				fields=['name'],
				filters = {'parent_territory': ['!=', '']},
				ignore_permissions=True
			)
			# Success Response
			frappe.local.response['http_status_code'] = 200  # HTTP 200 OK
			frappe.local.response['data'] = zones
	except Exception as e:
		# Generic error handling
		frappe.local.response['http_status_code'] = 500  # HTTP 500 Internal Server Error
		frappe.local.response['message'] = _("Unable to fetch POS Profiles: {0}").format(str(e))


class AddressAPI:
	@staticmethod
	def get(**kwargs):
		_get_address(**kwargs)


