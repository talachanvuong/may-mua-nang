from flask import Blueprint, render_template

from app.utils.decorators import anonymous_required

landing_dp = Blueprint('landing', __name__)


@landing_dp.route('/')
@anonymous_required
def index():
    return render_template('landing.html')
