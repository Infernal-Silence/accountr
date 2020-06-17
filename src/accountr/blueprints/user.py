from sqlite3 import IntegrityError
from flask import (
	Blueprint,
	jsonify,
	request,
)
from flask.views import MethodView
from werkzeug.security import generate_password_hash

from database import db
from services.users import UserService, UsersService
from auth import auth_required


bp = Blueprint('users', __name__)


class UsersView(MethodView):
	def post():
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
	def get(user_id):

		return 

bp.add_url_rule('/', view_func=UsersView.as_view('users'))
bp.add_url_rule('/<int:user_id>/', view_func=UserView.as_view('user'))