import frappe
from frappe import _

from mokambo.apis.jwt_decorator import generate_jwt_token


@frappe.whitelist(allow_guest=True)
def login_user(username=None, password=None):
	# Check if username or password is missing
	if not username or not password:
		frappe.local.response["http_status_code"] = 400
		frappe.local.response["message"] = _('Username and password are required')
		return

	# Fetch the user by mobile number
	user = frappe.db.get_value(
		'User',
		{'name': username},
		['name', 'enabled'],
	   	as_dict=True
	)

	# Check if the user exists
	if not user:
		frappe.local.response["http_status_code"] = 404
		frappe.local.response["message"] = _('User not found')
		return

	# Check if the user is enabled
	if not user.enabled:
		frappe.local.response["http_status_code"] = 403
		frappe.local.response["message"] = _('User account is disabled')
		return

	# Check the password using Frappe's authentication mechanism
	try:
		frappe.auth.check_password(user.name, password)
		print('check password ==> ', frappe.auth.check_password(user.name, password))
		# Perform the actual login action
		frappe.local.login_manager.authenticate(user.name, password)
		frappe.local.login_manager.post_login()
	except frappe.AuthenticationError:
		frappe.local.response["http_status_code"] = 401
		frappe.local.response["message"] = _('Invalid password')
		return

	# Generate JWT token for the user
	token = generate_jwt_token(user.name)

	frappe.local.response['data'] = {
		'token': token,
		'user': user.username or user.name,
		'full_name': user.full_name or user.name,
		# 'branch': branch,
	}

	# Clear unwanted keys from the response
	frappe.local.response.pop('message', None)
	frappe.local.response.pop('home_page', None)
	frappe.local.response.pop('full_name', None)
