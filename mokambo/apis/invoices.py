import frappe
from frappe import _

from mokambo.apis.jwt_decorator import jwt_required


@frappe.whitelist(allow_guest=True, methods=['POST'])
@jwt_required
def create_pos_invoice():
	customer = frappe.form_dict.get("customer")
	items = frappe.form_dict.get("items")
	payments = frappe.form_dict.get("payments")
	is_submit = frappe.form_dict.get("is_submit")
	print(frappe.form_dict)
	if not customer or not items or not payments:
		return {
			"status": "error",
			"error": _("Missing required parameters")
		}
	try:
		# Create a new Sales Invoice document
		invoice = frappe.get_doc({
			'doctype': 'Sales Invoice',
			'customer': customer,
			'is_pos': 1,  # Mark as POS Invoice
			'items': items,
			'payments': payments,
			'docstatus': 1  # Submit the document
		})

		# Insert and submit the document
		invoice.insert()
		if is_submit:
			invoice.submit()

		return {
			"status": "success",
			"invoice_name": invoice.name
		}

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), _("POS Invoice Creation Failed"))
		return {
			"status": "error",
			"error": str(e)
		}


@frappe.whitelist(allow_guest=True, methods=['GET'])
@jwt_required
def get_pos_invoices():
	invoices = frappe.get_all('Sales Invoice', fields=[
		'name', 'posting_date', 'grand_total', 'customer', 'customer_name', 'outstanding_amount',
		'status', 'is_return'
	])
	frappe.local.response['data'] = invoices


@frappe.whitelist(allow_guest=True, methods=['GET'])
@jwt_required
def get_pos_invoice(name):
	invoice = frappe.get_doc(doctype='Sales Invoice', filters={'name': name})
	frappe.local.response['data'] = invoice.items
