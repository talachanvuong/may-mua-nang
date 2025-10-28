from flask import Blueprint, redirect, render_template, request, session, url_for

from app.utils.decorators import token_required

user_bp = Blueprint('user', __name__)


@user_bp.route('/me', methods=['GET', 'POST'])
@token_required
def me():
    if request.method == 'POST':
        theme = request.form['theme']
        session['theme'] = theme

        return redirect(url_for('user.me'))

    return render_template('user_me.html', user=session['user'])


@user_bp.route('/logout')
@token_required
def logout():
    session.pop('google_oauth_token', None)
    session.pop('user', None)
    session.pop('location', None)

    return redirect(url_for('landing.index'))
