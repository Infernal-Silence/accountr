from http import HTTPStatus

from flask import (
	Blueprint,
	jsonify,
	request,
)
from flask.views import MethodView
from werkzeug.security import generate_password_hash

from ..database import db
from ..services.users import (
	UsersService,
	UserAlreadyExistError,
	UserNotFoundError
)
from accountr.auth import auth_required


bp = Blueprint('users', __name__)


class UsersView(MethodView):
	"""Обработка запросов о работе с пользователями (/users)
	post - регистрация
	get - получение информации о пользователе"""

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
			try:
				created_user = service.add_new_user(user_info)
			except UserAlreadyExistError:
				return '', HTTPStatus.CONFLICT
		return jsonify(created_user), HTTPStatus.CREATED

	@auth_required
	def get(self, user_id = None):
		with db.connection as con:
			service = UsersService(con)
			try:
				user = service.get_by_id(user_id)
			except UserNotFoundError:
				return '', HTTPStatus.NOT_FOUND
		return jsonify(user), HTTPStatus.OK

bp.add_url_rule('/', view_func=UsersView.as_view('users'))