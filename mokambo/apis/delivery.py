
from dataclasses import fields
import frappe
from frappe import _


def _get_deliveries(**kwargs):
	"""Fetch a list of deliveries based on pos_profile"""
	try:
		if not kwargs.get('pos_profile'):
			frappe.local.response["http_status_code"] = 400
			frappe.local.response["message"] = _('POS Profile is required')
			return
		else:
			# Fetch all deliveries
			deliveries = frappe.get_list(
				'Delivery',
				fields=['delivery','delivery_name'],
				filters = {'parent': kwargs.get('pos_profile')},
				ignore_permissions=True
			)
			# Success Response
			frappe.local.response['http_status_code'] = 200  # HTTP 200 OK
			frappe.local.response['data'] = deliveries
	except Exception as e:
		# Generic error handling
		frappe.local.response['http_status_code'] = 500  # HTTP 500 Internal Server Error
		frappe.local.response['message'] = _("Unable to fetch deliveries: {0}").format(str(e))


class DeliveryAPI:
	@staticmethod
	def get(**kwargs):
		_get_deliveries(**kwargs)


