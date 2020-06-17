import sqlite3

class UsersService(object):
	"""docstring for UsersSevice"""
	def __init__(self, connection):
		self.connection = connection

	def add_new_user(self, user_info):
		try:
			cur = self.connection.execute("""
				INSERT INTO users (first_name, last_name, email, password)
				VALUES (?, ?, ?, ?);""",
				(user_info['first_name'],
					user_info['last_name'],
					user_info['email'],
					user_info['password']))
		except sqlite3.IntegrityError:
			return None
		cur = self.connection.execute("""
			SELECT id, first_name, last_name, email 
			FROM users 
			ORDER BY id DESC 
			LIMIT 1
			""")
		created_user = cur.fetchone()
		return dict(created_user)

class UserService(object):
	def __init__(self, connection):
		self.connection = connection
	def get_by_id(self, user_id):
		cur = self.connection.execute("""
			SELECT id, first_name, last_name, email
			FROM users
			WHERE id = ?""",
			(user_id,))
		user = cur.fetchone()
		if not user:
			return  None
		return dict(user)