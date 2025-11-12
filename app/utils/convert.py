from datetime import datetime, timedelta


def time_ago(time):
    local_time = time + timedelta(hours=7)
    now = datetime.now()
    delta = now - local_time

    seconds = int(delta.total_seconds())

    if seconds < 60:
        return f'{seconds} giây trước'

    minutes = seconds // 60

    if minutes < 60:
        return f'{minutes} phút trước'

    hours = minutes // 60

    if hours < 24:
        return f'{hours} giờ trước'

    days = hours // 24

    return f'{days} ngày trước'


def weather_icon(weather_code):
    icons = {
        0: '☀️', 1: '🌤️', 2: '⛅', 3: '☁️',
        45: '🌫️', 48: '🌁',
        51: '🌦️', 53: '🌦️', 55: '🌧️',
        56: '🌧️', 57: '🌧️',
        61: '🌧️', 63: '🌧️', 65: '🌧️',
        66: '🌧️', 67: '🌧️',
        71: '🌨️', 73: '🌨️', 75: '🌨️',
        77: '❄️',
        80: '🌦️', 81: '🌧️', 82: '🌧️',
        85: '❄️', 86: '🌨️',
        95: '⛈️', 96: '🌩️', 99: '🌩️'
    }

    return icons.get(weather_code, '🌈')
