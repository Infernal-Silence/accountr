from werkzeug.security import check_password_hash

from .base import BaseService
from .exceptions import ServiceError


class AuthError(ServiceError):
    pass


class AuthService(BaseService):
    def login(self, email, password):
        cur = self.connection.execute(
            'SELECT'
            ' id,'
            ' password '
            'FROM users '
            'WHERE email = ?',
            (email,),
        )
        row = cur.fetchone()
        if row is None:
            raise AuthError
        if not check_password_hash(row['password'], password):
            raise AuthError
        return row['id']
