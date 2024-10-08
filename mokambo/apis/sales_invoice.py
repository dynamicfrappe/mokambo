import frappe
from frappe import _


class SalesInvoiceAPI:
	@staticmethod
	def get(cls, **kwargs):
		"""Fetch a list or a specific Sales invoice"""
		sales_invoice_id = kwargs.get('sales_invoice_id')
		if sales_invoice_id:
			try:
				sales_invoice = frappe.get_doc('Sales Invoice', sales_invoice_id)
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
				sales_invoices = frappe.get_all('Sales Invoice', fields=['name', 'customer'])
				# Success Response
				frappe.local.response['http_status_code'] = 200  # HTTP 200 OK
				frappe.local.response['data'] = sales_invoices
			except Exception as e:
				# Generic error handling
				frappe.local.response['http_status_code'] = 500  # HTTP 500 Internal Server Error
				frappe.local.response['message'] = _("Unable to fetch Sales Invoices: {0}").format(str(e))

	@staticmethod
	def post(cls, **kwargs):
		"""Create a new Sales Invoice."""
		try:
			new_sales_invoice = frappe.get_doc({
				"doctype": "Sales Invoice",
				"customer": kwargs.get('customer'),
				"items": kwargs.get('items')
			})
			new_sales_invoice.insert()
			return {"message": _("Sales Invoice created successfully"),
					"sales_invoice": new_sales_invoice.name}
		except Exception as e:
			frappe.throw(_("Unable to create Sales Invoice: {0}").format(str(e)))

	@staticmethod
	def put(cls, **kwargs):
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

	@staticmethod
	def delete(cls, **kwargs):
		"""Delete an existing Sales Invoice."""
		sales_invoice_id = kwargs.get('sales_invoice_id')
		try:
			frappe.delete_doc('Sales Invoice', sales_invoice_id)
			return {
				"message": _("Sales Invoice {0} deleted successfully").format(sales_invoice_id)}
		except frappe.DoesNotExistError:
			frappe.throw(_("Sales Invoice {0} not found").format(sales_invoice_id))
		except Exception as e:
			frappe.throw(_("Unable to delete Sales Invoice: {0}").format(str(e)))
