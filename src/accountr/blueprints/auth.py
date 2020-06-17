from http import HTTPStatus

from flask import (
    Blueprint,
    request,
    session,
)

from ..database import db
from ..services import (
    AuthService,
    AuthError,
)


bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['POST'])
def login():
    request_json = request.json
    email = request_json['email']
    password = request_json['password']
    with db.connection as connection:
        service = AuthService(connection)
        try:
            user_id = service.login(email, password)
        except AuthError:
            return '', HTTPStatus.FORBIDDEN
        else:
            session['user_id'] = user_id
            return '', HTTPStatus.OK
