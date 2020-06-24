from flask import (
    Blueprint,
    jsonify,
    request,
)
from flask.views import MethodView

from accountr.auth import auth_required
from ..database import db
from ..services.operations import (
    OperationsService
)
from ..services.types import (
    TypesService
)
from ..services.categories import (
    CategoriesService
)
from http import HTTPStatus

bp = Blueprint('operations', __name__)


class OperationsView(MethodView):
    """
    Обработка запросов о работе с операциями (/operations)
    post - создание операции
    """

    @auth_required
    def post(self, user):
        request_json = request.json
        user_id = user['id']
        type_id = request_json.get('type_id')
        category_id = request_json.get('category_id')

        with db.connection as con:
            service = TypesService(con)
            types = service.get_type(type_id)
            if not types:
                return '', HTTPStatus.BAD_REQUEST

            if category_id:
                service = CategoriesService(con)
                category = service.get_category(category_id)
                if not category:
                    return '', HTTPStatus.BAD_REQUEST
                if user_id != category['user_id']:
                    return '', HTTPStatus.FORBIDDEN

            service = OperationsService(con)
            category = service.create_operation(user_id, request_json)
            return jsonify(category), HTTPStatus.CREATED


class OperationView(MethodView):
    """
    Обработка запросов о работе с заданной операцией (/operations/<id>)
    get - получение информации об операции
    path - изменение операции
    delete - удаление операции
    """
    @auth_required
    def get(self, operation_id, user):
        user_id = user['id']
        with db.connection as con:
            service = OperationsService(con)
            operation = service.get_operation(operation_id)
            if user_id != operation['user_id']:
                return '', HTTPStatus.FORBIDDEN
            return jsonify(operation), HTTPStatus.OK

    @auth_required
    def patch(self, operation_id, user):
        request_json = request.json
        user_id = user['id']
        type_id = request_json.get('type_id')
        category_id = request_json.get('category_id')
        with db.connection as con:
            if type_id:
                service = TypesService(con)
                types = service.get_type(type_id)
                if not types:
                    return '', HTTPStatus.BAD_REQUEST

            if category_id:
                service = CategoriesService(con)
                category = service.get_category(category_id)
                if not category:
                    return '', HTTPStatus.BAD_REQUEST
                if user_id != category['user_id']:
                    return '', HTTPStatus.FORBIDDEN

            service = OperationsService(con)
            operation = service.get_operation(operation_id)
            if not operation:
                return '', HTTPStatus.BAD_REQUEST
            if user_id != operation['user_id']:
                return '', HTTPStatus.FORBIDDEN
            category = service.update_operation(operation_id, request_json)
            return jsonify(category), HTTPStatus.OK

    @auth_required
    def delete(self, operation_id, user):
        user_id = user['id']
        with db.connection as con:
            service = OperationsService(con)
            operation = service.get_operation(operation_id)
            if not operation:
                return '', HTTPStatus.BAD_REQUEST
            if user_id != operation['user_id']:
                return '', HTTPStatus.FORBIDDEN
            service.delete_operation(operation_id)
        return '', HTTPStatus.NO_CONTENT


bp.add_url_rule('', view_func=OperationsView.as_view('operations'))
bp.add_url_rule('/<int:operation_id>', view_func=OperationView.as_view('operation'))