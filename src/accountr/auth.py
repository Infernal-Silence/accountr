from functools import wraps

from flask import session

from database import db

# Неработающий декторатор, всегда возвращает user_id = 1
def auth_required(view_func):
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		return view_func(*args, **kwargs, user_id=1)
	return wrapper