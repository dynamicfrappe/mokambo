
from dataclasses import fields
import frappe
from frappe import _


def _get_zone(**kwargs):
	"""Fetch a list of Zones"""
	try:
		# Fetch all zones
		zones = frappe.get_list(
			'Territory',
			fields=['name'],
			filters = {'parent_territory': ['!=', '']},
			ignore_permissions=True
		)
  
		frappe.local.response["http_status_code"] = 200
		frappe.local.response['data'] = zones
		frappe.local.response["message"] = _('Zones fetched successfully')
	except Exception as e:
		# Generic error handling
		frappe.local.response['http_status_code'] = 500  # HTTP 500 Internal Server Error
		frappe.local.response['message'] = _("Unable to fetch zones: {0}").format(str(e))

  
class ZoneAPI:
	@staticmethod
	def get(**kwargs):
		_get_zone(**kwargs)
  
  
