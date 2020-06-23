from http import HTTPStatus

from flask import (
    Blueprint,
    request,
)

from ..auth import auth_required
from ..database import db
from ..services import (
    ReportService,
)


bp = Blueprint('report', __name__)


@bp.route('')
@auth_required
def get_report(user):
    user_id = user['id']
    with db.connection as connection:
        service = ReportService(connection)
        report = service.get_report(user_id, request.args)
        return report, HTTPStatus.OK
