from datetime import datetime, timezone

import requests
from flask import current_app, session
from flask_dance.contrib.google import google


def inject_location():
    if not google.authorized:
        return dict()

    exp = google.token['expires_at']
    now = datetime.now(timezone.utc).timestamp()

    if now >= exp:
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
