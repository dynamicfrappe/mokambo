import frappe
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder
from frappe.utils import date_diff, getdate

class CustomSalesOrder(SalesOrder):
	def before_save(self):
		print("Custom sales order")
		print(self.delivery_date)
		print(getdate())
		diff = date_diff(self.delivery_date, getdate())
		self.custom_days_to_delivery = diff
		print(self.custom_days_to_delivery)


def update_days_of_delivery():
	print("Updating days of delivery")
	orders = frappe.db.get_list("Sales Order", fields=["name", "delivery_date", "custom_days_to_delivery"])
	for order in orders:
		frappe.db.set_value("Sales Order", order.name, "custom_days_to_delivery", order.custom_days_to_delivery + 1 if order.custom_days_to_delivery else 1)
	frappe.db.commit()
