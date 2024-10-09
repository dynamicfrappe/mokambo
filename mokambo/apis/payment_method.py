import frappe
from frappe import _

from mokambo.apis.jwt_decorator import jwt_required



def _pos_profiles_payment_methods(pos_profile_name):
	"""
	API to fetch payment methods of a POS profile.

	Args:
		pos_profile_name (str): The name of the POS profile.

	Returns:
		list: Payment methods associated with the POS profile.
	"""
	# Fetch the POS Profile document
	pos_profile = frappe.get_doc('POS Profile', pos_profile_name)
	# Get the associated payment methods from the child table
	payment_methods = []
	if pos_profile:
		for method in pos_profile.payments:
			payment_methods.append({
				'name': method.name,
				'mode_of_payment': method.mode_of_payment,
				'default': method.default,
			})
	# payment_methods = PaymentMethodAPI.get(pos_profile_name)
	return payment_methods


class PaymentMethodAPI:

	@classmethod
	def get(cls, pos_profile_name, **kwargs):
		"""
		Fetch payment methods for the given POS Profile.

		Args:
			pos_profile_name (str): The name or ID of the POS Profile.

		Returns:
			list: A list of payment methods associated with the POS Profile.
		"""
		try:
			# Get the associated payment methods from the child table
			payment_methods = _pos_profiles_payment_methods(pos_profile_name)
			if payment_methods:
				# Success Response
				frappe.local.response['http_status_code'] = 200  # HTTP 200 OK
				frappe.local.response['data'] = payment_methods

		except frappe.DoesNotExistError:
			frappe.local.response['http_status_code'] = 404  # Not Found
			frappe.local.response['message'] = _("POS Profile not found.")
		except Exception as e:
			frappe.local.response['http_status_code'] = 500  # Internal Server Error
			frappe.local.response['message'] = _(
				"An error occurred while fetching payment methods.")
