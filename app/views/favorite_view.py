from flask import Blueprint, redirect, render_template, request, session, url_for

from app.services.favorite_service import FavoriteService
from app.utils.decorators import token_required

favorite_bp = Blueprint('favorite', __name__)


@favorite_bp.route('/add', methods=['POST'])
@token_required
def add():
    user = session['user']

    place = request.form['id']
    name = request.form['name']
    admin1 = request.form.get('admin1')
    country = request.form.get('country')
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    data = {
        'place': place,
        'name': name,
        'latitude': latitude,
        'longitude': longitude,
        'user': user['id']
    }

    if admin1:
        data['admin1'] = admin1

    if country:
        data['country'] = country

    FavoriteService.add(data)

    return redirect(url_for('favorite.get_all'))


@favorite_bp.route('/remove', methods=['POST'])
@token_required
def remove():
    user = session['user']

    place = request.form['place']

    FavoriteService.remove(user['id'], place)

    return redirect(url_for('favorite.get_all'))


@favorite_bp.route('/get_all')
@token_required
def get_all():
    user = session['user']
    favorites = FavoriteService.get_all(user['id'])

    return render_template('favorite.html', favorites=favorites)
