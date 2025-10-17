from flask import Blueprint, redirect, render_template, url_for
from flask_dance.contrib.google import google

landing_dp = Blueprint('landing', __name__)


@landing_dp.route('/')
def index():
    if not google.authorized:
        return render_template('landing.html')
    else:
        return redirect(url_for(''))  # Set value to homepage
