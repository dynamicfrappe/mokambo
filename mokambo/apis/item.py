import frappe
from frappe import _

def get_user_warehouse():
	"""Get the default warehouse based on the POS profile of the logged-in user."""

	# Fetch the pos_profile linked to the logged-in user from the child table `POS Profile User`
	pos_profile = frappe.db.get_value(
		"POS Profile User",
		{"user": frappe.local.user.name},
		["parent"],  # This retrieves the parent (POS Profile) linked to the user
	)

	# If a POS profile is found, fetch the warehouse
	if pos_profile:
		warehouse = frappe.db.get_value('POS Profile', {'name': pos_profile}, ['warehouse'])
		if warehouse:
			return warehouse
		else:
			frappe.local.response["http_status_code"] = 403
			frappe.local.response["message"] = _('There is no wherehouse linked to the POS Profile')
	else:
		frappe.local.response["http_status_code"] = 403
		frappe.local.response["message"] = _('User has no POS Profile')


def _get_bulk_item_stock(item_codes, warehouse=None):
	"""Fetch stock for all items in bulk, optionally filtering by warehouse."""
	filters = {"item_code": ["in", item_codes]}
	if warehouse:
		filters["warehouse"] = warehouse
	stock_data = frappe.db.get_all(
		'Bin',
		fields=['item_code', 'stock_uom', 'actual_qty'],
		filters=filters,
		ignore_permissions=True
	)

	# Group stock quantities by item code
	stock_map = {}
	for stock in stock_data:
		item_code = stock['item_code']
		if item_code not in stock_map:
			stock_map[item_code] = {}
		stock_map[item_code][stock['stock_uom']] = stock['actual_qty']

	return stock_map


def _get_bulk_item_prices(item_codes):
	"""Fetch prices for all items in bulk."""
	item_prices = frappe.db.get_all(
		'Item Price',
		fields=['item_code', 'uom', 'price_list_rate as rate'],
		filters={'item_code': ['in', item_codes]},
		ignore_permissions=True
	)

	# Group prices by item code
	price_map = {}
	for price in item_prices:
		item_code = price['item_code']
		if item_code not in price_map:
			price_map[item_code] = []
		price_map[item_code].append({
			'uom': price['uom'],
			'rate': price['rate']
		})

	return price_map


def _get_unique_uom_prices(uom_prices):
	# Use a dictionary to avoid duplicate UOMs
	unique_uom_prices = {}

	for uom_price in uom_prices:
		uom = uom_price['uom']
		if uom not in unique_uom_prices:
			# Add the UOM if it is not already in the dictionary
			unique_uom_prices[uom] = uom_price
		else:
			# Handle duplicates, e.g., keep the lowest or highest rate if needed
			if uom_price['rate'] < unique_uom_prices[uom]['rate']:
				unique_uom_prices[uom] = uom_price

	# Convert back to a list
	return list(unique_uom_prices.values())


def _get_items_stock_prices(items):
	"""Get stock and prices for all items."""

	# Fetch warehouse from the POS profile of the logged-in user
	warehouse = get_user_warehouse()

	# Fetch item codes
	item_codes = [item['item_code'] for item in items]

	# Fetch all prices and stock in bulk
	prices_map = _get_bulk_item_prices(item_codes)
	stock_map = _get_bulk_item_stock(item_codes, warehouse)
	# Attach stock and prices to the items
	for item in items:
		uom_prices = prices_map.get(item['item_code'], [])

		# Set the first UOM price and stock (if available)
		if uom_prices:
			item['stock_price'] = uom_prices[0]['rate']
			item['stock_quantity'] = stock_map.get(item['item_code'], {}).get(uom_prices[0]['uom'],
																			  0)
		else:
			item['stock_price'] = None
			item['stock_quantity'] = 0

		# Attach the complete UOM price list to the item
		for uom_price in uom_prices:
			uom_price['quantity'] = stock_map.get(item['item_code'], {}).get(uom_price['uom'], 0)

		item['uom_prices'] = _get_unique_uom_prices(uom_prices)
	return items


def get_items_prices(**kwargs):
	"""Fetch items with prices and stock in bulk."""
	item_group = kwargs.get('item_group')


	# Fetch all items in one query
	filters = {}
	if item_group and item_group != 'All Item Groups':
		filters['item_group'] = item_group

	items = frappe.get_all(
		'Item',
		fields=[
			'name', 'item_name', 'item_code', 'image', 'description', 'item_group',
			'standard_rate', 'stock_uom'
		],
		filters=filters,
		ignore_permissions=True
	)
	frappe.local.response['data'] = _get_items_stock_prices(items)


class ItemAPI:
	@staticmethod
	def get(**kwargs):
		get_items_prices(**kwargs)
