from functools import wraps

import frappe
import jwt
from frappe import _

# Secret key for encoding and decoding JWT tokens
SECRET_KEY = '12b6c68d653941aeaf9048f142f1c79c'


def jwt_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		token = frappe.request.headers.get('Authorization')
		if not token:
			return {
				'status': 'error',
				'message': _('Token is missing')
			}, 401
		try:
			payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
			frappe.local.user = frappe.get_doc("User", payload['user'])
		except jwt.ExpiredSignatureError:
			return {
				'status': 'error',
				'message': _('Token has expired')
			}, 401
		except jwt.InvalidTokenError:
			return {
				'status': 'error',
				'message': _('Invalid token')
			}, 401
		return f(*args, **kwargs)
	return decorated_function
