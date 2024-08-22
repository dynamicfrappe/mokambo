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
def login(username, password):
	try:
		login_manager = frappe.auth.LoginManager()
		login_manager.authenticate(username, password)
		login_manager.post_login()
	except frappe.exceptions.AuthenticationError:
		return {
			'status': 'error',
			'message': _('Invalid username or password')
		}
	token = generate_jwt_token(username)
	return {
		'status': 'success',
		'token': token
	}
