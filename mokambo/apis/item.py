import frappe


# def _get_item_price(item_code, price_list="Standard Selling"):
# 	item_price = frappe.get_value(
# 		"Item Price",
# 		{"item_code": item_code, "price_list": price_list},
# 		"price_list_rate"
# 	)
# 	return item_price
#
#
# def _get_item_stock_and_price(item_code, warehouse=None, price_list="Standard Selling"):
# 	# Get stock quantity
# 	stock = _get_item_stock(item_code, warehouse)
#
# 	# Get item price
# 	price = _get_item_price(item_code, price_list)
#
# 	return {
# 		"stock_quantity": stock,
# 		"price": price
# 	}
#
#
# def _get_stock_items(**kwargs):
# 	# Prepare base filters
# 	item_filters = []
# 	print('kwargs ==> ', kwargs)
# 	item_group = kwargs.get('item_group')
# 	if item_group:
# 		item_group = kwargs.get('item_group')
# 		item_filters.append("i.item_group = %s")
# 	price_list = "Standard Selling"
# 	# if kwargs.get('branch'):
# 	params = [price_list]
# 	print('item_group ==> ', item_group)
#
# 	if item_group:
# 		item_filters.append("i.item_group = %s")
# 		params.append(item_group)
#
# 	# if branch:
# 	# 	item_filters.append("i.custom_branch = %s")
# 	# 	params.append(branch)
# 	#
# 	# # Handle warehouse filter
# 	# warehouse_filter = "AND b.warehouse = %s" if warehouse else ""
# 	# if warehouse:
# 	# 	params.append(warehouse)
#
# 	# Combine filters
# 	item_filter = " AND ".join(item_filters) if item_filters else "1=1"
# 	warehouse_filter = "AND b.warehouse = %s" if kwargs.get('warehouse') else ""
# 	# Fetch data using Frappe ORM
# 	items = frappe.get_all(
# 		"Item",
# 		fields=[
# 			"name",
# 			"item_code",
# 			"item_name",
# 			"item_group",
# 			"image",
# 			"stock_uom",
# 			"custom_branch as branch",
# 			"MAX(IFNULL(tabBin.actual_qty, 0)) as stock_quantity",
# 			"MAX(IFNULL(tabItemPrice.price_list_rate, 0)) as price",
# 		],
# 		filters=item_filters,
# 		order_by="name",
# 		group_by="name, item_code, item_name, item_group, image, stock_uom",
# 		join=[
# 			"LEFT JOIN `tabBin` ON `tabItem`.item_code = `tabBin`.item_code {}".format(
# 				warehouse_filter),
# 			"LEFT JOIN `tabItem Price` ON `tabItem`.item_code = `tabItem Price`.item_code AND `tabItem Price`.price_list = %s"
# 		],
# 		as_list=True
# 	)
#
# 	# Prepare the response
# 	frappe.local.response['data'] = items
#
#
def _get_item_stock(item_code, uom, warehouse=None):
	filters = {"item_code": item_code, "stock_uom": uom}
	if warehouse:
		filters["warehouse"] = warehouse
	stock_quantity = frappe.get_value("Bin", filters, "actual_qty")
	return stock_quantity


def get_bulk_item_prices(item_codes):
	# Fetch all prices for the given list of items in a single query
	item_prices = frappe.db.get_all(
	  'Item Price',
	  fields=['item_code', 'uom', 'price_list_rate as rate'],
	  filters={'item_code': ['in', item_codes]},
	  ignore_permissions=True
	)
	# Group prices by item name
	# Initialize an empty dictionary to store prices grouped by item code
	price_map = {}

	# Iterate through the fetched prices
	for price in item_prices:
		item_code = price['item_code']

		# If this item code is not yet in the price_map, initialize an empty list
		if item_code not in price_map:
			price_map[item_code] = []

		# Append the current UOM and rate to the item's list of prices
		price_map[item_code].append({
			'uom': price['uom'],
			'rate': price['rate'],
			'quantity': _get_item_stock(item_code, price['uom'])
		})
	return price_map


def get_items_prices(**kwargs):
	item_group = kwargs.get('item_group')

	filters = {}
	if item_group and item_group != 'All Item Groups':
		filters['item_group'] = item_group

	# Fetch all items in one query
	items = frappe.get_all(
		'Item',
		fields=[
			'name', 'item_name', 'item_code', 'image', 'description', 'item_group',
			'standard_rate', 'stock_uom'
		],
		filters=filters,
		ignore_permissions=True
	)

	# Fetch item prices for all items at once
	item_codes = [item['item_code'] for item in items]
	prices_map = get_bulk_item_prices(item_codes)  # fetch prices for all items in one query
	# Iterate over each item and attach its uom_prices
	for item in items:
		uom_prices = prices_map.get(item['item_code'], [])
		item['stock_quantity'] = uom_prices[0]['quantity']
		item['stock_price'] = uom_prices[0]['rate']
		item['uom_prices'] = uom_prices  # Add the uom_prices list to the item
	frappe.local.response['data'] = items


class ItemAPI:
	@staticmethod
	def get(cls, **kwargs):
		get_items_prices(**kwargs)
