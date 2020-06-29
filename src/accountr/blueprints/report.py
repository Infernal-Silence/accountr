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
    if request.args.get('period') and (request.args.get('start_date') or request.args.get('end_date')):
        return '', HTTPStatus.BAD_REQUEST
    with db.connection as connection:
        service = ReportService(connection)
        report = service.get_report(user_id, request.args)
        return report, HTTPStatus.OK
