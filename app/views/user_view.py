from flask import Blueprint, redirect, render_template, session, url_for

from app.services.user_service import UserService
from app.utils.decorators import token_required

user_bp = Blueprint('user', __name__)


@user_bp.route('/me')
@token_required
def me():
    user = UserService.me_info()
    return render_template('user_me.html', user=user)


@user_bp.route('/logout')
@token_required
def logout():
    session.pop('google_oauth_token', None)
    return redirect(url_for('landing.index'))
