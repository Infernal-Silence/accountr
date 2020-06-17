from sqlite3 import IntegrityError
from flask import (
	Blueprint,
	jsonify,
	request,
)
from flask.views import MethodView
from werkzeug.security import generate_password_hash

from accountr.database import db
from accountr.services.users import UserService, UsersService
from accountr.auth import auth_required


bp = Blueprint('users', __name__)


class UsersView(MethodView):
	def post(self):
		request_json = request.json
		user_info = {
			'first_name':request_json['first_name'],
			'last_name':request_json['last_name'],
			'email':request_json['email'],
			'password':generate_password_hash(request_json['password'])
			}
		with db.connection as con:
			service = UsersService(con)
			created_user = service.add_new_user(user_info)
			if not created_user:
				return '',409
		return jsonify(created_user), 200


class UserView(MethodView):
	@auth_required
	def get(self, user_id = None):
		with db.connection as con:
			service = UserService(con)
			user = service.get_by_id(user_id)
			if not user:
				return  '', 404
		return jsonify(user), 200

bp.add_url_rule('/', view_func=UsersView.as_view('users'))
bp.add_url_rule('/', view_func=UserView.as_view('user'))