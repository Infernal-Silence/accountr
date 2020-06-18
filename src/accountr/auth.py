from functools import wraps

from flask import session

from database import db


def auth_required(view_func):
	'''Декоратор проверки авторизации пользователя.
	Добавляет параметр user_id к декорируемой функции
	Если пользователь не авторизирован, возвращается код ошибки 403'''
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		user_id = session.get('user_id')
		if not user_id:
			return '', 403
		with db.connection as con:
			cur = con.execute(
				'SELECT users.id '
				'FROM users '
				'WHERE id = ?',
				(user_id,),
			)
			user = cur.fetchone()
		if not user:
			return '', 403
		return view_func(*args, **kwargs, user_id = user_id)
	return wrapper