
import frappe
from frappe import _

data = {
	'custom_fields': {
        'Sales Invoice':[	
            {
                "label": "Booking Type",
                "fieldname": "bookingtype",
                "insert_after": "due_date",
                "fieldtype":"Select",
                "options":"payment-now\ndelivery\npayment-later\nreservation",
            },
            # These fields are added by Mokambo for delivering details
            {
                "label": "Delivery Date",
                "fieldname": "delivery_date",
                "insert_after": "bookingtype",
                "fieldtype":"Date",
            },
            {
                "label": "Delivery Time",
                "fieldname": "delivery_time",
                "insert_after": "delivery_date",
                "fieldtype":"Time",
            },
            {
                "label": "Delivery",
                "fieldname": "delivery",
                "insert_after": "delivery_time",
                "fieldtype":"Link",
                "options":"Employee",
            },
            {
                "label": "Delivery Name",
                "fieldname": "delivery_name",
                "insert_after": "delivery",
                "fieldtype":"Data",
                "fetch_from": "delivery.employee_name"
                },
            {
                "label": "Is Delivered",
                "fieldname": "is_delivered",
                "insert_after": "delivery",
                "fieldtype":"Check",
            },
            
            {
                "label": "Request Source",
                "fieldname": "request_source",
                "insert_after": "customer",
                "fieldtype":"Link",
                "options":"Request Source"
            },
            {
                "label": "Mobile No",
                "fieldname": "mobile_no",
                "insert_after": "territory",
                "fieldtype":"Data",
                "fetch_from": "customer_address.phone"
                
            }
        ],
        'POS Profile User':[
            {
                "label": "Role Type",
                "fieldname": "role_type",
                "insert_after": "default",
                "fieldtype":"Select",
                "options":"Cashier\nCall-center",
                "in_list_view": 1
            },
        ],
        'POS Profile':[
            {
                "label": "Applicable for Deliveries",
                "fieldname": "delivery_sec",
                "insert_after": "applicable_for_users",
                "fieldtype":"Section Break",
            },
            {
                "label": "Applicable for Deliveries",
                "fieldname": "delivery_table",
                "insert_after": "delivery_sec",
                "fieldtype":"Table",
                "options":"Delivery",
            },
        ],
	},
		"properties": [
            		
	],  
}