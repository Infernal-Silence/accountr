from flask import (
    Blueprint,
    jsonify,
)
from flask.views import MethodView

from accountr.auth import auth_required
from ..database import db
from ..services.types import (
    TypesService
)
from http import HTTPStatus

bp = Blueprint('types', __name__)


class TypesView(MethodView):
    """
    Обработка запросов о работе с типами операций (/types)
    get - получение всех типов операций
    """

    @auth_required
    def get(self, user):
        with db.connection as con:
            service = TypesService(con)
            types = service.get_types()
            return jsonify(types), HTTPStatus.OK


class TypeView(MethodView):
    """
    Обработка запросов о работе с заданным типом операции (/types/<id>)
    get - получение информации о типе операции
    """
    @auth_required
    def get(self, type_id, user):
        with db.connection as con:
            service = TypesService(con)
            operation = service.get_type(type_id)
            return jsonify(operation), HTTPStatus.OK


bp.add_url_rule('', view_func=TypesView.as_view('types'))
bp.add_url_rule('/<int:type_id>', view_func=TypeView.as_view('type'))