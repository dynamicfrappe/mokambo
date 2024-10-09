import frappe
from frappe import _

from mokambo.apis.auth import get_user_pos_profile


def create_pos_invoice(**kwargs):
	"""Create a new POS Invoice"""
	try:
		# Validate incoming data
		required_fields = ['customer', 'items']
		for field in required_fields:
			if field not in kwargs:
				frappe.local.response['http_status_code'] = 400  # Bad Request
				frappe.local.response['message'] = _("Field '{0}' is required.").format(field)
				return

		# Fetch the default mode of payment from the POS Profile
		user = frappe.local.user
		pos_profile = get_user_pos_profile(user.name)
		pos_profile = frappe.get_doc('POS Profile', pos_profile)
		default_payment_mode = pos_profile.get('payments')[0].get('mode_of_payment')  # Default to 'Cash' if not found

		# Create a new POS Invoice document
		pos_invoice = frappe.get_doc({
			'doctype': 'POS Invoice',
			'customer': kwargs['customer'],
			'items': [{
				'item_code': item['item_code'],
				'qty': item['qty'],
				'uom': item.get('uom', 'Unit')  # Default to 'Unit' if UOM is not provided
			} for item in kwargs['items']],
			'payments': [
				{'mode_of_payment': default_payment_mode}  # Use the default payment mode from the POS Profile
			],
			'is_pos': 1,  # Mark as POS Invoice
			'posting_date': kwargs.get('posting_date', frappe.utils.nowdate()),  # Optional field
			'posting_time': kwargs.get('posting_time', frappe.utils.nowtime()),  # Optional field
		})

		# Insert the document into the database
		pos_invoice.insert(ignore_permissions=True)

		# Success Response
		frappe.local.response['http_status_code'] = 201  # HTTP 201 Created
		frappe.local.response['data'] = {
			'name': pos_invoice.name,
			'message': _("POS Invoice created successfully.")
		}

	except frappe.ValidationError as ve:
		frappe.local.response['http_status_code'] = 400  # Bad Request
		frappe.local.response['message'] = str(ve)

	except Exception as e:
		# Generic error handling
		frappe.local.response['http_status_code'] = 500  # HTTP 500 Internal Server Error
		frappe.local.response['message'] = _("Unable to create POS Invoice: {0}").format(str(e))


class POSInvoiceAPI:
	@staticmethod
	def get(**kwargs):
		"""Fetch a list or a specific Sales invoice"""
		"""Fetch a list or a specific Sales invoice"""
		sales_invoice_id = kwargs.get('sales_invoice_id')
		page = int(kwargs.get('page', 1))  # Default to page 1 if not provided
		page_size = int(kwargs.get('page_size', 10))  # Default to 10 records per page

		sales_invoice_id = kwargs.get('sales_invoice_id')
		if sales_invoice_id:
			try:
				sales_invoice = frappe.get_doc('POS Invoice', sales_invoice_id)
				# Success Response
				frappe.local.response['http_status_code'] = 200  # HTTP 200 OK
				frappe.local.response['data'] = sales_invoice
			except frappe.DoesNotExistError:
				# If sales invoice does not exist
				frappe.local.response['http_status_code'] = 404  # HTTP 404 Not Found
				frappe.local.response['message'] = _("Sales Invoice {0} not found").format(sales_invoice_id)
			except Exception as e:
				# Generic error handling
				frappe.local.response['http_status_code'] = 500  # HTTP 500 Internal Server Error
				frappe.local.response['message'] = _("Unable to fetch Sales Invoice: {0}").format(str(e))
		else:
			try:
				# Calculate the starting record
				start = (page - 1) * page_size

				filters = {}
				if kwargs.get('status'):
					filters['status'] = kwargs.get('status')
				# Fetch paginated records
				pos_invoices = frappe.get_all(
					'POS Invoice',
					fields=[
						'name', 'customer', 'posting_date', 'posting_time', 'contact_mobile',
						'grand_total', 'outstanding_amount', 'status', 'is_return',
					],
					filters=filters,
					limit_start=start,  # Start from this record
					limit_page_length=page_size,  # Number of records to fetch
					ignore_permissions=True
				)

				# Fetch total number of records (for calculating total pages)
				total_records = frappe.db.count('POS Invoice')
				total_pages = (total_records + page_size - 1) // page_size  # Calculate total pages

				# Success Response
				frappe.local.response['http_status_code'] = 200  # HTTP 200 OK
				frappe.local.response['data'] = {
					'invoices': pos_invoices,
					'page': page,
					'page_size': page_size,
					'total_pages': total_pages,
					'total_records': total_records,
				}
			except Exception as e:
				# Generic error handling
				frappe.local.response['http_status_code'] = 500  # HTTP 500 Internal Server Error
				frappe.local.response['message'] = _("Unable to fetch Sales Invoices: {0}").format(str(e))

	@staticmethod
	def post(**kwargs):
		"""Create a new Sales Invoice."""
		try:
			create_pos_invoice(**kwargs)
		except frappe.ValidationError as ve:
			frappe.local.response['http_status_code'] = 400  # Bad Request
			frappe.local.response['message'] = str(ve)

	@staticmethod
	def put(**kwargs):
		"""Update an existing Sales Invoice."""
		sales_invoice_id = kwargs.get('sales_invoice_id')
		try:
			sales_invoice = frappe.get_doc('Sales Invoice', sales_invoice_id)
			sales_invoice.update(kwargs)
			sales_invoice.save()
			return {
				"message": _("Sales Invoice {0} updated successfully").format(sales_invoice_id)}
		except frappe.DoesNotExistError:
			frappe.throw(_("Sales Invoice {0} not found").format(sales_invoice_id))
		except Exception as e:
			frappe.throw(_("Unable to update Sales Invoice: {0}").format(str(e)))
