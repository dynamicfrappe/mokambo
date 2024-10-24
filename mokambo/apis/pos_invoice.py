import frappe
from frappe import _
from datetime import datetime

from mokambo.apis.auth import get_user_pos_profile
from mokambo.apis.item import _get_bulk_item_prices, _get_bulk_item_stock, _get_items_stock_prices
from frappe.utils.data import flt, get_link_to_form, nowdate



def _get_payment_mode(default=False):
	"""Get the default mode of payment from the POS Profile"""
	user = frappe.local.user
	pos_profile = get_user_pos_profile(user.name)
	pos_profile = frappe.get_doc('POS Profile', pos_profile)
	if default:
		return pos_profile.get('payments')[0].get('mode_of_payment')
	else:
		return pos_profile.get('payments')


def create_pos_invoice(**kwargs):
	"""Create a new POS Invoice"""
	try:
		# Validate incoming data
		required_fields = ['customer', 'items', 'bookingType']
		for field in required_fields:
			if field not in kwargs:
				frappe.local.response['http_status_code'] = 400  # Bad Request
				frappe.local.response['message'] = _("Field '{0}' is required.").format(field)
				return
			if field == 'bookingType':
				if kwargs['bookingType'] == 'payment-later':
					required_fields.append('receivingTime')
				if kwargs['bookingType'] == 'reservation':
					required_fields.append('receivingDate')
				if kwargs['bookingType'] == 'delivery':
					required_fields.append('zone')
					required_fields.append('address_id')


		# Fetch the default mode of payment from the POS Profile
		default_payment_mode = _get_payment_mode(default=True)
		warehouse = frappe.db.get_value('POS Profile', kwargs.get('pos_profile'), 'warehouse')

		# Create a new POS Invoice document
		pos_invoice = frappe.get_doc({
			'doctype': 'Sales Invoice',
			'customer': kwargs['customer'],
			'due_date': kwargs.get('posting_date', frappe.utils.nowdate()),
			'request_source': kwargs.get('requestSource', 'Branch'),
			'is_pos': 1,  # Mark as POS Invoice
			'bookingtype': kwargs['bookingType'],
			'items': [{
				'item_code': item['item_code'],
				'qty': item['qty'],
				'uom': item.get('uom', 'Unit')  # Default to 'Unit' if UOM is not provided
			} for item in kwargs['items']],
			'payments': [
				{'mode_of_payment': default_payment_mode}  # Use the default payment mode from the POS Profile
			],
			'posting_date': kwargs.get('posting_date', frappe.utils.nowdate()),  # Optional field
			'posting_time': kwargs.get('posting_time', frappe.utils.nowtime()),  # Optional field
			'pos_profile': kwargs.get("pos_profile"),
   			'update_stock': 1,
			'set_warehouse': warehouse
		})


		if kwargs['bookingType'] == 'payment-later':
			dt_object =  datetime.strptime(kwargs['receivingTime'], "%I:%M %p")
			pos_invoice.delivery_date = kwargs.get('posting_date', frappe.utils.nowdate())
			pos_invoice.delivery_time = dt_object.strftime("%H:%M:00")
		if kwargs['bookingType'] == 'reservation':
			dt_object = datetime.strptime(kwargs['receivingDate'], "%Y-%m-%d %I:%M %p")
			pos_invoice.delivery_date = dt_object.strftime("%Y-%m-%d")
			pos_invoice.delivery_time = dt_object.strftime("%H:%M:00")

	

		# Add contact details to the POS Invoice
		if kwargs['bookingType'] == 'delivery':
			# Fetch contact details
			#  create new address
			# address = frappe.new_doc('Address')
			# address.address_type = 'Shipping'
			# address.address_title =  kwargs['customer']
			# address.address_line1 = contact['address']
			# address.phone = contact['mobile_no']
			# address.city = kwargs['zone']
			# address.insert(ignore_permissions=True)
			# address.save()
			# frappe.db.commit()
			pos_invoice.territory = kwargs['zone']
			pos_invoice.customer_address = kwargs['address_id']
		
		# Insert the document into the database
		pos_invoice.insert(ignore_permissions=True)
		pos_invoice.save()
		frappe.db.commit()

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
		"""Fetch a list or a specific POS invoice"""
		page = int(kwargs.get('page', 1))  # Default to page 1 if not provided
		page_size = int(kwargs.get('page_size', 10))  # Default to 10 records per page

		pos_invoice_id = kwargs.get('full_invoice')
		if pos_invoice_id:
	  	# Fetch a specific Sales Invoice
			try:
				# Fetch the main POS Invoice fields
				pos_invoice = frappe.db.get_value(
					'Sales Invoice', pos_invoice_id,
					['name', 'bookingType', 'customer', 'pos_profile', 'grand_total', 'paid_amount', 'status', 'docstatus', 'total_net_weight',
					'is_delivered'],
					as_dict=True
				)
				if not pos_invoice:
					# If pos invoice does not exist
					frappe.local.response['http_status_code'] = 404  # HTTP 404 Not Found
					frappe.local.response['message'] = _("POS Invoice {0} not found").format(pos_invoice_id)
					return
				# print('pos_invoice ==> ', pos_invoice)
				items = frappe.get_all(
					'Sales Invoice Item',  # Child DocType
					filters={'parent': pos_invoice_id},  # Filter by the parent (POS Invoice)
					fields=['item_code', 'item_name', 'qty', 'rate', 'amount', 'total_weight', 'uom'],
					# Fetch specific fields from the child table
				)
				items = _get_items_stock_prices(items)
				# Fetch the payments from the child table
				payments = _get_payment_mode()
				customer = frappe.get_value(
					'Customer',
					pos_invoice.get('customer'),
					['name', 'customer_name', 'mobile_no'],
					as_dict=True
	 			)
				address = frappe.db.get_value('Address', frappe.db.get_value('Sales Invoice', pos_invoice_id, 'customer_address'),
					['address_line1', 'phone', 'city'],
					as_dict=True
				)
				pos_invoice['address'] = address
				# Add items and payments to the pos_invoice dict
				pos_invoice['items'] = items
				pos_invoice['customer'] = customer
				pos_invoice['default_payment_mode'] = _get_payment_mode(default=True)
				pos_invoice['payments'] = payments
				# Success Response
				frappe.local.response['http_status_code'] = 200  # HTTP 200 OK
				frappe.local.response['data'] = pos_invoice
			except frappe.DoesNotExistError:
				# If pos invoice does not exist
				frappe.local.response['http_status_code'] = 404  # HTTP 404 Not Found
				frappe.local.response['message'] = _("POS Invoice {0} not found").format(pos_invoice_id)
			except Exception as e:
				# Generic error handling
				frappe.local.response['http_status_code'] = 500  # HTTP 500 Internal Server Error
				frappe.local.response['message'] = _("Unable to fetch POS Invoice: {0}").format(str(e))
		else:
			try:
				# Calculate the starting record
				start = (page - 1) * page_size

				filters = {}
				if kwargs.get('docstatus'):
					filters['docstatus'] = kwargs.get('docstatus')
				if kwargs.get('pos_invoice_id'):
					filters['name'] = kwargs.get('pos_invoice_id')
				if kwargs.get('booking_type'):
					filters['bookingtype'] = kwargs.get('booking_type')
				if kwargs.get('customer'):
					customer_name = kwargs.get('customer')
					filters['customer_name'] = ['like', f'%{customer_name}%']

				if kwargs.get('start_date') and kwargs.get('end_date'):
					filters['posting_date'] = ['between', [kwargs['start_date'], kwargs['end_date']]]
				if kwargs.get('pos_profile'):
					filters['pos_profile'] = kwargs.get('pos_profile')
				if kwargs.get('mobile_no'):
					filters['mobile_no'] = kwargs.get('mobile_no')
				# Fetch paginated records
				pos_invoices = frappe.db.get_all(
					'Sales Invoice',
					fields=[
						'name', 'bookingType', 'customer', 'mobile_no', 'posting_date', 'posting_time',
						'grand_total', 'outstanding_amount', 'status', 'docstatus', 'is_return', 'is_delivered', 'territory', 'delivery', 'delivery_name'
					],
					filters=filters,
					limit_start=start,  # Start from this record
					limit_page_length=page_size,  # Number of records to fetch
					ignore_permissions=True
				)

				# Fetch total number of records (for calculating total pages)
				total_records = frappe.db.count('Sales Invoice', filters=filters)
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
				frappe.local.response['message'] = _("Unable to fetch POS Invoices: {0}").format(str(e))

	@staticmethod
	def post(**kwargs):
		"""Create a new POS Invoice."""
		try:
			create_pos_invoice(**kwargs)
		except frappe.ValidationError as ve:
			frappe.local.response['http_status_code'] = 400  # Bad Request
			frappe.local.response['message'] = str(ve)

	@staticmethod
	def put(**kwargs):
		"""Update an existing POS Invoice."""
		pos_invoice_id = kwargs.pop('pos_invoice_id')
		try:

			pos_invoice = frappe.get_all(
				'Sales Invoice',
				filters={'name': pos_invoice_id},
				ignore_permissions=True
			)

			if pos_invoice:
				pos_invoice = frappe.get_doc('Sales Invoice', pos_invoice[0].name)

			if pos_invoice.docstatus == 2:
				# Invoice is cancelled
				frappe.local.response['message'] = _("Sales Invoice {0} is Cancelled").format(pos_invoice_id)
				frappe.local.response['http_status_code'] = 400  # HTTP 404 Not Found
				return

			# # Update customer field if provided
			# if 'customer' in kwargs:
			# 	pos_invoice.customer = kwargs.get('customer')

			# Update payments if provided
			if 'payments' in kwargs:
				for payment_data in kwargs['payments']:
					payment_data['base_amount'] = payment_data['amount']
					pos_invoice.append('payments', payment_data)
				paid_amount = 0.0
				base_paid_amount = 0.0
				for data in pos_invoice.payments:
					data.base_amount = flt(data.amount * pos_invoice.conversion_rate, pos_invoice.precision("base_paid_amount"))
					paid_amount += data.amount
					base_paid_amount += data.base_amount
				pos_invoice.paid_amount = paid_amount
				pos_invoice.base_paid_amount = base_paid_amount	

			
			
			# frappe.db.set_value("Sales Invoice", pos_invoice, {"customer", kwargs.get('customer')})
			if 'delivery' in kwargs and pos_invoice.docstatus == 0:
				pos_invoice.delivery = kwargs.get('delivery')

			pos_invoice.save(ignore_permissions=True)
			frappe.db.commit()
     
			if pos_invoice.bookingtype == 'payment-now' or pos_invoice.bookingtype == 'delivery':
				if pos_invoice.total == pos_invoice.paid_amount	:
					pos_invoice.is_delivered = 1
					pos_invoice.save(ignore_permissions=True)
					pos_invoice.submit()
					frappe.db.commit()
			else:
				if pos_invoice.paid_amount > 0.0 and pos_invoice.paid_amount < pos_invoice.total:
					pos_invoice.save(ignore_permissions=True)
					pos_invoice.submit()
					frappe.db.commit()
				if pos_invoice.total == pos_invoice.paid_amount	:
					pos_invoice.is_delivered = 1
					pos_invoice.save(ignore_permissions=True)
					if pos_invoice.docstatus == 0:
						pos_invoice.submit()
					frappe.db.commit()
				
   
			frappe.local.response['message'] = _("POS Invoice {0} updated successfully").format(pos_invoice_id)
		except frappe.DoesNotExistError:
			# If POS invoice does not exist
			frappe.local.response['http_status_code'] = 404  # HTTP 404 Not Found
			frappe.local.response['message'] = _("POS Invoice {0} not found").format(pos_invoice_id)
		except Exception as e:
			# Generic error handling
			frappe.local.response['http_status_code'] = 500  # HTTP 500 Internal Server Error
			frappe.local.response['message'] = _("Unable to update POS Invoice: {0}").format(str(e))
