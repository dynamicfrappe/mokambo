import frappe

from mokambo.apis.core.users.jwt_decorator import jwt_required


def get_item_stock(item_code, warehouse=None):
	filters = {"item_code": item_code}
	if warehouse:
		filters["warehouse"] = warehouse
	# Fetch the stock quantity
	bin_data = frappe.get_all("Bin", filters=filters, fields=["warehouse", "actual_qty"])
	stock_quantities = {entry["warehouse"]: entry["actual_qty"] for entry in bin_data}
	return stock_quantities


def get_item_price(item_code, price_list="Standard Selling"):
	item_price = frappe.get_value(
		"Item Price",
		{"item_code": item_code, "price_list": price_list},
		"price_list_rate"
	)
	return item_price


def get_item_stock_and_price(item_code, warehouse=None, price_list="Standard Selling"):
	# Get stock quantity
	stock = get_item_stock(item_code, warehouse)

	# Get item price
	price = get_item_price(item_code, price_list)

	return {
		"stock_quantity": stock,
		"price": price
	}


@frappe.whitelist(allow_guest=True)
@jwt_required
def get_stock_items(item_group=None, branch=None, warehouse=None, price_list="Standard Selling"):
	# Prepare base filters
	item_filters = []
	params = [price_list]

	if item_group:
		item_filters.append("i.item_group = %s")
		params.append(item_group)

	if branch:
		item_filters.append("i.custom_branch = %s")
		params.append(branch)

	# Handle warehouse filter
	warehouse_filter = "AND b.warehouse = %s" if warehouse else ""
	if warehouse:
		params.append(warehouse)

	# Combine filters
	item_filter = " AND ".join(item_filters) if item_filters else "1=1"

	# Execute query
	items = frappe.db.sql("""
		SELECT
			i.name,
			i.item_code,
			i.item_name,
			i.item_group,
			i.image,
			i.stock_uom,
			i.custom_branch as branch,
			MAX(IFNULL(b.actual_qty, 0)) as stock_quantity,
			MAX(IFNULL(ip.price_list_rate, 0)) as price
		FROM
			`tabItem` i
		LEFT JOIN
			`tabBin` b ON i.item_code = b.item_code {warehouse_filter}
		LEFT JOIN
			`tabItem Price` ip ON i.item_code = ip.item_code AND ip.price_list = %s
		WHERE
			{item_filter}
		GROUP BY
			i.name, i.item_code, i.item_name, i.item_group, i.image, i.stock_uom
		""".format(
		warehouse_filter=warehouse_filter,
		item_filter=item_filter
	), tuple(params), as_dict=True)

	# Prepare the response
	frappe.local.response['data'] = items
