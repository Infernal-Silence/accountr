from flask import (
    Blueprint,
    jsonify,
    request,
)
from flask.views import MethodView

from accountr.auth import auth_required
from ..database import db
from ..services.categories import (
    CategoriesService
)
from http import HTTPStatus

bp = Blueprint('categories', __name__)


class CategoriesView(MethodView):
    """
    Обработка запросов о работе с категориями (/categories)
    get - получение информации о категориях пользователя
    post - создание категории
    """

    @auth_required
    def get(self, user):
        user_id = user['id']
        with db.connection as con:
            service = CategoriesService(con)
            categories = service.get_categories(user_id)
            return jsonify(categories), HTTPStatus.OK

    @auth_required
    def post(self, user):
        request_json = request.json
        parent_id = request_json.get('parent_id')
        user_id = user['id']

        with db.connection as con:
            service = CategoriesService(con)
            if parent_id:
                parent_category = service.get_category(parent_id)
                if not parent_category:
                    return '', HTTPStatus.BAD_REQUEST
            category = service.create_category(user_id, request_json)
            return jsonify(category), HTTPStatus.CREATED


class CategoryView(MethodView):
    """
    Обработка запросов о работе с заданной категорией (/categories/<id>)
    get - получение информации о категории
    path - изменение категории
    delete - удаление категории
    """
    @auth_required
    def get(self, category_id, user):
        user_id = user['id']
        with db.connection as con:
            service = CategoriesService(con)
            category = service.get_category(category_id)
            if user_id != category['user_id']:
                return '', HTTPStatus.FORBIDDEN
            return jsonify(category), HTTPStatus.OK

    @auth_required
    def patch(self, category_id, user):
        request_json = request.json
        parent_id = request_json.get('parent_id')
        user_id = user['id']
        with db.connection as con:
            service = CategoriesService(con)
            if parent_id:
                parent_category = service.get_category(parent_id)
                if not parent_category:
                    return '', HTTPStatus.BAD_REQUEST
                if user_id != parent_category['user_id']:
                    return '', HTTPStatus.FORBIDDEN
            category = service.get_category(category_id)
            if not category:
                return '', HTTPStatus.BAD_REQUEST
            if user_id != category['user_id']:
                return '', HTTPStatus.FORBIDDEN
            category = service.update_category(category_id, request_json)
            return jsonify(category), HTTPStatus.OK

    @auth_required
    def delete(self, category_id, user):
        user_id = user['id']
        with db.connection as con:
            service = CategoriesService(con)
            category = service.get_category(category_id)
            if not category:
                return '', HTTPStatus.BAD_REQUEST
            if user_id != category['user_id']:
                return '', HTTPStatus.FORBIDDEN
            category = service.delete_category(user_id, category_id)
        return '', HTTPStatus.NO_CONTENT


bp.add_url_rule('', view_func=CategoriesView.as_view('categories'))
bp.add_url_rule('/<int:category_id>', view_func=CategoryView.as_view('category'))
