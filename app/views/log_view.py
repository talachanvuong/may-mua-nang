from flask import Blueprint, render_template, session

from app.services.log_service import LogService
from app.utils.convert import time_ago
from app.utils.decorators import token_required

log_bp = Blueprint('log', __name__)


@log_bp.route('/get_all')
@token_required
def get_all():
    user = session['user']
    logs = LogService.get_all(user['id'])

    for log in logs:
        log['created_at'] = time_ago(log['created_at'])

    return render_template('log.html', logs=logs)
