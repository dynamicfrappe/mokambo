import frappe
from frappe import _
from datetime import datetime

def get_shift_status(**kwargs):
	# Validate incoming data
	required_fields = ['user', 'pos_profile']
	for field in required_fields:
		if not kwargs.get(field):
			frappe.local.response['http_status_code'] = 400  # Bad Request
			frappe.local.response['message'] = _("Field '{0}' is required.").format(field)
			return
	shift_id = frappe.db.get_all("POS Opening Entry",
	    filters = {'user': kwargs.get('user'), 'pos_profile': kwargs.get('pos_profile'), 'status': 'Open'},
	    fields= ['name']
		) 
	response = {}
	if shift_id:
		response['shift_id'] = shift_id[0].get('name')
	else:
		payment_methods = frappe.db.get_list("POS Payment Method",
			filters = {'parent': kwargs.get('pos_profile') }, 
			fields=['mode_of_payment'], ignore_permissions = True
		)
		response['shift_id'] = None
		response['methods'] = payment_methods

	frappe.local.response['http_status_code'] = 200  # HTTP 200 OK
	frappe.local.response['data'] = response

def open_shift(**kwargs):
	# Validate incoming data
	required_fields = ['user', 'pos_profile', 'methods']
	for field in required_fields:
		if not kwargs.get(field):
			frappe.local.response['http_status_code'] = 400  # Bad Request
			frappe.local.response['message'] = _("Field '{0}' is required.").format(field)
			return
	opening_shift = frappe.get_doc({
			'doctype': 'POS Opening Entry',
			'period_start_date': datetime.now(),
			'user': kwargs.get('user'),
			'pos_profile': kwargs.get('pos_profile'),
			'balance_details': [{
				'mode_of_payment': method['mode_of_payment'],
				'opening_amount': method['amount'],
			} for method in kwargs['methods']],
		})
	opening_shift.insert(ignore_permissions=True)
	opening_shift.save()
	opening_shift.submit()
	frappe.db.commit()
	response = {'shift_id': opening_shift.name}
	frappe.local.response['http_status_code'] = 201  # HTTP 201, Opening shift is created successfully
	frappe.local.response['data'] = response


def close_shift(shift_id):
	# Close shift
	closing_shift = frappe.get_doc({
			'doctype': 'POS Closing Entry',
			'pos_opening_entry': shift_id,
		})
	# Insert the document into the database
	closing_shift.insert(ignore_permissions=True)
	closing_shift.save(ignore_permissions=True)
	closing_shift.submit()
	frappe.db.commit()
	frappe.local.response['http_status_code'] = 201  # HTTP 201, shift is closed successfully

class ShiftAPI:
	@staticmethod
	def get(**kwargs):
		"""Validate shift status."""
		try:
			get_shift_status(**kwargs)
		except frappe.ValidationError as ve:
			frappe.local.response['http_status_code'] = 400  # Bad Request
			frappe.local.response['message'] = str(ve)

	@staticmethod
	def post(**kwargs):
		"""Toggle shift."""
		try:
			shift_id = kwargs.get('shift_id')
			if not shift_id:
				open_shift(**kwargs)
			else:
				close_shift(shift_id)
			
		except frappe.ValidationError as ve:
			frappe.local.response['http_status_code'] = 400  # Bad Request
			frappe.local.response['message'] = str(ve)