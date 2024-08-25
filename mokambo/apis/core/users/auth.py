import datetime

import frappe
import jwt
from frappe import _

from mokambo.apis.core.users.jwt_decorator import SECRET_KEY


def generate_jwt_token(user):
	payload = {
		'user': user,
		'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)  # Token expiration
	}
	token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
	return token


@frappe.whitelist(allow_guest=True)
def login(username=None, password=None):
	# Check if the username or password is missing
	if not username or not password:
		frappe.local.response["http_status_code"] = 400
		frappe.local.response["message"] = _('Username and password are required')
		return
	# return {_('Username and password are required')}
	try:
		login_manager = frappe.auth.LoginManager()
		login_manager.authenticate(username, password)
		login_manager.post_login()
	except frappe.exceptions.AuthenticationError:
		frappe.local.response["http_status_code"] = 400
		frappe.local.response["message"] = _('Invalid username or password')
	token = generate_jwt_token(username)

	user = frappe.get_doc("User", username)
	try:
		cashier_user = frappe.get_doc("Cashier", user)
		branch = cashier_user.branch
	except frappe.DoesNotExistError:
		branch = None

	frappe.local.response['data'] = {
		'token': token,
		'user': user.username,
		'full_name': user.full_name,
		'branch': branch,
	}

	# Clear unwanted keys from the response
	frappe.local.response.pop('message', None)
	frappe.local.response.pop('home_page', None)
	frappe.local.response.pop('full_name', None)
