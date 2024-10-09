import frappe
from frappe import _


def _get_pos_profiles(**kwargs):
	"""Fetch a list of POS Profiles"""
	try:
		# Fetch all POS Profile documents with necessary fields
		pos_profiles = frappe.get_list(
			'POS Profile', fields=['name'], ignore_permissions=True
		)

		# Success Response
		frappe.local.response['http_status_code'] = 200  # HTTP 200 OK
		frappe.local.response['data'] = pos_profiles
	except Exception as e:
		# Generic error handling
		frappe.local.response['http_status_code'] = 500  # HTTP 500 Internal Server Error
		frappe.local.response['message'] = _("Unable to fetch POS Profiles: {0}").format(str(e))


class POSProfileAPI:
	@staticmethod
	def get(**kwargs):
		_get_pos_profiles(**kwargs)
