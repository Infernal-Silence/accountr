from sqlite3 import IntegrityError

from .base import BaseService
from .exceptions import ServiceError


class UsersError(ServiceError):
	pass

class UserAlreadyExistError(UsersError):
	pass

class UsersService(BaseService):
	"""Обработка работы с пользователями (/users)
	add_new_user - добавляет нового пользователя в базу данных
	get_by_id - получает информацию о пользователе с указанным id"""

	def add_new_user(self, user_info):
		"""Добавляет пользователя с параметрами user_info в базу данных,
		возвращает сущность пользователя (без пароля) в виде словаря"""
		try:
			cur = self.connection.execute("""
				INSERT INTO users (first_name, last_name, email, password)
				VALUES (?, ?, ?, ?);""",
				(user_info['first_name'],
					user_info['last_name'],
					user_info['email'],
					user_info['password'])
				)
		except IntegrityError:
			raise UserAlreadyExistError
		cur = self.connection.execute("""
			SELECT id, first_name, last_name, email 
			FROM users 
			ORDER BY id DESC 
			LIMIT 1
			""")
		created_user = cur.fetchone()
		return dict(created_user)

