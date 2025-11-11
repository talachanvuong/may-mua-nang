from datetime import datetime, timedelta

import requests
from flask import current_app, session
from flask_dance.contrib.google import google

from app.services.track_service import TrackService


def inject_location():
    if not google.authorized:
        return dict()

    user = session['user']
    track = TrackService.get_by_access_token(user['id'], google.token['access_token'])
    now = datetime.now()

    if not track or now >= track.expires_at + timedelta(hours=7):
        return dict()

    params = {
        'apiKey': current_app.config['IPGEOLOCATION_API_KEY'],
        'fields': 'location.district,location.country_code2,location.latitude,location.longitude'
    }

    location = requests.get(f'https://api.ipgeolocation.io/v2/ipgeo', params=params).json()['location']
    district = location.get('district', location['country_code2'])

    session['location'] = {
        'district': district,
        'latitude': location['latitude'],
        'longitude': location['longitude'],
    }

    return dict(location=district)
