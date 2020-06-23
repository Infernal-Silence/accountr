from functools import wraps
from http import HTTPStatus

from flask import session

from .database import db


def auth_required(view_func):
	'''Декоратор проверки авторизации пользователя.
	Добавляет параметр user с данными пользователя (в словаре) к декорируемой функции
	Если пользователь не авторизирован, возвращается код ошибки 401'''
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		user_id = session.get('user_id')
		if not user_id:
			return '', HTTPStatus.UNAUTHORIZED
		with db.connection as con:
			cur = con.execute("""
				SELECT id, first_name, last_name, email
				FROM users 
				WHERE id = ?
				LIMIT 1;""",
				(user_id,),
			)
			user = cur.fetchone()
		if not user:
			return '', HTTPStatus.UNAUTHORIZED
		return view_func(*args, **kwargs, user = dict(user))
	return wrapper