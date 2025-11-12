import requests
from flask import session


class WeatherService:
    @staticmethod
    def search(keyword):
        params = {
            'name': keyword,
            'lang': 'vi'
        }

        data = requests.get('https://geocoding-api.open-meteo.com/v1/search', params=params).json()

        if 'results' not in data:
            return []

        results = data['results']
        fields = ['admin1', 'country', 'id', 'latitude', 'longitude', 'name']

        return [
            {field: result[field] for field in fields if field in result}
            for result in results
        ]

    @staticmethod
    def info(latitude, longitude, time, option):
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'hourly': option,
            'model': 'best_match',
            'timezone': 'Asia/Bangkok',
            'start_date': time,
            'end_date': time,
        }

        data = requests.get('https://api.open-meteo.com/v1/forecast', params=params).json()

        return {
            'unit': data['hourly_units'][option],
            'data': data['hourly'][option]
        }

    @staticmethod
    def map(areas):
        filtered_areas = []

        location = session['location']

        filtered_areas.append({
            'area': location['district'],
            'latitude': location['latitude'],
            'longitude': location['longitude']
        })

        for area in areas:
            new_area = area.name

            if area.admin1:
                new_area += f', {area.admin1}'

            if area.country:
                new_area += f', {area.country}'

            filtered_areas.append({
                'area': new_area,
                'latitude': area.latitude,
                'longitude': area.longitude
            })

        latitudes = ','.join(str(filtered_area['latitude']) for filtered_area in filtered_areas)
        longitudes = ','.join(str(filtered_area['longitude']) for filtered_area in filtered_areas)

        params = {
            'latitude': latitudes,
            'longitude': longitudes,
            'current': 'temperature_2m,weather_code',
            'model': 'best_match',
            'timezone': 'Asia/Bangkok'
        }

        data = requests.get('https://api.open-meteo.com/v1/forecast', params=params).json()
        data = [data] if isinstance(data, dict) else data

        return [
            {
                'area': filtered_areas[i]['area'],
                'latitude': data[i]['latitude'],
                'longitude': data[i]['longitude'],
                'temperature_2m': data[i]['current']['temperature_2m'],
                'weather_code': data[i]['current']['weather_code']
            }
            for i in range(len(data))
        ]
