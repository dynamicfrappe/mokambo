
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
        ],
        'POS Profile User':[
            {
                "label": "Role Type",
                "fieldname": "role_type",
                "insert_after": "default",
                "fieldtype":"Select",
                "options":"Cashier\nCall-center",
            },
        ]
	},
		"properties": [
            		
	],  
}