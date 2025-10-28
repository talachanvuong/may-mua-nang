import requests


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
